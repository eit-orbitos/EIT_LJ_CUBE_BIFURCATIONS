# Reference verification — manuscript V1.0.0

`paper/references.bib` has 30 entries; all 30 are cited in the manuscript and every citation resolves (checked by
`scripts/check_release_text.py` and by the BibTeX log of the clean build: no undefined citation).

## V1.0.0 (2026-11-16)

No bibliographic entry changed except the note of `Repo3` (Paper 3's own release: version 1.0.0, public release not yet
executed, with the controlled identifier placeholders). The 30 entries, their metadata and their DOIs are those of RC2,
which the final blind release audit re-checked (all 25 DOI-bearing entries resolved; no metadata defect found).

## RC2 bibliographic QA (2026-11-16)

Every entry with a DOI was re-resolved at Crossref (DataCite for Zenodo DOIs), and title, year, volume, pages/article
number and first-author family name were compared mechanically, then each mismatch was read by hand.

| result | entries |
|---|---|
| DOI resolved; every compared field agrees (21) | Palais 1979; Haynsworth 1968; Chechin–Gnezdilov–Zekhtser 2003; Doye–Wales 2002; Schwerdtfeger–Wales 2024; Hoare–McInnes 1983; Hoare–Pal 1971; Johansson 2017; SymPy 2017; Trombach et al. 2018; Paper 1; Golubitsky–Schaeffer 1985; Golubitsky–Stewart–Schaeffer 1988; Ihrig–Golubitsky 1984; Chossat–Lauterbach 2000; Cicogna 1981; Kielhöfer 2012; Milnor 1963; Moore–Kearfott–Cloud 2009; Field 2007; Krantz–Parks 2013 |
| DOI resolved; mechanical mismatch explained, entry correct (4) | Fousse et al. 2007 — the .bib gives `Art. 13`, Crossref gives article number `13` (same); Paper 2 — the .bib cites the manuscript title supplied by the author, the Zenodo record is titled "EIT-LJ Full-Vector Equilibria and Stability (Paper 2): code, certificates and audit records" (the note in the entry states this); Sturmfels 2008 — the Springer record returned no author list (title, year and DOI agree); Arjevani–Field 2022 — Crossref's title contains markup for S_k (text otherwise identical) |
| No DOI in the entry (5) | Tucker 2011 (book; a De Gruyter e-book DOI candidate exists but was not added, since the cited edition is the Princeton print edition); Wilson–Decius–Cross 1955 (book; no DOI found for the book); python-flint and mpmath (software, URL and version); `Repo3` (the Paper 3 release itself, placeholders only) |

Changes made in RC2 (metadata only, each confirmed at Crossref): Chechin et al. 2003 — DOI
`10.1016/S0020-7462(02)00081-1` added and page `1451` completed to `1451--1472`; Schwerdtfeger–Wales 2024 — DOI
`10.1021/acs.jctc.4c00135` added. Both entries are marked in the .bib file. `Repo3` now names release candidate
1.0.0-rc2. No other entry changed. No DOI was invented.

## Earlier verification (RC1, 2026-11-15; still valid)

- 15 entries marked `[P2]` are taken from the audited Paper 2 bibliography (Paper 2 V1.0, DOI
  10.5281/zenodo.24187155); two of them received a DOI in RC2 (above).
- 14 further entries were checked against Crossref, publisher (Springer, World Scientific, De Gruyter, SIAM, Elsevier),
  DataCite/Zenodo and arXiv records. Notes: the Golubitsky–Schaeffer and Golubitsky–Stewart–Schaeffer DOIs are the
  e-book records; Milnor's DOI is the electronic edition; Krantz–Parks is the 2013 reprint of the 2002 book; the
  Arjevani–Field arXiv title uses S_n where the journal version uses S_k.
- One candidate reference (Vanderbauwhede, *Local Bifurcation and Symmetry*, Pitman 1982) could only be partially
  confirmed and is **not** used.

## Status wording

Paper 1 (DOI 10.5281/zenodo.24149914, concept 10.5281/zenodo.24149913) is a Zenodo preprint, version 0.1.2. Paper 2
(DOI 10.5281/zenodo.24187155, concept 10.5281/zenodo.24187154) is a Zenodo archive record, version 1.0.0, with GitHub
repository https://github.com/eit-orbitos/EIT_LJ_FULL_VECTOR_STABILITY. Neither is described as journal-published.
Paper 3's own release is cited as version 1.0.0, not yet publicly released, with the placeholders
`[PAPER 3 GITHUB RELEASE — TO BE ASSIGNED AT PUBLIC RELEASE]` and `[PAPER 3 ZENODO DOI — TO BE ASSIGNED AT PUBLIC RELEASE]`; no identifier is invented.
