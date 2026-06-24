# Introduction and Related Work Citation Map

## Summary

All genuine `[CITATION REQUIRED: ...]` placeholders in the rewritten IEEE Transactions Introduction and Related Work were replaced. New citations were selected only when technically relevant to the sentence being supported. Supervisor-corpus papers were not cited for style-only reasons.

## Placeholder Resolution Table

| ID | Exact sentence | Claim type | Required source category | Selected citation(s) | BibTeX key(s) | Verification source |
|---|---|---|---|---|---|---|
| P1 | State-space models and Mamba-based vision modules have recently attracted attention because they provide a mechanism for structured long-range feature modeling with favorable computational properties. | State-space/vision foundation | State-space and Mamba foundations; visual Mamba/state-space models | Gu and Dao 2024; Zhu et al. 2024; Liu et al. 2024 | `gu2024mamba`; `zhu2024visionmamba`; `liu2024vmamba` | arXiv:2312.00752; arXiv:2401.09417; arXiv:2401.10166 |
| P2 | In visual tracking, reported Mamba-based designs use state-space modules for purposes such as long-term context modeling, multimodal feature interaction, nonlinear motion prediction, dynamic template generation, or nighttime template-search representation learning. | Technical positioning | Mamba-based tracking | Li et al. 2024; Huang et al. 2024; Xiao et al. 2024; Wang et al. 2024; Wu et al. 2024 | `li2024mambalct`; `huang2024mambafetrack`; `xiao2024mambatrack`; `wang2024mambaevt`; `wu2024mambanut` | arXiv records plus local paper cards |
| P3 | Modern RGB trackers have increasingly used transformer-based feature interaction to relate the initial target template to the search region. | Tracking method family | Transformer-based visual tracking | Chen et al. 2021; Yan et al. 2021 | `chen2021transt`; `yan2021stark` | arXiv:2103.15436; arXiv:2103.17154 |
| P4 | One-stream tracking further simplifies this formulation by learning template-search relations in a unified stream rather than maintaining separate feature extraction and matching stages. | Tracking method family | One-stream/template-search tracking | Cui et al. 2022; Ye et al. 2022 | `cui2022mixformer`; `ye2022ostrack` | arXiv:2203.11082; existing OSTrack bibliography entry |
| P5 | Robust tracking under degraded observations has been studied from several viewpoints, including low-light benchmark construction, nighttime UAV tracking, degradation-aware training, invariant feature learning, and evaluation under corrupted visual inputs. | Degradation/adverse tracking | Degradation/adverse-condition tracking | Zhong et al. 2024; Wu et al. 2024; local InvTrack | `zhong2024llot`; `wu2024mambanut`; `invtrack_local` | arXiv:2408.11463; arXiv:2412.00626; local InvTrack PDF/paper card |
| P6 | State-space and Mamba-based modules have been adopted in vision because they can model structured dependencies without relying solely on quadratic attention. | State-space/vision foundation | State-space and Mamba foundations; visual Mamba/state-space models | Gu and Dao 2024; Zhu et al. 2024; Liu et al. 2024 | `gu2024mamba`; `zhu2024visionmamba`; `liu2024vmamba` | arXiv:2312.00752; arXiv:2401.09417; arXiv:2401.10166 |
| P7 | In tracking, recent Mamba-based methods have been reported for roles such as temporal modeling, multimodal fusion, motion reasoning, template update, or efficient feature processing. | Technical positioning | Mamba-based tracking | Li et al. 2024; Huang et al. 2024; Xiao et al. 2024; Wang et al. 2024; Wu et al. 2024 | `li2024mambalct`; `huang2024mambafetrack`; `xiao2024mambatrack`; `wang2024mambaevt`; `wu2024mambanut` | arXiv records plus local paper cards |

## New Bibliography Entries

- `chen2021transt`: Transformer Tracking.
- `yan2021stark`: Learning Spatio-Temporal Transformer for Visual Tracking.
- `cui2022mixformer`: MixFormer: End-to-End Tracking with Iterative Mixed Attention.
- `gu2024mamba`: Mamba: Linear-Time Sequence Modeling with Selective State Spaces.
- `zhu2024visionmamba`: Vision Mamba: Efficient Visual Representation Learning with Bidirectional State Space Model.
- `liu2024vmamba`: VMamba: Visual State Space Model.
- `li2024mambalct`: MambaLCT: Boosting Tracking via Long-term Context State Space Model.
- `huang2024mambafetrack`: Mamba-FETrack: Frame-Event Tracking via State Space Model.
- `xiao2024mambatrack`: MambaTrack: A Simple Baseline for Multiple Object Tracking with State Space Model.
- `wang2024mambaevt`: MambaEVT: Event Stream based Visual Object Tracking using State Space Model.
- `wu2024mambanut`: MambaNUT: Nighttime UAV Tracking via Mamba and Adaptive Curriculum Learning.
- `zhong2024llot`: Low-Light Object Tracking: A Benchmark.

## Remaining Human-Review Items

- Several new entries are arXiv/preprint records because DOI or final page metadata was not confirmed locally.
- `invtrack_local` remains local unpublished evidence until final publication metadata is confirmed.
- The manuscript still avoids state-of-the-art, universal robustness, and uniform-improvement claims.
