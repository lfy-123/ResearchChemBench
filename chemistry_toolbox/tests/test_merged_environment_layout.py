from __future__ import annotations

from pathlib import Path

import yaml

from researchchem_toolbox.environment_layout import (
    ENV_ROOT_ENV,
    resolve_configured_path,
    resolve_runtime_path,
)
from researchchem_toolbox.paths import PROJECT_ROOT


def _pip_dependencies(environment_name: str) -> set[str]:
    environment_file = (
        PROJECT_ROOT
        / "chemistry_toolbox/environment/merged"
        / environment_name
        / "environment.yml"
    )
    payload = yaml.safe_load(environment_file.read_text(encoding="utf-8"))
    for dependency in payload["dependencies"]:
        if isinstance(dependency, dict) and "pip" in dependency:
            return set(dependency["pip"])
    return set()


def _requirements(environment_name: str) -> set[str]:
    requirements_file = (
        PROJECT_ROOT
        / "chemistry_toolbox/environment/merged"
        / environment_name
        / "requirements.txt"
    )
    return {
        line.strip()
        for line in requirements_file.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }


def test_runtime_ids_map_to_six_physical_prefixes():
    expected = {
        "core": "general-modern-openmpi5",
        "openff": "molecular-simulation-openff",
        "reaction": "kinetics-legacy",
        "deepmd": "equivariant-ml",
        "cp2k": "periodic-mpich",
        "catmap": "yambo-openmpi4",
    }
    for runtime, basename in expected.items():
        path = resolve_runtime_path(runtime, f".envs/{basename}")
        assert path == (PROJECT_ROOT / ".envs" / basename).resolve()


def test_envs_layout_is_unconditional():
    assert resolve_runtime_path("cp2k", ".envs/periodic-mpich") == (
        PROJECT_ROOT / ".envs/periodic-mpich"
    ).resolve()


def test_cross_runtime_command_paths_use_physical_envs_prefixes():
    assert resolve_configured_path(".envs/periodic-mpich/bin/cp2k") == (
        PROJECT_ROOT / ".envs/periodic-mpich/bin/cp2k"
    ).resolve()
    assert resolve_configured_path(".envs/kinetics-legacy/bin/abinit") == (
        PROJECT_ROOT / ".envs/kinetics-legacy/bin/abinit"
    ).resolve()
    assert resolve_configured_path(".envs/general-modern-openmpi5/lib") == (
        PROJECT_ROOT / ".envs/general-modern-openmpi5/lib"
    ).resolve()


def test_non_environment_project_paths_are_not_rewritten():
    path = resolve_configured_path(".software_cache/orca/6.1.1/orca")
    assert path == (PROJECT_ROOT / ".software_cache/orca/6.1.1/orca").resolve()


def test_environment_root_can_be_relocated(monkeypatch, tmp_path):
    monkeypatch.setenv(ENV_ROOT_ENV, str(tmp_path / "portable-envs"))
    expected_root = (tmp_path / "portable-envs").resolve()
    assert resolve_runtime_path("cp2k", ".envs/periodic-mpich") == (
        expected_root / "periodic-mpich"
    )
    assert resolve_configured_path(".envs/periodic-mpich/bin/cp2k") == (
        expected_root / "periodic-mpich/bin/cp2k"
    )
    assert resolve_configured_path(
        ".envs/general-modern-openmpi5/bin/python"
    ) == (expected_root / "general-modern-openmpi5/bin/python")


def test_repaired_runtime_dependencies_are_portable_build_inputs():
    reaction_dependencies = {
        "censo==2.1.2",
        "CoolProp==8.0.0",
        "numdifftools==0.9.42",
    }
    sharc_dependencies = {
        "numba==0.66.0",
        "llvmlite==0.48.0",
        "netCDF4==1.7.4",
        "cftime==1.6.5",
        "threadpoolctl==3.6.0",
    }

    assert reaction_dependencies <= _pip_dependencies("reaction-kinetics")
    assert reaction_dependencies <= _requirements("reaction-kinetics")
    assert sharc_dependencies <= _pip_dependencies("general-modern-openmpi5")
    assert sharc_dependencies <= _requirements("general-modern-openmpi5")
