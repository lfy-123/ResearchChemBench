"""Backend health probes and exact runtime dispatch without scientific fallback."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable

import yaml

from .models import BackendSpec


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PROFILE_CONFIG_PATH = PROJECT_ROOT / "config" / "mcp_profiles.yaml"


@lru_cache(maxsize=1)
def load_runtime_config() -> dict[str, Any]:
    value = yaml.safe_load(PROFILE_CONFIG_PATH.read_text(encoding="utf-8")) or {}
    if not isinstance(value.get("profiles"), dict):
        raise ValueError(f"Invalid runtime profile configuration: {PROFILE_CONFIG_PATH}")
    return value


def runtime_spec(name: str) -> dict[str, Any]:
    config = load_runtime_config()
    for group in ("profiles", "support_environments"):
        values = config.get(group) or {}
        if name in values:
            result = dict(values[name])
            result["name"] = name
            result["group"] = group
            return result
    raise KeyError(f"Unknown backend runtime {name!r}")


def runtime_path(name: str) -> Path:
    specification = runtime_spec(name)
    path = Path(str(specification["environment"])).expanduser()
    return path.resolve() if path.is_absolute() else (PROJECT_ROOT / path).resolve()


def runtime_python(name: str) -> Path:
    configured = str(runtime_spec(name).get("python") or "").strip()
    if configured:
        path = Path(configured).expanduser()
        return path.resolve() if path.is_absolute() else (PROJECT_ROOT / path).resolve()
    return runtime_path(name) / "bin" / "python"


def _runtime_entries(specification: dict[str, Any], key: str) -> list[str]:
    entries = []
    for value in specification.get(key) or []:
        path = Path(str(value)).expanduser()
        if not path.is_absolute():
            path = PROJECT_ROOT / path
        entries.append(str(path.resolve()))
    return entries


def runtime_environment(name: str) -> dict[str, str]:
    specification = runtime_spec(name)
    environment = runtime_path(name)
    path_entries = [str(environment / "bin"), *_runtime_entries(specification, "path_entries")]
    library_entries = [
        str(environment / "lib"),
        *_runtime_entries(specification, "library_path_entries"),
    ]
    values = {
        "PATH": os.pathsep.join([*path_entries, os.environ.get("PATH", "")]),
        "LD_LIBRARY_PATH": os.pathsep.join(
            [*library_entries, os.environ.get("LD_LIBRARY_PATH", "")]
        ),
        "PYTHONPATH": str(PROJECT_ROOT)
        + os.pathsep
        + os.environ.get("PYTHONPATH", ""),
        "RESEARCHCHEM_BACKEND_RUNTIME": name,
    }
    values.update(
        {
            str(variable): str(value)
            for variable, value in dict(
                specification.get("environment_variables") or {}
            ).items()
        }
    )
    model_cache = load_runtime_config().get("model_cache_root", ".model_cache")
    if specification.get("use_project_model_cache", False):
        cache = Path(str(model_cache)).expanduser()
        if not cache.is_absolute():
            cache = PROJECT_ROOT / cache
        cache.mkdir(parents=True, exist_ok=True)
        values["RESEARCHCHEMBENCH_MODEL_CACHE"] = str(cache.resolve())
        values["XDG_CACHE_HOME"] = str(cache.resolve())
    for variable, executable in dict(specification.get("command_variables") or {}).items():
        configured = Path(str(executable)).expanduser()
        if configured.is_absolute():
            candidate = configured
        elif configured.parent != Path("."):
            candidate = PROJECT_ROOT / configured
        else:
            candidate = environment / "bin" / configured
        if candidate.exists():
            values[str(variable)] = str(candidate.resolve())
    return values


def _module_probe(runtime: str, modules: Iterable[str]) -> dict[str, dict[str, Any]]:
    names = sorted(set(modules))
    if not names:
        return {}
    python = runtime_python(runtime)
    if not python.is_file():
        return {name: {"available": False, "version": None} for name in names}
    script = """
import importlib.metadata
import importlib.util
import json
import sys

out = {}
for name in json.loads(sys.argv[1]):
    try:
        available = importlib.util.find_spec(name) is not None
    except Exception:
        available = False
    version = None
    if available:
        for distribution in (name, name.split('.')[0]):
            try:
                version = importlib.metadata.version(distribution)
                break
            except Exception:
                pass
    out[name] = {'available': available, 'version': version}
print(json.dumps(out))
"""
    try:
        completed = subprocess.run(
            [str(python), "-c", script, json.dumps(names)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=30,
            check=False,
            env={**os.environ, **runtime_environment(runtime)},
        )
        if completed.returncode == 0:
            return json.loads(completed.stdout.strip().splitlines()[-1])
    except (OSError, subprocess.TimeoutExpired, json.JSONDecodeError, IndexError):
        pass
    return {name: {"available": False, "version": None} for name in names}


def _resolve_executable(runtime: str, executable: str) -> str | None:
    bin_directory = runtime_path(runtime) / "bin"
    candidates = [bin_directory / executable]
    if executable == "cp2k":
        candidates.extend(bin_directory / name for name in ("cp2k.psmp", "cp2k.popt", "cp2k.ssmp"))
    for candidate in candidates:
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return str(candidate.resolve())
    return None


def probe_all_backends(specs: Iterable[BackendSpec]) -> dict[str, dict[str, Any]]:
    specifications = list(specs)
    modules_by_runtime: dict[str, set[str]] = {}
    for specification in specifications:
        modules_by_runtime.setdefault(specification.runtime, set()).update(
            specification.python_modules
        )
    module_status = {
        runtime: _module_probe(runtime, modules)
        for runtime, modules in modules_by_runtime.items()
    }
    results: dict[str, dict[str, Any]] = {}
    for specification in specifications:
        python = runtime_python(specification.runtime)
        modules = {
            name: module_status.get(specification.runtime, {}).get(
                name, {"available": False, "version": None}
            )
            for name in specification.python_modules
        }
        executables = {
            name: _resolve_executable(specification.runtime, name)
            for name in specification.executables
        }
        runtime_env = runtime_environment(specification.runtime)
        environment = {
            name: bool(os.environ.get(name) or runtime_env.get(name))
            for name in specification.environment_variables
        }
        modules_ok = bool(modules) and all(item["available"] for item in modules.values())
        executables_ok = bool(executables) and any(executables.values())
        configured_command_ok = any(
            bool(os.environ.get(name) or runtime_env.get(name))
            for name in specification.environment_variables
            if not name.endswith("_KEY")
        )
        credential_names = [
            name for name in specification.environment_variables if name.endswith("_KEY")
        ]
        credentials_ok = all(environment[name] for name in credential_names)
        implementation_available = (
            modules_ok or executables_ok or configured_command_ok
            if (modules or executables or specification.environment_variables)
            else True
        )
        if credential_names:
            implementation_available = implementation_available and credentials_ok
        available = python.is_file() and implementation_available
        missing_modules = [name for name, item in modules.items() if not item["available"]]
        missing_executables = [name for name, path in executables.items() if not path]
        missing_environment = [name for name, present in environment.items() if not present]
        results[specification.id] = {
            "status": "available" if available else "unavailable",
            "available": available,
            "runtime": specification.runtime,
            "runtime_python": str(python),
            "runtime_python_exists": python.is_file(),
            "python_modules": modules,
            "executables": executables,
            "environment": environment,
            "missing_python_modules": missing_modules,
            "missing_executables": missing_executables,
            "missing_environment": missing_environment,
            "conda_packages": list(specification.conda_packages),
            "pip_packages": list(specification.pip_packages),
            "required_data_resources": list(specification.required_data_resources),
            "license_class": specification.license_class,
            "install_notes": specification.install_notes,
        }
    return results


def invoke_worker(
    *,
    runtime: str,
    payload: dict[str, Any],
    timeout_seconds: int,
) -> dict[str, Any]:
    """Execute exactly one requested backend in its declared runtime."""

    python = runtime_python(runtime)
    if not python.is_file():
        return {
            "status": "unavailable",
            "error": {
                "code": "runtime_missing",
                "message": f"Runtime Python does not exist: {python}",
            },
            "retryable": False,
        }
    environment = {**os.environ, **runtime_environment(runtime)}
    requested_cores = (
        (payload.get("request") or {}).get("resource_limits") or {}
    ).get("cpu_cores")
    if requested_cores is not None:
        threads = str(max(1, int(requested_cores)))
        for variable in (
            "OMP_NUM_THREADS",
            "MKL_NUM_THREADS",
            "OPENBLAS_NUM_THREADS",
            "NUMEXPR_NUM_THREADS",
            "VECLIB_MAXIMUM_THREADS",
        ):
            environment[variable] = threads
    try:
        completed = subprocess.run(
            [str(python), "-m", "researchchem_toolbox.worker"],
            input=json.dumps(payload, ensure_ascii=False),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=timeout_seconds,
            check=False,
            cwd=PROJECT_ROOT,
            env=environment,
        )
    except subprocess.TimeoutExpired as exc:
        return {
            "status": "timeout",
            "error": {
                "code": "worker_timeout",
                "message": f"Backend runtime exceeded {timeout_seconds} seconds",
                "stderr": (exc.stderr or "")[-2000:] if isinstance(exc.stderr, str) else "",
            },
            "retryable": True,
        }
    except OSError as exc:
        return {
            "status": "failed",
            "error": {"code": "worker_start_failed", "message": str(exc)},
            "retryable": False,
        }
    try:
        result = json.loads(completed.stdout.strip().splitlines()[-1])
    except (json.JSONDecodeError, IndexError):
        return {
            "status": "failed",
            "error": {
                "code": "invalid_worker_response",
                "message": "Backend worker did not return a JSON object",
                "stdout": completed.stdout[-2000:],
                "stderr": completed.stderr[-2000:],
                "returncode": completed.returncode,
            },
            "retryable": False,
        }
    if completed.stderr.strip():
        result.setdefault("worker_stderr", completed.stderr[-4000:])
    result.setdefault("worker_returncode", completed.returncode)
    return result
