"""Supervised pool of independent MinerU sandboxes.

Each slot owns one sandbox and executes one MinerU job at a time.  The pool
keeps the requested number of idle/working slots, replaces an idle sandbox
that was reclaimed by the control plane, and retries a failed paper once.
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
        startup_concurrency: int = 8,
        supervisor_interval_seconds: float = 15.0,
        max_attempts: int = 2,
        retry_delay_seconds: float = 5.0,
    ) -> None:
        self.options = options.validated()
        self.count = max(1, int(count))
        self.state_root = state_root.expanduser().resolve()
        self.startup_concurrency = max(1, min(int(startup_concurrency), self.count))
        self.supervisor_interval_seconds = max(5.0, float(supervisor_interval_seconds))
        self.max_attempts = max(1, int(max_attempts))
        self.retry_delay_seconds = max(0.0, float(retry_delay_seconds))
        self._slots: queue.Queue[dict[str, Any]] = queue.Queue()
        self._records: list[dict[str, Any]] = []
        self._slot_lock = threading.RLock()
        self._state_lock = threading.Lock()
        self._supervisor_stop = threading.Event()
        self._supervisor_thread: threading.Thread | None = None
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
        with self._slot_lock:
            return [slot["worker"] for slot in self._records if slot.get("worker") is not None]

    def start(self) -> None:
        if self._started:
            return
        self.state_root.mkdir(parents=True, exist_ok=True)
        # Create one environment with capacity=N, then create N instances
        # from that environment.  Each instance still gets an isolated source
        # and inventory file so lifecycle recovery remains independent.
        base_source = self.state_root / "environment.yaml"
        base_inventory = self.state_root / "environment.json"
        base_spec = SandboxRunOptions(
            **{**self.options.__dict__, "name_suffix": "-mineru-pool",
               "instance_capacity": self.count, "source": base_source,
               "inventory": base_inventory}
        )
        base_manager = SandboxManager(base_spec)
        first_worker = base_manager.ensure()
        environment_id = first_worker.environment_id
        specs: list[SandboxRunOptions] = []
        for index in range(1, self.count):
            suffix = f"-mineru-pool-{index + 1:03d}"
            spec = SandboxRunOptions(
                **{**self.options.__dict__, "name_suffix": suffix,
                   "instance_capacity": self.count,
                   "fixed_environment_id": environment_id,
                   "source": self.state_root / f"sandbox-{index + 1:03d}.yaml",
                   "inventory": self.state_root / f"sandbox-{index + 1:03d}.json"}
            )
            # Seed the source with the already-created shared environment. The
            # manager will create only the missing sandbox instance.
            spec.source.parent.mkdir(parents=True, exist_ok=True)
            spec_manager = SandboxManager(spec)
            spec_manager._write_source(spec_manager._source_template(
                environment_id=environment_id, sandbox_id=""
            ))
            specs.append(spec)

        def ensure(spec: SandboxRunOptions):
            manager = SandboxManager(spec)
            worker = manager.ensure()
            return manager, worker, worker.client()

        # A small startup fan-out avoids flooding the control plane while still
        # booting a large pool concurrently.
        with ThreadPoolExecutor(max_workers=self.startup_concurrency) as executor:
            slots = [(base_manager, first_worker, first_worker.client())]
            slots.extend(executor.map(ensure, specs))
        with self._slot_lock:
            self._records = [
                {"index": i, "manager": manager, "worker": worker, "client": client,
                 "busy": False, "dead": False}
                for i, (manager, worker, client) in enumerate(slots, start=1)
            ]
            for slot in self._records:
                self._slots.put(slot)
        self._started = True
        self._write_state()
        self._supervisor_stop.clear()
        self._supervisor_thread = threading.Thread(
            target=self._supervise, name="mineru-sandbox-supervisor", daemon=True
        )
        self._supervisor_thread.start()

    def stop(self) -> None:
        with self._stop_lock:
            if not self._started and not self._records:
                return
            self._supervisor_stop.set()
            thread = self._supervisor_thread
            if thread and thread is not threading.current_thread():
                thread.join(timeout=max(5.0, self.supervisor_interval_seconds + 2))
            with self._slot_lock:
                records = list(self._records)
            for slot in records:
                try:
                    slot["manager"].cleanup()
                except Exception:
                    continue
            self._write_state(stopped=True)
            with self._slot_lock:
                self._records = []
            self._started = False
            self._supervisor_thread = None

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
        last: dict[str, Any] = {"status": "failed", "error": {"message": "not attempted"}}
        for attempt in range(1, self.max_attempts + 1):
            if attempt > 1 and self.retry_delay_seconds:
                time.sleep(self.retry_delay_seconds)
            try:
                result = self._run_once(
                    item, target, command=command, method=method, backend=backend,
                    timeout_seconds=timeout_seconds, environment=environment,
                    extra_args=extra_args,
                )
            except Exception as exc:  # defensive isolation for one paper
                result = {
                    "status": "failed",
                    "error": {"error_type": type(exc).__name__, "message": str(exc)},
                }
            result["attempt"] = attempt
            result["max_attempts"] = self.max_attempts
            result["retry_count"] = attempt - 1
            last = result
            if str(result.get("status")) in {"success", "reused"}:
                return result
        return last

    def _run_once(self, item, target, *, command, method, backend, timeout_seconds,
                  environment, extra_args) -> dict[str, Any]:
        slot = self._slots.get()
        with self._slot_lock:
            slot["busy"] = True
        manager = slot["manager"]
        worker = slot["worker"]
        client = slot["client"]
        job_id = f"mineru-{uuid.uuid4().hex}"
        started = time.monotonic()
        try:
            client.proxy_json(
                "POST", port=worker.rpc_port,
                suffix=f"v1/mineru/jobs/{job_id}/start",
                payload={
                    "source_path": str(Path(item["source_path"]).expanduser().resolve()),
                    "command": command, "method": method, "backend": backend,
                    "timeout_seconds": timeout_seconds,
                    "environment": dict(environment or {}),
                    "extra_args": list(extra_args or []),
                }, timeout=30,
            )
            deadline = time.monotonic() + timeout_seconds + 300
            snapshot: dict[str, Any] = {}
            while time.monotonic() < deadline:
                snapshot = client.proxy_json(
                    "GET", port=worker.rpc_port,
                    suffix=f"v1/mineru/jobs/{job_id}/status", timeout=30,
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
                    client.download(port=worker.rpc_port,
                                    suffix=f"v1/mineru/jobs/{job_id}/archive",
                                    destination=Path(handle.name), timeout=3600)
                    _extract_archive(Path(handle.name), target)
            return {
                "status": str(job.get("status") or "failed"),
                "return_code": job.get("return_code"), "error": job.get("error"),
                "stdout_tail": str(snapshot.get("stdout_tail") or ""),
                "stderr_tail": str(snapshot.get("stderr_tail") or ""),
                "duration_seconds": job.get("duration_seconds") or round(time.monotonic() - started, 3),
                "sandbox_id": worker.sandbox_id,
            }
        except SandboxError:
            self._mark_dead(slot)
            raise
        except Exception:
            raise
        finally:
            try:
                client.proxy_json("DELETE", port=worker.rpc_port,
                                  suffix=f"v1/mineru/jobs/{job_id}", timeout=30)
            except Exception:
                pass
            with self._slot_lock:
                slot["busy"] = False
                if not slot.get("dead") and self._started:
                    self._slots.put(slot)
            self._write_state()

    def _mark_dead(self, slot: dict[str, Any]) -> None:
        with self._slot_lock:
            slot["dead"] = True

    def _supervise(self) -> None:
        while not self._supervisor_stop.wait(self.supervisor_interval_seconds):
            with self._slot_lock:
                records = list(self._records)
            replacements = []
            for slot in records:
                if slot.get("busy"):
                    continue
                unhealthy = bool(slot.get("dead"))
                if not unhealthy:
                    try:
                        detail = slot["manager"].status().get("sandbox") or {}
                        unhealthy = str((detail.get("status") or {}).get("state") or "") != "Running"
                        if not unhealthy:
                            slot["client"].proxy_json("GET", port=slot["worker"].rpc_port,
                                                      suffix="health", timeout=5)
                    except Exception:
                        unhealthy = True
                if unhealthy:
                    replacements.append(slot)
            for slot in replacements:
                self._replace_slot(slot)
            if replacements:
                self._write_state()

    def _replace_slot(self, slot: dict[str, Any]) -> None:
        with self._slot_lock:
            slot["dead"] = True
        # Idle slots live in the work queue. Remove the stale reference before
        # re-adding the recovered slot, otherwise one sandbox could be leased
        # to two documents concurrently.
        with self._slots.mutex:
            queued = [candidate for candidate in self._slots.queue if candidate is not slot]
            self._slots.queue.clear()
            self._slots.queue.extend(queued)
        try:
            worker = slot["manager"].ensure()
            client = worker.client()
        except Exception:
            with self._slot_lock:
                slot["dead"] = True
            return
        with self._slot_lock:
            slot.update(worker=worker, client=client, busy=False, dead=False)
            self._slots.put(slot)

    def _write_state(self, *, stopped: bool = False) -> None:
        with self._slot_lock:
            records = list(self._records)
        payload = {
            "schema_version": 2, "count": self.count,
            "cpu": self.options.cpu, "memory": self.options.memory,
            "stopped": stopped, "supervision": {"interval_seconds": self.supervisor_interval_seconds,
                                                   "max_attempts": self.max_attempts,
                                                   "retry_delay_seconds": self.retry_delay_seconds},
            "sandboxes": [
                {"slot": slot["index"],
                 "sandbox_id": getattr(slot.get("worker"), "sandbox_id", None),
                 "environment_id": getattr(slot.get("worker"), "environment_id", None),
                 "state": getattr(slot.get("worker"), "state", None),
                 "busy": bool(slot.get("busy")), "dead": bool(slot.get("dead"))}
                for slot in records
            ],
        }
        path = self.state_root / "pool.json"
        temporary = path.with_suffix(".json.tmp")
        with self._state_lock:
            temporary.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
            temporary.replace(path)


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
