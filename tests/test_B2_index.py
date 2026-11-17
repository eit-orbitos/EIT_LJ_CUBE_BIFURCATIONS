"""Phase B2.5: Proposition B3 (index 1 of the three-dimensional centre-manifold reduced Hessian on the D2h branch) and
Corollary B3' (full-slice index 4). The exact layer is the proof; the numerical tests are corroboration only. The
negative controls check that false alternatives and invalid dependency graphs are rejected."""
import copy
import io
import json
import pathlib
import zipfile

import mpmath as mp
import pytest
import sympy as sp

from cube_bif import b2_index as X

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


@pytest.fixture(autouse=True)
def _working_precision():
    with mp.workdps(40):
        yield


# ---- exact layer ----------------------------------------------------------------------------------------------------
def test_group_and_invariant_basis():
    inv = X.invariant_basis_check()
    assert inv["order"] == 24 and inv["all_invariant"] and inv["deg1_empty"]
    assert inv["deg2_spanned_by_I2"] and inv["deg3_spanned_by_I3"] and inv["deg4_spanned_by_I2sq_I4"]
    assert inv["signed_permutations_even_minus"]
    assert X.invariant_dimensions(6) == {1: 0, 2: 1, 3: 1, 4: 2, 5: 1, 6: 3}


def test_axis_commutant_and_parity():
    com = X.commutant_on_axis()
    assert com["stabiliser_order"] == 4 and com["h12_zero"] and com["h22_eq_h33"] and com["free_parameters"] == 3
    par = X.parity_on_axis()
    assert par["reversers"] == 4 and par["all"]


def test_generic_invariant_hessian_on_axis():
    g = X.generic_invariant_hessian(6)
    assert g["structure"] and g["h11_even"] and g["d_even"] and g["e_odd"]
    assert g["h11_low_ok"] and g["d_low_ok"] and g["e_low_ok"]


def test_branch_hessian_series():
    b = X.branch_hessian_series(6)
    assert b["m1_ok"] and b["h11_ok"] and b["d_ok"] and b["e_ok"] and b["det_ok"] and b["offdiag_zero"]
    assert b["h11_as_mu_ok"]


def test_no_competing_linear_diagonal_term():
    """The transverse diagonal entry has no O(s) term and the off-diagonal entry is exactly kappa s at first order."""
    b = X.branch_hessian_series(6)
    assert sp.expand(b["d"]).coeff(X.s, 1) == 0 and sp.expand(b["h11"]).coeff(X.s, 1) == 0
    assert sp.expand(b["e"]).coeff(X.s, 1) == X.KAP and sp.expand(b["e"]).coeff(X.s, 2) == 0


def test_transverse_eigensystem_and_bound():
    te = X.transverse_eigensystem()
    assert te["plus"] and te["minus"] and te["det"]
    tb = X.transverse_sign_bound()
    assert tb["identity"] and tb["all_negative"] and tb["inequality_cases"] == 432


@pytest.mark.parametrize("kap", [sp.Rational(3, 100), -sp.Rational(3, 100)])
@pytest.mark.parametrize("sv", [sp.Rational(1, 1000), -sp.Rational(1, 1000)])
def test_centre_index_gauge_and_sign_independent(kap, sv):
    """Leading-order 3x3 Hessian diag((c4/3)s^2) + [[-4 beta s^2, kappa s], [kappa s, -4 beta s^2]] with c4 > 0 and
    beta of either sign: exactly one negative eigenvalue for both signs of kappa and of s."""
    for beta in (sp.Rational(7, 10), -sp.Rational(7, 10)):
        c4 = sp.Integer(17)
        H = sp.Matrix([[c4 / 3 * sv ** 2, 0, 0], [0, -4 * beta * sv ** 2, kap * sv], [0, kap * sv, -4 * beta * sv ** 2]])
        assert X._inertia(H) == (1, 0, 2)
    assert X.centre_index_from_signs(">0") == 1 and X.centre_index_from_signs(">0", kappa_nonzero=False) is None


def test_ls_quartic_complete_invariant_form():
    r = X.ls_quartic_exact()
    assert r["invariant_form_exact"] and r["alpha_plus_beta_is_c4_over_24"] and r["hand_formula_ok"]
    assert r["b_irreps_present"] == ["A1g", "Eg", "T2g"] and r["d4_only_iiii_iijj"]
    ab = X.alpha_beta_closed()
    assert sp.expand(ab["alpha"] - r["alpha"]) == 0 and sp.expand(ab["beta"] - r["beta"]) == 0


def test_b_has_no_rigid_or_odd_component():
    dec = X.b_decomposition()
    zero = dec["zero_components"]
    for G in ("A2g", "T1g", "A1u", "A2u", "Eu", "T1u", "T2u"):
        assert zero[G], G
    assert not zero["A1g"] and not zero["Eg"] and not zero["T2g"]


def test_generic_multid_LS_and_schur_identity():
    ls = X.generic_ls_multid()
    assert ls["quartic_formula"] and ls["ls_residual_order2"] and ls["generic_coefficients"] == 55
    assert X.schur_hessian_identity()


def test_haynsworth_inertia_additivity():
    assert X.haynsworth_check()


def test_complementary_index_derived_from_frozen_table():
    ci = X.complementary_index()
    assert ci == {"total_dim": 24, "rigid": 6, "critical": 3, "W_dim": 15, "m_perp": 3, "W_positive": 12,
                  "W_zero": 0, "W_invertible": True, "paper2_index_on_curve": 3, "paper2_nullity_on_curve": 3}
    assert X.paper2_curve_consistency()["m_perp_constant_3"]
    assert X.full_index_corollary() == {"m_perp": 3, "full_slice_index": 4, "full_slice_nullity": 0,
                                        "hessian_R24_zero_eigenvalues": 6}


def _paper2_zip():
    from cube_bif import paper2_ref
    try:
        return paper2_ref.archive_path()
    except Exception:
        return None


def test_frozen_table_matches_paper2_archive():
    """The quoted block signs agree with Paper 2's own records (monotonicity directions and multiplicities)."""
    path = _paper2_zip()
    if path is None or not pathlib.Path(path).exists():
        pytest.skip("Paper 2 archive not available")
    z = zipfile.ZipFile(path)
    name = [n for n in z.namelist() if n.endswith("data/cube_index_theorem.json")][0]
    mono = json.load(io.BytesIO(z.read(name)))["monotonicity"]
    assert mono["Eu"] == "decreasing" and mono["A2u"] == "sign change"
    for k in ("A1g (breathing)", "Eg (cuboid)", "T1u (internal)", "T2u"):
        assert mono[k] == "increasing"
    tex = [n for n in z.namelist() if n.endswith("sections/05_morse_classification.tex")][0]
    t = z.read(tex).decode()
    assert "$q<\\qc$, $p=P_T(q)$ & $<0$ (T4) & $=0$ & 3 & 3" in t


def test_frozen_table_mutation_changes_m_perp():
    """Negative control: with A2u wrongly positive on the curve the derived m_perp is 2, so index 4 is not derivable."""
    tab = [dict(r) for r in X.FROZEN_SPECTRUM_ON_CURVE]
    for r in tab:
        if r["block"] == "A2u":
            r["sign"] = "+"
    assert X.complementary_index(tab)["m_perp"] == 2
    assert X.full_index_corollary(1, tab)["full_slice_index"] == 3
    tab0 = [dict(r) for r in X.FROZEN_SPECTRUM_ON_CURVE]
    for r in tab0:
        if r["block"] == "Eu":
            r["sign"] = "0"
    assert X.full_index_corollary(1, tab0) is None


def test_conjugate_branches_one_index_type():
    cj = X.conjugate_branches()
    assert cj["orbit3_ok"] and cj["orbit24_ok"] and cj["index_types"] == 1
    assert X.congruence_preserves_inertia()


def test_d3d_consistency():
    d = X.d3d_consistency()
    assert d["axial_ok"] and d["transverse_ok"]
    assert (d["centre_index_mu_pos"], d["centre_index_mu_neg"]) == (2, 1)
    assert (d["full_index_mu_pos"], d["full_index_mu_neg"]) == (5, 4)
    assert d["degree_sum_mu_pos"] == d["degree_sum_mu_neg"] == -3


# ---- statement and dependency graph ----------------------------------------------------------------------------------
def test_statement_and_graph_valid():
    assert X.validate_graph() == []
    assert X.validate_statement() == []


def test_graph_record_matches_module():
    rec = json.loads((DATA / "B2_5_dependency_graph.json").read_text())
    assert rec == json.loads(json.dumps(X.DEPENDENCY_GRAPH))


def test_centre_index_does_not_use_paper2_spectrum():
    assert "P2_theorem_index_on_curve" not in X._reachable(X.DEPENDENCY_GRAPH, "P_B3")
    assert "P2_theorem_index_on_curve" in X._reachable(X.DEPENDENCY_GRAPH, "C_B3")


BAD_PROP = {
    "transverse block positive definite": {"transverse_block": "positive definite"},
    "transverse block negative definite": {"transverse_block": "negative definite"},
    "kappa s term omitted": {"hessian_e": "0"},
    "kappa s replaced by kappa s^2": {"hessian_e": "kappa*s**2"},
    "determinant positive": {"transverse_det": "kappa**2*s**2"},
    "axial curvature alone as centre index": {"centre_index": 0, "centre_index_uses_axial_curvature_only": True},
    "index attributed to the axial curvature only (flag)": {"centre_index_uses_axial_curvature_only": True},
    "centre index 0": {"centre_index": 0},
    "centre index 2": {"centre_index": 2},
    "full-space stability from centre index": {"claims_full_space_stability": True},
    "stability claimed": {"claims_stability": True},
    "h11 with c4/6": {"hessian_h11": "c4*s**2/6"},
    "d with wrong sign": {"hessian_d": "4*beta*s**2"},
    "d with an O(s) term": {"hessian_d": "kappa*s - 4*beta*s**2"},
    "alpha + beta = c4/6": {"alpha_plus_beta": "c4/6"},
    "one quartic invariant only": {"invariant_dimensions": {2: 1, 3: 1, 4: 1}},
    "quartic I2^2 only": {"reduced_potential": "V0 + lam*I2/2 + kappa*I3 + alpha*I2**2"},
    "cubic term dropped": {"reduced_potential": "V0 + lam*I2/2 + alpha*I2**2 + beta*I4"},
    "conjugate copies counted as distinct index types": {"index_types_among_conjugates": 6},
    "gauge-dependent index": {"independent_of_kappa_gauge": False},
    "index depends on the sign of s": {"independent_of_s_sign": False},
    "h12 nonzero": {"hessian_offdiagonal_axial_zero": False},
    "audited status claimed": {"status": "PROVED (computer-assisted) · INDEPENDENTLY AUDITED"},
}

BAD_COR = {
    "rigid motions counted (index 10)": {"full_slice_index": 10, "R24_negative_eigenvalues": 10},
    "rigid motions counted (flag)": {"rigid_motions_counted": True},
    "rigid zero modes miscounted": {"R24_zero_eigenvalues": 0},
    "Paper 2 complementary index assumed": {"m_perp_assumed": True},
    "m_perp asserted without derivation": {"m_perp_source": "Paper 2 (quoted value)"},
    "m_perp = 2": {"m_perp": 2, "full_slice_index": 3, "R24_negative_eigenvalues": 3},
    "full index 3 (axial only)": {"full_slice_index": 3, "R24_negative_eigenvalues": 3},
    "full index 5": {"full_slice_index": 5, "R24_negative_eigenvalues": 5},
    "full-space stability claimed": {"claims_full_space_stability": True},
    "stable claimed": {"stable": True},
    "nonzero slice nullity": {"full_slice_nullity": 1},
}


@pytest.mark.parametrize("name", sorted(BAD_PROP))
def test_false_proposition_statements_rejected(name):
    st = copy.deepcopy(X.PROPOSITION_B3)
    st.update(BAD_PROP[name])
    assert X.validate_statement(st) != [], name


@pytest.mark.parametrize("name", sorted(BAD_COR))
def test_false_corollary_statements_rejected(name):
    co = copy.deepcopy(X.COROLLARY_B3)
    co.update(BAD_COR[name])
    assert X.validate_statement(None, co) != [], name


def _graph_with(mut):
    g = copy.deepcopy(X.DEPENDENCY_GRAPH)
    mut(g)
    return g


def _add_leaf(g, node, parent="S6_centre_index"):
    g["nodes"].append(node)
    g["edges"].append([parent, node["id"]])


BAD_GRAPHS = {
    "m_perp as an assumed input": lambda g: _add_leaf(g, {"id": "A_m_perp", "role": "input", "status": "ASSUMED",
                                                         "statement": "m_perp = 3"}, "C1_complementary_index"),
    "B2.2 scan as proof": lambda g: g["edges"].append(["S6_centre_index", "N_B22_scan"]),
    "Hessian numerics as proof": lambda g: g["edges"].append(["S5_transverse_inertia", "N_B25_hessian"]),
    "D3d consistency as proof": lambda g: g["edges"].append(["P_B3", "K_d3d_consistency"]),
    "centre index uses Paper 2 spectrum": lambda g: g["edges"].append(["S6_centre_index",
                                                                      "P2_theorem_index_on_curve"]),
    "Lemma K dropped": lambda g: g.update(edges=[e for e in g["edges"] if e[1] != "IN_lemma_K_kappa"]),
    "Paper 2 spectrum dropped from corollary": lambda g: g.update(
        edges=[e for e in g["edges"] if e[1] != "P2_theorem_index_on_curve"]),
    "unlisted input (Lemma Q as a separate leaf)": lambda g: _add_leaf(
        g, {"id": "LQ", "role": "input", "status": "CERTIFIED", "statement": "c4_hat > 0"}),
    "cycle": lambda g: g["edges"].append(["IN_exact_Oh_T2g_structure", "S1_invariant_normal_form"]),
    "derivation step not exact": lambda g: [n.update(status="CANDIDATE") for n in g["nodes"]
                                            if n["id"] == "S5_transverse_inertia"],
    "Proposition B2 with numeric status": lambda g: [n.update(status="VERIFIED-NUMERIC") for n in g["nodes"]
                                                     if n["id"] == "IN_proposition_B2"],
    "root marked audited": lambda g: [n.update(status="PROVED · INDEPENDENTLY AUDITED") for n in g["nodes"]
                                      if n["id"] == "P_B3"],
}


@pytest.mark.parametrize("name", sorted(BAD_GRAPHS))
def test_invalid_graphs_rejected(name):
    assert X.validate_graph(_graph_with(BAD_GRAPHS[name])) != [], name


# ---- numerical corroboration (not part of the proof) -------------------------------------------------------------------
def test_live_d2h_hessian_corroboration():
    r = X.d2h_point(mp.mpf("0.8"), "1e-6", 1, dps=60)
    assert r["neg"] == 4 and r["zero"] == 6 and r["W_neg"] == 3 and r["schur_neg"] == 1 and r["schur_zero"] == 0
    assert r["full_gradient_norm"] < mp.mpf("1e-50") and r["rigid_residual"] < mp.mpf("1e-50")
    assert max(abs(r["h11_rel_err"]), abs(r["d_rel_err"]), abs(r["e_rel_err"])) < mp.mpf("1e-4")
    ev = r["transverse_eigs"]
    assert ev[0] > 0 > ev[1]             # kappa s > 0: the negative direction is (0, 1, -1)


def test_live_quartic_route3():
    r = X.quartic_route3(mp.mpf("1.5"), (2, 1, 0), dps=60)
    assert r["rel_diff"] < mp.mpf("1e-18")


def test_numeric_record_all_checks_pass():
    rec = json.loads((DATA / "B2_5_index.json").read_text())
    assert rec["exact"]["all_pass"] and rec["exact"]["n_checks"] == 32
    nc = rec["numeric_checks"]
    assert nc["failed"] == [] and nc["passed"] == nc["n"] >= 300
