#!/usr/bin/env bash
set -euo pipefail

SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
ROOT_DIR="$(cd "$(dirname "$SCRIPT_PATH")/../.." && pwd)"
cd "$ROOT_DIR"

ENV_ROOT="${RESEARCHCHEMBENCH_ENV_ROOT:-$ROOT_DIR/.envs}"
FRAMEWORK_ENV="${RESEARCHCHEMBENCH_FRAMEWORK_ENV:-$ENV_ROOT/researchchembench}"
if [[ ! -x "$FRAMEWORK_ENV/bin/python" ]]; then
  echo "ResearchChemBench framework environment is missing: $FRAMEWORK_ENV" >&2
  exit 2
fi
export PATH="$FRAMEWORK_ENV/bin:$PATH"
export LD_LIBRARY_PATH="$FRAMEWORK_ENV/lib:${LD_LIBRARY_PATH:-}"

exec "$FRAMEWORK_ENV/bin/python" -m chemistry_toolbox.mcp.tool_manager "$@"
