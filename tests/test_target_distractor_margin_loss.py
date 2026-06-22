from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
import torch


ROOT = Path(__file__).resolve().parents[1]
OSTRACK_ROOT = ROOT / "external" / "OSTrack"
if str(OSTRACK_ROOT) not in sys.path:
    sys.path.insert(0, str(OSTRACK_ROOT))

import types

tensorboardx = types.ModuleType("tensorboardX")


class _SummaryWriter:
    def __init__(self, *args, **kwargs):
        pass

    def add_scalar(self, *args, **kwargs):
        pass

    def close(self):
        pass


tensorboardx.SummaryWriter = _SummaryWriter
sys.modules.setdefault("tensorboardX", tensorboardx)

from lib.train.actors.ostrack import OSTrackActor


def make_actor(ignore_ring=1, target_scale=1.0):
    cfg = SimpleNamespace(
        TRAIN=SimpleNamespace(
            TARGET_DISTRACTOR_MARGIN=SimpleNamespace(
                ENABLE=True,
                WEIGHT=0.05,
                MARGIN=0.2,
                LOSS="hinge",
                TARGET_POOLING="max",
                DISTRACTOR_POOLING="max",
                TARGET_SCALE=target_scale,
                IGNORE_RING=ignore_ring,
            ),
            FEATURE_CONSISTENCY=SimpleNamespace(ENABLE=False),
            TARGET_FEATURE_CONSISTENCY=SimpleNamespace(ENABLE=False),
            RESPONSE_CONSISTENCY=SimpleNamespace(ENABLE=False),
        )
    )
    return OSTrackActor(net=None, objective={}, loss_weight={}, settings=SimpleNamespace(batchsize=1), cfg=cfg)


def test_positive_hinge_loss_case():
    actor = make_actor(ignore_ring=0)
    score = torch.zeros((1, 1, 4, 4), requires_grad=True)
    score.data[:, :, 0, 0] = 0.9
    score.data[:, :, 1, 1] = 0.1
    gt = {"search_anno": torch.tensor([[[0.25, 0.25, 0.25, 0.25]]], dtype=torch.float32)}

    loss, stats = actor.compute_target_distractor_margin_loss({"score_map": score}, gt)

    assert loss.item() == pytest.approx(1.0)
    assert stats["target_score"].item() == pytest.approx(0.1)
    assert stats["distractor_score"].item() == pytest.approx(0.9)


def test_zero_loss_satisfied_margin_case():
    actor = make_actor(ignore_ring=0)
    score = torch.zeros((1, 1, 4, 4), requires_grad=True)
    score.data[:, :, 0, 0] = 0.1
    score.data[:, :, 1, 1] = 0.9
    gt = {"search_anno": torch.tensor([[[0.25, 0.25, 0.25, 0.25]]], dtype=torch.float32)}

    loss, stats = actor.compute_target_distractor_margin_loss({"score_map": score}, gt)

    assert loss.item() == pytest.approx(0.0)
    assert stats["margin_gap"].item() == pytest.approx(0.8)


def test_target_and_distractor_masks_non_empty():
    actor = make_actor(ignore_ring=1)
    anno = torch.tensor([[0.25, 0.25, 0.25, 0.25]], dtype=torch.float32)

    target_mask, distractor_mask = actor.build_response_target_masks(anno, (1, 1, 8, 8))

    assert target_mask.any()
    assert distractor_mask.any()
    assert target_mask.shape == (1, 1, 8, 8)
    assert distractor_mask.shape == (1, 1, 8, 8)


def test_ignore_ring_reduces_distractor_pool():
    anno = torch.tensor([[0.25, 0.25, 0.25, 0.25]], dtype=torch.float32)
    no_ring_actor = make_actor(ignore_ring=0)
    ring_actor = make_actor(ignore_ring=1)

    _, distractor_no_ring = no_ring_actor.build_response_target_masks(anno, (1, 1, 8, 8))
    _, distractor_ring = ring_actor.build_response_target_masks(anno, (1, 1, 8, 8))

    assert distractor_ring.sum().item() < distractor_no_ring.sum().item()


def test_partially_out_of_bounds_target_box():
    actor = make_actor(ignore_ring=0)
    anno = torch.tensor([[-0.2, -0.1, 0.4, 0.4]], dtype=torch.float32)

    target_mask, distractor_mask = actor.build_response_target_masks(anno, (1, 1, 8, 8))

    assert target_mask.any()
    assert distractor_mask.any()


def test_three_dimensional_response_shape_supported():
    actor = make_actor(ignore_ring=0)
    score = torch.zeros((1, 4, 4), requires_grad=True)
    score.data[:, 0, 0] = 0.9
    score.data[:, 1, 1] = 0.1
    gt = {"search_anno": torch.tensor([[[0.25, 0.25, 0.25, 0.25]]], dtype=torch.float32)}

    loss, _ = actor.compute_target_distractor_margin_loss({"score_map": score}, gt)

    assert loss.item() > 0


def test_four_dimensional_response_shape_supported():
    actor = make_actor(ignore_ring=0)
    score = torch.zeros((1, 1, 4, 4), requires_grad=True)
    score.data[:, :, 0, 0] = 0.9
    score.data[:, :, 1, 1] = 0.1
    gt = {"search_anno": torch.tensor([[[0.25, 0.25, 0.25, 0.25]]], dtype=torch.float32)}

    loss, _ = actor.compute_target_distractor_margin_loss({"score_map": score}, gt)

    assert loss.item() > 0


def test_gradients_propagate_through_response_map():
    actor = make_actor(ignore_ring=0)
    score = torch.zeros((1, 1, 4, 4), requires_grad=True)
    score.data[:, :, 0, 0] = 0.9
    score.data[:, :, 1, 1] = 0.1
    gt = {"search_anno": torch.tensor([[[0.25, 0.25, 0.25, 0.25]]], dtype=torch.float32)}

    loss, _ = actor.compute_target_distractor_margin_loss({"score_map": score}, gt)
    loss.backward()

    assert score.grad is not None
    assert torch.isfinite(score.grad).all()
    assert score.grad.abs().sum().item() > 0


def test_empty_distractor_mask_raises_clear_error():
    actor = make_actor(ignore_ring=0)
    anno = torch.tensor([[0.0, 0.0, 1.0, 1.0]], dtype=torch.float32)

    with pytest.raises(ValueError, match="empty distractor mask"):
        actor.build_response_target_masks(anno, (1, 1, 1, 1))


def test_invalid_multichannel_response_raises_clear_error():
    actor = make_actor(ignore_ring=0)
    score = torch.zeros((1, 2, 4, 4), requires_grad=True)
    gt = {"search_anno": torch.tensor([[[0.25, 0.25, 0.25, 0.25]]], dtype=torch.float32)}

    with pytest.raises(ValueError, match="single-channel response map"):
        actor.compute_target_distractor_margin_loss({"score_map": score}, gt)
