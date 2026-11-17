"""Forbidden-edit controls for scripts/check_preservation_V1_0_0.py.

Usage:  python scripts/preservation_controls_V1_0_0.py <EIT_LJ_CUBE_BIFURCATIONS_V0.4-dev.6.zip> [project root]
        [--rc2=<EIT_LJ_CUBE_BIFURCATIONS_V1.0.0-rc2.zip>] [--out docs/V1.0.0_PRESERVATION_CONTROLS.json]

Each control copies the V1.0.0 tree to a scratch directory, applies one forbidden modification,
regenerates SHA256SUMS (so that a regenerated manifest cannot hide the change; one control leaves it stale on purpose)
and requires the checker to FAIL. The unmodified copy, with a regenerated manifest, must PASS.
"""
import hashlib
import json
import pathlib
import shutil
import sys
import tempfile

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import check_preservation_V1_0_0 as chk  # noqa: E402


def write_manifest(root):
    root = pathlib.Path(root)
    lines = []
    for p in sorted(root.rglob("*")):
        if p.is_dir():
            continue
        rel = p.relative_to(root).as_posix()
        if rel == "SHA256SUMS" or "__pycache__" in rel or rel.startswith(".pytest_cache") or rel.endswith(".pyc"):
            continue
        lines.append(f"{hashlib.sha256(p.read_bytes()).hexdigest()}  ./{rel}")
    (root / "SHA256SUMS").write_text("\n".join(lines) + "\n")


def _edit(rel, fn):
    def apply(root):
        p = root / rel
        p.write_bytes(fn(p.read_bytes()))
    return apply


def _append(rel, extra=b"\n"):
    return _edit(rel, lambda b: b + extra)


def _replace(rel, old, new):
    def f(b):
        assert old.encode() in b, (rel, old)
        return b.replace(old.encode(), new.encode(), 1)
    return _edit(rel, f)


def _delete(rel):
    return lambda root: (root / rel).unlink()


def _add(rel, content=b"x\n"):
    def apply(root):
        (root / rel).parent.mkdir(parents=True, exist_ok=True)
        (root / rel).write_bytes(content)
    return apply


def _drop_line(rel, needle):
    def f(b):
        lines = b.decode().split("\n")
        i = next(k for k, l in enumerate(lines) if needle in l)
        del lines[i]
        return "\n".join(lines).encode()
    return _edit(rel, f)


CONTROLS = []
for label, rel in chk.KEY_ARTIFACTS:
    CONTROLS.append((f"modify key artefact: {label}", _append(rel, b" ")))
for rel in ("src/cube_bif/b1_cert.py", "src/cube_bif/b1_check.py", "src/cube_bif/lemma_m.py",
            "src/cube_bif/certcheck.py", "src/cube_bif/b2_cert.py", "src/cube_bif/b2_check.py",
            "src/cube_bif/b2_branch.py", "src/cube_bif/b2_index.py", "src/cube_bif/b2_quartic.py",
            "src/cube_bif/b2_symmetry.py", "src/cube_bif/theorem_a.py", "src/cube_bif/pairsum.py"):
    CONTROLS.append((f"modify mathematical source: {rel}", _append(rel, b"# edit\n")))
CONTROLS += [
    ("relabel STATUS_PROVED in b2_index.py (audited source)", _replace(
        "src/cube_bif/b2_index.py", "not independently audited", "INDEPENDENTLY AUDITED")),
    ("modify B2.3 negative-control record", _append("data/B2_3_negative_controls.json", b" ")),
    ("modify A1 sign table", _append("data/A1_sign_table.csv", b"0\n")),
    ("modify an earlier script (run_B1.py)", _append("scripts/run_B1.py", b"# edit\n")),
    ("modify an earlier identity-check document", _append("docs/V0.4-dev.6_IDENTITY_CHECK.md")),
    ("modify the external-brainstorm contradictions document", _append("docs/CONTRADICTIONS_EXTERNAL_BRAINSTORM.md")),
    ("modify a mathematical test (test_B2_index.py)", _append("tests/test_B2_index.py", b"# edit\n")),
    ("modify reference/PAPER2_INPUTS.md", _append("reference/PAPER2_INPUTS.md")),
    ("delete a V0.4-dev.6 file (data/B2_scan.csv)", _delete("data/B2_scan.csv")),
    ("add a file under src/", _add("src/cube_bif/extra.py")),
    ("add a file under data/", _add("data/extra.json", b"{}\n")),
    ("add an unexpected file at the root", _add("EXTRA.md")),
    ("add an unexpected script", _add("scripts/extra.py")),
    ("alter a new audit report (B2.5)", _append("audits/CUBE_BIFURCATIONS_V04_DEV6_BLIND_B25_REVIEWER_REPORT.md", b" ")),
    ("alter a new audit report (B2.3)", _append("audits/CUBE_BIFURCATIONS_V05_BLIND_B23_LEMMA_Q_REVIEWER_REPORT.md", b" ")),
    ("__init__.py: code change beyond version/status", _append("src/cube_bif/__init__.py", b"X = 1\n")),
    ("NOTES: delete a formula line (Lemma M bound)", _drop_line("NOTES.md", "161457/262144")),
    ("NOTES: edit the Proposition B3 Hessian line", _replace("NOTES.md", "−κ²s²", "+κ²s²")),
    ("CHANGELOG: edit an earlier entry", _replace("CHANGELOG.md", "## V0.4-dev.6 — 2026-11-15", "## V0.4-dev.6 — 2026-11-16")),
    ("RESEARCH_LOG: edit an earlier line", _replace("RESEARCH_LOG.md", "V0.1-dev: project started", "V0.1-dev: started")),
    ("audits/README.md: delete an earlier line", _drop_line("audits/README.md", "f82c5ef1a03c33c0909313bd6442d1879d39717f991cc8e245eb0c61f75d8b85")),
    ("README: remove the paper title", _replace("README.md", "**Symmetry-Breaking Bifurcations", "**Bifurcations")),
    ("LaTeX build debris in paper/", _add("paper/manuscript.aux")),
    ("add an unexpected test file", _add("tests/test_extra.py")),
    ("alter the B2.4 audit report", _append("audits/CUBE_BIFURCATIONS_V05_BLIND_B24_REVIEWER_REPORT.md", b" ")),
    ("modify proof dependency graph (B2.5)", _replace("data/B2_5_dependency_graph.json", "Haynsworth", "Hainsworth")),
    ("modify historical B1 certificate semantic-hash file", _append("data/B1_CERTIFICATE_SEMANTIC.sha256", b" ")),
]
CONTROLS += [
    ("alter the final blind release audit report", _append("audits/PAPER3_RC2_FINAL_BLIND_RELEASE_AUDIT.md", b" ")),
    ("modify Lemma Q certificate", _append("data/B2_c4hat_certificate.json", b" ")),
    ("modify the B2.5 index record (Morse indices)", _append("data/B2_5_index.json", b" ")),
]
RC2_ONLY = [
    ("alter a historical RC1 record (RELEASE_NOTES_RC1.md)", _append("RELEASE_NOTES_RC1.md")),
    ("alter a historical RC2 record (RELEASE_NOTES_RC2.md)", _append("RELEASE_NOTES_RC2.md")),
    ("alter the RC2 final-audit instructions", _append("FINAL_AUDIT_INSTRUCTIONS.md")),
    ("alter RC2 tooling (scan_text_rc2.py)", _append("scripts/scan_text_rc2.py", b"# edit\n")),
    ("edit a scientific manuscript section (05_a2u_pitchfork.tex)", _append("paper/sections/05_a2u_pitchfork.tex", b"%\n")),
    ("edit a manuscript appendix (B_certificates.tex)", _append("paper/appendices/B_certificates.tex", b"%\n")),
    ("edit a manuscript figure script", _append("paper/figures/make_figures.py", b"# edit\n")),
    ("NOTES: edit a non-status line of the RC2 section §16", _replace(
        "NOTES.md", "metadata were supplied after RC1. RC2 records them", "metadata were supplied before RC1. RC2 records them")),
    ("CHANGELOG: edit the RC2 entry", _replace("CHANGELOG.md", "## V1.0.0-rc2 — 2026-11-16", "## V1.0.0-rc2 — 2026-11-17")),
]
STALE = ("stale manifest (documentation edited, SHA256SUMS not regenerated)", _append("docs/AI_USE_LOG.md"))


def run(baseline_zip, root, rc2_zip=None):
    root = pathlib.Path(root)
    controls = CONTROLS + (RC2_ONLY if rc2_zip else [])
    results = []
    with tempfile.TemporaryDirectory() as td:
        def fresh(name):
            d = pathlib.Path(td) / name
            shutil.copytree(root, d, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache", "*.pyc"))
            return d
        base = fresh("baseline")
        write_manifest(base)
        def checkx(d):
            r = chk.check(baseline_zip, d)
            if rc2_zip:
                fails = chk.compare_rc2(rc2_zip, chk.load_tree(d))["failures"]
                r["failures"] = r["failures"] + fails
                r["pass"] = not r["failures"]
            return r
        b = checkx(base)
        baseline_pass = b["pass"]
        for i, (label, apply) in enumerate(controls + [STALE]):
            d = fresh(f"c{i}")
            write_manifest(d)
            apply(d)
            if (label, apply) != STALE:
                write_manifest(d)
            r = checkx(d)
            results.append({"control": label, "rejected": not r["pass"], "first_failure": (r["failures"] or [""])[0]})
            shutil.rmtree(d)
    return {"rc2_comparison": bool(rc2_zip), "baseline_pass": baseline_pass, "baseline_failures": b["failures"], "n_controls": len(results),
            "n_rejected": sum(r["rejected"] for r in results), "all_rejected": all(r["rejected"] for r in results),
            "controls": results}


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    opts = dict(a.split("=", 1) for a in argv[1:] if a.startswith("--") and "=" in a)
    root = args[1] if len(args) > 1 else str(pathlib.Path(__file__).resolve().parents[1])
    res = run(args[0], root, opts.get("--rc2"))
    if "--out" in opts:
        pathlib.Path(opts["--out"]).write_text(json.dumps(res, indent=2, ensure_ascii=False) + "\n")
    print(f"baseline pass: {res['baseline_pass']}; rejected {res['n_rejected']}/{res['n_controls']}")
    for r in res["controls"]:
        if not r["rejected"]:
            print("  NOT REJECTED:", r["control"])
    return 0 if res["baseline_pass"] and res["all_rejected"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
