"""Phase B1.7: Arb certificate that the normalised cubic carrier kappa_hat is positive on the whole closed T2g curve.

Functions (r real; X = 2^(-r/2), Y = 3^(-r/2), W = 1 + X + Y/3):
- M(r), Paper 2's 2x2 block;
- g_m(r), m in {uuu, uuv, uvv, vvv}, from b1_cubic.G_CLOSED.
Divided differences f_hat(p, q) = (f(p) - f(q))/(p - q), and f'(q) at p = q.

Curve. delta = p - q. On the curve D~(q, delta) := det M_hat(q + delta, q) = 0. Paper 2 (FROZEN INPUT): Lemma T3
gives exactly one zero with delta > 0 for each 0 <= q < q_c, namely delta = P_T(q) - q; Lemma T2 gives
det M'(q) > 0 on [0, q_c), and D~(q_c, 0) = det M'(q_c) = 0. For each rational q-box Q, a parametric interval Newton
step proves that for every q in Q there is exactly one zero of D~(q, .) in a ball Delta.

Divided differences on a box:
- far regime (inf Delta > 1): direct quotients of balls;
- near regime: the Taylor form
      f_hat(q + delta, q) = sum_{j=1..N} c_j(q) delta^(j-1) + delta^N c_{N+1}(xi),  xi in hull(Q, Q + Delta),
  with c_j = f^(j)/j! from arb_series; there is no division by delta.

Carrier: rho = -Mh12/Mh22 (chart n = (1, rho); valid where Mh22 != 0), and
kappa_hat = gh_uuu + 3 rho gh_uuv + 3 rho^2 gh_uvv + rho^3 gh_vvv.
On every box the certificate proves Mh22 > 0 and kappa_hat > (dyadic lower bound) > 0.
"""
import contextlib
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
from . import b1_cubic as b1

PREC = 128
Q_START, Q_END = fmpq(0), fmpq(101, 50)
CORNER = (fmpq(2019, 1000), fmpq(101, 50))            # the only box allowed to reach delta <= 0
BASE = [fmpq(k, 100) for k in range(202)] + [fmpq(2019, 1000), fmpq(101, 50)]
FAR = fmpq(1)
NEAR_MAX = fmpq(5, 4)
N_TAYLOR = 16
DELTA_GRID_BITS = 80
LB_BITS = 30
MAX_DEPTH = 12
NAMES = ("M11", "M12", "M22") + b1.CHANNELS

EXPRESSIONS = {
    "X": "2**(-r/2)", "Y": "3**(-r/2)", "W": "1 + X + Y/3",
    "M11": "(r*X + 2*(2*r + 1)*Y/9 - 2)/W",
    "M12": "2*sqrt(2)*(r + 2)*Y/(9*W)",
    "M22": "(2*r + 2*(r - 1)*Y/9 - 2)/W",
    "uuu": str(b1.G_CLOSED["uuu"]).replace("Xr", "X").replace("Yr", "Y"),
    "uuv": str(b1.G_CLOSED["uuv"]).replace("Xr", "X").replace("Yr", "Y"),
    "uvv": str(b1.G_CLOSED["uvv"]).replace("Xr", "X").replace("Yr", "Y"),
    "vvv": str(b1.G_CLOSED["vvv"]).replace("Xr", "X").replace("Yr", "Y"),
    "curve": "D~(q, delta) = Mh11*Mh22 - Mh12**2 = 0, Mh = M_hat(q + delta, q)",
    "chart": "rho = -Mh12/Mh22, n = (1, rho)",
    "kappa_hat": "gh_uuu + 3*rho*gh_uuv + 3*rho**2*gh_uvv + rho**3*gh_vvv",
    "kappa": "q*W_q*(p - q)*kappa_hat / (1 + rho**2)**(3/2)   (unit n, n_u > 0)",
}


def _set_prec():
    ctx.prec = PREC


def _funcs(x):
    """All seven functions at x (an arb ball or an arb_series)."""
    L2, L3 = arb(2).log(), arb(3).log()
    X = (-(L2 / 2) * x).exp()
    Y = (-(L3 / 2) * x).exp()
    W = 1 + X + Y / 3
    s2 = arb(2).sqrt()
    return {
        "M11": (x * X + 2 * (2 * x + 1) * Y / 9 - 2) / W,
        "M12": 2 * s2 * (x + 2) * Y / (9 * W),
        "M22": (2 * x + 2 * (x - 1) * Y / 9 - 2) / W,
        "uuu": (x + 2) * (-arb(3) / 4 * X + (4 * x + 7) * Y / 27) / W,
        "uuv": s2 * (x + 2) * (4 * x + 1) * Y / (54 * W),
        "uvv": (x + 2) * (-2 + 2 * (x + 1) * Y / 27) / W,
        "vvv": s2 * (x + 2) * (x + 4) * Y / (27 * W),
    }


class SeriesTruncationError(ArithmeticError):
    """A Taylor series is shorter than requested for a reason other than exact trailing zeros (erratum E-B1)."""


@contextlib.contextmanager
def _series_capacity(n):
    """Erratum E-B1 (V0.4-dev.4). python-flint truncates every arb_series at the context length ctx.cap (default 10),
    whatever prec= asks for. Inside this block ctx.cap is at least n; the previous value is restored on exit, also when
    an exception is raised. Yields the capacity in force."""
    old = ctx.cap
    try:
        ctx.cap = max(old, n)
        if ctx.cap < n:
            raise SeriesTruncationError(f"ctx.cap = {ctx.cap} could not be raised to {n}")
        yield ctx.cap
    finally:
        ctx.cap = old


def _series_coefficients(x, n):
    """{name: coefficient list} of every function at the series x + t, computed with ctx.cap >= n and prec = n."""
    with _series_capacity(n) as cap:
        vals = _funcs(arb_series([x, 1], prec=n))
        coeffs = {k: list(v.coeffs()) for k, v in vals.items()}
        if ctx.cap != cap or cap < n:
            raise SeriesTruncationError("ctx.cap changed or below the requested length during the series evaluation")
    for k, c in coeffs.items():
        if len(c) > n:
            raise SeriesTruncationError(f"{k}: series longer than requested ({len(c)} > {n})")
    return coeffs


def _taylor(x, n):
    """Taylor coefficients c_0..c_{n-1} of each function at the ball x (enclosures valid for every point of x).

    Erratum E-B1 (V0.4-dev.4; NOTES.md §10). Up to V0.4-dev.3 this routine did not raise ctx.cap and padded the
    cap-truncated coefficient list with zeros, so c_10, c_11, ... were silently replaced by 0. Now the series is
    computed with ctx.cap >= n (restored afterwards). A shorter result can then only come from python-flint trimming
    exact trailing zeros; this is checked by a recomputation with a longer series, in which every missing position must
    be absent or exactly zero, before the list is padded. Anything else raises SeriesTruncationError."""
    out = _series_coefficients(x, n)
    short = [k for k, c in out.items() if len(c) < n]
    if short:
        longer = _series_coefficients(x, n + 4)
        for k in short:
            c, c2 = out[k], longer[k]
            if any(not (c2[j] == 0) for j in range(len(c), min(n, len(c2)))):
                raise SeriesTruncationError(f"{k}: series shorter than requested and the missing coefficients are "
                                            f"not exact zeros")
            out[k] = c + [arb(0)] * (n - len(c))
    for k, c in out.items():
        if len(c) != n:
            raise SeriesTruncationError(f"{k}: {len(c)} coefficients instead of {n}")
    return out


def _hull(a, b):
    return a.union(b)


def divided(Q, D, regime):
    """Enclosures over q in Q, delta in D of f_hat(q + delta, q), d/d delta f_hat and d/dq f_hat (delta fixed)."""
    N = N_TAYLOR
    if regime == "far":
        P = Q + D
        fQ, fP = _funcs(Q), _funcs(P)
        tQ, tP = _taylor(Q, 2), _taylor(P, 2)
        val = {k: (fP[k] - fQ[k]) / D for k in NAMES}
        dval = {k: (tP[k][1] - val[k]) / D for k in NAMES}
        qval = {k: (tP[k][1] - tQ[k][1]) / D for k in NAMES}
        return val, dval, qval
    H = _hull(Q, Q + D)
    cQ, cH = _taylor(Q, N + 2), _taylor(H, N + 3)
    val, dval, qval = {}, {}, {}
    DN = D ** N
    for k in NAMES:
        c, h = cQ[k], cH[k]
        v = arb(0)
        for j in range(N, 0, -1):
            v = v * D + c[j]
        val[k] = v + DN * h[N + 1]
        dv = arb(0)
        for j in range(N, 1, -1):
            dv = dv * D + (j - 1) * c[j]
        dval[k] = dv + N * D ** (N - 1) * h[N + 1] + DN * h[N + 2]
        qv = arb(0)
        for j in range(N, 0, -1):
            qv = qv * D + (j + 1) * c[j + 1]
        qval[k] = qv + (N + 2) * DN * h[N + 2]
    return val, dval, qval


def _det_parts(val, dval=None):
    a, b, c = val["M11"], val["M12"], val["M22"]
    F = a * c - b * b
    if dval is None:
        return F
    return F, dval["M11"] * c + a * dval["M22"] - 2 * b * dval["M12"]


def F_centered(Q, m, regime):
    """D~(q, m) for all q in Q, by the mean-value form in q around the midpoint of Q."""
    q0 = arb(Q.mid())
    v0 = divided(q0, m, regime)[0]
    vQ, _, qQ = divided(Q, m, regime)
    a, b, c = vQ["M11"], vQ["M12"], vQ["M22"]
    Fq = qQ["M11"] * c + a * qQ["M22"] - 2 * b * qQ["M12"]
    return _det_parts(v0) + Fq * (Q - q0)


def newton(Q, D, regime, iters=8):
    """Parametric interval Newton in delta. Returns the contracted ball, or None if no strict inclusion."""
    proven = False
    for _ in range(iters):
        m = arb(D.mid())
        Fm = F_centered(Q, m, regime)
        val, dval, _ = divided(Q, D, regime)
        _, Fd = _det_parts(val, dval)
        if not (Fd < 0 or Fd > 0):
            return None
        Nw = m - Fm / Fd
        if Nw.lower() > D.lower() and Nw.upper() < D.upper():
            proven, D = True, Nw
        elif proven:
            D = D.intersection(Nw)
        else:
            return None
    return D if proven else None


def _carrier_value(val):
    c = val["M22"]
    rho = -val["M12"] / c
    kh = val["uuu"] + 3 * rho * val["uuv"] + 3 * rho ** 2 * val["uvv"] + rho ** 3 * val["vvv"]
    return kh, c, rho


def _carrier_slope(val, der):
    """Derivative of (kappa_hat, Mh22) along one variable, from values and derivatives of the seven functions."""
    b, c = val["M12"], val["M22"]
    rho = -b / c
    rho_x = -(der["M12"] * c - b * der["M22"]) / (c * c)
    g, gx = [val[m] for m in b1.CHANNELS], [der[m] for m in b1.CHANNELS]
    kx = (gx[0] + 3 * (rho_x * g[1] + rho * gx[1]) + 3 * (2 * rho * rho_x * g[2] + rho ** 2 * gx[2])
          + 3 * rho ** 2 * rho_x * g[3] + rho ** 3 * gx[3])
    return kx, der["M22"]


def carrier_enclosure(Q, D, regime):
    """Mean-value form in (q, delta) around the centre of the box: value at the centre plus slope enclosures over the
    box times the half-widths. Returns enclosures of kappa_hat, Mh22 and rho over the box."""
    q0, d0 = arb(Q.mid()), arb(D.mid())
    k0, c0, _ = _carrier_value(divided(q0, d0, regime)[0])
    val, dval, qval = divided(Q, D, regime)
    kq, cq = _carrier_slope(val, qval)
    kd, cd = _carrier_slope(val, dval)
    kh = k0 + kq * (Q - q0) + kd * (D - d0)
    m22 = c0 + cq * (Q - q0) + cd * (D - d0)
    return kh, m22, _carrier_value(val)[2]


# ---- exact bookkeeping ------------------------------------------------------------------------------------------------
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


def outward(D, bits=DELTA_GRID_BITS):
    """Round the ball D outward to a dyadic grid: exact rational endpoints."""
    s = fmpz(2) ** bits
    lo, hi = arb_to_fmpq(D.lower()), arb_to_fmpq(D.upper())
    lo_r = fmpq((lo * s).floor(), s)
    hi_r = fmpq((hi * s).ceil(), s)
    return lo_r, hi_r


def dyadic_lower_bound(E, bits=LB_BITS, margin=fmpq(1, 8)):
    """A dyadic number strictly below the ball E, lowered further by `margin` times the width of E, so that an
    independent evaluation with slightly wider balls can still confirm it."""
    s = fmpz(2) ** bits
    lo, hi = arb_to_fmpq(E.lower()), arb_to_fmpq(E.upper())
    k = ((lo - margin * (hi - lo)) * s).floor() - 1
    while not (E > arb(fmpq(k, s))):
        k -= 1
    return fmpq(k, s)


# ---- curve estimates (mpmath; only starting points, never used as proof) ------------------------------------------------
def _delta_estimate(qq, guess=None):
    with mp.workdps(30):
        qq = mp.mpf(int(qq.p)) / int(qq.q) if isinstance(qq, fmpq) else mp.mpf(qq)
        if guess is None:
            if qq < mp.mpf("2.0199"):
                return b1.curve_delta(qq)
            guess = 2 * (mp.mpf(b1.QC_LO) - qq)
        return mp.findroot(lambda d: b1.D_tilde(qq, d), mp.mpf(guess))


def initial_delta(qlo, qhi, est):
    a, b = est(qlo), est(qhi)
    lo, hi = min(a, b), max(a, b)
    pad = (hi - lo) / 2 + mp.mpf("1e-12") * (1 + abs(hi))
    return fmpq(int(mp.floor((lo - pad) * 2 ** 60)), 2 ** 60), fmpq(int(mp.ceil((hi + pad) * 2 ** 60)), 2 ** 60)


# ---- one box -----------------------------------------------------------------------------------------------------------
def certify_box(qlo, qhi, est, corner=False, claim_bound=fmpq(0), carrier=None):
    """Returns (record, None) on success or (None, reason)."""
    _set_prec()
    Q = ball(qlo, qhi)
    dlo, dhi = initial_delta(qlo, qhi, est)
    regime = "far" if dlo > FAR else "near"
    if regime == "near" and max(abs(dlo), abs(dhi)) > NEAR_MAX:
        return None, "delta range too wide for the Taylor form"
    D = newton(Q, ball(dlo, dhi), regime)
    if D is None:
        return None, "Newton inclusion failed"
    w = D.upper() - D.lower()
    slack = w / 4 + arb(fmpq(1, 2 ** 70))
    rlo, rhi = outward(_hull(D.lower() - slack, D.upper() + slack))
    Dr = ball(rlo, rhi)
    if newton(Q, Dr, regime, iters=1) is None:
        return None, "Newton inclusion failed on the rounded ball"
    if not corner and not rlo > 0:
        return None, "delta not positive"
    kh, m22, rho = (carrier or carrier_enclosure)(Q, Dr, regime)
    if not m22 > 0:
        return None, "Mh22 not certified positive"
    if not kh > arb(claim_bound):
        return None, "carrier not certified above the claimed bound"
    lb = dyadic_lower_bound(kh)
    if not lb > claim_bound:
        return None, "lower bound not above the claimed bound"
    return {"q_lo": str(qlo), "q_hi": str(qhi), "regime": regime, "delta_lo": str(rlo), "delta_hi": str(rhi),
            "kappa_hat_lower_bound": str(lb), "corner": corner}, None


def certify_interval(qa, qb, est, claim_bound=fmpq(0), carrier=None, max_depth=MAX_DEPTH, base=None):
    """Adaptive bisection of [qa, qb] (or of the given base partition). Returns (boxes, failure)."""
    pts = base if base is not None else [qa, qb]
    todo = [(pts[i], pts[i + 1], 0) for i in range(len(pts) - 1)][::-1]
    boxes, maxd = [], 0
    while todo:
        lo, hi, depth = todo.pop()
        corner = (lo, hi) == CORNER
        rec, why = certify_box(lo, hi, est, corner=corner, claim_bound=claim_bound, carrier=carrier)
        if rec is not None:
            rec["depth"] = depth
            boxes.append(rec)
            maxd = max(maxd, depth)
            continue
        if corner or depth >= max_depth:
            return boxes, {"q_lo": str(lo), "q_hi": str(hi), "depth": depth, "reason": why}
        mid = (lo + hi) / 2
        todo.append((mid, hi, depth + 1))
        todo.append((lo, mid, depth + 1))
    return boxes, None


# ---- endpoints and the corner box ---------------------------------------------------------------------------------------
def endpoint_q0():
    _set_prec()
    Q = arb(0)
    lo, hi = fmpq(4796368189344416004181122459356, 10 ** 30), fmpq(4796368189344416004181122459357, 10 ** 30)
    pad = fmpq(1, 10 ** 20)
    D = newton(Q, ball(lo - pad, hi + pad), "far")
    kh, m22, rho = carrier_enclosure(Q, D, "far")
    return {"P_T(0)_enclosure": [str(x) for x in outward(D, 120)],
            "paper2_enclosure": ["4.796368189344416004181122459356", "4.796368189344416004181122459357"],
            "overlaps_paper2": bool(D.overlaps(ball(lo, hi))),
            "kappa_hat": kh.str(25), "kappa_hat_lower_bound": str(dyadic_lower_bound(kh)), "rho": rho.str(20),
            "Mh22": m22.str(20), "certified": bool(kh > 0 and m22 > 0)}


def endpoint_corner():
    _set_prec()
    lo = fmpq(20199382317007999883028831854985758749007, 10 ** 40)
    hi = fmpq(20199382317007999883028831854985758749008, 10 ** 40)
    Q = ball(lo, hi)
    kh, m22, rho = carrier_enclosure(Q, arb(0), "near")
    ctx.prec = 4 * PREC                                    # det M' is about 1e-41 at these endpoints
    dlo = _det_parts(divided(arb(lo), arb(0), "near")[0])
    dhi = _det_parts(divided(arb(hi), arb(0), "near")[0])
    _set_prec()
    return {"q_c_enclosure_paper2_lemma_T2": [b1.QC_LO, b1.QC_HI],
            "det_M_prime_at_lo": dlo.str(10), "det_M_prime_at_hi": dhi.str(10),
            "sign_change_consistent_with_lemma_T2": bool(dlo > 0 and dhi < 0),
            "kappa_hat": kh.str(25), "kappa_hat_lower_bound": str(dyadic_lower_bound(kh)), "rho": rho.str(20),
            "Mh22": m22.str(20), "certified": bool(kh > 0 and m22 > 0)}


def corner_identification(corner_rec):
    """At q = q_lo of the corner box, Newton inside the box's Delta gives a positive enclosure: the zero in Delta is
    the physical one there; by continuity and Lemma T2 it stays positive for q < q_c in the box."""
    _set_prec()
    qlo = parse_q(corner_rec["q_lo"])
    D = ball(parse_q(corner_rec["delta_lo"]), parse_q(corner_rec["delta_hi"]))
    Da = newton(arb(qlo), D, corner_rec["regime"])
    ok = Da is not None and Da.lower() > 0
    lo, hi = outward(Da) if Da is not None else (None, None)
    return {"q": str(qlo), "delta_lo": str(lo), "delta_hi": str(hi), "positive": bool(ok),
            "q_c_inside_corner_box": bool(CORNER[0] < fmpq(20199382317007999883028831854985758749007, 10 ** 40)
                                          and fmpq(20199382317007999883028831854985758749008, 10 ** 40) < CORNER[1])}


# ---- certificate --------------------------------------------------------------------------------------------------------
def _cached_estimator():
    cache = {}

    def est(qq):
        key = (int(qq.p), int(qq.q))
        if key not in cache:
            cache[key] = _delta_estimate(qq)
        return cache[key]
    return est


def semantic_hash(cert):
    body = {k: v for k, v in cert.items() if k != "provenance"}
    return hashlib.sha256(json.dumps(body, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def build_certificate(root=None):
    t0 = time.time()
    est = _cached_estimator()
    boxes, fail = certify_interval(Q_START, Q_END, est, base=BASE)
    if fail is not None:
        raise RuntimeError(f"B1 certificate failed: {fail}")
    corner_rec = [b for b in boxes if b["corner"]]
    lbs = [parse_q(b["kappa_hat_lower_bound"]) for b in boxes]
    mn = min(lbs)
    exprs = json.dumps(EXPRESSIONS, sort_keys=True)
    cert = {
        "certificate": "EIT-LJ Cube Bifurcations (Paper 3), Phase B1: kappa_hat > 0 on the closed T2g curve",
        "statement": ("For every q in [0, 101/50] and every zero delta of D~(q, .) in the recorded ball (the physical "
                      "curve delta = P_T(q) - q for 0 <= q < q_c, the corner (q_c, 0), and a short mirror arc beyond "
                      "q_c): Mh22 > 0 and kappa_hat > recorded lower bound > 0."),
        "claim": {"quantity": "kappa_hat", "relation": ">", "value": "0", "q_interval": ["0", "101/50"]},
        "expressions": EXPRESSIONS,
        "expression_sha256": hashlib.sha256(exprs.encode()).hexdigest(),
        "frozen_inputs": {"paper2_lemma_T2_q_c": [b1.QC_LO, b1.QC_HI],
                          "paper2_lemma_T3": "exactly one p = P_T(q) > q with D(p, q) = 0, for 0 <= q < q_c",
                          "paper2_prop_supplementary_P_T(0)": [b1.PT0_LO, b1.PT0_HI]},
        "method": {"arb_precision_bits": PREC, "curve": "parametric interval Newton in delta, mean-value form in q",
                   "divided_differences": {"far (inf Delta > 1)": "ball quotients",
                                           "near": f"Taylor form, N = {N_TAYLOR}, remainder over hull(Q, Q+Delta)"},
                   "base_partition": "k/100 for k = 0..201, then 2019/1000, 101/50",
                   "corner_box": [str(CORNER[0]), str(CORNER[1])], "max_depth": MAX_DEPTH,
                   "delta_ball": f"Newton-contracted ball widened by 1/4 of its width on each side, rounded "
                                 f"outward to 2^-{DELTA_GRID_BITS}, re-verified", "lower_bound": f"dyadic (2^-{LB_BITS}) below the enclosure by 1/8 of its width"},
        "boxes": boxes,
        "n_boxes": len(boxes),
        "max_depth_used": max(b["depth"] for b in boxes),
        "min_lower_bound": str(mn),
        "min_lower_bound_decimal": mp.nstr(mp.mpf(int(mn.p)) / int(mn.q), 12),
        "corner_identification": corner_identification(corner_rec[0]),
        "endpoints": {"q=0": endpoint_q0(), "corner": endpoint_corner()},
    }
    code = {}
    if root is not None:
        for f in ("src/cube_bif/b1_cert.py", "src/cube_bif/b1_check.py", "src/cube_bif/b1_cubic.py",
                  "scripts/run_B1.py"):
            pth = pathlib.Path(root) / f
            if pth.exists():
                code[f] = hashlib.sha256(pth.read_bytes()).hexdigest()
    cert["provenance"] = {
        "excluded_from_semantic_hash": True, "seconds": round(time.time() - t0, 1),
        "timestamp_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "project_version": __version__,
        "python": sys.version.split()[0], "platform": platform.platform(), "python-flint": flint.__version__,
        "FLINT": flint.__FLINT_VERSION__, "sympy": sp.__version__, "mpmath": mp.__version__, "code_sha256": code}
    cert["provenance"]["semantic_sha256"] = semantic_hash(cert)
    return cert
