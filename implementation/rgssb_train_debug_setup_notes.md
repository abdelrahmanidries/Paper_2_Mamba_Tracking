# RG-SSB Train Debug Setup Notes

Date: 2026-06-10

## What Changed

This setup adds the smallest RG-SSB-only training/debug path for OSTrack. It does not run training and does not modify the original baseline config.

External OSTrack files modified or created:

- `external/OSTrack/experiments/ostrack/vitb_256_mae_ce_32x4_ep300_rgssb_train_debug.yaml`
- `external/OSTrack/experiments/ostrack/vitb_256_mae_ce_32x4_ep300_rgssb_train_lasot_debug.yaml`
- `external/OSTrack/lib/config/ostrack/config.py`
- `external/OSTrack/lib/train/freeze.py`
- `external/OSTrack/lib/train/base_functions.py`
- `external/OSTrack/lib/models/ostrack/ostrack.py`

Main project files created or modified:

- `scripts/verify_rgssb_trainable_params.py`
- `scripts/verify_lasot_rgssb_train_debug.py`
- `implementation/rgssb_train_debug_setup_notes.md`
- `implementation/patches/ostrack_rgssb_integration.patch`

## Debug Config

Config name:

`vitb_256_mae_ce_32x4_ep300_rgssb_train_debug`

Path:

`external/OSTrack/experiments/ostrack/vitb_256_mae_ce_32x4_ep300_rgssb_train_debug.yaml`

This config is debug-only. It keeps OSTrack template/search sizes unchanged and uses:

- `MODEL.RGSSB.ENABLE: True`
- `MODEL.PRETRAIN_FILE: output/checkpoints/train/ostrack/vitb_256_mae_ce_32x4_ep300/OSTrack_ep0300.pth.tar`
- `TRAIN.BATCH_SIZE: 1`
- `TRAIN.NUM_WORKER: 2`
- `TRAIN.EPOCH: 1`
- `TRAIN.PRINT_INTERVAL: 5`
- `TRAIN.FREEZE_MODE: "rgssb_only"`
- `DATA.TRAIN.SAMPLE_PER_EPOCH: 100`
- `DATA.VAL.SAMPLE_PER_EPOCH: 20`

## LaSOT-Only Debug Config

Config name:

`vitb_256_mae_ce_32x4_ep300_rgssb_train_lasot_debug`

Path:

`external/OSTrack/experiments/ostrack/vitb_256_mae_ce_32x4_ep300_rgssb_train_lasot_debug.yaml`

This is the preferred first smoke-training config because local LaSOT was verified manually:

- `external/OSTrack/data/lasot` points to `/home/abdel/Desktop/lasot`
- `Lasot(root="data/lasot", split="train")` creates 1120 sequences
- sample frames load successfully

The LaSOT-only config uses:

- `DATA.TRAIN.DATASETS_NAME: ["LASOT"]`
- `DATA.TRAIN.DATASETS_RATIO: [1]`
- `DATA.TRAIN.SAMPLE_PER_EPOCH: 100`
- `DATA.VAL.DATASETS_NAME: ["LASOT"]`
- `DATA.VAL.DATASETS_RATIO: [1]`
- `DATA.VAL.SAMPLE_PER_EPOCH: 20`
- `MODEL.RGSSB.ENABLE: True`
- `TRAIN.FREEZE_MODE: "rgssb_only"`
- `TRAIN.BATCH_SIZE: 1`
- `TRAIN.NUM_WORKER: 2`
- `TRAIN.EPOCH: 1`

GOT-10k, COCO, and TrackingNet are postponed because their local train/val paths have not been verified for this debug run. OTB is also postponed for training because it is not part of the inspected OSTrack training dataset registry.

## Freeze Mode Behavior

Default config behavior is preserved with:

`TRAIN.FREEZE_MODE = "none"`

The debug config uses:

`TRAIN.FREEZE_MODE = "rgssb_only"`

In `rgssb_only` mode:

- all parameters are frozen first by name logic,
- only parameters whose name contains `rgssb` remain trainable,
- the optimizer receives only parameters with `requires_grad=True`,
- trainable and frozen parameter counts are printed,
- a clear error is raised if no RG-SSB trainable parameters are found.

## Why RG-SSB-Only First

RG-SSB-only training is the safest first route because it tests whether the new block can receive gradients and learn without changing the pretrained OSTrack backbone or tracking head. This reduces the risk of clean tracking collapse and keeps memory pressure low on the GTX 1080.

## Checkpoint Loading

The train debug config initializes from the original OSTrack checkpoint. Because that checkpoint does not contain RG-SSB weights, RG-SSB-enabled training/debug uses `strict=False` and prints missing/unexpected keys. Missing `rgssb.*` keys are expected and are randomly initialized.

The baseline config remains disabled by default and is not modified.

## Verification

Run:

```bash
conda run -n ostrack python -m py_compile scripts/verify_rgssb_trainable_params.py
conda run -n ostrack python scripts/verify_rgssb_trainable_params.py
conda run -n ostrack python -m py_compile scripts/verify_lasot_rgssb_train_debug.py
conda run -n ostrack python scripts/verify_lasot_rgssb_train_debug.py
```

Expected result:

- `MODEL.RGSSB.ENABLE: True`
- `TRAIN.FREEZE_MODE: rgssb_only`
- only `rgssb.*` parameters are trainable
- trainable parameters: `2079936`
- frozen parameters: `92518533`

## First Tiny Training Smoke Command

Run this manually outside Codex when ready:

```bash
cd external/OSTrack
conda run -n ostrack python lib/train/run_training.py \
  --script ostrack \
  --config vitb_256_mae_ce_32x4_ep300_rgssb_train_lasot_debug \
  --save_dir output \
  --use_lmdb 0 \
  --use_wandb 0
```

This command uses the LaSOT-only debug config's 1 epoch and 100 training samples. It is still real training, so it was not run during setup.

## Postponed

The following are intentionally not included yet:

- feature consistency loss
- response consistency loss
- degradation token
- template-guided scan
- memory update
- response fusion
- full Mamba dependency
- full fine-tuning
- dataset downloads
- paper report changes
