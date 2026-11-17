"""The octahedral group O_h acting on labelled 8-particle configurations, in the convention of frozen Paper 2.

Labels s in {-1, 1}^3, ordered as itertools.product([-1, 1], repeat=3) (Paper 2: geometry.SIGNS).
Unit-edge cube: y*_s = s/2. A configuration is x in R^24, x = (x_s)_s with x_s in R^3, label-major order.
O_h = the 48 signed permutation matrices R, acting by

    (D(R) x)_{R s} = R x_s,   i.e.   (D(R) x)_s = R x_{R^{-1} s}

(Paper 2: analysis/cube_oh_decomposition.py, D(R); for diagonal R this is the D2h action of
src/eit_lj_stability/symmetry.py). Everything here is exact integer arithmetic.
"""
import itertools
from functools import lru_cache

import sympy as sp

LABELS = list(itertools.product([-1, 1], repeat=3))
INDEX = {s: i for i, s in enumerate(LABELS)}


@lru_cache(maxsize=None)
def oh_matrices():
    """The 48 elements of O_h as immutable 3x3 integer matrices (same enumeration order as Paper 2)."""
    G = []
    for perm in itertools.permutations(range(3)):
        for sg in itertools.product([-1, 1], repeat=3):
            R = sp.zeros(3)
            for i in range(3):
                R[i, perm[i]] = sg[i]
            G.append(sp.ImmutableMatrix(R))
    return tuple(G)


def sigma(R):
    """Product of the three nonzero entries of a signed permutation matrix (+1 or -1)."""
    out = 1
    for i in range(3):
        for j in range(3):
            if R[i, j] != 0:
                out *= int(R[i, j])
    return out


def element_type(R):
    """Geometric type of R in O_h, from det and trace, with the O_h class refinements:
    E, C3, C2' (face-diagonal 2-fold), C4, C4^2 (= coordinate 2-fold), i, S4, S6, sigma_h, sigma_d."""
    d, t = int(R.det()), int(R.trace())
    diag = all(R[i, j] == 0 for i in range(3) for j in range(3) if i != j)
    if d == 1:
        return {3: "E", 0: "C3", 1: "C4"}.get(t) or ("C4^2" if diag else "C2'")
    return {-3: "i", 0: "S6", -1: "S4"}.get(t) or ("sigma_h" if diag else "sigma_d")


CLASSES = ["E", "C3", "C2'", "C4", "C4^2", "i", "S4", "S6", "sigma_h", "sigma_d"]
CLASS_SIZE = {"E": 1, "C3": 8, "C2'": 6, "C4": 6, "C4^2": 3, "i": 1, "S4": 6, "S6": 8, "sigma_h": 3, "sigma_d": 6}

# Standard O_h character table (Mulliken), columns in the order of CLASSES.
CHARACTERS = {
    "A1g": [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    "A2g": [1, 1, -1, -1, 1, 1, -1, 1, 1, -1],
    "Eg": [2, -1, 0, 0, 2, 2, 0, -1, 2, 0],
    "T1g": [3, 0, -1, 1, -1, 3, 1, 0, -1, -1],
    "T2g": [3, 0, 1, -1, -1, 3, -1, 0, -1, 1],
    "A1u": [1, 1, 1, 1, 1, -1, -1, -1, -1, -1],
    "A2u": [1, 1, -1, -1, 1, -1, 1, -1, -1, 1],
    "Eu": [2, -1, 0, 0, 2, -2, 0, 1, -2, 0],
    "T1u": [3, 0, -1, 1, -1, -3, -1, 0, 1, 1],
    "T2u": [3, 0, 1, -1, -1, -3, 1, 0, 1, -1],
}


def character(irrep, R):
    return CHARACTERS[irrep][CLASSES.index(element_type(R))]


def act_label(R, s):
    """The label R s."""
    v = R * sp.Matrix(s)
    return tuple(int(c) for c in v)


@lru_cache(maxsize=None)
def D24(R):
    """24x24 integer matrix of R acting on configurations: (D(R) x)_{R s} = R x_s."""
    M = sp.zeros(24)
    for s in LABELS:
        t = act_label(R, s)
        M[3 * INDEX[t]:3 * INDEX[t] + 3, 3 * INDEX[s]:3 * INDEX[s] + 3] = R
    return sp.ImmutableMatrix(M)


def field(f):
    """24-vector (sympy column) of the displacement field s -> f(s) (f returns a 3-sequence)."""
    return sp.Matrix([c for s in LABELS for c in f(s)])


def as_field(x):
    """Inverse of field(): list of eight 3-vectors in label order."""
    return [sp.Matrix(x[3 * i:3 * i + 3]) for i in range(8)]


def projector(irrep):
    """Isotypic projector P = (d/48) sum_R chi(R) D(R) on R^24 (exact rationals)."""
    d = CHARACTERS[irrep][0]
    P = sp.zeros(24)
    for R in oh_matrices():
        P += character(irrep, R) * D24(R)
    return P * sp.Rational(d, 48)


def average(subgroup, D):
    """(1/|S|) sum_{g in S} D(g): the orthogonal projector onto Fix(S) for an orthogonal action D."""
    M = None
    for g in subgroup:
        M = D(g) if M is None else M + D(g)
    return M / len(subgroup)


def type_counts(subgroup):
    out = {}
    for R in subgroup:
        k = element_type(R)
        out[k] = out.get(k, 0) + 1
    return dict(sorted(out.items()))


# Element-type signatures of the subgroups of O_h met in this project (orders 2..48). A subgroup is labelled by
# matching its computed signature; labels are never assumed.
SIGNATURES = {
    "O_h": {"E": 1, "C3": 8, "C2'": 6, "C4": 6, "C4^2": 3, "i": 1, "S4": 6, "S6": 8, "sigma_h": 3, "sigma_d": 6},
    "T_d": {"E": 1, "C3": 8, "C4^2": 3, "S4": 6, "sigma_d": 6},
    "O": {"E": 1, "C3": 8, "C2'": 6, "C4": 6, "C4^2": 3},
    "T_h": {"E": 1, "C3": 8, "C4^2": 3, "i": 1, "S6": 8, "sigma_h": 3},
    "T": {"E": 1, "C3": 8, "C4^2": 3},
    "D4h": {"E": 1, "C4": 2, "C4^2": 3, "C2'": 2, "i": 1, "S4": 2, "sigma_h": 3, "sigma_d": 2},
    "D3d": {"E": 1, "C3": 2, "C2'": 3, "i": 1, "S6": 2, "sigma_d": 3},
    "D2h (axes: 3 coordinate)": {"E": 1, "C4^2": 3, "i": 1, "sigma_h": 3},
    "D2h (axes: 1 coordinate + 2 face-diagonal)": {"E": 1, "C4^2": 1, "C2'": 2, "i": 1, "sigma_h": 1, "sigma_d": 2},
    "C2h (coordinate axis)": {"E": 1, "C4^2": 1, "i": 1, "sigma_h": 1},
    "C2h (face-diagonal axis)": {"E": 1, "C2'": 1, "i": 1, "sigma_d": 1},
    "C3v": {"E": 1, "C3": 2, "sigma_d": 3},
    "C2v (coordinate axis, sigma_d mirrors)": {"E": 1, "C4^2": 1, "sigma_d": 2},
    "C2v (coordinate axis, sigma_h mirrors)": {"E": 1, "C4^2": 1, "sigma_h": 2},
    "C2v (face-diagonal axis)": {"E": 1, "C2'": 1, "sigma_h": 1, "sigma_d": 1},
    "S6": {"E": 1, "C3": 2, "i": 1, "S6": 2},
    "Ci": {"E": 1, "i": 1},
    "Cs (sigma_h)": {"E": 1, "sigma_h": 1},
    "Cs (sigma_d)": {"E": 1, "sigma_d": 1},
    "C1": {"E": 1},
}


def point_group_label(subgroup):
    sig = type_counts(subgroup)
    hits = [name for name, s in SIGNATURES.items() if s == sig]
    return hits[0] if len(hits) == 1 else f"unlabelled {sig}"


def is_subgroup(S):
    keys = {tuple(R) for R in S}
    return all(tuple(A * B) in keys for A in S for B in S)


def normalizer(S):
    keys = {tuple(R) for R in S}
    out = []
    for g in oh_matrices():
        gi = g.T  # orthogonal
        if all(tuple(g * R * gi) in keys for R in S):
            out.append(g)
    return out
