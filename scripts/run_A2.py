"""Phase A2 — build the Lemma M certificate, check it independently, run the method's negative controls.

Writes data/A2_lemma_M_certificate.json, data/A2_CERTIFICATE_SEMANTIC.sha256, data/A2_negative_controls.json and
data/A2_theorem_A_dependencies.json (the machine-readable statement and proof dependency graph of Theorem A).
"""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from flint import fmpq  # noqa: E402

from cube_bif import certcheck, lemma_m, theorem_a  # noqa: E402


def method_controls():
    """The same certification method must fail where the claim is false."""
    ev = lemma_m.Evaluator()
    out = []
    for name, lo, hi, sign, bound in [
        ("beyond the monotonicity range: [7, 8] (m' changes sign near 7.649)", fmpq(7), fmpq(8), 1, fmpq(0)),
        ("entirely beyond: [8, 9] (m' < 0)", fmpq(8), fmpq(9), 1, fmpq(0)),
        ("negated function: -m' > 0 on [0, 16/5]", fmpq(0), fmpq(16, 5), -1, fmpq(0)),
        ("bound above the infimum: m' > 31/50 on [0, 1/10] (m'(0) = 0.61697...)", fmpq(0), fmpq(1, 10), 1,
         fmpq(31, 50)),
    ]:
        res = lemma_m.certify(lo, hi, sign=sign, bound=bound, ev=ev)
        out.append({"control": name, "certified": res["ok"],
                    "outcome": "fails as required" if not res["ok"] else "UNEXPECTEDLY CERTIFIED",
                    "failure_box": res.get("failure")})
    # positive control: the same method on a sub-interval where the claim is true
    res = lemma_m.certify(fmpq(1), fmpq(2), ev=ev)
    out.append({"control": "positive control: m' > 0 on [1, 2]", "certified": res["ok"],
                "outcome": "certified as required" if res["ok"] else "UNEXPECTEDLY FAILED"})
    return out


def main():
    cert = lemma_m.build_certificate(ROOT)
    (ROOT / "data" / "A2_lemma_M_certificate.json").write_text(json.dumps(cert, indent=1))
    h = cert["provenance"]["semantic_sha256"]
    (ROOT / "data" / "A2_CERTIFICATE_SEMANTIC.sha256").write_text(f"{h}  A2_lemma_M_certificate.json (semantic)\n")
    ok, rep = certcheck.check(cert, h)
    controls = method_controls()
    (ROOT / "data" / "A2_negative_controls.json").write_text(json.dumps(
        {"all_as_required": all(c["outcome"].endswith("as required") for c in controls), "controls": controls},
        indent=1, default=str))
    (ROOT / "data" / "A2_theorem_A_dependencies.json").write_text(
        json.dumps(theorem_a.as_record(), indent=1, ensure_ascii=False))
    print(f"certificate: {cert['n_boxes']} boxes, max depth {cert['max_depth_used']}, "
          f"min lower bound {cert['min_lower_bound']} = {cert['min_lower_bound_decimal']}")
    print("near zero:", cert["near_zero"]["m'(0) exact"], "| m'' > 0 on [0, 1/8]:", cert["near_zero"]["all_positive"])
    print("P_A bound:", cert["P_A_bound"]["all_certified"], cert["P_A_bound"]["h_A(16/5) enclosure"])
    print("independent check:", ok, rep)
    for c in controls:
        print(f"  {c['outcome']:26s} {c['control']}")
    print("semantic sha256:", h, "| seconds:", cert["provenance"]["seconds"])
    return ok


if __name__ == "__main__":
    sys.exit(0 if main() else 1)
