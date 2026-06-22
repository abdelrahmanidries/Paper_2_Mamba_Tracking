#!/usr/bin/env python3
"""Verify the gated RG-SSB target-vs-distractor margin ablation.

This runs one mini forward/backward from the dataloader path. It does not run
full training or evaluation.
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
                raise RuntimeError("COCO is not used by the target-distractor verifier.")

        coco_module.COCO = _COCO
        sys.modules["pycocotools.coco"] = coco_module
        pycocotools_module.coco = coco_module
    if "pycocotools.mask" not in sys.modules:
        mask_module = types.ModuleType("pycocotools.mask")
        sys.modules["pycocotools.mask"] = mask_module
        pycocools_mask = mask_module
        pycocotools_module.mask = pycocools_mask


def _move_data_to_device(data, device: torch.device):
    for key, value in list(data.items()):
        if torch.is_tensor(value):
            data[key] = value.to(device)
    return data


def _assert(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(f"Verification failed for {name}")


def _grad_names(model) -> list[str]:
    return [name for name, param in model.named_parameters() if param.requires_grad and param.grad is not None]


def _clear_grads(model) -> None:
    model.zero_grad(set_to_none=True)


def _synthetic_positive_margin_case(actor, device: torch.device) -> tuple[float, float, float, float, float]:
    score_map = torch.zeros((1, 1, 16, 16), device=device, requires_grad=True)
    score_map.data[:, :, 1, 1] = 0.9
    score_map.data[:, :, 7, 7] = 0.1
    search_anno = torch.tensor([[[0.43, 0.43, 0.12, 0.12]]], device=device, dtype=torch.float32)
    pred = {"score_map": score_map}
    gt = {"search_anno": search_anno}
    loss, stats = actor.compute_target_distractor_margin_loss(pred, gt)
    if not torch.isfinite(loss) or float(loss.detach().cpu()) <= 0.0:
        raise AssertionError("Synthetic positive margin case did not produce positive finite loss.")
    loss.backward()
    if score_map.grad is None or not torch.isfinite(score_map.grad).all() or float(score_map.grad.abs().sum().detach().cpu()) <= 0.0:
        raise AssertionError("Synthetic positive margin case did not propagate gradients through response map.")
    target_score = float(stats["target_score"].detach().cpu())
    distractor_score = float(stats["distractor_score"].detach().cpu())
    gap = float(stats["margin_gap"].detach().cpu())
    margin_loss = float(loss.detach().cpu())
    violation_rate = float((torch.relu(0.2 - stats["margin_gap"]) > 0).float().mean().detach().cpu())
    return target_score, distractor_score, gap, margin_loss, violation_rate


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    ostrack_root = repo_root / "external" / "OSTrack"
    config_name = "vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_degraded_3000_featcons_lam002_tdm_debug"
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
    _assert("TRAIN.RESPONSE_CONSISTENCY.ENABLE", cfg.TRAIN.RESPONSE_CONSISTENCY.ENABLE is False)
    _assert("TRAIN.TARGET_FEATURE_CONSISTENCY.ENABLE", cfg.TRAIN.TARGET_FEATURE_CONSISTENCY.ENABLE is False)
    _assert("TRAIN.TARGET_DISTRACTOR_MARGIN.ENABLE", cfg.TRAIN.TARGET_DISTRACTOR_MARGIN.ENABLE is True)
    _assert("TRAIN.TARGET_DISTRACTOR_MARGIN.WEIGHT", abs(float(cfg.TRAIN.TARGET_DISTRACTOR_MARGIN.WEIGHT) - 0.05) < 1e-12)
    _assert("TRAIN.TARGET_DISTRACTOR_MARGIN.MARGIN", abs(float(cfg.TRAIN.TARGET_DISTRACTOR_MARGIN.MARGIN) - 0.2) < 1e-12)
    _assert("TRAIN.TARGET_DISTRACTOR_MARGIN.LOSS", cfg.TRAIN.TARGET_DISTRACTOR_MARGIN.LOSS == "hinge")
    _assert("TRAIN.TARGET_DISTRACTOR_MARGIN.TARGET_POOLING", cfg.TRAIN.TARGET_DISTRACTOR_MARGIN.TARGET_POOLING == "max")
    _assert("TRAIN.TARGET_DISTRACTOR_MARGIN.DISTRACTOR_POOLING", cfg.TRAIN.TARGET_DISTRACTOR_MARGIN.DISTRACTOR_POOLING == "max")
    _assert("TRAIN.TARGET_DISTRACTOR_MARGIN.TARGET_SCALE", abs(float(cfg.TRAIN.TARGET_DISTRACTOR_MARGIN.TARGET_SCALE) - 1.0) < 1e-12)
    _assert("TRAIN.TARGET_DISTRACTOR_MARGIN.IGNORE_RING", int(cfg.TRAIN.TARGET_DISTRACTOR_MARGIN.IGNORE_RING) == 1)
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
    first_batch = next(iter(loader_train))
    first_batch["epoch"] = 1
    batch_keys = sorted(list(first_batch.keys()))
    if "search_anno" not in first_batch:
        raise AssertionError(f"Train batch missing search_anno. Keys: {batch_keys}")
    if "search_images_clean" not in first_batch:
        raise AssertionError(f"Train batch missing search_images_clean. Keys: {batch_keys}")
    if tuple(first_batch["search_images"].shape) != tuple(first_batch["search_images_clean"].shape):
        raise AssertionError("Clean/degraded search tensor shapes differ.")

    model = build_ostrack(cfg, training=True)
    trainable_params, frozen_params, trainable_names = apply_freeze_mode(model, cfg)
    rgssb_trainable = [name for name in trainable_names if name.startswith("rgssb")]
    head_trainable = [name for name in trainable_names if name.startswith("box_head")]
    non_allowed = [name for name in trainable_names if not (name.startswith("rgssb") or name.startswith("box_head"))]
    backbone_trainable = [name for name, param in model.named_parameters() if name.startswith("backbone") and param.requires_grad]
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
    first_batch = _move_data_to_device(first_batch, device)

    objective = {
        "giou": giou_loss,
        "l1": torch.nn.functional.l1_loss,
        "focal": FocalLoss(),
        "cls": torch.nn.BCEWithLogitsLoss(),
    }
    loss_weight = {"giou": cfg.TRAIN.GIOU_WEIGHT, "l1": cfg.TRAIN.L1_WEIGHT, "focal": 1.0, "cls": 1.0}
    actor = OSTrackActor(net=model, objective=objective, loss_weight=loss_weight, settings=settings, cfg=cfg)

    with torch.no_grad():
        out = model(
            template=first_batch["template_images"][0].view(-1, *first_batch["template_images"].shape[2:]),
            search=first_batch["search_images"][0].view(-1, *first_batch["search_images"].shape[2:]),
            return_search_features=True,
        )
    score_map = out["score_map"]
    target_mask, distractor_mask = actor.build_response_target_masks(
        first_batch["search_anno"][-1],
        score_map.shape,
        device=score_map.device,
        dtype=score_map.dtype,
    )
    if tuple(target_mask.shape) != tuple(score_map.shape):
        raise AssertionError(f"Target mask shape mismatch: target={tuple(target_mask.shape)} score={tuple(score_map.shape)}")
    if tuple(distractor_mask.shape) != tuple(score_map.shape):
        raise AssertionError(f"Distractor mask shape mismatch: distractor={tuple(distractor_mask.shape)} score={tuple(score_map.shape)}")
    if not target_mask.any():
        raise AssertionError("Target mask is empty.")
    if not distractor_mask.any():
        raise AssertionError("Distractor mask is empty.")

    violating_batch = None
    violating_stats = None
    violating_margin_loss = None
    scanned_batches = 0
    iterator = iter(loader_train)
    for scanned_batches, candidate in enumerate(iterator, start=1):
        if scanned_batches > 50:
            scanned_batches = 50
            break
        candidate["epoch"] = 1
        candidate = _move_data_to_device(candidate, device)
        with torch.no_grad():
            candidate_out = actor.forward_pass(candidate)
            candidate_loss, candidate_stats = actor.compute_target_distractor_margin_loss(candidate_out, candidate)
        candidate_loss_value = float(candidate_loss.detach().cpu())
        if candidate_loss_value > 1e-8:
            violating_batch = candidate
            violating_stats = candidate_stats
            violating_margin_loss = candidate_loss_value
            break

    positive_branch_source = "real_batch"
    margin_only_box_head_grad = False
    if violating_batch is not None:
        _clear_grads(model)
        violating_out = actor.forward_pass(violating_batch)
        margin_only_loss, margin_only_stats = actor.compute_target_distractor_margin_loss(violating_out, violating_batch)
        if not torch.isfinite(margin_only_loss) or float(margin_only_loss.detach().cpu()) <= 0.0:
            raise AssertionError("Real violating batch did not produce positive finite margin loss during backward check.")
        margin_only_loss.backward()
        margin_only_grad_names = _grad_names(model)
        margin_only_box_head_grad = any(name.startswith("box_head") for name in margin_only_grad_names)
        if not margin_only_box_head_grad:
            raise AssertionError("Margin-only loss did not produce box_head.* gradients on the real violating batch.")
        target_score = float(margin_only_stats["target_score"].detach().cpu())
        distractor_score = float(margin_only_stats["distractor_score"].detach().cpu())
        margin_gap = float(margin_only_stats["margin_gap"].detach().cpu())
        positive_margin_loss = float(margin_only_loss.detach().cpu())
        violation_rate = 1.0
        total_batch = violating_batch
    else:
        positive_branch_source = "synthetic_response"
        target_score, distractor_score, margin_gap, positive_margin_loss, violation_rate = _synthetic_positive_margin_case(actor, device)
        total_batch = first_batch

    _clear_grads(model)
    loss, status = actor(total_batch)
    if not torch.isfinite(loss):
        raise AssertionError("Total loss is not finite.")
    required_status = [
        "Loss/feature_consistency",
        "Loss/target_distractor_margin",
        "TargetDistractor/target_score",
        "TargetDistractor/distractor_score",
        "TargetDistractor/margin_gap",
    ]
    for key in required_status:
        if key not in status:
            raise AssertionError(f"Missing status key: {key}")
    if "Loss/response_consistency" in status:
        raise AssertionError("Response consistency should be disabled in this config.")
    if "Loss/target_feature_consistency" in status:
        raise AssertionError("Target feature consistency should be disabled in this config.")
    margin_loss = float(status["Loss/target_distractor_margin"])
    feature_loss = float(status["Loss/feature_consistency"])
    if not torch.isfinite(torch.tensor(margin_loss)):
        raise AssertionError("Target-distractor margin loss is not finite.")
    if not torch.isfinite(torch.tensor(feature_loss)):
        raise AssertionError("Feature consistency loss is not finite.")
    loss.backward()

    trainable_grad_names = _grad_names(model)
    if not any(name.startswith("rgssb") for name in trainable_grad_names):
        raise AssertionError("No rgssb.* gradients found after backward.")
    if not any(name.startswith("box_head") for name in trainable_grad_names):
        raise AssertionError("No box_head.* gradients found after backward.")

    print(f"config: {config_path}")
    print(f"device: {device}")
    print(f"response_key: score_map")
    print(f"response_shape: {tuple(score_map.shape)}")
    print("response_values: sigmoid-clamped probabilities from CenterPredictor.get_score_map")
    print("search_anno_convention: normalized xywh in search crop coordinates")
    print(f"target_mask_shape: {tuple(target_mask.shape)}")
    print(f"target_mask_count: {int(target_mask.sum().detach().cpu())}")
    print(f"distractor_mask_count: {int(distractor_mask.sum().detach().cpu())}")
    print(f"total_loss: {float(loss.detach().cpu()):.6f}")
    print(f"feature_consistency_loss: {feature_loss:.6f}")
    print(f"target_distractor_margin_loss: {margin_loss:.6f}")
    print(f"positive_branch_source: {positive_branch_source}")
    print(f"real_batches_scanned: {scanned_batches}")
    print(f"real_violating_batch_found: {violating_batch is not None}")
    print(f"positive_margin_loss: {positive_margin_loss:.6f}")
    print(f"positive_target_score: {target_score:.6f}")
    print(f"positive_distractor_score: {distractor_score:.6f}")
    print(f"positive_achieved_gap: {margin_gap:.6f}")
    print(f"positive_violation_rate: {violation_rate:.6f}")
    print(f"margin_only_box_head_grad: {margin_only_box_head_grad if violating_batch is not None else 'synthetic_only'}")
    print(f"target_score: {float(status['TargetDistractor/target_score']):.6f}")
    print(f"distractor_score: {float(status['TargetDistractor/distractor_score']):.6f}")
    print(f"margin_gap: {float(status['TargetDistractor/margin_gap']):.6f}")
    print(f"trainable_params: {trainable_params}")
    print(f"frozen_params: {frozen_params}")
    print(f"rgssb_trainable_count: {len(rgssb_trainable)}")
    print(f"head_trainable_count: {len(head_trainable)}")
    print(f"backbone_trainable_count: {len(backbone_trainable)}")
    print(f"trainable_grad_count: {len(trainable_grad_names)}")
    print("verification: target-distractor margin mini forward/backward passed")


if __name__ == "__main__":
    main()
