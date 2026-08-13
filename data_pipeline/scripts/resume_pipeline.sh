#!/usr/bin/env bash
set -Eeuo pipefail

pipeline_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
for env_file in "${pipeline_root}/config.local.env" "${pipeline_root}/../config.local.env"; do
  if [[ -f "${env_file}" ]]; then
    set -a
    # shellcheck disable=SC1090
    source "${env_file}"
    set +a
  fi
done

python_bin="${pipeline_root}/.envs/researchchem-data-pipeline/bin/python"
if [[ ! -x "${python_bin}" ]]; then
  python_bin="$(command -v python3)"
fi

cd "${pipeline_root}"
export PYTHONPATH="${pipeline_root}${PYTHONPATH:+:${PYTHONPATH}}"
exec "${python_bin}" "${pipeline_root}/scripts/workflows/resume_pipeline.py" "$@"
