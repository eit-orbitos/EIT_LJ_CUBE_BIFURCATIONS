"""EIT-LJ Cube Bifurcations (Paper 3) — symmetry-breaking bifurcations from the cubic equilibrium in two-term
inverse-power clusters.

Authors: Toni Mladenovski and Mihail Mladenski (EITNetworks LLC, Tobyhanna, Pennsylvania, USA).

Status: FINAL RELEASE PREPARED / V1.0.0 · PENDING RC2→V1.0.0 DELTA AUDIT. Release candidate V1.0.0-rc2 passed the
final blind release audit (verdict RELEASE-READY; audits/PAPER3_RC2_FINAL_BLIND_RELEASE_AUDIT.md). Public release: not
yet executed. The mathematics is that of the audited V0.4-dev.6 (archive SHA-256
c473af60f8b54c0beecd252d9e8409eef734ba475c0d693b300946f57941b691); no mathematical source, certificate or proof record
changed in any release candidate or in V1.0.0. Current statuses (docs/AUDIT_STATUS_MATRIX.md):
- Track A: Theorem A and Corollary M — PROVED (computer-assisted) · INDEPENDENTLY AUDITED.
- B1: Lemma K — CERTIFIED · INDEPENDENTLY AUDITED · ERRATUM CLOSED; Proposition B1 — CERTIFIED (computer-assisted) ·
  INDEPENDENTLY AUDITED · ERRATUM CLOSED.
- B2.3: Lemma Q — CERTIFIED · INDEPENDENTLY AUDITED.
- B2.4: Proposition B2 — PROVED (computer-assisted) · INDEPENDENTLY AUDITED.
- B2.5: Proposition B3 and Corollary B3' — PROVED (computer-assisted) · INDEPENDENTLY AUDITED. Inertia
  (negative, zero, positive): centre (1, 0, 2), slice (4, 0, 14), R^24 (4, 6, 14); the six raw zero modes are rigid
  motions. No statement implies stability.
The proof records under data/ keep the status strings they had when they were generated; the audit statuses above are
recorded separately in docs/AUDIT_STATUS_MATRIX.json. Not frozen, not published.
Paper 2 (frozen at V0.2-dev.10, public V1.0, DOI 10.5281/zenodo.24187155) is used only as read-only input.
"""
__version__ = "1.0.0"
STATUS = "FINAL RELEASE PREPARED / V1.0.0 · PENDING RC2→V1.0.0 DELTA AUDIT"
