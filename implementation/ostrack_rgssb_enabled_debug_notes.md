# OSTrack RG-SSB Enabled Debug Notes

## Purpose

This adds a safe inference/debug path for RG-SSB without changing the original OSTrack baseline config. The original `vitb_256_mae_ce_32x4_ep300.yaml` remains RG-SSB-disabled. The new debug config enables RG-SSB only for explicit debug runs.

## Debug Config

Created:

```text
external/OSTrack/experiments/ostrack/vitb_256_mae_ce_32x4_ep300_rgssb_debug.yaml
```

It copies the baseline `vitb_256_mae_ce_32x4_ep300.yaml` settings and adds:

```yaml
MODEL:
  RGSSB:
    ENABLE: True
```

All other settings are kept the same.

## Why A Separate Debug Config

A separate config keeps the baseline immutable:

- baseline YAML stays disabled
- baseline checkpoint loading stays `strict=True`
- baseline profile and inference behavior remain unchanged
- RG-SSB debug runs are explicit and easy to identify in logs/results

## Checkpoint Loading

Patched:

```text
external/OSTrack/lib/test/tracker/ostrack.py
```

Behavior:

- If `cfg.MODEL.RGSSB.ENABLE` is `False`, checkpoint loading remains `strict=True`.
- If `cfg.MODEL.RGSSB.ENABLE` is `True`, checkpoint loading uses `strict=False`, prints `missing_keys` and `unexpected_keys`, and notes that missing `rgssb.*` keys are expected for the untrained debug module.

Why `strict=False` is needed:

The original OSTrack checkpoint has no RG-SSB weights. With RG-SSB enabled, the model contains new `rgssb.*` parameters, so strict loading would fail.

Checkpoint path logic was not changed. Because OSTrack constructs the checkpoint path from the config name, the debug config expects:

```text
external/OSTrack/output/checkpoints/train/ostrack/vitb_256_mae_ce_32x4_ep300_rgssb_debug/OSTrack_ep0300.pth.tar
```

Before inference, create a symlink or copy from the original checkpoint path.

## Verification

Compile:

```bash
conda run -n ostrack python -m py_compile \
  external/OSTrack/lib/test/tracker/ostrack.py \
  scripts/verify_ostrack_rgssb_integration.py
```

Integration verification:

```bash
conda run -n ostrack python scripts/verify_ostrack_rgssb_integration.py
```

Result:

```text
RGSSB config exists: True
Baseline config RGSSB ENABLE: False
Debug config RGSSB ENABLE: True
Disabled model active RGSSB: False
Enabled model active RGSSB: True
Disabled params: 92518533
Enabled params: 94598469
Parameter count difference: 2079936
score_map shape: (1, 1, 16, 16)
OSTrack RG-SSB integration verification passed.
```

## RG-SSB Enabled Profile

Command:

```bash
cd external/OSTrack
conda run -n ostrack python tracking/profile_model.py \
  --script ostrack \
  --config vitb_256_mae_ce_32x4_ep300_rgssb_debug
```

Sandboxed run failed because CUDA was not visible. Unsandboxed GPU run passed:

```text
overall macs is  21.974G
overall params is  94.201M
The average overall latency is 19.11 ms
FPS is 52.33 fps
```

## RG-SSB Enabled Car1 Inference

First prepare the debug checkpoint path as a symlink to the original checkpoint:

```bash
mkdir -p external/OSTrack/output/checkpoints/train/ostrack/vitb_256_mae_ce_32x4_ep300_rgssb_debug
ln -sf ../vitb_256_mae_ce_32x4_ep300/OSTrack_ep0300.pth.tar \
  external/OSTrack/output/checkpoints/train/ostrack/vitb_256_mae_ce_32x4_ep300_rgssb_debug/OSTrack_ep0300.pth.tar
```

Then run clean Car1 inference outside the Codex sandbox:

```bash
python3 scripts/run_ostrack_otb_eval.py \
  --clean_otb_root /media/abdel/4484139E5D690B76/otb \
  --eval_otb_root /media/abdel/4484139E5D690B76/otb \
  --sequence Car1 \
  --config vitb_256_mae_ce_32x4_ep300_rgssb_debug \
  --degradation clean \
  --severity none \
  --seed 0 \
  --results_csv experiments/baseline_results.csv
```

## Interpretation Warning

Any RG-SSB-enabled inference result at this stage uses randomly initialized, untrained RG-SSB weights. Treat outputs as debug behavior only, not as final performance or evidence of the method.

## Still Postponed

- training
- degradation token
- memory update
- template-guided scan
- response fusion
- feature consistency loss
- response consistency loss
- final performance claims
