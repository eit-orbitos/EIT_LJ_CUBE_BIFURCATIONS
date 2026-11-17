# FINAL BLIND RELEASE AUDIT — instructions for the independent auditor

Project: EIT-LJ Cube Bifurcations (Paper 3), release candidate **V1.0.0-rc2**.
Paper: *Symmetry-Breaking Bifurcations from the Cubic Equilibrium in Two-Term Inverse-Power Clusters*.
Authors: Toni Mladenovski and Mihail Mladenski (EITNetworks LLC, Tobyhanna, Pennsylvania, USA).
Status: RELEASE CANDIDATE · PENDING FINAL BLIND RELEASE AUDIT. FREEZE = NO · GitHub = HOLD · Zenodo = HOLD ·
Springer = HOLD · v1.0.0 tag = NOT CREATED.

This audit is to be performed by an auditor independent of the preparation of this release candidate. The preparing
agent has **not** performed it and does not claim any audit verdict. Work only from the archived artifacts supplied; do
not rely on any summary written by the authors or by the preparing agent (including `RELEASE_NOTES_RC2.md` and
`docs/QA_RESULTS_RC2.md`) as evidence. Report what you verified yourself, and mark anything you could not verify as
NOT_VERIFIED with the reason.

## Inputs (verify every hash first; stop and report if any differs)

| # | File | SHA-256 |
|---|---|---|
| 1 | `EIT_LJ_CUBE_BIFURCATIONS_V1.0.0-rc2.zip` (main archive) | in sidecar 2 and in manifest 8 |
| 2 | `EIT_LJ_CUBE_BIFURCATIONS_V1.0.0-rc2.zip.sha256` (sidecar) | — |
| 3 | `EIT_LJ_Paper3_manuscript_RC2.pdf` | in manifest 8 |
| 4 | `EIT_LJ_Paper3_source_RC2.zip` (LaTeX source, `manuscript.tex` at the ZIP root) | in manifest 8 |
| 5 | `EIT_LJ_CUBE_BIFURCATIONS_V0.4-dev.6.zip` (audited mathematical baseline) | `c473af60f8b54c0beecd252d9e8409eef734ba475c0d693b300946f57941b691` |
| 6 | `EIT_LJ_FULL_VECTOR_STABILITY_V1.0.zip` (Paper 2, frozen read-only input) | `bb70721df7f0aa17edca30d84d1b4aaf980c0a76693be14fa780e4ab8f64762d` |
| 7 | `EIT_LJ_CUBE_BIFURCATIONS_V1.0.0-rc1.zip` (previous candidate; for the metadata diff) | `33095d35107578054c7e54ff62be8a318ab973d7153e5c30d89da2fc9bc0361b` |
| 8 | `RC2_ARTIFACT_HASHES.sha256` (artifact hash manifest) | — |
| (opt.) | `EIT_LJ_Paper3_JMC_RC2_package.zip` (journal package draft, not submitted) | in manifest 8 |

The hashes in 2 and 8 were produced by the preparing agent; recompute every hash yourself. Then check the internal
manifest: `sha256sum -c SHA256SUMS` from the project root of the extracted main archive.

## Audit questions

1. **Artifact authenticity.** All input hashes; internal `SHA256SUMS`; the PDF and source ZIP correspond to
   `paper/` in the main archive (compare the source files byte for byte).
2. **dev.6 mathematical preservation (no new mathematics).** Run
   `python scripts/check_preservation_V1_0_0_rc2.py <dev.6 zip> . --rc1=<rc1 zip>` and, independently of that script,
   compare the trees yourself. Confirm that no file under `src/cube_bif/` (other than the version/status lines and
   docstring of `__init__.py`), `data/`, the pre-existing `scripts/` and `tests/` (other than `tests/test_docs.py`) or
   `audits/` changed, and that the historical B1 certificate keeps semantic SHA-256
   `616817fcc70e0fab7f106404e5e5332b17b9c4480bd440355f1ac5257a8518c6`. Optionally run
   `scripts/preservation_controls_V1_0_0_rc2.py <dev.6 zip> . --rc1=<rc1 zip>` and judge whether its forbidden edits
   are adequate.
3. **RC1 → RC2 difference.** Confirm that RC2 differs from RC1 only in metadata, authorship, affiliation,
   declarations, manuscript front matter/declarations/bibliography metadata, documentation, release tooling, release
   tests, checksums, status strings and packaging; that the historical RC1 records kept in the tree are byte-identical
   with RC1; and that every `src/`, `data/` and `audits/` file is byte-identical with RC1.
4. **Paper 2 read-only dependency.** Paper 2 is only read (by hash) and nothing of it is modified or redistributed.
5. **Certificate integrity.** Replay at least Lemma M and the bound P_A(q) < 16/5 (`scripts/run_A2.py`), the
   historical Lemma K certificate with the corrected checker and the corrected rebuild as corroboration only
   (`scripts/run_B1_erratum.py <scratch root>`), and Lemma Q (`scripts/run_B2_3.py`), on scratch copies. Check
   semantic hashes, endpoints and box covers (expected: Lemma M `49dce160…6a71e`, historical Lemma K `616817fc…8518c6`,
   corrected rebuild `b2f8e6dc…d505`, Lemma Q `f7bc244e…7d2`; Lemma Q lower bound 955723/262144). Do **not** run
   `scripts/run_B1.py` on the tree you audit: it would overwrite the historical certificate.
6. **Tests and controls.** With `EIT_LJ_PAPER2_ARCHIVE` (Paper 2 archive) and `EIT_LJ_DEV6_ARCHIVE` (dev.6 archive)
   set, run `python -m pytest -q tests` (0 skips are expected with both set; explain any skip), and as far as your
   resources allow the negative-control suites (`scripts/negative_controls*.py`). Check that no tolerance changed
   relative to dev.6 and that no post-hoc numerical tolerance is a proof dependency.
7. **Proof dependency structure.** Validate `data/A2_theorem_A_dependencies.json`, `data/B2_4_dependency_graph.json`,
   `data/B2_5_dependency_graph.json`: no cycles, no dangling dependencies, every leaf classified, no numerical
   corroboration reachable as a proof dependency, frozen Paper 2 inputs identified, and the classes exact / certified /
   standard / frozen kept distinct (`docs/THEOREM_DEPENDENCY_SUMMARY.md`). A read-only helper,
   `scripts/validate_dependency_graphs.py`, is provided; it treats the B2.5 input `IN_proposition_B2` as an in-paper
   result that is accepted only if the B2.4 graph itself validates. Judge that rule yourself and do not rely on the
   helper alone. Note: the graphs and other `data/` records are byte-identical to dev.6, so their embedded status
   strings (e.g. "PROVED (computer-assisted; not independently audited)") are the historical dev.6 wording; the
   current audit status is recorded in `docs/AUDIT_STATUS_MATRIX.json` and must be supported by the reports in `audits/`.
8. **Theorem ↔ manuscript consistency.** For every theorem, proposition, lemma and corollary in the manuscript, check
   that statement, hypotheses and status match the repository records (`NOTES.md`, `data/*`,
   `docs/AUDIT_STATUS_MATRIX.json`) and that no statement exceeds them. In particular: the A2u branches are two
   concentric regular tetrahedra of unequal radii on inversion-related vertex-direction sets (inversion exchanges the
   configurations x₊ and x₋); "supercritical" is tied to the reduced-energy convention; D3d transcriticality is derived
   by the implicit function theorem, not attributed to Ihrig–Golubitsky; Fix(D2h) = A1g ⊕ Eg ⊕ T2g⁽¹⁾ ⊕ T2g⁽²⁾; D2h
   configurations are not cuboids; H(WW) inertia (3, 0, 12); centre (1, 0, 2), slice (4, 0, 14) via Haynsworth
   additivity, R²⁴ (4, 6, 14); the D3d index comparison is a consistency check only; no A2u/Td full Morse index is
   claimed; no stability claim; the B1 erratum is disclosed and its closure stated correctly; the paper is local only.
9. **Audit-report integrity.** All six reports in `audits/` are byte-identical to the originals (`f82c5ef1…8b85`,
   `82bd4f21…65e5`, `ba482da0…6b74`, `841152f2…6bcf`, `0302930b…b1ec`, `bffd4948…165a`) and the statuses in
   `docs/AUDIT_STATUS_MATRIX.json` are supported by them — no more, no less.
10. **Bibliography.** Every entry is real, correctly described and cited; every citation resolves; no DOI is invented;
    Papers 1 and 2 are not presented as journal-published (`docs/REFERENCE_VERIFICATION.md`).
11. **Authorship and affiliation.** Exactly two human authors, Toni Mladenovski (corresponding; info@eitnetworks.org;
    ORCID 0009-0009-8343-662X) and Mihail Mladenski (mmladenski077@gmail.com in metadata; no ORCID), both
    "EITNetworks LLC, Tobyhanna, Pennsylvania, USA"; no sole-author wording; no educational institution, degree or
    invented credential; no invented contribution role for Mihail Mladenski; AI systems are not authors.
12. **Release metadata and stale claims.** `CITATION.cff`, `.zenodo.json`, README, submission drafts and release notes
    are consistent; placeholders `[PAPER 3 GITHUB RELEASE — TO BE ASSIGNED AFTER FINAL AUDIT]` and
    `[PAPER 3 ZENODO DOI — TO BE ASSIGNED AFTER FINAL AUDIT]` are used and no identifier is fabricated; no stale status
    or author strings on current surfaces (`scripts/check_release_text.py`, `scripts/scan_text_rc2.py`); no
    unsupported stability, global, novelty or technology/application claim.
13. **Packaging.** The source ZIP has `manuscript.tex` at its root and compiles from a clean extraction; the figures are
    regenerated deterministically by `paper/figures/make_figures.py`.

## Not in scope

New mathematics, A3, global T_d / D3d / D2h continuation, C2h branches, secondary bifurcations, Track C, and Paper 2
(read-only). Do not edit any file of the release candidate; report issues instead.

## Requested output

A report with: input hashes as verified; one verdict per audit question (PASS / PASS_WITH_NOTES / NEEDS_FIX /
NOT_VERIFIED) with evidence; a list of findings with severity (blocking / non-blocking); and an overall
recommendation (RELEASE-READY / NEEDS_FIX / BLOCK). The recommendation is advisory: freezing, tagging, publication on
GitHub or Zenodo and journal submission remain the authors' decisions and stay on HOLD until they decide. Human
authorship approvals (Mihail Mladenski's contribution statement, competing-interests wording) are submission items,
not mathematical defects.
