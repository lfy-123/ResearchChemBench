from __future__ import annotations

from pathlib import Path

import yaml

from chemistry_toolbox.src.environment_layout import (
    ENV_ROOT_ENV,
    SOFTWARE_ROOT_ENV,
    _runtime_to_group,
    resolve_configured_path,
    resolve_runtime_path,
    software_root,
)
from chemistry_toolbox.src.paths import PROJECT_ROOT
from chemistry_toolbox.src.runtime import runtime_names


def _pip_dependencies(environment_name: str) -> set[str]:
    environment_file = (
        PROJECT_ROOT
        / "chemistry_toolbox/environment"
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
        / "chemistry_toolbox/environment"
        / environment_name
        / "requirements.txt"
    )
    return {
        line.strip()
        for line in requirements_file.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    }


def test_runtime_ids_map_to_seven_physical_prefixes():
    expected = {
        "core": "general-modern-openmpi5",
        "openff": "molecular-simulation-openff",
        "reaction": "kinetics-legacy",
        "deepmd": "equivariant-ml",
        "cp2k": "periodic-mpich",
        "catmap": "yambo-openmpi4",
        "gmx_mmpbsa": "gmx-mmpbsa",
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


def test_managed_software_paths_follow_the_configured_root():
    path = resolve_configured_path(".software_cache/installations/orca/6.1.1/orca")
    assert path == (software_root() / "installations/orca/6.1.1/orca").resolve()


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
    for runtime in runtime_names():
        assert resolve_runtime_path(runtime, ".envs/ignored").is_relative_to(expected_root)


def test_v2_software_root_relocates_legacy_and_managed_paths(monkeypatch, tmp_path):
    root = tmp_path / "portable-software"
    root.mkdir()
    (root / ".layout.json").write_text("{}\n", encoding="utf-8")
    monkeypatch.setenv(SOFTWARE_ROOT_ENV, str(root))

    legacy_path = (".software_" + "cache") + "/orca/6.1.1/orca"
    assert resolve_configured_path(legacy_path) == (
        root / "installations/orca/6.1.1/orca"
    )
    assert resolve_configured_path(
        ".software_cache/installations/orca/6.1.1/orca"
    ) == (root / "installations/orca/6.1.1/orca")
    assert resolve_configured_path(".software_cache/shared/scientific-data/gpaw-setups") == (
        root / "shared/scientific-data/gpaw-setups"
    )


def test_every_runtime_has_one_consolidated_environment_mapping():
    assert set(runtime_names()) == set(_runtime_to_group())


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
