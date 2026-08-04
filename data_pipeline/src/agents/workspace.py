from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Any
from uuid import uuid4


def create_agent_run(root: str | Path, label: str) -> dict[str, Path]:
    run_id = f"{label}_{uuid4().hex[:12]}"
    run_root = Path(root).expanduser().resolve() / "agent_runs" / run_id
    paths = {
        "run_root": run_root,
        "workspace": run_root / "workspace",
        "input": run_root / "workspace" / "input",
        "work": run_root / "workspace" / "work",
        "output": run_root / "workspace" / "output",
        "home": run_root / "home",
    }
    for path in paths.values():
        path.mkdir(parents=True, exist_ok=True)
    return paths


def snapshot_file(source: str | Path, destination: str | Path) -> Path:
    source_path = Path(source).expanduser().resolve()
    target = Path(destination)
    target.parent.mkdir(parents=True, exist_ok=True)
    if source_path.is_dir():
        shutil.copytree(source_path, target, dirs_exist_ok=True, symlinks=False)
    else:
        shutil.copy2(source_path, target)
    return target


def make_input_read_only(path: str | Path) -> None:
    root = Path(path)
    for item in sorted(root.rglob("*"), reverse=True):
        try:
            item.chmod(0o555 if item.is_dir() else 0o444)
        except OSError:
            pass
    root.chmod(0o555)


def isolated_environment(
    paths: dict[str, Path],
    cli: str,
    extra: dict[str, Any] | None = None,
    *,
    copy_cli_auth: bool = True,
) -> dict[str, str]:
    env = os.environ.copy()
    home = paths["home"]
    env.update(
        {
            "HOME": str(home),
            "PWD": str(paths["workspace"]),
            "INIT_CWD": str(paths["workspace"]),
            "XDG_CONFIG_HOME": str(home / ".config"),
            "XDG_DATA_HOME": str(home / ".local" / "share"),
            "XDG_CACHE_HOME": str(home / ".cache"),
            "TMPDIR": str(paths["work"] / "tmp"),
        }
    )
    Path(env["TMPDIR"]).mkdir(parents=True, exist_ok=True)
    if cli == "opencode":
        _prepare_opencode_home(paths, env, copy_cli_auth)
    elif cli == "codex":
        _prepare_codex_home(paths, env, copy_cli_auth)
    elif cli == "claude":
        _prepare_claude_home(paths, env, copy_cli_auth)
    env.update({str(key): str(value) for key, value in (extra or {}).items()})
    return env


def remove_agent_credentials(home: str | Path) -> None:
    home_path = Path(home)
    candidates = (
        home_path / "opencode_root" / "data" / "opencode" / "auth.json",
        home_path / ".local" / "share" / "opencode" / "auth.json",
        home_path / ".codex" / "auth.json",
        home_path / ".claude" / ".credentials.json",
    )
    for candidate in candidates:
        candidate.unlink(missing_ok=True)


def _prepare_opencode_home(
    paths: dict[str, Path], env: dict[str, str], copy_cli_auth: bool
) -> None:
    source_root = Path(os.environ.get("OPENCODE_ROOT", "")).expanduser()
    target_root = paths["home"] / "opencode_root"
    env["OPENCODE_ROOT"] = str(target_root)
    if not copy_cli_auth:
        return
    auth_candidates = [
        source_root / "data" / "opencode" / "auth.json",
        Path.home() / ".local" / "share" / "opencode" / "auth.json",
    ]
    source = next((item for item in auth_candidates if item.is_file()), None)
    if source:
        target = target_root / "data" / "opencode" / "auth.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def _prepare_codex_home(paths: dict[str, Path], env: dict[str, str], copy_cli_auth: bool) -> None:
    source = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).expanduser()
    target = paths["home"] / ".codex"
    target.mkdir(parents=True, exist_ok=True)
    auth = source / "auth.json"
    if copy_cli_auth and auth.is_file():
        shutil.copy2(auth, target / "auth.json")
    env["CODEX_HOME"] = str(target)


def _prepare_claude_home(paths: dict[str, Path], env: dict[str, str], copy_cli_auth: bool) -> None:
    source = Path(os.environ.get("CLAUDE_CONFIG_DIR", Path.home() / ".claude")).expanduser()
    target = paths["home"] / ".claude"
    target.mkdir(parents=True, exist_ok=True)
    credentials = source / ".credentials.json"
    if copy_cli_auth and credentials.is_file():
        shutil.copy2(credentials, target / ".credentials.json")
    env["CLAUDE_CONFIG_DIR"] = str(target)
