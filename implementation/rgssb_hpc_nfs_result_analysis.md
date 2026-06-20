# RG-SSB HPC NFS Result Analysis

## 1. Executive summary

Regenerated from corrected normalized-NFS rows in `experiments/baseline_results.csv`. NFS annotations were normalized as aligned canonical XYWH; previous NFS tracking used invalid XYXY boxes as XYWH and is superseded. Normalized root: `/speed-scratch/a_idrais/nfs_ostrack_normalized`.

Selected 8-sequence corrected NFS average AUC change: `-0.018310` across `32` pairs. The corrected `nfs_cheetah` low-resolution anchor is baseline AUC `0.519832`, RG-SSB AUC `0.516986`, change `-0.002846`.

## 2. Technical status

NFS tracking was rerun using aligned canonical XYWH annotations. OTB and UAV123 are unaffected. Invalid historical rows are archived in `experiments/invalid_nfs_rows_before_xyxy_fix.csv`.

## 3. Per-condition summary

| condition | baseline AUC | RG-SSB AUC | AUC change | Precision change | center-error change | gains | neutral | drops |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| clean | 0.675091 | 0.668548 | -0.006544 | -0.009462 | -0.375172 | 0 | 7 | 1 |
| motion_blur_medium | 0.716539 | 0.708469 | -0.008069 | -0.001004 | -1.045716 | 0 | 7 | 1 |
| low_resolution_medium | 0.682018 | 0.647714 | -0.034304 | -0.040494 | +9.207933 | 0 | 5 | 3 |
| gaussian_noise_medium | 0.712428 | 0.688106 | -0.024323 | -0.028594 | +7.211646 | 0 | 5 | 3 |

## 4. Per-sequence summary

| sequence | baseline AUC | RG-SSB AUC | AUC change | gains | neutral | drops |
| --- | --- | --- | --- | --- | --- | --- |
| nfs_Gymnastics | 0.447206 | 0.365288 | -0.081919 | 0 | 2 | 2 |
| nfs_running | 0.628830 | 0.590202 | -0.038628 | 0 | 0 | 4 |
| nfs_dog | 0.679287 | 0.668399 | -0.010888 | 0 | 3 | 1 |
| nfs_basketball_player | 0.746317 | 0.736732 | -0.009586 | 0 | 3 | 1 |
| nfs_bottle | 0.835707 | 0.829191 | -0.006516 | 0 | 4 | 0 |
| nfs_walking | 0.923450 | 0.921153 | -0.002297 | 0 | 4 | 0 |
| nfs_bird_2 | 0.716828 | 0.717016 | +0.000187 | 0 | 4 | 0 |
| nfs_car | 0.594526 | 0.597692 | +0.003166 | 0 | 4 | 0 |

## 5. Main finding

The corrected selected NFS subset is mixed and must replace all stale NFS reports.

## 6. Recommended next experiment

Run corrected qualitative NFS failure inspection from the regenerated failure-case config.
