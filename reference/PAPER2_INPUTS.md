# Frozen Paper 2 inputs (read-only)

Paper 3 uses Paper 2 only as input. It never edits Paper 2's files, repository, release or Zenodo record.

- Archive: `EIT_LJ_FULL_VECTOR_STABILITY_V1.0.zip`, SHA-256
  `bb70721df7f0aa17edca30d84d1b4aaf980c0a76693be14fa780e4ab8f64762d`
- Zenodo: version DOI 10.5281/zenodo.24187155, concept DOI 10.5281/zenodo.24187154
- GitHub: release v1.0.0 of eit-orbitos/EIT_LJ_FULL_VECTOR_STABILITY
- Mathematics frozen at V0.2-dev.10 (archive SHA-256 3c2316c66a6bb75043503ebb0d76101b2f647666642880642518ae0f7faca40b).

`src/cube_bif/paper2_ref.py` imports Paper 2's `analysis/` modules from this archive after checking its SHA-256. The
archive is looked up through `EIT_LJ_PAPER2_ARCHIVE`, the directory next to this project, or `reference/`. Tests that
need the archive are skipped when it is absent; the frozen constants are compared in any case.

| input | where in Paper 2 | used for |
|---|---|---|
| Convention: labels, y*_s = s/2, (D(R)x)_{Rs} = R x_s | geometry.py, cube_oh_decomposition.py | all phases |
| Γ₂₄ blocks: A2u = 4α₂ + 4β₁, A1g = 2α₁ + 4α₂ + 2α₃ | data/cube_oh_blocks.json | cross-check of V_aa, V_bb |
| h_A = (2(r+1)x − 4)/(1 + x + y/3), λ_A2u = e^(−q−2) qW_q[h_A(p) − h_A(q)] | NOTES Lemma A | A2u curve, transversality |
| r* = 1.4749107381472217442 (unique maximum of h_A) | Lemma A | domain 0 < q < r* |
| P_A(q): unique p > r* with h_A(p) = h_A(q); P_A(0⁺) = 3.1054933552830915550 | Lemma A | curve points |
| Theorem 4′: extra zero modes exactly on the two curves; the curves never meet | NOTES §8 | one-dimensional kernel on the A2u curve |
| Proposition A: V_* = −KΦ^{1/(p−q)} | NOTES §2 | scale elimination |
| Lemma T0: T2g block K; K = e^(−q−2) qW_q[M(p) − M(q)] | analysis/t2g_block.py | Phase B0 |
| P_T(q), q_c = 2.0199382317007999883 | Lemma T3, Lemma T2 | T2g curve points |
| Lemma S: A1g, Eg, T1u (internal), T2u strictly stable for all p > q > 0; blocks A1g = 2α₁ + 4α₂ + 2α₃, Eg = 2α₁ + α₂ + 3β₂ + 2β₃; h_L(r) = Σ_k((r+1)ℓ_k − m_k)g_r(k)/W_r with h_L′ > 0 | NOTES §6 (Lemma S) | B2.1: h_A, h_E > 0, the denominators of the back-reaction |
| Lemma T1: tr K > 0 for all p > q > 0 (the upper T2g eigenvalue) | NOTES §6 (Lemma T1) | B1.8 transversality; B2.1: one-dimensional kernel on Fix(D2h) |
| P_T(0⁺) certified enclosure [4.796368189344416004181122459356, …357]; the tighter MPFR enclosure of Paper 2's blind audit | Lemma T3 (manuscript §5); audits/theorem4prime_v0.1/REVIEWER_REPORT.md | B1.4; B2.2 endpoint q = 0 (P_T(0) refined inside both) |
| q_c certified enclosure [2.0199382317007999883028831854985758749007, …9008] | Lemma T2 (manuscript §5) | B1.7 corner; B2.2 corner (q_c refined inside it) |
| Lemma T3: exactly one p = P_T(q) > q with D(p, q) = 0, for 0 ≤ q < q_c | Lemma T3 (manuscript §5) | B2.3: the corollary of Lemma Q (P_T(q) − q > 0); the P_T(0) and q_c enclosures enter through B1's certificate |
