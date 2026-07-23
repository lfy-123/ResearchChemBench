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
            "ChemGraph_001",
            "--no-score",
            "--workspaces-dir",
            str(workspaces),
        ],
        cwd=root,
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
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
            str(root / "eval_configs" / "quick_mock.yaml"),
            "--judge-model",
            "bailian/deepseek-v4-pro",
            "--dry-run",
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


def test_open_discovery_submission_script_has_model_specific_output_roots(tmp_path):
    root = Path(__file__).resolve().parents[1]
    local_config = tmp_path / "local.env"
    local_config.write_text(
        "OPENCODE_BASE_URL_VALUE=https://gateway.invalid/v1\n"
        "JUDGE_API_BASE=https://gateway.invalid/v1\n",
        encoding="utf-8",
    )
    env = os.environ.copy()
    env["RESEARCHCHEMBENCH_LOCAL_CONFIG"] = str(local_config)

    result = subprocess.run(
        [
            "bash",
            str(root / "scripts" / "submit_heterobiaryl_open_discovery.sh"),
            "pro",
            "--stage",
            "q6",
            "--dry-run",
        ],
        cwd=root,
        env=env,
        capture_output=True,
        text=True,
        timeout=120,
        check=False,
    )

    assert result.returncode == 0, result.stdout + result.stderr
    assert "Agent model:     bailian/deepseek-v4-pro" in result.stdout
    assert "Judge model:     bailian/deepseek-v4-pro" in result.stdout
    assert "agent_deepseek-v4-pro__judge_deepseek-v4-pro" in result.stdout
    assert "Heterobiaryl_PV_06_End_to_End" in result.stdout
