from __future__ import annotations

from pathlib import Path

from minichem_toolbox.environment_layout import environment_path
from minichem_toolbox.paths import MODEL_CACHE_ROOT, PROJECT_ROOT, SOFTWARE_CACHE_ROOT, TOOLBOX_ROOT
from minichem_toolbox.runtime import runtime_names, runtime_path
from minichem_mcp_tools.profiles import public_server_spec


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
        "config/merged_environments.yaml",
        ".envs/environment.yml",
        "mcp_tools/tool_config.json",
    ):
        text = (root / relative).read_text(encoding="utf-8")
        assert "/inspire/" not in text
        assert str(root) not in text


def test_public_server_uses_installed_transport_package() -> None:
    command = public_server_spec()["command"]
    assert command[1:3] == ["-m", "minichem_mcp_tools.server"]


def test_subprocess_module_references_use_installed_transport_package() -> None:
    root = Path(__file__).resolve().parents[1]
    for relative in (
        "mcp_tools/async_action_tools.py",
        "mcp_tools/distributed_job_dispatcher.py",
        "mcp_tools/open_execution.py",
        "mcp_tools/profiles.py",
        "mcp_tools/remote_job_launcher.py",
        "src/minichem_toolbox/sandbox_worker_rpc.py",
    ):
        text = (root / relative).read_text(encoding="utf-8")
        assert '"minichem_toolbox.mcp.' not in text
