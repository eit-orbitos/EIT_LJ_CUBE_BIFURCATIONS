# Audit status matrix — V1.0.0

Status at build time: **FINAL RELEASE PREPARED / V1.0.0 · PENDING RC2→V1.0.0 DELTA AUDIT**. FINAL BLIND RELEASE AUDIT: RELEASE-READY (of V1.0.0-rc2;
`PAPER3_RC2_FINAL_BLIND_RELEASE_AUDIT.md`). PUBLIC RELEASE: NOT YET EXECUTED. Human approvals: CLOSED. RC2 → V1.0.0
delta audit: PENDING. FREEZE = NO (pending the delta audit) · GitHub = HOLD · Zenodo publish = HOLD · Springer/JMC submission = HOLD · v1.0.0 public tag = NOT CREATED. Machine-readable: `docs/AUDIT_STATUS_MATRIX.json`.

| result | phase | status | independent audit | report(s) in `audits/` (SHA-256) | computer-assisted | erratum | erratum closed |
|---|---|---|---|---|---|---|---|
| Lemma M | A2 | CERTIFIED | INDEPENDENTLY AUDITED | `CUBE_BIFURCATIONS_REVIEWER_REPORT.md` (`f82c5ef1…8b85`) | yes | none | — |
| Corollary M | A2 | PROVED (computer-assisted) | INDEPENDENTLY AUDITED | `CUBE_BIFURCATIONS_REVIEWER_REPORT.md` (`f82c5ef1…8b85`) | yes | none | — |
| Theorem A | A2 | PROVED (computer-assisted) | INDEPENDENTLY AUDITED | `CUBE_BIFURCATIONS_REVIEWER_REPORT.md` (`f82c5ef1…8b85`) | yes | none | — |
| Lemma K | B1 | CERTIFIED | INDEPENDENTLY AUDITED · ERRATUM CLOSED | `CUBE_BIFURCATIONS_V03_REVIEWER_REPORT.md` (`82bd4f21…65e5`)<br>`CUBE_BIFURCATIONS_V04_DEV4_B1_ERRATUM_REAUDIT.md` (`ba482da0…6b74`) | yes | E-B1 | yes |
| Proposition B1 | B1 | CERTIFIED (computer-assisted) | INDEPENDENTLY AUDITED · ERRATUM CLOSED | `CUBE_BIFURCATIONS_V03_REVIEWER_REPORT.md` (`82bd4f21…65e5`)<br>`CUBE_BIFURCATIONS_V04_DEV4_B1_ERRATUM_REAUDIT.md` (`ba482da0…6b74`) | yes | E-B1 | yes |
| Lemma Q | B2.3 | CERTIFIED | INDEPENDENTLY AUDITED | `CUBE_BIFURCATIONS_V05_BLIND_B23_LEMMA_Q_REVIEWER_REPORT.md` (`841152f2…6bcf`) | yes | none | — |
| Proposition B2 | B2.4 | PROVED (computer-assisted) | INDEPENDENTLY AUDITED | `CUBE_BIFURCATIONS_V05_BLIND_B24_REVIEWER_REPORT.md` (`0302930b…b1ec`) | yes | none | — |
| Proposition B3 | B2.5 | PROVED (computer-assisted) | INDEPENDENTLY AUDITED | `CUBE_BIFURCATIONS_V04_DEV6_BLIND_B25_REVIEWER_REPORT.md` (`bffd4948…165a`) | yes | none | — |
| Corollary B3′ | B2.5 | PROVED (computer-assisted) | INDEPENDENTLY AUDITED | `CUBE_BIFURCATIONS_V04_DEV6_BLIND_B25_REVIEWER_REPORT.md` (`bffd4948…165a`) | yes | none | — |

## Dependencies

- **Lemma M** (§3.7): Arb ball-arithmetic certificate data/A2_lemma_M_certificate.json (semantic 49dce160...); independent checker certcheck.py.
- **Corollary M** (§3.8): Lemma M; exact A1 identity c4 = (16/3) q W_q [m(P_A(q)) - m(q)]; FROZEN INPUT Paper 2 Lemma A.
- **Theorem A** (§3.9; data/A2_theorem_A_dependencies.json): A0 exact A2u representation (VERIFIED-EXACT); Corollary M; FROZEN INPUT Paper 2 Theorem 4', Lemma A, Prop. A (transversality, kernel); standard Lyapunov-Schmidt reduction; implicit function theorem.
- **Lemma K** (§5.7, §10, §11): exact B1 trilinear structure and factorisation kappa = q W_q (p - q) kappa_hat (VERIFIED-EXACT); historical Arb certificate data/B1_kappa_certificate.json (semantic 616817fc...); FROZEN INPUT Paper 2 Lemmas T2/T3 and P_T(0) enclosure.
- **Proposition B1** (§5.9): Lemma K; B1.8 transversality tau < 0 (FROZEN INPUT Paper 2 Lemmas T1, T3 plus exact identity); B0 exact T2g representation and D3d isotropy; standard Lyapunov-Schmidt reduction; implicit function theorem.
- **Lemma Q** (§9): exact B2.1 identity c4 = D4V[e1^4] - 3 b_A^2/h_A - 3 b_E^2/h_E = q W_q (p - q) c4_hat; Arb certificate data/B2_c4hat_certificate.json (semantic f7bc244e...); imported hash-pinned B1 curve balls (Lemma K certificate); FROZEN INPUT Paper 2 Lemma T3, Lemma S.
- **Proposition B2** (§12; data/B2_4_dependency_graph.json): B2.0 exact parity/fixed space; B2.1 exact LS coefficient identity; Lemma Q; B1.8 tau < 0 (audited); standard Lyapunov-Schmidt reduction; implicit function theorem.
- **Proposition B3** (§13; data/B2_5_dependency_graph.json): exact O_h/T2g invariant structure; Lemma K (kappa != 0, audited); Proposition B2 (audited); standard Lyapunov-Schmidt/centre-manifold theory; exact Hessian expansion with analytic remainder bound.
- **Corollary B3′** (§13.6): Proposition B3; FROZEN INPUT Paper 2 Theorem (index) block signs; Haynsworth inertia additivity (standard).

## Audited inertia of the D2h branch points

Ordering negative / zero / positive; fixed 0 < q < q_c, small μ = p − P_T(q) > 0.

| space | inertia | Morse index | nullity |
|---|---|---|---|
| centre (3-D T2g reduced Hessian) | (1, 0, 2) | 1 | 0 |
| slice (rigid motions removed) | (4, 0, 14) | 4 | 0 |
| R²⁴ (raw) | (4, 6, 14) | — (the six zeros are rigid motions, not counted) | — |

None of these statements implies stability. Full report hashes are in `docs/AUDIT_STATUS_MATRIX.json` and `docs/AUDIT_INDEX.md`. An independent AI audit is not a journal peer review.
