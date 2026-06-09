# OSTrack Visual Degradation Debug Log

## Purpose

This log records the first visual comparison between clean OSTrack predictions and degraded OSTrack predictions on OTB Car1 under medium motion blur.

The goal is to verify visually that the synthetic degradation causes tracking drift, not only a numerical metric drop.

## Sequence

- Dataset: OTB
- Sequence: Car1
- Degradation: motion_blur
- Severity: medium
- Seed: 42
- Tracker: OSTrack
- Config: vitb_256_mae_ce_32x4_ep300
- Checkpoint: OSTrack_ep0300.pth.tar

## Visualization Colors

- Red box: ground truth
- Cyan box: clean OSTrack prediction
- Green box: degraded OSTrack prediction

## Quantitative Result Summary

Clean OSTrack:

```text
Mean IoU: 0.5755
Success AUC: 0.5760
Precision @20px: 0.7461
Mean center error: 16.46 px
Degraded OSTrack:
[200~Mean IoU: 0.1502
Success AUC: 0.1572
Precision @20px: 0.1980
Mean center error: 82.96 px~
Robustness drop:
Mean IoU drop: 0.4253
Success AUC drop: 0.4188
Precision @20px drop: 0.5480
Mean center error increase: 66.50 px
