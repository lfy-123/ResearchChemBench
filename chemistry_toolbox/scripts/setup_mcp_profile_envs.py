#!/usr/bin/env python3
"""Create isolated MCP and executable-support Conda environments."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


TOOLBOX_ROOT = Path(__file__).resolve().parents[1]
ROOT = TOOLBOX_ROOT.parent
CONFIG = TOOLBOX_ROOT / "config" / "mcp_profiles.yaml"
COMMON_PIP = TOOLBOX_ROOT / "environment" / "profiles" / "common-pip.txt"
STATUS_PATH = TOOLBOX_ROOT / "config" / "mcp_profile_status.json"
DEFAULT_PROFILES = (
    "services,quantum,psi4,reaction,qe,cp2k,periodic,phonons,md,mlip,docking"
)


def run(
    command: list[str],
    *,
    dry_run: bool = False,
    timeout_seconds: int = 1800,
) -> dict[str, Any]:
    print(f"+ {' '.join(command)}", flush=True)
    if dry_run:
        return {"returncode": 0, "command": command, "dry_run": True}
    try:
        completed = subprocess.run(
            command,
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
            env=os.environ.copy(),
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired as exc:
        output = exc.stdout if isinstance(exc.stdout, str) else ""
        if output:
            print(output[-4000:], flush=True)
        print(f"Timed out after {timeout_seconds} seconds", flush=True)
        return {
            "returncode": 124,
            "command": command,
            "output_tail": output[-2000:],
            "timeout_seconds": timeout_seconds,
        }
    if completed.stdout:
        print(completed.stdout[-4000:], flush=True)
    return {
        "returncode": completed.returncode,
        "command": command,
        "output_tail": completed.stdout[-2000:],
    }


def comma_list(value: str) -> list[str]:
    return [item.strip() for item in value.split(",") if item.strip()]


def load_existing_status(*, dry_run: bool) -> dict[str, Any]:
    if STATUS_PATH.exists() and not dry_run:
        try:
            value = json.loads(STATUS_PATH.read_text(encoding="utf-8"))
            if isinstance(value, dict):
                return value
        except (json.JSONDecodeError, OSError):
            pass
    return {}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profiles", default=DEFAULT_PROFILES)
    parser.add_argument(
        "--support-environments",
        default=None,
        help=(
            "Comma-separated executable-only environments. By default they are "
            "installed only when the default full profile set is requested."
        ),
    )
    parser.add_argument("--manager", default="")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--recreate", action="store_true")
    parser.add_argument("--continue-on-error", action="store_true")
    parser.add_argument(
        "--command-timeout",
        type=int,
        default=1800,
        help="Maximum seconds for one conda/pip operation (default: 1800).",
    )
    args = parser.parse_args()

    manager = args.manager or shutil.which("mamba") or shutil.which("conda")
    if not manager:
        raise SystemExit("mamba/conda was not found; pass --manager PATH")

    config = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    profiles = config["profiles"]
    support_environments = config.get("support_environments", {})
    selected_profiles = comma_list(args.profiles)
    selected_support = (
        comma_list(args.support_environments)
        if args.support_environments is not None
        else (list(support_environments) if args.profiles == DEFAULT_PROFILES else [])
    )
    unknown_profiles = sorted(set(selected_profiles) - set(profiles))
    unknown_support = sorted(set(selected_support) - set(support_environments))
    if unknown_profiles:
        raise SystemExit(f"Unknown profiles: {unknown_profiles}")
    if unknown_support:
        raise SystemExit(f"Unknown support environments: {unknown_support}")

    payload = load_existing_status(dry_run=args.dry_run)
    payload.update(
        {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "manager": manager,
        }
    )
    payload.setdefault("profiles", {})
    payload.setdefault("support_environments", {})

    def save_status() -> None:
        STATUS_PATH.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    def execute(command: list[str], record: dict[str, Any]) -> bool:
        step = run(
            command,
            dry_run=args.dry_run,
            timeout_seconds=args.command_timeout,
        )
        record["steps"].append(step)
        save_status()
        return step["returncode"] == 0

    def install_environment(
        name: str,
        specification: dict[str, Any],
        *,
        group: str,
        install_mcp_runtime: bool,
    ) -> bool:
        environment = (ROOT / specification["environment"]).resolve()
        record: dict[str, Any] = {
            "description": specification.get("description", ""),
            "conda_name": specification.get("conda_name", ""),
            "environment": str(environment),
            "conda_packages": specification.get("conda_packages", []),
            "pip_packages": specification.get("pip_packages", []),
            "steps": [],
            "status": "installing",
        }
        payload[group][name] = record
        save_status()
        print(f"\n=== {group} {name}: {environment} ===", flush=True)

        if args.recreate and environment.exists():
            if not execute(
                [manager, "env", "remove", "-y", "-p", str(environment)], record
            ):
                record["status"] = "failed_remove"
                save_status()
                return False

        python = environment / "bin" / "python"
        if not python.exists():
            if not execute(
                [
                    manager,
                    "create",
                    "-y",
                    "-p",
                    str(environment),
                    "--override-channels",
                    "-c",
                    "conda-forge",
                    f"python={specification.get('python_version', '3.10')}",
                    "pip",
                ],
                record,
            ):
                record["status"] = "failed_create"
                save_status()
                return False

        for package in specification.get("conda_packages", []):
            if not execute(
                [
                    manager,
                    "install",
                    "-y",
                    "-p",
                    str(environment),
                    "--override-channels",
                    "-c",
                    "conda-forge",
                    str(package),
                ],
                record,
            ):
                record.setdefault("failed_conda_packages", []).append(package)
                if not args.continue_on_error:
                    record["status"] = "partial"
                    save_status()
                    return False

        if install_mcp_runtime and not execute(
            [str(python), "-m", "pip", "install", "-r", str(COMMON_PIP)], record
        ):
            record["failed_common_pip"] = True
            if not args.continue_on_error:
                record["status"] = "partial"
                save_status()
                return False

        for package in specification.get("pip_packages", []):
            if not execute(
                [str(python), "-m", "pip", "install", str(package)], record
            ):
                record.setdefault("failed_pip_packages", []).append(package)
                if not args.continue_on_error:
                    record["status"] = "partial"
                    save_status()
                    return False

        failed = any(
            record.get(key)
            for key in (
                "failed_conda_packages",
                "failed_common_pip",
                "failed_pip_packages",
            )
        )
        record["status"] = "planned" if args.dry_run else ("partial" if failed else "installed")
        save_status()
        return not failed

    failed = False
    for name in selected_profiles:
        ok = install_environment(
            name,
            profiles[name],
            group="profiles",
            install_mcp_runtime=True,
        )
        failed = failed or not ok
        if not ok and not args.continue_on_error:
            break

    if not failed or args.continue_on_error:
        for name in selected_support:
            ok = install_environment(
                name,
                support_environments[name],
                group="support_environments",
                install_mcp_runtime=False,
            )
            failed = failed or not ok
            if not ok and not args.continue_on_error:
                break

    conda = shutil.which("conda")
    registration_command = [
        sys.executable,
        str(TOOLBOX_ROOT / "scripts" / "configure_mcp_conda_envs.py"),
    ]
    if conda:
        registration_command.extend(["--conda", conda])
    else:
        registration_command.append("--no-conda-config")
    if args.dry_run:
        registration_command.append("--dry-run")
    registration = run(
        registration_command,
        dry_run=False,
        timeout_seconds=args.command_timeout,
    )
    payload["conda_registration"] = registration
    failed = failed or registration["returncode"] != 0
    save_status()
    print(STATUS_PATH)
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
