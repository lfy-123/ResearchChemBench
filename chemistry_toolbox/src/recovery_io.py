"""Local-host recovery primitives. Control files live outside the Agent workspace."""
from __future__ import annotations

import fcntl
import ctypes
import hashlib
import json
import os
import socket
import signal
import uuid
from contextlib import contextmanager
from pathlib import Path


def control_directory(workspace: Path, run_id: str) -> Path:
    workspace = Path(workspace).resolve()
    suffix = "" if workspace.name == run_id else "-" + hashlib.sha256(str(workspace).encode()).hexdigest()[:12]
    return workspace.parent / ".rcb_recovery" / (run_id + suffix)


def atomic_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + "." + uuid.uuid4().hex + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(value, handle, ensure_ascii=False, sort_keys=True)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temporary, path)
    descriptor = os.open(path.parent, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


@contextmanager
def file_lock(path: Path, *, blocking: bool = True):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a+") as handle:
        fcntl.flock(handle, fcntl.LOCK_EX | (0 if blocking else fcntl.LOCK_NB))
        try:
            yield handle
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)


def file_hash(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def process_identity(pid: int | None, expected: dict | None = None) -> dict:
    identity = {"pid": pid, "host": socket.gethostname(), "alive": False, "verified": False}
    if not isinstance(pid, int) or pid <= 0:
        return {**identity, "reason": "missing_pid"}
    try:
        identity["boot_id"] = Path("/proc/sys/kernel/random/boot_id").read_text().strip()
        stat = Path(f"/proc/{pid}/stat").read_text()
        fields = stat[stat.rfind(")") + 2:].split()
        identity.update(start_ticks=int(fields[19]), pgid=int(fields[2]), alive=fields[0] not in {"Z", "X"})
    except (OSError, ValueError, IndexError):
        return {**identity, "reason": "process_missing"}
    matches = expected is None or all(expected.get(k) == identity.get(k) for k in ("host", "boot_id", "pid", "start_ticks"))
    if matches and expected and expected.get("launch_token"):
        try:
            marker = ("RCB_JOB_LAUNCH_TOKEN=" + expected["launch_token"]).encode()
            matches = marker in Path(f"/proc/{pid}/environ").read_bytes().split(b"\0")
        except OSError:
            matches = False
        if not matches:
            identity["reason"] = "launch_token_unverified"
    identity["verified"] = identity["alive"] and matches
    if not matches and "reason" not in identity:
        identity["reason"] = "process_identity_mismatch"
    return identity


def token_processes(token: str, *, variable: str = "RCB_JOB_LAUNCH_TOKEN") -> list[dict]:
    """Locate surviving descendants, including a child whose supervisor died.

    Only inspect processes of this uid. Never log their environment.
    """
    marker = (variable + "=" + token).encode()
    found = []
    for path in Path("/proc").glob("[0-9]*/environ"):
        try:
            values = path.read_bytes().split(b"\0") if path.stat().st_uid == os.getuid() else []
            if marker not in values:
                continue
            if variable == "RCB_AGENT_RUN_TOKEN" and any(value.startswith(b"RCB_JOB_LAUNCH_TOKEN=") for value in values):
                continue  # Computation belongs to the run, never to the Agent.
            identity = process_identity(int(path.parent.name))
            if identity["verified"]:
                found.append(identity)
        except (OSError, ValueError):
            continue
    return found


def signal_identity(identity: dict, sig=signal.SIGTERM) -> bool:
    """Pin a Linux process before checking identity, closing the PID reuse race."""
    pid = identity.get("pid")
    if not isinstance(pid, int): return False
    # Some conda Python builds omit the wrappers even on a capable kernel.
    # Linux uses these syscall numbers on the supported local architectures.
    libc = ctypes.CDLL(None, use_errno=True)
    if os.uname().machine not in {"x86_64", "aarch64", "riscv64"}:
        return False
    descriptor = libc.syscall(434, pid, 0)  # pidfd_open
    if descriptor < 0: return False
    try:
        if not process_identity(pid, identity).get("verified"): return False
        return libc.syscall(424, descriptor, int(sig), 0, 0) == 0  # pidfd_send_signal
    except (OSError, AttributeError):
        return False
    finally:
        os.close(descriptor)
