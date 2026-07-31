import json
import os
import subprocess
from pathlib import Path


def test_submit_evaluation_help():
    root = Path(__file__).resolve().parents[1]
    result = subprocess.run(
        ["bash", "scripts/submit_evaluation.sh", "--help"],
        cwd=root,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    assert result.returncode == 0
    assert "submit [OPTIONS] TASK [TASK ...]" in result.stdout
    assert "status" in result.stdout
    assert "follow" in result.stdout
    assert "summary" in result.stdout
    assert "--compute-action-timeout-seconds" in result.stdout
    assert "--fast-action-timeout-seconds" in result.stdout
    assert "--mcp-tool-timeout-seconds" in result.stdout
    assert "--available-cpu-cores" in result.stdout
    assert "--available-memory-mb" in result.stdout
    assert "--available-gpu-count" in result.stdout
    assert "--execution-mode" in result.stdout


def test_submit_evaluation_multi_task_dry_run(tmp_path: Path):
    root = Path(__file__).resolve().parents[1]
    run_root = tmp_path / "submission"
    result = subprocess.run(
        [
            "bash",
            "scripts/submit_evaluation.sh",
            "submit",
            "--dry-run",
            "--workspaces-dir",
            str(run_root),
            "--timeout-seconds",
            "600",
            "--max-turns",
            "20",
            "--compute-action-timeout-seconds",
            "500",
            "--fast-action-timeout-seconds",
            "30",
            "--mcp-tool-timeout-seconds",
            "600",
            "--available-cpu-cores",
            "12",
            "--available-memory-mb",
            "24576",
            "--available-gpu-count",
            "1",
            "Electron_Isodensity_Reproduction_01_Method_Selection",
            "Electron_Isodensity_01_Method_Selection",
        ],
        cwd=root,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "Planned runs: 2" in result.stdout
    config = json.loads((run_root / "evaluation_config.yaml").read_text())
    assert config["tasks"] == ["Electron_Isodensity_Reproduction_01_Method_Selection", "Electron_Isodensity_01_Method_Selection"]
    assert config["timeout_seconds"] == 600
    assert config["max_turns"] == 20
    assert config["compute_action_timeout_seconds"] == 500
    assert config["fast_action_timeout_seconds"] == 30
    assert config["mcp_tool_timeout_seconds"] == 600
    assert config["available_cpu_cores"] == 12
    assert config["available_memory_mb"] == 24576
    assert config["available_gpu_count"] == 1
    assert config["execution_mode"] == "local"
    submission = json.loads((run_root / "submission.json").read_text())
    assert submission["tasks"] == ["Electron_Isodensity_Reproduction_01_Method_Selection", "Electron_Isodensity_01_Method_Selection"]
    assert submission["agent_model"] == "deepseek-v4-flash"
    assert submission["compute_action_timeout_seconds"] == 500
    assert submission["fast_action_timeout_seconds"] == 30
    assert submission["mcp_tool_timeout_seconds"] == 600
    assert submission["execution_mode"] == "local"
    assert submission["resource_budget"] == {
        "cpu_cores": 12,
        "memory_mb": 24576,
        "gpu_count": 1,
        "scope": "per_task",
    }


def test_submit_evaluation_allows_operator_compute_timeout_above_default(tmp_path: Path):
    root = Path(__file__).resolve().parents[1]
    run_root = tmp_path / "long_timeout"
    result = subprocess.run(
        [
            "bash",
            "scripts/submit_evaluation.sh",
            "submit",
            "--dry-run",
            "--workspaces-dir",
            str(run_root),
            "--timeout-seconds",
            "10000",
            "--compute-action-timeout-seconds",
            "9000",
            "--mcp-tool-timeout-seconds",
            "9100",
            "Electron_Isodensity_Reproduction_01_Method_Selection",
        ],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    config = json.loads((run_root / "evaluation_config.yaml").read_text())
    assert config["compute_action_timeout_seconds"] == 9000
    assert config["mcp_tool_timeout_seconds"] == 9100


def test_submit_evaluation_distributed_mode_records_pool(tmp_path: Path):
    root = Path(__file__).resolve().parents[1]
    inventory = tmp_path / "inventory.json"
    inventory.write_text(
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
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    run_root = tmp_path / "distributed"
    environment = {
        **dict(os.environ),
        "RESEARCHCHEMBENCH_LOCAL_CONFIG": str(tmp_path / "missing.env"),
        "RCB_DISTRIBUTED_WORKER_INVENTORY": str(inventory),
        "RCB_DISTRIBUTED_STATE_ROOT": str(tmp_path / "pool"),
    }
    result = subprocess.run(
        [
            "bash",
            "scripts/submit_evaluation.sh",
            "submit",
            "--dry-run",
            "--execution-mode",
            "distributed",
            "--workspaces-dir",
            str(run_root),
            "Electron_Isodensity_Reproduction_01_Method_Selection",
        ],
        cwd=root,
        env=environment,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    submission = json.loads((run_root / "submission.json").read_text())
    assert submission["execution_mode"] == "distributed"
    assert submission["resource_budget"]["cpu_cores"] == 64
    assert submission["resource_budget"]["total_cpu_cores"] == 64
    assert submission["resource_budget"]["scope"] == (
        "per_job_on_one_compute_worker"
    )


def test_submit_evaluation_sandbox_mode_selects_sandbox_inventory(tmp_path: Path):
    root = Path(__file__).resolve().parents[1]
    inventory = tmp_path / "sandbox_inventory.json"
    inventory.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "transport": "sandbox",
                "workers": [
                    {
                        "worker_id": "sandbox-1",
                        "name": "sandbox-1",
                        "logical_cpus": 4,
                        "physical_cores": 2,
                        "memory_mb": 8192,
                        "available_cpu_cores": 2,
                        "available_memory_mb": 4096,
                        "gpu_count": 0,
                        "compute_cpu_ids": [0, 1],
                        "sandbox_id": "sbx-test",
                        "sandbox_api_base": "https://sandbox.invalid/brainbox",
                        "sandbox_project": "test-project",
                        "sandbox_project_root": str(root),
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    run_root = tmp_path / "sandbox-distributed"
    environment = {
        **dict(os.environ),
        "RESEARCHCHEMBENCH_LOCAL_CONFIG": str(tmp_path / "missing.env"),
        "RCB_DISTRIBUTED_SANDBOX_INVENTORY": str(inventory),
        "RCB_DISTRIBUTED_STATE_ROOT": str(tmp_path / "pool"),
    }
    result = subprocess.run(
        [
            "bash",
            "scripts/submit_evaluation.sh",
            "submit",
            "--dry-run",
            "--execution-mode",
            "distributed",
            "--distributed-transport",
            "sandbox",
            "--workspaces-dir",
            str(run_root),
            "Electron_Isodensity_Reproduction_01_Method_Selection",
        ],
        cwd=root,
        env=environment,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    submission = json.loads((run_root / "submission.json").read_text())
    assert submission["execution_mode"] == "distributed"
    assert submission["distributed_transport"] == "sandbox"
    assert submission["resource_budget"]["cpu_cores"] == 2
