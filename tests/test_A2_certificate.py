"""Phase A2 — the Lemma M certificate: independent re-check of every box, coverage, positivity, tamper rejection, and
negative controls for the certification method."""
import copy
import hashlib
import json
import pathlib
from fractions import Fraction

import mpmath as mp
import pytest
from flint import fmpq

from cube_bif import a2u, certcheck, lemma_m

ROOT = pathlib.Path(__file__).resolve().parents[1]
STORED = ROOT / "data" / "A2_lemma_M_certificate.json"
HASHFILE = ROOT / "data" / "A2_CERTIFICATE_SEMANTIC.sha256"


@pytest.fixture(scope="module")
def built():
    return lemma_m.build_certificate(ROOT)


@pytest.fixture(scope="module")
def stored():
    if not STORED.exists():
        pytest.skip("data/ not generated")
    return json.loads(STORED.read_text())


def rehash(cert):
    """Re-seal a tampered certificate (so that rejection comes from the mathematics, not from the hash)."""
    for k, v in cert["expressions"].items():
        cert["expression_sha256"][k] = hashlib.sha256(v.encode()).hexdigest()
    cert["provenance"]["semantic_sha256"] = certcheck.semantic_hash(cert)
    return cert


def rejected(cert, needle):
    ok, rep = certcheck.check(cert)
    assert not ok
    assert any(needle in f for f in rep["failures"]), rep["failures"]


# ---- the certificate itself ---------------------------------------------------------------------------------------
def test_fresh_certificate_passes_the_independent_checker(built):
    ok, rep = certcheck.check(built)
    assert ok, rep["failures"]
    assert rep["boxes_checked"] == built["n_boxes"]


def test_stored_certificate_passes_and_matches_the_hash_file(stored):
    h = HASHFILE.read_text().split()[0]
    ok, rep = certcheck.check(stored, h)
    assert ok, rep["failures"]


def test_fresh_and_stored_certificates_have_the_same_semantic_hash(built, stored):
    assert certcheck.semantic_hash(built) == certcheck.semantic_hash(stored)


def test_records_precision_counts_bound_and_versions(built):
    assert built["method"]["arb_precision_bits"] == 128
    assert built["n_boxes"] == len(built["boxes"]) and built["max_depth_used"] >= 1
    prov = built["provenance"]
    for k in ("python-flint", "FLINT", "sympy", "python", "code_sha256", "seconds", "semantic_sha256"):
        assert k in prov
    assert prov["excluded_from_semantic_hash"] is True


def test_coverage_is_gap_free_with_exact_rational_endpoints(built):
    los = [Fraction(b["lo"]) for b in built["boxes"]]
    his = [Fraction(b["hi"]) for b in built["boxes"]]
    assert los[0] == 0 and his[-1] == Fraction(16, 5)
    assert all(a < b for a, b in zip(los, his))
    assert all(his[i] == los[i + 1] for i in range(len(los) - 1))
    assert all("." not in b["lo"] + b["hi"] + b["lower_bound"] for b in built["boxes"])   # no decimal endpoints


def test_every_lower_bound_is_strictly_positive(built):
    lbs = [Fraction(b["lower_bound"]) for b in built["boxes"]]
    assert all(lb > 0 for lb in lbs)
    assert Fraction(built["min_lower_bound"]) == min(lbs)


def test_every_box_reconstructed_by_sampling(built):
    """Third, non-Arb route: m' sampled at 7 points of every box (mpmath, 40 digits) exceeds the box's bound."""
    mp.mp.dps = 40
    m = a2u.numeric(lemma_m.M_CLOSED)
    for b in built["boxes"]:
        lo, hi, lb = (mp.mpf(Fraction(b[k]).numerator) / Fraction(b[k]).denominator for k in ("lo", "hi", "lower_bound"))
        for j in range(7):
            assert mp.diff(m, lo + (hi - lo) * j / 6) > lb


# ---- tampered certificates are rejected ---------------------------------------------------------------------------
def test_rejects_a_gap(built):
    c = copy.deepcopy(built)
    c["boxes"][10]["hi"] = str(Fraction(c["boxes"][10]["hi"]) - Fraction(1, 1000))
    rejected(rehash(c), "gap or an overlap")


def test_rejects_an_overlap(built):
    c = copy.deepcopy(built)
    c["boxes"][20]["lo"] = str(Fraction(c["boxes"][20]["lo"]) - Fraction(1, 1000))
    rejected(rehash(c), "gap or an overlap")


def test_rejects_a_shortened_interval(built):
    c = copy.deepcopy(built)
    c["boxes"][0]["lo"] = "1/100"
    rejected(rehash(c), "start at 0")


def test_rejects_an_extended_claim(built):
    c = copy.deepcopy(built)
    c["claim"]["interval"] = ["0", "17/5"]
    rejected(rehash(c), "claim differs")


def test_rejects_a_flipped_relation(built):
    c = copy.deepcopy(built)
    c["claim"]["relation"] = "<"
    rejected(rehash(c), "claim differs")


def test_rejects_a_nonpositive_lower_bound(built):
    c = copy.deepcopy(built)
    c["boxes"][5]["lower_bound"] = "-1/1048576"
    rejected(rehash(c), "not strictly positive")


def test_rejects_a_sign_flipped_function(built):
    c = copy.deepcopy(built)
    c["expressions"]["Psi"] = "-(" + c["expressions"]["Psi"] + ")"
    rejected(rehash(c), "m' = Psi/(16 S^3) differs")


def test_rejects_an_altered_function_expression(built):
    c = copy.deepcopy(built)
    assert "81*r" in c["expressions"]["m"]
    c["expressions"]["m"] = c["expressions"]["m"].replace("81*r", "80*r")
    rejected(rehash(c), "m differs from the V0.1-dev closed form")


def test_rejects_an_altered_derivative_expression(built):
    c = copy.deepcopy(built)
    c["expressions"]["Phi"] = c["expressions"]["Phi"] + " + r**2"
    rejected(rehash(c), "m'' = Phi/(16 S^4) differs")


def test_rejects_an_inflated_lower_bound(built):
    c = copy.deepcopy(built)
    c["boxes"][0]["lower_bound"] = "7/10"       # m'(0) = 0.6169... < 0.7
    c["min_lower_bound"] = min((b["lower_bound"] for b in c["boxes"]), key=Fraction)
    rejected(rehash(c), "lower bound not confirmed")


def test_rejects_content_that_does_not_match_its_semantic_hash(built):
    c = copy.deepcopy(built)
    c["boxes"][3]["lower_bound"] = "1/2"         # still true, but the content no longer matches the recorded hash
    c["min_lower_bound"] = min((b["lower_bound"] for b in c["boxes"]), key=Fraction)
    rejected(c, "semantic hash")


def test_rejects_an_unrecorded_hash_file_value(built):
    ok, rep = certcheck.check(built, "0" * 64)
    assert not ok and any("hash file" in f for f in rep["failures"])


# ---- negative controls for the method ------------------------------------------------------------------------------
def test_method_fails_beyond_the_monotonicity_range():
    """m' changes sign near r = 7.649 (maximum of m); the same method must not certify [7, 8]."""
    res = lemma_m.certify(fmpq(7), fmpq(8))
    assert not res["ok"]
    f = res["failure"]
    assert Fraction(f["lo"]) <= Fraction(7649, 1000) <= Fraction(f["hi"]) or Fraction(f["lo"]) > Fraction(7649, 1000)


def test_method_fails_where_m_prime_is_negative():
    assert not lemma_m.certify(fmpq(8), fmpq(9))["ok"]


def test_method_fails_for_the_negated_function():
    assert not lemma_m.certify(fmpq(0), fmpq(16, 5), sign=-1)["ok"]


def test_method_fails_for_a_bound_above_the_infimum():
    assert not lemma_m.certify(fmpq(0), fmpq(1, 10), bound=fmpq(31, 50))["ok"]


def test_method_certifies_a_true_subclaim():
    assert lemma_m.certify(fmpq(1), fmpq(2))["ok"]
