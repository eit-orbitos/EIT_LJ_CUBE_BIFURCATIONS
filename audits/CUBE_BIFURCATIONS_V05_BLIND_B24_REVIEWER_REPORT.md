# Blind independent audit of Paper 3 V0.4-dev.5 — Track B / Phase B2.4 only

**Audit date:** 2026-11-15  
**Auditor:** Kimi Agent  
**Formal verdict:** **PASS**  
**Findings requiring correction:** none

## 1. Scope and audit position

This is a fresh blind independent audit of Phase B2.4 and Proposition B2 in `EIT_LJ_CUBE_BIFURCATIONS_V0.4-dev.5.zip`. The supplied completion report was treated as untrusted. The audit independently checked the proof derivation, the exact symmetry and geometry claims, the dependency boundary, clean reproduction, numerical corroboration, and adversarial controls.

The permitted proof inputs were the six inputs specified by the phase:

1. exact B2.0 parity and fixed-space results;
2. the exact B2.1 Lyapunov–Schmidt quartic identity;
3. certified Lemma Q from B2.3;
4. audited B1.8 transversality, \(\tau<0\);
5. standard Lyapunov–Schmidt reduction;
6. the analytic implicit function theorem.

Lemma Q was checked as a dependency and preserved artifact, but its B2.3 certificate was not independently re-audited here. B2.5 was not started. No full-space stability or three-dimensional centre-manifold index was inferred. Ihrig's theorem was not used.

Paper 2 was read-only. No uploaded archive or project source tree was modified. Nothing was frozen, published, pushed, released, or uploaded.

## 2. Authenticated inputs

| input | SHA-256 |
|---|---|
| `EIT_LJ_CUBE_BIFURCATIONS_V0.4-dev.5.zip` | `77267d56f7a271b81b6cc91166f6750c71e1fc4f214c337f016ecf75b4563949` |
| duplicate `EIT_LJ_CUBE_BIFURCATIONS_V0.4-dev.5(1).zip` | identical to the preceding archive |
| `EIT_LJ_CUBE_BIFURCATIONS_V0.4-dev.4.zip` | `8ae923beec9c095ec546c1a69e56a632698bfd8e4828a1165a8cbc1199cc06c7` |
| `EIT_LJ_FULL_VECTOR_STABILITY_V1.0(1).zip` | `bb70721df7f0aa17edca30d84d1b4aaf980c0a76693be14fa780e4ab8f64762d` |

The two dev.5 uploads are byte-identical. Internal manifest verification gave **113/113 passed** for dev.5 and **101/101 passed** for dev.4.

## 3. Identity boundary from V0.4-dev.4

The dev.5 identity checker passed against the authenticated dev.4 archive. Its independent result was:

- 94 byte-identical files;
- six permitted changed files;
- one append-only file;
- 11 permitted additions listed by the checker, plus the identity report itself;
- one regenerated integrity manifest;
- no deleted or unexpected files.

An independent comparison additionally confirmed:

- NOTES §§1–10 are byte-identical, with extracted-text SHA-256  
  `8803df9665fc5fb457459e56d47230ccd28c79ed112cb1900e77d7695265708d`;
- the historical B1 certificate is unchanged, SHA-256  
  `dee3ad024af69f76620de35f3d0aa8be06a9f4f099ca0ffb001c4914178f87ab`;
- the B2.3 certificate is unchanged, SHA-256  
  `9f6b31404ce9e03372b321567f53cb95254e2955c332e7eea7c381ca0f4d4209`;
- the B2.3 check report is unchanged, SHA-256  
  `34ba30d3879393e6bb9c727c17629ee67bec79379276edbc3030f427d63a23b9`;
- the included targeted B1 erratum re-audit is byte-identical to the delivered report, SHA-256  
  `ba482da06aa0492b6524e47680fd949170f4d0dafac0d5661a073efce4d46b74`;
- Track A, B0, B1, B2.0, B2.1, B2.2, B2.3, Paper 2 inputs, earlier scripts, records, and included audit reports remain inside the enforced identity boundary.

**Conclusion:** the identity chain is valid. No earlier mathematical or certified artifact was altered by B2.4.

## 4. Independent reconstruction of the exact proof

The independent exact calculation used no project imports. It reconstructed the 48 signed permutation matrices, their 24-dimensional action, and the displacement fields directly from the eight cube labels. A separate generic symbolic calculation performed the transverse stationary solve order by order. The scalar implicit-function calculation was also independently redone.

### 4.1 Fixed space, parity, and transverse invertibility

For

\[
e_1=n_u\,\widehat u_1+n_v\,\widehat v_1,\qquad
f_1=-n_v\,\widehat u_1+n_u\,\widehat v_1,
\]

the independent exact reconstruction found:

- \(|\Sigma|=8\) for \(\Sigma=\operatorname{Stab}(e_1)\);
- \(\operatorname{rank}P_{\operatorname{Fix}(\Sigma)}=4\);
- the orthonormal fixed basis
  \[
  \{\widehat A,\widehat E,\widehat u_1,\widehat v_1\}
  =\{\widehat A,\widehat E,e_1,f_1\};
  \]
- the normaliser has order 16;
- exactly eight elements reverse \(e_1\), and they are precisely \(N(\Sigma)\setminus\Sigma\);
- every reversing element acts on the fixed basis as
  \[
  \operatorname{diag}(1,1,-1,-1),
  \]
  hence on coordinates as \((s,w_A,w_E,w_f)\mapsto(-s,w_A,w_E,-w_f)\).

The B2.1 block form gives

\[
H|_{\operatorname{Fix}(\Sigma)}=\operatorname{diag}(h_A,h_E)\oplus K.
\]

At the critical curve point, the transverse Hessian has entries \(h_A>0\), \(h_E>0\), and \(f^TKf=\operatorname{tr}K>0\). Thus the Lyapunov–Schmidt transverse solve is locally unique and analytic. Symmetric criticality is applicable because the action is finite and orthogonal and the cube remains an equilibrium for every \(p\).

Uniqueness of the transverse solution under the reversing action implies

\[
w(-s,\mu)=D(g)w(s,\mu),\qquad V_{\rm red}(-s,\mu)=V_{\rm red}(s,\mu).
\]

The reduced potential is therefore even in \(s\).

### 4.2 Generic Lyapunov–Schmidt expansion

For a generic polynomial energy in \((s,w_A,w_E,w_f)\), invariant under the stated \(\mathbb Z_2\) action and with independent coefficients for every permitted cubic and quartic monomial, the independent calculation obtained

\[
w_1=-\frac{k_{sf}}{k_{ff}}f_1,
\]

with no \(A_{1g}\) or \(E_g\) component at first order. At criticality \(k_{ss}=k_{sf}=0\), so \(w_1=0\). The reduced quadratic coefficient is exactly

\[
\frac12\left(k_{ss}-\frac{k_{sf}^2}{k_{ff}}\right).
\]

All reduced coefficients of orders \(s\), \(s^3\), and \(s^5\) vanish. At criticality the quartic coefficient agrees with a separately computed directional-derivative formula:

\[
\frac1{24}\left(D^4V[e_1,e_1,e_1,e_1]
-3b^TH_{WW}^{-1}b\right),
\qquad b=D^3V[e_1,e_1,\cdot]|_W.
\]

The second-order correction at criticality lies only in \(\operatorname{span}\{\widehat A,\widehat E\}\), with coefficient

\[
-\frac12H_{A E}^{-1}(b_A,b_E)^T,
\]

and has no \(f_1\) component. Away from criticality the first-order \(f_1\) term is \(O(\mu)\); on the branch, where \(\mu=O(s^2)\), its contribution is \(O(s^3)\).

### 4.3 Schur complement and transversality

The independent symbolic calculation verified, for orthonormal \(n,f\),

\[
\lambda=n^TKn-\frac{(n^TKf)^2}{f^TKf}
=\frac{\det K}{f^TKf}.
\]

For a generic \(K(\mu)\) with \(K(0)n=0\) and nonsingular transverse direction,

\[
\lambda(0)=0,\qquad \lambda'(0)=n^TK'(0)n=\tau.
\]

Audited B1.8 supplies \(\tau<0\). Lemma Q and its corollary supply \(c_4>0\) for each fixed \(0<q<q_c\). Consequently,

\[
V_{\rm red}=V_0(\mu)+\frac{\lambda(\mu)}2s^2
+\frac{c_4}{24}s^4+O(s^6,\mu s^4,\mu^2s^2).
\]

Differentiation independently gives

\[
\partial_sV_{\rm red}=sG(s^2,\mu),\qquad
G(z,\mu)=\lambda(\mu)+\frac{c_4}{6}z+O(z^2,\mu z,\mu^2).
\]

The factor \(1/24\) in the potential and the factor \(1/6\) in \(G\) are correct.

### 4.4 Implicit-function branch and its side

A separate generic series calculation, including arbitrary second- and third-order coefficients of \(G\), reproduced

\[
G(0,0)=0,\qquad G_\mu(0,0)=\tau,\qquad G_z(0,0)=\frac{c_4}{6},
\]

and

\[
\mu_*(z)=-\frac{c_4}{6\tau}z+O(z^2),
\qquad
z=Z(\mu)=-\frac{6\tau}{c_4}\mu+O(\mu^2).
\]

Since \(\tau<0\) and \(c_4>0\),

\[
\mu_*'(0)=-\frac{c_4}{6\tau}>0.
\]

For every sufficiently small \(s\ne0\), an equilibrium requires \(\mu=\mu_*(s^2)>0\). Thus no nontrivial local equilibrium exists for \(\mu\le0\). For sufficiently small \(\mu>0\), monotonicity of \(\mu_*\) gives exactly one positive \(z\), hence exactly two equilibria \(s=\pm s_*(\mu)\), with

\[
s_*(\mu)^2=-\frac{6\tau}{c_4}\mu+O(\mu^2).
\]

The independent sign table also confirmed that reversing either the sign of \(\tau\) or the sign of \(c_4\) reverses the branch side. The branch is not transcritical and does not exist on both sides.

### 4.5 Pitchfork type and axial curvature

The eight reversing elements exchange the two nontrivial solutions, so the local pair is \(\mathbb Z_2\)-symmetric. In the stated energy-reduced axial convention, the branch is supercritical: it exists where the cube's axial reduced curvature is negative, and the nontrivial pair has positive axial reduced curvature.

Independently differentiating the reduced equation gives

\[
\partial_s^2V_{\rm red}=G(z,\mu)+2zG_z(z,\mu).
\]

Therefore

\[
\partial_s^2V_{\rm red}\big|_{s=0}=\tau\mu+O(\mu^2),
\]

whereas on \(G=0\),

\[
\partial_s^2V_{\rm red}\big|_{s=\pm s_*}
=2Z(\mu)G_z(Z(\mu),\mu)
=-2\tau\mu+O(\mu^2).
\]

On the branch side \(\mu>0\), the first expression is negative and the second positive. The independent generic calculation also verified that \(G(Z(\mu),\mu)\) vanishes through order \(\mu^2\).

These are strictly one-direction axial statements. They do not determine full-space stability or the centre-manifold Morse index.

### 4.6 Exact isotropy, non-cuboid status, and geometry

The independent 24-dimensional group reconstruction found

\[
\operatorname{rank}\big((D(R)-I)[\widehat u_1,\widehat v_1]\big)
=\begin{cases}
0,&R\in\Sigma,\\
2,&R\notin\Sigma.
\end{cases}
\]

The independently reconstructed six-dimensional \(T_{2g}\) space has an orthonormal basis, is invariant under all 48 group elements, contains \(\widehat u_1,\widehat v_1\), and is orthogonal to \(\widehat A,\widehat E\). Projecting any fixed branch displacement onto this invariant space therefore rules out every element outside \(\Sigma\). Since the branch's axial component is nonzero for small \(\mu>0\), its isotropy is exactly \(\Sigma\cong D_{2h}\), not \(D_{4h}\) or \(O_h\).

There are eight diagonal sign matrices, but only four belong to \(\Sigma\). The axial \(T_{2g}\) component is not fixed by the full diagonal sign group. Hence the nontrivial branch points are not in Paper 2's cuboid fixed space.

The first-order vertex formula was independently reconstructed:

\[
s e_1:\quad
\delta x_s=-\frac{sn_u}{4}(0,s_3,s_2)
-\frac{sn_v\sqrt2}{4}(s_1s_2s_3)(1,0,0).
\]

The first term acts on every square section \(x=\mathrm{const}\) by

\[
(y,z)\mapsto(y-\epsilon z,z-\epsilon y),
\qquad \epsilon=sn_u/2.
\]

An independent exact calculation confirmed four equal sides, perpendicular diagonals, diagonal length factors \(|1-\epsilon|\) and \(|1+\epsilon|\), and adjacent-side inner product \(-2\epsilon\). Thus the sections are rhombic/sheared at first order and are not rectangles for nonzero first-order displacement. The second term translates the two tetrahedra oppositely along \(x\) with weight \(n_v\). The notes correctly do not claim a certified global nonzero lower bound for \(n_v\).

## 5. Dependency graph and claim boundary

Independent traversal of the generated dependency graph confirmed:

- all six permitted inputs are reachable;
- every other reachable proof node is a `VERIFIED-EXACT` derivation step;
- no numerical or corroboration-only node is reachable from the proposition;
- the graph is acyclic;
- the proposition does not claim full-space stability, a centre-manifold index, or cuboid geometry.

Independent graph corruptions adding the B2.2 scan or B2.4 numerical branch points as proof dependencies were rejected. Removing transversality was also rejected.

The documented claim boundary is mathematically appropriate: the result is local for each fixed \(q\in(0,q_c)\), not uniform in \(q\), not global in \(\mu\), and makes no endpoint claim where the raw quartic coefficient degenerates.

## 6. Clean regeneration and supplied controls

From an empty B2.4 record state, `run_B2_4.py all` regenerated both outputs byte-for-byte:

| record | regenerated SHA-256 |
|---|---|
| `data/B2_4_branch.json` | `3d92a5666a750184d829787e5c854a43c3b436546e53fcd967f7a870aa93c9a6` |
| `data/B2_4_dependency_graph.json` | `898a00046051745906f2724d9fe4cfe913bfb19501026ddac9b6c070f914c978` |

The regenerated exact and numerical layers both reported `True`. The numerical record contains **22 checks at each of four \(q\) values, 88/88 passed**.

With the authenticated Paper 2 archive supplied explicitly, the complete dev.5 suite gave:

\[
\boxed{397\ \text{passed},\ 0\ \text{failed},\ 0\ \text{skipped}}
\]

in 268.60 seconds. This includes the 21 incorrect statements and ten invalid dependency graphs being rejected.

Other replay results:

- all **22/22** B2.4 code mutations detected;
- all **15** targeted mutation baselines passed unmutated first;
- all **45/45** forbidden identity modifications rejected;
- the unmodified identity-control baseline passed;
- both regenerated control records were byte-identical to their supplied counterparts.

The two skips described in the completion report were environmental Paper 2 archive lookups. Supplying the authenticated archive eliminated both skips; this is not a package defect.

## 7. Independent raw 24-dimensional numerical corroboration

A separate numerical implementation used no project imports. It constructed the raw pair energy, analytic gradient, and analytic Hessian directly in 24 coordinates. It independently located each curve point by solving \(\det K=0\) in the \((\widehat u_1,\widehat v_1)\) block, formed the kernel vector from that block, computed \(\tau\) by differentiating the raw restricted Hessian, and computed \(c_4\) from raw mixed derivatives plus an analytic pair-distance Taylor expansion of the fourth directional derivative.

At \(q=0.2,0.8,1.5,2.0\), this route found:

- maximum curve-point difference from the 25-digit stored values: \(4.09\times10^{-25}\);
- maximum relative \(c_4\) difference from the 20-digit stored values: \(1.94\times10^{-20}\);
- maximum relative \(\tau\) difference from the stored values: \(1.23\times10^{-20}\);
- axial-kernel residuals at the located curve points, with largest norm \(1.22\times10^{-65}\).

Independent Newton runs at both signs of the starting amplitude and at \(\mu/P_T=\pm10^{-6},\pm10^{-7}\) confirmed:

- both \(\pm s_*\) for positive \(\mu\);
- return to the cube for negative \(\mu\) from the mirror-amplitude starts;
- maximum full 24-dimensional gradient norm \(3.24\times10^{-65}\);
- amplitude-error ratios between approximately \(9.9999934\) and \(9.9999966\) when \(\mu\) was reduced by ten;
- the predicted axial curvature signs;
- exchange of the located pair by an independently identified reversing group element, with maximum residual \(3.09\times10^{-60}\).

This numerical work is corroboration only and is not needed for the proof verdict.

## 8. Independent adversarial controls

Separate adversarial checks rejected:

- either wrong input sign and the resulting wrong branch side;
- omission of the factor six in \(G\), \(\mu_*'(0)\), or the amplitude law;
- a branch claimed for \(\mu<0\) or on both sides;
- a wrong axial-curvature sign or omission of the factor two;
- an odd cubic term that breaks evenness;
- isotropy larger than \(\Sigma\);
- classification as a cuboid;
- numerical scans or located branch points used as proof dependencies;
- omission of the transversality input;
- any upgrade of axial curvature to full-space stability or a centre-manifold index.

All independent exact, numerical, and adversarial checks passed.

## 9. Findings

### CRITICAL

None.

### MAJOR

None.

### MINOR

None.

### INFORMATIONAL

1. Proposition B2 uses certified Lemma Q as an allowed input. This audit validates the B2.4 derivation and the dependency boundary, but does not independently re-audit the B2.3 certificate itself.
2. The completion report's two skipped tests were environmental. With the authenticated Paper 2 archive, the complete suite is 397 passed with no skips.
3. Numerical branch location and reduced scans are correctly labelled as corroboration. Local exclusion of nontrivial equilibria for \(\mu\le0\) follows from the analytic implicit-function argument, not from sampling.

None of these items requires a correction.

## 10. Formal determinations

| question | determination |
|---|---|
| Is the fixed-space parity argument correct? | **Yes.** The eight reversing elements act as \((s,w_f)\mapsto(-s,-w_f)\), and the reduced potential is even. |
| Is the Schur-complement identity correct? | **Yes.** \(\lambda=\det K/(f^TKf)\), \(\lambda(0)=0\), and \(\lambda'(0)=\tau<0\). |
| Is the quartic coefficient used correctly? | **Yes.** The B2.1 reduction formula is reproduced independently, and \(c_4>0\) follows from the permitted Lemma Q input. |
| Is the factor \(c_4/6\) correct? | **Yes.** |
| Are the implicit-function slopes correct? | **Yes.** \(\mu_*'(0)=-c_4/(6\tau)>0\) and \(s_*^2=-6\tau\mu/c_4+O(\mu^2)\). |
| Is the branch confined to \(\mu>0\)? | **Yes.** No nontrivial local equilibrium exists for \(\mu\le0\). |
| Is the pair a \(\mathbb Z_2\)-symmetric supercritical pitchfork in the stated convention? | **Yes.** |
| Are the axial curvature formulas and signs correct? | **Yes.** They are \(\tau\mu+O(\mu^2)\) at the cube and \(-2\tau\mu+O(\mu^2)\) on the nontrivial pair. |
| Is the isotropy exactly \(D_{2h}\)? | **Yes.** Every element outside \(\Sigma\) is excluded by an exact rank-two argument. |
| Is the non-cuboid and first-order rhombic/sheared geometry justified? | **Yes.** |
| Are second-order corrections confined to \(A_{1g}/E_g\), with \(f_1=O(s^3)\) on the branch? | **Yes.** |
| Does the proof depend on numerical scans or numerical branch location? | **No.** |
| Does any axial curvature statement justify full-space stability or a centre-manifold index? | **No.** The package correctly makes neither claim. |
| Did B2.4 alter earlier tracks or certificates? | **No.** The identity chain and independent hashes confirm preservation. |
| Is a B2.4 correction required? | **No.** |

## 11. Verdict

**PASS.** Proposition B2's B2.4 derivation is mathematically valid under its six declared inputs. The branch side, local equilibrium count, \(\mathbb Z_2\) exchange, energy-reduced axial classification, axial curvature signs, exact isotropy, non-cuboid status, and first- and second-order geometry are all supported. Reproduction, tests, identity controls, mutation controls, and independent adversarial checks are effective.

The B2.4 derivation may be recorded as independently audited. Lemma Q's own B2.3 certificate remains a separate, not-independently-audited input and is not certified anew by this report. No mathematical, code, data, dependency-graph, or wording correction is required for B2.4. B2.5 remains outside scope and was not started.
