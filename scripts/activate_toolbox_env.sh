#!/usr/bin/env bash

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
  echo "This script must be sourced: source scripts/activate_toolbox_env.sh" >&2
  exit 2
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_DIR="${RESEARCHCHEMBENCH_TOOLBOX_ENV:-$ROOT_DIR/.toolbox_env}"

if [[ ! -x "$ENV_DIR/bin/python" ]]; then
  echo "Toolbox environment not found at $ENV_DIR" >&2
  echo "Create it with: bash scripts/setup_toolbox_env.sh" >&2
  return 1
fi

export PATH="$ENV_DIR/bin:$PATH"
export LD_LIBRARY_PATH="$ENV_DIR/lib:${LD_LIBRARY_PATH:-}"
export CHEMGRAPH_ROOT="${CHEMGRAPH_ROOT:-$ROOT_DIR/../ChemGraph}"
export CHEMGRAPH_PYTHON="$ENV_DIR/bin/python"

echo "ResearchChemBench toolbox environment activated: $ENV_DIR"
