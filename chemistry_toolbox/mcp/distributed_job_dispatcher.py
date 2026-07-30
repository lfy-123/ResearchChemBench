"""Queue and dispatch one native/analysis job to the distributed compute pool."""

from __future__ import annotations

import json
import os
import shlex
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from researchchem_toolbox.distributed_pool import (
    DistributedResourceLimitExceeded,
    DistributedResourceUnavailable,
    pool_snapshot,
    register_distributed_request,
    reserve_distributed_resources,
)
from researchchem_toolbox.paths import PROJECT_ROOT

from .open_execution import _job_environment


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _atomic_json(path: Path, value: dict[str, Any]) -> None:
    temporary = path.with_suffix(path.suffix + f".{uuid.uuid4().hex}.tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    os.replace(temporary, path)


def _cancelled(specification: dict[str, Any]) -> bool:
    return Path(specification["job_directory"], "cancel_requested").is_file()


def _update_status(status_path: Path, **updates: Any) -> dict[str, Any]:
    status = json.loads(status_path.read_text(encoding="utf-8"))
    status.update(updates)
    _atomic_json(status_path, status)
    return status


def dispatch(spec_path: Path) -> int:
    specification = json.loads(spec_path.read_text(encoding="utf-8"))
    status_path = Path(specification["status_path"])
    resources = dict(specification["resource_limits"])
    label = str(
        (specification.get("metadata") or {}).get("label")
        or specification["command"][0]
    )
    try:
        queue_request = register_distributed_request(
            resources,
            kind=str(specification["job_type"]),
            label=label,
            workspace=str(Path(specification["job_directory"]).parent),
            job_id=str(specification["job_id"]),
            job_status_path=str(status_path),
        )
    except DistributedResourceLimitExceeded as exc:
        _update_status(
            status_path,
            status="failed",
            finished_at=_now(),
            error=exc.as_error(),
        )
        return 1
    _update_status(
        status_path,
        distributed_queue_request_id=queue_request.request_id,
        queue_reason="waiting_for_distributed_resources",
        resource_snapshot=pool_snapshot(),
        updated_at=_now(),
    )
    try:
        while True:
            if _cancelled(specification):
                _update_status(
                    status_path,
                    status="cancelled",
                    finished_at=_now(),
                    error={"code": "cancelled", "message": "Job cancelled while queued"},
                )
                return 2
            try:
                reservation = reserve_distributed_resources(
                    resources,
                    kind=str(specification["job_type"]),
                    label=label,
                    workspace=str(Path(specification["job_directory"]).parent),
                    job_id=str(specification["job_id"]),
                    job_status_path=str(status_path),
                    queue_request_id=queue_request.request_id,
                )
                break
            except DistributedResourceUnavailable as exc:
                _update_status(
                    status_path,
                    status="queued",
                    queue_reason=exc.reason,
                    resource_snapshot=exc.snapshot,
                    updated_at=_now(),
                )
                time.sleep(1.0)
    finally:
        queue_request.release()
    allocation = dict(reservation.resource_allocation)
    worker = reservation.worker
    specification["resource_allocation"] = allocation
    specification["distributed_reservation_path"] = str(reservation.path)
    specification["execution_mode"] = "distributed"
    specification["compute_worker_id"] = worker.worker_id
    _atomic_json(spec_path, specification)
    request_path = Path(specification["job_directory"]) / "request.json"
    request = json.loads(request_path.read_text(encoding="utf-8"))
    request["resource_allocation"] = allocation
    request["execution_mode"] = "distributed"
    request["compute_worker_id"] = worker.worker_id
    _atomic_json(request_path, request)
    _update_status(
        status_path,
        status="dispatching",
        resource_allocation=allocation,
        execution_mode="distributed",
        compute_worker_id=worker.worker_id,
        distributed_reservation_id=reservation.reservation_id,
        resource_snapshot=pool_snapshot(),
        updated_at=_now(),
    )
    reservation.attach_job(
        job_id=str(specification["job_id"]), job_status_path=str(status_path)
    )
    environment = _job_environment(
        str(specification["runtime"]),
        str(specification["job_id"]),
        Path(specification["job_directory"]),
        resources,
        allocation,
        job_type=str(specification["job_type"]),
    )
    framework_python = PROJECT_ROOT / ".envs" / "researchchembench" / "bin" / "python"
    remote_command = (
        f"cd {shlex.quote(str(PROJECT_ROOT))} && exec "
        f"{shlex.quote(str(framework_python))} -m "
        "chemistry_toolbox.mcp.remote_job_launcher"
    )
    ssh_options = shlex.split(
        os.environ.get("RCB_DISTRIBUTED_DIRECT_SSH_OPTIONS", "-C")
    )
    ssh_argv = [
        "ssh",
        *ssh_options,
        "-o",
        "BatchMode=yes",
        "-o",
        "ConnectTimeout=15",
        "-o",
        "StrictHostKeyChecking=yes",
    ]
    if worker.known_hosts_file:
        ssh_argv.extend(
            ["-o", f"UserKnownHostsFile={worker.known_hosts_file}"]
        )
    ssh_argv.extend([worker.execution_ssh_target, remote_command])
    envelope = {
        "schema_version": 1,
        "spec_path": str(spec_path),
        "job_directory": str(specification["job_directory"]),
        "environment": environment,
    }
    try:
        completed = subprocess.run(
            ssh_argv,
            input=json.dumps(envelope, ensure_ascii=False),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=45,
            check=False,
            cwd=PROJECT_ROOT,
        )
        response = json.loads(completed.stdout.strip().splitlines()[-1])
        if completed.returncode != 0 or response.get("status") != "success":
            raise RuntimeError(
                str(response.get("error") or completed.stderr[-2000:])
            )
    except Exception as exc:
        reservation.release()
        _update_status(
            status_path,
            status="failed",
            finished_at=_now(),
            error={"code": "remote_supervisor_start_failed", "message": str(exc)},
        )
        return 1
    reservation.stop_heartbeat()
    current = json.loads(status_path.read_text(encoding="utf-8"))
    current["remote_supervisor_pid"] = int(response["supervisor_pid"])
    current["dispatcher_finished_at"] = _now()
    _atomic_json(status_path, current)
    return 0


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: distributed_job_dispatcher.py SUPERVISOR_SPEC.json", file=sys.stderr)
        return 64
    return dispatch(Path(sys.argv[1]).resolve())


if __name__ == "__main__":
    raise SystemExit(main())
