#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

ENV_ROOT="${RESEARCHCHEMBENCH_ENV_ROOT:-$ROOT_DIR/.envs}"
FRAMEWORK_ENV="${RESEARCHCHEMBENCH_FRAMEWORK_ENV:-$ENV_ROOT/researchchembench}"
PYTHON="$FRAMEWORK_ENV/bin/python"

count=4
cpu_cores=20
available_cpu_cores=""
memory="48Gi"
reserve_memory_mb=4096
available_memory_mb=""
lifecycle_minutes=1440
instance_capacity=""
prewarm_size=0
ratio=1
name_prefix="researchchembench-sandbox"
environment_name=""
environment_id=""
description="ResearchChemBench distributed OpenSandbox workers"
image="registry.h.pjlab.org.cn/ailab-ai4chem-ai4chem_cpu/base:python312-20260627215752"
base_url="https://h.pjlab.org.cn/brainbox"
project="ailab-ai4chem"
api_key_env="RCB_SANDBOX_API_KEY"
project_root="$ROOT_DIR"
mount_path="/mnt/shared-storage-user/liyuqiang"
host_path="gpfs://gpfs1/liyuqiang"
shared_mount_read_only=true
remote_job_root="/tmp/researchchembench/jobs"
command_port=44772
rpc_port=44773
output="$ROOT_DIR/.sandboxes.local.yaml"
inventory="$ROOT_DIR/.sandbox_inventory.local.json"
replace=0
generate_only=0

usage() {
  cat <<'EOF'
Create a ResearchChemBench OpenSandbox pool and generate its local inventory.

Usage:
  bash scripts/create_sandbox_pool.sh [OPTIONS]

Main options:
  --count N                     Number of Sandbox instances. Default: 4.
  --cpu N                       CPU cores provisioned per instance. Default: 20.
  --available-cpu N             CPU cores exposed to the scheduler per instance.
                                Default: same as --cpu.
  --memory SIZE                 Memory provisioned per instance, for example 48Gi.
                                Default: 48Gi.
  --reserve-memory-mb N         Memory kept for RPC/system processes. Default: 4096.
  --available-memory-mb N       Scheduler memory per instance. Overrides the
                                value derived from --memory and --reserve-memory-mb.
  --lifecycle-minutes N         Instance lifecycle. Default: 1440.
  --instance-capacity N         Environment instance capacity. Default: --count.
  --prewarm-size N              Environment prewarm size. Default: 0.
  --ratio N                     Environment ratio. Default: 1.

Naming and environment options:
  --name-prefix NAME            Worker display-name prefix.
                                Default: researchchembench-sandbox.
  --environment-name NAME       Environment display name.
                                Default: NAME_PREFIX-CPUcpu.
  --environment-id ID           Reuse an existing Environment instead of creating one.
  --description TEXT            Environment description.
  --image URI                   Sandbox image URI.
  --base-url URL                OpenSandbox API base URL.
  --project NAME                OpenSandbox project. Default: ailab-ai4chem.
  --api-key-env NAME            Environment variable containing the API key.
                                Default: RCB_SANDBOX_API_KEY.

Storage and ports:
  --project-root PATH           ResearchChemBench project root visible in Sandbox.
  --mount-path PATH             Shared-storage mount path inside Sandbox.
  --host-path URI               Shared-storage host URI.
  --shared-mount-read-only BOOL true or false. Default: true. The current platform
                                rejects false unless allowWritableGPFS is enabled.
  --remote-job-root PATH        Writable Sandbox-local job root.
  --command-port N              OpenSandbox command port. Default: 44772.
  --rpc-port N                  ResearchChemBench RPC port. Default: 44773.

Output and safety:
  --output PATH                 Source YAML. Default: .sandboxes.local.yaml.
  --inventory PATH              Generated inventory. Default: .sandbox_inventory.local.json.
  --replace                     Replace an existing source YAML after creating a backup.
                                Existing remote environments/instances are not stopped.
  --generate-only               Only write the source YAML; do not call the API.
  -h, --help                    Show this help.

Examples:
  bash scripts/create_sandbox_pool.sh --replace

  bash scripts/create_sandbox_pool.sh \
    --count 4 --cpu 20 --memory 48Gi \
    --available-memory-mb 45000 --lifecycle-minutes 1440 --replace

  bash scripts/create_sandbox_pool.sh \
    --count 2 --cpu 32 --memory 96Gi \
    --name-prefix rcb-large --output .sandboxes.large.yaml \
    --inventory .sandbox_inventory.large.json
EOF
}

require_value() {
  local option="$1"
  local value="${2:-}"
  if [[ -z "$value" ]]; then
    echo "Error: $option requires a value." >&2
    exit 2
  fi
}

require_positive_integer() {
  local option="$1"
  local value="$2"
  if [[ ! "$value" =~ ^[1-9][0-9]*$ ]]; then
    echo "Error: $option must be a positive integer; received '$value'." >&2
    exit 2
  fi
}

require_nonnegative_integer() {
  local option="$1"
  local value="$2"
  if [[ ! "$value" =~ ^[0-9]+$ ]]; then
    echo "Error: $option must be a non-negative integer; received '$value'." >&2
    exit 2
  fi
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --count) require_value "$1" "${2:-}"; count="$2"; shift 2 ;;
    --cpu) require_value "$1" "${2:-}"; cpu_cores="$2"; shift 2 ;;
    --available-cpu) require_value "$1" "${2:-}"; available_cpu_cores="$2"; shift 2 ;;
    --memory) require_value "$1" "${2:-}"; memory="$2"; shift 2 ;;
    --reserve-memory-mb) require_value "$1" "${2:-}"; reserve_memory_mb="$2"; shift 2 ;;
    --available-memory-mb) require_value "$1" "${2:-}"; available_memory_mb="$2"; shift 2 ;;
    --lifecycle-minutes) require_value "$1" "${2:-}"; lifecycle_minutes="$2"; shift 2 ;;
    --instance-capacity) require_value "$1" "${2:-}"; instance_capacity="$2"; shift 2 ;;
    --prewarm-size) require_value "$1" "${2:-}"; prewarm_size="$2"; shift 2 ;;
    --ratio) require_value "$1" "${2:-}"; ratio="$2"; shift 2 ;;
    --name-prefix) require_value "$1" "${2:-}"; name_prefix="$2"; shift 2 ;;
    --environment-name) require_value "$1" "${2:-}"; environment_name="$2"; shift 2 ;;
    --environment-id) require_value "$1" "${2:-}"; environment_id="$2"; shift 2 ;;
    --description) require_value "$1" "${2:-}"; description="$2"; shift 2 ;;
    --image) require_value "$1" "${2:-}"; image="$2"; shift 2 ;;
    --base-url) require_value "$1" "${2:-}"; base_url="$2"; shift 2 ;;
    --project) require_value "$1" "${2:-}"; project="$2"; shift 2 ;;
    --api-key-env) require_value "$1" "${2:-}"; api_key_env="$2"; shift 2 ;;
    --project-root) require_value "$1" "${2:-}"; project_root="$2"; shift 2 ;;
    --mount-path) require_value "$1" "${2:-}"; mount_path="$2"; shift 2 ;;
    --host-path) require_value "$1" "${2:-}"; host_path="$2"; shift 2 ;;
    --shared-mount-read-only) require_value "$1" "${2:-}"; shared_mount_read_only="$2"; shift 2 ;;
    --remote-job-root) require_value "$1" "${2:-}"; remote_job_root="$2"; shift 2 ;;
    --command-port) require_value "$1" "${2:-}"; command_port="$2"; shift 2 ;;
    --rpc-port) require_value "$1" "${2:-}"; rpc_port="$2"; shift 2 ;;
    --output) require_value "$1" "${2:-}"; output="$2"; shift 2 ;;
    --inventory) require_value "$1" "${2:-}"; inventory="$2"; shift 2 ;;
    --replace) replace=1; shift ;;
    --generate-only) generate_only=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Error: unknown option '$1'." >&2; usage >&2; exit 2 ;;
  esac
done

if [[ ! -x "$PYTHON" ]]; then
  echo "Error: ResearchChemBench framework Python is missing: $PYTHON" >&2
  exit 2
fi

require_positive_integer --count "$count"
require_positive_integer --cpu "$cpu_cores"
require_nonnegative_integer --reserve-memory-mb "$reserve_memory_mb"
require_positive_integer --lifecycle-minutes "$lifecycle_minutes"
require_nonnegative_integer --prewarm-size "$prewarm_size"
require_positive_integer --ratio "$ratio"
require_positive_integer --command-port "$command_port"
require_positive_integer --rpc-port "$rpc_port"

available_cpu_cores="${available_cpu_cores:-$cpu_cores}"
instance_capacity="${instance_capacity:-$count}"
environment_name="${environment_name:-${name_prefix}-${cpu_cores}cpu}"
require_positive_integer --available-cpu "$available_cpu_cores"
require_positive_integer --instance-capacity "$instance_capacity"
if [[ -n "$available_memory_mb" ]]; then
  require_positive_integer --available-memory-mb "$available_memory_mb"
fi
if (( available_cpu_cores > cpu_cores )); then
  echo "Error: --available-cpu cannot exceed --cpu." >&2
  exit 2
fi
if (( instance_capacity < count )); then
  echo "Error: --instance-capacity cannot be smaller than --count." >&2
  exit 2
fi
if (( prewarm_size > instance_capacity )); then
  echo "Error: --prewarm-size cannot exceed --instance-capacity." >&2
  exit 2
fi
if [[ "$shared_mount_read_only" != "true" && "$shared_mount_read_only" != "false" ]]; then
  echo "Error: --shared-mount-read-only must be true or false." >&2
  exit 2
fi

if [[ "$output" != /* ]]; then
  output="$ROOT_DIR/$output"
fi
if [[ "$inventory" != /* ]]; then
  inventory="$ROOT_DIR/$inventory"
fi

if [[ -e "$output" && "$replace" -ne 1 ]]; then
  echo "Error: source configuration already exists: $output" >&2
  echo "Use --replace to back it up and create a new pool definition." >&2
  exit 2
fi

backup_stamp="$(date -u +%Y%m%d_%H%M%S)"
if [[ -e "$output" ]]; then
  output_backup="${output}.backup.${backup_stamp}"
  cp -p "$output" "$output_backup"
  echo "Backed up source configuration to: $output_backup"
fi
if [[ -e "$inventory" && "$generate_only" -ne 1 ]]; then
  inventory_backup="${inventory}.backup.${backup_stamp}"
  cp -p "$inventory" "$inventory_backup"
  echo "Backed up inventory to: $inventory_backup"
fi

mkdir -p "$(dirname "$output")" "$(dirname "$inventory")"

"$PYTHON" - \
  "$output" "$count" "$cpu_cores" "$available_cpu_cores" "$memory" \
  "$reserve_memory_mb" "$available_memory_mb" "$lifecycle_minutes" \
  "$instance_capacity" "$prewarm_size" "$ratio" "$name_prefix" \
  "$environment_name" "$environment_id" "$description" "$image" \
  "$base_url" "$project" "$api_key_env" "$project_root" "$mount_path" \
  "$host_path" "$shared_mount_read_only" "$remote_job_root" \
  "$command_port" "$rpc_port" <<'PY'
from __future__ import annotations

import os
import re
import sys
from pathlib import Path

import yaml

(
    output,
    count,
    cpu_cores,
    available_cpu_cores,
    memory,
    reserve_memory_mb,
    available_memory_mb,
    lifecycle_minutes,
    instance_capacity,
    prewarm_size,
    ratio,
    name_prefix,
    environment_name,
    environment_id,
    description,
    image,
    base_url,
    project,
    api_key_env,
    project_root,
    mount_path,
    host_path,
    shared_mount_read_only,
    remote_job_root,
    command_port,
    rpc_port,
) = sys.argv[1:]


def memory_to_mib(value: str) -> int:
    match = re.fullmatch(r"([1-9][0-9]*)(Mi|Gi|Ti)", value)
    if not match:
        raise SystemExit(
            f"Error: --memory must use Mi, Gi, or Ti units, for example 49152Mi or 48Gi; received {value!r}."
        )
    amount = int(match.group(1))
    multiplier = {"Mi": 1, "Gi": 1024, "Ti": 1024 * 1024}[match.group(2)]
    return amount * multiplier


count_value = int(count)
cpu_value = int(cpu_cores)
available_cpu_value = int(available_cpu_cores)
memory_mib = memory_to_mib(memory)
reserve_mib = int(reserve_memory_mb)
if available_memory_mb:
    scheduler_memory_mib = int(available_memory_mb)
else:
    scheduler_memory_mib = memory_mib - reserve_mib
if scheduler_memory_mib <= 0:
    raise SystemExit(
        "Error: derived available memory is not positive; reduce --reserve-memory-mb or set --available-memory-mb."
    )
if scheduler_memory_mib > memory_mib:
    raise SystemExit("Error: --available-memory-mb cannot exceed provisioned --memory.")

read_only = shared_mount_read_only == "true"
payload = {
    "schema_version": 1,
    "transport": "sandbox",
    "api": {
        "base_url": base_url.rstrip("/"),
        "project": project,
        "api_key_env": api_key_env,
    },
    "project": {
        "root": str(Path(project_root).expanduser().resolve()),
        "shared_mount_root": mount_path,
        "shared_mount_read_only": read_only,
        "remote_job_root": remote_job_root,
    },
    "environment": {
        "environment_id": environment_id or None,
        "create_if_missing": not bool(environment_id),
        "name": environment_name,
        "description": description,
        "image": image,
        "entrypoint": ["sleep", "inf"],
        "resources": {"cpu": str(cpu_value), "memory": memory},
        "ports": {"command": int(command_port), "rpc": int(rpc_port)},
        "default_lifecycle_minutes": int(lifecycle_minutes),
        "instance_capacity": int(instance_capacity),
        "prewarm_size": int(prewarm_size),
        "ratio": int(ratio),
        "volumes": [
            {
                "name": "storage-vol-1",
                "mount_path": mount_path,
                "read_only": read_only,
                "host_path": host_path,
            }
        ],
    },
    "scheduling": {
        "policy": "largest_cpu_first",
        "sandbox_state_root": "workspaces/.distributed_sandbox_pool",
        "renew_before_seconds": 18000,
        "health_check_interval_seconds": 30,
        "artifact_transport": "rpc_stream",
    },
    "workers": [
        {
            "worker_id": f"sandbox-{index}",
            "name": f"{environment_name}-{index}",
            "sandbox_id": None,
            "create_if_missing": True,
            "available_cpu_cores": available_cpu_value,
            "available_memory_mb": scheduler_memory_mib,
            "gpu_count": 0,
            "lifecycle_minutes": int(lifecycle_minutes),
            "enabled": True,
        }
        for index in range(1, count_value + 1)
    ],
}

destination = Path(output)
temporary = destination.with_suffix(destination.suffix + ".tmp")
temporary.write_text(
    yaml.safe_dump(payload, sort_keys=False, allow_unicode=True),
    encoding="utf-8",
)
os.chmod(temporary, 0o600)
os.replace(temporary, destination)
print(f"Wrote Sandbox source configuration: {destination}")
print(
    f"Requested pool: {count_value} instances x {cpu_value} CPU / {memory}; "
    f"scheduler exposes {available_cpu_value} CPU / {scheduler_memory_mib} MiB per instance"
)
PY

if [[ "$shared_mount_read_only" == "false" ]]; then
  echo "Warning: writable GPFS currently requires the platform feature gate allowWritableGPFS." >&2
fi

if [[ "$generate_only" -eq 1 ]]; then
  echo "Generate-only mode: no Environment or Sandbox instances were created."
  exit 0
fi

"$PYTHON" scripts/update_sandbox_inventory.py \
  --input "$output" \
  --output "$inventory"

chmod 600 "$output" "$inventory"

echo
echo "Sandbox pool is ready."
echo "Source configuration: $output"
echo "Generated inventory:   $inventory"
echo
echo "Submit an evaluation with:"
echo "  bash scripts/submit_evaluation.sh submit \\"
echo "    --execution-mode distributed \\"
echo "    --distributed-transport sandbox \\"
echo "    --distributed-inventory $inventory \\"
echo "    TASK_ID"
