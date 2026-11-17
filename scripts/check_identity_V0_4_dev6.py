"""Mechanical identity check: V0.4-dev.6 (Phase B2.5) against V0.4-dev.5.

Usage: python scripts/check_identity_V0_4_dev6.py <EIT_LJ_CUBE_BIFURCATIONS_V0.4-dev.5.zip> [<dev.6 project root>]
          [--report docs/V0.4-dev.6_IDENTITY_CHECK.md]

Every V0.4-dev.5 file must be byte-identical in V0.4-dev.6, except for the allowed changes below; each allowed change
is checked by its own rule, not merely listed:
- src/cube_bif/__init__.py: module docstring and the values of __version__ and STATUS only (0.4.0.dev6,
  "RESEARCH / V0.4-dev.6").
- tests/test_docs.py: the status test, the proved-status test and the B2.4 claim-boundary test are replaced by their
  dev.6 versions and one test (B2.5 claim boundary) is added; every other unit is identical, in the same order.
- NOTES.md: every section from "## 1." up to "## 13." (§1–§12) byte-identical; the header, §0 and the new §13
  (B2.5) and §14 (next steps) are documentation.
- CHANGELOG.md: earlier entries verbatim, a new "## V0.4-dev.6" entry on top.
- RESEARCH_LOG.md: append-only.
- README.md: documentation (free).
- added files: an explicit list (the B2.5 module, tests, scripts and records; this checker, its controls and report).
- SHA256SUMS: regenerated; it must list exactly the files of the tree with their current hashes.
Anything else (a changed, deleted or unexpected file) fails the check. In particular Paper 2's inputs, Track A, B0, B1
(code, formulas, the historical certificate and the erratum artefacts), B2.0-B2.4 (code, certificate, records,
dependency graphs), every audit report and audits/README.md, and every earlier script, record and identity report
must be byte-identical.

The generic helpers (zip/tree loading, unit comparison, manifest check) are imported unchanged from
scripts/check_identity_V0_4_dev4.py, which stays byte-identical.
"""
import ast
import io
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import check_identity_V0_4_dev4 as base  # noqa: E402

sha, load_zip, load_tree, compare_units, check_manifest = (base.sha, base.load_zip, base.load_tree,
                                                           base.compare_units, base.check_manifest)

REPORT = "docs/V0.4-dev.6_IDENTITY_CHECK.md"
ADDED = {
    "src/cube_bif/b2_index.py": "added (B2.5: exact layer, statements, dependency graph, numerics)",
    "tests/test_B2_index.py": "added (B2.5 tests and statement/graph negative controls)",
    "scripts/run_B2_5.py": "added (B2.5 records)",
    "scripts/negative_controls_B2_5.py": "added (B2.5 code-mutation controls)",
    "scripts/check_identity_V0_4_dev6.py": "added (this identity checker)",
    "scripts/identity_controls_V0_4_dev6.py": "added (forbidden-modification controls of this checker)",
    "data/B2_5_index.json": "added (B2.5 record)",
    "data/B2_5_dependency_graph.json": "added (B2.5 proof dependency graph)",
    "data/B2_5_negative_controls.json": "added (B2.5 record)",
    "data/B2_5_identity_controls.json": "added (identity-checker controls record)",
    REPORT: "added (this report)",
}
TEST_DOCS_ALLOWED = {
    "removed": {"test_status_is_research_V045_dev",
                "test_proved_status_only_computer_assisted_and_only_for_theorem_A_corollary_M_and_proposition_B2",
                "test_B1_erratum_closed_and_B2_4_claim_boundary"},
    "added": {"test_status_is_research_V046_dev",
              "test_proved_status_only_computer_assisted_and_only_for_A_M_B2_B3",
              "test_B1_erratum_closed_and_B2_4_claim_boundary_after_B2_5",
              "test_B2_5_claim_boundary"},
}


def check_init(old, new):
    fails = []
    to, tn = ast.parse(old), ast.parse(new)
    if len(to.body) != len(tn.body):
        return ["statement count changed"]
    for a, b in zip(to.body[1:], tn.body[1:]):
        if isinstance(a, ast.Assign) and isinstance(b, ast.Assign) and ast.unparse(a.targets[0]) in (
                "__version__", "STATUS") and ast.unparse(a.targets) == ast.unparse(b.targets):
            continue
        if ast.dump(a) != ast.dump(b):
            fails.append(f"statement changed: {ast.unparse(b)[:60]}")
    v = {ast.unparse(s.targets[0]): s.value.value for s in tn.body if isinstance(s, ast.Assign)}
    if v.get("__version__") != "0.4.0.dev6" or v.get("STATUS") != "RESEARCH / V0.4-dev.6":
        fails.append("version/status values")
    return fails


def check_test_docs(old, new):
    return compare_units(old, new, set(), TEST_DOCS_ALLOWED["added"], removed=TEST_DOCS_ALLOWED["removed"])


def notes_body(t):
    return t[t.index("\n## 1. "):t.index("\n## 13. ")]


def check_notes(old, new):
    try:
        return [] if notes_body(old) == notes_body(new) else ["NOTES.md: §1–§12 not byte-identical"]
    except ValueError:
        return ["NOTES.md: section markers missing"]


def check_changelog(old, new):
    i = old.index("\n## V0.4-dev.5")
    ok = new.startswith(old[:i]) and new.endswith(old[i:]) and "## V0.4-dev.6" in new[:new.index("\n## V0.4-dev.5")]
    return [] if ok else ["CHANGELOG.md: earlier entries not verbatim"]


RULES = {
    "src/cube_bif/__init__.py": ("changed (version/status metadata only)", check_init),
    "tests/test_docs.py": ("changed (three documentation tests replaced, one added)", check_test_docs),
    "NOTES.md": ("changed (documentation; §1–§12 byte-identical; header, §0, new §13–§14)", check_notes),
    "CHANGELOG.md": ("changed (documentation; earlier entries verbatim)", check_changelog),
    "RESEARCH_LOG.md": ("appended (documentation)", lambda o, n: [] if n.startswith(o) else
                        ["RESEARCH_LOG.md is not append-only"]),
    "README.md": ("changed (documentation)", lambda o, n: []),
}


def run(zip_path, root):
    old, new = load_zip(zip_path), load_tree(root)
    junk = [p for p in new if "__pycache__" in p or ".pytest_cache" in p or p.endswith(".pyc")]
    rows, fails = [], []
    if junk:
        fails.append(f"cache files present: {junk[:3]}")
    for p in sorted(set(old) | set(new)):
        if p in junk:
            continue
        o, n = old.get(p), new.get(p)
        if p == "SHA256SUMS":
            f = check_manifest({k: v for k, v in new.items() if k not in junk})
            rows.append((p, "regenerated (integrity list)" if not f else "FAIL: " + "; ".join(f), o, None))
            fails += f
            continue
        if o is None:
            if p not in ADDED:
                rows.append((p, "FAIL: unexpected added file", None, n))
                fails.append(f"{p}: unexpected added file")
            else:
                rows.append((p, ADDED[p], None, n))
            continue
        if n is None:
            rows.append((p, "FAIL: deleted", o, None))
            fails.append(f"{p}: deleted")
            continue
        if o == n:
            rows.append((p, "identical", o, n))
            continue
        if p in RULES:
            label, rule = RULES[p]
            f = rule(o.decode("utf-8"), n.decode("utf-8"))
            rows.append((p, label if not f else "FAIL: " + "; ".join(f), o, n))
            fails += [f"{p}: {x}" for x in f]
        else:
            rows.append((p, "FAIL: changed (must be byte-identical)", o, n))
            fails.append(f"{p}: changed (must be byte-identical)")
    return rows, fails, old


def report(rows, fails, zip_path, old):
    zsha = sha(pathlib.Path(zip_path).read_bytes())
    counts = {}
    for _, c, _, _ in rows:
        k = c.split(" (")[0]
        counts[k] = counts.get(k, 0) + 1
    notes_old = old["NOTES.md"].decode()
    out = io.StringIO()
    w = out.write
    w("# Identity check: V0.4-dev.6 (Phase B2.5) against V0.4-dev.5\n\n")
    w(f"- Reference: `EIT_LJ_CUBE_BIFURCATIONS_V0.4-dev.5.zip`, SHA-256 `{zsha}`.\n")
    w("- Generated by `scripts/check_identity_V0_4_dev6.py` (rules in its docstring); the checker's own controls are in "
      "`data/B2_5_identity_controls.json` (`scripts/identity_controls_V0_4_dev6.py`).\n")
    w("- Allowed: the B2.5 module, tests, scripts and records, this checker, its controls and report, documentation, "
      "version/status metadata, the integrity list. Everything else must be byte-identical: Paper 2's inputs, "
      "Track A, B0, B1 (code, formulas, the historical certificate, the erratum artefacts), B2.0-B2.4 (code, "
      "certificate, records, dependency graphs), every audit report and audits/README.md, all earlier scripts, "
      "records and identity reports.\n\n")
    w("## Result\n\n")
    w(("**PASS.** " if not fails else "**FAIL.** ") + ", ".join(f"{v} {k}" for k, v in sorted(counts.items())) + ".\n\n")
    for f in fails:
        w(f"- {f}\n")
    w(f"- SHA-256 of the NOTES text from \"## 1.\" up to \"## 13.\" (§1–§12): V0.4-dev.5 "
      f"`{sha(notes_body(notes_old).encode())}`; the same extract of V0.4-dev.6 is required to be byte-identical.\n\n")
    w("## Files\n\n| path | class | V0.4-dev.5 SHA-256 (16) | V0.4-dev.6 SHA-256 (16) |\n|---|---|---|---|\n")
    for p, c, o, n in rows:
        if p == REPORT:
            continue
        w(f"| `{p}` | {c} | {sha(o)[:16] if o is not None else '—'} | "
          f"{('regenerated' if p == 'SHA256SUMS' else sha(n)[:16]) if (n is not None or p == 'SHA256SUMS') else '—'} |\n")
    w("\nThis report is not listed in its own table (its row would depend on itself). SHA256SUMS is regenerated after "
      "it is written.\n")
    return out.getvalue()


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    zip_path = args[0]
    root = pathlib.Path(args[1]) if len(args) > 1 else pathlib.Path(__file__).resolve().parents[1]
    rows, fails, old = run(zip_path, root)
    if "--report" in argv:
        (root / REPORT).write_text(report(rows, fails, zip_path, old))
    for f in fails:
        print("FAIL", f)
    print("PASS" if not fails else f"FAIL ({len(fails)})")
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
