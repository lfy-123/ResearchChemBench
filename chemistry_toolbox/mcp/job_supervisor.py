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


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _atomic_json(path: Path, value: dict[str, Any]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def _preexec(resources: dict[str, Any]):
    def configure() -> None:
        memory_mb = resources.get("memory_mb")
        if memory_mb is not None:
            limit = int(memory_mb) * 1024 * 1024
            resource.setrlimit(resource.RLIMIT_AS, (limit, limit))
        walltime = max(1, int(resources.get("walltime_seconds") or 1800))
        cpu_limit = walltime + 5
        resource.setrlimit(resource.RLIMIT_CPU, (cpu_limit, cpu_limit))
        cpu_cores = resources.get("cpu_cores")
        if cpu_cores is not None and hasattr(os, "sched_getaffinity"):
            allowed = sorted(os.sched_getaffinity(0))
            if allowed:
                os.sched_setaffinity(0, set(allowed[: max(1, int(cpu_cores))]))

    return configure


def supervise(spec_path: Path) -> int:
    specification = json.loads(spec_path.read_text(encoding="utf-8"))
    job_directory = Path(specification["job_directory"]).resolve()
    status_path = Path(specification["status_path"]).resolve()
    stdout_path = Path(specification["stdout_path"]).resolve()
    stderr_path = Path(specification["stderr_path"]).resolve()
    command = [str(item) for item in specification["command"]]
    resources = dict(specification.get("resource_limits") or {})
    walltime = max(1, int(resources.get("walltime_seconds") or 1800))
    started_at = _now()
    started_monotonic = time.monotonic()
    child: subprocess.Popen[bytes] | None = None
    cancellation_signal: int | None = None

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
            "submitted_at": specification["submitted_at"],
            "started_at": started_at,
            "metadata": specification.get("metadata") or {},
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
                    preexec_fn=_preexec(resources),
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
            while child.poll() is None:
                if cancellation_signal is not None:
                    break
                if time.monotonic() - started_monotonic > walltime:
                    timed_out = True
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
            usage = resource.getrusage(resource.RUSAGE_CHILDREN)
            common = {
                "finished_at": _now(),
                "duration_seconds": round(time.monotonic() - started_monotonic, 6),
                "return_code": child.returncode,
                "resource_usage": {
                    "user_cpu_seconds": round(usage.ru_utime, 6),
                    "system_cpu_seconds": round(usage.ru_stime, 6),
                    "max_rss_kb": usage.ru_maxrss,
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


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: job_supervisor.py JOB_SPEC.json", file=sys.stderr)
        return 64
    return supervise(Path(sys.argv[1]).resolve())


if __name__ == "__main__":
    raise SystemExit(main())
