"""File-level legacy cache migration using the deterministic v2 classifier."""

from __future__ import annotations

import os
import re
import shutil
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .legacy_layout import classify_legacy_path, load_legacy_layout
from .receipts import write_json


def _link_or_copy(source: Path, destination: Path) -> str:
    try:
        os.link(source, destination)
        return "hardlink"
    except OSError:
        shutil.copy2(source, destination)
        return "copy"


def _relative_to_legacy_root(target: Path, legacy_root: Path) -> Path | None:
    """Map absolute links created before a legacy cache was renamed."""

    aliases = (legacy_root, legacy_root.parent / ".software_cache")
    for root in aliases:
        try:
            return target.relative_to(root)
        except ValueError:
            continue
    return None


def _rewrite_portable_shebang(path: Path, *, force: bool = False) -> bool:
    """Replace a host-specific interpreter with an environment-resolved one."""

    if not force and not os.access(path, os.X_OK):
        return False
    try:
        with path.open("rb") as handle:
            first_line = handle.readline(4096)
    except OSError:
        return False
    if not first_line.startswith(b"#!") or b"/inspire/hdd/global_user/" not in first_line:
        return False
    words = first_line[2:].decode("utf-8", errors="strict").strip().split()
    if not words:
        return False
    interpreter = Path(words[0]).name
    replacement = f"#!/usr/bin/env -S {interpreter}"
    if len(words) > 1:
        replacement += " " + " ".join(words[1:])
    replacement = (replacement + "\n").encode("utf-8")
    temporary = path.with_name(f".{path.name}.relocate-{os.getpid()}")
    stat = path.stat()
    with path.open("rb") as source, temporary.open("wb") as destination:
        source.readline()
        destination.write(replacement)
        shutil.copyfileobj(source, destination)
    shutil.copystat(path, temporary)
    os.chmod(temporary, stat.st_mode)
    temporary.replace(path)
    return True


_CACHE_REFERENCE = re.compile(
    r"/[^\"'\s]+/\.software_cache/(?P<relative>[^\"'\s]+)"
)


def _rewrite_relative_exec_wrapper(path: Path, cache_root: Path) -> bool:
    """Replace a legacy absolute cache reference with a launcher-relative path."""

    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    if not text.startswith("#!/usr/bin/env bash\n") or not _CACHE_REFERENCE.search(text):
        return False

    def replacement(match: re.Match[str]) -> str:
        mapped = classify_legacy_path(match.group("relative"))
        if mapped is None:
            return match.group(0)
        relative = os.path.relpath(cache_root / mapped, path.parent)
        return "${script_dir}/" + relative

    rewritten = _CACHE_REFERENCE.sub(replacement, text)
    if rewritten == text:
        return False
    marker = 'script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"\n'
    if marker not in rewritten:
        rewritten = rewritten.replace("#!/usr/bin/env bash\n", "#!/usr/bin/env bash\n" + marker, 1)
    temporary = path.with_name(f".{path.name}.relocate-{os.getpid()}")
    temporary.write_text(rewritten, encoding="utf-8")
    shutil.copystat(path, temporary)
    temporary.replace(path)
    return True


def _ensure_compatibility_links(cache_root: Path) -> list[dict[str, str]]:
    records = []
    for link_value, target_value in dict(
        load_legacy_layout().get("compatibility_links") or {}
    ).items():
        link = cache_root / link_value
        target = cache_root / target_value
        if link.is_symlink():
            status = "present" if link.resolve(strict=False) == target else "conflict"
        elif link.exists():
            status = "conflict"
        elif not target.exists():
            status = "target_missing"
        else:
            link.parent.mkdir(parents=True, exist_ok=True)
            link.symlink_to(os.path.relpath(target, link.parent))
            status = "created"
        records.append({"path": str(link_value), "target": str(target_value), "status": status})
    return records


def _write_portable_config_files(cache_root: Path) -> list[dict[str, str]]:
    records = []
    for relative, content in dict(
        load_legacy_layout().get("portable_config_files") or {}
    ).items():
        path = cache_root / relative
        if not path.is_file() or path.is_symlink():
            records.append({"path": str(relative), "status": "missing"})
            continue
        expected = str(content)
        if path.read_text(encoding="utf-8") == expected:
            records.append({"path": str(relative), "status": "already_portable"})
            continue
        temporary = path.with_name(f".{path.name}.relocate-{os.getpid()}")
        temporary.write_text(expected, encoding="utf-8")
        shutil.copystat(path, temporary)
        temporary.replace(path)
        records.append({"path": str(relative), "status": "rewritten"})
    return records


def relocate_v2(cache_root: Path) -> dict[str, Any]:
    """Apply deterministic, copy-on-write portability repairs to an existing v2 cache."""

    cache_root = cache_root.resolve()
    records = []
    for legacy_value in load_legacy_layout().get("portable_shebang_paths") or ():
        destination = classify_legacy_path(str(legacy_value))
        if destination is None:
            continue
        path = cache_root / destination
        if not path.is_file() or path.is_symlink():
            records.append({"path": destination.as_posix(), "status": "missing"})
            continue
        rewritten = _rewrite_portable_shebang(path, force=True)
        first_line = path.open("rb").readline(4096)
        portable = first_line.startswith(b"#!/usr/bin/env -S ")
        records.append(
            {
                "path": destination.as_posix(),
                "status": "rewritten" if rewritten else "already_portable" if portable else "unchanged",
            }
        )
    wrapper_records = []
    for legacy_root in load_legacy_layout().get("portable_wrapper_roots") or ():
        mapped_root = classify_legacy_path(str(legacy_root))
        if mapped_root is None:
            continue
        root = cache_root / mapped_root
        if not root.is_dir():
            wrapper_records.append({"path": mapped_root.as_posix(), "status": "missing"})
            continue
        for path in sorted(item for item in root.rglob("*") if item.is_file() and not item.is_symlink()):
            rewritten = _rewrite_relative_exec_wrapper(path, cache_root)
            wrapper_records.append(
                {
                    "path": path.relative_to(cache_root).as_posix(),
                    "status": "rewritten" if rewritten else "already_portable",
                }
            )
    report = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "cache_root": str(cache_root),
        "portable_shebangs": records,
        "portable_wrappers": wrapper_records,
        "portable_configs": _write_portable_config_files(cache_root),
        "compatibility_links": _ensure_compatibility_links(cache_root),
    }
    write_json(cache_root / "receipts" / "v2-relocation.json", report)
    return report


def plan_v2(legacy_root: Path) -> dict[str, Any]:
    """Classify a legacy tree without writing a destination cache."""

    legacy_root = legacy_root.resolve()
    if not legacy_root.is_dir():
        raise FileNotFoundError(legacy_root)
    roles: Counter[str] = Counter()
    roots: Counter[str] = Counter()
    ignored_roots: Counter[str] = Counter()
    destination_paths: set[Path] = set()
    collisions: list[dict[str, str]] = []
    for source in legacy_root.rglob("*"):
        relative = source.relative_to(legacy_root)
        destination = classify_legacy_path(relative)
        if destination is None:
            ignored_roots[relative.parts[0]] += 1
            continue
        if destination in destination_paths:
            collisions.append({"source": relative.as_posix(), "destination": destination.as_posix()})
        destination_paths.add(destination)
        roles[destination.parts[0]] += 1
        roots[relative.parts[0]] += 1
    return {
        "schema_version": 1,
        "legacy_root": str(legacy_root),
        "classified_paths": len(destination_paths),
        "roles": dict(sorted(roles.items())),
        "source_roots": dict(sorted(roots.items())),
        "ignored_roots": dict(sorted(ignored_roots.items())),
        "collisions": collisions,
    }


def migrate_v2(legacy_root: Path, destination_root: Path) -> dict[str, Any]:
    legacy_root = legacy_root.resolve()
    destination_root = destination_root.resolve()
    if legacy_root == destination_root:
        raise ValueError("Legacy and destination cache roots must differ")
    plan = plan_v2(legacy_root)
    if plan["collisions"]:
        raise ValueError(f"Legacy classification has {len(plan['collisions'])} path collisions")
    counts = {
        "hardlink": 0,
        "copy": 0,
        "symlink": 0,
        "directory": 0,
        "ignored": 0,
        "portable_shebang": 0,
    }
    unresolved_links: list[dict[str, str]] = []
    portable_shebang_paths = set(
        str(value) for value in load_legacy_layout().get("portable_shebang_paths") or ()
    )
    portable_wrapper_roots = tuple(
        Path(str(value)) for value in load_legacy_layout().get("portable_wrapper_roots") or ()
    )
    for source in legacy_root.rglob("*"):
        relative = source.relative_to(legacy_root)
        destination_relative = classify_legacy_path(relative)
        if destination_relative is None:
            counts["ignored"] += 1
            continue
        destination = destination_root / destination_relative
        if source.is_symlink():
            destination.parent.mkdir(parents=True, exist_ok=True)
            raw_target = Path(os.readlink(source))
            target = (
                raw_target
                if raw_target.is_absolute()
                else (source.parent / raw_target).resolve(strict=False)
            )
            target_relative = _relative_to_legacy_root(target, legacy_root)
            if target_relative is None:
                if raw_target.is_absolute():
                    unresolved_links.append(
                        {
                            "path": str(destination_relative),
                            "target": str(raw_target),
                            "reason": "external absolute target",
                        }
                    )
                destination.symlink_to(raw_target)
            else:
                mapped = classify_legacy_path(target_relative)
                if mapped is None:
                    unresolved_links.append(
                        {
                            "path": str(destination_relative),
                            "target": str(raw_target),
                            "reason": "target belongs to ignored root",
                        }
                    )
                    destination.symlink_to(raw_target)
                else:
                    destination.symlink_to(
                        os.path.relpath(destination_root / mapped, destination.parent)
                    )
            counts["symlink"] += 1
        elif source.is_dir():
            destination.mkdir(parents=True, exist_ok=True)
            shutil.copystat(source, destination, follow_symlinks=False)
            counts["directory"] += 1
        elif source.is_file():
            destination.parent.mkdir(parents=True, exist_ok=True)
            counts[_link_or_copy(source, destination)] += 1
            if _rewrite_portable_shebang(
                destination, force=relative.as_posix() in portable_shebang_paths
            ):
                counts["portable_shebang"] += 1
            if any(relative.is_relative_to(root) for root in portable_wrapper_roots):
                if _rewrite_relative_exec_wrapper(destination, destination_root):
                    counts["portable_wrapper"] = counts.get("portable_wrapper", 0) + 1
    report = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "legacy_root": str(legacy_root),
        "destination_root": str(destination_root),
        "counts": counts,
        "plan": plan,
        "unresolved_symlinks": unresolved_links,
        "portable_configs": _write_portable_config_files(destination_root),
        "compatibility_links": _ensure_compatibility_links(destination_root),
    }
    write_json(destination_root / "receipts" / "legacy-v2-migration.json", report)
    return report
