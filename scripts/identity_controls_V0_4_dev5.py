"""Controls for the identity checker (scripts/check_identity_V0_4_dev5.py): every forbidden modification below is
applied to a scratch copy of the V0.4-dev.5 tree, SHA256SUMS is regenerated afterwards (as a careful forger would), and
the checker must FAIL. The unmodified copy must PASS. Writes data/B2_4_identity_controls.json.

The mutation helpers are imported unchanged from scripts/identity_controls_V0_4_dev4.py, which stays byte-identical.

Usage: python scripts/identity_controls_V0_4_dev5.py <EIT_LJ_CUBE_BIFURCATIONS_V0.4-dev.4.zip>
"""
import json
import pathlib
import shutil
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import check_identity_V0_4_dev5 as idc  # noqa: E402
import identity_controls_V0_4_dev4 as h  # noqa: E402

regen_manifest, replace, append, delete, add = h.regen_manifest, h.replace, h.append, h.delete, h.add

CONTROLS = [
    # Paper 2 inputs and Track A
    ("Paper 2 input record changed", append("reference/PAPER2_INPUTS.md", "\n")),
    ("Track A source: lemma_m.py changed", append("src/cube_bif/lemma_m.py", "\n# x\n")),
    ("Track A certificate: A2_lemma_M_certificate.json changed", append("data/A2_lemma_M_certificate.json", " ")),
    ("Track A: theorem_a.py dependency graph changed", replace("src/cube_bif/theorem_a.py", '"H3", ', "")),
    # B0
    ("B0: t2g.py changed", append("src/cube_bif/t2g.py", "\n")),
    # B1 (code, formulas, certificate, erratum artefacts)
    ("B1 generator: corrected Taylor routine changed (ctx.cap no longer raised)",
     replace("src/cube_bif/b1_cert.py", "        ctx.cap = max(old, n)\n", "        ctx.cap = old\n")),
    ("B1 generator: N_TAYLOR 16 -> 12", replace("src/cube_bif/b1_cert.py", "N_TAYLOR = 16", "N_TAYLOR = 12")),
    ("B1 checker: N_CHECK 20 -> 18", replace("src/cube_bif/b1_check.py", "N_CHECK = 20", "N_CHECK = 18")),
    ("B1 checker: Model.taylor changed", replace("src/cube_bif/b1_check.py", "    def taylor(self, x, n):\n",
                                                 "    def taylor(self, x, n):  # x\n")),
    ("B1 exact layer: b1_cubic.py changed", append("src/cube_bif/b1_cubic.py", "\n")),
    ("historical B1 certificate: one byte changed", replace("data/B1_kappa_certificate.json", '"n_boxes": 222',
                                                             '"n_boxes":  222')),
    ("historical B1 certificate replaced by the corrected rebuild", lambda r: shutil.copy(
        r / "data/B1_ERRATUM_corrected_rebuild_certificate.json", r / "data/B1_kappa_certificate.json")),
    ("B1 semantic hash file changed", replace("data/B1_CERTIFICATE_SEMANTIC.sha256", "616817fc", "616817fd")),
    ("B1 erratum: corrected rebuild changed", append("data/B1_ERRATUM_corrected_rebuild_certificate.json", " ")),
    ("B1 erratum: B1_ERRATUM_report.json changed", append("data/B1_ERRATUM_report.json", " ")),
    ("B1 erratum: test_B1_erratum.py changed", append("tests/test_B1_erratum.py", "\n")),
    ("B1 erratum: run_B1_erratum.py changed", append("scripts/run_B1_erratum.py", "\n")),
    ("scripts/run_B1.py changed", append("scripts/run_B1.py", "\n")),
    # B2.0 - B2.3
    ("B2.0: b2_symmetry.py changed", append("src/cube_bif/b2_symmetry.py", "\n")),
    ("B2.1: b2_quartic.py changed", append("src/cube_bif/b2_quartic.py", "\n")),
    ("B2.2: b2_carrier.py changed", append("src/cube_bif/b2_carrier.py", "\n")),
    ("B2.2: B2_carrier.json changed", append("data/B2_carrier.json", " ")),
    ("B2.3: b2_cert.py changed", append("src/cube_bif/b2_cert.py", "\n")),
    ("B2.3: b2_check.py changed", append("src/cube_bif/b2_check.py", "\n")),
    ("B2.3: certificate changed", append("data/B2_c4hat_certificate.json", " ")),
    ("B2.3: B2_3_check_report.json changed", append("data/B2_3_check_report.json", " ")),
    ("B2.3 tests: test_B2_certificate.py changed", append("tests/test_B2_certificate.py", "\n")),
    # earlier scripts, records, reports
    ("dev.4 identity checker changed (the dev.5 checker imports it)",
     append("scripts/check_identity_V0_4_dev4.py", "\n")),
    ("dev.4 identity controls changed (the dev.5 controls import them)",
     append("scripts/identity_controls_V0_4_dev4.py", "\n")),
    ("earlier control record negative_controls.json changed", append("data/negative_controls.json", " ")),
    ("earlier identity report changed", append("docs/V0.4-dev.4_IDENTITY_CHECK.md", "\n")),
    ("historical B1 audit report changed", append("audits/CUBE_BIFURCATIONS_V03_REVIEWER_REPORT.md", "\n")),
    ("Track A audit report changed", append("audits/CUBE_BIFURCATIONS_REVIEWER_REPORT.md", "\n")),
    ("new re-audit report altered", append("audits/CUBE_BIFURCATIONS_V04_DEV4_B1_ERRATUM_REAUDIT.md", "\n")),
    ("audits/README.md: earlier text changed", replace("audits/README.md", "Audit reports are kept byte-identical",
                                                       "Audit reports are kept identical")),
    # structure
    ("file deleted: data/B1_scan.csv", delete("data/B1_scan.csv")),
    ("unexpected file added: src/cube_bif/extra.py", add("src/cube_bif/extra.py", "x = 1\n")),
    ("unexpected file added: data/B2_c4hat_certificate_v2.json", add("data/B2_c4hat_certificate_v2.json", "{}\n")),
    # documentation rules
    ("NOTES §5.7 body changed", replace("NOTES.md", "1311719/536870912 = 0.0024432670…", "1311719/536870912 ≈ 0.0024")),
    ("NOTES §10 erratum body changed", replace("NOTES.md", "### 10.1 The defect", "### 10.1 The issue")),
    ("CHANGELOG dev.4 entry changed", replace("CHANGELOG.md", "## V0.4-dev.4 — 2026-11-14",
                                              "## V0.4-dev.4 — 2026-11-13")),
    ("RESEARCH_LOG earlier entry changed", replace("RESEARCH_LOG.md", "## 2026-11-14 — V0.4-dev.4:",
                                                   "## 2026-11-14 — V0.4-dev.4 (edited):")),
    ("test_docs.py: an unrelated test changed", replace("tests/test_docs.py", "def test_no_novelty_language():",
                                                        "def test_no_novelty_language():  # x")),
    ("__init__.py: code added beyond version/status", append("src/cube_bif/__init__.py", "EXTRA = 1\n")),
    ("stale SHA256SUMS (file changed, manifest not regenerated)", "stale"),
]


def main(argv):
    zip_path = argv[0]
    results = []
    with tempfile.TemporaryDirectory() as tmp:
        base = pathlib.Path(tmp) / "base"
        shutil.copytree(ROOT, base, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))
        _, fails, _ = idc.run(zip_path, base)
        results.append({"control": "unmodified V0.4-dev.5 tree", "required": "PASS",
                        "result": "PASS" if not fails else "FAIL", "as_required": not fails, "failures": fails})
        for name, mutate in CONTROLS:
            dst = pathlib.Path(tmp) / "m"
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(base, dst)
            if mutate == "stale":
                append("src/cube_bif/lemma_m.py", "\n")(dst)
            else:
                mutate(dst)
                regen_manifest(dst)
            _, fails, _ = idc.run(zip_path, dst)
            results.append({"control": name, "required": "FAIL", "result": "FAIL" if fails else "PASS",
                            "as_required": bool(fails), "first_failure": fails[0] if fails else None})
            print(f"{'ok ' if fails else 'MISSED'} {name}: {fails[0] if fails else ''}"[:160], flush=True)
    ok = all(r["as_required"] for r in results)
    (ROOT / "data" / "B2_4_identity_controls.json").write_text(json.dumps(
        {"all_as_required": ok, "forbidden_modifications_rejected": sum(r["as_required"] for r in results[1:]),
         "forbidden_modifications": len(results) - 1, "controls": results}, indent=1))
    print(f"{sum(r['as_required'] for r in results[1:])}/{len(results) - 1} forbidden modifications rejected; "
          f"unmodified tree {'PASS' if results[0]['as_required'] else 'FAIL'}")
    return ok


if __name__ == "__main__":
    sys.exit(0 if main(sys.argv[1:]) else 1)
