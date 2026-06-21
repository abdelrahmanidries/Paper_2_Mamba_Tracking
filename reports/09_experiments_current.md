# Current Experiments

## 1. Experimental Goal

The current experiment stage evaluates whether a restoration-guided Mamba insertion can improve degradation robustness in an RGB template-search tracker without changing the overall OSTrack architecture. The selected method is OSTrack with RG-SSB and box head trainable, frozen backbone, and global clean/degraded feature consistency with weight `0.02`.

This section reports the current evidence only. It does not claim state-of-the-art performance, universal degradation robustness, or consistent superiority across all benchmarks.

## 2. Method Under Test

Current best configuration:

- Base tracker: OSTrack.
- Added module: RG-SSB.
- Frozen parameters: backbone.
- Trainable parameters: `rgssb.*` and `box_head.*`.
- Training setup: degradation-aware LaSOT.
- Feature consistency: global clean/degraded feature consistency.
- Feature-consistency lambda: `0.02`.
- Response consistency: disabled.
- Target-region consistency: disabled.
- HPC config: `vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_degraded_hpc_featcons_lam002`.

The baseline is original OSTrack config `vitb_256_mae_ce_32x4_ep300`.

## 3. Datasets and Subsets

Current evaluated scopes:

| benchmark | sequence count | conditions | pairs |
| --- | ---: | ---: | ---: |
| OTB broader subset | 13 | 4 | 52 |
| UAV123 expanded subset | 16 | 4 | 64 |
| NFS corrected expanded subset | 32 | 4 | 128 |

The subsets are useful for method development and stress testing, but they are not full benchmark claims.

## 4. Degradation Protocol

Each sequence is evaluated under four conditions:

- clean
- motion_blur medium, seed 42
- low_resolution medium, seed 42
- gaussian_noise medium, seed 42

The protocol uses one seed and one severity level. This is sufficient for a controlled proof-of-concept comparison, but not for final claims about broad corruption robustness.

## 5. Training and Evaluation Metrics

Training keeps the backbone frozen and optimizes RG-SSB plus the box head. The selected loss includes normal degraded-branch tracking loss plus global clean/degraded feature consistency at lambda `0.02`.

Metrics:

- Success AUC.
- Precision@20.
- Mean center error.
- Mean IoU where available.

Reported changes are computed as RG-SSB minus original OSTrack baseline for the same sequence, degradation, severity, and seed.

## 6. Ablation Summary

The current method was selected after local and HPC comparisons:

- RG-SSB-only training was insufficient.
- RG-SSB + head training was stronger.
- Balanced clean/degraded training was not selected.
- Feature consistency lambda `0.02` was selected over `0.05` and `0.10`.
- Response consistency was rejected for the current freeze.
- Target-region feature consistency was rejected for the current freeze.

These ablations are useful for method selection, but the local ablation subsets remain proof-of-concept evidence.

## 7. OTB Results

On the 13-sequence broader OTB subset, the current method improves average AUC by `+0.033144` over the original OSTrack baseline across 52 sequence-condition pairs.

This is the strongest current benchmark result. It supports the claim that RG-SSB with global feature consistency can improve selected OTB robustness under the tested synthetic degradations.

## 8. UAV123 Results

On the expanded 16-sequence UAV123 subset, the current method improves average AUC by `+0.017405` across 64 pairs.

The UAV123 result is positive but should be described as mixed/positive rather than conclusive. The benchmark contains aerial viewpoint and camera-motion effects that differ from OTB and LaSOT training data.

## 9. Corrected NFS Results

NFS required a correction before current results could be used. The old NFS evaluation treated aligned XYXY annotations as XYWH and produced invalid metrics and overlays. Those rows are archived in `experiments/invalid_nfs_rows_before_xyxy_fix.csv` and are not used here.

Corrected NFS tracking was rerun using normalized aligned canonical XYWH annotations. On the corrected 32-sequence expanded NFS subset, the current method changes average AUC by `-0.009638` across 128 pairs.

The corrected `nfs_cheetah` low-resolution anchor is:

- OSTrack baseline AUC: `0.519832`.
- RG-SSB AUC: `0.516986`.

This corrected result replaces the old invalid large-drop interpretation.

## 10. Cross-Benchmark Interpretation

Current benchmark averages:

| benchmark | average AUC change |
| --- | ---: |
| broader OTB | +0.033144 |
| expanded UAV123 | +0.017405 |
| corrected expanded NFS | -0.009638 |

The paper-level 244-pair table is positive on average, but the gain is small and includes a negative NFS component. The corrected 212-pair cross-benchmark failure-inspection aggregate is `+0.001478`.

The scientifically defensible interpretation is that the current method shows promising robustness potential, especially on OTB, but cross-benchmark transfer remains mixed.

## 11. Failure-Mode Analysis

Corrected NFS drift-onset analysis contains 10 failure cases selected from the corrected top NFS drops. Terminal outcomes:

| terminal outcome | count |
| --- | ---: |
| persistent RG-SSB-specific target loss | 5 |
| sudden center jump | 3 |
| shared tracker failure | 1 |
| ambiguous | 1 |

This suggests that several corrected NFS failures are not simply shared benchmark difficulty. Some cases show multi-stage behavior where both trackers fail briefly, the baseline recovers, and RG-SSB later enters persistent target loss.

## 12. Current Paper Boundary

Safe wording:

> The current RG-SSB + head setup shows promising OTB robustness and mixed cross-benchmark transfer under corrected normalized-NFS evaluation.

Unsafe wording:

- State-of-the-art.
- Universal robustness.
- Consistent superiority across all benchmarks.
- Final benchmark superiority.
