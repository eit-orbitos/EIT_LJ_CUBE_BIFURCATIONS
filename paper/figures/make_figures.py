"""Deterministic figure generation for the Paper 3 manuscript (no generative-AI artwork).

Usage (from the project root):  python paper/figures/make_figures.py
Writes paper/figures/fig1_parameter_plane.pdf, fig2_modes.pdf, fig3_bifurcation_diagrams.pdf and
paper/figures/figure_data.json (the sampled curve points). Requires matplotlib (vector PDF backend), mpmath, sympy.

Figure 1: the transition curves p = P_A(q) (0 < q < r*) and p = P_T(q) (0 < q < q_c) are evaluated at 30 significant
digits from their exact definitions (Paper 2, Lemma A and Lemma T3) with the project's own root finders; the plotted
polyline is a numerical sampling of curves whose properties are proved in Paper 2. The region shading and the index
labels illustrate Paper 2's index formula and are not a separate result.
Figure 2: first-order displacement fields from the exact formulas of NOTES.md §2, §5.9 and §6.1, with an exaggerated
amplitude; the kernel vector n is computed at q = 0.8.
Figure 3: leading-order normal forms only (axes in arbitrary units), with the conventions stated in the captions.
"""
import json
import pathlib
import sys

import matplotlib

matplotlib.use("pdf")
import matplotlib.pyplot as plt  # noqa: E402
import mpmath as mp  # noqa: E402
import numpy as np  # noqa: E402

HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "src"))
from cube_bif import a2u, t2g  # noqa: E402

mp.mp.dps = 30
matplotlib.rcParams.update({"font.size": 9, "font.family": "serif", "mathtext.fontset": "cm",
                            "pdf.fonttype": 42, "axes.linewidth": 0.7, "svg.hashsalt": "eit-lj-paper3"})
META = {"CreationDate": None, "ModDate": None, "Producer": "matplotlib (deterministic)", "Creator": "make_figures.py"}


def save(fig, name):
    fig.savefig(HERE / name, metadata=META, bbox_inches="tight")
    plt.close(fig)


# ---------------------------------------------------------------------------------------------------------------
def curves():
    rs = a2u.r_star()
    qc = mp.mpf(a2u.Q_C_FROZEN)
    qa = [rs * k / 120 for k in range(1, 120)]
    pa = [a2u.P_A(q, rs) for q in qa]
    qt = [qc * k / 120 for k in range(1, 120)]
    pt = [t2g.P_T(q) for q in qt]
    pa0 = a2u.P_A(mp.mpf("1e-12"), rs)
    pt0 = t2g.P_T(mp.mpf("1e-12"))
    return dict(r_star=rs, q_c=qc, P_A0=pa0, P_T0=pt0,
                A=[(q, p) for q, p in zip(qa, pa)], T=[(q, p) for q, p in zip(qt, pt)])


def fig1(c):
    rs, qc = float(c["r_star"]), float(c["q_c"])
    qa = [0.0] + [float(q) for q, _ in c["A"]] + [rs]
    pa = [float(c["P_A0"])] + [float(p) for _, p in c["A"]] + [rs]
    qt = [0.0] + [float(q) for q, _ in c["T"]] + [qc]
    pt = [float(c["P_T0"])] + [float(p) for _, p in c["T"]] + [qc]
    fig, ax = plt.subplots(figsize=(4.8, 3.9))
    qmax, pmax = 2.8, 5.4
    # illustrative shading of Paper 2's index formula (not a result of this paper)
    xs = np.linspace(0, qmax, 600)
    pa_i = np.interp(xs, qa, pa, right=np.nan)
    pt_i = np.interp(xs, qt, pt, right=np.nan)
    lower = np.where(xs < rs, pa_i, xs)                 # below: index 2 (only for q < r*)
    upper = np.where(xs < qc, pt_i, xs)
    ax.fill_between(xs, xs, np.where(xs < rs, lower, xs), color="#e8eef7", lw=0)
    ax.fill_between(xs, np.where(xs < rs, lower, xs), upper, where=xs < qc, color="#f6ecd9", lw=0)
    ax.fill_between(xs, np.maximum(upper, xs), pmax, color="#f3dede", lw=0)
    ax.fill_between(xs, 0, xs, color="#d9d9d9", lw=0)
    ax.plot([0, qmax], [0, qmax], color="0.35", lw=0.8)
    ax.plot(qa, pa, color="#1f4e9c", lw=1.6, label=r"$p=P_A(q)$, $0<q<r_*$ ($A_{2u}$; Theorem A)")
    ax.plot(qt, pt, color="#b2361c", lw=1.6, label=r"$p=P_T(q)$, $0<q<q_c$ ($T_{2g}$; Props. B1–B3)")
    ax.plot([rs], [rs], "o", ms=3.5, color="#1f4e9c")
    ax.plot([qc], [qc], "o", ms=3.5, color="#b2361c")
    ax.annotate(r"$(r_*,r_*)$", (rs, rs), xytext=(rs + 0.12, rs - 0.55), fontsize=8,
                arrowprops=dict(arrowstyle="-", lw=0.5))
    ax.annotate(r"$(q_c,q_c)$", (qc, qc), xytext=(qc + 0.15, qc - 0.6), fontsize=8,
                arrowprops=dict(arrowstyle="-", lw=0.5))
    ax.text(0.25, 2.25, "index 2", fontsize=8, color="0.25")
    ax.text(0.25, 3.75, "index 3", fontsize=8, color="0.25")
    ax.text(0.25, 5.05, "index 6", fontsize=8, color="0.25")
    ax.text(1.52, 1.82, "index 3", fontsize=8, color="0.25")
    ax.text(2.2, 1.0, r"$p\leq q$ (excluded)", fontsize=8, color="0.3")
    ax.set_xlim(0, qmax)
    ax.set_ylim(0, pmax)
    ax.set_xlabel(r"$q$")
    ax.set_ylabel(r"$p$")
    ax.legend(loc="upper right", fontsize=7, frameon=False)
    save(fig, "fig1_parameter_plane.pdf")


# ---------------------------------------------------------------------------------------------------------------
LABELS = [np.array(s, dtype=float) for s in __import__("itertools").product([-1, 1], repeat=3)]
EDGES = [(i, j) for i in range(8) for j in range(i + 1, 8) if np.sum(np.abs(LABELS[i] - LABELS[j])) == 2]


def config_cube():
    return [s / 2 for s in LABELS]


def config_td(eps):
    # A2u field E_A(s) = (s1 s2 s3) s: even tetrahedron (s1s2s3=+1) expands, odd one contracts (first order)
    return [s / 2 + eps * np.prod(s) * s for s in LABELS]


def config_d3d(t, nu, nv):
    J = np.ones((3, 3))
    return [s / 2 - (t * nu / 4) * (J - np.eye(3)) @ s - (t * nv * np.sqrt(2) / 4) * np.prod(s) * np.ones(3)
            for s in LABELS]


def config_d2h(t, nu, nv):
    return [s / 2 - (t * nu / 4) * np.array([0.0, s[2], s[1]]) - (t * nv * np.sqrt(2) / 4) * np.prod(s) *
            np.array([1.0, 0.0, 0.0]) for s in LABELS]


def draw(ax, pts, title, ref=None):
    view = np.array([[0.94, -0.34, 0.0], [-0.13, -0.36, 0.92]])     # fixed orthographic projection
    P = [view @ x for x in pts]
    if ref is not None:
        R = [view @ x for x in ref]
        for i, j in EDGES:
            ax.plot([R[i][0], R[j][0]], [R[i][1], R[j][1]], color="0.75", lw=0.6, ls=(0, (2, 2)))
    for i, j in EDGES:
        ax.plot([P[i][0], P[j][0]], [P[i][1], P[j][1]], color="0.15", lw=0.9)
    for k, s in enumerate(LABELS):
        even = np.prod(s) > 0
        ax.plot(P[k][0], P[k][1], "o", ms=5.5, mfc="#1f4e9c" if even else "white", mec="#1f4e9c", mew=1.0)
    ax.set_title(title, fontsize=8.5)
    ax.set_aspect("equal")
    ax.axis("off")


def fig2():
    q = mp.mpf("0.8")
    n = t2g.null_vector(t2g.P_T(q), q)
    nu, nv = -float(n[0]), -float(n[1])              # gauge n_u > 0 (B0's null_vector has the opposite sign)
    fig, axs = plt.subplots(1, 5, figsize=(7.4, 1.9), gridspec_kw=dict(width_ratios=[1, 1, 1, 1, 0.8], wspace=0.35))
    cube = config_cube()
    draw(axs[0], cube, r"cube ($O_h$)")
    draw(axs[1], config_td(0.09), r"$A_{2u}$ branch ($T_d$)", ref=cube)
    draw(axs[2], config_d3d(0.45, nu, nv), r"$T_{2g}$, $D_{3d}$ axis", ref=cube)
    draw(axs[3], config_d2h(0.5, nu, nv), r"$T_{2g}$, $D_{2h}$ axis", ref=cube)
    # cross-section x = const of the D2h first-order field: the square becomes a rhombus
    ax = axs[4]
    sq = np.array([[0.5, 0.5], [-0.5, 0.5], [-0.5, -0.5], [0.5, -0.5], [0.5, 0.5]])
    eps = 0.5 * nu / 2
    rh = np.array([[y - eps * z, z - eps * y] for y, z in sq])
    ax.plot(sq[:, 0], sq[:, 1], color="0.7", lw=0.7, ls=(0, (2, 2)))
    ax.plot(rh[:, 0], rh[:, 1], color="0.15", lw=0.9)
    ax.plot([-0.75, 0.75], [-0.75, 0.75], color="#b2361c", lw=0.5, ls=":")
    ax.plot([-0.75, 0.75], [0.75, -0.75], color="#b2361c", lw=0.5, ls=":")
    ax.set_title(r"$D_{2h}$ section $x=c$", fontsize=8.5)
    ax.set_xlabel(r"$y$", fontsize=8)
    ax.set_ylabel(r"$z$", fontsize=8)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    save(fig, "fig2_modes.pdf")
    return dict(q=str(q), n_u=nu, n_v=nv, td_eps=0.09, d3d_t=0.45, d2h_t=0.5, rhombus_eps=eps)


# ---------------------------------------------------------------------------------------------------------------
def fig3():
    mu = np.linspace(-1, 1, 401)
    mp_ = mu[mu > 0]
    fig, axs = plt.subplots(1, 3, figsize=(7.2, 2.3), sharey=False)
    kw_min = dict(color="#1f4e9c", lw=1.4)
    kw_max = dict(color="#b2361c", lw=1.2, ls=(0, (4, 2)))
    # (a) A2u pitchfork: a^2 = C mu, C > 0 (Theorem A); cube curvature lambda = lambda'(0) mu, lambda'(0) < 0
    ax = axs[0]
    ax.plot(mu[mu <= 0], 0 * mu[mu <= 0], **kw_min)
    ax.plot(mp_, 0 * mp_, **kw_max)
    ax.plot(mp_, np.sqrt(mp_), **kw_min)
    ax.plot(mp_, -np.sqrt(mp_), **kw_min)
    ax.set_title(r"(a) $A_{2u}$: $Z_2$ pitchfork ($T_d$)", fontsize=8.5)
    ax.set_xlabel(r"$\mu=p-P_A(q)$")
    ax.set_ylabel(r"$a$")
    # (b) D3d transcritical: s* = -(tau/kappa) mu > 0 for mu > 0 (gauge n_u > 0, kappa > 0, tau < 0)
    ax = axs[1]
    ax.plot(mu[mu <= 0], 0 * mu[mu <= 0], **kw_min)
    ax.plot(mp_, 0 * mp_, **kw_max)
    ax.plot(mu[mu <= 0], 0.8 * mu[mu <= 0], **kw_max)
    ax.plot(mp_, 0.8 * mp_, **kw_min)
    ax.set_title(r"(b) $T_{2g}$, $D_{3d}$ axis: transcritical", fontsize=8.5)
    ax.set_xlabel(r"$\mu=p-P_T(q)$")
    ax.set_ylabel(r"$s$ (gauge $n_u>0$)")
    # (c) D2h pitchfork: s^2 = -(6 tau / c4) mu (Proposition B2)
    ax = axs[2]
    ax.plot(mu[mu <= 0], 0 * mu[mu <= 0], **kw_min)
    ax.plot(mp_, 0 * mp_, **kw_max)
    ax.plot(mp_, np.sqrt(mp_), **kw_min)
    ax.plot(mp_, -np.sqrt(mp_), **kw_min)
    ax.set_title(r"(c) $T_{2g}$, $D_{2h}$ axis: $Z_2$ pitchfork", fontsize=8.5)
    ax.set_xlabel(r"$\mu=p-P_T(q)$")
    ax.set_ylabel(r"$s$")
    for ax in axs:
        ax.axhline(0, color="0.8", lw=0.4, zorder=0)
        ax.axvline(0, color="0.8", lw=0.4, zorder=0)
        ax.set_xticks([0])
        ax.set_yticks([0])
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1.15, 1.15)
    axs[0].plot([], [], label="minimum along the branch axis", **kw_min)
    axs[0].plot([], [], label="maximum along the branch axis", **kw_max)
    fig.legend(loc="lower center", ncol=2, fontsize=7.5, frameon=False, bbox_to_anchor=(0.5, -0.1))
    fig.tight_layout()
    save(fig, "fig3_bifurcation_diagrams.pdf")


def main():
    c = curves()
    fig1(c)
    modes = fig2()
    fig3()
    data = {"note": "sampled numerically at 30 digits from the exact curve definitions; illustration only",
            "r_star": mp.nstr(c["r_star"], 20), "q_c": mp.nstr(c["q_c"], 20), "P_A(0+)": mp.nstr(c["P_A0"], 20),
            "P_T(0+)": mp.nstr(c["P_T0"], 20),
            "A2u_curve": [[mp.nstr(q, 12), mp.nstr(p, 12)] for q, p in c["A"]],
            "T2g_curve": [[mp.nstr(q, 12), mp.nstr(p, 12)] for q, p in c["T"]], "fig2": modes}
    (HERE / "figure_data.json").write_text(json.dumps(data, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print("figures written:", sorted(p.name for p in HERE.glob("fig*.pdf")))


if __name__ == "__main__":
    main()
