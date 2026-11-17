"""Phase B2.4: Proposition B2 (the local D2h-axial pitchfork). The exact layer is the proof; the numerical tests are
corroboration only. The negative controls check that incorrect statements and invalid dependency graphs are rejected."""
import copy
import json
import pathlib

import mpmath as mp
import pytest
import sympy as sp

from cube_bif import b2_branch as B

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data"


@pytest.fixture(autouse=True)
def _working_precision():
    with mp.workdps(40):
        yield


# ---- exact layer: the reduced scalar equation ----------------------------------------------------------------------
def test_generic_even_LS_expansion():
    """Generic Z2-invariant energy on (s, wA, wE, wf): V_red even, s^2 coefficient = Schur/2, s^4 coefficient at mu = 0
    = (D4V - 3 b^T H_WW^-1 b)/24, w1 only along f_1, second-order correction in span{A_HAT, E_HAT} at mu = 0."""
    ls = B.generic_ls_checks()
    assert ls and all(ls.values()), ls


def test_removal_of_evenness_is_detected():
    """Negative control: one odd monomial s^3 in V gives an odd coefficient in V_red."""
    assert B.evenness_breaking_detected()


def test_model_hessian_on_fix_is_block_diagonal():
    m = B.model_structure()
    assert m["A_E_rows_decoupled"] and m["T2g_block_equals_B0_K"]


def test_schur_complement_and_lambda_prime_equals_tau():
    sch = B.schur_identities()
    assert sch["schur_equals_detK_over_fKf"] and sch["lambda_at_0_is_0"] and sch["lambda_prime_at_0_is_tau"]


def test_G_has_the_factor_6():
    g = B.reduced_G()
    assert g["matches"]
    assert sp.diff(g["G"], B.z).subs(B.z, 0) == B.C4 / 6
    assert B.FACTOR == 6


# ---- exact layer: implicit function theorem and branch side ---------------------------------------------------------
def test_ift_slope_and_amplitude_law():
    br = B.ift_branch()
    assert br["G_mu"] == B.TAU and br["G_z"] == B.C40 / 6
    assert sp.simplify(br["m1"] + B.C40 / (6 * B.TAU)) == 0
    assert sp.simplify(br["Z1"] + 6 * B.TAU / B.C40) == 0
    assert sp.simplify(br["Z1"] * br["m1"] - 1) == 0


def test_branch_side_is_derived_from_the_signs():
    assert B.branch_side("<0", ">0") == "mu > 0"          # the established case: tau < 0, c4 > 0
    assert B.branch_side(">0", ">0") == "mu < 0"          # wrong sign of tau flips the side
    assert B.branch_side("<0", "<0") == "mu < 0"          # wrong sign of c4 flips the side
    assert B.branch_side(">0", "<0") == "mu > 0"


def test_classification_in_the_energy_reduced_axial_convention():
    assert B.classify("<0", ">0") == "supercritical"
    assert B.classify(">0", ">0") == "supercritical"      # the type is the sign of c4, not of tau
    assert B.classify("<0", "<0") == "subcritical"
    assert B.classify(">0", "<0") == "subcritical"


def test_axial_curvature_leading_terms():
    c = B.axial_curvature()
    assert c["cube"] == B.TAU * B.mu and c["branch"] == -2 * B.TAU * B.mu
    assert c["G_on_branch_order1"] == 0 and c["G_on_branch_order2"] == 0
    T, C, m = sp.symbols("T C m", positive=True)       # tau = -T < 0, c4 = C > 0, mu = m > 0 (branch side)
    assert (c["cube"].subs({B.TAU: -T, B.mu: m})).is_negative
    assert (c["branch"].subs({B.TAU: -T, B.mu: m})).is_positive


# ---- exact layer: symmetry and geometry -----------------------------------------------------------------------------
def test_isotropy_of_branch_points_is_exactly_Sigma():
    iso = B.isotropy_exact()
    assert iso["ranks_inside_Sigma"] == [0] and iso["ranks_outside_Sigma"] == [2]
    assert iso["T2g_projector_kills_A_E_fixes_uh1_vh1"] and iso["T2g_projector_commutes"]
    assert iso["order_Sigma"] == 8 and iso["order_Sigma_cap_diagonal_Z2^3"] == 4 < iso["order_Z2^3"]


def test_reversing_elements_exchange_plus_and_minus_branches():
    ex = B.exchange_exact()
    assert ex["n_reversing_elements"] == 8 and ex["all_act_as_diag_1_1_-1_-1"]


def test_first_order_cross_section_is_a_rhombus():
    r = B.rhombus_exact()
    eps = sp.Symbol("epsilon", real=True)
    assert r["equal_sides"] and r["diagonals_perpendicular"]
    assert r["adjacent_side_inner_product"] == -2 * eps          # not a right angle for eps != 0
    assert r["diag_(1,1)_length_factor"] == sp.Abs(eps - 1) and r["diag_(1,-1)_length_factor"] == sp.Abs(eps + 1)


# ---- statement and dependency graph ---------------------------------------------------------------------------------
def test_dependency_graph_is_valid():
    assert B.validate_graph() == []


def test_proposition_statement_is_valid():
    assert B.validate_statement() == []


def test_dependency_graph_has_no_numerical_proof_dependency():
    g = B.DEPENDENCY_GRAPH
    reach = B._reachable(g, g["root"])
    statuses = {n["id"]: n["status"] for n in g["nodes"]}
    assert all(statuses[v] in B.ALLOWED_PROOF_STATUSES for v in reach if v != g["root"])
    assert not reach & {n["id"] for n in g["corroboration_only"]}
    for req in ("LQ_lemma_Q", "B18_tau", "B21_LS_c4_identity", "B20_parity_fixed_space", "STD_lyapunov_schmidt",
                "STD_implicit_function_theorem"):
        assert req in reach


def test_dependency_graph_uses_only_the_six_allowed_inputs():
    g = B.DEPENDENCY_GRAPH
    nodes = {n["id"]: n for n in g["nodes"]}
    reach = B._reachable(g, g["root"]) - {g["root"]}
    inputs = {v for v in reach if nodes[v]["role"] != "step"}
    assert inputs == set(B.ALLOWED_INPUTS) and len(inputs) == 6
    assert all(nodes[v]["status"] == B.ALLOWED_INPUTS[v] for v in inputs)
    assert all(nodes[v]["status"] == "VERIFIED-EXACT" for v in reach - inputs)
    assert set(g["allowed_inputs"]) == set(B.ALLOWED_INPUTS)


def _mutated(**changes):
    st = copy.deepcopy(B.PROPOSITION)
    for k, v in changes.items():
        if k == "inputs":
            st["inputs"] = v
        else:
            st[k] = v
    return st


STATEMENT_CONTROLS = {
    "wrong sign of tau": _mutated(inputs={"tau_sign": ">0", "c4_sign": ">0"}),
    "wrong sign of c4": _mutated(inputs={"tau_sign": "<0", "c4_sign": "<0"}),
    "missing factor 6 in G": _mutated(G="lam + c4*z"),
    "missing factor 6 in the amplitude law": _mutated(amplitude_law="-tau*mu/c4"),
    "missing factor 6 in mu*'(0)": _mutated(mu_star_slope="-c4/tau"),
    "missing factor 24 in V_red": _mutated(reduced_potential="V0 + lam*s**2/2 + c4*s**4/4"),
    "removal of evenness (flag)": _mutated(even_in_s=False),
    "removal of evenness (cubic term in V_red)": _mutated(reduced_potential="V0 + lam*s**2/2 + s**3 + c4*s**4/24"),
    "branch claimed on both sides": _mutated(branch_on_both_sides=True, nontrivial_equilibria_on_other_side=2),
    "branch side written as mu != 0": _mutated(branch_side="mu != 0"),
    "wrong branch side": _mutated(branch_side="mu < 0"),
    "wrong amplitude sign": _mutated(amplitude_law="6*tau*mu/c4"),
    "subcritical label": _mutated(classification="subcritical"),
    "classification without its convention": _mutated(classification_convention=""),
    "axial curvature upgraded to full-space stability": _mutated(claims_full_space_stability=True),
    "axial curvature upgraded to a centre-manifold index": _mutated(claims_centre_manifold_index=True),
    "wrong sign of the branch curvature": _mutated(axial_curvature_branch="2*tau*mu"),
    "wrong cube curvature": _mutated(axial_curvature_cube_branch_side="-tau*mu"),
    "cuboid claim": _mutated(claims_cuboid=True),
    "status upgraded to independently audited": _mutated(status="PROVED (computer-assisted) · INDEPENDENTLY AUDITED"),
    "cube missing on one side": _mutated(cube_exists_for_both_signs=False),
}


@pytest.mark.parametrize("name", sorted(STATEMENT_CONTROLS))
def test_incorrect_statement_is_rejected(name):
    assert B.validate_statement(STATEMENT_CONTROLS[name]) != []


def _graph(fn):
    g = copy.deepcopy(B.DEPENDENCY_GRAPH)
    fn(g)
    return g


def _add_scan_node(g):
    g["nodes"].append({"id": "B22_scan", "role": "input", "status": "VERIFIED-NUMERIC",
                       "statement": "B2.2 401-point scan of c4_hat"})
    g["edges"].append(["L2_ift_branch", "B22_scan"])


def _scan_replaces_lemma_Q(g):
    g["edges"] = [[a, ("N_B22_scan" if b == "LQ_lemma_Q" else b)] for a, b in g["edges"]]


def _lemma_Q_relabelled_as_scan(g):
    for nd in g["nodes"]:
        if nd["id"] == "LQ_lemma_Q":
            nd["status"] = "VERIFIED-NUMERIC"


def _numeric_branch_points_as_proof(g):
    g["edges"].append(["L2_ift_branch", "N_B24_branch_points"])


def _cycle(g):
    g["edges"].append(["LQ_lemma_Q", "P_B2"])


def _drop_tau(g):
    g["edges"] = [e for e in g["edges"] if e[1] != "B18_tau"]


def _candidate_input(g):
    for nd in g["nodes"]:
        if nd["id"] == "B21_LS_c4_identity":
            nd["status"] = "CANDIDATE"


def _unlisted_input(g):
    g["nodes"].append({"id": "B1_lemma_K", "role": "input", "status": "CERTIFIED",
                       "statement": "B1 Lemma K: kappa_hat > 0 on the closed T2g curve"})
    g["edges"].append(["L5_geometry", "B1_lemma_K"])


def _step_not_exact(g):
    for nd in g["nodes"]:
        if nd["id"] == "L4_axial_curvature":
            nd["status"] = "STANDARD"


def _lemma_Q_downgraded_to_exact(g):
    for nd in g["nodes"]:
        if nd["id"] == "LQ_lemma_Q":
            nd["status"] = "FROZEN INPUT"


GRAPH_CONTROLS = {
    "B2.2 scan added as a proof dependency": _add_scan_node,
    "B2.2 scan used instead of Lemma Q": _scan_replaces_lemma_Q,
    "Lemma Q replaced by a VERIFIED-NUMERIC claim": _lemma_Q_relabelled_as_scan,
    "B2.4 numerical branch points used as proof": _numeric_branch_points_as_proof,
    "cyclic dependency": _cycle,
    "transversality tau < 0 dropped": _drop_tau,
    "CANDIDATE input": _candidate_input,
    "unlisted input added (B1 Lemma K)": _unlisted_input,
    "derivation step without VERIFIED-EXACT status": _step_not_exact,
    "allowed input with the wrong status": _lemma_Q_downgraded_to_exact,
}


# the validator rule each invalid graph must trip (a substring of its failure message)
GRAPH_CONTROL_REASONS = {
    "B2.2 scan added as a proof dependency": "forbidden proof status VERIFIED-NUMERIC",
    "B2.2 scan used instead of Lemma Q": "corroboration-only node N_B22_scan",
    "Lemma Q replaced by a VERIFIED-NUMERIC claim": "forbidden proof status VERIFIED-NUMERIC",
    "B2.4 numerical branch points used as proof": "corroboration-only node N_B24_branch_points",
    "cyclic dependency": "cycle",
    "transversality tau < 0 dropped": "required dependency B18_tau not reachable",
    "CANDIDATE input": "forbidden proof status CANDIDATE",
    "unlisted input added (B1 Lemma K)": "B1_lemma_K is not one of the six allowed proof inputs",
    "derivation step without VERIFIED-EXACT status": "derivation step L4_axial_curvature is not VERIFIED-EXACT",
    "allowed input with the wrong status": "allowed input LQ_lemma_Q has status FROZEN INPUT",
}


@pytest.mark.parametrize("name", sorted(GRAPH_CONTROLS))
def test_invalid_dependency_graph_is_rejected(name):
    g = _graph(GRAPH_CONTROLS[name])
    fails = B.validate_graph(g)
    assert fails != []
    assert any(GRAPH_CONTROL_REASONS[name] in f for f in fails), fails
    assert B.validate_statement(B.PROPOSITION, g) != []


# ---- numerical corroboration (not a proof dependency) ---------------------------------------------------------------
@pytest.fixture(scope="module")
def cd08():
    with mp.workdps(60):
        return B.curve_data("0.8")


def test_numeric_branch_exists_only_for_mu_positive_with_both_signs(cd08):
    """NUMERICAL corroboration: at q = 0.8, p = P_T(1 +- 1e-6), Newton in Fix(Sigma) finds +-s* for mu > 0 with the
    full 24-D gradient ~ 0 and returns to the cube for mu < 0."""
    with mp.workdps(60):
        a = B.branch_point("0.8", "1e-6", 1, cd=cd08)
        b = B.branch_point("0.8", "1e-6", -1, cd=cd08)
        c = B.branch_point("0.8", "-1e-6", 1, cd=cd08)
        assert a["s_found"] > 0 > b["s_found"] and abs(a["s_found"] + b["s_found"]) < mp.mpf("1e-40")
        assert max(a["full_gradient_norm"], b["full_gradient_norm"]) < mp.mpf("1e-50")
        assert abs(a["amplitude_law_error"]) < mp.mpf("1e-4")
        assert a["axial_curvature"] > 0 > a["axial_curvature_cube"]
        assert abs(a["axial_curvature"] / (-2 * a["tau_mu"]) - 1) < mp.mpf("1e-3")
        assert abs(c["s_found"]) < mp.mpf("1e-40") and c["axial_curvature_cube"] > 0
        img = B.reversing_image_numeric(a["x"])
        assert max(abs(u - v) for u, v in zip(img, b["x"])) < mp.mpf("1e-50")


def test_numeric_amplitude_law_error_is_order_mu(cd08):
    with mp.workdps(60):
        e6 = B.branch_point("0.8", "1e-6", 1, cd=cd08)["amplitude_law_error"]
        e7 = B.branch_point("0.8", "1e-7", 1, cd=cd08)["amplitude_law_error"]
        assert 5 < e6 / e7 < 20


def test_numeric_reduced_scan_sign_changes(cd08):
    plus = B.reduced_scan("0.8", "1e-6", npts=12, cd=cd08)
    minus = B.reduced_scan("0.8", "-1e-6", npts=12, cd=cd08)
    assert plus["sign_changes"] == 1 and minus["sign_changes"] == 0
    assert all(v > 0 for _, v in minus["values"])


# ---- records --------------------------------------------------------------------------------------------------------
def test_B2_4_records():
    if not (DATA / "B2_4_branch.json").exists():
        pytest.skip("data/ not generated")
    rec = json.loads((DATA / "B2_4_branch.json").read_text())
    assert rec["all_checks_pass"] and rec["exact"]["all_exact_checks_pass"]
    assert rec["numeric_corroboration"]["all_numeric_checks_pass"]
    assert rec["status"] == B.STATUS_PROVED
    assert [c["q"] for c in rec["numeric_corroboration"]["curve_points"]] == ["0.2", "0.8", "1.5", "2.0"]
    assert "not a proof dependency" in rec["numeric_corroboration"]["role"]
    g = json.loads((DATA / "B2_4_dependency_graph.json").read_text())
    assert g["graph"] == json.loads(json.dumps(B.DEPENDENCY_GRAPH))
    assert g["statement"] == json.loads(json.dumps(B.PROPOSITION))
    assert g["graph_validation_failures"] == [] and g["statement_validation_failures"] == []
