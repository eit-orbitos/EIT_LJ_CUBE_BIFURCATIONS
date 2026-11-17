"""Mechanical preservation check: V1.0.0-rc2 against the audited V0.4-dev.6 archive.

Usage:  python scripts/check_preservation_V1_0_0_rc2.py <EIT_LJ_CUBE_BIFURCATIONS_V0.4-dev.6.zip> [project root]
        [--report docs/V1.0.0-rc2_PRESERVATION_CHECK.md] [--json <path>]

Rules (anything not allowed is a FAILURE):
- The baseline archive must have SHA-256 c473af60...b691.
- No file of V0.4-dev.6 may be removed.
- Every V0.4-dev.6 file is byte-identical, except the files in CHANGEABLE, each under its own rule:
    README.md                 documentation (free text; must keep the title line of the paper)
    NOTES.md                  documentation; every removed or replaced V0.4-dev.6 line must be a status line
                              (contains "audit", "status", "pending" or "not_provided", case-insensitive); lines may be
                              added anywhere. So no formula, statement or derivation line can be removed or edited.
    CHANGELOG.md              insert-only: the V0.4-dev.6 file is recovered by deleting one contiguous inserted block
    RESEARCH_LOG.md           append-only: the V0.4-dev.6 file is a byte prefix
    audits/README.md          insert-only: every V0.4-dev.6 line is kept, in order
    src/cube_bif/__init__.py  version/status metadata only: identical after masking the module docstring and the
                              values of __version__ and STATUS; no other line may change
    tests/test_docs.py        documentation/status test (the only test file allowed to change)
    SHA256SUMS                regenerated; must match the release-candidate tree exactly
- Added files only under ALLOWED_ADDED (documentation, manuscript, submission drafts, release metadata, the three new
  audit reports with their exact hashes, the release tooling and its test). Nothing may be added under src/ or data/.
- Optional --rc1=<V1.0.0-rc1 zip>: authenticate RC1 (SHA-256 33095d35...361b), require the historical RC1 records and
  every src/, data/ and audits/ file to be byte-identical with RC1, and list every file changed, added or removed
  relative to RC1 with its classification.
"""
import ast
import hashlib
import io
import json
import pathlib
import re
import sys
import zipfile

BASELINE_SHA256 = "c473af60f8b54c0beecd252d9e8409eef734ba475c0d693b300946f57941b691"
PREFIX = "EIT_LJ_CUBE_BIFURCATIONS/"

NEW_AUDITS = {
    "audits/CUBE_BIFURCATIONS_V05_BLIND_B23_LEMMA_Q_REVIEWER_REPORT.md":
        "841152f2cccd0a43c4f8e73ce5d0cf37e9793d26f12047d5143ea5a053e96bcf",
    "audits/CUBE_BIFURCATIONS_V05_BLIND_B24_REVIEWER_REPORT.md":
        "0302930b9a96ac6bca3df4e720ba34ab5937f73944aee76ba85f345706bdb1ec",
    "audits/CUBE_BIFURCATIONS_V04_DEV6_BLIND_B25_REVIEWER_REPORT.md":
        "bffd4948721ee62f6898336734670ee51381caf546cdd69e0a2ad810e37f165a",
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

ALLOWED_ADDED_EXACT = {
    "LICENSE": "licence", "LICENSE-DOCS": "licence", "CITATION.cff": "release metadata",
    ".zenodo.json": "release metadata", "RELEASE_NOTES_RC2.md": "release notes",
    "FINAL_AUDIT_INSTRUCTIONS.md": "release metadata",
    "AUTHORSHIP_FINAL_APPROVAL_REQUIRED.md": "authorship / declarations",
    "docs/AI_USE_LOG.md": "documentation", "docs/AUDIT_INDEX.md": "documentation",
    "docs/AUDIT_STATUS_MATRIX.json": "audit-status record", "docs/AUDIT_STATUS_MATRIX.md": "audit-status record",
    "docs/REPRODUCIBILITY.md": "documentation",
    "docs/REFERENCE_VERIFICATION.md": "documentation", "docs/THEOREM_DEPENDENCY_SUMMARY.md": "documentation",
    "docs/V1.0.0-rc2_PRESERVATION_CHECK.md": "preservation report",
    "docs/V1.0.0-rc2_PRESERVATION_CHECK.json": "preservation report",
    "docs/V1.0.0-rc2_PRESERVATION_CONTROLS.json": "preservation control record",
    "docs/V1.0.0-rc2_TEXT_SCAN.md": "text-scan record", "docs/V1.0.0-rc2_TEXT_SCAN.json": "text-scan record",
    "docs/QA_RESULTS_RC2.json": "QA record", "docs/QA_RESULTS_RC2.md": "QA record",
    "scripts/check_preservation_V1_0_0_rc2.py": "release tooling",
    "scripts/preservation_controls_V1_0_0_rc2.py": "release tooling",
    "scripts/check_release_text.py": "release tooling", "scripts/scan_text_rc2.py": "release tooling",
    "scripts/validate_dependency_graphs.py": "release tooling (read-only proof-graph validator)",
    "tests/test_release_rc2.py": "test of release metadata",
    # historical V1.0.0-rc1 records, kept byte-identical with RC1 (verified when --rc1=<zip> is given)
    "RELEASE_NOTES_RC1.md": "historical RC1 record", "docs/QA_RESULTS_RC1.json": "historical RC1 record",
    "docs/QA_RESULTS_RC1.md": "historical RC1 record",
    "docs/V1.0.0-rc1_PRESERVATION_CHECK.md": "historical RC1 record",
    "docs/V1.0.0-rc1_PRESERVATION_CONTROLS.json": "historical RC1 record",
    "scripts/check_preservation_V1_0_0_rc1.py": "historical RC1 record",
    "scripts/preservation_controls_V1_0_0_rc1.py": "historical RC1 record",
}
RC1_HISTORICAL = sorted(k for k, v in ALLOWED_ADDED_EXACT.items() if v == "historical RC1 record")
RC1_SHA256 = "33095d35107578054c7e54ff62be8a318ab973d7153e5c30d89da2fc9bc0361b"
ALLOWED_ADDED_PREFIX = {"paper/": "manuscript", "submission/": "submission draft"}

STATUS_TOKENS = ("audit", "status", "pending", "not_provided")


def sha(b):
    return hashlib.sha256(b).hexdigest()


def load_baseline(zpath):
    raw = pathlib.Path(zpath).read_bytes()
    if sha(raw) != BASELINE_SHA256:
        raise SystemExit(f"baseline archive hash {sha(raw)} != {BASELINE_SHA256}")
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


def rule_notes(old, new):
    ol, nl = old.decode().split("\n"), new.decode().split("\n")
    import difflib
    bad = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, ol, nl, autojunk=False).get_opcodes():
        if tag in ("replace", "delete"):
            for line in ol[i1:i2]:
                if not any(t in line.lower() for t in STATUS_TOKENS):
                    bad.append(line[:120])
    return (not bad), (f"{len(bad)} non-status line(s) removed or edited, first: {bad[0]!r}" if bad else
                       "only status lines removed/replaced; additions allowed")


def rule_insert_block(old, new):
    o, n = old.decode(), new.decode()
    if len(n) < len(o):
        return False, "shorter than V0.4-dev.6"
    k = 0
    while k < len(o) and o[k] == n[k]:
        k += 1
    ok = n.endswith(o[k:]) and len(n) - len(o) >= 0 and n[:k] == o[:k]
    return ok, "one contiguous inserted block" if ok else "V0.4-dev.6 text not recovered by removing one inserted block"


def rule_append(old, new):
    ok = new.startswith(old)
    return ok, "V0.4-dev.6 file is a byte prefix (append-only)" if ok else "not append-only"


def rule_subsequence(old, new):
    ol, nl = old.decode().split("\n"), new.decode().split("\n")
    it = iter(nl)
    ok = all(any(l == m for m in it) for l in ol)
    return ok, "every V0.4-dev.6 line kept in order (insert-only)" if ok else "a V0.4-dev.6 line was removed or edited"


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
        l = re.sub(r'^(__version__|STATUS)\s*=\s*".*"$', r'\1 = <masked>', l)
        out.append(l)
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
    ok = want == files
    if ok:
        return True, f"matches the release-candidate tree ({len(files)} entries)"
    missing = sorted(set(files) - set(want))[:3]
    extra = sorted(set(want) - set(files))[:3]
    wrong = sorted(k for k in set(want) & set(files) if want[k] != files[k])[:3]
    return False, f"stale manifest: missing {missing}, extra {extra}, wrong {wrong}"


RULES = {"README.md": rule_readme, "NOTES.md": rule_notes, "CHANGELOG.md": rule_insert_block,
         "RESEARCH_LOG.md": rule_append, "audits/README.md": rule_subsequence, "src/cube_bif/__init__.py": rule_init,
         "tests/test_docs.py": rule_free}

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
        return "new audit report (byte-identical)"
    if rel in ALLOWED_ADDED_EXACT:
        return ALLOWED_ADDED_EXACT[rel]
    for pre, kind in ALLOWED_ADDED_PREFIX.items():
        if rel.startswith(pre):
            if pre == "paper/" and re.search(r"\.(aux|log|fls|fdb_latexmk|blg|out|synctex\.gz)$", rel):
                return None
            return kind
    return None


def check(baseline_zip, root):
    old, new = load_baseline(baseline_zip), load_tree(root)
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
    if "SHA256SUMS" in new and old.get("SHA256SUMS") == new.get("SHA256SUMS"):
        ok, why = rule_manifest(new["SHA256SUMS"], new)
        if not ok:
            failures.append(f"SHA256SUMS: {why}")
    keys = []
    for label, rel in KEY_ARTIFACTS:
        same = rel in old and rel in new and old[rel] == new[rel]
        keys.append((label, rel, same, sha(new[rel]) if rel in new else None))
        if not same:
            failures.append(f"key artefact not byte-identical: {rel}")
    src_changed = [r for r, s, _ in rows if r.startswith("src/") and s != "IDENTICAL"]
    math_src_changed = [r for r in src_changed if r != "src/cube_bif/__init__.py"]
    counts = {}
    for _, s, _ in rows:
        counts[s] = counts.get(s, 0) + 1
    return {"pass": not failures, "failures": failures, "counts": counts, "rows": rows, "key_artifacts": keys,
            "mathematical_source_changed": math_src_changed, "baseline_sha256": BASELINE_SHA256}


def classify_vs_rc1(rel):
    if rel.startswith("paper/"):
        return "manuscript"
    if rel.startswith("submission/"):
        return "submission draft (declarations/metadata)"
    if rel in ("README.md", "NOTES.md", "CHANGELOG.md", "RESEARCH_LOG.md"):
        return "documentation / status strings"
    if rel == "src/cube_bif/__init__.py":
        return "version/status metadata"
    if rel == "SHA256SUMS":
        return "checksums"
    if rel in ("tests/test_docs.py", "tests/test_release_rc1.py", "tests/test_release_rc2.py"):
        return "test of release metadata"
    if rel in ("CITATION.cff", ".zenodo.json", "LICENSE", "LICENSE-DOCS"):
        return "release metadata / authorship / affiliation"
    if rel in ("AUTHORSHIP_FINAL_APPROVAL_REQUIRED.md", "docs/AUTHOR_CONTRIBUTIONS_REVIEW_REQUIRED.md"):
        return "authorship / declarations"
    if rel.startswith("scripts/"):
        return "release tooling"
    if rel.startswith("docs/") or rel in ("RELEASE_NOTES_RC2.md", "FINAL_AUDIT_INSTRUCTIONS.md"):
        return "documentation / release records"
    return None


def compare_rc1(rc1_zip, new):
    raw = pathlib.Path(rc1_zip).read_bytes()
    if sha(raw) != RC1_SHA256:
        raise SystemExit(f"RC1 archive hash {sha(raw)} != {RC1_SHA256}")
    old = {}
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        for n in z.namelist():
            if not n.endswith("/"):
                old[n[len(PREFIX):]] = z.read(n)
    rows, failures = [], []
    for rel in sorted(set(old) | set(new)):
        if old.get(rel) == new.get(rel):
            continue
        state = "REMOVED" if rel not in new else "ADDED" if rel not in old else "CHANGED"
        kind = classify_vs_rc1(rel)
        if rel.startswith(("src/", "data/", "audits/")) and rel != "src/cube_bif/__init__.py":
            kind = None
        if rel in RC1_HISTORICAL:
            kind = None
        rows.append((rel, state, kind or "FORBIDDEN"))
        if kind is None:
            failures.append(f"vs RC1: {state.lower()} {rel}")
    return rows, failures


def report_md(res):
    L = ["# V1.0.0-rc2 mechanical preservation check (against V0.4-dev.6)", "",
         f"Baseline archive: `EIT_LJ_CUBE_BIFURCATIONS_V0.4-dev.6.zip`, SHA-256 `{res['baseline_sha256']}`.",
         "Generated by `scripts/check_preservation_V1_0_0_rc2.py`; forbidden-edit controls by "
         "`scripts/preservation_controls_V1_0_0_rc2.py` (record `docs/V1.0.0-rc2_PRESERVATION_CONTROLS.json`).", "",
         f"**Result: {'PASS' if res['pass'] else 'FAIL'}.** Counts: " +
         ", ".join(f"{k} {v}" for k, v in sorted(res["counts"].items())) + ".",
         f"Mathematical source files changed: {len(res['mathematical_source_changed'])}"
         + (f" ({', '.join(res['mathematical_source_changed'])})" if res['mathematical_source_changed'] else "") + ".",
         ""]
    if res["failures"]:
        L += ["## Failures", ""] + [f"- {f}" for f in res["failures"]] + [""]
    L += ["## Key artefacts (must be byte-identical)", "", "| artefact | file | identical | SHA-256 |", "|---|---|---|---|"]
    for label, rel, same, h in res["key_artifacts"]:
        L.append(f"| {label} | `{rel}` | {'yes' if same else 'NO'} | `{h}` |")
    L += ["", "## Changed and added files", "", "| file | change | classification |", "|---|---|---|"]
    for rel, s, why in res["rows"]:
        if s != "IDENTICAL":
            L.append(f"| `{rel}` | {s} | {why} |")
    if "vs_rc1" in res:
        L += ["", "## Differences against V1.0.0-rc1 (SHA-256 `" + res["vs_rc1"]["rc1_sha256"] + "`)", "",
              "Every file not listed is byte-identical with RC1 (including every `src/`, `data/` and `audits/` file and the "
              "historical RC1 records).", "", "| file | change vs RC1 | classification |", "|---|---|---|"]
        for rel, s, why in res["vs_rc1"]["rows"]:
            L.append(f"| `{rel}` | {s} | {why} |")
    n_id = sum(1 for _, s, _ in res["rows"] if s == "IDENTICAL")
    L += ["", f"All other {n_id} files of V0.4-dev.6 are byte-identical (every mathematical source module, "
          "certificate, proof record, dependency graph, numerical record, earlier script, test file other than "
          "`tests/test_docs.py`, earlier audit report and earlier identity-check document).", ""]
    return "\n".join(L)


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    opts = dict(a.split("=", 1) for a in argv[1:] if a.startswith("--") and "=" in a)
    if not args:
        print(__doc__); return 2
    root = args[1] if len(args) > 1 else str(pathlib.Path(__file__).resolve().parents[1])
    res = check(args[0], root)
    if "--rc1" in opts:
        rows, fails = compare_rc1(opts["--rc1"], load_tree(root))
        res["vs_rc1"] = {"rc1_sha256": RC1_SHA256, "rows": rows, "failures": fails}
        res["failures"] = res["failures"] + fails
        res["pass"] = not res["failures"]
    if "--report" in opts:
        pathlib.Path(opts["--report"]).write_text(report_md(res))
    if "--json" in opts:
        j = dict(res); j["rows"] = [list(r) for r in res["rows"]]; j["key_artifacts"] = [list(k) for k in res["key_artifacts"]]
        if "vs_rc1" in j:
            j["vs_rc1"] = {**j["vs_rc1"], "rows": [list(r) for r in j["vs_rc1"]["rows"]]}
        pathlib.Path(opts["--json"]).write_text(json.dumps(j, indent=2))
    print("PASS" if res["pass"] else "FAIL", res["counts"])
    for f in res["failures"]:
        print("  -", f)
    return 0 if res["pass"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
