#!/usr/bin/env python3
"""Run bounded representative calls for public Actions missed by the main suite."""

from __future__ import annotations

import argparse
import json
import os
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in os.sys.path:
    os.sys.path.insert(0, str(ROOT))

from dotenv import load_dotenv

from researchchem_toolbox.service import execute_action


STATUS_PATH = ROOT / "config" / "action_gap_smoke_status.json"

WATER = {
    "atoms": [
        {"element": "O", "position_angstrom": [0.0, 0.0, 0.0]},
        {"element": "H", "position_angstrom": [0.0, 0.757, 0.586]},
        {"element": "H", "position_angstrom": [0.0, -0.757, 0.586]},
    ],
    "charge": 0,
    "multiplicity": 1,
    "pbc": [False, False, False],
}

SILICON = {
    "atoms": [
        {"element": "Si", "position_angstrom": [0.0, 0.0, 0.0]},
        {"element": "Si", "position_angstrom": [2.5, 2.5, 2.5]},
    ],
    "cell_angstrom": [[5.0, 0.0, 0.0], [0.0, 5.0, 0.0], [0.0, 0.0, 5.0]],
    "pbc": [True, True, True],
    "charge": 0,
    "multiplicity": 1,
}

TRAJECTORY_PDB = """MODEL        1
CRYST1   20.000   20.000   20.000  90.00  90.00  90.00 P 1           1
ATOM      1  O1  HOH A   1       1.000   1.000   1.000  1.00  0.00           O
ATOM      2  H1  HOH A   1       1.960   1.000   1.000  1.00  0.00           H
ATOM      3  H2  HOH A   1       0.760   1.930   1.000  1.00  0.00           H
ATOM      4  O2  HOH A   2       3.700   1.000   1.000  1.00  0.00           O
ATOM      5  H3  HOH A   2       4.660   1.000   1.000  1.00  0.00           H
ATOM      6  H4  HOH A   2       3.460   1.930   1.000  1.00  0.00           H
ENDMDL
MODEL        2
CRYST1   20.000   20.000   20.000  90.00  90.00  90.00 P 1           1
ATOM      1  O1  HOH A   1       1.100   1.000   1.000  1.00  0.00           O
ATOM      2  H1  HOH A   1       2.060   1.050   1.000  1.00  0.00           H
ATOM      3  H2  HOH A   1       0.860   1.930   1.050  1.00  0.00           H
ATOM      4  O2  HOH A   2       3.850   1.050   1.000  1.00  0.00           O
ATOM      5  H3  HOH A   2       4.810   1.050   1.000  1.00  0.00           H
ATOM      6  H4  HOH A   2       3.610   1.980   1.000  1.00  0.00           H
ENDMDL
MODEL        3
CRYST1   20.000   20.000   20.000  90.00  90.00  90.00 P 1           1
ATOM      1  O1  HOH A   1       1.250   1.000   1.000  1.00  0.00           O
ATOM      2  H1  HOH A   1       2.210   1.100   1.000  1.00  0.00           H
ATOM      3  H2  HOH A   1       1.010   1.930   1.100  1.00  0.00           H
ATOM      4  O2  HOH A   2       4.050   1.100   1.000  1.00  0.00           O
ATOM      5  H3  HOH A   2       5.010   1.100   1.000  1.00  0.00           H
ATOM      6  H4  HOH A   2       3.810   2.030   1.000  1.00  0.00           H
ENDMDL
END
"""

SINGLE_WATER_PDB = """ATOM      1  O   HOH A   1       0.000   0.000   0.000  1.00  0.00           O
ATOM      2  H1  HOH A   1       0.957   0.000   0.000  1.00  0.00           H
ATOM      3  H2  HOH A   1      -0.240   0.927   0.000  1.00  0.00           H
TER
END
"""

H2_PDB = """ATOM      1  H1  MOL A   1       0.000   0.000   0.000  1.00  0.00           H
ATOM      2  H2  MOL A   1       0.000   0.000   0.740  1.00  0.00           H
TER
END
"""

H2_XYZ = """2
frame 1
H 0.000 0.000 0.000
H 0.000 0.000 0.740
2
frame 2
H 0.000 0.000 0.000
H 0.000 0.000 0.760
"""

HCN_ISOMERIZATION_TS = {
    "atoms": [
        {"element": "C", "position_angstrom": [-0.03916665, 0.50098231, 0.07264016]},
        {"element": "H", "position_angstrom": [-0.61754364, 0.50098231, -0.93535190]},
        {"element": "N", "position_angstrom": [0.70013649, 0.50098231, -0.87617397]},
    ],
    "charge": 0,
    "multiplicity": 1,
    "pbc": [False, False, False],
}

HCN_HF_STO3G_TS = {
    "atoms": [
        {"element": "C", "position_angstrom": [0.23801823, 0.64326093, 0.0]},
        {"element": "H", "position_angstrom": [-0.96303310, 0.59539903, 0.0]},
        {"element": "N", "position_angstrom": [-0.07708005, -0.53675142, 0.0]},
    ],
    "charge": 0,
    "multiplicity": 1,
    "pbc": [False, False, False],
}

CATMAP_CO_OXIDATION_ENERGIES = """surface_name\tsite_name\tspecies_name\tformation_energy\tbulk_structure\tfrequencies\tother_parameters\treference
None\tgas\tCO2\t2.45\tNone\t[1333,2349,667,667]\t[]\tCatMAP_official_tutorial
None\tgas\tCO\t2.74\tNone\t[2170]\t[]\tCatMAP_official_tutorial
None\tgas\tO2\t5.42\tNone\t[1580]\t[]\tCatMAP_official_tutorial
Ru\t111\tO\t-0.07\tfcc\t[]\t[]\tCatMAP_official_tutorial
Ni\t111\tO\t0.35\tfcc\t[]\t[]\tCatMAP_official_tutorial
Rh\t111\tO\t0.55\tfcc\t[]\t[]\tCatMAP_official_tutorial
Cu\t111\tO\t1.07\tfcc\t[]\t[]\tCatMAP_official_tutorial
Pd\t111\tO\t1.55\tfcc\t[]\t[]\tCatMAP_official_tutorial
Pt\t111\tO\t1.62\tfcc\t[]\t[]\tCatMAP_official_tutorial
Ag\t111\tO\t2.05\tfcc\t[]\t[]\tCatMAP_official_tutorial
Au\t111\tO\t2.61\tfcc\t[]\t[]\tCatMAP_official_tutorial
Ru\t111\tCO\t1.30\tfcc\t[]\t[]\tCatMAP_official_tutorial
Rh\t111\tCO\t1.34\tfcc\t[]\t[]\tCatMAP_official_tutorial
Pd\t111\tCO\t1.55\tfcc\t[]\t[]\tCatMAP_official_tutorial
Ni\t111\tCO\t1.63\tfcc\t[]\t[]\tCatMAP_official_tutorial
Pt\t111\tCO\t1.70\tfcc\t[]\t[]\tCatMAP_official_tutorial
Cu\t111\tCO\t2.58\tfcc\t[]\t[]\tCatMAP_official_tutorial
Ag\t111\tCO\t2.99\tfcc\t[]\t[]\tCatMAP_official_tutorial
Au\t111\tCO\t3.04\tfcc\t[]\t[]\tCatMAP_official_tutorial
Ru\t111\tO-CO\t2.53\tfcc\t[]\t[]\tCatMAP_official_tutorial
Rh\t111\tO-CO\t3.10\tfcc\t[]\t[]\tCatMAP_official_tutorial
Ni\t111\tO-CO\t3.25\tfcc\t[]\t[]\tCatMAP_official_tutorial
Pt\t111\tO-CO\t4.04\tfcc\t[]\t[]\tCatMAP_official_tutorial
Cu\t111\tO-CO\t4.18\tfcc\t[]\t[]\tCatMAP_official_tutorial
Pd\t111\tO-CO\t4.20\tfcc\t[]\t[]\tCatMAP_official_tutorial
Ag\t111\tO-CO\t5.05\tfcc\t[]\t[]\tCatMAP_official_tutorial
Au\t111\tO-CO\t5.74\tfcc\t[]\t[]\tCatMAP_official_tutorial
Ag\t111\tO-O\t5.98\tfcc\t[]\t[]\tCatMAP_official_tutorial
Au\t111\tO-O\t7.22\tfcc\t[]\t[]\tCatMAP_official_tutorial
Cu\t111\tO-O\t4.74\tfcc\t[]\t[]\tCatMAP_official_tutorial
Pt\t111\tO-O\t5.35\tfcc\t[]\t[]\tCatMAP_official_tutorial
Rh\t111\tO-O\t3.79\tfcc\t[]\t[]\tCatMAP_official_tutorial
Ru\t111\tO-O\t3.34\tfcc\t[]\t[]\tCatMAP_official_tutorial
Pd\t111\tO-O\t5.34\tfcc\t[]\t[]\tCatMAP_official_tutorial
"""


def _error_text(result: dict[str, Any]) -> str | None:
    error = result.get("error")
    if isinstance(error, dict):
        return str(error.get("message") or error.get("code") or "")
    return str(error) if error else None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--include-network", action="store_true")
    args = parser.parse_args()
    load_dotenv(ROOT / "config.local.env", override=False)
    records: list[dict[str, Any]] = []

    def run(action: str, request: dict[str, Any], *, case_id: str | None = None):
        started = time.monotonic()
        response = execute_action(action, request)
        records.append(
            {
                "case_id": case_id or action,
                "action": action,
                "backend": response.get("backend"),
                "status": response.get("status"),
                "elapsed_seconds": round(time.monotonic() - started, 6),
                "error": response.get("error"),
                "warnings": response.get("warnings") or [],
            }
        )
        return response

    with tempfile.TemporaryDirectory(prefix="researchchem-action-gap-") as temporary:
        workspace = Path(temporary)
        os.environ["RESEARCHCHEMBENCH_WORKSPACE"] = str(workspace)
        water_pdb = workspace / "water.pdb"
        water_pdb.write_text(SINGLE_WATER_PDB, encoding="utf-8")
        trajectory_pdb = workspace / "trajectory.pdb"
        trajectory_pdb.write_text(TRAJECTORY_PDB, encoding="utf-8")
        h2_pdb = workspace / "h2.pdb"
        h2_pdb.write_text(H2_PDB, encoding="utf-8")
        h2_xyz = workspace / "h2.xyz"
        h2_xyz.write_text(H2_XYZ, encoding="utf-8")
        catmap_energies = workspace / "catmap_co_oxidation_energies.txt"
        catmap_energies.write_text(CATMAP_CO_OXIDATION_ENERGIES, encoding="utf-8")

        run(
            "repair_biomolecular_structure",
            {
                "backend_id": "pdbfixer",
                "inputs": {"structure": str(water_pdb)},
                "method_spec": {},
                "action_settings": {
                    "add_missing_residues": False,
                    "replace_nonstandard_residues": True,
                    "keep_water": True,
                },
            },
        )
        run(
            "assign_protonation_states",
            {
                "backend_id": "rdkit",
                "inputs": {"structure": "CCO"},
                "method_spec": {},
                "action_settings": {"ph": 7.0, "rule": "add_explicit_hydrogens"},
            },
            case_id="assign_protonation_states_rdkit",
        )
        run(
            "assign_protonation_states",
            {
                "backend_id": "pdbfixer",
                "inputs": {"structure": str(water_pdb)},
                "method_spec": {},
                "action_settings": {"ph": 7.0},
            },
            case_id="assign_protonation_states_pdbfixer",
        )
        for backend, settings in (
            (
                "spglib",
                {
                    "convention": "primitive",
                    "symmetry_tolerance_angstrom": 1.0e-5,
                    "angle_tolerance_degrees": -1.0,
                    "idealize": True,
                },
            ),
            (
                "pymatgen",
                {
                    "convention": "conventional",
                    "symmetry_tolerance_angstrom": 1.0e-5,
                    "angle_tolerance_degrees": 5.0,
                },
            ),
        ):
            run(
                "standardize_crystal_structure",
                {
                    "backend_id": backend,
                    "inputs": {"structure": SILICON},
                    "method_spec": {},
                    "action_settings": settings,
                },
                case_id=f"standardize_crystal_structure_{backend}",
            )

        hessian = {
            "matrix": [
                [0.5 if row == column else 0.0 for column in range(9)]
                for row in range(9)
            ],
            "unit": "eV/angstrom^2",
        }
        vibrations = run(
            "derive_vibrational_modes",
            {
                "inputs": {"hessian": hessian, "structure": WATER},
                "method_spec": {},
                "action_settings": {"linearity": "nonlinear"},
            },
        )
        run(
            "derive_ir_spectrum",
            {
                "inputs": {
                    "vibrations": {
                        "frequencies_cm1": [500.0, 1600.0, 3650.0],
                        "intensities_km_mol": [5.0, 70.0, 20.0],
                    }
                },
                "method_spec": {},
                "action_settings": {
                    "broadening": "gaussian",
                    "fwhm_cm1": 20.0,
                    "min_wavenumber_cm1": 0.0,
                    "max_wavenumber_cm1": 4000.0,
                    "points": 401,
                },
            },
        )
        frequency_result = (vibrations.get("result") or {}) if vibrations.get("status") == "success" else {
            "frequencies_cm1": [500.0, 1600.0, 3650.0],
        }
        frequency_result["structure"] = WATER
        run(
            "derive_thermochemistry",
            {
                "backend_id": "internal_thermochemistry",
                "inputs": {
                    "energy": {"energy": -75.0, "unit": "hartree"},
                    "frequencies": frequency_result,
                },
                "method_spec": {},
                "action_settings": {
                    "temperature_kelvin": 298.15,
                    "pressure_pa": 101325.0,
                    "geometry": "nonlinear",
                    "symmetry_number": 2,
                    "spin": 0.0,
                    "ignore_imaginary_modes": True,
                },
            },
        )
        run(
            "calculate_chemical_equilibrium",
            {
                "backend_id": "cantera",
                "inputs": {
                    "composition": "H2:2,O2:1,N2:3.76",
                    "mechanism": "gri30.yaml",
                },
                "method_spec": {},
                "action_settings": {
                    "temperature_kelvin": 1000.0,
                    "pressure_pa": 101325.0,
                    "equilibrium_mode": "TP",
                    "report_threshold": 1.0e-8,
                },
            },
        )
        run(
            "trace_intrinsic_reaction_coordinate",
            {
                "backend_id": "pysisyphus",
                "inputs": {"transition_state": HCN_ISOMERIZATION_TS},
                "method_spec": {
                    "calculator_backend": "xtb",
                    "method": "gfn2",
                    "charge": 0,
                    "multiplicity": 1,
                },
                "action_settings": {
                    "integrator": "eulerpc",
                    "step_length": 0.1,
                    "max_cycles": 5,
                    "forward": True,
                    "backward": False,
                },
                "resource_limits": {
                    "walltime_seconds": 600,
                    "memory_mb": 2048,
                    "cpu_cores": 2,
                    "gpu_count": 0,
                },
            },
            case_id="trace_intrinsic_reaction_coordinate_pysisyphus_xtb",
        )
        run(
            "trace_intrinsic_reaction_coordinate",
            {
                "backend_id": "pysisyphus",
                "inputs": {"transition_state": HCN_HF_STO3G_TS},
                "method_spec": {
                    "calculator_backend": "pyscf",
                    "method": "hf",
                    "basis": "sto-3g",
                    "charge": 0,
                    "multiplicity": 1,
                },
                "action_settings": {
                    "integrator": "eulerpc",
                    "step_length": 0.1,
                    "max_cycles": 2,
                    "forward": True,
                    "backward": False,
                },
                "resource_limits": {
                    "walltime_seconds": 600,
                    "memory_mb": 2048,
                    "cpu_cores": 2,
                    "gpu_count": 0,
                },
            },
            case_id="trace_intrinsic_reaction_coordinate_pysisyphus_pyscf",
        )
        run(
            "solve_microkinetic_model",
            {
                "backend_id": "catmap",
                "inputs": {
                    "model": {
                        "rxn_expressions": [
                            "*_s + CO_g -> CO*",
                            "2*_s + O2_g <-> O-O* + *_s -> 2O*",
                            "CO* + O* <-> O-CO* + * -> CO2_g + 2*",
                        ],
                        "surface_names": ["Pt", "Ag", "Cu", "Rh", "Pd", "Au", "Ru", "Ni"],
                        "descriptor_names": ["O_s", "CO_s"],
                        "descriptor_ranges": [[-1.0, 3.0], [-0.5, 4.0]],
                        "resolution": 2,
                        "species_definitions": {
                            "CO_g": {"pressure": 1.0},
                            "O2_g": {"pressure": 1.0 / 3.0},
                            "CO2_g": {"pressure": 0.0},
                            "s": {"site_names": ["111"], "total": 1},
                        },
                        "input_file": str(catmap_energies),
                        "gas_thermo_mode": "frozen_gas",
                        "adsorbate_thermo_mode": "frozen_adsorbate",
                        "output_variables": ["rate", "coverage", "production_rate"],
                        "scaling_constraint_dict": {
                            "O_s": ["+", 0, None],
                            "CO_s": [0, "+", None],
                            "O-CO_s": "initial_state",
                            "O-O_s": "final_state",
                        },
                        "decimal_precision": 50,
                        "tolerance": 1.0e-30,
                        "max_rootfinding_iterations": 100,
                        "max_bisections": 3,
                    }
                },
                "method_spec": {},
                "action_settings": {
                    "temperature_kelvin": 500.0,
                    "pressure_bar": 1.0,
                },
                "resource_limits": {
                    "walltime_seconds": 300,
                    "memory_mb": 2048,
                    "cpu_cores": 2,
                    "gpu_count": 0,
                },
            },
        )
        common_md = {
            "backend_id": "mdanalysis",
            "inputs": {"trajectory": str(trajectory_pdb), "topology": str(trajectory_pdb)},
            "method_spec": {},
        }
        run(
            "calculate_radial_distribution",
            {
                **common_md,
                "action_settings": {
                    "selection_a": "name O1",
                    "selection_b": "name O2",
                    "range_angstrom": [0.0, 8.0],
                    "bins": 16,
                },
            },
        )
        run(
            "calculate_mean_squared_displacement",
            {
                **common_md,
                "action_settings": {
                    "selection": "name O1 O2",
                    "dimensions": "xyz",
                    "fft": False,
                },
            },
        )
        run(
            "evaluate_collective_variables",
            {
                "backend_id": "plumed",
                "inputs": {
                    "trajectory": str(h2_xyz),
                    "topology": str(h2_pdb),
                    "collective_variables": [
                        {"label": "distance", "type": "DISTANCE", "atoms": [1, 2]}
                    ],
                },
                "method_spec": {},
                "action_settings": {
                    "stride": 1,
                    "box_angstrom": [20.0, 20.0, 20.0],
                    "timestep_ps": 1.0,
                    "trajectory_stride": 1,
                },
                "resource_limits": {"walltime_seconds": 120},
            },
        )

        displacement = run(
            "generate_displaced_supercells",
            {
                "backend_id": "phonopy",
                "inputs": {"structure": SILICON},
                "method_spec": {},
                "action_settings": {
                    "supercell_matrix": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                    "displacement_distance_angstrom": 0.01,
                },
            },
        )
        if displacement.get("status") == "success":
            displacement_result = displacement["result"]
            forces = [
                [[0.0, 0.0, 0.0] for _atom in item["structure"]["symbols"]]
                for item in displacement_result["displacements"]
            ]
            force_constants = run(
                "assemble_force_constants",
                {
                    "backend_id": "phonopy",
                    "inputs": {
                        "displacement_set": displacement_result,
                        "force_set": {"forces": forces},
                    },
                    "method_spec": {},
                    "action_settings": {},
                },
            )
            if force_constants.get("status") == "success":
                spring = [
                    [
                        [[0.1 if row == column else 0.0 for column in range(3)] for row in range(3)],
                        [[-0.1 if row == column else 0.0 for column in range(3)] for row in range(3)],
                    ],
                    [
                        [[-0.1 if row == column else 0.0 for column in range(3)] for row in range(3)],
                        [[0.1 if row == column else 0.0 for column in range(3)] for row in range(3)],
                    ],
                ]
                fc_result = {
                    "force_constants": spring,
                    "order": 2,
                    "supercell_matrix": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                    "original_structure": SILICON,
                }
                run(
                    "calculate_phonon_dispersion",
                    {
                        "backend_id": "phonopy",
                        "inputs": {"force_constants": fc_result, "structure": SILICON},
                        "method_spec": {},
                        "action_settings": {
                            "q_path": [
                                [[0.0, 0.0, 0.0], [0.25, 0.0, 0.0], [0.5, 0.0, 0.0]]
                            ],
                            "with_eigenvectors": False,
                            "labels": ["G", "X"],
                        },
                    },
                )
                run(
                    "calculate_phonon_density_of_states",
                    {
                        "backend_id": "phonopy",
                        "inputs": {"force_constants": fc_result, "structure": SILICON},
                        "method_spec": {},
                        "action_settings": {"q_mesh": [3, 3, 3]},
                    },
                )

        if args.include_network:
            network_cases = [
                (
                    "resolve_chemical_identity",
                    {
                        "inputs": {"query": {"identifier": "water", "namespace": "name"}},
                        "method_spec": {},
                        "action_settings": {"require_unique": True, "max_records": 2},
                        "resource_limits": {"walltime_seconds": 90},
                    },
                ),
                (
                    "retrieve_compound_properties",
                    {
                        "inputs": {"query": {"identifier": "962", "namespace": "cid"}},
                        "method_spec": {},
                        "action_settings": {
                            "properties": ["cid", "molecular_formula", "molecular_weight"],
                            "max_records": 1,
                        },
                        "resource_limits": {"walltime_seconds": 90},
                    },
                ),
                (
                    "retrieve_compound_structure",
                    {
                        "inputs": {"query": {"identifier": "962", "namespace": "cid"}},
                        "method_spec": {},
                        "action_settings": {
                            "record_type": "2d",
                            "hydrogen_policy": "explicit",
                            "max_records": 1,
                            "require_unique": True,
                        },
                        "resource_limits": {"walltime_seconds": 90},
                    },
                ),
                (
                    "search_similar_compounds",
                    {
                        "inputs": {"query": {"identifier": "CCO", "namespace": "smiles"}},
                        "method_spec": {},
                        "action_settings": {"threshold": 99, "max_records": 1, "timeout_seconds": 30},
                        "resource_limits": {"walltime_seconds": 90},
                    },
                ),
                (
                    "search_substructures",
                    {
                        "inputs": {"query": {"identifier": "O", "namespace": "smarts"}},
                        "method_spec": {},
                        "action_settings": {
                            "max_records": 1,
                            "match_stereo": False,
                            "match_charges": False,
                            "match_isotopes": False,
                            "timeout_seconds": 30,
                        },
                        "resource_limits": {"walltime_seconds": 90},
                    },
                ),
                (
                    "search_catalysis_records",
                    {
                        "inputs": {"query": {"reactants": "CO"}},
                        "method_spec": {},
                        "action_settings": {"max_records": 1, "timeout_seconds": 30},
                        "resource_limits": {"walltime_seconds": 90},
                    },
                ),
            ]
            for action, request in network_cases:
                run(action, request)
                time.sleep(1.0)

    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "schema_version": 1,
        "network_included": args.include_network,
        "summary": {
            "case_count": len(records),
            "passed": sum(item["status"] in {"success", "partial_success"} for item in records),
            "failed": sum(item["status"] not in {"success", "partial_success"} for item in records),
            "all_ok": all(item["status"] in {"success", "partial_success"} for item in records),
        },
        "cases": records,
    }
    STATUS_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(STATUS_PATH)
    print(json.dumps(payload["summary"], ensure_ascii=False))
    for item in records:
        if item["status"] not in {"success", "partial_success"}:
            print(item["case_id"], item["status"], _error_text(item))
    return 0 if payload["summary"]["all_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
