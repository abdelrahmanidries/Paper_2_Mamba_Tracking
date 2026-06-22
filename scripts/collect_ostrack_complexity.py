#!/usr/bin/env python3
"""Collect parameter-count complexity data for Paper Freeze V1 models."""

from __future__ import annotations

import argparse
import csv
import importlib
import importlib.util
import json
import os
import subprocess
import sys
import types
from contextlib import contextmanager
from pathlib import Path
from typing import Dict, Iterable, List, Optional


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


def install_optional_stubs() -> None:
    """Avoid optional import failures when building the model for counting."""
    if "easydict" not in sys.modules and importlib.util.find_spec("easydict") is None:
        easydict = types.ModuleType("easydict")

        class EasyDict(dict):
            def __init__(self, mapping=None, **kwargs):
                super().__init__()
                mapping = mapping or {}
                for key, value in dict(mapping, **kwargs).items():
                    if isinstance(value, dict) and not isinstance(value, EasyDict):
                        value = EasyDict(value)
                    self[key] = value

            def __getattr__(self, name):
                try:
                    return self[name]
                except KeyError as exc:
                    raise AttributeError(name) from exc

            def __setattr__(self, name, value):
                self[name] = value

            def __delattr__(self, name):
                try:
                    del self[name]
                except KeyError as exc:
                    raise AttributeError(name) from exc

        easydict.EasyDict = EasyDict
        sys.modules["easydict"] = easydict

    if "pycocotools" not in sys.modules:
        pycocotools = types.ModuleType("pycocotools")
        mask = types.ModuleType("pycocotools.mask")
        pycocotools.mask = mask
        sys.modules["pycocotools"] = pycocotools
        sys.modules["pycocotools.mask"] = mask


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def config_yaml_path(ostrack_root: Path, config_name: str) -> Path:
    return ostrack_root / "experiments" / "ostrack" / f"{config_name}.yaml"


def checkpoint_path(ostrack_root: Path, config_name: str, epoch: int) -> Path:
    return (
        ostrack_root
        / "output"
        / "checkpoints"
        / "train"
        / "ostrack"
        / config_name
        / f"OSTrack_ep{epoch:04d}.pth.tar"
    )


def reset_ostrack_config_modules() -> None:
    for name in list(sys.modules):
        if name == "lib.config.ostrack.config":
            importlib.reload(sys.modules[name])


def count_params_by_prefix(model, prefixes: Iterable[str]) -> int:
    prefixes = tuple(prefixes)
    return sum(p.numel() for name, p in model.named_parameters() if name.startswith(prefixes))


def collect_model_counts(project_root: Path, ostrack_root: Path, model_spec: dict) -> Dict[str, object]:
    import torch

    install_optional_stubs()
    abs_ostrack = (project_root / ostrack_root).resolve()
    if str(abs_ostrack) not in sys.path:
        sys.path.insert(0, str(abs_ostrack))

    config_name = model_spec["config"]
    yaml_path = config_yaml_path(abs_ostrack, config_name)
    if not yaml_path.exists():
        raise FileNotFoundError(f"Missing OSTrack config: {yaml_path}")

    with pushd(abs_ostrack):
        reset_ostrack_config_modules()
        from lib.config.ostrack.config import cfg, update_config_from_file
        from lib.models.ostrack import build_ostrack
        from lib.train.freeze import apply_freeze_mode

        update_config_from_file(str(yaml_path))
        model = build_ostrack(cfg, training=False)
        trainable_params, frozen_params, trainable_names = apply_freeze_mode(model, cfg)
        total_params = sum(p.numel() for p in model.parameters())
        backbone_params = count_params_by_prefix(model, ["backbone"])
        rgssb_params = count_params_by_prefix(model, ["rgssb"])
        box_head_params = count_params_by_prefix(model, ["box_head"])
        epoch = int(cfg.TEST.EPOCH)
        freeze_mode = getattr(cfg.TRAIN, "FREEZE_MODE", "none")

    ckpt = checkpoint_path(abs_ostrack, config_name, epoch)
    ckpt_size_mb: Optional[float] = None
    if ckpt.exists():
        ckpt_size_mb = ckpt.stat().st_size / (1024 * 1024)

    return {
        "model_label": model_spec["model_label"],
        "config": config_name,
        "measurement_type": "complexity",
        "repetition": "",
        "gpu_name": "",
        "torch_version": torch.__version__,
        "cuda_version": torch.version.cuda or "",
        "sequence": "",
        "frames": "",
        "warmup_frames": "",
        "initialization_ms": "",
        "mean_latency_ms": "",
        "median_latency_ms": "",
        "latency_std_ms": "",
        "fps": "",
        "peak_allocated_memory_mb": "",
        "peak_reserved_memory_mb": "",
        "total_params": total_params,
        "trainable_params": trainable_params,
        "frozen_params": frozen_params,
        "backbone_params": backbone_params,
        "rgssb_params": rgssb_params,
        "box_head_params": box_head_params,
        "checkpoint_size_mb": "" if ckpt_size_mb is None else f"{ckpt_size_mb:.6f}",
        "flops_or_macs": "unavailable",
        "provenance": "model_build_without_tracking",
        "notes": f"freeze_mode={freeze_mode}; trainable_tensors={len(trainable_names)}; checkpoint={ckpt}",
    }


def write_rows(path: Path, rows: List[Dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_COLUMNS)
        writer.writeheader()
        for row in rows:
            writer.writerow({col: row.get(col, "") for col in CSV_COLUMNS})


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--benchmark_config", required=True)
    parser.add_argument("--output_csv", default=None)
    args = parser.parse_args()

    if os.environ.get("OSTRACK_COMPLEXITY_REEXEC") != "1":
        try:
            env = os.environ.copy()
            env["OSTRACK_COMPLEXITY_REEXEC"] = "1"
            completed = subprocess.run(
                ["conda", "run", "-n", "ostrack", "python", __file__, *sys.argv[1:]],
                cwd=Path.cwd(),
                env=env,
                check=False,
            )
            return completed.returncode
        except FileNotFoundError:
            pass

    project_root = Path.cwd()
    bench_cfg = load_json(project_root / args.benchmark_config)
    ostrack_root = Path(bench_cfg["ostrack_root"])
    output_csv = Path(args.output_csv or bench_cfg["output_csv"])

    baseline = collect_model_counts(project_root, ostrack_root, bench_cfg["baseline"])
    final = collect_model_counts(project_root, ostrack_root, bench_cfg["final_method"])
    increase = int(final["total_params"]) - int(baseline["total_params"])
    final["notes"] = f"{final['notes']}; parameter_increase_vs_baseline={increase}"
    baseline["notes"] = f"{baseline['notes']}; parameter_increase_vs_baseline=0"

    write_rows(project_root / output_csv, [baseline, final])
    print(f"Wrote complexity table: {output_csv}")
    print(f"Baseline total params: {baseline['total_params']}")
    print(f"Final total params: {final['total_params']}")
    print(f"Parameter increase: {increase}")
    print("FLOPs/MACs: unavailable (no reliable tracer used for dynamic OSTrack path)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
