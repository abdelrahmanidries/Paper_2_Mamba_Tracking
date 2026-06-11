# RG-SSB + Head Three-Sequence Result Analysis

Date: 2026-06-10

Inputs:

- `experiments/baseline_results.csv`
- `experiments/rgssb_head_car1_david2_comparison.csv`
- `implementation/rgssb_head_car1_david2_result_analysis.md`
- `implementation/rgssb_head_training_plan.md`

## 1. Executive Summary

Across Car1, David2, and Coke, RG-SSB + head is promising but not uniformly better than the original OSTrack baseline. The three-sequence average AUC improves for clean, motion blur, low resolution, and Gaussian noise, though the low-resolution and Gaussian-noise gains are small. This supports continuing the current architecture with scaled or revised training, but it is still a local proof-of-concept rather than final paper evidence.

## 2. Technical Status

- RG-SSB + head training completed.
- Three-sequence evaluation completed for Car1, David2, and Coke.
- CSV logging works through `experiments/baseline_results.csv`.
- The pipeline is ready for the next decision.

## 3. Per-Sequence Result Summary

### Car1

RG-SSB + head improves: clean (+0.173733 AUC), motion_blur medium (+0.006426 AUC), low_resolution medium (+0.014366 AUC), gaussian_noise medium (+0.038042 AUC).
RG-SSB + head has no AUC drops on the analyzed conditions.
Average AUC change on Car1: `+0.058142`; this supports the method on this sequence.

- clean: AUC `0.575995` to `0.749728` (`+0.173733`), Precision@20 `0.746078` to `0.983333` (`+0.237255`), center error change `-13.974615` px.
- motion_blur medium: AUC `0.157212` to `0.163638` (`+0.006426`), Precision@20 `0.198039` to `0.212745` (`+0.014706`), center error change `-6.489876` px.
- low_resolution medium: AUC `0.214881` to `0.229247` (`+0.014366`), Precision@20 `0.267647` to `0.291176` (`+0.023529`), center error change `+3.479625` px.
- gaussian_noise medium: AUC `0.207270` to `0.245312` (`+0.038042`), Precision@20 `0.250980` to `0.322549` (`+0.071569`), center error change `-8.578029` px.

### David2

RG-SSB + head improves: motion_blur medium (+0.026882 AUC).
RG-SSB + head drops: clean (-0.019783 AUC), low_resolution medium (-0.023342 AUC), gaussian_noise medium (-0.046721 AUC).
Average AUC change on David2: `-0.015741`; this does not clearly support the method on this sequence.

- clean: AUC `0.794439` to `0.774656` (`-0.019783`), Precision@20 `1.000000` to `1.000000` (`+0.000000`), center error change `+0.057587` px.
- motion_blur medium: AUC `0.549680` to `0.576562` (`+0.026882`), Precision@20 `0.970205` to `0.972067` (`+0.001862`), center error change `-0.977709` px.
- low_resolution medium: AUC `0.806258` to `0.782916` (`-0.023342`), Precision@20 `1.000000` to `1.000000` (`+0.000000`), center error change `+0.047708` px.
- gaussian_noise medium: AUC `0.817542` to `0.770821` (`-0.046721`), Precision@20 `1.000000` to `0.981378` (`-0.018622`), center error change `+0.719061` px.

### Coke

RG-SSB + head improves: clean (+0.010820 AUC), motion_blur medium (+0.029703 AUC), low_resolution medium (+0.015174 AUC), gaussian_noise medium (+0.024429 AUC).
RG-SSB + head has no AUC drops on the analyzed conditions.
Average AUC change on Coke: `+0.020032`; this supports the method on this sequence.

- clean: AUC `0.758259` to `0.769079` (`+0.010820`), Precision@20 `0.958763` to `0.955326` (`-0.003437`), center error change `+0.915414` px.
- motion_blur medium: AUC `0.700384` to `0.730087` (`+0.029703`), Precision@20 `0.945017` to `0.927835` (`-0.017182`), center error change `+0.588151` px.
- low_resolution medium: AUC `0.745875` to `0.761049` (`+0.015174`), Precision@20 `0.945017` to `0.945017` (`+0.000000`), center error change `+0.549204` px.
- gaussian_noise medium: AUC `0.746759` to `0.771188` (`+0.024429`), Precision@20 `0.951890` to `0.945017` (`-0.006873`), center error change `-0.040342` px.

## 4. Average Result Summary

- clean: average AUC `0.709564` to `0.764488` (`+0.054923`), average Precision@20 change `+0.077939`, average center error change `-4.333871` px.
- motion_blur medium: average AUC `0.469092` to `0.490096` (`+0.021004`), average Precision@20 change `-0.000205`, average center error change `-2.293145` px.
- low_resolution medium: average AUC `0.589005` to `0.591071` (`+0.002066`), average Precision@20 change `+0.007843`, average center error change `+1.358846` px.
- gaussian_noise medium: average AUC `0.590524` to `0.595774` (`+0.005250`), average Precision@20 change `+0.015358`, average center error change `-2.633103` px.

## 5. Main Finding

RG-SSB + head shows stronger promise than the earlier RG-SSB-only runs. It improves several degraded cases, especially motion blur on all three sequences and Gaussian noise on Car1/Coke. The effect is not perfectly consistent: David2 low resolution and Gaussian noise drop, while the three-sequence averages remain positive because Car1 and Coke offset those David2 regressions. This remains a local proof-of-concept, not a final paper result.

## 6. Likely Reasons For Mixed Results

- The setup is still a small local training run.
- Training used only LaSOT.
- The debug run used only 1000 samples.
- The backbone remained frozen.
- There is no clean-degraded feature consistency loss.
- There is no response consistency loss.
- There is no clean/degraded balance control beyond the current training setup.
- Degradation is applied to search images only.
- There is no dedicated restoration supervision.

## 7. Recommended Next Experiment

Options:

- A. Add a fourth sequence.
- B. Train RG-SSB + head for more samples, e.g. 3000.
- C. Add clean/degraded feature consistency loss.
- D. Add response consistency loss.
- E. Move to HPC now.
- F. Add more architecture modules.

Recommended fastest high-quality step: **B. Train RG-SSB + head for 3000 degradation-aware LaSOT samples before adding new modules.**

The average result is mixed-positive: three of four conditions improve by average AUC, and motion blur improves across all three sequences. Scaling the same controlled setup is the fastest high-quality next step before adding losses or architectural components.

## 8. What To Postpone

- degradation token
- template-guided scan
- memory update
- response fusion
- full HPC training
- final paper claims

## 9. Decision

Decision: **continue current architecture with scaled training**.

The three-sequence evidence is encouraging enough to keep the current RG-SSB + head path, but not strong enough for broad robustness claims.

## 10. Final Table

| Sequence | Condition | Baseline AUC | RG-SSB + head AUC | AUC change | Baseline Precision@20 | RG-SSB + head Precision@20 | Center error change | Note |
|---|---|---:|---:|---:|---:|---:|---:|---|
| Car1 | clean | 0.575995 | 0.749728 | +0.173733 | 0.746078 | 0.983333 | -13.974615 | improved across AUC/precision/center error |
| Car1 | motion_blur medium | 0.157212 | 0.163638 | +0.006426 | 0.198039 | 0.212745 | -6.489876 | improved across AUC/precision/center error |
| Car1 | low_resolution medium | 0.214881 | 0.229247 | +0.014366 | 0.267647 | 0.291176 | +3.479625 | improved by AUC |
| Car1 | gaussian_noise medium | 0.207270 | 0.245312 | +0.038042 | 0.250980 | 0.322549 | -8.578029 | improved across AUC/precision/center error |
| David2 | clean | 0.794439 | 0.774656 | -0.019783 | 1.000000 | 1.000000 | +0.057587 | worse by AUC |
| David2 | motion_blur medium | 0.549680 | 0.576562 | +0.026882 | 0.970205 | 0.972067 | -0.977709 | improved across AUC/precision/center error |
| David2 | low_resolution medium | 0.806258 | 0.782916 | -0.023342 | 1.000000 | 1.000000 | +0.047708 | worse by AUC |
| David2 | gaussian_noise medium | 0.817542 | 0.770821 | -0.046721 | 1.000000 | 0.981378 | +0.719061 | worse by AUC |
| Coke | clean | 0.758259 | 0.769079 | +0.010820 | 0.958763 | 0.955326 | +0.915414 | improved by AUC |
| Coke | motion_blur medium | 0.700384 | 0.730087 | +0.029703 | 0.945017 | 0.927835 | +0.588151 | improved by AUC |
| Coke | low_resolution medium | 0.745875 | 0.761049 | +0.015174 | 0.945017 | 0.945017 | +0.549204 | improved by AUC |
| Coke | gaussian_noise medium | 0.746759 | 0.771188 | +0.024429 | 0.951890 | 0.945017 | -0.040342 | improved by AUC |

## 11. Average Table

| Condition | Average baseline AUC | Average RG-SSB + head AUC | Average AUC change | Decision note |
|---|---:|---:|---:|---|
| clean | 0.709564 | 0.764488 | +0.054923 | positive average |
| motion_blur medium | 0.469092 | 0.490096 | +0.021004 | positive average |
| low_resolution medium | 0.589005 | 0.591071 | +0.002066 | positive average |
| gaussian_noise medium | 0.590524 | 0.595774 | +0.005250 | positive average |

## Verification

Generated `experiments/rgssb_head_three_sequence_comparison.csv` by parsing `experiments/baseline_results.csv` with Python. No OSTrack training, evaluation, dataset modification, or `external/OSTrack` modification was performed.

Uncertain fields:

- Each degradation condition uses one seed.
- The report covers only Car1, David2, and Coke.
- Results are local proof-of-concept evidence, not final paper evidence.
