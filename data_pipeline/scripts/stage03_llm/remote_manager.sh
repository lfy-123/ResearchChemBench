#!/usr/bin/env bash
set -euo pipefail

usage() {
  echo "Usage: remote_manager.sh <start|stop|status>" >&2
}

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
PIPELINE_ROOT=$(cd "$SCRIPT_DIR/../.." && pwd)
RUNTIME_DIR="${STAGE03_LLM_RUNTIME_DIR:-$PIPELINE_ROOT/.stage03_llm_runtime}"
ENV_DIR="${STAGE03_LLM_ENV_DIR:-$PIPELINE_ROOT/.envs/stage03-qwen3-30b-a3b}"
VLLM_PORT="${STAGE03_LLM_VLLM_PORT:-18082}"
GATEWAY_PORT="${STAGE03_LLM_GATEWAY_PORT:-18083}"

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
  local deadline=$((SECONDS + timeout))
  while (( SECONDS < deadline )); do
    if curl --noproxy '*' -fsS "$url" >/dev/null 2>&1; then
      return 0
    fi
    sleep 5
  done
  return 1
}

command=${1:-}
case "$command" in
  start)
    test -x "$ENV_DIR/bin/python"
    test -s "${STAGE03_LLM_MODEL_DIR:-/mnt/shared-storage-user/liyuqiang/mdoels/Qwen3-30B-A3B-Instruct-2507}/config.json"
    mkdir -p "$RUNTIME_DIR/logs" "$RUNTIME_DIR/pids"
    "$0" stop >/dev/null 2>&1 || true
    export no_proxy="localhost,127.0.0.1,${no_proxy:-}"
    export NO_PROXY="$no_proxy"
    nohup "$ENV_DIR/bin/python" "$SCRIPT_DIR/vllm_entry.py" \
      >"$RUNTIME_DIR/logs/vllm.log" 2>&1 &
    echo $! >"$RUNTIME_DIR/pids/vllm.pid"
    if ! wait_http "http://127.0.0.1:$VLLM_PORT/v1/models" "${STAGE03_LLM_STARTUP_TIMEOUT:-1800}"; then
      tail -n 200 "$RUNTIME_DIR/logs/vllm.log" >&2 || true
      "$0" stop >/dev/null 2>&1 || true
      exit 1
    fi
    nohup "$ENV_DIR/bin/python" "$SCRIPT_DIR/fastapi_gateway.py" \
      >"$RUNTIME_DIR/logs/gateway.log" 2>&1 &
    echo $! >"$RUNTIME_DIR/pids/gateway.pid"
    if ! wait_http "http://127.0.0.1:$GATEWAY_PORT/health" 120; then
      tail -n 100 "$RUNTIME_DIR/logs/gateway.log" >&2 || true
      "$0" stop >/dev/null 2>&1 || true
      exit 1
    fi
    "$0" status
    ;;
  stop)
    stop_pid "$RUNTIME_DIR/pids/gateway.pid"
    stop_pid "$RUNTIME_DIR/pids/vllm.pid"
    echo "stage03 LLM services stopped"
    ;;
  status)
    vllm_status=stopped
    gateway_status=stopped
    pid_alive "$RUNTIME_DIR/pids/vllm.pid" && vllm_status=running
    pid_alive "$RUNTIME_DIR/pids/gateway.pid" && gateway_status=running
    echo "vllm=$vllm_status gateway=$gateway_status"
    curl --noproxy '*' -fsS "http://127.0.0.1:$GATEWAY_PORT/health" || true
    echo
    ;;
  *)
    usage
    exit 2
    ;;
esac
