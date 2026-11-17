"""Whole-tree classified text scan for V1.0.0-rc2 (stale status/author terms and claim-discipline terms).

Usage:  python scripts/scan_text_rc2.py [project root] [--md=<report.md>] [--json=<report.json>]

Every occurrence of a watched term in every text file of the tree is classified:
  VERBATIM AUDIT REPORT        audits/* (third-party records, never edited)
  AUDITED CODE OR RECORD       src/, data/, reference/ and the pre-RC scripts/tests (byte-identical with V0.4-dev.6)
  RELEASE TOOLING PATTERN      the release scanners/checkers/tests themselves (the term is a search pattern)
  HISTORICAL RECORD            NOTES §0-§15, earlier CHANGELOG/RESEARCH_LOG entries, identity checks, RC1 records
  CURRENT: <justification>     current surfaces, each justified by a rule or by a reviewed entry in REVIEWED
  CURRENT: UNRESOLVED          a current-surface occurrence with no justification  -> exit status 1
"""
import json
import pathlib
import re
import sys

STALE_TERMS = ["sole author", "AUTHOR CONTRIBUTION DETAILS REQUIRED", "FINAL AUTHOR REVIEW REQUIRED", "ORCID REQUIRED",
               "Mihail ORCID", "Woodland Park", "Little Falls", "New Jersey", "PCTI",
               "Passaic County Technical Institute", "student", "school", "not independently audited",
               "pending B2.3 audit", "pending B2.4 audit", "pending B2.5 audit", "erratum pending",
               "submission ready", "published", "accepted"]
CLAIM_TERMS = ["stable", "stability", "globally stable", "complete", "universal", "technological", "device",
               "switching", "memory", "hysteresis", "metastability", "application", "energy efficiency", "quantum",
               "AI architecture"]
TERMS = STALE_TERMS + CLAIM_TERMS
PAT = re.compile(r"(?<![A-Za-z])(" + "|".join(re.escape(t) for t in sorted(TERMS, key=len, reverse=True)) +
                 r")(?:s|es)?(?![A-Za-z])", re.I)
TEXT_SUFFIXES = {".md", ".tex", ".bib", ".py", ".json", ".cff", ".txt", ""}

RC_TOOLING = {"scripts/check_release_text.py", "scripts/scan_text_rc2.py", "scripts/check_preservation_V1_0_0_rc2.py",
              "scripts/preservation_controls_V1_0_0_rc2.py", "tests/test_release_rc2.py", "tests/test_docs.py"}
HISTORICAL_FILES = {"RELEASE_NOTES_RC1.md", "docs/QA_RESULTS_RC1.md", "docs/QA_RESULTS_RC1.json",
                    "docs/V1.0.0-rc1_PRESERVATION_CHECK.md", "docs/V1.0.0-rc1_PRESERVATION_CONTROLS.json",
                    "scripts/check_preservation_V1_0_0_rc1.py", "scripts/preservation_controls_V1_0_0_rc1.py",
                    "docs/CONTRADICTIONS_EXTERNAL_BRAINSTORM.md", "audits/README.md"}
GENERATED = {"docs/V1.0.0-rc2_TEXT_SCAN.md", "docs/V1.0.0-rc2_TEXT_SCAN.json",
             "docs/V1.0.0-rc2_PRESERVATION_CHECK.md", "docs/V1.0.0-rc2_PRESERVATION_CHECK.json",
             "docs/V1.0.0-rc2_PRESERVATION_CONTROLS.json", "docs/QA_RESULTS_RC2.md", "docs/QA_RESULTS_RC2.json"}

NEGATION = re.compile(r"\b(not|no|never|none|nor|without|unstable|saddles?|excluded|exclude[sd]?|outside|"
                      r"out of scope|do not|does not|isn't|aren't|neither|nothing|unsupported)\b|\bNOT\b", re.I)
RULES = [
    ("Paper 2 repository/archive identifier", lambda f, l, t: t == "STABILITY" and "FULL_VECTOR_STABILITY" in l),
    ("machine-readable flag: no stability implied", lambda f, l, t: '"implies_stability": false' in l),
    ("historical statement marked in place", lambda f, l, t: re.search(r"at that version|when written|historical|"
                                                                        r"superseded", l) is not None),
    ("bibliographic title / venue", lambda f, l, t: f == "paper/references.bib" and
        re.search(r"(title|journal|booktitle|series)\s*=", l) is not None),
    ("bibliographic note on the Paper 2 record title", lambda f, l, t: f == "paper/references.bib" and
        "Full-Vector Equilibria and Stability" in l),
    ("Paper 2 software-record title", lambda f, l, t: "Full-Vector Equilibria and Stability" in l),
    ("mathematical term (complete quartic / invariant / configuration)", lambda f, l, t: t.lower() == "complete" and
        re.search(r"complete (invariant )?quartic|complete branch configurations|complete configurations", l, re.I)),
    ("conservative novelty sentence", lambda f, l, t: t.lower() == "complete" and
        "not aware of a prior complete classification" in l),
    ("technical sense: a certificate or input accepted by a checker", lambda f, l, t: t.lower() == "accepted" and
        re.search(r"certificate|checker|endpoints?_accepted|endpoints accepted|accepted with|is accepted by|"
                  r"accepted \(|regeneration is accepted", l, re.I)),
    ("negated / disclaimer / scope exclusion", lambda f, l, t: NEGATION.search(l) is not None),
]
# Reviewed current-surface occurrences without a rule: (file, exact substring of the line) -> justification.
REVIEWED = {
    ("paper/sections/01_introduction.tex", "their stability can change with the exponents"):
        "general motivation: the linear stability (Morse index) of symmetric equilibria changes with (p, q); this is the "
        "frozen Paper 2 result the paper builds on; no stability claim for any branch",
    ("paper/sections/04_transition_curves.tex", "\\textbf{Stable and unstable blocks}"):
        "summary heading of frozen Paper 2 Lemmas S, E, T4 (sign-definite Hessian blocks of the cube); the next lines "
        "state the signs; not a claim about branches",
    ("paper/sections/01_introduction.tex", "That is a stability statement"):
        "describes the content of the cited Ihrig-Golubitsky theorem and distinguishes it from the branch-type question",
    ("paper/sections/06_t2g_invariants.tex", "Their theorem concerns stability"):
        "describes the cited theorem; the same sentence says it is not used in any proof",
    ("docs/AUDIT_STATUS_MATRIX.json", "technology/application claims"):
        "entry of the list `not_results_of_paper_3` (scope exclusion)",
    ("submission/COVER_LETTER_DRAFT.md", "[AUTHOR CHECK: update if either has since been submitted or accepted.]"):
        "author-check placeholder in the unsent cover letter; makes no acceptance claim",
}


def section_ranges(rel, text):
    """Return a function line_no -> 'current' | 'historical' for multi-era files."""
    lines = text.split("\n")
    def idx(prefix):
        for i, l in enumerate(lines, 1):
            if l.startswith(prefix):
                return i
        return None
    if rel == "NOTES.md":
        s0, s16 = idx("## 0. Status labels"), idx("## 16. Release candidate V1.0.0-rc2")
        return lambda n: "current" if (s0 and n < s0) or (s16 and n >= s16) else "historical"
    if rel == "CHANGELOG.md":
        a, b = idx("## V1.0.0-rc2"), idx("## V1.0.0-rc1")
        return lambda n: "current" if (a and b and a <= n < b) or (a and n < a) else "historical"
    if rel == "RESEARCH_LOG.md":
        a = idx("## 2026-11-16 — V1.0.0-rc2")
        return lambda n: "current" if a and n >= a else "historical"
    return None


def era(rel):
    if rel.startswith("audits/") and rel != "audits/README.md":
        return "VERBATIM AUDIT REPORT"
    if rel in RC_TOOLING:
        return "RELEASE TOOLING PATTERN"
    if rel in GENERATED:
        return "GENERATED RC2 RECORD (lists terms)"
    if rel in HISTORICAL_FILES or re.match(r"docs/V0\.", rel):
        return "HISTORICAL RECORD"
    if rel.startswith(("data/", "reference/")) or (rel.startswith("src/") and rel != "src/cube_bif/__init__.py"):
        return "AUDITED CODE OR RECORD"
    if rel.startswith(("scripts/", "tests/")):
        return "AUDITED CODE OR RECORD"
    return None


def scan(root):
    root = pathlib.Path(root)
    rows = []
    for p in sorted(root.rglob("*")):
        if not p.is_file() or p.suffix not in TEXT_SUFFIXES or "__pycache__" in p.parts or p.name == "SHA256SUMS":
            continue
        rel = p.relative_to(root).as_posix()
        if rel.startswith("paper/figures/") and p.suffix != ".py":
            continue
        text = p.read_text(encoding="utf-8", errors="ignore")
        multi = section_ranges(rel, text)
        fixed = era(rel)
        lines = text.split("\n")
        for n, line in enumerate(lines, 1):
            for m in PAT.finditer(line):
                term = m.group(1)
                if fixed:
                    cls = fixed
                elif multi and multi(n) == "historical":
                    cls = "HISTORICAL RECORD"
                else:
                    why = next((w for (f, s), w in REVIEWED.items() if f == rel and s in line), None)
                    if why is None:
                        why = next((name for name, rule in RULES if rule(rel, line, term)), None)
                    if why is None and n > 1 and NEGATION.search(lines[n - 2]) and term.lower() in ("stable",):
                        why = "negated in the same sentence (previous line)"
                    cls = "CURRENT: " + (why or "UNRESOLVED")
                rows.append({"file": rel, "line": n, "term": term, "class": cls, "text": line.strip()[:200]})
    unresolved = [r for r in rows if r["class"] == "CURRENT: UNRESOLVED"]
    counts = {}
    for r in rows:
        k = r["class"] if not r["class"].startswith("CURRENT") else "CURRENT (justified)" if \
            r["class"] != "CURRENT: UNRESOLVED" else "CURRENT: UNRESOLVED"
        counts[k] = counts.get(k, 0) + 1
    per_term = {}
    for r in rows:
        per_term.setdefault(r["term"].lower(), {}).setdefault(r["class"].split(":")[0], 0)
        per_term[r["term"].lower()][r["class"].split(":")[0]] += 1
    return {"pass": not unresolved, "n_occurrences": len(rows), "counts": counts, "per_term": per_term,
            "unresolved": unresolved, "rows": rows}


def report_md(res):
    L = ["# V1.0.0-rc2 classified text scan", "",
         "Generated by `scripts/scan_text_rc2.py`. Every occurrence of every watched term in every text file of the tree "
         "is listed below and classified. Historical records and verbatim audit reports are not edited.", "",
         f"**Result: {'PASS' if res['pass'] else 'FAIL'}** — {res['n_occurrences']} occurrences; " +
         ", ".join(f"{k}: {v}" for k, v in sorted(res["counts"].items())) + ".", "",
         "Watched stale/author terms: " + ", ".join(f"`{t}`" for t in STALE_TERMS) + ".", "",
         "Watched claim-discipline terms: " + ", ".join(f"`{t}`" for t in CLAIM_TERMS) + ".", "",
         "## Current-surface occurrences (each justified)", "", "| file:line | term | justification | text |",
         "|---|---|---|---|"]
    for r in res["rows"]:
        if r["class"].startswith("CURRENT"):
            L.append(f"| `{r['file']}:{r['line']}` | {r['term']} | {r['class'][9:]} | "
                     f"{r['text'][:110].replace('|', '/')} |")
    L += ["", "## Occurrences outside the current surfaces (by file and class)", "", "| file | class | n | terms |",
          "|---|---|---|---|"]
    agg = {}
    for r in res["rows"]:
        if not r["class"].startswith("CURRENT"):
            a = agg.setdefault((r["file"], r["class"]), [0, set()])
            a[0] += 1
            a[1].add(r["term"].lower())
    for (f, c), (n, ts) in sorted(agg.items()):
        L.append(f"| `{f}` | {c} | {n} | {', '.join(sorted(ts))} |")
    return "\n".join(L) + "\n"


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    opts = dict(a.split("=", 1) for a in argv[1:] if a.startswith("--") and "=" in a)
    root = args[0] if args else str(pathlib.Path(__file__).resolve().parents[1])
    res = scan(root)
    if "--md" in opts:
        pathlib.Path(opts["--md"]).write_text(report_md(res), encoding="utf-8")
    if "--json" in opts:
        pathlib.Path(opts["--json"]).write_text(json.dumps({k: v for k, v in res.items()}, indent=1,
                                                           ensure_ascii=False) + "\n", encoding="utf-8")
    print("PASS" if res["pass"] else "FAIL", res["counts"])
    for r in res["unresolved"]:
        print(f"  UNRESOLVED {r['file']}:{r['line']} [{r['term']}] {r['text'][:150]}")
    return 0 if res["pass"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
