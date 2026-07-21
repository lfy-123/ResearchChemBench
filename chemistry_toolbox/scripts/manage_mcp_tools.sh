#!/usr/bin/env bash
set -euo pipefail

SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
ROOT_DIR="$(cd "$(dirname "$SCRIPT_PATH")/../.." && pwd)"
cd "$ROOT_DIR"

if [[ -x "$ROOT_DIR/.toolbox_env/bin/python" ]]; then
  export PATH="$ROOT_DIR/.toolbox_env/bin:$PATH"
  export LD_LIBRARY_PATH="$ROOT_DIR/.toolbox_env/lib:${LD_LIBRARY_PATH:-}"
elif [[ -f "$ROOT_DIR/.venv/bin/activate" ]]; then
  # shellcheck disable=SC1091
  source "$ROOT_DIR/.venv/bin/activate"
fi

exec python -m chemistry_toolbox.mcp.tool_manager "$@"
