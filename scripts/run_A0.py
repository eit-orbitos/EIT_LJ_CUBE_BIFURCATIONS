"""Phase A0 — exact A2u representation audit. Writes data/A0_representation.json."""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import sympy as sp  # noqa: E402

from cube_bif import STATUS, __version__  # noqa: E402
from cube_bif.group import (CHARACTERS, D24, LABELS, average, character, element_type, oh_matrices,  # noqa: E402
                            point_group_label, projector, sigma, type_counts)
from cube_bif.modes import E_A, E_BR, ROTATIONS, TRANSLATIONS, Y_STAR  # noqa: E402


def ip(u, v):
    return (u.T * v)[0, 0]


def main():
    G = oh_matrices()
    mult = {ir: int(projector(ir).trace()) // CHARACTERS[ir][0] for ir in CHARACTERS}
    elements = []
    for k, R in enumerate(G):
        elements.append({"index": k, "matrix": [[int(R[i, j]) for j in range(3)] for i in range(3)],
                         "type": element_type(R), "sigma": sigma(R), "chi_A2u": character("A2u", R),
                         "D(R)E_A == chi E_A": bool(D24(R) * E_A == character("A2u", R) * E_A)})
    stab = [R for R in G if D24(R) * E_A == E_A]
    P_fix = average(stab, D24)
    fix_basis_ok = bool(P_fix * E_A == E_A and P_fix * E_BR == E_BR)
    inv = sp.ImmutableMatrix(-sp.eye(3))
    out = {
        "project": "EIT-LJ Cube Bifurcations (Paper 3)", "version": __version__, "status": STATUS,
        "convention": "labels s in {-1,1}^3 (itertools.product order), y*_s = s/2, (D(R)x)_{Rs} = R x_s (Paper 2)",
        "labels": LABELS,
        "E_A_field": {str(s): [int(c) * s[0] * s[1] * s[2] for c in s] for s in LABELS},
        "e_A": "E_A / sqrt(24),  E_A(s) = (s1 s2 s3) s",
        "checks": {
            "|E_A|^2 = 24": ip(E_A, E_A) == 24,
            "<E_A, translations> = 0": all(ip(E_A, t) == 0 for t in TRANSLATIONS),
            "<E_A, rotations> = 0": all(ip(E_A, r) == 0 for r in ROTATIONS),
            "<E_A, E_BR> = 0 (orthogonal to uniform scaling)": ip(E_A, E_BR) == 0,
            "E_A radial at every vertex (E_A(s) parallel to s)": all(
                sp.Matrix(E_A[3 * i:3 * i + 3]).cross(sp.Matrix(s)) == sp.zeros(3, 1) for i, s in enumerate(LABELS)),
            "D(R) E_A = chi_A2u(R) E_A for all 48 R": all(e["D(R)E_A == chi E_A"] for e in elements),
            "sigma(R) = chi_A2u(R) for all 48 R": all(e["sigma"] == e["chi_A2u"] for e in elements),
            "A2u isotypic projector has rank 1 and fixes E_A": bool(projector("A2u").rank() == 1
                                                                     and projector("A2u") * E_A == E_A),
            "inversion: D(-I) E_A = -E_A": bool(D24(inv) * E_A == -E_A),
            "inversion fixes the cube: D(-I) y* = y*": bool(D24(inv) * Y_STAR == Y_STAR),
            "Fix(Sigma_A) = span{E_BR, E_A} (rank 2, contains both)": bool(P_fix.rank() == 2 and fix_basis_ok),
        },
        "multiplicities_R24": mult,
        "stabilizer_Sigma_A": {"order": len(stab), "types": type_counts(stab), "label": point_group_label(stab),
                               "elements": [[[int(R[i, j]) for j in range(3)] for i in range(3)] for R in stab]},
        "elements": elements,
    }
    out["all_checks_pass"] = all(out["checks"].values())
    (ROOT / "data" / "A0_representation.json").write_text(json.dumps(out, indent=1, default=str))
    for k, v in out["checks"].items():
        print(f"{'PASS' if v else 'FAIL'}  {k}")
    print("multiplicities:", mult)
    print("Sigma_A:", len(stab), point_group_label(stab), type_counts(stab))
    return out


if __name__ == "__main__":
    main()
