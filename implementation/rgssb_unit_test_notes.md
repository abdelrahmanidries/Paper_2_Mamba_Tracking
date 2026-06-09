# RG-SSB Unit Test Notes

## What Was Implemented

Implemented a standalone `RestorationGuidedSSB` module in `src/models/rgssb.py` with a token-preserving interface:

```text
[B, N, C] -> [B, N, C]
```

For the first planned OSTrack insertion, the expected input is:

```text
[B, 256, 768] -> [B, 256, 768]
```

The block includes:

- residual connection
- LayerNorm over token channels
- local enhancement branch using token-to-map reshape, depthwise convolution, pointwise convolution, and GELU
- squeeze-excitation style channel attention
- lightweight SSM-style proxy using gated depthwise 1D convolution over the token sequence
- output projection
- optional dropout

## Why This Is Minimal

This is a proof-of-concept feature block for checking shape safety, gradient flow, parameter scale, and later OSTrack insertion after the backbone output. It intentionally preserves the input shape and avoids changing the tracking head contract.

## Why This Is Not the Final Method

The state branch is a dependency-free scan-style proxy, not a full Mamba implementation. It does not yet include MambaIR/MambaIRv2-style full restoration design, degradation-aware modulation, template-search interaction changes, memory, or response fusion.

## Expected OSTrack Insertion Point

The intended first integration point remains:

- after OSTrack backbone output
- before the tracking head
- search-token path only
- shape: `[B, 256, 768] -> [B, 256, 768]`

The module can internally reshape search tokens to `[B, 768, 16, 16]` when `spatial_size=(16, 16)`.

## Postponed

- degradation token
- template-guided attentive scan
- degradation-aware memory update
- restoration-guided response fusion
- full Mamba dependency
- clean/degraded feature consistency loss
- response consistency loss
- OSTrack integration
- training code

## Running Unit Tests

Use the OSTrack conda environment because it has PyTorch:

```bash
conda run -n ostrack python -m pytest tests/test_rgssb.py
```

Shape and parameter smoke check:

```bash
conda run -n ostrack python - <<'PY'
import torch
from src.models.rgssb import RestorationGuidedSSB
m = RestorationGuidedSSB(dim=768, spatial_size=(16, 16))
x = torch.randn(1, 256, 768)
y = m(x)
print(x.shape, y.shape)
print("params:", sum(p.numel() for p in m.parameters()))
PY
```
