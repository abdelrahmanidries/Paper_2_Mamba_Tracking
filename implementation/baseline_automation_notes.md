# Baseline Automation Notes

## Purpose

These scripts automate the manual OSTrack OTB sanity workflow already used for clean Car1 and degraded Car1 checks. They do not modify OSTrack model code, OSTrack source files, training code, paper reports, or dataset downloads.

## Scripts

- `scripts/create_degraded_otb_sequence.py` creates one OTB-style evaluation root for one sequence and one degradation. It copies `groundtruth_rect.txt`, preserves frame names and image sizes, and writes per-frame metadata to `metadata.jsonl`.
- `scripts/run_ostrack_otb_eval.py` temporarily points `external/OSTrack/data/otb` to the requested clean or degraded OTB root, runs OSTrack on one sequence, copies `Car1.txt` and `Car1_time.txt` into `outputs/ostrack_runs/...`, computes metrics with `scripts/evaluate_tracking_result.py`, appends one row to `experiments/baseline_results.csv`, and restores the OTB symlink in a `finally` block.

## Clean Car1

```bash
python scripts/run_ostrack_otb_eval.py \
  --clean_otb_root /media/abdel/4484139E5D690B76/otb \
  --eval_otb_root /media/abdel/4484139E5D690B76/otb \
  --sequence Car1 \
  --degradation clean \
  --severity none \
  --seed 0
```

## Degraded Car1

First create the degraded OTB-style root:

```bash
python scripts/create_degraded_otb_sequence.py \
  --clean_otb_root /media/abdel/4484139E5D690B76/otb \
  --sequence Car1 \
  --degradation low_resolution \
  --severity medium \
  --seed 42 \
  --output_root datasets/tiny_sot/degraded
```

Then run OSTrack against that root:

```bash
python scripts/run_ostrack_otb_eval.py \
  --clean_otb_root /media/abdel/4484139E5D690B76/otb \
  --eval_otb_root datasets/tiny_sot/degraded/otb_Car1_low_resolution_medium \
  --sequence Car1 \
  --degradation low_resolution \
  --severity medium \
  --seed 42
```

## Adding Another Degradation

Use a degradation name supported by `src/degradations/protocols.py`: `motion_blur`, `defocus_blur`, `gaussian_noise`, `sensor_noise`, `low_resolution`, `jpeg_compression`, `low_light`, or `mixed`. Use one of `mild`, `medium`, or `severe` for severity.

## Manual Symlink Restore

If needed, restore OSTrack's OTB symlink manually:

```bash
ln -sfn /media/abdel/4484139E5D690B76/otb external/OSTrack/data/otb
```

Check it with:

```bash
readlink external/OSTrack/data/otb
```

## Do Not Commit

- `outputs/`
- generated frames under `datasets/tiny_sot/degraded/`
- `external/OSTrack`
