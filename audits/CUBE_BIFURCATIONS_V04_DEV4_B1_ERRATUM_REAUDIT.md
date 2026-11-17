# Targeted Independent Re-audit Report
## Paper 3 V0.4-dev.4 — B1 `arb_series / ctx.cap` implementation erratum

**Audit date:** 2026-11-14  
**Patched package:** `EIT_LJ_CUBE_BIFURCATIONS_V0.4-dev.4.zip`  
**Pre-patch package:** `EIT_LJ_CUBE_BIFURCATIONS_V0.4-dev.3 (1).zip`  
**Scope:** erratum E-B1 only  
**Formal verdict:** **PASS**

## 1. Scope and conclusion

This was a targeted independent re-audit of the B1 Taylor-series implementation erratum, not a full Paper 3 audit. The supplied patch report and its recorded claims were treated as untrusted. The audit independently reproduced the defect, examined and tested the patch, replayed the historical certificate, generated a fresh corrected certificate, ran the non-Taylor B2.3 route with affected imports blocked, and checked the complete dev.3-to-dev.4 diff.

The original defect is real and produced unsound enclosures. V0.4-dev.4 corrects it properly. The stored historical certificate remains mathematically valid: its data pass the corrected checker, its curve balls pass a separate non-Taylor checker, and a fresh corrected build proves the same Lemma K claim. Lemma K and Proposition B1 are unchanged. No further full B1 audit is required, and the erratum can be marked **CLOSED**.

No project files were modified. B2.4 and B2.5 were not started.

## 2. Explicit answers to the required questions

| Question | Answer |
|---|---|
| 1. Was the original `ctx.cap` bug real? | **Yes.** It truncated all seven B1 functions and replaced genuinely nonzero coefficients with exact zeros, producing enclosures that excluded high-precision reference values. |
| 2. Does V0.4-dev.4 fix it correctly? | **Yes.** Both routines raise capacity sufficiently, restore the old context on normal and exceptional exits, retain high-order coefficients, and reject nonzero truncation rather than padding it. |
| 3. Is the historical B1 certificate still valid? | **Yes.** The corrected checker accepts all its curve inclusions and carrier bounds; the separate non-Taylor route also accepts all 222 curve balls. |
| 4. Does the corrected checker accept all 222 historical boxes? | **Yes: 222/222 curve inclusions and 222/222 carrier bounds**, with both endpoints accepted and no failures. |
| 5. Does the fresh corrected rebuild prove the same Lemma K claim? | **Yes.** It has 222 boxes, the same mathematical claim and expressions, the same endpoints, and the same minimum bound \(1311719/536870912\). |
| 6. Does the B2.3 non-Taylor route independently verify all 222 B1 curve balls? | **Yes: 222/222 PASS**, with `b1_cert` and `b1_check` imports blocked and no `arb_series` use. |
| 7. Is Lemma K changed? | **No.** Its statement, formulas, frozen inputs, endpoint records, and certified lower bound are unchanged. |
| 8. Is Proposition B1 changed? | **No.** Its statement and mathematical dependencies are unchanged. |
| 9. Is any further full B1 audit required? | **No.** The previous independent mathematical audit plus this targeted implementation and certificate re-audit are sufficient. |
| 10. Can the erratum be marked CLOSED after this audit? | **Yes.** |

## 3. Archive authentication and integrity

The recomputed archive hashes exactly match the required values:

| Archive | SHA-256 |
|---|---|
| V0.4-dev.3 | `cf331557f9cf6fd074920368a69268c331e4c84d1f3b64fd89b421a3b45d5c81` |
| V0.4-dev.4 | `8ae923beec9c095ec546c1a69e56a632698bfd8e4828a1165a8cbc1199cc06c7` |

Internal manifest verification passed:

- V0.4-dev.3: **88/88** files.
- V0.4-dev.4: **101/101** files.

The supplied original independent B1 report also matches its established SHA-256:

`82bd4f21630a20481113702a9f49dddfa6327f2baf3c07a131af259c1baa65e5`.

## 4. Independent reproduction of the original defect

### 4.1 Library behaviour and requested lengths

The audit used python-flint 0.9.0 with FLINT 3.6.0. A direct minimal exponential-series test gave:

- `ctx.cap = 10`, `arb_series(..., prec=18)`: **10 coefficients returned**;
- `ctx.cap = 18`, the same request: **18 coefficients returned**.

Thus `prec=` does not override `ctx.cap`.

The old generator uses `N_TAYLOR = 16` and requests series lengths 18 and 19 in the near regime. The old checker uses `N_CHECK = 20` and requests lengths 22 and 23. All exceed the default capacity 10.

At `r = 1`, every old raw seven-function series requested at length 18 returned only 10 coefficients. The old `_taylor` then returned lists of length 18 whose entries at indices 10 through 17 were all exact zero balls.

### 4.2 The discarded coefficients are genuinely nonzero

Independent 90-digit mpmath Taylor references, computed from separately written closed forms rather than package expression strings, confirmed nonzero high-order coefficients for **all seven functions**. Examples at \(r=1\) are

\[
c_{10}(M_{22})=5.2265226189004913383\ldots\times10^{-9},
\]

\[
c_{10}(g_{uvv})=-2.9224787277062881959\ldots\times10^{-9},
\]

and

\[
c_{17}(M_{22})=3.2167556146519595034\ldots\times10^{-15}.
\]

The zero padding was therefore mathematically false, not harmless trimming of exact trailing zeros.

### 4.3 Unsound old enclosures at \((q,\delta)=(1.9,0.9)\)

The audit independently evaluated the divided-difference reference

\[
\widehat f=\frac{f(q+\delta)-f(q)}{\delta}
\]

at 90-digit precision. Both the old generator and old checker excluded the reference value for **all seven functions**.

For example,

\[
\widehat M_{22}=1.552338787808308618848493481989\ldots,
\]

whereas the old enclosure was

\[
[1.5523387891162772848549465846539162\pm1.55\times10^{-35}],
\]

which does not contain the reference. Similarly,

\[
\widehat g_{uvv}=-2.031171622867651708396495403158\ldots,
\]

while the old generator returned

\[
[-2.0311716256607021534259798798889186\pm7.78\times10^{-36}],
\]

again excluding the reference. This independently reproduces at least one—and in fact fourteen, counting both routines and all seven channels—unsound enclosures.

The independent diagnostic record has SHA-256:

`7c7945f16b67a5398ab105f203d53fa77425d2eca58273b9c0006774128e5666`.

## 5. Audit of the patch

### 5.1 Capacity handling and context restoration

The corrected `b1_cert._taylor` uses `_series_capacity(n)`, and corrected `b1_check.Model.taylor` uses `SeriesLength(n)`. Both ensure `ctx.cap >= n` during evaluation and restore the previous value afterward.

Independent probes established:

- starting capacities **7, 10, and 40** were restored after each routine;
- capacity 10 was restored after deliberately injected exceptions in both `_funcs` and `Model.values`;
- corrected generator output at length 18 and checker output at length 23 contained the requested coefficients;
- every corrected \(c_{10}\) enclosure contained the independent high-precision reference; and
- both corrected divided-difference routines contained every reference value at the diagnostic point.

### 5.2 Truncation cannot silently become zero

The patch checks that the claimed capacity is actually in force. If a series is shorter than requested, it recomputes a longer series and permits padding only when every missing coefficient is exactly zero.

Independent mutation probes verified:

- simulated unraised capacity causes `SeriesTruncationError` in the generator;
- simulated unraised capacity causes `TruncatedSeries` in the checker;
- a genuine quadratic polynomial is still padded with exact trailing zeros correctly; and
- a short series with nonzero missing coefficients is rejected.

### 5.3 Regression tests genuinely reject the old behaviour

Running the new erratum test module against the actual dev.3 implementation produced:

**8 failed, 7 passed.**

The failures included high-order coefficient correctness, the Cauchy-integral reference, corrected diagnostic behaviour, near-grid containment, and truncation detection.

An additional independently created scratch mutant restored only the old `_taylor` and `Model.taylor` bodies while leaving the new helper code in place. The same new tests again produced:

**8 failed, 7 passed.**

On the corrected implementation, the targeted erratum and B1 certificate tests produced:

**43 passed.**

The patch therefore has effective regression coverage rather than tests that merely record the repaired output.

## 6. Historical B1 certificate

The historical file remained byte-identical, with file SHA-256

`dee3ad024af69f76620de35f3d0aa8be06a9f4f099ca0ffb001c4914178f87ab`

and semantic SHA-256

`616817fcc70e0fab7f106404e5e5332b17b9c4480bd440355f1ac5257a8518c6`.

The corrected checker independently returned:

- **222/222** curve/Newton inclusions confirmed;
- **222/222** carrier bounds confirmed;
- both endpoints accepted;
- corner identification and sign-change checks accepted;
- no checker refinement and no failures; and
- minimum lower bound

\[
\boxed{\frac{1311719}{536870912}}.
\]

The pre-patch generator was also run in a separate scratch tree. It regenerated the same historical semantic hash, `616817fc…c6`. Its file-level bytes differed only in non-semantic provenance data; the mathematical certificate body was reproduced.

**Conclusion:** the old implementation was unsound, but the particular stored historical certificate is nevertheless valid. The flaw did not invalidate the mathematical claim carried by those stored boxes and bounds.

## 7. Fresh corrected rebuild

A fresh certificate was generated with the corrected implementation and checked with the corrected checker. Its semantic SHA-256 is

`b2f8e6dcd1c5073635babea2f7a6079b7ede03acbbc4f33ac3cb20f64d21d505`,

exactly matching the patch's reported value.

Independent comparison with the historical certificate established:

| Property | Result |
|---|---|
| Boxes | 222, maximum depth 2 |
| Mathematical claim and statement | Identical |
| Expressions and expression hash | Identical |
| Frozen inputs and method description | Identical |
| Exact rational \(q\)-partition | Identical |
| Endpoint records | Identical |
| Minimum certified lower bound | \(1311719/536870912\), identical |
| Corrected checker | 222/222 curve inclusions and 222/222 carrier bounds |
| Changed boxes | Exactly 52, all near-diagonal |
| Unchanged boxes | All 170 far boxes |
| Changed fields | Only `delta_lo`, `delta_hi`, and `kappa_hat_lower_bound` |

All 52 changed near-diagonal bounds passed the corrected checker. Their lower bounds are higher than the historical ones; none is lower. The different semantic hash is therefore expected and reflects corrected, tighter near-diagonal enclosures, not a change to Lemma K.

## 8. Independent non-Taylor B2.3 route

Static inspection of `b2_check.py` found no project-module imports, no `arb_series`, and no call to either affected Taylor routine. Its divided differences use

\[
\widehat f(q,\delta)=\int_0^1 f'(q+t\delta)\,dt,
\]

with composite midpoint rules, exact derivative remainders, and centred box forms. Curve certification uses its own strict parametric interval-Newton inclusion.

The audit ran this checker in a fresh interpreter with import hooks that raised on either `cube_bif.b1_cert` or `cube_bif.b1_check`. Results:

- **222/222 imported B1 curve balls re-verified**;
- 222 B2.3 boxes and carriers checked;
- no failures;
- maximum curve quadrature subdivision 32;
- no \(q\)-splitting required;
- no blocked import was attempted, and neither B1 module appeared in the loaded modules; and
- B2.3 semantic hash reproduced as `f7bc244ecac4b89ce003a38ff52047d6cbe80f63a97236049f15f5e0da5c17d2`.

This supplies an independent certificate route that shares neither the defective implementation nor Taylor-series arithmetic.

## 9. Diff integrity and unchanged mathematics

An independent tree comparison found 79 identical files, 10 permitted changed files, 13 permitted added files, and no removed files. Changes are restricted to:

- the two affected Taylor implementations;
- erratum and certificate regression tests;
- documentation and version/status metadata;
- erratum diagnostics, rebuild artifacts, and controls; and
- the integrity manifest.

The following are byte-identical between dev.3 and dev.4:

- Track A mathematics, certificates, dependency graph, and original audit report;
- B0 mathematics and data;
- B1 exact formulas and the original independent B1 audit report;
- the historical B1 certificate and semantic hash;
- B2.0, B2.1, and B2.2 mathematics and data; and
- B2.3 mathematics, checker, and certificate.

`NOTES.md` §§0–9 are byte-identical between the two versions, with SHA-256

`6e6f62741552614ce83b4e84352d7119e2dafa609a858b394477a19d365a8472`.

Consequently, Lemma K and Proposition B1 are textually and mathematically unchanged. No unrelated mathematical change was found.

The independent diff-audit record has SHA-256:

`750c1ba000e6391600d996936a48d435ee8b1b321fe2dabd687621e52e82b042`.

## 10. Full verification and controls

The following were run independently rather than accepted from the patch report:

- Complete test suite: **343 passed, 2 skipped**.
- The two skips were solely Paper 2 archive lookups; supplying the authenticated frozen archive explicitly gave **2 passed**.
- Targeted erratum/certificate tests: **43 passed**.
- New erratum tests on old code: **8 failed, 7 passed**, as required for regression sensitivity.
- Independent old-truncation mutant: **8 failed, 7 passed**.
- Supplied erratum controls: **12/12 required mutations detected**, and **13/13 total outcomes as required**, including the documented certificate-test non-detection control.
- Standard negative controls: **34/34 detected**.
- Mechanical dev.3/dev.4 identity check: **PASS**.
- Identity-check adversarial controls: **41/41 forbidden modifications rejected**.
- Historical replay and corrected rebuild: all required checks passed.
- Non-Taylor B2.3 route: **222/222 PASS**.

## 11. Findings by severity

### CRITICAL

None.

### MAJOR

None.

### MINOR

None.

### INFORMATIONAL

1. The pre-patch implementation defect was substantive and could create unsound enclosures. It is corrected in dev.4 and covered by effective regressions.
2. The historical certificate's validity is established by its stored data passing corrected and non-Taylor checks; validity does not rely on the defective old evaluator.
3. The fresh corrected certificate has a different semantic hash because 52 near-diagonal records are tighter. The Lemma K statement and minimum bound are unchanged.
4. The full suite's two initial skips were environmental Paper 2 lookups, not missing mathematical checks; both passed when the frozen archive was supplied explicitly.

## 12. Final determination

The original `ctx.cap` bug was real, the dev.4 correction is sound, the historical certificate remains valid, the corrected rebuild proves the same Lemma K claim, and the independent non-Taylor route verifies all 222 historical curve balls. No further full B1 re-audit is necessary. Lemma K and Proposition B1 remain unchanged. The erratum may be marked **CLOSED**.

# Final verdict: PASS
