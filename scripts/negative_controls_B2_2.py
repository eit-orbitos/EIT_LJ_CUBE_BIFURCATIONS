"""Negative controls for Phase B2.2: each mutation is applied to a scratch copy of the project and must make the named
test fail. Kept separate from scripts/negative_controls.py so that the earlier script and its record stay
byte-identical. Writes data/B2_2_negative_controls.json."""
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
F = "src/cube_bif/b2_carrier.py"
T = "tests/test_B2_carrier.py::"

MUTATIONS = [
    ("B2.2 corner: values g(q_c) used instead of the derivatives g'(q_c)", F,
     "    G = g_prime_num(qc)\n", "    G = b2.g4_num(qc)\n", T + "test_corner_formulation"),
    ("B2.2 endpoint q = 0: projective kernel sign flipped (rho = +Mh12/Mh22)", F,
     "    rho = -Mh[0, 1] / Mh[1, 1]\n", "    rho = Mh[0, 1] / Mh[1, 1]\n", T + "test_endpoint_q0_formulation"),
    ("B2.2 derivative closed forms: chain-rule sign of dX/dr flipped", F,
     "sp.diff(expr, Xr) * (-L2 / 2 * Xr)", "sp.diff(expr, Xr) * (L2 / 2 * Xr)",
     T + "test_derivative_closed_forms_agree_with_numerical_differentiation"),
    ("B2.2 carrier assembly: unit normalisation (1 + rho^2)^2 -> (1 + rho^2) for Q", F,
     'out = {"Q": Qh / nrm2 ** 2,', 'out = {"Q": Qh / nrm2,', T + "test_corner_formulation"),
    ("B2.2 independent route: q -> 0 limit potential coefficient 7/3 -> 7/4", F,
     "            self.c = mp.mpf(7) / (3 * self.p * _W(self.p))",
     "            self.c = mp.mpf(7) / (4 * self.p * _W(self.p))", T + "test_independent_route_at_the_endpoints"),
    ("B2.2 independent route: corner limit potential, sign of W'/W flipped", F,
     "            self.k = 1 / self.q + _dW(self.q) / _W(self.q)",
     "            self.k = 1 / self.q - _dW(self.q) / _W(self.q)", T + "test_independent_route_at_the_endpoints"),
    ("B2.2 independent route: corner normaliser q_c W_qc -> q_c", F,
     "        return mp.mpf(p_or_q) * _W(mp.mpf(p_or_q))", "        return mp.mpf(p_or_q)",
     T + "test_independent_route_at_the_endpoints"),
    ("B2.2 scan summary: minimum searched over interior rows only (endpoints dropped)", F,
     "    kmin = min(range(len(c)), key=lambda i: c[i])", "    kmin = min(range(1, len(c) - 1), key=lambda i: c[i])",
     T + "test_coarse_scan"),
    ("B2.2 falsification: the 'Eg deleted' variant silently returns the true carrier", F,
     "        return (Q - mp.mpf(3) / 2 * bA ** 2) / nrm2 ** 2", '        return row["c4_hat"]',
     T + "test_falsification_statements_are_exposed"),
]


def main():
    results = []
    for name, rel, old, new, target in MUTATIONS:
        with tempfile.TemporaryDirectory() as tmp:
            dst = pathlib.Path(tmp) / "proj"
            shutil.copytree(ROOT, dst, ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache", "data"))
            f = dst / rel
            text = f.read_text()
            if text.count(old) != 1:
                results.append({"mutation": name, "outcome": "NOT APPLIED (pattern not unique)"})
                print(results[-1]["outcome"], name)
                continue
            f.write_text(text.replace(old, new))
            proc = subprocess.run([sys.executable, "-m", "pytest", "-q", "-x", "-p", "no:cacheprovider", target],
                                  cwd=dst, capture_output=True, text=True)
            failed_by_assertion = "AssertionError" in proc.stdout or "assert " in proc.stdout
            results.append({"mutation": name, "target": target,
                            "outcome": "detected (tests fail)" if proc.returncode != 0 else "NOT DETECTED",
                            "failure_is_an_assertion": failed_by_assertion})
        print(f"{results[-1]['outcome']:28s} {name}")
    ok = all(r["outcome"].startswith("detected") for r in results)
    (ROOT / "data" / "B2_2_negative_controls.json").write_text(
        json.dumps({"all_detected": ok, "controls": results}, indent=1))
    print(f"{sum(r['outcome'].startswith('detected') for r in results)}/{len(results)} detected")
    return ok


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
