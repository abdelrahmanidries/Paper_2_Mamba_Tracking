#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(pwd)"
ENV_FILE="${PROJECT_ROOT}/configs/hpc_paths_template.env"

echo "pwd: ${PROJECT_ROOT}"

if [[ ! -f "${PROJECT_ROOT}/AGENTS.md" ]]; then
  echo "ERROR: run this script from the project root." >&2
  exit 1
fi

if [[ -f "${ENV_FILE}" ]]; then
  # shellcheck disable=SC1090
  source "${ENV_FILE}"
else
  echo "ERROR: missing environment template: ${ENV_FILE}" >&2
  exit 1
fi

PROJECT_ROOT="${PROJECT_ROOT:-$(pwd)}"
OSTRACK_ROOT="${OSTRACK_ROOT:-${PROJECT_ROOT}/external/OSTrack}"
CONDA_ENV="${CONDA_ENV:-ostrack}"

if git rev-parse --abbrev-ref HEAD >/dev/null 2>&1; then
  echo "git branch: $(git rev-parse --abbrev-ref HEAD)"
else
  echo "WARNING: project is not a Git checkout."
fi

if command -v nvidia-smi >/dev/null 2>&1; then
  nvidia-smi
else
  echo "ERROR: nvidia-smi not found." >&2
  exit 1
fi

if ! command -v conda >/dev/null 2>&1; then
  echo "ERROR: conda not found." >&2
  exit 1
fi

if ! command -v python >/dev/null 2>&1; then
  echo "ERROR: python not found." >&2
  exit 1
fi

if [[ ! -d "${OSTRACK_ROOT}" ]]; then
  echo "ERROR: OSTrack root not found: ${OSTRACK_ROOT}" >&2
  exit 1
fi

BASE_CHECKPOINT="${OSTRACK_ROOT}/output/checkpoints/train/ostrack/vitb_256_mae_ce_32x4_ep300/OSTrack_ep0300.pth.tar"
if [[ ! -f "${BASE_CHECKPOINT}" ]]; then
  echo "ERROR: required OSTrack checkpoint not found: ${BASE_CHECKPOINT}" >&2
  exit 1
fi

if [[ -z "${LASOT_ROOT:-}" || ! -d "${LASOT_ROOT}" ]]; then
  echo "ERROR: LASOT_ROOT is unset or missing: ${LASOT_ROOT:-<unset>}" >&2
  exit 1
fi

if [[ -z "${OTB_ROOT:-}" || ! -d "${OTB_ROOT}" ]]; then
  echo "ERROR: OTB_ROOT is unset or missing: ${OTB_ROOT:-<unset>}" >&2
  exit 1
fi

for path in \
  "${PROJECT_ROOT}/implementation/patches/ostrack_rgssb_integration.patch" \
  "${PROJECT_ROOT}/scripts/verify_hpc_featcons_lam002_setup.py" \
  "${PROJECT_ROOT}/configs/rgssb_experiment_cycle_hpc_featcons_lam002.json" \
  "${PROJECT_ROOT}/scripts/hpc/slurm_rgssb_featcons_lam002_train.sh" \
  "${PROJECT_ROOT}/scripts/hpc/slurm_rgssb_featcons_lam002_eval.sh"; do
  if [[ ! -f "${path}" ]]; then
    echo "ERROR: required file missing: ${path}" >&2
    exit 1
  fi
done

echo "Running Python verifier with conda env: ${CONDA_ENV}"
conda run -n "${CONDA_ENV}" python scripts/verify_hpc_featcons_lam002_setup.py

echo "HPC environment verification passed."
