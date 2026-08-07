"""Run repository-reviewed source build commands inside an isolated staging tree."""

from __future__ import annotations

import os
import subprocess
from pathlib import Path


def install_commands(package: Path, destination: Path, options: dict[str, object]) -> None:
    from .archive import install_archive
    from .copy import install_copy

    source = destination / "source"
    if package.is_file():
        install_archive(package, source, {"strip_single_directory": options.get("strip_single_directory", False)})
    else:
        install_copy(package, source, {})
    install_prefix = destination / "install"
    install_prefix.mkdir(parents=True)
    environment = os.environ.copy()
    environment.update(
        {
            "RCB_SOURCE": str(source),
            "RCB_PREFIX": str(install_prefix),
            "RCB_JOBS": str(options.get("jobs") or os.cpu_count() or 1),
        }
    )
    for raw_command in options.get("commands", []) or []:
        if not isinstance(raw_command, list) or not raw_command:
            raise ValueError("Build commands must be non-empty argument lists")
        command = [
            str(item).replace("{source}", str(source)).replace("{prefix}", str(install_prefix))
            for item in raw_command
        ]
        subprocess.run(command, cwd=source, env=environment, check=True)
