"""Phase B0 — T2g reconnaissance (no branch theory). Writes data/B0_t2g.json."""
import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import mpmath as mp  # noqa: E402
import sympy as sp  # noqa: E402

from cube_bif import STATUS, __version__, paper2_ref, t2g  # noqa: E402
from cube_bif import numeric as nm  # noqa: E402
from cube_bif import pairsum as ps  # noqa: E402
from cube_bif.group import D24, element_type, oh_matrices, projector, sigma  # noqa: E402

mp.mp.dps = 40


def conj_key(S):
    """Canonical key of the O_h-conjugacy class of the subgroup S."""
    G = oh_matrices()
    return min(tuple(sorted(tuple(g * R * g.T) for R in S)) for g in G)


def main():
    G = oh_matrices()
    PT = projector("T2g")
    basis6 = t2g.UH + t2g.VH
    Bm = sp.Matrix.hstack(*basis6)
    H = ps.hessian()
    Ks = t2g.block_K(H)
    al = {k: 2 * ps.PSI[(1, k)] + 4 * k * ps.PSI[(2, k)] for k in (1, 2, 3)}
    be = {k: 2 * ps.PSI[(1, k)] for k in (1, 2, 3)}
    a1, a2, a3, b1, b2, b3 = al[1], al[2], al[3], be[1], be[2], be[3]
    K_paper2 = sp.Matrix([[2 * b1 + 2 * a2 + 2 * b2 + sp.Rational(4, 3) * a3 + sp.Rational(2, 3) * b3,
                           2 * sp.sqrt(2) / 3 * (a3 - b3)],
                          [2 * sp.sqrt(2) / 3 * (a3 - b3),
                           2 * a1 + 4 * b1 + sp.Rational(2, 3) * a3 + sp.Rational(4, 3) * b3]])
    Kpq = Ks[2].subs(ps.two_term())
    Mfac = ps.q_ * ps.W("q") * (t2g.M_paper2(ps.p_, ps.X["p"], ps.Y["p"]) - t2g.M_paper2(ps.q_, ps.X["q"], ps.Y["q"]))
    cb = t2g.critical_basis()
    mats = [t2g.T3(R) for R in G]
    checks = {
        "6 basis vectors lie in the T2g isotypic component": all(PT * v == v for v in basis6),
        "basis orthonormal": sp.simplify(Bm.T * Bm) == sp.eye(6),
        "copy 1 (U) transforms by sigma(R) R for all 48": all(t2g.rep_matrix_in(t2g.VH, R) == sigma(R) * R for R in G),
        "copy 2 (W) transforms by sigma(R) R for all 48": all(t2g.rep_matrix_in(t2g.UH, R) == sigma(R) * R for R in G),
        "critical basis n_u uh_k + n_v vh_k (symbolic n) transforms by sigma(R) R": all(
            sp.simplify(D24(R) * cb[k] - sum((t2g.T3(R)[j, k] * cb[j] for j in range(3)), sp.zeros(24, 1)))
            == sp.zeros(24, 1) for R in G for k in range(3)),
        "Hessian 2x2 block identical for k = 1, 2, 3": all(sp.simplify(Ks[0] - K) == sp.zeros(2) for K in Ks),
        "no Hessian coupling between different k": all(
            sp.expand((x.T * H * y)[0, 0]) == 0 for j in range(3) for k in range(3) if j != k
            for x in (t2g.UH[j], t2g.VH[j]) for y in (t2g.UH[k], t2g.VH[k])),
        "block equals Paper 2 Lemma T0 (alpha, beta form)": sp.simplify(Ks[2] - K_paper2) == sp.zeros(2),
        "unit edge, equilibrium: K(p,q) = q W_q [M(p) - M(q)] (Paper 2's M)": sp.simplify(Kpq - Mfac) == sp.zeros(2),
        "I3 = a1 a2 a3 invariant under all 48 matrices": all(
            sp.expand(t2g.I3.subs(dict(zip(t2g.A, list(T * sp.Matrix(t2g.A)))), simultaneous=True) - t2g.I3) == 0
            for T in mats),
        "kernel of the 3x3 representation = {E, i}": sorted(element_type(R) for R in G if t2g.T3(R) == sp.eye(3))
        == ["E", "i"],
    }
    inv_dims = {d: t2g.invariant_dimension(d, mats) for d in (1, 2, 3, 4)}
    checks["invariant dimensions deg 1..4 = 0, 1, 1, 2"] = inv_dims == {1: 0, 2: 1, 3: 1, 4: 2}
    # isotropy, grouped into O_h conjugacy classes
    rows = t2g.isotropy_table()
    classes = {}
    for row in rows:
        S = t2g.stabilizer(row["representative"])
        classes.setdefault(conj_key(S), []).append(row)
    iso = []
    for key, members in classes.items():
        r0 = dict(members[0])
        r0["conjugates_in_class"] = len(members)
        r0["representatives"] = [m["representative"] for m in members]
        r0["axial"] = r0["fix_dim"] == 1
        iso.append(r0)
    iso.sort(key=lambda w: (-w["order"], w["label"]))
    # 24-D stabilisers of representative critical vectors (symbolic n_u, n_v) equal the 3x3 stabilisers
    n_u, n_v = sp.symbols("n_u n_v", positive=True)
    cbp = t2g.critical_basis(n_u, n_v)
    st24 = {}
    for v in [(1, 0, 0), (1, 1, 1), (1, 1, 0), (2, 1, 0)]:
        w = sum((v[k] * cbp[k] for k in range(3)), sp.zeros(24, 1))
        S24 = {tuple(R) for R in G if sp.simplify(D24(R) * w - w) == sp.zeros(24, 1)}
        S3 = {tuple(R) for R in t2g.stabilizer(v)}
        st24[str(v)] = S24 == S3
    checks["24-D stabiliser of sum a_k e_k = 3x3 stabiliser of a (4 representatives)"] = all(st24.values())
    # curve samples on p = P_T(q)
    cit = paper2_ref.load_analysis("cube_index_theorem")
    samples = []
    for qq in ("0.25", "0.5", "1.0", "1.5", "1.9", "2.0"):
        pt = t2g.P_T(qq)
        n = t2g.null_vector(pt, mp.mpf(qq))
        V = nm.PairEnergy(pt, mp.mpf(qq))
        Hn = V.hessian(nm.y_star())
        worst = 0
        for k in range(3):
            e = [n[0] * mp.mpf(sp.N(t2g.UH[k][i], 50)) + n[1] * mp.mpf(sp.N(t2g.VH[k][i], 50)) for i in range(24)]
            He = [mp.fsum(Hn[i, j] * e[j] for j in range(24)) for i in range(24)]
            worst = max(worst, mp.sqrt(mp.fsum(c * c for c in He)))
        rec = {"q": qq, "P_T(q)": mp.nstr(pt, 25), "n_u": mp.nstr(n[0], 20), "n_v": mp.nstr(n[1], 20),
               "max_k |H e_k|": mp.nstr(worst, 3)}
        if cit is not None:
            rec["P_T (Paper 2 float code)"] = repr(cit.P_T(float(qq)))
        samples.append(rec)
    out = {
        "project": "EIT-LJ Cube Bifurcations (Paper 3)", "version": __version__, "status": STATUS,
        "basis": "uh_k = -W_k/4, vh_k = -(sqrt2/4) U_k; W_k(s) = S_k s, U_k(s) = (s1 s2 s3) eps_k "
                 "(k = 3: Paper 2 Lemma T0's u, v); critical basis e_k = n_u uh_k + n_v vh_k, n in ker[M(p)-M(q)]",
        "representation": "T(R) = sigma(R) R on span{e_1, e_2, e_3}, sigma(R) = product of the nonzero entries",
        "checks": checks, "invariant_dimensions": inv_dims,
        "isotropy_classes": iso, "stabilizer_24D_equals_3x3": st24, "curve_samples": samples,
        "matrices_3x3": [{"element": [[int(R[i, j]) for j in range(3)] for i in range(3)], "type": element_type(R),
                          "T(R)": [[int(t2g.T3(R)[i, j]) for j in range(3)] for i in range(3)]} for R in G],
        "ihrig_statement": (
            "Ihrig & Golubitsky (Physica D 13 (1984) 1-33, Thm 4.2(B)): for steady-state bifurcation on an absolutely "
            "irreducible representation with nonzero quadratic equivariants, the branches given by the Equivariant "
            "Branching Lemma (axial; hypothesis H4) are generically unstable near the bifurcation point; Chossat, "
            "Lauterbach & Melbourne removed the axial restriction (as summarised by Arjevani & Field, arXiv:2107.02422). "
            "It is a stability statement. It does not say that every branch is transcritical; that is decided per "
            "axis by the restriction of the quadratic equivariant (here the gradient of I3) to Fix(Sigma)."),
    }
    out["all_checks_pass"] = all(checks.values())
    (ROOT / "data" / "B0_t2g.json").write_text(json.dumps(out, indent=1, default=str))
    for k, v in checks.items():
        print(f"{'PASS' if v else 'FAIL'}  {k}")
    for r0 in iso:
        print({k: r0[k] for k in r0 if k in ("label", "order", "fix_dim", "conjugates_in_class", "representative",
                                             "normalizer_label", "normalizer_action_on_Fix", "I3_on_axis",
                                             "branch_type")})
    for smp in samples:
        print(smp)
    return out


if __name__ == "__main__":
    main()
