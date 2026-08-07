import json
import os
import subprocess
from pathlib import Path


def test_local_config_opencode_route_reaches_generated_workspace(tmp_path):
    root = Path(__file__).resolve().parents[1]
    local_config = tmp_path / "local.env"
    local_config.write_text(
        "OPENCODE_MODEL_VALUE=gateway/test-model\n"
        "OPENCODE_BASE_URL_VALUE=https://gateway.invalid/v1\n",
        encoding="utf-8",
    )
    workspaces = tmp_path / "workspaces"
    env = os.environ.copy()
    env["RESEARCHCHEMBENCH_LOCAL_CONFIG"] = str(local_config)

    result = subprocess.run(
        [
            "bash",
            str(root / "scripts" / "run_agent_eval.sh"),
            "--agent",
            "mock",
            "--task",
            "Electron_Isodensity_Reproduction_01_Method_Selection",
            "--no-score",
            "--workspaces-dir",
            str(workspaces),
            "--progress-max-chars",
            "123",
        ],
        cwd=root,
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "[RUN_START]" not in result.stdout
    assert "[MODEL_INPUT]" not in result.stdout
    assert "[MODEL_OUTPUT]" not in result.stdout
    assert "[MCP_CALL]" not in result.stdout
    assert "Live progress=1 console=0 max_chars=123" in result.stdout
    configs = list((workspaces / "cli_runs").glob("batch_*/*/opencode.json"))
    assert len(configs) == 1
    config = json.loads(configs[0].read_text(encoding="utf-8"))
    assert config["model"] == "gateway/test-model"
    assert config["provider"]["gateway"]["options"]["baseURL"] == (
        "https://gateway.invalid/v1"
    )
    assert config["provider"]["gateway"]["options"]["apiKey"] == (
        "{env:OPENAI_API_KEY}"
    )
    progress_logs = list((workspaces / "cli_runs").glob("batch_*/*/_live_progress.log"))
    assert len(progress_logs) == 1
    progress = progress_logs[0].read_text(encoding="utf-8")
    assert "[RUN_START]" in progress
    assert "[MODEL_INPUT]" in progress
    assert "[RUN_END]" in progress
    meta = json.loads((progress_logs[0].parent / "_meta.json").read_text(encoding="utf-8"))
    assert meta["progress_max_chars"] == 123
    assert meta["progress_console"] is False


def test_cli_judge_model_override_is_visible_in_batch_dry_run(tmp_path):
    root = Path(__file__).resolve().parents[1]
    local_config = tmp_path / "local.env"
    local_config.write_text(
        "OPENCODE_MODEL_VALUE=bailian/deepseek-v4-flash\n"
        "OPENCODE_BASE_URL_VALUE=https://gateway.invalid/v1\n"
        "JUDGE_MODEL_NAME=bailian/old-judge\n",
        encoding="utf-8",
    )
    env = os.environ.copy()
    env["RESEARCHCHEMBENCH_LOCAL_CONFIG"] = str(local_config)

    result = subprocess.run(
        [
            "bash",
            str(root / "scripts" / "run_agent_eval.sh"),
            "--config",
            str(root / "eval_configs" / "examples" / "quick_mock.yaml"),
            "--judge-model",
            "bailian/deepseek-v4-pro",
            "--dry-run",
            "--no-progress-console",
            "--progress-max-chars",
            "240",
        ],
        cwd=root,
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "Judge model:     bailian/deepseek-v4-pro" in result.stdout
