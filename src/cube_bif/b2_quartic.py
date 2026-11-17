"""Phase B2.1: the quartic Lyapunov-Schmidt coefficient on the D2h axis of the critical T2g representation.

On p = P_T(q), with unit n in ker K and e_1 = n_u uh_1 + n_v vh_1 (unit in R^24),

    c4 = D^4V[e_1, e_1, e_1, e_1] - 3 <b, H_perp^{-1} b>,    b = D^3V[e_1, e_1, .],

so that the reduced potential on the axis is V_red(s) = V(y*) + c4 s^4/24 + O(s^6) at mu = 0.

Route 1 (symmetry-adapted, exact). B2.0 (b2_symmetry.py) shows b = b_A A_HAT + b_E E_HAT exactly, for every pair
potential, with A_HAT the unit A1g (breathing) vector and E_HAT the unit Eg vector fixed by the axis stabiliser. A1g
and Eg each occur once in R^24, so H acts on these lines by scalars h_A, h_E (checked: H A_HAT = h_A A_HAT and
H E_HAT = h_E E_HAT exactly). Hence

    c4 = Q(n) - 3 b_A(n)^2 / h_A - 3 b_E(n)^2 / h_E,
    Q(n) = sum_j C(4, j) n_u^(4-j) n_v^j Q_j,   b_X(n) = n_u^2 bX_uu + 2 n_u n_v bX_uv + n_v^2 bX_vv.

On the two-term family each of these 13 linear forms is a difference form q W_q [g(p) - g(q)] (closed forms below), so

    c4 = q W_q (p - q) c4_hat,   c4_hat = Q_hat - 3 bA_hat^2 / hA_hat - 3 bE_hat^2 / hE_hat   (divided differences).

Route 2 (raw 24-D). (a) Exact: the same linear forms by SymPy expansion of the composed pair energy along lines
(psi replaced by its quartic Taylor polynomial at each sigma), with no Faa di Bruno coefficients and no symmetry.
(b) Numeric: D^4V[e_1^4] and b by mpmath differentiation of the 24-D energy and gradient, the full 24x24 Hessian,
and a spectral pseudo-inverse over its nonzero eigenvalues (no kernel basis supplied, no symmetry reduction).

Route 3 (restricted D2h family). The four-parameter family of Sigma-symmetric configurations built from the vertex
orbits of Sigma (b2_symmetry.orbit_fields), its own energy function, its own curve point (det of the 4x4 restricted
Hessian = 0), its own kernel vector, and a nonlinear reduction: for each s the three transverse coordinates are solved
by Newton, and c4 = lim 24 V_red(s)/s^4 by Richardson extrapolation in s^2. No derivative tensor and no T2g basis.
"""
import itertools
from functools import lru_cache

import mpmath as mp
import sympy as sp

from . import b1_cubic as b1
from . import b2_symmetry as s2
from . import pairsum as ps
from .group import LABELS
from .modes import E_BR, U_T2G, W_T2G
from .t2g import UH, VH

S2 = sp.sqrt(2)
S3 = sp.sqrt(3)
S6 = sp.sqrt(6)
r, Xr, Yr = ps.r_, ps.X["r"], ps.Y["r"]
WR = 1 + Xr + Yr / 3
nu, nv = sp.symbols("n_u n_v")

Q_CHANNELS = ("uuuu", "uuuv", "uuvv", "uvvv", "vvvv")
Q_BINOM = {"uuuu": 1, "uuuv": 4, "uuvv": 6, "uvvv": 4, "vvvv": 1}
B_CHANNELS = ("uu", "uv", "vv")
B_WEIGHT = {"uu": 1, "uv": 2, "vv": 1}
FORM_NAMES = tuple(["Q_" + c for c in Q_CHANNELS] + ["bA_" + c for c in B_CHANNELS] + ["bE_" + c for c in B_CHANNELS]
                   + ["hA", "hE"])

_W1, _U1 = W_T2G[0], U_T2G[0]
_SU, _SV = sp.Rational(-1, 4), -S2 / 4


# ---- route 1: exact linear forms (any pair potential) ---------------------------------------------------------------
@lru_cache(maxsize=None)
def linear_forms():
    """The 13 linear forms in PSI: Q_j = D^4V[uh_1^(4-j), vh_1^j], bX_cc' = D^3V[c_1, c'_1, X_HAT], h_X."""
    out = {}
    for j, ch in enumerate(Q_CHANNELS):
        out["Q_" + ch] = sp.expand(ps.derivative([_W1] * (4 - j) + [_U1] * j) * _SU ** (4 - j) * _SV ** j)
    pairs = {"uu": (_W1, _W1, _SU * _SU), "uv": (_W1, _U1, _SU * _SV), "vv": (_U1, _U1, _SV * _SV)}
    for ch, (d0, d1, sc) in pairs.items():
        out["bA_" + ch] = sp.expand(ps.derivative([d0, d1, E_BR]) * sc / sp.sqrt(24))
        out["bE_" + ch] = sp.expand(ps.derivative([d0, d1, s2.E_TET_X]) * sc / sp.sqrt(48))
    out["hA"] = sp.expand(ps.derivative([E_BR, E_BR]) / 24)
    out["hE"] = sp.expand(ps.derivative([s2.E_TET_X, s2.E_TET_X]) / 48)
    return out


def Q_of_n(n_u=nu, n_v=nv, forms=None):
    f = linear_forms() if forms is None else forms
    return sp.expand(sum(Q_BINOM[c] * n_u ** c.count("u") * n_v ** c.count("v") * f["Q_" + c] for c in Q_CHANNELS))


def b_of_n(X, n_u=nu, n_v=nv, forms=None):
    f = linear_forms() if forms is None else forms
    return sp.expand(sum(B_WEIGHT[c] * n_u ** c.count("u") * n_v ** c.count("v") * f[X + "_" + c]
                         for c in B_CHANNELS))


def c4_generic(n_u=nu, n_v=nv, forms=None):
    """c4 = Q(n) - 3 b_A(n)^2/h_A - 3 b_E(n)^2/h_E for a generic pair potential (symbolic PSI); unit n assumed."""
    f = linear_forms() if forms is None else forms
    return Q_of_n(n_u, n_v, f) - 3 * b_of_n("bA", n_u, n_v, f) ** 2 / f["hA"] - 3 * b_of_n("bE", n_u, n_v, f) ** 2 / f["hE"]


# Closed forms g(r): at the equilibrium (A = t, B = 1) each form equals q W_q [g(p) - g(q)] (tested against
# pairsum.g_of). X = 2^(-r/2), Y = 3^(-r/2), W = 1 + X + Y/3. Note 3X + Y + 3 = 3W.
G4_CLOSED = {
    "Q_uuuu": (r + 2) * (162 * Xr * r ** 2 + 648 * Xr * r + 729 * Xr + 32 * Yr * r ** 2 + 32 * Yr * r - 168 * Yr + 972)
    / (648 * WR),
    "Q_uuuv": S2 * Yr * (r + 2) * (r + 4) * (2 * r + 3) / (81 * WR),
    "Q_uuvv": (r + 2) * (2 * Yr * r ** 2 + 11 * Yr * r + 21 * Yr + 81) / (81 * WR),
    "Q_uvvv": S2 * Yr * (r - 3) * (r + 2) * (r + 4) / (81 * WR),
    "Q_vvvv": (r + 2) * (Yr * r ** 2 - 8 * Yr * r - 21 * Yr + 81 * r ** 2 + 324 * r + 729) / (81 * WR),
    "bA_uu": -S6 * (r + 2) * (9 * Xr * r + 4 * Yr * r + 2 * Yr - 18) / (54 * WR),
    "bA_uv": -2 * S3 * Yr * (r + 2) ** 2 / (27 * WR),
    "bA_vv": -S6 * (Yr + 9) * (r - 1) * (r + 2) / (27 * WR),
    "bE_uu": S3 * (r + 2) * (18 * Xr * r + 27 * Xr - 16 * Yr - 36) / (108 * WR),
    "bE_uv": S6 * Yr * (r + 2) / (27 * WR),
    "bE_vv": -2 * S3 * (r + 2) * (9 * r + 18 - 2 * Yr) / (27 * WR),
    "hA": 2 * (r + 1),
    "hE": (2 * (r + 1) + (r - 2) * Xr / 2 - 2 * Yr / 3) / WR,
}


def closed_form_residual(name):
    """g_of(linear form) - G4_CLOSED[name] (zero identically; tested)."""
    return sp.simplify(ps.g_of(linear_forms()[name], "r") - G4_CLOSED[name])


def difference_form_residual(name):
    """Linear form at the equilibrium minus q W_q [g(p) - g(q)] (zero identically; tested)."""
    L = linear_forms()[name].subs(ps.two_term())
    g = G4_CLOSED[name]
    gp = g.subs({r: ps.p_, Xr: ps.X["p"], Yr: ps.Y["p"]}, simultaneous=True)
    gq = g.subs({r: ps.q_, Xr: ps.X["q"], Yr: ps.Y["q"]}, simultaneous=True)
    return sp.simplify(sp.together(L - ps.q_ * ps.W("q") * (gp - gq)))


def factorisation_identity():
    """With L = c d Lhat for every form (c = q W_q, d = p - q): Q - 3 bA^2/hA - 3 bE^2/hE = c d c4_hat (exact)."""
    c, d = sp.symbols("c d", positive=True)
    Qh, bAh, bEh, hAh, hEh = sp.symbols("Qh bAh bEh hAh hEh", nonzero=True)
    lhs = c * d * Qh - 3 * (c * d * bAh) ** 2 / (c * d * hAh) - 3 * (c * d * bEh) ** 2 / (c * d * hEh)
    rhs = c * d * (Qh - 3 * bAh ** 2 / hAh - 3 * bEh ** 2 / hEh)
    return sp.simplify(lhs - rhs)


# ---- Hessian on the fixed space (exact decomposition of H_perp on Fix) ------------------------------------------------
def hessian_on_fix():
    """H restricted to Fix(Sigma) in the orthonormal basis (A_HAT, E_HAT, uh_1, vh_1), generic pair potential."""
    H = ps.hessian()
    B = [s2.A_HAT, s2.E_HAT, UH[0], VH[0]]
    return sp.Matrix(4, 4, lambda i, j: sp.expand((B[i].T * H * B[j])[0, 0]))


# ---- route 2(a): exact raw line differentiation -------------------------------------------------------------------------
def _psi_taylor(sv, dsig):
    return sum(ps.PSI[(k, sv)] * dsig ** k / sp.factorial(k) for k in range(1, 5))


def raw_mixed_derivative(vectors, orders):
    """d^(k1+..+km)/dt1^k1..dtm^km  sum_pairs psi(|x_i - x_j|^2) at x = y* + sum t_i v_i, t = 0, by SymPy expansion
    of the composed function (psi -> quartic Taylor polynomial at sigma = |r_ij|^2; exact for total order <= 4)."""
    m = len(vectors)
    t = sp.symbols(f"t0:{m}")
    tot = 0
    mono = sp.Mul(*[t[i] ** orders[i] for i in range(m)])
    fact = sp.Mul(*[sp.factorial(k) for k in orders])
    for i, j in itertools.combinations(range(8), 2):
        rr = [sp.Rational(LABELS[i][c] - LABELS[j][c], 2) for c in range(3)]
        sv = int(sum(c * c for c in rr))
        x = [rr[c] + sum(t[a] * (vectors[a][3 * i + c] - vectors[a][3 * j + c]) for a in range(m)) for c in range(3)]
        dsig = sp.expand(sum(c * c for c in x) - sv)
        poly = sp.Poly(sp.expand(_psi_taylor(sv, dsig)), *t)
        tot += poly.coeff_monomial(mono)
    return sp.expand(tot * fact)


def raw_b_vector(n_u=nu, n_v=nv):
    e = s2.e1(n_u, n_v)
    comps = []
    for m in range(24):
        em = sp.zeros(24, 1)
        em[m] = 1
        comps.append(raw_mixed_derivative([e, em], [2, 1]))
    return sp.Matrix(comps)


def raw_quartic(n_u=nu, n_v=nv):
    return raw_mixed_derivative([s2.e1(n_u, n_v)], [4])


# ---- numeric layer ------------------------------------------------------------------------------------------------------
@lru_cache(maxsize=None)
def _lambdified():
    return {k: sp.lambdify((r, Xr, Yr), v, "mpmath") for k, v in G4_CLOSED.items()}


def g4_num(rr):
    rr = mp.mpf(rr)
    X_, Y_ = mp.power(2, -rr / 2), mp.power(3, -rr / 2)
    return {k: f(rr, X_, Y_) for k, f in _lambdified().items()}


def route1(qq, dd=None):
    """c4 on the curve from the closed forms: divided differences, chart n = (1, rho), unit normalisation."""
    c = b1.carrier(qq, dd)
    pp, q_, rho = c["p"], c["q"], c["rho"]
    gh = b1.divided(g4_num, pp, q_)
    Qh = sum(Q_BINOM[ch] * rho ** ch.count("v") * gh["Q_" + ch] for ch in Q_CHANNELS)
    bAh = sum(B_WEIGHT[ch] * rho ** ch.count("v") * gh["bA_" + ch] for ch in B_CHANNELS)
    bEh = sum(B_WEIGHT[ch] * rho ** ch.count("v") * gh["bE_" + ch] for ch in B_CHANNELS)
    hAh, hEh = gh["hA"], gh["hE"]
    c4h_chart = Qh - 3 * bAh ** 2 / hAh - 3 * bEh ** 2 / hEh
    nrm2 = 1 + rho ** 2
    pref = q_ * b1.W_num(q_) * c["delta"]
    return {"q": q_, "p": pp, "delta": c["delta"], "rho": rho, "n": (1 / mp.sqrt(nrm2), rho / mp.sqrt(nrm2)),
            "Q_hat": Qh / nrm2 ** 2, "bA_hat": bAh / nrm2, "bE_hat": bEh / nrm2, "hA_hat": hAh, "hE_hat": hEh,
            "quartic_term_hat": Qh / nrm2 ** 2,
            "backreaction_A1g_hat": -3 * bAh ** 2 / hAh / nrm2 ** 2,
            "backreaction_Eg_hat": -3 * bEh ** 2 / hEh / nrm2 ** 2,
            "c4_hat": c4h_chart / nrm2 ** 2, "c4_hat_chart": c4h_chart, "prefactor_qWq_delta": pref,
            "c4": pref * c4h_chart / nrm2 ** 2,
            "D4V": pref * Qh / nrm2 ** 2, "b_A": pref * bAh / nrm2, "b_E": pref * bEh / nrm2,
            "h_A": pref * hAh, "h_E": pref * hEh}


def _e1_numeric(n_u, n_v):
    """e_1 = n_u uh_1 + n_v vh_1 in mpmath, from the integer fields: uh_1 = -W_1/4, vh_1 = -(sqrt2/4) U_1."""
    s2_ = mp.sqrt(2)
    return [-n_u * mp.mpf(int(w)) / 4 - n_v * s2_ * mp.mpf(int(u)) / 4 for w, u in zip(_W1, _U1)]


def route2_numeric(qq, dd=None):
    """Raw 24-D: D^4V[e^4], b = D^3V[e, e, .] by mpmath differentiation of the energy and of its analytic gradient,
    the full 24x24 Hessian, and w = H^+ b by the spectral pseudo-inverse over |eigenvalue| > 10^(-dps/2)."""
    from .numeric import PairEnergy, shift, y_star
    c = b1.carrier(qq, dd)
    pp, q_, rho = c["p"], c["q"], c["rho"]
    nrm = mp.sqrt(1 + rho ** 2)
    n_u, n_v = 1 / nrm, rho / nrm
    e = _e1_numeric(n_u, n_v)
    V = PairEnergy(pp, q_)
    y0 = y_star()
    V4 = mp.diff(lambda a: V.energy(shift(y0, (a, e))), 0, 4)
    b = [mp.diff(lambda a, i=i: V.gradient(shift(y0, (a, e)))[i], 0, 2) for i in range(24)]
    H = V.hessian(y0)
    E, U = mp.eigsy(H)
    tol = mp.mpf(10) ** (-(mp.mp.dps // 2))
    small = [k for k in range(24) if abs(E[k]) < tol]
    big = [k for k in range(24) if abs(E[k]) >= tol]
    proj = [mp.fsum(U[i, k] * b[i] for i in range(24)) for k in range(24)]
    bHb = mp.fsum(proj[k] ** 2 / E[k] for k in big)
    He = [mp.fsum(H[i, j] * e[j] for j in range(24)) for i in range(24)]
    return {"q": q_, "p": pp, "D4V": V4, "b": b, "bHinvb": bHb, "c4": V4 - 3 * bHb,
            "n_small_eigenvalues": len(small), "max_small_eigenvalue": max(abs(E[k]) for k in small),
            "min_nonzero_eigenvalue": min(abs(E[k]) for k in big),
            "max_b_component_on_small_eigenvectors": max(abs(proj[k]) for k in small),
            "He_residual": mp.sqrt(mp.fsum(x * x for x in He)),
            "b_norm": mp.sqrt(mp.fsum(x * x for x in b))}


# ---- route 3: restricted D2h family -------------------------------------------------------------------------------------
class RestrictedFamily:
    """x(theta) = y* + sum theta_i F_i over the four orbit fields of Sigma; its own pair energy."""

    def __init__(self, pp, qq):
        self.p, self.q = mp.mpf(pp), mp.mpf(qq)
        W = lambda e: 1 + mp.power(2, -e / 2) + mp.power(3, -e / 2) / 3
        self.A = self.q * W(self.q) / (self.p * W(self.p))
        self.y0 = [mp.mpf(c) / 2 for s in LABELS for c in s]
        flds = s2.orbit_fields()
        self.names = list(s2.ORBIT_DIRS)
        self.F = [[mp.mpf(int(c)) for c in flds[k]] for k in self.names]
        self.G = mp.matrix(4, 4)
        for a in range(4):
            for b_ in range(4):
                self.G[a, b_] = mp.fsum(x * y for x, y in zip(self.F[a], self.F[b_]))

    def energy_theta(self, th):
        x = [self.y0[i] + mp.fsum(th[a] * self.F[a][i] for a in range(4)) for i in range(24)]
        tot = mp.mpf(0)
        for i, j in itertools.combinations(range(8), 2):
            d2 = mp.fsum((x[3 * i + c] - x[3 * j + c]) ** 2 for c in range(3))
            rr = mp.sqrt(d2)
            tot += self.A * rr ** (-self.p) - rr ** (-self.q)
        return tot

    def hessian_theta(self):
        f = lambda *th: self.energy_theta(th)
        H = mp.matrix(4, 4)
        for a in range(4):
            for b_ in range(a, 4):
                orders = [0] * 4
                orders[a] += 1
                orders[b_] += 1
                H[a, b_] = H[b_, a] = mp.diff(f, (0, 0, 0, 0), tuple(orders))
        return H

    def normal_modes(self):
        """Eigen-decomposition of the restricted Hessian in the R^24 metric: eigenvalues and theta-vectors c with
        c^T G c = 1 (unit displacements in R^24)."""
        H = self.hessian_theta()
        Linv = mp.matrix(4, 4)
        for a in range(4):
            Linv[a, a] = 1 / mp.sqrt(self.G[a, a])
        assert all(self.G[a, b_] == 0 for a in range(4) for b_ in range(4) if a != b_)
        E, U = mp.eigsy(Linv * H * Linv)
        vecs = [Linv * mp.matrix([U[i, k] for i in range(4)]) for k in range(4)]
        return E, vecs

    def to_R24(self, th):
        return [mp.fsum(th[a] * self.F[a][i] for a in range(4)) for i in range(24)]


def route3_curve_point(qq, p_guess):
    """p > q with det(restricted 4x4 Hessian) = 0, by the secant method from p_guess."""
    f = lambda pp: mp.det(RestrictedFamily(pp, qq).hessian_theta())
    return mp.findroot(f, mp.mpf(p_guess), solver="secant", tol=mp.mpf(10) ** (-(mp.mp.dps - 12)))


def route3(qq, s0="1e-3", levels=5, p_guess=None):
    """c4 = lim 24 V_red(s)/s^4 in the restricted family, by Newton in the three transverse modes and Richardson
    extrapolation in s^2 (V_red is even in s: b2_symmetry.reversing_elements)."""
    qq = mp.mpf(qq)
    if p_guess is None:
        p_guess = b1.carrier(qq)["p"]
    pp = route3_curve_point(qq, p_guess)
    fam = RestrictedFamily(pp, qq)
    E, vecs = fam.normal_modes()
    k0 = min(range(4), key=lambda k: abs(E[k]))
    others = [k for k in range(4) if k != k0]
    kvec = vecs[k0]
    C = [vecs[k] for k in others]
    E0 = fam.energy_theta([0, 0, 0, 0])

    def theta(s, y):
        return [s * kvec[a] + mp.fsum(y[j] * C[j][a] for j in range(3)) for a in range(4)]

    def F(s, y):
        return fam.energy_theta(theta(s, y))

    def solve(s):
        y = [mp.mpf(0)] * 3
        tol = mp.mpf(10) ** (-(mp.mp.dps - 10))
        for _ in range(30):
            fy = lambda y0_, y1_, y2_: F(s, [y0_, y1_, y2_])
            g = mp.matrix([mp.diff(fy, tuple(y), tuple(1 if j == m else 0 for j in range(3))) for m in range(3)])
            Hm = mp.matrix(3, 3)
            for a in range(3):
                for b_ in range(a, 3):
                    o = [0, 0, 0]
                    o[a] += 1
                    o[b_] += 1
                    Hm[a, b_] = Hm[b_, a] = mp.diff(fy, tuple(y), tuple(o))
            step = mp.lu_solve(Hm, g)
            y = [y[j] - step[j] for j in range(3)]
            if mp.norm(step) < tol * (1 + mp.norm(mp.matrix(y))):
                break
        return y, F(s, y) - E0

    s0 = mp.mpf(s0)
    svals = [s0 / 2 ** j for j in range(levels)]
    Rv, ys = [], []
    for s in svals:
        y, vr = solve(s)
        ys.append(y)
        Rv.append(24 * vr / s ** 4)
    T = [[x] for x in Rv]
    for j in range(1, levels):
        for k in range(1, j + 1):
            T[j].append((4 ** k * T[j][k - 1] - T[j - 1][k - 1]) / (4 ** k - 1))
    c4 = T[-1][-1]
    err = abs(T[-1][-1] - T[-1][-2]) if levels > 1 else mp.inf
    # evenness check at the largest s
    _, vr_neg = solve(-svals[0])
    kR24 = fam.to_R24(kvec)
    return {"q": qq, "p": pp, "eigenvalues": [E[k] for k in range(4)], "kernel_index": k0,
            "kernel_eigenvalue": E[k0], "nonzero_eigenvalues": sorted(E[k] for k in others),
            "kernel_vector_R24": kR24, "c4": c4, "richardson_error": err, "R_values": Rv,
            "transverse_at_s0": ys[0], "evenness_defect": abs(vr_neg * 24 / svals[0] ** 4 - Rv[0])}
