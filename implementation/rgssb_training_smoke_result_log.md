# RG-SSB Training Smoke Result Log

## Purpose

This log records the first minimal RG-SSB training smoke test.

The goal was not to achieve final performance. The goal was to verify that RG-SSB can be trained inside OSTrack, saved as a checkpoint, loaded for evaluation, and compared against the original OSTrack baseline.

## Training Setup

- Base tracker: OSTrack
- Base config: vitb_256_mae_ce_32x4_ep300
- RG-SSB training config: vitb_256_mae_ce_32x4_ep300_rgssb_train_lasot_debug
- Training dataset: LaSOT only
- Training mode: RG-SSB only
- Frozen parameters: 92,518,533
- Trainable parameters: 2,079,936
- Batch size: 1
- Epochs: 1
- Samples per epoch: 100
- Validation samples: 20
- GPU: NVIDIA GeForce GTX 1080, 8 GB VRAM

## Training Result

The training smoke test completed successfully.

A checkpoint was saved at:

external/OSTrack/output/checkpoints/train/ostrack/vitb_256_mae_ce_32x4_ep300_rgssb_train_lasot_debug/OSTrack_ep0001.pth.tar

Checkpoint size:

377 MB

## Checkpoint Loading

The trained RG-SSB checkpoint loaded successfully for evaluation.

Evaluation checkpoint:

OSTrack_ep0001.pth.tar

Checkpoint loading result:

Missing keys: []
Unexpected keys: []

This confirms that the trained checkpoint contains RG-SSB weights.

## Clean Car1 Evaluation

Original OSTrack clean Car1:

Mean IoU: 0.5755
Success AUC: 0.5760
Precision @20px: 0.7461
Mean center error: 16.46 px

Trained RG-SSB clean Car1:

Mean IoU: 0.5433
Success AUC: 0.5442
Precision @20px: 0.7245
Mean center error: 17.84 px

Observation:

Clean tracking performance dropped slightly after the tiny RG-SSB-only training run. This is acceptable for a smoke test, but it shows that the current training setup is not yet optimized.

## Motion-Blur Car1 Evaluation

Original OSTrack motion_blur medium Car1:

Mean IoU: 0.1502
Success AUC: 0.1572
Precision @20px: 0.1980
Mean center error: 82.96 px

Trained RG-SSB motion_blur medium Car1:

Mean IoU: 0.1421
Success AUC: 0.1473
Precision @20px: 0.1853
Mean center error: 79.34 px

Observation:

The trained RG-SSB smoke model did not improve motion-blur robustness. The AUC slightly decreased compared with the original OSTrack baseline. This is not a final negative result because the training was extremely small and used only 100 LaSOT samples.

## Interpretation

The main technical goal was achieved:

- RG-SSB integrates into OSTrack.
- RG-SSB can be trained while the rest of OSTrack is frozen.
- The training loop works.
- A checkpoint is saved.
- The checkpoint loads correctly.
- Clean and degraded evaluations run successfully.
- Results are written to the baseline CSV.

The main scientific goal is not achieved yet:

- The current tiny RG-SSB training does not improve degraded tracking.
- More targeted degradation-aware training is needed.

## Likely Reason for No Improvement

The current training setup used standard LaSOT samples and standard OSTrack losses. It did not explicitly train on degraded template/search pairs. Therefore, RG-SSB had no direct supervision to learn restoration-guided degraded feature recovery.

## Next Required Improvement

The next training iteration should introduce degradation-aware training.

Recommended next step:

1. Create a training/debug configuration that injects synthetic degradation into the search image or template-search pair during training.
2. Start with motion_blur medium and low_resolution medium.
3. Keep RG-SSB-only training first.
4. Compare clean and degraded Car1 after training.
5. Only expand to more modules if the degradation-aware training improves results.

## Current Conclusion

The implementation pipeline is technically ready for degradation-aware RG-SSB training.

This result should be reported internally as:

"RG-SSB training smoke test succeeded technically, but standard clean-data training is insufficient for improving degradation robustness."

It should not be used as a final paper result.
