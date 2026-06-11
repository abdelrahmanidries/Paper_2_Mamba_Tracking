# RG-SSB + Head Clean-Degraded Feature Consistency Training Plan

Date: 2026-06-10

## Purpose

The fully degraded 3000-sample RG-SSB + head setup is stronger than the balanced 3000-sample setup overall, but results remain mixed across Car1, David2, and Coke. The next minimal training change is to add a clean-degraded feature consistency signal while keeping the architecture unchanged:

- backbone frozen
- trainable parameters limited to `rgssb.*` and `box_head.*`
- no degradation token
- no template-guided scan
- no memory module
- no response fusion
- no new architecture modules

## 1. OSTrack Training Flow Inspection

Training entry point:

- `external/OSTrack/lib/train/train_script.py`
  - `run(settings)` loads the YAML config through `lib.config.ostrack.config.update_config_from_file`.
  - `build_dataloaders(cfg, settings)` creates train/val loaders.
  - `build_ostrack(cfg)` constructs the model.
  - `OSTrackActor` wraps the model and loss functions.
  - `get_optimizer_scheduler(net, cfg)` applies freeze mode and builds the optimizer.
  - `LTRTrainer.train(...)` starts training.

Dataset and tensor creation:

- `external/OSTrack/lib/train/base_functions.py`
  - `build_dataloaders` creates `STARKProcessing` for training.
  - Training processing receives `degradation_cfg=cfg.DATA.DEGRADATION`.
  - The train sampler is `lib.train.data.sampler.TrackingSampler`.

- `external/OSTrack/lib/train/data/sampler.py`
  - `TrackingSampler.getitem()` samples one template frame and one search frame.
  - It loads raw images and boxes through `dataset.get_frames(...)`.
  - It returns a `TensorDict` containing `template_images`, `search_images`, `template_anno`, and `search_anno`.
  - It calls `self.processing(data)` before the loader stacks batches.

- `external/OSTrack/lib/train/data/processing.py`
  - `STARKProcessing.__call__` applies joint transforms first.
  - It crops template/search regions with `jittered_center_crop`.
  - Current synthetic degradation is applied to cropped images before tensor conversion and normalization:
    - `crops = self.degradation.apply(crops, role=s)`
  - It then applies `ToTensor`, jitter, flip normalization, and returns tensors.
  - Final tensor layout after loader stacking is used by the actor as:
    - `template_images`: `(N_t, batch, 3, H, W)`
    - `search_images`: `(N_s, batch, 3, H, W)`

Model call and output:

- `external/OSTrack/lib/train/actors/ostrack.py`
  - `OSTrackActor.__call__` runs `forward_pass(data)`, then `compute_losses(out_dict, data)`.
  - `forward_pass` reshapes:
    - template: `(batch, 3, 128, 128)`
    - search: `(batch, 3, 256, 256)` for the debug configs
  - It calls:
    - `self.net(template=template_list, search=search_img, ce_template_mask=..., ce_keep_rate=...)`
  - `compute_losses` uses:
    - `pred_boxes`
    - `score_map`
    - `search_anno`
  - Current losses are GIoU, L1, and focal/location loss.

- `external/OSTrack/lib/models/ostrack/ostrack.py`
  - `OSTrack.forward` calls `self.backbone(z=template, x=search, ...)`.
  - `forward_head` slices search tokens:
    - `enc_opt = cat_feature[:, -self.feat_len_s:]`
  - If RG-SSB is enabled:
    - `enc_opt = self.rgssb(enc_opt, search_len=self.feat_len_s, spatial_size=(self.feat_sz_s, self.feat_sz_s))`
  - `enc_opt` is reshaped to `(B, C, 16, 16)` and passed to `box_head`.
  - Output dict currently contains `pred_boxes`, `score_map`, `size_map`, `offset_map`, plus `backbone_feat`.

Safest feature exposure point:

- Post-RGSSB search tokens inside `OSTrack.forward_head`, immediately after:
  - `enc_opt = self.rgssb(...)`
- This tensor is expected to be `(B, 256, 768)` for the current 256 search-size config.

## 2. Candidate Feature Consistency Designs

### A. Clean-Degraded Search Feature Consistency After RG-SSB

Design:

- Run the same template with a clean search and a degraded search.
- Compare post-RGSSB search tokens from both branches.
- Use the degraded branch for the normal tracking loss.
- Use the clean branch as the consistency target, likely detached.

Implementation difficulty:

- Moderate. Requires returning post-RGSSB search tokens and adding a two-branch actor path.

Memory cost on GTX 1080:

- Moderate to high because the model needs clean and degraded search forwards. With the backbone frozen, this is more manageable.

Training speed risk:

- Approximately 2x forward cost for the model path unless the template/backbone reuse is optimized later.

Likelihood of helping degradation robustness:

- High relative to other minimal options because the loss directly constrains degraded search features to remain close to clean search features after restoration-guided processing.

Risk of hurting clean performance:

- Lower if the clean feature is detached, because the clean branch acts as a stable target and gradients update only the degraded branch path through RG-SSB/head.

### B. Clean-Degraded Search Feature Consistency Before RG-SSB

Design:

- Compare search tokens before RG-SSB.

Implementation difficulty:

- Moderate. Requires exposing pre-RGSSB tokens.

Memory cost:

- Similar to option A.

Likelihood of helping degradation robustness:

- Lower. The pre-RGSSB tensor is produced by the frozen backbone, so the trainable RG-SSB is not directly encouraged to restore or align its own output.

Risk of hurting clean performance:

- Moderate. It may penalize unavoidable degradation effects in frozen backbone features instead of teaching RG-SSB to correct them.

### C. Response-Map Consistency Between Clean And Degraded Branches

Design:

- Compare `score_map` outputs for clean and degraded searches.

Implementation difficulty:

- Moderate. The output is already available, but the branch design is still needed.

Memory cost:

- Similar to option A if both branches are forwarded.

Likelihood of helping degradation robustness:

- Medium to high, especially for localization stability.

Risk of hurting clean performance:

- Medium. It may over-constrain response shapes when degradation legitimately changes confidence or distractor behavior.

### D. Target-Region Feature Consistency Only

Design:

- Compare only tokens near the target region using the search ground-truth box.

Implementation difficulty:

- Higher. Requires mapping normalized/cropped boxes to 16x16 token indices and building target masks.

Memory cost:

- Similar forward cost, lower loss tensor cost.

Likelihood of helping degradation robustness:

- High in principle because it focuses the loss on target-discriminative features.

Risk of hurting clean performance:

- Lower than full-token consistency, but implementation complexity is higher and mask bugs are likely.

### E. Full-Image/Token Feature Consistency

Design:

- Compare all 256 search tokens after RG-SSB.

Implementation difficulty:

- Low once feature tensors are exposed.

Memory cost:

- Small loss tensor cost, but still requires two branch forwards.

Likelihood of helping degradation robustness:

- Medium. It is simple and stable, but background tokens may dominate unless normalized or masked later.

Risk of hurting clean performance:

- Medium. It can over-align background clutter and may reduce flexibility.

## 3. Recommended Minimal First Implementation

Recommended design: **A/E combined minimal variant: clean-degraded search feature consistency after RG-SSB on all search tokens.**

Use:

- same clean template
- clean search branch
- degraded search branch
- shared ground-truth box
- post-RGSSB search tokens with shape `(B, 256, 768)`
- clean feature detached as the target
- L1 or MSE feature loss with a small weight

Why this is the safest first implementation:

- It uses the current RG-SSB insertion point directly.
- It does not add architecture.
- It keeps the output shape unchanged.
- It avoids target-token masking complexity in the first pass.
- It gives RG-SSB a direct restoration-style objective.
- It can be disabled by config.
- It keeps the baseline path unchanged when disabled.

## 4. Training Batch Design

The training sample should contain:

- `template_images`: clean template crop
- `search_images`: degraded search crop for the tracking branch
- `search_images_clean`: clean search crop for the consistency target
- `search_anno`: same normalized search box for both clean and degraded search crops

The clean and degraded search crops must share:

- same source frame
- same jittered search crop
- same crop size
- same bounding box coordinates
- same tensor normalization path

The degraded search should preserve image size. Current training degradation already preserves size and does not modify boxes.

Minimal data-processing plan:

1. In `STARKProcessing`, after search crops are created and before degradation, keep a clean copy of the search crop list.
2. Apply degradation to the normal `search` crops when `DATA.DEGRADATION.ENABLE=True`.
3. Run the same search transform on both:
   - clean search crops
   - degraded search crops
4. Add `search_images_clean` to the returned `TensorDict`.

Important implementation detail:

- The clean and degraded branches should use identical geometric crop boxes. Do not re-jitter, re-crop, or re-sample the clean search branch.

## 5. Loss Definition

Recommended first loss:

```text
L_total = L_track_degraded + lambda_feat * L_feat_consistency
```

Where:

```text
L_feat_consistency = L1(normalize(F_degraded), normalize(detach(F_clean)))
```

Definitions:

- `F_degraded`: post-RGSSB search tokens from degraded search, shape `(B, 256, 768)`
- `F_clean`: post-RGSSB search tokens from clean search, shape `(B, 256, 768)`
- `detach(F_clean)`: recommended for first implementation
- `normalize`: optional `F.normalize(..., dim=-1)` before L1/MSE

Recommended loss type:

- Start with L1 after feature normalization.
- MSE is also acceptable but may overweight large feature deviations.

Recommended lambda:

- Start with `lambda_feat = 0.05`.
- If feature loss is numerically tiny after normalization, test `0.1`.

Do not add `L_track_clean` in the first implementation. It doubles tracking-head loss computation and makes the first debug result harder to attribute. It can be added later if clean performance still regresses.

## 6. Exact Code Locations For Later Implementation

Config defaults:

- `external/OSTrack/lib/config/ostrack/config.py`
  - Add:
    - `TRAIN.FEATURE_CONSISTENCY.ENABLE = False`
    - `TRAIN.FEATURE_CONSISTENCY.WEIGHT = 0.05`
    - `TRAIN.FEATURE_CONSISTENCY.LOSS = "l1"`
    - `TRAIN.FEATURE_CONSISTENCY.NORMALIZE = True`
    - `TRAIN.FEATURE_CONSISTENCY.DETACH_CLEAN = True`
  - Default disabled so baseline behavior is unchanged.

Training config:

- `external/OSTrack/experiments/ostrack/vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_degraded_3000_featcons_debug.yaml`
  - Enable RG-SSB.
  - Use `TRAIN.FREEZE_MODE: "rgssb_head"`.
  - Use LaSOT only.
  - Use `DATA.TRAIN.SAMPLE_PER_EPOCH: 3000`.
  - Use `DATA.VAL.SAMPLE_PER_EPOCH: 300`.
  - Use `DATA.DEGRADATION.PROBABILITY: 1.0`.
  - Enable feature consistency with weight `0.05`.
  - Keep `TEST.EPOCH: 1`.

Training data processing:

- `external/OSTrack/lib/train/data/processing.py`
  - Preserve a clean copy of search crops before degradation.
  - Transform clean search crops into `search_images_clean`.
  - Keep `search_anno` unchanged.
  - Only add clean-search output when feature consistency is enabled.

Potential degradation helper:

- `external/OSTrack/lib/train/data/degradation.py`
  - Likely no change needed.
  - Current adapter preserves size and supports probability.

Model feature return:

- `external/OSTrack/lib/models/ostrack/ostrack.py`
  - Add a config-controlled or argument-controlled return of post-RGSSB search tokens.
  - Safest output key:
    - `out["search_feat_rgssb"] = enc_opt`
  - Add this only when requested, e.g. `return_search_features=True`, to avoid unnecessary memory in normal training/evaluation.

Actor and loss:

- `external/OSTrack/lib/train/actors/ostrack.py`
  - In `forward_pass`, if feature consistency is enabled:
    - run degraded branch normally using `data["search_images"]`
    - run clean branch using `data["search_images_clean"]`
    - request `search_feat_rgssb` from both branches
  - In `compute_losses`, add:
    - `Loss/feature_consistency`
    - weighted feature consistency in `Loss/total`
  - Keep current GIoU/L1/location losses unchanged.

Verification script:

- `scripts/verify_rgssb_feature_consistency_pipeline.py`
  - Load planned config.
  - Build one batch or synthetic tensors.
  - Confirm clean/degraded search pair exists.
  - Confirm feature tensors have shape `(B, 256, 768)`.
  - Confirm feature consistency loss is finite.
  - Confirm trainable params remain `rgssb.*` and `box_head.*`.
  - Run one mini forward/backward only, not training.

Patch file:

- `implementation/patches/ostrack_rgssb_integration.patch`
  - Update after implementation to include the new config, processing changes, model feature return, actor loss, and verifier-relevant external changes.

## 7. Planned Config Name

Recommended config:

`vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_degraded_3000_featcons_debug.yaml`

Likely settings:

```yaml
MODEL:
  RGSSB:
    ENABLE: True
TRAIN:
  FREEZE_MODE: "rgssb_head"
  BATCH_SIZE: 1
  NUM_WORKER: 2
  EPOCH: 1
  FEATURE_CONSISTENCY:
    ENABLE: True
    WEIGHT: 0.05
    LOSS: "l1"
    NORMALIZE: True
    DETACH_CLEAN: True
DATA:
  TRAIN:
    DATASETS_NAME: ["LASOT"]
    DATASETS_RATIO: [1]
    SAMPLE_PER_EPOCH: 3000
  VAL:
    DATASETS_NAME: ["LASOT"]
    DATASETS_RATIO: [1]
    SAMPLE_PER_EPOCH: 300
  DEGRADATION:
    ENABLE: True
    PROBABILITY: 1.0
    APPLY_TO: "search_only"
    TYPES: ["motion_blur", "low_resolution", "gaussian_noise"]
    SEVERITY: "medium"
    SEED: 42
TEST:
  EPOCH: 1
```

Keep template/search sizes unchanged:

- template size: 128
- search size: 256

## 8. Verification Plan Before Training

Run no full training initially. Verify:

1. Config loads.
2. Model builds with RG-SSB enabled.
3. Freeze mode keeps only `rgssb.*` and `box_head.*` trainable.
4. Data processing can generate:
   - clean template
   - degraded search
   - clean search copy
5. Clean and degraded search tensors share the same annotation.
6. Model returns post-RGSSB feature tensors for both branches.
7. Feature consistency loss returns a finite scalar.
8. One mini-batch forward/backward works.
9. No full training is run during verification.

## 9. Evaluation Plan After Training

Evaluate the trained feature-consistency model on:

- Car1 clean
- Car1 motion_blur medium
- Car1 low_resolution medium
- Car1 gaussian_noise medium
- David2 clean
- David2 motion_blur medium
- David2 low_resolution medium
- David2 gaussian_noise medium
- Coke clean
- Coke motion_blur medium
- Coke low_resolution medium
- Coke gaussian_noise medium

Compare against:

- original OSTrack baseline
- 1000-sample RG-SSB + head
- fully degraded 3000 RG-SSB + head
- balanced 3000 RG-SSB + head

## 10. Decision Rules

Move to HPC if:

- average AUC improves over fully degraded 3000;
- clean performance does not collapse;
- at least two degraded conditions improve on average;
- no major sequence collapse appears on Car1, David2, or Coke.

Revise again if:

- feature consistency hurts all degraded cases;
- clean improves but degraded performance drops;
- motion blur collapses;
- feature loss dominates tracking loss;
- center error worsens badly despite small AUC gains.

## 11. Recommended Next Implementation Step

Implement the minimal post-RGSSB clean-degraded feature consistency path:

1. Add disabled-by-default config flags.
2. Add clean search crop/tensor preservation in training processing.
3. Add optional post-RGSSB search feature return from `OSTrack.forward_head`.
4. Add actor two-branch forward and feature loss.
5. Add a verifier script with one mini forward/backward.

## Verification

This document was created by inspecting the current OSTrack training code and existing experiment result summaries. No training, evaluation, dataset modification, `external/OSTrack` modification, or code implementation was performed.

Uncertain fields:

- Exact memory footprint of the two-branch forward needs runtime verification on the GTX 1080.
- Exact feature-loss scale needs inspection from the verifier before training.
- Whether full-token consistency is better than target-region consistency remains untested.
