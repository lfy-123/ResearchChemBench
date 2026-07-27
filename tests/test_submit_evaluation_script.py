import json
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
            "ChemGraph_001",
            "ChemGraph_002",
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
    assert config["tasks"] == ["ChemGraph_001", "ChemGraph_002"]
    assert config["timeout_seconds"] == 600
    assert config["max_turns"] == 20
    assert config["compute_action_timeout_seconds"] == 500
    assert config["fast_action_timeout_seconds"] == 30
    assert config["mcp_tool_timeout_seconds"] == 600
    assert config["available_cpu_cores"] == 12
    assert config["available_memory_mb"] == 24576
    assert config["available_gpu_count"] == 1
    submission = json.loads((run_root / "submission.json").read_text())
    assert submission["tasks"] == ["ChemGraph_001", "ChemGraph_002"]
    assert submission["agent_model"] == "deepseek-v4-flash"
    assert submission["compute_action_timeout_seconds"] == 500
    assert submission["fast_action_timeout_seconds"] == 30
    assert submission["mcp_tool_timeout_seconds"] == 600
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
            "ChemGraph_001",
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
