# Prepared GitHub release material for V1.0.0 — NOT USED YET

Prepared during final release preparation. **Nothing here has been executed:** no push, no tag, no GitHub release, no
draft release. GitHub = HOLD. These texts may be used only after the RC2 → V1.0.0 delta/preservation audit passes and
the authors explicitly authorize the public release. When that happens, the Zenodo DOI placeholder below is replaced by
the DOI actually minted; no identifier is invented here.

## Repository tree

The repository content is the content of `EIT_LJ_CUBE_BIFURCATIONS_V1.0.0.zip` (top-level folder
`EIT_LJ_CUBE_BIFURCATIONS/`), with every file at the path listed in its `SHA256SUMS`, including hidden files
(`.zenodo.json`). The repository name and URL are not fixed yet: `[PAPER 3 GITHUB RELEASE — TO BE ASSIGNED AT PUBLIC RELEASE]`.

## Annotated tag message (tag `v1.0.0` — NOT CREATED)

```text
EIT-LJ Cube Bifurcations (Paper 3) V1.0.0

Symmetry-Breaking Bifurcations from the Cubic Equilibrium in Two-Term Inverse-Power Clusters
Toni Mladenovski, Mihail Mladenski (EITNetworks LLC, Tobyhanna, Pennsylvania, USA)

Code, certificates, certificate checkers, tests, negative controls, proof dependency graphs, verbatim audit
records and manuscript sources. Mathematics as audited at V0.4-dev.6; V1.0.0-rc2 passed the final blind release
audit (RELEASE-READY); V1.0.0 adds only author-approved declarations and final metadata.
```

## Release title

`V1.0.0 — Symmetry-Breaking Bifurcations from the Cubic Equilibrium in Two-Term Inverse-Power Clusters`

## Release description

```markdown
Paper 3 of the EIT-LJ series: local symmetry-breaking bifurcations from the eight-particle cubic equilibrium for the
two-term inverse-power pair potential V(r) = A r^(-p) - B r^(-q).

Authors: Toni Mladenovski (corresponding; ORCID 0009-0009-8343-662X) and Mihail Mladenski — EITNetworks LLC,
Tobyhanna, Pennsylvania, USA.

Main results (local): A2u/Td Z2 pitchfork (supercritical in the reduced-energy convention); T2g/D3d transcritical
branches; T2g/D2h Z2 pitchfork (configurations exactly D2h, not cuboids); D2h branch inertia (negative, zero,
positive): centre (1, 0, 2), rigid-motion-reduced (4, 0, 14) — saddles. No global, stability or technology claim.

Statuses: Track A (Lemma M, Corollary M, Theorem A), B1 (Lemma K, Proposition B1; erratum E-B1 closed), Lemma Q,
Propositions B2 and B3 and Corollary B3′ — certified / proved (computer-assisted) and independently audited. The
independent audits are computational verifications by AI systems, archived verbatim in `audits/`; they are not
journal peer review.

Archive: [PAPER 3 ZENODO DOI — TO BE ASSIGNED AT PUBLIC RELEASE]
Licences: software PolyForm Noncommercial License 1.0.0; manuscript, documentation, figures, generated results and
package-authored metadata CC BY-NC-SA 4.0. Commercial use only by separate written agreement.
Copyright © 2026 EITNetworks LLC and the authors.
This research received no external funding.
```

## Assets to attach (with the SHA-256 values of `V1_ARTIFACT_HASHES.sha256`)

1. `EIT_LJ_CUBE_BIFURCATIONS_V1.0.0.zip` and `EIT_LJ_CUBE_BIFURCATIONS_V1.0.0.zip.sha256`
2. `EIT_LJ_Paper3_manuscript_V1.0.0.pdf`
3. `EIT_LJ_Paper3_source_V1.0.0.zip` (`manuscript.tex` at the ZIP root)
4. `V1_ARTIFACT_HASHES.sha256`

The JMC package (`EIT_LJ_Paper3_JMC_V1.0.0_package.zip`) is for journal submission and is not a release asset.
