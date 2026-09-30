import pytest

from evaluation.execution.runner import TaskRunner
from test_task_package_v19 import package


def test_wait_policy_frozen_and_only_waits_direct(tmp_path, monkeypatch):
    root = tmp_path / "tasks"
    package(root)
    monkeypatch.setattr("evaluation.execution.wait_policy.probe_cli", lambda exe: {"stdout": "codex-cli 0.154.0", "resolved_executable": "codex"})
    runner = TaskRunner("paper_fixture", task_type="autonomous_research", agent_key="codex", task_roots=[str(root)],
        workspace_root=tmp_path / "runs", model_wait_strategy="host_event_wait", timeout_seconds=90, mcp_tool_timeout_ms=600000)
    runner.workspace.mkdir(parents=True)
    runner.instructions_path.write_text("fixture")
    specs = runner._mcp_server_specs()
    assert specs[0]["disabled_tools"] == ["wait_execution_jobs", "wait_execution_events"]
    assert specs[1]["name"] == "chemistry_wait"
    assert specs[1]["command"][-1] == "--wait-only"
    assert specs[1]["environment"]["RESEARCHCHEMBENCH_JOB_WAIT_MODE"] == "event"
    assert runner._run_config()["model_wait_strategy"] == "host_event_wait"
    assert 'features.code_mode.direct_only_tool_namespaces=["mcp__chemistry_wait"]' in runner.build_agent_argv()


def test_unsupported_host_is_not_silently_downgraded(monkeypatch):
    from evaluation.execution.wait_policy import codex_wait_capability
    monkeypatch.setattr("evaluation.execution.wait_policy.probe_cli", lambda exe: {"stdout": "codex-cli 0.100.0", "resolved_executable": "codex"})
    with pytest.raises(ValueError, match="requires Codex"):
        codex_wait_capability("codex")
