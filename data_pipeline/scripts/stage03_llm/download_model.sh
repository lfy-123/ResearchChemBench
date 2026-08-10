#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
PIPELINE_ROOT=$(cd "$SCRIPT_DIR/../.." && pwd)
ENV_DIR="${RCB_PIPELINE_ENV_DIR:-$PIPELINE_ROOT/.envs/researchchem-data-pipeline}"
MODEL_ID="${STAGE03_LLM_MODEL_ID:-Qwen/Qwen3-30B-A3B-Instruct-2507}"
MODEL_DIR="${STAGE03_LLM_MODEL_DIR:-/mnt/shared-storage-user/liyuqiang/mdoels/Qwen3-30B-A3B-Instruct-2507}"

mkdir -p "$MODEL_DIR"
DOWNLOAD_BACKEND="${STAGE03_LLM_DOWNLOAD_BACKEND:-modelscope}"
if [[ "$DOWNLOAD_BACKEND" == "hf" ]]; then
  if [[ ! -x "$ENV_DIR/bin/hf" ]]; then
    echo "stage03 LLM environment is missing; run bootstrap_environment.sh first" >&2
    exit 1
  fi
  "$ENV_DIR/bin/hf" download "$MODEL_ID" \
    --local-dir "$MODEL_DIR" \
    --exclude '*.gguf' \
    --exclude '*.bin'
elif [[ "$DOWNLOAD_BACKEND" == "curl" || "$DOWNLOAD_BACKEND" == "modelscope" ]]; then
  API_FILE=$(mktemp)
  trap 'rm -f "$API_FILE"' EXIT
  curl -fsSL --retry 10 --retry-all-errors --connect-timeout 30 --max-time 300 \
    "https://huggingface.co/api/models/$MODEL_ID" -o "$API_FILE"
  REVISION=$(python3 - "$API_FILE" <<'PY'
import json, sys
print(json.load(open(sys.argv[1], encoding="utf-8"))["sha"])
PY
  )
  if [[ "$DOWNLOAD_BACKEND" == "modelscope" ]]; then
    REVISION="${STAGE03_LLM_MODEL_REVISION:-master}"
  fi
  mapfile -t FILES < <(python3 - "$API_FILE" <<'PY'
import json, sys
for item in json.load(open(sys.argv[1], encoding="utf-8")).get("siblings", []):
    name = str(item.get("rfilename") or "")
    if name and not name.endswith((".bin", ".gguf")) and name != ".gitattributes":
        print(name)
PY
  )
  download_one() {
    local name=$1
    local destination="$MODEL_DIR/$name"
    local partial="$destination.part"
    mkdir -p "$(dirname "$destination")"
    [[ -s "$destination" ]] && return 0
    if [[ "$DOWNLOAD_BACKEND" == "modelscope" ]]; then
      url="https://www.modelscope.cn/api/v1/models/$MODEL_ID/repo?Revision=$REVISION&FilePath=$name"
    else
      url="https://huggingface.co/$MODEL_ID/resolve/$REVISION/$name"
    fi
    curl_args=(
      -fL --retry 20 --retry-all-errors --retry-delay 5
      --connect-timeout 60 --speed-time 300 --speed-limit 1024
    )
    if [[ -s "$partial" ]]; then
      curl_args+=(-C -)
    fi
    curl "${curl_args[@]}" "$url" -o "$partial"
    mv "$partial" "$destination"
  }
  export -f download_one
  export MODEL_DIR MODEL_ID REVISION DOWNLOAD_BACKEND
  printf '%s\0' "${FILES[@]}" | xargs -0 -n1 -P "${STAGE03_LLM_DOWNLOAD_WORKERS:-4}" bash -c 'download_one "$1"' _
else
  echo "unsupported STAGE03_LLM_DOWNLOAD_BACKEND: $DOWNLOAD_BACKEND" >&2
  exit 2
fi

test -s "$MODEL_DIR/config.json"
test -s "$MODEL_DIR/tokenizer_config.json"
echo "model ready: $MODEL_DIR"
