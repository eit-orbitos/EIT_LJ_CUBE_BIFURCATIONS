"""Phase B2.3: Lemma Q, c4_hat > 0 on the closed physical T2g curve. Status: CERTIFIED (computer-assisted; not
independently audited). There is no monotonicity claim, no branch classification and no centre-manifold index here.

Writes:
- data/B2_c4hat_certificate.json and data/B2_CERTIFICATE_SEMANTIC.sha256: the certificate from the generator
  b2_cert.py (128 bits). It imports the hash-pinned B1 curve boxes;
- data/B2_3_check_report.json: the report of the independent checker b2_check.py (192 bits, no Taylor series);
- data/B2_3_method_controls.json: false statements on which the generator and the checker must fail, and positive
  controls on which they must pass.
"""
import json
import pathlib
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import mpmath as mp  # noqa: E402
from flint import arb, ctx, fmpq  # noqa: E402

from cube_bif import STATUS, __version__  # noqa: E402
from cube_bif import b2_carrier as bc  # noqa: E402
from cube_bif import b2_cert as gc  # noqa: E402
from cube_bif import b2_check as ck  # noqa: E402

DATA = ROOT / "data"
FALSE_LEVEL = fmpq(21, 5)          # the false function 21/5 - c4_hat changes sign on the curve
FALSE_BOUND = fmpq(19, 5)          # c4_hat > 19/5 is false at q = 0 (c4_hat(0) = 3.79934)


def _ref():
    d = json.loads((DATA / "B2_carrier.json").read_text())
    return d["endpoint_q0"]["c4_hat"], d["endpoint_corner"]["c4_hat"]


def _contains(E, s):
    return bool(E.contains(arb(s)))


def _fq(x, digits=20):
    r = gc.sp.Rational(mp.nstr(x, digits))
    return fmpq(int(r.p), int(r.q))


# ---- generator-side variants (the certification method applied to false carriers) ----------------------------------------
def _shifted(F):
    out = gc.carrier(F)
    out["c4_hat"] = FALSE_LEVEL - out["c4_hat"]
    return out


def _variant(kind):
    def f(F):
        rho = (F["M12"] if kind == "wrong kernel sign" else -F["M12"]) / F["M22"]
        Qh = sum((gc.b2.Q_BINOM[c] * rho ** c.count("v") * F["Q_" + c] for c in gc.b2.Q_CHANNELS), arb(0))
        bA = sum((gc.b2.B_WEIGHT[c] * rho ** c.count("v") * F["bA_" + c] for c in gc.b2.B_CHANNELS), arb(0))
        bE = sum((gc.b2.B_WEIGHT[c] * rho ** c.count("v") * F["bE_" + c] for c in gc.b2.B_CHANNELS), arb(0))
        n2 = 1 + rho * rho
        eg = {"Eg deleted": 0, "factor 3 -> 2": 2}.get(kind, 3)
        c = (Qh - fmpq(3, 2) * bA * bA - eg * bE * bE / F["hE"]) / (n2 * n2)
        return {"c4_hat": c, "rho": rho, "one_plus_rho2": n2, "hE": F["hE"], "Mh22": F["M22"]}
    return f


def _raw_certify(b1box, depth_max=8):
    """The raw coefficient c4 = q W_q delta c4_hat, certified positive on a B1 box by bisection in q."""
    ctx.prec = gc.PREC
    D = gc.ball(gc.parse_q(b1box["delta_lo"]), gc.parse_q(b1box["delta_hi"]))
    regime = "quotient" if gc.parse_q(b1box["delta_lo"]) > 1 else "symmetric Taylor"
    todo = [(gc.parse_q(b1box["q_lo"]), gc.parse_q(b1box["q_hi"]), 0)]
    while todo:
        lo, hi, d = todo.pop()
        Q = gc.ball(lo, hi)
        c = gc.carrier(gc.divided(Q, D, regime))["c4_hat"]
        WQ = 1 + (-(arb(2).log() / 2) * Q).exp() + (-(arb(3).log() / 2) * Q).exp() / 3
        if Q * WQ * D * c > 0:
            continue
        if d >= depth_max:
            return False, f"q in [{lo}, {hi}]: the enclosure of q W_q delta c4_hat contains 0"
        todo += [((lo + hi) / 2, hi, d + 1), (lo, (lo + hi) / 2, d + 1)]
    return True, None


def generator_controls(b1, ref0, refc, root_q):
    out = []

    def rec(name, required, certified, extra_ok=True, **detail):
        out.append({"side": "generator (b2_cert.py)", "control": name, "required": required, "certified": certified,
                    "as_required": certified == (required == "certify") and extra_ok, **detail})

    pieces, why = gc.certify_b1_box(0, b1["boxes"][0], claim_bound=FALSE_BOUND)
    e0 = gc.endpoint_q0(b1)
    E0 = gc.ball(*[gc.parse_q(s) for s in e0["c4_hat_enclosure"]])
    root_38 = mp.findroot(lambda t_: bc.interior(t_)["c4_hat"] - mp.mpf(19) / 5, (mp.mpf("0.001"), mp.mpf("0.3")),
                          solver="anderson")
    rec("false bound: c4_hat > 19/5 on the first curve box (c4_hat(0) = 3.79934 < 19/5)", "fail", pieces is not None,
        failure=why, root_of_c4_hat_minus_19_5=mp.nstr(root_38, 12))
    rec("false bound: c4_hat > 19/5 at the endpoint q = 0", "fail", bool(E0 > arb(FALSE_BOUND)),
        endpoint_enclosure=e0["c4_hat"])
    failed = []
    for i, bx in enumerate(b1["boxes"]):
        p, why = gc.certify_b1_box(i, bx, carrier_fn=_shifted)
        if p is None:
            failed.append({"b1_index": i, "q": [bx["q_lo"], bx["q_hi"]], "reason": why["reason"]})
    rq = _fq(root_q)
    root_box = next(i for i, bx in enumerate(b1["boxes"]) if gc.parse_q(bx["q_lo"]) <= rq <= gc.parse_q(bx["q_hi"]))
    failed_idx = {f["b1_index"] for f in failed}
    beyond = [i for i, bx in enumerate(b1["boxes"]) if gc.parse_q(bx["q_lo"]) > rq]
    rec("false function: 21/5 - c4_hat on all 222 curve boxes (it vanishes at the root below)", "fail", not failed,
        extra_ok=root_box in failed_idx and all(i in failed_idx for i in beyond),
        root_of_c4_hat_minus_21_5=mp.nstr(root_q, 15), box_containing_the_root=root_box,
        box_containing_the_root_failed=root_box in failed_idx,
        all_boxes_beyond_the_root_failed=all(i in failed_idx for i in beyond), n_boxes_failed=len(failed),
        first_failed_box=failed[0] if failed else None,
        note=("failures start below the root because the generator's box enclosures are wide in the quotient regime "
              "(up to 0.9 near q = 1.35, 0.25 on the first box): it certifies a margin only when it exceeds the "
              "enclosure width, and the recorded lower bounds of the true carrier are correspondingly conservative"))
    for label, i in (("the first curve box (q = 0)", 0), ("the corner box (p = q at q_c)", len(b1["boxes"]) - 1)):
        ok, why = _raw_certify(b1["boxes"][i])
        rec(f"raw (unnormalised) c4 = q W_q delta c4_hat on {label}", "fail", ok, failure=why)
    for kind in ("wrong kernel sign", "Eg deleted", "factor 3 -> 2"):
        f = _variant(kind)
        a = gc.endpoint_q0(b1, carrier_fn=f)
        c = gc.endpoint_corner(b1, carrier_fn=f)
        A = gc.ball(*[gc.parse_q(s) for s in a["c4_hat_enclosure"]])
        C = gc.ball(*[gc.parse_q(s) for s in c["c4_hat_enclosure"]])
        exposed = not _contains(A, ref0) and not _contains(C, refc)
        rec(f"variant '{kind}': its endpoint enclosures must exclude the B2.2 reference values", "fail",
            not exposed, q0_enclosure=a["c4_hat"], corner_enclosure=c["c4_hat"])
    ctx.prec = gc.PREC
    lo, hi = (gc.sp.Rational(s) for s in b1["endpoints"]["corner"]["q_c_enclosure_paper2_lemma_T2"])
    Qc = gc.ball(fmpq(int(lo.p), int(lo.q)), fmpq(int(hi.p), int(hi.q)))
    bad = gc.carrier(gc.funcs(Qc))["c4_hat"]
    rec("corner with values f(q_c) instead of the derivatives f'(q_c): must exclude the B2.2 corner value", "fail",
        _contains(bad, refc), corner_enclosure=bad.str(20))
    good = [gc.certify_b1_box(i, b1["boxes"][i])[0] is not None for i in range(50, 61)]
    rec("positive control: the true carrier on curve boxes 50..60", "certify", all(good))
    return out


# ---- checker-side controls -----------------------------------------------------------------------------------------------
def checker_controls(cert, model, root_q):
    ctx.prec = ck.CHECK_PREC
    out = []

    def rec(name, required, certified, **detail):
        out.append({"side": "checker (b2_check.py)", "control": name, "required": required, "certified": certified,
                    "as_required": certified == (required == "certify"), **detail})

    def box(j):
        b = cert["boxes"][j]
        return (ck._ball(ck._q(b["q_lo"]), ck._q(b["q_hi"])), ck._ball(ck._q(b["delta_lo"]), ck._q(b["delta_hi"])),
                ck._q(b["hE_hat_lower_bound"]), ck._q(b["Mh22_lower_bound"]))

    Q, D, lh, lm = box(0)
    rec("false bound: c4_hat > 19/5 on the first box", "fail", ck.confirm_box(model, Q, D, FALSE_BOUND, lh, lm)[0])
    rq = _fq(root_q)
    j = next(k for k, b in enumerate(cert["boxes"]) if ck._q(b["q_lo"]) <= rq <= ck._q(b["q_hi"]))
    original = ck.carrier_v
    ck.carrier_v = lambda G: FALSE_LEVEL - original(G)
    try:
        Q, D, lh, lm = box(j)
        ok = ck.confirm_box(model, Q, D, fmpq(0), lh, lm)[0]
    finally:
        ck.carrier_v = original
    rec("false function: 21/5 - c4_hat > 0 on the box containing its zero", "fail", ok,
        box={"index": j, "q": [cert["boxes"][j]["q_lo"], cert["boxes"][j]["q_hi"]]})
    for label, j in (("the first box (q = 0)", 0), ("the corner box", len(cert["boxes"]) - 1)):
        Q, D, lh, lm = box(j)
        res = ck.box_carrier(model, Q, D, 64, 32)
        WQ = 1 + (-(arb(2).log() / 2) * Q).exp() + (-(arb(3).log() / 2) * Q).exp() / 3
        rec(f"raw (unnormalised) c4 = q W_q delta c4_hat > 0 on {label}", "fail",
            bool(res is not None and Q * WQ * D * res["c4_hat"] > 0))
    Q, D, lh, lm = box(100)
    rec("positive control: the recorded bounds on box 100", "certify",
        ck.confirm_box(model, Q, D, ck._q(cert["boxes"][100]["c4_hat_lower_bound"]), lh, lm)[0])
    return out


def main():
    t0 = time.time()
    mp.mp.dps = 40
    ref0, refc = _ref()
    cert = gc.build_certificate(ROOT)
    (DATA / "B2_c4hat_certificate.json").write_text(json.dumps(cert, indent=1))
    sh = cert["provenance"]["semantic_sha256"]
    (DATA / "B2_CERTIFICATE_SEMANTIC.sha256").write_text(f"{sh}  B2_c4hat_certificate.json (semantic)\n")
    derived = ck.derive_functions()
    model = ck.Model(derived)
    ok, rep = ck.check(cert, ROOT, stored_semantic_hash=sh, derived=derived, model=model)
    report = {"project_version": __version__, "status": STATUS, "checker": "src/cube_bif/b2_check.py",
              "certificate": "data/B2_c4hat_certificate.json", "ok": ok, **rep}
    (DATA / "B2_3_check_report.json").write_text(json.dumps(report, indent=1))
    root_q = mp.findroot(lambda t_: bc.interior(t_)["c4_hat"] - mp.mpf(21) / 5, mp.mpf("1.0"))
    b1 = gc.load_b1(ROOT)
    controls = generator_controls(b1, ref0, refc, root_q) + checker_controls(cert, model, root_q)
    all_ok = all(c["as_required"] for c in controls)
    (DATA / "B2_3_method_controls.json").write_text(json.dumps(
        {"project_version": __version__, "all_as_required": all_ok, "controls": controls}, indent=1, default=str))
    print(json.dumps({"semantic_sha256": sh, "n_boxes": cert["n_boxes"], "min_lower_bound": cert["min_lower_bound"],
                      "min_lower_bound_decimal": cert["min_lower_bound_decimal"],
                      "min_lower_bound_box": cert["min_lower_bound_box"],
                      "denominator_bounds": cert["denominator_bounds"],
                      "endpoints": {k: v["c4_hat"] for k, v in cert["endpoints"].items()},
                      "independent_check": ok, "check_failures": rep["failures"][:5],
                      "method_controls_as_required": f"{sum(c['as_required'] for c in controls)}/{len(controls)}",
                      "seconds": round(time.time() - t0, 1)}, indent=1))
    return 0 if ok and all_ok else 1


if __name__ == "__main__":
    sys.exit(main())
