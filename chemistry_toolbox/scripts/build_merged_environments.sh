#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOLBOX_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
PROJECT_ROOT="$(cd "${TOOLBOX_ROOT}/.." && pwd)"
SPEC_ROOT="${TOOLBOX_ROOT}/environment/merged"
TARGET_ROOT="${RCB_MERGED_ENV_ROOT:-${PROJECT_ROOT}/.tool_envs_merged}"
MANAGER="${RCB_CONDA_MANAGER:-$(command -v mamba || command -v conda)}"

ALL_ENVIRONMENTS=(
  general-modern-openmpi5
  molecular-simulation-openff
  reaction-kinetics
  equivariant-ml
  periodic-mpich
  catmap-yambo-openmpi4
)

usage() {
  echo "Usage: $0 [--recreate] [--from-lock] [all|ENV ...]"
  echo "Target root: RCB_MERGED_ENV_ROOT (default: ${PROJECT_ROOT}/.tool_envs_merged)"
  echo "Conda manager: RCB_CONDA_MANAGER (default: mamba, then conda)"
  echo "Available environments: ${ALL_ENVIRONMENTS[*]}"
}

recreate=0
from_lock=0
selected=()
while (($#)); do
  case "$1" in
    --recreate) recreate=1 ;;
    --from-lock) from_lock=1 ;;
    -h|--help) usage; exit 0 ;;
    all) selected=("${ALL_ENVIRONMENTS[@]}") ;;
    *) selected+=("$1") ;;
  esac
  shift
done
if ((${#selected[@]} == 0)); then
  selected=("${ALL_ENVIRONMENTS[@]}")
fi

mkdir -p "${TARGET_ROOT}"
for name in "${selected[@]}"; do
  spec_dir="${SPEC_ROOT}/${name}"
  case "${name}" in
    reaction-kinetics) target_name="kinetics-legacy" ;;
    catmap-yambo-openmpi4) target_name="yambo-openmpi4" ;;
    *) target_name="${name}" ;;
  esac
  prefix="${TARGET_ROOT}/${target_name}"
  lock_file="${SPEC_ROOT}/locks/linux-64/${name}.explicit.txt"
  if [[ ! -f "${spec_dir}/environment.yml" ]]; then
    echo "Unknown merged environment: ${name}" >&2
    usage >&2
    exit 2
  fi
  if ((recreate)) && [[ -x "${prefix}/bin/python" ]]; then
    "${MANAGER}" env remove -y -p "${prefix}"
  fi
  if [[ ! -x "${prefix}/bin/python" ]]; then
    if ((from_lock)); then
      [[ -s "${lock_file}" ]] || { echo "Missing exact lock: ${lock_file}" >&2; exit 2; }
      "${MANAGER}" create -y -p "${prefix}" --file "${lock_file}"
    else
      "${MANAGER}" env create -y -p "${prefix}" -f "${spec_dir}/environment.yml"
    fi
  else
    if ((from_lock)); then
      echo "Exact-lock replay requires an absent prefix or --recreate: ${prefix}" >&2
      exit 2
    fi
    "${MANAGER}" env update -p "${prefix}" -f "${spec_dir}/environment.yml" --prune
  fi
  if [[ -s "${spec_dir}/requirements.txt" ]]; then
    PIP_CONFIG_FILE=/dev/null \
    PIP_INDEX_URL="${RCB_PIP_INDEX_URL:-http://nexus.sii.shaipower.online/repository/pypi/simple}" \
    PIP_TRUSTED_HOST="${RCB_PIP_TRUSTED_HOST:-nexus.sii.shaipower.online}" \
      "${prefix}/bin/python" -m pip install -r "${spec_dir}/requirements.txt"
  fi
  check_output="$(mktemp)"
  if ! "${prefix}/bin/python" -m pip check >"${check_output}" 2>&1; then
    case "${name}" in
      reaction-kinetics)
        remaining="$(grep -Ev '^(quantities 0\.12\.3|gprof2dot 2017\.9\.19|periodictable 1\.5\.2) is not supported on this platform$' "${check_output}" || true)"
        ;;
      catmap-yambo-openmpi4)
        remaining="$(grep -Ev '^ase 3\.17\.0 is not supported on this platform$' "${check_output}" || true)"
        ;;
      *) remaining="$(cat "${check_output}")" ;;
    esac
    if [[ -n "${remaining}" ]]; then
      cat "${check_output}" >&2
      rm -f "${check_output}"
      exit 1
    fi
  fi
  cat "${check_output}"
  rm -f "${check_output}"
done

gnina_static="${PROJECT_ROOT}/.software_cache/gnina/1.3.3/gnina.cuda12.8.static"
gnina_link="${PROJECT_ROOT}/.software_cache/gnina/1.3.3/gnina"
if [[ -x "${gnina_static}" && ! -e "${gnina_link}" ]]; then
  ln -s "$(basename "${gnina_static}")" "${gnina_link}"
fi

echo "Built ${#selected[@]} consolidated environment(s) under ${TARGET_ROOT}."
