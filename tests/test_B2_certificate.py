"""Phase B2.3: the Lemma Q certificate (c4_hat > 0 on the closed physical T2g curve), its generator (b2_cert.py) and
the independent checker (b2_check.py): the B1 pin, series lengths, enclosures, the stored and a fresh certificate,
consistent forgeries that must be rejected, and the recorded method controls."""
import copy
import hashlib
import json
import pathlib
from fractions import Fraction

import mpmath as mp
import pytest
import sympy as sp
from flint import arb, ctx, fmpq

from cube_bif import b2_cert as gc
from cube_bif import b2_check as ck
from cube_bif import b2_carrier as bc

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
CERT = DATA / "B2_c4hat_certificate.json"


def _need_data():
    if not CERT.exists():
        pytest.skip("data/ not generated")


@pytest.fixture(scope="module")
def derived():
    return ck.derive_functions()


@pytest.fixture(scope="module")
def model(derived):
    return ck.Model(derived)


@pytest.fixture(scope="module")
def stored():
    _need_data()
    return json.loads(CERT.read_text())


@pytest.fixture(scope="module")
def built():
    return gc.build_certificate(ROOT)


def _ref():
    d = json.loads((DATA / "B2_carrier.json").read_text())
    return d["endpoint_q0"]["c4_hat"], d["endpoint_corner"]["c4_hat"]


# ---- the B1 import ---------------------------------------------------------------------------------------------------------
def test_B1_certificate_is_pinned_and_loaded_only_with_the_pinned_hash(monkeypatch):
    pin = "616817fcc70e0fab7f106404e5e5332b17b9c4480bd440355f1ac5257a8518c6"
    assert gc.B1_SEMANTIC_PINNED == ck.B1_SEMANTIC_PINNED == pin
    b1 = gc.load_b1(ROOT)
    assert gc.semantic_hash(b1) == pin and len(b1["boxes"]) == 222
    monkeypatch.setattr(gc, "B1_SEMANTIC_PINNED", "0" * 64)
    with pytest.raises(RuntimeError, match="pinned"):
        gc.load_b1(ROOT)


# ---- generator internals: series length and enclosures ----------------------------------------------------------------------
def test_generator_series_have_the_requested_length_and_correct_high_coefficients():
    """Regression test for the python-flint series cap: coefficient 23 of the Taylor model at r = 1 is checked against
    mpmath, and ctx.cap is restored."""
    ctx.prec = gc.PREC
    cap = ctx.cap
    t = gc.taylor(arb(1), 24)
    assert ctx.cap == cap
    mp.mp.dps = 40
    for k in ("M11", "hE", "Q_uuvv", "bE_vv"):
        assert len(t[k]) == 24
        f = sp.lambdify(gc.r, gc.EXPR[k].subs({gc.Xr: 2 ** (-gc.r / 2), gc.Yr: 3 ** (-gc.r / 2)}), "mpmath")
        ref = mp.taylor(f, 1, 23)[23]
        val = mp.mpf(t[k][23].mid().str(30, radius=False))
        assert ref != 0 and abs(val - ref) <= mp.mpf("1e-10") * abs(ref), k


@pytest.mark.parametrize("q, d, regime", [("0.3", "4.1", "quotient"), ("1.2", "1.6", "quotient"),
                                          ("1.7", "0.6", "symmetric Taylor"), ("2.0", "0.05", "symmetric Taylor"),
                                          ("1.9", "0.95", "symmetric Taylor")])
def test_generator_divided_differences_contain_the_quotient(q, d, regime):
    """Thin points: the generator's enclosure must contain the 256-bit quotient (f(q + d) - f(q))/d."""
    ctx.prec = 256
    Q, D = arb(q), arb(d)
    fq, fp = gc.funcs(Q), gc.funcs(Q + D)
    ref = {k: (fp[k] - fq[k]) / D for k in gc.NAMES}
    ctx.prec = gc.PREC
    val = gc.divided(arb(q), arb(d), regime)
    for k in gc.NAMES:
        assert val[k].overlaps(ref[k]), (k, val[k], ref[k])
        assert val[k].rad() < 1e-15, k


# ---- checker internals ---------------------------------------------------------------------------------------------------------
@pytest.mark.parametrize("q, d", [("0.0", "4.796"), ("0.7", "2.6"), ("1.7", "0.6"), ("2.0", "0.0")])
def test_checker_point_values_contain_the_reference(model, q, d):
    """The checker's midpoint rule with remainder must contain the 256-bit quotient (or f'(q) at d = 0)."""
    ctx.prec = 256
    Q, D = arb(q), arb(d)
    f = {k: sp.lambdify(ck.R_, ck.stored_expr(gc.expression_strings()[k]).subs(
        {ck.X_: 2 ** (-ck.R_ / 2), ck.Y_: 3 ** (-ck.R_ / 2)}), "mpmath") for k in ck.ORDER}
    mp.mp.dps = 70
    for n in (32, 128):
        ctx.prec = ck.CHECK_PREC
        G = ck.dd_point(model, Q, D, n)
        for k in ck.ORDER:
            if d == "0.0":
                ref = mp.diff(f[k], mp.mpf(q))
            else:
                ref = (f[k](mp.mpf(q) + mp.mpf(d)) - f[k](mp.mpf(q))) / mp.mpf(d)
            assert G[k].overlaps(arb(mp.nstr(ref, 60), "1e-55")), (k, n, G[k], ref)


def _ref_funcs():
    out = {}
    for k in ck.ORDER:
        e = ck.stored_expr(gc.expression_strings()[k]).subs({ck.X_: 2 ** (-ck.R_ / 2), ck.Y_: 3 ** (-ck.R_ / 2)})
        out[k] = (sp.lambdify(ck.R_, e, "mpmath"), sp.lambdify(ck.R_, sp.diff(e, ck.R_), "mpmath"))
    return out


def _exact_dd(fs, q, d):
    """f_hat, d_q f_hat = (f'(p) - f'(q))/d and d_delta f_hat = (f'(p) - f_hat)/d at p = q + d (50 digits)."""
    mp.mp.dps = 50
    q, d = mp.mpf(q), mp.mpf(d)
    f, df = fs
    v = (f(q + d) - f(q)) / d
    return v, (df(q + d) - df(q)) / d, (df(q + d) - v) / d


@pytest.mark.parametrize("box", [("0", "1/100", "475/100", "481/100"), ("7/5", "141/100", "11/10", "112/100"),
                                 ("19/10", "19/10", "2/5", "2/5")])
def test_checker_box_ranges_contain_exact_values(model, box):
    """The centred box ranges of f_hat, d_q f_hat and d_delta f_hat contain the exact values at sample points of the
    box (the last box is a single point, where the midpoint sum alone would miss the value)."""
    fs = _ref_funcs()
    ql, qh, dl, dh = (fmpq(*[int(x) for x in (b.split("/") + ["1"])[:2]]) for b in box)
    ctx.prec = ck.CHECK_PREC
    val, dq, dd = ck.dd_box(model, ck._ball(ql, qh), ck._ball(dl, dh), 16)
    for qs in {ql, (ql + qh) / 2, qh}:
        for ds in {dl, (dl + dh) / 2, dh}:
            for k in ck.ORDER:
                v, a, b = _exact_dd(fs[k], mp.mpf(int(qs.p)) / int(qs.q), mp.mpf(int(ds.p)) / int(ds.q))
                assert val[k].overlaps(arb(mp.nstr(v, 45), "1e-40")), ("value", k, qs, ds)
                assert dq[k].overlaps(arb(mp.nstr(a, 45), "1e-40")), ("d_q", k, qs, ds)
                assert dd[k].overlaps(arb(mp.nstr(b, 45), "1e-40")), ("d_delta", k, qs, ds)


def test_checker_rejects_a_delta_ball_that_misses_the_curve(stored, model):
    """The Newton re-verification accepts the imported ball of box 30 and rejects the same ball shifted off the curve."""
    ctx.prec = ck.CHECK_PREC
    b = stored["boxes"][30]
    Q = ck._ball(ck._q(b["q_lo"]), ck._q(b["q_hi"]))
    lo, hi = ck._q(b["delta_lo"]), ck._q(b["delta_hi"])
    assert ck.curve_confirmed(model, Q, ck._ball(lo, hi))[0] is not None
    shift = 2 * (hi - lo)
    assert ck.curve_confirmed(model, Q, ck._ball(lo + shift, hi + shift))[0] is None


def test_checker_shares_no_code_with_the_generator():
    """b2_check imports nothing from the project and uses no Taylor series; it runs at a higher precision."""
    import ast
    tree = ast.parse((ROOT / "src" / "cube_bif" / "b2_check.py").read_text())
    mods, names = set(), set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            mods |= {a.name for a in node.names}
        elif isinstance(node, ast.ImportFrom):
            mods.add("." * node.level + (node.module or ""))
            names |= {a.name for a in node.names}
        elif isinstance(node, ast.Name):
            names.add(node.id)
    assert mods == {"hashlib", "itertools", "json", "pathlib", "sympy", "flint"}, mods
    assert "arb_series" not in names and "taylor" not in {n.lower() for n in names}
    assert ck.CHECK_PREC > gc.PREC


# ---- the certificate ---------------------------------------------------------------------------------------------------------
def test_stored_certificate_passes_the_independent_checker(stored, derived, model):
    h = (DATA / "B2_CERTIFICATE_SEMANTIC.sha256").read_text().split()[0]
    ok, rep = ck.check(stored, ROOT, stored_semantic_hash=h, derived=derived, model=model)
    assert ok, rep["failures"]
    assert rep["curve_reverified_b1_boxes"] == 222 and rep["carrier_confirmed"] == rep["boxes_checked"] == 222
    assert rep["centre_values_inside_stored_enclosures"] == 222


def test_fresh_build_is_accepted_by_the_independent_checker(built, derived, model):
    ok, rep = ck.check(built, ROOT, derived=derived, model=model, fail_fast=True)
    assert ok, rep["failures"]


def test_fresh_and_stored_semantic_hashes_agree(built, stored):
    assert gc.semantic_hash(built) == gc.semantic_hash(stored) == stored["provenance"]["semantic_sha256"]
    assert (DATA / "B2_CERTIFICATE_SEMANTIC.sha256").read_text().split()[0] == gc.semantic_hash(stored)


def test_certificate_content(stored):
    c = stored
    assert c["claim"] == ck.EXPECTED_CLAIM and c["corollary"] == ck.EXPECTED_COROLLARY
    assert c["imported_B1"]["semantic_sha256"] == ck.B1_SEMANTIC_PINNED and c["imported_B1"]["n_boxes"] == 222
    assert c["import_checks"] == ck.EXPECTED_IMPORT_CHECKS
    assert c["n_boxes"] == len(c["boxes"]) == 222
    assert c["boxes"][0]["q_lo"] == "0" and c["boxes"][-1]["q_hi"] == "101/50"
    assert all(Fraction(a["q_hi"]) == Fraction(b["q_lo"]) for a, b in zip(c["boxes"], c["boxes"][1:]))
    lbs = [Fraction(b["c4_hat_lower_bound"]) for b in c["boxes"]]
    assert min(lbs) == Fraction(c["min_lower_bound"]) > 3
    assert all(b["curve_reverified"] for b in c["boxes"])
    assert all(Fraction(b["hE_hat_lower_bound"]) > 1 and Fraction(b["Mh22_lower_bound"]) > 1 for b in c["boxes"])
    assert {b["regime"] for b in c["boxes"]} == {"quotient", "symmetric Taylor"}
    assert c["method"]["arb_precision_bits"] == 128
    for e in c["endpoints"].values():
        assert e["certified"] is True and Fraction(e["c4_hat_lower_bound"]) > 3
        assert e["raw_c4"].startswith("0 (exact")
    assert "monoton" not in json.dumps(c).lower()


def test_endpoint_enclosures_contain_the_B2_2_reference_values(stored):
    ref0, refc = _ref()
    ctx.prec = 256
    for key, ref in (("q=0", ref0), ("corner", refc)):
        lo, hi = stored["endpoints"][key]["c4_hat_enclosure"]
        assert Fraction(lo) < Fraction(ref) < Fraction(hi), key
        assert Fraction(hi) - Fraction(lo) < Fraction(1, 10 ** 28), key


def test_endpoints_use_the_direct_formulations(stored):
    b1 = json.loads((DATA / "B1_kappa_certificate.json").read_text())
    e0, ec = stored["endpoints"]["q=0"], stored["endpoints"]["corner"]
    assert e0["P_T(0)_ball_from_B1"] == b1["endpoints"]["q=0"]["P_T(0)_enclosure"]
    assert ec["q_c_enclosure_from_B1"] == b1["endpoints"]["corner"]["q_c_enclosure_paper2_lemma_T2"]
    assert e0["rule"] == ck.EXPECTED_FORMULAS["q0_rule"] and ec["rule"] == ck.EXPECTED_FORMULAS["corner_rule"]
    assert e0["exact_f0_matches_closed_forms_at_0"] is True


# ---- consistent forgeries: the checker must reject each ---------------------------------------------------------------------
def _forge(c):
    """Re-derive every summary field and both hashes, as a careful forger would."""
    for j, b in enumerate(c["boxes"]):
        b["index"] = j
    c["n_boxes"] = len(c["boxes"])
    lbs = [Fraction(b["c4_hat_lower_bound"]) for b in c["boxes"]]
    mn = min(lbs)
    k = lbs.index(mn)
    c["min_lower_bound"] = str(fmpq(mn.numerator, mn.denominator))
    c["min_lower_bound_decimal"] = mp.nstr(mp.mpf(mn.numerator) / mn.denominator, 12)
    c["min_lower_bound_box"] = {"index": k, "q_lo": c["boxes"][k]["q_lo"], "q_hi": c["boxes"][k]["q_hi"]}
    c["denominator_bounds"]["hE_hat_min_lower_bound"] = str(min(gc.parse_q(b["hE_hat_lower_bound"]) for b in c["boxes"]))
    c["denominator_bounds"]["Mh22_min_lower_bound"] = str(min(gc.parse_q(b["Mh22_lower_bound"]) for b in c["boxes"]))
    c["expression_sha256"] = hashlib.sha256(ck._canon({"expressions": c["expressions"],
                                                       "formulas": c["formulas"]}).encode()).hexdigest()
    c["provenance"]["semantic_sha256"] = ck.semantic_hash(c)
    return c


def _box(j, **kw):
    def f(c):
        c["boxes"][j].update(kw)
    return f


def _set(path, value):
    def f(c):
        d = c
        for k in path[:-1]:
            d = d[k]
        d[path[-1]] = value
    return f


TAMPERS = [
    ("gap in the q-coverage", _box(10, q_lo="21/200"), "gap or overlap"),
    ("overlap in the q-coverage", _box(10, q_hi="23/200"), "gap or overlap"),
    ("a box deleted", lambda c: c["boxes"].pop(57), "gap or overlap"),
    ("modified imported B1 delta-ball", _box(5, delta_hi="4837/1000"), "imported B1 curve box modified"),
    ("modified imported B1 box hash", _box(7, b1_box_sha256="0" * 64), "imported B1 curve box modified"),
    ("wrong B1 semantic hash", _set(["imported_B1", "semantic_sha256"], "1" * 64), "imported B1 semantic hash"),
    ("altered B1 corner metadata", _set(["imported_B1", "q_c_enclosure"], ["2.0199", "2.0200"]),
     "imported B1 metadata altered"),
    ("altered Q coefficient (formula)", _set(["formulas", "Qh(1,rho)"],
                                             "Qh_uuuu + 4*rho*Qh_uuuv + 4*rho**2*Qh_uuvv + 4*rho**3*Qh_uvvv + "
                                             "rho**4*Qh_vvvv"), "stored formulas differ"),
    ("altered Q coefficient (expression)", lambda c: c["expressions"].__setitem__(
        "Q_uuvv", "(" + c["expressions"]["Q_uuvv"] + ") + 1/1000"), "Q_uuvv differs from the independent"),
    ("deleted Eg correction", _set(["formulas", "carrier"], "c4_hat = (Qh(1,rho) - 3/2*bAh(1,rho)**2)/(1 + rho**2)**2"),
     "stored formulas differ"),
    ("factor 3 -> 2 in the Eg correction", _set(["formulas", "carrier"],
                                                "c4_hat = (Qh(1,rho) - 3/2*bAh(1,rho)**2 - 2*bEh(1,rho)**2/hEh)/"
                                                "(1 + rho**2)**2"), "stored formulas differ"),
    ("wrong kernel sign / chart", _set(["formulas", "chart"], "rho = Mh12/Mh22"), "stored formulas differ"),
    ("altered hE_hat", lambda c: c["expressions"].__setitem__("hE", c["expressions"]["hE"].replace("2*r + 2", "2*r + 3")),
     "hE differs from the independent"),
    ("inflated lower bound on the first box", _box(0, c4_hat_lower_bound="19/5",
                                                   c4_hat_enclosure=["19/5", "1054841671/268435456"]),
     "box 0: recorded bounds not confirmed"),
    ("inflated lower bound at the endpoint q = 0", _set(["endpoints", "q=0", "c4_hat_lower_bound"], "19/5"),
     "q=0: carrier bound not confirmed"),
    ("corner from values instead of derivatives", _set(["endpoints", "corner", "c4_hat_enclosure"],
                                                       ["7283610145951165/1000000000000000",
                                                        "7283610145951166/1000000000000000"]),
     "corner: stored enclosure does not overlap"),
    ("corner rule altered", _set(["formulas", "corner_rule"], "f_hat = f(q_c)"), "stored formulas differ"),
    ("raw c4 > 0 claimed at q = 0", _set(["endpoints", "q=0", "raw_c4"], "positive"),
     "q=0: raw c4 is not recorded as exactly zero"),
    ("raw c4 > 0 claimed at the corner", _set(["endpoints", "corner", "raw_c4"], "positive"),
     "corner: raw c4 is not recorded as exactly zero"),
    ("claim widened beyond the curve", _set(["claim", "q_interval"], ["0", "3"]), "claim differs"),
    ("corollary extended to the endpoints", _set(["corollary"], "c4 > 0 for 0 <= q <= q_c"), "corollary differs"),
    ("P_T(0) ball altered", _set(["endpoints", "q=0", "P_T(0)_ball_from_B1"], ["4", "5"]), "P_T(0) ball altered"),
    ("import check recorded as failed", _set(["import_checks", "q_coverage_gap_free_from_0_to_101/50"], False),
     "recorded import checks"),
]


@pytest.mark.parametrize("name, mutate, expect", TAMPERS, ids=[t[0] for t in TAMPERS])
def test_consistent_forgery_is_rejected(stored, derived, model, name, mutate, expect):
    c = copy.deepcopy(stored)
    mutate(c)
    _forge(c)
    ok, rep = ck.check(c, ROOT, derived=derived, model=model, fail_fast=True)
    assert not ok
    assert any(expect in f for f in rep["failures"]), rep["failures"]


def test_modified_semantic_hash_and_hash_file_are_rejected(stored, derived, model):
    c = copy.deepcopy(stored)
    c["provenance"]["semantic_sha256"] = "2" * 64
    ok, rep = ck.check(c, ROOT, derived=derived, model=model, fail_fast=True)
    assert not ok and "semantic hash in provenance" in rep["failures"][0]
    ok, rep = ck.check(stored, ROOT, stored_semantic_hash="3" * 64, derived=derived, model=model, fail_fast=True)
    assert not ok and "semantic hash file" in rep["failures"][0]
    c = copy.deepcopy(stored)
    c["boxes"][3]["c4_hat_lower_bound"] = "1/2"                 # content changed, hash not updated
    ok, rep = ck.check(c, ROOT, derived=derived, model=model, fail_fast=True)
    assert not ok and "semantic hash" in rep["failures"][0]


def test_malformed_certificate_is_rejected_not_crashed(stored, derived, model):
    c = copy.deepcopy(stored)
    del c["boxes"][4]["delta_lo"]
    _forge(c)
    ok, rep = ck.check(c, ROOT, derived=derived, model=model)
    assert not ok and rep["failures"]


# ---- recorded data -------------------------------------------------------------------------------------------------------------
def test_recorded_check_report_and_method_controls():
    _need_data()
    rep = json.loads((DATA / "B2_3_check_report.json").read_text())
    assert rep["ok"] and rep["failures"] == [] and rep["curve_reverified_b1_boxes"] == 222
    assert rep["precision_bits"] == 192 and rep["carrier_confirmed"] == 222
    ctl = json.loads((DATA / "B2_3_method_controls.json").read_text())
    assert ctl["all_as_required"] and len(ctl["controls"]) >= 15
    names = " | ".join(c["control"] for c in ctl["controls"])
    for item in ("false bound: c4_hat > 19/5", "false function: 21/5 - c4_hat", "raw (unnormalised) c4",
                 "wrong kernel sign", "Eg deleted", "factor 3 -> 2", "values f(q_c) instead of the derivatives",
                 "positive control"):
        assert item in names, item
    for c in ctl["controls"]:
        assert c["certified"] == (c["required"] == "certify"), c["control"]


def test_recorded_B1_series_cap_diagnostic():
    p = DATA / "B2_3_B1_series_cap_diagnostic.json"
    if not p.exists():
        pytest.skip("diagnostic not generated")
    d = json.loads(p.read_text())
    s = d["stored_certificate"]
    assert s["stored B1 certificate, B1 checker with ctx.cap = 32"]["ok"]
    assert s["stored B1 certificate, B1 checker with ctx.cap = 10"]["ok"]
    assert s["fresh B1 build with ctx.cap = 32"]["passes_B1_checker_with_cap_32"]
    assert d["series_truncation"]["exp series, prec=16, ctx.cap=10: coefficients returned"] == 10
    assert d["b1_near_divided_difference"]["functions whose default-cap enclosure excludes the quotient value"]
    assert d["b1_near_divided_difference"]["complete-series enclosures all contain the quotient values"]
    assert d["conclusion"].startswith("The defect is in the B1 code path, not in the stored B1 data")


def test_carrier_value_at_an_interior_point_agrees_with_B2_2(model):
    """The checker's homogeneous v-form at a thin interior curve point equals the B2.2 value (independent formulation)."""
    mp.mp.dps = 40
    row = bc.interior(mp.mpf("1.1"))
    ctx.prec = ck.CHECK_PREC
    G = ck.dd_point(model, arb("1.1"), arb(mp.nstr(row["delta"], 45)), 512)
    c = ck.carrier_v(G)
    assert c.rad() < 1e-6 and abs(mp.mpf(c.mid().str(30, radius=False)) - row["c4_hat"]) < mp.mpf("1e-6")
