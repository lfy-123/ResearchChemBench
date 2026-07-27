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
    submission = json.loads((run_root / "submission.json").read_text())
    assert submission["tasks"] == ["ChemGraph_001", "ChemGraph_002"]
    assert submission["agent_model"] == "deepseek-v4-flash"
