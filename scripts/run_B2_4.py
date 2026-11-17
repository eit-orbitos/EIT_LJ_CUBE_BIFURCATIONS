"""Phase B2.4: Proposition B2, the local D2h-axial pitchfork on the T2g curve.
Status: PROVED (computer-assisted; not independently audited). No centre-manifold index, no full-space stability, no
cuboid claim, B2.5 not started.

Writes (deterministic; no timestamps):
- data/B2_4_branch.json: the exact derivation results (proof layer) and the numerical corroboration (not a proof
  dependency): located branch points for q = 0.2, 0.8, 1.5, 2.0 and p = P_T(q)(1 + r), r = +-1e-6, +-1e-7, both
  start signs; reduced scans of dV_red/ds on both sides; the full 24-D gradient; the amplitude law; the axial
  curvature; the exchange of +s* and -s* by an element of N(Sigma) minus Sigma.
- data/B2_4_dependency_graph.json: the machine-readable proof dependency graph, the statement, and the validator
  result.

Usage: python scripts/run_B2_4.py [exact|numeric|all]   (default all; the parts merge into the same record)
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import mpmath as mp  # noqa: E402
import sympy as sp  # noqa: E402

from cube_bif import STATUS, __version__  # noqa: E402
from cube_bif import b2_branch as B  # noqa: E402

DATA = ROOT / "data"
REC = DATA / "B2_4_branch.json"
GRAPH = DATA / "B2_4_dependency_graph.json"
Q_VALUES = ("0.2", "0.8", "1.5", "2.0")
REL_MU = ("1e-6", "1e-7", "-1e-6", "-1e-7")
DPS = 60


def n(x, d=20):
    return mp.nstr(x, d)


def exact_part():
    ls = B.generic_ls_checks()
    br = B.ift_branch()
    curv = B.axial_curvature()
    rh = B.rhombus_exact()
    out = {
        "generic_LS_checks": ls,
        "evenness_breaking_control_detected": B.evenness_breaking_detected(),
        "model_structure": B.model_structure(),
        "schur_identities": B.schur_identities(),
        "G_from_V_red_matches_lambda_plus_c4_z_over_6": B.reduced_G()["matches"],
        "ift": {k: str(v) for k, v in br.items()},
        "branch_side_by_signs": {f"tau{t},c4{c}": B.branch_side(t, c) for t in ("<0", ">0") for c in ("<0", ">0")},
        "classification_by_signs": {f"tau{t},c4{c}": B.classify(t, c) for t in ("<0", ">0") for c in ("<0", ">0")},
        "axial_curvature_leading": {k: str(v) for k, v in curv.items()},
        "isotropy": B.isotropy_exact(),
        "exchange": B.exchange_exact(),
        "rhombus_first_order": {k: (v if isinstance(v, bool) else str(v)) for k, v in rh.items()},
    }
    checks = [
        all(ls.values()), out["evenness_breaking_control_detected"], all(out["model_structure"].values()),
        all(out["schur_identities"].values()), out["G_from_V_red_matches_lambda_plus_c4_z_over_6"],
        sp.simplify(br["m1"] + B.C40 / (6 * B.TAU)) == 0, sp.simplify(br["Z1"] + 6 * B.TAU / B.C40) == 0,
        out["branch_side_by_signs"]["tau<0,c4>0"] == "mu > 0",
        out["classification_by_signs"]["tau<0,c4>0"] == "supercritical",
        curv["cube"] == B.TAU * B.mu, curv["branch"] == -2 * B.TAU * B.mu,
        out["isotropy"]["ranks_inside_Sigma"] == [0] and out["isotropy"]["ranks_outside_Sigma"] == [2],
        out["isotropy"]["T2g_projector_kills_A_E_fixes_uh1_vh1"] and out["isotropy"]["T2g_projector_commutes"],
        out["exchange"]["n_reversing_elements"] == 8 and out["exchange"]["all_act_as_diag_1_1_-1_-1"],
        rh["equal_sides"] and rh["diagonals_perpendicular"],
    ]
    out["all_exact_checks_pass"] = all(bool(c) for c in checks)
    return out


def numeric_part():
    rows, scans, summary = [], [], []
    ok = True
    with mp.workdps(DPS):
        for q in Q_VALUES:
            cd = B.curve_data(q)
            per = {}
            for rel in REL_MU:
                for sg in (1, -1):
                    r = B.branch_point(q, rel, sg, dps=DPS, cd=cd)
                    per[(rel, sg)] = r
                    rows.append({"q": q, "rel_mu": rel, "start_sign": sg, "p": n(r["p"], 25), "mu": n(r["mu"]),
                                 "s_start": n(r["s_start"]), "s_found": n(r["s_found"], 25),
                                 "wA": n(r["wA"]), "wE": n(r["wE"]), "wf": n(r["wf"]),
                                 "s2_predicted": n(r["s2_predicted"]),
                                 "amplitude_law_error": n(r["amplitude_law_error"]) if "amplitude_law_error" in r
                                 else None,
                                 "full_gradient_norm": n(r["full_gradient_norm"], 3),
                                 "axial_curvature": n(r["axial_curvature"]),
                                 "axial_curvature_cube": n(r["axial_curvature_cube"]), "tau_mu": n(r["tau_mu"])})
            # checks per q
            chk = {}
            for rel in ("1e-6", "1e-7"):
                a, b = per[(rel, 1)], per[(rel, -1)]
                chk[f"{rel}: +s and -s found"] = bool(a["s_found"] > 0 > b["s_found"]
                                                      and abs(a["s_found"] + b["s_found"]) < mp.mpf("1e-40"))
                chk[f"{rel}: full 24-D gradient < 1e-50"] = bool(max(a["full_gradient_norm"],
                                                                     b["full_gradient_norm"]) < mp.mpf("1e-50"))
                chk[f"{rel}: |amplitude-law error| < 1e-4"] = bool(abs(a["amplitude_law_error"]) < mp.mpf("1e-4"))
                chk[f"{rel}: axial curvature at +-s* = -2 tau mu (rel. 1e-3) and > 0"] = bool(
                    a["axial_curvature"] > 0 and abs(a["axial_curvature"] / (-2 * a["tau_mu"]) - 1) < mp.mpf("1e-3"))
                chk[f"{rel}: axial curvature at the cube = tau mu (rel. 1e-3) and < 0"] = bool(
                    a["axial_curvature_cube"] < 0 and abs(a["axial_curvature_cube"] / a["tau_mu"] - 1) < mp.mpf("1e-3"))
                chk[f"{rel}: f_1 component O(s^3) (|wf| < 10 |s|^3)"] = bool(abs(a["wf"]) < 10 * abs(a["s_found"]) ** 3)
            ratio = per[("1e-6", 1)]["amplitude_law_error"] / per[("1e-7", 1)]["amplitude_law_error"]
            chk["amplitude-law error ratio (1e-6 vs 1e-7) in [5, 20]: O(mu)"] = bool(5 < ratio < 20)
            for rel in ("-1e-6", "-1e-7"):
                for sg in (1, -1):
                    r = per[(rel, sg)]
                    chk[f"{rel}, start {sg:+d}: Newton returns to the cube (|s| < 1e-40)"] = bool(
                        abs(r["s_found"]) < mp.mpf("1e-40"))
                chk[f"{rel}: axial curvature at the cube > 0"] = bool(per[(rel, 1)]["axial_curvature_cube"] > 0)
            img = B.reversing_image_numeric(per[("1e-6", 1)]["x"])
            exch = max(abs(u - v) for u, v in zip(img, per[("1e-6", -1)]["x"]))
            chk["D(g) x(+s*) = x(-s*) for g in N(Sigma) minus Sigma (< 1e-50)"] = bool(exch < mp.mpf("1e-50"))
            for rel in ("1e-6", "-1e-6"):
                sc = B.reduced_scan(q, rel, dps=50, cd=cd)
                scans.append({"q": q, "rel_mu": rel, "S": n(sc["S"]), "sign_changes_on_(0,S]": sc["sign_changes"],
                              "g_over_s_at_smallest_s": n(sc["g_over_s_at_smallest_s"]),
                              "tau_mu": n(sc["lambda_leading"]),
                              "g_over_s": [[n(a, 12), n(b, 12)] for a, b in sc["values"]]})
                want = 1 if rel == "1e-6" else 0
                chk[f"reduced scan {rel}: {want} sign change(s) of g(s)/s on (0, 3 s_pred]"] = sc["sign_changes"] == want
            summary.append({"q": q, "p0": n(cd["p0"], 25), "rho": n(cd["rho"]), "n_u": n(cd["n_u"]),
                            "n_v": n(cd["n_v"]), "tau": n(cd["tau"]), "c4": n(cd["c4"]),
                            "slope_-6tau/c4": n(-6 * cd["tau"] / cd["c4"]), "amplitude_error_ratio": n(ratio, 8),
                            "exchange_residual": n(exch, 3), "checks": chk})
            ok = ok and all(chk.values())
    return {"role": "corroboration only (VERIFIED-NUMERIC); not a proof dependency of Proposition B2",
            "method": "Newton in the four Fix(Sigma) coordinates (A_HAT, E_HAT, e_1, f_1) with the 24-D pair energy, "
                      "gradient and Hessian of numeric.py at %d digits; p = P_T(q)(1 + r); start at "
                      "+-sqrt|-6 tau mu/c4| (for mu < 0 the mirror amplitude, where no branch is predicted); reduced "
                      "scan: w(s) by Newton in (A_HAT, E_HAT, f_1) at fixed s, g(s) = <grad V, e_1>, 24 points on "
                      "(0, 3 sqrt|6 tau mu/c4|] at 50 digits" % DPS,
            "curve_points": summary, "branch_points": rows, "reduced_scans": scans, "all_numeric_checks_pass": ok}


def main():
    part = sys.argv[1] if len(sys.argv) > 1 else "all"
    rec = json.loads(REC.read_text()) if REC.exists() and part != "all" else {}
    rec.update({"phase": "B2.4", "project_version": __version__, "status_line": STATUS,
                "proposition": "Proposition B2", "status": B.STATUS_PROVED,
                "scope": "local D2h-axial branch in y* + Fix(Sigma), fixed q in (0, q_c), |mu| small; one-dimensional "
                         "axial reduced direction only; no centre-manifold index, no full-space stability, no cuboid "
                         "claim; B2.5 not started"})
    if part in ("exact", "all"):
        rec["exact"] = exact_part()
        GRAPH.write_text(json.dumps({"graph": B.DEPENDENCY_GRAPH, "statement": B.PROPOSITION,
                                     "graph_validation_failures": B.validate_graph(),
                                     "statement_validation_failures": B.validate_statement()},
                                    indent=1, ensure_ascii=False) + "\n")
    if part in ("numeric", "all"):
        rec["numeric_corroboration"] = numeric_part()
    rec["all_checks_pass"] = bool(rec.get("exact", {}).get("all_exact_checks_pass")
                                  and rec.get("numeric_corroboration", {}).get("all_numeric_checks_pass"))
    keys = ["phase", "project_version", "status_line", "proposition", "status", "scope", "exact",
            "numeric_corroboration", "all_checks_pass"]
    REC.write_text(json.dumps({k: rec[k] for k in keys if k in rec}, indent=1, ensure_ascii=False) + "\n")
    print("exact:", rec.get("exact", {}).get("all_exact_checks_pass"),
          "numeric:", rec.get("numeric_corroboration", {}).get("all_numeric_checks_pass"),
          "all:", rec["all_checks_pass"])


if __name__ == "__main__":
    main()
