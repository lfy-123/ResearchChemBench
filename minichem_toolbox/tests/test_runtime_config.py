from __future__ import annotations

from pathlib import Path

from minichem_toolbox.environment_layout import environment_path
from minichem_toolbox.paths import MODEL_CACHE_ROOT, PROJECT_ROOT, SOFTWARE_CACHE_ROOT, TOOLBOX_ROOT
from minichem_toolbox.runtime import runtime_names, runtime_path


def test_default_roots_are_internal() -> None:
    assert PROJECT_ROOT == TOOLBOX_ROOT
    assert SOFTWARE_CACHE_ROOT == TOOLBOX_ROOT / ".mini_software_cache"
    assert MODEL_CACHE_ROOT == TOOLBOX_ROOT / ".mini_model_cache"


def test_all_logical_runtimes_share_one_portable_prefix() -> None:
    expected = TOOLBOX_ROOT / ".envs" / "minichem"
    assert set(runtime_names()) == {
        "core",
        "gaussian",
        "goodvibes",
        "multiwfn",
        "quantum",
        "reaction",
        "sella",
        "workflows",
    }
    for name in runtime_names():
        assert runtime_path(name) == expected
        assert environment_path(name) == expected


def test_active_configuration_uses_relative_cache_paths() -> None:
    root = Path(__file__).resolve().parents[1]
    for relative in (
        "config/mcp_profiles.yaml",
        "environment.yml",
        "requirements.txt",
        "src/minichem_mcp_tools/tool_config.json",
    ):
        text = (root / relative).read_text(encoding="utf-8")
        assert "/inspire/" not in text
        assert str(root) not in text


def test_launcher_uses_installed_transport_package() -> None:
    launcher = (TOOLBOX_ROOT / "scripts" / "start_mcp.sh").read_text(encoding="utf-8")
    assert "-m minichem_mcp_tools.server" in launcher


def test_subprocess_module_references_use_installed_transport_package() -> None:
    root = Path(__file__).resolve().parents[1]
    for relative in (
        "src/minichem_mcp_tools/open_execution.py",
        "src/minichem_toolbox/runtime.py",
        "src/minichem_toolbox/worker_launcher.py",
    ):
        text = (root / relative).read_text(encoding="utf-8")
        assert '"minichem_toolbox.mcp.' not in text
