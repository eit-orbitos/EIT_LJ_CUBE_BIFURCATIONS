"""Independent numerical route (mpmath): the 24-dimensional pair energy itself, its analytic gradient and Hessian
(the parallel/perpendicular block formula of Paper 2, src/eit_lj_stability/hessian.py), and directional derivatives
by mpmath.diff. It shares no algebra with the symbolic routes in pairsum.py and a2u.py.
"""
import itertools

import mpmath as mp

from .group import LABELS

PAIRS = list(itertools.combinations(range(8), 2))


def y_star():
    return [mp.mpf(c) / 2 for s in LABELS for c in s]


def unit_field(f):
    v = [mp.mpf(c) for s in LABELS for c in f(s)]
    n = mp.sqrt(mp.fsum(c * c for c in v))
    return [c / n for c in v]


def e_A():
    return unit_field(lambda s: [s[0] * s[1] * s[2] * c for c in s])


def e_br():
    return unit_field(lambda s: s)


def t_eq(p, q):
    W = lambda e: 1 + mp.power(2, -e / 2) + mp.power(3, -e / 2) / 3
    return q * W(q) / (p * W(p))


class PairEnergy:
    """V(x) = sum phi(|x_i - x_j|), phi(r) = A r^-p - B r^-q (default A = t: unit-edge cube at equilibrium)."""

    def __init__(self, p, q, A=None, B=1):
        self.p, self.q = mp.mpf(p), mp.mpf(q)
        self.A = t_eq(self.p, self.q) if A is None else mp.mpf(A)
        self.B = mp.mpf(B)

    def phi(self, rr):
        return self.A * rr ** (-self.p) - self.B * rr ** (-self.q)

    def dphi(self, rr):
        return -self.p * self.A * rr ** (-self.p - 1) + self.q * self.B * rr ** (-self.q - 1)

    def d2phi(self, rr):
        return (self.p * (self.p + 1) * self.A * rr ** (-self.p - 2)
                - self.q * (self.q + 1) * self.B * rr ** (-self.q - 2))

    def energy(self, xv):
        tot = mp.mpf(0)
        for i, j in PAIRS:
            d = [xv[3 * i + c] - xv[3 * j + c] for c in range(3)]
            tot += self.phi(mp.sqrt(mp.fsum(c * c for c in d)))
        return tot

    def gradient(self, xv):
        g = [mp.mpf(0)] * 24
        for i, j in PAIRS:
            d = [xv[3 * i + c] - xv[3 * j + c] for c in range(3)]
            rr = mp.sqrt(mp.fsum(c * c for c in d))
            f = self.dphi(rr) / rr
            for c in range(3):
                g[3 * i + c] += f * d[c]
                g[3 * j + c] -= f * d[c]
        return g

    def hessian(self, xv):
        H = mp.zeros(24, 24)
        for i, j in PAIRS:
            d = [xv[3 * i + c] - xv[3 * j + c] for c in range(3)]
            rr = mp.sqrt(mp.fsum(c * c for c in d))
            e = [c / rr for c in d]
            d1, d2 = self.dphi(rr), self.d2phi(rr)
            for a in range(3):
                for b in range(3):
                    blk = d2 * e[a] * e[b] + d1 / rr * ((1 if a == b else 0) - e[a] * e[b])
                    H[3 * i + a, 3 * i + b] += blk
                    H[3 * j + a, 3 * j + b] += blk
                    H[3 * i + a, 3 * j + b] -= blk
                    H[3 * j + a, 3 * i + b] -= blk
        return H


def shift(base, *terms):
    out = list(base)
    for coef, vec in terms:
        out = [o + coef * v for o, v in zip(out, vec)]
    return out


def lyapunov_schmidt_c4(p, q, kernel):
    """c4 = D^4V[e,e,e,e] - 3 <b, H_perp^{-1} b>, e = e_A, b = D^3V[e,e,.], computed in R^24 without any symmetry
    reduction: b by differentiating the analytic gradient, H_perp^{-1} via (H + P_ker) w = b (b is orthogonal to
    ker H). `kernel` is a list of orthonormal 24-vectors spanning ker H (rigid motions and e_A)."""
    V = PairEnergy(p, q)
    y0, eA, eB = y_star(), e_A(), e_br()
    V4 = mp.diff(lambda a: V.energy(shift(y0, (a, eA))), 0, 4)
    b = [mp.diff(lambda a, i=i: V.gradient(shift(y0, (a, eA)))[i], 0, 2) for i in range(24)]
    H = V.hessian(y0)
    P = mp.zeros(24, 24)
    for kv in kernel:
        for i in range(24):
            for j in range(24):
                P[i, j] += kv[i] * kv[j]
    w = mp.lu_solve(H + P, mp.matrix(b))
    bHb = mp.fsum(b[i] * w[i] for i in range(24))
    return {"V_aaaa": V4, "b": b, "<b,Hinv b>": bHb, "c4": V4 - 3 * bHb, "H": H,
            "V_aab": mp.diff(lambda a, bb: V.energy(shift(y0, (a, eA), (bb, eB))), (0, 0), (2, 1)),
            "V_bb": mp.diff(lambda bb: V.energy(shift(y0, (bb, eB))), 0, 2),
            "V_aa": mp.diff(lambda a: V.energy(shift(y0, (a, eA))), 0, 2)}
