#!/usr/bin/env bash
set -euo pipefail

PROJECT_ROOT="$(pwd)"
OSTRACK_ROOT="${PROJECT_ROOT}/external/OSTrack"
PATCH_FILE="${PROJECT_ROOT}/implementation/patches/ostrack_rgssb_integration.patch"

echo "Project root: ${PROJECT_ROOT}"

if [[ ! -f "${PROJECT_ROOT}/AGENTS.md" ]]; then
  echo "ERROR: run this script from the project root." >&2
  exit 1
fi

if [[ ! -d "${OSTRACK_ROOT}" ]]; then
  echo "ERROR: external/OSTrack does not exist: ${OSTRACK_ROOT}" >&2
  exit 1
fi

if [[ ! -f "${PATCH_FILE}" ]]; then
  echo "ERROR: patch file not found: ${PATCH_FILE}" >&2
  exit 1
fi

cd "${OSTRACK_ROOT}"

echo "Checking patch applicability..."
if git apply --check "${PATCH_FILE}"; then
  echo "Applying patch..."
  git apply "${PATCH_FILE}"
  echo "Patch applied successfully."
else
  echo "ERROR: patch check failed. Inspect external/OSTrack state and patch compatibility." >&2
  exit 1
fi
