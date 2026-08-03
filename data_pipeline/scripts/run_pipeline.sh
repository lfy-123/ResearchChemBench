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

# ---------------------------- LLM parameters ----------------------------
# ScientificRecord evidence extraction
EXTRACTION_LLM_URL="${EXTRACTION_LLM_URL:-${JUDGE_API_BASE:-https://api.deepseek.com/v1}}"
EXTRACTION_LLM_API_KEY="${EXTRACTION_LLM_API_KEY:-${JUDGE_API_KEY:-}}"
EXTRACTION_LLM_MODEL_NAME="${EXTRACTION_LLM_MODEL_NAME:-${JUDGE_MODEL_NAME:-deepseek-v4-flash}}"

# Select exactly one task type for each paper
TASK_CLASSIFICATION_LLM_URL="${TASK_CLASSIFICATION_LLM_URL:-${JUDGE_API_BASE:-https://api.deepseek.com/v1}}"
TASK_CLASSIFICATION_LLM_API_KEY="${TASK_CLASSIFICATION_LLM_API_KEY:-${JUDGE_API_KEY:-}}"
TASK_CLASSIFICATION_LLM_MODEL_NAME="${TASK_CLASSIFICATION_LLM_MODEL_NAME:-${JUDGE_MODEL_NAME:-deepseek-v4-flash}}"

# Normalize explicitly reported CPU, GPU, memory, and runtime evidence
RESOURCE_LLM_URL="${RESOURCE_LLM_URL:-${JUDGE_API_BASE:-https://api.deepseek.com/v1}}"
RESOURCE_LLM_API_KEY="${RESOURCE_LLM_API_KEY:-${JUDGE_API_KEY:-}}"
RESOURCE_LLM_MODEL_NAME="${RESOURCE_LLM_MODEL_NAME:-${JUDGE_MODEL_NAME:-deepseek-v4-flash}}"

# Generate the task instruction, public inputs, hidden answer, and rubric
TASK_GENERATION_LLM_URL="${TASK_GENERATION_LLM_URL:-${JUDGE_API_BASE:-https://api.deepseek.com/v1}}"
TASK_GENERATION_LLM_API_KEY="${TASK_GENERATION_LLM_API_KEY:-${JUDGE_API_KEY:-}}"
TASK_GENERATION_LLM_MODEL_NAME="${TASK_GENERATION_LLM_MODEL_NAME:-${JUDGE_MODEL_NAME:-deepseek-v4-pro}}"

# Role-separated candidate review
REVIEW_LLM_URL="${REVIEW_LLM_URL:-${JUDGE_API_BASE:-https://api.deepseek.com/v1}}"
REVIEW_LLM_API_KEY="${REVIEW_LLM_API_KEY:-${JUDGE_API_KEY:-}}"
REVIEW_LLM_MODEL_NAME="${REVIEW_LLM_MODEL_NAME:-${JUDGE_MODEL_NAME:-deepseek-v4-flash}}"
# -----------------------------------------------------------------------

missing_keys=()
for key_name in \
  EXTRACTION_LLM_API_KEY \
  RESOURCE_LLM_API_KEY \
  TASK_CLASSIFICATION_LLM_API_KEY \
  TASK_GENERATION_LLM_API_KEY \
  REVIEW_LLM_API_KEY; do
  if [[ -z "${!key_name}" ]]; then
    missing_keys+=("$key_name")
  fi
done
if (( ${#missing_keys[@]} > 0 )); then
  echo "Set the following API keys at the top of this script or as environment variables:" >&2
  printf '  %s\n' "${missing_keys[@]}" >&2
  exit 2
fi

export EXTRACTION_LLM_URL EXTRACTION_LLM_API_KEY EXTRACTION_LLM_MODEL_NAME
export RESOURCE_LLM_URL RESOURCE_LLM_API_KEY RESOURCE_LLM_MODEL_NAME
export TASK_CLASSIFICATION_LLM_URL TASK_CLASSIFICATION_LLM_API_KEY
export TASK_CLASSIFICATION_LLM_MODEL_NAME
export TASK_GENERATION_LLM_URL TASK_GENERATION_LLM_API_KEY TASK_GENERATION_LLM_MODEL_NAME
export REVIEW_LLM_URL REVIEW_LLM_API_KEY REVIEW_LLM_MODEL_NAME

cd "$ROOT"
"$PIPELINE_PYTHON" -m src run \
  --config "$PIPELINE_CONFIG" \
  --output "$PIPELINE_SUMMARY"
