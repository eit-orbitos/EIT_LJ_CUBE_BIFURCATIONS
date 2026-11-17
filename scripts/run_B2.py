"""Phase B2.0 and B2.1: exact symmetry audit of the D2h axis and the quartic Lyapunov-Schmidt coefficient c4 by three
routes. No scan, no sign claim on the curve and no certificate (those are B2.2 and B2.3).

Writes:
- data/B2_symmetry.json: stabiliser, fixed space and its isotypic decomposition, the relayed claim tested, where
  b = D^3V[e_1, e_1, .] lives, the Schur reason, the normaliser, the vertex-orbit parametrisation, first-order
  geometry and the cuboid family;
- data/B2_quartic.json: the 13 exact linear forms, closed forms, difference forms, the Hessian on the fixed space,
  the exact raw route, and the three-route comparison at five curve points.
"""
import json
import pathlib
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import mpmath as mp  # noqa: E402
import sympy as sp  # noqa: E402

from cube_bif import STATUS, __version__, b1_cubic as b1, b2_quartic as b2, b2_symmetry as s2, t2g  # noqa: E402
from cube_bif import pairsum as ps  # noqa: E402
from cube_bif.group import D24, average  # noqa: E402

DATA = ROOT / "data"
POINTS = ("0.05", "0.5", "1.0", "1.5", "2.0")


def s(x, n=25):
    return mp.nstr(x, n)


def zero(v):
    return v.applyfunc(sp.expand) == sp.zeros(*v.shape)


def symmetry_layer():
    P = s2.fix_projector()
    pr = s2.b_projections()
    b = s2.b_vector()
    ips = s2.t2g_inner_products()
    rev = s2.reversing_elements()
    flds = s2.orbit_fields()
    Z2 = [sp.ImmutableMatrix(sp.diag(a, b_, c)) for a in (1, -1) for b_ in (1, -1) for c in (1, -1)]
    Pc = average(Z2, D24)
    claim = s2.claimed_basis_check()
    out = {
        "stabiliser_of_e1": s2.stabilizer_record(),
        "stabiliser_equals_3x3_stabiliser_of_100": {tuple(R) for R in s2.axis_stabilizer()}
        == {tuple(R) for R in t2g.stabilizer((1, 0, 0))},
        "fix_rank": int(P.rank()),
        "isotypic_ranks_of_Fix": s2.isotypic_ranks(),
        "character_prediction": s2.character_prediction(),
        "fixed_basis": {"A1g": "E_BR/sqrt(24) (breathing)", "Eg": "E_TET_X/sqrt(48), field s -> (2 s1, -s2, -s3)",
                        "T2g_u": "uh_1 = -W_1/4", "T2g_v": "vh_1 = -(sqrt2/4) U_1",
                        "note": "span{uh_1, vh_1} = span{e_1, f_1}, f_1 = -n_v uh_1 + n_u vh_1"},
        "relayed_claim_Fix_equals_span_e_A1g_Eg1_Eg2": claim,
        "b_projection_nonzero": {G: v != sp.zeros(24, 1) for G, v in pr.items()},
        "b_equals_A1g_plus_Eg_projections": zero(pr["A1g"] + pr["Eg"] - b),
        "b_T2g_inner_products_all_zero": all(v == 0 for v in ips.values()),
        "n_T2g_inner_products_checked": len(ips),
        "b_dot_f1_zero": sp.expand((s2.f1().T * b)[0, 0]) == 0,
        "b_dot_e1_zero": sp.expand((s2.e1().T * b)[0, 0]) == 0,
        "b_reconstruction_exact": {ch: s2.b_reconstruction_residual(ch) == sp.zeros(24, 1) for ch in s2.B_CHANNELS},
        "b_components_generic_psi": {ch: {k: str(v) for k, v in c.items()} for ch, c in s2.b_components().items()},
        "b_formula": "b = sum_cc' w_cc' n^cc' (bA_cc' A_HAT + bE_cc' E_HAT), w = (1, 2, 1) for uu, uv, vv",
        "sym2_T2g_part_equivariant": s2.sym2_t2g_part_is_equivariant(),
        "sym2_diagonal_part_permuted": s2.sym2_diagonal_part_is_invariant_set(),
        "sym2_T2g_part_on_axis_100": [int(c) for c in s2.sym2_t2g_part((1, 0, 0))],
        "reversing_elements": {"count": len(rev), "actions_on_Fix_basis": sorted({json.dumps(x["diag_action_on_Fix_basis"],
                                                                                         sort_keys=True) for x in rev}),
                               "all_Fix_basis_vectors_eigenvectors": all(x["Fix_basis_vectors_are_eigenvectors"]
                                                                         for x in rev)},
        "vertex_orbits": s2.orbit_structure(),
        "orbit_fields_in_Fix": all(zero(P * v - v) for v in flds.values()),
        "orbit_fields_rank": int(sp.Matrix.hstack(*flds.values()).rank()),
        "first_order_displacement": "vertex s: -(s n_u/4)(0, s3, s2) - (s n_v sqrt2/4)(s1 s2 s3)(1, 0, 0)",
        "cuboid_family_Fix_Z2cubed_rank": int(Pc.rank()),
        "e1_f1_orthogonal_to_cuboid_family": zero(Pc * s2.e1()) and zero(Pc * s2.f1()),
    }
    checks = [out["stabiliser_equals_3x3_stabiliser_of_100"], out["fix_rank"] == 4,
              out["isotypic_ranks_of_Fix"] == {"A1g": 1, "A2g": 0, "Eg": 1, "T1g": 0, "T2g": 2, "A1u": 0, "A2u": 0,
                                               "Eu": 0, "T1u": 0, "T2u": 0},
              not claim["claimed_vector_is_fixed"]["Eg(2) orthorhombic yz"], claim["f1_is_fixed"],
              not claim["f1_in_claimed_span"],
              all(not v for G, v in out["b_projection_nonzero"].items() if G not in ("A1g", "Eg")),
              out["b_equals_A1g_plus_Eg_projections"], out["b_T2g_inner_products_all_zero"], out["b_dot_f1_zero"],
              out["b_dot_e1_zero"], all(out["b_reconstruction_exact"].values()), out["sym2_T2g_part_equivariant"],
              out["sym2_diagonal_part_permuted"], out["sym2_T2g_part_on_axis_100"] == [0, 0, 0],
              out["reversing_elements"]["count"] == 8, out["orbit_fields_in_Fix"], out["orbit_fields_rank"] == 4,
              out["e1_f1_orthogonal_to_cuboid_family"]]
    out["all_checks_pass"] = all(checks)
    return out


def exact_layer():
    f = b2.linear_forms()
    H = b2.hessian_on_fix()
    K = t2g.block_K()[0]
    return {
        "linear_forms_generic_psi": {k: str(v) for k, v in f.items()},
        "c4_generic": "Q(n) - 3 b_A(n)^2/h_A - 3 b_E(n)^2/h_E, Q(n) = sum_j C(4,j) n_u^(4-j) n_v^j Q_j, "
                      "b_X(n) = n_u^2 bX_uu + 2 n_u n_v bX_uv + n_v^2 bX_vv (unit n)",
        "hessian_on_Fix_basis": "A_HAT, E_HAT, uh_1, vh_1",
        "hessian_on_Fix": [[str(H[i, j]) for j in range(4)] for i in range(4)],
        "hessian_on_Fix_T2g_block_equals_B0_block_K": sp.simplify(H[2:, 2:] - K) == sp.zeros(2),
        "A_HAT_E_HAT_eigenvectors_of_full_hessian": zero(ps.hessian() * s2.A_HAT - f["hA"] * s2.A_HAT)
        and zero(ps.hessian() * s2.E_HAT - f["hE"] * s2.E_HAT),
        "route2a_raw_quartic_equals_route1": sp.expand(b2.raw_quartic() - b2.Q_of_n()) == 0,
        "route2a_raw_b_equals_B2_0_b": zero(b2.raw_b_vector() - s2.b_vector()),
        "closed_forms": {k: str(v) for k, v in b2.G4_CLOSED.items()},
        "closed_form_residuals_zero": {k: b2.closed_form_residual(k) == 0 for k in b2.FORM_NAMES},
        "difference_form_residuals_zero": {k: b2.difference_form_residual(k) == 0 for k in b2.FORM_NAMES},
        "factorisation": "c4 = q W_q (p - q) c4_hat, c4_hat = Q_hat - 3 bA_hat^2/hA_hat - 3 bE_hat^2/hE_hat, "
                         "hA_hat = 2 exactly",
        "factorisation_identity_zero": b2.factorisation_identity() == 0,
        "positivity_of_hA_hE": "FROZEN INPUT: Paper 2, Lemma S (A1g and Eg strictly stable for all p > q > 0); "
                               "g_hA, g_hE equal Paper 2's h_L for A1g and Eg exactly",
    }


def routes():
    rows = []
    with mp.workdps(60):
        for qq in POINTS:
            t0 = time.time()
            r1 = b2.route1(qq)
            r2 = b2.route2_numeric(qq)
            r3 = b2.route3(qq)
            K = t2g.M_num(r1["p"]) - t2g.M_num(r1["q"])
            trK = r1["q"] * b1.W_num(r1["q"]) * (K[0, 0] + K[1, 1])
            want = sorted([trK, r1["h_A"], r1["h_E"]])
            e = b2._e1_numeric(*r1["n"])
            ip = mp.fsum(x * y for x, y in zip(r3["kernel_vector_R24"], e))
            rows.append({
                "q": qq, "p": s(r1["p"]), "delta": s(r1["delta"]), "rho": s(r1["rho"], 18),
                "Q_hat": s(r1["Q_hat"], 18), "bA_hat": s(r1["bA_hat"], 18), "bE_hat": s(r1["bE_hat"], 18),
                "hA_hat": s(r1["hA_hat"], 18), "hE_hat": s(r1["hE_hat"], 18),
                "backreaction_A1g_hat": s(r1["backreaction_A1g_hat"], 18),
                "backreaction_Eg_hat": s(r1["backreaction_Eg_hat"], 18),
                "c4_hat": s(r1["c4_hat"]), "c4_route1": s(r1["c4"], 30), "c4_route2": s(r2["c4"], 30),
                "c4_route3": s(r3["c4"], 30),
                "rel_diff_route2": mp.nstr(abs(r2["c4"] / r1["c4"] - 1), 3),
                "rel_diff_route3": mp.nstr(abs(r3["c4"] / r1["c4"] - 1), 3),
                "route3_richardson_error_relative": mp.nstr(r3["richardson_error"] / abs(r1["c4"]), 3),
                "route3_curve_point_minus_B1": mp.nstr(r3["p"] - r1["p"], 3),
                "route3_nonzero_eigenvalues_vs_trK_hA_hE_max_rel": mp.nstr(
                    max(abs(g / w - 1) for g, w in zip(r3["nonzero_eigenvalues"], want)), 3),
                "route3_kernel_vector_dot_e1": mp.nstr(abs(ip), 40),
                "route3_evenness_defect": mp.nstr(r3["evenness_defect"], 3),
                "route2_small_eigenvalues": r2["n_small_eigenvalues"],
                "route2_b_on_kernel": mp.nstr(r2["max_b_component_on_small_eigenvectors"], 3)})
            print(f"q = {qq}: c4 = {s(r1['c4'], 15)}, routes 2/3 rel {rows[-1]['rel_diff_route2']}, "
                  f"{rows[-1]['rel_diff_route3']} ({time.time() - t0:.1f} s)")
    return rows


def main():
    t0 = time.time()
    sym = symmetry_layer()
    sym.update({"project_version": __version__, "status": STATUS})
    (DATA / "B2_symmetry.json").write_text(json.dumps(sym, indent=1, ensure_ascii=False))
    print("B2.0 all checks pass:", sym["all_checks_pass"], f"({time.time() - t0:.1f} s)")
    ex = exact_layer()
    rt = routes()
    ok = (all(ex["closed_form_residuals_zero"].values()) and all(ex["difference_form_residuals_zero"].values())
          and ex["factorisation_identity_zero"] and ex["hessian_on_Fix_T2g_block_equals_B0_block_K"]
          and ex["A_HAT_E_HAT_eigenvectors_of_full_hessian"] and ex["route2a_raw_quartic_equals_route1"]
          and ex["route2a_raw_b_equals_B2_0_b"]
          and all(mp.mpf(r["rel_diff_route2"]) < mp.mpf("1e-40") for r in rt)
          and all(mp.mpf(r["rel_diff_route3"]) < mp.mpf("1e-28") for r in rt)
          and all(r["route2_small_eigenvalues"] == 9 for r in rt))
    out = {"project_version": __version__, "status": STATUS, "working_precision_digits": 60,
           "exact": ex, "route_comparison": rt,
           "scope": "c4 at five curve points, VERIFIED-NUMERIC at these points only. No scan, no sign claim on the "
                    "curve, no endpoint analysis and no certificate: those are B2.2 and B2.3.",
           "all_checks_pass": ok}
    (DATA / "B2_quartic.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print("B2.1 all checks pass:", ok, f"({time.time() - t0:.1f} s)")
    return sym["all_checks_pass"] and ok


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
