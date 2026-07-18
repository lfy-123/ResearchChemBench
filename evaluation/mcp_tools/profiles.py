"""Load dependency-isolated MCP tool profiles and their runtimes."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

from .registry import discovered_module_stems


PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / "config.local.env", override=False)
PROFILE_CONFIG_ENV = "RESEARCHCHEM_MCP_PROFILE_CONFIG"
PROFILE_ENV = "RESEARCHCHEM_MCP_PROFILE"
MODEL_CACHE_ENV = "RESEARCHCHEMBENCH_MODEL_CACHE"
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "config" / "mcp_profiles.yaml"


def profile_config_path() -> Path:
    configured = os.environ.get(PROFILE_CONFIG_ENV, "").strip()
    return Path(configured).expanduser().resolve() if configured else DEFAULT_CONFIG_PATH


def load_profile_config() -> dict[str, Any]:
    path = profile_config_path()
    value = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    profiles = value.get("profiles")
    if not isinstance(profiles, dict) or not profiles:
        raise ValueError(f"Invalid MCP profile configuration: {path}")
    model_cache_root = value.get("model_cache_root", ".model_cache")
    if not isinstance(model_cache_root, str) or not model_cache_root.strip():
        raise ValueError("model_cache_root must be a non-empty path string")
    discovered = set(discovered_module_stems())
    assigned: set[str] = set()
    conda_names: set[str] = set()
    for name, profile in profiles.items():
        if not isinstance(profile, dict):
            raise ValueError(f"Profile {name!r} must be a mapping")
        tools = profile.get("tools")
        if not isinstance(tools, list) or not tools or not all(isinstance(item, str) for item in tools):
            raise ValueError(f"Profile {name!r} tools must be a non-empty string list")
        unknown = sorted(set(tools) - discovered)
        if unknown:
            raise ValueError(f"Profile {name!r} references unknown tools: {unknown}")
        duplicates = sorted(assigned & set(tools))
        if duplicates:
            raise ValueError(f"Tools assigned to more than one MCP profile: {duplicates}")
        assigned.update(tools)
        conda_name = str(profile.get("conda_name") or "").strip()
        if not conda_name:
            raise ValueError(f"Profile {name!r} must declare conda_name")
        if conda_name in conda_names:
            raise ValueError(f"Duplicate conda_name: {conda_name}")
        conda_names.add(conda_name)
        libraries = profile.get("runtime_preload_libraries", [])
        if not isinstance(libraries, list) or not all(
            isinstance(item, str) and item for item in libraries
        ):
            raise ValueError(
                f"Profile {name!r} runtime_preload_libraries must be a string list"
            )
        if not isinstance(profile.get("use_project_model_cache", False), bool):
            raise ValueError(
                f"Profile {name!r} use_project_model_cache must be a boolean"
            )
    missing = sorted(discovered - assigned)
    if missing:
        raise ValueError(f"MCP profiles do not cover discovered tools: {missing}")
    defaults = value.get("default_profiles", [])
    if not isinstance(defaults, list) or any(item not in profiles for item in defaults):
        raise ValueError("default_profiles must reference configured profiles")
    support = value.get("support_environments", {})
    if not isinstance(support, dict):
        raise ValueError("support_environments must be a mapping")
    for name, specification in support.items():
        if not isinstance(specification, dict) or not specification.get("environment"):
            raise ValueError(f"Support environment {name!r} must declare environment")
        conda_name = str(specification.get("conda_name") or "").strip()
        if not conda_name:
            raise ValueError(f"Support environment {name!r} must declare conda_name")
        if conda_name in conda_names:
            raise ValueError(f"Duplicate conda_name: {conda_name}")
        conda_names.add(conda_name)
    return value


def profile_names() -> list[str]:
    return sorted(load_profile_config()["profiles"])


def get_profile(name: str) -> dict[str, Any]:
    profiles = load_profile_config()["profiles"]
    if name not in profiles:
        raise KeyError(f"Unknown MCP profile {name!r}; choose from {sorted(profiles)}")
    value = dict(profiles[name])
    value["name"] = name
    return value


def selected_profile_names(value: str | None = None) -> list[str]:
    config = load_profile_config()
    raw = value if value is not None else os.environ.get("RESEARCHCHEMBENCH_MCP_PROFILES", "")
    names = [item.strip() for item in raw.split(",") if item.strip()] if raw else list(config["default_profiles"])
    unknown = sorted(set(names) - set(config["profiles"]))
    if unknown:
        raise KeyError(f"Unknown MCP profiles: {unknown}")
    return names


def profile_environment_path(profile: dict[str, Any]) -> Path:
    path = Path(str(profile["environment"])).expanduser()
    return path.resolve() if path.is_absolute() else (PROJECT_ROOT / path).resolve()


def profile_python(name: str) -> Path:
    profile = get_profile(name)
    configured = str(profile.get("python") or "").strip()
    if configured:
        path = Path(configured).expanduser()
        return path.resolve() if path.is_absolute() else (PROJECT_ROOT / path).resolve()
    return profile_environment_path(profile) / "bin" / "python"


def project_model_cache_path() -> Path:
    """Return the ignored, project-owned cache for downloaded model assets."""

    configured = os.environ.get(MODEL_CACHE_ENV, "").strip()
    if not configured:
        configured = str(load_profile_config().get("model_cache_root") or ".model_cache")
    path = Path(configured).expanduser()
    return path.resolve() if path.is_absolute() else (PROJECT_ROOT / path).resolve()


def profile_runtime_environment(name: str) -> dict[str, str]:
    profile = get_profile(name)
    environment = profile_environment_path(profile)
    bin_dir = environment / "bin"
    values = {
        PROFILE_ENV: name,
        "PATH": str(bin_dir) + os.pathsep + os.environ.get("PATH", ""),
        "LD_LIBRARY_PATH": str(environment / "lib") + os.pathsep + os.environ.get("LD_LIBRARY_PATH", ""),
    }
    if profile.get("use_project_model_cache", False):
        cache_root = project_model_cache_path()
        cache_root.mkdir(parents=True, exist_ok=True)
        values[MODEL_CACHE_ENV] = str(cache_root)
        # MACE 0.3.16 resolves its cache as $XDG_CACHE_HOME/mace.
        values["XDG_CACHE_HOME"] = str(cache_root)
    for variable, executable in dict(profile.get("command_variables") or {}).items():
        configured = Path(str(executable)).expanduser()
        if configured.is_absolute():
            candidate = configured
        elif configured.parent != Path("."):
            candidate = PROJECT_ROOT / configured
        else:
            candidate = bin_dir / configured
        if candidate.exists():
            values[str(variable)] = str(candidate.resolve())
    return values


def apply_profile(name: str) -> dict[str, Any]:
    profile = get_profile(name)
    os.environ["RESEARCHCHEM_MCP_ENABLED_TOOLS"] = ",".join(profile["tools"])
    os.environ[PROFILE_ENV] = name
    for key, value in profile_runtime_environment(name).items():
        os.environ[key] = value
    return profile


def profile_server_spec(name: str) -> dict[str, Any]:
    profile = get_profile(name)
    python = profile_python(name)
    return {
        "profile": name,
        "name": str(profile["server_name"]),
        "description": str(profile.get("description") or ""),
        "python": str(python),
        "command": [
            str(python),
            "-m",
            "evaluation.mcp_tools.server",
            "--profile",
            name,
            "--transport",
            "stdio",
        ],
        "environment": profile_runtime_environment(name),
        "tools": list(profile["tools"]),
    }
