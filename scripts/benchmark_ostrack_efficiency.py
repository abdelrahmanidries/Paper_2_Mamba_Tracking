#!/usr/bin/env python3
"""Controlled same-GPU runtime benchmark for OSTrack Paper Freeze V1 models."""

from __future__ import annotations

import argparse
import csv
import importlib
import json
import os
import statistics
import subprocess
import sys
import tempfile
import time
from contextlib import contextmanager
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Mapping, Optional, Sequence, Tuple

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


@dataclass(frozen=True)
class CudaDeviceResolution:
    device: Optional[torch.device]
    logical_index: Optional[int]
    gpu_name: str
    device_count: int
    cuda_visible_devices: str
    slurm_localid: str
    slurm_gpus_on_node: str


def resolve_cuda_device(
    requested_index: int = 0,
    *,
    require_cuda: bool = True,
    torch_module=torch,
    env: Optional[Mapping[str, str]] = None,
) -> CudaDeviceResolution:
    """Resolve a PyTorch logical CUDA device for Slurm/MIG-safe benchmarking.

    CUDA_VISIBLE_DEVICES may contain physical ids, remapped ids, or MIG UUIDs.
    PyTorch exposes only the process-visible logical namespace, so this function
    deliberately selects logical index 0 by default and never interprets the
    CUDA_VISIBLE_DEVICES token as a PyTorch device index.
    """
    env = env or os.environ
    cuda_visible = env.get("CUDA_VISIBLE_DEVICES", "")
    slurm_localid = env.get("SLURM_LOCALID", "")
    slurm_gpus = env.get("SLURM_GPUS_ON_NODE", "")

    if not torch_module.cuda.is_available():
        if require_cuda:
            raise RuntimeError(
                "CUDA is unavailable; controlled GPU efficiency benchmark requires a CUDA device. "
                f"CUDA_VISIBLE_DEVICES={cuda_visible!r}"
            )
        return CudaDeviceResolution(
            device=None,
            logical_index=None,
            gpu_name="cuda_unavailable",
            device_count=0,
            cuda_visible_devices=cuda_visible,
            slurm_localid=slurm_localid,
            slurm_gpus_on_node=slurm_gpus,
        )

    device_count = int(torch_module.cuda.device_count())
    if device_count <= 0:
        raise RuntimeError(
            "CUDA reports available but PyTorch sees zero usable logical devices. "
            f"CUDA_VISIBLE_DEVICES={cuda_visible!r}; SLURM_LOCALID={slurm_localid!r}; "
            f"SLURM_GPUS_ON_NODE={slurm_gpus!r}"
        )
    if requested_index < 0 or requested_index >= device_count:
        raise RuntimeError(
            f"Requested logical CUDA device {requested_index} is invalid for "
            f"device_count={device_count}. CUDA_VISIBLE_DEVICES={cuda_visible!r}"
        )

    try:
        torch_module.cuda.set_device(requested_index)
        device = torch_module.device("cuda", requested_index)
        props = torch_module.cuda.get_device_properties(requested_index)
    except Exception as exc:  # pragma: no cover - exercised through mocked tests
        raise RuntimeError(
            f"Could not initialize logical CUDA device {requested_index}. "
            f"device_count={device_count}; CUDA_VISIBLE_DEVICES={cuda_visible!r}; "
            f"SLURM_LOCALID={slurm_localid!r}; SLURM_GPUS_ON_NODE={slurm_gpus!r}"
        ) from exc

    gpu_name = getattr(props, "name", None) or str(props)
    return CudaDeviceResolution(
        device=device,
        logical_index=requested_index,
        gpu_name=gpu_name,
        device_count=device_count,
        cuda_visible_devices=cuda_visible,
        slurm_localid=slurm_localid,
        slurm_gpus_on_node=slurm_gpus,
    )


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


def model_specs(bench_cfg: dict) -> List[Tuple[str, dict]]:
    return [("baseline", bench_cfg["baseline"]), ("final_method", bench_cfg["final_method"])]


def checkpoint_path(project_root: Path, model_spec: dict) -> Path:
    return (project_root / model_spec["checkpoint"]).resolve()


def config_yaml_path(project_root: Path, bench_cfg: dict, model_spec: dict) -> Path:
    return (
        project_root
        / bench_cfg["ostrack_root"]
        / "experiments"
        / "ostrack"
        / f"{model_spec['config']}.yaml"
    ).resolve()


def worker_python_command() -> List[str]:
    if os.environ.get("CONDA_DEFAULT_ENV") == "ostrack":
        return [sys.executable]
    return ["conda", "run", "-n", "ostrack", "python"]


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


def count_params_by_prefix(model, prefix: str) -> int:
    return sum(p.numel() for name, p in model.named_parameters() if name.startswith(prefix))


def validate_model_static_provenance(
    project_root: Path,
    bench_cfg: dict,
    model_key: str,
    *,
    actual_epoch: int,
    actual_rgssb_enabled: bool,
    total_params: int,
    rgssb_params: int,
    has_active_rgssb: bool,
    require_checkpoint: bool,
) -> Dict[str, object]:
    model_spec = bench_cfg[model_key]
    config_path = config_yaml_path(project_root, bench_cfg, model_spec)
    explicit_checkpoint = checkpoint_path(project_root, model_spec)
    checkpoint_exists = explicit_checkpoint.exists()

    if require_checkpoint and not checkpoint_exists:
        raise FileNotFoundError(f"Missing explicit checkpoint: {explicit_checkpoint}")
    if actual_epoch != int(model_spec["expected_test_epoch"]):
        raise RuntimeError(
            f"{model_spec['config']} TEST.EPOCH mismatch: "
            f"expected {model_spec['expected_test_epoch']}, got {actual_epoch}"
        )
    if actual_rgssb_enabled != bool(model_spec["expected_rgssb_enabled"]):
        raise RuntimeError(
            f"{model_spec['config']} RGSSB enabled mismatch: "
            f"expected {model_spec['expected_rgssb_enabled']}, got {actual_rgssb_enabled}"
        )

    expected_total = int(model_spec["expected_total_params"])
    if total_params != expected_total:
        raise RuntimeError(
            f"{model_spec['config']} parameter-count mismatch: expected {expected_total}, got {total_params}"
        )
    if bool(model_spec["expected_rgssb_enabled"]):
        if not has_active_rgssb:
            raise RuntimeError(f"{model_spec['config']} expected an active rgssb module, but none was built")
        if rgssb_params != 2079936:
            raise RuntimeError(f"{model_spec['config']} RG-SSB parameter mismatch: expected 2079936, got {rgssb_params}")
        if "ep0300" in explicit_checkpoint.name:
            raise RuntimeError(f"{model_spec['config']} resolved to an invalid final checkpoint: {explicit_checkpoint}")
    else:
        if has_active_rgssb or rgssb_params != 0:
            raise RuntimeError(f"{model_spec['config']} baseline unexpectedly built RG-SSB parameters")

    return {
        "model_key": model_key,
        "model_label": model_spec["model_label"],
        "config": model_spec["config"],
        "config_yaml": str(config_path),
        "test_epoch": actual_epoch,
        "expected_test_epoch": int(model_spec["expected_test_epoch"]),
        "rgssb_enabled": actual_rgssb_enabled,
        "expected_rgssb_enabled": bool(model_spec["expected_rgssb_enabled"]),
        "checkpoint": str(explicit_checkpoint),
        "checkpoint_exists": checkpoint_exists,
        "total_params": total_params,
        "expected_total_params": expected_total,
        "rgssb_params": rgssb_params,
        "provenance_valid": True,
    }


def validate_model_provenance(
    project_root: Path,
    bench_cfg: dict,
    model_key: str,
    *,
    require_checkpoint: bool,
) -> Dict[str, object]:
    model_spec = bench_cfg[model_key]
    ostrack_root = (project_root / bench_cfg["ostrack_root"]).resolve()
    config_path = config_yaml_path(project_root, bench_cfg, model_spec)
    if not config_path.exists():
        raise FileNotFoundError(f"Missing OSTrack config YAML: {config_path}")

    if str(ostrack_root) not in sys.path:
        sys.path.insert(0, str(ostrack_root))

    with pushd(ostrack_root):
        reset_ostrack_config_modules()
        from lib.config.ostrack.config import cfg, update_config_from_file
        from lib.models.ostrack import build_ostrack

        update_config_from_file(str(config_path))
        actual_epoch = int(cfg.TEST.EPOCH)
        actual_rgssb_enabled = bool(getattr(getattr(cfg.MODEL, "RGSSB", None), "ENABLE", False))
        model = build_ostrack(cfg, training=False)
        total_params = sum(p.numel() for p in model.parameters())
        rgssb_params = count_params_by_prefix(model, "rgssb")
        has_active_rgssb = bool(getattr(model, "rgssb", None) is not None)

    return validate_model_static_provenance(
        project_root,
        bench_cfg,
        model_key,
        actual_epoch=actual_epoch,
        actual_rgssb_enabled=actual_rgssb_enabled,
        total_params=total_params,
        rgssb_params=rgssb_params,
        has_active_rgssb=has_active_rgssb,
        require_checkpoint=require_checkpoint,
    )


def load_tracker(ostrack_root: Path, model_spec: dict, explicit_checkpoint: Path):
    if str(ostrack_root) not in sys.path:
        sys.path.insert(0, str(ostrack_root))
    with pushd(ostrack_root):
        reset_ostrack_config_modules()
        from lib.test.parameter.ostrack import parameters
        from lib.test.tracker.ostrack import OSTrack

        params = parameters(model_spec["config"])
        params.debug = 0
        inferred_checkpoint = Path(params.checkpoint)
        params.checkpoint = str(explicit_checkpoint)
        if not explicit_checkpoint.exists():
            raise FileNotFoundError(f"Missing explicit checkpoint for runtime benchmark: {explicit_checkpoint}")
        if int(params.cfg.TEST.EPOCH) != int(model_spec["expected_test_epoch"]):
            raise RuntimeError(
                f"Tracker parameter TEST.EPOCH mismatch for {model_spec['config']}: "
                f"expected {model_spec['expected_test_epoch']}, got {params.cfg.TEST.EPOCH}; "
                f"inferred checkpoint was {inferred_checkpoint}"
            )
        return OSTrack(params, dataset_name="otb"), params.checkpoint


def synchronize(device: torch.device) -> None:
    if torch.cuda.is_available():
        torch.cuda.synchronize(device)


def benchmark_model(
    project_root: Path,
    ostrack_root: Path,
    model_spec: dict,
    frames: List[np.ndarray],
    gt: List[List[float]],
    sequence: str,
    warmup_frames: int,
    repetitions: int,
    cuda_resolution: CudaDeviceResolution,
) -> List[Dict[str, object]]:
    if cuda_resolution.device is None or cuda_resolution.logical_index is None:
        raise RuntimeError("CUDA device was not resolved for the controlled benchmark.")

    explicit_checkpoint = checkpoint_path(project_root, model_spec)
    tracker, checkpoint = load_tracker(ostrack_root, model_spec, explicit_checkpoint)
    gpu_name = cuda_resolution.gpu_name
    device = cuda_resolution.device
    logical_index = cuda_resolution.logical_index
    measured_start = min(max(1, warmup_frames + 1), len(frames) - 1)
    rows: List[Dict[str, object]] = []

    for rep in range(1, repetitions + 1):
        torch.cuda.empty_cache()
        torch.cuda.reset_peak_memory_stats(logical_index)

        synchronize(device)
        init_start = time.perf_counter()
        with torch.inference_mode():
            tracker.initialize(frames[0], {"init_bbox": gt[0]})
        synchronize(device)
        init_ms = (time.perf_counter() - init_start) * 1000.0

        with torch.inference_mode():
            for idx in range(1, measured_start):
                tracker.track(frames[idx], {})

        latencies: List[float] = []
        with torch.inference_mode():
            for idx in range(measured_start, len(frames)):
                synchronize(device)
                start = time.perf_counter()
                tracker.track(frames[idx], {})
                synchronize(device)
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
                "peak_allocated_memory_mb": f"{torch.cuda.max_memory_allocated(logical_index) / (1024 * 1024):.6f}",
                "peak_reserved_memory_mb": f"{torch.cuda.max_memory_reserved(logical_index) / (1024 * 1024):.6f}",
                "provenance": "controlled_same_gpu_runtime",
                "notes": (
                    f"checkpoint={checkpoint}; logical_cuda_device={logical_index}; "
                    f"CUDA_VISIBLE_DEVICES={cuda_resolution.cuda_visible_devices}; "
                    f"timestamp={datetime.now(timezone.utc).isoformat()}"
                ),
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


def append_rows_atomically(path: Path, rows: List[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = path.read_text(encoding="utf-8") if path.exists() else ""
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    try:
        with tmp_path.open("w", newline="", encoding="utf-8") as f:
            if existing:
                f.write(existing)
                if not existing.endswith("\n"):
                    f.write("\n")
                writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
            else:
                writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
                writer.writeheader()
            for row in rows:
                writer.writerow({col: row.get(col, "") for col in CSV_COLUMNS})
        tmp_path.replace(path)
    finally:
        if tmp_path.exists():
            tmp_path.unlink()


def run_worker(
    project_root: Path,
    args,
    *,
    model_key: str,
    mode: str,
    output_path: Path,
) -> None:
    cmd = [
        *worker_python_command(),
        str(project_root / "scripts" / "benchmark_ostrack_efficiency.py"),
        "--benchmark_config",
        args.benchmark_config,
        "--_worker_mode",
        mode,
        "--_worker_model_key",
        model_key,
        "--_worker_output",
        str(output_path),
    ]
    if args.otb_root:
        cmd.extend(["--otb_root", args.otb_root])
    if args.sequence:
        cmd.extend(["--sequence", args.sequence])
    if args.warmup_frames is not None:
        cmd.extend(["--warmup_frames", str(args.warmup_frames)])
    if args.repetitions is not None:
        cmd.extend(["--repetitions", str(args.repetitions)])
    completed = subprocess.run(cmd, cwd=project_root, check=False)
    if completed.returncode != 0:
        raise RuntimeError(f"{mode} worker failed for {model_key} with exit code {completed.returncode}")


def load_worker_output(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def run_check_workers(project_root: Path, bench_cfg: dict, args) -> List[dict]:
    outputs: List[dict] = []
    with tempfile.TemporaryDirectory(prefix="paper_efficiency_check_") as tmp:
        tmp_dir = Path(tmp)
        for model_key, _ in model_specs(bench_cfg):
            output = tmp_dir / f"{model_key}.json"
            run_worker(project_root, args, model_key=model_key, mode="check_model", output_path=output)
            outputs.append(load_worker_output(output))
    return outputs


def run_benchmark_workers(project_root: Path, bench_cfg: dict, args) -> List[Dict[str, object]]:
    all_rows: List[Dict[str, object]] = []
    with tempfile.TemporaryDirectory(prefix="paper_efficiency_runtime_") as tmp:
        tmp_dir = Path(tmp)
        for model_key, _ in model_specs(bench_cfg):
            output = tmp_dir / f"{model_key}.json"
            run_worker(project_root, args, model_key=model_key, mode="benchmark_model", output_path=output)
            worker_result = load_worker_output(output)
            all_rows.extend(worker_result["rows"])
    return all_rows


def worker_check_model(project_root: Path, bench_cfg: dict, model_key: str, output_path: Path) -> int:
    provenance = validate_model_provenance(project_root, bench_cfg, model_key, require_checkpoint=False)
    output_path.write_text(json.dumps(provenance, indent=2, sort_keys=True), encoding="utf-8")
    return 0


def worker_benchmark_model(project_root: Path, bench_cfg: dict, args) -> int:
    model_key = args._worker_model_key
    provenance = validate_model_provenance(project_root, bench_cfg, model_key, require_checkpoint=True)
    cuda_resolution = resolve_cuda_device(require_cuda=True)
    otb_root = Path(args.otb_root or bench_cfg["otb_root"])
    sequence = args.sequence or bench_cfg["sequence"]
    warmup = int(args.warmup_frames or bench_cfg["warmup_frames"])
    repetitions = int(args.repetitions or bench_cfg["repetitions"])
    frame_paths, gt = sequence_paths(otb_root, sequence)
    frames = read_rgb_frames(frame_paths)
    rows = benchmark_model(
        project_root,
        (project_root / bench_cfg["ostrack_root"]).resolve(),
        bench_cfg[model_key],
        frames,
        gt,
        sequence,
        warmup,
        repetitions,
        cuda_resolution,
    )
    args._worker_output.write_text(
        json.dumps({"provenance": provenance, "rows": rows}, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    return 0


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
    provenance_rows = run_check_workers(project_root, bench_cfg, args)
    for row in provenance_rows:
        print("")
        print(f"Model: {row['model_label']}")
        print(f"  config: {row['config']}")
        print(f"  config YAML: {row['config_yaml']}")
        print(f"  TEST.EPOCH: {row['test_epoch']}")
        print(f"  RGSSB enabled: {row['rgssb_enabled']}")
        print(f"  checkpoint: {row['checkpoint']}")
        print(f"  checkpoint exists: {row['checkpoint_exists']}")
        print(f"  total parameters: {row['total_params']}")
        print(f"  expected parameters: {row['expected_total_params']}")
        print(f"  RG-SSB parameters: {row['rgssb_params']}")
        print(f"  provenance validation result: {row['provenance_valid']}")
    if provenance_rows[0]["total_params"] == provenance_rows[1]["total_params"]:
        raise RuntimeError("Baseline and final method resolved to the same parameter count; provenance isolation failed.")
    if provenance_rows[0]["rgssb_enabled"] == provenance_rows[1]["rgssb_enabled"]:
        raise RuntimeError("Baseline and final method resolved to the same RGSSB state; provenance isolation failed.")
    cuda_resolution = resolve_cuda_device(require_cuda=False)
    print(f"CUDA available for real benchmark: {torch.cuda.is_available()}")
    print(f"CUDA_VISIBLE_DEVICES: {cuda_resolution.cuda_visible_devices}")
    print(f"SLURM_LOCALID: {cuda_resolution.slurm_localid}")
    print(f"SLURM_GPUS_ON_NODE: {cuda_resolution.slurm_gpus_on_node}")
    print(f"Logical CUDA device count: {cuda_resolution.device_count}")
    print(f"Selected logical CUDA index: {cuda_resolution.logical_index}")
    print(f"GPU name: {cuda_resolution.gpu_name}")
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
    parser.add_argument("--_worker_mode", choices=["check_model", "benchmark_model"], default=None)
    parser.add_argument("--_worker_model_key", choices=["baseline", "final_method"], default=None)
    parser.add_argument("--_worker_output", type=Path, default=None)
    args = parser.parse_args()

    project_root = Path.cwd()
    bench_cfg = load_json(project_root / args.benchmark_config)
    if args.baseline_config:
        bench_cfg["baseline"]["config"] = args.baseline_config
    if args.test_config:
        bench_cfg["final_method"]["config"] = args.test_config

    if args._worker_mode:
        if args._worker_model_key is None or args._worker_output is None:
            raise RuntimeError("Worker mode requires --_worker_model_key and --_worker_output")
        if args._worker_mode == "check_model":
            return worker_check_model(project_root, bench_cfg, args._worker_model_key, args._worker_output)
        if args._worker_mode == "benchmark_model":
            return worker_benchmark_model(project_root, bench_cfg, args)

    if args.check_only:
        return check_only(project_root, bench_cfg, args)

    output_csv = project_root / (args.output_csv or bench_cfg["output_csv"])
    all_rows = run_benchmark_workers(project_root, bench_cfg, args)
    append_rows_atomically(output_csv, all_rows)
    print(f"Wrote controlled benchmark rows: {output_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
