#!/usr/bin/env bash
#SBATCH --job-name=rgssb-fc002-eval
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
HPC_CLEAN_OTB_ROOT="<HPC_OTB_ROOT>"
HPC_DEGRADED_OUTPUT_ROOT="<PROJECT_PATH>/datasets/tiny_sot/degraded"
HPC_RESULTS_CSV="<PROJECT_PATH>/experiments/baseline_results.csv"

source "${CONDA_INIT}"
conda activate "${CONDA_ENV}"

cd "${PROJECT_PATH}"

python3 scripts/run_rgssb_experiment_cycle.py \
  --cycle_config configs/rgssb_experiment_cycle_hpc_featcons_lam002.json \
  --eval_only
