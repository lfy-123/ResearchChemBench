#!/usr/bin/env python3
"""Run reproducible real calculations against every downloaded scientific resource."""

from __future__ import annotations

import argparse
import json
import os
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

from chemistry_toolbox.src.service import execute_action
from chemistry_toolbox.src.paths import portable_report_value


STATUS_PATH = TOOLBOX_ROOT / "evidence" / "status" / "scientific_resource_smoke_status.json"


SI_STRUCTURE = {
    "atoms": [{"element": "Si", "position_angstrom": [0.0, 0.0, 0.0]}],
    "cell_angstrom": [
        [5.43, 0.0, 0.0],
        [0.0, 5.43, 0.0],
        [0.0, 0.0, 5.43],
    ],
    "pbc": [True, True, True],
    "charge": 0,
    "multiplicity": 1,
}

SI2_STRUCTURE = {
    "atoms": [
        {"element": "Si", "position_angstrom": [0.0, 0.0, 0.0]},
        {"element": "Si", "position_angstrom": [1.3575, 1.3575, 1.3575]},
    ],
    "cell_angstrom": [
        [5.43, 0.0, 0.0],
        [0.0, 5.43, 0.0],
        [0.0, 0.0, 5.43],
    ],
    "pbc": [True, True, True],
    "charge": 0,
    "multiplicity": 1,
}

WATER_STRUCTURE = {
    "atoms": [
        {"element": "O", "position_angstrom": [0.0, 0.0, 0.0]},
        {"element": "H", "position_angstrom": [0.0, 0.80, 0.62]},
        {"element": "H", "position_angstrom": [0.0, -0.80, 0.62]},
    ],
    "pbc": [False, False, False],
    "charge": 0,
    "multiplicity": 1,
}


def request_cases() -> list[tuple[str, str, dict[str, Any]]]:
    common_limits = {"cpu_cores": 1}
    gamma = {"grid": [1, 1, 1], "shift": [0, 0, 0]}
    return [
        (
            "quantum_espresso_sssp_efficiency_si",
            "calculate_periodic_energy",
            {
                "backend_id": "quantum_espresso",
                "inputs": {"structure": SI_STRUCTURE},
                "method_spec": {
                    "input_dft": "PBE",
                    "pseudopotentials": {
                        "Si": "resource://qe_sssp_1_3_pbe_efficiency/Si"
                    },
                    "ecutwfc_ry": 30.0,
                    "ecutrho_ry": 240.0,
                    "k_points": gamma,
                },
                "action_settings": {"scf_convergence_ry": 1e-7},
                "resource_limits": common_limits,
            },
        ),
        (
            "quantum_espresso_sssp_precision_si",
            "calculate_periodic_energy",
            {
                "backend_id": "quantum_espresso",
                "inputs": {"structure": SI_STRUCTURE},
                "method_spec": {
                    "input_dft": "PBE",
                    "pseudopotentials": {
                        "Si": "resource://qe_sssp_1_3_pbe_precision/Si"
                    },
                    "ecutwfc_ry": 30.0,
                    "ecutrho_ry": 240.0,
                    "k_points": gamma,
                },
                "action_settings": {"scf_convergence_ry": 1e-7},
                "resource_limits": common_limits,
            },
        ),
        (
            "siesta_pseudodojo_psml_si",
            "calculate_periodic_energy",
            {
                "backend_id": "siesta",
                "inputs": {"structure": SI_STRUCTURE},
                "method_spec": {
                    "xc_functional": "GGA",
                    "xc_authors": "PBE",
                    "pseudopotentials": {
                        "Si": "resource://siesta_pseudo_dojo_nc_sr_05_pbe_standard_psml/Si"
                    },
                    "basis_size": "SZ",
                    "mesh_cutoff_ry": 80.0,
                    "k_points": gamma,
                },
                "action_settings": {},
                "resource_limits": common_limits,
            },
        ),
        (
            "abinit_pseudodojo_psp8_si",
            "calculate_periodic_energy",
            {
                "backend_id": "abinit",
                "inputs": {"structure": SI_STRUCTURE},
                "method_spec": {
                    "ixc": 11,
                    "pseudopotentials": {
                        "Si": "resource://abinit_pseudo_dojo_nc_sr_pbe_standard_psp8/Si"
                    },
                    "ecut_hartree": 15.0,
                    "k_points": gamma,
                },
                "action_settings": {"scf_convergence_hartree": 1e-8},
                "resource_limits": common_limits,
            },
        ),
        (
            "dftbplus_matsci_si",
            "calculate_periodic_energy",
            {
                "backend_id": "dftbplus",
                "inputs": {"structure": SI_STRUCTURE},
                "method_spec": {
                    "parameter_set": "resource://dftb_matsci_0_3",
                    "k_points": gamma,
                    "scc": True,
                    "max_angular_momenta": {"Si": "d"},
                },
                "action_settings": {
                    "scc_tolerance": 1e-8,
                    "max_scc_iterations": 200,
                },
                "resource_limits": common_limits,
            },
        ),
        (
            "dftbplus_3ob_dftb3_c",
            "calculate_periodic_energy",
            {
                "backend_id": "dftbplus",
                "inputs": {
                    "structure": {
                        "atoms": [
                            {"element": "C", "position_angstrom": [0.0, 0.0, 0.0]}
                        ],
                        "cell_angstrom": [
                            [10.0, 0.0, 0.0],
                            [0.0, 10.0, 0.0],
                            [0.0, 0.0, 10.0],
                        ],
                        "pbc": [True, True, True],
                    }
                },
                "method_spec": {
                    "parameter_set": "resource://dftb_3ob_3_1",
                    "k_points": gamma,
                    "scc": True,
                    "max_angular_momenta": {"C": "p"},
                    "third_order_full": True,
                    "hubbard_derivatives": {"C": -0.1492},
                    "damp_xh_exponent": 4.0,
                },
                "action_settings": {
                    "scc_tolerance": 1e-8,
                    "max_scc_iterations": 200,
                },
                "resource_limits": common_limits,
            },
        ),
        (
            "quantum_espresso_sssp_si_forces",
            "calculate_periodic_forces",
            {
                "backend_id": "quantum_espresso",
                "inputs": {"structure": SI_STRUCTURE},
                "method_spec": {
                    "input_dft": "PBE",
                    "pseudopotentials": {
                        "Si": "resource://qe_sssp_1_3_pbe_efficiency/Si"
                    },
                    "ecutwfc_ry": 30.0,
                    "ecutrho_ry": 240.0,
                    "k_points": gamma,
                },
                "action_settings": {},
                "resource_limits": common_limits,
            },
        ),
        (
            "quantum_espresso_sssp_si_stress",
            "calculate_periodic_stress",
            {
                "backend_id": "quantum_espresso",
                "inputs": {"structure": SI_STRUCTURE},
                "method_spec": {
                    "input_dft": "PBE",
                    "pseudopotentials": {
                        "Si": "resource://qe_sssp_1_3_pbe_efficiency/Si"
                    },
                    "ecutwfc_ry": 30.0,
                    "ecutrho_ry": 240.0,
                    "k_points": gamma,
                },
                "action_settings": {},
                "resource_limits": common_limits,
            },
        ),
        (
            "siesta_pseudodojo_si_forces",
            "calculate_periodic_forces",
            {
                "backend_id": "siesta",
                "inputs": {"structure": SI_STRUCTURE},
                "method_spec": {
                    "xc_functional": "GGA",
                    "xc_authors": "PBE",
                    "pseudopotentials": {
                        "Si": "resource://siesta_pseudo_dojo_nc_sr_05_pbe_standard_psml/Si"
                    },
                    "basis_size": "SZ",
                    "mesh_cutoff_ry": 80.0,
                    "k_points": gamma,
                },
                "action_settings": {},
                "resource_limits": common_limits,
            },
        ),
        (
            "dftbplus_matsci_si_forces",
            "calculate_periodic_forces",
            {
                "backend_id": "dftbplus",
                "inputs": {"structure": SI_STRUCTURE},
                "method_spec": {
                    "parameter_set": "resource://dftb_matsci_0_3",
                    "k_points": gamma,
                    "scc": True,
                    "max_angular_momenta": {"Si": "d"},
                },
                "action_settings": {
                    "scc_tolerance": 1e-8,
                    "max_scc_iterations": 200,
                },
                "resource_limits": common_limits,
            },
        ),
        (
            "abinit_pseudodojo_si_forces",
            "calculate_periodic_forces",
            {
                "backend_id": "abinit",
                "inputs": {"structure": SI_STRUCTURE},
                "method_spec": {
                    "ixc": 11,
                    "pseudopotentials": {
                        "Si": "resource://abinit_pseudo_dojo_nc_sr_pbe_standard_psp8/Si"
                    },
                    "ecut_hartree": 15.0,
                    "k_points": gamma,
                },
                "action_settings": {},
                "resource_limits": common_limits,
            },
        ),
        (
            "abinit_pseudodojo_si_stress",
            "calculate_periodic_stress",
            {
                "backend_id": "abinit",
                "inputs": {"structure": SI_STRUCTURE},
                "method_spec": {
                    "ixc": 11,
                    "pseudopotentials": {
                        "Si": "resource://abinit_pseudo_dojo_nc_sr_pbe_standard_psp8/Si"
                    },
                    "ecut_hartree": 15.0,
                    "k_points": gamma,
                },
                "action_settings": {},
                "resource_limits": common_limits,
            },
        ),
        (
            "dftbplus_matsci_si_relax",
            "relax_periodic_structure",
            {
                "backend_id": "dftbplus",
                "inputs": {"structure": SI_STRUCTURE},
                "method_spec": {
                    "parameter_set": "resource://dftb_matsci_0_3",
                    "k_points": gamma,
                    "scc": True,
                    "max_angular_momenta": {"Si": "d"},
                },
                "action_settings": {
                    "scc_tolerance": 1e-8,
                    "max_scc_iterations": 200,
                    "force_threshold_ev_per_angstrom": 10.0,
                    "max_steps": 2,
                    "relax_cell": False,
                },
                "resource_limits": common_limits,
            },
        ),
    ]


def prepare_docking_inputs(workspace: Path) -> None:
    (workspace / "receptor.pdbqt").write_text(
        "ATOM      1  C   REC A   1       0.000   0.000   0.000  1.00  0.00     0.000 C\nEND\n",
        encoding="utf-8",
    )
    (workspace / "ligand.pdbqt").write_text(
        "ROOT\n"
        "ATOM      1  C   LIG A   1       1.500   0.000   0.000  1.00  0.00     0.000 C\n"
        "ENDROOT\nTORSDOF 0\n",
        encoding="utf-8",
    )


def gnina_case() -> tuple[str, str, dict[str, Any]]:
    return (
        "gnina_1_3_3_builtin_cnn_cpu",
        "dock_ligand",
        {
            "backend_id": "gnina",
            "inputs": {
                "receptor": "receptor.pdbqt",
                "ligand": "ligand.pdbqt",
                "search_space": {
                    "center_angstrom": [0.0, 0.0, 0.0],
                    "size_angstrom": [10.0, 10.0, 10.0],
                },
            },
            "method_spec": {
                "cnn_model": "builtin_default",
                "cnn_scoring": "rescore",
            },
            "action_settings": {
                "exhaustiveness": 1,
                "num_modes": 1,
                "use_gpu": False,
                "cpu": 1,
                "seed": 20260718,
            },
            "resource_limits": {"cpu_cores": 1},
        },
    )


def orca_cases() -> list[tuple[str, str, dict[str, Any]]]:
    method = {"method": "HF", "basis": "STO-3G"}
    return [
        (
            "orca_6_1_1_openmpi418_water_energy_pal2",
            "calculate_energy",
            {
                "backend_id": "orca",
                "inputs": {"structure": WATER_STRUCTURE},
                "method_spec": method,
                "action_settings": {},
                "resource_limits": {"cpu_cores": 2},
            },
        ),
        (
            "orca_6_1_1_water_hessian",
            "calculate_hessian",
            {
                "backend_id": "orca",
                "inputs": {"structure": WATER_STRUCTURE},
                "method_spec": method,
                "action_settings": {},
                "resource_limits": {"cpu_cores": 1},
            },
        ),
        (
            "orca_6_1_1_water_geometry_optimization",
            "optimize_geometry",
            {
                "backend_id": "orca",
                "inputs": {"structure": WATER_STRUCTURE},
                "method_spec": method,
                "action_settings": {
                    "optimization_convergence": "Tight",
                    "max_steps": 50,
                },
                "resource_limits": {"cpu_cores": 1},
            },
        ),
        (
            "orca_6_1_1_water_dipole",
            "calculate_dipole_moment",
            {
                "backend_id": "orca",
                "inputs": {"structure": WATER_STRUCTURE},
                "method_spec": method,
                "action_settings": {},
                "resource_limits": {"cpu_cores": 1},
            },
        ),
    ]


def model_and_vasp_cases() -> list[tuple[str, str, dict[str, Any]]]:
    model_limits = {"cpu_cores": 1}
    mapping = {
        "device": "cpu",
        "chemical_species_mapping": "identity",
        "allow_tf32": False,
    }
    return [
        (
            "nequip_oam_s_si_periodic_forces",
            "calculate_periodic_forces",
            {
                "backend_id": "nequip",
                "inputs": {"structure": SI2_STRUCTURE},
                "method_spec": {
                    "model": "resource://nequip_oam_s_0_1",
                    **mapping,
                },
                "action_settings": {},
                "resource_limits": model_limits,
            },
        ),
        (
            "allegro_oam_l_si_periodic_energy",
            "calculate_periodic_energy",
            {
                "backend_id": "allegro",
                "inputs": {"structure": SI2_STRUCTURE},
                "method_spec": {
                    "model": "resource://allegro_oam_l_0_1",
                    **mapping,
                },
                "action_settings": {},
                "resource_limits": model_limits,
            },
        ),
        (
            "deepmd_dpa_3_3_omat24_si_periodic_stress",
            "calculate_periodic_stress",
            {
                "backend_id": "deepmd",
                "inputs": {"structure": SI2_STRUCTURE},
                "method_spec": {
                    "model": "resource://deepmd_dpa_3_3_1m",
                    "device": "cpu",
                    "model_branch": "Omat24",
                    "charge": 0,
                    "spin": 0,
                },
                "action_settings": {},
                "resource_limits": model_limits,
            },
        ),
        (
            "deepmd_dpa3_omol_large_water_energy",
            "calculate_energy",
            {
                "backend_id": "deepmd",
                "inputs": {"structure": WATER_STRUCTURE},
                "method_spec": {
                    "model": "resource://deepmd_dpa3_omol_large",
                    "device": "cpu",
                    "model_branch": "single_task",
                    "charge": 0,
                    "spin": 0,
                },
                "action_settings": {},
                "resource_limits": model_limits,
            },
        ),
        (
            "vasp_6_3_2_testsuite_si_energy",
            "calculate_periodic_energy",
            {
                "backend_id": "vasp",
                "inputs": {"structure": SI_STRUCTURE},
                "method_spec": {
                    "pseudopotentials": {
                        "Si": "resource://vasp_6_3_2_testsuite_si_potcar"
                    },
                    "encut_ev": 200.0,
                    "k_points": {"grid": [1, 1, 1], "shift": [0, 0, 0]},
                    "kpoint_scheme": "gamma",
                    "precision": "Normal",
                    "algorithm": "Normal",
                    "ismear": 0,
                    "sigma_ev": 0.05,
                    "spin_polarized": False,
                    "real_space_projection": False,
                    "xc_family": "pbe",
                },
                "action_settings": {
                    "scf_convergence_ev": 1e-5,
                    "max_scf_cycles": 80,
                },
                "resource_limits": {"cpu_cores": 1},
            },
        ),
        (
            "vasp_paw_pbe_54_si_energy",
            "calculate_periodic_energy",
            {
                "backend_id": "vasp",
                "inputs": {"structure": SI_STRUCTURE},
                "method_spec": {
                    "pseudopotentials": {
                        "Si": "resource://vasp_paw_pbe_54/Si"
                    },
                    "encut_ev": 300.0,
                    "k_points": {"grid": [1, 1, 1], "shift": [0, 0, 0]},
                    "kpoint_scheme": "gamma",
                    "precision": "Normal",
                    "algorithm": "Normal",
                    "ismear": 0,
                    "sigma_ev": 0.05,
                    "spin_polarized": False,
                    "real_space_projection": False,
                    "xc_family": "pbe",
                },
                "action_settings": {
                    "scf_convergence_ev": 1e-5,
                    "max_scf_cycles": 80,
                },
                "resource_limits": {"cpu_cores": 1},
            },
        ),
    ]


def compact_result(value: Any) -> Any:
    if not isinstance(value, dict):
        return value
    allowed = {
        "energy",
        "unit",
        "scores",
        "search_space",
        "poses_path",
        "forces",
        "stress",
        "converged",
        "structure",
        "dipole",
        "energy_hartree",
        "energy_unit",
        "optimization_convergence",
        "raw_hessian_path",
    }
    result = {key: item for key, item in value.items() if key in allowed}
    matrix = value.get("matrix")
    if isinstance(matrix, list) and matrix and isinstance(matrix[0], list):
        result["matrix_shape"] = [len(matrix), len(matrix[0])]
        result["matrix_max_abs"] = max(
            abs(float(item)) for row in matrix for item in row
        )
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=STATUS_PATH,
        help="Status JSON destination.",
    )
    args = parser.parse_args(argv)
    with tempfile.TemporaryDirectory(prefix="researchchem-resource-smoke-") as temporary:
        workspace = Path(temporary)
        os.environ["RESEARCHCHEMBENCH_WORKSPACE"] = str(workspace)
        prepare_docking_inputs(workspace)
        cases = [
            *request_cases(),
            gnina_case(),
            *orca_cases(),
            *model_and_vasp_cases(),
        ]
        results = []
        for case_id, action_id, request in cases:
            started = time.monotonic()
            response = execute_action(action_id, request)
            results.append(
                {
                    "case_id": case_id,
                    "action": action_id,
                    "backend": request["backend_id"],
                    "backend_version": response.get("backend_version"),
                    "status": response["status"],
                    "elapsed_seconds": round(time.monotonic() - started, 6),
                    "result": compact_result(response.get("result")),
                    "error": response.get("error"),
                    "warnings": response.get("warnings", []),
                    "parallel_processes": (response.get("provenance") or {}).get(
                        "parallel_processes"
                    ),
                    "resource_refs": (response.get("provenance") or {}).get(
                        "agent_selected_resource_refs", []
                    ),
                }
            )
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "schema_version": 1,
        "summary": {
            "case_count": len(results),
            "passed": sum(item["status"] == "success" for item in results),
            "failed": sum(item["status"] != "success" for item in results),
            "all_ok": all(item["status"] == "success" for item in results),
        },
        "cases": results,
    }
    payload = portable_report_value(payload)
    output = args.output.resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(output)
    print(json.dumps(payload["summary"], ensure_ascii=False))
    return 0 if payload["summary"]["all_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
