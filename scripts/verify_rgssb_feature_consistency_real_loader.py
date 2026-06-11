#!/usr/bin/env python3
"""Verify feature consistency through the real OSTrack train dataloader path."""

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
                raise RuntimeError("COCO is not used by the real-loader feature-consistency verifier.")

        coco_module.COCO = _COCO
        sys.modules["pycocotools.coco"] = coco_module
        pycocotools_module.coco = coco_module
    if "pycocotools.mask" not in sys.modules:
        mask_module = types.ModuleType("pycocotools.mask")
        sys.modules["pycocotools.mask"] = mask_module
        pycocotools_module.mask = mask_module


def _move_data_to_device(data, device: torch.device):
    for key, value in list(data.items()):
        if torch.is_tensor(value):
            data[key] = value.to(device)
    return data


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    ostrack_root = repo_root / "external" / "OSTrack"
    config_name = "vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_degraded_3000_featcons_debug"
    config_path = ostrack_root / "experiments" / "ostrack" / f"{config_name}.yaml"
    if not config_path.is_file():
        raise FileNotFoundError(f"Missing config: {config_path}")

    os.chdir(ostrack_root)
    sys.path.insert(0, str(ostrack_root))
    _stub_optional_coco_import()

    from lib.config.ostrack.config import cfg, update_config_from_file
    from lib.models.ostrack import build_ostrack
    from lib.train.actors import OSTrackActor
    from lib.train.admin.settings import Settings
    from lib.train.base_functions import build_dataloaders, update_settings
    from lib.train.freeze import apply_freeze_mode
    from lib.utils.box_ops import giou_loss
    from lib.utils.focal_loss import FocalLoss

    update_config_from_file(str(config_path))
    if cfg.MODEL.RGSSB.ENABLE is not True:
        raise AssertionError("MODEL.RGSSB.ENABLE must be True.")
    if cfg.TRAIN.FREEZE_MODE != "rgssb_head":
        raise AssertionError('TRAIN.FREEZE_MODE must be "rgssb_head".')
    if cfg.TRAIN.FEATURE_CONSISTENCY.ENABLE is not True:
        raise AssertionError("TRAIN.FEATURE_CONSISTENCY.ENABLE must be True.")
    if float(cfg.TRAIN.FEATURE_CONSISTENCY.WEIGHT) != 0.05:
        raise AssertionError("TRAIN.FEATURE_CONSISTENCY.WEIGHT must be 0.05.")
    cfg.TRAIN.NUM_WORKER = 0

    settings = Settings()
    settings.script_name = "ostrack"
    settings.config_name = config_name
    settings.project_path = f"train/ostrack/{config_name}"
    settings.local_rank = -1
    settings.save_dir = str(ostrack_root / "output")
    settings.use_lmdb = False
    settings.use_wandb = False
    settings.cfg_file = str(config_path)
    update_settings(settings, cfg)

    loader_train, loader_val = build_dataloaders(cfg, settings)
    batch = next(iter(loader_train))
    val_batch = next(iter(loader_val))
    batch["epoch"] = 1
    val_batch["epoch"] = 1
    batch_keys = sorted(list(batch.keys()))
    val_batch_keys = sorted(list(val_batch.keys()))

    if "search_images" not in batch:
        raise AssertionError("Real train dataloader batch is missing search_images.")
    if "search_images_clean" not in batch:
        raise AssertionError(f"Real train dataloader batch is missing search_images_clean. Keys: {batch_keys}")
    if "search_images" not in val_batch:
        raise AssertionError("Real val dataloader batch is missing search_images.")
    if "search_images_clean" not in val_batch:
        raise AssertionError(f"Real val dataloader batch is missing search_images_clean. Keys: {val_batch_keys}")
    if tuple(batch["search_images"].shape) != tuple(batch["search_images_clean"].shape):
        raise AssertionError(
            "Train search_images and search_images_clean shapes differ: "
            f"{tuple(batch['search_images'].shape)} vs {tuple(batch['search_images_clean'].shape)}"
        )
    if tuple(val_batch["search_images"].shape) != tuple(val_batch["search_images_clean"].shape):
        raise AssertionError(
            "Val search_images and search_images_clean shapes differ: "
            f"{tuple(val_batch['search_images'].shape)} vs {tuple(val_batch['search_images_clean'].shape)}"
        )

    model = build_ostrack(cfg, training=True)
    trainable_params, frozen_params, trainable_names = apply_freeze_mode(model, cfg)
    total_params = trainable_params + frozen_params
    rgssb_trainable = [name for name in trainable_names if name.startswith("rgssb")]
    head_trainable = [name for name in trainable_names if name.startswith("box_head")]
    backbone_trainable = [
        name for name, param in model.named_parameters()
        if name.startswith("backbone") and param.requires_grad
    ]
    if not rgssb_trainable:
        raise AssertionError("No rgssb.* parameters are trainable.")
    if not head_trainable:
        raise AssertionError("No box_head.* parameters are trainable.")
    if backbone_trainable:
        raise AssertionError(f"Backbone parameters must be frozen: {backbone_trainable[:10]}")

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    model.to(device)
    model.train()
    batch = _move_data_to_device(batch, device)

    objective = {
        "giou": giou_loss,
        "l1": torch.nn.functional.l1_loss,
        "focal": FocalLoss(),
        "cls": torch.nn.BCEWithLogitsLoss(),
    }
    loss_weight = {"giou": cfg.TRAIN.GIOU_WEIGHT, "l1": cfg.TRAIN.L1_WEIGHT, "focal": 1.0, "cls": 1.0}
    actor = OSTrackActor(net=model, objective=objective, loss_weight=loss_weight, settings=settings, cfg=cfg)
    loss, status = actor(batch)
    if not torch.isfinite(loss):
        raise AssertionError("Real-batch total loss is not finite.")
    if "Loss/feature_consistency" not in status:
        raise AssertionError("Real-batch feature consistency loss was not logged.")
    feature_loss = float(status["Loss/feature_consistency"])
    if not torch.isfinite(torch.tensor(feature_loss)):
        raise AssertionError("Real-batch feature consistency loss is not finite.")
    loss.backward()

    trainable_grad_names = [
        name for name, param in model.named_parameters()
        if param.requires_grad and param.grad is not None
    ]
    if not any(name.startswith("rgssb") for name in trainable_grad_names):
        raise AssertionError("No rgssb.* gradients found after real-batch backward.")
    if not any(name.startswith("box_head") for name in trainable_grad_names):
        raise AssertionError("No box_head.* gradients found after real-batch backward.")

    print(f"config: {config_path}")
    print(f"device: {device}")
    print(f"batch_keys: {batch_keys}")
    print(f"val_batch_keys: {val_batch_keys}")
    print(f"search_images_shape: {tuple(batch['search_images'].shape)}")
    print(f"search_images_clean_shape: {tuple(batch['search_images_clean'].shape)}")
    print(f"val_search_images_shape: {tuple(val_batch['search_images'].shape)}")
    print(f"val_search_images_clean_shape: {tuple(val_batch['search_images_clean'].shape)}")
    print(f"template_images_shape: {tuple(batch['template_images'].shape)}")
    print(f"search_anno_shape: {tuple(batch['search_anno'].shape)}")
    print(f"total_loss: {float(loss.detach().cpu()):.6f}")
    print(f"feature_consistency_loss: {feature_loss:.6f}")
    print(f"total_params: {total_params}")
    print(f"trainable_params: {trainable_params}")
    print(f"frozen_params: {frozen_params}")
    print(f"rgssb_trainable_count: {len(rgssb_trainable)}")
    print(f"head_trainable_count: {len(head_trainable)}")
    print(f"backbone_trainable_count: {len(backbone_trainable)}")
    print(f"trainable_grad_count: {len(trainable_grad_names)}")
    print("verification: real dataloader feature-consistency forward/backward passed")


if __name__ == "__main__":
    main()
