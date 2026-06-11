# RG-SSB + Head Car1/David2 Result Analysis

Date: 2026-06-10

Inputs:

- `experiments/baseline_results.csv`
- `experiments/rgssb_head_car1_david2_comparison.csv`
- `experiments/car1_rgssb_100_vs_1000_comparison.csv`
- `implementation/rgssb_1000_result_analysis.md`
- `implementation/rgssb_head_training_plan.md`
- `implementation/rgssb_car1_result_analysis.md`

## 1. Executive Summary

RG-SSB + head training gives a promising but inconsistent robustness signal across Car1 and David2.

On Car1, RG-SSB + head improves all analyzed conditions: clean, motion blur, low resolution, and Gaussian noise. On David2, it improves motion blur but reduces AUC on clean, low resolution, and Gaussian noise. This means the experiment is technically encouraging but not yet consistent enough for a final robustness claim.

## 2. Technical Status

- RG-SSB + head training completed.
- A checkpoint was saved and loaded for evaluation.
- Car1 and David2 evaluations completed.
- CSV logging works in `experiments/baseline_results.csv`.
- The pipeline is ready for the next controlled experiment.

## 3. Car1 Result Summary

Car1 clean:

- Baseline AUC: `0.575995`
- RG-SSB + head AUC: `0.749728`
- AUC change: `+0.173733`
- Precision@20: `0.746078` to `0.983333` (`+0.237255`)
- Center error: `16.455626` to `2.481011` (`-13.974615` px)

Car1 motion_blur medium:

- Baseline AUC: `0.157212`
- RG-SSB + head AUC: `0.163638`
- AUC change: `+0.006426`
- Precision@20: `0.198039` to `0.212745` (`+0.014706`)
- Center error: `82.957024` to `76.467148` (`-6.489876` px)

Car1 low_resolution medium:

- Baseline AUC: `0.214881`
- RG-SSB + head AUC: `0.229247`
- AUC change: `+0.014366`
- Precision@20: `0.267647` to `0.291176` (`+0.023529`)
- Center error: `55.176579` to `58.656204` (`+3.479625` px)

Car1 gaussian_noise medium:

- Baseline AUC: `0.207270`
- RG-SSB + head AUC: `0.245312`
- AUC change: `+0.038042`
- Precision@20: `0.250980` to `0.322549` (`+0.071569`)
- Center error: `64.898727` to `56.320698` (`-8.578029` px)

Car1 summary: RG-SSB + head improves AUC and Precision@20 on every analyzed Car1 condition. The low-resolution center error worsens, but AUC and Precision@20 improve.

## 4. David2 Result Summary

David2 clean:

- Baseline AUC: `0.794439`
- RG-SSB + head AUC: `0.774656`
- AUC change: `-0.019783`
- Precision@20: `1.000000` to `1.000000` (`+0.000000`)
- Center error: `1.541015` to `1.598602` (`+0.057587` px)

David2 motion_blur medium:

- Baseline AUC: `0.549680`
- RG-SSB + head AUC: `0.576562`
- AUC change: `+0.026882`
- Precision@20: `0.970205` to `0.972067` (`+0.001862`)
- Center error: `8.078309` to `7.100600` (`-0.977709` px)

David2 low_resolution medium:

- Baseline AUC: `0.806258`
- RG-SSB + head AUC: `0.782916`
- AUC change: `-0.023342`
- Precision@20: `1.000000` to `1.000000` (`+0.000000`)
- Center error: `1.516361` to `1.564069` (`+0.047708` px)

David2 gaussian_noise medium:

- Baseline AUC: `0.817542`
- RG-SSB + head AUC: `0.770821`
- AUC change: `-0.046721`
- Precision@20: `1.000000` to `0.981378` (`-0.018622`)
- Center error: `1.885668` to `2.604729` (`+0.719061` px)

David2 summary: RG-SSB + head improves motion blur, but clean, low resolution, and Gaussian noise drop by AUC. David2 baseline performance is already very high on clean, low-resolution, and Gaussian-noise conditions, so small regressions are easier to expose.

## 5. Main Finding

RG-SSB + head shows a promising signal, especially on Car1 and on David2 motion blur. However, improvement is not yet consistent across all degradations and sequences.

This is a local proof-of-concept result. It supports continuing the current architecture, but it is not a final paper result.

JPEG compression note: baseline JPEG rows exist for Car1 and David2, but RG-SSB + head JPEG compression has not been evaluated yet.

## 6. Likely Reasons For Mixed Results

- Training still uses only 1000 samples.
- Only LaSOT was used for training.
- Training may overfit to some appearance or degradation patterns.
- There is no clean-degraded feature consistency loss.
- There is no response consistency loss.
- There is no explicit low-resolution restoration supervision.
- Search-only degradation may be insufficient.
- Only RG-SSB and head were trained; the backbone remained frozen.

## 7. Recommended Next Experiment

Options:

- A. Add a third OTB sequence before changing training.
- B. Train RG-SSB + head with more samples, e.g. 3000.
- C. Add clean/degraded mixed training to protect clean performance.
- D. Add feature consistency loss.
- E. Add response consistency loss.
- F. Move to HPC now.

Recommended fastest high-quality step: **A. Add a third validation sequence before changing training.**

Reason: the current result is split by sequence. Car1 improves broadly, while David2 only improves on motion blur. Before increasing training or adding losses, we need one more OTB sequence to determine whether the mixed result is sequence-specific or systematic.

Recommended third sequence: use one of the already inspected candidate OTB sequences from the earlier multisequence baseline work, preferably a valid sequence with matching frame and ground-truth counts.

## 8. What To Postpone

- degradation token
- template-guided scan
- memory update
- full response fusion
- full HPC training
- final paper claims

## 9. Decision

Decision: **continue current architecture with more validation and revised training strategy**.

The RG-SSB + head experiment is strong enough to continue, but not consistent enough to scale blindly. Add a third sequence first, then decide whether the next training change should be more samples or consistency losses.

## 10. Final Table

| Sequence | Condition | Baseline AUC | RG-SSB + head AUC | AUC change | Baseline Precision@20 | RG-SSB + head Precision@20 | Center error change | Note |
|---|---|---:|---:|---:|---:|---:|---:|---|
| Car1 | clean | 0.575995 | 0.749728 | +0.173733 | 0.746078 | 0.983333 | -13.974615 | improved |
| Car1 | motion_blur medium | 0.157212 | 0.163638 | +0.006426 | 0.198039 | 0.212745 | -6.489876 | improved |
| Car1 | low_resolution medium | 0.214881 | 0.229247 | +0.014366 | 0.267647 | 0.291176 | +3.479625 | AUC/precision improved, center error worsened |
| Car1 | gaussian_noise medium | 0.207270 | 0.245312 | +0.038042 | 0.250980 | 0.322549 | -8.578029 | improved |
| David2 | clean | 0.794439 | 0.774656 | -0.019783 | 1.000000 | 1.000000 | +0.057587 | worse by AUC |
| David2 | motion_blur medium | 0.549680 | 0.576562 | +0.026882 | 0.970205 | 0.972067 | -0.977709 | improved |
| David2 | low_resolution medium | 0.806258 | 0.782916 | -0.023342 | 1.000000 | 1.000000 | +0.047708 | worse by AUC |
| David2 | gaussian_noise medium | 0.817542 | 0.770821 | -0.046721 | 1.000000 | 0.981378 | +0.719061 | worse |

## Verification

Generated `experiments/rgssb_head_car1_david2_comparison.csv` by parsing `experiments/baseline_results.csv` with Python. No OSTrack training, evaluation, dataset modification, or `external/OSTrack` modification was performed.

Uncertain fields:

- This analysis covers only Car1 and David2.
- Each degradation uses one seed.
- JPEG compression has not yet been evaluated for the RG-SSB + head model.
- Results are local proof-of-concept evidence, not final paper evidence.
