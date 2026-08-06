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
  manage_rlaunch_worker.sh status [--state <path>]
  manage_rlaunch_worker.sh stop [--state <path>]

Start options:
  --state <path>          Local state file.
  --cpu <n>               Default: 16
  --memory <MiB>          Default: 196000
  --charged-group <name>  Default: ai4chem_gpu
  --positive-tag <tag>    Default: h200
  --image <image>         rlaunch image; defaults to the ai4chem GPU image.
  --skip-bootstrap        Reuse the existing Stage 03 LLM environment.
  --skip-download         Require an existing model directory.
EOF
}

action=${1:-}
[[ -n "$action" ]] || { usage >&2; exit 2; }
shift
STATE="$DEFAULT_STATE"
CPU=16
MEMORY=196000
CHARGED_GROUP=ai4chem_gpu
POSITIVE_TAG=h200
IMAGE="registry.h.pjlab.org.cn/ailab-ai4chem-ai4chem_gpu/chemllm-workspace:test1-20260425150803"
SKIP_BOOTSTRAP=0
SKIP_DOWNLOAD=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --state) STATE=$2; shift 2 ;;
    --cpu) CPU=$2; shift 2 ;;
    --memory) MEMORY=$2; shift 2 ;;
    --charged-group) CHARGED_GROUP=$2; shift 2 ;;
    --positive-tag) POSITIVE_TAG=$2; shift 2 ;;
    --image) IMAGE=$2; shift 2 ;;
    --skip-bootstrap) SKIP_BOOTSTRAP=1; shift ;;
    --skip-download) SKIP_DOWNLOAD=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "unknown argument: $1" >&2; exit 2 ;;
  esac
done

read_state() {
  python3 - "$STATE" "$1" <<'PY'
import json, sys
print(json.load(open(sys.argv[1], encoding="utf-8"))[sys.argv[2]])
PY
}

write_state() {
  python3 - "$STATE" "$@" <<'PY'
import json, os, pathlib, sys
path = pathlib.Path(sys.argv[1])
keys = ["worker_token", "remote", "hostname", "base_url", "api_key", "model", "control_pid_file"]
value = dict(zip(keys, sys.argv[2:], strict=True))
path.parent.mkdir(parents=True, exist_ok=True)
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

case "$action" in
  start)
    [[ ! -e "$STATE" ]] || { echo "state already exists: $STATE" >&2; exit 1; }
    control_pid_file="/tmp/researchchem-stage03-llm-control.pid"
    api_key=$(python3 -c 'import secrets; print(secrets.token_hex(24))')
    command=(
      env -u http_proxy -u https_proxy -u HTTP_PROXY -u HTTPS_PROXY
      rlaunch -d --comment=researchchem-stage03-qwen
      --gpu=1 --cpu="$CPU" --memory="$MEMORY"
      --charged-group="$CHARGED_GROUP" --private-machine=group
      --worker-garbage-collection-time=6h
      --positive-tags="$POSITIVE_TAG"
      --mount=gpfs://gpfs1/liyuqiang:/mnt/shared-storage-user/liyuqiang
      -w "$PIPELINE_ROOT"
    )
    [[ -z "$IMAGE" ]] || command+=(--image="$IMAGE")
    command+=(-- bash -lc "echo \$\$ > $control_pid_file; exec sleep infinity")
    output=$("${command[@]}")
    printf '%s\n' "$output"
    worker=$(printf '%s\n' "$output" | grep -Eo 'ws-[A-Za-z0-9._@+:-]*worker[-A-Za-z0-9._@+:-]*' | head -n1)
    [[ -n "$worker" ]] || { echo "could not parse rlaunch worker" >&2; exit 1; }
    if [[ "$worker" == *@* ]]; then remote="$worker"; else remote="$worker$SSH_SUFFIX"; fi
    write_state "$worker" "$remote" "" "" "$api_key" \
      "qwen3-30b-a3b-instruct-2507" "$control_pid_file"
    if ! wait_ssh "$remote"; then
      echo "worker SSH did not become ready: $remote" >&2
      echo "state retained for a later cleanup attempt: $STATE" >&2
      exit 1
    fi
    hostname=$(ssh "$remote" hostname | tr -d '[:space:]')
    base_url="https://$GATEWAY_HOST/kapi/workspace.kubebrain.io/$NAMESPACE/$hostname.$WORKSPACE_USER/18083/v1"
    write_state "$worker" "$remote" "$hostname" "$base_url" "$api_key" \
      "qwen3-30b-a3b-instruct-2507" "$control_pid_file"
    remote_env="export STAGE03_LLM_API_KEY=$(printf '%q' "$api_key"); export no_proxy=localhost,127.0.0.1; export NO_PROXY=localhost,127.0.0.1;"
    if [[ "$SKIP_BOOTSTRAP" == 0 ]]; then
      ssh "$remote" "$remote_env bash $(printf '%q' "$SCRIPT_DIR/bootstrap_environment.sh")"
    fi
    if [[ "$SKIP_DOWNLOAD" == 0 ]]; then
      ssh "$remote" "source <(curl -sSL http://deploy.i.h.pjlab.org.cn/infra/scripts/setup_proxy.sh); $remote_env bash $(printf '%q' "$SCRIPT_DIR/download_model.sh")"
    fi
    ssh "$remote" "$remote_env bash $(printf '%q' "$SCRIPT_DIR/remote_manager.sh") start"
    echo "state=$STATE"
    echo "base_url=$base_url"
    ;;
  status)
    test -s "$STATE"
    remote=$(read_state remote)
    api_key=$(read_state api_key)
    base_url=$(read_state base_url)
    ssh "$remote" "export STAGE03_LLM_API_KEY=$(printf '%q' "$api_key"); bash $(printf '%q' "$SCRIPT_DIR/remote_manager.sh") status"
    curl -fsS -H "Authorization: Bearer $api_key" "$base_url/models"
    echo
    ;;
  stop)
    if [[ ! -s "$STATE" ]]; then
      echo "no Stage 03 LLM worker state: $STATE"
      exit 0
    fi
    remote=$(read_state remote)
    api_key=$(read_state api_key)
    control_pid_file=$(read_state control_pid_file)
    if ssh -o ConnectTimeout=8 "$remote" \
      "export STAGE03_LLM_API_KEY=$(printf '%q' "$api_key"); bash $(printf '%q' "$SCRIPT_DIR/remote_manager.sh") stop; test -s $(printf '%q' "$control_pid_file") && kill -TERM \$(cat $(printf '%q' "$control_pid_file"))"
    then
      rm -f "$STATE"
      echo "Stage 03 LLM rlaunch worker stopped"
    else
      echo "worker cleanup could not connect; state retained: $STATE" >&2
      exit 1
    fi
    ;;
  *)
    usage >&2
    exit 2
    ;;
esac
