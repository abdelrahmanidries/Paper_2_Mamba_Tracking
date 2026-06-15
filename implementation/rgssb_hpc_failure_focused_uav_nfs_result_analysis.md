# RG-SSB HPC Failure-Focused UAV123 + NFS Result Analysis

Inputs:

- `experiments/baseline_results.csv`
- `experiments/rgssb_hpc_cross_benchmark_failure_inspection.csv`
- `implementation/rgssb_hpc_cross_benchmark_failure_inspection.md`
- `implementation/failure_focused_uav_nfs_eval_plan.md`
- `implementation/rgssb_hpc_uav123_result_analysis.md`
- `implementation/rgssb_hpc_nfs_result_analysis.md`

## 1. Executive summary

The expanded failure-focused UAV123+NFS batch is near neutral overall, so the model is not consistently worse outside OTB but still lacks stable cross-benchmark gains. Across `128` expanded sequence-condition pairs, baseline average AUC is `0.492840`, HPC RG-SSB average AUC is `0.494445`, and average AUC change is `+0.001605`.
UAV123 average AUC change is `+0.017405` and NFS average AUC change is `-0.014195`. Outcome counts across both benchmarks: gains `23`, neutral `79`, drops `26`. NaN center-error rows: `40`; NaN center-error pairs ignored in averages: `20`.

## 2. Expanded UAV123 result

UAV123: `64` comparisons, average baseline AUC `0.660183`, average HPC RG-SSB AUC `0.677587`, average AUC change `+0.017405`. Precision@20 change `+0.029983`; center-error change `-3.500185` ignoring NaN pairs. Outcome counts: gains `9`, neutral `49`, drops `6`.
- `uav_car12`: average AUC change `-0.128083`; gains `1`, neutral `0`, drops `3`.
- `uav_bike1`: average AUC change `-0.017337`; gains `0`, neutral `2`, drops `2`.
- `uav_car11`: average AUC change `-0.007756`; gains `1`, neutral `2`, drops `1`.
- `uav_truck1`: average AUC change `-0.006265`; gains `0`, neutral `4`, drops `0`.
- `uav_person12_1`: average AUC change `-0.005090`; gains `0`, neutral `4`, drops `0`.
- `uav_person1`: average AUC change `-0.004718`; gains `0`, neutral `4`, drops `0`.
- `uav_person3`: average AUC change `-0.003507`; gains `0`, neutral `4`, drops `0`.
- `uav_building1`: average AUC change `-0.003077`; gains `0`, neutral `4`, drops `0`.
- `uav_wakeboard1`: average AUC change `-0.002646`; gains `1`, neutral `3`, drops `0`.
- `uav_car13`: average AUC change `-0.001539`; gains `0`, neutral `4`, drops `0`.
- `uav_car10`: average AUC change `-0.000752`; gains `0`, neutral `4`, drops `0`.
- `uav_boat1`: average AUC change `-0.000673`; gains `0`, neutral `4`, drops `0`.
- `uav_person10`: average AUC change `+0.003653`; gains `0`, neutral `4`, drops `0`.
- `uav_bike2`: average AUC change `+0.011136`; gains `1`, neutral `3`, drops `0`.
- `uav_truck2`: average AUC change `+0.082230`; gains `1`, neutral `3`, drops `0`.
- `uav_person14_1`: average AUC change `+0.362900`; gains `4`, neutral `0`, drops `0`.

## 3. Expanded NFS result

NFS: `64` comparisons, average baseline AUC `0.325497`, average HPC RG-SSB AUC `0.311302`, average AUC change `-0.014195`. Precision@20 change `-0.000662`; center-error change `+5.228074` ignoring NaN pairs. Outcome counts: gains `14`, neutral `30`, drops `20`.
- `nfs_cheetah`: average AUC change `-0.114721`; gains `0`, neutral `2`, drops `2`.
- `nfs_walking`: average AUC change `-0.072201`; gains `1`, neutral `1`, drops `2`.
- `nfs_person_scooter`: average AUC change `-0.044482`; gains `0`, neutral `0`, drops `4`.
- `nfs_car_drifting`: average AUC change `-0.039833`; gains `0`, neutral `0`, drops `4`.
- `nfs_motorcross`: average AUC change `-0.035224`; gains `0`, neutral `1`, drops `3`.
- `nfs_bottle`: average AUC change `-0.027437`; gains `0`, neutral `0`, drops `4`.
- `nfs_dog`: average AUC change `-0.006328`; gains `0`, neutral `4`, drops `0`.
- `nfs_basketball_player`: average AUC change `-0.002603`; gains `0`, neutral `4`, drops `0`.
- `nfs_car_jumping`: average AUC change `-0.000450`; gains `1`, neutral `2`, drops `1`.
- `nfs_running`: average AUC change `+0.000183`; gains `1`, neutral `3`, drops `0`.
- `nfs_horse_running`: average AUC change `+0.004701`; gains `0`, neutral `4`, drops `0`.
- `nfs_bird_2`: average AUC change `+0.007753`; gains `1`, neutral `3`, drops `0`.
- `nfs_basketball_player_2`: average AUC change `+0.008468`; gains `1`, neutral `3`, drops `0`.
- `nfs_soccer_player_2`: average AUC change `+0.015706`; gains `1`, neutral `3`, drops `0`.
- `nfs_Gymnastics`: average AUC change `+0.021961`; gains `4`, neutral `0`, drops `0`.
- `nfs_car`: average AUC change `+0.057392`; gains `4`, neutral `0`, drops `0`.

## 4. Condition-level result

- `clean`: average AUC change `+0.009171` across `32` cases; gains `5`, neutral `21`, drops `6`; Precision@20 change `+0.011095`; center-error change `-4.546992`.
- `motion_blur_medium`: average AUC change `+0.006356` across `32` cases; gains `6`, neutral `18`, drops `8`; Precision@20 change `+0.024148`; center-error change `-2.442864`.
- `low_resolution_medium`: average AUC change `-0.015135` across `32` cases; gains `4`, neutral `21`, drops `7`; Precision@20 change `-0.004407`; center-error change `+4.428009`.
- `gaussian_noise_medium`: average AUC change `+0.006027` across `32` cases; gains `8`, neutral `19`, drops `5`; Precision@20 change `+0.027805`; center-error change `+9.250314`.

## 5. Strongest gains

1. `UAV123` `uav_person14_1` `clean`: AUC change `+0.578395`.
2. `UAV123` `uav_person14_1` `low_resolution_medium`: AUC change `+0.565128`.
3. `UAV123` `uav_truck2` `motion_blur_medium`: AUC change `+0.379530`.
4. `UAV123` `uav_car12` `gaussian_noise_medium`: AUC change `+0.330661`.
5. `UAV123` `uav_person14_1` `motion_blur_medium`: AUC change `+0.287351`.
6. `UAV123` `uav_car11` `gaussian_noise_medium`: AUC change `+0.210977`.
7. `NFS` `nfs_walking` `clean`: AUC change `+0.144751`.
8. `NFS` `nfs_car` `clean`: AUC change `+0.065802`.
9. `NFS` `nfs_car_jumping` `clean`: AUC change `+0.058505`.
10. `NFS` `nfs_car` `motion_blur_medium`: AUC change `+0.056749`.

## 6. Largest drops

1. `NFS` `nfs_cheetah` `low_resolution_medium`: AUC change `-0.403866`.
2. `UAV123` `uav_car12` `clean`: AUC change `-0.345662`.
3. `NFS` `nfs_walking` `gaussian_noise_medium`: AUC change `-0.284435`.
4. `UAV123` `uav_car11` `low_resolution_medium`: AUC change `-0.250581`.
5. `UAV123` `uav_car12` `low_resolution_medium`: AUC change `-0.248676`.
6. `UAV123` `uav_car12` `motion_blur_medium`: AUC change `-0.248655`.
7. `NFS` `nfs_walking` `motion_blur_medium`: AUC change `-0.165552`.
8. `NFS` `nfs_car_jumping` `gaussian_noise_medium`: AUC change `-0.063006`.
9. `NFS` `nfs_person_scooter` `motion_blur_medium`: AUC change `-0.053077`.
10. `NFS` `nfs_motorcross` `low_resolution_medium`: AUC change `-0.052043`.

## 7. Comparison with earlier OTB/UAV123/NFS findings

- Earlier `OTB` subset: average AUC change `+0.033144` across `52` cases.
- Earlier `UAV123` subset: average AUC change `-0.005511` across `32` cases.
- Earlier `NFS` subset: average AUC change `-0.002660` across `32` cases.
- Expanded UAV123 now has average AUC change `+0.017405` across `64` cases.
- Expanded NFS now has average AUC change `-0.014195` across `64` cases.
The comparison should be interpreted as local proof-of-concept evidence: the expanded batch is larger than the earlier selected subsets, but it is still not full paper-scale evaluation and still uses one severity and one degradation seed.

## 8. Main conclusion

The expanded failure-focused UAV123+NFS batch is near neutral overall, so the model is not consistently worse outside OTB but still lacks stable cross-benchmark gains. The result should not be overclaimed because it uses selected UAV123/NFS subsets and does not include qualitative failure inspection. The main technical signal is whether the previous UAV123/NFS weakness persists after adding failure-focused coverage.

## 9. Recommended next experiment

Recommended next step: **Evaluate full UAV123/NFS or add target-region feature consistency only if the remaining drops persist under broader coverage.** This recommendation is based only on the parsed results. New architecture modules are not justified from this report alone.

## 10. What to postpone

- degradation token
- template-guided scan
- memory update
- response fusion
- final paper claims

## 11. Final decision

Decision: **expand cross-benchmark evaluation before changing architecture**.

## Detailed Tables

### Benchmark summary

| benchmark | cases | baseline AUC | HPC RG-SSB AUC | AUC change | Precision@20 change | center-error change | gains | neutral | drops |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| UAV123 | 64 | 0.660183 | 0.677587 | +0.017405 | +0.029983 | -3.500185 | 9 | 49 | 6 |
| NFS | 64 | 0.325497 | 0.311302 | -0.014195 | -0.000662 | +5.228074 | 14 | 30 | 20 |

### Condition summary

| condition | cases | AUC change | gains | neutral | drops |
| --- | ---: | ---: | ---: | ---: | ---: |
| clean | 32 | +0.009171 | 5 | 21 | 6 |
| motion_blur_medium | 32 | +0.006356 | 6 | 18 | 8 |
| low_resolution_medium | 32 | -0.015135 | 4 | 21 | 7 |
| gaussian_noise_medium | 32 | +0.006027 | 8 | 19 | 5 |

### Top 10 gains

| rank | benchmark | sequence | condition | AUC change |
| ---: | --- | --- | --- | ---: |
| 1 | UAV123 | uav_person14_1 | clean | +0.578395 |
| 2 | UAV123 | uav_person14_1 | low_resolution_medium | +0.565128 |
| 3 | UAV123 | uav_truck2 | motion_blur_medium | +0.379530 |
| 4 | UAV123 | uav_car12 | gaussian_noise_medium | +0.330661 |
| 5 | UAV123 | uav_person14_1 | motion_blur_medium | +0.287351 |
| 6 | UAV123 | uav_car11 | gaussian_noise_medium | +0.210977 |
| 7 | NFS | nfs_walking | clean | +0.144751 |
| 8 | NFS | nfs_car | clean | +0.065802 |
| 9 | NFS | nfs_car_jumping | clean | +0.058505 |
| 10 | NFS | nfs_car | motion_blur_medium | +0.056749 |

### Top 10 drops

| rank | benchmark | sequence | condition | AUC change |
| ---: | --- | --- | --- | ---: |
| 1 | NFS | nfs_cheetah | low_resolution_medium | -0.403866 |
| 2 | UAV123 | uav_car12 | clean | -0.345662 |
| 3 | NFS | nfs_walking | gaussian_noise_medium | -0.284435 |
| 4 | UAV123 | uav_car11 | low_resolution_medium | -0.250581 |
| 5 | UAV123 | uav_car12 | low_resolution_medium | -0.248676 |
| 6 | UAV123 | uav_car12 | motion_blur_medium | -0.248655 |
| 7 | NFS | nfs_walking | motion_blur_medium | -0.165552 |
| 8 | NFS | nfs_car_jumping | gaussian_noise_medium | -0.063006 |
| 9 | NFS | nfs_person_scooter | motion_blur_medium | -0.053077 |
| 10 | NFS | nfs_motorcross | low_resolution_medium | -0.052043 |

## Verification

- Parsed `experiments/baseline_results.csv` with Python.
- Created `experiments/rgssb_hpc_failure_focused_uav_nfs_comparison.csv`.
- Created `implementation/rgssb_hpc_failure_focused_uav_nfs_result_analysis.md`.
- Compared `128` sequence-condition pairs with one baseline row and one HPC RG-SSB row per pair.
- Preserved NaN center-error values in the detailed CSV and ignored NaN center-error pairs in averages.
- Did not run OSTrack, training, or evaluation.
- Did not modify datasets or `external/OSTrack`.

Uncertain fields:

- Each degraded condition uses one seed, `42`.
- Each degradation uses medium severity only.
- The report uses aggregate CSV metrics only and does not include qualitative frame/prediction inspection.
