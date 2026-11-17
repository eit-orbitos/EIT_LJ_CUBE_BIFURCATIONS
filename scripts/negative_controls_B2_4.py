"""Code-mutation controls for Phase B2.4 (src/cube_bif/b2_branch.py). Each mutation is applied to a scratch copy of the
project and must make the named test of tests/test_B2_branch.py fail. Every target is first run on an unmutated copy
and must pass there. The mutations cover the required failure classes: wrong sign of tau, wrong sign of c4, missing
factor 6, removal of evenness, a branch claimed on both sides, the B2.2 scan used as proof instead of Lemma Q, and the
axial curvature upgraded to full-space stability; plus validator and derivation sabotage. Kept separate from the
earlier control scripts so that they and their records stay byte-identical. Writes data/B2_4_negative_controls.json.
"""
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
F = "src/cube_bif/b2_branch.py"
T = "tests/test_B2_branch.py::"
STMT = T + "test_proposition_statement_is_valid"
GRAPH = T + "test_dependency_graph_is_valid"


def stmt_ctl(name):
    return T + f"test_incorrect_statement_is_rejected[{name}]"


def graph_ctl(name):
    return T + f"test_invalid_dependency_graph_is_rejected[{name}]"


MUTATIONS = [
    # ---- the derivation (exact layer)
    ("wrong sign of tau: G_mu = -tau", [("    return (tau * mu + c4 * z / FACTOR", "    return (-tau * mu + c4 * z / FACTOR")],
     T + "test_ift_slope_and_amplitude_law"),
    ("wrong sign of tau: the derived branch side ignores the sign of tau",
     [("    m1 = ift_branch(_signed(tau_sign, \"tau\"), _signed(c4_sign, \"c4\"))[\"m1\"]",
       "    m1 = ift_branch(_signed(\"<0\", \"tau\"), _signed(c4_sign, \"c4\"))[\"m1\"]")],
     T + "test_branch_side_is_derived_from_the_signs"),
    ("wrong sign of c4: '>0' mapped to a negative symbol",
     [("    if sign == \">0\":\n        return sp.Symbol(name + \"_abs\", positive=True)",
       "    if sign == \">0\":\n        return -sp.Symbol(name + \"_abs\", positive=True)")],
     T + "test_branch_side_is_derived_from_the_signs"),
    ("missing factor 6: G_z = c4", [("FACTOR = 6          # G_z(0, 0) = c4 / FACTOR",
                                     "FACTOR = 1          # G_z(0, 0) = c4 / FACTOR")], STMT),
    ("removal of evenness: odd monomials in the generic energy",
     [("        for e in _monomials(deg):", "        for e in _monomials(deg, even=False):")],
     T + "test_generic_even_LS_expansion"),
    ("transverse solve dropped (energy along the kernel line only)",
     [("        ak = (-Hinv * r).applyfunc(sp.simplify)", "        ak = (0 * r).applyfunc(sp.simplify)")],
     T + "test_generic_even_LS_expansion"),
    ("branch claimed on both sides (branch_side returns mu != 0)",
     [("    if m1.is_positive:\n        return \"mu > 0\"", "    if True:\n        return \"mu != 0\"")], STMT),
    ("classification swapped", [("    if cube_curv.is_negative and branch_curv.is_positive:\n        return \"supercritical\"",
                                 "    if cube_curv.is_negative and branch_curv.is_positive:\n        return \"subcritical\"")],
     T + "test_classification_in_the_energy_reduced_axial_convention"),
    ("axial curvature on the branch without the factor 2",
     [("    on_branch = sp.expand((2 * z * sp.diff(G, z)).subs(z, Zmu))",
       "    on_branch = sp.expand((z * sp.diff(G, z)).subs(z, Zmu))")], T + "test_axial_curvature_leading_terms"),
    ("exchange expectation: reversing elements assumed to fix f_1 and e_1",
     [("{\"A1g\": 1, \"Eg\": 1, \"T2g_u\": -1, \"T2g_v\": -1}", "{\"A1g\": 1, \"Eg\": 1, \"T2g_u\": 1, \"T2g_v\": 1}")],
     T + "test_reversing_elements_exchange_plus_and_minus_branches"),
    # ---- the statement
    ("statement upgrades the axial curvature to full-space stability",
     [("    \"claims_full_space_stability\": False,", "    \"claims_full_space_stability\": True,")], STMT),
    ("statement drops the factor 6 in the amplitude law",
     [("    \"amplitude_law\": \"-6*tau*mu/c4\",", "    \"amplitude_law\": \"-tau*mu/c4\",")], STMT),
    # ---- the dependency graph
    ("B2.2 scan used instead of Lemma Q (graph edge)",
     [("        [\"L2_ift_branch\", \"LQ_lemma_Q\"],", "        [\"L2_ift_branch\", \"N_B22_scan\"],")], GRAPH),
    ("B2.2 scan added as a proof dependency (graph edge)",
     [("        [\"L2_ift_branch\", \"STD_implicit_function_theorem\"],",
       "        [\"L2_ift_branch\", \"STD_implicit_function_theorem\"], [\"L2_ift_branch\", \"N_B22_scan\"],")], GRAPH),
    ("graph: an unlisted input (Paper 2 Lemma S as a separate leaf) added",
     [("        [\"X_generic_LS\", \"STD_lyapunov_schmidt\"],",
       "        [\"X_generic_LS\", \"STD_lyapunov_schmidt\"], [\"X_generic_LS\", \"P2_lemma_S\"],"),
      ("    \"nodes\": [\n",
       "    \"nodes\": [\n"
       "        {\"id\": \"P2_lemma_S\", \"role\": \"input\", \"status\": \"FROZEN INPUT\", "
       "\"statement\": \"Paper 2 Lemma S: h_A, h_E > 0\"},\n")], GRAPH),
    # ---- the validator
    ("validator: corroboration-only nodes accepted as proof",
     [("            fails.append(f\"corroboration-only node {v} is a proof dependency\")\n", "            pass\n")],
     graph_ctl("B2.4 numerical branch points used as proof")),
    ("validator: VERIFIED-NUMERIC accepted as a proof status",
     [("ALLOWED_PROOF_STATUSES = (\"VERIFIED-EXACT\", \"CERTIFIED\", \"FROZEN INPUT\", \"STANDARD\")",
       "ALLOWED_PROOF_STATUSES = (\"VERIFIED-EXACT\", \"CERTIFIED\", \"FROZEN INPUT\", \"STANDARD\", \"VERIFIED-NUMERIC\")"),
      ("FORBIDDEN_PROOF_STATUSES = (\"VERIFIED-NUMERIC\", \"CANDIDATE\", \"RECONNAISSANCE\")",
       "FORBIDDEN_PROOF_STATUSES = (\"CANDIDATE\", \"RECONNAISSANCE\")")],
     graph_ctl("Lemma Q replaced by a VERIFIED-NUMERIC claim")),
    ("validator: full-space stability and centre-manifold claims not checked",
     [("    for flag in (\"claims_full_space_stability\", \"claims_centre_manifold_index\", \"claims_cuboid\"):",
       "    for flag in (\"claims_cuboid\",):")], stmt_ctl("axial curvature upgraded to full-space stability")),
    ("validator: branch on both sides not checked",
     [("    if stmt.get(\"branch_on_both_sides\") is not False or stmt.get(\"nontrivial_equilibria_on_other_side\") != 0:",
       "    if False:")], stmt_ctl("branch claimed on both sides")),
    ("validator: input signs not checked", [("    if stmt.get(\"inputs\") != d[\"inputs\"]:", "    if False:")],
     stmt_ctl("wrong sign of tau")),
    ("validator: the six-input restriction not enforced",
     [("            fails.append(f\"node {v} is not one of the six allowed proof inputs {sorted(ALLOWED_INPUTS)}\")\n",
       "            pass\n")],
     graph_ctl("unlisted input added (B1 Lemma K)")),
    ("validator: evenness flag not checked",
     [("    if stmt.get(\"even_in_s\") is not True or not d[\"even_in_s\"]:", "    if False:")],
     stmt_ctl("removal of evenness (flag)")),
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
    only = set(sys.argv[1:])            # optional subset of mutation indices (for chunked runs); merged into the record
    out_path = ROOT / "data" / "B2_4_negative_controls.json"
    prev = json.loads(out_path.read_text()) if (only and out_path.exists()) else {}
    baseline = dict(prev.get("baseline", {}))
    results = {r["mutation"]: r for r in prev.get("results", [])}
    todo = [m for i, m in enumerate(MUTATIONS) if not only or str(i) in only]
    with tempfile.TemporaryDirectory() as tmp:
        dst = _copy(tmp)
        for target in sorted({m[2] for m in todo}):
            code, collected, _ = _run(dst, target)
            baseline[target] = {"passes_unmutated": code == 0 and collected}
            print(f"baseline {'ok ' if code == 0 else 'BAD'} {target}")
    for name, edits, target in todo:
        with tempfile.TemporaryDirectory() as tmp:
            dst = _copy(tmp)
            f = dst / F
            text = f.read_text()
            if any(text.count(old) != 1 for old, _ in edits):
                results[name] = {"mutation": name, "file": F, "target": target,
                                 "outcome": "NOT APPLIED (pattern not unique)"}
                print(results[name]["outcome"], name)
                continue
            for old, new in edits:
                text = text.replace(old, new)
            f.write_text(text)
            code, collected, out = _run(dst, target)
            detected = collected and code != 0
            results[name] = {"mutation": name, "file": F, "target": target,
                             "outcome": "DETECTED" if detected else "NOT DETECTED"}
            print(results[name]["outcome"], name)
    ordered = [results[m[0]] for m in MUTATIONS if m[0] in results]
    rec = {"all_detected": len(ordered) == len(MUTATIONS) and all(r["outcome"] == "DETECTED" for r in ordered)
           and all(v["passes_unmutated"] for v in baseline.values()),
           "baseline": dict(sorted(baseline.items())), "n_mutations": len(MUTATIONS),
           "n_detected": sum(r["outcome"] == "DETECTED" for r in ordered), "results": ordered}
    out_path.write_text(json.dumps(rec, indent=1) + "\n")
    print(f"{rec['n_detected']}/{len(MUTATIONS)} detected; all_detected = {rec['all_detected']}")


if __name__ == "__main__":
    main()
