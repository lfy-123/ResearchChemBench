#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON="$ROOT/.envs/minichem/bin/python"

if [[ ! -x "$PYTHON" ]]; then
  echo "MiniChem runtime is missing; run scripts/bootstrap.sh first" >&2
  exit 1
fi

export MINICHEM_HOME="$ROOT"
export PYTHONPATH="$ROOT/src${PYTHONPATH:+:$PYTHONPATH}"
exec "$PYTHON" -m minichem_mcp_tools.server "$@"
