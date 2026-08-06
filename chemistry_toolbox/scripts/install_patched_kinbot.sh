#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOLBOX_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
PROJECT_ROOT="$(cd "${TOOLBOX_ROOT}/.." && pwd)"
SOURCE_DIR="${PROJECT_ROOT}/.software_cache/kinbot/source-2.2.2"
PATCH_FILE="${TOOLBOX_ROOT}/patches/kinbot-v2.2.2-local-nwchem.patch"
KINBOT_REPOSITORY="https://github.com/zadorlab/KinBot.git"
KINBOT_COMMIT="2b530ad24a4dd6a52743a783752821d5d2560519"
TARGET_PREFIX="${1:-${RESEARCHCHEMBENCH_ENV_ROOT:-${PROJECT_ROOT}/.envs}/kinetics-legacy}"

[[ -x "${TARGET_PREFIX}/bin/python" ]] || {
  echo "Missing target Python environment: ${TARGET_PREFIX}" >&2
  exit 2
}
[[ -s "${PATCH_FILE}" ]] || { echo "Missing KinBot patch: ${PATCH_FILE}" >&2; exit 2; }

if [[ ! -d "${SOURCE_DIR}/.git" ]]; then
  mkdir -p "$(dirname "${SOURCE_DIR}")"
  git clone --no-checkout "${KINBOT_REPOSITORY}" "${SOURCE_DIR}"
  git -C "${SOURCE_DIR}" checkout --detach "${KINBOT_COMMIT}"
elif [[ "$(git -C "${SOURCE_DIR}" rev-parse HEAD)" != "${KINBOT_COMMIT}" ]]; then
  git -C "${SOURCE_DIR}" diff --quiet && git -C "${SOURCE_DIR}" diff --cached --quiet || {
    echo "Refusing to replace a modified KinBot source tree: ${SOURCE_DIR}" >&2
    exit 2
  }
  git -C "${SOURCE_DIR}" fetch origin "${KINBOT_COMMIT}"
  git -C "${SOURCE_DIR}" checkout --detach "${KINBOT_COMMIT}"
fi

if git -C "${SOURCE_DIR}" apply --reverse --check "${PATCH_FILE}"; then
  echo "KinBot portability patch is already applied."
elif git -C "${SOURCE_DIR}" apply --check "${PATCH_FILE}"; then
  git -C "${SOURCE_DIR}" apply "${PATCH_FILE}"
else
  echo "KinBot source does not match the pinned patch base." >&2
  exit 2
fi

PIP_CONFIG_FILE=/dev/null \
PIP_INDEX_URL="${RCB_PIP_INDEX_URL:-https://pypi.org/simple}" \
PIP_TRUSTED_HOST="${RCB_PIP_TRUSTED_HOST:-pypi.org}" \
  "${TARGET_PREFIX}/bin/python" -m pip install --no-deps --force-reinstall "${SOURCE_DIR}"

"${TARGET_PREFIX}/bin/python" -c 'import importlib.metadata, kinbot; print(importlib.metadata.version("kinbot"))'
