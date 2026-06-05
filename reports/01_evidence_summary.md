# Evidence Summary: Paper Matrix

Source: all Markdown files in `paper_cards/`. No PDFs or extracted JSONL files were used for this matrix generation step.

## Coverage
- Paper cards parsed: 20
- CSV output: `tables/paper_matrix.csv`
- Columns: 26
- Research gaps: not generated in this report.

## Tracking/task coverage
- image restoration (not tracking): 2
- multi-camera multi-target tracking: 1
- multi-object tracking: 4
- single-object tracking: 9
- visual object tracking: 4

## Modality coverage
- RGB-only or RGB-style: 8
- Multimodal/sensor-augmented: 10
- Image restoration input/output: 2

## Degradation and restoration coverage
- Degradation handling values: not reported=4, partial=13, yes=3
- Restoration/enhancement values: no=4, not reported=11, partial=2, yes=3
- All `Yes` and `Partial` values in the matrix retain page evidence either in the cell text or in the `evidence_pages` column.

## Mamba usage patterns observed in the cards
- Image restoration: MambaIR and MambaIRv2 use Mamba/SSM blocks for image restoration tasks.
- Template-search temporal/context modeling: MambaLCT, MCITrack, TemTrack, SMTrack, MambaEVT, MambaVT, MamTrack, HyMamba, and related trackers use Mamba-style hidden states, context, memory, or template/search interaction.
- Motion prediction or MOT association: MambaTrack MOT, MambaMOT, MM-Tracker, and SportMamba use Mamba/SSM mainly for motion, trajectory, or detection/association features.
- Multimodal fusion: Mamba-FETrack, MamTrack, MambaEVT, MambaVT, All-Day MCMT, and HyMamba use event, thermal/infrared, language, or hyperspectral inputs rather than plain RGB-only restoration.

## Novelty threat level summary
Novelty threat levels are derived only from each card novelty-threat text plus structured task/modality/restoration fields in the same card.
- high: 5
- medium: 15

High-threat rows in the matrix:
- `2024_ECCV_MambaIR`: MambaIR: A Simple Baseline for Image Restoration with State-Space Model
- `2025_AAAI_MCITrack`: Exploring Enhanced Contextual Information for Video-Level Object Tracking
- `2025_CVPR_MambaIRv2`: MambaIRv2: Attentive State Space Restoration
- `2025_ICASSP_MambaTrack`: MambaTrack: Exploiting Dual-Enhancement for Night UAV Tracking
- `InvTrack`: InvTrack: Efficient Deep Object Tracking Neural Network with Invariant Feature Learning

Medium-threat rows in the matrix:
- `2024_ACM_MambaTrack_MOT`: MambaTrack: A Simple Baseline for Multiple Object Tracking with State Space Model
- `2024_arXiv_Mamba_FETrack`: Mamba-FETrack: Frame-Event Tracking via State Space Model
- `2025_AAAI_MambaLCT`: MambaLCT: Boosting Tracking via Long-term Context State Space Model
- `2025_AAAI_MM_Tracker`: MM-Tracker: Motion Mamba for UAV-platform Multiple Object Tracking
- `2025_AAAI_TemTrack`: Robust Tracking via Mamba-based Context-aware Token Learning
- `2025_ACM_MultiStateTracker`: Multi-State Tracker: Enhancing Efficient Object Tracking via Multi-State Specialization and Interaction
- `2025_arXiv_HyMamba`: Hyperspectral Mamba for Hyperspectral Object Tracking
- `2025_CVPR_All_Day_MCMT`: All-Day Multi-Camera Multi-Target Tracking
- `2025_CVPR_RGBE_MamTrack`: Exploring Historical Information for RGBE Visual Tracking with Mamba
- `2025_CVPRW_SportMamba`: SportMamba: Adaptive Non-Linear Multi-Object Tracking with State Space Models for Team Sports
- `2025_ICASSP_MambaMOT`: MambaMOT: State-Space Model as Motion Predictor for Multi-Object Tracking
- `2025_IEEE_Transaction_MambaVT`: MambaVT: Spatio-Temporal Contextual Modeling for Robust RGB-T Tracking
- `2025_IROS_MambaNUT`: MambaNUT: Nighttime UAV Tracking via Mamba-based Adaptive Curriculum Learning
- `2026_IEEE_Transaction_MambaEVT`: MambaEVT: Event Stream-Based Visual Object Tracking Using State Space Model
- `2026_IEEE_Transaction_SMTrack`: SMTrack: State-Aware Mamba for Efficient Temporal Modeling in Visual Tracking

## Important caution
The matrix is an evidence organization artifact only. It does not rank or propose research gaps, and cells marked `not reported` should not be interpreted as negative findings beyond the paper-card evidence.
