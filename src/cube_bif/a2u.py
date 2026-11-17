"""A2u bifurcation of the cube: Phase A0 (representation audit) and Phase A1 (quartic Lyapunov-Schmidt coefficient).

Normalisation (stated once, used everywhere): unit-edge cube y*_s = s/2, phi(r) = t r^-p - r^-q with
t = q W_q / (p W_p) (so y* is an equilibrium), unit directions e_A = E_A/sqrt24, e_br = E_BR/sqrt24, coordinates
x = y* + a e_A + b e_br. Paper 2's normalisation (A = B = 1, edge e = t^(-1/(p-q))) multiplies the n-th derivative
by the positive factor e^(-q-n); no sign changes.
"""
from functools import lru_cache

import mpmath as mp
import sympy as sp

from . import pairsum as ps
from .group import LABELS
from .modes import E_A, E_BR

r, p, q, u = sp.symbols("r p q u", positive=True)
x, y = sp.symbols("x y", positive=True)          # x = 2^(-r/2), y = 3^(-r/2)

# Frozen Paper 2 inputs (paper/NOTES.md Lemma A; analysis/cube_index_theorem.py). Reference only.
# Kept as strings so that they are read at the working precision.
R_STAR_FROZEN = "1.4749107381472217442"
P_A_SOFT_FROZEN = "3.1054933552830915550"
Q_C_FROZEN = "2.0199382317007999883"


# ---- exact linear forms (valid for any pair potential) -----------------------------------------------------------
@lru_cache(maxsize=None)
def forms():
    """D^n V at the cube along unit e_A, e_br, as linear forms in psi_k(sig). Odd-in-a ones vanish identically."""
    D2AA = ps.derivative([E_A, E_A])
    D2BB = ps.derivative([E_BR, E_BR])
    D3AAB = ps.derivative([E_A, E_A, E_BR])
    D4A = ps.derivative([E_A] * 4)
    return {
        "V_a": ps.derivative([E_A]) / sp.sqrt(24),
        "V_b": ps.derivative([E_BR]) / sp.sqrt(24),
        "V_aa": D2AA / 24, "V_bb": D2BB / 24, "V_ab": ps.derivative([E_A, E_BR]) / 24,
        "V_aaa": ps.derivative([E_A] * 3) / 24 ** sp.Rational(3, 2),
        "V_abb": ps.derivative([E_A, E_BR, E_BR]) / 24 ** sp.Rational(3, 2),
        "V_aab": D3AAB / 24 ** sp.Rational(3, 2), "V_aaaa": D4A / 576,
        # rational carriers: c4 = (D4A - 3 D3AAB^2 / D2BB) / 576
        "D2BB": D2BB, "D3AAB": D3AAB, "D4A": D4A,
    }


def b_vector():
    """b = D^3V[e_A, e_A, .] in R^24 (exact linear forms)."""
    comps = []
    for i in range(24):
        ei = sp.zeros(24, 1)
        ei[i] = 1
        comps.append(ps.derivative([E_A, E_A, ei]) / 24)
    return sp.Matrix(comps)


def c4_linear_forms():
    """c4_eff = V_aaaa - 3 V_aab^2 / V_bb, written with rational carriers."""
    f = forms()
    return (f["D4A"] - 3 * f["D3AAB"] ** 2 / f["D2BB"]) / 576


# ---- one-variable functions g_Q(r): Q = q W_q [g_Q(p) - g_Q(q)] at the equilibrium ------------------------------
def _xy(expr):
    return sp.simplify(expr.subs({ps.X["r"]: x, ps.Y["r"]: y, ps.r_: r}))


@lru_cache(maxsize=None)
def g_functions():
    f = forms()
    return {"h_A": _xy(ps.g_of(f["V_aa"])), "g_B": _xy(ps.g_of(f["V_bb"])),
            "g_3": _xy(ps.g_of(f["D3AAB"] / 24 ** sp.Rational(3, 2))), "g_4": _xy(ps.g_of(f["V_aaaa"]))}


W_r = 1 + x + y / 3
H_A_FROZEN = (2 * (r + 1) * x - 4) / W_r            # Paper 2, Lemma A: h_A = N/D


# ---- scale-eliminated formulation: the T_d shape family ----------------------------------------------------------
# rho_+ = e^(-u/2) (even tetrahedron, s1 s2 s3 = +1), rho_- = e^(u/2) (odd): pair distances
#   face diagonals (same parity, 6 + 6): sqrt2 rho_+-;  edges (12): ((3/2)cosh u - 1/2)^(1/2);  body (4): sqrt3 cosh(u/2)
def U_sym(rr, uu, X_=None, Y_=None, mod=sp):
    X_ = 2 ** (-rr / 2) if X_ is None else X_
    Y_ = 3 ** (-rr / 2) if Y_ is None else Y_
    return (12 * X_ * mod.cosh(rr * uu / 2) + 12 * (mod.cosh(uu) * sp.Rational(3, 2) - sp.Rational(1, 2)) ** (-rr / 2)
            + 4 * Y_ * mod.cosh(uu / 2) ** (-rr))


@lru_cache(maxsize=None)
def scale_free_coefficients():
    """U(0), U''(0), U''''(0) of U_sym in u (exact, in r, x, y), and
    k(r) = U''/(r U),  m(r) = [U''''/U - 3 (U''/U)^2] / r   at u = 0, so that for f = log Phi along the family
    f''(0) = p q [k(q) - k(p)],   f''''(0) = p q [m(q) - m(p)]."""
    ser = sp.series(U_sym(r, u, x, y), u, 0, 6).removeO()
    U0 = sp.simplify(ser.coeff(u, 0))
    U2 = sp.simplify(2 * ser.coeff(u, 2))
    U4 = sp.simplify(24 * ser.coeff(u, 4))
    k = sp.simplify(U2 / (r * U0))
    m = sp.simplify((U4 / U0 - 3 * (U2 / U0) ** 2) / r)
    return {"U0": U0, "U2": U2, "U4": U4, "k": k, "m": m}


# ---- numerics (mpmath) -------------------------------------------------------------------------------------------
def numeric(fn_expr):
    """mpmath function of r from an expression in r, x, y."""
    f = sp.lambdify((r, x, y), fn_expr, "mpmath")
    return lambda rr: f(mp.mpf(rr), mp.power(2, -mp.mpf(rr) / 2), mp.power(3, -mp.mpf(rr) / 2))


def W_num(rr):
    rr = mp.mpf(rr)
    return 1 + mp.power(2, -rr / 2) + mp.power(3, -rr / 2) / 3


def h_A_num(rr):
    rr = mp.mpf(rr)
    X_, Y_ = mp.power(2, -rr / 2), mp.power(3, -rr / 2)
    return (2 * (rr + 1) * X_ - 4) / (1 + X_ + Y_ / 3)


def r_star():
    """Unique critical point of h_A (independent recomputation; Paper 2 Lemma A)."""
    return mp.findroot(lambda t: mp.diff(h_A_num, t), mp.mpf("1.47"))


def P_A(qq, rs=None):
    """Frozen Paper 2 definition: the unique p > r* with h_A(p) = h_A(q), for 0 < q < r*."""
    rs = r_star() if rs is None else rs
    qq = mp.mpf(qq)
    if not 0 < qq < rs:
        raise ValueError("P_A is defined only for 0 < q < r*")
    hq = h_A_num(qq)
    # divided difference: near r*, h_A(p) - h_A(q) ~ -c (p - q)(p + q - 2 r*), so this has a simple root
    g = lambda t: (h_A_num(t) - hq) / (t - qq)
    return mp.findroot(g, (rs, mp.mpf("3.2")), solver="anderson")


def curve_point(qq, rs=None):
    """All A1 quantities at q, p = P_A(q), in the unit-edge normalisation."""
    g = g_functions()
    sf = scale_free_coefficients()
    fn = {k: numeric(v) for k, v in g.items()}
    m_num = numeric(sf["m"])
    k_num = numeric(sf["k"])
    qq = mp.mpf(qq)
    pp = P_A(qq, rs)
    pref = qq * W_num(qq)                                 # q W_q
    d = {k: fn[k](pp) - fn[k](qq) for k in fn}
    Vaa = pref * d["h_A"]
    Vbb = pref * d["g_B"]
    Vaab = pref * d["g_3"]
    Vaaaa = pref * d["g_4"]
    c4_full = Vaaaa - 3 * Vaab ** 2 / Vbb
    c4_sf = mp.mpf(16) / 3 * pref * (m_num(pp) - m_num(qq))
    f2 = pp * qq * (k_num(qq) - k_num(pp))
    f4 = pp * qq * (m_num(qq) - m_num(pp))
    return {"q": qq, "p": pp, "h_A(p)-h_A(q)": d["h_A"], "V_aa": Vaa, "V_bb": Vbb, "V_aab": Vaab, "V_aaaa": Vaaaa,
            "c4_full": c4_full, "c4_scale_free": c4_sf, "f2": f2, "f4": f4,
            "Delta_m": (m_num(pp) - m_num(qq)) / (pp - qq),
            "dlambda_dp_sign_carrier": mp.diff(h_A_num, pp)}   # d V_aa / dp = q W_q h_A'(p)


# ---- equivalence of the two reductions (generic symbolic lemma) -------------------------------------------------
def foliation_lemma():
    """Generic F(a, b), even in a, with F_a = F_b = 0 at 0. R1 = critical value along vertical lines a = const
    (full-energy Lyapunov-Schmidt); R2 = critical value along rays from (0, -beta0) (scale elimination; the rays are
    the scaling orbits, beta0 = sqrt6 for the unit-edge cube), parametrised by the a-coordinate alpha of the ray's
    crossing with b = 0. Returns the quartic coefficients c4 (R = F0 + F_aa a^2/2 + c4 a^4/24 + ...)."""
    a, b, al, tau = sp.symbols("a b alpha tau")
    F0, Faa, Fbb, Faab, Fbbb, Faaaa, Faabb, Fbbbb, beta0 = sp.symbols(
        "F0 F_aa F_bb F_aab F_bbb F_aaaa F_aabb F_bbbb beta0", nonzero=True)

    def F(A_, B_):
        return (F0 + Faa * A_ ** 2 / 2 + Fbb * B_ ** 2 / 2 + Faab * A_ ** 2 * B_ / 2 + Fbbb * B_ ** 3 / 6
                + Faaaa * A_ ** 4 / 24 + Faabb * A_ ** 2 * B_ ** 2 / 4 + Fbbbb * B_ ** 4 / 24)

    c2, c4_ = sp.symbols("c2 c4")
    bs = c2 * a ** 2 + c4_ * a ** 4
    eq = sp.expand(sp.diff(F(a, b), b).subs(b, bs))
    sol = sp.solve([eq.coeff(a, 2), eq.coeff(a, 4)], [c2, c4_], dict=True)[0]
    R1 = sp.expand(F(a, bs.subs(sol)))
    d2, d4 = sp.symbols("d2 d4")
    ts = d2 * al ** 2 + d4 * al ** 4
    G = F(al * (1 + tau), beta0 * tau)
    eq2 = sp.expand(sp.diff(G, tau).subs(tau, ts))
    sol2 = sp.solve([eq2.coeff(al, 2), eq2.coeff(al, 4)], [d2, d4], dict=True)[0]
    R2 = sp.expand(G.subs(tau, ts.subs(sol2)))
    c4R1 = sp.simplify(24 * R1.coeff(a, 4))
    c4R2 = sp.simplify(24 * R2.coeff(al, 4))
    return {"c4_R1": c4R1, "c4_R2": c4R2, "difference": sp.factor(sp.simplify(c4R2 - c4R1)),
            "quadratic_R1": sp.simplify(2 * R1.coeff(a, 2)), "quadratic_R2": sp.simplify(2 * R2.coeff(al, 2)),
            "symbols": {"F_aa": Faa, "F_bb": Fbb, "F_aab": Faab, "F_aaaa": Faaaa, "beta0": beta0}}


def scale_free_chain():
    """On the curve (f''(0) = 0): R2(alpha) = V0 exp((f(u(alpha)) - f(0))/(p - q)), u(alpha) = log((1-z)/(1+z)),
    z = alpha/sqrt6, V0 = -12 W_q (p - q)/p (unit edge), f''''(0) = p q [m(q) - m(p)]. Returns c4 from this chain,
    which should equal (16/3) q W_q [m(p) - m(q)]."""
    al = sp.symbols("alpha")
    f4, mp_, mq_, Wq = sp.symbols("f4 m_p m_q W_q")
    uu = sp.log((1 - al / sp.sqrt(6)) / (1 + al / sp.sqrt(6)))
    V0 = -12 * Wq * (p - q) / p
    expo = (f4 / 24 * uu ** 4) / (p - q)
    R2 = sp.series(V0 * sp.exp(expo), al, 0, 6).removeO()
    c4 = sp.simplify(24 * R2.coeff(al, 4))
    c4 = sp.simplify(c4.subs(f4, p * q * (mq_ - mp_)))
    return c4, sp.simplify(c4 - sp.Rational(16, 3) * q * Wq * (mp_ - mq_))
