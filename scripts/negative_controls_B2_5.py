"""Code-mutation controls for Phase B2.5 (src/cube_bif/b2_index.py). Each mutation is applied to a scratch copy of the
project and must make the named test of tests/test_B2_index.py fail. Every target is first run on an unmutated copy and
must pass there. The mutations cover the required false alternatives: transverse block positive definite, transverse
block negative definite, omission of the kappa s term, kappa s replaced by kappa s^2, the axial curvature alone counted
as the centre index, full-space stability claimed from the centre index, rigid motions counted in the Morse index, and
the Paper 2 complementary index assumed instead of derived; plus derivation, frozen-table, graph and validator sabotage.
Kept separate from the earlier control scripts so that they and their records stay byte-identical.
Writes data/B2_5_negative_controls.json. Optional arguments: a subset of mutation indices (chunked runs; merged).
"""
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
F = "src/cube_bif/b2_index.py"
T = "tests/test_B2_index.py::"
STMT = T + "test_statement_and_graph_valid"


def prop_ctl(name):
    return T + f"test_false_proposition_statements_rejected[{name}]"


def cor_ctl(name):
    return T + f"test_false_corollary_statements_rejected[{name}]"


def graph_ctl(name):
    return T + f"test_invalid_graphs_rejected[{name}]"


MUTATIONS = [
    # ---- the derivation (exact layer)
    ("omission of the kappa s term: cubic invariant dropped from the generic reduced potential",
     [("    V = sp.Symbol(\"V0\") + LAM * I2 / 2 + KAP * I3 + ALPHA * I2 ** 2 + BETA * I4\n",
       "    V = sp.Symbol(\"V0\") + LAM * I2 / 2 + 0 * KAP * I3 + ALPHA * I2 ** 2 + BETA * I4\n")],
     T + "test_branch_hessian_series"),
    ("kappa s replaced by kappa s^2: cubic term replaced by kappa a1 I3",
     [("    V = sp.Symbol(\"V0\") + LAM * I2 / 2 + KAP * I3 + ALPHA * I2 ** 2 + BETA * I4\n",
       "    V = sp.Symbol(\"V0\") + LAM * I2 / 2 + KAP * a1 * I3 + ALPHA * I2 ** 2 + BETA * I4\n")],
     T + "test_branch_hessian_series"),
    ("kappa s term dropped in the derived statement (transverse block becomes definite)",
     [("    indefinite = sp.simplify(lead_plus + lead_minus) == 0 and lead_plus != 0\n",
       "    indefinite = False\n")], STMT),
    ("c4 = 12(alpha + beta) instead of 24(alpha + beta) on the branch (missing factor)",
     [("    c4 = 24 * (ALPHA + BETA)\n    zstar", "    c4 = 12 * (ALPHA + BETA)\n    zstar")],
     T + "test_branch_hessian_series"),
    ("axis parity: e assumed even (reversing elements fix e)",
     [("\"e_flips\": Hm[1, 2] == -e,", "\"e_flips\": Hm[1, 2] == e,")], T + "test_axis_commutant_and_parity"),
    ("axial curvature alone counted as the centre index (transverse part dropped)",
     [("    return (1 if h11c < 0 else 0) + transverse\n", "    return (1 if h11c < 0 else 0)\n")],
     T + "test_centre_index_gauge_and_sign_independent"),
    ("transverse block taken positive definite in the centre index (det sign ignored)",
     [("    if det_negative:\n        transverse = 1\n", "    if det_negative:\n        transverse = 0\n")],
     T + "test_centre_index_gauge_and_sign_independent"),
    ("remainder bound: admissible radius doubled",
     [("smax = min(sp.Integer(1), abs(kap) / (cd + ce))", "smax = min(sp.Integer(1), 2 * abs(kap) / (cd + ce))")],
     T + "test_transverse_eigensystem_and_bound"),
    # ---- the statement
    ("statement: transverse block negative definite",
     [("    \"transverse_block\": \"indefinite\",", "    \"transverse_block\": \"negative definite\",")], STMT),
    ("statement: transverse block positive definite",
     [("    \"transverse_block\": \"indefinite\",", "    \"transverse_block\": \"positive definite\",")], STMT),
    ("statement: h23 = kappa s^2",
     [("    \"hessian_e\": \"kappa*s\",", "    \"hessian_e\": \"kappa*s**2\",")], STMT),
    ("statement: full-space stability claimed from the centre index",
     [("    \"claims_full_space_stability\": False,\n    \"claims_stability\": False,",
       "    \"claims_full_space_stability\": True,\n    \"claims_stability\": False,")], STMT),
    ("statement: status upgraded to independently audited",
     [("    \"status\": STATUS_PROVED,\n    \"dependency_root\": \"P_B3\",",
       "    \"status\": STATUS_PROVED + \" · INDEPENDENTLY AUDITED\",\n    \"dependency_root\": \"P_B3\",")], STMT),
    ("corollary: rigid motions counted",
     [("    \"rigid_motions_counted\": False,", "    \"rigid_motions_counted\": True,")], STMT),
    ("corollary: Paper 2 complementary index assumed",
     [("    \"m_perp_assumed\": False,", "    \"m_perp_assumed\": True,")], STMT),
    # ---- the frozen table and the index counting
    ("frozen table: A2u sign flipped to +",
     [("{\"block\": \"A2u\", \"dim\": 1, \"sign\": \"-\",", "{\"block\": \"A2u\", \"dim\": 1, \"sign\": \"+\",")],
     T + "test_complementary_index_derived_from_frozen_table"),
    ("index counting: rigid motions added to the full-slice index",
     [("\"full_slice_index\": ci[\"m_perp\"] + centre_index,",
       "\"full_slice_index\": ci[\"m_perp\"] + centre_index + ci[\"rigid\"],")],
     T + "test_complementary_index_derived_from_frozen_table"),
    ("Paper 2 index formula: T2g multiplicity 2 instead of 3",
     [("    return 2 + int(q_ge_rstar or p_gt_PA) + 3 * int(q_ge_qc or p_gt_PT)",
       "    return 2 + int(q_ge_rstar or p_gt_PA) + 2 * int(q_ge_qc or p_gt_PT)")],
     T + "test_complementary_index_derived_from_frozen_table"),
    ("conjugates: copies counted as distinct index types",
     [("            \"index_types\": 1}", "            \"index_types\": 6}")], T + "test_conjugate_branches_one_index_type"),
    ("D3d consistency: transverse eigenvalue sign flipped",
     [("\"transverse_ok\": sp.simplify(ev_tr + 2 * KAP * t) == 0,", "\"transverse_ok\": sp.simplify(ev_tr - 2 * KAP * t) == 0,")],
     T + "test_d3d_consistency"),
    # ---- the validators
    ("validator: m_perp derivation not checked",
     [("    if cor.get(\"m_perp_assumed\") is not False or \"derived\" not in cor.get(\"m_perp_source\", \"\"):",
       "    if False:")], cor_ctl("Paper 2 complementary index assumed")),
    ("validator: rigid-motion counting not checked",
     [("    if cor.get(\"rigid_motions_counted\") is not False or cor.get(\"R24_zero_eigenvalues\") != d[\"R24_zero_eigenvalues\"]:",
       "    if False:")], cor_ctl("rigid motions counted (flag)")),
    ("validator: stability flags not checked",
     [("    for flag in (\"claims_full_space_stability\", \"claims_stability\"):\n        if stmt.get(flag) is not False:",
       "    for flag in ():\n        if stmt.get(flag) is not False:")], prop_ctl("full-space stability from centre index")),
    ("validator: axial-only flag not checked",
     [("    if stmt.get(\"centre_index_uses_axial_curvature_only\") is not False:", "    if False:")],
     prop_ctl("index attributed to the axial curvature only (flag)")),
    ("validator: transverse block type not checked",
     [("    if stmt.get(\"transverse_block\") != d[\"transverse_block\"]:", "    if False:")],
     prop_ctl("transverse block positive definite")),
    ("validator: hessian_e not compared with the derivation",
     [("    cmp(\"hessian_e\", d[\"hessian_e\"])\n", "")], prop_ctl("kappa s replaced by kappa s^2")),
    ("validator: numeric/scan wording not checked and corroboration nodes accepted",
     [("            if v in corr:\n                fails.append(f\"{root}: corroboration/consistency-only node {v} is a proof dependency\")\n"
       "                continue\n",
       "            if v in corr:\n                continue\n")], graph_ctl("B2.2 scan as proof")),
    ("validator: Paper 2 spectrum allowed as a centre-index input",
     [("ALLOWED_INPUTS_B3 = {\n    \"IN_exact_Oh_T2g_structure\": \"VERIFIED-EXACT\",",
       "ALLOWED_INPUTS_B3 = {\n    \"P2_theorem_index_on_curve\": \"FROZEN INPUT\",\n    \"IN_exact_Oh_T2g_structure\": \"VERIFIED-EXACT\",")],
     STMT),
]


def _copy(tmp):
    dst = pathlib.Path(tmp) / "proj"
    shutil.copytree(ROOT, dst, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))
    return dst


def _run(dst, target):
    proc = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", target],
                          cwd=dst, capture_output=True, text=True)
    out = proc.stdout + proc.stderr
    collected = proc.returncode not in (4, 5) and "no tests ran" not in out and "not found:" not in out
    return proc.returncode, collected, out


def main():
    only = set(sys.argv[1:])
    out_path = ROOT / "data" / "B2_5_negative_controls.json"
    prev = json.loads(out_path.read_text()) if (only and out_path.exists()) else {}
    baseline = dict(prev.get("baseline", {}))
    results = {r["mutation"]: r for r in prev.get("results", [])}
    todo = [m for i, m in enumerate(MUTATIONS) if not only or str(i) in only]
    with tempfile.TemporaryDirectory() as tmp:
        dst = _copy(tmp)
        for target in sorted({m[2] for m in todo}):
            code, collected, _ = _run(dst, target)
            baseline[target] = {"passes_unmutated": code == 0 and collected}
            print(f"baseline {'ok ' if code == 0 else 'BAD'} {target}", flush=True)
    for name, edits, target in todo:
        with tempfile.TemporaryDirectory() as tmp:
            dst = _copy(tmp)
            f = dst / F
            text = f.read_text()
            if any(text.count(old) != 1 for old, _ in edits):
                results[name] = {"mutation": name, "file": F, "target": target,
                                 "outcome": "NOT APPLIED (pattern not unique)"}
                print(results[name]["outcome"], name, flush=True)
                continue
            for old, new in edits:
                text = text.replace(old, new)
            f.write_text(text)
            code, collected, out = _run(dst, target)
            detected = collected and code != 0
            results[name] = {"mutation": name, "file": F, "target": target,
                             "outcome": "DETECTED" if detected else "NOT DETECTED"}
            print(results[name]["outcome"], name, flush=True)
    targets = {m[2] for m in MUTATIONS}
    baseline = {k: v for k, v in baseline.items() if k in targets}     # drop entries of retired targets
    ordered = [results[m[0]] for m in MUTATIONS if m[0] in results]
    rec = {"all_detected": len(ordered) == len(MUTATIONS) and all(r["outcome"] == "DETECTED" for r in ordered)
           and all(v["passes_unmutated"] for v in baseline.values()),
           "baseline": dict(sorted(baseline.items())), "n_mutations": len(MUTATIONS),
           "n_detected": sum(r["outcome"] == "DETECTED" for r in ordered), "results": ordered}
    out_path.write_text(json.dumps(rec, indent=1) + "\n")
    print(f"{rec['n_detected']}/{len(MUTATIONS)} detected; all_detected = {rec['all_detected']}")


if __name__ == "__main__":
    main()
