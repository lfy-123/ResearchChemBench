#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PIPELINE_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
PIPELINE_PYTHON="${PIPELINE_PYTHON:-$PIPELINE_ROOT/.envs/researchchem-data-pipeline/bin/python}"

config=""
output=""
backend="sandbox"
sandbox_cpu="128"
sandbox_memory="256Gi"
sandbox_lifecycle_minutes="1440"
sandbox_cleanup="stop"
microbatch=""
microbatch_size=""
microbatch_concurrency=""
microbatch_softcite_instances=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --config)
      config="$2"
      shift 2
      ;;
    --output)
      output="$2"
      shift 2
      ;;
    --backend)
      backend="$2"
      shift 2
      ;;
    --sandbox-cpu)
      sandbox_cpu="$2"
      shift 2
      ;;
    --sandbox-memory)
      sandbox_memory="$2"
      shift 2
      ;;
    --sandbox-lifecycle-minutes)
      sandbox_lifecycle_minutes="$2"
      shift 2
      ;;
    --sandbox-cleanup)
      sandbox_cleanup="$2"
      shift 2
      ;;
    --microbatch)
      microbatch="--microbatch"
      shift
      ;;
    --no-microbatch)
      microbatch="--no-microbatch"
      shift
      ;;
    --microbatch-size)
      microbatch_size="$2"
      shift 2
      ;;
    --microbatch-concurrency)
      microbatch_concurrency="$2"
      shift 2
      ;;
    --microbatch-softcite-instances)
      microbatch_softcite_instances="$2"
      shift 2
      ;;
    -h|--help)
      cat <<'EOF'
Usage: run_stage_01_04_screening.sh --config CONFIG [options]

Runs the existing pipeline through Stage 04. The config must set or will be
generated with stop_after=resource_limits.

Options:
  --output PATH
  --backend sandbox|local
  --sandbox-cpu N
  --sandbox-memory SIZE
  --sandbox-lifecycle-minutes N
  --sandbox-cleanup keep|stop|delete
  --microbatch | --no-microbatch
  --microbatch-size N
  --microbatch-concurrency N
  --microbatch-softcite-instances N
EOF
      exit 0
      ;;
    *)
      echo "error: unknown argument: $1" >&2
      exit 2
      ;;
  esac
done

if [[ -z "$config" ]]; then
  echo "error: --config is required" >&2
  exit 2
fi
if [[ ! -x "$PIPELINE_PYTHON" ]]; then
  echo "error: Python is not executable: $PIPELINE_PYTHON" >&2
  exit 1
fi
if [[ ! -f "$config" ]]; then
  echo "error: config does not exist: $config" >&2
  exit 1
fi
if [[ "$backend" != "sandbox" && "$backend" != "local" ]]; then
  echo "error: --backend must be sandbox or local" >&2
  exit 2
fi

stop_after="$($PIPELINE_PYTHON -c 'import json,sys; print(json.load(open(sys.argv[1], encoding="utf-8")).get("stop_after", ""))' "$config")"
if [[ "$stop_after" != "resource_limits" ]]; then
  echo "error: four-stage workflow requires stop_after=resource_limits in $config" >&2
  exit 2
fi

command=(
  "$PIPELINE_PYTHON" -m src run
  --config "$config"
  --execution-backend "$backend"
)
if [[ -n "$output" ]]; then
  command+=(--output "$output")
fi
if [[ -n "$microbatch" ]]; then
  command+=("$microbatch")
fi
if [[ -n "$microbatch_size" ]]; then
  command+=(--microbatch-size "$microbatch_size")
fi
if [[ -n "$microbatch_concurrency" ]]; then
  command+=(--microbatch-concurrency "$microbatch_concurrency")
fi
if [[ -n "$microbatch_softcite_instances" ]]; then
  command+=(--microbatch-softcite-instances "$microbatch_softcite_instances")
fi
if [[ "$backend" == "sandbox" ]]; then
  command+=(
    --sandbox-cpu "$sandbox_cpu"
    --sandbox-memory "$sandbox_memory"
    --sandbox-lifecycle-minutes "$sandbox_lifecycle_minutes"
    --sandbox-cleanup "$sandbox_cleanup"
  )
fi

cd "$PIPELINE_ROOT"
exec "${command[@]}"
