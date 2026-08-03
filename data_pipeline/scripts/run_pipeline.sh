#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PIPELINE_PYTHON="${PIPELINE_PYTHON:-python}"
PIPELINE_CONFIG="${PIPELINE_CONFIG:-${1:-$ROOT/config.json}}"
PIPELINE_SUMMARY="${PIPELINE_SUMMARY:-${2:-$ROOT/runs/current/outputs/run_summary.json}}"
PIPELINE_ENV_FILE="${PIPELINE_ENV_FILE:-$ROOT/../config.local.env}"

if [[ -f "$PIPELINE_ENV_FILE" ]]; then
  set -a
  # shellcheck disable=SC1090
  source "$PIPELINE_ENV_FILE"
  set +a
fi

RESOURCE_LLM_URL="${RESOURCE_LLM_URL:-${JUDGE_API_BASE:-https://api.deepseek.com/v1}}"
RESOURCE_LLM_API_KEY="${RESOURCE_LLM_API_KEY:-${JUDGE_API_KEY:-}}"
RESOURCE_LLM_MODEL_NAME="${RESOURCE_LLM_MODEL_NAME:-${JUDGE_MODEL_NAME:-deepseek-v4-flash}}"
export RESOURCE_LLM_URL RESOURCE_LLM_API_KEY RESOURCE_LLM_MODEL_NAME
export HF_ENDPOINT="${HF_ENDPOINT:-https://hf-mirror.com}"
export HF_HUB_DOWNLOAD_TIMEOUT="${HF_HUB_DOWNLOAD_TIMEOUT:-600}"

cd "$ROOT"
exec "$PIPELINE_PYTHON" -m src run \
  --config "$PIPELINE_CONFIG" \
  --output "$PIPELINE_SUMMARY"
