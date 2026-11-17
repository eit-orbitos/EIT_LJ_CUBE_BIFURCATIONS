"""Phase A2: Theorem A.

These tests check four things:
- the machine-readable dependency graph (closed, acyclic, every named test exists, no numerical check is a
  dependency);
- the exact algebra of the reduced equation that fixes the branch side;
- one hypothesis check (pair distances);
- numerical corroboration. The numerical checks are labelled as such and are not used in the proof.
"""
import ast
import json
import pathlib

import mpmath as mp
import pytest
import sympy as sp

from cube_bif import a2u, branch, theorem_a
from cube_bif.modes import Y_STAR

mp.mp.dps = 40
ROOT = pathlib.Path(__file__).resolve().parents[1]
G = theorem_a.GRAPH


def _test_functions():
    out = {}
    for f in (ROOT / "tests").glob("test_*.py"):
        tree = ast.parse(f.read_text(encoding="utf-8"))
        out[f.name] = {n.name for n in tree.body if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")}
    return out


# ---- the dependency graph ----------------------------------------------------------------------------------------
def test_every_node_is_a_leaf_with_an_allowed_status_or_a_composite():
    for name, node in G.items():
        if name == "Theorem A":
            assert node["status"] == theorem_a.THEOREM_STATUS
            continue
        if "status" in node:
            assert node["status"] in theorem_a.LEAF_STATUSES, name
        else:
            assert node.get("uses"), f"composite node {name} uses nothing"


def test_graph_is_closed_and_acyclic_and_everything_is_used():
    for name, node in G.items():
        for u in node.get("uses", []):
            assert u in G, f"{name} uses undefined node {u}"
    state = {}

    def visit(n):
        if state.get(n) == 1:
            raise AssertionError(f"cycle through {n}")
        if state.get(n) == 2:
            return
        state[n] = 1
        for u in G[n].get("uses", []):
            visit(u)
        state[n] = 2

    visit("Theorem A")
    assert theorem_a.closure() == set(G), set(G) - theorem_a.closure()


def test_hypotheses_H1_to_H4_are_dependencies_of_theorem_A():
    uses = G["Theorem A"]["uses"]
    for h, word in (("H1", "Z2 evenness"), ("H2", "ker Hess"), ("H3", "transversality"), ("H4", "c4(q) > 0")):
        assert h in uses and word in G[h]["claim"], h
    assert {"Lemma M", "H4.P_A bound", "Lemma A"} <= theorem_a.closure("H4")
    assert "H2.Theorem 4'" in theorem_a.closure("H2") and "Lemma A" in theorem_a.closure("H3")


def test_every_named_test_exists():
    have = _test_functions()
    for name, node in G.items():
        for key in ("tests", "corroboration"):
            for t in node.get(key, []):
                f, fn = t.split("::")
                assert f in have and fn in have[f], f"{name}: {t} does not exist"


def test_verified_and_certified_leaves_name_their_own_tests():
    for name, node in theorem_a.leaves().items():
        if node["status"] in ("VERIFIED-EXACT", "CERTIFIED"):
            assert node.get("tests"), name
        if node["status"] == "STANDARD":
            assert node.get("ref"), name


def test_frozen_inputs_are_listed_in_the_paper2_reference():
    ref = (ROOT / "reference" / "PAPER2_INPUTS.md").read_text(encoding="utf-8")
    frozen = [n for n in G.values() if n.get("status") == "FROZEN INPUT"]
    assert {n["paper2"] for n in frozen} == {"Lemma A", "Theorem 4′", "Proposition A"}
    for n in frozen:
        assert n["paper2"] in ref, n["paper2"]


def test_no_numerical_check_is_a_dependency():
    """The branch side and every hypothesis come from exact or certified links. Numerical tests appear only as
    corroboration, never under 'tests' of a node in the dependency closure."""
    numerical = set()
    for node in G.values():
        numerical.update(node.get("corroboration", []))
    for name in theorem_a.closure():
        for t in G[name].get("tests", []):
            assert t not in numerical, (name, t)
            assert "numerical" not in t and "located_branch" not in t, (name, t)
    side = G["branch side"]
    assert side["status"] == "VERIFIED-EXACT" and set(side["uses"]) == {"H3", "H4", "IFT"}


def test_recorded_graph_matches_the_code():
    f = ROOT / "data" / "A2_theorem_A_dependencies.json"
    if not f.exists():
        pytest.skip("data/ not generated")
    assert json.loads(f.read_text(encoding="utf-8")) == json.loads(json.dumps(theorem_a.as_record()))


# ---- (H0) hypothesis check --------------------------------------------------------------------------------------
def test_cube_pair_distances_are_bounded_below():
    pts = [Y_STAR[3 * i:3 * i + 3, 0] for i in range(8)]
    d2 = sorted(sum((pts[i][c] - pts[j][c]) ** 2 for c in range(3)) for i in range(8) for j in range(i + 1, 8))
    assert d2 == [1] * 12 + [2] * 12 + [3] * 4


# ---- the reduced equation (exact algebra of the proof) ----------------------------------------------------------
def test_branch_side_from_the_reduced_equation():
    """G(s, mu) = lambda'(0) mu + (c4/6) s + second-order terms (generic coefficients).
    The implicit-function slope of the zero set at (0, 0) is mu*'(0) = -G_s/G_mu = -c4/(6 lambda'(0)). It is
    positive when lambda'(0) < 0 < c4, so s = a^2 > 0 forces mu > 0."""
    s, mu = sp.symbols("s mu", real=True)
    lam1, c4, gss, gsm, gmm = sp.symbols("lambda1 c4 G_ss G_smu G_mumu", real=True)
    Gs = lam1 * mu + c4 / 6 * s + gss * s ** 2 / 2 + gsm * s * mu + gmm * mu ** 2 / 2
    slope0 = (-sp.diff(Gs, s) / sp.diff(Gs, mu)).subs({s: 0, mu: 0})
    assert sp.simplify(slope0 + c4 / (6 * lam1)) == 0
    neg, pos = sp.symbols("l c", positive=True)
    assert sp.simplify(slope0.subs({lam1: -neg, c4: pos})).is_positive
    # the zero set to second order: mu*(s) = slope0 s + O(s^2) solves G = 0 to first order
    k2 = sp.symbols("k2")
    musol = slope0 * s + k2 * s ** 2
    ser = sp.expand(Gs.subs(mu, musol))
    assert sp.simplify(ser.coeff(s, 1)) == 0
    # amplitude: inverting mu = slope0 s gives s = -6 lambda'(0) mu / c4 = 6 |lambda'(0)| mu / c4
    assert sp.simplify(mu / slope0 - (-6 * lam1 * mu / c4)) == 0


def test_second_derivatives_of_the_reduced_potential():
    """V_red = lambda a^2/2 + c4 a^4/24 + d a^6/720 (+ O(a^8)). Then d_a V_red = a G(a^2), and
    d^2_a V_red = G + 2 a^2 G_s. At a = 0 this is lambda. On the branch (G = 0) it is 2 a^2 G_s, and at leading
    order (c4/3) a^2 = -2 lambda."""
    a, lam, c4, d = sp.symbols("a lambda c4 d", real=True)
    s = sp.symbols("s", real=True)
    Vred = lam * a ** 2 / 2 + c4 * a ** 4 / 24 + d * a ** 6 / 720
    Gf = lam + c4 * s / 6 + d * s ** 2 / 120
    assert sp.expand(sp.diff(Vred, a) - a * Gf.subs(s, a ** 2)) == 0
    V2 = sp.diff(Vred, a, 2)
    assert sp.expand(V2 - (Gf + 2 * s * sp.diff(Gf, s)).subs(s, a ** 2)) == 0
    assert V2.subs(a, 0) == lam
    # on the branch at leading order: s = -6 lambda / c4
    assert sp.simplify((2 * s * sp.diff(Gf, s)).subs(d, 0).subs(s, -6 * lam / c4) - (-2 * lam)) == 0


# ---- numerical corroboration (VERIFIED-NUMERIC; not used in the proof) -----------------------------------------
@pytest.fixture(scope="module")
def rs():
    return a2u.r_star()


def test_signs_of_the_reduced_equation_at_curve_points(rs):
    """NUMERICAL corroboration: lambda'(0) < 0, c4 > 0, slope -c4/(6 lambda'(0)) > 0, and lambda(mu) has the sign
    of -mu, at six curve points."""
    for qq in ("0.02", "0.3", "0.7", "1.0", "1.3", "1.47"):
        cp = a2u.curve_point(qq, rs)
        q, pa = cp["q"], cp["p"]
        lam1 = q * a2u.W_num(q) * mp.diff(a2u.h_A_num, pa)
        assert lam1 < 0 and cp["c4_full"] > 0 and -cp["c4_full"] / (6 * lam1) > 0
        for sgn in (1, -1):
            mu = sgn * mp.mpf("1e-8")
            lam = q * a2u.W_num(q) * (a2u.h_A_num(pa + mu) - a2u.h_A_num(q))
            assert lam * mu < 0


@pytest.mark.parametrize("qq", ["0.2", "0.8", "1.3"])
def test_amplitude_law_matches_the_located_branch(qq, rs):
    """NUMERICAL corroboration of the amplitude in Theorem A: a^2 = 6 q W_q |h_A'(P_A)| mu / c4 + O(mu^2).
    The branch is located in the T_d family as a zero of f'(u). Its e_A coordinate is
    alpha = -sqrt6 tanh(u/2) = a (1 + O(a^2))."""
    cp = a2u.curve_point(qq, rs)
    q, pa = cp["q"], cp["p"]
    pp = pa * (1 + mp.mpf("1e-7"))
    a2_pred = 6 * q * a2u.W_num(q) * abs(mp.diff(a2u.h_A_num, pa)) * (pp - pa) / cp["c4_full"]
    u = branch.branch_point(pp, q)["u_found"]
    alpha = -mp.sqrt(6) * mp.tanh(u / 2)
    assert abs(alpha ** 2 / a2_pred - 1) < mp.mpf("1e-5")


@pytest.mark.parametrize("qq", ["0.2", "1.3"])
def test_extremum_types_in_the_T_d_family(qq, rs):
    """NUMERICAL corroboration of the energy statement. Along the T_d family the scale-optimised energy is
    E(u) = -K exp(f(u)/(p - q)), with K > 0 (Proposition A). At a critical point, sign E'' = -sign f''.

    For p > P_A(q): f''(0) > 0 (the cube is a local maximum) and f''(u_branch) < 0 (the branch points are local
    minima). For p < P_A(q): f''(0) < 0."""
    q, pa = mp.mpf(qq), a2u.P_A(qq, rs)
    pp = pa * (1 + mp.mpf("1e-6"))
    assert branch.taylor_f(pp, q)[0] > 0
    ub = branch.branch_point(pp, q)["u_found"]
    assert mp.diff(lambda t: branch.f(t, pp, q), ub, 2) < 0
    pm = pa * (1 - mp.mpf("1e-6"))
    assert branch.taylor_f(pm, q)[0] < 0
