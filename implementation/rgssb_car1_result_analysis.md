# RG-SSB Car1 Result Analysis

Date: 2026-06-10

Inputs:

- `experiments/baseline_results.csv`
- `experiments/car1_rgssb_comparison.csv`
- `implementation/rgssb_training_smoke_result_log.md`
- `implementation/rgssb_debug_inference_log.md`
- `implementation/rgssb_degraded_training_setup_notes.md`
- `implementation/rgssb_train_debug_setup_notes.md`

## 1. Executive Summary

The first RG-SSB degradation-aware training cycle is technically successful but does not yet show consistent degradation-robust tracking improvement on OTB Car1.

Compared with the original OSTrack baseline, the degradation-trained RG-SSB smoke model improves Gaussian noise, is roughly similar on motion blur and JPEG compression by AUC, worsens low resolution, and slightly reduces clean performance. This is a smoke-test result only, not a final scientific conclusion.

## 2. What Worked Technically

- RG-SSB integration works behind config flags.
- RG-SSB can be enabled and disabled without changing the baseline config.
- RG-SSB can be trained while the rest of OSTrack is frozen.
- Checkpoints save and load.
- Evaluation runs for clean and degraded Car1.
- CSV logging works through `experiments/baseline_results.csv`.
- The degradation-aware training pipeline works and is config-gated.
- Synthetic training degradation preserves image size and does not modify boxes.

## 3. Current Performance Result

The most relevant comparison is:

- Baseline: `vitb_256_mae_ce_32x4_ep300`
- Degradation-trained RG-SSB: `vitb_256_mae_ce_32x4_ep300_rgssb_train_lasot_degraded_debug`

On clean Car1, AUC drops from `0.575995` to `0.557173` (`-0.018822`). Precision@20 drops from `0.746078` to `0.729412`, and mean center error increases by `1.018886` px.

On Gaussian noise medium, AUC improves from `0.207270` to `0.221782` (`+0.014512`). Precision@20 improves by `+0.030393`, and mean center error decreases by `1.999050` px.

On motion blur medium, AUC is almost unchanged: `0.157212` baseline vs `0.156805` RG-SSB (`-0.000407`). Precision@20 improves slightly, and center error improves by `7.679779` px, but the AUC does not support a clear success claim.

On JPEG compression medium, AUC is also roughly unchanged: `0.240012` baseline vs `0.238924` RG-SSB (`-0.001088`). Precision@20 improves slightly, but center error worsens slightly.

On low resolution medium, RG-SSB worsens: AUC drops from `0.214881` to `0.196525` (`-0.018356`), Precision@20 drops by `-0.020588`, and center error worsens by `14.086071` px.

## 4. Main Finding

The first degradation-aware RG-SSB smoke training does not yet produce consistent improvement across degradation types.

- Gaussian noise improved.
- Motion blur is roughly similar by AUC.
- Low resolution worsened.
- JPEG compression is roughly similar by AUC.
- Clean performance slightly dropped.

This means the implementation path is viable, but the current training strategy is too small and too weak to validate the method.

## 5. Likely Reasons

The likely reasons are practical rather than conclusive architectural failures:

- Training used only 100 LaSOT samples.
- Only RG-SSB was trained; the tracking head and backbone stayed frozen.
- There is no clean-degraded feature consistency loss.
- There is no response consistency loss.
- There is no target-aware restoration loss.
- Degradation was applied only to the search crop.
- Training was too short.
- Low-resolution recovery likely needs more specific supervision than generic tracking loss on 100 samples.

## 6. Recommended Next Training Iteration

Options:

- A. Increase degraded training samples from 100 to 1000.
- B. Train RG-SSB + head instead of RG-SSB only.
- C. Add clean-degraded feature consistency loss.
- D. Add response consistency loss.
- E. Add low-resolution-specific training.
- F. Add degradation token.
- G. Add template-guided attentive scan.

Recommended fastest next option: **A. Increase degraded training samples from 100 to 1000**.

Reason: this changes the least. It keeps the current architecture, current loss, current freezing strategy, current LaSOT-only setup, and current degradation adapter. Before adding new losses or modules, we should test whether the current RG-SSB block can learn a more stable correction from more degraded samples.

## 7. Recommended Next Experiment

Run one larger local smoke test:

- Config: new 1000-sample degraded LaSOT RG-SSB debug config.
- Trainable parameters: RG-SSB only.
- Frozen parameters: backbone and tracking head.
- Dataset: LaSOT only.
- Batch size: 1.
- GPU: one GTX 1080.
- Training samples: 1000.
- Validation samples: 100.
- Degradation types: `motion_blur`, `low_resolution`, `gaussian_noise`.
- Severity: `medium`.
- Apply to: `search_only`.

Then evaluate Car1 on:

- clean
- motion_blur medium
- low_resolution medium
- gaussian_noise medium

Do not expand to new modules until this larger smoke test confirms whether the current block can learn anything stable.

## 8. What To Postpone

- degradation token
- template-guided scan
- memory update
- full response fusion
- full HPC training
- all datasets
- clean-degraded consistency loss until the 1000-sample test is checked
- response consistency loss until the 1000-sample test is checked

## 9. Decision

Decision: **continue with the current architecture, but revise the training strategy**.

The current RG-SSB module should not be abandoned yet. The implementation works, Gaussian noise improved, and the training run is too small to judge the architecture. The next change should be more training signal, not a larger architecture.

## 10. Final Table

| Condition | Baseline AUC | Degradation-trained RG-SSB AUC | AUC change | Decision note |
|---|---:|---:|---:|---|
| clean | 0.575995 | 0.557173 | -0.018822 | Clean performance slightly dropped. |
| motion_blur medium | 0.157212 | 0.156805 | -0.000407 | Roughly similar by AUC; center error improved. |
| low_resolution medium | 0.214881 | 0.196525 | -0.018356 | Worsened; needs more targeted training. |
| jpeg_compression medium | 0.240012 | 0.238924 | -0.001088 | Roughly similar by AUC. |
| gaussian_noise medium | 0.207270 | 0.221782 | +0.014512 | Improved in this smoke test. |

## Verification

Generated `experiments/car1_rgssb_comparison.csv` by parsing `experiments/baseline_results.csv` with Python. No OSTrack training, evaluation, dataset modification, or `external/OSTrack` modification was performed.

Uncertain fields:

- Only Car1 is analyzed here.
- This is based on one seed per degradation condition.
- The untrained RG-SSB and clean-trained RG-SSB configs only have partial Car1 degradation coverage in the CSV, so missing rows are marked as `missing_rgssb` in the comparison CSV.
