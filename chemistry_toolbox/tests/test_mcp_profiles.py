from __future__ import annotations

import json
import os
from pathlib import Path

from chemistry_toolbox.mcp.profiles import (
    MODEL_CACHE_ENV,
    load_profile_config,
    profile_runtime_environment,
    public_server_spec,
    project_model_cache_path,
)
from chemistry_toolbox.mcp.discovery_tools import PROGRESSIVE_DISCOVERY_TOOL_NAMES
from chemistry_toolbox.mcp.open_tools import OPEN_EXECUTION_TOOL_NAMES
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
    assert len(assigned) == len(set(assigned)) == len(backend_specs())
    for runtime, value in assignments.items():
        assert all(backend_specs()[backend].runtime == runtime for backend in value["backends"])


def test_runtimes_have_unique_researchchem_conda_names():
    config = load_profile_config()
    specifications = [*config["profiles"].values(), *config["support_environments"].values()]
    names = [specification["conda_name"] for specification in specifications]
    assert len(names) == len(set(names)) == len(specifications)
    assert all(name.startswith("researchchem-") for name in names)


def test_public_server_is_one_progressive_complete_catalog_server():
    spec = public_server_spec()
    assert spec["name"] == "researchchem_toolbox"
    assert spec["profile"] is None
    assert spec["discovery_mode"] == "progressive"
    assert set(spec["tools"]) == set(PROGRESSIVE_DISCOVERY_TOOL_NAMES) | set(
        OPEN_EXECUTION_TOOL_NAMES
    )
    assert "--profile" not in spec["command"]
    assert spec["command"][-2:] == ["--discovery-mode", "progressive"]
    assert "chemistry_toolbox.mcp.server" in spec["command"]


def test_model_profiles_use_ignored_project_model_cache(monkeypatch):
    monkeypatch.delenv(MODEL_CACHE_ENV, raising=False)
    expected = project_model_cache_path()
    for name in ("core", "quantum", "mlip", "nequip", "deepmd"):
        environment = profile_runtime_environment(name)
        assert Path(environment[MODEL_CACHE_ENV]) == expected
        assert Path(environment["XDG_CACHE_HOME"]) == expected
    assert MODEL_CACHE_ENV not in profile_runtime_environment("services")


def test_orca_runtime_injects_exact_binary_and_mpi_paths():
    environment = profile_runtime_environment("quantum")
    assert environment["CHEMGRAPH_ORCA_COMMAND"].endswith(
        ".software_cache/orca/6.1.1/orca"
    )
    assert ".software_cache/orca/6.1.1" in environment["PATH"]
    assert ".software_cache/openmpi/4.1.8/bin" in environment["PATH"]
    assert ".software_cache/openmpi/4.1.8/lib" in environment["LD_LIBRARY_PATH"]


def test_vasp_runtime_injects_exact_binary_path_without_selecting_potcars():
    environment = profile_runtime_environment("vasp")
    assert environment["CHEMGRAPH_VASP_COMMAND"].endswith(
        ".software_cache/vasp/6.3.2/bin/vasp_std"
    )
    assert ".software_cache/vasp/6.3.2/bin" in environment["PATH"]
    assert "POTCAR" not in environment


def test_manual_runtime_paths_are_exact_and_project_relative_values_are_resolved():
    gaussian = profile_runtime_environment("gaussian")
    assert gaussian["CHEMGRAPH_GAUSSIAN_COMMAND"].endswith(
        ".software_cache/gaussian/g16/install/g16/g16"
    )
    assert Path(gaussian["GAUSS_SCRDIR"]).is_absolute()
    assert gaussian["GAUSS_SCRDIR"].endswith(
        ".software_cache/gaussian/g16/scratch"
    )
    assert profile_runtime_environment("gamess")["CHEMGRAPH_GAMESS_COMMAND"].endswith(
        ".software_cache/gamess/2024-r2-p1/source/rungms"
    )
    assert profile_runtime_environment("namd")["CHEMGRAPH_NAMD_COMMAND"].endswith(
        ".software_cache/namd/3.0.2/multicore-avx512/namd3"
    )
    amber = profile_runtime_environment("amber")
    assert amber["CHEMGRAPH_AMBER_MPI_EXECUTABLE"].endswith(
        ".software_cache/amber/26/install/bin/pmemd.MPI"
    )
    assert profile_runtime_environment("charmm")["CHEMGRAPH_CHARMM_COMMAND"].endswith(
        ".software_cache/charmm/50b2/install/bin/charmm"
    )


def test_task_workspace_gets_one_server_progressive_prompt_and_complete_catalog(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_MCP_PROFILES", "core,services")
    runner = TaskRunner("ChemGraph_001", agent_key="opencode", workspace_root=tmp_path)
    runner.setup_workspace()
    claude = json.loads((runner.workspace / ".mcp.json").read_text())
    opencode = json.loads((runner.workspace / "opencode.json").read_text())
    assert set(claude["mcpServers"]) == {"researchchem_toolbox"}
    assert set(opencode["mcp"]) == {"researchchem_toolbox"}
    catalog = json.loads((runner.workspace / "_toolbox_catalog.json").read_text())
    assert len(catalog["actions"]) == len(action_specs())
    assert catalog["discovery_mode"] == "progressive"
    prompt = (runner.workspace / "INSTRUCTIONS.md").read_text()
    assert "task-specific retrieval" in prompt
    assert "automatic backend selection" in prompt
    assert "`calculate_energy`" not in prompt
    assert "search_actions" in prompt


def test_task_workspace_can_preserve_full_compatibility_prompt(tmp_path):
    runner = TaskRunner(
        "ChemGraph_001",
        agent_key="mock",
        workspace_root=tmp_path,
        tool_discovery_mode="full",
    )
    runner.setup_workspace()
    prompt = (runner.workspace / "INSTRUCTIONS.md").read_text()
    assert all(f"`{action_id}`" in prompt for action_id in action_specs())
    catalog = json.loads((runner.workspace / "_toolbox_catalog.json").read_text())
    assert catalog["discovery_mode"] == "full"
