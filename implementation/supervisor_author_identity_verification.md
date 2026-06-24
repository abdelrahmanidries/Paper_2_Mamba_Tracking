# Supervisor Author Identity Verification

## Verification Standard

I included a paper only when the author instance was supported by at least two identity signals, preferably: Concordia affiliation in the PDF, official Concordia profile, ORCID/OpenAlex disambiguation, recurring coauthor network, and DOI metadata.

Unavailable papers remain in metadata but are not analyzed as full text.

## M. O. Ahmad

Verified identity: **M. Omair Ahmad**, Concordia University.

Evidence signals:

- Official Concordia profile: <https://www.concordia.ca/faculty/omair-ahmad.html>
- Concordia personal ECE page: <https://users.encs.concordia.ca/~omair/>
- OpenAlex author profile: <https://openalex.org/A5068820891>
- ORCID in OpenAlex metadata: <https://orcid.org/0000-0002-2924-6659>
- Repeated PDF affiliation evidence: Department of Electrical and Computer Engineering, Concordia University, in `AS2010_EURASIP_CEPSTRUM`, `AS2014_EURASIP_ECHO`, `AS2015_MSAINDELFR`, `AS2018_VARIATIONAL_MIXED_NOISE`, `AH2020_R_SPATIOGRAM_TRACKING`, and `AS2024_PATHOWAVE`.
- Recurring coauthors: Wei-Ping Zhu, M. N. S. Swamy, Alireza Esmaeilzehi, and other Concordia ECE signal/image processing collaborators.

Decision: high-confidence identity for included Ahmad papers.

## M. N. S. Swamy

Verified identity: **M. N. S. Swamy**, Concordia University.

Evidence signals:

- Concordia ECE personal page: <https://users.encs.concordia.ca/~swamy/>
- OpenAlex author profile: <https://openalex.org/A5013967994>
- ORCID in OpenAlex metadata: <https://orcid.org/0000-0002-3989-5476>
- Repeated PDF affiliation evidence: Department of Electrical and Computer Engineering, Concordia University, in `AS2015_MSAINDELFR`, `AS2018_VARIATIONAL_MIXED_NOISE`, `AS2024_PATHOWAVE`, `SW2013_FRONTIERS_SYNAPTIC`, and `SW2015_COSINE_TCHEBICHEF`.
- Recurring coauthor network with M. Omair Ahmad and Wei-Ping Zhu in signal, image, biomedical, and circuit/systems papers.

Decision: high-confidence identity for included Swamy papers except `SW2019_HEARING_AIDS`, which is marked medium-high because the accessible manuscript confirms the DOI/repository record and author name but exposes less first-page affiliation detail than the other PDFs.

## Ambiguity and Exclusion Rules

- Initials are ambiguous. I did not use papers merely because they contained a similar “Ahmad” or “Swamy” name.
- OpenAlex entries for Swamy alone showed possible name-collision pollution. I excluded any item that did not also show Concordia affiliation, recurring ECE coauthors, or DOI/PDF consistency.
- Recent IEEE Transactions papers by the verified Ahmad-Swamy author pair were discovered but excluded from full-text analysis when no lawful accessible PDF could be obtained.

## Included Full-Text Papers

| Corpus ID | Supervisor identity basis | Full text source |
|---|---|---|
| `AS2024_PATHOWAVE` | PDF lists both Ahmad and Swamy at Concordia ECE | arXiv author-posted preprint |
| `AH2020_R_SPATIOGRAM_TRACKING` | PDF lists Ahmad at Concordia ECE | publisher-open PDF |
| `AS2018_VARIATIONAL_MIXED_NOISE` | PDF lists both at Concordia ECE | arXiv author-posted preprint |
| `AS2015_MSAINDELFR` | PDF lists both at Concordia ECE; Ahmad corresponding | BMC open-access PDF |
| `AS2014_EURASIP_ECHO` | PDF lists Ahmad at Concordia ECE | EURASIP/SpringerOpen PDF |
| `AS2010_EURASIP_CEPSTRUM` | PDF lists Ahmad at Concordia ECE | Hindawi/EURASIP open PDF |
| `SW2019_HEARING_AIDS` | DOI/repository record and recurring Swamy signal-processing authorship | Aalborg institutional accepted manuscript |
| `SW2015_COSINE_TCHEBICHEF` | PDF lists Swamy at Concordia ECE | publisher-open PDF |
| `SW2013_FRONTIERS_SYNAPTIC` | PDF lists Swamy at Concordia ECE | Frontiers open-access PDF |

## Excluded but Discovered Papers

The excluded recent IEEE papers are listed in `experiments/supervisor_style_corpus_metadata.csv` with `full_text_available=false`. They were not analyzed beyond metadata. Important examples include IEEE TPAMI 2025 ACLI, IEEE TGRS 2025 UADiff, IEEE TBC 2024 DMML, IEEE TAI 2022 ultralight super-resolution, IEEE TCI 2021 SRNSSI, IEEE TBC 2021 UPDResNN, and IEEE TIP 2019 image denoising.
