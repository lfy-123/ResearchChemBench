#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
LIVE_NETWORK=0
STATUS_REPORT=0

usage() {
  cat <<'EOF'
Run all one-file-per-tool ResearchChemBench MCP tests.

Usage:
  bash evaluation/mcp_tools/test_tools/run_tests.sh [options]

Options:
  --live-network   Call PubChem, RCSB PDB, and Catalysis-Hub instead of mocks.
  --status-report  Run scripts/verify_toolbox.py after pytest.
  -h, --help       Show this help.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --live-network)
      LIVE_NETWORK=1
      shift
      ;;
    --status-report)
      STATUS_REPORT=1
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

ENV_DIR="${RESEARCHCHEMBENCH_TOOLBOX_ENV:-$ROOT_DIR/.toolbox_env}"
if [[ ! -x "$ENV_DIR/bin/python" ]]; then
  echo "Missing toolbox environment: $ENV_DIR" >&2
  echo "Run: bash scripts/setup_toolbox_env.sh" >&2
  exit 1
fi

export PATH="$ENV_DIR/bin:$PATH"
export LD_LIBRARY_PATH="$ENV_DIR/lib:${LD_LIBRARY_PATH:-}"
export CHEMGRAPH_ROOT="${CHEMGRAPH_ROOT:-$ROOT_DIR/../ChemGraph}"
if [[ "$LIVE_NETWORK" -eq 1 ]]; then
  export RESEARCHCHEM_LIVE_NETWORK_TESTS=1
else
  unset RESEARCHCHEM_LIVE_NETWORK_TESTS || true
fi

cd "$ROOT_DIR"
PROFILE_TEST_ARGS=()
if [[ "$LIVE_NETWORK" -eq 1 ]]; then
  PROFILE_TEST_ARGS+=("--live-network")
fi
"$ENV_DIR/bin/python" scripts/run_mcp_profile_tool_tests.py "${PROFILE_TEST_ARGS[@]}"

if [[ "$STATUS_REPORT" -eq 1 ]]; then
  "$ENV_DIR/bin/python" scripts/verify_toolbox.py
fi
