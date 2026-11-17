# Independent Reviewer Report
## EIT–LJ Cube Bifurcations V0.2-dev — Track A / Theorem A

**Audit date:** 2026-11-14  
**Audited package:** `EIT_LJ_CUBE_BIFURCATIONS_V0.2-dev.zip`  
**Package SHA-256:** `ba835b0dee8cb6d80214b4bd9a61bf2a65d6a4d52376b4e7e0a3dcfd71691e30`  
**Scope:** blind integrity, reproduction, certificate, exact-mathematics, proof-dependency, wording, and claim-boundary audit of Track A.  
**Out of scope:** B1, A3, any modification of Paper 2, and any freezing, publication, or repository action.

## 1. Executive summary

Theorem A is supported by the package’s stated proof chain. The stored Arb/FLINT certificate was regenerated and independently replayed successfully. A further checker, written separately for this audit and using MPFR directed rounding rather than Arb, independently re-proved every recorded dyadic bound. Direct coordinate-based symbolic computations independently confirmed the A0/A1 identities used by the theorem, including the exact on-curve equivalence of the two quartic formulas.

No CRITICAL or MAJOR issue was found. No mathematical correction, new hypothesis, or certificate regeneration is required. Two MINOR documentation corrections remain: the previously identified tetrahedron/inversion wording, and one stale negative-control count.

## 2. Integrity and reproduction

### 2.1 Package integrity

- The uploaded ZIP hash matches the expected value exactly.
- All **39/39** entries in `SHA256SUMS` verify successfully.
- The extracted package contains 40 files when `SHA256SUMS` itself is included.
- The audited copy was kept separate from the reproduction copy. No package file was edited.

### 2.2 Reproduction environment

| Component | Version |
|---|---:|
| Python | 3.12.12 |
| python-flint | 0.9.0 |
| FLINT | 3.6.0 |
| SymPy | 1.14.0 |
| mpmath | 1.3.0 |
| NumPy | 2.2.5 |
| SciPy | 1.16.2 |
| pytest | 9.2.0 |
| gmpy2 | 2.3.2 |
| MPFR | 4.2.2 |

The documented sequence was run in a separate copy:

```text
run_A0.py
run_A1.py
run_B0.py
run_A2.py
pytest
negative_controls.py
```

### 2.3 Reproduction results

| Check | Result |
|---|---|
| A0 representation generation | PASS |
| A1 quartic/sign-table generation | PASS |
| B0 reconnaissance generation | PASS |
| A2 certificate generation and independent Arb checker | PASS |
| Full test suite | **128 passed, 2 skipped** |
| Negative controls | **17/17 detected** |
| Stored certificate replayed directly through `certcheck.check` | PASS, zero failures |
| Regenerated A0 output | Matches stored output |
| Regenerated A1 sign table | Byte-identical |
| Regenerated A2 semantic certificate body | Matches stored body exactly |
| Regenerated semantic SHA-256 | Matches stored hash |
| Regenerated Theorem A graph | Matches stored graph exactly |

The two skips are the documented optional cross-checks against the Paper 2 V1.0 code archive, whose required archive was not supplied for this audit. They are not failed mathematical checks and are not proof dependencies. The A1/B0 JSON differences in the reproduction copy are precisely the omission of those optional Paper 2-code fields. The A2 JSON differences are confined to the excluded `provenance` block, including timing and platform data.

## 3. Lemma M certificate audit

### 3.1 Mathematical certification method

The certificate uses the mean-value enclosure

\[
m'(B)\subseteq m'(c)+(B-c)m''(B),\qquad c=\operatorname{mid}(B),
\]

with exact rational box endpoints and Arb ball arithmetic. The function is analytic on the certified range: the closed form has positive denominator and no residual division by \(r\) at \(r=0\). A successful strict comparison against a recorded dyadic lower bound therefore certifies that bound throughout the box.

### 3.2 Arb/FLINT regeneration and independent replay

| Item | Audited result |
|---|---|
| Main interval | \([0,16/5]\) |
| Boxes | 64 |
| Coverage | Exact, gap-free, non-overlapping |
| Maximum generation depth | 6 |
| Generator precision | 128-bit Arb |
| Independent package-checker precision | 160-bit Arb |
| Boxes accepted by the independent package checker | 64/64 |
| Additional refinement required by that checker | 0 |
| Minimum recorded lower bound | \(161457/262144\approx0.615909576416\) |
| Exact \(m'(0)\) | \(\frac{18}{49}+\frac{12}{49}\log2+\frac{57}{784}\log3\) |
| Semantic SHA-256 | `49dce160b2a17a9f61554200617b9a75b5b02e244e21963b5956317156b6a71e` |
| Failures | 0 |

The checker independently reconstructs \(m'\) and \(m''\), checks the stored expressions and hashes, verifies coverage and positivity, re-evaluates every box, checks the near-zero and \(P_A\) blocks, and recomputes the semantic hash. The semantic hash correctly excludes only the `provenance` block.

The near-zero block was also replayed: \(m''>0\) is confirmed on its eight subboxes of \([0,1/8]\), and the exact value of \(m'(0)\) is positive. This block is consistent with, but is not needed to weaken or replace, the main 64-box certificate.

### 3.3 Independent MPFR directed-rounding certification

A separate implementation was used to avoid relying solely on the package’s two Arb routes. It:

1. derives \(m\) directly from the printed geometric \(T_d\) pair sum;
2. computes \(m'\) and \(m''\) through its own total-derivative implementation;
3. compiles the resulting SymPy expression trees through a separate evaluator;
4. uses exact rational endpoints and 192-bit MPFR directed rounding for arithmetic, exponentials, and logarithms;
5. applies the same mean-value theorem without weakening any recorded lower bound.

| Item | Independent MPFR result |
|---|---|
| Original boxes read from the certificate | 64 |
| Certified subboxes | 128 |
| Additional bisections | 64 |
| Maximum additional depth | 1 |
| All recorded dyadic bounds strictly exceeded | Yes |
| Gap-free coverage of \([0,16/5]\) | Yes |
| Minimum recorded bound independently recovered | \(161457/262144\) |
| Failures | 0 |

The generic expression-tree MPFR evaluator has more interval dependency than the package’s specialised Arb evaluator. One bisection of each original box was therefore used; this is an evaluator-efficiency difference, not a certificate failure. Every half-box strictly exceeded its original recorded bound.

The independent enclosures include

\[
m'(0)\in[0.61697086622652009160412952273540033958597319846054301982114,\;
0.61697086622652009160412952273540033958597319846054301982193],
\]

\[
h_A(16/5)\approx-0.88588385074402018157<-6/7,
\]

and

\[
h_A'(16/5)\approx-0.30982672944564306192<0.
\]

Thus the two signs needed for the uniform \(P_A(q)<16/5\) argument were also confirmed independently of Arb.

### 3.4 Negative and tamper controls

The executed controls correctly reject false claims and defective implementations, including:

- attempted certification on \([7,8]\), where \(m'\) changes sign;
- attempted certification on \([8,9]\), where \(m'<0\);
- the negated claim for \(-m'\);
- the false stronger bound \(m'>31/50\) on \([0,1/10]\);
- dropped mean-value remainder terms;
- inflated lower bounds;
- disabled coverage, claim, or positivity checks;
- removal of transversality from the Theorem A graph;
- introduction of a numerical branch check as a proof dependency.

The positive control on \([1,2]\) certifies as required. All **17/17** scripted mutations were detected.

## 4. Independent exact A0/A1 audit

These checks were implemented without importing the package’s group, pair-sum, or quartic derivation code.

### 4.1 A0 representation and isotropy

Independent enumeration of all 48 signed permutation matrices confirmed:

- \(D(R)e_A=\chi_{A_{2u}}(R)e_A\) for every group element;
- the \(A_{2u}\) projector has rank 1 and fixes \(e_A\);
- the \(O_h\)-fixed subspace has rank 1 and is generated by the breathing field;
- \(e_A\) is orthogonal to translations, rotations, and breathing;
- inversion fixes the cube and sends \(e_A\) to \(-e_A\);
- the stabiliser of \(e_A\) has 24 elements;
- its fixed subspace has rank 2 and is \(\operatorname{span}\{e_{br},e_A\}\).

These facts support the even reduced potential, the one-dimensional \(A_{2u}\) center direction, the breathing-only Lyapunov–Schmidt complement, and the \(T_d\) isotropy conclusion.

### 4.2 Direct coordinate expansion and Hessian identities

A direct two-parameter energy expansion was constructed from the eight cube coordinates in the \(e_A/e_{br}\) directions, independently of `pairsum.py`. It confirmed:

- the symmetry-forced zeros \(V_{ab}=V_{aaa}=V_{abb}=0\);
- the closed forms \(h_A,g_B,g_3,g_4\);
- the difference-form Hessian and quartic coefficients;
- \(He_A=V_{aa}e_A\) and \(He_{br}=V_{bb}e_{br}\);
- translations in the Hessian kernel;
- \(k=h_A/8-1/4\).

In particular, \(V_{bb}=2qW_q(p-q)>0\) on the curve, so the breathing Hessian direction is nondegenerate where the reduced quartic formula divides by \(V_{bb}\).

### 4.3 Exact on-curve quartic equivalence

The direct full-energy expression and the scale-eliminated expression were compared symbolically. After clearing denominators, their difference is exactly divisible by the polynomial obtained by clearing denominators in

\[
h_A(p)-h_A(q)=0.
\]

The multivariate polynomial remainder is zero. Consequently,

\[
c_4=V_{aaaa}-3V_{aab}^2/V_{bb}
   =\frac{16}{3}qW_q\bigl[m(p)-m(q)\bigr]
\]

exactly on \(p=P_A(q)\), not merely to numerical precision. The formulas are not improperly identified off the curve.

## 5. Corollary M and Theorem A

### 5.1 Uniform positivity of \(c_4\)

The range argument is valid. Paper 2 Lemma A gives

\[
0<q<r^*<P_A(q).
\]

The certified signs \(h_A(16/5)<-6/7\) and \(h_A'(16/5)<0\), together with Lemma A’s monotonicity statements, give \(P_A(q)<16/5\). Hence both \(q\) and \(P_A(q)\) lie in the certified interval.

Lemma M and the mean value theorem then yield

\[
m(P_A(q))-m(q)
\ge \frac{161457}{262144}\bigl(P_A(q)-q\bigr)>0.
\]

Since \(qW_q>0\),

\[
c_4(q)\ge \frac{16}{3}\frac{161457}{262144}
 qW_q\bigl(P_A(q)-q\bigr)>0.
\]

This proves the required uniform positivity for every fixed \(q\in(0,r^*)\).

### 5.2 Kernel and transversality

The dependency chain correctly combines:

- the exact \(A_{2u}\) eigenvector and its multiplicity-one isotypic component;
- the six rigid infinitesimal motions;
- Paper 2 Theorem 4′, excluding every additional zero mode on the \(A_{2u}\) curve;
- the exact identity
  \[
  \lambda(\mu)=qW_q\bigl[h_A(P_A(q)+\mu)-h_A(q)\bigr];
  \]
- Paper 2 Lemma A, giving
  \[
  \lambda'(0)=qW_qh_A'(P_A(q))<0.
  \]

Thus the one-dimensional kernel modulo rigid motions and the transversality hypothesis are both justified.

### 5.3 Reduced equation, branch side, and amplitude

Writing

\[
\partial_aV_{red}=aG(a^2,\mu),
\]

the established signs give

\[
G(0,0)=0,\qquad G_\mu(0,0)=\lambda'(0)<0,
\qquad G_s(0,0)=c_4/6>0.
\]

The implicit function theorem therefore gives one nontrivial zero curve \(\mu=\mu_*(s)\), with

\[
\mu_*'(0)=-\frac{c_4}{6\lambda'(0)}>0.
\]

Thus \(s=a^2>0\) forces \(\mu>0\), and inversion of the leading relation gives exactly

\[
a(p)^2=\frac{6qW_q|h_A'(P_A(q))|\mu}{c_4(q)}+O(\mu^2).
\]

The branch side follows analytically from the reduced equation; it does not depend on numerical branch finding.

### 5.4 Slice and equilibrium classification

The normal-slice step is valid locally. For an \(E(3)\)-invariant potential, the gradient at the cube lies in the tangent space to its rigid-motion orbit. Near the cube, transversality of the affine normal slice to that orbit ensures that critical points of the restriction to the slice have no residual full-gradient component. Lyapunov–Schmidt reduction on the slice therefore classifies the stated local equilibria, without silently discarding a transverse gradient.

Equivariance places the complement in

\[
\operatorname{Fix}(T_d)\cap e_A^\perp=\operatorname{span}\{e_{br}\},
\]

and \(w(a,\mu)=O(a^2)\). Inversion exchanges the two nonzero values of \(a\) while preserving the breathing complement, so it exchanges \(x_+\) and \(x_-\). For \(a\ne0\), the exact stabiliser within \(O_h\) is \(T_d\).

### 5.5 Stability claim boundary

For \(0<\mu<\epsilon\),

\[
\partial_a^2V_{red}(0,\mu)=\lambda(\mu)<0,
\]

while on either nontrivial branch,

\[
\partial_a^2V_{red}=2a^2G_s>0
\]

for sufficiently small \(\mu\). The strict maximum at \(a=0\) and strict minima at \(a=\pm a(p)\) are therefore proved **only for the one-dimensional Lyapunov–Schmidt reduced potential**.

The theorem does not claim full-configuration-space local extrema or Morse-index stability, and the audited wording in the theorem itself keeps this boundary explicit. No global \(T_d\)-branch or full-space stability conclusion is inferred in this report.

## 6. Proof dependency graph

The recorded graph contains 35 nodes. Independent traversal confirmed that it is:

- closed from `Theorem A`;
- acyclic;
- free of unused nodes;
- explicit about H0–H4, reduction, and branch side;
- supported by named existing tests for exact/certified leaves;
- restricted to the declared frozen inputs:
  - Paper 2 Lemma A;
  - Paper 2 Theorem 4′;
  - Paper 2 Proposition A.

Numerical checks occur only as corroboration and are not used as proof dependencies. The graph correctly routes \(c_4>0\) through the exact quartic identity, Lemma M, Lemma A, and the certified \(P_A\) range bound. It correctly routes branch side and reduced-potential extremum types through transversality, quartic positivity, and the implicit function theorem.

## 7. Findings

| ID | Severity | Location | Finding | Effect | Required action |
|---|---|---|---|---|---|
| MINOR-01 | MINOR documentation | `NOTES.md` §2 item 7 and §3.9; `README.md` “What V0.2-dev contains” | “Mutually inverted” tetrahedra “of different sizes,” and “the odd tetrahedron is the inversion of the even one,” are not literally correct: spatial inversion preserves radius. | No effect on the certificate, reduced equation, computed stabiliser, or \(T_d\) conclusion. | Replace with inversion-related **vertex-direction sets** and unequal radii; retain that inversion exchanges the two branch configurations. |
| MINOR-02 | MINOR documentation | `NOTES.md` §3.7, negative-controls paragraph | The text says “15 of 15 in total,” while the current suite and `RESEARCH_LOG.md` give 17/17. | Stale documentation count only. | Change to 17/17, optionally clarifying that these comprise 15 earlier/generator/checker controls plus two Theorem A graph controls. |

No CRITICAL or MAJOR findings. No additional MINOR mathematical findings.

### 7.1 Required wording for MINOR-01

A mathematically precise replacement is:

> Two concentric regular tetrahedra of unequal radii on inversion-related vertex-direction sets.

For the proof paragraph in §3.9, the shell argument can be written:

> The two tetrahedra have unequal radii, so a symmetry of a fixed branch configuration cannot exchange the shells. Their vertex-direction sets are inversion-related, and the point group is \(T_d\), in agreement with the exactly computed stabiliser. Spatial inversion exchanges the complete configurations \(x_+\) and \(x_-\); it does not map the unequal-radius shells onto one another within a single fixed configuration.

The shorter `README.md` phrase should be updated consistently.

## 8. Final verdict

\[
\boxed{\textbf{PASS WITH MINOR DOCUMENTATION CORRECTIONS — Theorem A passes the independent mathematical, dependency-graph, Arb/FLINT, and independent MPFR audit. After MINOR-01 and MINOR-02 are corrected, Track A may be labelled independently audited; no mathematical or certificate revision is required.}}
\]

B1 was not started. Paper 2 was not modified. Nothing was frozen, published, pushed, or otherwise released.
