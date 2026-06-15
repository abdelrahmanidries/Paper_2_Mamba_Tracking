# RG-SSB HPC Cross-Benchmark Failure Inspection

Inputs:

- `experiments/baseline_results.csv`
- `experiments/rgssb_hpc_broader_otb_comparison.csv`
- `experiments/rgssb_hpc_uav123_comparison.csv`
- `experiments/rgssb_hpc_nfs_comparison.csv`
- `implementation/rgssb_hpc_broader_otb_result_analysis.md`
- `implementation/rgssb_hpc_uav123_result_analysis.md`
- `implementation/rgssb_hpc_nfs_result_analysis.md`

## 1. Executive summary

Across OTB, UAV123, and NFS, the HPC RG-SSB lambda `0.02` checkpoint is strongest on broader OTB and weaker on the selected UAV123/NFS subsets. OTB average AUC change is `+0.033144`, UAV123 is `-0.005511`, and NFS is `-0.002660`.
This pattern supports continuing failure inspection and broader evaluation before changing architecture. The strongest gains are concentrated in OTB and a few NFS cases, while the largest drops are dominated by UAV123 low-resolution and NFS walking/noise or motion-blur cases.

## 2. Benchmark-level result

- OTB: average AUC change `+0.033144` across `52` cases; strong gains `9`, moderate gains `7`, neutral `31`, moderate drops `5`, strong drops `0`.
- UAV123: average AUC change `-0.005511` across `32` cases; strong gains `1`, moderate gains `0`, neutral `28`, moderate drops `2`, strong drops `1`.
- NFS: average AUC change `-0.002660` across `32` cases; strong gains `5`, moderate gains `6`, neutral `15`, moderate drops `4`, strong drops `2`.

Best benchmark by average AUC change is `OTB`. Weakest benchmark by average AUC change is `UAV123`. Failures are not limited to one non-OTB benchmark, but the average behavior is weaker outside OTB than on broader OTB.

## 3. Condition-level result

- clean: average AUC change `+0.012788` across `29` cases; strong gains `3`, moderate gains `3`, neutral `20`, moderate drops `3`, strong drops `0`.
- motion_blur_medium: average AUC change `+0.017132` across `29` cases; strong gains `5`, moderate gains `6`, neutral `14`, moderate drops `3`, strong drops `1`.
- low_resolution_medium: average AUC change `+0.012607` across `29` cases; strong gains `3`, moderate gains `2`, neutral `21`, moderate drops `2`, strong drops `1`.
- gaussian_noise_medium: average AUC change `+0.007888` across `29` cases; strong gains `4`, moderate gains `2`, neutral `19`, moderate drops `3`, strong drops `1`.

Best condition by average AUC change is `motion_blur_medium`. Weakest condition is `gaussian_noise_medium`. Gaussian noise differs by benchmark: OTB `+0.021530`, UAV123 `+0.021314`, NFS `-0.027707`. Low resolution also differs by benchmark: OTB `+0.046462`, UAV123 `-0.037168`, NFS `+0.007367`.

## 4. Strongest gains

The top improvements are mostly OTB robustness wins, with NFS `nfs_walking` clean and NFS `nfs_car` also appearing. This suggests the model can help substantially, but the benefit is not uniform across domains or degradations.

1. `OTB` `Walking2` `low_resolution_medium`: AUC change `+0.454515`.
2. `OTB` `Walking2` `gaussian_noise_medium`: AUC change `+0.262792`.
3. `OTB` `Deer` `motion_blur_medium`: AUC change `+0.227165`.
4. `UAV123` `uav_car11` `gaussian_noise_medium`: AUC change `+0.210977`.
5. `OTB` `Deer` `low_resolution_medium`: AUC change `+0.171246`.
6. `OTB` `Football` `motion_blur_medium`: AUC change `+0.166730`.
7. `OTB` `Deer` `clean`: AUC change `+0.153117`.
8. `NFS` `nfs_walking` `clean`: AUC change `+0.144751`.
9. `OTB` `Walking2` `motion_blur_medium`: AUC change `+0.067763`.
10. `OTB` `David2` `motion_blur_medium`: AUC change `+0.067279`.

## 5. Largest drops

The largest drops are concentrated in UAV123 `uav_car11`, NFS `nfs_walking`, and some OTB/NFS sequence-specific failures. These should be inspected before changing the model because a small number of sequence-condition pairs can dominate the negative cross-benchmark story.

1. `NFS` `nfs_walking` `gaussian_noise_medium`: AUC change `-0.284435`.
2. `UAV123` `uav_car11` `low_resolution_medium`: AUC change `-0.250581`.
3. `NFS` `nfs_walking` `motion_blur_medium`: AUC change `-0.165552`.
4. `OTB` `David2` `gaussian_noise_medium`: AUC change `-0.038203`.
5. `OTB` `BlurBody` `clean`: AUC change `-0.032608`.
6. `NFS` `nfs_bottle` `motion_blur_medium`: AUC change `-0.029910`.
7. `NFS` `nfs_bottle` `low_resolution_medium`: AUC change `-0.029623`.
8. `OTB` `BlurBody` `motion_blur_medium`: AUC change `-0.029051`.
9. `NFS` `nfs_bottle` `clean`: AUC change `-0.028648`.
10. `OTB` `BlurBody` `low_resolution_medium`: AUC change `-0.027835`.

## 6. Failure pattern interpretation

- Does the model fail more on UAV123/NFS than OTB? Yes, relative to OTB. OTB has average AUC change `+0.033144`, while UAV123 and NFS are `-0.005511` and `-0.002660`.
- Does it fail more by condition? The weakest condition across all benchmarks is `gaussian_noise_medium` with average AUC change `+0.007888`.
- Are failures concentrated in a few sequences? Yes. The highest failure concentrations include OTB:BlurBody (4 drop cases, avg -0.027732), NFS:nfs_bottle (4 drop cases, avg -0.027437), NFS:nfs_walking (2 drop cases, avg -0.072201), UAV123:uav_bike1 (2 drop cases, avg -0.017337), UAV123:uav_car11 (1 drop cases, avg -0.007756).
- Are gains concentrated in OTB only? Not only, but OTB contributes the most moderate/strong gains: OTB `16`, UAV123 `1`, NFS `11`.
- Does Gaussian noise behave differently across benchmarks? Yes. It is positive on OTB `+0.021530` and UAV123 `+0.021314`, but negative on NFS `-0.027707`.
- Does low resolution behave differently across benchmarks? Yes. It is positive on OTB `+0.046462` and NFS `+0.007367`, but clearly negative on UAV123 `-0.037168`.
- Likely factors include domain shift from OTB to UAV/NFS, aerial viewpoint in UAV123, high-frame-rate/sampling behavior in NFS, the frozen backbone, LaSOT-only training, search-only degradation, no target-region feature consistency, no response consistency, and no sequence-specific adaptation.

## 7. Recommended next experiment

Options:

- A. Evaluate more UAV123/NFS sequences.
- B. Train longer on HPC.
- C. Add target-region feature consistency.
- D. Add benchmark/domain-specific training data.
- E. Add new architecture modules.
- F. Prepare paper-level experiment plan with current evidence.

Recommended fastest high-quality next step: **expand UAV123/NFS evaluation and inspect sequence-level failures before changing architecture**. The parsed results do not justify adding new architecture modules yet, because failures are partly benchmark- and sequence-specific and the strongest positive result remains broader OTB.

## 8. What to postpone

- degradation token
- template-guided scan
- memory update
- response fusion
- final paper claims

## 9. Decision

Decision: **expand cross-benchmark evaluation**.

## 10. Tables

### Benchmark summary table

| benchmark | cases | average AUC change | strong gains | moderate gains | neutral | moderate drops | strong drops |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| OTB | 52 | +0.033144 | 9 | 7 | 31 | 5 | 0 |
| UAV123 | 32 | -0.005511 | 1 | 0 | 28 | 2 | 1 |
| NFS | 32 | -0.002660 | 5 | 6 | 15 | 4 | 2 |

### Condition summary table

| condition | cases | average AUC change | strong gains | moderate gains | neutral | moderate drops | strong drops |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| clean | 29 | +0.012788 | 3 | 3 | 20 | 3 | 0 |
| motion_blur_medium | 29 | +0.017132 | 5 | 6 | 14 | 3 | 1 |
| low_resolution_medium | 29 | +0.012607 | 3 | 2 | 21 | 2 | 1 |
| gaussian_noise_medium | 29 | +0.007888 | 4 | 2 | 19 | 3 | 1 |

### Top 10 gains table

| rank | benchmark | sequence | condition | AUC change | outcome |
| ---: | --- | --- | --- | ---: | --- |
| 1 | OTB | Walking2 | low_resolution_medium | +0.454515 | strong_gain |
| 2 | OTB | Walking2 | gaussian_noise_medium | +0.262792 | strong_gain |
| 3 | OTB | Deer | motion_blur_medium | +0.227165 | strong_gain |
| 4 | UAV123 | uav_car11 | gaussian_noise_medium | +0.210977 | strong_gain |
| 5 | OTB | Deer | low_resolution_medium | +0.171246 | strong_gain |
| 6 | OTB | Football | motion_blur_medium | +0.166730 | strong_gain |
| 7 | OTB | Deer | clean | +0.153117 | strong_gain |
| 8 | NFS | nfs_walking | clean | +0.144751 | strong_gain |
| 9 | OTB | Walking2 | motion_blur_medium | +0.067763 | strong_gain |
| 10 | OTB | David2 | motion_blur_medium | +0.067279 | strong_gain |

### Top 10 drops table

| rank | benchmark | sequence | condition | AUC change | outcome |
| ---: | --- | --- | --- | ---: | --- |
| 1 | NFS | nfs_walking | gaussian_noise_medium | -0.284435 | strong_drop |
| 2 | UAV123 | uav_car11 | low_resolution_medium | -0.250581 | strong_drop |
| 3 | NFS | nfs_walking | motion_blur_medium | -0.165552 | strong_drop |
| 4 | OTB | David2 | gaussian_noise_medium | -0.038203 | moderate_drop |
| 5 | OTB | BlurBody | clean | -0.032608 | moderate_drop |
| 6 | NFS | nfs_bottle | motion_blur_medium | -0.029910 | moderate_drop |
| 7 | NFS | nfs_bottle | low_resolution_medium | -0.029623 | moderate_drop |
| 8 | OTB | BlurBody | motion_blur_medium | -0.029051 | moderate_drop |
| 9 | NFS | nfs_bottle | clean | -0.028648 | moderate_drop |
| 10 | OTB | BlurBody | low_resolution_medium | -0.027835 | moderate_drop |

## Verification

- Parsed the existing OTB, UAV123, and NFS comparison CSV files with Python.
- Created `experiments/rgssb_hpc_cross_benchmark_failure_inspection.csv`.
- Created `implementation/rgssb_hpc_cross_benchmark_failure_inspection.md`.
- Combined `116` sequence-condition pairs: OTB `52`, UAV123 `32`, NFS `32`.
- Did not run OSTrack.
- Did not run training or evaluation.
- Did not modify datasets or `external/OSTrack`.

Uncertain fields:

- Each degraded condition uses one seed, `42`.
- Each degradation uses medium severity only.
- UAV123 and NFS use selected subsets, not full benchmark coverage.
- The report uses aggregate CSV metrics only and does not include visual inspection of frames or predictions.
