"""Controls for the identity checker (scripts/check_identity_V0_4_dev6.py): every forbidden modification below is
applied to a scratch copy of the V0.4-dev.6 tree, SHA256SUMS is regenerated afterwards (as a careful forger would), and
the checker must FAIL. The unmodified copy must PASS. Writes data/B2_5_identity_controls.json.

The mutation helpers are imported unchanged from scripts/identity_controls_V0_4_dev4.py, and the dev.5 forbidden
modifications from scripts/identity_controls_V0_4_dev5.py (both stay byte-identical); B2.4- and dev.6-specific
controls are added here.

Usage: python scripts/identity_controls_V0_4_dev6.py <EIT_LJ_CUBE_BIFURCATIONS_V0.4-dev.5.zip>
"""
import json
import pathlib
import shutil
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import check_identity_V0_4_dev6 as idc  # noqa: E402
import identity_controls_V0_4_dev4 as h  # noqa: E402
import identity_controls_V0_4_dev5 as prev  # noqa: E402

regen_manifest, replace, append, delete, add = h.regen_manifest, h.replace, h.append, h.delete, h.add

CONTROLS = [c for c in prev.CONTROLS if c[1] != "stale"] + [
    # B2.4 (Proposition B2) must stay byte-identical
    ("B2.4: b2_branch.py changed", append("src/cube_bif/b2_branch.py", "\n")),
    ("B2.4: B2_4_branch.json changed", append("data/B2_4_branch.json", " ")),
    ("B2.4: dependency graph changed", append("data/B2_4_dependency_graph.json", " ")),
    ("B2.4: negative-control record changed", append("data/B2_4_negative_controls.json", " ")),
    ("B2.4: test_B2_branch.py changed", append("tests/test_B2_branch.py", "\n")),
    ("B2.4: run_B2_4.py changed", append("scripts/run_B2_4.py", "\n")),
    ("dev.5 identity checker changed (imported by nothing, must stay)", append("scripts/check_identity_V0_4_dev5.py", "\n")),
    ("dev.5 identity controls changed (the dev.6 controls import them)",
     append("scripts/identity_controls_V0_4_dev5.py", "\n")),
    ("dev.5 identity report changed", append("docs/V0.4-dev.5_IDENTITY_CHECK.md", "\n")),
    ("audits/README.md changed (no new audit in dev.6)", append("audits/README.md", "\n")),
    ("B1 re-audit report changed", replace("audits/CUBE_BIFURCATIONS_V04_DEV4_B1_ERRATUM_REAUDIT.md", "PASS", "PASS.")),
    # documentation rules
    ("NOTES §12 (B2.4) body changed", replace("NOTES.md", "### 12.10 Claim boundary", "### 12.10 Claim boundary (edited)")),
    ("NOTES §11 status upgraded", replace("NOTES.md", "## 11. Targeted re-audit of erratum E-B1",
                                          "## 11. Targeted re-audit of erratum E-B1 (edited)")),
    ("CHANGELOG dev.5 entry changed", replace("CHANGELOG.md", "## V0.4-dev.5 — 2026-11-14",
                                              "## V0.4-dev.5 — 2026-11-15")),
    ("RESEARCH_LOG dev.5 text changed", replace("RESEARCH_LOG.md", "V0.4-dev.5", "V0.4-dev.5*")),
    ("__init__.py: wrong version value", replace("src/cube_bif/__init__.py", '__version__ = "0.4.0.dev6"',
                                                 '__version__ = "0.4.0"')),
    ("unexpected file added: data/B2_5_extra.json", add("data/B2_5_extra.json", "{}\n")),
    ("stale SHA256SUMS (file changed, manifest not regenerated)", "stale"),
]


def main(argv):
    zip_path = argv[0]
    results = []
    with tempfile.TemporaryDirectory() as tmp:
        base = pathlib.Path(tmp) / "base"
        shutil.copytree(ROOT, base, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))
        _, fails, _ = idc.run(zip_path, base)
        results.append({"control": "unmodified V0.4-dev.6 tree", "required": "PASS",
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
    (ROOT / "data" / "B2_5_identity_controls.json").write_text(json.dumps(
        {"all_as_required": ok, "forbidden_modifications_rejected": sum(r["as_required"] for r in results[1:]),
         "forbidden_modifications": len(results) - 1, "controls": results}, indent=1))
    print(f"{sum(r['as_required'] for r in results[1:])}/{len(results) - 1} forbidden modifications rejected; "
          f"unmodified tree {'PASS' if results[0]['as_required'] else 'FAIL'}")
    return ok


if __name__ == "__main__":
    sys.exit(0 if main(sys.argv[1:]) else 1)
