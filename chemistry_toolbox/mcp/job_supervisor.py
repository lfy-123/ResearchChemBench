"""Standalone persistent supervisor for one chemistry execution job.

This module intentionally uses only the Python standard library.  The MCP server
starts it in a detached process group and passes a trusted, server-generated JSON
specification.  It never parses shell syntax and always launches an argv vector.
"""

from __future__ import annotations

import json
import os
import resource
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from chemistry_toolbox.src.remote_scratch import (
    cleanup_remote_scratch,
    prepare_remote_scratch,
)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _atomic_json(path: Path, value: dict[str, Any]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def _preexec(
    resources: dict[str, Any],
    evaluation_budget: dict[str, Any],
    resource_allocation: dict[str, Any],
):
    def configure() -> None:
        # The supervisor enforces walltime for the complete process group.
        # RLIMIT_CPU counts aggregate thread CPU time for one process and can
        # terminate a valid parallel calculation well before its walltime.
        # RLIMIT_AS is also unsuitable here because scientific executables may
        # reserve a large virtual address space while using little resident
        # memory. The parent supervisor monitors process-group RSS instead.
        allocated_cpu_ids = [
            int(item) for item in resource_allocation.get("cpu_ids") or []
        ]
        cpu_cores = resources.get("cpu_cores")
        if allocated_cpu_ids and hasattr(os, "sched_setaffinity"):
            allowed = set(os.sched_getaffinity(0))
            selected = set(allocated_cpu_ids)
            if not selected <= allowed:
                raise RuntimeError(
                    "Allocated CPU ids are outside the job affinity: "
                    f"allocated={sorted(selected)}, allowed={sorted(allowed)}"
                )
            os.sched_setaffinity(0, selected)
        elif cpu_cores is not None and hasattr(os, "sched_getaffinity"):
            allowed = sorted(os.sched_getaffinity(0))
            if allowed:
                os.sched_setaffinity(0, set(allowed[: max(1, int(cpu_cores))]))

    return configure


def _memory_limit_mb(
    resources: dict[str, Any], evaluation_budget: dict[str, Any]
) -> int | None:
    candidates = [
        int(value)
        for value in (
            resources.get("memory_mb"),
            evaluation_budget.get("memory_mb"),
        )
        if value is not None
    ]
    return min(candidates) if candidates else None


def _process_group_rss_kb(process_group_id: int) -> int | None:
    proc = Path("/proc")
    if not proc.is_dir():
        return None
    total = 0
    observed = False
    for entry in proc.iterdir():
        if not entry.name.isdigit():
            continue
        try:
            stat = (entry / "stat").read_text(encoding="utf-8")
            fields = stat[stat.rfind(")") + 2 :].split()
            if len(fields) < 3 or int(fields[2]) != process_group_id:
                continue
            status = (entry / "status").read_text(encoding="utf-8")
            match = next(
                (line for line in status.splitlines() if line.startswith("VmRSS:")),
                None,
            )
            if match:
                total += int(match.split()[1])
            observed = True
        except (FileNotFoundError, PermissionError, ProcessLookupError, ValueError):
            continue
    return total if observed else None


def supervise(spec_path: Path) -> int:
    specification = json.loads(spec_path.read_text(encoding="utf-8"))
    job_directory = Path(specification["job_directory"]).resolve()
    status_path = Path(specification["status_path"]).resolve()
    stdout_path = Path(specification["stdout_path"]).resolve()
    stderr_path = Path(specification["stderr_path"]).resolve()
    command = [str(item) for item in specification["command"]]
    resources = dict(specification.get("resource_limits") or {})
    resource_allocation = dict(specification.get("resource_allocation") or {})
    evaluation_budget = dict(specification.get("evaluation_resource_budget") or {})
    walltime = max(1, int(resources.get("walltime_seconds") or 7200))
    memory_limit_mb = _memory_limit_mb(resources, evaluation_budget)
    started_at = _now()
    started_monotonic = time.monotonic()
    child: subprocess.Popen[bytes] | None = None
    cancellation_signal: int | None = None
    cancellation_path = job_directory / "cancel_requested"
    reservation_path_raw = str(
        specification.get("distributed_reservation_path") or ""
    )
    reservation_path = Path(reservation_path_raw) if reservation_path_raw else None
    scratch_directory: Path | None = None
    last_reservation_heartbeat = 0.0

    def heartbeat_reservation(*, force: bool = False) -> None:
        nonlocal last_reservation_heartbeat
        if reservation_path is None:
            return
        now = time.monotonic()
        if not force and now - last_reservation_heartbeat < 5.0:
            return
        try:
            value = json.loads(reservation_path.read_text(encoding="utf-8"))
            value["heartbeat_at"] = _now()
            value["heartbeat_unix"] = time.time()
            _atomic_json(reservation_path, value)
            last_reservation_heartbeat = now
        except (FileNotFoundError, OSError, json.JSONDecodeError):
            pass

    def status(state: str, **extra: Any) -> None:
        value = {
            "schema_version": 1,
            "job_id": specification["job_id"],
            "job_type": specification["job_type"],
            "status": state,
            "supervisor_pid": os.getpid(),
            "command": command,
            "job_directory": specification["relative_job_directory"],
            "stdout_path": specification["relative_stdout_path"],
            "stderr_path": specification["relative_stderr_path"],
            "resource_limits": resources,
            "resource_allocation": resource_allocation,
            "submitted_at": specification["submitted_at"],
            "started_at": started_at,
            "metadata": specification.get("metadata") or {},
            "execution_mode": specification.get("execution_mode", "local"),
            "compute_worker_id": specification.get("compute_worker_id"),
            "scratch_isolation": os.environ.get(
                "RESEARCHCHEM_DISTRIBUTED_SCRATCH_ISOLATION"
            ),
            **extra,
        }
        _atomic_json(status_path, value)

    def terminate_child(sig: int) -> None:
        nonlocal cancellation_signal
        cancellation_signal = sig
        if child is not None and child.poll() is None:
            try:
                os.killpg(child.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass

    signal.signal(signal.SIGTERM, lambda signum, _frame: terminate_child(signum))
    signal.signal(signal.SIGINT, lambda signum, _frame: terminate_child(signum))

    stdin_handle = None
    try:
        if specification.get("execution_mode") == "distributed":
            try:
                scratch_directory = prepare_remote_scratch(
                    os.environ, job_token=str(specification["job_id"])
                )
            except (OSError, ValueError) as exc:
                status(
                    "failed",
                    finished_at=_now(),
                    duration_seconds=0.0,
                    return_code=None,
                    error={"code": "remote_scratch_setup_failed", "message": str(exc)},
                )
                return 6
        heartbeat_reservation(force=True)
        if cancellation_path.is_file():
            status(
                "cancelled",
                finished_at=_now(),
                duration_seconds=0.0,
                return_code=None,
                error={"code": "cancelled", "message": "Job cancellation was requested"},
            )
            return 2
        if specification.get("stdin_path"):
            stdin_handle = Path(specification["stdin_path"]).open("rb")
        with stdout_path.open("ab", buffering=0) as stdout_handle, stderr_path.open(
            "ab", buffering=0
        ) as stderr_handle:
            try:
                child = subprocess.Popen(
                    command,
                    cwd=job_directory,
                    stdin=stdin_handle if stdin_handle is not None else subprocess.DEVNULL,
                    stdout=stdout_handle,
                    stderr=stderr_handle,
                    env=os.environ.copy(),
                    shell=False,
                    start_new_session=True,
                    close_fds=True,
                    preexec_fn=_preexec(
                        resources, evaluation_budget, resource_allocation
                    ),
                )
            except Exception as exc:
                status(
                    "failed",
                    finished_at=_now(),
                    duration_seconds=round(time.monotonic() - started_monotonic, 6),
                    return_code=None,
                    error={"code": "process_start_failed", "message": str(exc)},
                )
                return 1
            status("running", child_pid=child.pid, return_code=None)
            timed_out = False
            memory_exceeded = False
            peak_process_group_rss_kb = 0
            while child.poll() is None:
                heartbeat_reservation()
                if cancellation_path.is_file() and cancellation_signal is None:
                    cancellation_signal = signal.SIGTERM
                    try:
                        os.killpg(child.pid, signal.SIGTERM)
                    except ProcessLookupError:
                        pass
                if cancellation_signal is not None:
                    break
                if time.monotonic() - started_monotonic > walltime:
                    timed_out = True
                    try:
                        os.killpg(child.pid, signal.SIGTERM)
                    except ProcessLookupError:
                        pass
                    break
                process_group_rss_kb = _process_group_rss_kb(child.pid)
                if process_group_rss_kb is not None:
                    peak_process_group_rss_kb = max(
                        peak_process_group_rss_kb, process_group_rss_kb
                    )
                    if (
                        memory_limit_mb is not None
                        and process_group_rss_kb > memory_limit_mb * 1024
                    ):
                        memory_exceeded = True
                        try:
                            os.killpg(child.pid, signal.SIGTERM)
                        except ProcessLookupError:
                            pass
                        break
                time.sleep(0.2)
            if child.poll() is None:
                try:
                    child.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    try:
                        os.killpg(child.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    child.wait()
            background_process_cleanup = "none_detected"
            try:
                os.killpg(child.pid, 0)
            except ProcessLookupError:
                pass
            else:
                background_process_cleanup = "terminated_remaining_process_group"
                try:
                    os.killpg(child.pid, signal.SIGTERM)
                    time.sleep(0.2)
                    os.killpg(child.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            usage = resource.getrusage(resource.RUSAGE_CHILDREN)
            common = {
                "finished_at": _now(),
                "duration_seconds": round(time.monotonic() - started_monotonic, 6),
                "return_code": child.returncode,
                "background_process_cleanup": background_process_cleanup,
                "resource_usage": {
                    "user_cpu_seconds": round(usage.ru_utime, 6),
                    "system_cpu_seconds": round(usage.ru_stime, 6),
                    "max_rss_kb": usage.ru_maxrss,
                    "peak_process_group_rss_kb": peak_process_group_rss_kb,
                    "memory_limit_mb": memory_limit_mb,
                },
            }
            if cancellation_signal is not None:
                status(
                    "cancelled",
                    **common,
                    error={"code": "cancelled", "message": "Job cancellation was requested"},
                )
                return 2
            if timed_out:
                status(
                    "timeout",
                    **common,
                    error={
                        "code": "walltime_exceeded",
                        "message": f"Job exceeded {walltime} seconds",
                    },
                )
                return 3
            if memory_exceeded:
                status(
                    "failed",
                    **common,
                    error={
                        "code": "memory_limit_exceeded",
                        "message": (
                            f"Process group exceeded the {memory_limit_mb} MB job memory limit"
                        ),
                    },
                )
                return 5
            if child.returncode == 0:
                status("success", **common, error=None)
                return 0
            status(
                "failed",
                **common,
                error={
                    "code": "nonzero_exit",
                    "message": f"Program exited with status {child.returncode}",
                },
            )
            return 4
    finally:
        if stdin_handle is not None:
            stdin_handle.close()
        if reservation_path is not None:
            reservation_path.unlink(missing_ok=True)
        cleanup_remote_scratch(scratch_directory)


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: job_supervisor.py JOB_SPEC.json", file=sys.stderr)
        return 64
    return supervise(Path(sys.argv[1]).resolve())


if __name__ == "__main__":
    raise SystemExit(main())
