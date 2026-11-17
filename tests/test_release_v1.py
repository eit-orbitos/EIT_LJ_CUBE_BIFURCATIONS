"""V1.0.0 release checks: version/status, verbatim audit reports (including the final blind release audit of
V1.0.0-rc2), audit-status matrix and holds, author and affiliation metadata (no corporate role for Mihail Mladenski),
author-approved declarations, PDF document properties, release-text scans, proof-graph validation, and the mechanical
preservation check against the audited V0.4-dev.6 archive and against V1.0.0-rc2.

The preservation test needs the V0.4-dev.6 archive (SHA-256 c473af60...b691); pass its path in the environment variable
EIT_LJ_DEV6_ARCHIVE. Without it that single test is skipped with an explicit reason. If EIT_LJ_RC2_ARCHIVE points to the
V1.0.0-rc2 archive (SHA-256 6dee0be5...1a08), the comparison against RC2 is included."""
import hashlib
import json
import os
import pathlib
import re
import subprocess
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
DEV6_SHA256 = "c473af60f8b54c0beecd252d9e8409eef734ba475c0d693b300946f57941b691"
AFF = "EITNetworks LLC, Tobyhanna, Pennsylvania, USA"
AUDITS = {
    "audits/CUBE_BIFURCATIONS_REVIEWER_REPORT.md": "f82c5ef1a03c33c0909313bd6442d1879d39717f991cc8e245eb0c61f75d8b85",
    "audits/CUBE_BIFURCATIONS_V03_REVIEWER_REPORT.md": "82bd4f21630a20481113702a9f49dddfa6327f2baf3c07a131af259c1baa65e5",
    "audits/CUBE_BIFURCATIONS_V04_DEV4_B1_ERRATUM_REAUDIT.md":
        "ba482da06aa0492b6524e47680fd949170f4d0dafac0d5661a073efce4d46b74",
    "audits/CUBE_BIFURCATIONS_V05_BLIND_B23_LEMMA_Q_REVIEWER_REPORT.md":
        "841152f2cccd0a43c4f8e73ce5d0cf37e9793d26f12047d5143ea5a053e96bcf",
    "audits/CUBE_BIFURCATIONS_V05_BLIND_B24_REVIEWER_REPORT.md":
        "0302930b9a96ac6bca3df4e720ba34ab5937f73944aee76ba85f345706bdb1ec",
    "audits/CUBE_BIFURCATIONS_V04_DEV6_BLIND_B25_REVIEWER_REPORT.md":
        "bffd4948721ee62f6898336734670ee51381caf546cdd69e0a2ad810e37f165a",
    "audits/PAPER3_RC2_FINAL_BLIND_RELEASE_AUDIT.md": "37b0b4d68f4675b4546f7313aca6937c51cdf1ee11d1cc20b528918e636d7448",
}
STATUS = "FINAL RELEASE PREPARED / V1.0.0 · PENDING RC2→V1.0.0 DELTA AUDIT"
CI_TEXT = ("Toni Mladenovski is Founder of EITNetworks LLC. Both authors are affiliated with EITNetworks LLC. Software "
           "associated with this work is released under a noncommercial license, with commercial use available only by "
           "separate written agreement. The research received no external funding.")


def test_version_and_status_are_final_release_prepared():
    sys.path.insert(0, str(ROOT / "src"))
    import cube_bif
    assert cube_bif.__version__ == "1.0.0"
    assert cube_bif.STATUS == STATUS


def test_all_audit_reports_are_verbatim():
    for rel, h in AUDITS.items():
        assert hashlib.sha256((ROOT / rel).read_bytes()).hexdigest() == h, rel


def test_audit_status_matrix_inertia_and_holds():
    m = json.loads((ROOT / "docs" / "AUDIT_STATUS_MATRIX.json").read_text(encoding="utf-8"))
    assert m["version"] == "1.0.0"
    assert m["status"] == STATUS
    assert m["final_blind_release_audit"] == "RELEASE-READY"
    assert m["final_blind_release_audit_record"]["audited_archive_sha256"] == \
        "6dee0be5f975d23fce3a36770ddebad8041aae9e3f302df0cd923fad91481a08"
    assert (m["rc2_to_v1_delta_audit"], m["public_release"]) == ("PENDING", "NOT YET EXECUTED")
    inertia = m["D2h_branch_inertia"]
    assert inertia["ordering"] == "negative / zero / positive"
    assert (inertia["centre"], inertia["slice"], inertia["R24"]) == ([1, 0, 2], [4, 0, 14], [4, 6, 14])
    assert (inertia["centre_morse_index"], inertia["centre_nullity"]) == (1, 0)
    assert (inertia["slice_morse_index"], inertia["slice_nullity"]) == (4, 0)
    assert inertia["implies_stability"] is False
    ids = {r["id"]: r for r in m["records"]}
    for rid in ("Theorem A", "Corollary M", "Proposition B2", "Proposition B3", "Corollary B3′"):
        assert ids[rid]["status"] == "PROVED (computer-assisted)", rid
        assert ids[rid]["audit"] == "INDEPENDENTLY AUDITED", rid
    for rid in ("Lemma M", "Lemma K", "Lemma Q"):
        assert ids[rid]["status"] == "CERTIFIED", rid
    for rid in ("Lemma K", "Proposition B1"):
        assert ids[rid]["audit"] == "INDEPENDENTLY AUDITED · ERRATUM CLOSED", rid
    assert (m["freeze"], m["github"], m["zenodo"], m["springer_submission"], m["v1_0_0_tag"]) == \
        ("NO", "HOLD", "HOLD", "HOLD", "NOT CREATED")


def test_author_and_affiliation_metadata():
    cff = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    authors = cff[cff.index("authors:"):cff.index("keywords:")]
    assert re.findall(r"given-names: (\S+)", authors) == ["Toni", "Mihail"]
    assert authors.count(f'affiliation: "{AFF}"') == 2
    toni, mihail = authors[:authors.index("Mladenski")], authors[authors.index("Mladenski"):]
    assert "0009-0009-8343-662X" in toni and "info@eitnetworks.org" in toni
    assert "orcid" not in mihail and "mmladenski077@gmail.com" in mihail
    z = json.loads((ROOT / ".zenodo.json").read_text(encoding="utf-8"))
    assert [c["name"] for c in z["creators"]] == ["Mladenovski, Toni", "Mladenski, Mihail"]
    assert all(c["affiliation"] == AFF for c in z["creators"])
    assert z["creators"][0]["orcid"] == "0009-0009-8343-662X" and "orcid" not in z["creators"][1]
    ms = (ROOT / "paper" / "manuscript.tex").read_text(encoding="utf-8")
    front = ms[:ms.index("\\begin{document}")]
    assert AFF in front and "info@eitnetworks.org" in front and "0009-0009-8343-662X" in front
    assert "mmladenski077" not in front and "tml30993" not in front
    assert len(re.findall(r"\d{4}-\d{4}-\d{4}-\d{3}[\dX]", front)) == 2  # Toni's ORCID: link target and text
    assert "Founder" not in front and "Co-founder" not in front
    assert "pdftitle={Symmetry-Breaking Bifurcations from the Cubic Equilibrium in Two-Term Inverse-Power Clusters}" \
        in " ".join(front.split())
    assert "pdfauthor={Toni Mladenovski; Mihail Mladenski}" in front
    # stale locations / school: nowhere outside the scanners, their tests and their generated scan record
    skip = ("scripts", "tests", "audits")
    tree = "\n".join(p.read_text(encoding="utf-8", errors="ignore") for p in ROOT.rglob("*")
                     if p.is_file() and p.suffix in (".md", ".tex", ".cff", ".json", ".bib", ".py")
                     and not any(s in p.parts for s in skip) and "TEXT_SCAN" not in p.name)
    for bad in ("Woodland Park", "Little Falls", "New Jersey", "Passaic", "PCTI"):
        assert bad not in tree, bad


def test_no_corporate_role_for_mihail_and_approved_competing_interests():
    """Author correction: Mihail Mladenski keeps the EITNetworks LLC affiliation but no corporate role is stated; the
    corrected competing-interests text is used verbatim on every current declaration surface."""
    for rel in ("README.md", "CITATION.cff", ".zenodo.json", "paper/manuscript.tex", "paper/sections/13_declarations.tex",
                "submission/DECLARATIONS.md", "submission/SUBMISSION_METADATA_SHEET.md",
                "submission/COVER_LETTER_DRAFT.md"):
        t = " ".join((ROOT / rel).read_text(encoding="utf-8").split())
        assert not re.search(r"(?i)co-?founder|cofounder", t), rel
    for rel in ("paper/sections/13_declarations.tex", "submission/DECLARATIONS.md", "submission/COVER_LETTER_DRAFT.md",
                "AUTHOR_DECISION_V1.0.0.md"):
        assert CI_TEXT in " ".join((ROOT / rel).read_text(encoding="utf-8").split()), rel
    readme = " ".join((ROOT / "README.md").read_text(encoding="utf-8").split())
    assert "**Mihail Mladenski** — EITNetworks LLC, Tobyhanna, Pennsylvania, USA. mmladenski077@gmail.com. No ORCID." \
        in readme
    for gone in ("AUTHORSHIP_FINAL_APPROVAL_REQUIRED.md", "submission/DECLARATIONS_DRAFT.md"):
        assert not (ROOT / gone).exists(), gone


def test_release_text_scan_has_no_finding():
    p = subprocess.run([sys.executable, str(ROOT / "scripts" / "check_release_text.py"), str(ROOT)],
                       capture_output=True, text=True)
    assert p.returncode == 0, p.stdout + p.stderr


def test_whole_tree_text_scan_has_no_unresolved_occurrence():
    p = subprocess.run([sys.executable, str(ROOT / "scripts" / "scan_text_v1.py"), str(ROOT)],
                       capture_output=True, text=True)
    assert p.returncode == 0, p.stdout[-4000:] + p.stderr[-2000:]


def test_proof_dependency_graphs_validate():
    """Read-only structural validation of the three proof graphs: acyclic, no dangling edge, classified leaves,
    no numerical / corroboration / consistency item reachable as a proof dependency, Paper 2 inputs frozen."""
    p = subprocess.run([sys.executable, str(ROOT / "scripts" / "validate_dependency_graphs.py"), str(ROOT)],
                       capture_output=True, text=True)
    assert p.returncode == 0, p.stdout + p.stderr
    assert p.stdout.count("PASS ") == 3


def test_preservation_against_dev6():
    archive = os.environ.get("EIT_LJ_DEV6_ARCHIVE")
    if not archive or not pathlib.Path(archive).is_file():
        pytest.skip("EIT_LJ_DEV6_ARCHIVE not set: the audited V0.4-dev.6 archive is needed for the preservation check")
    assert hashlib.sha256(pathlib.Path(archive).read_bytes()).hexdigest() == DEV6_SHA256
    args = [sys.executable, str(ROOT / "scripts" / "check_preservation_V1_0_0.py"), archive, str(ROOT)]
    rc2 = os.environ.get("EIT_LJ_RC2_ARCHIVE")
    if rc2 and pathlib.Path(rc2).is_file():
        args.append(f"--rc2={rc2}")
    p = subprocess.run(args, capture_output=True, text=True)
    assert p.returncode == 0, p.stdout[-4000:] + p.stderr[-2000:]
