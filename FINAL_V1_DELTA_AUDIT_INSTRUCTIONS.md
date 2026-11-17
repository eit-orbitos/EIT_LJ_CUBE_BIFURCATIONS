# Final RC2 → V1.0.0 delta/preservation audit — instructions for the independent auditor

Project: EIT-LJ Cube Bifurcations (Paper 3), "Symmetry-Breaking Bifurcations from the Cubic Equilibrium in Two-Term
Inverse-Power Clusters". Authors: Toni Mladenovski (corresponding) and Mihail Mladenski, EITNetworks LLC, Tobyhanna,
Pennsylvania, USA.

Status of the package under audit: **FINAL RELEASE PREPARED / V1.0.0 · PENDING RC2→V1.0.0 DELTA AUDIT**. Public release
not executed. The auditor must **not** publish, push, tag, upload or submit anything, and must not edit the package.
Work from the archived artefacts, not from summaries (including this file and the release notes).

## Inputs (authenticate each by SHA-256 before use; stop on any mismatch)

| # | File | SHA-256 |
|---|---|---|
| 1 | `EIT_LJ_CUBE_BIFURCATIONS_V1.0.0.zip` (+ `.sha256` sidecar) | see `V1_ARTIFACT_HASHES.sha256` (delivered alongside) |
| 2 | `EIT_LJ_Paper3_manuscript_V1.0.0.pdf` | see `V1_ARTIFACT_HASHES.sha256` |
| 3 | `EIT_LJ_Paper3_source_V1.0.0.zip` | see `V1_ARTIFACT_HASHES.sha256` |
| 4 | `EIT_LJ_Paper3_JMC_V1.0.0_package.zip` | see `V1_ARTIFACT_HASHES.sha256` |
| 5 | `EIT_LJ_CUBE_BIFURCATIONS_V1.0.0-rc2.zip` (audited RC2) | `6dee0be5f975d23fce3a36770ddebad8041aae9e3f302df0cd923fad91481a08` |
| 6 | `EIT_LJ_CUBE_BIFURCATIONS_V0.4-dev.6.zip` (mathematical baseline) | `c473af60f8b54c0beecd252d9e8409eef734ba475c0d693b300946f57941b691` |
| 7 | `EIT_LJ_FULL_VECTOR_STABILITY_V1.0.zip` (Paper 2, read-only) | `bb70721df7f0aa17edca30d84d1b4aaf980c0a76693be14fa780e4ab8f64762d` |
| 8 | `PAPER3_RC2_FINAL_BLIND_RELEASE_AUDIT.md` | `37b0b4d68f4675b4546f7313aca6937c51cdf1ee11d1cc20b528918e636d7448` |
| 9 | `RC2_ARTIFACT_HASHES.sha256` (corrected RC2 manifest) | `f96a88d339effd42bac895c28ae7aef169068521a17b38bcd4599e596db96628` |

Note on input 9: the corrected RC2 manifest used during preparation was reconstructed from the earlier RC2 manifest by
replacing the superseded JMC-package and README entries; the reconstructed file matched the required SHA-256 exactly
and all 22 of its entries verified. The superseded manifest (`e276…`) and JMC hash (`4be4…`) were not used.

## What to verify

1. **Authenticity:** recompute every hash above and in `V1_ARTIFACT_HASHES.sha256`; check the sidecar; check the
   internal `SHA256SUMS` of the V1.0.0 archive against its files.
2. **Delta is restricted:** list every file that differs between RC2 and V1.0.0 (independently, e.g. by extracting
   both archives and comparing bytes). Each difference must be one of: approved human statements, version/status
   metadata, copyright-notice metadata, PDF document properties, release notes, audit index/status, release tooling,
   tests of release metadata, checksums, packaging. Removed files may only be `AUTHORSHIP_FINAL_APPROVAL_REQUIRED.md`,
   `submission/DECLARATIONS_DRAFT.md` and `tests/test_release_rc2.py` (all kept in RC2). The author-side comparison is
   `docs/V1.0.0_PRESERVATION_CHECK.md` and `scripts/check_preservation_V1_0_0.py` — reproduce it, do not trust it.
3. **No mathematical change:** every file under `src/` (except `src/cube_bif/__init__.py`, which may change only its
   docstring, `__version__` and `STATUS`), `data/` and `reference/` is byte-identical with both RC2 and V0.4-dev.6; no
   certificate, semantic hash, proof dependency graph, numerical proof record or interval bound changed; every
   scientific manuscript section (01–11), appendix and figure is byte-identical with RC2.
4. **Audit reports:** all six earlier reports are byte-identical (hashes in `docs/AUDIT_INDEX.md`); the final blind
   release audit report is archived byte-identically (`37b0b4d6…7448`).
5. **Tests and replays:** run the full suite with the Paper 2, dev.6 and RC2 archives available
   (`EIT_LJ_PAPER2_ARCHIVE`, `EIT_LJ_DEV6_ARCHIVE`, `EIT_LJ_RC2_ARCHIVE`); expected 0 failures, 0 skips. Replay the
   certificates (Lemma M `49dce160…6a71e`; historical Lemma K `616817fc…8c6`; corrected Lemma K corroboration
   `b2f8e6dc…d505`; Lemma Q `f7bc244e…17d2`, lower bound 955723/262144) and the negative controls (130 mutations as
   required, 86 baselines). Validate the three proof DAGs.
6. **Declarations match the author-approved texts exactly** (see `AUTHOR_DECISION_V1.0.0.md`, which also records the
   same-day correction): competing interests, author contributions, licences and copyright, funding — in the
   manuscript (`\paragraph{…}` headings), `submission/DECLARATIONS.md`, the cover letter and the metadata sheet. No
   temporary approval flag remains on a current surface.
7. **Authorship and affiliation:** exactly two human authors in order; both EITNetworks LLC, Tobyhanna, Pennsylvania,
   USA; ORCID only for Toni Mladenovski (0009-0009-8343-662X); Mihail Mladenski's e-mail mmladenski077@gmail.com in
   metadata, no ORCID; no educational institution, credential or degree; **no corporate role stated for Mihail
   Mladenski** (no "Co-founder", owner, member, employee or manager) on any current surface; Toni Mladenovski's role
   "Founder" only where relevant (competing interests, metadata).
8. **PDF:** build the manuscript from a clean extraction of the source ZIP (`manuscript.tex` at its root); compare the
   visible text with the delivered PDF; check the PDF document properties Title and Author.
9. **Identifiers:** no GitHub release URL, Zenodo DOI or arXiv identifier for Paper 3 exists or is invented; only the
   controlled placeholders appear. No Zenodo DOI was reserved; if one is claimed anywhere, treat it as a finding.
10. **Claims:** no public-release, publication, acceptance or submission claim; no stability, global or technology
    claim; Papers 1 and 2 described as Zenodo records only.

## Expected outcome

If every check passes, the expected recommendation is **`V1.0.0 FREEZE AUTHORIZED`** — a recommendation to the
authors only. Freeze, GitHub push/tag/release, Zenodo publication and Springer/JMC submission remain the authors'
separate, explicit decisions; the auditor performs none of them.
