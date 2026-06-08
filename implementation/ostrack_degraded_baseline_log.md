# OSTrack Degraded Baseline Log

## Purpose

This log records the first degraded baseline test for OSTrack on a local Linux GTX 1080 workstation.

The goal is to verify whether a standard RGB tracker suffers measurable performance degradation under synthetic image degradation before implementing any proposed restoration-guided Mamba module.

## Base Tracker

- Tracker: OSTrack
- Config: vitb_256_mae_ce_32x4_ep300
- Checkpoint: OSTrack_ep0300.pth.tar
- Dataset: OTB Car1
- Machine: local Linux GTX 1080 workstation

## Clean Baseline: Car1

```text
Frames: 1020
Mean IoU: 0.5755
Success AUC: 0.5760
Precision @20px: 0.7461
Mean center error: 16.46 px

Degradation type: motion_blur
Severity: medium
Seed: 42
Frames: 1020
Ground-truth lines: 1020


Frames: 1020
Mean IoU: 0.1502
Success AUC: 0.1572
Precision @20px: 0.1980
Mean center error: 82.96 px

Mean IoU drop: 0.4253
Success AUC drop: 0.4188
Precision @20px drop: 0.5480
Mean center error increase: 66.50 px
