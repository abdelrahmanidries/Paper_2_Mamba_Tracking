#!/usr/bin/env python3
"""Analyze temporal drift onset for corrected NFS failure cases.

This script is offline-only. It reads existing corrected NFS predictions or
previously generated per-frame diagnostics and never runs OSTrack.
"""

from __future__ import annotations

import argparse
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
from scripts.inspect_tracking_failure_case import (
    comparison_row,
    condition_dir_name,
    exact_row,
    get_sequence_info,
    resolve_result_path,
)
from src.evaluation.nfs_annotations import canonical_sequence_info, load_canonical_nfs_ground_truth, metadata_frame_paths


BASELINE_CONFIG = "vitb_256_mae_ce_32x4_ep300"
RGSSB_CONFIG = "vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_degraded_hpc_featcons_lam002"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze corrected NFS temporal drift-onset cases.")
    parser.add_argument("--config", default="configs/nfs_failure_cases_to_inspect.json", type=Path)
    parser.add_argument("--case_index", type=int, default=None)
    parser.add_argument("--sequence", default=None)
    parser.add_argument("--degradation", default=None)
    parser.add_argument("--severity", default=None)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--diagnostics_root", default="outputs/failure_inspection_corrected_nfs", type=Path)
    parser.add_argument("--output_root", default="outputs/failure_inspection_corrected_nfs", type=Path)
    parser.add_argument("--combined_csv", default="experiments/nfs_corrected_drift_onset_analysis.csv", type=Path)
    parser.add_argument("--check_only", action="store_true")
    parser.add_argument("--max_contact_frames", type=int, default=21)
    return parser.parse_args()


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as csv_file:
        return list(csv.DictReader(csv_file))


def write_csv(path: Path, rows: Iterable[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


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


def case_dir(root: Path, case: dict) -> Path:
    return root / str(case["sequence"]) / condition_dir_name(case["degradation"], case["severity"], case["seed"])


def to_float(value: object) -> float:
    if value is None or value == "":
        return math.nan
    try:
        return float(value)
    except (TypeError, ValueError):
        return math.nan


def parse_box(value: str) -> list[float]:
    if value.startswith("["):
        return [float(x) for x in json.loads(value)]
    return [float(x) for x in value.replace(",", " ").split()[:4]]


def load_diagnostics(path: Path) -> dict[str, np.ndarray]:
    rows = read_csv_rows(path)
    if not rows:
        raise ValueError(f"No diagnostics rows found: {path}")
    return {
        "baseline_iou": np.asarray([to_float(row["baseline_iou"]) for row in rows], dtype=np.float64),
        "rgssb_iou": np.asarray([to_float(row["rgssb_iou"]) for row in rows], dtype=np.float64),
        "baseline_center_error": np.asarray([to_float(row["baseline_center_error"]) for row in rows], dtype=np.float64),
        "rgssb_center_error": np.asarray([to_float(row["rgssb_center_error"]) for row in rows], dtype=np.float64),
        "baseline_boxes": np.asarray([parse_box(row["baseline_box"]) for row in rows], dtype=np.float64),
        "rgssb_boxes": np.asarray([parse_box(row["rgssb_box"]) for row in rows], dtype=np.float64),
        "gt_boxes": np.asarray([parse_box(row["ground_truth_box"]) for row in rows], dtype=np.float64),
    }


def choose_nfs_root(cfg: dict, case: dict) -> Path:
    candidates: list[Path] = []
    if case["degradation"] != "clean":
        candidates.append(Path(cfg.get("degraded_root_base", "")) / f"nfs_{case['sequence']}_{case['degradation']}_{case['severity']}")
    for key in ("local_clean_nfs_root", "clean_nfs_root"):
        if cfg.get(key):
            candidates.append(Path(cfg[key]))
    for candidate in candidates:
        if candidate and candidate.exists():
            return candidate
    return Path(cfg.get("local_clean_nfs_root") or cfg.get("clean_nfs_root", ""))


def load_from_predictions(cfg: dict, case: dict, result_rows: list[dict[str, str]]) -> tuple[dict[str, np.ndarray], dict[str, object]]:
    baseline_config = case.get("baseline_config") or cfg.get("baseline_config", BASELINE_CONFIG)
    test_config = case.get("rgssb_config") or case.get("test_config") or cfg.get("test_config", RGSSB_CONFIG)
    baseline_row = exact_row(result_rows, baseline_config, case["sequence"], case["degradation"], case["severity"], case["seed"])
    test_row = exact_row(result_rows, test_config, case["sequence"], case["degradation"], case["severity"], case["seed"])
    baseline_path, baseline_candidates = resolve_result_path(cfg, baseline_row, baseline_config, case)
    test_path, test_candidates = resolve_result_path(cfg, test_row, test_config, case)
    if baseline_path is None or test_path is None:
        raise FileNotFoundError(
            "Missing existing prediction file. "
            f"baseline_found={baseline_path is not None} test_found={test_path is not None} "
            f"baseline_candidates={[str(p) for p in baseline_candidates[:3]]} "
            f"test_candidates={[str(p) for p in test_candidates[:3]]}"
        )
    nfs_root = choose_nfs_root(cfg, case)
    bundle = load_canonical_nfs_ground_truth(nfs_root, case["sequence"])
    baseline_boxes = load_boxes(baseline_path).astype(np.float64)
    rgssb_boxes = load_boxes(test_path).astype(np.float64)
    if len(baseline_boxes) != len(bundle.gt_xywh) or len(rgssb_boxes) != len(bundle.gt_xywh):
        raise ValueError(
            f"Prediction/aligned GT mismatch for {case['sequence']}: "
            f"baseline={len(baseline_boxes)} rgssb={len(rgssb_boxes)} gt={len(bundle.gt_xywh)}"
        )
    data = {
        "baseline_iou": box_iou_xywh(bundle.gt_xywh, baseline_boxes),
        "rgssb_iou": box_iou_xywh(bundle.gt_xywh, rgssb_boxes),
        "baseline_center_error": center_error(bundle.gt_xywh, baseline_boxes),
        "rgssb_center_error": center_error(bundle.gt_xywh, rgssb_boxes),
        "baseline_boxes": baseline_boxes,
        "rgssb_boxes": rgssb_boxes,
        "gt_boxes": bundle.gt_xywh,
    }
    meta = {
        "baseline_result_path": str(baseline_path),
        "rgssb_result_path": str(test_path),
        "ground_truth_root": str(nfs_root),
        "raw_annotation_count": bundle.raw_annotation_count,
        "aligned_annotation_count": bundle.aligned_annotation_count,
        "image_count": bundle.image_count,
        "sampling_stride": bundle.sampling_stride,
        "coordinate_format": bundle.coordinate_format,
    }
    return data, meta


def first_sustained(mask: np.ndarray, run_length: int = 5) -> tuple[int | None, int]:
    count = 0
    start = 0
    for idx, value in enumerate(mask):
        if bool(value):
            if count == 0:
                start = idx
            count += 1
            if count >= run_length:
                return start, count
        else:
            count = 0
    return None, 0


def centers(boxes: np.ndarray) -> np.ndarray:
    return np.column_stack((boxes[:, 0] + boxes[:, 2] / 2.0, boxes[:, 1] + boxes[:, 3] / 2.0))


def safe_area_ratios(boxes: np.ndarray) -> np.ndarray:
    areas = np.maximum(boxes[:, 2] * boxes[:, 3], 1e-6)
    ratios = areas[1:] / areas[:-1]
    return np.concatenate(([math.nan], ratios))


def first_threshold(values: np.ndarray, threshold: float, op: str = ">=") -> int | None:
    if op == ">=":
        hits = np.where(values >= threshold)[0]
    else:
        hits = np.where(values <= threshold)[0]
    return int(hits[0]) if len(hits) else None


def recovery_after(iou: np.ndarray, start_idx: int | None, run_length: int = 5) -> tuple[bool, int | None]:
    if start_idx is None:
        return False, None
    idx, _ = first_sustained(iou[start_idx + 1 :] >= 0.4, run_length=run_length)
    if idx is None:
        return False, None
    return True, start_idx + 1 + idx


def classify_failure(
    divergence_idx: int | None,
    shared_idx: int | None,
    jump_idx: int | None,
    scale_idx: int | None,
    recovery: bool,
) -> str:
    if divergence_idx is not None and (shared_idx is None or divergence_idx < shared_idx):
        if recovery:
            return "temporary RG-SSB-specific failure with recovery"
        return "persistent RG-SSB-specific target loss"
    if shared_idx is not None and (divergence_idx is None or shared_idx <= divergence_idx):
        return "shared tracker failure"
    if jump_idx is not None:
        return "sudden center jump"
    if scale_idx is not None:
        return "scale collapse or expansion"
    return "ambiguous"


def event_row(event_type: str, idx: int | None, data: dict[str, np.ndarray], extra: dict[str, object] | None = None) -> dict[str, object]:
    row: dict[str, object] = {"event_type": event_type, "frame_index": "", "frame_number": ""}
    if idx is not None:
        row.update(
            {
                "frame_index": idx,
                "frame_number": idx + 1,
                "baseline_iou": float(data["baseline_iou"][idx]),
                "rgssb_iou": float(data["rgssb_iou"][idx]),
                "baseline_center_error": float(data["baseline_center_error"][idx]),
                "rgssb_center_error": float(data["rgssb_center_error"][idx]),
            }
        )
    if extra:
        row.update(extra)
    return row


def frame_window(center_idx: int | None, frame_count: int, before: int = 10, after: int = 10) -> list[int]:
    if center_idx is None:
        return []
    start = max(0, center_idx - before)
    end = min(frame_count - 1, center_idx + after)
    return list(range(start, end + 1))


def draw_overlay(image, gt_box, baseline_box, rgssb_box, label: str):
    from PIL import ImageDraw

    draw = ImageDraw.Draw(image)
    for box, color, name in [
        (gt_box, "lime", "gt"),
        (baseline_box, "dodgerblue", "baseline"),
        (rgssb_box, "red", "rgssb"),
    ]:
        x, y, w, h = [float(v) for v in box]
        draw.rectangle([x, y, x + w, y + h], outline=color, width=3)
        draw.text((x, max(0, y - 12)), name, fill=color)
    draw.rectangle([0, 0, min(image.width, 460), 24], fill=(0, 0, 0))
    draw.text((4, 5), label, fill="white")
    return image


def save_contact_sheet(
    case_output: Path,
    cfg: dict,
    case: dict,
    data: dict[str, np.ndarray],
    center_idx: int | None,
    max_frames: int,
) -> tuple[int, str | None]:
    if center_idx is None or max_frames <= 0:
        return 0, None
    try:
        from PIL import Image
    except Exception as exc:
        print(f"warning: PIL unavailable; skipping contact sheet for {case['sequence']}: {exc}")
        return 0, None

    nfs_root = choose_nfs_root(cfg, case)
    if not nfs_root.exists():
        print(f"warning: NFS image root unavailable; skipping contact sheet for {case['sequence']}: {nfs_root}")
        return 0, None
    frames = metadata_frame_paths(nfs_root, canonical_sequence_info(get_sequence_info(case["sequence"])))
    indices = frame_window(center_idx, len(data["rgssb_iou"]))
    if len(indices) > max_frames:
        indices = indices[:max_frames]
    overlays = []
    visuals_dir = case_output / "drift_window_overlays"
    visuals_dir.mkdir(parents=True, exist_ok=True)
    for idx in indices:
        if idx >= len(frames) or not frames[idx].is_file():
            continue
        image = Image.open(frames[idx]).convert("RGB")
        label = f"f={idx + 1} bIoU={data['baseline_iou'][idx]:.2f} rIoU={data['rgssb_iou'][idx]:.2f}"
        image = draw_overlay(image, data["gt_boxes"][idx], data["baseline_boxes"][idx], data["rgssb_boxes"][idx], label)
        image.thumbnail((320, 240))
        image.save(visuals_dir / f"frame_{idx + 1:05d}.jpg")
        overlays.append(image.copy())
    if not overlays:
        return 0, None
    tile_w = max(img.width for img in overlays)
    tile_h = max(img.height for img in overlays)
    cols = min(5, len(overlays))
    rows = int(math.ceil(len(overlays) / cols))
    sheet = Image.new("RGB", (cols * tile_w, rows * tile_h), "white")
    for i, image in enumerate(overlays):
        sheet.paste(image, ((i % cols) * tile_w, (i // cols) * tile_h))
    sheet_path = case_output / "drift_onset_contact_sheet.jpg"
    sheet.save(sheet_path)
    return len(overlays), str(sheet_path)


def analyze_case(
    cfg: dict,
    case: dict,
    args: argparse.Namespace,
    result_rows: list[dict[str, str]],
    comparison_rows: list[dict[str, str]],
) -> dict[str, object]:
    sequence = str(case["sequence"])
    degradation = str(case["degradation"])
    severity = str(case["severity"])
    seed = str(case["seed"])
    diagnostics_path = case_dir(args.diagnostics_root, case) / "per_frame_diagnostics.csv"
    source = "diagnostics_csv"
    meta: dict[str, object] = {}
    if diagnostics_path.is_file():
        data = load_diagnostics(diagnostics_path)
        meta["diagnostics_path"] = str(diagnostics_path)
    else:
        source = "prediction_files"
        data, meta = load_from_predictions(cfg, case, result_rows)

    baseline_iou = data["baseline_iou"]
    rgssb_iou = data["rgssb_iou"]
    rgssb_boxes = data["rgssb_boxes"]
    frame_count = len(rgssb_iou)
    divergence_idx, divergence_run = first_sustained((baseline_iou >= 0.4) & (rgssb_iou <= 0.2), run_length=5)
    shared_idx, shared_run = first_sustained((baseline_iou <= 0.2) & (rgssb_iou <= 0.2), run_length=5)

    center_steps = np.concatenate(([math.nan], np.linalg.norm(np.diff(centers(rgssb_boxes), axis=0), axis=1)))
    jump_idx = first_threshold(center_steps, 100.0, op=">=")
    area_ratios = safe_area_ratios(rgssb_boxes)
    scale_hits = np.where((area_ratios >= 2.0) | (area_ratios <= 0.5))[0]
    scale_idx = int(scale_hits[0]) if len(scale_hits) else None

    first_failure_idx = min([idx for idx in [divergence_idx, shared_idx, jump_idx, scale_idx] if idx is not None], default=None)
    recovered, recovery_idx = recovery_after(rgssb_iou, divergence_idx, run_length=5)
    classification = classify_failure(divergence_idx, shared_idx, jump_idx, scale_idx, recovered)

    comp = comparison_row(comparison_rows, sequence, degradation, severity, seed)
    auc_change = to_float(comp.get("auc_change") if comp else case.get("corrected_auc_change"))
    baseline_auc = to_float(comp.get("baseline_auc") if comp else case.get("corrected_baseline_auc"))
    rgssb_auc = to_float(comp.get("hpc_rgssb_auc") if comp else case.get("corrected_rgssb_auc"))

    output_dir = case_dir(args.output_root, case)
    output_dir.mkdir(parents=True, exist_ok=True)
    events = [
        event_row("first_rgssb_specific_sustained_divergence", divergence_idx, data, {"consecutive_frames": divergence_run}),
        event_row("first_shared_failure", shared_idx, data, {"consecutive_frames": shared_run}),
        event_row("first_large_rgssb_center_jump", jump_idx, data, {"center_displacement_px": float(center_steps[jump_idx]) if jump_idx is not None else ""}),
        event_row("first_severe_scale_change", scale_idx, data, {"area_ratio": float(area_ratios[scale_idx]) if scale_idx is not None else ""}),
        event_row("first_recovery", recovery_idx, data, {"recovered": recovered}),
    ]
    event_fields = [
        "event_type",
        "frame_index",
        "frame_number",
        "baseline_iou",
        "rgssb_iou",
        "baseline_center_error",
        "rgssb_center_error",
        "consecutive_frames",
        "center_displacement_px",
        "area_ratio",
        "recovered",
    ]
    write_csv(output_dir / "drift_events.csv", events, event_fields)

    contact_center_idx = divergence_idx if divergence_idx is not None else first_failure_idx
    visuals_saved, contact_sheet = save_contact_sheet(output_dir, cfg, case, data, contact_center_idx, args.max_contact_frames)
    summary = {
        "sequence": sequence,
        "condition": f"{degradation} {severity}",
        "degradation": degradation,
        "severity": severity,
        "seed": int(seed),
        "source": source,
        "frame_count": int(frame_count),
        "baseline_auc": baseline_auc,
        "rgssb_auc": rgssb_auc,
        "auc_change": auc_change,
        "first_divergence_frame": int(divergence_idx + 1) if divergence_idx is not None else None,
        "baseline_iou_at_divergence": float(baseline_iou[divergence_idx]) if divergence_idx is not None else None,
        "rgssb_iou_at_divergence": float(rgssb_iou[divergence_idx]) if divergence_idx is not None else None,
        "first_shared_failure_frame": int(shared_idx + 1) if shared_idx is not None else None,
        "first_center_jump_frame": int(jump_idx + 1) if jump_idx is not None else None,
        "first_center_jump_px": float(center_steps[jump_idx]) if jump_idx is not None else None,
        "first_scale_change_frame": int(scale_idx + 1) if scale_idx is not None else None,
        "first_area_ratio": float(area_ratios[scale_idx]) if scale_idx is not None else None,
        "consecutive_failed_frames": int(divergence_run or shared_run),
        "recovery_status": "recovered" if recovered else "no_recovery_detected",
        "recovery_frame": int(recovery_idx + 1) if recovery_idx is not None else None,
        "failure_classification": classification,
        "visual_overlay_frames_saved": visuals_saved,
        "contact_sheet": contact_sheet,
        **meta,
    }
    (output_dir / "drift_onset_summary.json").write_text(json.dumps(summary, indent=2, allow_nan=True) + "\n", encoding="utf-8")

    return {
        "sequence": sequence,
        "condition": f"{degradation} {severity}",
        "degradation": degradation,
        "severity": severity,
        "seed": int(seed),
        "auc_change": f"{auc_change:+.6f}" if not math.isnan(auc_change) else "nan",
        "first_divergence_frame": summary["first_divergence_frame"] or "",
        "baseline_iou_at_divergence": f"{summary['baseline_iou_at_divergence']:.6f}" if summary["baseline_iou_at_divergence"] is not None else "",
        "rgssb_iou_at_divergence": f"{summary['rgssb_iou_at_divergence']:.6f}" if summary["rgssb_iou_at_divergence"] is not None else "",
        "center_jump": f"{summary['first_center_jump_px']:.6f}" if summary["first_center_jump_px"] is not None else "",
        "area_ratio": f"{summary['first_area_ratio']:.6f}" if summary["first_area_ratio"] is not None else "",
        "consecutive_failed_frames": summary["consecutive_failed_frames"],
        "recovery_status": summary["recovery_status"],
        "failure_classification": classification,
        "output_dir": str(output_dir),
        "source": source,
    }


def check_only(cfg: dict, cases: list[dict], args: argparse.Namespace) -> int:
    result_rows = read_csv_rows(Path(cfg["results_csv"]))
    comparison_rows = read_csv_rows(Path(cfg["comparison_csv"]))
    missing_rows = []
    missing_result_pairs = 0
    diagnostics_found = 0
    print(f"cases: {len(cases)}")
    print(f"diagnostics_root: {args.diagnostics_root}")
    print(f"output_root: {args.output_root}")
    for idx, case in enumerate(cases):
        get_sequence_info(case["sequence"])
        comp = comparison_row(comparison_rows, case["sequence"], case["degradation"], case["severity"], case["seed"])
        base = exact_row(result_rows, case.get("baseline_config", cfg["baseline_config"]), case["sequence"], case["degradation"], case["severity"], case["seed"])
        test = exact_row(result_rows, case.get("rgssb_config", cfg["test_config"]), case["sequence"], case["degradation"], case["severity"], case["seed"])
        if comp is None or base is None or test is None:
            missing_rows.append((case["sequence"], case["degradation"], case["severity"], case["seed"]))
        base_path, _ = resolve_result_path(cfg, base, case.get("baseline_config", cfg["baseline_config"]), case)
        test_path, _ = resolve_result_path(cfg, test, case.get("rgssb_config", cfg["test_config"]), case)
        diag_path = case_dir(args.diagnostics_root, case) / "per_frame_diagnostics.csv"
        diagnostics_found += int(diag_path.is_file())
        if base_path is None or test_path is None:
            missing_result_pairs += 1
        print(
            f"[{idx}] {case['sequence']} {case['degradation']}/{case['severity']} seed {case['seed']} "
            f"auc_change={(comp or case).get('auc_change') or case.get('corrected_auc_change')} "
            f"diagnostics={diag_path.is_file()} baseline_result={base_path is not None} rgssb_result={test_path is not None}"
        )
    if missing_rows:
        raise ValueError(f"Missing corrected CSV rows for cases: {missing_rows[:5]}")
    if missing_result_pairs:
        print(f"warning: {missing_result_pairs}/{len(cases)} cases lack local prediction files; run full analysis on Speed or provide diagnostics CSVs.")
    print(f"diagnostics_found: {diagnostics_found}/{len(cases)}")
    print("check_only: passed")
    return 0


def main() -> int:
    args = parse_args()
    cfg = load_json(args.config)
    cases = filter_cases(list(cfg["cases"]), args)
    if not cases:
        raise ValueError("No failure cases matched filters")
    if args.check_only:
        return check_only(cfg, cases, args)

    result_rows = read_csv_rows(Path(cfg["results_csv"]))
    comparison_rows = read_csv_rows(Path(cfg["comparison_csv"]))
    combined = [analyze_case(cfg, case, args, result_rows, comparison_rows) for case in cases]
    fields = [
        "sequence",
        "condition",
        "degradation",
        "severity",
        "seed",
        "auc_change",
        "first_divergence_frame",
        "baseline_iou_at_divergence",
        "rgssb_iou_at_divergence",
        "center_jump",
        "area_ratio",
        "consecutive_failed_frames",
        "recovery_status",
        "failure_classification",
        "output_dir",
        "source",
    ]
    write_csv(args.combined_csv, combined, fields)
    print(f"wrote {args.combined_csv} rows={len(combined)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
