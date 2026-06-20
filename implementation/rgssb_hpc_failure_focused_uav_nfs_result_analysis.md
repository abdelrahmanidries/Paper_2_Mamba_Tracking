# RG-SSB HPC Failure-Focused UAV123/NFS Result Analysis

## 1. Executive summary

Regenerated from corrected normalized-NFS rows. UAV123 values are unchanged; NFS uses aligned canonical XYWH annotations from `/speed-scratch/a_idrais/nfs_ostrack_normalized`. Previous NFS qualitative diagnostics and overlays are superseded.

| benchmark | pairs | baseline AUC | RG-SSB AUC | AUC change | gains | neutral | drops |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NFS | 128 | 0.681149 | 0.671511 | -0.009638 | 18 | 87 | 23 |
| UAV123 | 64 | 0.660183 | 0.677587 | +0.017405 | 9 | 49 | 6 |

## 2. Expanded UAV123 result

Unchanged.

## 3. Expanded NFS result

Corrected from normalized aligned XYWH annotations.

## 4. Condition-level result

| condition | baseline AUC | RG-SSB AUC | AUC change | Precision change | center-error change | gains | neutral | drops |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| clean | 0.685313 | 0.687481 | +0.002169 | +0.009991 | +4.055111 | 6 | 36 | 6 |
| motion_blur_medium | 0.653730 | 0.665815 | +0.012085 | +0.022509 | -7.324327 | 9 | 32 | 7 |
| low_resolution_medium | 0.684138 | 0.661038 | -0.023100 | -0.025265 | +10.307658 | 4 | 33 | 11 |
| gaussian_noise_medium | 0.673462 | 0.679812 | +0.006350 | +0.014245 | +0.410484 | 8 | 35 | 5 |

## 5. Strongest gains

| sequence | condition | baseline AUC | RG-SSB AUC | AUC change |
| --- | --- | --- | --- | --- |
| nfs_soccer_player_2 | motion_blur_medium | 0.505284 | 0.614612 | +0.109328 |
| nfs_soccer_ball_2 | low_resolution_medium | 0.643354 | 0.721242 | +0.077888 |
| nfs_drone | low_resolution_medium | 0.254880 | 0.329844 | +0.074964 |
| nfs_footbal_skill | clean | 0.456957 | 0.519764 | +0.062807 |
| nfs_footbal_skill | motion_blur_medium | 0.416371 | 0.476986 | +0.060615 |
| nfs_helicopter | gaussian_noise_medium | 0.578569 | 0.633504 | +0.054935 |
| nfs_basketball_player_2 | motion_blur_medium | 0.473775 | 0.528128 | +0.054353 |
| nfs_parkour | gaussian_noise_medium | 0.553260 | 0.604131 | +0.050871 |
| nfs_drone | motion_blur_medium | 0.241726 | 0.288967 | +0.047241 |
| nfs_drone | clean | 0.261952 | 0.304526 | +0.042574 |

## 6. Largest drops

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

## 7. Comparison with earlier OTB/UAV123/NFS findings

Earlier NFS findings are superseded; OTB/UAV123 remain valid.

## 8. Main conclusion

Corrected failure-focused transfer remains mixed.

## 9. Recommended next experiment

Corrected NFS qualitative failure inspection.

## 10. What to postpone

New architecture modules and final claims.

## 11. Final decision

Proceed with corrected NFS failure-case inspection.
