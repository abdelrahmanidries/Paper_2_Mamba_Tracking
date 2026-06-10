# RG-SSB 1000-Sample Car1 Result Analysis

Date: 2026-06-10

Inputs:

- `experiments/baseline_results.csv`
- `experiments/car1_rgssb_100_vs_1000_comparison.csv`
- `experiments/car1_rgssb_comparison.csv`
- `implementation/rgssb_car1_result_analysis.md`
- `implementation/rgssb_training_smoke_result_log.md`
- `implementation/rgssb_degraded_training_setup_notes.md`

## 1. Executive Summary

Increasing degradation-aware RG-SSB training from 100 to 1000 LaSOT samples helped on some degraded Car1 conditions, but it did not solve robustness consistently.

The 1000-sample RG-SSB model improved Gaussian noise clearly relative to the OSTrack baseline and improved low resolution slightly. Motion blur did not improve by AUC, and clean performance remains below the original OSTrack baseline. This is still a debug-stage result, not a final method claim.

## 2. Technical Status

- 1000-sample degradation-aware RG-SSB training completed.
- A checkpoint was saved and used for evaluation.
- Clean and degraded Car1 evaluations completed.
- CSV logging works in `experiments/baseline_results.csv`.
- The training/evaluation pipeline is functional for the RG-SSB debug configs.

## 3. Result Summary

Comparison targets:

- Baseline: `vitb_256_mae_ce_32x4_ep300`
- 100-sample RG-SSB: `vitb_256_mae_ce_32x4_ep300_rgssb_train_lasot_degraded_debug`
- 1000-sample RG-SSB: `vitb_256_mae_ce_32x4_ep300_rgssb_train_lasot_degraded_1000_debug`

Clean Car1:

- Baseline AUC: `0.575995`
- 100-sample RG-SSB AUC: `0.557173`
- 1000-sample RG-SSB AUC: `0.552271`
- Clean performance is still below baseline and dropped slightly further at 1000 samples.

Motion blur medium:

- Baseline AUC: `0.157212`
- 100-sample RG-SSB AUC: `0.156805`
- 1000-sample RG-SSB AUC: `0.151563`
- Motion blur did not improve by AUC. Center error is lower than baseline, but the AUC and Precision@20 are worse, so this should not be counted as a win.

Low resolution medium:

- Baseline AUC: `0.214881`
- 100-sample RG-SSB AUC: `0.196525`
- 1000-sample RG-SSB AUC: `0.216832`
- Low resolution improved slightly over baseline at 1000 samples (`+0.001951` AUC). This is small, but it reverses the 100-sample degradation and is relevant to the restoration/super-resolution direction.

Gaussian noise medium:

- Baseline AUC: `0.207270`
- 100-sample RG-SSB AUC: `0.221782`
- 1000-sample RG-SSB AUC: `0.229402`
- Gaussian noise improved further at 1000 samples (`+0.022132` AUC over baseline).

JPEG compression:

- Baseline and 100-sample RG-SSB rows exist.
- The 1000-sample RG-SSB model has not yet been evaluated on JPEG compression in `experiments/baseline_results.csv`.

## 4. Interpretation

The 1000-sample run suggests that more degraded samples help RG-SSB learn some useful behavior, especially for Gaussian noise and slightly for low resolution. However, the result is not consistent enough for a robustness claim.

Likely reasons:

- RG-SSB-only training may be too limited.
- The tracking head remains frozen and may not adapt to RG-SSB-modified features.
- There is no clean-degraded feature consistency loss.
- There is no response consistency loss.
- Search-only degradation may not cover all template-search mismatch cases.
- Motion blur may need stronger temporal, boundary-aware, or response-level training.
- Low-resolution improvement is small but relevant to the MambaIR/super-resolution direction.

## 5. Recommended Next Experiment

Options:

- A. Train RG-SSB + head.
- B. Add clean-degraded feature consistency.
- C. Add response consistency loss.
- D. Increase training samples again.
- E. Add more degradations.
- F. Move to HPC now.

Recommended fastest high-value step: **A. Train RG-SSB + head on the same 1000-sample degradation-aware LaSOT setup, while keeping the backbone frozen.**

Reason:

- The current RG-SSB block appears to help Gaussian noise and low resolution when given more samples.
- The frozen head may be limiting how well the tracker uses RG-SSB-altered features.
- Training the head is simpler than adding new losses or architecture modules.
- It is still local-debug scale and does not require HPC.

Proposed next setup:

- Dataset: LaSOT only.
- Samples per epoch: 1000.
- Validation samples: 100.
- Trainable: RG-SSB + tracking head.
- Frozen: backbone.
- Degradation types: `motion_blur`, `low_resolution`, `gaussian_noise`.
- Apply to: `search_only`.
- Batch size: 1.
- Epochs: 1.

## 6. What To Postpone

- full HPC training
- degradation token
- template-guided attentive scan
- memory update
- response fusion
- all datasets
- final paper claims

## 7. Decision

Decision: **continue current architecture with revised training strategy**.

Do not abandon RG-SSB yet. The 1000-sample run shows useful movement on Gaussian noise and low resolution, but the training strategy needs to let the head adapt before adding larger architectural components.

## 8. Final Table

| Condition | Baseline AUC | 100-sample RG-SSB AUC | 1000-sample RG-SSB AUC | Best model | Note |
|---|---:|---:|---:|---|---|
| clean | 0.575995 | 0.557173 | 0.552271 | baseline | RG-SSB still below clean baseline. |
| motion_blur medium | 0.157212 | 0.156805 | 0.151563 | baseline | 1000 samples did not improve AUC. |
| low_resolution medium | 0.214881 | 0.196525 | 0.216832 | 1000-sample RG-SSB | Small improvement over baseline. |
| gaussian_noise medium | 0.207270 | 0.221782 | 0.229402 | 1000-sample RG-SSB | Clear improvement in this debug result. |

## Verification

Generated `experiments/car1_rgssb_100_vs_1000_comparison.csv` by parsing `experiments/baseline_results.csv` with Python. No OSTrack training, evaluation, dataset modification, or `external/OSTrack` modification was performed.

Uncertain fields:

- This analysis is Car1-only.
- Each degradation uses one seed.
- JPEG compression has not yet been evaluated for the 1000-sample RG-SSB model.
- The results are debug-scale and should not be used as final paper evidence.
