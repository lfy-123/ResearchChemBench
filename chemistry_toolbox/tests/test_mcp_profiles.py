from __future__ import annotations

import json
import os
import shutil
from pathlib import Path

from chemistry_toolbox.mcp.profiles import (
    MODEL_CACHE_ENV,
    load_profile_config,
    profile_runtime_environment,
    profile_python,
    public_server_spec,
    project_model_cache_path,
    project_runtime_cache_path,
)
from chemistry_toolbox.src.paths import RUNTIME_CACHE_ENV
from chemistry_toolbox.mcp.discovery_tools import PROGRESSIVE_DISCOVERY_TOOL_NAMES
from chemistry_toolbox.mcp.open_tools import OPEN_EXECUTION_TOOL_NAMES
from chemistry_toolbox.mcp.async_action_tools import ASYNC_ACTION_TOOL_NAMES
from evaluation.execution.runner import TaskRunner
from chemistry_toolbox.src.catalog import action_specs, backend_specs
from chemistry_toolbox.src.environment_layout import software_root
from chemistry_toolbox.src.environment_layout import SOFTWARE_ROOT_ENV
from chemistry_toolbox.src.runtime import runtime_environment, runtime_python


def test_runtimes_cover_each_backend_once():
    config = load_profile_config()
    assignments = config["profiles"]
    assigned = [backend for value in assignments.values() for backend in value["backends"]]
    assert set(assigned) == set(backend_specs())
    assert len(assigned) == len(set(assigned)) == len(backend_specs())
    for runtime, value in assignments.items():
        assert all(backend_specs()[backend].runtime == runtime for backend in value["backends"])


def test_runtimes_have_unique_researchchem_conda_names():
    config = load_profile_config()
    specifications = list(config["profiles"].values())
    names = [specification["conda_name"] for specification in specifications]
    assert len(names) == len(set(names)) == len(specifications)
    assert all(name.startswith("researchchem-") for name in names)


def test_public_server_is_one_progressive_complete_catalog_server():
    spec = public_server_spec()
    assert spec["name"] == "researchchem_toolbox"
    assert spec["profile"] is None
    assert spec["discovery_mode"] == "progressive"
    assert set(spec["tools"]) == (
        set(PROGRESSIVE_DISCOVERY_TOOL_NAMES)
        | set(OPEN_EXECUTION_TOOL_NAMES)
        | set(ASYNC_ACTION_TOOL_NAMES)
    )
    assert "--profile" not in spec["command"]
    assert spec["command"][-2:] == ["--discovery-mode", "progressive"]
    assert "chemistry_toolbox.mcp.server" in spec["command"]


def test_model_profiles_use_ignored_project_model_cache(monkeypatch):
    monkeypatch.delenv(MODEL_CACHE_ENV, raising=False)
    monkeypatch.delenv(RUNTIME_CACHE_ENV, raising=False)
    expected_model_cache = project_model_cache_path()
    expected_runtime_cache = project_runtime_cache_path()
    for name in ("core", "quantum", "mlip", "nequip", "deepmd"):
        environment = profile_runtime_environment(name)
        assert Path(environment[MODEL_CACHE_ENV]) == expected_model_cache
        assert Path(environment[RUNTIME_CACHE_ENV]) == expected_runtime_cache
        assert Path(environment["XDG_CACHE_HOME"]) == expected_runtime_cache
    services = profile_runtime_environment("services")
    assert MODEL_CACHE_ENV not in services
    assert Path(services[RUNTIME_CACHE_ENV]) == expected_runtime_cache
    assert Path(services["XDG_CACHE_HOME"]) == expected_runtime_cache


def test_orca_runtime_injects_exact_binary_and_mpi_paths():
    environment = profile_runtime_environment("quantum")
    worker_environment = runtime_environment("quantum")
    path_entries = environment["PATH"].split(os.pathsep)
    library_entries = environment["LD_LIBRARY_PATH"].split(os.pathsep)
    expected_mpi_bin = str(software_root() / "shared/mpi/openmpi/4.1.8-fortran/bin")
    expected_mpi_lib = str(software_root() / "shared/mpi/openmpi/4.1.8-fortran/lib")
    assert expected_mpi_bin in path_entries
    assert expected_mpi_lib in library_entries
    assert environment["CHEMGRAPH_ORCA_COMMAND"] == str(
        software_root() / "installations/orca/6.1.1/orca"
    )
    assert str(software_root() / "installations/orca/6.1.1") in path_entries
    assert path_entries.index(expected_mpi_bin) < next(
        index
        for index, entry in enumerate(path_entries)
        if entry.endswith(".envs/general-modern-openmpi5/bin")
    )
    assert library_entries.index(expected_mpi_lib) < next(
        index
        for index, entry in enumerate(library_entries)
        if entry.endswith(".envs/general-modern-openmpi5/lib")
    )
    assert Path(shutil.which("mpirun", path=environment["PATH"]) or "") == (
        Path(expected_mpi_bin) / "mpirun"
    )
    assert environment["OPAL_PREFIX"] == str(
        software_root() / "shared/mpi/openmpi/4.1.8-fortran"
    )
    assert "OMPI_MCA_osc" not in environment
    assert environment["OMPI_MCA_pml"] == "ob1"
    assert environment["OMPI_MCA_btl"] == "self,vader,tcp"
    for key in (
        "PATH",
        "LD_LIBRARY_PATH",
        "OPAL_PREFIX",
        "OMPI_MCA_pml",
        "OMPI_MCA_btl",
    ):
        assert worker_environment[key] == environment[key]


def test_openmpi5_general_backends_do_not_inherit_orca_openmpi4():
    environment = profile_runtime_environment("nwchem")
    path_entries = environment["PATH"].split(os.pathsep)
    assert path_entries[0].endswith(
        ".envs/general-modern-openmpi5/bin"
    )
    assert not any(
        entry == str(software_root() / "shared/mpi/openmpi/4.1.8-fortran/bin")
        for entry in path_entries
    )


def test_nwchem_basis_library_preserves_required_directory_separator():
    environment = profile_runtime_environment("nwchem")
    assert environment["NWCHEM_BASIS_LIBRARY"].endswith("/")
    assert Path(environment["NWCHEM_BASIS_LIBRARY"]).is_dir()


def test_runtime_profiles_publish_resolved_software_root():
    expected = str(software_root())
    assert profile_runtime_environment("rmg")[SOFTWARE_ROOT_ENV] == expected
    assert runtime_environment("rmg")[SOFTWARE_ROOT_ENV] == expected


def test_orca_openmpi_runtime_has_required_fortran_capabilities():
    status = json.loads(
        (Path(__file__).parents[1] / "evidence" / "status" / "toolbox_resource_status.json").read_text(
            encoding="utf-8"
        )
    )
    resource = next(
        item
        for item in status["resources"]
        if item["id"] == "openmpi_4_1_8_orca_runtime"
    )
    assert resource["status"] == "pass"
    matched = {
        probe["matched_text"] for probe in resource["capability_probes"]
    }
    assert "Fort mpif.h: yes (all)" in matched
    assert "Fort use mpi: yes" in matched


def test_vasp_runtime_injects_exact_binary_path_without_selecting_potcars():
    environment = profile_runtime_environment("vasp")
    assert environment["CHEMGRAPH_VASP_COMMAND"] == str(
        software_root() / "installations/vasp/6.3.2/bin/vasp_std"
    )
    assert str(software_root() / "installations/vasp/6.3.2/bin") in environment["PATH"].split(os.pathsep)
    assert "POTCAR" not in environment


def test_manual_runtime_paths_are_exact_and_project_relative_values_are_resolved():
    gaussian = profile_runtime_environment("gaussian")
    assert gaussian["CHEMGRAPH_GAUSSIAN_COMMAND"] == str(
        software_root() / "installations/gaussian/g16/install/g16/g16"
    )
    assert Path(gaussian["GAUSS_SCRDIR"]).is_absolute()
    assert gaussian["GAUSS_SCRDIR"] == str(software_root() / "validation/gaussian/g16/scratch")
    gamess = profile_runtime_environment("gamess")
    assert gamess["CHEMGRAPH_GAMESS_COMMAND"] == str(
        software_root() / "installations/gamess/2024-r2-p1/source/rungms"
    )
    assert "GMS_SCRATCH" not in gamess
    assert "GMS_RESTART" not in gamess
    assert "MOLCAS_WORKDIR" not in profile_runtime_environment("openmolcas")
    kinbot_source = software_root() / "installations/kinbot/source-2.2.2"
    assert str(kinbot_source) in profile_runtime_environment("kinbot")[
        "PYTHONPATH"
    ].split(os.pathsep)
    acpype_root = software_root() / "installations/acpype/2023.10.27"
    acpype = profile_runtime_environment("acpype")
    acpype_worker = runtime_environment("acpype")
    expected_python = (acpype_root / "deps/bin/python").resolve()
    assert profile_python("acpype").resolve() == expected_python
    assert runtime_python("acpype").resolve() == expected_python
    assert acpype["CHEMGRAPH_ACPYPE_COMMAND"] == str(
        acpype_root / "python/bin/acpype"
    )
    for environment in (acpype, acpype_worker):
        python_paths = environment["PYTHONPATH"].split(os.pathsep)
        assert str(acpype_root / "python") in python_paths
        assert str(
            Path(".envs/molecular-simulation-openff/lib/python3.12/site-packages").resolve()
        ) in python_paths
        assert str(acpype_root / "deps/lib/python3.12/site-packages") not in python_paths
        assert str(acpype_root / "deps/lib") in environment[
            "LD_LIBRARY_PATH"
        ].split(os.pathsep)
    assert acpype["BABEL_LIBDIR"] == str(acpype_root / "deps/lib/openbabel/3.1.0")
    assert acpype["BABEL_DATADIR"] == str(acpype_root / "deps/share/openbabel/3.1.0")
    assert profile_runtime_environment("namd")["CHEMGRAPH_NAMD_COMMAND"] == str(
        software_root() / "installations/namd/3.0.2/multicore-avx512/namd3"
    )
    amber = profile_runtime_environment("amber")
    assert amber["CHEMGRAPH_AMBER_MPI_EXECUTABLE"] == str(
        software_root() / "installations/amber/26/install/bin/pmemd.MPI"
    )
    assert profile_runtime_environment("charmm")["CHEMGRAPH_CHARMM_COMMAND"] == str(
        software_root() / "installations/charmm/50b2/install/bin/charmm"
    )
    expected_mesmer = str(software_root() / "installations/mesmer/7.1")
    assert profile_runtime_environment("mesmer")["MESMER_DIR"] == expected_mesmer
    assert runtime_environment("mesmer")["MESMER_DIR"] == expected_mesmer


def test_docking_runtime_scopes_cuda_12_libraries_to_gnina_profile():
    docking = profile_runtime_environment("docking")
    libraries = docking["LD_LIBRARY_PATH"].split(os.pathsep)

    for package in (
        "cudnn",
        "cuda_runtime",
        "cublas",
        "cufft",
        "cusparse",
        "cusolver",
        "nvjitlink",
    ):
        expected = Path(
            f".envs/molecular-simulation-openff/lib/python3.12/site-packages/nvidia/{package}/lib"
        ).resolve()
        assert str(expected) in libraries
    assert not any("site-packages/nvidia" in item for item in profile_runtime_environment("quantum")["LD_LIBRARY_PATH"].split(os.pathsep))


def test_native_binary_compatibility_libraries_are_resolved_portably(monkeypatch):
    monkeypatch.delenv("LD_PRELOAD", raising=False)
    runtime_lib = Path(".envs/general-modern-openmpi5/lib").resolve()

    amber_profile = profile_runtime_environment("amber")
    amber_worker = runtime_environment("amber")
    expected_preloads = [
        str((runtime_lib / "libstdc++.so.6").resolve()),
        str((runtime_lib / "libgcc_s.so.1").resolve()),
    ]
    assert amber_profile["LD_PRELOAD"].split(os.pathsep) == expected_preloads
    assert amber_worker["LD_PRELOAD"].split(os.pathsep) == expected_preloads
    assert "LD_PRELOAD" not in profile_runtime_environment("quantum")
    assert "LD_PRELOAD" not in runtime_environment("quantum")

    charmm_library = str(
        software_root() / "installations/charmm/50b2/install/lib"
    )
    charmm_profile = profile_runtime_environment("charmm")
    charmm_worker = runtime_environment("charmm")
    assert charmm_library in charmm_profile["LD_LIBRARY_PATH"].split(os.pathsep)
    assert charmm_library in charmm_worker["LD_LIBRARY_PATH"].split(os.pathsep)


def test_task_workspace_gets_one_server_progressive_prompt_and_complete_catalog(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_MCP_PROFILES", "core,services")
    runner = TaskRunner("Electron_Isodensity_Reproduction_01_Method_Selection", agent_key="opencode", workspace_root=tmp_path)
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
        "Electron_Isodensity_Reproduction_01_Method_Selection",
        agent_key="mock",
        workspace_root=tmp_path,
        tool_discovery_mode="full",
    )
    runner.setup_workspace()
    prompt = (runner.workspace / "INSTRUCTIONS.md").read_text()
    assert all(f"`{action_id}`" in prompt for action_id in action_specs())
    catalog = json.loads((runner.workspace / "_toolbox_catalog.json").read_text())
    assert catalog["discovery_mode"] == "full"
