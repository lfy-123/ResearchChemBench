#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
MINERU_REPO="$ROOT/third_party/MinerU"
MINERU_COMMIT="79d6d8d79fb8f3ddba5cc34c07a16f0ec36f56c7"

command -v git >/dev/null || {
  echo "git is required." >&2
  exit 1
}
command -v pdftotext >/dev/null || {
  echo "pdftotext is required." >&2
  if [[ "$(uname -s)" == "Darwin" ]]; then
    echo "Install it with: brew install poppler" >&2
  else
    echo "On Ubuntu/Debian: sudo apt-get install poppler-utils" >&2
  fi
  exit 1
}

mkdir -p "$ROOT/third_party"
if [[ ! -d "$MINERU_REPO/.git" ]]; then
  git clone https://github.com/opendatalab/MinerU.git "$MINERU_REPO"
fi

if ! git -C "$MINERU_REPO" diff --quiet; then
  echo "MinerU checkout has local changes; refusing to switch commits." >&2
  exit 1
fi
git -C "$MINERU_REPO" fetch origin "$MINERU_COMMIT"
git -C "$MINERU_REPO" checkout "$MINERU_COMMIT"

PYTHON="$(command -v "${PIPELINE_PYTHON:-python}")"
MODEL_CACHE_ROOT="${MODEL_CACHE_ROOT:-$ROOT/.model_cache}"
export HF_HOME="${HF_HOME:-$MODEL_CACHE_ROOT/huggingface}"
export HUGGINGFACE_HUB_CACHE="${HUGGINGFACE_HUB_CACHE:-$HF_HOME/hub}"
export MODELSCOPE_CACHE="${MODELSCOPE_CACHE:-$MODEL_CACHE_ROOT/modelscope}"
export MINERU_TOOLS_CONFIG_JSON="${MINERU_TOOLS_CONFIG_JSON:-$MODEL_CACHE_ROOT/mineru/mineru.json}"
mkdir -p "$(dirname "$MINERU_TOOLS_CONFIG_JSON")" "$HF_HOME" "$MODELSCOPE_CACHE"
"$PYTHON" -m pip install -e "$ROOT[dev]"
"$PYTHON" -m pip install \
  --index-url https://download.pytorch.org/whl/cpu \
  "torch==2.6.0" \
  "torchvision==0.21.0"
"$PYTHON" -m pip install \
  --constraint "$ROOT/mineru-constraints.txt" \
  -e "$MINERU_REPO[pipeline]"
"$PYTHON" -m pip install "transformers==4.57.3"

(cd "$MODEL_CACHE_ROOT" && "$PYTHON" -m mineru.cli.models_download --source auto --model_type pipeline)
"$PYTHON" "$ROOT/scripts/bootstrap/prepare_model_cache.py" --cache "$MODEL_CACHE_ROOT"
MINERU="$("$PYTHON" -c 'import shutil; print(shutil.which("mineru") or "")')"
if [[ -z "$MINERU" ]]; then
  echo "MinerU entry point was not installed for $PYTHON." >&2
  exit 1
fi
"$MINERU" --version
"$PYTHON" -m src --help >/dev/null

echo
echo "ResearchChemBench and MinerU are ready."
echo "Python: $PYTHON"
echo "Run: $ROOT/scripts/workflows/run_pipeline.sh"
