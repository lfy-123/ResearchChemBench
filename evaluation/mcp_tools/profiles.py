"""Load dependency-isolated backend runtimes without filtering public tools."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

from researchchem_toolbox.catalog import action_specs, backend_specs


PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / "config.local.env", override=False)
PROFILE_CONFIG_ENV = "RESEARCHCHEM_MCP_PROFILE_CONFIG"
PROFILE_ENV = "RESEARCHCHEM_BACKEND_RUNTIME"
MODEL_CACHE_ENV = "RESEARCHCHEMBENCH_MODEL_CACHE"
DEFAULT_CONFIG_PATH = PROJECT_ROOT / "config" / "mcp_profiles.yaml"


def profile_config_path() -> Path:
    configured = os.environ.get(PROFILE_CONFIG_ENV, "").strip()
    return Path(configured).expanduser().resolve() if configured else DEFAULT_CONFIG_PATH


def load_profile_config() -> dict[str, Any]:
    path = profile_config_path()
    value = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    profiles = value.get("profiles")
    support = value.get("support_environments", {})
    if not isinstance(profiles, dict) or not profiles:
        raise ValueError(f"Invalid backend runtime configuration: {path}")
    if not isinstance(support, dict):
        raise ValueError("support_environments must be a mapping")
    public_server = value.get("public_server")
    if not isinstance(public_server, dict) or public_server.get("runtime") not in profiles:
        raise ValueError("public_server.runtime must reference a configured profile")

    expected = backend_specs()
    assigned: dict[str, str] = {}
    conda_names: set[str] = set()
    for group_name, group in (("profiles", profiles), ("support_environments", support)):
        for name, profile in group.items():
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
    for group in ("profiles", "support_environments"):
        if name in config.get(group, {}):
            value = dict(config[group][name])
            value["name"] = name
            value["group"] = group
            return value
    raise KeyError(f"Unknown backend runtime {name!r}")


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
        "PYTHONPATH": str(PROJECT_ROOT) + os.pathsep + os.environ.get("PYTHONPATH", ""),
    }
    if profile.get("use_project_model_cache", False):
        cache_root = project_model_cache_path()
        cache_root.mkdir(parents=True, exist_ok=True)
        values[MODEL_CACHE_ENV] = str(cache_root)
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
    """Apply one runtime environment without changing the public action catalog."""

    profile = get_profile(name)
    for key, value in profile_runtime_environment(name).items():
        os.environ[key] = value
    return profile


def runtime_for_backend(backend_id: str) -> str:
    if backend_id not in backend_specs():
        raise KeyError(f"Unknown backend: {backend_id}")
    return backend_specs()[backend_id].runtime


def public_server_spec() -> dict[str, Any]:
    config = load_profile_config()
    public = dict(config["public_server"])
    runtime = str(public["runtime"])
    python = profile_python(runtime)
    return {
        "profile": None,
        "runtime": runtime,
        "name": str(public.get("server_name") or "researchchem_toolbox"),
        "description": str(public.get("description") or "Complete ResearchChem atomic toolbox"),
        "python": str(python),
        "command": [
            str(python),
            "-m",
            "evaluation.mcp_tools.server",
            "--transport",
            "stdio",
        ],
        "environment": profile_runtime_environment(runtime),
        "tools": sorted(action_specs()),
    }


def profile_server_spec(name: str) -> dict[str, Any]:
    """Deprecated compatibility alias; every name resolves to the one full server."""

    get_profile(name)
    return public_server_spec()
