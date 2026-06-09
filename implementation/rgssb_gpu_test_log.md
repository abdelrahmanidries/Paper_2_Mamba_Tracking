# RG-SSB GPU Test Log

## Purpose

This log records the first standalone GPU test of the minimal Restoration-Guided State Space Block, RG-SSB.

The goal is to verify that the block can run on the local Linux GTX 1080 machine before integration into OSTrack.

## Environment

- Machine: local Linux GPU workstation
- GPU: NVIDIA GeForce GTX 1080, 8 GB VRAM
- Conda environment: ostrack
- Test location: project root
- Module: src/models/rgssb.py

## Test Configuration

Input tensor:

Shape: [2, 256, 768]
Device: CUDA
Requires gradient: True

RG-SSB configuration:

dim: 768
spatial_size: (16, 16)
local_kernel_size: 3
channel_reduction: 4
use_local_branch: True
use_channel_attention: True
use_state_branch: True

## Result

CUDA available: True
GPU: NVIDIA GeForce GTX 1080
Input shape: (2, 256, 768)
Output shape: (2, 256, 768)
Params: 2,079,936
Backward passed: True
Allocated GPU memory MB: 21.62
Reserved GPU memory MB: 44.0

## Interpretation

The standalone RG-SSB block preserves the expected OSTrack insertion shape:

[B, 256, 768] -> [B, 256, 768]

The backward pass works, and the memory usage is small enough for local proof-of-concept testing on the GTX 1080.

This result supports moving to the next step: integrating RG-SSB into OSTrack behind a config flag, disabled by default.

## Important Notes

- This is only a standalone unit/GPU test.
- RG-SSB has not yet been integrated into OSTrack.
- No training has been run with RG-SSB yet.
- The current state-space branch is a lightweight proxy, not the final full Mamba implementation.
