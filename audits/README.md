# External audits

Audit reports are kept byte-identical to the copies that were received. They are records, not instructions.

| report | auditor | audited package | received | verdict |
|---|---|---|---|---|
| `CUBE_BIFURCATIONS_REVIEWER_REPORT.md` | Kimi Agent (blind audit of Track A) | `EIT_LJ_CUBE_BIFURCATIONS_V0.2-dev.zip` | 2026-11-13 (the auditor dated the report 2026-11-14) | PASS WITH MINOR DOCUMENTATION CORRECTIONS |
| `CUBE_BIFURCATIONS_V03_REVIEWER_REPORT.md` | Kimi Agent (audit of the V0.2.1-dev correction chain and of Phase B1) | `EIT_LJ_CUBE_BIFURCATIONS_V0.2.1-dev.zip` and `EIT_LJ_CUBE_BIFURCATIONS_V0.3-dev.zip` | 2026-11-13 (the auditor dated the report 2026-11-14) | PASS, no mathematical, certificate or documentation correction required |
| `CUBE_BIFURCATIONS_V04_DEV4_B1_ERRATUM_REAUDIT.md` | Kimi Agent (targeted re-audit of erratum E-B1 only) | `EIT_LJ_CUBE_BIFURCATIONS_V0.4-dev.4.zip`, with `EIT_LJ_CUBE_BIFURCATIONS_V0.4-dev.3.zip` as the pre-patch package | 2026-11-14 | PASS; the erratum may be marked CLOSED; no further full B1 audit required |
| `CUBE_BIFURCATIONS_V05_BLIND_B23_LEMMA_Q_REVIEWER_REPORT.md` | blind independent reviewer (B2.3 / Lemma Q only; the report does not name the auditing system or a date) | `EIT_LJ_CUBE_BIFURCATIONS_V0.4-dev.5.zip` (named `…dev.5(2).zip` in the report) | 2026-11-15 (with V1.0.0-rc1) | PASS; no CRITICAL, MAJOR or MINOR finding; Lemma Q independently audited and re-certified |
| `CUBE_BIFURCATIONS_V05_BLIND_B24_REVIEWER_REPORT.md` | Kimi Agent (blind audit of B2.4 / Proposition B2 only), dated 2026-11-15 | `EIT_LJ_CUBE_BIFURCATIONS_V0.4-dev.5.zip` | 2026-11-15 (with V1.0.0-rc1) | PASS; findings requiring correction: none |
| `CUBE_BIFURCATIONS_V04_DEV6_BLIND_B25_REVIEWER_REPORT.md` | Kimi Agent (blind audit of B2.5 / Proposition B3 and Corollary B3′ only), dated 2026-11-15 | `EIT_LJ_CUBE_BIFURCATIONS_V0.4-dev.6.zip` | 2026-11-15 (with V1.0.0-rc1) | PASS; findings requiring correction: none |
| `PAPER3_RC2_FINAL_BLIND_RELEASE_AUDIT.md` | final blind release audit of the whole release candidate (supplied by the author as the Kimi audit; the report does not name the auditing system), dated 2026-11-16 | `EIT_LJ_CUBE_BIFURCATIONS_V1.0.0-rc2.zip` | 2026-11-16 (with V1.0.0) | RELEASE-READY; blocking findings: none |

## Track A report

- Report SHA-256: `f82c5ef1a03c33c0909313bd6442d1879d39717f991cc8e245eb0c61f75d8b85`.
- Audited package SHA-256: `ba835b0dee8cb6d80214b4bd9a61bf2a65d6a4d52376b4e7e0a3dcfd71691e30`. The report quotes
  this hash.
- Source archive: `Kimi_Agent_Blind_Theorem4_Proof_Audit_1.zip`, SHA-256
  `e2b2a144f83fd30031f2a84b58d956a14728e4b906bc0b787536bb2f41a172e8`. It also held two files that are not part of
  this project and are not copied here:
  - `REVIEWER_REPORT.md`, an earlier audit of the Paper 2 manuscript against its frozen repository;
  - an image.
- Summary and the corrections made: `NOTES.md` §3.10 and `CHANGELOG.md` (V0.2.1-dev).

## Phase B1 report

- Report SHA-256: `82bd4f21630a20481113702a9f49dddfa6327f2baf3c07a131af259c1baa65e5`.
- Audited packages, with the hashes the report quotes and that match the archives here:
  - V0.2.1-dev: `3bd6ac4200122610f6d4f6a6fd4b19b5ff43117398f5b324dabc59c92c2a9f55`;
  - V0.3-dev: `3901c0db5daf3d7862629bca61e5a49b7bd15faeedcf44fab007ada6ffc128fe`.
- Source archive: `Kimi_Agent_Blind_Theorem4_Proof_Audit_2.zip`, SHA-256
  `1058e2a12b545e7ca3208ba8d8c562f0712c047c10625cb64a5cba7a672333e0`. It also held three files:
  - the Track A report above, byte-identical to the copy already here;
  - the Paper 2 manuscript review and the image, which are not part of this project and are not copied.
- Summary: `NOTES.md` §5.11 and `CHANGELOG.md` (V0.3.1-dev).

## Erratum E-B1 re-audit (received with V0.4-dev.5)

- Report SHA-256: `ba482da06aa0492b6524e47680fd949170f4d0dafac0d5661a073efce4d46b74`.
- Audited packages, with the hashes the report quotes and that match the archives of this project:
  - V0.4-dev.4: `8ae923beec9c095ec546c1a69e56a632698bfd8e4828a1165a8cbc1199cc06c7`;
  - V0.4-dev.3 (pre-patch): `cf331557f9cf6fd074920368a69268c331e4c84d1f3b64fd89b421a3b45d5c81`. The report names the
    uploaded copy `EIT_LJ_CUBE_BIFURCATIONS_V0.4-dev.3 (1).zip`; the hash is the same.
- Source archive: `Kimi_Agent_Blind Theorem4 Proof Audit (4).zip`, SHA-256
  `8302bfcac97d78ea00228d19d5d5ddf87dff9edcd96bb72d84a4e40ddcf1fd54`. It also held five files:
  - the Track A report and the Phase B1 report above, byte-identical to the copies already here;
  - `CUBE_BIFURCATIONS_V03_BLIND_REVIEWER_REPORT.md` (SHA-256
    `49a73fa004d9d5b6d6a92e1771c7f63aef10d776b479976479584ba82a40a428`), a further blind audit of V0.3-dev Phase B1
    (verdict PASS). It was not part of the V0.4-dev.5 request and is not copied or relied on here;
  - the Paper 2 manuscript review and an image, which are not part of this project and are not copied.
- Summary and status change: `NOTES.md` §11 and `CHANGELOG.md` (V0.4-dev.5).

## B2.3, B2.4 and B2.5 reports (received with V1.0.0-rc1)

All three were supplied by the author, authenticated against the hashes he gave, and copied byte-identically.

- **B2.3 / Lemma Q** — `CUBE_BIFURCATIONS_V05_BLIND_B23_LEMMA_Q_REVIEWER_REPORT.md`, SHA-256
  `841152f2cccd0a43c4f8e73ce5d0cf37e9793d26f12047d5143ea5a053e96bcf`.
  - Audited package: V0.4-dev.5, SHA-256 `77267d56f7a271b81b6cc91166f6750c71e1fc4f214c337f016ecf75b4563949` (quoted in
    the report); Paper 2 `bb70721d…762d`.
  - Verdict PASS: independent raw-coordinate derivation, separate MPFR interval certification of all 222 boxes and both
    endpoints, independent strict Newton inclusion of the 222 imported B1 curve balls, 93 targeted tests, 9
    independent adversarial controls and the 24/24 mutation suite. Four INFORMATIONAL items, none requiring a
    correction (computer-assisted; the corner box also covers a short nonphysical mirror arc; B2.4 examined only as a
    consumer of Lemma Q; no numerical scan needed).
- **B2.4 / Proposition B2** — `CUBE_BIFURCATIONS_V05_BLIND_B24_REVIEWER_REPORT.md`, SHA-256
  `0302930b9a96ac6bca3df4e720ba34ab5937f73944aee76ba85f345706bdb1ec`.
  - Audited package: V0.4-dev.5 (`77267d56…3949`), with V0.4-dev.4 (`8ae923be…c7`) for the identity check.
  - Verdict PASS: derivation, branch side, Z₂ exchange, energy-reduced axial classification, axial curvature, exact
    D2h isotropy, non-cuboid status and geometry confirmed; 397 passed with the Paper 2 archive. Three INFORMATIONAL
    items (Lemma Q used as an input and not re-audited there; the two skips were environmental; numerical work is
    corroboration only).
- **B2.5 / Proposition B3 and Corollary B3′** — `CUBE_BIFURCATIONS_V04_DEV6_BLIND_B25_REVIEWER_REPORT.md`, SHA-256
  `bffd4948721ee62f6898336734670ee51381caf546cdd69e0a2ad810e37f165a`.
  - Audited package: V0.4-dev.6 (`c473af60…b691`), with V0.4-dev.5 for the identity check and the two reports above
    authenticated as inputs.
  - Verdict PASS: centre inertia (1, 0, 2), same index on all six conjugate branch points, m_⊥ = 3 from frozen Paper 2,
    slice inertia (4, 0, 14), raw R²⁴ inertia (4, 6, 14); no stability claim; the post-hoc numerical tolerance does not
    affect the proof. 469 passed; 28/28 mutations; 62/62 identity controls; 10/10 independent adversarial rejections.

## Final blind release audit of V1.0.0-rc2 (received with V1.0.0)

Supplied by the author, authenticated against the hash he gave, and copied byte-identically.

- `PAPER3_RC2_FINAL_BLIND_RELEASE_AUDIT.md`, SHA-256 `37b0b4d68f4675b4546f7313aca6937c51cdf1ee11d1cc20b528918e636d7448`.
- Audited artifacts (hashes quoted in the report): RC2 archive `6dee0be5…1a08` with sidecar `7f39b894…7ffea`, manuscript
  PDF `674509e9…f334`, source ZIP `5626fb5e…5164`, JMC package `d002d5e8…fd00`, corrected artifact manifest
  `f96a88d3…6628`; V0.4-dev.6 `c473af60…b691`, Paper 2 `bb70721d…762d`, RC1 `33095d35…361b`.
- Verdict **RELEASE-READY**: 7 PASS and 6 PASS_WITH_NOTES audit questions, no blocking finding; 479/479 tests, 130/130
  controls as required, certificates replayed with the expected semantic hashes, clean 30-page source build, 30
  references, 3 figures, 7 tables, byte-identical figure regeneration with matplotlib 3.11.2.
- Six non-blocking notes: NB-01 (stale external manifest `e276…`; use `f96a…`), NB-02 (permitted metadata-only
  `__init__.py` and insert-only `audits/README.md` changes), NB-03 (three human approvals open; closed in V1.0.0 by
  author decision, not by the report), NB-04 (blank PDF Title/Author properties; populated in V1.0.0), NB-05 (cosmetic
  TeX notices), NB-06 (figure bytes depend on the plotting-library version; use matplotlib 3.11.2).

An independent AI audit is not a journal peer review. Summary of current statuses: `docs/AUDIT_STATUS_MATRIX.md`.

