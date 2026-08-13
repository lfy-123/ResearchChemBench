"""Opt-in pool of independent MinerU sandboxes.

The normal pipeline still uses :class:`SandboxPipelineRuntime` and one sandbox.
This module is intentionally small and only implements the RPC contract needed
by Stage04. A pool slot owns one sandbox and therefore executes one MinerU job
at a time; the queue of slots provides bounded cross-document parallelism.
"""

from __future__ import annotations

import json
import queue
import shutil
import tarfile
import tempfile
import threading
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

from src.sandbox.control import SandboxError
from src.sandbox.manager import SandboxManager, SandboxRunOptions, SandboxWorker


class MineruSandboxPool:
    """Manage N sandboxes and expose the runtime ``run_mineru`` interface."""

    def __init__(
        self,
        *,
        options: SandboxRunOptions,
        count: int,
        state_root: Path,
    ) -> None:
        self.options = options.validated()
        self.count = max(1, int(count))
        self.state_root = state_root.expanduser().resolve()
        self._slots: queue.Queue[tuple[SandboxManager, SandboxWorker, Any]] = queue.Queue()
        self._managers: list[SandboxManager] = []
        self._started = False
        self._stop_lock = threading.Lock()

    def __enter__(self) -> "MineruSandboxPool":
        self.start()
        return self

    def __exit__(self, exc_type, exc, traceback) -> bool:
        self.stop()
        return False

    @property
    def workers(self) -> list[SandboxWorker]:
        return [slot[1] for slot in list(self._slots.queue)]

    def start(self) -> None:
        if self._started:
            return
        self.state_root.mkdir(parents=True, exist_ok=True)
        specs = []
        for index in range(self.count):
            suffix = f"-mineru-pool-{index + 1:03d}"
            specs.append(
                SandboxRunOptions(
                    **{
                        **self.options.__dict__,
                        "name_suffix": suffix,
                        "source": self.state_root / f"sandbox-{index + 1:03d}.yaml",
                        "inventory": self.state_root / f"sandbox-{index + 1:03d}.json",
                    }
                )
            )
        # Startup is parallel so a larger pool does not serialize sandbox boot.
        def ensure(spec: SandboxRunOptions):
            manager = SandboxManager(spec)
            worker = manager.ensure()
            return manager, worker, worker.client()

        with ThreadPoolExecutor(max_workers=self.count) as executor:
            slots = list(executor.map(ensure, specs))
        self._managers = [slot[0] for slot in slots]
        for slot in slots:
            self._slots.put(slot)
        self._write_state()
        self._started = True

    def stop(self) -> None:
        with self._stop_lock:
            if not self._managers:
                return
            # ``stop`` is deliberately best-effort: completed results must not
            # be lost because one expired sandbox cannot be contacted.
            for manager in self._managers:
                try:
                    manager.cleanup()
                except Exception:
                    continue
            self._write_state(stopped=True)
            self._managers = []
            self._started = False

    def run_mineru(
        self,
        item: dict[str, Any],
        target: Path,
        *,
        command: str,
        method: str,
        backend: str | None,
        timeout_seconds: int,
        environment: dict[str, str] | None,
        extra_args: list[str] | None,
    ) -> dict[str, Any]:
        if not self._started:
            raise RuntimeError("MineruSandboxPool is not started")
        manager, worker, client = self._slots.get()
        job_id = f"mineru-{uuid.uuid4().hex}"
        started = time.monotonic()
        try:
            client.proxy_json(
                "POST",
                port=worker.rpc_port,
                suffix=f"v1/mineru/jobs/{job_id}/start",
                payload={
                    "source_path": str(Path(item["source_path"]).expanduser().resolve()),
                    "command": command,
                    "method": method,
                    "backend": backend,
                    "timeout_seconds": timeout_seconds,
                    "environment": dict(environment or {}),
                    "extra_args": list(extra_args or []),
                },
                timeout=30,
            )
            deadline = time.monotonic() + timeout_seconds + 300
            snapshot: dict[str, Any] = {}
            while time.monotonic() < deadline:
                snapshot = client.proxy_json(
                    "GET",
                    port=worker.rpc_port,
                    suffix=f"v1/mineru/jobs/{job_id}/status",
                    timeout=30,
                )
                status = str((snapshot.get("job") or {}).get("status") or "")
                if status in {"success", "failed", "timeout"}:
                    break
                time.sleep(2)
            else:
                raise TimeoutError(f"sandbox MinerU job {job_id} did not finish")
            job = dict(snapshot.get("job") or {})
            if job.get("status") == "success":
                target.parent.mkdir(parents=True, exist_ok=True)
                with tempfile.NamedTemporaryFile(suffix=".tar.gz") as handle:
                    client.download(
                        port=worker.rpc_port,
                        suffix=f"v1/mineru/jobs/{job_id}/archive",
                        destination=Path(handle.name),
                        timeout=3600,
                    )
                    _extract_archive(Path(handle.name), target)
            return {
                "status": str(job.get("status") or "failed"),
                "return_code": job.get("return_code"),
                "error": job.get("error"),
                "stdout_tail": str(snapshot.get("stdout_tail") or ""),
                "stderr_tail": str(snapshot.get("stderr_tail") or ""),
                "duration_seconds": job.get("duration_seconds")
                or round(time.monotonic() - started, 3),
                "sandbox_id": worker.sandbox_id,
            }
        except Exception as exc:
            return {
                "status": "failed",
                "error": {"error_type": type(exc).__name__, "message": str(exc)},
                "duration_seconds": round(time.monotonic() - started, 3),
                "sandbox_id": worker.sandbox_id,
            }
        finally:
            try:
                client.proxy_json(
                    "DELETE",
                    port=worker.rpc_port,
                    suffix=f"v1/mineru/jobs/{job_id}",
                    timeout=30,
                )
            except Exception:
                pass
            self._slots.put((manager, worker, client))

    def _write_state(self, *, stopped: bool = False) -> None:
        payload = {
            "schema_version": 1,
            "count": self.count,
            "cpu": self.options.cpu,
            "memory": self.options.memory,
            "stopped": stopped,
            "sandboxes": [
                {
                    "sandbox_id": worker.sandbox_id,
                    "environment_id": worker.environment_id,
                    "state": worker.state,
                }
                for _manager, worker, _client in list(self._slots.queue)
            ],
        }
        path = self.state_root / "pool.json"
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _extract_archive(archive_path: Path, target: Path) -> None:
    staging = target.parent / f".{target.name}.sandbox-download"
    shutil.rmtree(staging, ignore_errors=True)
    staging.mkdir(parents=True, exist_ok=True)
    root = staging.resolve()
    with tarfile.open(archive_path, "r:gz") as archive:
        for member in archive.getmembers():
            if member.issym() or member.islnk():
                raise SandboxError("sandbox MinerU archive contains links")
            destination = (staging / member.name).resolve()
            if destination != root and root not in destination.parents:
                raise SandboxError(f"sandbox MinerU archive escapes destination: {member.name}")
        archive.extractall(staging)
    downloaded = staging / "output"
    if not downloaded.is_dir():
        raise SandboxError("sandbox MinerU archive is missing output directory")
    if target.exists():
        shutil.rmtree(target)
    downloaded.rename(target)
    shutil.rmtree(staging, ignore_errors=True)


__all__ = ["MineruSandboxPool"]
