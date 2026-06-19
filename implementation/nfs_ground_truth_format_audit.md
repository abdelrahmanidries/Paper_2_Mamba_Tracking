# NFS Ground-Truth Format Audit

## Status

All NFS-derived metrics, comparisons, qualitative overlays, and reports should be treated as **provisional** until the NFS annotation pipeline is corrected and the affected results are regenerated.

## Source-code findings

`external/OSTrack/lib/test/evaluation/nfsdataset.py` defines each sequence with `name`, `path`, `startFrame`, `endFrame`, zero padding `nz`, image extension `ext`, `anno_path`, and `object_class`. It constructs frame paths with:

```text
range(startFrame + initOmit, endFrame + 1)
```

It loads annotations with:

```text
load_text(anno_path, delimiter='\t', dtype=np.float64)
ground_truth_rect[initOmit:, :]
```

The OSTrack loader does **not** convert raw NFS rows from `[track_id, x1, y1, x2, y2, frame, ...]` into `[x, y, width, height]`. Therefore, the authoritative coordinate convention returned in `Sequence.ground_truth_rect` is whatever the configured `anno/nfs_*.txt` files already contain. OSTrack expects those files to be compatible with tracker initialization and evaluation, effectively `[x, y, width, height]` rows with one row per constructed frame.

## Raw annotation findings

The audited local NFS source mode is `zip_raw_nfs`. The script audited `16` frame rows. In those raw rows:

- direct first-four-column `[x, y, width, height]` was numerically plausible for `11` rows, but this interpretation is contradicted by the ten-column raw schema and frame-index column.
- raw NFS columns 1-4 interpreted as `[x1, y1, x2, y2]`, converted to `[x, y, width, height]`, were plausible for `16` rows.
- a frame-index-like numeric column was detected in all rows: `True`. For dense raw NFS rows this column matches the sampled raw annotation line, not necessarily the constructed 30fps frame filename.

This supports the conclusion that the raw annotation rows in the audited NFS source are not directly usable as `[x, y, width, height]`.

## Frame alignment

The project-side NFS scripts currently add a custom sampler when raw annotation rows are denser than frame images. The sampler computes a stride from raw annotation count to expected frame count. This handles row-count mismatch, but it does not fix the coordinate-column format. If raw rows are still ten-column NFS rows, sampling alone is insufficient.

OSTrack's own `nfsdataset.py` does not perform this sampler. It simply returns `ground_truth_rect[initOmit:, :]`. If an extracted NFS root contains raw ten-column annotation files, OSTrack tracking may have been initialized from incorrect boxes as well.

## Existing predictions

Existing prediction files were not available in this workspace, so prediction contents were not audited locally.

Tracker prediction files, when present, are outputs produced for the evaluated frame sequence. Their row count can remain valid, but their semantic validity depends on whether the tracker was initialized with correct ground truth. If OSTrack was run against raw ten-column annotation files, NFS tracking should be rerun after creating proper OSTrack-compatible NFS annotations. If OSTrack was run against already converted four-column annotations, only metrics and overlays need regeneration with the same converted convention.

## Current script validity

- `scripts/evaluate_tracking_result.py` assumes `[x, y, width, height]`.
- `scripts/run_ostrack_nfs_eval.py` uses `load_boxes`, which keeps only the first four numeric fields and assumes `[x, y, width, height]`.
- `scripts/inspect_tracking_failure_case.py` uses the same assumption.
- `scripts/inspect_nfs_sequences.py` and `scripts/create_degraded_nfs_sequence.py` check aligned row counts but do not verify coordinate-column format.

Given the audited raw rows, these scripts parse raw NFS annotations incorrectly unless the configured `anno/` files have already been converted to four-column `[x, y, width, height]`.

## Invalid or provisional outputs

NFS-derived outputs are provisional:

- NFS rows in `experiments/baseline_results.csv`
- `experiments/rgssb_hpc_nfs_comparison.csv`
- `experiments/rgssb_hpc_nfs_expanded32_comparison.csv`
- `experiments/rgssb_hpc_failure_focused_uav_nfs_comparison.csv` for its NFS subset
- NFS sections in paper-level result summaries
- NFS qualitative overlays under `outputs/failure_inspection/`

OTB and UAV123 are outside this audit scope.

## Decision

Do not modify or rerun experiments yet. First, create an explicit NFS annotation normalization step that converts raw NFS rows into OSTrack-compatible `[x, y, width, height]` rows aligned one-to-one with the constructed frame list. After that, rerun NFS tracking if the prior run used raw ten-column annotations. If prior Speed runs can prove that `anno/nfs_*.txt` already contained converted four-column rows, then regenerate only NFS metrics and overlays.

## Audit table

See `experiments/nfs_ground_truth_format_audit.csv` for per-frame raw rows, image sizes, candidate coordinate interpretations, frame alignment, and prediction-file availability.

## Verification

- Inspected `external/OSTrack/lib/test/evaluation/nfsdataset.py`.
- Inspected project-side NFS evaluation and visualization scripts.
- Read raw NFS annotation rows from the configured NFS source without modifying datasets.
- Wrote this audit without running OSTrack tracking, training, or benchmark evaluation.
