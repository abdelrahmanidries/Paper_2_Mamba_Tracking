# NFS Ground-Truth Fix And Recovery Plan

## Confirmed Root Cause

The NFS annotations used by the current project-side pipeline are not in canonical tracker `[x, y, width, height]` form. Raw NFS annotations on Speed are `[x1, y1, x2, y2]`. For example:

```text
[525, 286, 945, 516] -> [525, 286, 420, 230]
```

OSTrack's `external/OSTrack/lib/test/evaluation/nfsdataset.py` loads annotation rows unchanged and returns `ground_truth_rect[initOmit:, :]`. It does not convert XYXY to XYWH and it does not downsample dense raw annotations to the sampled image sequence.

Therefore, existing NFS tracking was initialized with invalid boxes if it used the raw NFS annotations directly.

## Exact Alignment Rule

NFS 30fps image folders are sequentially named for the evaluated frame sequence, while raw annotations can retain denser rows. The verified alignment rule is:

```text
available = raw_annotation_count - initOmit
stride = round(available / image_count)
selected_raw_index(i) = initOmit + i * stride
```

where `i` is the zero-based evaluated-frame position.

Representative checks:

| sequence | image count | raw annotation count | stride | selected rows |
| --- | ---: | ---: | ---: | --- |
| nfs_cheetah | 167 | 1329 | 8 | 0, 8, 16, ..., 1328 |
| nfs_walking | 555 | 4433 | 8 | 0, 8, 16, ..., 4432 |
| nfs_Gymnastics | 368 | 2944 | 8 | 0, 8, 16, ..., 2936 |
| nfs_basketball_player | 369 | 2945 | 8 | 0, 8, 16, ..., 2944 |

The helper validates that the selected index list has exactly one row per evaluated image.

## Normalized-Root Design

Create a separate normalized root. Do not modify the original NFS dataset.

Recommended Speed path:

```text
/speed-scratch/a_idrais/nfs_ostrack_normalized
```

The normalized root contains:

```text
nfs_ostrack_normalized/
  sequences/
  anno/
  normalization_manifest.json
```

Images are reused through symlinks where possible. Annotation files are rewritten to contain exactly one canonical XYWH row per evaluated image.

## Degraded Root Construction Fix

OSTrack constructs the complete NFS sequence list even when `tracking/test.py` is called with one selected sequence. Therefore, a degraded single-sequence root must still preserve the complete normalized NFS layout.

The corrected degraded-root layout is:

```text
nfs_<sequence>_<degradation>_<severity>/
  normalization_manifest.json
  anno/                  # complete symlink/copy from normalized clean root
  sequences/
    <target>/            # copied target directory with degraded frames
    <non-target>/        # symlinked to normalized clean root
```

Annotations never change under image degradation, so `anno/` is mirrored in full from the normalized clean root. The target sequence keeps the same annotation file as the clean normalized root, and only the target images are degraded.

After creating a degraded root, `scripts/create_degraded_nfs_sequence.py` validates:

- degraded annotation-file count equals normalized annotation-file count
- degraded sequence-directory count equals normalized sequence-directory count
- every sequence entry in `external/OSTrack/lib/test/evaluation/nfsdataset.py` has a sequence directory and annotation file
- target annotation count equals target image count
- target annotations are canonical aligned XYWH

The test suite creates a temporary normalized NFS root, degrades `nfs_basketball_player`, and verifies that OSTrack's full `NFSDataset` can be constructed from the degraded root without running a tracker.

## Exact Recovery Order

1. Export invalid NFS rows:

```bash
python3 scripts/export_invalid_nfs_rows.py
```

2. Prepare the normalized NFS root:

```bash
python3 scripts/prepare_normalized_nfs_root.py \
  --raw_nfs_root /speed-scratch/a_idrais/nfs \
  --output_root /speed-scratch/a_idrais/nfs_ostrack_normalized
```

3. Verify the normalized root:

```bash
python3 scripts/verify_normalized_nfs_root.py \
  --nfs_root /speed-scratch/a_idrais/nfs_ostrack_normalized
```

4. After confirming the backup, remove invalid NFS rows from the main CSV:

```bash
python3 scripts/export_invalid_nfs_rows.py \
  --remove_from_main_csv
```

5. Edit NFS suite configs so `clean_nfs_root` points to:

```text
/speed-scratch/a_idrais/nfs_ostrack_normalized
```

6. Rerun corrected baseline NFS:

```bash
python3 scripts/run_nfs_degradation_suite.py \
  --suite_config configs/nfs_eval_suite_expanded32_ostrack.json \
  --no_skip_existing
```

7. Rerun corrected HPC RG-SSB NFS:

```bash
python3 scripts/run_nfs_degradation_suite.py \
  --suite_config configs/nfs_eval_suite_expanded32_hpc_rgssb_featcons_lam002.json \
  --no_skip_existing
```

8. Regenerate NFS analyses.

9. Regenerate cross-benchmark and paper-level tables.

## Invalid Artifacts

Treat these as invalid or provisional until corrected NFS is rerun:

- all `nfs_*` rows in `experiments/baseline_results.csv`
- `experiments/rgssb_hpc_nfs_comparison.csv`
- `experiments/rgssb_hpc_nfs_expanded32_comparison.csv`
- NFS rows in failure-focused comparisons
- NFS-derived cross-benchmark reports
- NFS portions of paper-level tables
- `outputs/failure_inspection/` NFS diagnostics and overlays

## Unaffected Artifacts

OTB and UAV123 are unaffected by this NFS-specific annotation issue.

Unaffected:

- OTB result rows and OTB analysis reports
- UAV123 result rows and UAV123 analysis reports
- non-NFS rows in `experiments/baseline_results.csv`
- training checkpoints

## Verification Commands

```bash
python3 -m py_compile \
  src/evaluation/nfs_annotations.py \
  scripts/prepare_normalized_nfs_root.py \
  scripts/verify_normalized_nfs_root.py \
  scripts/export_invalid_nfs_rows.py \
  scripts/inspect_nfs_sequences.py \
  scripts/create_degraded_nfs_sequence.py \
  scripts/run_ostrack_nfs_eval.py \
  scripts/inspect_tracking_failure_case.py
```

```bash
python3 -m pytest tests/test_nfs_ground_truth_parser.py
```

```bash
python3 scripts/export_invalid_nfs_rows.py \
  --check_only
```

## Decision

Existing NFS prediction files must be discarded for scientific reporting because tracker initialization used invalid ground truth if the raw NFS root was used. Corrected NFS tracking must be rerun from the normalized root before using NFS metrics in cross-benchmark claims.
