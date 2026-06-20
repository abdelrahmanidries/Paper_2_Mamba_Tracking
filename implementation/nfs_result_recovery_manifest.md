# NFS Result Recovery Manifest

## Confirmed NFS bug

Aligned NFS XYXY annotations were treated as XYWH. Previous NFS tracking used invalid XYXY boxes as XYWH. NFS tracking was rerun using aligned canonical XYWH annotations from `/speed-scratch/a_idrais/nfs_ostrack_normalized`.

## Commits

- Corrected commit: `eec74d6`
- Archive-repair commit: `819ce0b`

## Invalid row archive

`experiments/invalid_nfs_rows_before_xyxy_fix.csv` contains `256` invalid historical rows: 128 baseline rows and 128 HPC RG-SSB rows.

## Corrected active NFS row count

`experiments/baseline_results.csv` contains 256 corrected active NFS rows: 128 baseline and 128 HPC RG-SSB.

## Anchor-row verification

- Baseline `nfs_cheetah low_resolution medium seed 42`: AUC `0.519832`, mean IoU `0.519185`.
- HPC RG-SSB `nfs_cheetah low_resolution medium seed 42`: AUC `0.516986`, mean IoU `0.516131`.
- Corrected first prediction was independently verified on Speed as canonical XYWH: `525,286,420,230`.

## Normalized annotation rule

Raw NFS XYXY rows are aligned to sampled frames and converted to canonical XYWH. Example: `[525, 286, 945, 516] -> [525, 286, 420, 230]`.

## Regenerated artifacts

1. `experiments/rgssb_hpc_nfs_comparison.csv`
2. `implementation/rgssb_hpc_nfs_result_analysis.md`
3. `experiments/rgssb_hpc_nfs_expanded32_comparison.csv`
4. `implementation/rgssb_hpc_nfs_expanded32_result_analysis.md`
5. `experiments/rgssb_hpc_failure_focused_uav_nfs_comparison.csv`
6. `implementation/rgssb_hpc_failure_focused_uav_nfs_result_analysis.md`
7. `experiments/rgssb_hpc_cross_benchmark_failure_inspection.csv`
8. `implementation/rgssb_hpc_cross_benchmark_failure_inspection.md`
9. `experiments/rgssb_current_method_evidence_summary.csv`
10. `implementation/rgssb_current_method_evidence_summary.md`
11. `experiments/paper_level_result_table_current.csv`
12. `experiments/paper_level_benchmark_summary.csv`
13. `implementation/paper_level_results_summary.md`
14. `implementation/paper_level_risk_and_claims.md`
15. `configs/nfs_failure_cases_to_inspect.json`

## Superseded artifacts

Old NFS qualitative diagnostics and overlays under `outputs/failure_inspection/` are superseded. Old NFS comparison CSVs and NFS-dependent reports before this regeneration are superseded.

## Unchanged OTB/UAV123 artifacts

OTB and UAV123 numeric results are unchanged and were not recomputed from stale NFS artifacts.

## Corrected NFS averages

Expanded32 NFS average AUC change: `-0.009638`.

| condition | baseline AUC | RG-SSB AUC | AUC change | Precision change | center-error change | gains | neutral | drops |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| clean | 0.680741 | 0.679726 | -0.001015 | +0.005024 | +5.389951 | 5 | 23 | 4 |
| motion_blur_medium | 0.677900 | 0.680036 | +0.002136 | +0.009332 | -4.892959 | 5 | 22 | 5 |
| low_resolution_medium | 0.685388 | 0.651750 | -0.033638 | -0.032953 | +13.799242 | 3 | 20 | 9 |
| gaussian_noise_medium | 0.680570 | 0.674533 | -0.006037 | -0.009151 | +0.526014 | 5 | 22 | 5 |

## Revised cross-benchmark conclusion

| benchmark | pairs | baseline AUC | RG-SSB AUC | AUC change | gains | neutral | drops |
| --- | --- | --- | --- | --- | --- | --- | --- |
| OTB | 52 | 0.646964 | 0.680108 | +0.033144 | 16 | 31 | 5 |
| UAV123 | 64 | 0.660183 | 0.677587 | +0.017405 | 9 | 49 | 6 |
| NFS | 128 | 0.681149 | 0.671511 | -0.009638 | 18 | 87 | 23 |

## Newly selected qualitative failure cases

| sequence | condition | baseline AUC | RG-SSB AUC | AUC change |
| --- | --- | --- | --- | --- |
| nfs_bowling_1 | low_resolution_medium | 0.802960 | 0.204882 | -0.598078 |
| nfs_Gymnastics | low_resolution_medium | 0.439706 | 0.243946 | -0.195760 |
| nfs_Gymnastics | gaussian_noise_medium | 0.457356 | 0.289954 | -0.167402 |
| nfs_basketball_player_2 | gaussian_noise_medium | 0.747717 | 0.621882 | -0.125835 |
| nfs_parkour | low_resolution_medium | 0.678559 | 0.563674 | -0.114885 |
| nfs_motorcross | low_resolution_medium | 0.690023 | 0.615638 | -0.074385 |
| nfs_running | motion_blur_medium | 0.636471 | 0.572707 | -0.063764 |
| nfs_person_scooter | motion_blur_medium | 0.782849 | 0.728766 | -0.054083 |
| nfs_footbal_skill | low_resolution_medium | 0.485375 | 0.432394 | -0.052981 |
| nfs_car_rc_rolling | clean | 0.509422 | 0.469179 | -0.040243 |

## Provenance warning for paper tables

Paper tables must cite corrected normalized-NFS results only. Pre-fix NFS rows in the invalid archive are provenance records and must not be used as evidence.
