"""Phase B2.5: Proposition B3, the Morse index of the three-dimensional T2g centre-manifold (Lyapunov-Schmidt) reduced
Hessian on the D2h branch of Proposition B2, and Corollary B3' (the full-slice index).

Fix 0 < q < q_c, mu = p - P_T(q), unit n in ker K at mu = 0 with n_u > 0 (chart gauge), e_k = n_u uh_k + n_v vh_k,
f_k = -n_v uh_k + n_u vh_k (k = 1, 2, 3). Coordinates a = (a1, a2, a3) on E_c = span{e_1, e_2, e_3}. The slice is
S = y* + R^perp (R = the six rigid-motion fields at y*), and W = S-directions orthogonal to E_c (dimension 15). The
reduced potential is V_red(a, mu) = V_p(y* + sum a_k e_k + w(a, mu)), with w in W solving P_W grad V = 0.

EXACT LAYER (proof; SymPy, exact arithmetic; each item has a test):
  1. g3_group / invariant_dimensions / invariant_basis_check: the 3x3 action T(R) = sigma(R) R has 24 distinct
     matrices (signed permutations with an even number of -1); invariant polynomials of degree 1..6 have dimensions
     0, 1, 1, 2, 1, 3; degree 2 is spanned by I2 = |a|^2, degree 3 by I3 = a1 a2 a3, degree 4 by I2^2 and I4 = sum a_k^4.
  2. axis_stabiliser / commutant_on_axis / parity_on_axis: at a = (s, 0, 0) the Hessian of ANY G3-invariant C^2
     function has the form [[h11, 0, 0], [0, d, e], [0, e, d]]; h11 and d are even in s, e is odd.
  3. generic_invariant_hessian: for a generic invariant polynomial of degree <= 6 (all invariant coefficients
     symbolic): h11 = lam + 12(alpha + beta) s^2 + O(s^4), d = lam + 4 alpha s^2 + O(s^4), e = kappa s + O(s^3).
  4. branch_hessian_series: with mu-dependent coefficients and mu = mu*(s^2) from the axial equation:
     mu*'(0) = -c4/(6 tau), h11 = (c4/3) s^2 + O(s^4), d = -4 beta s^2 + O(s^4), e = kappa s + O(s^3),
     det of the transverse block = -kappa^2 s^2 + O(s^4); h11 = -2 tau mu + O(mu^2) (B2.4 consistency).
  5. transverse_eigensystem / transverse_sign_bound: eigenvalues d +- e on (0, 1, +-1)/sqrt2 exactly; an explicit
     remainder inequality shows d + e and d - e have opposite signs for 0 < |s| < |kappa|/(C_D + C_E).
  6. ls_quartic_exact: the complete O_h-invariant quartic V4 of the reduced potential at mu = 0 for a generic pair
     potential, V4 = (1/24) D^4V[x^4] - (1/8) <b(x), H_W^-1 b(x)>, b(x) = D^3V[x, x, .]: b(x) lies in A1g + Eg + T2g,
     its W-part has A1g, Eg and f_k components only, and V4 = alpha I2^2 + beta I4 with explicit alpha, beta;
     alpha + beta = c4/24 (B2.1).
  7. generic_ls_multid / schur_hessian_identity / haynsworth_check: the quartic LS formula for a multi-dimensional
     kernel; D^2 V_red = H_cc - H_cW H_WW^-1 H_Wc along the reduction; index additivity (Haynsworth).
  8. FROZEN_SPECTRUM_ON_CURVE / complementary_index: Paper 2's Theorem (index) block signs on the T2g curve (FROZEN
     INPUT), from which m_perp = 3 is derived by counting (rigid motions and the critical T2g triple excluded).
  9. conjugate_branches: the six points (+-s, 0, 0), (0, +-s, 0), (0, 0, +-s) form one G3-orbit; in R^24 the O_h-orbit
     of e_1 is {+-e_k}; congruent Hessians, one index type.
 10. d3d_consistency: the same cubic normal form on the D3d axis (consistency check only, not a new proposition).
 11. PROPOSITION_B3, COROLLARY_B3, DEPENDENCY_GRAPH, validate_statement, validate_graph.

NUMERIC LAYER (corroboration only, never a proof dependency): the raw 24x24 Hessian at numerically located D2h and
D3d equilibria, its spectrum, the Schur complement onto E_c, and a nonlinear (derivative-free) check of V4.
"""
import itertools
from functools import lru_cache

import mpmath as mp
import sympy as sp

from . import pairsum as ps
from .group import oh_matrices, D24, sigma, projector, LABELS
from .modes import E_BR, U_T2G, W_T2G, TRANSLATIONS, ROTATIONS

# ======================================================================================================================
# EXACT LAYER
# ======================================================================================================================
a1, a2, a3 = sp.symbols("a1 a2 a3", real=True)
A = (a1, a2, a3)
s, mu, z = sp.symbols("s mu z", real=True)
I2 = a1 ** 2 + a2 ** 2 + a3 ** 2
I3 = a1 * a2 * a3
I4 = a1 ** 4 + a2 ** 4 + a3 ** 4
TAU, KAP, C4 = sp.symbols("tau kappa c4", real=True, nonzero=True)
ALPHA, BETA = sp.symbols("alpha beta", real=True)
nu, nv = sp.symbols("n_u n_v")          # the same symbols as t2g.py / b2_quartic.py
HA, HE, KFF = sp.symbols("h_A h_E k_ff", positive=True)


# ---- 1. the 3x3 group and its invariants ----------------------------------------------------------------------------
@lru_cache(maxsize=None)
def g3_group():
    """The distinct matrices T(R) = sigma(R) R, R in O_h (the action on the critical T2g coordinates a)."""
    out = []
    for R in oh_matrices():
        T = sp.ImmutableMatrix(sigma(R) * R)
        if T not in out:
            out.append(T)
    return tuple(out)


def _act(poly, T):
    img = T * sp.Matrix(A)
    return sp.expand(poly.subs({a1: img[0], a2: img[1], a3: img[2]}, simultaneous=True))


def _monomials(deg):
    return [a1 ** i * a2 ** j * a3 ** (deg - i - j) for i in range(deg + 1) for j in range(deg + 1 - i)]


def reynolds(poly):
    G = g3_group()
    return sp.expand(sum(_act(poly, T) for T in G) / len(G))


@lru_cache(maxsize=None)
def invariant_basis(deg):
    """A basis of the invariant polynomials of degree deg (Reynolds images of monomials, row-reduced)."""
    mons = _monomials(deg)
    imgs = [sp.Poly(reynolds(m), *A) for m in mons]
    M = sp.Matrix([[im.coeff_monomial(b) for b in mons] for im in imgs])
    R, piv = M.T.rref()
    basis = [sp.expand(sum(M[i, j] * mons[j] for j in range(len(mons)))) for i in piv]
    return tuple(b for b in basis if b != 0)


def invariant_dimensions(maxdeg=6):
    return {d: len(invariant_basis(d)) for d in range(1, maxdeg + 1)}


def _in_span(poly, basis):
    mons = sorted(set().union(*[sp.Poly(b, *A).monoms() for b in basis] + [sp.Poly(poly, *A).monoms()]))
    cols = [[sp.Poly(b, *A).coeff_monomial(m) for m in mons] for b in basis]
    M = sp.Matrix(cols).T
    v = sp.Matrix([sp.Poly(poly, *A).coeff_monomial(m) for m in mons])
    return M.rank() == M.row_join(v).rank()


def invariant_basis_check():
    """I2, I3, I2^2, I4 are invariant and span the invariants of degree 2, 3, 4; no invariant of degree 1."""
    G = g3_group()
    inv = all(_act(f, T) == sp.expand(f) for f in (I2, I3, I2 ** 2, I4) for T in G)
    return {"order": len(G), "all_invariant": inv,
            "deg2_spanned_by_I2": len(invariant_basis(2)) == 1 and _in_span(I2, invariant_basis(2)),
            "deg3_spanned_by_I3": len(invariant_basis(3)) == 1 and _in_span(I3, invariant_basis(3)),
            "deg4_spanned_by_I2sq_I4": (len(invariant_basis(4)) == 2 and _in_span(sp.expand(I2 ** 2), invariant_basis(4))
                                        and _in_span(I4, invariant_basis(4))
                                        and sp.Matrix([[sp.Poly(sp.expand(I2 ** 2), *A).coeff_monomial(a1 ** 4),
                                                        sp.Poly(sp.expand(I2 ** 2), *A).coeff_monomial(a1 ** 2 * a2 ** 2)],
                                                       [1, 0]]).rank() == 2),
            "deg1_empty": len(invariant_basis(1)) == 0,
            "signed_permutations_even_minus": all(
                all(sum(1 for x in T if x != 0) == 3 for _ in [0]) and sp.prod([x for x in T if x != 0]) == 1
                for T in G)}


# ---- 2. Hessian structure on the axis, for any invariant function ------------------------------------------------------
AXIS = sp.Matrix([1, 0, 0])


def axis_stabiliser():
    return tuple(T for T in g3_group() if T * AXIS == AXIS)


def axis_reversers():
    return tuple(T for T in g3_group() if T * AXIS == -AXIS)


def commutant_on_axis():
    """General symmetric 3x3 H with T H T^T = H for every T in the axis stabiliser (exact linear solve)."""
    h = sp.symbols("h11 h12 h13 h22 h23 h33")
    H = sp.Matrix([[h[0], h[1], h[2]], [h[1], h[3], h[4]], [h[2], h[4], h[5]]])
    eqs = []
    for T in axis_stabiliser():
        eqs += list(T * H * T.T - H)
    sol = sp.solve(eqs, h, dict=True)
    Hs = H.subs(sol[0]) if sol else H
    return {"stabiliser_order": len(axis_stabiliser()), "H": Hs,
            "h12_zero": Hs[0, 1] == 0 and Hs[0, 2] == 0, "h22_eq_h33": sp.simplify(Hs[1, 1] - Hs[2, 2]) == 0,
            "free_parameters": len(Hs.free_symbols)}


def parity_on_axis():
    """For T in G3 with T(1,0,0) = -(1,0,0): H(-s) = T H(s) T^T. On the commutant form this gives h11, d even and e
    odd in s (for every reverser)."""
    h11, d, e = sp.symbols("h11 d e")
    H = sp.Matrix([[h11, 0, 0], [0, d, e], [0, e, d]])
    out = []
    for T in axis_reversers():
        Hm = T * H * T.T
        out.append({"h11": Hm[0, 0] == h11, "d": Hm[1, 1] == d and Hm[2, 2] == d, "e_flips": Hm[1, 2] == -e,
                    "zeros": Hm[0, 1] == 0 and Hm[0, 2] == 0})
    return {"reversers": len(axis_reversers()), "checks": out,
            "all": bool(out) and all(all(c.values()) for c in out)}


# ---- 3. a generic invariant polynomial and its Hessian on the axis ------------------------------------------------------
LAM = sp.Symbol("lam", real=True)


@lru_cache(maxsize=None)
def generic_invariant_V(maxdeg=6):
    """V0 + lam I2/2 + kappa I3 + alpha I2^2 + beta I4 + sum over invariant bases of degree 5..maxdeg with symbolic
    coefficients c{deg}_{i}."""
    V = sp.Symbol("V0") + LAM * I2 / 2 + KAP * I3 + ALPHA * I2 ** 2 + BETA * I4
    coeffs = []
    for d in range(5, maxdeg + 1):
        for i, b in enumerate(invariant_basis(d)):
            c = sp.Symbol(f"c{d}_{i}", real=True)
            coeffs.append(c)
            V += c * b
    return sp.expand(V), tuple(coeffs)


def generic_invariant_hessian(maxdeg=6):
    V, _ = generic_invariant_V(maxdeg)
    H = sp.hessian(V, A).subs({a1: s, a2: 0, a3: 0})
    H = H.applyfunc(sp.expand)
    h11, d, e = H[0, 0], H[1, 1], H[1, 2]

    def low(expr, k):
        return sp.expand(sum(sp.Poly(expr, s).coeff_monomial(s ** j) * s ** j for j in range(k + 1)))

    return {"H": H,
            "structure": H[0, 1] == 0 and H[0, 2] == 0 and sp.expand(H[1, 1] - H[2, 2]) == 0,
            "h11_even": sp.expand(h11 - h11.subs(s, -s)) == 0, "d_even": sp.expand(d - d.subs(s, -s)) == 0,
            "e_odd": sp.expand(e + e.subs(s, -s)) == 0,
            "h11_low": low(h11, 3), "d_low": low(d, 3), "e_low": low(e, 2),
            "h11_low_ok": sp.expand(low(h11, 3) - (LAM + 12 * (ALPHA + BETA) * s ** 2)) == 0,
            "d_low_ok": sp.expand(low(d, 3) - (LAM + 4 * ALPHA * s ** 2)) == 0,
            "e_low_ok": sp.expand(low(e, 2) - KAP * s) == 0}


# ---- 4. on the branch ------------------------------------------------------------------------------------------------
@lru_cache(maxsize=None)
def branch_hessian_series(maxdeg=6):
    """mu-dependent coefficients: lam(mu) = tau mu + l2 mu^2, kappa(mu) = kappa + k1 mu, alpha(mu) = alpha + al1 mu,
    beta(mu) = beta + be1 mu, degree-5/6 coefficients constant (enough to the orders below). mu = m1 z + m2 z^2,
    z = s^2, solved from (1/s) dV/ds (s, 0, 0) = 0 order by order. Returns the series of h11, d, e and the transverse
    determinant on the branch."""
    V, coeffs = generic_invariant_V(maxdeg)
    l2, k1, al1, be1, m1, m2 = sp.symbols("l2 k1 al1 be1 m1 m2", real=True)
    sub = {LAM: TAU * mu + l2 * mu ** 2, KAP: KAP + k1 * mu, ALPHA: ALPHA + al1 * mu, BETA: BETA + be1 * mu}
    Vm = sp.expand(V.subs(sub, simultaneous=True))
    g = sp.expand(sp.diff(Vm, a1).subs({a1: s, a2: 0, a3: 0}) / s)
    gz = sp.expand(g.subs(mu, m1 * s ** 2 + m2 * s ** 4))
    eq2 = sp.Poly(gz, s).coeff_monomial(s ** 2)
    m1v = sp.solve(eq2, m1)[0]
    eq4 = sp.Poly(gz.subs(m1, m1v), s).coeff_monomial(s ** 4)
    m2v = sp.solve(eq4, m2)[0]
    H = sp.hessian(Vm, A).subs({a1: s, a2: 0, a3: 0}).subs(mu, m1v * s ** 2 + m2v * s ** 4)
    H = H.applyfunc(sp.expand)
    cut = lambda ex, k: sp.expand(sum(sp.Poly(ex, s).coeff_monomial(s ** j) * s ** j for j in range(k + 1)))
    h11, d, e = cut(H[0, 0], 3), cut(H[1, 1], 3), cut(H[1, 2], 2)
    det = cut(sp.expand(H[1, 1] ** 2 - H[1, 2] ** 2), 3)
    c4 = 24 * (ALPHA + BETA)
    zstar = sp.symbols("zstar")
    # h11 in terms of mu: s^2 = -6 tau mu/c4 + O(mu^2)
    h11_mu = sp.expand((c4 / 3) * (-6 * TAU * mu / c4))
    return {"m1": sp.simplify(m1v), "m1_ok": sp.simplify(m1v - (-c4 / (6 * TAU))) == 0,
            "h11": h11, "d": d, "e": e, "det": det,
            "h11_ok": sp.expand(h11 - c4 / 3 * s ** 2) == 0,
            "d_ok": sp.expand(d + 4 * BETA * s ** 2) == 0,
            "e_ok": sp.expand(e - KAP * s) == 0,
            "det_ok": sp.expand(det + KAP ** 2 * s ** 2) == 0,
            "h11_as_mu_ok": sp.simplify(h11_mu + 2 * TAU * mu) == 0,
            "offdiag_zero": all(sp.expand(H[0, j]) == 0 for j in (1, 2)) and sp.expand(H[1, 1] - H[2, 2]) == 0}


# ---- 5. the transverse block --------------------------------------------------------------------------------------------
def transverse_eigensystem():
    d, e = sp.symbols("d e", real=True)
    M = sp.Matrix([[d, e], [e, d]])
    vp, vm = sp.Matrix([1, 1]) / sp.sqrt(2), sp.Matrix([1, -1]) / sp.sqrt(2)
    return {"plus": sp.simplify(M * vp - (d + e) * vp) == sp.zeros(2, 1),
            "minus": sp.simplify(M * vm - (d - e) * vm) == sp.zeros(2, 1),
            "det": sp.expand(M.det() - (d ** 2 - e ** 2)) == 0,
            "eigenvalues": sorted(M.eigenvals().keys(), key=str)}


def transverse_sign_bound():
    """d = s^2 D, e = s (kappa + s^2 E) with |D| <= C_D, |E| <= C_E for |s| <= 1. Then
    (d + e)(d - e) = d^2 - e^2 = s^2 [ s^2 D^2 - (kappa + s^2 E)^2 ], and for 0 < |s| <= 1 with
    (C_D + C_E)|s| < |kappa|:  |s D| <= C_D |s| < |kappa| - C_E s^2 <= |kappa + s^2 E|, so d^2 - e^2 < 0.
    Returned: the exact identity, and the inequality chain checked on a grid of exact rational cases including the
    extreme admissible values of D and E (worst case D = +-C_D, E = -sign(kappa) C_E)."""
    D, E, CD, CE = sp.symbols("D E C_D C_E", real=True)
    d = s ** 2 * D
    e = s * (KAP + s ** 2 * E)
    ident = sp.expand((d + e) * (d - e) - s ** 2 * (s ** 2 * D ** 2 - (KAP + s ** 2 * E) ** 2)) == 0
    ok = True
    cases = 0
    for kap in (sp.Rational(1, 3), -sp.Rational(2, 7)):
        for cd in (sp.Integer(0), sp.Rational(5, 2), sp.Integer(40)):
            for ce in (sp.Integer(0), sp.Integer(3), sp.Integer(17)):
                smax = min(sp.Integer(1), abs(kap) / (cd + ce)) if cd + ce > 0 else sp.Integer(1)
                for frac in (sp.Rational(1, 1000), sp.Rational(1, 3), sp.Rational(999, 1000)):
                    sv = smax * frac
                    for Dv in (-cd, cd):
                        for Ev in (-ce, ce):
                            for sgn in (1, -1):
                                val = ((d + e) * (d - e)).subs({s: sgn * sv, D: Dv, E: Ev, KAP: kap})
                                ok = ok and val < 0
                                cases += 1
    return {"identity": ident, "inequality_cases": cases, "all_negative": ok}


def centre_index_from_signs(c4_sign, kappa_nonzero=True):
    """Leading-order centre index at (+-s*, 0, 0), read off the derived branch series (branch_hessian_series):
    axial part from the s^2 coefficient of h11 (= c4/3 with c4 = 24(alpha + beta)), transverse part from the s^2
    coefficient of the transverse determinant (= -kappa^2 < 0 for every real kappa != 0: one negative and one
    positive eigenvalue). Returns None if kappa = 0 (undetermined at this order)."""
    if not kappa_nonzero:
        return None
    br = branch_hessian_series(6)
    c4v = sp.Integer(1) if c4_sign == ">0" else sp.Integer(-1)
    h11c = sp.expand(sp.expand(br["h11"]).coeff(s, 2).subs(BETA, c4v / 24 - ALPHA))
    detc = sp.expand(br["det"]).coeff(s, 2)
    det_negative = all(detc.subs(KAP, kv) < 0 for kv in (sp.Rational(3, 7), -sp.Rational(3, 7), 5, -5)) \
        and sp.simplify(detc + KAP ** 2) == 0
    if det_negative:
        transverse = 1
    else:
        return None
    return (1 if h11c < 0 else 0) + transverse


# ---- 6. the complete invariant quartic of V_red at mu = 0 (generic pair potential) ---------------------------------------
_FIELD = {"u": W_T2G, "v": U_T2G}
_SCALE = {"u": sp.Rational(-1, 4), "v": -sp.sqrt(2) / 4}


@lru_cache(maxsize=None)
def _raw(keys):
    """D^nV on integer fields named by keys (('u', k) | ('v', k) | ('c', m) | ('A',) | ('E', k) ...), as a linear form."""
    dirs = []
    for key in keys:
        if key[0] in ("u", "v"):
            dirs.append(_FIELD[key[0]][key[1]])
        elif key[0] == "c":
            vct = sp.zeros(24, 1)
            vct[key[1]] = 1
            dirs.append(vct)
        else:
            raise ValueError(key)
    return ps.derivative(dirs)


def _vec(kind, k, n_u=nu, n_v=nv):
    """e_k (kind 'e') or f_k (kind 'f') as a list of (coefficient, key)."""
    if kind == "e":
        return [(n_u * _SCALE["u"], ("u", k)), (n_v * _SCALE["v"], ("v", k))]
    return [(-n_v * _SCALE["u"], ("u", k)), (n_u * _SCALE["v"], ("v", k))]


def multilinear(vectors, extra=()):
    """D^nV[v_1, ..., v_m, extra...] with v_i given as lists of (coefficient, key), extra as raw keys."""
    tot = 0
    for combo in itertools.product(*vectors):
        coef = sp.Mul(*[c for c, _ in combo])
        keys = tuple(sorted([k for _, k in combo] + list(extra)))
        tot += coef * _raw(keys)
    return sp.expand(tot)


@lru_cache(maxsize=None)
def quartic_tensor():
    """D^4V[e_i, e_j, e_k, e_l] for sorted index tuples (symbolic n, generic psi)."""
    return {idx: multilinear([_vec("e", i) for i in idx]) for idx in itertools.combinations_with_replacement(range(3), 4)}


def d4_polynomial():
    """D^4V[x^4], x = sum a_k e_k, as a polynomial in a (multinomial expansion over sorted index tuples)."""
    tot = 0
    for idx, val in quartic_tensor().items():
        cnt = [idx.count(k) for k in range(3)]
        mult = sp.factorial(4) / sp.Mul(*[sp.factorial(c) for c in cnt])
        tot += mult * val * sp.Mul(*[A[k] ** cnt[k] for k in range(3)])
    return sp.expand(tot)


@lru_cache(maxsize=None)
def b_vector():
    """b(x)_m = D^3V[x, x, eps_m], x = sum a_k e_k (24 polynomials, quadratic in a)."""
    out = []
    for m in range(24):
        tot = 0
        for i in range(3):
            for j in range(3):
                tot += A[i] * A[j] * multilinear([_vec("e", i), _vec("e", j)], extra=(("c", m),))
        out.append(sp.expand(tot))
    return sp.Matrix(out)


@lru_cache(maxsize=None)
def _P(irrep):
    return sp.ImmutableMatrix(projector(irrep))


def _f_vec24(k, n_u=nu, n_v=nv):
    return (-n_v * W_T2G[k] * _SCALE["u"] + n_u * U_T2G[k] * _SCALE["v"])


def _e_vec24(k, n_u=nu, n_v=nv):
    return (n_u * W_T2G[k] * _SCALE["u"] + n_v * U_T2G[k] * _SCALE["v"])


@lru_cache(maxsize=None)
def b_decomposition():
    """Isotypic decomposition of b(x): which irreps occur; |P_A1g b|^2, |P_Eg b|^2; <b, f_k>, <b, e_k>."""
    b = b_vector()
    norms = {}
    for G in ("A1g", "A2g", "Eg", "T1g", "T2g", "A1u", "A2u", "Eu", "T1u", "T2u"):
        Pb = (_P(G) * b).applyfunc(sp.expand)
        norms[G] = Pb == sp.zeros(24, 1)
    nAg = sp.expand((b.T * _P("A1g") * b)[0, 0])
    nEg = sp.expand((b.T * _P("Eg") * b)[0, 0])
    bf = [sp.expand((_f_vec24(k).T * b)[0, 0]) for k in range(3)]
    be = [sp.expand((_e_vec24(k).T * b)[0, 0]) for k in range(3)]
    return {"zero_components": norms, "A1g_sq": nAg, "Eg_sq": nEg, "b_f": bf, "b_e": be}


def kappa_f(n_u=nu, n_v=nv):
    """D^3V[e_1, e_2, f_3] (generic psi, symbolic n)."""
    return multilinear([_vec("e", 0, n_u, n_v), _vec("e", 1, n_u, n_v), _vec("f", 2, n_u, n_v)])


def q_mix(n_u=nu, n_v=nv):
    """D^4V[e_1, e_1, e_2, e_2] (generic psi, symbolic n)."""
    return multilinear([_vec("e", 0, n_u, n_v), _vec("e", 0, n_u, n_v), _vec("e", 1, n_u, n_v),
                        _vec("e", 1, n_u, n_v)])


@lru_cache(maxsize=None)
def ls_quartic_exact():
    """V4(a) = (1/24) D^4V[x^4] - (1/8) <b_W, H_WW^-1 b_W> at mu = 0, with H_WW acting as h_A on A1g, h_E on Eg and
    k_ff = f^T K f on span{f_k} (the T2g part of W at mu = 0); b has no other W-component (checked). Returns alpha,
    beta with V4 = alpha I2^2 + beta I4 and the checks."""
    from . import b2_quartic as q4
    dec = b_decomposition()
    D4 = d4_polynomial()
    back = dec["A1g_sq"] / HA + dec["Eg_sq"] / HE + sum(x ** 2 for x in dec["b_f"]) / KFF
    V4 = sp.expand(D4 / 24 - back / 8)
    P = sp.Poly(V4, *A)
    ab = P.coeff_monomial(a1 ** 4)            # alpha + beta
    al = P.coeff_monomial(a1 ** 2 * a2 ** 2) / 2
    be = sp.expand(ab - al)
    resid = sp.expand(V4 - (al * I2 ** 2 + be * I4))
    f = q4.linear_forms()
    Qn = q4.Q_of_n()
    bA, bE = q4.b_of_n("bA"), q4.b_of_n("bE")
    c4_formula = sp.expand(Qn - 3 * bA ** 2 / HA - 3 * bE ** 2 / HE)
    zero_irreps = [G for G, z0 in dec["zero_components"].items() if z0]
    kf = kappa_f()
    qm = q_mix()
    # hand formula: V4 = (Q/24) I4 + (Qmix/4) S2 - (1/8)[bA^2 I2^2/hA + bE^2 (I4 - S2)/hE + 4 kf^2 S2/kff],
    # S2 = a1^2 a2^2 + a1^2 a3^2 + a2^2 a3^2
    S2 = a1 ** 2 * a2 ** 2 + a1 ** 2 * a3 ** 2 + a2 ** 2 * a3 ** 2
    hand = sp.expand(Qn * I4 / 24 + qm * S2 / 4 - (bA ** 2 * I2 ** 2 / HA + bE ** 2 * (I4 - S2) / HE
                                                   + 4 * kf ** 2 * S2 / KFF) / 8)
    return {"alpha": al, "beta": be, "V4": V4,
            "invariant_form_exact": resid == 0,
            "alpha_plus_beta_is_c4_over_24": sp.expand(24 * ab - c4_formula) == 0,
            "b_irreps_present": sorted(set(dec["zero_components"]) - set(zero_irreps)),
            "hand_formula_ok": sp.expand(V4 - hand) == 0,
            "d4_only_iiii_iijj": all(sp.expand(v) == 0 for idx, v in quartic_tensor().items()
                                     if sorted(idx.count(k) for k in range(3) if idx.count(k)) not in ([4], [2, 2])),
            "hA_matches": True if f["hA"] is not None else False}


def alpha_beta_closed():
    """alpha = Qmix/8 - bA^2/(8 hA) + bE^2/(16 hE) - kf^2/(4 kff);  beta = c4/24 - alpha (exact identities, tested)."""
    from . import b2_quartic as q4
    bA, bE = q4.b_of_n("bA"), q4.b_of_n("bE")
    al = q_mix() / 8 - bA ** 2 / (8 * HA) + bE ** 2 / (16 * HE) - kappa_f() ** 2 / (4 * KFF)
    c4 = q4.Q_of_n() - 3 * bA ** 2 / HA - 3 * bE ** 2 / HE
    return {"alpha": sp.expand(al), "beta": sp.expand(c4 / 24 - al)}


# ---- 7. LS identities for a multi-dimensional kernel; Schur complement; inertia additivity ------------------------------
def _ls_energy(coeffs):
    x1, x2, w1, w2 = sp.symbols("x1 x2 w1 w2", real=True)
    allv = (x1, x2, w1, w2)
    N = 0
    k = 0
    for deg in (3, 4):
        for e in itertools.product(range(deg + 1), repeat=4):
            if sum(e) == deg:
                N += coeffs[k] * sp.Mul(*[v ** j for v, j in zip(allv, e)])
                k += 1
    return allv, N


def _trunc(expr, xs, k):
    t = sp.Symbol("t_")
    ex = sp.expand(expr.subs({x: t * x for x in xs}, simultaneous=True))
    return sp.expand(sum(ex.coeff(t, j) for j in range(k + 1)))


def generic_ls_multid():
    """Generic polynomial energy V = h1 w1^2/2 + h2 w2^2/2 + N(x1, x2, w1, w2), N with all 55 cubic and quartic
    monomials (symbolic coefficients): zero Hessian on the kernel x, no x-w coupling, H_ww = diag(h1, h2).
    Lyapunov-Schmidt: w(x) solves dV/dw = 0; through degree 2, w = -H_ww^-1 b(x)/2 with b_m(x) = D^3V[x, x, w_m],
    and the quartic of V_red = V(x, w(x)) depends only on that part. Checks: dV/dw(x, w(x)) = O(|x|^3), and
    quartic(V_red) = (1/24) D^4V[x^4] - (1/8) b^T H_ww^-1 b."""
    h1, h2 = sp.symbols("h1 h2", positive=True)
    (x1, x2, w1, w2), N = _ls_energy([sp.Symbol(f"g{i}") for i in range(55)])
    X = (x1, x2)
    V = h1 * w1 ** 2 / 2 + h2 * w2 ** 2 / 2 + N
    b = [2 * _trunc(sp.diff(N, wv).subs({w1: 0, w2: 0}), X, 2) for wv in (w1, w2)]
    w = [-b[0] / (2 * h1), -b[1] / (2 * h2)]
    resid_ok = all(_trunc(sp.diff(V, wv).subs({w1: w[0], w2: w[1]}, simultaneous=True), X, 2) == 0 for wv in (w1, w2))
    Vred4 = _trunc(V.subs({w1: w[0], w2: w[1]}, simultaneous=True), X, 4) - _trunc(V.subs({w1: w[0], w2: w[1]},
                                                                                       simultaneous=True), X, 3)
    D4 = 24 * (_trunc(N.subs({w1: 0, w2: 0}), X, 4) - _trunc(N.subs({w1: 0, w2: 0}), X, 3))
    formula = sp.expand(D4 / 24 - (b[0] ** 2 / h1 + b[1] ** 2 / h2) / 8)
    return {"quartic_formula": sp.expand(Vred4 - formula) == 0, "ls_residual_order2": resid_ok,
            "generic_coefficients": 55}


def schur_hessian_identity(trials=3, seed=11):
    """D^2 V_red = [H_xx - H_xw H_ww^-1 H_wx](x, w(x)) (chain rule, using dV/dw(x, w(x)) = 0 and
    w_x = -H_ww^-1 H_wx). Checked exactly through second order in x for energies with random rational cubic and
    quartic coefficients: w(x) to degree 3 by two contraction steps w <- -H_ww^-1 dN/dw(x, w)."""
    import random
    rnd = random.Random(seed)
    ok = True
    for _ in range(trials):
        h1, h2 = sp.Rational(rnd.randint(1, 9), rnd.randint(1, 4)), -sp.Rational(rnd.randint(1, 9), rnd.randint(1, 4))
        (x1, x2, w1, w2), N = _ls_energy([sp.Rational(rnd.randint(-9, 9), rnd.randint(1, 5)) for _ in range(55)])
        X = (x1, x2)
        V = h1 * w1 ** 2 / 2 + h2 * w2 ** 2 / 2 + N
        hs = (h1, h2)
        w = [sp.Integer(0), sp.Integer(0)]
        for _ in range(3):
            w = [_trunc(-sp.diff(N, wv).subs({w1: w[0], w2: w[1]}, simultaneous=True) / hs[j], X, 3)
                 for j, wv in enumerate((w1, w2))]
        ok = ok and all(_trunc(sp.diff(V, wv).subs({w1: w[0], w2: w[1]}, simultaneous=True), X, 3) == 0
                        for wv in (w1, w2))
        Vr = _trunc(V.subs({w1: w[0], w2: w[1]}, simultaneous=True), X, 4)
        Hr = sp.hessian(Vr, X).applyfunc(lambda ex: _trunc(ex, X, 2))
        Hf = sp.hessian(V, (x1, x2, w1, w2)).subs({w1: w[0], w2: w[1]}, simultaneous=True)
        Hf = Hf.applyfunc(lambda ex: _trunc(ex, X, 2))
        Haa, Haw, Hww = Hf[:2, :2], Hf[:2, 2:], Hf[2:, 2:]
        H0 = sp.diag(1 / h1, 1 / h2)
        Dd = Hww - sp.diag(h1, h2)
        Hinv = H0 - H0 * Dd * H0 + H0 * Dd * H0 * Dd * H0
        Sch = (Haa - Haw * Hinv * Haw.T).applyfunc(lambda ex: _trunc(ex, X, 2))
        ok = ok and (Hr - Sch).applyfunc(sp.expand) == sp.zeros(2)
    return ok


def _inertia(M):
    """(n_neg, n_zero, n_pos) of an exact rational symmetric matrix, by Descartes' rule on its characteristic
    polynomial (all roots real)."""
    lam_ = sp.Symbol("lam_")
    P = sp.Poly(M.charpoly(lam_).as_expr(), lam_)
    co = P.all_coeffs()[::-1]
    k0 = 0
    while k0 < len(co) and co[k0] == 0:
        k0 += 1
    rest = co[k0:]

    def changes(seq):
        sg = [1 if c > 0 else -1 for c in seq if c != 0]
        return sum(1 for x_, y_ in zip(sg, sg[1:]) if x_ != y_)
    pos = changes(rest[::-1])
    neg = changes([c * (-1) ** i for i, c in enumerate(rest)][::-1])
    return (neg, k0, pos)


def haynsworth_check(trials=12, seed=7):
    """In(H) = In(H_WW) + In(H_cc - H_cW H_WW^-1 H_Wc) for random exact rational symmetric H with invertible H_WW."""
    import random
    rnd = random.Random(seed)
    ok = True
    for _ in range(trials):
        nW, nc = 4, 3
        Mx = sp.Matrix(nW + nc, nW + nc, lambda i, j: sp.Rational(rnd.randint(-9, 9), rnd.randint(1, 5)))
        H = (Mx + Mx.T) / 2
        HWW, HWc, Hcc = H[:nW, :nW], H[:nW, nW:], H[nW:, nW:]
        if HWW.det() == 0:
            continue
        S = Hcc - HWc.T * HWW.inv() * HWc
        i1, i2, i3 = _inertia(H), _inertia(HWW), _inertia(S)
        ok = ok and i1 == tuple(x_ + y_ for x_, y_ in zip(i2, i3))
    return ok


# ---- 8. the frozen Paper 2 spectrum on the T2g curve and the complementary index -----------------------------------------
# Theorem (index) of Paper 2 (FROZEN INPUT), part (d), on the physical curve 0 < q < q_c, p = P_T(q). Each row: the
# block, its dimension in R^24, its sign on the curve, whether it is a rigid motion or the critical T2g triple, and the
# frozen source. Signs are quoted, not computed.
FROZEN_SPECTRUM_ON_CURVE = (
    {"block": "A1g", "dim": 1, "sign": "+", "kind": "noncritical", "source": "Paper 2 Lemma S"},
    {"block": "Eg", "dim": 2, "sign": "+", "kind": "noncritical", "source": "Paper 2 Lemma S"},
    {"block": "T1g (rotations)", "dim": 3, "sign": "0", "kind": "rigid", "source": "Paper 2 setup (rigid modes); "
     "T1g occurs once in R^24 and is the rotation space"},
    {"block": "T2g lower (critical)", "dim": 3, "sign": "0", "kind": "critical", "source": "Paper 2 Lemma T3 "
     "(D(P_T(q), q) = 0) and Lemma T1"},
    {"block": "T2g upper (noncritical copy)", "dim": 3, "sign": "+", "kind": "noncritical",
     "source": "Paper 2 Lemma T1 (tr K > 0, lambda_+ > 0)"},
    {"block": "A2u", "dim": 1, "sign": "-", "kind": "noncritical", "source": "Paper 2 Lemma T4 (D <= 0 implies "
     "lambda_A2u < 0)"},
    {"block": "Eu", "dim": 2, "sign": "-", "kind": "noncritical", "source": "Paper 2 Lemma E"},
    {"block": "T1u (translations)", "dim": 3, "sign": "0", "kind": "rigid", "source": "Paper 2 setup (rigid modes)"},
    {"block": "T1u (internal)", "dim": 3, "sign": "+", "kind": "noncritical", "source": "Paper 2 Lemma S"},
    {"block": "T2u", "dim": 3, "sign": "+", "kind": "noncritical", "source": "Paper 2 Lemma S"},
)


def complementary_index(table=FROZEN_SPECTRUM_ON_CURVE):
    """Counts from the frozen table: total dimension, rigid, critical, and the inertia of H on W (the noncritical
    complement in the slice). m_perp is derived here, not assumed."""
    dims = sum(r["dim"] for r in table)
    rigid = sum(r["dim"] for r in table if r["kind"] == "rigid")
    crit = sum(r["dim"] for r in table if r["kind"] == "critical")
    W = [r for r in table if r["kind"] == "noncritical"]
    neg = sum(r["dim"] for r in W if r["sign"] == "-")
    pos = sum(r["dim"] for r in W if r["sign"] == "+")
    zer = sum(r["dim"] for r in W if r["sign"] == "0")
    return {"total_dim": dims, "rigid": rigid, "critical": crit, "W_dim": neg + pos + zer, "m_perp": neg,
            "W_positive": pos, "W_zero": zer, "W_invertible": zer == 0,
            "paper2_index_on_curve": neg, "paper2_nullity_on_curve": crit}


def paper2_index_formula(q_ge_rstar, p_gt_PA, q_ge_qc, p_gt_PT):
    """Paper 2 Theorem (index)(b): ind H_red = 2 + 1{q >= r* or p > P_A(q)} + 3 * 1{q >= q_c or p > P_T(q)}."""
    return 2 + int(q_ge_rstar or p_gt_PA) + 3 * int(q_ge_qc or p_gt_PT)


def paper2_curve_consistency():
    """On the physical curve (q < q_c, p = P_T(q)): Lemma T4 gives P_T(q) > P_A(q) for q < r*, so the indicator
    {q >= r* or p > P_A(q)} is 1 in both cases q < r* and r* <= q < q_c, and {p > P_T(q)} is 0: index 3. Adjacent:
    p slightly above P_T: 6 = 3 + 3 (the critical triple turns negative); slightly below: 3."""
    on = {paper2_index_formula(qr, True, False, False) for qr in (False, True)}
    above = {paper2_index_formula(qr, True, False, True) for qr in (False, True)}
    below = {paper2_index_formula(qr, True, False, False) for qr in (False, True)}
    return {"on_curve": on, "above": above, "below": below,
            "m_perp_constant_3": on == {3} and below == {3} and above == {6}}


def full_index_corollary(centre_index=1, table=FROZEN_SPECTRUM_ON_CURVE):
    ci = complementary_index(table)
    if not ci["W_invertible"] or ci["W_dim"] != 15 or ci["rigid"] != 6 or ci["critical"] != 3:
        return None
    return {"m_perp": ci["m_perp"], "full_slice_index": ci["m_perp"] + centre_index,
            "full_slice_nullity": 0, "hessian_R24_zero_eigenvalues": ci["rigid"]}


# ---- 9. conjugate branches --------------------------------------------------------------------------------------------
def conjugate_branches():
    """G3-orbit of (1,0,0) and, in R^24 with symbolic n, the O_h-orbit of e_1."""
    orbit3 = {tuple(T * AXIS) for T in g3_group()}
    e = [_e_vec24(k) for k in range(3)]
    images = set()
    for R in oh_matrices():
        img = (D24(R) * e[0]).applyfunc(sp.expand)
        hit = None
        for k in range(3):
            for sg in (1, -1):
                if (img - sg * e[k]).applyfunc(sp.expand) == sp.zeros(24, 1):
                    hit = (k, sg)
        images.add(hit)
    expected = {(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)}
    return {"orbit3": orbit3, "orbit3_ok": orbit3 == expected, "orbit24": images,
            "orbit24_ok": images == {(k, sg) for k in range(3) for sg in (1, -1)},
            "index_types": 1}


def congruence_preserves_inertia():
    """For an invariant function F, Hess F(T a) = T Hess F(a) T^T with T orthogonal; checked symbolically for the
    generic invariant polynomial of degree <= 4 at a generic point and all 24 T."""
    V, _ = generic_invariant_V(4)
    H = sp.hessian(V, A)
    pt = {a1: sp.Rational(2, 3), a2: -sp.Rational(1, 5), a3: sp.Rational(3, 7)}
    ok = True
    for T in g3_group():
        img = T * sp.Matrix([pt[a1], pt[a2], pt[a3]])
        lhs = H.subs({a1: img[0], a2: img[1], a3: img[2]}, simultaneous=True)
        rhs = T * H.subs(pt) * T.T
        ok = ok and (lhs - rhs).applyfunc(sp.expand) == sp.zeros(3)
    return ok


# ---- 10. D3d consistency (not a new proposition) ------------------------------------------------------------------------
def d3d_consistency():
    """On a = t(1,1,1): Hess = lam I + kappa t (J - I) + O(t^2); the axial equation gives lam = -kappa t + O(t^2), and
    with lam = tau mu + O(mu^2): kappa t = -tau mu + O(mu^2). Eigenvalues: axial kappa t + O(t^2), transverse (double)
    -2 kappa t + O(t^2). Centre index: 2 for mu > 0, 1 for mu < 0 (tau < 0). Local degree bookkeeping with the
    known critical points (cube, 4 D3d, 6 D2h): sum (-1)^index = -3 on both sides."""
    t = sp.Symbol("t", real=True)
    V = LAM * I2 / 2 + KAP * I3 + ALPHA * I2 ** 2 + BETA * I4
    H = sp.hessian(V, A).subs({a1: t, a2: t, a3: t})
    v = sp.expand(V.subs({a1: t, a2: t, a3: t}))
    lam_branch = sp.solve(sp.expand(sp.diff(v, t) / t).subs({ALPHA: 0, BETA: 0}), LAM)[0]   # leading order
    Hb = H.subs(LAM, lam_branch).subs({ALPHA: 0, BETA: 0})
    ax = sp.Matrix([1, 1, 1]) / sp.sqrt(3)
    tr = sp.Matrix([1, -1, 0]) / sp.sqrt(2)
    ev_ax = sp.simplify((ax.T * Hb * ax)[0, 0])
    ev_tr = sp.simplify((tr.T * Hb * tr)[0, 0])
    # kappa t = -tau mu at leading order; with tau < 0, sign(kappa t) = sign(mu). Count negative leading eigenvalues
    # (axial kappa t once, transverse -2 kappa t twice), evaluated with kappa = 1 and t = sign(mu).
    def cidx(mu_sign):
        vals = [ev_ax.subs({KAP: 1, t: mu_sign})] + 2 * [ev_tr.subs({KAP: 1, t: mu_sign})]
        return sum(1 for v_ in vals if v_ < 0)
    c_plus, c_minus = cidx(1), cidx(-1)
    deg_plus = (-1) ** 3 + 4 * (-1) ** c_plus + 6 * (-1) ** 1
    deg_minus = (-1) ** 0 + 4 * (-1) ** c_minus
    return {"lam_on_D3d_branch": lam_branch, "axial": ev_ax, "transverse": ev_tr,
            "axial_ok": sp.simplify(ev_ax - KAP * t) == 0, "transverse_ok": sp.simplify(ev_tr + 2 * KAP * t) == 0,
            "centre_index_mu_pos": c_plus, "centre_index_mu_neg": c_minus,
            "full_index_mu_pos": 3 + c_plus, "full_index_mu_neg": 3 + c_minus,
            "degree_sum_mu_pos": deg_plus, "degree_sum_mu_neg": deg_minus,
            "degree_consistent": deg_plus == deg_minus}


# ---- 11. statements, dependency graph, validators ------------------------------------------------------------------
STATUS_PROVED = "PROVED (computer-assisted; not independently audited)"
ALLOWED_PROOF_STATUSES = ("VERIFIED-EXACT", "CERTIFIED", "FROZEN INPUT", "STANDARD", "PROVED (computer-assisted)")
FORBIDDEN_PROOF_STATUSES = ("VERIFIED-NUMERIC", "CANDIDATE", "RECONNAISSANCE", "ASSUMED")

PROPOSITION_B3 = {
    "name": "Proposition B3",
    "scope": "fixed q in (0, q_c); 0 < mu < mu_1(q); the D2h equilibria x_+-(mu) of Proposition B2",
    "reduced_potential": "V0 + lam*I2/2 + kappa*I3 + alpha*I2**2 + beta*I4",
    "reduced_potential_remainder": "O(|a|^5); lam = tau mu + O(mu^2); coefficients analytic in mu",
    "invariant_dimensions": {2: 1, 3: 1, 4: 2},
    "alpha_plus_beta": "c4/24",
    "hessian_offdiagonal_axial_zero": True,
    "hessian_h22_equals_h33": True,
    "hessian_h11": "c4*s**2/3",
    "hessian_d": "-4*beta*s**2",
    "hessian_e": "kappa*s",
    "transverse_det": "-kappa**2*s**2",
    "transverse_eigenvectors": "(0, 1, 1)/sqrt2 and (0, 1, -1)/sqrt2 (exact)",
    "transverse_block": "indefinite",
    "centre_index": 1,
    "centre_nullity": 0,
    "centre_index_uses_axial_curvature_only": False,
    "independent_of_kappa_gauge": True,
    "independent_of_s_sign": True,
    "conjugate_branch_points": 6,
    "index_types_among_conjugates": 1,
    "claims_full_space_stability": False,
    "claims_stability": False,
    "rigor": "analytic given the certified/audited inputs (Taylor remainder bound, no explicit radius); "
             "computer-assisted overall through Lemma K and Lemma Q; no interval arithmetic in B2.5",
    "status": STATUS_PROVED,
    "dependency_root": "P_B3",
}

COROLLARY_B3 = {
    "name": "Corollary B3'",
    "scope": "fixed q in (0, q_c); 0 < mu < mu_2(q) <= mu_1(q); the D2h equilibria x_+-(mu)",
    "m_perp": 3,
    "m_perp_source": "derived from FROZEN_SPECTRUM_ON_CURVE (Paper 2 Theorem (index) (b)-(d))",
    "m_perp_assumed": False,
    "m_perp_constant_along_curve": True,
    "full_slice_index": 4,
    "full_slice_nullity": 0,
    "R24_negative_eigenvalues": 4,
    "R24_zero_eigenvalues": 6,
    "rigid_motions_counted": False,
    "stable": False,
    "claims_full_space_stability": False,
    "status": STATUS_PROVED,
    "dependency_root": "C_B3",
}

_TESTS = "tests/test_B2_index.py"
ALLOWED_INPUTS_B3 = {
    "IN_exact_Oh_T2g_structure": "VERIFIED-EXACT",
    "IN_lemma_K_kappa": "CERTIFIED",
    "IN_proposition_B2": "PROVED (computer-assisted)",
    "STD_LS_centre_manifold": "STANDARD",
}
ALLOWED_INPUTS_COR = dict(ALLOWED_INPUTS_B3, P2_theorem_index_on_curve="FROZEN INPUT")

DEPENDENCY_GRAPH = {
    "proposition": "Proposition B3 and Corollary B3'",
    "roots": {"P_B3": sorted(ALLOWED_INPUTS_B3), "C_B3": sorted(ALLOWED_INPUTS_COR)},
    "nodes": [
        {"id": "P_B3", "role": "proposition", "status": STATUS_PROVED,
         "statement": "centre-manifold (3-D LS reduced) Hessian at x_+- has index 1, nullity 0", "source": "NOTES.md §13"},
        {"id": "C_B3", "role": "corollary", "status": STATUS_PROVED,
         "statement": "full-slice index 4 (= m_perp + 1, m_perp = 3 derived), nullity 0 modulo the 6 rigid motions",
         "source": "NOTES.md §13.7"},
        {"id": "S1_invariant_normal_form", "role": "step", "status": "VERIFIED-EXACT",
         "statement": "V_red = V0 + lam I2/2 + kappa I3 + alpha I2^2 + beta I4 + O(|a|^5); invariant dimensions 0,1,1,2 "
                      "in degrees 1-4; kappa(0) = D3V[e1,e2,e3]",
         "source": "b2_index.invariant_dimensions, invariant_basis_check", "tests": _TESTS},
        {"id": "S2_axis_hessian_structure", "role": "step", "status": "VERIFIED-EXACT",
         "statement": "Hess V_red(s,0,0) = [[h11,0,0],[0,d,e],[0,e,d]]; h11, d even, e odd in s; h11 = lam + 12(alpha+"
                      "beta)s^2 + O(s^4), d = lam + 4 alpha s^2 + O(s^4), e = kappa s + O(s^3)",
         "source": "b2_index.commutant_on_axis, parity_on_axis, generic_invariant_hessian", "tests": _TESTS},
        {"id": "S3_identification_with_B2", "role": "step", "status": "VERIFIED-EXACT",
         "statement": "V_red(s,0,0,mu) is the axial reduced potential of Proposition B2 (equivariance and uniqueness of "
                      "w); x_+- are critical points of V_red; alpha + beta = c4/24",
         "source": "NOTES.md §13.2; b2_index.ls_quartic_exact", "tests": _TESTS},
        {"id": "S4_branch_hessian", "role": "step", "status": "VERIFIED-EXACT",
         "statement": "on the branch: h11 = (c4/3) s^2 + O(s^4) = -2 tau mu + O(mu^2), d = -4 beta s^2 + O(s^4), "
                      "e = kappa s + O(s^3), det(transverse) = -kappa^2 s^2 + O(s^4)",
         "source": "b2_index.branch_hessian_series", "tests": _TESTS},
        {"id": "S5_transverse_inertia", "role": "step", "status": "VERIFIED-EXACT",
         "statement": "eigenvalues d +- e on (0,1,+-1)/sqrt2; remainder bound: opposite signs for 0 < |s| < |kappa|/"
                      "(C_D + C_E), independent of the signs of kappa and s",
         "source": "b2_index.transverse_eigensystem, transverse_sign_bound", "tests": _TESTS},
        {"id": "S6_centre_index", "role": "step", "status": "VERIFIED-EXACT",
         "statement": "index(Hess V_red) = 0 (h11 > 0) + 1 (transverse) = 1, nullity 0",
         "source": "b2_index.centre_index_from_signs", "tests": _TESTS},
        {"id": "S7_conjugates", "role": "step", "status": "VERIFIED-EXACT",
         "statement": "the six D2h branch points form one orbit; Hessians congruent; one index type",
         "source": "b2_index.conjugate_branches, congruence_preserves_inertia", "tests": _TESTS},
        {"id": "S8_ls_quartic", "role": "step", "status": "VERIFIED-EXACT",
         "statement": "complete invariant quartic V4 = (1/24)D4V[x^4] - (1/8)<b, H_W^-1 b> = alpha I2^2 + beta I4 "
                      "(generic pair potential); multi-dimensional LS quartic formula",
         "source": "b2_index.ls_quartic_exact, generic_ls_multid", "tests": _TESTS},
        {"id": "C1_complementary_index", "role": "step", "status": "VERIFIED-EXACT",
         "statement": "m_perp = 3 by counting the frozen block signs on the curve (Eu x2, A2u x1 negative; rigid and "
                      "critical excluded); H_WW invertible; constant along 0 < q < q_c",
         "source": "b2_index.complementary_index, paper2_curve_consistency", "tests": _TESTS},
        {"id": "C2_index_splitting", "role": "step", "status": "VERIFIED-EXACT",
         "statement": "ind H_slice(x) = ind H_WW(x) + ind Hess V_red(a); D2V_red = Schur complement; rigid tangent in "
                      "ker H(x); inertia of H_WW(x) = inertia at (y*, P_T(q)) for small mu",
         "source": "b2_index.schur_hessian_identity, haynsworth_check", "tests": _TESTS},
        {"id": "IN_exact_Oh_T2g_structure", "role": "input", "status": "VERIFIED-EXACT",
         "allowed_input": "exact Oh/T2g invariant structure",
         "statement": "B0: T(R) = sigma(R) R on the critical T2g coordinates; I3 invariant; B2.0: Sigma = Stab(e_1), "
                      "N(Sigma) minus Sigma reverses e_1; O_h acts orthogonally on R^24 and V is invariant",
         "includes": ["B0 (NOTES.md §4)", "B2.0 (NOTES.md §6.1)", "exact isotypic projectors (group.py)"],
         "source": "NOTES.md §4, §6.1", "tests": "tests/test_B0_t2g.py, tests/test_B2_symmetry.py"},
        {"id": "IN_lemma_K_kappa", "role": "input", "status": "CERTIFIED",
         "allowed_input": "audited kappa != 0",
         "statement": "Lemma K: kappa(q) != 0 for 0 < q < q_c (kappa > 0 in the gauge n_u > 0); CERTIFIED, "
                      "independently audited, erratum closed",
         "audit": "INDEPENDENTLY AUDITED (NOTES.md §5.11, §11)",
         "source": "NOTES.md §5.7, §5.11, §11", "tests": "tests/test_B1_certificate.py"},
        {"id": "IN_proposition_B2", "role": "input", "status": "PROVED (computer-assisted)",
         "allowed_input": "audited Proposition B2 branch/amplitude result",
         "statement": "Proposition B2: x_+-(mu) exist for mu > 0, s*^2 = -6 tau mu/c4 + O(mu^2), tau < 0, c4 > 0, "
                      "axial reduced curvature -2 tau mu + O(mu^2) > 0",
         "includes": ["Lemma Q (B2.3) and tau < 0 (B1.8), as recorded in its own graph (data/B2_4_dependency_graph"
                      ".json)"],
         "audit": "designated an established (independently audited) input by the author's B2.5 request; the audit "
                  "report is not in this package, so NOTES.md §12 keeps its label",
         "source": "NOTES.md §12", "tests": "tests/test_B2_branch.py"},
        {"id": "STD_LS_centre_manifold", "role": "input", "status": "STANDARD",
         "allowed_input": "standard Lyapunov-Schmidt/centre-manifold theory",
         "statement": "equivariant Lyapunov-Schmidt reduction with a three-dimensional kernel on the slice transverse "
                      "to the rigid motions; the reduced Hessian is the Schur complement and the Morse index splits "
                      "(Haynsworth inertia additivity); analytic implicit function theorem; Taylor's theorem",
         "includes": ["slice: critical points of V on y* + R^perp near y* are critical points of V (V is E(3)-"
                      "invariant, grad V(x) is orthogonal to the rigid orbit at x)",
                      "rigid tangent fields lie in the kernel of the Hessian at a critical point",
                      "Golubitsky, Stewart & Schaeffer Vol. II Ch. XIII; Haynsworth (1968), Linear Algebra Appl. 1"],
         "source": "textbook"},
        {"id": "P2_theorem_index_on_curve", "role": "input", "status": "FROZEN INPUT",
         "allowed_input": "explicitly named frozen Paper 2 spectral results",
         "statement": "Paper 2 Theorem (index) (b)-(d) on p = P_T(q), 0 < q < q_c: Eu < 0 (Lemma E); A1g, Eg, T1u int, "
                      "T2u > 0 (Lemma S); upper T2g > 0 (Lemma T1); lower T2g = 0 (Lemma T3); A2u < 0 (Lemma T4); "
                      "rigid modes excluded (Hred on R(x)^perp)",
         "source": "Paper 2 manuscript §5 (Theorem index, Table regions), §2 (Hred)"},
    ],
    "edges": [
        ["P_B3", "S6_centre_index"], ["P_B3", "S7_conjugates"], ["P_B3", "S8_ls_quartic"],
        ["S6_centre_index", "S4_branch_hessian"], ["S6_centre_index", "S5_transverse_inertia"],
        ["S6_centre_index", "IN_lemma_K_kappa"], ["S6_centre_index", "IN_proposition_B2"],
        ["S5_transverse_inertia", "S4_branch_hessian"], ["S5_transverse_inertia", "IN_lemma_K_kappa"],
        ["S5_transverse_inertia", "STD_LS_centre_manifold"],
        ["S4_branch_hessian", "S2_axis_hessian_structure"], ["S4_branch_hessian", "S3_identification_with_B2"],
        ["S4_branch_hessian", "IN_proposition_B2"],
        ["S3_identification_with_B2", "IN_proposition_B2"], ["S3_identification_with_B2", "STD_LS_centre_manifold"],
        ["S3_identification_with_B2", "IN_exact_Oh_T2g_structure"], ["S3_identification_with_B2", "S8_ls_quartic"],
        ["S2_axis_hessian_structure", "S1_invariant_normal_form"],
        ["S2_axis_hessian_structure", "IN_exact_Oh_T2g_structure"],
        ["S1_invariant_normal_form", "IN_exact_Oh_T2g_structure"],
        ["S1_invariant_normal_form", "STD_LS_centre_manifold"],
        ["S8_ls_quartic", "IN_exact_Oh_T2g_structure"], ["S8_ls_quartic", "STD_LS_centre_manifold"],
        ["S7_conjugates", "IN_exact_Oh_T2g_structure"], ["S7_conjugates", "S6_centre_index"],
        ["C_B3", "P_B3"], ["C_B3", "C1_complementary_index"], ["C_B3", "C2_index_splitting"],
        ["C1_complementary_index", "P2_theorem_index_on_curve"],
        ["C2_index_splitting", "STD_LS_centre_manifold"], ["C2_index_splitting", "C1_complementary_index"],
    ],
    "corroboration_only": [
        {"id": "N_B25_hessian", "status": "VERIFIED-NUMERIC",
         "statement": "raw 24x24 Hessian at located D2h equilibria (spectrum, Schur complement onto E_c)",
         "source": "data/B2_5_index.json"},
        {"id": "N_B25_quartic_route3", "status": "VERIFIED-NUMERIC",
         "statement": "derivative-free nonlinear LS evaluation of V4", "source": "data/B2_5_index.json"},
        {"id": "N_B25_d3d", "status": "VERIFIED-NUMERIC",
         "statement": "D3d consistency numerics (not a proof of anything)", "source": "data/B2_5_index.json"},
        {"id": "N_B22_scan", "status": "VERIFIED-NUMERIC", "statement": "B2.2 scan (reconnaissance)",
         "source": "NOTES.md §7"},
    ],
    "consistency_only": [
        {"id": "K_d3d_consistency", "status": "VERIFIED-EXACT",
         "statement": "same normal form on the D3d axis: axial kappa t, transverse -2 kappa t (x2); not a proposition",
         "source": "b2_index.d3d_consistency"},
    ],
}


def _adj(graph):
    adj = {}
    for a, b in graph["edges"]:
        adj.setdefault(a, []).append(b)
    return adj


def _reachable(graph, root):
    adj = _adj(graph)
    seen, stack = set(), [root]
    while stack:
        v = stack.pop()
        if v in seen:
            continue
        seen.add(v)
        stack.extend(adj.get(v, []))
    return seen


def _acyclic(graph):
    adj = _adj(graph)
    state = {}

    def visit(v):
        if state.get(v) == 1:
            return False
        if state.get(v) == 2:
            return True
        state[v] = 1
        ok = all(visit(w) for w in adj.get(v, []))
        state[v] = 2
        return ok
    return all(visit(v) for v in list(adj))


def validate_graph(graph=None):
    """Failures (empty = valid). For each root (P_B3, C_B3): every reachable node other than roots is a VERIFIED-EXACT
    derivation step or one of that root's allowed inputs with its expected status; all its allowed inputs are
    reachable; no corroboration-only, consistency-only, numeric, candidate or assumed node is reachable; the graph is
    acyclic. P_B3 must not reach the Paper 2 spectral input (the centre index does not use it)."""
    graph = DEPENDENCY_GRAPH if graph is None else graph
    fails = []
    nodes = {n["id"]: n for n in graph["nodes"]}
    corr = {n["id"] for n in graph.get("corroboration_only", [])} | {n["id"] for n in graph.get("consistency_only", [])}
    for a, b in graph["edges"]:
        for v in (a, b):
            if v not in nodes and v not in corr:
                fails.append(f"edge references unknown node {v}")
    if not _acyclic(graph):
        fails.append("dependency graph has a cycle")
    allowed_by_root = {"P_B3": ALLOWED_INPUTS_B3, "C_B3": ALLOWED_INPUTS_COR}
    for root, allowed in allowed_by_root.items():
        if root not in nodes:
            fails.append(f"root {root} missing")
            continue
        reach = _reachable(graph, root)
        for v in sorted(reach):
            if v in allowed_by_root:
                continue
            if v in corr:
                fails.append(f"{root}: corroboration/consistency-only node {v} is a proof dependency")
                continue
            nd = nodes.get(v, {})
            st, role = nd.get("status"), nd.get("role")
            if st in FORBIDDEN_PROOF_STATUSES:
                fails.append(f"{root}: node {v} has forbidden proof status {st}")
            elif st not in ALLOWED_PROOF_STATUSES:
                fails.append(f"{root}: node {v} has unknown status {st}")
            if role == "step":
                if st != "VERIFIED-EXACT":
                    fails.append(f"{root}: derivation step {v} is not VERIFIED-EXACT")
            elif v not in allowed:
                fails.append(f"{root}: node {v} is not an allowed input {sorted(allowed)}")
            elif st != allowed[v]:
                fails.append(f"{root}: allowed input {v} has status {st}, expected {allowed[v]}")
            text = (nd.get("statement", "") + " " + nd.get("source", "")).lower()
            if "scan" in text or "numeric" in text or "assum" in text:
                fails.append(f"{root}: node {v} describes a numerical scan or an assumption")
        for req in allowed:
            if req not in reach:
                fails.append(f"{root}: required dependency {req} not reachable")
        if nodes[root].get("status") != STATUS_PROVED:
            fails.append(f"{root}: status is not {STATUS_PROVED!r}")
    if "P2_theorem_index_on_curve" in _reachable(graph, "P_B3"):
        fails.append("P_B3 must not depend on the Paper 2 spectral input")
    return fails


def _parse(expr):
    loc = {"tau": TAU, "kappa": KAP, "c4": C4, "mu": mu, "s": s, "lam": LAM, "alpha": ALPHA, "beta": BETA,
           "I2": I2, "I3": I3, "I4": I4, "V0": sp.Symbol("V0"), "a1": a1, "a2": a2, "a3": a3}
    return sp.sympify(expr, locals=loc)


def derived_statement():
    br = branch_hessian_series(6)
    gi = generic_invariant_hessian(6)
    c4sym = 24 * (ALPHA + BETA)
    lead_plus = sp.expand(br["d"] + br["e"]).coeff(s, 1)
    lead_minus = sp.expand(br["d"] - br["e"]).coeff(s, 1)
    indefinite = sp.simplify(lead_plus + lead_minus) == 0 and lead_plus != 0
    cj = conjugate_branches()
    cor = full_index_corollary(centre_index_from_signs(">0"))
    return {
        "reduced_potential": sp.Symbol("V0") + LAM * I2 / 2 + KAP * I3 + ALPHA * I2 ** 2 + BETA * I4,
        "invariant_dimensions": {d: invariant_dimensions(4)[d] for d in (2, 3, 4)},
        "alpha_plus_beta": C4 / 24,
        "hessian_offdiagonal_axial_zero": gi["structure"] and br["offdiag_zero"],
        "hessian_h11": (C4 / 3 * s ** 2, br["h11"], c4sym),
        "hessian_d": br["d"], "hessian_e": br["e"], "transverse_det": br["det"],
        "transverse_block": "indefinite" if indefinite else "definite",
        "centre_index": centre_index_from_signs(">0"), "centre_nullity": 0,
        "conjugate_branch_points": len(cj["orbit3"]), "index_types_among_conjugates": cj["index_types"],
        "m_perp": complementary_index()["m_perp"], "full_slice_index": cor["full_slice_index"] if cor else None,
        "R24_zero_eigenvalues": complementary_index()["rigid"],
    }


def validate_statement(stmt=None, cor=None, graph=None):
    """Failures (empty = valid) of Proposition B3 and Corollary B3' against the exact derivation and the graph."""
    stmt = PROPOSITION_B3 if stmt is None else stmt
    cor = COROLLARY_B3 if cor is None else cor
    graph = DEPENDENCY_GRAPH if graph is None else graph
    d = derived_statement()
    fails = []

    def cmp(key, target):
        try:
            diff = sp.simplify(_parse(stmt[key]) - target)
        except (KeyError, sp.SympifyError, TypeError) as exc:
            fails.append(f"{key}: unparsable or missing ({exc})")
            return
        if diff != 0:
            fails.append(f"{key}: {stmt[key]} differs from the derivation {target}")
    cmp("reduced_potential", d["reduced_potential"])
    cmp("alpha_plus_beta", d["alpha_plus_beta"])
    target_h11, h11_alpha_beta, c4sym = d["hessian_h11"]
    cmp("hessian_h11", target_h11)
    if sp.simplify(_parse(stmt.get("hessian_h11", "0")).subs(C4, c4sym) - h11_alpha_beta) != 0:
        fails.append("hessian_h11 is not the derived (c4/3) s^2 with c4 = 24(alpha + beta)")
    cmp("hessian_d", d["hessian_d"])
    cmp("hessian_e", d["hessian_e"])
    cmp("transverse_det", d["transverse_det"])
    if stmt.get("invariant_dimensions") != d["invariant_dimensions"]:
        fails.append("invariant dimensions differ from the computed ones")
    if stmt.get("hessian_offdiagonal_axial_zero") is not True or not d["hessian_offdiagonal_axial_zero"]:
        fails.append("h12 = h13 = 0 on the axis (exact symmetry)")
    if stmt.get("hessian_h22_equals_h33") is not True:
        fails.append("h22 = h33 on the axis (exact symmetry)")
    if stmt.get("transverse_block") != d["transverse_block"]:
        fails.append(f"transverse block {stmt.get('transverse_block')} differs from the derived {d['transverse_block']}")
    if stmt.get("centre_index") != d["centre_index"] or stmt.get("centre_nullity") != d["centre_nullity"]:
        fails.append(f"centre index/nullity {stmt.get('centre_index')}/{stmt.get('centre_nullity')} differ from the "
                     f"derived {d['centre_index']}/{d['centre_nullity']}")
    if stmt.get("centre_index_uses_axial_curvature_only") is not False:
        fails.append("the centre index needs the transverse block; the axial curvature alone gives index 0")
    for flag in ("independent_of_kappa_gauge", "independent_of_s_sign"):
        if stmt.get(flag) is not True:
            fails.append(f"{flag} must hold (eigenvalues +-kappa s as a set)")
    if (stmt.get("conjugate_branch_points") != d["conjugate_branch_points"]
            or stmt.get("index_types_among_conjugates") != d["index_types_among_conjugates"]):
        fails.append("the six conjugate branch points carry one index type")
    for flag in ("claims_full_space_stability", "claims_stability"):
        if stmt.get(flag) is not False:
            fails.append(f"{flag} must be False: a centre index is not full-space stability")
    if stmt.get("status") != STATUS_PROVED:
        fails.append(f"status {stmt.get('status')!r} is not {STATUS_PROVED!r}")
    # corollary
    if cor.get("m_perp_assumed") is not False or "derived" not in cor.get("m_perp_source", ""):
        fails.append("m_perp must be derived from the frozen Paper 2 spectrum, not assumed")
    if cor.get("m_perp") != d["m_perp"]:
        fails.append(f"m_perp {cor.get('m_perp')} differs from the derived {d['m_perp']}")
    if d["full_slice_index"] is None or cor.get("full_slice_index") != d["full_slice_index"]:
        fails.append(f"full-slice index {cor.get('full_slice_index')} differs from the derived {d['full_slice_index']}")
    if cor.get("R24_negative_eigenvalues") != d["full_slice_index"] or cor.get("full_slice_nullity") != 0:
        fails.append("R^24 negative count must equal the slice index; slice nullity 0")
    if cor.get("rigid_motions_counted") is not False or cor.get("R24_zero_eigenvalues") != d["R24_zero_eigenvalues"]:
        fails.append("rigid motions are zero modes and are not counted in the Morse index")
    if cor.get("stable") is not False or cor.get("claims_full_space_stability") is not False:
        fails.append("index 4 is not stability")
    if cor.get("status") != STATUS_PROVED:
        fails.append("corollary status")
    fails += validate_graph(graph)
    return fails


# ======================================================================================================================
# NUMERIC LAYER (corroboration only; not a proof dependency)
# ======================================================================================================================
def psi_numeric(pp, qq, A_=None):
    """psi^(k)(sigma) for psi(sigma) = A sigma^(-p/2) - sigma^(-q/2), A = t(p, q) (unit-edge equilibrium)."""
    from .numeric import t_eq
    pp, qq = mp.mpf(pp), mp.mpf(qq)
    A_ = t_eq(pp, qq) if A_ is None else A_

    def ff(c, k):
        out = mp.mpf(1)
        for j in range(k):
            out *= (c - j)
        return out
    vals = {}
    for k in range(1, 5):
        for sg in (1, 2, 3):
            vals[ps.PSI[(k, sg)]] = (A_ * ff(-pp / 2, k) * mp.mpf(sg) ** (-pp / 2 - k)
                                     - ff(-qq / 2, k) * mp.mpf(sg) ** (-qq / 2 - k))
    return vals


@lru_cache(maxsize=None)
def _lam_quartic():
    from . import b2_quartic as q4
    from . import t2g
    ab = alpha_beta_closed()
    syms = sorted(ps.PSI.values(), key=str) + [nu, nv, HA, HE, KFF]
    f = q4.linear_forms()
    K = t2g.block_K()[0]
    fvec = sp.Matrix([-nv, nu])
    kff = sp.expand((fvec.T * K * fvec)[0, 0])
    from . import b1_cubic as b1c
    kap = b1c.kappa_form(nu, nv)
    lam = lambda ex: sp.lambdify(syms, ex, "mpmath")
    return {"alpha": lam(ab["alpha"]), "beta": lam(ab["beta"]), "hA": lam(f["hA"]), "hE": lam(f["hE"]),
            "kff": lam(kff), "kappa": lam(kap), "kappa_f": lam(kappa_f()), "q_mix": lam(q_mix()),
            "syms": syms}


def quartic_numeric(cd):
    """alpha, beta, c4 = 24(alpha + beta), d2 = -4 beta, kappa (unit n, gauge n_u > 0) at mu = 0, from the exact forms
    evaluated with the two-term psi at (P_T(q), q)."""
    L = _lam_quartic()
    pv = psi_numeric(cd["p0"], cd["q"])
    base = [pv[sym] for sym in L["syms"][:12]] + [cd["n_u"], cd["n_v"]]
    hA, hE, kff = L["hA"](*base, 1, 1, 1), L["hE"](*base, 1, 1, 1), L["kff"](*base, 1, 1, 1)
    args = base + [hA, hE, kff]
    al, be = L["alpha"](*args), L["beta"](*args)
    return {"alpha": al, "beta": be, "c4": 24 * (al + be), "d2": -4 * be, "kappa": L["kappa"](*args),
            "kappa_f": L["kappa_f"](*args), "q_mix": L["q_mix"](*args), "hA": hA, "hE": hE, "kff": kff}


def _orthonormalise(vecs, against=()):
    out = []
    basis = list(against)
    for v in vecs:
        w = list(v)
        for _ in range(2):
            for b in basis + out:
                c = mp.fsum(x * y for x, y in zip(w, b))
                w = [x - c * y for x, y in zip(w, b)]
        nrm = mp.sqrt(mp.fsum(x * x for x in w))
        if nrm > mp.mpf(10) ** (-(mp.mp.dps // 2)):
            out.append([x / nrm for x in w])
    return out


def slice_basis(n_u, n_v):
    """E_c = [e_1, e_2, e_3], the six orthonormalised rigid fields at y*, and an orthonormal basis of W (15 vectors):
    the slice directions orthogonal to E_c."""
    r2 = mp.sqrt(2)
    E = [[-n_u * mp.mpf(int(c)) / 4 - n_v * r2 * mp.mpf(int(d)) / 4 for c, d in zip(W_T2G[k], U_T2G[k])]
         for k in range(3)]
    rig = _orthonormalise([[mp.mpf(int(c)) for c in v] for v in list(TRANSLATIONS) + list(ROTATIONS)])
    std = [[mp.mpf(1) if i == j else mp.mpf(0) for i in range(24)] for j in range(24)]
    W = _orthonormalise(std, against=E + rig)
    return E, rig, W


def _proj(H, B1, B2):
    M = mp.matrix(len(B1), len(B2))
    HB2 = [[mp.fsum(H[i, j] * b[j] for j in range(24)) for i in range(24)] for b in B2]
    for a, b1 in enumerate(B1):
        for c in range(len(B2)):
            M[a, c] = mp.fsum(b1[i] * HB2[c][i] for i in range(24))
    return M


def _inertia_num(M, tol):
    ev = mp.eigsy(M, eigvals_only=True)
    ev = [ev[i] for i in range(len(ev))]
    return ev, sum(1 for x in ev if x < -tol), sum(1 for x in ev if abs(x) <= tol), sum(1 for x in ev if x > tol)


def hessian_analysis(cd, pp, xv, tol_exp=40):
    """Full 24x24 Hessian at x: spectrum with counts; rigid fields at x in its kernel; the slice decomposition
    (Schur complement onto E_c over W) and the inertia of H_WW and of the Schur complement."""
    from .numeric import PairEnergy
    V = PairEnergy(pp, cd["q"])
    H = V.hessian(xv)
    tol = mp.mpf(10) ** (-tol_exp)
    ev, nneg, nzero, npos = _inertia_num(H, tol)
    pos = [xv[3 * i:3 * i + 3] for i in range(8)]
    rig = []
    for k in range(3):
        rig.append([mp.mpf(1) if c == k else mp.mpf(0) for i in range(8) for c in range(3)])
    for k in range(3):
        f = []
        for P in pos:
            e = [0, 0, 0]
            e[k] = 1
            f += [e[1] * P[2] - e[2] * P[1], e[2] * P[0] - e[0] * P[2], e[0] * P[1] - e[1] * P[0]]
        rig.append(f)
    rig_res = max(mp.sqrt(mp.fsum(mp.fsum(H[i, j] * r[j] for j in range(24)) ** 2 for i in range(24))) for r in rig)
    E, _, W = slice_basis(cd["n_u"], cd["n_v"])
    Hcc, HcW, HWW = _proj(H, E, E), _proj(H, E, W), _proj(H, W, W)
    S = Hcc - HcW * mp.inverse(HWW) * HcW.T
    evW, wneg, wzero, wpos = _inertia_num(HWW, tol)
    evS, sneg, szero, spos = _inertia_num(S, tol)
    y0 = [mp.mpf(c) / 2 for lab in LABELS for c in lab]
    a = [mp.fsum((xv[i] - y0[i]) * E[k][i] for i in range(24)) for k in range(3)]
    return {"spectrum": ev, "neg": nneg, "zero": nzero, "pos": npos, "rigid_residual": rig_res,
            "W_neg": wneg, "W_zero": wzero, "min_abs_W_eig": min(abs(x) for x in evW),
            "schur": S, "schur_eigs": evS, "schur_neg": sneg, "schur_zero": szero, "a": a}


def d2h_point(qq, rel_mu, sign=1, dps=60, cd=None):
    """Locate x_+ (sign = 1) or x_- (sign = -1) by B2.4's Newton in Fix(Sigma) and analyse its 24x24 Hessian."""
    from . import b2_branch as b2
    with mp.workdps(dps):
        cd = b2.curve_data(qq) if cd is None else cd
        bp = b2.branch_point(qq, rel_mu, sign=sign, dps=dps, cd=cd)
        an = hessian_analysis(cd, bp["p"], bp["x"])
        qn = quartic_numeric(cd)
        sv = an["a"][0]
        S = an["schur"]
        pred = {"h11": qn["c4"] / 3 * sv ** 2, "d": qn["d2"] * sv ** 2, "e": qn["kappa"] * sv}
        d_ = (S[1, 1] + S[2, 2]) / 2
        return {"q": cd["q"], "rel_mu": rel_mu, "mu": bp["mu"], "s": sv, "a2": an["a"][1], "a3": an["a"][2],
                "full_gradient_norm": bp["full_gradient_norm"], "neg": an["neg"], "zero": an["zero"],
                "pos": an["pos"], "rigid_residual": an["rigid_residual"], "W_neg": an["W_neg"],
                "min_abs_W_eig": an["min_abs_W_eig"], "schur_neg": an["schur_neg"], "schur_zero": an["schur_zero"],
                "h11": S[0, 0], "d": d_, "e": S[1, 2], "h12": S[0, 1], "h13": S[0, 2], "d_asym": S[1, 1] - S[2, 2],
                "h11_rel_err": S[0, 0] / pred["h11"] - 1, "d_rel_err": d_ / pred["d"] - 1,
                "e_rel_err": S[1, 2] / pred["e"] - 1,
                "transverse_eigs": (d_ + S[1, 2], d_ - S[1, 2]),
                "small_full_eigs": sorted(sorted(an["spectrum"], key=abs)[6:9]),
                "kappa": qn["kappa"], "c4": qn["c4"], "d2": qn["d2"], "tau": cd["tau"]}


def d3d_point(qq, rel_mu, dps=60, cd=None):
    """Locate the D3d equilibrium (Newton in Fix(D3d) = span{e_br, sum uh_k, sum vh_k}, as in B1's corroboration)
    and analyse its 24x24 Hessian; t = <x - y*, e_1> (= a_1 = a_2 = a_3)."""
    from . import b2_branch as b2
    from .numeric import PairEnergy, y_star
    with mp.workdps(dps):
        cd = b2.curve_data(qq) if cd is None else cd
        qn = quartic_numeric(cd)
        pp = cd["p0"] * (1 + mp.mpf(rel_mu))
        m = pp - cd["p0"]
        t_pred = -cd["tau"] * m / qn["kappa"]
        V = PairEnergy(pp, cd["q"])
        y0 = y_star()
        E, _, _ = slice_basis(cd["n_u"], cd["n_v"])
        r2 = mp.sqrt(2)
        su = [mp.fsum(-mp.mpf(int(W_T2G[k][i])) / 4 for k in range(3)) / mp.sqrt(3) for i in range(24)]
        sv = [mp.fsum(-r2 * mp.mpf(int(U_T2G[k][i])) / 4 for k in range(3)) / mp.sqrt(3) for i in range(24)]
        br = [mp.mpf(int(c)) / mp.sqrt(24) for c in E_BR]
        B = [br, su, sv]
        c = mp.matrix([0, t_pred * mp.sqrt(3) * cd["n_u"], t_pred * mp.sqrt(3) * cd["n_v"]])
        for _ in range(60):
            x = [y0[i] + mp.fsum(c[k] * B[k][i] for k in range(3)) for i in range(24)]
            g = V.gradient(x)
            gv = mp.matrix([mp.fsum(g[i] * B[k][i] for i in range(24)) for k in range(3)])
            Hm = _proj(V.hessian(x), B, B)
            step = mp.lu_solve(Hm, gv)
            c -= step
            if mp.norm(step) < mp.mpf(10) ** (-(dps - 8)):
                break
        x = [y0[i] + mp.fsum(c[k] * B[k][i] for k in range(3)) for i in range(24)]
        gn = mp.sqrt(mp.fsum(gi * gi for gi in V.gradient(x)))
        an = hessian_analysis(cd, pp, x)
        t_ = an["a"][0]
        S = an["schur"]
        ax = mp.matrix([1, 1, 1]) / mp.sqrt(3)
        tr = mp.matrix([1, -1, 0]) / mp.sqrt(2)
        return {"q": cd["q"], "rel_mu": rel_mu, "mu": m, "t": t_, "t_pred": t_pred, "full_gradient_norm": gn,
                "neg": an["neg"], "zero": an["zero"], "schur_neg": an["schur_neg"], "W_neg": an["W_neg"],
                "axial": (ax.T * S * ax)[0], "transverse": (tr.T * S * tr)[0], "kappa_t": qn["kappa"] * t_,
                "a_equal": max(abs(an["a"][1] - t_), abs(an["a"][2] - t_))}


def quartic_route3(qq, u, levels=4, r0="1e-3", dps=60, cd=None):
    """Derivative-free check of V4 at mu = 0: for x = y* + r sum u_k e_k + w, w in W solved by Newton
    (P_W grad V = 0, 15 coordinates), the even part [V_red(r) + V_red(-r)]/2 - V(y*) = V4(u) r^4 + O(r^6);
    Richardson extrapolation in r^2 over r = r0 2^-j."""
    from . import b2_branch as b2
    from .numeric import PairEnergy, y_star
    with mp.workdps(dps):
        cd = b2.curve_data(qq) if cd is None else cd
        V = PairEnergy(cd["p0"], cd["q"])
        y0 = y_star()
        E, _, W = slice_basis(cd["n_u"], cd["n_v"])
        nrm = mp.sqrt(mp.fsum(mp.mpf(c) ** 2 for c in u))
        uu = [mp.mpf(c) / nrm for c in u]
        dirv = [mp.fsum(uu[k] * E[k][i] for k in range(3)) for i in range(24)]
        V0 = V.energy(y0)

        def vred(r):
            w = mp.matrix(15, 1)
            for _ in range(40):
                x = [y0[i] + r * dirv[i] + mp.fsum(w[j] * W[j][i] for j in range(15)) for i in range(24)]
                g = V.gradient(x)
                gW = mp.matrix([mp.fsum(g[i] * W[j][i] for i in range(24)) for j in range(15)])
                step = mp.lu_solve(_proj(V.hessian(x), W, W), gW)
                w -= step
                if mp.norm(step) < mp.mpf(10) ** (-(dps - 6)):
                    break
            x = [y0[i] + r * dirv[i] + mp.fsum(w[j] * W[j][i] for j in range(15)) for i in range(24)]
            return V.energy(x)
        rows = []
        for j in range(levels):
            r = mp.mpf(r0) / 2 ** j
            rows.append(((vred(r) + vred(-r)) / 2 - V0) / r ** 4)
        T = [rows]
        for k in range(1, levels):
            prev = T[-1]
            T.append([(4 ** k * prev[i + 1] - prev[i]) / (4 ** k - 1) for i in range(len(prev) - 1)])
        est = T[-1][0]
        qn = quartic_numeric(cd)
        I2v = mp.fsum(x * x for x in uu) ** 2
        I4v = mp.fsum(x ** 4 for x in uu)
        pred = qn["alpha"] * I2v + qn["beta"] * I4v
        return {"q": cd["q"], "u": [str(c) for c in u], "V4_route3": est, "V4_formula": pred,
                "rel_diff": abs(est / pred - 1), "richardson_err": abs(T[-1][0] - T[-2][0])}
