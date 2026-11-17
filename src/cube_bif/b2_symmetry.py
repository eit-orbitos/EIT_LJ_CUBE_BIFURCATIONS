"""Phase B2.0: exact symmetry audit of the D2h axis of the critical T2g representation.

No structure is assumed. Every statement is computed from the O_h action D(R) on R^24 (group.py), the B0 bases
uh_k = -W_k/4, vh_k = -(sqrt2/4) U_k (t2g.py) and the exact pair-sum derivatives (pairsum.py):

1. Sigma := {R in O_h : D(R) e_1 = e_1}, e_1 = n_u uh_1 + n_v vh_1, with symbolic n_u, n_v. Its element types and
   its label come from the computed signature (group.point_group_label).
2. P_Fix = (1/|Sigma|) sum_{g in Sigma} D(g), the orthogonal projector onto Fix_{R^24}(Sigma); its rank, and the rank
   of P_Gamma P_Fix for all ten O_h irreps Gamma (exact rational matrices), cross-checked by the character formula.
3. An explicit orthonormal basis of Fix_{R^24}(Sigma) with the isotypic component of each vector, and the claimed
   basis {e_1, A1g, Eg(1), Eg(2)} relayed from the external brainstorm, tested against it.
4. b = D^3V[e_1, e_1, .] as a 24-vector of linear forms in psi^(k)(sigma) (any pair potential phi(r) = psi(r^2),
   symbolic n), its projections on all ten isotypic components and its inner products with uh_k, vh_k (k = 1, 2, 3),
   in particular <b, f_1> and <b, e_1>, where f_1 = -n_v uh_1 + n_u vh_1 is the second T2g direction in Fix.
5. The structural reason (Schur): b is the image of e_1 (x) e_1 under an O_h-equivariant map Sym^2(T2g) -> R^24, and
   the T2g component (a2 a3, a3 a1, a1 a2) of a (x) a vanishes on the axis a = (1, 0, 0).
6. An element of the normaliser acting by -1 on e_1, and its action on Fix (evenness of the axial reduced problem).
7. The same fixed space built independently from the vertex orbits of Sigma (the parametrisation used by route 3
   of B2.1).
"""
from functools import lru_cache

import sympy as sp

from . import pairsum as ps
from .group import (CHARACTERS, D24, LABELS, act_label, average, character, field, oh_matrices,
                    point_group_label, projector, sigma, type_counts)
from .modes import E_BR, U_T2G, W_T2G, unit
from .t2g import UH, VH

nu, nv = sp.symbols("n_u n_v")
S2 = sp.sqrt(2)
IRREPS = tuple(CHARACTERS)

# Eg displacement fields at the cube (strains applied to y*_s = s/2, unnormalised, integer entries)
E_TET_X = field(lambda s: [2 * s[0], -s[1], -s[2]])     # strain diag(2, -1, -1): tetragonal along x
E_ORTH_YZ = field(lambda s: [0, s[1], -s[2]])            # strain diag(0, 1, -1): the other Eg direction
NORM2 = {"E_BR": 24, "E_TET_X": 48, "E_ORTH_YZ": 16}

A_HAT = E_BR / sp.sqrt(24)          # unit A1g (breathing)
E_HAT = E_TET_X / sp.sqrt(48)       # unit Eg vector fixed by Sigma (shown in the tests)


def e1(n_u=nu, n_v=nv):
    return n_u * UH[0] + n_v * VH[0]


def f1(n_u=nu, n_v=nv):
    return -n_v * UH[0] + n_u * VH[0]


def _is_zero(v):
    return v.applyfunc(sp.expand) == sp.zeros(*v.shape)


# ---- 1. the stabiliser, computed in 24-D --------------------------------------------------------------------------
@lru_cache(maxsize=None)
def axis_stabilizer():
    """Sigma = {R in O_h : D(R) e_1 = e_1} for symbolic n (so: fixes uh_1 and vh_1 separately)."""
    v = e1()
    return tuple(R for R in oh_matrices() if _is_zero(D24(R) * v - v))


def stabilizer_record():
    S = axis_stabilizer()
    return {"order": len(S), "label": point_group_label(S), "types": type_counts(S),
            "contains_inversion": any(R == -sp.eye(3) for R in S),
            "elements": [[int(c) for c in R] for R in S]}


# ---- 2. the fixed space and its isotypic decomposition ------------------------------------------------------------
@lru_cache(maxsize=None)
def fix_projector():
    return sp.ImmutableMatrix(average(axis_stabilizer(), D24))


@lru_cache(maxsize=None)
def iso_projector(G):
    return sp.ImmutableMatrix(projector(G))


def isotypic_ranks():
    """rank(P_Gamma P_Fix) for every irrep: the dimension of Fix(Sigma) inside the Gamma-isotypic component."""
    P = fix_projector()
    return {G: int((iso_projector(G) * P).rank()) for G in IRREPS}


def character_prediction():
    """mult(Gamma, R^24) * dim Fix_Gamma(Sigma), both from characters only (no matrices of R^24 beyond traces)."""
    S = axis_stabilizer()
    out = {}
    for G in IRREPS:
        m = sp.Rational(sum(character(G, R) * D24(R).trace() for R in oh_matrices()), 48)
        f = sp.Rational(sum(character(G, R) for R in S), len(S))
        out[G] = {"multiplicity_in_R24": int(m), "dim_Fix_in_irrep": int(f), "predicted_rank": int(m * f)}
    return out


def fixed_basis(n_u=nu, n_v=nv):
    """Orthonormal basis of Fix_{R^24}(Sigma): A1g, Eg (tetragonal along x), and the two T2g copies at index 1
    (equivalently e_1 and f_1 for unit n)."""
    return {"A1g": A_HAT, "Eg": E_HAT, "T2g_u": UH[0], "T2g_v": VH[0]}


def claimed_basis_check(n_u=sp.Integer(1), n_v=sp.Rational(1, 50)):
    """The relayed claim Fix(D2h) = span{e_crit, A1g, Eg(1), Eg(2)}, tested with a rational n (any nonzero n works).
    Returns which claimed vectors are fixed and whether f_1 lies in the claimed span."""
    P = fix_projector()
    claimed = {"e_crit": e1(n_u, n_v), "A1g": A_HAT, "Eg(1) tetragonal x": E_HAT, "Eg(2) orthorhombic yz": E_ORTH_YZ}
    fixed = {k: _is_zero(P * v - v) for k, v in claimed.items()}
    M = sp.Matrix.hstack(*claimed.values())
    f = f1(n_u, n_v)
    f_in_span = sp.Matrix.hstack(M, f).rank() == M.rank()
    inter = sp.Matrix.hstack(*(P * v for v in claimed.values())).rank()
    return {"claimed_vector_is_fixed": fixed, "f1_is_fixed": _is_zero(P * f - f), "f1_in_claimed_span": f_in_span,
            "rank_of_claimed_span": int(M.rank()), "rank_of_P_Fix_applied_to_claimed": int(inter),
            "P_Fix_kills_Eg(2)": _is_zero(P * E_ORTH_YZ)}


# ---- 4. b = D^3V[e_1, e_1, .] ---------------------------------------------------------------------------------------
_DIRS = {"u": (W_T2G[0], sp.Rational(-1, 4)), "v": (U_T2G[0], -S2 / 4)}
B_CHANNELS = ("uu", "uv", "vv")


@lru_cache(maxsize=None)
def b_channels():
    """b_cc' = D^3V[c_1, c'_1, .] for cc' in uu, uv, vv: 24-vectors of linear forms in PSI (generic pair potential)."""
    out = {}
    for ch in B_CHANNELS:
        (d0, s0), (d1, s1) = _DIRS[ch[0]], _DIRS[ch[1]]
        comps = []
        for m in range(24):
            em = sp.zeros(24, 1)
            em[m] = 1
            comps.append(sp.expand(ps.derivative([d0, d1, em]) * s0 * s1))
        out[ch] = sp.ImmutableMatrix(comps)
    return out


def b_vector(n_u=nu, n_v=nv):
    bc = b_channels()
    return (n_u ** 2 * bc["uu"] + 2 * n_u * n_v * bc["uv"] + n_v ** 2 * bc["vv"]).applyfunc(sp.expand)


def b_projections(b=None):
    """P_Gamma b for all ten irreps."""
    b = b_vector() if b is None else b
    return {G: (iso_projector(G) * b).applyfunc(sp.expand) for G in IRREPS}


def t2g_inner_products():
    """<b_cc', uh_k> and <b_cc', vh_k> for all channels and k = 1, 2, 3 (expected: all zero)."""
    bc = b_channels()
    return {(ch, nm, k): sp.expand((B[k].T * bc[ch])[0, 0])
            for ch in B_CHANNELS for nm, B in (("uh", UH), ("vh", VH)) for k in range(3)}


@lru_cache(maxsize=None)
def b_components():
    """b_cc' = bA_cc' A_HAT + bE_cc' E_HAT: the two coefficients per channel (linear forms in PSI)."""
    bc = b_channels()
    return {ch: {"A1g": sp.expand((A_HAT.T * bc[ch])[0, 0]), "Eg": sp.expand((E_HAT.T * bc[ch])[0, 0])}
            for ch in B_CHANNELS}


def b_reconstruction_residual(ch):
    c = b_components()[ch]
    return (b_channels()[ch] - c["A1g"] * A_HAT - c["Eg"] * E_HAT).applyfunc(sp.expand)


# ---- 5. the Schur argument -------------------------------------------------------------------------------------------
a_sym = sp.symbols("a1:4")


def sym2_t2g_part(a):
    """The T2g component of a (x) a in Sym^2(T2g) = (A1g + Eg) + T2g: (a2 a3, a3 a1, a1 a2)."""
    return sp.Matrix([a[1] * a[2], a[2] * a[0], a[0] * a[1]])


def sym2_t2g_part_is_equivariant():
    """t(T a) = T t(a) for all 48 T = sigma(R) R (exact): so it is a T2g-type component of Sym^2."""
    a = sp.Matrix(a_sym)
    return all(_is_zero(sym2_t2g_part(sigma(R) * R * a) - sigma(R) * R * sym2_t2g_part(a)) for R in oh_matrices())


def sym2_diagonal_part_is_invariant_set():
    """(a1^2, a2^2, a3^2) is permuted by every T(R) (it spans A1g + Eg, the complement of the T2g part)."""
    a = sp.Matrix(a_sym)
    sq = lambda v: sp.Matrix([v[0] ** 2, v[1] ** 2, v[2] ** 2])
    for R in oh_matrices():
        P = R.applyfunc(abs)
        if not _is_zero(sq(sigma(R) * R * a) - P * sq(a)):
            return False
    return True


# ---- 6. normaliser element acting by -1 on the axis -------------------------------------------------------------------
def reversing_elements():
    """R in O_h with D(R) e_1 = -e_1 (symbolic n), with their action on the Fix basis (diagonal entries)."""
    v = e1()
    basis = fixed_basis()
    out = []
    for R in oh_matrices():
        if _is_zero(D24(R) * v + v):
            act = {k: sp.simplify((b_.T * D24(R) * b_)[0, 0]) for k, b_ in basis.items()}
            preserved = all(_is_zero(D24(R) * b_ - act[k] * b_) for k, b_ in basis.items())
            out.append({"R": [int(c) for c in R], "diag_action_on_Fix_basis": {k: int(x) for k, x in act.items()},
                        "Fix_basis_vectors_are_eigenvectors": preserved})
    return out


# ---- 7. the same fixed space from the vertex orbits of Sigma (route-3 parametrisation) ---------------------------------
ORBIT_REPS = {"orbit_1": (1, 1, 1), "orbit_2": (1, 1, -1)}
ORBIT_DIRS = {"a": ("orbit_1", (1, 0, 0)), "b": ("orbit_1", (0, 1, 1)),
              "c": ("orbit_2", (1, 0, 0)), "d": ("orbit_2", (0, 1, -1))}


def sigma_explicit():
    """Sigma written down directly (x special): P diag(d1, d, d) with P in {I, swap(y, z)}, d1, d = +-1."""
    swap = sp.Matrix([[1, 0, 0], [0, 0, 1], [0, 1, 0]])
    out = []
    for P in (sp.eye(3), swap):
        for d1 in (1, -1):
            for d in (1, -1):
                out.append(sp.ImmutableMatrix(P * sp.diag(d1, d, d)))
    return out


def orbit_field(rep, direction, group=None):
    """Displacement field: vertex g.rep moves by g.direction for g in Sigma (well defined: the stabiliser of rep in
    Sigma fixes direction; checked)."""
    group = sigma_explicit() if group is None else group
    disp = {}
    for g in group:
        lab = act_label(g, rep)
        img = tuple(int(c) for c in g * sp.Matrix(direction))
        if lab in disp and disp[lab] != img:
            raise ValueError("direction not fixed by the vertex stabiliser")
        disp[lab] = img
    return field(lambda s: list(disp.get(tuple(s), (0, 0, 0))))


def orbit_fields():
    return {k: orbit_field(ORBIT_REPS[o], d) for k, (o, d) in ORBIT_DIRS.items()}


def orbit_structure():
    """Vertex orbits of Sigma on the eight labels, and the stabiliser order of each representative."""
    S = axis_stabilizer()
    orbits = []
    seen = set()
    for s in LABELS:
        if s in seen:
            continue
        orb = sorted({act_label(R, s) for R in S})
        seen.update(orb)
        stab = [R for R in S if act_label(R, s) == s]
        orbits.append({"orbit": [list(x) for x in orb], "representative": list(orb[0]),
                       "stabiliser_order": len(stab)})
    return orbits


# ---- first-order geometry of the axial displacement ----------------------------------------------------------------------
def first_order_displacement(s=sp.Symbol("s")):
    """Vertex displacement of s e_1 (first order only): -(s n_u/4)(0, s3, s2) - (s n_v sqrt2/4)(s1 s2 s3)(1, 0, 0)."""
    v = s * e1()
    return [sp.Matrix(v[3 * i:3 * i + 3]) for i in range(8)]
