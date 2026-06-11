#!/usr/bin/env python3
"""Verify RG-SSB feature-consistency lambda sweep configs.

This verifier builds models and applies the configured freeze mode only. It does
not run training, evaluation, dataloaders, forward passes, or backward passes.
"""

from __future__ import annotations

import gc
import json
import os
import sys
import types
from pathlib import Path
from typing import Any


def _stub_optional_coco_import() -> None:
    if "pycocotools" not in sys.modules:
        sys.modules["pycocotools"] = types.ModuleType("pycocotools")
    pycocotools_module = sys.modules["pycocotools"]
    if "pycocotools.coco" not in sys.modules:
        coco_module = types.ModuleType("pycocotools.coco")

        class _COCO:
            def __init__(self, *args, **kwargs):
                raise RuntimeError("COCO is not used by the lambda-sweep verifier.")

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


def _load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as json_file:
        return json.load(json_file)


def _verify_cycle_config(path: Path, expected_config_name: str) -> None:
    if not path.is_file():
        raise FileNotFoundError(f"Missing cycle config: {path}")
    data = _load_json(path)
    _assert(f"{path.name} config_name", data.get("config_name") == expected_config_name)
    _assert(f"{path.name} train", data.get("train") is True)
    _assert(f"{path.name} eval", data.get("eval") is True)
    _assert(f"{path.name} overwrite_existing", data.get("overwrite_existing") is True)
    _assert(f"{path.name} sequences", data.get("sequences") == ["Car1", "David2", "Coke"])
    _assert(
        f"{path.name} conditions",
        data.get("conditions")
        == [
            {"degradation": "clean", "severity": "none", "seed": 0},
            {"degradation": "motion_blur", "severity": "medium", "seed": 42},
            {"degradation": "low_resolution", "severity": "medium", "seed": 42},
            {"degradation": "gaussian_noise", "severity": "medium", "seed": 42},
        ],
    )


def _verify_trainable_params(model, trainable_names: list[str]) -> tuple[int, int, int, list[str]]:
    rgssb_trainable = [name for name in trainable_names if name.startswith("rgssb")]
    head_trainable = [name for name in trainable_names if name.startswith("box_head")]
    non_allowed = [
        name
        for name in trainable_names
        if not (name.startswith("rgssb") or name.startswith("box_head"))
    ]
    backbone_trainable = [
        name
        for name, param in model.named_parameters()
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
    return (
        len(rgssb_trainable),
        len(head_trainable),
        len(backbone_trainable),
        trainable_names,
    )


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    ostrack_root = repo_root / "external" / "OSTrack"
    if not ostrack_root.is_dir():
        raise FileNotFoundError(f"Missing OSTrack root: {ostrack_root}")

    expected = {
        "vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_degraded_3000_featcons_lam002_debug": {
            "weight": 0.02,
            "cycle_config": repo_root / "configs" / "rgssb_experiment_cycle_featcons_lam002.json",
        },
        "vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_degraded_3000_featcons_lam010_debug": {
            "weight": 0.10,
            "cycle_config": repo_root / "configs" / "rgssb_experiment_cycle_featcons_lam010.json",
        },
    }

    os.chdir(ostrack_root)
    sys.path.insert(0, str(ostrack_root))
    _stub_optional_coco_import()

    from lib.config.ostrack.config import cfg, update_config_from_file
    from lib.models.ostrack import build_ostrack
    from lib.train.freeze import apply_freeze_mode

    lasot_root = Path("data/lasot")
    if not lasot_root.exists():
        raise FileNotFoundError(f"LaSOT root does not exist: {lasot_root.resolve()}")

    expected_types = ["motion_blur", "low_resolution", "gaussian_noise"]
    for config_name, values in expected.items():
        config_path = ostrack_root / "experiments" / "ostrack" / f"{config_name}.yaml"
        if not config_path.is_file():
            raise FileNotFoundError(f"Missing OSTrack config: {config_path}")

        update_config_from_file(str(config_path))
        _assert(f"{config_name} MODEL.RGSSB.ENABLE", cfg.MODEL.RGSSB.ENABLE is True)
        _assert(f"{config_name} TRAIN.FREEZE_MODE", cfg.TRAIN.FREEZE_MODE == "rgssb_head")
        _assert(f"{config_name} DATA.TRAIN.DATASETS_NAME", list(cfg.DATA.TRAIN.DATASETS_NAME) == ["LASOT"])
        _assert(f"{config_name} DATA.TRAIN.DATASETS_RATIO", list(cfg.DATA.TRAIN.DATASETS_RATIO) == [1])
        _assert(f"{config_name} DATA.TRAIN.SAMPLE_PER_EPOCH", int(cfg.DATA.TRAIN.SAMPLE_PER_EPOCH) == 3000)
        _assert(f"{config_name} DATA.VAL.DATASETS_NAME", list(cfg.DATA.VAL.DATASETS_NAME) == ["LASOT"])
        _assert(f"{config_name} DATA.VAL.DATASETS_RATIO", list(cfg.DATA.VAL.DATASETS_RATIO) == [1])
        _assert(f"{config_name} DATA.VAL.SAMPLE_PER_EPOCH", int(cfg.DATA.VAL.SAMPLE_PER_EPOCH) == 300)
        _assert(f"{config_name} TRAIN.BATCH_SIZE", int(cfg.TRAIN.BATCH_SIZE) == 1)
        _assert(f"{config_name} TRAIN.NUM_WORKER", int(cfg.TRAIN.NUM_WORKER) == 2)
        _assert(f"{config_name} TRAIN.EPOCH", int(cfg.TRAIN.EPOCH) == 1)
        _assert(f"{config_name} TEST.EPOCH", int(cfg.TEST.EPOCH) == 1)
        _assert(f"{config_name} DATA.DEGRADATION.ENABLE", cfg.DATA.DEGRADATION.ENABLE is True)
        _assert(f"{config_name} DATA.DEGRADATION.PROBABILITY", float(cfg.DATA.DEGRADATION.PROBABILITY) == 1.0)
        _assert(f"{config_name} DATA.DEGRADATION.APPLY_TO", cfg.DATA.DEGRADATION.APPLY_TO == "search_only")
        _assert(f"{config_name} DATA.DEGRADATION.TYPES", list(cfg.DATA.DEGRADATION.TYPES) == expected_types)
        _assert(f"{config_name} DATA.DEGRADATION.SEVERITY", cfg.DATA.DEGRADATION.SEVERITY == "medium")
        _assert(f"{config_name} DATA.DEGRADATION.SEED", int(cfg.DATA.DEGRADATION.SEED) == 42)
        _assert(f"{config_name} FEATURE_CONSISTENCY.ENABLE", cfg.TRAIN.FEATURE_CONSISTENCY.ENABLE is True)
        _assert(
            f"{config_name} FEATURE_CONSISTENCY.WEIGHT",
            abs(float(cfg.TRAIN.FEATURE_CONSISTENCY.WEIGHT) - float(values["weight"])) < 1e-12,
        )
        _assert(f"{config_name} FEATURE_CONSISTENCY.LOSS", cfg.TRAIN.FEATURE_CONSISTENCY.LOSS == "l1")
        _assert(f"{config_name} FEATURE_CONSISTENCY.NORMALIZE", cfg.TRAIN.FEATURE_CONSISTENCY.NORMALIZE is True)
        _assert(f"{config_name} FEATURE_CONSISTENCY.DETACH_CLEAN", cfg.TRAIN.FEATURE_CONSISTENCY.DETACH_CLEAN is True)

        model = build_ostrack(cfg, training=True)
        trainable_params, frozen_params, trainable_names = apply_freeze_mode(model, cfg)
        rgssb_count, head_count, backbone_count, checked_names = _verify_trainable_params(
            model,
            trainable_names,
        )

        _verify_cycle_config(Path(values["cycle_config"]), config_name)

        print(f"config: {config_path}")
        print(f"lambda: {cfg.TRAIN.FEATURE_CONSISTENCY.WEIGHT}")
        print(f"MODEL.RGSSB.ENABLE: {cfg.MODEL.RGSSB.ENABLE}")
        print(f"TRAIN.FREEZE_MODE: {cfg.TRAIN.FREEZE_MODE}")
        print(f"TRAIN.FEATURE_CONSISTENCY.ENABLE: {cfg.TRAIN.FEATURE_CONSISTENCY.ENABLE}")
        print(f"lasot_root: {lasot_root.resolve()}")
        print(f"trainable_params: {trainable_params}")
        print(f"frozen_params: {frozen_params}")
        print(f"rgssb_trainable_count: {rgssb_count}")
        print(f"head_trainable_count: {head_count}")
        print(f"backbone_trainable_count: {backbone_count}")
        print(f"cycle_config: {values['cycle_config']}")
        print("trainable parameter names:")
        for name in checked_names:
            print(f"  {name}")
        print("verification: config, cycle config, and freeze mode passed")
        del model
        gc.collect()


if __name__ == "__main__":
    main()
