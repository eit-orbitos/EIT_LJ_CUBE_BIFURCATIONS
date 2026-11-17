# Release notes — EIT-LJ Cube Bifurcations (Paper 3) V1.0.0-rc1

Status: **RELEASE CANDIDATE / V1.0.0-rc1 · PENDING FINAL BLIND RELEASE AUDIT**.
Holds: FREEZE = NO · GitHub = HOLD · Zenodo = HOLD · Springer submission = HOLD · tag v1.0.0 NOT CREATED.
Nothing in this release candidate has been published, pushed, uploaded or submitted.

Authors: Toni Mladenovski and Mihail Mladenski (EITNetworks LLC).
Corresponding author: Toni Mladenovski, info@eitnetworks.org, ORCID 0009-0009-8343-662X.

## What this release candidate is

V1.0.0-rc1 is a packaging, audit-status and manuscript release candidate. It contains **no new mathematics**. The
mathematics, certificates, proof records and their code are those of the audited V0.4-dev.6 archive
(`EIT_LJ_CUBE_BIFURCATIONS_V0.4-dev.6.zip`, SHA-256
`c473af60f8b54c0beecd252d9e8409eef734ba475c0d693b300946f57941b691`). The mechanical comparison is in
`docs/V1.0.0-rc1_PRESERVATION_CHECK.md`; the forbidden-edit controls of that comparison are in
`docs/V1.0.0-rc1_PRESERVATION_CONTROLS.json`.

Scope of the paper: local bifurcation theory from the cubic equilibrium only — the A2u pitchfork (Track A), the T2g
cubic and quartic invariants, the D3d transcritical branches, the D2h pitchfork, and the centre and full-slice Morse
index on the D2h branches. Excluded: A3, global T_d continuation, C2h branches, Track C, T1u, any 8×8+1 or computing
application, and any claim of stability.

## Statuses recorded in this release candidate

| Result | Status | Audit |
|---|---|---|
| Track A: Lemma M | CERTIFIED | INDEPENDENTLY AUDITED |
| Track A: Corollary M, Theorem A | PROVED (computer-assisted) | INDEPENDENTLY AUDITED |
| B1: Lemma K | CERTIFIED | INDEPENDENTLY AUDITED · ERRATUM CLOSED |
| B1: Proposition B1 | CERTIFIED (computer-assisted) | INDEPENDENTLY AUDITED · ERRATUM CLOSED |
| B2.3: Lemma Q | CERTIFIED | INDEPENDENTLY AUDITED |
| B2.4: Proposition B2 | PROVED (computer-assisted) | INDEPENDENTLY AUDITED |
| B2.5: Proposition B3, Corollary B3′ | PROVED (computer-assisted) | INDEPENDENTLY AUDITED |

D2h branch inertia (negative, zero, positive): centre space (1, 0, 2) — centre Morse index 1, nullity 0; transverse
slice (4, 0, 14) — slice Morse index 4, nullity 0; R²⁴ (4, 6, 14), the six raw zero modes being rigid motions. No
statement implies stability. Axial curvature, centre index and slice index are separate quantities.

The independent audits were performed by AI systems on the author's instruction; they are not journal peer review.

## Changes relative to V0.4-dev.6

- Added the three B2 audit reports verbatim (`audits/`; SHA-256 `841152f2…`, `0302930b…`, `bffd4948…`).
- Updated status surfaces only: `README.md`, `NOTES.md` (status lines and a new §15), `CHANGELOG.md` (insert-only),
  `RESEARCH_LOG.md` (append-only), `audits/README.md` (insert-only), `src/cube_bif/__init__.py` (version
  `1.0.0rc1` and `STATUS` only), `tests/test_docs.py` (status test), `SHA256SUMS` (regenerated).
- Added: manuscript (`paper/`), JMC submission drafts (`submission/`), audit index, audit-status matrix, theorem
  dependency summary, AI-use log, reproducibility guide, reference verification, author-contribution review file,
  QA record, preservation report and controls, `CITATION.cff`, `.zenodo.json`, `LICENSE`, `LICENSE-DOCS`, release
  tooling (`scripts/check_preservation_V1_0_0_rc1.py`, `scripts/preservation_controls_V1_0_0_rc1.py`,
  `scripts/check_release_text.py`) and `tests/test_release_rc1.py`.
- Unchanged byte-for-byte: every file under `src/cube_bif/` except `__init__.py`, every file under `data/`
  (including the historical B1 certificate, semantic SHA-256 `616817fc…8518c6`), every pre-existing script and test
  except `tests/test_docs.py`, every earlier audit report, and every earlier identity-check document.

## Verification performed for this release candidate

See `docs/QA_RESULTS_RC1.md` (machine-readable: `docs/QA_RESULTS_RC1.json`): full test suite, deterministic
regeneration of proof records, certificate replays, all negative-control suites, preservation check and its
forbidden-edit controls, release-text scan and a clean manuscript build. These are the author-side checks; they do not
replace the final blind release audit.

## Licences

Software: PolyForm Noncommercial License 1.0.0 (`LICENSE`). Manuscript, documentation, figures, data and metadata:
CC BY-NC-SA 4.0 (`LICENSE-DOCS`). Commercial use only by separate written agreement. Audit reports in `audits/` are
reproduced verbatim as records.

## Open items before any release or submission

1. FINAL BLIND RELEASE AUDIT of this release candidate (`FINAL_AUDIT_INSTRUCTIONS.md`) — not yet performed.
2. AUTHOR CONTRIBUTION DETAILS REQUIRED FOR MIHAIL MLADENSKI BEFORE FINAL SUBMISSION
   (`docs/AUTHOR_CONTRIBUTIONS_REVIEW_REQUIRED.md`).
   No ORCID or e-mail is recorded for the second author; none has been supplied and none is invented.
3. AUTHOR INPUT REQUIRED — official EITNetworks LLC institutional city.
4. Competing-interests statement: FINAL AUTHOR REVIEW REQUIRED.
5. GitHub release and Zenodo DOI: `[PAPER 3 GITHUB RELEASE — TO BE ASSIGNED AFTER FINAL AUDIT]`,
   `[PAPER 3 ZENODO DOI — TO BE ASSIGNED AFTER FINAL AUDIT]`.
