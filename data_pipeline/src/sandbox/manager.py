from __future__ import annotations

import json
import os
import re
import shlex
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

from src.sandbox.control import OpenSandboxClient, SandboxError

DATA_PIPELINE_ROOT = Path(__file__).resolve().parents[2]
PROJECT_ROOT = DATA_PIPELINE_ROOT.parent
DEFAULT_SOURCE = DATA_PIPELINE_ROOT / ".sandboxes.local.yaml"
DEFAULT_INVENTORY = DATA_PIPELINE_ROOT / ".sandbox_inventory.local.json"
DEFAULT_BASE_URL = "https://h.pjlab.org.cn/brainbox"
DEFAULT_PROJECT = "ailab-ai4chem"
DEFAULT_IMAGE = "registry.h.pjlab.org.cn/ailab-ai4chem-ai4chem_cpu/base:python312-20260627215752"
DEFAULT_RUNTIME_ROOT = "/tmp/researchchem-data-pipeline"
SERVICE_PORTS = {
    "command": 44772,
    "rpc": 44773,
    "grobid": 8070,
    "softcite": 8060,
    "quantities": 8062,
}
SOFTCITE_POOL_PORT_BASE = 8160
MAX_SOFTCITE_INSTANCES = 16
EXPOSED_SERVICE_PORTS = {
    **SERVICE_PORTS,
    **{
        f"softcite_{instance}": SOFTCITE_POOL_PORT_BASE + (instance - 1) * 2
        for instance in range(1, MAX_SOFTCITE_INSTANCES)
    },
}
WORKER_PROTOCOL_VERSION = 5


def service_instance_ports(name: str, instance: int = 0) -> tuple[int, int]:
    if instance < 0:
        raise ValueError("service instance must be non-negative")
    if name == "softcite" and instance >= MAX_SOFTCITE_INSTANCES:
        raise ValueError(f"softcite supports at most {MAX_SOFTCITE_INSTANCES} instances")
    if instance == 0:
        application = int(SERVICE_PORTS[name])
    elif name == "softcite":
        application = SOFTCITE_POOL_PORT_BASE + (instance - 1) * 2
    else:
        raise ValueError(f"multiple instances are only supported for softcite, not {name}")
    return application, application + 1


@dataclass(frozen=True)
class SandboxRunOptions:
    cpu: int = 32
    memory: str = "96Gi"
    lifecycle_minutes: int = 1440
    startup_timeout_seconds: int = 3600
    cleanup: str = "stop"
    source: Path = DEFAULT_SOURCE
    inventory: Path = DEFAULT_INVENTORY
    base_url: str = DEFAULT_BASE_URL
    project: str = DEFAULT_PROJECT
    image: str = DEFAULT_IMAGE
    api_key_env: str = "RCB_SANDBOX_API_KEY"

    def validated(self) -> SandboxRunOptions:
        if self.cpu < 1:
            raise ValueError("sandbox CPU must be a positive integer")
        if not re.fullmatch(r"[1-9][0-9]*(?:Mi|Gi|Ti)", self.memory):
            raise ValueError("sandbox memory must use Mi, Gi, or Ti, for example 96Gi")
        if not 3 <= self.lifecycle_minutes <= 1440:
            raise ValueError("sandbox lifecycle must be between 3 and 1440 minutes")
        if self.startup_timeout_seconds < 60:
            raise ValueError("sandbox startup timeout must be at least 60 seconds")
        if self.cleanup not in {"keep", "stop", "delete"}:
            raise ValueError("sandbox cleanup must be keep, stop, or delete")
        return self


@dataclass(frozen=True)
class SandboxWorker:
    sandbox_id: str
    environment_id: str
    name: str
    state: str
    expires_at: str
    cpu: int
    memory: str
    base_url: str
    project: str
    api_key_env: str
    command_port: int = SERVICE_PORTS["command"]
    rpc_port: int = SERVICE_PORTS["rpc"]

    def client(self) -> OpenSandboxClient:
        api_key = os.environ.get(self.api_key_env, "").strip()
        if not api_key:
            raise SandboxError(
                f"missing OpenSandbox API key environment variable: {self.api_key_env}",
                retryable=False,
            )
        return OpenSandboxClient(
            base_url=self.base_url,
            project=self.project,
            api_key=api_key,
            sandbox_id=self.sandbox_id,
            command_port=self.command_port,
            rpc_port=self.rpc_port,
        )


class SandboxManager:
    """Create, inspect, renew, stop, and delete one managed pipeline sandbox."""

    def __init__(self, options: SandboxRunOptions) -> None:
        self.options = options.validated()
        self.source_path = self.options.source.expanduser().resolve()
        self.inventory_path = self.options.inventory.expanduser().resolve()
        self._load_environment()
        api_key = os.environ.get(self.options.api_key_env, "").strip()
        if not api_key:
            raise SandboxError(
                f"missing OpenSandbox API key environment variable: {self.options.api_key_env}",
                retryable=False,
            )
        self.control = OpenSandboxClient(
            base_url=self.options.base_url,
            project=self.options.project,
            api_key=api_key,
        )

    @staticmethod
    def _load_environment() -> None:
        for path in (DATA_PIPELINE_ROOT / "config.local.env", PROJECT_ROOT / "config.local.env"):
            if path.is_file():
                load_dotenv(path, override=False)

    def ensure(self) -> SandboxWorker:
        source = self._load_source()
        if source and not self._resources_match(source):
            self._replace_incompatible_pool(source)
            source = {}

        environment_id = str((source.get("environment") or {}).get("environment_id") or "")
        if not environment_id:
            environment = self.control.management_json(
                "POST",
                "/v1/sandbox-environments",
                payload=self._environment_payload(),
                timeout=120,
            )
            environment_id = str(environment["id"])
            source = self._source_template(environment_id=environment_id, sandbox_id="")
            self._write_source(source)

        sandbox_id = str((source.get("worker") or {}).get("sandbox_id") or "")
        detail: dict[str, Any] | None = None
        if sandbox_id:
            try:
                detail = self.control.management_json("GET", f"/v1/sandboxes/{sandbox_id}")
            except SandboxError as exc:
                if exc.status != 404:
                    raise
            if detail:
                state = str((detail.get("status") or {}).get("state") or "")
                if state in {"Pending", "Creating"}:
                    detail = self._wait_running(sandbox_id)
                elif state != "Running":
                    detail = None
                    sandbox_id = ""

        if not sandbox_id:
            response = self.control.management_json(
                "POST",
                "/v1/sandboxes",
                payload={
                    "environmentId": environment_id,
                    "name": f"researchchem-data-pipeline-{self.options.cpu}cpu",
                    "type": "code",
                    "lifecycleMinutes": self.options.lifecycle_minutes,
                    "metadata": {"owner": "researchchem-data-pipeline", "schema_version": "1"},
                },
                timeout=120,
            )
            sandbox_id = str(response["id"])
            source.setdefault("worker", {})["sandbox_id"] = sandbox_id
            self._write_source(source)
            detail = self._wait_running(sandbox_id)

        assert detail is not None
        worker = self._worker_from_detail(detail, environment_id)
        worker = self._ensure_lifecycle(worker)
        self._ensure_worker_rpc(worker)
        self._write_inventory(worker)
        return worker

    def status(self) -> dict[str, Any]:
        source = self._load_source()
        environment_id = str((source.get("environment") or {}).get("environment_id") or "")
        sandbox_id = str((source.get("worker") or {}).get("sandbox_id") or "")
        result: dict[str, Any] = {
            "source": str(self.source_path),
            "inventory": str(self.inventory_path),
            "environment_id": environment_id or None,
            "sandbox_id": sandbox_id or None,
        }
        if environment_id:
            try:
                result["environment"] = _redact_credentials(
                    self.control.management_json(
                        "GET", f"/v1/sandbox-environments/{environment_id}"
                    )
                )
            except SandboxError as exc:
                result["environment_error"] = str(exc)
        if sandbox_id:
            try:
                result["sandbox"] = _redact_credentials(
                    self.control.management_json("GET", f"/v1/sandboxes/{sandbox_id}")
                )
            except SandboxError as exc:
                result["sandbox_error"] = str(exc)
        return result

    def stop(self) -> dict[str, Any]:
        source = self._load_source()
        sandbox_id = str((source.get("worker") or {}).get("sandbox_id") or "")
        if not sandbox_id:
            return {"status": "not_found", "message": "no managed sandbox is recorded"}
        try:
            detail = self.control.management_json("GET", f"/v1/sandboxes/{sandbox_id}")
            state = str((detail.get("status") or {}).get("state") or "")
            if state not in {"Terminated", "Failed"}:
                self.control.management_json("POST", f"/v1/sandboxes/{sandbox_id}/stop")
        except SandboxError as exc:
            if exc.status != 404:
                raise
        self.inventory_path.unlink(missing_ok=True)
        return {"status": "stopped", "sandbox_id": sandbox_id}

    def delete(self, *, delete_environment: bool = False) -> dict[str, Any]:
        source = self._load_source()
        sandbox_id = str((source.get("worker") or {}).get("sandbox_id") or "")
        environment_id = str((source.get("environment") or {}).get("environment_id") or "")
        if sandbox_id:
            try:
                self.control.management_json("DELETE", f"/v1/sandboxes/{sandbox_id}")
            except SandboxError as exc:
                if exc.status != 404:
                    raise
            source.setdefault("worker", {})["sandbox_id"] = None
        if delete_environment and environment_id:
            self.control.management_json("DELETE", f"/v1/sandbox-environments/{environment_id}")
            source = {}
        if source:
            self._write_source(source)
        else:
            self.source_path.unlink(missing_ok=True)
        self.inventory_path.unlink(missing_ok=True)
        return {
            "status": "deleted",
            "sandbox_id": sandbox_id or None,
            "environment_id": environment_id if delete_environment else None,
        }

    def cleanup(self) -> dict[str, Any]:
        if self.options.cleanup == "keep":
            return {"status": "kept"}
        if self.options.cleanup == "delete":
            return self.delete(delete_environment=False)
        return self.stop()

    def _replace_incompatible_pool(self, source: dict[str, Any]) -> None:
        sandbox_id = str((source.get("worker") or {}).get("sandbox_id") or "")
        environment_id = str((source.get("environment") or {}).get("environment_id") or "")
        if sandbox_id:
            try:
                self.control.management_json("DELETE", f"/v1/sandboxes/{sandbox_id}")
            except SandboxError as exc:
                if exc.status != 404:
                    raise
        if environment_id:
            self.control.management_json("DELETE", f"/v1/sandbox-environments/{environment_id}")
        self.source_path.unlink(missing_ok=True)
        self.inventory_path.unlink(missing_ok=True)

    def _resources_match(self, source: dict[str, Any]) -> bool:
        environment = dict(source.get("environment") or {})
        resources = dict(environment.get("resources") or {})
        return (
            str(resources.get("cpu") or "") == str(self.options.cpu)
            and str(resources.get("memory") or "") == self.options.memory
            and str(environment.get("image") or "") == self.options.image
            and dict(environment.get("ports") or {}) == EXPOSED_SERVICE_PORTS
            and str((source.get("api") or {}).get("project") or "") == self.options.project
            and str((source.get("api") or {}).get("base_url") or "").rstrip("/")
            == self.options.base_url.rstrip("/")
        )

    def _environment_payload(self) -> dict[str, Any]:
        ports = [
            {"containerPort": port, "purpose": f"data-pipeline-{name}"}
            for name, port in EXPOSED_SERVICE_PORTS.items()
        ]
        return {
            "name": f"researchchem-data-pipeline-{self.options.cpu}cpu",
            "description": "ResearchChemBench data pipeline managed sandbox",
            "image": {"uri": self.options.image},
            "entrypoint": ["sleep", "inf"],
            "resources": {"cpu": str(self.options.cpu), "memory": self.options.memory},
            "ports": ports,
            "defaultLifecycleMinutes": self.options.lifecycle_minutes,
            "instanceCapacity": 1,
            "prewarmSize": 0,
            "ratio": 1,
            "volumes": [
                {
                    "name": "storage-vol-1",
                    "mountPath": "/mnt/shared-storage-user/liyuqiang",
                    "readOnly": True,
                    "host": {"path": "gpfs://gpfs1/liyuqiang"},
                }
            ],
        }

    def _source_template(self, *, environment_id: str, sandbox_id: str) -> dict[str, Any]:
        return {
            "schema_version": 1,
            "transport": "sandbox",
            "api": {
                "base_url": self.options.base_url.rstrip("/"),
                "project": self.options.project,
                "api_key_env": self.options.api_key_env,
            },
            "project": {
                "root": str(DATA_PIPELINE_ROOT),
                "shared_mount_root": "/mnt/shared-storage-user/liyuqiang",
                "shared_mount_read_only": True,
                "remote_runtime_root": DEFAULT_RUNTIME_ROOT,
            },
            "environment": {
                "environment_id": environment_id,
                "name": f"researchchem-data-pipeline-{self.options.cpu}cpu",
                "image": self.options.image,
                "resources": {"cpu": str(self.options.cpu), "memory": self.options.memory},
                "ports": dict(EXPOSED_SERVICE_PORTS),
                "default_lifecycle_minutes": self.options.lifecycle_minutes,
            },
            "worker": {
                "worker_id": "data-pipeline-sandbox-1",
                "sandbox_id": sandbox_id or None,
                "name": "researchchem-data-pipeline-worker",
            },
        }

    def _load_source(self) -> dict[str, Any]:
        if not self.source_path.is_file():
            return {}
        value = yaml.safe_load(self.source_path.read_text(encoding="utf-8")) or {}
        if not isinstance(value, dict):
            raise ValueError(f"sandbox source must be a YAML mapping: {self.source_path}")
        return value

    def _write_source(self, value: dict[str, Any]) -> None:
        self.source_path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.source_path.with_suffix(self.source_path.suffix + ".tmp")
        temporary.write_text(
            yaml.safe_dump(value, sort_keys=False, allow_unicode=True), encoding="utf-8"
        )
        os.chmod(temporary, 0o600)
        os.replace(temporary, self.source_path)

    def _write_inventory(self, worker: SandboxWorker) -> None:
        payload = {
            "schema_version": 1,
            "transport": "sandbox",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "project_path": str(DATA_PIPELINE_ROOT),
            "workers": [
                {
                    **asdict(worker),
                    "worker_id": "data-pipeline-sandbox-1",
                    "service_ports": dict(EXPOSED_SERVICE_PORTS),
                    "remote_runtime_root": DEFAULT_RUNTIME_ROOT,
                    "enabled": True,
                }
            ],
        }
        self.inventory_path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.inventory_path.with_suffix(self.inventory_path.suffix + ".tmp")
        temporary.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        os.chmod(temporary, 0o600)
        os.replace(temporary, self.inventory_path)

    def _wait_running(self, sandbox_id: str, timeout: float | None = None) -> dict[str, Any]:
        timeout = float(timeout or self.options.startup_timeout_seconds)
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            detail = self.control.management_json("GET", f"/v1/sandboxes/{sandbox_id}")
            state = str((detail.get("status") or {}).get("state") or "")
            if state == "Running":
                return detail
            if state in {"Failed", "Terminated"}:
                raise SandboxError(f"sandbox {sandbox_id} entered state {state}")
            time.sleep(5)
        raise SandboxError(f"sandbox {sandbox_id} did not become Running within {timeout}s")

    def _worker_from_detail(self, detail: dict[str, Any], environment_id: str) -> SandboxWorker:
        resources = dict(detail.get("resources") or {})
        return SandboxWorker(
            sandbox_id=str(detail["id"]),
            environment_id=environment_id,
            name=str(detail.get("name") or "researchchem-data-pipeline-worker"),
            state=str((detail.get("status") or {}).get("state") or ""),
            expires_at=str(detail.get("expiresAt") or detail.get("expireAt") or ""),
            cpu=int(float(resources.get("cpu") or self.options.cpu)),
            memory=str(resources.get("memory") or self.options.memory),
            base_url=self.options.base_url,
            project=self.options.project,
            api_key_env=self.options.api_key_env,
        )

    def _ensure_lifecycle(self, worker: SandboxWorker) -> SandboxWorker:
        response = self.control.management_json(
            "PATCH",
            f"/v1/sandboxes/{worker.sandbox_id}/lifecycle",
            payload={"lifecycleMinutes": self.options.lifecycle_minutes, "mode": "set"},
        )
        detail = self.control.management_json("GET", f"/v1/sandboxes/{worker.sandbox_id}")
        updated = self._worker_from_detail(detail, worker.environment_id)
        del response
        return updated

    def _ensure_worker_rpc(self, worker: SandboxWorker) -> None:
        client = worker.client()
        old_pid: int | None = None
        try:
            health = client.proxy_json("GET", port=worker.rpc_port, suffix="health", timeout=5)
            if (
                health.get("status") == "success"
                and int(health.get("protocol_version") or 0) == WORKER_PROTOCOL_VERSION
            ):
                return
            old_pid = int(health.get("pid") or 0) or None
        except SandboxError:
            pass
        python = DATA_PIPELINE_ROOT / ".envs" / "researchchem-data-pipeline" / "bin" / "python"
        if not python.is_file():
            raise SandboxError(f"data pipeline Python is missing: {python}", retryable=False)
        log_path = f"{DEFAULT_RUNTIME_ROOT}/worker.log"
        stop_old = f"kill {old_pid} 2>/dev/null || true; sleep 1; " if old_pid else ""
        command = (
            stop_old + f"mkdir -p {shlex.quote(DEFAULT_RUNTIME_ROOT)} && "
            f"cd {shlex.quote(str(DATA_PIPELINE_ROOT))} && "
            "PYTHONDONTWRITEBYTECODE=1 nohup "
            f"{shlex.quote(str(python))} -m src.sandbox.worker "
            f"--host 0.0.0.0 --port {worker.rpc_port} "
            f"--runtime-root {shlex.quote(DEFAULT_RUNTIME_ROOT)} "
            f">{shlex.quote(log_path)} 2>&1 </dev/null &"
        )
        result = client.run_command(command, timeout=60)
        if result["status"] != "success":
            raise SandboxError(
                f"failed to start data pipeline sandbox worker: {result.get('error')}",
                response=str(result.get("stderr") or ""),
            )
        deadline = time.monotonic() + 120
        last_error: Exception | None = None
        while time.monotonic() < deadline:
            try:
                health = client.proxy_json("GET", port=worker.rpc_port, suffix="health", timeout=5)
                if health.get("status") == "success":
                    return
            except SandboxError as exc:
                last_error = exc
            time.sleep(2)
        raise SandboxError(f"sandbox worker RPC did not become healthy: {last_error}")


def _redact_credentials(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: (
                "***"
                if key.casefold() in {"accesstoken", "api_key", "apikey"}
                else _redact_credentials(item)
            )
            for key, item in value.items()
        }
    if isinstance(value, list):
        return [_redact_credentials(item) for item in value]
    return value


__all__ = [
    "DATA_PIPELINE_ROOT",
    "DEFAULT_INVENTORY",
    "DEFAULT_SOURCE",
    "EXPOSED_SERVICE_PORTS",
    "MAX_SOFTCITE_INSTANCES",
    "SERVICE_PORTS",
    "service_instance_ports",
    "WORKER_PROTOCOL_VERSION",
    "SandboxManager",
    "SandboxRunOptions",
    "SandboxWorker",
]
