#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
PIPELINE_ROOT=$(cd "$SCRIPT_DIR/../.." && pwd)
DEFAULT_PYTHON="$PIPELINE_ROOT/.envs/researchchem-data-pipeline/bin/python"

if [[ -f "$PIPELINE_ROOT/config.local.env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source "$PIPELINE_ROOT/config.local.env"
  set +a
fi

if [[ -z "${RCB_NEW_API_KEY:-}" && -n "${OPENAI_API_KEY:-}" ]]; then
  export RCB_NEW_API_KEY="$OPENAI_API_KEY"
fi
if [[ -z "${RCB_NEW_API_BASE_URL:-}" && -n "${OPENAI_BASE_URL:-}" ]]; then
  export RCB_NEW_API_BASE_URL="$OPENAI_BASE_URL"
fi

# The New API tunnel is loopback-only. Do not send it through the cluster proxy.
export NO_PROXY="127.0.0.1,localhost,${NO_PROXY:-}"
export no_proxy="127.0.0.1,localhost,${no_proxy:-}"

cd "$PIPELINE_ROOT"
exec "${PYTHON:-$DEFAULT_PYTHON}" scripts/workflows/run_stage00_05_api_batches.py "$@"
