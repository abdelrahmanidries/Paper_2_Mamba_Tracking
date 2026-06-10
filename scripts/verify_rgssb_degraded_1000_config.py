#!/usr/bin/env python3
"""Verify the 1000-sample RG-SSB degraded LaSOT debug config."""

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
                raise RuntimeError("COCO is not used by the 1000-sample RG-SSB verifier.")

        coco_module.COCO = _COCO
        sys.modules["pycocotools.coco"] = coco_module
        pycocotools_module.coco = coco_module
    if "pycocotools.mask" not in sys.modules:
        mask_module = types.ModuleType("pycocotools.mask")
        sys.modules["pycocotools.mask"] = mask_module
        pycocotools_module.mask = mask_module


def _first_visible_frame_id(visible) -> int:
    for idx, flag in enumerate(visible.tolist()):
        if bool(flag):
            return idx
    raise AssertionError("No visible frame found in sample sequence.")


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    ostrack_root = repo_root / "external" / "OSTrack"
    config_path = (
        ostrack_root
        / "experiments"
        / "ostrack"
        / "vitb_256_mae_ce_32x4_ep300_rgssb_train_lasot_degraded_1000_debug.yaml"
    )

    if not config_path.is_file():
        raise FileNotFoundError(f"Missing config: {config_path}")

    os.chdir(ostrack_root)
    sys.path.insert(0, str(ostrack_root))
    _stub_optional_coco_import()

    from lib.config.ostrack.config import cfg, update_config_from_file
    from lib.train.data import opencv_loader
    from lib.train.dataset import Lasot

    update_config_from_file(str(config_path))

    expected_types = ["motion_blur", "low_resolution", "gaussian_noise"]
    checks = {
        "MODEL.RGSSB.ENABLE": cfg.MODEL.RGSSB.ENABLE is True,
        "TRAIN.FREEZE_MODE": cfg.TRAIN.FREEZE_MODE == "rgssb_only",
        "DATA.TRAIN.DATASETS_NAME": list(cfg.DATA.TRAIN.DATASETS_NAME) == ["LASOT"],
        "DATA.TRAIN.DATASETS_RATIO": list(cfg.DATA.TRAIN.DATASETS_RATIO) == [1],
        "DATA.TRAIN.SAMPLE_PER_EPOCH": int(cfg.DATA.TRAIN.SAMPLE_PER_EPOCH) == 1000,
        "DATA.VAL.DATASETS_NAME": list(cfg.DATA.VAL.DATASETS_NAME) == ["LASOT"],
        "DATA.VAL.DATASETS_RATIO": list(cfg.DATA.VAL.DATASETS_RATIO) == [1],
        "DATA.VAL.SAMPLE_PER_EPOCH": int(cfg.DATA.VAL.SAMPLE_PER_EPOCH) == 100,
        "TRAIN.BATCH_SIZE": int(cfg.TRAIN.BATCH_SIZE) == 1,
        "TRAIN.NUM_WORKER": int(cfg.TRAIN.NUM_WORKER) == 2,
        "TRAIN.EPOCH": int(cfg.TRAIN.EPOCH) == 1,
        "TEST.EPOCH": int(cfg.TEST.EPOCH) == 1,
        "DATA.SEARCH.SIZE": int(cfg.DATA.SEARCH.SIZE) == 256,
        "DATA.TEMPLATE.SIZE": int(cfg.DATA.TEMPLATE.SIZE) == 128,
        "DATA.DEGRADATION.ENABLE": cfg.DATA.DEGRADATION.ENABLE is True,
        "DATA.DEGRADATION.PROBABILITY": float(cfg.DATA.DEGRADATION.PROBABILITY) == 1.0,
        "DATA.DEGRADATION.APPLY_TO": cfg.DATA.DEGRADATION.APPLY_TO == "search_only",
        "DATA.DEGRADATION.TYPES": list(cfg.DATA.DEGRADATION.TYPES) == expected_types,
        "DATA.DEGRADATION.SEVERITY": cfg.DATA.DEGRADATION.SEVERITY == "medium",
        "DATA.DEGRADATION.SEED": int(cfg.DATA.DEGRADATION.SEED) == 42,
    }
    failed = [name for name, ok in checks.items() if not ok]
    if failed:
        raise AssertionError(f"Config verification failed for: {failed}")

    lasot_root = Path("data/lasot")
    if not lasot_root.exists():
        raise FileNotFoundError(f"LaSOT root does not exist: {lasot_root.resolve()}")

    dataset = Lasot(root=str(lasot_root), split="train", image_loader=opencv_loader)
    sequence_info = dataset.get_sequence_info(0)
    frame_id = _first_visible_frame_id(sequence_info["visible"])
    frames, anno, meta = dataset.get_frames(0, [frame_id], sequence_info)
    if not frames or frames[0] is None:
        raise AssertionError("Failed to load a LaSOT sample frame.")

    print(f"config: {config_path}")
    print(f"MODEL.RGSSB.ENABLE: {cfg.MODEL.RGSSB.ENABLE}")
    print(f"TRAIN.FREEZE_MODE: {cfg.TRAIN.FREEZE_MODE}")
    print(f"DATA.TRAIN.DATASETS_NAME: {list(cfg.DATA.TRAIN.DATASETS_NAME)}")
    print(f"DATA.TRAIN.SAMPLE_PER_EPOCH: {cfg.DATA.TRAIN.SAMPLE_PER_EPOCH}")
    print(f"DATA.VAL.DATASETS_NAME: {list(cfg.DATA.VAL.DATASETS_NAME)}")
    print(f"DATA.VAL.SAMPLE_PER_EPOCH: {cfg.DATA.VAL.SAMPLE_PER_EPOCH}")
    print(f"TRAIN.EPOCH: {cfg.TRAIN.EPOCH}")
    print(f"TEST.EPOCH: {cfg.TEST.EPOCH}")
    print(f"DATA.DEGRADATION.ENABLE: {cfg.DATA.DEGRADATION.ENABLE}")
    print(f"DATA.DEGRADATION.TYPES: {list(cfg.DATA.DEGRADATION.TYPES)}")
    print(f"DATA.DEGRADATION.APPLY_TO: {cfg.DATA.DEGRADATION.APPLY_TO}")
    print(f"lasot_root: {lasot_root.resolve()}")
    print(f"lasot_sequences: {dataset.get_num_sequences()}")
    print(f"sequence_0_name: {dataset.sequence_list[0]}")
    print(f"loaded_frame_id: {frame_id}")
    print(f"loaded_frame_shape: {frames[0].shape}")
    print(f"first_bbox: {anno['bbox'][0].tolist()}")
    print(f"object_class_name: {meta.get('object_class_name')}")
    print("verification: 1000-sample degraded RG-SSB LaSOT config is ready")


if __name__ == "__main__":
    main()
