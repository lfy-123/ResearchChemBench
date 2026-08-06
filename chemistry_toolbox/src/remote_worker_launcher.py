"""Run one predefined Action worker on a trusted remote compute node.

The coordinator sends the environment and Action payload over SSH stdin so
credentials and evaluator configuration do not appear in the remote command
line.  The scientific runtime remains responsible for applying the exact CPU
affinity before importing backend modules, and cancellation is propagated from
the SSH owner through every scientific subprocess group.
"""

from __future__ import annotations

import ctypes
import json
import os
import signal
import subprocess
import sys
from pathlib import Path
from typing import Any

from .remote_scratch import cleanup_remote_scratch, prepare_remote_scratch


def _failure(code: str, message: str, **details: Any) -> dict[str, Any]:
    return {
        "status": "failed",
        "error": {"code": code, "message": message, **details},
        "retryable": False,
    }


def _request_parent_death_signal() -> None:
    """Ask Linux to terminate this launcher when the owning sshd exits."""

    if not sys.platform.startswith("linux"):
        return
    parent = os.getppid()
    libc = ctypes.CDLL(None, use_errno=True)
    if libc.prctl(1, signal.SIGTERM, 0, 0, 0) != 0:  # PR_SET_PDEATHSIG
        errno = ctypes.get_errno()
        raise OSError(errno, os.strerror(errno))
    if os.getppid() != parent:
        os.kill(os.getpid(), signal.SIGTERM)


def _terminate_child(process: subprocess.Popen, *, grace_seconds: float = 5.0) -> None:
    if process.poll() is not None:
        return
    if os.name == "posix":
        try:
            os.killpg(process.pid, signal.SIGTERM)
        except ProcessLookupError:
            return
    else:
        process.terminate()
    try:
        process.wait(timeout=grace_seconds)
    except subprocess.TimeoutExpired:
        if os.name == "posix":
            try:
                os.killpg(process.pid, signal.SIGKILL)
            except ProcessLookupError:
                return
        else:
            process.kill()
        process.wait()


def main() -> int:
    process: subprocess.Popen | None = None
    scratch_directory: Path | None = None
    termination_signal = 0

    def handle_termination(signum, _frame) -> None:
        nonlocal termination_signal
        termination_signal = int(signum)
        if process is not None:
            _terminate_child(process)

    signal.signal(signal.SIGTERM, handle_termination)
    signal.signal(signal.SIGINT, handle_termination)
    try:
        _request_parent_death_signal()
    except OSError as exc:
        print(json.dumps(_failure("parent_death_signal_failed", str(exc))))
        return 70
    try:
        envelope = json.load(sys.stdin)
        runtime_python = Path(str(envelope["runtime_python"])).resolve()
        project_root = Path(str(envelope["project_root"])).resolve()
        reservation_id = str(envelope["distributed_reservation_id"])
        payload = dict(envelope["payload"])
        environment = {
            str(key): str(value)
            for key, value in dict(envelope.get("environment") or {}).items()
        }
    except (KeyError, TypeError, ValueError, json.JSONDecodeError) as exc:
        print(json.dumps(_failure("invalid_remote_envelope", str(exc))))
        return 64
    if not runtime_python.is_file():
        print(
            json.dumps(
                _failure(
                    "remote_runtime_missing",
                    f"Runtime Python does not exist on compute node: {runtime_python}",
                )
            )
        )
        return 69
    try:
        scratch_directory = prepare_remote_scratch(
            environment, job_token=reservation_id
        )
    except (OSError, ValueError) as exc:
        print(json.dumps(_failure("remote_scratch_setup_failed", str(exc))))
        return 73
    try:
        process = subprocess.Popen(
            [str(runtime_python), "-m", "chemistry_toolbox.src.worker_launcher"],
            text=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=project_root,
            env={**os.environ, **environment},
            start_new_session=os.name == "posix",
        )
        if termination_signal:
            _terminate_child(process)
        stdout, stderr = process.communicate(json.dumps(payload, ensure_ascii=False))
        returncode = process.returncode
    except OSError as exc:
        print(json.dumps(_failure("remote_worker_start_failed", str(exc))))
        return 70
    finally:
        if process is not None and process.poll() is None:
            _terminate_child(process)
        cleanup_remote_scratch(scratch_directory)
    if termination_signal:
        return 128 + termination_signal
    try:
        result = json.loads(stdout.strip().splitlines()[-1])
    except (json.JSONDecodeError, IndexError):
        result = _failure(
            "invalid_remote_worker_response",
            "Remote backend worker did not return a JSON object",
            stdout=stdout[-2000:],
            stderr=stderr[-2000:],
            returncode=returncode,
        )
    if stderr.strip():
        result.setdefault("worker_stderr", stderr[-4000:])
    result.setdefault("worker_returncode", returncode)
    provenance = dict(result.get("provenance") or {})
    provenance["scratch_isolation"] = environment.get(
        "RESEARCHCHEM_DISTRIBUTED_SCRATCH_ISOLATION",
        "worker_local_ephemeral",
    )
    result["provenance"] = provenance
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
