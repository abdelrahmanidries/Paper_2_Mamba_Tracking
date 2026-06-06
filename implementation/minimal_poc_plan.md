# Minimal Proof-of-Concept Plan

## 1. Minimum model design

The minimum model should be a base RGB single-object template-search tracker with one inserted **Restoration-Guided State Space Block**.

Recommended minimal model:

```text
template/search images
        |
base tracker feature extractor
        |
minimal RG-SSB at one selected stage
        |
unchanged template-search interaction / tracking head
        |
classification map + box prediction
```

The first proof-of-concept should not attempt to implement the full paper architecture. The goal is to test whether restoration-guided Mamba feature recovery gives a measurable benefit under degradation.

## 2. Exact modules to implement

Implement these first:

1. Base tracker integration.
2. Synthetic degradation pipeline.
3. Minimal RG-SSB:
   - Mamba/state-space branch.
   - Local enhancement branch.
   - Channel selection or channel attention branch.
   - Residual feature update.
4. Tracking losses already used by the base tracker.
5. Clean-degraded feature consistency loss.
6. Response consistency loss if response maps are directly accessible.
7. Clean/degraded evaluation scripts.
8. Response-map visualization if feasible.

## 3. Exact modules to postpone

Postpone these until the minimal model is validated:

- Degradation token or prompt.
- Template-Guided Attentive Scan.
- Degradation-aware memory update.
- Complex restoration-guided response fusion.
- Contrastive target-distractor loss.
- Real degraded fine-tuning.
- Full multi-dataset benchmark.
- Final paper figures.

## 4. First training setting

Use a small but controlled training setup:

1. Start from a pretrained base tracker if available.
2. Use clean template/search pairs.
3. Add synthetic degraded pairs.
4. Train with:
   - tracking loss
   - feature consistency loss
   - response consistency loss only if easy to compute
5. Include template/search degradation cases:
   - clean template + degraded search
   - degraded template + clean search
   - degraded template + degraded search

First degradation types:

- motion blur
- Gaussian noise
- low resolution
- JPEG compression
- mixed medium degradation

Low light and sensor noise can be added after the first loop is stable.

## 5. First testing setting

Use one dataset subset first, not the full benchmark suite.

Required evaluations:

1. Clean baseline.
2. Degraded baseline.
3. Base tracker with same degradation training.
4. Base tracker + vanilla Mamba block.
5. Base tracker + RG-SSB.
6. External restoration preprocessing + tracker if feasible.

Report:

- clean performance
- degraded performance
- degradation robustness drop
- runtime or FPS
- response-map examples

## 6. Expected signs that the idea is promising

The idea is promising if:

1. RG-SSB improves degraded tracking over the base tracker.
2. RG-SSB improves over base tracker with the same degradation training.
3. RG-SSB improves over a vanilla Mamba block.
4. The improvement is visible in response maps or localization stability.
5. The runtime overhead is acceptable.
6. External restoration preprocessing does not clearly dominate the proposed feature-level approach.

These are signs to continue, not final paper results.

## 7. Failure signs that mean the idea may be weak

The idea may be weak if:

1. Base tracker with degradation training matches RG-SSB.
2. Vanilla Mamba matches RG-SSB.
3. MambaIR/MambaIRv2 preprocessing plus tracker matches or exceeds RG-SSB with lower implementation risk.
4. RG-SSB improves image-like features but not tracking metrics.
5. Response maps remain diffuse under degradation.
6. Runtime cost is too high for tracking.
7. The method only helps low light but not blur, noise, low resolution, JPEG, or mixed degradation.

If these failure signs appear, revise the method before adding optional modules.
