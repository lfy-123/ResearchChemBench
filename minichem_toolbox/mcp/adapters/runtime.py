"""Runtime discovery and safe subprocess helpers for optional chemistry backends."""

from __future__ import annotations

import importlib.metadata
import importlib.util
import os
import shlex
import shutil
import subprocess
from pathlib import Path
from typing import Any, Iterable

from ..workspace import resolve_workspace_output_path, resolve_workspace_path


def module_available(module: str) -> bool:
    """Return whether a Python module can be discovered without importing it."""

    if not module:
        return False
    try:
        return importlib.util.find_spec(module) is not None
    except (ImportError, ModuleNotFoundError, ValueError):
        return False


def module_version(distribution: str) -> str | None:
    """Return installed distribution version when available."""

    try:
        return importlib.metadata.version(distribution)
    except importlib.metadata.PackageNotFoundError:
        return None


def resolve_executable(
    executable: str,
    *,
    environment_variable: str | None = None,
) -> list[str] | None:
    """Resolve a trusted executable from an administrator environment or PATH."""

    configured = os.environ.get(environment_variable or "", "").strip()
    if configured:
        command = shlex.split(configured)
        if not command:
            return None
        path = shutil.which(command[0]) or command[0]
        if not Path(path).expanduser().exists() and shutil.which(command[0]) is None:
            return None
        command[0] = str(Path(path).expanduser()) if Path(path).expanduser().exists() else path
        return command
    path = shutil.which(executable)
    return [path] if path else None


def backend_status(
    backend: str,
    *,
    python_modules: Iterable[str] = (),
    executables: Iterable[str] = (),
    environment_variables: Iterable[str] = (),
    manual_action: str = "Install or configure the requested backend.",
) -> dict[str, Any]:
    """Return a structured, import-safe availability record."""

    modules = {name: module_available(name) for name in python_modules if name}
    commands = {name: shutil.which(name) for name in executables if name}
    environment = {
        name: bool(os.environ.get(name, "").strip())
        for name in environment_variables
        if name
    }
    available = bool(
        (modules and all(modules.values()))
        or (commands and any(commands.values()))
        or (environment and any(environment.values()))
    )
    if not modules and not commands and not environment:
        available = True
    return {
        "status": "available" if available else "unavailable",
        "backend": backend,
        "available": available,
        "python_modules": modules,
        "executables": commands,
        "environment": environment,
        "manual_action": None if available else manual_action,
    }


def unavailable_result(
    backend: str,
    *,
    reason: str,
    manual_action: str,
) -> dict[str, Any]:
    return {
        "status": "unavailable",
        "backend": backend,
        "available": False,
        "reason": reason,
        "manual_action": manual_action,
    }


def safe_input_file(value: str) -> Path:
    return resolve_workspace_path(value, must_exist=True)


def safe_output_directory(value: str) -> Path:
    probe = resolve_workspace_output_path(str(Path(value) / ".researchchem-probe"))
    directory = probe.parent
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def run_external(
    *,
    backend: str,
    executable: str,
    arguments: list[str],
    output_directory: str,
    environment_variable: str | None = None,
    timeout_seconds: int = 600,
    stdin_text: str | None = None,
) -> dict[str, Any]:
    """Run a configured backend without a shell and persist bounded logs."""

    if timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be positive")
    command = resolve_executable(
        executable,
        environment_variable=environment_variable,
    )
    if command is None:
        variable_hint = f" or set {environment_variable}" if environment_variable else ""
        return unavailable_result(
            backend,
            reason=f"Executable {executable!r} was not found",
            manual_action=f"Install {backend}{variable_hint}, then restart the MCP server.",
        )
    workdir = safe_output_directory(output_directory)
    completed = subprocess.run(
        [*command, *arguments],
        cwd=workdir,
        input=stdin_text,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout_seconds,
        check=False,
        env=os.environ.copy(),
    )
    stdout_path = workdir / "stdout.log"
    stderr_path = workdir / "stderr.log"
    stdout_path.write_text(completed.stdout[-1_000_000:], encoding="utf-8")
    stderr_path.write_text(completed.stderr[-1_000_000:], encoding="utf-8")
    return {
        "status": "success" if completed.returncode == 0 else "error",
        "backend": backend,
        "available": True,
        "returncode": completed.returncode,
        "command": [Path(command[0]).name, *command[1:], *arguments],
        "output_directory": str(workdir),
        "stdout_log": str(stdout_path),
        "stderr_log": str(stderr_path),
        "stdout_preview": completed.stdout[-4000:],
        "stderr_preview": completed.stderr[-4000:],
    }

