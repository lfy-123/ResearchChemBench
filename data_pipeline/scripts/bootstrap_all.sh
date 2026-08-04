#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
export PIPELINE_PYTHON="${PIPELINE_PYTHON:-python}"
export MODEL_CACHE_ROOT="${MODEL_CACHE_ROOT:-$ROOT/.model_cache}"
export HF_ENDPOINT="${HF_ENDPOINT:-https://hf-mirror.com}"
export HF_HUB_DOWNLOAD_TIMEOUT="${HF_HUB_DOWNLOAD_TIMEOUT:-600}"
export HF_HUB_ETAG_TIMEOUT="${HF_HUB_ETAG_TIMEOUT:-60}"

bash "$ROOT/scripts/bootstrap_grobid.sh"
bash "$ROOT/scripts/bootstrap_stage_gates.sh"
bash "$ROOT/scripts/bootstrap_mineru.sh"

echo
echo "Data pipeline runtime is ready."
echo "Model cache: $MODEL_CACHE_ROOT"
echo "Run: bash $ROOT/scripts/run_pipeline.sh"
