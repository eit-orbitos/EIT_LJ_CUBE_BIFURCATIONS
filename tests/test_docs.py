"""Claim discipline: status labels; "proved" only computer-assisted and only for Theorem A and Corollary M; no novelty\nlanguage; recorded data consistent."""
import json
import pathlib
import re

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
DOCS = [ROOT / "README.md", ROOT / "NOTES.md", ROOT / "RESEARCH_LOG.md",
        ROOT / "docs" / "CONTRADICTIONS_EXTERNAL_BRAINSTORM.md", ROOT / "reference" / "PAPER2_INPUTS.md"]


def text(p):
    return p.read_text(encoding="utf-8")


def test_status_is_final_release_prepared():
    """V1.0.0: the current status surfaces carry the final-release-prepared status, the RC2 audit verdict and the
    audited labels."""
    for p in (ROOT / "README.md", ROOT / "NOTES.md", ROOT / "RESEARCH_LOG.md"):
        assert "FINAL RELEASE PREPARED / V1.0.0" in text(p), p.name
        assert "PENDING RC2→V1.0.0 DELTA AUDIT" in text(p), p.name
        assert "RELEASE-READY" in text(p), p.name
        assert "INDEPENDENTLY AUDITED" in text(p), p.name
        assert "ERRATUM CLOSED" in text(p), p.name
    import cube_bif
    assert cube_bif.STATUS == "FINAL RELEASE PREPARED / V1.0.0 · PENDING RC2→V1.0.0 DELTA AUDIT"
    assert cube_bif.__version__ == "1.0.0"


def test_proved_status_only_computer_assisted_and_only_for_A_M_B2_B3():
    for p in DOCS:
        t = text(p)
        assert "STATUS: PROVED" not in t.upper(), p.name
        assert "**PROVED**" not in t, p.name
        assert not re.search(r"PROVED(?! \(computer-assisted)", t), p.name
        for line in t.splitlines():
            if "PROVED (computer-assisted" in line:
                assert any(k in line for k in ("Theorem A", "Corollary M", "Proposition B2", "Proposition B3",
                                               "Corollary B3′", "| PROVED (computer-assisted) |")), line
    notes = text(ROOT / "NOTES.md")
    headings = [l for l in notes.splitlines() if l.startswith("#") and "PROVED" in l]
    assert len(headings) == 4
    assert headings[0].startswith("### 3.8 Corollary M") and headings[1].startswith("### 3.9 Theorem A")
    assert "INDEPENDENTLY AUDITED" in headings[1]
    assert headings[2] == ("## 12. Phase B2.4 — Proposition B2: the D2h-axial pitchfork — "
                           "PROVED (computer-assisted) · INDEPENDENTLY AUDITED (audit recorded in V1.0.0-rc1, §15)")
    assert headings[3] == ("## 13. Phase B2.5 — Proposition B3: the centre-manifold index of the D2h branch — "
                           "PROVED (computer-assisted) · INDEPENDENTLY AUDITED (audit recorded in V1.0.0-rc1, §15)")
    lq = [l for l in notes.splitlines() if l.startswith("## 9. Phase B2.3")]
    assert lq == ["## 9. Phase B2.3 — Lemma Q: ĉ₄ > 0 on the closed T2g curve — CERTIFIED (computer-assisted) · "
                  "INDEPENDENTLY AUDITED (audit recorded in V1.0.0-rc1, §15)"]
    assert "Theorem candidate A (CANDIDATE)" not in notes


def test_theorem_A_cites_every_hypothesis_and_its_status():
    notes = text(ROOT / "NOTES.md")
    sec = notes[notes.index("### 3.9 Theorem A"):notes.index("## 4. Phase B0")]
    for item in ("(H0)", "(H1) Z₂ evenness", "(H2) one-dimensional kernel mod rigid motions", "(H3) transversality",
                 "(H4) c₄(q) > 0", "Lemma M", "FROZEN INPUT (Paper 2, Theorem 4′)", "FROZEN INPUT (Paper 2, Lemma A)",
                 "FROZEN INPUT (Paper 2, Prop. A)", "CERTIFIED", "STANDARD", "VERIFIED-EXACT",
                 "Branch side, from the reduced equation", "μ*′(0) = −G_s/G_μ = −c₄/(6λ′(0)) > 0",
                 "src/cube_bif/theorem_a.py", "not used in the proof"):
        assert item in sec, item
    lemma = notes[notes.index("### 3.7 Lemma M"):notes.index("### 3.8 Corollary M")]
    for item in ("161457/262144", "16/5", "m′(r) = Ψ/(16S³)", "128 bits", "160 bits", "64", "[7, 8]"):
        assert item in lemma, item


def test_no_novelty_language():
    pat = re.compile(r"\bnovel\b|for the first time|\bfirst to\b|new result|groundbreaking|unprecedented", re.I)
    for p in DOCS:
        assert not pat.search(text(p)), p.name


def test_paper2_archive_hash_is_the_published_one():
    from cube_bif import paper2_ref
    assert paper2_ref.ARCHIVE_SHA256 == "bb70721df7f0aa17edca30d84d1b4aaf980c0a76693be14fa780e4ab8f64762d"
    assert "10.5281/zenodo.24187155" in text(ROOT / "reference" / "PAPER2_INPUTS.md")


def test_recorded_data_report_all_checks_passing():
    data = ROOT / "data"
    if not (data / "A1_quartic.json").exists():
        pytest.skip("data/ not generated")
    a0 = json.loads(text(data / "A0_representation.json"))
    a1 = json.loads(text(data / "A1_quartic.json"))
    b0 = json.loads(text(data / "B0_t2g.json"))
    assert a0["all_checks_pass"] and a1["identities_all_true"] and b0["all_checks_pass"]
    s = a1["sign_table_summary"]
    assert s["c4_full > 0 at every point"] and s["transversality: h_A'(P_A(q)) < 0 at every point"]
    assert a0["stabilizer_Sigma_A"]["label"] == "T_d"


def test_recorded_A2_data_are_consistent():
    data = ROOT / "data"
    if not (data / "A2_lemma_M_certificate.json").exists():
        pytest.skip("data/ not generated")
    from fractions import Fraction
    cert = json.loads(text(data / "A2_lemma_M_certificate.json"))
    assert cert["claim"] == {"quantity": "m'(r)", "relation": ">", "value": "0", "interval": ["0", "16/5"]}
    assert cert["n_boxes"] == len(cert["boxes"]) == 64
    assert Fraction(cert["min_lower_bound"]) == Fraction(161457, 262144) > 0
    assert cert["near_zero"]["all_positive"] and cert["P_A_bound"]["all_certified"]
    h = text(data / "A2_CERTIFICATE_SEMANTIC.sha256").split()[0]
    assert h == cert["provenance"]["semantic_sha256"]
    ctl = json.loads(text(data / "A2_negative_controls.json"))
    assert ctl["all_as_required"] and len(ctl["controls"]) == 5
    neg = json.loads(text(data / "negative_controls.json"))
    assert neg["all_detected"]


def test_B2_records_and_claim_boundary():
    """B2.0/B2.1 records pass; no B2 heading carries CERTIFIED, PROVED or AUDITED; the section states its boundary."""
    notes = text(ROOT / "NOTES.md")
    sec = notes[notes.index("## 6. Phase B2"):notes.index("## 7. Phase B2.2")]
    heads = [l for l in sec.splitlines() if l.startswith("#")]
    assert len(heads) == 3
    assert not any(k in h for h in heads for k in ("CERTIFIED", "PROVED", "AUDITED"))
    for item in ("Nothing in B2 is called proved or certified", "**Claim boundary.**", "values at five points only",
                 "FROZEN INPUT, Paper 2's Lemma S", "**The relayed claim Fix(D2h) = span{e_crit, A1g, Eg⁽¹⁾, Eg⁽²⁾} "
                 "is not correct**", "⟨b, f₁⟩ = 0 and\n  ⟨b, e₁⟩ = 0 exactly"):
        assert item in sec, item
    data = ROOT / "data"
    if not (data / "B2_quartic.json").exists():
        pytest.skip("data/ not generated")
    sym = json.loads(text(data / "B2_symmetry.json"))
    quart = json.loads(text(data / "B2_quartic.json"))
    assert sym["all_checks_pass"] and quart["all_checks_pass"]
    assert sym["isotypic_ranks_of_Fix"] == {"A1g": 1, "A2g": 0, "Eg": 1, "T1g": 0, "T2g": 2,
                                            "A1u": 0, "A2u": 0, "Eu": 0, "T1u": 0, "T2u": 0}
    assert len(quart["route_comparison"]) == 5 and "no sign claim" in quart["scope"].lower()


def test_B1_erratum_closed_and_B2_4_claim_boundary_after_B2_5():
    """§11 records the targeted re-audit (report hash) and the closed erratum; §12 (unchanged) states the convention,
    the dependency rule and what is not claimed."""
    notes = text(ROOT / "NOTES.md")
    s11 = notes[notes.index("## 11. Targeted re-audit of erratum E-B1"):notes.index("## 12. Phase B2.4")]
    for item in ("CERTIFIED · INDEPENDENTLY AUDITED · ERRATUM CLOSED",
                 "ba482da06aa0492b6524e47680fd949170f4d0dafac0d5661a073efce4d46b74", "formal verdict **PASS**"):
        assert item in s11, item
    s12 = notes[notes.index("## 12. Phase B2.4"):notes.index("## 13. Phase B2.5")]
    for item in ("supercritical in the energy-reduced axial convention", "s*(μ)² = −(6τ/c₄) μ + O(μ²)",
                 "G(z, μ) = λ(μ) + (c₄/6)z + O(z², μz, μ²)", "μ*′(0) = −G_z/G_μ = −c₄/(6τ)",
                 "**No numerical scan is a proof dependency.**", "### 12.10 Claim boundary",
                 "the index on the three-dimensional centre manifold, or stability in R²⁴ (B2.5)",
                 "The branch is not called\n  a cuboid", "isotropy exactly Σ ≅ D2h",
                 "VERIFIED-NUMERIC; not used in the proof"):
        assert item in s12, item
    assert (ROOT / "audits" / "CUBE_BIFURCATIONS_V04_DEV4_B1_ERRATUM_REAUDIT.md").exists()


def test_B2_5_claim_boundary():
    """§13 states the centre index, the derived m_perp, the rigor class, the input-status discrepancy and what is not
    claimed; §14 keeps A3 and release preparation as proposals."""
    notes = text(ROOT / "NOTES.md")
    s13 = notes[notes.index("## 13. Phase B2.5"):notes.index("## 14. Next steps")]
    for item in ("index_centre(D2h branch) = 1,   nullity 0", "det[[d, e], [e, d]] = −κ²s² + O(s⁴)",
                 "**no competing O(s) diagonal term**", "**m_⊥ is derived, not assumed.**", "**m_⊥ = 3**",
                 "index m_⊥ + 1 = **4** and nullity 0", "Rigid translations and\n> rotations are not counted",
                 "**no interval-arithmetic certificate is produced in B2.5**",
                 "**No audit report for B2.3\nor B2.4 is in this package (NOT_PROVIDED here).**",
                 "**No numerical scan is a proof dependency.**", "Consistency only; not used in the proof.",
                 "**Tolerance change, recorded:**", "### 13.11 Claim boundary",
                 "stability of the D2h branch in any sense",
                 "Not independently audited when written (audited since; see §15). Not frozen, not published",
                 "(Resolved in V1.0.0-rc1: both reports were received, PASS; §15.)"):
        assert item in s13, item
    s14 = notes[notes.index("## 14. Next steps"):]
    assert "an independent audit of B2.5" in s14 and "**A3:**" in s14 and "Not started." in s14
    data = ROOT / "data"
    if not (data / "B2_5_index.json").exists():
        pytest.skip("data/ not generated")
    rec = json.loads(text(data / "B2_5_index.json"))
    assert rec["exact"]["all_pass"]
    assert rec["exact"]["statement"]["centre_index"] == 1 and rec["exact"]["corollary"]["full_slice_index"] == 4


def test_rc1_status_section():
    """§15 (V1.0.0-rc1) records the audited statuses, the three new reports by hash, the audited inertia, the
    certificate of record, the historical status strings and the open author items."""
    notes = text(ROOT / "NOTES.md")
    s15 = notes[notes.index("## 15. Release candidate V1.0.0-rc1"):notes.index("## 16. Release candidate V1.0.0-rc2")]
    assert "historical; superseded as current status by §16" in s15
    for item in ("RELEASE CANDIDATE / V1.0.0-rc1 · PENDING FINAL BLIND RELEASE AUDIT",
                 "| Lemma Q | CERTIFIED · INDEPENDENTLY AUDITED |",
                 "| Proposition B2 | PROVED (computer-assisted) · INDEPENDENTLY AUDITED |",
                 "| Proposition B3 | PROVED (computer-assisted) · INDEPENDENTLY AUDITED |",
                 "| Corollary B3′ | PROVED (computer-assisted) · INDEPENDENTLY AUDITED |",
                 "| Lemma K | CERTIFIED · INDEPENDENTLY AUDITED · ERRATUM CLOSED |",
                 "841152f2cccd0a43c4f8e73ce5d0cf37e9793d26f12047d5143ea5a053e96bcf",
                 "0302930b9a96ac6bca3df4e720ba34ab5937f73944aee76ba85f345706bdb1ec",
                 "bffd4948721ee62f6898336734670ee51381caf546cdd69e0a2ad810e37f165a",
                 "centre (three-dimensional T2g reduced Hessian): (1, 0, 2)", "slice (rigid motions removed): (4, 0, 14)",
                 "R²⁴: (4, 6, 14)", "None of these statements implies stability",
                 "616817fcc70e0fab7f106404e5e5332b17b9c4480bd440355f1ac5257a8518c6", "corroboration only",
                 "Mihail Mladenski's exact\nauthor-contribution statement"):
        assert item in s15, item
    for rel in ("CUBE_BIFURCATIONS_V05_BLIND_B23_LEMMA_Q_REVIEWER_REPORT.md",
                "CUBE_BIFURCATIONS_V05_BLIND_B24_REVIEWER_REPORT.md",
                "CUBE_BIFURCATIONS_V04_DEV6_BLIND_B25_REVIEWER_REPORT.md"):
        assert (ROOT / "audits" / rel).exists(), rel


def test_rc2_status_section():
    """§16 (V1.0.0-rc2, historical) records the RC2 status, holds, unchanged audited statuses and inertia, the authors with the
    Tobyhanna affiliation, and the open human-author items (not mathematical defects)."""
    notes = text(ROOT / "NOTES.md")
    s16 = " ".join(notes[notes.index("## 16. Release candidate V1.0.0-rc2"):
                         notes.index("## 17. Release V1.0.0")].split())  # line-wrap independent
    assert "historical; superseded as current status by §17" in s16
    for item in ("RELEASE CANDIDATE / V1.0.0-rc2 · PENDING FINAL BLIND RELEASE AUDIT", "FREEZE = NO", "GitHub = HOLD",
                 "Zenodo = HOLD", "Springer submission = HOLD", "v1.0.0 tag = NOT CREATED",
                 "33095d35107578054c7e54ff62be8a318ab973d7153e5c30d89da2fc9bc0361b",
                 "INDEPENDENTLY AUDITED · ERRATUM CLOSED", "centre (1, 0, 2), slice (4, 0, 14),\nR²⁴ (4, 6, 14)",
                 "None of these statements implies stability", "EITNetworks LLC, Tobyhanna, Pennsylvania, USA",
                 "ORCID 0009-0009-8343-662X", "no ORCID", "No educational\ninstitution is listed",
                 "FINAL AUTHOR CONTRIBUTION APPROVAL REQUIRED BEFORE SPRINGER\nSUBMISSION", "not mathematical defects"):
        assert " ".join(item.split()) in s16, item


def test_v1_status_section():
    """§17 (V1.0.0) records the current status, the RC2 final blind audit verdict, the closed human approvals, the holds,
    the unchanged audited statuses and inertia, the authors (no corporate role for Mihail Mladenski) and the
    placeholders."""
    notes = text(ROOT / "NOTES.md")
    s17 = " ".join(notes[notes.index("## 17. Release V1.0.0"):].split())
    for item in ("FINAL RELEASE PREPARED / V1.0.0 · PENDING RC2→V1.0.0 DELTA AUDIT", "RELEASE-READY",
                 "37b0b4d68f4675b4546f7313aca6937c51cdf1ee11d1cc20b528918e636d7448", "HUMAN APPROVALS: CLOSED",
                 "PUBLIC RELEASE: NOT YET EXECUTED", "FREEZE = NO", "GitHub = HOLD", "Zenodo publish = HOLD",
                 "Springer/JMC submission = HOLD", "v1.0.0 public tag = NOT CREATED",
                 "6dee0be5f975d23fce3a36770ddebad8041aae9e3f302df0cd923fad91481a08",
                 "INDEPENDENTLY AUDITED · ERRATUM CLOSED", "centre (1, 0, 2), slice (4, 0, 14), R²⁴ (4, 6, 14)",
                 "None of these statements implies stability", "EITNetworks LLC, Tobyhanna, Pennsylvania, USA",
                 "ORCID 0009-0009-8343-662X", "no ORCID", "No educational institution is listed",
                 "no corporate role is stated for him", "[PAPER 3 ZENODO DOI — TO BE ASSIGNED AT PUBLIC RELEASE]"):
        assert item in s17, item
