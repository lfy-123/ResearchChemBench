from __future__ import annotations

import http.client
import io
import json
import os
import subprocess
import tarfile
import threading
import time
from pathlib import Path

import yaml

from chemistry_toolbox.mcp.distributed_job_dispatcher import (
    _extract_job_archive,
    _sandbox_synchronizing_status,
)
from researchchem_toolbox import runtime
from researchchem_toolbox.distributed_pool import load_worker_inventory
from researchchem_toolbox.resource_budget import resource_budget_record
from researchchem_toolbox.sandbox_client import OpenSandboxClient, SandboxTransportError
from researchchem_toolbox.sandbox_worker_rpc import SandboxWorkerServer


def _sandbox_inventory(path: Path) -> None:
    allowed = sorted(os.sched_getaffinity(0))
    path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "transport": "sandbox",
                "workers": [
                    {
                        "worker_id": "sandbox-1",
                        "name": "sandbox-test",
                        "logical_cpus": len(allowed),
                        "physical_cores": max(1, len(allowed) // 2),
                        "memory_mb": 8192,
                        "available_cpu_cores": min(4, len(allowed)),
                        "available_memory_mb": 4096,
                        "gpu_count": 0,
                        "compute_cpu_ids": allowed[: min(4, len(allowed))],
                        "sandbox_id": "sbx-test",
                        "environment_id": "env-test",
                        "sandbox_api_base": "https://sandbox.invalid/brainbox",
                        "sandbox_project": "test-project",
                        "sandbox_api_key_env": "RCB_SANDBOX_API_KEY",
                        "sandbox_command_port": 44772,
                        "sandbox_rpc_port": 44773,
                        "sandbox_project_root": str(path.parent),
                        "sandbox_remote_job_root": "/tmp/researchchembench-test/jobs",
                    }
                ],
            }
        ),
        encoding="utf-8",
    )


def test_sandbox_inventory_does_not_require_ssh_target(tmp_path, monkeypatch):
    inventory = tmp_path / "sandbox_inventory.json"
    _sandbox_inventory(inventory)
    monkeypatch.setenv("RESEARCHCHEMBENCH_EXECUTION_MODE", "distributed")
    monkeypatch.setenv("RCB_DISTRIBUTED_TRANSPORT", "sandbox")
    monkeypatch.setenv("RCB_DISTRIBUTED_INVENTORY", str(inventory))
    worker = load_worker_inventory()[0]
    assert worker.transport == "sandbox"
    assert worker.execution_ssh_target == ""
    assert worker.sandbox_id == "sbx-test"
    assert worker.sandbox_rpc_port == 44773
    assert resource_budget_record() == {
        "cpu_cores": min(4, len(os.sched_getaffinity(0))),
        "memory_mb": 4096,
        "gpu_count": 0,
        "source": "distributed_compute_pool",
        "agent_controllable": False,
        "scope": "per_job",
    }


def test_sandbox_action_uses_transport_without_entering_ssh_path(tmp_path, monkeypatch):
    inventory = tmp_path / "sandbox_inventory.json"
    _sandbox_inventory(inventory)
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    monkeypatch.setenv("RESEARCHCHEMBENCH_EXECUTION_MODE", "distributed")
    monkeypatch.setenv("RCB_DISTRIBUTED_TRANSPORT", "sandbox")
    monkeypatch.setenv("RCB_DISTRIBUTED_INVENTORY", str(inventory))
    monkeypatch.setenv("RCB_DISTRIBUTED_STATE_ROOT", str(tmp_path / "state"))
    monkeypatch.setenv("RCB_SANDBOX_API_KEY", "test-key")
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(workspace))
    runtime_python = tmp_path / "runtime-python"
    runtime_python.touch()
    monkeypatch.setattr(runtime, "runtime_python", lambda _name: runtime_python)
    monkeypatch.setattr(
        runtime,
        "runtime_environment",
        lambda _name: {"PATH": "/usr/bin", "RESEARCHCHEM_BACKEND_RUNTIME": "test"},
    )
    calls = []

    class Client:
        @classmethod
        def from_worker(cls, worker):
            calls.append(("worker", worker.worker_id))
            return cls()

        def run_action(self, envelope, *, timeout_seconds):
            calls.append(("action", envelope, timeout_seconds))
            return {"status": "success", "result": {"ok": True}}

    monkeypatch.setattr(runtime, "OpenSandboxClient", Client)
    result = runtime.invoke_worker(
        runtime="test",
        payload={
            "action_id": "test_action",
            "backend_id": "test_backend",
            "request": {
                "resource_limits": {
                    "cpu_cores": 2,
                    "memory_mb": 1024,
                    "gpu_count": 0,
                }
            },
        },
        timeout_seconds=60,
    )
    assert result["status"] == "success"
    assert result["provenance"]["distributed_transport"] == "sandbox"
    assert result["provenance"]["sandbox_id"] == "sbx-test"
    assert calls[1][1]["payload"]["action_id"] == "test_action"
    assert not list((tmp_path / "state" / "reservations").glob("*.json"))


def _request(
    port: int,
    method: str,
    path: str,
    *,
    body: bytes = b"",
    content_type: str = "application/json",
) -> tuple[int, bytes]:
    connection = http.client.HTTPConnection("127.0.0.1", port, timeout=30)
    try:
        connection.request(
            method,
            path,
            body=body,
            headers={
                "Content-Type": content_type,
                "Content-Length": str(len(body)),
            },
        )
        response = connection.getresponse()
        return response.status, response.read()
    finally:
        connection.close()


def test_sandbox_worker_rpc_runs_persistent_native_job(tmp_path):
    server = SandboxWorkerServer(("127.0.0.1", 0), tmp_path / "remote-jobs")
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    port = server.server_address[1]
    job_id = "job_rpc_test"
    remote_directory = (tmp_path / "remote-jobs" / job_id).resolve()
    try:
        status, payload = _request(port, "GET", "/health")
        assert status == 200
        assert json.loads(payload)["status"] == "success"

        archive_buffer = io.BytesIO()
        with tarfile.open(fileobj=archive_buffer, mode="w:gz") as archive:
            for name, data in {
                "stdout.log": b"",
                "stderr.log": b"",
                "status.json": json.dumps({"status": "queued"}).encode(),
            }.items():
                info = tarfile.TarInfo(name)
                info.size = len(data)
                archive.addfile(info, io.BytesIO(data))
            for name in ("inputs", "outputs", "report"):
                info = tarfile.TarInfo(name)
                info.type = tarfile.DIRTYPE
                info.mode = 0o755
                archive.addfile(info)
        status, payload = _request(
            port,
            "POST",
            f"/v1/jobs/{job_id}/stage",
            body=archive_buffer.getvalue(),
            content_type="application/gzip",
        )
        assert status == 200, payload

        cpu_id = sorted(os.sched_getaffinity(0))[0]
        specification = {
            "schema_version": 1,
            "job_id": job_id,
            "job_type": "native_software",
            "runtime": "core",
            "command": [
                "bash",
                "-c",
                (
                    "echo rpc-ok; echo artifact-ok > outputs/result.txt; "
                    "ln -s result.txt outputs/latest.txt; "
                    "ln -s missing.txt outputs/broken.txt"
                ),
            ],
            "job_directory": str(remote_directory),
            "relative_job_directory": f"sandbox/{job_id}",
            "status_path": str(remote_directory / "status.json"),
            "stdout_path": str(remote_directory / "stdout.log"),
            "stderr_path": str(remote_directory / "stderr.log"),
            "relative_stdout_path": f"sandbox/{job_id}/stdout.log",
            "relative_stderr_path": f"sandbox/{job_id}/stderr.log",
            "stdin_path": None,
            "resource_limits": {
                "cpu_cores": 1,
                "memory_mb": 1024,
                "gpu_count": 0,
                "walltime_seconds": 30,
            },
            "resource_allocation": {
                "worker_id": "sandbox-test",
                "cpu_ids": [cpu_id],
                "gpu_ids": [],
            },
            "evaluation_resource_budget": {},
            "submitted_at": "2026-07-31T00:00:00Z",
            "metadata": {"label": "rpc-test"},
            "execution_mode": "distributed",
            "compute_worker_id": "sandbox-test",
        }
        body = json.dumps(
            {"specification": specification, "environment": {}},
            ensure_ascii=False,
        ).encode()
        status, payload = _request(
            port, "POST", f"/v1/jobs/{job_id}/start", body=body
        )
        assert status == 200, payload
        assert json.loads(payload)["status"] == "success"

        deadline = time.monotonic() + 15
        job = {}
        while time.monotonic() < deadline:
            status, payload = _request(port, "GET", f"/v1/jobs/{job_id}/status")
            assert status == 200, payload
            job = json.loads(payload)["job"]
            if job.get("status") in {"success", "failed", "timeout", "cancelled"}:
                break
            time.sleep(0.1)
        assert job["status"] == "success", job
        assert (remote_directory / "outputs" / "result.txt").read_text().strip() == "artifact-ok"
        status, archive_payload = _request(
            port, "GET", f"/v1/jobs/{job_id}/archive"
        )
        assert status == 200, archive_payload
        with tarfile.open(fileobj=io.BytesIO(archive_payload), mode="r:gz") as archive:
            latest = archive.getmember("outputs/latest.txt")
            assert latest.isfile()
            extracted = archive.extractfile(latest)
            assert extracted is not None
            assert extracted.read() == b"artifact-ok\n"
            assert "outputs/broken.txt" not in archive.getnames()

        outside = tmp_path / "outside.txt"
        outside.write_text("must-not-leak\n", encoding="utf-8")
        (remote_directory / "outputs" / "escape.txt").symlink_to(outside)
        status, archive_payload = _request(
            port, "GET", f"/v1/jobs/{job_id}/archive"
        )
        assert status == 500
        assert b"archive link escapes directory" in archive_payload
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def test_sandbox_worker_rpc_archives_relative_action_artifacts(tmp_path):
    server = SandboxWorkerServer(("127.0.0.1", 0), tmp_path / "remote-jobs")
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    port = server.server_address[1]
    project_root = Path(__file__).parents[1]
    reservation_id = "action_artifact_test"
    envelope = {
        "schema_version": 1,
        "project_root": str(project_root),
        "runtime_python": str(runtime.runtime_python("core")),
        "distributed_reservation_id": reservation_id,
        "environment": runtime.runtime_environment("core"),
        "payload": {
            "action_id": "generate_3d_structure",
            "backend_id": "rdkit",
            "request": {
                "backend_id": "rdkit",
                "inputs": {"molecule": "O"},
                "method_spec": {},
                "action_settings": {
                    "random_seed": 20260718,
                    "timeout_seconds": 60,
                },
                "resource_limits": {
                    "cpu_cores": 1,
                    "memory_mb": 1024,
                    "gpu_count": 0,
                    "walltime_seconds": 60,
                },
            },
        },
    }
    try:
        status, payload = _request(
            port,
            "POST",
            "/v1/actions/run",
            body=json.dumps(
                {"envelope": envelope, "timeout_seconds": 60},
                ensure_ascii=False,
            ).encode(),
        )
        assert status == 200, payload
        result = json.loads(payload)
        assert result["status"] == "success", result
        assert result["artifact_files"]
        relative_path = result["artifact_files"][0]["path"]
        assert not Path(relative_path).is_absolute()

        status, archive_payload = _request(
            port,
            "GET",
            f"/v1/actions/{reservation_id}/archive",
        )
        assert status == 200, archive_payload
        with tarfile.open(fileobj=io.BytesIO(archive_payload), mode="r:gz") as archive:
            assert relative_path in archive.getnames()
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


def test_action_input_archive_preserves_workspace_relative_paths(tmp_path):
    workspace = tmp_path / "workspace"
    source = workspace / "outputs" / "prior" / "artifact.sdf"
    source.parent.mkdir(parents=True)
    source.write_text("artifact-data\n", encoding="utf-8")
    destination = tmp_path / "inputs.tar.gz"
    OpenSandboxClient._action_input_archive(
        {
            "request": {
                "inputs": {
                    "ensemble": {
                        "artifact_id": "art_0123456789abcdef0123456789abcdef",
                        "path": "outputs/prior/artifact.sdf",
                    }
                }
            }
        },
        workspace=workspace,
        destination=destination,
    )
    with tarfile.open(destination, "r:gz") as archive:
        assert archive.getnames() == ["outputs/prior/artifact.sdf"]
        extracted = archive.extractfile("outputs/prior/artifact.sdf")
        assert extracted is not None
        assert extracted.read() == b"artifact-data\n"


def test_job_archive_can_replace_read_only_staged_inputs(tmp_path):
    destination = tmp_path / "job"
    staged = destination / "inputs" / "author-output.log"
    staged.parent.mkdir(parents=True)
    staged.write_text("original\n", encoding="utf-8")
    staged.chmod(0o444)
    archive_path = tmp_path / "job.tar.gz"
    with tarfile.open(archive_path, "w:gz") as archive:
        for name, data, mode in (
            ("inputs/author-output.log", b"original\n", 0o444),
            ("outputs/result.json", b'{"ok": true}\n', 0o644),
        ):
            info = tarfile.TarInfo(name)
            info.size = len(data)
            info.mode = mode
            archive.addfile(info, io.BytesIO(data))
    _extract_job_archive(archive_path, destination)
    assert staged.read_text(encoding="utf-8") == "original\n"
    assert (destination / "outputs" / "result.json").is_file()


def test_sandbox_terminal_state_is_hidden_until_artifacts_are_synchronized():
    status = _sandbox_synchronizing_status(
        {
            "status": "success",
            "finished_at": "2026-07-31T00:00:00Z",
            "duration_seconds": 3.5,
            "return_code": 0,
        },
        terminal_status="success",
    )
    assert status["status"] == "running"
    assert status["sandbox_remote_terminal_status"] == "success"
    assert status["sandbox_artifacts_synchronizing"] is True
    assert "finished_at" not in status
    assert "duration_seconds" not in status


def test_sandbox_archive_download_retries_transient_failures(tmp_path, monkeypatch):
    client = OpenSandboxClient(
        base_url="https://sandbox.invalid/brainbox",
        project="test-project",
        api_key="test-key",
        sandbox_id="sbx-test",
    )
    destination = tmp_path / "job.tar.gz"
    calls = []

    def download(_suffix, target):
        calls.append(target)
        target.write_bytes(b"partial")
        if len(calls) < 3:
            raise SandboxTransportError("broken pipe")
        target.write_bytes(b"complete")

    monkeypatch.setattr(client, "_download_archive", download)
    monkeypatch.setattr(time, "sleep", lambda _seconds: None)
    client._download_archive_with_retry("v1/jobs/job-test/archive", destination)
    assert len(calls) == 3
    assert destination.read_bytes() == b"complete"


def test_sandbox_archive_download_does_not_retry_permanent_failure(
    tmp_path, monkeypatch
):
    client = OpenSandboxClient(
        base_url="https://sandbox.invalid/brainbox",
        project="test-project",
        api_key="test-key",
        sandbox_id="sbx-test",
    )
    destination = tmp_path / "job.tar.gz"
    calls = []

    def download(_suffix, target):
        calls.append(target)
        target.write_bytes(b"error-page")
        raise SandboxTransportError("not found", status=404, retryable=False)

    monkeypatch.setattr(client, "_download_archive", download)
    monkeypatch.setattr(time, "sleep", lambda _seconds: None)
    try:
        client._download_archive_with_retry("v1/jobs/missing/archive", destination)
    except SandboxTransportError as exc:
        assert exc.status == 404
    else:  # pragma: no cover - assertion helper without pytest dependency here
        raise AssertionError("permanent download failure should propagate")
    assert len(calls) == 1
    assert destination.read_bytes() == b"error-page"


def test_minimal_sandbox_source_configuration_is_supported(tmp_path):
    source = tmp_path / ".sandboxes.local.yaml"
    source.write_text(
        yaml.safe_dump(
            {
                "sandboxes": [
                    {
                        "sandbox_id": "sbx-one",
                        "available_cpu_cores": 64,
                        "available_memory_mb": 128000,
                    }
                ]
            },
            sort_keys=False,
        ),
        encoding="utf-8",
    )
    completed = subprocess.run(
        [
            str(Path(__file__).parents[1] / ".envs/researchchembench/bin/python"),
            "-c",
            (
                "import runpy; m=runpy.run_path('scripts/update_sandbox_inventory.py'); "
                f"p=m['_normalize_source'](m['yaml'].safe_load(open({str(source)!r}))); "
                "print(p[0]['project'], p[1][0]['sandbox_id'])"
            ),
        ],
        cwd=Path(__file__).parents[1],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    assert completed.returncode == 0, completed.stderr
    assert completed.stdout.strip() == "ailab-ai4chem sbx-one"
