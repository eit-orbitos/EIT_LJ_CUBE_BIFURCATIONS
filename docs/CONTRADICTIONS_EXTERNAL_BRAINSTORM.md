# Contradictions with the external brainstorm (Google), as relayed on 2026-11-13

**Source.** The brainstorm itself was not available to this project. Its content is known only through the review
the author relayed on 2026-11-13. That review said which ideas to keep, which to drop, and what the Paper 3 plan
should be. Each item below is checked against this project's exact or numerical results. Nothing from the
brainstorm was used as input.

| # | Brainstorm claim (as relayed) | Result here | Status |
|---|---|---|---|
| C1 | r* ≈ 2.66 | **Contradicted.** r* = 1.4749107381472217442484782… is the unique critical point of h_A. It was recomputed independently and agrees with frozen Paper 2 (Lemma A) to 4.9·10⁻²⁰. h_A′ < 0 on (r*, ∞), so nothing happens at 2.66. The value 2.66 does lie in the range (r*, 3.1055) of P_A (P_A(q) = 2.66 near q ≈ 0.37), but it is not r*. Where 2.66 came from was not found. | VERIFIED-NUMERIC (and FROZEN INPUT) |
| C2 | Test P_A at q = 2.0 | **Invalid point.** P_A exists only for 0 < q < r* ≈ 1.4749. For q ≥ r*, the A2u mode is unstable for every p > q (Paper 2 Lemma A). q = 2.0 is close to the T2g corner q_c = 2.0199…, so the A2u and T2g curves may have been confused. | FROZEN INPUT |
| C3 | Quadratic back-reaction of a² into E_g, T2g, … | **Contradicted.** A2u ⊗ A2u = A1g. b = D³V[e_A, e_A, ·] is O_h-invariant, hence lies in Fix(O_h) = span{e_br} (one-dimensional). All 24 components were checked exactly, for every pair potential. | VERIFIED-EXACT |
| C4 | Explicit f(r), equation for P_A, coordinate a, and formulas for U_{r,aa}, V_aab, V_bb, c4_eff | **Not used.** They cannot describe the audited A2u problem, since they give r* ≈ 2.66 (C1). This project's formulas come from the exact eigenvector E_A(s) = (s₁s₂s₃)s (NOTES §3.1–3.4). | — |
| C5 | All D3d and D2h branches are transcritical | **Contradicted for D2h.** The normaliser of the D2h isotropy (D4h) contains elements acting by −1 on its fixed line, so the reduced equation there is odd: pitchfork-type. For D3d the normaliser acts trivially and I₃ = a₁a₂a₃ ≠ 0 on the axis, so the branch is transcritical-type provided κ ≠ 0. κ is not yet computed (Phase B1). **Update V0.3-dev:** κ ≠ 0 on the whole T2g curve is certified (NOTES §5.7), and the D3d branches are transcritical by the implicit function theorem (NOTES §5.9). | VERIFIED-EXACT (ingredients); generic type STANDARD; D3d CERTIFIED |
| C6 | "Ihrig's theorem implies transcritical" | **Misattribution.** The theorem (Ihrig & Golubitsky 1984; extended by Chossat, Lauterbach & Melbourne) says that, generically, nonzero quadratic equivariants make the branches unstable near the bifurcation. It is about stability, not about branch type. Correct statement: NOTES §4. | STANDARD |
| C7 | Isotropy labels assumed in advance (D3d, D2h, C2h) | Computed from the stabilisers instead. D3d and D2h are axial. **C2h (direction (1,1,0)) has a two-dimensional fixed space, so it is not axial** and the Equivariant Branching Lemma gives no branch for it. | VERIFIED-EXACT |

**What the relayed review got right**, and this project confirms:
- the A2u stabiliser is T_d (computed, not assumed);
- evenness of the reduced A2u potential (c₃ = 0);
- the scalar A1g reduction c₄ = V_aaaa − 3V_aab²/V_bb;
- the T2g cubic invariant a₁a₂a₃ (invariant under all 48 matrices);
- I₃ vanishes on the coordinate axes but not on the diagonals.

## Google note on Phase B1 (relayed by the author, 2026-11-13)

The note was relayed together with the B1 request. The B1 work followed the request, not the note. Each claim is
checked below.

| # | Claim in the note | Result here | Status |
|---|---|---|---|
| G1 | T2g is even under inversion (gerade), which allows the cubic invariant I₃ = a₁a₂a₃ | **Confirmed.** T(R) = σ(R)R has kernel {E, i}. I₃ is invariant under all 48 matrices (B0). The raw 24-D cubic restriction to the critical space is exactly 6κ·a₁a₂a₃ (NOTES §5.1). | VERIFIED-EXACT |
| G2 | Near q_c all derivatives of V carry the factor (p − q); extract the positive factor and work with a nonsingular carrier on (0, q_c] | **Confirmed, with the order derived rather than assumed.** Every coefficient is a difference form qW_q[g(p) − g(q)], so κ = qW_q(p − q)κ̂. κ̂ is nonzero at both ends, so there is exactly one factor q and one factor p − q (NOTES §5.2, §5.4). | VERIFIED-EXACT, CERTIFIED |
| G3 | Build the Arb certificate for κ(q) ≠ 0 on the whole interval (0, q_c] | **Not as stated.** Raw κ is zero at q_c (and tends to 0 as q → 0⁺). The certificate is for the normalised carrier κ̂ on the closed curve, which gives κ ≠ 0 on the physical range 0 < q < q_c. The control "raw κ on the corner box" fails as it must. | CERTIFIED |
| G4 | By Ihrig's theorem the four D3d branches are transcritical and linearly unstable on both sides; they change Morse index | **Misattribution (as C6).** Here the transcritical type comes from the scalar reduced equation on the D3d axis, by the implicit function theorem, using κ ≠ 0 and τ ≠ 0 (NOTES §5.9). Ihrig–Golubitsky is a stability statement. No stability and no Morse-index change is claimed in B1; that belongs to B2. | STANDARD; not used |
| G5 | On the D2h axes I₃ = 0, so the branch is a pitchfork governed by the quartic coefficient, and it connects directly to Paper 2's global cuboid family | **Partly confirmed.** I₃ = 0 on (1, 0, 0), and the reduced equation there is odd (B0; NOTES §5.10). The quartic coefficient is B2. The geometry of the D2h configurations has not been derived, so calling them cuboids, or linking them to Paper 2's cuboid family, is not supported yet. | VERIFIED-EXACT (parity); rest open |

## Google claims relayed with the B2 plan (2026-11-13)

The author's review gate relayed the B2 plan together with two items from a Google note. The note itself was not
available to this project. The B2 work followed the plan, not the note.

| # | Claim (as relayed) | Result here | Status |
|---|---|---|---|
| G6 | Fix_{R²⁴}(D2h) = span{e_crit, A1g, Eg⁽¹⁾, Eg⁽²⁾} | **Contradicted.** The projector onto the fixed space of the stabiliser of e₁ has rank 4 = A1g (1) + Eg (1) + T2g (2, one direction per copy). The second Eg direction is not fixed: the projector maps it to 0. f₁ = −n_v uh₁ + n_u vh₁, the second T2g direction, is fixed but missing from the claim. The claimed span meets the fixed space in three dimensions only. This is the point the review gate flagged (two T2g copies). b = D³V[e₁, e₁, ·] nevertheless has no f₁ component, exactly; the reason is Schur's lemma on Sym²(T2g) (NOTES §6.1), not the claimed fixed space. | VERIFIED-EXACT |
| G5, update | (from the B1 note) the D2h branches connect directly to Paper 2's global cuboid family | **Contradicted near the cube.** e₁ is orthogonal to Fix(Z₂³), the cuboid family A1g ⊕ Eg, and Fix(D2h) ∩ Fix(Z₂³) = span{Â, Ê}. A D2h-symmetric configuration near the cube with a nonzero e₁-component is therefore not a cuboid; to first order its cross-sections are rhombi (NOTES §6.1). Whether a D2h branch reaches the cuboid family far from the cube was not studied. | VERIFIED-EXACT |

The relayed plan also mentions a Google parametrisation (u_x, u_y, u_z, α) as a possible cross-check. It was not
available here. Route 3 of B2.1 uses its own parametrisation of the same four-dimensional fixed space, built from the
vertex orbits of the stabiliser (NOTES §6.1–6.2).
