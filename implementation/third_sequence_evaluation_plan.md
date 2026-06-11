# Third Sequence Evaluation Plan

Date: 2026-06-10

## Purpose

The RG-SSB + head result is split across Car1 and David2: Car1 improves broadly, while David2 improves only on motion blur. Before changing training again, add a third OTB sequence to test whether this pattern is sequence-specific or more systematic.

## Candidate Inspection

Clean OTB root:

`/media/abdel/4484139E5D690B76/otb`

| Sequence | Folder | img/ | Frames | GT lines | Counts match | First image | First GT parses | First GT |
|---|---|---|---:|---:|---|---|---|---|
| Coke | yes | yes | 291 | 291 | yes | yes | yes | `298,160,48,80` |
| Walking | yes | yes | 412 | 412 | yes | yes | yes | `692 439 24 79` |
| Walking2 | yes | yes | 500 | 500 | yes | yes | yes | `130 132 31 115` |
| Deer | yes | yes | 71 | 71 | yes | yes | yes | `306,5,95,65` |
| FaceOcc1 | yes | yes | 892 | 892 | yes | yes | yes | `118 69 114 162` |
| Dog1 | yes | yes | 1350 | 1350 | yes | yes | yes | `139,112,51,36` |

## Selected Third Sequence

Selected sequence: `Coke`

Rationale:

- Valid frame and ground-truth counts.
- 291 frames, so it is not extremely short.
- Preferred by the request if valid.
- Different from Car1 and David2, so it adds a new appearance category for robustness sanity testing.
- No structural mismatch was detected.

## Suite Configs

The suite runner supports multiple sequences but one tracker config per suite file, so two configs were created:

- `configs/baseline_degradation_suite_three_sequences_ostrack.json`
- `configs/baseline_degradation_suite_three_sequences_rgssb_head.json`

Both include:

- `Car1`
- `David2`
- `Coke`

Conditions:

- clean, severity none, seed 0
- motion_blur, severity medium, seed 42
- low_resolution, severity medium, seed 42
- gaussian_noise, severity medium, seed 42

## Run Missing Baseline Rows

Run outside Codex:

```bash
python3 scripts/run_baseline_degradation_suite.py \
  --suite_config configs/baseline_degradation_suite_three_sequences_ostrack.json \
  --skip_existing
```

Expected behavior:

- Existing Car1 and David2 baseline rows are skipped.
- Coke baseline rows are generated/evaluated.
- Degraded Coke roots are created under `datasets/tiny_sot/degraded/`.
- Results are appended to `experiments/baseline_results.csv`.

## Run Missing RG-SSB + Head Rows

Run outside Codex:

```bash
python3 scripts/run_baseline_degradation_suite.py \
  --suite_config configs/baseline_degradation_suite_three_sequences_rgssb_head.json \
  --skip_existing
```

Expected behavior:

- Existing Car1 and David2 RG-SSB + head rows are skipped.
- Coke RG-SSB + head rows are generated/evaluated.
- Results are appended to `experiments/baseline_results.csv`.

## Expected Outputs

- `outputs/ostrack_runs/ostrack/vitb_256_mae_ce_32x4_ep300/Coke/...`
- `outputs/ostrack_runs/ostrack/vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_degraded_1000_debug/Coke/...`
- generated degraded OTB roots for Coke under `datasets/tiny_sot/degraded/`
- new Coke rows in `experiments/baseline_results.csv`

## What Not To Commit

- `outputs/`
- `datasets/tiny_sot/degraded/`
- `external/OSTrack/`
- model checkpoints

## Inspect Final Results

After running both suites:

```bash
python3 - <<'PY'
import csv
with open("experiments/baseline_results.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        if row["sequence"] == "Coke":
            print(row["config"], row["degradation"], row["severity"], row["seed"], row["success_auc"], row["precision_20"], row["mean_center_error"])
PY
```

## Next Analysis Step

Create a three-sequence analysis comparing original OSTrack and RG-SSB + head on Car1, David2, and Coke for clean, motion blur, low resolution, and Gaussian noise. Do not make final claims until the third sequence is evaluated.
