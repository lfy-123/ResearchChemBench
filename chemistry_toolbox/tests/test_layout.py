from __future__ import annotations

from pathlib import Path

from researchchem_toolbox.paths import CONFIG_ROOT, PROJECT_ROOT, SOURCE_ROOT, TOOLBOX_ROOT


def test_canonical_toolbox_layout_exists():
    assert TOOLBOX_ROOT == PROJECT_ROOT / "chemistry_toolbox"
    assert SOURCE_ROOT == TOOLBOX_ROOT / "src"
    assert CONFIG_ROOT == TOOLBOX_ROOT / "config"
    for relative in ("mcp", "scripts", "tests", "docs", "environment"):
        assert (TOOLBOX_ROOT / relative).is_dir()


def test_legacy_paths_are_compatibility_links():
    mappings = {
        PROJECT_ROOT / "researchchem_toolbox": SOURCE_ROOT / "researchchem_toolbox",
        PROJECT_ROOT / "evaluation" / "mcp_tools": TOOLBOX_ROOT / "mcp",
        PROJECT_ROOT / "config": CONFIG_ROOT,
        PROJECT_ROOT / "environment": TOOLBOX_ROOT / "environment",
    }
    for legacy, canonical in mappings.items():
        assert legacy.is_symlink()
        assert legacy.resolve() == canonical.resolve()


def test_runtime_assets_remain_outside_source_tree():
    for relative in (".software_cache", ".model_cache", ".tool_envs", ".toolbox_env"):
        path = PROJECT_ROOT / relative
        assert path.is_dir()
        assert TOOLBOX_ROOT not in path.parents


def test_old_document_paths_resolve_to_canonical_documents():
    old = PROJECT_ROOT / "docs" / "tools" / "CHEMISTRY_TOOLBOX_REFACTOR_PLAN.md"
    new = TOOLBOX_ROOT / "docs" / "CHEMISTRY_TOOLBOX_REFACTOR_PLAN.md"
    assert old.is_symlink()
    assert old.resolve() == new.resolve()
