# RG-SSB Target-Region Feature Consistency Plan

## 1. Motivation

The current best RG-SSB + head setup uses global clean-degraded feature consistency with lambda `0.02`. The broader OTB result is positive, but the expanded failure-focused UAV123 + NFS result is only near neutral overall:

- broader OTB average AUC change: `+0.033144`
- expanded UAV123 average AUC change: `+0.017405`
- expanded NFS average AUC change: `-0.014195`
- expanded UAV123 + NFS overall average AUC change: `+0.001605`

This suggests that global feature consistency is not reliably transferring across harder UAV123/NFS cases. A likely failure mode is that the current feature loss aligns all search tokens equally, including background, clutter, and distractors. Target-region feature consistency should focus the clean-degraded alignment on the object area while keeping the architecture unchanged.

## 2. Current Feature Consistency Implementation

Current clean/degraded search creation:

- File: `external/OSTrack/lib/train/data/processing.py`
- `STARKProcessing.__call__` crops the search image with `jittered_center_crop`.
- When consistency is enabled and `s == "search"`, it stores `clean_search_crops = [crop.copy() for crop in crops]` before degradation.
- The degraded branch then applies `self.degradation.apply(crops, role=s)`.
- Both clean and degraded search crops use the same transformed box coordinates, passed through `bbox=boxes`.
- The clean search tensor is returned as `data["search_images_clean"]`.

Current post-RGSSB feature return:

- File: `external/OSTrack/lib/models/ostrack/ostrack.py`
- `forward_head` takes the search tokens from the backbone output: `cat_feature[:, -self.feat_len_s:]`.
- If RG-SSB is enabled, it applies `self.rgssb(...)`.
- It stores the post-RGSSB search tokens as `search_feat_rgssb`.
- When `return_search_features=True`, the model returns `out["search_feat_rgssb"]`.
- Current expected tensor shape is `[B, 256, 768]`, corresponding to a `16 x 16` search grid with 768 channels.

Current loss computation:

- File: `external/OSTrack/lib/train/actors/ostrack.py`
- The degraded branch computes the normal tracking losses.
- If clean/degraded consistency is enabled, the actor requires `data["search_images_clean"]`.
- The clean branch is run with the same template and clean search crop.
- Current global feature consistency compares:

```text
F_degraded = pred_dict["search_feat_rgssb"]
F_clean = pred_dict["search_feat_rgssb_clean"]
```

- If `DETACH_CLEAN=True`, the clean feature is detached.
- If `NORMALIZE=True`, both features are normalized along channel dimension.
- Current loss is global L1 or MSE over all `[B, 256, 768]` tokens.
- Current best lambda from local sweep is `0.02`.

## 3. Why Global Feature Consistency May Fail

Global consistency treats every search token equally. On the `16 x 16` search grid, most tokens are usually background. For small targets, the target may occupy only a few grid cells while background, distractors, and padding dominate the loss.

This is risky for UAV123 and NFS:

- UAV123 has aerial viewpoint, camera motion, small targets, scale changes, and background motion.
- NFS includes fast motion, high-frame-rate sampling behavior, sports/action sequences, and severe motion blur.
- Aligning full clean/degraded search features may over-constrain background regions that are not semantically relevant to tracking.
- If background appearance changes under degradation, global alignment can compete with target localization.
- The target region should receive higher weight than background; background can remain weakly constrained or ignored.

## 4. Proposed Target-Region Feature Consistency

Use the ground-truth search box already available as `data["search_anno"]` to create a spatial target mask over the `16 x 16` search-token grid.

Minimal design:

1. Use the transformed search box in search-image coordinates.
2. Map the box from search image space to token grid space.
3. Create a soft spatial mask centered on the target.
4. Reshape post-RGSSB features from `[B, 256, 768]` to `[B, 16, 16, 768]`.
5. Compare clean/degraded features with weighted L1.
6. Detach clean features as before.
7. Keep backbone frozen and train only `rgssb.*` and `box_head.*`.

Recommended loss formula for the first minimal version:

```text
L_total = L_track_degraded + lambda_tr * L_target_feature_consistency

L_target_feature_consistency =
  sum(M * |normalize(F_degraded) - normalize(detach(F_clean))|)
  / (sum(M) * C)
```

where:

- `F_degraded` and `F_clean` are post-RGSSB search features.
- `M` is a target-centered mask shaped `[B, 256, 1]` or `[B, 1, 16, 16]`.
- `C = 768`.
- `lambda_tr = 0.02` initially.

Alternative ablation formula:

```text
L_total = L_track_degraded
        + lambda_feat * L_global_feature_consistency
        + lambda_tr * L_target_feature_consistency
```

The first implementation should use target-region only. Keeping global consistency simultaneously should be an ablation, not the default, because the current hypothesis is that global alignment is the problem.

## 5. Implementation Options

| option | difficulty | memory cost | risk | expected benefit | recommendation |
| --- | --- | --- | --- | --- | --- |
| A. Hard binary target mask on `16 x 16` grid | Low | Very low | Box-to-token quantization can be brittle for small targets | Directly suppresses background loss | Useful baseline, but too sharp for first choice |
| B. Soft Gaussian target mask on `16 x 16` grid | Low-medium | Very low | Sigma choice needs tuning | Smoothly emphasizes target and nearby context | Recommended first implementation |
| C. Target box plus context ring | Medium | Very low | More mask hyperparameters | Captures target plus immediate surrounding context | Good second ablation |
| D. Response-map-weighted feature consistency | Medium-high | Low | Uses model predictions, can reinforce bad localization early | Aligns where model believes target is | Postpone until target-mask baseline is known |
| E. Full global feature consistency | Already implemented | Very low | Background dominates loss | Proven useful on OTB but mixed cross-benchmark | Keep only as comparison baseline |

## 6. Recommended First Implementation

Use a soft Gaussian target mask over the `16 x 16` search-token grid.

Suggested config defaults:

```yaml
TRAIN:
  TARGET_FEATURE_CONSISTENCY:
    ENABLE: True
    WEIGHT: 0.02
    LOSS: "l1"
    NORMALIZE: True
    DETACH_CLEAN: True
    MASK_TYPE: "gaussian"
    SIGMA_SCALE: 0.5
    BACKGROUND_WEIGHT: 0.05
  FEATURE_CONSISTENCY:
    ENABLE: False
  RESPONSE_CONSISTENCY:
    ENABLE: False
```

Rationale:

- Gaussian weighting reduces sensitivity to token-grid quantization.
- A small `BACKGROUND_WEIGHT = 0.05` prevents the loss from completely ignoring immediate context and stabilizes normalization.
- `WEIGHT = 0.02` preserves the best feature-consistency lambda found so far.
- Clean features should remain detached.
- No new architecture module is added.

## 7. Files for Future Implementation

Likely implementation files:

- `external/OSTrack/lib/config/ostrack/config.py`
  - Add disabled-by-default `TRAIN.TARGET_FEATURE_CONSISTENCY` fields.
- `external/OSTrack/lib/train/actors/ostrack.py`
  - Add target-region feature consistency enable flag.
  - Request `return_search_features=True` when target feature consistency is enabled.
  - Build target mask from `gt_dict["search_anno"][-1]`.
  - Compute weighted target feature loss.
  - Log `Loss/target_feature_consistency`.
- `external/OSTrack/lib/train/data/processing.py`
  - Modify only if box coordinate access is insufficient. Current `search_anno` appears sufficient because clean/degraded crops share transformed `boxes`.
- `scripts/verify_rgssb_target_feature_consistency_pipeline.py`
  - Verify config, data path, model build, masks, finite losses, and trainable/frozen parameters.
- New OSTrack config YAML:
  - local debug config first.
- New experiment-cycle config:
  - local debug training/evaluation cycle.

Files not needed for the first implementation:

- no new model architecture module
- no degradation token
- no template-guided scan
- no memory update
- no response fusion

## 8. Recommended First Experiment Config

Use a local debug config first:

```text
vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_degraded_3000_target_featcons_lam002_debug.yaml
```

Suggested setup:

- `MODEL.RGSSB.ENABLE: True`
- `TRAIN.FREEZE_MODE: "rgssb_head"`
- `DATA.TRAIN.DATASETS_NAME: ["LASOT"]`
- `DATA.TRAIN.SAMPLE_PER_EPOCH: 3000`
- `DATA.VAL.DATASETS_NAME: ["LASOT"]`
- `DATA.VAL.SAMPLE_PER_EPOCH: 300`
- `TRAIN.BATCH_SIZE: 1`
- `TRAIN.NUM_WORKER: 2`
- `TRAIN.EPOCH: 1`
- `TEST.EPOCH: 1`
- `DATA.DEGRADATION.ENABLE: True`
- `DATA.DEGRADATION.PROBABILITY: 1.0`
- `DATA.DEGRADATION.APPLY_TO: "search_only"`
- `DATA.DEGRADATION.TYPES: ["motion_blur", "low_resolution", "gaussian_noise"]`
- `DATA.DEGRADATION.SEVERITY: "medium"`
- `DATA.DEGRADATION.SEED: 42`
- `TRAIN.TARGET_FEATURE_CONSISTENCY.ENABLE: True`
- `TRAIN.TARGET_FEATURE_CONSISTENCY.WEIGHT: 0.02`
- `TRAIN.TARGET_FEATURE_CONSISTENCY.MASK_TYPE: "gaussian"`
- `TRAIN.TARGET_FEATURE_CONSISTENCY.SIGMA_SCALE: 0.5`
- `TRAIN.TARGET_FEATURE_CONSISTENCY.BACKGROUND_WEIGHT: 0.05`
- `TRAIN.FEATURE_CONSISTENCY.ENABLE: False`
- `TRAIN.RESPONSE_CONSISTENCY.ENABLE: False`

If the debug result is positive, create the HPC config:

```text
vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_degraded_hpc_target_featcons_lam002.yaml
```

## 9. Verification Plan Before Training

Before any real training:

- Config loads.
- Model builds.
- Clean search branch is enabled when target-region feature consistency is enabled.
- Post-RGSSB clean and degraded features have shape `[B, 256, 768]`.
- Target mask has shape `[B, 1, 16, 16]` or `[B, 256, 1]`.
- Target mask aligns with `search_anno` in transformed search-crop coordinates.
- Mask values are finite and normalized.
- Target feature loss is finite.
- One real dataloader forward/backward pass works.
- Trainable parameters remain `rgssb.*` and `box_head.*`.
- Backbone parameters remain frozen.
- Default behavior is unchanged when `TRAIN.TARGET_FEATURE_CONSISTENCY.ENABLE=False`.

## 10. Evaluation Plan

Evaluate the target-region feature-consistency checkpoint on:

- broader OTB set used for HPC lambda `0.02`
- expanded UAV123 failure-focused subset
- expanded NFS failure-focused subset

Compare against:

- original OSTrack baseline: `vitb_256_mae_ce_32x4_ep300`
- global feature consistency lambda `0.02` local debug setup
- HPC global feature consistency lambda `0.02`

Primary metrics:

- success AUC
- Precision@20
- mean center error, ignoring NaN pairs in averages

Primary comparisons:

- NFS average AUC change versus global feature consistency
- UAV123 average AUC change versus global feature consistency
- broader OTB average AUC remains positive
- cross-benchmark average improves over global feature consistency

## 11. Decision Rules

Proceed if:

- NFS average improves over global feature consistency.
- UAV123 does not drop meaningfully.
- OTB remains positive.
- Overall cross-benchmark average improves over global feature consistency.
- Gains are not isolated to one sequence.

Reject or revise if:

- clean performance collapses.
- motion blur worsens strongly.
- target mask introduces unstable or non-finite losses.
- gains are isolated to one sequence.
- target-region loss reduces OTB robustness while not improving NFS/UAV123.

## 12. Final Recommendation

Implement the minimal target-region feature consistency path using a soft Gaussian target mask on the `16 x 16` search-token grid. Keep architecture unchanged, keep the backbone frozen, train only RG-SSB + box head, disable global feature consistency by default for this ablation, and keep lambda `0.02`.

This is the lowest-risk next training refinement because it directly addresses the suspected failure mode of global background-dominated feature alignment without adding new architecture modules.

