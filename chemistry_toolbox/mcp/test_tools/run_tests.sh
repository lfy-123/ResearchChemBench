#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
ENV_ROOT="${RESEARCHCHEMBENCH_ENV_ROOT:-$ROOT_DIR/.envs}"
PYTHON_BIN="${RESEARCHCHEM_TEST_PYTHON:-$ENV_ROOT/researchchembench/bin/python}"

cd "$ROOT_DIR"
exec "$PYTHON_BIN" -m pytest -q \
  tests/test_atomic_catalog.py \
  tests/test_dispatch_autonomy.py \
  tests/test_atomic_actions.py \
  tests/test_mcp_tool_package.py \
  tests/test_mcp_profiles.py \
  "$@"
