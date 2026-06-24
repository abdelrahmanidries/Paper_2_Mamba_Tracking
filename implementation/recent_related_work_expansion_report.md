# Recent Related Work Expansion Report

## Scope

Expanded `paper/ieee_transactions/sections/related_work.tex` using verified recent literature on transformer/one-stream tracking, temporal target adaptation, visual state-space models, Mamba-based tracking, restoration-oriented Mamba, and tracking under degraded observations.

## Papers Audited

Twenty-two candidate or boundary papers were audited in `experiments/related_work_recent_literature_audit.csv`.

## Already Present Before Expansion

- `gu2024mamba`
- `zhu2024visionmamba`
- `liu2024vmamba`
- `guo2024mambair`
- `guo2025mambairv2`
- `ye2022ostrack`
- `cui2022mixformer`
- `li2024mambalct`
- `huang2024mambafetrack`
- `wang2024mambaevt`
- `wu2024mambanut`
- `zhong2024llot`
- `invtrack_local`

## New Sources Added

- `chen2023seqtrack`
- `cai2023romtrack`
- `cai2024hiptrack`
- `zheng2024odtrack`
- `lin2024lorat`
- `xie2024aqatrack`
- `wang2025mambafetrackv2`

## Bibliography Updates

- Added 7 BibTeX entries.
- Updated `guo2024mambair` with arXiv metadata.
- Updated `guo2025mambairv2` with CVPR 2025 page range and arXiv metadata.
- Normalized title capitalization for `wang2024mambaevt`.
- Updated `wu2024mambanut` title to match the revised arXiv record.
- Removed 0 entries.

## Final Related Work Structure

1. Transformer and One-Stream Visual Tracking
2. Temporal Modeling and Target Adaptation
3. State-Space Models for Visual Representation
4. Mamba-Based Visual Tracking
5. Tracking Under Degraded Observations and Present-Work Positioning

## Final Paper List by Subsection

| Subsection | Citation keys |
|---|---|
| Transformer and One-Stream Visual Tracking | `chen2021transt`, `yan2021stark`, `cui2022mixformer`, `ye2022ostrack`, `chen2023seqtrack`, `cai2023romtrack`, `cai2024hiptrack`, `zheng2024odtrack`, `lin2024lorat`, `xie2024aqatrack` |
| Temporal Modeling and Target Adaptation | `yan2021stark`, `cai2024hiptrack`, `zheng2024odtrack`, `chen2023seqtrack`, `xie2024aqatrack` |
| State-Space Models for Visual Representation | `gu2024mamba`, `zhu2024visionmamba`, `liu2024vmamba`, `guo2024mambair`, `guo2025mambairv2` |
| Mamba-Based Visual Tracking | `li2024mambalct`, `huang2024mambafetrack`, `wang2025mambafetrackv2`, `wang2024mambaevt`, `wu2024mambanut` |
| Tracking Under Degraded Observations and Present-Work Positioning | `zhong2024llot`, `wu2024mambanut`, `invtrack_local` |

## Citation Counts

| Subsection | Citation commands | Unique references |
|---|---:|---:|
| Transformer and One-Stream Visual Tracking | 4 | 10 |
| Temporal Modeling and Target Adaptation | 3 | 5 |
| State-Space Models for Visual Representation | 3 | 5 |
| Mamba-Based Visual Tracking | 5 | 5 |
| Tracking Under Degraded Observations and Present-Work Positioning | 3 | 3 |

Unique sources cited in Related Work after expansion: 22.

## Peer-Reviewed Versus Preprint Count

For the 22 unique Related Work sources:

- Peer-reviewed or accepted peer-reviewed: 12.
- ArXiv-only or final venue not independently confirmed: 9.
- Local unpublished evidence: 1.

## Publication-Year Distribution

| Year | Count |
|---|---:|
| 2021 | 2 |
| 2022 | 2 |
| 2023 | 2 |
| 2024 | 14 |
| 2025 | 2 |

## Citation-Density and Readability Checks

- Paragraphs with more than five citations: 0.
- Claims with no supporting citation: none found in the expanded Related Work for major literature claims.
- Repeated citations: `yan2021stark`, `chen2023seqtrack`, `cai2024hiptrack`, `zheng2024odtrack`, `xie2024aqatrack`, and `wu2024mambanut` are repeated because they support both method-family and boundary-positioning claims.
- Redundant candidate not selected: ARTrackV2 was not selected because SeqTrack and AQATrack already support the autoregressive tracking synthesis.
- Optional candidate not selected: Camouflaged Object Tracking was not selected because the manuscript is focused on image-quality degradation rather than camouflage.

## Unresolved Metadata

- `invtrack_local`: local unpublished evidence only.
- `liu2024vmamba`: final publication metadata not independently confirmed.
- `li2024mambalct`: final venue not independently confirmed despite local paper card.
- `huang2024mambafetrack`: arXiv record states in peer review.
- `wang2024mambaevt`: final venue not independently confirmed despite local paper card.
- `wu2024mambanut`: final venue not independently confirmed despite local paper card.
- `zhong2024llot`: final venue not independently confirmed.
- `zheng2024odtrack`: final venue not independently confirmed.
- `xie2024aqatrack`: final venue not independently confirmed.
- `wang2025mambafetrackv2`: arXiv-only journal extension record.

## Claim-Boundary Checks

- No unsupported C13 state-of-the-art claim was added.
- No unsupported C14 universal robustness claim was added.
- Corrected NFS provenance was not modified.
- TDM remains rejected and absent from the final method.
- Final method remains global feature consistency with `lambda=0.02`.
- The proposed method is positioned as RG-SSB after search-token extraction with frozen OSTrack backbone, not as a complete Mamba backbone or full image-restoration network.
