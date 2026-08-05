#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
DEFAULT_ENV="$PROJECT_ROOT/.envs/researchchem-data-pipeline"
DEFAULT_CREDENTIALS="/mnt/shared-storage-user/liyuqiang/benchmark/pipline_demo/pdfs/xinghe.txt"

XINGHE_PYTHON="${XINGHE_PYTHON:-$DEFAULT_ENV/bin/python}"
XINGHE_CREDENTIALS="${XINGHE_CREDENTIALS:-$DEFAULT_CREDENTIALS}"

if [[ ! -x "$XINGHE_PYTHON" ]]; then
  echo "error: Python is not executable: $XINGHE_PYTHON" >&2
  exit 1
fi

exec "$XINGHE_PYTHON" "$SCRIPT_DIR/download_xinghe_batch.py" \
  --credentials "$XINGHE_CREDENTIALS" \
  "$@"
