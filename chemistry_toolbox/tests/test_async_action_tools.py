from __future__ import annotations

import json
import time
from pathlib import Path

from chemistry_toolbox.mcp import action_batch_supervisor
from chemistry_toolbox.mcp.async_action_tools import (
    submit_action_batch_async,
    wait_execution_events,
)
from chemistry_toolbox.mcp.discovery_models import (
    ActionBatchItem,
    ActionBatchRequest,
    ExecutionEventWaitRequest,
)


def _request_record(batch_id: str) -> dict:
    resources = [("large", 4, 8000), ("small", 1, 2000), ("medium", 2, 4000)]
    return {
        "schema_version": 1,
        "batch_id": batch_id,
        "action_id": "calculate_energy",
        "backend_id": "ase_emt",
        "component_backends": {},
        "method_spec": {},
        "action_settings": {},
        "max_concurrency": 3,
        "items": [
            {
                "item_id": name,
                "batch_index": index,
                "inputs": {"label": name},
                "resource_limits": {
                    "cpu_cores": cpu,
                    "memory_mb": memory,
                    "gpu_count": 0,
                },
                "normalized_resources": {
                    "cpu_cores": cpu,
                    "memory_mb": memory,
                    "gpu_count": 0,
                },
            }
            for index, (name, cpu, memory) in enumerate(resources)
        ],
    }


def test_async_supervisor_starts_largest_request_first(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    monkeypatch.setenv("RESEARCHCHEMBENCH_AVAILABLE_CPU_CORES", "4")
    monkeypatch.setenv("RESEARCHCHEMBENCH_AVAILABLE_MEMORY_MB", "16000")
    monkeypatch.setenv("RESEARCHCHEMBENCH_AVAILABLE_GPU_COUNT", "0")
    batch_id = "batch_" + "1" * 32
    directory = tmp_path / "outputs" / "action_batches" / batch_id
    directory.mkdir(parents=True)
    request = _request_record(batch_id)
    request_path = directory / "request.json"
    request_path.write_text(json.dumps(request), encoding="utf-8")
    (directory / "status.json").write_text(
        json.dumps(
            {
                "batch_id": batch_id,
                "status": "queued",
                "last_sequence": 0,
                "events": [],
                "items": [
                    {
                        "item_id": item["item_id"],
                        "batch_index": item["batch_index"],
                        "status": "queued",
                        "resource_limits": item["resource_limits"],
                    }
                    for item in request["items"]
                ],
            }
        ),
        encoding="utf-8",
    )
    started = []

    def fake_execute(action_id, action_request):
        started.append(action_request["inputs"]["label"])
        time.sleep(0.02)
        return {
            "status": "success",
            "action": action_id,
            "result": {"label": action_request["inputs"]["label"]},
            "output_artifacts": [],
        }

    monkeypatch.setattr(action_batch_supervisor, "execute_action", fake_execute)
    assert action_batch_supervisor.run_batch(request_path) == 0
    status = json.loads((directory / "status.json").read_text(encoding="utf-8"))
    assert started[0] == "large"
    assert status["status"] == "success"
    assert [item["status"] for item in status["items"]] == [
        "success",
        "success",
        "success",
    ]
    started_events = [
        event["item_id"]
        for event in status["events"]
        if event["type"] == "item_started"
    ]
    assert started_events[0] == "large"


def test_submit_and_wait_async_batch_persist_status(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    monkeypatch.setenv("RESEARCHCHEMBENCH_AVAILABLE_CPU_CORES", "4")
    monkeypatch.setenv("RESEARCHCHEMBENCH_AVAILABLE_MEMORY_MB", "16000")
    monkeypatch.setenv("RESEARCHCHEMBENCH_AVAILABLE_GPU_COUNT", "0")
    (tmp_path / "outputs").mkdir()

    class Supervisor:
        pid = 12345

    monkeypatch.setattr(
        "chemistry_toolbox.mcp.async_action_tools.subprocess.Popen",
        lambda *args, **kwargs: Supervisor(),
    )
    submitted = submit_action_batch_async(
        ActionBatchRequest(
            action_id="calculate_energy",
            backend_id="ase_emt",
            items=[
                ActionBatchItem(
                    item_id="point_1",
                    inputs={"label": "one"},
                    resource_limits={"cpu_cores": 2, "memory_mb": 4000},
                )
            ],
        )
    )
    assert submitted["status"] == "success"
    waited = wait_execution_events(
        ExecutionEventWaitRequest(batch_ids=[submitted["batch_id"]])
    )
    assert waited["status"] == "success"
    assert waited["batches"][0]["status"] == "queued"
    assert waited["batches"][0]["next_sequence"] == 0
