# PAPER 3 RC2 — FINAL BLIND RELEASE AUDIT

**Project:** EIT-LJ Cube Bifurcations (Paper 3)  
**Release candidate:** V1.0.0-rc2  
**Paper:** *Symmetry-Breaking Bifurcations from the Cubic Equilibrium in Two-Term Inverse-Power Clusters*  
**Audit date:** 2026-11-16  
**Audit type:** fresh standalone computational release audit from the supplied archived artifacts  
**Overall recommendation:** **RELEASE-READY**, subject to the explicit human and publication holds below

## 1. Scope, independence of evidence, and decision

This report audits **Paper 3 RC2**, not Paper 2 and not Theorem 4′ of Paper 2. It does not reuse the old Paper 2 `REVIEWER_REPORT.md`, and it does not convert any earlier phase audit into a release verdict.

The audit followed `FINAL_AUDIT_INSTRUCTIONS.md`. Work was performed on clean extractions and disposable scratch copies. No release-candidate file was edited. `RELEASE_NOTES_RC2.md` and `docs/QA_RESULTS_RC2.md` were not used as audit evidence. All integrity, preservation, certificate, test, dependency-graph, bibliography, build, figure, and visual checks reported below were rerun or independently inspected during this audit.

The recommendation is an advisory computational release audit, not journal peer review and not a human authorship approval. It supports proceeding to the authors’ release decisions; it does not itself freeze, tag, publish, upload, or submit anything.

### Decision summary

| Item | Result |
|---|---|
| Audit questions passed | 7 `PASS`; 6 `PASS_WITH_NOTES`; 0 `NEEDS_FIX`; 0 `NOT_VERIFIED` |
| Blocking findings | **None** |
| Non-blocking findings | 6 documentation, metadata, approval, and reproducibility notes |
| Mathematical/certificate changes required | **None** |
| Manuscript/source/package mismatch | **None** |
| Tests | **479/479 passed; 0 skipped, failed, or errored** |
| Negative controls | **130/130 behaved as required** |
| Clean source build | **30 A4 pages; 30 references; 3 figures; 7 tables** |
| Deterministic figures | **3/3 PDFs and `figure_data.json` byte-identical** |
| Overall | **RELEASE-READY** |

## 2. Verified input artifacts

The following hashes were recomputed from the actual supplied files. Duplicate dev.6 uploads were byte-identical.

| Artifact | Verified SHA-256 |
|---|---|
| `EIT_LJ_CUBE_BIFURCATIONS_V1.0.0-rc2(1).zip` | `6dee0be5f975d23fce3a36770ddebad8041aae9e3f302df0cd923fad91481a08` |
| `EIT_LJ_CUBE_BIFURCATIONS_V1.0.0-rc2.zip(1).sha256` | `7f39b894ff365e95f4097af0006eef1ecaffe8287a7bf0ceb9afc0b549d7ffea` |
| `EIT_LJ_Paper3_manuscript_RC2(1).pdf` | `674509e9f055dd2e8b28ea908fcd724bda23060d619369e07d74c4d5941bf334` |
| `EIT_LJ_Paper3_source_RC2(1).zip` | `5626fb5e440b67612a85a692646e94c36272716dbca95df5e8e3146fe49c5164` |
| `EIT_LJ_CUBE_BIFURCATIONS_V0.4-dev.6(2).zip` | `c473af60f8b54c0beecd252d9e8409eef734ba475c0d693b300946f57941b691` |
| `EIT_LJ_CUBE_BIFURCATIONS_V0.4-dev.6(3).zip` | `c473af60f8b54c0beecd252d9e8409eef734ba475c0d693b300946f57941b691` |
| `EIT_LJ_CUBE_BIFURCATIONS_V1.0.0-rc1(1).zip` | `33095d35107578054c7e54ff62be8a318ab973d7153e5c30d89da2fc9bc0361b` |
| `EIT_LJ_Paper3_JMC_RC2_package.zip` | `d002d5e875d79bfbc4b6211b1fc99a192ef5910145f75709504684884d41fd00` |
| `EIT_LJ_FULL_VECTOR_STABILITY_V1.0(4).zip` (Paper 2, read-only) | `bb70721df7f0aa17edca30d84d1b4aaf980c0a76693be14fa780e4ab8f64762d` |
| Corrected `RC2_ARTIFACT_HASHES.sha256` used as authority | `f96a88d339effd42bac895c28ae7aef169068521a17b38bcd4599e596db96628` |
| Superseded uploaded `RC2_ARTIFACT_HASHES(1).sha256` | `e276a441c61d7e85fa4880d16984e0a4f99ce195d2457cc6148c3b7d184eeec3` |

The uploaded `e276…` manifest was stale and contained the obsolete JMC value `4be4…`. It was not used to authenticate the release. The corrected `f96a…` manifest records the actual JMC hash `d002…`; all **22/22** entries in that corrected manifest were recomputed and passed. This discrepancy is a non-blocking input-management note, not a defect in the RC2 payload.

## 3. Audit questions 1–7

### Question 1 — Artifact authenticity

**Verdict: PASS_WITH_NOTES**

Evidence:

- Every required payload hash matched the sidecar, the controlling expected hashes, or the corrected external manifest, as applicable.
- The main archive’s internal `SHA256SUMS` passed **191/191** entries.
- The corrected external artifact manifest passed **22/22** entries.
- The standalone source archive and the main archive’s `paper/` tree shared **23 source files**, all byte-identical. `manuscript.bbl` was correctly identified as source-archive-only build support, not a missing main-tree source file.
- `manuscript.tex` is at the source ZIP root.
- The JMC package’s PDF and source ZIP are byte-identical to the standalone supplied PDF and source ZIP.
- The JMC package’s internal checksum file passed all **10/10** payload entries.

Note: the superseded uploaded external manifest is documented in Section 2. The corrected manifest authenticates the actual artifacts without altering any candidate payload.

### Question 2 — dev.6 mathematical preservation

**Verdict: PASS_WITH_NOTES**

The supplied preservation checker was run against the authenticated dev.6 and RC1 archives:

```text
PASS {'ADDED': 67, 'CHANGED': 8, 'IDENTICAL': 117}
```

An independent tree comparison, not relying on that checker’s classifications, found the same eight changed pre-existing files:

- `CHANGELOG.md`
- `NOTES.md`
- `README.md`
- `RESEARCH_LOG.md`
- `SHA256SUMS`
- `audits/README.md`
- `src/cube_bif/__init__.py`
- `tests/test_docs.py`

There were 67 added files, zero removed files, and 117 identical files. Independent checks established:

- every protected mathematical source, data record, certificate, numerical record, dependency graph, pre-existing script/test other than the documented documentation-test exception, and historical audit report is byte-identical to dev.6;
- `src/cube_bif/__init__.py` differs only in its module docstring and the `__version__`/`STATUS` metadata, verified by parsing the valid Python and masking only those fields;
- `audits/README.md` is an insert-only index: every old line remains in order, and all six historical reports are byte-identical;
- no tolerance or proof-bearing numerical record changed;
- the historical Lemma K certificate retains semantic SHA-256 `616817fcc70e0fab7f106404e5e5332b17b9c4480bd440355f1ac5257a8518c6`.

The forbidden-edit controls passed their unmodified baseline and rejected **60/60** forbidden edits. Their coverage includes protected source, data, scripts, tests, certificates, graphs, and historical reports.

Note: the instruction’s literal phrase “every file under `audits/`” needs to be read together with its permission for new audit records. The actual exceptions are precisely the metadata-only `__init__.py` and insert-only audit index; neither is a mathematical change.

### Question 3 — RC1 → RC2 difference

**Verdict: PASS_WITH_NOTES**

The independent RC1/RC2 comparison found:

| Category | Count |
|---|---:|
| Added | 14 |
| Removed | 2 |
| Changed | 27 |
| Identical | 151 |

The only removed RC1 files were:

- `docs/AUTHOR_CONTRIBUTIONS_REVIEW_REQUIRED.md`
- `tests/test_release_rc1.py`

These are superseded release-documentation/tooling items, not mathematical deletions. The changes are confined to metadata, authorship/affiliation and declarations, manuscript front matter and bibliography metadata, documentation, release tooling/tests, checksums, status strings, and packaging. Historical RC1 records retained in RC2 are byte-identical. Protected mathematical source, data, and historical audit reports remain unchanged.

The two precise exceptions to a literal “every `src/` and `audits/` file byte-identical” reading are the same permitted metadata-only `src/cube_bif/__init__.py` update and insert-only `audits/README.md` update described under Question 2. They are non-blocking and contain no new mathematics.

### Question 4 — Paper 2 read-only dependency

**Verdict: PASS**

- The authenticated Paper 2 archive hash remained `bb70721df7f0aa17edca30d84d1b4aaf980c0a76693be14fa780e4ab8f64762d` throughout.
- RC2 contains no Paper 2 ZIP and no redistributed named Paper 2 payload.
- Its reference directory contains only `reference/PAPER2_INPUTS.md`, which identifies the frozen input by hash.
- Tests and certificate checks accessed Paper 2 through the external archive environment variable.
- No Paper 2 file, repository, release, or Zenodo record was modified or redistributed.

### Question 5 — Certificate integrity

**Verdict: PASS**

All replays used fresh scratch copies. `scripts/run_B1.py` was not run on the audited tree.

| Certificate/check | Independently observed result | Semantic SHA-256 |
|---|---|---|
| Lemma M and `P_A(q)<16/5` | 64 boxes; maximum depth 6; minimum lower bound `161457/262144`; `P_A` bound true; independent checker passed with no failures | `49dce160b2a17a9f61554200617b9a75b5b02e244e21963b5956317156b6a71e` |
| Historical Lemma K, corrected checker | 222 boxes; Newton 222/222; carrier 222/222; endpoints accepted; no failures; historical bytes unchanged | `616817fcc70e0fab7f106404e5e5332b17b9c4480bd440355f1ac5257a8518c6` |
| Corrected Lemma K rebuild | Corrected checker passed; Newton/carrier 222/222; identical endpoint records; corroboration only, not a replacement | `b2f8e6dcd1c5073635babea2f7a6079b7ede03acbbc4f33ac3cb20f64d21d505` |
| Taylor-free B2.3 cross-check of B1 curve | 222/222 curve balls passed; blocked B1 modules were not imported | Not a new certificate of record |
| Lemma Q | 222 boxes; minimum lower bound `955723/262144`; independent check passed; no failures; method controls 15/15 | `f7bc244ecac4b89ce003a38ff52047d6cbe80f63a97236049f15f5e0da5c17d2` |

The Lemma Q endpoint enclosures were independently reproduced as approximately `3.7993380378668858` at `q=0` and `4.3770354906131219` at the corner. The B1 erratum remains closed on the stated evidence: the historical certificate is accepted by the corrected checker, the corrected rebuild is corroboration only, and the Taylor-free route independently accepts all curve balls.

### Question 6 — Tests and negative controls

**Verdict: PASS**

Tests ran on a scratch tree with authenticated Paper 2, dev.6, and RC1 archives supplied through their environment variables. The batches were:

| Batch | Result |
|---|---:|
| Mathematical/exact tests | 342 passed |
| Lemma M/Lemma Q certificate tests | 74 passed |
| B1 certificate/erratum tests | 43 passed |
| Documentation/release tests | 20 passed |
| **Total** | **479 passed; 0 skipped** |

Fresh negative-control execution gave:

| Suite | Required detection behavior |
|---|---:|
| Main mutation suite | 34/34 detected |
| B2.2 | 9/9 detected |
| B2.3 | 24/24 detected |
| B2.4 | 22/22 detected |
| B2.5 | 28/28 detected |
| B1 erratum | 12/12 detected directly; the thirteenth was detected by the separate erratum tests exactly as designed |
| **Total** | **130/130 behaved as required** |

Chunk summaries for B2.4/B2.5 report chunk counts rather than full-suite totals; aggregation by the actual result records gives 22/22 and 28/28. The final two B2.3 chunks each reported 4/4 detections.

No tolerance changed relative to dev.6 because all proof-bearing code and data are byte-preserved. The disclosed widened numerical-corroboration threshold is confined to a non-proof numerical check; dependency-graph inspection confirmed that neither it nor any other numerical corroboration is reachable as a proof dependency.

### Question 7 — Proof dependency structure

**Verdict: PASS**

The supplied validator and an independent structural checker were applied to all three graphs:

| Graph | Nodes | Edges |
|---|---:|---:|
| Theorem A | 35 | 39 |
| Proposition B2 | 13 | 22 |
| Proposition B3/Corollary B3′ | 17 | 31 |

Independently verified properties:

- acyclicity;
- no dangling dependencies;
- every node reachable from a declared root;
- declared root-to-leaf sets equal to computed sets;
- every proof leaf classified;
- exact, certified, standard, frozen, and established-in-paper classes kept distinct;
- frozen Paper 2 inputs explicitly identified;
- consistency and numerical-corroboration items excluded from proof reachability.

The B2.5 roots are `P_B3` and `C_B3`. `IN_proposition_B2` is acceptable only as an established in-paper input because the B2.4 graph independently validates; it is not treated as an unclassified external assumption. Embedded dev.6 status strings remain historical wording, while current status is correctly carried by `docs/AUDIT_STATUS_MATRIX.json`.

## 4. Audit questions 8–13

### Question 8 — Theorem ↔ manuscript consistency

**Verdict: PASS**

Every theorem-like environment in the manuscript was enumerated and checked against the repository records, proof graphs, certificates, and current audit-status matrix. The required claim boundaries are preserved:

- **Theorem A:** the `A2u` branches are two concentric regular tetrahedra of unequal radii on inversion-related vertex-direction sets. Spatial inversion exchanges the complete configurations `x+` and `x−`; it does not exchange the unequal shells within one fixed configuration.
- “Supercritical” is explicitly tied to the reduced-energy convention and its one-dimensional reduced-potential minima/maxima, not full-space stability.
- **Proposition B1:** `D3d` transcriticality follows from the analytic implicit function theorem using `κ≠0` and `τ≠0`. Ihrig–Golubitsky is discussed only as related generic-instability context and is not used to infer branch type.
- **Proposition B2:** `Fix(D2h) = A1g ⊕ Eg ⊕ T2g^(1) ⊕ T2g^(2)`, with one fixed direction from each summand. The fixed-space proof and the non-cuboid argument agree; `D2h` configurations are expressly not cuboids.
- **Corollary B3′ complement:** `H_WW` has inertia `(3,0,12)`, with the negative `A2u` and two `Eu` directions derived rather than assumed.
- **Proposition B3:** centre inertia is `(1,0,2)`, hence centre index 1 and nullity 0, identically on all six conjugate `D2h` branch points.
- **Corollary B3′:** rigid-motion-reduced slice inertia is `(4,0,14)` by Haynsworth additivity `(3,0,12)+(1,0,2)`; raw `R^24` inertia is `(4,6,14)`, with six rigid zero modes.
- The `D3d` centre-index calculation and local-degree sum are explicitly labelled a sign-consistency check, not a result of the paper.
- No full Morse index is claimed for the `A2u/Td` branches, and no `D3d` branch Morse index is promoted to a theorem.
- No stability claim is made. Statements that the `D2h` points are saddles follow from their positive Morse index and are not represented as stability.
- Erratum E-B1 accurately describes the series-cap/zero-padding defect, the invalidity of the original near-diagonal implementation as written, the unchanged historical certificate, corrected-checker acceptance, corroborating rebuild, Taylor-free cross-check, and closure without changing Lemma K or Proposition B1.
- All branch results remain local, with no uniform radius in `q`, no endpoint branch claim, no global continuation, no secondary-bifurcation claim, and no technology/application claim.

The abstract, summary table, discussion, figures/captions, appendices, `.zenodo.json`, and README remain within these same boundaries.

### Question 9 — Audit-report integrity

**Verdict: PASS**

All six historical reports are byte-identical to their required originals:

| Report | Verified SHA-256 |
|---|---|
| `CUBE_BIFURCATIONS_REVIEWER_REPORT.md` | `f82c5ef1a03c33c0909313bd6442d1879d39717f991cc8e245eb0c61f75d8b85` |
| `CUBE_BIFURCATIONS_V03_REVIEWER_REPORT.md` | `82bd4f21630a20481113702a9f49dddfa6327f2baf3c07a131af259c1baa65e5` |
| `CUBE_BIFURCATIONS_V04_DEV4_B1_ERRATUM_REAUDIT.md` | `ba482da06aa0492b6524e47680fd949170f4d0dafac0d5661a073efce4d46b74` |
| `CUBE_BIFURCATIONS_V05_BLIND_B23_LEMMA_Q_REVIEWER_REPORT.md` | `841152f2cccd0a43c4f8e73ce5d0cf37e9793d26f12047d5143ea5a053e96bcf` |
| `CUBE_BIFURCATIONS_V05_BLIND_B24_REVIEWER_REPORT.md` | `0302930b9a96ac6bca3df4e720ba34ab5937f73944aee76ba85f345706bdb1ec` |
| `CUBE_BIFURCATIONS_V04_DEV6_BLIND_B25_REVIEWER_REPORT.md` | `bffd4948721ee62f6898336734670ee51381caf546cdd69e0a2ad810e37f165a` |

The status matrix claims no more than these reports support:

- Track A: Lemma M, Corollary M, Theorem A independently audited; the later B1 report confirms the two Track A documentation corrections without changing the mathematics.
- B1: Lemma K and Proposition B1 independently audited, with the targeted erratum re-audit supporting “ERRATUM CLOSED.”
- B2.3: Lemma Q independently audited.
- B2.4: Proposition B2 independently audited.
- B2.5: Proposition B3 and Corollary B3′ independently audited, including centre/slice/raw inertia and the no-stability boundary.

`audits/README.md` is only an index and is not counted as a seventh mathematical audit report. This final release audit is separate from all six phase audits.

### Question 10 — Bibliography

**Verdict: PASS**

- The bibliography contains **30 entries**; independent citation-key extraction found **30 cited keys**, with no undefined or uncited entry.
- All **25 DOI-bearing entries** were independently resolved through DOI content negotiation. Title, year, and available first-author/volume/page metadata were compared.
- Apparent title mismatches were benign registry-format differences: subtitles stored separately for Fousse, Kielhöfer, and Krantz–Parks; series-volume suffixes for Milnor; abbreviated book titles for the two Golubitsky volumes; TeX/MathML markup for Arjevani–Field; and the explicitly disclosed difference between Paper 2’s manuscript title and its Zenodo software-record title. Article-number `Art. 13` versus `13` is the same MPFR article identifier.
- The five entries without DOIs are two real books, two software records with resolving official URLs, and Paper 3’s own deliberately placeholder-only release-candidate citation. The Tucker and Wilson–Decius–Cross bibliographic details were independently corroborated; the python-flint and mpmath official URLs returned successfully.
- DataCite classifies Paper 1 as **Preprint** and Paper 2 as **Software**. The manuscript correctly describes them as a Zenodo preprint and public archive/repository release, not journal publications.
- No DOI or Paper 3 public identifier is invented. The clean BibTeX build produced 30 `\bibitem` entries with no undefined citation.

### Question 11 — Authorship and affiliation

**Verdict: PASS_WITH_NOTES**

Current surfaces consistently identify exactly two human authors:

1. **Toni Mladenovski**, corresponding author, `info@eitnetworks.org`, ORCID `0009-0009-8343-662X`;
2. **Mihail Mladenski**, submission metadata email `mmladenski077@gmail.com`, no ORCID.

Both have the affiliation **EITNetworks LLC, Tobyhanna, Pennsylvania, USA**. The manuscript byline, `CITATION.cff`, `.zenodo.json`, README, submission metadata, and declarations agree. No sole-author wording, educational institution, academic degree, invented credential, or invented ORCID was found. AI systems are expressly tools and not authors.

Mihail Mladenski is confirmed as co-author, but no specific scholarly contribution or CRediT role is invented for him. The temporary contribution wording says only that his detailed statement will be finalized and approved by the authors.

Non-blocking human items remain explicitly open: Mihail Mladenski’s detailed contribution wording, competing-interests wording, and copyright-holder wording. The first two block Springer submission; copyright wording blocks final release. They are not mathematical or certificate defects and were not silently treated as approved.

### Question 12 — Release metadata and stale claims

**Verdict: PASS_WITH_NOTES**

- `scripts/check_release_text.py` returned `PASS surfaces=44 bib=30 cited=30 findings=0`.
- `scripts/scan_text_rc2.py` returned `PASS`; all matches were classified as current justified text, historical record, verbatim audit report, audited code/record, generated scan record, or release-tooling pattern.
- `CITATION.cff`, `.zenodo.json`, README, release drafts, submission drafts, manuscript declarations, and bibliography consistently identify RC2 as pending final blind release audit, not frozen or published.
- The required placeholders remain exactly:
  - `[PAPER 3 GITHUB RELEASE — TO BE ASSIGNED AFTER FINAL AUDIT]`
  - `[PAPER 3 ZENODO DOI — TO BE ASSIGNED AFTER FINAL AUDIT]`
- No Paper 3 GitHub release URL, Zenodo DOI, final tag, submission claim, stability claim, global claim, unsupported novelty claim, or technology/application claim was found on a current surface.
- Historical documents and verbatim audits retain their historical wording and are not misrepresented as current release status.

Note: “pending final blind release audit” is the correct status of the audited RC2 artifact itself. This report supplies the requested audit verdict but does not rewrite the candidate or automatically authorize a status transition.

### Question 13 — Packaging, clean build, and deterministic figures

**Verdict: PASS_WITH_NOTES**

Packaging and build evidence:

- The source ZIP has `manuscript.tex` at its root.
- A clean extraction compiled successfully with Tectonic, including a fresh BibTeX pass.
- The build produced **30 A4 pages**, **30 bibliography entries**, **3 figures**, and **7 tables**.
- There were no undefined references, undefined citations, fatal errors, or missing manuscript content.
- The supplied PDF is also 30 A4 pages. Every page was rendered to an image and inspected on contact sheets covering pages 1–10, 11–20, and 21–30. No clipping, overlap, blank unintended page, missing figure/table, corrupted glyph, or other visual release defect was found.
- The draft JMC package retains its intended 10 payload files plus checksum manifest, and all payload checksums passed. Its PDF/source ZIP match the standalone artifacts byte-for-byte.

Using the recorded `matplotlib 3.11.2` in isolated scratch space, `paper/figures/make_figures.py` regenerated all outputs byte-identically:

| Output | SHA-256 |
|---|---|
| `fig1_parameter_plane.pdf` | `ae3f9d9346ae13054837141f9d1c6fd393b9adacd9e73dc89dbf193bef932269` |
| `fig2_modes.pdf` | `f9fc5b1265cfd646750a0eb8216a488eb8a58c64522588393aa58c6cf39740ed` |
| `fig3_bifurcation_diagrams.pdf` | `6f86791683243ab07ba181922cfee63964e8b87987b245943033055297d2f48f` |
| `figure_data.json` | `9fb10b064c93e87f4ca3c6946d9521b7b647d01c412622c2efbebf0224ca0ed2` |

Non-blocking notes:

- The supplied PDF’s document-property **Title** and **Author** fields are blank. The visible manuscript title, byline, affiliation, corresponding-author email, and ORCID are present and correct. This is a document-metadata improvement, not a mathematical or packaging failure.
- The clean build reported two very small overfull boxes, `0.15236 pt` and `0.91545 pt`, plus cosmetic float/`hyperref`/engine notices. Visual inspection found no resulting visible defect.
- Byte-deterministic figure reproduction depends on the recorded plotting version; using that version succeeds exactly. This is an environment requirement, not nondeterminism in the archived generator.

## 5. Findings and severity

### Blocking findings

**None.**

No mathematical, certificate, dependency, theorem-wording, authenticity, test, bibliography, authorship, packaging, or visual defect requiring an RC2 correction was found.

### Non-blocking findings

| ID | Severity | Finding | Required handling |
|---|---|---|---|
| NB-01 | Non-blocking | The uploaded `e276…` external manifest was stale and listed obsolete JMC hash `4be4…`. | Use only corrected manifest `f96a…`, whose 22 entries all pass and whose JMC value is `d002…`; do not reuse the stale values. |
| NB-02 | Non-blocking | Literal checklist wording could be read as forbidding the metadata-only `__init__.py` and insert-only `audits/README.md` changes. | Interpret with the expressly permitted release metadata/new audit records; both exceptions were independently verified and contain no mathematics. |
| NB-03 | Non-blocking for release audit; blocking for later human steps | Mihail Mladenski’s contribution wording, competing-interests wording, and copyright-holder wording await human approval. | Close only through explicit author approval, in the required sequence; do not infer approval from this report. |
| NB-04 | Non-blocking | Supplied PDF document-property Title and Author fields are blank. | Optionally populate in a future metadata-only manuscript rebuild; visible title/byline are correct. |
| NB-05 | Non-blocking | Two sub-point overfull boxes and cosmetic TeX notices remain. | No correction required; all 30 pages were visually inspected and are sound. |
| NB-06 | Non-blocking | Figure bytes vary with plotting-library versions. | Retain and use the recorded `matplotlib 3.11.2` for byte-identical regeneration. |

## 6. Release recommendation and holds

Paper 3 RC2 satisfies the supplied final-audit checklist. The dev.6 mathematics and historical audit records are preserved; RC1→RC2 changes are release/metadata work; Paper 2 remains read-only; all required certificates replay with their expected semantic hashes; all tests and controls behave as required; proof dependencies are structurally sound; manuscript claims remain local and within the audited results; bibliography and authorship metadata are consistent; and the source, figures, PDF, and draft journal package reproduce and inspect cleanly.

Accordingly, the release candidate is recommended **RELEASE-READY** with the non-blocking notes above.

This verdict does **not** perform or authorize any of the following by itself:

- **FREEZE = NO**
- **GitHub = HOLD**
- **Zenodo = HOLD**
- **Springer submission = HOLD**
- **FINAL v1.0.0 TAG = NOT CREATED**

No file was pushed, published, uploaded, tagged, frozen, or submitted during this audit. The three human approvals remain open and must follow a valid release-ready audit rather than being treated as completed by it. Final freezing, tagging, publication, identifier assignment, and journal submission remain separate author decisions.

FINAL BLIND RELEASE AUDIT: RELEASE-READY