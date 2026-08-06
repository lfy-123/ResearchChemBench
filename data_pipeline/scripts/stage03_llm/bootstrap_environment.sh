#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
PIPELINE_ROOT=$(cd "$SCRIPT_DIR/../.." && pwd)
ENV_DIR="${STAGE03_LLM_ENV_DIR:-$PIPELINE_ROOT/.envs/stage03-qwen3-30b-a3b}"
PYTHON_BIN="${STAGE03_LLM_BOOTSTRAP_PYTHON:-python3}"

if [[ ! -x "$ENV_DIR/bin/python" ]]; then
  "$PYTHON_BIN" -m venv "$ENV_DIR"
fi

"$ENV_DIR/bin/python" -m pip install --upgrade pip setuptools wheel
"$ENV_DIR/bin/python" -m pip install -r "$SCRIPT_DIR/requirements.txt"
"$ENV_DIR/bin/python" - <<'PY'
import fastapi
import httpx
import torch
import vllm

print("torch", torch.__version__)
print("cuda_available", torch.cuda.is_available())
print("gpu_count", torch.cuda.device_count())
print("vllm", vllm.__version__)
print("fastapi", fastapi.__version__)
print("httpx", httpx.__version__)
PY
