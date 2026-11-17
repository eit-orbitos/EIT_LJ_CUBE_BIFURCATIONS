# Research log — EIT-LJ Cube Bifurcations (Paper 3)

## 2026-11-13 — V0.1-dev: project started; Phases A0, A1, B0

- **Start.** Separate project, started at the author's request: "Start a completely separate Paper 3 research
  project. Do not modify Paper 2 or its frozen/public artifacts." Working title: Symmetry-Breaking Bifurcations from
  the Cubic Equilibrium in Two-Term Inverse-Power Clusters. Status RESEARCH CANDIDATE / V0.1-dev. Paper 2 is used
  read-only, from its public V1.0 archive (SHA-256 bb70721d…, checked on every import).
- **A0 (VERIFIED-EXACT, 17 tests):**
  - E_A(s) = (s₁s₂s₃)s, |E_A|² = 24, radial at every vertex.
  - Orthogonal to the translations, the rotations and the breathing direction.
  - D(R)E_A = χ_A2u(R)E_A for all 48 R, with χ_A2u = σ(R).
  - The stabiliser, computed, has 24 elements: E, 8 C3, 3 C2, 6 S4, 6 σ_d, i.e. T_d. Fix(T_d) = span{e_br, e_A}.
  - D(−I)e_A = −e_A, and V is O_h-invariant. So the reduced potential is even (equivariant Lyapunov–Schmidt).
- **A1:**
  - VERIFIED-EXACT:
    - b = D³V[e_A, e_A, ·] = V_aab e_br in all 24 components, for any pair potential.
    - V_aa and V_bb equal Paper 2's A2u and A1g blocks.
    - Difference forms hold, and h_A is identical to Paper 2's.
    - k = h_A/8 − 1/4; m(0⁺) = 8/7 and m(∞) = 21/8.
    - Generic foliation lemma: c₄(R₂) − c₄(R₁) = −12F_aa(F_aa + F_aabβ₀)/(F_bbβ₀²).
    - On the curve: c₄ = (16/3)qW_q[m(p) − m(q)].
  - VERIFIED-NUMERIC:
    - The 24-dimensional route (no symmetry reduction) agrees to 10⁻⁴⁰.
    - r* agrees with the frozen value to 4.9·10⁻²⁰, P_A(0⁺) to 1.2·10⁻²⁰, and P_A with Paper 2's code to 1.7·10⁻¹³.
    - Sign table, 415 points: c₄ > 0 everywhere; Δm ∈ [1.21310, 1.26546], including both endpoint limits.
    - m′ > 0.617 on (0, P_A(0⁺)]; the maximum of m is at r ≈ 7.649.
    - Local branch: it exists only for p > P_A(q), with an O(δ) amplitude error. The amplitude law is confirmed.
  - Transversality follows from Paper 2 Lemma A (FROZEN INPUT).
  - **Theorem candidate A** (NOTES §3.7) is open. It is missing Lemma M.
- **B0:**
  - VERIFIED-EXACT:
    - Matched T2g bases; T(R) = σ(R)R for both copies and for the critical basis, with symbolic n.
    - The Hessian block equals Paper 2's Lemma T0 and factorises through M(r).
    - I₃ = a₁a₂a₃ is invariant; invariant dimensions are 0, 1, 1, 2.
    - Isotropy classes: D3d (4 conjugates, axial, normaliser D3d acting trivially, I₃ ≠ 0 → transcritical-type if
      κ ≠ 0); D2h (3 conjugates, axial, normaliser D4h containing −1 → pitchfork-type); C2h (6 conjugates, two-
      dimensional fixed space, not axial); Ci (generic).
  - VERIFIED-NUMERIC: the critical vectors satisfy H e = 0 to 10⁻⁴⁰ at six P_T points, and P_T agrees with Paper 2's
    code.
  - The Ihrig statement is recorded correctly, as a stability statement.
- **Contradictions** with the external brainstorm (C1–C7): `docs/CONTRADICTIONS_EXTERNAL_BRAINSTORM.md`. The main one
  is r* ≈ 2.66 versus the frozen 1.4749107381….
- **Tests and controls:**
  - pytest: 75 passed (17 A0, 32 A1, 21 B0, 5 documentation; Paper 2 archive present).
  - Negative controls: 9 of 9 mutations detected.
- **Not done:** nothing was frozen, published or pushed. Proposed next phases: A2 (Lemma M by proof or Arb
  certificate), A3 (global T_d branch and its index), B1 (κ on the P_T curve; D2h quartic data).

## 2026-11-13 — V0.2-dev: Phase A2 (Lemma M certificate, Corollary M, Theorem A)

- **Request:** "Proceed with Phase A2 only. Do not start B1 yet." The goal was to prove or certify Lemma M, preferably
  on the whole of (0, 3.2], without changing the A0/A1 mathematics. Status is now **RESEARCH / V0.2-dev**: Theorem A is
  proved computer-assisted and **not independently audited**.
- **A0/A1/B0 unchanged:**
  - Their code and tests are byte-identical to V0.1-dev.
  - Regenerated, their JSON files differ from V0.1-dev only in the status and version fields.
  - `A1_sign_table.csv` is byte-identical.
- **Exact derivative (VERIFIED-EXACT):**
  - m = N/(16S²), with S = 3x + y + 3 ≥ 3.
  - m′ = Ψ/(16S³), where Ψ = S·N′ − 2N·S′ has 54 terms; m″ = Φ/(16S⁴), where Φ has 138 terms.
  - Two independent derivations agree: the chain rule with partials, and x, y treated as functions of r.
  - The closed form has no division by r (identity tested).
- **Near r = 0 (exact plus CERTIFIED):**
  - m′(0) = 18/49 + (12/49)log 2 + (57/784)log 3 = 0.61697086623 > 0.
  - m″(0) = 45/98 − (9/1372)L2 + (261/5488)L3 − (6/343)L2² + (363/5488)L2L3 − (285/10976)L3² = 0.51751007587.
  - m″ > 0 on [0, 1/8], certified on 8 boxes. So m′ ≥ m′(0) there.
- **Lemma M certificate (CERTIFIED):** m′(r) > 0 on [0, 16/5].
  - Arb via python-flint 0.9.0 (FLINT 3.6.0) at 128 bits, with the mean-value box test.
  - Recursive bisection gave 64 boxes [k/20, (k+1)/20], with exact rational endpoints, gap-free; maximum depth 6.
  - Dyadic lower bounds on a 2⁻²⁰ grid, each confirmed by a strict Arb comparison.
  - **Minimum certified lower bound: 161457/262144 ≈ 0.6159096**, on [0, 1/20]. The largest is ≈ 1.509.
  - About 0.5 s.
  - Semantic SHA-256: 49dce160b2a17a9f61554200617b9a75b5b02e244e21963b5956317156b6a71e. The provenance block is
    excluded from the hash; the hash is the same after every regeneration.
- **Independent checker** (`certcheck.py`, 160 bits): it uses its own derivation and its own Arb evaluator. It
  confirmed all 64 boxes without refinement, and checked:
  - the claim and the expressions;
  - coverage and the lower bounds;
  - the near-zero and P_A blocks;
  - the hash.
- **P_A(q) < 16/5 (CERTIFIED plus Lemma A):** h_A(16/5) = −0.88588385… < −6/7, and h_A′(16/5) = −0.30983 < 0. The
  certified enclosures of P_A(0⁺) and r* contain the frozen values.
- **Tests of the certificate:**
  - Every box is reconstructed, and coverage and positivity are checked.
  - 12 kinds of tampered certificate are rejected: a gap, an overlap, a shortened start, an extended claim, a flipped
    relation, a non-positive bound, a negated Ψ, an altered m, an altered Φ, an inflated bound, a hash mismatch, and a
    wrong hash file.
- **Negative controls for the method:**
  - On [7, 8] it fails at r = 7.6490136855, the zero of m′. It also fails on [8, 9], for −m′, and for m′ > 31/50 on
    [0, 1/10].
  - [1, 2] is certified.
- **Corollary M — PROVED (computer-assisted):** c₄(q) ≥ (16/3)·L_min·qW_q·(P_A(q) − q) > 0 for every q ∈ (0, r*).
- **Theorem A — PROVED (computer-assisted; not independently audited):** NOTES §3.9; the former Theorem candidate A.
  - It cites (H0) analyticity and invariance, (H1) Z₂ evenness, (H2) the one-dimensional kernel modulo rigid motions
    (Paper 2 Theorem 4′), (H3) transversality (Paper 2 Lemma A), and (H4) c₄ > 0 (Corollary M).
  - **The branch side comes from the reduced equation.** G_μ = λ′(0) < 0 and G_s = c₄/6 > 0, so
    μ*′(0) = −c₄/(6λ′(0)) > 0 and the T_d branches exist only for p > P_A(q).
  - On the branch ∂²_aV_red = 2a²G_s > 0, and at the cube it is λ(μ) < 0: a supercritical pitchfork in the energy
    sense.
  - The dependency graph is machine-readable (`src/cube_bif/theorem_a.py`, `data/A2_theorem_A_dependencies.json`).
    It is tested to be closed and acyclic, every named test exists, and no numerical check is a dependency.
- **Numerical corroboration (not used in the proof):**
  - The amplitude law a² = 6qW_q|h_A′|μ/c₄ matches the located T_d branch to a relative 5.0·10⁻⁸, 3.8·10⁻⁸ and
    2.8·10⁻⁸ at q = 0.2, 0.8, 1.3 (μ = 10⁻⁷P_A).
  - Along the family, f″(0) > 0 > f″(u_branch) ≈ −2f″(0) for p > P_A, and f″(0) < 0 for p < P_A.
- **Tests and controls:**
  - pytest: **130 passed** with the Paper 2 archive present (17 A0, 32 A1, 12 A2 Lemma M, 24 A2 certificate,
    17 A2 Theorem A, 21 B0, 7 documentation).
  - Without the archive: 128 passed, 2 skipped (the two Paper 2 code cross-checks).
  - Negative controls: **17 of 17** mutations detected (9 from V0.1-dev, 6 on the A2 generator and checker, 2 on the
    Theorem A graph). With no mutation, the targeted tests pass in a copy without `data/`.
- **Not done:** nothing was frozen, published or pushed, and Paper 2 is untouched. B1 is not started. Proposed: an
  independent replay of the A2 certificate before Theorem A is relied on, then A3 and B1.

## 2026-11-13 — V0.2.1-dev: documentation/audit patch after the independent Track A audit

- **Status:** RESEARCH / V0.2.1-dev. No mathematical changes.
- **Audit received:** Kimi Agent, blind audit of `EIT_LJ_CUBE_BIFURCATIONS_V0.2-dev.zip` (SHA-256 ba835b0d…91e30).
  - The report came in `Kimi_Agent_Blind_Theorem4_Proof_Audit_1.zip` (SHA-256 e2b2a144…72e8). The auditor dated it
    2026-11-14.
  - It is kept byte-identical in `audits/`.
  - Verdict: PASS WITH MINOR DOCUMENTATION CORRECTIONS. There was no CRITICAL or MAJOR finding, and no mathematical,
    certificate or hypothesis correction.
- **Independent checks in the audit:**
  - A separate reproduction: 128 passed and 2 skipped (no Paper 2 archive), controls 17/17, and the same semantic
    certificate hash.
  - An MPFR directed-rounding re-certification of all 64 recorded lower bounds, written separately (192 bits,
    128 half-boxes, 0 failures).
  - Exact A0/A1 re-derivations without the package code, including the exact on-curve quartic identity.
  - A traversal of the 35-node dependency graph.
- **Corrections (documentation only):**
  - MINOR-01: the T_d branch configurations are two concentric regular tetrahedra of unequal radii on
    inversion-related vertex-direction sets. Spatial inversion exchanges the complete configurations x₊ and x₋, not
    the shells within one configuration (NOTES §2 item 7 and §3.9, README).
  - MINOR-02: the negative-control count in NOTES §3.7 is now 17/17.
- **Status after the corrections:** Theorem A and Corollary M are PROVED (computer-assisted) · INDEPENDENTLY AUDITED,
  and Lemma M is CERTIFIED · INDEPENDENTLY AUDITED. The audit is summarised in NOTES §3.10; `CHANGELOG.md` is new.
- **Version metadata (strings only):**
  - `__version__` 0.2.1.dev0, `STATUS` and the docstring status sentence in `src/cube_bif/__init__.py`;
  - `THEOREM_STATUS` in `src/cube_bif/theorem_a.py`, with the matching `status` field in
    `data/A2_theorem_A_dependencies.json`;
  - the version and status assertions in `tests/test_docs.py`.
- **Mechanical diff check against the V0.2-dev archive** (`docs/V0.2.1-dev_DIFF_CHECK.md`): every other source file,
  script and test, the certificate JSON, its semantic hash file and all other data are byte-identical. The data were
  not regenerated, so their embedded version fields still read 0.2.0.dev0.
- **Verification:**
  - pytest: 130 passed with the Paper 2 archive; 128 passed and 2 skipped without it.
  - Negative controls: 17/17, run in a scratch copy, whose output equals the stored `negative_controls.json`.
  - Certificate replay: 64/64 boxes, no refinement, semantic hash 49dce160…6a71e unchanged.
- **Next:** B1, the cubic coefficient κ(q) = D³V[e₁, e₂, e₃] on p = P_T(q): decide whether κ(q) ≠ 0 on the whole T2g
  curve. Then, separately, the D2h quartic coefficient. B1 is not started. Nothing was frozen, published or pushed, and
  Paper 2 is untouched.

## 2026-11-13 — V0.3-dev: Track B, Phase B1 (cubic coefficient on the T2g curve)

- **Request:** "Proceed with Track B, Phase B1 only", with V0.2.1-dev as the read-only audited baseline for Track A.
  - Status: **RESEARCH / V0.3-dev**.
  - Theorem A and Corollary M stay PROVED (computer-assisted) · INDEPENDENTLY AUDITED, and every Track A file is
    byte-identical with V0.2.1-dev.
  - B1 is labelled VERIFIED-EXACT, VERIFIED-NUMERIC or CERTIFIED, and is not independently audited.
- **B1.1, exact:**
  - The 216 trilinear values on the six T2g basis vectors were computed first. 48 are nonzero, only on permutations of
    (1, 2, 3). Each channel is index-symmetric, and the mixed channels coincide.
  - Four coefficients remain:
    - t_uuu = −12ψ″(2) − 12ψ″(3) − 32ψ‴(3);
    - t_uuv = −√2(10ψ″(3) + 16ψ‴(3));
    - t_uvv = −8ψ″(1) − 8ψ″(3) − 16ψ‴(3);
    - t_vvv = −8√2ψ‴(3).
  - Route 2 (raw 24-D SymPy, 800 tensor entries) agrees exactly, and D³V[x, x, x] = 6κ·a₁a₂a₃ for x = Σa_k e_k.
- **B1.2, exact:**
  - Each coefficient is qW_q[g_m(p) − g_m(q)] with closed g_m, so κ = qW_q(p − q)κ̂.
  - The curve is D̃ = det M̂ = 0, with M̂ the divided-difference block.
- **B1.3:**
  - The chart is n = (1, ρ), ρ = −M̂₁₂/M̂₂₂. M̂₂₂ > 0 is certified on the whole curve, so one chart covers it.
  - The B0 gauge is the negative of the chart gauge.
- **B1.4, endpoint limits:**
  - κ̂(0⁺) = 0.0028795125799552 (P_T(0) = 4.796368189344416004…).
  - κ̂(q_c⁻) = 0.0068917823096484.
  - Raw κ vanishes linearly at both ends.
- **B1.5:** route 3 (mpmath differentiation of the 24-D energy) agrees at six curve points to a relative 4·10⁻³⁸.
- **B1.6, candidate scan** (401 points):
  - κ̂ goes from 0.00287951 at q = 0 to 0.00689178 at the corner. It is increasing, with no sign change.
  - ρ ∈ [0.0197, 0.0278]; M̂₂₂ ∈ [1.456, 1.513]; ∂D̃/∂δ ∈ [−0.108, −0.064]; dP_T/dq ∈ [−1.94, −1.00].
- **B1.7, certificate (CERTIFIED):**
  - Arb at 128 bits on q ∈ [0, 101/50], 222 rational boxes, maximum depth 2.
  - Interval Newton encloses the curve; there are 170 far boxes and 52 near-diagonal Taylor-form boxes.
  - Minimum certified κ̂ = 1311719/536870912 ≈ 0.0024433.
  - Endpoints certified: κ̂(0) and κ̂(corner), each to about 10⁻²⁸.
  - The corner box is identified with the physical curve through Paper 2's Lemmas T2 and T3.
  - Semantic SHA-256: 616817fcc70e0fab7f106404e5e5332b17b9c4480bd440355f1ac5257a8518c6.
  - Independent checker (160 bits, its own derivation and evaluator, Taylor order 20): 222/222 Newton inclusions and
    carrier bounds confirmed, without refinement.
  - 15 kinds of tampered certificate are rejected.
  - Method controls:
    - false bound > 3/1000: fails at q = 0;
    - 9/2000 − κ̂: fails at [9473/20480, 4737/10240], next to its root 0.462937;
    - raw κ: fails at q = 0 and at the corner;
    - wrong kernel vector: fails;
    - the true carrier on [1/2, 1]: certified.
- **B1.8:** transversality τ < 0 for all 0 < q < q_c comes from Paper 2's Lemma T1 (tr K > 0) and Lemma T3
  (∂_pD < 0), with the exact identity ∂_pD = tr(N)·n^T M′ n. No new certificate was needed.
- **B1.9:**
  - Proposition B1 (CERTIFIED): in y* + Fix(D3d) (three-dimensional, no rigid motions) the reduced equation is
    G(s, μ) = λ_red(μ) + κ(μ)s + O(s²), with λ_red′(0) = τ.
  - The implicit function theorem gives s* = −(τ/κ)μ + O(μ²) on both sides of the curve: transcritical. In the chart
    gauge, s* > 0 for p > P_T.
  - To first order, the cube is compressed along a body diagonal for p > P_T and elongated for p < P_T.
  - Numerical corroboration at q = 0.3, 1.0, 1.8: Newton in Fix(D3d) finds equilibria with |∇V| < 10⁻⁴⁹, s has the
    sign of μ, and |s/s* − 1| = O(μ).
  - Ihrig's theorem was not used, and no stability is claimed.
- **B1.10:** the D2h parity is retained (an element maps (1, 0, 0) to −(1, 0, 0)). D2h was not started, and the
  configurations are not called cuboids.
- **Google note** (relayed with the request): recorded in `docs/CONTRADICTIONS_EXTERNAL_BRAINSTORM.md` (G1–G5).
  - Correct: gerade T2g and I₃; the factor p − q.
  - Not as stated: a certificate for raw κ on (0, q_c]; Ihrig as the reason for transcriticality; a link from D2h to
    Paper 2's cuboids.
- **Tests and controls:** pytest 195 (A0 17, A1 32, A2 53, B0 21, B1 65, docs 7). Negative controls 24/24 (17
  earlier + 7 B1 mutations).
- **Not done:** nothing frozen, published or pushed; Paper 2 untouched; B2 (D2h quartic coefficient, stability) not
  started.

## 2026-11-13 — V0.3.1-dev: audit-status patch after the independent B1 audit

- **Status:** RESEARCH / V0.3.1-dev. No mathematical changes. Lemma K and Proposition B1 are CERTIFIED · INDEPENDENTLY
  AUDITED.
- **Audit received:** Kimi Agent, audit of V0.2.1-dev (3bd6ac42…91e30) and V0.3-dev (3901c0db…128fe).
  - The report came in `Kimi_Agent_Blind_Theorem4_Proof_Audit_2.zip`
    (SHA-256 1058e2a12b545e7ca3208ba8d8c562f0712c047c10625cb64a5cba7a672333e0).
  - The report is `CUBE_BIFURCATIONS_V03_REVIEWER_REPORT.md`
    (SHA-256 82bd4f21630a20481113702a9f49dddfa6327f2baf3c07a131af259c1baa65e5), dated 2026-11-14 by the auditor.
  - Both hashes were computed here and match the values the author relayed.
  - The archive's copy of the Track A report is byte-identical to `audits/CUBE_BIFURCATIONS_REVIEWER_REPORT.md`.
  - Verdict: PASS. No defect of any severity; no correction required.
- **Independent checks in the audit:**
  - Identity rows of both earlier diff reports. The extracted NOTES §§1–3.10 hash 7fde8afa… also matches this
    project's own extraction.
  - Reproduction: 130 and 195 passed; controls 24/24; unchanged semantic hashes.
  - A direct 24-coordinate re-derivation of the trilinear structure, the closed forms and the factorisation.
  - A standalone 192-bit, order-24 replay of Lemma K: 222/222 boxes, both endpoints, the corner identification.
  - The transversality chain, the D3d fixed space and reduction, and the sign −τ/κ > 0.
- **Observation recorded in NOTES §5.11:** the generator and the internal checker share the near-diagonal Taylor
  method. The audit used its own derivative enclosures. B2 should give its checker an enclosure method of its own.
- **Hash relayed without a match:** a value 49a73fa004d9d5b6d6a92e1771c7f63aef10d776b479976479584ba82a40a428 was
  relayed with the audit. It matches no archive, upload, audit file or project file available here, and it is not
  recorded as the hash of any artifact.
- **Correction of a value in the V0.3-dev hand-over message (not in any file):** the B1 semantic hash was abbreviated
  there as "616817fc…20ef4". The correct value, in the data files and in the audit, is
  616817fcc70e0fab7f106404e5e5332b17b9c4480bd440355f1ac5257a8518c6.
- **Mechanical diff check against V0.3-dev** (`docs/V0.3.1-dev_DIFF_CHECK.md`): all B1 mathematics, the
  certificates, source, tests and data are byte-identical. The B1 mathematical sections of NOTES are compared
  section by section.
- **Not done:** nothing frozen, published or pushed; Paper 2 untouched; B2 not started.

## 2026-11-13 — V0.4-dev.1: Phase B2 started (B2.0 and B2.1)

- **Status:** RESEARCH / V0.4-dev.1. Track A stays PROVED (computer-assisted) · INDEPENDENTLY AUDITED for Theorem A
  and Corollary M; Lemma K and Proposition B1 stay CERTIFIED · INDEPENDENTLY AUDITED. B2 is not certified, proved or
  audited.
- **Request:** the B2 plan relayed by the author from his review gate (attachment of 2026-11-13). Order B2.0 → B2.5;
  this version does B2.0 and B2.1 only and stops before B2.2. Roles in the plan: Google as red team only, this project
  as the main derivation, Kimi as blind auditor once B2 is complete.
- **B2.0 (exact):**
  - The stabiliser of e₁, computed in 24-D for symbolic n, is the D2h with C2 axes x, (0,1,1), (0,1,−1); it equals
    B0's 3×3 stabiliser of (1, 0, 0).
  - Fix_{R²⁴}(D2h) has rank 4: A1g 1, Eg 1, T2g 2 (one per copy), all other irreps 0; the character formula agrees.
  - The relayed Google claim span{e_crit, A1g, Eg⁽¹⁾, Eg⁽²⁾} is not correct: Eg⁽²⁾ is not fixed and f₁ is missing
    (G6 in `docs/CONTRADICTIONS_EXTERNAL_BRAINSTORM.md`). The review gate had flagged the two T2g copies.
  - b = D³V[e₁, e₁, ·] ∈ A1g ⊕ Eg exactly, for every pair potential and every n; ⟨b, f₁⟩ = ⟨b, e₁⟩ = 0 exactly. The
    reason is Schur's lemma on Sym²(T2g); Σ-invariance alone would allow an f₁ component.
  - The normaliser (D4h) acts on Fix by diag(1, 1, −1, −1): the axial reduced potential is even.
  - First order: the cross-sections become rhombi and the tetrahedra shift along x. e₁ is orthogonal to the cuboid
    family Fix(Z₂³) (G5, update).
- **B2.1:**
  - c₄ = D⁴V[e₁⁴] − 3b_A²/h_A − 3b_E²/h_E = qW_q(p − q)ĉ₄, with 13 closed forms; h_A, h_E are Paper 2's A1g and Eg
    blocks, positive by Lemma S (added to `reference/PAPER2_INPUTS.md` with Lemma T1).
  - Three routes at q = 0.05, 0.5, 1.0, 1.5, 2.0 (60 digits): route 2 (raw 24-D, spectral solve) agrees with route 1
    to ≤ 8.2·10⁻⁶⁰ relative; route 3 (restricted D2h family, its own curve point, Newton reduction, Richardson) to
    ≤ 9.5·10⁻³⁷. Route 3 also reproduces tr K, h_A, h_E as its nonzero eigenvalues and ±e₁ as its kernel.
  - ĉ₄ at these points: 3.8339, 4.0838, 4.2570, 4.3483, 4.3770. The back-reaction lowers it by 1.3–5.1 %. No sign
    claim on the curve; no scan, endpoint limit or certificate (B2.2, B2.3).
- **Tests and controls:** pytest 261 (A0 17, A1 32, A2 53, B0 21, B1 65, B2 65, docs 8). Negative controls 34/34
  (24 earlier + 10 B2 mutations).
- **Identity:** every Track A, B0 and B1 file is byte-identical with V0.3.1-dev (`docs/V0.4-dev.1_IDENTITY_CHECK.md`).
- **Not done:** nothing frozen, published or pushed; Paper 2 untouched; B2.2–B2.5 not started.

## 2026-11-13 — V0.4-dev.2: Phase B2.2 (carrier reconnaissance)

- **Status:** RESEARCH / V0.4-dev.2. B2.2 = VERIFIED-NUMERIC / RECONNAISSANCE.
  - Theorem A and Corollary M stay PROVED (computer-assisted) · INDEPENDENTLY AUDITED.
  - Lemma K and Proposition B1 stay CERTIFIED · INDEPENDENTLY AUDITED.
  - B2 is not certified, proved or audited.
- **Gate:** the review gate passed B2.0/B2.1 and asked for B2.2 only (endpoints, corner, conditioning, a scan of at
  least 401 points, an independent route, falsification), with no certificate, no branch type and no B2.4/B2.5.
- **Endpoints:**
  - q = 0 from its own formulation: f̂ = (f(p₀) − f(0))/p₀ with exact f(0). p₀ was refined at 100 digits inside
    Paper 2's enclosure, and also lies inside the tighter enclosure of Paper 2's blind audit.
    ĉ₄(0) = 3.7993380378668858157102270287692…
  - Corner from exact derivative closed forms, with B1's chart ρ_c; q_c was refined at 100 digits inside Paper 2's
    enclosure. ĉ₄(q_c) = 4.3770354906131219361130218849453…
  - The corner expression contains no p − q. Its denominators at q_c are W 1.6065, M′₂₂ 1.4555, g′_hE 1.9983 and
    1 + ρ_c² 1.00077.
  - The approach is linear at q = 0 (slope 0.70628) and quadratic at the corner (−0.098749(q_c − q)²). The second
    follows from the p ↔ q symmetry.
- **Scan:** 401 points q_k = k q_c/400, with the endpoint formulations at k = 0 and 400.
  - Minimum 3.79933803786688581571 at q = 0; maximum 4.37703549061312193611 at the corner.
  - No sign change; strictly increasing on the grid.
  - Denominator minima: ĥ_E 1.998317 (corner), M̂₂₂ 1.455508 (corner), 1 + ρ² 1.000389 (q = 0), |∂D̃/∂δ| 0.064338
    (q = 0).
- **Independent route:** raw 24-D, with its own curve point and kernel from the restricted 4×4 Hessian. At the
  endpoints it uses the limit potentials φ₀ = 7/(3pW_p) r^−p + log r and φ_c = −(1/q + W′/W + log r) r^−q, and from
  them it finds p₀ (to 2·10⁻⁵⁶) and q_c (to 4·10⁻⁵⁷) by itself. It agrees at 6 interior points and both endpoints to
  ≤ 1.2·10⁻⁴⁸. The nonlinear endpoint checks agree to ~10⁻³⁶.
- **Falsification:** 7/7 false statements exposed (a bound 10⁻⁶ above the minimum; Eg deleted; factor 3 → 2; wrong
  normalisation; kernel (1, −ρ); values instead of derivatives at the corner; raw c₄ ≠ 0 at the ends).
- **Tests and controls:**
  - pytest 280 (A0 17, A1 32, A2 53, B0 21, B1 65, B2 65, B2.2 19, docs 8).
  - Code-mutation controls 43: the 34 earlier ones unchanged, plus 9 B2.2 mutations in a separate script, all
    detected by assertions.
- **Identity:** everything earlier is byte-identical with V0.4-dev.1 except documentation and version strings
  (`docs/V0.4-dev.2_IDENTITY_CHECK.md`).
- **Not done:** no Arb certificate, no branch classification, B2.4/B2.5 not started; nothing frozen, published or
  pushed (GitHub and Zenodo on hold); Paper 2 untouched.

## 2026-11-13 — V0.4-dev.3: Phase B2.3 (certificate: Lemma Q)

- **Status:** RESEARCH / V0.4-dev.3. Lemma Q (ĉ₄ > 0 on the closed physical T2g curve) and its corollary
  (c₄ > 0 for 0 < q < q_c) are CERTIFIED (computer-assisted; not independently audited).
  - Theorem A and Corollary M stay PROVED (computer-assisted) · INDEPENDENTLY AUDITED.
  - Lemma K and Proposition B1 stay CERTIFIED · INDEPENDENTLY AUDITED.
- **Gate:** the review gate passed B2.2 and asked for B2.3 only: positivity of ĉ₄ on the closed curve with the
  corollary, the B1 curve boxes reused under a pinned hash, direct endpoint certificates, an independent checker of a
  different architecture, tamper tests and controls. No monotonicity, no branch type, no B2.4/B2.5.
- **Curve:** B1's 222 boxes and δ-balls imported unchanged (semantic hash 616817fc…8518c6 pinned in the generator and
  the checker). The certificate records its import checks (coverage, order, balls, hashes, corner box). Both programs
  re-verify every ball by interval Newton.
- **Generator** (128 bits): quotient far from the diagonal (170 boxes), an even symmetric series with Lagrange
  remainder near it (52 boxes). All 222 boxes certified without splits; the smallest recorded bound is
  955723/262144 ≈ 3.6458 (first box). ĥ_E ≥ 1985555/1048576 and M̂₂₂ ≥ 362177/262144.
- **Endpoints:** q = 0 from the exact values at r = 0 and B1's P_T(0) ball, ĉ₄(0) ∈ [3.79933803786688581571022702877
  ± 7.9·10⁻³¹]; the corner from f′(q_c), ĉ₄(q_c) ∈ [4.37703549061312193611302188495 ± 4.6·10⁻³⁰]. Both contain the
  B2.2 values. The raw c₄ is recorded as exactly 0 at both.
- **Checker** (192 bits, no Taylor series, no project imports): its own derivation (16/16 expressions agree), the
  integral f̂ = ∫₀¹ f′(q + t(p − q)) dt by the midpoint rule with remainder and centred box forms, the v-form kernel
  with ‖v‖⁴. Result: 222/222 balls re-verified, 222/222 boxes confirmed at 32 subintervals, 222/222 centre values
  inside the stored enclosures.
- **Controls:** 23 consistent forgeries rejected; 15/15 method controls as required (false bound 19/5, false function
  21/5 − ĉ₄, raw c₄ at both ends, four wrong variants, positive controls); 24/24 code mutations detected.
- **Finding:** python-flint truncates arb_series at ctx.cap (default 10). B1's generator and checker pad truncated
  series with zeros: at (1.9, 0.9) their default-cap near-regime enclosures miss the true divided differences by up
  to 2.8·10⁻⁹. The stored B1 certificate passes B1's checker with complete series and the B2.3 re-verification; a
  corrected rebuild is valid but has other bytes. B1 unchanged; erratum proposed (NOTES §9.8).
- **Tests and controls:**
  - pytest 330 (A0 17, A1 32, A2 53, B0 21, B1 65, B2 65, B2.2 19, B2.3 50, docs 8).
  - Code-mutation controls 67: the 43 earlier ones unchanged, plus 24 B2.3 mutations in a separate script.
- **Identity:** everything earlier is byte-identical with V0.4-dev.2 except documentation and version strings
  (`docs/V0.4-dev.3_IDENTITY_CHECK.md`).
- **Not done:** no monotonicity claim, no branch classification (B2.4), no centre-manifold index (B2.5); the B1 erratum
  is not applied; nothing frozen, published or pushed (GitHub and Zenodo on hold); Paper 2 untouched.

## 2026-11-14 — V0.4-dev.4: B1 implementation erratum E-B1 (series length)

- **Status:** RESEARCH / V0.4-dev.4. B1 (Lemma K, Proposition B1): CERTIFIED · INDEPENDENTLY AUDITED · IMPLEMENTATION
  ERRATUM PENDING TARGETED RE-AUDIT. Theorem A and Corollary M stay PROVED (computer-assisted) · INDEPENDENTLY
  AUDITED; Lemma Q stays CERTIFIED (computer-assisted; not independently audited).
- **Gate:** the author authorised the B1 erratum only (proposed in NOTES §9.8): fix the two Taylor routines, add
  regression tests, keep the historical certificate, replay it, rebuild separately, cross-check with B2.3, document.
  No B2.4/B2.5, no change to Paper 2.
- **Reproduced before the patch** on the unmodified V0.4-dev.3 archive (cf331557…5c81): python-flint returns 10
  coefficients for a requested 16; c₁₀ onwards come back as exact zeros in both routines; at (1.9, 0.9) all seven
  near-regime enclosures of both routines exclude the 60-digit quotient (worst g_uvv, off by 2.8·10⁻⁹). In this
  environment the unmodified generator reproduces the historical semantic hash 616817fc… under run_B1.py's conditions.
- **Correction:** ctx.cap raised to the requested length in a restoring context manager, explicit truncation checks,
  zero padding only after a longer recomputation shows exact zeros. Independent implementations in the generator and
  the checker.
- **Evidence for the stored certificate:** corrected checker 222/222 inclusions, 222/222 carrier bounds, endpoints
  accepted, bound unchanged; fresh corrected rebuild b2f8e6dc… (52 near boxes differ, 170 far boxes identical, same
  bound and endpoints, stored separately); B2.3 Taylor-free checker 222/222 balls with neither affected routine loaded.
- **Tests and controls:** pytest 345 collected, 343 passed, 2 skipped (Paper 2 archive absent). Erratum mutation
  controls 13/13 as required, including the restored V0.4-dev.3 routines and ctx.cap = 10. Existing controls
  34/34, 9/9, 24/24 detected, records byte-identical; B1 6/6 and A2 5/5 method controls as required. Identity check
  against V0.4-dev.3 PASS, 41/41 forbidden modifications rejected.
- **Not done:** the targeted independent re-audit (Kimi) is pending, so the erratum is not closed; B2.4/B2.5 not
  started; nothing frozen, published, pushed or uploaded (GitHub and Zenodo on hold); Paper 2 untouched.

## 2026-11-14 — V0.4-dev.5: erratum E-B1 closed; B2.4, Proposition B2

- **Status:** RESEARCH / V0.4-dev.5. B1 (Lemma K, Proposition B1): CERTIFIED · INDEPENDENTLY AUDITED · ERRATUM CLOSED.
  Proposition B2 (B2.4): PROVED (computer-assisted; not independently audited). Lemma Q stays CERTIFIED
  (computer-assisted; not independently audited). Theorem A and Corollary M stay PROVED (computer-assisted) ·
  INDEPENDENTLY AUDITED.
- **Re-audit received:** Kimi Agent's targeted re-audit of erratum E-B1 (report ba482da0…, PASS): defect real, patch
  correct, historical certificate valid, fresh rebuild b2f8e6dc… proves the same Lemma K claim, Taylor-free B2.3
  route 222/222; the erratum may be marked CLOSED. Added byte-identical to `audits/`; no B1 file changed.
- **Gate:** the author authorised B2.4 only: the local branch structure on the D2h axis. No B2.5, no change to
  Paper 2, no freeze or publication.
- **Derivation:** generic Z₂-invariant Lyapunov–Schmidt expansion on the 4-D fixed space (exact, 35 free
  coefficients). It gives V_red = V₀ + ½λs² + (c₄/24)s⁴ + O(s⁶), with λ the Schur complement of K (λ′(0) = τ) and c₄
  the B2.1 coefficient; G = λ + (c₄/6)z + …; μ*′(0) = −c₄/(6τ) > 0. So the pair ±s* exists only for p > P_T(q), with
  s² = −(6τ/c₄)μ + O(μ²). It is a Z₂ pitchfork, supercritical in the energy-reduced axial convention. Axial curvature:
  τμ at the cube, −2τμ at ±s*. Isotropy exactly Σ; rhombic sections at first order.
- **Dependency graph:** machine-readable and validated. Its leaves are exactly the six inputs the request allows;
  every other node is a VERIFIED-EXACT step of this phase. A first draft named Paper 2's Lemmas S, T1, T3, the B0
  basis, analyticity and symmetric criticality as extra leaves; they are now listed inside the allowed inputs they
  belong to (as recorded in §5.8, §6.2, §9.1, §12.2), and the validator rejects any extra input. The B2.2 scan and
  the B2.4 numerics are corroboration only.
- **Numerical corroboration:** q = 0.2, 0.8, 1.5, 2.0; r = ±10⁻⁶, ±10⁻⁷. Both ±s* are found for μ > 0, with the 24-D
  gradient below 10⁻⁵⁹; for μ < 0 Newton from the mirror amplitude returns to the cube (|s| ≤ 7·10⁻⁵³). The amplitude-law error is O(μ) (ratio 10.0000), and the reduced scans
  show one sign change for μ > 0 and none for μ < 0. 88/88 checks pass.
- **Tests and controls:**
  - 51 new tests, including 21 rejected statements and 10 rejected graphs;
  - code-mutation controls 22/22 detected;
  - the earlier control suites (Track A/B1 34, B2.2 9, B2.3 24, erratum 13) were not re-run in V0.4-dev.5: every
    file they mutate or test, and their records, is byte-identical with V0.4-dev.4, where they were re-run
    (identity check below);
  - full suite: 397 collected, 395 passed, 2 skipped (Paper 2 archive not in the package);
  - identity check against V0.4-dev.4: PASS; 45/45 forbidden modifications rejected.
- **Not done:** B2.5 (centre-manifold index) not started; no full-space stability, no cuboid claim; B2.3 and B2.4
  not independently audited; nothing frozen, published, pushed or uploaded (GitHub and Zenodo on hold); Paper 2
  untouched.

## 2026-11-15 — V0.4-dev.6: B2.5, Proposition B3 and Corollary B3′

- **Status:** RESEARCH / V0.4-dev.6. Proposition B3 and Corollary B3′ (B2.5): PROVED (computer-assisted; not
  independently audited). B1 stays CERTIFIED · INDEPENDENTLY AUDITED · ERRATUM CLOSED; Track A unchanged.
- **Gate:** the author authorised B2.5 only (the Morse index of the 3-D centre-manifold reduced Hessian on the D2h
  branch, then a full-slice corollary only if the frozen Paper 2 signs determine it). No global branch problem, no A3,
  no C2h study, no change to Paper 2, no freeze or publication.
- **Input statuses:** the request designates B2.3 and B2.4 as independently audited; no B2.3/B2.4 audit report is in
  the package (NOT_PROVIDED). The labels of §9 and §12 are kept as written; the graph records the designation.
- **Derivation:** invariant theory of the 24-element action on E_c (dimensions 0, 1, 1, 2 in degrees 1–4); exact LS
  quartic αI₂² + βI₄ with α + β = c₄/24; exact axis Hessian form and parity; on the branch h₁₁ = (c₄/3)s²,
  d = −4βs², e = κs, det = −κ²s² (leading orders); remainder bound for the transverse sign; centre index 1, nullity 0.
  m_⊥ = 3 derived from the frozen block signs; Haynsworth additivity gives the slice index 4. D3d consistency: centre
  index 2/1, degree −3 on both sides.
- **Numerical corroboration:** raw 24-D Hessian at 24 D2h equilibria, 8 D3d equilibria, the cube at 4 points of the
  curve, and a derivative-free quartic check: 300/300. The first run had 294/300: six q = 2.0 checks of the O(μ)
  relative error exceeded the initial bound 50·(μ/P_T) (values 51–53); the bound was raised to 200·(μ/P_T) after
  inspection. The separate O(μ) scaling check was unchanged and passes (ratio 10 per decade).
- **Development notes:** a first multi-variable symbolic LS attempt timed out and was replaced by a degree-truncated
  calculation; a matrix right-hand-side solve failure in the numerical Schur complement was replaced by the inverse of
  the complementary block; early quartic mismatches came from inconsistent n_u, n_v symbols and were fixed by sharing
  them with b2_quartic.py. The centre index in the derived statement is read off the derived branch series (h₁₁ and
  determinant coefficients), not set by hand.
- **Tests and controls:** 71 new tests in `tests/test_B2_index.py` (23 false Proposition B3 statements, 11 false Corollary B3′ statements and 12 invalid graphs rejected); code-mutation controls 28/28 detected (15 target tests, each passing unmutated); full suite 469 collected, 469 passed, 0 skipped (run in chunks, with the Paper 2 archive beside the project; without it the 3 archive cross-checks are skipped). The earlier control suites (34, 9, 24, 13, 22) were not re-run: every file they mutate or test, and their records, is byte-identical with V0.4-dev.5.
- **Identity check against V0.4-dev.5:** PASS; 62/62 forbidden modifications rejected (the 44 dev.5 controls plus 18 for B2.4 files, earlier reports, audits/README.md, NOTES §11–§12, the CHANGELOG dev.5 entry, version values, an extra file and a stale manifest).
- **Not done:** independent audit of B2.5 (and the B2.3/B2.4 audit reports); explicit radii; release preparation;
  nothing frozen, published, pushed or uploaded (GitHub and Zenodo on hold); Paper 2 untouched.

## 2026-11-15 — V1.0.0-rc1: release candidate (audit-status patch, manuscript, release metadata; no new mathematics)

- **Gate:** the author authorised packaging, manuscript and release preparation only: no new mathematics, no A3, C2h,
  Track C or new branches; no freeze, publication, GitHub push, Zenodo upload or Springer submission; no v1.0.0 tag.
  The result is RELEASE CANDIDATE / V1.0.0-rc1 · PENDING FINAL BLIND RELEASE AUDIT.
- **Inputs authenticated:** V0.4-dev.6 (`c473af60…b691`, internal manifest 124/124), frozen Paper 2 V1.0
  (`bb70721d…762d`), and the B2.3, B2.4 and B2.5 audit reports (`841152f2…6bcf`, `0302930b…b1ec`, `bffd4948…165a`).
  All matched. Each report's formal verdict is PASS with no finding requiring correction.
- **Status:** Lemma Q CERTIFIED · INDEPENDENTLY AUDITED. Proposition B2, Proposition B3 and Corollary B3′ — each
  PROVED (computer-assisted) · INDEPENDENTLY AUDITED (Proposition B2, Proposition B3, Corollary B3′). Track A and B1
  unchanged (B1 ERRATUM CLOSED).
- **Authorship:** two authors, Toni Mladenovski (Founder) and Mihail Mladenski (Co-founder), EITNetworks LLC. Mihail
  Mladenski's contribution, ORCID, e-mail and the company city are not in any project source and were not invented.
- **Work:** manuscript (`paper/`), figures from a deterministic script, release metadata, audit index and status matrix,
  JMC drafts, preservation checker against V0.4-dev.6 with forbidden-edit controls, release-text scanner. Counts,
  hashes and open items: `RELEASE_NOTES_RC1.md`.
- **Not done:** the final blind release audit (to be performed by a separate auditor); nothing frozen, published,
  pushed, uploaded or submitted; Paper 2 untouched.

## 2026-11-16 — V1.0.0-rc2: author/institution metadata update (release candidate; no new mathematics)

- Author decision (Toni Mladenovski): produce RC2 because author and institution metadata were supplied after RC1; do
  not overwrite RC1; no new mathematics; no publication, push, upload, submission, tag or freeze.
- Metadata supplied by the author: affiliation of both authors EITNetworks LLC, Tobyhanna, Pennsylvania, USA; Toni
  Mladenovski — Founder, corresponding author, info@eitnetworks.org (secondary tml30993@gmail.com for submission
  metadata), ORCID 0009-0009-8343-662X; Mihail Mladenski — Co-founder, mmladenski077@gmail.com, no ORCID. No
  educational institution is to be listed.
- The project records were searched for a documented scholarly contribution of Mihail Mladenski; none was found, so
  none is stated (`AUTHORSHIP_FINAL_APPROVAL_REQUIRED.md`).
- The result is RELEASE CANDIDATE / V1.0.0-rc2 · PENDING FINAL BLIND RELEASE AUDIT. Changes, QA results, artifact
  hashes and open items: `RELEASE_NOTES_RC2.md`.

## 2026-11-16 — V1.0.0: final release prepared (author-approved declarations; no new mathematics)

- Input: the final blind release audit of V1.0.0-rc2 (`PAPER3_RC2_FINAL_BLIND_RELEASE_AUDIT.md`, SHA-256
  `37b0b4d6…7448`), verdict RELEASE-READY, no blocking finding; supplied by the author as the Kimi
  audit (the report itself does not name the auditing system). Every input archive was authenticated by SHA-256 first
  (RC2, its sidecar, PDF, source ZIP, the corrected RC2 artifact manifest `f96a88d3…6628`, JMC package `d002d5e8…fd00`,
  V0.4-dev.6, Paper 2 V1.0, RC1); all matched.
- Author decision (Toni Mladenovski, stating the approval of both authors): the author-contribution,
  competing-interests and copyright-holder texts are approved as given; NB-03 is closed for final release preparation.
  Produce V1.0.0 locally; do not overwrite RC2; no new mathematics; no publication, push, upload, submission, tag or
  freeze. Next step: an independent RC2 → V1.0.0 delta/preservation audit.
- Zenodo DOI reservation: not performed (no authenticated Zenodo access in this environment); placeholders kept.
- Author correction (second instruction of Toni Mladenovski, same day, before packaging): Mihail Mladenski is not a
  co-founder, owner, member, employee or manager of EITNetworks LLC; the "Co-founder" label is removed from current
  surfaces and the competing-interests text is replaced by the corrected approved wording. His EITNetworks LLC
  affiliation is unchanged. The RC1/RC2 entries above record the metadata as supplied at that time.
- Result: FINAL RELEASE PREPARED / V1.0.0 · PENDING RC2→V1.0.0 DELTA AUDIT. Changes, QA results and open items: `RELEASE_NOTES_V1.0.0.md`.
