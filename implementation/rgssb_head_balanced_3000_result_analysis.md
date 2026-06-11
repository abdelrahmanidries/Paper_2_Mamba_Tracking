# RG-SSB + Head Balanced 3000-Sample Result Analysis

Date: 2026-06-10

Inputs:

- `experiments/baseline_results.csv`
- `experiments/rgssb_head_1000_vs_3000_three_sequence_comparison.csv`
- `implementation/rgssb_head_3000_result_analysis.md`
- `implementation/rgssb_head_balanced_3000_training_plan.md`

## 1. Executive Summary

Balanced 3000-sample training does not improve the overall three-sequence result compared with fully degraded 3000-sample training. It slightly improves some clean/general behavior on David2, but fully degraded 3000 is stronger on most average conditions. This is local proof-of-concept evidence, not final paper evidence.

## 2. Technical Status

- Balanced 3000 training completed.
- A checkpoint was saved.
- Three-sequence evaluation completed for Car1, David2, and Coke.
- CSV logging works through `experiments/baseline_results.csv`.
- This is local proof-of-concept evidence, not final paper evidence.

## 3. Result Summary By Sequence

### Car1

Balanced training improves over baseline on: clean (+0.039371 AUC), motion_blur medium (+0.003563 AUC), gaussian_noise medium (+0.003495 AUC).
Balanced training drops below baseline on: low_resolution medium (-0.012726 AUC).
Balanced training is worse than fully degraded 3000 on: clean (-0.012134 AUC), motion_blur medium (-0.026460 AUC), low_resolution medium (-0.027994 AUC), gaussian_noise medium (-0.009280 AUC).
Average balanced vs baseline AUC change on Car1: `+0.008426`; balanced vs fully degraded 3000: `-0.018967`. This supports balanced training relative to baseline.

- clean: baseline `0.575995`, 1000 `0.749728`, fully degraded 3000 `0.627500`, balanced 3000 `0.615366`; balanced vs baseline `+0.039371`, balanced vs fully degraded 3000 `-0.012134`; best model `rgssb_head_1000`.
- motion_blur medium: baseline `0.157212`, 1000 `0.163638`, fully degraded 3000 `0.187235`, balanced 3000 `0.160775`; balanced vs baseline `+0.003563`, balanced vs fully degraded 3000 `-0.026460`; best model `rgssb_head_3000_degraded`.
- low_resolution medium: baseline `0.214881`, 1000 `0.229247`, fully degraded 3000 `0.230149`, balanced 3000 `0.202155`; balanced vs baseline `-0.012726`, balanced vs fully degraded 3000 `-0.027994`; best model `rgssb_head_3000_degraded`.
- gaussian_noise medium: baseline `0.207270`, 1000 `0.245312`, fully degraded 3000 `0.220045`, balanced 3000 `0.210765`; balanced vs baseline `+0.003495`, balanced vs fully degraded 3000 `-0.009280`; best model `rgssb_head_1000`.

### David2

Balanced training improves over baseline on: clean (+0.004370 AUC), motion_blur medium (+0.001678 AUC), low_resolution medium (+0.003558 AUC).
Balanced training drops below baseline on: gaussian_noise medium (-0.028652 AUC).
Balanced training improves over fully degraded 3000 on: clean (+0.003319 AUC), low_resolution medium (+0.007633 AUC), gaussian_noise medium (+0.004462 AUC).
Balanced training is worse than fully degraded 3000 on: motion_blur medium (-0.027583 AUC).
Average balanced vs baseline AUC change on David2: `-0.004762`; balanced vs fully degraded 3000: `-0.003042`. This does not clearly support balanced training relative to baseline.

- clean: baseline `0.794439`, 1000 `0.774656`, fully degraded 3000 `0.795490`, balanced 3000 `0.798809`; balanced vs baseline `+0.004370`, balanced vs fully degraded 3000 `+0.003319`; best model `rgssb_head_3000_balanced`.
- motion_blur medium: baseline `0.549680`, 1000 `0.576562`, fully degraded 3000 `0.578941`, balanced 3000 `0.551358`; balanced vs baseline `+0.001678`, balanced vs fully degraded 3000 `-0.027583`; best model `rgssb_head_3000_degraded`.
- low_resolution medium: baseline `0.806258`, 1000 `0.782916`, fully degraded 3000 `0.802183`, balanced 3000 `0.809816`; balanced vs baseline `+0.003558`, balanced vs fully degraded 3000 `+0.007633`; best model `rgssb_head_3000_balanced`.
- gaussian_noise medium: baseline `0.817542`, 1000 `0.770821`, fully degraded 3000 `0.784428`, balanced 3000 `0.788890`; balanced vs baseline `-0.028652`, balanced vs fully degraded 3000 `+0.004462`; best model `baseline`.

### Coke

Balanced training improves over baseline on: clean (+0.000034 AUC), motion_blur medium (+0.010820 AUC), low_resolution medium (+0.001769 AUC), gaussian_noise medium (+0.007213 AUC).
Balanced training improves over fully degraded 3000 on: gaussian_noise medium (+0.002041 AUC).
Balanced training is worse than fully degraded 3000 on: clean (-0.000851 AUC), motion_blur medium (-0.007281 AUC), low_resolution medium (-0.001667 AUC).
Average balanced vs baseline AUC change on Coke: `+0.004959`; balanced vs fully degraded 3000: `-0.001940`. This supports balanced training relative to baseline.

- clean: baseline `0.758259`, 1000 `0.769079`, fully degraded 3000 `0.759144`, balanced 3000 `0.758293`; balanced vs baseline `+0.000034`, balanced vs fully degraded 3000 `-0.000851`; best model `rgssb_head_1000`.
- motion_blur medium: baseline `0.700384`, 1000 `0.730087`, fully degraded 3000 `0.718485`, balanced 3000 `0.711204`; balanced vs baseline `+0.010820`, balanced vs fully degraded 3000 `-0.007281`; best model `rgssb_head_1000`.
- low_resolution medium: baseline `0.745875`, 1000 `0.761049`, fully degraded 3000 `0.749311`, balanced 3000 `0.747644`; balanced vs baseline `+0.001769`, balanced vs fully degraded 3000 `-0.001667`; best model `rgssb_head_1000`.
- gaussian_noise medium: baseline `0.746759`, 1000 `0.771188`, fully degraded 3000 `0.751931`, balanced 3000 `0.753972`; balanced vs baseline `+0.007213`, balanced vs fully degraded 3000 `+0.002041`; best model `rgssb_head_1000`.

## 4. Average Result Summary

- clean: baseline `0.709564`, 1000 `0.764488`, fully degraded 3000 `0.727378`, balanced 3000 `0.724156`; balanced vs baseline `+0.014592`, balanced vs 1000 `-0.040332`, balanced vs fully degraded 3000 `-0.003222`.
- motion_blur medium: baseline `0.469092`, 1000 `0.490096`, fully degraded 3000 `0.494887`, balanced 3000 `0.474446`; balanced vs baseline `+0.005354`, balanced vs 1000 `-0.015650`, balanced vs fully degraded 3000 `-0.020441`.
- low_resolution medium: baseline `0.589005`, 1000 `0.591071`, fully degraded 3000 `0.593881`, balanced 3000 `0.586538`; balanced vs baseline `-0.002466`, balanced vs 1000 `-0.004532`, balanced vs fully degraded 3000 `-0.007343`.
- gaussian_noise medium: baseline `0.590524`, 1000 `0.595774`, fully degraded 3000 `0.585468`, balanced 3000 `0.584542`; balanced vs baseline `-0.005981`, balanced vs 1000 `-0.011231`, balanced vs fully degraded 3000 `-0.000926`.

## 5. Main Finding

Balanced training may protect some clean/general behavior in isolated cases, especially David2 clean and low resolution, but it does not outperform fully degraded 3000-sample training on average. Fully degraded 3000 is stronger for motion blur and low resolution averages, while the earlier 1000-sample model remains strongest for several clean and Gaussian-noise cases. The results are mixed, so this should not be overclaimed as robust degradation handling.

## 6. Likely Reasons For Results

- Balanced training reduces degradation exposure compared with probability `1.0`.
- Fully degraded training may specialize more strongly to degraded inputs.
- Search-only degradation may be insufficient for stable template-search robustness.
- The backbone is frozen, limiting adaptation to degraded appearance.
- There is no feature consistency loss.
- There is no response consistency loss.
- There is no explicit target-aware restoration supervision.

## 7. Recommended Next Experiment

Options:

- A. Continue with fully degraded 3000 setup.
- B. Continue with balanced 3000 setup.
- C. Add clean-degraded feature consistency loss.
- D. Add response consistency loss.
- E. Move to HPC with current best setup.
- F. Add a fourth OTB sequence.
- G. Add degradation token or template-guided scan.

Recommended fastest high-quality step: **C/D. Add clean-degraded feature or response consistency to the fully degraded 3000 setup.**

Reason: the balanced 3000 setup did not beat fully degraded 3000 on average, and neither 3000 variant clearly dominates the 1000-sample model. The next useful change is a stronger training signal that explicitly ties clean and degraded behavior, rather than only changing degradation probability.

## 8. What To Postpone

- degradation token
- template-guided scan
- memory update
- response fusion
- final paper claims

## 9. Decision

Decision: **add feature/response consistency**.

Continue with the current RG-SSB + head architecture, but revise the training objective before HPC scaling or additional modules.

## 10. Final Table

| Sequence | Condition | Baseline AUC | 1000 AUC | Fully degraded 3000 AUC | Balanced 3000 AUC | Balanced vs baseline AUC change | Balanced vs fully degraded 3000 AUC change | Best model | Note |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| Car1 | clean | 0.575995 | 0.749728 | 0.627500 | 0.615366 | +0.039371 | -0.012134 | rgssb_head_1000 | balanced improves over baseline but trails fully degraded 3000 |
| Car1 | motion_blur medium | 0.157212 | 0.163638 | 0.187235 | 0.160775 | +0.003563 | -0.026460 | rgssb_head_3000_degraded | balanced improves over baseline but trails fully degraded 3000 |
| Car1 | low_resolution medium | 0.214881 | 0.229247 | 0.230149 | 0.202155 | -0.012726 | -0.027994 | rgssb_head_3000_degraded | balanced below baseline |
| Car1 | gaussian_noise medium | 0.207270 | 0.245312 | 0.220045 | 0.210765 | +0.003495 | -0.009280 | rgssb_head_1000 | balanced improves over baseline but trails fully degraded 3000 |
| David2 | clean | 0.794439 | 0.774656 | 0.795490 | 0.798809 | +0.004370 | +0.003319 | rgssb_head_3000_balanced | balanced improves over baseline and fully degraded 3000 |
| David2 | motion_blur medium | 0.549680 | 0.576562 | 0.578941 | 0.551358 | +0.001678 | -0.027583 | rgssb_head_3000_degraded | balanced improves over baseline but trails fully degraded 3000 |
| David2 | low_resolution medium | 0.806258 | 0.782916 | 0.802183 | 0.809816 | +0.003558 | +0.007633 | rgssb_head_3000_balanced | balanced improves over baseline and fully degraded 3000 |
| David2 | gaussian_noise medium | 0.817542 | 0.770821 | 0.784428 | 0.788890 | -0.028652 | +0.004462 | baseline | balanced beats fully degraded 3000 but remains below baseline |
| Coke | clean | 0.758259 | 0.769079 | 0.759144 | 0.758293 | +0.000034 | -0.000851 | rgssb_head_1000 | balanced improves over baseline but trails fully degraded 3000 |
| Coke | motion_blur medium | 0.700384 | 0.730087 | 0.718485 | 0.711204 | +0.010820 | -0.007281 | rgssb_head_1000 | balanced improves over baseline but trails fully degraded 3000 |
| Coke | low_resolution medium | 0.745875 | 0.761049 | 0.749311 | 0.747644 | +0.001769 | -0.001667 | rgssb_head_1000 | balanced improves over baseline but trails fully degraded 3000 |
| Coke | gaussian_noise medium | 0.746759 | 0.771188 | 0.751931 | 0.753972 | +0.007213 | +0.002041 | rgssb_head_1000 | balanced improves over baseline and fully degraded 3000 |

## 11. Average Table

| Condition | Average baseline AUC | Average 1000 AUC | Average fully degraded 3000 AUC | Average balanced 3000 AUC | Balanced vs baseline change | Balanced vs fully degraded 3000 change | Decision note |
|---|---:|---:|---:|---:|---:|---:|---|
| clean | 0.709564 | 0.764488 | 0.727378 | 0.724156 | +0.014592 | -0.003222 | above baseline, below fully degraded 3000 |
| motion_blur medium | 0.469092 | 0.490096 | 0.494887 | 0.474446 | +0.005354 | -0.020441 | above baseline, below fully degraded 3000 |
| low_resolution medium | 0.589005 | 0.591071 | 0.593881 | 0.586538 | -0.002466 | -0.007343 | weak/mixed |
| gaussian_noise medium | 0.590524 | 0.595774 | 0.585468 | 0.584542 | -0.005981 | -0.000926 | weak/mixed |

## Verification

Generated `experiments/rgssb_head_balanced_vs_degraded_3000_comparison.csv` by parsing `experiments/baseline_results.csv` with Python. No OSTrack training, evaluation, dataset modification, or `external/OSTrack` modification was performed.

Uncertain fields:

- Each degradation condition uses one seed.
- The comparison covers only Car1, David2, and Coke.
- These are local proof-of-concept results, not final paper evidence.
