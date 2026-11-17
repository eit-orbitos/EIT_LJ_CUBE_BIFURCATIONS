"""Mechanical preservation check for V1.0.0: against the audited V0.4-dev.6 archive and against V1.0.0-rc2.

Usage:  python scripts/check_preservation_V1_0_0.py <EIT_LJ_CUBE_BIFURCATIONS_V0.4-dev.6.zip> [project root]
        [--rc2=<EIT_LJ_CUBE_BIFURCATIONS_V1.0.0-rc2.zip>] [--report <md>] [--json <path>]

Part 1 (against V0.4-dev.6, SHA-256 c473af60...b691) - the rules of the RC2 checker, with the V1.0.0 file set:
- No file of V0.4-dev.6 may be removed. Every V0.4-dev.6 file is byte-identical except the files in CHANGEABLE, each
  under its own rule (README: title kept; NOTES: only status lines - lines naming audit/status/pending/not_provided, or
  lines of a status block that starts with '**Status' - removed/replaced; CHANGELOG: insert-only;
  RESEARCH_LOG: append-only; audits/README.md: insert-only; src/cube_bif/__init__.py: docstring, __version__ and
  STATUS only; tests/test_docs.py: status test; SHA256SUMS: must match the tree).
- Added files only under ALLOWED_ADDED; the four audit reports added since V0.4-dev.6 must have their exact hashes;
  nothing may be added under src/ or data/.
Part 2 (--rc2, against V1.0.0-rc2, SHA-256 6dee0be5...1a08) - every file that differs from RC2 is listed and classified:
- FORBIDDEN: any change, addition or removal under src/ (except __init__.py under its rule), data/, reference/; any
  change of an audit report or a historical RC1/RC2 record; any change of a V0.4-dev.6 script or test (except
  tests/test_docs.py); any change of a manuscript file other than PAPER_CHANGEABLE (so every scientific section,
  appendix and figure of the manuscript is byte-identical with RC2); any removal other than REMOVABLE_VS_RC2.
- Rule-checked against RC2: NOTES.md (only status lines removed/replaced), CHANGELOG.md (insert-only),
  RESEARCH_LOG.md (append-only), audits/README.md (insert-only), src/cube_bif/__init__.py (docstring/version/status).
"""
import ast
import difflib
import hashlib
import io
import json
import pathlib
import re
import sys
import zipfile

BASELINE_SHA256 = "c473af60f8b54c0beecd252d9e8409eef734ba475c0d693b300946f57941b691"
RC2_SHA256 = "6dee0be5f975d23fce3a36770ddebad8041aae9e3f302df0cd923fad91481a08"
PREFIX = "EIT_LJ_CUBE_BIFURCATIONS/"

NEW_AUDITS = {
    "audits/CUBE_BIFURCATIONS_V05_BLIND_B23_LEMMA_Q_REVIEWER_REPORT.md":
        "841152f2cccd0a43c4f8e73ce5d0cf37e9793d26f12047d5143ea5a053e96bcf",
    "audits/CUBE_BIFURCATIONS_V05_BLIND_B24_REVIEWER_REPORT.md":
        "0302930b9a96ac6bca3df4e720ba34ab5937f73944aee76ba85f345706bdb1ec",
    "audits/CUBE_BIFURCATIONS_V04_DEV6_BLIND_B25_REVIEWER_REPORT.md":
        "bffd4948721ee62f6898336734670ee51381caf546cdd69e0a2ad810e37f165a",
    "audits/PAPER3_RC2_FINAL_BLIND_RELEASE_AUDIT.md":
        "37b0b4d68f4675b4546f7313aca6937c51cdf1ee11d1cc20b528918e636d7448",
}

CHANGEABLE = {
    "README.md": "documentation",
    "NOTES.md": "documentation (status lines only removed/replaced)",
    "CHANGELOG.md": "documentation (insert-only)",
    "RESEARCH_LOG.md": "documentation (append-only)",
    "audits/README.md": "audit index (insert-only)",
    "src/cube_bif/__init__.py": "version/status metadata only",
    "tests/test_docs.py": "documentation/status test",
    "SHA256SUMS": "regenerated integrity manifest",
}

HIST_RC1 = {
    "RELEASE_NOTES_RC1.md", "docs/QA_RESULTS_RC1.json", "docs/QA_RESULTS_RC1.md", "docs/V1.0.0-rc1_PRESERVATION_CHECK.md",
    "docs/V1.0.0-rc1_PRESERVATION_CONTROLS.json", "scripts/check_preservation_V1_0_0_rc1.py",
    "scripts/preservation_controls_V1_0_0_rc1.py",
}
HIST_RC2 = {
    "RELEASE_NOTES_RC2.md", "FINAL_AUDIT_INSTRUCTIONS.md", "docs/QA_RESULTS_RC2.json", "docs/QA_RESULTS_RC2.md",
    "docs/V1.0.0-rc2_PRESERVATION_CHECK.md", "docs/V1.0.0-rc2_PRESERVATION_CHECK.json",
    "docs/V1.0.0-rc2_PRESERVATION_CONTROLS.json", "docs/V1.0.0-rc2_TEXT_SCAN.md", "docs/V1.0.0-rc2_TEXT_SCAN.json",
    "scripts/check_preservation_V1_0_0_rc2.py", "scripts/preservation_controls_V1_0_0_rc2.py", "scripts/scan_text_rc2.py",
}

ALLOWED_ADDED_EXACT = {
    "LICENSE": "licence / copyright notice", "LICENSE-DOCS": "licence / copyright notice",
    "CITATION.cff": "release metadata", ".zenodo.json": "release metadata",
    "RELEASE_NOTES_V1.0.0.md": "release notes", "FINAL_V1_DELTA_AUDIT_INSTRUCTIONS.md": "release metadata",
    "AUTHOR_DECISION_V1.0.0.md": "approved human statements (author decision record)",
    "docs/AI_USE_LOG.md": "documentation", "docs/AUDIT_INDEX.md": "audit index/status",
    "docs/AUDIT_STATUS_MATRIX.json": "audit index/status", "docs/AUDIT_STATUS_MATRIX.md": "audit index/status",
    "docs/REPRODUCIBILITY.md": "documentation", "docs/REFERENCE_VERIFICATION.md": "documentation",
    "docs/THEOREM_DEPENDENCY_SUMMARY.md": "documentation", "docs/GITHUB_RELEASE_V1.0.0.md": "release metadata",
    "docs/V1.0.0_PRESERVATION_CHECK.md": "preservation report", "docs/V1.0.0_PRESERVATION_CHECK.json": "preservation report",
    "docs/V1.0.0_PRESERVATION_CONTROLS.json": "preservation control record",
    "docs/V1.0.0_TEXT_SCAN.md": "text-scan record", "docs/V1.0.0_TEXT_SCAN.json": "text-scan record",
    "docs/QA_RESULTS_V1.0.0.md": "QA record", "docs/QA_RESULTS_V1.0.0.json": "QA record",
    "scripts/check_preservation_V1_0_0.py": "release tooling", "scripts/preservation_controls_V1_0_0.py": "release tooling",
    "scripts/check_release_text.py": "release tooling", "scripts/scan_text_v1.py": "release tooling",
    "scripts/validate_dependency_graphs.py": "release tooling (read-only proof-graph validator)",
    "tests/test_release_v1.py": "test of release metadata",
}
ALLOWED_ADDED_EXACT.update({k: "historical RC1 record" for k in HIST_RC1})
ALLOWED_ADDED_EXACT.update({k: "historical RC2 record" for k in HIST_RC2})
ALLOWED_ADDED_PREFIX = {"paper/": "manuscript", "submission/": "submission material"}

# against RC2
PAPER_CHANGEABLE = {
    "paper/manuscript.tex": "manuscript front matter (version line) and PDF document properties",
    "paper/macros.tex": "manuscript: controlled placeholder text",
    "paper/references.bib": "manuscript: self-reference note (Repo3)",
    "paper/sections/12_reproducibility.tex": "manuscript: release wording",
    "paper/sections/13_declarations.tex": "approved human statements (declarations)",
}
REMOVABLE_VS_RC2 = {
    "AUTHORSHIP_FINAL_APPROVAL_REQUIRED.md": "approval-hold record superseded by AUTHOR_DECISION_V1.0.0.md (kept in RC2)",
    "submission/DECLARATIONS_DRAFT.md": "draft superseded by submission/DECLARATIONS.md (kept in RC2)",
    "tests/test_release_rc2.py": "release test superseded by tests/test_release_v1.py (kept in RC2)",
}
CLASS_VS_RC2 = {
    "README.md": "documentation / status strings", "NOTES.md": "documentation / status strings (§17 added)",
    "CHANGELOG.md": "documentation (insert-only)", "RESEARCH_LOG.md": "documentation (append-only)",
    "audits/README.md": "audit index/status (insert-only)", "src/cube_bif/__init__.py": "version/status metadata",
    "SHA256SUMS": "checksums", "tests/test_docs.py": "test of release metadata",
    "tests/test_release_v1.py": "test of release metadata",
    "CITATION.cff": "release metadata (version; approved licence/copyright text)",
    ".zenodo.json": "release metadata (version; approved licence/copyright text)",
    "LICENSE": "copyright notice metadata (approved wording)", "LICENSE-DOCS": "copyright notice metadata (approved wording)",
    "AUTHOR_DECISION_V1.0.0.md": "approved human statements (author decision record)",
    "audits/PAPER3_RC2_FINAL_BLIND_RELEASE_AUDIT.md": "final audit report (verbatim)",
    "RELEASE_NOTES_V1.0.0.md": "release notes", "FINAL_V1_DELTA_AUDIT_INSTRUCTIONS.md": "release notes / audit handoff",
    "docs/AUDIT_INDEX.md": "audit index/status", "docs/AUDIT_STATUS_MATRIX.md": "audit index/status",
    "docs/AUDIT_STATUS_MATRIX.json": "audit index/status",
}
STATUS_TOKENS = ("audit", "status", "pending", "not_provided")


def sha(b):
    return hashlib.sha256(b).hexdigest()


def load_zip(zpath, expect):
    raw = pathlib.Path(zpath).read_bytes()
    if sha(raw) != expect:
        raise SystemExit(f"archive hash {sha(raw)} != {expect}")
    out = {}
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        for n in z.namelist():
            if n.endswith("/"):
                continue
            assert n.startswith(PREFIX), n
            out[n[len(PREFIX):]] = z.read(n)
    return out


def load_tree(root):
    root = pathlib.Path(root)
    out = {}
    for p in sorted(root.rglob("*")):
        if p.is_dir():
            continue
        rel = p.relative_to(root).as_posix()
        if "__pycache__" in rel or rel.startswith(".pytest_cache") or rel.endswith(".pyc"):
            continue
        out[rel] = p.read_bytes()
    return out


def _status_paragraph_lines(lines):
    """Indices of every status block: a line starting with '**Status' and its continuation lines, up to the next blank
    line or list item."""
    out = set()
    for i, l in enumerate(lines):
        if l.lstrip().startswith("**Status"):
            k = i
            while k < len(lines) and lines[k].strip() and (k == i or not lines[k].lstrip().startswith("- ")):
                out.add(k); k += 1
    return out


def rule_notes(old, new):
    ol, nl = old.decode().split("\n"), new.decode().split("\n")
    status_par = _status_paragraph_lines(ol)
    bad = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, ol, nl, autojunk=False).get_opcodes():
        if tag in ("replace", "delete"):
            bad += [ol[k][:120] for k in range(i1, i2)
                    if k not in status_par and not any(t in ol[k].lower() for t in STATUS_TOKENS)]
    return (not bad), (f"{len(bad)} non-status line(s) removed or edited, first: {bad[0]!r}" if bad else
                       "only status lines removed/replaced; additions allowed")


def rule_insert_block(old, new):
    o, n = old.decode(), new.decode()
    if len(n) < len(o):
        return False, "shorter than the reference"
    k = 0
    while k < len(o) and o[k] == n[k]:
        k += 1
    ok = n.endswith(o[k:]) and n[:k] == o[:k]
    return ok, "one contiguous inserted block" if ok else "reference text not recovered by removing one inserted block"


def rule_append(old, new):
    ok = new.startswith(old)
    return ok, "reference file is a byte prefix (append-only)" if ok else "not append-only"


def rule_subsequence(old, new):
    ol, nl = old.decode().split("\n"), new.decode().split("\n")
    it = iter(nl)
    ok = all(any(l == m for m in it) for l in ol)
    return ok, "every reference line kept in order (insert-only)" if ok else "a reference line was removed or edited"


def _mask_init(src):
    tree = ast.parse(src)
    lines = src.split("\n")
    drop = set()
    for node in tree.body:
        if isinstance(node, ast.Expr) and isinstance(getattr(node, "value", None), ast.Constant) and \
                isinstance(node.value.value, str):
            drop.update(range(node.lineno - 1, node.end_lineno))
    out = []
    for i, l in enumerate(lines):
        if i in drop:
            continue
        out.append(re.sub(r'^(__version__|STATUS)\s*=\s*".*"$', r'\1 = <masked>', l))
    return "\n".join(out).strip()


def rule_init(old, new):
    ok = _mask_init(old.decode()) == _mask_init(new.decode())
    return ok, "identical apart from docstring, __version__ and STATUS" if ok else "code beyond version/status changed"


def rule_free(old, new):
    return True, "documentation"


def rule_readme(old, new):
    title = "**Symmetry-Breaking Bifurcations from the Cubic Equilibrium in Two-Term Inverse-Power Clusters**"
    ok = title in new.decode()
    return ok, "documentation; paper title kept" if ok else "paper title missing"


def rule_manifest(new_manifest, tree):
    want = {}
    for line in new_manifest.decode().splitlines():
        if not line.strip():
            continue
        h, name = line.split(None, 1)
        name = name.lstrip("*")
        if name.startswith("./"):
            name = name[2:]
        want[name] = h
    files = {k: sha(v) for k, v in tree.items() if k != "SHA256SUMS"}
    if want == files:
        return True, f"matches the tree ({len(files)} entries)"
    missing = sorted(set(files) - set(want))[:3]
    extra = sorted(set(want) - set(files))[:3]
    wrong = sorted(k for k in set(want) & set(files) if want[k] != files[k])[:3]
    return False, f"stale manifest: missing {missing}, extra {extra}, wrong {wrong}"


RULES = {"README.md": rule_readme, "NOTES.md": rule_notes, "CHANGELOG.md": rule_insert_block,
         "RESEARCH_LOG.md": rule_append, "audits/README.md": rule_subsequence, "src/cube_bif/__init__.py": rule_init,
         "tests/test_docs.py": rule_free}
RULES_VS_RC2 = {"NOTES.md": rule_notes, "CHANGELOG.md": rule_insert_block, "RESEARCH_LOG.md": rule_append,
                "audits/README.md": rule_subsequence, "src/cube_bif/__init__.py": rule_init}

KEY_ARTIFACTS = [
    ("Track A certificate (Lemma M)", "data/A2_lemma_M_certificate.json"),
    ("Track A semantic hash", "data/A2_CERTIFICATE_SEMANTIC.sha256"),
    ("Theorem A dependency graph", "data/A2_theorem_A_dependencies.json"),
    ("historical B1 certificate (Lemma K)", "data/B1_kappa_certificate.json"),
    ("historical B1 semantic hash", "data/B1_CERTIFICATE_SEMANTIC.sha256"),
    ("B1 erratum: corrected rebuild", "data/B1_ERRATUM_corrected_rebuild_certificate.json"),
    ("B1 erratum: corrected rebuild semantic hash", "data/B1_ERRATUM_CORRECTED_REBUILD_SEMANTIC.sha256"),
    ("B1 erratum: report", "data/B1_ERRATUM_report.json"),
    ("B1 erratum: pre-patch reproduction", "data/B1_ERRATUM_pre_patch_reproduction.json"),
    ("B2.3 certificate (Lemma Q)", "data/B2_c4hat_certificate.json"),
    ("B2.3 semantic hash", "data/B2_CERTIFICATE_SEMANTIC.sha256"),
    ("B2.3 checker report", "data/B2_3_check_report.json"),
    ("B2.4 branch record", "data/B2_4_branch.json"),
    ("B2.4 dependency graph", "data/B2_4_dependency_graph.json"),
    ("B2.5 index record", "data/B2_5_index.json"),
    ("B2.5 dependency graph", "data/B2_5_dependency_graph.json"),
    ("Track A audit report", "audits/CUBE_BIFURCATIONS_REVIEWER_REPORT.md"),
    ("B1 audit report", "audits/CUBE_BIFURCATIONS_V03_REVIEWER_REPORT.md"),
    ("erratum E-B1 re-audit report", "audits/CUBE_BIFURCATIONS_V04_DEV4_B1_ERRATUM_REAUDIT.md"),
]


def classify_added(rel):
    if rel in NEW_AUDITS:
        return "audit report added since V0.4-dev.6 (byte-identical)"
    if rel in ALLOWED_ADDED_EXACT:
        return ALLOWED_ADDED_EXACT[rel]
    for pre, kind in ALLOWED_ADDED_PREFIX.items():
        if rel.startswith(pre):
            if pre == "paper/" and re.search(r"\.(aux|log|fls|fdb_latexmk|blg|out|synctex\.gz|pdf)$", rel) and \
                    not rel.startswith("paper/figures/"):
                return None
            return kind
    return None


def check(baseline_zip, root):
    old, new = load_zip(baseline_zip, BASELINE_SHA256), load_tree(root)
    rows, failures = [], []
    for rel in sorted(set(old) | set(new)):
        if rel in old and rel not in new:
            rows.append((rel, "REMOVED", "forbidden")); failures.append(f"removed: {rel}")
            continue
        if rel not in old:
            kind = classify_added(rel)
            if kind is None:
                rows.append((rel, "ADDED", "forbidden location")); failures.append(f"added in forbidden location: {rel}")
            elif rel in NEW_AUDITS and sha(new[rel]) != NEW_AUDITS[rel]:
                rows.append((rel, "ADDED", "audit report hash mismatch")); failures.append(f"audit report altered: {rel}")
            else:
                rows.append((rel, "ADDED", kind))
            continue
        if old[rel] == new[rel]:
            rows.append((rel, "IDENTICAL", ""))
            continue
        if rel == "SHA256SUMS":
            ok, why = rule_manifest(new[rel], new)
        elif rel in RULES:
            ok, why = RULES[rel](old[rel], new[rel])
        else:
            ok, why = False, "protected file changed"
        rows.append((rel, "CHANGED" if ok else "CHANGED (FORBIDDEN)", f"{CHANGEABLE.get(rel, 'protected')}: {why}"))
        if not ok:
            failures.append(f"{rel}: {why}")
    keys = []
    for label, rel in KEY_ARTIFACTS:
        same = rel in old and rel in new and old[rel] == new[rel]
        keys.append((label, rel, same, sha(new[rel]) if rel in new else None))
        if not same:
            failures.append(f"key artefact not byte-identical: {rel}")
    src_changed = [r for r, s, _ in rows if r.startswith("src/") and s != "IDENTICAL"]
    math_src_changed = [r for r in src_changed if r != "src/cube_bif/__init__.py"]
    data_changed = [r for r, s, _ in rows if r.startswith("data/") and s != "IDENTICAL"]
    counts = {}
    for _, s, _ in rows:
        counts[s] = counts.get(s, 0) + 1
    return {"pass": not failures, "failures": failures, "counts": counts, "rows": rows, "key_artifacts": keys,
            "mathematical_source_changed": math_src_changed, "data_changed": data_changed,
            "baseline_sha256": BASELINE_SHA256}


def classify_vs_rc2(rel, state):
    if state == "REMOVED":
        return REMOVABLE_VS_RC2.get(rel)
    if rel.startswith(("data/", "reference/")) or (rel.startswith("src/") and rel != "src/cube_bif/__init__.py"):
        return None
    if rel in HIST_RC1 or rel in HIST_RC2:
        return None
    if rel.startswith("audits/"):
        if rel == "audits/README.md":
            return CLASS_VS_RC2[rel]
        return CLASS_VS_RC2.get(rel) if state == "ADDED" else None
    if rel.startswith("paper/"):
        return PAPER_CHANGEABLE.get(rel)
    if rel.startswith("submission/"):
        return "submission material (approved statements / metadata / cover letter)"
    if rel.startswith("tests/"):
        return CLASS_VS_RC2.get(rel)
    if rel.startswith("scripts/"):
        return ALLOWED_ADDED_EXACT.get(rel) if ALLOWED_ADDED_EXACT.get(rel) == "release tooling" else None
    if rel in CLASS_VS_RC2:
        return CLASS_VS_RC2[rel]
    if rel.startswith("docs/"):
        k = ALLOWED_ADDED_EXACT.get(rel)
        return k if k and not k.startswith("historical") else None
    return None


def compare_rc2(rc2_zip, new):
    old = load_zip(rc2_zip, RC2_SHA256)
    rows, failures = [], []
    for rel in sorted(set(old) | set(new)):
        if old.get(rel) == new.get(rel):
            continue
        state = "REMOVED" if rel not in new else "ADDED" if rel not in old else "CHANGED"
        kind = classify_vs_rc2(rel, state)
        if kind and rel in NEW_AUDITS and state == "ADDED" and sha(new[rel]) != NEW_AUDITS[rel]:
            kind = None
        why = ""
        if kind and state == "CHANGED" and rel in RULES_VS_RC2:
            ok, why = RULES_VS_RC2[rel](old[rel], new[rel])
            if not ok:
                kind = None
        if kind and rel == "SHA256SUMS":
            ok, why = rule_manifest(new[rel], new)
            if not ok:
                kind = None
        rows.append((rel, state, (kind + (f" — {why}" if why else "")) if kind else "FORBIDDEN" + (f" — {why}" if why else "")))
        if kind is None:
            failures.append(f"vs RC2: {state.lower()} {rel}" + (f" ({why})" if why else ""))
    identical = sum(1 for rel in set(old) & set(new) if old[rel] == new[rel])
    groups = {"src (excluding __init__.py)": "src/", "data": "data/", "audits (excluding README.md)": "audits/",
              "reference": "reference/", "paper/figures": "paper/figures/", "paper/appendices": "paper/appendices/"}
    group_identity = {}
    for g, pre in groups.items():
        files = [r for r in old if r.startswith(pre) and r not in ("src/cube_bif/__init__.py", "audits/README.md")]
        group_identity[g] = {"files": len(files), "byte_identical": sum(1 for r in files if new.get(r) == old[r])}
    sections = [r for r in old if r.startswith("paper/sections/") and r not in PAPER_CHANGEABLE]
    group_identity["paper/sections (scientific sections 01-11)"] = {
        "files": len(sections), "byte_identical": sum(1 for r in sections if new.get(r) == old[r])}
    return {"rc2_sha256": RC2_SHA256, "rows": rows, "failures": failures, "identical": identical,
            "group_identity": group_identity}


def report_md(res):
    L = ["# V1.0.0 mechanical preservation check (against V0.4-dev.6 and V1.0.0-rc2)", "",
         f"Baseline archive: `EIT_LJ_CUBE_BIFURCATIONS_V0.4-dev.6.zip`, SHA-256 `{res['baseline_sha256']}`.",
         "Generated by `scripts/check_preservation_V1_0_0.py`; forbidden-edit controls by "
         "`scripts/preservation_controls_V1_0_0.py` (record `docs/V1.0.0_PRESERVATION_CONTROLS.json`).", "",
         f"**Result: {'PASS' if res['pass'] else 'FAIL'}.** Against V0.4-dev.6: " +
         ", ".join(f"{k} {v}" for k, v in sorted(res["counts"].items())) + ".",
         f"Mathematical source files changed (V0.4-dev.6 → V1.0.0): {len(res['mathematical_source_changed'])}; "
         f"data files changed: {len(res['data_changed'])}.", ""]
    if res["failures"]:
        L += ["## Failures", ""] + [f"- {f}" for f in res["failures"]] + [""]
    L += ["## Part 1 — key artefacts (byte-identical with V0.4-dev.6)", "",
          "| artefact | file | identical | SHA-256 |", "|---|---|---|---|"]
    for label, rel, same, h in res["key_artifacts"]:
        L.append(f"| {label} | `{rel}` | {'yes' if same else 'NO'} | `{h}` |")
    L += ["", "## Part 1 — files changed or added since V0.4-dev.6", "", "| file | change | classification |",
          "|---|---|---|"]
    for rel, s, why in res["rows"]:
        if s != "IDENTICAL":
            L.append(f"| `{rel}` | {s} | {why} |")
    n_id = sum(1 for _, s, _ in res["rows"] if s == "IDENTICAL")
    L += ["", f"All other {n_id} files of V0.4-dev.6 are byte-identical (every mathematical source module, "
          "certificate, proof record, dependency graph, numerical record, earlier script, test file other than "
          "`tests/test_docs.py`, earlier audit report and earlier identity-check document).", ""]
    if "vs_rc2" in res:
        v = res["vs_rc2"]
        L += ["## Part 2 — every difference against V1.0.0-rc2 (SHA-256 `" + v["rc2_sha256"] + "`)", "",
              f"{v['identical']} files are byte-identical with RC2. Byte-identity of protected groups:", "",
              "| group | files in RC2 | byte-identical in V1.0.0 |", "|---|---|---|"]
        for g, x in v["group_identity"].items():
            L.append(f"| {g} | {x['files']} | {x['byte_identical']} |")
        L += ["", "| file | change vs RC2 | classification |", "|---|---|---|"]
        for rel, s, why in v["rows"]:
            L.append(f"| `{rel}` | {s} | {why} |")
        L.append("")
    return "\n".join(L)


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    opts = dict(a.split("=", 1) for a in argv[1:] if a.startswith("--") and "=" in a)
    if not args:
        print(__doc__); return 2
    root = args[1] if len(args) > 1 else str(pathlib.Path(__file__).resolve().parents[1])
    res = check(args[0], root)
    if "--rc2" in opts:
        res["vs_rc2"] = compare_rc2(opts["--rc2"], load_tree(root))
        res["failures"] = res["failures"] + res["vs_rc2"]["failures"]
        res["pass"] = not res["failures"]
    if "--report" in opts:
        pathlib.Path(opts["--report"]).write_text(report_md(res))
    if "--json" in opts:
        j = dict(res); j["rows"] = [list(r) for r in res["rows"]]; j["key_artifacts"] = [list(k) for k in res["key_artifacts"]]
        if "vs_rc2" in j:
            j["vs_rc2"] = {**j["vs_rc2"], "rows": [list(r) for r in j["vs_rc2"]["rows"]]}
        pathlib.Path(opts["--json"]).write_text(json.dumps(j, indent=2))
    print("PASS" if res["pass"] else "FAIL", res["counts"], "vs RC2 differences:",
          len(res["vs_rc2"]["rows"]) if "vs_rc2" in res else "not checked")
    for f in res["failures"]:
        print("  -", f)
    return 0 if res["pass"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
