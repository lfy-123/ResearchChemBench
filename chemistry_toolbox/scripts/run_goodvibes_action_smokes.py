#!/usr/bin/env python3
"""Run bounded real GoodVibes 4.3 smoke tests for every registered Action."""

from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


TOOLBOX_ROOT = Path(__file__).resolve().parents[1]
ROOT = TOOLBOX_ROOT.parent
SOURCE_ROOT = TOOLBOX_ROOT / "src"
for path in (SOURCE_ROOT, ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from researchchem_toolbox.service import execute_action


OUTPUT = TOOLBOX_ROOT / "config" / "goodvibes_action_smoke_status.json"
GOODVIBES_SOURCE = ROOT / ".software_cache" / "goodvibes" / "4.3.0" / "source"


def common_settings(*, temperature: bool = True) -> dict[str, Any]:
    settings: dict[str, Any] = {
        "standard_state": "gas_1atm",
        "entropy_model": "grimme",
        "enthalpy_model": "head_gordon",
        "frequency_scale_factor": 1.0,
        "zpe_scale_factor": 1.0,
        "symmetry_correction": False,
        "imaginary_frequency_policy": "retain",
        "entropy_frequency_cutoff_cm1": 100.0,
        "enthalpy_frequency_cutoff_cm1": 100.0,
        "free_rotor_inertia_model": "global",
    }
    if temperature:
        settings["temperature_kelvin"] = 298.15
    return settings


def request(inputs: dict[str, Any], settings: dict[str, Any]) -> dict[str, Any]:
    return {
        "backend_id": "goodvibes",
        "inputs": inputs,
        "method_spec": {},
        "action_settings": settings,
        "resource_limits": {"cpu_cores": 2, "walltime_seconds": 300},
    }


def cases(workspace: Path) -> list[tuple[str, str, dict[str, Any]]]:
    g16 = GOODVIBES_SOURCE / "tests" / "g16"
    orca6 = GOODVIBES_SOURCE / "tests" / "orca6"
    selectivity = GOODVIBES_SOURCE / "goodvibes" / "examples" / "selectivity"
    input_directory = workspace / "inputs"
    input_directory.mkdir()

    def stage(source: Path) -> str:
        target = input_directory / source.name
        shutil.copy2(source, target)
        return str(target.relative_to(workspace))

    gaussian_a = stage(g16 / "01a_water_hf_freq.log")
    gaussian_b = stage(g16 / "01b_water_hf_freq_scaled.log")
    orca_water = stage(orca6 / "01a_water_hf_freq.out")
    selectivity_files = [
        stage(selectivity / "DA_exo_12_i.out"),
        stage(selectivity / "DA_exo_12_ii.out"),
        stage(selectivity / "DA_endo_12_i.out"),
        stage(selectivity / "DA_endo_12_ii.out"),
    ]
    profile = stage(TOOLBOX_ROOT / "tests" / "fixtures" / "goodvibes_water_profile.yaml")
    return [
        (
            "goodvibes_gaussian_thermochemistry",
            "derive_thermochemistry",
            request({"output_file": gaussian_a}, common_settings()),
        ),
        (
            "goodvibes_orca_thermochemistry",
            "derive_thermochemistry",
            request(
                {"output_file": orca_water},
                common_settings(),
            ),
        ),
        (
            "goodvibes_temperature_scan",
            "scan_thermochemistry_temperature",
            request(
                {
                    "output_files": [gaussian_a],
                    "temperatures_kelvin": [273.15, 298.15, 350.0],
                },
                common_settings(temperature=False),
            ),
        ),
        (
            "goodvibes_ensemble",
            "analyze_thermochemical_ensemble",
            request(
                {"output_files": [gaussian_a, gaussian_b]},
                {
                    **common_settings(),
                    "population_basis": "quasi_harmonic_gibbs",
                    "deduplicate_structures": False,
                },
            ),
        ),
        (
            "goodvibes_validation",
            "validate_thermochemistry_inputs",
            request(
                {"output_files": [gaussian_a, gaussian_b]},
                {
                    **common_settings(),
                    "duplicate_energy_cutoff_kcal_mol": 0.05,
                    "duplicate_rotational_cutoff_fraction": 0.01,
                    "duplicate_rmsd_cutoff_angstrom": None,
                },
            ),
        ),
        (
            "goodvibes_selectivity",
            "analyze_thermochemical_selectivity",
            request(
                {
                    "output_files": selectivity_files,
                    "label_groups": {
                        "exo": selectivity_files[:2],
                        "endo": selectivity_files[2:],
                    },
                },
                {
                    **common_settings(),
                    "population_basis": "quasi_harmonic_gibbs",
                    "deduplicate_structures": False,
                },
            ),
        ),
        (
            "goodvibes_reaction_profile",
            "analyze_reaction_free_energy_profile",
            request(
                {
                    "output_files": [gaussian_a, gaussian_b],
                    "profile_definition_file": profile,
                },
                {**common_settings(), "profile_ensemble_mode": "gconf"},
            ),
        ),
    ]


def main() -> int:
    records = []
    with tempfile.TemporaryDirectory(prefix="researchchem_goodvibes_smoke_") as value:
        workspace = Path(value)
        os.environ["RESEARCHCHEMBENCH_WORKSPACE"] = str(workspace)
        for case_id, action_id, action_request in cases(workspace):
            started = time.monotonic()
            result = execute_action(action_id, action_request)
            records.append(
                {
                    "case_id": case_id,
                    "action": action_id,
                    "backend": "goodvibes",
                    "status": result["status"],
                    "elapsed_seconds": round(time.monotonic() - started, 6),
                    "backend_version": result.get("backend_version"),
                    "warning_count": len(result.get("warnings") or []),
                    "artifact_count": len(result.get("output_artifacts") or []),
                    "error": result.get("error"),
                }
            )
    passed = sum(item["status"] in {"success", "partial_success"} for item in records)
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "goodvibes_version": "4.3.0",
        "summary": {
            "case_count": len(records),
            "passed": passed,
            "failed": len(records) - passed,
            "covered_actions": len({item["action"] for item in records}),
        },
        "cases": records,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload["summary"], ensure_ascii=False))
    print(OUTPUT)
    return 0 if passed == len(records) else 1


if __name__ == "__main__":
    raise SystemExit(main())
