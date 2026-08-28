"""File-level legacy cache migration using the deterministic v2 classifier."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .legacy_layout import classify_legacy_path, load_legacy_layout
from .receipts import write_json


def _portable_root_label(path: Path, *, destination: bool = False) -> str:
    """Return a stable receipt label instead of exposing a host checkout path."""

    return (
        "${RESEARCHCHEMBENCH_SOFTWARE_ROOT}"
        if destination
        else "${LEGACY_SOFTWARE_CACHE_ROOT}"
    )


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

_ABSOLUTE_PATH_START = r"(?<![$A-Za-z0-9_])/[^\"'\s]+/"
_GAMESS_RUNTIME_PATHS = (
    (
        re.compile(
            _ABSOLUTE_PATH_START
            + r"(?:installations/)?gamess/2024-r2-p1/source"
        ),
        "$RESEARCHCHEMBENCH_SOFTWARE_ROOT/installations/gamess/2024-r2-p1/source",
    ),
    (
        re.compile(
            _ABSOLUTE_PATH_START + r"(?:build/)?gamess/2024-r2-p1/build"
        ),
        "$RESEARCHCHEMBENCH_SOFTWARE_ROOT/build/gamess/2024-r2-p1/build",
    ),
    (
        re.compile(
            _ABSOLUTE_PATH_START
            + r"(?:validation/)?gamess/2024-r2-p1/scratch"
        ),
        "$RESEARCHCHEMBENCH_SOFTWARE_ROOT/validation/gamess/2024-r2-p1/scratch",
    ),
    (
        re.compile(
            _ABSOLUTE_PATH_START
            + r"(?:installations/)?gamess/2024-r2-p1/restart"
        ),
        "$RESEARCHCHEMBENCH_SOFTWARE_ROOT/installations/gamess/2024-r2-p1/restart",
    ),
    (
        re.compile(_ABSOLUTE_PATH_START + r"\.tool_envs/gamess/lib"),
        "$GMS_RUNTIME_LIB",
    ),
    (
        re.compile(
            _ABSOLUTE_PATH_START
            + r"(?:\.tool_envs/gamess|\.envs/general-modern-openmpi5)/bin/tcsh"
        ),
        "tcsh",
    ),
)

_GAMESS_WRITABLE_DIRECTORY_ASSIGNMENTS = (
    (
        re.compile(
            r"(?m)^(?P<indent>\s*)set SCR="
            r"\$RESEARCHCHEMBENCH_SOFTWARE_ROOT/validation/gamess/"
            r"2024-r2-p1/scratch\s*$"
        ),
        r"\g<indent>if ( $?GMS_SCRATCH ) set SCR=$GMS_SCRATCH",
    ),
    (
        re.compile(
            r"(?m)^(?P<indent>\s*)set USERSCR="
            r"\$RESEARCHCHEMBENCH_SOFTWARE_ROOT/installations/gamess/"
            r"2024-r2-p1/restart\s*$"
        ),
        r"\g<indent>if ( $?GMS_RESTART ) set USERSCR=$GMS_RESTART",
    ),
)

_ACPYPE_LAUNCHER = Path("installations/acpype/2023.10.27/python/bin/acpype")
_KINBOT_REACTION_FAMILY = Path(
    "installations/kinbot/source-2.2.2/kinbot/reac_family.py"
)

# These locally compiled binaries have historically carried build-host RPATHs.
# Runtime profiles already provide the required library directories, so keeping
# an embedded path makes a migrated cache non-relocatable and can select stale
# system libraries.  Keep this list deliberately narrow: arbitrary binaries
# must not be rewritten during cache migration.
_STALE_RPATH_BINARIES = (
    Path("installations/charmm/50b2/install/bin/charmm"),
    Path("installations/vasp/6.3.2/bin/vasp_std"),
)

_VASP_MAKEFILE = Path("installations/vasp/6.3.2/makefile.include")
_VASP_LEGACY_ENV = re.compile(
    r"(?m)^VASP_ENV\s*=\s*/(?:inspire|mnt|home)/[^\n]+$"
)
_VASP_PORTABLE_ENV = """# Keep the build configuration relocatable.  A caller may override
# RESEARCHCHEMBENCH_ENV_ROOT for a staged environment; otherwise derive the
# consolidated general environment from this file's location.
ifeq ($(strip $(RESEARCHCHEMBENCH_ENV_ROOT)),)
VASP_ENV    ?= $(abspath $(dir $(lastword $(MAKEFILE_LIST)))/../../../../.envs/general-modern-openmpi5)
else
VASP_ENV    ?= $(RESEARCHCHEMBENCH_ENV_ROOT)/general-modern-openmpi5
endif"""


def _clear_stale_binary_rpaths(cache_root: Path) -> list[dict[str, str]]:
    """Remove embedded RPATHs from known profile-managed ELF entrypoints.

    ``chrpath`` is an optional migration helper.  Missing helper support is
    reported rather than treated as a migration failure; the profile remains
    usable when it supplies ``LD_LIBRARY_PATH`` explicitly.
    """

    helper = shutil.which("chrpath")
    records: list[dict[str, str]] = []
    for relative in _STALE_RPATH_BINARIES:
        path = cache_root / relative
        record = {"path": relative.as_posix()}
        if not path.is_file() or path.is_symlink():
            record["status"] = "missing"
            records.append(record)
            continue
        if helper is None:
            record["status"] = "helper_missing"
            records.append(record)
            continue
        listed = subprocess.run(
            [helper, "-l", str(path)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        if "no rpath or runpath tag" in listed.stdout.lower():
            record["status"] = "already_portable"
            records.append(record)
            continue
        if listed.returncode != 0:
            record["status"] = "not_elf"
            records.append(record)
            continue
        # ``migrate_v2`` may have created a hardlink from the legacy cache.
        # Break that link before mutating the ELF so the source remains intact.
        if path.stat().st_nlink > 1:
            temporary = path.with_name(f".{path.name}.rpath-copy-{os.getpid()}")
            shutil.copy2(path, temporary)
            temporary.replace(path)
        cleared = subprocess.run(
            [helper, "-d", str(path)],
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
        record["status"] = "cleared" if cleared.returncode == 0 else "clear_failed"
        if cleared.returncode != 0:
            record["output"] = cleared.stdout.strip()[-500:]
        records.append(record)
    return records


def _rewrite_vasp_makefile(cache_root: Path) -> dict[str, str]:
    """Replace the VASP build host's absolute environment path with a relative rule."""

    path = cache_root / _VASP_MAKEFILE
    record = {"path": _VASP_MAKEFILE.as_posix()}
    if not path.is_file() or path.is_symlink():
        record["status"] = "missing"
        return record
    text = path.read_text(encoding="utf-8")
    if "/inspire/" not in text and "/mnt/" not in text and "/home/" not in text:
        record["status"] = "already_portable"
        return record
    rewritten, count = _VASP_LEGACY_ENV.subn(_VASP_PORTABLE_ENV, text, count=1)
    if count != 1:
        record["status"] = "unexpected_format"
        return record
    temporary = path.with_name(f".{path.name}.relocate-{os.getpid()}")
    temporary.write_text(rewritten, encoding="utf-8")
    shutil.copystat(path, temporary)
    temporary.replace(path)
    record["status"] = "rewritten"
    return record


def _rewrite_acpype_launcher(cache_root: Path) -> dict[str, str]:
    """Replace the cached console script's build-host Python with its bundled runtime."""

    path = cache_root / _ACPYPE_LAUNCHER
    if not path.is_file() or path.is_symlink():
        return {"path": _ACPYPE_LAUNCHER.as_posix(), "status": "missing"}
    expected = """#!/usr/bin/env bash
set -euo pipefail
install_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/../.." && pwd)"
export PYTHONPATH="${install_root}/python${PYTHONPATH:+:${PYTHONPATH}}"
export BABEL_LIBDIR="${BABEL_LIBDIR:-${install_root}/deps/lib/openbabel/3.1.0}"
export BABEL_DATADIR="${BABEL_DATADIR:-${install_root}/deps/share/openbabel/3.1.0}"
exec "${install_root}/deps/bin/python" -m acpype.cli "$@"
"""
    if path.read_text(encoding="utf-8") == expected:
        return {"path": _ACPYPE_LAUNCHER.as_posix(), "status": "already_portable"}
    temporary = path.with_name(f".{path.name}.relocate-{os.getpid()}")
    temporary.write_text(expected, encoding="utf-8")
    shutil.copystat(path, temporary)
    temporary.replace(path)
    return {"path": _ACPYPE_LAUNCHER.as_posix(), "status": "rewritten"}


def _patch_kinbot_nwchem_reaction_family(cache_root: Path) -> dict[str, str]:
    """Add KinBot's missing NWChem template identifiers idempotently."""

    path = cache_root / _KINBOT_REACTION_FAMILY
    if not path.is_file() or path.is_symlink():
        return {"path": _KINBOT_REACTION_FAMILY.as_posix(), "status": "missing"}
    text = path.read_text(encoding="utf-8")
    expected = (
        "    elif rxn.qc.qc == 'nwchem':\n"
        "        code = 'nwchem'\n"
        "        Code = 'NWChem'\n"
    )
    if expected in text:
        return {
            "path": _KINBOT_REACTION_FAMILY.as_posix(),
            "status": "already_portable",
        }
    anchor = "    elif rxn.qc.qc == 'nn_pes' and step >= rxn.max_step:\n"
    if text.count(anchor) != 1:
        return {
            "path": _KINBOT_REACTION_FAMILY.as_posix(),
            "status": "unexpected_source",
        }
    rewritten = text.replace(anchor, expected + anchor, 1)
    temporary = path.with_name(f".{path.name}.relocate-{os.getpid()}")
    temporary.write_text(rewritten, encoding="utf-8")
    shutil.copystat(path, temporary)
    temporary.replace(path)
    return {"path": _KINBOT_REACTION_FAMILY.as_posix(), "status": "rewritten"}


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


def _rewrite_gamess_runtime_paths(path: Path) -> bool:
    """Make generated GAMESS tcsh files consume the runtime profile paths."""

    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return False
    rewritten = text
    for pattern, replacement in _GAMESS_RUNTIME_PATHS:
        rewritten = pattern.sub(replacement, rewritten)
    for pattern, replacement in _GAMESS_WRITABLE_DIRECTORY_ASSIGNMENTS:
        rewritten = pattern.sub(replacement, rewritten)
    if rewritten == text:
        return False
    temporary = path.with_name(f".{path.name}.relocate-{os.getpid()}")
    temporary.write_text(rewritten, encoding="utf-8")
    shutil.copystat(path, temporary)
    temporary.replace(path)
    return True


def _rewrite_gamess_files(cache_root: Path) -> list[dict[str, str]]:
    records = []
    for legacy_value in load_legacy_layout().get("portable_gamess_paths") or ():
        destination = classify_legacy_path(str(legacy_value))
        if destination is None:
            continue
        path = cache_root / destination
        if path.is_symlink():
            try:
                path.resolve(strict=True).relative_to(cache_root)
            except (FileNotFoundError, ValueError):
                records.append({"path": destination.as_posix(), "status": "invalid_link"})
            else:
                records.append({"path": destination.as_posix(), "status": "portable_link"})
            continue
        if not path.is_file():
            records.append({"path": destination.as_posix(), "status": "missing"})
            continue
        rewritten = _rewrite_gamess_runtime_paths(path)
        records.append(
            {
                "path": destination.as_posix(),
                "status": "rewritten" if rewritten else "already_portable",
            }
        )
    return records


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


def _rewrite_aiida_config(cache_root: Path) -> dict[str, str]:
    """Repair AiiDA's SQLite repository path after a cache relocation.

    AiiDA stores the repository path in JSON and older deployments wrote the
    complete checkout path there.  Keep the persisted value project-relative;
    the profile's ``AIIDA_PATH`` supplies the current checkout at runtime.
    """

    relative = Path("state/aiida/.aiida/config.json")
    path = cache_root / relative
    if not path.is_file() or path.is_symlink():
        return {"path": relative.as_posix(), "status": "missing"}
    try:
        document = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        return {"path": relative.as_posix(), "status": f"invalid:{exc.__class__.__name__}"}

    profiles = document.get("profiles")
    profile = profiles.get("researchchembench") if isinstance(profiles, dict) else None
    storage = profile.get("storage") if isinstance(profile, dict) else None
    config = storage.get("config") if isinstance(storage, dict) else None
    raw = config.get("filepath") if isinstance(config, dict) else None
    if not isinstance(raw, str) or not raw.strip():
        return {"path": relative.as_posix(), "status": "missing_filepath"}

    project_root = cache_root.parent
    configured = Path(raw).expanduser()
    current = configured if configured.is_absolute() else project_root / configured
    repository_root = cache_root / "state/aiida/.aiida/repository"
    # Prefer the repository referenced by the old config, then fall back to a
    # single repository migrated with the cache.  Never invent a missing path.
    candidates = []
    if current.is_dir() and (current / "database.sqlite").is_file():
        candidates.append(current)
    if repository_root.is_dir():
        candidates.extend(
            item for item in sorted(repository_root.iterdir())
            if item.is_dir() and (item / "database.sqlite").is_file()
        )
    if not candidates:
        return {"path": relative.as_posix(), "status": "repository_missing"}
    selected = candidates[0]
    # AiiDA resolves the SQLite filepath relative to the process directory.
    # The relocatable ``verdi`` shim changes into the profile's ``.aiida``
    # directory before invoking AiiDA, so persist only the repository-relative
    # component and never the checkout path.
    portable = (Path("repository") / selected.name).as_posix()
    if raw == portable:
        return {"path": relative.as_posix(), "status": "already_portable"}
    config["filepath"] = portable
    temporary = path.with_name(f".{path.name}.relocate-{os.getpid()}")
    temporary.write_text(
        json.dumps(document, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    shutil.copystat(path, temporary)
    temporary.replace(path)
    return {"path": relative.as_posix(), "status": "rewritten"}


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
        "cache_root": _portable_root_label(cache_root, destination=True),
        "portable_shebangs": records,
        "portable_wrappers": wrapper_records,
        "portable_gamess_files": _rewrite_gamess_files(cache_root),
        "portable_acpype_launcher": _rewrite_acpype_launcher(cache_root),
        "kinbot_nwchem_reaction_family": _patch_kinbot_nwchem_reaction_family(cache_root),
        "binary_rpaths": _clear_stale_binary_rpaths(cache_root),
        "vasp_makefile": _rewrite_vasp_makefile(cache_root),
        "portable_configs": _write_portable_config_files(cache_root),
        "aiida_config": _rewrite_aiida_config(cache_root),
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
        "legacy_root": _portable_root_label(legacy_root),
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
        "legacy_root": _portable_root_label(legacy_root),
        "destination_root": _portable_root_label(destination_root, destination=True),
        "counts": counts,
        "plan": plan,
        "unresolved_symlinks": unresolved_links,
        "portable_gamess_files": _rewrite_gamess_files(destination_root),
        "portable_acpype_launcher": _rewrite_acpype_launcher(destination_root),
        "kinbot_nwchem_reaction_family": _patch_kinbot_nwchem_reaction_family(destination_root),
        "binary_rpaths": _clear_stale_binary_rpaths(destination_root),
        "vasp_makefile": _rewrite_vasp_makefile(destination_root),
        "portable_configs": _write_portable_config_files(destination_root),
        "aiida_config": _rewrite_aiida_config(destination_root),
        "compatibility_links": _ensure_compatibility_links(destination_root),
    }
    write_json(destination_root / "receipts" / "legacy-v2-migration.json", report)
    return report
