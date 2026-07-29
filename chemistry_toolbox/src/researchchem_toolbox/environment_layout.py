"""Resolve legacy or consolidated chemistry-toolbox runtime prefixes.

The public runtime identifiers (``quantum``, ``md``, ``cp2k`` and so on) stay
stable.  Only their physical Conda prefixes change.  This keeps backend and
Action contracts independent of the deployment layout and allows an operator
to fall back to the legacy prefixes while the consolidated layout is tested.
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from typing import Any

import yaml

from .paths import CONFIG_ROOT, PROJECT_ROOT


ENVIRONMENT_LAYOUT_ENV = "RESEARCHCHEM_ENV_LAYOUT"
MERGED_ENV_ROOT_ENV = "RCB_MERGED_ENV_ROOT"
MERGED_CONFIG_PATH = CONFIG_ROOT / "merged_environments.yaml"
VALID_LAYOUTS = {"auto", "legacy", "merged"}


@lru_cache(maxsize=1)
def load_merged_environment_config() -> dict[str, Any]:
    value = yaml.safe_load(MERGED_CONFIG_PATH.read_text(encoding="utf-8")) or {}
    environments = value.get("environments")
    runtime_mapping = value.get("runtime_mapping")
    if not isinstance(environments, dict) or not isinstance(runtime_mapping, dict):
        raise ValueError(f"Invalid merged environment configuration: {MERGED_CONFIG_PATH}")
    return value


def selected_environment_layout() -> str:
    layout = os.environ.get(ENVIRONMENT_LAYOUT_ENV, "auto").strip().lower() or "auto"
    if layout not in VALID_LAYOUTS:
        choices = ", ".join(sorted(VALID_LAYOUTS))
        raise ValueError(f"{ENVIRONMENT_LAYOUT_ENV} must be one of: {choices}")
    return layout


@lru_cache(maxsize=1)
def _runtime_to_group() -> dict[str, str]:
    config = load_merged_environment_config()
    result: dict[str, str] = {}
    for group, runtimes in config["runtime_mapping"].items():
        if group not in config["environments"]:
            raise ValueError(f"Unknown merged environment group {group!r}")
        for runtime in runtimes or []:
            runtime_name = str(runtime)
            if runtime_name in result:
                raise ValueError(f"Merged runtime {runtime_name!r} is assigned twice")
            result[runtime_name] = str(group)
    return result


def merged_environment_path(runtime: str) -> Path | None:
    group = _runtime_to_group().get(runtime)
    if group is None:
        return None
    return _merged_group_path(group)


def _merged_root_override() -> Path | None:
    value = os.environ.get(MERGED_ENV_ROOT_ENV, "").strip()
    if not value:
        return None
    path = Path(value).expanduser()
    return path.resolve() if path.is_absolute() else (PROJECT_ROOT / path).resolve()


def _merged_group_path(group: str) -> Path:
    configured = Path(str(load_merged_environment_config()["environments"][group]["path"]))
    if override := _merged_root_override():
        return (override / configured.name).resolve()
    return configured.resolve() if configured.is_absolute() else (PROJECT_ROOT / configured).resolve()


def _legacy_path(value: str | Path) -> Path:
    path = Path(value).expanduser()
    return path.resolve() if path.is_absolute() else (PROJECT_ROOT / path).resolve()


def resolve_runtime_path(runtime: str, legacy_value: str | Path) -> Path:
    """Resolve a logical runtime to the selected physical prefix."""

    legacy = _legacy_path(legacy_value)
    layout = selected_environment_layout()
    merged = merged_environment_path(runtime)
    if layout == "legacy" or merged is None:
        return legacy
    if layout == "merged":
        return merged
    return merged if (merged / "bin" / "python").is_file() else legacy


def _group_for_legacy_prefix(relative: Path) -> tuple[str, int] | None:
    """Return a merged group and the number of replaced path components."""

    parts = relative.parts
    if not parts:
        return None
    if parts[0] == ".toolbox_env":
        return "general", 1
    if len(parts) < 2 or parts[0] != ".tool_envs":
        return None
    legacy_name = parts[1]
    aliases = {
        # The old ``deepmd`` prefix was the compiler/runtime environment used
        # by source builds.  DeePMD model inference lived in deepmd_models.
        "deepmd": "general",
        "deepmd_models": "equivariant_ml",
    }
    group = aliases.get(legacy_name) or _runtime_to_group().get(legacy_name)
    return (group, 2) if group else None


def resolve_configured_path(value: str | Path) -> Path:
    """Resolve a configured path and rewrite legacy-prefix references.

    This also handles cross-runtime command paths such as a periodic profile
    referring explicitly to the CP2K or ABINIT executable.
    """

    path = Path(value).expanduser()
    if path.is_absolute() or selected_environment_layout() == "legacy":
        return path.resolve() if path.is_absolute() else (PROJECT_ROOT / path).resolve()
    if path.parts[:1] == (".tool_envs_merged",) and _merged_root_override():
        return (_merged_root_override() / Path(*path.parts[1:])).resolve()
    replacement = _group_for_legacy_prefix(path)
    if replacement is not None:
        group, consumed = replacement
        merged = _merged_group_path(group)
        candidate = merged.joinpath(*path.parts[consumed:]).resolve()
        if selected_environment_layout() == "merged" or (merged / "bin" / "python").is_file():
            return candidate
    return (PROJECT_ROOT / path).resolve()
