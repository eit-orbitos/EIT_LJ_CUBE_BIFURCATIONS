"""Phase A2 — Lemma M: m'(r) > 0 for 0 <= r <= 16/5, certified with Arb ball arithmetic (python-flint).

m is the V0.1-dev closed form (a2u.scale_free_coefficients()["m"]; identity tested), written as

    m = N / (16 S^2),   S = 3x + y + 3,   N = S (3r^3 x + 81 r + (3r+2) y + 126) - 3r (3r x - y - 9)^2,

with x = 2^(-r/2), y = 3^(-r/2). The total r-derivative acts by dx/dr = -(L2/2) x, dy/dr = -(L3/2) y, where
L2 = log 2 and L3 = log 3 are kept as symbols and enclosed by Arb. Then

    m'  = Psi / (16 S^3),   Psi = S N' - 2 N S',
    m'' = Phi / (16 S^4),   Phi = S Psi' - 3 Psi S',      with S' = -(3 L2/2) x - (L3/2) y.

No division by r occurs: the factor r of U''(0) and U''''(0) in the V0.1-dev definition
m = [U''''/U - 3 (U''/U)^2] / r cancels exactly in the closed form, so m is analytic at r = 0 and its Arb evaluation
near r = 0 involves no 0/0 cancellation.

Box test (mean-value form). For B = [lo, hi] with exact rational endpoints and c = (lo + hi)/2,

    { m'(r) : r in B }  is contained in  m'(c) + (B - c) * m''(B),

evaluated in Arb with outward rounding (B is the Arb ball containing [lo, hi]). A box is accepted when this enclosure
is certainly greater than a recorded dyadic lower bound that is itself > 0. Boxes are bisected until accepted and of
width <= W_MAX; the procedure fails (it never guesses) if a box cannot be accepted down to MAX_DEPTH bisections.
"""
import datetime
import hashlib
import json
import math
import pathlib
import platform
import sys
import time

import flint
import mpmath
import sympy as sp
from flint import arb, ctx, fmpq

from . import __version__, a2u

r, x, y = a2u.r, a2u.x, a2u.y
L2, L3 = sp.symbols("L2 L3", positive=True)
GENS = (r, x, y, L2, L3)

PREC = 128                      # Arb working precision (bits)
INTERVAL = (fmpq(0), fmpq(16, 5))
W_MAX = fmpq(1, 20)             # resolution cap on accepted boxes
MAX_DEPTH = 40                  # bisection limit before declaring failure
LB_BITS = 20                    # recorded lower bounds are multiples of 2^-LB_BITS
R0_NEAR_ZERO = fmpq(1, 8)       # initial interval handled by the separate near-zero argument

S = 3 * x + y + 3
N = S * (3 * r ** 3 * x + 81 * r + y * (3 * r + 2) + 126) - 3 * r * (3 * r * x - y - 9) ** 2
M_CLOSED = N / (16 * S ** 2)


def d_dr(e):
    """Total r-derivative with x = 2^(-r/2), y = 3^(-r/2)."""
    return sp.diff(e, r) + sp.diff(e, x) * (-L2 / 2 * x) + sp.diff(e, y) * (-L3 / 2 * y)


def forms():
    Sp = sp.expand(d_dr(S))
    Np = sp.expand(d_dr(N))
    Psi = sp.expand(S * Np - 2 * N * Sp)
    Phi = sp.expand(S * sp.expand(d_dr(Psi)) - 3 * Psi * Sp)
    return {"S": S, "S'": Sp, "N": sp.expand(N), "Psi": Psi, "Phi": Phi,
            "m": M_CLOSED, "m'": Psi / (16 * S ** 3), "m''": Phi / (16 * S ** 4)}


# ---- Arb evaluation (generator side: compiled monomial lists) ----------------------------------------------------
def _compile(poly_expr):
    P = sp.Poly(poly_expr, *GENS)
    terms = [(mon, fmpq(int(c.p), int(c.q))) for mon, c in P.terms()]
    maxdeg = [max((mon[i] for mon, _ in terms), default=0) for i in range(len(GENS))]

    def ev(vals):
        pows = []
        for v, dmax in zip(vals, maxdeg):
            row = [arb(1)]
            for _ in range(dmax):
                row.append(row[-1] * v)
            pows.append(row)
        tot = arb(0)
        for mon, c in terms:
            t = arb(c)
            for i, k in enumerate(mon):
                if k:
                    t = t * pows[i][k]
            tot += t
        return tot
    return ev


class Evaluator:
    def __init__(self, prec=PREC):
        ctx.prec = prec
        f = forms()
        self.psi = _compile(f["Psi"])
        self.phi = _compile(f["Phi"])
        self.L2 = arb(2).log()
        self.L3 = arb(3).log()

    def _vals(self, rb):
        xb = (-rb * self.L2 / 2).exp()
        yb = (-rb * self.L3 / 2).exp()
        return (rb, xb, yb, self.L2, self.L3), 3 * xb + yb + 3

    def m1(self, rb):
        vals, Sb = self._vals(rb)
        return self.psi(vals) / (16 * Sb ** 3)

    def m2(self, rb):
        vals, Sb = self._vals(rb)
        return self.phi(vals) / (16 * Sb ** 4)

    def mvf(self, lo, hi, sign=1):
        rb = arb(lo).union(arb(hi))
        c = (lo + hi) / 2
        rc = arb(c)
        return sign * (self.m1(rc) + (rb - rc) * self.m2(rb))


def dyadic_lower_bound(E, bits=LB_BITS):
    """Largest multiple of 2^-bits (minus one step) that the ball E certainly exceeds, checked by Arb."""
    v = float(E.lower().mid())
    n = math.floor(v * 2 ** bits) - 1
    q = fmpq(n, 2 ** bits)
    while not (E > arb(q)):
        n -= 1
        q = fmpq(n, 2 ** bits)
    return q


def certify(lo, hi, sign=1, bound=fmpq(0), w_max=W_MAX, max_depth=MAX_DEPTH, ev=None):
    """Adaptive certification of sign*m'(r) > bound on [lo, hi]. Returns dict(ok, boxes | failure)."""
    ev = Evaluator() if ev is None else ev
    stack = [(lo, hi, 0)]
    boxes = []
    while stack:
        a, b, d = stack.pop()
        E = ev.mvf(a, b, sign)
        if b - a <= w_max and E > arb(bound):
            boxes.append({"lo": str(a), "hi": str(b), "depth": d, "lower_bound": dyadic_lower_bound(E)})
            continue
        if d >= max_depth:
            return {"ok": False, "failure": {"lo": str(a), "hi": str(b), "depth": d, "enclosure": E.str(10)},
                    "boxes_accepted_before_failure": len(boxes)}
        mid = (a + b) / 2
        stack.append((mid, b, d + 1))
        stack.append((a, mid, d + 1))
    return {"ok": True, "boxes": boxes}


# ---- near r = 0: exact series and an initial-interval argument -----------------------------------------------------
def near_zero(ev=None):
    ev = Evaluator() if ev is None else ev
    f = forms()
    at0 = {r: 0, x: 1, y: 1}
    m1_0 = sp.expand(sp.simplify(f["m'"].subs(at0)))
    m2_0 = sp.expand(sp.simplify(f["m''"].subs(at0)))
    coeffs = {str(k): str(v) for k, v in sp.Poly(m1_0, L2, L3).as_dict().items()}
    # m'' > 0 on [0, R0] (direct Arb enclosures on 8 sub-boxes), hence m' increasing there and m'(r) >= m'(0)
    sub = []
    k = 8
    for i in range(k):
        a, b = R0_NEAR_ZERO * i / k, R0_NEAR_ZERO * (i + 1) / k
        E2 = ev.m2(arb(a).union(arb(b)))
        sub.append({"lo": str(a), "hi": str(b), "m''_lower_bound": str(dyadic_lower_bound(E2)) if E2 > 0 else "none",
                    "positive": bool(E2 > 0)})
    return {"m'(0) exact": str(m1_0), "m'(0) as polynomial in (L2, L3)": coeffs,
            "m'(0) positivity": "every coefficient (18/49, 12/49, 57/784) is a positive rational and L2, L3 > 0",
            "m'(0) enclosure": ev.m1(arb(0)).str(30),
            "m''(0) exact": str(m2_0), "m''(0) enclosure": ev.m2(arb(0)).str(30),
            "series": "m'(r) = m'(0) + m''(0) r + O(r^2), analytic at r = 0 (no division by r in the closed form)",
            "initial_interval": ["0", str(R0_NEAR_ZERO)], "m''_positive_on_subboxes": sub,
            "conclusion": "m'' > 0 on [0, 1/8] (certified) => m'(r) >= m'(0) > 0 on [0, 1/8]",
            "all_positive": all(s["positive"] for s in sub)}


# ---- P_A(q) < 16/5 for every q in (0, r*): rigorous inputs ---------------------------------------------------------
def pa_bound(prec=PREC):
    ctx.prec = prec
    hA = a2u.H_A_FROZEN
    dhA = sp.together(d_dr(hA))
    l2, l3 = arb(2).log(), arb(3).log()

    def val(e, rq):
        rb = arb(rq)
        xb, yb = (-rb * l2 / 2).exp(), (-rb * l3 / 2).exp()
        num, den = sp.fraction(sp.together(e))
        ev_n, ev_d = _compile(sp.expand(num)), _compile(sp.expand(den))
        vals = (rb, xb, yb, l2, l3)
        return ev_n(vals) / ev_d(vals)

    top = fmpq(16, 5)
    six7 = arb(fmpq(6, 7))
    hA_top, dhA_top = val(hA, top), val(dhA, top)
    a, b = fmpq(3105493355283091, 10 ** 15), fmpq(3105493355283092, 10 ** 15)
    s_lo, s_hi = fmpq(1474910738147221, 10 ** 15), fmpq(1474910738147222, 10 ** 15)
    out = {
        "h_A": str(hA), "h_A'": str(dhA),
        "h_A(16/5) enclosure": hA_top.str(25), "h_A(16/5) < -6/7": bool(hA_top + six7 < 0),
        "h_A'(16/5) enclosure": dhA_top.str(25), "h_A'(16/5) < 0 (so 16/5 > r*, Lemma A)": bool(dhA_top < 0),
        "P_A(0+) enclosure": [str(a), str(b)],
        "P_A(0+) enclosure certified": bool(val(hA, a) + six7 > 0 and val(hA, b) + six7 < 0 and val(dhA, a) < 0),
        "r* enclosure": [str(s_lo), str(s_hi)],
        "r* enclosure certified": bool(val(dhA, s_lo) > 0 and val(dhA, s_hi) < 0),
        "argument": ("Lemma A (Paper 2): h_A increases on (0, r*) from h_A(0+) = -6/7 and decreases strictly on "
                     "(r*, inf). For 0 < q < r*: h_A(P_A(q)) = h_A(q) > -6/7 > h_A(16/5), and P_A(q), 16/5 > r*, "
                     "so P_A(q) < 16/5. Hence 0 < q < r* < P_A(q) < 16/5."),
    }
    out["all_certified"] = all(out[k] for k in ("h_A(16/5) < -6/7", "h_A'(16/5) < 0 (so 16/5 > r*, Lemma A)",
                                                 "P_A(0+) enclosure certified", "r* enclosure certified"))
    return out


# ---- certificate --------------------------------------------------------------------------------------------------
def _sha(s):
    return hashlib.sha256(s.encode()).hexdigest()


def semantic_hash(cert):
    body = {k: v for k, v in cert.items() if k != "provenance"}
    return _sha(json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=True))


def build_certificate(root):
    t0 = time.time()
    ev = Evaluator(PREC)
    f = forms()
    res = certify(*INTERVAL, ev=ev)
    if not res["ok"]:
        raise RuntimeError(f"certification failed: {res['failure']}")
    boxes = [{"lo": b["lo"], "hi": b["hi"], "lower_bound": str(b["lower_bound"])} for b in res["boxes"]]
    lmin = min(b["lower_bound"] for b in res["boxes"])
    expr = {"m": str(f["m"]), "S": str(f["S"]), "S'": str(f["S'"]), "N": str(f["N"]), "Psi": str(f["Psi"]),
            "Phi": str(f["Phi"]), "m'": "Psi/(16*S**3)", "m''": "Phi/(16*S**4)"}
    cert = {
        "certificate": "Lemma M (EIT-LJ Cube Bifurcations, Paper 3, Phase A2)",
        "statement": "m'(r) > 0 for every r in [0, 16/5]; m is the V0.1-dev closed form",
        "claim": {"quantity": "m'(r)", "relation": ">", "value": "0", "interval": [str(INTERVAL[0]), str(INTERVAL[1])]},
        "variables": {"x": "2^(-r/2)", "y": "3^(-r/2)", "L2": "log 2", "L3": "log 3",
                      "d/dr": "dx/dr = -(L2/2) x, dy/dr = -(L3/2) y"},
        "expressions": expr,
        "expression_sha256": {k: _sha(v) for k, v in expr.items()},
        "method": {"arithmetic": "Arb ball arithmetic (python-flint), outward rounding",
                   "arb_precision_bits": PREC,
                   "box_test": "m'(B) in m'(c) + (B - c) m''(B), c = midpoint, B = Arb ball containing [lo, hi]",
                   "subdivision": "recursive bisection from [0, 16/5] until certified and width <= 1/20",
                   "w_max": str(W_MAX), "max_depth": MAX_DEPTH, "lower_bound_grid": f"2^-{LB_BITS}"},
        "boxes": boxes,
        "n_boxes": len(boxes),
        "max_depth_used": max(b["depth"] for b in res["boxes"]),
        "min_lower_bound": str(lmin),
        "min_lower_bound_decimal": mpmath.nstr(mpmath.mpf(int(lmin.p)) / int(lmin.q), 12),
        "near_zero": near_zero(ev),
        "P_A_bound": pa_bound(PREC),
    }
    code = {p: _sha((root / p).read_text()) for p in ("src/cube_bif/lemma_m.py", "src/cube_bif/certcheck.py",
                                                      "src/cube_bif/a2u.py", "scripts/run_A2.py")}
    cert["provenance"] = {
        "excluded_from_semantic_hash": True,
        "seconds": round(time.time() - t0, 3),
        "timestamp_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),
        "project_version": __version__, "python": sys.version.split()[0], "platform": platform.platform(),
        "python-flint": flint.__version__, "FLINT": flint.__FLINT_VERSION__, "sympy": sp.__version__,
        "mpmath": mpmath.__version__, "code_sha256": code,
    }
    cert["provenance"]["semantic_sha256"] = semantic_hash(cert)
    return cert
