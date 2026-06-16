# RG-SSB HPC NFS Expanded32 Result Analysis

Inputs:

- `experiments/baseline_results.csv`
- `implementation/nfs_expanded32_evaluation_plan.md`
- `implementation/paper_level_results_summary.md`
- `implementation/rgssb_hpc_nfs_result_analysis.md`
- `implementation/rgssb_hpc_failure_focused_uav_nfs_result_analysis.md`

## 1. Executive summary

The expanded 32-sequence NFS comparison covers `128` sequence-condition pairs. Baseline average AUC is `0.272698`, HPC RG-SSB average AUC is `0.262237`, and the average AUC change is `-0.010461`. Average Precision@20 change is `-0.003138`. Average center-error change is `+8.641516` after ignoring NaN center-error pairs.

The expanded 32-sequence NFS batch is near neutral for HPC RG-SSB by AUC, with sequence-specific gains and drops. The outcome counts are `25` gains, `63` neutral cases, and `40` drops using the `+/-0.02` AUC threshold.

NaN center-error rows preserved in the detailed CSV: `0`. NaN center-error pair changes ignored in averages: `0`.

## 2. Expanded NFS technical status

- Expanded NFS baseline evaluation rows are present in `experiments/baseline_results.csv`.
- Expanded NFS HPC RG-SSB rows are present in `experiments/baseline_results.csv`.
- The analysis uses 32 NFS sequences from `configs/nfs_eval_suite_expanded32_ostrack.json`.
- Four conditions are analyzed: clean, motion blur medium, low resolution medium, and Gaussian noise medium.
- NFS aligned-annotation handling is assumed from the evaluation scripts; this report only parses logged metrics.
- CSV logging works for the expanded NFS batch.
- This is stronger NFS evidence than the earlier 8-sequence and 16-sequence subsets, but it is still subset evidence rather than full paper-scale benchmark evidence.

## 3. Per-condition result

| condition | baseline AUC | HPC RG-SSB AUC | AUC change | Precision@20 change | center-error change | gains | neutral | drops |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| clean | 0.272958 | 0.273905 | +0.000946 | -0.000294 | +1.177886 | 7 | 14 | 11 |
| motion_blur_medium | 0.271782 | 0.258834 | -0.012948 | -0.004104 | -0.407968 | 5 | 16 | 11 |
| low_resolution_medium | 0.270241 | 0.250543 | -0.019698 | -0.001277 | +13.688244 | 6 | 15 | 11 |
| gaussian_noise_medium | 0.275808 | 0.265665 | -0.010144 | -0.006875 | +20.107903 | 7 | 18 | 7 |

## 4. Per-sequence result

| sequence | baseline AUC | HPC RG-SSB AUC | AUC change | improved overall | gains | neutral | drops |
| --- | --- | --- | --- | --- | --- | --- | --- |
| nfs_drone | 0.245474 | 0.308876 | +0.063402 | yes | 4 | 0 | 0 |
| nfs_car | 0.084139 | 0.141532 | +0.057392 | yes | 4 | 0 | 0 |
| nfs_dog_1 | 0.349879 | 0.376974 | +0.027095 | yes | 3 | 1 | 0 |
| nfs_Gymnastics | 0.308989 | 0.330950 | +0.021961 | yes | 4 | 0 | 0 |
| nfs_helicopter | 0.065442 | 0.085324 | +0.019882 | yes | 2 | 2 | 0 |
| nfs_soccer_player_2 | 0.323246 | 0.338953 | +0.015706 | yes | 1 | 3 | 0 |
| nfs_car_side | 0.179547 | 0.194078 | +0.014531 | yes | 1 | 3 | 0 |
| nfs_basketball_player_2 | 0.382508 | 0.390976 | +0.008468 | yes | 1 | 3 | 0 |
| nfs_bird_2 | 0.258398 | 0.266151 | +0.007753 | yes | 1 | 3 | 0 |
| nfs_horse_running | 0.191342 | 0.196043 | +0.004701 | yes | 0 | 4 | 0 |
| nfs_basketball_1 | 0.133576 | 0.134374 | +0.000799 | yes | 0 | 4 | 0 |
| nfs_running | 0.484513 | 0.484695 | +0.000183 | yes | 1 | 3 | 0 |
| nfs_car_jumping | 0.125225 | 0.124775 | -0.000450 | no | 1 | 2 | 1 |
| nfs_footbal_skill | 0.091508 | 0.090545 | -0.000964 | no | 0 | 4 | 0 |
| nfs_basketball_player | 0.348265 | 0.345662 | -0.002603 | no | 0 | 4 | 0 |
| nfs_bowling_1 | 0.181199 | 0.177082 | -0.004117 | no | 0 | 4 | 0 |
| nfs_parkour | 0.166951 | 0.162555 | -0.004396 | no | 1 | 1 | 2 |
| nfs_dog | 0.425101 | 0.418773 | -0.006328 | no | 0 | 4 | 0 |
| nfs_biker_all_1 | 0.132108 | 0.123237 | -0.008871 | no | 0 | 3 | 1 |
| nfs_car_rc_rolling | 0.085236 | 0.074098 | -0.011138 | no | 0 | 3 | 1 |
| nfs_biker_whole_body | 0.190512 | 0.179295 | -0.011216 | no | 0 | 4 | 0 |
| nfs_tiger | 0.372948 | 0.351073 | -0.021875 | no | 0 | 1 | 3 |
| nfs_soccer_ball_2 | 0.276436 | 0.254175 | -0.022261 | no | 0 | 1 | 3 |
| nfs_bottle | 0.373810 | 0.346372 | -0.027437 | no | 0 | 0 | 4 |
| nfs_running_100_m | 0.272444 | 0.239554 | -0.032890 | no | 0 | 1 | 3 |
| nfs_motorcross | 0.325146 | 0.289922 | -0.035224 | no | 0 | 1 | 3 |
| nfs_car_drifting | 0.162393 | 0.122561 | -0.039833 | no | 0 | 0 | 4 |
| nfs_biker_acrobat | 0.349919 | 0.306292 | -0.043626 | no | 0 | 1 | 3 |
| nfs_person_scooter | 0.365437 | 0.320955 | -0.044482 | no | 0 | 0 | 4 |
| nfs_car_camaro | 0.425193 | 0.353204 | -0.071989 | no | 0 | 0 | 4 |
| nfs_walking | 0.358665 | 0.286464 | -0.072201 | no | 1 | 1 | 2 |
| nfs_cheetah | 0.690772 | 0.576051 | -0.114721 | no | 0 | 2 | 2 |

## 5. Strongest gains

| sequence | condition | baseline AUC | HPC RG-SSB AUC | AUC change | Precision@20 change | center-error change |
| --- | --- | --- | --- | --- | --- | --- |
| nfs_walking | clean | 0.222442 | 0.367193 | +0.144751 | +0.010810 | -54.278015 |
| nfs_parkour | motion_blur_medium | 0.099351 | 0.198020 | +0.098669 | +0.000000 | -172.371765 |
| nfs_drone | motion_blur_medium | 0.248939 | 0.335502 | +0.086563 | -0.028571 | +37.552597 |
| nfs_drone | low_resolution_medium | 0.239887 | 0.310891 | +0.071004 | -0.014285 | +45.939636 |
| nfs_drone | clean | 0.246959 | 0.314710 | +0.067751 | +0.000000 | +36.787628 |
| nfs_car | clean | 0.091658 | 0.157460 | +0.065802 | +0.000000 | -112.925965 |
| nfs_car_jumping | clean | 0.125563 | 0.184068 | +0.058505 | +0.000000 | -45.851288 |
| nfs_car | motion_blur_medium | 0.079914 | 0.136663 | +0.056749 | +0.000000 | -139.422364 |
| nfs_car | low_resolution_medium | 0.091089 | 0.146505 | +0.055416 | +0.000000 | -83.351990 |
| nfs_car | gaussian_noise_medium | 0.073895 | 0.125498 | +0.051603 | +0.000000 | -347.725677 |

## 6. Largest drops

| sequence | condition | baseline AUC | HPC RG-SSB AUC | AUC change | Precision@20 change | center-error change |
| --- | --- | --- | --- | --- | --- | --- |
| nfs_cheetah | low_resolution_medium | 0.701785 | 0.297919 | -0.403866 | -0.011976 | +134.532310 |
| nfs_walking | gaussian_noise_medium | 0.584444 | 0.300009 | -0.284435 | -0.064864 | +92.845772 |
| nfs_walking | motion_blur_medium | 0.404799 | 0.239247 | -0.165552 | -0.014415 | +48.305969 |
| nfs_car_camaro | low_resolution_medium | 0.455171 | 0.374312 | -0.080859 | +0.027778 | +98.771209 |
| nfs_car_camaro | motion_blur_medium | 0.432068 | 0.353135 | -0.078933 | -0.027777 | +95.052643 |
| nfs_biker_acrobat | motion_blur_medium | 0.336324 | 0.261061 | -0.075263 | -0.007813 | +11.286178 |
| nfs_car_camaro | clean | 0.446920 | 0.372937 | -0.073983 | +0.027778 | +94.163818 |
| nfs_running_100_m | motion_blur_medium | 0.266251 | 0.192516 | -0.073735 | -0.003195 | +81.261902 |
| nfs_parkour | low_resolution_medium | 0.236258 | 0.165756 | -0.070502 | +0.000000 | +185.631714 |
| nfs_biker_acrobat | low_resolution_medium | 0.348855 | 0.284731 | -0.064124 | -0.015626 | +1.449890 |

## 7. Comparison with previous selected NFS subset

The first 16 expanded32 NFS sequences correspond to the earlier failure-focused NFS set. Their average AUC change is `-0.014195` across `64` pairs. The 16 newly added sequences have average AUC change `-0.006727` across `64` pairs.

This means the expanded NFS result should be read as confirming the earlier negative/mixed trend.

## 8. Cross-benchmark interpretation with OTB and UAV123

- `OTB` paper-level summary average AUC change: `+0.033144`.
- `UAV123` paper-level summary average AUC change: `+0.017405`.
- `NFS` paper-level summary average AUC change: `-0.014195`.

The expanded NFS result remains the key stress test for the current method because NFS contains fast motion, sports/action sequences, small objects, and high-frame-rate sampling behavior. A positive OTB result alone is not enough to claim broad robustness; the NFS result shows that transfer remains sequence- and condition-dependent.

## 9. Main conclusion

The expanded 32-sequence NFS batch is near neutral for HPC RG-SSB by AUC, with sequence-specific gains and drops. The current HPC RG-SSB lambda `0.02` checkpoint should not be described as uniformly robust on NFS. It has clear wins on some sequence-condition pairs, but the expanded result indicates that NFS behavior is still mixed and should be inspected before changing architecture.

## 10. Recommended next experiment

Options considered:

- A. Evaluate the remaining NFS sequences or move toward full NFS coverage.
- B. Run qualitative failure inspection on the largest NFS drops.
- C. Run longer HPC training.
- D. Add target-region feature consistency again.
- E. Add response consistency again.
- F. Add new architecture modules.

Recommended next experiment: **Prioritize NFS failure inspection and consider training/data refinements before adding new architecture modules.** This recommendation is based only on the parsed results.

## 11. What to postpone

- degradation token
- template-guided scan
- memory update
- response fusion
- final paper claims
- new architecture modules before qualitative failure inspection

## 12. Decision

Decision: **continue NFS failure analysis before revising training or architecture**.

## Final detailed table

| sequence | condition | baseline AUC | HPC RG-SSB AUC | AUC change | best model | outcome |
| --- | --- | --- | --- | --- | --- | --- |
| nfs_Gymnastics | clean | 0.311558 | 0.334912 | +0.023354 | hpc_rgssb | gain |
| nfs_Gymnastics | motion_blur_medium | 0.313038 | 0.333244 | +0.020206 | hpc_rgssb | gain |
| nfs_Gymnastics | low_resolution_medium | 0.311558 | 0.334992 | +0.023434 | hpc_rgssb | gain |
| nfs_Gymnastics | gaussian_noise_medium | 0.299801 | 0.320652 | +0.020851 | hpc_rgssb | gain |
| nfs_basketball_player | clean | 0.338378 | 0.338163 | -0.000215 | baseline | neutral |
| nfs_basketball_player | motion_blur_medium | 0.331777 | 0.328289 | -0.003488 | baseline | neutral |
| nfs_basketball_player | low_resolution_medium | 0.339424 | 0.327645 | -0.011779 | baseline | neutral |
| nfs_basketball_player | gaussian_noise_medium | 0.383482 | 0.388553 | +0.005071 | hpc_rgssb | neutral |
| nfs_car | clean | 0.091658 | 0.157460 | +0.065802 | hpc_rgssb | gain |
| nfs_car | motion_blur_medium | 0.079914 | 0.136663 | +0.056749 | hpc_rgssb | gain |
| nfs_car | low_resolution_medium | 0.091089 | 0.146505 | +0.055416 | hpc_rgssb | gain |
| nfs_car | gaussian_noise_medium | 0.073895 | 0.125498 | +0.051603 | hpc_rgssb | gain |
| nfs_dog | clean | 0.419264 | 0.414563 | -0.004701 | baseline | neutral |
| nfs_dog | motion_blur_medium | 0.432145 | 0.417860 | -0.014285 | baseline | neutral |
| nfs_dog | low_resolution_medium | 0.419168 | 0.414390 | -0.004778 | baseline | neutral |
| nfs_dog | gaussian_noise_medium | 0.429828 | 0.428280 | -0.001548 | baseline | neutral |
| nfs_running | clean | 0.483116 | 0.480878 | -0.002238 | baseline | neutral |
| nfs_running | motion_blur_medium | 0.484681 | 0.474253 | -0.010428 | baseline | neutral |
| nfs_running | low_resolution_medium | 0.482589 | 0.471372 | -0.011217 | baseline | neutral |
| nfs_running | gaussian_noise_medium | 0.487664 | 0.512278 | +0.024614 | hpc_rgssb | gain |
| nfs_bottle | clean | 0.368912 | 0.340264 | -0.028648 | baseline | drop |
| nfs_bottle | motion_blur_medium | 0.367636 | 0.337726 | -0.029910 | baseline | drop |
| nfs_bottle | low_resolution_medium | 0.368149 | 0.338526 | -0.029623 | baseline | drop |
| nfs_bottle | gaussian_noise_medium | 0.390541 | 0.368973 | -0.021568 | baseline | drop |
| nfs_bird_2 | clean | 0.252434 | 0.259360 | +0.006926 | hpc_rgssb | neutral |
| nfs_bird_2 | motion_blur_medium | 0.253682 | 0.272964 | +0.019282 | hpc_rgssb | neutral |
| nfs_bird_2 | low_resolution_medium | 0.250957 | 0.272007 | +0.021050 | hpc_rgssb | gain |
| nfs_bird_2 | gaussian_noise_medium | 0.276521 | 0.260275 | -0.016246 | baseline | neutral |
| nfs_walking | clean | 0.222442 | 0.367193 | +0.144751 | hpc_rgssb | gain |
| nfs_walking | motion_blur_medium | 0.404799 | 0.239247 | -0.165552 | baseline | drop |
| nfs_walking | low_resolution_medium | 0.222977 | 0.239408 | +0.016431 | hpc_rgssb | neutral |
| nfs_walking | gaussian_noise_medium | 0.584444 | 0.300009 | -0.284435 | baseline | drop |
| nfs_basketball_player_2 | clean | 0.395043 | 0.396991 | +0.001948 | hpc_rgssb | neutral |
| nfs_basketball_player_2 | motion_blur_medium | 0.394726 | 0.383941 | -0.010785 | baseline | neutral |
| nfs_basketball_player_2 | low_resolution_medium | 0.398056 | 0.397558 | -0.000498 | baseline | neutral |
| nfs_basketball_player_2 | gaussian_noise_medium | 0.342207 | 0.385414 | +0.043207 | hpc_rgssb | gain |
| nfs_car_drifting | clean | 0.157157 | 0.114348 | -0.042809 | baseline | drop |
| nfs_car_drifting | motion_blur_medium | 0.161048 | 0.110742 | -0.050306 | baseline | drop |
| nfs_car_drifting | low_resolution_medium | 0.151262 | 0.111944 | -0.039318 | baseline | drop |
| nfs_car_drifting | gaussian_noise_medium | 0.180106 | 0.153208 | -0.026898 | baseline | drop |
| nfs_car_jumping | clean | 0.125563 | 0.184068 | +0.058505 | hpc_rgssb | gain |
| nfs_car_jumping | motion_blur_medium | 0.117912 | 0.120612 | +0.002700 | hpc_rgssb | neutral |
| nfs_car_jumping | low_resolution_medium | 0.125113 | 0.125113 | +0.000000 | tie | neutral |
| nfs_car_jumping | gaussian_noise_medium | 0.132313 | 0.069307 | -0.063006 | baseline | drop |
| nfs_cheetah | clean | 0.697634 | 0.684058 | -0.013576 | baseline | neutral |
| nfs_cheetah | motion_blur_medium | 0.707773 | 0.676172 | -0.031601 | baseline | drop |
| nfs_cheetah | low_resolution_medium | 0.701785 | 0.297919 | -0.403866 | baseline | drop |
| nfs_cheetah | gaussian_noise_medium | 0.655896 | 0.646054 | -0.009842 | baseline | neutral |
| nfs_horse_running | clean | 0.150723 | 0.153786 | +0.003063 | hpc_rgssb | neutral |
| nfs_horse_running | motion_blur_medium | 0.150581 | 0.154854 | +0.004273 | hpc_rgssb | neutral |
| nfs_horse_running | low_resolution_medium | 0.145594 | 0.154427 | +0.008833 | hpc_rgssb | neutral |
| nfs_horse_running | gaussian_noise_medium | 0.318470 | 0.321105 | +0.002635 | hpc_rgssb | neutral |
| nfs_motorcross | clean | 0.325717 | 0.301346 | -0.024371 | baseline | drop |
| nfs_motorcross | motion_blur_medium | 0.325463 | 0.279259 | -0.046204 | baseline | drop |
| nfs_motorcross | low_resolution_medium | 0.337395 | 0.285352 | -0.052043 | baseline | drop |
| nfs_motorcross | gaussian_noise_medium | 0.312008 | 0.293729 | -0.018279 | baseline | neutral |
| nfs_person_scooter | clean | 0.363484 | 0.316808 | -0.046676 | baseline | drop |
| nfs_person_scooter | motion_blur_medium | 0.366504 | 0.313427 | -0.053077 | baseline | drop |
| nfs_person_scooter | low_resolution_medium | 0.375015 | 0.335243 | -0.039772 | baseline | drop |
| nfs_person_scooter | gaussian_noise_medium | 0.356747 | 0.318342 | -0.038405 | baseline | drop |
| nfs_soccer_player_2 | clean | 0.314893 | 0.330693 | +0.015800 | hpc_rgssb | neutral |
| nfs_soccer_player_2 | motion_blur_medium | 0.309349 | 0.313434 | +0.004085 | hpc_rgssb | neutral |
| nfs_soccer_player_2 | low_resolution_medium | 0.313330 | 0.329151 | +0.015821 | hpc_rgssb | neutral |
| nfs_soccer_player_2 | gaussian_noise_medium | 0.355414 | 0.382533 | +0.027119 | hpc_rgssb | gain |
| nfs_basketball_1 | clean | 0.134225 | 0.140615 | +0.006390 | hpc_rgssb | neutral |
| nfs_basketball_1 | motion_blur_medium | 0.144267 | 0.136016 | -0.008251 | baseline | neutral |
| nfs_basketball_1 | low_resolution_medium | 0.133382 | 0.137174 | +0.003792 | hpc_rgssb | neutral |
| nfs_basketball_1 | gaussian_noise_medium | 0.122428 | 0.123692 | +0.001264 | hpc_rgssb | neutral |
| nfs_biker_acrobat | clean | 0.347153 | 0.320390 | -0.026763 | baseline | drop |
| nfs_biker_acrobat | motion_blur_medium | 0.336324 | 0.261061 | -0.075263 | baseline | drop |
| nfs_biker_acrobat | low_resolution_medium | 0.348855 | 0.284731 | -0.064124 | baseline | drop |
| nfs_biker_acrobat | gaussian_noise_medium | 0.367342 | 0.358988 | -0.008354 | baseline | neutral |
| nfs_biker_all_1 | clean | 0.149566 | 0.127661 | -0.021905 | baseline | drop |
| nfs_biker_all_1 | motion_blur_medium | 0.124507 | 0.121879 | -0.002628 | baseline | neutral |
| nfs_biker_all_1 | low_resolution_medium | 0.125559 | 0.125559 | +0.000000 | tie | neutral |
| nfs_biker_all_1 | gaussian_noise_medium | 0.128800 | 0.117848 | -0.010952 | baseline | neutral |
| nfs_biker_whole_body | clean | 0.182718 | 0.165963 | -0.016755 | baseline | neutral |
| nfs_biker_whole_body | motion_blur_medium | 0.189625 | 0.182182 | -0.007443 | baseline | neutral |
| nfs_biker_whole_body | low_resolution_medium | 0.185799 | 0.168334 | -0.017465 | baseline | neutral |
| nfs_biker_whole_body | gaussian_noise_medium | 0.203905 | 0.200703 | -0.003202 | baseline | neutral |
| nfs_bowling_1 | clean | 0.186877 | 0.181551 | -0.005326 | baseline | neutral |
| nfs_bowling_1 | motion_blur_medium | 0.176355 | 0.174754 | -0.001601 | baseline | neutral |
| nfs_bowling_1 | low_resolution_medium | 0.186648 | 0.180930 | -0.005718 | baseline | neutral |
| nfs_bowling_1 | gaussian_noise_medium | 0.174917 | 0.171094 | -0.003823 | baseline | neutral |
| nfs_car_camaro | clean | 0.446920 | 0.372937 | -0.073983 | baseline | drop |
| nfs_car_camaro | motion_blur_medium | 0.432068 | 0.353135 | -0.078933 | baseline | drop |
| nfs_car_camaro | low_resolution_medium | 0.455171 | 0.374312 | -0.080859 | baseline | drop |
| nfs_car_camaro | gaussian_noise_medium | 0.366612 | 0.312431 | -0.054181 | baseline | drop |
| nfs_car_rc_rolling | clean | 0.085755 | 0.078889 | -0.006866 | baseline | neutral |
| nfs_car_rc_rolling | motion_blur_medium | 0.085117 | 0.068668 | -0.016449 | baseline | neutral |
| nfs_car_rc_rolling | low_resolution_medium | 0.084158 | 0.086873 | +0.002715 | hpc_rgssb | neutral |
| nfs_car_rc_rolling | gaussian_noise_medium | 0.085915 | 0.061961 | -0.023954 | baseline | drop |
| nfs_car_side | clean | 0.177484 | 0.185185 | +0.007701 | hpc_rgssb | neutral |
| nfs_car_side | motion_blur_medium | 0.182985 | 0.181335 | -0.001650 | baseline | neutral |
| nfs_car_side | low_resolution_medium | 0.182618 | 0.188119 | +0.005501 | hpc_rgssb | neutral |
| nfs_car_side | gaussian_noise_medium | 0.175101 | 0.221672 | +0.046571 | hpc_rgssb | gain |
| nfs_dog_1 | clean | 0.349717 | 0.389675 | +0.039958 | hpc_rgssb | gain |
| nfs_dog_1 | motion_blur_medium | 0.364745 | 0.385608 | +0.020863 | hpc_rgssb | gain |
| nfs_dog_1 | low_resolution_medium | 0.349540 | 0.385608 | +0.036068 | hpc_rgssb | gain |
| nfs_dog_1 | gaussian_noise_medium | 0.335514 | 0.347006 | +0.011492 | hpc_rgssb | neutral |
| nfs_drone | clean | 0.246959 | 0.314710 | +0.067751 | hpc_rgssb | gain |
| nfs_drone | motion_blur_medium | 0.248939 | 0.335502 | +0.086563 | hpc_rgssb | gain |
| nfs_drone | low_resolution_medium | 0.239887 | 0.310891 | +0.071004 | hpc_rgssb | gain |
| nfs_drone | gaussian_noise_medium | 0.246110 | 0.274399 | +0.028289 | hpc_rgssb | gain |
| nfs_footbal_skill | clean | 0.093115 | 0.091301 | -0.001814 | baseline | neutral |
| nfs_footbal_skill | motion_blur_medium | 0.089184 | 0.087446 | -0.001738 | baseline | neutral |
| nfs_footbal_skill | low_resolution_medium | 0.092737 | 0.092434 | -0.000303 | baseline | neutral |
| nfs_footbal_skill | gaussian_noise_medium | 0.090998 | 0.090998 | +0.000000 | tie | neutral |
| nfs_helicopter | clean | 0.069211 | 0.100383 | +0.031172 | hpc_rgssb | gain |
| nfs_helicopter | motion_blur_medium | 0.067486 | 0.087225 | +0.019739 | hpc_rgssb | neutral |
| nfs_helicopter | low_resolution_medium | 0.057011 | 0.090802 | +0.033791 | hpc_rgssb | gain |
| nfs_helicopter | gaussian_noise_medium | 0.068061 | 0.062887 | -0.005174 | baseline | neutral |
| nfs_parkour | clean | 0.289177 | 0.235063 | -0.054114 | baseline | drop |
| nfs_parkour | motion_blur_medium | 0.099351 | 0.198020 | +0.098669 | hpc_rgssb | gain |
| nfs_parkour | low_resolution_medium | 0.236258 | 0.165756 | -0.070502 | baseline | drop |
| nfs_parkour | gaussian_noise_medium | 0.043018 | 0.051383 | +0.008365 | hpc_rgssb | neutral |
| nfs_running_100_m | clean | 0.286275 | 0.265239 | -0.021036 | baseline | drop |
| nfs_running_100_m | motion_blur_medium | 0.266251 | 0.192516 | -0.073735 | baseline | drop |
| nfs_running_100_m | low_resolution_medium | 0.270332 | 0.226078 | -0.044254 | baseline | drop |
| nfs_running_100_m | gaussian_noise_medium | 0.266916 | 0.274381 | +0.007465 | hpc_rgssb | neutral |
| nfs_soccer_ball_2 | clean | 0.295084 | 0.266559 | -0.028525 | baseline | drop |
| nfs_soccer_ball_2 | motion_blur_medium | 0.280642 | 0.253735 | -0.026907 | baseline | drop |
| nfs_soccer_ball_2 | low_resolution_medium | 0.288368 | 0.261035 | -0.027333 | baseline | drop |
| nfs_soccer_ball_2 | gaussian_noise_medium | 0.241648 | 0.235371 | -0.006277 | baseline | neutral |
| nfs_tiger | clean | 0.376454 | 0.353941 | -0.022513 | baseline | drop |
| nfs_tiger | motion_blur_medium | 0.408161 | 0.370918 | -0.037243 | baseline | drop |
| nfs_tiger | low_resolution_medium | 0.377930 | 0.357186 | -0.020744 | baseline | drop |
| nfs_tiger | gaussian_noise_medium | 0.329246 | 0.322247 | -0.006999 | baseline | neutral |

## Verification

- Parsed `experiments/baseline_results.csv` with Python.
- Used all 32 sequences from `configs/nfs_eval_suite_expanded32_ostrack.json`.
- Created `experiments/rgssb_hpc_nfs_expanded32_comparison.csv`.
- Created `implementation/rgssb_hpc_nfs_expanded32_result_analysis.md`.
- Compared `128` sequence-condition pairs with one baseline row and one HPC RG-SSB row per pair.
- Preserved NaN center-error values in the detailed CSV and ignored NaN pairwise center-error changes in averages.
- Did not run OSTrack.
- Did not run training or evaluation.
- Did not modify datasets or `external/OSTrack`.

Uncertain fields:

- Each degraded condition uses one seed, `42`.
- Each degradation uses medium severity only.
- This report is based on 32 selected NFS sequences, not necessarily full NFS coverage.
- The report compares parsed CSV metrics only and does not inspect qualitative tracking failures.
