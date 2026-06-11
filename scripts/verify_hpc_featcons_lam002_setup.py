#!/usr/bin/env python3
"""Verify the HPC RG-SSB feature-consistency lambda 0.02 setup.

This script builds the model and applies freeze mode only. It does not run
training, evaluation, or dataloaders.
"""

from __future__ import annotations

import os
import sys
import types
from pathlib import Path


def _stub_optional_coco_import() -> None:
    if "pycocotools" not in sys.modules:
        sys.modules["pycocotools"] = types.ModuleType("pycocotools")
    pycocotools_module = sys.modules["pycocotools"]
    if "pycocotools.coco" not in sys.modules:
        coco_module = types.ModuleType("pycocotools.coco")

        class _COCO:
            def __init__(self, *args, **kwargs):
                raise RuntimeError("COCO is not used by the HPC setup verifier.")

        coco_module.COCO = _COCO
        sys.modules["pycocotools.coco"] = coco_module
        pycocotools_module.coco = coco_module
    if "pycocotools.mask" not in sys.modules:
        mask_module = types.ModuleType("pycocotools.mask")
        sys.modules["pycocotools.mask"] = mask_module
        pycocotools_module.mask = mask_module


def _assert(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(f"Verification failed for {name}")


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    ostrack_root = repo_root / "external" / "OSTrack"
    config_name = "vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_degraded_hpc_featcons_lam002"
    config_path = ostrack_root / "experiments" / "ostrack" / f"{config_name}.yaml"
    cycle_config = repo_root / "configs" / "rgssb_experiment_cycle_hpc_featcons_lam002.json"
    train_slurm = repo_root / "scripts" / "hpc" / "slurm_rgssb_featcons_lam002_train.sh"
    eval_slurm = repo_root / "scripts" / "hpc" / "slurm_rgssb_featcons_lam002_eval.sh"
    hpc_readme = repo_root / "scripts" / "hpc" / "README_rgssb_hpc.md"

    if not config_path.is_file():
        raise FileNotFoundError(f"Missing HPC config: {config_path}")
    for path in [cycle_config, train_slurm, eval_slurm, hpc_readme]:
        if not path.is_file():
            raise FileNotFoundError(f"Missing HPC support file: {path}")

    os.chdir(ostrack_root)
    sys.path.insert(0, str(ostrack_root))
    _stub_optional_coco_import()

    from lib.config.ostrack.config import cfg, update_config_from_file
    from lib.models.ostrack import build_ostrack
    from lib.train.freeze import apply_freeze_mode

    update_config_from_file(str(config_path))

    expected_types = ["motion_blur", "low_resolution", "gaussian_noise"]
    _assert("MODEL.RGSSB.ENABLE", cfg.MODEL.RGSSB.ENABLE is True)
    _assert("TRAIN.FREEZE_MODE", cfg.TRAIN.FREEZE_MODE == "rgssb_head")
    _assert("TRAIN.FEATURE_CONSISTENCY.ENABLE", cfg.TRAIN.FEATURE_CONSISTENCY.ENABLE is True)
    _assert("TRAIN.FEATURE_CONSISTENCY.WEIGHT", abs(float(cfg.TRAIN.FEATURE_CONSISTENCY.WEIGHT) - 0.02) < 1e-12)
    response_cfg = getattr(cfg.TRAIN, "RESPONSE_CONSISTENCY", None)
    _assert(
        "TRAIN.RESPONSE_CONSISTENCY disabled",
        response_cfg is None or bool(getattr(response_cfg, "ENABLE", False)) is False,
    )
    if response_cfg is not None:
        _assert("TRAIN.RESPONSE_CONSISTENCY.WEIGHT", float(response_cfg.WEIGHT) == 0.0)
    _assert("DATA.TRAIN.DATASETS_NAME", list(cfg.DATA.TRAIN.DATASETS_NAME) == ["LASOT"])
    _assert("DATA.TRAIN.DATASETS_RATIO", list(cfg.DATA.TRAIN.DATASETS_RATIO) == [1])
    _assert("DATA.VAL.DATASETS_NAME", list(cfg.DATA.VAL.DATASETS_NAME) == ["LASOT"])
    _assert("DATA.VAL.DATASETS_RATIO", list(cfg.DATA.VAL.DATASETS_RATIO) == [1])
    _assert("DATA.DEGRADATION.ENABLE", cfg.DATA.DEGRADATION.ENABLE is True)
    _assert("DATA.DEGRADATION.PROBABILITY", float(cfg.DATA.DEGRADATION.PROBABILITY) == 1.0)
    _assert("DATA.DEGRADATION.APPLY_TO", cfg.DATA.DEGRADATION.APPLY_TO == "search_only")
    _assert("DATA.DEGRADATION.TYPES", list(cfg.DATA.DEGRADATION.TYPES) == expected_types)
    _assert("TRAIN.BATCH_SIZE", int(cfg.TRAIN.BATCH_SIZE) == 8)
    _assert("TRAIN.NUM_WORKER", int(cfg.TRAIN.NUM_WORKER) == 8)
    _assert("TRAIN.EPOCH", int(cfg.TRAIN.EPOCH) == 10)
    _assert("TEST.EPOCH", int(cfg.TEST.EPOCH) == 10)

    model = build_ostrack(cfg, training=True)
    trainable_params, frozen_params, trainable_names = apply_freeze_mode(model, cfg)
    total_params = trainable_params + frozen_params
    rgssb_trainable = [name for name in trainable_names if name.startswith("rgssb")]
    head_trainable = [name for name in trainable_names if name.startswith("box_head")]
    non_allowed = [
        name for name in trainable_names
        if not (name.startswith("rgssb") or name.startswith("box_head"))
    ]
    backbone_trainable = [
        name for name, param in model.named_parameters()
        if name.startswith("backbone") and param.requires_grad
    ]
    if not rgssb_trainable:
        raise AssertionError("No rgssb.* parameters are trainable.")
    if not head_trainable:
        raise AssertionError("No box_head.* parameters are trainable.")
    if non_allowed:
        raise AssertionError(f"Unexpected trainable parameters: {non_allowed[:20]}")
    if backbone_trainable:
        raise AssertionError(f"Backbone parameters must be frozen: {backbone_trainable[:20]}")

    print(f"config: {config_path}")
    print(f"cycle_config: {cycle_config}")
    print(f"train_slurm: {train_slurm}")
    print(f"eval_slurm: {eval_slurm}")
    print(f"hpc_readme: {hpc_readme}")
    print(f"MODEL.RGSSB.ENABLE: {cfg.MODEL.RGSSB.ENABLE}")
    print(f"TRAIN.FREEZE_MODE: {cfg.TRAIN.FREEZE_MODE}")
    print(f"TRAIN.FEATURE_CONSISTENCY.WEIGHT: {cfg.TRAIN.FEATURE_CONSISTENCY.WEIGHT}")
    print(f"TRAIN.RESPONSE_CONSISTENCY.ENABLE: {getattr(response_cfg, 'ENABLE', False) if response_cfg is not None else False}")
    print(f"DATA.TRAIN.DATASETS_NAME: {list(cfg.DATA.TRAIN.DATASETS_NAME)}")
    print(f"DATA.TRAIN.SAMPLE_PER_EPOCH: {cfg.DATA.TRAIN.SAMPLE_PER_EPOCH}")
    print(f"DATA.VAL.SAMPLE_PER_EPOCH: {cfg.DATA.VAL.SAMPLE_PER_EPOCH}")
    print(f"TRAIN.BATCH_SIZE: {cfg.TRAIN.BATCH_SIZE}")
    print(f"TRAIN.EPOCH: {cfg.TRAIN.EPOCH}")
    print(f"TEST.EPOCH: {cfg.TEST.EPOCH}")
    print(f"total_params: {total_params}")
    print(f"trainable_params: {trainable_params}")
    print(f"frozen_params: {frozen_params}")
    print(f"rgssb_trainable_count: {len(rgssb_trainable)}")
    print(f"head_trainable_count: {len(head_trainable)}")
    print(f"backbone_trainable_count: {len(backbone_trainable)}")
    print("verification: HPC lambda 0.02 setup is ready for training submission after path edits")


if __name__ == "__main__":
    main()
