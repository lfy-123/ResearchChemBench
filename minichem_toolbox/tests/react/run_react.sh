#!/usr/bin/env bash
set -euo pipefail

REACT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOLBOX_ROOT="$(cd "$REACT_DIR/../.." && pwd)"
RUNTIME_PYTHON="$TOOLBOX_ROOT/.envs/minichem/bin/python"

if [[ ! -x "$RUNTIME_PYTHON" ]]; then
  echo "MiniChem runtime is missing; run scripts/bootstrap.sh first" >&2
  exit 1
fi

for candidate in "$TOOLBOX_ROOT/config.local.env" "$TOOLBOX_ROOT/../config.local.env"; do
  if [[ -f "$candidate" ]]; then
    set -a
    # shellcheck disable=SC1090
    source "$candidate"
    set +a
    break
  fi
done

# The catalog's evaluator default is sized for the full benchmark worker.  A
# local/container smoke test may have a smaller CPU affinity, which nproc
# reports correctly.
export RESEARCHCHEMBENCH_AVAILABLE_CPU_CORES="${RESEARCHCHEMBENCH_AVAILABLE_CPU_CORES:-$(nproc)}"

exec "$RUNTIME_PYTHON" "$REACT_DIR/react_agent.py" "$@"
