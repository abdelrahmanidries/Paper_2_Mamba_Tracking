# HPC Transfer Checklist

## Transfer These Files

Transfer the project source tree with:

- `implementation/hpc_featcons_lam002_plan.md`
- `implementation/hpc_transfer_checklist.md`
- `implementation/hpc_run_order.md`
- `implementation/patches/ostrack_rgssb_integration.patch`
- `configs/hpc_paths_template.env`
- `configs/rgssb_experiment_cycle_hpc_featcons_lam002.json`
- `scripts/run_rgssb_experiment_cycle.py`
- `scripts/run_ostrack_otb_eval.py`
- `scripts/create_degraded_otb_sequence.py`
- `scripts/verify_hpc_featcons_lam002_setup.py`
- `scripts/hpc/`
- `src/degradations/`
- `experiments/baseline_results.csv`
- `experiments/rgssb_featcons_lambda_sweep_comparison.csv`
- `implementation/rgssb_featcons_lambda_sweep_result_analysis.md`

## Do Not Transfer

Do not transfer or commit:

- `external/OSTrack/output/`
- checkpoints such as `*.pth.tar`
- generated `outputs/`
- generated or full `datasets/`
- HPC job logs unless intentionally archiving a short result summary
- large local cache files

## Expected Git State

- Expected project branch: `implementation-poc`
- Best local setup: RG-SSB + box head with feature consistency lambda `0.02`
- Response consistency: disabled
- Architecture additions postponed: degradation token, template-guided scan,
  memory update, response fusion, and new modules

## OSTrack Base

- Repository: `https://github.com/botaoye/OSTrack`
- Required OSTrack commit hash: `33b5e12586216b7fd0e95d255bd01ba44cbec759`
- Local expected path after clone: `external/OSTrack`
- Required patch file:
  `implementation/patches/ostrack_rgssb_integration.patch`

## Required Checkpoints

Required base checkpoint before training:

```text
external/OSTrack/output/checkpoints/train/ostrack/vitb_256_mae_ce_32x4_ep300/OSTrack_ep0300.pth.tar
```

Expected HPC checkpoint after training:

```text
external/OSTrack/output/checkpoints/train/ostrack/vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_degraded_hpc_featcons_lam002/OSTrack_ep0010.pth.tar
```

## Required Datasets

- LaSOT train/validation root for OSTrack training
- OTB root for evaluation
- Writable degraded OTB output root for generated evaluation variants

Dataset paths must be edited in:

- `configs/hpc_paths_template.env`
- `configs/rgssb_experiment_cycle_hpc_featcons_lam002.json`
- OSTrack environment/local path configuration if the HPC clone requires it

## Required HPC Environment

The cluster must provide:

- CUDA-compatible GPU node
- `nvidia-smi`
- Conda or Mamba
- Python environment named `ostrack` or an edited equivalent
- PyTorch/CUDA stack compatible with OSTrack
- Python packages required by this project and OSTrack

## Required Edits Before SLURM

Edit:

- `configs/hpc_paths_template.env`
- `scripts/hpc/slurm_rgssb_featcons_lam002_train.sh`
- `scripts/hpc/slurm_rgssb_featcons_lam002_eval.sh`
- `configs/rgssb_experiment_cycle_hpc_featcons_lam002.json`

Replace placeholders for account, partition, GPU type/count, CPUs, memory, wall
time, project path, conda init path, LaSOT root, OTB root, output root, scratch
directory, and results directory.

## Verification Before Training

From the project root on HPC:

```bash
bash scripts/hpc/verify_hpc_environment.sh
conda run -n ostrack python scripts/verify_hpc_featcons_lam002_setup.py
```

Both checks must pass before submitting the training job.
