"""Phase A2 — exact derivation of m' and m'', the behaviour at r = 0, and the bound P_A(q) < 16/5."""
import mpmath as mp
import sympy as sp
from flint import fmpq

from cube_bif import a2u, certcheck, lemma_m, paper2_ref

r, x, y, L2, L3 = lemma_m.r, lemma_m.x, lemma_m.y, lemma_m.L2, lemma_m.L3


def test_closed_form_is_the_V01_m():
    assert sp.simplify(lemma_m.M_CLOSED - a2u.scale_free_coefficients()["m"]) == 0


def test_closed_form_has_no_division_by_r():
    """r * m equals the V0.1-dev definition U''''/U - 3 (U''/U)^2, and m's denominator is 16 S^2 (no factor r)."""
    sf = a2u.scale_free_coefficients()
    assert sp.simplify(r * lemma_m.M_CLOSED - (sf["U4"] / sf["U0"] - 3 * (sf["U2"] / sf["U0"]) ** 2)) == 0
    num, den = sp.fraction(sp.together(lemma_m.M_CLOSED))
    assert sp.simplify(den / (16 * lemma_m.S ** 2)) == 1
    assert sp.Poly(den, r).degree() == 0


def test_S_is_at_least_3():
    assert sp.expand(lemma_m.S - 3) == 3 * x + y
    assert all(c > 0 for c in sp.Poly(lemma_m.S, x, y).coeffs())


def test_m_prime_formula_by_an_independent_derivation():
    f = lemma_m.forms()
    m1 = certcheck.derive(a2u.scale_free_coefficients()["m"])
    assert certcheck.same(f["Psi"] / (16 * lemma_m.S ** 3), m1)
    assert certcheck.same(f["m'"], m1)


def test_m_second_formula_by_an_independent_derivation():
    f = lemma_m.forms()
    m2 = certcheck.derive(certcheck.derive(a2u.scale_free_coefficients()["m"]))
    assert certcheck.same(f["Phi"] / (16 * lemma_m.S ** 4), m2)


def test_S_prime():
    assert sp.expand(lemma_m.forms()["S'"] - (-sp.Rational(3, 2) * L2 * x - L3 * y / 2)) == 0


def test_m_prime_at_zero_exact_and_positive():
    m1_0 = sp.expand(lemma_m.forms()["m'"].subs({r: 0, x: 1, y: 1}))
    assert sp.simplify(m1_0 - (sp.Rational(18, 49) + sp.Rational(12, 49) * L2 + sp.Rational(57, 784) * L3)) == 0
    assert all(c > 0 for c in sp.Poly(m1_0, L2, L3).coeffs())
    assert abs(m1_0.subs({L2: sp.log(2), L3: sp.log(3)}).evalf(30) - sp.Float("0.616970866226520091604129522735", 30)) \
        < sp.Float("1e-28")


def test_m_second_at_zero_exact():
    m2_0 = sp.expand(lemma_m.forms()["m''"].subs({r: 0, x: 1, y: 1}))
    expect = (sp.Rational(45, 98) + sp.Rational(261, 5488) * L3 - sp.Rational(9, 1372) * L2 - sp.Rational(6, 343) * L2 ** 2
              + sp.Rational(363, 5488) * L2 * L3 - sp.Rational(285, 10976) * L3 ** 2)
    assert sp.simplify(m2_0 - expect) == 0


def test_series_at_zero_matches_numerical_derivatives():
    mp.mp.dps = 40
    m = a2u.numeric(lemma_m.M_CLOSED)
    for order, key in ((1, "m'(0) exact"), (2, "m''(0) exact")):
        e = sp.parse_expr(lemma_m.near_zero()[key], local_dict={"L2": L2, "L3": L3})
        exact = mp.mpf(str(sp.N(e.subs({L2: sp.log(2), L3: sp.log(3)}), 40)))
        assert abs(mp.diff(m, 0, order) - exact) < mp.mpf(10) ** -25


def test_near_zero_initial_interval_certified():
    nz = lemma_m.near_zero()
    assert nz["all_positive"] and nz["initial_interval"] == ["0", "1/8"]
    assert all(s["positive"] and fmpq(*map(int, s["m''_lower_bound"].split("/"))) > 0 for s in nz["m''_positive_on_subboxes"])


def test_P_A_below_16_over_5_inputs_certified():
    pb = lemma_m.pa_bound()
    assert pb["all_certified"]
    a, b = (mp.mpf(fmpq_s.split("/")[0]) / mp.mpf(fmpq_s.split("/")[1]) for fmpq_s in pb["P_A(0+) enclosure"])
    assert a < mp.mpf(paper2_ref.FROZEN["P_A_soft"]) < b
    lo, hi = (mp.mpf(s.split("/")[0]) / mp.mpf(s.split("/")[1]) for s in pb["r* enclosure"])
    assert lo < mp.mpf(paper2_ref.FROZEN["r_star"]) < hi


def test_m_increment_on_the_curve_dominates_the_certified_bound():
    """Consistency with the certificate: [m(P_A(q)) - m(q)]/(P_A(q) - q) >= min lower bound, at 9 curve points."""
    import json
    import pathlib
    mp.mp.dps = 40
    rs = a2u.r_star()
    m = a2u.numeric(lemma_m.M_CLOSED)
    stored = pathlib.Path(__file__).resolve().parents[1] / "data" / "A2_lemma_M_certificate.json"
    cert = json.loads(stored.read_text()) if stored.exists() else lemma_m.build_certificate(stored.parents[1])
    num, den = (int(v) for v in cert["min_lower_bound"].split("/"))
    lmin = mp.mpf(num) / den
    for k in range(1, 10):
        qq = rs * k / 10
        pp = a2u.P_A(qq, rs)
        assert pp < mp.mpf(16) / 5
        assert (m(pp) - m(qq)) / (pp - qq) >= lmin
