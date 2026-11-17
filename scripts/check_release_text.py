"""Release-text and authorship scan for V1.0.0: stale status/approval/author strings, authorship and affiliation
metadata, corporate-role wording, author-approved declarations, PDF document properties, claim language, placeholders
and bibliography coverage on the CURRENT surfaces.

Usage:  python scripts/check_release_text.py [project root]      (exit 0 = no finding)

Current surfaces: README.md; NOTES.md header (before "## 0.") and §17; CHANGELOG.md V1.0.0 entry; RESEARCH_LOG.md
V1.0.0 entry; src/cube_bif/__init__.py; CITATION.cff, .zenodo.json, LICENSE, LICENSE-DOCS, RELEASE_NOTES_V1.0.0.md,
FINAL_V1_DELTA_AUDIT_INSTRUCTIONS.md, AUTHOR_DECISION_V1.0.0.md, docs/GITHUB_RELEASE_V1.0.0.md; the current docs
(AI-use log, audit index, status matrix, reproducibility, reference verification, dependency summary); paper/ (*.tex,
*.bib); submission/.
Historical records (earlier CHANGELOG/RESEARCH_LOG entries, NOTES §1-§16, RC1 and RC2 records, identity-check
documents, audit reports, proof records in data/, audited source modules) are out of scope by design;
`scripts/scan_text_v1.py` classifies every occurrence of the watched terms in the whole tree, including those records.
"""
import json
import pathlib
import re
import sys

AFF = "EITNetworks LLC, Tobyhanna, Pennsylvania, USA"
TONI_ORCID = "0009-0009-8343-662X"
TONI_MAIL = "info@eitnetworks.org"
TONI_MAIL2 = "tml30993@gmail.com"
MIHAIL_MAIL = "mmladenski077@gmail.com"
HISTORICAL_MARKERS = ("when written", "at that version", "historical", "keep the wording", "STATUS_PROVED",
                      "(\"not independently audited\")", "resolved", "Resolved", "superseded", "Superseded",
                      "stale", "QA item", "must not", "scan", "at V0.4-dev", "replaces")
STALE = [r"not independently audited", r"ERRATUM PENDING", r"erratum pending", r"PENDING TARGETED",
         r"NOT_PROVIDED", r"RESEARCH / V0\.4-dev\.6", r"pending B2\.[345] audit", r"FINAL AUTHOR REVIEW REQUIRED",
         r"AUTHOR CONTRIBUTION DETAILS REQUIRED", r"AUTHOR INPUT REQUIRED", r"ORCID REQUIRED", r"Mihail ORCID",
         r"Woodland Park", r"Little Falls", r"New Jersey", r"\bPCTI\b", r"Passaic", r"submission[- ]ready",
         r"V1\.0\.0-rc1 · PENDING", r"1\.0\.0rc1", r"V1\.0\.0-rc2 · PENDING", r"1\.0\.0rc2",
         r"FINAL AUTHOR APPROVAL", r"FINAL AUTHOR CONTRIBUTION APPROVAL", r"AUTHORSHIP FINAL APPROVAL",
         r"(?i)copyright-holder approval", r"(?i)human approval required", r"(?i)approval required",
         r"(?i)contribution statement will be finalized", r"TO BE ASSIGNED AFTER FINAL AUDIT",
         r"PENDING FINAL BLIND RELEASE AUDIT"]
# corporate-role words that must not be attached to Mihail Mladenski on a current surface (checked per paragraph)
ROLE = r"(?i)\b(co-?founder|cofounder|owner|member|employee|manager|successor|heir)s?\b"
ROLE_EXEMPT = r"(?i)(correction|withdrawn|removed|is not (currently )?a|not currently|replaces the earlier|earlier wording)"
NOVELTY = [r"first[- ]ever", r"\bunprecedented\b", r"completely novel", r"no one has (previously )?shown",
           r"for the first time", r"\bnovel\b", r"groundbreaking"]
OLD_GEOMETRY = [r"mutually inverted tetrahedra", r"inverted tetrahedra of different sizes"]
SCHOOL = r"\b(PCTI|Passaic|school|student|university|college|institute of technology|high school)\b"
CREDENTIAL = r"\b(Ph\.?\s?D|Dr\.|Prof\.|M\.Sc|B\.Sc|MSc|BSc|professor)\b"
AI_NAMES = r"(Claude|ChatGPT|GPT|Kimi|Tasklet|Gemini|Grok|OpenAI|Anthropic|Moonshot)"
KNOWN_DOIS = {"10.5281/zenodo.24187155", "10.5281/zenodo.24187154", "10.5281/zenodo.24149914",
              "10.5281/zenodo.24149913"}
GH_PLACEHOLDER = "PAPER 3 GITHUB RELEASE"
DOI_PLACEHOLDER = "PAPER 3 ZENODO DOI"
TITLE = "Symmetry-Breaking Bifurcations from the Cubic Equilibrium"
FUNDING = "This research received no external funding."
CI_TEXT = 'Toni Mladenovski is Founder of EITNetworks LLC. Both authors are affiliated with EITNetworks LLC. Software associated with this work is released under a noncommercial license, with commercial use available only by separate written agreement. The research received no external funding.'
CONTRIB_TEXT = 'Toni Mladenovski conceived the study, established the research direction, oversaw the mathematical development and analysis, prepared and reviewed the manuscript, and takes responsibility for the scientific claims. Mihail Mladenski contributed to the conceptualization, structural framing, definition refinement, and analytical discussions throughout the development of the study, and reviewed and approved the final manuscript.'
LIC_TEXT = 'Software: PolyForm Noncommercial License 1.0.0. Manuscript, documentation, figures, generated results and package-authored metadata: CC BY-NC-SA 4.0. Commercial use only by separate written agreement. Copyright © 2026 EITNetworks LLC and the authors.'
LIC_TEX = 'Software: PolyForm Noncommercial License 1.0.0. Manuscript, documentation, figures, generated results and package-authored metadata: CC BY-NC-SA 4.0. Commercial use only by separate written agreement. Copyright \\copyright{} 2026 EITNetworks LLC and the authors.'
PDF_TITLE = "Symmetry-Breaking Bifurcations from the Cubic Equilibrium in Two-Term Inverse-Power Clusters"
PDF_AUTHOR = "Toni Mladenovski; Mihail Mladenski"
STATUS_V1 = "FINAL RELEASE PREPARED / V1.0.0 · PENDING RC2→V1.0.0 DELTA AUDIT"


def flat(s):
    return re.sub(r"\s+", " ", s)


def surfaces(root):
    root = pathlib.Path(root)
    out = {}
    rd = lambda rel: (root / rel).read_text(encoding="utf-8")
    out["README.md"] = rd("README.md")
    notes = rd("NOTES.md")
    out["NOTES.md[header]"] = notes[:notes.index("## 0. Status labels")]
    out["NOTES.md[§17]"] = notes[notes.index("## 17. Release V1.0.0"):]
    ch = rd("CHANGELOG.md")
    out["CHANGELOG.md[v1]"] = ch[ch.index("## V1.0.0 —"):ch.index("## V1.0.0-rc2")]
    rl = rd("RESEARCH_LOG.md")
    out["RESEARCH_LOG.md[v1]"] = rl[rl.index("## 2026-11-16 — V1.0.0:"):]
    out["src/cube_bif/__init__.py"] = rd("src/cube_bif/__init__.py")
    for rel in ("CITATION.cff", ".zenodo.json", "LICENSE", "LICENSE-DOCS", "RELEASE_NOTES_V1.0.0.md",
                "FINAL_V1_DELTA_AUDIT_INSTRUCTIONS.md", "AUTHOR_DECISION_V1.0.0.md", "docs/GITHUB_RELEASE_V1.0.0.md"):
        if (root / rel).exists():
            out[rel] = rd(rel)
    for rel in ("AI_USE_LOG.md", "AUDIT_INDEX.md", "AUDIT_STATUS_MATRIX.md", "AUDIT_STATUS_MATRIX.json",
                "REPRODUCIBILITY.md", "REFERENCE_VERIFICATION.md", "THEOREM_DEPENDENCY_SUMMARY.md"):
        out[f"docs/{rel}"] = rd(f"docs/{rel}")
    for p in sorted((root / "paper").rglob("*")):
        if p.suffix in (".tex", ".bib"):
            out[p.relative_to(root).as_posix()] = p.read_text(encoding="utf-8")
    for p in sorted((root / "submission").glob("*")):
        if p.is_file():
            out[p.relative_to(root).as_posix()] = p.read_text(encoding="utf-8")
    return out


def scan(root):
    root = pathlib.Path(root)
    S = surfaces(root)
    findings = []

    def f(rel, i, kind, line):
        findings.append({"file": rel, "line": i, "kind": kind, "text": str(line).strip()[:160]})
    author_files = {"README.md", "CITATION.cff", ".zenodo.json", "AUTHOR_DECISION_V1.0.0.md",
                    "paper/manuscript.tex", "paper/sections/13_declarations.tex", "src/cube_bif/__init__.py"} | \
        {k for k in S if k.startswith("submission/")}
    for rel, text in S.items():
        for i, line in enumerate(text.split("\n"), 1):
            hist = any(m in line for m in HISTORICAL_MARKERS)
            for pat in STALE:
                if re.search(pat, line) and not hist:
                    f(rel, i, "stale status/metadata", line)
            for pat in NOVELTY:
                if re.search(pat, line, re.I) and not re.search(r"(do not|not write|scan|NOVELTY|no novelty)", line):
                    f(rel, i, "novelty language", line)
            for pat in OLD_GEOMETRY:
                if re.search(pat, line, re.I) and "no old" not in line.lower():
                    f(rel, i, "old geometry wording", line)
            if re.search(r"sole author|single author|sole-author", line, re.I) and \
                    not re.search(r"(no|not|never|stale|reuse)", line, re.I):
                f(rel, i, "sole-author wording", line)
            for m in re.finditer(r"Mihail\s+([A-Za-z]+)", line):
                if m.group(1) != "Mladenski":
                    f(rel, i, "Mihail name spelling", line)
            for m in re.finditer(r"\bMla\w*sk\w*", line):
                if m.group(0) not in ("Mladenski", "Mladenovski", "MLADENSKI", "Mladenski's", "Mladenovski's"):
                    f(rel, i, "surname spelling", line)
            for m in re.finditer(r"(?<!Mladenovski, )\bToni\s+([A-Za-z]+)", line):
                if m.group(1) != "Mladenovski":
                    f(rel, i, "Toni name spelling", line)
            if re.search(r"\b(is|are|remains?)\s+(locally\s+|linearly\s+|dynamically\s+|globally\s+)?stable\b", line,
                         re.I) and not re.search(r"\bnot\b|\bno\b|never|unstable", line, re.I):
                f(rel, i, "stability overclaim", line)
            if re.search(r"cuboid", line, re.I) and re.search(r"D2h|Dtwoh|D_\{2h\}|D_\{?2h", line) and \
                    not re.search(r"\bnot\b|\bno\b|never|non-cuboid", line, re.I):
                f(rel, i, "D2h called cuboid", line)
            for m in re.finditer(r"10\.5281/zenodo\.\d+", line):
                if m.group(0) not in KNOWN_DOIS:
                    f(rel, i, "unknown Zenodo DOI", line)
            emails = set(re.findall(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+", line)) - {TONI_MAIL, TONI_MAIL2, MIHAIL_MAIL}
            if emails:
                f(rel, i, "unexpected e-mail address", line)
            for m in re.finditer(r"\d{4}-\d{4}-\d{4}-\d{3}[\dX]", line):
                if m.group(0) != TONI_ORCID:
                    f(rel, i, "unexpected ORCID", line)
            if re.search(r"(Mihail|Mladenski)[^.;)]*orcid", line, re.I) and \
                    not re.search(r"no ORCID|ORCID: none|none \(no ORCID|has no ORCID|ORCID\s*\|?\s*none|no orcid|"
                                  r"not invented|not recorded|none is recorded|Mihail Mladenski\)", line, re.I):
                f(rel, i, "possible Mihail ORCID", line)
            if rel in author_files and re.search(SCHOOL, line, re.I) and \
                    not re.search(r"\bno\b|\bnot\b|none", line, re.I):
                f(rel, i, "educational institution in author metadata", line)
            if rel in author_files and re.search(CREDENTIAL, line):
                f(rel, i, "academic credential in author metadata", line)
            if not rel.endswith((".tex", ".bib")) and \
                    re.search(r"github\.com/eit-orbitos/[^\s)\"]*(CUBE|Cube|cube|PAPER3|Paper3)", line):
                f(rel, i, "invented Paper 3 repository URL", line)
    for rel, text in S.items():
        for par in re.split(r"\n\s*\n", text):
            fp = flat(par)
            for sent in re.split(r"(?<=[.;|])\s", fp):
                if re.search(r"Mihail|Mladenski", sent) and re.search(ROLE, sent) and not re.search(ROLE_EXEMPT, fp) \
                        and not re.search(r"context manager|\bmember\b of the (tree|archive|zip)", sent, re.I):
                    f(rel, 0, "corporate-role wording near Mihail Mladenski", sent)
    # ---- authorship metadata ----
    cff = S.get("CITATION.cff", "")
    blk = cff[cff.index("authors:"):cff.index("keywords:")] if "authors:" in cff else ""
    if re.search(AI_NAMES, blk):
        f("CITATION.cff", 0, "AI system listed as author", blk)
    people = re.findall(r"- family-names: (\S+)\n\s+given-names: (\S+)", blk)
    if people != [("Mladenovski", "Toni"), ("Mladenski", "Mihail")]:
        f("CITATION.cff", 0, "authors (exactly two, in order)", people)
    if blk.count(f'affiliation: "{AFF}"') != 2:
        f("CITATION.cff", 0, "affiliation", blk)
    tb, mb = (blk[:blk.index("Mladenski")], blk[blk.index("Mladenski"):]) if "Mladenski" in blk else ("", "")
    if TONI_ORCID not in tb or TONI_MAIL not in tb:
        f("CITATION.cff", 0, "Toni ORCID/e-mail", tb)
    if "orcid" in mb or MIHAIL_MAIL not in mb:
        f("CITATION.cff", 0, "Mihail ORCID must be absent, e-mail present", mb)
    z = json.loads(S.get(".zenodo.json", "{}") or "{}")
    names = [c.get("name", "") for c in z.get("creators", [])]
    if names != ["Mladenovski, Toni", "Mladenski, Mihail"]:
        f(".zenodo.json", 0, "creators", names)
    for c in z.get("creators", []):
        if c.get("affiliation") != AFF:
            f(".zenodo.json", 0, "affiliation", c)
        if c.get("name") == "Mladenski, Mihail" and "orcid" in c:
            f(".zenodo.json", 0, "Mihail ORCID must be absent", c)
        if c.get("name") == "Mladenovski, Toni" and c.get("orcid") != TONI_ORCID:
            f(".zenodo.json", 0, "Toni ORCID", c)
    if z.get("version") != "1.0.0":
        f(".zenodo.json", 0, "version", z.get("version"))
    ms = S.get("paper/manuscript.tex", "")
    am = re.search(r"\\author\{(.*?)\}\n", ms)
    byline = am.group(1) if am else ""
    if byline.count("$^{1") != 2 or "Toni Mladenovski$^{1,*}$" not in byline or \
            "Mihail Mladenski$^{1}$" not in byline or byline.index("Toni") > byline.index("Mihail") or \
            re.search(AI_NAMES + r"|Founder|Co-founder", byline):
        f("paper/manuscript.tex", 0, "byline (two authors, Toni corresponding, no titles)", byline)
    front = ms[:ms.index("\\begin{document}")]
    if AFF not in front:
        f("paper/manuscript.tex", 0, "affiliation in front matter", "")
    if TONI_MAIL not in front or TONI_ORCID not in front or TONI_MAIL2 in front or MIHAIL_MAIL in front:
        f("paper/manuscript.tex", 0, "corresponding-author line (primary e-mail and ORCID only)", "")
    if len(re.findall(r"\d{4}-\d{4}-\d{4}-\d{3}[\dX]", front.replace(TONI_ORCID, "T"))) != 0:
        f("paper/manuscript.tex", 0, "second ORCID in front matter", "")
    if TITLE not in flat(ms.replace("\\\\", " ")):
        f("paper/manuscript.tex", 0, "title", "")
    hs = flat(ms)
    if f"pdftitle={{{PDF_TITLE}}}" not in hs or f"pdfauthor={{{PDF_AUTHOR}}}" not in hs:
        f("paper/manuscript.tex", 0, "PDF document properties (pdftitle/pdfauthor)", "")
    if re.search(r"^version:\s*\"?1\.0\.0\"?\s*$", cff, re.M) is None:
        f("CITATION.cff", 0, "version 1.0.0", "")
    init = S.get("src/cube_bif/__init__.py", "")
    if '__version__ = "1.0.0"' not in init or f'STATUS = "{STATUS_V1}"' not in init:
        f("src/cube_bif/__init__.py", 0, "version/status", "")
    for rel in ("README.md", "CITATION.cff", "submission/COVER_LETTER_DRAFT.md",
                "submission/SUBMISSION_METADATA_SHEET.md"):
        if rel in S and "Symmetry-Breaking Bifurcations" not in S[rel]:
            f(rel, 0, "title missing", "")
    # ---- declarations (author-approved texts, verbatim; no approval flag left) ----
    dec_raw = S.get("paper/sections/13_declarations.tex", "")
    dec = flat(dec_raw)
    for head, need in (("Funding.", FUNDING), ("Competing interests.", CI_TEXT),
                       ("Author contributions.", CONTRIB_TEXT), ("Licences and copyright.", LIC_TEX)):
        if flat("\\paragraph{" + head + "} " + need) not in dec:
            f("paper/sections/13_declarations.tex", 0, f"approved text under \\paragraph{{{head}}} missing", need[:60])
    for rel in ("submission/DECLARATIONS.md", "AUTHOR_DECISION_V1.0.0.md"):
        dd = flat(S.get(rel, ""))
        for need, kind in ((FUNDING, "funding"), (CI_TEXT, "competing interests"), (CONTRIB_TEXT, "contributions"),
                           (LIC_TEXT, "licences and copyright")):
            if rel == "submission/DECLARATIONS.md" and kind == "licences and copyright":
                continue
            if flat(need) not in dd:
                f(rel, 0, kind + " text missing", need[:60])
    cl = flat(S.get("submission/COVER_LETTER_DRAFT.md", ""))
    if flat(CI_TEXT) not in cl or FUNDING not in cl:
        f("submission/COVER_LETTER_DRAFT.md", 0, "competing-interests / funding text", "")
    sheet = flat(S.get("submission/SUBMISSION_METADATA_SHEET.md", ""))
    if FUNDING not in sheet or flat(LIC_TEXT) not in sheet:
        f("submission/SUBMISSION_METADATA_SHEET.md", 0, "funding / licence text", "")
    for rel in ("LICENSE", "LICENSE-DOCS"):
        if "Copyright © 2026 EITNetworks LLC and the authors." not in S.get(rel, ""):
            f(rel, 0, "approved copyright notice", "")
    for rel in ("submission/COVER_LETTER_DRAFT.md", "RELEASE_NOTES_V1.0.0.md"):
        if rel in S and FUNDING.lower().rstrip(".") not in S[rel].lower():
            f(rel, 0, "funding sentence missing", "")
    for rel in ("AUTHORSHIP_FINAL_APPROVAL_REQUIRED.md", "submission/DECLARATIONS_DRAFT.md"):
        if (root / rel).exists():
            f(rel, 0, "superseded approval-hold file still present", "")
    for rel, text in S.items():
        if re.search(r"(?i)\bpublicly released\b|\bhas been (published|submitted|accepted)\b|"
                     r"\bis now (public|published)\b", text) and not re.search(r"(?i)not (yet )?(been )?", text):
            f(rel, 0, "public-release / publication claim", "")
    # ---- placeholders and bibliography ----
    allt = "\n".join(S.values())
    for ph in (GH_PLACEHOLDER, DOI_PLACEHOLDER):
        if ph not in allt:
            f("*", 0, "placeholder missing", ph)
    bib = S.get("paper/references.bib", "")
    keys = set(re.findall(r"@\w+\{([^,]+),", bib))
    cited = set()
    for rel, text in S.items():
        if rel.endswith(".tex"):
            for m in re.finditer(r"\\cite[pt]?\*?(?:\[[^\]]*\])*\{([^}]*)\}", text):
                cited.update(k.strip() for k in m.group(1).split(","))
    for k in sorted(keys - cited):
        f("paper/references.bib", 0, "uncited entry", k)
    for k in sorted(cited - keys):
        f("paper", 0, "undefined citation", k)
    return {"pass": not findings, "n_surfaces": len(S), "n_bib_entries": len(keys), "n_cited": len(cited),
            "findings": findings}


def main(argv):
    root = argv[1] if len(argv) > 1 else str(pathlib.Path(__file__).resolve().parents[1])
    res = scan(root)
    print("PASS" if res["pass"] else "FAIL", f"surfaces={res['n_surfaces']} bib={res['n_bib_entries']} "
          f"cited={res['n_cited']} findings={len(res['findings'])}")
    for x in res["findings"]:
        print(f"  {x['file']}:{x['line']} [{x['kind']}] {x['text']}")
    return 0 if res["pass"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
