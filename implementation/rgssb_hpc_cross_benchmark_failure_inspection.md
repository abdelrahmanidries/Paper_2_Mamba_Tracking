# RG-SSB HPC Cross-Benchmark Failure Inspection

## 1. Executive summary

Regenerated after the normalized aligned XYWH NFS fix. OTB and UAV123 numeric values are unchanged; NFS values are corrected from `baseline_results.csv`. Overall cross-benchmark average AUC change is `+0.001478` across `212` pairs.

## 2. Benchmark-level result

| benchmark | pairs | baseline AUC | RG-SSB AUC | AUC change | gains | neutral | drops |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NFS | 128 | 0.681149 | 0.671511 | -0.009638 | 18 | 87 | 23 |
| OTB | 52 | 0.646964 | 0.680108 | +0.033144 | 16 | 31 | 5 |
| UAV123 | 32 | 0.790494 | 0.784983 | -0.005511 | 1 | 28 | 3 |

## 3. Condition-level result

| condition | baseline AUC | RG-SSB AUC | AUC change | Precision change | center-error change | gains | neutral | drops |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| clean | 0.703351 | 0.705868 | +0.002516 | +0.011597 | +2.741789 | 8 | 39 | 6 |
| motion_blur_medium | 0.671394 | 0.684462 | +0.013068 | +0.019933 | -4.996932 | 14 | 32 | 7 |
| low_resolution_medium | 0.690659 | 0.676136 | -0.014523 | -0.011584 | +7.276453 | 5 | 37 | 11 |
| gaussian_noise_medium | 0.691673 | 0.696526 | +0.004853 | +0.011426 | -0.375647 | 8 | 38 | 7 |

## 4. Strongest gains

| benchmark | sequence | condition | AUC change |
| --- | --- | --- | --- |
| OTB | Walking2 | low_resolution_medium | +0.454515 |
| OTB | Walking2 | gaussian_noise_medium | +0.262792 |
| OTB | Deer | motion_blur_medium | +0.227165 |
| UAV123 | uav_car11 | gaussian_noise_medium | +0.210977 |
| OTB | Deer | low_resolution_medium | +0.171246 |
| OTB | Football | motion_blur_medium | +0.166730 |
| OTB | Deer | clean | +0.153117 |
| NFS | nfs_soccer_player_2 | motion_blur_medium | +0.109328 |
| NFS | nfs_soccer_ball_2 | low_resolution_medium | +0.077888 |
| NFS | nfs_drone | low_resolution_medium | +0.074964 |

## 5. Largest drops

| benchmark | sequence | condition | AUC change |
| --- | --- | --- | --- |
| NFS | nfs_bowling_1 | low_resolution_medium | -0.598078 |
| UAV123 | uav_car11 | low_resolution_medium | -0.250581 |
| NFS | nfs_Gymnastics | low_resolution_medium | -0.195760 |
| NFS | nfs_Gymnastics | gaussian_noise_medium | -0.167402 |
| NFS | nfs_basketball_player_2 | gaussian_noise_medium | -0.125835 |
| NFS | nfs_parkour | low_resolution_medium | -0.114885 |
| NFS | nfs_motorcross | low_resolution_medium | -0.074385 |
| NFS | nfs_running | motion_blur_medium | -0.063764 |
| NFS | nfs_person_scooter | motion_blur_medium | -0.054083 |
| NFS | nfs_footbal_skill | low_resolution_medium | -0.052981 |

## 6. Failure pattern interpretation

NFS is corrected and remains the main stress benchmark. Old NFS qualitative overlays are superseded.

## 7. Recommended next experiment

Corrected NFS qualitative failure inspection.

## 8. What to postpone

New architecture modules and final claims.

## 9. Decision

Continue corrected failure inspection.
