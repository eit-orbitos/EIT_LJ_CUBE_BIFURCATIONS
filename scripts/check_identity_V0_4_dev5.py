"""Mechanical identity check: V0.4-dev.5 (B1 erratum closure record + Phase B2.4) against V0.4-dev.4.

Usage: python scripts/check_identity_V0_4_dev5.py <EIT_LJ_CUBE_BIFURCATIONS_V0.4-dev.4.zip> [<dev.5 project root>]
          [--report docs/V0.4-dev.5_IDENTITY_CHECK.md]

Every V0.4-dev.4 file must be byte-identical in V0.4-dev.5, except for the allowed changes below; each allowed change
is checked by its own rule, not merely listed:
- src/cube_bif/__init__.py: module docstring and the values of __version__ and STATUS only (0.4.0.dev5,
  "RESEARCH / V0.4-dev.5").
- tests/test_docs.py: the status test and the proved-status test are replaced by their dev.5 versions and one test
  (B1 erratum closed, B2.4 claim boundary) is added; every other unit is identical, in the same order.
- NOTES.md: every section from "## 1." up to "## 11." (§1–§10) byte-identical; the header, §0 and the new §11–§13 are
  documentation.
- CHANGELOG.md: earlier entries verbatim, a new "## V0.4-dev.5" entry on top.
- RESEARCH_LOG.md: append-only.
- audits/README.md: one table row for the new report inserted and one section appended; nothing else changes.
- README.md: documentation (free).
- added files: an explicit list. The new audit report must have the pinned SHA-256 of the received copy.
- SHA256SUMS: regenerated; it must list exactly the files of the tree with their current hashes.
Anything else (a changed, deleted or unexpected file) fails the check. In particular Paper 2's inputs, Track A, B0, B1
(code, formulas, the historical certificate and the erratum artefacts), B2.0-B2.3 and every earlier audit report,
script, record and identity report must be byte-identical.

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

REPORT = "docs/V0.4-dev.5_IDENTITY_CHECK.md"
REAUDIT = "audits/CUBE_BIFURCATIONS_V04_DEV4_B1_ERRATUM_REAUDIT.md"
REAUDIT_SHA = "ba482da06aa0492b6524e47680fd949170f4d0dafac0d5661a073efce4d46b74"
ADDED = {
    REAUDIT: "added (targeted re-audit report, byte-identical to the received copy)",
    "src/cube_bif/b2_branch.py": "added (B2.4: exact layer, statement, dependency graph, numerics)",
    "tests/test_B2_branch.py": "added (B2.4 tests and statement/graph negative controls)",
    "scripts/run_B2_4.py": "added (B2.4 records)",
    "scripts/negative_controls_B2_4.py": "added (B2.4 code-mutation controls)",
    "scripts/check_identity_V0_4_dev5.py": "added (this identity checker)",
    "scripts/identity_controls_V0_4_dev5.py": "added (forbidden-modification controls of this checker)",
    "data/B2_4_branch.json": "added (B2.4 record)",
    "data/B2_4_dependency_graph.json": "added (B2.4 proof dependency graph)",
    "data/B2_4_negative_controls.json": "added (B2.4 record)",
    "data/B2_4_identity_controls.json": "added (identity-checker controls record)",
    REPORT: "added (this report)",
}
TEST_DOCS_ALLOWED = {
    "removed": {"test_status_is_research_V044_dev",
                "test_proved_status_only_computer_assisted_and_only_for_theorem_A_and_corollary_M"},
    "added": {"test_status_is_research_V045_dev",
              "test_proved_status_only_computer_assisted_and_only_for_theorem_A_corollary_M_and_proposition_B2",
              "test_B1_erratum_closed_and_B2_4_claim_boundary"},
}
AUDITS_README_ROW = "| `CUBE_BIFURCATIONS_V04_DEV4_B1_ERRATUM_REAUDIT.md` |"
AUDITS_README_SECTION = "\n## Erratum E-B1 re-audit (received with V0.4-dev.5)\n"


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
    if v.get("__version__") != "0.4.0.dev5" or v.get("STATUS") != "RESEARCH / V0.4-dev.5":
        fails.append("version/status values")
    return fails


def check_test_docs(old, new):
    return compare_units(old, new, set(), TEST_DOCS_ALLOWED["added"], removed=TEST_DOCS_ALLOWED["removed"])


def notes_body(t):
    return t[t.index("\n## 1. "):t.index("\n## 11. ")]


def check_notes(old, new):
    try:
        return [] if notes_body(old) == notes_body(new) else ["NOTES.md: §1–§10 not byte-identical"]
    except ValueError:
        return ["NOTES.md: section markers missing"]


def check_changelog(old, new):
    i = old.index("\n## V0.4-dev.4")
    ok = new.startswith(old[:i]) and new.endswith(old[i:]) and "## V0.4-dev.5" in new[:new.index("\n## V0.4-dev.4")]
    return [] if ok else ["CHANGELOG.md: earlier entries not verbatim"]


def check_audits_readme(old, new):
    lines = new.split("\n")
    rows = [k for k, l in enumerate(lines) if l.startswith(AUDITS_README_ROW)]
    if len(rows) != 1:
        return ["audits/README.md: the new table row is missing or duplicated"]
    stripped = "\n".join(lines[:rows[0]] + lines[rows[0] + 1:])
    if not stripped.startswith(old) or not stripped[len(old):].startswith(AUDITS_README_SECTION):
        return ["audits/README.md: changed beyond one inserted row and one appended section"]
    return []


RULES = {
    "src/cube_bif/__init__.py": ("changed (version/status metadata only)", check_init),
    "tests/test_docs.py": ("changed (status tests replaced, one documentation test added)", check_test_docs),
    "NOTES.md": ("changed (documentation; §1–§10 byte-identical; header, §0, new §11–§13)", check_notes),
    "CHANGELOG.md": ("changed (documentation; earlier entries verbatim)", check_changelog),
    "RESEARCH_LOG.md": ("appended (documentation)", lambda o, n: [] if n.startswith(o) else
                        ["RESEARCH_LOG.md is not append-only"]),
    "audits/README.md": ("changed (one row inserted, one section appended)", check_audits_readme),
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
            elif p == REAUDIT and sha(n) != REAUDIT_SHA:
                rows.append((p, "FAIL: re-audit report differs from the received copy", None, n))
                fails.append(f"{p}: SHA-256 {sha(n)[:16]}… is not the received {REAUDIT_SHA[:16]}…")
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
    w("# Identity check: V0.4-dev.5 (B1 erratum closure record + Phase B2.4) against V0.4-dev.4\n\n")
    w(f"- Reference: `EIT_LJ_CUBE_BIFURCATIONS_V0.4-dev.4.zip`, SHA-256 `{zsha}`.\n")
    w("- Generated by `scripts/check_identity_V0_4_dev5.py` (rules in its docstring); the checker's own controls are in "
      "`data/B2_4_identity_controls.json` (`scripts/identity_controls_V0_4_dev5.py`).\n")
    w("- Allowed: the targeted re-audit report (pinned hash), the B2.4 module, tests, scripts and records, "
      "documentation, version/status metadata, the integrity list. Everything else must be byte-identical: Paper 2's "
      "inputs, Track A, B0, B1 (code, formulas, the historical certificate, the erratum artefacts), B2.0-B2.3, the "
      "earlier audit reports, all earlier scripts, records and identity reports.\n\n")
    w("## Result\n\n")
    w(("**PASS.** " if not fails else "**FAIL.** ") + ", ".join(f"{v} {k}" for k, v in sorted(counts.items())) + ".\n\n")
    for f in fails:
        w(f"- {f}\n")
    w(f"- SHA-256 of the NOTES text from \"## 1.\" up to \"## 11.\" (§1–§10): V0.4-dev.4 "
      f"`{sha(notes_body(notes_old).encode())}`; the same extract of V0.4-dev.5 is required to be byte-identical.\n\n")
    w("## Files\n\n| path | class | V0.4-dev.4 SHA-256 (16) | V0.4-dev.5 SHA-256 (16) |\n|---|---|---|---|\n")
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
