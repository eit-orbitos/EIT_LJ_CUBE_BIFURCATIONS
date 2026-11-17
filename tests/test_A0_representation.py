"""Phase A0 — one test per identity of the exact A2u representation audit."""
import random
from fractions import Fraction

import sympy as sp

from cube_bif.group import (CHARACTERS, D24, INDEX, LABELS, average, character, element_type, oh_matrices,
                            point_group_label, projector, sigma, type_counts)
from cube_bif.modes import E_A, E_BR, ROTATIONS, TRANSLATIONS, Y_STAR
from cube_bif import a2u

G = oh_matrices()
INV = sp.ImmutableMatrix(-sp.eye(3))


def ip(u, v):
    return (u.T * v)[0, 0]


def test_oh_is_a_group_of_48_signed_permutations():
    keys = {tuple(R) for R in G}
    assert len(keys) == 48
    assert all(tuple(A * B) in keys for A in G for B in G)
    assert all(R.T * R == sp.eye(3) for R in G)


def test_class_sizes_match_character_table():
    counts = type_counts(G)
    assert counts == {"C2'": 6, "C3": 8, "C4": 6, "C4^2": 3, "E": 1, "S4": 6, "S6": 8, "i": 1, "sigma_d": 6,
                      "sigma_h": 3}
    # row orthogonality of the stored character table
    for a in CHARACTERS:
        for b in CHARACTERS:
            s = sum(character(a, R) * character(b, R) for R in G)
            assert s == (48 if a == b else 0)


def test_action_is_orthogonal_and_extends_paper2_convention():
    for R in G:
        D = D24(R)
        assert D.T * D == sp.eye(24)
        assert D * Y_STAR == Y_STAR                       # every element fixes the cube
    # for diagonal R this is Paper 2's D2h action (g.Y)_s = R y_{R s}
    x = sp.Matrix(sp.symbols("x0:24"))
    for R in G:
        if R.is_diagonal():
            lhs = D24(R) * x
            for s in LABELS:
                t = tuple(int(c) for c in R * sp.Matrix(s))
                assert lhs[3 * INDEX[s]:3 * INDEX[s] + 3, 0] == R * x[3 * INDEX[t]:3 * INDEX[t] + 3, 0]


def test_multiplicities_in_R24():
    mult = {ir: int(projector(ir).trace()) // CHARACTERS[ir][0] for ir in CHARACTERS}
    assert mult == {"A1g": 1, "A2g": 0, "Eg": 1, "T1g": 1, "T2g": 2, "A1u": 0, "A2u": 1, "Eu": 1, "T1u": 2, "T2u": 1}


def test_e_A_norm():
    assert ip(E_A, E_A) == 24


def test_e_A_orthogonal_to_translations():
    assert all(ip(E_A, t) == 0 for t in TRANSLATIONS)


def test_e_A_orthogonal_to_rotations():
    assert all(ip(E_A, r) == 0 for r in ROTATIONS)


def test_e_A_radial_and_orthogonal_to_uniform_scaling():
    assert ip(E_A, E_BR) == 0
    for i, s in enumerate(LABELS):
        assert sp.Matrix(E_A[3 * i:3 * i + 3]) == (s[0] * s[1] * s[2]) * sp.Matrix(s)


def test_e_A_has_A2u_character_under_all_48():
    for R in G:
        assert D24(R) * E_A == character("A2u", R) * E_A


def test_sigma_is_the_A2u_character():
    assert all(sigma(R) == character("A2u", R) for R in G)


def test_A2u_isotypic_component_is_span_e_A():
    P = projector("A2u")
    assert P.rank() == 1 and P * E_A == E_A


def test_stabilizer_of_e_A_is_T_d_computed():
    S = [R for R in G if D24(R) * E_A == E_A]
    assert len(S) == 24
    assert type_counts(S) == {"C3": 8, "C4^2": 3, "E": 1, "S4": 6, "sigma_d": 6}
    assert point_group_label(S) == "T_d"
    assert INV not in S


def test_fix_of_stabilizer_is_span_breathing_and_A2u():
    S = [R for R in G if D24(R) * E_A == E_A]
    P = average(S, D24)
    assert P.rank() == 2 and P * E_A == E_A and P * E_BR == E_BR


def test_inversion_flips_e_A_and_fixes_the_cube():
    assert D24(INV) * E_A == -E_A
    assert D24(INV) * Y_STAR == Y_STAR


def test_pair_energy_is_Oh_invariant_for_any_pair_potential():
    """For a random rational configuration x and every R, the multiset of squared pair distances of D(R)x equals
    that of x; hence V(D(R)x) = V(x) for every pair potential."""
    rnd = random.Random(7)
    x = [Fraction(rnd.randint(-50, 50), rnd.randint(1, 9)) for _ in range(24)]

    def d2(v):
        out = []
        for i in range(8):
            for j in range(i + 1, 8):
                out.append(sum((v[3 * i + c] - v[3 * j + c]) ** 2 for c in range(3)))
        return sorted(out)

    base = d2(x)
    xs = sp.Matrix([sp.Rational(c.numerator, c.denominator) for c in x])
    for R in G:
        y = D24(R) * xs
        assert d2([Fraction(int(sp.fraction(c)[0]), int(sp.fraction(c)[1])) for c in y]) == base


def test_symmetry_forced_zeros_hold_for_any_pair_potential():
    f = a2u.forms()
    for k in ("V_a", "V_ab", "V_aaa", "V_abb"):
        assert f[k] == 0, k


def test_element_types_cover_all_classes():
    assert {element_type(R) for R in G} == set(["E", "C3", "C2'", "C4", "C4^2", "i", "S4", "S6", "sigma_h",
                                                "sigma_d"])
