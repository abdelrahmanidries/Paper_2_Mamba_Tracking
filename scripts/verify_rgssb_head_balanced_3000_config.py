#!/usr/bin/env python3
"""Verify the balanced 3000-sample RG-SSB + head LaSOT debug config."""

from __future__ import annotations

import os
import sys
import types
from pathlib import Path

import numpy as np


def _stub_optional_coco_import() -> None:
    if "pycocotools" not in sys.modules:
        sys.modules["pycocotools"] = types.ModuleType("pycocotools")
    pycocotools_module = sys.modules["pycocotools"]
    if "pycocotools.coco" not in sys.modules:
        coco_module = types.ModuleType("pycocotools.coco")

        class _COCO:
            def __init__(self, *args, **kwargs):
                raise RuntimeError("COCO is not used by the balanced RG-SSB verifier.")

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


def _assert(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(f"Verification failed for {name}")


def _verify_probability_logic(degradation_cfg, augmentor_cls) -> tuple[int, int]:
    augmentor = augmentor_cls(degradation_cfg)
    grid_x = np.tile(np.arange(64, dtype=np.uint8), (64, 1))
    grid_y = grid_x.T
    image = np.stack([grid_x * 4, grid_y * 4, ((grid_x + grid_y) * 2).astype(np.uint8)], axis=2)
    clean_count = 0
    degraded_count = 0

    for _ in range(100):
        augmentor.begin_sample()
        out = augmentor.apply([image], role="search")[0]
        if np.array_equal(out, image):
            clean_count += 1
        else:
            degraded_count += 1

    if clean_count == 0 or degraded_count == 0:
        raise AssertionError(
            "DATA.DEGRADATION.PROBABILITY=0.5 should produce both clean and degraded synthetic samples."
        )
    return clean_count, degraded_count


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    ostrack_root = repo_root / "external" / "OSTrack"
    config_path = (
        ostrack_root
        / "experiments"
        / "ostrack"
        / "vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_balanced_3000_debug.yaml"
    )

    if not config_path.is_file():
        raise FileNotFoundError(f"Missing config: {config_path}")

    os.chdir(ostrack_root)
    sys.path.insert(0, str(ostrack_root))
    _stub_optional_coco_import()

    from lib.config.ostrack.config import cfg, update_config_from_file
    from lib.models.ostrack import build_ostrack
    from lib.train.data import opencv_loader
    from lib.train.data.degradation import TrainingDegradationAugmentor
    from lib.train.dataset import Lasot
    from lib.train.freeze import apply_freeze_mode

    update_config_from_file(str(config_path))

    expected_types = ["motion_blur", "low_resolution", "gaussian_noise"]
    _assert("MODEL.RGSSB.ENABLE", cfg.MODEL.RGSSB.ENABLE is True)
    _assert("TRAIN.FREEZE_MODE", cfg.TRAIN.FREEZE_MODE == "rgssb_head")
    _assert("DATA.TRAIN.DATASETS_NAME", list(cfg.DATA.TRAIN.DATASETS_NAME) == ["LASOT"])
    _assert("DATA.TRAIN.DATASETS_RATIO", list(cfg.DATA.TRAIN.DATASETS_RATIO) == [1])
    _assert("DATA.TRAIN.SAMPLE_PER_EPOCH", int(cfg.DATA.TRAIN.SAMPLE_PER_EPOCH) == 3000)
    _assert("DATA.VAL.DATASETS_NAME", list(cfg.DATA.VAL.DATASETS_NAME) == ["LASOT"])
    _assert("DATA.VAL.DATASETS_RATIO", list(cfg.DATA.VAL.DATASETS_RATIO) == [1])
    _assert("DATA.VAL.SAMPLE_PER_EPOCH", int(cfg.DATA.VAL.SAMPLE_PER_EPOCH) == 300)
    _assert("TRAIN.BATCH_SIZE", int(cfg.TRAIN.BATCH_SIZE) == 1)
    _assert("TRAIN.NUM_WORKER", int(cfg.TRAIN.NUM_WORKER) == 2)
    _assert("TRAIN.EPOCH", int(cfg.TRAIN.EPOCH) == 1)
    _assert("TEST.EPOCH", int(cfg.TEST.EPOCH) == 1)
    _assert("DATA.SEARCH.SIZE", int(cfg.DATA.SEARCH.SIZE) == 256)
    _assert("DATA.TEMPLATE.SIZE", int(cfg.DATA.TEMPLATE.SIZE) == 128)
    _assert("DATA.DEGRADATION.ENABLE", cfg.DATA.DEGRADATION.ENABLE is True)
    _assert("DATA.DEGRADATION.PROBABILITY", float(cfg.DATA.DEGRADATION.PROBABILITY) == 0.5)
    _assert("DATA.DEGRADATION.APPLY_TO", cfg.DATA.DEGRADATION.APPLY_TO == "search_only")
    _assert("DATA.DEGRADATION.TYPES", list(cfg.DATA.DEGRADATION.TYPES) == expected_types)
    _assert("DATA.DEGRADATION.SEVERITY", cfg.DATA.DEGRADATION.SEVERITY == "medium")
    _assert("DATA.DEGRADATION.SEED", int(cfg.DATA.DEGRADATION.SEED) == 42)

    probability_clean, probability_degraded = _verify_probability_logic(
        cfg.DATA.DEGRADATION, TrainingDegradationAugmentor
    )

    lasot_root = Path("data/lasot")
    if not lasot_root.exists():
        raise FileNotFoundError(f"LaSOT root does not exist: {lasot_root.resolve()}")

    dataset = Lasot(root=str(lasot_root), split="train", image_loader=opencv_loader)
    sequence_info = dataset.get_sequence_info(0)
    frame_id = _first_visible_frame_id(sequence_info["visible"])
    frames, anno, meta = dataset.get_frames(0, [frame_id], sequence_info)
    if not frames or frames[0] is None:
        raise AssertionError("Failed to load a LaSOT sample frame.")

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
    print(f"MODEL.RGSSB.ENABLE: {cfg.MODEL.RGSSB.ENABLE}")
    print(f"TRAIN.FREEZE_MODE: {cfg.TRAIN.FREEZE_MODE}")
    print(f"DATA.TRAIN.DATASETS_NAME: {list(cfg.DATA.TRAIN.DATASETS_NAME)}")
    print(f"DATA.TRAIN.SAMPLE_PER_EPOCH: {cfg.DATA.TRAIN.SAMPLE_PER_EPOCH}")
    print(f"DATA.VAL.DATASETS_NAME: {list(cfg.DATA.VAL.DATASETS_NAME)}")
    print(f"DATA.VAL.SAMPLE_PER_EPOCH: {cfg.DATA.VAL.SAMPLE_PER_EPOCH}")
    print(f"TRAIN.BATCH_SIZE: {cfg.TRAIN.BATCH_SIZE}")
    print(f"TRAIN.EPOCH: {cfg.TRAIN.EPOCH}")
    print(f"TEST.EPOCH: {cfg.TEST.EPOCH}")
    print(f"DATA.DEGRADATION.ENABLE: {cfg.DATA.DEGRADATION.ENABLE}")
    print(f"DATA.DEGRADATION.PROBABILITY: {cfg.DATA.DEGRADATION.PROBABILITY}")
    print(f"DATA.DEGRADATION.TYPES: {list(cfg.DATA.DEGRADATION.TYPES)}")
    print(f"DATA.DEGRADATION.APPLY_TO: {cfg.DATA.DEGRADATION.APPLY_TO}")
    print(f"probability_probe_clean_count: {probability_clean}")
    print(f"probability_probe_degraded_count: {probability_degraded}")
    print(f"lasot_root: {lasot_root.resolve()}")
    print(f"lasot_sequences: {dataset.get_num_sequences()}")
    print(f"sequence_0_name: {dataset.sequence_list[0]}")
    print(f"loaded_frame_id: {frame_id}")
    print(f"loaded_frame_shape: {frames[0].shape}")
    print(f"first_bbox: {anno['bbox'][0].tolist()}")
    print(f"object_class_name: {meta.get('object_class_name')}")
    print("trainable parameter names:")
    for name in trainable_names:
        print(f"  {name}")
    print(f"total_params: {total_params}")
    print(f"trainable_params: {trainable_params}")
    print(f"frozen_params: {frozen_params}")
    print(f"rgssb_trainable_count: {len(rgssb_trainable)}")
    print(f"head_trainable_count: {len(head_trainable)}")
    print(f"backbone_trainable_count: {len(backbone_trainable)}")
    print("verification: balanced config is ready; RG-SSB and head are trainable; backbone is frozen")


if __name__ == "__main__":
    main()
