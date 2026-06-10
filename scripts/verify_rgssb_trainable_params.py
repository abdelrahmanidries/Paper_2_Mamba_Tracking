#!/usr/bin/env python3
"""Verify RG-SSB-only trainable parameters for the OSTrack debug config."""

from __future__ import annotations

import os
import sys
from pathlib import Path


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    ostrack_root = repo_root / "external" / "OSTrack"
    config_path = ostrack_root / "experiments" / "ostrack" / "vitb_256_mae_ce_32x4_ep300_rgssb_train_debug.yaml"

    if not ostrack_root.exists():
        raise FileNotFoundError(f"OSTrack root does not exist: {ostrack_root}")
    if not config_path.exists():
        raise FileNotFoundError(f"RG-SSB train debug config does not exist: {config_path}")

    os.chdir(ostrack_root)
    sys.path.insert(0, str(ostrack_root))

    from lib.config.ostrack.config import cfg, update_config_from_file
    from lib.models.ostrack import build_ostrack
    from lib.train.freeze import apply_freeze_mode

    update_config_from_file(str(config_path))
    print(f"config: {config_path}")
    print(f"MODEL.RGSSB.ENABLE: {cfg.MODEL.RGSSB.ENABLE}")
    print(f"TRAIN.FREEZE_MODE: {cfg.TRAIN.FREEZE_MODE}")

    model = build_ostrack(cfg, training=True)
    trainable_params, frozen_params, trainable_names = apply_freeze_mode(model, cfg)

    non_rgssb = [name for name in trainable_names if "rgssb" not in name]
    if non_rgssb:
        raise AssertionError(f"Non-RG-SSB parameters are trainable: {non_rgssb}")
    if not trainable_names:
        raise AssertionError("No trainable RG-SSB parameters found.")

    total_params = trainable_params + frozen_params
    print("trainable parameter names:")
    for name in trainable_names:
        print(f"  {name}")
    print(f"total_params: {total_params}")
    print(f"trainable_params: {trainable_params}")
    print(f"frozen_params: {frozen_params}")
    print("verification: only rgssb.* parameters are trainable")


if __name__ == "__main__":
    main()
