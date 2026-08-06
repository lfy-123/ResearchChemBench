#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
PIPELINE_ROOT=$(cd "$SCRIPT_DIR/../.." && pwd)
ENV_DIR="${STAGE03_LLM_ENV_DIR:-$PIPELINE_ROOT/.envs/stage03-qwen3-30b-a3b}"
MODEL_ID="${STAGE03_LLM_MODEL_ID:-Qwen/Qwen3-30B-A3B-Instruct-2507}"
MODEL_DIR="${STAGE03_LLM_MODEL_DIR:-/mnt/shared-storage-user/liyuqiang/mdoels/Qwen3-30B-A3B-Instruct-2507}"

if [[ ! -x "$ENV_DIR/bin/hf" ]]; then
  echo "stage03 LLM environment is missing; run bootstrap_environment.sh first" >&2
  exit 1
fi

mkdir -p "$MODEL_DIR"
"$ENV_DIR/bin/hf" download "$MODEL_ID" \
  --local-dir "$MODEL_DIR" \
  --exclude '*.gguf' '*.bin'

test -s "$MODEL_DIR/config.json"
test -s "$MODEL_DIR/tokenizer_config.json"
echo "model ready: $MODEL_DIR"
