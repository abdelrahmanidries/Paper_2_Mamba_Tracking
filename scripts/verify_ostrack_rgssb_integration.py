"""Verify the minimal OSTrack RG-SSB integration without running training."""

from __future__ import annotations

import copy
import sys
from pathlib import Path

import torch


ROOT = Path(__file__).resolve().parents[1]
OSTRACK_ROOT = ROOT / "external" / "OSTrack"
if str(OSTRACK_ROOT) not in sys.path:
    sys.path.insert(0, str(OSTRACK_ROOT))

from lib.config.ostrack.config import cfg, update_config_from_file
from lib.models.layers.rgssb import RestorationGuidedSSB
from lib.models.ostrack import build_ostrack


def has_active_rgssb(model: torch.nn.Module) -> bool:
    return any(isinstance(module, RestorationGuidedSSB) for module in model.modules())


def main() -> int:
    config_path = OSTRACK_ROOT / "experiments" / "ostrack" / "vitb_256_mae_ce_32x4_ep300.yaml"
    update_config_from_file(str(config_path))

    has_config = hasattr(cfg.MODEL, "RGSSB")
    print(f"RGSSB config exists: {has_config}")
    if not has_config:
        raise RuntimeError("cfg.MODEL.RGSSB is missing")
    print(f"RGSSB default ENABLE: {cfg.MODEL.RGSSB.ENABLE}")

    disabled_cfg = copy.deepcopy(cfg)
    disabled_cfg.MODEL.RGSSB.ENABLE = False
    disabled_model = build_ostrack(disabled_cfg, training=False)
    print(f"Disabled model active RGSSB: {has_active_rgssb(disabled_model)}")
    if has_active_rgssb(disabled_model):
        raise RuntimeError("RG-SSB should not be active when disabled")

    enabled_cfg = copy.deepcopy(cfg)
    enabled_cfg.MODEL.RGSSB.ENABLE = True
    enabled_model = build_ostrack(enabled_cfg, training=False)
    print(f"Enabled model active RGSSB: {has_active_rgssb(enabled_model)}")
    if not has_active_rgssb(enabled_model):
        raise RuntimeError("RG-SSB should be active when enabled")

    enabled_model.eval()
    batch = 1
    template_tokens = 64
    search_tokens = 256
    dim = enabled_cfg.MODEL.RGSSB.DIM
    cat_feature = torch.randn(batch, template_tokens + search_tokens, dim)
    with torch.no_grad():
        out = enabled_model.forward_head(cat_feature)

    print(f"Synthetic cat_feature shape: {tuple(cat_feature.shape)}")
    print(f"pred_boxes shape: {tuple(out['pred_boxes'].shape)}")
    print(f"score_map shape: {tuple(out['score_map'].shape)}")
    print(f"size_map shape: {tuple(out['size_map'].shape)}")
    print(f"offset_map shape: {tuple(out['offset_map'].shape)}")

    expected_score_shape = (batch, 1, 16, 16)
    if tuple(out["score_map"].shape) != expected_score_shape:
        raise RuntimeError(f"Unexpected score_map shape: {tuple(out['score_map'].shape)}")

    print("OSTrack RG-SSB integration verification passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
