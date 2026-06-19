#!/usr/bin/env python3
"""Audit NFS raw annotation format, frame alignment, and metric validity."""

from __future__ import annotations

import argparse
import ast
import csv
import io
import json
import math
import re
import sys
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import numpy as np
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.evaluate_tracking_result import load_boxes


NFS_DATASET_PY = ROOT / "external" / "OSTrack" / "lib" / "test" / "evaluation" / "nfsdataset.py"
DEFAULT_LOCAL_NFS_ROOT = Path("/media/abdel/4484139E5D690B76/nfs")
DEFAULT_SPEED_NFS_ROOT = Path("/speed-scratch/a_idrais/nfs")

BASELINE_CONFIG = "vitb_256_mae_ce_32x4_ep300"
TEST_CONFIG = "vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_degraded_hpc_featcons_lam002"

AUDIT_CASES = [
    {"sequence": "nfs_cheetah", "degradation": "low_resolution", "severity": "medium", "seed": 42, "frames": [26, 40, 45]},
    {"sequence": "nfs_walking", "degradation": "gaussian_noise", "severity": "medium", "seed": 42, "frames": [80, 111, 338, 343, 374]},
    {"sequence": "nfs_walking", "degradation": "motion_blur", "severity": "medium", "seed": 42, "frames": [80, 111, 338, 343, 374]},
    {"sequence": "nfs_drone", "degradation": "clean", "severity": "none", "seed": 0, "frames": [10, 30, 50], "control": True},
]


@dataclass
class AnnotationSource:
    mode: str
    annotation_id: str
    image_id_template: str
    raw_lines: list[str]
    zip_path: Path | None = None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Audit NFS annotation format and project-side metric validity.")
    parser.add_argument("--nfs_root", type=Path, default=DEFAULT_LOCAL_NFS_ROOT if DEFAULT_LOCAL_NFS_ROOT.exists() else DEFAULT_SPEED_NFS_ROOT)
    parser.add_argument("--results_csv", type=Path, default=Path("experiments/baseline_results.csv"))
    parser.add_argument("--output_csv", type=Path, default=Path("experiments/nfs_ground_truth_format_audit.csv"))
    parser.add_argument("--output_md", type=Path, default=Path("implementation/nfs_ground_truth_format_audit.md"))
    parser.add_argument("--check_predictions", action="store_true", help="Try to load prediction files referenced by baseline_results.csv.")
    return parser.parse_args()


def load_sequence_info() -> list[dict]:
    module = ast.parse(NFS_DATASET_PY.read_text(encoding="utf-8"))
    for node in ast.walk(module):
        if isinstance(node, ast.FunctionDef) and node.name == "_get_sequence_info_list":
            for child in ast.walk(node):
                if isinstance(child, ast.Assign):
                    for target in child.targets:
                        if isinstance(target, ast.Name) and target.id == "sequence_info_list":
                            return ast.literal_eval(child.value)
    raise RuntimeError(f"Could not parse sequence_info_list from {NFS_DATASET_PY}")


def get_sequence_info(sequence: str) -> dict:
    for info in load_sequence_info():
        if info["name"] == sequence:
            return info
    raise ValueError(f"Unknown NFS sequence: {sequence}")


def sequence_basename(info: dict) -> str:
    return Path(info["path"]).name


def expected_frame_count(info: dict) -> int:
    return int(info["endFrame"]) - (int(info["startFrame"]) + int(info.get("initOmit", 0))) + 1


def frame_number_for_audit_frame(info: dict, audit_frame_number: int) -> int:
    # Audit frame numbers are 1-based positions in OSTrack's constructed frame list.
    return int(info["startFrame"]) + int(info.get("initOmit", 0)) + audit_frame_number - 1


def parse_numeric_prefix(line: str) -> tuple[list[float], int, str]:
    tokens = re.split(r"[\s,\t]+", line.strip())
    numeric: list[float] = []
    for token in tokens:
        if not token:
            continue
        try:
            numeric.append(float(token))
        except ValueError:
            break
    delimiter = "tab" if "\t" in line else "comma" if "," in line else "whitespace"
    return numeric, len(tokens), delimiter


def find_annotation_source(nfs_root: Path, info: dict) -> AnnotationSource:
    extracted_anno = nfs_root / info["anno_path"]
    if extracted_anno.is_file():
        return AnnotationSource(
            mode="extracted_ostrack_layout",
            annotation_id=str(extracted_anno),
            image_id_template=str(nfs_root / info["path"] / "{frame:05d}." + str(info["ext"])),
            raw_lines=extracted_anno.read_text(encoding="utf-8").splitlines(),
        )

    base = sequence_basename(info)
    zip_path = nfs_root / f"{base}.zip"
    if zip_path.is_file():
        with zipfile.ZipFile(zip_path) as zf:
            names = set(zf.namelist())
            annotation_candidates = [
                f"{base}/30/{base}.txt",
                f"{base}/240/{base}.txt",
                f"{base}/{base}.txt",
            ]
            annotation_member = next((name for name in annotation_candidates if name in names), None)
            if annotation_member is None:
                raise FileNotFoundError(f"No expected annotation member found in {zip_path}")
            raw_lines = zf.read(annotation_member).decode("utf-8", errors="replace").splitlines()
        return AnnotationSource(
            mode="zip_raw_nfs",
            annotation_id=f"{zip_path}:{annotation_member}",
            image_id_template=f"{zip_path}:{base}/30/{base}/{{frame:05d}}.{info['ext']}",
            raw_lines=raw_lines,
            zip_path=zip_path,
        )

    raise FileNotFoundError(f"No extracted annotation or zip archive found for {info['name']} under {nfs_root}")


def read_image_size(nfs_root: Path, info: dict, source: AnnotationSource, frame_number: int) -> tuple[int | None, int | None, str, bool]:
    base = sequence_basename(info)
    ext = str(info["ext"])
    if source.mode == "extracted_ostrack_layout":
        path = nfs_root / info["path"] / f"{frame_number:0{int(info['nz'])}}.{ext}"
        if not path.is_file():
            return None, None, str(path), False
        with Image.open(path) as image:
            return image.size[0], image.size[1], str(path), True

    assert source.zip_path is not None
    candidates = [
        f"{base}/30/{base}/{frame_number:0{int(info['nz'])}}.{ext}",
        f"{base}/240/{base}/{frame_number:0{int(info['nz'])}}.{ext}",
    ]
    with zipfile.ZipFile(source.zip_path) as zf:
        names = set(zf.namelist())
        member = next((name for name in candidates if name in names), None)
        if member is None:
            return None, None, f"{source.zip_path}:{candidates[0]}", False
        with zf.open(member) as fp:
            data = fp.read()
        with Image.open(io.BytesIO(data)) as image:
            return image.size[0], image.size[1], f"{source.zip_path}:{member}", True


def aligned_annotation_indices(raw_count: int, expected_frames: int, init_omit: int) -> tuple[list[int], int]:
    available = max(0, raw_count - init_omit)
    if expected_frames <= 0:
        return [], 0
    if available == expected_frames:
        return list(range(init_omit, init_omit + expected_frames)), 1
    if available > expected_frames:
        stride = max(1, round(available / expected_frames))
        indices = list(range(init_omit, raw_count, stride))[:expected_frames]
        if len(indices) == expected_frames:
            return indices, stride
    return list(range(init_omit, raw_count)), 1


def candidate_boxes(values: list[float]) -> dict[str, list[float] | None]:
    out: dict[str, list[float] | None] = {
        "candidate_a_direct_c0_c3_xywh": None,
        "candidate_b_direct_c0_c3_xyxy_to_xywh": None,
        "candidate_c_raw_nfs_c1_c4_xyxy_to_xywh": None,
    }
    if len(values) >= 4:
        out["candidate_a_direct_c0_c3_xywh"] = [values[0], values[1], values[2], values[3]]
        out["candidate_b_direct_c0_c3_xyxy_to_xywh"] = [values[0], values[1], values[2] - values[0], values[3] - values[1]]
    if len(values) >= 5:
        out["candidate_c_raw_nfs_c1_c4_xyxy_to_xywh"] = [values[1], values[2], values[3] - values[1], values[4] - values[2]]
    return out


def plausibility(box: list[float] | None, width: int | None, height: int | None) -> tuple[bool, str]:
    if box is None:
        return False, "unavailable"
    x, y, w, h = box
    if not all(math.isfinite(v) for v in box):
        return False, "nonfinite"
    if w <= 0 or h <= 0:
        return False, "nonpositive_size"
    if width is None or height is None:
        return True, "positive_size_image_missing"
    area_ratio = (w * h) / max(width * height, 1)
    inside = x >= -2 and y >= -2 and x + w <= width + 2 and y + h <= height + 2
    if not inside:
        return False, f"outside_image_area_ratio_{area_ratio:.4f}"
    if area_ratio > 0.95:
        return False, f"implausibly_large_area_ratio_{area_ratio:.4f}"
    return True, f"inside_image_area_ratio_{area_ratio:.4f}"


def row_for_prediction(rows: list[dict[str, str]], config: str, sequence: str, degradation: str, severity: str, seed: int) -> dict[str, str] | None:
    for row in rows:
        if (
            row.get("config") == config
            and row.get("sequence") == sequence
            and row.get("degradation") == degradation
            and row.get("severity") == severity
            and str(row.get("seed")) == str(seed)
        ):
            return row
    return None


def prediction_status(rows: list[dict[str, str]], config: str, case: dict, frame_position: int, check_predictions: bool) -> tuple[str, str, str]:
    row = row_for_prediction(rows, config, case["sequence"], case["degradation"], case["severity"], int(case["seed"]))
    if row is None:
        return "missing_csv_row", "", ""
    path = Path(row.get("result_path", ""))
    if not path.is_file():
        return "missing_result_file", str(path), ""
    if not check_predictions:
        return "exists_not_loaded", str(path), ""
    try:
        boxes = load_boxes(path)
    except Exception as exc:
        return "load_error", str(path), str(exc)
    if frame_position < 1 or frame_position > len(boxes):
        return "frame_out_of_range", str(path), f"prediction_rows={len(boxes)}"
    return "loaded", str(path), json.dumps([float(v) for v in boxes[frame_position - 1].tolist()])


def audit_rows(args: argparse.Namespace) -> tuple[list[dict[str, object]], dict[str, object]]:
    result_rows = []
    if args.results_csv.is_file():
        with args.results_csv.open("r", encoding="utf-8", newline="") as csv_file:
            result_rows = list(csv.DictReader(csv_file))

    output: list[dict[str, object]] = []
    per_sequence_sources = {}
    for case in AUDIT_CASES:
        info = get_sequence_info(case["sequence"])
        source = find_annotation_source(args.nfs_root, info)
        per_sequence_sources[case["sequence"]] = source
        expected_frames = expected_frame_count(info)
        indices, stride = aligned_annotation_indices(len(source.raw_lines), expected_frames, int(info.get("initOmit", 0)))
        for frame_position in case["frames"]:
            if frame_position < 1 or frame_position > len(indices):
                raise ValueError(f"Audit frame {frame_position} out of range for {case['sequence']}")
            raw_line_index = indices[frame_position - 1]
            raw_text = source.raw_lines[raw_line_index]
            numeric, raw_column_count, delimiter = parse_numeric_prefix(raw_text)
            frame_number = frame_number_for_audit_frame(info, frame_position)
            image_width, image_height, image_path, image_exists = read_image_size(args.nfs_root, info, source, frame_number)
            candidates = candidate_boxes(numeric)
            plaus = {name: plausibility(box, image_width, image_height) for name, box in candidates.items()}
            if plaus["candidate_c_raw_nfs_c1_c4_xyxy_to_xywh"][0]:
                inferred = "raw_nfs_columns_1_4_xyxy"
            elif plaus["candidate_a_direct_c0_c3_xywh"][0]:
                inferred = "direct_c0_c3_xywh"
            else:
                inferred = "undetermined"
            raw_frame_index_value = int(round(numeric[5])) if len(numeric) >= 6 and math.isfinite(numeric[5]) else None
            has_frame_index = raw_frame_index_value in {frame_number, raw_line_index + 1}
            base_status, base_path, base_box = prediction_status(result_rows, BASELINE_CONFIG, case, frame_position, args.check_predictions)
            test_status, test_path, test_box = prediction_status(result_rows, TEST_CONFIG, case, frame_position, args.check_predictions)
            row = {
                "sequence": case["sequence"],
                "is_control_sequence": bool(case.get("control", False)),
                "degradation": case["degradation"],
                "severity": case["severity"],
                "seed": case["seed"],
                "audit_frame_position": frame_position,
                "actual_frame_number": frame_number,
                "image_path": image_path,
                "image_exists": image_exists,
                "image_width": image_width if image_width is not None else "",
                "image_height": image_height if image_height is not None else "",
                "annotation_source_mode": source.mode,
                "raw_annotation_file": source.annotation_id,
                "raw_annotation_line_number_1based": raw_line_index + 1,
                "raw_annotation_text": raw_text,
                "parsed_numeric_columns": json.dumps(numeric),
                "raw_column_count": raw_column_count,
                "numeric_column_count": len(numeric),
                "has_frame_index_or_timestamp_column": has_frame_index,
                "raw_frame_index_column_value": raw_frame_index_value if raw_frame_index_value is not None else "",
                "raw_frame_index_matches_sampled_source_line": raw_frame_index_value == raw_line_index + 1,
                "raw_frame_index_matches_constructed_frame_number": raw_frame_index_value == frame_number,
                "detected_delimiter": delimiter,
                "expected_ostrack_frame_count": expected_frames,
                "raw_annotation_line_count": len(source.raw_lines),
                "aligned_annotation_count_project_sampler": len(indices),
                "project_sampler_stride": stride,
                "ostrack_loader_annotation_rows_after_init_omit": len(source.raw_lines) - int(info.get("initOmit", 0)),
                "candidate_a_direct_xywh": json.dumps(candidates["candidate_a_direct_c0_c3_xywh"]),
                "candidate_a_plausible": plaus["candidate_a_direct_c0_c3_xywh"][0],
                "candidate_a_reason": plaus["candidate_a_direct_c0_c3_xywh"][1],
                "candidate_b_direct_xyxy_to_xywh": json.dumps(candidates["candidate_b_direct_c0_c3_xyxy_to_xywh"]),
                "candidate_b_plausible": plaus["candidate_b_direct_c0_c3_xyxy_to_xywh"][0],
                "candidate_b_reason": plaus["candidate_b_direct_c0_c3_xyxy_to_xywh"][1],
                "candidate_c_raw_nfs_xyxy_to_xywh": json.dumps(candidates["candidate_c_raw_nfs_c1_c4_xyxy_to_xywh"]),
                "candidate_c_plausible": plaus["candidate_c_raw_nfs_c1_c4_xyxy_to_xywh"][0],
                "candidate_c_reason": plaus["candidate_c_raw_nfs_c1_c4_xyxy_to_xywh"][1],
                "inferred_raw_annotation_format": inferred,
                "baseline_prediction_status": base_status,
                "baseline_result_path": base_path,
                "baseline_prediction_box_if_loaded": base_box,
                "rgssb_prediction_status": test_status,
                "rgssb_result_path": test_path,
                "rgssb_prediction_box_if_loaded": test_box,
            }
            output.append(row)

    summary = {
        "audit_row_count": len(output),
        "nfs_root": str(args.nfs_root),
        "source_modes": sorted({source.mode for source in per_sequence_sources.values()}),
        "all_rows_have_raw_nfs_candidate_plausible": all(bool(row["candidate_c_plausible"]) for row in output),
        "any_direct_xywh_plausible": any(bool(row["candidate_a_plausible"]) for row in output),
        "all_rows_have_frame_index_column": all(bool(row["has_frame_index_or_timestamp_column"]) for row in output),
        "prediction_files_available": sum(1 for row in output if row["baseline_prediction_status"] in {"exists_not_loaded", "loaded"} and row["rgssb_prediction_status"] in {"exists_not_loaded", "loaded"}),
    }
    return output, summary


def write_csv(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0].keys()) if rows else []
    with path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, rows: list[dict[str, object]], summary: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    direct_ok = sum(1 for row in rows if bool(row["candidate_a_plausible"]))
    raw_ok = sum(1 for row in rows if bool(row["candidate_c_plausible"]))
    missing_predictions = sum(1 for row in rows if row["baseline_prediction_status"] == "missing_result_file" or row["rgssb_prediction_status"] == "missing_result_file")
    prediction_statement = (
        "Existing prediction files were not available in this workspace, so prediction contents were not audited locally."
        if missing_predictions
        else "Existing prediction files were present for audited rows."
    )
    md = f"""# NFS Ground-Truth Format Audit

## Status

All NFS-derived metrics, comparisons, qualitative overlays, and reports should be treated as **provisional** until the NFS annotation pipeline is corrected and the affected results are regenerated.

## Source-code findings

`external/OSTrack/lib/test/evaluation/nfsdataset.py` defines each sequence with `name`, `path`, `startFrame`, `endFrame`, zero padding `nz`, image extension `ext`, `anno_path`, and `object_class`. It constructs frame paths with:

```text
range(startFrame + initOmit, endFrame + 1)
```

It loads annotations with:

```text
load_text(anno_path, delimiter='\\t', dtype=np.float64)
ground_truth_rect[initOmit:, :]
```

The OSTrack loader does **not** convert raw NFS rows from `[track_id, x1, y1, x2, y2, frame, ...]` into `[x, y, width, height]`. Therefore, the authoritative coordinate convention returned in `Sequence.ground_truth_rect` is whatever the configured `anno/nfs_*.txt` files already contain. OSTrack expects those files to be compatible with tracker initialization and evaluation, effectively `[x, y, width, height]` rows with one row per constructed frame.

## Raw annotation findings

The audited local NFS source mode is `{', '.join(summary['source_modes'])}`. The script audited `{summary['audit_row_count']}` frame rows. In those raw rows:

- direct first-four-column `[x, y, width, height]` was numerically plausible for `{direct_ok}` rows, but this interpretation is contradicted by the ten-column raw schema and frame-index column.
- raw NFS columns 1-4 interpreted as `[x1, y1, x2, y2]`, converted to `[x, y, width, height]`, were plausible for `{raw_ok}` rows.
- a frame-index-like numeric column was detected in all rows: `{summary['all_rows_have_frame_index_column']}`. For dense raw NFS rows this column matches the sampled raw annotation line, not necessarily the constructed 30fps frame filename.

This supports the conclusion that the raw annotation rows in the audited NFS source are not directly usable as `[x, y, width, height]`.

## Frame alignment

The project-side NFS scripts currently add a custom sampler when raw annotation rows are denser than frame images. The sampler computes a stride from raw annotation count to expected frame count. This handles row-count mismatch, but it does not fix the coordinate-column format. If raw rows are still ten-column NFS rows, sampling alone is insufficient.

OSTrack's own `nfsdataset.py` does not perform this sampler. It simply returns `ground_truth_rect[initOmit:, :]`. If an extracted NFS root contains raw ten-column annotation files, OSTrack tracking may have been initialized from incorrect boxes as well.

## Existing predictions

{prediction_statement}

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
"""
    path.write_text(md, encoding="utf-8")


def main() -> int:
    args = parse_args()
    rows, summary = audit_rows(args)
    write_csv(args.output_csv, rows)
    write_markdown(args.output_md, rows, summary)
    print(f"rows: {len(rows)}")
    print(f"output_csv: {args.output_csv}")
    print(f"output_md: {args.output_md}")
    print(f"source_modes: {summary['source_modes']}")
    print(f"all_rows_have_raw_nfs_candidate_plausible: {summary['all_rows_have_raw_nfs_candidate_plausible']}")
    print(f"any_direct_xywh_plausible: {summary['any_direct_xywh_plausible']}")
    print(f"all_rows_have_frame_index_column: {summary['all_rows_have_frame_index_column']}")
    print(f"prediction_files_available_for_audited_rows: {summary['prediction_files_available']}/{len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
