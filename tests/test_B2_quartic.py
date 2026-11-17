"""Phase B2.1 — the quartic Lyapunov-Schmidt coefficient c4 on the D2h axis (NOTES §6.2): exact linear forms, the
Hessian on the fixed space, closed forms and difference forms, and the three routes."""
import mpmath as mp
import pytest
import sympy as sp

from cube_bif import b1_cubic as b1
from cube_bif import b2_quartic as b2
from cube_bif import b2_symmetry as s2
from cube_bif import pairsum as ps
from cube_bif import t2g

mp.mp.dps = 50
P = ps.PSI
S2 = sp.sqrt(2)


@pytest.fixture(autouse=True)
def _working_precision():
    with mp.workdps(50):
        yield


def zero(v):
    return v.applyfunc(sp.expand) == sp.zeros(*v.shape)


# ---- exact decomposition of the Hessian on the fixed space ------------------------------------------------------------
def test_A_and_E_hat_are_eigenvectors_of_the_full_24D_hessian():
    H = ps.hessian()
    f = b2.linear_forms()
    assert zero(H * s2.A_HAT - f["hA"] * s2.A_HAT)
    assert zero(H * s2.E_HAT - f["hE"] * s2.E_HAT)


def test_hessian_on_fix_is_diag_hA_hE_plus_the_B0_block():
    H = b2.hessian_on_fix()
    f = b2.linear_forms()
    K = t2g.block_K()[0]
    assert all(H[i, j] == 0 for i in range(4) for j in range(4) if i != j and not (i >= 2 and j >= 2))
    assert sp.expand(H[0, 0] - f["hA"]) == 0 and sp.expand(H[1, 1] - f["hE"]) == 0
    assert sp.simplify(H[2:, 2:] - K) == sp.zeros(2)


def test_hessian_scalars_are_paper2_A1g_and_Eg_blocks():
    """Paper 2 (§6 table, Lemma S): A1g = 2a1 + 4a2 + 2a3, Eg = 2a1 + a2 + 3b2 + 2b3 with a_k = phi''(r_k),
    b_k = phi'(r_k)/r_k; for phi(r) = psi(r^2): a_k = 2 psi'(k) + 4k psi''(k), b_k = 2 psi'(k)."""
    a = {k: 2 * P[(1, k)] + 4 * k * P[(2, k)] for k in (1, 2, 3)}
    b = {k: 2 * P[(1, k)] for k in (1, 2, 3)}
    f = b2.linear_forms()
    assert sp.expand(f["hA"] - (2 * a[1] + 4 * a[2] + 2 * a[3])) == 0
    assert sp.expand(f["hE"] - (2 * a[1] + a[2] + 3 * b[2] + 2 * b[3])) == 0


def test_hessian_closed_forms_are_paper2_h_L_exactly():
    """h_L(r) = sum_k ((r+1) l_k - m_k) k^(-(r+2)/2) / W_r with (l; m) = (2,4,2; 0,0,0) and (2,1,0; 0,3,2)."""
    r, X, Y = b2.r, b2.Xr, b2.Yr
    g = {1: sp.Integer(1), 2: X / 2, 3: Y / 3}
    W = 1 + X + Y / 3

    def h_L(l, m):
        return sum(((r + 1) * l[k - 1] - m[k - 1]) * g[k] for k in (1, 2, 3)) / W

    assert sp.simplify(b2.G4_CLOSED["hA"] - h_L((2, 4, 2), (0, 0, 0))) == 0
    assert sp.simplify(b2.G4_CLOSED["hE"] - h_L((2, 1, 0), (0, 3, 2))) == 0
    assert sp.simplify(b2.G4_CLOSED["hA"] - 2 * (r + 1)) == 0          # so hA_hat = 2 exactly


# ---- the 13 linear forms ---------------------------------------------------------------------------------------------------
def test_quartic_channel_forms():
    f = b2.linear_forms()
    expect = {
        "Q_uuuu": 6 * P[(2, 1)] + 18 * P[(2, 2)] + 12 * P[(2, 3)] + 96 * P[(3, 2)] + 96 * P[(3, 3)]
        + 64 * P[(4, 2)] + 64 * P[(4, 3)],
        "Q_uuuv": S2 * (24 * P[(3, 3)] + 32 * P[(4, 3)]),
        "Q_uuvv": 4 * P[(2, 1)] + 4 * P[(2, 3)] + 24 * P[(3, 3)] + 32 * P[(4, 3)],
        "Q_uvvv": S2 * (24 * P[(3, 3)] + 16 * P[(4, 3)]),
        "Q_vvvv": 36 * P[(2, 1)] + 12 * P[(2, 3)] + 48 * P[(3, 1)] + 48 * P[(3, 3)] + 16 * P[(4, 1)] + 16 * P[(4, 3)],
    }
    for k, v in expect.items():
        assert sp.expand(f[k] - v) == 0, k


def test_back_reaction_forms_are_the_B2_0_components():
    f = b2.linear_forms()
    comps = s2.b_components()
    for ch in b2.B_CHANNELS:
        assert sp.expand(f["bA_" + ch] - comps[ch]["A1g"]) == 0
        assert sp.expand(f["bE_" + ch] - comps[ch]["Eg"]) == 0


def test_c4_formula_is_gauge_invariant():
    c = b2.c4_generic()
    assert sp.simplify(c - c.subs({b2.nu: -b2.nu, b2.nv: -b2.nv}, simultaneous=True)) == 0


# ---- route 2(a): exact raw line differentiation -----------------------------------------------------------------------------
def test_route2a_raw_quartic_equals_route1():
    assert sp.expand(b2.raw_quartic() - b2.Q_of_n()) == 0


def test_route2a_raw_b_vector_equals_the_B2_0_vector():
    assert zero(b2.raw_b_vector() - s2.b_vector())


def test_route2a_raw_hessian_scalars():
    f = b2.linear_forms()
    assert sp.expand(b2.raw_mixed_derivative([s2.A_HAT], [2]) - f["hA"]) == 0
    assert sp.expand(b2.raw_mixed_derivative([s2.E_HAT], [2]) - f["hE"]) == 0
    assert sp.expand(b2.raw_mixed_derivative([s2.e1()], [3])) == 0            # no cubic term on the axis


# ---- two-term specialisation -----------------------------------------------------------------------------------------------
@pytest.mark.parametrize("name", b2.FORM_NAMES)
def test_closed_forms_match_pairsum_and_have_no_division_by_r(name):
    assert b2.closed_form_residual(name) == 0
    assert b2.r not in sp.denom(sp.together(b2.G4_CLOSED[name])).free_symbols


@pytest.mark.parametrize("name", b2.FORM_NAMES)
def test_each_form_is_an_exact_difference_form(name):
    assert b2.difference_form_residual(name) == 0


def test_factorisation_identity():
    assert b2.factorisation_identity() == 0


def test_route1_unit_quantities_reassemble_c4():
    c = b2.route1("1.0")
    c4 = c["D4V"] - 3 * c["b_A"] ** 2 / c["h_A"] - 3 * c["b_E"] ** 2 / c["h_E"]
    assert abs(c4 / c["c4"] - 1) < mp.mpf("1e-40")
    assert abs(c["hA_hat"] - 2) < mp.mpf("1e-40") and c["hE_hat"] > 0


# ---- route 2(b): numeric raw 24-D with a spectral linear solve ----------------------------------------------------------------
@pytest.mark.parametrize("qq", ["0.3", "1.0", "1.8"])
def test_route2_numeric_raw_24D_agrees(qq):
    r1 = b2.route1(qq)
    r2 = b2.route2_numeric(qq)
    assert r2["n_small_eigenvalues"] == 9                 # 6 rigid motions + the 3 critical T2g vectors
    assert r2["max_small_eigenvalue"] < mp.mpf("1e-40") and r2["min_nonzero_eigenvalue"] > mp.mpf("1e-3")
    assert r2["max_b_component_on_small_eigenvectors"] < mp.mpf("1e-40")
    assert r2["He_residual"] < mp.mpf("1e-40")
    assert abs(r2["D4V"] / r1["D4V"] - 1) < mp.mpf("1e-40")
    assert abs(r2["c4"] / r1["c4"] - 1) < mp.mpf("1e-40")


# ---- route 3: restricted D2h family --------------------------------------------------------------------------------------------
@pytest.mark.parametrize("qq", ["0.3", "1.8"])
def test_route3_restricted_family_agrees(qq):
    with mp.workdps(60):
        r1 = b2.route1(qq)
        r3 = b2.route3(qq)
        K = t2g.M_num(r1["p"]) - t2g.M_num(r1["q"])
        trK = r1["q"] * b1.W_num(r1["q"]) * (K[0, 0] + K[1, 1])
        assert abs(r3["p"] - r1["p"]) < mp.mpf("1e-45")                   # its own curve point
        assert abs(r3["kernel_eigenvalue"]) < mp.mpf("1e-45")
        for got, want in zip(r3["nonzero_eigenvalues"], sorted([trK, r1["h_A"], r1["h_E"]])):
            assert abs(got / want - 1) < mp.mpf("1e-40")
        e = b2._e1_numeric(*r1["n"])
        ip = mp.fsum(x * y for x, y in zip(r3["kernel_vector_R24"], e))
        assert abs(abs(ip) - 1) < mp.mpf("1e-40")                           # its kernel vector is +-e_1
        assert r3["evenness_defect"] < mp.mpf("1e-35")
        assert r3["richardson_error"] < mp.mpf("1e-25") * abs(r1["c4"])
        assert abs(r3["c4"] / r1["c4"] - 1) < mp.mpf("1e-28")
