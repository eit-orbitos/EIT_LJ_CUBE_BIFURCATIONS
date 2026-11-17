"""Phase B0: T2g reconnaissance — critical eigenspace, 3x3 representation, cubic invariant, isotropy and normalisers.

T2g occurs twice in R^24. Orthonormal, equivariantly matched bases of the two copies (k = 1, 2, 3):
    uh_k = -W_k / 4,    vh_k = -(sqrt2/4) U_k
(for k = 3 these are Paper 2's u, v of Lemma T0, analysis/t2g_block.py). By Schur's lemma the Hessian acts on
span{uh_k, vh_k} by one 2x2 matrix K, the same for every k, with no coupling between different k. On the T2g curve
p = P_T(q) (det K = 0) the critical eigenspace is span{e_k}, e_k = n_u uh_k + n_v vh_k, n = (n_u, n_v) in ker K.
"""
import itertools

import mpmath as mp
import sympy as sp

from . import pairsum as ps
from .group import oh_matrices, D24, sigma, point_group_label, type_counts, normalizer
from .modes import U_T2G, W_T2G

UH = [-w / 4 for w in W_T2G]
VH = [-sp.sqrt(2) / 4 * u for u in U_T2G]
nu, nv = sp.symbols("n_u n_v")
a1, a2, a3 = sp.symbols("a1 a2 a3")
A = (a1, a2, a3)
I3 = a1 * a2 * a3


def critical_basis(n_u=nu, n_v=nv):
    return [n_u * UH[k] + n_v * VH[k] for k in range(3)]


def rep_matrix_in(basis, R):
    """T(R) with D(R) basis_k = sum_j T_jk basis_j, for an orthonormal (or orthogonal) basis; exact."""
    D = D24(R)
    T = sp.zeros(3)
    for k in range(3):
        img = D * basis[k]
        for j in range(3):
            T[j, k] = sp.simplify((basis[j].T * img)[0, 0] / (basis[j].T * basis[j])[0, 0])
    return T


def T3(R):
    """The 3x3 matrix of R on the T2g critical space (claim, verified in tests: sigma(R) R)."""
    return sigma(R) * R


# ---- Hessian block (Lemma T0 of Paper 2, recomputed) ------------------------------------------------------------
def block_K(H=None):
    H = ps.hessian() if H is None else H
    out = []
    for k in range(3):
        bk = [UH[k], VH[k]]
        out.append(sp.Matrix(2, 2, lambda i, j: sp.simplify((bk[i].T * H * bk[j])[0, 0])))
    return out


def M_paper2(rr, X_, Y_):
    """Paper 2's M(r) (analysis/t2g_block.py), with X_ = 2^(-r/2), Y_ = 3^(-r/2)."""
    Wr = 1 + X_ + Y_ / 3
    return sp.Matrix([[rr * X_ + 2 * (2 * rr + 1) / 9 * Y_ - 2, 2 * sp.sqrt(2) * (rr + 2) / 9 * Y_],
                      [2 * sp.sqrt(2) * (rr + 2) / 9 * Y_, 2 * rr + 2 * (rr - 1) / 9 * Y_ - 2]]) / Wr


def M_num(rr):
    rr = mp.mpf(rr)
    X_, Y_ = mp.power(2, -rr / 2), mp.power(3, -rr / 2)
    Wr = 1 + X_ + Y_ / 3
    s2 = mp.sqrt(2)
    return mp.matrix([[rr * X_ + 2 * (2 * rr + 1) / 9 * Y_ - 2, 2 * s2 * (rr + 2) / 9 * Y_],
                      [2 * s2 * (rr + 2) / 9 * Y_, 2 * rr + 2 * (rr - 1) / 9 * Y_ - 2]]) / Wr


def P_T(qq):
    """Unique p > q with det[M(p) - M(q)] = 0 (Paper 2, Lemma T3), 0 < q < q_c: scan for the sign change, refine."""
    qq = mp.mpf(qq)
    D = lambda t: mp.det(M_num(t) - M_num(qq))
    grid = [qq + mp.mpf(k) / 400 * 8 for k in range(1, 401)]
    vals = [D(t) for t in grid]
    hits = [i for i in range(len(grid) - 1) if vals[i] > 0 >= vals[i + 1]]
    if len(hits) != 1:
        raise ArithmeticError(f"P_T({qq}): {len(hits)} sign changes")
    i = hits[0]
    return mp.findroot(D, (grid[i], grid[i + 1]), solver="anderson")


def null_vector(pp, qq):
    K = M_num(pp) - M_num(qq)
    n = mp.matrix([K[0, 1], -K[0, 0]])
    return n / mp.norm(n)


# ---- invariants ---------------------------------------------------------------------------------------------------
def monomials(deg):
    return [a1 ** i * a2 ** j * a3 ** (deg - i - j) for i in range(deg + 1) for j in range(deg + 1 - i)]


def reynolds(poly, mats):
    vec = sp.Matrix(A)
    tot = 0
    for T in mats:
        img = T * vec
        tot += poly.subs({a1: img[0], a2: img[1], a3: img[2]}, simultaneous=True)
    return sp.expand(tot / len(mats))


def invariant_dimension(deg, mats):
    imgs = [sp.Poly(reynolds(mn, mats), *A) for mn in monomials(deg)]
    basis = monomials(deg)
    rows = [[im.coeff_monomial(b) for b in basis] for im in imgs]
    return sp.Matrix(rows).rank()


# ---- isotropy -----------------------------------------------------------------------------------------------------
def stabilizer(v):
    v = sp.Matrix(v)
    return [R for R in oh_matrices() if T3(R) * v == v]


def fix_dimension(S):
    P = sum((T3(R) for R in S), sp.zeros(3)) / len(S)
    return P.rank()


def isotropy_table(rng=2):
    """Stabilisers of all nonzero integer vectors with entries in [-rng, rng], up to equality, with their labels,
    fixed-space dimensions, normaliser actions and the restriction of the cubic invariant."""
    seen = {}
    for v in itertools.product(range(-rng, rng + 1), repeat=3):
        if v == (0, 0, 0):
            continue
        S = stabilizer(v)
        key = frozenset(tuple(R) for R in S)
        seen.setdefault(key, {"subgroup": S, "vectors": []})["vectors"].append(v)
    rows = []
    for key, rec in seen.items():
        S = rec["subgroup"]
        dim = fix_dimension(S)
        row = {"order": len(S), "label": point_group_label(S), "types": type_counts(S), "fix_dim": dim,
               "representative": min(rec["vectors"], key=lambda w: (sum(abs(c) for c in w), [-c for c in w])),
               "n_vectors": len(rec["vectors"])}
        if dim == 1:
            v = sp.Matrix(row["representative"])
            N = normalizer(S)
            acts = sorted({int(((T3(g) * v).T * v)[0, 0] / (v.T * v)[0, 0]) for g in N})
            row.update({"normalizer_order": len(N), "normalizer_label": point_group_label(N),
                        "normalizer_action_on_Fix": acts,
                        "I3_on_axis": int(I3.subs(dict(zip(A, row["representative"]))))})
            if -1 in acts:
                row["branch_type"] = "pitchfork-type (an element of N(Sigma) acts as -1 on Fix: reduced equation odd)"
            elif row["I3_on_axis"] != 0:
                row["branch_type"] = ("transcritical-type when the cubic coefficient kappa != 0 "
                                      "(N(Sigma)/Sigma acts trivially; I3 != 0 on the axis)")
            else:
                row["branch_type"] = "undetermined at cubic order"
        rows.append(row)
    return sorted(rows, key=lambda w: (-w["order"], w["label"]))
