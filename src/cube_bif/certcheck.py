"""Independent checker for the Lemma M certificate (data/A2_lemma_M_certificate.json).

It shares no derivation or evaluation code with lemma_m.py:
- m', m'' are re-derived from the V0.1-dev m (a2u.scale_free_coefficients()["m"]) by a different route: x and y are
  replaced by undefined functions X(r), Y(r) with X' = -(L2/2) X, Y' = -(L3/2) Y. The certificate's expressions must
  agree with them exactly.
- Evaluation uses its own Arb tree-walker over the parsed expressions, at its own precision (CHECK_PREC bits).
- Every box is re-verified (mean-value form; if needed the box is split further, but the claim checked is still
  m' > recorded lower bound on the whole box). Coverage of [0, 16/5] must be gap-free with exact rational endpoints.
The certificate is a project artifact; its expression strings are parsed by SymPy with an explicit symbol table.
"""
import hashlib
import json
from fractions import Fraction

import sympy as sp
from flint import arb, ctx, fmpq

from . import a2u

CHECK_PREC = 160
r, x, y = a2u.r, a2u.x, a2u.y
L2, L3 = sp.symbols("L2 L3", positive=True)
SYMS = {"r": r, "x": x, "y": y, "L2": L2, "L3": L3}
EXPECTED_CLAIM = {"quantity": "m'(r)", "relation": ">", "value": "0", "interval": ["0", "16/5"]}
NEAR_ZERO_M1 = sp.Rational(18, 49) + sp.Rational(12, 49) * L2 + sp.Rational(57, 784) * L3


def q_of(s):
    F = Fraction(s)
    return fmpq(F.numerator, F.denominator)


def derive(e):
    X, Y = sp.Function("X")(r), sp.Function("Y")(r)
    d = sp.diff(e.subs({x: X, y: Y}, simultaneous=True), r)
    d = d.subs({sp.Derivative(X, r): -L2 / 2 * X, sp.Derivative(Y, r): -L3 / 2 * Y})
    return d.subs({X: x, Y: y}, simultaneous=True)


def same(e1, e2):
    return sp.expand(sp.numer(sp.together(e1 - e2))) == 0


def compile_tree(e):
    """Closure evaluating the SymPy tree e in Arb, given env {name: arb}."""
    if e.is_Symbol:
        name = e.name
        return lambda env: env[name]
    if e.is_Integer:
        v = int(e)
        return lambda env: arb(v)
    if e.is_Rational:
        v = fmpq(int(e.p), int(e.q))
        return lambda env: arb(v)
    if e.is_Add:
        fs = [compile_tree(a) for a in e.args]

        def add(env):
            t = arb(0)
            for f in fs:
                t = t + f(env)
            return t
        return add
    if e.is_Mul:
        fs = [compile_tree(a) for a in e.args]

        def mul(env):
            t = arb(1)
            for f in fs:
                t = t * f(env)
            return t
        return mul
    if e.is_Pow and e.exp.is_Integer:
        fb, k = compile_tree(e.base), int(e.exp)
        if k >= 0:
            return lambda env: fb(env) ** k
        return lambda env: 1 / (fb(env) ** (-k))
    raise ValueError(f"unsupported node {e.func}")


class Model:
    def __init__(self, Psi, Phi, Sx, prec=CHECK_PREC):
        ctx.prec = prec
        self.fm1 = compile_tree(Psi / (16 * Sx ** 3))
        self.fm2 = compile_tree(Phi / (16 * Sx ** 4))
        self.l2, self.l3 = arb(2).log(), arb(3).log()

    def env(self, rb):
        return {"r": rb, "x": (-rb * self.l2 / 2).exp(), "y": (-rb * self.l3 / 2).exp(), "L2": self.l2, "L3": self.l3}

    def m1(self, rb):
        return self.fm1(self.env(rb))

    def m2(self, rb):
        return self.fm2(self.env(rb))

    def box_exceeds(self, lo, hi, lb, depth=0, max_depth=4):
        rb = arb(lo).union(arb(hi))
        c = (lo + hi) / 2
        rc = arb(c)
        E = self.m1(rc) + (rb - rc) * self.m2(rb)
        if E > arb(lb):
            return True, depth
        if depth >= max_depth:
            return False, depth
        mid = (lo + hi) / 2
        ok1, d1 = self.box_exceeds(lo, mid, lb, depth + 1, max_depth)
        if not ok1:
            return False, d1
        ok2, d2 = self.box_exceeds(mid, hi, lb, depth + 1, max_depth)
        return ok2, max(d1, d2)


def semantic_hash(cert):
    body = {k: v for k, v in cert.items() if k != "provenance"}
    return hashlib.sha256(json.dumps(body, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()).hexdigest()


def check(cert, stored_semantic_hash=None):
    """Return (ok, report). ok is True only if every check passes."""
    fail = []
    rep = {}
    # 1. claim and interval
    if cert.get("claim") != EXPECTED_CLAIM:
        fail.append(f"claim differs from {EXPECTED_CLAIM}")
    # 2. expressions: hashes, canonical m, re-derived m', m''
    ex = cert["expressions"]
    for k, v in ex.items():
        if cert.get("expression_sha256", {}).get(k) != hashlib.sha256(v.encode()).hexdigest():
            fail.append(f"expression hash mismatch: {k}")
    try:
        P = {k: sp.parse_expr(ex[k], local_dict=dict(SYMS)) for k in ("m", "S", "Psi", "Phi")}
    except Exception as e:  # noqa: BLE001
        return False, {"failures": [f"unparsable expression: {e}"]}
    m_can = a2u.scale_free_coefficients()["m"]
    m1_can, = (derive(m_can),)
    m2_can = derive(m1_can)
    if ex.get("m'") != "Psi/(16*S**3)" or ex.get("m''") != "Phi/(16*S**4)":
        fail.append("m', m'' are not stated as Psi/(16 S^3), Phi/(16 S^4)")
    if not same(P["m"], m_can):
        fail.append("m differs from the V0.1-dev closed form")
    if not same(P["S"], 3 * x + y + 3):
        fail.append("S differs from 3x + y + 3")
    if not same(P["Psi"] / (16 * P["S"] ** 3), m1_can):
        fail.append("m' = Psi/(16 S^3) differs from the re-derived m'")
    if not same(P["Phi"] / (16 * P["S"] ** 4), m2_can):
        fail.append("m'' = Phi/(16 S^4) differs from the re-derived m''")
    # 3. coverage
    boxes = cert["boxes"]
    try:
        los = [q_of(b["lo"]) for b in boxes]
        his = [q_of(b["hi"]) for b in boxes]
        lbs = [q_of(b["lower_bound"]) for b in boxes]
    except (ValueError, ZeroDivisionError) as e:
        return False, {"failures": fail + [f"non-rational endpoint or bound: {e}"]}
    if not boxes or los[0] != fmpq(0) or his[-1] != fmpq(16, 5):
        fail.append("boxes do not start at 0 and end at 16/5")
    if any(not (a < b) for a, b in zip(los, his)):
        fail.append("a box has lo >= hi")
    if any(his[i] != los[i + 1] for i in range(len(boxes) - 1)):
        fail.append("coverage has a gap or an overlap")
    if cert.get("n_boxes") != len(boxes):
        fail.append("n_boxes does not match")
    # 4. lower bounds
    if any(not (lb > 0) for lb in lbs):
        fail.append("a recorded lower bound is not strictly positive")
    if lbs and q_of(cert["min_lower_bound"]) != min(lbs):
        fail.append("min_lower_bound is not the minimum of the box bounds")
    # 5. re-verify every box with the independent evaluator
    model = Model(P["Psi"], P["Phi"], P["S"])
    bad, refined = [], 0
    for i, (a, b, lb) in enumerate(zip(los, his, lbs)):
        ok, depth = model.box_exceeds(a, b, lb)
        refined += depth > 0
        if not ok:
            bad.append(i)
    if bad:
        fail.append(f"lower bound not confirmed on boxes {bad[:10]}")
    rep["boxes_checked"] = len(boxes)
    rep["boxes_needing_refinement"] = refined
    # 6. near r = 0
    nz = cert["near_zero"]
    m1_0 = sp.expand(m1_can.subs({r: 0, x: 1, y: 1}))
    if not same(sp.parse_expr(nz["m'(0) exact"], local_dict=dict(SYMS)), m1_0) or not same(m1_0, NEAR_ZERO_M1):
        fail.append("m'(0) exact value differs")
    if any(c <= 0 for c in sp.Poly(m1_0, L2, L3).coeffs()):
        fail.append("m'(0) has a non-positive coefficient")
    sub = nz["m''_positive_on_subboxes"]
    if q_of(sub[0]["lo"]) != 0 or q_of(sub[-1]["hi"]) != q_of(nz["initial_interval"][1]) or any(
            q_of(sub[i]["hi"]) != q_of(sub[i + 1]["lo"]) for i in range(len(sub) - 1)):
        fail.append("near-zero sub-boxes do not tile the initial interval")
    for s in sub:
        if not (model.m2(arb(q_of(s["lo"])).union(arb(q_of(s["hi"])))) > 0):
            fail.append(f"m'' > 0 not confirmed on [{s['lo']}, {s['hi']}]")
    # 7. P_A(q) < 16/5
    hA = a2u.H_A_FROZEN
    fh, fdh = compile_tree(sp.together(hA)), compile_tree(sp.together(derive(hA)))
    e16 = model.env(arb(fmpq(16, 5)))
    if not (fh(e16) + arb(fmpq(6, 7)) < 0):
        fail.append("h_A(16/5) < -6/7 not confirmed")
    if not (fdh(e16) < 0):
        fail.append("h_A'(16/5) < 0 not confirmed")
    a, b = (q_of(s) for s in cert["P_A_bound"]["P_A(0+) enclosure"])
    ea, eb = model.env(arb(a)), model.env(arb(b))
    if not (fh(ea) + arb(fmpq(6, 7)) > 0 and fh(eb) + arb(fmpq(6, 7)) < 0 and fdh(ea) < 0):
        fail.append("P_A(0+) enclosure not confirmed")
    # 8. semantic hash
    h = semantic_hash(cert)
    rep["semantic_sha256"] = h
    if cert.get("provenance", {}).get("semantic_sha256") != h:
        fail.append("semantic hash in provenance does not match the content")
    if stored_semantic_hash is not None and stored_semantic_hash != h:
        fail.append("semantic hash differs from the recorded hash file")
    rep["failures"] = fail
    return not fail, rep
