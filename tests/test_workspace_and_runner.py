import json
from pathlib import Path

from evaluation.run_task import TaskRunner


def test_workspace_does_not_copy_hidden_ground_truth(tmp_path: Path):
    runner = TaskRunner("ChemGraph_001", agent_key="mock", workspace_root=tmp_path)
    runner.setup_workspace()
    assert runner.instructions_path.is_file()
    assert not (runner.workspace / "target_study").exists()
    assert (runner.workspace / "report").is_dir()
    assert (runner.workspace / ".mcp.json").is_file()
    mcp_config = json.loads((runner.workspace / ".mcp.json").read_text())
    assert "chemistry_toolbox.mcp.server" in mcp_config["mcpServers"]["researchchem_toolbox"]["args"]


def test_mock_agent_end_to_end(tmp_path: Path):
    runner = TaskRunner("ChemGraph_001", agent_key="mock", workspace_root=tmp_path)
    meta = runner.run()
    assert meta["status"] == "completed"
    assert meta["exit_code"] == 0
    assert (runner.workspace / "report" / "report.md").is_file()
    events = [json.loads(line) for line in runner.output_path.read_text().splitlines()]
    assert events[-1]["type"] == "result"


def test_codex_and_claude_commands_include_mcp(tmp_path: Path):
    codex = TaskRunner("ChemGraph_001", agent_key="codex", workspace_root=tmp_path)
    codex.setup_workspace()
    codex_argv = codex.command_preview()
    assert codex_argv[:2] == ["codex", "exec"]
    assert any("mcp_servers.researchchem_toolbox.command" in item for item in codex_argv)
    assert "--json" in codex_argv

    claude = TaskRunner("ChemGraph_001", agent_key="claude", workspace_root=tmp_path)
    claude.setup_workspace()
    claude_argv = claude.command_preview()
    assert claude_argv[:2] == ["claude", "-p"]
    assert "--mcp-config" in claude_argv
    assert "--strict-mcp-config" in claude_argv
    assert any("mcp__researchchem_toolbox__*" in item for item in claude_argv)
    assert not any(item == "mcp__*" for item in claude_argv)

    opencode = TaskRunner("ChemGraph_001", agent_key="opencode", workspace_root=tmp_path)
    opencode.setup_workspace()
    opencode_argv = opencode.command_preview()
    assert opencode_argv[:2] == ["opencode", "run"]
    assert "--pure" in opencode_argv
    config = json.loads((opencode.workspace / "opencode.json").read_text())
    assert config["mcp"]["researchchem_toolbox"]["type"] == "local"
    assert config["mcp"]["researchchem_toolbox"]["timeout"] == 3_600_000
    assert config["model"] == "deepseek/deepseek-v4-flash"
    assert "OPENAI_API_KEY" not in json.dumps(config)


def test_agent_environment_does_not_receive_judge_key(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("JUDGE_API_KEY", "private-judge-key")
    monkeypatch.setenv("OPENAI_API_KEY", "agent-auth-key")
    runner = TaskRunner("ChemGraph_001", agent_key="mock", workspace_root=tmp_path)
    runner.setup_workspace()
    env = runner._agent_environment()
    assert "JUDGE_API_KEY" not in env
    assert env["OPENAI_API_KEY"] == "agent-auth-key"
    assert env["RESEARCHCHEMBENCH_WORKSPACE"] == str(runner.workspace.resolve())


def test_concurrent_opencode_runs_use_isolated_databases(tmp_path: Path):
    first = TaskRunner("ChemGraph_005", agent_key="opencode", workspace_root=tmp_path)
    second = TaskRunner("ChemGraph_024", agent_key="opencode", workspace_root=tmp_path)
    first.setup_workspace()
    second.setup_workspace()

    first_env = first._agent_environment()
    second_env = second._agent_environment()
    assert first_env["OPENCODE_DB"] == str(
        (first.workspace / "_opencode/opencode.db").resolve()
    )
    assert second_env["OPENCODE_DB"] == str(
        (second.workspace / "_opencode/opencode.db").resolve()
    )
    assert first_env["OPENCODE_DB"] != second_env["OPENCODE_DB"]
    assert first_env["OPENCODE_WORKSPACE_ID"] == first.run_id
    assert second_env["OPENCODE_WORKSPACE_ID"] == second.run_id
