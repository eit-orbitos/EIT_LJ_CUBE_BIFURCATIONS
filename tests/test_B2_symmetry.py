"""Phase B2.0 — exact symmetry audit of the D2h axis of the critical T2g representation (NOTES §6.1).
Every structural statement is computed here from the O_h action on R^24; none is assumed."""
import sympy as sp

from cube_bif import b2_symmetry as s2
from cube_bif import t2g
from cube_bif.group import D24, average, field, oh_matrices, point_group_label, projector
from cube_bif.modes import ROTATIONS, TRANSLATIONS
from cube_bif.pairsum import PSI

Z24 = sp.zeros(24, 1)
S3, S6 = sp.sqrt(3), sp.sqrt(6)


def zero(v):
    return v.applyfunc(sp.expand) == sp.zeros(*v.shape)


# ---- the stabiliser ------------------------------------------------------------------------------------------------
def test_stabiliser_of_e1_computed_in_24D_is_the_face_diagonal_D2h():
    rec = s2.stabilizer_record()
    assert rec["order"] == 8 and rec["contains_inversion"]
    assert rec["label"] == "D2h (axes: 1 coordinate + 2 face-diagonal)"
    assert rec["types"] == {"E": 1, "C4^2": 1, "C2'": 2, "i": 1, "sigma_h": 1, "sigma_d": 2}


def test_stabiliser_equals_the_3x3_stabiliser_of_100_and_the_explicit_list():
    S = {tuple(R) for R in s2.axis_stabilizer()}
    assert S == {tuple(R) for R in t2g.stabilizer((1, 0, 0))}
    assert S == {tuple(R) for R in s2.sigma_explicit()}


def test_stabiliser_fixes_both_T2g_copies_separately():
    for R in s2.axis_stabilizer():
        assert D24(R) * t2g.UH[0] == t2g.UH[0] and zero(D24(R) * t2g.VH[0] - t2g.VH[0])


# ---- the fixed space -----------------------------------------------------------------------------------------------
def test_fix_projector_is_an_orthogonal_projector_of_rank_4():
    P = s2.fix_projector()
    assert P * P == P and P.T == P and P.rank() == 4


def test_isotypic_decomposition_of_the_fixed_space():
    ranks = s2.isotypic_ranks()
    assert ranks == {"A1g": 1, "A2g": 0, "Eg": 1, "T1g": 0, "T2g": 2,
                     "A1u": 0, "A2u": 0, "Eu": 0, "T1u": 0, "T2u": 0}
    assert sum(ranks.values()) == s2.fix_projector().rank() == 4


def test_character_formula_agrees_with_the_projector_ranks():
    pred = s2.character_prediction()
    assert {G: v["predicted_rank"] for G, v in pred.items()} == s2.isotypic_ranks()
    assert {G: v["multiplicity_in_R24"] for G, v in pred.items()} == {
        "A1g": 1, "A2g": 0, "Eg": 1, "T1g": 1, "T2g": 2, "A1u": 0, "A2u": 1, "Eu": 1, "T1u": 2, "T2u": 1}


def test_no_rigid_motion_in_the_fixed_space():
    P = s2.fix_projector()
    for v in TRANSLATIONS + ROTATIONS:
        assert P * v == Z24


def test_explicit_orthonormal_basis_of_the_fixed_space():
    B = s2.fixed_basis()
    P = s2.fix_projector()
    M = sp.Matrix.hstack(*B.values())
    assert sp.simplify(M.T * M) == sp.eye(4)
    irrep = {"A1g": "A1g", "Eg": "Eg", "T2g_u": "T2g", "T2g_v": "T2g"}
    for k, v in B.items():
        assert zero(P * v - v), k
        assert zero(projector(irrep[k]) * v - v), k


def test_e1_and_f1_are_both_fixed_for_every_n():
    P = s2.fix_projector()
    for v in (s2.e1(), s2.f1()):
        assert zero(P * v - v)


def test_claimed_fixed_space_from_the_brainstorm_is_not_Fix():
    """Relayed claim: Fix(D2h) = span{e_crit, A1g, Eg(1), Eg(2)}. Eg(2) is not fixed (P_Fix kills it), and the
    second T2g direction f_1 is fixed but missing from the claimed span."""
    c = s2.claimed_basis_check()
    assert c["claimed_vector_is_fixed"] == {"e_crit": True, "A1g": True, "Eg(1) tetragonal x": True,
                                            "Eg(2) orthorhombic yz": False}
    assert c["P_Fix_kills_Eg(2)"] and c["f1_is_fixed"] and not c["f1_in_claimed_span"]
    assert c["rank_of_claimed_span"] == 4 and c["rank_of_P_Fix_applied_to_claimed"] == 3


def test_fixed_eg_vector_is_the_tetragonal_strain_along_the_axis():
    P = s2.fix_projector()
    PE = projector("Eg")
    assert PE * s2.E_TET_X == s2.E_TET_X and PE * s2.E_ORTH_YZ == s2.E_ORTH_YZ
    assert P * s2.E_TET_X == s2.E_TET_X and P * s2.E_ORTH_YZ == Z24


# ---- b = D^3V[e_1, e_1, .] -------------------------------------------------------------------------------------------
def test_b_lies_in_A1g_plus_Eg_for_every_pair_potential_and_every_n():
    pr = s2.b_projections()
    for G, v in pr.items():
        if G not in ("A1g", "Eg"):
            assert v == Z24, G
    assert pr["A1g"] != Z24 and pr["Eg"] != Z24
    assert zero(pr["A1g"] + pr["Eg"] - s2.b_vector())


def test_b_has_no_component_on_any_T2g_basis_vector():
    ips = s2.t2g_inner_products()
    assert len(ips) == 18 and all(v == 0 for v in ips.values())


def test_b_is_orthogonal_to_f1_and_to_e1_exactly():
    b = s2.b_vector()
    assert sp.expand((s2.f1().T * b)[0, 0]) == 0
    assert sp.expand((s2.e1().T * b)[0, 0]) == 0


def test_b_is_exactly_bA_times_Ahat_plus_bE_times_Ehat():
    for ch in s2.B_CHANNELS:
        assert s2.b_reconstruction_residual(ch) == Z24, ch
    assert sp.expand((s2.E_ORTH_YZ.T * s2.b_vector())[0, 0]) == 0


def test_b_component_closed_forms():
    P = PSI
    c = s2.b_components()
    expect = {
        "uu": {"A1g": S6 * (4 * P[(2, 1)] + 32 * P[(2, 2)] + 28 * P[(2, 3)] + 32 * P[(3, 2)] + 48 * P[(3, 3)]) / 3,
               "Eg": -S3 * (4 * P[(2, 1)] + 20 * P[(2, 2)] + 16 * P[(2, 3)] + 32 * P[(3, 2)]) / 3},
        "uv": {"A1g": 16 * S3 * (P[(2, 3)] + 3 * P[(3, 3)]) / 3, "Eg": 4 * S6 * P[(2, 3)] / 3},
        "vv": {"A1g": S6 * (20 * P[(2, 1)] + 20 * P[(2, 3)] + 8 * P[(3, 1)] + 24 * P[(3, 3)]) / 3,
               "Eg": 16 * S3 * (P[(2, 1)] + P[(2, 3)] + P[(3, 1)]) / 3},
    }
    for ch in s2.B_CHANNELS:
        for X in ("A1g", "Eg"):
            assert sp.expand(c[ch][X] - expect[ch][X]) == 0, (ch, X)


# ---- the structural reason ------------------------------------------------------------------------------------------------
def test_schur_reason_the_T2g_part_of_a_tensor_a_vanishes_on_the_axis():
    assert s2.sym2_t2g_part_is_equivariant() and s2.sym2_diagonal_part_is_invariant_set()
    assert s2.sym2_t2g_part((1, 0, 0)) == sp.zeros(3, 1)
    assert s2.sym2_t2g_part((1, 1, 1)) != sp.zeros(3, 1)          # contrast: the D3d axis


# ---- normaliser and evenness ------------------------------------------------------------------------------------------------
def test_reversing_elements_act_as_diag_1_1_minus1_minus1_on_Fix():
    rev = s2.reversing_elements()
    assert len(rev) == 8
    for x in rev:
        assert x["Fix_basis_vectors_are_eigenvectors"]
        assert x["diag_action_on_Fix_basis"] == {"A1g": 1, "Eg": 1, "T2g_u": -1, "T2g_v": -1}
    N = {tuple(R) for R in s2.axis_stabilizer()} | {tuple(x["R"]) for x in rev}
    assert point_group_label([sp.ImmutableMatrix(3, 3, list(k)) for k in N]) == "D4h"


# ---- the same fixed space from the vertex orbits (route-3 parametrisation) -----------------------------------------------------
def test_vertex_orbits_of_sigma():
    orbs = s2.orbit_structure()
    assert len(orbs) == 2 and all(len(o["orbit"]) == 4 and o["stabiliser_order"] == 2 for o in orbs)
    parities = [{s[0] * s[1] * s[2] for s in o["orbit"]} for o in orbs]
    assert sorted(len(p) for p in parities) == [2, 2]       # each orbit meets both tetrahedra


def test_vertex_orbit_fields_span_the_fixed_space():
    P = s2.fix_projector()
    flds = s2.orbit_fields()
    assert all(zero(P * v - v) for v in flds.values())
    assert sp.Matrix.hstack(*flds.values()).rank() == 4
    G = sp.Matrix(4, 4, lambda i, j: (list(flds.values())[i].T * list(flds.values())[j])[0, 0])
    assert G == sp.diag(4, 8, 4, 8)


# ---- first-order geometry and the cuboid family --------------------------------------------------------------------------------
def test_first_order_displacement_of_the_axial_mode():
    s = sp.Symbol("s")
    disp = s2.first_order_displacement(s)
    for i, lab in enumerate(s2.LABELS):
        s1, s2_, s3 = lab
        expect = (-(s * s2.nu / 4) * sp.Matrix([0, s3, s2_])
                  - (s * s2.nv * sp.sqrt(2) / 4) * (s1 * s2_ * s3) * sp.Matrix([1, 0, 0]))
        assert sp.simplify(disp[i] - expect) == sp.zeros(3, 1)


def test_axial_mode_is_orthogonal_to_the_cuboid_family():
    """Fix(Z2^3) (the coordinate D2h of a cuboid) is A1g + Eg (Paper 2); e_1 has no component there, while
    Fix(Sigma) meets it in span{A_HAT, E_HAT}."""
    Z2 = [sp.ImmutableMatrix(sp.diag(a, b, c)) for a in (1, -1) for b in (1, -1) for c in (1, -1)]
    Pc = average(Z2, D24)
    assert Pc.rank() == 3
    assert zero(Pc * s2.e1()) and zero(Pc * s2.f1())
    assert Pc * s2.A_HAT == s2.A_HAT and Pc * s2.E_HAT == s2.E_HAT
