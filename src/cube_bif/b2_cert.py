"""Phase B2.3: Arb certificate that the normalised D2h quartic carrier c4_hat is positive on the whole closed physical
T2g curve (Lemma Q). Generator (128 bits).

Carrier (B2.1, exact; chart n ~ (1, rho), rho = -Mh12/Mh22, hA_hat = 2 exactly):

    c4_hat = [Qh(1, rho) - (3/2) bAh(1, rho)^2 - 3 bEh(1, rho)^2 / hEh] / (1 + rho^2)^2,

with f_hat the divided differences of the 16 functions M11, M12, M22 (Paper 2's M) and the 13 B2.1 closed forms.

Curve (imported, not re-proved). The independently audited B1 certificate (data/B1_kappa_certificate.json, Lemma K)
is loaded only if its semantic SHA-256 equals the pinned value. Its 222 rational q-boxes and their delta-balls are
used unchanged: for every q in a box, the unique zero of D~(q, .) in the box's ball is the physical curve
delta = P_T(q) - q (q < q_c), the corner (q_c, 0), or the short mirror arc beyond q_c (corner box only). So
c4_hat > 0 on every box Q x Delta implies c4_hat > 0 on the closed physical curve.

Divided differences on a box (no division by delta near the diagonal):
- far (inf Delta > 1): the quotient (f(Q + Delta) - f(Q))/Delta of balls;
- near: m = q + delta/2, h = delta/2 and the symmetric form
      f_hat = sum_{k<K} c_{2k+1}(m) h^(2k) + h^(2K) c_{2K+1}(xi),   xi in hull(q, q + delta),   c_j = f^(j)/j!,
  from arb_series; the remainder is the weighted mean of f^(2K+1)/(2K+1)! over the hull (exact Lagrange form).

Endpoints, each certified directly:
- q = 0: f_hat = (f(p0) - f(0))/p0 with the exact values f(0) (B2.2) and p0 in B1's certified P_T(0) ball;
- corner: f_hat = f'(q) for q in Paper 2's certified q_c enclosure (as recorded by B1); no division by p - q.
"""
import hashlib
import json
import pathlib
import platform
import sys
import time

import flint
import mpmath as mp
import sympy as sp
from flint import arb, arb_series, ctx, fmpq, fmpz

from . import __version__
from . import b2_carrier as bc
from . import b2_quartic as b2
from . import pairsum as ps

PREC = 128
K_SYM = 10
LB_BITS = 20
ENCL_BITS = 40
MAX_SPLIT = 4
B1_FILE = "data/B1_kappa_certificate.json"
B1_HASH_FILE = "data/B1_CERTIFICATE_SEMANTIC.sha256"
B1_SEMANTIC_PINNED = "616817fcc70e0fab7f106404e5e5332b17b9c4480bd440355f1ac5257a8518c6"

r, Xr, Yr = ps.r_, ps.X["r"], ps.Y["r"]
_W = 1 + Xr + Yr / 3
M_EXPR = {"M11": (r * Xr + 2 * (2 * r + 1) * Yr / 9 - 2) / _W,
          "M12": 2 * sp.sqrt(2) * (r + 2) * Yr / (9 * _W),
          "M22": (2 * r + 2 * (r - 1) * Yr / 9 - 2) / _W}
EXPR = {**M_EXPR, **b2.G4_CLOSED}
NAMES = tuple(EXPR)

FORMULAS = {
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
CLAIM = {"quantity": "c4_hat", "relation": ">", "value": "0",
         "curve": "closed physical T2g curve: p = P_T(q) for 0 <= q < q_c, and the corner p = q = q_c",
         "q_interval": ["0", "101/50"]}


# ---- exact bookkeeping (same canonical rules as B1) --------------------------------------------------------------------
def parse_q(s):
    if "/" in s:
        a, b = s.split("/")
        return fmpq(int(a), int(b))
    return fmpq(int(s))


def ball(lo, hi):
    return arb(lo).union(arb(hi)) if lo != hi else arb(lo)


def arb_to_fmpq(x):
    m, e = x.man_exp()
    e = int(e)
    return fmpq(m) * fmpq(2) ** e if e >= 0 else fmpq(m, fmpz(2) ** (-e))


def outward(E, bits=ENCL_BITS):
    s = fmpz(2) ** bits
    lo, hi = arb_to_fmpq(E.lower()), arb_to_fmpq(E.upper())
    return fmpq((lo * s).floor(), s), fmpq((hi * s).ceil(), s)


def dyadic_lower_bound(E, bits=LB_BITS, margin=fmpq(1, 8), gap=fmpq(1, 1024)):
    """A dyadic number strictly below the ball E, lowered by max(margin * width, gap): robust, so that an
    independent evaluation with wider balls can confirm it."""
    s = fmpz(2) ** bits
    lo, hi = arb_to_fmpq(E.lower()), arb_to_fmpq(E.upper())
    k = ((lo - max(margin * (hi - lo), gap)) * s).floor() - 1
    while not (E > arb(fmpq(k, s))):
        k -= 1
    return fmpq(k, s)


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def semantic_hash(cert):
    return hashlib.sha256(canonical({k: v for k, v in cert.items() if k != "provenance"}).encode()).hexdigest()


def expression_strings():
    out = {"X": "2**(-r/2)", "Y": "3**(-r/2)", "W": "1 + X + Y/3"}
    for k in NAMES:
        out[k] = str(EXPR[k]).replace("Xr", "X").replace("Yr", "Y")
    return out


# ---- compiled Arb evaluation of the 16 closed forms (arb balls or arb_series) -------------------------------------------
def _compile(exprs):
    names = list(exprs)
    repl, red = sp.cse([exprs[k] for k in names])
    consts, index = [], {}

    def const(key):
        if key not in index:
            index[key] = len(consts)
            consts.append(key)
        return f"C[{index[key]}]"

    def em(e):
        if e.is_Symbol:
            return {r: "x", Xr: "X", Yr: "Y"}.get(e, str(e))
        if e.is_Rational:
            return const(("q", int(e.p), int(e.q)))
        if e.is_Pow and e.exp == sp.Rational(1, 2) and e.base.is_Integer:
            return const(("sqrt", int(e.base)))
        if e.is_Add:
            return "(" + " + ".join(em(a) for a in e.args) + ")"
        if e.is_Mul:
            num, den = [], []
            for a in e.args:
                if a.is_Pow and a.exp.is_Integer and a.exp < 0:
                    den.append(em(sp.Pow(a.base, -a.exp, evaluate=False)) if a.exp != -1 else em(a.base))
                else:
                    num.append(em(a))
            s = "*".join(num) if num else const(("q", 1, 1))
            return f"({s})" if not den else f"(({s})/({'*'.join(den)}))"
        if e.is_Pow and e.exp.is_Integer:
            k, b = int(e.exp), em(e.base)
            prod = "*".join([b] * abs(k))
            return f"({prod})" if k > 0 else f"({const(('q', 1, 1))}/({prod}))"
        raise ValueError(f"unsupported node: {e}")

    lines = ["def _f(x, C):", f"    X = (x * {const(('mlog', 2))}).exp()", f"    Y = (x * {const(('mlog', 3))}).exp()"]
    for sym, e in repl:
        lines.append(f"    {sym} = {em(e)}")
    lines.append("    return [" + ", ".join(em(e) for e in red) + "]")
    ns = {}
    exec("\n".join(lines), ns)
    return ns["_f"], consts


_BLOCK = {}


def _constants(keys):
    out = []
    for key in keys:
        if key[0] == "q":
            out.append(arb(fmpq(key[1], key[2])))
        elif key[0] == "sqrt":
            out.append(arb(key[1]).sqrt())
        else:
            out.append(-arb(key[1]).log() / 2)
    return out


def funcs(x):
    """The 16 functions at x (an arb ball or an arb_series)."""
    if "f" not in _BLOCK:
        _BLOCK["f"], _BLOCK["c"] = _compile(EXPR)
    vals = _BLOCK["f"](x, _constants(_BLOCK["c"]))
    return dict(zip(NAMES, vals))


def taylor(x, n):
    """Taylor coefficients c_0..c_{n-1} of each function, valid for every point of the ball x.

    python-flint truncates every arb_series at the context length ctx.cap (default 10), whatever is passed to the
    constructor. The length is therefore set to n explicitly while the series are computed; afterwards a result can
    only be shorter than n by trailing coefficients that are exactly zero (python-flint trims those), which are then
    restored as exact zeros."""
    old = ctx.cap
    ctx.cap = n
    try:
        vals = funcs(arb_series([x, 1]))
        out = {}
        for k, v in vals.items():
            c = list(v.coeffs())
            if len(c) > n:
                raise ArithmeticError("series longer than requested")
            out[k] = c + [arb(0)] * (n - len(c))
    finally:
        ctx.cap = old
    return out


# ---- divided differences ---------------------------------------------------------------------------------------------------
def divided(Q, D, regime):
    if regime == "quotient":
        fP, fQ = funcs(Q + D), funcs(Q)
        return {k: (fP[k] - fQ[k]) / D for k in NAMES}
    M, H = Q + D / 2, abs(D / 2)
    hull = Q.union(Q + D)
    cM, cH = taylor(M, 2 * K_SYM), taylor(hull, 2 * K_SYM + 2)
    H2 = H * H
    out = {}
    for k in NAMES:
        v = cH[k][2 * K_SYM + 1]
        for j in range(K_SYM - 1, -1, -1):
            v = v * H2 + cM[k][2 * j + 1]
        out[k] = v
    return out


def derivatives(Q):
    """f'(q) for q in Q (the corner rule)."""
    T = taylor(Q, 2)
    return {k: T[k][1] for k in NAMES}


def divided_with_slopes(Q, D, regime):
    """Enclosures over Q x D of f_hat, d f_hat/dq and d f_hat/d delta (for the curve re-verification).
    quotient: d_delta f_hat = (f'(p) - f_hat)/delta, d_q f_hat = (f'(p) - f'(q))/delta, p = q + delta.
    symmetric (m = q + delta/2, h = delta/2; d_q = d_m, d_delta = (d_m + d_h)/2), from the integral form
    f_hat = (1/2) int_{-1}^{1} f'(m + s h) ds with Lagrange remainders over hull(q, q + delta):
        d_m f_hat = sum_{k<K} (2k+2) c_{2k+2}(m) h^(2k) + h^(2K) (2K+2) c_{2K+2}(hull),
        d_h f_hat = sum_{k<K-1} (2k+2) c_{2k+3}(m) h^(2k+1) + h^(2K-1) (2K) c_{2K+1}(hull)."""
    if regime == "quotient":
        P = Q + D
        tP, tQ = taylor(P, 2), taylor(Q, 2)
        val = {k: (tP[k][0] - tQ[k][0]) / D for k in NAMES}
        return val, {k: (tP[k][1] - tQ[k][1]) / D for k in NAMES}, {k: (tP[k][1] - val[k]) / D for k in NAMES}
    M, H = Q + D / 2, D / 2
    hull = Q.union(Q + D)
    cM, cH = taylor(M, 2 * K_SYM + 1), taylor(hull, 2 * K_SYM + 3)
    val, dq, dd = {}, {}, {}
    for k in NAMES:
        c, h = cM[k], cH[k]
        v = h[2 * K_SYM + 1]
        for j in range(K_SYM - 1, -1, -1):
            v = v * (H * H) + c[2 * j + 1]
        val[k] = v
        dm = sum(((2 * j + 2) * c[2 * j + 2] * H ** (2 * j) for j in range(K_SYM)), arb(0)) \
            + H ** (2 * K_SYM) * (2 * K_SYM + 2) * h[2 * K_SYM + 2]
        dh = sum(((2 * j + 2) * c[2 * j + 3] * H ** (2 * j + 1) for j in range(K_SYM - 1)), arb(0)) \
            + H ** (2 * K_SYM - 1) * (2 * K_SYM) * h[2 * K_SYM + 1]
        dq[k], dd[k] = dm, (dm + dh) / 2
    return val, dq, dd


def _dtilde(v):
    return v["M11"] * v["M22"] - v["M12"] * v["M12"]


def _dtilde_slope(v, d):
    return d["M11"] * v["M22"] + v["M11"] * d["M22"] - 2 * v["M12"] * d["M12"]


def newton_inclusion(Q, D, regime):
    """Strict parametric interval Newton inclusion for D~(q, .) on the imported ball D, for all q in Q:
    N = m - D~(Q, m)/d_delta D~(Q, D) inside int D, with D~(Q, m) by the mean-value form in q. Returns N or None."""
    q0, m = arb(Q.mid()), arb(D.mid())
    v0 = divided_with_slopes(q0, m, regime)[0]
    vQ, qQ, _ = divided_with_slopes(Q, m, regime)
    F = _dtilde(v0) + _dtilde_slope(vQ, qQ) * (Q - q0)
    v, _, dD = divided_with_slopes(Q, D, regime)
    Fd = _dtilde_slope(v, dD)
    if not (Fd < 0 or Fd > 0):
        return None
    Nw = m - F / Fd
    return Nw if (Nw.lower() > D.lower() and Nw.upper() < D.upper()) else None


def carrier(F):
    """c4_hat and its denominators from the 16 divided differences (chart form, hA_hat = 2 exactly)."""
    rho = -F["M12"] / F["M22"]
    Qh = sum((b2.Q_BINOM[c] * rho ** c.count("v") * F["Q_" + c] for c in b2.Q_CHANNELS), arb(0))
    bA = sum((b2.B_WEIGHT[c] * rho ** c.count("v") * F["bA_" + c] for c in b2.B_CHANNELS), arb(0))
    bE = sum((b2.B_WEIGHT[c] * rho ** c.count("v") * F["bE_" + c] for c in b2.B_CHANNELS), arb(0))
    n2 = 1 + rho * rho
    c = (Qh - fmpq(3, 2) * bA * bA - 3 * bE * bE / F["hE"]) / (n2 * n2)
    return {"c4_hat": c, "rho": rho, "one_plus_rho2": n2, "hE": F["hE"], "Mh22": F["M22"]}


# ---- B1 import ---------------------------------------------------------------------------------------------------------------
def load_b1(root):
    root = pathlib.Path(root)
    cert = json.loads((root / B1_FILE).read_text())
    h = semantic_hash(cert)
    if h != B1_SEMANTIC_PINNED:
        raise RuntimeError(f"B1 certificate semantic hash {h} differs from the pinned value")
    if cert.get("provenance", {}).get("semantic_sha256") != h:
        raise RuntimeError("B1 certificate: recorded semantic hash differs from its content")
    if (root / B1_HASH_FILE).read_text().split()[0] != h:
        raise RuntimeError("B1 semantic hash file differs")
    return cert


def box_hash(b1box):
    return hashlib.sha256(canonical(b1box).encode()).hexdigest()


# ---- boxes -------------------------------------------------------------------------------------------------------------------
def certify_piece(qlo, qhi, D, regime, claim_bound=fmpq(0), carrier_fn=None):
    Q = ball(qlo, qhi)
    F = divided(Q, D, regime)
    res = (carrier_fn or carrier)(F)
    if not (res["hE"] > 0 and res["Mh22"] > 0):
        return None, "denominator not certified positive"
    if not res["c4_hat"] > arb(claim_bound):
        return None, "carrier not certified above the claimed bound"
    lb = dyadic_lower_bound(res["c4_hat"])
    if not lb > claim_bound:
        return None, "lower bound not above the claimed bound"
    elo, ehi = outward(res["c4_hat"])
    return {"q_lo": str(qlo), "q_hi": str(qhi), "c4_hat_enclosure": [str(elo), str(ehi)],
            "c4_hat_lower_bound": str(lb),
            "hE_hat_lower_bound": str(dyadic_lower_bound(res["hE"], margin=fmpq(0), gap=fmpq(0))),
            "Mh22_lower_bound": str(dyadic_lower_bound(res["Mh22"], margin=fmpq(0), gap=fmpq(0))),
            "one_plus_rho2_lower_bound": "1"}, None


def certify_b1_box(i, b1box, claim_bound=fmpq(0), carrier_fn=None, max_split=MAX_SPLIT):
    """One B1 box: the whole q-range with its delta-ball, bisected in q (same ball) if necessary."""
    ctx.prec = PREC
    D = ball(parse_q(b1box["delta_lo"]), parse_q(b1box["delta_hi"]))
    regime = "quotient" if parse_q(b1box["delta_lo"]) > 1 else "symmetric Taylor"
    if newton_inclusion(ball(parse_q(b1box["q_lo"]), parse_q(b1box["q_hi"])), D, regime) is None:
        return None, {"b1_index": i, "reason": "curve re-verification: no strict Newton inclusion in the imported ball"}
    todo = [(parse_q(b1box["q_lo"]), parse_q(b1box["q_hi"]), 0)]
    pieces = []
    while todo:
        lo, hi, depth = todo.pop()
        rec, why = certify_piece(lo, hi, D, regime, claim_bound, carrier_fn)
        if rec is not None:
            rec.update({"b1_index": i, "b1_box_sha256": box_hash(b1box), "delta_lo": b1box["delta_lo"],
                        "delta_hi": b1box["delta_hi"], "corner": b1box["corner"], "regime": regime,
                        "split_depth": depth, "curve_reverified": True})
            pieces.append(rec)
            continue
        if depth >= max_split:
            return None, {"b1_index": i, "q_lo": str(lo), "q_hi": str(hi), "reason": why}
        mid = (lo + hi) / 2
        todo.append((mid, hi, depth + 1))
        todo.append((lo, mid, depth + 1))
    pieces.sort(key=lambda p: parse_q(p["q_lo"]))
    return pieces, None


def import_checks(b1, boxes):
    """Checks of the imported curve boxes, recorded in the certificate (the checker repeats them independently)."""
    qs = [(parse_q(b["q_lo"]), parse_q(b["q_hi"])) for b in boxes]
    src = [b1["boxes"][b["b1_index"]] for b in boxes]
    return {
        "B1_semantic_sha256_equals_the_pin": semantic_hash(b1) == B1_SEMANTIC_PINNED,
        "q_coverage_gap_free_from_0_to_101/50": bool(qs and qs[0][0] == 0 and qs[-1][1] == fmpq(101, 50)
                                                     and all(a[1] == b[0] for a, b in zip(qs, qs[1:]))),
        "boxes_ordered_and_nonempty": all(a < b for a, b in qs),
        "every_B1_box_used": sorted({b["b1_index"] for b in boxes}) == list(range(len(b1["boxes"]))),
        "boxes_inside_their_B1_q_range": all(parse_q(s_["q_lo"]) <= a and b <= parse_q(s_["q_hi"])
                                             for (a, b), s_ in zip(qs, src)),
        "delta_balls_and_corner_flags_equal_to_B1": all(
            b["delta_lo"] == s_["delta_lo"] and b["delta_hi"] == s_["delta_hi"] and b["corner"] == s_["corner"]
            for b, s_ in zip(boxes, src)),
        "B1_box_hashes_recorded": all(b["b1_box_sha256"] == box_hash(s_) for b, s_ in zip(boxes, src)),
        "exactly_one_corner_box_and_it_is_the_last": [b["corner"] for b in b1["boxes"]].count(True) == 1
                                                      and b1["boxes"][-1]["corner"],
    }


# ---- endpoints ---------------------------------------------------------------------------------------------------------------
def exact_zero_values():
    """f(0) for the 16 functions as balls, from the exact values (B2.2: bc.g_at_zero, bc.M_at_zero)."""
    def to_arb(e):
        e = sp.nsimplify(e)
        coeff, rest = e.as_coeff_Mul()
        out = arb(fmpq(int(sp.Rational(coeff).p), int(sp.Rational(coeff).q)))
        if rest != 1:
            if not (rest.is_Pow and rest.exp == sp.Rational(1, 2) and rest.base.is_Integer):
                raise ValueError(f"unexpected exact value {e}")
            out = out * arb(int(rest.base)).sqrt()
        return out
    vals = {k: to_arb(v) for k, v in bc.g_at_zero().items()}
    M0 = bc.M_at_zero()
    vals.update({"M11": to_arb(M0[0, 0]), "M12": to_arb(M0[0, 1]), "M22": to_arb(M0[1, 1])})
    return vals


def endpoint_q0(b1, carrier_fn=None):
    ctx.prec = PREC
    lo, hi = (parse_q(s) for s in b1["endpoints"]["q=0"]["P_T(0)_enclosure"])
    P = ball(lo, hi)
    f0, fP = exact_zero_values(), funcs(P)
    res = (carrier_fn or carrier)({k: (fP[k] - f0[k]) / P for k in NAMES})
    elo, ehi = outward(res["c4_hat"], 100)
    return {"P_T(0)_ball_from_B1": [str(lo), str(hi)], "rule": FORMULAS["q0_rule"],
            "c4_hat": res["c4_hat"].str(30), "c4_hat_enclosure": [str(elo), str(ehi)],
            "c4_hat_lower_bound": str(dyadic_lower_bound(res["c4_hat"])),
            "rho": res["rho"].str(25), "hE_hat": res["hE"].str(25), "Mh22": res["Mh22"].str(25),
            "raw_c4": "0 (exact: the factor q vanishes)",
            "exact_f0_matches_closed_forms_at_0": all(abs(funcs(arb(0))[k] - f0[k]) < arb(fmpq(1, 10 ** 30))
                                                      for k in NAMES),
            "certified": bool(res["c4_hat"] > 0 and res["hE"] > 0 and res["Mh22"] > 0)}


def endpoint_corner(b1, carrier_fn=None):
    ctx.prec = PREC
    lo, hi = (sp.Rational(s) for s in b1["endpoints"]["corner"]["q_c_enclosure_paper2_lemma_T2"])
    Qc = ball(fmpq(int(lo.p), int(lo.q)), fmpq(int(hi.p), int(hi.q)))
    res = (carrier_fn or carrier)(derivatives(Qc))
    elo, ehi = outward(res["c4_hat"], 100)
    return {"q_c_enclosure_from_B1": b1["endpoints"]["corner"]["q_c_enclosure_paper2_lemma_T2"],
            "rule": FORMULAS["corner_rule"], "c4_hat": res["c4_hat"].str(30), "c4_hat_enclosure": [str(elo), str(ehi)],
            "c4_hat_lower_bound": str(dyadic_lower_bound(res["c4_hat"])),
            "rho": res["rho"].str(25), "hE_hat": res["hE"].str(25), "Mh22": res["Mh22"].str(25),
            "raw_c4": "0 (exact: the factor p - q vanishes)",
            "certified": bool(res["c4_hat"] > 0 and res["hE"] > 0 and res["Mh22"] > 0)}


# ---- the certificate ---------------------------------------------------------------------------------------------------------
def build_certificate(root, claim_bound=fmpq(0), carrier_fn=None):
    t0 = time.time()
    root = pathlib.Path(root)
    b1 = load_b1(root)
    boxes = []
    for i, bx in enumerate(b1["boxes"]):
        pieces, fail = certify_b1_box(i, bx, claim_bound, carrier_fn)
        if fail is not None:
            raise RuntimeError(f"B2.3 certificate failed: {fail}")
        boxes.extend(pieces)
    for j, bx in enumerate(boxes):
        bx["index"] = j
    checks = import_checks(b1, boxes)
    if not all(checks.values()):
        raise RuntimeError(f"B2.3 certificate: import check failed: {checks}")
    lbs = [parse_q(b["c4_hat_lower_bound"]) for b in boxes]
    mn = min(lbs)
    kmin = lbs.index(mn)
    ex = expression_strings()
    cert = {
        "certificate": "EIT-LJ Cube Bifurcations (Paper 3), Phase B2.3: c4_hat > 0 on the closed T2g curve (Lemma Q)",
        "statement": ("For every q in [0, 101/50] and every delta in the B1 ball of its box (which contains the unique "
                      "zero of D~(q, .) there: the physical curve delta = P_T(q) - q for 0 <= q < q_c, the corner "
                      "(q_c, 0), and a short mirror arc beyond q_c): hE_hat > 0, Mh22 > 0 and c4_hat > recorded lower "
                      "bound > 0. Endpoints, certified directly: q = 0 with p = P_T(0), and the corner with diagonal "
                      "derivatives."),
        "claim": CLAIM,
        "expressions": ex,
        "formulas": FORMULAS,
        "expression_sha256": hashlib.sha256(canonical({"expressions": ex, "formulas": FORMULAS}).encode()).hexdigest(),
        "imported_B1": {"file": B1_FILE, "semantic_sha256": B1_SEMANTIC_PINNED, "n_boxes": len(b1["boxes"]),
                        "corner_box": b1["method"]["corner_box"], "corner_identification": b1["corner_identification"],
                        "P_T(0)_enclosure": b1["endpoints"]["q=0"]["P_T(0)_enclosure"],
                        "q_c_enclosure": b1["endpoints"]["corner"]["q_c_enclosure_paper2_lemma_T2"],
                        "frozen_inputs": b1["frozen_inputs"]},
        "import_checks": checks,
        "method": {"arb_precision_bits": PREC, "symmetric_taylor_terms_K": K_SYM,
                   "regimes": {"quotient": "inf delta > 1", "symmetric Taylor": "otherwise"},
                   "lower_bound": f"dyadic (2^-{LB_BITS}) below the enclosure by max(1/8 of its width, 2^-10)",
                   "series_length": "ctx.cap set to the number of Taylor coefficients requested (python-flint "
                                    "truncates arb_series at ctx.cap); results checked not to be truncated",
                   "enclosure_rounding": f"outward to 2^-{ENCL_BITS}", "max_q_split": MAX_SPLIT,
                   "curve": ("B1 delta-balls imported unchanged (hash-pinned) and re-verified here by a strict "
                             "parametric interval Newton inclusion on every box (quotient / symmetric Taylor with "
                             "complete tails)")},
        "boxes": boxes,
        "n_boxes": len(boxes),
        "min_lower_bound": str(mn),
        "min_lower_bound_decimal": mp.nstr(mp.mpf(int(mn.p)) / int(mn.q), 12),
        "min_lower_bound_box": {"index": kmin, "q_lo": boxes[kmin]["q_lo"], "q_hi": boxes[kmin]["q_hi"]},
        "denominator_bounds": {
            "hE_hat_min_lower_bound": str(min(parse_q(b["hE_hat_lower_bound"]) for b in boxes)),
            "Mh22_min_lower_bound": str(min(parse_q(b["Mh22_lower_bound"]) for b in boxes)),
            "one_plus_rho2_min_lower_bound": "1"},
        "endpoints": {"q=0": endpoint_q0(b1, carrier_fn), "corner": endpoint_corner(b1, carrier_fn)},
        "corollary": ("c4(q) = q W_q (P_T(q) - q) c4_hat(q) > 0 for 0 < q < q_c: q > 0, W_q > 1, and P_T(q) - q > 0 "
                      "(Paper 2, Lemma T3)."),
    }
    code = {}
    for f in ("src/cube_bif/b2_cert.py", "src/cube_bif/b2_check.py", "src/cube_bif/b2_quartic.py",
              "src/cube_bif/b2_carrier.py", "scripts/run_B2_3.py"):
        p = root / f
        if p.exists():
            code[f] = hashlib.sha256(p.read_bytes()).hexdigest()
    cert["provenance"] = {
        "excluded_from_semantic_hash": True, "seconds": round(time.time() - t0, 1),
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "project_version": __version__,
        "python": sys.version.split()[0], "platform": platform.platform(), "python-flint": flint.__version__,
        "FLINT": flint.__FLINT_VERSION__, "sympy": sp.__version__, "mpmath": mp.__version__, "code_sha256": code}
    cert["provenance"]["semantic_sha256"] = semantic_hash(cert)
    return cert
