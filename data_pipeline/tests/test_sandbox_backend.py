from __future__ import annotations

import io
import json
import tarfile
import urllib.request

import pytest
import yaml

from src.pipeline import _sandbox_options_from_config, _sandbox_runtime_from_config
from src.sandbox.control import SandboxError
from src.sandbox.manager import SandboxManager, SandboxRunOptions
from src.sandbox.mineru_pool import MineruSandboxPool
from src.sandbox.proxy import LocalSandboxProxy
from src.sandbox.runtime import PooledMineruPipelineRuntime, SandboxPipelineRuntime
from src.sandbox.worker import PipelineSandboxServer


class FakeControl:
    def __init__(self) -> None:
        self.environment_id = "env-test"
        self.sandbox_id = "sbx-test"
        self.state = "Running"
        self.calls: list[tuple[str, str]] = []

    def management_json(self, method, suffix, *, payload=None, timeout=30):
        del payload, timeout
        self.calls.append((method, suffix))
        if suffix == "/v1/sandbox-environments" and method == "POST":
            return {"id": self.environment_id}
        if suffix == "/v1/sandboxes" and method == "POST":
            return {"id": self.sandbox_id, "status": {"state": "Pending"}}
        if suffix.endswith("/lifecycle"):
            return {"lifecycleMinutes": 120, "accessToken": "sat-new"}
        if suffix == f"/v1/sandboxes/{self.sandbox_id}":
            return {
                "id": self.sandbox_id,
                "name": "pipeline-test",
                "status": {"state": self.state},
                "environmentId": self.environment_id,
                "expiresAt": "2030-01-01T00:00:00Z",
                "resources": {"cpu": "12", "memory": "24Gi"},
            }
        return {}


def test_manager_creates_source_and_inventory(tmp_path, monkeypatch):
    monkeypatch.setenv("RCB_SANDBOX_API_KEY", "test-key")
    options = SandboxRunOptions(
        cpu=12,
        memory="24Gi",
        lifecycle_minutes=120,
        cleanup="keep",
        source=tmp_path / ".sandboxes.local.yaml",
        inventory=tmp_path / ".sandbox_inventory.local.json",
        base_url="https://sandbox.invalid/brainbox",
        project="test-project",
        image="registry.invalid/pipeline:test",
    )
    manager = SandboxManager(options)
    fake = FakeControl()
    manager.control = fake
    monkeypatch.setattr(manager, "_ensure_worker_rpc", lambda worker: None)

    worker = manager.ensure()

    assert worker.sandbox_id == "sbx-test"
    source = yaml.safe_load(options.source.read_text(encoding="utf-8"))
    assert source["environment"]["resources"] == {"cpu": "12", "memory": "24Gi"}
    assert source["worker"]["sandbox_id"] == "sbx-test"
    inventory = json.loads(options.inventory.read_text(encoding="utf-8"))
    assert inventory["workers"][0]["service_ports"]["grobid"] == 8070
    assert inventory["workers"][0]["service_ports"]["softcite_1"] == 8160
    assert options.source.stat().st_mode & 0o777 == 0o600
    assert options.inventory.stat().st_mode & 0o777 == 0o600


def test_manager_waits_for_recorded_pending_sandbox_without_recreating(
    tmp_path, monkeypatch
):
    monkeypatch.setenv("RCB_SANDBOX_API_KEY", "test-key")
    options = SandboxRunOptions(
        cpu=12,
        memory="24Gi",
        lifecycle_minutes=120,
        cleanup="keep",
        source=tmp_path / ".sandboxes.local.yaml",
        inventory=tmp_path / ".sandbox_inventory.local.json",
        base_url="https://sandbox.invalid/brainbox",
        project="test-project",
        image="registry.invalid/pipeline:test",
    )
    manager = SandboxManager(options)
    options.source.write_text(
        yaml.safe_dump(
            manager._source_template(
                environment_id="env-test", sandbox_id="sbx-test"
            )
        ),
        encoding="utf-8",
    )
    fake = FakeControl()
    fake.state = "Pending"
    manager.control = fake
    monkeypatch.setattr(
        manager,
        "_wait_running",
        lambda sandbox_id: {
            "id": sandbox_id,
            "name": "pipeline-test",
            "status": {"state": "Running"},
            "environmentId": "env-test",
            "expiresAt": "2030-01-01T00:00:00Z",
            "resources": {"cpu": "12", "memory": "24Gi"},
        },
    )
    monkeypatch.setattr(manager, "_ensure_worker_rpc", lambda worker: None)

    worker = manager.ensure()

    assert worker.sandbox_id == "sbx-test"
    assert ("POST", "/v1/sandboxes") not in fake.calls


def test_manager_reuses_compatible_environment_after_name_conflict(tmp_path, monkeypatch):
    monkeypatch.setenv("RCB_SANDBOX_API_KEY", "test-key")
    options = SandboxRunOptions(
        cpu=64,
        memory="128Gi",
        lifecycle_minutes=120,
        cleanup="keep",
        source=tmp_path / ".sandboxes.local.yaml",
        inventory=tmp_path / ".sandbox_inventory.local.json",
        base_url="https://sandbox.invalid/brainbox",
        project="test-project",
        image="registry.invalid/pipeline:test",
    )
    manager = SandboxManager(options)

    class ConflictControl(FakeControl):
        def management_json(self, method, suffix, *, payload=None, timeout=30):
            if suffix == "/v1/sandbox-environments" and method == "POST":
                self.calls.append((method, suffix))
                raise SandboxError("environment name conflict", status=409)
            if suffix == "/v1/sandbox-environments" and method == "GET":
                self.calls.append((method, suffix))
                return {
                    "items": [
                        {
                            "id": "env-existing",
                            "name": "researchchem-data-pipeline-64cpu",
                            "resources": {"cpu": "64", "memory": "128Gi"},
                            "image": {"uri": "registry.invalid/pipeline:test"},
                        }
                    ]
                }
            return super().management_json(
                method, suffix, payload=payload, timeout=timeout
            )

    fake = ConflictControl()
    manager.control = fake
    monkeypatch.setattr(manager, "_ensure_worker_rpc", lambda worker: None)

    worker = manager.ensure()

    assert worker.environment_id == "env-existing"
    source = yaml.safe_load(options.source.read_text(encoding="utf-8"))
    assert source["environment"]["environment_id"] == "env-existing"
    assert ("GET", "/v1/sandbox-environments") in fake.calls


def test_resource_validation_rejects_ambiguous_memory():
    with pytest.raises(ValueError, match="Mi, Gi, or Ti"):
        SandboxRunOptions(memory="96GB").validated()


def test_manager_retries_transient_ensure_failure(tmp_path, monkeypatch):
    monkeypatch.setenv("RCB_SANDBOX_API_KEY", "test-key")
    manager = SandboxManager(
        SandboxRunOptions(
            cleanup="keep",
            source=tmp_path / "source.yaml",
            inventory=tmp_path / "inventory.json",
        )
    )
    calls = 0
    worker = object()

    def ensure():
        nonlocal calls
        calls += 1
        if calls == 1:
            raise SandboxError("temporarily unavailable", status=503, retryable=True)
        return worker

    monkeypatch.setattr(manager, "ensure", ensure)
    monkeypatch.setattr("src.sandbox.manager.time.sleep", lambda _seconds: None)

    assert manager.ensure_with_retry(attempts=2) is worker
    assert calls == 2


def test_pipeline_builds_pooled_mineru_runtime_from_config(tmp_path):
    config = {
        "workspace": str(tmp_path / "run" / "batches" / "batch-0001"),
        "execution": {
            "sandbox": {
                "cpu": 64,
                "memory": "128Gi",
                "source": str(tmp_path / "main.yaml"),
                "inventory": str(tmp_path / "main.json"),
            },
            "mineru_sandbox_pool": {
                "enabled": True,
                "count": 32,
                "cpu": 16,
                "memory": "32Gi",
                "state_root": str(tmp_path / "pool"),
                "startup_concurrency": 32,
                "max_attempts": 2,
                "retry_delay_seconds": 5,
            },
        },
    }

    options = _sandbox_options_from_config(config)
    runtime = _sandbox_runtime_from_config(config, options=options)

    assert options.cpu == 64
    assert options.memory == "128Gi"
    assert isinstance(runtime, PooledMineruPipelineRuntime)
    assert runtime.mineru_pool.count == 32
    assert runtime.mineru_pool.options.cpu == 16
    assert runtime.mineru_pool.options.memory == "32Gi"


def test_mineru_pool_does_not_retry_execution_timeout(tmp_path, monkeypatch):
    pool = MineruSandboxPool(
        options=SandboxRunOptions(
            source=tmp_path / "source.yaml",
            inventory=tmp_path / "inventory.json",
        ),
        count=1,
        state_root=tmp_path / "pool",
        max_attempts=2,
        retry_delay_seconds=0,
    )
    pool._started = True
    calls = 0

    def run_once(*_args, **_kwargs):
        nonlocal calls
        calls += 1
        return {"status": "timeout", "error": "configured deadline exceeded"}

    monkeypatch.setattr(pool, "_run_once", run_once)
    result = pool.run_mineru(
        {"source_path": str(tmp_path / "paper.pdf")},
        tmp_path / "output",
        command="mineru",
        method="auto",
        backend="pipeline",
        timeout_seconds=3000,
        environment=None,
        extra_args=None,
    )

    assert calls == 1
    assert result["status"] == "timeout"
    assert result["attempt"] == 1
    assert result["retry_count"] == 0
    assert result["retry_suppressed_reason"] == "mineru_timeout"


def test_mineru_pool_still_retries_non_timeout_failure(tmp_path, monkeypatch):
    pool = MineruSandboxPool(
        options=SandboxRunOptions(
            source=tmp_path / "source.yaml",
            inventory=tmp_path / "inventory.json",
        ),
        count=1,
        state_root=tmp_path / "pool",
        max_attempts=2,
        retry_delay_seconds=0,
    )
    pool._started = True
    statuses = iter(("failed", "success"))
    calls = 0

    def run_once(*_args, **_kwargs):
        nonlocal calls
        calls += 1
        return {"status": next(statuses)}

    monkeypatch.setattr(pool, "_run_once", run_once)
    result = pool.run_mineru(
        {"source_path": str(tmp_path / "paper.pdf")},
        tmp_path / "output",
        command="mineru",
        method="auto",
        backend="pipeline",
        timeout_seconds=3000,
        environment=None,
        extra_args=None,
    )

    assert calls == 2
    assert result["status"] == "success"
    assert result["attempt"] == 2
    assert result["retry_count"] == 1


class FakeProxyClient:
    def proxy_bytes(self, method, *, port, suffix, body, headers, timeout):
        assert method == "POST"
        assert port == 8070
        assert suffix == "api/test?value=1"
        assert body == b"payload"
        assert headers["Content-Type"] == "text/plain"
        assert timeout == 30
        return 201, {"content-type": "text/plain"}, b"sandbox-response"


class InitiallyPendingProxyClient:
    def __init__(self) -> None:
        self.calls = 0

    def proxy_bytes(self, method, *, port, suffix, body, headers, timeout):
        del method, port, suffix, body, headers, timeout
        self.calls += 1
        return 403, {"content-type": "text/plain"}, b"sandbox sbx-test is not running (status: pending)"


class RecoveredProxyClient:
    def proxy_bytes(self, method, *, port, suffix, body, headers, timeout):
        del method, port, suffix, body, headers, timeout
        return 200, {"content-type": "text/plain"}, b"recovered"


def test_local_proxy_preserves_http_request_and_response():
    proxy = LocalSandboxProxy(FakeProxyClient(), remote_port=8070, request_timeout=30).start()
    try:
        request = urllib.request.Request(
            f"{proxy.base_url}/api/test?value=1",
            data=b"payload",
            headers={"Content-Type": "text/plain"},
            method="POST",
        )
        with urllib.request.urlopen(request, timeout=5) as response:
            assert response.status == 201
            assert response.read() == b"sandbox-response"
    finally:
        proxy.close()


def test_local_proxy_recovers_and_replays_when_sandbox_becomes_pending():
    pending = InitiallyPendingProxyClient()
    recovered = RecoveredProxyClient()
    recovery_calls = []
    proxy = LocalSandboxProxy(
        pending,
        remote_port=8070,
        request_timeout=30,
        recover_client=lambda status, payload: (
            recovery_calls.append((status, payload)) or recovered
        ),
    ).start()
    try:
        with urllib.request.urlopen(f"{proxy.base_url}/api/test", timeout=5) as response:
            assert response.status == 200
            assert response.read() == b"recovered"
    finally:
        proxy.close()
    assert pending.calls == 1
    assert len(recovery_calls) == 1


def test_worker_health_endpoint(tmp_path):
    server = PipelineSandboxServer(("127.0.0.1", 0), tmp_path / "runtime")
    import threading

    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        with urllib.request.urlopen(
            f"http://127.0.0.1:{server.server_address[1]}/health", timeout=5
        ) as response:
            payload = json.load(response)
        assert payload["status"] == "success"
        assert payload["service"] == "researchchem-data-pipeline-sandbox-worker"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def test_worker_rewrites_numbered_softcite_instance_ports(tmp_path):
    server = PipelineSandboxServer(("127.0.0.1", 0), tmp_path / "runtime")
    try:
        config = {"server": {"applicationConnectors": [{}], "adminConnectors": [{}]}}
        server._rewrite_service_config(
            "softcite",
            config,
            tmp_path / "softcite-002",
            application_port=8162,
            admin_port=8163,
        )
        assert config["server"]["applicationConnectors"][0]["port"] == 8162
        assert config["server"]["adminConnectors"][0]["port"] == 8163
    finally:
        server.server_close()


def test_mineru_archive_rejects_path_escape(tmp_path):
    archive = tmp_path / "bad.tar.gz"
    with tarfile.open(archive, "w:gz") as handle:
        info = tarfile.TarInfo("../escape.txt")
        payload = b"escape"
        info.size = len(payload)
        handle.addfile(info, io.BytesIO(payload))
    with pytest.raises(Exception, match="escapes destination"):
        SandboxPipelineRuntime._extract_archive(archive, tmp_path / "target")
