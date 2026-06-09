# OSTrack RG-SSB Integration Notes

## Scope

This integration adds a minimal Restoration-Guided State Space Block, RG-SSB, to OSTrack behind a config flag. The flag is disabled by default, so the existing OSTrack baseline path remains unchanged unless explicitly enabled later.

No training was run. No datasets, paper reports, or OSTrack checkpoint paths were modified.

## External OSTrack Files Modified

- `external/OSTrack/lib/models/layers/rgssb.py`
- `external/OSTrack/lib/config/ostrack/config.py`
- `external/OSTrack/lib/models/ostrack/ostrack.py`

## Main Project Files Created

- `scripts/verify_ostrack_rgssb_integration.py`
- `implementation/ostrack_rgssb_integration_notes.md`
- `implementation/patches/ostrack_rgssb_integration.patch`

## Insertion Point

The insertion point follows `implementation/ostrack_rgssb_insertion_plan.md`:

- after OSTrack backbone output
- before the tracking head
- search-token path only

In `external/OSTrack/lib/models/ostrack/ostrack.py`, `OSTrack.forward_head()` slices search tokens:

```python
enc_opt = cat_feature[:, -self.feat_len_s:]
```

When RG-SSB is enabled, the integration applies:

```python
enc_opt = self.rgssb(
    enc_opt,
    search_len=self.feat_len_s,
    spatial_size=(self.feat_sz_s, self.feat_sz_s),
)
```

Expected tensor shape:

```text
[B, 256, 768] -> [B, 256, 768]
```

The block can internally reshape to:

```text
[B, 256, 768] -> [B, 768, 16, 16] -> [B, 256, 768]
```

## Config Flags Added

Added to `external/OSTrack/lib/config/ostrack/config.py`:

```python
cfg.MODEL.RGSSB = edict()
cfg.MODEL.RGSSB.ENABLE = False
cfg.MODEL.RGSSB.DIM = 768
cfg.MODEL.RGSSB.SPATIAL_SIZE = [16, 16]
cfg.MODEL.RGSSB.LOCAL_KERNEL_SIZE = 3
cfg.MODEL.RGSSB.CHANNEL_REDUCTION = 4
cfg.MODEL.RGSSB.USE_LOCAL_BRANCH = True
cfg.MODEL.RGSSB.USE_CHANNEL_ATTENTION = True
cfg.MODEL.RGSSB.USE_STATE_BRANCH = True
```

Default is `ENABLE = False`.

## Why Disabled by Default

Disabled-by-default preserves the baseline:

- no active RG-SSB module is created
- original strict checkpoint loading still works
- output tensor shapes and head path are unchanged
- profiling with the existing `vitb_256_mae_ce_32x4_ep300` config should match the original baseline

## How to Enable Later

Do not edit the original baseline YAML for experiments. Create a new RG-SSB YAML later and set:

```yaml
MODEL:
  RGSSB:
    ENABLE: True
```

Additional branch flags can be changed for ablation, but the first enabled run should keep all branches on.

## Checkpoint Loading Risk

Current test-time checkpoint loading in `external/OSTrack/lib/test/tracker/ostrack.py` remains:

```python
network.load_state_dict(torch.load(self.params.checkpoint, map_location='cpu')['net'], strict=True)
```

With `RGSSB.ENABLE=False`, this is correct and should continue to load original OSTrack checkpoints.

With `RGSSB.ENABLE=True`, the original checkpoint will likely fail with `strict=True` because `rgssb.*` parameters are new and absent from the checkpoint. The future enabled path should conditionally use `strict=False` and verify missing keys are limited to RG-SSB parameters.

## Tests Run

Compile:

```bash
conda run -n ostrack python -m py_compile \
  external/OSTrack/lib/models/layers/rgssb.py \
  scripts/verify_ostrack_rgssb_integration.py
```

Standalone RG-SSB tests:

```bash
conda run -n ostrack python -m pytest tests/test_rgssb.py
```

Result:

```text
11 passed in 1.06s
```

Integration verification:

```bash
conda run -n ostrack python scripts/verify_ostrack_rgssb_integration.py
```

Result:

```text
RGSSB config exists: True
RGSSB default ENABLE: False
Disabled model active RGSSB: False
Enabled model active RGSSB: True
Synthetic cat_feature shape: (1, 320, 768)
pred_boxes shape: (1, 1, 4)
score_map shape: (1, 1, 16, 16)
size_map shape: (1, 2, 16, 16)
offset_map shape: (1, 2, 16, 16)
OSTrack RG-SSB integration verification passed.
```

Baseline profile with RG-SSB disabled:

```bash
cd external/OSTrack
conda run -n ostrack python tracking/profile_model.py --script ostrack --config vitb_256_mae_ce_32x4_ep300
```

Sandboxed run failed because CUDA was not visible. Unsandboxed run succeeded:

```text
overall macs is  21.517G
overall params is  92.121M
The average overall latency is 18.61 ms
FPS is 53.74 fps
```

This is consistent with the earlier disabled baseline profile.

## Reproducibility Patch

Patch file:

```text
implementation/patches/ostrack_rgssb_integration.patch
```

The patch includes:

- added RG-SSB config defaults
- config-gated `OSTrack.forward_head()` insertion
- new `lib/models/layers/rgssb.py`

## Postponed

- degradation token
- template-guided attentive scan
- memory update
- response fusion
- full Mamba dependency
- feature consistency loss
- response consistency loss
- checkpoint loading change for enabled RG-SSB
- training code
- full degradation suite with enabled RG-SSB

## Next Safe Step

Create a separate RG-SSB experiment YAML and then update checkpoint loading only for `RGSSB.ENABLE=True`. After that, run a one-forward model check and one clean Car1 inference before any degraded inference.
