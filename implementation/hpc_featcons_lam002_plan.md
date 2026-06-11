# HPC Plan: RG-SSB + Head Feature Consistency Lambda 0.02

## Why Lambda 0.02 Was Selected

The local lambda sweep found feature consistency lambda `0.02` as the best
overall setup across the 12 Car1/David2/Coke sequence-condition pairs. In
`experiments/rgssb_featcons_lambda_sweep_comparison.csv`, lambda `0.02` reached
overall average AUC `0.613026`, above the original OSTrack baseline `0.589546`,
fully degraded 3000 `0.600403`, balanced 3000 `0.592421`, lambda `0.05`
`0.594527`, and lambda `0.10` `0.601905`.

## Why Response Consistency Is Disabled

The response-consistency comparison showed feature+response consistency at
overall average AUC `0.593666`, below feature-only lambda `0.02` at `0.613026`.
Response consistency helped motion blur on average but hurt clean, low
resolution, and Gaussian noise. The HPC setup therefore keeps response
consistency disabled.

## Why The Architecture Remains Unchanged

The current evidence supports the RG-SSB + head training objective, not a new
module. The HPC setup keeps the architecture unchanged and does not add a
degradation token, template-guided scan, memory update, response fusion, or
response-consistency module.

## Local Evidence

- Feature consistency lambda `0.02` is the best local average among tested
  feature-consistency weights.
- Response consistency with weight `0.05` is worse overall than feature-only
  lambda `0.02`.
- Backbone frozen with trainable `rgssb.*` and `box_head.*` has been verified.
- The result is still local proof-of-concept evidence, not final paper evidence.

## What Must Be Edited For HPC

Edit:

- `scripts/hpc/slurm_rgssb_featcons_lam002_train.sh`
- `scripts/hpc/slurm_rgssb_featcons_lam002_eval.sh`
- `configs/rgssb_experiment_cycle_hpc_featcons_lam002.json`

Fields to edit:

- SLURM account
- partition
- GPU type and count
- CPU count
- memory
- wall time
- project path
- conda initialization path
- LaSOT root
- OTB root
- degraded output root if different
- results CSV path if different

The HPC config starts with conservative values:

- `TRAIN.BATCH_SIZE: 8`
- `TRAIN.NUM_WORKER: 8`
- `TRAIN.EPOCH: 10`
- `DATA.TRAIN.SAMPLE_PER_EPOCH: 10000`
- `DATA.VAL.SAMPLE_PER_EPOCH: 1000`
- `TEST.EPOCH: 10`

These must be adjusted based on GPU memory, queue limits, and training time.

## Training And Evaluation Order

1. Run local verification:

```bash
conda run -n ostrack python scripts/verify_hpc_featcons_lam002_setup.py
```

2. Edit HPC paths and SLURM placeholders.
3. Submit `scripts/hpc/slurm_rgssb_featcons_lam002_train.sh`.
4. Confirm checkpoint:

```text
external/OSTrack/output/checkpoints/train/ostrack/vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_degraded_hpc_featcons_lam002/OSTrack_ep0010.pth.tar
```

5. Submit `scripts/hpc/slurm_rgssb_featcons_lam002_eval.sh`.
6. Inspect `experiments/baseline_results.csv`.

## Results That Justify Paper-Scale Continuation

- Higher average AUC than local lambda `0.02` or a clear gain over fully degraded
  3000 on the same evaluation conditions.
- No severe clean tracking collapse.
- Gains on degraded conditions are not limited to one sequence.
- Precision@20 and center error move consistently with AUC.

## Results That Require Revising Training

- Clean performance drops while degraded gains are small.
- Improvements occur only on one sequence or one degradation.
- Gaussian noise or low resolution regresses strongly.
- Precision@20 or center error contradicts AUC gains.

## What Not To Commit

Do not commit:

- checkpoints
- outputs
- datasets
- `external/OSTrack/output`
- `*.pth.tar`

Commit only reviewed source/config/documentation changes and selected result
summaries intended for version control.
