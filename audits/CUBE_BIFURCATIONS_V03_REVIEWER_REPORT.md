# Independent Reviewer Report
## EIT–LJ Cube Bifurcations — V0.2.1-dev correction chain and V0.3-dev Phase B1

**Audit date:** 2026-11-14  
**Reviewer:** Kimi Agent  
**Audited packages:**

- `EIT_LJ_CUBE_BIFURCATIONS_V0.2.1-dev.zip`
- `EIT_LJ_CUBE_BIFURCATIONS_V0.3-dev.zip`

**Read-only frozen input:** `EIT_LJ_FULL_VECTOR_STABILITY_V1.0.zip` (Paper 2)  
**Prior audit retained:** `CUBE_BIFURCATIONS_REVIEWER_REPORT.md` for V0.2-dev Track A  
**Report status:** independent mathematical, certificate, identity-chain, and reproduction audit

## 1. Scope and decision questions

This report separately addresses four questions:

1. Does V0.2.1-dev implement the two documentation corrections required by the completed Track A audit, without changing the audited mathematics or Lemma M certificate?
2. Does V0.3-dev preserve the audited Track A material and the B0 mathematical layer?
3. Is the new B1 Lemma K certificate a rigorous proof that the normalised cubic carrier is positive on the closed physical \(T_{2g}\) curve?
4. Does Proposition B1 correctly derive the local two-sided \(D_{3d}\) transcritical branches, with the stated signs and without an unstated stability claim?

The audit includes independent exact derivations, an independent interval-arithmetic replay, examination of the physical-curve and corner identification, inspection of the proof dependencies, and a complete reproduction of the supplied suites. Passing package tests are treated as controls, not as substitutes for the mathematical audit.

The following were not audited as new claims and remain outside scope:

- stability of the \(D_{3d}\) branches;
- the \(D_{2h}\) quartic coefficient, branch equation beyond its retained parity observation, or stability;
- any B2 work;
- any revision of Paper 2;
- freezing, publication, repository changes, or release authorisation.

## 2. Input authentication and integrity

### 2.1 Archive hashes

| archive | independently computed SHA-256 |
|---|---|
| V0.2-dev, audited baseline | `ba835b0dee8cb6d80214b4bd9a61bf2a65d6a4d52376b4e7e0a3dcfd71691e30` |
| V0.2.1-dev | `3bd6ac4200122610f6d4f6a6fd4b19b5ff43117398f5b324dabc59c92c2a9f55` |
| V0.3-dev | `3901c0db5daf3d7862629bca61e5a49b7bd15faeedcf44fab007ada6ffc128fe` |
| Paper 2 V1.0 | `bb70721df7f0aa17edca30d84d1b4aaf980c0a76693be14fa780e4ab8f64762d` |

The Paper 2 hash exactly matches both the supplied value and `reference/PAPER2_INPUTS.md`. All **102/102** entries in Paper 2's internal `SHA256SUMS` passed. Paper 2 was used read-only.

The package integrity checks gave:

- V0.2.1-dev: **43/43** internal entries passed;
- V0.3-dev: **56/56** internal entries passed.

### 2.2 Reproduction environment

The reproduction environment used Python 3.12.12, python-flint 0.9.0, FLINT 3.6.0, SymPy 1.14.0, mpmath 1.3.0, NumPy 2.2.5, SciPy 1.16.2, pytest 9.2.0, and gmpy2 2.3.2. The independent B1 interval audit used Arb at 192 bits with Taylor order 24; the corner sign cross-check used 640 bits.

## 3. V0.2.1-dev correction and identity audit

### 3.1 MINOR-01: tetrahedron wording

The operative statements in `NOTES.md` and `README.md` now describe the branch configurations as:

> two concentric regular tetrahedra of unequal radii on inversion-related vertex-direction sets.

They also correctly state that spatial inversion exchanges the complete branch configurations \(x_+\) and \(x_-\), not the unequal-radius shells within one fixed configuration. The older wording remains only where the audit history explicitly quotes the correction. This resolves MINOR-01 without changing the geometry or the theorem.

### 3.2 MINOR-02: negative-control count

`NOTES.md` §3.7 now gives **17/17**, consistently with the V0.2.1 suite and research log. The stale operative count “15 of 15 in total” is absent. This resolves MINOR-02.

### 3.3 No mathematical drift from V0.2-dev

The independent file-by-file comparison verified every row of `docs/V0.2.1-dev_DIFF_CHECK.md`. The only differences from V0.2-dev are the declared documentation additions/edits, version/status metadata, and regenerated integrity list.

In particular:

- the Lemma M certificate and semantic hash file are byte-identical;
- every A0/A1/A2/B0 mathematical module other than the two declared metadata files is byte-identical;
- every A0/A1/A2/B0 mathematical test and every script is byte-identical;
- the Theorem A graph agrees after masking exactly its two declared status fields;
- `theorem_a.py` differs only in `THEOREM_STATUS`;
- the included Track A reviewer report is byte-identical to the delivered report.

The included report SHA-256 is:

`f82c5ef1a03c33c0909313bd6442d1879d39717f991cc8e245eb0c61f75d8b85`.

## 4. V0.3-dev preservation of Track A and B0

The independent comparison verified every row of `docs/V0.3-dev_TRACK_A_IDENTITY.md`.

The following hold:

- all declared Track A and B0 source, script, test, and data files are byte-identical to V0.2.1-dev;
- `NOTES.md` §§1–3.10 are byte-identical to V0.2.1-dev, with SHA-256
  `7fde8afa5cdbc439391416de46608f67c05cdec9b13f0470861b2e8edb7f6a02` for that extracted exposition;
- the changing package/version header before §1 is not part of the claimed identical mathematical exposition;
- `RESEARCH_LOG.md` is append-only;
- the first 17 negative-control records are unchanged and V0.3-dev contains 24;
- the 12 declared B1 files are additions;
- `__init__.py` and `test_docs.py` contain only the documented version/status changes;
- the prior Track A report remains byte-identical.

Consequently, the new B1 material does not alter the audited Track A proof or certificate.

## 5. Complete reproduction

With the authenticated Paper 2 archive supplied as the frozen input, the reproduction produced:

| check | result |
|---|---|
| V0.2.1-dev full suite | **130 passed**, 0 failed |
| V0.3-dev A0, A1, B0, A2, B1 regeneration | all completed successfully |
| V0.3-dev full suite | **195 passed**, 0 failed, 0 skipped |
| V0.3-dev negative controls | **24/24 detected** |
| A2 semantic hash after replay | `49dce160b2a17a9f61554200617b9a75b5b02e244e21963b5956317156b6a71e` |
| B1 semantic hash after regeneration and replay | `616817fcc70e0fab7f106404e5e5332b17b9c4480bd440355f1ac5257a8518c6` |

The stored B1 certificate has 222 boxes, maximum depth 2, and minimum recorded lower bound \(1311719/536870912\). The supplied independent checker confirmed all 222 Newton inclusions and all 222 carrier bounds without refinement. These results were then checked again by the separate audit derivation described below.

## 6. Independent exact audit of the cubic coefficient

### 6.1 Direct 24-coordinate derivation

The audit constructed the cube labels, the two matched \(T_{2g}\) fields, and the pair energy directly. For each of the 216 basis triples, it differentiated the restriction of the 24-coordinate pair energy along the three selected directions. No B1 module, stored trilinear table, or closed form was imported for this derivation.

The independent computation found:

- 216 trilinear entries in total;
- exactly 48 nonzero entries;
- every nonzero entry has indices equal to a permutation of \((1,2,3)\);
- each channel is invariant under permutation of those indices;
- the mixed channels coincide as required by symmetry.

The four independent coefficients are exactly

\[
\begin{aligned}
t_{uuu}&=-12\psi''(2)-12\psi''(3)-32\psi'''(3),\\
t_{uuv}&=-\sqrt2\bigl(10\psi''(3)+16\psi'''(3)\bigr),\\
t_{uvv}&=-8\psi''(1)-8\psi''(3)-16\psi'''(3),\\
t_{vvv}&=-8\sqrt2\,\psi'''(3).
\end{aligned}
\]

Hence, for \(e_k=n_u\hat u_k+n_v\hat v_k\),

\[
\kappa=D^3V[e_1,e_2,e_3]
=t_{uuu}n_u^3+3t_{uuv}n_u^2n_v+3t_{uvv}n_un_v^2+t_{vvv}n_v^3.
\]

This independently confirms the cubic restriction \(D^3V[x,x,x]=6\kappa a_1a_2a_3\) for \(x=\sum a_ke_k\).

### 6.2 Two-term closed forms and factorisation

For \(\psi(\sigma)=\sigma^{-r/2}\), the audit independently derived

\[
D U_r=rW_r\,g_m(r)
\]

in each cubic channel and each Hessian entry. Writing \(X=2^{-r/2}\), \(Y=3^{-r/2}\), and \(W=1+X+Y/3\), the cubic functions are exactly

\[
\begin{aligned}
g_{uuu}&=\frac{(r+2)\left(-\frac34X+\frac{4r+7}{27}Y\right)}{W},\\
g_{uuv}&=\frac{\sqrt2(r+2)(4r+1)Y}{54W},\\
g_{uvv}&=\frac{(r+2)\left(-2+\frac{2(r+1)}{27}Y\right)}{W},\\
g_{vvv}&=\frac{\sqrt2(r+2)(r+4)Y}{27W}.
\end{aligned}
\]

The three independently derived Hessian entries also agree with Paper 2's \(M(r)\).

Since \(V=tU_p-U_q\) at the unit-edge equilibrium with \(t=qW_q/(pW_p)\),

\[
t_m=qW_q\bigl[g_m(p)-g_m(q)\bigr].
\]

With \(\delta=p-q\) and \(\widehat f(p,q)=(f(p)-f(q))/\delta\), continued analytically by \(f'(q)\) on the diagonal, this gives the claimed factorisation

\[
\kappa=qW_q\,\delta\,\widehat\kappa.
\]

No division by \(r\) occurs in any \(g_m\).

### 6.3 Projective chart

The audit independently verified

\[
\widehat M
\begin{pmatrix}1\\\rho\end{pmatrix}
=
\begin{pmatrix}\det\widehat M/\widehat M_{22}\\0\end{pmatrix},
\qquad
\rho=-\frac{\widehat M_{12}}{\widehat M_{22}}.
\]

Thus, on \(\det\widehat M=0\), positivity of \(\widehat M_{22}\) proves that \((1,\rho)\) spans the kernel. In this chart,

\[
\widehat\kappa=\widehat g_{uuu}+3\rho\widehat g_{uuv}
+3\rho^2\widehat g_{uvv}+\rho^3\widehat g_{vvv}.
\]

For unit \(n=(1,\rho)/\sqrt{1+\rho^2}\),

\[
\kappa=\frac{qW_q\delta\,\widehat\kappa}{(1+\rho^2)^{3/2}}.
\]

All factors outside \(\widehat\kappa\) are strictly positive for \(0<q<q_c\), so the certified carrier bound implies \(\kappa>0\) in the gauge \(n_u>0\).

## 7. Independent audit of Lemma K

### 7.1 Stored claim and coverage

The certificate covers

\[
q\in[0,101/50]
\]

by 222 gap-free rational boxes. There are 170 far-boxes and 52 near-diagonal boxes. Every non-corner \(\delta\)-ball is strictly positive; the unique corner box is

\[
Q=[2019/1000,101/50]
\]

and its \(\delta\)-ball straddles zero.

The claimed minimum is

\[
\widehat\kappa\geq \frac{1311719}{536870912}
=0.0024432670325\ldots>0.
\]

### 7.2 Parametric interval Newton step

For \(F(q,\delta)=\det\widehat M(q+\delta,q)\), each box proves a strict parametric interval Newton inclusion

\[
N(Q,m,D)=m-\frac{F(Q,m)}{\partial_\delta F(Q,D)}
\subset\operatorname{int}D,
\]

with \(\partial_\delta F(Q,D)\) bounded away from zero. The mean-value form in \(q\) encloses \(F(Q,m)\). This proves, for every \(q\in Q\), existence and uniqueness of a zero \(\delta_*(q)\) in the recorded ball and continuity of that zero.

The certificate does not rely on Newton iteration as an approximate solver. Numerical root finding supplies only starting estimates; the strict ball inclusions supply the proof.

### 7.3 Independent divided-difference enclosures

Far from the diagonal, the audit used direct ball quotients and the exact identities

\[
\partial_\delta\widehat f=\frac{f'(q+\delta)-\widehat f}{\delta},
\qquad
\partial_q\widehat f=\frac{f'(q+\delta)-f'(q)}{\delta}.
\]

Near the diagonal, it independently used

\[
\widehat f(q+\delta,q)
=\sum_{j=1}^{N}c_j(q)\delta^{j-1}
+\delta^N c_{N+1}(\xi),
\qquad c_j=f^{(j)}/j!,
\]

with \(\xi\) in the hull of \(Q\) and \(Q+D\). For the \(\delta\)-derivative, the audit used the integral identity

\[
\partial_\delta\widehat f(q+\delta,q)
=\int_0^1t f''(q+t\delta)\,dt,
\]

which yields the rigorous Taylor enclosure

\[
\partial_\delta\widehat f
\in
\sum_{j=2}^{N}(j-1)c_j(q)\delta^{j-2}
+N\delta^{N-1}c_{N+1}(\eta),
\qquad \eta\in\operatorname{hull}(Q,Q+D).
\]

The \(q\)-derivative was independently enclosed as

\[
\partial_q\widehat f
\in
\sum_{j=1}^{N}(j+1)c_{j+1}(q)\delta^{j-1}
+(N+2)\delta^Nc_{N+2}(\eta).
\]

This separate derivation is important because the generator and supplied checker share their near-diagonal differentiation implementation. As a diagnostic, their corresponding balls contained the independently computed derivative balls for all **364/364** near-box function components. The audit verdict, however, rests on the independently derived enclosures.

### 7.4 Independent interval result

The standalone 192-bit, order-24 replay confirmed:

| item | independent result |
|---|---|
| Newton inclusions | **222/222**, without refinement |
| carrier lower bounds | **222/222**, without refinement |
| \(\widehat M_{22}>0\) | confirmed on every box |
| far/near boxes | 170 / 52 |
| minimum lower bound | \(1311719/536870912\), on the first box |
| semantic hash | `616817fcc70e0fab7f106404e5e5332b17b9c4480bd440355f1ac5257a8518c6` |
| failures | **0** |

The carrier enclosures are mean-value forms in both \(q\) and \(\delta\), so positivity is proved over each full rectangle, not merely at sampled curve points.

### 7.5 Endpoints

At \(q=0\), an independent Newton inclusion inside the padded Paper 2 enclosure gave

\[
\widehat\kappa(0)
=0.002879512579955235482686978\ldots
\]

with the stored bound confirmed and \(\widehat M_{22}>0\).

At the corner, using Paper 2's 40-digit \(q_c\) enclosure and \(\delta=0\), the independent evaluation confirmed

\[
\widehat\kappa(q_c,q_c)
=0.006891782309648378299130289\ldots
\]

and \(\widehat M_{22}>0\). At 640 bits, \(\det M'\) was strictly positive at the left endpoint and strictly negative at the right endpoint of the \(q_c\) enclosure, consistently with Lemma T2.

Thus both limits of the closed physical curve are covered, even though raw \(\kappa\) vanishes linearly at each end through \(q\) or \(\delta\).

## 8. Physical-curve and corner identification

For every non-corner box, \(\delta>0\). Paper 2 Lemma T3 states that for \(0\leq q<q_c\) there is exactly one \(p=P_T(q)>q\) with \(D(p,q)=0\). Therefore the unique zero enclosed in the positive recorded ball is necessarily the physical curve point.

The corner box requires the additional argument, which was checked explicitly:

1. At \(q=2019/1000\), the independent Newton inclusion gives a strictly positive \(\delta\)-enclosure.
2. The parametric Newton inclusion makes the enclosed zero \(\delta_*(q)\) continuous throughout the corner box.
3. For \(q<q_c\), \(\delta_*(q)\) cannot pass through zero because
   \(\widetilde D(q,0)=\det M'(q)>0\) by Lemma T2.
4. Hence \(\delta_*(q)>0\) on \([2019/1000,q_c)\), and Lemma T3 again identifies it with \(P_T(q)-q\).
5. At \(q_c\), the enclosed zero is the diagonal corner \(\delta=0\).

The short mirror arc for \(q>q_c\) is additional certified coverage and is not mistaken for the physical \(p>q\) branch. The physical-curve selection is therefore valid through the corner, with no gap at either endpoint.

## 9. Transversality and Proposition B1

### 9.1 Transversality

For unit \(n\),

\[
\tau=n^T\partial_pK\,n
=qW_q\,n^TM'(P_T(q))n.
\]

On the curve, \(N=M(p)-M(q)\) is singular and symmetric with kernel \(n\). The independent exact identity

\[
\operatorname{adj}N=\operatorname{tr}(N)\,nn^T
\]

gives

\[
\partial_pD=\operatorname{tr}(N)\,n^TM'(p)n.
\]

Paper 2 Lemma T1 gives \(\operatorname{tr}K>0\), hence \(\operatorname{tr}N>0\); Lemma T3 gives \(\partial_pD<0\). Since \(qW_q>0\), it follows that \(\tau<0\) for every \(0<q<q_c\). The chart normalisation divides by the positive factor \(1+\rho^2\), so it does not change this sign.

### 9.2 Fixed subspace and one-dimensional reduction

An independently constructed 48-element signed-permutation action gave:

- the \(D_{3d}\) stabiliser of \((1,1,1)\) has order 12;
- its fixed space in \(\mathbb R^{24}\) has rank 3;
- it is spanned by the breathing field and the two matched \(T_{2g}\) diagonal fields;
- it contains no translation or infinitesimal rotation.

At the critical point, Paper 2 Theorem 4′ gives nullity 3, entirely in \(T_{2g}\), and excludes an additional \(A_{2u}\) zero on this curve. The intersection of the three-dimensional kernel with the \(D_{3d}\) fixed space is therefore exactly the diagonal direction \(E=e_1+e_2+e_3\).

With

\[
w\in\operatorname{span}\{e_{br},f_1+f_2+f_3\},
\qquad f_k=-n_v\hat u_k+n_u\hat v_k,
\]

Lyapunov–Schmidt reduction gives

\[
v(s,\mu)=v(0,\mu)+\frac32\lambda_{\rm red}(\mu)s^2
+\kappa(\mu)s^3+O(s^4).
\]

Consequently,

\[
\partial_sv=3s\,G(s,\mu),
\qquad
G(s,\mu)=\lambda_{\rm red}(\mu)+\kappa(\mu)s+O(s^2).
\]

The independent Schur-complement calculation confirms

\[
\lambda_{\rm red}(\mu)
=\frac{\det K(p)}{f^TK(p)f},
\qquad f=(-n_v,n_u),
\]

with

\[
\lambda_{\rm red}(0)=0,
\qquad
\lambda_{\rm red}'(0)=n^T\partial_pK\,n=\tau.
\]

The complementary denominator is nonzero near the curve, and the breathing direction does not couple to the \(T_{2g}\) block at second order because it belongs to a different irreducible representation.

### 9.3 Two-sided branch and sign

At \((s,\mu)=(0,0)\),

\[
G=0,\qquad G_s=\kappa\neq0,\qquad G_\mu=\tau\neq0.
\]

The implicit function theorem therefore gives the unique nontrivial local zero curve

\[
s_*(\mu)=-\frac{\tau}{\kappa}\mu+O(\mu^2).
\]

Because the slope is nonzero, \(s_*(\mu)\neq0\) for sufficiently small \(\mu\neq0\), on both sides of \(\mu=0\). Together with the persistent cube solution \(s=0\), this is a transcritical crossing, not a pitchfork.

Lemma K and transversality give \(\kappa>0\) and \(\tau<0\), hence

\[
-\tau/\kappa>0.
\]

In the gauge \(n_u>0\), \(s_*>0\) for \(p>P_T(q)\) and \(s_*<0\) for \(p<P_T(q)\). Conjugation by \(O_h\) gives the same conclusion on all four \(D_{3d}\) axes.

The numerical Newton branch finding is corroboration only. Neither existence nor two-sidedness nor the sign depends on it.

### 9.4 First-order geometry

The independent field computation confirms that the shear part has axial and transverse scale factors

\[
1-sn_u
\quad\text{along }(1,1,1),
\qquad
1+\frac{sn_u}{2}
\quad\text{across it}.
\]

The second matched field translates the two tetrahedra oppositely along the diagonal. Thus, to first order, \(s_*>0\) gives compression along the selected body diagonal and \(s_*<0\) gives elongation. No stronger geometric classification is needed for Proposition B1.

## 10. Controls, findings, and claim boundaries

### 10.1 Controls

The following controls all behaved as required:

- 195 V0.3-dev tests passed with authenticated Paper 2 input;
- all 24 global negative controls were detected;
- the B1 tamper tests reject altered coverage, bounds, balls, expressions, corner metadata, and hashes;
- false carrier bounds and sign-changing carriers fail;
- raw \(\kappa\) correctly fails at the two endpoints;
- the wrong kernel chart fails;
- the true-carrier positive control certifies.

These controls support implementation integrity but are not used as proof steps.

### 10.2 Findings

| severity | findings |
|---|---|
| Major mathematical or certificate defect | none |
| Minor mathematical or certificate defect | none |
| Documentation defect requiring correction | none |
| Unjustified stability or full-space extremum claim | none |

The submitted V0.3-dev labels B1 as “not independently audited,” which was accurate for the submitted archive. A subsequent audit-status patch may record this report and update that label; no certified mathematical file needs revision.

### 10.3 Boundaries retained

- Strict extrema are not asserted for the \(D_{3d}\) branches.
- No centre-manifold or full-space stability conclusion is drawn.
- Ihrig's theorem is not used to classify the branch as transcritical.
- The \(D_{2h}\) quartic coefficient and stability remain deferred to B2.
- Paper 2 remains unchanged and read-only.
- Nothing has been frozen, published, pushed, or released by this audit.
- The supplied project archives were not modified.

## 11. Final verdict

**PASS — V0.2.1-dev implements both required Track A documentation corrections without changing the audited mathematics, and V0.3-dev preserves Track A and B0. Lemma K and Proposition B1 pass the independent exact-algebra, interval-certificate, physical-curve/corner, frozen-input dependency, transversality, and D3d-reduction audit. Phase B1 may be labelled independently audited; no mathematical, certificate, or documentation correction is required.**
