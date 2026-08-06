#!/usr/bin/env python3
"""Run one bounded real Action for locally available backends lacking evidence."""

from __future__ import annotations

import json
import os
import shutil
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


TOOLBOX_ROOT = Path(__file__).resolve().parents[1]
ROOT = TOOLBOX_ROOT.parent
SOURCE_ROOT = TOOLBOX_ROOT / "src"
for path in (SOURCE_ROOT, ROOT):
    if str(path) not in os.sys.path:
        os.sys.path.insert(0, str(path))

from dotenv import load_dotenv

from researchchem_toolbox.service import execute_action
from researchchem_toolbox.paths import portable_report_value


STATUS_PATH = TOOLBOX_ROOT / "config" / "backend_gap_smoke_status.json"

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

SILICON_CLUSTER = {
    "atoms": [
        {"element": "Si", "position_angstrom": [0.0, 0.0, 0.0]},
        {"element": "Si", "position_angstrom": [2.35, 0.0, 0.0]},
    ],
    "cell_angstrom": [[12.0, 0.0, 0.0], [0.0, 12.0, 0.0], [0.0, 0.0, 12.0]],
    "charge": 0,
    "multiplicity": 1,
    "pbc": [False, False, False],
}

SILICON_PERIODIC = {
    "atoms": [{"element": "Si", "position_angstrom": [0.0, 0.0, 0.0]}],
    "cell_angstrom": [[5.43, 0.0, 0.0], [0.0, 5.43, 0.0], [0.0, 0.0, 5.43]],
    "charge": 0,
    "multiplicity": 1,
    "pbc": [True, True, True],
}

RECEPTOR_PDBQT = (
    "ATOM      1  C   REC A   1       0.000   0.000   0.000  1.00  0.00     0.000 C\n"
    "END\n"
)

LIGAND_PDBQT = (
    "ROOT\n"
    "ATOM      1  C   LIG A   1       1.500   0.000   0.000  1.00  0.00     0.000 C\n"
    "ENDROOT\n"
    "TORSDOF 0\n"
)

ARGON_GRO = """Argon smoke
1
    1AR      AR    1   1.500   1.500   1.500
   3.00000   3.00000   3.00000
"""

ARGON_TOP = """[ defaults ]
1 2 yes 0.5 0.5

[ atomtypes ]
Ar 39.948 0.0 A 0.3405 0.997

[ moleculetype ]
AR 1

[ atoms ]
1 Ar 1 AR AR 1 0.0 39.948

[ system ]
Argon smoke

[ molecules ]
AR 1
"""

ARGON_LAMMPS = """LAMMPS argon smoke

1 atoms
1 atom types

0.0 10.0 xlo xhi
0.0 10.0 ylo yhi
0.0 10.0 zlo zhi

Masses

1 39.948

Atoms # atomic

1 1 5.0 5.0 5.0
"""


def _message(result: dict[str, Any]) -> str | None:
    error = result.get("error")
    if isinstance(error, dict):
        return str(error.get("message") or error.get("code") or "")
    return str(error) if error else None


def main() -> int:
    load_dotenv(ROOT / "config.local.env", override=False)
    records: list[dict[str, Any]] = []

    def run(case_id: str, action: str, backend: str, request: dict[str, Any]) -> dict[str, Any]:
        started = time.monotonic()
        response = execute_action(action, request)
        records.append(
            {
                "case_id": case_id,
                "action": action,
                "backend": response.get("backend") or backend,
                "status": response.get("status"),
                "elapsed_seconds": round(time.monotonic() - started, 6),
                "error": response.get("error"),
                "warnings": response.get("warnings") or [],
            }
        )
        return response

    with tempfile.TemporaryDirectory(prefix="researchchem-backend-gap-") as temporary:
        workspace = Path(temporary)
        os.environ["RESEARCHCHEMBENCH_WORKSPACE"] = str(workspace)

        receptor = workspace / "receptor.pdbqt"
        receptor.write_text(RECEPTOR_PDBQT, encoding="utf-8")
        ligand = workspace / "ligand.pdbqt"
        ligand.write_text(LIGAND_PDBQT, encoding="utf-8")
        gro = workspace / "argon.gro"
        gro.write_text(ARGON_GRO, encoding="utf-8")
        top = workspace / "argon.top"
        top.write_text(ARGON_TOP, encoding="utf-8")
        lammps_data = workspace / "argon.data"
        lammps_data.write_text(ARGON_LAMMPS, encoding="utf-8")

        run(
            "rdkit_gasteiger_ethanol",
            "assign_partial_charges",
            "rdkit_gasteiger",
            {
                "backend_id": "rdkit_gasteiger",
                "inputs": {"structure": "CCO"},
                "method_spec": {"charge_model": "gasteiger"},
                "action_settings": {},
            },
        )
        run(
            "openbabel_ethanol_3d",
            "generate_3d_structure",
            "openbabel",
            {
                "backend_id": "openbabel",
                "inputs": {"molecule": "CCO"},
                "method_spec": {"force_field": "uff"},
                "action_settings": {"timeout_seconds": 120},
            },
        )
        run(
            "tblite_water_energy",
            "calculate_energy",
            "tblite",
            {
                "backend_id": "tblite",
                "inputs": {"structure": WATER},
                "method_spec": {"method": "gfn2"},
                "action_settings": {},
            },
        )
        run(
            "pyscf_water_energy",
            "calculate_energy",
            "pyscf",
            {
                "backend_id": "pyscf",
                "inputs": {"structure": WATER},
                "method_spec": {"method": "rhf", "basis": "sto-3g"},
                "action_settings": {"scf_convergence": 1.0e-8},
                "resource_limits": {"walltime_seconds": 300, "memory_mb": 1024, "cpu_cores": 1},
            },
        )
        run(
            "psi4_water_energy",
            "calculate_energy",
            "psi4",
            {
                "backend_id": "psi4",
                "inputs": {"structure": WATER},
                "method_spec": {"method": "hf", "basis": "sto-3g"},
                "action_settings": {},
                "resource_limits": {"walltime_seconds": 300, "memory_mb": 1024, "cpu_cores": 1},
            },
        )
        run(
            "gamess_water_energy",
            "calculate_energy",
            "gamess",
            {
                "backend_id": "gamess",
                "inputs": {"structure": WATER},
                "method_spec": {"scftyp": "RHF", "gbasis": "STO", "ngauss": 3},
                "action_settings": {"scf_convergence": 1.0e-8},
                "resource_limits": {"walltime_seconds": 300, "memory_mb": 1024, "cpu_cores": 1},
            },
        )
        gaussian = run(
            "gaussian_water_hessian",
            "calculate_hessian",
            "gaussian",
            {
                "backend_id": "gaussian",
                "inputs": {"structure": WATER},
                "method_spec": {"method": "HF", "basis": "STO-3G"},
                "action_settings": {"scf_convergence": "Tight"},
                "resource_limits": {"walltime_seconds": 600, "memory_mb": 1024, "cpu_cores": 1},
            },
        )
        if gaussian.get("status") in {"success", "partial_success"}:
            gaussian_result = gaussian.get("result") or {}
            output_file = gaussian_result.get("output_file")
            if output_file:
                run(
                    "goodvibes_gaussian_water",
                    "derive_thermochemistry",
                    "goodvibes",
                    {
                        "backend_id": "goodvibes",
                        "inputs": {
                            "energy": {
                                "energy": gaussian_result.get("energy_hartree", -74.9),
                                "unit": "hartree",
                            },
                            "frequencies": {"output_file": output_file},
                            "output_file": output_file,
                        },
                        "method_spec": {},
                        "action_settings": {"temperature_kelvin": 298.15, "frequency_scale": 1.0},
                        "resource_limits": {"walltime_seconds": 300, "memory_mb": 1024, "cpu_cores": 1},
                    },
                )

        run(
            "cp2k_silicon_energy",
            "calculate_periodic_energy",
            "cp2k",
            {
                "backend_id": "cp2k",
                "inputs": {"structure": SILICON_PERIODIC},
                "method_spec": {
                    "method": "PBE",
                    "basis_set": {"Si": "DZVP-MOLOPT-SR-GTH"},
                    "potential": {"Si": "GTH-PBE"},
                    "cutoff_ry": 100.0,
                    "k_points": [1, 1, 1],
                    "scf_algorithm": "ot",
                },
                "action_settings": {"scf_convergence": 1.0e-6, "max_scf_cycles": 100},
                "resource_limits": {"walltime_seconds": 600, "memory_mb": 2048, "cpu_cores": 1},
            },
        )
        run(
            "mace_silicon_cluster_energy",
            "calculate_energy",
            "mace",
            {
                "backend_id": "mace",
                "inputs": {"structure": SILICON_CLUSTER},
                "method_spec": {
                    "model": str((ROOT / ".model_cache/mace/macempa0mediummodel").resolve()),
                    "device": "cpu",
                    "allow_model_download": False,
                    "default_dtype": "float64",
                },
                "action_settings": {},
                "resource_limits": {"walltime_seconds": 600, "memory_mb": 4096, "cpu_cores": 2},
            },
        )
        run(
            "chgnet_silicon_cluster_energy",
            "calculate_energy",
            "chgnet",
            {
                "backend_id": "chgnet",
                "inputs": {"structure": SILICON_CLUSTER},
                "method_spec": {
                    "model": "pretrained-0.3.0",
                    "device": "cpu",
                    "allow_model_download": True,
                },
                "action_settings": {},
                "resource_limits": {"walltime_seconds": 600, "memory_mb": 4096, "cpu_cores": 2},
            },
        )
        run(
            "crest_water_conformers",
            "generate_conformer_ensemble",
            "crest",
            {
                "backend_id": "crest",
                "inputs": {"molecule": WATER},
                "method_spec": {"method": "gfn2", "charge": 0, "multiplicity": 1},
                "action_settings": {"energy_window_kcal_mol": 3.0},
                "resource_limits": {"walltime_seconds": 600, "memory_mb": 2048, "cpu_cores": 2},
            },
        )
        run(
            "vina_minimal_docking",
            "dock_ligand",
            "vina",
            {
                "backend_id": "vina",
                "inputs": {
                    "receptor": str(receptor),
                    "ligand": str(ligand),
                    "search_space": {
                        "center_angstrom": [0.0, 0.0, 0.0],
                        "size_angstrom": [10.0, 10.0, 10.0],
                    },
                },
                "method_spec": {},
                "action_settings": {
                    "exhaustiveness": 1,
                    "num_modes": 1,
                    "energy_range_kcal_mol": 3.0,
                },
                "resource_limits": {"walltime_seconds": 180, "memory_mb": 1024, "cpu_cores": 1},
            },
        )
        run(
            "gromacs_argon_minimization",
            "minimize_system_energy",
            "gromacs",
            {
                "backend_id": "gromacs",
                "inputs": {
                    "system": {
                        "coordinate_path": str(gro),
                        "gromacs_topology_path": str(top),
                    }
                },
                "method_spec": {"cutoff_scheme": "Verlet"},
                "action_settings": {
                    "force_tolerance_kj_mol_nm": 1000.0,
                    "max_iterations": 10,
                },
                "resource_limits": {"walltime_seconds": 180, "memory_mb": 1024, "cpu_cores": 1},
            },
        )
        run(
            "lammps_argon_minimization",
            "minimize_system_energy",
            "lammps",
            {
                "backend_id": "lammps",
                "inputs": {
                    "system": {
                        "lammps_data_path": str(lammps_data),
                        "pair_style": "lj/cut 8.5",
                        "pair_coefficients": ["1 1 0.238 3.405"],
                    }
                },
                "method_spec": {"units": "real", "atom_style": "atomic", "neighbor_skin": 2.0},
                "action_settings": {
                    "energy_tolerance": 1.0e-8,
                    "force_tolerance": 1.0e-8,
                    "max_iterations": 10,
                    "max_evaluations": 100,
                },
                "resource_limits": {"walltime_seconds": 180, "memory_mb": 1024, "cpu_cores": 1},
            },
        )

        namd_source = ROOT / ".software_cache/namd/3.0.2/smoke"
        namd_files = {}
        for name in ("CH_final.psf", "CH_final.pdb", "CH_cgenff.prm"):
            destination = workspace / name
            shutil.copy2(namd_source / name, destination)
            namd_files[name] = destination
        run(
            "namd_minimal_minimization",
            "minimize_system_energy",
            "namd",
            {
                "backend_id": "namd",
                "inputs": {
                    "system": {
                        "namd_psf_path": str(namd_files["CH_final.psf"]),
                        "coordinate_path": str(namd_files["CH_final.pdb"]),
                        "namd_parameter_paths": [str(namd_files["CH_cgenff.prm"])],
                    }
                },
                "method_spec": {
                    "force_field_family": "charmm",
                    "exclude": "scaled1-4",
                    "one_four_scaling": 1.0,
                    "cutoff_angstrom": 12.0,
                    "switching": True,
                    "switch_distance_angstrom": 10.0,
                    "pairlist_distance_angstrom": 14.0,
                    "pme": False,
                    "rigid_bonds": "none",
                },
                "action_settings": {"max_iterations": 2, "report_interval": 1},
                "resource_limits": {"walltime_seconds": 180, "memory_mb": 1024, "cpu_cores": 1},
            },
        )

        amber_source = ROOT / ".software_cache/amber/26/smoke/gb7_trx_serial"
        amber_topology = workspace / "amber.prmtop"
        amber_coordinates = workspace / "amber.inpcrd"
        shutil.copy2(amber_source / "prmtop", amber_topology)
        shutil.copy2(amber_source / "trxox.2.4ns.x", amber_coordinates)
        run(
            "amber_pmemd_minimization",
            "minimize_system_energy",
            "amber_pmemd",
            {
                "backend_id": "amber_pmemd",
                "inputs": {
                    "system": {
                        "amber_topology_path": str(amber_topology),
                        "amber_coordinate_path": str(amber_coordinates),
                    }
                },
                "method_spec": {
                    "boundary": "implicit",
                    "cutoff_angstrom": 999.0,
                    "constraints": "none",
                    "igb": 7,
                    "saltcon_molar": 0.0,
                },
                "action_settings": {
                    "max_iterations": 5,
                    "steepest_descent_steps": 2,
                    "gradient_tolerance_kcal_mol_angstrom": 1.0,
                    "report_interval": 1,
                },
                "resource_limits": {"walltime_seconds": 300, "memory_mb": 2048, "cpu_cores": 1},
            },
        )

        charmm_source = ROOT / ".software_cache/charmm/50b2/source/tool/pycharmm/tests/data"
        charmm_files = {}
        for name in ("water_cube.psf", "water_cube.crd", "water_ions.rtf", "water_ions.prm"):
            destination = workspace / name
            shutil.copy2(charmm_source / name, destination)
            charmm_files[name] = destination
        run(
            "charmm_water_minimization",
            "minimize_system_energy",
            "charmm",
            {
                "backend_id": "charmm",
                "inputs": {
                    "system": {
                        "charmm_topology_paths": [str(charmm_files["water_ions.rtf"])],
                        "charmm_parameter_paths": [str(charmm_files["water_ions.prm"])],
                        "charmm_psf_path": str(charmm_files["water_cube.psf"]),
                        "charmm_coordinate_path": str(charmm_files["water_cube.crd"]),
                    }
                },
                "method_spec": {
                    "force_field_family": "charmm",
                    "coordinate_format": "card",
                    "flexible_parameters": True,
                    "electrostatics": "cdie",
                    "electrostatic_switch": "fshift",
                    "dielectric": 1.0,
                    "vdw_switch": "vshift",
                    "cutoff_angstrom": 9.0,
                    "switch_on_angstrom": 7.0,
                    "pairlist_distance_angstrom": 10.0,
                    "constraints": "none",
                },
                "action_settings": {
                    "algorithm": "sd",
                    "max_iterations": 1,
                    "gradient_tolerance_kcal_mol_angstrom": 1000.0,
                    "report_interval": 1,
                },
                "resource_limits": {"walltime_seconds": 300, "memory_mb": 2048, "cpu_cores": 1},
            },
        )

    passed = sum(item["status"] in {"success", "partial_success"} for item in records)
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "schema_version": 1,
        "summary": {
            "case_count": len(records),
            "passed": passed,
            "failed": len(records) - passed,
            "all_ok": passed == len(records),
        },
        "cases": records,
    }
    payload = portable_report_value(payload)
    STATUS_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(STATUS_PATH)
    print(json.dumps(payload["summary"], ensure_ascii=False))
    for item in records:
        if item["status"] not in {"success", "partial_success"}:
            print(item["case_id"], item["status"], _message(item))
    return 0 if payload["summary"]["all_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
