from __future__ import annotations

import contextlib
import fcntl
import shutil
import tarfile
import tempfile
import threading
import time
import uuid
from pathlib import Path
from typing import Any, Iterator

from src.sandbox.control import SandboxError
from src.sandbox.manager import (
    SERVICE_PORTS,
    SandboxManager,
    SandboxRunOptions,
    SandboxWorker,
    service_instance_ports,
)
from src.sandbox.proxy import LocalSandboxProxy


class SandboxPipelineRuntime:
    """One pipeline run sharing one managed OpenSandbox instance."""

    def __init__(self, options: SandboxRunOptions) -> None:
        self.options = options.validated()
        self.manager = SandboxManager(self.options)
        self.worker: SandboxWorker | None = None
        self.client = None
        self.proxies: dict[tuple[str, int], LocalSandboxProxy] = {}
        self._service_references: dict[tuple[str, int], int] = {}
        self._started_services: set[tuple[str, int]] = set()
        self._service_configs: dict[tuple[str, int], dict[str, Any]] = {}
        self._service_lock = threading.RLock()
        self._recovery_lock = threading.RLock()
        self._lock_handle = None

    def __enter__(self) -> SandboxPipelineRuntime:
        lock_path = self.manager.source_path.parent / ".sandbox_state" / "active.lock"
        lock_path.parent.mkdir(parents=True, exist_ok=True)
        self._lock_handle = lock_path.open("a+", encoding="utf-8")
        try:
            fcntl.flock(self._lock_handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            self._lock_handle.close()
            self._lock_handle = None
            raise RuntimeError("another data pipeline run is already using the sandbox") from exc
        try:
            self.worker = self.manager.ensure_with_retry()
            self.client = self.worker.client()
            for name in ("grobid", "softcite", "quantities"):
                self._proxy(name, 0)
        except Exception:
            self._release_lock()
            raise
        return self

    def __exit__(self, exc_type, exc, traceback) -> bool:
        for name, instance in list(self._started_services):
            try:
                config = self._service_configs.get((name, instance))
                if config is not None:
                    self._mirror_service_log(name, config, instance=instance)
                if self.options.cleanup != "keep":
                    self.stop_service(name, instance=instance)
            except Exception:
                pass
        for proxy in self.proxies.values():
            proxy.close()
        self.proxies.clear()
        try:
            self.manager.cleanup()
        finally:
            self._release_lock()
        return False

    def apply(self, config: dict[str, Any]) -> dict[str, Any]:
        service_configs = {
            "grobid": config.get("grobid_extract", {}),
            "softcite": config.get("software_coverage", {}),
            "quantities": config.get("grobid_quantities", {}),
        }
        for name, service_config in service_configs.items():
            service_config.update(self.service_config(name, service_config, instance=0))
        mineru = config.setdefault("mineru", {})
        mineru.setdefault("environment", {})["_sandbox_runtime"] = self
        config["execution_backend"] = "sandbox"
        return config

    def service_config(
        self, name: str, config: dict[str, Any], *, instance: int = 0
    ) -> dict[str, Any]:
        prepared = dict(config)
        prepared["environment"] = dict(config.get("environment") or {})
        prepared["base_url"] = self._proxy(name, instance).base_url
        prepared["_sandbox_runtime"] = self
        prepared["_sandbox_instance"] = instance
        if instance and prepared.get("service_log"):
            path = Path(str(prepared["service_log"]))
            prepared["service_log"] = str(
                path.with_name(f"{path.stem}.instance-{instance:03d}{path.suffix}")
            )
        return prepared

    @contextlib.contextmanager
    def service(self, name: str, config: dict[str, Any]) -> Iterator[None]:
        instance = int(config.get("_sandbox_instance", 0))
        key = (name, instance)
        with self._service_lock:
            references = self._service_references.get(key, 0)
            if references == 0 and key not in self._started_services:
                self.start_service(name, config, instance=instance)
            self._service_references[key] = references + 1
        try:
            yield
        finally:
            with self._service_lock:
                remaining = self._service_references.get(key, 1) - 1
                if remaining > 0:
                    self._service_references[key] = remaining
                else:
                    self._service_references.pop(key, None)
                    self._mirror_service_log(name, config, instance=instance)

    def start_service(
        self, name: str, config: dict[str, Any], *, instance: int = 0
    ) -> dict[str, Any]:
        response = self._proxy_json(
            "POST",
            port=SERVICE_PORTS["rpc"],
            suffix=self._service_suffix(name, instance, "start"),
            payload={"environment": dict(config.get("environment") or {})},
            timeout=float(config.get("startup_timeout_seconds") or 1200) + 120,
        )
        if not response.get("healthy"):
            raise SandboxError(
                f"sandbox service {name} instance {instance} did not become healthy: {response}"
            )
        with self._service_lock:
            self._started_services.add((name, instance))
            self._service_configs[(name, instance)] = config
        return response

    def stop_service(self, name: str, *, instance: int = 0) -> None:
        if self.client is None:
            return
        try:
            self.client.proxy_json(
                "POST",
                port=SERVICE_PORTS["rpc"],
                suffix=self._service_suffix(name, instance, "stop"),
                payload={},
                timeout=60,
            )
        except SandboxError:
            pass
        finally:
            with self._service_lock:
                self._started_services.discard((name, instance))
                self._service_configs.pop((name, instance), None)

    def service_healthy(self, name: str, *, instance: int = 0) -> bool:
        try:
            response = self._proxy_json(
                "GET",
                port=SERVICE_PORTS["rpc"],
                suffix=self._service_suffix(name, instance, "status"),
                timeout=10,
            )
            return bool(response.get("healthy"))
        except SandboxError:
            return False

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
        job_id = f"mineru-{uuid.uuid4().hex}"
        self._proxy_json(
            "POST",
            port=SERVICE_PORTS["rpc"],
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
            snapshot = self._proxy_json(
                "GET",
                port=SERVICE_PORTS["rpc"],
                suffix=f"v1/mineru/jobs/{job_id}/status",
                timeout=30,
            )
            job = dict(snapshot.get("job") or {})
            if job.get("status") in {"success", "failed", "timeout"}:
                break
            time.sleep(2)
        else:
            raise TimeoutError(f"sandbox MinerU job {job_id} did not finish")
        job = dict(snapshot.get("job") or {})
        if job.get("status") == "success":
            target.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(suffix=".tar.gz") as handle:
                self._download(
                    port=SERVICE_PORTS["rpc"],
                    suffix=f"v1/mineru/jobs/{job_id}/archive",
                    destination=Path(handle.name),
                )
                self._extract_archive(Path(handle.name), target)
        try:
            self._proxy_json(
                "DELETE",
                port=SERVICE_PORTS["rpc"],
                suffix=f"v1/mineru/jobs/{job_id}",
                timeout=30,
            )
        except SandboxError:
            pass
        return {
            "status": str(job.get("status") or "failed"),
            "return_code": job.get("return_code"),
            "error": job.get("error"),
            "stdout_tail": str(snapshot.get("stdout_tail") or ""),
            "stderr_tail": str(snapshot.get("stderr_tail") or ""),
            "duration_seconds": job.get("duration_seconds"),
            "sandbox_id": self.worker.sandbox_id if self.worker else None,
        }

    @staticmethod
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
        os_replace_directory(downloaded, target)
        shutil.rmtree(staging, ignore_errors=True)

    def _mirror_service_log(self, name: str, config: dict[str, Any], *, instance: int = 0) -> None:
        log_path = config.get("service_log")
        if not log_path or self.client is None:
            return
        try:
            response = self.client.proxy_json(
                "GET",
                port=SERVICE_PORTS["rpc"],
                suffix=self._service_suffix(name, instance, "logs"),
                timeout=30,
            )
            destination = Path(str(log_path)).expanduser().resolve()
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(str(response.get("log") or ""), encoding="utf-8")
        except SandboxError:
            return

    def _proxy(self, name: str, instance: int) -> LocalSandboxProxy:
        key = (name, instance)
        proxy = self.proxies.get(key)
        if proxy is not None:
            return proxy
        remote_port, _admin_port = service_instance_ports(name, instance)
        proxy = LocalSandboxProxy(
            self._client(),
            remote_port=remote_port,
            request_timeout=1800 if name in {"grobid", "softcite"} else 300,
            recover_client=self._recover_proxy_client,
        ).start()
        self.proxies[key] = proxy
        return proxy

    @staticmethod
    def _service_suffix(name: str, instance: int, operation: str) -> str:
        if instance == 0:
            return f"v1/services/{name}/{operation}"
        return f"v1/services/{name}/instances/{instance}/{operation}"

    def _client(self):
        if self.client is None:
            raise RuntimeError("sandbox runtime is not active")
        return self.client

    def _proxy_json(self, method: str, **kwargs) -> dict[str, Any]:
        try:
            return self._client().proxy_json(method, **kwargs)
        except SandboxError as exc:
            if not self._sandbox_unavailable(exc.status, exc.response.encode("utf-8")):
                raise
            client = self._recover_sandbox()
            return client.proxy_json(method, **kwargs)

    def _download(self, **kwargs) -> None:
        try:
            self._client().download(**kwargs)
        except SandboxError as exc:
            if not self._sandbox_unavailable(exc.status, exc.response.encode("utf-8")):
                raise
            self._recover_sandbox().download(**kwargs)

    def _recover_proxy_client(self, status: int, payload: bytes):
        if not self._sandbox_unavailable(status, payload):
            return None
        return self._recover_sandbox()

    @staticmethod
    def _sandbox_unavailable(status: int | None, payload: bytes) -> bool:
        if status not in {403, 409, 502, 503}:
            return False
        detail = payload.decode("utf-8", errors="replace").casefold()
        return "sandbox" in detail and (
            "not running" in detail
            or "status: pending" in detail
            or "status pending" in detail
        )

    def _recover_sandbox(self):
        """Wait for a displaced sandbox and restore its RPC and managed services once."""
        with self._recovery_lock:
            # A concurrent request may already have completed recovery.
            try:
                health = self._client().proxy_json(
                    "GET", port=SERVICE_PORTS["rpc"], suffix="health", timeout=5
                )
                if health.get("status") == "success":
                    return self._client()
            except SandboxError:
                pass

            worker = self.manager.ensure()
            self.worker = worker
            self.client = worker.client()
            for proxy in self.proxies.values():
                proxy.server.client = self.client

            services = [
                (key, self._service_configs[key])
                for key in sorted(self._started_services)
                if key in self._service_configs
            ]
            self._started_services.clear()
            for (name, instance), config in services:
                self.start_service(name, config, instance=instance)
            return self.client

    def _release_lock(self) -> None:
        if self._lock_handle is None:
            return
        fcntl.flock(self._lock_handle.fileno(), fcntl.LOCK_UN)
        self._lock_handle.close()
        self._lock_handle = None


def os_replace_directory(source: Path, destination: Path) -> None:
    source.rename(destination)


__all__ = ["SandboxPipelineRuntime"]
