"""Controls for the identity checker (scripts/check_identity_V0_4_dev4.py): every forbidden modification below is
applied to a scratch copy of the V0.4-dev.4 tree, SHA256SUMS is regenerated afterwards (as a careful forger would), and
the checker must FAIL. The unmodified copy must PASS. Writes data/B1_ERRATUM_identity_controls.json.

Usage: python scripts/identity_controls_V0_4_dev4.py <EIT_LJ_CUBE_BIFURCATIONS_V0.4-dev.3.zip>
"""
import hashlib
import json
import pathlib
import shutil
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import check_identity_V0_4_dev4 as idc  # noqa: E402


def regen_manifest(root):
    lines = []
    for p in sorted(root.rglob("*")):
        rel = p.relative_to(root).as_posix()
        if p.is_file() and rel != "SHA256SUMS":
            lines.append(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  ./{rel}")
    (root / "SHA256SUMS").write_text("\n".join(lines) + "\n")


def replace(rel, old, new):
    def f(root):
        p = root / rel
        t = p.read_text()
        assert t.count(old) >= 1, (rel, old)
        p.write_text(t.replace(old, new, 1))
    return f


def append(rel, text):
    def f(root):
        p = root / rel
        p.write_bytes(p.read_bytes() + text.encode())
    return f


def delete(rel):
    return lambda root: (root / rel).unlink()


def add(rel, text):
    return lambda root: (root / rel).write_text(text)


CONTROLS = [
    ("Track A source: lemma_m.py changed", append("src/cube_bif/lemma_m.py", "\n# x\n")),
    ("Track A certificate: A2_lemma_M_certificate.json changed", append("data/A2_lemma_M_certificate.json", " ")),
    ("Track A: theorem_a.py dependency graph changed", replace("src/cube_bif/theorem_a.py", '"H3", ', "")),
    ("B0: t2g.py changed", append("src/cube_bif/t2g.py", "\n")),
    ("B1 formula: g_uuv denominator 54 -> 52 in b1_cert._funcs (outside the Taylor routine)",
     replace("src/cube_bif/b1_cert.py", "(54 * W)", "(52 * W)")),
    ("B1 generator: N_TAYLOR 16 -> 12", replace("src/cube_bif/b1_cert.py", "N_TAYLOR = 16", "N_TAYLOR = 12")),
    ("B1 generator: comment added inside newton()", replace("src/cube_bif/b1_cert.py",
                                                           "    proven = False\n", "    proven = False  # x\n")),
    ("B1 checker: Newton inclusion relaxed (outside Model.taylor)", replace(
        "src/cube_bif/b1_check.py", "    return Nw if (Nw.lower() > D.lower() and Nw.upper() < D.upper()) else None",
        "    return Nw")),
    ("B1 checker: N_CHECK 20 -> 18", replace("src/cube_bif/b1_check.py", "N_CHECK = 20", "N_CHECK = 18")),
    ("B1 checker: Model.dd changed", replace("src/cube_bif/b1_check.py", "        N = N_CHECK\n",
                                             "        N = N_CHECK - 1\n")),
    ("B1 exact layer: b1_cubic.py changed", append("src/cube_bif/b1_cubic.py", "\n")),
    ("historical B1 certificate: one byte changed", replace("data/B1_kappa_certificate.json", '"n_boxes": 222',
                                                             '"n_boxes":  222')),
    ("historical B1 certificate replaced by the corrected rebuild", lambda r: shutil.copy(
        r / "data/B1_ERRATUM_corrected_rebuild_certificate.json", r / "data/B1_kappa_certificate.json")),
    ("B1 semantic hash file changed", replace("data/B1_CERTIFICATE_SEMANTIC.sha256", "616817fc", "616817fd")),
    ("B1 records: B1_negative_controls.json changed", append("data/B1_negative_controls.json", "\n")),
    ("scripts/run_B1.py changed", append("scripts/run_B1.py", "\n")),
    ("B2.0: b2_symmetry.py changed", append("src/cube_bif/b2_symmetry.py", "\n")),
    ("B2.1: b2_quartic.py changed", append("src/cube_bif/b2_quartic.py", "\n")),
    ("B2.2: b2_carrier.py changed", append("src/cube_bif/b2_carrier.py", "\n")),
    ("B2.2: B2_carrier.json changed", append("data/B2_carrier.json", " ")),
    ("B2.3: b2_cert.py changed", append("src/cube_bif/b2_cert.py", "\n")),
    ("B2.3: b2_check.py changed", append("src/cube_bif/b2_check.py", "\n")),
    ("B2.3: certificate changed", append("data/B2_c4hat_certificate.json", " ")),
    ("B2.3: historical series-cap diagnostic changed", append("data/B2_3_B1_series_cap_diagnostic.json", " ")),
    ("B2.3: diagnose_B1_series_cap.py changed", append("scripts/diagnose_B1_series_cap.py", "\n")),
    ("earlier control record negative_controls.json changed", append("data/negative_controls.json", " ")),
    ("earlier control script negative_controls.py changed", append("scripts/negative_controls.py", "\n")),
    ("historical B1 audit report changed", append("audits/CUBE_BIFURCATIONS_V03_REVIEWER_REPORT.md", "\n")),
    ("Track A audit report changed", append("audits/CUBE_BIFURCATIONS_REVIEWER_REPORT.md", "\n")),
    ("Paper 2 input record changed", append("reference/PAPER2_INPUTS.md", "\n")),
    ("earlier identity report changed", append("docs/V0.4-dev.3_IDENTITY_CHECK.md", "\n")),
    ("file deleted: data/B1_scan.csv", delete("data/B1_scan.csv")),
    ("unexpected file added: src/cube_bif/extra.py", add("src/cube_bif/extra.py", "x = 1\n")),
    ("unexpected file added: data/B1_kappa_certificate_v2.json", add("data/B1_kappa_certificate_v2.json", "{}\n")),
    ("NOTES §5.7 body changed", replace("NOTES.md", "1311719/536870912 = 0.0024432670…", "1311719/536870912 ≈ 0.0024")),
    ("CHANGELOG earlier entry changed", replace("CHANGELOG.md", "## V0.4-dev.2 — 2026-11-13", "## V0.4-dev.2 — 2026-11-12")),
    ("RESEARCH_LOG earlier entry changed", replace("RESEARCH_LOG.md", "## 2026-11-13 — V0.4-dev.3",
                                                   "## 2026-11-13 — V0.4-dev.3 (edited)")),
    ("test_B1_certificate.py: another test changed", replace("tests/test_B1_certificate.py",
                                                             "assert min(lbs) > fmpq(24, 10000)",
                                                             "assert min(lbs) > fmpq(20, 10000)")),
    ("test_docs.py: change beyond the status pins", replace("tests/test_docs.py", "assert len(headings) == 2",
                                                            "assert len(headings) >= 2")),
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
        results.append({"control": "unmodified V0.4-dev.4 tree", "required": "PASS",
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
    (ROOT / "data" / "B1_ERRATUM_identity_controls.json").write_text(json.dumps(
        {"all_as_required": ok, "forbidden_modifications_rejected": sum(r["as_required"] for r in results[1:]),
         "forbidden_modifications": len(results) - 1, "controls": results}, indent=1))
    print(f"{sum(r['as_required'] for r in results[1:])}/{len(results) - 1} forbidden modifications rejected; "
          f"unmodified tree {'PASS' if results[0]['as_required'] else 'FAIL'}")
    return ok


if __name__ == "__main__":
    sys.exit(0 if main(sys.argv[1:]) else 1)
