# Baseline Automation Notes

## Purpose

These scripts automate the manual OSTrack OTB sanity workflow already used for clean Car1 and degraded Car1 checks. They do not modify OSTrack model code, OSTrack source files, training code, paper reports, or dataset downloads.

## Scripts

- `scripts/create_degraded_otb_sequence.py` creates one complete OTB-style evaluation root for one sequence and one degradation. It symlinks every non-target clean OTB sequence into the generated root, replaces the target sequence with degraded frames, copies `groundtruth_rect.txt`, preserves frame names and image sizes, and writes per-frame metadata to `<sequence>/metadata.jsonl`.
- `scripts/run_ostrack_otb_eval.py` temporarily points `external/OSTrack/data/otb` to the requested clean or degraded OTB root, runs OSTrack on one sequence, copies result files into `outputs/ostrack_runs/<tracker>/<config>/<sequence>/<degradation>_<severity>_seed<seed>/`, computes metrics with `scripts/evaluate_tracking_result.py`, appends one row to `experiments/baseline_results.csv`, and restores the OTB symlink in a `finally` block.

## Output Path Safety

Result backup directories include both tracker and config names. This avoids collisions between the original OSTrack baseline config and debug configs such as `vitb_256_mae_ce_32x4_ep300_rgssb_debug`, which can otherwise share the same sequence/degradation/severity/seed labels.

## CSV Duplicate Protection

Each result row is uniquely identified by:

```text
tracker, config, sequence, degradation, severity, seed
```

`scripts/run_ostrack_otb_eval.py` skips an existing row by default before launching OSTrack. This prevents accidental duplicate rows and avoids unnecessary GPU runs.

Explicit skip:

```bash
python3 scripts/run_ostrack_otb_eval.py \
  --clean_otb_root /media/abdel/4484139E5D690B76/otb \
  --eval_otb_root /media/abdel/4484139E5D690B76/otb \
  --sequence Car1 \
  --degradation clean \
  --severity none \
  --seed 0 \
  --skip_existing
```

Overwrite an existing row after rerunning the evaluation:

```bash
python3 scripts/run_ostrack_otb_eval.py \
  --clean_otb_root /media/abdel/4484139E5D690B76/otb \
  --eval_otb_root /media/abdel/4484139E5D690B76/otb \
  --sequence Car1 \
  --config vitb_256_mae_ce_32x4_ep300_rgssb_debug \
  --degradation clean \
  --severity none \
  --seed 0 \
  --overwrite_existing
```

If a matching row exists, the script will either skip it or replace it. It will not append a duplicate matching row.

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
