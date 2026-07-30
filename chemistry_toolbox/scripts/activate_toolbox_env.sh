#!/usr/bin/env bash

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
  echo "This script must be sourced: source chemistry_toolbox/scripts/activate_toolbox_env.sh" >&2
  exit 2
fi

SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
ROOT_DIR="$(cd "$(dirname "$SCRIPT_PATH")/../.." && pwd)"
ENV_DIR="${RESEARCHCHEMBENCH_TOOLBOX_ENV:-$ROOT_DIR/.toolbox_env}"

if [[ ! -x "$ENV_DIR/bin/python" ]]; then
  echo "Toolbox environment not found at $ENV_DIR" >&2
  echo "Create it with: bash chemistry_toolbox/scripts/setup_toolbox_env.sh" >&2
  return 1
fi

export PATH="$ENV_DIR/bin:$PATH"
export LD_LIBRARY_PATH="$ENV_DIR/lib:${LD_LIBRARY_PATH:-}"

echo "ResearchChemBench toolbox environment activated: $ENV_DIR"
