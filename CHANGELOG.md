# Changelog — EIT-LJ Cube Bifurcations (Paper 3)

All versions are private research versions: not frozen, not published, no public repository.

## V1.0.0 — 2026-11-16 — final release prepared: author-approved declarations and final metadata (no new mathematics)

Status at build time: **FINAL RELEASE PREPARED / V1.0.0 · PENDING RC2→V1.0.0 DELTA AUDIT**. V1.0.0-rc2 passed the final blind release audit (RELEASE-READY;
`audits/PAPER3_RC2_FINAL_BLIND_RELEASE_AUDIT.md`). Human approvals CLOSED (`AUTHOR_DECISION_V1.0.0.md`). Public release
not yet executed; FREEZE = NO (pending the delta audit) · GitHub = HOLD · Zenodo publish = HOLD · Springer/JMC submission = HOLD · v1.0.0 public tag = NOT CREATED. RC1 and RC2 are kept unchanged. Paper 2 is untouched and used read-only.

- **Declarations:** author-approved competing-interests, author-contribution and copyright texts inserted verbatim
  (manuscript `\paragraph` headings, `submission/DECLARATIONS.md` replacing `submission/DECLARATIONS_DRAFT.md`,
  `LICENSE`, `LICENSE-DOCS`, `CITATION.cff`, `.zenodo.json`); temporary approval flags removed from current surfaces;
  `AUTHOR_DECISION_V1.0.0.md` replaces `AUTHORSHIP_FINAL_APPROVAL_REQUIRED.md`.
- **Author correction (corporate role):** the "Co-founder" label for Mihail Mladenski is removed from every current
  surface (he is not a co-founder, owner, member, employee or manager of EITNetworks LLC; no other title replaces it);
  his scientific affiliation EITNetworks LLC, Tobyhanna, Pennsylvania, USA is unchanged. The competing-interests text
  is the corrected author-approved wording ("Toni Mladenovski is Founder of EITNetworks LLC. Both authors are
  affiliated with EITNetworks LLC. …"), in the manuscript, `submission/DECLARATIONS.md`, the cover letter and
  `AUTHOR_DECISION_V1.0.0.md`. Earlier RC1/RC2 records keep the wording supplied at that time.
- **Version/status:** `1.0.0`, `FINAL RELEASE PREPARED / V1.0.0 · PENDING RC2→V1.0.0 DELTA AUDIT`; manuscript version line; PDF Title/Author document properties.
- **Audit records:** final blind release audit report archived byte-identically; audit index, status matrix and
  `audits/README.md` (insert-only) updated.
- **Placeholders:** public identifiers renamed to `[PAPER 3 GITHUB RELEASE — TO BE ASSIGNED AT PUBLIC RELEASE]` and `[PAPER 3 ZENODO DOI — TO BE ASSIGNED AT PUBLIC RELEASE]`; no identifier invented.
- **Release tooling:** `scripts/check_preservation_V1_0_0.py`, `scripts/preservation_controls_V1_0_0.py`,
  `scripts/scan_text_v1.py`, updated `scripts/check_release_text.py`; `tests/test_release_v1.py` replaces
  `tests/test_release_rc2.py`; `tests/test_docs.py` status tests updated. RC1 and RC2 records kept as historical.
- **No mathematical change:** every `src/` file except `__init__.py`, every `data/` file and every earlier audit report
  byte-identical with V0.4-dev.6 and RC2 (`docs/V1.0.0_PRESERVATION_CHECK.md`).

## V1.0.0-rc2 — 2026-11-16 — release candidate: author/institution metadata update (no new mathematics)

Status: **RELEASE CANDIDATE / V1.0.0-rc2 · PENDING FINAL BLIND RELEASE AUDIT**. FREEZE = NO; GitHub, Zenodo and
Springer submission on HOLD; v1.0.0 tag NOT CREATED. RC1 is kept unchanged. Paper 2 is untouched and used read-only.

- **Authors and affiliation:** both authors EITNetworks LLC, Tobyhanna, Pennsylvania, USA (manuscript front matter,
  `CITATION.cff`, `.zenodo.json`, README, submission drafts, `src/cube_bif/__init__.py` docstring). Mihail Mladenski's
  e-mail recorded (mmladenski077@gmail.com); he has no ORCID and none is recorded. No educational institution listed.
- **Declarations:** competing-interests factual draft and temporary author-contribution wording, each flagged for final
  author approval; funding sentence unchanged. New `AUTHORSHIP_FINAL_APPROVAL_REQUIRED.md` replaces
  `docs/AUTHOR_CONTRIBUTIONS_REVIEW_REQUIRED.md`.
- **Version/status:** `1.0.0rc2`, `RELEASE CANDIDATE / V1.0.0-rc2 · PENDING FINAL BLIND RELEASE AUDIT`.
- **Bibliography metadata:** Crossref-confirmed DOIs added to Chechin et al. 2003 (with full page range) and
  Schwerdtfeger–Wales 2024; every DOI re-resolved (`docs/REFERENCE_VERIFICATION.md`).
- **Release tooling:** `scripts/check_preservation_V1_0_0_rc2.py`, `scripts/preservation_controls_V1_0_0_rc2.py`,
  `scripts/scan_text_rc2.py`, updated `scripts/check_release_text.py`; `tests/test_release_rc2.py` replaces
  `tests/test_release_rc1.py`; `tests/test_docs.py` status test updated. RC1 records kept as historical.
- **No mathematical change:** every `src/` file except `__init__.py` and every `data/` file byte-identical with
  V0.4-dev.6 (`docs/V1.0.0-rc2_PRESERVATION_CHECK.md`).

## V1.0.0-rc1 — 2026-11-15 — release candidate: audit-status patch, manuscript and release metadata (no new mathematics)

Status: **RELEASE CANDIDATE / V1.0.0-rc1 · PENDING FINAL BLIND RELEASE AUDIT**. FREEZE = NO; GitHub, Zenodo and
Springer submission on HOLD; no v1.0.0 tag. Paper 2 is untouched and used read-only.

- **Audits recorded:** the B2.3 (Lemma Q), B2.4 (Proposition B2) and B2.5 (Proposition B3, Corollary B3′) blind
  reports by Kimi Agent, each formal verdict PASS with no finding requiring correction, copied byte-identically into
  `audits/` (SHA-256 `841152f2…6bcf`, `0302930b…b1ec`, `bffd4948…165a`). Lemma Q: CERTIFIED · INDEPENDENTLY AUDITED.
  Propositions B2, B3 and Corollary B3′: PROVED (computer-assisted) · INDEPENDENTLY AUDITED. Audited inertia (negative,
  zero, positive): centre (1, 0, 2), slice (4, 0, 14), R²⁴ (4, 6, 14); no stability claim.
  Resolved: the NOT_PROVIDED note of V0.4-dev.6 (the B2.3/B2.4 reports are now in the package).
- **Authors:** Toni Mladenovski (Founder, EITNetworks LLC; corresponding) and Mihail Mladenski (Co-founder, EITNetworks
  LLC). Mihail Mladenski's contribution statement, ORCID/e-mail (if required) and the company city (if required) are
  not invented; they are listed as open author items (`docs/AUTHOR_CONTRIBUTIONS_REVIEW_REQUIRED.md`).
- **Status surfaces:** `src/cube_bif/__init__.py` (version 1.0.0rc1, status, docstring), README, NOTES (header, §0,
  status labels of §9, §12, §13 and "at that version"/"when written" markers on historical status sentences, new §15),
  `audits/README.md`, `tests/test_docs.py`. No mathematical statement changed.
- **Manuscript:** `paper/` (LaTeX source, 13 sections, 4 appendices, bibliography, three deterministic vector figures,
  `paper/tools/check_appendix_closed_forms.py`).
- **Release metadata (prepared, not published):** `CITATION.cff`, `.zenodo.json`, `RELEASE_NOTES_RC1.md`,
  `FINAL_AUDIT_INSTRUCTIONS.md`, `LICENSE` (PolyForm Noncommercial 1.0.0), `LICENSE-DOCS` (CC BY-NC-SA 4.0),
  `docs/AI_USE_LOG.md`, `docs/REPRODUCIBILITY.md`, `docs/AUDIT_INDEX.md`, `docs/AUDIT_STATUS_MATRIX.{json,md}`,
  `docs/THEOREM_DEPENDENCY_SUMMARY.md`, `docs/REFERENCE_VERIFICATION.md`, `submission/` (JMC drafts, not submitted).
- **Preservation:** `scripts/check_preservation_V1_0_0_rc1.py` and `scripts/preservation_controls_V1_0_0_rc1.py`
  compare against V0.4-dev.6; `scripts/check_release_text.py` scans for stale status strings, authorship errors and
  claim language; `tests/test_release_rc1.py`. Results: `RELEASE_NOTES_RC1.md` and
  `docs/V1.0.0-rc1_PRESERVATION_CHECK.md`.
- **Kept byte-identical by design:** every mathematical source module, certificate, proof record, dependency graph,
  numerical record, earlier script, earlier audit report and earlier identity-check document. The `status` strings
  inside proof records and the status constants in `b2_branch.py`/`b2_index.py` therefore still read "not
  independently audited"; the current statuses are in `docs/AUDIT_STATUS_MATRIX.json`.

## V0.4-dev.6 — 2026-11-15 — B2.5: Proposition B3 (centre-manifold index of the D2h branch) and Corollary B3′

B2.5 only. No global branch problem, no A3, no C2h secondary-branch study; Paper 2 is untouched; nothing is frozen,
published, pushed or uploaded (GitHub and Zenodo on hold).

**Input statuses (NOTES §13):** the author's request designates B2.3 and B2.4 as independently audited. No audit report
for B2.3 or B2.4 is in this package (NOT_PROVIDED), so §9 and §12 keep their labels; Proposition B3's status does not
depend on that label.

**B2.5 (NOTES §13):** Proposition B3 and Corollary B3′ — PROVED (computer-assisted; not independently audited).
- Reduced potential on the critical T2g space E_c: V_red = V₀ + ½λ|a|² + κa₁a₂a₃ + α|a|⁴ + βΣa_k⁴ + O(|a|⁵). The
  invariant dimensions (0, 1, 1, 2, 1, 3 in degrees 1–6) are computed; the complete quartic after LS elimination is
  derived exactly for a generic pair potential, and α + β = c₄/24.
- Hessian on the axis has the exact form [[h₁₁, 0, 0], [0, d, e], [0, e, d]]; on the branch h₁₁ = (c₄/3)s² + O(s⁴)
  = −2τμ + O(μ²), d = −4βs² + O(s⁴), e = κs + O(s³), det = −κ²s² + O(s⁴). No O(s) diagonal term.
- Explicit remainder bound: the transverse eigenvalues d ± e have opposite signs for 0 < |s| < |κ|/(C_D + C_E).
  Centre index 1, nullity 0, independent of the gauge sign of κ and of s ↔ −s; all six conjugate branch points have
  one index type. Analytic given the inputs; no explicit radius; no interval certificate in B2.5.
- Corollary B3′: m_⊥ = 3 (A2u + Eu) derived from Paper 2's Theorem (index) block signs, constant on the physical
  curve; full-slice index 4, nullity 0; in R²⁴ inertia (4, 6, 14) with the 6 rigid modes excluded. No stability claim.
- D3d consistency check (not a theorem): centre index 2 (μ > 0) and 1 (μ < 0); local degree −3 on both sides.
- Dependency graph (machine-readable, validated): Proposition B3 rests only on the exact O_h/T2g structure, Lemma K,
  Proposition B2 and standard LS/centre-manifold theory; Corollary B3′ adds the named Paper 2 spectral result. No
  numerical scan is a proof dependency.
- Numerical corroboration (raw 24-D Hessian, 60 digits): q = 0.2, 0.8, 1.5, 2.0; μ/P_T = 10⁻⁵, 10⁻⁶, 10⁻⁷; both signs
  of s: 300/300 checks, after one recorded tolerance change (NOTES §13.8).
- Tests and controls: 71 new tests in `tests/test_B2_index.py` (23 false Proposition B3 statements, 11 false Corollary B3′ statements and 12 invalid graphs rejected); code-mutation controls 28/28 detected (15 target tests, each passing unmutated); full suite 469 collected, 469 passed, 0 skipped (run in chunks, with the Paper 2 archive beside the project; without it the 3 archive cross-checks are skipped). The earlier control suites (34, 9, 24, 13, 22) were not re-run: every file they mutate or test, and their records, is byte-identical with V0.4-dev.5.
- Identity check against V0.4-dev.5: PASS; 62/62 forbidden modifications rejected (the 44 dev.5 controls plus 18 for B2.4 files, earlier reports, audits/README.md, NOTES §11–§12, the CHANGELOG dev.5 entry, version values, an extra file and a stale manifest).

**Changed files:** `src/cube_bif/__init__.py` (version/status), `tests/test_docs.py` (three documentation tests
replaced, one added), `NOTES.md` (header, §0 sentence, new §13–§14; §1–§12 byte-identical), `README.md`,
`CHANGELOG.md`, `RESEARCH_LOG.md` (appended), `SHA256SUMS`. **Added:** `src/cube_bif/b2_index.py`,
`tests/test_B2_index.py`, `scripts/run_B2_5.py`, `scripts/negative_controls_B2_5.py`,
`scripts/check_identity_V0_4_dev6.py`, `scripts/identity_controls_V0_4_dev6.py`, `data/B2_5_index.json`,
`data/B2_5_dependency_graph.json`, `data/B2_5_negative_controls.json`, `data/B2_5_identity_controls.json`,
`docs/V0.4-dev.6_IDENTITY_CHECK.md`.

## V0.4-dev.5 — 2026-11-14 — B1 erratum closed; B2.4: Proposition B2 (the D2h-axial pitchfork)

B2.5 is not started; Paper 2 is untouched; nothing is frozen, published, pushed or uploaded.

**Audit status (NOTES §11):** the targeted independent re-audit of erratum E-B1 (Kimi Agent, 2026-11-14, PASS) is
added byte-identical as `audits/CUBE_BIFURCATIONS_V04_DEV4_B1_ERRATUM_REAUDIT.md` (SHA-256
ba482da06aa0492b6524e47680fd949170f4d0dafac0d5661a073efce4d46b74; provenance in `audits/README.md`).
B1 status: **CERTIFIED · INDEPENDENTLY AUDITED · ERRATUM CLOSED**. No B1 file changes.

**B2.4 (NOTES §12):** Proposition B2 — PROVED (computer-assisted; not independently audited).
- Reduced equation on the D2h axis: V_red = V₀(μ) + ½λ(μ)s² + (c₄/24)s⁴ + O(s⁶, μs⁴, μ²s²), even in s, λ(0) = 0,
  λ′(0) = τ < 0, c₄ > 0; ∂_sV_red = s·G(s², μ), G = λ(μ) + (c₄/6)z + O(z², μz, μ²).
- Implicit function theorem: μ*′(0) = −c₄/(6τ) > 0, s² = −(6τ/c₄)μ + O(μ²); the nontrivial pair ±s* exists only for
  μ > 0 (p > P_T(q)), derived from the signs.
- Z₂-symmetric pitchfork (exchanged by the 8 elements of N(Σ) ∖ Σ), supercritical in the energy-reduced axial
  convention; axial reduced curvature τμ < 0 at the cube (μ > 0) and −2τμ > 0 at ±s*. One-dimensional axial
  statement only: no centre-manifold index, no full-space stability.
- Geometry: isotropy exactly Σ (D2h); not in the cuboid family Fix(Z₂³); rhombic (sheared) cross-sections and the
  opposite tetrahedral translation at first order; O(s²) corrections in span{Â, Ê}; f₁ component O(s³).
- Proof dependency graph (machine-readable, validated): its leaves are exactly the six allowed inputs — B2.0
  parity/fixed space and the B2.1 LS identity (exact), Lemma Q (certified), τ < 0 (B1.8, frozen and audited),
  Lyapunov–Schmidt and the implicit function theorem (standard). Facts these inputs already rest on (Paper 2's
  Lemmas S, T1, T2, T3; the B0 bases; analyticity and symmetric criticality as LS hypotheses) are listed inside the
  nodes, not as extra inputs; the validator rejects any extra input. No numerical scan is a proof dependency.
- Numerical corroboration at q = 0.2, 0.8, 1.5, 2.0 and p = P_T(1 ± 10⁻⁶), P_T(1 ± 10⁻⁷): 88/88 checks pass.

**Verification:** full suite 397 collected, 395 passed, 2 skipped (the two Paper 2 archive checks; the archive is not
in the package), run in file/group chunks on Python 3.13.5, python-flint 0.9.0, SymPy 1.14.0, mpmath 1.3.0; 51 of the
tests are new (`tests/test_B2_branch.py`), one is new in `tests/test_docs.py`. B2.4 code-mutation controls 22/22
detected, each of the 15 targets passing unmutated first. Records regenerated serially from empty files; the numerical
record is reproduced bit for bit. The earlier control suites were not re-run: every file they mutate or test, and
their records, is byte-identical with V0.4-dev.4 (identity check). Identity check against V0.4-dev.4: PASS; 45/45 forbidden modifications rejected, even with SHA256SUMS regenerated (`data/B2_4_identity_controls.json`).

**Changed:**
- `src/cube_bif/__init__.py`: version 0.4.0.dev5 and status (docstring and the two values only).
- `tests/test_docs.py`: status pins; the proved-status test admits Proposition B2 (three proved headings); one new
  test for §11 and §12.
- `audits/README.md`: the new report and its provenance (earlier text verbatim).
- Documentation: `NOTES.md` (header; in §0 the sentence on proved statuses; §11 re-audit, §12 B2.4, §13 next steps
  replace the old §11 next steps; §1–§10 byte-identical), `README.md`, `RESEARCH_LOG.md` (appended), this file.

**New:**
- `src/cube_bif/b2_branch.py`; `tests/test_B2_branch.py` (51 tests); `scripts/run_B2_4.py`,
  `scripts/negative_controls_B2_4.py`, `scripts/check_identity_V0_4_dev5.py`, `scripts/identity_controls_V0_4_dev5.py`;
  `docs/V0.4-dev.5_IDENTITY_CHECK.md`.
- Data: `data/B2_4_branch.json`, `data/B2_4_dependency_graph.json`, `data/B2_4_negative_controls.json`,
  `data/B2_4_identity_controls.json`.
- `audits/CUBE_BIFURCATIONS_V04_DEV4_B1_ERRATUM_REAUDIT.md` (byte-identical copy).

**Unchanged (byte-identical with V0.4-dev.4):** Track A, B0, B1 (including both corrected Taylor routines, the
historical certificate 616817fc… and the corrected rebuild), B2.0, B2.1, B2.2, B2.3 (code, certificate f7bc244e…,
records), all earlier tests except `test_docs.py`, all earlier scripts and control records, the earlier audit
reports (`docs/V0.4-dev.5_IDENTITY_CHECK.md`).

## V0.4-dev.4 — 2026-11-14 — B1 implementation erratum E-B1 (series length)

A B1 implementation erratum patch only. B2.4 and B2.5 are not started; Paper 2 is untouched; nothing is frozen,
published, pushed or uploaded. B1 status: **CERTIFIED · INDEPENDENTLY AUDITED · IMPLEMENTATION ERRATUM PENDING
TARGETED RE-AUDIT**; the erratum is not closed (NOTES §10).

**Defect:** python-flint 0.9.0 truncates every arb_series at ctx.cap (default 10). `b1_cert._taylor` and
`b1_check.Model.taylor` requested longer series without raising ctx.cap and padded the result with zeros, so the
near-diagonal Taylor forms dropped c₁₀, c₁₁, … and the remainder. The original B1 Taylor implementation was not
rigorous as written. Reproduced on the unmodified V0.4-dev.3 code before the patch: at (q, δ) = (1.9, 0.9) all seven
near-regime enclosures of both routines exclude the 60-digit reference (worst miss 2.8·10⁻⁹).

**Changed:**
- `src/cube_bif/b1_cert.py`: `_taylor` corrected; new `SeriesTruncationError`, `_series_capacity` (context manager:
  ctx.cap ≥ n, restored on exit and on exceptions) and `_series_coefficients`; `import contextlib`. Nothing else.
- `src/cube_bif/b1_check.py`: `Model.taylor` corrected; new `TruncatedSeries`, `SeriesLength` (context manager) and
  `Model._raw_series`. Nothing else.
- `tests/test_B1_certificate.py`: `test_fresh_and_stored_semantic_hashes_agree` replaced by
  `test_stored_certificate_is_the_historical_audited_one` (the corrected generator produces other bytes).
- `src/cube_bif/__init__.py`: version 0.4.0.dev4 and status; `tests/test_docs.py`: status pins only.
- Documentation: `NOTES.md` (header; new §10 Erratum E-B1; Next steps renumbered §11; §0–§9 byte-identical),
  `README.md`, `RESEARCH_LOG.md` (appended) and this file.

**New:**
- `tests/test_B1_erratum.py` (15 regression tests); `scripts/run_B1_erratum.py`, `scripts/negative_controls_B1_erratum.py`,
  `scripts/reproduce_B1_erratum_pre_patch.py`, `scripts/check_identity_V0_4_dev4.py`,
  `scripts/identity_controls_V0_4_dev4.py`; `docs/V0.4-dev.4_IDENTITY_CHECK.md`.
- Data: `data/B1_ERRATUM_report.json`, `data/B1_ERRATUM_pre_patch_reproduction.json`,
  `data/B1_ERRATUM_corrected_rebuild_certificate.json`, `data/B1_ERRATUM_CORRECTED_REBUILD_SEMANTIC.sha256`,
  `data/B1_ERRATUM_negative_controls.json`, `data/B1_ERRATUM_identity_controls.json`.

**Unchanged (byte-identical with V0.4-dev.3):** the historical B1 certificate `data/B1_kappa_certificate.json`
(semantic 616817fc…8518c6) and its hash file, every other B1 file, Track A, B0, B2.0, B2.1, B2.2, B2.3, the audit
reports, all earlier scripts and control records (`docs/V0.4-dev.4_IDENTITY_CHECK.md`).

**Results (NOTES §10.3):**
- Corrected B1 checker on the historical certificate: 222/222 curve inclusions, 222/222 carrier bounds, endpoints
  accepted, Lemma K bound 1311719/536870912 unchanged.
- Fresh corrected rebuild (stored separately): semantic b2f8e6dcd1c5073635babea2f7a6079b7ede03acbbc4f33ac3cb20f64d21d505,
  222 boxes, the same bound, endpoints and claim; only the 52 near-regime boxes differ; accepted by the corrected checker.
- B2.3 checker (no Taylor series, neither affected routine loaded): 222/222 imported B1 curve balls re-verified.
- Tests: 345 collected, 343 passed, 2 skipped (the Paper 2 archive checks; the archive is not part of the package),
  including the 15 new erratum tests. Erratum code-mutation controls 13/13 as required (12 detected, 1 documented
  expected non-detection). Existing controls 34/34, 9/9, 24/24 detected with byte-identical records; B1 and A2 method
  controls 6/6 and 5/5 as required. Identity check against V0.4-dev.3: PASS; 41/41 forbidden modifications rejected.

## V0.4-dev.3 — 2026-11-13 — Track B, Phase B2.3 (certificate: Lemma Q)

B2.2 passed the review gate. This version adds B2.3 only: Lemma Q, ĉ₄ > 0 on the whole closed physical T2g curve,
CERTIFIED (computer-assisted; not independently audited), and its corollary c₄ > 0 for 0 < q < q_c. No monotonicity
claim, no branch classification, no centre-manifold index.

**Unchanged (byte-identical with V0.4-dev.2):** every Track A, B0, B1, B2.0, B2.1 and B2.2 file, the earlier control
scripts and their records included (`docs/V0.4-dev.3_IDENTITY_CHECK.md`).

**New:**
- `src/cube_bif/b2_cert.py`: the generator (128 bits). It imports B1's curve boxes under a pinned semantic hash and
  records the import checks, re-verifies every imported ball by interval Newton, and uses ball quotients far from
  the diagonal and an even symmetric series near it. The endpoints have their own formulations; the lower bounds are
  robust dyadic numbers; the certificate has a semantic hash.
- `src/cube_bif/b2_check.py`: the independent checker (192 bits, no Taylor series, no project imports): its own
  derivation, integral divided differences with rational subdivision, the kernel vector v = (M̂₂₂, −M̂₁₂) with ‖v‖⁴
  normalisation, its own Newton re-verification, mean-value box bounds.
- `scripts/run_B2_3.py`, `scripts/negative_controls_B2_3.py`, `scripts/diagnose_B1_series_cap.py`,
  `tests/test_B2_certificate.py`.
- Data: `data/B2_c4hat_certificate.json`, `data/B2_CERTIFICATE_SEMANTIC.sha256`, `data/B2_3_check_report.json`,
  `data/B2_3_method_controls.json`, `data/B2_3_negative_controls.json`, `data/B2_3_B1_series_cap_diagnostic.json`.

**Results (NOTES §9):**
- 222 boxes, all positive. The smallest recorded bound is 955723/262144 ≈ 3.6458 (first box); ĥ_E ≥ 1.8936 and
  M̂₂₂ ≥ 1.3816 on every box.
- ĉ₄(0) ∈ [3.79933803786688581571022702877 ± 7.9·10⁻³¹] and ĉ₄(q_c) ∈ [4.37703549061312193611302188495 ± 4.6·10⁻³⁰].
- Semantic SHA-256: f7bc244ecac4b89ce003a38ff52047d6cbe80f63a97236049f15f5e0da5c17d2.
- The checker re-verifies all 222 curve balls and confirms all 222 boxes. 23 consistent forgeries are rejected, 15
  method controls behave as required, and 24 of 24 code mutations are detected.

**Finding (NOTES §9.8):** python-flint truncates every arb_series at ctx.cap (default 10). B1's two Taylor routines pad
the truncated series with zeros, which is unsound as written. The stored B1 certificate is valid: its own checker
accepts it with complete series, and the B2.3 checker re-verifies all its curve balls without Taylor series. B1 is
unchanged; an erratum is proposed for the gate.

**Changed:**
- `src/cube_bif/__init__.py`: version 0.4.0.dev3 and status.
- `tests/test_docs.py`: version and status pins only.
- Documentation:
  - `NOTES.md`: header, and a new §9; the old §9 became §10.
  - `README.md`, `RESEARCH_LOG.md` (appended), `reference/PAPER2_INPUTS.md` (appended: Lemma T3 in the corollary)
    and this file.

## V0.4-dev.2 — 2026-11-13 — Track B, Phase B2.2 (reconnaissance)

B2.0 and B2.1 passed the review gate. This version adds B2.2 only: numerical reconnaissance of the normalised D2h
quartic carrier ĉ₄ on the closed physical T2g curve. Status: VERIFIED-NUMERIC / RECONNAISSANCE. No certificate, no
branch classification, no centre-manifold index.

**Unchanged (byte-identical with V0.4-dev.1):** every Track A, B0, B1, B2.0 and B2.1 file. That includes
`scripts/negative_controls.py` and its record, kept untouched by giving B2.2 its own control script
(`docs/V0.4-dev.2_IDENTITY_CHECK.md`).

**New:**
- `src/cube_bif/b2_carrier.py`: exact values at r = 0 and exact derivative closed forms; P_T(0) and q_c refined
  inside Paper 2's enclosures; both endpoint formulations; the scan; the independent raw 24-D route with limit
  potentials and its own curve points; the nonlinear endpoint check; the falsification statements.
- `scripts/run_B2_2.py`, `scripts/negative_controls_B2_2.py`, `tests/test_B2_carrier.py`.
- Data: `data/B2_carrier.json`, `data/B2_scan.csv`, `data/B2_falsification.json`, `data/B2_2_negative_controls.json`.

**Results (NOTES §7):**
- ĉ₄(0) = 3.79933803786688581571… and ĉ₄(q_c) = 4.37703549061312193611…, each from its own endpoint formulation. At
  the corner, derivatives replace the divided differences and nothing is divided by p − q.
- Scan (401 points): positive, strictly increasing on the grid, no sign change. The minimum is at q = 0; the approach
  to the corner is quadratic.
- Denominators: ĥ_E ≥ 1.998, M̂₂₂ ≥ 1.455, 1 + ρ² ≥ 1.0004.
- The independent route agrees to ≤ 1.2·10⁻⁴⁸. All 7 falsification statements are exposed, and 9 of 9 B2.2 code
  mutations are detected.

**Changed:**
- `src/cube_bif/__init__.py`: version 0.4.0.dev2 and status.
- `tests/test_docs.py`: version and status pins; the end marker of §6 in the B2 test (the next heading is now §7,
  Phase B2.2).
- Documentation:
  - `NOTES.md`: header, and a new §7; the old §7 and §8 became §8 and §9.
  - `README.md`, `RESEARCH_LOG.md` (appended), `reference/PAPER2_INPUTS.md` (appended: the two enclosures used) and
    this file.

## V0.4-dev.1 — 2026-11-13 — Track B, Phase B2: B2.0 and B2.1

Starts Phase B2 as the relayed plan orders it: B2.0 (exact symmetry audit) and B2.1 (the quartic coefficient) only,
to be checked at the review gate before B2.2 (carrier and scan) and B2.3 (certificate).

**Track A, B0 and B1 are unchanged.** Every Track A, B0 and B1 file is byte-identical with V0.3.1-dev: source,
scripts, tests, both certificates and all their data (`docs/V0.4-dev.1_IDENTITY_CHECK.md`).

**New:**
- `src/cube_bif/b2_symmetry.py`: the stabiliser of e₁ in 24-D, the projector onto its fixed space and the isotypic
  decomposition, the relayed claim tested, b = D³V[e₁, e₁, ·] exactly with all its projections, the Schur reason,
  the normaliser, the vertex-orbit parametrisation, first-order geometry.
- `src/cube_bif/b2_quartic.py`: route 1 (13 exact linear forms, closed forms, difference forms, factorisation), the
  Hessian on the fixed space, route 2 (exact raw line expansion; numeric raw 24-D with a spectral solve), route 3
  (restricted D2h family, own curve point, Newton reduction, Richardson).
- `scripts/run_B2.py`; tests `tests/test_B2_symmetry.py`, `tests/test_B2_quartic.py`.
- Data: `data/B2_symmetry.json`, `data/B2_quartic.json`.

**Results (NOTES §6):**
- Fix_{R²⁴}(D2h) = A1g ⊕ Eg(1 direction) ⊕ T2g ⊕ T2g (one direction per copy), dimension 4. The relayed claim
  span{e_crit, A1g, Eg⁽¹⁾, Eg⁽²⁾} is not correct.
- b ∈ A1g ⊕ Eg exactly for every pair potential; ⟨b, f₁⟩ = ⟨b, e₁⟩ = 0 exactly.
- c₄ = D⁴V[e₁⁴] − 3b_A²/h_A − 3b_E²/h_E = qW_q(p − q)ĉ₄ (VERIFIED-EXACT); h_A, h_E > 0 by Paper 2's Lemma S.
- Three routes agree at five curve points (VERIFIED-NUMERIC there only). No sign claim on the curve, no certificate,
  not audited.

**Changed:**
- `scripts/negative_controls.py`: ten B2 mutations added; the earlier 24 are unchanged. `data/negative_controls.json`
  regenerated (34 controls; the earlier 24 records unchanged).
- `src/cube_bif/__init__.py`: version 0.4.0.dev1 and status.
- `tests/test_docs.py`: version and status pins; one added test of the B2 records and claim boundary.
- Documentation: `NOTES.md` (header, new §6; the old §6 and §7 became §7 and §8), `README.md`, `RESEARCH_LOG.md`
  (appended), `docs/CONTRADICTIONS_EXTERNAL_BRAINSTORM.md` (appended: the relayed B2 claims),
  `reference/PAPER2_INPUTS.md` (appended: Lemmas S and T1), this file.

## V0.3.1-dev — 2026-11-13 — audit-status patch

No mathematical changes. Records the independent audit of Phase B1 (PASS; no mathematical, certificate or
documentation correction required) and updates the B1 status labels.

**Audit record:**
- `audits/CUBE_BIFURCATIONS_V03_REVIEWER_REPORT.md`, byte-identical
  (SHA-256 82bd4f21630a20481113702a9f49dddfa6327f2baf3c07a131af259c1baa65e5).
- Source archive: `Kimi_Agent_Blind_Theorem4_Proof_Audit_2.zip`
  (SHA-256 1058e2a12b545e7ca3208ba8d8c562f0712c047c10625cb64a5cba7a672333e0).
- `audits/README.md` lists both reports.
- `NOTES.md` §5.11 summarises the audit.
- Lemma K and Proposition B1 now carry CERTIFIED · INDEPENDENTLY AUDITED.

**Version and status metadata (strings only):**
- `src/cube_bif/__init__.py`: `__version__` 0.3.1.dev0, `STATUS` "RESEARCH / V0.3.1-dev", and the status sentences
  of the docstring.
- `tests/test_docs.py`: the version and status pins.

**Documentation:**
- `NOTES.md`: the header, the §5.7 and §5.9 headings, the new §5.11, and §7.
- `README.md`, `RESEARCH_LOG.md` (appended), this file.

**Unchanged (byte-identical with V0.3-dev):**
- all source, scripts and tests other than the two metadata files;
- the Lemma K and Lemma M certificates and their semantic hash files;
- all data, which was not regenerated, so the B1 records still name 0.3.0.dev0, the version of the unchanged code
  that produced them.

The comparison is in `docs/V0.3.1-dev_DIFF_CHECK.md`.

## V0.3-dev — 2026-11-13 — Track B, Phase B1

**Track A is unchanged.** Every Track A file is byte-identical with the audited V0.2.1-dev
(`docs/V0.3-dev_TRACK_A_IDENTITY.md`): source, scripts, tests, the Lemma M certificate and all data.

**New:**
- `src/cube_bif/b1_cubic.py`: exact trilinear table (route 1), raw 24-D route 2, closed forms g_m, divided differences,
  chart, scan, route 3, D3d corroboration.
- `src/cube_bif/b1_cert.py`: Arb certificate generator.
- `src/cube_bif/b1_check.py`: independent checker.
- `scripts/run_B1.py`.
- Tests: `tests/test_B1_exact.py`, `tests/test_B1_certificate.py`, `tests/test_B1_d3d.py`.
- Data: `data/B1_cubic.json`, `data/B1_scan.csv`, `data/B1_kappa_certificate.json`,
  `data/B1_CERTIFICATE_SEMANTIC.sha256`, `data/B1_negative_controls.json`.

**Results:**
- κ = D³V[e₁, e₂, e₃] = qW_q(p − q)κ̂ exactly.
- Lemma K (CERTIFIED): κ̂ ≥ 1311719/536870912 > 0 on the closed T2g curve, so κ ≠ 0 for 0 < q < q_c.
- Transversality τ < 0 comes from Paper 2's Lemmas T1 and T3.
- Proposition B1 (CERTIFIED): the D3d branches are transcritical.
- B1 is not independently audited.

**Changed:**
- `src/cube_bif/__init__.py`: version 0.3.0.dev0 and status.
- `tests/test_docs.py`: version and status pins.
- `scripts/negative_controls.py`: seven B1 mutations added, so `data/negative_controls.json` now has 24 entries.
- Documentation:
  - `NOTES.md`: new §5 (Phase B1); the old §5 and §6 became §6 and §7.
  - `README.md`, `RESEARCH_LOG.md`, this file.
  - `docs/CONTRADICTIONS_EXTERNAL_BRAINSTORM.md`: the C5 update and a section on the Google note.

## V0.2.1-dev — 2026-11-13 — documentation/audit patch

No mathematical changes. Implements the two documentation corrections required by the independent Track A audit.

**MINOR-01 (wording of the T_d branch configurations):**
- The configurations are now described as two concentric regular tetrahedra of unequal radii on inversion-related
  vertex-direction sets.
- Spatial inversion exchanges the complete branch configurations x₊ and x₋; it does not exchange the unequal-radius
  shells within one fixed configuration.
- Changed in `NOTES.md` §2 item 7, `NOTES.md` §3.9 (statement and proof) and `README.md`.

**MINOR-02:** the negative-control count in `NOTES.md` §3.7 is corrected to 17/17 (9 from V0.1-dev, 6 on the A2
generator and checker, 2 on the Theorem A graph).

**Audit record:**
- `NOTES.md` §3.10 summarises the audit (Kimi Agent, blind audit of V0.2-dev, SHA-256 ba835b0d…91e30). It covers a
  separate reproduction, an independent MPFR directed-rounding re-certification of Lemma M, and exact A0/A1 checks
  written without the package code.
- `audits/` holds the report, byte-identical.
- As the verdict allows, Theorem A and Corollary M now carry PROVED (computer-assisted) · INDEPENDENTLY AUDITED, and
  Lemma M carries CERTIFIED · INDEPENDENTLY AUDITED.

**Version and status metadata (strings only):**
- `src/cube_bif/__init__.py`: `__version__` 0.2.1.dev0, `STATUS` "RESEARCH / V0.2.1-dev", and the status sentence of
  the docstring.
- `src/cube_bif/theorem_a.py`: the `THEOREM_STATUS` string, and the matching `status` field of
  `data/A2_theorem_A_dependencies.json`.
- `tests/test_docs.py`: the assertions that pin the version and the status wording.

**Unchanged (byte-identical with V0.2-dev):**
- all other source, the scripts, and every A0/A1/A2/B0 test file;
- the Lemma M certificate JSON and its semantic hash file;
- every other data file.

The data files were not regenerated. Their embedded version fields therefore still read 0.2.0.dev0, the version of
the unchanged code that produced them. The byte comparison is in `docs/V0.2.1-dev_DIFF_CHECK.md`.

## V0.2-dev — 2026-11-13 — Phase A2

- Lemma M: an Arb certificate that m′(r) > 0 on [0, 16/5], with minimum lower bound 161457/262144. It comes with an
  independent checker, tamper tests and negative controls.
- Corollary M (c₄ > 0 on the whole A2u curve) and Theorem A (the A2u pitchfork), proved computer-assisted.
- A machine-readable proof dependency graph.

## V0.1-dev — 2026-11-13 — Phases A0, A1, B0

- Exact A2u representation audit.
- The quartic coefficient on the A2u curve (Theorem candidate A).
- T2g reconnaissance.
