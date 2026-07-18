#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_DIR="$ROOT_DIR/.toolbox_env"
CHEMGRAPH_ROOT_VALUE="$ROOT_DIR/../ChemGraph"
MANAGER=""
SKIP_VERIFY=0

usage() {
  cat <<'EOF'
Create the project-local ResearchChemBench chemistry toolbox environment.

Usage:
  bash scripts/setup_toolbox_env.sh [options]

Options:
  --env-dir PATH          Environment prefix (default: .toolbox_env).
  --chemgraph-root PATH   ChemGraph checkout (default: ../ChemGraph).
  --manager PATH          Explicit mamba/conda executable.
  --skip-verify           Install only; do not run validation/tests.
  -h, --help              Show this help.

The script installs open-source conda-forge backends, then the Python
dependencies in environment/toolbox-pip.txt under tested numerical pins.
Licensed/account-gated programs and API keys are never downloaded or written.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --env-dir)
      ENV_DIR="$(realpath -m "$2")"
      shift 2
      ;;
    --chemgraph-root)
      CHEMGRAPH_ROOT_VALUE="$(realpath -m "$2")"
      shift 2
      ;;
    --manager)
      MANAGER="$2"
      shift 2
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
  "$MANAGER" create -y -p "$ENV_DIR" -c conda-forge \
    --file "$ROOT_DIR/environment/toolbox-conda.txt"
fi

PYTHON_BIN="$ENV_DIR/bin/python"
"$PYTHON_BIN" -m pip install --upgrade pip setuptools wheel
"$PYTHON_BIN" -m pip install \
  --constraint "$ROOT_DIR/environment/toolbox-constraints.txt" \
  --requirement "$ROOT_DIR/environment/toolbox-pip.txt" \
  --editable "$ROOT_DIR[test]"

"$PYTHON_BIN" "$ROOT_DIR/scripts/configure_mcp_conda_envs.py"

if [[ "$SKIP_VERIFY" -eq 1 ]]; then
  echo "Installation completed without verification: $ENV_DIR"
  exit 0
fi

export PATH="$ENV_DIR/bin:$PATH"
export LD_LIBRARY_PATH="$ENV_DIR/lib:${LD_LIBRARY_PATH:-}"
export CHEMGRAPH_ROOT="$CHEMGRAPH_ROOT_VALUE"

cd "$ROOT_DIR"
"$PYTHON_BIN" -m evaluation.mcp_tools.tool_manager validate
"$PYTHON_BIN" -m pytest -q \
  tests/test_atomic_catalog.py \
  tests/test_dispatch_autonomy.py \
  tests/test_atomic_actions.py \
  tests/test_mcp_tool_package.py \
  tests/test_mcp_profiles.py
"$PYTHON_BIN" scripts/check_mcp_tools.py --smoke
"$PYTHON_BIN" scripts/verify_toolbox.py

echo "Toolbox environment installed and verified: $ENV_DIR"
