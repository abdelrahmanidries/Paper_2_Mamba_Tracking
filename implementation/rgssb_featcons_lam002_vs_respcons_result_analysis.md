# RG-SSB Lambda 0.02 Feature Consistency vs Response Consistency Result Analysis

Inputs:

- `experiments/baseline_results.csv`
- `experiments/rgssb_featcons_lambda_sweep_comparison.csv`
- `implementation/rgssb_featcons_lambda_sweep_result_analysis.md`
- `implementation/rgssb_response_consistency_setup_notes.md`

## 1. Executive summary

Response consistency `hurt` the lambda `0.02` feature-consistency setup on overall average AUC. Feature-only average AUC is `0.613026` and feature+response average AUC is `0.593666`, giving a response-consistency gain of `-0.019360` across the 12 sequence-condition pairs.

The result does not support keeping this exact response-consistency setting as the next main setup.

## 2. Technical status

- Lambda `0.02` feature-consistency training completed.
- Response-consistency training completed.
- Three-sequence evaluation completed for Car1, David2, and Coke.
- CSV logging works through `experiments/baseline_results.csv`.
- This is local proof-of-concept evidence, not final paper evidence.

## 3. Per-sequence result summary

### Car1

Average response-consistency gain over feature-only on Car1: `-0.057482` AUC.
Response consistency improves over feature-only on: motion_blur_medium (+0.022792).
Response consistency hurts on: clean (-0.009280), low_resolution_medium (-0.022879), gaussian_noise_medium (-0.220559).
This sequence does not support keeping this exact response-consistency setting.

### David2

Average response-consistency gain over feature-only on David2: `+0.000056` AUC.
Response consistency improves over feature-only on: gaussian_noise_medium (+0.009219).
Response consistency hurts on: clean (-0.003927), motion_blur_medium (-0.004148), low_resolution_medium (-0.000922).
This sequence supports keeping or tuning response consistency, but only as local evidence.

### Coke

Average response-consistency gain over feature-only on Coke: `-0.000655` AUC.
Response consistency improves over feature-only on: clean (+0.000306), gaussian_noise_medium (+0.000272).
Response consistency hurts on: motion_blur_medium (-0.000987), low_resolution_medium (-0.002211).
This sequence does not support keeping this exact response-consistency setting.

## 4. Per-condition average summary

| condition | average baseline AUC | average feature-only AUC | average feature+response AUC | average response gain | average Precision@20 change | average center-error change | decision |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| clean | 0.709564 | 0.713036 | 0.708736 | -0.004300 | -0.006209 | +0.368947 | response consistency hurts this condition on average |
| motion_blur_medium | 0.469092 | 0.477794 | 0.483679 | +0.005886 | +0.015557 | -2.413154 | response consistency helps this condition on average |
| low_resolution_medium | 0.589005 | 0.594930 | 0.586259 | -0.008671 | -0.012418 | +5.250682 | response consistency hurts this condition on average |
| gaussian_noise_medium | 0.590524 | 0.666344 | 0.595988 | -0.070356 | -0.096988 | +11.567173 | response consistency hurts this condition on average |

## 5. Overall average summary

| setup | overall average AUC |
| --- | ---: |
| baseline | 0.589546 |
| feature consistency lambda 0.02 | 0.613026 |
| feature consistency lambda 0.02 + response consistency | 0.593666 |

Response-consistency overall gain over feature-only: `-0.019360` AUC.

## 6. Main finding

Response consistency hurts or fails to improve the feature-only setup overall. It should be dropped or redesigned before further scaling.
This should not be overclaimed: it is three-sequence, local proof-of-concept evidence with one seed per degradation condition.

## 7. Likely reasons

- Response consistency may stabilize localization maps in some cases.
- Response consistency may over-constrain the model when clean and degraded response maps should differ.
- Response consistency weight `0.05` may be too high or too low.
- Response consistency is applied globally, not target-region weighted.
- The backbone is frozen, limiting adaptation capacity.
- Training is local and small.

## 8. Recommended next experiment

Options:

- A. Keep response consistency and tune its weight.
- B. Drop response consistency and keep feature consistency lambda 0.02.
- C. Add target-region response consistency.
- D. Move feature-consistency lambda 0.02 setup to HPC.
- E. Add new architecture modules.

Recommended fastest high-quality next step: **B. Drop response consistency and keep feature consistency lambda 0.02.**

This recommendation is based only on the parsed CSV results. New architecture modules remain premature.

## 9. Decision

Decision: **drop response consistency**.

## 10. Final detailed table

| sequence | condition | baseline AUC | feature-only AUC | feature+response AUC | response gain over feature-only | best model | note |
| --- | --- | ---: | ---: | ---: | ---: | --- | --- |
| Car1 | clean | 0.575995 | 0.583557 | 0.574277 | -0.009280 | feature_only | response consistency hurts; feature-only remains best |
| Car1 | motion_blur_medium | 0.157212 | 0.167084 | 0.189876 | +0.022792 | feature_response | response consistency improves feature-only and is best for this pair |
| Car1 | low_resolution_medium | 0.214881 | 0.231528 | 0.208649 | -0.022879 | feature_only | response consistency hurts; feature-only remains best |
| Car1 | gaussian_noise_medium | 0.207270 | 0.465211 | 0.244652 | -0.220559 | feature_only | response consistency hurts; feature-only remains best |
| David2 | clean | 0.794439 | 0.786880 | 0.782953 | -0.003927 | baseline | response consistency hurts feature-only |
| David2 | motion_blur_medium | 0.549680 | 0.538931 | 0.534783 | -0.004148 | baseline | response consistency hurts feature-only |
| David2 | low_resolution_medium | 0.806258 | 0.792485 | 0.791563 | -0.000922 | baseline | response consistency hurts feature-only |
| David2 | gaussian_noise_medium | 0.817542 | 0.768110 | 0.777329 | +0.009219 | baseline | response consistency improves feature-only but baseline remains stronger |
| Coke | clean | 0.758259 | 0.768671 | 0.768977 | +0.000306 | feature_response | response consistency improves feature-only and is best for this pair |
| Coke | motion_blur_medium | 0.700384 | 0.727366 | 0.726379 | -0.000987 | feature_only | response consistency hurts; feature-only remains best |
| Coke | low_resolution_medium | 0.745875 | 0.760777 | 0.758566 | -0.002211 | feature_only | response consistency hurts; feature-only remains best |
| Coke | gaussian_noise_medium | 0.746759 | 0.765711 | 0.765983 | +0.000272 | feature_response | response consistency improves feature-only and is best for this pair |

## 11. Average table

| condition | average baseline AUC | average feature-only AUC | average feature+response AUC | average response gain | decision note |
| --- | ---: | ---: | ---: | ---: | --- |
| clean | 0.709564 | 0.713036 | 0.708736 | -0.004300 | response consistency hurts this condition on average |
| motion_blur_medium | 0.469092 | 0.477794 | 0.483679 | +0.005886 | response consistency helps this condition on average |
| low_resolution_medium | 0.589005 | 0.594930 | 0.586259 | -0.008671 | response consistency hurts this condition on average |
| gaussian_noise_medium | 0.590524 | 0.666344 | 0.595988 | -0.070356 | response consistency hurts this condition on average |

## Verification

- Parsed `experiments/baseline_results.csv` with Python.
- Created `experiments/rgssb_featcons_lam002_vs_respcons_comparison.csv`.
- Created `implementation/rgssb_featcons_lam002_vs_respcons_result_analysis.md`.
- Did not run OSTrack.
- Did not run training or evaluation.
- Did not modify datasets or `external/OSTrack`.

Uncertain fields:

- Each degradation condition uses one seed.
- The comparison covers only Car1, David2, and Coke.
- These are local proof-of-concept results, not final paper evidence.
