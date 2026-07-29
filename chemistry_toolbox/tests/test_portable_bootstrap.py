from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]


def load_script(name: str):
    path = ROOT / "chemistry_toolbox" / "scripts" / f"{name}.py"
    specification = importlib.util.spec_from_file_location(name, path)
    assert specification and specification.loader
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


bootstrap = load_script("bootstrap_chemistry_toolbox")
capture = load_script("capture_portable_toolbox_lock")


def test_environment_prefixes_stay_in_managed_roots(tmp_path: Path):
    assert bootstrap.safe_target_prefix(tmp_path, ".toolbox_env") == (
        tmp_path / ".toolbox_env"
    ).resolve()
    assert bootstrap.safe_target_prefix(tmp_path, ".tool_envs/quantum") == (
        tmp_path / ".tool_envs/quantum"
    ).resolve()
    assert bootstrap.safe_target_prefix(
        tmp_path, ".tool_envs_merged/general-modern-openmpi5"
    ) == (tmp_path / ".tool_envs_merged/general-modern-openmpi5").resolve()
    with pytest.raises(bootstrap.BootstrapError):
        bootstrap.safe_target_prefix(tmp_path, "../outside")
    with pytest.raises(bootstrap.BootstrapError):
        bootstrap.safe_target_prefix(tmp_path, "arbitrary-env")


def test_explicit_lock_parser_keeps_artifact_hashes():
    value = """# platform: linux-64
@EXPLICIT
https://example.invalid/a.conda#abc123

"""
    assert bootstrap.explicit_entries(value) == {
        "https://example.invalid/a.conda#abc123"
    }


def test_manifest_can_be_selected_from_platform_root(tmp_path: Path):
    directory = tmp_path / "linux-64"
    directory.mkdir()
    payload = {"schema_version": 1, "lock_platform": "linux-64"}
    (directory / "manifest.json").write_text(json.dumps(payload), encoding="utf-8")
    path, loaded = bootstrap.resolve_manifest(tmp_path, "linux-64")
    assert path == directory / "manifest.json"
    assert loaded == payload


def test_offline_pip_options_use_only_the_wheelhouse(tmp_path: Path):
    arguments = argparse.Namespace(
        offline=True,
        no_index=False,
        wheelhouse=tmp_path / "wheels",
    )
    assert bootstrap.pip_install_options(arguments) == [
        "--no-deps",
        "--no-index",
        "--find-links",
        str((tmp_path / "wheels").resolve()),
    ]


def test_external_asset_symlink_is_lexically_safe(tmp_path: Path):
    external = tmp_path / "external"
    external.mkdir()
    target = tmp_path / "checkout"
    target.mkdir()
    (target / ".software_cache").symlink_to(external, target_is_directory=True)
    path, portable = bootstrap.asset_target(target, ".software_cache")
    assert path == target / ".software_cache"
    assert portable is True


def test_capture_deduplicates_shared_conda_prefixes():
    records = capture.collect_environments()
    prefixes = [item["prefix"] for item in records]
    assert len(prefixes) == len(set(prefixes))
    assert ".toolbox_env" in prefixes
    assert ".tool_envs_merged/general-modern-openmpi5" in prefixes
    deepmd = next(item for item in records if item["prefix"] == ".tool_envs/deepmd")
    assert len(deepmd["declared_by"]) > 1


def test_nested_health_check_commands_are_required_assets():
    assets, _manual = capture.collect_assets(hash_critical_assets=False)
    indexed = {item["path"]: item for item in assets}
    gaussian = ".software_cache/gaussian/g16/install/g16/g16"
    assert indexed[gaussian]["required"] is True
    assert (
        "mcp_profiles.support_environments.gaussian.external_commands"
        in indexed[gaussian]["reasons"]
    )


def test_noneditable_build_path_falls_back_to_exact_index_version(monkeypatch):
    def fake_run(command, **_kwargs):
        if command[-3:] == ["pip", "freeze", "--all"]:
            return "cffi @ file:///temporary/build/cffi\n"
        if command[-4:] == ["pip", "list", "--format", "json"]:
            return json.dumps([{"name": "cffi", "version": "2.0.0"}])
        raise AssertionError(command)

    monkeypatch.setattr(capture, "run", fake_run)
    entries, requirements, project_editable, local_entries = capture.capture_pip_lock(
        Path("/fake/python"),
        [
            {
                "name": "cffi",
                "version": "2.1.0",
                "channel": "pypi",
                "build_string": "pypi_0",
            }
        ],
    )
    assert requirements == ["cffi==2.0.0"]
    assert entries[0]["conda_recorded_version"] == "2.1.0"
    assert entries[0]["kind"] == "index_fallback_from_local"
    assert entries[0]["original_source_kind"] == "file_url_outside_repository"
    assert "original_source_path" not in entries[0]
    assert project_editable is False
    assert local_entries == []
