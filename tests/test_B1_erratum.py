"""Erratum E-B1 (V0.4-dev.4): the series length of the two B1 Taylor routines, b1_cert._taylor and
b1_check.Model.taylor (NOTES.md §10).

python-flint 0.9.0 truncates every arb_series at ctx.cap (default 10), whatever prec= asks for. Up to V0.4-dev.3 both
routines asked for longer series without raising ctx.cap and padded the shortened lists with zeros. These tests fail
on that implementation (scripts/negative_controls_B1_erratum.py restores it and checks) and pass on the corrected one.
References are independent of python-flint: mpmath at 60 digits on the closed forms (finite differences, and the\nCauchy integral formula)."""
import contextlib
import hashlib
import json
import pathlib
from fractions import Fraction

import mpmath as mp
import pytest
import sympy as sp
from flint import arb, arb_series, ctx, fmpq

from cube_bif import b1_cert, b1_check

ROOT = pathlib.Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
HISTORICAL_SEMANTIC = "616817fcc70e0fab7f106404e5e5332b17b9c4480bd440355f1ac5257a8518c6"
HISTORICAL_FILE_SHA256 = "dee3ad024af69f76620de35f3d0aa8be06a9f4f099ca0ffb001c4914178f87ab"
NAMES = ("M11", "M12", "M22", "uuu", "uuv", "uvv", "vvv")
R = sp.Symbol("r")


@contextlib.contextmanager
def cap(n):
    old = ctx.cap
    ctx.cap = n
    try:
        yield
    finally:
        ctx.cap = old


@contextlib.contextmanager
def prec(bits):
    old = ctx.prec
    ctx.prec = bits
    try:
        yield
    finally:
        ctx.prec = old


def _closed_forms():
    """The seven closed forms as SymPy expressions in r, from the generator's expression strings (b1_check verifies
    them against its own derivation)."""
    X, Y = 2 ** (-R / 2), 3 ** (-R / 2)
    loc = {"r": R, "X": X, "Y": Y, "W": 1 + X + Y / 3, "sqrt": sp.sqrt}
    return {k: sp.sympify(b1_cert.EXPRESSIONS[k], locals=loc) for k in NAMES}


@pytest.fixture(scope="module")
def forms():
    return _closed_forms()


@pytest.fixture(scope="module")
def mpf_funcs(forms):
    return {k: sp.lambdify(R, e, "mpmath") for k, e in forms.items()}


@pytest.fixture(scope="module")
def model(forms):
    """The checker's Model on functions in r, X, Y. Built from the generator's strings for speed; the B1 certificate
    tests compare these strings with the checker's own derivation."""
    loc = {"r": b1_check.R_, "X": b1_check.X_, "Y": b1_check.Y_, "W": 1 + b1_check.X_ + b1_check.Y_ / 3,
           "sqrt": sp.sqrt}
    return b1_check.Model({k: sp.sympify(b1_cert.EXPRESSIONS[k], locals=loc) for k in NAMES})


def _mp_taylor(f, x0, n, dps=60):
    with mp.workdps(dps):
        return mp.taylor(f, mp.mpf(x0), n - 1)


def _close(ball, ref, tol=mp.mpf(10) ** -40):
    with mp.workdps(70):
        mid = mp.mpf(ball.mid().str(60, radius=False))
        rad = mp.mpf(ball.rad().str(10, radius=False))
        return abs(mid - ref) <= rad + tol


def _fq(s):
    f = Fraction(s)
    return fmpq(f.numerator, f.denominator)


def _quotient_reference(mpf_funcs, q, d):
    with mp.workdps(60):
        q, d = mp.mpf(q), mp.mpf(d)
        return {k: (f(q + d) - f(q)) / d for k, f in mpf_funcs.items()}


# ---- the library behaviour that caused the defect ---------------------------------------------------------------------
def test_python_flint_truncates_series_at_ctx_cap():
    with cap(10):
        assert len(arb_series([arb(1), 1], prec=16).exp().coeffs()) == 10
    with cap(16):
        assert len(arb_series([arb(1), 1], prec=16).exp().coeffs()) == 16


# ---- series length and high coefficients against independent references -------------------------------------------------
def test_generator_series_have_the_requested_length_and_correct_high_coefficients(mpf_funcs):
    n = 24
    with cap(10), prec(128):
        c = b1_cert._taylor(arb(1), n)
        assert ctx.cap == 10
    for k in NAMES:
        assert len(c[k]) == n, k
        ref = _mp_taylor(mpf_funcs[k], 1, n)
        assert any(not c[k][j].contains(0) for j in range(10, n)), k            # nonzero above index 10
        for j in range(n):
            assert _close(c[k][j], ref[j]), (k, j, c[k][j].str(20), mp.nstr(ref[j], 20))


def test_checker_series_have_the_requested_length_and_correct_high_coefficients(model, mpf_funcs):
    n = b1_check.N_CHECK + 3
    with cap(10), prec(b1_check.CHECK_PREC):
        c = model.taylor(arb(1), n)
        assert ctx.cap == 10
    for k in NAMES:
        assert len(c[k]) == n, k
        ref = _mp_taylor(mpf_funcs[k], 1, n)
        assert any(not c[k][j].contains(0) for j in range(10, n)), k
        for j in range(n):
            assert _close(c[k][j], ref[j]), (k, j, c[k][j].str(20), mp.nstr(ref[j], 20))


def test_high_coefficients_against_a_cauchy_integral(mpf_funcs):
    """c_10..c_23 of every function at r = 1 by the Cauchy integral formula (mpmath, contour radius 1/2): a second
    reference that shares nothing with python-flint's series arithmetic or with mpmath's finite differences."""
    n = 24
    with cap(10), prec(128):
        c = b1_cert._taylor(arb(1), n)
    for k in NAMES:
        with mp.workdps(50):
            ref = mp.taylor(mpf_funcs[k], 1, n - 1, method="quad", radius=mp.mpf(1) / 2)
        for j in range(10, n):
            assert _close(c[k][j], mp.re(ref[j]), mp.mpf(10) ** -35), (k, j, c[k][j].str(20), mp.nstr(ref[j], 20))


# ---- the diagnostic point (q, delta) = (1.9, 0.9) ----------------------------------------------------------------------
def _old_generator_taylor(x, n):
    """V0.4-dev.3 b1_cert._taylor, verbatim (no ctx.cap, zero padding), kept here only to reproduce the defect."""
    s = arb_series([x, 1], prec=n)
    out = {}
    for k, v in b1_cert._funcs(s).items():
        c = list(v.coeffs())
        out[k] = c + [arb(0)] * (n - len(c))
    return out


def _old_checker_taylor(self, x, n):
    """V0.4-dev.3 b1_check.Model.taylor, verbatim."""
    s = arb_series([x, 1], prec=n)
    out = {}
    for k, v in self.values(s).items():
        c = list(v.coeffs())
        out[k] = c + [arb(0)] * (n - len(c))
    return out


def _contains(ball, ref):
    with mp.workdps(70):
        return ball.contains(arb(mp.nstr(ref, 55)))


def test_diagnostic_point_old_generator_excluded_the_reference(mpf_funcs, monkeypatch):
    ref = _quotient_reference(mpf_funcs, "1.9", "0.9")
    monkeypatch.setattr(b1_cert, "_taylor", _old_generator_taylor)
    with cap(10), prec(128):
        old = b1_cert.divided(arb(fmpq(19, 10)), arb(fmpq(9, 10)), "near")[0]
    assert [k for k in NAMES if not _contains(old[k], ref[k])]          # the defect, reproduced


def test_diagnostic_point_corrected_generator_contains_the_reference(mpf_funcs):
    ref = _quotient_reference(mpf_funcs, "1.9", "0.9")
    with cap(10), prec(128):
        new = b1_cert.divided(arb(fmpq(19, 10)), arb(fmpq(9, 10)), "near")[0]
    for k in NAMES:
        assert _contains(new[k], ref[k]), (k, new[k].str(25), mp.nstr(ref[k], 25))


def test_diagnostic_point_old_checker_excluded_the_reference(model, mpf_funcs, monkeypatch):
    ref = _quotient_reference(mpf_funcs, "1.9", "0.9")
    monkeypatch.setattr(b1_check.Model, "taylor", _old_checker_taylor)
    with cap(10), prec(b1_check.CHECK_PREC):
        old = model.dd(arb(fmpq(19, 10)), arb(fmpq(9, 10)), "near")[0]
    assert [k for k in NAMES if not _contains(old[k], ref[k])]


def test_diagnostic_point_corrected_checker_contains_the_reference(model, mpf_funcs):
    ref = _quotient_reference(mpf_funcs, "1.9", "0.9")
    with cap(10), prec(b1_check.CHECK_PREC):
        new = model.dd(arb(fmpq(19, 10)), arb(fmpq(9, 10)), "near")[0]
    for k in NAMES:
        assert _contains(new[k], ref[k]), (k, new[k].str(25), mp.nstr(ref[k], 25))


def test_divided_differences_contain_the_reference_on_a_near_grid(model, mpf_funcs):
    """Thin points across the near regime (delta up to 5/4): every enclosure contains the 60-digit quotient."""
    for q, d in (("0.3", "1.0"), ("1.2", "1.1"), ("1.6", "1.2"), ("1.9", "0.9"), ("2.0", "0.05")):
        ref = _quotient_reference(mpf_funcs, q, d)
        Q, D = arb(_fq(q)), arb(_fq(d))
        with cap(10), prec(128):
            g = b1_cert.divided(Q, D, "near")[0]
        with cap(10), prec(b1_check.CHECK_PREC):
            c = model.dd(Q, D, "near")[0]
        for k in NAMES:
            assert _close(g[k], ref[k], mp.mpf(10) ** -25) and _close(c[k], ref[k], mp.mpf(10) ** -25), (q, d, k)


# ---- ctx.cap restoration, truncation detection, exact-zero padding ----------------------------------------------------------
def test_ctx_cap_is_restored_after_the_call_and_after_an_exception(model, monkeypatch):
    for start in (10, 7, 40):
        with cap(start), prec(128):
            b1_cert._taylor(arb(1), 19)
            assert ctx.cap == start
            model.taylor(arb(1), 23)
            assert ctx.cap == start

    def boom(*a, **k):
        raise RuntimeError("boom")
    with cap(10):
        monkeypatch.setattr(b1_cert, "_funcs", boom)
        with pytest.raises(RuntimeError):
            b1_cert._taylor(arb(1), 19)
        assert ctx.cap == 10
        monkeypatch.setattr(model, "values", boom)
        with pytest.raises(RuntimeError):
            model.taylor(arb(1), 23)
        assert ctx.cap == 10


def test_an_unraised_capacity_is_detected_not_zero_padded(model, monkeypatch):
    """If the capacity were not raised (the V0.4-dev.3 situation), both routines must raise instead of padding."""
    @contextlib.contextmanager
    def fake_capacity(n):
        yield n                                     # claims n, leaves ctx.cap at 10
    monkeypatch.setattr(b1_cert, "_series_capacity", fake_capacity)

    class FakeLength:
        def __init__(self, n):
            self.n = n

        def __enter__(self):
            return self.n

        def __exit__(self, *a):
            return False
    monkeypatch.setattr(b1_check, "SeriesLength", FakeLength)
    with cap(10), prec(128):
        with pytest.raises(b1_cert.SeriesTruncationError):
            b1_cert._taylor(arb(1), 16)
        with pytest.raises(b1_check.TruncatedSeries):
            model.taylor(arb(1), 20)


def test_zero_padding_only_for_exact_trailing_zeros(model, monkeypatch):
    # a genuine polynomial: python-flint trims its exact trailing zeros, which are restored
    monkeypatch.setattr(b1_cert, "_funcs", lambda x: {"p": x * x})
    with cap(10), prec(128):
        c = b1_cert._taylor(arb(3), 12)["p"]
    assert c[0] == 9 and c[1] == 6 and c[2] == 1
    assert len(c) == 12 and all(v == 0 for v in c[3:])
    # a short list whose missing coefficients are not zero must be rejected
    calls = []

    def short_then_full(x, n):
        calls.append(n)
        full = [arb(1)] * n
        return {"p": full[:5] if len(calls) == 1 else full}
    monkeypatch.setattr(b1_cert, "_series_coefficients", short_then_full)
    with pytest.raises(b1_cert.SeriesTruncationError):
        b1_cert._taylor(arb(1), 12)
    # the checker
    monkeypatch.setattr(model, "f", {**model.f, **{k: b1_check.R_ ** 2 for k in NAMES}})
    with cap(10), prec(160):
        cc = model.taylor(arb(3), 12)
    assert all(len(cc[k]) == 12 and all(v == 0 for v in cc[k][3:]) for k in NAMES)
    seen = []

    def raw_short_then_full(x, n):
        seen.append(n)
        return {k: ([arb(1)] * n)[:5] if len(seen) == 1 else [arb(1)] * n for k in NAMES}
    monkeypatch.setattr(model, "_raw_series", raw_short_then_full)
    with pytest.raises(b1_check.TruncatedSeries):
        model.taylor(arb(1), 12)


# ---- the historical certificate and the erratum records -------------------------------------------------------------------
def test_historical_B1_certificate_is_untouched():
    f = DATA / "B1_kappa_certificate.json"
    if not f.exists():
        pytest.skip("data/ not generated")
    assert hashlib.sha256(f.read_bytes()).hexdigest() == HISTORICAL_FILE_SHA256
    cert = json.loads(f.read_text())
    assert b1_check.semantic_hash(cert) == HISTORICAL_SEMANTIC == cert["provenance"]["semantic_sha256"]
    assert (DATA / "B1_CERTIFICATE_SEMANTIC.sha256").read_text().split()[0] == HISTORICAL_SEMANTIC
    assert cert["min_lower_bound"] == "1311719/536870912" and cert["n_boxes"] == 222


def test_recorded_erratum_report():
    p = DATA / "B1_ERRATUM_report.json"
    if not p.exists():
        pytest.skip("erratum report not generated")
    d = json.loads(p.read_text())
    h = d["historical_certificate_replay"]
    assert h["ok"] and h["semantic_sha256"] == HISTORICAL_SEMANTIC and h["failures"] == []
    assert h["newton_confirmed"] == h["carrier_confirmed"] == h["boxes_checked"] == 222
    assert h["endpoints_accepted"] and h["min_lower_bound"] == "1311719/536870912"
    f = d["fresh_corrected_rebuild"]
    assert f["passes_corrected_checker"] and f["n_boxes"] == 222 and f["lemma_K_claim_identical"]
    assert f["stored_as"] != "data/B1_kappa_certificate.json"
    b = d["B2_3_non_taylor_cross_check"]
    assert b["ok"] and b["curve_reverified_b1_boxes"] == b["boxes_checked"] == 222
    assert not b["b1_modules_imported"] and b["static"]["imports_project_modules"] == []
    dg = d["diagnostic_point"]
    assert dg["old_generator_excludes"] and not dg["corrected_generator_excludes"]
    assert dg["old_checker_excludes"] and not dg["corrected_checker_excludes"]


def test_corrected_rebuild_is_stored_separately_with_its_hash():
    p = DATA / "B1_ERRATUM_corrected_rebuild_certificate.json"
    if not p.exists():
        pytest.skip("corrected rebuild not generated")
    cert = json.loads(p.read_text())
    h = (DATA / "B1_ERRATUM_CORRECTED_REBUILD_SEMANTIC.sha256").read_text().split()[0]
    assert b1_check.semantic_hash(cert) == h == cert["provenance"]["semantic_sha256"]
    hist = json.loads((DATA / "B1_kappa_certificate.json").read_text())
    for key in ("claim", "statement", "expressions", "expression_sha256", "frozen_inputs"):
        assert cert[key] == hist[key], key
    assert [(b["q_lo"], b["q_hi"]) for b in cert["boxes"]] == [(b["q_lo"], b["q_hi"]) for b in hist["boxes"]]
    assert cert["min_lower_bound"] == hist["min_lower_bound"] and cert["endpoints"] == hist["endpoints"]
    # only near-regime boxes (the code path of the erratum) may differ
    assert all(a == b for a, b in zip(cert["boxes"], hist["boxes"]) if b["regime"] == "far")
