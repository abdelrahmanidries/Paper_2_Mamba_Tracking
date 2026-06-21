# Paper Freeze V1 Manifest

## 1. Frozen Method

Paper Freeze V1 freezes the current defensible fallback method:

- Tracker: OSTrack + RG-SSB + box head.
- Backbone: frozen.
- Trainable groups: `rgssb.*` and `box_head.*`.
- Training data: degradation-aware LaSOT.
- Feature consistency: global clean/degraded feature consistency.
- Feature-consistency weight: `lambda = 0.02`.
- Response consistency: disabled.
- Target-region consistency: disabled.
- HPC config: `vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_degraded_hpc_featcons_lam002`.

This freeze does not add degradation tokens, template-guided scan, memory update, response fusion, or other new architecture modules.

## 2. Authoritative Result Files

Current numeric claims must come from:

- `experiments/baseline_results.csv`
- `experiments/rgssb_hpc_broader_otb_comparison.csv`
- `experiments/rgssb_hpc_nfs_expanded32_comparison.csv`
- `experiments/rgssb_hpc_failure_focused_uav_nfs_comparison.csv`
- `experiments/rgssb_hpc_cross_benchmark_failure_inspection.csv`
- `experiments/paper_level_result_table_current.csv`
- `experiments/paper_level_benchmark_summary.csv`
- `experiments/nfs_corrected_drift_onset_analysis.csv`
- `experiments/paper_claim_traceability.csv`

Historical/provenance-only archive:

- `experiments/invalid_nfs_rows_before_xyxy_fix.csv`

## 3. Corrected NFS Provenance

The old NFS metrics were invalid because aligned NFS XYXY annotations were treated as XYWH. Those rows are archived in `experiments/invalid_nfs_rows_before_xyxy_fix.csv` and must not be used for current paper claims, tables, or figures.

Corrected NFS tracking was rerun using normalized aligned canonical XYWH annotations. Mandatory corrected anchors:

- Invalid historical NFS rows archived: `256`.
- Corrected active NFS rows in `experiments/baseline_results.csv`: `256`.
- Corrected expanded NFS comparison pairs: `128`.
- Corrected `nfs_cheetah` low-resolution baseline AUC: `0.519832`.
- Corrected `nfs_cheetah` low-resolution RG-SSB AUC: `0.516986`.
- Corrected expanded NFS average AUC change: `-0.009638`.

Old invalid NFS qualitative overlays and diagnostics are superseded.

## 4. Benchmark Scope

Current Paper Freeze V1 scope:

| benchmark | sequences | conditions | pairs | average AUC change |
| --- | ---: | ---: | ---: | ---: |
| broader OTB | 13 | 4 | 52 | +0.033144 |
| expanded UAV123 | 16 | 4 | 64 | +0.017405 |
| corrected expanded NFS | 32 | 4 | 128 | -0.009638 |

The 244-pair paper-level table average is `+0.006572`. The corrected cross-benchmark failure-inspection aggregate has a separate 212-pair scope and average AUC change `+0.001478`.

Evaluation conditions:

- clean
- motion_blur medium, seed 42
- low_resolution medium, seed 42
- gaussian_noise medium, seed 42

## 5. Completed Ablations

Completed or analyzed ablations include:

- RG-SSB-only local smoke tests.
- RG-SSB + head local training.
- Fully degraded 3000-sample local setup.
- Balanced clean/degraded 3000-sample local setup.
- Feature consistency lambda sweep: `0.02`, `0.05`, `0.10`.
- Feature consistency + response consistency.
- Target-region feature consistency.
- HPC-scale lambda `0.02` global feature-consistency setup.

## 6. Rejected Ablations

Rejected for Paper Freeze V1:

- Response consistency: not retained after local comparison.
- Target-region feature consistency: not retained after local comparison.
- Balanced clean/degraded training: not selected over current global feature-consistency setup.
- New architecture modules: postponed.

## 7. Current Figures and Tables

Current table assets:

- `experiments/paper_level_result_table_current.csv`
- `experiments/paper_level_benchmark_summary.csv`
- `experiments/paper_claim_traceability.csv`
- `experiments/nfs_corrected_drift_onset_analysis.csv`

Missing figure assets:

- No finalized success/precision plots.
- No final qualitative figure panel from corrected NFS drift analysis.
- No final runtime/FPS table.
- No parameter-count table in paper-ready format.

## 8. Remaining Missing Evidence

- Full benchmark coverage beyond selected subsets.
- Multiple degradation seeds.
- Multiple severities.
- Additional real-world corruption types.
- Runtime/FPS and memory reporting.
- More complete comparison against published trackers.
- Final corrected qualitative figures.

## 9. Reproducibility Status

Automation exists for:

- Experiment-cycle execution.
- Baseline/RG-SSB degradation suites.
- Normalized NFS preparation and verification.
- Corrected NFS analysis regeneration.
- Drift-onset analysis from existing corrected diagnostics.

The safe reproducibility boundary is local/HPC reproduction of the current selected setup, not complete paper-scale reproduction across every public benchmark.

## 10. Safe Fallback Submission Position

Paper Freeze V1 supports a cautious proof-of-concept paper position:

> RG-SSB can be integrated into OSTrack and trained with frozen backbone plus trainable RG-SSB and box head. Under selected synthetic degradation tests, the current global feature-consistency setup improves broader OTB and expanded UAV123 subsets, while corrected NFS remains mixed/slightly negative. The result is promising but not sufficient for state-of-the-art or universal robustness claims.

This is the fallback position if the final gated distractor-aware ablation fails.

## 11. Evidence Status

Final/current evidence:

- Broader OTB `+0.033144`.
- Expanded UAV123 `+0.017405`.
- Corrected expanded NFS `-0.009638`.
- Corrected 212-pair cross-benchmark failure-inspection aggregate `+0.001478`.
- Corrected NFS drift rows: `10`.

Provisional evidence:

- Local small-scale ablation rankings.
- Corrected qualitative drift interpretation until final figures are selected.

Superseded evidence:

- All NFS rows archived in `experiments/invalid_nfs_rows_before_xyxy_fix.csv`.
- Old NFS qualitative overlays generated before normalized aligned XYWH correction.
