# RG-SSB HPC UAV123 Result Analysis

Inputs:

- `experiments/baseline_results.csv`
- `implementation/uav123_hpc_evaluation_plan.md`
- `implementation/rgssb_hpc_broader_otb_result_analysis.md`
- `experiments/rgssb_hpc_broader_otb_comparison.csv`

## 1. Executive summary

The HPC RG-SSB + head feature-consistency lambda `0.02` model does not improve over the original OSTrack baseline on the selected UAV123 subset: baseline average AUC `0.790494`, HPC RG-SSB average AUC `0.784983`, change `-0.005511` across 32 sequence-condition pairs.
Average Precision@20 change is `-0.001949`. Average center-error change is `+0.162469` after ignoring NaN center-error pairs. NaN center-error rows found: `8`; NaN pairwise center-error changes ignored in averages: `4`.

## 2. Technical status

- UAV123 baseline evaluation completed.
- UAV123 HPC RG-SSB evaluation completed.
- 8 sequences and 4 conditions were evaluated.
- 64 rows were added to `experiments/baseline_results.csv`.
- CSV logging works.
- This is cross-benchmark evidence beyond OTB.
- This is still not final paper-scale evidence.

## 3. Per-condition summary

### clean

Average baseline AUC `0.823353`, average HPC RG-SSB AUC `0.816164`, AUC change `-0.007190`. Average Precision@20 change `+0.000624`; average center-error change `+0.173397` after ignoring NaN pairs. On this condition, RG-SSB does not help on average by AUC.

### motion_blur_medium

Average baseline AUC `0.750654`, average HPC RG-SSB AUC `0.751655`, AUC change `+0.001001`. Average Precision@20 change `+0.001281`; average center-error change `+0.278309` after ignoring NaN pairs. On this condition, RG-SSB helps on average by AUC.

### low_resolution_medium

Average baseline AUC `0.811460`, average HPC RG-SSB AUC `0.774292`, AUC change `-0.037168`. Average Precision@20 change `-0.066106`; average center-error change `+0.135054` after ignoring NaN pairs. On this condition, RG-SSB does not help on average by AUC.

### gaussian_noise_medium

Average baseline AUC `0.776508`, average HPC RG-SSB AUC `0.797822`, AUC change `+0.021314`. Average Precision@20 change `+0.056406`; average center-error change `+0.063117` after ignoring NaN pairs. On this condition, RG-SSB helps on average by AUC.

## 4. Per-sequence summary

Improved overall sequences: none.
Worsened overall sequences: uav_car10, uav_person1, uav_truck1, uav_bike1, uav_boat1, uav_building1, uav_person3, uav_car11.
Strongest average gains: uav_boat1 (-0.000673), uav_car10 (-0.000752), uav_building1 (-0.003077).
Largest average drops: uav_bike1 (-0.017337), uav_car11 (-0.007756), uav_truck1 (-0.006265).
Sequences where RG-SSB is consistently better across all four conditions: none.
Sequences where OSTrack remains better across all four conditions: uav_person1, uav_truck1, uav_bike1, uav_building1.

### uav_car10

Average baseline AUC `0.857237`, average HPC RG-SSB AUC `0.856485`, change `-0.000752`. Improvements: motion_blur_medium (+0.009957). Drops: clean (-0.007751), low_resolution_medium (-0.004214), gaussian_noise_medium (-0.001001). Average center-error change `+0.092206` ignoring NaN pairs.

### uav_person1

Average baseline AUC `0.854716`, average HPC RG-SSB AUC `0.849998`, change `-0.004718`. Improvements: none. Drops: clean (-0.006072), motion_blur_medium (-0.001028), low_resolution_medium (-0.006344), gaussian_noise_medium (-0.005428). Average center-error change `+0.204416` ignoring NaN pairs.

### uav_truck1

Average baseline AUC `0.896927`, average HPC RG-SSB AUC `0.890661`, change `-0.006265`. Improvements: none. Drops: clean (-0.004918), motion_blur_medium (-0.002267), low_resolution_medium (-0.004683), gaussian_noise_medium (-0.013194). Average center-error change `+0.076704` ignoring NaN pairs.

### uav_bike1

Average baseline AUC `0.856188`, average HPC RG-SSB AUC `0.838851`, change `-0.017337`. Improvements: none. Drops: clean (-0.026109), motion_blur_medium (-0.025088), low_resolution_medium (-0.013736), gaussian_noise_medium (-0.004413). Average center-error change `+0.585074` ignoring NaN pairs.

### uav_boat1

Average baseline AUC `0.901941`, average HPC RG-SSB AUC `0.901267`, change `-0.000673`. Improvements: motion_blur_medium (+0.007066). Drops: clean (-0.004681), low_resolution_medium (-0.003682), gaussian_noise_medium (-0.001396). Average center-error change `+0.030661` ignoring NaN pairs.

### uav_building1

Average baseline AUC `0.856183`, average HPC RG-SSB AUC `0.853105`, change `-0.003077`. Improvements: none. Drops: clean (-0.003716), motion_blur_medium (-0.001393), low_resolution_medium (-0.005700), gaussian_noise_medium (-0.001499). Average center-error change `+0.020823` ignoring NaN pairs.

### uav_person3

Average baseline AUC `0.851450`, average HPC RG-SSB AUC `0.847943`, change `-0.003507`. Improvements: motion_blur_medium (+0.017091). Drops: clean (-0.009177), low_resolution_medium (-0.008407), gaussian_noise_medium (-0.013535). Average center-error change `+0.127401` ignoring NaN pairs.

### uav_car11

Average baseline AUC `0.249310`, average HPC RG-SSB AUC `0.241553`, change `-0.007756`. Improvements: clean (+0.004907), motion_blur_medium (+0.003673), gaussian_noise_medium (+0.210977). Drops: low_resolution_medium (-0.250581). Average center-error change `nan` ignoring NaN pairs.

## 5. Main finding

The UAV123 result does not show a clear positive transfer from OTB-style evaluation to this selected UAV123 subset, with average AUC change `-0.005511`. It still provides useful cross-benchmark evidence for deciding the next experiment, but it does not by itself support a paper-scale robustness claim because only 8 UAV123 sequences, one degradation severity, and one seed were evaluated. Remaining weaknesses include sequence-specific drops, NaN center-error entries on `uav_car11`, no UAV-specific training, and no evaluation yet on NFS or larger UAV123 subsets.

## 6. Likely reasons for gains or drops

- UAV123 introduces aerial viewpoint changes and camera motion, which can shift behavior relative to LaSOT and OTB.
- Domain shift from LaSOT/OTB-style data to UAV123 may explain sequence-specific gains and drops.
- Degradation-aware training likely helps when synthetic corruption overlaps the evaluated degradation.
- Feature consistency lambda `0.02` may provide a light clean-degraded alignment signal without over-constraining the frozen backbone.
- RG-SSB + head adaptation keeps the architecture minimal while allowing task-specific updates in the restoration block and box head.
- The backbone is frozen, so adaptation capacity is limited.
- No UAV-specific training was used.
- Response consistency is disabled in this setup.
- There is no target-region weighting, so consistency is not focused on the object region.
- There is no degradation token, memory module, template-guided scan, or response fusion module.

## 7. Recommended next experiment

Options:

- A. Evaluate on NFS.
- B. Evaluate on more UAV123 sequences.
- C. Run longer HPC training.
- D. Add target-region feature consistency.
- E. Add response consistency again.
- F. Add new architecture modules.
- G. Prepare paper-level experiment plan.

Recommended fastest high-quality next step: **Inspect UAV123 failure cases and evaluate NFS or more UAV123 sequences before changing architecture.** This recommendation is based only on the parsed results.

## 8. What to postpone

- degradation token
- template-guided scan
- memory update
- response fusion
- final paper claims

## 9. Decision

Decision: **evaluate more UAV123 sequences**.

## 10. Final detailed table

| sequence | condition | baseline AUC | HPC RG-SSB AUC | AUC change | baseline Precision@20 | HPC Precision@20 | center error change | best model | note |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| uav_car10 | clean | 0.863690 | 0.855939 | -0.007751 | 1.000000 | 1.000000 | +0.106078 | baseline | OSTrack baseline has higher AUC |
| uav_car10 | motion_blur_medium | 0.829978 | 0.839935 | +0.009957 | 1.000000 | 1.000000 | +0.141038 | hpc_rgssb | HPC RG-SSB improves AUC over baseline |
| uav_car10 | low_resolution_medium | 0.866897 | 0.862683 | -0.004214 | 1.000000 | 1.000000 | +0.053801 | baseline | OSTrack baseline has higher AUC |
| uav_car10 | gaussian_noise_medium | 0.868384 | 0.867383 | -0.001001 | 1.000000 | 1.000000 | +0.067908 | baseline | OSTrack baseline has higher AUC |
| uav_person1 | clean | 0.855612 | 0.849540 | -0.006072 | 1.000000 | 1.000000 | +0.190590 | baseline | OSTrack baseline has higher AUC |
| uav_person1 | motion_blur_medium | 0.854149 | 0.853121 | -0.001028 | 1.000000 | 1.000000 | +0.231372 | baseline | OSTrack baseline has higher AUC |
| uav_person1 | low_resolution_medium | 0.858226 | 0.851882 | -0.006344 | 1.000000 | 1.000000 | +0.258775 | baseline | OSTrack baseline has higher AUC |
| uav_person1 | gaussian_noise_medium | 0.850878 | 0.845450 | -0.005428 | 1.000000 | 1.000000 | +0.136926 | baseline | OSTrack baseline has higher AUC |
| uav_truck1 | clean | 0.909330 | 0.904412 | -0.004918 | 0.991361 | 0.978402 | +0.037711 | baseline | OSTrack baseline has higher AUC |
| uav_truck1 | motion_blur_medium | 0.877874 | 0.875607 | -0.002267 | 0.946004 | 0.946004 | +0.138339 | baseline | OSTrack baseline has higher AUC |
| uav_truck1 | low_resolution_medium | 0.905181 | 0.900498 | -0.004683 | 0.987041 | 0.978402 | -0.023962 | baseline | OSTrack baseline has higher AUC |
| uav_truck1 | gaussian_noise_medium | 0.895323 | 0.882129 | -0.013194 | 0.974082 | 0.961123 | +0.154730 | baseline | OSTrack baseline has higher AUC |
| uav_bike1 | clean | 0.851681 | 0.825572 | -0.026109 | 0.997407 | 0.988655 | +0.771038 | baseline | OSTrack baseline has higher AUC |
| uav_bike1 | motion_blur_medium | 0.830919 | 0.805831 | -0.025088 | 0.965640 | 0.964019 | +1.068531 | baseline | OSTrack baseline has higher AUC |
| uav_bike1 | low_resolution_medium | 0.868633 | 0.854897 | -0.013736 | 0.996110 | 0.992220 | +0.430696 | baseline | OSTrack baseline has higher AUC |
| uav_bike1 | gaussian_noise_medium | 0.873518 | 0.869105 | -0.004413 | 0.995462 | 0.996759 | +0.070030 | baseline | OSTrack baseline has higher AUC |
| uav_boat1 | clean | 0.907177 | 0.902496 | -0.004681 | 1.000000 | 1.000000 | -0.038782 | baseline | OSTrack baseline has higher AUC |
| uav_boat1 | motion_blur_medium | 0.891946 | 0.899012 | +0.007066 | 1.000000 | 1.000000 | +0.255298 | hpc_rgssb | HPC RG-SSB improves AUC over baseline |
| uav_boat1 | low_resolution_medium | 0.907342 | 0.903660 | -0.003682 | 1.000000 | 1.000000 | +0.056466 | baseline | OSTrack baseline has higher AUC |
| uav_boat1 | gaussian_noise_medium | 0.901298 | 0.899902 | -0.001396 | 1.000000 | 1.000000 | -0.150337 | baseline | OSTrack baseline has higher AUC |
| uav_building1 | clean | 0.856573 | 0.852857 | -0.003716 | 1.000000 | 1.000000 | +0.033140 | baseline | OSTrack baseline has higher AUC |
| uav_building1 | motion_blur_medium | 0.866347 | 0.864954 | -0.001393 | 1.000000 | 1.000000 | -0.002586 | baseline | OSTrack baseline has higher AUC |
| uav_building1 | low_resolution_medium | 0.861661 | 0.855961 | -0.005700 | 1.000000 | 1.000000 | +0.056993 | baseline | OSTrack baseline has higher AUC |
| uav_building1 | gaussian_noise_medium | 0.840149 | 0.838650 | -0.001499 | 1.000000 | 1.000000 | -0.004256 | baseline | OSTrack baseline has higher AUC |
| uav_person3 | clean | 0.859261 | 0.850084 | -0.009177 | 1.000000 | 1.000000 | +0.114006 | baseline | OSTrack baseline has higher AUC |
| uav_person3 | motion_blur_medium | 0.827018 | 0.844109 | +0.017091 | 1.000000 | 1.000000 | +0.116172 | hpc_rgssb | HPC RG-SSB improves AUC over baseline |
| uav_person3 | low_resolution_medium | 0.862664 | 0.854257 | -0.008407 | 1.000000 | 1.000000 | +0.112608 | baseline | OSTrack baseline has higher AUC |
| uav_person3 | gaussian_noise_medium | 0.856859 | 0.843324 | -0.013535 | 1.000000 | 1.000000 | +0.166816 | baseline | OSTrack baseline has higher AUC |
| uav_car11 | clean | 0.483503 | 0.488410 | +0.004907 | 0.792285 | 0.818991 | nan | hpc_rgssb | HPC RG-SSB improves AUC over baseline |
| uav_car11 | motion_blur_medium | 0.027000 | 0.030673 | +0.003673 | 0.032641 | 0.044510 | nan | hpc_rgssb | HPC RG-SSB improves AUC over baseline |
| uav_car11 | low_resolution_medium | 0.361078 | 0.110497 | -0.250581 | 0.727003 | 0.210682 | nan | baseline | OSTrack baseline has higher AUC |
| uav_car11 | gaussian_noise_medium | 0.125657 | 0.336634 | +0.210977 | 0.243323 | 0.706231 | nan | hpc_rgssb | HPC RG-SSB improves AUC over baseline |

## 11. Average condition table

| condition | average baseline AUC | average HPC RG-SSB AUC | average AUC change | average Precision@20 change | average center-error change | decision note |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| clean | 0.823353 | 0.816164 | -0.007190 | +0.000624 | +0.173397 | Near tie on average |
| motion_blur_medium | 0.750654 | 0.751655 | +0.001001 | +0.001281 | +0.278309 | RG-SSB improves slightly on average |
| low_resolution_medium | 0.811460 | 0.774292 | -0.037168 | -0.066106 | +0.135054 | OSTrack remains clearly better on average |
| gaussian_noise_medium | 0.776508 | 0.797822 | +0.021314 | +0.056406 | +0.063117 | RG-SSB improves clearly on average |

## 12. Average sequence table

| sequence | average baseline AUC | average HPC RG-SSB AUC | average AUC change | improved overall yes/no | note |
| --- | ---: | ---: | ---: | --- | --- |
| uav_car10 | 0.857237 | 0.856485 | -0.000752 | no | Near tie overall |
| uav_person1 | 0.854716 | 0.849998 | -0.004718 | no | Near tie overall |
| uav_truck1 | 0.896927 | 0.890661 | -0.006265 | no | Near tie overall |
| uav_bike1 | 0.856188 | 0.838851 | -0.017337 | no | Worsens overall |
| uav_boat1 | 0.901941 | 0.901267 | -0.000673 | no | Near tie overall |
| uav_building1 | 0.856183 | 0.853105 | -0.003077 | no | Near tie overall |
| uav_person3 | 0.851450 | 0.847943 | -0.003507 | no | Near tie overall |
| uav_car11 | 0.249310 | 0.241553 | -0.007756 | no | Near tie overall |

## Verification

- Parsed `experiments/baseline_results.csv` with Python.
- Created `experiments/rgssb_hpc_uav123_comparison.csv`.
- Created `implementation/rgssb_hpc_uav123_result_analysis.md`.
- Compared 32 sequence-condition pairs with one baseline row and one HPC RG-SSB row per pair.
- Preserved NaN center-error values in the detailed CSV and ignored NaN pairwise center-error changes in averages.
- Did not run OSTrack.
- Did not run training or evaluation.
- Did not modify datasets or `external/OSTrack`.

Uncertain fields:

- Each degraded condition uses one seed, `42`.
- Each degradation uses medium severity only.
- The UAV123 subset contains 8 selected sequences, not the full benchmark.
- NaN center-error values for `uav_car11` indicate center-error metrics should be interpreted with caution for that sequence.
