"""Independent checker for the Phase B1 certificate (data/B1_kappa_certificate.json).

It shares no code with b1_cubic.py or b1_cert.py:
- It derives the seven functions itself. The three Hessian-block entries M_ij(r) and the four cubic channels g_m(r)
  come from its own SymPy differentiation of the pair terms along the T2g directions, with psi = sigma^(-r/2). The
  result is compared with the expression strings stored in the certificate.
- It evaluates them with its own Arb expression walker, at 160 bits.
- It has its own divided differences: ball quotients far from the diagonal, a Taylor form with N = 20 near it.
- It re-checks one interval Newton inclusion on every stored delta-ball, the positivity of Mh22, the stored lower
  bound of kappa_hat, gap-free coverage, the corner box, the two endpoints and the semantic hash.
"""
import hashlib
import itertools
import json

import sympy as sp
from flint import arb, arb_series, ctx, fmpq

CHECK_PREC = 160
N_CHECK = 20
EXPECTED_CLAIM = {"quantity": "kappa_hat", "relation": ">", "value": "0", "q_interval": ["0", "101/50"]}
QC_LO = fmpq(20199382317007999883028831854985758749007, 10 ** 40)
QC_HI = fmpq(20199382317007999883028831854985758749008, 10 ** 40)
ORDER = ("M11", "M12", "M22", "uuu", "uuv", "uvv", "vvv")
R_, X_, Y_, W_ = sp.symbols("r X Y W", positive=True)


# ---- independent derivation ------------------------------------------------------------------------------------------
def _labels():
    return list(itertools.product([-1, 1], repeat=3))


def _fields():
    """Unnormalised T2g fields: shear S_k s and opposite tetrahedron translation (s1 s2 s3) e_k."""
    S = {0: ((0, 0, 0), (0, 0, 1), (0, 1, 0)), 1: ((0, 0, 1), (0, 0, 0), (1, 0, 0)), 2: ((0, 1, 0), (1, 0, 0), (0, 0, 0))}
    shear = {k: [sum(S[k][a][b] * s[b] for b in range(3)) for s in _labels() for a in range(3)] for k in range(3)}
    trans = {k: [(s[0] * s[1] * s[2]) * (1 if a == k else 0) for s in _labels() for a in range(3)] for k in range(3)}
    return shear, trans


def _directional(dirs):
    """D^n of U_r = sum |x_i - x_j|^(-r) at the unit-edge cube along dirs, divided by r W_r, as an expression in
    r, X = 2^(-r/2), Y = 3^(-r/2). psi(sigma) = sigma^(-r/2) enters through its derivatives at sigma = 1, 2, 3."""
    n = len(dirs)
    t = sp.symbols(f"t0:{n}")
    L = _labels()
    tot = 0
    for i, j in itertools.combinations(range(8), 2):
        base = [sp.Rational(L[i][c] - L[j][c], 2) for c in range(3)]
        sv = int(sum(b * b for b in base))
        vec = [base[c] + sum(t[a] * (dirs[a][3 * i + c] - dirs[a][3 * j + c]) for a in range(n)) for c in range(3)]
        sig = sum(v * v for v in vec)
        powr = {1: sp.Integer(1), 2: X_, 3: Y_}[sv]
        poly = 0
        for k in range(1, n + 1):
            ff = sp.Integer(1)
            for m in range(k):
                ff *= (-R_ / 2 - m)
            poly += ff * powr * sp.Integer(sv) ** (-k) * (sig - sv) ** k / sp.factorial(k)
        d = poly
        for a in range(n):
            d = sp.diff(d, t[a])
        tot += d.subs({ta: 0 for ta in t})
    return sp.cancel(sp.together(sp.expand(tot) / (R_ * (1 + X_ + Y_ / 3))))


def derive_functions():
    shear, trans = _fields()
    uh = {k: [sp.Rational(-1, 4) * c for c in shear[k]] for k in range(3)}
    vh = {k: [-sp.sqrt(2) / 4 * c for c in trans[k]] for k in range(3)}
    b = {"u": uh, "v": vh}
    out = {"M11": _directional([uh[2], uh[2]]), "M12": _directional([uh[2], vh[2]]),
           "M22": _directional([vh[2], vh[2]])}
    for m in ("uuu", "uuv", "uvv", "vvv"):
        out[m] = _directional([b[m[0]][0], b[m[1]][1], b[m[2]][2]])
    return out


def _stored(expr_str):
    loc = {"r": R_, "X": X_, "Y": Y_, "W": 1 + X_ + Y_ / 3, "sqrt": sp.sqrt}
    return sp.sympify(expr_str, locals=loc)


# ---- series length (erratum E-B1, V0.4-dev.4) --------------------------------------------------------------------------
class TruncatedSeries(ArithmeticError):
    """A series came back shorter than requested and the gap is not made of exact zeros."""


class SeriesLength:
    """Context manager: ctx.cap >= length inside the block (python-flint truncates every arb_series at ctx.cap, default
    10, whatever prec= asks for); the saved value is put back on exit, whether or not an exception was raised."""

    def __init__(self, length):
        self.length = length
        self.saved = None

    def __enter__(self):
        self.saved = ctx.cap
        if self.saved < self.length:
            ctx.cap = self.length
        if ctx.cap < self.length:
            ctx.cap = self.saved
            raise TruncatedSeries(f"capacity {ctx.cap} below the requested length {self.length}")
        return ctx.cap

    def __exit__(self, exc_type, exc, tb):
        ctx.cap = self.saved
        return False


# ---- Arb walker (works on arb balls and on arb_series) ------------------------------------------------------------
def _walk(e, env):
    if e.is_Symbol:
        return env[e]
    if e.is_Integer:
        return arb(int(e))
    if e.is_Rational:
        return arb(fmpq(int(e.p), int(e.q)))
    if e == sp.sqrt(2):
        return arb(2).sqrt()
    if e.is_Add:
        acc = None
        for a in e.args:
            v = _walk(a, env)
            acc = v if acc is None else acc + v
        return acc
    if e.is_Mul:
        acc = None
        for a in e.args:
            v = _walk(a, env)
            acc = v if acc is None else acc * v
        return acc
    if e.is_Pow:
        base, ex = e.args
        if ex.is_Integer:
            v = _walk(base, env)
            k = int(ex)
            out = v
            for _ in range(abs(k) - 1):
                out = out * v
            return 1 / out if k < 0 else out
        if base == 2 and ex == sp.Rational(1, 2):
            return arb(2).sqrt()
    raise ValueError(f"unsupported node {e}")


class Model:
    def __init__(self, funcs):
        self.f = {k: sp.factor(v) for k, v in funcs.items()}          # factored forms: less interval dependency

    def values(self, x):
        L2, L3 = arb(2).log(), arb(3).log()
        env = {R_: x, X_: (-(L2 / 2) * x).exp(), Y_: (-(L3 / 2) * x).exp()}
        return {k: _walk(self.f[k], env) for k in ORDER}

    def taylor(self, x, n):
        """c_0..c_{n-1} of every function at the ball x.

        Erratum E-B1 (V0.4-dev.4; NOTES.md §10): up to V0.4-dev.3 the series were computed under python-flint's
        default ctx.cap = 10 and zero-padded, which replaced c_10, c_11, ... by 0. Now ctx.cap >= n during the
        evaluation; a result shorter than n is accepted only if a series of length n + 3 shows that every missing
        coefficient is exactly zero."""
        raw = self._raw_series(x, n)
        out = {}
        for k in ORDER:
            c = raw[k]
            if len(c) < n:
                ext = self._raw_series(x, n + 3)[k]
                for j in range(len(c), n):
                    if j < len(ext) and not (ext[j] == 0):
                        raise TruncatedSeries(f"{k}: coefficient {j} missing but not exactly zero")
                c = c + [arb(0)] * (n - len(c))
            if len(c) != n:
                raise TruncatedSeries(f"{k}: {len(c)} coefficients, {n} requested")
            out[k] = c
        return out

    def _raw_series(self, x, n):
        with SeriesLength(n) as cap:
            vals = self.values(arb_series([x, 1], prec=n))
            raw = {k: list(vals[k].coeffs()) for k in ORDER}
            if ctx.cap != cap or cap < n:
                raise TruncatedSeries("capacity changed during the evaluation")
        if any(len(c) > n for c in raw.values()):
            raise TruncatedSeries("series longer than requested")
        return raw

    def dd(self, Q, D, regime):
        """(value, d/d delta, d/dq) of every divided difference over Q x D."""
        if regime == "far":
            P = Q + D
            tQ, tP = self.taylor(Q, 2), self.taylor(P, 2)
            v = {k: (tP[k][0] - tQ[k][0]) / D for k in ORDER}
            return v, {k: (tP[k][1] - v[k]) / D for k in ORDER}, {k: (tP[k][1] - tQ[k][1]) / D for k in ORDER}
        N = N_CHECK
        H = Q.union(Q + D)
        cQ, cH = self.taylor(Q, N + 2), self.taylor(H, N + 3)
        v, dv, qv = {}, {}, {}
        for k in ORDER:
            c, h = cQ[k], cH[k]
            v[k] = sum((c[j] * D ** (j - 1) for j in range(2, N + 1)), c[1]) + D ** N * h[N + 1]
            dv[k] = (sum(((j - 1) * c[j] * D ** (j - 2) for j in range(3, N + 1)), c[2])
                     + N * D ** (N - 1) * h[N + 1] + D ** N * h[N + 2])
            qv[k] = sum(((j + 1) * c[j + 1] * D ** (j - 1) for j in range(2, N + 1)), 2 * c[2]) \
                + (N + 2) * D ** N * h[N + 2]
        return v, dv, qv


def _det(v):
    return v["M11"] * v["M22"] - v["M12"] ** 2


def _det_d(v, d):
    return d["M11"] * v["M22"] + v["M11"] * d["M22"] - 2 * v["M12"] * d["M12"]


def newton_inclusion(model, Q, D, regime):
    q0, m = arb(Q.mid()), arb(D.mid())
    v0 = model.dd(q0, m, regime)[0]
    vQ, _, qQ = model.dd(Q, m, regime)
    Fm = _det(v0) + _det_d(vQ, qQ) * (Q - q0)
    v, dv, _ = model.dd(Q, D, regime)
    Fd = _det_d(v, dv)
    if not (Fd > 0 or Fd < 0):
        return None
    Nw = m - Fm / Fd
    return Nw if (Nw.lower() > D.lower() and Nw.upper() < D.upper()) else None


def carrier(model, Q, D, regime):
    def parts(v):
        rho = -v["M12"] / v["M22"]
        return v["uuu"] + 3 * rho * v["uuv"] + 3 * rho ** 2 * v["uvv"] + rho ** 3 * v["vvv"], v["M22"], rho

    def slope(v, d):
        rho = -v["M12"] / v["M22"]
        rx = -(d["M12"] * v["M22"] - v["M12"] * d["M22"]) / v["M22"] ** 2
        g = [v[m] for m in ("uuu", "uuv", "uvv", "vvv")]
        gx = [d[m] for m in ("uuu", "uuv", "uvv", "vvv")]
        return (gx[0] + 3 * rx * g[1] + 3 * rho * gx[1] + 6 * rho * rx * g[2] + 3 * rho ** 2 * gx[2]
                + 3 * rho ** 2 * rx * g[3] + rho ** 3 * gx[3]), d["M22"]
    q0, d0 = arb(Q.mid()), arb(D.mid())
    k0, c0, _ = parts(model.dd(q0, d0, regime)[0])
    v, dv, qv = model.dd(Q, D, regime)
    kq, cq = slope(v, qv)
    kd, cd = slope(v, dv)
    return k0 + kq * (Q - q0) + kd * (D - d0), c0 + cq * (Q - q0) + cd * (D - d0)


def carrier_confirmed(model, Q, D, regime, lb, depth=0, max_depth=4):
    """kappa_hat > lb and Mh22 > 0 on Q x D; if not confirmed, split Q and shrink D by one Newton step on each half
    (the zero of each q in the half lies in N(Q_half, D))."""
    kh, m22 = carrier(model, Q, D, regime)
    if kh > arb(lb) and m22 > 0:
        return True, depth
    if depth >= max_depth:
        return False, depth
    lo, hi, mid = Q.lower(), Q.upper(), arb(Q.mid())
    worst = depth
    for half in (lo.union(mid), mid.union(hi)):
        q0, m = arb(half.mid()), arb(D.mid())
        v0 = model.dd(q0, m, regime)[0]
        vQ, _, qQ = model.dd(half, m, regime)
        Fm = _det(v0) + _det_d(vQ, qQ) * (half - q0)
        v, dv, _ = model.dd(half, D, regime)
        Fd = _det_d(v, dv)
        if not (Fd > 0 or Fd < 0):
            return False, depth
        Dh = D.intersection(m - Fm / Fd)
        ok, d = carrier_confirmed(model, half, Dh, regime, lb, depth + 1, max_depth)
        if not ok:
            return False, d
        worst = max(worst, d)
    return True, worst


def _q(s):
    if "/" in s:
        a, b = s.split("/")
        return fmpq(int(a), int(b))
    return fmpq(int(s))


def _ball(lo, hi):
    return arb(lo).union(arb(hi)) if lo != hi else arb(lo)


def semantic_hash(cert):
    body = {k: v for k, v in cert.items() if k != "provenance"}
    return hashlib.sha256(json.dumps(body, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def check(cert, stored_semantic_hash=None, derived=None):
    """Returns (ok, report). `derived` may pass precomputed derive_functions() (it takes about a minute)."""
    ctx.prec = CHECK_PREC
    fails, rep = [], {}
    if cert.get("claim") != EXPECTED_CLAIM:
        fails.append("claim differs from the expected claim")
    funcs = derive_functions() if derived is None else derived
    ex = cert.get("expressions", {})
    for k in ORDER:
        if k not in ex or sp.simplify(_stored(ex[k]) - funcs[k]) != 0:
            fails.append(f"stored expression {k} differs from the independent derivation")
    if hashlib.sha256(json.dumps(ex, sort_keys=True).encode()).hexdigest() != cert.get("expression_sha256"):
        fails.append("expression hash mismatch")
    model = Model(funcs)
    boxes = cert.get("boxes", [])
    if not boxes or _q(boxes[0]["q_lo"]) != 0:
        fails.append("coverage does not start at 0")
    if boxes and _q(boxes[-1]["q_hi"]) != _q(EXPECTED_CLAIM["q_interval"][1]):
        fails.append("coverage does not end at the claimed endpoint")
    for a, b in zip(boxes, boxes[1:]):
        if _q(a["q_hi"]) != _q(b["q_lo"]):
            fails.append(f"gap or overlap at {a['q_hi']}")
            break
    if cert.get("n_boxes") != len(boxes):
        fails.append("n_boxes does not match")
    corners = [b for b in boxes if b.get("corner")]
    if len(corners) != 1 or not (_q(corners[0]["q_lo"]) < QC_LO and QC_HI < _q(corners[0]["q_hi"])):
        fails.append("the corner box must be unique and contain Paper 2's q_c enclosure")
    lbs, newton_ok, carrier_ok, refined, deepest = [], 0, 0, 0, 0
    for b in boxes:
        Q = _ball(_q(b["q_lo"]), _q(b["q_hi"]))
        dlo, dhi = _q(b["delta_lo"]), _q(b["delta_hi"])
        if not dlo < dhi or _q(b["q_lo"]) >= _q(b["q_hi"]):
            fails.append(f"degenerate box at {b['q_lo']}")
            continue
        if not b.get("corner") and not dlo > 0:
            fails.append(f"delta ball not positive at {b['q_lo']}")
        if b["regime"] == "far" and not dlo > 1:
            fails.append(f"far regime with delta <= 1 at {b['q_lo']}")
        D = _ball(dlo, dhi)
        if newton_inclusion(model, Q, D, b["regime"]) is None:
            fails.append(f"Newton inclusion not confirmed at {b['q_lo']}")
            continue
        newton_ok += 1
        lb = _q(b["kappa_hat_lower_bound"])
        lbs.append(lb)
        if not lb > 0:
            fails.append(f"lower bound not strictly positive at {b['q_lo']}")
        ok, d = carrier_confirmed(model, Q, D, b["regime"], lb)
        if not ok:
            fails.append(f"lower bound not confirmed at {b['q_lo']}")
            continue
        carrier_ok += 1
        refined += 1 if d > 0 else 0
        deepest = max(deepest, d)
    if lbs and str(min(lbs)) != cert.get("min_lower_bound"):
        fails.append("min_lower_bound is not the minimum of the box bounds")
    # corner identification
    if len(corners) == 1:
        c = corners[0]
        Da = newton_inclusion(model, arb(_q(c["q_lo"])), _ball(_q(c["delta_lo"]), _q(c["delta_hi"])), c["regime"])
        if Da is None or not Da.lower() > 0:
            fails.append("corner identification: delta at the left end of the corner box not certified positive")
    # endpoints
    lo0, hi0 = fmpq(4796368189344416004181122459356, 10 ** 30), fmpq(4796368189344416004181122459357, 10 ** 30)
    D0 = _ball(lo0 - fmpq(1, 10 ** 20), hi0 + fmpq(1, 10 ** 20))
    N0 = newton_inclusion(model, arb(0), D0, "far")
    if N0 is None:
        fails.append("endpoint q = 0: Newton inclusion failed")
    else:
        ok0, _ = carrier_confirmed(model, arb(0), N0, "far", _q(cert["endpoints"]["q=0"]["kappa_hat_lower_bound"]),
                                   max_depth=0)
        if not ok0:
            fails.append("endpoint q = 0: carrier bound not confirmed")
    Qc = _ball(QC_LO, QC_HI)
    kc, cc = carrier(model, Qc, arb(0), "near")
    if not (kc > arb(_q(cert["endpoints"]["corner"]["kappa_hat_lower_bound"])) and cc > 0):
        fails.append("corner endpoint: carrier bound not confirmed")
    ctx.prec = 4 * CHECK_PREC
    s_lo = _det(model.dd(arb(QC_LO), arb(0), "near")[0])
    s_hi = _det(model.dd(arb(QC_HI), arb(0), "near")[0])
    ctx.prec = CHECK_PREC
    if not (s_lo > 0 and s_hi < 0):
        fails.append("det M' does not change sign across Paper 2's q_c enclosure")
    # hashes
    sh = semantic_hash(cert)
    if cert.get("provenance", {}).get("semantic_sha256") != sh:
        fails.append("semantic hash in provenance does not match the content")
    if stored_semantic_hash is not None and stored_semantic_hash != sh:
        fails.append("semantic hash file does not match the content")
    rep.update({"boxes_checked": len(boxes), "newton_confirmed": newton_ok, "carrier_confirmed": carrier_ok,
                "boxes_refined_by_checker": refined, "max_checker_refinement_depth": deepest,
                "failures": fails, "semantic_sha256": sh, "precision_bits": CHECK_PREC, "taylor_order": N_CHECK})
    return not fails, rep
