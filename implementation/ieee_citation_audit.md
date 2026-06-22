# IEEE Citation Audit

## Resolution Method

Priority order followed:

1. Local project evidence: `paper/ieee_transactions/references.bib`, local tracker dataset comments, local paper cards, and `papers/InvTrack.pdf`.
2. Crossref metadata queries for exact title, author order, venue, pages, year, and DOI.
3. arXiv metadata where Crossref/local evidence needed title or author corroboration.

No citation metadata was guessed. DOI fields were inserted only when Crossref returned an exact matching record.

## Resolved Required Sources

| Key | Source | Metadata Status |
|---|---|---|
| `ye2022ostrack` | Joint Feature Learning and Relation Modeling for Tracking: A One-Stream Framework | Exact title, author list, ECCV 2022 venue, LNCS pages 341--357, and DOI verified by Crossref; arXiv 2203.11991 corroborates title/authors. |
| `fan2019lasot` | LaSOT: A High-Quality Benchmark for Large-Scale Single Object Tracking | Exact CVPR 2019 title, author list, pages 5369--5378, and DOI verified by Crossref; local pytracking files corroborate title. |
| `wu2013otb` | Online Object Tracking: A Benchmark | Exact title, authors, CVPR 2013 venue, pages 2411--2418, and DOI verified by Crossref. |
| `mueller2016uav123` | A Benchmark and Simulator for UAV Tracking | Exact title, authors, ECCV 2016 venue, LNCS pages 445--461, and DOI verified by Crossref; local tracker files corroborate UAV123 title. |
| `galoogahi2017nfs` | Need for Speed: A Benchmark for Higher Frame Rate Object Tracking | Exact title, authors, ICCV 2017 venue, pages 1134--1143, and DOI verified by Crossref; arXiv 1703.05884 corroborates title/authors. |

## Placeholder Audit

- OSTrack placeholder replaced with `\cite{ye2022ostrack}`.
- LaSOT placeholder replaced with `\cite{fan2019lasot}`.
- OTB placeholder replaced with `\cite{wu2013otb}`.
- UAV123 placeholder replaced with `\cite{mueller2016uav123}`.
- NFS placeholder replaced with `\cite{galoogahi2017nfs}`.
- The explanatory citation-placeholder macro was removed from `main.tex`.

Expected unresolved citation count: 0.

## InvTrack Local Entry

`invtrack_local` is retained because the manuscript cites InvTrack in the introduction and degradation-robust tracking related work. The local PDF verifies the paper title and author list, but it has placeholder publication dates and placeholder DOI-style text. The entry therefore remains `@unpublished` and should not be treated as final bibliographic metadata.
