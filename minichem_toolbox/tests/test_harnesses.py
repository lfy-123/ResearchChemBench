from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


def test_harness_workspace_is_isolated(tmp_path: Path) -> None:
    root = Path(__file__).resolve().parents[1]
    workspace = tmp_path / "opencode-run"
    subprocess.run(
        [
            sys.executable,
            str(root / "tests" / "harnesses" / "prepare_harness.py"),
            "--toolbox-root",
            str(root),
            "--workspace",
            str(workspace),
        ],
        check=True,
        text=True,
        capture_output=True,
    )
    config = json.loads((workspace / "opencode.json").read_text(encoding="utf-8"))
    assert config["model"] == "deepseek/deepseek-v4-flash"
    assert config["provider"]["deepseek"]["options"]["apiKey"] == "{env:OPENAI_API_KEY}"
    assert config["mcp"]["minichem_toolbox"]["command"] == [
        str(workspace / "start_minichem_mcp.sh")
    ]
    for name in ("code", "data", "outputs", "report", "tool_logs", "_sessions"):
        assert (workspace / name).is_dir()
    launcher = (workspace / "start_minichem_mcp.sh").read_text(encoding="utf-8")
    assert f"MINICHEM_MCP_WORKSPACE={json.dumps(str(workspace))}" in launcher
