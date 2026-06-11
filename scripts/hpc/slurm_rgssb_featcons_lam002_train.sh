#!/usr/bin/env bash
#SBATCH --job-name=rgssb-fc002-train
#SBATCH --account=<ACCOUNT>
#SBATCH --partition=<PARTITION>
#SBATCH --gres=gpu:<GPU_TYPE>:<NUM_GPUS>
#SBATCH --cpus-per-task=<CPUS>
#SBATCH --mem=<MEMORY>
#SBATCH --time=<WALL_TIME>
#SBATCH --output=<PROJECT_PATH>/outputs/hpc_logs/%x_%j.out
#SBATCH --error=<PROJECT_PATH>/outputs/hpc_logs/%x_%j.err

set -euo pipefail

PROJECT_PATH="<PROJECT_PATH>"
CONDA_INIT="<CONDA_INITIALIZATION_PATH>"
CONDA_ENV="ostrack"

# Edit these paths on the HPC system before submitting.
LASOT_ROOT="<HPC_LASOT_ROOT>"
OTB_ROOT="<HPC_OTB_ROOT>"
OSTRACK_OUTPUT_ROOT="<PROJECT_PATH>/external/OSTrack/output"

source "${CONDA_INIT}"
conda activate "${CONDA_ENV}"

cd "${PROJECT_PATH}/external/OSTrack"

# Optional: adapt your local.py/environment.py outside this script if the HPC
# dataset layout differs from the local workstation.
export LASOT_ROOT
export OTB_ROOT
export OSTRACK_OUTPUT_ROOT

python lib/train/run_training.py \
  --script ostrack \
  --config vitb_256_mae_ce_32x4_ep300_rgssb_head_train_lasot_degraded_hpc_featcons_lam002 \
  --save_dir output \
  --use_lmdb 0 \
  --use_wandb 0
