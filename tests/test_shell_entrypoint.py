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
