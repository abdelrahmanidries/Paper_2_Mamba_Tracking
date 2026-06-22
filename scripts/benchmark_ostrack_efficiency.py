#!/usr/bin/env python3
"""Controlled same-GPU runtime benchmark for OSTrack Paper Freeze V1 models."""

from __future__ import annotations

import argparse
import csv
import importlib
import json
import os
import statistics
import sys
import time
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

import cv2
import numpy as np
import torch


CSV_COLUMNS = [
    "model_label",
    "config",
    "measurement_type",
    "repetition",
    "gpu_name",
    "torch_version",
    "cuda_version",
    "sequence",
    "frames",
    "warmup_frames",
    "initialization_ms",
    "mean_latency_ms",
    "median_latency_ms",
    "latency_std_ms",
    "fps",
    "peak_allocated_memory_mb",
    "peak_reserved_memory_mb",
    "total_params",
    "trainable_params",
    "frozen_params",
    "backbone_params",
    "rgssb_params",
    "box_head_params",
    "checkpoint_size_mb",
    "flops_or_macs",
    "provenance",
    "notes",
]


@contextmanager
def pushd(path: Path):
    old = Path.cwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(old)


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def parse_gt(path: Path) -> List[List[float]]:
    rows: List[List[float]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        sep = "," if "," in line else None
        rows.append([float(x) for x in line.split(sep)])
    return rows


def sequence_paths(otb_root: Path, sequence: str) -> Tuple[List[Path], List[List[float]]]:
    seq_dir = otb_root / sequence
    img_dir = seq_dir / "img"
    gt_path = seq_dir / "groundtruth_rect.txt"
    if not img_dir.exists() or not gt_path.exists():
        raise FileNotFoundError(f"Missing OTB sequence files for {sequence}: {seq_dir}")
    frames = sorted(
        [p for p in img_dir.iterdir() if p.suffix.lower() in {".jpg", ".jpeg", ".png", ".bmp"}]
    )
    gt = parse_gt(gt_path)
    if len(frames) != len(gt):
        raise ValueError(f"Frame/annotation mismatch for {sequence}: frames={len(frames)} gt={len(gt)}")
    if len(frames) < 2:
        raise ValueError(f"Need at least two frames for benchmark: {sequence}")
    return frames, gt


def read_rgb_frames(paths: Sequence[Path]) -> List[np.ndarray]:
    frames: List[np.ndarray] = []
    for path in paths:
        bgr = cv2.imread(str(path), cv2.IMREAD_COLOR)
        if bgr is None:
            raise ValueError(f"Could not read image: {path}")
        frames.append(cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB))
    return frames


def reset_ostrack_config_modules() -> None:
    for name in list(sys.modules):
        if name == "lib.config.ostrack.config":
            importlib.reload(sys.modules[name])


def load_tracker(ostrack_root: Path, config_name: str):
    if str(ostrack_root) not in sys.path:
        sys.path.insert(0, str(ostrack_root))
    with pushd(ostrack_root):
        reset_ostrack_config_modules()
        from lib.test.parameter.ostrack import parameters
        from lib.test.tracker.ostrack import OSTrack

        params = parameters(config_name)
        params.debug = 0
        if not Path(params.checkpoint).exists():
            raise FileNotFoundError(f"Missing checkpoint for runtime benchmark: {params.checkpoint}")
        return OSTrack(params, dataset_name="otb"), params.checkpoint


def synchronize() -> None:
    if torch.cuda.is_available():
        torch.cuda.synchronize()


def benchmark_model(
    project_root: Path,
    ostrack_root: Path,
    model_spec: dict,
    frames: List[np.ndarray],
    gt: List[List[float]],
    sequence: str,
    warmup_frames: int,
    repetitions: int,
) -> List[Dict[str, object]]:
    if not torch.cuda.is_available():
        raise RuntimeError("CUDA is unavailable; controlled GPU efficiency benchmark cannot run.")

    tracker, checkpoint = load_tracker(ostrack_root, model_spec["config"])
    gpu_name = torch.cuda.get_device_name(torch.cuda.current_device())
    measured_start = min(max(1, warmup_frames + 1), len(frames) - 1)
    rows: List[Dict[str, object]] = []

    for rep in range(1, repetitions + 1):
        torch.cuda.empty_cache()
        torch.cuda.reset_peak_memory_stats()

        synchronize()
        init_start = time.perf_counter()
        with torch.inference_mode():
            tracker.initialize(frames[0], {"init_bbox": gt[0]})
        synchronize()
        init_ms = (time.perf_counter() - init_start) * 1000.0

        with torch.inference_mode():
            for idx in range(1, measured_start):
                tracker.track(frames[idx], {})

        latencies: List[float] = []
        with torch.inference_mode():
            for idx in range(measured_start, len(frames)):
                synchronize()
                start = time.perf_counter()
                tracker.track(frames[idx], {})
                synchronize()
                latencies.append((time.perf_counter() - start) * 1000.0)

        if not latencies:
            raise ValueError("No measured frames after warm-up; reduce --warmup_frames.")

        mean_ms = statistics.fmean(latencies)
        std_ms = statistics.pstdev(latencies) if len(latencies) > 1 else 0.0
        rows.append(
            {
                "model_label": model_spec["model_label"],
                "config": model_spec["config"],
                "measurement_type": "controlled_runtime",
                "repetition": rep,
                "gpu_name": gpu_name,
                "torch_version": torch.__version__,
                "cuda_version": torch.version.cuda or "",
                "sequence": sequence,
                "frames": len(latencies),
                "warmup_frames": measured_start - 1,
                "initialization_ms": f"{init_ms:.6f}",
                "mean_latency_ms": f"{mean_ms:.6f}",
                "median_latency_ms": f"{statistics.median(latencies):.6f}",
                "latency_std_ms": f"{std_ms:.6f}",
                "fps": f"{1000.0 / mean_ms:.6f}",
                "peak_allocated_memory_mb": f"{torch.cuda.max_memory_allocated() / (1024 * 1024):.6f}",
                "peak_reserved_memory_mb": f"{torch.cuda.max_memory_reserved() / (1024 * 1024):.6f}",
                "provenance": "controlled_same_gpu_runtime",
                "notes": f"checkpoint={checkpoint}; timestamp={datetime.now(timezone.utc).isoformat()}",
            }
        )

    aggregate = aggregate_rows(rows, model_spec, sequence, gpu_name, len(frames), measured_start - 1)
    rows.append(aggregate)
    return rows


def aggregate_rows(
    rows: List[Dict[str, object]],
    model_spec: dict,
    sequence: str,
    gpu_name: str,
    frame_count: int,
    warmup_frames: int,
) -> Dict[str, object]:
    def vals(key: str) -> List[float]:
        return [float(r[key]) for r in rows if r.get(key) not in ("", None)]

    mean_latency = statistics.fmean(vals("mean_latency_ms"))
    return {
        "model_label": model_spec["model_label"],
        "config": model_spec["config"],
        "measurement_type": "controlled_runtime_aggregate",
        "repetition": "aggregate",
        "gpu_name": gpu_name,
        "torch_version": torch.__version__,
        "cuda_version": torch.version.cuda or "",
        "sequence": sequence,
        "frames": frame_count - 1 - warmup_frames,
        "warmup_frames": warmup_frames,
        "initialization_ms": f"{statistics.fmean(vals('initialization_ms')):.6f}",
        "mean_latency_ms": f"{mean_latency:.6f}",
        "median_latency_ms": f"{statistics.fmean(vals('median_latency_ms')):.6f}",
        "latency_std_ms": f"{statistics.fmean(vals('latency_std_ms')):.6f}",
        "fps": f"{1000.0 / mean_latency:.6f}",
        "peak_allocated_memory_mb": f"{max(vals('peak_allocated_memory_mb')):.6f}",
        "peak_reserved_memory_mb": f"{max(vals('peak_reserved_memory_mb')):.6f}",
        "provenance": "controlled_same_gpu_runtime",
        "notes": "aggregate_over_repetitions",
    }


def write_rows(path: Path, rows: List[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    exists = path.exists()
    with path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        if not exists:
            writer.writeheader()
        for row in rows:
            writer.writerow({col: row.get(col, "") for col in CSV_COLUMNS})


def check_only(project_root: Path, bench_cfg: dict, args) -> int:
    ostrack_root = project_root / bench_cfg["ostrack_root"]
    otb_root = Path(args.otb_root or bench_cfg["otb_root"])
    sequence = args.sequence or bench_cfg["sequence"]
    frames, gt = sequence_paths(otb_root, sequence)
    print(f"Benchmark config OK: {args.benchmark_config}")
    print(f"OSTrack root: {ostrack_root}")
    print(f"Sequence: {sequence}, frames={len(frames)}, gt={len(gt)}")
    print(f"Warm-up frames: {args.warmup_frames or bench_cfg['warmup_frames']}")
    print(f"Repetitions: {args.repetitions or bench_cfg['repetitions']}")
    for spec in [bench_cfg["baseline"], bench_cfg["final_method"]]:
        cfg_path = ostrack_root / "experiments" / "ostrack" / f"{spec['config']}.yaml"
        print(f"Config exists: {cfg_path.exists()} {cfg_path}")
    print(f"CUDA available for real benchmark: {torch.cuda.is_available()}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--benchmark_config", required=True)
    parser.add_argument("--baseline_config", default=None)
    parser.add_argument("--test_config", default=None)
    parser.add_argument("--otb_root", default=None)
    parser.add_argument("--sequence", default=None)
    parser.add_argument("--warmup_frames", type=int, default=None)
    parser.add_argument("--repetitions", type=int, default=None)
    parser.add_argument("--output_csv", default=None)
    parser.add_argument("--check_only", action="store_true")
    args = parser.parse_args()

    project_root = Path.cwd()
    bench_cfg = load_json(project_root / args.benchmark_config)
    if args.baseline_config:
        bench_cfg["baseline"]["config"] = args.baseline_config
    if args.test_config:
        bench_cfg["final_method"]["config"] = args.test_config

    if args.check_only:
        return check_only(project_root, bench_cfg, args)

    ostrack_root = (project_root / bench_cfg["ostrack_root"]).resolve()
    otb_root = Path(args.otb_root or bench_cfg["otb_root"])
    sequence = args.sequence or bench_cfg["sequence"]
    warmup = int(args.warmup_frames or bench_cfg["warmup_frames"])
    repetitions = int(args.repetitions or bench_cfg["repetitions"])
    output_csv = project_root / (args.output_csv or bench_cfg["output_csv"])

    frame_paths, gt = sequence_paths(otb_root, sequence)
    frames = read_rgb_frames(frame_paths)
    all_rows: List[Dict[str, object]] = []
    for spec in [bench_cfg["baseline"], bench_cfg["final_method"]]:
        all_rows.extend(benchmark_model(project_root, ostrack_root, spec, frames, gt, sequence, warmup, repetitions))
    write_rows(output_csv, all_rows)
    print(f"Wrote controlled benchmark rows: {output_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
