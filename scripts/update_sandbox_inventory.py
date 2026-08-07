#!/usr/bin/env python3
"""Probe or create OpenSandbox workers and atomically generate an inventory."""

from __future__ import annotations

import argparse
import json
import os
import shlex
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml

from chemistry_toolbox.src.distributed_pool import (
    effective_compute_cpu_cores,
    select_compute_core_groups,
    select_compute_cpu_ids,
    threads_per_physical_core,
)
from chemistry_toolbox.src.sandbox_client import OpenSandboxClient


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_PROJECT_PATH = str(PROJECT_ROOT)


REMOTE_PROBE = r"""
import json
import os
import socket
from pathlib import Path

allowed = sorted(os.sched_getaffinity(0))
cpus = []
for cpu in allowed:
    topology = Path(f"/sys/devices/system/cpu/cpu{cpu}/topology")
    core = int((topology / "core_id").read_text().strip())
    socket_id = int((topology / "physical_package_id").read_text().strip())
    siblings = [
        int(value)
        for part in (topology / "thread_siblings_list").read_text().strip().split(",")
        for value in (
            range(int(part.split("-")[0]), int(part.split("-")[1]) + 1)
            if "-" in part else [int(part)]
        )
        if int(value) in allowed
    ]
    nodes = list(Path(f"/sys/devices/system/cpu/cpu{cpu}").glob("node[0-9]*"))
    node = int(nodes[0].name[4:]) if nodes else -1
    cpus.append({
        "cpu": cpu,
        "core": core,
        "socket": socket_id,
        "numa_node": node,
        "siblings": sorted(set(siblings)),
    })

memory_limit_bytes = None
for candidate in (
    Path("/sys/fs/cgroup/memory.max"),
    Path("/sys/fs/cgroup/memory/memory.limit_in_bytes"),
):
    if not candidate.is_file():
        continue
    raw = candidate.read_text().strip()
    if raw and raw != "max":
        parsed = int(raw)
        if parsed < 1 << 60:
            memory_limit_bytes = parsed
            break
if memory_limit_bytes is None:
    for line in Path("/proc/meminfo").read_text().splitlines():
        if line.startswith("MemTotal:"):
            memory_limit_bytes = int(line.split()[1]) * 1024
            break

project = Path(os.environ["RCB_SANDBOX_PROBE_PROJECT_ROOT"])
print(json.dumps({
    "hostname": socket.gethostname(),
    "fqdn": socket.getfqdn(),
    "logical_cpus": len(allowed),
    "cpu_topology": cpus,
    "memory_mb": int(memory_limit_bytes // (1024 * 1024)),
    "project_readable": os.access(project, os.R_OK),
    "project_writable": os.access(project, os.W_OK),
    "framework": (project / ".envs/researchchembench/bin/python").is_file(),
}))
"""


def _load_local_environment() -> None:
    path = Path(
        os.environ.get("RESEARCHCHEMBENCH_LOCAL_CONFIG", PROJECT_ROOT / "config.local.env")
    )
    if not path.is_file():
        return
    try:
        from dotenv import load_dotenv
    except ImportError:
        return
    load_dotenv(path, override=False)


def _atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    os.chmod(temporary, 0o600)
    os.replace(temporary, path)


def _atomic_yaml(path: Path, value: Any) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        yaml.safe_dump(value, sort_keys=False, allow_unicode=True), encoding="utf-8"
    )
    os.chmod(temporary, 0o600)
    os.replace(temporary, path)


def _normalize_source(payload: dict[str, Any]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    api = dict(payload.get("api") or {})
    project_config = dict(payload.get("project") or {})
    environment = dict(payload.get("environment") or {})
    scheduling = dict(payload.get("scheduling") or {})
    entries = payload.get("sandboxes")
    if entries is None:
        entries = payload.get("workers")
    if not isinstance(entries, list) or not entries:
        raise ValueError("input must contain a non-empty sandboxes or workers list")
    common = {
        "base_url": str(
            api.get("base_url")
            or os.environ.get("RCB_SANDBOX_BASE_URL")
            or "https://h.pjlab.org.cn/brainbox"
        ),
        "project": str(
            api.get("project")
            or os.environ.get("RCB_SANDBOX_PROJECT")
            or "ailab-ai4chem"
        ),
        "api_key_env": str(api.get("api_key_env") or "RCB_SANDBOX_API_KEY"),
        "project_root": str(project_config.get("root") or DEFAULT_PROJECT_PATH),
        "remote_job_root": str(
            project_config.get("remote_job_root") or "/tmp/researchchembench/jobs"
        ),
        "environment": environment,
        "scheduling": scheduling,
    }
    return common, [dict(item) for item in entries]


def _control_client(common: dict[str, Any]) -> OpenSandboxClient:
    key_env = common["api_key_env"]
    api_key = os.environ.get(key_env, "").strip()
    if not api_key:
        raise ValueError(f"missing OpenSandbox API key environment variable: {key_env}")
    return OpenSandboxClient(
        base_url=common["base_url"],
        project=common["project"],
        api_key=api_key,
        sandbox_id="control-plane",
    )


def _environment_payload(environment: dict[str, Any]) -> dict[str, Any]:
    resources = dict(environment.get("resources") or {})
    ports = dict(environment.get("ports") or {})
    volumes = []
    for volume in environment.get("volumes") or []:
        item = dict(volume)
        volumes.append(
            {
                "name": str(item.get("name") or "storage-vol-1"),
                "mountPath": str(item["mount_path"]),
                "readOnly": bool(item.get("read_only", True)),
                "host": {"path": str(item["host_path"])},
            }
        )
    return {
        "name": str(environment.get("name") or "researchchembench-worker"),
        "description": str(
            environment.get("description")
            or "ResearchChemBench distributed OpenSandbox workers"
        ),
        "image": {"uri": str(environment["image"])},
        "entrypoint": list(environment.get("entrypoint") or ["sleep", "inf"]),
        "resources": {
            "cpu": str(resources.get("cpu") or "80"),
            "memory": str(resources.get("memory") or "180Gi"),
        },
        "ports": [
            {"containerPort": int(ports.get("command") or 44772), "purpose": "system service"},
            {
                "containerPort": int(ports.get("rpc") or 44773),
                "purpose": "ResearchChemBench worker RPC",
            },
        ],
        "defaultLifecycleMinutes": int(
            environment.get("default_lifecycle_minutes") or 1440
        ),
        "instanceCapacity": int(environment.get("instance_capacity") or 4),
        "prewarmSize": int(environment.get("prewarm_size") or 0),
        "ratio": int(environment.get("ratio") or 1),
        "volumes": volumes,
    }


def _ensure_environment(
    source: dict[str, Any], common: dict[str, Any], control: OpenSandboxClient
) -> str:
    environment = common["environment"]
    environment_id = str(environment.get("environment_id") or "")
    if environment_id:
        return environment_id
    if not environment.get("create_if_missing", False):
        return ""
    response = control.management_json(
        "POST", "/v1/sandbox-environments", payload=_environment_payload(environment), timeout=90
    )
    environment_id = str(response["id"])
    source.setdefault("environment", {})["environment_id"] = environment_id
    print(f"created sandbox environment {environment_id}")
    return environment_id


def _wait_running(
    control: OpenSandboxClient, sandbox_id: str, *, timeout: float = 300.0
) -> dict[str, Any]:
    deadline = time.monotonic() + timeout
    while True:
        detail = control.management_json("GET", f"/v1/sandboxes/{sandbox_id}")
        state = str((detail.get("status") or {}).get("state") or "")
        if state == "Running":
            return detail
        if state in {"Failed", "Terminated"}:
            raise RuntimeError(f"sandbox {sandbox_id} entered state {state}")
        if time.monotonic() >= deadline:
            raise TimeoutError(f"sandbox {sandbox_id} did not become Running")
        time.sleep(5.0)


def _ensure_sandbox(
    entry: dict[str, Any],
    *,
    index: int,
    environment_id: str,
    control: OpenSandboxClient,
) -> tuple[str, dict[str, Any]]:
    sandbox_id = str(entry.get("sandbox_id") or "")
    if not sandbox_id:
        if not entry.get("create_if_missing", False):
            raise ValueError(f"sandbox {index} requires sandbox_id")
        if not environment_id:
            raise ValueError(f"sandbox {index} cannot be created without environment_id")
        response = control.management_json(
            "POST",
            "/v1/sandboxes",
            payload={
                "environmentId": environment_id,
                "name": str(entry.get("name") or f"researchchembench-worker-{index}"),
                "type": "code",
                "lifecycleMinutes": int(entry.get("lifecycle_minutes") or 1440),
            },
            timeout=90,
        )
        sandbox_id = str(response["id"])
        entry["sandbox_id"] = sandbox_id
        print(f"created sandbox {sandbox_id}")
    return sandbox_id, _wait_running(control, sandbox_id)


def _probe(
    entry: dict[str, Any],
    *,
    index: int,
    sandbox_id: str,
    environment_id: str,
    common: dict[str, Any],
    control: OpenSandboxClient,
) -> dict[str, Any]:
    environment = common["environment"]
    ports = dict(environment.get("ports") or {})
    command_port = int(entry.get("command_port") or ports.get("command") or 44772)
    rpc_port = int(entry.get("rpc_port") or ports.get("rpc") or 44773)
    client = OpenSandboxClient(
        base_url=common["base_url"],
        project=common["project"],
        api_key=control.api_key,
        sandbox_id=sandbox_id,
        command_port=command_port,
        rpc_port=rpc_port,
        project_root=common["project_root"],
        remote_job_root=common["remote_job_root"],
    )
    project_root = common["project_root"]
    probe_command = (
        f"RCB_SANDBOX_PROBE_PROJECT_ROOT={shlex.quote(project_root)} "
        + shlex.join(["python3", "-c", REMOTE_PROBE])
    )
    completed = client.run_command(probe_command, timeout=60)
    if completed["status"] != "success":
        raise RuntimeError(
            f"sandbox {sandbox_id} probe failed: {completed.get('error')} "
            f"{completed.get('stderr')}"
        )
    try:
        probe = json.loads(completed["stdout"].strip().splitlines()[-1])
    except (json.JSONDecodeError, IndexError) as exc:
        raise RuntimeError(f"sandbox {sandbox_id} returned invalid probe JSON") from exc
    if not probe.get("project_readable") or not probe.get("framework"):
        raise RuntimeError(
            f"sandbox {sandbox_id} cannot read the project framework environment"
        )
    client.ensure_rpc()
    configured_cpu = int(entry["available_cpu_cores"])
    available_memory = int(entry["available_memory_mb"])
    logical_cpus = int(probe["logical_cpus"])
    memory_mb = int(probe["memory_mb"])
    if configured_cpu > logical_cpus:
        raise ValueError(
            f"sandbox {sandbox_id} configures {configured_cpu} CPU but owns {logical_cpus}"
        )
    if available_memory > memory_mb:
        raise ValueError(
            f"sandbox {sandbox_id} exposes {available_memory} MiB but owns {memory_mb} MiB"
        )
    topology = list(probe["cpu_topology"])
    threads_per_core = threads_per_physical_core(topology)
    available_cpu = effective_compute_cpu_cores(topology, configured_cpu)
    compute_cpu_ids = select_compute_cpu_ids(topology, available_cpu)
    compute_core_groups = select_compute_core_groups(topology, available_cpu)
    physical_cores = len(
        {(int(item["socket"]), int(item["core"])) for item in topology}
    )
    worker_id = str(entry.get("worker_id") or f"sandbox-{index}")
    return {
        "worker_id": worker_id,
        "name": str(entry.get("name") or probe["hostname"]),
        "hostname": str(probe["hostname"]),
        "fqdn": str(probe.get("fqdn") or probe["hostname"]),
        "transport": "sandbox",
        "execution_ssh_target": "",
        "direct_ip": "",
        "logical_cpus": logical_cpus,
        "physical_cores": physical_cores,
        "memory_mb": memory_mb,
        "configured_cpu_cores": configured_cpu,
        "available_cpu_cores": available_cpu,
        "available_memory_mb": available_memory,
        "reserved_cpu_cores": logical_cpus - configured_cpu,
        "unscheduled_smt_threads": configured_cpu - available_cpu,
        "reserved_memory_mb": memory_mb - available_memory,
        "gpu_count": int(entry.get("gpu_count") or 0),
        "threads_per_core": threads_per_core,
        "smt_enabled": threads_per_core > 1,
        "cpu_core_semantics": "physical",
        "compute_cpu_ids": compute_cpu_ids,
        "compute_core_groups": compute_core_groups,
        "all_cpu_ids": sorted(int(item["cpu"]) for item in topology),
        "sandbox_id": sandbox_id,
        "environment_id": environment_id,
        "sandbox_api_base": common["base_url"],
        "sandbox_project": common["project"],
        "sandbox_api_key_env": common["api_key_env"],
        "sandbox_command_port": command_port,
        "sandbox_rpc_port": rpc_port,
        "sandbox_project_root": project_root,
        "sandbox_remote_job_root": common["remote_job_root"],
        "enabled": bool(entry.get("enabled", True)),
        "connectivity_status": "reachable",
        "sandbox_state": "Running",
        "shared_project_writable": bool(probe.get("project_writable")),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args(argv)
    _load_local_environment()
    input_path = args.input.expanduser().resolve()
    output_path = args.output.expanduser()
    if not output_path.is_absolute():
        output_path = (PROJECT_ROOT / output_path).resolve()
    source = yaml.safe_load(input_path.read_text(encoding="utf-8")) or {}
    if not isinstance(source, dict):
        parser.error("input must contain a YAML mapping")
    common, entries = _normalize_source(source)
    control = _control_client(common)
    original_environment_id = str(
        (source.get("environment") or {}).get("environment_id") or ""
    )
    environment_id = _ensure_environment(source, common, control)
    workers = []
    errors = []
    changed = original_environment_id != environment_id
    source_entries = source.get("sandboxes")
    if source_entries is None:
        source_entries = source.get("workers")
    for index, entry in enumerate(entries, 1):
        try:
            sandbox_id, detail = _ensure_sandbox(
                entry,
                index=index,
                environment_id=environment_id,
                control=control,
            )
            del detail
            if source_entries[index - 1].get("sandbox_id") != sandbox_id:
                source_entries[index - 1]["sandbox_id"] = sandbox_id
                changed = True
            worker = _probe(
                entry,
                index=index,
                sandbox_id=sandbox_id,
                environment_id=environment_id,
                common=common,
                control=control,
            )
            workers.append(worker)
            print(
                f"[{index}/{len(entries)}] {worker['worker_id']} {sandbox_id} "
                f"actual={worker['logical_cpus']}threads/"
                f"{worker['physical_cores']}cores/{worker['memory_mb']}MiB "
                f"configured={worker['configured_cpu_cores']}threads "
                f"available={worker['available_cpu_cores']}physical-cores/"
                f"{worker['available_memory_mb']}MiB"
            )
        except Exception as exc:
            errors.append(f"sandbox {index}: {type(exc).__name__}: {exc}")
    if errors:
        if changed:
            _atomic_yaml(input_path, source)
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    if common["environment"].get("environment_id") != environment_id:
        source.setdefault("environment", {})["environment_id"] = environment_id
        changed = True
    if changed:
        _atomic_yaml(input_path, source)
    inventory = {
        "schema_version": 1,
        "transport": "sandbox",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "project_path": common["project_root"],
        "scheduling_policy": str(
            common["scheduling"].get("policy") or "largest_cpu_first"
        ),
        "workers": workers,
    }
    _atomic_json(output_path, inventory)
    print(f"wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
