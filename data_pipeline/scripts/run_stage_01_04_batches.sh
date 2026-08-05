#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PIPELINE_PYTHON="${PIPELINE_PYTHON:-$SCRIPT_DIR/../.envs/researchchem-data-pipeline/bin/python}"

if [[ ! -x "$PIPELINE_PYTHON" ]]; then
  echo "error: Python is not executable: $PIPELINE_PYTHON" >&2
  exit 1
fi

exec "$PIPELINE_PYTHON" "$SCRIPT_DIR/run_stage_01_04_batches.py" "$@"
