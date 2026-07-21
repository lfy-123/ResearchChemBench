#!/usr/bin/env python3
"""Capture exact Conda/Python locks and portable asset requirements.

The generated lock set is intentionally platform-specific.  It records exact
Conda artifact URLs/builds, only the distributions installed through pip, the
project editable install, runtime aliases, and checksums for registered or
critical external assets.  It never copies software, model weights, licenses,
or credentials into the source tree.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlparse

import yaml


TOOLBOX_ROOT = Path(__file__).resolve().parents[1]
ROOT = TOOLBOX_ROOT.parent
MCP_CONFIG = TOOLBOX_ROOT / "config" / "mcp_profiles.yaml"
AUX_CONFIG = TOOLBOX_ROOT / "config" / "auxiliary_environments.yaml"
RESOURCE_CONFIG = TOOLBOX_ROOT / "config" / "toolbox_resources.json"
REQUESTED_CONFIG = TOOLBOX_ROOT / "config" / "requested_software.yaml"
NATIVE_GUIDE_CONFIG = TOOLBOX_ROOT / "config" / "native_software_guides.yaml"
TOOL_CONFIG = TOOLBOX_ROOT / "mcp" / "tool_config.json"
DEFAULT_LOCK_ROOT = TOOLBOX_ROOT / "environment" / "locks"
PROJECT_DISTRIBUTION = "researchchembench"


def run(command: list[str], *, timeout: int = 300) -> str:
    completed = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=timeout,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            f"Command failed ({completed.returncode}): {' '.join(command)}\n"
            f"{completed.stderr[-4000:]}"
        )
    return completed.stdout


def canonical_name(value: str) -> str:
    return re.sub(r"[-_.]+", "-", value).lower().strip()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(4 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def relative(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path.resolve())


def declared_path(value: str) -> Path:
    path = Path(os.path.expandvars(os.path.expanduser(value)))
    return path if path.is_absolute() else ROOT / path


def load_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    if not isinstance(value, dict):
        raise ValueError(f"Expected a mapping in {path}")
    return value


def add_environment(
    environments: dict[str, dict[str, Any]],
    *,
    group: str,
    name: str,
    specification: dict[str, Any],
) -> None:
    prefix = declared_path(str(specification["environment"])).resolve()
    key = str(prefix)
    record = environments.setdefault(
        key,
        {
            "prefix": relative(prefix),
            "declared_by": [],
            "groups": [],
            "names": [],
            "conda_names": [],
            "backends": [],
            "descriptions": [],
        },
    )
    record["declared_by"].append(f"{group}.{name}")
    record["groups"].append(group)
    record["names"].append(name)
    if specification.get("conda_name"):
        record["conda_names"].append(str(specification["conda_name"]))
    record["backends"].extend(str(item) for item in specification.get("backends") or [])
    if specification.get("description"):
        record["descriptions"].append(str(specification["description"]))


def collect_environments() -> list[dict[str, Any]]:
    environments: dict[str, dict[str, Any]] = {}
    mcp = load_yaml(MCP_CONFIG)
    for group in ("profiles", "support_environments"):
        for name, specification in (mcp.get(group) or {}).items():
            add_environment(
                environments,
                group=f"mcp_profiles.{group}",
                name=str(name),
                specification=dict(specification),
            )
    auxiliary = load_yaml(AUX_CONFIG)
    for name, specification in (auxiliary.get("auxiliary_environments") or {}).items():
        add_environment(
            environments,
            group="auxiliary_environments",
            name=str(name),
            specification=dict(specification),
        )

    discovered = [ROOT / ".toolbox_env"]
    if (ROOT / ".tool_envs").is_dir():
        discovered.extend(sorted((ROOT / ".tool_envs").iterdir()))
    for prefix in discovered:
        if not prefix.is_dir():
            continue
        key = str(prefix.resolve())
        record = environments.setdefault(
            key,
            {
                "prefix": relative(prefix),
                "declared_by": [],
                "groups": [],
                "names": [],
                "conda_names": [],
                "backends": [],
                "descriptions": [],
            },
        )
        record.setdefault("discovered", True)

    used_ids: set[str] = set()
    records = []
    for value in sorted(environments.values(), key=lambda item: item["prefix"]):
        prefix = declared_path(value["prefix"]).resolve()
        if value["prefix"] == ".toolbox_env":
            base = "core"
        elif not str(value["prefix"]).startswith(".tool_envs/") and value["names"]:
            base = sorted(value["names"])[0]
        else:
            base = prefix.name
        lock_id = re.sub(r"[^A-Za-z0-9_.-]+", "_", base)
        if lock_id in used_ids:
            suffix = hashlib.sha256(str(prefix).encode()).hexdigest()[:8]
            lock_id = f"{lock_id}-{suffix}"
        used_ids.add(lock_id)
        value["id"] = lock_id
        value["exists"] = prefix.exists()
        value["kind"] = "conda" if (prefix / "conda-meta").is_dir() else "asset_runtime"
        for field in ("declared_by", "groups", "names", "conda_names", "backends", "descriptions"):
            value[field] = sorted(set(value[field]))
        records.append(value)
    return records


def freeze_name(line: str) -> str | None:
    value = line.strip()
    if not value or value.startswith("#"):
        return None
    if value.startswith("-e "):
        egg = re.search(r"[#&]egg=([^&]+)", value)
        return canonical_name(egg.group(1)) if egg else None
    if " @ " in value:
        return canonical_name(value.split(" @ ", 1)[0])
    match = re.match(r"^([A-Za-z0-9_.-]+)(?:===|==)", value)
    return canonical_name(match.group(1)) if match else None


def classify_requirement(line: str) -> str:
    lowered = line.lower()
    if lowered.startswith("-e "):
        return "editable_vcs" if "git+" in lowered else "editable_local"
    if " @ file:" in lowered:
        return "local"
    if "git+" in lowered or " @ http://" in lowered or " @ https://" in lowered:
        return "direct_url"
    return "index"


def local_requirement_path(line: str) -> Path | None:
    value = line.strip()
    if value.startswith("-e "):
        source = value[3:].strip()
    elif " @ " in value:
        source = value.split(" @ ", 1)[1].strip()
    else:
        return None
    if source.startswith("file:"):
        parsed = urlparse(source)
        return Path(unquote(parsed.path)).resolve()
    if source.startswith("/"):
        return Path(source).resolve()
    return None


def capture_pip_lock(
    python: Path,
    conda_packages: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[str], bool, list[dict[str, Any]]]:
    pypi = {
        canonical_name(str(item["name"])): item
        for item in conda_packages
        if str(item.get("channel") or "").lower() == "pypi"
        or str(item.get("build_string") or "") == "pypi_0"
    }
    if not pypi:
        return [], [], False, []
    freeze_lines = run([str(python), "-m", "pip", "freeze", "--all"]).splitlines()
    pip_inventory = {
        canonical_name(str(item["name"])): str(item["version"])
        for item in json.loads(
            run([str(python), "-m", "pip", "list", "--format", "json"])
        )
    }
    mapped = {
        name: line.strip()
        for line in freeze_lines
        if (name := freeze_name(line)) is not None
    }
    entries: list[dict[str, Any]] = []
    requirements: list[str] = []
    local_entries: list[dict[str, Any]] = []
    project_editable = False
    for name, package in sorted(pypi.items()):
        conda_recorded_version = str(package["version"])
        version = pip_inventory.get(name, conda_recorded_version)
        line = mapped.get(name) or f"{package['name']}=={version}"
        kind = classify_requirement(line)
        if name == canonical_name(PROJECT_DISTRIBUTION):
            project_editable = True
            entries.append(
                {
                    "name": str(package["name"]),
                    "version": version,
                    "kind": "project_editable",
                    "relative_path": ".",
                }
            )
            continue
        entry: dict[str, Any] = {
            "name": str(package["name"]),
            "version": version,
            "kind": kind,
        }
        if conda_recorded_version != version:
            entry["conda_recorded_version"] = conda_recorded_version
        path = local_requirement_path(line)
        if path is not None:
            try:
                local_relative = str(path.relative_to(ROOT))
            except ValueError:
                if kind == "editable_local":
                    entry["source_path"] = str(path)
                    entry["portable"] = False
                    local_entries.append(entry)
                else:
                    fallback = f"{package['name']}=={version}"
                    entry.update(
                        kind="index_fallback_from_local",
                        original_source_kind="file_url_outside_repository",
                        original_source_basename=path.name,
                        requirement=fallback,
                        portable=True,
                        byte_identical_source=False,
                    )
                    requirements.append(fallback)
            else:
                entry["relative_path"] = local_relative
                entry["portable"] = True
                local_entries.append(entry)
            entries.append(entry)
            continue
        entry["requirement"] = line
        entry["portable"] = True
        entries.append(entry)
        requirements.append(line)
    return entries, requirements, project_editable, local_entries


def capture_environment(
    record: dict[str, Any],
    *,
    conda: str,
    platform_lock_root: Path,
    skip_pip_check: bool,
) -> dict[str, Any]:
    prefix = declared_path(record["prefix"]).resolve()
    output = {**record}
    if record["kind"] != "conda" or not prefix.exists():
        output["captured"] = False
        return output
    lock_directory = platform_lock_root / record["id"]
    lock_directory.mkdir(parents=True, exist_ok=True)
    python = prefix / "bin" / "python"
    # Conda's pip interoperability cache can change its view of shadowed Conda
    # records the first time pip metadata is scanned.  Warm that view before
    # exporting either the package inventory or the final explicit lock.
    if python.is_file():
        run([str(python), "-m", "pip", "list", "--format", "json"])
    conda_packages = json.loads(
        run([conda, "list", "-p", str(prefix), "--json"], timeout=600)
    )
    pip_entries: list[dict[str, Any]] = []
    pip_requirements: list[str] = []
    project_editable = False
    local_entries: list[dict[str, Any]] = []
    python_version = None
    pip_check: dict[str, Any] = {"skipped": True}
    if python.is_file():
        python_version = run([str(python), "-c", "import platform; print(platform.python_version())"]).strip()
        pip_entries, pip_requirements, project_editable, local_entries = capture_pip_lock(
            python, conda_packages
        )
        if not skip_pip_check:
            completed = subprocess.run(
                [str(python), "-m", "pip", "check"],
                cwd=ROOT,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                check=False,
                timeout=300,
            )
            pip_check = {
                "returncode": completed.returncode,
                "ok": completed.returncode == 0,
                "output": completed.stdout.strip(),
            }
    explicit = run(
        [conda, "list", "-p", str(prefix), "--explicit", "--sha256"],
        timeout=600,
    )
    if "@EXPLICIT" not in explicit:
        raise RuntimeError(f"Conda did not produce an explicit lock for {prefix}")
    explicit_path = lock_directory / "conda-explicit.txt"
    explicit_path.write_text(explicit.rstrip() + "\n", encoding="utf-8")
    requirements_path = lock_directory / "pip-requirements.txt"
    requirements_path.write_text(
        "\n".join(pip_requirements) + ("\n" if pip_requirements else ""),
        encoding="utf-8",
    )
    pip_lock_path = lock_directory / "pip-lock.json"
    pip_lock_path.write_text(
        json.dumps(
            {
                "schema_version": 1,
                "entries": pip_entries,
                "project_editable": project_editable,
                "local_entries": local_entries,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    conda_count = sum(
        str(item.get("channel") or "").lower() != "pypi"
        and str(item.get("build_string") or "") != "pypi_0"
        for item in conda_packages
    )
    output.update(
        {
            "captured": True,
            "python_version": python_version,
            "conda_package_count": conda_count,
            "pip_package_count": len(pip_entries),
            "project_editable": project_editable,
            "conda_explicit_lock": str(explicit_path.relative_to(platform_lock_root)),
            "pip_requirements_lock": str(requirements_path.relative_to(platform_lock_root)),
            "pip_metadata_lock": str(pip_lock_path.relative_to(platform_lock_root)),
            "conda_lock_sha256": sha256(explicit_path),
            "pip_requirements_sha256": sha256(requirements_path),
            "pip_metadata_sha256": sha256(pip_lock_path),
            "pip_check": pip_check,
        }
    )
    return output


def merge_asset(
    assets: dict[str, dict[str, Any]],
    value: str,
    *,
    reason: str,
    required: bool,
    checksum_algorithm: str | None = None,
    checksum: str | None = None,
    hash_file: bool = False,
) -> None:
    path = declared_path(value)
    key = relative(path)
    record = assets.setdefault(
        key,
        {
            "path": key,
            "reasons": [],
            "required": False,
        },
    )
    record["reasons"].append(reason)
    record["required"] = bool(record["required"] or required)
    record["exists"] = path.exists()
    record["kind"] = "directory" if path.is_dir() else "file" if path.is_file() else "missing"
    if path.is_file():
        record["size_bytes"] = path.stat().st_size
    if checksum_algorithm and checksum:
        record["expected_checksum"] = {
            "algorithm": checksum_algorithm,
            "value": checksum,
        }
    if hash_file and path.is_file():
        record["captured_sha256"] = sha256(path)


def collect_assets(*, hash_critical_assets: bool) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    assets: dict[str, dict[str, Any]] = {}
    mcp = load_yaml(MCP_CONFIG)
    auxiliary = load_yaml(AUX_CONFIG)
    for group_name, group in (
        ("mcp_profiles.profiles", mcp.get("profiles") or {}),
        ("mcp_profiles.support_environments", mcp.get("support_environments") or {}),
        ("auxiliary_environments", auxiliary.get("auxiliary_environments") or {}),
    ):
        for name, raw in group.items():
            specification = dict(raw)
            reason = f"{group_name}.{name}"
            health_checks = dict(specification.get("health_checks") or {})
            external_commands = [
                *(specification.get("external_commands") or []),
                *(health_checks.get("external_commands") or []),
            ]
            for value in external_commands:
                merge_asset(
                    assets,
                    str(value),
                    reason=reason + ".external_commands",
                    required=True,
                    hash_file=hash_critical_assets,
                )
            for value in specification.get("cache_paths") or []:
                merge_asset(
                    assets,
                    str(value),
                    reason=reason + ".cache_paths",
                    required=False,
                )
            for field in ("path_entries", "library_path_entries"):
                for value in specification.get(field) or []:
                    merge_asset(
                        assets,
                        str(value),
                        reason=f"{reason}.{field}",
                        required=False,
                    )
            for variable, value in (specification.get("command_variables") or {}).items():
                text = str(value)
                if "/" in text or text.startswith("."):
                    merge_asset(
                        assets,
                        text,
                        reason=f"{reason}.command_variables.{variable}",
                        required=True,
                        hash_file=hash_critical_assets,
                    )

    resources = json.loads(RESOURCE_CONFIG.read_text(encoding="utf-8"))
    for specification in resources.get("resources") or []:
        resource_id = str(specification["id"])
        merge_asset(
            assets,
            str(specification["path"]),
            reason=f"toolbox_resources.{resource_id}",
            required=True,
            checksum_algorithm=specification.get("checksum_algorithm"),
            checksum=specification.get("checksum"),
            hash_file=False,
        )
        for field in ("archive", "distribution_archive", "source_archive"):
            supporting = specification.get(field)
            if isinstance(supporting, dict) and supporting.get("path"):
                merge_asset(
                    assets,
                    str(supporting["path"]),
                    reason=f"toolbox_resources.{resource_id}.{field}",
                    required=False,
                    checksum_algorithm=supporting.get("checksum_algorithm"),
                    checksum=supporting.get("checksum"),
                )
        for value in specification.get("import_sources") or []:
            merge_asset(
                assets,
                str(value),
                reason=f"toolbox_resources.{resource_id}.import_sources",
                required=False,
            )

    requested = load_yaml(REQUESTED_CONFIG)
    manual = []
    for item in requested.get("requested_software") or []:
        for value in item.get("cache_paths") or []:
            merge_asset(
                assets,
                str(value),
                reason=f"requested_software.{item.get('name')}.cache_paths",
                required=False,
            )
        if item.get("status_policy") in {"manual", "interface"}:
            manual.append(
                {
                    "name": item.get("name"),
                    "status_policy": item.get("status_policy"),
                    "license": item.get("license"),
                    "public_adapter": item.get("public_adapter"),
                    "mcp_exposure": item.get("mcp_exposure"),
                    "notes": item.get("notes"),
                }
            )
    for value in assets.values():
        value["reasons"] = sorted(set(value["reasons"]))
    return sorted(assets.values(), key=lambda item: item["path"]), manual


def cpu_flags() -> list[str]:
    try:
        text = Path("/proc/cpuinfo").read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    match = re.search(r"^flags\s*:\s*(.+)$", text, re.M)
    return sorted(set(match.group(1).split())) if match else []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--conda", default="")
    parser.add_argument("--output-root", type=Path, default=DEFAULT_LOCK_ROOT)
    parser.add_argument("--environments", default="all", help="Comma-separated lock ids or all.")
    parser.add_argument("--skip-pip-check", action="store_true")
    parser.add_argument("--hash-critical-assets", action="store_true")
    args = parser.parse_args()

    conda = args.conda or shutil.which("conda")
    if not conda:
        raise SystemExit("conda was not found; pass --conda PATH")
    info = json.loads(run([conda, "info", "--json"]))
    subdir = str(info.get("subdir") or info.get("platform") or "unknown")
    platform_lock_root = args.output_root.resolve() / subdir
    platform_lock_root.mkdir(parents=True, exist_ok=True)

    environments = collect_environments()
    selected = {item.strip() for item in args.environments.split(",") if item.strip()}
    if selected != {"all"}:
        unknown = selected - {item["id"] for item in environments}
        if unknown:
            raise SystemExit(f"Unknown environment lock ids: {sorted(unknown)}")
        environments = [item for item in environments if item["id"] in selected]

    captured = []
    for index, record in enumerate(environments, start=1):
        print(f"[{index}/{len(environments)}] capture {record['id']} -> {record['prefix']}", flush=True)
        captured.append(
            capture_environment(
                record,
                conda=conda,
                platform_lock_root=platform_lock_root,
                skip_pip_check=args.skip_pip_check,
            )
        )
    assets, manual = collect_assets(hash_critical_assets=args.hash_critical_assets)
    asset_path_text = "\n".join(str(item["path"]).lower() for item in assets)
    required_cpu_flags = []
    if "avx2" in asset_path_text:
        required_cpu_flags.append("avx2")
    if "avx512" in asset_path_text or "avx-512" in asset_path_text:
        required_cpu_flags.append("avx512f")
    source_flags = cpu_flags()
    git_commit = run(["git", "rev-parse", "HEAD"]).strip()
    manifest = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repository_commit": git_commit,
        "lock_platform": subdir,
        "source_host": {
            "system": platform.system(),
            "machine": platform.machine(),
            "libc": list(platform.libc_ver()),
            "python": platform.python_version(),
            "conda_version": info.get("conda_version"),
            "cpu_flags_of_interest": [
                value for value in ("avx", "avx2", "avx512f", "fma") if value in source_flags
            ],
        },
        "policy": {
            "exact_conda_artifacts": True,
            "pip_no_dependencies": True,
            "automatic_licensed_downloads": False,
            "automatic_credential_copy": False,
            "asset_roots": [".software_cache", ".model_cache", "download"],
            "required_cpu_flags": required_cpu_flags,
        },
        "configuration_files": {
            relative(path): {"sha256": sha256(path)}
            for path in (
                MCP_CONFIG,
                AUX_CONFIG,
                RESOURCE_CONFIG,
                REQUESTED_CONFIG,
                NATIVE_GUIDE_CONFIG,
                TOOL_CONFIG,
            )
        },
        "summary": {
            "environment_count": len(captured),
            "captured_conda_environments": sum(bool(item.get("captured")) for item in captured),
            "asset_runtime_count": sum(item.get("kind") == "asset_runtime" for item in captured),
            "required_asset_count": sum(bool(item.get("required")) for item in assets),
            "missing_required_assets": sum(
                bool(item.get("required")) and not bool(item.get("exists")) for item in assets
            ),
            "manual_or_interface_items": len(manual),
        },
        "environments": captured,
        "assets": assets,
        "manual_items": manual,
    }
    manifest_path = platform_lock_root / "manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(manifest_path)
    print(json.dumps(manifest["summary"], ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
