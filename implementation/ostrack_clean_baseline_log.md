# OSTrack Clean Baseline Log

## Purpose

This log records the first clean baseline tests for OSTrack on the local Linux GTX 1080 workstation.

The goal is to confirm that the OSTrack environment, checkpoint, OTB dataset path, and evaluation pipeline work correctly before testing degraded tracking.

## Environment

- Base tracker: OSTrack
- Config: vitb_256_mae_ce_32x4_ep300
- Checkpoint: OSTrack_ep0300.pth.tar
- Machine: local Linux GTX 1080 workstation
- GPU: NVIDIA GeForce GTX 1080, 8 GB VRAM
- Purpose: clean baseline sanity check before degraded baseline testing

## OSTrack Profile Smoke Test

Command:

python tracking/profile_model.py --script ostrack --config vitb_256_mae_ce_32x4_ep300

Result:

overall macs is 21.517G
overall params is 92.121M
average latency is 18.54 ms
FPS is 53.93 fps

## OTB Football Result

Football was tested first, but it is not suitable as the first clean sanity baseline because the sequence contains many visually similar players and strong distractors.

Frames evaluated: 362
Mean IoU: 0.1313
Success AUC: 0.1390
Precision @20px: 0.1657
Mean center error: 219.10 px

Observation: visualization showed that OSTrack drifted to similar players. Football should be kept later as a difficult distractor or failure-case sequence.

## OTB Car1 Result

Car1 was selected as the first clean sanity baseline because it has matching frame and ground-truth counts.

Frames: 1020
Ground-truth lines: 1020
FPS: 49.45
Mean IoU: 0.5755
Success AUC: 0.5760
Precision @20px: 0.7461
Mean center error: 16.46 px

## Interpretation

Car1 is a suitable sequence for the first clean/degraded baseline comparison. The clean result is reasonable enough to use as a local proof-of-concept baseline before testing synthetic degradation.

Football is useful later as a challenging distractor sequence, but it should not be used as the first sanity baseline.

## Important Notes

- This is a local proof-of-concept result, not a final paper result.
- Generated tracking outputs are stored under outputs/ and should not be committed.
- Full training and final experiments will be performed later on the university HPC.

## Next Step

Use Car1 for the first degraded baseline comparison.
