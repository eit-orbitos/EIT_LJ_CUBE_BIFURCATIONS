# AI-use log — Paper 3 (EIT-LJ Cube Bifurcations), V1.0.0

## Authors and responsibility

Paper 3 has two human authors: **Toni Mladenovski** and **Mihail Mladenski** (EITNetworks LLC, Tobyhanna, Pennsylvania, USA). AI systems are tools,
not authors. Toni Mladenovski directed the work (every phase gate, scope decision and status decision is recorded in
`RESEARCH_LOG.md`) and takes final responsibility for the claims. No project record documents that Mihail Mladenski
used, directed or reviewed any AI workflow, and none is claimed here.

## Systems and environments

| system | provider | role in this project |
|---|---|---|
| ChatGPT (GPT-5.6 Sol) | OpenAI | external assessment and planning input relayed by the author (the assessment of the original external brainstorm and the review gate of the B2 plan); its outputs entered the project only as instructions or claims to be checked |
| Claude | Anthropic | symbolic derivation assistance, code, tests, certificates and checkers, computational verification, documentation, manuscript and release preparation (the model that executed the work in the Tasklet environment) |
| Kimi (Kimi Agent) | Moonshot AI | independent blind adversarial audits of Track A, B1, erratum E-B1, B2.4 and B2.5 (reports in `audits/`); the B2.3 report does not name its system |
| Tasklet | Tasklet | agent execution environment in which the code was written and run, the records generated and the packages built |
| Google (suggestion relayed via ChatGPT) | Google | origin of the external brainstorm reviewed at the start (red team only); several of its claims were found to be wrong (`docs/CONTRADICTIONS_EXTERNAL_BRAINSTORM.md`) |

## Roles of AI assistance

- symbolic derivation assistance (SymPy-based exact calculations written and run by the AI under the author's plan);
- code assistance (all modules in `src/cube_bif/` and `scripts/`);
- test generation (`tests/`, negative controls and mutation suites);
- computational verification (certificate generation and independent checking, numerical corroboration);
- adversarial auditing (separate AI system; see `audits/`);
- manuscript and release preparation (`paper/`, `submission/`, release metadata).

The computational commands were executed by AI agents in the Tasklet sandbox, not personally by either author. The
author reviewed the reports, set every gate and authorised each phase.

## What the mathematical claims rest on

Not on unverified generative-model output. Every claim rests on:

- exact symbolic calculations (VERIFIED-EXACT records in `data/`, each with its own test);
- explicit proof arguments (standard Lyapunov–Schmidt reduction, the implicit function theorem, Haynsworth inertia
  additivity), with machine-checked dependency graphs;
- certified interval (ball) arithmetic with independent checkers (Arb via python-flint);
- independent re-certification in the audits (MPFR and Arb replays);
- archived reproducibility records, SHA-256 manifests and mechanical identity checks.

Independent AI audits are computational audits, not journal peer review. AI agreement does not prove a mathematical
claim; the certificates and proofs do.

## Figures

All figures are produced by the deterministic script `paper/figures/make_figures.py` from the project's own formulas
and data. No generative-AI artwork is used.

## Known AI-related incidents (disclosed)

- **Erratum E-B1:** an AI-written implementation of the Lemma K near-diagonal Taylor models did not raise python-flint's
  `ctx.cap`, so series were truncated and zero-padded. Found during B2.3 by an AI-written cross-check, corrected in
  V0.4-dev.4, independently re-audited and closed (NOTES §10, §11; manuscript §10.2).
- **B2.5 numerical tolerance:** an AI-chosen acceptance bound for a numerical corroboration check was raised after
  inspection (50·μ to 200·μ); disclosed in NOTES §13.8; the audit confirms it does not affect the proof.
- **RC2 metadata update (2026-11-16):** the author and institution metadata, declarations, bibliography metadata and
  release tooling of V1.0.0-rc2 were prepared by the AI agent (Claude in the Tasklet environment) from metadata supplied
  by Toni Mladenovski. No mathematical file was changed. No contribution role for Mihail Mladenski was generated.
- **V1.0.0 final release preparation (2026-11-16):** the version metadata, archived audit record, release notes, release
  tooling and packaging of V1.0.0 were prepared by the AI agent (Claude in the Tasklet environment). The
  author-contribution, competing-interests and copyright texts were supplied and approved by the authors and inserted
  verbatim; the agent did not write or extend them. The final blind release audit of V1.0.0-rc2 was performed by a
  separate auditor (supplied by the author as the Kimi audit), not by the preparing agent. No mathematical file was
  changed.
