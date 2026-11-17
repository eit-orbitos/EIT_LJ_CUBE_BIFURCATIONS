# V1.0.0-rc1 QA results (author-side verification; not the final blind release audit)

Executed on a frozen snapshot of the release-candidate code (snapshot SHA-256 `1b106b005112877ee57836f9918997f81d219a3c7a474f9903ba5de3eb57e89a`): `src/`, `data/`, `scripts/` (pre-existing) and `tests/` (except `tests/test_docs.py`) are byte-identical to this release candidate. Environment: Python 3.15.1, python-flint 0.9.0, sympy 1.14.0, mpmath 1.3.0, pytest 9.2.0. Paper 2 archive supplied through `EIT_LJ_PAPER2_ARCHIVE` (SHA-256 `bb70721d…762d`), so no test is skipped for lack of it.

Runs were split into pieces of < 110 s (sandbox limit) using the suites' own test ids, mutation lists and per-mutation predicates. No project file was edited during QA.

## 1. Test suite

| scope | collected | passed | failed | errors | skipped |
|---|---|---|---|---|---|
| all test files except `test_docs.py` / `test_release_rc1.py` (snapshot) | 459 | 459 | 0 | 0 | 0 |
| `tests/test_docs.py` + `tests/test_release_rc1.py` (final tree, `EIT_LJ_DEV6_ARCHIVE` set) | 16 | 16 | 0 | 0 | 0 |
| **total** | **475** | **475** | **0** | **0** | **0** |

Each collected test id was executed exactly once (54 JUnit pieces). Interruptions (rerun, not counted as results): pytest_test_B1_certificate__006: outer command timeout terminated unfinished attempt; no completed node reported in buffered log; rerun required; pytest_test_B1_certificate__007: outer command timeout terminated unfinished attempt; no completed node reported in buffered log; rerun required; pytest_test_B1_certificate__009: execution marker recovered from complete JUnit XML; pytest_test_B1_certificate__002: timeout exit 124 at 100.11 s, no completed nodes; split into individual nodes.

Without `EIT_LJ_DEV6_ARCHIVE`, `tests/test_release_rc1.py::test_preservation_against_dev6` is skipped with an explicit reason; without `EIT_LJ_PAPER2_ARCHIVE`, the Paper 2 cross-checks are skipped.

## 2. Certificate replays

| replay | result |
|---|---|
| historical B1 certificate (`run_B1_erratum.py`) | semantic SHA-256 `616817fc…8518c6` accepted; Newton 222/222; carrier 222/222; endpoints accepted; min lower bound 1311719/536870912; certificate bytes unchanged |
| corrected B1 rebuild (corroboration only) | semantic SHA-256 `b2f8e6dc…d505` (as expected); passes corrected checker 222/222; Lemma K claim identical |
| B2.3 non-Taylor cross-check (b1_cert/b1_check import-blocked) | ok; 222/222 B1 boxes re-verified; semantic SHA-256 `f7bc244e…17d2` |
| `run_B2_3.py` | semantic SHA-256 `f7bc244e…17d2`; 222 boxes; independent check true; method controls 15/15 |
| `run_A2.py` | semantic SHA-256 `49dce160…6a71e` |
| `run_B1_erratum.py` all_required | true (full single run 68.2 s; piecewise re-execution also true) |

## 3. Deterministic regeneration of proof records

`run_A0, run_A1, run_B0, run_B2, run_B2_2, run_B2_4, run_B2_5` all exit 0. Every regenerated `data/` file is byte-identical to the stored one, or identical after removing only version/status keys (`version`, `project_version`, `status`, `status_line` — these carry the release-candidate version string) and timing/platform provenance (`seconds`, `timestamp_utc`, `python`, `platform`). Files with such metadata-only differences: A0_representation.json, A1_quartic.json, A2_lemma_M_certificate.json, B0_t2g.json, B1_ERRATUM_corrected_rebuild_certificate.json, B1_ERRATUM_report.json, B2_3_check_report.json, B2_3_method_controls.json, B2_4_branch.json, B2_c4hat_certificate.json, B2_carrier.json, B2_falsification.json, B2_quartic.json, B2_symmetry.json. The stored records were not replaced (they keep their V0.4 metadata).

## 4. Negative controls (mutation suites)

| suite | mutations | as required | baseline targets passing unmutated |
|---|---|---|---|
| `negative_controls.py` | 34 | 34/34 detected | 24/24 |
| `negative_controls_B2_2.py` | 9 | 9/9 detected | 6/6 |
| `negative_controls_B2_3.py` | 24 | 24/24 detected | 16/16 |
| `negative_controls_B1_erratum.py` | 13 | 13/13 (12 detected + 1 expected-undetected by design) | 10/10 |
| `negative_controls_B2_4.py` | 22 | 22/22 detected | 15/15 |
| `negative_controls_B2_5.py` | 28 | 28/28 detected | 15/15 |
| **total** | **130** | **130/130** | **86/86** |

Counts agree with the stored records in `data/*negative_controls*.json` (34, 9, 24, 13, 22, 28; all_detected / all_as_required true).

## 5. Identity and preservation controls

- `scripts/identity_controls_V0_4_dev6.py` on the original V0.4-dev.6 tree: 62/62 forbidden modifications rejected, unmodified tree PASS. On the release-candidate tree it is not applicable by design (it pins the dev.6 version string); it is superseded by the release-candidate checks below.
- `scripts/check_preservation_V1_0_0_rc1.py`: see `docs/V1.0.0-rc1_PRESERVATION_CHECK.md`.
- `scripts/preservation_controls_V1_0_0_rc1.py`: see `docs/V1.0.0-rc1_PRESERVATION_CONTROLS.json`.
- `scripts/check_release_text.py`: PASS, 0 findings; 30/30 bibliography entries cited.

## 6. Manuscript build

Clean build from the source ZIP (pdflatex, bibtex, pdflatex ×2): 30 pages, 30 references, 3 figures, 7 tables; no undefined references or citations; one overfull box of 0.92 pt; 26 hyperref PDF-bookmark token warnings (cosmetic, from mathematics in section titles). Figures regenerate deterministically from `paper/figures/make_figures.py`.

These checks are author-side evidence. They do not replace the final blind release audit and do not establish external validation.
