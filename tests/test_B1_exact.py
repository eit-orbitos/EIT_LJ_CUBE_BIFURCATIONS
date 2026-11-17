"""Phase B1 (exact layer and routes): trilinear structure, I3 restriction, difference forms, divided differences,
projective chart, transversality identity, direct 24-D differentiation, endpoint values."""
import itertools

import mpmath as mp
import pytest
import sympy as sp

from cube_bif import b1_cubic as b1
from cube_bif import pairsum as ps
from cube_bif import t2g

mp.mp.dps = 40


@pytest.fixture(autouse=True)
def _working_precision():
    """Each test runs at this module's precision, whatever other modules set."""
    with mp.workdps(40):
        yield


@pytest.fixture(scope="module")
def table():
    return b1.trilinear_table()


# ---- B1.1 route 1: the 216 trilinear values ------------------------------------------------------------------------
def test_216_values_vanish_off_the_I3_pattern(table):
    assert len(table) == 216
    nonzero = [(ch, idx) for (ch, idx), v in table.items() if v != 0]
    assert len(nonzero) == 48
    assert all(sorted(idx) == [0, 1, 2] for _, idx in nonzero)


def test_each_channel_is_invariant_under_index_permutations(table):
    for ch in ("".join(c) for c in itertools.product("uv", repeat=3)):
        vals = {sp.expand(table[(ch, idx)] - table[(ch, (0, 1, 2))]) for idx in itertools.permutations(range(3))}
        assert vals == {0}, ch


def test_mixed_channels_coincide(table):
    """Symmetry of D^3V in its arguments plus index-permutation invariance: uuv = uvu = vuu, uvv = vuv = vvu."""
    for group in (("uuv", "uvu", "vuu"), ("uvv", "vuv", "vvu")):
        vals = {sp.expand(table[(g, (0, 1, 2))] - table[(group[0], (0, 1, 2))]) for g in group}
        assert vals == {0}


def test_independent_coefficients_closed_forms():
    P = ps.PSI
    t = b1.independent_coefficients()
    s2 = sp.sqrt(2)
    expect = {"uuu": -12 * P[(2, 2)] - 12 * P[(2, 3)] - 32 * P[(3, 3)],
              "uuv": -s2 * (10 * P[(2, 3)] + 16 * P[(3, 3)]),
              "uvv": -8 * P[(2, 1)] - 8 * P[(2, 3)] - 16 * P[(3, 3)],
              "vvv": -8 * s2 * P[(3, 3)]}
    for m in b1.CHANNELS:
        assert sp.expand(t[m] - expect[m]) == 0, m


def test_kappa_is_the_binomial_cubic_in_n():
    t = b1.independent_coefficients()
    k = b1.kappa_form()
    poly = sp.Poly(k, b1.nu, b1.nv)
    assert poly.total_degree() == 3 and poly.is_homogeneous
    assert sp.expand(poly.coeff_monomial(b1.nu ** 2 * b1.nv) - 3 * t["uuv"]) == 0
    assert sp.expand(poly.coeff_monomial(b1.nu * b1.nv ** 2) - 3 * t["uvv"]) == 0


# ---- B1.1 route 2: raw 24-D ----------------------------------------------------------------------------------------
@pytest.fixture(scope="module")
def raw():
    return b1.raw24_pair_tensors()


def test_raw24_route_reproduces_the_four_coefficients(raw):
    basis = {"u": t2g.UH, "v": t2g.VH}
    ind = b1.independent_coefficients()
    for m in b1.CHANNELS:
        val = b1.raw24_contract(basis[m[0]][0], basis[m[1]][1], basis[m[2]][2])
        assert sp.simplify(val - ind[m]) == 0, m


def test_raw24_cubic_restriction_is_a_multiple_of_I3(raw):
    """D^3V[x, x, x] with x = sum a_k e_k (symbolic n_u, n_v, generic psi) equals 6 kappa a1 a2 a3 exactly."""
    e = b1.critical_vectors()
    x = e[0] * b1.a1 + e[1] * b1.a2 + e[2] * b1.a3
    C = b1.raw24_contract(x, x, x)
    assert sp.expand(C - 6 * b1.kappa_form() * b1.a1 * b1.a2 * b1.a3) == 0


def test_raw24_off_pattern_contractions_vanish(raw):
    e = b1.critical_vectors()
    for idx in ((0, 0, 0), (0, 0, 1), (1, 1, 2), (2, 2, 2), (0, 2, 2)):
        assert b1.raw24_contract(e[idx[0]], e[idx[1]], e[idx[2]]) == 0, idx


# ---- B1.2 two-term specialisation and the factorisation --------------------------------------------------------------
@pytest.mark.parametrize("m", b1.CHANNELS)
def test_each_coefficient_is_an_exact_difference_form(m):
    assert b1.difference_form_residual(m) == 0


@pytest.mark.parametrize("m", b1.CHANNELS)
def test_closed_forms_match_pairsum_and_have_no_division_by_r(m):
    L = b1.independent_coefficients()[m]
    assert sp.simplify(ps.g_of(L, "r") - b1.G_CLOSED[m]) == 0
    assert b1.r not in sp.denom(sp.together(b1.G_CLOSED[m])).free_symbols


def test_divided_difference_curve_condition():
    """det M_hat = D / (p - q)^2 (2x2), and D~(p, q) is symmetric in p and q: the mirror of the physical curve."""
    p, q = sp.symbols("p q")
    A = sp.Matrix(2, 2, lambda i, j: sp.Function(f"m{i}{j}")(p) if i <= j else sp.Function(f"m{j}{i}")(p))
    B = A.subs(p, q)
    D = (A - B).det()
    assert sp.simplify(((A - B) / (p - q)).det() - D / (p - q) ** 2) == 0
    assert sp.simplify(((A - B) / (p - q)).det() - ((B - A) / (q - p)).det()) == 0


def test_projective_chart_is_the_kernel_on_the_curve():
    a, b, c = sp.symbols("a b c")
    Mh = sp.Matrix([[a, b], [b, c]])
    v = Mh * sp.Matrix([1, -b / c])
    assert sp.simplify(v[0] - Mh.det() / c) == 0 and sp.simplify(v[1]) == 0


def test_transversality_identity_for_a_singular_symmetric_block():
    """For N = [[a, b], [b, c]] with ac = b^2 and kernel vector n: adj(N) = tr(N) n n^T / |n|^2. Hence
    d/dp det(M(p) - M(q)) = tr(N) n^T M'(p) n / |n|^2 on the curve (B1.8)."""
    a, b = sp.symbols("a b", nonzero=True)
    c = b ** 2 / a
    N = sp.Matrix([[a, b], [b, c]])
    n = sp.Matrix([-b, a])
    assert sp.simplify(N * n) == sp.zeros(2, 1)
    assert sp.simplify(N.adjugate() - N.trace() * n * n.T / (n.T * n)[0]) == sp.zeros(2)


# ---- B1.5 route 3 and the gauge ---------------------------------------------------------------------------------------
@pytest.mark.parametrize("qq", ["0.3", "1.0", "1.8"])
def test_route3_direct_differentiation_matches(qq):
    c = b1.carrier(qq)
    formula = c["q"] * b1.W_num(c["q"]) * c["delta"] * c["kappa_hat"]
    direct = b1.kappa_direct(c["p"], c["q"], 1, c["rho"])
    assert abs(direct / formula - 1) < mp.mpf("1e-30")


def test_B0_null_vector_is_minus_the_chart_vector():
    c = b1.carrier("1.0")
    nB0 = t2g.null_vector(c["p"], c["q"])
    chart = mp.matrix([1, c["rho"]]) / mp.sqrt(1 + c["rho"] ** 2)
    assert mp.norm(nB0 + chart) < mp.mpf("1e-30")


# ---- B1.4 endpoints ---------------------------------------------------------------------------------------------------
def test_endpoint_q0_limit():
    c = b1.carrier(0)
    assert mp.mpf(b1.PT0_LO) <= c["p"] <= mp.mpf(b1.PT0_HI)
    assert abs(c["kappa_hat"] - mp.mpf("0.002879512579955")) < mp.mpf("1e-14")
    assert c["tau_hat"] < 0


def test_corner_limit():
    lo, hi = mp.mpf(b1.QC_LO), mp.mpf(b1.QC_HI)
    assert mp.det(b1.M_prime(lo)) > 0 > mp.det(b1.M_prime(hi))          # consistent with Paper 2, Lemma T2
    c = b1.corner_limit((lo + hi) / 2)
    assert abs(c["kappa_hat"] - mp.mpf("0.006891782309648")) < mp.mpf("1e-14")
    assert c["tau_tilde"] < 0


# ---- B1.6 candidate scan (coarse here; the recorded scan uses 400 intervals) --------------------------------------------
def test_coarse_scan_has_no_sign_change():
    rows = b1.scan(40)
    k = [r_["kappa_hat"] for r_ in rows]
    assert min(k) > mp.mpf("0.0028") and max(k) < mp.mpf("0.0069")
    assert all(r_["Mh22"] > mp.mpf("1.45") for r_ in rows)
    assert all(r_["tau_tilde"] < 0 for r_ in rows)
    assert all(r_["dDtilde_ddelta"] < 0 for r_ in rows)
