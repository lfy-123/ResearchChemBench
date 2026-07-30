"""Install or remove the portable chemistry MCP server in Agent CLI configs."""

from __future__ import annotations

import argparse
import json
import os
import shlex
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Iterable

SUPPORTED_AGENTS = ("codex", "claude", "opencode")


def _server_command(python_executable: str) -> list[str]:
    return [python_executable, "-m", "researchchem_mcp_tools.server"]


def _server_environment(workspace: Path | None) -> dict[str, str]:
    environment = {"PYTHONUNBUFFERED": "1"}
    if workspace is not None:
        environment["RESEARCHCHEM_MCP_WORKSPACE"] = str(workspace.resolve())
    return environment


def _print_command(command: Iterable[str]) -> None:
    print("  $ " + shlex.join(list(command)))


def _run(command: list[str], *, dry_run: bool, ignore_error: bool = False) -> None:
    _print_command(command)
    if dry_run:
        return
    result = subprocess.run(command, check=False)
    if result.returncode and not ignore_error:
        raise RuntimeError(
            f"Command failed with exit code {result.returncode}: {shlex.join(command)}"
        )


def _require_cli(executable: str, *, explicit: bool, dry_run: bool) -> bool:
    if dry_run or shutil.which(executable):
        return True
    if explicit:
        raise RuntimeError(f"Required Agent CLI is not installed or not on PATH: {executable}")
    print(f"Skipping {executable}: executable not found")
    return False


def configure_codex(
    *,
    name: str,
    command: list[str],
    environment: dict[str, str],
    uninstall: bool,
    dry_run: bool,
) -> None:
    print("Codex MCP configuration:")
    remove = ["codex", "mcp", "remove", name]
    _run(remove, dry_run=dry_run, ignore_error=True)
    if uninstall:
        return
    add = ["codex", "mcp", "add", name]
    for key, value in environment.items():
        add.extend(["--env", f"{key}={value}"])
    add.extend(["--", *command])
    _run(add, dry_run=dry_run)


def configure_claude(
    *,
    name: str,
    command: list[str],
    environment: dict[str, str],
    scope: str,
    uninstall: bool,
    dry_run: bool,
) -> None:
    print("Claude MCP configuration:")
    remove = ["claude", "mcp", "remove", name, "--scope", scope]
    _run(remove, dry_run=dry_run, ignore_error=True)
    if uninstall:
        return
    # Claude's --env option is variadic. Put the server name before --env so
    # it cannot be consumed as another KEY=VALUE token.
    add = ["claude", "mcp", "add", "--scope", scope, name]
    for key, value in environment.items():
        add.extend(["--env", f"{key}={value}"])
    add.extend(["--", *command])
    _run(add, dry_run=dry_run)


def _opencode_config_path(scope: str, project_dir: Path) -> Path:
    if scope in {"project", "local"}:
        return project_dir.resolve() / "opencode.json"
    config_home = Path(
        os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")
    ).expanduser()
    return config_home / "opencode" / "opencode.json"


def _read_json_config(path: Path) -> dict:
    if not path.exists():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"OpenCode config is not strict JSON and cannot be updated safely: {path}"
        ) from exc
    if not isinstance(value, dict):
        raise RuntimeError(f"OpenCode config must be a JSON object: {path}")
    return value


def _write_json_config(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        backup = path.with_suffix(path.suffix + ".researchchem.bak")
        shutil.copy2(path, backup)
        print(f"  Backup: {backup}")
    temporary = path.with_suffix(path.suffix + ".researchchem.tmp")
    temporary.write_text(
        json.dumps(value, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def configure_opencode(
    *,
    name: str,
    command: list[str],
    environment: dict[str, str],
    scope: str,
    project_dir: Path,
    uninstall: bool,
    dry_run: bool,
) -> None:
    path = _opencode_config_path(scope, project_dir)
    print(f"OpenCode MCP configuration: {path}")
    config = _read_json_config(path)
    mcp_config = config.setdefault("mcp", {})
    if not isinstance(mcp_config, dict):
        raise RuntimeError(f"OpenCode config field 'mcp' must be an object: {path}")
    if uninstall:
        mcp_config.pop(name, None)
    else:
        mcp_config[name] = {
            "type": "local",
            "command": command,
            "environment": environment,
            "enabled": True,
        }
    print(json.dumps({"mcp": {name: mcp_config.get(name)}}, indent=2))
    if not dry_run:
        _write_json_config(path, config)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--agent",
        action="append",
        choices=["all", *SUPPORTED_AGENTS],
        default=[],
        help="Agent to configure; repeatable. Default: all installed Agents.",
    )
    parser.add_argument("--name", default="researchchem-tools")
    parser.add_argument("--workspace", type=Path)
    parser.add_argument("--python", default=sys.executable)
    parser.add_argument(
        "--scope",
        choices=["local", "project", "user"],
        default="user",
        help="Claude/OpenCode config scope. Codex MCP config is user-level.",
    )
    parser.add_argument("--project-dir", type=Path, default=Path.cwd())
    parser.add_argument("--uninstall", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    selected = args.agent or ["all"]
    expanded = list(SUPPORTED_AGENTS) if "all" in selected else list(dict.fromkeys(selected))
    explicit = "all" not in selected
    workspace = args.workspace.resolve() if args.workspace else None
    if workspace is not None and not workspace.is_dir():
        parser.error(f"Workspace directory does not exist: {workspace}")

    command = _server_command(args.python)
    environment = _server_environment(workspace)
    action = "Uninstalling" if args.uninstall else "Installing"
    print(f"{action} portable ResearchChem MCP tools")
    print(f"  Server name:    {args.name}")
    print(f"  Server command: {shlex.join(command)}")
    print(f"  Agents:         {', '.join(expanded)}")
    if args.dry_run:
        print("  Mode:           dry-run")

    for agent in expanded:
        if agent == "codex":
            if _require_cli("codex", explicit=explicit, dry_run=args.dry_run):
                configure_codex(
                    name=args.name,
                    command=command,
                    environment=environment,
                    uninstall=args.uninstall,
                    dry_run=args.dry_run,
                )
        elif agent == "claude":
            if _require_cli("claude", explicit=explicit, dry_run=args.dry_run):
                configure_claude(
                    name=args.name,
                    command=command,
                    environment=environment,
                    scope=args.scope,
                    uninstall=args.uninstall,
                    dry_run=args.dry_run,
                )
        elif agent == "opencode":
            configure_opencode(
                name=args.name,
                command=command,
                environment=environment,
                scope=args.scope,
                project_dir=args.project_dir,
                uninstall=args.uninstall,
                dry_run=args.dry_run,
            )

    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
