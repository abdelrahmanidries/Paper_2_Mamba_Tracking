# RG-SSB + Head Training Plan

Date: 2026-06-10

## Purpose

The 1000-sample RG-SSB-only degraded LaSOT run improved Gaussian noise and slightly improved low resolution on Car1, but it did not improve motion blur and clean performance remained below the original OSTrack baseline. The next local debug step is to train RG-SSB plus the tracking head while keeping the backbone frozen.

## Why RG-SSB-Only Was Insufficient

RG-SSB-only training changes the search feature tokens before the head, but the head remains fixed to the original OSTrack feature distribution. The 1000-sample result suggests RG-SSB can move some degraded cases in the right direction, but the frozen head may limit how well the tracker converts modified features into score maps, offsets, and sizes.

## Why RG-SSB + Head Next

Training `rgssb.*` and `box_head.*` is the smallest high-value change after RG-SSB-only training. It allows the prediction head to adapt to RG-SSB-modified features without unfreezing the ViT backbone. This keeps memory and overfitting risk lower than backbone fine-tuning.

## Why Backbone Remains Frozen

The GTX 1080 local setup has limited VRAM, and the goal is still a debug-scale experiment. Freezing the backbone reduces memory risk and preserves the pretrained OSTrack representation while testing whether the inserted block and head can adapt.

## Config

New config:

`external/OSTrack/experiments/ostrack/vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_degraded_1000_debug.yaml`

Key settings:

- `MODEL.RGSSB.ENABLE: True`
- `TRAIN.FREEZE_MODE: "rgssb_head"`
- trainable prefixes: `rgssb.*`, `box_head.*`
- frozen prefix: `backbone.*`
- dataset: LaSOT only
- training samples: 1000
- validation samples: 100
- degradation types: `motion_blur`, `low_resolution`, `gaussian_noise`
- apply to: `search_only`
- batch size: 1
- epoch: 1
- test epoch: 1

## Expected Benefit

The head should better adapt score-map, size, and offset prediction to features modified by RG-SSB. This may help motion blur and reduce clean-performance loss compared with RG-SSB-only training.

## Risks

- Clean performance may drop further if the head overfits the small debug set.
- Motion blur may still require response consistency or boundary-aware supervision.
- The head adds several million trainable parameters, increasing overfitting risk.
- This is still Car1-focused local debug evidence, not final paper evidence.

## Training Command

Run outside Codex:

```bash
cd external/OSTrack
conda run -n ostrack python lib/train/run_training.py \
  --script ostrack \
  --config vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_degraded_1000_debug \
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

Use `scripts/run_ostrack_otb_eval.py` with `--config vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_degraded_1000_debug` and `--overwrite_existing` for each condition.

## Before Moving To HPC

Check:

- Training completes without NaNs or OOM.
- Checkpoint `OSTrack_ep0001.pth.tar` is saved.
- Backbone is frozen and only `rgssb.*` plus `box_head.*` are trainable.
- Clean Car1 does not collapse.
- Motion blur improves or at least recovers relative to RG-SSB-only 1000-sample training.
- Low resolution and Gaussian noise retain their 1000-sample gains.

## Postponed

- full HPC training
- degradation token
- template-guided attentive scan
- memory update
- response fusion
- all datasets
- final paper claims
