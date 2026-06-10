# RG-SSB Degraded Training Setup Notes

Date: 2026-06-10

## Purpose

The first RG-SSB-only training smoke test used clean LaSOT samples. It verified the training loop, checkpoint save/load, and evaluation path, but it did not improve degradation robustness. In the recorded smoke result, clean Car1 dropped slightly and motion-blur Car1 did not improve. This is expected for clean-only training because RG-SSB never saw degraded template/search evidence during optimization.

This setup adds synthetic degradation augmentation to the OSTrack training data path for a tiny RG-SSB-only debug run.

## What Was Added

External OSTrack files:

- `external/OSTrack/lib/config/ostrack/config.py`
- `external/OSTrack/lib/train/data/degradation.py`
- `external/OSTrack/lib/train/data/processing.py`
- `external/OSTrack/lib/train/base_functions.py`
- `external/OSTrack/experiments/ostrack/vitb_256_mae_ce_32x4_ep300_rgssb_train_lasot_degraded_debug.yaml`

Main project files:

- `scripts/verify_training_degradation_pipeline.py`
- `implementation/rgssb_degraded_training_setup_notes.md`
- `implementation/patches/ostrack_rgssb_integration.patch`

## Config-Gated Defaults

The default config now includes:

- `DATA.DEGRADATION.ENABLE = False`
- `DATA.DEGRADATION.PROBABILITY = 0.0`
- `DATA.DEGRADATION.APPLY_TO = "search_only"`
- `DATA.DEGRADATION.TYPES = ["motion_blur", "low_resolution"]`
- `DATA.DEGRADATION.SEVERITY = "medium"`
- `DATA.DEGRADATION.SEED = 42`

The default is disabled, so baseline OSTrack processing is unchanged unless a debug config explicitly enables degradation.

## Training Insertion Point

The augmentation is inserted in:

`external/OSTrack/lib/train/data/processing.py::STARKProcessing.__call__`

It runs after `jittered_center_crop(...)` creates template/search crops and before `self.transform[s](...)` converts images to tensors, applies brightness jitter, and normalizes. At this point the image crops are numpy RGB arrays, and the bounding boxes/masks have already been computed. The degradation adapter preserves image size and does not modify boxes or masks.

Only the training processing object receives `cfg.DATA.DEGRADATION`. The validation processing path remains clean.

## Debug Config

Config:

`external/OSTrack/experiments/ostrack/vitb_256_mae_ce_32x4_ep300_rgssb_train_lasot_degraded_debug.yaml`

Key settings:

- `MODEL.RGSSB.ENABLE: True`
- `TRAIN.FREEZE_MODE: "rgssb_only"`
- `DATA.TRAIN.DATASETS_NAME: ["LASOT"]`
- `DATA.VAL.DATASETS_NAME: ["LASOT"]`
- `TRAIN.BATCH_SIZE: 1`
- `TRAIN.NUM_WORKER: 2`
- `TRAIN.EPOCH: 1`
- `DATA.TRAIN.SAMPLE_PER_EPOCH: 100`
- `DATA.VAL.SAMPLE_PER_EPOCH: 20`
- `TEST.EPOCH: 1`
- `DATA.DEGRADATION.ENABLE: True`
- `DATA.DEGRADATION.PROBABILITY: 1.0`
- `DATA.DEGRADATION.APPLY_TO: "search_only"`
- `DATA.DEGRADATION.TYPES: ["motion_blur", "low_resolution"]`
- `DATA.DEGRADATION.SEVERITY: "medium"`
- `DATA.DEGRADATION.SEED: 42`

## Why Search Only First

`search_only` keeps the template clean and degrades the search crop. This is the smallest test of whether RG-SSB can help the tracker recover target-discriminative search features while preserving the original template cue. It also limits the number of variables in the first degraded smoke run.

## Why Motion Blur And Low Resolution First

Motion blur and low resolution are used first because they are common image-quality degradations and were already part of the OTB degradation baseline workflow. They also stress different failure modes: motion blur weakens local detail, while low resolution removes high-frequency target evidence.

## Verification

Run:

```bash
conda run -n ostrack python -m py_compile \
  scripts/verify_training_degradation_pipeline.py \
  external/OSTrack/lib/train/data/degradation.py

conda run -n ostrack python scripts/verify_training_degradation_pipeline.py
```

The verifier checks:

- default/baseline degradation is disabled,
- degraded debug config enables degradation,
- RG-SSB is enabled,
- freeze mode is `rgssb_only`,
- LaSOT is the only train/val dataset,
- synthetic degradation preserves image size,
- synthetic degradation changes the image,
- a LaSOT frame can be loaded and degraded with size preserved.

## Next Tiny Degraded Training Smoke Command

Run manually outside Codex:

```bash
cd external/OSTrack
conda run -n ostrack python lib/train/run_training.py \
  --script ostrack \
  --config vitb_256_mae_ce_32x4_ep300_rgssb_train_lasot_degraded_debug \
  --save_dir output \
  --use_lmdb 0 \
  --use_wandb 0
```

This is real training and was not run during setup.

## Postponed

- clean-degraded feature consistency loss
- response consistency loss
- degradation token
- memory update
- template-guided scan
- response fusion
- full Mamba dependency
- larger datasets or downloaded data
