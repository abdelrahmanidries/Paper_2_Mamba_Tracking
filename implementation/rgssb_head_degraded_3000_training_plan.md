# RG-SSB + Head 3000-Sample Degraded LaSOT Training Plan

Date: 2026-06-10

## Purpose

The 1000-sample RG-SSB + head experiment was mixed-positive across Car1, David2, and Coke. Average AUC improved on clean, motion blur, low resolution, and Gaussian noise, with the strongest signal on clean and motion blur. The next debug step is to scale the same controlled setup to 3000 degraded LaSOT samples before adding new modules or losses.

## Config

New config:

`external/OSTrack/experiments/ostrack/vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_degraded_3000_debug.yaml`

Key settings:

- `MODEL.RGSSB.ENABLE: True`
- `TRAIN.FREEZE_MODE: "rgssb_head"`
- trainable prefixes: `rgssb.*`, `box_head.*`
- frozen prefix: `backbone.*`
- dataset: LaSOT only
- training samples: 3000
- validation samples: 300
- degradation types: `motion_blur`, `low_resolution`, `gaussian_noise`
- degradation severity: `medium`
- degradation target: `search_only`
- batch size: 1
- epoch: 1
- test epoch: 1
- template size: 128
- search size: 256

## Why Scale From 1000 To 3000 Samples

The 1000-sample run showed enough signal to justify more data, but not enough consistency for a claim. Increasing to 3000 samples keeps the experiment local and controlled while testing whether the mixed result was caused by undertraining rather than the module design.

## Why Keep RG-SSB + Head Training

RG-SSB-only training left the original tracking head fixed to the baseline feature distribution. Training `rgssb.*` and `box_head.*` lets the head adapt to RG-SSB-modified search features while keeping the backbone representation unchanged.

## Why Backbone Remains Frozen

The local GTX 1080 setup has limited memory, and this is still a debug experiment. Freezing the backbone reduces OOM risk, limits overfitting, and keeps the test focused on whether the inserted restoration-guided block plus head can improve degraded tracking.

## Why The Same Degradation Types Are Used

The three-sequence comparison used motion blur, low resolution, and Gaussian noise. Keeping the same degradation set isolates the effect of scaling samples from 1000 to 3000. Adding new degradations now would make the result harder to interpret.

## Success Criteria

Success would mean:

- Training completes without OOM or NaNs.
- Checkpoint `OSTrack_ep0001.pth.tar` is saved for the 3000-sample config.
- RG-SSB and head remain the only trainable parameter groups.
- Average AUC across Car1, David2, and Coke improves over the 1000-sample RG-SSB + head model on at least motion blur and one of low resolution or Gaussian noise.
- Clean average AUC does not collapse relative to the original OSTrack baseline.

## Failure Criteria

Failure would mean:

- Training fails from OOM, NaNs, or data-loading errors.
- Backbone parameters are accidentally trainable.
- Clean performance collapses.
- Degraded average AUC does not improve over the 1000-sample model.
- Improvements appear only on one sequence while the others regress strongly.

## Training Command

Run outside Codex:

```bash
cd external/OSTrack
conda run -n ostrack python lib/train/run_training.py \
  --script ostrack \
  --config vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_degraded_3000_debug \
  --save_dir output \
  --use_lmdb 0 \
  --use_wandb 0
```

## Evaluation Conditions After Training

Evaluate the trained 3000-sample config on:

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

Use `scripts/run_ostrack_otb_eval.py` with:

`--config vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_degraded_3000_debug`

and `--overwrite_existing` only when intentionally replacing rows for the same unique key.

## Before Moving To HPC

Check:

- The 3000-sample training log confirms `TRAIN.FREEZE_MODE: rgssb_head`.
- Only `rgssb.*` and `box_head.*` are trainable.
- The saved checkpoint resolves through `TEST.EPOCH: 1`.
- Three-sequence average AUC improves over the 1000-sample model.
- Clean performance remains acceptable.
- Failure cases are understood before increasing datasets or adding losses.

## Postponed

- degradation token
- template-guided scan
- memory update
- response fusion
- feature consistency loss
- response consistency loss
- full HPC training
- final paper claims
