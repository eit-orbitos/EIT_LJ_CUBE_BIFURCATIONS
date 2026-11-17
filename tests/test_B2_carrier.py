"""Phase B2.2 — the normalised carrier c4_hat on the closed T2g curve (NOTES §7): exact endpoint data, both endpoint
formulations, the independent route with limit potentials, a coarse scan, falsification, records and claim boundary.
Everything numerical here is reconnaissance: no sign of c4_hat is proved or certified."""
import csv
import json
import pathlib

import mpmath as mp
import pytest
import sympy as sp

from cube_bif import b1_cubic as b1
from cube_bif import b2_carrier as bc
from cube_bif import b2_quartic as b2

ROOT = pathlib.Path(__file__).resolve().parents[1]
mp.mp.dps = 50
S2, S3, S6 = sp.sqrt(2), sp.sqrt(3), sp.sqrt(6)
C4_HAT_0 = "3.79933803786688581571022702876921125515828919"
C4_HAT_QC = "4.37703549061312193611302188494539202422124684"


@pytest.fixture(autouse=True)
def _working_precision():
    with mp.workdps(50):
        yield


@pytest.fixture(scope="module")
def ends():
    with mp.workdps(50):
        qc, p0 = bc.refine_qc(80), bc.refine_p0(80)
        return {"qc": qc, "p0": p0, "q0": bc.endpoint_q0(p0), "corner": bc.corner(qc)}


# ---- exact layer ---------------------------------------------------------------------------------------------------
def test_exact_values_at_q0():
    expect = {"Q_uuuu": sp.Rational(73, 36), "Q_uuuv": 8 * S2 / 63, "Q_uuvv": sp.Rational(68, 63),
              "Q_uvvv": -8 * S2 / 63, "Q_vvvv": sp.Rational(472, 63), "bA_uu": 16 * S6 / 63, "bA_uv": -8 * S3 / 63,
              "bA_vv": 20 * S6 / 63, "bE_uu": -25 * S3 / 126, "bE_uv": 2 * S6 / 63, "bE_vv": -64 * S3 / 63,
              "hA": sp.Integer(2), "hE": sp.Rational(1, 7)}
    g0 = bc.g_at_zero()
    assert set(g0) == set(expect)
    for k, v in expect.items():
        assert sp.simplify(g0[k] - v) == 0, k
    M0 = bc.M_at_zero()
    assert sp.simplify(M0 - sp.Matrix([[-16, 4 * S2], [4 * S2, -20]]) / 21) == sp.zeros(2)


def test_derivative_closed_forms_agree_with_numerical_differentiation():
    for rr in (mp.mpf("0.7"), mp.mpf("2.0")):
        gp = bc.g_prime_num(rr)
        for k in bc.NAMES:
            num = mp.diff(lambda t: b2.g4_num(t)[k], rr)
            assert abs(gp[k] - num) < mp.mpf("1e-40"), k
        Mp = bc.M_prime_num(rr)
        Mn = b1.M_prime(rr)
        assert mp.norm(Mp - Mn) < mp.mpf("1e-40")
    assert sp.simplify(bc.g_prime_closed()["hA"] - 2) == 0


def test_corner_expression_has_no_p_or_q_and_nonzero_denominators(ends):
    cs = bc.corner_symbolic()
    assert cs["free_symbols"] <= {bc.r, bc.Xr, bc.Yr}
    qc = ends["qc"]
    args = (qc, mp.power(2, -qc / 2), mp.power(3, -qc / 2))
    vals = {k: sp.lambdify((bc.r, bc.Xr, bc.Yr), v, "mpmath")(*args) for k, v in cs["denominators"].items()}
    assert vals["W"] > 1 and vals["M'22"] > mp.mpf("1.45") and vals["g_hE'"] > mp.mpf("1.99")
    assert vals["1+rho^2"] >= 1
    num = sp.lambdify((bc.r, bc.Xr, bc.Yr), cs["c4_hat"], "mpmath")(*args)
    assert abs(num - ends["corner"]["c4_hat"]) < mp.mpf("1e-40")


def test_limit_potential_at_q0_is_the_limit_of_phi_over_q():
    rs, p, q = sp.symbols("r p q", positive=True)
    W = lambda e: 1 + 2 ** (-e / 2) + 3 ** (-e / 2) / 3
    A = q * W(q) / (p * W(p))
    expr = (A * rs ** (-p) - rs ** (-q)) / q + 1 / q            # + 1/q: an additive constant only
    lim = sp.limit(expr, q, 0)
    assert sp.simplify(lim - (sp.Rational(7, 3) / (p * W(p)) * rs ** (-p) + sp.log(rs))) == 0


def test_limit_potential_at_the_corner_is_d_phi_dp_at_p_equal_q():
    rs, p, q = sp.symbols("r p q", positive=True)
    W = lambda e: 1 + 2 ** (-e / 2) + 3 ** (-e / 2) / 3
    phi = q * W(q) / (p * W(p)) * rs ** (-p) - rs ** (-q)
    assert sp.simplify(phi.subs(p, q)) == 0
    dphi = sp.diff(phi, p).subs(p, q)
    want = -(1 / q + sp.diff(W(q), q) / W(q) + sp.log(rs)) * rs ** (-q)
    assert sp.simplify(dphi - want) == 0


@pytest.mark.parametrize("kind", ["two_term", "q0", "corner"])
def test_potential_derivatives(kind):
    pot = {"two_term": lambda: bc.Potential("two_term", p="3.2", q="1.0"), "q0": lambda: bc.Potential("q0", p="4.8"),
           "corner": lambda: bc.Potential("corner", q="2.02")}[kind]()
    for x in (mp.mpf("0.9"), mp.mpf("1.4"), mp.mpf("1.8")):
        assert abs(mp.diff(pot.phi, x) - pot.dphi(x)) < mp.mpf("1e-40")
        assert abs(mp.diff(pot.phi, x, 2) - pot.d2phi(x)) < mp.mpf("1e-40")


# ---- endpoints ---------------------------------------------------------------------------------------------------------
def test_refined_endpoints_lie_in_the_frozen_enclosures(ends):
    assert mp.mpf(bc.QC_LO) <= ends["qc"] <= mp.mpf(bc.QC_HI)
    assert mp.mpf(bc.PT0_LO) <= ends["p0"] <= mp.mpf(bc.PT0_HI)
    assert mp.mpf(bc.PT0_AUDIT_LO) <= ends["p0"] <= mp.mpf(bc.PT0_AUDIT_HI)
    lead = mp.mpf("2.019938231700799988302883185498575874900736")     # Paper 2 NOTES §6 (truncated digits)
    assert 0 <= ends["qc"] - lead < mp.mpf("1e-42")


def test_endpoint_q0_formulation(ends):
    e0 = ends["q0"]
    assert abs(e0["c4_hat"] - mp.mpf(C4_HAT_0)) < mp.mpf("1e-40")
    assert abs(e0["Q"] + e0["A1g"] + e0["Eg"] - e0["c4_hat"]) < mp.mpf("1e-45")
    assert e0["A1g"] < 0 and e0["Eg"] < 0 and abs(e0["hA"] - 2) < mp.mpf("1e-45")
    assert e0["kernel_residual"] < mp.mpf("1e-40")
    r1 = b2.route1(0, dd=ends["p0"])
    assert abs(r1["c4_hat"] - e0["c4_hat"]) < mp.mpf("1e-40")
    assert abs(e0["rho"] - mp.mpf("0.0197163555530139")) < mp.mpf("1e-15")       # B1, NOTES §5.4


def test_corner_formulation(ends):
    ec = ends["corner"]
    assert abs(ec["c4_hat"] - mp.mpf(C4_HAT_QC)) < mp.mpf("1e-40")
    assert abs(ec["Q"] + ec["A1g"] + ec["Eg"] - ec["c4_hat"]) < mp.mpf("1e-45")
    assert ec["delta"] == 0 and ec["kernel_residual"] < mp.mpf("1e-40")
    assert abs(ec["rho"] - b1.corner_limit(ends["qc"])["rho"]) < mp.mpf("1e-35")


def test_approach_is_linear_at_q0_and_quadratic_at_the_corner(ends):
    e0, ec, qc = ends["q0"], ends["corner"], ends["qc"]
    s1 = [(bc.interior(mp.mpf(10) ** -j)["c4_hat"] - e0["c4_hat"]) / mp.mpf(10) ** -j for j in (4, 6)]
    assert abs(s1[1] - mp.mpf("0.7062843")) < mp.mpf("1e-6") and abs(s1[0] - s1[1]) < mp.mpf("1e-4")
    s2 = [(bc.interior(qc - mp.mpf(10) ** -j)["c4_hat"] - ec["c4_hat"]) / mp.mpf(10) ** (-2 * j) for j in (4, 6)]
    assert abs(s2[1] - mp.mpf("-0.0987491")) < mp.mpf("1e-6") and abs(s2[0] - s2[1]) < mp.mpf("1e-5")


# ---- independent route ------------------------------------------------------------------------------------------------
def test_independent_route_at_an_interior_point():
    row = bc.interior("1.0")
    ind = bc.independent("two_term", row["p"], q=row["q"])
    assert ind["n_small"] == 9 and ind["b_on_small"] < mp.mpf("1e-40")
    assert abs(ind["curve_parameter"] - row["p"]) < mp.mpf("1e-40")
    assert abs(ind["c4_hat"] / row["c4_hat"] - 1) < mp.mpf("1e-40")


@pytest.mark.parametrize("kind", ["q0", "corner"])
def test_independent_route_at_the_endpoints(kind, ends):
    ref = ends["p0"] if kind == "q0" else ends["qc"]
    want = ends["q0"] if kind == "q0" else ends["corner"]
    ind = bc.independent(kind, ref * (1 + mp.mpf("1e-3")))
    assert abs(ind["curve_parameter"] - ref) < mp.mpf("1e-45")                  # its own p0 (resp. q_c)
    assert ind["equilibrium_gradient"] < mp.mpf("1e-40")                        # the cube is an equilibrium
    assert ind["n_small"] == 9 and ind["b_on_small"] < mp.mpf("1e-40")
    assert abs(ind["c4_hat"] / want["c4_hat"] - 1) < mp.mpf("1e-40")


# ---- coarse scan and falsification (reconnaissance) -------------------------------------------------------------------
@pytest.fixture(scope="module")
def coarse(ends):
    with mp.workdps(50):
        return bc.scan(40, qc=ends["qc"], p0=ends["p0"])


def test_coarse_scan(coarse):
    sm = bc.scan_summary(coarse)
    assert coarse[0]["formulation"] == "endpoint q = 0" and coarse[-1]["formulation"] == "corner (derivatives)"
    assert sm["n_points"] == 41 and sm["all_positive"] and sm["sign_changes"] == 0
    assert sm["strictly_increasing_on_grid"] and sm["min"][2] == 0 and sm["max"][2] == 40
    assert sm["denominator_minima"]["hE"][0] > mp.mpf("1.99")
    assert sm["denominator_minima"]["Mh22"][0] > mp.mpf("1.45")
    assert sm["max_kernel_residual"] < mp.mpf("1e-40")


def test_falsification_statements_are_exposed(coarse, ends):
    indep = {}
    row = bc.interior("1.0")
    indep["1.0"] = (row, bc.independent("two_term", row["p"], q=row["q"])["c4_hat"])
    indep["q0"] = (coarse[0], bc.independent("q0", ends["p0"])["c4_hat"])
    indep["corner"] = (coarse[-1], bc.independent("corner", ends["qc"])["c4_hat"])
    rep = bc.falsification_report(coarse, indep)
    assert len(rep) == 7
    assert all(x["exposed"] for x in rep), [x["statement"] for x in rep if not x["exposed"]]


# ---- records and claim boundary -----------------------------------------------------------------------------------------
def test_recorded_B2_2_data():
    data = ROOT / "data"
    if not (data / "B2_carrier.json").exists():
        pytest.skip("data/ not generated")
    rec = json.loads((data / "B2_carrier.json").read_text(encoding="utf-8"))
    assert rec["all_checks_pass"] and all(rec["enclosure_checks"].values())
    assert rec["scan"]["n_points"] == 401 and rec["scan"]["sign_changes"] == 0 and rec["scan"]["all_positive"]
    assert rec["endpoint_q0"]["c4_hat"].startswith(C4_HAT_0[:30])
    assert rec["endpoint_corner"]["c4_hat"].startswith(C4_HAT_QC[:30])
    with open(data / "B2_scan.csv", newline="") as fh:
        rows = list(csv.reader(fh))
    assert len(rows) == 402 and rows[1][1] == "endpoint q = 0" and rows[-1][1] == "corner (derivatives)"
    fal = json.loads((data / "B2_falsification.json").read_text(encoding="utf-8"))
    assert fal["all_exposed"] and len(fal["statements"]) == 7
    neg = data / "B2_2_negative_controls.json"
    if neg.exists():
        n = json.loads(neg.read_text(encoding="utf-8"))
        assert n["all_detected"] and len(n["controls"]) >= 8


def test_notes_section_7_claim_boundary():
    notes = (ROOT / "NOTES.md").read_text(encoding="utf-8")
    sec = notes[notes.index("## 7. Phase B2.2"):notes.index("## 8. Contradictions")]
    heads = [l for l in sec.splitlines() if l.startswith("#")]
    assert heads[0].endswith("(VERIFIED-NUMERIC / RECONNAISSANCE)")
    assert not any(k in h for h in heads for k in ("CERTIFIED", "PROVED", "AUDITED"))
    for item in ("No sign of ĉ₄ is\nproved or certified", "### 7.7 Claim boundary", "B2_scan.csv", "FROZEN INPUT",
                 "**No sign of ĉ₄ is proved or certified.**"):
        assert item in sec, item
