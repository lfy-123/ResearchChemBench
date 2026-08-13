from __future__ import annotations

import fcntl
import hashlib
import os
import socket
import threading
import time
import uuid
from pathlib import Path
from typing import Any


def process_identity(pid: int | None = None) -> dict[str, Any]:
    current_pid = int(pid or os.getpid())
    boot_path = Path("/proc/sys/kernel/random/boot_id")
    boot_id = boot_path.read_text(encoding="utf-8").strip() if boot_path.is_file() else "unknown"
    start_ticks = ""
    stat_path = Path(f"/proc/{current_pid}/stat")
    if stat_path.is_file():
        fields = stat_path.read_text(encoding="utf-8", errors="replace").split()
        if len(fields) > 21:
            start_ticks = fields[21]
    return {
        "pid": current_pid,
        "hostname": socket.gethostname(),
        "boot_id": boot_id,
        "process_start_ticks": start_ticks,
    }


def command_hash(argv: list[str]) -> str:
    return hashlib.sha256("\x00".join(argv).encode("utf-8")).hexdigest()


class RunLease:
    """One process lease backed by an OS lock and the resume database."""

    def __init__(
        self,
        store,
        *,
        command_digest: str,
        generation: int,
        heartbeat_seconds: float = 30.0,
    ) -> None:
        self.store = store
        self.command_digest = command_digest
        self.generation = int(generation)
        self.heartbeat_seconds = max(1.0, float(heartbeat_seconds))
        self.owner_id = uuid.uuid4().hex
        self.identity = process_identity()
        self._handle = None
        self._stop = threading.Event()
        self._thread: threading.Thread | None = None

    def __enter__(self):
        lock_path = self.store.root / ".stage00-05-resume.lock"
        lock_path.parent.mkdir(parents=True, exist_ok=True)
        self._handle = lock_path.open("a+", encoding="utf-8")
        try:
            fcntl.flock(self._handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            self._handle.close()
            self._handle = None
            raise RuntimeError(f"another Stage00-05 resume process owns {lock_path}") from exc
        self.store.reconcile_interrupted_work()
        self.store.start_lease(
            owner_id=self.owner_id,
            generation=self.generation,
            command_hash=self.command_digest,
            **self.identity,
        )
        self._thread = threading.Thread(target=self._heartbeat, daemon=True)
        self._thread.start()
        return self

    def __exit__(self, exc_type, exc, traceback) -> None:
        self._stop.set()
        if self._thread is not None:
            self._thread.join(timeout=self.heartbeat_seconds + 2.0)
        status = "completed" if exc_type is None else "interrupted_signal" if exc_type is KeyboardInterrupt else "failed"
        self.store.finish_lease(self.owner_id, status=status)
        if self._handle is not None:
            fcntl.flock(self._handle.fileno(), fcntl.LOCK_UN)
            self._handle.close()
            self._handle = None

    def _heartbeat(self) -> None:
        while not self._stop.wait(self.heartbeat_seconds):
            self.store.heartbeat_lease(self.owner_id)
