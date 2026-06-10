#!/usr/bin/env python3
"""Verify OSTrack training degradation augmentation without running training."""

from __future__ import annotations

import os
import sys
import types
from pathlib import Path

import numpy as np
import yaml


def _stub_optional_coco_import() -> None:
    if "pycocotools" not in sys.modules:
        sys.modules["pycocotools"] = types.ModuleType("pycocotools")
    pycocotools_module = sys.modules["pycocotools"]
    if "pycocotools.coco" not in sys.modules:
        coco_module = types.ModuleType("pycocotools.coco")

        class _COCO:
            def __init__(self, *args, **kwargs):
                raise RuntimeError("COCO is not used by the degradation verifier.")

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


def _make_synthetic_image() -> np.ndarray:
    height, width = 96, 128
    y = np.arange(height, dtype=np.uint8)[:, None]
    x = np.arange(width, dtype=np.uint8)[None, :]
    return np.stack(
        [
            np.tile(x, (height, 1)),
            np.tile(y, (1, width)),
            (np.tile(x, (height, 1)) // 2 + np.tile(y, (1, width)) // 2).astype(np.uint8),
        ],
        axis=2,
    )


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    ostrack_root = repo_root / "external" / "OSTrack"
    degraded_config = (
        ostrack_root
        / "experiments"
        / "ostrack"
        / "vitb_256_mae_ce_32x4_ep300_rgssb_train_lasot_degraded_debug.yaml"
    )
    baseline_config = ostrack_root / "experiments" / "ostrack" / "vitb_256_mae_ce_32x4_ep300.yaml"

    if not degraded_config.is_file():
        raise FileNotFoundError(f"Missing degraded debug config: {degraded_config}")
    if not baseline_config.is_file():
        raise FileNotFoundError(f"Missing baseline config: {baseline_config}")

    with baseline_config.open("r", encoding="utf-8") as f:
        baseline_data = yaml.safe_load(f) or {}
    baseline_degradation = baseline_data.get("DATA", {}).get("DEGRADATION", {})
    if bool(baseline_degradation.get("ENABLE", False)):
        raise AssertionError("Baseline config unexpectedly enables DATA.DEGRADATION.")

    os.chdir(ostrack_root)
    sys.path.insert(0, str(ostrack_root))
    _stub_optional_coco_import()

    from lib.config.ostrack.config import cfg, update_config_from_file
    from lib.train.data import opencv_loader
    from lib.train.data.degradation import TrainingDegradationAugmentor
    from lib.train.dataset import Lasot

    if cfg.DATA.DEGRADATION.ENABLE is not False:
        raise AssertionError("Default DATA.DEGRADATION.ENABLE must be False.")

    update_config_from_file(str(degraded_config))

    if cfg.DATA.DEGRADATION.ENABLE is not True:
        raise AssertionError("Degraded debug config must enable DATA.DEGRADATION.")
    if cfg.MODEL.RGSSB.ENABLE is not True:
        raise AssertionError("Degraded debug config must enable MODEL.RGSSB.")
    if cfg.TRAIN.FREEZE_MODE != "rgssb_only":
        raise AssertionError('Degraded debug config must use TRAIN.FREEZE_MODE="rgssb_only".')
    if list(cfg.DATA.TRAIN.DATASETS_NAME) != ["LASOT"]:
        raise AssertionError("Degraded debug config must train on LASOT only.")
    if list(cfg.DATA.VAL.DATASETS_NAME) != ["LASOT"]:
        raise AssertionError("Degraded debug config must validate on LASOT only.")

    augmentor = TrainingDegradationAugmentor(cfg.DATA.DEGRADATION)

    synthetic = _make_synthetic_image()
    augmentor.begin_sample()
    degraded_synthetic = augmentor.apply([synthetic.copy()], role="search")[0]
    synthetic_size_preserved = degraded_synthetic.shape == synthetic.shape
    synthetic_changed = bool(np.any(degraded_synthetic != synthetic))
    if not synthetic_size_preserved:
        raise AssertionError("Synthetic degradation changed image size.")
    if not synthetic_changed:
        raise AssertionError("Synthetic degradation did not change the image.")

    dataset = Lasot(root="data/lasot", split="train", image_loader=opencv_loader)
    sequence_info = dataset.get_sequence_info(0)
    frame_id = _first_visible_frame_id(sequence_info["visible"])
    frames, anno, meta = dataset.get_frames(0, [frame_id], sequence_info)
    frame = frames[0]
    augmentor.begin_sample()
    degraded_frame = augmentor.apply([frame.copy()], role="search")[0]
    frame_size_preserved = degraded_frame.shape == frame.shape
    if not frame_size_preserved:
        raise AssertionError("LaSOT frame degradation changed image size.")

    print(f"config: {degraded_config}")
    print(f"baseline_degradation_enabled: {bool(baseline_degradation.get('ENABLE', False))}")
    print(f"default_degradation_enabled: False")
    print(f"DATA.DEGRADATION.ENABLE: {cfg.DATA.DEGRADATION.ENABLE}")
    print(f"DATA.DEGRADATION.APPLY_TO: {cfg.DATA.DEGRADATION.APPLY_TO}")
    print(f"DATA.DEGRADATION.TYPES: {list(cfg.DATA.DEGRADATION.TYPES)}")
    print(f"DATA.DEGRADATION.SEVERITY: {cfg.DATA.DEGRADATION.SEVERITY}")
    print(f"MODEL.RGSSB.ENABLE: {cfg.MODEL.RGSSB.ENABLE}")
    print(f"TRAIN.FREEZE_MODE: {cfg.TRAIN.FREEZE_MODE}")
    print(f"train_datasets: {list(cfg.DATA.TRAIN.DATASETS_NAME)}")
    print(f"val_datasets: {list(cfg.DATA.VAL.DATASETS_NAME)}")
    print(f"synthetic_size_preserved: {synthetic_size_preserved}")
    print(f"synthetic_changed: {synthetic_changed}")
    print(f"lasot_sequences: {dataset.get_num_sequences()}")
    print(f"lasot_sequence_0_name: {dataset.sequence_list[0]}")
    print(f"lasot_frame_id: {frame_id}")
    print(f"lasot_frame_shape: {frame.shape}")
    print(f"lasot_degraded_size_preserved: {frame_size_preserved}")
    print(f"lasot_first_bbox: {anno['bbox'][0].tolist()}")
    print(f"lasot_object_class_name: {meta.get('object_class_name')}")
    print("verification: training degradation pipeline is config-gated and preserves image size")


if __name__ == "__main__":
    main()
