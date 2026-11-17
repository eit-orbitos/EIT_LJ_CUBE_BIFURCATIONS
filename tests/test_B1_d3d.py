"""Phase B1.8-B1.10: the reduced equation on a D3d axis (exact algebra), the Schur-complement eigenvalue, the
transcritical sign, the numerically located branch (corroboration only), and the retained D2h parity fact."""
import mpmath as mp
import pytest
import sympy as sp

from cube_bif import b1_cubic as b1
from cube_bif import t2g
from cube_bif.group import D24, oh_matrices
from cube_bif.modes import E_BR

mp.mp.dps = 40


@pytest.fixture(autouse=True)
def _working_precision():
    """Each test runs at this module's precision, whatever other modules set."""
    with mp.workdps(40):
        yield


def test_fix_D3d_in_R24_is_breathing_plus_the_two_T2g_diagonals():
    S = t2g.stabilizer((1, 1, 1))
    assert len(S) == 12
    P = sum((D24(R) for R in S), sp.zeros(24)) / len(S)
    assert P.rank() == 3
    for v in (E_BR, sum(t2g.UH, sp.zeros(24, 1)), sum(t2g.VH, sp.zeros(24, 1))):
        assert sp.simplify(P * v - v) == sp.zeros(24, 1)


def test_invariant_quadratic_and_cubic_forms_are_one_dimensional():
    mats = [t2g.T3(R) for R in oh_matrices()]
    assert t2g.invariant_dimension(2, mats) == 1 and t2g.invariant_dimension(3, mats) == 1
    assert t2g.reynolds(t2g.I3, mats) == t2g.I3
    assert sp.expand(t2g.reynolds(t2g.a1 ** 2, mats) - (t2g.a1 ** 2 + t2g.a2 ** 2 + t2g.a3 ** 2) / 3) == 0


def test_reduced_equation_on_the_D3d_axis():
    """V_red = V0 + (1/2) lam |a|^2 + kap a1 a2 a3 + quartic invariants. On a = s(1, 1, 1):
    dV/ds = 3 s (lam + kap s + O(s^2)), so G(s, mu) = lam(mu) + kap(mu) s + O(s^2), and the implicit function
    theorem gives s*(mu) = -lam(mu)/kap + O(mu^2) with slope -lam'(0)/kap."""
    s, mu, lam1, kap, c1, c2 = sp.symbols("s mu lambda1 kappa c1 c2", real=True)
    a1, a2, a3 = t2g.A
    lam = lam1 * mu
    Vred = lam / 2 * (a1 ** 2 + a2 ** 2 + a3 ** 2) + kap * a1 * a2 * a3 \
        + c1 * (a1 ** 2 + a2 ** 2 + a3 ** 2) ** 2 + c2 * (a1 ** 4 + a2 ** 4 + a3 ** 4)
    on_axis = sp.expand(Vred.subs({a1: s, a2: s, a3: s}))
    dV = sp.diff(on_axis, s)
    G = sp.cancel(dV / (3 * s))
    assert sp.expand(G - (lam + kap * s + sp.Rational(4, 3) * (9 * c1 + 3 * c2) * s ** 2)) == 0
    slope = (-sp.diff(G, mu) / sp.diff(G, s)).subs({s: 0, mu: 0})
    assert sp.simplify(slope + lam1 / kap) == 0
    grad = [sp.diff(Vred, v).subs({a1: s, a2: s, a3: s}) for v in t2g.A]
    assert sp.simplify(grad[0] - grad[1]) == 0 and sp.simplify(grad[1] - grad[2]) == 0   # gradient stays on the axis


def test_schur_complement_eigenvalue_and_its_derivative():
    """lam_red(mu) = n0^T K n0 - (n0^T K m0)^2/(m0^T K m0), with K(0) n0 = 0: lam_red(0) = 0 and
    lam_red'(0) = n0^T K'(0) n0 = tau (B1.8)."""
    mu = sp.Symbol("mu")
    k11, k12, k22, d11, d12, d22 = sp.symbols("k11 k12 k22 d11 d12 d22", real=True)
    t = sp.Symbol("t", positive=True)
    n0 = sp.Matrix([sp.cos(t), sp.sin(t)])
    m0 = sp.Matrix([-sp.sin(t), sp.cos(t)])
    K0 = k22 * m0 * m0.T                                          # K(0) has kernel n0
    K = K0 + mu * sp.Matrix([[d11, d12], [d12, d22]])
    S = (n0.T * K * n0)[0] - (n0.T * K * m0)[0] ** 2 / (m0.T * K * m0)[0]
    assert sp.simplify(S.subs(mu, 0)) == 0
    assert sp.simplify(sp.diff(S, mu).subs(mu, 0) - (n0.T * sp.Matrix([[d11, d12], [d12, d22]]) * n0)[0]) == 0


def test_schur_eigenvalue_vanishes_on_the_curve_numerically():
    c = b1.carrier("1.0")
    K = b1.M_hat(c["p"], c["q"])
    n0 = mp.matrix([1, c["rho"]]) / mp.sqrt(1 + c["rho"] ** 2)
    assert abs(b1.schur_reduced_eigenvalue(K, n0)) < mp.mpf("1e-30")


@pytest.mark.parametrize("qq", ["0.05", "1.0", "2.0"])
def test_transcritical_slope_sign_in_the_chart_gauge(qq):
    """kappa > 0 (certificate, gauge n_u > 0) and tau < 0 (Paper 2 Lemmas T1, T3): s*'(0) = -tau/kappa > 0."""
    c = b1.carrier(qq)
    nrm = mp.sqrt(1 + c["rho"] ** 2)
    kap = c["q"] * b1.W_num(c["q"]) * c["delta"] * c["kappa_hat"] / nrm ** 3
    tau = c["q"] * b1.W_num(c["q"]) * c["tau_hat"] / nrm ** 2
    assert kap > 0 and tau < 0 and -tau / kap > 0


@pytest.mark.parametrize("qq", ["0.3", "1.8"])
def test_d3d_branch_exists_on_both_sides_numerically(qq):
    """NUMERICAL corroboration (not used in any proof): Newton in Fix(D3d) finds genuine equilibria (full 24-D
    gradient ~ 0) on both sides of the curve, with s of the sign of mu and |s/s_pred - 1| = O(mu)."""
    plus, minus = b1.d3d_branch_point(qq, "1e-7"), b1.d3d_branch_point(qq, "-1e-7")
    for r in (plus, minus):
        assert r["full_gradient_norm"] < mp.mpf("1e-40")
        assert abs(r["s_found"] / r["s_predicted"] - 1) < mp.mpf("2e-3")
    assert plus["s_found"] > 0 > minus["s_found"]


def test_D2h_axis_restriction_is_even_and_D3d_axis_is_not():
    """B1.10 (retained from B0): some T(R) maps (1, 0, 0) to -(1, 0, 0), so V_red restricted to the D2h axis is even
    and its scalar equation odd (pitchfork type; the quartic coefficient belongs to B2). No T(R) maps (1, 1, 1) to
    -(1, 1, 1), consistent with the nonzero cubic term kappa s^3 on the D3d axis."""
    e1, d = sp.Matrix([1, 0, 0]), sp.Matrix([1, 1, 1])
    assert any(t2g.T3(R) * e1 == -e1 for R in oh_matrices())
    assert not any(t2g.T3(R) * d == -d for R in oh_matrices())
    assert t2g.I3.subs({t2g.a1: 1, t2g.a2: 0, t2g.a3: 0}) == 0
