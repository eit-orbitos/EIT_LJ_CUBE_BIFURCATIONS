"""Check that the closed forms printed in manuscript Appendix A agree exactly with the expressions used by the code.

The formulas below are typed independently from paper/appendices/A_closed_forms.tex (not imported from the code)
and compared symbolically with src/cube_bif. Exit status 0 means every printed formula agrees.
Run from the repository root:  python3 paper/tools/check_appendix_closed_forms.py
"""
import sys
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from cube_bif import a2u, b1_cubic, b2_quartic, pairsum as ps  # noqa: E402
from cube_bif.t2g import M_paper2  # noqa: E402

r = ps.r_
X, Y = ps.X["r"], ps.Y["r"]
W = 1 + X + Y / 3
s2, s3, s6 = sp.sqrt(2), sp.sqrt(3), sp.sqrt(6)
R = sp.Rational
P = ps.PSI  # P[(k, sigma)] = psi^{(k)}(sigma)


def psi(k, sig):
    return P[(k, sig)]


failures = []


def same(name, printed, code):
    ok = sp.simplify(sp.together(printed - code)) == 0
    print(f"{'OK  ' if ok else 'FAIL'} {name}")
    if not ok:
        failures.append(name)


# --- A.1  A2u forms for every pair potential --------------------------------------------------------------------
f = a2u.forms()
same("V_aa (psi form)", 8 * psi(1, 1) + 8 * psi(1, 2) + 32 * psi(2, 2), f["V_aa"])
same("V_bb (psi form)", 4 * psi(1, 1) + 8 * psi(1, 2) + 4 * psi(1, 3) + 8 * psi(2, 1) + 32 * psi(2, 2) + 24 * psi(2, 3),
     f["V_bb"])
same("V_aab (psi form)", R(8, 3) * s6 * psi(2, 1) + 16 * s6 * psi(2, 2) + R(64, 3) * s6 * psi(3, 2), f["V_aab"])
same("V_aaaa (psi form)", 16 * psi(2, 1) + 16 * psi(2, 2) + 128 * psi(3, 2) + R(256, 3) * psi(4, 2), f["V_aaaa"])

# --- A.1  two-term difference forms -------------------------------------------------------------------------------
same("h_A", (2 * (r + 1) * X - 4) / W, ps.g_of(f["V_aa"]))
same("g_B", 2 * (r + 1), ps.g_of(f["V_bb"]))
same("g_3", s6 * (r + 2) * (2 - (r + 1) * X) / (3 * W), ps.g_of(f["V_aab"]))
same("g_4", (r + 2) * ((r + 1) * (r + 3) * X + 12) / (3 * W), ps.g_of(f["V_aaaa"]))

# --- A.2  B1 cubic closed forms and M(r) (eq. M of Section 4) -------------------------------------------------------
printed_g = {
    "uuu": (r + 2) * (-R(3, 4) * X + (4 * r + 7) * Y / 27) / W,
    "uuv": s2 * (r + 2) * (4 * r + 1) * Y / (54 * W),
    "uvv": (r + 2) * (-2 + 2 * (r + 1) * Y / 27) / W,
    "vvv": s2 * (r + 2) * (r + 4) * Y / (27 * W),
}
for k, v in printed_g.items():
    same(f"g_{k}", v, b1_cubic.G_CLOSED[k])
M_printed = sp.Matrix([[r * X + R(2, 9) * (2 * r + 1) * Y - 2, R(2, 9) * s2 * (r + 2) * Y],
                       [R(2, 9) * s2 * (r + 2) * Y, 2 * r + R(2, 9) * (r - 1) * Y - 2]]) / W
M_code = M_paper2(r, X, Y)
for i in range(2):
    for j in range(2):
        same(f"M[{i + 1}{j + 1}]", M_printed[i, j], M_code[i, j])

# --- A.3  B2.1 forms for every pair potential -----------------------------------------------------------------------
lf = b2_quartic.linear_forms()
d1 = {s: psi(1, s) for s in (1, 2, 3)}
d2 = {s: psi(2, s) for s in (1, 2, 3)}
d3 = {s: psi(3, s) for s in (1, 2, 3)}
same("h_A (psi form, B2.1)", 4 * d1[1] + 8 * d1[2] + 4 * d1[3] + 8 * d2[1] + 32 * d2[2] + 24 * d2[3], lf["hA"])
same("h_E (psi form, B2.1)", 4 * d1[1] + 8 * d1[2] + 4 * d1[3] + 8 * d2[1] + 8 * d2[2], lf["hE"])
b_printed = {
    "bA_uu": s6 / 3 * (4 * d2[1] + 32 * d2[2] + 28 * d2[3] + 32 * d3[2] + 48 * d3[3]),
    "bE_uu": -s3 / 3 * (4 * d2[1] + 20 * d2[2] + 16 * d2[3] + 32 * d3[2]),
    "bA_uv": 16 * s3 / 3 * (d2[3] + 3 * d3[3]),
    "bE_uv": 4 * s6 / 3 * d2[3],
    "bA_vv": s6 / 3 * (20 * d2[1] + 20 * d2[3] + 8 * d3[1] + 24 * d3[3]),
    "bE_vv": 16 * s3 / 3 * (d2[1] + d2[3] + d3[1]),
}
for k, v in b_printed.items():
    same(f"{k} (psi form)", v, lf[k])

g4_printed = {
    "Q_uuuu": (r + 2) * (162 * r**2 * X + 648 * r * X + 729 * X + 32 * r**2 * Y + 32 * r * Y - 168 * Y + 972) / (648 * W),
    "Q_uuuv": s2 * (r + 2) * (r + 4) * (2 * r + 3) * Y / (81 * W),
    "Q_uuvv": (r + 2) * (81 + (2 * r**2 + 11 * r + 21) * Y) / (81 * W),
    "Q_uvvv": s2 * (r - 3) * (r + 2) * (r + 4) * Y / (81 * W),
    "Q_vvvv": (r + 2) * (81 * r**2 + 324 * r + 729 + (r**2 - 8 * r - 21) * Y) / (81 * W),
    "bA_uu": -s6 * (r + 2) * (9 * r * X + (4 * r + 2) * Y - 18) / (54 * W),
    "bE_uu": s3 * (r + 2) * ((18 * r + 27) * X - 16 * Y - 36) / (108 * W),
    "bA_uv": -2 * s3 * (r + 2) ** 2 * Y / (27 * W),
    "bE_uv": s6 * (r + 2) * Y / (27 * W),
    "bA_vv": -s6 * (r - 1) * (r + 2) * (Y + 9) / (27 * W),
    "bE_vv": -2 * s3 * (r + 2) * (9 * r + 18 - 2 * Y) / (27 * W),
    "hA": 2 * (r + 1),
    "hE": (2 * (r + 1) + (r - 2) * X / 2 - 2 * Y / 3) / W,
}
for k, v in g4_printed.items():
    same(f"g_{k} (closed form)", v, b2_quartic.G4_CLOSED[k])
    same(f"g_{k} (from the psi form)", v, ps.g_of(lf[k]))

print(f"\n{'ALL PRINTED CLOSED FORMS AGREE' if not failures else 'MISMATCH: ' + ', '.join(failures)}")
sys.exit(1 if failures else 0)
