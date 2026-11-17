"""Phase B2.4: Proposition B2, the local D2h-axial pitchfork on the T2g transition curve.

Fix 0 < q < q_c, mu = p - P_T(q). Sigma (order 8, labelled D2h) is the stabiliser of e_1 = n_u uh_1 + n_v vh_1
(B2.0), with n = n(0) the unit kernel vector of K at mu = 0, in the chart gauge n_u > 0. On y* + Fix(Sigma) we use the
orthonormal coordinates (s, wA, wE, wf) along (e_1, A_HAT, E_HAT, f_1), f_1 = -n_v uh_1 + n_u vh_1.

The module has two layers.

EXACT LAYER (proof). Everything below is symbolic (SymPy, exact rational arithmetic); the tests check each item.
  1. generic_ls_reduction: for a GENERIC polynomial energy in (s, wA, wE, wf) that is invariant under
     (s, wA, wE, wf) -> (-s, wA, wE, -wf) (the action of every element of N(Sigma) minus Sigma, B2.0), the
     Lyapunov-Schmidt reduced potential has vanishing odd coefficients, s^2 coefficient (1/2)(kss - ksf^2/kff) (the
     Schur complement) and, when kss = ksf = 0, s^4 coefficient (D^4V[e^4] - 3 b^T H_WW^-1 b)/24.
  2. model_structure: in the model, H on Fix(Sigma) is diag(h_A, h_E) (+) K (generic pair potential), so kss, ksf, kff
     are the entries of K in the (e_1, f_1) basis, the Schur complement is lambda(mu) = det K/(f^T K f), and
     lambda(0) = 0, lambda'(0) = n^T K'(0) n = tau.
  3. reduced_G: dV_red/ds = s G(s^2, mu) with G(z, mu) = lambda(mu) + c4(mu) z/6 + 6 a3(mu) z^2 + ...
  4. ift_branch: from G(0,0) = 0, G_mu = tau, G_z = c4/6: mu*(z) = -c4/(6 tau) z + O(z^2) and its inverse
     s^2 = Z(mu) = -(6 tau/c4) mu + O(mu^2), with the second-order coefficients for a generic G.
  5. branch_side / classify: the side of mu carrying the nontrivial branch and the pitchfork type, derived from the
     signs of tau and c4 (not assumed).
  6. axial_curvature: d^2V_red/ds^2 = G + 2 z G_z: tau mu + O(mu^2) at the cube, -2 tau mu + O(mu^2) at s = +-s*(mu).
  7. isotropy_exact / exchange_exact: every point of y* + Fix(Sigma) with a nonzero (uh_1, vh_1) component has
     isotropy exactly Sigma in O_h; the 8 elements of N(Sigma) minus Sigma act as (s, wf) -> (-s, -wf) and fix
     (wA, wE), so they exchange +s* and -s*.
  8. rhombus_exact: the first-order displacement maps each square cross-section x = const to a rhombus.
  9. PROPOSITION, DEPENDENCY_GRAPH, validate_statement, validate_graph: the machine-readable statement, its proof
     dependency graph and a validator that re-derives every claim from the exact layer and rejects inconsistent
     statements and graphs.

NUMERIC LAYER (corroboration only, never a proof dependency): Newton in the four Fix(Sigma) coordinates with the
24-D pair energy of numeric.py, a reduced scan of dV_red/ds on both sides of the curve, the full 24-D gradient, the
amplitude law and the axial curvature at located points.
"""
import itertools
from functools import lru_cache

import mpmath as mp
import sympy as sp

# ======================================================================================================================
# EXACT LAYER
# ======================================================================================================================
s, wA, wE, wf = sp.symbols("s wA wE wf", real=True)
z, mu = sp.symbols("z mu", real=True)
COORDS = (s, wA, wE, wf)
W_COORDS = (wA, wE, wf)
QUAD = {name: sp.Symbol(name, real=True) for name in ("kss", "ksf", "kff", "hA", "hAE", "hE")}


def _monomials(deg, even=True):
    """Exponent tuples (a, b, c, d) of s^a wA^b wE^c wf^d of total degree deg; with even=True only those with a + d
    even, i.e. the monomials invariant under (s, wf) -> (-s, -wf)."""
    out = []
    for e in itertools.product(range(deg + 1), repeat=4):
        if sum(e) == deg and (not even or (e[0] + e[3]) % 2 == 0):
            out.append(e)
    return out


def generic_even_energy(max_deg=4, break_evenness=False):
    """V(s, wA, wE, wf) = V2 + sum of all Z2-invariant monomials of degree 3..max_deg with independent symbolic
    coefficients, V2 = (kss s^2 + 2 ksf s wf + kff wf^2 + hA wA^2 + 2 hAE wA wE + hE wE^2)/2. Z2 forbids the
    couplings s wA, s wE, wf wA, wf wE. With break_evenness=True one odd monomial (s^3) is added: negative control."""
    k = QUAD
    V = (k["kss"] * s ** 2 + 2 * k["ksf"] * s * wf + k["kff"] * wf ** 2 + k["hA"] * wA ** 2
         + 2 * k["hAE"] * wA * wE + k["hE"] * wE ** 2) / 2
    coeffs = {}
    for deg in range(3, max_deg + 1):
        for e in _monomials(deg):
            c = sp.Symbol("c_%d%d%d%d" % e, real=True)
            coeffs[e] = c
            V += c * s ** e[0] * wA ** e[1] * wE ** e[2] * wf ** e[3]
    if break_evenness:
        V += sp.Symbol("odd_s3", real=True) * s ** 3
    return sp.expand(V), coeffs


def _series_coeff(expr, k):
    return sp.expand(expr).coeff(s, k)


def generic_ls_reduction(V, order=5):
    """Lyapunov-Schmidt reduction of V along s: w(s) = w1 s + w2 s^2 solves grad_W V(s, w(s)) = 0 order by order
    (H_WW w_k = -[known terms]); since grad_W V = 0 along the exact w, an error O(s^3) in w changes V_red only at
    O(s^6), so V_red(s) = V(s, w1 s + w2 s^2) is exact through s^5. Returns the coefficients of V_red up to s^order
    and the coefficient vectors w1, w2."""
    if order > 5:
        raise ValueError("w is computed through s^2; V_red is exact through s^5 only")
    HWW = sp.Matrix(3, 3, lambda i, j: sp.diff(V, W_COORDS[i], W_COORDS[j]).subs({c: 0 for c in COORDS}))
    Hinv = HWW.inv()
    w = [sp.Integer(0)] * 3
    sol = []
    for kk in (1, 2):
        a = sp.symbols(f"a{kk}_0:3")
        trial = [w[i] + a[i] * s ** kk for i in range(3)]
        sub = dict(zip(W_COORDS, trial))
        eqs = [_series_coeff(sp.diff(V, W_COORDS[i]).subs(sub, simultaneous=True), kk) for i in range(3)]
        # the equations are H_WW a + r = 0 with r independent of a
        r = sp.Matrix([e.subs({ai: 0 for ai in a}) for e in eqs])
        lin = sp.Matrix(3, 3, lambda i, j: sp.diff(eqs[i], a[j]))
        if sp.simplify(lin - HWW) != sp.zeros(3, 3):
            raise ArithmeticError("order-k equation is not H_WW a + r")
        ak = (-Hinv * r).applyfunc(sp.simplify)
        sol.append(ak)
        w = [w[i] + ak[i] * s ** kk for i in range(3)]
    Vred = sp.expand(V.subs(dict(zip(W_COORDS, w)), simultaneous=True))
    coeffs = {kk: sp.simplify(_series_coeff(Vred, kk)) for kk in range(order + 1)}
    return {"coefficients": coeffs, "w1": sol[0], "w2": sol[1], "H_WW": HWW}


def ls_formula_quartic(V):
    """(D^4V[e^4] - 3 b^T H_WW^-1 b)/24 computed directly from the derivatives of V at 0 (b_i = d^3V/ds^2 dw_i),
    without the series route."""
    at0 = {c: 0 for c in COORDS}
    HWW = sp.Matrix(3, 3, lambda i, j: sp.diff(V, W_COORDS[i], W_COORDS[j]).subs(at0))
    b = sp.Matrix([sp.diff(V, s, 2, W_COORDS[i]).subs(at0) for i in range(3)])
    V4 = sp.diff(V, s, 4).subs(at0)
    return sp.simplify((V4 - 3 * (b.T * HWW.inv() * b)[0, 0]) / 24), b


@lru_cache(maxsize=None)
def generic_ls_checks():
    """The exact LS facts for the generic Z2-invariant energy (cached; used by the tests and the validator)."""
    V, _ = generic_even_energy(4)
    red = generic_ls_reduction(V, 5)
    k = QUAD
    co = red["coefficients"]
    schur = k["kss"] - k["ksf"] ** 2 / k["kff"]
    at_crit = {k["kss"]: 0, k["ksf"]: 0}
    V0 = V.subs(at_crit)
    red0 = generic_ls_reduction(V0, 5)
    quart_formula, b = ls_formula_quartic(V0)
    hab = sp.Matrix([[k["hA"], k["hAE"]], [k["hAE"], k["hE"]]])
    w2_AE_expected = (-hab.inv() * sp.Matrix([b[0], b[1]]) / 2).applyfunc(sp.simplify)
    return {
        "odd_coefficients_vanish": all(sp.simplify(co[kk]) == 0 for kk in (1, 3, 5)),
        "constant_term_zero": sp.simplify(co[0]) == 0,
        "s2_coefficient_is_half_schur": sp.simplify(co[2] - schur / 2) == 0,
        "s4_coefficient_at_mu0_is_ls_formula": sp.simplify(red0["coefficients"][4] - quart_formula) == 0,
        "w1_has_only_wf_component": sp.simplify(red["w1"][0]) == 0 and sp.simplify(red["w1"][1]) == 0,
        "w1_wf_is_minus_ksf_over_kff": sp.simplify(red["w1"][2] + k["ksf"] / k["kff"]) == 0,
        "w2_has_no_wf_component": sp.simplify(red["w2"][2]) == 0,
        "w1_vanishes_at_mu0": all(sp.simplify(x) == 0 for x in red0["w1"]),
        "w2_AE_at_mu0_is_minus_half_Hinv_b": all(sp.simplify(red0["w2"][i] - w2_AE_expected[i]) == 0
                                                for i in range(2)),
        "w2_wf_at_mu0_zero": sp.simplify(red0["w2"][2]) == 0,
    }


def evenness_breaking_detected():
    """Negative control: with one odd monomial s^3 added, the reduced potential acquires an odd coefficient."""
    V, _ = generic_even_energy(3, break_evenness=True)
    red = generic_ls_reduction(V, 3)
    return sp.simplify(red["coefficients"][3]) != 0


# ---- 2. the model: H on Fix(Sigma), the Schur complement and tau ----------------------------------------------------
def model_structure():
    """In the orthonormal basis (A_HAT, E_HAT, uh_1, vh_1), H|Fix(Sigma) = diag(h_A, h_E) (+) K for a generic pair
    potential (B2.1), and the 2x2 block is the B0 block K. So in (s, wA, wE, wf) coordinates hAE = 0, there is no
    s-wA, s-wE, wf-wA, wf-wE coupling, and (kss, ksf, kff) = (n^T K n, n^T K f, f^T K f)."""
    from . import b2_quartic as q4
    from . import t2g
    H = q4.hessian_on_fix()
    K = t2g.block_K()[0]
    off = [H[i, j] for i in range(4) for j in range(4) if i != j and not (i >= 2 and j >= 2)]
    return {"A_E_rows_decoupled": all(sp.expand(x) == 0 for x in off),
            "T2g_block_equals_B0_K": sp.expand(H[2:, 2:] - K) == sp.zeros(2, 2),
            "h_A_h_E_are_the_B21_forms": True}


def schur_identities():
    """For orthonormal (n, f) in R^2 and symmetric K: n^T K n - (n^T K f)^2/(f^T K f) = det K/(f^T K f); if
    K(0) n = 0 then lambda(0) = 0 and lambda'(0) = n^T K'(0) n (exact, generic K)."""
    t = sp.Symbol("t", real=True)
    k11, k12, k22, d11, d12, d22, e11, e12, e22 = sp.symbols("k11 k12 k22 d11 d12 d22 e11 e12 e22", real=True)
    n = sp.Matrix([sp.cos(t), sp.sin(t)])
    f = sp.Matrix([-sp.sin(t), sp.cos(t)])
    K = sp.Matrix([[k11, k12], [k12, k22]])
    lam = (n.T * K * n)[0] - (n.T * K * f)[0] ** 2 / (f.T * K * f)[0]
    ident = sp.simplify(lam - K.det() / (f.T * K * f)[0]) == 0
    kff = sp.Symbol("kff", positive=True)
    Kmu = kff * f * f.T + mu * sp.Matrix([[d11, d12], [d12, d22]]) + mu ** 2 * sp.Matrix([[e11, e12], [e12, e22]])
    lam_mu = (n.T * Kmu * n)[0] - (n.T * Kmu * f)[0] ** 2 / (f.T * Kmu * f)[0]
    d1 = sp.simplify(sp.diff(lam_mu, mu).subs(mu, 0) - (n.T * sp.Matrix([[d11, d12], [d12, d22]]) * n)[0])
    return {"schur_equals_detK_over_fKf": ident, "lambda_at_0_is_0": sp.simplify(lam_mu.subs(mu, 0)) == 0,
            "lambda_prime_at_0_is_tau": d1 == 0}


# ---- 3. dV_red/ds = s G(s^2, mu) ---------------------------------------------------------------------------------------
LAM, C4, A3 = sp.symbols("lambda c4 a3", real=True)
FACTOR = 6          # G_z(0, 0) = c4 / FACTOR


def reduced_G():
    """V_red = V0 + lambda s^2/2 + c4 s^4/24 + a3 s^6: dV_red/ds = s G(s^2) with G(z) = lambda + c4 z/6 + 6 a3 z^2."""
    V0 = sp.Symbol("V0")
    Vred = V0 + LAM * s ** 2 / 2 + C4 * s ** 4 / 24 + A3 * s ** 6
    G = sp.expand(sp.cancel(sp.diff(Vred, s) / s)).subs(s ** 2, z)
    G = sp.expand(G.subs(s, sp.sqrt(z)))
    return {"V_red": Vred, "G": G, "G_expected": LAM + C4 * z / FACTOR + 6 * A3 * z ** 2,
            "matches": sp.expand(G - (LAM + C4 * z / FACTOR + 6 * A3 * z ** 2)) == 0}


# ---- 4. the implicit function theorem -----------------------------------------------------------------------------
TAU = sp.Symbol("tau", real=True, nonzero=True)
C40 = sp.Symbol("c4", real=True, nonzero=True)
GCO = {n: sp.Symbol(n, real=True) for n in ("g20", "g11", "g02", "g30", "g21", "g12", "g03")}


def generic_G(tau=TAU, c4=C40):
    """A generic analytic G(z, mu) truncated at total degree 3, with G(0,0) = 0, G_mu(0,0) = tau, G_z(0,0) = c4/6."""
    g = GCO
    return (tau * mu + c4 * z / FACTOR + g["g20"] * mu ** 2 + g["g11"] * mu * z + g["g02"] * z ** 2
            + g["g30"] * mu ** 3 + g["g21"] * mu ** 2 * z + g["g12"] * mu * z ** 2 + g["g03"] * z ** 3)


def ift_branch(tau=TAU, c4=C40):
    """mu*(z) = m1 z + m2 z^2 with G(z, mu*(z)) = O(z^3), and its inverse Z(mu) = Z1 mu + Z2 mu^2 (exact)."""
    G = generic_G(tau, c4)
    m1, m2 = sp.symbols("m1 m2")
    e = sp.expand(G.subs(mu, m1 * z + m2 * z ** 2))
    s1 = sp.solve(e.coeff(z, 1), m1)[0]
    s2 = sp.solve(e.coeff(z, 2).subs(m1, s1), m2)[0]
    Z1, Z2 = sp.symbols("Z1 Z2")
    inv = sp.expand((s1 * z + s2 * z ** 2).subs(z, Z1 * mu + Z2 * mu ** 2))
    z1 = sp.solve(inv.coeff(mu, 1) - 1, Z1)[0]
    z2 = sp.solve(inv.coeff(mu, 2).subs(Z1, z1), Z2)[0]
    return {"m1": sp.simplify(s1), "m2": sp.simplify(s2), "Z1": sp.simplify(z1), "Z2": sp.simplify(z2),
            "G_mu": sp.diff(G, mu).subs({z: 0, mu: 0}), "G_z": sp.diff(G, z).subs({z: 0, mu: 0})}


def _signed(sign, name):
    if sign == "<0":
        return -sp.Symbol(name + "_abs", positive=True)
    if sign == ">0":
        return sp.Symbol(name + "_abs", positive=True)
    raise ValueError(f"sign must be '<0' or '>0', got {sign!r}")


def branch_side(tau_sign, c4_sign):
    """The side of mu that carries the nontrivial branch, derived from the sign of mu*'(0) = -c4/(6 tau):
    s^2 = mu*^{-1}(mu) > 0 requires sign(mu) = sign(mu*'(0))."""
    m1 = ift_branch(_signed(tau_sign, "tau"), _signed(c4_sign, "c4"))["m1"]
    if m1.is_positive:
        return "mu > 0"
    if m1.is_negative:
        return "mu < 0"
    raise ArithmeticError("sign of mu*'(0) undetermined")


def axial_curvature(tau=TAU, c4=C40):
    """d^2V_red/ds^2 = G(s^2, mu) + 2 s^2 G_z(s^2, mu). Leading terms (exact series): at the cube, G(0, mu) =
    tau mu + O(mu^2); on the branch, where G = 0, 2 z G_z with z = Z(mu): -2 tau mu + O(mu^2)."""
    G = generic_G(tau, c4)
    br = ift_branch(tau, c4)
    Zmu = br["Z1"] * mu + br["Z2"] * mu ** 2
    cube = sp.expand(G.subs(z, 0))
    on_branch = sp.expand((2 * z * sp.diff(G, z)).subs(z, Zmu))
    G_on_branch = sp.expand(G.subs(z, Zmu))
    return {"cube": sp.simplify(cube.coeff(mu, 1)) * mu, "branch": sp.simplify(on_branch.coeff(mu, 1)) * mu,
            "G_on_branch_order1": sp.simplify(G_on_branch.coeff(mu, 1)),
            "G_on_branch_order2": sp.simplify(G_on_branch.coeff(mu, 2))}


def classify(tau_sign, c4_sign):
    """Pitchfork type in the ENERGY-REDUCED AXIAL convention: 'supercritical' when the two nontrivial equilibria exist
    on the side where the cube's axial reduced curvature lambda(mu) is negative (they bifurcate into the side where
    the cube has lost axial minimality, and are themselves axial minima of V_red); 'subcritical' otherwise.
    Equivalently: the gradient flow s' = -dV_red/ds has the normal form s' = nu s - (c4/6) s^3 + ..., nu = -lambda,
    so the type is the sign of c4. Derived here from the signs, not looked up."""
    side = branch_side(tau_sign, c4_sign)
    tau = _signed(tau_sign, "tau")
    c4 = _signed(c4_sign, "c4")
    mu_rep = sp.Symbol("m", positive=True) * (1 if side == "mu > 0" else -1)
    cube_curv = (tau * mu_rep)
    branch_curv = axial_curvature(tau, c4)["branch"].subs(mu, mu_rep)
    if cube_curv.is_negative and branch_curv.is_positive:
        return "supercritical"
    if cube_curv.is_positive and branch_curv.is_negative:
        return "subcritical"
    raise ArithmeticError("classification undetermined")


# ---- 7. isotropy and exchange -------------------------------------------------------------------------------------
def isotropy_exact():
    """For every R in O_h: rank of (D(R) - I)[uh_1, vh_1] is 0 if R is in Sigma and 2 otherwise. Since the T2g
    isotypic projector commutes with every D(R), kills A_HAT and E_HAT and fixes uh_1, vh_1, a point
    y* + aA A_HAT + aE E_HAT + a uh_1 + b vh_1 with (a, b) != 0 has isotropy exactly Sigma."""
    from . import b2_symmetry as s2
    from .group import D24, oh_matrices
    from .t2g import UH, VH
    S = {tuple(R) for R in s2.axis_stabilizer()}
    M = sp.Matrix.hstack(UH[0], VH[0])
    ranks_in, ranks_out = set(), set()
    for R in oh_matrices():
        rk = ((D24(R) - sp.eye(24)) * M).applyfunc(sp.simplify).rank()
        (ranks_in if tuple(R) in S else ranks_out).add(int(rk))
    PT = s2.iso_projector("T2g")
    proj_ok = (sp.simplify(PT * s2.A_HAT) == sp.zeros(24, 1) and sp.simplify(PT * s2.E_HAT) == sp.zeros(24, 1)
               and sp.simplify(PT * UH[0] - UH[0]) == sp.zeros(24, 1)
               and sp.simplify(PT * VH[0] - VH[0]) == sp.zeros(24, 1))
    commute = all(sp.simplify(PT * D24(R) - D24(R) * PT) == sp.zeros(24, 24) for R in oh_matrices())
    diag = [R for R in oh_matrices() if R.is_diagonal()]
    sigma_diag = [R for R in diag if tuple(R) in S]
    return {"ranks_inside_Sigma": sorted(ranks_in), "ranks_outside_Sigma": sorted(ranks_out),
            "T2g_projector_kills_A_E_fixes_uh1_vh1": proj_ok, "T2g_projector_commutes": commute,
            "order_Sigma": len(S), "order_Sigma_cap_diagonal_Z2^3": len(sigma_diag), "order_Z2^3": len(diag)}


def exchange_exact():
    """Each R with D(R) e_1 = -e_1 acts on (A_HAT, E_HAT, uh_1, vh_1) as diag(1, 1, -1, -1) (B2.0), hence on
    (s, wA, wE, wf) as (-s, wA, wE, -wf): it maps the LS solution w(s, mu) to w(-s, mu) (uniqueness) and the branch
    point at +s* to the one at -s*."""
    from . import b2_symmetry as s2
    rev = s2.reversing_elements()
    ok = all(r["Fix_basis_vectors_are_eigenvectors"] and r["diag_action_on_Fix_basis"] ==
             {"A1g": 1, "Eg": 1, "T2g_u": -1, "T2g_v": -1} for r in rev)
    return {"n_reversing_elements": len(rev), "all_act_as_diag_1_1_-1_-1": ok}


# ---- 8. first-order geometry -----------------------------------------------------------------------------------------
def rhombus_exact():
    """First order in s, each cross-section x = const moves by (y, z) -> (y - eps z, z - eps y), eps = s n_u/2 (B2.0).
    The image of the square with vertices (+-1/2, +-1/2) has four equal sides, perpendicular diagonals along (1, 1) and
    (1, -1) scaled by 1 - eps and 1 + eps, and for eps != 0 a non-right angle: a rhombus that is not a square.
    Replacing eps by -eps exchanges the two diagonals."""
    eps = sp.Symbol("epsilon", real=True)
    L = sp.Matrix([[1, -eps], [-eps, 1]])
    P = [sp.Matrix(v) / 2 for v in ((1, 1), (-1, 1), (-1, -1), (1, -1))]
    Q = [L * v for v in P]
    sides = [sp.expand(((Q[(i + 1) % 4] - Q[i]).T * (Q[(i + 1) % 4] - Q[i]))[0]) for i in range(4)]
    d1, d2 = Q[0] - Q[2], Q[1] - Q[3]
    angle = sp.expand(((Q[1] - Q[0]).T * (Q[3] - Q[0]))[0])
    return {"equal_sides": all(sp.expand(x - sides[0]) == 0 for x in sides),
            "diagonals_perpendicular": sp.expand((d1.T * d2)[0]) == 0,
            "diag_(1,1)_length_factor": sp.factor(sp.sqrt(sp.expand((d1.T * d1)[0])) / sp.sqrt(2)),
            "diag_(1,-1)_length_factor": sp.factor(sp.sqrt(sp.expand((d2.T * d2)[0])) / sp.sqrt(2)),
            "adjacent_side_inner_product": sp.factor(angle)}


# ---- 9. statement, dependency graph, validator --------------------------------------------------------------------
STATUS_PROVED = "PROVED (computer-assisted; not independently audited)"
ALLOWED_PROOF_STATUSES = ("VERIFIED-EXACT", "CERTIFIED", "FROZEN INPUT", "STANDARD")
FORBIDDEN_PROOF_STATUSES = ("VERIFIED-NUMERIC", "CANDIDATE", "RECONNAISSANCE")

PROPOSITION = {
    "name": "Proposition B2",
    "scope": "fixed q in (0, q_c); mu = p - P_T(q); equilibria of V_p in y* + Fix(Sigma) near y*, |mu| small",
    "coordinate": "s = <x - y*, e_1>, e_1 = n_u uh_1 + n_v vh_1, unit n in ker K at mu = 0, n_u > 0",
    "inputs": {"tau_sign": "<0", "c4_sign": ">0"},
    "reduced_potential": "V0 + lam*s**2/2 + c4*s**4/24",
    "reduced_potential_remainder": "O(s^6, mu s^4, mu^2 s^2) with lam = tau mu + O(mu^2)",
    "even_in_s": True,
    "G": "lam + c4*z/6",
    "G_remainder": "O(z^2, mu z, mu^2)",
    "mu_star_slope": "-c4/(6*tau)",
    "amplitude_law": "-6*tau*mu/c4",
    "branch_side": "mu > 0",
    "branch_on_both_sides": False,
    "cube_exists_for_both_signs": True,
    "nontrivial_equilibria_on_branch_side": 2,
    "nontrivial_equilibria_on_other_side": 0,
    "pitchfork_symmetry": "Z2 generated by any element of N(Sigma) minus Sigma (8 elements); (s, wf) -> (-s, -wf)",
    "classification": "supercritical",
    "classification_convention": "energy-reduced axial",
    "axial_curvature_cube_branch_side": "tau*mu",
    "axial_curvature_branch": "-2*tau*mu",
    "isotropy_of_branch_points": "exactly Sigma (order 8, D2h)",
    "claims_cuboid": False,
    "claims_full_space_stability": False,
    "claims_centre_manifold_index": False,
    "status": STATUS_PROVED,
    "dependency_root": "P_B2",
}

_TESTS = "tests/test_B2_branch.py"
# The six allowed proof inputs of the B2.4 request, and the status each must carry. Every other node reachable from
# the proposition must be a derivation step of this phase (role "step", VERIFIED-EXACT). Facts that an allowed input
# already rests on, as recorded in NOTES.md, are listed in its "includes" field and are not separate inputs.
ALLOWED_INPUTS = {
    "B20_parity_fixed_space": "VERIFIED-EXACT",
    "B21_LS_c4_identity": "VERIFIED-EXACT",
    "LQ_lemma_Q": "CERTIFIED",
    "B18_tau": "FROZEN INPUT",
    "STD_lyapunov_schmidt": "STANDARD",
    "STD_implicit_function_theorem": "STANDARD",
}
DEPENDENCY_GRAPH = {
    "proposition": "Proposition B2",
    "root": "P_B2",
    "allowed_inputs": sorted(ALLOWED_INPUTS),
    "nodes": [
        {"id": "P_B2", "role": "proposition", "status": STATUS_PROVED,
         "statement": "Local D2h-axial pitchfork on the T2g curve (NOTES.md §12)", "source": "NOTES.md §12"},
        {"id": "L1_reduced_equation", "role": "step", "status": "VERIFIED-EXACT",
         "statement": "V_red = V0(mu) + lambda(mu) s^2/2 + c4(mu) s^4/24 + O(s^6), even in s; dV_red/ds = s G(s^2, mu), "
                      "G = lambda + c4 z/6 + O(z^2); lambda(0) = 0, lambda'(0) = tau, c4(0) = c4",
         "source": "NOTES.md §12.2; src/cube_bif/b2_branch.py (generic_ls_checks, model_structure, schur_identities, "
                   "reduced_G)", "tests": _TESTS},
        {"id": "L2_ift_branch", "role": "step", "status": "VERIFIED-EXACT",
         "statement": "unique local curve mu = mu*(z), mu*'(0) = -c4/(6 tau) > 0; s^2 = -6 tau mu/c4 + O(mu^2); "
                      "nontrivial equilibria only for mu > 0",
         "source": "NOTES.md §12.3; src/cube_bif/b2_branch.py (ift_branch, branch_side)", "tests": _TESTS},
        {"id": "L3_pitchfork", "role": "step", "status": "VERIFIED-EXACT",
         "statement": "cube for both signs; s = +-s*(mu) only for mu > 0; exchanged by N(Sigma) minus Sigma; "
                      "supercritical in the energy-reduced axial convention",
         "source": "NOTES.md §12.4; src/cube_bif/b2_branch.py (classify, exchange_exact)", "tests": _TESTS},
        {"id": "L4_axial_curvature", "role": "step", "status": "VERIFIED-EXACT",
         "statement": "d2V_red/ds2 = tau mu + O(mu^2) < 0 at the cube (mu > 0); -2 tau mu + O(mu^2) > 0 at +-s*",
         "source": "NOTES.md §12.5; src/cube_bif/b2_branch.py (axial_curvature)", "tests": _TESTS},
        {"id": "L5_geometry", "role": "step", "status": "VERIFIED-EXACT",
         "statement": "isotropy exactly Sigma; rhombic sections at first order; opposite tetrahedral translation "
                      "weight n_v; O(s^2) corrections in span{A_HAT, E_HAT}; f_1 component O(s^3)",
         "source": "NOTES.md §12.6; src/cube_bif/b2_branch.py (isotropy_exact, rhombus_exact, generic_ls_checks)",
         "tests": _TESTS},
        {"id": "X_generic_LS", "role": "step", "status": "VERIFIED-EXACT",
         "statement": "generic Z2-invariant LS expansion: odd coefficients 0, s^2 coefficient = Schur/2, "
                      "s^4 coefficient at mu = 0 = (D4V - 3 b^T H^-1 b)/24",
         "source": "NOTES.md §12.2 step 7; src/cube_bif/b2_branch.py (generic_ls_checks)", "tests": _TESTS},
        {"id": "B20_parity_fixed_space", "role": "input", "status": "VERIFIED-EXACT",
         "allowed_input": "exact B2.0 parity/fixed-space results",
         "statement": "B2.0: Sigma = Stab(e_1), order 8; Fix(Sigma) = span{A_HAT, E_HAT, uh_1, vh_1}; the 8 elements of "
                      "N(Sigma) minus Sigma act on Fix(Sigma) as diag(1, 1, -1, -1)",
         "includes": ["Fix(Sigma) contains no rigid motion",
                      "first-order displacement of s e_1: vertex s moves by -(s n_u/4)(0, s3, s2) "
                      "- (s n_v sqrt2/4)(s1 s2 s3)(1, 0, 0)",
                      "stated in the B0 bases uh_k, vh_k and with the B0 block K (exact definitions used by B2.0)"],
         "source": "NOTES.md §6.1", "tests": "tests/test_B2_symmetry.py, tests/test_B0_t2g.py"},
        {"id": "B21_LS_c4_identity", "role": "input", "status": "VERIFIED-EXACT",
         "allowed_input": "exact B2.1 LS coefficient identity",
         "statement": "B2.1: H|Fix(Sigma) = diag(h_A, h_E) (+) K; c4 = D4V[e_1^4] - 3<b, H_perp^-1 b> = "
                      "Q - 3 b_A^2/h_A - 3 b_E^2/h_E with <b, f_1> = 0; c4 = q W_q (p - q) c4_hat",
         "includes": ["the identity's recorded hypotheses: h_A > 0, h_E > 0 (Paper 2 Lemma S, FROZEN INPUT) and "
                      "tr K > 0 (Paper 2 Lemma T1, FROZEN INPUT), as stated in NOTES.md §6.2"],
         "source": "NOTES.md §6.1-6.2", "tests": "tests/test_B2_quartic.py, tests/test_B2_symmetry.py"},
        {"id": "LQ_lemma_Q", "role": "input", "status": "CERTIFIED",
         "allowed_input": "certified Lemma Q from B2.3",
         "statement": "B2.3 Lemma Q: c4_hat > 0 on the closed T2g curve, hence c4(q) > 0 for 0 < q < q_c "
                      "(certified; not independently audited)",
         "includes": ["the corollary c4(q) = q W_q (P_T(q) - q) c4_hat(q) > 0 of NOTES.md §9.1, which uses Paper 2 "
                      "Lemmas T2, T3 (FROZEN INPUT) as recorded there"],
         "source": "NOTES.md §9; data/B2_c4hat_certificate.json (semantic f7bc244e...)",
         "tests": "tests/test_B2_certificate.py"},
        {"id": "B18_tau", "role": "input", "status": "FROZEN INPUT",
         "allowed_input": "audited B1/Paper-2 transversality result tau < 0",
         "statement": "tau = n^T dK/dp n < 0 for 0 < q < q_c on the T2g curve p = P_T(q), where ker K = span{n} "
                      "(B1.8; independently audited with B1)",
         "includes": ["Paper 2 Lemmas T1 (tr K > 0) and T3 (unique curve point P_T(q) > q, D_p < 0) and the exact "
                      "adj identity, as recorded in NOTES.md §5.8"],
         "source": "NOTES.md §5.8, §5.11", "tests": "tests/test_B1_d3d.py, tests/test_B1_exact.py"},
        {"id": "STD_lyapunov_schmidt", "role": "input", "status": "STANDARD",
         "allowed_input": "standard Lyapunov-Schmidt reduction",
         "statement": "Lyapunov-Schmidt reduction of an equivariant gradient problem with a one-dimensional kernel "
                      "(Golubitsky & Schaeffer, Vol. I, Ch. I §3 and Ch. VII; Golubitsky, Stewart & Schaeffer, "
                      "Vol. II, Ch. XIII)",
         "includes": ["its hypotheses, checked in NOTES.md §12.2 steps 1-2: V_p is real-analytic in (x, p) near "
                      "(y*, P_T(q)) (pair distances near 1, sqrt2, sqrt3; r^-p = exp(-p log r)); the O_h action is "
                      "finite and orthogonal, so grad V is in Fix(Sigma) on y* + Fix(Sigma) (symmetric criticality)"],
         "source": "textbook"},
        {"id": "STD_implicit_function_theorem", "role": "input", "status": "STANDARD",
         "allowed_input": "implicit function theorem",
         "statement": "real-analytic implicit function theorem (Krantz & Parks, The Implicit Function Theorem, "
                      "Thm 2.3.5)", "source": "textbook"},
    ],
    "edges": [
        ["P_B2", "L1_reduced_equation"], ["P_B2", "L2_ift_branch"], ["P_B2", "L3_pitchfork"],
        ["P_B2", "L4_axial_curvature"], ["P_B2", "L5_geometry"],
        ["L1_reduced_equation", "X_generic_LS"],
        ["L1_reduced_equation", "B20_parity_fixed_space"],
        ["L1_reduced_equation", "B21_LS_c4_identity"],
        ["L1_reduced_equation", "B18_tau"],
        ["L1_reduced_equation", "STD_lyapunov_schmidt"],
        ["L1_reduced_equation", "STD_implicit_function_theorem"],
        ["L2_ift_branch", "L1_reduced_equation"],
        ["L2_ift_branch", "LQ_lemma_Q"],
        ["L2_ift_branch", "B18_tau"],
        ["L2_ift_branch", "STD_implicit_function_theorem"],
        ["L3_pitchfork", "L2_ift_branch"],
        ["L3_pitchfork", "B20_parity_fixed_space"],
        ["L4_axial_curvature", "L2_ift_branch"],
        ["L5_geometry", "L2_ift_branch"],
        ["L5_geometry", "B20_parity_fixed_space"],
        ["L5_geometry", "X_generic_LS"],
        ["X_generic_LS", "STD_lyapunov_schmidt"],
    ],
    "corroboration_only": [
        {"id": "N_B22_scan", "status": "VERIFIED-NUMERIC",
         "statement": "B2.2 401-point scan of c4_hat (reconnaissance)", "source": "NOTES.md §7"},
        {"id": "N_B24_branch_points", "status": "VERIFIED-NUMERIC",
         "statement": "B2.4 located branch points, reduced scans, amplitude law (this phase)",
         "source": "data/B2_4_branch.json"},
    ],
}

def _reachable(graph, root):
    adj = {}
    for a, b in graph["edges"]:
        adj.setdefault(a, []).append(b)
    seen, stack = set(), [root]
    while stack:
        v = stack.pop()
        if v in seen:
            continue
        seen.add(v)
        stack.extend(adj.get(v, []))
    return seen


def _acyclic(graph):
    adj = {}
    for a, b in graph["edges"]:
        adj.setdefault(a, []).append(b)
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


REQUIRED_NODES = tuple(sorted(ALLOWED_INPUTS))


def validate_graph(graph=None):
    """Failures (empty = valid): edges reference known nodes; acyclic; every node reachable from the root has an
    allowed proof status (VERIFIED-EXACT, CERTIFIED, FROZEN INPUT, STANDARD) or is the root; no corroboration node
    and no VERIFIED-NUMERIC/CANDIDATE/RECONNAISSANCE node is reachable; every reachable node is either a
    VERIFIED-EXACT derivation step of this phase or one of the six allowed inputs (ALLOWED_INPUTS) with its expected
    status; all six allowed inputs are reachable."""
    graph = DEPENDENCY_GRAPH if graph is None else graph
    fails = []
    nodes = {n["id"]: n for n in graph["nodes"]}
    corr = {n["id"] for n in graph.get("corroboration_only", [])}
    for a, b in graph["edges"]:
        if a not in nodes and a not in corr:
            fails.append(f"edge from unknown node {a}")
        if b not in nodes and b not in corr:
            fails.append(f"edge to unknown node {b}")
    if not _acyclic(graph):
        fails.append("dependency graph has a cycle")
    reach = _reachable(graph, graph["root"])
    for v in sorted(reach):
        if v == graph["root"]:
            continue
        if v in corr:
            fails.append(f"corroboration-only node {v} is a proof dependency")
            continue
        st = nodes.get(v, {}).get("status")
        if st in FORBIDDEN_PROOF_STATUSES:
            fails.append(f"node {v} has forbidden proof status {st}")
        elif st not in ALLOWED_PROOF_STATUSES:
            fails.append(f"node {v} has unknown status {st}")
        role = nodes.get(v, {}).get("role")
        if role == "step":
            if st != "VERIFIED-EXACT":
                fails.append(f"derivation step {v} is not VERIFIED-EXACT")
        elif v not in ALLOWED_INPUTS:
            fails.append(f"node {v} is not one of the six allowed proof inputs {sorted(ALLOWED_INPUTS)}")
        elif st != ALLOWED_INPUTS[v]:
            fails.append(f"allowed input {v} has status {st}, expected {ALLOWED_INPUTS[v]}")
        stmt = nodes.get(v, {}).get("statement", "").lower()
        if "scan" in stmt or "numeric" in stmt:
            fails.append(f"node {v} describes a numerical scan")
    for req in REQUIRED_NODES:
        if req not in reach:
            fails.append(f"required dependency {req} not reachable")
    root = nodes.get(graph["root"], {})
    if root.get("status") != STATUS_PROVED:
        fails.append("root status is not the computer-assisted, not-audited proved status")
    return fails


def _parse(expr):
    loc = {"tau": TAU, "c4": C40, "mu": mu, "z": z, "s": s, "lam": LAM, "V0": sp.Symbol("V0")}
    return sp.sympify(expr, locals=loc)


def derived_statement():
    """Every checkable field of the proposition, re-derived from the exact layer with tau < 0 and c4 > 0."""
    br = ift_branch()
    curv = axial_curvature()
    Gd = reduced_G()
    ls = generic_ls_checks()
    return {
        "inputs": {"tau_sign": "<0", "c4_sign": ">0"},
        "reduced_potential": (sp.Symbol("V0") + LAM * s ** 2 / 2 + C4.subs(C4, C40) * s ** 4 / 24),
        "even_in_s": ls["odd_coefficients_vanish"],
        "G": (Gd["G_expected"] - 6 * A3 * z ** 2).subs(C4, C40),
        "mu_star_slope": br["m1"],
        "amplitude_law": br["Z1"] * mu,
        "branch_side": branch_side("<0", ">0"),
        "classification": classify("<0", ">0"),
        "axial_curvature_cube_branch_side": curv["cube"],
        "axial_curvature_branch": curv["branch"],
    }


def validate_statement(stmt=None, graph=None):
    """Failures (empty = valid) of a proposition statement against the exact derivation and the dependency graph."""
    stmt = PROPOSITION if stmt is None else stmt
    graph = DEPENDENCY_GRAPH if graph is None else graph
    d = derived_statement()
    fails = []
    if stmt.get("inputs") != d["inputs"]:
        fails.append(f"input signs {stmt.get('inputs')} differ from the established tau < 0, c4 > 0")
    for key in ("reduced_potential", "G", "mu_star_slope", "amplitude_law", "axial_curvature_cube_branch_side",
                "axial_curvature_branch"):
        try:
            diff = sp.simplify(_parse(stmt[key]) - d[key])
        except (KeyError, sp.SympifyError, TypeError) as exc:
            fails.append(f"{key}: unparsable or missing ({exc})")
            continue
        if diff != 0:
            fails.append(f"{key}: {stmt[key]} differs from the derivation {d[key]}")
    if stmt.get("even_in_s") is not True or not d["even_in_s"]:
        fails.append("evenness of V_red in s is required (B2.0 parity) and derived")
    if stmt.get("branch_side") != d["branch_side"]:
        fails.append(f"branch side {stmt.get('branch_side')} differs from the derived {d['branch_side']}")
    if stmt.get("branch_on_both_sides") is not False or stmt.get("nontrivial_equilibria_on_other_side") != 0:
        fails.append("the nontrivial branch exists on one side only")
    if stmt.get("nontrivial_equilibria_on_branch_side") != 2:
        fails.append("exactly two nontrivial equilibria +-s* on the branch side")
    if stmt.get("cube_exists_for_both_signs") is not True:
        fails.append("the cube is an equilibrium for both signs of mu")
    if stmt.get("classification") != d["classification"]:
        fails.append(f"classification {stmt.get('classification')} differs from the derived {d['classification']}")
    if stmt.get("classification_convention") != "energy-reduced axial":
        fails.append("the classification must state the energy-reduced axial convention")
    for flag in ("claims_full_space_stability", "claims_centre_manifold_index", "claims_cuboid"):
        if stmt.get(flag) is not False:
            fails.append(f"{flag} must be False: the curvature result is one-dimensional and axial only")
    if stmt.get("status") != STATUS_PROVED:
        fails.append(f"status {stmt.get('status')!r} is not {STATUS_PROVED!r}")
    if stmt.get("dependency_root") != graph.get("root"):
        fails.append("statement and graph roots differ")
    fails += validate_graph(graph)
    return fails


# ======================================================================================================================
# NUMERIC LAYER (corroboration only; not a proof dependency)
# ======================================================================================================================
def _fix_basis_numeric(n_u, n_v):
    """[A_HAT, E_HAT, e_1, f_1] as mpmath 24-vectors, from the integer fields."""
    from . import b2_symmetry as s2
    from .modes import E_BR, U_T2G, W_T2G
    r2 = mp.sqrt(2)
    A = [mp.mpf(int(c)) / mp.sqrt(24) for c in E_BR]
    E = [mp.mpf(int(c)) / mp.sqrt(48) for c in s2.E_TET_X]
    uh = [-mp.mpf(int(c)) / 4 for c in W_T2G[0]]
    vh = [-r2 * mp.mpf(int(c)) / 4 for c in U_T2G[0]]
    e1 = [n_u * a + n_v * b for a, b in zip(uh, vh)]
    f1 = [-n_v * a + n_u * b for a, b in zip(uh, vh)]
    return [A, E, e1, f1]


def curve_data(qq):
    """P_T(q), unit n (chart gauge n_u > 0), tau (unit n) and c4 (route 1 of B2.1) at mu = 0."""
    from . import b1_cubic as b1
    from . import b2_quartic as q4
    c = b1.carrier(qq)
    r = q4.route1(qq, c["delta"])
    nrm = mp.sqrt(1 + c["rho"] ** 2)
    tau = c["q"] * b1.W_num(c["q"]) * c["tau_hat"] / nrm ** 2
    return {"q": c["q"], "p0": c["p"], "rho": c["rho"], "n_u": 1 / nrm, "n_v": c["rho"] / nrm, "tau": tau,
            "c4": r["c4"]}


class FixProblem:
    """V_p restricted to y* + Fix(Sigma) in the coordinates (wA, wE, s, wf), through the 24-D pair energy."""

    def __init__(self, cd, pp):
        from .numeric import PairEnergy, y_star
        self.cd = cd
        self.V = PairEnergy(pp, cd["q"])
        self.y0 = y_star()
        self.B = _fix_basis_numeric(cd["n_u"], cd["n_v"])

    def x(self, c):
        return [self.y0[i] + mp.fsum(c[a] * self.B[a][i] for a in range(4)) for i in range(24)]

    def grad(self, c):
        g = self.V.gradient(self.x(c))
        return [mp.fsum(g[i] * self.B[a][i] for i in range(24)) for a in range(4)], g

    def hess(self, c):
        H = self.V.hessian(self.x(c))
        J = mp.matrix(4, 4)
        for a in range(4):
            Ha = [mp.fsum(H[i, j] * self.B[a][j] for j in range(24)) for i in range(24)]
            for b in range(4):
                J[b, a] = mp.fsum(self.B[b][i] * Ha[i] for i in range(24))
        return J

    def newton(self, c0, free=(0, 1, 2, 3), iters=60):
        c = list(c0)
        tol = mp.mpf(10) ** (-(mp.mp.dps - 8))
        for _ in range(iters):
            g, _ = self.grad(c)
            J = self.hess(c)
            idx = list(free)
            Jr = mp.matrix(len(idx), len(idx))
            for i, a in enumerate(idx):
                for j, b in enumerate(idx):
                    Jr[i, j] = J[a, b]
            step = mp.lu_solve(Jr, mp.matrix([g[a] for a in idx]))
            for i, a in enumerate(idx):
                c[a] -= step[i]
            if mp.norm(step) < tol * (1 + mp.norm(mp.matrix(c))):
                break
        return c

    def axial_curvature(self, c):
        """Schur complement of the 4x4 Fix Hessian onto the s direction: d2V_red/ds2 at a critical point."""
        J = self.hess(c)
        W = [0, 1, 3]
        JWW = mp.matrix(3, 3)
        for i, a in enumerate(W):
            for j, b in enumerate(W):
                JWW[i, j] = J[a, b]
        JWs = mp.matrix([J[a, 2] for a in W])
        return J[2, 2] - (JWs.T * mp.lu_solve(JWW, JWs))[0]


def branch_point(qq, rel_mu, sign=1, dps=60, cd=None):
    """Newton in the four Fix(Sigma) coordinates at p = P_T(q)(1 + rel_mu), started at s0 = sign sqrt|-6 tau mu/c4|
    (for mu < 0 this is the mirror amplitude, where no branch is predicted). Returns the converged amplitude, the full
    24-D gradient norm, the amplitude-law error and the axial curvature."""
    with mp.workdps(dps):
        cd = curve_data(qq) if cd is None else cd
        pp = cd["p0"] * (1 + mp.mpf(rel_mu))
        m = pp - cd["p0"]
        pred = -6 * cd["tau"] * m / cd["c4"]
        s0 = sign * mp.sqrt(abs(pred))
        F = FixProblem(cd, pp)
        c = F.newton([0, 0, s0, 0])
        _, g24 = F.grad(c)
        gn = mp.sqrt(mp.fsum(x * x for x in g24))
        out = {"q": cd["q"], "p": pp, "mu": m, "s_start": s0, "s_found": c[2], "wA": c[0], "wE": c[1], "wf": c[3],
               "s2_predicted": pred, "full_gradient_norm": gn, "x": F.x(c)}
        if pred > 0:
            out["amplitude_law_error"] = c[2] ** 2 / pred - 1
        out["axial_curvature"] = F.axial_curvature(c)
        out["axial_curvature_cube"] = F.axial_curvature([0, 0, 0, 0])
        out["tau_mu"] = cd["tau"] * m
        return out


def reduced_scan(qq, rel_mu, npts=24, factor=3, dps=50, cd=None):
    """g(s) = dV_red/ds = <grad V(x(s)), e_1> with x(s) = y* + s e_1 + w(s), w from Newton in (wA, wE, wf) at fixed s,
    on s_k = k S/npts, k = 1..npts, S = factor sqrt|6 tau mu/c4|. Returns the values of g(s)/s and the number of sign
    changes on (0, S] (the reduced potential is even, so s < 0 mirrors s > 0)."""
    with mp.workdps(dps):
        cd = curve_data(qq) if cd is None else cd
        pp = cd["p0"] * (1 + mp.mpf(rel_mu))
        m = pp - cd["p0"]
        S = factor * mp.sqrt(abs(6 * cd["tau"] * m / cd["c4"]))
        F = FixProblem(cd, pp)
        c = [mp.mpf(0)] * 4
        vals = []
        for k in range(1, npts + 1):
            c[2] = S * k / npts
            c = F.newton(c, free=(0, 1, 3))
            g, _ = F.grad(c)
            vals.append((c[2], g[2] / c[2]))
        signs = [1 if v > 0 else -1 for _, v in vals]
        changes = sum(1 for a, b in zip(signs, signs[1:]) if a != b)
        return {"q": cd["q"], "mu": m, "S": S, "values": vals, "sign_changes": changes,
                "g_over_s_at_smallest_s": vals[0][1], "lambda_leading": cd["tau"] * m}


def reversing_image_numeric(xv):
    """D(R) x for one R in N(Sigma) minus Sigma (the first returned by B2.0), numerically."""
    from . import b2_symmetry as s2
    from .group import D24
    R = sp.ImmutableMatrix(3, 3, s2.reversing_elements()[0]["R"])
    D = D24(R)
    return [mp.fsum(int(D[i, j]) * xv[j] for j in range(24) if D[i, j] != 0) for i in range(24)]
