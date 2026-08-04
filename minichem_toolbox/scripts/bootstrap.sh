#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOFTWARE_CACHE="$ROOT/.mini_software_cache"
RUNTIME="$ROOT/.envs/minichem"
SPEC="$ROOT/environment.yml"
PIP_SPEC="$ROOT/requirements.txt"
PYPI_INDEX="${MINICHEM_PYPI_INDEX_URL:-https://pypi.org/simple}"
PIP_ARGS=(--index-url "$PYPI_INDEX")

if [[ "${MINICHEM_PIP_OFFLINE:-0}" == "1" ]]; then
  PIP_ARGS=(--no-index)
fi

mkdir -p "$ROOT/.envs" "$ROOT/.mini_model_cache"

if [[ ! -x "$RUNTIME/bin/python" ]]; then
  MANAGER="$(command -v mamba || command -v micromamba || command -v conda || true)"
  if [[ -z "$MANAGER" ]]; then
    echo "mamba, micromamba, or conda is required to create .envs/minichem" >&2
    exit 1
  fi
  "$MANAGER" env create -y -p "$RUNTIME" -f "$SPEC"
fi

"$RUNTIME/bin/python" -m pip install \
  "${PIP_ARGS[@]}" \
  -r "$PIP_SPEC"
"$RUNTIME/bin/python" -m pip install \
  "${PIP_ARGS[@]}" \
  --no-build-isolation \
  --no-deps \
  -e "$ROOT"

mkdir -p "$SOFTWARE_CACHE/gaussian/g16/scratch"
chmod 700 "$SOFTWARE_CACHE/gaussian/g16/scratch" 2>/dev/null || true

MINICHEM_HOME="$ROOT" "$RUNTIME/bin/python" "$ROOT/scripts/verify_minichem.py"
echo "MiniChem runtime is ready: $RUNTIME"
