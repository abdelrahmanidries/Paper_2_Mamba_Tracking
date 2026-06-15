# RG-SSB Target Feature Consistency Setup Notes

## Why This Was Implemented

Global feature consistency with lambda `0.02` was strong on broader OTB but mixed on UAV123 and NFS. The failure-focused analysis suggested that aligning the whole search region can over-weight background, distractors, camera motion, and clutter. Target-region feature consistency keeps the architecture unchanged while focusing clean-degraded alignment around the ground-truth target region.

## What Was Added

New debug config:

```text
external/OSTrack/experiments/ostrack/vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_degraded_3000_target_featcons_lam002_debug.yaml
```

New experiment-cycle config:

```text
configs/rgssb_experiment_cycle_target_featcons_lam002.json
```

New verifier:

```text
scripts/verify_rgssb_target_feature_consistency_pipeline.py
```

## Config Defaults

`TRAIN.TARGET_FEATURE_CONSISTENCY` is disabled by default in `external/OSTrack/lib/config/ostrack/config.py`.

Default fields:

```yaml
TRAIN:
  TARGET_FEATURE_CONSISTENCY:
    ENABLE: False
    WEIGHT: 0.0
    LOSS: "l1"
    MASK_TYPE: "gaussian"
    SIGMA_SCALE: 0.5
    BACKGROUND_WEIGHT: 0.05
    DETACH_CLEAN: True
    NORMALIZE: True
```

Default OSTrack behavior remains unchanged when `ENABLE=False`.

## Soft Gaussian Mask

The actor uses `search_anno[-1]`, which contains the transformed search-region target box in normalized `xywh` coordinates. The box center is mapped to the `16 x 16` post-RGSSB search-token grid. For each token center, a Gaussian weight is computed from normalized distance to the target center.

Mask shape:

```text
[B, 256, 1]
```

The mask includes a small background floor:

```text
M = background_weight + (1 - background_weight) * gaussian_target_weight
```

The first debug config uses:

- `MASK_TYPE: "gaussian"`
- `SIGMA_SCALE: 0.5`
- `BACKGROUND_WEIGHT: 0.05`

## Loss Formula

For the first ablation, global feature consistency is disabled and target-region feature consistency is enabled:

```text
L_total = L_track_degraded + lambda_tr * L_target_feature_consistency
```

with:

```text
L_target_feature_consistency =
  sum(M * |normalize(F_degraded) - normalize(detach(F_clean))|)
  / (sum(M) * C)
```

where:

- `F_degraded` is `pred_dict["search_feat_rgssb"]`.
- `F_clean` is `pred_dict["search_feat_rgssb_clean"]`.
- `M` is the soft target mask.
- `C` is the channel dimension, currently `768`.
- `lambda_tr = 0.02`.

## Training Configuration

The debug config keeps:

- RG-SSB enabled.
- `TRAIN.FREEZE_MODE: "rgssb_head"`.
- LaSOT-only debug training.
- `DATA.TRAIN.SAMPLE_PER_EPOCH: 3000`.
- `DATA.VAL.SAMPLE_PER_EPOCH: 300`.
- `TRAIN.BATCH_SIZE: 1`.
- `TRAIN.EPOCH: 1`.
- search-only degradation with `motion_blur`, `low_resolution`, and `gaussian_noise`.
- response consistency disabled.
- global feature consistency disabled.

## Verification Command

```bash
conda run -n ostrack python scripts/verify_rgssb_target_feature_consistency_pipeline.py
```

The verifier checks:

- target feature consistency is enabled;
- global feature consistency is disabled;
- response consistency is disabled;
- real train and validation loader batches include `search_images_clean`;
- `search_anno` exists;
- target mask shape and value range are valid;
- one mini forward/backward passes;
- target feature loss and total loss are finite;
- trainable parameters remain `rgssb.*` and `box_head.*`;
- backbone remains frozen.

Verified result on 2026-06-15:

```text
target_mask_shape: (1, 256, 1)
target_mask_min: 0.050001
target_mask_max: 0.987552
total_loss: 0.271812
target_feature_consistency_loss: 0.013623
trainable_params: 8554053
frozen_params: 86044416
rgssb_trainable_count: 16
head_trainable_count: 54
backbone_trainable_count: 0
trainable_grad_count: 70
```

## Experiment Cycle Command

Dry-run:

```bash
python3 scripts/run_rgssb_experiment_cycle.py \
  --cycle_config configs/rgssb_experiment_cycle_target_featcons_lam002.json \
  --dry_run
```

Actual local debug cycle outside Codex:

```bash
python3 scripts/run_rgssb_experiment_cycle.py \
  --cycle_config configs/rgssb_experiment_cycle_target_featcons_lam002.json
```

## Evaluation Conditions

The local debug cycle evaluates:

- `Car1`
- `David2`
- `Coke`

under:

- clean, severity `none`, seed `0`
- motion blur, severity `medium`, seed `42`
- low resolution, severity `medium`, seed `42`
- Gaussian noise, severity `medium`, seed `42`

## What Remains Postponed

- response consistency
- target box plus context ring ablation
- response-map-weighted feature consistency
- degradation token
- template-guided scan
- memory update
- response fusion
- new architecture modules
- final paper claims
