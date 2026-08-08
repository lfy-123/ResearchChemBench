#!/usr/bin/env bash
set -euo pipefail

SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
ROOT_DIR="$(cd "$(dirname "$SCRIPT_PATH")/../.." && pwd)"
ENV_ROOT="${RESEARCHCHEMBENCH_ENV_ROOT:-$ROOT_DIR/.envs}"
ENV_DIR="$ENV_ROOT/researchchembench"
MANAGER=""
SKIP_VERIFY=0
FROM_LOCK=0

usage() {
  cat <<'EOF'
Create the project-local ResearchChemBench framework environment.

Usage:
  bash chemistry_toolbox/scripts/setup_toolbox_env.sh [options]

Options:
  --env-dir PATH          Environment prefix (default: .envs/researchchembench).
  --manager PATH          Explicit mamba/conda executable.
  --from-lock             Replay the tested linux-64 Conda artifact lock.
  --skip-verify           Install only; do not run validation/tests.
  -h, --help              Show this help.

The script installs the ResearchChemBench framework, evaluation runtime, and
open-source chemistry dependencies under tested numerical pins.
Licensed/account-gated programs and API keys are never downloaded or written.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --env-dir)
      ENV_DIR="$(realpath -m "$2")"
      shift 2
      ;;
    --manager)
      MANAGER="$2"
      shift 2
      ;;
    --from-lock)
      FROM_LOCK=1
      shift
      ;;
    --skip-verify)
      SKIP_VERIFY=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ -z "$MANAGER" ]]; then
  if command -v mamba >/dev/null 2>&1; then
    MANAGER="$(command -v mamba)"
  elif command -v conda >/dev/null 2>&1; then
    MANAGER="$(command -v conda)"
  else
    echo "Neither mamba nor conda is available. Use --manager PATH." >&2
    exit 1
  fi
fi

if [[ ! -x "$ENV_DIR/bin/python" ]]; then
  if [[ "$FROM_LOCK" -eq 1 ]]; then
    LOCK_FILE="$ROOT_DIR/chemistry_toolbox/environment/researchchembench/linux-64.explicit.txt"
    [[ -s "$LOCK_FILE" ]] || { echo "Missing framework lock: $LOCK_FILE" >&2; exit 2; }
    "$MANAGER" create -y -p "$ENV_DIR" --file "$LOCK_FILE"
  else
    "$MANAGER" create -y -p "$ENV_DIR" -c conda-forge \
      --file "$ROOT_DIR/chemistry_toolbox/environment/researchchembench/conda-spec.txt"
  fi
fi

PYTHON_BIN="$ENV_DIR/bin/python"
PIP_CONFIG_FILE=/dev/null \
PIP_INDEX_URL="${RCB_PIP_INDEX_URL:-https://pypi.org/simple}" \
PIP_TRUSTED_HOST="${RCB_PIP_TRUSTED_HOST:-pypi.org}" \
  "$PYTHON_BIN" -m pip install --upgrade pip setuptools wheel
PIP_CONFIG_FILE=/dev/null \
PIP_INDEX_URL="${RCB_PIP_INDEX_URL:-https://pypi.org/simple}" \
PIP_TRUSTED_HOST="${RCB_PIP_TRUSTED_HOST:-pypi.org}" \
  "$PYTHON_BIN" -m pip install \
  --constraint "$ROOT_DIR/chemistry_toolbox/environment/researchchembench/constraints.txt" \
  --requirement "$ROOT_DIR/chemistry_toolbox/environment/researchchembench/requirements.txt" \
  --editable "$ROOT_DIR[test]"
"$PYTHON_BIN" -m pip check

"$PYTHON_BIN" "$ROOT_DIR/chemistry_toolbox/scripts/cache_minilm_model.py"

export PATH="$ENV_DIR/bin:$PATH"
export LD_LIBRARY_PATH="$ENV_DIR/lib:${LD_LIBRARY_PATH:-}"
for command in \
  researchchembench \
  researchchembench-eval \
  researchchem-mcp-server \
  researchchem-mcp-install \
  researchchem-tool \
  researchchem-software; do
  [[ -x "$ENV_DIR/bin/$command" ]] || {
    echo "Missing console entry point after project installation: $command" >&2
    exit 1
  }
done

if [[ "$SKIP_VERIFY" -eq 1 ]]; then
  echo "Installation completed without verification: $ENV_DIR"
  exit 0
fi

cd "$ROOT_DIR"
"$PYTHON_BIN" -m chemistry_toolbox.mcp.tool_manager validate
"$PYTHON_BIN" -m pytest -q \
  chemistry_toolbox/tests/test_atomic_catalog.py \
  chemistry_toolbox/tests/test_dispatch_autonomy.py \
  chemistry_toolbox/tests/test_atomic_actions.py \
  chemistry_toolbox/tests/test_mcp_tool_package.py \
  chemistry_toolbox/tests/test_mcp_profiles.py
"$PYTHON_BIN" chemistry_toolbox/scripts/check_mcp_tools.py --smoke
"$PYTHON_BIN" chemistry_toolbox/scripts/verify_toolbox.py

echo "ResearchChemBench framework environment installed and verified: $ENV_DIR"
