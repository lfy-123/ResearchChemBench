#!/usr/bin/env bash

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
  echo "This script must be sourced: source chemistry_toolbox/scripts/activate_toolbox_env.sh" >&2
  exit 2
fi

SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
ROOT_DIR="$(cd "$(dirname "$SCRIPT_PATH")/../.." && pwd)"
ENV_ROOT="${RESEARCHCHEMBENCH_ENV_ROOT:-$ROOT_DIR/.envs}"
ENV_DIR="${RESEARCHCHEMBENCH_FRAMEWORK_ENV:-$ENV_ROOT/researchchembench}"

if [[ ! -x "$ENV_DIR/bin/python" ]]; then
  echo "Toolbox environment not found at $ENV_DIR" >&2
  echo "Create it with: bash chemistry_toolbox/scripts/setup_toolbox_env.sh" >&2
  return 1
fi

export PATH="$ENV_DIR/bin:$PATH"
export LD_LIBRARY_PATH="$ENV_DIR/lib:${LD_LIBRARY_PATH:-}"
export RESEARCHCHEMBENCH_MODEL_CACHE="${RESEARCHCHEMBENCH_MODEL_CACHE:-$ROOT_DIR/.model_cache}"
export RESEARCHCHEMBENCH_RUNTIME_CACHE="${RESEARCHCHEMBENCH_RUNTIME_CACHE:-$ROOT_DIR/.runtime_cache}"
export XDG_CACHE_HOME="$RESEARCHCHEMBENCH_RUNTIME_CACHE"
mkdir -p "$RESEARCHCHEMBENCH_RUNTIME_CACHE"

echo "ResearchChemBench framework environment activated: $ENV_DIR"
