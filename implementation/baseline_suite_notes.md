# Baseline Degradation Suite Notes

## Purpose

The suite runner batches the Car1 OSTrack clean/degraded baseline checks so we do not manually run one degradation at a time. It keeps the existing single-run scripts as the execution path, so metric calculation, result CSV appends, and OTB symlink restoration remain in `scripts/run_ostrack_otb_eval.py`.

## Why This Speeds Up Baselines

The runner reads one JSON config, creates degraded OTB roots only when needed, launches OSTrack evaluation for each setting, skips completed rows by default, and records per-run failures in `experiments/baseline_suite_failures.jsonl` without stopping the full suite.

## Why Car1 First

Car1 is the initial proof-of-concept sequence because the clean baseline has matching frame and ground-truth counts and produced a usable sanity-check result. This keeps the first degradation suite small enough to inspect before expanding to harder OTB sequences.

## Included Degradations

- clean, severity `none`, seed `0`
- motion_blur, severity `medium`, seed `42`
- low_resolution, severity `medium`, seed `42`
- jpeg_compression, severity `medium`, seed `42`
- gaussian_noise, severity `medium`, seed `42`

## Postponed Degradations

Defocus blur, sensor noise, low light, mixed degradation, additional severities, additional seeds, and additional OTB sequences are postponed until the Car1 medium-severity baseline table is verified.

## Dry Run

```bash
python3 scripts/run_baseline_degradation_suite.py \
  --suite_config configs/baseline_degradation_suite_car1.json \
  --dry_run
```

By default, existing rows in `experiments/baseline_results.csv` are skipped. Use `--no_skip_existing` only when intentionally regenerating and appending duplicate baseline rows.

## Real Suite

Run this outside the Codex sandbox so CUDA is visible to OSTrack:

```bash
python3 scripts/run_baseline_degradation_suite.py \
  --suite_config configs/baseline_degradation_suite_car1.json
```

For a cautious first real run:

```bash
python3 scripts/run_baseline_degradation_suite.py \
  --suite_config configs/baseline_degradation_suite_car1.json \
  --max_runs 1
```

## Inspect Results

```bash
column -s, -t experiments/baseline_results.csv
tail -n 20 experiments/baseline_suite_failures.jsonl
find outputs/ostrack_runs/Car1 -maxdepth 2 -type f | sort
```

## Do Not Commit

- `outputs/`
- generated frames under `datasets/tiny_sot/degraded/`
- `external/OSTrack`
- local failure logs unless they are intentionally summarized elsewhere
