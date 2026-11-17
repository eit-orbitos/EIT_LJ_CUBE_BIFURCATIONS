"""Mechanical identity check: V0.4-dev.4 (erratum E-B1) against V0.4-dev.3.

Usage: python scripts/check_identity_V0_4_dev4.py <EIT_LJ_CUBE_BIFURCATIONS_V0.4-dev.3.zip> [<dev.4 project root>]
          [--report docs/V0.4-dev.4_IDENTITY_CHECK.md]

Every V0.4-dev.3 file must be byte-identical in V0.4-dev.4, except for the allowed changes below; each allowed change
is checked by its own rule, not merely listed:
- src/cube_bif/b1_cert.py: only the Taylor routine _taylor changes; the only additions are `import contextlib` and the
  helpers SeriesTruncationError, _series_capacity, _series_coefficients. Every other line (formulas, Newton, carrier,
  bookkeeping, endpoints, certificate assembly) is identical, in the same order.
- src/cube_bif/b1_check.py: only Model.taylor changes; the only additions are TruncatedSeries, SeriesLength,
  Model._raw_series and one section comment. Everything else identical.
- tests/test_B1_certificate.py: the fresh-versus-stored hash test is replaced by a pin of the stored certificate;
  every other test is identical.
- tests/test_docs.py: status pins only (exact string mapping dev.3 -> dev.4).
- src/cube_bif/__init__.py: module docstring and the values of __version__ and STATUS only.
- documentation: NOTES.md (every section from "## 0." to the end of §9 byte-identical), CHANGELOG.md (earlier entries
  verbatim), RESEARCH_LOG.md (append-only), README.md (documentation; free).
- added files: an explicit list (erratum tests, scripts, data records, this report).
- SHA256SUMS: regenerated; it must list exactly the files of the tree with their current hashes.
Anything else (a changed, deleted or unexpected file) fails the check.
"""
import ast
import hashlib
import io
import pathlib
import re
import sys
import zipfile

PREFIX = "EIT_LJ_CUBE_BIFURCATIONS/"
REPORT = "docs/V0.4-dev.4_IDENTITY_CHECK.md"
ADDED = {
    "tests/test_B1_erratum.py": "added (erratum regression tests)",
    "scripts/run_B1_erratum.py": "added (erratum verification)",
    "scripts/negative_controls_B1_erratum.py": "added (erratum code-mutation controls)",
    "scripts/reproduce_B1_erratum_pre_patch.py": "added (pre-patch reproduction on V0.4-dev.3)",
    "scripts/check_identity_V0_4_dev4.py": "added (this identity checker)",
    "scripts/identity_controls_V0_4_dev4.py": "added (forbidden-modification controls of this checker)",
    "data/B1_ERRATUM_report.json": "added (erratum record)",
    "data/B1_ERRATUM_pre_patch_reproduction.json": "added (erratum record)",
    "data/B1_ERRATUM_corrected_rebuild_certificate.json": "added (corrected rebuild, corroboration only)",
    "data/B1_ERRATUM_CORRECTED_REBUILD_SEMANTIC.sha256": "added (corrected rebuild hash)",
    "data/B1_ERRATUM_negative_controls.json": "added (erratum record)",
    "data/B1_ERRATUM_identity_controls.json": "added (erratum record)",
    REPORT: "added (this report)",
}
B1_CERT_ALLOWED = {"changed": {"_taylor"}, "added": {"SeriesTruncationError", "_series_capacity",
                                                     "_series_coefficients", "import contextlib"}}
B1_CHECK_ALLOWED = {"changed": {"Model.taylor"}, "added": {"TruncatedSeries", "SeriesLength", "Model._raw_series"}}
B1_CHECK_ADDED_LINES = {"# ---- series length (erratum E-B1, V0.4-dev.4) "
                        "--------------------------------------------------------------------------"}
TEST_B1_CERT_ALLOWED = {"removed": {"test_fresh_and_stored_semantic_hashes_agree"},
                        "added": {"test_stored_certificate_is_the_historical_audited_one"}}
PIN_MAP = [("RESEARCH / V0.4-dev.3", "RESEARCH / V0.4-dev.4"), ("0.4.0.dev3", "0.4.0.dev4"),
           ("test_status_is_research_V043_dev", "test_status_is_research_V044_dev")]


def sha(b):
    return hashlib.sha256(b).hexdigest()


def load_zip(path):
    out = {}
    with zipfile.ZipFile(path) as z:
        for n in z.namelist():
            if n.endswith("/"):
                continue
            if not n.startswith(PREFIX):
                raise SystemExit(f"unexpected member {n}")
            out[n[len(PREFIX):]] = z.read(n)
    return out


def load_tree(root):
    root = pathlib.Path(root)
    out = {}
    for p in sorted(root.rglob("*")):
        if p.is_file():
            rel = p.relative_to(root).as_posix()
            out[rel] = p.read_bytes()
    return out


# ---- python units: top-level statements and class methods, with their exact source lines --------------------------
def _units(src):
    """[(name, text)] for each top-level statement (functions, classes and methods by name), in order. Lines between
    statements (comments, blank lines) are attached to the following unit as its prefix; blank-line runs collapsed."""
    lines = src.splitlines()
    tree = ast.parse(src)
    units = []

    def name_of(node, cls=None):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            return (cls + "." if cls else "") + node.name
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            return "import " + ", ".join(a.name for a in node.names) if isinstance(node, ast.Import) else \
                "from " + (node.module or "") + " import " + ", ".join(a.name for a in node.names)
        if isinstance(node, ast.Expr) and isinstance(getattr(node, "value", None), ast.Constant) \
                and isinstance(node.value.value, str):
            return (cls + "." if cls else "") + "<docstring>"
        return (cls + "." if cls else "") + "<stmt:" + ast.unparse(node).split("\n")[0][:60] + ">"

    def start(node):
        return min([node.lineno] + [d.lineno for d in getattr(node, "decorator_list", [])])

    def add(nodes, cls=None, prev_end=0):
        for node in nodes:
            s, e = start(node), node.end_lineno
            gap = [l for l in lines[prev_end:s - 1] if l.strip()]
            if isinstance(node, ast.ClassDef):
                body_start = node.body[0].lineno if node.body else e + 1
                header = "\n".join(gap + lines[s - 1:body_start - 1])
                units.append((name_of(node, cls) + "<header>", header))
                add(node.body, cls=node.name, prev_end=body_start - 1)
            else:
                units.append((name_of(node, cls), "\n".join(gap + lines[s - 1:e])))
            prev_end = e
        return prev_end
    end = add(tree.body)
    tail = [l for l in lines[end:] if l.strip()]
    if tail:
        units.append(("<tail>", "\n".join(tail)))
    return units


def compare_units(old_src, new_src, changed, added, removed=(), added_lines=()):
    """Fails unless: the units of the old file, minus `changed` and `removed`, appear unchanged and in the same order
    in the new file; the new file's other units are `changed` or `added`; comment lines that are new are listed."""
    fails = []
    old_u, new_u = _units(old_src), _units(new_src)
    old_d, new_d = dict(old_u), dict(new_u)
    if len(old_d) != len(old_u) or len(new_d) != len(new_u):
        fails.append("duplicate unit names")

    def cov(n, names):
        return any(n == a or n == a + "<header>" or n.startswith(a + ".") for a in names)
    keep_old = [(n, t) for n, t in old_u if not cov(n, changed) and not cov(n, removed)]
    keep_new = [(n, t) for n, t in new_u if not cov(n, changed) and not cov(n, added)]

    def strip_added(t):
        return "\n".join(l for l in t.split("\n") if l.strip() not in {a.strip() for a in added_lines})
    if [n for n, _ in keep_old] != [n for n, _ in keep_new]:
        fails.append("unit list or order differs outside the allowed units: "
                     f"{sorted(set(n for n, _ in keep_old) ^ set(n for n, _ in keep_new))[:6]}")
    else:
        for (n, t), (_, t2) in zip(keep_old, keep_new):
            if t != strip_added(t2):
                fails.append(f"unit {n} changed")
    for n in changed:
        if n not in old_d or n not in new_d:
            fails.append(f"allowed unit {n} missing")
    for n in removed:
        if any(cov(m, {n}) for m in new_d):
            fails.append(f"unit {n} should have been removed")
    for n in added:
        if not any(cov(m, {n}) for m in new_d):
            fails.append(f"allowed addition {n} missing")
    return fails


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
    if v.get("__version__") != "0.4.0.dev4" or v.get("STATUS") != "RESEARCH / V0.4-dev.4":
        fails.append("version/status values")
    return fails


def check_pins(old, new):
    t = old
    for a, b in PIN_MAP:
        t = t.replace(a, b)
    return [] if t == new else ["test_docs.py differs beyond the status pins"]


def check_notes(old, new):
    def body(t):
        i, j = t.index("\n## 0. Status labels"), t.index("\n## 10. ")
        return t[i:j]
    fails = []
    try:
        if body(old) != body(new):
            fails.append("NOTES.md: §0–§9 not byte-identical")
    except ValueError:
        fails.append("NOTES.md: section markers missing")
    return fails


def check_changelog(old, new):
    i = old.index("\n## V0.4-dev.3")
    return [] if new.endswith(old[i:]) and new.startswith(old[:i]) and "## V0.4-dev.4" in new[:new.index(
        "\n## V0.4-dev.3")] else ["CHANGELOG.md: earlier entries not verbatim"]


def check_manifest(tree):
    lines = tree.get("SHA256SUMS", b"").decode().splitlines()
    listed = {}
    for l in lines:
        h, p = l.split("  ", 1)
        listed[p[2:] if p.startswith("./") else p] = h
    actual = {p: sha(b) for p, b in tree.items() if p != "SHA256SUMS"}
    fails = []
    if set(listed) != set(actual):
        fails.append(f"SHA256SUMS lists other files: {sorted(set(listed) ^ set(actual))[:5]}")
    bad = [p for p in listed if p in actual and listed[p] != actual[p]]
    if bad:
        fails.append(f"SHA256SUMS stale for {bad[:5]}")
    return fails


RULES = {
    "src/cube_bif/b1_cert.py": ("changed (erratum: _taylor and its helpers only)", lambda o, n: compare_units(
        o, n, B1_CERT_ALLOWED["changed"], B1_CERT_ALLOWED["added"])),
    "src/cube_bif/b1_check.py": ("changed (erratum: Model.taylor and its helpers only)", lambda o, n: compare_units(
        o, n, B1_CHECK_ALLOWED["changed"], B1_CHECK_ALLOWED["added"], added_lines=B1_CHECK_ADDED_LINES)),
    "tests/test_B1_certificate.py": ("changed (fresh-vs-stored hash test replaced by a pin of the stored "
                                     "certificate)", lambda o, n: compare_units(
        o, n, set(), TEST_B1_CERT_ALLOWED["added"], removed=TEST_B1_CERT_ALLOWED["removed"])),
    "tests/test_docs.py": ("changed (status pins only)", check_pins),
    "src/cube_bif/__init__.py": ("changed (version/status metadata only)", check_init),
    "NOTES.md": ("changed (documentation; §0–§9 byte-identical; header, §10 erratum, §11 next steps)", check_notes),
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
            if p in ADDED:
                rows.append((p, ADDED[p], None, n))
            else:
                rows.append((p, "FAIL: unexpected added file", None, n))
                fails.append(f"{p}: unexpected added file")
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
    w("# Identity check: V0.4-dev.4 (erratum E-B1) against V0.4-dev.3\n\n")
    w(f"- Reference: `EIT_LJ_CUBE_BIFURCATIONS_V0.4-dev.3.zip`, SHA-256 `{zsha}`.\n")
    w("- Generated by `scripts/check_identity_V0_4_dev4.py` (rules in its docstring); the checker's own controls are in "
      "`data/B1_ERRATUM_identity_controls.json` (`scripts/identity_controls_V0_4_dev4.py`).\n")
    w("- Allowed: the two affected B1 Taylor routines and their helpers (checked unit by unit), the erratum tests, "
      "scripts and records, documentation, version/status metadata, the integrity list. Everything else must be "
      "byte-identical: Track A, B0, B1 formulas and the historical B1 certificate, B2.0, B2.1, B2.2, B2.3, the audit "
      "reports, all earlier scripts and records.\n\n")
    w("## Result\n\n")
    w(("**PASS.** " if not fails else "**FAIL.** ") + ", ".join(f"{v} {k}" for k, v in sorted(counts.items())) + ".\n\n")
    for f in fails:
        w(f"- {f}\n")
    i, j = notes_old.index("\n## 0. Status labels"), notes_old.index("\n## 10. ")
    w(f"- SHA-256 of the NOTES text from \"## 0. Status labels\" up to \"## 10.\" (§0–§9): V0.4-dev.3 "
      f"`{sha(notes_old[i:j].encode())}`; the same extract of V0.4-dev.4 is required to be byte-identical.\n\n")
    w("## Files\n\n| path | class | V0.4-dev.3 SHA-256 (16) | V0.4-dev.4 SHA-256 (16) |\n|---|---|---|---|\n")
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
