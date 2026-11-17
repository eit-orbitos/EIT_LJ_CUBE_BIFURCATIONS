# Reproducibility — V1.0.0

## Environment used

Python 3 (CPython 3.11+), python-flint 0.9.0 (Arb), SymPy 1.14.0, mpmath 1.3.0, NumPy, SciPy, pytest. LaTeX
(pdfLaTeX, BibTeX, latexmk; natbib/plainnat) for the manuscript; matplotlib for the figures. The release checks of
V1.0.0-rc2 and V1.0.0 were run with Python 3.15.1, pytest 9.2.0 and matplotlib 3.11.2; figure PDFs are byte-identical
only with the recorded matplotlib 3.11.2 (other versions change the bytes, not the content).

    python -m pip install sympy==1.14.0 mpmath==1.3.0 python-flint==0.9.0 numpy scipy pytest matplotlib

Place the frozen Paper 2 archive `EIT_LJ_FULL_VECTOR_STABILITY_V1.0.zip` (SHA-256
`bb70721df7f0aa17edca30d84d1b4aaf980c0a76693be14fa780e4ab8f64762d`) next to the project directory or set
`EIT_LJ_PAPER2_ARCHIVE`; without it three cross-checks against Paper 2's code are skipped.

## Steps

1. Integrity: `sha256sum -c SHA256SUMS` (from the project root).
2. Tests: `python -m pytest -q` (several files are long; they can be run file by file).
3. Certificates: `python scripts/run_A2.py` (Lemma M), `python scripts/run_B1_erratum.py` (historical Lemma K replay with
   the corrected checker, corrected rebuild, Taylor-free cross-check), `python scripts/run_B2_3.py` (Lemma Q). Do **not**
   run `scripts/run_B1.py`: it would overwrite the audited historical certificate (NOTES §10.2).
4. Proof records: `scripts/run_A0.py`, `run_A1.py`, `run_B0.py`, `run_B2.py`, `run_B2_2.py`, `run_B2_4.py`,
   `run_B2_5.py`. Regenerated records embed the project version and status; compare semantically (see below).
5. Negative controls: `scripts/negative_controls*.py` (code mutations the tests must detect).
6. Preservation against V0.4-dev.6 and V1.0.0-rc2:
   `python scripts/check_preservation_V1_0_0.py <V0.4-dev.6 zip> --rc2=<V1.0.0-rc2 zip>` and
   `python scripts/preservation_controls_V1_0_0.py <V0.4-dev.6 zip> --rc2=<V1.0.0-rc2 zip>`.
7. Release text: `python scripts/check_release_text.py` (current surfaces, authorship, declarations, bibliography) and
   `python scripts/scan_text_v1.py` (classified whole-tree scan for stale and claim terms).
8. Figures: `python paper/figures/make_figures.py`; appendix formulas: `python paper/tools/check_appendix_closed_forms.py`.
9. Manuscript: from `paper/` (or the root of the source ZIP), `latexmk -pdf manuscript.tex`.

## Semantic comparison of regenerated records

Records written by the `run_*.py` scripts contain the package version and status (`version`, `project_version`,
`status`) and provenance (timestamps, durations, platform). Under V1.0.0 these differ from the stored V0.4-dev.6
records; the stored records are kept byte-identical (they are the audited artefacts). A regeneration is accepted when
the records agree after removing only those keys. Certificate semantic hashes exclude provenance by construction.

## Expected certificate hashes

| certificate | semantic SHA-256 |
|---|---|
| Lemma M (`data/A2_lemma_M_certificate.json`) | `49dce160b2a17a9f61554200617b9a75b5b02e244e21963b5956317156b6a71e` |
| Lemma K, historical (`data/B1_kappa_certificate.json`) | `616817fcc70e0fab7f106404e5e5332b17b9c4480bd440355f1ac5257a8518c6` |
| Lemma K, corrected rebuild (corroboration only) | `b2f8e6dcd1c5073635babea2f7a6079b7ede03acbbc4f33ac3cb20f64d21d505` |
| Lemma Q (`data/B2_c4hat_certificate.json`) | `f7bc244ecac4b89ce003a38ff52047d6cbe80f63a97236049f15f5e0da5c17d2` |

The QA results for this release are in `docs/QA_RESULTS_V1.0.0.md` and `RELEASE_NOTES_V1.0.0.md`.

Test-suite environment variables: `EIT_LJ_PAPER2_ARCHIVE` (Paper 2 V1.0 archive), `EIT_LJ_DEV6_ARCHIVE` (V0.4-dev.6
archive) and `EIT_LJ_RC2_ARCHIVE` (V1.0.0-rc2 archive); the last two are used only by the preservation test in
`tests/test_release_v1.py`. With all three set, no test is skipped.
