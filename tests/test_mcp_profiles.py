from __future__ import annotations

import asyncio
import json
import os
from pathlib import Path

from fastmcp import Client

from evaluation.mcp_tools.profiles import (
    MODEL_CACHE_ENV,
    load_profile_config,
    project_model_cache_path,
    profile_runtime_environment,
    profile_server_spec,
)
from evaluation.mcp_tools.registry import discovered_module_stems
from evaluation.mcp_tools.server import create_server
from evaluation.run_task import TaskRunner


def test_profiles_cover_each_tool_once():
    config = load_profile_config()
    assigned = [
        tool
        for profile in config["profiles"].values()
        for tool in profile["tools"]
    ]
    assert sorted(assigned) == discovered_module_stems()
    assert len(assigned) == len(set(assigned)) == 41


def test_profiles_have_unique_researchchem_conda_names():
    config = load_profile_config()
    specifications = [
        *config["profiles"].values(),
        *config["support_environments"].values(),
    ]
    names = [specification["conda_name"] for specification in specifications]
    assert len(names) == len(set(names)) == 13
    assert all(name.startswith("researchchem-") for name in names)


def test_profile_server_lists_only_profile_tools(monkeypatch):
    variables = {
        "RESEARCHCHEM_MCP_ENABLED_TOOLS",
        "RESEARCHCHEM_MCP_PROFILE",
        *profile_runtime_environment("core"),
    }
    previous = {key: os.environ.get(key) for key in variables}
    monkeypatch.delenv("RESEARCHCHEM_MCP_ENABLED_TOOLS", raising=False)
    server = create_server("core")

    async def collect():
        async with Client(server) as client:
            return {tool.name for tool in await client.list_tools()}

    actual = asyncio.run(collect())
    for key, value in previous.items():
        if value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = value
    expected = set(load_profile_config()["profiles"]["core"]["tools"])
    assert actual == expected


def test_profile_server_spec_uses_profile_python():
    spec = profile_server_spec("services")
    assert spec["name"] == "researchchem_services"
    assert spec["command"][-4:] == [
        "--profile",
        "services",
        "--transport",
        "stdio",
    ]
    assert spec["environment"]["RESEARCHCHEM_MCP_PROFILE"] == "services"
    assert "MP_API_KEY" not in spec["environment"]


def test_mace_profiles_use_ignored_project_model_cache(monkeypatch):
    monkeypatch.delenv(MODEL_CACHE_ENV, raising=False)
    expected = project_model_cache_path()
    assert expected.name == ".model_cache"
    for name in ("core", "quantum", "mlip"):
        environment = profile_runtime_environment(name)
        assert Path(environment[MODEL_CACHE_ENV]) == expected
        assert Path(environment["XDG_CACHE_HOME"]) == expected
    assert MODEL_CACHE_ENV not in profile_runtime_environment("services")


def test_periodic_profile_resolves_cross_environment_commands():
    environment = profile_runtime_environment("periodic")
    assert Path(environment["CHEMGRAPH_QE_COMMAND"]).name == "pw.x"
    assert Path(environment["CHEMGRAPH_CP2K_COMMAND"]).name in {"cp2k", "cp2k.psmp"}
    assert Path(environment["CHEMGRAPH_ABINIT_COMMAND"]).name == "abinit"
    assert all(Path(environment[name]).is_file() for name in (
        "CHEMGRAPH_QE_COMMAND",
        "CHEMGRAPH_CP2K_COMMAND",
        "CHEMGRAPH_ABINIT_COMMAND",
    ))


def test_agent_configs_support_multiple_profile_servers(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_MCP_PROFILES", "core,services")
    runner = TaskRunner("ChemGraph_001", agent_key="opencode", workspace_root=tmp_path)
    runner.setup_workspace()

    claude = json.loads((runner.workspace / ".mcp.json").read_text())
    assert set(claude["mcpServers"]) == {"researchchem_core", "researchchem_services"}

    opencode = json.loads((runner.workspace / "opencode.json").read_text())
    assert set(opencode["mcp"]) == {"researchchem_core", "researchchem_services"}
