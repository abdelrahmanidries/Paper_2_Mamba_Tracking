#!/usr/bin/env python3
"""Verify the RG-SSB feature+response consistency training path.

This runs one mini forward/backward from the real dataloader path. It does not
run full training or evaluation.
"""

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
                raise RuntimeError("COCO is not used by the response-consistency verifier.")

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


def _assert(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(f"Verification failed for {name}")


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    ostrack_root = repo_root / "external" / "OSTrack"
    config_name = "vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_degraded_3000_featcons_lam002_respcons_debug"
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
    _assert("MODEL.RGSSB.ENABLE", cfg.MODEL.RGSSB.ENABLE is True)
    _assert("TRAIN.FREEZE_MODE", cfg.TRAIN.FREEZE_MODE == "rgssb_head")
    _assert("TRAIN.FEATURE_CONSISTENCY.ENABLE", cfg.TRAIN.FEATURE_CONSISTENCY.ENABLE is True)
    _assert("TRAIN.FEATURE_CONSISTENCY.WEIGHT", abs(float(cfg.TRAIN.FEATURE_CONSISTENCY.WEIGHT) - 0.02) < 1e-12)
    _assert("TRAIN.FEATURE_CONSISTENCY.LOSS", cfg.TRAIN.FEATURE_CONSISTENCY.LOSS == "l1")
    _assert("TRAIN.FEATURE_CONSISTENCY.NORMALIZE", cfg.TRAIN.FEATURE_CONSISTENCY.NORMALIZE is True)
    _assert("TRAIN.FEATURE_CONSISTENCY.DETACH_CLEAN", cfg.TRAIN.FEATURE_CONSISTENCY.DETACH_CLEAN is True)
    _assert("TRAIN.RESPONSE_CONSISTENCY.ENABLE", cfg.TRAIN.RESPONSE_CONSISTENCY.ENABLE is True)
    _assert("TRAIN.RESPONSE_CONSISTENCY.WEIGHT", abs(float(cfg.TRAIN.RESPONSE_CONSISTENCY.WEIGHT) - 0.05) < 1e-12)
    _assert("TRAIN.RESPONSE_CONSISTENCY.LOSS", cfg.TRAIN.RESPONSE_CONSISTENCY.LOSS == "mse")
    _assert("TRAIN.RESPONSE_CONSISTENCY.DETACH_CLEAN", cfg.TRAIN.RESPONSE_CONSISTENCY.DETACH_CLEAN is True)
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

    if "search_images_clean" not in batch:
        raise AssertionError(f"Train batch missing search_images_clean. Keys: {batch_keys}")
    if "search_images_clean" not in val_batch:
        raise AssertionError(f"Val batch missing search_images_clean. Keys: {val_batch_keys}")
    if tuple(batch["search_images"].shape) != tuple(batch["search_images_clean"].shape):
        raise AssertionError("Train clean/degraded search tensor shapes differ.")
    if tuple(val_batch["search_images"].shape) != tuple(val_batch["search_images_clean"].shape):
        raise AssertionError("Val clean/degraded search tensor shapes differ.")

    model = build_ostrack(cfg, training=True)
    trainable_params, frozen_params, trainable_names = apply_freeze_mode(model, cfg)
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
        raise AssertionError("Total loss is not finite.")
    if "Loss/feature_consistency" not in status:
        raise AssertionError("Feature consistency loss was not logged.")
    if "Loss/response_consistency" not in status:
        raise AssertionError("Response consistency loss was not logged.")
    feature_loss = float(status["Loss/feature_consistency"])
    response_loss = float(status["Loss/response_consistency"])
    if not torch.isfinite(torch.tensor(feature_loss)):
        raise AssertionError("Feature consistency loss is not finite.")
    if not torch.isfinite(torch.tensor(response_loss)):
        raise AssertionError("Response consistency loss is not finite.")
    loss.backward()

    trainable_grad_names = [
        name for name, param in model.named_parameters()
        if param.requires_grad and param.grad is not None
    ]
    if not any(name.startswith("rgssb") for name in trainable_grad_names):
        raise AssertionError("No rgssb.* gradients found after backward.")
    if not any(name.startswith("box_head") for name in trainable_grad_names):
        raise AssertionError("No box_head.* gradients found after backward.")

    print(f"config: {config_path}")
    print(f"device: {device}")
    print(f"batch_keys: {batch_keys}")
    print(f"val_batch_keys: {val_batch_keys}")
    print(f"search_images_shape: {tuple(batch['search_images'].shape)}")
    print(f"search_images_clean_shape: {tuple(batch['search_images_clean'].shape)}")
    print(f"total_loss: {float(loss.detach().cpu()):.6f}")
    print(f"feature_consistency_loss: {feature_loss:.6f}")
    print(f"response_consistency_loss: {response_loss:.6f}")
    print(f"trainable_params: {trainable_params}")
    print(f"frozen_params: {frozen_params}")
    print(f"rgssb_trainable_count: {len(rgssb_trainable)}")
    print(f"head_trainable_count: {len(head_trainable)}")
    print(f"backbone_trainable_count: {len(backbone_trainable)}")
    print(f"trainable_grad_count: {len(trainable_grad_names)}")
    print("verification: response-consistency mini forward/backward passed")


if __name__ == "__main__":
    main()
