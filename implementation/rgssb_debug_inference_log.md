# RG-SSB Debug Inference Log

## Purpose

This log records the first OSTrack inference tests with RG-SSB enabled through the debug config.

The goal was to verify that RG-SSB can be integrated into OSTrack, enabled by config flag, loaded with the original OSTrack checkpoint using strict=False, and executed during inference without crashing.

These results are only debug results. RG-SSB is currently untrained, so these numbers should not be treated as scientific performance claims.

## Base Tracker

- Tracker: OSTrack
- Baseline config: vitb_256_mae_ce_32x4_ep300
- RG-SSB debug config: vitb_256_mae_ce_32x4_ep300_rgssb_debug
- Checkpoint: OSTrack_ep0300.pth.tar
- Sequence: OTB Car1
- Machine: local Linux GTX 1080 workstation

## RG-SSB Debug Config

RG-SSB was enabled with:

MODEL.RGSSB.ENABLE = True

Expected insertion shape:

[B, 256, 768] -> [B, 256, 768]

Checkpoint loading behavior:

- Baseline config uses strict=True.
- RG-SSB debug config uses strict=False.
- Missing rgssb.* keys are expected because the original OSTrack checkpoint does not contain RG-SSB weights.
- Unexpected keys: none.

## Clean Car1 Inference

Original OSTrack clean Car1:

Mean IoU: 0.5755
Success AUC: 0.5760
Precision @20px: 0.7461
Mean center error: 16.46 px

RG-SSB debug clean Car1:

Mean IoU: 0.6109
Success AUC: 0.6108
Precision @20px: 0.7980
Mean center error: 13.78 px
FPS: 49.68

Interpretation:

RG-SSB enabled inference works on clean Car1. The untrained RG-SSB did not break tracking and even produced a slightly higher clean score in this debug run. This should not be over-interpreted because RG-SSB has not been trained.

## Motion-Blur Car1 Inference

Original OSTrack motion_blur medium Car1:

Mean IoU: 0.1502
Success AUC: 0.1572
Precision @20px: 0.1980
Mean center error: 82.96 px

RG-SSB debug motion_blur medium Car1:

Mean IoU: 0.1501
Success AUC: 0.1570
Precision @20px: 0.2000
Mean center error: 84.03 px
FPS: 49.78

Interpretation:

RG-SSB enabled inference also works under motion blur. Since the RG-SSB module is untrained, it does not yet improve degraded tracking. This is expected. The key result is that the integrated model runs correctly and produces valid tracking outputs.

## Current Conclusion

The RG-SSB integration is technically functional:

- RG-SSB disabled baseline path works.
- RG-SSB enabled debug path works.
- Original checkpoint can be loaded with strict=False for debug mode.
- Clean inference works.
- Degraded inference works.
- Result logging and CSV replacement/appending work.
- OTB symlink restoration works.

The next important step is not more inference. The next important step is to create a small training/debug plan so RG-SSB can learn useful weights.

## Next Step

Prepare a minimal training/debug workflow:

1. Freeze most of OSTrack if needed.
2. Train only RG-SSB and possibly the head on a tiny degraded subset.
3. Use clean/degraded pairs.
4. Verify loss decreases.
5. Evaluate whether trained RG-SSB improves degraded Car1 without destroying clean Car1.

## Important Notes

- These results are local proof-of-concept results only.
- Final training and full experiments will be performed later on the university HPC.
- Do not claim that untrained RG-SSB improves degradation robustness.
- The meaningful test will come after RG-SSB training.
