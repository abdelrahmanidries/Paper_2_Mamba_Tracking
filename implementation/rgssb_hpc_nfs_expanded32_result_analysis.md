# RG-SSB HPC NFS Expanded32 Result Analysis

## 1. Executive summary

Regenerated from corrected normalized-NFS rows in `experiments/baseline_results.csv`. NFS annotations are aligned canonical XYWH; old XYXY-as-XYWH NFS outputs are superseded. Normalized root: `/speed-scratch/a_idrais/nfs_ostrack_normalized`.

Corrected expanded-NFS average AUC change is `-0.009638` across `128` pairs. Baseline average AUC is `0.681149`, RG-SSB average AUC is `0.671511`. Counts: `18` gains, `87` neutral, `23` drops. NaN center-error changes: `0`.

## 2. Expanded NFS technical status

- 32 sequences x 4 conditions = 128 corrected matched pairs.
- The invalid historical archive contains 256 rows.
- The old invalid `nfs_cheetah` low-resolution large-drop value is not present in corrected outputs.

## 3. Per-condition result

| condition | baseline AUC | RG-SSB AUC | AUC change | Precision change | center-error change | gains | neutral | drops |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| clean | 0.680741 | 0.679726 | -0.001015 | +0.005024 | +5.389951 | 5 | 23 | 4 |
| motion_blur_medium | 0.677900 | 0.680036 | +0.002136 | +0.009332 | -4.892959 | 5 | 22 | 5 |
| low_resolution_medium | 0.685388 | 0.651750 | -0.033638 | -0.032953 | +13.799242 | 3 | 20 | 9 |
| gaussian_noise_medium | 0.680570 | 0.674533 | -0.006037 | -0.009151 | +0.526014 | 5 | 22 | 5 |

## 4. Per-sequence result

| sequence | baseline AUC | RG-SSB AUC | AUC change | gains | neutral | drops |
| --- | --- | --- | --- | --- | --- | --- |
| nfs_bowling_1 | 0.802422 | 0.665507 | -0.136915 | 2 | 1 | 1 |
| nfs_Gymnastics | 0.447206 | 0.365288 | -0.081919 | 0 | 2 | 2 |
| nfs_running | 0.628830 | 0.590202 | -0.038628 | 0 | 0 | 4 |
| nfs_person_scooter | 0.766080 | 0.728364 | -0.037716 | 0 | 0 | 4 |
| nfs_motorcross | 0.641406 | 0.614750 | -0.026657 | 0 | 3 | 1 |
| nfs_basketball_player_2 | 0.671370 | 0.649597 | -0.021773 | 1 | 2 | 1 |
| nfs_car_rc_rolling | 0.483073 | 0.461634 | -0.021439 | 0 | 2 | 2 |
| nfs_cheetah | 0.538463 | 0.521477 | -0.016986 | 0 | 2 | 2 |
| nfs_parkour | 0.590986 | 0.579293 | -0.011693 | 2 | 0 | 2 |
| nfs_dog | 0.679287 | 0.668399 | -0.010888 | 0 | 3 | 1 |
| nfs_running_100_m | 0.745018 | 0.735101 | -0.009917 | 0 | 4 | 0 |
| nfs_basketball_player | 0.746317 | 0.736732 | -0.009586 | 0 | 3 | 1 |
| nfs_basketball_1 | 0.756083 | 0.746630 | -0.009453 | 0 | 3 | 1 |
| nfs_biker_all_1 | 0.895842 | 0.887234 | -0.008608 | 0 | 4 | 0 |
| nfs_car_jumping | 0.723447 | 0.715572 | -0.007876 | 0 | 4 | 0 |
| nfs_bottle | 0.835707 | 0.829191 | -0.006516 | 0 | 4 | 0 |
| nfs_car_side | 0.831041 | 0.824991 | -0.006051 | 0 | 4 | 0 |
| nfs_dog_1 | 0.680457 | 0.676126 | -0.004332 | 0 | 4 | 0 |
| nfs_biker_acrobat | 0.846960 | 0.843885 | -0.003075 | 0 | 4 | 0 |
| nfs_walking | 0.923450 | 0.921153 | -0.002297 | 0 | 4 | 0 |
| nfs_car_camaro | 0.735561 | 0.734942 | -0.000619 | 0 | 4 | 0 |
| nfs_bird_2 | 0.716828 | 0.717016 | +0.000187 | 0 | 4 | 0 |
| nfs_car_drifting | 0.846162 | 0.848538 | +0.002375 | 0 | 4 | 0 |
| nfs_car | 0.594526 | 0.597692 | +0.003166 | 0 | 4 | 0 |
| nfs_biker_whole_body | 0.786955 | 0.792759 | +0.005803 | 0 | 4 | 0 |
| nfs_tiger | 0.698096 | 0.707552 | +0.009456 | 0 | 4 | 0 |
| nfs_helicopter | 0.590586 | 0.600583 | +0.009997 | 1 | 3 | 0 |
| nfs_footbal_skill | 0.462210 | 0.478800 | +0.016590 | 2 | 1 | 1 |
| nfs_soccer_player_2 | 0.485867 | 0.507296 | +0.021428 | 1 | 3 | 0 |
| nfs_soccer_ball_2 | 0.690338 | 0.712716 | +0.022378 | 1 | 3 | 0 |
| nfs_horse_running | 0.717839 | 0.741292 | +0.023453 | 4 | 0 | 0 |
| nfs_drone | 0.238367 | 0.288048 | +0.049681 | 4 | 0 | 0 |

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

## 7. Comparison with previous selected NFS subset

Previous NFS metrics were invalid because raw XYXY annotations were treated as XYWH. Use only corrected normalized-NFS results.

## 8. Cross-benchmark interpretation with OTB and UAV123

OTB and UAV123 are unchanged. Corrected NFS remains mixed/slightly negative and is the current stress benchmark.

## 9. Main conclusion

Corrected expanded NFS is mixed/slightly negative overall.

## 10. Recommended next experiment

Inspect corrected NFS top drops qualitatively.

## 11. What to postpone

New architecture modules and final paper claims.

## 12. Decision

Continue corrected failure inspection before changing training or architecture.
