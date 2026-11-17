"""Code-mutation controls for Phase B2.3 (generator b2_cert.py and checker b2_check.py). Each mutation is applied to a
scratch copy of the project (data included) and must make the named test fail. Every target is first run on an
unmutated copy and must pass there, so that a failure under a mutation is not a missing or broken target. Kept
separate from the earlier control scripts so that they and their records stay byte-identical. Writes
data/B2_3_negative_controls.json."""
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
G = "src/cube_bif/b2_cert.py"
C = "src/cube_bif/b2_check.py"
T = "tests/test_B2_certificate.py::"
FRESH = T + "test_fresh_build_is_accepted_by_the_independent_checker"
STORED = T + "test_stored_certificate_passes_the_independent_checker"


def forgery(name):
    return T + f"test_consistent_forgery_is_rejected[{name}]"


MUTATIONS = [
    # ---- generator: the fresh certificate must be rejected by the unchanged checker (or a direct test must fail)
    ("generator: Q coefficient 6 -> 4 for Qh_uuvv", G,
     "    Qh = sum((b2.Q_BINOM[c] * rho", '    Qh = sum(((4 if c == "uuvv" else b2.Q_BINOM[c]) * rho', FRESH),
    ("generator: Eg back-reaction deleted", G,
     "    c = (Qh - fmpq(3, 2) * bA * bA - 3 * bE * bE / F[\"hE\"]) / (n2 * n2)",
     "    c = (Qh - fmpq(3, 2) * bA * bA) / (n2 * n2)", FRESH),
    ("generator: Eg factor 3 -> 2", G, "- 3 * bE * bE / F[\"hE\"]) / (n2 * n2)", "- 2 * bE * bE / F[\"hE\"]) / (n2 * n2)",
     FRESH),
    ("generator: kernel sign flipped (rho = +Mh12/Mh22)", G, "    rho = -F[\"M12\"] / F[\"M22\"]",
     "    rho = F[\"M12\"] / F[\"M22\"]", FRESH),
    ("generator: hE_hat closed form doubled", G, "EXPR = {**M_EXPR, **b2.G4_CLOSED}",
     "EXPR = {**M_EXPR, **b2.G4_CLOSED, \"hE\": 2 * b2.G4_CLOSED[\"hE\"]}", FRESH),
    ("generator: corner from the values f(q_c) instead of the derivatives f'(q_c)", G,
     "    res = (carrier_fn or carrier)(derivatives(Qc))", "    res = (carrier_fn or carrier)(funcs(Qc))", FRESH),
    ("generator: q = 0 endpoint without the exact values f(0)", G,
     "{k: (fP[k] - f0[k]) / P for k in NAMES}", "{k: fP[k] / P for k in NAMES}", FRESH),
    ("generator: recorded lower bound = upper end of the box enclosure", G,
     "    lb = dyadic_lower_bound(res[\"c4_hat\"])\n", "    lb = arb_to_fmpq(res[\"c4_hat\"].upper())\n", FRESH),
    ("generator: series length not set (python-flint cap; truncated series zero-padded)", G,
     "    ctx.cap = n\n", "    pass\n",
     T + "test_generator_series_have_the_requested_length_and_correct_high_coefficients"),
    ("generator: symmetric Taylor remainder dropped", G, "        v = cH[k][2 * K_SYM + 1]\n", "        v = arb(0)\n",
     T + "test_generator_divided_differences_contain_the_quotient"),
    ("generator: B1 semantic-hash pin not enforced", G, "    if h != B1_SEMANTIC_PINNED:", "    if False:",
     T + "test_B1_certificate_is_pinned_and_loaded_only_with_the_pinned_hash"),
    # ---- checker: a forgery must still be rejected, the valid certificate accepted, enclosures valid
    ("checker: imported B1 semantic hash not compared with the pin", C,
     "    if imp.get(\"semantic_sha256\") != B1_SEMANTIC_PINNED:", "    if False:", forgery("wrong B1 semantic hash")),
    ("checker: gaps and overlaps in the q-coverage not checked", C,
     "        if _q(a[\"q_hi\"]) != _q(b[\"q_lo\"]):", "        if False:", forgery("gap in the q-coverage")),
    ("checker: imported B1 boxes not compared", C, "        if not same:", "        if False:",
     forgery("modified imported B1 delta-ball")),
    ("checker: kernel sign flipped (v = (Mh22, +Mh12))", C, "    v1, v2 = G[\"M22\"], -G[\"M12\"]",
     "    v1, v2 = G[\"M22\"], G[\"M12\"]", STORED),
    ("checker: midpoint-rule remainder dropped", C,
     "        acc = [a + w * m + (w ** 3 / 24) * d0 * d0 * c for a, m, c in zip(acc, mid, rem)]",
     "        acc = [a + w * m for a, m, c in zip(acc, mid, rem)]",
     T + "test_checker_point_values_contain_the_reference"),
    ("checker: centred form without the t-variation inside a subinterval", C,
     "        E = (Q - q0) + (T - ti) * D + ti * (D - d0)", "        E = (Q - q0) + ti * (D - d0)",
     T + "test_checker_box_ranges_contain_exact_values"),
    ("checker: raw c4 at the endpoints not checked", C,
     "        if not (raw == 0) or not str(rec.get(\"raw_c4\", \"\")).startswith(\"0 (\"):", "        if False:",
     forgery("raw c4 > 0 claimed at q = 0")),
    ("checker: box bound compared with 0 instead of the recorded lower bound", C,
     "res[\"c4_hat\"] > arb(lb_c)", "res[\"c4_hat\"] > 0", forgery("inflated lower bound on the first box")),
    ("checker: corner evaluated off the diagonal (delta = 1 instead of 0)", C,
     "    _endpoint(model, ec, dd_point(model, Qc, arb(0), 1)", "    _endpoint(model, ec, dd_point(model, Qc, arb(1), 1)",
     STORED),
    ("checker: semantic hash not compared", C,
     "    if cert.get(\"provenance\", {}).get(\"semantic_sha256\") != sh:", "    if False:",
     T + "test_modified_semantic_hash_and_hash_file_are_rejected"),
    ("checker: Newton inclusion always accepted", C,
     "        if Nw.lower() > Dk.lower() and Nw.upper() < Dk.upper():", "        if True:",
     T + "test_checker_rejects_a_delta_ball_that_misses_the_curve"),
    ("checker: stored expressions not compared with the independent derivation", C,
     "        if k not in ex or sp.simplify(sp.radsimp(stored_expr(ex[k]) - funcs[k])) != 0:", "        if k not in ex:",
     forgery("altered hE_hat")),
    ("checker: stored formulas not compared", C, "    if cert.get(\"formulas\") != EXPECTED_FORMULAS:", "    if False:",
     forgery("deleted Eg correction")),
]


def _copy(tmp):
    dst = pathlib.Path(tmp) / "proj"
    shutil.copytree(ROOT, dst, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))
    return dst


def _run(dst, target):
    proc = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", target],
                          cwd=dst, capture_output=True, text=True)
    out = proc.stdout + proc.stderr
    collected = proc.returncode not in (4, 5) and "no tests ran" not in out and "not found:" not in out
    return proc.returncode, collected, out


def main():
    baseline = {}
    with tempfile.TemporaryDirectory() as tmp:
        dst = _copy(tmp)
        for target in sorted({m[4] for m in MUTATIONS}):
            code, collected, _ = _run(dst, target)
            baseline[target] = {"passes_unmutated": code == 0 and collected}
            print(f"baseline {'ok ' if code == 0 else 'BAD'} {target}")
    results = []
    for name, rel, old, new, target in MUTATIONS:
        with tempfile.TemporaryDirectory() as tmp:
            dst = _copy(tmp)
            f = dst / rel
            text = f.read_text()
            if text.count(old) != 1:
                results.append({"mutation": name, "file": rel, "target": target,
                                "outcome": "NOT APPLIED (pattern not unique)"})
                print(results[-1]["outcome"], name)
                continue
            f.write_text(text.replace(old, new))
            code, collected, out = _run(dst, target)
            detected = code != 0 and collected and baseline[target]["passes_unmutated"]
            results.append({"mutation": name, "file": rel, "target": target,
                            "outcome": "detected (tests fail)" if detected else "NOT DETECTED",
                            "failure_is_an_assertion": "AssertionError" in out or "assert " in out})
        print(f"{results[-1]['outcome']:28s} {name}")
    ok = all(r["outcome"].startswith("detected") for r in results) and all(
        b["passes_unmutated"] for b in baseline.values())
    (ROOT / "data" / "B2_3_negative_controls.json").write_text(json.dumps(
        {"all_detected": ok, "baseline": baseline, "controls": results}, indent=1))
    print(f"{sum(r['outcome'].startswith('detected') for r in results)}/{len(results)} detected")
    return ok


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
