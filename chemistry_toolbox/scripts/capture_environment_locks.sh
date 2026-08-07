#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOLBOX_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
PROJECT_ROOT="$(cd "${TOOLBOX_ROOT}/.." && pwd)"
TARGET_ROOT="${RESEARCHCHEMBENCH_ENV_ROOT:-${PROJECT_ROOT}/.envs}"
ENVIRONMENT_ROOT="${TOOLBOX_ROOT}/environment"
MANAGER="${RCB_CONDA_MANAGER:-$(command -v mamba || command -v conda)}"

declare -A PREFIXES=(
  [general-modern-openmpi5]="general-modern-openmpi5"
  [molecular-simulation-openff]="molecular-simulation-openff"
  [reaction-kinetics]="kinetics-legacy"
  [equivariant-ml]="equivariant-ml"
  [periodic-mpich]="periodic-mpich"
  [catmap-yambo-openmpi4]="yambo-openmpi4"
  [gmx-mmpbsa]="gmx-mmpbsa"
)

selected=("$@")
if ((${#selected[@]} == 0)); then
  selected=("${!PREFIXES[@]}")
fi

for name in "${selected[@]}"; do
  [[ -n "${PREFIXES[${name}]:-}" ]] || {
    echo "Unknown environment: ${name}" >&2
    exit 2
  }
  prefix="${TARGET_ROOT}/${PREFIXES[${name}]}"
  [[ -x "${prefix}/bin/python" ]] || { echo "Missing environment: ${prefix}" >&2; exit 2; }
  lock_dir="${ENVIRONMENT_ROOT}/${name}"
  explicit="${lock_dir}/linux-64.explicit.txt"
  temporary="${explicit}.tmp"
  {
    printf '@EXPLICIT\n'
    "${MANAGER}" list -p "${prefix}" --explicit | grep -E '^https?://'
  } > "${temporary}"
  mv "${temporary}" "${explicit}"
  "${prefix}/bin/python" -m pip freeze \
    | sed "s#${PROJECT_ROOT}#\${PROJECT_ROOT}#g" \
    > "${lock_dir}/linux-64.pip-freeze.txt"
done

PROJECT_ROOT="${PROJECT_ROOT}" ENVIRONMENT_ROOT="${ENVIRONMENT_ROOT}" python3 - <<'PY'
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

root = Path(os.environ["ENVIRONMENT_ROOT"])
project = Path(os.environ["PROJECT_ROOT"])
files = []
for path in sorted(root.glob("*/linux-64.*.txt")):
    files.append(
        {
            "path": str(path.relative_to(project)),
            "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "line_count": len(path.read_text(encoding="utf-8").splitlines()),
        }
    )
payload = {
    "schema_version": 1,
    "generated_at": datetime.now(timezone.utc).isoformat(),
    "platform": "linux-64",
    "files": files,
}
(root / "lock-manifest.json").write_text(
    json.dumps(payload, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)
PY

echo "Captured ${#selected[@]} environment lock(s) under ${ENVIRONMENT_ROOT}."
