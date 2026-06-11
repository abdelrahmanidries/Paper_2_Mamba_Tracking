# RG-SSB Response Consistency Setup Notes

## Why Response Consistency Was Added

The feature-consistency lambda sweep found lambda `0.02` as the best local setup
so far. Feature consistency aligns post-RGSSB clean and degraded features, but it
does not directly check whether the tracker response map becomes stable. Response
consistency is added as the next minimal training-objective refinement while
keeping the architecture unchanged.

## Loss Formula

The degraded branch keeps the normal tracking loss. The clean branch is used only
as a consistency target.

```text
L_total = L_track_degraded + lambda_feat * L_feat + lambda_resp * L_resp

L_feat = L1(normalize(F_degraded), normalize(detach(F_clean)))
L_resp = MSE(score_map_degraded, detach(score_map_clean))
```

The clean response is detached when
`TRAIN.RESPONSE_CONSISTENCY.DETACH_CLEAN: True`.

## Config Name

`vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_degraded_3000_featcons_lam002_respcons_debug`

## Lambda Values

- `TRAIN.FEATURE_CONSISTENCY.WEIGHT: 0.02`
- `TRAIN.RESPONSE_CONSISTENCY.WEIGHT: 0.05`

## What Stays Fixed

- Backbone remains frozen.
- Trainable parameters remain `rgssb.*` and `box_head.*`.
- `MODEL.RGSSB.ENABLE: True`.
- `TRAIN.FREEZE_MODE: "rgssb_head"`.
- LaSOT train/val only.
- `DATA.TRAIN.SAMPLE_PER_EPOCH: 3000`.
- `DATA.VAL.SAMPLE_PER_EPOCH: 300`.
- `TRAIN.EPOCH: 1` and `TEST.EPOCH: 1`.
- Search-only synthetic degradation.
- Degradation types remain `motion_blur`, `low_resolution`, and
  `gaussian_noise` at medium severity.

## What Remains Postponed

- degradation token
- template-guided scan
- memory update
- response fusion module
- target-region feature weighting
- new architecture modules
- final paper claims

## Training Command

Run outside Codex:

```bash
cd external/OSTrack
conda run -n ostrack python lib/train/run_training.py \
  --script ostrack \
  --config vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_degraded_3000_featcons_lam002_respcons_debug \
  --save_dir output \
  --use_lmdb 0 \
  --use_wandb 0
```

## Evaluation Command

Use the experiment-cycle runner:

```bash
python3 scripts/run_rgssb_experiment_cycle.py \
  --cycle_config configs/rgssb_experiment_cycle_featcons_lam002_respcons.json
```

## Success Criteria

- Verifier reports finite total loss.
- Verifier reports finite feature-consistency loss.
- Verifier reports finite response-consistency loss.
- Trainable parameters are restricted to `rgssb.*` and `box_head.*`.
- Backbone parameters remain frozen.
- Experiment-cycle dry-run prints one training command and 12 evaluation
  commands.
- After real execution, CSV rows are written for all 12 configured
  sequence-condition pairs.

## Failure Criteria

- Missing `search_images_clean` in the real dataloader path.
- Missing `score_map` or `score_map_clean` in actor outputs.
- Non-finite feature, response, or total loss.
- Any `backbone.*` parameter remains trainable.
- Response consistency changes behavior when disabled.
