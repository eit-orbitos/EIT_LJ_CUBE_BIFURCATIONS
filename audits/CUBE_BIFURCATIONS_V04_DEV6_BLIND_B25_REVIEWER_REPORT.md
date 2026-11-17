# Blind independent audit of Paper 3 V0.4-dev.6 — Phase B2.5 only

**Audit date:** 2026-11-15  
**Auditor:** Kimi Agent  
**Formal verdict:** **PASS**  
**Findings requiring correction:** none

## 1. Scope and audit position

This is a fresh blind independent audit of Phase B2.5, Proposition B3, and Corollary B3′ in `EIT_LJ_CUBE_BIFURCATIONS_V0.4-dev.6.zip`. All B2.5 code, formulas, tests, numerical records, dependency graphs, and conclusions were treated as untrusted. The exact derivations were reconstructed without importing the B2.5 implementation, and the numerical corroboration was separately implemented from the raw 24-dimensional pair energy.

The audit used the independently audited Lemma K/\(\kappa\ne0\), Proposition B2, exact \(O_h/T_{2g}\) structure, standard Lyapunov–Schmidt/centre-manifold theory, and the frozen Paper 2 spectrum only at the declared boundaries. It did not use Ihrig's theorem, numerical scans, or branch-location calculations as proof inputs.

No stability claim is inferred from either index statement. Paper 2 remained read-only. No uploaded archive or project source tree was modified. Nothing was frozen, published, pushed, released, or uploaded. A3, \(C_{2h}\), and every other new mathematical track remained outside scope and were not started.

## 2. Authenticated inputs and preservation boundary

### 2.1 Input hashes

| input | SHA-256 | result |
|---|---|---|
| `EIT_LJ_CUBE_BIFURCATIONS_V0.4-dev.6.zip` | `c473af60f8b54c0beecd252d9e8409eef734ba475c0d693b300946f57941b691` | matches the required hash |
| `EIT_LJ_FULL_VECTOR_STABILITY_V1.0(3).zip` | `bb70721df7f0aa17edca30d84d1b4aaf980c0a76693be14fa780e4ab8f64762d` | frozen Paper 2 input authenticated |
| supplied B2.3 / Lemma Q independent report | `841152f2cccd0a43c4f8e73ce5d0cf37e9793d26f12047d5143ea5a053e96bcf` | exact earlier audit artifact |
| supplied B2.4 / Proposition B2 independent report | `0302930b9a96ac6bca3df4e720ba34ab5937f73944aee76ba85f345706bdb1ec` | exact earlier audit artifact |

The dev.6 internal integrity list was checked entry by entry: **124/124 entries passed**. The supplied B2.3 and B2.4 reports therefore correspond to the exact independently delivered artifacts used to authenticate the two audited B2.5 inputs.

### 2.2 dev.5-to-dev.6 identity check

The identity checker was rerun against the authenticated dev.5 archive, SHA-256 `77267d56f7a271b81b6cc91166f6750c71e1fc4f214c337f016ecf75b4563949`. Its result was **PASS**:

- 10 permitted additions;
- one append-only file;
- five permitted changed files;
- 107 byte-identical files;
- one regenerated integrity list;
- no deleted or unexpected files.

The NOTES §§1–12 extract remained byte-identical, with SHA-256 `2d23da494ff7381ff2d2106cea313f8b6dba7a0f082475905815dcf625952168`. The enforced boundary also preserved, among other earlier artifacts:

- historical B1 certificate: `dee3ad024af69f76620de35f3d0aa8be06a9f4f099ca0ffb001c4914178f87ab`;
- B2.3 certificate: `9f6b31404ce9e03372b321567f53cb95254e2955c332e7eea7c381ca0f4d4209`;
- B2.3 check report: `34ba30d3879393e6bb9c727c17629ee67bec79379276edbc3030f427d63a23b9`;
- B2.4 branch record: `3d92a5666a750184d829787e5c854a43c3b436546e53fcd967f7a870aa93c9a6`;
- B2.4 dependency graph: `898a00046051745906f2724d9fe4cfe913bfb19501026ddac9b6c070f914c978`.

All **62/62** forbidden identity modifications were rejected, and the unmodified identity-control baseline passed. Track A, B0, B1 including the erratum artifacts, B2.0–B2.4, Paper 2 inputs, earlier scripts, certificates, records, and included audits remain inside the enforced preservation boundary.

## 3. Clean regeneration and supplied controls

Clean regeneration reproduced the supplied B2.5 records byte-for-byte:

| record | regenerated SHA-256 |
|---|---|
| `data/B2_5_index.json` | `4e54e4ad536a637c049d3f566a3a41dc4cab3c4089678915622db1f5a7ab7458` |
| `data/B2_5_dependency_graph.json` | `e9b728c32fd200481d7c35124acc3d52678721d067708dddfea9580f471c4a4e` |
| `data/B2_5_negative_controls.json` | `82080692a8d6465b9bc0d8f6f66ffde9ef9dc66ad625b36dc4ca29d9f626932c` |

The regenerated exact layer reported **32/32 checks passed**. The regenerated numerical layer reported **300/300 checks passed**. These package checks were treated only as reproduction evidence; the mathematical and independent numerical verdicts below do not rely on them.

Other replay results were:

- focused B2.5 tests with the authenticated Paper 2 archive present: **71 passed**;
- freshly executed B2.5 code mutations: **28/28 detected**, with every targeted unmutated baseline passing;
- complete project suite, run in subsets within the execution window: **469 passed, 0 failed**;
- identity controls: **62/62 forbidden modifications rejected**.

No test or mutation result was accepted as a substitute for the independent derivations.

## 4. Independent \(T_{2g}\) invariant reconstruction

The three-dimensional representation was reconstructed directly as the 24 signed permutation matrices

\[
T_{i,\pi(i)}=\varepsilon_i,\qquad
\varepsilon_1\varepsilon_2\varepsilon_3=1,
\]

with no project import. Reynolds projection on homogeneous polynomial spaces gave independently

\[
\dim\mathcal P_1^G=0,\qquad
\dim\mathcal P_2^G=1,\qquad
\dim\mathcal P_3^G=1,\qquad
\dim\mathcal P_4^G=2.
\]

The reconstructed invariant spans were exactly

\[
\mathcal P_2^G=\operatorname{span}\{I_2\},\qquad
\mathcal P_3^G=\operatorname{span}\{I_3\},\qquad
\mathcal P_4^G=\operatorname{span}\{I_2^2,I_4\},
\]

where

\[
I_2=|a|^2,\qquad I_3=a_1a_2a_3,\qquad
I_4=a_1^4+a_2^4+a_3^4.
\]

Consequently, every smooth equivariant Lyapunov–Schmidt reduced potential has the stated local form

\[
V_{\rm red}
=V_0+\frac12\lambda I_2+\kappa I_3
+\alpha I_2^2+\beta I_4+O(|a|^5),
\]

with coefficients analytic in \(\mu\). No higher-degree invariant is needed for the B2.5 inertia argument.

The cubic normalization was also checked explicitly. For \(x=\sum_i a_ie_i\),

\[
D^3V[x,x,x]=6\kappa a_1a_2a_3,
\]

whereas the mixed multilinear derivative satisfies

\[
\kappa=D^3V[e_1,e_2,e_3].
\]

The factor six belongs to the diagonal trilinear evaluation, not to the mixed coordinate derivative.

## 5. Independent complete quartic Lyapunov–Schmidt correction

Starting with the raw energy on the critical-plus-noncritical decomposition, the stationary transverse equation gives

\[
w(x)=-\frac12H_{WW}^{-1}b(x)+O(|x|^3),
\qquad b(x)=D^3V[x,x,\cdot]|_W.
\]

Substitution through degree four independently yields the multidimensional formula

\[
V_4(x)=\frac1{24}D^4V[x,x,x,x]
-\frac18\langle b(x),H_{WW}^{-1}b(x)\rangle.
\]

The raw 24-dimensional calculation determined the complete support of \(b\), rather than assuming the axial support:

\[
\operatorname{supp}(b)=A_{1g}\oplus E_g\oplus T_{2g}.
\]

Within the noncritical complement \(W\), only \(A_{1g}\), \(E_g\), and the upper noncritical \(T_{2g}\) vectors \(f_k\) contribute. The critical \(e_k\)-components do not enter \(H_{WW}^{-1}\). The reconstruction included the arbitrary-chart normalization \(\|e_k\|^2=\|f_k\|^2=n_u^2+n_v^2\), and the raw residual against the reconstructed support vanished exactly.

Independent pair-distance chain rules were used for \(D^2,D^3,D^4\). In particular, for \(\psi(|r|^2)\), \(A_i=2r\cdot v_i\), and \(B_{ij}=v_i\cdot v_j\),

\[
\begin{aligned}
D^4\psi[v_1,v_2,v_3,v_4]
={}&\psi_4A_1A_2A_3A_4
+2\psi_3\sum_{\{i,j\}\subset\{1,2,3,4\}}B_{ij}A_kA_l\\
&+4\psi_2(B_{12}B_{34}+B_{13}B_{24}+B_{14}B_{23}),
\end{aligned}
\]

where \(\{k,l\}\) is the complement of \(\{i,j\}\), and the middle sum has exactly six off-diagonal pairs. The raw derivative implementation was cross-checked against high-precision differentiation.

The resulting quartic contains only the three \(a_i^4\) and three \(a_i^2a_j^2\) monomial types and is exactly

\[
V_4=\alpha I_2^2+\beta I_4.
\]

On the \(D_{2h}\) axis \(a=(s,0,0)\), both quartic invariants equal \(s^4\). Independently evaluating the raw axial Lyapunov–Schmidt formula therefore gives

\[
V_4(se_1)=(\alpha+\beta)s^4=\frac{c_4}{24}s^4,
\qquad\boxed{\alpha+\beta=\frac{c_4}{24}}.
\]

## 6. Reduced Hessian on the \(D_{2h}\) branch

At \(a=(s,0,0)\), the independently reconstructed stabilizer image in the three-dimensional representation has order four. Solving the symmetric commutant equations gives exactly

\[
H_c(s)=
\begin{pmatrix}
h_{11}&0&0\\
0&d&e\\
0&e&d
\end{pmatrix}.
\]

The four independently identified reversing elements imply

\[
h_{11}(-s)=h_{11}(s),\qquad d(-s)=d(s),\qquad e(-s)=-e(s).
\]

Thus \(h_{11}\) and \(d\) are even and \(e\) is odd. In particular, symmetry forbids an \(O(s)\) diagonal term; this is not an asymptotic approximation.

For a generic invariant potential, direct differentiation on the axis gives, before imposing the branch equation,

\[
h_{11}=\lambda+12(\alpha+\beta)s^2+O(s^4),
\]

\[
d=\lambda+4\alpha s^2+O(s^4),
\qquad e=\kappa s+O(s^3).
\]

The axial equilibrium equation independently gives

\[
\mu=-\frac{c_4}{6\tau}s^2+O(s^4),
\qquad \lambda=\tau\mu+O(\mu^2)
=-\frac{c_4}{6}s^2+O(s^4).
\]

Substitution on the audited Proposition-B2 branch therefore yields

\[
\boxed{h_{11}=\frac{c_4}{3}s^2+O(s^4)},
\]

\[
\boxed{d=-4\beta s^2+O(s^4)},
\qquad
\boxed{e=\kappa s+O(s^3)}.
\]

Equivalently, \(h_{11}=-2\tau\mu+O(\mu^2)>0\), consistently with the independently audited B2.4 result.

## 7. Rigorous transverse inertia and remainder control

The transverse block has exact eigensystem

\[
(d+e,\ (0,1,1)/\sqrt2),\qquad
(d-e,\ (0,1,-1)/\sqrt2).
\]

Its leading determinant is

\[
(d+e)(d-e)=d^2-e^2=-\kappa^2s^2+O(s^4).
\]

The sign conclusion was nevertheless proved with an explicit remainder bound, not from big-O notation alone. On a sufficiently small neighbourhood, write

\[
d=s^2D(s),\qquad e=s(\kappa+s^2E(s)),
\]

with \(|D|\le C_D\) and \(|E|\le C_E\) for \(|s|\le r\le1\). Then the exact identity is

\[
(d+e)(d-e)
=s^2\left[s^2D^2-(\kappa+s^2E)^2\right].
\]

If \(C_D+C_E>0\) and

\[
0<|s|<\frac{|\kappa|}{C_D+C_E},
\]

then, since \(|s|\le1\),

\[
|\kappa+s^2E|
\ge |\kappa|-C_Es^2
>C_D|s|
\ge |sD|.
\]

If \(C_D=C_E=0\), the conclusion is immediate. Hence \(e^2>d^2\) strictly and

\[
(d+e)(d-e)<0.
\]

The two transverse eigenvalues are therefore nonzero and have opposite signs. The argument uses only \(\kappa\ne0\) and the local Taylor bounds. It is independent of the sign or gauge of \(\kappa\), the replacement \(s\mapsto-s\), and the sign of \(\beta\). A separate exact rational sweep of 432 remainder cases agreed with the analytic inequality.

## 8. Centre-manifold Morse index and conjugate branches

Audited Proposition B2 supplies the positive axial eigenvalue \(h_{11}>0\). Section 7 supplies one negative and one positive transverse eigenvalue. The centre Hessian consequently has inertia

\[
\boxed{(n_-,n_0,n_+)=(1,0,2)},
\]

and therefore

\[
\boxed{\operatorname{index}_{centre}=1,
\qquad \operatorname{nullity}_{centre}=0}.
\]

This uses both the axial and transverse blocks. Positive axial curvature alone would not determine the centre index.

The independently reconstructed \(O_h\)-orbit of the axial reduced points is

\[
\{\pm se_1,\ \pm se_2,\ \pm se_3\},
\]

which has six elements and is one orbit. Orthogonal equivariance gives

\[
H_c(Ta)=T H_c(a)T^T.
\]

Orthogonal congruence preserves inertia, so all six conjugate \(D_{2h}\) branch points have exactly the same centre index and nullity.

## 9. Independent frozen Paper 2 complement and full-slice inertia

The value \(m_\perp=3\) was not imported from dev.6. It was reconstructed from the supplied frozen Paper 2 manuscript: the \(O_h\) block decomposition in §4, the reduced-Hessian and rigid-mode definitions in §2, and Lemmas S, E, T1, T3, and T4 with the region table in §5.

On \(p=P_T(q)\), \(0<q<q_c\), the independent block count is:

| Paper 2 sector | multiplicity | sign/status on the curve |
|---|---:|---|
| \(A_{1g}\) | 1 | positive, Lemma S |
| \(E_g\) | 2 | positive, Lemma S |
| rotations \(T_{1g}\) | 3 | rigid zero, excluded from \(H_{\rm red}\) |
| lower critical \(T_{2g}\) | 3 | critical zero, Lemma T3; excluded from \(W\) |
| upper noncritical \(T_{2g}\) | 3 | positive, Lemma T1 |
| \(A_{2u}\) | 1 | negative, Lemma T4 |
| \(E_u\) | 2 | negative, Lemma E |
| translations \(T_{1u}\) | 3 | rigid zero, excluded from \(H_{\rm red}\) |
| internal \(T_{1u}\) | 3 | positive, Lemma S |
| \(T_{2u}\) | 3 | positive, Lemma S |

Before removing the critical triple, the nonrigid reduced Hessian has index 3 and nullity 3. Removing the three critical zero directions leaves the 15-dimensional noncritical complement \(W\), with

\[
\boxed{\operatorname{inertia}(H_{WW})=(3,0,12)},
\qquad \boxed{m_\perp=3}.
\]

In particular \(H_{WW}\) is nonsingular at the cube. Its inertia remains \(3/0/12\) on the sufficiently local branch by continuity and the minimum absolute eigenvalue staying away from zero.

For the actual displaced equilibrium, the reduced centre Hessian is the Schur complement

\[
S=H_{CC}-H_{CW}H_{WW}^{-1}H_{WC},
\]

not merely the raw diagonal block \(H_{CC}\). Haynsworth inertia additivity gives

\[
\operatorname{inertia}(H_{\rm slice})
=\operatorname{inertia}(H_{WW})+\operatorname{inertia}(S).
\]

Therefore

\[
\operatorname{index}_{slice}=3+1=4,
\qquad
\operatorname{nullity}_{slice}=0+0=0,
\]

and the positive count is \(12+2=14\). Thus

\[
\boxed{\operatorname{inertia}(H_{\rm slice})=(4,0,14)}.
\]

Restoring the six rigid infinitesimal translations and rotations adds six zero eigenvalues and leaves every nonrigid sign unchanged:

\[
\boxed{\operatorname{inertia}_{\mathbb R^{24}}=(4,6,14)}
\]

in negative/zero/positive order. The six rigid zero modes are not slice directions and are not included in the slice nullity or Morse index.

## 10. Independent dependency-graph audit

An independent parser and traversal, not the package validator, checked `data/B2_5_dependency_graph.json`. The graph has 17 proof nodes and 31 dependency edges. It is closed and acyclic.

For Proposition B3, the reachable leaves are exactly:

1. exact \(O_h/T_{2g}\) structure;
2. independently audited Lemma K, \(\kappa\ne0\);
3. independently audited Proposition B2;
4. standard Lyapunov–Schmidt/centre-manifold theory.

Every other reachable node is a `VERIFIED-EXACT` derivation step. Proposition B3 does not reach the Paper 2 spectral input.

For Corollary B3′, the reachable leaf set is exactly the same set plus the explicitly named frozen Paper 2 spectral result. The numerical Hessian, derivative-free quartic, D3d numerical, and B2.2 scan records are outside the proof graph, as is the D3d consistency-only node. No numerical scan or branch-location calculation is a proof dependency.

Eight independent graph corruptions were all rejected: insertion of the numerical Hessian, insertion of the B2.2 scan, insertion of D3d consistency, a dangling edge, a cycle, removal of Lemma K, relabelling the frozen Paper 2 input as numerical, and removal of the Paper 2 dependency from the corollary.

## 11. Independent raw 24-dimensional numerical corroboration

A separate implementation used no project imports. It constructed the unit-edge cube and raw pair energy

\[
V(x)=\sum_{i<j}\left(t_{\rm eq}(p,q)|x_i-x_j|^{-p}-|x_i-x_j|^{-q}\right),
\]

together with its analytic gradient, analytic Hessian, and analytic pair-distance derivatives through fourth order. It independently located \(P_T(q)\) by solving \(\det K=0\), formed the unit kernel and upper vectors, computed \(\tau,c_4,\alpha,\beta,\kappa\), solved the 18-dimensional rigid-slice equilibrium equations, and formed the full Hessian, \(W\)-block, and centre Schur complement.

The independently located curve points were:

| \(q\) | independent \(P_T(q)\) |
|---:|---:|
| 0.2 | 4.424754188126528 |
| 0.8 | 3.4719146272247556 |
| 1.5 | 2.5774133595470645 |
| 2.0 | 2.039927962193008 |

The independent \(c_4\) values agreed with the package to within \(2.0\times10^{-13}\) relative error, and the independent \(\kappa\) values to within \(1.7\times10^{-12}\). The finite-difference \(\tau\) values agreed to within \(1.9\times10^{-9}\) relative error; all other normal-form coefficient comparisons were at the expected double-precision level.

At every \(q\in\{0.2,0.8,1.5,2.0\}\), every relative \(\mu\in\{10^{-5},10^{-6},10^{-7}\}\), and both branch signs — **24 branch points in total** — the independent computation found:

- full-gradient infinity norm at most \(8.05\times10^{-16}\);
- raw \(\mathbb R^{24}\) inertia \(4/6/14\);
- rigid-slice inertia \(4/0/14\);
- \(W\)-index 3 and centre inertia \(1/0/2\);
- positive axial centre curvature and opposite transverse signs;
- maximum rigid-field Hessian residual \(9.54\times10^{-16}\);
- largest absolute eigenvalue associated with the six rigid directions \(3.67\times10^{-15}\), versus smallest absolute nonrigid eigenvalue \(3.87\times10^{-9}\);
- minimum absolute \(W\)-block eigenvalue \(0.0153080\).

The final independent numerical record has SHA-256 `b3f16e1e03f98f085e9741c8fb079814a3e16a61aaf8efec4af2e02a08285489`.

### 11.1 Raw convergence assessment without the adjusted tolerance

No \(50\mu\) or \(200\mu\) acceptance threshold was used. For the positive-sign points, the first tenfold reduction of \(\mu\) gave the following error-decade ratios; the negative-sign points behaved equivalently:

| relative leading-term error | \(10^{-5}\to10^{-6}\) ratio range | \(10^{-6}\to10^{-7}\) ratio range |
|---|---:|---:|
| \(h_{11}\) | 9.308–10.253 | double-precision floor reached |
| \(d\) | 9.471–11.915 | double-precision floor reached |
| \(e\) | 9.999868–10.000172 | 9.998831–10.000338 |

Thus all three errors decrease by approximately ten on the first decade, and \(e\) does so on both decades. At the smallest step, the \(h_{11}\) and \(d\) entries are obtained after inversion and subtraction in the double-precision Schur complement; their relative errors then sit at the numerical floor, with maximum absolute leading-term discrepancy approximately \(1.08\times10^{-12}\). This floor does not affect the eigenvalue signs or any inertia count.

For the difficult \(q=2.0\) case, the raw absolute-error/\(\mu\) ratios at the first two steps were approximately:

| coefficient | \(\mu/P_T=10^{-5}\) | \(\mu/P_T=10^{-6}\) |
|---|---:|---:|
| \(h_{11}\) | 51.42 | 55.24 maximum over the two signs |
| \(d\) | 51.36 | 54.85 maximum over the two signs |
| \(e\) | 53.42 | 53.41 |

These are direct convergence measurements, not thresholds. They explain why a fixed \(50\mu\) numerical comparison can fail while the mathematical \(O(\mu)\) relative-error statement remains valid. The later change to \(200\mu\) is therefore informational and post hoc. Neither tolerance occurs in the exact derivation or the dependency graph, and neither affects the proof or this verdict.

All numerical work in this section is corroboration only.

## 12. Independent adversarial rejection checks

Separate exact counterexamples and logical controls rejected every required incorrect claim:

1. **Positive-definite transverse block:** rejected by its negative determinant and one negative eigenvalue.
2. **Negative-definite transverse block:** rejected by the same indefinite eigensystem.
3. **Omission of \(\kappa s\):** rejected because it removes the leading \(-\kappa^2s^2\) determinant and can produce transverse zero or same-sign eigenvalues.
4. **Replacement \(\kappa s\mapsto\kappa s^2\):** rejected by parity and an explicit example in which both transverse eigenvalues are negative.
5. **Centre index from axial curvature alone:** rejected by two matrices with identical positive \(h_{11}\) but different centre indices.
6. **Full-space stability from index 1:** rejected by the negative centre direction; the full slice in fact has four negative directions.
7. **Rigid modes counted in the Morse/slice index:** rejected by the quotient construction, which changes raw \(4/6/14\) to slice \(4/0/14\), not to slice nullity 6.
8. **Assuming \(m_\perp=3\):** rejected as underdetermined without the frozen block signs; changing the \(E_u\) sign, for example, would give \(m_\perp=1\).
9. **Any wrong noncritical Paper 2 block sign:** every individual sign flip was checked and changed the predicted full index away from 4.
10. **Full index 4 without Haynsworth/Schur splitting:** rejected by the coupled matrix \(\begin{pmatrix}1&2\\2&1\end{pmatrix}\), whose raw diagonal-block indices sum to 0 but whose Schur complement is \(-3\) and whose actual full index is 1.

The independent adversarial record contains **10/10 rejected claims** and has SHA-256 `3f985032d4b65950fe491bcaebd69504f97e9a6d2b1f501b3161dffd530b3e14`.

## 13. Findings

### CRITICAL

None.

### MAJOR

None.

### MINOR

None.

### INFORMATIONAL

1. The post-hoc numerical tolerance change from \(50\mu\) to \(200\mu\) has no proof role. Independent raw ratios show genuine first-order error decay without adopting either threshold.
2. The independent double-precision Schur calculation reaches its relative-error floor for \(h_{11}\) and \(d\) at the smallest tested step. This is explicitly separated from the mathematical asymptotic argument and does not alter any sign or inertia result.
3. Proposition B3 is local for each fixed \(q\in(0,q_c)\). Its analytic Taylor-remainder argument does not supply an explicit uniform radius in \(q\); no such stronger claim is made.
4. The archive's internal status strings were not edited after this external audit. Their historical `not independently audited` wording is not a mathematical or wording defect in dev.6 itself.

None of these items requires a correction.

## 14. Formal determinations

| requested question | determination |
|---|---|
| 1. Is Proposition B3 valid? | **Yes.** The independent invariant, quartic, branch-Hessian, transverse-remainder, and centre-inertia derivations establish it under the declared audited inputs. |
| 2. Are centre index 1 and nullity 0 valid? | **Yes.** The centre inertia is exactly \(1/0/2\) in negative/zero/positive order. |
| 3. Do all \(D_{2h}\) conjugate branches have the same index? | **Yes.** The six points form one \(O_h\)-orbit and their reduced Hessians are orthogonally congruent. |
| 4. Does \(m_\perp=3\) follow from frozen Paper 2? | **Yes.** Independent counting gives \(E_u\) multiplicity 2 and \(A_{2u}\) multiplicity 1 negative, with no noncritical zero and 12 positive complement directions. |
| 5. Is Corollary B3′ full-slice index 4 valid? | **Yes.** Haynsworth/Schur addition gives \(3+1=4\), with slice nullity 0. |
| 6. Is raw \(\mathbb R^{24}\) inertia \(4/6/14\) valid? | **Yes.** Restoring exactly six rigid zero modes to slice \(4/0/14\) gives raw \(4/6/14\). |
| 7. Does any claim amount to a stability overclaim? | **No.** The package does not claim stability, and this audit makes no such inference. Index 1 on the centre and index 4 on the slice certify negative directions, not stability. |
| 8. Does the post-hoc numerical tolerance affect the proof? | **No.** It is absent from the exact proof and dependency graph and was not used in the independent numerical assessment. |
| 9. Is any mathematical, code, or wording correction required? | **No.** No B2.5 defect requiring correction was found. |

## 15. Verdict

**PASS.** Proposition B3 and Corollary B3′ are mathematically valid under their declared inputs. The centre index and nullity are \(1\) and \(0\), all six conjugate branches have the same index, frozen Paper 2 independently yields \(m_\perp=3\), the full rigid slice has index \(4\) and nullity \(0\), and the raw \(\mathbb R^{24}\) inertia is \(4/6/14\).

Archive authentication, manifest verification, clean regeneration, tests, fresh mutations, identity controls, dependency-graph controls, independent raw numerical corroboration, and independent adversarial checks all passed. No mathematical, code, data, dependency-graph, or wording correction is required for B2.5. No stability claim is justified or made, and the post-hoc numerical tolerance has no effect on the proof.
