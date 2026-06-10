#!/usr/bin/env python3
"""Verify the LaSOT-only RG-SSB train debug config without running training."""

from __future__ import annotations

import os
import sys
import types
from pathlib import Path


def _stub_optional_coco_import() -> None:
    """Avoid requiring pycocotools while importing the OSTrack dataset package."""
    if "pycocotools" not in sys.modules:
        sys.modules["pycocotools"] = types.ModuleType("pycocotools")
    pycocotools_module = sys.modules["pycocotools"]
    if "pycocotools.coco" not in sys.modules:
        coco_module = types.ModuleType("pycocotools.coco")

        class _COCO:
            def __init__(self, *args, **kwargs):
                raise RuntimeError("COCO is not used by the LaSOT-only RG-SSB debug verifier.")

        coco_module.COCO = _COCO
        sys.modules["pycocotools.coco"] = coco_module
        pycocotools_module.coco = coco_module
    if "pycocotools.mask" not in sys.modules:
        mask_module = types.ModuleType("pycocotools.mask")
        sys.modules["pycocotools.mask"] = mask_module
        pycocotools_module.mask = mask_module


def _first_visible_frame_ids(visible, count: int = 3) -> list[int]:
    ids = [idx for idx, flag in enumerate(visible.tolist()) if bool(flag)]
    if len(ids) < count:
        raise AssertionError(f"Expected at least {count} visible frames, found {len(ids)}")
    return ids[:count]


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    ostrack_root = repo_root / "external" / "OSTrack"
    config_path = (
        ostrack_root
        / "experiments"
        / "ostrack"
        / "vitb_256_mae_ce_32x4_ep300_rgssb_train_lasot_debug.yaml"
    )

    if not ostrack_root.exists():
        raise FileNotFoundError(f"OSTrack root does not exist: {ostrack_root}")
    if not config_path.exists():
        raise FileNotFoundError(f"LaSOT RG-SSB train debug config does not exist: {config_path}")

    os.chdir(ostrack_root)
    sys.path.insert(0, str(ostrack_root))
    _stub_optional_coco_import()

    from lib.config.ostrack.config import cfg, update_config_from_file
    from lib.train.data import opencv_loader
    from lib.train.dataset import Lasot

    update_config_from_file(str(config_path))

    forbidden = {"GOT10K_vottrain", "GOT10K_votval", "GOT10K_train_full", "COCO17", "TRACKINGNET"}
    train_names = list(cfg.DATA.TRAIN.DATASETS_NAME)
    val_names = list(cfg.DATA.VAL.DATASETS_NAME)

    if cfg.MODEL.RGSSB.ENABLE is not True:
        raise AssertionError("MODEL.RGSSB.ENABLE must be True.")
    if cfg.TRAIN.FREEZE_MODE != "rgssb_only":
        raise AssertionError('TRAIN.FREEZE_MODE must be "rgssb_only".')
    if train_names != ["LASOT"]:
        raise AssertionError(f"Expected train datasets ['LASOT'], got {train_names}")
    if val_names != ["LASOT"]:
        raise AssertionError(f"Expected val datasets ['LASOT'], got {val_names}")
    if forbidden.intersection(train_names + val_names):
        raise AssertionError(f"Unexpected non-LaSOT datasets in config: {train_names + val_names}")

    dataset = Lasot(root="data/lasot", split="train", image_loader=opencv_loader)
    num_sequences = dataset.get_num_sequences()
    if num_sequences <= 0:
        raise AssertionError("LaSOT train split has no sequences.")

    sequence_info = dataset.get_sequence_info(0)
    frame_ids = _first_visible_frame_ids(sequence_info["visible"], count=3)
    frames, anno, meta = dataset.get_frames(0, frame_ids, sequence_info)
    if len(frames) != len(frame_ids):
        raise AssertionError("Loaded frame count does not match requested frame ids.")
    if len(anno["bbox"]) != len(frame_ids):
        raise AssertionError("Loaded annotation count does not match requested frame ids.")

    print(f"config: {config_path}")
    print(f"MODEL.RGSSB.ENABLE: {cfg.MODEL.RGSSB.ENABLE}")
    print(f"TRAIN.FREEZE_MODE: {cfg.TRAIN.FREEZE_MODE}")
    print(f"DATA.TRAIN.DATASETS_NAME: {train_names}")
    print(f"DATA.VAL.DATASETS_NAME: {val_names}")
    print(f"lasot_root: {Path('data/lasot').resolve()}")
    print(f"lasot_sequences: {num_sequences}")
    print(f"sequence_0_name: {dataset.sequence_list[0]}")
    print(f"loaded_frame_ids: {frame_ids}")
    print(f"first_frame_shape: {frames[0].shape}")
    print(f"first_bbox: {anno['bbox'][0].tolist()}")
    print(f"object_class_name: {meta.get('object_class_name')}")
    print("verification: LaSOT-only RG-SSB train debug config does not require GOT10K/COCO/TrackingNet")


if __name__ == "__main__":
    main()
