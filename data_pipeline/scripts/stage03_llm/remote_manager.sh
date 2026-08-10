#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: remote_manager.sh <start|start-screening|start-mineru|stop|status>" >&2
}

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
PIPELINE_ROOT=$(cd "$SCRIPT_DIR/../.." && pwd)
RUNTIME_DIR="${STAGE03_LLM_RUNTIME_DIR:-/tmp/researchchem-stage03-llm}"
ENV_DIR="${RCB_PIPELINE_ENV_DIR:-$PIPELINE_ROOT/.envs/researchchem-data-pipeline}"
VLLM_PORT="${STAGE03_LLM_VLLM_PORT:-18082}"
GATEWAY_PORT="${STAGE03_LLM_GATEWAY_PORT:-18083}"
MINERU_PORT="${STAGE04_MINERU_PORT:-18084}"
MINERU_ENV_DIR="${STAGE04_MINERU_ENV_DIR:-$ENV_DIR}"

pid_alive() {
  local file=$1
  [[ -s "$file" ]] && kill -0 "$(<"$file")" 2>/dev/null
}

stop_pid() {
  local file=$1
  if pid_alive "$file"; then
    local pid
    pid=$(<"$file")
    kill -TERM "$pid" 2>/dev/null || true
    for _ in $(seq 1 30); do
      kill -0 "$pid" 2>/dev/null || break
      sleep 1
    done
    kill -KILL "$pid" 2>/dev/null || true
  fi
  rm -f "$file"
}

wait_http() {
  local url=$1
  local timeout=$2
  local pid_file=${3:-}
  local deadline=$((SECONDS + timeout))
  while (( SECONDS < deadline )); do
    if curl --noproxy '*' -fsS "$url" >/dev/null 2>&1; then
      return 0
    fi
    if [[ -n "$pid_file" ]] && ! pid_alive "$pid_file"; then
      return 1
    fi
    sleep 5
  done
  return 1
}

start_screening_service() {
  test -x "$ENV_DIR/bin/python"
  test -s "${STAGE03_LLM_MODEL_DIR:-/mnt/shared-storage-user/liyuqiang/mdoels/Qwen3-30B-A3B-Instruct-2507}/config.json"
  mkdir -p "$RUNTIME_DIR/logs" "$RUNTIME_DIR/pids"
  "$0" stop-services >/dev/null 2>&1 || true
  export no_proxy="localhost,127.0.0.1,${no_proxy:-}"
  export NO_PROXY="$no_proxy"
  nohup "$ENV_DIR/bin/python" "$SCRIPT_DIR/vllm_entry.py" \
    >"$RUNTIME_DIR/logs/vllm.log" 2>&1 &
  echo $! >"$RUNTIME_DIR/pids/vllm.pid"
  if ! wait_http "http://127.0.0.1:$VLLM_PORT/v1/models" \
    "${STAGE03_LLM_STARTUP_TIMEOUT:-1800}" "$RUNTIME_DIR/pids/vllm.pid"; then
    tail -n 200 "$RUNTIME_DIR/logs/vllm.log" >&2 || true
    "$0" stop-screening >/dev/null 2>&1 || true
    return 1
  fi
  nohup "$ENV_DIR/bin/python" "$SCRIPT_DIR/fastapi_gateway.py" \
    >"$RUNTIME_DIR/logs/gateway.log" 2>&1 &
  echo $! >"$RUNTIME_DIR/pids/gateway.pid"
  if ! wait_http "http://127.0.0.1:$GATEWAY_PORT/health" 120 \
    "$RUNTIME_DIR/pids/gateway.pid"; then
    tail -n 100 "$RUNTIME_DIR/logs/gateway.log" >&2 || true
    "$0" stop-screening >/dev/null 2>&1 || true
    return 1
  fi
}

command=${1:-}
case "$command" in
  start|start-screening)
    start_screening_service
    "$0" status
    ;;
  start-mineru)
    test -x "$MINERU_ENV_DIR/bin/mineru-api"
    test -s "${MINERU_TOOLS_CONFIG_JSON:-$PIPELINE_ROOT/.model_cache/mineru/mineru.json}"
    mkdir -p "$RUNTIME_DIR/logs" "$RUNTIME_DIR/pids"
    "$0" stop-services >/dev/null 2>&1 || true
    export no_proxy="localhost,127.0.0.1,${no_proxy:-}"
    export NO_PROXY="$no_proxy"
    export MINERU_DEVICE_MODE="${MINERU_DEVICE_MODE:-cuda}"
    export MINERU_MODEL_SOURCE="${MINERU_MODEL_SOURCE:-local}"
    export MINERU_API_MAX_CONCURRENT_REQUESTS="${MINERU_API_MAX_CONCURRENT_REQUESTS:-3}"
    nohup "$MINERU_ENV_DIR/bin/mineru-api" --host 127.0.0.1 --port "$MINERU_PORT" \
      >"$RUNTIME_DIR/logs/mineru-api.log" 2>&1 &
    echo $! >"$RUNTIME_DIR/pids/mineru-api.pid"
    if ! wait_http "http://127.0.0.1:$MINERU_PORT/health" \
      "${STAGE04_MINERU_STARTUP_TIMEOUT:-1800}" "$RUNTIME_DIR/pids/mineru-api.pid"; then
      tail -n 200 "$RUNTIME_DIR/logs/mineru-api.log" >&2 || true
      "$0" stop-mineru >/dev/null 2>&1 || true
      exit 1
    fi
    "$0" status
    ;;
  stop-screening)
    stop_pid "$RUNTIME_DIR/pids/gateway.pid"
    stop_pid "$RUNTIME_DIR/pids/vllm.pid"
    echo "screening services stopped"
    ;;
  stop-mineru)
    stop_pid "$RUNTIME_DIR/pids/mineru-api.pid"
    echo "MinerU service stopped"
    ;;
  stop-services|stop)
    "$0" stop-screening >/dev/null 2>&1 || true
    "$0" stop-mineru >/dev/null 2>&1 || true
    echo "shared GPU worker services stopped"
    ;;
  status)
    vllm_status=stopped
    gateway_status=stopped
    pid_alive "$RUNTIME_DIR/pids/vllm.pid" && vllm_status=running
    pid_alive "$RUNTIME_DIR/pids/gateway.pid" && gateway_status=running
    mineru_status=stopped
    pid_alive "$RUNTIME_DIR/pids/mineru-api.pid" && mineru_status=running
    echo "vllm=$vllm_status gateway=$gateway_status mineru=$mineru_status"
    if [[ "$gateway_status" == running ]]; then
      curl --noproxy '*' -fsS "http://127.0.0.1:$GATEWAY_PORT/health" || true
    elif [[ "$mineru_status" == running ]]; then
      curl --noproxy '*' -fsS "http://127.0.0.1:$MINERU_PORT/health" || true
    fi
    echo
    ;;
  *)
    usage
    exit 2
    ;;
esac
