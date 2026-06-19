#!/usr/bin/env python3
"""Inspect per-frame tracking failures for logged NFS comparison cases."""

from __future__ import annotations

import argparse
import ast
import csv
import json
import math
import sys
from pathlib import Path
from typing import Iterable

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.evaluate_tracking_result import box_iou_xywh, center_error, load_boxes
from src.evaluation.nfs_annotations import (
    get_sequence_info as shared_get_sequence_info,
    load_canonical_nfs_ground_truth,
    metadata_frame_paths,
)


NFS_DATASET_PY = ROOT / "external" / "OSTrack" / "lib" / "test" / "evaluation" / "nfsdataset.py"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Inspect NFS tracking failure cases from existing result files.")
    parser.add_argument("--config", default="configs/nfs_failure_cases_to_inspect.json", type=Path)
    parser.add_argument("--case_index", type=int, default=None)
    parser.add_argument("--sequence", default=None)
    parser.add_argument("--degradation", default=None)
    parser.add_argument("--severity", default=None)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--save_visuals", action="store_true")
    parser.add_argument("--max_visual_frames", type=int, default=None)
    parser.add_argument("--check_only", action="store_true")
    return parser.parse_args()


def load_config(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_nfs_sequence_info() -> list[dict]:
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
    info = shared_get_sequence_info(sequence)
    return {
        "name": info.name,
        "path": info.path,
        "startFrame": info.start_frame,
        "endFrame": info.end_frame,
        "nz": info.nz,
        "ext": info.ext,
        "anno_path": info.anno_path,
        "object_class": info.object_class,
        "initOmit": info.init_omit,
    }


def frame_count(info: dict) -> int:
    start = int(info["startFrame"]) + int(info.get("initOmit", 0))
    end = int(info["endFrame"])
    return end - start + 1


def frame_paths(nfs_root: Path, info: dict) -> list[Path]:
    start = int(info["startFrame"]) + int(info.get("initOmit", 0))
    end = int(info["endFrame"])
    nz = int(info["nz"])
    ext = str(info["ext"])
    seq_dir = nfs_root / info["path"]
    return [seq_dir / f"{frame:0{nz}}.{ext}" for frame in range(start, end + 1)]


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


def load_aligned_gt(anno_path: Path, info: dict) -> tuple[np.ndarray, int, int]:
    bundle = load_canonical_nfs_ground_truth(anno_path.parents[1], str(info["name"]))
    return bundle.gt_xywh, bundle.raw_annotation_count, bundle.sampling_stride


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as csv_file:
        return list(csv.DictReader(csv_file))


def exact_row(rows: list[dict[str, str]], config: str, sequence: str, degradation: str, severity: str, seed: int | str) -> dict[str, str] | None:
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


def comparison_row(rows: list[dict[str, str]], sequence: str, degradation: str, severity: str, seed: int | str) -> dict[str, str] | None:
    for row in rows:
        if (
            row.get("sequence") == sequence
            and row.get("degradation") == degradation
            and row.get("severity") == severity
            and str(row.get("seed")) == str(seed)
        ):
            return row
    return None


def condition_dir_name(degradation: str, severity: str, seed: int | str) -> str:
    return f"{degradation}_{severity}_seed{seed}"


def candidate_result_paths(cfg: dict, row: dict[str, str] | None, config_name: str, case: dict) -> list[Path]:
    sequence = str(case["sequence"])
    degradation = str(case["degradation"])
    severity = str(case["severity"])
    seed = str(case["seed"])
    candidates: list[Path] = []
    if row and row.get("result_path"):
        candidates.append(Path(row["result_path"]))
    result_root = Path(cfg.get("result_root", "outputs/ostrack_runs"))
    candidates.append(
        result_root
        / "ostrack"
        / config_name
        / "nfs"
        / sequence
        / condition_dir_name(degradation, severity, seed)
        / f"{sequence}.txt"
    )
    candidates.append(
        result_root
        / "ostrack"
        / config_name
        / sequence
        / condition_dir_name(degradation, severity, seed)
        / f"{sequence}.txt"
    )
    candidates.append(result_root / sequence / condition_dir_name(degradation, severity, seed) / f"{sequence}.txt")
    return candidates


def resolve_result_path(cfg: dict, row: dict[str, str] | None, config_name: str, case: dict) -> tuple[Path | None, list[Path]]:
    candidates = candidate_result_paths(cfg, row, config_name, case)
    for path in candidates:
        if path.is_file():
            return path, candidates
    return None, candidates


def eval_root_for_case(cfg: dict, case: dict) -> Path:
    if case["degradation"] == "clean":
        return Path(cfg["clean_nfs_root"])
    return Path(cfg["degraded_root_base"]) / f"nfs_{case['sequence']}_{case['degradation']}_{case['severity']}"


def filter_cases(cases: list[dict], args: argparse.Namespace) -> list[dict]:
    selected = cases
    if args.case_index is not None:
        if args.case_index < 0 or args.case_index >= len(cases):
            raise IndexError(f"case_index {args.case_index} out of range for {len(cases)} cases")
        selected = [cases[args.case_index]]
    if args.sequence is not None:
        selected = [case for case in selected if case["sequence"] == args.sequence]
    if args.degradation is not None:
        selected = [case for case in selected if case["degradation"] == args.degradation]
    if args.severity is not None:
        selected = [case for case in selected if case["severity"] == args.severity]
    if args.seed is not None:
        selected = [case for case in selected if int(case["seed"]) == args.seed]
    return selected


def write_csv(path: Path, rows: Iterable[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def to_float(value: str | float | int | None) -> float:
    if value is None or value == "":
        return math.nan
    try:
        return float(value)
    except ValueError:
        return math.nan


def box_to_list(box: np.ndarray) -> list[float]:
    return [float(x) for x in box.tolist()]


def draw_visuals(
    case_dir: Path,
    frames: list[Path],
    gt: np.ndarray,
    baseline: np.ndarray,
    test: np.ndarray,
    diagnostics: list[dict[str, object]],
    max_visual_frames: int,
    stride: int,
) -> int:
    try:
        from PIL import Image, ImageDraw
    except Exception as exc:
        print(f"warning: PIL unavailable; skipping visuals: {exc}")
        return 0

    visuals_dir = case_dir / "visuals"
    visuals_dir.mkdir(parents=True, exist_ok=True)
    saved = 0
    stride = max(1, stride)
    for diag in diagnostics:
        if saved >= max_visual_frames:
            break
        frame_index = int(diag["frame_index"])
        if frame_index % stride != 0 and not bool(diag["bad_frame"]):
            continue
        image_path = frames[frame_index] if frame_index < len(frames) else None
        if image_path is None or not image_path.is_file():
            print(f"warning: image unavailable for frame {frame_index + 1}: {image_path}")
            continue
        image = Image.open(image_path).convert("RGB")
        draw = ImageDraw.Draw(image)
        for box, color, label in [
            (gt[frame_index], "lime", "gt"),
            (baseline[frame_index], "dodgerblue", "baseline"),
            (test[frame_index], "red", "rgssb"),
        ]:
            x, y, w, h = [float(v) for v in box]
            draw.rectangle([x, y, x + w, y + h], outline=color, width=3)
            draw.text((x, max(0, y - 12)), label, fill=color)
        text = (
            f"frame {frame_index + 1} "
            f"IoU b={float(diag['baseline_iou']):.3f} "
            f"r={float(diag['rgssb_iou']):.3f}"
        )
        draw.rectangle([0, 0, min(image.width, 420), 22], fill=(0, 0, 0))
        draw.text((4, 4), text, fill="white")
        image.save(visuals_dir / f"frame_{frame_index + 1:05d}.jpg")
        saved += 1
    return saved


def inspect_case(cfg: dict, case: dict, args: argparse.Namespace, result_rows: list[dict[str, str]], comparison_rows: list[dict[str, str]]) -> dict[str, object]:
    sequence = str(case["sequence"])
    degradation = str(case["degradation"])
    severity = str(case["severity"])
    seed = str(case["seed"])
    baseline_config = cfg["baseline_config"]
    test_config = cfg["test_config"]

    baseline_row = exact_row(result_rows, baseline_config, sequence, degradation, severity, seed)
    test_row = exact_row(result_rows, test_config, sequence, degradation, severity, seed)
    comp_row = comparison_row(comparison_rows, sequence, degradation, severity, seed)
    baseline_path, baseline_candidates = resolve_result_path(cfg, baseline_row, baseline_config, case)
    test_path, test_candidates = resolve_result_path(cfg, test_row, test_config, case)

    eval_root = eval_root_for_case(cfg, case)
    clean_root = Path(cfg["clean_nfs_root"])
    info = get_sequence_info(sequence)
    anno_root = eval_root if (eval_root / info["anno_path"]).is_file() else clean_root
    anno_path = anno_root / info["anno_path"]
    frames_root = eval_root if (eval_root / info["path"]).is_dir() else clean_root

    status = {
        "sequence": sequence,
        "degradation": degradation,
        "severity": severity,
        "seed": seed,
        "baseline_result": str(baseline_path) if baseline_path else None,
        "test_result": str(test_path) if test_path else None,
        "eval_root": str(eval_root),
        "annotation_path": str(anno_path),
    }

    if baseline_path is None or test_path is None:
        print(f"missing result file for {sequence} {degradation}/{severity} seed {seed}")
        print("  baseline candidates:")
        for path in baseline_candidates:
            print(f"    {path}")
        print("  test candidates:")
        for path in test_candidates:
            print(f"    {path}")
        status["processed"] = False
        status["reason"] = "missing_result_file"
        return status
    if not anno_path.is_file():
        print(f"missing annotation file for {sequence}: {anno_path}")
        status["processed"] = False
        status["reason"] = "missing_annotation_file"
        return status

    gt, raw_gt_count, gt_stride = load_aligned_gt(anno_path, info)
    base_pred = load_boxes(baseline_path)
    test_pred = load_boxes(test_path)
    if len(base_pred) != len(gt) or len(test_pred) != len(gt):
        raise ValueError(
            f"Prediction/aligned GT mismatch for {sequence}: "
            f"baseline={len(base_pred)} test={len(test_pred)} aligned_gt={len(gt)} raw_gt={raw_gt_count}"
        )

    base_iou = box_iou_xywh(gt, base_pred)
    test_iou = box_iou_xywh(gt, test_pred)
    base_ce = center_error(gt, base_pred)
    test_ce = center_error(gt, test_pred)
    iou_diff = test_iou - base_iou
    ce_diff = test_ce - base_ce

    diagnostics: list[dict[str, object]] = []
    bad_rows: list[dict[str, object]] = []
    for idx in range(len(gt)):
        bad = bool((test_iou[idx] <= base_iou[idx] - 0.2) or (ce_diff[idx] >= 20.0) or (test_iou[idx] < 0.1 and base_iou[idx] >= 0.3))
        row = {
            "frame_index": idx,
            "frame_number": idx + 1,
            "baseline_iou": float(base_iou[idx]),
            "rgssb_iou": float(test_iou[idx]),
            "iou_difference": float(iou_diff[idx]),
            "baseline_center_error": float(base_ce[idx]),
            "rgssb_center_error": float(test_ce[idx]),
            "center_error_difference": float(ce_diff[idx]),
            "baseline_box": json.dumps(box_to_list(base_pred[idx])),
            "rgssb_box": json.dumps(box_to_list(test_pred[idx])),
            "ground_truth_box": json.dumps(box_to_list(gt[idx])),
            "bad_frame": bad,
        }
        diagnostics.append(row)
        if bad:
            bad_rows.append(row)

    output_root = Path(cfg.get("output_root", "outputs/failure_inspection"))
    case_dir = output_root / sequence / condition_dir_name(degradation, severity, seed)
    fields = [
        "frame_index",
        "frame_number",
        "baseline_iou",
        "rgssb_iou",
        "iou_difference",
        "baseline_center_error",
        "rgssb_center_error",
        "center_error_difference",
        "baseline_box",
        "rgssb_box",
        "ground_truth_box",
        "bad_frame",
    ]
    write_csv(case_dir / "per_frame_diagnostics.csv", diagnostics, fields)
    write_csv(case_dir / "bad_frames.csv", bad_rows, fields)

    worst_iou_idx = int(np.argmin(iou_diff))
    worst_ce_idx = int(np.argmax(ce_diff))
    summary = {
        "sequence": sequence,
        "condition": condition_dir_name(degradation, severity, seed),
        "degradation": degradation,
        "severity": severity,
        "seed": int(seed),
        "frame_count": int(len(gt)),
        "raw_annotation_line_count": int(raw_gt_count),
        "aligned_ground_truth_count": int(len(gt)),
        "annotation_stride": int(gt_stride),
        "baseline_result_path": str(baseline_path),
        "rgssb_result_path": str(test_path),
        "mean_baseline_iou": float(np.mean(base_iou)),
        "mean_rgssb_iou": float(np.mean(test_iou)),
        "mean_iou_difference": float(np.mean(iou_diff)),
        "baseline_auc_from_comparison_csv": to_float(comp_row.get("baseline_auc") if comp_row else None),
        "rgssb_auc_from_comparison_csv": to_float(comp_row.get("hpc_rgssb_auc") if comp_row else None),
        "auc_change": to_float(comp_row.get("auc_change") if comp_row else case.get("auc_change")),
        "mean_baseline_center_error": float(np.mean(base_ce)),
        "mean_rgssb_center_error": float(np.mean(test_ce)),
        "mean_center_error_difference": float(np.mean(ce_diff)),
        "number_of_bad_frames": int(len(bad_rows)),
        "worst_frame_by_iou_drop": {
            "frame_index": worst_iou_idx,
            "frame_number": worst_iou_idx + 1,
            "iou_difference": float(iou_diff[worst_iou_idx]),
            "baseline_iou": float(base_iou[worst_iou_idx]),
            "rgssb_iou": float(test_iou[worst_iou_idx]),
        },
        "worst_frame_by_center_error_increase": {
            "frame_index": worst_ce_idx,
            "frame_number": worst_ce_idx + 1,
            "center_error_difference": float(ce_diff[worst_ce_idx]),
            "baseline_center_error": float(base_ce[worst_ce_idx]),
            "rgssb_center_error": float(test_ce[worst_ce_idx]),
        },
    }

    save_visuals = bool(args.save_visuals or cfg.get("save_visuals", False))
    max_visual_frames = args.max_visual_frames if args.max_visual_frames is not None else int(cfg.get("max_visual_frames", 30))
    if save_visuals and max_visual_frames > 0:
        frames = metadata_frame_paths(frames_root, shared_get_sequence_info(sequence))
        summary["visual_frames_saved"] = draw_visuals(
            case_dir,
            frames,
            gt,
            base_pred,
            test_pred,
            diagnostics,
            max_visual_frames=max_visual_frames,
            stride=int(cfg.get("frame_stride_for_visuals", 10)),
        )
    else:
        summary["visual_frames_saved"] = 0

    case_dir.mkdir(parents=True, exist_ok=True)
    (case_dir / "summary.json").write_text(json.dumps(summary, indent=2, allow_nan=True) + "\n", encoding="utf-8")
    print(f"processed {sequence} {degradation}/{severity} seed {seed}: {case_dir}")
    status["processed"] = True
    status["output_dir"] = str(case_dir)
    status["bad_frames"] = len(bad_rows)
    return status


def check_only(cfg: dict, cases: list[dict]) -> int:
    result_rows = read_rows(Path(cfg["results_csv"]))
    comparison_rows = read_rows(Path(cfg["comparison_csv"]))
    print(f"cases: {len(cases)}")
    print(f"baseline_config: {cfg['baseline_config']}")
    print(f"test_config: {cfg['test_config']}")
    print(f"clean_nfs_root: {cfg['clean_nfs_root']}")
    print(f"degraded_root_base: {cfg['degraded_root_base']}")
    print(f"output_root: {cfg['output_root']}")

    missing_metadata = []
    missing_rows = []
    missing_results = 0
    for idx, case in enumerate(cases):
        sequence = case["sequence"]
        degradation = case["degradation"]
        severity = case["severity"]
        seed = case["seed"]
        try:
            info = get_sequence_info(sequence)
        except ValueError:
            missing_metadata.append(sequence)
            continue
        baseline_row = exact_row(result_rows, cfg["baseline_config"], sequence, degradation, severity, seed)
        test_row = exact_row(result_rows, cfg["test_config"], sequence, degradation, severity, seed)
        comp_row = comparison_row(comparison_rows, sequence, degradation, severity, seed)
        if baseline_row is None or test_row is None or comp_row is None:
            missing_rows.append((sequence, degradation, severity, seed))
        base_path, _ = resolve_result_path(cfg, baseline_row, cfg["baseline_config"], case)
        test_path, _ = resolve_result_path(cfg, test_row, cfg["test_config"], case)
        if base_path is None or test_path is None:
            missing_results += 1
        expected_frames = frame_count(info)
        print(
            f"[{idx}] {sequence} {degradation}/{severity} seed {seed} "
            f"auc_change={case.get('auc_change')} expected_frames={expected_frames} "
            f"baseline_result_exists={base_path is not None} test_result_exists={test_path is not None}"
        )

    if missing_metadata:
        raise ValueError(f"Unknown NFS sequences in config: {missing_metadata}")
    if missing_rows:
        raise ValueError(f"Missing baseline/comparison CSV rows: {missing_rows[:5]}")
    if missing_results:
        print(f"warning: {missing_results}/{len(cases)} cases are missing local result files; run diagnostics on Speed outputs.")
    print("check_only: passed")
    return 0


def main() -> int:
    args = parse_args()
    cfg = load_config(args.config)
    cases = filter_cases(list(cfg["cases"]), args)
    if not cases:
        raise ValueError("No failure cases matched the requested filters")
    if args.check_only:
        return check_only(cfg, cases)

    result_rows = read_rows(Path(cfg["results_csv"]))
    comparison_rows = read_rows(Path(cfg["comparison_csv"]))
    statuses = [inspect_case(cfg, case, args, result_rows, comparison_rows) for case in cases]
    processed = [status for status in statuses if status.get("processed")]
    print(f"processed_cases: {len(processed)}/{len(statuses)}")
    return 0 if processed else 2


if __name__ == "__main__":
    raise SystemExit(main())
