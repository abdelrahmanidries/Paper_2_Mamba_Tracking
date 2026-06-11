# RG-SSB Experiment Cycle Runner

## Why this runner was created

The RG-SSB experiments now require repeated local cycles: optional OSTrack
training, checkpoint verification, clean OTB evaluation, degraded OTB generation,
degraded evaluation, CSV inspection, and failure logging. Doing that manually is
slow and easy to make inconsistent across lambda/config sweeps.

## How it speeds up the workflow

The runner converts a cycle JSON into the same existing commands every time. It
prints or executes the training command, derives the expected checkpoint from the
OSTrack YAML `TEST.EPOCH`, evaluates the configured sequence/degradation grid,
and prints the final rows already written by `scripts/run_ostrack_otb_eval.py`.

## What it automates

- Path validation for the project, OSTrack root, OSTrack YAML, clean OTB root,
  base checkpoint, and checkpoint output area.
- Optional local OSTrack training through `lib/train/run_training.py`.
- Expected checkpoint verification before evaluation.
- Degraded OTB root creation through `scripts/create_degraded_otb_sequence.py`.
- Clean and degraded evaluation through `scripts/run_ostrack_otb_eval.py`.
- Per-cycle run logs under `outputs/experiment_cycle_logs/`.
- Per-cycle failure records under
  `outputs/experiment_cycle_logs/<cycle_name>_failures.jsonl`.
- Final CSV row inspection for the configured runs.

## What it does not automate

- It does not create a new model architecture.
- It does not edit `external/OSTrack/`.
- It does not modify datasets directly; degraded roots are created only through
  the existing degradation script.
- It does not compute or invent tracking metrics.
- It does not delete checkpoints, outputs, datasets, or CSV rows.
- It does not commit anything.

## Dry-run

Use dry-run before every new cycle config:

```bash
python3 scripts/run_rgssb_experiment_cycle.py \
  --cycle_config configs/rgssb_experiment_cycle_local.json \
  --dry_run
```

Dry-run validates paths, verifies the configured checkpoint if evaluation is
enabled, prints the training/evaluation commands, writes a cycle log, and does
not run training or evaluation.

## Eval-only

Use eval-only when the checkpoint already exists:

```bash
python3 scripts/run_rgssb_experiment_cycle.py \
  --cycle_config configs/rgssb_experiment_cycle_local.json \
  --eval_only
```

This skips training, verifies the checkpoint, creates degraded OTB roots as
needed, runs the configured evaluations, and prints matching CSV rows.

## Training + Evaluation

For a training cycle, create a new config with `"train": true` and `"eval": true`,
then run:

```bash
python3 scripts/run_rgssb_experiment_cycle.py \
  --cycle_config configs/<new_cycle_config>.json
```

The training command is executed from `external/OSTrack`:

```bash
conda run -n ostrack python lib/train/run_training.py \
  --script ostrack \
  --config <config_name> \
  --save_dir output \
  --use_lmdb 0 \
  --use_wandb 0
```

## New Lambda or Config Cycle

Create a new JSON file under `configs/` and change:

- `cycle_name` to a unique short run name.
- `config_name` to the exact OSTrack YAML basename.
- `train` depending on whether training should run.
- `eval` depending on whether evaluation should run.
- `conditions` or `sequences` only when the experiment protocol changes.

Keep config names unique so checkpoints and CSV rows remain traceable.

## What Not to Commit

Do not commit:

- `external/OSTrack/`
- `external/OSTrack/output/`
- `outputs/`
- `datasets/`
- `*.pth.tar`

Commit only reviewed source/config/documentation changes and final result
summaries that are meant to be versioned.

## Inspect Final CSV Rows

The runner prints matching rows from:

```text
experiments/baseline_results.csv
```

To inspect manually:

```bash
python3 - <<'PY'
import csv
config = "vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_degraded_3000_featcons_debug"
with open("experiments/baseline_results.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        if row["config"] == config:
            print(row)
PY
```

## Quality Controls

- Unique config names keep checkpoints and CSV rows tied to one experiment.
- Checkpoint verification prevents accidental evaluation of missing or wrong
  training outputs.
- CSV logging stays centralized in `scripts/run_ostrack_otb_eval.py`.
- Dry-run support exposes the exact commands before expensive execution.
- Git commits should happen only after reviewing generated results and notes.
- No invented metrics are allowed; metrics must come from the evaluation script.
