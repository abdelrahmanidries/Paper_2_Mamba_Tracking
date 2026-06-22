# Target-versus-Distractor Margin Ablation Result Analysis

## 1. Executive Summary

The target-versus-distractor margin (TDM) ablation is rejected.

Compared with the current local global feature-consistency lambda `0.02` setup, TDM has an overall average AUC difference of `-0.014549` across the 12 Car1/David2/Coke sequence-condition pairs. Although it improves several individual conditions, the Car1 Gaussian-noise regression dominates the aggregate.

Final gate decision:

```text
REJECT_AND_ROLL_BACK_TO_PAPER_FREEZE_V1
```

The current best method remains global clean/degraded feature consistency with lambda `0.02`, response consistency disabled, and target-region consistency disabled.

## 2. Compared Configs

Baseline for this gate:

```text
vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_degraded_3000_featcons_lam002_debug
```

TDM ablation:

```text
vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_degraded_3000_featcons_lam002_tdm_debug
```

All values are parsed from `experiments/baseline_results.csv`. No training or evaluation was run for this report.

## 3. Gate Results

| gate | result | evidence |
| --- | --- | --- |
| all 12 local pairs present | PASS | `experiments/baseline_results.csv` contains all paired rows |
| local average improves over global lambda 0.02 | FAIL | overall difference `-0.014549` |
| no severe clean collapse | PASS | average clean difference `+0.010425` |
| final local decision | REJECT | local average fails |

The ablation therefore does not qualify for HPC promotion.

## 4. Condition Summary

| condition | TDM minus global lambda 0.02 AUC |
| --- | ---: |
| clean | +0.010425 |
| motion_blur medium | +0.009550 |
| low_resolution medium | +0.001167 |
| gaussian_noise medium | -0.079338 |

The positive effects on clean, motion blur, and low resolution are not sufficient to offset the Gaussian-noise regression.

## 5. Main Positive Effect

TDM improves several local condition averages:

- clean: `+0.010425`
- motion_blur medium: `+0.009550`
- low_resolution medium: `+0.001167`

The strongest individual gain is Car1 clean, where AUC improves from `0.583557` to `0.646573`, a change of `+0.063016`.

## 6. Main Regression

The dominant failure is Car1 Gaussian noise:

- global feature consistency lambda `0.02` AUC: `0.465211`
- TDM AUC: `0.222646`
- AUC change: `-0.242565`

This single regression is large enough to dominate the aggregate result. The average Gaussian-noise difference is `-0.079338`.

The largest clean drop is Coke clean:

- global AUC: `0.768671`
- TDM AUC: `0.741724`
- AUC change: `-0.026947`

Clean average remains positive overall, but the individual clean drop is still a warning sign.

## 7. Detailed Table

| sequence | condition | global AUC | TDM AUC | TDM - global | decision note |
| --- | --- | ---: | ---: | ---: | --- |
| Car1 | clean | 0.583557 | 0.646573 | +0.063016 | TDM improves |
| Car1 | motion_blur medium | 0.167084 | 0.187711 | +0.020627 | TDM improves |
| Car1 | low_resolution medium | 0.231528 | 0.233440 | +0.001912 | near neutral |
| Car1 | gaussian_noise medium | 0.465211 | 0.222646 | -0.242565 | dominant regression |
| David2 | clean | 0.786880 | 0.782086 | -0.004794 | near neutral |
| David2 | motion_blur medium | 0.538931 | 0.545458 | +0.006527 | small gain |
| David2 | low_resolution medium | 0.792485 | 0.789922 | -0.002563 | near neutral |
| David2 | gaussian_noise medium | 0.768110 | 0.768442 | +0.000332 | near neutral |
| Coke | clean | 0.768671 | 0.741724 | -0.026947 | largest clean drop |
| Coke | motion_blur medium | 0.727366 | 0.728863 | +0.001497 | near neutral |
| Coke | low_resolution medium | 0.760777 | 0.764928 | +0.004151 | small gain |
| Coke | gaussian_noise medium | 0.765711 | 0.769930 | +0.004219 | small gain |

Full machine-readable table:

```text
experiments/rgssb_tdm_gate_comparison.csv
```

## 8. Interpretation

The TDM loss does what it was designed to do mechanically: it encourages target response to exceed distractor response, and verification showed a positive real-batch margin violation with gradients reaching `box_head.*`. However, the local result indicates that this additional pressure can destabilize Gaussian-noise behavior, especially on Car1.

Because the local gate is explicitly designed to prevent expensive HPC promotion of unstable ablations, this result is a clean rejection rather than an inconclusive result.

## 9. Decision

Reject TDM and roll back to Paper Freeze V1.

Current frozen method:

- OSTrack + RG-SSB + box_head
- frozen backbone
- global clean/degraded feature consistency
- feature-consistency weight `0.02`
- response consistency disabled
- target-region consistency disabled
- TDM disabled

No further architecture or loss experiments are planned for this paper version.

## 10. Next Step

Move to paper completion:

- finalize paper tables,
- prepare corrected NFS provenance paragraph,
- prepare limitations and failure-mode discussion,
- avoid adding new method changes unless required by reviewer feedback.
