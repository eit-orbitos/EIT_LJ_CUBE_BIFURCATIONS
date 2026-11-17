"""Phase B1: exact trilinear structure, normalised cubic carrier, candidate scan, Arb certificate, independent check,
method negative controls and the D3d corroboration.

Writes:
- data/B1_cubic.json: exact formulas, route checks, endpoint limits, scan summary, transversality status and the
  D3d corroboration;
- data/B1_scan.csv: the candidate scan;
- data/B1_kappa_certificate.json and data/B1_CERTIFICATE_SEMANTIC.sha256;
- data/B1_negative_controls.json.
"""
import csv
import json
import pathlib
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import mpmath as mp  # noqa: E402
import sympy as sp  # noqa: E402
from flint import arb, fmpq  # noqa: E402

from cube_bif import STATUS, __version__, b1_cert, b1_check, b1_cubic as b1, t2g  # noqa: E402

DATA = ROOT / "data"


def s(x, n=20):
    return mp.nstr(x, n)


def exact_layer():
    table = b1.trilinear_table()
    nonzero = [(ch, idx) for (ch, idx), v in table.items() if v != 0]
    ind = b1.independent_coefficients()
    basis = {"u": t2g.UH, "v": t2g.VH}
    route2 = {m: bool(sp.simplify(b1.raw24_contract(basis[m[0]][0], basis[m[1]][1], basis[m[2]][2]) - ind[m]) == 0)
              for m in b1.CHANNELS}
    e = b1.critical_vectors()
    x = e[0] * b1.a1 + e[1] * b1.a2 + e[2] * b1.a3
    i3 = sp.expand(b1.raw24_contract(x, x, x) - 6 * b1.kappa_form() * b1.a1 * b1.a2 * b1.a3) == 0
    return {
        "trilinear_values_computed": len(table),
        "nonzero_values": len(nonzero),
        "nonzero_only_on_permutations_of_123": all(sorted(idx) == [0, 1, 2] for _, idx in nonzero),
        "independent_coefficients_generic_psi": {m: str(ind[m]) for m in b1.CHANNELS},
        "kappa_generic": "t_uuu n_u^3 + 3 t_uuv n_u^2 n_v + 3 t_uvv n_u n_v^2 + t_vvv n_v^3",
        "route2_raw24_equals_route1": route2,
        "raw24_cubic_restriction_equals_6_kappa_a1a2a3": bool(i3),
        "difference_form_residuals_zero": {m: b1.difference_form_residual(m) == 0 for m in b1.CHANNELS},
        "g_closed_forms": {m: str(b1.G_CLOSED[m]) for m in b1.CHANNELS},
        "M_closed_form_paper2": [[str(b1.M_CLOSED[i, j]) for j in range(2)] for i in range(2)],
        "factorisation": "kappa = q W_q (p - q) kappa_hat, kappa_hat = sum binom n^.. (g_m(p) - g_m(q))/(p - q)",
        "chart": "n = (1, rho), rho = -Mh12/Mh22; Mh (1, rho)^T = (det Mh / Mh22, 0)^T",
    }


def route3(points=("0.05", "0.3", "1.0", "1.5", "1.8", "2.0")):
    out = []
    for qq in points:
        c = b1.carrier(qq)
        formula = c["q"] * b1.W_num(c["q"]) * c["delta"] * c["kappa_hat"]
        direct = b1.kappa_direct(c["p"], c["q"], 1, c["rho"])
        out.append({"q": qq, "p": s(c["p"]), "kappa_chart_formula": s(formula), "kappa_chart_direct": s(direct),
                    "relative_difference": mp.nstr(abs(direct / formula - 1), 3)})
    return out


def scan_layer(n=400):
    rows = b1.scan(n)
    with open(DATA / "B1_scan.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["q", "delta=p-q", "p", "rho", "Mh22", "kappa_hat", "tau_hat", "tau_tilde", "dDtilde_ddelta",
                    "dP_T/dq"])
        for r in rows:
            w.writerow([s(r["q"], 15), s(r["delta"], 15), s(r["p"], 15), s(r["rho"], 15), s(r["Mh22"], 12),
                        s(r["kappa_hat"], 15), s(r["tau_hat"], 12), s(r["tau_tilde"], 12),
                        s(r["dDtilde_ddelta"], 12), s(r.get("dP_dq", mp.nan), 8)])
    k = [r["kappa_hat"] for r in rows]
    imin = min(range(len(k)), key=lambda i: abs(k[i]))
    return {
        "grid": f"q_k = k q_c / {n}, k = 0..{n}; the last point is the corner limit",
        "min_abs_kappa_hat": s(abs(k[imin]), 15), "at_q": s(rows[imin]["q"], 10),
        "max_kappa_hat": s(max(k), 15),
        "sign_changes_in_chart_gauge": sum(1 for a, b in zip(k, k[1:]) if a * b <= 0),
        "kappa_hat_monotone_increasing": all(b > a for a, b in zip(k, k[1:])),
        "endpoint_q0": s(k[0], 20), "endpoint_corner": s(k[-1], 20),
        "rho_range": [s(min(r["rho"] for r in rows), 10), s(max(r["rho"] for r in rows), 10)],
        "Mh22_range": [s(min(r["Mh22"] for r in rows), 10), s(max(r["Mh22"] for r in rows), 10)],
        "dDtilde_ddelta_range": [s(min(r["dDtilde_ddelta"] for r in rows), 8),
                                 s(max(r["dDtilde_ddelta"] for r in rows), 8)],
        "dP_T_dq_range": [s(min(r["dP_dq"] for r in rows[1:]), 6), s(max(r["dP_dq"] for r in rows[1:]), 6)],
        "tau_tilde_range": [s(min(r["tau_tilde"] for r in rows), 8), s(max(r["tau_tilde"] for r in rows), 8)],
        "status": "VERIFIED-NUMERIC (candidate scan; the certificate is separate)",
    }


def d3d_layer():
    out = []
    for qq in ("0.3", "1.0", "1.8"):
        for rel in ("1e-6", "-1e-6", "1e-7", "-1e-7"):
            r = b1.d3d_branch_point(qq, rel)
            out.append({"q": qq, "rel_mu": rel, "mu": s(r["mu"], 8), "s_predicted": s(r["s_predicted"], 12),
                        "s_found": s(r["s_found"], 12),
                        "relative_difference": mp.nstr(abs(r["s_found"] / r["s_predicted"] - 1), 3),
                        "full_gradient_norm": mp.nstr(r["full_gradient_norm"], 3),
                        "kappa_unit": s(r["kappa_unit"], 12), "tau_unit": s(r["tau_unit"], 12)})
    return out


def method_controls(derived):
    """The same certification method must fail on false or ill-posed claims and pass a true one."""
    est = b1_cert._cached_estimator()
    out = []

    def run(name, qa, qb, require, claim=fmpq(0), carrier=None, base=None):
        t0 = time.time()
        boxes, fail = b1_cert.certify_interval(qa, qb, est, claim_bound=claim, carrier=carrier, base=base,
                                               max_depth=12)
        ok = fail is None
        out.append({"control": name, "interval": [str(qa), str(qb)], "required": require,
                    "certified": ok, "as_required": (ok if require == "certify" else not ok),
                    "failure": fail, "seconds": round(time.time() - t0, 2)})

    def shifted(c0):
        def f(Q, D, reg):
            kh, m22, rho = b1_cert.carrier_enclosure(Q, D, reg)
            return arb(c0) - kh, m22, rho
        return f

    def raw(Q, D, reg):
        kh, m22, rho = b1_cert.carrier_enclosure(Q, D, reg)
        L2, L3 = arb(2).log(), arb(3).log()
        WQ = 1 + (-(L2 / 2) * Q).exp() + (-(L3 / 2) * Q).exp() / 3
        return Q * WQ * D * kh, m22, rho

    def wrong_sign(Q, D, reg):
        val = b1_cert.divided(Q, D, reg)[0]
        rho = val["M12"] / val["M22"]
        kh = val["uuu"] + 3 * rho * val["uuv"] + 3 * rho ** 2 * val["uvv"] + rho ** 3 * val["vvv"]
        return kh, val["M22"], rho

    run("false bound: kappa_hat > 3/1000 on [0, 1/10] (true kappa_hat(0) = 0.0028795)", fmpq(0), fmpq(1, 10),
        "fail", claim=fmpq(3, 1000))
    run("sign change: 9/2000 - kappa_hat on [2/5, 3/5] (positive at 2/5, negative at 3/5)", fmpq(2, 5),
        fmpq(3, 5), "fail", carrier=shifted(fmpq(9, 2000)))
    root = mp.findroot(lambda t_: b1.carrier(t_)["kappa_hat"] - mp.mpf(9) / 2000, mp.mpf("0.47"))
    out[-1]["root_of_9/2000-kappa_hat"] = s(root, 12)
    run("raw kappa (not normalised) on [0, 1/100]: vanishes at q = 0", fmpq(0), fmpq(1, 100), "fail", carrier=raw)
    run("raw kappa (not normalised) on the corner box: vanishes at q_c", b1_cert.CORNER[0], b1_cert.CORNER[1],
        "fail", carrier=raw, base=[b1_cert.CORNER[0], b1_cert.CORNER[1]])
    run("wrong kernel vector: rho = +Mh12/Mh22 on [1/2, 1]", fmpq(1, 2), fmpq(1), "fail", carrier=wrong_sign)
    run("positive control: the true carrier on [1/2, 1]", fmpq(1, 2), fmpq(1), "certify")
    return out


def main():
    t0 = time.time()
    mp.mp.dps = 40
    out = {"project": "EIT-LJ Cube Bifurcations (Paper 3)", "version": __version__, "status": STATUS,
           "phase": "B1", "exact": exact_layer(), "route3_direct_differentiation": route3()}
    qc = b1.corner_limit((mp.mpf(b1.QC_LO) + mp.mpf(b1.QC_HI)) / 2)
    c0 = b1.carrier(0)
    out["endpoint_limits"] = {
        "q->0+": {"P_T(0)": s(c0["p"], 25), "rho": s(c0["rho"], 20), "kappa_hat": s(c0["kappa_hat"], 20),
                  "raw_kappa": "q W_q (p - q) kappa_hat -> 0 linearly (factor q)"},
        "q->q_c-": {"q_c": s(qc["q"], 25), "rho_c": s(qc["rho"], 20), "kappa_hat": s(qc["kappa_hat"], 20),
                    "tau_tilde": s(qc["tau_tilde"], 15),
                    "raw_kappa": "q W_q (p - q) kappa_hat -> 0 linearly (p - q = 2(q_c - q) + O((q_c - q)^2), "
                                 "Paper 2 Prop. supplementary (iii))"},
    }
    out["scan"] = scan_layer()
    out["transversality"] = {
        "status": "FROZEN INPUT + VERIFIED-EXACT",
        "argument": ("tau = n^T dK/dp n = q W_q n^T M'(P_T(q)) n (unit n). On the curve N = M(p) - M(q) is singular "
                     "symmetric with kernel n, so adj N = tr(N) n n^T and dD/dp = tr(N) n^T M'(p) n. Paper 2 "
                     "Lemma T1: tr K > 0, so tr N > 0; Lemma T3: dD/dp(P_T(q), q) < 0 for 0 <= q < q_c. Hence "
                     "tau < 0 for every 0 < q < q_c."),
        "normalised_near_corner": "tau_hat = n^T M'(p) n = (p - q) tau_tilde, tau_tilde -> n_c^T M''(q_c) n_c / 2",
    }
    out["d3d_corroboration"] = d3d_layer()
    derived = b1_check.derive_functions()
    cert = b1_cert.build_certificate(ROOT)
    (DATA / "B1_kappa_certificate.json").write_text(json.dumps(cert, indent=1))
    sh = cert["provenance"]["semantic_sha256"]
    (DATA / "B1_CERTIFICATE_SEMANTIC.sha256").write_text(f"{sh}  B1_kappa_certificate.json (semantic)\n")
    ok, rep = b1_check.check(cert, sh, derived=derived)
    out["certificate"] = {"n_boxes": cert["n_boxes"], "max_depth_used": cert["max_depth_used"],
                          "min_lower_bound": cert["min_lower_bound"],
                          "min_lower_bound_decimal": cert["min_lower_bound_decimal"],
                          "semantic_sha256": sh, "independent_check": {"ok": ok, **rep}}
    controls = method_controls(derived)
    (DATA / "B1_negative_controls.json").write_text(json.dumps(
        {"controls": controls, "all_as_required": all(c["as_required"] for c in controls)}, indent=1, default=str))
    out["negative_controls_all_as_required"] = all(c["as_required"] for c in controls)
    out["seconds"] = round(time.time() - t0, 1)
    (DATA / "B1_cubic.json").write_text(json.dumps(out, indent=1, default=str))
    print(json.dumps({"certificate": out["certificate"], "controls": out["negative_controls_all_as_required"],
                      "scan": {k: out["scan"][k] for k in ("min_abs_kappa_hat", "sign_changes_in_chart_gauge")},
                      "seconds": out["seconds"]}, indent=1, default=str))
    return 0 if ok and out["negative_controls_all_as_required"] else 1


if __name__ == "__main__":
    sys.exit(main())
