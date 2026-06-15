# RG-SSB HPC NFS Result Analysis

Inputs:

- `experiments/baseline_results.csv`
- `implementation/nfs_hpc_evaluation_plan.md`
- `implementation/rgssb_hpc_broader_otb_result_analysis.md`
- `implementation/rgssb_hpc_uav123_result_analysis.md`
- `experiments/rgssb_hpc_broader_otb_comparison.csv`
- `experiments/rgssb_hpc_uav123_comparison.csv`

## 1. Executive summary

The HPC RG-SSB + head feature-consistency lambda `0.02` model does not improve over the original OSTrack baseline on the selected NFS subset: baseline average AUC `0.330235`, HPC RG-SSB average AUC `0.327575`, change `-0.002660` across 32 sequence-condition pairs.
Average Precision@20 change is `-0.001757`. Average center-error change is `-12.163420` after ignoring NaN center-error pairs. NaN center-error rows found: `0`; NaN pairwise center-error changes ignored in averages: `0`.

## 2. Technical status

- NFS baseline evaluation completed.
- NFS HPC RG-SSB evaluation completed.
- 8 sequences and 4 conditions were evaluated.
- 64 NFS rows were added to `experiments/baseline_results.csv`.
- NFS annotation alignment was fixed before evaluation.
- CSV logging works.
- This is cross-benchmark evidence beyond OTB and UAV123.
- This is still not final paper-scale evidence.

## 3. Per-condition summary

### clean

Average baseline AUC `0.310970`, average HPC RG-SSB AUC `0.336599`, AUC change `+0.025629`. Average Precision@20 change `+0.002829`; average center-error change `-15.597252` after ignoring NaN pairs. On this condition, RG-SSB helps on average by AUC.

### motion_blur_medium

Average baseline AUC `0.333459`, average HPC RG-SSB AUC `0.317531`, AUC change `-0.015928`. Average Precision@20 change `-0.002478`; average center-error change `+0.462576` after ignoring NaN pairs. On this condition, RG-SSB does not help on average by AUC.

### low_resolution_medium

Average baseline AUC `0.310739`, average HPC RG-SSB AUC `0.318106`, AUC change `+0.007367`. Average Precision@20 change `+0.001737`; average center-error change `-4.838398` after ignoring NaN pairs. On this condition, RG-SSB helps on average by AUC.

### gaussian_noise_medium

Average baseline AUC `0.365772`, average HPC RG-SSB AUC `0.338065`, AUC change `-0.027707`. Average Precision@20 change `-0.009116`; average center-error change `-28.680605` after ignoring NaN pairs. On this condition, RG-SSB does not help on average by AUC.

## 4. Per-sequence summary

Improved overall sequences: nfs_Gymnastics, nfs_car, nfs_running, nfs_bird_2.
Worsened overall sequences: nfs_basketball_player, nfs_dog, nfs_bottle, nfs_walking.
Strongest average gains: nfs_car (+0.057392), nfs_Gymnastics (+0.021961), nfs_bird_2 (+0.007753).
Largest average drops: nfs_walking (-0.072201), nfs_bottle (-0.027437), nfs_dog (-0.006328).
Sequences where RG-SSB is consistently better across all four conditions: nfs_Gymnastics, nfs_car.
Sequences where OSTrack remains better across all four conditions: nfs_dog, nfs_bottle.

### nfs_Gymnastics

Average baseline AUC `0.308989`, average HPC RG-SSB AUC `0.330950`, change `+0.021961`. Improvements: clean (+0.023354), motion_blur_medium (+0.020206), low_resolution_medium (+0.023434), gaussian_noise_medium (+0.020851). Drops: none. Average center-error change `+12.804592` ignoring NaN pairs.

### nfs_basketball_player

Average baseline AUC `0.348265`, average HPC RG-SSB AUC `0.345662`, change `-0.002603`. Improvements: gaussian_noise_medium (+0.005071). Drops: clean (-0.000215), motion_blur_medium (-0.003488), low_resolution_medium (-0.011779). Average center-error change `+9.989136` ignoring NaN pairs.

### nfs_car

Average baseline AUC `0.084139`, average HPC RG-SSB AUC `0.141532`, change `+0.057392`. Improvements: clean (+0.065802), motion_blur_medium (+0.056749), low_resolution_medium (+0.055416), gaussian_noise_medium (+0.051603). Drops: none. Average center-error change `-170.856499` ignoring NaN pairs.

### nfs_dog

Average baseline AUC `0.425101`, average HPC RG-SSB AUC `0.418773`, change `-0.006328`. Improvements: none. Drops: clean (-0.004701), motion_blur_medium (-0.014285), low_resolution_medium (-0.004778), gaussian_noise_medium (-0.001548). Average center-error change `+11.402188` ignoring NaN pairs.

### nfs_running

Average baseline AUC `0.484513`, average HPC RG-SSB AUC `0.484695`, change `+0.000183`. Improvements: gaussian_noise_medium (+0.024614). Drops: clean (-0.002238), motion_blur_medium (-0.010428), low_resolution_medium (-0.011217). Average center-error change `+20.987394` ignoring NaN pairs.

### nfs_bottle

Average baseline AUC `0.373810`, average HPC RG-SSB AUC `0.346372`, change `-0.027437`. Improvements: none. Drops: clean (-0.028648), motion_blur_medium (-0.029910), low_resolution_medium (-0.029623), gaussian_noise_medium (-0.021568). Average center-error change `+28.806820` ignoring NaN pairs.

### nfs_bird_2

Average baseline AUC `0.258398`, average HPC RG-SSB AUC `0.266151`, change `+0.007753`. Improvements: clean (+0.006926), motion_blur_medium (+0.019282), low_resolution_medium (+0.021050). Drops: gaussian_noise_medium (-0.016246). Average center-error change `-26.308041` ignoring NaN pairs.

### nfs_walking

Average baseline AUC `0.358665`, average HPC RG-SSB AUC `0.286464`, change `-0.072201`. Improvements: clean (+0.144751), low_resolution_medium (+0.016431). Drops: motion_blur_medium (-0.165552), gaussian_noise_medium (-0.284435). Average center-error change `+15.867052` ignoring NaN pairs.

## 5. Cross-benchmark interpretation

The broader OTB result was positive, with average AUC change `+0.033144` across 52 sequence-condition pairs. The selected UAV123 subset was mixed/slightly negative, with average AUC change `-0.005511` across 32 sequence-condition pairs. The selected NFS subset should be interpreted in that context: it adds another benchmark with high-frame-rate sampling behavior, and its average AUC change is `-0.002660`.

## 6. Main finding

The selected NFS result is not positive on average, so it weakens the cross-benchmark transfer story relative to the broader OTB result. The result should not be overclaimed because it covers 8 selected NFS sequences, four synthetic conditions, one severity, and one degradation seed. Remaining weaknesses include sequence-specific drops, no NFS-specific training, no response consistency, no target-region weighting, and no full-benchmark evaluation yet.

## 7. Likely reasons for gains or drops

- NFS has high-frame-rate and sampling behavior, so prediction and annotation alignment can affect metric stability if not handled consistently.
- Fast motion and motion blur can make NFS sequences sensitive to degradation-aware adaptation.
- Degradation-aware training likely helps when synthetic corruption overlaps the evaluated degradation.
- Feature consistency lambda `0.02` provides a light clean-degraded alignment signal.
- RG-SSB + head adaptation keeps the backbone frozen while allowing the restoration-oriented block and box head to adapt.
- The backbone is frozen, so adaptation capacity is limited.
- No NFS-specific training was used.
- Response consistency is disabled in this setup.
- There is no target-region weighting, so consistency is global rather than object-focused.
- There is no degradation token, memory module, template-guided scan, or response fusion module.

## 8. Recommended next experiment

Options:

- A. Evaluate on more NFS sequences.
- B. Evaluate on full UAV123 or more UAV123 sequences.
- C. Run longer HPC training.
- D. Add target-region feature consistency.
- E. Add response consistency again.
- F. Add new architecture modules.
- G. Prepare paper-level experiment plan.

Recommended fastest high-quality next step: **Evaluate more NFS/UAV123 sequences and inspect failures before changing architecture.** This recommendation is based only on the parsed results.

## 9. What to postpone

- degradation token
- template-guided scan
- memory update
- response fusion
- final paper claims

## 10. Decision

Decision: **evaluate more NFS/UAV123 sequences**.

## 11. Final detailed table

| sequence | condition | baseline AUC | HPC RG-SSB AUC | AUC change | baseline Precision@20 | HPC Precision@20 | center error change | best model | note |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| nfs_Gymnastics | clean | 0.311558 | 0.334912 | +0.023354 | 0.002717 | 0.002717 | +12.789764 | hpc_rgssb | HPC RG-SSB improves AUC over baseline |
| nfs_Gymnastics | motion_blur_medium | 0.313038 | 0.333244 | +0.020206 | 0.002717 | 0.002717 | +14.322418 | hpc_rgssb | HPC RG-SSB improves AUC over baseline |
| nfs_Gymnastics | low_resolution_medium | 0.311558 | 0.334992 | +0.023434 | 0.002717 | 0.002717 | +13.576279 | hpc_rgssb | HPC RG-SSB improves AUC over baseline |
| nfs_Gymnastics | gaussian_noise_medium | 0.299801 | 0.320652 | +0.020851 | 0.002717 | 0.002717 | +10.529908 | hpc_rgssb | HPC RG-SSB improves AUC over baseline |
| nfs_basketball_player | clean | 0.338378 | 0.338163 | -0.000215 | 0.005420 | 0.013550 | +6.305512 | baseline | OSTrack baseline is slightly higher by AUC |
| nfs_basketball_player | motion_blur_medium | 0.331777 | 0.328289 | -0.003488 | 0.008130 | 0.008130 | +14.262650 | baseline | OSTrack baseline is slightly higher by AUC |
| nfs_basketball_player | low_resolution_medium | 0.339424 | 0.327645 | -0.011779 | 0.005420 | 0.008130 | +18.110627 | baseline | OSTrack baseline is clearly higher by AUC |
| nfs_basketball_player | gaussian_noise_medium | 0.383482 | 0.388553 | +0.005071 | 0.016260 | 0.016260 | +1.277756 | hpc_rgssb | HPC RG-SSB is slightly higher by AUC |
| nfs_car | clean | 0.091658 | 0.157460 | +0.065802 | 0.000495 | 0.000495 | -112.925965 | hpc_rgssb | HPC RG-SSB improves AUC over baseline |
| nfs_car | motion_blur_medium | 0.079914 | 0.136663 | +0.056749 | 0.000495 | 0.000495 | -139.422364 | hpc_rgssb | HPC RG-SSB improves AUC over baseline |
| nfs_car | low_resolution_medium | 0.091089 | 0.146505 | +0.055416 | 0.000495 | 0.000495 | -83.351990 | hpc_rgssb | HPC RG-SSB improves AUC over baseline |
| nfs_car | gaussian_noise_medium | 0.073895 | 0.125498 | +0.051603 | 0.000495 | 0.000495 | -347.725677 | hpc_rgssb | HPC RG-SSB improves AUC over baseline |
| nfs_dog | clean | 0.419264 | 0.414563 | -0.004701 | 0.005825 | 0.006796 | +12.790558 | baseline | OSTrack baseline is slightly higher by AUC |
| nfs_dog | motion_blur_medium | 0.432145 | 0.417860 | -0.014285 | 0.008738 | 0.004854 | +21.766358 | baseline | OSTrack baseline is clearly higher by AUC |
| nfs_dog | low_resolution_medium | 0.419168 | 0.414390 | -0.004778 | 0.008738 | 0.003883 | +11.150955 | baseline | OSTrack baseline is slightly higher by AUC |
| nfs_dog | gaussian_noise_medium | 0.429828 | 0.428280 | -0.001548 | 0.003883 | 0.003883 | -0.099121 | baseline | OSTrack baseline is slightly higher by AUC |
| nfs_running | clean | 0.483116 | 0.480878 | -0.002238 | 0.032496 | 0.031019 | +21.415420 | baseline | OSTrack baseline is slightly higher by AUC |
| nfs_running | motion_blur_medium | 0.484681 | 0.474253 | -0.010428 | 0.035451 | 0.032496 | +37.058136 | baseline | OSTrack baseline is clearly higher by AUC |
| nfs_running | low_resolution_medium | 0.482589 | 0.471372 | -0.011217 | 0.033973 | 0.035451 | +29.408661 | baseline | OSTrack baseline is clearly higher by AUC |
| nfs_running | gaussian_noise_medium | 0.487664 | 0.512278 | +0.024614 | 0.023634 | 0.016248 | -3.932640 | hpc_rgssb | HPC RG-SSB improves AUC over baseline |
| nfs_bottle | clean | 0.368912 | 0.340264 | -0.028648 | 0.023300 | 0.023300 | +28.393005 | baseline | OSTrack baseline is clearly higher by AUC |
| nfs_bottle | motion_blur_medium | 0.367636 | 0.337726 | -0.029910 | 0.023300 | 0.024727 | +30.628571 | baseline | OSTrack baseline is clearly higher by AUC |
| nfs_bottle | low_resolution_medium | 0.368149 | 0.338526 | -0.029623 | 0.020922 | 0.023776 | +30.119598 | baseline | OSTrack baseline is clearly higher by AUC |
| nfs_bottle | gaussian_noise_medium | 0.390541 | 0.368973 | -0.021568 | 0.016643 | 0.018069 | +26.086105 | baseline | OSTrack baseline is clearly higher by AUC |
| nfs_bird_2 | clean | 0.252434 | 0.259360 | +0.006926 | 0.006303 | 0.010504 | -39.268296 | hpc_rgssb | HPC RG-SSB is slightly higher by AUC |
| nfs_bird_2 | motion_blur_medium | 0.253682 | 0.272964 | +0.019282 | 0.010504 | 0.010504 | -23.221130 | hpc_rgssb | HPC RG-SSB improves AUC over baseline |
| nfs_bird_2 | low_resolution_medium | 0.250957 | 0.272007 | +0.021050 | 0.006303 | 0.012605 | -34.315796 | hpc_rgssb | HPC RG-SSB improves AUC over baseline |
| nfs_bird_2 | gaussian_noise_medium | 0.276521 | 0.260275 | -0.016246 | 0.012605 | 0.010504 | -8.426941 | baseline | OSTrack baseline is clearly higher by AUC |
| nfs_walking | clean | 0.222442 | 0.367193 | +0.144751 | 0.030631 | 0.041441 | -54.278015 | hpc_rgssb | HPC RG-SSB improves AUC over baseline |
| nfs_walking | motion_blur_medium | 0.404799 | 0.239247 | -0.165552 | 0.037838 | 0.023423 | +48.305969 | baseline | OSTrack baseline is clearly higher by AUC |
| nfs_walking | low_resolution_medium | 0.222977 | 0.239408 | +0.016431 | 0.023423 | 0.028829 | -23.405518 | hpc_rgssb | HPC RG-SSB improves AUC over baseline |
| nfs_walking | gaussian_noise_medium | 0.584444 | 0.300009 | -0.284435 | 0.086486 | 0.021622 | +92.845772 | baseline | OSTrack baseline is clearly higher by AUC |

## 12. Average condition table

| condition | average baseline AUC | average HPC RG-SSB AUC | average AUC change | average Precision@20 change | average center-error change | decision note |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| clean | 0.310970 | 0.336599 | +0.025629 | +0.002829 | -15.597252 | RG-SSB improves clearly on average |
| motion_blur_medium | 0.333459 | 0.317531 | -0.015928 | -0.002478 | +0.462576 | OSTrack remains clearly better on average |
| low_resolution_medium | 0.310739 | 0.318106 | +0.007367 | +0.001737 | -4.838398 | RG-SSB improves slightly on average |
| gaussian_noise_medium | 0.365772 | 0.338065 | -0.027707 | -0.009116 | -28.680605 | OSTrack remains clearly better on average |

## 13. Average sequence table

| sequence | average baseline AUC | average HPC RG-SSB AUC | average AUC change | improved overall yes/no | note |
| --- | ---: | ---: | ---: | --- | --- |
| nfs_Gymnastics | 0.308989 | 0.330950 | +0.021961 | yes | Improves overall |
| nfs_basketball_player | 0.348265 | 0.345662 | -0.002603 | no | Near tie overall |
| nfs_car | 0.084139 | 0.141532 | +0.057392 | yes | Improves overall |
| nfs_dog | 0.425101 | 0.418773 | -0.006328 | no | Near tie overall |
| nfs_running | 0.484513 | 0.484695 | +0.000183 | yes | Slight overall improvement |
| nfs_bottle | 0.373810 | 0.346372 | -0.027437 | no | Worsens overall |
| nfs_bird_2 | 0.258398 | 0.266151 | +0.007753 | yes | Slight overall improvement |
| nfs_walking | 0.358665 | 0.286464 | -0.072201 | no | Worsens overall |

## Verification

- Parsed `experiments/baseline_results.csv` with Python.
- Created `experiments/rgssb_hpc_nfs_comparison.csv`.
- Created `implementation/rgssb_hpc_nfs_result_analysis.md`.
- Compared 32 sequence-condition pairs with one baseline row and one HPC RG-SSB row per pair.
- Preserved NaN center-error values in the detailed CSV and ignored NaN pairwise center-error changes in averages.
- Did not run OSTrack.
- Did not run training or evaluation.
- Did not modify datasets or `external/OSTrack`.

Uncertain fields:

- Each degraded condition uses one seed, `42`.
- Each degradation uses medium severity only.
- The NFS subset contains 8 selected sequences, not the full benchmark.
- The report compares parsed CSV metrics only and does not inspect qualitative tracking failures.
