"""Load dependency-isolated backend runtimes without filtering public tools."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

from chemistry_toolbox.src.catalog import (
    TOOL_DISCOVERY_MODE_ENV,
    action_specs,
    backend_specs,
    resolve_tool_discovery_mode,
)
from chemistry_toolbox.src.environment_layout import (
    SOFTWARE_ROOT_ENV,
    resolve_configured_path,
    resolve_runtime_path,
    software_root,
)
from chemistry_toolbox.src.paths import (
    CONFIG_ROOT,
    MODEL_CACHE_ENV,
    PROJECT_ROOT,
    RUNTIME_CACHE_ENV,
)


load_dotenv(PROJECT_ROOT / "config.local.env", override=False)
PROFILE_CONFIG_ENV = "RESEARCHCHEM_MCP_PROFILE_CONFIG"
PROFILE_ENV = "RESEARCHCHEM_BACKEND_RUNTIME"
DEFAULT_CONFIG_PATH = CONFIG_ROOT / "mcp_profiles.yaml"


def profile_config_path() -> Path:
    configured = os.environ.get(PROFILE_CONFIG_ENV, "").strip()
    return Path(configured).expanduser().resolve() if configured else DEFAULT_CONFIG_PATH


def load_profile_config() -> dict[str, Any]:
    path = profile_config_path()
    value = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    profiles = value.get("profiles")
    if not isinstance(profiles, dict) or not profiles:
        raise ValueError(f"Invalid backend runtime configuration: {path}")
    public_server = value.get("public_server")
    if not isinstance(public_server, dict) or public_server.get("runtime") not in profiles:
        raise ValueError("public_server.runtime must reference a configured profile")

    expected = backend_specs()
    assigned: dict[str, str] = {}
    conda_names: set[str] = set()
    for name, profile in profiles.items():
        group_name = "profiles"
        if not isinstance(profile, dict):
            raise ValueError(f"{group_name}.{name} must be a mapping")
        backends = profile.get("backends")
        if not isinstance(backends, list) or not backends or not all(
            isinstance(item, str) and item for item in backends
        ):
            raise ValueError(f"{group_name}.{name}.backends must be a non-empty string list")
        if len(backends) != len(set(backends)):
            raise ValueError(f"{group_name}.{name}.backends contains duplicates")
        for backend_id in backends:
            if backend_id not in expected:
                raise ValueError(f"Unknown backend {backend_id!r} in runtime {name}")
            if backend_id in assigned:
                raise ValueError(
                    f"Backend {backend_id!r} assigned to both {assigned[backend_id]} and {name}"
                )
            if expected[backend_id].runtime != name:
                raise ValueError(
                    f"BackendSpec {backend_id} declares runtime {expected[backend_id].runtime}, "
                    f"but config assigns it to {name}"
                )
            assigned[backend_id] = name
        conda_name = str(profile.get("conda_name") or "").strip()
        if not conda_name or conda_name in conda_names:
            raise ValueError(f"Invalid or duplicate conda_name for runtime {name}")
        conda_names.add(conda_name)
        libraries = profile.get("runtime_preload_libraries", [])
        if not isinstance(libraries, list) or not all(isinstance(item, str) for item in libraries):
            raise ValueError(f"runtime_preload_libraries for {name} must be a string list")
    missing = sorted(set(expected) - set(assigned))
    if missing:
        raise ValueError(f"Backend runtimes do not cover BackendSpec entries: {missing}")
    defaults = value.get("default_profiles", [])
    if not isinstance(defaults, list) or any(item not in profiles for item in defaults):
        raise ValueError("default_profiles must reference configured profiles")
    return value


def profile_names() -> list[str]:
    return sorted(load_profile_config()["profiles"])


def get_profile(name: str) -> dict[str, Any]:
    config = load_profile_config()
    if name not in config["profiles"]:
        raise KeyError(f"Unknown backend runtime {name!r}")
    value = dict(config["profiles"][name])
    value["name"] = name
    value["group"] = "profiles"
    return value


def selected_profile_names(value: str | None = None) -> list[str]:
    """Select runtimes for installation/probing only; this never changes MCP tools."""

    config = load_profile_config()
    raw = value if value is not None else os.environ.get("RESEARCHCHEMBENCH_MCP_PROFILES", "")
    names = [item.strip() for item in raw.split(",") if item.strip()] if raw else list(config["default_profiles"])
    unknown = sorted(set(names) - set(config["profiles"]))
    if unknown:
        raise KeyError(f"Unknown backend runtime profiles: {unknown}")
    return names


def profile_environment_path(profile: dict[str, Any]) -> Path:
    return resolve_runtime_path(str(profile["name"]), str(profile["environment"]))


def profile_python(name: str) -> Path:
    profile = get_profile(name)
    configured = str(profile.get("python") or "").strip()
    if configured:
        return resolve_configured_path(configured)
    return profile_environment_path(profile) / "bin" / "python"


def project_model_cache_path() -> Path:
    configured = os.environ.get(MODEL_CACHE_ENV, "").strip()
    if not configured:
        configured = str(load_profile_config().get("model_cache_root") or ".model_cache")
    path = Path(configured).expanduser()
    return path.resolve() if path.is_absolute() else (PROJECT_ROOT / path).resolve()


def project_runtime_cache_path() -> Path:
    configured = os.environ.get(RUNTIME_CACHE_ENV, "").strip()
    if not configured:
        configured = str(load_profile_config().get("runtime_cache_root") or ".runtime_cache")
    path = Path(configured).expanduser()
    return path.resolve() if path.is_absolute() else (PROJECT_ROOT / path).resolve()


def _profile_entries(profile: dict[str, Any], key: str) -> list[str]:
    entries = []
    for value in profile.get(key) or []:
        entries.append(str(resolve_configured_path(str(value))))
    return entries


def _profile_environment_value(value: Any) -> str:
    """Resolve project-relative path values without rewriting ordinary scalars."""

    text = str(value)
    if text.startswith(".") or "/" in text:
        preserve_trailing_slash = text.endswith("/")
        resolved = str(resolve_configured_path(text))
        return resolved + "/" if preserve_trailing_slash else resolved
    return text


def profile_runtime_environment(name: str) -> dict[str, str]:
    profile = get_profile(name)
    environment = profile_environment_path(profile)
    bin_dir = environment / "bin"
    path_entries = [
        *_profile_entries(profile, "prepend_path_entries"),
        str(bin_dir),
        *_profile_entries(profile, "path_entries"),
    ]
    library_entries = [
        *_profile_entries(profile, "prepend_library_path_entries"),
        str(environment / "lib"),
        *_profile_entries(profile, "library_path_entries"),
    ]
    values = {
        PROFILE_ENV: name,
        SOFTWARE_ROOT_ENV: str(software_root()),
        "PATH": os.pathsep.join([*path_entries, os.environ.get("PATH", "")]),
        "LD_LIBRARY_PATH": os.pathsep.join(
            [*library_entries, os.environ.get("LD_LIBRARY_PATH", "")]
        ),
        "PYTHONPATH": os.pathsep.join(
            [str(PROJECT_ROOT), os.environ.get("PYTHONPATH", "")]
        ),
    }
    values.update(
        {
            str(variable): _profile_environment_value(value)
            for variable, value in dict(
                profile.get("environment_variables") or {}
            ).items()
        }
    )
    runtime_cache = project_runtime_cache_path()
    runtime_cache.mkdir(parents=True, exist_ok=True)
    values[RUNTIME_CACHE_ENV] = str(runtime_cache)
    values["XDG_CACHE_HOME"] = str(runtime_cache)
    if profile.get("use_project_model_cache", False):
        cache_root = project_model_cache_path()
        cache_root.mkdir(parents=True, exist_ok=True)
        values[MODEL_CACHE_ENV] = str(cache_root)
    for variable, executable in dict(profile.get("command_variables") or {}).items():
        configured = Path(str(executable)).expanduser()
        if configured.is_absolute():
            candidate = configured
        elif configured.parent != Path("."):
            candidate = resolve_configured_path(configured)
        else:
            candidate = bin_dir / configured
        if candidate.exists():
            values[str(variable)] = str(candidate.resolve())
    return values


def apply_profile(name: str) -> dict[str, Any]:
    """Apply one runtime environment without changing the public action catalog."""

    profile = get_profile(name)
    for key, value in profile_runtime_environment(name).items():
        os.environ[key] = value
    return profile


def runtime_for_backend(backend_id: str) -> str:
    if backend_id not in backend_specs():
        raise KeyError(f"Unknown backend: {backend_id}")
    return backend_specs()[backend_id].runtime


def public_server_spec(discovery_mode: str | None = None) -> dict[str, Any]:
    config = load_profile_config()
    public = dict(config["public_server"])
    runtime = str(public["runtime"])
    python = profile_python(runtime)
    mode = resolve_tool_discovery_mode(discovery_mode)
    from .discovery_tools import PROGRESSIVE_DISCOVERY_TOOL_NAMES
    from .open_tools import OPEN_EXECUTION_TOOL_NAMES
    from .async_action_tools import ASYNC_ACTION_TOOL_NAMES

    tools = (
        sorted(action_specs()) + list(OPEN_EXECUTION_TOOL_NAMES) + list(ASYNC_ACTION_TOOL_NAMES)
        if mode == "full"
        else list(PROGRESSIVE_DISCOVERY_TOOL_NAMES)
        + list(OPEN_EXECUTION_TOOL_NAMES)
        + list(ASYNC_ACTION_TOOL_NAMES)
    )
    environment = profile_runtime_environment(runtime)
    environment[TOOL_DISCOVERY_MODE_ENV] = mode
    return {
        "profile": None,
        "runtime": runtime,
        "discovery_mode": mode,
        "name": str(public.get("server_name") or "researchchem_toolbox"),
        "description": str(
            public.get("description")
            or "Complete ResearchChem catalog with progressive discovery"
        ),
        "python": str(python),
        "command": [
            str(python),
            "-m",
            "chemistry_toolbox.mcp.server",
            "--transport",
            "stdio",
            "--discovery-mode",
            mode,
        ],
        "environment": environment,
        "tools": tools,
    }


def profile_server_spec(name: str) -> dict[str, Any]:
    """Deprecated compatibility alias; every name resolves to the one public server."""

    get_profile(name)
    return public_server_spec()
