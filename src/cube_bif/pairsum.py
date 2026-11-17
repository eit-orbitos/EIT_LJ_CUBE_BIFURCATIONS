"""Exact multilinear derivatives of a pair energy at the unit-edge cube.

V(x) = sum_{s<s'} phi(|x_s - x_s'|) with phi(r) = psi(r^2). For one pair with base difference r and direction
differences d_j (Faa di Bruno for psi(|r + .|^2), whose inner function is quadratic):

  D^1 = 2 psi' (r.d0)
  D^2 = 4 psi'' (r.d0)(r.d1) + 2 psi' (d0.d1)
  D^3 = 8 psi''' (r.d0)(r.d1)(r.d2) + 4 psi'' [ (d0.d1)(r.d2) + (d0.d2)(r.d1) + (d1.d2)(r.d0) ]
  D^4 = 16 psi'''' prod_j (r.dj) + 8 psi''' sum_{6 pairs} (da.db)(r.dc)(r.dd) + 4 psi'' sum_{3 pairings} (da.db)(dc.dd)

At the cube, sig = |r|^2 in {1, 2, 3} (edges, face diagonals, body diagonals), and psi^{(k)}(sig) is the symbol
psi{k}_{sig}. All coefficients are exact rationals; results are linear forms in these 12 symbols, valid for any pair
potential. Directions must have rational entries (normalise outside).
"""
import itertools
from fractions import Fraction

import sympy as sp

from .group import LABELS

PSI = {(k, sig): sp.Symbol(f"psi{k}_{sig}") for k in range(1, 5) for sig in (1, 2, 3)}
PAIRS = list(itertools.combinations(range(8), 2))


def _frac_vec(v):
    out = []
    for c in v:
        c = sp.nsimplify(c)
        if not c.is_Rational:
            raise ValueError("direction entries must be rational")
        out.append(Fraction(int(c.p), int(c.q)))
    return out


def _base(i, j):
    return [Fraction(LABELS[i][c] - LABELS[j][c], 2) for c in range(3)]


def _dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def derivative(dirs):
    """D^n V [dirs[0], ..., dirs[n-1]] at the unit-edge cube, n = 1..4, as a linear form in PSI."""
    n = len(dirs)
    D = [_frac_vec(d) for d in dirs]
    acc = {}

    def add(k, sig, c):
        if c:
            acc[(k, sig)] = acc.get((k, sig), Fraction(0)) + c

    for i, j in PAIRS:
        r = _base(i, j)
        sig = int(_dot(r, r))
        d = [[D[m][3 * i + c] - D[m][3 * j + c] for c in range(3)] for m in range(n)]
        xr = [_dot(r, dm) for dm in d]
        dd = [[_dot(d[a], d[b]) for b in range(n)] for a in range(n)]
        if n == 1:
            add(1, sig, 2 * xr[0])
        elif n == 2:
            add(2, sig, 4 * xr[0] * xr[1])
            add(1, sig, 2 * dd[0][1])
        elif n == 3:
            add(3, sig, 8 * xr[0] * xr[1] * xr[2])
            add(2, sig, 4 * (dd[0][1] * xr[2] + dd[0][2] * xr[1] + dd[1][2] * xr[0]))
        elif n == 4:
            add(4, sig, 16 * xr[0] * xr[1] * xr[2] * xr[3])
            s3 = Fraction(0)
            for a, b in itertools.combinations(range(4), 2):
                c, e = [m for m in range(4) if m not in (a, b)]
                s3 += dd[a][b] * xr[c] * xr[e]
            add(3, sig, 8 * s3)
            add(2, sig, 4 * (dd[0][1] * dd[2][3] + dd[0][2] * dd[1][3] + dd[0][3] * dd[1][2]))
        else:
            raise ValueError("n must be 1..4")
    return sp.Add(*[sp.Rational(c.numerator, c.denominator) * PSI[key] for key, c in sorted(acc.items())])


def hessian():
    """24x24 Hessian at the cube: pair block 4 psi''(sig) r r^T + 2 psi'(sig) I_3."""
    H = sp.zeros(24)
    for i, j in PAIRS:
        r = sp.Matrix([sp.Rational(LABELS[i][c] - LABELS[j][c], 2) for c in range(3)])
        sig = int((r.T * r)[0, 0])
        B = 4 * PSI[(2, sig)] * r * r.T + 2 * PSI[(1, sig)] * sp.eye(3)
        for (a, b, sgn) in ((i, i, 1), (j, j, 1), (i, j, -1), (j, i, -1)):
            H[3 * a:3 * a + 3, 3 * b:3 * b + 3] += sgn * B
    return H


# ---------------------------------------------------------------------------------------------------------------
# Specialisation to phi(r) = A r^-p - B r^-q, i.e. psi(sig) = A sig^(-p/2) - B sig^(-q/2).
r_, p_, q_ = sp.symbols("r p q", positive=True)
X = {name: sp.Symbol(f"X{name}", positive=True) for name in ("r", "p", "q")}   # X_r = 2^(-r/2)
Y = {name: sp.Symbol(f"Y{name}", positive=True) for name in ("r", "p", "q")}   # Y_r = 3^(-r/2)
EXP = {"r": r_, "p": p_, "q": q_}


def power_psi(name):
    """psi^{(k)}(sig) for psi(sig) = sig^(-e/2), e = r, p or q, with sig^(-e/2) -> 1, X_e, Y_e."""
    e = EXP[name]
    base = {1: sp.Integer(1), 2: X[name], 3: Y[name]}
    out = {}
    for k in range(1, 5):
        ff = sp.Integer(1)
        for j in range(k):
            ff *= (-e / 2 - j)
        for sig in (1, 2, 3):
            out[PSI[(k, sig)]] = ff * base[sig] * sp.Integer(sig) ** (-k)
    return out


def W(name):
    """W_e = U_e(cube)/12 = 1 + X_e + Y_e/3 (Paper 2)."""
    return 1 + X[name] + Y[name] / 3


def T_EQ():
    """A/B at the unit-edge cubic equilibrium: t = q W_q / (p W_p) (Paper 2)."""
    return q_ * W("q") / (p_ * W("p"))


def two_term(A=None, B=1):
    """Substitution psi_k(sig) for psi = A sig^(-p/2) - B sig^(-q/2); A defaults to the equilibrium value t."""
    A = T_EQ() if A is None else A
    P, Q = power_psi("p"), power_psi("q")
    return {s: A * P[s] - B * Q[s] for s in PSI.values()}


def g_of(linear_form, name="r"):
    """g_Q(e) = L_Q(e) / (e W_e), where L_Q is the linear form evaluated on psi = sig^(-e/2).
    At the equilibrium (A = t, B = 1): Q = q W_q [ g_Q(p) - g_Q(q) ]."""
    return sp.together(linear_form.subs(power_psi(name)) / (EXP[name] * W(name)))


def to_numeric_exponent(expr, name="r"):
    """Replace X_e, Y_e by 2^(-e/2), 3^(-e/2)."""
    e = EXP[name]
    return expr.subs({X[name]: 2 ** (-e / 2), Y[name]: 3 ** (-e / 2)})
