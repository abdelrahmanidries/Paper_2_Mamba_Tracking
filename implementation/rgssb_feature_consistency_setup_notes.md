# RG-SSB Feature Consistency Setup Notes

Date: 2026-06-10

## What Was Added

This setup adds a minimal clean-degraded feature consistency training path for RG-SSB + head debug training. It keeps the architecture unchanged and leaves default OSTrack behavior disabled by default.

New debug config:

`external/OSTrack/experiments/ostrack/vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_degraded_3000_featcons_debug.yaml`

## Dataloader Crash Fix

Observed crash:

```text
KeyError: "Feature consistency requires data['search_images_clean']."
```

Root cause:

The initial verifier manually exercised `STARKProcessing`, but it did not test the real `build_dataloaders` path. The train processing path preserved `search_images_clean`, but the validation processing path did not receive `cfg.TRAIN.FEATURE_CONSISTENCY`. Since OSTrack uses the same actor for train and validation, validation batches also need `search_images_clean` whenever feature consistency is enabled.

Fix:

- `external/OSTrack/lib/train/base_functions.py` now passes `feature_consistency_cfg=cfg.TRAIN.FEATURE_CONSISTENCY` to both train and validation `STARKProcessing`.
- `external/OSTrack/lib/train/actors/ostrack.py` keeps the hard failure when the key is missing, but now prints the available batch keys in the error message.
- `scripts/verify_rgssb_feature_consistency_real_loader.py` verifies both train and validation loader batches contain `search_images_clean`.

## Why Feature Consistency Was Added

The fully degraded 3000-sample RG-SSB + head setup was stronger than the balanced 3000-sample setup overall, but results remained mixed. Feature consistency adds a direct clean-degraded alignment signal without adding new modules.

## Where Clean Search Is Preserved

File:

`external/OSTrack/lib/train/data/processing.py`

When `TRAIN.FEATURE_CONSISTENCY.ENABLE` is true, `STARKProcessing` preserves a clean copy of the search crop before degradation and returns it as:

`search_images_clean`

The normal `search_images` path can still receive synthetic degradation. Both clean and degraded search crops use the same crop geometry and box coordinates.

## Where Features Are Returned

File:

`external/OSTrack/lib/models/ostrack/ostrack.py`

The model now accepts:

`return_search_features=True`

When requested, it returns:

`search_feat_rgssb`

Expected shape for the current debug config:

`[B, 256, 768]`

Default inference and evaluation behavior is unchanged because the feature tensor is returned only when requested.

## Where The Loss Is Computed

File:

`external/OSTrack/lib/train/actors/ostrack.py`

When `TRAIN.FEATURE_CONSISTENCY.ENABLE` is true:

- the degraded search branch computes the normal tracking losses;
- the clean search branch returns post-RGSSB search features;
- the clean feature is detached when `DETACH_CLEAN=True`;
- feature consistency is added to the total loss.

## Loss Formula

```text
L_total = L_track_degraded + lambda_feat * L_feat_consistency

L_feat_consistency = L1(normalize(F_degraded), normalize(detach(F_clean)))
```

Config value:

`TRAIN.FEATURE_CONSISTENCY.WEIGHT: 0.05`

## What Remains Postponed

- feature consistency target-region masking
- response consistency loss
- clean tracking loss branch
- degradation token
- template-guided scan
- memory update
- response fusion
- new architecture modules
- full training claims

## Verification Command

```bash
conda run -n ostrack python scripts/verify_rgssb_feature_consistency_pipeline.py
```

The verifier checks:

- config values;
- LaSOT root availability;
- model build;
- trainable parameters remain `rgssb.*` and `box_head.*`;
- backbone remains frozen;
- one mini forward/backward works;
- feature consistency loss is finite;
- post-RGSSB feature shape is `[1, 256, 768]`.

## Real-Loader Verification Command

```bash
conda run -n ostrack python scripts/verify_rgssb_feature_consistency_real_loader.py
```

This verifier checks:

- the actual `build_dataloaders` path;
- train batch keys;
- validation batch keys;
- `search_images_clean` in both train and validation batches;
- shape compatibility between `search_images` and `search_images_clean`;
- one real-batch forward/backward through `OSTrackActor`;
- finite feature consistency loss.

## Training Smoke Test Command

Run outside Codex:

```bash
cd external/OSTrack
conda run -n ostrack python lib/train/run_training.py \
  --script ostrack \
  --config vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_degraded_3000_featcons_debug \
  --save_dir output \
  --use_lmdb 0 \
  --use_wandb 0
```

## Evaluation Conditions After Training

Evaluate:

- Car1 clean
- Car1 motion_blur medium
- Car1 low_resolution medium
- Car1 gaussian_noise medium
- David2 clean
- David2 motion_blur medium
- David2 low_resolution medium
- David2 gaussian_noise medium
- Coke clean
- Coke motion_blur medium
- Coke low_resolution medium
- Coke gaussian_noise medium

Compare against:

- original OSTrack baseline
- 1000-sample RG-SSB + head
- fully degraded 3000 RG-SSB + head
- balanced 3000 RG-SSB + head
