#!/usr/bin/env python3
"""Probe rlaunch workers and atomically generate a local scheduler inventory."""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import shlex
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor, as_completed
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

host_key = Path("/etc/ssh/ssh_host_ed25519_key.pub").read_text().strip().split()
print(json.dumps({
    "hostname": socket.gethostname(),
    "fqdn": socket.getfqdn(),
    "ips": os.popen("hostname -I").read().split(),
    "logical_cpus": len(allowed),
    "cpu_topology": cpus,
    "memory_mb": int(memory_limit_bytes // (1024 * 1024)),
    "ssh_host_key_type": host_key[0],
    "ssh_host_public_key": host_key[1],
}))
"""


def _run(
    argv: list[str],
    *,
    input_text: str | None = None,
    timeout: int = 30,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        argv,
        input=input_text,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
        check=False,
    )


def _parse_ssh(value: str) -> tuple[list[str], str]:
    parts = shlex.split(value.strip())
    if parts and parts[0] == "ssh":
        parts = parts[1:]
    if not parts:
        raise ValueError("worker ssh entry is empty")
    # rlaunch prints option flags followed by one gateway target.  Reject a
    # remote command here so inventory updates cannot execute arbitrary input.
    target = parts[-1]
    if target.startswith("-") or "@" not in target:
        raise ValueError(f"cannot identify SSH target in {value!r}")
    options = parts[:-1]
    return options, target


def _fingerprint(key_type: str, public_key: str) -> str:
    del key_type
    digest = hashlib.sha256(base64.b64decode(public_key)).digest()
    return "SHA256:" + base64.b64encode(digest).decode().rstrip("=")


def _probe_worker(
    entry: dict[str, Any],
    *,
    index: int,
    known_hosts_path: Path,
    project_path: str,
) -> tuple[dict[str, Any], str]:
    options, gateway_target = _parse_ssh(str(entry["ssh"]))
    remote_probe_command = shlex.join(["python3", "-c", REMOTE_PROBE])
    gateway_argv = [
        "ssh",
        *options,
        "-o",
        "BatchMode=yes",
        "-o",
        "ConnectTimeout=15",
        gateway_target,
        remote_probe_command,
    ]
    completed = _run(gateway_argv, timeout=30)
    if completed.returncode != 0:
        raise RuntimeError(
            f"gateway probe failed for worker {index}: {completed.stderr.strip()}"
        )
    try:
        probe = json.loads(completed.stdout.strip().splitlines()[-1])
    except (json.JSONDecodeError, IndexError) as exc:
        raise RuntimeError(
            f"gateway probe returned invalid JSON for worker {index}"
        ) from exc
    ips = [value for value in probe.get("ips") or [] if value]
    if not ips:
        raise RuntimeError(f"worker {index} reported no direct IP")
    direct_ip = str(ips[0])
    configured_cpu = int(entry["available_cpu_cores"])
    available_memory = int(entry["available_memory_mb"])
    logical_cpus = int(probe["logical_cpus"])
    memory_mb = int(probe["memory_mb"])
    if configured_cpu > logical_cpus:
        raise ValueError(
            f"worker {index} configures {configured_cpu} CPU but owns {logical_cpus}"
        )
    if available_memory > memory_mb:
        raise ValueError(
            f"worker {index} exposes {available_memory} MiB but owns {memory_mb} MiB"
        )
    topology = list(probe["cpu_topology"])
    threads_per_core = threads_per_physical_core(topology)
    available_cpu = effective_compute_cpu_cores(topology, configured_cpu)
    compute_cpu_ids = select_compute_cpu_ids(topology, available_cpu)
    compute_core_groups = select_compute_core_groups(
        topology, available_cpu
    )
    physical_cores = len(
        {
            (int(item["socket"]), int(item["core"]))
            for item in probe["cpu_topology"]
        }
    )
    key_type = str(probe["ssh_host_key_type"])
    public_key = str(probe["ssh_host_public_key"])
    known_host_line = f"{direct_ip} {key_type} {public_key}"

    execution_user = str(entry.get("execution_user") or "liyuqiang")
    direct_target = f"{execution_user}@{direct_ip}"
    direct_probe_code = (
        "import json,os,socket;from pathlib import Path;"
        f"p=Path({project_path!r});"
        "print(json.dumps({'user':os.environ.get('USER',''),"
        "'hostname':socket.gethostname(),'project_writable':os.access(p,os.W_OK),"
        "'framework':(p/'.envs/researchchembench/bin/python').is_file()}))"
    )
    direct_probe_command = shlex.join(["python3", "-c", direct_probe_code])
    with tempfile.NamedTemporaryFile("w", encoding="utf-8") as handle:
        handle.write(known_host_line + "\n")
        handle.flush()
        direct = _run(
            [
                "ssh",
                "-o",
                "BatchMode=yes",
                "-o",
                "ConnectTimeout=8",
                "-o",
                "StrictHostKeyChecking=yes",
                "-o",
                f"UserKnownHostsFile={handle.name}",
                direct_target,
                direct_probe_command,
            ],
            timeout=20,
        )
    if direct.returncode != 0:
        raise RuntimeError(
            f"direct SSH validation failed for worker {index}: {direct.stderr.strip()}"
        )
    direct_probe = json.loads(direct.stdout.strip().splitlines()[-1])
    if not direct_probe.get("project_writable") or not direct_probe.get("framework"):
        raise RuntimeError(
            f"worker {index} lacks writable project or framework environment"
        )

    configured_name = str(entry.get("name") or "").strip()
    discovered_name = str(probe["hostname"])
    if configured_name and configured_name != discovered_name:
        raise ValueError(
            f"worker {index} configured name {configured_name!r} does not match "
            f"remote hostname {discovered_name!r}"
        )
    return (
        {
            "worker_id": str(entry.get("worker_id") or f"compute-{index}"),
            "name": discovered_name,
            "hostname": discovered_name,
            "fqdn": str(probe.get("fqdn") or discovered_name),
            "gateway_ssh_target": gateway_target,
            "gateway_ssh_options": options,
            "execution_ssh_target": direct_target,
            "direct_ip": direct_ip,
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
            "all_cpu_ids": sorted(
                int(item["cpu"]) for item in probe["cpu_topology"]
            ),
            "known_hosts_file": str(known_hosts_path.resolve()),
            "ssh_host_key_fingerprint": _fingerprint(key_type, public_key),
            "enabled": bool(entry.get("enabled", True)),
            "connectivity_status": "reachable",
        },
        known_host_line,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--known-hosts", type=Path)
    parser.add_argument("--project-path", default=DEFAULT_PROJECT_PATH)
    args = parser.parse_args(argv)

    input_path = args.input.expanduser().resolve()
    output_path = args.output.expanduser()
    if not output_path.is_absolute():
        output_path = (PROJECT_ROOT / output_path).resolve()
    known_hosts_path = args.known_hosts or output_path.with_suffix(".known_hosts")
    if not known_hosts_path.is_absolute():
        known_hosts_path = (PROJECT_ROOT / known_hosts_path).resolve()
    payload = yaml.safe_load(input_path.read_text(encoding="utf-8")) or {}
    entries = payload.get("workers") if isinstance(payload, dict) else None
    if not isinstance(entries, list) or not entries:
        parser.error("input must contain a non-empty workers list")

    workers_by_index: dict[int, dict[str, Any]] = {}
    known_hosts_by_index: dict[int, str] = {}
    errors: list[str] = []
    valid_entries: list[tuple[int, dict[str, Any]]] = []
    for index, entry in enumerate(entries, 1):
        if not isinstance(entry, dict):
            errors.append(f"worker {index}: entry must be a mapping")
            continue
        valid_entries.append((index, entry))
    with ThreadPoolExecutor(max_workers=min(16, len(valid_entries) or 1)) as executor:
        futures = {
            executor.submit(
                _probe_worker,
                entry,
                index=index,
                known_hosts_path=known_hosts_path,
                project_path=args.project_path,
            ): index
            for index, entry in valid_entries
        }
        for future in as_completed(futures):
            index = futures[future]
            try:
                worker, known_host = future.result()
            except Exception as exc:
                errors.append(f"worker {index}: {type(exc).__name__}: {exc}")
                continue
            workers_by_index[index] = worker
            known_hosts_by_index[index] = known_host
            print(
                f"[{index}/{len(entries)}] {worker['worker_id']} {worker['name']} "
                f"actual={worker['logical_cpus']}threads/"
                f"{worker['physical_cores']}cores/{worker['memory_mb']}MiB "
                f"configured={worker['configured_cpu_cores']}threads "
                f"available={worker['available_cpu_cores']}physical-cores/"
                f"{worker['available_memory_mb']}MiB",
                flush=True,
            )

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1
    workers = [workers_by_index[index] for index, _entry in valid_entries]
    known_host_lines = [known_hosts_by_index[index] for index, _entry in valid_entries]

    known_hosts_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_known_hosts = known_hosts_path.with_suffix(
        known_hosts_path.suffix + ".tmp"
    )
    temporary_known_hosts.write_text(
        "\n".join(known_host_lines) + "\n", encoding="utf-8"
    )
    os.chmod(temporary_known_hosts, 0o600)
    os.replace(temporary_known_hosts, known_hosts_path)
    inventory = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "project_path": args.project_path,
        "scheduling_policy": "largest_cpu_first",
        "workers": workers,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    temporary_output = output_path.with_suffix(output_path.suffix + ".tmp")
    temporary_output.write_text(
        json.dumps(inventory, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    os.chmod(temporary_output, 0o600)
    os.replace(temporary_output, output_path)
    print(f"Inventory: {output_path}")
    print(f"Known hosts: {known_hosts_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
