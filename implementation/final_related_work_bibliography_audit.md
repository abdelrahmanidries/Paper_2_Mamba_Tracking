# Final Related Work Bibliography Audit

## Scope

This audit checked the unresolved or preprint-backed Related Work references against authoritative sources before final submission packaging. No new papers were added, and scientific claims/results were not expanded.

Primary local files audited:

- `paper/ieee_transactions/references.bib`
- `paper/ieee_transactions/sections/introduction.tex`
- `paper/ieee_transactions/sections/related_work.tex`
- `experiments/related_work_recent_literature_audit.csv`
- `implementation/recent_related_work_expansion_report.md`

## Source Decisions

| Key | Final decision | Evidence used | Metadata outcome |
|---|---|---|---|
| `liu2024vmamba` | Upgraded from arXiv-only to peer-reviewed conference | arXiv metadata reports "NeurIPS 2024 spotlight" for `arXiv:2401.10166` | Venue set to `Advances in Neural Information Processing Systems`, year 2024, note `Spotlight`; DOI/pages not reported |
| `li2024mambalct` | Retained as preprint | arXiv metadata for `arXiv:2412.13615`; no authoritative final venue found | No venue/DOI invented |
| `huang2024mambafetrack` | Retained as preprint | arXiv metadata for `arXiv:2404.18174` reports `In Peer Review`; no authoritative final record found | No venue/DOI invented |
| `wang2024mambaevt` | Retained as preprint | arXiv metadata for `arXiv:2408.10487` reports `In Peer Review`; no authoritative final record found | No venue/DOI invented |
| `wu2024mambanut` | Retained as preprint | arXiv metadata for `arXiv:2412.00626`; no authoritative IROS/final record found | Title updated to current arXiv casing; no venue/DOI invented |
| `zhong2024llot` | Retained as preprint | arXiv metadata for `arXiv:2408.11463`; no authoritative final record found | No venue/DOI invented |
| `zheng2024odtrack` | Retained as preprint | arXiv metadata for `arXiv:2401.01686`; no authoritative final record found | No venue/DOI invented |
| `xie2024aqatrack` | Retained as preprint | arXiv metadata for `arXiv:2403.10574`; no authoritative final record found | Title updated to current arXiv spelling; no venue/DOI invented |
| `wang2025mambafetrackv2` | Retained as preprint | arXiv metadata for `arXiv:2506.23783`; comment says journal extension of PRCV 2024 Mamba-FETrack but gives no final journal venue | Title updated to current arXiv casing; no journal venue/DOI invented |
| `invtrack_local` | Removed from submission-facing bibliography and citations | Local PDF has placeholder dates and DOI; web search found no exact authoritative publication/preprint metadata | Not cited in final submission |

## Final Publication Records Found

- `liu2024vmamba`: VMamba was upgraded to NeurIPS 2024 spotlight. Volume, issue, pages, article number, and DOI remain not reported in the verified metadata used here.

## Papers Remaining as Preprints

- `li2024mambalct`
- `huang2024mambafetrack`
- `wang2024mambaevt`
- `wu2024mambanut`
- `zhong2024llot`
- `zheng2024odtrack`
- `xie2024aqatrack`
- `wang2025mambafetrackv2`

## InvTrack Decision

`invtrack_local` was removed from `references.bib` and from manuscript citations. The local `papers/InvTrack.pdf` contains placeholder publication dates and a placeholder DOI (`10.1109/XXXX.2022.1234567`), and no exact authoritative publication or arXiv record was found for the title. It is therefore not suitable for final submission citation.

## Bibliography Entries Updated

- `liu2024vmamba`: entry type changed to `@inproceedings`; venue and spotlight note added.
- `li2024mambalct`: arXiv preprint note added.
- `huang2024mambafetrack`: arXiv preprint note added.
- `wang2024mambaevt`: title casing aligned to arXiv; arXiv preprint note added.
- `wu2024mambanut`: title casing aligned to arXiv; arXiv preprint note added.
- `zhong2024llot`: arXiv preprint note added.
- `zheng2024odtrack`: arXiv preprint note added.
- `xie2024aqatrack`: title spelling aligned to arXiv; arXiv preprint note added.
- `wang2025mambafetrackv2`: title casing aligned to arXiv; arXiv preprint note added.
- `invtrack_local`: removed.

## Unresolved Metadata

- No publisher DOI, pages, volume, issue, or article number was verified for the retained preprints.
- Mamba-FETrack V2 reports that Mamba-FETrack was published at PRCV 2024, but no official PRCV/Springer/DBLP/Crossref record was verified during this audit, so the original Mamba-FETrack entry was not upgraded.
- VMamba pages/volume/article number were not verified from an official proceedings page during this audit; the upgrade relies on verified arXiv metadata reporting NeurIPS 2024 spotlight.

## Manuscript Impact

- Related Work remains in the same five-subsection structure.
- Related Work now cites 21 unique sources, which remains approximately the requested 22-source target.
- Peer-reviewed and preprint records are distinguished in BibTeX notes where needed.
- No local unpublished evidence is cited in the final manuscript.
