# RG-SSB HPC Broader OTB Result Analysis

Inputs:

- `experiments/baseline_results.csv`
- `implementation/hpc_broader_otb_evaluation_plan.md`
- `implementation/rgssb_hpc_featcons_lam002_result_analysis.md`
- `experiments/rgssb_hpc_featcons_lam002_comparison.csv`

## 1. Executive summary

The HPC RG-SSB + head feature-consistency lambda `0.02` model improves over the original OSTrack baseline across the broader 13-sequence OTB set: baseline average AUC `0.646964`, HPC RG-SSB average AUC `0.680108`, change `+0.033144` across 52 sequence-condition pairs.
Average Precision@20 change is `+0.050250` and average center-error change is `-4.563202`. Lower center error is better, so the center-error average indicates improvement.

## 2. Technical status

- Broader OTB baseline evaluation completed.
- Broader HPC RG-SSB evaluation completed.
- 13 sequences and 4 conditions were evaluated.
- CSV logging works.
- This is stronger evidence than the 3-sequence local proof-of-concept.
- This is still not final paper-scale evidence.

## 3. Per-condition summary

### clean

Average baseline AUC `0.685161`, average HPC RG-SSB AUC `0.702342`, AUC change `+0.017181`. Average Precision@20 change `+0.034530`; average center-error change `-2.393782`. On this condition, RG-SSB helps on average by AUC.

### motion_blur_medium

Average baseline AUC `0.606603`, average HPC RG-SSB AUC `0.654005`, AUC change `+0.047403`. Average Precision@20 change `+0.057504`; average center-error change `-8.093379`. On this condition, RG-SSB helps on average by AUC.

### low_resolution_medium

Average baseline AUC `0.629297`, average HPC RG-SSB AUC `0.675759`, AUC change `+0.046462`. Average Precision@20 change `+0.074568`; average center-error change `-4.934272`. On this condition, RG-SSB helps on average by AUC.

### gaussian_noise_medium

Average baseline AUC `0.666797`, average HPC RG-SSB AUC `0.688327`, AUC change `+0.021530`. Average Precision@20 change `+0.034399`; average center-error change `-2.831376`. On this condition, RG-SSB helps on average by AUC.

## 4. Per-sequence summary

Improved overall sequences: Car1, David2, Coke, Walking, Walking2, FaceOcc1, Dog1, Deer, Football, BlurCar2, BlurFace.
Worsened overall sequences: BlurBody, Box.
Strongest average gains: Walking2 (+0.205431), Deer (+0.140078), Football (+0.042831).
Largest average drops: BlurBody (-0.027732), Box (-0.009781).
Sequences where RG-SSB is consistently better across all four conditions: Car1, Coke, Walking2, FaceOcc1, Deer, BlurCar2.
Sequences where OSTrack remains better across all four conditions: BlurBody, Box.

### Car1

Average baseline AUC `0.288840`, average HPC RG-SSB AUC `0.324027`, change `+0.035188`. Improvements: clean (+0.038245), motion_blur_medium (+0.036042), low_resolution_medium (+0.012939), gaussian_noise_medium (+0.053524). Drops: none.

### David2

Average baseline AUC `0.741980`, average HPC RG-SSB AUC `0.749041`, change `+0.007062`. Improvements: clean (+0.003227), motion_blur_medium (+0.067279). Drops: low_resolution_medium (-0.004057), gaussian_noise_medium (-0.038203).

### Coke

Average baseline AUC `0.737819`, average HPC RG-SSB AUC `0.745841`, change `+0.008022`. Improvements: clean (+0.004492), motion_blur_medium (+0.021742), low_resolution_medium (+0.004151), gaussian_noise_medium (+0.001701). Drops: none.

### Walking

Average baseline AUC `0.782034`, average HPC RG-SSB AUC `0.784191`, change `+0.002157`. Improvements: motion_blur_medium (+0.028285). Drops: clean (-0.006368), low_resolution_medium (-0.008363), gaussian_noise_medium (-0.004926).

### Walking2

Average baseline AUC `0.500955`, average HPC RG-SSB AUC `0.706386`, change `+0.205431`. Improvements: clean (+0.036654), motion_blur_medium (+0.067763), low_resolution_medium (+0.454515), gaussian_noise_medium (+0.262792). Drops: none.

### FaceOcc1

Average baseline AUC `0.611394`, average HPC RG-SSB AUC `0.625341`, change `+0.013947`. Improvements: clean (+0.012077), motion_blur_medium (+0.020657), low_resolution_medium (+0.012643), gaussian_noise_medium (+0.010412). Drops: none.

### Dog1

Average baseline AUC `0.857869`, average HPC RG-SSB AUC `0.862015`, change `+0.004146`. Improvements: clean (+0.001738), motion_blur_medium (+0.023264). Drops: low_resolution_medium (-0.003872), gaussian_noise_medium (-0.004547).

### Deer

Average baseline AUC `0.315053`, average HPC RG-SSB AUC `0.455132`, change `+0.140078`. Improvements: clean (+0.153117), motion_blur_medium (+0.227165), low_resolution_medium (+0.171246), gaussian_noise_medium (+0.008785). Drops: none.

### Football

Average baseline AUC `0.218554`, average HPC RG-SSB AUC `0.261385`, change `+0.042831`. Improvements: motion_blur_medium (+0.166730), gaussian_noise_medium (+0.005880). Drops: clean (-0.000602), low_resolution_medium (-0.000684).

### BlurBody

Average baseline AUC `0.832758`, average HPC RG-SSB AUC `0.805026`, change `-0.027732`. Improvements: none. Drops: clean (-0.032608), motion_blur_medium (-0.029051), low_resolution_medium (-0.027835), gaussian_noise_medium (-0.021433).

### BlurCar2

Average baseline AUC `0.850135`, average HPC RG-SSB AUC `0.858458`, change `+0.008323`. Improvements: clean (+0.011475), motion_blur_medium (+0.006533), low_resolution_medium (+0.008395), gaussian_noise_medium (+0.006888). Drops: none.

### BlurFace

Average baseline AUC `0.824895`, average HPC RG-SSB AUC `0.826095`, change `+0.001200`. Improvements: clean (+0.004358), low_resolution_medium (+0.001968), gaussian_noise_medium (+0.000422). Drops: motion_blur_medium (-0.001948).

### Box

Average baseline AUC `0.848251`, average HPC RG-SSB AUC `0.838469`, change `-0.009781`. Improvements: none. Drops: clean (-0.002456), motion_blur_medium (-0.018224), low_resolution_medium (-0.017039), gaussian_noise_medium (-0.001407).

## 5. Main finding

The broader OTB result shows broader robustness potential for RG-SSB because the average AUC change over baseline is `+0.033144` across 52 comparisons. This supports continuing to paper-scale experiments, but it should not be presented as a final paper claim yet. Remaining weaknesses include sequence-specific drops, a single degradation severity and seed, evaluation on OTB only, and no comparison yet on UAV123, NFS, TrackingNet, or other broader benchmarks.

## 6. Likely reasons for gains or drops

- Degradation-aware training likely helps under synthetic motion blur, low resolution, and Gaussian noise when the adaptation matches the evaluation corruption.
- Feature consistency lambda `0.02` may provide a useful but relatively light clean-degraded alignment signal.
- RG-SSB + head adaptation changes only the restoration-oriented block and box head while keeping the backbone frozen, limiting overfitting risk but also limiting adaptation capacity.
- The model was trained only on LaSOT, so OTB sequence behavior can vary with target size, occlusion, blur, background clutter, and annotation style.
- Response consistency is not used in this setup, so localization-map alignment is not directly constrained.
- There is no target-region weighting, so feature consistency is global rather than focused on the object region.
- There is no degradation token, memory module, template-guided scan, or response fusion; the result reflects the current minimal architecture change.

## 7. Recommended next experiment

Options:

- A. Evaluate on UAV123.
- B. Evaluate on NFS.
- C. Evaluate on additional OTB sequences.
- D. Run longer HPC training.
- E. Add target-region feature consistency.
- F. Add response consistency again.
- G. Add new architecture modules.

Recommended fastest high-quality next step: **Evaluate on UAV123 or NFS before adding new architecture modules.** This recommendation is based only on the parsed results. Since the broader OTB average is positive, one additional benchmark is more informative than changing the architecture now.

## 8. What to postpone

- degradation token
- template-guided scan
- memory update
- response fusion
- final paper claims

## 9. Decision

Decision: **proceed to broader benchmark evaluation**.

## 10. Final detailed table

| sequence | condition | baseline AUC | HPC RG-SSB AUC | AUC change | baseline Precision@20 | HPC Precision@20 | center error change | best model | note |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| Car1 | clean | 0.575995 | 0.614240 | +0.038245 | 0.746078 | 0.806863 | -3.274851 | hpc_rgssb | HPC RG-SSB improves AUC over baseline |
| Car1 | motion_blur_medium | 0.157212 | 0.193254 | +0.036042 | 0.198039 | 0.259804 | -7.056549 | hpc_rgssb | HPC RG-SSB improves AUC over baseline |
| Car1 | low_resolution_medium | 0.214881 | 0.227820 | +0.012939 | 0.267647 | 0.301961 | +2.183479 | hpc_rgssb | HPC RG-SSB improves AUC over baseline |
| Car1 | gaussian_noise_medium | 0.207270 | 0.260794 | +0.053524 | 0.250980 | 0.329412 | -7.751110 | hpc_rgssb | HPC RG-SSB improves AUC over baseline |
| David2 | clean | 0.794439 | 0.797666 | +0.003227 | 1.000000 | 1.000000 | -0.014071 | hpc_rgssb | HPC RG-SSB improves AUC over baseline |
| David2 | motion_blur_medium | 0.549680 | 0.616959 | +0.067279 | 0.970205 | 0.970205 | -1.869067 | hpc_rgssb | HPC RG-SSB improves AUC over baseline |
| David2 | low_resolution_medium | 0.806258 | 0.802201 | -0.004057 | 1.000000 | 1.000000 | -0.023843 | baseline | OSTrack baseline has higher AUC |
| David2 | gaussian_noise_medium | 0.817542 | 0.779339 | -0.038203 | 1.000000 | 0.988827 | +0.690411 | baseline | OSTrack baseline has higher AUC |
| Coke | clean | 0.758259 | 0.762751 | +0.004492 | 0.958763 | 0.958763 | +0.461617 | hpc_rgssb | HPC RG-SSB improves AUC over baseline |
| Coke | motion_blur_medium | 0.700384 | 0.722126 | +0.021742 | 0.945017 | 0.934708 | +0.253159 | hpc_rgssb | HPC RG-SSB improves AUC over baseline |
| Coke | low_resolution_medium | 0.745875 | 0.750026 | +0.004151 | 0.945017 | 0.948454 | +0.517938 | hpc_rgssb | HPC RG-SSB improves AUC over baseline |
| Coke | gaussian_noise_medium | 0.746759 | 0.748460 | +0.001701 | 0.951890 | 0.945017 | +0.242024 | hpc_rgssb | HPC RG-SSB improves AUC over baseline |
| Walking | clean | 0.787297 | 0.780929 | -0.006368 | 1.000000 | 1.000000 | +0.110742 | baseline | OSTrack baseline has higher AUC |
| Walking | motion_blur_medium | 0.759276 | 0.787561 | +0.028285 | 1.000000 | 1.000000 | +0.096197 | hpc_rgssb | HPC RG-SSB improves AUC over baseline |
| Walking | low_resolution_medium | 0.788114 | 0.779751 | -0.008363 | 1.000000 | 1.000000 | +0.142411 | baseline | OSTrack baseline has higher AUC |
| Walking | gaussian_noise_medium | 0.793449 | 0.788523 | -0.004926 | 1.000000 | 1.000000 | +0.096453 | baseline | OSTrack baseline has higher AUC |
| Walking2 | clean | 0.784772 | 0.821426 | +0.036654 | 0.924000 | 1.000000 | -3.445851 | hpc_rgssb | HPC RG-SSB improves AUC over baseline |
| Walking2 | motion_blur_medium | 0.377287 | 0.445050 | +0.067763 | 0.550000 | 0.614000 | -3.848328 | hpc_rgssb | HPC RG-SSB improves AUC over baseline |
| Walking2 | low_resolution_medium | 0.364673 | 0.819188 | +0.454515 | 0.398000 | 1.000000 | -46.092053 | hpc_rgssb | HPC RG-SSB improves AUC over baseline |
| Walking2 | gaussian_noise_medium | 0.477089 | 0.739881 | +0.262792 | 0.604000 | 0.938000 | -26.107455 | hpc_rgssb | HPC RG-SSB improves AUC over baseline |
| FaceOcc1 | clean | 0.586478 | 0.598555 | +0.012077 | 0.547085 | 0.567265 | +0.358234 | hpc_rgssb | HPC RG-SSB improves AUC over baseline |
| FaceOcc1 | motion_blur_medium | 0.609943 | 0.630600 | +0.020657 | 0.634529 | 0.671525 | +0.329286 | hpc_rgssb | HPC RG-SSB improves AUC over baseline |
| FaceOcc1 | low_resolution_medium | 0.599476 | 0.612119 | +0.012643 | 0.614350 | 0.591928 | +0.426672 | hpc_rgssb | HPC RG-SSB improves AUC over baseline |
| FaceOcc1 | gaussian_noise_medium | 0.649680 | 0.660092 | +0.010412 | 0.705157 | 0.746637 | -1.062599 | hpc_rgssb | HPC RG-SSB improves AUC over baseline |
| Dog1 | clean | 0.861188 | 0.862926 | +0.001738 | 1.000000 | 1.000000 | -0.065019 | hpc_rgssb | HPC RG-SSB improves AUC over baseline |
| Dog1 | motion_blur_medium | 0.834389 | 0.857653 | +0.023264 | 1.000000 | 1.000000 | -0.273772 | hpc_rgssb | HPC RG-SSB improves AUC over baseline |
| Dog1 | low_resolution_medium | 0.874939 | 0.871067 | -0.003872 | 1.000000 | 1.000000 | +0.027244 | baseline | OSTrack baseline has higher AUC |
| Dog1 | gaussian_noise_medium | 0.860961 | 0.856414 | -0.004547 | 1.000000 | 1.000000 | -0.108740 | baseline | OSTrack baseline has higher AUC |
| Deer | clean | 0.271231 | 0.424348 | +0.153117 | 0.366197 | 0.661972 | -31.865010 | hpc_rgssb | HPC RG-SSB improves AUC over baseline |
| Deer | motion_blur_medium | 0.208339 | 0.435504 | +0.227165 | 0.281690 | 0.647887 | -61.908870 | hpc_rgssb | HPC RG-SSB improves AUC over baseline |
| Deer | low_resolution_medium | 0.267187 | 0.438433 | +0.171246 | 0.338028 | 0.704225 | -33.476219 | hpc_rgssb | HPC RG-SSB improves AUC over baseline |
| Deer | gaussian_noise_medium | 0.513457 | 0.522242 | +0.008785 | 0.746479 | 0.746479 | -2.376277 | hpc_rgssb | HPC RG-SSB improves AUC over baseline |
| Football | clean | 0.138997 | 0.138395 | -0.000602 | 0.165746 | 0.165746 | +6.521927 | baseline | OSTrack baseline has higher AUC |
| Football | motion_blur_medium | 0.324955 | 0.491685 | +0.166730 | 0.497238 | 0.740331 | -38.014608 | hpc_rgssb | HPC RG-SSB improves AUC over baseline |
| Football | low_resolution_medium | 0.144412 | 0.143728 | -0.000684 | 0.171271 | 0.165746 | +7.177093 | baseline | OSTrack baseline has higher AUC |
| Football | gaussian_noise_medium | 0.265850 | 0.271730 | +0.005880 | 0.356354 | 0.364641 | -0.217575 | hpc_rgssb | HPC RG-SSB improves AUC over baseline |
| BlurBody | clean | 0.835240 | 0.802632 | -0.032608 | 0.976048 | 0.973054 | +0.038402 | baseline | OSTrack baseline has higher AUC |
| BlurBody | motion_blur_medium | 0.846446 | 0.817395 | -0.029051 | 0.985030 | 0.982036 | +0.376382 | baseline | OSTrack baseline has higher AUC |
| BlurBody | low_resolution_medium | 0.840932 | 0.813097 | -0.027835 | 0.982036 | 0.982036 | +0.085330 | baseline | OSTrack baseline has higher AUC |
| BlurBody | gaussian_noise_medium | 0.808413 | 0.786980 | -0.021433 | 0.982036 | 0.979042 | -0.161147 | baseline | OSTrack baseline has higher AUC |
| BlurCar2 | clean | 0.847863 | 0.859338 | +0.011475 | 1.000000 | 1.000000 | -0.102214 | hpc_rgssb | HPC RG-SSB improves AUC over baseline |
| BlurCar2 | motion_blur_medium | 0.844309 | 0.850842 | +0.006533 | 1.000000 | 1.000000 | +0.098410 | hpc_rgssb | HPC RG-SSB improves AUC over baseline |
| BlurCar2 | low_resolution_medium | 0.852348 | 0.860743 | +0.008395 | 1.000000 | 1.000000 | -0.055330 | hpc_rgssb | HPC RG-SSB improves AUC over baseline |
| BlurCar2 | gaussian_noise_medium | 0.856021 | 0.862909 | +0.006888 | 1.000000 | 1.000000 | -0.135860 | hpc_rgssb | HPC RG-SSB improves AUC over baseline |
| BlurFace | clean | 0.820959 | 0.825317 | +0.004358 | 1.000000 | 1.000000 | +0.178871 | hpc_rgssb | HPC RG-SSB improves AUC over baseline |
| BlurFace | motion_blur_medium | 0.836985 | 0.835037 | -0.001948 | 1.000000 | 1.000000 | +0.247937 | baseline | OSTrack baseline has higher AUC |
| BlurFace | low_resolution_medium | 0.824413 | 0.826381 | +0.001968 | 1.000000 | 1.000000 | +0.196004 | hpc_rgssb | HPC RG-SSB improves AUC over baseline |
| BlurFace | gaussian_noise_medium | 0.817223 | 0.817645 | +0.000422 | 1.000000 | 1.000000 | +0.156674 | hpc_rgssb | HPC RG-SSB improves AUC over baseline |
| Box | clean | 0.844373 | 0.841917 | -0.002456 | 0.955211 | 0.954350 | -0.021937 | baseline | OSTrack baseline has higher AUC |
| Box | motion_blur_medium | 0.836629 | 0.818405 | -0.018224 | 0.962102 | 0.950904 | +6.355896 | baseline | OSTrack baseline has higher AUC |
| Box | low_resolution_medium | 0.857352 | 0.840313 | -0.017039 | 0.966408 | 0.957795 | +4.745732 | baseline | OSTrack baseline has higher AUC |
| Box | gaussian_noise_medium | 0.854649 | 0.853242 | -0.001407 | 0.973299 | 0.979328 | -0.072690 | baseline | OSTrack baseline has higher AUC |

## 11. Average condition table

| condition | average baseline AUC | average HPC RG-SSB AUC | average AUC change | average Precision@20 change | average center-error change | decision note |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| clean | 0.685161 | 0.702342 | +0.017181 | +0.034530 | -2.393782 | RG-SSB improves clearly on average |
| motion_blur_medium | 0.606603 | 0.654005 | +0.047403 | +0.057504 | -8.093379 | RG-SSB improves clearly on average |
| low_resolution_medium | 0.629297 | 0.675759 | +0.046462 | +0.074568 | -4.934272 | RG-SSB improves clearly on average |
| gaussian_noise_medium | 0.666797 | 0.688327 | +0.021530 | +0.034399 | -2.831376 | RG-SSB improves clearly on average |

## 12. Average sequence table

| sequence | average baseline AUC | average HPC RG-SSB AUC | average AUC change | improved overall yes/no | note |
| --- | ---: | ---: | ---: | --- | --- |
| Car1 | 0.288840 | 0.324027 | +0.035188 | yes | Improves overall |
| David2 | 0.741980 | 0.749041 | +0.007062 | yes | Slight overall improvement |
| Coke | 0.737819 | 0.745841 | +0.008022 | yes | Slight overall improvement |
| Walking | 0.782034 | 0.784191 | +0.002157 | yes | Slight overall improvement |
| Walking2 | 0.500955 | 0.706386 | +0.205431 | yes | Improves overall |
| FaceOcc1 | 0.611394 | 0.625341 | +0.013947 | yes | Improves overall |
| Dog1 | 0.857869 | 0.862015 | +0.004146 | yes | Slight overall improvement |
| Deer | 0.315053 | 0.455132 | +0.140078 | yes | Improves overall |
| Football | 0.218554 | 0.261385 | +0.042831 | yes | Improves overall |
| BlurBody | 0.832758 | 0.805026 | -0.027732 | no | Worsens overall |
| BlurCar2 | 0.850135 | 0.858458 | +0.008323 | yes | Slight overall improvement |
| BlurFace | 0.824895 | 0.826095 | +0.001200 | yes | Slight overall improvement |
| Box | 0.848251 | 0.838469 | -0.009781 | no | Near tie overall |

## Verification

- Parsed `experiments/baseline_results.csv` with Python.
- Created `experiments/rgssb_hpc_broader_otb_comparison.csv`.
- Created `implementation/rgssb_hpc_broader_otb_result_analysis.md`.
- Compared 52 sequence-condition pairs with one baseline row and one HPC RG-SSB row per pair.
- Did not run OSTrack.
- Did not run training or evaluation.
- Did not modify datasets or `external/OSTrack`.

Uncertain fields:

- Each degraded condition uses one seed, `42`.
- Each degradation uses medium severity only.
- This broader OTB analysis is stronger than the 3-sequence proof-of-concept, but it is still not final paper-scale evidence.
