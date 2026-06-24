# Introduction and Related Work Citation Map

## Summary

The IEEE Transactions Introduction and Related Work now use a broader but bounded set of tracking, state-space, Mamba tracking, restoration, and degraded-observation citations. The expansion keeps the approved claim boundaries: no state-of-the-art claim by the present method, no universal robustness claim, no claim that Mamba has not been used in tracking, and no claim that low-light or degradation-aware tracking is absent.

## Subsection-Level Related Work Map

| Section | Main supported claim | Selected citation keys | Verification source |
|---|---|---|---|
| Transformer and One-Stream Visual Tracking | Transformer and one-stream trackers model template-search interaction, while recent trackers explore sequence generation, robust object modeling, prompting, temporal token propagation, parameter-efficient adaptation, and autoregressive queries. | `chen2021transt`; `yan2021stark`; `cui2022mixformer`; `ye2022ostrack`; `chen2023seqtrack`; `cai2023romtrack`; `cai2024hiptrack`; `zheng2024odtrack`; `lin2024lorat`; `xie2024aqatrack` | CVF pages for SeqTrack/ROMTrack/HIPTrack; arXiv records for ODTrack/LoRAT/AQATrack; existing bibliography for TransT/STARK/MixFormer/OSTrack |
| Temporal Modeling and Target Adaptation | Recent tracking methods use tracking history, temporal tokens, autoregressive decoding, or spatio-temporal queries; this differs from restoration-guided search-feature adaptation. | `yan2021stark`; `cai2024hiptrack`; `zheng2024odtrack`; `chen2023seqtrack`; `xie2024aqatrack` | CVF/arXiv records listed in the audit CSV |
| State-Space Models for Visual Representation | Mamba, Vision Mamba, and VMamba establish state-space visual representation foundations; MambaIR and MambaIRv2 establish restoration-oriented state-space processing but not tracking localization. | `gu2024mamba`; `zhu2024visionmamba`; `liu2024vmamba`; `guo2024mambair`; `guo2025mambairv2` | arXiv/CVF records; CVF confirmed MambaIRv2 pages 28124--28133 |
| Mamba-Based Visual Tracking | Mamba trackers already use state-space modules for long-term context, RGB-event fusion, event-only dynamic template generation, and nighttime UAV tracking. | `li2024mambalct`; `huang2024mambafetrack`; `wang2025mambafetrackv2`; `wang2024mambaevt`; `wu2024mambanut` | arXiv records and local paper-card evidence; final venue unresolved for several entries |
| Tracking Under Degraded Observations and Present-Work Positioning | Low-light tracking and degradation-invariant tracking already exist, so the proposed method is positioned narrowly as feature-level restoration-guided state-space adaptation inside OSTrack. | `zhong2024llot`; `wu2024mambanut`; `invtrack_local` | arXiv LLOT/MambaNUT records; local InvTrack evidence |

## New Bibliography Entries

- `chen2023seqtrack`: SeqTrack: Sequence to Sequence Learning for Visual Object Tracking.
- `cai2023romtrack`: Robust Object Modeling for Visual Tracking.
- `cai2024hiptrack`: HIPTrack: Visual Tracking with Historical Prompts.
- `zheng2024odtrack`: ODTrack: Online Dense Temporal Token Learning for Visual Tracking.
- `lin2024lorat`: Tracking Meets LoRA: Faster Training, Larger Model, Stronger Performance.
- `xie2024aqatrack`: Autoregressive Queries for Adaptive Tracking with Spatio-Temporal Transformers.
- `wang2025mambafetrackv2`: Mamba-FETrack V2: Revisiting State Space Model for Frame-Event Based Visual Object Tracking.

## Updated Bibliography Entries

- `guo2024mambair`: added arXiv identifier and archive metadata; final page metadata remains unresolved.
- `guo2025mambairv2`: updated to CVPR 2025 proceedings format with verified pages 28124--28133 and arXiv identifier.
- `wang2024mambaevt`: normalized title capitalization to the paper title.
- `wu2024mambanut`: updated title to the revised arXiv title.

## Remaining Human-Review Items

- `invtrack_local` remains local unpublished evidence until final publication metadata is confirmed.
- `liu2024vmamba`, `li2024mambalct`, `huang2024mambafetrack`, `wang2024mambaevt`, `wu2024mambanut`, `zhong2024llot`, `zheng2024odtrack`, `xie2024aqatrack`, and `wang2025mambafetrackv2` remain arXiv-only in the bibliography because no final publication metadata was independently confirmed during this audit.
- Local paper cards list final venues for some Mamba tracking papers, but the audit uses independently verified metadata in `experiments/related_work_recent_literature_audit.csv`.
