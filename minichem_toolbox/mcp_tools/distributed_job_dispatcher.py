"""Queue and dispatch one native/analysis job to the distributed compute pool."""

from __future__ import annotations

import json
import os
import shlex
import stat
import subprocess
import sys
import tarfile
import tempfile
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from minichem_toolbox.distributed_pool import (
    DistributedResourceLimitExceeded,
    DistributedResourceUnavailable,
    pool_snapshot,
    register_distributed_request,
    reserve_distributed_resources,
)
from minichem_toolbox.paths import PROJECT_ROOT
from minichem_toolbox.sandbox_client import (
    OpenSandboxClient,
    SandboxTransportError,
)

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


def _replace_job_path(value: str, *, local_root: Path, remote_root: Path) -> str:
    text = str(value)
    local_text = str(local_root)
    if text == local_text:
        return str(remote_root)
    prefix = local_text + os.sep
    if text.startswith(prefix):
        return str(remote_root / text[len(prefix) :])
    return text


def _sandbox_specification(
    specification: dict[str, Any], *, remote_directory: Path
) -> dict[str, Any]:
    local_directory = Path(specification["job_directory"]).resolve()
    remote = dict(specification)
    for key in (
        "job_directory",
        "status_path",
        "stdout_path",
        "stderr_path",
        "stdin_path",
    ):
        if remote.get(key):
            remote[key] = _replace_job_path(
                str(remote[key]), local_root=local_directory, remote_root=remote_directory
            )
    remote["command"] = [
        _replace_job_path(
            str(item), local_root=local_directory, remote_root=remote_directory
        )
        for item in specification["command"]
    ]
    # The coordinator owns the reservation heartbeat for sandbox jobs because
    # the project GPFS mount is intentionally read-only inside the sandbox.
    remote["distributed_reservation_path"] = ""
    remote["distributed_transport"] = "sandbox"
    return remote


def _sandbox_environment(
    environment: dict[str, str], *, local_directory: Path, remote_directory: Path
) -> dict[str, str]:
    result = {}
    path_list_names = {
        "PATH",
        "PYTHONPATH",
        "LD_LIBRARY_PATH",
        "LIBRARY_PATH",
        "CPATH",
        "PKG_CONFIG_PATH",
    }
    for key, value in environment.items():
        if key in path_list_names:
            result[key] = os.pathsep.join(
                _replace_job_path(
                    item, local_root=local_directory, remote_root=remote_directory
                )
                for item in value.split(os.pathsep)
            )
        else:
            result[key] = _replace_job_path(
                value, local_root=local_directory, remote_root=remote_directory
            )
    return result


def _job_archive(job_directory: Path, destination: Path) -> None:
    with tarfile.open(destination, "w:gz", dereference=True) as archive:
        for child in sorted(job_directory.iterdir()):
            if child.name.startswith("dispatcher."):
                continue
            archive.add(child, arcname=child.name, recursive=True)


def _extract_job_archive(archive_path: Path, destination: Path) -> None:
    root = destination.resolve()
    with tarfile.open(archive_path, "r:gz") as archive:
        for member in archive.getmembers():
            if member.issym() or member.islnk():
                raise ValueError("sandbox job archive contains links")
            target = (destination / member.name).resolve()
            if target != root and root not in target.parents:
                raise ValueError(
                    f"sandbox job archive escapes destination: {member.name}"
                )
            if target.is_file():
                target.chmod(target.stat().st_mode | stat.S_IWUSR)
            elif target.is_dir():
                target.chmod(target.stat().st_mode | stat.S_IRWXU)
        archive.extractall(destination)


def _sandbox_synchronizing_status(
    remote_status: dict[str, Any], *, terminal_status: str
) -> dict[str, Any]:
    status = dict(remote_status)
    status.update(
        {
            "status": "running",
            "sandbox_remote_terminal_status": terminal_status,
            "sandbox_artifacts_synchronizing": True,
        }
    )
    status.pop("finished_at", None)
    status.pop("duration_seconds", None)
    return status


def _dispatch_sandbox(
    *,
    specification: dict[str, Any],
    status_path: Path,
    reservation,
    environment: dict[str, str],
) -> int:
    worker = reservation.worker
    job_id = str(specification["job_id"])
    local_directory = Path(specification["job_directory"]).resolve()
    remote_directory = Path(worker.sandbox_remote_job_root) / job_id
    client = OpenSandboxClient.from_worker(worker)
    try:
        client.ensure_rpc()
        with tempfile.NamedTemporaryFile(suffix=".tar.gz") as handle:
            _job_archive(local_directory, Path(handle.name))
            client.upload_job_archive(job_id, Path(handle.name))
        response = client.start_job(
            job_id,
            specification=_sandbox_specification(
                specification, remote_directory=remote_directory
            ),
            environment=_sandbox_environment(
                environment,
                local_directory=local_directory,
                remote_directory=remote_directory,
            ),
        )
        if response.get("status") != "success":
            raise SandboxTransportError(str(response.get("error") or response))
        _update_status(
            status_path,
            status="dispatching",
            distributed_transport="sandbox",
            sandbox_id=worker.sandbox_id,
            remote_supervisor_pid=int(response["supervisor_pid"]),
            dispatcher_pid=os.getpid(),
            updated_at=_now(),
        )
        cancellation_sent = False
        consecutive_failures = 0
        while True:
            if _cancelled(specification) and not cancellation_sent:
                client.cancel_job(job_id)
                cancellation_sent = True
            try:
                snapshot = client.job_status(job_id)
                consecutive_failures = 0
            except SandboxTransportError:
                consecutive_failures += 1
                if consecutive_failures < 5:
                    time.sleep(2.0)
                    continue
                raise
            remote_status = dict(snapshot.get("job") or {})
            remote_status.update(
                {
                    "distributed_transport": "sandbox",
                    "sandbox_id": worker.sandbox_id,
                    "dispatcher_pid": os.getpid(),
                    "compute_worker_id": worker.worker_id,
                    "distributed_reservation_id": reservation.reservation_id,
                }
            )
            Path(specification["stdout_path"]).write_text(
                str(snapshot.get("stdout_tail") or ""), encoding="utf-8"
            )
            Path(specification["stderr_path"]).write_text(
                str(snapshot.get("stderr_tail") or ""), encoding="utf-8"
            )
            terminal_status = str(remote_status.get("status") or "")
            if terminal_status in {
                "success",
                "failed",
                "timeout",
                "cancelled",
            }:
                # Do not expose a terminal local state until the complete remote
                # job directory has landed.  Otherwise collect_execution_job can
                # observe success during the archive-download window and return
                # before declared outputs are present, unlike the SSH/shared-FS
                # transport where terminal status and files become visible
                # together.
                synchronizing_status = _sandbox_synchronizing_status(
                    remote_status, terminal_status=terminal_status
                )
                _atomic_json(status_path, synchronizing_status)
                with tempfile.NamedTemporaryFile(suffix=".tar.gz") as handle:
                    client.download_job_archive(job_id, Path(handle.name))
                    _extract_job_archive(Path(handle.name), local_directory)
                (local_directory / "sandbox_supervisor_spec.json").unlink(
                    missing_ok=True
                )
                final_status = json.loads(status_path.read_text(encoding="utf-8"))
                final_status.update(
                    {
                        "distributed_transport": "sandbox",
                        "sandbox_id": worker.sandbox_id,
                        "dispatcher_pid": os.getpid(),
                        "compute_worker_id": worker.worker_id,
                        "distributed_reservation_id": reservation.reservation_id,
                        "sandbox_artifacts_synchronized": True,
                        "sandbox_artifacts_synchronizing": False,
                    }
                )
                _atomic_json(status_path, final_status)
                try:
                    client.delete_job(job_id)
                except SandboxTransportError:
                    pass
                return 0 if final_status.get("status") == "success" else 1
            _atomic_json(status_path, remote_status)
            time.sleep(1.0)
    except Exception as exc:
        _update_status(
            status_path,
            status="failed",
            finished_at=_now(),
            distributed_transport="sandbox",
            sandbox_id=worker.sandbox_id,
            error={
                "code": "sandbox_remote_job_failed",
                "message": str(exc),
            },
        )
        return 1
    finally:
        reservation.release()


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
    if worker.transport == "sandbox":
        return _dispatch_sandbox(
            specification=specification,
            status_path=status_path,
            reservation=reservation,
            environment=environment,
        )
    framework_python = (
        PROJECT_ROOT / ".mini_software_cache" / "runtimes" / "minichem" / "bin" / "python"
    )
    remote_command = (
        f"cd {shlex.quote(str(PROJECT_ROOT))} && exec "
        f"{shlex.quote(str(framework_python))} -m "
        "minichem_mcp_tools.remote_job_launcher"
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
