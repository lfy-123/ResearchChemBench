#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
PIPELINE_ROOT=$(cd "$SCRIPT_DIR/../.." && pwd)
DEFAULT_STATE="$PIPELINE_ROOT/.stage03_llm_worker.local.json"
SSH_SUFFIX=".liyuqiang+root.ailab-ai4chem.pod@h.pjlab.org.cn"
GATEWAY_HOST="h.pjlab.org.cn"
NAMESPACE="ailab-ai4chem"
WORKSPACE_USER="liyuqiang"

usage() {
  cat <<'EOF'
Usage:
  manage_rlaunch_worker.sh start [options]
  manage_rlaunch_worker.sh start-screening [--state <path>]
  manage_rlaunch_worker.sh recover-screening [--state <path>]
  manage_rlaunch_worker.sh release-screening [--state <path>]
  manage_rlaunch_worker.sh start-mineru [options]
  manage_rlaunch_worker.sh status [--state <path>]
  manage_rlaunch_worker.sh stop [--state <path>]

Start options:
  --state <path>          Local state file.
  --cpu <n>               Default: 32
  --memory <MiB>          Default: 160000 (about 153 GiB)
  --charged-group <name>  Default: ai4chem_gpu
  --positive-tag <tag>    Optional scheduler positive tag.
  --image <image>         Optional rlaunch image; uses the cluster default when omitted.
  --existing-worker <ssh> Reuse an already running worker and never stop that worker.
  --skip-bootstrap        Reuse the unified data-pipeline environment.
  --skip-download         Require an existing model directory.
  --mineru-env <path>     Unified data-pipeline environment.
  --mineru-config <path>  Shared MinerU model configuration JSON.
  --mineru-concurrency N  Maximum requests in the persistent MinerU API.
EOF
}

action=${1:-}
[[ -n "$action" ]] || { usage >&2; exit 2; }
shift
STATE="$DEFAULT_STATE"
CPU=32
MEMORY=160000
CHARGED_GROUP=ai4chem_gpu
POSITIVE_TAG=""
IMAGE=""
SKIP_BOOTSTRAP=0
SKIP_DOWNLOAD=0
MINERU_ENV="$PIPELINE_ROOT/.envs/researchchem-data-pipeline"
MINERU_CONFIG="$PIPELINE_ROOT/.model_cache/mineru/mineru.json"
MINERU_CONCURRENCY=8
EXISTING_WORKER=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    --state) STATE=$2; shift 2 ;;
    --cpu) CPU=$2; shift 2 ;;
    --memory) MEMORY=$2; shift 2 ;;
    --charged-group) CHARGED_GROUP=$2; shift 2 ;;
    --positive-tag) POSITIVE_TAG=$2; shift 2 ;;
    --image) IMAGE=$2; shift 2 ;;
    --existing-worker) EXISTING_WORKER=$2; shift 2 ;;
    --skip-bootstrap) SKIP_BOOTSTRAP=1; shift ;;
    --skip-download) SKIP_DOWNLOAD=1; shift ;;
    --mineru-env) MINERU_ENV=$2; shift 2 ;;
    --mineru-config) MINERU_CONFIG=$2; shift 2 ;;
    --mineru-concurrency) MINERU_CONCURRENCY=$2; shift 2 ;;
    -h|--help) usage; exit 0 ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
done

read_state() {
  python3 - "$STATE" "$1" <<'PY'
import json, sys
print(json.load(open(sys.argv[1], encoding="utf-8")).get(sys.argv[2], ""))
PY
}

write_state() {
  python3 - "$STATE" "$@" <<'PY'
import json, os, pathlib, sys
path = pathlib.Path(sys.argv[1])
keys = ["worker_token", "remote", "hostname", "base_url", "api_key", "model", "control_pid_file", "tunnel_pid_file", "worker_ownership"]
value = dict(zip(keys, sys.argv[2:], strict=True))
path.parent.mkdir(parents=True, exist_ok=True)
temporary = path.with_suffix(path.suffix + ".tmp")
temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
os.chmod(temporary, 0o600)
temporary.replace(path)
PY
}

update_state() {
  python3 - "$STATE" "$1" "$2" <<'PY'
import json, os, pathlib, sys
path = pathlib.Path(sys.argv[1])
value = json.loads(path.read_text(encoding="utf-8"))
value[sys.argv[2]] = sys.argv[3]
temporary = path.with_suffix(path.suffix + ".tmp")
temporary.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")
os.chmod(temporary, 0o600)
temporary.replace(path)
PY
}

wait_ssh() {
  local remote=$1
  local deadline=$((SECONDS + 1800))
  while (( SECONDS < deadline )); do
    ssh -o BatchMode=yes -o StrictHostKeyChecking=accept-new -o ConnectTimeout=8 \
      "$remote" hostname >/dev/null 2>&1 && return 0
    sleep 15
  done
  return 1
}

stop_rlaunch_process() {
  local worker=$1
  brainctl -n "$NAMESPACE" stop "process/$worker" >/dev/null 2>&1 || true
}

stop_tunnel() {
  local pid_file=$1
  local remote=${2:-}
  if [[ -s "$pid_file" ]]; then
    local control_socket
    control_socket=$(<"$pid_file")
    if [[ -n "$remote" && -S "$control_socket" ]]; then
      ssh -S "$control_socket" -O exit "$remote" >/dev/null 2>&1 || true
    fi
    [[ "$control_socket" == /tmp/rcb-s3-*.sock ]] && rm -f "$control_socket"
  fi
  rm -f "$pid_file"
}

start_tunnel() {
  local remote=$1
  local pid_file=$2
  local local_port=${3:-${STAGE03_LLM_LOCAL_GATEWAY_PORT:-18083}}
  local remote_port=${4:-18083}
  local health_path=${5:-/health}
  local state_id
  state_id=$(printf '%s' "$pid_file" | cksum | awk '{print $1}')
  local control_socket="/tmp/rcb-s3-${state_id}.sock"
  mkdir -p "$(dirname "$pid_file")"
  stop_tunnel "$pid_file" "$remote"
  rm -f "$control_socket"
  ssh -o BatchMode=yes -o ExitOnForwardFailure=yes \
    -o ServerAliveInterval=30 -o ServerAliveCountMax=3 \
    -M -S "$control_socket" -f -N \
    -L "127.0.0.1:${local_port}:127.0.0.1:${remote_port}" "$remote" \
    >"${pid_file}.log" 2>&1
  echo "$control_socket" >"$pid_file"
  local deadline=$((SECONDS + 30))
  while (( SECONDS < deadline )); do
    if curl --noproxy '*' -fsS "http://127.0.0.1:${local_port}${health_path}" >/dev/null 2>&1; then
      printf 'http://127.0.0.1:%s\n' "$local_port"
      return 0
    fi
    [[ -S "$control_socket" ]] || break
    sleep 1
  done
  cat "${pid_file}.log" >&2 || true
  stop_tunnel "$pid_file" "$remote"
  return 1
}

case "$action" in
  start)
    [[ ! -e "$STATE" ]] || { echo "state already exists: $STATE" >&2; exit 1; }
    tunnel_pid_file="${STATE}.ssh-tunnel.pid"
    api_key=$(python3 -c 'import secrets; print(secrets.token_hex(24))')
    if [[ -n "$EXISTING_WORKER" ]]; then
      remote="$EXISTING_WORKER"
      worker=${remote%%.*}
      control_pid_file=""
      worker_ownership=external
      echo "Reusing external worker: $remote"
    else
      control_pid_file="/tmp/researchchem-stage03-llm-control.pid"
      worker_ownership=managed
      command=(
        env -u http_proxy -u https_proxy -u HTTP_PROXY -u HTTPS_PROXY
        rlaunch -d --comment=researchchem-stage03-qwen
        --gpu=1 --cpu="$CPU" --memory="$MEMORY"
        --charged-group="$CHARGED_GROUP" --private-machine=group
        --worker-garbage-collection-time=24h
        --mount=gpfs://gpfs1/liyuqiang:/mnt/shared-storage-user/liyuqiang
        -w "$PIPELINE_ROOT"
      )
      [[ -z "$POSITIVE_TAG" ]] || command+=(--positive-tags="$POSITIVE_TAG")
      [[ -z "$IMAGE" ]] || command+=(--image="$IMAGE")
      command+=(-- bash -lc "echo \$\$ > $control_pid_file; exec sleep infinity")
      output=$("${command[@]}")
      printf '%s\n' "$output"
      worker=$(printf '%s\n' "$output" | grep -Eo 'ws-[A-Za-z0-9._@+:-]*worker[-A-Za-z0-9._@+:-]*' | head -n1)
      [[ -n "$worker" ]] || { echo "could not parse rlaunch worker" >&2; exit 1; }
      if [[ "$worker" == *@* ]]; then remote="$worker"; else remote="$worker$SSH_SUFFIX"; fi
    fi
    write_state "$worker" "$remote" "" "" "$api_key" \
      "qwen3-30b-a3b-instruct-2507" "$control_pid_file" "$tunnel_pid_file" "$worker_ownership"
    if [[ "$SKIP_BOOTSTRAP" == 0 ]]; then
      if ! bash -lc "source <(curl -sSL http://deploy.i.h.pjlab.org.cn/infra/scripts/setup_proxy.sh); bash $(printf '%q' "$SCRIPT_DIR/bootstrap_environment.sh")"; then
        [[ "$worker_ownership" != managed ]] || stop_rlaunch_process "$worker"
        echo "local Stage 03 environment preparation failed" >&2
        exit 1
      fi
    fi
    if [[ "$SKIP_DOWNLOAD" == 0 ]]; then
      if ! bash -lc "source <(curl -sSL http://deploy.i.h.pjlab.org.cn/infra/scripts/setup_proxy.sh); bash $(printf '%q' "$SCRIPT_DIR/download_model.sh")"; then
        [[ "$worker_ownership" != managed ]] || stop_rlaunch_process "$worker"
        echo "local Stage 03 model preparation failed" >&2
        exit 1
      fi
    fi
    if ! wait_ssh "$remote"; then
      echo "worker SSH did not become ready: $remote" >&2
      [[ "$worker_ownership" != managed ]] || stop_rlaunch_process "$worker"
      echo "worker connection failed; state retained for diagnostics: $STATE" >&2
      exit 1
    fi
    hostname=$(ssh "$remote" hostname | tr -d '[:space:]')
    write_state "$worker" "$remote" "$hostname" "" "$api_key" \
      "qwen3-30b-a3b-instruct-2507" "$control_pid_file" "$tunnel_pid_file" "$worker_ownership"
    remote_env="export STAGE03_LLM_API_KEY=$(printf '%q' "$api_key"); export no_proxy=localhost,127.0.0.1; export NO_PROXY=localhost,127.0.0.1;"
    ssh "$remote" "$remote_env bash $(printf '%q' "$SCRIPT_DIR/remote_manager.sh") start"
    if ! base_url=$(start_tunnel "$remote" "$tunnel_pid_file"); then
      [[ "$worker_ownership" != managed ]] || stop_rlaunch_process "$worker"
      echo "Stage 03 LLM SSH tunnel failed" >&2
      exit 1
    fi
    base_url="$base_url/v1"
    write_state "$worker" "$remote" "$hostname" "$base_url" "$api_key" \
      "qwen3-30b-a3b-instruct-2507" "$control_pid_file" "$tunnel_pid_file" "$worker_ownership"
    update_state service screening
    echo "state=$STATE"
    echo "base_url=$base_url"
    ;;
  status)
    test -s "$STATE"
    remote=$(read_state remote)
    api_key=$(read_state api_key)
    worker=$(read_state worker_token)
    hostname=$(read_state hostname)
    control_pid_file=$(read_state control_pid_file)
    tunnel_pid_file=$(read_state tunnel_pid_file)
    [[ -n "$tunnel_pid_file" ]] || tunnel_pid_file="${STATE}.ssh-tunnel.pid"
    service=$(read_state service)
    [[ -n "$service" ]] || service=screening
    ssh "$remote" "export STAGE03_LLM_API_KEY=$(printf '%q' "$api_key"); bash $(printf '%q' "$SCRIPT_DIR/remote_manager.sh") status"
    if [[ "$service" == mineru ]]; then
      base_url=$(start_tunnel "$remote" "$tunnel_pid_file" 18084 18084 /health)
      update_state base_url "$base_url"
      curl --noproxy '*' -fsS "$base_url/health"
    else
      base_url=$(start_tunnel "$remote" "$tunnel_pid_file" 18083 18083 /health)
      base_url="$base_url/v1"
      update_state base_url "$base_url"
      curl -fsS -H "Authorization: Bearer $api_key" "$base_url/models"
    fi
    echo
    ;;
  release-screening)
    test -s "$STATE"
    remote=$(read_state remote)
    tunnel_pid_file=$(read_state tunnel_pid_file)
    [[ -n "$tunnel_pid_file" ]] || tunnel_pid_file="${STATE}.ssh-tunnel.pid"
    stop_tunnel "$tunnel_pid_file" "$remote"
    ssh "$remote" "bash $(printf '%q' "$SCRIPT_DIR/remote_manager.sh") stop-screening"
    update_state service idle
    update_state base_url ""
    ;;
  start-screening)
    test -s "$STATE"
    remote=$(read_state remote)
    api_key=$(read_state api_key)
    tunnel_pid_file=$(read_state tunnel_pid_file)
    [[ -n "$tunnel_pid_file" ]] || tunnel_pid_file="${STATE}.ssh-tunnel.pid"
    stop_tunnel "$tunnel_pid_file" "$remote"
    remote_env="export STAGE03_LLM_API_KEY=$(printf '%q' "$api_key"); export no_proxy=localhost,127.0.0.1; export NO_PROXY=localhost,127.0.0.1;"
    ssh "$remote" "$remote_env bash $(printf '%q' "$SCRIPT_DIR/remote_manager.sh") start-screening"
    base_url=$(start_tunnel "$remote" "$tunnel_pid_file" 18083 18083 /health)
    base_url="$base_url/v1"
    update_state service screening
    update_state model qwen3-30b-a3b-instruct-2507
    update_state base_url "$base_url"
    echo "base_url=$base_url"
    ;;
  recover-screening)
    test -s "$STATE"
    remote=$(read_state remote)
    api_key=$(read_state api_key)
    tunnel_pid_file=$(read_state tunnel_pid_file)
    [[ -n "$tunnel_pid_file" ]] || tunnel_pid_file="${STATE}.ssh-tunnel.pid"
    remote_env="export STAGE03_LLM_API_KEY=$(printf '%q' "$api_key"); export no_proxy=localhost,127.0.0.1; export NO_PROXY=localhost,127.0.0.1;"
    if ! ssh "$remote" "curl --noproxy '*' -fsS http://127.0.0.1:18083/health >/dev/null"; then
      ssh "$remote" "$remote_env bash $(printf '%q' "$SCRIPT_DIR/remote_manager.sh") start-screening"
    fi
    base_url=$(start_tunnel "$remote" "$tunnel_pid_file" 18083 18083 /health)
    base_url="$base_url/v1"
    update_state service screening
    update_state model qwen3-30b-a3b-instruct-2507
    update_state base_url "$base_url"
    echo "base_url=$base_url"
    ;;
  start-mineru)
    test -s "$STATE"
    remote=$(read_state remote)
    tunnel_pid_file=$(read_state tunnel_pid_file)
    [[ -n "$tunnel_pid_file" ]] || tunnel_pid_file="${STATE}.ssh-tunnel.pid"
    stop_tunnel "$tunnel_pid_file" "$remote"
    remote_env="export STAGE04_MINERU_ENV_DIR=$(printf '%q' "$MINERU_ENV"); export MINERU_TOOLS_CONFIG_JSON=$(printf '%q' "$MINERU_CONFIG"); export MINERU_API_MAX_CONCURRENT_REQUESTS=$(printf '%q' "$MINERU_CONCURRENCY"); export MINERU_DEVICE_MODE=cuda; export MINERU_MODEL_SOURCE=local;"
    ssh "$remote" "$remote_env bash $(printf '%q' "$SCRIPT_DIR/remote_manager.sh") start-mineru"
    base_url=$(start_tunnel "$remote" "$tunnel_pid_file" 18084 18084 /health)
    update_state service mineru
    update_state model mineru
    update_state base_url "$base_url"
    echo "base_url=$base_url"
    ;;
  stop)
    if [[ ! -s "$STATE" ]]; then
      echo "no Stage 03 LLM worker state: $STATE"
      exit 0
    fi
    remote=$(read_state remote)
    api_key=$(read_state api_key)
    control_pid_file=$(read_state control_pid_file)
    tunnel_pid_file=$(read_state tunnel_pid_file)
    [[ -n "$tunnel_pid_file" ]] || tunnel_pid_file="${STATE}.ssh-tunnel.pid"
    worker=$(read_state worker_token)
    worker_ownership=$(read_state worker_ownership)
    [[ -n "$worker_ownership" ]] || worker_ownership=managed
    stop_tunnel "$tunnel_pid_file" "$remote"
    if ssh -o ConnectTimeout=8 "$remote" \
      "export STAGE03_LLM_API_KEY=$(printf '%q' "$api_key"); bash $(printf '%q' "$SCRIPT_DIR/remote_manager.sh") stop"
    then
      [[ "$worker_ownership" != managed ]] || stop_rlaunch_process "$worker"
      rm -f "$STATE"
      if [[ "$worker_ownership" == managed ]]; then
        echo "Stage 03 LLM rlaunch worker stopped"
      else
        echo "Stage 03 services stopped; external worker preserved: $remote"
      fi
    else
      [[ "$worker_ownership" != managed ]] || stop_rlaunch_process "$worker"
      rm -f "$STATE"
      if [[ "$worker_ownership" == managed ]]; then
        echo "Stage 03 LLM rlaunch worker stopped via brainctl; SSH cleanup was unavailable" >&2
      else
        echo "external worker preserved; remote service cleanup was unavailable: $remote" >&2
      fi
    fi
    ;;
  *)
    usage >&2
    exit 2
    ;;
esac
