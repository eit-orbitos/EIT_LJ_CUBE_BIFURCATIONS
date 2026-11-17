"""Negative controls: each mutation is applied to a scratch copy of the project and must make the named tests fail.
A control that still passes means the test cannot see that error. Writes data/negative_controls.json."""
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]

MUTATIONS = [
    ("A2u field uses s1 s2 instead of s1 s2 s3", "src/cube_bif/modes.py",
     "E_A = field(lambda s: [parity(s) * c for c in s])", "E_A = field(lambda s: [s[0] * s[1] * c for c in s])",
     "tests/test_A0_representation.py"),
    ("character table: A2u sign on C4 flipped", "src/cube_bif/group.py",
     '"A2u": [1, 1, -1, -1, 1, -1, 1, -1, -1, 1]', '"A2u": [1, 1, -1, 1, 1, -1, 1, -1, -1, 1]',
     "tests/test_A0_representation.py"),
    ("D4 Faa di Bruno coefficient 8 -> 6", "src/cube_bif/pairsum.py",
     "add(3, sig, 8 * s3)", "add(3, sig, 6 * s3)", "tests/test_A1_quartic.py::test_full_energy_and_scale_free_c4_agree_on_curve"),
    ("scale-free chain constant: u-rescaling sqrt6 -> sqrt5", "src/cube_bif/a2u.py",
     "uu = sp.log((1 - al / sp.sqrt(6)) / (1 + al / sp.sqrt(6)))", "uu = sp.log((1 - al / sp.sqrt(5)) / (1 + al / sp.sqrt(5)))",
     "tests/test_A1_quartic.py::test_scale_free_chain_constant"),
    ("c4 numeric route: factor 3 -> 2 in the LS correction", "src/cube_bif/numeric.py",
     '"c4": V4 - 3 * bHb', '"c4": V4 - 2 * bHb', "tests/test_A1_quartic.py::test_c4_by_the_24D_numeric_route"),
    ("frozen r* last digit changed", "src/cube_bif/paper2_ref.py",
     '"r_star": "1.4749107381472217442"', '"r_star": "1.4749107381472217452"',
     "tests/test_A1_quartic.py::test_r_star_and_P_A_soft_match_frozen_constants"),
    ("T2g representation without the sigma(R) factor", "src/cube_bif/t2g.py",
     "    return sigma(R) * R\n", "    return R\n", "tests/test_B0_t2g.py"),
    ("Paper 2 M(r): off-diagonal (r+2) -> (r+1)", "src/cube_bif/t2g.py",
     "2 * sp.sqrt(2) * (rr + 2) / 9 * Y_],\n                      [2 * sp.sqrt(2) * (rr + 2) / 9 * Y_,",
     "2 * sp.sqrt(2) * (rr + 1) / 9 * Y_],\n                      [2 * sp.sqrt(2) * (rr + 1) / 9 * Y_,",
     "tests/test_B0_t2g.py::test_block_factorises_through_paper2_M"),
    ("isotropy: normaliser action ignored (always +1)", "src/cube_bif/t2g.py",
     "acts = sorted({int(((T3(g) * v).T * v)[0, 0] / (v.T * v)[0, 0]) for g in N})", "acts = [1]",
     "tests/test_B0_t2g.py::test_branch_types_from_invariant_and_normalizer"),
    # Phase A2 (Lemma M certificate)
    ("A2 generator: dx/dr sign flipped in the chain rule", "src/cube_bif/lemma_m.py",
     "sp.diff(e, x) * (-L2 / 2 * x)", "sp.diff(e, x) * (L2 / 2 * x)",
     "tests/test_A2_certificate.py::test_fresh_certificate_passes_the_independent_checker"),
    ("A2 generator: mean-value remainder dropped (point value used as box bound)", "src/cube_bif/lemma_m.py",
     "return sign * (self.m1(rc) + (rb - rc) * self.m2(rb))", "return sign * self.m1(rc)",
     "tests/test_A2_certificate.py::test_fresh_certificate_passes_the_independent_checker"),
    ("A2 generator: lower bound raised by 2^-8 above its enclosure, Arb check removed (false on the first box)",
     "src/cube_bif/lemma_m.py",
     ("n = math.floor(v * 2 ** bits) - 1", "    while not (E > arb(q)):"),
     ("n = math.floor(v * 2 ** bits) + 4096", "    while False:"),
     "tests/test_A2_certificate.py::test_fresh_certificate_passes_the_independent_checker"),
    ("A2 checker: coverage test disabled", "src/cube_bif/certcheck.py",
     "if any(his[i] != los[i + 1] for i in range(len(boxes) - 1)):",
     "if False and any(his[i] != los[i + 1] for i in range(len(boxes) - 1)):",
     "tests/test_A2_certificate.py::test_rejects_a_gap"),
    ("A2 checker: claim not compared", "src/cube_bif/certcheck.py",
     'if cert.get("claim") != EXPECTED_CLAIM:', 'if False:',
     "tests/test_A2_certificate.py::test_rejects_a_flipped_relation"),
    ("A2 checker: positivity of lower bounds not required", "src/cube_bif/certcheck.py",
     "if any(not (lb > 0) for lb in lbs):", "if False:",
     "tests/test_A2_certificate.py::test_rejects_a_nonpositive_lower_bound"),
    # Phase A2 (Theorem A dependency graph)
    ("Theorem A graph: transversality (H3) dropped from the theorem's dependencies", "src/cube_bif/theorem_a.py",
     '"uses": ["H0", "H1", "H2", "H3", "H4", "reduction", "branch side"],',
     '"uses": ["H0", "H1", "H2", "H4", "reduction", "branch side"],',
     "tests/test_A2_theorem.py::test_hypotheses_H1_to_H4_are_dependencies_of_theorem_A"),
    ("Theorem A graph: a numerical check listed as a proof dependency of the branch side", "src/cube_bif/theorem_a.py",
     '"tests": [A2T + "test_branch_side_from_the_reduced_equation",',
     '"tests": [A2T + "test_signs_of_the_reduced_equation_at_curve_points",\n'
     '                              A2T + "test_branch_side_from_the_reduced_equation",',
     "tests/test_A2_theorem.py::test_no_numerical_check_is_a_dependency"),
    # Phase B1 (cubic coefficient on the T2g curve)
    ("B1 exact layer: coefficient 54 -> 52 in the closed form g_uuv", "src/cube_bif/b1_cubic.py",
     '"uuv": S2 * (r + 2) * (4 * r + 1) * Yr / (54 * WR),', '"uuv": S2 * (r + 2) * (4 * r + 1) * Yr / (52 * WR),',
     "tests/test_B1_exact.py::test_each_coefficient_is_an_exact_difference_form"),
    ("B1 generator: wrong kernel vector (rho = +Mh12/Mh22) in the carrier", "src/cube_bif/b1_cert.py",
     '    rho = -val["M12"] / c\n', '    rho = val["M12"] / c\n',
     "tests/test_B1_certificate.py::test_fresh_certificate_passes_the_independent_checker"),
    ("B1 generator: centre value used as the box bound (mean-value slopes dropped)", "src/cube_bif/b1_cert.py",
     "    kh = k0 + kq * (Q - q0) + kd * (D - d0)", "    kh = k0",
     "tests/test_B1_certificate.py::test_fresh_certificate_passes_the_independent_checker"),
    ("B1 generator: lower bound placed above the enclosure, Arb confirmation removed", "src/cube_bif/b1_cert.py",
     ("    k = ((lo - margin * (hi - lo)) * s).floor() - 1", "    while not (E > arb(fmpq(k, s))):"),
     ("    k = (hi * s).floor() + 1", "    while False:"),
     "tests/test_B1_certificate.py::test_fresh_certificate_passes_the_independent_checker"),
    ("B1 checker: coverage test disabled", "src/cube_bif/b1_check.py",
     '        if _q(a["q_hi"]) != _q(b["q_lo"]):', "        if False:",
     "tests/test_B1_certificate.py::test_tampered_certificate_is_rejected"),
    ("B1 checker: Newton inclusion not required", "src/cube_bif/b1_check.py",
     "    return Nw if (Nw.lower() > D.lower() and Nw.upper() < D.upper()) else None", "    return Nw",
     "tests/test_B1_certificate.py::test_tampered_certificate_is_rejected"),
    ("B1 checker: stored expressions not compared with the derivation", "src/cube_bif/b1_check.py",
     "        if k not in ex or sp.simplify(_stored(ex[k]) - funcs[k]) != 0:", "        if k not in ex:",
     "tests/test_B1_certificate.py::test_tampered_certificate_is_rejected"),
    # Phase B2.0 (exact symmetry audit of the D2h axis)
    ("B2.0: fixed Eg vector replaced by the orthorhombic yz direction (the relayed claim's Eg(2))",
     "src/cube_bif/b2_symmetry.py", "E_HAT = E_TET_X / sp.sqrt(48)", "E_HAT = E_ORTH_YZ / sp.sqrt(16)",
     "tests/test_B2_symmetry.py::test_explicit_orthonormal_basis_of_the_fixed_space"),
    ("B2.0: projector averaged over O_h instead of the stabiliser", "src/cube_bif/b2_symmetry.py",
     "    return sp.ImmutableMatrix(average(axis_stabilizer(), D24))",
     "    return sp.ImmutableMatrix(average(oh_matrices(), D24))",
     "tests/test_B2_symmetry.py::test_isotypic_decomposition_of_the_fixed_space"),
    ("B2.0: mixed channel weight 2 -> 1 in b(n)", "src/cube_bif/b2_symmetry.py",
     '    return (n_u ** 2 * bc["uu"] + 2 * n_u * n_v * bc["uv"] + n_v ** 2 * bc["vv"]).applyfunc(sp.expand)',
     '    return (n_u ** 2 * bc["uu"] + n_u * n_v * bc["uv"] + n_v ** 2 * bc["vv"]).applyfunc(sp.expand)',
     "tests/test_B2_quartic.py::test_route2a_raw_b_vector_equals_the_B2_0_vector"),
    # Phase B2.1 (quartic coefficient, three routes)
    ("B2.1 route 1: back-reaction factor 3 -> 2", "src/cube_bif/b2_quartic.py",
     "    c4h_chart = Qh - 3 * bAh ** 2 / hAh - 3 * bEh ** 2 / hEh",
     "    c4h_chart = Qh - 2 * bAh ** 2 / hAh - 2 * bEh ** 2 / hEh",
     "tests/test_B2_quartic.py::test_route2_numeric_raw_24D_agrees"),
    ("B2.1 route 1: Eg back-reaction dropped (A1g only)", "src/cube_bif/b2_quartic.py",
     "    c4h_chart = Qh - 3 * bAh ** 2 / hAh - 3 * bEh ** 2 / hEh", "    c4h_chart = Qh - 3 * bAh ** 2 / hAh",
     "tests/test_B2_quartic.py::test_route2_numeric_raw_24D_agrees"),
    ("B2.1 route 1: binomial weight of the uuvv channel 6 -> 4", "src/cube_bif/b2_quartic.py",
     'Q_BINOM = {"uuuu": 1, "uuuv": 4, "uuvv": 6, "uvvv": 4, "vvvv": 1}',
     'Q_BINOM = {"uuuu": 1, "uuuv": 4, "uuvv": 4, "uvvv": 4, "vvvv": 1}',
     "tests/test_B2_quartic.py::test_route2a_raw_quartic_equals_route1"),
    ("B2.1 closed form: bE_uv denominator 27 -> 26", "src/cube_bif/b2_quartic.py",
     '    "bE_uv": S6 * Yr * (r + 2) / (27 * WR),', '    "bE_uv": S6 * Yr * (r + 2) / (26 * WR),',
     "tests/test_B2_quartic.py::test_closed_forms_match_pairsum_and_have_no_division_by_r"),
    ("B2.1 route 2: b as the first instead of the second derivative of the gradient along e_1",
     "src/cube_bif/b2_quartic.py",
     "    b = [mp.diff(lambda a, i=i: V.gradient(shift(y0, (a, e)))[i], 0, 2) for i in range(24)]",
     "    b = [mp.diff(lambda a, i=i: V.gradient(shift(y0, (a, e)))[i], 0, 1) for i in range(24)]",
     "tests/test_B2_quartic.py::test_route2_numeric_raw_24D_agrees"),
    ("B2.1 route 3: transverse coordinates not solved (energy along the kernel line only)",
     "src/cube_bif/b2_quartic.py", "            step = mp.lu_solve(Hm, g)", "            step = mp.matrix([0, 0, 0])",
     "tests/test_B2_quartic.py::test_route3_restricted_family_agrees"),
    ("B2.1 route 3: Richardson ratio 4 -> 2", "src/cube_bif/b2_quartic.py",
     "            T[j].append((4 ** k * T[j][k - 1] - T[j - 1][k - 1]) / (4 ** k - 1))",
     "            T[j].append((2 ** k * T[j][k - 1] - T[j - 1][k - 1]) / (2 ** k - 1))",
     "tests/test_B2_quartic.py::test_route3_restricted_family_agrees"),
]


def main():
    results = []
    for name, rel, old, new, target in MUTATIONS:
        with tempfile.TemporaryDirectory() as tmp:
            dst = pathlib.Path(tmp) / "proj"
            shutil.copytree(ROOT, dst, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache", "data"))
            f = dst / rel
            text = f.read_text()
            olds, news = (old, new) if isinstance(old, tuple) else ((old,), (new,))
            if any(text.count(o) != 1 for o in olds):
                results.append({"mutation": name, "outcome": "NOT APPLIED (pattern not unique)"})
                continue
            for o, n_ in zip(olds, news):
                text = text.replace(o, n_)
            f.write_text(text)
            proc = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", target],
                                  cwd=dst, capture_output=True, text=True)
            results.append({"mutation": name, "target": target,
                            "outcome": "detected (tests fail)" if proc.returncode != 0 else "NOT DETECTED"})
        print(f"{results[-1]['outcome']:28s} {name}")
    ok = all(r["outcome"].startswith("detected") for r in results)
    (ROOT / "data" / "negative_controls.json").write_text(json.dumps({"all_detected": ok, "controls": results}, indent=1))
    print(f"{sum(r['outcome'].startswith('detected') for r in results)}/{len(results)} detected")
    return ok


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
