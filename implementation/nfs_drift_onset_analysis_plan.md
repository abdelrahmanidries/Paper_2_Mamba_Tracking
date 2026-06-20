# NFS Drift-Onset Analysis Plan

## Purpose

The corrected normalized-NFS analysis shows that the current HPC RG-SSB lambda 0.02 checkpoint is slightly negative on the expanded NFS subset, with the largest drops concentrated in a small set of sequence-condition pairs. This plan adds an offline temporal diagnostic layer to identify whether those failures begin as RG-SSB-specific divergence, shared tracker failure, sudden jumps, scale instability, gradual drift, or temporary failure with recovery.

This analysis uses only existing corrected predictions, corrected aligned XYWH ground truth, and generated per-frame diagnostics. It does not run tracking, training, or benchmark evaluation.

## Inputs

- Failure case config: `configs/nfs_failure_cases_to_inspect.json`
- Corrected NFS comparison: `experiments/rgssb_hpc_nfs_expanded32_comparison.csv`
- Logged result rows: `experiments/baseline_results.csv`
- Optional existing diagnostics: `outputs/failure_inspection_corrected_nfs/`
- Shared corrected NFS annotation logic: `src/evaluation/nfs_annotations.py`

The NFS ground truth must remain the normalized aligned canonical XYWH version. Older diagnostics and overlays created before the XYXY/alignment fix are superseded.

## Failure Cases

The current corrected failure config contains the top corrected expanded-NFS drops:

- `nfs_bowling_1`, low_resolution medium
- `nfs_Gymnastics`, low_resolution medium
- `nfs_Gymnastics`, gaussian_noise medium
- `nfs_basketball_player_2`, gaussian_noise medium
- `nfs_parkour`, low_resolution medium
- `nfs_motorcross`, low_resolution medium
- `nfs_running`, motion_blur medium
- `nfs_person_scooter`, motion_blur medium
- `nfs_footbal_skill`, low_resolution medium
- `nfs_car_rc_rolling`, clean none

## Drift Events

`scripts/analyze_nfs_drift_onset.py` detects:

- First RG-SSB-specific sustained divergence: baseline IoU >= 0.4 and RG-SSB IoU <= 0.2 for at least 5 consecutive frames.
- First shared failure: both baseline and RG-SSB IoU <= 0.2 for at least 5 consecutive frames.
- First large RG-SSB center jump: adjacent RG-SSB prediction center displacement >= 100 px.
- First severe scale change: adjacent predicted area ratio >= 2.0 or <= 0.5.
- Recovery: RG-SSB IoU returns to >= 0.4 for at least 5 consecutive frames after a detected failure.

Each case is assigned one failure classification:

- RG-SSB-specific distractor switch
- shared tracker failure
- gradual drift
- sudden center jump
- scale collapse or expansion
- temporary failure with recovery
- ambiguous

## Outputs

For each case:

- `outputs/failure_inspection_corrected_nfs/<sequence>/<condition>/drift_onset_summary.json`
- `outputs/failure_inspection_corrected_nfs/<sequence>/<condition>/drift_events.csv`
- `outputs/failure_inspection_corrected_nfs/<sequence>/<condition>/drift_onset_contact_sheet.jpg`, when images are locally available
- `outputs/failure_inspection_corrected_nfs/<sequence>/<condition>/drift_window_overlays/`, when images are locally available

Combined table:

- `experiments/nfs_corrected_drift_onset_analysis.csv`

The contact sheet covers up to 10 frames before through 10 frames after the first sustained divergence. If no sustained divergence is found, it centers on the first detected failure event.

## Commands

Check-only validation:

```bash
python3 scripts/analyze_nfs_drift_onset.py \
  --config configs/nfs_failure_cases_to_inspect.json \
  --check_only
```

Run full CSV and overlay analysis on Speed:

```bash
cd /speed-scratch/a_idrais/Paper_2_Mamba_Tracking
python3 scripts/analyze_nfs_drift_onset.py \
  --config configs/nfs_failure_cases_to_inspect.json \
  --diagnostics_root outputs/failure_inspection_corrected_nfs \
  --output_root outputs/failure_inspection_corrected_nfs
```

Run one case:

```bash
python3 scripts/analyze_nfs_drift_onset.py \
  --config configs/nfs_failure_cases_to_inspect.json \
  --case_index 0
```

## Interpretation

If most cases are RG-SSB-specific distractor switches or gradual drift, the next refinement should focus on training constraints that preserve target identity under degraded search conditions. If failures are dominated by sudden center jumps or scale collapse, the box head or localization stability should be inspected before adding architectural modules. If most failures are shared, the issue is likely benchmark difficulty or degradation severity rather than an RG-SSB-specific regression.

## What Not To Commit

- `outputs/failure_inspection_corrected_nfs/`
- generated contact sheets and frame overlays
- checkpoints
- degraded datasets
- `external/OSTrack/output/`

## Recommended Next Decision

Use the drift classifications to decide whether to keep training unchanged and expand evaluation, tune the training loss for localization stability, or inspect target-preservation losses. Do not add degradation tokens, memory modules, response fusion, or template-guided scan until the failure onset patterns are understood.
