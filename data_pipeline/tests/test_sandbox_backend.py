from __future__ import annotations

import io
import json
import tarfile
import urllib.request

import pytest
import yaml

from src.sandbox.manager import SandboxManager, SandboxRunOptions
from src.sandbox.proxy import LocalSandboxProxy
from src.sandbox.runtime import SandboxPipelineRuntime
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


def test_resource_validation_rejects_ambiguous_memory():
    with pytest.raises(ValueError, match="Mi, Gi, or Ti"):
        SandboxRunOptions(memory="96GB").validated()


class FakeProxyClient:
    def proxy_bytes(self, method, *, port, suffix, body, headers, timeout):
        assert method == "POST"
        assert port == 8070
        assert suffix == "api/test?value=1"
        assert body == b"payload"
        assert headers["Content-Type"] == "text/plain"
        assert timeout == 30
        return 201, {"content-type": "text/plain"}, b"sandbox-response"


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
