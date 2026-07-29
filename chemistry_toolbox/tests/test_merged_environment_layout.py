from __future__ import annotations

from pathlib import Path

import pytest

from researchchem_toolbox.environment_layout import (
    ENVIRONMENT_LAYOUT_ENV,
    MERGED_ENV_ROOT_ENV,
    resolve_configured_path,
    resolve_runtime_path,
    selected_environment_layout,
)
from researchchem_toolbox.paths import PROJECT_ROOT


def test_merged_layout_maps_logical_runtimes_to_six_physical_prefixes(monkeypatch):
    monkeypatch.setenv(ENVIRONMENT_LAYOUT_ENV, "merged")
    expected = {
        "core": "general-modern-openmpi5",
        "openff": "molecular-simulation-openff",
        "reaction": "kinetics-legacy",
        "deepmd": "equivariant-ml",
        "cp2k": "periodic-mpich",
        "catmap": "yambo-openmpi4",
    }
    for runtime, basename in expected.items():
        path = resolve_runtime_path(runtime, f".tool_envs/{runtime}")
        assert path == (PROJECT_ROOT / ".tool_envs_merged" / basename).resolve()


def test_legacy_layout_preserves_original_runtime_prefix(monkeypatch):
    monkeypatch.setenv(ENVIRONMENT_LAYOUT_ENV, "legacy")
    assert resolve_runtime_path("cp2k", ".tool_envs/cp2k") == (
        PROJECT_ROOT / ".tool_envs/cp2k"
    ).resolve()


def test_merged_layout_rewrites_cross_runtime_command_paths(monkeypatch):
    monkeypatch.setenv(ENVIRONMENT_LAYOUT_ENV, "merged")
    assert resolve_configured_path(".tool_envs/cp2k/bin/cp2k") == (
        PROJECT_ROOT / ".tool_envs_merged/periodic-mpich/bin/cp2k"
    ).resolve()
    assert resolve_configured_path(".tool_envs/abinit/bin/abinit") == (
        PROJECT_ROOT / ".tool_envs_merged/kinetics-legacy/bin/abinit"
    ).resolve()
    assert resolve_configured_path(".tool_envs/deepmd/lib") == (
        PROJECT_ROOT / ".tool_envs_merged/general-modern-openmpi5/lib"
    ).resolve()


def test_non_environment_project_paths_are_not_rewritten(monkeypatch):
    monkeypatch.setenv(ENVIRONMENT_LAYOUT_ENV, "merged")
    path = resolve_configured_path(".software_cache/orca/6.1.1/orca")
    assert path == (PROJECT_ROOT / ".software_cache/orca/6.1.1/orca").resolve()


def test_merged_root_can_be_relocated_for_portable_rebuilds(monkeypatch, tmp_path):
    monkeypatch.setenv(ENVIRONMENT_LAYOUT_ENV, "merged")
    monkeypatch.setenv(MERGED_ENV_ROOT_ENV, str(tmp_path / "portable-envs"))
    expected_root = (tmp_path / "portable-envs").resolve()
    assert resolve_runtime_path("cp2k", ".tool_envs/cp2k") == (
        expected_root / "periodic-mpich"
    )
    assert resolve_configured_path(".tool_envs/cp2k/bin/cp2k") == (
        expected_root / "periodic-mpich/bin/cp2k"
    )
    assert resolve_configured_path(
        ".tool_envs_merged/general-modern-openmpi5/bin/python"
    ) == (expected_root / "general-modern-openmpi5/bin/python")


def test_invalid_environment_layout_is_rejected(monkeypatch):
    monkeypatch.setenv(ENVIRONMENT_LAYOUT_ENV, "unsupported")
    with pytest.raises(ValueError, match=ENVIRONMENT_LAYOUT_ENV):
        selected_environment_layout()
