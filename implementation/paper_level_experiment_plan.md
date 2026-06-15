# Paper-Level Experiment Plan

## Goal

The next experiment stage should test whether the current best RG-SSB setup provides reproducible degradation robustness beyond local proof-of-concept results. The goal is not to claim state-of-the-art yet. The goal is to build a paper-ready result structure that can support or reject a careful claim about restoration-guided feature adaptation for RGB template-search tracking under synthetic image-quality degradation.

## Current Best Method

Current best setup:

- Model: OSTrack + RG-SSB + `box_head`
- Backbone: frozen
- Trainable parameters: `rgssb.*` and `box_head.*`
- Training data: degradation-aware LaSOT
- Degradation protocol: search-only synthetic degradation
- Feature consistency: global clean-degraded post-RGSSB feature consistency
- Lambda: `0.02`
- Response consistency: disabled
- Target-region consistency: disabled
- HPC config: `vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_degraded_hpc_featcons_lam002`

This setup was selected because the local lambda sweep showed lambda `0.02` as the best feature-consistency setting, response consistency hurt overall, target-region feature consistency hurt relative to global feature consistency, and the HPC checkpoint produced a positive broader OTB result.

## Current Evidence

- Broader OTB is positive: average AUC change `+0.033144` over the original OSTrack baseline.
- Selected UAV123 was mixed/slightly negative: average AUC change `-0.005511`.
- Expanded UAV123 is positive/mixed: average AUC change `+0.017405`.
- Selected NFS was mixed/slightly negative: average AUC change `-0.002660`.
- Expanded NFS is mixed/negative: average AUC change `-0.014195`.
- Expanded UAV123 + NFS combined is near neutral: average AUC change `+0.001605`.
- Response consistency was rejected for the current method because it hurt the feature-only lambda `0.02` setup by `-0.019360` AUC locally.
- Target-region consistency was rejected for the current method because it hurt relative to global lambda `0.02` by `-0.023555` AUC locally.
- Global feature consistency lambda `0.02` remains the current best training objective.

## Main Benchmark Plan

Recommended benchmark order:

1. Broader OTB or full OTB subset.
2. Expanded UAV123.
3. Expanded NFS.
4. Optional additional benchmark if available, such as TrackingNet, LaSOT test, or another standard tracker benchmark with compatible evaluation tooling.

Run OTB first because the current method is already positive there and it is the safest benchmark for confirming pipeline stability. Then run UAV123 and NFS because those expose the current cross-benchmark risk.

## Evaluation Conditions

Primary conditions:

- clean
- motion_blur, severity `medium`
- low_resolution, severity `medium`
- gaussian_noise, severity `medium`

Later extensions:

- multiple degradation seeds
- multiple severities
- JPEG compression
- additional real-world corruptions
- mixed corruptions
- real degraded videos if benchmark annotations and protocol are available

## Metrics

Primary tracking metrics:

- Success AUC
- Precision@20
- Mean center error
- Mean IoU where available

Efficiency and reproducibility metrics:

- FPS / runtime
- parameter count
- training memory if available
- inference memory if available
- checkpoint name and epoch
- exact config name

## Baselines

Required baselines:

- Original OSTrack: `vitb_256_mae_ce_32x4_ep300`
- Current best method: `vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_degraded_hpc_featcons_lam002`

Optional local ablations if needed:

- RG-SSB-only
- RG-SSB + head without feature consistency
- global feature consistency lambda `0.02`
- response consistency
- target-region consistency

The optional ablations should be used to explain method design, not to expand the method with new modules.

## Run Order

1. Verify the current best checkpoint and config paths.
2. Run dry-runs for every benchmark suite.
3. Evaluate original OSTrack baseline on missing benchmark/condition rows.
4. Evaluate current best RG-SSB checkpoint on the same rows.
5. Parse and validate CSV rows.
6. Generate benchmark-specific comparison CSVs.
7. Generate cross-benchmark summary tables.
8. Inspect the largest drops before making claims.
9. Only after tables are complete, decide whether more sequences or seeds are needed.

## Success Criteria

Paper-level continuation is justified if:

- OTB remains positive on the broader/full subset.
- UAV123 average AUC is positive or near neutral without large systematic drops.
- NFS improves or at least no longer shows systematic negative transfer after broader evaluation.
- Overall cross-benchmark average is positive.
- Gains are not concentrated in one sequence only.
- Runtime and parameter overhead are acceptable relative to OSTrack.

## Failure Criteria

Revise training or architecture only if:

- broader/full UAV123 and NFS remain negative overall;
- clean tracking performance collapses;
- gains come from isolated outlier sequences;
- the method consistently worsens motion blur, low resolution, or Gaussian noise across benchmarks;
- runtime overhead is too high for the observed accuracy change.

Architecture changes should remain postponed until benchmark-level evidence shows the current training objective is insufficient.

