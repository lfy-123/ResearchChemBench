"""Standalone persistent supervisor for one chemistry execution job.

This module intentionally uses only the Python standard library.  The MCP server
starts it in a detached process group and passes a trusted, server-generated JSON
specification.  It never parses shell syntax and always launches an argv vector.
"""

from __future__ import annotations

from chemistry_toolbox.src.execution_states import TERMINAL_STATES

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

from chemistry_toolbox.mcp.execution_store import ExecutionStore


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
        # Gaussian can emit multi-gigabyte ELF core images when a native
        # process aborts (for example after a filesystem write failure).  Core
        # images are not part of the scientific evidence contract: input,
        # stdout, stderr, checkpoint, status, and cancellation/recovery
        # records are retained separately.  Disable only core dumping for the
        # child process group so a crash cannot consume the user's quota and
        # prevent subsequent author-route retries.  This does not impose a
        # wall-clock limit or alter Gaussian's numerical calculation.
        try:
            resource.setrlimit(resource.RLIMIT_CORE, (0, 0))
        except (AttributeError, OSError, ValueError):
            # Platforms without RLIMIT_CORE (or restrictive launchers) keep
            # the prior behavior; supervision must still proceed.
            pass
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
    raw_walltime = resources.get("walltime_seconds")
    # ``None`` is an explicit evaluator policy for a native job that must be
    # allowed to finish naturally (for example a long Gaussian optimization).
    # Resource and cancellation supervision remain active in this mode.
    walltime = max(1, int(raw_walltime)) if raw_walltime is not None else None
    memory_limit_mb = _memory_limit_mb(resources, evaluation_budget)
    run_deadline = specification.get("run_deadline")
    absolute_deadline = datetime.fromisoformat(run_deadline).timestamp() if run_deadline else None
    started_at = _now()
    started_monotonic = time.monotonic()
    job_deadline = min(time.time() + walltime if walltime is not None else float("inf"),
                       absolute_deadline if absolute_deadline is not None else float("inf"))
    job_deadline_at = datetime.fromtimestamp(job_deadline, timezone.utc).isoformat() if job_deadline != float("inf") else None
    child: subprocess.Popen[bytes] | None = None
    cancellation_signal: int | None = None
    cancellation_path = job_directory / "cancel_requested"
    reservation_path_raw = str(
        specification.get("distributed_reservation_path") or ""
    )
    reservation_path = Path(reservation_path_raw) if reservation_path_raw else None
    scratch_directory: Path | None = None
    last_reservation_heartbeat = 0.0
    last_activity_at, activity = 0.0, None

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
            "process_started": child is not None,
            "child_pid": child.pid if child is not None else None,
            "deadline_at": job_deadline_at,
            "metadata": specification.get("metadata") or {},
            "execution_mode": specification.get("execution_mode", "local"),
            "compute_worker_id": specification.get("compute_worker_id"),
            "scratch_isolation": os.environ.get(
                "RESEARCHCHEM_DISTRIBUTED_SCRATCH_ISOLATION"
            ),
            **extra,
        }
        _atomic_json(status_path, value)
        if specification.get("recovery_managed"):
            from chemistry_toolbox.src.recovery_io import atomic_json, process_identity
            value["launch_token"] = specification["launch_token"]
            value["recovery_managed"] = True
            store = ExecutionStore(Path(specification["workspace"]), run_id=specification["run_id"])
            if state in TERMINAL_STATES:
                atomic_json(store.directory / "terminal" / (specification["job_id"] + ".json"), value)
            _atomic_json(status_path, value)
            try:
                store.record_job_state(specification["job_id"], state, state_payload={
                    "status": value, "supervisor_identity": process_identity(os.getpid()),
                    **({"child_identity": process_identity(extra["child_pid"])} if extra.get("child_pid") else {})})
            except Exception as exc:
                # Keep supervising the child; the trusted terminal fact above
                # can be reconciled even if SQLite was temporarily unavailable.
                print(f"execution_store_write_failed: {type(exc).__name__}: {exc}", file=sys.stderr, flush=True)

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
        if absolute_deadline is not None and time.time() >= absolute_deadline:
            status("timeout", finished_at=_now(), duration_seconds=0, return_code=None,
                   error={"code": "run_deadline_exceeded", "message": "Original run deadline expired before launch"})
            return 3
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
                if time.monotonic() - last_activity_at >= 30:
                    last_activity_at = time.monotonic()
                    try:
                        from chemistry_toolbox.src.process_activity import process_activity
                        activity = process_activity(child.pid, (stdout_path, stderr_path), activity)
                        _atomic_json(job_directory / "activity.json", activity)
                    except Exception:
                        pass  # Observability must never change process supervision.
                if cancellation_path.is_file() and cancellation_signal is None:
                    cancellation_signal = signal.SIGTERM
                    try:
                        os.killpg(child.pid, signal.SIGTERM)
                    except ProcessLookupError:
                        pass
                if cancellation_signal is not None:
                    break
                if (walltime is not None and time.monotonic() - started_monotonic > walltime) or (absolute_deadline is not None and time.time() >= absolute_deadline):
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
            if specification.get("recovery_managed"):
                from chemistry_toolbox.src.recovery_io import token_processes, signal_identity
                survivors = [item for item in token_processes(specification["launch_token"]) if item["pid"] != os.getpid()]
                for item in survivors:
                    signal_identity(item)
                if survivors:
                    time.sleep(0.2)
                    for item in token_processes(specification["launch_token"]):
                        if item["pid"] != os.getpid():
                            signal_identity(item, signal.SIGKILL)
                    time.sleep(0.1)
                    if any(item["pid"] != os.getpid() for item in token_processes(specification["launch_token"])):
                        status("needs_reconciliation", error={"code": "surviving_descendants", "message": "Managed descendants could not be stopped"})
                        return 7
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
                cancel_reason = None
                if cancellation_path.is_file():
                    try: cancel_reason = json.loads(cancellation_path.read_text()).get("reason")
                    except (OSError, ValueError): pass
                if cancel_reason == "deadline":
                    status("timeout", **common, error={"code": "run_deadline_exceeded", "message": "Original run deadline expired"})
                    return 3
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
            if specification.get("recovery_managed") and specification["job_type"] == "predefined_action":
                from .action_result_io import read_action_result
                store = ExecutionStore(Path(specification["workspace"]), run_id=specification["run_id"])
                result, problem = read_action_result(store, specification["job_id"], launch_token=specification["launch_token"])
                if problem:
                    status("failed", **common, error=problem)
                    return 4
                if child.returncode < 0 or (child.returncode != 0 and result["status"] in {"success", "partial_success"}):
                    status("failed", **common, error={"code": "result_process_conflict", "message": "Action result conflicts with abnormal worker termination"})
                    return 4
                status(result["status"], **common, error=result.get("error"))
                return 0 if result["status"] in {"success", "partial_success"} else 4
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
