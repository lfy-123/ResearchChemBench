from __future__ import annotations

import json
import os
from pathlib import Path

from evaluation.mcp_tools.profiles import (
    MODEL_CACHE_ENV,
    load_profile_config,
    profile_runtime_environment,
    public_server_spec,
    project_model_cache_path,
)
from evaluation.run_task import TaskRunner
from researchchem_toolbox.catalog import action_specs, backend_specs


def test_runtimes_cover_each_backend_once():
    config = load_profile_config()
    assignments = {
        **config["profiles"],
        **config["support_environments"],
    }
    assigned = [backend for value in assignments.values() for backend in value["backends"]]
    assert set(assigned) == set(backend_specs())
    assert len(assigned) == len(set(assigned)) == 45
    for runtime, value in assignments.items():
        assert all(backend_specs()[backend].runtime == runtime for backend in value["backends"])


def test_runtimes_have_unique_researchchem_conda_names():
    config = load_profile_config()
    specifications = [*config["profiles"].values(), *config["support_environments"].values()]
    names = [specification["conda_name"] for specification in specifications]
    assert len(names) == len(set(names)) == 13
    assert all(name.startswith("researchchem-") for name in names)


def test_public_server_is_one_full_catalog_server():
    spec = public_server_spec()
    assert spec["name"] == "researchchem_toolbox"
    assert spec["profile"] is None
    assert spec["tools"] == sorted(action_specs())
    assert "--profile" not in spec["command"]


def test_model_profiles_use_ignored_project_model_cache(monkeypatch):
    monkeypatch.delenv(MODEL_CACHE_ENV, raising=False)
    expected = project_model_cache_path()
    for name in ("core", "quantum", "mlip"):
        environment = profile_runtime_environment(name)
        assert Path(environment[MODEL_CACHE_ENV]) == expected
        assert Path(environment["XDG_CACHE_HOME"]) == expected
    assert MODEL_CACHE_ENV not in profile_runtime_environment("services")


def test_task_workspace_gets_one_server_full_prompt_and_catalog(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_MCP_PROFILES", "core,services")
    runner = TaskRunner("ChemGraph_001", agent_key="opencode", workspace_root=tmp_path)
    runner.setup_workspace()
    claude = json.loads((runner.workspace / ".mcp.json").read_text())
    opencode = json.loads((runner.workspace / "opencode.json").read_text())
    assert set(claude["mcpServers"]) == {"researchchem_toolbox"}
    assert set(opencode["mcp"]) == {"researchchem_toolbox"}
    catalog = json.loads((runner.workspace / "_toolbox_catalog.json").read_text())
    assert len(catalog["actions"]) == 44
    prompt = (runner.workspace / "INSTRUCTIONS.md").read_text()
    assert "task-specific tool retrieval" in prompt
    assert "automatic backend selection" in prompt
    assert all(f"`{action_id}`" in prompt for action_id in action_specs())
