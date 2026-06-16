# NFS Failure-Case Inspection Plan

## Why this inspection is needed

The expanded 32-sequence NFS analysis shows that the current HPC RG-SSB lambda `0.02` checkpoint is slightly negative overall on NFS. The average AUC change is `-0.010461`, with large sequence-condition drops concentrated in specific cases. Before changing training or architecture, the next step is per-frame inspection using existing result files and aligned NFS ground truth.

This setup does not run training, does not run OSTrack evaluation, and does not modify `external/OSTrack` or datasets.

## Selected failure cases

Cases were selected from `experiments/rgssb_hpc_nfs_expanded32_comparison.csv` by sorting AUC change ascending and taking the top 10 largest drops. Required known failures are included when present.

| rank | sequence | degradation | severity | seed | AUC change |
| ---: | --- | --- | --- | ---: | ---: |
| 1 | nfs_cheetah | low_resolution | medium | 42 | -0.403866 |
| 2 | nfs_walking | gaussian_noise | medium | 42 | -0.284435 |
| 3 | nfs_walking | motion_blur | medium | 42 | -0.165552 |
| 4 | nfs_car_camaro | low_resolution | medium | 42 | -0.080859 |
| 5 | nfs_car_camaro | motion_blur | medium | 42 | -0.078933 |
| 6 | nfs_biker_acrobat | motion_blur | medium | 42 | -0.075263 |
| 7 | nfs_car_camaro | clean | none | 0 | -0.073983 |
| 8 | nfs_running_100_m | motion_blur | medium | 42 | -0.073735 |
| 9 | nfs_parkour | low_resolution | medium | 42 | -0.070502 |
| 10 | nfs_biker_acrobat | low_resolution | medium | 42 | -0.064124 |

The selected cases are stored in `configs/nfs_failure_cases_to_inspect.json`.

## What the inspection script outputs

`scripts/inspect_tracking_failure_case.py` reads existing baseline and HPC RG-SSB result files, aligns NFS ground truth, and writes per-case diagnostics under:

`outputs/failure_inspection/<sequence>/<degradation>_<severity>_seed<seed>/`

For each case it writes:

- `per_frame_diagnostics.csv`
- `bad_frames.csv`
- `summary.json`

The per-frame diagnostics include baseline IoU, RG-SSB IoU, IoU difference, baseline center error, RG-SSB center error, center-error difference, baseline box, RG-SSB box, and ground-truth box.

Bad frames are selected when:

- RG-SSB IoU is lower than baseline IoU by at least `0.2`, or
- RG-SSB center error is worse than baseline by at least `20` pixels, or
- RG-SSB IoU is below `0.1` while baseline IoU is at least `0.3`.

## NFS annotation alignment

NFS raw annotation files can be denser than extracted image frames. The inspection script uses the same aligned annotation logic used by `scripts/run_ostrack_nfs_eval.py`:

- parse OSTrack NFS metadata from `external/OSTrack/lib/test/evaluation/nfsdataset.py`
- compute expected frames from `startFrame + initOmit` through `endFrame`
- load raw annotation rows
- sample raw annotation rows to the expected frame count when raw annotations are denser
- verify prediction line count equals aligned ground-truth count

Do not compare raw annotation line count directly to frame count.

## Commands

Check only:

```bash
python3 scripts/inspect_tracking_failure_case.py \
  --config configs/nfs_failure_cases_to_inspect.json \
  --check_only
```

CSV-only diagnostics for all cases on Speed:

```bash
cd /speed-scratch/a_idrais/Paper_2_Mamba_Tracking
python3 scripts/inspect_tracking_failure_case.py \
  --config configs/nfs_failure_cases_to_inspect.json
```

CSV-only diagnostics for the first case:

```bash
python3 scripts/inspect_tracking_failure_case.py \
  --config configs/nfs_failure_cases_to_inspect.json \
  --case_index 0 \
  --max_visual_frames 0
```

Visual overlay generation for one case:

```bash
python3 scripts/inspect_tracking_failure_case.py \
  --config configs/nfs_failure_cases_to_inspect.json \
  --case_index 0 \
  --save_visuals \
  --max_visual_frames 30
```

## Speed paths

- Project root: `/speed-scratch/a_idrais/Paper_2_Mamba_Tracking`
- NFS root: `/speed-scratch/a_idrais/nfs`
- Degraded root base: `/speed-scratch/a_idrais/Paper_2_Mamba_Tracking/datasets/tiny_sot/degraded`
- Output root: `/speed-scratch/a_idrais/Paper_2_Mamba_Tracking/outputs/failure_inspection`

## What not to commit

- `outputs/failure_inspection/`
- generated visual frames
- degraded datasets
- checkpoints
- `external/OSTrack/output/`

## How to interpret bad-frame CSVs

Start with `summary.json` to identify the number of bad frames and the worst frames by IoU drop and center-error increase. Then inspect `bad_frames.csv` to see whether failures are short bursts, long drifts, or immediate initialization-related errors. Generate visual overlays only for cases where CSV diagnostics indicate meaningful failures.

## Next decision after inspection

If failures are concentrated in a few sequences or short temporal windows, continue qualitative inspection and broaden evaluation before changing the method. If failures are systematic across motion blur, low resolution, or small-object cases, consider a training/data refinement before adding new architecture modules.
