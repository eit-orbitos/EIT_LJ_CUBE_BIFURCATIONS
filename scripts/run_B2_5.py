"""Phase B2.5 records: data/B2_5_index.json (exact checks and numerical corroboration) and
data/B2_5_dependency_graph.json (the machine-readable proof dependency graph of Proposition B3 / Corollary B3').

Usage: python scripts/run_B2_5.py [exact|numeric|graph|all]. The numeric part is corroboration only.
Each part merges its section into data/B2_5_index.json, so the parts can be run separately.
"""
import json
import pathlib
import sys

import mpmath as mp

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cube_bif import b2_index as X  # noqa: E402
from cube_bif import b2_branch as b2  # noqa: E402

OUT = ROOT / "data" / "B2_5_index.json"
GRAPH = ROOT / "data" / "B2_5_dependency_graph.json"
QS = ("0.2", "0.8", "1.5", "2.0")
RELS = ("1e-5", "1e-6", "1e-7")


def nstr(x, n=12):
    return mp.nstr(x, n)


def load():
    return json.loads(OUT.read_text()) if OUT.exists() else {}


def save(rec):
    OUT.write_text(json.dumps(rec, indent=1, sort_keys=True) + "\n")


def exact_part():
    inv = X.invariant_basis_check()
    com = X.commutant_on_axis()
    par = X.parity_on_axis()
    gi = X.generic_invariant_hessian(6)
    br = X.branch_hessian_series(6)
    te = X.transverse_eigensystem()
    tb = X.transverse_sign_bound()
    lq = X.ls_quartic_exact()
    ab = X.alpha_beta_closed()
    import sympy as sp
    ls = X.generic_ls_multid()
    ci = X.complementary_index()
    pc = X.paper2_curve_consistency()
    cj = X.conjugate_branches()
    d3 = X.d3d_consistency()
    checks = {
        "group_order_24": inv["order"] == 24, "invariants_I2_I3_I2sq_I4": (
            inv["all_invariant"] and inv["deg2_spanned_by_I2"] and inv["deg3_spanned_by_I3"]
            and inv["deg4_spanned_by_I2sq_I4"] and inv["deg1_empty"]),
        "axis_stabiliser_order_4": com["stabiliser_order"] == 4,
        "commutant_form": com["h12_zero"] and com["h22_eq_h33"] and com["free_parameters"] == 3,
        "parity_h11_d_even_e_odd": par["all"],
        "generic_hessian_structure": gi["structure"] and gi["h11_even"] and gi["d_even"] and gi["e_odd"],
        "generic_hessian_leading_terms": gi["h11_low_ok"] and gi["d_low_ok"] and gi["e_low_ok"],
        "branch_mu_slope": br["m1_ok"], "branch_h11": br["h11_ok"], "branch_d": br["d_ok"], "branch_e": br["e_ok"],
        "branch_det": br["det_ok"], "branch_h11_equals_minus_2_tau_mu": br["h11_as_mu_ok"],
        "branch_offdiagonal_zero": br["offdiag_zero"],
        "transverse_eigensystem": te["plus"] and te["minus"] and te["det"],
        "transverse_sign_bound": tb["identity"] and tb["all_negative"],
        "ls_quartic_invariant_form": lq["invariant_form_exact"],
        "ls_quartic_alpha_plus_beta_c4": lq["alpha_plus_beta_is_c4_over_24"],
        "ls_quartic_hand_formula": lq["hand_formula_ok"],
        "ls_quartic_b_irreps_A1g_Eg_T2g": lq["b_irreps_present"] == ["A1g", "Eg", "T2g"],
        "d4_only_iiii_iijj": lq["d4_only_iiii_iijj"],
        "alpha_beta_closed": sp.expand(ab["alpha"] - lq["alpha"]) == 0 and sp.expand(ab["beta"] - lq["beta"]) == 0,
        "generic_ls_multid": ls["quartic_formula"] and ls["ls_residual_order2"],
        "schur_hessian_identity": X.schur_hessian_identity(),
        "haynsworth": X.haynsworth_check(),
        "m_perp_3": ci["m_perp"] == 3 and ci["W_invertible"] and ci["W_dim"] == 15,
        "paper2_curve_consistency": pc["m_perp_constant_3"],
        "conjugates_one_orbit": cj["orbit3_ok"] and cj["orbit24_ok"],
        "congruence": X.congruence_preserves_inertia(),
        "d3d_consistency": d3["axial_ok"] and d3["transverse_ok"] and d3["degree_consistent"],
        "statement_valid": X.validate_statement() == [], "graph_valid": X.validate_graph() == [],
    }
    checks = {k: bool(v) for k, v in checks.items()}
    rec = load()
    rec["exact"] = {
        "checks": checks, "all_pass": all(checks.values()), "n_checks": len(checks),
        "invariant_dimensions_deg1_6": {str(k): v for k, v in X.invariant_dimensions(6).items()},
        "branch_series": {"h11": str(br["h11"]), "d": str(br["d"]), "e": str(br["e"]), "det": str(br["det"]),
                          "mu_slope": str(br["m1"])},
        "complementary_index": ci, "corollary": X.full_index_corollary(),
        "d3d": {k: (v if isinstance(v, (int, bool)) else str(v)) for k, v in d3.items()},
        "statement": {k: (v if not isinstance(v, dict) else {str(a): b for a, b in v.items()})
                      for k, v in X.PROPOSITION_B3.items()},
        "corollary_statement": X.COROLLARY_B3,
    }
    save(rec)
    print("exact", rec["exact"]["all_pass"], rec["exact"]["n_checks"])


def numeric_part(which="all"):
    rec = load()
    num = rec.get("numeric", {})
    with mp.workdps(60):
        cds = {q: b2.curve_data(mp.mpf(q)) for q in QS}
        if which in ("all", "d2h"):
            rows = []
            for q in QS:
                for rel in RELS:
                    for sg in (1, -1):
                        r = X.d2h_point(mp.mpf(q), rel, sg, cd=cds[q])
                        rows.append({k: (nstr(v) if isinstance(v, mp.mpf) else
                                         [nstr(x) for x in v] if isinstance(v, (tuple, list)) else v)
                                     for k, v in r.items()})
            num["d2h"] = rows
        if which in ("all", "d3d"):
            rows = []
            for q in QS:
                for rel in ("1e-6", "-1e-6"):
                    r = X.d3d_point(mp.mpf(q), rel, cd=cds[q])
                    rows.append({k: (nstr(v) if isinstance(v, mp.mpf) else v) for k, v in r.items()})
            num["d3d"] = rows
        if which in ("all", "quartic"):
            rows = []
            for q in QS:
                qn = X.quartic_numeric(cds[q])
                for u in ((1, 0, 0), (1, 1, 0), (1, 1, 1), (2, 1, 0)):
                    r = X.quartic_route3(mp.mpf(q), u, cd=cds[q])
                    rows.append({k: (nstr(v) if isinstance(v, mp.mpf) else v) for k, v in r.items()})
                rows.append({"q": q, "coefficients": {k: nstr(v) for k, v in qn.items()}})
            num["quartic"] = rows
        if which in ("all", "cube"):
            rows = []
            for q in QS:
                cd = cds[q]
                an = X.hessian_analysis(cd, cd["p0"], [mp.mpf(c) / 2 for lab in X.LABELS for c in lab])
                rows.append({"q": q, "neg": an["neg"], "zero": an["zero"], "pos": an["pos"], "W_neg": an["W_neg"],
                             "min_abs_W_eig": nstr(an["min_abs_W_eig"])})
            num["cube_on_curve"] = rows
    rec["numeric"] = num
    save(rec)
    print("numeric", which, "done")


def summarise():
    """Evaluate the numerical corroboration checks from the stored record."""
    rec = load()
    num = rec["numeric"]
    F = mp.mpf
    checks = []

    def add(name, ok):
        checks.append({"check": name, "pass": bool(ok)})
    for r in num["d2h"]:
        tag = f"d2h q={r['q']} rel={r['rel_mu']} sign={'+' if F(r['s']) > 0 else '-'}"
        add(tag + " gradient<1e-50", F(r["full_gradient_norm"]) < F("1e-50"))
        add(tag + " R24 index 4, 6 zero (rigid)", r["neg"] == 4 and r["zero"] == 6)
        add(tag + " rigid fields in kernel", F(r["rigid_residual"]) < F("1e-50"))
        add(tag + " H_WW index 3 (m_perp)", r["W_neg"] == 3)
        add(tag + " centre (Schur) index 1, nullity 0", r["schur_neg"] == 1 and r["schur_zero"] == 0)
        add(tag + " h12 = h13 = 0, h22 = h33", max(abs(F(r["h12"])), abs(F(r["h13"])), abs(F(r["d_asym"])))
            < F("1e-45"))
        ev = [F(x) for x in r["transverse_eigs"]]
        add(tag + " transverse eigenvalues of opposite sign", ev[0] * ev[1] < 0)
        neg_vec = "(0,1,-1)" if ev[1] < 0 else "(0,1,1)"
        add(tag + " negative direction (0,1,-sign(kappa s))", neg_vec == ("(0,1,-1)" if F(r["s"]) * F(r["kappa"]) > 0
                                                                          else "(0,1,1)"))
        add(tag + " h11 > 0", F(r["h11"]) > 0)
        lim = 200 * abs(F(r["rel_mu"]))   # O(mu) constant; q = 2.0 needs ~53 (c4 small near the corner)
        add(tag + " h11, d, e match (c4/3)s^2, -4 beta s^2, kappa s to O(mu)",
            max(abs(F(r["h11_rel_err"])), abs(F(r["d_rel_err"])), abs(F(r["e_rel_err"]))) < lim)
    by = {}
    for r in num["d2h"]:
        if F(r["s"]) > 0:
            by.setdefault(r["q"], {})[r["rel_mu"]] = r
    for q, rr in by.items():
        e5, e6, e7 = (abs(F(rr[k]["e_rel_err"])) for k in RELS)
        add(f"d2h q={q} error scaling O(mu)", 7 < e6 / e7 < 13 and 7 < e5 / e6 < 13)
        t5, t6, t7 = (abs(F(rr[k]["e"])) for k in RELS)
        a5, a6, a7 = (F(rr[k]["h11"]) for k in RELS)
        add(f"d2h q={q} transverse ~ sqrt(mu), axial ~ mu",
            abs(t6 / t7 - mp.sqrt(10)) < F("0.01") and abs(a6 / a7 - 10) < F("0.01"))
    for r in num["d3d"]:
        tag = f"d3d q={r['q']} rel={r['rel_mu']}"
        mupos = F(r["rel_mu"]) > 0
        add(tag + " gradient<1e-50", F(r["full_gradient_norm"]) < F("1e-50"))
        add(tag + " R24 index " + ("5" if mupos else "4"), r["neg"] == (5 if mupos else 4) and r["zero"] == 6)
        add(tag + " centre index " + ("2" if mupos else "1"), r["schur_neg"] == (2 if mupos else 1))
        add(tag + " axial ~ kappa t, transverse ~ -2 kappa t",
            abs(F(r["axial"]) / F(r["kappa_t"]) - 1) < F("0.05") and abs(F(r["transverse"]) / F(r["kappa_t"]) + 2)
            < F("0.1"))
    for r in num["quartic"]:
        if "V4_route3" in r:
            add(f"quartic q={r['q']} u={r['u']} route3 = alpha I2^2 + beta I4", F(r["rel_diff"]) < F("1e-18"))
    for r in num["cube_on_curve"]:
        add(f"cube at p=P_T(q={r['q']}) index 3, 9 zero (6 rigid + 3 critical), H_WW index 3",
            r["neg"] == 3 and r["zero"] == 9 and r["W_neg"] == 3)
    rec["numeric_checks"] = {"n": len(checks), "passed": sum(c["pass"] for c in checks),
                             "failed": [c["check"] for c in checks if not c["pass"]], "checks": checks}
    save(rec)
    print("numeric checks", rec["numeric_checks"]["passed"], "/", rec["numeric_checks"]["n"],
          rec["numeric_checks"]["failed"])


def graph_part():
    GRAPH.write_text(json.dumps(X.DEPENDENCY_GRAPH, indent=1, sort_keys=True) + "\n")
    print("graph written; failures:", X.validate_graph())


if __name__ == "__main__":
    arg = sys.argv[1] if len(sys.argv) > 1 else "all"
    if arg in ("exact", "all"):
        exact_part()
    if arg in ("graph", "all"):
        graph_part()
    if arg in ("numeric", "all"):
        numeric_part()
    if arg.startswith("numeric:"):
        numeric_part(arg.split(":")[1])
    if arg in ("summary", "all"):
        summarise()
