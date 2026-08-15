"""Run one CLI Agent inside a minimal mount-namespace filesystem."""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--rootfs", type=Path, required=True)
    parser.add_argument("--executable", type=Path, required=True)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = list(args.command)
    if command[:1] == ["--"]:
        command = command[1:]
    if not command:
        raise SystemExit("namespace_exec requires a command")

    workspace = args.workspace.resolve()
    root = args.rootfs.resolve()
    executable = args.executable.resolve()
    if not workspace.is_dir() or not executable.is_file():
        raise SystemExit("workspace or Agent executable is unavailable")
    _prepare_root(root)
    _run(["mount", "--make-rprivate", "/"])
    _bind_read_only(Path("/usr"), root / "usr", recursive=True)
    _bind_read_only(executable, root / "agent-executable")
    _bind(workspace, root / "workspace")
    for name in ("inputs", "private_input"):
        for path in workspace.rglob(name):
            if path.is_dir():
                _bind_read_only(path, root / "workspace" / path.relative_to(workspace), recursive=True)
    _run(["mount", "-t", "tmpfs", "tmpfs", str(root / "tmp")])
    _run(["mount", "-t", "tmpfs", "tmpfs", str(root / "home")])
    (root / "home" / "agent" / ".codex").mkdir(parents=True)
    _run(["mount", "-t", "proc", "proc", str(root / "proc")])
    for name in ("null", "zero", "random", "urandom"):
        source = Path("/dev") / name
        target = root / "dev" / name
        target.touch(exist_ok=True)
        _bind(source, target)

    rewritten = [value.replace(str(workspace), "/workspace") for value in command]
    rewritten[0] = "/agent-executable"
    environment = os.environ.copy()
    environment.update(
        {
            "HOME": "/home/agent",
            "CODEX_HOME": "/home/agent/.codex",
            "TMPDIR": "/tmp",
            "PATH": "/usr/local/bin:/usr/bin:/bin",
            "PWD": "/workspace",
        }
    )
    for key in ("PYTHONPATH", "LD_LIBRARY_PATH", "CONDA_PREFIX", "CONDA_EXE"):
        environment.pop(key, None)
    os.chroot(root)
    os.chdir("/workspace")
    os.execve(rewritten[0], rewritten, environment)


def _prepare_root(root: Path) -> None:
    if root.exists():
        shutil.rmtree(root)
    for directory in ("usr", "workspace", "tmp", "home", "proc", "dev", "etc"):
        (root / directory).mkdir(parents=True, exist_ok=True)
    for link, target in (("bin", "usr/bin"), ("lib", "usr/lib"), ("lib64", "usr/lib64")):
        path = root / link
        if not path.exists():
            path.symlink_to(target)
    (root / "agent-executable").touch()
    (root / "etc" / "passwd").write_text("agent:x:0:0:agent:/home/agent:/bin/bash\n")
    (root / "etc" / "group").write_text("agent:x:0:\n")
    (root / "etc" / "hosts").write_text("127.0.0.1 localhost\n")


def _bind(source: Path, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    if source.is_dir():
        target.mkdir(parents=True, exist_ok=True)
    elif not target.exists():
        target.touch()
    _run(["mount", "--bind", str(source), str(target)])


def _bind_read_only(source: Path, target: Path, *, recursive: bool = False) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    if source.is_dir():
        target.mkdir(parents=True, exist_ok=True)
    elif not target.exists():
        target.touch()
    _run(["mount", "--rbind" if recursive else "--bind", str(source), str(target)])
    if recursive:
        _run(["mount", "--make-rslave", str(target)])
    _run(["mount", "-o", "remount,bind,ro", str(target)])


def _run(command: list[str]) -> None:
    subprocess.run(command, check=True, capture_output=True, text=True)


if __name__ == "__main__":
    main()
