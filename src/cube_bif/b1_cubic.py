"""Phase B1: the cubic coefficient kappa = D^3V[e_1, e_2, e_3] of the critical T2g representation on p = P_T(q).

Basis (B0): uh_k = -W_k/4 and vh_k = -(sqrt2/4) U_k, k = 1, 2, 3 (orthonormal, matched: both copies transform by
T(R) = sigma(R) R). Critical vectors e_k = n_u uh_k + n_v vh_k with n in ker K, K = q W_q [M(p) - M(q)].

Route 1 (symmetry-adapted). All 216 trilinear values D^3V[b_i, b_j, b_k] on the six basis vectors, from the exact
pair-sum formula of pairsum.py, as linear forms in psi^(k)(sigma) for a generic pair potential. The identities that
O_h-equivariance predicts are checked on this table before they are used.

Route 2 (raw 24-D). The third-derivative tensor of V(x) = sum psi(|x_i - x_j|^2) in the 24 coordinates, by SymPy
differentiation of each pair term in its own six coordinates, contracted with the 24-vectors. No T2g reduction, no
Faa di Bruno formula.

Two-term specialisation (A = t, B = 1). Every independent coefficient is a difference form q W_q [g_m(p) - g_m(q)]
with g_m in closed form. So kappa = q W_q (p - q) kappa_hat, where kappa_hat uses divided differences.
"""
import itertools
from functools import lru_cache

import mpmath as mp
import sympy as sp

from . import pairsum as ps
from .group import LABELS
from .modes import U_T2G, W_T2G, Y_STAR
from .t2g import M_num, M_paper2, UH, VH

CHANNELS = ("uuu", "uuv", "uvv", "vvv")
BINOM = {"uuu": 1, "uuv": 3, "uvv": 3, "vvv": 1}
nu, nv = sp.symbols("n_u n_v")
a1, a2, a3 = sp.symbols("a1 a2 a3")
rho = sp.Symbol("rho")
r, Xr, Yr = ps.r_, ps.X["r"], ps.Y["r"]
S2 = sp.sqrt(2)

# Closed forms g_m(r), with X = 2^(-r/2), Y = 3^(-r/2), W = 1 + X + Y/3 (verified in tests against pairsum.g_of).
WR = 1 + Xr + Yr / 3
G_CLOSED = {
    "uuu": (r + 2) * (-sp.Rational(3, 4) * Xr + (4 * r + 7) * Yr / 27) / WR,
    "uuv": S2 * (r + 2) * (4 * r + 1) * Yr / (54 * WR),
    "uvv": (r + 2) * (-2 + 2 * (r + 1) * Yr / 27) / WR,
    "vvv": S2 * (r + 2) * (r + 4) * Yr / (27 * WR),
}
M_CLOSED = M_paper2(r, Xr, Yr)


# ---- route 1: symmetry-adapted trilinear table -------------------------------------------------------------------
_DIRS = {"u": W_T2G, "v": U_T2G}
_SCALE = {"u": sp.Rational(-1, 4), "v": -S2 / 4}


@lru_cache(maxsize=None)
def trilinear_table():
    """{(channel, (i, j, k)): D^3V[b^c0_i, b^c1_j, b^c2_k]} for all 8 channels and 27 index triples (216 values)."""
    out = {}
    for ch in itertools.product("uv", repeat=3):
        for idx in itertools.product(range(3), repeat=3):
            L = ps.derivative([_DIRS[ch[m]][idx[m]] for m in range(3)])
            out[("".join(ch), idx)] = sp.expand(L * _SCALE[ch[0]] * _SCALE[ch[1]] * _SCALE[ch[2]])
    return out


def independent_coefficients(table=None):
    """t_m = D^3V[b_1, b_2, b_3] in the channels uuu, uuv, uvv, vvv (indices 1, 2, 3)."""
    table = trilinear_table() if table is None else table
    return {m: table[(m, (0, 1, 2))] for m in CHANNELS}


def kappa_form(n_u=nu, n_v=nv, coeffs=None):
    """kappa = sum over channels of binom * n_u^(#u) n_v^(#v) * t_m (a cubic polynomial in n_u, n_v)."""
    t = independent_coefficients() if coeffs is None else coeffs
    return sp.expand(sum(BINOM[m] * n_u ** m.count("u") * n_v ** m.count("v") * t[m] for m in CHANNELS))


# ---- route 2: raw 24-D third-derivative tensor --------------------------------------------------------------------
@lru_cache(maxsize=None)
def raw24_pair_tensors():
    """For each pair (i, j): the nonzero third derivatives of psi(|x_i - x_j|^2) in its six coordinates (x_i, x_j),
    at the cube, as linear forms in PSI. SymPy differentiates the pair term in the six coordinates; psi is replaced
    by its cubic Taylor polynomial at sigma = |r_ij|^2, which is exact for third derivatives at the cube."""
    z = sp.symbols("z0:6")                                  # (x_i, x_j) local coordinates
    sig = sum((z[c] - z[3 + c]) ** 2 for c in range(3))
    triples = list(itertools.combinations_with_replacement(range(6), 3))
    out = {}
    for i, j in itertools.combinations(range(8), 2):
        base = [sp.Rational(LABELS[i][c], 2) for c in range(3)] + [sp.Rational(LABELS[j][c], 2) for c in range(3)]
        sv = int(sum((base[c] - base[3 + c]) ** 2 for c in range(3)))
        f = sum(ps.PSI[(k, sv)] * (sig - sv) ** k / sp.factorial(k) for k in range(1, 4))
        ent = {}
        for abc in triples:
            d = sp.expand(sp.diff(f, *[z[m] for m in abc]).subs(dict(zip(z, base)), simultaneous=True))
            if d != 0:
                ent[abc] = d
        out[(i, j)] = ent
    return out


def raw24_contract(d1, d2, d3):
    """D^3V[d1, d2, d3] from the raw tensor; d1, d2, d3 are 24-vectors (SymPy Matrix or list, may be symbolic)."""
    tot = 0
    for (i, j), ent in raw24_pair_tensors().items():
        loc = lambda d: [d[3 * i + c] for c in range(3)] + [d[3 * j + c] for c in range(3)]
        x1, x2, x3 = loc(d1), loc(d2), loc(d3)
        for (a, b, c), val in ent.items():
            perms = set(itertools.permutations((a, b, c)))
            tot += val * sum(x1[s[0]] * x2[s[1]] * x3[s[2]] for s in perms)
    return sp.expand(tot)


def critical_vectors(n_u=nu, n_v=nv):
    return [n_u * UH[k] + n_v * VH[k] for k in range(3)]


# ---- two-term specialisation ---------------------------------------------------------------------------------------
def difference_form_residual(m):
    """t_m at the equilibrium minus q W_q [g_m(p) - g_m(q)]; zero identically (tested)."""
    t = independent_coefficients()[m].subs(ps.two_term())
    g = G_CLOSED[m]
    gp = g.subs({r: ps.p_, Xr: ps.X["p"], Yr: ps.Y["p"]}, simultaneous=True)
    gq = g.subs({r: ps.q_, Xr: ps.X["q"], Yr: ps.Y["q"]}, simultaneous=True)
    return sp.simplify(sp.together(t - ps.q_ * ps.W("q") * (gp - gq)))


# ---- numeric layer (mpmath) ---------------------------------------------------------------------------------------
def g_num(rr):
    rr = mp.mpf(rr)
    X_, Y_ = mp.power(2, -rr / 2), mp.power(3, -rr / 2)
    W_ = 1 + X_ + Y_ / 3
    s2 = mp.sqrt(2)
    return {"uuu": (rr + 2) * (-mp.mpf(3) / 4 * X_ + (4 * rr + 7) * Y_ / 27) / W_,
            "uuv": s2 * (rr + 2) * (4 * rr + 1) * Y_ / (54 * W_),
            "uvv": (rr + 2) * (-2 + 2 * (rr + 1) * Y_ / 27) / W_,
            "vvv": s2 * (rr + 2) * (rr + 4) * Y_ / (27 * W_)}


def W_num(rr):
    rr = mp.mpf(rr)
    return 1 + mp.power(2, -rr / 2) + mp.power(3, -rr / 2) / 3


def divided(f, pp, qq):
    """(f(p) - f(q)) / (p - q), and f'(q) at p = q; f returns a dict or an mpmath matrix."""
    pp, qq = mp.mpf(pp), mp.mpf(qq)
    if abs(pp - qq) > mp.mpf(10) ** (-(mp.mp.dps // 3)):
        a, b = f(pp), f(qq)
        if isinstance(a, dict):
            return {k: (a[k] - b[k]) / (pp - qq) for k in a}
        return (a - b) / (pp - qq)
    h = pp - qq
    if isinstance(f(qq), dict):
        return {k: mp.diff(lambda t: f(t)[k], qq) + mp.diff(lambda t: f(t)[k], qq, 2) * h / 2 for k in f(qq)}
    return mp.matrix([[mp.diff(lambda t: f(t)[i, j], qq) + mp.diff(lambda t: f(t)[i, j], qq, 2) * h / 2
                       for j in range(2)] for i in range(2)])


def M_hat(pp, qq):
    return divided(M_num, pp, qq)


def D_tilde(qq, dd):
    """det M_hat(q + delta, q) = D(q + delta, q) / delta^2 (Paper 2's D~)."""
    return mp.det(M_hat(mp.mpf(qq) + dd, qq))


def curve_delta(qq):
    """delta(q) = P_T(q) - q for 0 <= q < q_c: the unique sign change of D~(q, .) on (0, 6) (Paper 2, Lemma T3)."""
    qq = mp.mpf(qq)
    grid = [mp.mpf(10) ** (-8 + mp.mpf(j) / 10) for j in range(81)] + [mp.mpf(j) / 50 for j in range(51, 300)]
    vals = [D_tilde(qq, x) for x in grid]
    hits = [i for i in range(len(grid) - 1) if vals[i] > 0 >= vals[i + 1]]
    if len(hits) != 1:
        raise ArithmeticError(f"delta({qq}): {len(hits)} sign changes")
    i = hits[0]
    return mp.findroot(lambda x: D_tilde(qq, x), (grid[i], grid[i + 1]), solver="anderson")


def M_prime(rr):
    return mp.matrix([[mp.diff(lambda t: M_num(t)[i, j], rr) for j in range(2)] for i in range(2)])


def carrier(qq, dd=None):
    """Normalised carrier on the curve: rho = -Mh12/Mh22 (chart n = (1, rho)),
    kappa_hat = gh_uuu + 3 rho gh_uuv + 3 rho^2 gh_uvv + rho^3 gh_vvv, and the transversality quantities."""
    qq = mp.mpf(qq)
    dd = curve_delta(qq) if dd is None else mp.mpf(dd)
    pp = qq + dd
    Mh = M_hat(pp, qq)
    rh = -Mh[0, 1] / Mh[1, 1]
    gh = divided(g_num, pp, qq)
    kh = gh["uuu"] + 3 * rh * gh["uuv"] + 3 * rh ** 2 * gh["uvv"] + rh ** 3 * gh["vvv"]
    n = mp.matrix([1, rh])
    tau_hat = (n.T * M_prime(pp) * n)[0]                 # n^T M'(p) n, chart vector (unnormalised)
    return {"q": qq, "p": pp, "delta": dd, "rho": rh, "Mh22": Mh[1, 1], "Mh": Mh, "gh": gh, "kappa_hat": kh,
            "tau_hat": tau_hat, "tau_tilde": (tau_hat / dd) if dd != 0 else None,
            "kappa_unit": kh / (1 + rh ** 2) ** mp.mpf(1.5)}


def corner_limit(qc):
    """kappa_hat at the corner (q_c, q_c): divided differences become derivatives, rho_c = -M'12/M'22."""
    qc = mp.mpf(qc)
    Mp = M_prime(qc)
    rh = -Mp[0, 1] / Mp[1, 1]
    gd = {m: mp.diff(lambda t: g_num(t)[m], qc) for m in CHANNELS}
    kh = gd["uuu"] + 3 * rh * gd["uuv"] + 3 * rh ** 2 * gd["uvv"] + rh ** 3 * gd["vvv"]
    return {"q": qc, "rho": rh, "kappa_hat": kh, "det_M_prime": mp.det(Mp), "gd": gd,
            "tau_tilde": (mp.matrix([1, rh]).T * mp.matrix([[mp.diff(lambda t: M_num(t)[i, j], qc, 2) / 2
                                                              for j in range(2)] for i in range(2)])
                          * mp.matrix([1, rh]))[0]}


# Paper 2, Lemma T2 (FROZEN INPUT): q_c lies in this rational interval (40 decimals).
QC_LO = "2.0199382317007999883028831854985758749007"
QC_HI = "2.0199382317007999883028831854985758749008"
# Paper 2, Proposition (limits and corners) (ii): enclosure of P_T(0+) = P_T(0).
PT0_LO = "4.796368189344416004181122459356"
PT0_HI = "4.796368189344416004181122459357"


def scan(n=400):
    """Candidate scan of the carrier on q_k = k q_c / n, k = 0..n (the last point is the corner limit).
    Each row also records the conditioning of the curve (dD~/d delta at the curve, dP_T/dq) and of the chart."""
    qc = (mp.mpf(QC_LO) + mp.mpf(QC_HI)) / 2
    rows, prev = [], None
    for k in range(n + 1):
        qq = qc * k / n
        if k < n:
            c = carrier(qq)
            dD = mp.diff(lambda d: D_tilde(qq, d), c["delta"])
            row = {"q": qq, "delta": c["delta"], "p": c["p"], "rho": c["rho"], "Mh22": c["Mh22"],
                   "kappa_hat": c["kappa_hat"], "tau_hat": c["tau_hat"], "tau_tilde": c["tau_tilde"],
                   "dDtilde_ddelta": dD}
        else:
            c = corner_limit(qc)
            dD = mp.diff(lambda t: mp.det(M_prime(t)), qc) / 2      # Paper 2: d/d delta D~(q_c, 0) = (det M')'/2
            row = {"q": qc, "delta": mp.mpf(0), "p": qc, "rho": c["rho"], "Mh22": M_prime(qc)[1, 1],
                   "kappa_hat": c["kappa_hat"], "tau_hat": mp.mpf(0), "tau_tilde": c["tau_tilde"],
                   "dDtilde_ddelta": dD}
        if prev is not None:
            row["dP_dq"] = 1 + (row["delta"] - prev["delta"]) / (row["q"] - prev["q"])
        rows.append(row)
        prev = row
    return rows


# ---- route 3: direct numerical differentiation of the 24-D energy --------------------------------------------------
def kappa_direct(pp, qq, n_u, n_v):
    """D^3V[e_1, e_2, e_3] = d^3/da1 da2 da3 V(y* + sum a_k e_k) at 0, by mpmath.diff on the pair energy itself."""
    from .numeric import PairEnergy, y_star
    V = PairEnergy(pp, qq)
    y0 = y_star()
    s2 = mp.sqrt(2)
    E = []
    for k in range(3):
        w = [mp.mpf(c) for c in W_T2G[k]]
        u = [mp.mpf(c) for c in U_T2G[k]]
        E.append([-n_u * wc / 4 - n_v * s2 * uc / 4 for wc, uc in zip(w, u)])
    f = lambda x1, x2, x3: V.energy([y0[i] + x1 * E[0][i] + x2 * E[1][i] + x3 * E[2][i] for i in range(24)])
    return mp.diff(f, (0, 0, 0), (1, 1, 1))


def d3d_branch_point(qq, rel_mu, s_guess=None, dps=50):
    """VERIFIED-NUMERIC corroboration of the D3d branch (not used in any proof).

    Fix(D3d) in R^24 is span{e_br, sum_k uh_k, sum_k vh_k} (3-dimensional, computed in the tests). By symmetric
    criticality the D3d-symmetric equilibria near the cube are critical points of V restricted to it. With
    p = P_T(q)(1 + rel_mu), Newton in these three coordinates is started at the predicted branch point
    s*(mu) = -tau mu / kappa (unit n, chart gauge n_u > 0) and its converged amplitude s = <x - y*, sum e_k>/3
    is returned with the prediction."""
    from .numeric import PairEnergy, y_star
    old = mp.mp.dps
    mp.mp.dps = dps
    try:
        c = carrier(qq)
        q_, p0 = c["q"], c["p"]
        nrm = mp.sqrt(1 + c["rho"] ** 2)
        n_u, n_v = 1 / nrm, c["rho"] / nrm
        kap = q_ * W_num(q_) * c["delta"] * c["kappa_hat"] / nrm ** 3
        tau = q_ * W_num(q_) * c["tau_hat"] / nrm ** 2
        pp = p0 * (1 + mp.mpf(rel_mu))
        mu = pp - p0
        s_pred = -tau * mu / kap
        V = PairEnergy(pp, q_)
        y0 = y_star()
        s2 = mp.sqrt(2)
        su = [sum(-mp.mpf(W_T2G[k][i]) / 4 for k in range(3)) for i in range(24)]
        sv = [sum(-s2 * mp.mpf(U_T2G[k][i]) / 4 for k in range(3)) for i in range(24)]
        br = [mp.mpf(c_) / 2 for s in LABELS for c_ in s]
        nb = mp.sqrt(mp.fsum(x * x for x in br))
        B = [[x / nb for x in br], [x / mp.sqrt(3) for x in su], [x / mp.sqrt(3) for x in sv]]
        e_sum = [n_u * a + n_v * b for a, b in zip(su, sv)]
        s0 = s_pred if s_guess is None else mp.mpf(s_guess)
        cvec = mp.matrix([0, s0 * mp.sqrt(3) * n_u, s0 * mp.sqrt(3) * n_v])
        for _ in range(40):
            x = [y0[i] + sum(cvec[a] * B[a][i] for a in range(3)) for i in range(24)]
            g = V.gradient(x)
            H = V.hessian(x)
            gv = mp.matrix([mp.fsum(g[i] * B[a][i] for i in range(24)) for a in range(3)])
            Hm = mp.matrix(3, 3)
            for a in range(3):
                for b in range(3):
                    Hm[a, b] = mp.fsum(B[a][i] * H[i, j] * B[b][j] for i in range(24) for j in range(24)
                                       if B[a][i] != 0 and B[b][j] != 0)
            step = mp.lu_solve(Hm, gv)
            cvec -= step
            if mp.norm(step) < mp.mpf(10) ** (-(dps - 8)):
                break
        x = [y0[i] + sum(cvec[a] * B[a][i] for a in range(3)) for i in range(24)]
        s_found = mp.fsum((x[i] - y0[i]) * e_sum[i] for i in range(24)) / 3
        grad_norm = mp.sqrt(mp.fsum(gi * gi for gi in V.gradient(x)))
        return {"q": q_, "p": pp, "mu": mu, "kappa_unit": kap, "tau_unit": tau, "s_predicted": s_pred,
                "s_found": s_found, "breathing": cvec[0], "full_gradient_norm": grad_norm}
    finally:
        mp.mp.dps = old


def schur_reduced_eigenvalue(K, n0):
    """lambda_red = n0^T K n0 - (n0^T K m0)^2 / (m0^T K m0), m0 a unit vector orthogonal to the unit vector n0:
    the quadratic coefficient of the Lyapunov-Schmidt reduced potential on the T2g kernel (Schur complement)."""
    m0 = mp.matrix([-n0[1], n0[0]])
    knn = (n0.T * K * n0)[0]
    knm = (n0.T * K * m0)[0]
    kmm = (m0.T * K * m0)[0]
    return knn - knm ** 2 / kmm


assert Y_STAR.shape == (24, 1)
