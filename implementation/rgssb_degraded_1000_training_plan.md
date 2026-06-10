# RG-SSB Degraded 1000-Sample Training Plan

Date: 2026-06-10

## Purpose

The first degradation-aware RG-SSB smoke run used only 100 LaSOT training samples. It worked technically, but the Car1 analysis showed mixed results: Gaussian noise improved, motion blur and JPEG compression were roughly similar by AUC, low resolution worsened, and clean performance dropped slightly.

This plan creates the next local debug step: 1000 degraded LaSOT samples while keeping the architecture and freezing strategy unchanged.

## Config

New config:

`external/OSTrack/experiments/ostrack/vitb_256_mae_ce_32x4_ep300_rgssb_train_lasot_degraded_1000_debug.yaml`

Key settings:

- `MODEL.RGSSB.ENABLE: True`
- `TRAIN.FREEZE_MODE: "rgssb_only"`
- `DATA.TRAIN.DATASETS_NAME: ["LASOT"]`
- `DATA.TRAIN.SAMPLE_PER_EPOCH: 1000`
- `DATA.VAL.DATASETS_NAME: ["LASOT"]`
- `DATA.VAL.SAMPLE_PER_EPOCH: 100`
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

Template/search sizes remain unchanged:

- template size: 128
- search size: 256

## Why Increase From 100 To 1000 Samples

The 100-sample run was a smoke test. It verified the pipeline but likely provided too little degraded data for RG-SSB to learn stable behavior. Increasing to 1000 samples is the smallest useful scale-up before changing losses or architecture.

## Why Keep RG-SSB-Only Freezing

Only RG-SSB remains trainable to isolate whether the inserted block can learn useful degradation handling. Training the head or backbone would add another variable and increase the risk of clean tracking collapse on a local debug run.

## Why These Degradations

- `motion_blur`: Car1 baseline is weak here, and the first degradation-aware run was roughly similar by AUC.
- `low_resolution`: current result worsened, so it needs more exposure before adding low-resolution-specific supervision.
- `gaussian_noise`: current result improved, so it is worth retaining as a positive signal.

JPEG compression is postponed in this next run because it was roughly flat and the goal is to keep the degradation set focused.

## Why Search Only

`search_only` keeps the template clean and degrades the search crop. This keeps the experiment small and tests whether RG-SSB can improve search features under degradation without changing the template cue.

## Expected Benefits

- More stable RG-SSB weight updates than the 100-sample smoke run.
- Better evidence about whether the current block can help without new losses.
- Potential improvement on Gaussian noise and motion blur.
- Better diagnosis of whether low-resolution failure is data-limited or requires a different loss/module.

## Risks

- Clean performance may drop further.
- Low-resolution may still worsen without dedicated restoration supervision.
- RG-SSB-only training may be too limited if the head cannot adapt to changed features.
- Local GTX 1080 runtime will be longer than the 100-sample smoke run.
- Results are still single-sequence and single-seed debug evidence.

## Training Command

Run outside Codex:

```bash
cd external/OSTrack
conda run -n ostrack python lib/train/run_training.py \
  --script ostrack \
  --config vitb_256_mae_ce_32x4_ep300_rgssb_train_lasot_degraded_1000_debug \
  --save_dir output \
  --use_lmdb 0 \
  --use_wandb 0
```

## Evaluation Commands After Training

Clean Car1:

```bash
python3 scripts/run_ostrack_otb_eval.py \
  --clean_otb_root /media/abdel/4484139E5D690B76/otb \
  --eval_otb_root /media/abdel/4484139E5D690B76/otb \
  --sequence Car1 \
  --config vitb_256_mae_ce_32x4_ep300_rgssb_train_lasot_degraded_1000_debug \
  --degradation clean \
  --severity none \
  --seed 0 \
  --overwrite_existing
```

Motion blur, low resolution, and Gaussian noise can be evaluated through the existing degradation-suite flow or by running `scripts/run_ostrack_otb_eval.py` against the corresponding generated degraded OTB roots.

## Before Moving To HPC

Check:

- Training completes without NaNs or OOM.
- Checkpoint `OSTrack_ep0001.pth.tar` is saved.
- Clean Car1 does not collapse.
- Motion blur and Gaussian noise improve or stay stable.
- Low resolution does not degrade further.
- `experiments/baseline_results.csv` contains non-duplicated rows for the 1000-sample config.

If these checks are not met, revise the training strategy before adding architecture modules or scaling to HPC.

## Postponed

- degradation token
- template-guided scan
- memory update
- response fusion
- feature consistency loss
- response consistency loss
- full HPC training
- all datasets
