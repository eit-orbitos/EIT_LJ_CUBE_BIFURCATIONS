"""Diagnostic found during Phase B2.3: python-flint truncates every arb_series at ctx.cap (default 10), whatever
prec= is passed. The B1 generator (b1_cert._taylor, N = 16) and the B1 checker (b1_check.Model.taylor, N = 20) ask
for longer series and pad the returned coefficients with zeros, so their near-regime Taylor models silently drop the
coefficients from index 10 on, including the remainder. This script measures the effect and re-checks the stored B1
certificate. It reads B1's code and data and modifies neither.

Writes data/B2_3_B1_series_cap_diagnostic.json.
"""
import json
import pathlib
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import flint  # noqa: E402
from flint import arb, arb_series, ctx, fmpq  # noqa: E402

from cube_bif import __version__  # noqa: E402
from cube_bif import b1_cert, b1_check  # noqa: E402

DATA = ROOT / "data"


def _set_cap(n):
    old = ctx.cap
    ctx.cap = n
    return old


def series_truncation():
    out = {"python-flint": flint.__version__, "default_ctx_cap": ctx.cap}
    old = _set_cap(10)
    try:
        out["exp series, prec=16, ctx.cap=10: coefficients returned"] = len(arb_series([arb(1), 1], prec=16).exp().coeffs())
        ctx.cap = 16
        out["exp series, prec=16, ctx.cap=16: coefficients returned"] = len(arb_series([arb(1), 1], prec=16).exp().coeffs())
    finally:
        ctx.cap = old
    return out


def b1_taylor_model():
    """Coefficients c_10..c_15 of B1's generator model at r = 1 (thin): zero-padded under the default cap."""
    ctx.prec = 128
    old = _set_cap(10)
    try:
        short = b1_cert._taylor(arb(1), 16)
        ctx.cap = 32
        full = b1_cert._taylor(arb(1), 16)
    finally:
        ctx.cap = old
    dropped = max(abs(full[k][j]).upper() for k in full for j in range(10, 16))
    zero = all(short[k][j] == 0 for k in short for j in range(10, 16))
    agree = all(short[k][j].overlaps(full[k][j]) for k in short for j in range(10))
    return {"coefficients 10..15 returned as exact zeros (default cap)": zero,
            "coefficients 0..9 agree with the complete series": agree,
            "largest dropped |c_j| (j = 10..15, any function)": arb(dropped).str(6)}


def near_divided_difference(q="1.9", d="0.9"):
    """B1's near-regime divided difference at a thin point against the plain quotient (f(q + d) - f(q))/d at 256 bits."""
    Q, D = arb(fmpq(19, 10)), arb(fmpq(9, 10))
    old = _set_cap(10)
    try:
        ctx.prec = 128
        short = b1_cert.divided(Q, D, "near")[0]
        ctx.cap = 32
        full = b1_cert.divided(Q, D, "near")[0]
    finally:
        ctx.cap = old
    ctx.prec = 256
    fq, fp = b1_cert._funcs(Q), b1_cert._funcs(Q + D)
    ref = {k: (fp[k] - fq[k]) / D for k in fq}
    ctx.prec = 128
    miss = [k for k in short if not short[k].overlaps(ref[k])]
    worst = max(short, key=lambda k: abs(short[k] - ref[k]).upper())
    return {"point": {"q": q, "delta": d},
            "functions whose default-cap enclosure excludes the quotient value": miss,
            "worst function": worst, "default-cap enclosure": short[worst].str(25),
            "quotient value (256 bits)": ref[worst].str(25),
            "complete-series enclosure (cap 32)": full[worst].str(25),
            "complete-series enclosures all contain the quotient values": all(full[k].overlaps(ref[k]) for k in full)}


def recheck_stored():
    cert = json.loads((DATA / "B1_kappa_certificate.json").read_text())
    h = (DATA / "B1_CERTIFICATE_SEMANTIC.sha256").read_text().split()[0]
    derived = b1_check.derive_functions()
    out = {}
    for cap in (10, 32):
        old = _set_cap(cap)
        try:
            ok, rep = b1_check.check(cert, h, derived=derived)
        finally:
            ctx.cap = old
        out[f"stored B1 certificate, B1 checker with ctx.cap = {cap}"] = {
            "ok": ok, "newton_confirmed": rep["newton_confirmed"], "carrier_confirmed": rep["carrier_confirmed"],
            "boxes_checked": rep["boxes_checked"], "boxes_refined_by_checker": rep["boxes_refined_by_checker"],
            "failures": rep["failures"]}
    old = _set_cap(32)
    try:
        fresh = b1_cert.build_certificate(ROOT)
        ok, rep = b1_check.check(fresh, fresh["provenance"]["semantic_sha256"], derived=derived)
    finally:
        ctx.cap = old
    out["fresh B1 build with ctx.cap = 32"] = {
        "semantic_sha256": fresh["provenance"]["semantic_sha256"], "stored_semantic_sha256": h,
        "same": fresh["provenance"]["semantic_sha256"] == h,
        "boxes_differing_from_stored": sum(a != b for a, b in zip(fresh["boxes"], cert["boxes"])),
        "n_boxes": fresh["n_boxes"], "min_lower_bound": fresh["min_lower_bound"],
        "stored_min_lower_bound": cert["min_lower_bound"], "passes_B1_checker_with_cap_32": ok}
    return out


def main():
    t0 = time.time()
    out = {"project_version": __version__, "finding": __doc__.split("\n\n")[0].replace("\n", " "),
           "series_truncation": series_truncation(), "b1_generator_taylor_model": b1_taylor_model(),
           "b1_near_divided_difference": near_divided_difference(), "stored_certificate": recheck_stored()}
    rep = DATA / "B2_3_check_report.json"
    if rep.exists():
        r = json.loads(rep.read_text())
        out["B2.3 checker (no Taylor series), imported B1 delta-balls re-verified"] = (
            f"{r['curve_reverified_b1_boxes']}/{r['boxes_checked']}")
    s = out["stored_certificate"]
    out["conclusion"] = (
        "The defect is in the B1 code path, not in the stored B1 data: the stored certificate passes B1's own checker "
        "with complete series (ctx.cap = 32) as well as with the default cap, and the B2.3 checker re-verifies every "
        "imported delta-ball without Taylor series. A corrected generator produces different but equally valid bytes "
        "(another semantic hash), so the B1 test that compares fresh and stored semantic hashes would fail after a fix."
        if s["stored B1 certificate, B1 checker with ctx.cap = 32"]["ok"] else
        "The stored B1 certificate does NOT pass B1's checker with complete series: B1 must be re-examined.")
    out["proposed_erratum (not applied; B1 is audited and unchanged here)"] = [
        "b1_cert._taylor and b1_check.Model.taylor: set ctx.cap to the requested length for the call and assert that "
        "no returned series is longer than requested (never pad a truncated series).",
        "Keep the audited certificate data/B1_kappa_certificate.json (semantic 616817fc...8518c6), which the corrected "
        "checker accepts; replace the fresh-versus-stored hash test by 'the fresh build passes the corrected checker' "
        "and 'the stored certificate passes the corrected checker'.",
        "Add a regression test on the series length; record the erratum in NOTES.md section 5 and the audit folder; "
        "a short targeted re-audit of the erratum is a gate decision."]
    (DATA / "B2_3_B1_series_cap_diagnostic.json").write_text(json.dumps(out, indent=1, default=str))
    print(json.dumps(out, indent=1, default=str))
    print("seconds", round(time.time() - t0, 1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
