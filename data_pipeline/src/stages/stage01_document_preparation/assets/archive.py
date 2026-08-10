from __future__ import annotations

import shutil
import tarfile
import zipfile
from pathlib import Path


class ArchiveError(RuntimeError):
    pass


def is_archive(path: str | Path, file_name: str | None = None) -> bool:
    name = (file_name or Path(path).name).casefold()
    return name.endswith((".zip", ".tar", ".tar.gz", ".tgz", ".tar.bz2", ".tbz2"))


def safe_extract(
    path: str | Path,
    destination: str | Path,
    *,
    max_files: int = 5000,
    max_total_bytes: int = 50 * 1024**3,
) -> list[Path]:
    source = Path(path)
    target = Path(destination)
    target.mkdir(parents=True, exist_ok=True)
    if zipfile.is_zipfile(source):
        members = _zip_members(source, max_files, max_total_bytes)
        with zipfile.ZipFile(source) as archive:
            for member in members:
                output = _safe_target(target, member.filename)
                if member.is_dir():
                    output.mkdir(parents=True, exist_ok=True)
                    continue
                output.parent.mkdir(parents=True, exist_ok=True)
                with archive.open(member) as incoming, output.open("wb") as outgoing:
                    shutil.copyfileobj(incoming, outgoing)
    elif tarfile.is_tarfile(source):
        members = _tar_members(source, max_files, max_total_bytes)
        with tarfile.open(source) as archive:
            for member in members:
                if member.isdir():
                    _safe_target(target, member.name).mkdir(parents=True, exist_ok=True)
                    continue
                incoming = archive.extractfile(member)
                if incoming is None:
                    continue
                output = _safe_target(target, member.name)
                output.parent.mkdir(parents=True, exist_ok=True)
                with incoming, output.open("wb") as outgoing:
                    shutil.copyfileobj(incoming, outgoing)
    else:
        raise ArchiveError(f"unsupported archive: {source}")
    return sorted(item for item in target.rglob("*") if item.is_file())


def _zip_members(path: Path, max_files: int, max_total_bytes: int) -> list[zipfile.ZipInfo]:
    with zipfile.ZipFile(path) as archive:
        members = archive.infolist()
    if len(members) > max_files:
        raise ArchiveError(f"archive contains {len(members)} entries, limit is {max_files}")
    if sum(item.file_size for item in members) > max_total_bytes:
        raise ArchiveError("archive expanded size exceeds limit")
    for item in members:
        _validate_member(item.filename)
        mode = item.external_attr >> 16
        if mode and (mode & 0o170000) == 0o120000:
            raise ArchiveError(f"symbolic link is not allowed: {item.filename}")
    return members


def _tar_members(path: Path, max_files: int, max_total_bytes: int) -> list[tarfile.TarInfo]:
    with tarfile.open(path) as archive:
        members = archive.getmembers()
    if len(members) > max_files:
        raise ArchiveError(f"archive contains {len(members)} entries, limit is {max_files}")
    if sum(item.size for item in members) > max_total_bytes:
        raise ArchiveError("archive expanded size exceeds limit")
    for item in members:
        _validate_member(item.name)
        if item.issym() or item.islnk() or item.isdev():
            raise ArchiveError(f"links and devices are not allowed: {item.name}")
    return members


def _validate_member(name: str) -> None:
    path = Path(name)
    if path.is_absolute() or ".." in path.parts:
        raise ArchiveError(f"unsafe archive path: {name}")


def _safe_target(root: Path, name: str) -> Path:
    output = (root / name).resolve()
    if root.resolve() not in output.parents and output != root.resolve():
        raise ArchiveError(f"archive path escapes destination: {name}")
    return output
