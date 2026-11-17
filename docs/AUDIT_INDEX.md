# Audit index — V1.0.0

Every independent audit report in `audits/`, byte-identical to the copy received. Reports are records, not instructions; they are not relicensed.

| report | scope | audited package (SHA-256) | verdict | report SHA-256 |
|---|---|---|---|---|
| `CUBE_BIFURCATIONS_REVIEWER_REPORT.md` | Track A (Lemma M, Corollary M, Theorem A) | V0.2-dev (`ba835b0d…1e30`) | PASS WITH MINOR DOCUMENTATION CORRECTIONS (applied in V0.2.1-dev) | `f82c5ef1a03c33c0909313bd6442d1879d39717f991cc8e245eb0c61f75d8b85` |
| `CUBE_BIFURCATIONS_V03_REVIEWER_REPORT.md` | V0.2.1-dev correction chain and Phase B1 (Lemma K, Proposition B1) | V0.2.1-dev (`3bd6ac42…9f55`), V0.3-dev (`3901c0db…28fe`) | PASS | `82bd4f21630a20481113702a9f49dddfa6327f2baf3c07a131af259c1baa65e5` |
| `CUBE_BIFURCATIONS_V04_DEV4_B1_ERRATUM_REAUDIT.md` | targeted re-audit of erratum E-B1 | V0.4-dev.4 (`8ae923be…06c7`), pre-patch V0.4-dev.3 (`cf331557…5c81`) | PASS; erratum CLOSED | `ba482da06aa0492b6524e47680fd949170f4d0dafac0d5661a073efce4d46b74` |
| `CUBE_BIFURCATIONS_V05_BLIND_B23_LEMMA_Q_REVIEWER_REPORT.md` | B2.3 / Lemma Q | V0.4-dev.5 (`77267d56…3949`) | PASS | `841152f2cccd0a43c4f8e73ce5d0cf37e9793d26f12047d5143ea5a053e96bcf` |
| `CUBE_BIFURCATIONS_V05_BLIND_B24_REVIEWER_REPORT.md` | B2.4 / Proposition B2 | V0.4-dev.5 (`77267d56…3949`) | PASS | `0302930b9a96ac6bca3df4e720ba34ab5937f73944aee76ba85f345706bdb1ec` |
| `CUBE_BIFURCATIONS_V04_DEV6_BLIND_B25_REVIEWER_REPORT.md` | B2.5 / Proposition B3, Corollary B3′ | V0.4-dev.6 (`c473af60…b691`) | PASS | `bffd4948721ee62f6898336734670ee51381caf546cdd69e0a2ad810e37f165a` |
| `PAPER3_RC2_FINAL_BLIND_RELEASE_AUDIT.md` | final blind release audit of the release candidate | V1.0.0-rc2 (`6dee0be5…1a08`) | RELEASE-READY (no blocking finding) | `37b0b4d68f4675b4546f7313aca6937c51cdf1ee11d1cc20b528918e636d7448` |

Details of each report and what was copied: `audits/README.md`. Current statuses: `docs/AUDIT_STATUS_MATRIX.md`.

V1.0.0 adds one report: the final blind release audit of V1.0.0-rc2 (verdict RELEASE-READY), performed under
`FINAL_AUDIT_INSTRUCTIONS.md` (historical RC2 record). The next audit is the RC2 → V1.0.0 delta/preservation audit
(`FINAL_V1_DELTA_AUDIT_INSTRUCTIONS.md`); it has not been performed. Public release: not yet executed.
