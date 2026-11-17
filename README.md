# EIT-LJ Cube Bifurcations (Paper 3) — V1.0.0

**Symmetry-Breaking Bifurcations from the Cubic Equilibrium in Two-Term Inverse-Power Clusters**

Status at build time (2026-11-16): **FINAL RELEASE PREPARED / V1.0.0 · PENDING RC2→V1.0.0 DELTA AUDIT**.
FINAL BLIND RELEASE AUDIT of V1.0.0-rc2: **RELEASE-READY** (`audits/PAPER3_RC2_FINAL_BLIND_RELEASE_AUDIT.md`, SHA-256
`37b0b4d68f4675b4546f7313aca6937c51cdf1ee11d1cc20b528918e636d7448`). Human approvals (author contributions, competing interests,
copyright-holder wording): **CLOSED** by author decision (`AUTHOR_DECISION_V1.0.0.md`). PUBLIC RELEASE: NOT YET
EXECUTED. FREEZE = NO (pending the delta audit) · GitHub = HOLD · Zenodo publish = HOLD · Springer/JMC submission = HOLD · v1.0.0 public tag = NOT CREATED. The next step is the independent RC2 → V1.0.0 delta/preservation audit
(`FINAL_V1_DELTA_AUDIT_INSTRUCTIONS.md`).

The mathematics is that of the audited development version V0.4-dev.6 (archive SHA-256
`c473af60f8b54c0beecd252d9e8409eef734ba475c0d693b300946f57941b691`). V1.0.0 adds no mathematics. It differs from
V1.0.0-rc2 (archive SHA-256 `6dee0be5f975d23fce3a36770ddebad8041aae9e3f302df0cd923fad91481a08`) only in the author-approved declarations,
copyright metadata, version/status metadata, PDF document properties, the archived final audit report, audit
index/status records, release notes, release tooling, checksums and packaging. It is checked against V0.4-dev.6 and
against V1.0.0-rc2 by `scripts/check_preservation_V1_0_0.py` (`docs/V1.0.0_PRESERVATION_CHECK.md`).

## Authors

- **Toni Mladenovski** — EITNetworks LLC, Tobyhanna, Pennsylvania, USA (Founder). Corresponding author,
  info@eitnetworks.org, ORCID 0009-0009-8343-662X.
- **Mihail Mladenski** — EITNetworks LLC, Tobyhanna, Pennsylvania, USA. mmladenski077@gmail.com. No ORCID.

No educational institution is listed for either author. The author-contribution, competing-interests and copyright
statements are approved by the authors (`AUTHOR_DECISION_V1.0.0.md`; manuscript, "Statements and declarations").
AI systems were used as tools and are not authors (`docs/AI_USE_LOG.md`). Funding: this research received no external
funding.

## Current status of the results

Machine-readable: `docs/AUDIT_STATUS_MATRIX.json`; human-readable: `docs/AUDIT_STATUS_MATRIX.md`; reports: `audits/`.

| result | status |
|---|---|
| Lemma M (Track A) | CERTIFIED · INDEPENDENTLY AUDITED |
| Theorem A — the A2u pitchfork | PROVED (computer-assisted) · INDEPENDENTLY AUDITED |
| Corollary M — c₄ > 0 on the A2u curve | PROVED (computer-assisted) · INDEPENDENTLY AUDITED |
| Lemma K — κ̂ > 0 on the T2g curve | CERTIFIED · INDEPENDENTLY AUDITED · ERRATUM CLOSED |
| Proposition B1 — the D3d transcritical branches | CERTIFIED (computer-assisted) · INDEPENDENTLY AUDITED · ERRATUM CLOSED |
| Lemma Q — ĉ₄ > 0 on the closed T2g curve | CERTIFIED · INDEPENDENTLY AUDITED |
| Proposition B2 — the D2h pitchfork | PROVED (computer-assisted) · INDEPENDENTLY AUDITED |
| Proposition B3 — centre-manifold inertia of the D2h branch | PROVED (computer-assisted) · INDEPENDENTLY AUDITED |
| Corollary B3′ — full-slice inertia of the D2h branch | PROVED (computer-assisted) · INDEPENDENTLY AUDITED |

Audited inertia of the D2h branch points (negative / zero / positive), for fixed 0 < q < q_c and small μ = p − P_T(q) > 0:
centre (1, 0, 2) — centre Morse index 1, nullity 0; slice (4, 0, 14) — slice Morse index 4, nullity 0; R²⁴ (4, 6, 14),
where the six raw zero modes are the rigid motions and are never counted. **None of these statements implies
stability**: the branch points are saddles with four negative directions in the rigid-motion-reduced configuration
space.

The historical audited B1 certificate (semantic SHA-256 `616817fcc70e0fab7f106404e5e5332b17b9c4480bd440355f1ac5257a8518c6`)
is the certificate of record; the corrected rebuild of erratum E-B1 (semantic `b2f8e6dc…`) is corroboration only.

Status strings inside proof records (`data/*.json`) and in the status constants of `src/cube_bif/b2_branch.py`
and `src/cube_bif/b2_index.py` keep the wording they had when generated ("not independently audited"); these audited
artefacts are byte-identical with V0.4-dev.6 by design. The table above is the current status.

## Release contents (added since V0.4-dev.6)

- `paper/` — manuscript source (`manuscript.tex`), bibliography, sections, appendices, deterministic figure script and
  vector figures; `paper/tools/check_appendix_closed_forms.py` checks the appendix formulas against the code.
- `submission/` — Journal of Mathematical Chemistry drafts (not submitted): cover letter, metadata sheet,
  declarations, AI-use disclosure.
- `docs/AUDIT_INDEX.md`, `docs/AUDIT_STATUS_MATRIX.{json,md}`, `docs/THEOREM_DEPENDENCY_SUMMARY.md`,
  `docs/AI_USE_LOG.md`, `docs/REPRODUCIBILITY.md`, `docs/REFERENCE_VERIFICATION.md`.
- Current (V1.0.0) records: `RELEASE_NOTES_V1.0.0.md`, `AUTHOR_DECISION_V1.0.0.md`,
  `FINAL_V1_DELTA_AUDIT_INSTRUCTIONS.md`, `audits/PAPER3_RC2_FINAL_BLIND_RELEASE_AUDIT.md` (final blind release audit
  of RC2, verbatim), `docs/V1.0.0_PRESERVATION_CHECK.{md,json}`, `docs/V1.0.0_PRESERVATION_CONTROLS.json`,
  `docs/V1.0.0_TEXT_SCAN.{md,json}`, `docs/QA_RESULTS_V1.0.0.{md,json}`, `docs/GITHUB_RELEASE_V1.0.0.md` (prepared tag
  message, release description and asset list; nothing pushed).
- Release metadata (prepared, not published): `CITATION.cff`, `.zenodo.json`, `LICENSE`, `LICENSE-DOCS`.
- Release tooling: `scripts/check_preservation_V1_0_0.py`, `scripts/preservation_controls_V1_0_0.py`,
  `scripts/check_release_text.py`, `scripts/scan_text_v1.py`; tests `tests/test_release_v1.py`.
- Historical RC2 records, kept byte-identical with V1.0.0-rc2 and not current: `RELEASE_NOTES_RC2.md`,
  `FINAL_AUDIT_INSTRUCTIONS.md` (the instructions under which the completed final blind release audit was performed),
  `docs/QA_RESULTS_RC2.{md,json}`, `docs/V1.0.0-rc2_PRESERVATION_CHECK.{md,json}`,
  `docs/V1.0.0-rc2_PRESERVATION_CONTROLS.json`, `docs/V1.0.0-rc2_TEXT_SCAN.{md,json}`,
  `scripts/check_preservation_V1_0_0_rc2.py`, `scripts/preservation_controls_V1_0_0_rc2.py`,
  `scripts/scan_text_rc2.py`. Their open author-approval items are closed by `AUTHOR_DECISION_V1.0.0.md`.
- Historical RC1 records, kept byte-identical with V1.0.0-rc1 and not current: `RELEASE_NOTES_RC1.md`,
  `docs/QA_RESULTS_RC1.{md,json}`, `docs/V1.0.0-rc1_PRESERVATION_CHECK.md`,
  `docs/V1.0.0-rc1_PRESERVATION_CONTROLS.json`, `scripts/check_preservation_V1_0_0_rc1.py`,
  `scripts/preservation_controls_V1_0_0_rc1.py`. Their open author items (city, second-author contact, review flags)
  are superseded (historical).

## Licences

Software: PolyForm Noncommercial License 1.0.0. Manuscript, documentation, figures, generated results and package-authored metadata: CC BY-NC-SA 4.0. Commercial use only by separate written agreement. Copyright © 2026 EITNetworks LLC and the authors. Software licence: `LICENSE`; documentation
licence: `LICENSE-DOCS`; contact for commercial licensing: info@eitnetworks.org. The independent audit reports in `audits/` are reproduced verbatim as records and are not
relicensed.

## Development history

V0.1-dev was labelled RESEARCH CANDIDATE / V0.1-dev. Its mathematics (Phases A0, A1, B0) is unchanged in V0.2-dev.
V0.2.1-dev is a documentation/audit patch of V0.2-dev with no mathematical changes. V0.3-dev added Phase B1 and left
every Track A file byte-identical (`docs/V0.3-dev_TRACK_A_IDENTITY.md`). V0.3.1-dev is an audit-status patch of
V0.3-dev with no mathematical changes (`CHANGELOG.md`, `docs/V0.3.1-dev_DIFF_CHECK.md`). V0.4-dev.1 starts Phase B2
with B2.0 and B2.1 and leaves every Track A, B0 and B1 file byte-identical (`docs/V0.4-dev.1_IDENTITY_CHECK.md`).
V0.4-dev.2 adds B2.2 and leaves every earlier file byte-identical apart from documentation and version strings
(`docs/V0.4-dev.2_IDENTITY_CHECK.md`). V0.4-dev.3 adds B2.3 in the same way (`docs/V0.4-dev.3_IDENTITY_CHECK.md`).
V0.4-dev.4 is a B1 implementation erratum patch only (erratum E-B1, `NOTES.md` §10): it corrects the two B1 Taylor
routines and adds regression tests and records; everything else is byte-identical with V0.4-dev.3
(`docs/V0.4-dev.4_IDENTITY_CHECK.md`). V0.4-dev.5 records the targeted re-audit that closes erratum E-B1 and adds
B2.4; every earlier file is byte-identical apart from documentation, version strings, `tests/test_docs.py` and
`audits/README.md` (`docs/V0.4-dev.5_IDENTITY_CHECK.md`). V0.4-dev.6 adds B2.5; every earlier file is byte-identical
apart from documentation, version strings and `tests/test_docs.py` (`docs/V0.4-dev.6_IDENTITY_CHECK.md`).
V1.0.0-rc1 is a packaging, audit-status and manuscript release candidate with no new mathematics
(`docs/V1.0.0-rc1_PRESERVATION_CHECK.md`). V1.0.0-rc2 updates author and institution metadata, declarations,
bibliography metadata and release tooling, again with no new mathematics (`docs/V1.0.0-rc2_PRESERVATION_CHECK.md`).
V1.0.0-rc2 passed the final blind release audit (RELEASE-READY). V1.0.0 inserts the author-approved declarations and
copyright wording, sets the final version metadata and PDF document properties, and archives the final audit report,
again with no new mathematics (`docs/V1.0.0_PRESERVATION_CHECK.md`).

Paper 2 (EIT_LJ_FULL_VECTOR_STABILITY: frozen at V0.2-dev.10, public V1.0, DOI 10.5281/zenodo.24187155) is used only
as read-only input (`reference/PAPER2_INPUTS.md`).

## Mathematical content (unchanged since V0.4-dev.6)

- **Phase A0 — exact A2u representation audit.**
  - The exact eigenvector is E_A(s) = (s₁s₂s₃)s, in Paper 2's convention.
  - It is orthogonal to the rigid motions and to scaling, and has the A2u character under all 48 elements.
  - Its stabiliser, computed, is T_d.
  - Inversion acts as −1, so the reduced potential is even (c₃ = 0).
- **Phase A1 — quartic Lyapunov–Schmidt coefficient on the A2u curve p = P_A(q), 0 < q < r*.**
  - b = D³V[e_A, e_A, ·] lies exactly in the breathing direction.
  - So c₄ = V_aaaa − 3V_aab²/V_bb, with closed forms in p, q, 2^(−p/2), 3^(−p/2), 2^(−q/2), 3^(−q/2).
  - Equivalent scale-eliminated form: c₄ = (16/3)qW_q[m(P_A(q)) − m(q)].
  - The two forms agree to 10⁻³⁹, and a 24-dimensional numerical route agrees with both.
  - Numerically, c₄ > 0 at all 415 points of the curve.
- **Phase A2 (new in V0.2-dev) — Lemma M, Corollary M, Theorem A.**
  - Lemma M (CERTIFIED): m′(r) ≥ 161457/262144 ≈ 0.6159 > 0 on [0, 16/5].
    - Arb ball arithmetic (python-flint) at 128 bits, mean-value box test.
    - 64 boxes with exact rational endpoints.
    - Re-verified at 160 bits by an independent checker with its own derivation.
    - Tampered certificates are rejected, and the same method fails on [7, 8], where m′ changes sign.
  - Near r = 0: m′(0) = 18/49 + (12/49)log 2 + (57/784)log 3 > 0 exactly, and m″ > 0 on [0, 1/8] (certified).
  - Certified: h_A(16/5) < −6/7 and h_A′(16/5) < 0. With Paper 2's Lemma A this gives P_A(q) < 16/5.
  - Corollary M: c₄(q) ≥ (16/3)·L_min·qW_q·(P_A(q) − q) > 0 on the whole A2u curve.
  - Theorem A, PROVED (computer-assisted) · INDEPENDENTLY AUDITED:
    - The cube undergoes a supercritical (in the energy sense) Z₂ pitchfork at p = P_A(q), for every q ∈ (0, r*).
    - The two T_d branches exist only for p > P_A(q). This side comes from the reduced equation.
    - Each branch configuration is two concentric regular tetrahedra of unequal radii on inversion-related
      vertex-direction sets. Spatial inversion exchanges the complete configurations x₊ and x₋, not the shells within
      one configuration.
    - The proof dependency graph is machine-readable and tested (`src/cube_bif/theorem_a.py`).
- **Phase B0 — T2g reconnaissance.**
  - Exact bases and the critical eigenspace on p = P_T(q).
  - The 3×3 matrices are σ(R)R.
  - I₃ = a₁a₂a₃ is invariant.
  - Isotropy: D3d (axial, transcritical-type if κ ≠ 0), D2h (axial, pitchfork-type), C2h (not axial).
- **Phase B1 (new in V0.3-dev) — the cubic coefficient κ = D³V[e₁, e₂, e₃] on p = P_T(q), 0 < q < q_c.**
  - Exact: of the 216 trilinear values on the T2g basis, only the a₁a₂a₃ pattern survives. Four coefficients remain,
    and the raw 24-D cubic restriction is exactly 6κ·a₁a₂a₃ (two independent symbolic routes).
  - Exact factorisation: κ = qW_q(p − q)·κ̂, where κ̂ is built from divided differences, with the chart n = (1, ρ),
    ρ = −M̂₁₂/M̂₂₂.
  - Lemma K (CERTIFIED · INDEPENDENTLY AUDITED): κ̂ ≥ 1311719/536870912 ≈ 0.00244 > 0 on the closed curve,
    endpoints included.
    - Arb at 128 bits; 222 rational boxes; interval Newton for the curve; a Taylor form near the diagonal.
    - Independent checker at 160 bits; tampered certificates are rejected; method controls fail where they must.
  - So κ(q) ≠ 0 for every 0 < q < q_c. Raw κ vanishes only at the two ends (factors q and p − q).
  - Transversality τ < 0 follows from Paper 2's Lemmas T1 and T3, with an exact identity.
  - Proposition B1 (CERTIFIED · INDEPENDENTLY AUDITED): on each D3d axis the reduced equation
    G(s, μ) = λ_red(μ) + κs + O(s²) gives one branch s* = −(τ/κ)μ + O(μ²), on both sides of the curve:
    transcritical. This is by the implicit function theorem, not by Ihrig's theorem. No stability is claimed.
  - D2h: the pitchfork-type parity is retained from B0. The quartic coefficient is left for B2.
- **Phase B2.0 and B2.1 (new in V0.4-dev.1) — the D2h axis a = (s, 0, 0) of the critical T2g representation.**
  - B2.0 (exact): the stabiliser of e₁, computed in 24-D, is the D2h with C2 axes x, (0, 1, 1), (0, 1, −1).
    Fix_{R²⁴}(D2h) is four-dimensional: A1g, the tetragonal Eg direction, and one direction from each T2g copy
    (e₁ and f₁). The relayed claim span{e_crit, A1g, Eg⁽¹⁾, Eg⁽²⁾} is not correct (tested).
  - b = D³V[e₁, e₁, ·] lies exactly in A1g ⊕ Eg for every pair potential; ⟨b, f₁⟩ = ⟨b, e₁⟩ = 0 exactly. The reason is
    Schur's lemma on Sym²(T2g), whose T2g component vanishes on the axis.
  - B2.1 (exact formula): c₄ = D⁴V[e₁⁴] − 3b_A²/h_A − 3b_E²/h_E = qW_q(p − q)ĉ₄, with closed forms. h_A and h_E are
    Paper 2's A1g and Eg blocks, positive by its Lemma S.
  - Three routes (symmetry-adapted; raw 24-D with a spectral solve; the restricted four-parameter D2h family with a
    nonlinear reduction) agree at five curve points to 10⁻⁵⁹ and 10⁻³⁶. Values at those points only; the scan, the
    endpoints, the sign on the curve and the certificate are B2.2 and B2.3.
- **Phase B2.2 (new in V0.4-dev.2) — reconnaissance of the normalised carrier ĉ₄ = c₄/(qW_q(p − q)).**
  - Endpoint q = 0, evaluated from its own formulation (exact values at r = 0; P_T(0) refined inside Paper 2's
    enclosure): ĉ₄(0) = 3.79933803786688581571…
  - Corner, with derivatives in place of divided differences and nothing divided by p − q:
    ĉ₄(q_c) = 4.37703549061312193611…. The approach to the corner is quadratic.
  - 401-point scan (`data/B2_scan.csv`): ĉ₄ is positive and strictly increasing on the grid, with no sign change.
    The minimum is at q = 0. Denominators stay away from 0 (ĥ_E ≥ 1.998, M̂₂₂ ≥ 1.455).
  - An independent raw 24-D route agrees to ≤ 1.2·10⁻⁴⁸. At the endpoints it uses limit potentials (φ/q → c r^−p +
    log r; φ/(p − q) → −(1/q + W′/W + log r) r^−q) and finds P_T(0) and q_c by itself.
  - Seven deliberately false statements are all exposed. Status: VERIFIED-NUMERIC / RECONNAISSANCE; the certificate
    is B2.3.
- **Phase B2.3 (new in V0.4-dev.3) — Lemma Q: ĉ₄ > 0 on the closed physical T2g curve, CERTIFIED · INDEPENDENTLY
  AUDITED** (audit received with V1.0.0-rc1).
  - The curve is B1's: its 222 rational q-boxes and δ-balls, imported unchanged under a pinned semantic hash and
    re-verified. Endpoints are certified directly: q = 0 with the exact values at r = 0 and B1's P_T(0) ball; the
    corner with the derivatives f′(q_c), dividing by nothing.
  - Generator at 128 bits: ball quotients far from the diagonal, an even symmetric series with a Lagrange remainder
    near it. Every box is positive; the smallest recorded bound is 955723/262144 ≈ 3.6458.
    ĉ₄(0) = 3.79933803786688581571… and ĉ₄(q_c) = 4.37703549061312193611… (enclosures of radius < 10⁻²⁹).
  - Corollary: c₄ = qW_q(P_T(q) − q)ĉ₄ > 0 for 0 < q < q_c (Paper 2, Lemma T3 for P_T(q) > q). The raw c₄ is 0 at
    both ends.
  - Independent checker at 192 bits, with no Taylor series and no code shared with the generator. It derives the
    functions itself and uses f̂ = ∫₀¹ f′(q + t(p − q)) dt with rational subdivision. The kernel is v = (M̂₂₂, −M̂₁₂)
    with ‖v‖⁴ normalisation. It re-verifies all 222 curve balls by interval Newton and confirms every bound.
  - 23 consistent forgeries are rejected, 15 method controls behave as required, and 24 of 24 code mutations are
    detected.
  - A finding about python-flint's series length and B1's Taylor code (`NOTES.md` §9.8): the stored B1 certificate is
    valid; an erratum for B1 was proposed (applied in V0.4-dev.4).
- **Erratum E-B1 (V0.4-dev.4) — the B1 Taylor routines** (`NOTES.md` §10, §11). Status of B1: **CERTIFIED ·
  INDEPENDENTLY AUDITED · ERRATUM CLOSED** (V0.4-dev.5).
  - Defect: python-flint truncates every arb_series at ctx.cap (default 10). `b1_cert._taylor` and
    `b1_check.Model.taylor` requested longer series without raising ctx.cap and zero-padded the result, dropping c₁₀,
    c₁₁, … and the remainder. The original near-diagonal Taylor implementation was not rigorous as written.
    Reproduced on the unmodified V0.4-dev.3 code: at (q, δ) = (1.9, 0.9) all seven near-regime enclosures of both
    routines exclude the 60-digit reference.
  - Correction: ctx.cap raised to the requested length inside a context manager that restores it, also on
    exceptions; explicit checks against truncation; zero padding only for verified exact trailing zeros.
  - The stored B1 certificate (semantic 616817fc…) is unchanged and remains valid: the corrected checker accepts it
    (222/222 curve inclusions, 222/222 carrier bounds, endpoints; the Lemma K bound unchanged); a fresh corrected
    rebuild (semantic b2f8e6dc…, stored separately) proves the same claim with the same bound; the Taylor-free B2.3
    checker re-verifies all 222 curve balls without loading either affected routine.
  - The targeted independent re-audit (Kimi Agent, 2026-11-14) passed with no findings above informational; the report
    is in `audits/` and `NOTES.md` §11 summarises it.
- **Phase B2.4 (new in V0.4-dev.5) — Proposition B2, the D2h-axial pitchfork** (`NOTES.md` §12).
  Status: Proposition B2 — PROVED (computer-assisted) · INDEPENDENTLY AUDITED (audit received with V1.0.0-rc1).
  - Reduced equation: V_red = V₀(μ) + ½λ(μ)s² + (c₄/24)s⁴ + O(s⁶, μs⁴, μ²s²), even in s; λ(0) = 0, λ′(0) = τ < 0,
    c₄ > 0 (Lemma Q); ∂_sV_red = s·G(s², μ), G = λ(μ) + (c₄/6)z + O(z², μz, μ²).
  - Implicit function theorem: μ*′(0) = −c₄/(6τ) > 0, so s² = −(6τ/c₄)μ + O(μ²) and the pair ±s* exists only for
    p > P_T(q); the cube exists on both sides.
  - Z₂-symmetric pitchfork (N(Σ) ∖ Σ exchanges ±s*), supercritical in the energy-reduced axial convention; axial
    reduced curvature τμ < 0 at the cube and −2τμ > 0 at ±s* (one-dimensional axial statement only).
  - Geometry: isotropy exactly Σ ≅ D2h; rhombic (sheared) cross-sections and opposite tetrahedral translation at first
    order; not in the cuboid family; O(s²) corrections in span{Â, Ê}.
  - Machine-readable proof dependency graph, validated: its leaves are exactly the six allowed inputs (B2.0, B2.1,
    Lemma Q, τ < 0, Lyapunov–Schmidt, implicit function theorem); no numerical scan is a proof dependency. Numerical
    corroboration at q = 0.2, 0.8, 1.5, 2.0 (88/88 checks); 51 tests; 22/22 code mutations detected.
- **Phase B2.5 (new in V0.4-dev.6) — Proposition B3 and Corollary B3′, the index of the D2h branch** (`NOTES.md`
  §13). Status: Proposition B3 and Corollary B3′ — PROVED (computer-assisted) · INDEPENDENTLY AUDITED (audit received
  with V1.0.0-rc1).
  - Reduced potential on the critical T2g space: V_red = V₀ + ½λ|a|² + κa₁a₂a₃ + α|a|⁴ + βΣa_k⁴ + O(|a|⁵); the
    invariant dimensions 0, 1, 1, 2 (degrees 1–4) are computed, and α + β = c₄/24 is derived by LS elimination.
  - At the D2h branch points: h₁₁ = (c₄/3)s² + O(s⁴), transverse block [[d, e], [e, d]] with d = −4βs² + O(s⁴),
    e = κs + O(s³), determinant −κ²s² + O(s⁴) < 0 (explicit remainder bound): centre index 1, nullity 0, for both
    signs of κ and s; all six conjugate branch points have the same index.
  - Corollary: m_⊥ = 3 (A2u + Eu) derived from Paper 2's Theorem (index) block signs; full-slice index 4.
  - D3d consistency check (not a theorem): centre index 2 (μ > 0) and 1 (μ < 0); local degree −3 on both sides.
  - Dependency graph validated; no numerical scan is a proof dependency. Raw 24-D Hessian corroboration at
    q = 0.2, 0.8, 1.5, 2.0 (300/300 checks).
- **Contradictions** with the external brainstorm: `docs/CONTRADICTIONS_EXTERNAL_BRAINSTORM.md`.

Details, formulas and status labels are in `NOTES.md`; the history is in `RESEARCH_LOG.md`.

## Rules

- Nothing is called proved until each identity it uses has its own test. Numerical sign statements stay CANDIDATE
  until a proof or a certificate exists.
- "Proved" here means computer-assisted. Every proved or certified result listed above has been independently audited
  (reports in `audits/`; index in `docs/AUDIT_INDEX.md`). An independent AI audit is not a journal peer review.
- No change to Paper 2, and no freezing or publishing without the author's explicit authorisation.

## Run

    python -m pip install sympy mpmath numpy scipy pytest   # Python >= 3.11
    python -m pip install python-flint                       # Arb, for Phase A2 (tested with 0.9.0)
    python scripts/run_A0.py && python scripts/run_A1.py && python scripts/run_B0.py   # writes data/
    python scripts/run_A2.py                                 # Lemma M certificate + independent check
    python scripts/run_B1.py                                 # B1 (historical): do NOT re-run (V0.4-dev.4 on); it
                                                             #   overwrites the audited certificate (NOTES.md §10.2)
    python scripts/run_B2.py                                 # B2.0 + B2.1: symmetry audit, c4 by three routes
    python scripts/run_B2_2.py                               # B2.2: endpoints, scan, independent route, falsification
    python scripts/negative_controls_B2_2.py                 # B2.2 code mutations the tests must detect
    python scripts/run_B2_3.py                               # B2.3: Lemma Q certificate + independent check + controls
    python scripts/diagnose_B1_series_cap.py                 # B2.3 finding: python-flint series length and B1
    python scripts/negative_controls_B2_3.py                 # B2.3 code mutations the tests must detect
    python -m pytest -q                                      # every identity has its own test
    python scripts/negative_controls.py                      # mutations the tests must detect
    python scripts/run_B1_erratum.py                         # erratum E-B1: historical replay, corrected rebuild,
                                                             #   B2.3 Taylor-free cross-check, diagnostic point
    python scripts/negative_controls_B1_erratum.py           # erratum E-B1 code mutations the tests must detect
    python scripts/reproduce_B1_erratum_pre_patch.py <V0.4-dev.3 zip>   # the defect on the unmodified V0.4-dev.3 code
    python scripts/check_identity_V0_4_dev4.py <V0.4-dev.3 zip>         # mechanical identity check
    python scripts/identity_controls_V0_4_dev4.py <V0.4-dev.3 zip>      # forbidden modifications it must reject
    python scripts/run_B2_4.py                               # B2.4: Proposition B2 records, dependency graph,
                                                             #   numerical corroboration
    python scripts/negative_controls_B2_4.py                 # B2.4 code mutations the tests must detect
    python scripts/check_identity_V0_4_dev5.py <V0.4-dev.4 zip>         # mechanical identity check (V0.4-dev.5)
    python scripts/identity_controls_V0_4_dev5.py <V0.4-dev.4 zip>      # forbidden modifications it must reject
    python scripts/run_B2_5.py                               # B2.5: Proposition B3 records, dependency graph,
                                                             #   numerical corroboration (about 10 minutes)
    python scripts/negative_controls_B2_5.py                 # B2.5 code mutations the tests must detect
    python scripts/check_identity_V0_4_dev6.py <V0.4-dev.5 zip>         # mechanical identity check (V0.4-dev.6)
    python scripts/identity_controls_V0_4_dev6.py <V0.4-dev.5 zip>      # forbidden modifications it must reject
    python scripts/check_preservation_V1_0_0_rc1.py <V0.4-dev.6 zip>    # mechanical preservation check (V1.0.0-rc1)
    python scripts/preservation_controls_V1_0_0_rc1.py <V0.4-dev.6 zip> # forbidden modifications it must reject
    python scripts/check_preservation_V1_0_0.py <V0.4-dev.6 zip> --rc2=<V1.0.0-rc2 zip>   # V1.0.0 preservation check
    python scripts/preservation_controls_V1_0_0.py <V0.4-dev.6 zip> --rc2=<V1.0.0-rc2 zip> # forbidden modifications
    python scripts/check_release_text.py                     # stale-status, authorship and claim-language scan
    python scripts/scan_text_v1.py                           # classified whole-tree text scan
    python paper/figures/make_figures.py                     # deterministic manuscript figures
    python paper/tools/check_appendix_closed_forms.py        # appendix formulas against the code

To run the cross-checks against Paper 2's own code, place `EIT_LJ_FULL_VECTOR_STABILITY_V1.0.zip` next to this
directory or set `EIT_LJ_PAPER2_ARCHIVE`. Without the archive those cross-checks are skipped.

## Layout

    src/cube_bif/   group.py (O_h, characters, point-group signatures), modes.py (exact fields),
                    b1_cubic.py (B1 exact layer, routes, scan), b1_cert.py (B1 certificate), b1_check.py (checker),
                    pairsum.py (exact multilinear derivatives), a2u.py (A0/A1), t2g.py (B0),
                    numeric.py (independent 24-D route), branch.py (T_d-family branch check), paper2_ref.py,
                    lemma_m.py (A2 certificate generator), certcheck.py (independent checker),
                    theorem_a.py (Theorem A statement and dependency graph),
                    b2_symmetry.py (B2.0 symmetry audit), b2_quartic.py (B2.1 quartic coefficient, three routes),
                    b2_carrier.py (B2.2 carrier reconnaissance), b2_cert.py (B2.3 certificate generator),
                    b2_check.py (B2.3 independent checker), b2_branch.py (B2.4 Proposition B2, dependency graph),
                    b2_index.py (B2.5 Proposition B3, Corollary B3′, dependency graph)
    scripts/        run_A0.py, run_A1.py, run_B0.py, run_A2.py, run_B1.py, run_B2.py, run_B2_2.py, run_B2_3.py,
                    negative_controls.py, negative_controls_B2_2.py, negative_controls_B2_3.py,
                    diagnose_B1_series_cap.py, run_B1_erratum.py, negative_controls_B1_erratum.py,
                    reproduce_B1_erratum_pre_patch.py, check_identity_V0_4_dev4.py, identity_controls_V0_4_dev4.py,
                    run_B2_4.py, negative_controls_B2_4.py, check_identity_V0_4_dev5.py, identity_controls_V0_4_dev5.py,
                    run_B2_5.py, negative_controls_B2_5.py, check_identity_V0_4_dev6.py, identity_controls_V0_4_dev6.py,
                    check_preservation_V1_0_0_rc1.py, preservation_controls_V1_0_0_rc1.py,
                    check_preservation_V1_0_0_rc2.py, preservation_controls_V1_0_0_rc2.py, scan_text_rc2.py
                    (historical release tooling), check_preservation_V1_0_0.py, preservation_controls_V1_0_0.py,
                    check_release_text.py, scan_text_v1.py, validate_dependency_graphs.py
    tests/          test_A0_representation.py, test_A1_quartic.py, test_A2_lemma_m.py, test_A2_certificate.py,
                    test_A2_theorem.py, test_B0_t2g.py, test_B1_exact.py, test_B1_certificate.py, test_B1_d3d.py,
                    test_B2_symmetry.py, test_B2_quartic.py, test_B2_carrier.py, test_B2_certificate.py,
                    test_B1_erratum.py, test_B2_branch.py, test_B2_index.py, test_docs.py, test_release_v1.py
    data/           A0_representation.json, A1_quartic.json, A1_sign_table.csv, B0_t2g.json, negative_controls.json,
                    A2_lemma_M_certificate.json, A2_CERTIFICATE_SEMANTIC.sha256, A2_negative_controls.json,
                    A2_theorem_A_dependencies.json, B1_cubic.json, B1_scan.csv, B1_kappa_certificate.json,
                    B1_CERTIFICATE_SEMANTIC.sha256, B1_negative_controls.json, B2_symmetry.json, B2_quartic.json,
                    B2_carrier.json, B2_scan.csv, B2_falsification.json, B2_2_negative_controls.json,
                    B2_c4hat_certificate.json, B2_CERTIFICATE_SEMANTIC.sha256, B2_3_check_report.json,
                    B2_3_method_controls.json, B2_3_negative_controls.json, B2_3_B1_series_cap_diagnostic.json,
                    B1_ERRATUM_report.json, B1_ERRATUM_pre_patch_reproduction.json,
                    B1_ERRATUM_corrected_rebuild_certificate.json, B1_ERRATUM_CORRECTED_REBUILD_SEMANTIC.sha256,
                    B1_ERRATUM_negative_controls.json, B1_ERRATUM_identity_controls.json, B2_4_branch.json,
                    B2_4_dependency_graph.json, B2_4_negative_controls.json, B2_4_identity_controls.json,
                    B2_5_index.json, B2_5_dependency_graph.json, B2_5_negative_controls.json,
                    B2_5_identity_controls.json
    docs/           CONTRADICTIONS_EXTERNAL_BRAINSTORM.md, V0.2.1-dev_DIFF_CHECK.md (byte comparison with V0.2-dev),
                    V0.3-dev_TRACK_A_IDENTITY.md (Track A byte comparison with V0.2.1-dev),
                    V0.3.1-dev_DIFF_CHECK.md (byte comparison with V0.3-dev),
                    V0.4-dev.1_IDENTITY_CHECK.md (byte comparison with V0.3.1-dev),
                    V0.4-dev.2_IDENTITY_CHECK.md (byte comparison with V0.4-dev.1),
                    V0.4-dev.3_IDENTITY_CHECK.md (byte comparison with V0.4-dev.2),
                    V0.4-dev.4_IDENTITY_CHECK.md (mechanical comparison with V0.4-dev.3),
                    V0.4-dev.5_IDENTITY_CHECK.md (mechanical comparison with V0.4-dev.4),
                    V0.4-dev.6_IDENTITY_CHECK.md (mechanical comparison with V0.4-dev.5),
                    V1.0.0-rc1_PRESERVATION_CHECK.md (mechanical comparison with V0.4-dev.6), AUDIT_INDEX.md,
                    AUDIT_STATUS_MATRIX.json/.md, THEOREM_DEPENDENCY_SUMMARY.md, AI_USE_LOG.md, REPRODUCIBILITY.md,
                    REFERENCE_VERIFICATION.md, V1.0.0-rc2 and V1.0.0 preservation/QA/text-scan records,
                    GITHUB_RELEASE_V1.0.0.md
    audits/         README.md, CUBE_BIFURCATIONS_REVIEWER_REPORT.md (independent Track A audit, verbatim),
                    CUBE_BIFURCATIONS_V03_REVIEWER_REPORT.md (independent B1 audit, verbatim),
                    CUBE_BIFURCATIONS_V04_DEV4_B1_ERRATUM_REAUDIT.md (targeted erratum re-audit, verbatim),
                    CUBE_BIFURCATIONS_V05_BLIND_B23_LEMMA_Q_REVIEWER_REPORT.md (B2.3 audit, verbatim),
                    CUBE_BIFURCATIONS_V05_BLIND_B24_REVIEWER_REPORT.md (B2.4 audit, verbatim),
                    CUBE_BIFURCATIONS_V04_DEV6_BLIND_B25_REVIEWER_REPORT.md (B2.5 audit, verbatim),
                    PAPER3_RC2_FINAL_BLIND_RELEASE_AUDIT.md (final blind release audit of V1.0.0-rc2, verbatim)
    paper/          manuscript.tex, macros.tex, references.bib, sections/, appendices/, figures/, tools/
    submission/     JMC drafts: cover letter, metadata sheet, declarations, AI-use disclosure (not submitted)
    reference/      PAPER2_INPUTS.md
    CHANGELOG.md    version history
    RELEASE_NOTES_V1.0.0.md, AUTHOR_DECISION_V1.0.0.md, FINAL_V1_DELTA_AUDIT_INSTRUCTIONS.md, CITATION.cff,
    .zenodo.json, LICENSE, LICENSE-DOCS; historical: RELEASE_NOTES_RC1.md, RELEASE_NOTES_RC2.md,
    FINAL_AUDIT_INSTRUCTIONS.md

## AI use

AI systems were used as tools; they are not authors. Systems involved: ChatGPT (OpenAI; GPT-5.6 Sol), Claude
(Anthropic), Kimi (Moonshot AI) and the Tasklet agent execution environment. Their roles (symbolic derivation
assistance, code, test generation, computational verification, adversarial auditing, manuscript and release
preparation) are described in `docs/AI_USE_LOG.md`. The mathematical claims rest on exact symbolic calculations,
explicit proof arguments, certified interval arithmetic, independent re-certification and archived reproducibility
records, not on unverified generative-model output. Toni Mladenovski directed the work and takes final responsibility
for the claims.
