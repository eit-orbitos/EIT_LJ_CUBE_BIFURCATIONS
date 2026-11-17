# EIT-LJ Cube Bifurcations (Paper 3) — research notes

**Working title:** Symmetry-Breaking Bifurcations from the Cubic Equilibrium in Two-Term Inverse-Power Clusters
**Status at build time: FINAL RELEASE PREPARED / V1.0.0 · PENDING RC2→V1.0.0 DELTA AUDIT** (2026-11-16). Final blind release audit of
V1.0.0-rc2: RELEASE-READY. Public release not yet executed; not frozen. Authors: Toni Mladenovski and Mihail Mladenski
(EITNetworks LLC, Tobyhanna, Pennsylvania, USA). The mathematics is that of V0.4-dev.6; §17 gives the current status
(§15 and §16 are the RC1 and RC2 records, with the same result statuses). In V1.0.0-rc1 the status labels of §9, §12 and §13 were updated to the audited status; sentences
in §1–§14 that describe the status at an earlier version are marked "at that version" or "when written".
- V0.1-dev (Phases A0, A1, B0) is unchanged.
- V0.2-dev added Phase A2: Lemma M (certified), Corollary M and Theorem A (proved computer-assisted).
- V0.2.1-dev was a documentation/audit patch. Track A passed an independent audit (§3.10):
  Theorem A and Corollary M are **PROVED (computer-assisted) · INDEPENDENTLY AUDITED**.
- V0.3-dev added Track B, Phase B1 (§5): κ ≠ 0 on the whole T2g curve (Lemma K) and the D3d branches are
  transcritical (Proposition B1). Track A is byte-identical with the audited V0.2.1-dev.
- V0.3.1-dev is an audit-status patch with no mathematical changes. Phase B1 passed an independent audit (§5.11):
  Lemma K and Proposition B1 are **CERTIFIED · INDEPENDENTLY AUDITED**.
- V0.4-dev.1 starts Phase B2 (§6) with B2.0, the exact symmetry audit of the D2h axis, and B2.1, the quartic
  coefficient c₄ by three routes. Nothing in B2 is certified, proved or audited, and no sign of c₄ on the curve is
  claimed. Track A, B0 and B1 (§1–5.11) are byte-identical with V0.3.1-dev.
- V0.4-dev.2 adds B2.2 (§7), numerical reconnaissance of the normalised carrier ĉ₄ on the closed curve: both endpoint
  formulations, a 401-point scan, an independent raw 24-D route and falsification checks. B2.0 and B2.1 passed the
  review gate. No sign of ĉ₄ is proved or certified. Everything in §1–6.2 is byte-identical with V0.4-dev.1.
- V0.4-dev.3 adds B2.3 (§9): Lemma Q, ĉ₄ > 0 on the whole closed physical T2g curve, CERTIFIED (computer-assisted;
  not independently audited at that version), and its corollary c₄ > 0 for 0 < q < q_c. B2.2 passed the review gate. §9.8 records a
  finding about B1's Taylor code; the audited B1 certificate is valid and B1 is unchanged. Apart from this header,
  §1–8 are byte-identical with V0.4-dev.2.
- V0.4-dev.4 is a B1 implementation erratum patch only (§10, erratum E-B1). The two B1 Taylor routines did not raise
  python-flint's ctx.cap and zero-padded truncated series; they are corrected, with regression tests. The stored B1
  certificate (616817fc…) is unchanged and re-verified by the corrected checker, by a fresh corrected rebuild and by
  the Taylor-free B2.3 checker. B1 status: at that version **CERTIFIED · INDEPENDENTLY AUDITED · IMPLEMENTATION ERRATUM PENDING
  TARGETED RE-AUDIT**; the erratum is not closed. §0–§9 are byte-identical with V0.4-dev.3 (the section labels of §5
  are those of V0.3.1-dev; §10 gives the current B1 status). Next steps are §11.
- V0.4-dev.5 records the targeted independent re-audit of erratum E-B1 (§11, Kimi Agent, PASS): B1 status
  **CERTIFIED · INDEPENDENTLY AUDITED · ERRATUM CLOSED**. It adds B2.4 (§12):
  **Proposition B2 — PROVED (computer-assisted; not independently audited at that version)**: the D2h-axial branch is a Z₂-symmetric
  pitchfork on the side p > P_T(q), supercritical in the energy-reduced axial convention, with the axial reduced
  curvature only (no centre-manifold index, no full-space stability, no cuboid claim). §1–§10 are byte-identical with
  V0.4-dev.4; in §0 only the sentence on proved statuses changes. The bullets above are historical: §11 gives the current B1 status and
  §13 the next steps. B2.5 is not started.
- V0.4-dev.6 adds B2.5 (§13): **Proposition B3 — PROVED (computer-assisted; not independently audited at that version)**: the
  three-dimensional centre-manifold reduced Hessian at the D2h branch points has index 1, nullity 0; and
  **Corollary B3′ — PROVED (computer-assisted; not independently audited at that version)**: with m_⊥ = 3 derived from frozen Paper 2
  block signs, the full-slice index is 4, nullity 0 (rigid motions excluded). No stability claim. §1–§12 are
  byte-identical with V0.4-dev.5; in §0 only the sentence on proved statuses changes. The bullets above are
  historical; §14 gives the next steps.
- V1.0.0-rc1 is a packaging, audit-status and manuscript release candidate with **no new mathematics** (§15). It
  records the independent audits of B2.3, B2.4 and B2.5 (all PASS): Lemma Q is **CERTIFIED · INDEPENDENTLY AUDITED**;
  Proposition B2, Proposition B3 and Corollary B3′ are **PROVED (computer-assisted) · INDEPENDENTLY AUDITED**. Status:
  RELEASE CANDIDATE at that version (V1.0.0-rc1; superseded by V1.0.0-rc2). In §0–§14 only status labels and
  version markers change ("at that version", "when written"); no mathematical statement, formula or result changes.
- V1.0.0-rc2 updates author and institution metadata, declarations and release tooling, with **no new mathematics**
  (§16). Status at that version: RELEASE CANDIDATE / V1.0.0-rc2 · PENDING FINAL BLIND RELEASE AUDIT; it then passed the
  final blind release audit (RELEASE-READY).
- V1.0.0 inserts the author-approved declarations and copyright wording and sets the final version metadata, with
  **no new mathematics** (§17). Status at build time: **FINAL RELEASE PREPARED / V1.0.0 · PENDING RC2→V1.0.0 DELTA AUDIT**.

Paper 2 (EIT_LJ_FULL_VECTOR_STABILITY, frozen at V0.2-dev.10, public V1.0, DOI 10.5281/zenodo.24187155) is used only
as read-only input. Nothing in this project modifies it. Its frozen statements are quoted with the label FROZEN INPUT.

## 0. Status labels

| label | meaning |
|---|---|
| VERIFIED-EXACT | exact symbolic identity (SymPy, rational/algebraic arithmetic), with its own test |
| VERIFIED-NUMERIC | mpmath at 40–50 digits, with its own test; not a certificate |
| STANDARD | textbook result, cited; its hypotheses are checked here |
| FROZEN INPUT | proved in Paper 2 (frozen, audited); quoted, not re-proved |
| CANDIDATE | expected result; not proved. Its sign or inequality rests on numerical evidence only |
| CERTIFIED | Arb ball-arithmetic certificate (outward rounding), re-verified by an independent checker, with tamper tests and negative controls |
| PROVED (computer-assisted) | every link is VERIFIED-EXACT, CERTIFIED, FROZEN INPUT or STANDARD, each with its own test |
| INDEPENDENTLY AUDITED | passed an external audit (separate reproduction and separate implementation) that required no mathematical or certificate correction; see §3.10 |

Only Corollary M, Theorem A, Proposition B2 (§12, V0.4-dev.5), Proposition B3 and Corollary B3′ (§13, V0.4-dev.6)
carry a proved status, and all five are computer-assisted and independently audited (§3.10, §15). No other statement in this project is called proved. A CANDIDATE becomes a result only after a separate proof or certificate, with its own test.

## 1. Setting and conventions (identical to Paper 2)

- Model: eight particles, pair potential φ(r) = A r^−p − B r^−q, A, B > 0, p > q > 0.
- Labels s ∈ {±1}³ in the order of `itertools.product([-1, 1], repeat=3)`. Configuration x ∈ R²⁴, label-major.
- O_h: the 48 signed permutation matrices R, acting by (D(R)x)_{Rs} = R x_s (Paper 2's D(R); for diagonal R it is
  Paper 2's D2h action).
- **Normalisation used here:** unit-edge cube y*_s = s/2, B = 1, A = t = qW_q/(pW_p), so y* is an equilibrium;
  W_r = 1 + x + y/3 with x = 2^(−r/2), y = 3^(−r/2). Paper 2's normalisation (A = B = 1, edge e = t^(−1/(p−q)))
  multiplies the n-th derivative by the positive factor e^(−q−n), so no sign changes.
- Exact fields: E_br(s) = s (breathing), E_A(s) = (s₁s₂s₃)s (A2u), translations, rotations ε_k × s;
  e_A = E_A/√24, e_br = E_br/√24. Coordinates x = y* + a e_A + b e_br + ….
- Γ₂₄ = A1g + Eg + T1g + 2T2g + A2u + Eu + 2T1u + T2u (VERIFIED-EXACT, character projectors).

## 2. Phase A0 — exact A2u representation audit (all VERIFIED-EXACT)

1. **e_A is exact and normalised:** E_A(s) = (s₁s₂s₃)s, |E_A|² = 24. It is radial at every vertex. The sign alternates
   between the two inscribed regular tetrahedra (even: s₁s₂s₃ = +1; odd: −1).
2. **Orthogonality:** e_A ⟂ the three translations, ⟂ the three rotations, and ⟂ e_br (uniform scaling).
3. **Character:** D(R)e_A = χ_A2u(R) e_A for all 48 R. Here χ_A2u(R) = σ(R) := the product of the nonzero entries of
   R, which is also det(R)·sgn(perm R). The A2u isotypic projector has rank 1.
4. **Stabiliser, computed from the 48 matrices:** Σ_A = {R : D(R)e_A = e_A} has 24 elements: E, 8 C3, 3 C2 (= C4²),
   6 S4 and 6 σ_d, with no inversion. That is the signature of **T_d**. Fix(T_d) = span{e_br, e_A} (rank-2
   projector).
5. **Inversion:** D(−I)e_A = −e_A and D(−I)y* = y*.
6. **Evenness of the reduced potential** (STANDARD equivariant Lyapunov–Schmidt reduction, with VERIFIED-EXACT
   ingredients):
   - V is O_h-invariant: for every R, the multiset of squared pair distances of D(R)x equals that of x (exact check on
     a random rational x).
   - Orthogonal complements of O_h-invariant subspaces are O_h-invariant, and the rigid-motion space T1u ⊕ T1g is
     O_h-invariant.
   - Hence the reduced function on the A2u kernel satisfies V_red(D(−I)·a) = V_red(a), i.e.
     **V_red(a, μ) = V_red(−a, μ)**, and every odd coefficient vanishes (in particular c₃ = 0).
   - As a direct check: V_a, V_ab, V_aaa and V_abb vanish identically, for any pair potential.
   - V_b vanishes only at the equilibrium (A = t); it is not a symmetry zero.
7. **Branch space:** the kernel direction e_A is fixed by T_d. The Lyapunov–Schmidt solution w(a) is unique and
   equivariant, so the bifurcating equilibria x(a) = y* + a e_A + w(a) satisfy D(R)x(a) = x(χ_A2u(R)a). They are
   therefore T_d-symmetric and lie in Fix(T_d) = span{e_br, e_A}. Conversely, by symmetric criticality (Palais), every
   critical point of V restricted to Fix(T_d) is an equilibrium. For a ≠ 0 these configurations are two concentric
   regular tetrahedra of unequal radii ρ₊ ≠ ρ₋ on inversion-related vertex-direction sets. Spatial inversion exchanges
   the complete configurations x(a) and x(−a); it does not exchange the unequal-radius shells within one fixed
   configuration.

## 3. Phase A1 — quartic Lyapunov–Schmidt coefficient on the A2u curve

### 3.1 Exact multilinear forms (VERIFIED-EXACT, valid for any pair potential)

With φ(r) = ψ(r²) and ψ_k(σ) = ψ^(k)(σ) at σ = |r|² ∈ {1, 2, 3}:

    V_aa   = 8ψ₁(1) + 8ψ₁(2) + 32ψ₂(2)                          (= 4α₂ + 4β₁, Paper 2's A2u block)
    V_bb   = 4ψ₁(1) + 8ψ₁(2) + 4ψ₁(3) + 8ψ₂(1) + 32ψ₂(2) + 24ψ₂(3)  (= 2α₁ + 4α₂ + 2α₃, Paper 2's A1g block)
    V_aab  = (8√6/3)ψ₂(1) + 16√6 ψ₂(2) + (64√6/3)ψ₃(2)
    V_aaaa = 16ψ₂(1) + 16ψ₂(2) + 128ψ₃(2) + (256/3)ψ₄(2)

(α_k = φ″(√k), β_k = φ′(√k)/√k.) The body diagonals (σ = 3) do not enter V_aa, V_aab or V_aaaa, because the A2u field
moves the two ends of each body diagonal by the same vector.

### 3.2 Where b = D³V[e_A, e_A, ·] lives (VERIFIED-EXACT)

A2u ⊗ A2u = A1g, so b is O_h-invariant and lies in Fix(O_h) = span{e_br}, which is one-dimensional. This is checked
component by component in R²⁴: **b = V_aab e_br exactly**, for every pair potential. e_br is a Hessian eigenvector
with eigenvalue V_bb (exact). Therefore the general formula (STANDARD)

    c₄ = D⁴V[e,e,e,e] − 3⟨b, H_⊥⁻¹ b⟩        (V_red = … + ½λa² + (c₄/24)a⁴ + …)

collapses to **c₄ = V_aaaa − 3 V_aab²/V_bb**. VERIFIED-NUMERIC independently in R²⁴: no symmetry reduction, b from
the analytic gradient, and ⟨b, H_⊥⁻¹b⟩ from (H + P_ker)w = b. At q = 0.5 and q = 1.2 it agrees to 10⁻⁴⁰.

### 3.3 Closed forms on the two-term family (VERIFIED-EXACT)

At the unit-edge equilibrium every quantity above has the **difference form** Q = qW_q [g_Q(p) − g_Q(q)], with
g_Q(r) = L_Q(ψ_r)/(rW_r):

    h_A(r) = (2(r+1)x − 4)/W_r                     (identical to Paper 2 Lemma A)
    g_B(r) = 2(r + 1)                              ⇒  V_bb = 2qW_q(p − q) > 0
    g_3(r) = √6 (r+2)(2 − (r+1)x)/(3W_r)
    g_4(r) = (r+2)((r+1)(r+3)x + 12)/(3W_r)

    c₄ = qW_q { [g_4(p) − g_4(q)] − 3[g_3(p) − g_3(q)]² / (2(p − q)) }      on the curve h_A(p) = h_A(q).

### 3.4 Scale-eliminated formulation and equivalence (VERIFIED-EXACT, plus VERIFIED-NUMERIC agreement)

**The T_d shape family.** Set ρ₊ = e^(−u/2) and ρ₋ = e^(u/2), so u is the log of the ratio of the two tetrahedra's
sizes. The pair sum is then

    U_r(u) = 12x·cosh(ru/2) + 12((3/2)cosh u − 1/2)^(−r/2) + 4y·cosh(u/2)^(−r),

and f(u) = log Φ = p log U_q − q log U_p is even in u. Its Taylor coefficients at u = 0 are:

    U(0) = 12W_r,   U″(0) = r(3rx − y − 9),   U⁗(0) = r(3r³x + 81r + (3r+2)y + 126)/4
    k(r) = U″/(rU)                 = h_A(r)/8 − 1/4                              (exact identity)
    m(r) = [U⁗/U − 3(U″/U)²]/r     = [(3x+y+3)(3r³x+81r+(3r+2)y+126) − 3r(3rx−y−9)²] / (16(3x+y+3)²)
    f″(0) = pq[k(q) − k(p)] = −(pq/8)[h_A(p) − h_A(q)],     f⁗(0) = pq[m(q) − m(p)].

**Equivalence lemma.** Take a generic F(a, b), even in a, with F_a = F_b = 0. Compare two reductions:
- R₁: critical values along the lines a = const (full-energy Lyapunov–Schmidt reduction);
- R₂: critical values along rays from (0, −√6), i.e. the scaling orbits (scale elimination), parametrised by where
  each ray crosses b = 0.

Exact symbolic computation gives c₄(R₂) − c₄(R₁) = −12F_aa(F_aa + F_aab β₀)/(F_bb β₀²), which vanishes when
F_aa = 0. With Paper 2's V_* = −KΦ^{1/(p−q)} (FROZEN INPUT, Proposition A), the reparametrisation
u(α) = log((1 − α/√6)/(1 + α/√6)) and V₀ = −12W_q(p − q)/p, this gives on the curve:

    **c₄ = (16/3) qW_q [m(p) − m(q)] = −(4U_q/(9p)) f⁗(0)**.

Agreement with the full-energy formula is 10⁻³⁹ (relative) at 415 points. Off the curve the two formulas differ, as
the lemma predicts (tested).

### 3.5 Transversality and the kernel (FROZEN INPUT plus VERIFIED-EXACT)

- Transversality: ∂V_aa/∂p = qW_q h_A′(P_A(q)) on the curve, which is < 0 because h_A is strictly decreasing on
  (r*, ∞) (Paper 2 Lemma A). The crossing is therefore transversal at every point of the curve. Equivalently,
  ∂f″(0)/∂p > 0.
- Kernel: on p = P_A(q), 0 < q < r*, the only zero mode besides the six rigid motions is A2u (Paper 2 Theorem 4′; the
  two curves never meet).

### 3.6 Sign of c₄ along the curve (VERIFIED-NUMERIC; the sign is now proved in §3.8)

The frozen definition of P_A is: the unique p > r* with h_A(p) = h_A(q). It was solved at 50 digits, with a
divided-difference formulation that stays well conditioned near r*. Recomputed constants:

- r* = 1.4749107381472217442484782…, matching the frozen value to 4.9·10⁻²⁰;
- P_A(0⁺) = 3.1054933552830915550122…, matching to 1.2·10⁻²⁰;
- P_A agrees with Paper 2's own code to 1.7·10⁻¹³ (float precision).

**Table** (`data/A1_sign_table.csv`): 415 points, q ∈ [1.47·10⁻⁸, r*(1 − 10⁻¹²)].
- **c₄ > 0 at every point.**
- Δm(q) := [m(P_A(q)) − m(q)]/(P_A(q) − q) lies in [1.21310, 1.26546].
- Endpoint limits: Δm(0⁺) = (m(P_A(0⁺)) − 8/7)/P_A(0⁺) = 1.213102; Δm(r*⁻) = m′(r*) = 1.265460.
- c₄ itself tends to 0 at both ends only through the factor qW_q(p − q). The normalised carrier
  c₄/(qW_q(p − q)) = (16/3)Δm ∈ [6.4699, 6.7491] stays away from zero, so no sign change and no zero were found.

**Why the sign is stable:**
- m(0⁺) = 8/7 and m(∞) = 21/8 (exact limits).
- m′ > 0.617 on a 2000-point grid of (0, P_A(0⁺)]. The maximum of m is at r ≈ 7.649, far beyond P_A(0⁺) ≈ 3.105.
- Every point of the curve has q < r* < p ≤ P_A(0⁺), so monotonicity of m on (0, P_A(0⁺)] alone forces
  m(P_A(q)) > m(q).

**Local branch, checked directly in the T_d family (VERIFIED-NUMERIC):**
- For p = P_A(q)(1 + δ), δ = 10⁻³, 10⁻⁵ and 10⁻⁷, a nonzero critical point exists. It satisfies
  u_found/u_pred − 1 = O(δ), with u_pred = √(−6f″/f⁗).
- For δ = −10⁻⁵ there is none: f′ keeps one sign on (0, 0.05].
- To first order, the amplitude law is u² ≈ (3/4)|h_A′(P_A(q))|(p − P_A(q))/[m(P_A(q)) − m(q)]. At δ = 10⁻⁷ it
  matches the located branch to a relative 5·10⁻⁸ (tested).

### 3.7 Lemma M (Phase A2) — CERTIFIED · INDEPENDENTLY AUDITED

> **Lemma M.** m′(r) > 0 for every r ∈ [0, 16/5]. More precisely, m′(r) ≥ L_min = 161457/262144 = 0.61590957…
> on [0, 16/5].

Here m is the V0.1-dev closed form, unchanged. The interval [0, 16/5] contains the whole range (0, P_A(0⁺)] that is
needed.

**Exact derivative** (VERIFIED-EXACT; two independent derivations agree). Put L2 = log 2 and L3 = log 3. Then:

    m = N/(16S²),   S = 3x + y + 3,   N = S(3r³x + 81r + (3r+2)y + 126) − 3r(3rx − y − 9)²
    dx/dr = −(L2/2)x,   dy/dr = −(L3/2)y,   S′ = −(3L2/2)x − (L3/2)y

    m′(r) = Ψ/(16S³) = [L2·A + L3·B + C] / (32(3x + y + 3)³),   with Ψ = S·N′ − 2N·S′ and
      A = r³(45x²y + 135x² − 3xy² − 18xy − 27x) + r²(54x²y + 486x² − 18xy² − 216xy − 486x)
          + r(27x²y + 729x² − 9xy² − 54xy − 729x) + 18x²y + 1134x² + 6xy² + 396xy + 1134x
      B = r³(−45x²y + 3xy² + 9xy) + r²(−54x²y + 18xy² + 270xy) + r(−27x²y + 9xy² + 351xy + 36y² − 108y)
          − 18x²y − 6xy² + 342xy + 120y² + 360y
      C = r²(−324x³ − 54x²y − 162x² + 18xy² + 108xy + 162x) + r(216x²y + 1944x² + 72xy² + 864xy + 1944x)
          + 54x²y + 1458x² + 18xy² + 756xy + 1458x + 72y² + 216y

    m″(r) = Φ/(16S⁴),   Φ = S·Ψ′ − 3Ψ·S′   (138 terms, stored in the certificate)

The first derivation is the chain rule with partial derivatives (`lemma_m.py`). The second treats x and y as functions
X(r), Y(r) with X′ = −(L2/2)X, Y′ = −(L3/2)Y (`certcheck.py`). The two agree exactly.

**Near r = 0** (VERIFIED-EXACT plus CERTIFIED):
- The closed form has no division by r. The factor r of U″(0) and U⁗(0) in the V0.1-dev definition cancels exactly
  (tested: r·m = U⁗/U − 3(U″/U)²). So m is analytic at r = 0, and its Arb evaluation there has no 0/0 cancellation.
- m′(0) = 18/49 + (12/49)log 2 + (57/784)log 3 = 0.6169708662…, which is > 0 because every term is positive.
- m″(0) = 45/98 − (9/1372)L2 + (261/5488)L3 − (6/343)L2² + (363/5488)L2L3 − (285/10976)L3² = 0.5175100758….
- Series: m′(r) = m′(0) + m″(0)r + O(r²).
- Initial interval: m″ > 0 on [0, 1/8], certified with Arb on 8 boxes, each with a recorded dyadic lower bound > 0.49.
  Hence m′(r) ≥ m′(0) > 0 on [0, 1/8], independently of the main certificate.

**Certificate** (`data/A2_lemma_M_certificate.json`; semantic SHA-256 in `data/A2_CERTIFICATE_SEMANTIC.sha256`):

| item | value |
|---|---|
| arithmetic | Arb ball arithmetic (python-flint 0.9.0, FLINT 3.6.0), outward rounding |
| precision | 128 bits (generator); 160 bits (independent checker) |
| box test | mean-value form: m′(B) ⊆ m′(c) + (B − c)·m″(B), c = midpoint |
| subdivision | recursive bisection of [0, 16/5] until certified and width ≤ 1/20 (depth limit 40) |
| boxes | 64, exact rational endpoints k/20 (k = 0..64), gap-free; maximum depth 6 |
| lower bounds | dyadic rationals (grid 2⁻²⁰), each checked by Arb to lie strictly below the box enclosure |
| minimum lower bound | **L_min = 161457/262144 ≈ 0.6159096**, on [0, 1/20]; the true infimum is m′(0) ≈ 0.6169709 |
| largest lower bound | ≈ 1.509, on [61/20, 31/10] |
| semantic hash | SHA-256 of the canonical JSON without the `provenance` block (seconds, timestamp, versions, code hashes) |

**Independent checker** (`certcheck.py`). It uses a different derivation route, its own Arb tree-walker at 160 bits,
and no shared evaluation code. It checks:
- the claim, and the expressions against the V0.1-dev m and its own derivatives;
- gap-free coverage of [0, 16/5] with exact rationals;
- that every bound is > 0, and the recorded minimum;
- every box, recomputed (all 64 confirmed without refinement);
- the near-zero and P_A blocks;
- the semantic hash.

**Independent re-certification** (Track A audit, §3.10): a separate implementation with MPFR directed rounding
(192 bits) re-proved every recorded lower bound, with no failures.

**Tampered certificates are rejected** (one test each): a gap, an overlap, a shortened start, an extended claim, a
flipped relation, a non-positive bound, a negated Ψ, an altered m, an altered Φ, an inflated bound (7/10 on [0, 1/20]),
content not matching its hash, and a wrong hash file.

**Negative controls for the method:**
- On [7, 8] the same method fails. Its failure box sits at r = 7.64901368548…, the zero of m′ (the maximum of m).
- It also fails on [8, 9] (where m′ < 0), for −m′ on [0, 16/5], and for the false bound m′ > 31/50 on [0, 1/10].
- A true sub-claim, [1, 2], is certified.
- Six code mutations of the generator and the checker are all detected by the tests. Together with the nine V0.1-dev
  mutations and the two on the Theorem A graph (§3.9), `scripts/negative_controls.py` detects 17/17.

**P_A(q) < 16/5** (CERTIFIED plus FROZEN INPUT):
- Certified with Arb: h_A(16/5) = −0.88588385… < −6/7, and h_A′(16/5) < 0.
- By Lemma A (Paper 2), h_A rises on (0, r*) from h_A(0⁺) = −6/7 and decreases strictly on (r*, ∞). For 0 < q < r*:
  h_A(P_A(q)) = h_A(q) > −6/7 > h_A(16/5), with both P_A(q) and 16/5 greater than r*. So **0 < q < r* < P_A(q) < 16/5**.
- Also certified: P_A(0⁺) ∈ [3105493355283091, 3105493355283092]·10⁻¹⁵ and r* ∈ [1474910738147221, 1474910738147222]·10⁻¹⁵.
  Both enclosures contain the frozen values.

### 3.8 Corollary M: c₄ > 0 on the whole A2u curve — PROVED (computer-assisted) · INDEPENDENTLY AUDITED

Let 0 < q < r*. By §3.7, q and P_A(q) lie in [0, 16/5], and P_A(q) > q. Lemma M and the mean value theorem give
m(P_A(q)) − m(q) = m′(ξ)(P_A(q) − q) ≥ L_min·(P_A(q) − q) > 0. With the exact identity of §3.4:

    c₄(q) = (16/3)·qW_q·[m(P_A(q)) − m(q)]  ≥  (16/3)·L_min·qW_q·(P_A(q) − q)  >  0.        ∎

(This is the unit-edge normalisation with unit e_A. In Paper 2's normalisation c₄ is multiplied by e^(−q−4) > 0,
where e = t^(−1/(p−q)) is Paper 2's edge length (§1), so the sign is the same.)

### 3.9 Theorem A — PROVED (computer-assisted) · INDEPENDENTLY AUDITED

*(V0.1-dev called this Theorem candidate A.)*

**Setting.**
- Fix q ∈ (0, r*). For p > q let V_p = t(p,q)U_p − U_q, with t = qW_q/(pW_p). Up to rescaling length and energy, this
  is V = AU_p − BU_q for any A, B > 0.
- The unit-edge cube y* is an equilibrium of V_p for every p.
- T is the six-dimensional space of rigid infinitesimal motions at y*, and 𝒮 = y* + T^⊥ is the slice (it is
  O_h-invariant).
- μ = p − P_A(q), and V_red(a, μ) is the Lyapunov–Schmidt reduced potential on span{e_A}.

> **Theorem A.** There exist ε > 0 and a neighbourhood 𝒩 of y* in 𝒮 such that, for |μ| < ε, the equilibria of V_p in
> 𝒩 are exactly:
> 1. the cube y*, for every such p; and
> 2. for μ > 0 only, two further equilibria x_±(p) = y* ± a(p)e_A + w(p), with a(p) > 0, w(p) ⟂ e_A and
>    w(p) = β(p)e_br ∈ span{e_br}, β(p) = O(a(p)²), where
>    a(p)² = 6qW_q|h_A′(P_A(q))|·μ / c₄(q) + O(μ²), and c₄(q) > 0 is given by Corollary M.
>
> For μ ≤ 0 there are no equilibria in 𝒩 other than the cube. Spatial inversion D(−I) exchanges the complete branch
> configurations x₊ and x₋; it does not exchange the unequal-radius shells within one fixed configuration. Each of x₊
> and x₋ has point group T_d: two concentric regular tetrahedra of unequal radii on inversion-related vertex-direction
> sets.
>
> The bifurcation is a **supercritical pitchfork in the energy sense**: for 0 < μ < ε, V_red(·, μ) has a strict local
> maximum at a = 0 and strict local minima at a = ±a(p).

**Branch side, from the reduced equation and the sign convention** (not from numerical branch finding):
- Since V_p is real-analytic in (x, p), the reduced potential V_red is real-analytic. It is even in a by (H1), so
  V_red(a, μ) = V_red(0, μ) + ½λ(μ)a² + (c₄(μ)/24)a⁴ + O(a⁶), and ∂_aV_red = a·G(a², μ) with G analytic.
- λ(μ) = qW_q[h_A(P_A(q) + μ) − h_A(q)] exactly, because e_A is an exact Hessian eigenvector for every p (H2). So
  λ(0) = 0 and λ′(0) = qW_q·h_A′(P_A(q)) < 0 (H3).
- G(s, μ) = λ(μ) + (c₄(μ)/6)s + O(s²), so G(0, 0) = 0, G_μ(0, 0) = λ′(0) < 0 and G_s(0, 0) = c₄/6 > 0 (H4).
- The equilibria near y* are a = 0 and the zeros of G(a², μ). Since G_μ(0, 0) ≠ 0, the implicit function theorem
  says the zeros of G near (0, 0) form exactly one curve, μ = μ*(s), with slope μ*′(0) = −G_s/G_μ = −c₄/(6λ′(0)) > 0.
  - So a² = s > 0 forces μ > 0. For each small μ > 0 there is exactly one s = a(p)² > 0, namely
    a(p)² = −6λ′(0)μ/c₄ + O(μ²) = 6qW_q|h_A′(P_A(q))|μ/c₄ + O(μ²). For μ ≤ 0 there is none.
  - The branch lies on the side p > P_A(q), where λ(μ) < 0, i.e. where the cube is unstable in the e_A direction
    (λ(μ) > 0 for p < P_A(q)).
- Second derivatives: ∂²_aV_red = G + 2a²G_s.
  - At a = 0 this is λ(μ), which is < 0 for μ > 0.
  - On the branch, G = 0, so it is 2a²G_s = (c₄/3)a(p)² + O(μ²) = −2λ(μ) + O(μ²) > 0.
  - So a = 0 is a strict local maximum and a = ±a(p) are strict local minima of V_red(·, μ).

**Rest of the proof.**
- Equilibria of V_p near y* in 𝒮 are exactly the critical points of V_p restricted to 𝒮 (slice argument, STANDARD).
- At p = P_A(q), the Hessian of V_p restricted to 𝒮 has kernel span{e_A} (H2). The Lyapunov–Schmidt reduction on 𝒮
  (STANDARD) writes the equilibria near y* as x = y* + a e_A + w(a, μ), with w unique, O_h-equivariant and
  w(a, μ) = O(a²) (because H e_A = λ e_A exactly, ∂_a w(0, μ) = 0). The equilibria are then the zeros of ∂_aV_red found
  above.
- Equivariance puts w(a, μ) in Fix(T_d) ∩ e_A^⊥ = span{e_br} (A0 §2.4), and gives D(R)x(a) = x(χ_A2u(R)a) (A0 §2.7).
  So D(−I) exchanges x₊ and x₋, and each is fixed exactly by T_d within O_h (a ≠ 0).
- x_± consists of the even and the odd tetrahedron of the cube, scaled about the centre by 1/2 + (β ± a)/√24 and
  1/2 + (β ∓ a)/√24. The two tetrahedra have unequal radii (a ≠ 0), so a symmetry of a fixed branch configuration
  cannot exchange the shells; it preserves each shell, and the symmetries of a regular tetrahedron form T_d. Their
  vertex-direction sets are inversion-related, and the point group is T_d, in agreement with the exactly computed
  stabiliser. Spatial inversion exchanges the complete configurations x₊ and x₋; it does not map the unequal-radius
  shells onto one another within a single fixed configuration.
- The conditions G_μ ≠ 0 and G_s ≠ 0 are the STANDARD recognition conditions of the Z₂-symmetric pitchfork
  (Golubitsky & Schaeffer, *Singularities and Groups in Bifurcation Theory*, Vol. I). The argument above uses only the
  implicit function theorem. The equivariant reduction is in Vol. II (Golubitsky, Stewart & Schaeffer). ∎

**Proof dependency graph:**

    Theorem A ............................................................................. PROVED (computer-assisted) · INDEPENDENTLY AUDITED
    ├─ (H0) V_p real-analytic near (y*, P_A(q)); O_h- and E(3)-invariant; y* an equilibrium
    │     pair distances of y* are 1, √2, √3 (all ≥ 1) .................................... VERIFIED-EXACT
    │     V is O_h-invariant; D(R) is orthogonal .......................................... VERIFIED-EXACT
    │     a pair energy is E(3)-invariant ................................................. STANDARD
    │     ∇V(y*) ∈ Fix(O_h) = span{e_br}; V_b = 0 exactly when A = t ...................... VERIFIED-EXACT
    ├─ (H1) Z₂ evenness: V_red(−a, μ) = V_red(a, μ), so ∂_aV_red = a·G(a², μ)
    │     D(R)e_A = χ_A2u(R)e_A; D(−I)e_A = −e_A; D(−I)y* = y* ............................ VERIFIED-EXACT
    │     invariant complements; T is O_h-invariant ....................................... STANDARD
    │     equivariant Lyapunov–Schmidt reduction .......................................... STANDARD
    │     analyticity: an odd analytic g equals a·G(a², μ) ................................ STANDARD
    ├─ (H2) one-dimensional kernel mod rigid motions: ker = T ⊕ span{e_A} at p = P_A(q)
    │     A2u has multiplicity 1 in Γ₂₄; its isotypic component is span{e_A} .............. VERIFIED-EXACT
    │     H e_A = V_aa e_A; V_aa = qW_q[h_A(p) − h_A(q)] .................................. VERIFIED-EXACT
    │     translations and rotations lie in the kernel .................................... VERIFIED-EXACT
    │     no other zero mode on p = P_A(q); the two curves never meet ..................... FROZEN INPUT (Paper 2, Theorem 4′)
    ├─ (H3) transversality: λ′(0) = qW_q h_A′(P_A(q)) < 0
    │     λ(μ) = qW_q[h_A(P_A(q) + μ) − h_A(q)] exactly ................................... VERIFIED-EXACT
    │     h_A strictly decreasing on (r*, ∞); P_A(q) > r* ................................. FROZEN INPUT (Paper 2, Lemma A)
    ├─ (H4) c₄(q) > 0 (Corollary M)
    │     c₄ = V_aaaa − 3⟨b, H_⊥⁻¹b⟩ ...................................................... STANDARD
    │     b = V_aab e_br and H e_br = V_bb e_br ........................................... VERIFIED-EXACT
    │     V_bb, V_aab, V_aaaa as closed difference forms .................................. VERIFIED-EXACT
    │     c₄ = (16/3)qW_q[m(P_A(q)) − m(q)] (foliation lemma + chain) ..................... VERIFIED-EXACT
    │           V_* = −KΦ^{1/(p−q)} ....................................................... FROZEN INPUT (Paper 2, Prop. A)
    │     Lemma M: m′ ≥ L_min > 0 on [0, 16/5] (§3.7) ..................................... CERTIFIED
    │     q < r* < P_A(q) ................................................................. FROZEN INPUT (Paper 2, Lemma A)
    │     P_A(q) < 16/5: h_A(16/5) < −6/7, h_A′(16/5) < 0 (with Lemma A) .................. CERTIFIED
    ├─ reduction
    │     slice argument for the rigid motions ............................................ STANDARD
    │     Lyapunov–Schmidt reduction with parameter; w unique, O_h-equivariant ............ STANDARD
    │     Stab(e_A) = T_d; Fix(T_d) = span{e_br, e_A} ..................................... VERIFIED-EXACT
    └─ branch side: μ*′(0) = −c₄/(6λ′(0)) > 0; ∂²_aV_red = 2a²G_s on the branch ........... VERIFIED-EXACT
          uses (H3), (H4) and the implicit function theorem ............................... STANDARD

**Machine-readable form.** The graph is in `src/cube_bif/theorem_a.py` and is recorded in
`data/A2_theorem_A_dependencies.json`. It names the tests behind every VERIFIED-EXACT and CERTIFIED leaf.

`tests/test_A2_theorem.py` checks that:
- the graph is closed and acyclic;
- (H1)–(H4) are dependencies of Theorem A;
- every named test exists;
- the FROZEN INPUT leaves are exactly Lemma A, Theorem 4′ and Proposition A of `reference/PAPER2_INPUTS.md`;
- no numerical check is a dependency.

The same file checks the algebra of the reduced equation (slope, amplitude, second derivatives) symbolically.

**Numerical corroboration** (VERIFIED-NUMERIC, not used in the proof):
- Amplitude law: the branch located in the T_d family matches a(p)² = 6qW_q|h_A′|μ/c₄ with a relative error that
  scales with μ. At q = 0.2, 0.8, 1.3 and μ = 10⁻⁷·P_A(q) the error is 5.0·10⁻⁸, 3.8·10⁻⁸ and 2.8·10⁻⁸; a wrong
  constant (6/5 of it) would be off by 0.17.
- Extremum types along the T_d family, for p = P_A(q)(1 ± 10⁻⁶):
  - p above P_A(q): f″(0) > 0 (the cube is a local maximum of the scale-optimised energy), and f″(u_branch) < 0, with
    f″(u_branch) ≈ −2f″(0) (the branch points are local minima);
  - p below P_A(q): f″(0) < 0.
- The signs λ′(0) < 0, c₄ > 0 and μ*′(0) > 0 hold at six curve points.

The branch finding of §3.6 agrees with all of this.

### 3.10 Independent audit of Track A (V0.2-dev)

- **Auditor and record:** Kimi Agent, blind audit. The report is kept byte-identical as
  `audits/CUBE_BIFURCATIONS_REVIEWER_REPORT.md` (SHA-256 f82c5ef1a03c33c0909313bd6442d1879d39717f991cc8e245eb0c61f75d8b85).
  It arrived in `Kimi_Agent_Blind_Theorem4_Proof_Audit_1.zip`
  (SHA-256 e2b2a144f83fd30031f2a84b58d956a14728e4b906bc0b787536bb2f41a172e8), received 2026-11-13. The auditor dated
  the report 2026-11-14.
- **Audited package:** `EIT_LJ_CUBE_BIFURCATIONS_V0.2-dev.zip`,
  SHA-256 ba835b0dee8cb6d80214b4bd9a61bf2a65d6a4d52376b4e7e0a3dcfd71691e30. The report quotes this hash, and all 39
  checksums verified.
- **Scope:** integrity, reproduction, the certificate, the exact mathematics, the proof dependencies, wording and the
  claim boundary of Track A. B1, A3 and Paper 2 were out of scope.
- **What the auditor checked independently:**
  - Reproduction in a separate copy: run_A0, run_A1, run_B0, run_A2, pytest (128 passed, 2 skipped because the Paper 2
    archive was not supplied) and the negative controls (17/17). The regenerated certificate body and its semantic
    hash are identical to the stored ones.
  - A separate checker with MPFR directed rounding (192 bits). It derives m from the T_d pair sum, differentiates it
    itself and uses its own evaluator. It re-proved every recorded dyadic lower bound on 128 half-boxes (one extra
    bisection per box), with no failures. It also confirmed h_A(16/5) < −6/7 and h_A′(16/5) < 0 without Arb.
  - Exact A0/A1 checks written without the package's group, pair-sum or quartic code:
    - the 48 signed permutations and the rank-1 A2u projector;
    - Fix(O_h) = span{e_br}; the stabiliser of e_A (24 elements) and Fix(T_d) = span{e_br, e_A};
    - the closed forms and the Hessian identities;
    - the on-curve identity c₄ = V_aaaa − 3V_aab²/V_bb = (16/3)qW_q[m(p) − m(q)], confirmed exactly by a zero
      polynomial remainder modulo the cleared curve equation h_A(p) = h_A(q).
  - The dependency graph: 35 nodes, closed, acyclic and with no unused nodes. The frozen inputs are exactly Lemma A,
    Theorem 4′ and Proposition A, and the numerical checks are corroboration only.
- **Findings:** no CRITICAL or MAJOR finding, and no mathematical or certificate correction. Two MINOR documentation
  findings, both corrected in V0.2.1-dev:
  - MINOR-01: the tetrahedra were called mutually inverted and of different sizes, and the odd tetrahedron the
    inversion of the even one. Spatial inversion preserves radius, so this was not literally correct. The text now
    reads: two concentric regular tetrahedra of unequal radii on inversion-related vertex-direction sets; spatial
    inversion exchanges the complete configurations x₊ and x₋, not the shells within one configuration (§2 item 7,
    §3.9, README).
  - MINOR-02: §3.7 gave a stale count of 15 negative controls; the suite has 17 (17/17 detected).
- **Claim boundary (confirmed by the audit):** the strict local maximum at a = 0 and the strict minima at a = ±a(p)
  are statements about the one-dimensional reduced potential. No full-configuration-space stability or Morse index is
  claimed.
- **Verdict:** PASS WITH MINOR DOCUMENTATION CORRECTIONS. Once MINOR-01 and MINOR-02 are corrected, Track A may be
  labelled independently audited, and no mathematical or certificate revision is required.
- **Applies to V0.2.1-dev unchanged:** V0.2.1-dev differs from the audited V0.2-dev only in documentation and in
  version/status strings. All source, the certificate and all other data are byte-identical
  (`docs/V0.2.1-dev_DIFF_CHECK.md`).

## 4. Phase B0 — T2g reconnaissance (VERIFIED-EXACT unless stated)

- **Bases.** uh_k = −W_k/4 and vh_k = −(√2/4)U_k (k = 1, 2, 3), with W_k(s) = S_k s (shear-type) and
  U_k(s) = (s₁s₂s₃)ε_k (the two tetrahedra translate in opposite directions). For k = 3 these are Paper 2's u, v.
  - They span the six-dimensional T2g isotypic component and are orthonormal.
  - Both copies transform by the same matrices **T(R) = σ(R)·R** (an equivariant matching).
  - The Hessian acts on each pair {uh_k, vh_k} by one 2×2 block K. K is the same for every k, there is no coupling
    between different k, and K equals Paper 2's Lemma T0 block.
  - At the equilibrium, K = qW_q[M(p) − M(q)], with Paper 2's M(r).
- **Critical eigenspace on p = P_T(q):** e_k = n_u uh_k + n_v vh_k, where n spans ker[M(p) − M(q)]. Numerically,
  n ≈ (−0.9997, −0.022 to −0.028) along the curve: the mode is almost pure shear, with about 2–3 % opposite
  translation of the two tetrahedra.
  - H e_k = 0 to 10⁻⁴⁰ at q = 0.25, 0.5, 1.0, 1.5, 1.9, 2.0 (VERIFIED-NUMERIC).
  - P_T agrees with Paper 2's code to float precision.
  - With symbolic n, the basis transforms by T(R) for every n.
- **3×3 representation.** T(R) = σ(R)R has kernel {E, i}, and its image is T_d acting on R³. Invariants of degree
  1, 2, 3, 4 have dimensions 0, 1, 1, 2. The cubic invariant **I₃ = a₁a₂a₃ is invariant under all 48 matrices**, and
  every invariant cubic is a multiple of it. A nonzero quadratic equivariant therefore exists, namely ∇I₃.
- **Isotropy (computed from stabilisers of all integer vectors in [−2, 2]³; labels from computed element types):**

| isotropy (O_h) | order | conjugates | dim Fix | representative a | normaliser, action on Fix | I₃ on axis | generic local branch |
|---|---|---|---|---|---|---|---|
| D3d | 12 | 4 | 1 (axial) | (1,1,1) | D3d, trivial | ≠ 0 | transcritical-type, provided the cubic coefficient κ ≠ 0 |
| D2h (C2 axes: one 4-fold axis, two face diagonals) | 8 | 3 | 1 (axial) | (1,0,0) | D4h, contains −1 | 0 | pitchfork-type (reduced equation odd by symmetry) |
| C2h (face-diagonal axis) | 4 | 6 | 2 | (1,1,0) | — | — | not axial: the EBL gives nothing |
| Ci | 2 | 1 | 3 | generic | — | — | — |

  - The 24-dimensional stabiliser of Σa_k e_k equals the 3×3 stabiliser of a, checked at four representatives with
    symbolic n.
  - κ = D³V[e₁, e₂, e₃] on the curve has not been computed yet. That is Phase B1.
- **Ihrig's theorem, stated correctly (STANDARD):** Ihrig & Golubitsky (Physica D 13 (1984) 1–33, Thm 4.2(B)) cover
  steady-state bifurcation on an absolutely irreducible representation that has nonzero quadratic equivariants. Under
  their hypothesis (H4) that branches are axial, the branches given by the Equivariant Branching Lemma are
  generically unstable near the bifurcation. Chossat, Lauterbach & Melbourne later removed the axial restriction
  (summary: Arjevani & Field, arXiv:2107.02422).
  - It is a stability statement. It does **not** say that the branches are transcritical. Whether a branch is
    transcritical or pitchfork-type is decided axis by axis, as in the table above.
  - In this gradient problem the cube is already a saddle (index ≥ 2), so stability means the index within the
    centre manifold.

## 5. Phase B1 — the cubic coefficient on the T2g curve (V0.3-dev)

Labels as in §0. The B1 request's "EXACT" is VERIFIED-EXACT here. Nothing in B1 is called proved. Track A
(§2–3.10) is unchanged and byte-identical with the audited V0.2.1-dev.

**Basis (B0).** uh_k = −W_k/4 and vh_k = −(√2/4)U_k, k = 1, 2, 3. Both copies transform by T(R) = σ(R)R. On
p = P_T(q) the critical vectors are e_k = n_u uh_k + n_v vh_k, with n ∈ ker K and K = qW_q[M(p) − M(q)] (Paper 2's
M). κ = D³V[e₁, e₂, e₃].

### 5.1 Exact trilinear structure (B1.1) — VERIFIED-EXACT

All 216 values D³V[b_i, b_j, b_k] on the six basis vectors were computed for a generic pair potential
φ(r) = ψ(r²), before any symmetry was used (route 1: the pair-sum formula of `pairsum.py`).
- 48 are nonzero, all with {i, j, k} = {1, 2, 3}.
- Within each channel the value does not depend on the order of i, j, k, and uuv = uvu = vuu, uvv = vuv = vvu.

That leaves four independent coefficients, with ψ^(k) evaluated at σ = |r|² ∈ {1, 2, 3}:

    t_uuu = −12ψ″(2) − 12ψ″(3) − 32ψ‴(3)
    t_uuv = −√2 (10ψ″(3) + 16ψ‴(3))
    t_uvv = −8ψ″(1) − 8ψ″(3) − 16ψ‴(3)
    t_vvv = −8√2 ψ‴(3)

    κ = t_uuu n_u³ + 3 t_uuv n_u² n_v + 3 t_uvv n_u n_v² + t_vvv n_v³

**Route 2 (raw 24-D).** The third-derivative tensor of V(x) = Σψ(|x_i − x_j|²) was computed in the 24 coordinates by
SymPy differentiation, pair by pair, with no T2g reduction (800 nonzero entries). Contracted with the basis vectors,
it reproduces the four coefficients exactly. With x = Σa_k e_k and symbolic n_u, n_v, ψ:

    D³V[x, x, x] = 6κ a₁a₂a₃   exactly,

so the cubic restriction to the critical space is a multiple of I₃(a) = a₁a₂a₃.

### 5.2 Two-term specialisation, divided differences and the factorisation (B1.2) — VERIFIED-EXACT

At the unit-edge equilibrium (A = t, B = 1), each coefficient is exactly a difference form
t_m = qW_q[g_m(p) − g_m(q)]. With X = 2^(−r/2), Y = 3^(−r/2) and W = 1 + X + Y/3:

    g_uuu(r) = (r+2)(−(3/4)X + (4r+7)Y/27)/W        g_uuv(r) = √2(r+2)(4r+1)Y/(54W)
    g_uvv(r) = (r+2)(−2 + 2(r+1)Y/27)/W             g_vvv(r) = √2(r+2)(r+4)Y/(27W)

None of them divides by r.

Write f̂(p, q) = (f(p) − f(q))/(p − q), with f̂(q, q) = f′(q); this is analytic in (p, q).
- Divided-difference block: M̂(p, q) = (M(p) − M(q))/(p − q), so K = qW_q(p − q)M̂.
- The curve: D̃(q, δ) := det M̂(q + δ, q) = D(q + δ, q)/δ² (Paper 2's D̃). D̃(p, q) is symmetric in p and q.
  - Physical curve: D̃ = 0 with δ = p − q > 0, i.e. p = P_T(q), 0 ≤ q < q_c (Paper 2, Lemma T3).
  - Its closure adds the corner (q_c, q_c), where D̃ = det M′(q_c) = 0 (Lemma T2).
  - Beyond q_c the zero set continues as the mirror image p < q.

**Factorisation (derived, not assumed):**

    κ = qW_q (p − q) κ̂,     κ̂ = ĝ_uuu n_u³ + 3ĝ_uuv n_u²n_v + 3ĝ_uvv n_u n_v² + ĝ_vvv n_v³.

κ̂ is analytic on the closed curve. It is nonzero at both ends (§5.4, certified in §5.7). So κ has exactly one factor
q and exactly one factor (p − q), and no other zero.

### 5.3 Gauge and the projective chart (B1.3)

The sign of κ changes under n ↦ −n, so only κ ≠ 0 is gauge invariant. Chart: n ∝ (1, ρ), with ρ = −M̂₁₂/M̂₂₂.
- Exact identity: M̂(1, ρ)ᵀ = (det M̂/M̂₂₂, 0)ᵀ. So (1, ρ) spans ker M̂ wherever det M̂ = 0 and M̂₂₂ ≠ 0.
- The certificate proves M̂₂₂ > 0 on the whole closed curve. Hence n_u ≠ 0 everywhere, and one chart covers the
  curve with no transition needed.
- In the chart, κ̂ = ĝ_uuu + 3ρĝ_uuv + 3ρ²ĝ_uvv + ρ³ĝ_vvv. For unit n, κ = qW_q(p − q)κ̂/(1 + ρ²)^(3/2).
- B0's `null_vector` is −(1, ρ)/√(1 + ρ²), so the B0 gauge has the opposite sign (tested).

### 5.4 Endpoints (B1.4)

| endpoint | p − q | ρ | κ̂ (limit) | raw κ |
|---|---|---|---|---|
| q → 0⁺ | P_T(0) = 4.796368189344416004181122… | 0.0197163555530139 | 0.0028795125799552354827 | → 0 linearly (factor q) |
| q → q_c⁻ | → 0, P_T(q) − q = 2(q_c − q) + O((q_c − q)²) | 0.0277614207531459 | 0.0068917823096483782991 | → 0 linearly (factor p − q) |

So the certificate is not formulated as κ ≠ 0 on (0, q_c]: raw κ vanishes at the corner. It is formulated for κ̂ on
the closed curve, which includes both ends.

### 5.5 Three routes (B1.5)

1. Route 1: exact symmetry-adapted contraction (§5.1).
2. Route 2: raw 24-D SymPy differentiation. It agrees with route 1 exactly.
3. Route 3 (corroboration only): ∂³/∂a₁∂a₂∂a₃ V(y* + Σa_k e_k), by mpmath differentiation of the 24-D pair energy at
   six curve points (q = 0.05, 0.3, 1.0, 1.5, 1.8, 2.0). It agrees with qW_q(p − q)κ̂ to a relative 4·10⁻³⁸ or better.

### 5.6 Candidate scan (B1.6) — VERIFIED-NUMERIC

Grid: 401 points q_k = k·q_c/400; the last point is the corner limit. File: `data/B1_scan.csv`.

| quantity | result |
|---|---|
| κ̂ (chart gauge) | min 0.00287951258 at q = 0, max 0.00689178231 at the corner; increasing; no sign change |
| ρ | 0.019716 to 0.027761 |
| M̂₂₂ (chart conditioning) | 1.4555 to 1.5133 |
| ∂D̃/∂δ at the curve (curve conditioning) | −0.1077 to −0.0643 |
| dP_T/dq | −1.940 (at q = 0) to −1.0007 (at the corner) |
| τ̃ = n^T M′(p) n/(p − q) (normalised transversality) | −0.0740 to −0.0425 |

### 5.7 Arb certificate (B1.7) — CERTIFIED · INDEPENDENTLY AUDITED

> **Lemma K.** On the closed T2g curve, κ̂ ≥ 1311719/536870912 = 0.0024432670… > 0, and M̂₂₂ > 0.
> Hence κ(q) ≠ 0 for every 0 < q < q_c. In the gauge n_u > 0, κ(q) > 0.

| item | value |
|---|---|
| arithmetic | Arb (python-flint 0.9.0, FLINT 3.6.0), 128 bits, outward rounding |
| covering | q ∈ [0, 101/50], 222 boxes with exact rational endpoints, gap-free (base k/100, depth ≤ 2: 185/35/2 boxes) |
| curve | per box, a parametric interval Newton step in δ (mean-value form in q) proves exactly one zero of D̃(q, ·) in a recorded ball, for every q in the box |
| divided differences | far from the diagonal (inf δ > 1): ball quotients (170 boxes). Near it: the Taylor form Σ_{j≤16} c_j(q)δ^{j−1} + δ^16 c₁₇(hull) (52 boxes), with no division by δ |
| carrier | mean-value form in (q, δ); M̂₂₂ > 0 and κ̂ > dyadic lower bound on every box |
| minimum lower bound | 1311719/536870912 ≈ 0.0024433 on [0, 1/100]; the true minimum is κ̂(0) = 0.0028795 |
| endpoint q = 0 | Newton at q = 0 inside Paper 2's P_T(0) enclosure; κ̂(0) ∈ 0.0028795125799552354826978 ± 2.1·10⁻²⁸ |
| endpoint corner | q ∈ Paper 2's 40-digit q_c enclosure, δ = 0; κ̂ ∈ 0.0068917823096483782991303 ± 2.8·10⁻²⁸; det M′ changes sign across the enclosure (cross-check of Lemma T2) |
| semantic SHA-256 | `data/B1_CERTIFICATE_SEMANTIC.sha256` (provenance excluded) |

**Why the enclosed zero is the physical curve.**
- Every box except the corner box [2019/1000, 101/50] has a positive δ-ball. Its zero has p > q, so it is P_T(q)
  by Lemma T3.
- The corner box contains Paper 2's q_c enclosure. At its left end, q = 2019/1000, a Newton step inside its ball
  gives a positive enclosure.
  - The unique zero δ*(q) in the ball is continuous in q.
  - It is never 0 for q < q_c, because D̃(q, 0) = det M′(q) > 0 there (Lemma T2).
  - So δ*(q) > 0 on [2019/1000, q_c), which makes it P_T(q) − q.
  - At q_c the zero is δ = 0, the corner.

**Independent checker** (`b1_check.py`, 160 bits).
- It derives the seven functions M₁₁, M₁₂, M₂₂ and g_m itself: SymPy directional derivatives of the pair terms along
  T2g fields it builds from the labels. These agree with the stored expressions.
- It evaluates with its own Arb walker (factored forms) and its own divided differences (Taylor order 20).
- It confirmed all 222 Newton inclusions and all 222 carrier bounds without refinement, plus the corner argument,
  both endpoints and the semantic hash.

**Tampered certificates are rejected** (one test each): a gap, an overlap, a shifted start, a truncated end, a
flipped relation, a non-positive bound, an inflated bound, a shifted δ-ball, an altered g_uuu, an altered M₁₂, a
missing corner box, a δ-ball through 0, the far regime near the diagonal, content not matching its hash, and a wrong
hash file.

**Method controls** (`data/B1_negative_controls.json`):
- The same method fails on the false bound κ̂ > 3/1000 near q = 0.
- It fails on 9/2000 − κ̂, which changes sign at q = 0.46294; it fails next to that root.
- It fails on the raw κ, both at q = 0 and at the corner.
- It fails with the wrong kernel vector ρ = +M̂₁₂/M̂₂₂.
- It certifies the true carrier on [1/2, 1].
- Seven code mutations of the B1 generator, checker and closed forms are detected by the tests.

### 5.8 Transversality (B1.8) — FROZEN INPUT plus VERIFIED-EXACT

Frozen Paper 2 already proves it; no new certificate is needed.
- τ := n^T ∂_pK n = qW_q n^T M′(P_T(q)) n, for unit n.
- On the curve, N = M(p) − M(q) is singular and symmetric with kernel n, so adj N = tr(N) n nᵀ (exact identity,
  tested). Hence ∂_pD = tr(N)·n^T M′(p) n.
- Lemma T1: tr K > 0, so tr N > 0. Lemma T3: ∂_pD(P_T(q), q) < 0 for 0 ≤ q < q_c.
- Therefore **τ < 0 for every 0 < q < q_c**.

The normalised form near the corner is τ̂ = n^T M′(p) n = (p − q)τ̃, with τ̃ → n_cᵀM″(q_c)n_c/2 = −0.0740 (scan,
corroboration only). It is not needed, because the physical range ends before q_c.

### 5.9 The D3d branches (B1.9) — CERTIFIED (computer-assisted) · INDEPENDENTLY AUDITED

> **Proposition B1.** Fix q ∈ (0, q_c) and let μ = p − P_T(q). Take unit n ∈ ker M̂(P_T(q), q) with n_u > 0, and
> let κ = D³V[e₁, e₂, e₃] and τ = n^T ∂_pK n at μ = 0. Then κ > 0 (Lemma K) and τ < 0 (§5.8).
>
> In y* + Fix(D3d) near y*, for small |μ|, the equilibria of V_p are exactly:
> - the cube; and
> - one branch x(μ) = y* + s*(μ)(e₁ + e₂ + e₃) + w(μ), with w ∈ span{e_br, f₁ + f₂ + f₃} and
>   f_k = −n_v uh_k + n_u vh_k, where
>
>       s*(μ) = −(τ/κ)μ + O(μ²).
>
> The branch is defined for both signs of μ and s*(μ) ≠ 0 for μ ≠ 0: it crosses the cube transversally, so it is
> **transcritical**. In this gauge, s* > 0 for p > P_T(q) and s* < 0 for p < P_T(q). The same holds on each of the
> four D3d axes (conjugate by O_h).

**The scalar reduced equation, derived explicitly.**
1. Fix(D3d) in R²⁴ is span{e_br, Σuh_k, Σvh_k}. It is three-dimensional and contains no rigid motion (exact
   projector, tested). By symmetric criticality its equilibria are the critical points of V restricted to it.
2. At μ = 0 the Hessian there has kernel span{e₁ + e₂ + e₃}. This uses Paper 2's Theorem (index): nullity 3, all
   in T2g, and the A2u eigenvalue is nonzero on this curve. Fix(D3d) meets the T2g kernel only on the diagonal.
3. One-dimensional Lyapunov–Schmidt reduction: v(s, μ) = V_p(y* + s(e₁ + e₂ + e₃) + w(s, μ)), with w = O(s²) in
   span{e_br, Σf_k}. On the axis |a|² = 3s² and a₁a₂a₃ = s³, so

       v(s, μ) = v(0, μ) + (3/2)λ_red(μ)s² + κ(μ)s³ + O(s⁴),
       ∂_s v = 3s·G(s, μ),   G(s, μ) = λ_red(μ) + κ(μ)s + O(s²).

   Here λ_red(μ) = det K(p)/(fᵀK(p)f), f = (−n_v, n_u) (Schur complement; e_br does not couple at second order). It
   satisfies λ_red(0) = 0 and λ_red′(0) = τ (tested symbolically).
4. G(0, 0) = 0, G_s(0, 0) = κ ≠ 0 and G_μ(0, 0) = τ ≠ 0. By the implicit function theorem the nontrivial zeros near
   (0, 0) form one curve s = s*(μ), with s*′(0) = −τ/κ ≠ 0. The trivial solution s = 0 is the cube. ∎

Both gates are used: κ ≠ 0 for the implicit function theorem, and τ ≠ 0 so that the branch leaves the cube on both
sides. Ihrig's theorem is not used. No full-space or centre-manifold stability is claimed.

**First-order geometry** (VERIFIED-EXACT, first order in s only). The displacement s(e₁ + e₂ + e₃) moves vertex s by
−(s n_u/4)(J − I)s − (s n_v √2/4)(s₁s₂s₃)(1, 1, 1), where J is the all-ones matrix.
- The first term scales the cube by 1 − s n_u along the body diagonal (1, 1, 1) and by 1 + s n_u/2 across it.
- The second term shifts the two tetrahedra oppositely along that diagonal, with a small weight ρ ≈ 0.02–0.03.
- So for p > P_T(q) the cube is compressed along one body diagonal, and for p < P_T(q) it is elongated.

**Numerical corroboration** (not used in the proof): Newton in the three Fix(D3d) coordinates at q = 0.3, 1.0, 1.8
and μ = ±10⁻⁶P_T, ±10⁻⁷P_T.
- It finds genuine equilibria: full 24-D gradient below 10⁻⁴⁹.
- s has the sign of μ.
- |s/s* − 1| is 1.0·10⁻³, 4.6·10⁻⁴ and 2.9·10⁻⁴ at 10⁻⁷, ten times larger at 10⁻⁶: it is O(μ).

### 5.10 D2h (B1.10) — retained from B0, not started

Some T(R) maps (1, 0, 0) to −(1, 0, 0) (tested). So V_red restricted to the D2h axis is even and its scalar equation
is odd: pitchfork type. No T(R) maps (1, 1, 1) to −(1, 1, 1), consistent with the cubic term on the D3d axis.
- The quartic coefficient and stability belong to B2.
- The geometry of the D2h configurations has not been derived, so they are not called cuboids.

### 5.11 Independent audit of Phase B1 (V0.3-dev)

- **Auditor and record:** Kimi Agent. The report is kept byte-identical as
  `audits/CUBE_BIFURCATIONS_V03_REVIEWER_REPORT.md` (SHA-256 82bd4f21630a20481113702a9f49dddfa6327f2baf3c07a131af259c1baa65e5).
  It arrived in `Kimi_Agent_Blind_Theorem4_Proof_Audit_2.zip`
  (SHA-256 1058e2a12b545e7ca3208ba8d8c562f0712c047c10625cb64a5cba7a672333e0), received 2026-11-13. The auditor dated
  the report 2026-11-14.
- **Audited packages:** V0.2.1-dev (3bd6ac42…91e30) and V0.3-dev (3901c0db…128fe). The report quotes both hashes and
  they match the archives here.
- **Scope:** the V0.2.1-dev correction chain, the preservation of Track A and B0 in V0.3-dev, Lemma K and
  Proposition B1. Out of scope: stability of the D3d branches, the D2h quartic coefficient, B2, Paper 2, freezing and
  publication.
- **What the auditor checked independently:**
  - Integrity and identity: every row of `docs/V0.2.1-dev_DIFF_CHECK.md` and of
    `docs/V0.3-dev_TRACK_A_IDENTITY.md`. The extracted NOTES §§1–3.10 hash 7fde8afa… matches this project's own
    extraction.
  - Reproduction: 130 passed for V0.2.1-dev; 195 passed for V0.3-dev with the Paper 2 archive; negative controls
    24/24; the same A2 and B1 semantic hashes after regeneration.
  - A direct 24-coordinate derivation, without importing any B1 module: the 216 trilinear values, 48 of them nonzero,
    the four coefficients t_m, the closed forms g_m, Paper 2's M(r), the factorisation κ = qW_q δ κ̂ and the chart
    identity.
  - Lemma K: a standalone replay at 192 bits with Taylor order 24 and its own enclosures of the δ- and q-derivatives.
    It confirmed 222/222 Newton inclusions and 222/222 carrier bounds without refinement, M̂₂₂ > 0 on every box and
    both endpoints. det M′ changes sign across Paper 2's q_c enclosure (checked at 640 bits).
  - The physical-curve and corner identification (Lemmas T2 and T3), the transversality chain τ < 0, the fixed space
    of D3d (rank 3, no rigid motion), the Schur-complement eigenvalue, the reduced equation, the sign
    −τ/κ > 0 and the first-order geometry.
- **Observation (not a finding):** the generator and the internal checker share the near-diagonal Taylor method. The
  audit therefore derived its own enclosures of the derivatives, and its verdict rests on them. As a diagnostic, the
  shared balls contained the independently computed ones for 364/364 near-box components.
- **Findings:** none, in any category. The report notes that V0.3-dev correctly labelled B1 "not independently
  audited", and that a later audit-status patch may record the report and update the label. No certified file needs
  revision.
- **Claim boundary (confirmed):**
  - no strict extremum, centre-manifold or full-space stability is claimed for the D3d branches;
  - Ihrig's theorem is not used to classify the branch;
  - the D2h quartic coefficient and stability remain for B2.
- **Verdict:** PASS. Phase B1 may be labelled independently audited; no mathematical, certificate or documentation
  correction is required.
- **Applies to V0.3.1-dev unchanged:** V0.3.1-dev differs from the audited V0.3-dev only in documentation and in
  version/status strings. All B1 mathematics, the certificate, source, tests and data are byte-identical
  (`docs/V0.3.1-dev_DIFF_CHECK.md`).

## 6. Phase B2 — the quartic coefficient on the D2h axis (V0.4-dev.1: B2.0 and B2.1 only)

Labels as in §0. Nothing in B2 is called proved or certified, and nothing in B2 is audited. This version follows the
B2 plan the author relayed from his review gate on 2026-11-13: B2.0 (symmetry) and B2.1 (c₄) first, checked at the
gate before any certificate work; then B2.2 (carrier and scan), B2.3 (certificate), B2.4 (branch) and B2.5
(centre-manifold index). Track A, B0 and B1 (§1–5.11) are byte-identical with V0.3.1-dev
(`docs/V0.4-dev.1_IDENTITY_CHECK.md`).

**Setting.** On p = P_T(q), e₁ = n_u uh₁ + n_v vh₁ with unit n ∈ ker K (B0), so e₁ is a unit vector of R²⁴. The
D2h axis of the critical representation is a = (s, 0, 0), i.e. the displacement s e₁.

### 6.1 B2.0 — exact symmetry audit (VERIFIED-EXACT)

Code: `src/cube_bif/b2_symmetry.py`; tests: `tests/test_B2_symmetry.py`; record: `data/B2_symmetry.json`. Nothing
below was assumed; each item is computed from the O_h action on R²⁴.

**Stabiliser, computed in 24-D.** Σ := {R ∈ O_h : D(R)e₁ = e₁}, with n_u, n_v symbolic.
- Order 8, element types E, C4², i, σ_h, 2C2′, 2σ_d. From this signature: the D2h whose C2 axes are x, (0, 1, 1)
  and (0, 1, −1).
- It equals B0's 3×3 stabiliser of (1, 0, 0), and it fixes uh₁ and vh₁ separately.

**Fixed space.** P_Fix = (1/8)Σ_{g∈Σ} D(g) is an orthogonal projector of rank 4. The rank of P_Γ P_Fix for each
irrep Γ:

| Γ | A1g | A2g | Eg | T1g | T2g | A1u | A2u | Eu | T1u | T2u |
|---|---|---|---|---|---|---|---|---|---|---|
| multiplicity in R²⁴ | 1 | 0 | 1 | 1 | 2 | 0 | 1 | 1 | 2 | 1 |
| dim Fix_Γ(Σ) | 1 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| rank of P_Γ P_Fix | 1 | 0 | 1 | 0 | **2** | 0 | 0 | 0 | 0 | 0 |

The character formula (multiplicity × dim Fix_Γ) gives the same ranks. No rigid motion is fixed. So

    Fix_{R²⁴}(Σ) = span{Â, Ê, uh₁, vh₁} = span{Â, Ê, e₁, f₁}     (orthonormal),

- Â = E_BR/√24: breathing (A1g);
- Ê = E_TET_X/√48, with E_TET_X(s) = (2s₁, −s₂, −s₃): the tetragonal strain along the axis (Eg);
- e₁ and f₁ = −n_v uh₁ + n_u vh₁: **each T2g copy contributes one fixed direction**, for every n.

**The relayed claim Fix(D2h) = span{e_crit, A1g, Eg⁽¹⁾, Eg⁽²⁾} is not correct** (tested):
- the second Eg direction (strain diag(0, 1, −1)) is not fixed; P_Fix maps it to 0;
- f₁ is fixed, but it is not in the claimed span;
- the claimed span meets Fix(Σ) in three dimensions only. The count 4 agrees by coincidence.

**Where b = D³V[e₁, e₁, ·] lives.** b was computed as a 24-vector of linear forms in ψ^(k)(σ), for a generic pair
potential φ(r) = ψ(r²) and symbolic n. With b(n) = n_u² b_uu + 2n_u n_v b_uv + n_v² b_vv:
- P_Γ b = 0 for the eight irreps other than A1g and Eg, and P_A1g b + P_Eg b = b.
- ⟨b, uh_k⟩ = ⟨b, vh_k⟩ = 0 for k = 1, 2, 3 and all three channels (18 values). In particular **⟨b, f₁⟩ = 0 and
  ⟨b, e₁⟩ = 0 exactly.**
- b = b_A Â + b_E Ê exactly, with no component on the second Eg direction. Writing ψ″_σ = ψ″(σ), ψ‴_σ = ψ‴(σ):

| channel | b_A (A1g) | b_E (Eg) |
|---|---|---|
| uu | √6(4ψ″₁ + 32ψ″₂ + 28ψ″₃ + 32ψ‴₂ + 48ψ‴₃)/3 | −√3(4ψ″₁ + 20ψ″₂ + 16ψ″₃ + 32ψ‴₂)/3 |
| uv | 16√3(ψ″₃ + 3ψ‴₃)/3 | 4√6 ψ″₃/3 |
| vv | √6(20ψ″₁ + 20ψ″₃ + 8ψ‴₁ + 24ψ‴₃)/3 | 16√3(ψ″₁ + ψ″₃ + ψ‴₁)/3 |

**Why ⟨b, f₁⟩ = 0 although f₁ is Σ-fixed.** Σ-invariance alone allows an f₁ component. The vanishing has a finer
reason.
- b is the image of e₁ ⊗ e₁ under the O_h-equivariant map Sym²(T2g) → R²⁴, x ⊗ x ↦ D³V[x, x, ·].
- Sym²(T2g) = (A1g ⊕ Eg) ⊕ T2g. The T2g component is t(a) = (a₂a₃, a₃a₁, a₁a₂); its equivariance was checked for all
  48 matrices. A1g ⊕ Eg is spanned by (a₁², a₂², a₃²), which every matrix permutes.
- By Schur's lemma the T2g-isotypic part of b is the image of t(a), and t(1, 0, 0) = 0. On the D3d axis
  t(1, 1, 1) ≠ 0. This is the I₃ pattern of §5.1 seen from the other side.

**Evenness.** Exactly 8 elements of O_h map e₁ to −e₁. With Σ they form the normaliser, labelled D4h from its
signature. Each acts on (Â, Ê, uh₁, vh₁) as diag(1, 1, −1, −1). So V on y* + Fix(Σ) is invariant under
(e₁, f₁) ↦ −(e₁, f₁), and the axial reduced potential is even in s. This re-derives in 24-D the pitchfork-type
parity of B0 (§5.10).

**The same fixed space from the vertex orbits** (the parametrisation of route 3 in §6.2).
- Σ has two vertex orbits of size 4: {(1,1,1), (1,−1,−1), (−1,1,1), (−1,−1,−1)}/2 and
  {(1,1,−1), (1,−1,1), (−1,1,−1), (−1,−1,1)}/2. Each orbit meets both tetrahedra.
- Each vertex has a mirror (order 2) as stabiliser in Σ, so it moves in a plane: (a, b, b) at (1,1,1)/2 and
  (c, d, −d) at (1,1,−1)/2.
- The four orbit fields lie in Fix(Σ) and have rank 4, with Gram matrix diag(4, 8, 4, 8).

**First-order geometry and the cuboid family** (VERIFIED-EXACT, first order in s only).
- s e₁ moves vertex s by −(s n_u/4)(0, s₃, s₂) − (s n_v√2/4)(s₁s₂s₃)(1, 0, 0).
- The first term acts on every cross-section x = const by (y, z) ↦ (y − εz, z − εy), ε = s n_u/2. The square
  section is compressed by 1 − ε along (0, 1, 1) and stretched by 1 + ε along (0, 1, −1): it becomes a rhombus.
- The second term moves the two tetrahedra oppositely along x, with the small weight ρ ≈ 0.02–0.03.
- Fix(Z₂³), the cuboid family A1g ⊕ Eg of Paper 2, has rank 3. e₁ and f₁ are orthogonal to it, and
  Fix(Σ) ∩ Fix(Z₂³) = span{Â, Ê}. So a Σ-symmetric configuration near the cube with a nonzero e₁-component is not a
  cuboid.

### 6.2 B2.1 — the quartic coefficient (exact formula VERIFIED-EXACT; three routes VERIFIED-NUMERIC at five points)

Code: `src/cube_bif/b2_quartic.py`; tests: `tests/test_B2_quartic.py`; record: `data/B2_quartic.json`.

**The reduction (STANDARD; its value is confirmed independently by route 3).** By symmetric criticality the
Σ-symmetric equilibria near y* are the critical points of V on y* + Fix(Σ). At μ = 0 the Hessian there has kernel
span{e₁}: its other eigenvalues are h_A, h_E (below) and tr K, which are nonzero by Paper 2's Lemma S and Lemma T1
(FROZEN INPUT). Eliminating w ∈ span{Â, Ê, f₁}, w = O(s²), at second order gives

    V_red(s) = V(y*) + (c₄/24)s⁴ + O(s⁶),     c₄ = D⁴V[e₁⁴] − 3⟨b, H_⊥⁻¹b⟩.

V_red is even in s (§6.1), and the cubic term vanishes: D³V[e₁, e₁, e₁] = 0.

**Exact decomposition of H on the fixed space** (generic ψ). In the basis (Â, Ê, uh₁, vh₁),

    H|Fix(Σ) = diag(h_A, h_E) ⊕ K        (K = the B0 block; on the curve K = diag(0, tr K) in (e₁, f₁)).

Â and Ê are eigenvectors of the full 24×24 Hessian: A1g and Eg occur once each in R²⁴. Since b ∈ span{Â, Ê}:

    H_⊥⁻¹ b = (b_A/h_A) Â + (b_E/h_E) Ê,
    c₄ = Q(n) − 3 b_A(n)²/h_A − 3 b_E(n)²/h_E,        Q(n) = Σ_j C(4, j) n_u^(4−j) n_v^j Q_j.

The forms, with ψ′_σ = ψ′(σ) and ψ⁗_σ = ψ⁗(σ):

    h_A = 4ψ′₁ + 8ψ′₂ + 4ψ′₃ + 8ψ″₁ + 32ψ″₂ + 24ψ″₃     = Paper 2's A1g block 2α₁ + 4α₂ + 2α₃
    h_E = 4ψ′₁ + 8ψ′₂ + 4ψ′₃ + 8ψ″₁ + 8ψ″₂              = Paper 2's Eg block 2α₁ + α₂ + 3β₂ + 2β₃
    Q_uuuu = 6ψ″₁ + 18ψ″₂ + 12ψ″₃ + 96ψ‴₂ + 96ψ‴₃ + 64ψ⁗₂ + 64ψ⁗₃
    Q_uuuv = √2(24ψ‴₃ + 32ψ⁗₃)
    Q_uuvv = 4ψ″₁ + 4ψ″₃ + 24ψ‴₃ + 32ψ⁗₃
    Q_uvvv = √2(24ψ‴₃ + 16ψ⁗₃)
    Q_vvvv = 36ψ″₁ + 12ψ″₃ + 48ψ‴₁ + 48ψ‴₃ + 16ψ⁗₁ + 16ψ⁗₃

The ψ′ part of h_A and h_E is 4(ψ′₁ + 2ψ′₂ + ψ′₃), which vanishes at the equilibrium. Paper 2's α_k = φ″(r_k) and
β_k = φ′(r_k)/r_k become α_k = 2ψ′_k + 4kψ″_k and β_k = 2ψ′_k.

**Denominators.** h_A > 0 and h_E > 0 for all p > q > 0: FROZEN INPUT, Paper 2's Lemma S (A1g and Eg strictly
stable). The closed forms g_hA and g_hE below are exactly Paper 2's h_L for these two blocks (tested). Lemma S
proves h_L′ > 0 for both (its Ψ_L > 0), so the divided differences ĥ_A = 2 and ĥ_E are positive on the closed curve,
corner included.

**Two-term specialisation (VERIFIED-EXACT).** Each of the 13 forms is a difference form qW_q[g(p) − g(q)], with
X = 2^(−r/2), Y = 3^(−r/2), W = 1 + X + Y/3, and none of the g divides by r:

    g_Quuuu = (r+2)(162r²X + 648rX + 729X + 32r²Y + 32rY − 168Y + 972)/(648W)
    g_Quuuv = √2(r+2)(r+4)(2r+3)Y/(81W)
    g_Quuvv = (r+2)(81 + (2r² + 11r + 21)Y)/(81W)
    g_Quvvv = √2(r−3)(r+2)(r+4)Y/(81W)
    g_Qvvvv = (r+2)(81r² + 324r + 729 + (r² − 8r − 21)Y)/(81W)
    g_bA,uu = −√6(r+2)(9rX + (4r+2)Y − 18)/(54W)        g_bE,uu = √3(r+2)((18r+27)X − 16Y − 36)/(108W)
    g_bA,uv = −2√3(r+2)²Y/(27W)                          g_bE,uv = √6(r+2)Y/(27W)
    g_bA,vv = −√6(r−1)(r+2)(Y+9)/(27W)                   g_bE,vv = −2√3(r+2)(9r + 18 − 2Y)/(27W)
    g_hA = 2(r+1)                                        g_hE = [2(r+1) + (r−2)X/2 − 2Y/3]/W

**Factorisation (derived, not assumed).** Every term carries qW_q(p − q), so

    c₄ = qW_q (p − q) ĉ₄,     ĉ₄ = Q̂ − 3 b̂_A²/ĥ_A − 3 b̂_E²/ĥ_E,     ĥ_A = 2 exactly,

with the divided differences f̂ of §5.2. In the chart n ∝ (1, ρ) of §5.3,
ĉ₄ = [Q̂(1, ρ) − (3/2) b̂_A(1, ρ)² − 3 b̂_E(1, ρ)²/ĥ_E]/(1 + ρ²)² for unit n. Unlike κ, c₄ does not depend on the
gauge n ↦ −n.

**Three routes.**
1. **Route 1 (symmetry-adapted):** the formula above, evaluated from the closed forms with divided differences and
   the chart.
2. **Route 2 (raw 24-D).**
   - (a) Exact: the composed pair energy expanded along lines with SymPy, with ψ replaced by its quartic Taylor
     polynomial at each σ. It uses no Faà di Bruno coefficients and no symmetry. For symbolic n it reproduces
     D⁴V[e₁⁴] = Q(n), the full 24-vector b, and h_A, h_E exactly.
   - (b) Numeric: D⁴V[e₁⁴] and b by mpmath differentiation of the 24-D energy and of its analytic gradient, the full
     24×24 Hessian, and the spectral pseudo-inverse over its nonzero eigenvalues. No kernel basis is supplied and no
     symmetry is used. At every point it finds exactly 9 eigenvalues below 10⁻³⁰ (6 rigid motions and the 3 critical
     vectors), and b is orthogonal to their eigenvectors to 10⁻⁶⁰.
3. **Route 3 (restricted D2h family):** the four orbit coordinates of §6.1, its own energy code and no T2g basis.
   - Its own curve point: det of the 4×4 restricted Hessian = 0 (secant method).
   - Its own kernel vector, from that Hessian in the R²⁴ metric.
   - A nonlinear reduction: for each s the three transverse modes are solved by Newton, and
     c₄ = lim 24[V_red(s) − V(y*)]/s⁴ by Richardson extrapolation in s², s = 10⁻³·2^(−j), j = 0…4.
   - No derivative tensor is used. The parametrisation (u_x, u_y, u_z, α) mentioned in the relayed Google note was
     not available here; route 3 uses its own.

Comparison at five curve points (60 digits; Q̂, the two back-reaction terms and ĉ₄ in the unit-n normalisation):

| q | p = P_T(q) | ρ | Q̂ | −3b̂_A²/ĥ_A | −3b̂_E²/ĥ_E | ĉ₄ | c₄ (route 1) | route 2 rel. diff. | route 3 rel. diff. |
|---|---|---|---|---|---|---|---|---|---|
| 0.05 | 4.70037056290 | 0.020118 | 4.04014 | −0.13382 | −0.07242 | 3.833896 | 2.0566893428 | 1.6·10⁻⁶¹ | 9.5·10⁻³⁷ |
| 0.5 | 3.92183132617 | 0.023287 | 4.21575 | −0.08401 | −0.04792 | 4.083826 | 14.632170243 | 5.5·10⁻⁶¹ | 9.5·10⁻³⁷ |
| 1.0 | 3.19636564884 | 0.025812 | 4.34321 | −0.05357 | −0.03259 | 4.257048 | 17.760922165 | 1.6·10⁻⁶¹ | 8.3·10⁻³⁷ |
| 1.5 | 2.57741335955 | 0.027278 | 4.41289 | −0.03934 | −0.02523 | 4.348320 | 12.233548713 | 2.3·10⁻⁶¹ | 7.4·10⁻³⁷ |
| 2.0 | 2.03992796219 | 0.027761 | 4.43521 | −0.03517 | −0.02304 | 4.376996 | 0.5631301719 | 8.2·10⁻⁶⁰ | 7.0·10⁻³⁷ |

Route 3, in addition:
- its curve point agrees with B1's to 3·10⁻⁶¹;
- its three nonzero restricted eigenvalues equal tr K, h_A and h_E to 7·10⁻⁶⁰ (relative);
- its kernel vector is ±e₁;
- V_red(−s) and V_red(s) agree to working precision (largest difference 3·10⁻⁴⁷ in 24V_red/s⁴, at q = 1.0);
- the Richardson error estimates are below 7·10⁻³¹ (relative).

At these points the back-reaction lowers ĉ₄ by 1.3 % (q = 2.0) to 5.1 % (q = 0.05). Dropping the transverse solve
(energy along the kernel line only) returns D⁴V[e₁⁴] instead of c₄, and the tests detect it (negative control).

**Claim boundary.** The table gives values at five points only. Not done here, by design: the sign of c₄ on the
whole curve, the endpoint limits (q → 0⁺ and the corner), the scan and the certificate (B2.2, B2.3); the branch
side and the super/subcritical classification (B2.4); any stability or Morse index (B2.5).

## 7. Phase B2.2 — the normalised quartic carrier on the closed curve (VERIFIED-NUMERIC / RECONNAISSANCE)

Labels as in §0. B2.2 is numerical reconnaissance ahead of a certificate, and it proves nothing. The few exact
identities in it are marked VERIFIED-EXACT, and the inputs from Paper 2 are marked FROZEN INPUT. **No sign of ĉ₄ is
proved or certified.** There is no Arb certificate, no super/subcritical classification, and B2.4 and B2.5 are not
started. Track A, B0, B1, B2.0 and B2.1 (§1–6.2) are byte-identical with V0.4-dev.1
(`docs/V0.4-dev.2_IDENTITY_CHECK.md`).

Code: `src/cube_bif/b2_carrier.py`; tests: `tests/test_B2_carrier.py`; script: `scripts/run_B2_2.py`; records:
`data/B2_carrier.json`, `data/B2_scan.csv`, `data/B2_falsification.json`, `data/B2_2_negative_controls.json`.

**The carrier (B2.1, exact).** c₄ = qW_q(p − q)ĉ₄ and, in the chart n ∝ (1, ρ) with ρ = −M̂₁₂/M̂₂₂,

    ĉ₄ = [Q̂(1, ρ) − (3/2) b̂_A(1, ρ)² − 3 b̂_E(1, ρ)²/ĥ_E] / (1 + ρ²)².

Below, "Q̂", "A1g term" and "Eg term" are the three summands with the factor 1/(1 + ρ²)² included, so they add up to
ĉ₄.

### 7.1 Endpoint q → 0⁺

**Formulation (VERIFIED-EXACT).** The formula is evaluated at q = 0 itself, not extrapolated from small q:
f̂ = (f(p₀) − f(0))/p₀ for the 13 closed forms and M̂ = (M(p₀) − M(0))/p₀. At r = 0 (X = Y = 1, W = 7/3) the closed
forms have exact values:

| g_Quuuu | g_Quuuv | g_Quuvv | g_Quvvv | g_Qvvvv | g_bA,uu | g_bA,uv | g_bA,vv | g_bE,uu | g_bE,uv | g_bE,vv | g_hA | g_hE |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 73/36 | 8√2/63 | 68/63 | −8√2/63 | 472/63 | 16√6/63 | −8√3/63 | 20√6/63 | −25√3/126 | 2√6/63 | −64√3/63 | 2 | 1/7 |

    M(0) = (1/21)[[−16, 4√2], [4√2, −20]],     p₀ = P_T(0) is the root of det[M(p) − M(0)] = 0.

**p₀ (FROZEN INPUT, refined).** Root finding on D̃(0, p) at 100 digits, inside Paper 2's certified enclosure
[4.796368189344416004181122459356, …357] (Lemma T3); D̃(0, ·) changes sign across it.

    p₀ = 4.7963681893444160041811224593562648333436851992894951588044886378258764…

It also lies inside the tighter MPFR enclosure from Paper 2's own blind audit,
[4.79636818934441600418112245935626482872…, 4.79636818934441600418112245935626483643…].

**Values** (80-digit evaluation; 45 digits in `data/B2_carrier.json`):

| quantity | value at q = 0 |
|---|---|
| ρ₀ | 0.0197163555530138765207016659191… |
| 1 + ρ₀² | 1.0003887346762928611246409854131… |
| M̂₂₂ | 1.5133403767422389187397667264848… |
| ĥ_E | 1.9991175681777892838805676426979… |
| ĥ_A | 2 |
| Q̂ | 4.0164575781153334278053069323935… |
| A1g term | −0.1411357471036181890408668753966… |
| Eg term | −0.0759837931448294230542130282277… |
| **ĉ₄(0)** | **3.7993380378668858157102270287692…** |

Approach check (not used for the value): (ĉ₄(q) − ĉ₄(0))/q = 0.70323, 0.706254, 0.7062840, 0.7062843 at
q = 10⁻², 10⁻⁴, 10⁻⁶, 10⁻⁸. The carrier is continuous at q = 0, with slope about 0.70628.

### 7.2 Corner q → q_c⁻

**Formulation (VERIFIED-EXACT).** At p = q = q_c every divided difference becomes the diagonal derivative,
f̂(q_c, q_c) = f′(q_c), and the chart is B1's ρ_c = −M′₁₂/M′₂₂. With all g′ at r = q_c:

    ĉ₄(q_c) = [ Σ_j C(4, j) ρ_c^j g′_{Q_j}
                − (3/2)(g′_{bA,uu} + 2ρ_c g′_{bA,uv} + ρ_c² g′_{bA,vv})²
                − 3 (g′_{bE,uu} + 2ρ_c g′_{bE,uv} + ρ_c² g′_{bE,vv})² / g′_{hE} ] / (1 + ρ_c²)²,    g′_{hA} = 2.

The derivatives are exact closed forms, g′(r) = ∂_r g − (log 2/2) X ∂_X g − (log 3/2) Y ∂_Y g. All 13 of them, and M′,
are recorded in `data/B2_carrier.json` and checked against numerical differentiation.
- **No division by p − q remains.** The corner expression is a function of r, X and Y alone (checked symbolically).
- Its only denominators are W (≥ 1), M′₂₂, g′_{hE} and 1 + ρ_c². At q_c these are 1.6065, 1.4555, 1.9983 and 1.00077.

**q_c (FROZEN INPUT, refined).** Root finding on det M′(r) at 100 digits, inside Paper 2's certified enclosure
[2.0199382317007999883028831854985758749007, …9008] (Lemma T2); det M′ changes sign across it.

    q_c = 2.0199382317007999883028831854985758749007365981536932554493825809307115…

This agrees with the digits printed in Paper 2's NOTES (2.019938231700799988302883185498575874900736…).

| quantity | value at the corner |
|---|---|
| ρ_c | 0.0277614207531459210146270045290… (equals B1's corner chart) |
| 1 + ρ_c² | 1.0007706964822332010363765511731… |
| M′₂₂ | 1.4555084712125296078064849112505… |
| ĥ_E = g′_{hE}(q_c) | 1.9983173671120638186095016362586… |
| ĥ_A | 2 |
| Q̂ | 4.4352429471647753083494174185066… |
| A1g term | −0.0351662275329967254877359643722… |
| Eg term | −0.0230412290186566467486595691890… |
| **ĉ₄(q_c)** | **4.3770354906131219361130218849453…** |

**The approach to the corner is quadratic.** (ĉ₄(q) − ĉ₄(q_c))/(q_c − q)² = −0.098877, −0.0987504, −0.09874909 and
−0.09874908 at q_c − q = 10⁻², 10⁻⁴, 10⁻⁶ and 10⁻⁸. The reason is structural:
- Divided differences and D̃ are symmetric under p ↔ q. Near the corner they are therefore analytic functions of
  m = (p + q)/2 and h² = ((p − q)/2)².
- On the curve m − q_c = O(h²), because det M′ has a simple zero at q_c.
- So ĉ₄ = ĉ₄(q_c) + O((q_c − q)²) along the curve: the carrier is stationary at the corner. The coefficient −0.098749
  is numerical.

### 7.3 Denominator conditioning (VERIFIED-NUMERIC)

Over the 401 scan points, endpoints included:

| denominator | minimum of its absolute value | where |
|---|---|---|
| ĥ_E | 1.99831736711206 | corner |
| M̂₂₂ (chart; M′₂₂ at the corner) | 1.45550847121253 | corner |
| 1 + ρ² | 1.00038873467629 | q = 0 |
| ĥ_A | 2 (exact) | everywhere |
| W (inside the closed forms) | ≥ 1 (exact) | everywhere |
| ∂D̃/∂δ on the curve (curve conditioning) | 0.0643377716 | q = 0 |

- The kernel residual |M̂(1, ρ)| is below 2·10⁻⁴⁹ at every point.
- At both ends the formulation stays well conditioned: no denominator approaches 0, and the scan joins the endpoint
  formulations continuously (§7.1, §7.2).
- These are margins only. Positivity of ĥ_A and ĥ_E on the whole closed curve is FROZEN INPUT (Paper 2's Lemma S;
  §6.2), and M̂₂₂ > 0 on the closed curve is certified in B1 (Lemma K).

### 7.4 Dense scan (VERIFIED-NUMERIC)

File: `data/B2_scan.csv`. It has 401 points q_k = k·q_c/400, k = 0…400, computed at 50 digits.
- Row 0 is the q = 0 formulation and row 400 the corner formulation. The other rows use the B2.1 divided differences.
- Each row records q, P_T(q), δ, ρ, Q̂, the A1g term, the Eg term, ĉ₄, ĥ_E, M̂₂₂, 1 + ρ², ∂D̃/∂δ, dP_T/dq and the kernel
  residual.

| quantity | result |
|---|---|
| minimum of ĉ₄ | 3.79933803786688581571 at q = 0 (row 0) |
| maximum of ĉ₄ | 4.37703549061312193611 at the corner (row 400) |
| smallest margin from zero | 3.7993, at q = 0 |
| sign changes | none; all 401 values are positive |
| monotonicity on the grid | strictly increasing; increments from 2.5·10⁻⁶ (next to the flat corner) to 3.6·10⁻³ |
| interior extremum | none on the grid; the maximum is the corner, where the slope is 0 (§7.2) |
| Q̂ | 4.0165 to 4.4352 |
| A1g term | −0.1411 to −0.0352 |
| Eg term | −0.0760 to −0.0230 |

Numerically, then, ĉ₄ is positive and increasing along the whole closed curve. The back-reaction lowers it by 1.3 %
at the corner and by 5.4 % at q = 0. Monotonicity is plausible but not proved, and nothing here is a certificate.

### 7.5 Independent route (VERIFIED-NUMERIC)

This route shares no code with the primary carrier: no closed forms g, no divided differences, no Paper 2 M(r) and no
B1 curve code.
- A general pair energy, with its gradient and Hessian in R²⁴, for a potential given in closed form.
- Its own curve point: where the 4×4 Hessian on the D2h fixed space (the vertex-orbit fields of §6.1) is singular,
  found by the secant method.
- Its own critical vector: the kernel of that 4×4 Hessian, mapped to R²⁴.
- The raw 24-D quartic and back-reaction: D⁴V[e⁴] and b = D³V[e, e, ·] by mpmath differentiation, the full 24×24
  Hessian and a spectral pseudo-inverse.
- The factor qW_q(p − q) removed analytically. In the interior the potential is divided by it. At the endpoints the
  limit potentials are used; that they are the limits is VERIFIED-EXACT (SymPy):

      q → 0:   φ/q → φ₀(r) = 7/(3pW_p) r^−p + log r  (up to a constant),           c₄(φ₀) = (7/3) p₀ ĉ₄(0);
      corner:  φ/(p − q) → φ_c(r) = −(1/q + W′_q/W_q + log r) r^−q  at p = q,     c₄(φ_c) = q_c W_{q_c} ĉ₄(q_c).

  The cube is an equilibrium of both (gradient below 2·10⁻⁵⁰). The route finds p₀ from φ₀ alone and q_c from φ_c
  alone.

| point | primary ĉ₄ | independent, relative difference | own curve point − primary |
|---|---|---|---|
| q = 0 (limit potential φ₀) | 3.79933803786688581571 | 1.9·10⁻⁵⁰ | −2.3·10⁻⁵⁶ (p₀) |
| q = 0.001 | 3.80004401628086258385 | 5.4·10⁻⁵¹ | 4.5·10⁻⁵¹ |
| q = 0.5 | 4.08382550595353747053 | 5.4·10⁻⁵¹ | −2.1·10⁻⁵¹ |
| q = 1.0 | 4.25704820401701963880 | 5.4·10⁻⁵¹ | 7.8·10⁻⁵² |
| q = 1.5 | 4.34831982108678430679 | 1.2·10⁻⁵⁰ | 1.8·10⁻⁵¹ |
| q = 2.0 | 4.37699613301241789685 | 4.1·10⁻⁵⁰ | −2.3·10⁻⁵² |
| q = 2.019 | 4.37703540367586694150 | 1.2·10⁻⁴⁸ | −9.2·10⁻⁵² |
| corner (limit potential φ_c) | 4.37703549061312193611 | 9.4·10⁻⁵¹ | −3.9·10⁻⁵⁷ (q_c) |

- At every point the raw Hessian has exactly 9 eigenvalues below 10⁻²⁵, and b is orthogonal to their eigenvectors to
  3·10⁻⁵⁰.
- A second, nonlinear check was made at the two endpoints. It uses the restricted family with the limit potentials,
  with Newton reduction and Richardson extrapolation as in route 3 of B2.1. It agrees to 9.3·10⁻³⁷ at q = 0 and to
  7.0·10⁻³⁷ at the corner.

### 7.6 Falsification reconnaissance (VERIFIED-NUMERIC)

File: `data/B2_falsification.json`. Each deliberately false statement was run through the same machinery:

| false statement | how it is tested | exposed |
|---|---|---|
| ĉ₄ ≥ (observed minimum)(1 + 10⁻⁶) | every scan row against the bound | yes: row 0 (q = 0) violates it |
| the carrier with the Eg back-reaction deleted | against the independent route | yes: off by 0.53–2.0 % |
| the carrier with the factor 3 changed to 2 | against the independent route | yes: off by 0.44–1.9 % |
| (1 + ρ²)² replaced by (1 + ρ²) | against the independent route | yes: off by 0.039–0.077 % |
| the projective kernel is (1, −ρ) | kernel residual, and the independent route | yes: residual ≥ 0.0597 (true kernel < 2·10⁻⁴⁹); off by ≥ 0.56 % |
| at the corner, values g(q_c) may replace the derivatives g′(q_c) | against the independent corner route | yes: off by 99 % |
| raw c₄ is nonzero at q = 0 or at q = q_c | raw c₄ = qW_q(p − q)ĉ₄ at the endpoint rows; raw 24-D c₄ near the ends | yes: exactly 0 at both ends |

Near the ends, raw 24-D c₄ is 0.0425, 4.3·10⁻⁴ and 4.3·10⁻⁶ at q = 10⁻³, 10⁻⁵ and 10⁻⁷, and 0.0284 and 2.8·10⁻⁴ at
q_c − q = 10⁻³ and 10⁻⁵. Meanwhile c₄/(qW_q(p − q)) tends to 3.79934 and to 4.37704.

Code mutations: 9 mutations of the B2.2 code are detected by the tests, each by an assertion
(`scripts/negative_controls_B2_2.py`, `data/B2_2_negative_controls.json`). The 34 earlier controls are unchanged.

### 7.7 Claim boundary

- **No sign of ĉ₄ is proved or certified.** The endpoint values, the scan and the independent route are numerical
  reconnaissance for B2.3.
- What the reconnaissance suggests for B2.3:
  - one sign (positive), with a large margin: at least 3.79, with the minimum at the q = 0 endpoint;
  - denominators bounded away from zero: ĥ_E ≥ 1.998, M̂₂₂ ≥ 1.455;
  - a flat corner (quadratic approach). A near-diagonal Taylor or derivative form must handle it without dividing by
    p − q.
- Not done here, by design:
  - the Arb certificate (B2.3);
  - the branch side and the super/subcritical classification (B2.4);
  - stability and the centre-manifold index (B2.5).

## 8. Contradictions with the external brainstorm

See `docs/CONTRADICTIONS_EXTERNAL_BRAINSTORM.md`.

## 9. Phase B2.3 — Lemma Q: ĉ₄ > 0 on the closed T2g curve — CERTIFIED (computer-assisted) · INDEPENDENTLY AUDITED (audit recorded in V1.0.0-rc1, §15)

B2.2 passed the review gate. B2.3 certifies the sign of the normalised carrier and nothing else. It does not certify
monotonicity, it does not call the D2h pitchfork supercritical or subcritical, and it claims no centre-manifold index.

### 9.1 Statement

**Lemma Q (CERTIFIED, computer-assisted) · INDEPENDENTLY AUDITED (audit recorded in V1.0.0-rc1, §15).** On the whole closed physical T2g curve, i.e.
p = P_T(q) for 0 ≤ q < q_c together with the corner p = q = q_c,

    ĉ₄ = [Q̂(1, ρ) − (3/2) b̂_A(1, ρ)² − 3 b̂_E(1, ρ)²/ĥ_E] / (1 + ρ²)² > 0,   ρ = −M̂₁₂/M̂₂₂,

and ĥ_E > 0, M̂₂₂ > 0 there. At q = 0 the divided differences are (f(P_T(0)) − f(0))/P_T(0), with the exact values
f(0) of §7.1. At the corner they are the derivatives f′(q_c) of §7.2. Certified values:
- ĉ₄ ≥ 955723/262144 ≈ 3.6458 on every curve box; the smallest recorded bound is on the first box, q ∈ [0, 1/100];
- ĉ₄(0) ∈ [3.79933803786688581571022702877 ± 7.9·10⁻³¹];
- ĉ₄(q_c) ∈ [4.37703549061312193611302188495 ± 4.6·10⁻³⁰].

**Corollary (of Lemma Q).** c₄(q) = qW_q(P_T(q) − q)·ĉ₄(q) > 0 for 0 < q < q_c, because q > 0, W_q > 1 and
P_T(q) − q > 0 (FROZEN INPUT, Paper 2, Lemma T3). The raw c₄ is exactly 0 at both ends, through the factors q and
p − q; no sign of the raw c₄ is claimed there.

Dependencies:
- the exact factorisation c₄ = qW_q(p − q)ĉ₄ with ĥ_A = 2 (VERIFIED-EXACT, §6);
- B1's curve boxes from the Lemma K certificate (CERTIFIED · INDEPENDENTLY AUDITED, §5.11), imported unchanged;
- FROZEN INPUT: Paper 2's Lemma T2 (the q_c enclosure), Lemma T3 (the unique curve point P_T(q) > q) and the
  P_T(0) enclosure.

### 9.2 Curve input (imported from B1, hash-pinned)

- `data/B1_kappa_certificate.json` is used only if its semantic SHA-256 is 616817fc…8518c6. The value is pinned in
  both the generator and the checker; the B1 hash file and B1's recorded provenance hash are compared as well.
- Its 222 boxes are used unchanged: exact rational q-boxes (steps of 1/100, 37 of them bisected once or twice by B1,
  and the corner box [2019/1000, 101/50]) with their δ-balls. By B1, for each q in a box the unique zero of D̃(q, ·) = det M̂(q + ·, q)
  in the box's ball is the curve point δ = P_T(q) − q (q < q_c), the corner (q_c, 0), or a short mirror arc beyond
  q_c (corner box only). So ĉ₄ > 0 on every box Q × Δ gives ĉ₄ > 0 on the closed curve.
- The certificate records its import checks (`import_checks`): gap-free coverage of [0, 101/50]; ordered, non-empty
  boxes; every B1 box used; δ-balls, corner flags and box hashes equal to B1's; one corner box, the last.
- The checker repeats every import check, compares the imported metadata with the B1 file (corner box, corner
  identification, P_T(0) and q_c enclosures, frozen inputs) and re-verifies every imported δ-ball (§9.5). The curve
  is not re-proved from scratch.

### 9.3 Generator (`src/cube_bif/b2_cert.py`, Arb at 128 bits)

- The 16 functions (M₁₁, M₁₂, M₂₂ and the 13 closed forms of §6) are compiled to straight-line Arb code.
- Divided differences over a box Q × Δ:
  - far (inf Δ > 1; 170 boxes): the ball quotient (f(Q + Δ) − f(Q))/Δ;
  - near (52 boxes, the corner box among them): with m = q + δ/2 and h = δ/2, the even series
    f̂ = Σ_{k<10} c_{2k+1}(m) h^{2k} + h^{20} c₂₁(ξ), ξ ∈ hull(q, q + δ), c_j = f^{(j)}/j!. The remainder is the exact
    Lagrange form of f̂ = ½∫₋₁¹ f′(m + sh) ds. Nothing is divided by δ.
- The carrier uses the chart form above, with ĥ_A = 2 exactly.
- On every box the generator first re-verifies the curve by a strict parametric interval Newton inclusion in the
  imported ball. It then certifies ĥ_E > 0, M̂₂₂ > 0 and ĉ₄ > 0 on the whole box. No box needed a split.
- Lower bounds are dyadic (2⁻²⁰) and lie below the enclosure by max(1/8 of its width, 2⁻¹⁰): robust rather than
  tight. No global bound is preselected. The quotient-regime enclosures are wide (up to 0.9 near q = 1.35), so the
  recorded bounds are conservative.
- Series length: python-flint truncates every arb_series at ctx.cap (default 10), whatever length is requested
  (§9.8). The generator sets ctx.cap to the requested length and checks the result; a regression test compares the
  23rd Taylor coefficient with mpmath.

### 9.4 Endpoints, certified directly

- q = 0: B1's certified P_T(0) ball (rational endpoints) and f̂ = (f(p₀) − f(0))/p₀ with the exact values at r = 0
  (§7.1). The endpoint is certified on its own, not inferred from q > 0.
- Corner: Paper 2's 40-digit q_c enclosure, as recorded by B1. Every divided difference is replaced by f′(q_c), and
  no expression divides by p − q.
- Both enclosures are rounded outward to 2⁻¹⁰⁰ and contain the 45-digit B2.2 values. ĥ_E > 0 and M̂₂₂ > 0 at both
  ends; the raw c₄ is recorded as exactly 0.

### 9.5 Independent checker (`src/cube_bif/b2_check.py`, Arb at 192 bits)

It imports nothing from the project and uses no Taylor series.
- Functions: it derives the 16 functions itself, from the pair terms ψ(σ) = σ^(−r/2) along fields built from the
  vertex labels, divided by rW_r, and compares them symbolically with the stored strings (all 16 agree). Its own
  chain rule gives f′, f″ and f‴, and its own compiler turns them into Arb code.
- Divided differences come from f̂(p, q) = ∫₀¹ f′(q + t(p − q)) dt with rational subdivision of t:
  - point values: the composite midpoint rule with its exact remainder (|T|³/24)δ²f‴(q + Tδ);
  - box ranges of f̂, ∂_q f̂ = ∫f″ dt and ∂_δ f̂ = ∫t f″ dt: a centred form on each subinterval;
  - the subdivision is refined (32 up to 256) before a box is bisected. At δ = 0 the rule gives f′(q) exactly.
- Kernel: v = (M̂₂₂, −M̂₁₂) and the homogeneous form [Q̂(v) − 3b̂_A(v)²/ĥ_A − 3b̂_E(v)²/ĥ_E]/‖v‖⁴; the chart ρ is
  never formed.
- On a box: the value at the centre plus the gradient over the box (dual numbers) times the box, a mean-value form.
  It confirms ĉ₄, ĥ_E and M̂₂₂ above their recorded bounds and ‖v‖² above the square of the M̂₂₂ bound.
- Curve: for every imported ball, ∂_δD̃ excludes 0 on Q × Δ (uniqueness), and a contracted interval Newton image lies
  strictly inside the ball (existence). This is its own re-verification of the B1 balls.
- Endpoints: q = 0 by the midpoint rule over B1's P_T(0) ball (1024 subintervals); the corner with δ = 0. The stored
  endpoint enclosures must overlap its own values, and its centre value of every box must lie in the stored box
  enclosure.
- Structure: claim, formulas, corollary, expression hash, B1 pin and file hash, imported metadata, boxes and import
  checks, coverage, indices, regimes, minima, denominator minima, raw-c₄ records and the semantic hash.

### 9.6 Results

| quantity | value |
|---|---|
| boxes | 222 (170 quotient, 52 symmetric series), no splits |
| smallest recorded lower bound | 955723/262144 ≈ 3.64579, box 0 (q ∈ [0, 1/100]) |
| ĥ_E, M̂₂₂: smallest recorded bounds | 1985555/1048576 ≈ 1.8936, 362177/262144 ≈ 1.3816 |
| ĉ₄(0) | [3.79933803786688581571022702877 ± 7.9·10⁻³¹] |
| ĉ₄(q_c) | [4.37703549061312193611302188495 ± 4.6·10⁻³⁰] |
| semantic SHA-256 | f7bc244ecac4b89ce003a38ff52047d6cbe80f63a97236049f15f5e0da5c17d2 |
| independent checker | 222/222 balls re-verified and 222/222 boxes confirmed, all at 32 subintervals and without splits; 222/222 centre values inside the stored enclosures; ĉ₄(0) ∈ [3.7993380 ± 7.9·10⁻⁸], ĉ₄(q_c) ∈ [4.3770354906131219361 ± 1.3·10⁻²⁰] |

Files: `data/B2_c4hat_certificate.json`, `data/B2_CERTIFICATE_SEMANTIC.sha256`, `data/B2_3_check_report.json`
(`scripts/run_B2_3.py`).

### 9.7 Tamper tests and controls

- Consistent forgeries (`tests/test_B2_certificate.py`; every summary field and both hashes re-derived, as a careful
  forger would): all 23 are rejected. They cover a gap, an overlap and a deleted box; a modified imported δ-ball or
  box hash; a wrong B1 semantic hash and altered B1 metadata; an altered Q coefficient (formula and expression); the
  Eg correction deleted, its factor 3 → 2, a wrong kernel sign; an altered ĥ_E; an inflated lower bound on the first
  box and at q = 0; corner values instead of derivatives, and the corner rule altered; raw c₄ > 0 claimed at either
  end; the claim widened, the corollary extended to the ends, the P_T(0) ball altered, and a failed import check.
  A modified semantic hash, a wrong hash file and a malformed certificate are rejected too.
- Method controls (`data/B2_3_method_controls.json`, 15/15 as required):
  - generator: the false bound ĉ₄ > 19/5 fails on the first box (ĉ₄ = 19/5 at q ≈ 0.00094) and at q = 0;
  - the false function 21/5 − ĉ₄, which vanishes at q ≈ 0.80316, fails on the box containing its zero and on every
    box beyond it (failures start at q = 0.42 because the quotient-regime enclosures are wide);
  - the raw c₄ fails on the first box and on the corner box;
  - the wrong kernel sign, the Eg correction deleted, the factor 3 → 2 and corner values instead of derivatives all
    give endpoint enclosures that exclude the B2.2 values;
  - the checker fails on ĉ₄ > 19/5 on the first box, on 21/5 − ĉ₄ on the box of its zero, and on the raw c₄ at both
    ends;
  - positive controls (the true carrier on boxes 50–60; the recorded bound on box 100) pass.
- Code mutations (`data/B2_3_negative_controls.json`, `scripts/negative_controls_B2_3.py`): 24 of 24 detected, 11 in
  the generator and 13 in the checker. Every target test passes on an unmutated copy first.

### 9.8 Finding: python-flint truncates arb_series at ctx.cap (B1 code path)

- python-flint (0.9.0 here) truncates every arb_series at the context length ctx.cap, whose default is 10, whatever
  length is passed. It trims only exact trailing zeros. A series requested with 16 coefficients comes back with 10.
- The B1 generator (`b1_cert._taylor`, N = 16) and the B1 checker (`b1_check.Model.taylor`, N = 20) pad the returned
  list with zeros. Their near-regime Taylor models therefore drop c₁₀, c₁₁, … and the remainder term, so they are
  unsound as written: at (q, δ) = (1.9, 0.9), the default-cap enclosures of 7 of the 16 B1 divided differences exclude
  the plain 256-bit quotient (worst 2.8·10⁻⁹ off, radius 10⁻²⁵). With ctx.cap = 32 the same code is correct.
- The stored B1 certificate is not affected:
  - B1's own checker accepts it with complete series (ctx.cap = 32): 222/222 Newton inclusions and 222/222 carrier
    bounds, no refinement. It also accepts it with the default cap;
  - the B2.3 checker, which uses no Taylor series, re-verifies all 222 imported δ-balls;
  - the dropped coefficients are small (at most 5.3·10⁻⁹ at r = 1) against the box margins.
- A B1 rebuild with ctx.cap = 32 is also valid (B1's checker accepts it). Its bytes differ (semantic hash
  77282594…, the same smallest bound 1311719/536870912), so B1's test that compares fresh and stored hashes would
  fail after a fix.
- The independent B1 replay (§5.11) used Arb at 192 bits with Taylor order 24 (python-flint 0.9.0). Its report does
  not say whether the series length was raised above ctx.cap, so it may have met the same truncation. The re-checks
  above do not depend on it.
- B1 is audited and is not changed here. Proposed erratum, for the gate:
  - set ctx.cap to the requested length in both B1 Taylor routines; a returned series is then shorter only by exact
    trailing zeros, which the zero padding restores correctly;
  - keep the audited certificate (616817fc…), which the corrected checker accepts. Replace the fresh-versus-stored
    hash test by checker acceptance of both;
  - add a regression test. Whether a short targeted re-audit is needed is a gate decision.
- Record: `data/B2_3_B1_series_cap_diagnostic.json` (`scripts/diagnose_B1_series_cap.py`).

### 9.9 Claim boundary

- Lemma Q and its corollary only, with the status CERTIFIED (computer-assisted; not independently audited when written; see §15).
- Not claimed:
  - monotonicity of ĉ₄ (the scan of §7.4 is numerical only);
  - that q = 0 is where ĉ₄ is smallest. The value 3.7993 there is certified, and it is the smallest scan value, but the
    certified bound on the whole curve is 3.6458;
  - the branch side, or a super/subcritical classification of the D2h pitchfork (B2.4);
  - stability, or the index on the centre manifold (B2.5);
  - any sign of the raw c₄ at the two ends, where it is 0.

## 10. Erratum E-B1 (V0.4-dev.4): series length in the B1 Taylor routines

**B1 status at V0.4-dev.4: CERTIFIED · INDEPENDENTLY AUDITED · IMPLEMENTATION ERRATUM PENDING TARGETED RE-AUDIT.**
(Superseded: the erratum was CLOSED in V0.4-dev.5 after the targeted re-audit, §11; current status in §15.) At V0.4-dev.4
the erratum was applied but not closed: a targeted independent re-audit (Kimi) was pending. Sections 5.7 to 5.11 are kept as written for
V0.3.1-dev; where they describe the near-diagonal Taylor code, this section corrects them.

### 10.1 The defect

- python-flint 0.9.0 truncates every `arb_series` at the context length `ctx.cap`, whose default is 10, whatever
  length `prec=` requests. The result has min(prec, ctx.cap) coefficients, less any exact trailing zeros, which are
  trimmed.
- `b1_cert._taylor` (the generator; near regime N = 16, so series of length 18 and 19) and `b1_check.Model.taylor`
  (the checker; N = 20, lengths 22 and 23) requested these longer series without raising `ctx.cap`, then padded the
  shortened lists with zeros. A truncated series was therefore read as exact zero coefficients: c₁₀, c₁₁, … were
  replaced by 0, and so was the Lagrange remainder term c_{N+1}(hull).
- **The original B1 near-diagonal Taylor implementation was therefore not rigorous as written.** Its enclosures are
  not guaranteed to contain the true divided differences.
- Reproduced before the patch on the unmodified V0.4-dev.3 archive (`scripts/reproduce_B1_erratum_pre_patch.py`,
  `data/B1_ERRATUM_pre_patch_reproduction.json`):
  - c₁₀ to c₁₅ (generator) and c₁₀ to c₁₉ (checker) are exact zeros for all seven functions at r = 1; for example,
    c₁₂ of M₂₂ is −5.6199345878802576681·10⁻¹¹ (mpmath, 60 digits) but 0 in the generator;
  - at (q, δ) = (1.9, 0.9), with the default ctx.cap, all seven near-regime divided differences of the generator and
    all seven of the checker exclude the plain quotient (f(q + δ) − f(q))/δ computed by mpmath at 60 digits. Worst
    case g_uvv: the generator's enclosure [−2.031171625660702153425980 ± 1.2·10⁻²⁵] misses −2.0311716228676517083965…
    by 2.8·10⁻⁹.
- Scope: only the near regime, i.e. the 52 near-diagonal boxes (the corner box among them). The far regime (170 boxes)
  uses ball quotients and series of length 2, which were never truncated. The two endpoint evaluations are at δ = 0,
  where every coefficient above c₂ is multiplied by 0; the corrected rebuild reproduces both endpoint records
  byte for byte.
- B1's mathematical formulas, the curve argument, the carrier, the box partition and the claimed bound are not
  affected. The defect is in the code that enclosed the divided differences near the diagonal.
- The independent B1 replay of §5.11 (Taylor order 24, python-flint 0.9.0) does not state whether it raised ctx.cap;
  it may have met the same truncation (§9.8). The evidence below does not rely on it.

### 10.2 The correction (`src/cube_bif/b1_cert.py`, `src/cube_bif/b1_check.py`)

- Generator: a context manager `_series_capacity(n)` raises `ctx.cap` to max(ctx.cap, n) and restores the previous
  value on exit, also after an exception. `_series_coefficients` checks that the capacity is in force during the
  evaluation and that no series is longer than requested. `_taylor` pads a short series only after a recomputation at
  length n + 4 shows every missing position absent or exactly zero; anything else raises `SeriesTruncationError`.
- Checker, written separately (no shared code): the context manager class `SeriesLength`, `Model._raw_series` and
  `Model.taylor`, with a recomputation at length n + 3 before any padding, and `TruncatedSeries` otherwise.
- The checks are explicit `raise` statements, not `assert`, so they stay active under `python -O`.
- Nothing else in B1 changes: formulas, Newton steps, carrier, bookkeeping, N = 16 and N = 20, 128 and 160 bits
  (`docs/V0.4-dev.4_IDENTITY_CHECK.md`, checked unit by unit).
- Test change: B1's test that compared fresh and stored semantic hashes is replaced by a pin of the stored
  certificate (616817fc…), because the corrected generator produces other bytes. The tests that the corrected checker
  accepts the stored certificate and a fresh build stay.
- `scripts/run_B1.py` is unchanged. It rewrites `data/B1_kappa_certificate.json` and must not be re-run in this
  package; the corrected rebuild is written to a separate file by `scripts/run_B1_erratum.py`.
- `scripts/diagnose_B1_series_cap.py` and its record are the B2.3 record of the finding and stay byte-identical. They
  describe the V0.4-dev.3 code.

### 10.3 The stored B1 certificate remains valid

The historical certificate `data/B1_kappa_certificate.json` (file SHA-256 dee3ad02…87ab, semantic SHA-256
616817fcc70e0fab7f106404e5e5332b17b9c4480bd440355f1ac5257a8518c6) is not overwritten. Its validity rests on three
checks that do not use the defective code (`scripts/run_B1_erratum.py`, `data/B1_ERRATUM_report.json`):

| evidence | result |
|---|---|
| corrected B1 checker (160 bits, N = 20, complete series) on the historical certificate | 222/222 Newton inclusions and 222/222 carrier bounds accepted, no refinement; both endpoints, the corner identification and the sign change of det M′ accepted; semantic hash equals the hash file; Lemma K lower bound 1311719/536870912 unchanged |
| fresh corrected rebuild, under the conditions of `scripts/run_B1.py` (mpmath 40 digits) | semantic SHA-256 b2f8e6dcd1c5073635babea2f7a6079b7ede03acbbc4f33ac3cb20f64d21d505; 222 boxes on the same q-partition (depth ≤ 2); smallest bound 1311719/536870912, as before; both endpoint records identical; claim, statement, expressions, frozen inputs and method identical; accepted by the corrected checker 222/222 and 222/222 |
| B2.3 checker (192 bits, integral divided differences, no Taylor series) | all 222 imported B1 δ-balls re-verified by its own interval Newton; 222/222 B2.3 boxes confirmed. Run in a fresh interpreter in which importing `cube_bif.b1_cert` or `cube_bif.b1_check` raises: neither module was loaded, so neither affected routine was called. Statically, `b2_check.py` imports only flint, sympy and the standard library and never uses `arb_series` |

- The rebuild differs from the historical certificate in exactly the 52 near-regime boxes (their δ-balls and lower
  bounds); the 170 far boxes are identical. Each rebuilt δ-ball overlaps the historical one, and the 52 near-box
  lower bounds are higher than before, none lower.
- Control: under the same conditions the unmodified V0.4-dev.3 generator reproduces the historical semantic hash
  616817fc… exactly in this environment (`data/B1_ERRATUM_pre_patch_reproduction.json`). So the differences come from
  the correction alone. The hash 77282594… reported in §9.8 was a rebuild at mpmath's default precision, which seeds
  the Newton steps differently.
- The rebuild is stored as `data/B1_ERRATUM_corrected_rebuild_certificate.json` (with
  `data/B1_ERRATUM_CORRECTED_REBUILD_SEMANTIC.sha256`). It is corroboration only and does not replace the historical
  certificate.
- **Lemma K is unchanged as a mathematical claim:** κ̂ ≥ 1311719/536870912 > 0 and M̂₂₂ > 0 on the closed T2g curve,
  so κ(q) ≠ 0 for 0 < q < q_c. Proposition B1 is unchanged.

### 10.4 Regression tests and controls

- `tests/test_B1_erratum.py` (15 tests). They request series longer than 10 coefficients and compare every
  coefficient up to c₂₃ (generator) and c₂₂ (checker) with mpmath at 60 digits, and c₁₀ to c₂₃ with the Cauchy integral
  formula. They require nonzero coefficients above index 10, reproduce the old routines at (1.9, 0.9) (the reference is
  excluded) and check the corrected ones there and at four more near-regime points (the reference is contained).
  They also check the restoration of ctx.cap after a call and after an exception, the detection of an unraised
  capacity, zero padding only for exact trailing zeros, the untouched historical certificate and the recorded erratum
  data.
- Code-mutation controls (`scripts/negative_controls_B1_erratum.py`, `data/B1_ERRATUM_negative_controls.json`):
  13/13 as required. Twelve mutations are detected (every named test fails; each target was first run unmutated and
  passed): the V0.4-dev.3 `_taylor` and the V0.4-dev.3 `Model.taylor` restored verbatim; `ctx.cap` fixed at 10 in
  either routine, with and without the capacity guard (in the checker the second guard in `Model._raw_series` still
  raises `TruncatedSeries`); the saved `ctx.cap` not restored; the capacity check removed; zero padding without the
  exact-zero check. The thirteenth is a documented expected non-detection: with the V0.4-dev.3 `_taylor` restored,
  the fresh-build certificate test still passes, which is why the erratum tests exist.
- Existing controls, re-run on scratch copies of V0.4-dev.4: `scripts/negative_controls.py` 34/34,
  `scripts/negative_controls_B2_2.py` 9/9 and `scripts/negative_controls_B2_3.py` 24/24 (with 16/16 unmutated
  baselines) detected; the regenerated records are byte-identical with `data/negative_controls.json`,
  `data/B2_2_negative_controls.json` and `data/B2_3_negative_controls.json`. The certificate method controls of
  `scripts/run_B1.py` (6, now through the corrected generator) and `scripts/run_A2.py` (5) are all as required; their
  records agree with `data/B1_negative_controls.json` (apart from the timing fields) and
  `data/A2_negative_controls.json` (identical). The stored records are not rewritten.
- Identity check against V0.4-dev.3 (`scripts/check_identity_V0_4_dev4.py`, `docs/V0.4-dev.4_IDENTITY_CHECK.md`):
  PASS. Every V0.4-dev.3 file is byte-identical except the allowed ones, each checked by its own rule (the two Taylor
  routines and their helpers unit by unit). 41/41 deliberate forbidden modifications, each followed by a regenerated
  SHA256SUMS, are rejected and the unmodified tree passes (`scripts/identity_controls_V0_4_dev4.py`,
  `data/B1_ERRATUM_identity_controls.json`).

### 10.5 What is not claimed

- The erratum is not closed. A targeted independent re-audit of the two corrected routines and of the evidence in
  §10.3 (Kimi) is pending.
- The independent audit of §5.11 is not re-interpreted: it audited V0.3-dev as delivered, and its replay may have used
  truncated series.
- Nothing in B2.4 or B2.5 is started. Paper 2 is untouched. Nothing is frozen, published, pushed or uploaded.

## 11. Targeted re-audit of erratum E-B1 — ERRATUM CLOSED (V0.4-dev.5)

**B1 status: CERTIFIED · INDEPENDENTLY AUDITED · ERRATUM CLOSED.** §10 is kept as written for V0.4-dev.4; its
"pending" status line is historical and this section supersedes it.

- **Auditor and record:** Kimi Agent, *Targeted Independent Re-audit Report — Paper 3 V0.4-dev.4 — B1
  `arb_series / ctx.cap` implementation erratum*, dated 2026-11-14, formal verdict **PASS**. Kept byte-identical as
  `audits/CUBE_BIFURCATIONS_V04_DEV4_B1_ERRATUM_REAUDIT.md`, SHA-256
  ba482da06aa0492b6524e47680fd949170f4d0dafac0d5661a073efce4d46b74 (provenance: `audits/README.md`).
- **Audited packages:** V0.4-dev.4 (8ae923be…c06c7) and V0.4-dev.3 (cf331557…5c81); the hashes quoted in the report
  match the archives of this project.
- **Findings, as reported:** the defect was real and produced unsound enclosures (independently reproduced at
  (1.9, 0.9) in all seven channels of both routines); the patch is correct (capacity raised and restored, also on
  exceptions; truncation rejected rather than padded; the new tests fail 8 of 15 on the old code); the historical
  certificate is valid (corrected checker 222/222 and 222/222, endpoints accepted, bound 1311719/536870912); the
  fresh corrected rebuild has semantic hash b2f8e6dc…d505 and proves the same Lemma K claim; the Taylor-free B2.3
  route re-verifies 222/222 curve balls with both affected modules blocked; the dev.3 → dev.4 diff is restricted to
  the permitted files. No critical, major or minor findings; four informational notes.
- **Auditor's conclusion:** Lemma K and Proposition B1 are unchanged; no further full B1 audit is required; the
  erratum may be marked CLOSED. This package records that status and changes no B1 file.
- The audit of §5.11 (V0.3-dev) is not re-interpreted; the re-audit supplements it for the corrected routines.

## 12. Phase B2.4 — Proposition B2: the D2h-axial pitchfork — PROVED (computer-assisted) · INDEPENDENTLY AUDITED (audit recorded in V1.0.0-rc1, §15)

Labels as in §0. The author's B2.4 request lists Lemma Q (B2.3) as certified and B1 as audited with the erratum
closed (§11). B2.4 proves the local branch structure on the D2h axis and nothing else. B2.5 (the index on the
three-dimensional centre manifold) is not started. Code: `src/cube_bif/b2_branch.py`; tests:
`tests/test_B2_branch.py`; records: `data/B2_4_branch.json`, `data/B2_4_dependency_graph.json`
(`scripts/run_B2_4.py`); controls: `data/B2_4_negative_controls.json` (`scripts/negative_controls_B2_4.py`).

**Setting.** Fix q ∈ (0, q_c) and put μ = p − P_T(q). Take the unit kernel vector n of K at μ = 0 with n_u > 0, and
keep it fixed for all μ: e₁ = n_u uh₁ + n_v vh₁, f₁ = −n_v uh₁ + n_u vh₁. Σ = Stab(e₁) (order 8, labelled D2h; §6.1).
On y* + Fix(Σ) use the orthonormal coordinates (s, w_A, w_E, w_f) along (e₁, Â, Ê, f₁). τ = nᵀ∂_pK n at μ = 0, and
c₄ = c₄(q) is the quartic coefficient of §6.2.

### 12.1 Statement

> **Proposition B2 — PROVED (computer-assisted) · INDEPENDENTLY AUDITED (audit recorded in V1.0.0-rc1, §15).** Fix q ∈ (0, q_c). Then τ < 0 (§5.8)
> and c₄ > 0 (Lemma Q and its corollary, §9.1). There are ε > 0 and μ₀ > 0, depending on q, such that for |μ| < μ₀
> the equilibria of V_p in y* + Fix(Σ) within distance ε of y* are exactly:
> - the cube y*, for every μ;
> - for μ > 0 only, two further equilibria x_±(μ) = y* ± s*(μ)e₁ + w(±s*(μ), μ), with s*(μ) > 0 and
>
>       s*(μ)² = −(6τ/c₄) μ + O(μ²);
>
> - for μ ≤ 0, no other equilibrium.
>
> x₊ and x₋ are exchanged by each of the 8 elements of N(Σ) ∖ Σ, and each has isotropy exactly Σ in O_h. The branch
> is a Z₂-symmetric pitchfork, **supercritical in the energy-reduced axial convention** (§12.4), opening towards
> p > P_T(q). Along the axial reduced coordinate s, ∂²_sV_red = τμ + O(μ²) < 0 at the cube for μ > 0 and
> ∂²_sV_red = −2τμ + O(μ²) > 0 at x_±(μ). The same holds on each of the three D2h axes (conjugate by O_h).
>
> Not claimed: the index on the three-dimensional centre manifold, stability in R²⁴, that x_± are cuboids, anything
> uniform in q or global in μ.

### 12.2 The reduced scalar equation

1. **Analyticity.** Near (y*, P_T(q)) all pair distances stay near 1, √2, √3, so V_p(x) is real-analytic in (x, p)
   (r^−p = e^(−p log r), and A = t(p, q) is analytic in p). With A = t(p, q), y* is an equilibrium for every p.
2. **Symmetric criticality** (elementary): ∇V(D(g)x) = D(g)∇V(x) with D(g) orthogonal, so ∇V(x) ∈ Fix(Σ) for
   x ∈ y* + Fix(Σ). The Σ-symmetric equilibria are therefore exactly the critical points of V restricted to
   y* + Fix(Σ).
3. **Hessian on Fix(Σ)** (B2.1, VERIFIED-EXACT, generic pair potential): in (Â, Ê, uh₁, vh₁) it is
   diag(h_A, h_E) ⊕ K(p). In (s, w_A, w_E, w_f) the s-row is (k_ss, 0, 0, k_sf), with (k_ss, k_sf, k_ff) =
   (nᵀKn, nᵀKf, fᵀKf), f = (−n_v, n_u). At μ = 0, k_ss = k_sf = 0 and the other eigenvalues are h_A, h_E and
   k_ff = tr K, all positive (Paper 2's Lemma S and Lemma T1, FROZEN INPUT). So H_WW is invertible near μ = 0.
4. **Lyapunov–Schmidt** (STANDARD, with the analytic implicit function theorem): ∂_W V(y* + s e₁ + w) = 0 has a
   unique analytic solution w = w(s, μ) near (0, 0), with w(0, μ) = 0 because the cube is an equilibrium. Put
   V_red(s, μ) = V(y* + s e₁ + w(s, μ)). Its critical points near 0 correspond one-to-one to the equilibria of V in
   y* + Fix(Σ) near y*.
5. **Evenness** (B2.0, VERIFIED-EXACT): each g ∈ N(Σ) ∖ Σ acts on Fix(Σ) as diag(1, 1, −1, −1) in (Â, Ê, uh₁, vh₁),
   i.e. (s, w_A, w_E, w_f) ↦ (−s, w_A, w_E, −w_f). It preserves the complement W = span{Â, Ê, f₁} and V, so by
   uniqueness w(−s, μ) = D(g)w(s, μ) and **V_red(−s, μ) = V_red(s, μ)**.
6. **Coefficients.** Hence V_red(s, μ) = V₀(μ) + ½λ(μ)s² + (c₄(μ)/24)s⁴ + O(s⁶), with coefficients analytic in μ:
   - λ(μ) = ∂²_sV_red(0, μ) = k_ss − k_sf²/k_ff = det K(p)/(fᵀK(p)f) (the Schur complement; exact, since
     V_red′ = V_s along w and w_s = −H_WW⁻¹H_Ws at s = 0), so λ(0) = 0 and **λ′(0) = nᵀK′(0)n = τ < 0**;
   - c₄(0) = D⁴V[e₁⁴] − 3bᵀH_WW⁻¹b with b = D³V[e₁, e₁, ·]|_W, which is the c₄ of §6.2 (b ∈ span{Â, Ê}, ⟨b, f₁⟩ = 0),
     so **c₄(0) = c₄ > 0**.

   With λ(μ) = τμ + O(μ²) and c₄(μ) = c₄ + O(μ):

       V_red(s, μ) = V₀(μ) + ½λ(μ)s² + (c₄/24)s⁴ + O(s⁶, μs⁴, μ²s²),
       ∂_sV_red = s·G(s², μ),   G(z, μ) = λ(μ) + (c₄/6)z + O(z², μz, μ²).

   G is analytic near (0, 0): an even analytic function is a power series in s², and G(z, μ) = Σ 2k a_k(μ)z^(k−1).
7. **Exact checks** (`b2_branch.py`, each tested):
   - for a generic polynomial energy in (s, w_A, w_E, w_f) with the Z₂ symmetry of step 5 (35 independent
     coefficients, coupling w_A–w_E allowed), the reduced potential has vanishing s¹, s³, s⁵ coefficients, s²
     coefficient ½(k_ss − k_sf²/k_ff) and, at k_ss = k_sf = 0, s⁴ coefficient (D⁴V − 3bᵀH_WW⁻¹b)/24, computed
     independently from the derivatives;
   - one odd monomial s³ added gives an odd coefficient (negative control);
   - the model's H|Fix(Σ) is block diagonal with the B0 block K; the Schur identity; λ(0) = 0 and λ′(0) = τ for a
     generic K(μ);
   - ∂_s of V₀ + ½λs² + (c₄/24)s⁴ + a₃s⁶ is s(λ + (c₄/6)z + 6a₃z²): the factor 6.

### 12.3 Implicit function theorem and the branch side

G(0, 0) = λ(0) = 0, G_μ(0, 0) = τ ≠ 0 and G_z(0, 0) = c₄/6 > 0. By the analytic implicit function theorem there are
a neighbourhood U of (0, 0) and a unique analytic μ*(z) with

    {(z, μ) ∈ U : G(z, μ) = 0} = {μ = μ*(z)},   μ*′(0) = −G_z/G_μ = −c₄/(6τ).

For a generic G with these first derivatives (exact): μ*(z) = −(c₄/(6τ))z + m₂z² + O(z³), and the inverse is

    z = Z(μ) = −(6τ/c₄) μ + Z₂ μ² + O(μ³),   Z₂ = 6(−c₄²g₂₀ + 6c₄g₁₁τ − 36g₀₂τ²)/c₄³,

where g₂₀, g₁₁, g₀₂ are the second-order Taylor coefficients of G. So s² = −(6τ/c₄)μ + O(μ²).

**Branch side, derived.** τ < 0 and c₄ > 0 give μ*′(0) = −c₄/(6τ) > 0. Choose z₀ > 0 with μ*′ > 0 on [−z₀, z₀].
- For small s ≠ 0, x = y* + s e₁ + w(s, μ) is an equilibrium iff G(s², μ) = 0 iff μ = μ*(s²), and μ*(s²) > 0.
  So **no nontrivial equilibrium exists for μ ≤ 0**.
- For 0 < μ < μ₀, μ* is a bijection of [0, z₀] onto [0, μ*(z₀)], so there is exactly one z = Z(μ) > 0 with
  μ*(z) = μ, and exactly two solutions s = ±s*(μ), s*(μ) = √Z(μ) > 0.

The side μ > 0 (p > P_T(q)) comes from the signs, not from an assumption. The tests derive it from the signs and
check that flipping either sign flips the side (τ > 0, c₄ > 0 or τ < 0, c₄ < 0 give μ < 0).

### 12.4 Pitchfork classification and the convention used

- The cube s = 0 is an equilibrium for both signs of μ (step 1).
- The nontrivial equilibria ±s*(μ) exist only for μ > 0, and they come as a pair.
- Every g ∈ N(Σ) ∖ Σ maps (s, w_A, w_E, w_f) to (−s, w_A, w_E, −w_f) and w(s, μ) to w(−s, μ), so D(g)x₊ = x₋. N(Σ)/Σ ≅ Z₂
  acts on the axis by s ↦ −s, and the branch is a **Z₂-symmetric pitchfork**.
- **Convention (energy-reduced axial pitchfork).** Write ν := −λ(μ) = −τμ + O(μ²) for the negative of the cube's
  axial reduced curvature. The gradient flow on the axis, ṡ = −∂_sV_red = νs − (c₄/6)s³ + …, has the normal form
  ẋ = νx − x³ after scaling when c₄ > 0. A pitchfork is called **supercritical** in this convention when the two
  nontrivial equilibria exist on the side where the cube's axial reduced curvature λ(μ) is negative, i.e. where the
  cube has lost minimality along s, and are themselves minima of V_red(·, μ). It is subcritical when they exist on the
  side where λ(μ) > 0 and are maxima of V_red. The type is the sign of c₄ and does not depend on the orientation of
  the parameter p (tested for all four sign combinations).
- Here c₄ > 0, so the pitchfork is **supercritical in the energy-reduced axial convention**. In terms of p, it opens
  towards p > P_T(q).
- "Supercritical" here refers only to the one-dimensional reduced problem on the axis. It is not a stability
  statement in R²⁴ or on the three-dimensional centre manifold. The cube is already a saddle of V_p in R²⁴
  (index ≥ 2, §4).

### 12.5 Axial reduced curvature

∂²_sV_red = G(s², μ) + 2s²G_z(s², μ) (exact).
- At the cube: ∂²_sV_red(0, μ) = λ(μ) = τμ + O(μ²). It is **negative on the branch side μ > 0** and positive for
  μ < 0.
- At s = ±s*(μ), where G = 0: ∂²_sV_red = 2Z(μ)·(c₄/6 + O(Z, μ)) = **−2τμ + O(μ²) > 0** (exact series; G vanishes on
  the branch through order μ²).

This is a statement about the one-dimensional axial reduced direction only. No Morse index on the
three-dimensional centre manifold and no full-space stability is inferred. Scope note for B2.5 (not a claim): at
a = (s, 0, 0) the cubic invariant κa₁a₂a₃ of §5 puts κs in the (a₂, a₃) entry of the 3 × 3 reduced Hessian, and
κ ≠ 0 (Lemma K). So the centre-manifold index at x_± is not determined by c₄ alone.

### 12.6 Geometry (what is rigorously supported)

- **Exact isotropy** (VERIFIED-EXACT): for every R ∈ O_h, the rank of (D(R) − I)[uh₁, vh₁] is 0 if R ∈ Σ and 2
  otherwise. The T2g isotypic projector commutes with every D(R), kills Â and Ê, and fixes uh₁, vh₁. So every point
  of y* + Fix(Σ) with a nonzero (uh₁, vh₁) component has isotropy exactly Σ. On the branch that component is
  ±s*e₁ + O(s*³)f₁ ≠ 0, so **x_± have isotropy exactly Σ ≅ D2h**: not D4h, and not O_h.
- **Not a cuboid configuration in the sense of Paper 2:** Σ contains only 4 of the 8 diagonal sign matrices Z₂³, so
  x_± are not in Fix(Z₂³), the cuboid family A1g ⊕ Eg (Fix(Σ) ∩ Fix(Z₂³) = span{Â, Ê}, §6.1). The branch is not called
  a cuboid.
- **Shape to the orders that are proved:** x_±(μ) − y* = ±s*e₁ + s*²(ω_A Â + ω_E Ê) + O(s*³), with
  (ω_A, ω_E) = −½(b_A/h_A, b_E/h_E) at μ = 0. The f₁ component is odd in s, and its linear coefficient
  −k_sf(μ)/k_ff = O(μ) = O(s*²), so it is O(s*³). These follow from the exact generic expansion.
- **First order** (B2.0, VERIFIED-EXACT): ±s*e₁ moves vertex s by ∓(s* n_u/4)(0, s₃, s₂) ∓ (s* n_v√2/4)(s₁s₂s₃)(1, 0, 0).
  - The first term maps each cross-section x = const by (y, z) ↦ (y − εz, z − εy), ε = ±s* n_u/2. The square becomes
    a **rhombus** (exact: four equal sides, perpendicular diagonals scaled by 1 − ε along (0, 1, 1) and 1 + ε along
    (0, 1, −1), adjacent-side inner product −2ε ≠ 0). The cross-sections are sheared, not rectangular. x₊ and x₋ are
    the two rhombi with the diagonals exchanged.
  - The second term moves the two tetrahedra in opposite directions along x, with weight n_v (the opposite
    translation component of B0/B2.0). n_v = ρ/√(1 + ρ²) with ρ = 0.0213, 0.0249, 0.0273, 0.0278 at
    q = 0.2, 0.8, 1.5, 2.0 (numerical). That n_v ≠ 0 on the whole curve is not certified here.
- **Second order:** a uniform breathing (A1g) and a tetragonal strain along x (Eg). Both are D4h-symmetric. Their
  signs and sizes are not claimed.
- The branch remains Σ-symmetric (D2h) for all small μ > 0, because it lies in y* + Fix(Σ).

### 12.7 Proof dependency graph

`data/B2_4_dependency_graph.json` (from `b2_branch.DEPENDENCY_GRAPH`). Its leaves are exactly the six proof inputs
allowed by the B2.4 request; every other node is a derivation step of this phase.

| node | role | status | content |
|---|---|---|---|
| B20_parity_fixed_space | input: exact B2.0 parity/fixed-space results | VERIFIED-EXACT | Σ = Stab(e₁); Fix(Σ) = span{Â, Ê, uh₁, vh₁}; N(Σ) ∖ Σ acts as diag(1, 1, −1, −1); first-order displacement (§6.1) |
| B21_LS_c4_identity | input: exact B2.1 LS coefficient identity | VERIFIED-EXACT | H\|Fix(Σ) = diag(h_A, h_E) ⊕ K; c₄ = D⁴V − 3⟨b, H⊥⁻¹b⟩ = qW_q(p − q)ĉ₄, ⟨b, f₁⟩ = 0 (§6.1–6.2) |
| LQ_lemma_Q | input: certified Lemma Q (B2.3) | CERTIFIED | ĉ₄ > 0 on the closed curve, hence c₄ > 0 for 0 < q < q_c (§9.1; not independently audited when written; see §15) |
| B18_tau | input: audited B1/Paper 2 transversality | FROZEN INPUT | τ < 0 for 0 < q < q_c, ker K = span{n} on the curve (§5.8; audited with B1) |
| STD_lyapunov_schmidt | input: standard | STANDARD | equivariant Lyapunov–Schmidt reduction, one-dimensional kernel |
| STD_implicit_function_theorem | input: standard | STANDARD | analytic implicit function theorem |
| X_generic_LS, L1–L5 | derivation steps | VERIFIED-EXACT | the exact algebra of §12.2–12.6 |

Facts that an allowed input already rests on, as recorded earlier in these notes, are listed in that node's
`includes` field and are not separate inputs:
- B21_LS_c4_identity includes its recorded hypotheses h_A, h_E > 0 (Paper 2's Lemma S) and tr K > 0 (Lemma T1), §6.2;
- LQ_lemma_Q includes the corollary c₄ > 0 of §9.1, which uses Paper 2's Lemmas T2 and T3;
- B18_tau includes Paper 2's Lemmas T1 and T3 and the exact adj identity, §5.8;
- STD_lyapunov_schmidt includes its hypotheses, checked in §12.2 steps 1–2 (analyticity; symmetric criticality for the
  finite orthogonal O_h action);
- B20_parity_fixed_space is stated in the exact B0 bases and block K.

`validate_graph` checks that the graph is acyclic; that every node reachable from the proposition is either a
VERIFIED-EXACT derivation step or one of the six allowed inputs with its expected status; that all six are reachable;
and that no corroboration-only node and no VERIFIED-NUMERIC, CANDIDATE or RECONNAISSANCE node is reachable. Adding
any other input fails, even one with an acceptable status (tested with B1's Lemma K and with Paper 2's Lemma S as
separate leaves). **No numerical scan is a proof dependency.** The B2.2 scan and the B2.4 numerics are listed only as
corroboration.

### 12.8 Numerical corroboration (VERIFIED-NUMERIC; not used in the proof)

Newton in the four Fix(Σ) coordinates, with the 24-D pair energy, gradient and Hessian of `numeric.py` at 60 digits,
at p = P_T(q)(1 + r) with r = ±10⁻⁶, ±10⁻⁷, started at ±√|6τμ/c₄|. The reduced scan solves w(s) by Newton at fixed s
and evaluates g(s) = ⟨∇V, e₁⟩ on 24 points of (0, 3√|6τμ/c₄|] (50 digits).

| q | P_T(q) | τ | c₄ | −6τ/c₄ | s* (r = 10⁻⁶) | s²/s_pred² − 1 (10⁻⁶ / 10⁻⁷) | ratio | max ‖∇V‖ (24-D) | max abs(s) for μ < 0 | ∂²_sV_red / (−2τμ) at s* | at cube / (τμ) | ‖D(g)x₊ − x₋‖ |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 0.2 | 4.42475418813 | −0.0879094 | 7.408562 | 0.0711955 | ±0.000561268 | −9.01·10⁻⁷ / −9.01·10⁻⁸ | 9.99999 | 1.4·10⁻⁶⁰ | 1.8·10⁻⁵⁴ | 1.000001 | 1.0 | 1.1·10⁻⁵⁷ |
| 0.8 | 3.47191462722 | −0.243686 | 17.70546 | 0.0825800 | ±0.000535453 | −7.56·10⁻⁷ / −7.56·10⁻⁸ | 9.99999 | 2.3·10⁻⁶⁰ | 1.6·10⁻⁵⁴ | 1.000001 | 1.000001 | 5.3·10⁻⁵⁷ |
| 1.5 | 2.57741335955 | −0.191835 | 12.23355 | 0.0940866 | ±0.000492443 | −5.92·10⁻⁷ / −5.92·10⁻⁸ | 10.0 | 1.5·10⁻⁶⁰ | 6.3·10⁻⁵⁵ | 1.000002 | 1.000002 | 3.1·10⁻⁵⁶ |
| 2.0 | 2.03992796219 | −0.00949161 | 0.5631302 | 0.101131 | ±0.000454201 | −4.83·10⁻⁷ / −4.83·10⁻⁸ | 10.0 | 1.1·10⁻⁶⁰ | 6.5·10⁻⁵³ | 1.000051 | 1.000051 | 3.5·10⁻⁵⁵ |

- For μ > 0, Newton started at ±s finds both ±s* (s₋ = −s₊ to 10⁻⁴⁰) with the full 24-D gradient below 10⁻⁵⁹. For
  μ < 0, started at the mirror amplitude, it returns to the cube.
- Amplitude law: the relative error of s² against −6τμ/c₄ falls by a factor 10.0000 when μ falls by 10, so it is
  O(μ), as the exact second-order term Z₂μ² predicts.
- Reduced scans: g(s)/s changes sign exactly once on (0, 3s_pred] for r = +10⁻⁶ and never for r = −10⁻⁶ (there it
  stays positive, close to λ(μ) ≈ τμ > 0), at all four q.
- The axial curvature (the Schur complement of the 4 × 4 Fix Hessian onto e₁) agrees with τμ at the cube and with
  −2τμ at s*, to the expected O(μ). The f₁ component of x_± is O(s*³).
- An element of N(Σ) ∖ Σ maps the located x₊ onto the located x₋.
- 88/88 numerical checks pass (`data/B2_4_branch.json`, regenerated serially from an empty record; it is
  reproduced bit for bit).
- Scope of the μ < 0 evidence: Newton from the mirror amplitude and a 24-point sample of g(s)/s on
  (0, 3√|6τμ/c₄|]. This does not exclude roots between sample points or far from the cube. Local absence of a
  nontrivial branch for μ ≤ 0 is the analytic result of §12.3, not of the numerics.

### 12.9 Tests and controls

- `tests/test_B2_branch.py`, 51 tests:
  - exact layer: 12;
  - the statement and the graph: 4 (including the six-input restriction);
  - 21 incorrect statements rejected;
  - 10 invalid dependency graphs rejected;
  - numerical corroboration: 3 (corroboration only, not part of the proof);
  - records: 1.
- The rejected statements and graphs include, as required:
  - wrong sign of τ and wrong sign of c₄;
  - a missing factor 6 (in G, in the amplitude law and in μ*′(0));
  - evenness removed (as a flag and as a cubic term);
  - the branch claimed on both sides;
  - the B2.2 scan used instead of Lemma Q, or added as a proof dependency;
  - the axial curvature upgraded to full-space stability or to a centre-manifold index.
- They also cover a wrong side, a wrong amplitude sign, the subcritical label, a missing convention, wrong curvature
  signs, a cuboid claim, an upgraded audit status, a cycle, a dropped τ input, a CANDIDATE input, an unlisted input
  (B1's Lemma K), a derivation step without exact status and an allowed input with the wrong status.
- Code-mutation controls (`scripts/negative_controls_B2_4.py`): **22/22 detected**. Each of the
  15 targets passes unmutated first. They cover:
  - the sign of τ (twice) and the sign of c₄;
  - the factor 6, evenness removed and the transverse solve dropped;
  - the branch on both sides, the classification swapped, the curvature factor 2 and the exchange action;
  - two statement edits and three graph edits (the B2.2 scan as proof, twice; Paper 2's Lemma S as an extra leaf);
  - seven validator sabotages (including the six-input restriction switched off).

### 12.10 Claim boundary

- Proposition B2 only, with the status **PROVED (computer-assisted; not independently audited when written; see §15)**. Every proof
  dependency is VERIFIED-EXACT, CERTIFIED (Lemma Q, not independently audited when written; see §15), FROZEN INPUT (Paper 2; B1.8, audited)
  or STANDARD.
- Local in (s, μ) for each fixed q ∈ (0, q_c). No uniformity in q, and no statement at q = 0 or at the corner, where
  c₄ = 0.
- Not claimed:
  - the index on the three-dimensional centre manifold, or stability in R²⁴ (B2.5);
  - stability of the branch within any larger family;
  - that the branch configurations are cuboids, or any edge-length or angle statement beyond first order;
  - that n_v ≠ 0 on the whole curve;
  - equilibria outside y* + Fix(Σ) (for example the D3d branches of Proposition B1).
- Not independently audited when written (audited since; see §15). Not frozen, not published, nothing pushed or uploaded.

## 13. Phase B2.5 — Proposition B3: the centre-manifold index of the D2h branch — PROVED (computer-assisted) · INDEPENDENTLY AUDITED (audit recorded in V1.0.0-rc1, §15)

Labels as in §0. B2.5 determines the Morse index of the three-dimensional T2g centre-manifold (Lyapunov–Schmidt)
reduced Hessian at the D2h branch points of Proposition B2, and then, from explicitly named frozen Paper 2 results, the
full-slice index. No global branch problem, no A3, no C2h secondary-branch study. Code: `src/cube_bif/b2_index.py`;
tests: `tests/test_B2_index.py`; records: `data/B2_5_index.json`, `data/B2_5_dependency_graph.json`
(`scripts/run_B2_5.py`); controls: `data/B2_5_negative_controls.json` (`scripts/negative_controls_B2_5.py`).

**Input statuses.** The author's B2.5 request designates as established inputs: B1 (κ ≠ 0, D3d result; independently
audited, §5.11, §11), B2.3 (Lemma Q, "independently re-certified") and B2.4 (Proposition B2, "independently
audited"). This package contains the audit reports for Track A, B1 and erratum E-B1 only. **No audit report for B2.3
or B2.4 is in this package (NOT_PROVIDED here).** (Resolved in V1.0.0-rc1: both reports were received, PASS; §15.) §9
and §12 therefore kept their labels as written at V0.4-dev.6, and the dependency graph records the author's designation together with this fact. Proposition B3 uses
Proposition B2 as a PROVED (computer-assisted) input; its own status below does not depend on the audit label of B2.

**Setting.** Fix q ∈ (0, q_c), μ = p − P_T(q), the unit kernel vector n of K at μ = 0 with n_u > 0 (the gauge of §5
and §12), e_k = n_u uh_k + n_v vh_k and f_k = −n_v uh_k + n_u vh_k (k = 1, 2, 3). E_c = span{e₁, e₂, e₃} is the
critical T2g space. The slice is S = y* + R^⊥ (R = the six rigid-motion fields at y*); W ⊂ R^⊥ is the orthogonal
complement of E_c in R^⊥ (dimension 15). Coordinates a = (a₁, a₂, a₃) on E_c.

### 13.1 Statement

> **Proposition B3 — PROVED (computer-assisted) · INDEPENDENTLY AUDITED (audit recorded in V1.0.0-rc1, §15).** Fix q ∈ (0, q_c), and let x_±(μ),
> 0 < μ < μ₁(q), be the D2h equilibria of Proposition B2. Let V_red(a, μ) be the Lyapunov–Schmidt reduced potential on
> the three-dimensional critical space E_c. Then
>
>     V_red(a, μ) = V₀(μ) + ½λ(μ)|a|² + κ(μ) a₁a₂a₃ + α(μ)|a|⁴ + β(μ)(a₁⁴ + a₂⁴ + a₃⁴) + O(|a|⁵),
>
> with λ(0) = 0, λ′(0) = τ < 0, κ(0) = κ ≠ 0 (Lemma K) and α + β = c₄/24 > 0 (B2.1, Lemma Q). At x_± (a = (±s*, 0, 0),
> s*² = −(6τ/c₄)μ + O(μ²)) the reduced Hessian is
>
>     H_c = [[h₁₁, 0, 0], [0, d, e], [0, e, d]],   h₁₁ = (c₄/3)s² + O(s⁴) = −2τμ + O(μ²),
>     d = −4βs² + O(s⁴),   e = κs + O(s³),   det[[d, e], [e, d]] = −κ²s² + O(s⁴),
>
> with s = ±s*. Its transverse eigenvalues are d ± e on (0, 1, ±1)/√2, one positive and one negative. Hence
>
>     index_centre(D2h branch) = 1,   nullity 0,
>
> for every sufficiently small μ > 0, independently of the gauge sign of κ and of s ↔ −s. All six D2h branch points
> (±s*e_k, k = 1, 2, 3) are conjugate under O_h and have the same index.
>
> Not claimed: stability in any sense, an explicit radius μ₁(q), anything uniform in q or global in μ.

### 13.2 The reduced potential and its invariant structure

1. **Reduction** (STANDARD). Near (y*, P_T(q)) V_p is real-analytic (§12.2 step 1). On the slice S the Hessian at the
   transition point has kernel exactly E_c (Paper 2: the lower T2g eigenvalue vanishes on the curve, Lemma T3, and
   every other block is nonzero, Theorem (index)). H_WW is invertible there (indefinite: index 3, §13.6), which is
   all the implicit function theorem needs. So ∂_W V(y* + Σa_k e_k + w) = 0 has a unique analytic solution
   w = w(a, μ), w(0, μ) = 0, and V_red(a, μ) = V(y* + Σa_k e_k + w(a, μ)). Critical points of V_red near 0 correspond
   one-to-one to equilibria of V in S near y*; equilibria of V in S are equilibria in R²⁴ (V is E(3)-invariant, so
   ∇V(x) ⟂ the rigid orbit at x).
2. **Equivariance** (B0/B2.0, VERIFIED-EXACT). O_h acts on E_c by T(R) = σ(R)R (§4); the 48 elements give 24 distinct
   3×3 matrices (the signed permutations with an even number of −1). By uniqueness of w, V_red(T a, μ) = V_red(a, μ).
3. **Invariants** (VERIFIED-EXACT, Reynolds operator over the 24 matrices). The invariant polynomials of degree 1–6
   have dimensions 0, 1, 1, 2, 1, 3. Degree 2 is spanned by I₂ = |a|², degree 3 by I₃ = a₁a₂a₃, degree 4 by I₂² and
   I₄ = Σa_k⁴ (the quartic basis is derived, not assumed). Hence the normal form of §13.1, with coefficients analytic
   in μ.
4. **Cubic coefficient.** w = O(|a|²), so the cubic part of V_red is (1/6)D³V[x, x, x] with x = Σa_k e_k; the only
   invariant monomial is a₁a₂a₃, with coefficient D³V[e₁, e₂, e₃] = κ, the B1 coefficient (§5). Lemma K: κ ≠ 0 for
   0 < q < q_c (κ > 0 in the gauge n_u > 0).
5. **Complete quartic after LS elimination** (VERIFIED-EXACT, generic pair potential). With b(x) = D³V[x, x, ·]|_W,
   V₄ = (1/24)D⁴V[x⁴] − (1/8)⟨b, H_WW⁻¹b⟩ (the multi-dimensional LS formula, checked on a generic energy with all 55
   cubic and quartic monomials). b(x) has components only in A1g, Eg and T2g (the f_k), all other isotypic components
   vanish exactly, so H_WW⁻¹ acts on b through h_A, h_E and k_ff = tr K > 0 (Paper 2, Lemmas S and T1). The result is
   exactly of the form αI₂² + βI₄, with
   α = Q_mix/8 − b_A²/(8h_A) + b_E²/(16h_E) − κ_f²/(4k_ff),  β = c₄/24 − α,
   Q_mix = D⁴V[e₁, e₁, e₂, e₂], κ_f = D³V[e₁, e₂, f₃]; α + β = c₄/24 is the B2.1 identity. A hand formula and an
   independent derivative-free numerical evaluation (§13.8) agree.
6. **Identification with Proposition B2** (VERIFIED-EXACT). On the axis a = (s, 0, 0) the solution w is Σ-fixed by
   uniqueness, so it is the LS solution of §12.2 on Fix(Σ), and V_red(s, 0, 0, μ) is the axial potential of
   Proposition B2. In particular c₄ = 24(α + β), and the critical points (±s*, 0, 0) are x_±: by the symmetry of
   step 7 the gradient of V_red at (s, 0, 0) is (∂_sV_red, 0, 0).

### 13.3 The Hessian on the axis and on the branch

7. **Symmetry form** (VERIFIED-EXACT). The stabiliser of the axis (1, 0, 0) in the 24 matrices has order 4. Its
   commutant forces the Hessian of any invariant C² function at (s, 0, 0) to be [[h₁₁, 0, 0], [0, d, e], [0, e, d]].
   The 4 axis-reversing elements show h₁₁ and d even in s and e odd in s.
8. **Generic expansion** (VERIFIED-EXACT, generic invariant polynomial through degree 6, all invariant coefficients
   symbolic): h₁₁ = λ + 12(α + β)s² + O(s⁴), d = λ + 4αs² + O(s⁴), e = κs + O(s³). The cubic term is the only O(s)
   contribution, and it sits off the diagonal: **no competing O(s) diagonal term**.
9. **On the branch** (VERIFIED-EXACT, with μ-dependent λ, κ, α, β and μ = μ*(s²) solved order by order from
   ∂_sV_red = 0): μ*′(0) = −c₄/(6τ) (Proposition B2), λ = −(c₄/6)s² + O(s⁴), and
   h₁₁ = (c₄/3)s² + O(s⁴) = −2τμ + O(μ²) (the audited B2.4 axial curvature), d = −4βs² + O(s⁴), e = κs + O(s³),
   det = d² − e² = −κ²s² + O(s⁴).

### 13.4 Transverse splitting with a remainder bound (analytic)

10. The transverse block [[d, e], [e, d]] has eigenvalues d + e and d − e on (0, 1, 1)/√2 and (0, 1, −1)/√2, exactly.
11. **Remainder bound.** d and e are analytic in s along the branch, d even with d(0) = 0, e odd with e′(0) = κ.
    Write d = s²D(s), e = s(κ + s²E(s)) with D, E analytic, and fix r > 0 inside their domain with |D| ≤ C_D,
    |E| ≤ C_E on |s| ≤ r (r ≤ 1). Then (d + e)(d − e) = s²[s²D² − (κ + s²E)²] exactly, and for
    0 < |s| < min(r, |κ|/(C_D + C_E)):
    |sD| ≤ C_D|s| < |κ| − C_E|s| ≤ |κ| − C_E s² ≤ |κ + s²E|,
    so (d + e)(d − e) < 0: **one positive and one negative transverse eigenvalue**, whatever the signs of κ and s.
    The identity and the inequality chain are checked exactly (432 rational worst cases, including D = ±C_D and
    E = −sign(κ)C_E). The O(s²) corrections therefore cannot overturn the O(|s|) splitting for small branch amplitude.
12. **Rigor class.** The argument is analytic (Taylor remainders), given the inputs. No explicit radius is computed and
    **no interval-arithmetic certificate is produced in B2.5**. The status is computer-assisted overall because its
    inputs Lemma K and Lemma Q are Arb certificates and the exact algebra is computer algebra (SymPy).

### 13.5 Centre-manifold index

13. h₁₁ = (c₄/3)s² + O(s⁴) > 0 for small s ≠ 0 (c₄ > 0), and the transverse block has inertia (1, 0, 1). The 3×3
    matrix is block diagonal, so **index_centre = 0 + 1 = 1, nullity 0**. The leading-order Hessian has exactly one
    negative eigenvalue for both signs of κ and of s, and for both signs of β (tested exactly). The negative direction
    is (0, 1, −sign(κs))/√2 at leading order. The axial curvature alone would give index 0; the index comes from the
    κs splitting, which needs κ ≠ 0. If κ = 0 the index is not determined at this order (the code returns None).
14. **Conjugate branches** (VERIFIED-EXACT). The 24 matrices map (1, 0, 0) onto exactly the six points ±e_k, and in
    R²⁴ the O_h-orbit of e₁ is {±e₁, ±e₂, ±e₃}. For an invariant function Hess F(Ta) = T Hess F(a) Tᵀ with T
    orthogonal (checked for all 24 T), so the six branch points have congruent Hessians: one index type. Symmetry
    copies are not counted as distinct.

### 13.6 Corollary B3′: the full-slice index (from frozen Paper 2 results)

> **Corollary B3′ — PROVED (computer-assisted) · INDEPENDENTLY AUDITED (audit recorded in V1.0.0-rc1, §15).** For fixed q ∈ (0, q_c) and
> 0 < μ < μ₂(q) ≤ μ₁(q), the Hessian of V at x_±(μ) restricted to the slice has index m_⊥ + 1 = **4** and nullity 0;
> in R²⁴ it has 4 negative eigenvalues, the 6 rigid zero modes, and 14 positive eigenvalues. Rigid translations and
> rotations are not counted. Not claimed: stability (index 4 is not stability), anything uniform in q.

15. **Frozen inputs used** (Paper 2, Theorem (index) (b)–(d) on p = P_T(q), 0 < q < q_c; FROZEN INPUT), by block of
    Γ₂₄ = A1g + Eg + T1g + 2T2g + A2u + Eu + 2T1u + T2u:

    | block | dim | sign on the curve | Paper 2 source |
    |---|---|---|---|
    | A1g | 1 | + | Lemma S |
    | Eg | 2 | + | Lemma S |
    | T1g (rotations) | 3 | 0, rigid, excluded | setup (rigid modes) |
    | T2g lower (critical) | 3 | 0, the centre space E_c | Lemma T3 (D(P_T(q), q) = 0), Lemma T1 |
    | T2g upper (noncritical copy) | 3 | + | Lemma T1 (tr K > 0, λ₊ > 0) |
    | A2u | 1 | − | Lemma T4 (D ≤ 0 ⇒ λ_A2u < 0) |
    | Eu | 2 | − | Lemma E |
    | T1u (translations) | 3 | 0, rigid, excluded | setup (rigid modes) |
    | T1u (internal) | 3 | + | Lemma S |
    | T2u | 3 | + | Lemma S |

16. **m_⊥ is derived, not assumed.** Counting the table: rigid 6, critical 3, W = the other 15 directions, with
    3 negative (A2u + Eu), 12 positive, 0 zero. So H_WW is invertible with **m_⊥ = 3**, at every point of the
    physical curve. Paper 2's index formula, ind H_red = 2 + 1{q ≥ r* or p > P_A(q)} + 3·1{q ≥ q_c or p > P_T(q)},
    gives 3 on the curve in both cases q < r* and r* ≤ q < q_c (Lemma T4: P_T > P_A for q < r*), with nullity 3: the
    same count. The quoted signs are checked against Paper 2's own archive (`data/cube_index_theorem.json`
    monotonicity record and the Table in `sections/05_morse_classification.tex`), when the archive is present.
17. **Splitting** (STANDARD: Haynsworth inertia additivity; checked exactly on random rational matrices). At a critical
    point of the reduction, D²V_red = H_cc − H_cW H_WW⁻¹ H_Wc (chain rule; checked exactly through second order for
    generic energies), so In(H|_S) = In(H_WW) + In(D²V_red). H_WW at x_±(μ) is a small perturbation of H_WW at
    (y*, P_T(q)), which is invertible with index 3; for 0 < μ < μ₂(q) its index stays 3. Hence the slice index is
    3 + 1 = 4, nullity 0. The rigid fields at x_± lie in the kernel of the R²⁴ Hessian (V is E(3)-invariant), and
    R(y*)^⊥ is a complement of that kernel for x_± near y*, so the R²⁴ Hessian has inertia (4, 6, 14).
18. If any quoted block sign changed (for example A2u not negative), the derived m_⊥ changes and index 4 is not
    derivable; if a W-block were zero, the corollary is withheld (tested).

### 13.7 D3d consistency check (not a new proposition)

19. The same normal form on a = t(1, 1, 1): Hess V_red = λI + κt(J − I) + O(t²), and on the D3d branch
    λ = −κt + O(t²). Axial eigenvalue κt, transverse (double) −2κt, with κt = −τμ + O(μ²), so sign(κt) = sign(μ)
    (τ < 0). Centre index 2 for μ > 0 and 1 for μ < 0; full index 5 and 4. This agrees with the transcritical D3d
    result of B1 (§5) and with the local degree bookkeeping: Σ(−1)^index over the cube, the four D3d points and (for
    μ > 0) the six D2h points is −1 + 4 − 6 = −3 for μ > 0 and +1 − 4 = −3 for μ < 0. The sign conventions of B1 and
    B2 are consistent. Consistency only; not used in the proof.

### 13.8 Numerical corroboration (VERIFIED-NUMERIC; not used in the proof)

Raw 24-D route, mpmath at 60 digits, independent of the normal form: Newton on the full 24-D gradient from the
leading-order amplitude, then the full 24×24 Hessian, its spectrum, the slice basis, H_WW, and the Schur complement
onto E_c. q = 0.2, 0.8, 1.5, 2.0; μ = r·P_T(q) with r = 10⁻⁵, 10⁻⁶, 10⁻⁷; both signs of s.

| q | r | s* | h₁₁ | d + e, d − e | rel. error of (h₁₁, d, e) vs leading order | ‖∇V‖ |
|---|---|---|---|---|---|---|
| 0.2 | 10⁻⁵ | 1.775·10⁻³ | 7.780·10⁻⁶ | 8.49·10⁻⁶, −1.57·10⁻⁵ | 1.5·10⁻⁵, 1.2·10⁻⁵, 7.4·10⁻⁵ | 6·10⁻⁶¹ |
| 0.2 | 10⁻⁷ | 1.775·10⁻⁴ | 7.780·10⁻⁸ | 1.17·10⁻⁶, −1.25·10⁻⁶ | 1.5·10⁻⁷, 1.2·10⁻⁷, 7.4·10⁻⁷ | 1·10⁻⁶⁰ |
| 0.8 | 10⁻⁷ | 1.693·10⁻⁴ | 1.692·10⁻⁷ | 3.80·10⁻⁶, −3.96·10⁻⁶ | 1.7·10⁻⁷, 1.6·10⁻⁷, 5.1·10⁻⁷ | 2·10⁻⁶⁰ |
| 1.5 | 10⁻⁷ | 1.557·10⁻⁴ | 9.889·10⁻⁸ | 2.86·10⁻⁶, −2.95·10⁻⁶ | 2.8·10⁻⁷, 2.7·10⁻⁷, 5.1·10⁻⁷ | 1·10⁻⁶⁰ |
| 2.0 | 10⁻⁵ | 1.436·10⁻³ | 3.874·10⁻⁷ | 1.09·10⁻⁶, −1.45·10⁻⁶ | 5.1·10⁻⁴, 5.1·10⁻⁴, 5.3·10⁻⁴ | 5·10⁻⁶¹ |
| 2.0 | 10⁻⁷ | 1.436·10⁻⁴ | 3.872·10⁻⁹ | 1.25·10⁻⁷, −1.29·10⁻⁷ | 5.1·10⁻⁶, 5.1·10⁻⁶, 5.3·10⁻⁶ | 9·10⁻⁶¹ |

- At every point (24 equilibria): R²⁴ inertia 4 negative, 6 zero (the rigid fields are in the kernel to 10⁻⁵⁰),
  14 positive; H_WW index 3; the Schur complement onto E_c has index 1, nullity 0; h₁₂ = h₁₃ = 0 and h₂₂ = h₃₃ to
  10⁻⁴⁵; transverse eigenvalues of opposite sign with the negative direction (0, 1, −sign(κs)).
- As μ → 0⁺ the three small centre eigenvalues keep the predicted pattern (+, +, −): h₁₁ ∝ μ (ratio 10 per decade),
  transverse ±|κs| ∝ √μ (ratio √10 per decade).
- The relative errors are O(μ): they fall by 10 per decade at every q. The constant is ≈ 1.5–7.4 for q ≤ 1.5 and
  ≈ 51–53 at q = 2.0 (c₄ is small there; the cube's smallest |H_WW| eigenvalue is 0.0153 at q = 2.0 against 0.24–0.52
  at the other q). **Tolerance change, recorded:** the first run used a pass bound of 50·r for this check, and six
  q = 2.0 checks failed (values 51.3·r to 53.4·r). After inspecting them the bound was raised to 200·r. The O(μ)
  scaling check (ratio 7–13 per decade) is separate and was not changed. This is a data-informed numerical threshold,
  not a certificate.
- The cube on the curve (p = P_T(q), 4 values of q): index 3, 9 zero eigenvalues (6 rigid + 3 critical), H_WW index 3,
  smallest |H_WW| eigenvalue 0.0153–0.520.
- D3d (r = ±10⁻⁶): R²⁴ index 5 (μ > 0) and 4 (μ < 0), centre index 2 and 1; axial ≈ κt and transverse ≈ −2κt.
- Quartic route 3 (derivative-free nonlinear LS evaluation of V₄ at 5 directions × 4 q, Richardson-extrapolated):
  agrees with αI₂² + βI₄ to relative 10⁻²⁸–10⁻¹⁸.
- 300/300 numerical checks pass (after the tolerance change above).

### 13.9 Proof dependency graph

`data/B2_5_dependency_graph.json` (from `b2_index.DEPENDENCY_GRAPH`), two roots.

| node | role | status | content |
|---|---|---|---|
| IN_exact_Oh_T2g_structure | input: exact O_h/T2g invariant structure | VERIFIED-EXACT | B0 (§4), B2.0 (§6.1), exact isotypic projectors |
| IN_lemma_K_kappa | input: audited κ ≠ 0 | CERTIFIED | Lemma K, independently audited, erratum closed (§5.7, §5.11, §11) |
| IN_proposition_B2 | input: Proposition B2 branch/amplitude | PROVED (computer-assisted) | §12; includes Lemma Q and τ < 0 as recorded in its own graph; audit designated by the author, report not in this package |
| STD_LS_centre_manifold | input: standard | STANDARD | equivariant LS reduction with a 3-D kernel on the slice, Schur complement, Haynsworth inertia additivity, analytic IFT, Taylor's theorem |
| P2_theorem_index_on_curve | input (Corollary B3′ only) | FROZEN INPUT | Paper 2 Theorem (index) (b)–(d): block signs on the curve (table of §13.6) |
| S1–S8, C1, C2 | derivation steps | VERIFIED-EXACT | §13.2–13.6 |

- P_B3 (Proposition B3) reaches exactly the first four inputs and **does not reach the Paper 2 spectral input**: the
  centre index does not use it. C_B3 (Corollary B3′) adds P2_theorem_index_on_curve.
- `validate_graph` rejects: cycles; any unlisted input; a derivation step that is not VERIFIED-EXACT; any
  VERIFIED-NUMERIC, CANDIDATE, RECONNAISSANCE or ASSUMED node; any corroboration- or consistency-only node (the B2.2
  scan, the B2.5 numerics, the D3d check) as a dependency; node text describing a scan or an assumption; a dropped
  required input; a root status other than the one stated in §13.1 and §13.6.
- **No numerical scan is a proof dependency.**

### 13.10 Tests and controls

- `tests/test_B2_index.py`: 71 tests (exact layer, statement and graph validators, Paper 2 archive cross-check, live
  numerical corroboration). They include 23 rejected false statements of Proposition B3, 11 rejected false statements
  of Corollary B3′ and 12 rejected graphs. Required false alternatives and where they are rejected:
  - transverse block positive definite / negative definite: statement tests and code mutations;
  - omission of the κs term; κs replaced by κs²: statement tests and code mutations of the generic potential;
  - the axial curvature alone counted as the centre index: statement test and a code mutation of the index count;
  - full-space stability claimed from the centre index: statement tests (Proposition and Corollary);
  - rigid motions counted in the Morse index: corollary tests (index 10; flag; zero-mode count) and a code mutation;
  - the Paper 2 complementary index assumed instead of derived: corollary tests, a graph test (m_⊥ as an ASSUMED
    input) and frozen-table mutations (A2u sign flipped gives m_⊥ = 2; Eu zero withholds the corollary).
- Code-mutation controls (`scripts/negative_controls_B2_5.py`, record `data/B2_5_negative_controls.json`):
  **28/28 detected**; each of the 15 target tests passes on the unmutated code. They cover the κs term dropped
  or replaced by κs² in the derivation, the transverse block made definite, the axial curvature counted alone, the
  factor in c₄ = 24(α + β), the parity of e, the remainder radius, statement and corollary flags (definite blocks,
  κs², stability, audited status, rigid motions counted, m_⊥ assumed), the frozen table (A2u sign), the index count
  (rigid modes added), Paper 2's index formula, the conjugate count, the D3d sign, and each validator check.
- Full suite: 469 collected, 469 passed (with the Paper 2 archive present; without it 3 archive cross-checks skip).

### 13.11 Claim boundary

- Proposition B3 and Corollary B3′ only, with the status **PROVED (computer-assisted; not independently audited when written; see §15)**.
  Every proof dependency is VERIFIED-EXACT, CERTIFIED (Lemma K, independently audited), FROZEN INPUT (Paper 2,
  corollary only), STANDARD, or Proposition B2, which is PROVED (computer-assisted).
- Local statements for fixed q, small μ > 0, near y*. No explicit radius; no interval certificate in B2.5.
- **Not claimed:** stability of the D2h branch in any sense (it has index 1 on the centre manifold and index 4 on the
  slice); full-space dynamics; global continuation; secondary bifurcations (C2h or other); anything about A3.
- The D3d paragraph is a consistency check, not a theorem.
- Not independently audited when written (audited since; see §15). Not frozen, not published, nothing pushed or uploaded.

## 14. Next steps (proposed, not started)

- **Track A is complete** (§3.7–3.10).
- **B1 is complete:** Lemma K and Proposition B1 are CERTIFIED · INDEPENDENTLY AUDITED · ERRATUM CLOSED (§5, §10,
  §11).
- **B2:** B2.0–B2.2 passed the review gate. B2.3 (Lemma Q, CERTIFIED), B2.4 (Proposition B2) and B2.5
  (Proposition B3, Corollary B3′) are done. The author designates B2.3 and B2.4 as independently audited; the reports
  are not in this package, so they should be added (byte-identical, with hashes) before the labels of §9 and §12 are
  changed. Proposed next:
  - an independent audit of B2.5, with the dependency graph of §13.9 as its checklist;
  - release preparation for Paper 3, as a separate gate (B2.5 is the last new mathematics planned for Paper 3).
- **A3:** the global T_d branch (unchanged proposal). Not started.

## 15. Release candidate V1.0.0-rc1 — status at RC1 (historical; superseded as current status by §16)

*Historical record of V1.0.0-rc1. The statuses below are unchanged in RC2; the RC1 status line and the open author items at the end of this section are superseded by §16.*

**Status: RELEASE CANDIDATE / V1.0.0-rc1 · PENDING FINAL BLIND RELEASE AUDIT.** FREEZE = NO · GitHub = HOLD ·
Zenodo = HOLD · Springer submission = HOLD · no v1.0.0 tag. The only permitted next step is the final blind release
audit (`FINAL_AUDIT_INSTRUCTIONS.md`).

**What changed against V0.4-dev.6.** Documentation, author metadata, audit-status records, version metadata, the
manuscript and its figures, release metadata, the three new audit reports (byte-identical) and the integrity
manifest. No mathematical source, certificate, proof record, dependency graph or numerical record changed; this is
checked by `scripts/check_preservation_V1_0_0_rc1.py` (report: `docs/V1.0.0-rc1_PRESERVATION_CHECK.md`).

**Current statuses** (machine-readable: `docs/AUDIT_STATUS_MATRIX.json`):

| result | status | independent audit (report in `audits/`) |
|---|---|---|
| Lemma M | CERTIFIED · INDEPENDENTLY AUDITED | `CUBE_BIFURCATIONS_REVIEWER_REPORT.md` |
| Corollary M | PROVED (computer-assisted) · INDEPENDENTLY AUDITED | `CUBE_BIFURCATIONS_REVIEWER_REPORT.md` |
| Theorem A | PROVED (computer-assisted) · INDEPENDENTLY AUDITED | `CUBE_BIFURCATIONS_REVIEWER_REPORT.md` |
| Lemma K | CERTIFIED · INDEPENDENTLY AUDITED · ERRATUM CLOSED | `CUBE_BIFURCATIONS_V03_REVIEWER_REPORT.md`; erratum E-B1: `CUBE_BIFURCATIONS_V04_DEV4_B1_ERRATUM_REAUDIT.md` |
| Proposition B1 | CERTIFIED (computer-assisted) · INDEPENDENTLY AUDITED · ERRATUM CLOSED | as Lemma K |
| Lemma Q | CERTIFIED · INDEPENDENTLY AUDITED | `CUBE_BIFURCATIONS_V05_BLIND_B23_LEMMA_Q_REVIEWER_REPORT.md` |
| Proposition B2 | PROVED (computer-assisted) · INDEPENDENTLY AUDITED | `CUBE_BIFURCATIONS_V05_BLIND_B24_REVIEWER_REPORT.md` |
| Proposition B3 | PROVED (computer-assisted) · INDEPENDENTLY AUDITED | `CUBE_BIFURCATIONS_V04_DEV6_BLIND_B25_REVIEWER_REPORT.md` |
| Corollary B3′ | PROVED (computer-assisted) · INDEPENDENTLY AUDITED | `CUBE_BIFURCATIONS_V04_DEV6_BLIND_B25_REVIEWER_REPORT.md` |

The three new reports have SHA-256 `841152f2cccd0a43c4f8e73ce5d0cf37e9793d26f12047d5143ea5a053e96bcf` (B2.3),
`0302930b9a96ac6bca3df4e720ba34ab5937f73944aee76ba85f345706bdb1ec` (B2.4) and
`bffd4948721ee62f6898336734670ee51381caf546cdd69e0a2ad810e37f165a` (B2.5); each formal verdict is PASS with no finding
requiring correction. With them, the NOT_PROVIDED note of §13 and the open item of §14 are resolved.

**Audited inertia of the D2h branch points** (ordering: negative / zero / positive), for fixed 0 < q < q_c and
sufficiently small μ = p − P_T(q) > 0:
- centre (three-dimensional T2g reduced Hessian): (1, 0, 2) — centre Morse index 1, centre nullity 0;
- slice (rigid motions removed): (4, 0, 14) — slice Morse index 4, slice nullity 0;
- R²⁴: (4, 6, 14) — the six raw zero modes are the rigid translations and rotations, never counted in a Morse index.

None of these statements implies stability; the branch points are saddles.

**B1 certificates.** The historical, audited Lemma K certificate (semantic SHA-256
`616817fcc70e0fab7f106404e5e5332b17b9c4480bd440355f1ac5257a8518c6`) remains the certificate of record. The corrected
rebuild of erratum E-B1 (semantic SHA-256 `b2f8e6dcd1c5073635babea2f7a6079b7ede03acbbc4f33ac3cb20f64d21d505`) is
corroboration only and does not replace it.

**Historical status strings.** Proof records in `data/` (for example the `status` fields of
`data/B2_4_dependency_graph.json` and `data/B2_5_dependency_graph.json`) and the status constants in
`src/cube_bif/b2_branch.py` and `src/cube_bif/b2_index.py` keep the wording they had when they were generated
("not independently audited"). They are byte-identical by design: they are the exact artefacts the independent
auditors examined, and changing them would change audited source and records. In this file the labels of §9, §12 and
§13 were updated in V1.0.0-rc1. The table above and `docs/AUDIT_STATUS_MATRIX.json` are the current statuses.

**Open human-author items (release/submission blockers, not invented here):** Mihail Mladenski's exact
author-contribution statement (blocks journal submission); Mihail Mladenski's ORCID and e-mail, if the journal requires
them; the official institutional city of EITNetworks LLC, if required; final competing-interests wording approved by
both authors. See `docs/AUTHOR_CONTRIBUTIONS_REVIEW_REQUIRED.md` and `RELEASE_NOTES_RC1.md`.

## 16. Release candidate V1.0.0-rc2 — status at RC2 (historical; superseded as current status by §17)

**Status: RELEASE CANDIDATE / V1.0.0-rc2 · PENDING FINAL BLIND RELEASE AUDIT.** FREEZE = NO · GitHub = HOLD ·
Zenodo = HOLD · Springer submission = HOLD · v1.0.0 tag = NOT CREATED. The only permitted next step is the final blind
release audit (`FINAL_AUDIT_INSTRUCTIONS.md`), to be performed by an independent auditor.

**Why RC2.** Author and institution metadata were supplied after RC1. RC2 records them and does nothing else of
substance; RC1 (archive SHA-256 `33095d35107578054c7e54ff62be8a318ab973d7153e5c30d89da2fc9bc0361b`) is kept unchanged.

**What changed against RC1.** Author and institution metadata (both authors: EITNetworks LLC, Tobyhanna, Pennsylvania,
USA; Mihail Mladenski's e-mail; no ORCID for Mihail Mladenski); declarations (competing interests, author
contributions); version/status metadata (1.0.0rc2); documentation and status surfaces; bibliography metadata (two
Crossref-confirmed DOIs); release tooling, tests of release metadata, checksums and packaging. No mathematical source,
certificate, proof record, dependency graph, numerical record or audit report changed; this is checked against
V0.4-dev.6 by `scripts/check_preservation_V1_0_0_rc2.py` (`docs/V1.0.0-rc2_PRESERVATION_CHECK.md`).

**Statuses (unchanged from §15).** Lemma M: CERTIFIED · INDEPENDENTLY AUDITED.
Track A (Corollary M, Theorem A): PROVED (computer-assisted) · INDEPENDENTLY AUDITED.
B1 (Lemma K, Proposition B1): INDEPENDENTLY AUDITED · ERRATUM CLOSED. Lemma Q: CERTIFIED · INDEPENDENTLY AUDITED.
Proposition B2, Proposition B3, Corollary B3′: PROVED (computer-assisted) · INDEPENDENTLY AUDITED.
D2h branch inertia (negative / zero / positive): centre (1, 0, 2), slice (4, 0, 14), R²⁴ (4, 6, 14). None of these
statements implies stability; the D2h branch points are saddles. The Morse index of the D3d branch and the full Morse
index of the A2u/Td branch are not results of Paper 3.

**Authors.** Toni Mladenovski (corresponding author; info@eitnetworks.org; ORCID 0009-0009-8343-662X) and Mihail
Mladenski (mmladenski077@gmail.com; no ORCID), both EITNetworks LLC, Tobyhanna, Pennsylvania, USA. No educational
institution is listed.

**Open human-author items (not mathematical defects):** FINAL AUTHOR CONTRIBUTION APPROVAL REQUIRED BEFORE SPRINGER
SUBMISSION (Mihail Mladenski's detailed contribution statement; `AUTHORSHIP_FINAL_APPROVAL_REQUIRED.md`); competing-
interests wording — FINAL AUTHOR APPROVAL REQUIRED BEFORE SPRINGER SUBMISSION; copyright-holder wording in `LICENSE`
and `LICENSE-DOCS` — FINAL AUTHOR APPROVAL REQUIRED BEFORE FINAL RELEASE.

## 17. Release V1.0.0 — current status (final release prepared; no new mathematics)

**Status at build time: FINAL RELEASE PREPARED / V1.0.0 · PENDING RC2→V1.0.0 DELTA AUDIT.** FINAL BLIND RELEASE AUDIT (of V1.0.0-rc2): **RELEASE-READY**
(`audits/PAPER3_RC2_FINAL_BLIND_RELEASE_AUDIT.md`, SHA-256 `37b0b4d68f4675b4546f7313aca6937c51cdf1ee11d1cc20b528918e636d7448`; no blocking finding; a
computational release verification, not journal peer review). HUMAN APPROVALS: CLOSED (author decision,
`AUTHOR_DECISION_V1.0.0.md`). PUBLIC RELEASE: NOT YET EXECUTED. FREEZE = NO (pending the delta audit) · GitHub = HOLD · Zenodo publish = HOLD · Springer/JMC submission = HOLD · v1.0.0 public tag = NOT CREATED. The next step is the independent
RC2 → V1.0.0 delta/preservation audit (`FINAL_V1_DELTA_AUDIT_INSTRUCTIONS.md`).

**What changed against RC2** (archive SHA-256 `6dee0be5f975d23fce3a36770ddebad8041aae9e3f302df0cd923fad91481a08`, kept unchanged). The authors approved
the final author-contribution, competing-interests and copyright-holder texts; they are inserted verbatim in the
manuscript, `submission/DECLARATIONS.md`, `LICENSE`, `LICENSE-DOCS`, `CITATION.cff` and `.zenodo.json`, and every
temporary approval flag is removed from the current surfaces (the RC2 audit's non-blocking item NB-03 is closed by
this author decision). Version/status metadata: `1.0.0`; manuscript PDF Title and Author properties populated (NB-04);
the final blind release audit report archived verbatim; audit index and status matrix updated; release notes, release
tooling, tests of release metadata, checksums and packaging. No mathematical source, certificate, proof record,
dependency graph, numerical record or earlier audit report changed; this is checked against V0.4-dev.6 and RC2 by
`scripts/check_preservation_V1_0_0.py` (`docs/V1.0.0_PRESERVATION_CHECK.md`).

**Statuses (unchanged from §15 and §16).** Lemma M: CERTIFIED · INDEPENDENTLY AUDITED.
Track A (Corollary M, Theorem A): PROVED (computer-assisted) · INDEPENDENTLY AUDITED.
B1 (Lemma K, Proposition B1): INDEPENDENTLY AUDITED · ERRATUM CLOSED. Lemma Q: CERTIFIED · INDEPENDENTLY AUDITED.
Proposition B2, Proposition B3, Corollary B3′: PROVED (computer-assisted) · INDEPENDENTLY AUDITED.
D2h branch inertia (negative / zero / positive): centre (1, 0, 2), slice (4, 0, 14), R²⁴ (4, 6, 14). None of these
statements implies stability; the D2h branch points are saddles. The Morse index of the D3d branch and the full Morse
index of the A2u/Td branch are not results of Paper 3.

**Authors.** Toni Mladenovski (Founder; corresponding author; info@eitnetworks.org; ORCID 0009-0009-8343-662X) and
Mihail Mladenski (mmladenski077@gmail.com; no ORCID), both EITNetworks LLC, Tobyhanna, Pennsylvania, USA.
No educational institution is listed. Mihail Mladenski's EITNetworks LLC affiliation is a scientific affiliation; no
corporate role is stated for him (author correction recorded in `AUTHOR_DECISION_V1.0.0.md`; the "Co-founder" label
of RC2 is withdrawn).

**Public identifiers.** No GitHub release URL, Zenodo DOI or arXiv identifier exists yet; none is invented. The
manuscript and metadata carry the controlled placeholders `[PAPER 3 GITHUB RELEASE — TO BE ASSIGNED AT PUBLIC RELEASE]` and `[PAPER 3 ZENODO DOI — TO BE ASSIGNED AT PUBLIC RELEASE]`.
