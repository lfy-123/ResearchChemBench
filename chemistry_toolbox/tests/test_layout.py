from __future__ import annotations

from pathlib import Path

from researchchem_toolbox.paths import CONFIG_ROOT, PROJECT_ROOT, SOURCE_ROOT, TOOLBOX_ROOT


def test_canonical_toolbox_layout_exists():
    assert TOOLBOX_ROOT == PROJECT_ROOT / "chemistry_toolbox"
    assert SOURCE_ROOT == TOOLBOX_ROOT / "src"
    assert CONFIG_ROOT == TOOLBOX_ROOT / "config"
    for relative in ("mcp", "scripts", "tests", "docs", "environment"):
        assert (TOOLBOX_ROOT / relative).is_dir()


def test_legacy_implementation_paths_are_removed():
    legacy_paths = (
        PROJECT_ROOT / "researchchem_toolbox",
        PROJECT_ROOT / "evaluation" / "mcp_tools",
        PROJECT_ROOT / "config",
        PROJECT_ROOT / "environment",
    )
    for legacy in legacy_paths:
        assert not legacy.exists()
        assert not legacy.is_symlink()


def test_runtime_assets_remain_outside_source_tree():
    for relative in (".software_cache", ".model_cache", ".envs"):
        path = PROJECT_ROOT / relative
        assert path.is_dir()
        assert TOOLBOX_ROOT not in path.parents


def test_removed_environment_layouts_do_not_exist():
    for relative in (".venv", ".toolbox_env", ".tool_envs", ".tool_envs_merged", ".conda_envs"):
        assert not (PROJECT_ROOT / relative).exists()


def test_old_document_compatibility_links_are_removed():
    old = PROJECT_ROOT / "docs" / "tools" / "CHEMISTRY_TOOLBOX_REFACTOR_PLAN.md"
    assert not old.exists()
    assert not old.is_symlink()
