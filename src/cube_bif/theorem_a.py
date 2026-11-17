"""Theorem A (the A2u pitchfork): statement and proof dependency graph, in machine-readable form.

Each leaf has a status in LEAF_STATUSES:
- VERIFIED-EXACT and CERTIFIED leaves name the tests that check them, as "file::function" under tests/;
- FROZEN INPUT leaves name the Paper 2 item, which is listed in reference/PAPER2_INPUTS.md;
- STANDARD leaves name a reference. They may also name tests that check their hypotheses.

Composite nodes have no status of their own. They list the nodes they use. A leaf may also use other nodes.

Numerical checks (VERIFIED-NUMERIC) are listed under "corroboration". They are never dependencies.

tests/test_A2_theorem.py checks:
- that the graph is closed and acyclic;
- that every named test exists;
- that H1-H4 are dependencies of Theorem A;
- that no numerical check is a dependency.
"""

LEAF_STATUSES = ("VERIFIED-EXACT", "CERTIFIED", "FROZEN INPUT", "STANDARD")
THEOREM_STATUS = "PROVED (computer-assisted) · INDEPENDENTLY AUDITED"

STATEMENT = (
    "Fix q in (0, r*). For p > q let V_p = t(p,q) U_p - U_q, with t = q W_q / (p W_p). The unit-edge cube y* is an "
    "equilibrium of V_p for every p. Let S = y* + T^perp be the O_h-invariant slice, where T is the space of rigid "
    "infinitesimal motions at y*, and let mu = p - P_A(q). "
    "There exist eps > 0 and a neighbourhood N of y* in S such that, for |mu| < eps, the equilibria of V_p in N are "
    "exactly: "
    "(1) the cube y*; "
    "(2) for mu > 0 only, x_pm(p) = y* pm a(p) e_A + beta(p) e_br, with a(p) > 0, beta(p) = O(a(p)^2), and "
    "a(p)^2 = 6 q W_q |h_A'(P_A(q))| mu / c4(q) + O(mu^2), where c4(q) > 0. "
    "x_+ and x_- are exchanged by D(-I), and each has point group T_d. "
    "For 0 < mu < eps the reduced potential has a strict local maximum at a = 0 and strict local minima at "
    "a = pm a(p): the pitchfork is supercritical in the energy sense."
)

A0 = "test_A0_representation.py::"
A1 = "test_A1_quartic.py::"
A2C = "test_A2_certificate.py::"
A2L = "test_A2_lemma_m.py::"
A2T = "test_A2_theorem.py::"
GS1 = "Golubitsky & Schaeffer, Singularities and Groups in Bifurcation Theory, Vol. I (Springer, 1985)"
GSS2 = "Golubitsky, Stewart & Schaeffer, Singularities and Groups in Bifurcation Theory, Vol. II (Springer, 1988)"

GRAPH = {
    "Theorem A": {
        "status": THEOREM_STATUS,
        "claim": "the A2u pitchfork of STATEMENT",
        "uses": ["H0", "H1", "H2", "H3", "H4", "reduction", "branch side"],
        "corroboration": [A1 + "test_local_branch_appears_only_for_p_above_P_A",
                          A1 + "test_first_order_amplitude_law",
                          A2T + "test_amplitude_law_matches_the_located_branch",
                          A2T + "test_extremum_types_in_the_T_d_family",
                          A2T + "test_signs_of_the_reduced_equation_at_curve_points"],
    },
    # ---- (H0) smoothness, invariance, equilibrium ---------------------------------------------------------------
    "H0": {"claim": "V_p is real-analytic near (y*, P_A(q)), invariant under O_h and E(3); y* is an equilibrium",
           "uses": ["H0.distances", "H0.Oh", "H0.E3", "H0.equilibrium"]},
    "H0.distances": {"status": "VERIFIED-EXACT",
                     "claim": "the pair distances of y* are 1, sqrt2, sqrt3 (all >= 1), so V_p is analytic near y*",
                     "tests": [A2T + "test_cube_pair_distances_are_bounded_below"]},
    "H0.Oh": {"status": "VERIFIED-EXACT", "claim": "V is O_h-invariant for any pair potential; D(R) is orthogonal",
              "tests": [A0 + "test_pair_energy_is_Oh_invariant_for_any_pair_potential",
                        A0 + "test_action_is_orthogonal_and_extends_paper2_convention"]},
    "H0.E3": {"status": "STANDARD", "claim": "a pair energy depends only on pair distances, so it is E(3)-invariant",
              "ref": "definition of V"},
    "H0.equilibrium": {"status": "VERIFIED-EXACT",
                       "claim": "grad V(y*) lies in Fix(O_h) = span{e_br} (A1g has multiplicity 1); "
                                "V_b = 0 exactly when A = t(p, q)",
                       "tests": [A0 + "test_multiplicities_in_R24",
                                 A1 + "test_V_b_vanishes_exactly_at_the_equilibrium"]},
    # ---- (H1) Z2 evenness ---------------------------------------------------------------------------------------
    "H1": {"claim": "Z2 evenness: V_red(-a, mu) = V_red(a, mu), so d_a V_red = a G(a^2, mu) with G analytic",
           "uses": ["H1.character", "H1.inversion", "H1.complements", "H1.LS", "H1.analytic"]},
    "H1.character": {"status": "VERIFIED-EXACT", "claim": "D(R) e_A = chi_A2u(R) e_A for all 48 R",
                     "tests": [A0 + "test_e_A_has_A2u_character_under_all_48", A0 + "test_sigma_is_the_A2u_character"]},
    "H1.inversion": {"status": "VERIFIED-EXACT", "claim": "D(-I) e_A = -e_A and D(-I) y* = y*",
                     "tests": [A0 + "test_inversion_flips_e_A_and_fixes_the_cube"]},
    "H1.complements": {"status": "STANDARD",
                       "claim": "D(R) orthogonal => orthogonal complements of O_h-invariant subspaces are invariant; "
                                "the rigid-motion space T at the O_h-fixed y* is O_h-invariant",
                       "ref": "linear algebra; D(R) maps E(3)-orbits to E(3)-orbits",
                       "tests": [A0 + "test_action_is_orthogonal_and_extends_paper2_convention"]},
    "H1.LS": {"status": "STANDARD", "claim": "the equivariant Lyapunov-Schmidt reduction inherits the symmetry",
              "ref": GSS2,
              "tests": [A0 + "test_symmetry_forced_zeros_hold_for_any_pair_potential"]},
    "H1.analytic": {"status": "STANDARD",
                    "claim": "V_p is real-analytic in (x, p), so V_red is analytic (analytic implicit function "
                             "theorem); an odd analytic g(a, mu) equals a G(a^2, mu) with G analytic",
                    "ref": "analytic implicit function theorem; power series"},
    # ---- (H2) one-dimensional kernel modulo rigid motions ---------------------------------------------------------
    "H2": {"claim": "at p = P_A(q): ker Hess V_p(y*) = T + span{e_A}",
           "uses": ["H2.multiplicity", "H2.eigenvector", "H2.V_aa", "H2.rigid", "H2.Theorem 4'"]},
    "H2.multiplicity": {"status": "VERIFIED-EXACT",
                        "claim": "A2u has multiplicity 1 in Gamma_24; its isotypic component is span{e_A}",
                        "tests": [A0 + "test_multiplicities_in_R24", A0 + "test_A2u_isotypic_component_is_span_e_A"]},
    "H2.eigenvector": {"status": "VERIFIED-EXACT", "claim": "H e_A = V_aa e_A for any pair potential",
                       "tests": [A1 + "test_e_A_and_e_br_are_hessian_eigenvectors"]},
    "H2.V_aa": {"status": "VERIFIED-EXACT",
                "claim": "V_aa = q W_q [h_A(p) - h_A(q)] at the equilibrium; h_A is Paper 2's",
                "tests": [A1 + "test_V_aa_is_paper2_A2u_block", A1 + "test_difference_form_at_the_equilibrium",
                          A1 + "test_g_functions_closed_forms"]},
    "H2.rigid": {"status": "VERIFIED-EXACT", "claim": "translations and rotations lie in the kernel at the equilibrium",
                 "tests": [A1 + "test_translations_in_kernel_for_any_pair_potential",
                           A1 + "test_rotations_in_kernel_only_at_equilibrium"]},
    "H2.Theorem 4'": {"status": "FROZEN INPUT", "paper2": "Theorem 4′",
                      "claim": "on p = P_A(q), 0 < q < r*, the only zero modes besides the rigid motions are A2u; "
                               "the two curves never meet"},
    # ---- (H3) transversality ------------------------------------------------------------------------------------
    "H3": {"claim": "transversality: lambda'(0) = q W_q h_A'(P_A(q)) < 0", "uses": ["H3.identity", "Lemma A"]},
    "H3.identity": {"status": "VERIFIED-EXACT",
                    "claim": "lambda(mu) = V_aa = q W_q [h_A(P_A(q) + mu) - h_A(q)] exactly for every p, because "
                             "e_A is an exact eigenvector; so lambda(0) = 0 and lambda'(0) = q W_q h_A'(P_A(q))",
                    "tests": [A1 + "test_difference_form_at_the_equilibrium",
                              A1 + "test_e_A_and_e_br_are_hessian_eigenvectors"],
                    "corroboration": [A1 + "test_transversality_on_the_curve"]},
    "Lemma A": {"status": "FROZEN INPUT", "paper2": "Lemma A",
                "claim": "h_A has a unique maximum at r*, increases on (0, r*) from h_A(0+) = -6/7, decreases "
                         "strictly on (r*, inf); P_A(q) > r* is the unique p > r* with h_A(p) = h_A(q)"},
    # ---- (H4) c4 > 0 (Corollary M) ------------------------------------------------------------------------------
    "H4": {"claim": "c4(q) > 0 for every q in (0, r*) (Corollary M)",
           "uses": ["H4.LS formula", "H4.b", "H4.closed forms", "H4.scale-free", "Proposition A", "Lemma M",
                    "Lemma A", "H4.P_A bound"]},
    "H4.LS formula": {"status": "STANDARD",
                      "claim": "c4 = V_aaaa - 3 <b, H_perp^-1 b>, b = D^3 V[e_A, e_A, .] (quartic coefficient of the "
                               "Lyapunov-Schmidt reduced function)",
                      "ref": GS1,
                      "corroboration": [A1 + "test_c4_by_the_24D_numeric_route"]},
    "H4.b": {"status": "VERIFIED-EXACT",
             "claim": "b = V_aab e_br and H e_br = V_bb e_br, so <b, H_perp^-1 b> = V_aab^2 / V_bb",
             "tests": [A1 + "test_b_vector_lies_in_the_breathing_direction",
                       A1 + "test_e_A_and_e_br_are_hessian_eigenvectors"]},
    "H4.closed forms": {"status": "VERIFIED-EXACT",
                        "claim": "V_bb, V_aab, V_aaaa = q W_q [g(p) - g(q)] with the closed forms g_B, g_3, g_4",
                        "tests": [A1 + "test_difference_form_at_the_equilibrium", A1 + "test_g_functions_closed_forms",
                                  A1 + "test_V_bb_is_paper2_A1g_block"]},
    "H4.scale-free": {"status": "VERIFIED-EXACT",
                      "claim": "on the curve c4 = (16/3) q W_q [m(p) - m(q)] (foliation lemma, scale-free chain, "
                               "series coefficients of the T_d family); m is the V0.1-dev closed form",
                      "uses": ["Proposition A"],
                      "tests": [A1 + "test_generic_foliation_lemma", A1 + "test_scale_free_chain_constant",
                                A1 + "test_scale_free_series_coefficients", A2L + "test_closed_form_is_the_V01_m"],
                      "corroboration": [A1 + "test_full_energy_and_scale_free_c4_agree_on_curve",
                                        A1 + "test_the_two_c4_formulas_differ_off_the_curve"]},
    "Proposition A": {"status": "FROZEN INPUT", "paper2": "Proposition A",
                      "claim": "V_* = -K Phi^(1/(p-q)) (scale elimination)"},
    "Lemma M": {"status": "CERTIFIED",
                "claim": "m'(r) >= L_min = 161457/262144 > 0 on [0, 16/5] (Arb certificate, independent checker)",
                "tests": [A2C + "test_fresh_certificate_passes_the_independent_checker",
                          A2C + "test_stored_certificate_passes_and_matches_the_hash_file",
                          A2C + "test_coverage_is_gap_free_with_exact_rational_endpoints",
                          A2C + "test_every_lower_bound_is_strictly_positive",
                          A2L + "test_m_prime_formula_by_an_independent_derivation",
                          A2L + "test_m_second_formula_by_an_independent_derivation",
                          A2L + "test_closed_form_has_no_division_by_r",
                          A2L + "test_m_prime_at_zero_exact_and_positive",
                          A2L + "test_near_zero_initial_interval_certified"],
                "corroboration": [A2C + "test_every_box_reconstructed_by_sampling",
                                  A1 + "test_m_is_increasing_on_the_curve_range_numerical"]},
    "H4.P_A bound": {"status": "CERTIFIED",
                     "claim": "h_A(16/5) < -6/7 and h_A'(16/5) < 0; with Lemma A, q < r* < P_A(q) < 16/5",
                     "uses": ["Lemma A"],
                     "tests": [A2L + "test_P_A_below_16_over_5_inputs_certified"],
                     "corroboration": [A2L + "test_m_increment_on_the_curve_dominates_the_certified_bound"]},
    # ---- reduction and the branch side --------------------------------------------------------------------------
    "reduction": {"claim": "equilibria in the slice near y* <-> zeros of d_a V_red; the solution w lies in "
                           "Fix(T_d) ∩ e_A^perp = span{e_br}",
                  "uses": ["reduction.slice", "reduction.LS", "reduction.Fix"]},
    "reduction.slice": {"status": "STANDARD",
                        "claim": "for E(3)-invariant V, critical points of V restricted to the slice y* + T^perp "
                                 "near y* are equilibria, and conversely",
                        "ref": "slice argument; e.g. " + GSS2},
    "reduction.LS": {"status": "STANDARD", "claim": "Lyapunov-Schmidt reduction with parameter (implicit function "
                                                    "theorem); the solution w(a, mu) is unique and O_h-equivariant",
                     "ref": GS1 + "; " + GSS2},
    "reduction.Fix": {"status": "VERIFIED-EXACT",
                      "claim": "the stabiliser of e_A is T_d, and Fix(T_d) = span{e_br, e_A}",
                      "tests": [A0 + "test_stabilizer_of_e_A_is_T_d_computed",
                                A0 + "test_fix_of_stabilizer_is_span_breathing_and_A2u"]},
    "branch side": {"status": "VERIFIED-EXACT",
                    "claim": "G(0,0) = 0, G_mu = lambda'(0) < 0, G_s = c4/6 > 0 => the nontrivial zeros form one "
                             "curve mu = mu*(s), mu*'(0) = -c4/(6 lambda'(0)) > 0, so a^2 > 0 forces mu > 0; on it "
                             "d^2 V_red/da^2 = 2 a^2 G_s = -2 lambda(mu) + O(mu^2) > 0, and at a = 0 it is "
                             "lambda(mu) < 0",
                    "uses": ["H3", "H4", "IFT"],
                    "tests": [A2T + "test_branch_side_from_the_reduced_equation",
                              A2T + "test_second_derivatives_of_the_reduced_potential"]},
    "IFT": {"status": "STANDARD", "claim": "implicit function theorem; Z2 pitchfork recognition",
            "ref": GS1},
}


def leaves():
    return {k: v for k, v in GRAPH.items() if "status" in v and v["status"] in LEAF_STATUSES}


def closure(node="Theorem A"):
    """All nodes reachable from node through 'uses' (node included)."""
    seen, stack = set(), [node]
    while stack:
        n = stack.pop()
        if n in seen:
            continue
        seen.add(n)
        stack.extend(GRAPH[n].get("uses", []))
    return seen


def as_record():
    return {"theorem": "Theorem A (EIT-LJ Cube Bifurcations, Paper 3)", "status": THEOREM_STATUS,
            "statement": STATEMENT, "leaf_statuses": list(LEAF_STATUSES), "graph": GRAPH}
