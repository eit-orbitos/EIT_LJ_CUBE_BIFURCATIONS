# Theorem and result dependency summary — V1.0.0

(V1.0.0 changes only this title line and this note; the evidence-class legend below was added in RC2; the proof
dependencies are those of V0.4-dev.6 and are unchanged.)

Machine-readable graphs (byte-identical with V0.4-dev.6, validated by the tests): `data/A2_theorem_A_dependencies.json`
(Theorem A), `data/B2_4_dependency_graph.json` (Proposition B2), `data/B2_5_dependency_graph.json` (Proposition B3,
Corollary B3′). Node `status` strings inside these graphs are historical; current statuses: `docs/AUDIT_STATUS_MATRIX.json`.

Leaf classes: VERIFIED-EXACT (exact symbolic, tested), CERTIFIED (Arb ball-arithmetic certificate with an independent
checker), FROZEN INPUT (a named result of frozen Paper 2, DOI 10.5281/zenodo.24187155), STANDARD (a textbook theorem).
Evidence classes kept separate throughout: exact symbolic result (VERIFIED-EXACT); standard theorem (STANDARD);
frozen Paper 2 input (FROZEN INPUT); certified interval result (CERTIFIED); numerical corroboration (VERIFIED-NUMERIC,
never a proof leaf); independent audit (recorded per result in `docs/AUDIT_STATUS_MATRIX.json`, not a proof step).
**No numerical scan, branch location or numerical Hessian is a proof dependency** of any result below; numerical work
is recorded as corroboration only.

```
Lemma M (CERTIFIED) ──┐
Paper 2 Lemma A (FROZEN) ─┴─> Corollary M: c4 > 0 on the A2u curve
A0 exact A2u representation, T_d stabiliser, evenness (EXACT) ─┐
Paper 2 Thm 4', Lemma A, Prop. A: kernel, transversality (FROZEN) ─┤
Corollary M ───────────────────────────────────────────────────┼─> Theorem A: A2u Z2 pitchfork, branch side p > P_A(q)
Lyapunov–Schmidt, implicit function theorem (STANDARD) ────────┘

B1 exact trilinear structure, I3 = a1 a2 a3, kappa = q W_q (p-q) kappa_hat (EXACT) ─┐
Lemma K certificate, historical semantic 616817fc… (CERTIFIED; erratum E-B1 closed) ─┼─> Lemma K: kappa != 0, 0 < q < q_c
Paper 2 Lemmas T2/T3, P_T(0) enclosure (FROZEN) ──────────────────────────────────┘
Lemma K + tau < 0 (B1.8: Paper 2 Lemmas T1, T3 + exact identity) + B0 D3d isotropy
  + Lyapunov–Schmidt + implicit function theorem ─> Proposition B1: D3d transcritical branches (not via Ihrig's theorem)

B2.1 exact identity c4 = D4V[e1^4] - 3 b_A^2/h_A - 3 b_E^2/h_E = q W_q (p-q) c4_hat (EXACT) ─┐
Lemma Q certificate, semantic f7bc244e… (CERTIFIED), imported B1 curve balls ─────────────┼─> Lemma Q: c4 > 0, 0 < q < q_c
Paper 2 Lemmas T3, S (FROZEN) ─────────────────────────────────────────────────────────┘
B2.0 parity/fixed space (EXACT) + B2.1 (EXACT) + Lemma Q + tau < 0 (B1.8)
  + Lyapunov–Schmidt + implicit function theorem ─> Proposition B2: D2h Z2 pitchfork, mu > 0, s*^2 = -(6 tau/c4) mu + O(mu^2)

exact O_h/T2g invariant structure (EXACT) + Lemma K (kappa != 0) + Proposition B2
  + Lyapunov–Schmidt / centre-manifold theory (STANDARD) [+ exact Hessian expansion with remainder bound, EXACT]
  ─> Proposition B3: centre inertia (1, 0, 2)
Proposition B3 + Paper 2 Theorem (index) block signs on p = P_T(q) (FROZEN: inertia(H_WW) = (3, 0, 12), Eu x2, A2u x1)
  + Haynsworth inertia additivity (STANDARD) ─> Corollary B3′: slice inertia (4, 0, 14); R^24 inertia (4, 6, 14)
```

The D3d consistency check of B2.5 and all numerical corroboration are marked `consistency_only` /
`corroboration_only` in the graphs and are not edges into any proposition.
