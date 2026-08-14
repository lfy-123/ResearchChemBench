#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
PIPELINE_ROOT=$(cd "$SCRIPT_DIR/../.." && pwd)
DEFAULT_PYTHON="$PIPELINE_ROOT/.envs/researchchem-data-pipeline/bin/python"

for env_file in "$PIPELINE_ROOT/config.local.env" "$PIPELINE_ROOT/../config.local.env"; do
  if [[ -f "$env_file" ]]; then
    set -a
    # shellcheck disable=SC1090
    source "$env_file"
    set +a
  fi
done

if [[ "${RCB_SETUP_PROXY:-1}" == "1" ]]; then
  # shellcheck disable=SC1090
  source <(curl -fsSL http://deploy.i.h.pjlab.org.cn/infra/scripts/setup_proxy.sh)
fi

cd "$PIPELINE_ROOT"
export PATH="$(dirname "${PYTHON:-$DEFAULT_PYTHON}"):$PATH"
exec "${PYTHON:-$DEFAULT_PYTHON}" scripts/workflows/run_stage00_04_batches.py "$@"
