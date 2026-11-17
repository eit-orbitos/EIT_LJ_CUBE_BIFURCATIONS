# Blind Independent Reviewer Report
## Paper 3 — Phase B2.3 / Lemma Q only

**Audited package:** `EIT_LJ_CUBE_BIFURCATIONS_V0.4-dev.5(2).zip`  
**Review type:** fresh blind mathematical, certificate, implementation, reproduction, and adversarial audit  
**Scope:** Phase B2.3 / Lemma Q only; B2.4 checked solely for dependency integrity  
**Excluded:** B2.5, any new branch classification, any full-space stability or centre-manifold-index claim  
**Formal verdict:** **PASS**

## 1. Final determinations

| Required determination | Finding |
|---|---|
| 1. Is Lemma Q independently re-certified? | **Yes.** The closed-curve certificate was independently reconstructed and verified with separate directed-rounding arithmetic. |
| 2. Does \(\widehat c_4>0\) hold on the whole closed physical curve? | **Yes.** All 222 curve boxes, the \(q=0\) endpoint, and the corner \(p=q=q_c\) were independently certified. |
| 3. Does \(c_4(q)>0\) follow for every \(0<q<q_c\)? | **Yes.** Here \(c_4=qW_q(P_T(q)-q)\widehat c_4\), and all three factors are strictly positive on the open physical curve. |
| 4. Are both endpoint treatments valid? | **Yes.** The \(q=0\) formula is the correct direct limit formula; at the corner every divided difference is replaced by \(f'(q_c)\), with no division by \(p-q\). |
| 5. Are the imported B1 curve boxes valid inputs? | **Yes.** The semantic pin is intact, all 222 balls passed independent strict parametric Newton inclusion, and their physical-branch and corner selection is correct. |
| 6. Is any mathematical, certificate, code, or wording correction required? | **No.** No CRITICAL, MAJOR, or MINOR defect was found. |

Accordingly, **Lemma Q may be recorded as independently audited and re-certified**.

## 2. Integrity and dependency boundary

### 2.1 Supplied archives

- Paper 3 archive SHA-256:  
  `77267d56f7a271b81b6cc91166f6750c71e1fc4f214c337f016ecf75b4563949`
- Paper 2 archive SHA-256:  
  `bb70721df7f0aa17edca30d84d1b4aaf980c0a76693be14fa780e4ab8f64762d`

The Paper 3 archive is byte-identical to the previously authenticated dev.5 archive. Its internal manifest passed **113/113** file checks. Paper 2 was used read-only.

### 2.2 B2.3 and imported B1 certificates

- `data/B2_c4hat_certificate.json` SHA-256:  
  `9f6b31404ce9e03372b321567f53cb95254e2955c332e7eea7c381ca0f4d4209`
- Recomputed B2.3 semantic SHA-256:  
  `f7bc244ecac4b89ce003a38ff52047d6cbe80f63a97236049f15f5e0da5c17d2`
- Recomputed B2.3 expression/formula SHA-256:  
  `4aff8215a4e19870b5945b486d01df8fda2dbbe1313f2789f21e5801d4ac8860`
- Imported `data/B1_kappa_certificate.json` SHA-256:  
  `dee3ad024af69f76620de35f3d0aa8be06a9f4f099ca0ffb001c4914178f87ab`
- Recomputed imported B1 semantic SHA-256:  
  `616817fcc70e0fab7f106404e5e5332b17b9c4480bd440355f1ac5257a8518c6`

Each recomputed value matches its recorded value. The B2.3 boxes use the B1 \(q\)-boxes and \(\delta\)-balls without alteration.

### 2.3 Earlier tracks and B2.4 dependency

The dev.5 identity checker passed against the authenticated dev.4 archive. Earlier mathematical tracks and audit records are preserved under its permitted-change rules.

The B2.4 dependency graph contains Lemma Q as the certified input `LQ_lemma_Q`, sourced from the same B2.3 certificate and semantic hash. It is consumed by the B2.4 IFT branch step. No B2.4 conclusion was re-audited here, and no B2.5 work was performed.

## 3. Independent mathematical reconstruction

The package’s quartic formulas were not assumed. The calculation was restarted from the raw 24-dimensional pair energy

\[
V(x)=\sum_{1\le i<j\le8}\psi\!\left(\lVert x_i-x_j\rVert^2\right),
\]

at the unit-edge cube, using independently constructed displacement fields

\[
\widehat u_1=-W_1/4,\qquad \widehat v_1=-(\sqrt2/4)U_1,
\]
\[
\widehat A=E_{\rm br}/\sqrt{24},\qquad
\widehat E=E_{\rm tet,x}/\sqrt{48}.
\]

Raw composed pair-distance expansions gave the five quartic channels, the three cubic channels paired with each back-reaction direction, and the two Hessian denominators. The calculation also reconstructed the three entries of the Hessian matrix \(M\) used in the curve equation.

### 3.1 Back-reaction support and Lyapunov–Schmidt coefficient

For each channel \(uu,uv,vv\), the full raw 24-vector \(b_{cc'}\) satisfies exactly

\[
b_{cc'}=b_{A,cc'}\widehat A+b_{E,cc'}\widehat E.
\]

Thus the back-reaction has no omitted component. Independent full-Hessian contractions prove

\[
H\widehat A=h_A\widehat A,\qquad H\widehat E=h_E\widehat E.
\]

On the critical axis, solving the transverse stationary equations gives

\[
w(s)=-\frac12H_\perp^{-1}b\,s^2+O(s^3),
\qquad b=D^3V[e_1,e_1,\cdot].
\]

Substitution into the reduced potential therefore yields, independently,

\[
c_4=D^4V[e_1^4]-3\langle b,H_\perp^{-1}b\rangle
=Q-3\frac{b_A^2}{h_A}-3\frac{b_E^2}{h_E}.
\]

The factor \(3\) is the contraction with \(w_2=-H_\perp^{-1}b/2\), not an externally imposed convention.

### 3.2 Exact difference-form factorization

For

\[
\phi(r)=A r^{-p}-r^{-q},\qquad
A=\frac{qW_q}{pW_p},\qquad
W_r=1+2^{-r/2}+\frac{3^{-r/2}}3,
\]

the raw derivatives of \(\psi(\sigma)=\phi(\sqrt\sigma)\) were substituted directly. Every one of the 16 reconstructed linear forms has the exact structure

\[
L=A F(p)-F(q)
=qW_q\bigl(g(p)-g(q)\bigr),
\qquad g(r)=\frac{F(r)}{rW_r}.
\]

Consequently, with \(c=qW_q\) and \(d=p-q\),

\[
Q=cd\,\widehat Q,\qquad b_X=cd\,\widehat b_X,\qquad
h_X=cd\,\widehat h_X,
\]

and hence

\[
\boxed{c_4=qW_q(p-q)\widehat c_4}.
\]

The independently derived \(g\)-functions match all 16 stored expressions symbolically. In particular,

\[
g_{h_A}(r)=2(r+1),\qquad \widehat h_A=2.
\]

### 3.3 Projective kernel and normalized carrier

For the divided-difference matrix \(\widehat M\), direct substitution gives

\[
\widehat M\binom{1}{\rho}
=\binom{\det\widehat M/\widehat M_{22}}
{\widehat M_{12}+\rho\widehat M_{22}}.
\]

On \(\det\widehat M=0\), the projective kernel is therefore

\[
\boxed{\rho=-\widehat M_{12}/\widehat M_{22}},
\qquad n\propto(1,\rho).
\]

The unit vector is \((1,\rho)/\sqrt{1+\rho^2}\). Quartic homogeneity, quadratic homogeneity of \(b_A,b_E\), and \(\widehat h_A=2\) give

\[
\boxed{
\widehat c_4=
\frac{\widehat Q(1,\rho)-\frac32\widehat b_A(1,\rho)^2
-3\widehat b_E(1,\rho)^2/\widehat h_E}
{(1+\rho^2)^2}}.
\]

This independently establishes both the normalization and the relative factors in the two back-reaction terms.

## 4. Independent curve verification

The imported B1 partition is gap-free from \(0\) to \(101/50\), with 222 ordered nonempty boxes. For every box, a separately implemented strict parametric interval Newton operator verified a unique zero of

\[
\widetilde D(q,\delta)=\det\widehat M(q+\delta,q)
\]

inside the stored \(\delta\)-ball, uniformly for \(q\) in the box.

The independent operator used a mean-value form in \(q\), a nonzero \(\partial_\delta\widetilde D\) enclosure, and strict interior inclusion of the Newton image. No project curve routine was called.

Branch selection is valid:

- every noncorner ball has \(\delta>0\);
- every noncorner \(q\)-box lies below the certified \(q_c\) enclosure;
- Paper 2 Lemma T3 therefore identifies each such zero with the physical \(p=P_T(q)>q\);
- only the last box is marked as the corner box, and it contains both \(q_c\) and \(\delta=0\);
- the short mirror arc in that final box is harmless because positivity is proved for the entire ball.

The independent Newton certification confirmed **222/222** boxes. An altered ball on box 30 was rejected.

## 5. Separate directed-rounding carrier certification

### 5.1 Independent numerical method

A new interval implementation used 320-bit MPFR directed rounding. It did not import project modules, call the Arb generator/checker, or reuse their Taylor routines.

For far boxes it evaluated the direct quotient with outward rounding. Near the diagonal it used an independently written forward Taylor–integral form. With \(c_j=f^{(j)}/j!\), \(d=\delta\), and \(N=16\),

\[
\widehat f(q,d)=
\sum_{k=0}^{N-1}c_{k+1}(q)d^k+c_{N+1}(\xi)d^N,
\qquad \xi\in\operatorname{hull}(q,q+d).
\]

The slope enclosures required by Newton certification were obtained from the corresponding integrated \(f''\) identities, including their complete directed-rounding remainder terms. This route remains valid when the corner \(\delta\)-ball crosses zero and performs no division by \(\delta\) in that regime.

### 5.2 Results on all boxes

- Curve Newton inclusions: **222/222 passed**.
- Strict \(\widehat c_4>0\) enclosures: **222/222 passed**.
- Every stored per-box lower bound: **222/222 independently confirmed**.
- \(\widehat h_E>0\): **222/222 passed**.
- \(\widehat M_{22}>0\): **222/222 passed**.
- Required q-splits for the independent certification: **none**.

The smallest independent lower endpoint occurred on box 0:

\[
\widehat c_4\in
[3.6713702580975280727,\;3.9349532059665934984].
\]

This strictly confirms the claimed global bound

\[
\boxed{\widehat c_4\ge\frac{955723}{262144}
=3.645793914794921875>0}.
\]

The independent box enclosures also gave \(\widehat h_E\)-lower endpoints no smaller than approximately \(1.8888503762\) and \(\widehat M_{22}\)-lower endpoints no smaller than approximately \(1.3807858017\). These are enclosure minima, not claimed sharp functional minima.

## 6. Independent endpoint certification

### 6.1 Endpoint \(q=0\)

The direct formula

\[
\widehat f=\frac{f(p_0)-f(0)}{p_0},
\qquad p_0=P_T(0),
\]

was evaluated using exact values at \(r=0\) and the preserved B1 \(p_0\) enclosure. Independent directed-rounding evaluation of \(\det(M(p)-M(0))\) at its two endpoints gave

\[
8.6450070233\times10^{-37}>0,
\qquad
-1.3625061768\times10^{-36}<0.
\]

The resulting certified enclosures are

\[
\widehat c_4(0)\in
[3.7993380378668858157102270261,\;
 3.7993380378668858157102270293],
\]
\[
\widehat h_E\in[1.9991175681777892838805676414,\;
 1.9991175681777892838805676430],
\]
\[
\widehat M_{22}\in[1.5133403767422389187397667264,\;
 1.5133403767422389187397667280].
\]

All are strictly positive. Omitting the exact \(f(0)\) term produces a disjoint, rejected enclosure.

### 6.2 Corner \(p=q=q_c\)

At the diagonal, every divided difference was replaced by the derivative \(f'(q_c)\). Independent evaluation of \(\det M'(r)\) at the endpoints of the preserved \(q_c\) enclosure gave

\[
7.8862913667\times10^{-42}>0,
\qquad
-1.3662039822\times10^{-41}<0.
\]

The corner carrier is enclosed by

\[
\widehat c_4(q_c)\in
[4.3770354906131219361130218836,\;
 4.3770354906131219361130218900],
\]

with

\[
\widehat h_E\in[1.9983173671120638186095016357,\;
 1.9983173671120638186095016374],
\]
\[
\widehat M_{22}\in[1.4555084712125296078064849097,\;
 1.4555084712125296078064849113].
\]

No corner expression divides by \(p-q\). Using values \(f(q_c)\) instead of derivatives gives the disjoint enclosure approximately \([7.2836101459511656691,7.2836101459511656691]\), and is rejected.

### 6.3 Raw coefficient at the endpoints

The raw identity contains an explicit factor \(q\) at \(q=0\) and an explicit factor \(p-q\) at the corner. Therefore raw \(c_4\) is exactly zero at both endpoints. A claim of raw \(c_4>0\) at either endpoint is false; the normalized carrier is the correct closed-curve object.

## 7. Open-curve corollary

For every \(0<q<q_c\),

\[
q>0,\qquad W_q>1,\qquad P_T(q)-q>0,
\]

where the last two properties are the recorded equilibrium/Paper 2 inputs. Combining them with the independently certified normalized positivity gives

\[
\boxed{c_4(q)=qW_q(P_T(q)-q)\widehat c_4(q)>0}.
\]

The endpoint vanishing of raw \(c_4\) does not contradict this open-curve conclusion.

## 8. Reproduction, tests, and adversarial controls

### 8.1 Clean reproduction

A separate clean extraction regenerated the B2.3 certificate and check report successfully:

- regenerated semantic hash equals the stored semantic hash;
- all 222 regenerated boxes match semantically;
- both regenerated endpoint records match semantically;
- supplied independent checker: passed with no failures;
- supplied method controls: **15/15** behaved as required;
- targeted tests: **93 passed, 0 failed**.

### 8.2 Independent adversarial controls

| Corruption | Independent result |
|---|---|
| Wrong/deleted \(E_g\) back-reaction | Rejected; both endpoint enclosures exclude the certified values. |
| Back-reaction factor \(3\to2\) | Rejected; both endpoint enclosures exclude the certified values. |
| Wrong kernel sign | Rejected; both endpoint enclosures exclude the certified values. |
| Corner values instead of derivatives | Rejected; disjoint corner enclosure. |
| Inflated bound \(\widehat c_4>19/5\) | Rejected at \(q=0\), where \(3.7993380379<3.8\). |
| Raw \(c_4>0\) at \(q=0\) | Rejected exactly because \(q=0\). |
| Raw \(c_4>0\) at the corner | Rejected exactly because \(p-q=0\). |
| Altered imported B1 curve ball | Rejected by independent Newton inclusion on box 30. |
| \(q=0\) formula without \(f(0)\) | Rejected; disjoint endpoint enclosure. |

All nine independent adversarial controls passed. The supplied B2.3 code-mutation suite additionally detected **24/24** mutations, including generator, checker, endpoint, remainder, provenance, curve-ball, and raw-endpoint corruptions. Its long execution was split into batches; every unmutated baseline passed and every mutation was detected.

The B2.2 numerical scan remains corroboration only and was not used as a proof input.

## 9. Findings by severity

### CRITICAL

None.

### MAJOR

None.

### MINOR

None.

### INFORMATIONAL

1. Lemma Q is computer-assisted. Its curve selection continues to use the preserved Paper 2 Lemmas T2/T3 and the supplementary \(P_T(0)\) enclosure as declared inputs.
2. The final corner box also covers a short nonphysical mirror arc; this enlarges but does not weaken the certified domain.
3. B2.4 was examined only to confirm that its dependency record consumes the preserved Lemma Q certificate. Its branch proposition was not reassessed.
4. No numerical scan, approximate root finder, or full-space stability assertion is needed for Lemma Q.

## 10. Conclusion

The independent raw-coordinate derivation, separate MPFR interval certification, endpoint calculations, clean reproduction, and adversarial controls all agree. Lemma Q is valid as stated:

\[
\widehat c_4>0
\]

on the entire closed physical \(T_{2g}\) transition curve, including \(q=0\) and \(p=q=q_c\), and

\[
c_4(q)>0\qquad(0<q<q_c).
\]

**Verdict: PASS.** Lemma Q is independently re-certified. No correction is required, and the B2.3 phase may be marked independently audited. Nothing was frozen, published, pushed, released, or modified in the supplied project archives.

## Appendix A. Independent evidence digests

- Independent raw derivation result SHA-256:  
  `094a0a843053f0d9a0dd411a0bc89c3f0fc44c68a2499cfc0673dd6593ced4b8`
- Independent interval result SHA-256:  
  `25787fb090de6fc7f9ceb6af385299bbe23e53f7deb88f0e03560f983eca2a81`
- Independent adversarial result SHA-256:  
  `df5ee2fa11d23e19da669dfc307532c1a916af221fdb6ca7280f7143b3e17718`

These digests identify the independent scratch evidence used for this review; the supplied project files were not edited.
