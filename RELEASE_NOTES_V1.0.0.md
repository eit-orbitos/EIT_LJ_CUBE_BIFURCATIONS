# Release notes — EIT-LJ Cube Bifurcations (Paper 3) V1.0.0

Paper title: **Symmetry-Breaking Bifurcations from the Cubic Equilibrium in Two-Term Inverse-Power Clusters**.

Status at build time: **FINAL RELEASE PREPARED / V1.0.0 · PENDING RC2→V1.0.0 DELTA AUDIT**.
FINAL BLIND RELEASE AUDIT (of V1.0.0-rc2): **RELEASE-READY**. HUMAN APPROVALS: CLOSED.
**PUBLIC RELEASE: NOT YET EXECUTED.** FREEZE = NO (pending the delta audit) · GitHub = HOLD · Zenodo publish = HOLD ·
Springer/JMC submission = HOLD · v1.0.0 public tag = NOT CREATED.

At the time this package was built nothing had been published, pushed, uploaded, tagged or submitted, and no Zenodo
DOI had been reserved. The next step is only the independent RC2 → V1.0.0 delta/preservation audit
(`FINAL_V1_DELTA_AUDIT_INSTRUCTIONS.md`); a public release requires that audit's PASS and explicit author
authorization.

## Authors

| | Name | Affiliation | Contact | ORCID |
|---|---|---|---|---|
| 1 (corresponding) | Toni Mladenovski | EITNetworks LLC, Tobyhanna, Pennsylvania, USA | info@eitnetworks.org | 0009-0009-8343-662X |
| 2 | Mihail Mladenski | EITNetworks LLC, Tobyhanna, Pennsylvania, USA | mmladenski077@gmail.com | none |

No educational institution is listed for either author. No AI system is an author. Toni Mladenovski is Founder of
EITNetworks LLC; no corporate role is stated for Mihail Mladenski, whose EITNetworks LLC affiliation is a scientific
affiliation (author correction recorded in `AUTHOR_DECISION_V1.0.0.md`).

## What V1.0.0 is

V1.0.0-rc2 (archive `EIT_LJ_CUBE_BIFURCATIONS_V1.0.0-rc2.zip`, SHA-256
`6dee0be5f975d23fce3a36770ddebad8041aae9e3f302df0cd923fad91481a08`) passed the final blind release audit with verdict
RELEASE-READY and no blocking finding. The report is archived verbatim as
`audits/PAPER3_RC2_FINAL_BLIND_RELEASE_AUDIT.md` (SHA-256
`37b0b4d68f4675b4546f7313aca6937c51cdf1ee11d1cc20b528918e636d7448`); it was supplied by the author as the Kimi audit and
is a computational release verification, not journal peer review.

The authors then approved the final author-contribution, competing-interests and copyright-holder texts, closing the
human-approval hold (NB-03 of that audit). A same-day author correction removed the "Co-founder" label for Mihail
Mladenski and replaced the competing-interests wording accordingly, before this package was built.

V1.0.0 therefore differs from RC2 **only** in declarations, metadata, version/status, PDF document properties, audit
index/status records, release notes and tooling, tests of release metadata, checksums and packaging. **No new
mathematics was introduced.** The mathematical baseline remains the audited V0.4-dev.6
(`EIT_LJ_CUBE_BIFURCATIONS_V0.4-dev.6.zip`, SHA-256
`c473af60f8b54c0beecd252d9e8409eef734ba475c0d693b300946f57941b691`). RC1 and RC2 archives are kept unchanged; their
records inside this tree are carried byte-identically as history.

## Changes relative to V1.0.0-rc2

- **Approved declarations** (verbatim, `\paragraph{…}` headings in `paper/sections/13_declarations.tex`;
  `submission/DECLARATIONS.md`, which replaces `submission/DECLARATIONS_DRAFT.md`; cover letter; metadata sheet):
  - Competing interests: "Toni Mladenovski is Founder of EITNetworks LLC. Both authors are affiliated with EITNetworks
    LLC. Software associated with this work is released under a noncommercial license, with commercial use available
    only by separate written agreement. The research received no external funding."
  - Author contributions: "Toni Mladenovski conceived the study, established the research direction, oversaw the
    mathematical development and analysis, prepared and reviewed the manuscript, and takes responsibility for the
    scientific claims. Mihail Mladenski contributed to the conceptualization, structural framing, definition
    refinement, and analytical discussions throughout the development of the study, and reviewed and approved the
    final manuscript."
  - Licences and copyright: "Software: PolyForm Noncommercial License 1.0.0. Manuscript, documentation, figures,
    generated results and package-authored metadata: CC BY-NC-SA 4.0. Commercial use only by separate written
    agreement. Copyright © 2026 EITNetworks LLC and the authors." (also `LICENSE`, `LICENSE-DOCS`, `CITATION.cff`,
    `.zenodo.json`; the external licence instruments are referenced, not altered).
  - Funding: "This research received no external funding."
  - The temporary approval flags and `AUTHORSHIP_FINAL_APPROVAL_REQUIRED.md` are removed from the current surfaces;
    `AUTHOR_DECISION_V1.0.0.md` records the author decision and the correction.
- **Version/status:** `src/cube_bif/__init__.py` (`__version__ = "1.0.0"`, `STATUS`, docstring only); manuscript
  version line; `CITATION.cff`, `.zenodo.json`.
- **PDF document properties** (RC2 audit item NB-04): `\hypersetup{pdftitle=…, pdfauthor={Toni Mladenovski; Mihail
  Mladenski}}`.
- **Audit records:** final blind release audit report archived verbatim; `docs/AUDIT_INDEX.md`,
  `docs/AUDIT_STATUS_MATRIX.*`, `audits/README.md` (insert-only) updated.
- **Placeholders:** `[PAPER 3 GITHUB RELEASE — TO BE ASSIGNED AT PUBLIC RELEASE]` and
  `[PAPER 3 ZENODO DOI — TO BE ASSIGNED AT PUBLIC RELEASE]`; no identifier was invented and no DOI was reserved
  (ZENODO DOI RESERVATION NOT PERFORMED: no authenticated Zenodo access in the preparation environment).
- **Documentation:** `README.md`, `NOTES.md` (new §17; §16 marked historical), `CHANGELOG.md` (insert-only),
  `RESEARCH_LOG.md` (append-only), AI-use log, reproducibility guide, reference verification, dependency summary,
  `docs/GITHUB_RELEASE_V1.0.0.md` (prepared tag message, release description and asset list; not used yet).
- **Release tooling and tests:** `scripts/check_preservation_V1_0_0.py`, `scripts/preservation_controls_V1_0_0.py`,
  `scripts/scan_text_v1.py`, `scripts/check_release_text.py` (updated); `tests/test_release_v1.py` replaces
  `tests/test_release_rc2.py`; `tests/test_docs.py` status tests updated.
- **Checksums** (`SHA256SUMS`) regenerated; packaging.

Byte-identical with both V0.4-dev.6 and RC2: every file under `src/cube_bif/` except `__init__.py`, every file under
`data/` (including the historical Lemma K certificate, semantic SHA-256
`616817fcc70e0fab7f106404e5e5332b17b9c4480bd440355f1ac5257a8518c6`, which remains authoritative; the corrected rebuild,
semantic SHA-256 `b2f8e6dcd1c5073635babea2f7a6079b7ede03acbbc4f33ac3cb20f64d21d505`, remains corroboration only), every
earlier audit report, `reference/`, every pre-existing script and mathematical test, and every scientific section,
appendix and figure of the manuscript. See `docs/V1.0.0_PRESERVATION_CHECK.md`.

## Statuses (unchanged)

| Result | Status | Audit |
|---|---|---|
| Track A: Lemma M | CERTIFIED | INDEPENDENTLY AUDITED |
| Track A: Corollary M, Theorem A | PROVED (computer-assisted) | INDEPENDENTLY AUDITED |
| B1: Lemma K | CERTIFIED | INDEPENDENTLY AUDITED · ERRATUM CLOSED |
| B1: Proposition B1 | CERTIFIED (computer-assisted) | INDEPENDENTLY AUDITED · ERRATUM CLOSED |
| B2.3: Lemma Q (global carrier lower bound 955723/262144) | CERTIFIED | INDEPENDENTLY AUDITED |
| B2.4: Proposition B2 | PROVED (computer-assisted) | INDEPENDENTLY AUDITED |
| B2.5: Proposition B3, Corollary B3′ | PROVED (computer-assisted) | INDEPENDENTLY AUDITED |

D2h branch inertia (negative, zero, positive): centre space (1, 0, 2) — centre Morse index 1, nullity 0; complementary
frozen Paper 2 block (3, 0, 12); rigid-motion-reduced slice (4, 0, 14) — Morse index 4, nullity 0; R²⁴ (4, 6, 14), the
six raw zero modes being rigid motions. The D2h branch points are saddles; nothing in the package claims stability. The
Morse index of the D3d branches (only a consistency check) and the full Morse index of the A2u/Td branch are not results
of Paper 3. Global continuation, secondary bifurcations, C2h, A3 and global energy barriers are outside the
paper, and no application is claimed.

## Author-side verification

See `docs/QA_RESULTS_V1.0.0.md` (machine-readable `.json`): full test suite, certificate replays, deterministic
regeneration of proof records, all negative-control suites, proof-dependency-graph validation, figure regeneration,
preservation check against V0.4-dev.6 and RC2 with its forbidden-edit controls, text scans
(`docs/V1.0.0_TEXT_SCAN.md`) and a clean manuscript build from the source archive. These are author-side checks; they do
not replace the delta audit.

## Funding

This research received no external funding.

## Open items

1. RC2 → V1.0.0 delta/preservation audit (`FINAL_V1_DELTA_AUDIT_INSTRUCTIONS.md`) — pending; the only next step.
2. After its PASS and explicit author authorization only: freeze, GitHub push/tag/release, Zenodo publication (the real
   DOI then replaces the placeholders), Springer/JMC submission. None of these is authorized by this package.

No scientific or human-approval blocker remains open.
