from __future__ import annotations

from pathlib import Path

from researchchem_toolbox.environment_layout import (
    ENV_ROOT_ENV,
    resolve_configured_path,
    resolve_runtime_path,
)
from researchchem_toolbox.paths import PROJECT_ROOT


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


def test_external_runtime_preserves_explicit_software_path():
    assert resolve_runtime_path("matlab", ".software_cache/matlab/R2018a/install") == (
        PROJECT_ROOT / ".software_cache/matlab/R2018a/install"
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
