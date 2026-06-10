#!/usr/bin/env python3
"""Verify RG-SSB + head trainable parameters for the degraded LaSOT debug config."""

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
                raise RuntimeError("COCO is not used by the RG-SSB + head verifier.")

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
        / "vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_degraded_1000_debug.yaml"
    )

    if not config_path.is_file():
        raise FileNotFoundError(f"Missing config: {config_path}")

    os.chdir(ostrack_root)
    sys.path.insert(0, str(ostrack_root))
    _stub_optional_coco_import()

    from lib.config.ostrack.config import cfg, update_config_from_file
    from lib.models.ostrack import build_ostrack
    from lib.train.data import opencv_loader
    from lib.train.dataset import Lasot
    from lib.train.freeze import apply_freeze_mode

    update_config_from_file(str(config_path))
    if cfg.MODEL.RGSSB.ENABLE is not True:
        raise AssertionError("MODEL.RGSSB.ENABLE must be True.")
    if cfg.TRAIN.FREEZE_MODE != "rgssb_head":
        raise AssertionError('TRAIN.FREEZE_MODE must be "rgssb_head".')

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
        raise AssertionError(f"Unexpected trainable parameters: {non_allowed}")
    if backbone_trainable:
        raise AssertionError(f"Backbone parameters must be frozen: {backbone_trainable[:10]}")

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
    print("trainable parameter names:")
    for name in trainable_names:
        print(f"  {name}")
    print(f"total_params: {total_params}")
    print(f"trainable_params: {trainable_params}")
    print(f"frozen_params: {frozen_params}")
    print(f"rgssb_trainable_count: {len(rgssb_trainable)}")
    print(f"head_trainable_count: {len(head_trainable)}")
    print(f"backbone_trainable_count: {len(backbone_trainable)}")
    print(f"trainable_prefixes: rgssb, box_head")
    print(f"lasot_root: {lasot_root.resolve()}")
    print(f"lasot_sequences: {dataset.get_num_sequences()}")
    print(f"sequence_0_name: {dataset.sequence_list[0]}")
    print(f"loaded_frame_id: {frame_id}")
    print(f"loaded_frame_shape: {frames[0].shape}")
    print(f"first_bbox: {anno['bbox'][0].tolist()}")
    print(f"object_class_name: {meta.get('object_class_name')}")
    print("verification: RG-SSB and head are trainable; backbone is frozen")


if __name__ == "__main__":
    main()
