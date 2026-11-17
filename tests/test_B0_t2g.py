"""Phase B0 — one test per identity of the T2g reconnaissance."""
import mpmath as mp
import pytest
import sympy as sp

from cube_bif import numeric as nm, paper2_ref, t2g
from cube_bif import pairsum as ps
from cube_bif.group import D24, element_type, oh_matrices, normalizer, point_group_label, projector, sigma

mp.mp.dps = 40
G = oh_matrices()
MATS = [t2g.T3(R) for R in G]


@pytest.fixture(scope="module")
def H():
    return ps.hessian()


def test_basis_spans_the_T2g_isotypic_component():
    P = projector("T2g")
    B = sp.Matrix.hstack(*(t2g.UH + t2g.VH))
    assert P.rank() == 6 and all(P * v == v for v in t2g.UH + t2g.VH)
    assert sp.simplify(B.T * B) == sp.eye(6)


def test_both_copies_transform_by_sigma_R_times_R():
    for R in G:
        assert t2g.rep_matrix_in(t2g.UH, R) == sigma(R) * R
        assert t2g.rep_matrix_in(t2g.VH, R) == sigma(R) * R


def test_critical_basis_transforms_by_sigma_R_for_any_null_vector():
    cb = t2g.critical_basis()
    for R in G:
        for k in range(3):
            img = sum((t2g.T3(R)[j, k] * cb[j] for j in range(3)), sp.zeros(24, 1))
            assert sp.simplify(D24(R) * cb[k] - img) == sp.zeros(24, 1)


def test_hessian_block_is_k_independent_and_uncoupled(H):
    Ks = t2g.block_K(H)
    assert all(sp.simplify(Ks[0] - K) == sp.zeros(2) for K in Ks)
    for j in range(3):
        for k in range(3):
            if j != k:
                for x in (t2g.UH[j], t2g.VH[j]):
                    for y in (t2g.UH[k], t2g.VH[k]):
                        assert sp.expand((x.T * H * y)[0, 0]) == 0


def test_hessian_block_equals_paper2_lemma_T0(H):
    al = {k: 2 * ps.PSI[(1, k)] + 4 * k * ps.PSI[(2, k)] for k in (1, 2, 3)}
    be = {k: 2 * ps.PSI[(1, k)] for k in (1, 2, 3)}
    a1, a2, a3, b1, b2, b3 = al[1], al[2], al[3], be[1], be[2], be[3]
    Kc = sp.Matrix([[2 * b1 + 2 * a2 + 2 * b2 + sp.Rational(4, 3) * a3 + sp.Rational(2, 3) * b3,
                     2 * sp.sqrt(2) / 3 * (a3 - b3)],
                    [2 * sp.sqrt(2) / 3 * (a3 - b3), 2 * a1 + 4 * b1 + sp.Rational(2, 3) * a3 + sp.Rational(4, 3) * b3]])
    assert sp.simplify(t2g.block_K(H)[2] - Kc) == sp.zeros(2)


def test_block_factorises_through_paper2_M(H):
    K = t2g.block_K(H)[2].subs(ps.two_term())
    rhs = ps.q_ * ps.W("q") * (t2g.M_paper2(ps.p_, ps.X["p"], ps.Y["p"]) - t2g.M_paper2(ps.q_, ps.X["q"], ps.Y["q"]))
    assert sp.simplify(K - rhs) == sp.zeros(2)


@pytest.mark.parametrize("qq", ["0.25", "1.0", "1.9", "2.0"])
def test_critical_vectors_are_in_the_kernel_on_P_T(qq):
    pt = t2g.P_T(qq)
    n = t2g.null_vector(pt, mp.mpf(qq))
    Hn = nm.PairEnergy(pt, mp.mpf(qq)).hessian(nm.y_star())
    for k in range(3):
        e = [n[0] * mp.mpf(sp.N(t2g.UH[k][i], 50)) + n[1] * mp.mpf(sp.N(t2g.VH[k][i], 50)) for i in range(24)]
        He = [mp.fsum(Hn[i, j] * e[j] for j in range(24)) for i in range(24)]
        assert mp.sqrt(mp.fsum(c * c for c in He)) < mp.mpf(10) ** -30


def test_P_T_matches_paper2_code():
    cit = paper2_ref.load_analysis("cube_index_theorem")
    if cit is None:
        pytest.skip("frozen Paper 2 archive not available")
    for qq in ("0.25", "1.0", "1.5", "2.0"):
        assert abs(t2g.P_T(qq) - cit.P_T(float(qq))) < 1e-11


def test_cubic_invariant_I3_is_invariant():
    for T in MATS:
        img = T * sp.Matrix(t2g.A)
        assert sp.expand(t2g.I3.subs(dict(zip(t2g.A, list(img))), simultaneous=True) - t2g.I3) == 0


def test_invariant_dimensions():
    assert [t2g.invariant_dimension(d, MATS) for d in (1, 2, 3, 4)] == [0, 1, 1, 2]


def test_representation_kernel_is_E_and_inversion():
    assert sorted(element_type(R) for R in G if t2g.T3(R) == sp.eye(3)) == ["E", "i"]


def test_image_of_the_representation_is_tetrahedral():
    img = {tuple(T) for T in MATS}
    assert len(img) == 24
    labels = point_group_label([sp.ImmutableMatrix(3, 3, list(t)) for t in img])
    assert labels == "T_d"


@pytest.fixture(scope="module")
def table():
    return t2g.isotropy_table()


def test_isotropy_types_and_fixed_dimensions(table):
    summary = sorted({(r["label"], r["order"], r["fix_dim"]) for r in table})
    assert summary == sorted([("D3d", 12, 1), ("D2h (axes: 1 coordinate + 2 face-diagonal)", 8, 1),
                              ("C2h (face-diagonal axis)", 4, 2), ("Ci", 2, 3)])
    counts = {}
    for r in table:
        counts[r["label"]] = counts.get(r["label"], 0) + 1
    assert counts == {"D3d": 4, "D2h (axes: 1 coordinate + 2 face-diagonal)": 3, "C2h (face-diagonal axis)": 6,
                      "Ci": 1}


def test_axial_directions_and_their_stabilizers():
    for v, label in (((1, 1, 1), "D3d"), ((1, 0, 0), "D2h (axes: 1 coordinate + 2 face-diagonal)")):
        S = t2g.stabilizer(v)
        assert point_group_label(S) == label and t2g.fix_dimension(S) == 1


def test_110_is_not_axial():
    S = t2g.stabilizer((1, 1, 0))
    assert point_group_label(S) == "C2h (face-diagonal axis)" and t2g.fix_dimension(S) == 2


def test_normalizer_actions_on_fixed_lines():
    for v, expect in (((1, 1, 1), [1]), ((1, 0, 0), [-1, 1])):
        S = t2g.stabilizer(v)
        N = normalizer(S)
        w = sp.Matrix(v)
        acts = sorted({int(((t2g.T3(g) * w).T * w)[0, 0] / (w.T * w)[0, 0]) for g in N})
        assert acts == expect
    assert point_group_label(normalizer(t2g.stabilizer((1, 1, 1)))) == "D3d"
    assert point_group_label(normalizer(t2g.stabilizer((1, 0, 0)))) == "D4h"


def test_branch_types_from_invariant_and_normalizer(table):
    for r in table:
        if r["fix_dim"] != 1:
            continue
        if r["label"] == "D3d":
            assert r["I3_on_axis"] != 0 and r["normalizer_action_on_Fix"] == [1]
            assert r["branch_type"].startswith("transcritical-type")
        else:
            assert r["I3_on_axis"] == 0 and -1 in r["normalizer_action_on_Fix"]
            assert r["branch_type"].startswith("pitchfork-type")


def test_24D_stabilisers_equal_3x3_stabilisers():
    n_u, n_v = sp.symbols("n_u n_v", positive=True)
    cb = t2g.critical_basis(n_u, n_v)
    for v in [(1, 0, 0), (1, 1, 1), (1, 1, 0), (2, 1, 0)]:
        w = sum((v[k] * cb[k] for k in range(3)), sp.zeros(24, 1))
        S24 = {tuple(R) for R in G if sp.simplify(D24(R) * w - w) == sp.zeros(24, 1)}
        assert S24 == {tuple(R) for R in t2g.stabilizer(v)}
