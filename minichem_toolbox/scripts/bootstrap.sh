#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CACHE="$ROOT/.mini_software_cache"
RUNTIME="$CACHE/runtimes/minichem"
PACK="$CACHE/runtime_packs/minichem.tar.gz"
SPEC="$CACHE/environment.yml"
PIP_SPEC="$CACHE/requirements-runtime.txt"
PYPI_INDEX="${MINICHEM_PYPI_INDEX_URL:-https://pypi.org/simple}"

mkdir -p "$CACHE/runtimes" "$ROOT/.mini_model_cache"

if [[ ! -x "$RUNTIME/bin/python" ]]; then
  if [[ -f "$PACK" ]]; then
    mkdir -p "$RUNTIME"
    tar -xzf "$PACK" -C "$RUNTIME"
  else
    MANAGER="$(command -v mamba || command -v micromamba || command -v conda || true)"
    if [[ -z "$MANAGER" ]]; then
      echo "mamba, micromamba, or conda is required when no runtime pack is present" >&2
      exit 1
    fi
    "$MANAGER" env create -y -p "$RUNTIME" -f "$SPEC"
  fi
fi

if [[ -x "$RUNTIME/bin/conda-unpack" ]]; then
  "$RUNTIME/bin/conda-unpack"
fi

"$RUNTIME/bin/python" -m pip install \
  --index-url "$PYPI_INDEX" \
  -r "$PIP_SPEC"
"$RUNTIME/bin/python" -m pip install --no-deps -e "$ROOT"

mkdir -p "$CACHE/gaussian/g16/scratch"
chmod 700 "$CACHE/gaussian/g16/scratch" 2>/dev/null || true

MINICHEM_HOME="$ROOT" "$RUNTIME/bin/python" "$ROOT/scripts/verify_minichem.py"
echo "MiniChem runtime is ready: $RUNTIME"
