"""Erratum E-B1 (V0.4-dev.4): verification records for the corrected B1 Taylor routines (NOTES.md §10).

1. Diagnostic point (q, delta) = (1.9, 0.9): the V0.4-dev.3 routines (reproduced verbatim, default ctx.cap = 10) and
   the corrected ones, against the plain quotient (f(q + delta) - f(q))/delta in mpmath at 60 digits.
2. Historical certificate replay: the corrected B1 checker on data/B1_kappa_certificate.json (semantic 616817fc...),
   which is read and never written.
3. Fresh corrected rebuild: a new B1 certificate from the corrected generator, stored separately as
   data/B1_ERRATUM_corrected_rebuild_certificate.json, checked by the corrected checker and compared with the
   historical one.
4. B2.3 cross-check without Taylor series: the B2.3 checker (src/cube_bif/b2_check.py) in a fresh interpreter in which
   importing cube_bif.b1_cert or cube_bif.b1_check raises, so that neither affected routine can run; plus a static
   check of its imports and names.

Writes data/B1_ERRATUM_report.json, data/B1_ERRATUM_corrected_rebuild_certificate.json and
data/B1_ERRATUM_CORRECTED_REBUILD_SEMANTIC.sha256. Never writes data/B1_kappa_certificate.json or
data/B1_CERTIFICATE_SEMANTIC.sha256 (unlike scripts/run_B1.py, which regenerates them and must not be re-run).
"""
import ast
import hashlib
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
DATA = ROOT / "data"
HISTORICAL_SEMANTIC = "616817fcc70e0fab7f106404e5e5332b17b9c4480bd440355f1ac5257a8518c6"
NAMES = ("M11", "M12", "M22", "uuu", "uuv", "uvv", "vvv")

B23_CHILD = r'''
import importlib.abc, json, pathlib, sys
ROOT = pathlib.Path(sys.argv[1])
BLOCKED = {"cube_bif.b1_cert", "cube_bif.b1_check"}
attempts = []
class Block(importlib.abc.MetaPathFinder):
    def find_spec(self, name, path=None, target=None):
        if name in BLOCKED:
            attempts.append(name)
            raise ImportError(f"{name} is blocked during the B2.3 cross-check")
        return None
sys.meta_path.insert(0, Block())
sys.path.insert(0, str(ROOT / "src"))
from cube_bif import b2_check as ck
cert = json.loads((ROOT / "data" / "B2_c4hat_certificate.json").read_text())
h = (ROOT / "data" / "B2_CERTIFICATE_SEMANTIC.sha256").read_text().split()[0]
ok, rep = ck.check(cert, ROOT, stored_semantic_hash=h)
print(json.dumps({"ok": ok, "boxes_checked": rep.get("boxes_checked"),
                  "curve_reverified_b1_boxes": rep.get("curve_reverified_b1_boxes"),
                  "carrier_confirmed": rep.get("carrier_confirmed"), "failures": rep.get("failures"),
                  "semantic_sha256": rep.get("semantic_sha256"), "import_attempts_blocked": attempts,
                  "b1_modules_imported": sorted(m for m in sys.modules if m in BLOCKED)}))
'''


def _mp_ref():
    import mpmath as mp
    import sympy as sp
    from cube_bif import b1_cert
    r = sp.Symbol("r")
    X, Y = 2 ** (-r / 2), 3 ** (-r / 2)
    loc = {"r": r, "X": X, "Y": Y, "W": 1 + X + Y / 3, "sqrt": sp.sqrt}
    f = {k: sp.lambdify(r, sp.sympify(b1_cert.EXPRESSIONS[k], locals=loc), "mpmath") for k in NAMES}
    with mp.workdps(60):
        q, d = mp.mpf(19) / 10, mp.mpf(9) / 10
        return {k: (f[k](q + d) - f[k](q)) / d for k in NAMES}


def diagnostic_point():
    import mpmath as mp
    from flint import arb, arb_series, ctx, fmpq
    from cube_bif import b1_cert, b1_check
    ref = _mp_ref()

    def old_gen(x, n):                                  # V0.4-dev.3 b1_cert._taylor, verbatim
        s = arb_series([x, 1], prec=n)
        out = {}
        for k, v in b1_cert._funcs(s).items():
            c = list(v.coeffs())
            out[k] = c + [arb(0)] * (n - len(c))
        return out

    def old_chk(self, x, n):                            # V0.4-dev.3 b1_check.Model.taylor, verbatim
        s = arb_series([x, 1], prec=n)
        out = {}
        for k, v in self.values(s).items():
            c = list(v.coeffs())
            out[k] = c + [arb(0)] * (n - len(c))
        return out

    model = b1_check.Model({k: b1_check._stored(b1_cert.EXPRESSIONS[k]) for k in NAMES})
    assert ctx.cap == 10, "the diagnostic is run under python-flint's default ctx.cap"
    res = {}
    new_taylor, new_model_taylor = b1_cert._taylor, b1_check.Model.taylor
    for label, gen, chk in (("old", old_gen, old_chk), ("corrected", new_taylor, new_model_taylor)):
        b1_cert._taylor, b1_check.Model.taylor = gen, chk
        try:
            ctx.prec = 128                          # the point is formed at the working precision of each routine
            g = b1_cert.divided(arb(fmpq(19, 10)), arb(fmpq(9, 10)), "near")[0]
            ctx.prec = b1_check.CHECK_PREC
            c = model.dd(arb(fmpq(19, 10)), arb(fmpq(9, 10)), "near")[0]
        finally:
            b1_cert._taylor, b1_check.Model.taylor = new_taylor, new_model_taylor
        res[label] = (g, c)
    ctx.prec = 128

    def inside(ball, k):
        with mp.workdps(70):
            return bool(ball.contains(arb(mp.nstr(ref[k], 55))))
    rows = {}
    for k in NAMES:
        rows[k] = {"mpmath_quotient_60_digits": mp.nstr(ref[k], 30),
                   "old_generator": res["old"][0][k].str(30), "old_generator_contains": inside(res["old"][0][k], k),
                   "corrected_generator": res["corrected"][0][k].str(30),
                   "corrected_generator_contains": inside(res["corrected"][0][k], k),
                   "old_checker": res["old"][1][k].str(30), "old_checker_contains": inside(res["old"][1][k], k),
                   "corrected_checker": res["corrected"][1][k].str(30),
                   "corrected_checker_contains": inside(res["corrected"][1][k], k)}
    with mp.workdps(70):
        err = {k: abs(mp.mpf(res["old"][0][k].mid().str(60, radius=False)) - ref[k]) for k in NAMES}
    worst = max(NAMES, key=lambda k: err[k])
    return {"point": {"q": "19/10", "delta": "9/10"}, "ctx.cap during the evaluation (default)": 10,
            "old_generator_excludes": [k for k in NAMES if not rows[k]["old_generator_contains"]],
            "corrected_generator_excludes": [k for k in NAMES if not rows[k]["corrected_generator_contains"]],
            "old_checker_excludes": [k for k in NAMES if not rows[k]["old_checker_contains"]],
            "corrected_checker_excludes": [k for k in NAMES if not rows[k]["corrected_checker_contains"]],
            "worst_old_generator": {"function": worst, "error_of_midpoint": mp.nstr(err[worst], 3),
                                    "old_radius": res["old"][0][worst].rad().str(3, radius=False)},
            "functions": rows}


def _endpoint_failures(fails):
    keys = ("endpoint", "corner", "det M'")
    return [f for f in fails if any(k in f for k in keys)]


def historical_replay(derived):
    from flint import ctx
    from cube_bif import b1_check
    raw = (DATA / "B1_kappa_certificate.json").read_bytes()
    cert = json.loads(raw)
    h = (DATA / "B1_CERTIFICATE_SEMANTIC.sha256").read_text().split()[0]
    cap0 = ctx.cap
    ok, rep = b1_check.check(cert, h, derived=derived)
    lbs = [b1_check._q(b["kappa_hat_lower_bound"]) for b in cert["boxes"]]
    return {"file": "data/B1_kappa_certificate.json", "file_sha256": hashlib.sha256(raw).hexdigest(),
            "semantic_sha256": b1_check.semantic_hash(cert), "hash_file": h,
            "pinned_semantic_sha256": HISTORICAL_SEMANTIC, "ok": ok, "boxes_checked": rep["boxes_checked"],
            "newton_confirmed": rep["newton_confirmed"], "carrier_confirmed": rep["carrier_confirmed"],
            "boxes_refined_by_checker": rep["boxes_refined_by_checker"],
            "max_checker_refinement_depth": rep["max_checker_refinement_depth"],
            "endpoints_accepted": ok and not _endpoint_failures(rep["failures"]),
            "corner_identification_and_sign_change_accepted": ok and not _endpoint_failures(rep["failures"]),
            "min_lower_bound": cert["min_lower_bound"], "min_lower_bound_recomputed": str(min(lbs)),
            "endpoint_lower_bounds": {k: cert["endpoints"][k]["kappa_hat_lower_bound"] for k in ("q=0", "corner")},
            "ctx.cap before / after": [cap0, ctx.cap], "precision_bits": rep["precision_bits"],
            "taylor_order": rep["taylor_order"], "failures": rep["failures"]}


def fresh_rebuild(derived):
    """Built under the conditions of scripts/run_B1.py, which produced the historical certificate: mpmath at 40 digits
    globally (the curve estimates that seed the Newton steps depend on it). Under these conditions the V0.4-dev.3 code
    reproduces the historical semantic hash exactly (data/B1_ERRATUM_pre_patch_reproduction.json), so every difference
    below comes from the corrected Taylor routines."""
    import mpmath as mp
    from flint import ctx
    from cube_bif import b1_cert, b1_check
    hist = json.loads((DATA / "B1_kappa_certificate.json").read_text())
    cap0 = ctx.cap
    with mp.workdps(40):
        cert = b1_cert.build_certificate(ROOT)
    sh = cert["provenance"]["semantic_sha256"]
    out_file = DATA / "B1_ERRATUM_corrected_rebuild_certificate.json"
    assert out_file.name != "B1_kappa_certificate.json"
    out_file.write_text(json.dumps(cert, indent=1))
    (DATA / "B1_ERRATUM_CORRECTED_REBUILD_SEMANTIC.sha256").write_text(
        f"{sh}  B1_ERRATUM_corrected_rebuild_certificate.json (semantic)\n")
    ok, rep = b1_check.check(cert, sh, derived=derived)
    same_keys = {k: cert[k] == hist[k] for k in ("claim", "statement", "expressions", "expression_sha256",
                                                  "frozen_inputs", "method")}
    part_same = [(b["q_lo"], b["q_hi"]) for b in cert["boxes"]] == [(b["q_lo"], b["q_hi"]) for b in hist["boxes"]]
    diff_boxes = [i for i, (a, b) in enumerate(zip(cert["boxes"], hist["boxes"])) if a != b]
    regimes = {}
    for i in diff_boxes:
        regimes[hist["boxes"][i]["regime"]] = regimes.get(hist["boxes"][i]["regime"], 0) + 1
    fields = {}
    for i in diff_boxes:
        for k in cert["boxes"][i]:
            if cert["boxes"][i][k] != hist["boxes"][i].get(k):
                fields[k] = fields.get(k, 0) + 1
    nested = 0
    lb_cmp = {"higher": 0, "equal": 0, "lower": 0}
    for a, b in zip(cert["boxes"], hist["boxes"]):
        alo, ahi, blo, bhi = (b1_check._q(a["delta_lo"]), b1_check._q(a["delta_hi"]), b1_check._q(b["delta_lo"]),
                              b1_check._q(b["delta_hi"]))
        nested += int(alo < bhi and blo < ahi)
        la, lb = b1_check._q(a["kappa_hat_lower_bound"]), b1_check._q(b["kappa_hat_lower_bound"])
        lb_cmp["higher" if la > lb else "equal" if la == lb else "lower"] += 1
    return {"stored_as": "data/" + out_file.name, "semantic_sha256": sh,
            "historical_semantic_sha256": hist["provenance"]["semantic_sha256"],
            "same_semantic_hash_as_historical": sh == hist["provenance"]["semantic_sha256"],
            "passes_corrected_checker": ok, "checker_newton_confirmed": rep["newton_confirmed"],
            "checker_carrier_confirmed": rep["carrier_confirmed"], "checker_failures": rep["failures"],
            "n_boxes": cert["n_boxes"], "max_depth_used": cert["max_depth_used"],
            "min_lower_bound": cert["min_lower_bound"], "min_lower_bound_decimal": cert["min_lower_bound_decimal"],
            "historical_min_lower_bound": hist["min_lower_bound"],
            "endpoints": {k: {"certified": cert["endpoints"][k]["certified"],
                              "kappa_hat": cert["endpoints"][k]["kappa_hat"],
                              "kappa_hat_lower_bound": cert["endpoints"][k]["kappa_hat_lower_bound"],
                              "historical_kappa_hat_lower_bound": hist["endpoints"][k]["kappa_hat_lower_bound"]}
                          for k in ("q=0", "corner")},
            "endpoint_records_identical_to_historical": cert["endpoints"] == hist["endpoints"],
            "corner_identification": cert["corner_identification"],
            "identical_to_historical": same_keys, "same_q_partition": part_same,
            "build_conditions": "as scripts/run_B1.py: mpmath 40 digits, Arb 128 bits, python-flint default ctx.cap",
            "boxes_differing_from_historical": len(diff_boxes), "differing_boxes_by_regime": regimes,
            "near_regime_boxes_in_historical": sum(b["regime"] == "near" for b in hist["boxes"]),
            "differing_fields_count": fields,
            "delta_balls_overlapping_historical": nested,
            "lower_bounds_vs_historical": lb_cmp,
            "lemma_K_claim_identical": all(same_keys[k] for k in ("claim", "statement", "expressions",
                                                                    "expression_sha256", "frozen_inputs"))
                                       and part_same and ok and cert["min_lower_bound"] == hist["min_lower_bound"],
            "ctx.cap before / after": [cap0, ctx.cap]}


def b23_static():
    src = (ROOT / "src" / "cube_bif" / "b2_check.py").read_text()
    tree = ast.parse(src)
    mods, names = [], set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            mods += [a.name for a in node.names]
        elif isinstance(node, ast.ImportFrom):
            mods.append(("." * node.level) + (node.module or ""))
            names |= {a.name for a in node.names}
        elif isinstance(node, ast.Name):
            names.add(node.id)
        elif isinstance(node, ast.Attribute):
            names.add(node.attr)
    return {"modules_imported": sorted(set(mods)),
            "imports_project_modules": sorted(m for m in mods if m.startswith(".") or m.startswith("cube_bif")),
            "uses_arb_series": "arb_series" in names,
            "mentions_b1_cert_or_b1_check": bool({"b1_cert", "b1_check"} & names),
            "calls_a_taylor_routine": bool({"_taylor", "taylor"} & names)}


def b23_cross_check():
    proc = subprocess.run([sys.executable, "-c", B23_CHILD, str(ROOT)], capture_output=True, text=True)
    if proc.returncode != 0:
        return {"ok": False, "error": proc.stderr[-2000:]}
    out = json.loads(proc.stdout.strip().splitlines()[-1])
    out["method"] = ("src/cube_bif/b2_check.py, Arb at 192 bits: divided differences from the integral "
                     "f_hat = int_0^1 f'(q + t(p - q)) dt (midpoint rule with exact remainder, centred forms), no "
                     "Taylor series; run in a fresh interpreter in which importing cube_bif.b1_cert or "
                     "cube_bif.b1_check raises")
    out["static"] = b23_static()
    return out


def main():
    import flint
    import mpmath as mp
    import sympy as sp
    from flint import ctx
    from cube_bif import STATUS, __version__, b1_check
    hist_bytes = (DATA / "B1_kappa_certificate.json").read_bytes()
    out = {"erratum": "E-B1", "project_version": __version__, "status": STATUS,
           "environment": {"python": sys.version.split()[0], "python-flint": flint.__version__,
                           "FLINT": flint.__FLINT_VERSION__, "sympy": sp.__version__, "mpmath": mp.__version__,
                           "default_ctx_cap": ctx.cap}}
    out["diagnostic_point"] = diagnostic_point()
    derived = b1_check.derive_functions()
    out["historical_certificate_replay"] = historical_replay(derived)
    out["fresh_corrected_rebuild"] = fresh_rebuild(derived)
    out["B2_3_non_taylor_cross_check"] = b23_cross_check()
    out["historical_certificate_bytes_unchanged"] = (DATA / "B1_kappa_certificate.json").read_bytes() == hist_bytes
    h, f, b = out["historical_certificate_replay"], out["fresh_corrected_rebuild"], out["B2_3_non_taylor_cross_check"]
    out["all_required"] = bool(
        h["ok"] and h["semantic_sha256"] == HISTORICAL_SEMANTIC and h["newton_confirmed"] == 222
        and h["carrier_confirmed"] == 222 and h["endpoints_accepted"] and h["min_lower_bound"] == "1311719/536870912"
        and f["passes_corrected_checker"] and b.get("ok") and b.get("curve_reverified_b1_boxes") == 222
        and not b.get("b1_modules_imported") and not out["diagnostic_point"]["corrected_generator_excludes"]
        and not out["diagnostic_point"]["corrected_checker_excludes"] and out["historical_certificate_bytes_unchanged"])
    (DATA / "B1_ERRATUM_report.json").write_text(json.dumps(out, indent=1, default=str))
    print(json.dumps({k: v for k, v in out.items() if k != "diagnostic_point"}, indent=1, default=str)[:6000])
    return 0 if out["all_required"] else 1


if __name__ == "__main__":
    sys.exit(main())
