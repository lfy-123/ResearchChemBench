#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TOOLBOX_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
PROJECT_ROOT="$(cd "${TOOLBOX_ROOT}/.." && pwd)"
TARGET_ROOT="${RESEARCHCHEMBENCH_ENV_ROOT:-${PROJECT_ROOT}/.envs}"
LOCK_ROOT="${TOOLBOX_ROOT}/environment/merged/locks/linux-64"
MANAGER="${RCB_CONDA_MANAGER:-$(command -v mamba || command -v conda)}"

declare -A PREFIXES=(
  [general-modern-openmpi5]="general-modern-openmpi5"
  [molecular-simulation-openff]="molecular-simulation-openff"
  [reaction-kinetics]="kinetics-legacy"
  [equivariant-ml]="equivariant-ml"
  [periodic-mpich]="periodic-mpich"
  [catmap-yambo-openmpi4]="yambo-openmpi4"
)

mkdir -p "${LOCK_ROOT}"
for name in "${!PREFIXES[@]}"; do
  prefix="${TARGET_ROOT}/${PREFIXES[${name}]}"
  [[ -x "${prefix}/bin/python" ]] || { echo "Missing merged environment: ${prefix}" >&2; exit 2; }
  explicit="${LOCK_ROOT}/${name}.explicit.txt"
  temporary="${explicit}.tmp"
  {
    printf '@EXPLICIT\n'
    "${MANAGER}" list -p "${prefix}" --explicit | grep -E '^https?://'
  } > "${temporary}"
  mv "${temporary}" "${explicit}"
  "${prefix}/bin/python" -m pip freeze > "${LOCK_ROOT}/${name}.pip-freeze.txt"
done

PROJECT_ROOT="${PROJECT_ROOT}" LOCK_ROOT="${LOCK_ROOT}" python3 - <<'PY'
import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path

root = Path(os.environ["LOCK_ROOT"])
project = Path(os.environ["PROJECT_ROOT"])
files = []
for path in sorted(root.glob("*.txt")):
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
(root / "manifest.json").write_text(
    json.dumps(payload, indent=2, sort_keys=True) + "\n",
    encoding="utf-8",
)
PY

echo "Captured ${#PREFIXES[@]} merged environment locks under ${LOCK_ROOT}."
