# Release notes — EIT-LJ Cube Bifurcations (Paper 3) V1.0.0-rc2

Paper title: **Symmetry-Breaking Bifurcations from the Cubic Equilibrium in Two-Term Inverse-Power Clusters**.

Status: **RELEASE CANDIDATE / V1.0.0-rc2 · PENDING FINAL BLIND RELEASE AUDIT**.
Holds: FREEZE = NO · GitHub = HOLD · Zenodo = HOLD · Springer submission = HOLD · v1.0.0 tag = NOT CREATED.
Nothing in this release candidate has been published, pushed, uploaded or submitted. The final blind release audit has
not been performed; this file does not report its outcome.

## Authors

| | Name | Affiliation | Contact | ORCID |
|---|---|---|---|---|
| 1 (corresponding) | Toni Mladenovski | EITNetworks LLC, Tobyhanna, Pennsylvania, USA | info@eitnetworks.org | 0009-0009-8343-662X |
| 2 | Mihail Mladenski | EITNetworks LLC, Tobyhanna, Pennsylvania, USA | mmladenski077@gmail.com | none |

No educational institution is listed for either author. No AI system is an author.

## Why RC2

Author and institution metadata were supplied after V1.0.0-rc1. RC2 records them. RC1 is kept unchanged (archive
`EIT_LJ_CUBE_BIFURCATIONS_V1.0.0-rc1.zip`, SHA-256
`33095d35107578054c7e54ff62be8a318ab973d7153e5c30d89da2fc9bc0361b`); its historical records (`RELEASE_NOTES_RC1.md`,
`docs/QA_RESULTS_RC1.*`, `docs/V1.0.0-rc1_PRESERVATION_*`, the RC1 preservation scripts) are carried byte-identically.

RC2 contains **no new mathematics**. The mathematics, certificates, proof records and their code are those of the
audited V0.4-dev.6 archive (`EIT_LJ_CUBE_BIFURCATIONS_V0.4-dev.6.zip`, SHA-256
`c473af60f8b54c0beecd252d9e8409eef734ba475c0d693b300946f57941b691`). The mechanical comparison is
`docs/V1.0.0-rc2_PRESERVATION_CHECK.md` (machine-readable `.json`); its forbidden-edit controls are in
`docs/V1.0.0-rc2_PRESERVATION_CONTROLS.json`.

## Changes relative to V1.0.0-rc1

- Authorship / affiliation: both authors EITNetworks LLC, Tobyhanna, Pennsylvania, USA (manuscript front matter,
  `CITATION.cff`, `.zenodo.json`, `README.md`, submission drafts); Mihail Mladenski's e-mail recorded in metadata; no
  ORCID for Mihail Mladenski; Toni Mladenovski the only corresponding author.
- Declarations: author-contribution wording (temporary, conservative), competing-interests draft, funding sentence
  ("This research received no external funding."), AI-use disclosure; `AUTHORSHIP_FINAL_APPROVAL_REQUIRED.md` added and
  `docs/AUTHOR_CONTRIBUTIONS_REVIEW_REQUIRED.md` (RC1) retired.
- Bibliography: two Crossref-confirmed DOIs added (Chechin et al. 2003; Schwerdtfeger and Wales 2024) and the page
  range of Chechin et al. completed; the self-reference to this package says rc2. See `docs/REFERENCE_VERIFICATION.md`.
- Version/status metadata: `src/cube_bif/__init__.py` (`__version__ = "1.0.0rc2"` and `STATUS` only).
- Documentation and status surfaces: `README.md`, `NOTES.md` (new §16; RC1 §15 kept as history), `CHANGELOG.md`
  (insert-only), `RESEARCH_LOG.md` (append-only), audit index, audit-status matrix, theorem dependency summary,
  AI-use log, reproducibility guide, `FINAL_AUDIT_INSTRUCTIONS.md`.
- Release tooling and tests of release metadata: `scripts/check_preservation_V1_0_0_rc2.py`,
  `scripts/preservation_controls_V1_0_0_rc2.py`, `scripts/scan_text_rc2.py`, `scripts/validate_dependency_graphs.py`
  (read-only proof-graph validator), `scripts/check_release_text.py` (updated); `tests/test_release_rc2.py`
  replaces `tests/test_release_rc1.py`; `tests/test_docs.py` updated.
- Checksums (`SHA256SUMS`) regenerated; packaging.

Unchanged byte-for-byte against both V0.4-dev.6 and RC1: every file under `src/cube_bif/` except `__init__.py`, every
file under `data/` (including the historical Lemma K certificate, semantic SHA-256
`616817fcc70e0fab7f106404e5e5332b17b9c4480bd440355f1ac5257a8518c6`, which remains authoritative; the corrected rebuild,
semantic SHA-256 `b2f8e6dcd1c5073635babea2f7a6079b7ede03acbbc4f33ac3cb20f64d21d505`, remains corroboration only),
every file under `audits/`, every pre-existing script and every test other than the release-metadata tests. The figures
regenerate byte-identically.

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
frozen Paper 2 block (3, 0, 12); transverse slice (4, 0, 14) — Morse index 4, nullity 0; R²⁴ (4, 6, 14), the six raw
zero modes being rigid motions. The D2h branch points are saddles; nothing in the package claims stability. The Morse
index of the D3d branches (only a consistency check) and the full Morse index of the A2u/Td branch are not results of
Paper 3. Global continuation, secondary bifurcations, C2h, A3, global energy barriers and any application are outside
the paper.

The independent audits were performed by AI systems on the authors' instruction. They are archived verbatim in
`audits/` and are not journal peer review.

## Author-side verification

See `docs/QA_RESULTS_RC2.md` (machine-readable `docs/QA_RESULTS_RC2.json`): full test suite, certificate replays,
deterministic regeneration of proof records, all negative-control suites, proof-dependency-graph validation, figure
regeneration, preservation check and its forbidden-edit controls, text scans (`docs/V1.0.0-rc2_TEXT_SCAN.md`) and a
clean manuscript build from the source archive. These are author-side checks; they do not replace the final blind
release audit.

## Funding

This research received no external funding.

## Licences

Software: PolyForm Noncommercial License 1.0.0 (`LICENSE`). Manuscript, documentation, figures, generated results and
package-authored metadata: CC BY-NC-SA 4.0 (`LICENSE-DOCS`). Commercial use only by separate written agreement where
applicable. Audit reports in `audits/` are reproduced verbatim as records.

## Open items

1. FINAL BLIND RELEASE AUDIT of this release candidate (`FINAL_AUDIT_INSTRUCTIONS.md`) — not yet performed; it is the
   only permitted next step.
2. HUMAN AUTHORSHIP APPROVAL REQUIRED BEFORE SPRINGER SUBMISSION: FINAL AUTHOR CONTRIBUTION APPROVAL REQUIRED BEFORE
   SPRINGER SUBMISSION (Mihail Mladenski's detailed contribution statement; `AUTHORSHIP_FINAL_APPROVAL_REQUIRED.md`).
   This is not a mathematical defect.
3. Competing-interests wording: FINAL AUTHOR APPROVAL REQUIRED BEFORE SPRINGER SUBMISSION.
4. Copyright-holder wording in `LICENSE` / `LICENSE-DOCS`: FINAL AUTHOR APPROVAL REQUIRED BEFORE FINAL RELEASE.
5. Public identifiers: `[PAPER 3 GITHUB RELEASE — TO BE ASSIGNED AFTER FINAL AUDIT]`,
   `[PAPER 3 ZENODO DOI — TO BE ASSIGNED AFTER FINAL AUDIT]`.
