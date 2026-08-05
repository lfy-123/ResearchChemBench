from __future__ import annotations

import contextlib
import shutil
import tarfile
import tempfile
import time
import uuid
from pathlib import Path
from typing import Any, Iterator

from src.sandbox.control import SandboxError
from src.sandbox.manager import SERVICE_PORTS, SandboxManager, SandboxRunOptions, SandboxWorker
from src.sandbox.proxy import LocalSandboxProxy


class SandboxPipelineRuntime:
    """One pipeline run sharing one managed OpenSandbox instance."""

    def __init__(self, options: SandboxRunOptions) -> None:
        self.options = options.validated()
        self.manager = SandboxManager(self.options)
        self.worker: SandboxWorker | None = None
        self.client = None
        self.proxies: dict[str, LocalSandboxProxy] = {}

    def __enter__(self) -> SandboxPipelineRuntime:
        self.worker = self.manager.ensure()
        self.client = self.worker.client()
        for name in ("grobid", "softcite", "quantities"):
            self.proxies[name] = LocalSandboxProxy(
                self.client,
                remote_port=SERVICE_PORTS[name],
                request_timeout=1800 if name in {"grobid", "softcite"} else 300,
            ).start()
        return self

    def __exit__(self, exc_type, exc, traceback) -> bool:
        for name in list(self.proxies):
            try:
                self.stop_service(name)
            except Exception:
                pass
        for proxy in self.proxies.values():
            proxy.close()
        self.proxies.clear()
        self.manager.cleanup()
        return False

    def apply(self, config: dict[str, Any]) -> dict[str, Any]:
        service_configs = {
            "grobid": config.get("grobid_extract", {}),
            "softcite": config.get("software_coverage", {}),
            "quantities": config.get("grobid_quantities", {}),
        }
        for name, service_config in service_configs.items():
            service_config["base_url"] = self.proxies[name].base_url
            service_config["_sandbox_runtime"] = self
        mineru = config.setdefault("mineru", {})
        mineru.setdefault("environment", {})["_sandbox_runtime"] = self
        config["execution_backend"] = "sandbox"
        return config

    @contextlib.contextmanager
    def service(self, name: str, config: dict[str, Any]) -> Iterator[None]:
        self.start_service(name, config)
        try:
            yield
        finally:
            self._mirror_service_log(name, config)
            self.stop_service(name)

    def start_service(self, name: str, config: dict[str, Any]) -> dict[str, Any]:
        client = self._client()
        response = client.proxy_json(
            "POST",
            port=SERVICE_PORTS["rpc"],
            suffix=f"v1/services/{name}/start",
            payload={"environment": dict(config.get("environment") or {})},
            timeout=float(config.get("startup_timeout_seconds") or 1200) + 120,
        )
        if not response.get("healthy"):
            raise SandboxError(f"sandbox service {name} did not become healthy: {response}")
        return response

    def stop_service(self, name: str) -> None:
        if self.client is None:
            return
        try:
            self.client.proxy_json(
                "POST",
                port=SERVICE_PORTS["rpc"],
                suffix=f"v1/services/{name}/stop",
                payload={},
                timeout=60,
            )
        except SandboxError:
            pass

    def service_healthy(self, name: str) -> bool:
        try:
            response = self._client().proxy_json(
                "GET",
                port=SERVICE_PORTS["rpc"],
                suffix=f"v1/services/{name}/status",
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
        client = self._client()
        job_id = f"mineru-{uuid.uuid4().hex}"
        client.proxy_json(
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
            snapshot = client.proxy_json(
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
                client.download(
                    port=SERVICE_PORTS["rpc"],
                    suffix=f"v1/mineru/jobs/{job_id}/archive",
                    destination=Path(handle.name),
                )
                self._extract_archive(Path(handle.name), target)
        try:
            client.proxy_json(
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

    def _mirror_service_log(self, name: str, config: dict[str, Any]) -> None:
        log_path = config.get("service_log")
        if not log_path or self.client is None:
            return
        try:
            response = self.client.proxy_json(
                "GET",
                port=SERVICE_PORTS["rpc"],
                suffix=f"v1/services/{name}/logs",
                timeout=30,
            )
            destination = Path(str(log_path)).expanduser().resolve()
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(str(response.get("log") or ""), encoding="utf-8")
        except SandboxError:
            return

    def _client(self):
        if self.client is None:
            raise RuntimeError("sandbox runtime is not active")
        return self.client


def os_replace_directory(source: Path, destination: Path) -> None:
    source.rename(destination)


__all__ = ["SandboxPipelineRuntime"]
