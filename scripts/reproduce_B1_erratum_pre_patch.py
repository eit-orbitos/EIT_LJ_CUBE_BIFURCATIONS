"""Erratum E-B1: reproduce the defect on the UNMODIFIED V0.4-dev.3 code (before the patch).

Usage: python scripts/reproduce_B1_erratum_pre_patch.py <EIT_LJ_CUBE_BIFURCATIONS_V0.4-dev.3.zip>

The archive is checked against its SHA-256, extracted to a temporary directory, and its own b1_cert._taylor and
b1_check.Model.taylor are run in a fresh interpreter under python-flint's default ctx.cap = 10. Nothing of this
project is imported by the child. It also rebuilds the B1 certificate with the V0.4-dev.3 generator under the
conditions of scripts/run_B1.py (mpmath at 40 digits) and compares the semantic hash with the historical one, which
shows that this environment reproduces the historical build. Writes data/B1_ERRATUM_pre_patch_reproduction.json.
"""
import hashlib
import json
import pathlib
import subprocess
import sys
import tempfile
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
DEV3_SHA256 = "cf331557f9cf6fd074920368a69268c331e4c84d1f3b64fd89b421a3b45d5c81"

CHILD = r'''
import json, sys, pathlib
root = pathlib.Path(sys.argv[1]); sys.path.insert(0, str(root / "src"))
import flint, mpmath as mp, sympy as sp
from flint import arb, arb_series, ctx, fmpq
from cube_bif import b1_cert, b1_check, __version__
NAMES = ("M11", "M12", "M22", "uuu", "uuv", "uvv", "vvv")
out = {"project_version_of_the_code_run": __version__, "python-flint": flint.__version__,
       "default_ctx_cap": ctx.cap}
assert ctx.cap == 10
out["arb_series exp, prec=16, ctx.cap=10: coefficients returned"] = len(arb_series([arb(1), 1], prec=16).exp().coeffs())
r = sp.Symbol("r"); X, Y = 2 ** (-r / 2), 3 ** (-r / 2)
loc = {"r": r, "X": X, "Y": Y, "W": 1 + X + Y / 3, "sqrt": sp.sqrt}
f = {k: sp.lambdify(r, sp.sympify(b1_cert.EXPRESSIONS[k], locals=loc), "mpmath") for k in NAMES}
def inside(ball, x):
    with mp.workdps(70):
        return bool(ball.contains(arb(mp.nstr(x, 55))))
# 1. Taylor coefficients at r = 1 against mpmath (60 digits)
with mp.workdps(60):
    ref = {k: mp.taylor(f[k], mp.mpf(1), 23) for k in NAMES}
ctx.prec = 128
g = b1_cert._taylor(arb(1), 16)
out["generator b1_cert._taylor(1, 16): c_10..c_15 all exactly zero"] = all(g[k][j] == 0 for k in NAMES for j in range(10, 16))
out["generator: coefficients c_10..c_15 whose enclosure excludes the mpmath value"] = sum(
    not inside(g[k][j], ref[k][j]) for k in NAMES for j in range(10, 16))
out["generator: coefficients c_0..c_9 enclosing the mpmath value"] = sum(inside(g[k][j], ref[k][j]) for k in NAMES for j in range(10))
model = b1_check.Model({k: b1_check._stored(b1_cert.EXPRESSIONS[k]) for k in NAMES})
ctx.prec = 160
c = model.taylor(arb(1), 20)
out["checker b1_check.Model.taylor(1, 20): c_10..c_19 all exactly zero"] = all(c[k][j] == 0 for k in NAMES for j in range(10, 20))
out["checker: coefficients c_10..c_19 whose enclosure excludes the mpmath value"] = sum(
    not inside(c[k][j], ref[k][j]) for k in NAMES for j in range(10, 20))
with mp.workdps(60):
    out["example: M22 c_12 at r = 1, mpmath"] = mp.nstr(ref["M22"][12], 20)
out["example: M22 c_12 at r = 1, V0.4-dev.3 generator"] = g["M22"][12].str(20)
# 2. the diagnostic point (q, delta) = (1.9, 0.9)
with mp.workdps(60):
    q, d = mp.mpf(19) / 10, mp.mpf(9) / 10
    quo = {k: (f[k](q + d) - f[k](q)) / d for k in NAMES}
ctx.prec = 128
gd = b1_cert.divided(arb(fmpq(19, 10)), arb(fmpq(9, 10)), "near")[0]
ctx.prec = 160
cd = model.dd(arb(fmpq(19, 10)), arb(fmpq(9, 10)), "near")[0]
out["diagnostic point"] = {"q": "19/10", "delta": "9/10"}
out["generator divided differences excluding the 60-digit quotient"] = [k for k in NAMES if not inside(gd[k], quo[k])]
out["checker divided differences excluding the 60-digit quotient"] = [k for k in NAMES if not inside(cd[k], quo[k])]
with mp.workdps(70):
    errs = {k: abs(mp.mpf(gd[k].mid().str(60, radius=False)) - quo[k]) for k in NAMES}
w = max(NAMES, key=lambda k: errs[k])
out["worst generator divided difference"] = {"function": w, "enclosure": gd[w].str(25),
    "radius": gd[w].rad().str(3, radius=False), "mpmath quotient": mp.nstr(quo[w], 25),
    "midpoint error": mp.nstr(errs[w], 3)}
# 3. the historical certificate is reproduced by this code under scripts/run_B1.py's conditions (mpmath 40 digits)
hist = json.loads((root / "data" / "B1_kappa_certificate.json").read_text())
with mp.workdps(40):
    fresh = b1_cert.build_certificate()
out["V0.4-dev.3 generator, mpmath 40 digits (as scripts/run_B1.py): semantic SHA-256"] = fresh["provenance"]["semantic_sha256"]
out["reproduces the historical certificate 616817fc..."] = (
    fresh["provenance"]["semantic_sha256"] == hist["provenance"]["semantic_sha256"]
    == "616817fcc70e0fab7f106404e5e5332b17b9c4480bd440355f1ac5257a8518c6")
out["ctx.cap after"] = ctx.cap
print(json.dumps(out))
'''


def main(argv):
    zpath = pathlib.Path(argv[0])
    zsha = hashlib.sha256(zpath.read_bytes()).hexdigest()
    if zsha != DEV3_SHA256:
        print(f"archive SHA-256 {zsha} is not the V0.4-dev.3 archive")
        return 1
    with tempfile.TemporaryDirectory() as tmp:
        with zipfile.ZipFile(zpath) as z:
            z.extractall(tmp)
        root = pathlib.Path(tmp) / "EIT_LJ_CUBE_BIFURCATIONS"
        proc = subprocess.run([sys.executable, "-c", CHILD, str(root)], capture_output=True, text=True, cwd=tmp)
    if proc.returncode != 0:
        print(proc.stderr[-3000:])
        return 1
    out = {"erratum": "E-B1", "what": "the V0.4-dev.3 B1 Taylor routines, unmodified, before the patch",
           "archive": zpath.name, "archive_sha256": zsha, "python": sys.version.split()[0],
           "result": json.loads(proc.stdout.strip().splitlines()[-1])}
    r = out["result"]
    out["defect_reproduced"] = bool(
        r["arb_series exp, prec=16, ctx.cap=10: coefficients returned"] == 10
        and r["generator b1_cert._taylor(1, 16): c_10..c_15 all exactly zero"]
        and r["checker b1_check.Model.taylor(1, 20): c_10..c_19 all exactly zero"]
        and r["generator divided differences excluding the 60-digit quotient"]
        and r["checker divided differences excluding the 60-digit quotient"])
    (ROOT / "data" / "B1_ERRATUM_pre_patch_reproduction.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))
    return 0 if out["defect_reproduced"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
