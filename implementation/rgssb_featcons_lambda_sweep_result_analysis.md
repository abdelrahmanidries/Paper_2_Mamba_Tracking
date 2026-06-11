# RG-SSB Feature-Consistency Lambda Sweep Result Analysis

Inputs:

- `experiments/baseline_results.csv`
- `implementation/rgssb_feature_consistency_3000_result_analysis.md`
- `implementation/featcons_lambda_sweep_plan.md`
- `implementation/rgssb_head_3000_result_analysis.md`
- `implementation/rgssb_head_balanced_3000_result_analysis.md`

## 1. Executive summary

Best feature-consistency lambda overall is `0.02` with average AUC `0.613026` across the 12 sequence-condition pairs. The best setup overall is `lambda_0.02` with average AUC `0.613026`.

Feature consistency with the best lambda is also the strongest setup in this local comparison. It improves over the previous fully degraded 3000-sample setup on average, but this is still local proof-of-concept evidence rather than final paper evidence.

## 2. Technical status

- Lambda `0.02` and lambda `0.10` cycles completed.
- Lambda `0.05` was the original feature-consistency run.
- Three-sequence evaluation completed for Car1, David2, and Coke.
- CSV logging works through `experiments/baseline_results.csv`.
- This is still local proof-of-concept evidence, not final paper evidence.

## 3. Per-lambda summary

### Lambda 0.02

- Overall average AUC: `0.613026`.
- Average AUC change vs baseline: `+0.023480`.
- Average AUC change vs fully degraded 3000: `+0.012622`.
- Improves over baseline on `8/12` sequence-condition pairs and drops on `4/12`.
- Improves over fully degraded 3000 on `6/12` sequence-condition pairs and drops on `6/12`.
- Best feature-consistency lambda on `5/12` sequence-condition pairs.
- Strongest lambda cases: Car1 low_resolution_medium (0.231528), Car1 gaussian_noise_medium (0.465211), David2 clean (0.786880), David2 low_resolution_medium (0.792485), Coke low_resolution_medium (0.760777).
- Drops below baseline on: David2 clean (-0.007559), David2 motion_blur_medium (-0.010749), David2 low_resolution_medium (-0.013773), David2 gaussian_noise_medium (-0.049432).

### Lambda 0.05

- Overall average AUC: `0.594527`.
- Average AUC change vs baseline: `+0.004981`.
- Average AUC change vs fully degraded 3000: `-0.005876`.
- Improves over baseline on `6/12` sequence-condition pairs and drops on `6/12`.
- Improves over fully degraded 3000 on `5/12` sequence-condition pairs and drops on `7/12`.
- Best feature-consistency lambda on `4/12` sequence-condition pairs.
- Strongest lambda cases: Car1 motion_blur_medium (0.185556), David2 motion_blur_medium (0.541678), David2 gaussian_noise_medium (0.773291), Coke gaussian_noise_medium (0.767990).
- Drops below baseline on: Car1 clean (-0.002796), Car1 low_resolution_medium (-0.009154), David2 clean (-0.010989), David2 motion_blur_medium (-0.008002), David2 low_resolution_medium (-0.015857), David2 gaussian_noise_medium (-0.044251).

### Lambda 0.10

- Overall average AUC: `0.601905`.
- Average AUC change vs baseline: `+0.012359`.
- Average AUC change vs fully degraded 3000: `+0.001502`.
- Improves over baseline on `8/12` sequence-condition pairs and drops on `4/12`.
- Improves over fully degraded 3000 on `6/12` sequence-condition pairs and drops on `6/12`.
- Best feature-consistency lambda on `3/12` sequence-condition pairs.
- Strongest lambda cases: Car1 clean (0.649913), Coke clean (0.773434), Coke motion_blur_medium (0.729645).
- Drops below baseline on: David2 clean (-0.012316), David2 motion_blur_medium (-0.011136), David2 low_resolution_medium (-0.017829), David2 gaussian_noise_medium (-0.049026).

## 4. Per-condition average summary

| condition | baseline | full3000 | balanced3000 | lambda 0.02 | lambda 0.05 | lambda 0.10 | best lambda | best model |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| clean | 0.709564 | 0.727378 | 0.724156 | 0.713036 | 0.708599 | 0.735157 | 0.10 | lambda_0.10 |
| motion_blur_medium | 0.469092 | 0.494887 | 0.474446 | 0.477794 | 0.485241 | 0.484459 | 0.05 | full3000 |
| low_resolution_medium | 0.589005 | 0.593881 | 0.586538 | 0.594930 | 0.585170 | 0.591649 | 0.02 | lambda_0.02 |
| gaussian_noise_medium | 0.590524 | 0.585468 | 0.584542 | 0.666344 | 0.599100 | 0.596357 | 0.02 | lambda_0.02 |

Best feature-consistency lambda by condition:

- clean: lambda `0.10`.
- motion_blur_medium: lambda `0.05`.
- low_resolution_medium: lambda `0.02`.
- gaussian_noise_medium: lambda `0.02`.

## 5. Overall average summary

| setup | overall average AUC |
| --- | ---: |
| baseline | 0.589546 |
| fully degraded 3000 | 0.600403 |
| balanced 3000 | 0.592421 |
| feature consistency lambda 0.02 | 0.613026 |
| feature consistency lambda 0.05 | 0.594527 |
| feature consistency lambda 0.10 | 0.601905 |

Best overall model: `lambda_0.02`. Best overall feature-consistency lambda: `0.02`.

Average AUC changes:

- Lambda `0.02` vs baseline: `+0.023480`; vs fully degraded 3000: `+0.012622`.
- Lambda `0.05` vs baseline: `+0.004981`; vs fully degraded 3000: `-0.005876`.
- Lambda `0.10` vs baseline: `+0.012359`; vs fully degraded 3000: `+0.001502`.

## 6. Main finding

Lambda tuning helped: lambda `0.02` is better than the original lambda `0.05` on overall average AUC. However, the gain is modest and should not be overclaimed because the comparison covers only three OTB sequences and one seed per degradation condition.
Feature consistency should be kept for the next controlled experiment because the best lambda is above the fully degraded 3000 setup on overall average AUC.
The result justifies one more local training refinement before HPC-scale training only if that refinement is fast and directly tests the loss behavior. It does not justify adding new architecture modules yet.

## 7. Likely reasons

- Lambda controls the strength of clean-degraded feature alignment.
- Too high a lambda may over-constrain features and suppress target-discriminative variation.
- Too low a lambda may be insufficient to stabilize degraded search features.
- The backbone is frozen, so only RG-SSB and the box head can adapt.
- Feature loss is applied only after RG-SSB, not throughout the backbone.
- No response consistency loss is used yet.
- No target-region weighting is used yet.
- `search_only` degradation is still used.

## 8. Recommended next experiment

Options:

- A. Use best lambda and move to HPC-scale training.
- B. Use best lambda and add response consistency.
- C. Use best lambda and add target-region feature consistency.
- D. Train longer locally.
- E. Add new architecture modules.

Recommended fastest high-quality next step: **B. Use the best lambda and add response consistency**.

Reason: the best lambda improves the feature-consistency setup, but condition-level results are still mixed. Response consistency directly tests whether clean-degraded alignment improves the tracker output rather than only internal features. This is a training-objective refinement, not a new architecture module, and it is more diagnostic than simply training longer locally.

## 9. What to postpone

- degradation token
- template-guided scan
- memory update
- response fusion
- final paper claims

## 10. Decision

Decision: **add response consistency using feature-consistency lambda `0.02` as the starting point**.

## 11. Final detailed table

| sequence | condition | baseline AUC | full3000 AUC | balanced3000 AUC | lambda 0.02 AUC | lambda 0.05 AUC | lambda 0.10 AUC | best model | best lambda | note |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |
| Car1 | clean | 0.575995 | 0.627500 | 0.615366 | 0.583557 | 0.573199 | 0.649913 | lambda_0.10 | 0.10 | feature consistency best overall for this pair (lambda_0.10); best lambda beats baseline and full3000 |
| Car1 | motion_blur_medium | 0.157212 | 0.187235 | 0.160775 | 0.167084 | 0.185556 | 0.185187 | full3000 | 0.05 | fully degraded 3000 remains strongest; best lambda is below full3000 |
| Car1 | low_resolution_medium | 0.214881 | 0.230149 | 0.202155 | 0.231528 | 0.205727 | 0.226694 | lambda_0.02 | 0.02 | feature consistency best overall for this pair (lambda_0.02); best lambda beats baseline and full3000 |
| Car1 | gaussian_noise_medium | 0.207270 | 0.220045 | 0.210765 | 0.465211 | 0.256018 | 0.254640 | lambda_0.02 | 0.02 | feature consistency best overall for this pair (lambda_0.02); best lambda beats baseline and full3000 |
| David2 | clean | 0.794439 | 0.795490 | 0.798809 | 0.786880 | 0.783450 | 0.782123 | balanced3000 | 0.02 | balanced 3000 remains strongest; best lambda is below baseline |
| David2 | motion_blur_medium | 0.549680 | 0.578941 | 0.551358 | 0.538931 | 0.541678 | 0.538544 | full3000 | 0.05 | fully degraded 3000 remains strongest; best lambda is below baseline |
| David2 | low_resolution_medium | 0.806258 | 0.802183 | 0.809816 | 0.792485 | 0.790401 | 0.788429 | balanced3000 | 0.02 | balanced 3000 remains strongest; best lambda is below baseline |
| David2 | gaussian_noise_medium | 0.817542 | 0.784428 | 0.788890 | 0.768110 | 0.773291 | 0.768516 | baseline | 0.05 | original baseline remains strongest; best lambda is below baseline |
| Coke | clean | 0.758259 | 0.759144 | 0.758293 | 0.768671 | 0.769147 | 0.773434 | lambda_0.10 | 0.10 | feature consistency best overall for this pair (lambda_0.10); best lambda beats baseline and full3000 |
| Coke | motion_blur_medium | 0.700384 | 0.718485 | 0.711204 | 0.727366 | 0.728488 | 0.729645 | lambda_0.10 | 0.10 | feature consistency best overall for this pair (lambda_0.10); best lambda beats baseline and full3000 |
| Coke | low_resolution_medium | 0.745875 | 0.749311 | 0.747644 | 0.760777 | 0.759382 | 0.759824 | lambda_0.02 | 0.02 | feature consistency best overall for this pair (lambda_0.02); best lambda beats baseline and full3000 |
| Coke | gaussian_noise_medium | 0.746759 | 0.751931 | 0.753972 | 0.765711 | 0.767990 | 0.765915 | lambda_0.05 | 0.05 | feature consistency best overall for this pair (lambda_0.05); best lambda beats baseline and full3000 |

## 12. Average table

| condition | average baseline AUC | average full3000 AUC | average balanced3000 AUC | average lambda 0.02 AUC | average lambda 0.05 AUC | average lambda 0.10 AUC | best average lambda | best average model | decision note |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- | --- |
| clean | 0.709564 | 0.727378 | 0.724156 | 0.713036 | 0.708599 | 0.735157 | 0.10 | lambda_0.10 | feature consistency best overall for this pair (lambda_0.10); best lambda beats baseline and full3000 |
| motion_blur_medium | 0.469092 | 0.494887 | 0.474446 | 0.477794 | 0.485241 | 0.484459 | 0.05 | full3000 | fully degraded 3000 remains strongest; best lambda is below full3000 |
| low_resolution_medium | 0.589005 | 0.593881 | 0.586538 | 0.594930 | 0.585170 | 0.591649 | 0.02 | lambda_0.02 | feature consistency best overall for this pair (lambda_0.02); best lambda beats baseline and full3000 |
| gaussian_noise_medium | 0.590524 | 0.585468 | 0.584542 | 0.666344 | 0.599100 | 0.596357 | 0.02 | lambda_0.02 | feature consistency best overall for this pair (lambda_0.02); best lambda beats baseline and full3000 |

## Verification

- Parsed `experiments/baseline_results.csv` with Python.
- Created `experiments/rgssb_featcons_lambda_sweep_comparison.csv`.
- Created `implementation/rgssb_featcons_lambda_sweep_result_analysis.md`.
- No OSTrack training was run.
- No OSTrack evaluation was run.
- No datasets or `external/OSTrack` files were modified.

Uncertain fields:

- Each degradation condition uses one seed.
- The comparison covers only Car1, David2, and Coke.
- These are local proof-of-concept results, not final paper evidence.
