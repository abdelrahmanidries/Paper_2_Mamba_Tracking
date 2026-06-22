# RG-SSB Target-versus-Distractor Margin Setup Notes

## Purpose

This is the single gated final ablation defined in `implementation/final_ablation_gate.md`. It addresses corrected NFS drift cases where a shared disturbance is followed by baseline recovery and persistent RG-SSB-specific target loss.

The ablation adds a loss term only. It does not add a new architecture module.

## Fixed Base Method

The ablation starts from Paper Freeze V1:

- OSTrack + RG-SSB + box head.
- Frozen backbone.
- Trainable parameters limited to `rgssb.*` and `box_head.*`.
- Global clean/degraded feature consistency enabled.
- Feature-consistency weight: `0.02`.
- Response consistency disabled.
- Target-region feature consistency disabled.

## Inspected Implementation Details

Files inspected:

- `external/OSTrack/lib/train/actors/ostrack.py`
- `external/OSTrack/lib/models/ostrack/ostrack.py`
- `external/OSTrack/lib/models/layers/head.py`
- `external/OSTrack/lib/train/data/processing.py`
- `external/OSTrack/lib/config/ostrack/config.py`
- `implementation/final_ablation_gate.md`
- `experiments/nfs_corrected_drift_onset_analysis.csv`

Confirmed response details:

- Degraded-branch response-map key: `score_map`.
- For the selected CENTER head, `score_map` is `score_map_ctr`.
- Shape: `[B, 1, H, W]`, where `H = W = DATA.SEARCH.SIZE / MODEL.BACKBONE.STRIDE`.
- In the local debug config, `DATA.SEARCH.SIZE = 256` and stride is `16`, so response shape is `[B, 1, 16, 16]`.
- Values are sigmoid-clamped probabilities from `CenterPredictor.get_score_map`, not raw logits.

Confirmed box details:

- `search_anno` is normalized `[x, y, w, h]` in search-crop coordinates.
- The target box is mapped to the response grid by testing each response-cell center against the normalized target box.
- `TARGET_SCALE` expands or contracts the target box around its center before mask construction.
- `IGNORE_RING` removes a ring around the target mask from the distractor pool.

## Loss Definition

For each sample:

```text
target_score = pool(score_map inside target mask)
distractor_score = pool(score_map outside target mask and ignore ring)
L_margin = mean(max(0, margin - target_score + distractor_score))
```

Default ablation settings:

```text
TRAIN.TARGET_DISTRACTOR_MARGIN.ENABLE = True
TRAIN.TARGET_DISTRACTOR_MARGIN.WEIGHT = 0.05
TRAIN.TARGET_DISTRACTOR_MARGIN.MARGIN = 0.2
TRAIN.TARGET_DISTRACTOR_MARGIN.LOSS = "hinge"
TRAIN.TARGET_DISTRACTOR_MARGIN.TARGET_POOLING = "max"
TRAIN.TARGET_DISTRACTOR_MARGIN.DISTRACTOR_POOLING = "max"
TRAIN.TARGET_DISTRACTOR_MARGIN.TARGET_SCALE = 1.0
TRAIN.TARGET_DISTRACTOR_MARGIN.IGNORE_RING = 1
```

Total local ablation loss:

```text
L_total = L_track + 0.02 * L_global_feature_consistency + 0.05 * L_target_distractor_margin
```

## Files Created or Modified

External OSTrack:

- `external/OSTrack/lib/config/ostrack/config.py`
- `external/OSTrack/lib/train/actors/ostrack.py`
- `external/OSTrack/experiments/ostrack/vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_degraded_3000_featcons_lam002_tdm_debug.yaml`

Project files:

- `configs/rgssb_experiment_cycle_featcons_lam002_tdm.json`
- `scripts/verify_rgssb_target_distractor_margin_pipeline.py`
- `implementation/rgssb_target_distractor_margin_setup_notes.md`

## Verification

Run:

```bash
python3 -m py_compile scripts/verify_rgssb_target_distractor_margin_pipeline.py
conda run -n ostrack python scripts/verify_rgssb_target_distractor_margin_pipeline.py
python3 scripts/run_rgssb_experiment_cycle.py \
  --cycle_config configs/rgssb_experiment_cycle_featcons_lam002_tdm.json \
  --dry_run
```

The verifier must show:

- config loads,
- `score_map` exists,
- target and distractor masks have the response-map shape,
- margin loss is finite,
- global feature-consistency loss remains finite,
- response consistency is disabled,
- target-region feature consistency is disabled,
- trainable parameters remain `rgssb.*` and `box_head.*`,
- backbone remains frozen,
- one mini forward/backward passes.

## Gates

Local proceed gate:

- verifier passes,
- real-batch backward pass completes,
- local average improves over current global lambda `0.02`,
- no severe clean collapse.

HPC keep gate:

- corrected expanded NFS improves meaningfully,
- broader OTB decreases by no more than `0.005`,
- expanded UAV123 decreases by no more than `0.005`,
- overall cross-benchmark average improves,
- persistent RG-SSB-specific target-loss cases decrease below `5`.

If any keep gate fails, reject this ablation and return to Paper Freeze V1.
