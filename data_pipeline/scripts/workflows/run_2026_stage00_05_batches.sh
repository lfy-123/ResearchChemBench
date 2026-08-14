#!/usr/bin/env bash
set -Eeuo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
pipeline_root="$(cd "${script_dir}/../.." && pwd)"
run_id="${RUN_ID:-stage00-05-published-since-20260101-$(date +%Y%m%dT%H%M%S)}"
run_root="${RUN_ROOT:-${pipeline_root}/runs/${run_id}}"
publication_date_from="${PUBLICATION_DATE_FROM:-2026-01-01}"
dataset="${DATASET:-kps-2026-05-07}"
batch_size="${BATCH_SIZE:-1000}"
publication_index="${run_root}/stage00_publication_candidates.jsonl"
mkdir -p "${run_root}/logs" "${run_root}/configs"

if [[ -f "${pipeline_root}/config.local.env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source "${pipeline_root}/config.local.env"
  set +a
fi

if [[ "${RCB_SETUP_PROXY:-1}" == "1" ]]; then
  # Publisher sites used by Stage01 are not reachable directly from every
  # development node. Keep this opt-out for environments with native access.
  # shellcheck disable=SC1090
  source <(curl -fsSL http://deploy.i.h.pjlab.org.cn/infra/scripts/setup_proxy.sh)
fi

# The user-managed model gateway is loopback-only and must never be sent
# through the publisher/network proxy configured above.
export NO_PROXY="127.0.0.1,localhost,${NO_PROXY:-}"
export no_proxy="127.0.0.1,localhost,${no_proxy:-}"

python_bin="${pipeline_root}/.envs/researchchem-data-pipeline/bin/python"
if [[ ! -x "${python_bin}" ]]; then
  echo "missing pipeline Python: ${python_bin}" >&2
  exit 1
fi

cd "${pipeline_root}"
export PATH="$(dirname "${python_bin}"):${PATH}"
export PYTHONPATH="${pipeline_root}${PYTHONPATH:+:${PYTHONPATH}}"

"${python_bin}" - "${publication_index}" "${dataset}" "${publication_date_from}" <<'PY'
import json
import sys
from pathlib import Path

from src.stages.stage00_remote_corpus import build_publication_index

index_path, dataset, threshold = sys.argv[1:]
summary = build_publication_index(
    Path(index_path),
    dataset=dataset,
    publication_date_from=threshold,
    credentials="/mnt/shared-storage-user/liyuqiang/benchmark/pipline_demo/pdfs/xinghe.txt",
)
print(json.dumps(summary, ensure_ascii=False), flush=True)
PY

total="$("${python_bin}" - "${publication_index}.summary.json" <<'PY'
import json
import sys
print(int(json.load(open(sys.argv[1], encoding="utf-8"))["available_pdfs"]))
PY
)"
if (( total < 1 )); then
  echo "no remotely available papers meet publication_date >= ${publication_date_from}" >&2
  exit 1
fi

cat >"${run_root}/launch_manifest.json" <<EOF
{
  "run_id": "${run_id}",
  "run_root": "${run_root}",
  "dataset": "${dataset}",
  "publication_date_from": "${publication_date_from}",
  "total": ${total},
  "batch_size": ${batch_size},
  "mineru_sandbox_count": 32,
  "mineru_sandbox_cpu": 16,
  "mineru_sandbox_memory": "32Gi"
}
EOF

batch_count=$(( (total + batch_size - 1) / batch_size ))
config_count="$(find "${run_root}/configs" -maxdepth 1 -type f -name 'batch-*.json' 2>/dev/null | wc -l)"
if [[ "${RCB_REGENERATE_CONFIGS:-0}" == "1" || "${config_count}" == "0" ]]; then
  bash "${pipeline_root}/scripts/workflows/run_stage00_05_api_batches.sh" \
    --run-root "${run_root}" \
    --dataset "${dataset}" \
    --publication-date-from "${publication_date_from}" \
    --publication-index-path "${publication_index}" \
    --total "${total}" \
    --batch-size "${batch_size}" \
    --stop-after stage05 \
    --microbatch-size 10 \
    --microbatch-concurrency 32 \
    --stage02-workers 16 \
    --stage03-workers 16 \
    --stage04-microbatch-concurrency 8 \
    --stage04-api-concurrency 32 \
    --stage05-workers 16 \
    --sandbox-cpu 64 \
    --sandbox-memory 128Gi \
    --sandbox-cleanup stop \
    --sandbox-startup-timeout-seconds 14400 \
    --mineru-sandbox-count 32 \
    --mineru-sandbox-cpu 16 \
    --mineru-sandbox-memory 32Gi \
    --mineru-sandbox-startup-concurrency 32 \
    --prepare-only \
    "$@"
elif (( config_count != batch_count )); then
  echo "refusing to resume with a partial config set: ${config_count}/${batch_count}" >&2
  echo "repair the config set or set RCB_REGENERATE_CONFIGS=1 explicitly" >&2
  exit 1
else
  echo "reusing ${config_count} frozen batch configs under ${run_root}" >&2
fi

exec bash "${pipeline_root}/scripts/resume_pipeline.sh" \
  --run-root "${run_root}" \
  --total "${total}" \
  --batch-size "${batch_size}" \
  --start-stage stage00 \
  --stop-stage stage05 \
  --resume-config current
