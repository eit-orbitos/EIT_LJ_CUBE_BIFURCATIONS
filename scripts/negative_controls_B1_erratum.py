"""Code-mutation controls for erratum E-B1 (b1_cert._taylor and b1_check.Model.taylor). Each mutation is applied to a
scratch copy of the project (data included) and every named test must fail; every target is first run on an
unmutated copy and must pass there. Two controls restore the V0.4-dev.3 routines verbatim (python-flint's default
ctx.cap = 10 in force, truncated series zero-padded). Kept separate from the earlier control scripts so that they and
their records stay byte-identical. Writes data/B1_ERRATUM_negative_controls.json.

Usage: python scripts/negative_controls_B1_erratum.py"""
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
G = "src/cube_bif/b1_cert.py"
C = "src/cube_bif/b1_check.py"
T = "tests/test_B1_erratum.py::"
GEN_SERIES = T + "test_generator_series_have_the_requested_length_and_correct_high_coefficients"
GEN_CAUCHY = T + "test_high_coefficients_against_a_cauchy_integral"
GEN_DIAG = T + "test_diagnostic_point_corrected_generator_contains_the_reference"
CHK_SERIES = T + "test_checker_series_have_the_requested_length_and_correct_high_coefficients"
CHK_DIAG = T + "test_diagnostic_point_corrected_checker_contains_the_reference"
GRID = T + "test_divided_differences_contain_the_reference_on_a_near_grid"
RESTORE = T + "test_ctx_cap_is_restored_after_the_call_and_after_an_exception"
UNRAISED = T + "test_an_unraised_capacity_is_detected_not_zero_padded"
PADDING = T + "test_zero_padding_only_for_exact_trailing_zeros"
FRESH_B1 = "tests/test_B1_certificate.py::test_fresh_certificate_passes_the_independent_checker"


def _between(path, start, end):
    text = (ROOT / path).read_text()
    i = text.index(start)
    return text[i:text.index(end, i)]


OLD_GEN = '''def _taylor(x, n):
    """Taylor coefficients c_0..c_{n-1} of each function at the ball x (enclosures valid for every point of x)."""
    s = arb_series([x, 1], prec=n)
    out = {}
    for k, v in _funcs(s).items():
        c = list(v.coeffs())
        out[k] = c + [arb(0)] * (n - len(c))
    return out


'''
OLD_CHK = '''    def taylor(self, x, n):
        s = arb_series([x, 1], prec=n)
        out = {}
        for k, v in self.values(s).items():
            c = list(v.coeffs())
            out[k] = c + [arb(0)] * (n - len(c))
        return out

'''


def mutations():
    gen_new = _between(G, "def _taylor(x, n):", "def _hull(")
    chk_new = _between(C, "    def taylor(self, x, n):", "    def _raw_series(")
    return [
        # ---- generator
        ("generator: V0.4-dev.3 _taylor restored verbatim (no ctx.cap, zero padding)", G, gen_new, OLD_GEN,
         [GEN_SERIES, GEN_CAUCHY, GEN_DIAG, GRID]),
        ("generator: V0.4-dev.3 _taylor restored verbatim; the fresh B1 certificate is still accepted (no target in "
         "the certificate tests sees the defect, which is why the erratum tests exist)", G, gen_new, OLD_GEN,
         [FRESH_B1], "expected_not_detected"),
        ("generator: ctx.cap set to 10 (the python-flint default) instead of max(old, n)", G,
         "        ctx.cap = max(old, n)\n", "        ctx.cap = 10\n", [GEN_SERIES, GEN_DIAG]),
        ("generator: ctx.cap set to 10 and the capacity guard removed", G,
         ("        ctx.cap = max(old, n)\n        if ctx.cap < n:\n"),
         ("        ctx.cap = 10\n        if False:\n"), [GEN_SERIES, GEN_DIAG]),
        ("generator: previous ctx.cap not restored", G, "    finally:\n        ctx.cap = old\n",
         "    finally:\n        pass\n", [RESTORE]),
        ("generator: check that the capacity really is in force removed", G,
         "        if ctx.cap != cap or cap < n:\n", "        if False:\n", [UNRAISED]),
        ("generator: zero padding without the exact-zero check", G,
         "            if any(not (c2[j] == 0) for j in range(len(c), min(n, len(c2)))):\n",
         "            if False:\n", [PADDING]),
        # ---- checker
        ("checker: V0.4-dev.3 Model.taylor restored verbatim (no ctx.cap, zero padding)", C, chk_new, OLD_CHK,
         [CHK_SERIES, CHK_DIAG, GRID]),
        ("checker: ctx.cap set to 10 instead of the requested length", C,
         "        if self.saved < self.length:\n            ctx.cap = self.length\n",
         "        if self.saved < self.length:\n            ctx.cap = 10\n", [CHK_SERIES, CHK_DIAG]),
        ("checker: ctx.cap set to 10 and the capacity guard removed", C,
         "            ctx.cap = self.length\n        if ctx.cap < self.length:\n",
         "            ctx.cap = 10\n        if False:\n", [CHK_SERIES, CHK_DIAG]),
        ("checker: saved ctx.cap not restored on exit", C,
         "    def __exit__(self, exc_type, exc, tb):\n        ctx.cap = self.saved\n",
         "    def __exit__(self, exc_type, exc, tb):\n        pass\n", [RESTORE]),
        ("checker: check that the capacity really is in force removed", C,
         "            if ctx.cap != cap or cap < n:\n", "            if False:\n", [UNRAISED]),
        ("checker: zero padding without the exact-zero check", C,
         "                    if j < len(ext) and not (ext[j] == 0):\n", "                    if False:\n",
         [PADDING]),
    ]


def _copy(tmp):
    dst = pathlib.Path(tmp) / "proj"
    shutil.copytree(ROOT, dst, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))
    return dst


def _run(dst, targets):
    proc = subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *targets],
                          cwd=dst, capture_output=True, text=True)
    out = proc.stdout + proc.stderr
    collected = proc.returncode not in (4, 5) and "no tests ran" not in out and "not found:" not in out
    failed = sum(1 for t in targets if f"FAILED {t}" in out or f"ERROR {t}" in out)
    return proc.returncode, collected, failed, out


def baseline_part(targets):
    out = {}
    with tempfile.TemporaryDirectory() as tmp:
        dst = _copy(tmp)
        for target in targets:
            code, collected, _, _ = _run(dst, [target])
            out[target] = {"passes_unmutated": code == 0 and collected}
            print(f"baseline {'ok ' if code == 0 else 'BAD'} {target}", flush=True)
    return out


def mutation_part(m, baseline):
    name, rel, old, new, targets = m[:5]
    expect = m[5] if len(m) > 5 else "detected"
    with tempfile.TemporaryDirectory() as tmp:
        dst = _copy(tmp)
        f = dst / rel
        text = f.read_text()
        if text.count(old) != 1:
            r = {"mutation": name, "file": rel, "targets": targets, "outcome": "NOT APPLIED (pattern not unique)",
                 "as_required": False}
            print(r["outcome"], name, flush=True)
            return r
        f.write_text(text.replace(old, new))
        code, collected, failed, out = _run(dst, targets)
    base_ok = all(baseline[t]["passes_unmutated"] for t in targets)
    every_target_fails = code != 0 and collected and failed == len(targets)
    if expect == "detected":
        outcome = "detected (every target fails)" if every_target_fails and base_ok else "NOT DETECTED"
        ok = outcome.startswith("detected")
    else:
        outcome = "not detected by this target, as expected" if code == 0 and collected else "target failed"
        ok = code == 0 and collected
    r = {"mutation": name, "file": rel, "targets": targets, "targets_failed": failed, "required": expect,
         "outcome": outcome, "as_required": ok,
         "failure_is_an_assertion_or_error": ("AssertionError" in out or "assert " in out or "Error" in out)
         if failed else None}
    print(f"{r['outcome']:40s} {name}", flush=True)
    return r


def assemble(baseline, results):
    ok = all(r["as_required"] for r in results) and all(b["passes_unmutated"] for b in baseline.values())
    (ROOT / "data" / "B1_ERRATUM_negative_controls.json").write_text(json.dumps(
        {"all_as_required": ok, "baseline": baseline, "controls": results}, indent=1))
    n_det = sum(r["required"] == "detected" and r["as_required"] for r in results if "required" in r)
    print(f"{n_det}/{sum(r.get('required') == 'detected' for r in results)} detected; "
          f"{sum(r['as_required'] for r in results)}/{len(results)} as required")
    return ok


def main(argv=()):
    """No arguments: everything in one run. Resumable parts (for environments that limit the length of one command):
    --state DIR --part baseline | --part <index> | --part assemble."""
    muts = mutations()
    targets = sorted({t for m in muts for t in m[4]})
    if "--part" not in argv:
        baseline = baseline_part(targets)
        return assemble(baseline, [mutation_part(m, baseline) for m in muts])
    state = pathlib.Path(argv[argv.index("--state") + 1])
    state.mkdir(parents=True, exist_ok=True)
    part = argv[argv.index("--part") + 1]
    if part == "baseline":
        (state / "baseline.json").write_text(json.dumps(baseline_part(targets)))
        return True
    baseline = json.loads((state / "baseline.json").read_text())
    if part == "assemble":
        results = [json.loads((state / f"m{i:02d}.json").read_text()) for i in range(len(muts))]
        return assemble(baseline, results)
    i = int(part)
    (state / f"m{i:02d}.json").write_text(json.dumps(mutation_part(muts[i], baseline)))
    return True


if __name__ == "__main__":
    sys.exit(0 if main(sys.argv[1:]) else 1)
