#!/usr/bin/env python3
"""Verify the Paper Freeze V1 efficiency benchmark package without running inference."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Dict, Iterable, List


REQUIRED_COLUMNS = [
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


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def parse_time_file(path: Path) -> Dict[str, object]:
    values: List[float] = []
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            values.append(float(line.split()[0]))
        except ValueError:
            continue
    fps = ""
    if values:
        total = sum(values)
        if total > 0:
            fps = len(values) / total
    return {"path": str(path), "entries": len(values), "apparent_fps": fps}


def audit_time_files(roots: Iterable[Path]) -> List[Dict[str, object]]:
    rows: List[Dict[str, object]] = []
    seen = set()
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*_time.txt"):
            if path in seen:
                continue
            seen.add(path)
            rows.append(parse_time_file(path))
    return rows


def validate_csv(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Missing efficiency result CSV: {path}")
    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        missing = [col for col in REQUIRED_COLUMNS if col not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(f"{path} is missing required columns: {missing}")
        rows = list(reader)
    if not rows:
        raise ValueError(f"{path} has no rows; run collect_ostrack_complexity.py first")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--benchmark_config", default="configs/paper_efficiency_benchmark.json")
    args = parser.parse_args()

    project_root = Path.cwd()
    cfg = load_json(project_root / args.benchmark_config)
    ostrack_root = project_root / cfg["ostrack_root"]
    output_csv = project_root / cfg["output_csv"]

    required = [
        project_root / args.benchmark_config,
        project_root / "scripts" / "benchmark_ostrack_efficiency.py",
        project_root / "scripts" / "collect_ostrack_complexity.py",
        ostrack_root / "experiments" / "ostrack" / f"{cfg['baseline']['config']}.yaml",
        ostrack_root / "experiments" / "ostrack" / f"{cfg['final_method']['config']}.yaml",
    ]
    for path in required:
        if not path.exists():
            raise FileNotFoundError(f"Missing required file: {path}")

    validate_csv(output_csv)
    timing_rows = audit_time_files(project_root / Path(root) for root in cfg.get("historical_time_roots", []))
    if str(project_root / "scripts") not in sys.path:
        sys.path.insert(0, str(project_root / "scripts"))
    from benchmark_ostrack_efficiency import resolve_cuda_device, run_check_workers

    cuda_resolution = resolve_cuda_device(require_cuda=False)
    worker_args = SimpleNamespace(
        benchmark_config=args.benchmark_config,
        otb_root=None,
        sequence=None,
        warmup_frames=None,
        repetitions=None,
    )
    provenance_rows = run_check_workers(project_root, cfg, worker_args)

    print("Efficiency benchmark setup verified.")
    print(f"Result table: {output_csv}")
    print(f"CUDA_VISIBLE_DEVICES: {cuda_resolution.cuda_visible_devices}")
    print(f"SLURM_LOCALID: {cuda_resolution.slurm_localid}")
    print(f"SLURM_GPUS_ON_NODE: {cuda_resolution.slurm_gpus_on_node}")
    print(f"Logical CUDA device count: {cuda_resolution.device_count}")
    print(f"Selected logical CUDA index: {cuda_resolution.logical_index}")
    print(f"GPU name: {cuda_resolution.gpu_name}")
    for row in provenance_rows:
        print("")
        print(f"Model: {row['model_label']}")
        print(f"  config: {row['config']}")
        print(f"  TEST.EPOCH: {row['test_epoch']}")
        print(f"  RGSSB enabled: {row['rgssb_enabled']}")
        print(f"  checkpoint: {row['checkpoint']}")
        print(f"  checkpoint exists: {row['checkpoint_exists']}")
        print(f"  total parameters: {row['total_params']}")
        print(f"  expected parameters: {row['expected_total_params']}")
        print(f"  provenance validation result: {row['provenance_valid']}")
    print(f"Historical timing files found: {len(timing_rows)}")
    if timing_rows:
        sample = timing_rows[:5]
        for row in sample:
            fps = row["apparent_fps"]
            fps_text = "" if fps == "" else f"{fps:.3f}"
            print(f"  {row['path']} entries={row['entries']} apparent_fps={fps_text}")
    print("Historical timing audit conclusion: not paper-ready unless hardware provenance matches.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
