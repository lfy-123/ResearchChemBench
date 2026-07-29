#!/usr/bin/env python3
"""Recreate or verify the complete ResearchChemBench chemistry toolbox.

This bootstrapper deliberately uses only the Python standard library so that a
fresh host can run it before the project Conda environment exists.  Exact
Conda artifacts and pip distributions come from the platform lock manifest;
licensed programs, model weights, pseudopotentials, and other large assets are
copied or linked from an operator-supplied ResearchChemBench asset tree.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import re
import shlex
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable


TOOLBOX_ROOT = Path(__file__).resolve().parents[1]
ROOT = TOOLBOX_ROOT.parent
DEFAULT_LOCK_ROOT = TOOLBOX_ROOT / "environment" / "locks"
DEFAULT_ASSET_ROOTS = (".software_cache", ".model_cache")


class BootstrapError(RuntimeError):
    """A reproducibility or installation invariant was not satisfied."""


def canonical_name(value: str) -> str:
    return re.sub(r"[-_.]+", "-", value).lower().strip()


def file_digest(path: Path, algorithm: str = "sha256") -> str:
    digest = hashlib.new(algorithm)
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(8 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def cpu_flags() -> set[str]:
    try:
        value = Path("/proc/cpuinfo").read_text(encoding="utf-8", errors="replace")
    except OSError:
        return set()
    match = re.search(r"^flags\s*:\s*(.+)$", value, re.M)
    return set(match.group(1).split()) if match else set()


def shell_join(command: Iterable[object]) -> str:
    return shlex.join(str(item) for item in command)


def run(
    command: list[str],
    *,
    cwd: Path,
    dry_run: bool = False,
    environment: dict[str, str] | None = None,
    timeout: int = 3600,
) -> subprocess.CompletedProcess[str]:
    print("+ " + shell_join(command), flush=True)
    if dry_run:
        return subprocess.CompletedProcess(command, 0, "", "")
    completed = subprocess.run(
        command,
        cwd=cwd,
        env=environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        timeout=timeout,
    )
    if completed.stdout:
        print(completed.stdout.rstrip(), flush=True)
    if completed.returncode != 0:
        raise BootstrapError(
            f"Command failed ({completed.returncode}): {shell_join(command)}"
        )
    return completed


def find_manager(explicit: str = "") -> str:
    if explicit:
        path = shutil.which(explicit) or str(Path(explicit).expanduser())
        if not Path(path).is_file():
            raise BootstrapError(f"Conda manager does not exist: {path}")
        return path
    for name in ("conda", "mamba"):
        if path := shutil.which(name):
            return path
    raise BootstrapError("Neither mamba nor conda was found; pass --manager PATH")


def conda_info(manager: str) -> dict[str, Any]:
    completed = subprocess.run(
        [manager, "info", "--json"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=120,
    )
    if completed.returncode != 0:
        raise BootstrapError(f"Unable to query Conda: {completed.stderr[-2000:]}")
    return json.loads(completed.stdout)


def host_subdir(info: dict[str, Any]) -> str:
    return str(info.get("subdir") or info.get("platform") or "unknown")


def resolve_manifest(lock_root: Path, subdir: str) -> tuple[Path, dict[str, Any]]:
    candidate = lock_root.expanduser().resolve()
    if candidate.is_file():
        manifest_path = candidate
    elif (candidate / "manifest.json").is_file():
        manifest_path = candidate / "manifest.json"
    else:
        manifest_path = candidate / subdir / "manifest.json"
    if not manifest_path.is_file():
        raise BootstrapError(f"No lock manifest for {subdir}: {manifest_path}")
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    if int(payload.get("schema_version", 0)) != 1:
        raise BootstrapError(f"Unsupported lock schema: {payload.get('schema_version')}")
    return manifest_path, payload


def locked_file(manifest_directory: Path, relative: str, expected_sha256: str) -> Path:
    path = (manifest_directory / relative).resolve()
    try:
        path.relative_to(manifest_directory.resolve())
    except ValueError as exc:
        raise BootstrapError(f"Lock path escapes manifest directory: {relative}") from exc
    if not path.is_file():
        raise BootstrapError(f"Missing lock file: {path}")
    actual = file_digest(path)
    if actual.lower() != expected_sha256.lower():
        raise BootstrapError(
            f"Lock checksum mismatch for {path}: expected {expected_sha256}, got {actual}"
        )
    return path


def safe_target_prefix(target_root: Path, declared_prefix: str) -> Path:
    prefix = Path(declared_prefix)
    if prefix.is_absolute():
        raise BootstrapError(f"Absolute environment prefixes are not portable: {prefix}")
    target = (target_root / prefix).resolve()
    try:
        target.relative_to(target_root.resolve())
    except ValueError as exc:
        raise BootstrapError(f"Environment prefix escapes target root: {prefix}") from exc
    if prefix.parts[:1] not in {
        (".toolbox_env",),
        (".tool_envs",),
        (".tool_envs_merged",),
    }:
        raise BootstrapError(f"Refusing unmanaged environment prefix: {prefix}")
    return target


def explicit_entries(text: str) -> set[str]:
    return {
        line.strip()
        for line in text.splitlines()
        if line.strip() and not line.lstrip().startswith("#") and line.strip() != "@EXPLICIT"
    }


def verify_conda_lock(manager: str, prefix: Path, lock_path: Path) -> dict[str, Any]:
    if not (prefix / "conda-meta").is_dir():
        raise BootstrapError(f"Missing Conda environment: {prefix}")
    command = [manager, "list", "-p", str(prefix), "--explicit", "--sha256"]
    completed = subprocess.run(
        command,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=600,
    )
    hash_verified = True
    if completed.returncode != 0:
        command = [manager, "list", "-p", str(prefix), "--explicit"]
        completed = subprocess.run(
            command,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=600,
        )
        hash_verified = False
    if completed.returncode != 0:
        raise BootstrapError(f"Unable to inspect {prefix}: {completed.stderr[-2000:]}")
    expected = explicit_entries(lock_path.read_text(encoding="utf-8"))
    actual = explicit_entries(completed.stdout)
    if not hash_verified:
        expected = {item.split("#", 1)[0] for item in expected}
        actual = {item.split("#", 1)[0] for item in actual}
    missing = sorted(expected - actual)
    extra = sorted(actual - expected)
    if missing or extra:
        raise BootstrapError(
            f"Conda lock mismatch for {prefix}: {len(missing)} missing, {len(extra)} extra"
        )
    return {
        "exact": True,
        "package_count": len(expected),
        "artifact_hashes_verified": hash_verified,
    }


def pip_inventory(python: Path) -> dict[str, str]:
    completed = subprocess.run(
        [str(python), "-m", "pip", "list", "--format", "json"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
        timeout=300,
    )
    if completed.returncode != 0:
        raise BootstrapError(f"Unable to inspect pip packages in {python.parent.parent}")
    return {
        canonical_name(str(item["name"])): str(item["version"])
        for item in json.loads(completed.stdout)
    }


def verify_pip_lock(
    prefix: Path,
    metadata_path: Path,
    source_pip_check: dict[str, Any],
) -> dict[str, Any]:
    python = prefix / "bin" / "python"
    if not python.is_file():
        return {"checked": False, "reason": "environment has no Python executable"}
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    installed = pip_inventory(python)
    mismatches = []
    for entry in metadata.get("entries") or []:
        name = canonical_name(str(entry["name"]))
        expected = str(entry["version"])
        actual = installed.get(name)
        if actual != expected:
            mismatches.append({"name": name, "expected": expected, "actual": actual})
    if mismatches:
        raise BootstrapError(f"pip lock mismatch for {prefix}: {mismatches[:8]}")
    check = subprocess.run(
        [str(python), "-m", "pip", "check"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
        timeout=300,
    )
    baseline_ok = source_pip_check.get("ok")
    if baseline_ok is True and check.returncode != 0:
        raise BootstrapError(f"pip check regressed for {prefix}: {check.stdout[-2000:]}")
    return {
        "checked": True,
        "locked_package_count": len(metadata.get("entries") or []),
        "pip_check_ok": check.returncode == 0,
        "source_pip_check_ok": baseline_ok,
        "pip_check_output": check.stdout.strip(),
    }


def pip_install_options(args: argparse.Namespace) -> list[str]:
    options = ["--no-deps"]
    if args.offline or args.no_index:
        options.append("--no-index")
    if args.wheelhouse:
        options.extend(["--find-links", str(args.wheelhouse.expanduser().resolve())])
    return options


def install_pip_layer(
    prefix: Path,
    requirements: Path,
    metadata_path: Path,
    target_root: Path,
    args: argparse.Namespace,
) -> list[str]:
    python = prefix / "bin" / "python"
    if not python.is_file() and not args.dry_run:
        return []
    commands: list[str] = []
    options = pip_install_options(args)
    if requirements.read_text(encoding="utf-8").strip():
        command = [str(python), "-m", "pip", "install", *options, "-r", str(requirements)]
        run(command, cwd=target_root, dry_run=args.dry_run)
        commands.append(shell_join(command))
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    for entry in metadata.get("local_entries") or []:
        if not entry.get("portable"):
            raise BootstrapError(
                f"Non-portable local pip source for {entry.get('name')}: "
                f"{entry.get('source_path')}"
            )
        source = (target_root / str(entry["relative_path"])).resolve()
        if not args.dry_run and not source.exists():
            raise BootstrapError(f"Missing local pip source: {source}")
        command = [str(python), "-m", "pip", "install", *options]
        if str(entry.get("kind")) == "editable_local":
            command.append("--editable")
        command.append(str(source))
        run(command, cwd=target_root, dry_run=args.dry_run)
        commands.append(shell_join(command))
    if metadata.get("project_editable"):
        command = [
            str(python),
            "-m",
            "pip",
            "install",
            *options,
            "--editable",
            str(target_root),
        ]
        run(command, cwd=target_root, dry_run=args.dry_run)
        commands.append(shell_join(command))
    return commands


def remove_environment(manager: str, prefix: Path, target_root: Path, dry_run: bool) -> None:
    safe_target_prefix(target_root, str(prefix.relative_to(target_root)))
    if not prefix.exists():
        return
    if (prefix / "conda-meta").is_dir():
        run(
            [manager, "env", "remove", "-y", "-p", str(prefix)],
            cwd=target_root,
            dry_run=dry_run,
        )
    elif dry_run:
        print(f"+ remove non-Conda path {prefix}")
    else:
        raise BootstrapError(f"Refusing to remove non-Conda path: {prefix}")


def restore_environment(
    manager: str,
    record: dict[str, Any],
    manifest_directory: Path,
    target_root: Path,
    args: argparse.Namespace,
) -> dict[str, Any]:
    if record.get("kind") != "conda" or not record.get("captured"):
        prefix, portable = asset_target(target_root, str(record["prefix"]))
        return {
            "id": record["id"],
            "prefix": str(prefix),
            "status": "asset_runtime",
            "exists": prefix.exists(),
            "portable": portable,
        }
    prefix = safe_target_prefix(target_root, str(record["prefix"]))
    conda_lock = locked_file(
        manifest_directory,
        str(record["conda_explicit_lock"]),
        str(record["conda_lock_sha256"]),
    )
    requirements = locked_file(
        manifest_directory,
        str(record["pip_requirements_lock"]),
        str(record["pip_requirements_sha256"]),
    )
    metadata = locked_file(
        manifest_directory,
        str(record["pip_metadata_lock"]),
        str(record["pip_metadata_sha256"]),
    )
    existed = (prefix / "conda-meta").is_dir()
    if args.recreate and not args.verify_only:
        remove_environment(manager, prefix, target_root, args.dry_run)
        existed = False
    if not existed:
        if args.verify_only:
            raise BootstrapError(f"Environment is absent in verify-only mode: {prefix}")
        prefix.parent.mkdir(parents=True, exist_ok=True) if not args.dry_run else None
        command = [manager, "create", "-y", "-p", str(prefix), "--file", str(conda_lock)]
        if args.offline:
            command.append("--offline")
        run(command, cwd=target_root, dry_run=args.dry_run, timeout=7200)
        install_pip_layer(prefix, requirements, metadata, target_root, args)
    if args.dry_run and not existed:
        return {
            "id": record["id"],
            "prefix": str(prefix),
            "status": "planned",
            "created": True,
        }
    conda_result = verify_conda_lock(manager, prefix, conda_lock)
    pip_result = verify_pip_lock(prefix, metadata, dict(record.get("pip_check") or {}))
    return {
        "id": record["id"],
        "prefix": str(prefix),
        "status": "verified",
        "created": not existed,
        "conda": conda_result,
        "pip": pip_result,
    }


def copy_asset_roots(
    source_root: Path,
    target_root: Path,
    roots: list[str],
    mode: str,
    dry_run: bool,
) -> list[dict[str, Any]]:
    results = []
    for relative in roots:
        source = (source_root / relative).resolve()
        destination = target_root / relative
        record: dict[str, Any] = {
            "root": relative,
            "source": str(source),
            "destination": str(destination),
            "mode": mode,
        }
        if not source.exists():
            record.update(status="missing_source")
            results.append(record)
            continue
        if source == destination.resolve():
            record.update(status="already_local")
            results.append(record)
            continue
        if mode == "link":
            if destination.is_symlink() and destination.resolve() == source:
                record.update(status="already_linked")
            elif destination.exists() or destination.is_symlink():
                raise BootstrapError(f"Refusing to replace existing asset root: {destination}")
            else:
                print(f"+ ln -s {source} {destination}")
                if not dry_run:
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    destination.symlink_to(source, target_is_directory=source.is_dir())
                record.update(status="linked")
        else:
            if shutil.which("rsync"):
                source_argument = str(source) + ("/" if source.is_dir() else "")
                destination_argument = str(destination) + ("/" if source.is_dir() else "")
                run(
                    ["rsync", "-a", source_argument, destination_argument],
                    cwd=target_root,
                    dry_run=dry_run,
                    timeout=86400,
                )
            else:
                print(f"+ copy {source} -> {destination}")
                if not dry_run:
                    if source.is_dir():
                        shutil.copytree(source, destination, symlinks=True, dirs_exist_ok=True)
                    else:
                        destination.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(source, destination, follow_symlinks=False)
            record.update(status="copied")
        results.append(record)
    return results


def asset_target(target_root: Path, declared: str) -> tuple[Path, bool]:
    path = Path(declared)
    if path.is_absolute():
        return path, False
    resolved = Path(os.path.abspath(target_root / path))
    try:
        resolved.relative_to(target_root.resolve())
    except ValueError as exc:
        raise BootstrapError(f"Asset path escapes target root: {declared}") from exc
    return resolved, True


def verify_assets(target_root: Path, assets: list[dict[str, Any]]) -> dict[str, Any]:
    results = []
    failures = []
    for specification in assets:
        path, portable = asset_target(target_root, str(specification["path"]))
        exists = path.exists()
        item: dict[str, Any] = {
            "path": str(specification["path"]),
            "resolved_path": str(path),
            "portable": portable,
            "required": bool(specification.get("required")),
            "exists": exists,
        }
        expected = specification.get("expected_checksum")
        captured = specification.get("captured_sha256")
        if exists and path.is_file() and isinstance(expected, dict):
            actual = file_digest(path, str(expected["algorithm"]))
            item["checksum_ok"] = actual.lower() == str(expected["value"]).lower()
        elif exists and path.is_file() and captured:
            item["checksum_ok"] = file_digest(path) == str(captured)
        if item["required"] and (not exists or item.get("checksum_ok") is False):
            failures.append(item)
        results.append(item)
    if failures:
        raise BootstrapError(f"Required asset verification failed for {len(failures)} paths")
    return {
        "checked": len(results),
        "required": sum(bool(item.get("required")) for item in results),
        "present": sum(bool(item.get("exists")) for item in results),
        "results": results,
    }


def verify_configuration_files(
    target_root: Path, records: dict[str, dict[str, str]]
) -> dict[str, Any]:
    mismatches = []
    for relative, metadata in records.items():
        path = target_root / relative
        actual = file_digest(path) if path.is_file() else None
        expected = str(metadata["sha256"])
        if actual != expected:
            mismatches.append({"path": relative, "expected": expected, "actual": actual})
    if mismatches:
        raise BootstrapError(
            "The checkout configuration differs from the lock manifest: "
            + ", ".join(item["path"] for item in mismatches)
        )
    return {"checked": len(records), "exact": True}


def compatibility_check(
    manifest: dict[str, Any], current_subdir: str, allow_cpu_mismatch: bool
) -> dict[str, Any]:
    locked_subdir = str(manifest["lock_platform"])
    if locked_subdir != current_subdir:
        raise BootstrapError(
            f"Platform lock mismatch: lock={locked_subdir}, host={current_subdir}"
        )
    required = set(manifest.get("policy", {}).get("required_cpu_flags") or [])
    missing = sorted(required - cpu_flags())
    if missing and not allow_cpu_mismatch:
        raise BootstrapError(
            f"Host CPU lacks flags required by configured binaries: {', '.join(missing)}; "
            "use --allow-cpu-mismatch only if those backends will stay disabled"
        )
    source_libc = (manifest.get("source_host", {}).get("libc") or ["", ""])[1]
    return {
        "platform": current_subdir,
        "required_cpu_flags": sorted(required),
        "missing_cpu_flags": missing,
        "source_libc": source_libc,
        "host_libc": platform.libc_ver()[1],
    }


def post_configure(target_root: Path, manager: str, args: argparse.Namespace) -> list[str]:
    python = target_root / ".toolbox_env" / "bin" / "python"
    if args.dry_run:
        python_exists = True
    else:
        python_exists = python.is_file()
    if not python_exists:
        raise BootstrapError(f"Core Python is unavailable: {python}")
    commands = [
        [
            str(python),
            str(target_root / "chemistry_toolbox/scripts/configure_toolbox_resources.py"),
            "--quick",
            "--no-write",
        ],
        [
            str(python),
            str(target_root / "chemistry_toolbox/scripts/configure_mcp_conda_envs.py"),
            "--conda",
            manager,
            "--no-conda-config",
            "--keep-prefix-registry",
        ],
    ]
    executed = []
    for command in commands:
        run(command, cwd=target_root, dry_run=args.dry_run, timeout=7200)
        executed.append(shell_join(command))
    return executed


def post_verify(target_root: Path, args: argparse.Namespace) -> list[str]:
    python = target_root / ".toolbox_env" / "bin" / "python"
    commands = [
        [str(python), "-m", "chemistry_toolbox.mcp.tool_manager", "validate"],
        [
            str(python),
            str(target_root / "chemistry_toolbox/scripts/verify_toolbox.py"),
            "--no-write",
        ],
    ]
    if args.full_verify:
        commands.extend(
            [
                [
                    str(python),
                    str(target_root / "chemistry_toolbox/scripts/check_mcp_tools.py"),
                    "--smoke",
                ],
                [
                    str(python),
                    str(target_root / "chemistry_toolbox/scripts/check_mcp_profile_envs.py"),
                    "--no-write",
                    "--timeout-seconds",
                    str(args.profile_timeout),
                ],
            ]
        )
    executed = []
    for command in commands:
        run(
            command,
            cwd=target_root,
            dry_run=args.dry_run,
            timeout=max(86400, args.profile_timeout * 100),
        )
        executed.append(shell_join(command))
    return executed


def select_environments(
    records: list[dict[str, Any]], selection: str
) -> list[dict[str, Any]]:
    requested = {item.strip() for item in selection.split(",") if item.strip()}
    if not requested or requested == {"all"}:
        return records
    known = {str(item["id"]) for item in records}
    unknown = requested - known
    if unknown:
        raise BootstrapError(f"Unknown environment ids: {sorted(unknown)}")
    return [item for item in records if str(item["id"]) in requested]


def write_report(path: Path, payload: dict[str, Any]) -> None:
    path = path.expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(path)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--lock-root", type=Path, default=DEFAULT_LOCK_ROOT)
    parser.add_argument("--manager", default="")
    parser.add_argument("--environments", default="all")
    parser.add_argument("--target-root", type=Path, default=ROOT)
    parser.add_argument("--asset-source", type=Path)
    parser.add_argument("--asset-mode", choices=("copy", "link", "skip"), default="copy")
    parser.add_argument("--recreate", action="store_true")
    parser.add_argument("--verify-only", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--wheelhouse", type=Path)
    parser.add_argument("--no-index", action="store_true")
    parser.add_argument("--continue-on-error", action="store_true")
    parser.add_argument("--skip-post-configure", action="store_true")
    parser.add_argument("--skip-post-verify", action="store_true")
    parser.add_argument("--full-verify", action="store_true")
    parser.add_argument("--profile-timeout", type=int, default=600)
    parser.add_argument("--allow-cpu-mismatch", action="store_true")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()

    if args.verify_only and args.recreate:
        parser.error("--verify-only and --recreate cannot be combined")
    if args.offline and not args.wheelhouse and not args.verify_only:
        print(
            "warning: --offline was requested without --wheelhouse; pip restoration can "
            "only succeed if every required wheel is available from another configured source",
            file=sys.stderr,
        )

    target_root = args.target_root.expanduser().resolve()
    manager = find_manager(args.manager)
    info = conda_info(manager)
    subdir = host_subdir(info)
    manifest_path, manifest = resolve_manifest(args.lock_root, subdir)
    manifest_directory = manifest_path.parent
    payload: dict[str, Any] = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "mode": (
            "dry_run" if args.dry_run else "verify_only" if args.verify_only else "restore"
        ),
        "target_root": str(target_root),
        "manifest": str(manifest_path),
        "manager": manager,
        "status": "running",
        "errors": [],
    }
    try:
        payload["compatibility"] = compatibility_check(
            manifest, subdir, args.allow_cpu_mismatch
        )
        payload["configuration"] = verify_configuration_files(
            target_root, dict(manifest.get("configuration_files") or {})
        )
        roots = list(manifest.get("policy", {}).get("asset_roots") or DEFAULT_ASSET_ROOTS)
        if args.asset_source and args.asset_mode != "skip" and not args.verify_only:
            payload["asset_transfer"] = copy_asset_roots(
                args.asset_source.expanduser().resolve(),
                target_root,
                roots,
                args.asset_mode,
                args.dry_run,
            )
        else:
            payload["asset_transfer"] = []

        selected = select_environments(
            list(manifest.get("environments") or []), args.environments
        )
        environment_results = []
        for index, record in enumerate(selected, start=1):
            print(
                f"[{index}/{len(selected)}] {record['id']} -> {record['prefix']}",
                flush=True,
            )
            try:
                environment_results.append(
                    restore_environment(
                        manager, record, manifest_directory, target_root, args
                    )
                )
            except Exception as exc:  # continue mode intentionally records every failure
                failure = {
                    "id": record.get("id"),
                    "prefix": record.get("prefix"),
                    "status": "failed",
                    "error": str(exc),
                }
                environment_results.append(failure)
                payload["errors"].append(failure)
                if not args.continue_on_error:
                    raise
        payload["environments"] = environment_results

        if (
            not args.verify_only
            and not args.skip_post_configure
            and not payload["errors"]
            and args.environments == "all"
        ):
            payload["post_configure"] = post_configure(target_root, manager, args)
        else:
            payload["post_configure"] = []

        if not args.dry_run:
            payload["assets"] = verify_assets(
                target_root, list(manifest.get("assets") or [])
            )
        else:
            payload["assets"] = {"skipped": "dry_run"}

        if (
            not args.skip_post_verify
            and not payload["errors"]
            and args.environments == "all"
        ):
            payload["post_verify"] = post_verify(target_root, args)
        else:
            payload["post_verify"] = []
        payload["status"] = "failed" if payload["errors"] else "passed"
    except Exception as exc:
        if not payload["errors"] or payload["errors"][-1].get("error") != str(exc):
            payload["errors"].append({"error": str(exc)})
        payload["status"] = "failed"
        print(f"ERROR: {exc}", file=sys.stderr)
    finally:
        payload["finished_at"] = datetime.now(timezone.utc).isoformat()
        if args.report and not args.dry_run:
            write_report(args.report, payload)

    summary = {
        "status": payload["status"],
        "environments": len(payload.get("environments") or []),
        "failed_environments": sum(
            item.get("status") == "failed" for item in payload.get("environments") or []
        ),
        "errors": len(payload["errors"]),
    }
    print(json.dumps(summary, ensure_ascii=False))
    return 0 if payload["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
