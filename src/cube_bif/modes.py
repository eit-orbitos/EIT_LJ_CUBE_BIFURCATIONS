"""Exact displacement fields at the unit-edge cube y*_s = s/2 (unnormalised, integer entries).

E_BR(s) = s                       breathing (uniform radial scaling); y* = E_BR / 2, |E_BR|^2 = 24
E_A(s)  = (s1 s2 s3) s            A2u: radial, sign alternating between the two inscribed tetrahedra, |E_A|^2 = 24
T_k(s)  = eps_k                   translations
R_k(s)  = eps_k x s               infinitesimal rotations about the centre
U_k(s)  = (s1 s2 s3) eps_k        T2g copy 1 (A2u (x) T1u): the two tetrahedra translate oppositely
W_k(s)  = S_k s                   T2g copy 2 (T1u (x) T1u): S_1 = E23 + E32, S_2 = E13 + E31, S_3 = E12 + E21

Unit vectors: e_A = E_A / sqrt(24), e_br = E_BR / sqrt(24), U_k / sqrt(8), W_k / 4.
"""
import sympy as sp

from .group import field, LABELS

def parity(s):
    return s[0] * s[1] * s[2]


E_BR = field(lambda s: s)
E_A = field(lambda s: [parity(s) * c for c in s])
Y_STAR = E_BR / 2
TRANSLATIONS = [field(lambda s, k=k: [1 if j == k else 0 for j in range(3)]) for k in range(3)]


def _cross(k, s):
    e = [0, 0, 0]
    e[k] = 1
    return [e[1] * s[2] - e[2] * s[1], e[2] * s[0] - e[0] * s[2], e[0] * s[1] - e[1] * s[0]]


ROTATIONS = [field(lambda s, k=k: _cross(k, s)) for k in range(3)]
U_T2G = [field(lambda s, k=k: [parity(s) if j == k else 0 for j in range(3)]) for k in range(3)]
_S = [sp.Matrix([[0, 0, 0], [0, 0, 1], [0, 1, 0]]), sp.Matrix([[0, 0, 1], [0, 0, 0], [1, 0, 0]]),
      sp.Matrix([[0, 1, 0], [1, 0, 0], [0, 0, 0]])]
W_T2G = [field(lambda s, k=k: list(_S[k] * sp.Matrix(s))) for k in range(3)]

NORM2 = {"E_BR": 24, "E_A": 24, "U": 8, "W": 16}


def unit(v):
    return v / sp.sqrt((v.T * v)[0, 0])


__all__ = ["E_BR", "E_A", "Y_STAR", "TRANSLATIONS", "ROTATIONS", "U_T2G", "W_T2G", "parity", "unit", "LABELS"]
