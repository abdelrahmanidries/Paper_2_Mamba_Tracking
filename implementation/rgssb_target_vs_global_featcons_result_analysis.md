# RG-SSB Target-Region vs Global Feature Consistency Result Analysis

Inputs:

- `experiments/baseline_results.csv`
- `implementation/rgssb_target_feature_consistency_setup_notes.md`
- `implementation/rgssb_target_region_feature_consistency_plan.md`
- `implementation/rgssb_featcons_lambda_sweep_result_analysis.md`

## 1. Executive summary

Target-region feature consistency does not improve over global feature consistency lambda `0.02` on this 12-pair local comparison. Overall baseline AUC is `0.589546`, global feature consistency AUC is `0.613026`, target-region feature consistency AUC is `0.589471`, and target vs global AUC change is `-0.023555`.
Average Precision@20 change target vs global is `-0.031605`; average center-error change target vs global is `+5.063618`. Lower center error is better.

## 2. Technical status

- Target-region training completed locally.
- Target-region evaluation completed locally on Car1, David2, and Coke.
- CSV logging works through `experiments/baseline_results.csv`.
- This is a local 3000-sample debug comparison, not paper-scale evidence.
- Global feature consistency lambda `0.02` remains the stronger reference unless target-region results improve in broader follow-up.

## 3. Result summary

- `Car1`: baseline AUC `0.288840`, global AUC `0.361845`, target AUC `0.300987`, target vs global `-0.060858`; target drops versus global on average.
- `David2`: baseline AUC `0.741980`, global AUC `0.721602`, target AUC `0.721168`, target vs global `-0.000434`; target drops versus global on average.
- `Coke`: baseline AUC `0.737819`, global AUC `0.755631`, target AUC `0.746257`, target vs global `-0.009374`; target drops versus global on average.

## 4. Condition-level result

- `clean`: baseline AUC `0.709564`, global AUC `0.713036`, target AUC `0.710805`, target vs global `-0.002231`; target drops on average.
- `motion_blur_medium`: baseline AUC `0.469092`, global AUC `0.477794`, target AUC `0.478781`, target vs global `+0.000987`; target improves on average.
- `low_resolution_medium`: baseline AUC `0.589005`, global AUC `0.594930`, target AUC `0.585323`, target vs global `-0.009607`; target drops on average.
- `gaussian_noise_medium`: baseline AUC `0.590524`, global AUC `0.666344`, target AUC `0.582974`, target vs global `-0.083370`; target drops on average.

## 5. Main finding

Target-region feature consistency does not improve over global feature consistency lambda `0.02` on this 12-pair local comparison. This should be interpreted carefully because the result covers only three OTB sequences and four conditions. The target mask did not automatically solve the cross-benchmark failure pattern; the decision should be based on parsed AUC, Precision@20, and center-error changes rather than the hypothesis alone.

## 6. Likely reasons

- The target mask may be too narrow or slightly misaligned after mapping normalized search boxes to a `16 x 16` token grid.
- Global context may still be useful, especially when background structure helps disambiguate the target under degradation.
- The current mask uses a coarse `16 x 16` token grid, so small targets can be quantized into very few high-weight tokens.
- The background weight `0.05` may be too low if surrounding context matters, or too high if clutter still dominates.
- Local 3000-sample training is small and can produce sequence-specific behavior.
- The backbone remains frozen, so adaptation capacity is limited to RG-SSB and box head.

## 7. Recommended next experiment

Options:
- A. Drop target-region consistency and keep global lambda `0.02`.
- B. Tune target mask/background weight.
- C. Use global + target consistency together.
- D. Move current best global lambda `0.02` setup to broader evaluation/paper planning.
- E. Add new architecture modules.

Recommended next step: **Keep global feature consistency lambda `0.02` as the current best setup; only tune target-region consistency if failure analysis justifies another local ablation.** This recommendation is based only on the parsed results. Adding new architecture modules is not justified by this comparison.

## 8. Decision

Decision: **keep global feature consistency**.

## Detailed Tables

### Per-sequence average table

| sequence | average baseline AUC | average global AUC | average target AUC | target vs global AUC change | target Precision@20 change vs global | target center-error change vs global |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Car1 | 0.288840 | 0.361845 | 0.300987 | -0.060858 | -0.083823 | +11.618302 |
| David2 | 0.741980 | 0.721602 | 0.721168 | -0.000434 | -0.003259 | -0.018672 |
| Coke | 0.737819 | 0.755631 | 0.746257 | -0.009374 | -0.007732 | +3.591226 |

### Per-condition average table

| condition | average baseline AUC | average global AUC | average target AUC | target vs global AUC change | target Precision@20 change vs global | target center-error change vs global |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| clean | 0.709564 | 0.713036 | 0.710805 | -0.002231 | -0.005882 | +0.251554 |
| motion_blur_medium | 0.469092 | 0.477794 | 0.478781 | +0.000987 | -0.005356 | -0.146187 |
| low_resolution_medium | 0.589005 | 0.594930 | 0.585323 | -0.009607 | -0.012910 | +5.453014 |
| gaussian_noise_medium | 0.590524 | 0.666344 | 0.582974 | -0.083370 | -0.102271 | +14.696094 |

### Top gains from target over global

| sequence | condition | target vs global AUC change | note |
| --- | --- | ---: | --- |
| David2 | motion_blur_medium | +0.005070 | near tie between target and global |
| Coke | clean | +0.003606 | near tie between target and global |
| Coke | motion_blur_medium | -0.000341 | near tie between target and global |
| David2 | gaussian_noise_medium | -0.000553 | near tie between target and global |
| Car1 | motion_blur_medium | -0.001767 | near tie between target and global |

### Largest drops from target versus global

| sequence | condition | target vs global AUC change | note |
| --- | --- | ---: | --- |
| Car1 | gaussian_noise_medium | -0.211755 | target-region drops versus global |
| Coke | gaussian_noise_medium | -0.037801 | target-region drops versus global |
| Car1 | low_resolution_medium | -0.023132 | target-region drops versus global |
| Car1 | clean | -0.006776 | near tie between target and global |
| David2 | clean | -0.003522 | near tie between target and global |

### Final detailed table

| sequence | condition | baseline AUC | global AUC | target AUC | global vs baseline | target vs baseline | target vs global | best model | note |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |
| Car1 | clean | 0.575995 | 0.583557 | 0.576781 | +0.007562 | +0.000786 | -0.006776 | global_featcons | near tie between target and global |
| Car1 | motion_blur_medium | 0.157212 | 0.167084 | 0.165317 | +0.009872 | +0.008105 | -0.001767 | global_featcons | near tie between target and global |
| Car1 | low_resolution_medium | 0.214881 | 0.231528 | 0.208396 | +0.016647 | -0.006485 | -0.023132 | global_featcons | target-region drops versus global |
| Car1 | gaussian_noise_medium | 0.207270 | 0.465211 | 0.253456 | +0.257941 | +0.046186 | -0.211755 | global_featcons | target-region drops versus global |
| David2 | clean | 0.794439 | 0.786880 | 0.783358 | -0.007559 | -0.011081 | -0.003522 | baseline | near tie between target and global |
| David2 | motion_blur_medium | 0.549680 | 0.538931 | 0.544001 | -0.010749 | -0.005679 | +0.005070 | baseline | near tie between target and global |
| David2 | low_resolution_medium | 0.806258 | 0.792485 | 0.789756 | -0.013773 | -0.016502 | -0.002729 | baseline | near tie between target and global |
| David2 | gaussian_noise_medium | 0.817542 | 0.768110 | 0.767557 | -0.049432 | -0.049985 | -0.000553 | baseline | near tie between target and global |
| Coke | clean | 0.758259 | 0.768671 | 0.772277 | +0.010412 | +0.014018 | +0.003606 | target_featcons | near tie between target and global |
| Coke | motion_blur_medium | 0.700384 | 0.727366 | 0.727025 | +0.026982 | +0.026641 | -0.000341 | global_featcons | near tie between target and global |
| Coke | low_resolution_medium | 0.745875 | 0.760777 | 0.757817 | +0.014902 | +0.011942 | -0.002960 | global_featcons | near tie between target and global |
| Coke | gaussian_noise_medium | 0.746759 | 0.765711 | 0.727910 | +0.018952 | -0.018849 | -0.037801 | global_featcons | target-region drops versus global |

## Verification

- Parsed `experiments/baseline_results.csv` with Python.
- Created `experiments/rgssb_target_vs_global_featcons_comparison.csv`.
- Created `implementation/rgssb_target_vs_global_featcons_result_analysis.md`.
- Compared 12 sequence-condition pairs with baseline, global lambda `0.02`, and target-region lambda `0.02` rows.
- Did not run OSTrack, training, or evaluation.
- Did not modify datasets or `external/OSTrack`.

Uncertain fields:

- This comparison uses only Car1, David2, and Coke.
- Each degraded condition uses one seed, `42`, and medium severity.
- The result is local debug evidence, not paper-scale evidence.
