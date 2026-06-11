# RG-SSB + Head 3000-Sample Result Analysis

Date: 2026-06-10

Inputs:

- `experiments/baseline_results.csv`
- `experiments/rgssb_head_three_sequence_comparison.csv`
- `implementation/rgssb_head_three_sequence_result_analysis.md`
- `implementation/rgssb_head_degraded_3000_training_plan.md`

## 1. Executive Summary

The 3000-sample RG-SSB + head model produced mixed average results and did not clearly improve the proof-of-concept beyond the 1000-sample model. It is still useful local evidence that RG-SSB + head can improve several degraded cases, but it is not a final robustness result.

## 2. Technical Status

- 3000-sample training completed.
- A checkpoint was saved and evaluated.
- Three-sequence evaluation completed for Car1, David2, and Coke.
- CSV logging works through `experiments/baseline_results.csv`.
- The pipeline is ready for the next decision.

## 3. Result Summary By Sequence

### Car1

3000-sample RG-SSB + head improves over baseline on: clean (+0.051505 AUC), motion_blur medium (+0.030023 AUC), low_resolution medium (+0.015268 AUC), gaussian_noise medium (+0.012775 AUC).
It improves over the 1000-sample model on: motion_blur medium (+0.023597 AUC), low_resolution medium (+0.000902 AUC).
It trails the 1000-sample model on: clean (-0.122228 AUC), gaussian_noise medium (-0.025267 AUC).
Average 3000 vs baseline AUC change on Car1: `+0.027393`; average 3000 vs 1000 change: `-0.030749`. This supports the method relative to baseline.

- clean: baseline `0.575995`, 1000 `0.749728`, 3000 `0.627500`; 3000 vs baseline `+0.051505`, 3000 vs 1000 `-0.122228`; best model `rgssb_head_1000`.
- motion_blur medium: baseline `0.157212`, 1000 `0.163638`, 3000 `0.187235`; 3000 vs baseline `+0.030023`, 3000 vs 1000 `+0.023597`; best model `rgssb_head_3000`.
- low_resolution medium: baseline `0.214881`, 1000 `0.229247`, 3000 `0.230149`; 3000 vs baseline `+0.015268`, 3000 vs 1000 `+0.000902`; best model `rgssb_head_3000`.
- gaussian_noise medium: baseline `0.207270`, 1000 `0.245312`, 3000 `0.220045`; 3000 vs baseline `+0.012775`, 3000 vs 1000 `-0.025267`; best model `rgssb_head_1000`.

### David2

3000-sample RG-SSB + head improves over baseline on: clean (+0.001051 AUC), motion_blur medium (+0.029261 AUC).
3000-sample RG-SSB + head drops below baseline on: low_resolution medium (-0.004075 AUC), gaussian_noise medium (-0.033114 AUC).
It improves over the 1000-sample model on: clean (+0.020834 AUC), motion_blur medium (+0.002379 AUC), low_resolution medium (+0.019267 AUC), gaussian_noise medium (+0.013607 AUC).
Average 3000 vs baseline AUC change on David2: `-0.001719`; average 3000 vs 1000 change: `+0.014022`. This does not clearly support the method relative to baseline.

- clean: baseline `0.794439`, 1000 `0.774656`, 3000 `0.795490`; 3000 vs baseline `+0.001051`, 3000 vs 1000 `+0.020834`; best model `rgssb_head_3000`.
- motion_blur medium: baseline `0.549680`, 1000 `0.576562`, 3000 `0.578941`; 3000 vs baseline `+0.029261`, 3000 vs 1000 `+0.002379`; best model `rgssb_head_3000`.
- low_resolution medium: baseline `0.806258`, 1000 `0.782916`, 3000 `0.802183`; 3000 vs baseline `-0.004075`, 3000 vs 1000 `+0.019267`; best model `baseline`.
- gaussian_noise medium: baseline `0.817542`, 1000 `0.770821`, 3000 `0.784428`; 3000 vs baseline `-0.033114`, 3000 vs 1000 `+0.013607`; best model `baseline`.

### Coke

3000-sample RG-SSB + head improves over baseline on: clean (+0.000885 AUC), motion_blur medium (+0.018101 AUC), low_resolution medium (+0.003436 AUC), gaussian_noise medium (+0.005172 AUC).
It trails the 1000-sample model on: clean (-0.009935 AUC), motion_blur medium (-0.011602 AUC), low_resolution medium (-0.011738 AUC), gaussian_noise medium (-0.019257 AUC).
Average 3000 vs baseline AUC change on Coke: `+0.006899`; average 3000 vs 1000 change: `-0.013133`. This supports the method relative to baseline.

- clean: baseline `0.758259`, 1000 `0.769079`, 3000 `0.759144`; 3000 vs baseline `+0.000885`, 3000 vs 1000 `-0.009935`; best model `rgssb_head_1000`.
- motion_blur medium: baseline `0.700384`, 1000 `0.730087`, 3000 `0.718485`; 3000 vs baseline `+0.018101`, 3000 vs 1000 `-0.011602`; best model `rgssb_head_1000`.
- low_resolution medium: baseline `0.745875`, 1000 `0.761049`, 3000 `0.749311`; 3000 vs baseline `+0.003436`, 3000 vs 1000 `-0.011738`; best model `rgssb_head_1000`.
- gaussian_noise medium: baseline `0.746759`, 1000 `0.771188`, 3000 `0.751931`; 3000 vs baseline `+0.005172`, 3000 vs 1000 `-0.019257`; best model `rgssb_head_1000`.

## 4. Average Result Summary

- clean: baseline `0.709564`, 1000 `0.764488`, 3000 `0.727378`; 1000 vs baseline `+0.054923`, 3000 vs baseline `+0.017814`, 3000 vs 1000 `-0.037110`.
- motion_blur medium: baseline `0.469092`, 1000 `0.490096`, 3000 `0.494887`; 1000 vs baseline `+0.021004`, 3000 vs baseline `+0.025795`, 3000 vs 1000 `+0.004791`.
- low_resolution medium: baseline `0.589005`, 1000 `0.591071`, 3000 `0.593881`; 1000 vs baseline `+0.002066`, 3000 vs baseline `+0.004876`, 3000 vs 1000 `+0.002810`.
- gaussian_noise medium: baseline `0.590524`, 1000 `0.595774`, 3000 `0.585468`; 1000 vs baseline `+0.005250`, 3000 vs baseline `-0.005056`, 3000 vs 1000 `-0.010306`.

## 5. Main Finding

The 3000-sample RG-SSB + head result remains positive relative to the original OSTrack baseline on average for clean, motion blur, and low resolution, but Gaussian noise is slightly below baseline on average. Compared with the 1000-sample model, the 3000-sample model improves average AUC for motion blur and low resolution, but drops on clean and Gaussian noise. The strongest 3000-sample signal is motion blur, where all three sequences improve over baseline. Scaling to 3000 samples helps some degraded conditions, but does not by itself establish consistently better robustness than the 1000-sample run. This is local proof-of-concept evidence, not a final result.

## 6. Likely Reasons For Improvements Or Regressions

- More degradation-aware samples can help stabilize localization on some conditions, especially motion blur.
- RG-SSB + head training adapts localization better than RG-SSB-only training because the head sees RG-SSB-modified features during optimization.
- The backbone is still frozen, which limits adaptation to degraded appearance.
- There is no clean-degraded feature consistency loss.
- There is no response consistency loss.
- There is no degradation token.
- Degradation is applied to search images only.
- The local training size is still limited and may be sensitive to sampled LaSOT clips and one random seed.

## 7. Recommended Next Experiment

Options:

- A. Train RG-SSB + head for 5000 or more samples locally.
- B. Add clean/degraded feature consistency loss.
- C. Add response consistency loss.
- D. Add clean/degraded mixed training balance.
- E. Move this exact setup to HPC.
- F. Add degradation token or template-guided scan.

Recommended fastest high-quality step: **B/D. Add clean-degraded feature consistency or explicit clean/degraded mixed training balance before HPC scaling.**

Reason: 3000 samples improve motion blur and low resolution relative to the 1000-sample model, but clean and Gaussian noise regress. The next change should improve the training signal and clean/degraded balance rather than simply increasing sample count or moving the same setup to HPC.

## 8. What To Postpone

- degradation token
- template-guided scan
- memory update
- response fusion
- final paper claims

## 9. Decision

Decision: **revise training strategy**.

Continue with the current RG-SSB + head architecture, but add a cleaner training objective or clean/degraded balance before larger-scale training.

## 10. Final Table

| Sequence | Condition | Baseline AUC | 1000-sample AUC | 3000-sample AUC | 3000 vs baseline AUC change | 3000 vs 1000 AUC change | Best model | Note |
|---|---|---:|---:|---:|---:|---:|---|---|
| Car1 | clean | 0.575995 | 0.749728 | 0.627500 | +0.051505 | -0.122228 | rgssb_head_1000 | 3000 improves over baseline but trails 1000 |
| Car1 | motion_blur medium | 0.157212 | 0.163638 | 0.187235 | +0.030023 | +0.023597 | rgssb_head_3000 | 3000 improves over baseline and 1000 |
| Car1 | low_resolution medium | 0.214881 | 0.229247 | 0.230149 | +0.015268 | +0.000902 | rgssb_head_3000 | 3000 improves over baseline and 1000 |
| Car1 | gaussian_noise medium | 0.207270 | 0.245312 | 0.220045 | +0.012775 | -0.025267 | rgssb_head_1000 | 3000 improves over baseline but trails 1000 |
| David2 | clean | 0.794439 | 0.774656 | 0.795490 | +0.001051 | +0.020834 | rgssb_head_3000 | 3000 improves over baseline and 1000 |
| David2 | motion_blur medium | 0.549680 | 0.576562 | 0.578941 | +0.029261 | +0.002379 | rgssb_head_3000 | 3000 improves over baseline and 1000 |
| David2 | low_resolution medium | 0.806258 | 0.782916 | 0.802183 | -0.004075 | +0.019267 | baseline | 3000 recovers over 1000 but remains below baseline |
| David2 | gaussian_noise medium | 0.817542 | 0.770821 | 0.784428 | -0.033114 | +0.013607 | baseline | 3000 recovers over 1000 but remains below baseline |
| Coke | clean | 0.758259 | 0.769079 | 0.759144 | +0.000885 | -0.009935 | rgssb_head_1000 | 3000 improves over baseline but trails 1000 |
| Coke | motion_blur medium | 0.700384 | 0.730087 | 0.718485 | +0.018101 | -0.011602 | rgssb_head_1000 | 3000 improves over baseline but trails 1000 |
| Coke | low_resolution medium | 0.745875 | 0.761049 | 0.749311 | +0.003436 | -0.011738 | rgssb_head_1000 | 3000 improves over baseline but trails 1000 |
| Coke | gaussian_noise medium | 0.746759 | 0.771188 | 0.751931 | +0.005172 | -0.019257 | rgssb_head_1000 | 3000 improves over baseline but trails 1000 |

## 11. Average Table

| Condition | Average baseline AUC | Average 1000-sample AUC | Average 3000-sample AUC | Average 3000 vs baseline change | Average 3000 vs 1000 change | Decision note |
|---|---:|---:|---:|---:|---:|---|
| clean | 0.709564 | 0.764488 | 0.727378 | +0.017814 | -0.037110 | above baseline, below 1000 |
| motion_blur medium | 0.469092 | 0.490096 | 0.494887 | +0.025795 | +0.004791 | improves over 1000 |
| low_resolution medium | 0.589005 | 0.591071 | 0.593881 | +0.004876 | +0.002810 | improves over 1000 |
| gaussian_noise medium | 0.590524 | 0.595774 | 0.585468 | -0.005056 | -0.010306 | weak/mixed |

## Verification

Generated `experiments/rgssb_head_1000_vs_3000_three_sequence_comparison.csv` by parsing `experiments/baseline_results.csv` with Python. No OSTrack training, evaluation, dataset modification, or `external/OSTrack` modification was performed.

Uncertain fields:

- Each degradation condition uses one seed.
- The comparison covers only Car1, David2, and Coke.
- These are local proof-of-concept results, not final paper evidence.
