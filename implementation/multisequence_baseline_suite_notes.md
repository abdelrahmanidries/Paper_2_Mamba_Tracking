# Multisequence Baseline Suite Notes

## Purpose

This extends the baseline suite so Day 2 and Day 3 checks can be run from one command. The runner now supports the original single-sequence config and a multi-sequence config with shared degradation settings.

## Why This Speeds Up Day 2 and Day 3

The suite avoids manual degradation/evaluation commands for each sequence and degradation. It creates degraded OTB roots as needed, launches OSTrack through the existing single-run evaluator, appends metrics to `experiments/baseline_results.csv`, skips completed rows by default, and records failures in `experiments/baseline_suite_failures.jsonl`.

## Selected Second Sequence

Selected sequence: `David2`.

Reason: it was the first valid candidate in the requested priority list. Inspection found 537 image frames, 537 ground-truth lines, an existing first image, and matching counts.

## Included Runs

For both `Car1` and `David2`:

- clean, severity `none`, seed `0`
- motion_blur, severity `medium`, seed `42`
- low_resolution, severity `medium`, seed `42`
- jpeg_compression, severity `medium`, seed `42`
- gaussian_noise, severity `medium`, seed `42`

## Dry Run

```bash
python3 scripts/run_baseline_degradation_suite.py \
  --suite_config configs/baseline_degradation_suite_car1_plus_one.json \
  --dry_run \
  --skip_existing
```

## Real Suite

Run outside the Codex sandbox so CUDA is visible to OSTrack:

```bash
python3 scripts/run_baseline_degradation_suite.py \
  --suite_config configs/baseline_degradation_suite_car1_plus_one.json \
  --skip_existing
```

## Inspect Results

```bash
column -s, -t experiments/baseline_results.csv
tail -n 20 experiments/baseline_suite_failures.jsonl
find outputs/ostrack_runs -maxdepth 3 -type f | sort
```

## Do Not Commit

- `outputs/`
- generated frames under `datasets/tiny_sot/degraded/`
- `external/OSTrack/`
