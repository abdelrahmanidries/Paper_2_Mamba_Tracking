# Feature-Consistency Lambda Sweep Plan

## Why This Sweep Is Needed

The current feature-consistency experiment uses `TRAIN.FEATURE_CONSISTENCY.WEIGHT = 0.05`.
The 3000-sample results were mixed: the constraint may be too weak to improve
degraded robustness consistently, or too strong and suppressing target-specific
discriminative features. A small local sweep tests this without changing the
architecture or the degradation protocol.

## Lambda Values

- `0.02`: weaker feature-consistency pressure.
- `0.10`: stronger feature-consistency pressure.
- Existing reference: `0.05`.

## What Stays Fixed

- Backbone remains frozen.
- Trainable parameters remain `rgssb.*` and `box_head.*` only.
- `MODEL.RGSSB.ENABLE: True`.
- `TRAIN.FREEZE_MODE: "rgssb_head"`.
- LaSOT train/val only.
- `DATA.TRAIN.SAMPLE_PER_EPOCH: 3000`.
- `DATA.VAL.SAMPLE_PER_EPOCH: 300`.
- `TRAIN.EPOCH: 1` and `TEST.EPOCH: 1`.
- Search-only training degradation.
- Degradation types: `motion_blur`, `low_resolution`, `gaussian_noise`.
- Degradation severity: `medium`.
- Evaluation sequences: `Car1`, `David2`, `Coke`.
- Evaluation conditions: clean, motion blur, low resolution, Gaussian noise.

## Run Lambda 0.02 Cycle

```bash
python3 scripts/run_rgssb_experiment_cycle.py \
  --cycle_config configs/rgssb_experiment_cycle_featcons_lam002.json
```

## Run Lambda 0.10 Cycle

```bash
python3 scripts/run_rgssb_experiment_cycle.py \
  --cycle_config configs/rgssb_experiment_cycle_featcons_lam010.json
```

## Metrics To Compare

Compare the CSV rows in `experiments/baseline_results.csv` for:

- `mean_iou`
- `success_auc`
- `precision_20`
- `mean_center_error`

Compare each lambda against the existing `0.05` feature-consistency run and the
RG-SSB head-only references, sequence by sequence and degradation by degradation.
Do not average away a severe regression on a single sequence without reporting it.

## When Lambda 0.02 Is Better

Lambda `0.02` is better if it improves degraded-condition metrics over `0.05`
while preserving clean tracking performance. The most useful result would be
higher `success_auc` or `precision_20` on motion blur, low resolution, and
Gaussian noise without a meaningful drop on clean `Car1`, `David2`, or `Coke`.

## When Lambda 0.10 Is Better

Lambda `0.10` is better if stronger feature alignment improves degraded
robustness without collapsing clean discrimination. It should show consistent
degraded gains over `0.05` and `0.02`, especially on the conditions where the
current result analysis showed mixed behavior.

## When To Replace Feature Consistency

Feature consistency should be replaced by response consistency if both `0.02`
and `0.10` fail to improve degraded tracking reliably, or if improved feature
alignment trades off against target localization. A warning pattern is better
feature-consistency training behavior but flat or worse `success_auc`,
`precision_20`, or `mean_center_error` in evaluation. That would suggest the
constraint is aligning internal features without improving the tracker response
that determines the final box.
