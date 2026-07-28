import hashlib
import json
import os
import signal
import sqlite3
import sys
from pathlib import Path
from zipfile import ZipFile

import pytest

from evaluation.config import DEFAULT_MCP_TOOL_TIMEOUT_MS
from evaluation.run_task import TaskRunner


def _archive_runner(tmp_path: Path, members: dict[str, str]) -> TaskRunner:
    runner = TaskRunner("ChemGraph_001", agent_key="mock", workspace_root=tmp_path)
    runner.workspace.mkdir(parents=True)
    data = runner.workspace / "data"
    data.mkdir()
    archive_path = data / "input.zip"
    with ZipFile(archive_path, "w") as archive:
        for name, content in members.items():
            archive.writestr(name, content)
    runner.task_info["archive_extractions"] = [
        {
            "source": "input.zip",
            "destination": "expanded",
            "format": "zip",
            "sha256": hashlib.sha256(archive_path.read_bytes()).hexdigest(),
        }
    ]
    return runner


def test_workspace_does_not_copy_hidden_ground_truth(tmp_path: Path):
    runner = TaskRunner("ChemGraph_001", agent_key="mock", workspace_root=tmp_path)
    runner.setup_workspace()
    assert runner.instructions_path.is_file()
    assert not (runner.workspace / "target_study").exists()
    assert (runner.workspace / "report").is_dir()
    assert (runner.workspace / ".mcp.json").is_file()
    mcp_config = json.loads((runner.workspace / ".mcp.json").read_text())
    assert "chemistry_toolbox.mcp.server" in mcp_config["mcpServers"]["researchchem_toolbox"]["args"]


def test_resource_budget_is_visible_and_recorded_end_to_end(tmp_path: Path):
    runner = TaskRunner(
        "ChemGraph_001",
        agent_key="mock",
        workspace_root=tmp_path,
        available_cpu_cores=12,
        available_memory_mb=24576,
        available_gpu_count=1,
    )
    runner.setup_workspace()

    instructions = runner.instructions_path.read_text(encoding="utf-8")
    assert "CPU: 12 logical cores" in instructions
    assert "Memory: 24576 MiB" in instructions
    assert "GPU: 1" in instructions
    catalog = json.loads((runner.workspace / "_toolbox_catalog.json").read_text())
    assert catalog["evaluation_resource_budget"]["cpu_cores"] == 12
    environment = runner._agent_environment()
    assert environment["RESEARCHCHEMBENCH_AVAILABLE_CPU_CORES"] == "12"
    assert environment["RESEARCHCHEMBENCH_AVAILABLE_MEMORY_MB"] == "24576"
    assert environment["RESEARCHCHEMBENCH_AVAILABLE_GPU_COUNT"] == "1"
    runner._write_meta("prepared")
    meta = json.loads(runner.meta_path.read_text())
    assert meta["resource_budget"] == runner.resource_budget_record()


def test_task_archive_is_hash_checked_and_safely_extracted(tmp_path: Path):
    runner = _archive_runner(tmp_path, {"nested/evidence.txt": "scientific evidence"})
    runner._extract_task_archives()
    assert (
        runner.workspace / "data" / "expanded" / "nested" / "evidence.txt"
    ).read_text() == "scientific evidence"


def test_task_archive_rejects_path_traversal(tmp_path: Path):
    runner = _archive_runner(tmp_path, {"../ground_truth.json": "hidden"})
    with pytest.raises(ValueError, match="Unsafe task archive member"):
        runner._extract_task_archives()
    assert not (runner.workspace / "data" / "expanded").exists()


def test_mock_agent_end_to_end(tmp_path: Path):
    runner = TaskRunner("ChemGraph_001", agent_key="mock", workspace_root=tmp_path)
    meta = runner.run()
    assert meta["status"] == "completed"
    assert meta["exit_code"] == 0
    assert (runner.workspace / "report" / "report.md").is_file()
    events = [json.loads(line) for line in runner.output_path.read_text().splitlines()]
    assert events[-1]["type"] == "result"
    trajectory = runner.workspace / "_model_io.jsonl"
    assert trajectory.is_file()
    manifest = json.loads(trajectory.read_text().splitlines()[0])
    assert manifest["format_version"] == "researchchembench.model_io.v1"
    assert meta["model_io_trace"]["path"] == str(trajectory)


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
    assert (
        config["mcp"]["researchchem_toolbox"]["timeout"]
        == DEFAULT_MCP_TOOL_TIMEOUT_MS
    )
    assert config["model"] == "deepseek/deepseek-v4-flash"
    assert config["provider"]["deepseek"]["options"]["apiKey"] == (
        "{env:OPENAI_API_KEY}"
    )
    assert config["agent"]["build"]["steps"] == opencode.max_turns
    assert config["agent"]["general"]["steps"] == opencode.max_turns


def test_agent_environment_does_not_receive_judge_key(tmp_path: Path, monkeypatch):
    monkeypatch.setenv("JUDGE_API_KEY", "private-judge-key")
    monkeypatch.setenv("OPENAI_API_KEY", "agent-auth-key")
    runner = TaskRunner("ChemGraph_001", agent_key="mock", workspace_root=tmp_path)
    runner.setup_workspace()
    env = runner._agent_environment()
    assert "JUDGE_API_KEY" not in env
    assert env["OPENAI_API_KEY"] == "agent-auth-key"
    assert env["RESEARCHCHEMBENCH_WORKSPACE"] == str(runner.workspace.resolve())


def test_concurrent_opencode_runs_use_isolated_databases(
    tmp_path: Path, monkeypatch
):
    runtime_root = tmp_path / "opencode-runtime"
    monkeypatch.setenv(
        "RESEARCHCHEMBENCH_OPENCODE_RUNTIME_ROOT", str(runtime_root)
    )
    first = TaskRunner("ChemGraph_005", agent_key="opencode", workspace_root=tmp_path)
    second = TaskRunner("ChemGraph_024", agent_key="opencode", workspace_root=tmp_path)
    first.setup_workspace()
    second.setup_workspace()

    first_env = first._agent_environment()
    second_env = second._agent_environment()
    assert first_env["OPENCODE_DB"] == str(
        (runtime_root / first.run_id / "opencode.db").resolve()
    )
    assert second_env["OPENCODE_DB"] == str(
        (runtime_root / second.run_id / "opencode.db").resolve()
    )
    assert first_env["OPENCODE_DB"] != second_env["OPENCODE_DB"]
    assert "OPENCODE_WORKSPACE_ID" not in first_env
    assert "OPENCODE_WORKSPACE_ID" not in second_env


def test_opencode_database_is_archived_from_local_runtime(
    tmp_path: Path, monkeypatch
):
    runtime_root = tmp_path / "opencode-runtime"
    monkeypatch.setenv(
        "RESEARCHCHEMBENCH_OPENCODE_RUNTIME_ROOT", str(runtime_root)
    )
    runner = TaskRunner("ChemGraph_005", agent_key="opencode", workspace_root=tmp_path)
    runner.setup_workspace()
    environment = runner._agent_environment()
    runtime_database = Path(environment["OPENCODE_DB"])
    with sqlite3.connect(runtime_database) as connection:
        connection.execute("CREATE TABLE messages (value TEXT)")
        connection.execute("INSERT INTO messages VALUES ('persisted')")

    result = runner._sync_opencode_database()

    archived = runner.workspace / "_opencode" / "opencode.db"
    assert result["status"] == "archived"
    assert archived.is_file()
    with sqlite3.connect(archived) as connection:
        assert connection.execute("SELECT value FROM messages").fetchone() == (
            "persisted",
        )
    assert not runtime_database.parent.exists()


def test_opencode_command_qualifies_bare_deepseek_model(tmp_path: Path, monkeypatch):
    monkeypatch.setattr("evaluation.run_task.OPENCODE_MODEL", "deepseek-v4-flash")
    runner = TaskRunner("ChemGraph_005", agent_key="opencode", workspace_root=tmp_path)
    runner.setup_workspace()

    command = runner.build_agent_argv()

    assert command[command.index("--model") + 1] == "deepseek/deepseek-v4-flash"
    assert "--auto" in command


@pytest.mark.skipif(os.name != "posix", reason="POSIX process-group behavior")
def test_runner_terminates_the_dedicated_process_group(tmp_path: Path, monkeypatch):
    runner = TaskRunner("ChemGraph_001", agent_key="mock", workspace_root=tmp_path)

    class ProcessStub:
        pid = 12345

        @staticmethod
        def poll():
            return None

        @staticmethod
        def terminate():
            raise AssertionError("POSIX process groups should be terminated with killpg")

        @staticmethod
        def kill():
            raise AssertionError("POSIX process groups should be killed with killpg")

    calls = []
    runner.process = ProcessStub()  # type: ignore[assignment]
    runner.process_group_id = 12345
    monkeypatch.setattr(os, "killpg", lambda pgid, sig: calls.append((pgid, sig)))

    runner._terminate_process_tree()
    runner._terminate_process_tree(force=True)

    assert calls == [(12345, signal.SIGTERM), (12345, signal.SIGKILL)]


@pytest.mark.skipif(os.name != "posix", reason="POSIX process-group behavior")
def test_runner_cancels_detached_execution_jobs(tmp_path: Path, monkeypatch):
    runner = TaskRunner("ChemGraph_001", agent_key="mock", workspace_root=tmp_path)
    job_root = runner.workspace / "outputs" / "execution_jobs"
    running = job_root / "job_running" / "status.json"
    terminal = job_root / "job_finished" / "status.json"
    running.parent.mkdir(parents=True)
    terminal.parent.mkdir(parents=True)
    running.write_text(
        json.dumps(
            {
                "job_id": "job_running",
                "status": "running",
                "supervisor_pid": 12345,
                "child_pid": 23456,
            }
        )
        + "\n"
    )
    terminal.write_text(
        json.dumps(
            {
                "job_id": "job_finished",
                "status": "success",
                "supervisor_pid": 34567,
            }
        )
        + "\n"
    )
    signals = []
    group_signals = []
    monkeypatch.setattr(os, "kill", lambda pid, sig: signals.append((pid, sig)))
    monkeypatch.setattr(
        os, "killpg", lambda pgid, sig: group_signals.append((pgid, sig))
    )

    summary = runner._cancel_workspace_execution_jobs(
        reason="timeout", grace_seconds=0
    )

    assert summary["discovered_jobs"] == 2
    assert summary["active_jobs"] == 1
    assert summary["already_terminal_jobs"] == 1
    assert summary["termination_signals_sent"] == 1
    assert summary["forced_jobs"] == 1
    assert summary["cancelled_jobs"] == 1
    assert signals == [
        (12345, signal.SIGTERM),
        (12345, signal.SIGKILL),
    ]
    assert group_signals == [(23456, signal.SIGKILL)]
    updated = json.loads(running.read_text())
    assert updated["status"] == "cancelled"
    assert updated["error"]["code"] == "benchmark_run_terminated"
    assert updated["benchmark_cleanup"] == {
        "reason": "timeout",
        "forced": True,
    }
    assert json.loads(terminal.read_text())["status"] == "success"


def test_runner_timeout_records_background_job_cleanup(tmp_path: Path, monkeypatch):
    runner = TaskRunner(
        "ChemGraph_001",
        agent_key="mock",
        workspace_root=tmp_path,
        timeout_seconds=0.01,
    )
    runner.setup_workspace()
    monkeypatch.setattr(
        runner,
        "build_agent_argv",
        lambda: [sys.executable, "-c", "import time; time.sleep(30)"],
    )
    cleanup_calls = []

    def cleanup(*, reason: str, grace_seconds: float = 7.0):
        cleanup_calls.append((reason, grace_seconds))
        return {
            "reason": reason,
            "discovered_jobs": 1,
            "active_jobs": 1,
            "cancelled_jobs": 1,
        }

    monkeypatch.setattr(runner, "_cancel_workspace_execution_jobs", cleanup)

    meta = runner.run()

    assert meta["status"] == "failed"
    assert meta["termination"] == "timeout"
    assert cleanup_calls == [("timeout", 7.0)]
    assert meta["background_job_cleanup"]["cancelled_jobs"] == 1
