#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYTHON="${PIPELINE_PYTHON:-python}"
CONFIG="${1:-$ROOT/config.json}"
STAGE2_DOCUMENTS="${2:-$ROOT/runs/pdf_bundle_grobid_20260802/outputs/stage_02_grobid_extract/documents.jsonl}"
MANIFEST="${3:-$ROOT/runs/pdf_bundle_main_papers/main_paper_corpus_manifest.json}"
OUTPUT_ROOT="${4:-$ROOT/runs/stage03_04_redesign/outputs}"
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
exec "$PYTHON" scripts/run_stage03_04.py \
  --config "$CONFIG" \
  --stage2-documents "$STAGE2_DOCUMENTS" \
  --manifest "$MANIFEST" \
  --output-root "$OUTPUT_ROOT"
