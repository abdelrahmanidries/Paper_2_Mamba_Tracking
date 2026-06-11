# RG-SSB + Head Balanced 3000-Sample Training Plan

Date: 2026-06-10

## Purpose

The fully degraded 3000-sample RG-SSB + head run improved average AUC over baseline for clean, motion blur, and low resolution, but Gaussian noise dropped slightly. It also improved motion blur and low resolution compared with the 1000-sample model, while clean and Gaussian noise regressed. The next local debug step is to balance clean and degraded samples without changing the architecture.

## Config

New config:

`external/OSTrack/experiments/ostrack/vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_balanced_3000_debug.yaml`

Key settings:

- `MODEL.RGSSB.ENABLE: True`
- `TRAIN.FREEZE_MODE: "rgssb_head"`
- trainable prefixes: `rgssb.*`, `box_head.*`
- frozen prefix: `backbone.*`
- dataset: LaSOT only
- training samples: 3000
- validation samples: 300
- degradation probability: 0.5
- degradation types: `motion_blur`, `low_resolution`, `gaussian_noise`
- degradation severity: `medium`
- degradation target: `search_only`
- batch size: 1
- epoch: 1
- test epoch: 1
- template size: 128
- search size: 256

## Why Balanced Clean/Degraded Training Is Needed

The fully degraded setup exposes RG-SSB and the head to degraded search crops every time. That can help degraded tracking, but it may shift the model away from clean tracking behavior and may overfit to degraded appearance statistics. A 50/50 clean-degraded mix tests whether the model can keep clean tracking stable while still learning degradation robustness.

## What Changed From The Fully Degraded 3000 Setup

Only one training-data setting changes:

- `DATA.DEGRADATION.PROBABILITY: 1.0` becomes `DATA.DEGRADATION.PROBABILITY: 0.5`

The architecture, dataset, sample counts, degradation types, freeze mode, template/search sizes, and one-epoch debug schedule are unchanged.

## Why Probability Is 0.5

Probability `0.5` creates an approximate clean/degraded balance. In the current degradation adapter, each training sample calls `begin_sample()`, and degradation is skipped when the sampled random value exceeds the configured probability. Therefore:

- `0.0` means clean samples.
- `1.0` means degraded samples.
- `0.5` means an approximate half clean, half degraded mixture.

## Why Backbone Remains Frozen

The local goal is still controlled debug training on limited hardware. Freezing the backbone keeps memory lower, preserves pretrained OSTrack features, and isolates whether RG-SSB plus the tracking head can adapt to mixed clean/degraded search features.

## Why RG-SSB + Head Remains Trainable

RG-SSB modifies the search feature tokens before the head. The head must remain trainable so score, offset, and size prediction can adapt to those modified features. Training the backbone is postponed until the debug objective is clearer.

## Expected Benefit

Balanced training should reduce clean-performance regression and may recover Gaussian-noise behavior while preserving the motion-blur and low-resolution gains seen in the fully degraded 3000-sample run.

## Risks

- Degraded robustness may weaken because only about half the samples are degraded.
- The 3000-sample debug run may still be too small.
- Search-only degradation may not cover template degradation effects.
- Without feature or response consistency, the model may still learn unstable condition-specific behavior.

## Training Command

Run outside Codex:

```bash
cd external/OSTrack
conda run -n ostrack python lib/train/run_training.py \
  --script ostrack \
  --config vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_balanced_3000_debug \
  --save_dir output \
  --use_lmdb 0 \
  --use_wandb 0
```

## Evaluation Conditions After Training

Evaluate the trained balanced config on:

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

`--config vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_balanced_3000_debug`

## What Would Justify Moving To HPC

Moving to HPC is justified if the balanced 3000-sample model:

- improves average AUC over baseline on clean, motion blur, low resolution, and Gaussian noise;
- improves or matches the fully degraded 3000-sample model on clean and Gaussian noise;
- does not lose the motion-blur and low-resolution gains;
- shows no severe per-sequence collapse.

## What Would Mean Feature/Response Consistency Is Needed Next

Add feature or response consistency next if:

- clean performance still regresses;
- Gaussian noise remains below baseline;
- improvements are isolated to one sequence;
- motion blur and low resolution improve but center error becomes worse;
- the balanced objective is stable but not strong enough.

## Postponed

- feature consistency loss
- response consistency loss
- degradation token
- template-guided scan
- memory update
- response fusion
- final paper claims
