"""Independent checker for the Phase B2.3 certificate (data/B2_c4hat_certificate.json), 192 bits.

It shares no code with b2_cert.py, b2_quartic.py or b2_carrier.py, and it uses no Taylor series:
- Functions. It derives the 16 functions itself, by SymPy differentiation of the pair terms along fields it builds
  from the vertex labels (psi(sigma) = sigma^(-r/2), divided by r W_r), and compares them with the stored strings.
  Their first, second and third derivatives come from its own chain rule; all are compiled to straight-line Arb code.
- Divided differences, from the identity f_hat(p, q) = int_0^1 f'(q + t (p - q)) dt, with rational subdivision of
  t in [0, 1]: at the centre of a box the composite midpoint rule with its exact remainder
  (|T|^3/24) delta^2 f'''(q + T delta); over a box, range sums of f' and of f'' (for the slopes
  d_q f_hat = int f'' dt and d_delta f_hat = int t f'' dt). Near the diagonal the integrand is nearly constant and
  the rule loses nothing; at delta = 0 it returns f'(q) exactly. The subdivision is doubled when a bound is not
  confirmed.
- Kernel vector. v = (Mh22, -Mh12) and the homogeneous quartic carrier
      c4_hat = [Qh(v) - 3 bAh(v)^2/hAh - 3 bEh(v)^2/hEh] / (v1^2 + v2^2)^2,
  never the chart rho. On a box: the mean-value form around the centre, with the partial derivatives carried by
  forward-mode dual numbers; the box is bisected when a bound is not confirmed.
- Curve. The imported B1 balls are re-verified by its own strict parametric interval Newton inclusion.
- Structure: the claim, the formulas, the pinned B1 semantic hash (and the B1 file itself), the imported boxes and
  metadata, gap-free coverage, both endpoints (stored enclosures must overlap its own), the semantic hash.
"""
import hashlib
import itertools
import json
import pathlib

import sympy as sp
from flint import arb, ctx, fmpq

CHECK_PREC = 192
B1_SEMANTIC_PINNED = "616817fcc70e0fab7f106404e5e5332b17b9c4480bd440355f1ac5257a8518c6"
EXPECTED_CLAIM = {"quantity": "c4_hat", "relation": ">", "value": "0",
                  "curve": "closed physical T2g curve: p = P_T(q) for 0 <= q < q_c, and the corner p = q = q_c",
                  "q_interval": ["0", "101/50"]}
EXPECTED_FORMULAS = {
    "chart": "rho = -Mh12/Mh22",
    "carrier": "c4_hat = (Qh(1,rho) - 3/2*bAh(1,rho)**2 - 3*bEh(1,rho)**2/hEh)/(1 + rho**2)**2",
    "Qh(1,rho)": "Qh_uuuu + 4*rho*Qh_uuuv + 6*rho**2*Qh_uuvv + 4*rho**3*Qh_uvvv + rho**4*Qh_vvvv",
    "bXh(1,rho)": "bXh_uu + 2*rho*bXh_uv + rho**2*bXh_vv  (X = A, E)",
    "hA_hat": "2 (exact: g_hA = 2*r + 2)",
    "divided_difference_far": "f_hat = (f(q + delta) - f(q))/delta",
    "divided_difference_near": ("f_hat = sum_{k<K} c_{2k+1}(m)*h**(2k) + h**(2K)*c_{2K+1}(hull(q, q + delta)), "
                                "m = q + delta/2, h = delta/2, c_j = f^(j)/j!"),
    "q0_rule": "f_hat = (f(p0) - f(0))/p0 with the exact values f(0), p0 = P_T(0)",
    "corner_rule": "f_hat = f'(q_c) (diagonal derivatives); no division by p - q",
    "raw_c4": "c4 = q*W_q*(p - q)*c4_hat (unit n): zero at q = 0 and at the corner",
}
ORDER = ("M11", "M12", "M22", "Q_uuuu", "Q_uuuv", "Q_uuvv", "Q_uvvv", "Q_vvvv", "bA_uu", "bA_uv", "bA_vv",
         "bE_uu", "bE_uv", "bE_vv", "hA", "hE")
R_, X_, Y_, L2_, L3_ = sp.symbols("r X Y L2 L3", positive=True)
SPLIT_MAX = 6


# ---- independent derivation --------------------------------------------------------------------------------------------
def _labels():
    return list(itertools.product([-1, 1], repeat=3))


def _vec(f):
    return [c for s in _labels() for c in f(s)]


def _directional(dir_orders):
    """d^n/dt_1^o_1 ... of sum_pairs psi(|x_i - x_j|^2) at the cube along the given directions, divided by r W_r,
    with psi(sigma) = sigma^(-r/2) (its derivatives at sigma = 1, 2, 3 in r, X = 2^(-r/2), Y = 3^(-r/2))."""
    dirs = [d for d, _ in dir_orders]
    orders = [o for _, o in dir_orders]
    n = sum(orders)
    t = sp.symbols(f"t0:{len(dirs)}")
    mono = sp.Mul(*[t[a] ** orders[a] for a in range(len(dirs))])
    L = _labels()
    tot = 0
    for i, j in itertools.combinations(range(8), 2):
        base = [sp.Rational(L[i][c] - L[j][c], 2) for c in range(3)]
        sv = int(sum(b * b for b in base))
        vec = [base[c] + sum(t[a] * (dirs[a][3 * i + c] - dirs[a][3 * j + c]) for a in range(len(dirs)))
               for c in range(3)]
        ds = sp.expand(sum(v * v for v in vec) - sv)
        powr = {1: sp.Integer(1), 2: X_, 3: Y_}[sv]
        poly = 0
        for k in range(1, n + 1):
            ff = sp.Integer(1)
            for m in range(k):
                ff *= (-R_ / 2 - m)
            poly += ff * powr * sp.Integer(sv) ** (-k) * ds ** k / sp.factorial(k)
        tot += sp.Poly(sp.expand(poly), *t).coeff_monomial(mono)
    fact = sp.Mul(*[sp.factorial(o) for o in orders])
    return sp.cancel(sp.together(sp.expand(tot * fact) / (R_ * (1 + X_ + Y_ / 3))))


def derive_functions():
    shear = _vec(lambda s: [0, s[2], s[1]])                  # S_1 s
    trans = _vec(lambda s: [s[0] * s[1] * s[2], 0, 0])        # (s1 s2 s3) e_1
    u = [sp.Rational(-1, 4) * c for c in shear]
    v = [-sp.sqrt(2) / 4 * c for c in trans]
    a = [c / sp.sqrt(24) for c in _vec(lambda s: list(s))]
    e = [c / sp.sqrt(48) for c in _vec(lambda s: [2 * s[0], -s[1], -s[2]])]
    out = {"M11": _directional([(u, 2)]), "M12": _directional([(u, 1), (v, 1)]), "M22": _directional([(v, 2)])}
    for j, ch in enumerate(("uuuu", "uuuv", "uuvv", "uvvv", "vvvv")):
        parts = [(u, 4 - j)] if j < 4 else []
        if j > 0:
            parts.append((v, j))
        out["Q_" + ch] = _directional(parts)
    pairs = {"uu": [(u, 2)], "uv": [(u, 1), (v, 1)], "vv": [(v, 2)]}
    for ch, pr in pairs.items():
        out["bA_" + ch] = _directional(pr + [(a, 1)])
        out["bE_" + ch] = _directional(pr + [(e, 1)])
    out["hA"] = _directional([(a, 2)])
    out["hE"] = _directional([(e, 2)])
    return out


def _d(expr):
    return sp.diff(expr, R_) + sp.diff(expr, X_) * (-L2_ / 2 * X_) + sp.diff(expr, Y_) * (-L3_ / 2 * Y_)


def stored_expr(s):
    return sp.sympify(s, locals={"r": R_, "X": X_, "Y": Y_, "sqrt": sp.sqrt})


# ---- own compiler: SymPy -> straight-line Arb code -------------------------------------------------------------------------
def _codegen(exprs):
    red_in = [exprs[k] for k in ORDER]
    repl, red = sp.cse(red_in)
    consts, index = [], {}

    def cst(key):
        if key not in index:
            index[key] = len(consts)
            consts.append(key)
        return f"K[{index[key]}]"

    def em(e):
        if e.is_Symbol:
            return {R_: "x", X_: "X", Y_: "Y", L2_: cst(("log", 2)), L3_: cst(("log", 3))}.get(e, str(e))
        if e.is_Rational:
            return cst(("q", int(e.p), int(e.q)))
        if e.is_Pow and e.exp == sp.Rational(1, 2) and e.base.is_Integer:
            return cst(("sqrt", int(e.base)))
        if e.is_Add:
            return "(" + " + ".join(em(z) for z in e.args) + ")"
        if e.is_Mul:
            top, bot = [], []
            for z in e.args:
                if z.is_Pow and z.exp.is_Integer and z.exp < 0:
                    bot.append(em(z.base if z.exp == -1 else sp.Pow(z.base, -z.exp, evaluate=False)))
                else:
                    top.append(em(z))
            num = "*".join(top) if top else cst(("q", 1, 1))
            return f"({num})" if not bot else f"(({num})/({'*'.join(bot)}))"
        if e.is_Pow and e.exp.is_Integer:
            k, b = int(e.exp), em(e.base)
            prod = "*".join([b] * abs(k))
            return f"({prod})" if k > 0 else f"({cst(('q', 1, 1))}/({prod}))"
        raise ValueError(f"unsupported node {e}")

    body = ["def _g(x, K):", f"    X = (x * {cst(('mlog', 2))}).exp()", f"    Y = (x * {cst(('mlog', 3))}).exp()"]
    body += [f"    {s} = {em(e)}" for s, e in repl]
    body.append("    return (" + ", ".join(em(e) for e in red) + ",)")
    ns = {}
    exec("\n".join(body), ns)
    return ns["_g"], consts


def _konst(keys):
    out = []
    for key in keys:
        if key[0] == "q":
            out.append(arb(fmpq(key[1], key[2])))
        elif key[0] == "sqrt":
            out.append(arb(key[1]).sqrt())
        elif key[0] == "log":
            out.append(arb(key[1]).log())
        else:
            out.append(-arb(key[1]).log() / 2)
    return out


class Model:
    """Compiled first, second and third r-derivatives of the 16 functions (X' = -(log 2/2) X, Y' = -(log 3/2) Y)."""

    def __init__(self, funcs):
        d1 = {k: _d(funcs[k]) for k in ORDER}
        d2 = {k: _d(d1[k]) for k in ORDER}
        d3 = {k: _d(d2[k]) for k in ORDER}
        self.blocks = {}
        for name, ex in (("f1", d1), ("f2", d2), ("f3", d3)):
            self.blocks[name] = _codegen(ex)
        self._cache = {}

    def __call__(self, name, x):
        g, keys = self.blocks[name]
        ck = (name, ctx.prec)
        if ck not in self._cache:
            self._cache[ck] = _konst(keys)
        return g(x, self._cache[ck])


# ---- divided differences by the integral identity --------------------------------------------------------------------------
def _ball(lo, hi):
    return arb(lo).union(arb(hi)) if lo != hi else arb(lo)


def dd_point(model, q0, d0, n):
    """f_hat(q0 + d0, q0) for the 16 functions: composite midpoint rule on n rational subintervals of [0, 1], with
    the exact remainder (|T|^3/24) d0^2 f'''(q0 + T d0). q0, d0 may be (small) balls."""
    acc = [arb(0)] * 16
    w = fmpq(1, n)
    for i in range(n):
        mid = model("f1", q0 + arb(fmpq(2 * i + 1, 2 * n)) * d0)
        rem = model("f3", q0 + _ball(fmpq(i, n), fmpq(i + 1, n)) * d0)
        acc = [a + w * m + (w ** 3 / 24) * d0 * d0 * c for a, m, c in zip(acc, mid, rem)]
    return dict(zip(ORDER, acc))


def dd_box(model, Q, D, n):
    """Ranges over the box Q x D of f_hat = int f', d_q f_hat = int f'' and d_delta f_hat = int t f'', by a centred
    form on each subinterval T of [0, 1]: for t in T, q in Q, delta in D, with x_T = q0 + t_T d0 (thin) and the range
    X_T = Q + T D, f^(k)(q + t delta) lies in f^(k)(x_T) + f^(k+1)(X_T) E_T, E_T = (Q - q0) + (T - t_T) D + t_T (D - d0);
    the weights 1 and t are non-negative, so the integral over T lies in (int_T weight) times that ball."""
    q0, d0 = _mid(Q), _mid(D)
    val, dq, dd = [arb(0)] * 16, [arb(0)] * 16, [arb(0)] * 16
    w = fmpq(1, n)
    for i in range(n):
        ti = fmpq(2 * i + 1, 2 * n)
        T = _ball(fmpq(i, n), fmpq(i + 1, n))
        xc = q0 + ti * d0
        X = Q + T * D
        E = (Q - q0) + (T - ti) * D + ti * (D - d0)
        f1c, f2c, f2r, f3r = model("f1", xc), model("f2", xc), model("f2", X), model("f3", X)
        for k in range(16):
            b1 = f1c[k] + f2r[k] * E
            b2 = f2c[k] + f3r[k] * E
            val[k] += w * b1
            dq[k] += w * b2
            dd[k] += (w * ti) * b2
    return dict(zip(ORDER, val)), dict(zip(ORDER, dq)), dict(zip(ORDER, dd))


# ---- dual numbers (value, d/dq, d/d delta) over arb ----------------------------------------------------------------------
class Dual:
    __slots__ = ("v", "a", "b")

    def __init__(self, v, a=0, b=0):
        self.v, self.a, self.b = v, a, b

    @staticmethod
    def _c(x):
        return x if isinstance(x, Dual) else Dual(x)

    def __add__(self, o):
        o = Dual._c(o)
        return Dual(self.v + o.v, self.a + o.a, self.b + o.b)

    __radd__ = __add__

    def __neg__(self):
        return Dual(-self.v, -self.a, -self.b)

    def __sub__(self, o):
        return self + (-Dual._c(o))

    def __rsub__(self, o):
        return Dual._c(o) - self

    def __mul__(self, o):
        o = Dual._c(o)
        return Dual(self.v * o.v, self.a * o.v + self.v * o.a, self.b * o.v + self.v * o.b)

    __rmul__ = __mul__

    def __truediv__(self, o):
        o = Dual._c(o)
        q = self.v / o.v
        return Dual(q, (self.a - q * o.a) / o.v, (self.b - q * o.b) / o.v)


def carrier_v(G):
    """The homogeneous carrier with the kernel vector v = (Mh22, -Mh12); works on arb and on Dual."""
    v1, v2 = G["M22"], -G["M12"]
    w = {"uuuu": 1, "uuuv": 4, "uuvv": 6, "uvvv": 4, "vvvv": 1}
    Qv = 0
    for ch, c in w.items():
        term = G["Q_" + ch] * c
        for _ in range(ch.count("u")):
            term = term * v1
        for _ in range(ch.count("v")):
            term = term * v2
        Qv = Qv + term
    bA = v1 * v1 * G["bA_uu"] + 2 * v1 * v2 * G["bA_uv"] + v2 * v2 * G["bA_vv"]
    bE = v1 * v1 * G["bE_uu"] + 2 * v1 * v2 * G["bE_uv"] + v2 * v2 * G["bE_vv"]
    n2 = v1 * v1 + v2 * v2
    return (Qv - 3 * bA * bA / G["hA"] - 3 * bE * bE / G["hE"]) / (n2 * n2)


def _mid(x):
    return arb(x.mid())


def _exact(x):
    m, e = x.man_exp()
    e = int(e)
    return fmpq(m) * fmpq(2) ** e if e >= 0 else fmpq(m, 2 ** (-e))


def _halves(B):
    m = _mid(B)
    return [B.lower().union(m), m.union(B.upper())]


SCHEDULE = ((32, 16), (64, 32), (128, 64), (256, 128))      # (centre subintervals, box subintervals)


def box_carrier(model, Q, D, nc, ns):
    """Mean-value enclosures over Q x D of c4_hat (homogeneous v-form), hE_hat, Mh22 and |v|^2: the value at the centre
    (midpoint rule with remainder) plus the gradient over the box (dual numbers on the box ranges) times the box."""
    q0, d0 = _mid(Q), _mid(D)
    Gc = dd_point(model, q0, d0, nc)
    val, dq, dd = dd_box(model, Q, D, ns)
    if not (val["hE"] > 0 and val["M22"] > 0):
        return None
    cd = carrier_v({k: Dual(val[k], dq[k], dd[k]) for k in ORDER})
    c = carrier_v(Gc) + cd.a * (Q - q0) + cd.b * (D - d0)
    hE = Gc["hE"] + dq["hE"] * (Q - q0) + dd["hE"] * (D - d0)
    m22 = Gc["M22"] + dq["M22"] * (Q - q0) + dd["M22"] * (D - d0)
    m12 = Gc["M12"] + dq["M12"] * (Q - q0) + dd["M12"] * (D - d0)
    return {"c4_hat": c, "hE": hE, "Mh22": m22, "v_norm2": m22 * m22 + m12 * m12, "centre": carrier_v(Gc)}


def confirm_box(model, Q, D, lb_c, lb_h, lb_m, depth=0):
    """(ok, depth, n): c4_hat > lb_c, hE_hat > lb_h, Mh22 > lb_m and |v|^2 > lb_m^2 on all of Q x D. Refines the
    subdivision of [0, 1] first, then bisects the box."""
    last = SCHEDULE[0][0]
    for nc, ns in SCHEDULE:
        last = nc
        res = box_carrier(model, Q, D, nc, ns)
        if res is not None and res["c4_hat"] > arb(lb_c) and res["hE"] > arb(lb_h) and res["Mh22"] > arb(lb_m) \
                and res["v_norm2"] > arb(lb_m) * arb(lb_m):
            return True, depth, nc
    if depth >= SPLIT_MAX:
        return False, depth, last
    worst = depth
    for qq in (_halves(Q) if Q.rad() > 0 else [Q]):
        for dd_ in (_halves(D) if D.rad() > 0 else [D]):
            ok, d, n = confirm_box(model, qq, dd_, lb_c, lb_h, lb_m, depth + 1)
            if not ok:
                return False, d, n
            worst, last = max(worst, d), max(last, n)
    return True, worst, last


def _dt(G):
    return G["M11"] * G["M22"] - G["M12"] * G["M12"]


def _dt_slope(v, s):
    return s["M11"] * v["M22"] + v["M11"] * s["M22"] - 2 * v["M12"] * s["M12"]


def fd_enclosure(model, Q, D, n, depth=0, max_depth=4):
    """An enclosure of d_delta D~ over Q x D that excludes 0 (the hull over a partition of D), or None."""
    val, _, dd = dd_box(model, Q, D, n)
    Fd = _dt_slope(val, dd)
    if Fd > 0 or Fd < 0:
        return Fd
    if depth >= max_depth or D.rad() == 0:
        return None
    parts = [fd_enclosure(model, Q, h, n, depth + 1, max_depth) for h in _halves(D)]
    if any(x is None for x in parts) or not ((parts[0] > 0 and parts[1] > 0) or (parts[0] < 0 and parts[1] < 0)):
        return None
    return parts[0].union(parts[1])


def newton_curve(model, Q, D, n, iterations=12):
    """For every q in Q: D~(q, .) = det Mh(q + ., q) is strictly monotone on D (d_delta D~ excludes 0 on Q x D) and
    has a zero in D, by a strictly included interval Newton image after contraction. Every zero in D_k lies in
    N(Q, D_k) (mean value theorem), so D_(k+1) = N(Q, D_k) intersected with D_k loses none; N(Q, D_k) inside int D_k gives existence.
    Returns the final image (the unique zero lies in it for every q in Q) or None."""
    Fd = fd_enclosure(model, Q, D, n)
    if Fd is None:
        return None
    Dk = D
    for _ in range(iterations):
        q0, m = _mid(Q), _mid(Dk)
        Gc = dd_point(model, q0, m, n)
        vq, dq, _ = dd_box(model, Q, m, n)
        F = _dt(Gc) + _dt_slope(vq, dq) * (Q - q0)
        Nw = m - F / Fd
        if Nw.lower() > Dk.lower() and Nw.upper() < Dk.upper():
            return Nw
        lo = max(_exact(Nw.lower()), _exact(Dk.lower()))
        hi = min(_exact(Nw.upper()), _exact(Dk.upper()))
        if lo > hi:
            return None
        if lo == _exact(Dk.lower()) and hi == _exact(Dk.upper()):
            return None                                        # no contraction
        Dk = _ball(lo, hi)
        Fn = fd_enclosure(model, Q, Dk, n)
        if Fn is not None:
            Fd = Fn
    return None


def curve_confirmed(model, Q, D, depth=0, max_depth=4):
    """newton_curve with a finer subdivision of [0, 1], then bisection of Q. Returns (image or None, depth, n)."""
    for n in (32, 128):
        Nw = newton_curve(model, Q, D, n)
        if Nw is not None:
            return Nw, depth, n
    if depth >= max_depth or Q.rad() == 0:
        return None, depth, 128
    outs = [curve_confirmed(model, h, D, depth + 1, max_depth) for h in _halves(Q)]
    if any(o[0] is None for o in outs):
        return None, max(o[1] for o in outs), 128
    return outs[0][0].union(outs[1][0]), max(o[1] for o in outs), max(o[2] for o in outs)


# ---- certificate bookkeeping ------------------------------------------------------------------------------------------------
def _q(s):
    if "/" in s:
        a, b = s.split("/")
        return fmpq(int(a), int(b))
    return fmpq(int(s))


def _canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def semantic_hash(cert):
    return hashlib.sha256(_canon({k: v for k, v in cert.items() if k != "provenance"}).encode()).hexdigest()


def _decimal_ball(lo, hi):
    a, b = sp.Rational(lo), sp.Rational(hi)
    return _ball(fmpq(int(a.p), int(a.q)), fmpq(int(b.p), int(b.q)))


EXPECTED_COROLLARY = ("c4(q) = q W_q (P_T(q) - q) c4_hat(q) > 0 for 0 < q < q_c: q > 0, W_q > 1, and P_T(q) - q > 0 "
                      "(Paper 2, Lemma T3).")
EXPECTED_IMPORT_CHECKS = {k: True for k in (
    "B1_semantic_sha256_equals_the_pin", "q_coverage_gap_free_from_0_to_101/50", "boxes_ordered_and_nonempty",
    "every_B1_box_used", "boxes_inside_their_B1_q_range", "delta_balls_and_corner_flags_equal_to_B1",
    "B1_box_hashes_recorded", "exactly_one_corner_box_and_it_is_the_last")}
BOX_KEYS = {"index", "b1_index", "b1_box_sha256", "q_lo", "q_hi", "delta_lo", "delta_hi", "corner", "regime",
            "split_depth", "curve_reverified", "c4_hat_enclosure", "c4_hat_lower_bound", "hE_hat_lower_bound",
            "Mh22_lower_bound", "one_plus_rho2_lower_bound"}


def check(cert, root, stored_semantic_hash=None, derived=None, model=None, fail_fast=False):
    """Returns (ok, report). root: the project directory (for the B1 certificate)."""
    ctx.prec = CHECK_PREC
    fails, rep = [], {}
    try:
        _check(cert, root, stored_semantic_hash, derived, model, fail_fast, fails, rep)
    except Exception as exc:                                   # a malformed certificate is rejected, not crashed on
        fails.append(f"malformed certificate: {type(exc).__name__}: {exc}")
    rep["failures"] = fails
    return not fails, rep


class _Stop(Exception):
    pass


def _check(cert, root, stored_semantic_hash, derived, model, fail_fast, fails, rep):
    def fail(msg):
        fails.append(msg)
        if fail_fast:
            raise _Stop()

    try:
        _body(cert, root, stored_semantic_hash, derived, model, fail, rep)
    except _Stop:
        pass


def _endpoint(model, rec, G, label, fail, rep):
    c = carrier_v(G)
    rep["endpoints"][label] = {"c4_hat": c.str(20), "hE_hat": G["hE"].str(12), "Mh22": G["M22"].str(12),
                               "v_norm2": (G["M22"] ** 2 + G["M12"] ** 2).str(12)}
    lb = _q(rec.get("c4_hat_lower_bound", "0"))
    if not (lb > 0 and c > arb(lb) and G["hE"] > 0 and G["M22"] > 0):
        fail(f"{label}: carrier bound not confirmed")
    lo, hi = rec.get("c4_hat_enclosure", ["0", "0"])
    if not c.overlaps(_ball(_q(lo), _q(hi))):
        fail(f"{label}: stored enclosure does not overlap the independent value")
    if rec.get("certified") is not True:
        fail(f"{label}: not recorded as certified")


def _body(cert, root, stored_semantic_hash, derived, model, fail, rep):
    sh = semantic_hash(cert)
    rep["semantic_sha256"] = sh
    if cert.get("provenance", {}).get("semantic_sha256") != sh:
        fail("semantic hash in provenance does not match")
    if stored_semantic_hash is not None and stored_semantic_hash != sh:
        fail("semantic hash file does not match")
    if cert.get("claim") != EXPECTED_CLAIM:
        fail("claim differs from the expected claim")
    if cert.get("formulas") != EXPECTED_FORMULAS:
        fail("stored formulas differ from the expected formulas")
    if cert.get("corollary") != EXPECTED_COROLLARY:
        fail("corollary differs from the expected statement")
    ex = cert.get("expressions", {})
    h = hashlib.sha256(_canon({"expressions": ex, "formulas": cert.get("formulas")}).encode()).hexdigest()
    if h != cert.get("expression_sha256"):
        fail("expression hash mismatch")
    if (ex.get("X"), ex.get("Y"), ex.get("W")) != ("2**(-r/2)", "3**(-r/2)", "1 + X + Y/3"):
        fail("stored definitions of X, Y, W altered")
    funcs = derive_functions() if derived is None else derived
    for k in ORDER:
        if k not in ex or sp.simplify(sp.radsimp(stored_expr(ex[k]) - funcs[k])) != 0:
            fail(f"stored expression {k} differs from the independent derivation")
    # ---- imported B1: pinned hash, unaltered metadata and boxes, gap-free coverage
    imp = cert.get("imported_B1", {})
    if imp.get("semantic_sha256") != B1_SEMANTIC_PINNED:
        fail("imported B1 semantic hash differs from the pin")
    b1 = json.loads((pathlib.Path(root) / "data" / "B1_kappa_certificate.json").read_text())
    if semantic_hash(b1) != B1_SEMANTIC_PINNED:
        fail("the B1 certificate file does not have the pinned hash")
    meta = {"corner_box": b1["method"]["corner_box"], "corner_identification": b1["corner_identification"],
            "P_T(0)_enclosure": b1["endpoints"]["q=0"]["P_T(0)_enclosure"],
            "q_c_enclosure": b1["endpoints"]["corner"]["q_c_enclosure_paper2_lemma_T2"],
            "frozen_inputs": b1["frozen_inputs"], "n_boxes": len(b1["boxes"])}
    for k, v in meta.items():
        if imp.get(k) != v:
            fail(f"imported B1 metadata altered: {k}")
    if cert.get("import_checks") != EXPECTED_IMPORT_CHECKS:
        fail("the recorded import checks are not all passed")
    boxes = cert.get("boxes", [])
    if cert.get("n_boxes") != len(boxes):
        fail("n_boxes does not match")
    if not boxes or _q(boxes[0]["q_lo"]) != 0:
        fail("coverage does not start at 0")
    if boxes and _q(boxes[-1]["q_hi"]) != _q(EXPECTED_CLAIM["q_interval"][1]):
        fail("coverage does not end at 101/50")
    for a, b in zip(boxes, boxes[1:]):
        if _q(a["q_hi"]) != _q(b["q_lo"]):
            fail(f"gap or overlap at q = {a['q_hi']} / {b['q_lo']}")
    for j, b in enumerate(boxes):
        if set(b) != BOX_KEYS:
            fail(f"box {j}: unexpected fields")
        if b.get("index") != j:
            fail(f"box {j}: index out of order")
        if not _q(b["q_lo"]) < _q(b["q_hi"]):
            fail(f"box {j}: empty or reversed q-range")
        i = b.get("b1_index")
        if not isinstance(i, int) or not 0 <= i < len(b1["boxes"]):
            fail(f"box {j}: no valid B1 index")
            continue
        src = b1["boxes"][i]
        same = (b["delta_lo"] == src["delta_lo"] and b["delta_hi"] == src["delta_hi"]
                and b["corner"] == src["corner"] and _q(src["q_lo"]) <= _q(b["q_lo"]) < _q(b["q_hi"]) <= _q(src["q_hi"])
                and b.get("b1_box_sha256") == hashlib.sha256(_canon(src).encode()).hexdigest())
        if not same:
            fail(f"box {j}: imported B1 curve box modified")
        if b["regime"] != ("quotient" if _q(b["delta_lo"]) > 1 else "symmetric Taylor"):
            fail(f"box {j}: regime label inconsistent")
        if b["one_plus_rho2_lower_bound"] != "1":
            fail(f"box {j}: chart normalisation bound altered")
        if not b["corner"] and not _q(b["delta_lo"]) > 0:
            fail(f"box {j}: delta ball of a non-corner box not positive")
    used = sorted({b["b1_index"] for b in boxes if isinstance(b.get("b1_index"), int)})
    if used != list(range(len(b1["boxes"]))):
        fail("not every B1 box is covered")
    lbs = [_q(b["c4_hat_lower_bound"]) for b in boxes]
    if lbs:
        mn = min(lbs)
        if str(mn) != cert.get("min_lower_bound") \
                or cert.get("min_lower_bound_box", {}).get("index") != lbs.index(mn):
            fail("min_lower_bound or its box is not the minimum of the recorded bounds")
        dec = sp.Rational(str(cert.get("min_lower_bound_decimal", "0")))
        if abs(dec - sp.Rational(int(mn.p), int(mn.q))) > sp.Rational(1, 10 ** 10):
            fail("min_lower_bound_decimal does not match min_lower_bound")
        den = cert.get("denominator_bounds", {})
        if den.get("hE_hat_min_lower_bound") != str(min(_q(b["hE_hat_lower_bound"]) for b in boxes)) \
                or den.get("Mh22_min_lower_bound") != str(min(_q(b["Mh22_lower_bound"]) for b in boxes)) \
                or den.get("one_plus_rho2_min_lower_bound") != "1":
            fail("denominator bounds are not the minima of the recorded bounds")
    # ---- endpoints, certified directly (not inferred from q > 0)
    model = Model(funcs) if model is None else model
    rep["endpoints"] = {}
    e0 = cert.get("endpoints", {}).get("q=0", {})
    if e0.get("P_T(0)_ball_from_B1") != b1["endpoints"]["q=0"]["P_T(0)_enclosure"]:
        fail("q = 0: P_T(0) ball altered")
    P0 = _ball(*[_q(s) for s in b1["endpoints"]["q=0"]["P_T(0)_enclosure"]])
    D0 = _ball(_q(b1["boxes"][0]["delta_lo"]), _q(b1["boxes"][0]["delta_hi"]))
    if not (_q(b1["boxes"][0]["q_lo"]) == 0 and P0.lower() > D0.lower() and P0.upper() < D0.upper()):
        fail("q = 0: P_T(0) ball not inside the first curve box")
    _endpoint(model, e0, dd_point(model, arb(0), P0, 1024), "q=0", fail, rep)
    ec = cert.get("endpoints", {}).get("corner", {})
    if ec.get("q_c_enclosure_from_B1") != b1["endpoints"]["corner"]["q_c_enclosure_paper2_lemma_T2"]:
        fail("corner: q_c enclosure altered")
    Qc = _decimal_ball(*b1["endpoints"]["corner"]["q_c_enclosure_paper2_lemma_T2"])
    cb = [b for b in b1["boxes"] if b["corner"]]
    if len(cb) != 1 or not (Qc.lower() > arb(_q(cb[0]["q_lo"])) and Qc.upper() < arb(_q(cb[0]["q_hi"]))
                            and _q(cb[0]["delta_lo"]) < 0 < _q(cb[0]["delta_hi"])):
        fail("corner: (q_c, 0) not inside the corner box")
    _endpoint(model, ec, dd_point(model, Qc, arb(0), 1), "corner", fail, rep)   # delta = 0: exactly f'(q)
    for label, rec, qv, dv in (("q=0", e0, arb(0), P0), ("corner", ec, Qc, arb(0))):
        raw = qv * (1 + (-(arb(2).log() / 2) * qv).exp() + (-(arb(3).log() / 2) * qv).exp() / 3) * dv
        if not (raw == 0) or not str(rec.get("raw_c4", "")).startswith("0 ("):
            fail(f"{label}: raw c4 is not recorded as exactly zero")
    # ---- corner identification (B1): the unique zero in the corner ball at q = 2019/1000 is positive
    ci = b1["corner_identification"]
    Nci = newton_curve(model, arb(_q(ci["q"])), _ball(_q(cb[0]["delta_lo"]), _q(cb[0]["delta_hi"])), 32)
    if Nci is None or not Nci.lower() > 0:
        fail("corner identification not re-verified")
    # ---- boxes: curve re-verification (once per B1 box) and the recorded bounds
    stats = {"curve_reverified_b1_boxes": 0, "curve_max_q_split": 0, "curve_max_n": 0, "carrier_confirmed": 0,
             "carrier_max_split": 0, "carrier_max_n": 0, "centre_values_inside_stored_enclosures": 0}
    done_b1 = set()
    for j, b in enumerate(boxes):
        i = b["b1_index"]
        Q = _ball(_q(b["q_lo"]), _q(b["q_hi"]))
        D = _ball(_q(b["delta_lo"]), _q(b["delta_hi"]))
        if i not in done_b1:
            src = b1["boxes"][i]
            Nw, d, n = curve_confirmed(model, _ball(_q(src["q_lo"]), _q(src["q_hi"])), D)
            if Nw is None:
                fail(f"box {j}: curve re-verification failed (B1 box {i})")
            else:
                done_b1.add(i)
                stats["curve_reverified_b1_boxes"] += 1
                stats["curve_max_q_split"] = max(stats["curve_max_q_split"], d)
                stats["curve_max_n"] = max(stats["curve_max_n"], n)
        lb = _q(b["c4_hat_lower_bound"])
        if not (lb > 0 and _q(b["hE_hat_lower_bound"]) > 0 and _q(b["Mh22_lower_bound"]) > 0):
            fail(f"box {j}: a recorded lower bound is not strictly positive")
        ok, d, n = confirm_box(model, Q, D, lb, _q(b["hE_hat_lower_bound"]), _q(b["Mh22_lower_bound"]))
        if not ok:
            fail(f"box {j}: recorded bounds not confirmed (q in [{b['q_lo']}, {b['q_hi']}])")
        else:
            stats["carrier_confirmed"] += 1
            stats["carrier_max_split"] = max(stats["carrier_max_split"], d)
            stats["carrier_max_n"] = max(stats["carrier_max_n"], n)
        centre = carrier_v(dd_point(model, _mid(Q), _mid(D), 64))
        lo, hi = b["c4_hat_enclosure"]
        if not centre.overlaps(_ball(_q(lo), _q(hi))) or not _q(lo) >= lb:
            fail(f"box {j}: stored enclosure does not contain the independent centre value")
        else:
            stats["centre_values_inside_stored_enclosures"] += 1
    rep.update({"boxes_checked": len(boxes), "precision_bits": CHECK_PREC, **stats})
