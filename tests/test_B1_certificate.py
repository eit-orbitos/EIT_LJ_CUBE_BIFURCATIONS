"""Phase B1.7: the Arb certificate that kappa_hat > 0 on the closed T2g curve, its independent checker, tamper tests
and method controls."""
import copy
import json
import pathlib

import mpmath as mp
import pytest
from flint import arb, fmpq

from cube_bif import b1_cert, b1_check
from cube_bif import b1_cubic as b1

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
mp.mp.dps = 30


@pytest.fixture(autouse=True)
def _working_precision():
    """Each test runs at this module's precision, whatever other modules set."""
    with mp.workdps(30):
        yield


@pytest.fixture(scope="module")
def derived():
    return b1_check.derive_functions()


@pytest.fixture(scope="module")
def built():
    return b1_cert.build_certificate(ROOT)


@pytest.fixture(scope="module")
def stored():
    f = DATA / "B1_kappa_certificate.json"
    if not f.exists():
        pytest.skip("data/ not generated")
    return json.loads(f.read_text())


def rehash(cert):
    cert["provenance"]["semantic_sha256"] = b1_check.semantic_hash(cert)
    return cert


def failures(cert, derived, h=None):
    ok, rep = b1_check.check(cert, h, derived=derived)
    return ok, " | ".join(rep["failures"])


# ---- the certificate passes ---------------------------------------------------------------------------------------
def test_fresh_certificate_passes_the_independent_checker(built, derived):
    ok, msg = failures(built, derived)
    assert ok, msg


def test_stored_certificate_passes_and_matches_the_hash_file(stored, derived):
    h = (DATA / "B1_CERTIFICATE_SEMANTIC.sha256").read_text().split()[0]
    ok, msg = failures(stored, derived, h)
    assert ok, msg


def test_stored_certificate_is_the_historical_audited_one(stored):
    """Erratum E-B1 (V0.4-dev.4, NOTES.md §10): the corrected generator produces other bytes, so fresh and stored
    semantic hashes are no longer compared. The stored, audited certificate is pinned instead; the two tests above
    show that the corrected checker accepts both it and a fresh build."""
    assert b1_check.semantic_hash(stored) == "616817fcc70e0fab7f106404e5e5332b17b9c4480bd440355f1ac5257a8518c6"


def test_records_precision_boxes_depth_and_versions(built):
    assert built["method"]["arb_precision_bits"] == 128
    assert built["n_boxes"] == len(built["boxes"]) >= 200
    assert built["max_depth_used"] == max(b["depth"] for b in built["boxes"])
    prov = built["provenance"]
    for k in ("python-flint", "FLINT", "sympy", "mpmath", "project_version", "code_sha256", "semantic_sha256"):
        assert k in prov
    assert prov["excluded_from_semantic_hash"] is True


def test_coverage_is_gap_free_with_exact_rationals(built):
    b = built["boxes"]
    assert b1_check._q(b[0]["q_lo"]) == 0 and b1_check._q(b[-1]["q_hi"]) == fmpq(101, 50)
    assert all(b1_check._q(x["q_hi"]) == b1_check._q(y["q_lo"]) for x, y in zip(b, b[1:]))
    assert all("." not in x[k] for x in b for k in ("q_lo", "q_hi", "delta_lo", "delta_hi"))
    corner = [x for x in b if x["corner"]]
    assert len(corner) == 1 and b1_check._q(corner[0]["q_lo"]) < b1_check.QC_LO < b1_check.QC_HI \
        < b1_check._q(corner[0]["q_hi"])
    assert all(b1_check._q(x["delta_lo"]) > 0 for x in b if not x["corner"])


def test_every_lower_bound_is_strictly_positive_and_min_matches(built):
    lbs = [b1_check._q(x["kappa_hat_lower_bound"]) for x in built["boxes"]]
    assert all(lb > 0 for lb in lbs)
    assert str(min(lbs)) == built["min_lower_bound"]
    assert min(lbs) > fmpq(24, 10000)


def test_every_box_reconstructed_by_sampling(built):
    """NUMERICAL corroboration: at three points of every box (left of q_c) the curve value of delta lies in the
    recorded ball and kappa_hat exceeds the recorded bound."""
    for x in built["boxes"]:
        lo, hi = b1_check._q(x["q_lo"]), b1_check._q(x["q_hi"])
        dlo, dhi = b1_check._q(x["delta_lo"]), b1_check._q(x["delta_hi"])
        lb = b1_check._q(x["kappa_hat_lower_bound"])
        for t in (fmpq(0), fmpq(1, 2), fmpq(1)):
            q = lo + t * (hi - lo)
            qq = mp.mpf(int(q.p)) / int(q.q)
            if qq >= mp.mpf("2.0199"):
                continue
            c = b1.carrier(qq)
            assert mp.mpf(int(dlo.p)) / int(dlo.q) <= c["delta"] <= mp.mpf(int(dhi.p)) / int(dhi.q), x["q_lo"]
            assert c["kappa_hat"] > mp.mpf(int(lb.p)) / int(lb.q), x["q_lo"]


def test_endpoints_and_corner_identification(built):
    e = built["endpoints"]
    assert e["q=0"]["certified"] and e["q=0"]["overlaps_paper2"]
    assert e["corner"]["certified"] and e["corner"]["sign_change_consistent_with_lemma_T2"]
    assert built["corner_identification"]["positive"] and built["corner_identification"]["q_c_inside_corner_box"]
    assert b1_check._q(e["corner"]["kappa_hat_lower_bound"]) > fmpq(6, 1000)


# ---- tampered certificates are rejected --------------------------------------------------------------------------------
def tampered(built, f):
    c = copy.deepcopy(built)
    f(c)
    return rehash(c)


@pytest.mark.parametrize("name,mutate,expect", [
    ("gap", lambda c: c["boxes"].pop(10), "gap or overlap"),
    ("overlap", lambda c: c["boxes"][10].update(q_lo=c["boxes"][9]["q_lo"]), "gap or overlap"),
    ("start", lambda c: c["boxes"][0].update(q_lo="1/1000"), "does not start at 0"),
    ("truncated end", lambda c: c["boxes"].pop(), "does not end at the claimed endpoint"),
    ("flipped relation", lambda c: c["claim"].update(relation="<"), "claim differs"),
    ("non-positive bound", lambda c: c["boxes"][3].update(kappa_hat_lower_bound="0"), "not strictly positive"),
    ("inflated bound", lambda c: c["boxes"][0].update(kappa_hat_lower_bound="1/250"), "lower bound not confirmed"),
    ("shifted delta ball", lambda c: c["boxes"][5].update(
        delta_lo=str(b1_check._q(c["boxes"][5]["delta_lo"]) + fmpq(1, 20)),
        delta_hi=str(b1_check._q(c["boxes"][5]["delta_hi"]) + fmpq(1, 20))), "Newton inclusion not confirmed"),
    ("altered g_uuu", lambda c: c["expressions"].update(uuu=c["expressions"]["uuu"].replace("4*r + 7", "4*r + 8")),
     "stored expression uuu differs"),
    ("altered M12", lambda c: c["expressions"].update(M12=c["expressions"]["M12"].replace("(r + 2)", "(r + 3)")),
     "stored expression M12 differs"),
    ("corner box removed", lambda c: [b.update(corner=False) for b in c["boxes"]], "corner box must be unique"),
    ("delta ball through zero", lambda c: c["boxes"][7].update(delta_lo="-1/1000"), "delta ball not positive"),
    ("far regime too close to the diagonal", lambda c: [b.update(regime="far") for b in c["boxes"]
                                                         if b["corner"]], "far regime with delta <= 1"),
])
def test_tampered_certificate_is_rejected(built, derived, name, mutate, expect):
    ok, msg = failures(tampered(built, mutate), derived)
    assert not ok and expect in msg, (name, msg)


def test_semantic_hash_mismatch_is_rejected(built, derived):
    c = copy.deepcopy(built)
    c["boxes"][1]["kappa_hat_lower_bound"] = "1/1000"
    ok, msg = failures(c, derived)
    assert not ok and "semantic hash" in msg


def test_wrong_hash_file_is_rejected(built, derived):
    ok, msg = failures(built, derived, "0" * 64)
    assert not ok and "hash file" in msg


# ---- method controls -----------------------------------------------------------------------------------------------------
@pytest.fixture(scope="module")
def est():
    return b1_cert._cached_estimator()


def test_method_fails_on_a_false_bound(est):
    boxes, fail = b1_cert.certify_interval(fmpq(0), fmpq(1, 10), est, claim_bound=fmpq(3, 1000), max_depth=8)
    assert fail is not None and b1_check._q(fail["q_lo"]) == 0


def test_method_fails_at_a_sign_change(est):
    def f(Q, D, reg):
        kh, m22, rho = b1_cert.carrier_enclosure(Q, D, reg)
        return arb(fmpq(9, 2000)) - kh, m22, rho
    boxes, fail = b1_cert.certify_interval(fmpq(2, 5), fmpq(3, 5), est, carrier=f, max_depth=10)
    assert fail is not None
    assert fmpq(44, 100) < b1_check._q(fail["q_lo"]) < fmpq(47, 100)          # the root is 0.46294


def test_method_fails_on_the_raw_coefficient_at_both_endpoints(est):
    def raw(Q, D, reg):
        kh, m22, rho = b1_cert.carrier_enclosure(Q, D, reg)
        L2, L3 = arb(2).log(), arb(3).log()
        return Q * (1 + (-(L2 / 2) * Q).exp() + (-(L3 / 2) * Q).exp() / 3) * D * kh, m22, rho
    assert b1_cert.certify_interval(fmpq(0), fmpq(1, 100), est, carrier=raw, max_depth=6)[1] is not None
    c = b1_cert.CORNER
    assert b1_cert.certify_interval(c[0], c[1], est, carrier=raw, base=[c[0], c[1]])[1] is not None


def test_method_fails_with_the_wrong_kernel_vector(est):
    def wrong(Q, D, reg):
        v = b1_cert.divided(Q, D, reg)[0]
        rho = v["M12"] / v["M22"]
        return v["uuu"] + 3 * rho * v["uuv"] + 3 * rho ** 2 * v["uvv"] + rho ** 3 * v["vvv"], v["M22"], rho
    assert b1_cert.certify_interval(fmpq(1, 2), fmpq(1), est, carrier=wrong, max_depth=6)[1] is not None


def test_method_certifies_a_true_subclaim(est):
    boxes, fail = b1_cert.certify_interval(fmpq(1, 2), fmpq(1), est)
    assert fail is None and boxes
