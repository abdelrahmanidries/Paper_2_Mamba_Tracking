# Broader OTB Evaluation Plan For HPC Lambda 0.02

## Why This Evaluation Is Needed

The HPC lambda `0.02` RG-SSB + head checkpoint improved over the original
OSTrack baseline on the initial three-sequence average, but it did not beat the
best local lambda `0.02` setup overall. Before changing the training objective or
architecture again, the next step is to test whether the HPC checkpoint
generalizes across more OTB sequences.

## Selected Sequences

Selected broader set:

- `Car1`
- `David2`
- `Coke`
- `Walking`
- `Walking2`
- `FaceOcc1`
- `Dog1`
- `Deer`
- `Football`
- `BlurBody`
- `BlurCar2`
- `BlurFace`
- `Box`

The set keeps the original three sequences and adds ten more valid candidate OTB
sequences. Local inspection found matching image-frame and ground-truth counts
for every selected sequence.

## Configs Created

- Baseline OSTrack:
  `configs/baseline_degradation_suite_otb_broader_ostrack.json`
- HPC RG-SSB lambda `0.02`:
  `configs/rgssb_experiment_cycle_hpc_featcons_lam002_otb_broader.json`

Both configs use four conditions:

- clean / none / seed `0`
- motion_blur / medium / seed `42`
- low_resolution / medium / seed `42`
- gaussian_noise / medium / seed `42`

Each config plans `13 * 4 = 52` sequence-condition rows.

## Run Baseline Evaluation

Dry-run first:

```bash
python3 scripts/run_baseline_degradation_suite.py \
  --suite_config configs/baseline_degradation_suite_otb_broader_ostrack.json \
  --dry_run \
  --skip_existing
```

Real run:

```bash
python3 scripts/run_baseline_degradation_suite.py \
  --suite_config configs/baseline_degradation_suite_otb_broader_ostrack.json \
  --skip_existing
```

## Run HPC RG-SSB Evaluation

Dry-run first:

```bash
python3 scripts/run_rgssb_experiment_cycle.py \
  --cycle_config configs/rgssb_experiment_cycle_hpc_featcons_lam002_otb_broader.json \
  --dry_run \
  --eval_only
```

Real run:

```bash
python3 scripts/run_rgssb_experiment_cycle.py \
  --cycle_config configs/rgssb_experiment_cycle_hpc_featcons_lam002_otb_broader.json \
  --eval_only
```

## What To Commit

Commit:

- the two broader evaluation configs
- `scripts/verify_broader_otb_eval_configs.py`
- this plan
- later, compact result analysis files after evaluation

## What Not To Commit

Do not commit:

- checkpoints
- `external/OSTrack/output/`
- generated `outputs/`
- generated degraded datasets
- full OTB or LaSOT datasets
- large job logs

## Expected Output Rows

Expected rows per evaluated model:

```text
13 sequences * 4 conditions = 52 rows
```

Expected total after running both baseline and HPC RG-SSB broader configs:

```text
104 rows
```

Some baseline rows for `Car1`, `David2`, and `Coke` already exist and may be
skipped when `--skip_existing` is used.

## Next Analysis Step

After running the broader evaluation, create a broader OTB comparison report
that compares:

- original OSTrack baseline
- local lambda `0.02`
- HPC lambda `0.02`

The report should compute per-sequence, per-condition, per-condition average,
and overall average AUC/Precision@20/center-error changes.
