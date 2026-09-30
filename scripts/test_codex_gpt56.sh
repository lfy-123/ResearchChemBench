#!/usr/bin/env bash
# Codex entrypoint over the final verified task releases.
# Usage:
#   bash scripts/test_codex_gpt56.sh paper_2f2aa11ea61a32bb --dry-run
#   bash scripts/test_codex_gpt56.sh --mode autonomous_research paper_2f2aa11ea61a32bb paper_60f4c45810428116 --resume
# Test settings and credentials: config.local.env (gitignored), RCB_CODEX_*.
# Codex configuration: https://developers.openai.com/codex/config-reference/
set -euo pipefail

RCB_TEST_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$RCB_TEST_ROOT"

RCB_TEST_LOCAL_CONFIG="${RESEARCHCHEMBENCH_LOCAL_CONFIG:-$RCB_TEST_ROOT/config.local.env}"
if [[ -f "$RCB_TEST_LOCAL_CONFIG" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "$RCB_TEST_LOCAL_CONFIG"
  set +a
fi
RCB_TEST_ENV_ROOT="${RESEARCHCHEMBENCH_ENV_ROOT:-$RCB_TEST_ROOT/.envs}"
RCB_TEST_FRAMEWORK_ENV="${RESEARCHCHEMBENCH_FRAMEWORK_ENV:-$RCB_TEST_ENV_ROOT/researchchembench}"
if [[ ! -x "$RCB_TEST_FRAMEWORK_ENV/bin/python" ]]; then
  echo "Missing framework Python: $RCB_TEST_FRAMEWORK_ENV/bin/python" >&2
  exit 2
fi
export RESEARCHCHEMBENCH_ENV_ROOT="$RCB_TEST_ENV_ROOT"
export PATH="$RCB_TEST_FRAMEWORK_ENV/bin:$PATH"
export LD_LIBRARY_PATH="$RCB_TEST_FRAMEWORK_ENV/lib:${LD_LIBRARY_PATH:-}"
export RCB_CODEX_BASE_URL="${RCB_CODEX_BASE_URL:-http://35.220.164.252:3888}"
export RCB_CODEX_MODEL="${RCB_CODEX_MODEL:-gpt-5.6-sol}"
export RCB_CODEX_REASONING_EFFORT="${RCB_CODEX_REASONING_EFFORT:-high}"

exec "$RCB_TEST_FRAMEWORK_ENV/bin/python" -m evaluation.pilot "$@"
