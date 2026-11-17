"""Phase B2.2: the normalised D2h quartic carrier c4_hat on the closed physical T2g curve (VERIFIED-NUMERIC /
RECONNAISSANCE). No certificate, no branch classification, no centre-manifold index.

Writes:
- data/B2_carrier.json: exact endpoint data, refined q_c and P_T(0), both endpoint formulations with every
  contribution (45 digits), the corner expression's structure, the scan summary, conditioning, endpoint approach,
  the independent-route comparison;
- data/B2_scan.csv: 401 rows on q_k = k q_c/400 (k = 0: the q = 0 formulation; k = 400: the corner formulation);
- data/B2_falsification.json: deliberately false statements and whether they are exposed.
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

from cube_bif import STATUS, __version__, b1_cubic as b1, b2_carrier as bc  # noqa: E402

DATA = ROOT / "data"
INTERIOR = ("0.001", "0.5", "1.0", "1.5", "2.0", "2.019")


def s(x, n=20):
    return mp.nstr(x, n)


def endpoint_record(d, n=45):
    keys = ("q", "p", "rho", "one_plus_rho2", "Mh22", "hE", "hA", "Q", "A1g", "Eg", "c4_hat", "Q_chart", "bA_chart",
            "bE_chart", "det_Mh", "kernel_residual")
    return {k: s(d[k], n) for k in keys}


def exact_layer(qc):
    cs = bc.corner_symbolic()
    with mp.workdps(60):
        den = {k: s(sp.lambdify((bc.r, bc.Xr, bc.Yr), v, "mpmath")(qc, mp.power(2, -qc / 2), mp.power(3, -qc / 2)), 25)
               for k, v in cs["denominators"].items()}
    return {
        "g_at_zero": {k: str(v) for k, v in bc.g_at_zero().items()},
        "M_at_zero": [[str(bc.M_at_zero()[i, j]) for j in range(2)] for i in range(2)],
        "q0_formulation": "f_hat = (f(p0) - f(0))/p0 with the exact f(0); Mh = (M(p0) - M(0))/p0; p0 = P_T(0) is the "
                          "root of det[M(p) - M(0)] = 0 in Paper 2's certified enclosure",
        "corner_formulation": "f_hat = f'(q_c) from exact derivative closed forms (dX/dr = -(log2/2)X, "
                              "dY/dr = -(log3/2)Y); rho_c = -M'12/M'22; q_c is the root of det M'(r) = 0 in Paper 2's "
                              "certified enclosure",
        "g_prime_closed_forms": {k: str(v) for k, v in bc.g_prime_closed().items()},
        "M_prime_closed_form": [[str(bc.M_prime_closed()[i, j]) for j in range(2)] for i in range(2)],
        "corner_expression_free_symbols": sorted(str(x) for x in cs["free_symbols"]),
        "corner_expression_contains_p_or_q": bool({bc.ps.p_, bc.ps.q_} & cs["free_symbols"]),
        "corner_denominators_at_qc": den,
        "limit_potentials": {
            "q -> 0": "phi/q -> 7/(3 p W_p) r^-p + log r (up to a constant); c4(phi_0) = (7/3) p0 c4_hat(0)",
            "corner": "phi/(p - q) -> -(1/q + W'_q/W_q + log r) r^-q at p = q; c4(phi_c) = q_c W_qc c4_hat(q_c)"},
    }


def write_scan(rows):
    with open(DATA / "B2_scan.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["k", "formulation", "q", "p=P_T(q)", "delta=p-q", "rho", "Q_hat", "A1g_term=-(3/2)bA_hat^2",
                    "Eg_term=-3bE_hat^2/hE_hat", "c4_hat", "hE_hat", "Mh22", "1+rho^2", "dDtilde_ddelta", "dP_T/dq",
                    "kernel_residual"])
        for k, x in enumerate(rows):
            w.writerow([k, x["formulation"], s(x["q"], 22), s(x["p"], 22), s(x["delta"], 22), s(x["rho"], 18),
                        s(x["Q"], 22), s(x["A1g"], 22), s(x["Eg"], 22), s(x["c4_hat"], 22), s(x["hE"], 18),
                        s(x["Mh22"], 18), s(x["one_plus_rho2"], 18), s(x["dDtilde_ddelta"], 15),
                        s(x.get("dP_dq", mp.nan), 12), s(x["kernel_residual"], 3)])


def summary_record(sm):
    return {"n_points": sm["n_points"],
            "min_c4_hat": {"value": s(sm["min"][0], 25), "q": s(sm["min"][1], 25), "row": sm["min"][2]},
            "max_c4_hat": {"value": s(sm["max"][0], 25), "q": s(sm["max"][1], 25), "row": sm["max"][2]},
            "smallest_abs_c4_hat": {"value": s(sm["smallest_abs"][0], 25), "q": s(sm["smallest_abs"][1], 25),
                                    "row": sm["smallest_abs"][2]},
            "sign_changes": sm["sign_changes"], "all_positive": sm["all_positive"],
            "strictly_increasing_on_grid": sm["strictly_increasing_on_grid"],
            "grid_turning_points": sm["grid_turning_points"],
            "min_increment": s(sm["min_increment"], 6), "max_increment": s(sm["max_increment"], 6),
            "denominator_minima": {k: {"min_abs": s(v[0], 20), "q": s(v[1], 20)}
                                   for k, v in sm["denominator_minima"].items()},
            "max_kernel_residual": s(sm["max_kernel_residual"], 3),
            "contribution_ranges": {k: [s(a, 15), s(b, 15)] for k, (a, b) in sm["contribution_ranges"].items()}}


def approach(qc, e0, ec):
    out = {"q_to_0": [], "q_to_qc": []}
    for j in (2, 4, 6, 8):
        x = bc.interior(mp.mpf(10) ** (-j))
        out["q_to_0"].append({"q": f"1e-{j}", "c4_hat": s(x["c4_hat"], 25),
                              "(c4_hat - c4_hat(0))/q": s((x["c4_hat"] - e0["c4_hat"]) / x["q"], 12)})
    for j in (2, 4, 6, 8):
        x = bc.interior(qc - mp.mpf(10) ** (-j))
        out["q_to_qc"].append({"q_c - q": f"1e-{j}", "delta": s(x["delta"], 10), "c4_hat": s(x["c4_hat"], 25),
                               "(c4_hat - c4_hat(q_c))/(q_c - q)^2":
                                   s((x["c4_hat"] - ec["c4_hat"]) / (qc - x["q"]) ** 2, 12)})
    return out


def main():
    t0 = time.time()
    with mp.workdps(100):
        qc = bc.refine_qc(100)
        p0 = bc.refine_p0(100)
    with mp.workdps(80):
        e0 = bc.endpoint_q0(p0)
        ec = bc.corner(qc)
        e0r, ecr = endpoint_record(e0), endpoint_record(ec)
        checks = {"q_c_in_paper2_enclosure": mp.mpf(bc.QC_LO) <= qc <= mp.mpf(bc.QC_HI),
                  "p0_in_paper2_enclosure": mp.mpf(bc.PT0_LO) <= p0 <= mp.mpf(bc.PT0_HI),
                  "p0_in_paper2_audit_enclosure": mp.mpf(bc.PT0_AUDIT_LO) <= p0 <= mp.mpf(bc.PT0_AUDIT_HI)}
    print(f"endpoints: c4_hat(0) = {s(e0['c4_hat'], 25)}, c4_hat(q_c) = {s(ec['c4_hat'], 25)} ({time.time() - t0:.1f} s)")
    ex = exact_layer(qc)
    with mp.workdps(50):
        rows = bc.scan(400, qc=qc, p0=p0)
        sm = bc.scan_summary(rows)
        write_scan(rows)
        print(f"scan: {len(rows)} rows, min {s(sm['min'][0], 12)} at q = {s(sm['min'][1], 6)}, "
              f"max {s(sm['max'][0], 12)} at q = {s(sm['max'][1], 6)} ({time.time() - t0:.1f} s)")
        appr = approach(qc, e0, ec)
        comp, indep, raw_series = [], {}, []
        for qq in INTERIOR:
            row = bc.interior(qq)
            ind = bc.independent("two_term", row["p"], q=row["q"])
            indep[qq] = (row, ind["c4_hat"])
            comp.append({"point": f"q = {qq}", "primary_c4_hat": s(row["c4_hat"], 30),
                         "independent_c4_hat": s(ind["c4_hat"], 30),
                         "relative_difference": s(abs(ind["c4_hat"] / row["c4_hat"] - 1), 3),
                         "own_curve_point_minus_primary": s(ind["curve_parameter"] - row["p"], 3),
                         "zero_eigenvalues": ind["n_small"], "b_on_kernel": s(ind["b_on_small"], 3)})
        for lab, kind, row, guess in (("q = 0", "q0", rows[0], p0 * (1 + mp.mpf("1e-3"))),
                                      ("corner", "corner", rows[-1], qc * (1 + mp.mpf("1e-3")))):
            ind = bc.independent(kind, guess)
            indep["q0" if kind == "q0" else "corner"] = (row, ind["c4_hat"])
            ref = p0 if kind == "q0" else qc
            comp.append({"point": lab, "primary_c4_hat": s(row["c4_hat"], 30),
                         "independent_c4_hat": s(ind["c4_hat"], 30),
                         "relative_difference": s(abs(ind["c4_hat"] / row["c4_hat"] - 1), 3),
                         "own_curve_point_minus_refined": s(ind["curve_parameter"] - ref, 3),
                         "zero_eigenvalues": ind["n_small"], "b_on_kernel": s(ind["b_on_small"], 3),
                         "limit_potential_equilibrium_gradient": s(ind["equilibrium_gradient"], 3)})
        print(f"independent route: max rel {max(mp.mpf(c['relative_difference']) for c in comp)} "
              f"({time.time() - t0:.1f} s)")
        for qq in ("1e-3", "1e-5", "1e-7"):
            raw_series.append(bc.raw_c4_unnormalised(qq, bc.interior(qq)["p"]))
        for d in ("1e-3", "1e-5"):
            qq = qc - mp.mpf(d)
            raw_series.append(bc.raw_c4_unnormalised(qq, bc.interior(qq)["p"]))
        fals = bc.falsification_report(rows, indep, raw_series)
    with mp.workdps(60):
        nl = {}
        for lab, kind, guess in (("q = 0", "q0", p0), ("corner", "corner", qc)):
            r3 = bc.independent_nonlinear(kind, guess)
            ref = e0["c4_hat"] if kind == "q0" else ec["c4_hat"]
            nl[lab] = {"c4_hat": s(r3["c4_hat"], 30), "relative_difference": s(abs(r3["c4_hat"] / ref - 1), 3),
                       "richardson_error_relative": s(r3["richardson_error"] / ref, 3)}
    print(f"nonlinear endpoint checks done ({time.time() - t0:.1f} s)")
    ok = (all(checks.values()) and not ex["corner_expression_contains_p_or_q"]
          and sm["all_positive"] and sm["n_points"] == 401
          and all(mp.mpf(c["relative_difference"]) < mp.mpf("1e-40") for c in comp)
          and all(c["zero_eigenvalues"] == 9 for c in comp)
          and all(mp.mpf(v["relative_difference"]) < mp.mpf("1e-28") for v in nl.values())
          and all(f["exposed"] for f in fals))
    rec = {"project_version": __version__, "status": STATUS,
           "label": "B2.2 = VERIFIED-NUMERIC / RECONNAISSANCE (exact identities marked in NOTES §7)",
           "q_c_refined_100_digits": s(qc, 100), "p0_refined_100_digits": s(p0, 100),
           "frozen_enclosures": {"q_c": [bc.QC_LO, bc.QC_HI], "P_T(0)": [bc.PT0_LO, bc.PT0_HI],
                                 "P_T(0) Paper 2 audit": [bc.PT0_AUDIT_LO, bc.PT0_AUDIT_HI]},
           "enclosure_checks": checks,
           "endpoint_q0": e0r, "endpoint_corner": ecr, "exact": ex,
           "scan_working_digits": 50, "scan": summary_record(sm), "endpoint_approach": appr,
           "independent_route": comp, "independent_nonlinear_endpoints": nl,
           "falsification_file": "data/B2_falsification.json",
           "scope": "Numerical reconnaissance. No sign of c4_hat is proved or certified; no Arb certificate; no "
                    "super/subcritical classification; B2.4 and B2.5 not started.",
           "all_checks_pass": ok}
    (DATA / "B2_carrier.json").write_text(json.dumps(rec, indent=1, ensure_ascii=False))
    (DATA / "B2_falsification.json").write_text(json.dumps(
        {"project_version": __version__, "all_exposed": all(f["exposed"] for f in fals), "statements": fals},
        indent=1, ensure_ascii=False))
    print("B2.2 all checks pass:", ok, f"({time.time() - t0:.1f} s)")
    return ok


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
