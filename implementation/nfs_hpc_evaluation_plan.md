# NFS HPC Evaluation Plan

## Why NFS Is Next

The broader OTB result was positive for the HPC RG-SSB + head
feature-consistency lambda `0.02` checkpoint, while the selected UAV123 subset
was mixed and slightly negative overall. NFS is the next benchmark because it
tests high-frame-rate tracking behavior and provides another cross-benchmark
check before changing architecture or training.

## OSTrack NFS Support

- OSTrack dataset name: `nfs`
- Loader: `external/OSTrack/lib/test/evaluation/nfsdataset.py`
- Root path source: `settings.nfs_path` in
  `external/OSTrack/lib/test/evaluation/local.py`
- Expected extracted root layout:
  - `sequences/<sequence_folder>/<frame>.jpg`
  - `anno/nfs_<sequence_folder>.txt`
- Annotation delimiter: tab
- OSTrack constructs the full NFS sequence list before selecting one sequence in
  `tracking/test.py`, so degraded roots should preserve a complete NFS-style
  root. The project-side degradation script mirrors non-target sequence folders
  and replaces only the selected target sequence folder.

## Selected Sequences

Selected NFS sequences:

- `nfs_Gymnastics`
- `nfs_basketball_player`
- `nfs_car`
- `nfs_dog`
- `nfs_running`
- `nfs_bottle`
- `nfs_bird_2`
- `nfs_walking`

These sequences were selected from OSTrack's NFS metadata to cover people,
vehicles, animals, and varied motion. The local NFS path currently appears to
contain raw per-sequence zip files rather than the extracted OSTrack layout, so
frame/annotation checks should be rerun after extraction or on HPC.

## Dataset Paths

- Local default: `/media/abdel/4484139E5D690B76/nfs`
- HPC default: `/speed-scratch/a_idrais/nfs`

Before real evaluation, ensure the selected path has the extracted OSTrack
layout:

```text
<nfs_root>/sequences/
<nfs_root>/anno/
```

Edit `clean_nfs_root` in the suite configs before running on HPC if needed.

## Scripts Created

- `scripts/inspect_nfs_sequences.py`
- `scripts/create_degraded_nfs_sequence.py`
- `scripts/run_ostrack_nfs_eval.py`
- `scripts/run_nfs_degradation_suite.py`
- `scripts/verify_nfs_eval_setup.py`

## Configs Created

- `configs/nfs_eval_suite_ostrack.json`
- `configs/nfs_eval_suite_hpc_rgssb_featcons_lam002.json`

Each config plans:

```text
8 sequences * 4 conditions = 32 rows
```

Conditions:

- clean / none / seed `0`
- motion_blur / medium / seed `42`
- low_resolution / medium / seed `42`
- gaussian_noise / medium / seed `42`

## Run Baseline NFS Evaluation

Dry-run first:

```bash
python3 scripts/run_nfs_degradation_suite.py \
  --suite_config configs/nfs_eval_suite_ostrack.json \
  --dry_run \
  --skip_existing
```

Real run:

```bash
python3 scripts/run_nfs_degradation_suite.py \
  --suite_config configs/nfs_eval_suite_ostrack.json \
  --skip_existing
```

## Run HPC RG-SSB NFS Evaluation

Dry-run first:

```bash
python3 scripts/run_nfs_degradation_suite.py \
  --suite_config configs/nfs_eval_suite_hpc_rgssb_featcons_lam002.json \
  --dry_run \
  --skip_existing
```

Real run:

```bash
python3 scripts/run_nfs_degradation_suite.py \
  --suite_config configs/nfs_eval_suite_hpc_rgssb_featcons_lam002.json \
  --skip_existing
```

## What To Commit

- NFS helper scripts
- NFS evaluation configs
- this plan
- later, compact NFS result analysis files after evaluation

## What Not To Commit

- checkpoints
- `external/OSTrack/output/`
- generated `outputs/`
- generated degraded NFS roots
- full NFS dataset or extracted frames
- raw per-sequence NFS zip files
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

After running both NFS suites, create an NFS comparison report that compares:

- original OSTrack baseline
- HPC RG-SSB lambda `0.02`

Compute per-sequence, per-condition, and overall AUC/Precision@20/center-error
changes. Do not invent missing results.
