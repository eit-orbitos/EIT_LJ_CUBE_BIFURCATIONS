"""Phase B2.2: the normalised D2h quartic carrier c4_hat on the closed physical T2g curve (VERIFIED-NUMERIC /
RECONNAISSANCE; the exact identities are marked as such in NOTES §7).

B2.1 (exact): c4 = q W_q (p - q) c4_hat and, in the chart n ~ (1, rho), rho = -Mh12/Mh22,

    c4_hat = [Q_hat(1, rho) - (3/2) bA_hat(1, rho)^2 - 3 bE_hat(1, rho)^2 / hE_hat] / (1 + rho^2)^2,

with f_hat = (f(p) - f(q))/(p - q) for the 13 closed forms of b2_quartic.G4_CLOSED (hA_hat = 2 exactly).

Endpoint q = 0. The same formula at q = 0 itself: f_hat = (f(p0) - f(0))/p0 with the exact values f(0) (X = Y = 1,
W = 7/3), M_hat = (M(p0) - M(0))/p0 with the exact M(0), and p0 = P_T(0) refined by root finding inside Paper 2's
certified enclosure.

Corner (q_c, q_c). Every divided difference becomes the diagonal derivative f'(q_c), computed from exact derivative
closed forms (dX/dr = -(log2/2) X, dY/dr = -(log3/2) Y); the chart is B1's rho_c = -M'12/M'22. Nothing divides by
p - q. q_c is refined by root finding on det M'(r) inside Paper 2's certified enclosure.

Scan: q_k = k q_c/400, k = 0..400, with the two endpoint formulations at k = 0 and k = 400.

Independent route (does not use the closed forms, divided differences, Paper 2's M(r) or B1's curve code):
- a general pair energy, gradient and Hessian in R^24 for a potential phi given in closed form;
- its own curve point: det of the 4x4 Hessian restricted to the D2h fixed space (b2_symmetry.orbit_fields) = 0;
- its own critical vector: the kernel of that 4x4 Hessian, mapped to R^24;
- raw 24-D quartic and back-reaction: D^4V[e^4] and b = D^3V[e, e, .] by mpmath differentiation, the full Hessian
  and a spectral pseudo-inverse;
- the factor q W_q (p - q) removed analytically: in the interior the potential is divided by it; at the endpoints the
  limit potentials are used,
      q -> 0:  phi/q -> phi_0(r) = 7/(3 p W_p) r^-p + log r   (up to a constant),   c4(phi_0) = (7/3) p0 c4_hat(0);
      corner:  phi/(p - q) -> phi_c(r) = -(1/q + W'_q/W_q + log r) r^-q,          c4(phi_c) = q_c W_qc c4_hat(q_c),
  and at q = 0 the curve point p0 (resp. at the corner q_c) is found from phi_0 (resp. phi_c) alone.
"""
import itertools
from functools import lru_cache

import mpmath as mp
import sympy as sp

from . import b1_cubic as b1
from . import b2_quartic as b2
from . import b2_symmetry as s2
from . import pairsum as ps
from .group import LABELS
from .t2g import M_num, M_paper2

r, Xr, Yr = ps.r_, ps.X["r"], ps.Y["r"]
L2, L3 = sp.log(2), sp.log(3)
NAMES = b2.FORM_NAMES

# Frozen Paper 2 enclosures (FROZEN INPUT), as used in B1.
QC_LO, QC_HI = b1.QC_LO, b1.QC_HI
PT0_LO, PT0_HI = b1.PT0_LO, b1.PT0_HI
# The independent MPFR enclosure of P_T(0+) from Paper 2's own blind audit (audits/theorem4prime_v0.1, read-only).
PT0_AUDIT_LO = "4.796368189344416004181122459356264828727186725514416637"
PT0_AUDIT_HI = "4.79636818934441600418112245935626483643090650306336005"


# ---- exact layer --------------------------------------------------------------------------------------------------
def d_dr(expr):
    """d/dr of an expression in r, X = 2^(-r/2), Y = 3^(-r/2)."""
    return sp.diff(expr, r) + sp.diff(expr, Xr) * (-L2 / 2 * Xr) + sp.diff(expr, Yr) * (-L3 / 2 * Yr)


@lru_cache(maxsize=None)
def g_prime_closed():
    """Exact derivative closed forms g'(r) of the 13 B2.1 forms (functions of r, X, Y, log2, log3)."""
    return {k: sp.together(sp.expand(d_dr(v))) for k, v in b2.G4_CLOSED.items()}


@lru_cache(maxsize=None)
def M_prime_closed():
    M = M_paper2(r, Xr, Yr)
    return M.applyfunc(lambda e: sp.together(sp.expand(d_dr(e))))


@lru_cache(maxsize=None)
def g_at_zero():
    """Exact values g(0) (X = Y = 1, W = 7/3)."""
    return {k: sp.nsimplify(sp.radsimp(sp.simplify(v.subs({r: 0, Xr: 1, Yr: 1})))) for k, v in b2.G4_CLOSED.items()}


@lru_cache(maxsize=None)
def M_at_zero():
    return sp.simplify(M_paper2(sp.Integer(0), sp.Integer(1), sp.Integer(1)))


def chart_carrier_symbolic(G, rho):
    """Assemble the unit-n carrier and its three contributions from per-form values G (any of: divided differences,
    derivatives) and the chart rho. Shared by the q = 0 and corner formulations (symbolic or numeric)."""
    Qh = sum(b2.Q_BINOM[c] * rho ** c.count("v") * G["Q_" + c] for c in b2.Q_CHANNELS)
    bAh = sum(b2.B_WEIGHT[c] * rho ** c.count("v") * G["bA_" + c] for c in b2.B_CHANNELS)
    bEh = sum(b2.B_WEIGHT[c] * rho ** c.count("v") * G["bE_" + c] for c in b2.B_CHANNELS)
    nrm2 = 1 + rho ** 2
    out = {"Q": Qh / nrm2 ** 2, "A1g": -3 * bAh ** 2 / G["hA"] / nrm2 ** 2,
           "Eg": -3 * bEh ** 2 / G["hE"] / nrm2 ** 2, "bA_chart": bAh, "bE_chart": bEh, "Q_chart": Qh,
           "hE": G["hE"], "hA": G["hA"], "rho": rho, "one_plus_rho2": nrm2}
    out["c4_hat"] = out["Q"] + out["A1g"] + out["Eg"]
    return out


@lru_cache(maxsize=None)
def corner_symbolic():
    """The corner carrier as an explicit function of r (derivatives only). Returns the expression, its free symbols and
    the denominators it can have: W (inside every g'), M'22 (chart), g_hE' and 1 + rho_c^2."""
    gp = g_prime_closed()
    Mp = M_prime_closed()
    rho = -Mp[0, 1] / Mp[1, 1]
    parts = chart_carrier_symbolic(gp, rho)
    return {"c4_hat": parts["c4_hat"], "rho": rho, "free_symbols": parts["c4_hat"].free_symbols,
            "denominators": {"W": 1 + Xr + Yr / 3, "M'22": Mp[1, 1], "g_hE'": gp["hE"], "1+rho^2": 1 + rho ** 2}}


# ---- numeric layer -------------------------------------------------------------------------------------------------
@lru_cache(maxsize=None)
def _lambdified():
    gp = {k: sp.lambdify((r, Xr, Yr), v, "mpmath") for k, v in g_prime_closed().items()}
    Mp = [[sp.lambdify((r, Xr, Yr), M_prime_closed()[i, j], "mpmath") for j in range(2)] for i in range(2)]
    g0 = {k: sp.lambdify((), v, "mpmath") for k, v in g_at_zero().items()}
    M0 = [[sp.lambdify((), M_at_zero()[i, j], "mpmath") for j in range(2)] for i in range(2)]
    return gp, Mp, g0, M0


def _xy(rr):
    rr = mp.mpf(rr)
    return rr, mp.power(2, -rr / 2), mp.power(3, -rr / 2)


def g_prime_num(rr):
    gp = _lambdified()[0]
    a = _xy(rr)
    return {k: f(*a) for k, f in gp.items()}


def M_prime_num(rr):
    Mp = _lambdified()[1]
    a = _xy(rr)
    return mp.matrix([[Mp[i][j](*a) for j in range(2)] for i in range(2)])


def g_zero_num():
    return {k: f() for k, f in _lambdified()[2].items()}


def M_zero_num():
    M0 = _lambdified()[3]
    return mp.matrix([[M0[i][j]() for j in range(2)] for i in range(2)])


def refine_qc(dps=80):
    """q_c: the zero of det M'(r) inside Paper 2's certified enclosure (FROZEN INPUT, Lemma T2), refined."""
    with mp.workdps(dps):
        lo, hi = mp.mpf(QC_LO), mp.mpf(QC_HI)
        f = lambda t: mp.det(M_prime_num(t))
        if not (f(lo) > 0 > f(hi)):
            raise ArithmeticError("det M' does not change sign across the frozen q_c enclosure")
        qc = mp.findroot(f, (lo, hi), solver="anderson")
        if not lo <= qc <= hi:
            raise ArithmeticError("refined q_c left the frozen enclosure")
        return +qc


def refine_p0(dps=80):
    """p0 = P_T(0): the zero of D~(0, p) = det[(M(p) - M(0))/p] inside Paper 2's certified enclosure, refined."""
    with mp.workdps(dps):
        lo, hi = mp.mpf(PT0_LO), mp.mpf(PT0_HI)
        M0 = M_zero_num()
        f = lambda p: mp.det((M_num(p) - M0) / p)
        if not (f(lo) > 0 > f(hi)):
            raise ArithmeticError("D~(0, .) does not change sign across the frozen P_T(0) enclosure")
        p0 = mp.findroot(f, (lo, hi), solver="anderson")
        if not lo <= p0 <= hi:
            raise ArithmeticError("refined p0 left the frozen enclosure")
        return +p0


def endpoint_q0(p0=None):
    """The carrier at q = 0 from its own formulation: f_hat = (f(p0) - f(0))/p0 with exact f(0)."""
    p0 = refine_p0(mp.mp.dps + 20) if p0 is None else mp.mpf(p0)
    gp, g0 = b2.g4_num(p0), g_zero_num()
    G = {k: (gp[k] - g0[k]) / p0 for k in NAMES}
    Mh = (M_num(p0) - M_zero_num()) / p0
    rho = -Mh[0, 1] / Mh[1, 1]
    out = chart_carrier_symbolic(G, rho)
    out.update({"q": mp.mpf(0), "p": p0, "delta": p0, "Mh22": Mh[1, 1], "Mh": Mh, "det_Mh": mp.det(Mh),
                "kernel_residual": mp.norm(Mh * mp.matrix([1, rho]))})
    return out


def corner(qc=None):
    """The carrier at the corner (q_c, q_c): derivatives f'(q_c) and the chart rho_c = -M'12/M'22."""
    qc = refine_qc(mp.mp.dps + 20) if qc is None else mp.mpf(qc)
    G = g_prime_num(qc)
    Mp = M_prime_num(qc)
    rho = -Mp[0, 1] / Mp[1, 1]
    out = chart_carrier_symbolic(G, rho)
    out.update({"q": qc, "p": qc, "delta": mp.mpf(0), "Mh22": Mp[1, 1], "Mh": Mp, "det_Mh": mp.det(Mp),
                "kernel_residual": mp.norm(Mp * mp.matrix([1, rho]))})
    return out


def interior(qq, dd=None):
    """The carrier at 0 < q < q_c by the B2.1 divided-difference formulation (b2_quartic.route1), with the curve and
    chart diagnostics of B1 (b1_cubic.carrier)."""
    c = b1.carrier(qq, dd)
    r1 = b2.route1(c["q"], dd=c["delta"])
    nrm2 = 1 + c["rho"] ** 2
    return {"q": c["q"], "p": c["p"], "delta": c["delta"], "rho": c["rho"], "Mh22": c["Mh22"], "Mh": c["Mh"],
            "det_Mh": mp.det(c["Mh"]), "kernel_residual": mp.norm(c["Mh"] * mp.matrix([1, c["rho"]])),
            "Q": r1["Q_hat"], "A1g": r1["backreaction_A1g_hat"], "Eg": r1["backreaction_Eg_hat"],
            "c4_hat": r1["c4_hat"], "hE": r1["hE_hat"], "hA": r1["hA_hat"], "one_plus_rho2": nrm2,
            "Q_chart": r1["Q_hat"] * nrm2 ** 2, "bA_chart": r1["bA_hat"] * nrm2, "bE_chart": r1["bE_hat"] * nrm2}


def curve_slope(qq, delta):
    """dD~/d delta at the curve (curve conditioning), and at the corner Paper 2's (det M')'/2."""
    if delta == 0:
        return mp.diff(lambda t: mp.det(M_prime_num(t)), qq) / 2
    if qq == 0:
        M0 = M_zero_num()
        return mp.diff(lambda d: mp.det((M_num(d) - M0) / d), delta)
    return mp.diff(lambda d: b1.D_tilde(qq, d), delta)


def scan(n=400, qc=None, p0=None):
    """Rows on q_k = k q_c/n, k = 0..n: the q = 0 formulation at k = 0, the corner formulation at k = n."""
    qc = refine_qc(mp.mp.dps + 20) if qc is None else mp.mpf(qc)
    p0 = refine_p0(mp.mp.dps + 20) if p0 is None else mp.mpf(p0)
    rows = []
    for k in range(n + 1):
        if k == 0:
            row = endpoint_q0(p0)
            row["formulation"] = "endpoint q = 0"
        elif k == n:
            row = corner(qc)
            row["formulation"] = "corner (derivatives)"
        else:
            row = interior(qc * k / n)
            row["formulation"] = "divided differences"
        row["dDtilde_ddelta"] = curve_slope(row["q"], row["delta"])
        rows.append(row)
    for i in range(1, len(rows)):
        rows[i]["dP_dq"] = 1 + (rows[i]["delta"] - rows[i - 1]["delta"]) / (rows[i]["q"] - rows[i - 1]["q"])
    return rows


def scan_summary(rows):
    c = [x["c4_hat"] for x in rows]
    diffs = [c[i + 1] - c[i] for i in range(len(c) - 1)]
    sign_changes = sum(1 for i in range(len(c) - 1) if (c[i] > 0) != (c[i + 1] > 0))
    turns = [i + 1 for i in range(len(diffs) - 1) if (diffs[i] > 0) != (diffs[i + 1] > 0)]
    kmin = min(range(len(c)), key=lambda i: c[i])
    kmax = max(range(len(c)), key=lambda i: c[i])
    kabs = min(range(len(c)), key=lambda i: abs(c[i]))
    mins = {}
    for key in ("hE", "Mh22", "one_plus_rho2"):
        k = min(range(len(rows)), key=lambda i: abs(rows[i][key]))
        mins[key] = (abs(rows[k][key]), rows[k]["q"])
    kd = min(range(len(rows)), key=lambda i: abs(rows[i]["dDtilde_ddelta"]))
    mins["dDtilde_ddelta"] = (abs(rows[kd]["dDtilde_ddelta"]), rows[kd]["q"])
    return {"n_points": len(rows), "min": (c[kmin], rows[kmin]["q"], kmin), "max": (c[kmax], rows[kmax]["q"], kmax),
            "smallest_abs": (abs(c[kabs]), rows[kabs]["q"], kabs), "sign_changes": sign_changes,
            "all_positive": all(x > 0 for x in c), "all_negative": all(x < 0 for x in c),
            "strictly_increasing_on_grid": all(d > 0 for d in diffs),
            "strictly_decreasing_on_grid": all(d < 0 for d in diffs),
            "grid_turning_points": turns, "min_increment": min(diffs), "max_increment": max(diffs),
            "denominator_minima": mins,
            "max_kernel_residual": max(x["kernel_residual"] for x in rows),
            "contribution_ranges": {k: (min(x[k] for x in rows), max(x[k] for x in rows)) for k in ("Q", "A1g", "Eg")}}


# ---- independent route ------------------------------------------------------------------------------------------------
def _W(e):
    return 1 + mp.power(2, -e / 2) + mp.power(3, -e / 2) / 3


def _dW(e):
    return -mp.log(2) / 2 * mp.power(2, -e / 2) - mp.log(3) / 2 * mp.power(3, -e / 2) / 3


class Potential:
    """phi(r) in closed form, with phi' and phi''. Kinds:
    two_term(p, q):  (A r^-p - r^-q) / (q W_q (p - q)),  A = q W_q/(p W_p)   [the factor removed analytically]
    q0(p):           7/(3 p W_p) r^-p + log r                                [lim phi/q, up to a constant]
    corner(q):       -(1/q + W'_q/W_q + log r) r^-q                          [lim phi/(p - q) at p = q]"""

    def __init__(self, kind, p=None, q=None):
        self.kind = kind
        if kind == "two_term":
            self.p, self.q = mp.mpf(p), mp.mpf(q)
            self.A = self.q * _W(self.q) / (self.p * _W(self.p))
            self.s = self.q * _W(self.q) * (self.p - self.q)
        elif kind == "q0":
            self.p = mp.mpf(p)
            self.c = mp.mpf(7) / (3 * self.p * _W(self.p))
        elif kind == "corner":
            self.q = mp.mpf(q)
            self.k = 1 / self.q + _dW(self.q) / _W(self.q)
        else:
            raise ValueError(kind)

    def phi(self, x):
        if self.kind == "two_term":
            return (self.A * x ** (-self.p) - x ** (-self.q)) / self.s
        if self.kind == "q0":
            return self.c * x ** (-self.p) + mp.log(x)
        return -(self.k + mp.log(x)) * x ** (-self.q)

    def dphi(self, x):
        if self.kind == "two_term":
            return (-self.p * self.A * x ** (-self.p - 1) + self.q * x ** (-self.q - 1)) / self.s
        if self.kind == "q0":
            return -self.c * self.p * x ** (-self.p - 1) + 1 / x
        return x ** (-self.q - 1) * (self.q * (self.k + mp.log(x)) - 1)

    def d2phi(self, x):
        if self.kind == "two_term":
            return (self.p * (self.p + 1) * self.A * x ** (-self.p - 2)
                    - self.q * (self.q + 1) * x ** (-self.q - 2)) / self.s
        if self.kind == "q0":
            return self.c * self.p * (self.p + 1) * x ** (-self.p - 2) - 1 / x ** 2
        return x ** (-self.q - 2) * ((2 * self.q + 1) - self.q * (self.q + 1) * (self.k + mp.log(x)))

    def normaliser(self, p_or_q):
        """c4(phi) / c4_hat at the curve point: 1 (interior), (7/3) p0 (q = 0), q_c W_qc (corner)."""
        if self.kind == "two_term":
            return mp.mpf(1)
        if self.kind == "q0":
            return mp.mpf(7) / 3 * mp.mpf(p_or_q)
        return mp.mpf(p_or_q) * _W(mp.mpf(p_or_q))


_PAIRS = list(itertools.combinations(range(8), 2))


class GeneralPairEnergy:
    """V(x) = sum phi(|x_i - x_j|) in R^24 for a Potential; analytic gradient and Hessian."""

    def __init__(self, pot):
        self.pot = pot

    def energy(self, xv):
        tot = mp.mpf(0)
        for i, j in _PAIRS:
            tot += self.pot.phi(mp.sqrt(mp.fsum((xv[3 * i + c] - xv[3 * j + c]) ** 2 for c in range(3))))
        return tot

    def gradient(self, xv):
        g = [mp.mpf(0)] * 24
        for i, j in _PAIRS:
            d = [xv[3 * i + c] - xv[3 * j + c] for c in range(3)]
            rr = mp.sqrt(mp.fsum(c * c for c in d))
            f = self.pot.dphi(rr) / rr
            for c in range(3):
                g[3 * i + c] += f * d[c]
                g[3 * j + c] -= f * d[c]
        return g

    def hessian(self, xv):
        H = mp.zeros(24, 24)
        for i, j in _PAIRS:
            d = [xv[3 * i + c] - xv[3 * j + c] for c in range(3)]
            rr = mp.sqrt(mp.fsum(c * c for c in d))
            e = [c / rr for c in d]
            d1, d2 = self.pot.dphi(rr), self.pot.d2phi(rr)
            for a in range(3):
                for b_ in range(3):
                    blk = d2 * e[a] * e[b_] + d1 / rr * ((1 if a == b_ else 0) - e[a] * e[b_])
                    H[3 * i + a, 3 * i + b_] += blk
                    H[3 * j + a, 3 * j + b_] += blk
                    H[3 * i + a, 3 * j + b_] -= blk
                    H[3 * j + a, 3 * i + b_] -= blk
        return H


class LimitFamily(b2.RestrictedFamily):
    """The four-parameter D2h family of B2.1 (orbit fields of the stabiliser), with a general Potential."""

    def __init__(self, pot):          # the parent constructor is not called: it builds the two-term potential
        self.pot = pot
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
        return GeneralPairEnergy(self.pot).energy(x)


def make_potential(kind, value, q=None):
    if kind == "two_term":
        return Potential("two_term", p=value, q=q)
    if kind == "q0":
        return Potential("q0", p=value)
    return Potential("corner", q=value)


def own_curve_point(kind, guess, q=None):
    """The free parameter (p for two_term and q0, q for corner) at which the restricted 4x4 Hessian is singular."""
    f = lambda v: mp.det(LimitFamily(make_potential(kind, v, q)).hessian_theta())
    return mp.findroot(f, mp.mpf(guess), solver="secant")


def raw24_c4(pot, e):
    """c4 = D^4V[e^4] - 3 <b, H^+ b> for the Potential, raw in R^24 (spectral pseudo-inverse)."""
    V = GeneralPairEnergy(pot)
    y0 = [mp.mpf(c) / 2 for s in LABELS for c in s]
    line = lambda a: [y + a * ei for y, ei in zip(y0, e)]
    V4 = mp.diff(lambda a: V.energy(line(a)), 0, 4)
    b = [mp.diff(lambda a, i=i: V.gradient(line(a))[i], 0, 2) for i in range(24)]
    H = V.hessian(y0)
    E, U = mp.eigsy(H)
    tol = mp.mpf(10) ** (-(mp.mp.dps // 2))
    small = [k for k in range(24) if abs(E[k]) < tol]
    big = [k for k in range(24) if abs(E[k]) >= tol]
    proj = [mp.fsum(U[i, k] * b[i] for i in range(24)) for k in range(24)]
    bHb = mp.fsum(proj[k] ** 2 / E[k] for k in big)
    grad0 = mp.sqrt(mp.fsum(x * x for x in V.gradient(y0)))
    return {"D4V": V4, "bHinvb": bHb, "c4": V4 - 3 * bHb, "n_small": len(small),
            "max_small": max(abs(E[k]) for k in small) if small else None,
            "min_nonzero": min(abs(E[k]) for k in big),
            "b_on_small": max(abs(proj[k]) for k in small) if small else None, "equilibrium_gradient": grad0}


def independent(kind, guess, q=None):
    """Independent carrier value: own curve point, own kernel vector, raw 24-D c4 of the normalised potential."""
    v = own_curve_point(kind, guess, q)
    pot = make_potential(kind, v, q)
    fam = LimitFamily(pot)
    E, vecs = fam.normal_modes()
    k0 = min(range(4), key=lambda k: abs(E[k]))
    e = fam.to_R24(vecs[k0])
    res = raw24_c4(pot, e)
    norm = pot.normaliser(v)
    res.update({"kind": kind, "curve_parameter": v, "restricted_eigenvalues": [E[k] for k in range(4)],
                "c4_hat": res["c4"] / norm, "normaliser": norm, "kernel_vector": e})
    return res


def independent_nonlinear(kind, guess, q=None, s0="1e-3", levels=5):
    """Endpoint-safe nonlinear check: Newton in the three transverse restricted modes and Richardson extrapolation of
    24 V_red(s)/s^4 for the normalised (limit) potential; own curve point and kernel."""
    v = own_curve_point(kind, guess, q)
    pot = make_potential(kind, v, q)
    fam = LimitFamily(pot)
    E, vecs = fam.normal_modes()
    k0 = min(range(4), key=lambda k: abs(E[k]))
    kvec = vecs[k0]
    C = [vecs[k] for k in range(4) if k != k0]
    E0 = fam.energy_theta([0, 0, 0, 0])

    def F(s, y):
        return fam.energy_theta([s * kvec[a] + mp.fsum(y[j] * C[j][a] for j in range(3)) for a in range(4)])

    def vred(s):
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
        return F(s, y) - E0

    s0 = mp.mpf(s0)
    R = [24 * vred(s0 / 2 ** j) / (s0 / 2 ** j) ** 4 for j in range(levels)]
    T = [[x] for x in R]
    for j in range(1, levels):
        for k in range(1, j + 1):
            T[j].append((4 ** k * T[j][k - 1] - T[j - 1][k - 1]) / (4 ** k - 1))
    norm = pot.normaliser(v)
    return {"kind": kind, "curve_parameter": v, "c4": T[-1][-1], "c4_hat": T[-1][-1] / norm,
            "richardson_error": abs(T[-1][-1] - T[-1][-2]) / norm}


# ---- falsification reconnaissance ---------------------------------------------------------------------------------------
def variant_carrier(row, variant):
    """Deliberately altered carriers from a scan row's chart quantities (Q_chart, bA_chart, bE_chart, hE, rho)."""
    nrm2 = row["one_plus_rho2"]
    Q, bA, bE, hE = row["Q_chart"], row["bA_chart"], row["bE_chart"], row["hE"]
    if variant == "Eg back-reaction deleted":
        return (Q - mp.mpf(3) / 2 * bA ** 2) / nrm2 ** 2
    if variant == "factor 3 -> 2":
        return (Q - bA ** 2 - 2 * bE ** 2 / hE) / nrm2 ** 2
    if variant == "unit normalisation (1+rho^2)^2 -> (1+rho^2)":
        return (Q - mp.mpf(3) / 2 * bA ** 2 - 3 * bE ** 2 / hE) / nrm2
    raise ValueError(variant)


def wrong_kernel_carrier(row, G):
    """The carrier with the projective kernel sign flipped: chart (1, -rho). G: per-form divided differences or
    derivatives at the row. Returns the carrier and the kernel residual |Mh (1, -rho)|."""
    rho = -row["rho"]
    parts = chart_carrier_symbolic(G, rho)
    return parts["c4_hat"], mp.norm(row["Mh"] * mp.matrix([1, rho]))


def per_form_values(row):
    """f_hat for the 13 forms at a scan row (divided differences, or derivatives at the corner, or the q = 0 form)."""
    if row["delta"] == 0:
        return g_prime_num(row["q"])
    if row["q"] == 0:
        gp, g0 = b2.g4_num(row["p"]), g_zero_num()
        return {k: (gp[k] - g0[k]) / row["p"] for k in NAMES}
    return b1.divided(b2.g4_num, row["p"], row["q"])


def raw_c4_from_carrier(row):
    """Raw c4 = q W_q (p - q) c4_hat at a row: zero at both endpoints (factors q and p - q)."""
    return row["q"] * _W(row["q"]) * row["delta"] * row["c4_hat"]


def raw_c4_unnormalised(qq, guess):
    """Raw c4 (potential not divided by q W_q (p - q)) at an interior curve point, by the independent route; with the
    ratio c4 / (q W_q (p - q)). Used to show that raw c4 vanishes at both ends of the curve."""
    p = own_curve_point("two_term", guess, q=qq)
    pot = Potential("two_term", p=p, q=qq)
    fam = LimitFamily(pot)
    E, vecs = fam.normal_modes()
    k0 = min(range(4), key=lambda k: abs(E[k]))
    e = fam.to_R24(vecs[k0])
    raw = Potential("two_term", p=p, q=qq)
    raw.s = mp.mpf(1)
    res = raw24_c4(raw, e)
    q_ = mp.mpf(qq)
    return {"q": q_, "p": p, "c4_raw": res["c4"], "factor": q_ * _W(q_) * (p - q_),
            "c4_raw_over_factor": res["c4"] / (q_ * _W(q_) * (p - q_))}


def falsification_report(rows, indep, raw_series=None, rel_tol="1e-20"):
    """Deliberately false statements and whether the numerical machinery exposes them.
    rows: scan rows (dicts as returned by scan); indep: {label: (row, independent c4_hat)} at the comparison points;
    raw_series: optional list of raw_c4_unnormalised results near the two ends."""
    tol = mp.mpf(rel_tol)
    out = []
    c = [x["c4_hat"] for x in rows]
    m = min(c)
    bound = m * (1 + mp.mpf("1e-6"))
    viol = [i for i, x in enumerate(c) if x < bound]
    out.append({"statement": "c4_hat >= (observed minimum)(1 + 1e-6) on the closed curve",
                "test": "every scan row compared with the bound",
                "exposed": bool(viol),
                "evidence": {"bound": mp.nstr(bound, 20), "violating_rows": len(viol),
                             "first_violation_q": mp.nstr(rows[viol[0]]["q"], 15) if viol else None}})
    for variant in ("Eg back-reaction deleted", "factor 3 -> 2", "unit normalisation (1+rho^2)^2 -> (1+rho^2)"):
        devs = {lab: abs(variant_carrier(row, variant) / iv - 1) for lab, (row, iv) in indep.items()}
        out.append({"statement": f"carrier with {variant} equals c4_hat",
                    "test": "compared with the independent raw 24-D route at every comparison point",
                    "exposed": all(d > tol for d in devs.values()),
                    "evidence": {"min_relative_deviation": mp.nstr(min(devs.values()), 5),
                                 "max_relative_deviation": mp.nstr(max(devs.values()), 5)}})
    devs, resid = {}, {}
    for lab, (row, iv) in indep.items():
        val, res = wrong_kernel_carrier(row, per_form_values(row))
        devs[lab] = abs(val / iv - 1)
        resid[lab] = res
    out.append({"statement": "the projective kernel is (1, -rho) (sign of rho flipped)",
                "test": "kernel residual |Mh (1, -rho)| and comparison with the independent route",
                "exposed": all(d > tol for d in devs.values()) and all(x > mp.mpf("1e-10") for x in resid.values()),
                "evidence": {"min_relative_deviation": mp.nstr(min(devs.values()), 5),
                             "min_kernel_residual": mp.nstr(min(resid.values()), 5),
                             "true_kernel_residual_max": mp.nstr(max(x["kernel_residual"] for x in rows), 3)}})
    row_c = rows[-1]
    values_as_derivatives = chart_carrier_symbolic(b2.g4_num(row_c["q"]), row_c["rho"])["c4_hat"]
    ivc = indep["corner"][1] if "corner" in indep else None
    if ivc is not None:
        out.append({"statement": "at the corner the divided differences may be replaced by the values g(q_c)",
                    "test": "compared with the independent corner route (derivative potential)",
                    "exposed": abs(values_as_derivatives / ivc - 1) > tol,
                    "evidence": {"relative_deviation": mp.nstr(abs(values_as_derivatives / ivc - 1), 5)}})
    ends = [raw_c4_from_carrier(rows[0]), raw_c4_from_carrier(rows[-1])]
    ev = {"raw_c4_at_q0": mp.nstr(ends[0], 5), "raw_c4_at_corner": mp.nstr(ends[1], 5)}
    if raw_series:
        ev["raw_c4_near_the_ends"] = [{"q": mp.nstr(x["q"], 12), "p - q": mp.nstr(x["p"] - x["q"], 8),
                                       "c4_raw": mp.nstr(x["c4_raw"], 10),
                                       "c4_raw/(q W_q (p - q))": mp.nstr(x["c4_raw_over_factor"], 20)}
                                      for x in raw_series]
    out.append({"statement": "raw c4 is nonzero at q = 0 and at q = q_c",
                "test": "raw c4 = q W_q (p - q) c4_hat at the two endpoint rows; raw 24-D c4 near the ends",
                "exposed": all(x == 0 for x in ends),
                "evidence": ev})
    return out
