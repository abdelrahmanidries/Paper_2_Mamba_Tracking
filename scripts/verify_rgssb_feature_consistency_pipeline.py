#!/usr/bin/env python3
"""Verify the minimal RG-SSB feature-consistency training path."""

from __future__ import annotations

import os
import sys
import types
from pathlib import Path

import torch


def _stub_optional_coco_import() -> None:
    if "pycocotools" not in sys.modules:
        sys.modules["pycocotools"] = types.ModuleType("pycocotools")
    pycocotools_module = sys.modules["pycocotools"]
    if "pycocotools.coco" not in sys.modules:
        coco_module = types.ModuleType("pycocotools.coco")

        class _COCO:
            def __init__(self, *args, **kwargs):
                raise RuntimeError("COCO is not used by the feature-consistency verifier.")

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


def _move_data_to_device(data: dict, device: torch.device) -> dict:
    moved = {}
    for key, value in data.items():
        moved[key] = value.to(device) if torch.is_tensor(value) else value
    return moved


def _visible_ids(visible, count: int) -> list[int]:
    ids = [idx for idx, flag in enumerate(visible.tolist()) if bool(flag)]
    if len(ids) < count:
        raise AssertionError("Not enough visible LaSOT frames for processing verification.")
    return ids[:count]


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    ostrack_root = repo_root / "external" / "OSTrack"
    config_path = (
        ostrack_root
        / "experiments"
        / "ostrack"
        / "vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_degraded_3000_featcons_debug.yaml"
    )
    if not config_path.is_file():
        raise FileNotFoundError(f"Missing config: {config_path}")

    os.chdir(ostrack_root)
    sys.path.insert(0, str(ostrack_root))
    _stub_optional_coco_import()

    from lib.config.ostrack.config import cfg, update_config_from_file
    from lib.models.ostrack import build_ostrack
    from lib.train.actors import OSTrackActor
    from lib.train.data import opencv_loader
    from lib.train.data import processing
    import lib.train.data.transforms as tfm
    from lib.train.dataset import Lasot
    from lib.train.freeze import apply_freeze_mode
    from lib.utils import TensorDict
    from lib.utils.box_ops import giou_loss
    from lib.utils.focal_loss import FocalLoss

    update_config_from_file(str(config_path))

    _assert("MODEL.RGSSB.ENABLE", cfg.MODEL.RGSSB.ENABLE is True)
    _assert("TRAIN.FREEZE_MODE", cfg.TRAIN.FREEZE_MODE == "rgssb_head")
    _assert("TRAIN.FEATURE_CONSISTENCY.ENABLE", cfg.TRAIN.FEATURE_CONSISTENCY.ENABLE is True)
    _assert("TRAIN.FEATURE_CONSISTENCY.WEIGHT", float(cfg.TRAIN.FEATURE_CONSISTENCY.WEIGHT) == 0.05)
    _assert("TRAIN.FEATURE_CONSISTENCY.LOSS", cfg.TRAIN.FEATURE_CONSISTENCY.LOSS == "l1")
    _assert("TRAIN.FEATURE_CONSISTENCY.NORMALIZE", cfg.TRAIN.FEATURE_CONSISTENCY.NORMALIZE is True)
    _assert("TRAIN.FEATURE_CONSISTENCY.DETACH_CLEAN", cfg.TRAIN.FEATURE_CONSISTENCY.DETACH_CLEAN is True)
    _assert("DATA.DEGRADATION.PROBABILITY", float(cfg.DATA.DEGRADATION.PROBABILITY) == 1.0)

    lasot_root = Path("data/lasot")
    if not lasot_root.exists():
        raise FileNotFoundError(f"LaSOT root does not exist: {lasot_root.resolve()}")
    dataset = Lasot(root=str(lasot_root), split="train", image_loader=opencv_loader)
    sequence_info = dataset.get_sequence_info(0)
    frame_ids = _visible_ids(sequence_info["visible"], 2)
    frames, anno, meta = dataset.get_frames(0, [frame_ids[0]], sequence_info)
    if not frames or frames[0] is None:
        raise AssertionError("Failed to load a LaSOT sample frame.")
    template_frames, template_anno, _ = dataset.get_frames(0, [frame_ids[0]], sequence_info)
    search_frames, search_anno, _ = dataset.get_frames(0, [frame_ids[1]], sequence_info)
    height, width, _ = template_frames[0].shape
    processor = processing.STARKProcessing(
        search_area_factor={"template": cfg.DATA.TEMPLATE.FACTOR, "search": cfg.DATA.SEARCH.FACTOR},
        output_sz={"template": cfg.DATA.TEMPLATE.SIZE, "search": cfg.DATA.SEARCH.SIZE},
        center_jitter_factor={"template": cfg.DATA.TEMPLATE.CENTER_JITTER, "search": cfg.DATA.SEARCH.CENTER_JITTER},
        scale_jitter_factor={"template": cfg.DATA.TEMPLATE.SCALE_JITTER, "search": cfg.DATA.SEARCH.SCALE_JITTER},
        mode="sequence",
        transform=tfm.Transform(
            tfm.ToTensorAndJitter(0.2),
            tfm.RandomHorizontalFlip_Norm(probability=0.5),
            tfm.Normalize(mean=cfg.DATA.MEAN, std=cfg.DATA.STD),
        ),
        joint_transform=tfm.Transform(tfm.ToGrayscale(probability=0.05), tfm.RandomHorizontalFlip(probability=0.5)),
        degradation_cfg=cfg.DATA.DEGRADATION,
        feature_consistency_cfg=cfg.TRAIN.FEATURE_CONSISTENCY,
    )
    processed = processor(TensorDict({
        "template_images": template_frames,
        "template_anno": template_anno["bbox"],
        "template_masks": [torch.zeros((height, width))],
        "search_images": search_frames,
        "search_anno": search_anno["bbox"],
        "search_masks": [torch.zeros((height, width))],
    }))
    if not processed.get("valid", False):
        raise AssertionError("Feature consistency processing sample was invalid.")
    if "search_images_clean" not in processed:
        raise AssertionError("STARKProcessing did not produce search_images_clean.")
    if tuple(processed["search_images_clean"].shape) != tuple(processed["search_images"].shape):
        raise AssertionError("Clean and degraded search tensor shapes differ.")

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

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.train()

    class _Settings:
        batchsize = 1
        num_template = 1
        num_search = 1

    objective = {
        "giou": giou_loss,
        "l1": torch.nn.functional.l1_loss,
        "focal": FocalLoss(),
        "cls": torch.nn.BCEWithLogitsLoss(),
    }
    loss_weight = {"giou": cfg.TRAIN.GIOU_WEIGHT, "l1": cfg.TRAIN.L1_WEIGHT, "focal": 1.0, "cls": 1.0}
    actor = OSTrackActor(net=model, objective=objective, loss_weight=loss_weight, settings=_Settings(), cfg=cfg)

    template = torch.rand(1, 1, 3, cfg.DATA.TEMPLATE.SIZE, cfg.DATA.TEMPLATE.SIZE)
    search_degraded = torch.rand(1, 1, 3, cfg.DATA.SEARCH.SIZE, cfg.DATA.SEARCH.SIZE)
    search_clean = search_degraded.clamp(0.0, 1.0)
    search_degraded = (0.8 * search_clean + 0.2 * torch.rand_like(search_clean)).clamp(0.0, 1.0)
    bbox = torch.tensor([[[0.35, 0.35, 0.25, 0.25]]], dtype=torch.float32)
    data = {
        "template_images": template,
        "search_images": search_degraded,
        "search_images_clean": search_clean,
        "template_anno": bbox.clone(),
        "search_anno": bbox.clone(),
        "epoch": 0,
    }
    data = _move_data_to_device(data, device)

    loss, status = actor(data)
    if not torch.isfinite(loss):
        raise AssertionError("Total loss is not finite.")
    if "Loss/feature_consistency" not in status:
        raise AssertionError("Feature consistency loss was not logged.")
    feature_loss = float(status["Loss/feature_consistency"])
    if not torch.isfinite(torch.tensor(feature_loss)):
        raise AssertionError("Feature consistency loss is not finite.")

    loss.backward()
    trainable_grad_names = [
        name for name, param in model.named_parameters()
        if param.requires_grad and param.grad is not None
    ]
    if not any(name.startswith("rgssb") for name in trainable_grad_names):
        raise AssertionError("No rgssb.* gradients found after backward.")
    if not any(name.startswith("box_head") for name in trainable_grad_names):
        raise AssertionError("No box_head.* gradients found after backward.")

    with torch.no_grad():
        out = model(
            template=data["template_images"][0].view(-1, *data["template_images"].shape[2:]),
            search=data["search_images"][0].view(-1, *data["search_images"].shape[2:]),
            return_search_features=True,
        )
    feature_shape = tuple(out["search_feat_rgssb"].shape)
    _assert("search_feat_rgssb shape", feature_shape == (1, 256, 768))

    print(f"config: {config_path}")
    print(f"device: {device}")
    print(f"MODEL.RGSSB.ENABLE: {cfg.MODEL.RGSSB.ENABLE}")
    print(f"TRAIN.FREEZE_MODE: {cfg.TRAIN.FREEZE_MODE}")
    print(f"TRAIN.FEATURE_CONSISTENCY.ENABLE: {cfg.TRAIN.FEATURE_CONSISTENCY.ENABLE}")
    print(f"TRAIN.FEATURE_CONSISTENCY.WEIGHT: {cfg.TRAIN.FEATURE_CONSISTENCY.WEIGHT}")
    print(f"DATA.DEGRADATION.PROBABILITY: {cfg.DATA.DEGRADATION.PROBABILITY}")
    print(f"lasot_root: {lasot_root.resolve()}")
    print(f"lasot_sequences: {dataset.get_num_sequences()}")
    print(f"sample_sequence: {dataset.sequence_list[0]}")
    print(f"sample_frame_shape: {frames[0].shape}")
    print(f"sample_bbox: {anno['bbox'][0].tolist()}")
    print(f"sample_class: {meta.get('object_class_name')}")
    print(f"processing_search_shape: {tuple(processed['search_images'].shape)}")
    print(f"processing_search_clean_shape: {tuple(processed['search_images_clean'].shape)}")
    print(f"search_feat_rgssb_shape: {feature_shape}")
    print(f"total_loss: {float(loss.detach().cpu()):.6f}")
    print(f"feature_consistency_loss: {feature_loss:.6f}")
    print(f"total_params: {total_params}")
    print(f"trainable_params: {trainable_params}")
    print(f"frozen_params: {frozen_params}")
    print(f"rgssb_trainable_count: {len(rgssb_trainable)}")
    print(f"head_trainable_count: {len(head_trainable)}")
    print(f"backbone_trainable_count: {len(backbone_trainable)}")
    print(f"trainable_grad_count: {len(trainable_grad_names)}")
    print("verification: one mini forward/backward passed")


if __name__ == "__main__":
    main()
