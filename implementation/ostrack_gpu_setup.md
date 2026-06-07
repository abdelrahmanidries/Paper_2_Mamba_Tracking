# OSTrack GPU Setup

## Machine

Linux GPU workstation.

## GPU

NVIDIA GeForce GTX 1080, 8 GB VRAM.

## NVIDIA Driver

535.309.01.

## CUDA shown by nvidia-smi

12.2.

## OSTrack Conda Environment

Environment name: ostrack.

## PyTorch Verification

```text
torch: 1.10.0
cuda available: True
cuda runtime: 11.3
GPU: NVIDIA GeForce GTX 1080
```

## Dependency Verification

```text
OSTrack dependencies OK
OSTTrack config import OK
```

## OSTrack Local Path Setup

The following files were created successfully:

```text
external/OSTrack/lib/train/admin/local.py
external/OSTrack/lib/test/evaluation/local.py
```

## OSTrack Profile Smoke Test

Command:

```bash
python tracking/profile_model.py --script ostrack --config vitb_256_mae_ce_32x4_ep300
```

Result:

```text
overall macs is 21.517G
overall params is 92.121M
average latency is 18.54 ms
FPS is 53.93 fps
```

## Role of This Machine

This GTX 1080 machine will be used for proof-of-training and debugging only:

- OSTrack smoke tests
- small clean/degraded baseline checks
- minimal proof-of-concept training
- debugging before HPC jobs

Full training and final experiments will be performed on the university HPC.

## Environment Separation

The project `.venv` is used for degradation scripts and project utilities.

The `ostrack` Conda environment is used for OSTrack training/evaluation.
