# UAV123 HPC Evaluation Plan

## Why UAV123 Is Next

The broader OTB analysis shows that the HPC RG-SSB + head feature-consistency
lambda `0.02` checkpoint improves over the original OSTrack baseline on average
across 13 OTB sequences and four conditions. UAV123 is the next benchmark
because it tests aerial tracking behavior beyond OTB without changing the model
architecture or training objective.

## OSTrack UAV123 Support

- OSTrack dataset name: `uav`
- Loader: `external/OSTrack/lib/test/evaluation/uavdataset.py`
- Root path source: `settings.uav_path` in
  `external/OSTrack/lib/test/evaluation/local.py`
- Expected root layout:
  - `data_seq/UAV123/<sequence_folder>/<frame>.jpg`
  - `anno/UAV123/<sequence_annotation>.txt`
- Frame names are zero-padded according to each sequence metadata entry.
- OSTrack constructs the full UAV123 sequence list before selecting one sequence
  in `tracking/test.py`, so degraded roots should preserve a complete UAV123
  layout. The project-side degradation script mirrors non-target sequence
  folders and replaces only the selected target sequence folder.

## Selected Sequences

Selected non-overlapping UAV123 sequence folders:

- `uav_car10`
- `uav_person1`
- `uav_truck1`
- `uav_bike1`
- `uav_boat1`
- `uav_building1`
- `uav_person3`
- `uav_car11`

These were selected because the local UAV123 root contains the expected image
folders, first/last frames, and annotation files with matching frame counts.
They also avoid split-sequence folders such as `uav_car1_1`/`uav_car1_2`.

## Dataset Paths

- Local default: `/media/abdel/windows/UAV123`
- HPC default: `/speed-scratch/a_idrais/UAV123`

Edit `clean_uav_root` in the suite configs before running on HPC.

## Scripts Created

- `scripts/inspect_uav123_sequences.py`
- `scripts/create_degraded_uav123_sequence.py`
- `scripts/run_ostrack_uav123_eval.py`
- `scripts/run_uav123_degradation_suite.py`
- `scripts/verify_uav123_eval_setup.py`

## Configs Created

- `configs/uav123_eval_suite_ostrack.json`
- `configs/uav123_eval_suite_hpc_rgssb_featcons_lam002.json`

Each config plans:

```text
8 sequences * 4 conditions = 32 rows
```

Conditions:

- clean / none / seed `0`
- motion_blur / medium / seed `42`
- low_resolution / medium / seed `42`
- gaussian_noise / medium / seed `42`

## Run Baseline UAV123 Evaluation

Dry-run first:

```bash
python3 scripts/run_uav123_degradation_suite.py \
  --suite_config configs/uav123_eval_suite_ostrack.json \
  --dry_run \
  --skip_existing
```

Real run:

```bash
python3 scripts/run_uav123_degradation_suite.py \
  --suite_config configs/uav123_eval_suite_ostrack.json \
  --skip_existing
```

## Run HPC RG-SSB UAV123 Evaluation

Dry-run first:

```bash
python3 scripts/run_uav123_degradation_suite.py \
  --suite_config configs/uav123_eval_suite_hpc_rgssb_featcons_lam002.json \
  --dry_run \
  --skip_existing
```

Real run:

```bash
python3 scripts/run_uav123_degradation_suite.py \
  --suite_config configs/uav123_eval_suite_hpc_rgssb_featcons_lam002.json \
  --skip_existing
```

## What To Commit

- UAV123 helper scripts
- UAV123 evaluation configs
- this plan
- later, compact UAV123 result analysis files after evaluation

## What Not To Commit

- checkpoints
- `external/OSTrack/output/`
- generated `outputs/`
- generated degraded UAV123 roots
- full UAV123 dataset
- large HPC logs

## Expected Output Rows

Expected rows per model:

```text
32 rows
```

Expected total after running baseline and HPC RG-SSB:

```text
64 rows
```

Rows are appended to `experiments/baseline_results.csv` with the existing key:

```text
tracker, config, sequence, degradation, severity, seed
```

## Next Analysis Step

After running both UAV123 suites, create a UAV123 comparison report that compares:

- original OSTrack baseline
- HPC RG-SSB lambda `0.02`

Compute per-sequence, per-condition, and overall AUC/Precision@20/center-error
changes. Do not invent missing results.
