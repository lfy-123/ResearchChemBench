#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
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
"$PYTHON" -m pip install --break-system-packages -e "$ROOT[dev]"
"$PYTHON" -m pip install --break-system-packages -e "$MINERU_REPO[all]"

"$PYTHON" -m mineru.cli.models_download --source auto --model_type pipeline
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
echo "Run: $ROOT/scripts/run_pipeline.sh"
