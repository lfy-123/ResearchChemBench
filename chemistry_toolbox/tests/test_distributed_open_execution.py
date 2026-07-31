from __future__ import annotations

import json
from pathlib import Path

from chemistry_toolbox.mcp.execution_models import (
    ExecutionResourceRequest,
    JobCancelRequest,
)
from chemistry_toolbox.mcp.open_execution import (
    _start_job,
    cancel_execution_job,
    get_execution_resources,
)


def _inventory(path: Path) -> None:
    path.write_text(
        json.dumps(
            {
                "workers": [
                    {
                        "worker_id": "compute-1",
                        "name": "worker-1",
                        "execution_ssh_target": "user@10.0.0.1",
                        "logical_cpus": 80,
                        "physical_cores": 40,
                        "memory_mb": 200000,
                        "available_cpu_cores": 64,
                        "available_memory_mb": 128000,
                        "gpu_count": 0,
                        "compute_cpu_ids": list(range(64)),
                    },
                    {
                        "worker_id": "compute-2",
                        "name": "worker-2",
                        "execution_ssh_target": "user@10.0.0.2",
                        "logical_cpus": 80,
                        "physical_cores": 40,
                        "memory_mb": 200000,
                        "available_cpu_cores": 64,
                        "available_memory_mb": 128000,
                        "gpu_count": 0,
                        "compute_cpu_ids": list(range(100, 164)),
                    },
                ]
            }
        ),
        encoding="utf-8",
    )


def test_distributed_job_is_queued_without_local_compute(tmp_path, monkeypatch):
    for name in ("code", "outputs", "report", "tool_logs"):
        (tmp_path / name).mkdir()
    inventory = tmp_path / "inventory.json"
    _inventory(inventory)
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    monkeypatch.setenv("RESEARCHCHEMBENCH_EXECUTION_MODE", "distributed")
    monkeypatch.setenv("RCB_DISTRIBUTED_WORKER_INVENTORY", str(inventory))
    monkeypatch.setenv("RCB_DISTRIBUTED_STATE_ROOT", str(tmp_path / "pool"))

    class Dispatcher:
        pid = 4321

    monkeypatch.setattr(
        "chemistry_toolbox.mcp.open_execution.subprocess.Popen",
        lambda *args, **kwargs: Dispatcher(),
    )
    submitted = _start_job(
        job_type="native_software",
        runtime="core",
        command=["/bin/true"],
        stdin_target=None,
        staged_inputs=[],
        resource_limits={
            "cpu_cores": 8,
            "memory_mb": 12000,
            "gpu_count": 0,
            "walltime_seconds": 60,
        },
        metadata={"label": "distributed-test"},
    )
    assert submitted["status"] == "success"
    assert submitted["job_status"] == "queued"
    assert submitted["execution_mode"] == "distributed"
    assert submitted["resource_allocation"] == {}
    directory = tmp_path / submitted["job_directory"]
    status = json.loads((directory / "status.json").read_text(encoding="utf-8"))
    assert status["dispatcher_pid"] == 4321
    assert status["execution_mode"] == "distributed"

    cancelled = cancel_execution_job(JobCancelRequest(job_id=submitted["job_id"]))
    assert cancelled["cancellation_sent"] is True
    assert (directory / "cancel_requested").is_file()


def test_distributed_resource_contract_is_anonymous(tmp_path, monkeypatch):
    inventory = tmp_path / "inventory.json"
    _inventory(inventory)
    monkeypatch.setenv("RESEARCHCHEMBENCH_EXECUTION_MODE", "distributed")
    monkeypatch.setenv("RCB_DISTRIBUTED_WORKER_INVENTORY", str(inventory))
    monkeypatch.setenv("RCB_DISTRIBUTED_STATE_ROOT", str(tmp_path / "pool"))
    resources = get_execution_resources(ExecutionResourceRequest())
    assert resources["status"] == "success"
    assert resources["execution_mode"] == "distributed"
    assert resources["total_cpu_cores"] == 128
    assert resources["maximum_cpu_cores_per_job"] == 64
    assert resources["single_job_cross_node_execution"] is False
    assert all("execution_ssh_target" not in item for item in resources["workers"])
