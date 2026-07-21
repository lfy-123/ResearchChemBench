#!/usr/bin/env python3
"""Exercise every Action/Backend pair missing from the previous audit.

The case registry is intentionally explicit: each test chooses its backend,
scientific method, resources, and bounded runtime. Results are checkpointed
after every case so an interrupted or partially failing audit can be resumed.
"""

from __future__ import annotations

import argparse
import copy
import json
import os
import shutil
import tempfile
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


TOOLBOX_ROOT = Path(__file__).resolve().parents[1]
ROOT = TOOLBOX_ROOT.parent
SOURCE_ROOT = TOOLBOX_ROOT / "src"
for path in (SOURCE_ROOT, ROOT):
    if str(path) not in os.sys.path:
        os.sys.path.insert(0, str(path))

from dotenv import load_dotenv

from researchchem_toolbox.catalog import action_specs
from researchchem_toolbox.service import execute_action


STATUS_PATH = TOOLBOX_ROOT / "config" / "action_backend_matrix_smoke_status.json"
PASS_STATUSES = {"success", "partial_success"}
GROUPS = (
    "molecular_electronic",
    "periodic",
    "dynamics",
    "analysis_reaction",
    "phonons",
)

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

SILICON_PERIODIC_2 = {
    "atoms": [
        {"element": "Si", "position_angstrom": [0.0, 0.0, 0.0]},
        {"element": "Si", "position_angstrom": [1.3575, 1.3575, 1.3575]},
    ],
    "cell_angstrom": [[5.43, 0.0, 0.0], [0.0, 5.43, 0.0], [0.0, 0.0, 5.43]],
    "charge": 0,
    "multiplicity": 1,
    "pbc": [True, True, True],
}

HCN_TS = {
    "atoms": [
        {"element": "C", "position_angstrom": [-0.03916665, 0.50098231, 0.07264016]},
        {"element": "H", "position_angstrom": [-0.61754364, 0.50098231, -0.93535190]},
        {"element": "N", "position_angstrom": [0.70013649, 0.50098231, -0.87617397]},
    ],
    "charge": 0,
    "multiplicity": 1,
    "pbc": [False, False, False],
}

WATER_PDB = """ATOM      1  O   HOH A   1       0.000   0.000   0.000  1.00  0.00           O
ATOM      2  H1  HOH A   1       0.957   0.000   0.000  1.00  0.00           H
ATOM      3  H2  HOH A   1      -0.240   0.927   0.000  1.00  0.00           H
CONECT    1    2    3
CONECT    2    1
CONECT    3    1
TER
END
"""

TRAJECTORY_PDB = """MODEL        1
CRYST1   20.000   20.000   20.000  90.00  90.00  90.00 P 1           1
ATOM      1  O1  HOH A   1       0.000   0.000   0.000  1.00  0.00           O
ATOM      2  H1  HOH A   1       0.960   0.000   0.000  1.00  0.00           H
ATOM      3  H2  HOH A   1      -0.240   0.930   0.000  1.00  0.00           H
ATOM      4  O2  HOH A   2       2.700   0.000   0.000  1.00  0.00           O
ATOM      5  H3  HOH A   2       3.660   0.000   0.000  1.00  0.00           H
ATOM      6  H4  HOH A   2       2.460   0.930   0.000  1.00  0.00           H
ENDMDL
MODEL        2
CRYST1   20.000   20.000   20.000  90.00  90.00  90.00 P 1           1
ATOM      1  O1  HOH A   1       0.000   0.000   0.000  1.00  0.00           O
ATOM      2  H1  HOH A   1       0.960   0.050   0.000  1.00  0.00           H
ATOM      3  H2  HOH A   1      -0.240   0.930   0.050  1.00  0.00           H
ATOM      4  O2  HOH A   2       2.750   0.050   0.000  1.00  0.00           O
ATOM      5  H3  HOH A   2       3.710   0.050   0.000  1.00  0.00           H
ATOM      6  H4  HOH A   2       2.510   0.980   0.000  1.00  0.00           H
ENDMDL
END
"""

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


@dataclass(frozen=True)
class Case:
    group: str
    action: str
    backend: str
    request_factory: Callable[["Context"], dict[str, Any]]

    @property
    def case_id(self) -> str:
        return f"{self.action}__{self.backend}"


@dataclass
class Context:
    workspace: Path
    cache: dict[str, Any] = field(default_factory=dict)

    def file(self, name: str, content: str) -> Path:
        key = f"file:{name}"
        if key not in self.cache:
            path = self.workspace / name
            path.write_text(content, encoding="utf-8")
            self.cache[key] = path
        return self.cache[key]

    def copied(self, key: str, source: Path, name: str | None = None) -> Path:
        cache_key = f"copy:{key}"
        if cache_key not in self.cache:
            destination = self.workspace / (name or source.name)
            shutil.copy2(source, destination)
            self.cache[cache_key] = destination
        return self.cache[cache_key]


def static(request: dict[str, Any]) -> Callable[[Context], dict[str, Any]]:
    def factory(_context: Context) -> dict[str, Any]:
        return copy.deepcopy(request)

    return factory


def request(
    backend: str,
    structure: dict[str, Any],
    method: dict[str, Any],
    settings: dict[str, Any],
    *,
    limits: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "backend_id": backend,
        "inputs": {"structure": structure},
        "method_spec": method,
        "action_settings": settings,
        "resource_limits": limits or {"walltime_seconds": 300, "memory_mb": 2048, "cpu_cores": 1},
    }


def molecular_cases() -> list[Case]:
    cases: list[Case] = []

    def add(action: str, backend: str, value: dict[str, Any]) -> None:
        cases.append(Case("molecular_electronic", action, backend, static(value)))

    psi = {"method": "hf", "basis": "sto-3g"}
    pyscf = {"method": "rhf", "basis": "sto-3g"}
    tblite = {"method": "gfn2"}
    gaussian = {"method": "HF", "basis": "STO-3G"}
    gamess = {"scftyp": "RHF", "gbasis": "STO", "ngauss": 3}
    quantum_limits = {"walltime_seconds": 600, "memory_mb": 2048, "cpu_cores": 1}

    add("calculate_atomic_charges", "psi4", request("psi4", WATER, psi, {}))
    add("calculate_atomic_charges", "pyscf", request("pyscf", WATER, pyscf, {"scf_convergence": 1e-9}))
    add("calculate_dipole_moment", "gamess", request("gamess", WATER, gamess, {"scf_convergence": 1e-8}, limits=quantum_limits))
    add("calculate_dipole_moment", "gaussian", request("gaussian", WATER, gaussian, {"scf_convergence": "Tight"}, limits=quantum_limits))
    add("calculate_dipole_moment", "psi4", request("psi4", WATER, psi, {}))
    add("calculate_dipole_moment", "pyscf", request("pyscf", WATER, pyscf, {"scf_convergence": 1e-9}))
    add("calculate_dipole_moment", "tblite", request("tblite", WATER, tblite, {}))
    add("calculate_energy", "gaussian", request("gaussian", WATER, gaussian, {"scf_convergence": "Tight"}, limits=quantum_limits))

    add("calculate_forces", "ase_emt", request("ase_emt", WATER, {}, {}))
    add(
        "calculate_forces",
        "chgnet",
        request("chgnet", SILICON_CLUSTER, {"model": "pretrained-0.3.0", "device": "cpu", "allow_model_download": True}, {}),
    )
    deepmd_water = {
        "model": "resource://deepmd_dpa3_omol_large",
        "device": "cpu",
        "model_branch": "single_task",
        "charge": 0,
        "spin": 0,
    }
    add("calculate_forces", "deepmd", request("deepmd", WATER, deepmd_water, {}, limits={"walltime_seconds": 600, "memory_mb": 8192, "cpu_cores": 1}))
    mace = {
        "model": str((ROOT / ".model_cache/mace/macempa0mediummodel").resolve()),
        "device": "cpu",
        "allow_model_download": False,
        "default_dtype": "float64",
    }
    add("calculate_forces", "mace", request("mace", SILICON_CLUSTER, mace, {}, limits={"walltime_seconds": 600, "memory_mb": 8192, "cpu_cores": 1}))
    add("calculate_forces", "tblite", request("tblite", WATER, tblite, {}))

    add("calculate_hessian", "ase_emt", request("ase_emt", WATER, {}, {"displacement_angstrom": 0.01}))
    add(
        "calculate_hessian",
        "chgnet",
        request(
            "chgnet",
            SILICON_CLUSTER,
            {"model": "pretrained-0.3.0", "device": "cpu", "allow_model_download": True},
            {"displacement_angstrom": 0.01},
            limits={"walltime_seconds": 600, "memory_mb": 8192, "cpu_cores": 1},
        ),
    )
    add(
        "calculate_hessian",
        "deepmd",
        request(
            "deepmd",
            WATER,
            deepmd_water,
            {"displacement_angstrom": 0.01},
            limits={"walltime_seconds": 600, "memory_mb": 8192, "cpu_cores": 1},
        ),
    )
    add(
        "calculate_hessian",
        "mace",
        request(
            "mace",
            WATER,
            mace,
            {"displacement_angstrom": 0.01},
            limits={"walltime_seconds": 600, "memory_mb": 8192, "cpu_cores": 1},
        ),
    )
    add("calculate_hessian", "psi4", request("psi4", WATER, psi, {}, limits=quantum_limits))
    add("calculate_hessian", "tblite", request("tblite", WATER, tblite, {"displacement_angstrom": 0.01}))
    add("calculate_hessian", "xtb", request("xtb", WATER, {"method": "gfn2"}, {}, limits=quantum_limits))
    add("calculate_orbitals", "psi4", request("psi4", WATER, psi, {}, limits=quantum_limits))
    add("calculate_orbitals", "pyscf", request("pyscf", WATER, pyscf, {"scf_convergence": 1e-9, "include_coefficients": False}))

    add("optimize_geometry", "ase_emt", request("ase_emt", WATER, {}, {"fmax_ev_per_angstrom": 10.0, "optimizer": "bfgs", "max_steps": 2}))
    add(
        "optimize_geometry",
        "chgnet",
        request("chgnet", SILICON_CLUSTER, {"model": "pretrained-0.3.0", "device": "cpu", "allow_model_download": True}, {"fmax_ev_per_angstrom": 10.0, "optimizer": "bfgs", "max_steps": 2}),
    )
    add("optimize_geometry", "deepmd", request("deepmd", WATER, deepmd_water, {"fmax_ev_per_angstrom": 100.0, "optimizer": "bfgs", "max_steps": 2}, limits={"walltime_seconds": 600, "memory_mb": 8192, "cpu_cores": 1}))
    add("optimize_geometry", "gamess", request("gamess", WATER, gamess, {"scf_convergence": 1e-8, "gradient_tolerance_hartree_per_bohr": 0.1, "max_steps": 10}, limits=quantum_limits))
    add("optimize_geometry", "gaussian", request("gaussian", WATER, gaussian, {"scf_convergence": "Tight", "optimization_convergence": "Loose", "max_steps": 20}, limits=quantum_limits))
    add("optimize_geometry", "mace", request("mace", SILICON_CLUSTER, mace, {"fmax_ev_per_angstrom": 10.0, "optimizer": "bfgs", "max_steps": 2}, limits={"walltime_seconds": 600, "memory_mb": 8192, "cpu_cores": 1}))
    add("optimize_geometry", "tblite", request("tblite", WATER, tblite, {"fmax_ev_per_angstrom": 1.0, "optimizer": "bfgs", "max_steps": 20}))
    add("optimize_geometry", "xtb", request("xtb", WATER, {"method": "gfn2"}, {"optimization_level": "loose"}, limits=quantum_limits))
    return cases


def _periodic_methods() -> dict[str, dict[str, Any]]:
    gamma = {"grid": [1, 1, 1], "shift": [0, 0, 0]}
    mapping = {"device": "cpu", "chemical_species_mapping": "identity", "allow_tf32": False}
    return {
        "cp2k": {
            "method": "PBE",
            "basis_set": {"Si": "DZVP-MOLOPT-SR-GTH"},
            "potential": {"Si": "GTH-PBE"},
            "cutoff_ry": 100.0,
            "k_points": [1, 1, 1],
            "scf_algorithm": "ot",
        },
        "vasp": {
            "pseudopotentials": {"Si": "resource://vasp_6_3_2_testsuite_si_potcar"},
            "encut_ev": 200.0,
            "k_points": gamma,
            "kpoint_scheme": "gamma",
            "precision": "Normal",
            "algorithm": "Normal",
            "ismear": 0,
            "sigma_ev": 0.05,
            "spin_polarized": False,
            "real_space_projection": False,
            "xc_family": "pbe",
        },
        "abinit": {
            "ixc": 11,
            "pseudopotentials": {"Si": "resource://abinit_pseudo_dojo_nc_sr_pbe_standard_psp8/Si"},
            "ecut_hartree": 15.0,
            "k_points": gamma,
        },
        "quantum_espresso": {
            "input_dft": "PBE",
            "pseudopotentials": {"Si": "resource://qe_sssp_1_3_pbe_efficiency/Si"},
            "ecutwfc_ry": 30.0,
            "ecutrho_ry": 240.0,
            "k_points": gamma,
        },
        "siesta": {
            "xc_functional": "GGA",
            "xc_authors": "PBE",
            "pseudopotentials": {"Si": "resource://siesta_pseudo_dojo_nc_sr_05_pbe_standard_psml/Si"},
            "basis_size": "SZ",
            "mesh_cutoff_ry": 80.0,
            "k_points": gamma,
        },
        "deepmd": {
            "model": "resource://deepmd_dpa_3_3_1m",
            "device": "cpu",
            "model_branch": "Omat24",
            "charge": 0,
            "spin": 0,
        },
        "nequip": {"model": "resource://nequip_oam_s_0_1", **mapping},
        "allegro": {"model": "resource://allegro_oam_l_0_1", **mapping},
    }


def periodic_cases() -> list[Case]:
    methods = _periodic_methods()
    limits = {"walltime_seconds": 600, "memory_mb": 8192, "cpu_cores": 1}
    cases: list[Case] = []

    def add(action: str, backend: str, structure: dict[str, Any], settings: dict[str, Any]) -> None:
        cases.append(Case("periodic", action, backend, static(request(backend, structure, methods[backend], settings, limits=limits))))

    add("calculate_periodic_energy", "deepmd", SILICON_PERIODIC_2, {})
    add("calculate_periodic_energy", "nequip", SILICON_PERIODIC_2, {})
    add("calculate_periodic_forces", "allegro", SILICON_PERIODIC_2, {})
    add("calculate_periodic_forces", "cp2k", SILICON_PERIODIC, {"scf_convergence": 1e-6, "max_scf_cycles": 100})
    add("calculate_periodic_forces", "deepmd", SILICON_PERIODIC_2, {})
    add("calculate_periodic_forces", "vasp", SILICON_PERIODIC, {"scf_convergence_ev": 1e-5, "max_scf_cycles": 80})
    add("calculate_periodic_stress", "allegro", SILICON_PERIODIC_2, {})
    add("calculate_periodic_stress", "cp2k", SILICON_PERIODIC, {"scf_convergence": 1e-6, "max_scf_cycles": 100})
    add("calculate_periodic_stress", "nequip", SILICON_PERIODIC_2, {})
    add("calculate_periodic_stress", "vasp", SILICON_PERIODIC, {"scf_convergence_ev": 1e-5, "max_scf_cycles": 80})

    relax = {"force_threshold_ev_per_angstrom": 100.0, "max_steps": 2, "relax_cell": False}
    add("relax_periodic_structure", "abinit", SILICON_PERIODIC, {**relax, "scf_convergence_hartree": 1e-8})
    add("relax_periodic_structure", "allegro", SILICON_PERIODIC_2, {**relax, "optimizer": "bfgs"})
    add("relax_periodic_structure", "cp2k", SILICON_PERIODIC, {**relax, "scf_convergence": 1e-6, "max_scf_cycles": 100})
    add("relax_periodic_structure", "deepmd", SILICON_PERIODIC_2, {**relax, "optimizer": "bfgs"})
    add("relax_periodic_structure", "nequip", SILICON_PERIODIC_2, {**relax, "optimizer": "bfgs"})
    add("relax_periodic_structure", "quantum_espresso", SILICON_PERIODIC, {**relax, "scf_convergence_ry": 1e-7})
    add("relax_periodic_structure", "siesta", SILICON_PERIODIC, relax)
    add("relax_periodic_structure", "vasp", SILICON_PERIODIC, {**relax, "scf_convergence_ev": 1e-5, "max_scf_cycles": 80})
    return cases


def _openmm_system(context: Context) -> dict[str, Any]:
    if "openmm_system" in context.cache:
        return context.cache["openmm_system"]
    pdb_path = context.file("water.pdb", WATER_PDB)
    response = execute_action(
        "assign_force_field_parameters",
        {
            "backend_id": "openmm_builder",
            "inputs": {"structure": str(pdb_path)},
            "method_spec": {"force_field": ["tip3p.xml"]},
            "action_settings": {},
        },
    )
    if response.get("status") not in PASS_STATUSES:
        raise RuntimeError(f"OpenMM parameterization prerequisite failed: {response.get('error')}")
    context.cache["openmm_system"] = response["result"]
    return response["result"]


def _licensed_md_files(context: Context) -> dict[str, Path]:
    if "licensed_md_files" in context.cache:
        return context.cache["licensed_md_files"]
    files: dict[str, Path] = {
        "argon_gro": context.file("argon.gro", ARGON_GRO),
        "argon_top": context.file("argon.top", ARGON_TOP),
        "argon_data": context.file("argon.data", ARGON_LAMMPS),
    }
    namd_source = ROOT / ".software_cache/namd/3.0.2/smoke"
    for name in ("CH_final.psf", "CH_final.pdb", "CH_cgenff.prm"):
        files[name] = context.copied(f"namd:{name}", namd_source / name, name)
    amber_source = ROOT / ".software_cache/amber/26/smoke/gb7_trx_serial"
    files["amber_prmtop"] = context.copied("amber:prmtop", amber_source / "prmtop", "amber.prmtop")
    files["amber_inpcrd"] = context.copied("amber:inpcrd", amber_source / "trxox.2.4ns.x", "amber.inpcrd")
    charmm_source = ROOT / ".software_cache/charmm/50b2/source/tool/pycharmm/tests/data"
    for name in ("water_cube.psf", "water_cube.crd", "water_ions.rtf", "water_ions.prm"):
        files[name] = context.copied(f"charmm:{name}", charmm_source / name, name)
    context.cache["licensed_md_files"] = files
    return files


def dynamics_cases() -> list[Case]:
    cases: list[Case] = []

    def openmm_minimize(context: Context) -> dict[str, Any]:
        return {
            "backend_id": "openmm",
            "inputs": {"system": _openmm_system(context)},
            "method_spec": {"platform": "Reference", "platform_properties": {}},
            "action_settings": {"force_tolerance_kj_mol_nm": 1000.0, "max_iterations": 10},
            "resource_limits": {"walltime_seconds": 300, "memory_mb": 2048, "cpu_cores": 1},
        }

    def openmm_dynamics(context: Context) -> dict[str, Any]:
        return {
            "backend_id": "openmm",
            "inputs": {"system": _openmm_system(context)},
            "method_spec": {"platform": "Reference", "platform_properties": {}},
            "action_settings": {
                "ensemble": "NVT",
                "temperature_kelvin": 300.0,
                "timestep_fs": 0.5,
                "steps": 10,
                "report_interval": 2,
                "friction_per_ps": 1.0,
                "initialize_velocities": True,
                "random_seed": 20260721,
            },
            "resource_limits": {"walltime_seconds": 300, "memory_mb": 2048, "cpu_cores": 1},
        }

    def openmm_solvate(context: Context) -> dict[str, Any]:
        return {
            "backend_id": "openmm_builder",
            "inputs": {"system": _openmm_system(context)},
            "method_spec": {"force_field": ["tip3p.xml"]},
            "action_settings": {
                "box_shape": "cubic",
                "padding_angstrom": 3.0,
                "solvent_model": "tip3p",
                "ionic_strength_molar": 0.0,
                "positive_ion": "Na+",
                "negative_ion": "Cl-",
            },
            "resource_limits": {"walltime_seconds": 300, "memory_mb": 2048, "cpu_cores": 1},
        }

    def amber(context: Context) -> dict[str, Any]:
        files = _licensed_md_files(context)
        return {
            "backend_id": "amber_pmemd",
            "inputs": {"system": {"amber_topology_path": str(files["amber_prmtop"]), "amber_coordinate_path": str(files["amber_inpcrd"])}},
            "method_spec": {"boundary": "implicit", "cutoff_angstrom": 999.0, "constraints": "none", "igb": 7, "saltcon_molar": 0.0},
            "action_settings": {"ensemble": "NVE", "temperature_kelvin": 300.0, "timestep_fs": 0.5, "steps": 2, "report_interval": 1, "random_seed": 11, "restart": False},
            "resource_limits": {"walltime_seconds": 300, "memory_mb": 2048, "cpu_cores": 1},
        }

    def charmm(context: Context) -> dict[str, Any]:
        files = _licensed_md_files(context)
        return {
            "backend_id": "charmm",
            "inputs": {"system": {
                "charmm_topology_paths": [str(files["water_ions.rtf"])],
                "charmm_parameter_paths": [str(files["water_ions.prm"])],
                "charmm_psf_path": str(files["water_cube.psf"]),
                "charmm_coordinate_path": str(files["water_cube.crd"]),
            }},
            "method_spec": {
                "force_field_family": "charmm", "coordinate_format": "card", "flexible_parameters": True,
                "electrostatics": "cdie", "electrostatic_switch": "fshift", "dielectric": 1.0,
                "vdw_switch": "vshift", "cutoff_angstrom": 9.0, "switch_on_angstrom": 7.0,
                "pairlist_distance_angstrom": 10.0, "constraints": "none", "nonbond_update_interval": 1,
            },
            "action_settings": {"ensemble": "NVE", "temperature_kelvin": 300.0, "timestep_fs": 0.5, "steps": 2, "report_interval": 1, "random_seed": 13, "restart": False},
            "resource_limits": {"walltime_seconds": 300, "memory_mb": 2048, "cpu_cores": 1},
        }

    def gromacs(context: Context) -> dict[str, Any]:
        files = _licensed_md_files(context)
        return {
            "backend_id": "gromacs",
            "inputs": {"system": {"coordinate_path": str(files["argon_gro"]), "gromacs_topology_path": str(files["argon_top"])}},
            "method_spec": {"cutoff_scheme": "Verlet"},
            "action_settings": {
                "ensemble": "NVE", "temperature_kelvin": 300.0, "timestep_fs": 1.0,
                "steps": 2, "report_interval": 1, "generate_velocities": True,
                "random_seed": 13,
            },
            "resource_limits": {"walltime_seconds": 300, "memory_mb": 2048, "cpu_cores": 1},
        }

    def lammps(context: Context) -> dict[str, Any]:
        files = _licensed_md_files(context)
        return {
            "backend_id": "lammps",
            "inputs": {"system": {"lammps_data_path": str(files["argon_data"]), "pair_style": "lj/cut 8.5", "pair_coefficients": ["1 1 0.238 3.405"]}},
            "method_spec": {"units": "real", "atom_style": "atomic", "neighbor_skin": 2.0},
            "action_settings": {"ensemble": "NVE", "temperature_kelvin": 300.0, "timestep_fs": 1.0, "steps": 2, "report_interval": 1},
            "resource_limits": {"walltime_seconds": 300, "memory_mb": 2048, "cpu_cores": 1},
        }

    def namd(context: Context) -> dict[str, Any]:
        files = _licensed_md_files(context)
        return {
            "backend_id": "namd",
            "inputs": {"system": {
                "namd_psf_path": str(files["CH_final.psf"]),
                "coordinate_path": str(files["CH_final.pdb"]),
                "namd_parameter_paths": [str(files["CH_cgenff.prm"])],
            }},
            "method_spec": {
                "force_field_family": "charmm", "exclude": "scaled1-4", "one_four_scaling": 1.0,
                "cutoff_angstrom": 12.0, "switching": True, "switch_distance_angstrom": 10.0,
                "pairlist_distance_angstrom": 14.0, "pme": False, "rigid_bonds": "none",
            },
            "action_settings": {"ensemble": "NVE", "temperature_kelvin": 300.0, "timestep_fs": 0.5, "steps": 2, "report_interval": 1, "random_seed": 17},
            "resource_limits": {"walltime_seconds": 300, "memory_mb": 2048, "cpu_cores": 1},
        }

    cases.extend(
        [
            Case("dynamics", "minimize_system_energy", "openmm", openmm_minimize),
            Case("dynamics", "propagate_dynamics", "amber_pmemd", amber),
            Case("dynamics", "propagate_dynamics", "charmm", charmm),
            Case("dynamics", "propagate_dynamics", "gromacs", gromacs),
            Case("dynamics", "propagate_dynamics", "lammps", lammps),
            Case("dynamics", "propagate_dynamics", "namd", namd),
            Case("dynamics", "propagate_dynamics", "openmm", openmm_dynamics),
            Case("dynamics", "solvate_molecular_system", "openmm_builder", openmm_solvate),
        ]
    )
    return cases


def analysis_reaction_cases() -> list[Case]:
    cases: list[Case] = []

    def trajectory(action: str, settings: dict[str, Any], extra_inputs: dict[str, Any] | None = None) -> Case:
        def factory(context: Context) -> dict[str, Any]:
            path = context.file("trajectory.pdb", TRAJECTORY_PDB)
            return {
                "backend_id": "mdanalysis",
                "inputs": {"trajectory": str(path), "topology": str(path), **(extra_inputs or {})},
                "method_spec": {},
                "action_settings": settings,
                "resource_limits": {"walltime_seconds": 300, "memory_mb": 2048, "cpu_cores": 1},
            }

        return Case("analysis_reaction", action, "mdanalysis", factory)

    cases.append(trajectory("calculate_dihedral_distribution", {"periodic": False}, {"atom_quartets": [[0, 1, 3, 4]]}))
    cases.append(trajectory("calculate_radius_of_gyration", {"selection": "all"}))
    cases.append(trajectory("calculate_trajectory_rmsd", {"selection": "all"}))
    cases.append(
        Case(
            "analysis_reaction",
            "integrate_reaction_network",
            "cantera",
            static(
                {
                    "backend_id": "cantera",
                    "inputs": {
                        "network": {"mechanism": "h2o2.yaml"},
                        "initial_state": {"temperature_kelvin": 1000.0, "pressure_pa": 101325.0, "composition": "H2:2,O2:1,AR:7"},
                    },
                    "method_spec": {},
                    "action_settings": {"time_end_seconds": 1e-6, "num_points": 3},
                    "resource_limits": {"walltime_seconds": 300, "memory_mb": 2048, "cpu_cores": 1},
                }
            ),
        )
    )
    cases.append(
        Case(
            "analysis_reaction",
            "locate_transition_state",
            "pysisyphus",
            static(
                {
                    "backend_id": "pysisyphus",
                    "inputs": {"initial_guess": HCN_TS},
                    "method_spec": {"calculator_backend": "xtb", "method": "gfn2", "charge": 0, "multiplicity": 1},
                    "action_settings": {"optimizer": "rsirfo", "convergence": "gau", "max_cycles": 10},
                    "resource_limits": {"walltime_seconds": 600, "memory_mb": 2048, "cpu_cores": 1},
                }
            ),
        )
    )
    return cases


def _synthetic_force_constants() -> dict[str, Any]:
    spring = [[[0.1 if row == column else 0.0 for column in range(3)] for row in range(3)]]
    positive = spring[0]
    negative = [[-value for value in row] for row in positive]
    return {
        "force_constants": [[positive, negative], [negative, positive]],
        "order": 2,
        "supercell_matrix": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
        "original_structure": SILICON_PERIODIC_2,
    }


def _phono3py_displacement(context: Context) -> dict[str, Any]:
    if "phono3py_displacement" in context.cache:
        return context.cache["phono3py_displacement"]
    response = execute_action(
        "generate_displaced_supercells",
        {
            "backend_id": "phono3py",
            "inputs": {"structure": SILICON_PERIODIC_2},
            "method_spec": {},
            "action_settings": {
                "supercell_matrix": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                "displacement_distance_angstrom": 0.01,
                "order": 2,
            },
        },
    )
    if response.get("status") not in PASS_STATUSES:
        raise RuntimeError(f"Phono3py displacement prerequisite failed: {response.get('error')}")
    context.cache["phono3py_displacement"] = response["result"]
    return response["result"]


def phonon_cases() -> list[Case]:
    def generate(_context: Context) -> dict[str, Any]:
        return {
            "backend_id": "phono3py",
            "inputs": {"structure": SILICON_PERIODIC_2},
            "method_spec": {},
            "action_settings": {
                "supercell_matrix": [[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                "displacement_distance_angstrom": 0.01,
                "order": 2,
            },
        }

    def assemble(context: Context) -> dict[str, Any]:
        displacement = _phono3py_displacement(context)
        forces = [
            [[0.0, 0.0, 0.0] for _symbol in item["structure"]["symbols"]]
            for item in displacement["displacements"]
        ]
        return {
            "backend_id": "phono3py",
            "inputs": {"displacement_set": displacement, "force_set": {"forces": forces}},
            "method_spec": {},
            "action_settings": {},
        }

    force_constants = _synthetic_force_constants()
    return [
        Case("phonons", "assemble_force_constants", "phono3py", assemble),
        Case(
            "phonons",
            "calculate_phonon_density_of_states",
            "phono3py",
            static({"backend_id": "phono3py", "inputs": {"force_constants": force_constants, "structure": SILICON_PERIODIC_2}, "method_spec": {}, "action_settings": {"q_mesh": [3, 3, 3]}}),
        ),
        Case(
            "phonons",
            "calculate_phonon_dispersion",
            "phono3py",
            static({"backend_id": "phono3py", "inputs": {"force_constants": force_constants, "structure": SILICON_PERIODIC_2}, "method_spec": {}, "action_settings": {"q_path": [[[0.0, 0.0, 0.0], [0.25, 0.0, 0.0], [0.5, 0.0, 0.0]]], "with_eigenvectors": False, "labels": ["G", "X"]}}),
        ),
        Case("phonons", "generate_displaced_supercells", "phono3py", generate),
    ]


def all_cases() -> list[Case]:
    cases = [
        *molecular_cases(),
        *periodic_cases(),
        *dynamics_cases(),
        *analysis_reaction_cases(),
        *phonon_cases(),
    ]
    pairs = [(case.action, case.backend) for case in cases]
    if len(cases) != 65 or len(set(pairs)) != 65:
        raise RuntimeError(
            f"Action/Backend gap registry must contain 65 unique pairs, found {len(cases)}/{len(set(pairs))}"
        )
    catalog = action_specs()
    invalid = [
        pair
        for pair in pairs
        if pair[0] not in catalog or pair[1] not in catalog[pair[0]].backend_ids
    ]
    if invalid:
        raise RuntimeError(f"Gap registry contains pairs absent from the Catalog: {invalid}")
    return cases


def _request_summary(value: dict[str, Any]) -> dict[str, Any]:
    inputs = value.get("inputs") or {}
    return {
        "input_fields": sorted(inputs),
        "method_spec": value.get("method_spec") or {},
        "action_settings": value.get("action_settings") or {},
        "resource_limits": value.get("resource_limits") or {},
    }


def _result_summary(value: Any) -> Any:
    if not isinstance(value, dict):
        return value
    summary: dict[str, Any] = {"keys": sorted(value)}
    for key in (
        "energy",
        "unit",
        "converged",
        "minimized",
        "ensemble",
        "steps",
        "duration_ps",
        "atom_count",
        "particle_count",
        "solvated",
        "order",
    ):
        if key in value and isinstance(value[key], (str, int, float, bool, type(None))):
            summary[key] = value[key]
    for key in ("forces", "matrix", "stress", "charges", "dipole", "displacements"):
        item = value.get(key)
        if isinstance(item, list):
            shape = [len(item)]
            cursor = item
            while cursor and isinstance(cursor[0], list):
                cursor = cursor[0]
                shape.append(len(cursor))
            summary[f"{key}_shape"] = shape
    return summary


def _load_existing(path: Path) -> dict[tuple[str, str], dict[str, Any]]:
    if not path.is_file():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return {
        (str(item["action"]), str(item["backend"])): item
        for item in payload.get("cases") or []
    }


def _write_status(
    path: Path,
    cases: list[Case],
    records: dict[tuple[str, str], dict[str, Any]],
) -> dict[str, Any]:
    ordered = sorted(
        records.values(), key=lambda item: (GROUPS.index(item["group"]), item["action"], item["backend"])
    )
    expected = {(case.action, case.backend) for case in cases}
    observed = set(records) & expected
    passed = {pair for pair in observed if records[pair].get("status") in PASS_STATUSES}
    failed = observed - passed
    missing = expected - observed
    payload = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "schema_version": 1,
        "purpose": (
            "Complete the original 62 Action/Backend gaps plus three explicitly exposed "
            "finite-difference Hessian backends."
        ),
        "summary": {
            "registered_gap_pair_count": len(expected),
            "observed_pair_count": len(observed),
            "passed_pair_count": len(passed),
            "failed_pair_count": len(failed),
            "missing_pair_count": len(missing),
            "all_observed": not missing,
            "all_ok": not missing and not failed,
        },
        "missing_pairs": [list(pair) for pair in sorted(missing)],
        "failed_pairs": [list(pair) for pair in sorted(failed)],
        "cases": ordered,
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--group", action="append", choices=GROUPS, help="Run only one group; repeatable.")
    parser.add_argument("--case", action="append", default=[], help="Run only exact <action>__<backend> case ids.")
    parser.add_argument("--output", type=Path, default=STATUS_PATH)
    parser.add_argument("--fresh", action="store_true", help="Discard existing checkpoint records before running.")
    parser.add_argument("--resume", action="store_true", help="Skip selected pairs already recorded as success/partial_success.")
    parser.add_argument("--list", action="store_true", help="List the 65 registered cases without running them.")
    args = parser.parse_args()

    load_dotenv(ROOT / "config.local.env", override=False)
    cases = all_cases()
    if args.list:
        for case in cases:
            print(f"{case.group}\t{case.action}\t{case.backend}\t{case.case_id}")
        return 0

    selected_groups = set(args.group or GROUPS)
    selected_ids = set(args.case)
    selected = [
        case
        for case in cases
        if case.group in selected_groups and (not selected_ids or case.case_id in selected_ids)
    ]
    unknown_ids = selected_ids - {case.case_id for case in cases}
    if unknown_ids:
        raise SystemExit(f"Unknown case ids: {sorted(unknown_ids)}")
    records = {} if args.fresh else _load_existing(args.output)

    with tempfile.TemporaryDirectory(prefix="researchchem-action-backend-matrix-") as temporary:
        context = Context(Path(temporary))
        os.environ["RESEARCHCHEMBENCH_WORKSPACE"] = str(context.workspace)
        for index, case in enumerate(selected, start=1):
            pair = (case.action, case.backend)
            existing = records.get(pair)
            if args.resume and existing and existing.get("status") in PASS_STATUSES:
                print(f"[{index}/{len(selected)}] SKIP {case.case_id}", flush=True)
                continue
            print(f"[{index}/{len(selected)}] RUN  {case.case_id}", flush=True)
            started = time.monotonic()
            request_value: dict[str, Any] | None = None
            try:
                request_value = case.request_factory(context)
                response = execute_action(case.action, request_value)
                record = {
                    "case_id": case.case_id,
                    "group": case.group,
                    "action": case.action,
                    "backend": case.backend,
                    "status": response.get("status"),
                    "backend_version": response.get("backend_version"),
                    "elapsed_seconds": round(time.monotonic() - started, 6),
                    "request_summary": _request_summary(request_value),
                    "result_summary": _result_summary(response.get("result")),
                    "error": response.get("error"),
                    "warnings": response.get("warnings") or [],
                    "output_artifact_count": len(response.get("output_artifacts") or []),
                }
            except Exception as exc:  # keep the audit running after one backend failure
                record = {
                    "case_id": case.case_id,
                    "group": case.group,
                    "action": case.action,
                    "backend": case.backend,
                    "status": "failed",
                    "backend_version": None,
                    "elapsed_seconds": round(time.monotonic() - started, 6),
                    "request_summary": _request_summary(request_value) if request_value else None,
                    "result_summary": None,
                    "error": {"code": "matrix_runner_exception", "message": f"{type(exc).__name__}: {exc}"},
                    "warnings": [],
                    "output_artifact_count": 0,
                }
            records[pair] = record
            _write_status(args.output, cases, records)
            message = "PASS" if record["status"] in PASS_STATUSES else "FAIL"
            print(f"[{index}/{len(selected)}] {message} {case.case_id} {record['elapsed_seconds']}s", flush=True)

    payload = _write_status(args.output, cases, records)
    print(args.output)
    print(json.dumps(payload["summary"], ensure_ascii=False))
    selected_failed = [
        records[(case.action, case.backend)]
        for case in selected
        if (case.action, case.backend) in records
        and records[(case.action, case.backend)].get("status") not in PASS_STATUSES
    ]
    for item in selected_failed:
        print(item["case_id"], item["status"], item.get("error"))
    return 1 if selected_failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
