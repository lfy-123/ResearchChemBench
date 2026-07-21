#!/usr/bin/env python3
"""Probe one backend runtime from inside that runtime's Python environment."""

from __future__ import annotations

import argparse
import importlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

TOOLBOX_ROOT = Path(__file__).resolve().parents[1]
ROOT = TOOLBOX_ROOT.parent
SOURCE_ROOT = TOOLBOX_ROOT / "src"
for path in (SOURCE_ROOT, ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--profile", required=True)
    parser.add_argument("--live-materials-project", action="store_true")
    parser.add_argument("--check-models", action="store_true")
    args = parser.parse_args()

    from chemistry_toolbox.mcp.profiles import apply_profile, load_profile_config
    from researchchem_toolbox.catalog import backend_specs
    from researchchem_toolbox.runtime import probe_all_backends

    profile = apply_profile(args.profile)
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
    command_results = {str(command): shutil.which(str(command)) for command in health.get("commands", [])}
    manual_results = {str(command): shutil.which(str(command)) for command in health.get("manual_commands", [])}
    external_results = {}
    for value in health.get("external_commands", []):
        from pathlib import Path

        path = Path(str(value)).expanduser()
        if not path.is_absolute():
            path = Path(__file__).resolve().parents[2] / path
        external_results[str(value)] = str(path.resolve()) if path.is_file() else None

    dependency_environment = os.environ.copy()
    dependency_environment.pop("PYTHONPATH", None)
    with tempfile.TemporaryDirectory(prefix="researchchem_pip_check_") as temporary:
        dependency_probe = subprocess.run(
            [sys.executable, "-m", "pip", "check"],
            cwd=temporary,
            env=dependency_environment,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            check=False,
        )
    dependency_lines = (
        [line.strip() for line in dependency_probe.stdout.splitlines() if line.strip()]
        if dependency_probe.returncode != 0
        else []
    )
    allowed_dependency_patterns = [
        re.compile(str(value))
        for value in health.get("allowed_dependency_issue_patterns", [])
    ]
    ignored_dependency_issues = [
        line
        for line in dependency_lines
        if any(pattern.fullmatch(line) for pattern in allowed_dependency_patterns)
    ]
    unignored_dependency_issues = [
        line for line in dependency_lines if line not in ignored_dependency_issues
    ]
    dependency_check = {
        "success": dependency_probe.returncode == 0 or not unignored_dependency_issues,
        "returncode": dependency_probe.returncode,
        "output": dependency_probe.stdout.strip(),
        "ignored_issues": ignored_dependency_issues,
        "unignored_issues": unignored_dependency_issues,
    }

    model_results = {}
    if args.check_models:
        for check_name, specification in (health.get("models") or {}).items():
            try:
                if str(specification["backend"]) != "mace_mp":
                    raise ValueError("Only mace_mp model checks are supported")
                from ase import Atoms
                from mace.calculators import mace_mp

                calculator = mace_mp(
                    model=str(specification["model"]),
                    device=str(specification.get("device") or "cpu"),
                    default_dtype=str(specification.get("default_dtype") or "float64"),
                )
                atoms = Atoms("Si", positions=[[0, 0, 0]], cell=[5.43] * 3, pbc=True)
                atoms.calc = calculator
                energy = float(atoms.get_potential_energy())
                model_results[str(check_name)] = {"success": math.isfinite(energy), "energy_ev": energy}
            except Exception as exc:
                model_results[str(check_name)] = {"success": False, "error": f"{type(exc).__name__}: {exc}"}

    specifications = [backend_specs()[backend_id] for backend_id in profile["backends"]]
    backend_health = probe_all_backends(specifications)
    allowed_unavailable = set(
        (load_profile_config().get("audit") or {}).get(
            "allowed_unavailable_backends", []
        )
    )
    unexpected_unavailable = sorted(
        backend_id
        for backend_id, item in backend_health.items()
        if not item.get("available") and backend_id not in allowed_unavailable
    )
    live_checks = {}
    if args.live_materials_project and "materials_project" in profile["backends"]:
        from researchchem_toolbox.service import execute_action

        result = execute_action(
            "search_materials",
            {"inputs": {"query": "mp-149"}, "method_spec": {}, "action_settings": {"max_records": 1}},
        )
        live_checks["materials_project"] = {"success": result["status"] == "success", "status": result["status"]}

    required_ok = (
        all(item["available"] for item in module_results.values())
        and all(command_results.values())
        and all(external_results.values())
        and dependency_check["success"]
        and not unexpected_unavailable
        and all(item.get("success", False) for item in model_results.values())
        and all(item.get("success", False) for item in live_checks.values())
    )
    result = {
        "profile": args.profile,
        "conda_name": profile.get("conda_name"),
        "python": sys.executable,
        "python_version": sys.version.split()[0],
        "expected_backends": sorted(profile["backends"]),
        "backend_health": backend_health,
        "allowed_unavailable_backends": sorted(
            set(profile["backends"]) & allowed_unavailable
        ),
        "unexpected_unavailable_backends": unexpected_unavailable,
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
