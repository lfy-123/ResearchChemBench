"""Install an operator-provided file or directory without altering the source."""

from __future__ import annotations

import os
import shutil
from pathlib import Path


def install_copy(package: Path, destination: Path, options: dict[str, object]) -> None:
    if package.is_dir():
        shutil.copytree(package, destination, symlinks=True)
    else:
        destination.mkdir(parents=True, exist_ok=False)
        target_name = str(options.get("target_name") or package.name)
        shutil.copy2(package, destination / target_name)
    for link_value, target_value in dict(options.get("aliases") or {}).items():
        link = destination / str(link_value)
        target = destination / str(target_value)
        if not target.is_file():
            raise FileNotFoundError(target)
        link.parent.mkdir(parents=True, exist_ok=True)
        link.symlink_to(os.path.relpath(target, link.parent))
    for relative in options.get("executable_paths", []) or []:
        path = destination / str(relative)
        path.chmod(path.stat().st_mode | 0o111)
