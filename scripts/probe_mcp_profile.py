#!/usr/bin/env python3
"""Probe one MCP profile from inside that profile's Python environment."""

from __future__ import annotations

import argparse
import asyncio
import importlib
import json
import math
import os
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", required=True)
    parser.add_argument("--live-materials-project", action="store_true")
    parser.add_argument("--check-models", action="store_true")
    args = parser.parse_args()

    # server.py selects the profile before constructing its module-level server.
    sys.argv = ["researchchem-mcp", "--profile", args.profile]
    from evaluation.mcp_tools.profiles import apply_profile, get_profile

    profile = apply_profile(args.profile)
    from evaluation.mcp_tools.server import mcp

    health = dict(profile.get("health_checks") or {})
    module_results = {}
    for module_name in health.get("modules", []):
        try:
            module = importlib.import_module(str(module_name))
            module_results[str(module_name)] = {
                "available": True,
                "version": str(getattr(module, "__version__", "unknown")),
            }
        except Exception as exc:
            module_results[str(module_name)] = {
                "available": False,
                "error": f"{type(exc).__name__}: {exc}",
            }

    command_results = {
        str(command): shutil.which(str(command))
        for command in health.get("commands", [])
    }
    manual_results = {
        str(command): shutil.which(str(command))
        for command in health.get("manual_commands", [])
    }
    external_results = {}
    for value in health.get("external_commands", []):
        path = Path(str(value)).expanduser()
        if not path.is_absolute():
            path = ROOT / path
        external_results[str(value)] = str(path.resolve()) if path.is_file() else None

    dependency_environment = os.environ.copy()
    dependency_environment.pop("PYTHONPATH", None)
    dependency_probe = subprocess.run(
        [sys.executable, "-m", "pip", "check"],
        cwd=Path(sys.prefix),
        env=dependency_environment,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    dependency_check = {
        "success": dependency_probe.returncode == 0,
        "returncode": dependency_probe.returncode,
        "output": dependency_probe.stdout.strip(),
    }

    model_results = {}
    if args.check_models:
        for check_name, specification in (health.get("models") or {}).items():
            try:
                backend = str(specification["backend"])
                if backend != "mace_mp":
                    raise ValueError(f"Unsupported model health-check backend: {backend}")
                from ase import Atoms
                from mace.calculators import mace_mp

                calculator = mace_mp(
                    model=str(specification["model"]),
                    device=str(specification.get("device") or "cpu"),
                    default_dtype=str(specification.get("default_dtype") or "float64"),
                )
                atoms = Atoms(
                    "Si",
                    positions=[[0.0, 0.0, 0.0]],
                    cell=[5.43, 5.43, 5.43],
                    pbc=True,
                )
                atoms.calc = calculator
                energy = float(atoms.get_potential_energy())
                model_results[str(check_name)] = {
                    "success": math.isfinite(energy),
                    "backend": backend,
                    "model": str(specification["model"]),
                    "energy_ev": energy,
                }
            except Exception as exc:
                model_results[str(check_name)] = {
                    "success": False,
                    "error": f"{type(exc).__name__}: {exc}",
                }

    tool_names = sorted(tool.name for tool in asyncio.run(mcp.list_tools()))
    live_checks = {}
    if args.live_materials_project and args.profile == "services":
        try:
            from evaluation.mcp_tools.tools.query_materials_project import (
                query_materials_project_core,
            )

            result = query_materials_project_core(material_id="mp-149", max_records=1)
            records = result.get("records") or []
            live_checks["materials_project"] = {
                "success": bool(
                    result.get("status") == "success"
                    and records
                    and records[0].get("material_id") == "mp-149"
                ),
                "status": result.get("status"),
                "count": result.get("count", 0),
                "material_id": records[0].get("material_id") if records else None,
            }
        except Exception as exc:
            live_checks["materials_project"] = {
                "success": False,
                "error": f"{type(exc).__name__}: {exc}",
            }

    required_ok = (
        tool_names == sorted(profile["tools"])
        and all(item["available"] for item in module_results.values())
        and all(command_results.values())
        and all(external_results.values())
        and dependency_check["success"]
        and all(item.get("success", False) for item in model_results.values())
        and all(item.get("success", False) for item in live_checks.values())
    )
    result = {
        "profile": args.profile,
        "conda_name": profile.get("conda_name"),
        "server_name": profile["server_name"],
        "python": sys.executable,
        "python_version": sys.version.split()[0],
        "expected_tools": sorted(profile["tools"]),
        "listed_tools": tool_names,
        "modules": module_results,
        "commands": command_results,
        "external_commands": external_results,
        "dependency_check": dependency_check,
        "model_checks": model_results,
        "manual_commands": manual_results,
        "live_checks": live_checks,
        "required_ok": required_ok,
    }
    print("PROFILE_PROBE_JSON=" + json.dumps(result, ensure_ascii=False))
    return 0 if required_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
