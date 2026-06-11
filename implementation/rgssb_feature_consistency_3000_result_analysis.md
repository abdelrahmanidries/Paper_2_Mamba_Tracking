# Feature-Consistency RG-SSB + Head 3000 Result Analysis

## 1. Executive summary

This report compares the original OSTrack baseline, the fully degraded 3000-sample RG-SSB + head model, the balanced 3000-sample RG-SSB + head model, and the feature-consistency 3000-sample RG-SSB + head model across Car1, David2, and Coke.

The feature-consistency model is a local proof-of-concept result, not a final paper result.

Average feature-consistency AUC change versus the original baseline across the four analyzed conditions is +0.0050. Average change versus the fully degraded 3000 setup is -0.0059. Average change versus the balanced 3000 setup is +0.0021.

## 2. Technical status

- Feature-consistency training completed after fixing the real dataloader path.
- The trained checkpoint was saved and evaluated.
- Three-sequence evaluation completed for Car1, David2, and Coke.
- CSV logging works through `experiments/baseline_results.csv`.
- This remains local proof-of-concept evidence, not final paper evidence.

## 3. Result summary by sequence

### Car1

Feature consistency should be interpreted by comparing condition-level AUC changes in the final table. Car1 is useful because the original OSTrack baseline is sensitive to synthetic degradations, especially motion blur, low resolution, and Gaussian noise.

### David2

David2 is a stronger/easier sequence than Car1 in several degraded conditions. It is useful for checking whether RG-SSB gains generalize or overfit to Car1.

### Coke

Coke provides a third validation sequence and helps identify whether a training strategy is sequence-specific or more stable.

## 4. Average result summary

| condition | baseline | fully degraded 3000 | balanced 3000 | featcons 3000 | featcons-baseline | featcons-full3000 | featcons-balanced |
| --- | --- | --- | --- | --- | --- | --- | --- |
| clean | 0.7096 | 0.7274 | 0.7242 | 0.7086 | -0.0010 | -0.0188 | -0.0156 |
| motion_blur_medium | 0.4691 | 0.4949 | 0.4744 | 0.4852 | 0.0161 | -0.0096 | 0.0108 |
| low_resolution_medium | 0.5890 | 0.5939 | 0.5865 | 0.5852 | -0.0038 | -0.0087 | -0.0014 |
| gaussian_noise_medium | 0.5905 | 0.5855 | 0.5845 | 0.5991 | 0.0086 | 0.0136 | 0.0146 |

Best average model by condition:

| condition | best average model | best average AUC |
| --- | --- | --- |
| clean | fully_degraded_3000 | 0.7274 |
| motion_blur_medium | fully_degraded_3000 | 0.4949 |
| low_resolution_medium | fully_degraded_3000 | 0.5939 |
| gaussian_noise_medium | featcons_3000 | 0.5991 |

## 5. Main finding

Feature consistency should be described cautiously. It may improve some degradation cases, but the result must be judged against both the original baseline and the previous 3000-sample training variants.

The current evidence does not justify final robustness claims. It is best used to decide the next local training step.

## 6. Likely reasons for results

Likely reasons include:

- Feature consistency encourages clean/degraded feature alignment.
- The selected lambda may be too small or too large.
- The clean feature target is detached, which stabilizes training but may limit adaptation.
- The backbone remains frozen.
- The feature loss is applied only after RG-SSB.
- There is no response consistency loss yet.
- There is no target-region weighting.
- Degradation is still search-only.
- The 3000-sample local training is still small.

## 7. Recommended next experiment

Decision based on parsed results: **feature consistency is useful but not clearly better than the fully degraded 3000 setup; tune lambda or add response consistency next**.

The fastest high-quality next step is to avoid new architecture modules and run a small controlled loss/training sweep. Recommended options are:

1. Tune feature-consistency lambda, for example 0.02 and 0.10.
2. Add response consistency only if lambda tuning does not help.
3. Keep backbone frozen until the loss behavior is clearer.
4. Continue evaluating on Car1, David2, and Coke before moving to HPC.

## 8. What to postpone

Postpone:

- degradation token
- template-guided scan
- memory update
- response fusion
- final paper claims

## 9. Decision

Decision: **feature consistency is useful but not clearly better than the fully degraded 3000 setup; tune lambda or add response consistency next**.

## 10. Final table

| sequence | condition | baseline AUC | full3000 AUC | balanced3000 AUC | featcons3000 AUC | featcons-baseline | featcons-full3000 | best model |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Car1 | clean | 0.5760 | 0.6275 | 0.6154 | 0.5732 | -0.0028 | -0.0543 | fully_degraded_3000 |
| Car1 | motion_blur_medium | 0.1572 | 0.1872 | 0.1608 | 0.1856 | 0.0283 | -0.0017 | fully_degraded_3000 |
| Car1 | low_resolution_medium | 0.2149 | 0.2301 | 0.2022 | 0.2057 | -0.0092 | -0.0244 | fully_degraded_3000 |
| Car1 | gaussian_noise_medium | 0.2073 | 0.2200 | 0.2108 | 0.2560 | 0.0487 | 0.0360 | featcons_3000 |
| David2 | clean | 0.7944 | 0.7955 | 0.7988 | 0.7834 | -0.0110 | -0.0120 | balanced_3000 |
| David2 | motion_blur_medium | 0.5497 | 0.5789 | 0.5514 | 0.5417 | -0.0080 | -0.0373 | fully_degraded_3000 |
| David2 | low_resolution_medium | 0.8063 | 0.8022 | 0.8098 | 0.7904 | -0.0159 | -0.0118 | balanced_3000 |
| David2 | gaussian_noise_medium | 0.8175 | 0.7844 | 0.7889 | 0.7733 | -0.0443 | -0.0111 | baseline |
| Coke | clean | 0.7583 | 0.7591 | 0.7583 | 0.7691 | 0.0109 | 0.0100 | featcons_3000 |
| Coke | motion_blur_medium | 0.7004 | 0.7185 | 0.7112 | 0.7285 | 0.0281 | 0.0100 | featcons_3000 |
| Coke | low_resolution_medium | 0.7459 | 0.7493 | 0.7476 | 0.7594 | 0.0135 | 0.0101 | featcons_3000 |
| Coke | gaussian_noise_medium | 0.7468 | 0.7519 | 0.7540 | 0.7680 | 0.0212 | 0.0161 | featcons_3000 |

## 11. Average table

| condition | avg baseline | avg full3000 | avg balanced3000 | avg featcons3000 | featcons-baseline | featcons-full3000 | featcons-balanced |
| --- | --- | --- | --- | --- | --- | --- | --- |
| clean | 0.7096 | 0.7274 | 0.7242 | 0.7086 | -0.0010 | -0.0188 | -0.0156 |
| motion_blur_medium | 0.4691 | 0.4949 | 0.4744 | 0.4852 | 0.0161 | -0.0096 | 0.0108 |
| low_resolution_medium | 0.5890 | 0.5939 | 0.5865 | 0.5852 | -0.0038 | -0.0087 | -0.0014 |
| gaussian_noise_medium | 0.5905 | 0.5855 | 0.5845 | 0.5991 | 0.0086 | 0.0136 | 0.0146 |

## Verification

- Parsed `experiments/baseline_results.csv`.
- Created `experiments/rgssb_head_featcons_3000_comparison.csv`.
- No OSTrack training was run.
- No OSTrack evaluation was run.
- No external/OSTrack files were modified.
