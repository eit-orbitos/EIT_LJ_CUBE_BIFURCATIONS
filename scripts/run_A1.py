"""Phase A1 — quartic Lyapunov-Schmidt coefficient on the A2u curve p = P_A(q), 0 < q < r*.

Writes data/A1_quartic.json (exact formulas, identities, constants, branch checks) and data/A1_sign_table.csv.
Numbers are mpmath at 50 digits; sign statements are NUMERICAL (not certified).
"""
import csv
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import mpmath as mp  # noqa: E402
import sympy as sp  # noqa: E402

from cube_bif import STATUS, __version__, a2u, branch, paper2_ref  # noqa: E402
from cube_bif import pairsum as ps  # noqa: E402
from cube_bif.modes import E_BR  # noqa: E402

mp.mp.dps = 50


def s(v, n=25):
    return mp.nstr(v, n)


def main():
    out = {"project": "EIT-LJ Cube Bifurcations (Paper 3)", "version": __version__, "status": STATUS,
           "normalisation": a2u.__doc__.strip()}
    f = a2u.forms()
    g = a2u.g_functions()
    sf = a2u.scale_free_coefficients()
    b = a2u.b_vector()
    beta = (b.T * E_BR)[0, 0] / sp.sqrt(24)
    out["exact"] = {
        "linear_forms_psi": {k: str(sp.expand(f[k])) for k in ("V_aa", "V_bb", "V_aab", "V_aaaa")},
        "vanishing_by_symmetry": {k: str(f[k]) for k in ("V_a", "V_b", "V_ab", "V_aaa", "V_abb")},
        "g_functions (Q = q W_q [g_Q(p) - g_Q(q)], x = 2^(-r/2), y = 3^(-r/2))": {k: str(v) for k, v in g.items()},
        "c4_full": "q W_q { [g_4(p)-g_4(q)] - 3 [g_3(p)-g_3(q)]^2 / [g_B(p)-g_B(q)] }",
        "scale_free": {k: str(v) for k, v in sf.items()},
        "c4_scale_free (on the curve)": "(16/3) q W_q [ m(p) - m(q) ]",
        "f''(0) = p q [k(q)-k(p)] = -(p q/8) [h_A(p)-h_A(q)]": str(sp.simplify(sf["k"] - (a2u.H_A_FROZEN / 8 - sp.Rational(1, 4)))),
    }
    lemma = a2u.foliation_lemma()
    chain_c4, chain_res = a2u.scale_free_chain()
    out["identities"] = {
        "V_a = V_ab = V_aaa = V_abb = 0 for every pair potential (symmetry)": all(
            f[k] == 0 for k in ("V_a", "V_ab", "V_aaa", "V_abb")),
        "V_b = 0 at the equilibrium A = t (two-term potential)": sp.simplify(f["V_b"].subs(ps.two_term())) == 0,
        "V_b is not identically zero (the equilibrium condition is needed)": f["V_b"] != 0,
        "b = D3V[e_A,e_A,.] = V_aab e_br exactly (24 components)": bool(
            sp.simplify(b - beta * E_BR / sp.sqrt(24)) == sp.zeros(24, 1)) and sp.simplify(beta - f["V_aab"]) == 0,
        "h_A (this project) == h_A (Paper 2 Lemma A)": sp.simplify(g["h_A"] - a2u.H_A_FROZEN) == 0,
        "k(r) = h_A(r)/8 - 1/4": sp.simplify(sf["k"] - (a2u.H_A_FROZEN / 8 - sp.Rational(1, 4))) == 0,
        "generic LS: c4_R1 = F_aaaa - 3 F_aab^2/F_bb": str(lemma["c4_R1"]),
        "generic: c4_R2 - c4_R1": str(lemma["difference"]),
        "generic: c4_R2 = c4_R1 when F_aa = 0": lemma["difference"].subs(lemma["symbols"]["F_aa"], 0) == 0,
        "chain: c4 = (16/3) q W_q (m_p - m_q) on the curve": chain_res == 0,
    }
    rs = a2u.r_star()
    P0 = mp.findroot(lambda t: a2u.h_A_num(t) + mp.mpf(6) / 7, (rs, mp.mpf("3.2")), solver="anderson")
    m_num = a2u.numeric(sf["m"])
    m_r = sf["m"].subs({a2u.x: 2 ** (-a2u.r / 2), a2u.y: 3 ** (-a2u.r / 2)})
    m0 = sp.limit(m_r, a2u.r, 0)
    m_inf = sp.limit(m_r, a2u.r, sp.oo)
    out["constants"] = {
        "r_star (recomputed)": s(rs, 40), "r_star (Paper 2 frozen)": paper2_ref.FROZEN["r_star"],
        "r_star agreement": s(abs(rs - mp.mpf(paper2_ref.FROZEN["r_star"])), 3),
        "P_A(0+) (recomputed: h_A(p) = -6/7)": s(P0, 40), "P_A(0+) (Paper 2 frozen)": paper2_ref.FROZEN["P_A_soft"],
        "P_A(0+) agreement": s(abs(P0 - mp.mpf(paper2_ref.FROZEN["P_A_soft"])), 3),
        "m(0+)": str(m0), "m(infinity)": str(m_inf),
    }
    # ---- sign table -----------------------------------------------------------------------------------------
    qs = [rs * mp.mpf(i) / 400 for i in range(1, 400)]
    qs += [rs * mp.mpf(10) ** (-k) for k in range(3, 9)] + [rs * (1 - mp.mpf(10) ** (-k)) for k in range(3, 13)]
    qs = sorted(set(qs))
    rows = []
    for qq in qs:
        cp = a2u.curve_point(qq, rs)
        rows.append(cp)
    keys = ["q", "p", "h_A(p)-h_A(q)", "V_bb", "V_aab", "V_aaaa", "c4_full", "c4_scale_free", "Delta_m", "f4",
            "dlambda_dp_sign_carrier"]
    with open(ROOT / "data" / "A1_sign_table.csv", "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(keys + ["rel_diff_full_vs_scale_free", "c4_over_qWq_times_(p-q)"])
        for cp in rows:
            rel = abs(cp["c4_full"] - cp["c4_scale_free"]) / abs(cp["c4_full"])
            w.writerow([s(cp[k], 20) for k in keys] + [s(rel, 3),
                                                      s(cp["c4_full"] / (cp["q"] * a2u.W_num(cp["q"]) * (cp["p"] - cp["q"])), 20)])
    dms = [cp["Delta_m"] for cp in rows]
    rels = [abs(cp["c4_full"] - cp["c4_scale_free"]) / abs(cp["c4_full"]) for cp in rows]
    resid = [abs(cp["h_A(p)-h_A(q)"]) for cp in rows]
    out["sign_table_summary"] = {
        "points": len(rows), "q_min": s(min(qs), 10), "q_max": s(max(qs), 25),
        "c4_full > 0 at every point": all(cp["c4_full"] > 0 for cp in rows),
        "Delta_m = [m(p)-m(q)]/(p-q): min": s(min(dms), 12), "max": s(max(dms), 12),
        "max |h_A(p)-h_A(q)| (curve residual)": s(max(resid), 3),
        "max relative |c4_full - c4_scale_free|": s(max(rels), 3),
        "transversality: h_A'(P_A(q)) < 0 at every point": all(cp["dlambda_dp_sign_carrier"] < 0 for cp in rows),
        "endpoint q -> 0+: Delta_m -> (m(P_A(0+)) - m(0+)) / P_A(0+)": s((m_num(P0) - mp.mpf(8) / 7) / P0, 12),
        "endpoint q -> r*: Delta_m -> m'(r*)": s(mp.diff(m_num, rs), 12),
    }
    # monotonicity of m on (0, P_A(0+)] and location of its maximum (numerical scan)
    grid = [P0 * mp.mpf(k) / 2000 for k in range(1, 2001)]
    dm = [mp.diff(m_num, t) for t in grid]
    rmax = mp.findroot(lambda t: mp.diff(m_num, t), mp.mpf(7.6))
    out["m_scan"] = {"min m'(r) on (0, P_A(0+)] (2000-point grid)": s(min(dm), 12),
                     "argmin": s(grid[dm.index(min(dm))], 8), "argmax of m on (0, inf)": s(rmax, 20),
                     "m(argmax)": s(m_num(rmax), 20)}
    # ---- local branch inside the T_d family (numerical) -----------------------------------------------------
    br = []
    for qq in ("0.2", "0.8", "1.3"):
        pa = a2u.P_A(qq, rs)
        for d in ("1e-3", "1e-5", "1e-7"):
            bp = branch.branch_point(pa * (1 + mp.mpf(d)), mp.mpf(qq))
            br.append({"q": qq, "p": f"P_A(q)(1+{d})", "u_pred": s(bp["u_pred"], 15), "u_found": s(bp["u_found"], 15),
                       "u_found/u_pred - 1": s(bp["u_found"] / bp["u_pred"] - 1, 5)})
        pm = pa * (1 - mp.mpf("1e-5"))
        bm = branch.branch_point(pm, mp.mpf(qq))
        br.append({"q": qq, "p": "P_A(q)(1-1e-5)", "u_pred": "none (-6 f''/f'''' < 0)" if bm["u_pred"] is None else "?",
                   "f' one-signed on (0, 0.05]": branch.no_small_branch(pm, mp.mpf(qq), mp.mpf("0.05"))})
    out["branch_check"] = br
    # ---- cross-check against Paper 2's own code (if the frozen archive is available) ----------------------------
    cit = paper2_ref.load_analysis("cube_index_theorem")
    if cit is not None:
        dev = max(abs(a2u.P_A(qq, rs) - cit.P_A(float(qq))) for qq in ("0.05", "0.3", "0.7", "1.0", "1.3", "1.47"))
        out["paper2_cross_check"] = {"archive_sha256": paper2_ref.ARCHIVE_SHA256,
                                     "max |P_A(this) - P_A(Paper 2 float code)| at 6 points": s(dev, 3)}
    out["identities_all_true"] = all(v is True for v in out["identities"].values() if isinstance(v, bool))
    (ROOT / "data" / "A1_quartic.json").write_text(json.dumps(out, indent=1, default=str))
    print(json.dumps({k: out[k] for k in ("identities", "constants", "sign_table_summary", "m_scan")}, indent=1,
                     default=str))
    return out


if __name__ == "__main__":
    main()
