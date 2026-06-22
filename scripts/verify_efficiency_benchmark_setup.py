#!/usr/bin/env python3
"""Verify the Paper Freeze V1 efficiency benchmark package without running inference."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
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

    print("Efficiency benchmark setup verified.")
    print(f"Result table: {output_csv}")
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
