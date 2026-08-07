"""Safe extraction of tar and zip software distributions."""

from __future__ import annotations

import shutil
import tarfile
import zipfile
from pathlib import Path


def _safe_destination(root: Path, member_name: str) -> Path:
    destination = (root / member_name).resolve(strict=False)
    try:
        destination.relative_to(root.resolve())
    except ValueError as exc:
        raise ValueError(f"Archive member escapes extraction root: {member_name}") from exc
    return destination


def _extract_tar(package: Path, destination: Path) -> None:
    with tarfile.open(package, "r:*") as handle:
        members = handle.getmembers()
        for member in members:
            _safe_destination(destination, member.name)
            if member.issym() or member.islnk():
                link_root = Path(member.name).parent
                _safe_destination(destination, str(link_root / member.linkname))
        handle.extractall(destination, members=members)


def _extract_zip(package: Path, destination: Path) -> None:
    with zipfile.ZipFile(package) as handle:
        for member in handle.infolist():
            _safe_destination(destination, member.filename)
        handle.extractall(destination)


def _strip_single_directory(destination: Path) -> None:
    children = list(destination.iterdir())
    if len(children) != 1 or not children[0].is_dir():
        raise ValueError("strip_single_directory requires one top-level directory")
    source = children[0]
    temporary = destination.parent / f"{destination.name}.strip"
    source.replace(temporary)
    destination.rmdir()
    temporary.replace(destination)


def install_archive(package: Path, destination: Path, options: dict[str, object]) -> None:
    destination.mkdir(parents=True, exist_ok=False)
    if tarfile.is_tarfile(package):
        _extract_tar(package, destination)
    elif zipfile.is_zipfile(package):
        _extract_zip(package, destination)
    else:
        raise ValueError(f"Unsupported archive format: {package}")
    if bool(options.get("strip_single_directory", False)):
        _strip_single_directory(destination)
    for relative in options.get("executable_paths", []) or []:
        path = destination / str(relative)
        path.chmod(path.stat().st_mode | 0o111)
