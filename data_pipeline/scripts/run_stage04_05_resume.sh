#!/usr/bin/env bash
set -Eeuo pipefail

pipeline_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
if [[ -f "${pipeline_root}/config.local.env" ]]; then
  set -a
  # shellcheck disable=SC1091
  source "${pipeline_root}/config.local.env"
  set +a
fi

# The configured model gateway is loopback-only; keep it off the cluster proxy.
export NO_PROXY="127.0.0.1,localhost,${NO_PROXY:-}"
export no_proxy="127.0.0.1,localhost,${no_proxy:-}"
python_bin="${pipeline_root}/.envs/researchchem-data-pipeline/bin/python"
if [[ ! -x "${python_bin}" ]]; then
  python_bin="$(command -v python3)"
fi

cd "${pipeline_root}"
export PATH="$(dirname "${python_bin}"):${PATH}"
export PYTHONPATH="${pipeline_root}${PYTHONPATH:+:${PYTHONPATH}}"
exec "${python_bin}" "${pipeline_root}/scripts/workflows/run_stage04_05_resume.py" "$@"
