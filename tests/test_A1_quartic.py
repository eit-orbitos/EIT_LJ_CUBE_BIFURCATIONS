"""Phase A1 — one test per identity of the quartic Lyapunov-Schmidt computation on the A2u curve."""
import mpmath as mp
import pytest
import sympy as sp

from cube_bif import a2u, branch, numeric as nm, paper2_ref
from cube_bif import pairsum as ps
from cube_bif.modes import E_A, E_BR, ROTATIONS, TRANSLATIONS

mp.mp.dps = 40
PSI = ps.PSI
ALPHA = {k: 2 * PSI[(1, k)] + 4 * k * PSI[(2, k)] for k in (1, 2, 3)}     # phi''(sqrt k)
BETA = {k: 2 * PSI[(1, k)] for k in (1, 2, 3)}                            # phi'(sqrt k)/sqrt k
R_, X_, Y_ = a2u.r, a2u.x, a2u.y


@pytest.fixture(scope="module")
def rs():
    return a2u.r_star()


@pytest.fixture(scope="module")
def forms():
    return a2u.forms()


def test_V_aa_is_paper2_A2u_block(forms):
    assert sp.expand(forms["V_aa"] - (4 * ALPHA[2] + 4 * BETA[1])) == 0


def test_V_bb_is_paper2_A1g_block(forms):
    assert sp.expand(forms["V_bb"] - (2 * ALPHA[1] + 4 * ALPHA[2] + 2 * ALPHA[3])) == 0


def test_V_b_vanishes_exactly_at_the_equilibrium(forms):
    assert forms["V_b"] != 0
    assert sp.simplify(forms["V_b"].subs(ps.two_term())) == 0


def test_b_vector_lies_in_the_breathing_direction(forms):
    b = a2u.b_vector()
    beta = (b.T * E_BR)[0, 0] / sp.sqrt(24)
    assert sp.simplify(b - beta * E_BR / sp.sqrt(24)) == sp.zeros(24, 1)
    assert sp.simplify(beta - forms["V_aab"]) == 0


def test_e_A_and_e_br_are_hessian_eigenvectors(forms):
    H = ps.hessian()
    assert sp.expand(H * E_A - forms["V_aa"] * E_A) == sp.zeros(24, 1)
    assert sp.expand(H * E_BR - forms["V_bb"] * E_BR) == sp.zeros(24, 1)


def test_translations_in_kernel_for_any_pair_potential():
    H = ps.hessian()
    for v in TRANSLATIONS:
        assert sp.expand(H * v) == sp.zeros(24, 1)


def test_rotations_in_kernel_only_at_equilibrium():
    H = ps.hessian()
    for v in ROTATIONS:
        assert sp.expand(H * v) != sp.zeros(24, 1)
        assert sp.simplify((H * v).subs(ps.two_term())) == sp.zeros(24, 1)


def test_g_functions_closed_forms():
    g = a2u.g_functions()
    W = 3 * X_ + Y_ + 3
    assert sp.simplify(g["h_A"] - a2u.H_A_FROZEN) == 0
    assert sp.simplify(g["g_B"] - 2 * (R_ + 1)) == 0
    assert sp.simplify(g["g_3"] - sp.sqrt(6) * (R_ + 2) * (2 - (R_ + 1) * X_) / W) == 0
    assert sp.simplify(g["g_4"] - (R_ + 2) * ((R_ + 1) * (R_ + 3) * X_ + 12) / W) == 0


def test_difference_form_at_the_equilibrium(forms):
    """Q = q W_q [g_Q(p) - g_Q(q)] for Q in {V_aa, V_bb, V_aab, V_aaaa} (two-term potential, A = t)."""
    sub = ps.two_term()
    for key in ("V_aa", "V_bb", "V_aab", "V_aaaa"):
        gq = ps.g_of(forms[key])
        rhs = ps.q_ * ps.W("q") * (gq.subs({ps.r_: ps.p_, ps.X["r"]: ps.X["p"], ps.Y["r"]: ps.Y["p"]})
                                   - gq.subs({ps.r_: ps.q_, ps.X["r"]: ps.X["q"], ps.Y["r"]: ps.Y["q"]}))
        assert sp.simplify(forms[key].subs(sub) - rhs) == 0, key


def test_scale_free_series_coefficients():
    sf = a2u.scale_free_coefficients()
    assert sp.simplify(sf["U0"] - 12 * (1 + X_ + Y_ / 3)) == 0
    assert sp.simplify(sf["U2"] - (3 * R_ ** 2 * X_ - 9 * R_ - R_ * Y_)) == 0
    assert sp.simplify(sf["U4"] - (sp.Rational(3, 4) * R_ ** 4 * X_ + sp.Rational(81, 4) * R_ ** 2
                                   + sp.Rational(63, 2) * R_ + Y_ * (3 * R_ ** 2 + 2 * R_) / 4)) == 0
    # independent numerical differentiation of the T_d family itself
    for rr in ("0.7", "2.3"):
        U = lambda t: branch.U_sym(rr, t)
        rrm = mp.mpf(rr)
        Xn, Yn = mp.power(2, -rrm / 2), mp.power(3, -rrm / 2)
        for key, order in (("U2", 2), ("U4", 4)):
            exact = sp.lambdify((R_, X_, Y_), sf[key], "mpmath")(rrm, Xn, Yn)
            assert abs(mp.diff(U, 0, order) - exact) < mp.mpf(10) ** -25


def test_k_equals_h_A_over_8_minus_quarter():
    sf = a2u.scale_free_coefficients()
    assert sp.simplify(sf["k"] - (a2u.H_A_FROZEN / 8 - sp.Rational(1, 4))) == 0


def test_m_limits():
    sf = a2u.scale_free_coefficients()
    m_r = sf["m"].subs({X_: 2 ** (-R_ / 2), Y_: 3 ** (-R_ / 2)})
    assert sp.limit(m_r, R_, 0) == sp.Rational(8, 7)
    assert sp.limit(m_r, R_, sp.oo) == sp.Rational(21, 8)


def test_generic_foliation_lemma():
    L = a2u.foliation_lemma()
    s = L["symbols"]
    assert sp.simplify(L["c4_R1"] - (s["F_aaaa"] - 3 * s["F_aab"] ** 2 / s["F_bb"])) == 0
    assert sp.simplify(L["quadratic_R1"] - L["quadratic_R2"]) == 0
    assert L["difference"] != 0
    assert sp.simplify(L["difference"].subs(s["F_aa"], 0)) == 0


def test_scale_free_chain_constant():
    c4, res = a2u.scale_free_chain()
    assert res == 0


def test_r_star_and_P_A_soft_match_frozen_constants(rs):
    assert abs(rs - mp.mpf(paper2_ref.FROZEN["r_star"])) < mp.mpf(10) ** -19
    P0 = mp.findroot(lambda t: a2u.h_A_num(t) + mp.mpf(6) / 7, (rs, mp.mpf("3.2")), solver="anderson")
    assert abs(P0 - mp.mpf(paper2_ref.FROZEN["P_A_soft"])) < mp.mpf(10) ** -19


def test_P_A_matches_paper2_code(rs):
    cit = paper2_ref.load_analysis("cube_index_theorem")
    if cit is None:
        pytest.skip("frozen Paper 2 archive not available")
    for qq in ("0.05", "0.3", "0.7", "1.0", "1.3", "1.47"):
        assert abs(a2u.P_A(qq, rs) - cit.P_A(float(qq))) < 1e-12


@pytest.mark.parametrize("qq", ["0.01", "0.3", "0.9", "1.4", "1.4749"])
def test_full_energy_and_scale_free_c4_agree_on_curve(qq, rs):
    cp = a2u.curve_point(qq, rs)
    assert abs(cp["h_A(p)-h_A(q)"]) < mp.mpf(10) ** -35
    assert abs(cp["c4_full"] - cp["c4_scale_free"]) <= mp.mpf(10) ** -25 * abs(cp["c4_full"])


def test_the_two_c4_formulas_differ_off_the_curve():
    g = {k: a2u.numeric(v) for k, v in a2u.g_functions().items()}
    m = a2u.numeric(a2u.scale_free_coefficients()["m"])
    qq, pp = mp.mpf("0.9"), mp.mpf("2.5")                    # h_A(p) != h_A(q)
    pref = qq * a2u.W_num(qq)
    d = {k: g[k](pp) - g[k](qq) for k in g}
    full = pref * (d["g_4"] - 3 * d["g_3"] ** 2 / d["g_B"])
    sf = mp.mpf(16) / 3 * pref * (m(pp) - m(qq))
    assert abs(d["h_A"]) > mp.mpf("0.01") and abs(full - sf) > mp.mpf("0.01")


@pytest.mark.parametrize("qq", ["0.5", "1.2"])
def test_c4_by_the_24D_numeric_route(qq, rs):
    """Independent route: energy in R^24, b by differentiating the analytic gradient, <b, H_perp^-1 b> by solving
    (H + P_ker) w = b, no symmetry reduction."""
    cp = a2u.curve_point(qq, rs)
    T = [nm.unit_field(lambda s, k=k: [1 if j == k else 0 for j in range(3)]) for k in range(3)]

    def cross(k, s):
        e = [0, 0, 0]
        e[k] = 1
        return [e[1] * s[2] - e[2] * s[1], e[2] * s[0] - e[0] * s[2], e[0] * s[1] - e[1] * s[0]]

    Rr = [nm.unit_field(lambda s, k=k: cross(k, s)) for k in range(3)]
    out = nm.lyapunov_schmidt_c4(cp["p"], cp["q"], T + Rr + [nm.e_A()])
    tol = mp.mpf(10) ** -30
    assert abs(out["c4"] - cp["c4_full"]) < tol * abs(cp["c4_full"])
    assert abs(out["V_aa"]) < tol
    assert abs(out["V_bb"] - cp["V_bb"]) < tol and abs(out["V_aab"] - cp["V_aab"]) < tol
    eb = nm.e_br()
    beta = mp.fsum(out["b"][i] * eb[i] for i in range(24))
    assert max(abs(out["b"][i] - beta * eb[i]) for i in range(24)) < tol


def test_transversality_on_the_curve(rs):
    """d V_aa / dp = q W_q h_A'(p) at p = P_A(q); h_A' < 0 on (r*, inf) is Paper 2 Lemma A (frozen input)."""
    for qq in ("0.02", "0.5", "1.0", "1.47"):
        pp = a2u.P_A(qq, rs)
        assert mp.diff(a2u.h_A_num, pp) < 0


def test_sign_of_c4_on_a_grid_numerical(rs):
    """NUMERICAL: c4 > 0 and Delta_m in [1.21, 1.27] at 40 points of the curve (the full table has 415)."""
    for i in range(1, 41):
        cp = a2u.curve_point(rs * mp.mpf(i) / 41, rs)
        assert cp["c4_full"] > 0
        assert mp.mpf("1.21") < cp["Delta_m"] < mp.mpf("1.27")


def test_m_is_increasing_on_the_curve_range_numerical(rs):
    """NUMERICAL (not certified): m' > 0.6 on a grid of (0, P_A(0+)], so m(P_A(q)) > m(q) for every q."""
    m = a2u.numeric(a2u.scale_free_coefficients()["m"])
    P0 = mp.mpf(paper2_ref.FROZEN["P_A_soft"])
    assert min(mp.diff(m, P0 * mp.mpf(k) / 300) for k in range(1, 301)) > mp.mpf("0.6")


@pytest.mark.parametrize("qq", ["0.2", "1.3"])
def test_local_branch_appears_only_for_p_above_P_A(qq, rs):
    """NUMERICAL: inside the T_d family, small nonzero critical points exist for p = P_A(q)(1 + d), d > 0, with
    u ~ sqrt(-6 f''/f''''), and not for d < 0."""
    pa, q = a2u.P_A(qq, rs), mp.mpf(qq)
    ratios = []
    for d in ("1e-4", "1e-6"):
        bp = branch.branch_point(pa * (1 + mp.mpf(d)), q)
        ratios.append(abs(bp["u_found"] / bp["u_pred"] - 1))
    assert ratios[1] < ratios[0] < mp.mpf("1e-3")
    pm = pa * (1 - mp.mpf("1e-5"))
    assert branch.branch_point(pm, q)["u_pred"] is None
    assert branch.no_small_branch(pm, q, mp.mpf("0.05"))


@pytest.mark.parametrize("qq", ["0.2", "0.8", "1.3"])
def test_first_order_amplitude_law(qq, rs):
    """NUMERICAL: u^2 ~ (3/4) |h_A'(P_A)| (p - P_A) / [m(P_A) - m(q)] for p slightly above P_A(q)."""
    q = mp.mpf(qq)
    pa = a2u.P_A(q, rs)
    pp = pa * (1 + mp.mpf("1e-7"))
    m = a2u.numeric(a2u.scale_free_coefficients()["m"])
    law = mp.mpf(3) / 4 * abs(mp.diff(a2u.h_A_num, pa)) * (pp - pa) / (m(pa) - m(q))
    u = branch.branch_point(pp, q)["u_found"]
    assert abs(u ** 2 / law - 1) < mp.mpf("1e-6")
