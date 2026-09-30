from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest
from pydantic import ValidationError

from chemistry_toolbox.mcp import action_batch_supervisor
from chemistry_toolbox.mcp.async_action_tools import (
    _read_events,
    submit_action_batch_async,
    wait_execution_events,
)
from chemistry_toolbox.mcp.discovery_models import (
    ActionBatchItem,
    ActionBatchRequest,
    ExecutionEventWaitRequest,
)


def test_result_pages_never_advance_past_undelivered_events(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    monkeypatch.setenv("RESEARCHCHEM_MCP_WORKSPACE", str(tmp_path))
    ids=[]
    for batch_index in range(2):
        batch="batch_"+str(batch_index)*32;ids.append(batch)
        directory=tmp_path/"outputs"/"action_batches"/batch;directory.mkdir(parents=True)
        events=[{"sequence":i+1,"type":"item_finished","item_id":str(i),"status":"failed"} for i in range(32)]
        items=[{"item_id":str(i),"status":"failed","result":{"status":"failed","error":{"code":"fixture"}}} for i in range(32)]
        (directory/"status.json").write_text(json.dumps({"batch_id":batch,"status":"failed","last_sequence":32,"events":events,"items":items}))
    clock=[0]
    def read(cursors):
        return _read_events(ExecutionEventWaitRequest(batch_ids=ids,after_sequences=cursors),
            policy={"settle_seconds":1,"max_batch_seconds":2,"heartbeat_seconds":3,"poll_interval_seconds":1,"failure_tail_chars":100},
            monotonic_fn=lambda:clock[0],sleep_fn=lambda n:clock.__setitem__(0,clock[0]+n))
    first=read({})
    assert first["return_reason"]=="result_page" and len(first["newly_terminal_items"])==32
    assert first["next_sequences"]=={ids[0]:32,ids[1]:0}
    assert first["remaining_batch_ids"]==[ids[1]]
    second=read(first["next_sequences"])
    assert len(second["newly_terminal_items"])==32
    assert second["next_sequences"]=={ids[0]:32,ids[1]:32}


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
    request_record = json.loads(
        (
            tmp_path
            / "outputs"
            / "action_batches"
            / submitted["batch_id"]
            / "request.json"
        ).read_text(encoding="utf-8")
    )
    assert request_record["supervisor_parent_pid"] == os.getpid()
    clock = [0.0]
    waited = _read_events(
        ExecutionEventWaitRequest(batch_ids=[submitted["batch_id"]]),
        policy={
            "settle_seconds": 2,
            "max_batch_seconds": 4,
            "heartbeat_seconds": 5,
            "poll_interval_seconds": 1,
            "failure_tail_chars": 100,
        },
        monotonic_fn=lambda: clock[0],
        sleep_fn=lambda seconds: clock.__setitem__(0, clock[0] + seconds),
    )
    assert waited["status"] == "success"
    assert waited["return_reason"] == "heartbeat"
    assert waited["batches"][0]["status"] == "queued"
    assert waited["batches"][0]["next_sequence"] == 0
    assert waited["batches"][0]["item_status_counts"] == {"queued": 1}
    assert "items" not in waited["batches"][0]


def test_submit_crest_conformer_batch_is_accepted(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    monkeypatch.setenv("RESEARCHCHEMBENCH_AVAILABLE_CPU_CORES", "32")
    monkeypatch.setenv("RESEARCHCHEMBENCH_AVAILABLE_MEMORY_MB", "64000")
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
            action_id="generate_conformer_ensemble",
            backend_id="crest",
            method_spec={"method": "GFN2-xTB"},
            items=[
                ActionBatchItem(
                    item_id=f"conformer_{index}",
                    inputs={"molecule": f"outputs/start_{index}.xyz"},
                    resource_limits={"cpu_cores": 8, "memory_mb": 8000},
                )
                for index in range(3)
            ],
        )
    )
    assert submitted["status"] == "success"
    assert submitted["item_count"] == 3
    assert submitted["scheduling"] == "largest_cpu_then_memory_first"


def test_event_wait_settles_and_returns_terminal_artifact_handoff(
    tmp_path, monkeypatch
):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    monkeypatch.setenv("RESEARCHCHEMBENCH_AVAILABLE_CPU_CORES", "4")
    monkeypatch.setenv("RESEARCHCHEMBENCH_AVAILABLE_MEMORY_MB", "16000")
    monkeypatch.setenv("RESEARCHCHEMBENCH_AVAILABLE_GPU_COUNT", "0")
    batch_id = "batch_" + "c" * 32
    directory = tmp_path / "outputs" / "action_batches" / batch_id
    directory.mkdir(parents=True)
    status_path = directory / "status.json"
    result = {
        "status": "success",
        "result": {"energy_hartree": -1.0},
        "output_artifacts": [{"artifact_id": "artifact_1"}],
        "artifact_handoff": {"primary_output": {"artifact_id": "artifact_1"}},
        "provenance": {"compute_worker_id": "compute-1"},
    }
    status_path.write_text(
        json.dumps(
            {
                "batch_id": batch_id,
                "status": "running",
                "last_sequence": 1,
                "events": [
                    {"sequence": 1, "type": "item_finished", "item_id": "done"}
                ],
                "items": [
                    {
                        "item_id": "done",
                        "batch_index": 0,
                        "status": "success",
                        "resource_limits": {"cpu_cores": 2, "memory_mb": 4000},
                        "result": result,
                    },
                    {
                        "item_id": "active",
                        "batch_index": 1,
                        "status": "running",
                        "resource_limits": {"cpu_cores": 2, "memory_mb": 4000},
                    },
                ],
            }
        ),
        encoding="utf-8",
    )
    clock = [0.0]
    waited = _read_events(
        ExecutionEventWaitRequest(batch_ids=[batch_id], timeout_seconds=0.1),
        policy={
            "settle_seconds": 3,
            "max_batch_seconds": 10,
            "heartbeat_seconds": 20,
            "poll_interval_seconds": 1,
            "failure_tail_chars": 100,
        },
        monotonic_fn=lambda: clock[0],
        sleep_fn=lambda seconds: clock.__setitem__(0, clock[0] + seconds),
    )
    assert waited["return_reason"] == "settled_state_update"
    assert waited["wait_duration_seconds"] == 3
    assert waited["newly_terminal_items"][0]["result"]["output_artifacts"] == [
        {"artifact_id": "artifact_1"}
    ]
    assert waited["newly_terminal_items"][0]["worker_id"] == "compute-1"
    assert waited["running_items"][0]["item_id"] == "active"
    assert waited["remaining_batch_ids"] == [batch_id]
    assert waited["deprecated_request_timeout_seconds_ignored"] == 0.1


def test_event_wait_supports_long_compute_waits() -> None:
    request = ExecutionEventWaitRequest(
        batch_ids=["batch_" + "a" * 32], timeout_seconds=600
    )
    assert request.timeout_seconds == 600

    with pytest.raises(ValidationError):
        ExecutionEventWaitRequest(
            batch_ids=["batch_" + "a" * 32], timeout_seconds=601
        )


@pytest.mark.skipif(not sys.platform.startswith("linux"), reason="Linux prctl test")
def test_detached_batch_supervisor_exits_with_owning_mcp_process(
    tmp_path: Path,
) -> None:
    request_path = tmp_path / "request.json"
    status_path = tmp_path / "status.json"
    status_path.write_text(
        json.dumps(
            {
                "batch_id": "batch_" + "b" * 32,
                "status": "queued",
                "last_sequence": 0,
                "events": [],
                "items": [
                    {
                        "item_id": "pending",
                        "batch_index": 0,
                        "status": "queued",
                        "resource_limits": {
                            "cpu_cores": 999,
                            "memory_mb": 1,
                            "gpu_count": 0,
                        },
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    parent_program = "\n".join(
        [
            "import json, os, pathlib, subprocess, sys, time",
            "request_path = pathlib.Path(sys.argv[1])",
            "request = {",
            "  'batch_id': 'batch_' + 'b' * 32,",
            "  'action_id': 'calculate_energy',",
            "  'backend_id': 'ase_emt',",
            "  'component_backends': {}, 'method_spec': {}, 'action_settings': {},",
            "  'max_concurrency': 1, 'supervisor_parent_pid': os.getpid(),",
            "  'items': [{'item_id': 'pending', 'batch_index': 0, 'inputs': {},",
            "             'resource_limits': {'cpu_cores': 999, 'memory_mb': 1, 'gpu_count': 0},",
            "             'normalized_resources': {'cpu_cores': 999, 'memory_mb': 1, 'gpu_count': 0}}]",
            "}",
            "request_path.write_text(json.dumps(request), encoding='utf-8')",
            "child = subprocess.Popen([sys.executable, '-m', 'chemistry_toolbox.mcp.action_batch_supervisor', str(request_path)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)",
            "print(child.pid, flush=True)",
            "time.sleep(0.5)",
        ]
    )
    environment = os.environ.copy()
    environment.pop("RESEARCHCHEMBENCH_EXECUTION_MODE", None)
    environment.pop("RCB_DISTRIBUTED_WORKER_INVENTORY", None)
    parent = subprocess.run(
        [sys.executable, "-c", parent_program, str(request_path)],
        cwd=Path(__file__).parents[2],
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=10,
        check=True,
    )
    supervisor_pid = int(parent.stdout.strip())
    deadline = time.monotonic() + 5
    while time.monotonic() < deadline:
        try:
            os.kill(supervisor_pid, 0)
        except ProcessLookupError:
            break
        time.sleep(0.05)
    else:
        os.kill(supervisor_pid, 9)
        pytest.fail("detached batch supervisor survived its owning MCP process")
