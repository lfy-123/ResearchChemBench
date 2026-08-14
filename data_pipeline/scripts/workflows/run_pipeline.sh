#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
PIPELINE_ROOT=$(cd "$SCRIPT_DIR/../.." && pwd)
CONFIG=${1:-$PIPELINE_ROOT/config.example.json}
DEFAULT_PYTHON="$PIPELINE_ROOT/.envs/researchchem-data-pipeline/bin/python"

if [[ -f "$PIPELINE_ROOT/config.local.env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source "$PIPELINE_ROOT/config.local.env"
  set +a
fi

if [[ "${RCB_SETUP_PROXY:-1}" == "1" ]]; then
  # shellcheck disable=SC1090
  source <(curl -fsSL http://deploy.i.h.pjlab.org.cn/infra/scripts/setup_proxy.sh)
fi

cd "$PIPELINE_ROOT"
export PATH="$(dirname "${PYTHON:-$DEFAULT_PYTHON}"):$PATH"
exec "${PYTHON:-$DEFAULT_PYTHON}" -m src.cli run --config "$CONFIG"
