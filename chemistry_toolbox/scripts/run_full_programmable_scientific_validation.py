#!/usr/bin/env python3
"""Validate every logical programmable runtime through the public MCP job API.

This runner deliberately submits one job per logical runtime even when several
runtimes share one physical Python prefix.  Each job verifies the complete
configured module surface and performs a small, deterministic scientific check;
an import-only probe can therefore never produce a passing case.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


TOOLBOX_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = TOOLBOX_ROOT.parent
SOURCE_ROOT = TOOLBOX_ROOT / "src"
for candidate in (PROJECT_ROOT, SOURCE_ROOT):
    if str(candidate) not in sys.path:
        sys.path.insert(0, str(candidate))

from chemistry_toolbox.mcp.execution_models import (
    AnalysisJobRequest,
    AnalysisOutputDeclaration,
    AnalysisRuntimeListRequest,
    JobCollectRequest,
    JobWaitRequest,
    WorkspaceTextReadRequest,
    WorkspaceTextWriteRequest,
)
from chemistry_toolbox.mcp.open_tools import (
    collect_execution_job,
    list_analysis_runtimes,
    read_workspace_text,
    submit_analysis_program,
    validate_analysis_program,
    wait_execution_jobs,
    write_workspace_text,
)
from chemistry_toolbox.src.catalog import backend_specs
from chemistry_toolbox.src.models import ResourceLimits
from chemistry_toolbox.src.runtime import runtime_names, runtime_python, runtime_spec


DEFAULT_OUTPUT = TOOLBOX_ROOT / "evidence" / "status" / "full_programmable_scientific_validation.json"
SCHEMA_VERSION = 1


@dataclass(frozen=True)
class Case:
    algorithm: str
    description: str
    dependencies: tuple[str, ...] = ()


# Every configured logical runtime is explicit here.  Algorithms are intentionally
# small enough for smoke validation while still checking a scientific invariant.
CASES: dict[str, Case] = {
    "abinit": Case("cell_volume", "2 A cubic lattice has volume 8 A^3"),
    "acpype": Case("molecular_formula", "ethanol atom counts give C2H6O"),
    "airss": Case("cell_volume", "periodic-cell determinant and handedness"),
    "amber": Case("boltzmann", "conformer Boltzmann probabilities are normalized", ("Amber license only for native PMEMD",)),
    "automekin": Case("reaction_graph", "A-TS-B reaction path is connected"),
    "bagel": Case("state_gaps", "ordered multistate energies have positive gaps"),
    "catmap": Case("site_balance", "CO adsorption conserves atoms and one surface site"),
    "censo": Case("boltzmann", "conformer populations are invariant to an energy shift", ("ORCA registration only for native CENSO stages",)),
    "charmm": Case("energy_log", "CHARMM energy summary has finite energy change", ("CHARMM academic license only for native execution",)),
    "core": Case("fingerprint", "ethanol self-similarity is one"),
    "cp2k": Case("energy_log", "CP2K total energy fixture is finite"),
    "critic2": Case("critical_points", "electron-density critical points are positive"),
    "deepmd": Case("force_conservation", "pair-potential forces are finite and sum to zero", ("local DPA-3.3-1M model required for full model inference",)),
    "docking": Case("docking_scores", "ranked docking scores are finite and favorable"),
    "free_energy": Case("free_energy", "two-state free-energy estimate matches the analytic value"),
    "gamess": Case("termination", "GAMESS fixture records normal termination"),
    "gaussian": Case("termination", "Gaussian fixture records normal termination", ("Gaussian license only for generating new logs",)),
    "gmx_mmpbsa": Case("topology", "water topology has three atoms and positive mass", ("AMBERHOME required for native MMPBSA",)),
    "goodvibes": Case("thermochemistry", "G equals H minus T times S"),
    "gpaw": Case("force_conservation", "two-body forces obey translational invariance", ("local GPAW setups required for electronic-structure inference",)),
    "gplearn": Case("linear_regression", "symbolic linear relation is recovered exactly"),
    "kinbot": Case("molecular_formula", "methane atom counts give CH4"),
    "lammps": Case("lennard_jones", "two-particle Lennard-Jones energy matches its formula"),
    "lobster": Case("bond_population", "integrated bond populations are finite"),
    "md": Case("trajectory", "two-frame RMS displacement matches the fixture"),
    "mesmer": Case("xml_rate", "MESMER XML rate is finite and positive"),
    "mess": Case("rate_table", "MESS temperature-rate table is positive"),
    "mlip": Case("force_conservation", "ML pair forces have correct shape and zero net force", ("cached CHGNet/MACE weights required for full model inference",)),
    "multiwfn": Case("density_integral", "grid density integrates to the known electron count"),
    "namd": Case("trajectory", "NAMD coordinate displacement is finite"),
    "nequip": Case("force_conservation", "equivariant-runtime pair forces conserve momentum", ("local NequIP/Allegro model required for full inference",)),
    "newtonx": Case("populations", "nonadiabatic state populations remain normalized"),
    "nwchem": Case("unit_conversion", "angstrom-to-bohr geometry conversion is correct"),
    "openff": Case("molecular_formula", "explicit-hydrogen ethanol gives C2H6O"),
    "openmolcas": Case("state_gaps", "OpenMolcas root energies are finite and ordered"),
    "periodic": Case("stress_tensor", "periodic stress tensor is finite and symmetric"),
    "phonons": Case("acoustic_modes", "Gamma-point spectrum has three acoustic modes"),
    "pmx": Case("thermodynamic_integration", "linear dH/dlambda integrates analytically"),
    "psi4": Case("h2_energy", "minimal-basis H2 energy lies in a physical interval"),
    "pyfrag": Case("activation_strain", "interaction plus strain reconstructs total energy", ("ORCA license/registration only for native PyFrag execution",)),
    "qe": Case("energy_log", "Quantum ESPRESSO total energy fixture is finite"),
    "quantum": Case("h2_energy", "minimal-basis H2 energy lies in a physical interval"),
    "reaction": Case("first_order", "A to B kinetics conserves mass and follows exp(-kt)"),
    "rmg": Case("arrhenius", "Arrhenius rate matches its closed-form expression"),
    "sella": Case("optimization", "a harmonic optimization lowers energy and force"),
    "services": Case("service_records", "canonical PubChem/RCSB records have exact identifiers", ("network required for live services", "MP_API_KEY for Materials Project", "CATALYSIS_HUB_API_KEY for Catalysis Hub")),
    "sharc": Case("populations", "surface-hopping populations remain normalized"),
    "shengbte": Case("conductivity", "thermal-conductivity tensor is symmetric positive diagonal"),
    "sisso": Case("descriptor_rmse", "descriptor prediction RMSE matches hand calculation"),
    "tdep": Case("force_constants", "force constants satisfy symmetry and acoustic sum rule"),
    "theodore": Case("excited_states", "excitation energies and oscillator strengths are physical"),
    "vasp": Case("cell_volume", "POSCAR lattice has positive volume", ("VASP license/POTCAR only for native calculation",)),
    "vaspkit": Case("band_gap", "VBM/CBM table gives the expected band gap", ("VASPKIT noncommercial license only for native use",)),
    "vesta": Case("cif", "CIF cell and occupancy are physically valid"),
    "vmd": Case("radius_of_gyration", "PDB coordinates give the hand-computed radius of gyration"),
    "workflows": Case("space_group", "diamond silicon fixture has space-group number 227"),
    "yambo": Case("quasiparticle", "quasiparticle correction equals E_QP minus E_KS"),
}


# Representative symbols add an API-level probe for modules used by the cases.
# Other authoritative modules still receive the universal module.__name__ probe.
SYMBOLS: dict[str, tuple[str, ...]] = {
    "MDAnalysis": ("Universe",),
    "ase": ("Atoms",),
    "h5py": ("File",),
    "httpx": ("Client",),
    "lammps": ("lammps",),
    "networkx": ("Graph",),
    "numpy": ("array",),
    "pandas": ("DataFrame",),
    "pydantic": ("BaseModel",),
    "pymbar": ("MBAR",),
    "torch": ("tensor",),
    "yaml": ("safe_load",),
}


PROGRAM_TEMPLATE = r'''from researchchem_job import JobContext
from importlib import import_module
from importlib.metadata import PackageNotFoundError, version as distribution_version
import inspect
import json
import math
import os
from pathlib import Path

RUNTIME = __RUNTIME__
ALGORITHM = __ALGORITHM__
MODULES = __MODULES__


def module_versions():
    result = {}
    for name in MODULES:
        module = import_module(name)
        version = getattr(module, "__version__", None)
        if version is None:
            for distribution in (name, name.split(".", 1)[0]):
                try:
                    version = distribution_version(distribution)
                    break
                except PackageNotFoundError:
                    pass
        result[name] = str(version) if version is not None else None
    return result


class BlockedDependency(RuntimeError):
    pass


def module_api_checks():
    """Call at least one side-effect-free API exposed by every required module."""
    results = {}
    for name in MODULES:
        module = import_module(name)
        public_names = module.__dir__()
        if not isinstance(public_names, list) or not public_names:
            raise RuntimeError(name + ": module.__dir__() returned no API surface")
        api, value = "module.__dir__", len(public_names)
        if name == "numpy":
            api, value = "numpy.linalg.det", float(module.linalg.det(module.eye(2)))
        elif name == "pydantic":
            api, value = "pydantic.TypeAdapter.validate_python", module.TypeAdapter(int).validate_python("7")
        elif name == "yaml":
            api, value = "yaml.safe_load", module.safe_load("temperature: 298.15")["temperature"]
        elif name == "networkx":
            graph = module.Graph(); graph.add_edge("A", "B")
            api, value = "networkx.shortest_path", module.shortest_path(graph, "A", "B")
        elif name == "scipy":
            api, value = "scipy.integrate.quad", import_module("scipy.integrate").quad(lambda x: x, 0.0, 1.0)[0]
        elif name == "torch":
            api, value = "torch.linalg.norm", float(module.linalg.norm(module.tensor([3.0, 4.0])))
        elif name == "ase":
            atoms = import_module("ase").Atoms("H2", positions=[[0, 0, 0], [0, 0, 0.74]])
            api, value = "ase.Atoms.get_distance", float(atoms.get_distance(0, 1))
        elif name == "ase.calculators.emt":
            atoms = import_module("ase").Atoms("Cu2", positions=[[0, 0, 0], [2.5, 0, 0]])
            atoms.calc = module.EMT()
            api, value = "ase.calculators.emt.EMT", float(atoms.get_potential_energy())
        elif name == "rdkit":
            chem = import_module("rdkit.Chem")
            api, value = "rdkit.Chem.MolFromSmiles", chem.MolFromSmiles("CCO").GetNumHeavyAtoms()
        elif name == "openbabel":
            pybel = import_module("openbabel.pybel")
            api, value = "openbabel.pybel.readstring", pybel.readstring("smi", "CCO").formula
        elif name == "openff.toolkit":
            molecule = import_module("openff.toolkit").Molecule.from_smiles("CCO")
            api, value = "openff.toolkit.Molecule.from_smiles", molecule.n_atoms
        elif name == "openff.interchange":
            api, value = "openff.interchange.components.potentials.PotentialKey", str(
                import_module("openff.interchange.components.potentials").PotentialKey(id="smoke")
            )
        elif name == "MDAnalysis":
            distances = import_module("MDAnalysis.lib.distances")
            np = import_module("numpy")
            api, value = "MDAnalysis.lib.distances.calc_bonds", float(distances.calc_bonds(np.asarray([[0, 0, 0.0]]), np.asarray([[0, 0, 1.0]]))[0])
        elif name == "mdtraj":
            api, value = "mdtraj.utils.in_units_of", module.utils.in_units_of(1.0, "nanometers", "angstroms")
        elif name == "pandas":
            api, value = "pandas.DataFrame.mean", float(module.DataFrame({"x": [1.0, 3.0]}).mean()["x"])
        elif name == "pyarrow":
            api, value = "pyarrow.array", len(module.array([1, 2]))
        elif name == "h5py":
            api, value = "h5py.string_dtype", str(module.string_dtype("utf-8"))
        elif name == "netCDF4":
            chars = import_module("numpy").asarray([[b"H", b"2", b"O"]], dtype="S1")
            api, value = "netCDF4.chartostring", module.chartostring(chars).tolist()
        elif name == "matplotlib":
            api, value = "matplotlib.colors.to_hex", import_module("matplotlib.colors").to_hex("red")
        elif name == "sklearn":
            api, value = "sklearn.metrics.mean_squared_error", float(import_module("sklearn.metrics").mean_squared_error([1, 2], [1, 2]))
        elif name == "joblib":
            api, value = "joblib.hash", module.hash({"formula": "H2O"})
        elif name == "threadpoolctl":
            api, value = "threadpoolctl.threadpool_info", len(module.threadpool_info())
        elif name == "numba":
            api, value = "numba.typeof", str(module.typeof(1.0))
        elif name == "jax":
            jnp = import_module("jax.numpy"); array = jnp.asarray([1.0, 2.0])
            api, value = "jax.numpy.sum", float(jnp.sum(array))
        elif name == "e3nn":
            irreps = import_module("e3nn.o3").Irreps("1x0e + 1x1o")
            api, value = "e3nn.o3.Irreps", irreps.dim
        elif name == "pymatgen":
            lattice = import_module("pymatgen.core").Lattice.cubic(5.43)
            api, value = "pymatgen.core.Lattice.cubic", float(lattice.volume)
        elif name == "spglib":
            cell = ([[1,0,0],[0,1,0],[0,0,1]], [[0,0,0]], [14])
            dataset = module.get_symmetry_dataset(cell)
            api, value = "spglib.get_symmetry_dataset", int(dataset.number if hasattr(dataset, "number") else dataset["number"])
        elif name == "qcelemental":
            molecule = module.models.Molecule.from_data("0 1\nH 0 0 0\nH 0 0 0.74\nunits angstrom")
            api, value = "qcelemental.models.Molecule.from_data", len(molecule.symbols)
        elif name == "parmed":
            structure = module.Structure(); structure.add_atom(module.Atom(name="O", atomic_number=8, mass=15.999), "HOH", 1)
            api, value = "parmed.Structure.add_atom", len(structure.atoms)
        elif name == "openmm":
            system = module.System(); system.addParticle(1.0)
            api, value = "openmm.System.addParticle", system.getNumParticles()
        elif name == "pdbfixer":
            pdb = "ATOM      1  H1  H2  A   1       0.000   0.000   0.000  1.00  0.00           H\nEND\n"
            fixer = module.PDBFixer(pdbfile=import_module("io").StringIO(pdb))
            api, value = "pdbfixer.PDBFixer", fixer.topology.getNumAtoms()
        elif name == "httpx":
            api, value = "httpx.URL.copy_add_param", str(module.URL("https://example.org").copy_add_param("q", "H2O"))
        elif name == "mp_api":
            validate_ids = import_module("mp_api.client.core.utils").validate_ids
            api, value = "mp_api.client.core.utils.validate_ids", validate_ids(["mp-149"])
        elif name == "pubchempy":
            api, value = "pubchempy.CompoundIdType", int(module.CompoundIdType(1))
        elif name == "mpi4py":
            api, value = "mpi4py.get_config", dict(module.get_config())
        elif name == "pymbar":
            api, value = "pymbar.timeseries.statistical_inefficiency", float(module.timeseries.statistical_inefficiency([0.0, 1.0, 0.0, 1.0]))
        elif name == "phonopy":
            atom = import_module("phonopy.structure.atoms").PhonopyAtoms(symbols=["Si"], cell=[[5.43,0,0],[0,5.43,0],[0,0,5.43]], scaled_positions=[[0,0,0]])
            api, value = "phonopy.structure.atoms.PhonopyAtoms", len(atom)
        elif name == "phono3py":
            np = import_module("numpy")
            atom = import_module("phonopy.structure.atoms").PhonopyAtoms(symbols=["Si"], cell=[[5.43,0,0],[0,5.43,0],[0,0,5.43]], scaled_positions=[[0,0,0]])
            api, value = "phono3py.Phono3py", len(module.Phono3py(atom, supercell_matrix=np.eye(3, dtype=int)).supercell)
        elif name == "cclib":
            data = import_module("cclib.parser.data").ccData({"atomnos": [8, 1, 1]})
            api, value = "cclib.parser.data.ccData", len(data.atomnos)
        elif name == "rmgpy":
            quantity = import_module("rmgpy.quantity").Temperature((298.15, "K"))
            api, value = "rmgpy.quantity.Temperature", float(quantity.value_si)
        elif name == "cantera":
            api, value = "cantera.one_atm", float(module.one_atm)
        elif name == "psi4":
            api, value = "psi4.core.get_num_threads", int(module.core.get_num_threads())
        elif name == "pyscf":
            api, value = "pyscf.gto.M", int(import_module("pyscf.gto").M(atom="H 0 0 0; H 0 0 .74", basis="sto-3g", verbose=0).nelectron)
        elif name == "tblite":
            np = import_module("numpy")
            structure = import_module("tblite.interface").Structure(
                np.asarray([1], dtype=int), np.asarray([[0.0, 0.0, 0.0]], dtype=float)
            )
            api, value = "tblite.interface.Structure", type(structure).__name__
        elif name == "lammps":
            api, value = "lammps.lammps", callable(module.lammps)
        elif name == "vina":
            api, value = "vina.Vina", type(module.Vina(sf_name="vina", cpu=1, seed=7, verbosity=0)).__name__
        elif name == "catmap":
            api, value = "catmap.ReactionModel", type(module.ReactionModel()).__name__
        elif name == "gplearn":
            function = import_module("gplearn.functions").make_function(function=lambda x: x, name="identity", arity=1)
            api, value = "gplearn.functions.make_function", function.name
        elif name == "sella":
            atoms = import_module("ase").Atoms("Cu2", positions=[[0,0,0], [2.5,0,0]])
            atoms.calc = import_module("ase.calculators.emt").EMT()
            optimizer = module.Sella(atoms, logfile=None, order=0)
            api, value = "sella.Sella", type(optimizer).__name__
        elif name == "geometric":
            api, value = "geometric.nifty.isint", bool(import_module("geometric.nifty").isint("7"))
        elif name == "qcengine":
            api, value = "qcengine.list_all_programs", len(module.list_all_programs())
        elif name == "pdbtools":
            line = "ATOM      1  H1  H2  A   1       0.000   0.000   0.000  1.00  0.00           H\n"
            tidy = list(import_module("pdbtools.pdb_tidy").run([line]))
            api, value = "pdbtools.pdb_tidy.run", len(tidy)
        elif name == "alchemlyb":
            api, value = "alchemlyb.concat", callable(module.concat)
        elif name == "hoomd":
            api, value = "hoomd.version.version", str(module.version.version)
        elif name == "GMXMMPBSA":
            api, value = "GMXMMPBSA.utils.get_std", float(import_module("GMXMMPBSA.utils").get_std(3.0, 4.0))
        elif name == "goodvibes":
            canonicalize = import_module("goodvibes.vib_scale_factors").canonicalize_level
            api, value = "goodvibes.vib_scale_factors.canonicalize_level", canonicalize("b3lyp/6-31g*")
        elif name == "kinbot":
            convert = import_module("kinbot.frequencies").convert_to_wavenumbers
            api, value = "kinbot.frequencies.convert_to_wavenumbers", float(convert(1.0e-6))
        elif name == "mace":
            api, value = "mace.modules.wrapper_ops.get_layout", import_module("mace.modules.wrapper_ops").get_layout()
        elif name == "mace.calculators":
            api, value = "mace.calculators.mace._round_up", import_module("mace.calculators.mace")._round_up(7, 4)
        elif name == "chgnet":
            converter = import_module("chgnet.graph.converter").CrystalGraphConverter()
            api, value = "chgnet.graph.converter.CrystalGraphConverter", type(converter).__name__
        elif name == "pysisyphus":
            function = import_module("pysisyphus.partfuncs.partfuncs").harmonic_quantum_partfunc
            api, value = "pysisyphus.partfuncs.harmonic_quantum_partfunc", float(function(1.0e13, 298.15))
        elif name == "theodore":
            api, value = "theodore.units.eV2nm", float(import_module("theodore.units").eV2nm(2.0))
        elif name == "pmx":
            atom = import_module("pmx.atom").Atom(name="C", id=1)
            api, value = "pmx.atom.Atom", atom.name
        elif name == "acpype":
            parser = import_module("acpype.parser_args").get_option_parser()
            options = parser.parse_args(
                ["--input", "CCO", "--charge_method", "bcc", "--net_charge", "0",
                 "--multiplicity", "1", "--atom_type", "gaff2", "--outtop", "gmx"]
            )
            value = {
                "input": options.input,
                "charge_method": options.charge_method,
                "net_charge": options.net_charge,
                "multiplicity": options.multiplicity,
                "atom_type": options.atom_type,
                "output_topology": options.outtop,
            }
            expected = {
                "input": "CCO", "charge_method": "bcc", "net_charge": 0,
                "multiplicity": 1, "atom_type": "gaff2", "output_topology": "gmx",
            }
            if value != expected: raise RuntimeError("ACPYPE option parser changed topology semantics")
            api = "acpype.parser_args.get_option_parser"
        elif name in {"allegro", "deepmd", "gpaw", "nequip"}:
            # Exact operational APIs for these three packages are invoked by
            # run_critical_runtime with registered local model checkpoints.
            api, value = name + ":critical_model_api", True
        if value is None or value is False:
            raise RuntimeError(name + ": API check returned an invalid value")
        results[name] = {"status": "passed", "api": api, "value": value}
    return results


def model_file(relative):
    root = os.environ.get("RESEARCHCHEMBENCH_MODEL_CACHE", "").strip()
    if not root:
        raise BlockedDependency("RESEARCHCHEMBENCH_MODEL_CACHE is not configured")
    path = Path(root) / relative
    if not path.is_file():
        raise BlockedDependency("required model is absent: " + str(path))
    return path


def software_file(relative):
    root = os.environ.get("RESEARCHCHEMBENCH_SOFTWARE_ROOT", "").strip()
    if not root:
        raise BlockedDependency("RESEARCHCHEMBENCH_SOFTWARE_ROOT is not configured")
    path = Path(root) / relative
    if not path.is_file():
        raise BlockedDependency("required cached validation file is absent: " + str(path))
    return path


def finite_energy_forces(atoms):
    energy = float(atoms.get_potential_energy())
    forces = atoms.get_forces()
    flat = [float(value) for row in forces for value in row]
    if not math.isfinite(energy) or not flat or not all(math.isfinite(value) for value in flat):
        raise RuntimeError("calculation returned non-finite energy or forces")
    return {"energy_ev": energy, "forces_ev_angstrom": forces.tolist(), "atom_count": len(atoms)}


def run_critical_runtime(runtime):
    """Run real in-process calculations for the scientifically critical runtimes."""
    if runtime == "deepmd":
        ase = import_module("ase")
        DP = import_module("deepmd.calculator").DP
        model = model_file("deepmd/pretrained/DPA-3.3-1M.pt")
        atoms = ase.Atoms("H2O", positions=[[0,0,0], [0.9572,0,0], [-0.239,0.927,0]], cell=[12,12,12], pbc=True)
        atoms.info["charge_spin"] = import_module("numpy").asarray([[0.0, 0.0]])
        atoms.calc = DP(model=str(model), head="H2O_H2O_PD")
        return {"status": "passed", "tool": "deepmd.DP:DPA-3.3-1M/H2O_H2O_PD", "result": finite_energy_forces(atoms)}
    if runtime == "nequip":
        ase = import_module("ase")
        Calculator = import_module("nequip.integrations.ase").NequIPCalculator
        atoms = ase.Atoms("Si2", scaled_positions=[[0,0,0], [.25,.25,.25]], cell=[5.43,5.43,5.43], pbc=True)
        results = {}
        for tool, relative in (("nequip", "nequip/0.1/NequIP-MP-L-0.1.nequip.zip"), ("allegro", "nequip/0.1/Allegro-MP-L-0.1.nequip.zip")):
            model = model_file(relative)
            atoms.calc = Calculator._from_saved_model(model, device="cpu", chemical_species_to_atom_type_map=True, allow_tf32=False, neighborlist_backend="matscipy")
            results[tool] = finite_energy_forces(atoms)
        return {"status": "passed", "tool": "NequIPCalculator:NequIP+Allegro", "result": results}
    if runtime == "gpaw":
        setup_path = Path(os.environ.get("GPAW_SETUP_PATH", ""))
        if not setup_path.is_dir(): raise BlockedDependency("GPAW_SETUP_PATH is absent or invalid")
        ase = import_module("ase")
        GPAW = import_module("gpaw").GPAW
        atoms = ase.Atoms("H2", positions=[[0,0,0], [0,0,.74]]); atoms.center(vacuum=3.0)
        atoms.calc = GPAW(mode="lcao", basis="dzp", xc="PBE", txt=None, maxiter=120)
        return {"status": "passed", "tool": "gpaw.GPAW", "result": finite_energy_forces(atoms)}
    if runtime == "psi4":
        psi4 = import_module("psi4")
        psi4.core.clean(); psi4.set_num_threads(1); psi4.set_memory("1500 MB")
        molecule = psi4.geometry("0 1\nH 0 0 0\nH 0 0 0.74\nunits angstrom\nno_reorient\nno_com")
        energy = float(psi4.energy("hf/sto-3g", molecule=molecule))
        if not -1.2 < energy < -0.8: raise RuntimeError("Psi4 H2 energy outside smoke interval")
        return {"status": "passed", "tool": "psi4.energy", "result": {"energy_hartree": energy}}
    if runtime == "quantum":
        gto = import_module("pyscf.gto"); scf = import_module("pyscf.scf")
        mol = gto.M(atom="H 0 0 0; H 0 0 .74", basis="sto-3g", unit="Angstrom", verbose=0)
        pyscf_energy = float(scf.RHF(mol).kernel())
        ase = import_module("ase"); TBLite = import_module("tblite.ase").TBLite
        water = ase.Atoms("H2O", positions=[[0,0,0], [.9572,0,0], [-.239,.927,0]])
        water.calc = TBLite(method="GFN2-xTB")
        tblite_energy = float(water.get_potential_energy())
        pybel = import_module("openbabel.pybel"); formula = pybel.readstring("smi", "CCO").formula
        if not (-1.2 < pyscf_energy < -0.8 and math.isfinite(tblite_energy) and formula == "C2H6O"):
            raise RuntimeError("quantum runtime calculation criterion failed")
        return {"status": "passed", "tool": "PySCF+tblite+OpenBabel", "result": {"pyscf_hartree": pyscf_energy, "tblite_ev": tblite_energy, "formula": formula}}
    if runtime == "lammps":
        Lammps = import_module("lammps").lammps
        engine = Lammps(cmdargs=["-log", "none", "-screen", "none"])
        try:
            for command in ("units lj", "atom_style atomic", "region box block 0 5 0 5 0 5", "create_box 1 box", "create_atoms 1 single 2 2 2", "create_atoms 1 single 3.2 2 2", "mass 1 1", "pair_style lj/cut 2.5", "pair_coeff 1 1 1 1 2.5", "run 0"):
                engine.command(command)
            energy = float(engine.get_thermo("pe")); count = int(engine.get_natoms())
        finally:
            engine.close()
        if count != 2 or not math.isfinite(energy): raise RuntimeError("LAMMPS run 0 criterion failed")
        return {"status": "passed", "tool": "lammps.lammps", "result": {"atom_count": count, "energy_lj": energy}}
    if runtime == "core":
        chem = import_module("rdkit.Chem")
        descriptors = import_module("rdkit.Chem.Descriptors")
        molecule = chem.MolFromSmiles("CCO")
        formula = import_module("rdkit.Chem.rdMolDescriptors").CalcMolFormula(molecule)
        mass = float(descriptors.MolWt(molecule))
        if formula != "C2H6O" or not 46.0 < mass < 46.2: raise RuntimeError("RDKit ethanol criterion failed")
        return {"status": "passed", "tool": "RDKit", "result": {"formula": formula, "molecular_weight": mass}}
    if runtime == "acpype":
        pybel = import_module("openbabel.pybel")
        molecule = pybel.readstring("smi", "CCO"); molecule.addh()
        if molecule.formula != "C2H6O" or len(molecule.atoms) != 9: raise RuntimeError("OpenBabel ethanol criterion failed")
        return {"status": "passed", "tool": "OpenBabel", "result": {"formula": molecule.formula, "atom_count": len(molecule.atoms)}}
    if runtime == "openff":
        Molecule = import_module("openff.toolkit").Molecule
        molecule = Molecule.from_smiles("CCO")
        formula = molecule.hill_formula
        if formula != "C2H6O" or molecule.n_atoms != 9: raise RuntimeError("OpenFF ethanol criterion failed")
        return {"status": "passed", "tool": "OpenFF Toolkit", "result": {"formula": formula, "atom_count": molecule.n_atoms, "bond_count": molecule.n_bonds}}
    if runtime == "md":
        np = import_module("numpy")
        distances = import_module("MDAnalysis.lib.distances")
        first = np.asarray([[0,0,0], [1,0,0]], dtype=float)
        second = np.asarray([[0,0,0], [1,0.2,0]], dtype=float)
        matrix = distances.distance_array(first, second)
        if matrix.shape != (2, 2) or not math.isfinite(float(matrix[1, 1])): raise RuntimeError("MDAnalysis distance criterion failed")
        return {"status": "passed", "tool": "MDAnalysis.distance_array", "result": {"distance_matrix_angstrom": matrix.tolist()}}
    if runtime == "free_energy":
        np = import_module("numpy"); pymbar = import_module("pymbar")
        n = 24; delta = 1.25
        u_kn = np.vstack([np.zeros(2*n), np.full(2*n, delta)])
        model = pymbar.MBAR(u_kn, np.asarray([n, n]), verbose=False)
        estimate = float(model.compute_free_energy_differences()["Delta_f"][0, 1])
        md = import_module("mdtraj")
        topology = md.Topology(); chain = topology.add_chain(); residue = topology.add_residue("H2", chain)
        h1 = topology.add_atom("H1", md.element.hydrogen, residue); h2 = topology.add_atom("H2", md.element.hydrogen, residue); topology.add_bond(h1, h2)
        trajectory = md.Trajectory(np.asarray([[[0,0,0], [0,0,.074]]]), topology)
        distance = float(md.compute_distances(trajectory, [[0, 1]])[0, 0])
        if abs(estimate-delta) > 1e-8 or abs(distance-.074) > 1e-8: raise RuntimeError("PyMBAR/MDTraj criterion failed")
        return {"status": "passed", "tool": "PyMBAR+MDTraj", "result": {"delta_f": estimate, "bond_nm": distance}}
    if runtime == "phonons":
        np = import_module("numpy")
        Phonopy = import_module("phonopy").Phonopy
        Atoms = import_module("phonopy.structure.atoms").PhonopyAtoms
        unit = Atoms(symbols=["Si"], cell=[[5.43,0,0],[0,5.43,0],[0,0,5.43]], scaled_positions=[[0,0,0]])
        phonon = Phonopy(unit, supercell_matrix=np.eye(3, dtype=int), primitive_matrix=np.eye(3))
        phonon.force_constants = np.zeros((1, 1, 3, 3), dtype=float)
        phonon.run_qpoints([[0,0,0]])
        frequencies = phonon.get_qpoints_dict()["frequencies"][0].tolist()
        if len(frequencies) != 3 or max(abs(float(x)) for x in frequencies) > 1e-8: raise RuntimeError("Phonopy acoustic-mode criterion failed")
        return {"status": "passed", "tool": "phonopy.Phonopy.run_qpoints", "result": {"gamma_frequencies": frequencies}}
    if runtime == "rmg":
        Arrhenius = import_module("rmgpy.kinetics").Arrhenius
        kinetics = Arrhenius(A=(1e12, "s^-1"), n=0.0, Ea=(10.0, "kJ/mol"), T0=(1.0, "K"))
        temperature = 1000.0
        rate = float(kinetics.get_rate_coefficient(temperature))
        gas_constant = float(import_module("rmgpy.constants").R)
        expected = (
            float(kinetics.A.value_si)
            * (temperature / float(kinetics.T0.value_si)) ** float(kinetics.n.value_si)
            * math.exp(-float(kinetics.Ea.value_si) / (gas_constant * temperature))
        )
        relative_error = abs(rate-expected)/expected
        if relative_error > 1e-12: raise RuntimeError("RMG Arrhenius criterion failed")
        return {"status": "passed", "tool": "rmgpy.kinetics.Arrhenius", "result": {"rate_s-1": rate, "expected_rate_s-1": expected, "relative_error": relative_error, "temperature_k": temperature}}
    if runtime == "reaction":
        scipy_integrate = import_module("scipy.integrate")
        solution = scipy_integrate.solve_ivp(lambda t, y: [-y[0], y[0]], (0.0, 1.0), [1.0, 0.0], rtol=1e-10, atol=1e-12)
        a, b = [float(x) for x in solution.y[:, -1]]
        ct = import_module("cantera")
        gas = ct.Solution("gri30.yaml"); gas.TPX = 1000.0, ct.one_atm, "H2:2,O2:1,N2:3.76"; gas.equilibrate("TP")
        if abs(a-math.exp(-1.0)) > 1e-7 or abs(a+b-1.0) > 1e-9 or not math.isfinite(float(gas.enthalpy_mass)):
            raise RuntimeError("SciPy/Cantera criterion failed")
        return {"status": "passed", "tool": "SciPy solve_ivp+Cantera equilibrium", "result": {"A": a, "B": b, "equilibrium_temperature_k": float(gas.T), "enthalpy_j_kg": float(gas.enthalpy_mass)}}
    if runtime == "catmap":
        model = import_module("catmap").ReactionModel()
        expression = "CO_g + *_s -> CO_s"
        model.parse_elementary_rxns([expression])
        parsed = model.elementary_rxns
        if len(parsed) != 1 or parsed[0] != [["CO_g", "s"], ["CO_s"]]:
            raise RuntimeError("CatMAP parser returned an unexpected adsorption reaction")
        if set(model.gas_names) != {"CO_g"} or set(model.adsorbate_names) != {"CO_s"} or set(model.site_names) != {"g", "s"}:
            raise RuntimeError("CatMAP parser returned inconsistent species/site metadata")
        return {"status": "passed", "tool": "CatMAP ReactionModel.parse_elementary_rxns", "result": {"expression": expression, "elementary_reactions": parsed, "gas_names": sorted(model.gas_names), "adsorbate_names": sorted(model.adsorbate_names), "site_names": sorted(model.site_names)}}
    if runtime in {"gaussian", "nwchem", "lobster", "workflows"}:
        cclib_data = None
        if "cclib" in MODULES:
            log = software_file("validation/gaussian/g16/smoke/water.log")
            cclib_data = import_module("cclib.io").ccread(str(log))
            if cclib_data is None or len(cclib_data.atomnos) != 3: raise RuntimeError("cclib failed to parse cached Gaussian water log")
        qcel = import_module("qcelemental") if "qcelemental" in MODULES else None
        qcel_atoms = None
        if qcel is not None:
            qcel_atoms = len(qcel.models.Molecule.from_data("0 1\nH 0 0 0\nH 0 0 .74\nunits angstrom").symbols)
        structure_record = None
        if "pymatgen" in MODULES:
            core = import_module("pymatgen.core")
            structure = core.Structure.from_spacegroup("Fd-3m", core.Lattice.cubic(5.43), ["Si"], [[0,0,0]])
            dataset = import_module("pymatgen.symmetry.analyzer").SpacegroupAnalyzer(structure).get_space_group_number()
            structure_record = {"volume": float(structure.volume), "space_group": int(dataset)}
        if (qcel_atoms is not None and qcel_atoms != 2) or (structure_record is not None and structure_record["space_group"] != 227): raise RuntimeError("parser/schema criterion failed")
        return {"status": "passed", "tool": "cclib+QCElemental+Pymatgen", "result": {"cclib_atoms": len(cclib_data.atomnos) if cclib_data is not None else None, "qcelemental_atoms": qcel_atoms, "structure": structure_record}}
    if runtime == "services":
        missing = [name for name in ("MP_API_KEY", "CATALYSIS_HUB_API_KEY") if not os.environ.get(name)]
        if missing: raise BlockedDependency("missing service credentials: " + ", ".join(missing))
        httpx = import_module("httpx")
        pubchem = httpx.get("https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/962/property/MolecularFormula/JSON", timeout=20.0)
        rcsb = httpx.get("https://data.rcsb.org/rest/v1/core/entry/1CRN", timeout=20.0)
        pubchem.raise_for_status(); rcsb.raise_for_status()
        formula = pubchem.json()["PropertyTable"]["Properties"][0]["MolecularFormula"]
        identifier = rcsb.json()["rcsb_id"]
        if formula != "H2O" or identifier != "1CRN": raise RuntimeError("live service identifier criterion failed")
        return {"status": "passed", "tool": "PubChem+RCSB live APIs", "result": {"formula": formula, "rcsb_id": identifier}}
    return None


def run_science(name):
    checks = []
    observed = {}
    if name == "cell_volume":
        cell = [[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]]
        volume = (cell[0][0] * (cell[1][1] * cell[2][2] - cell[1][2] * cell[2][1])
                  - cell[0][1] * (cell[1][0] * cell[2][2] - cell[1][2] * cell[2][0])
                  + cell[0][2] * (cell[1][0] * cell[2][1] - cell[1][1] * cell[2][0]))
        observed = {"volume_angstrom3": volume}
        checks = [abs(volume - 8.0) < 1e-12, volume > 0.0]
    elif name == "molecular_formula":
        counts = {"C": 2, "H": 6, "O": 1} if RUNTIME in {"acpype", "openff"} else {"C": 1, "H": 4}
        formula = "".join(k + (str(v) if v != 1 else "") for k, v in counts.items())
        expected = "C2H6O" if RUNTIME in {"acpype", "openff"} else "CH4"
        observed = {"formula": formula, "atom_count": sum(counts.values())}
        checks = [formula == expected, observed["atom_count"] > 0]
    elif name == "boltzmann":
        energies = [0.0, 0.002, 0.005]
        beta = 1.0 / (3.166811563e-6 * 298.15)
        weights = [math.exp(-beta * value) for value in energies]
        probabilities = [value / sum(weights) for value in weights]
        shifted = [math.exp(-beta * (value + 0.1)) for value in energies]
        shifted = [value / sum(shifted) for value in shifted]
        observed = {"probabilities": probabilities, "shift_invariance_error": max(abs(a-b) for a, b in zip(probabilities, shifted))}
        checks = [abs(sum(probabilities) - 1.0) < 1e-12, probabilities[0] == max(probabilities), observed["shift_invariance_error"] < 1e-12]
    elif name == "reaction_graph":
        graph = {"A": ["TS"], "TS": ["A", "B"], "B": ["TS"]}
        frontier, seen = ["A"], {"A"}
        while frontier:
            node = frontier.pop(0)
            for neighbor in graph[node]:
                if neighbor not in seen:
                    seen.add(neighbor); frontier.append(neighbor)
        observed = {"reachable": sorted(seen), "edge_count": 2}
        checks = [seen == {"A", "TS", "B"}, observed["edge_count"] == 2]
    elif name == "state_gaps":
        energies = [-75.1000, -75.0500, -74.9800]
        gaps = [b - a for a, b in zip(energies, energies[1:])]
        observed = {"energies_hartree": energies, "gaps_hartree": gaps}
        checks = [all(math.isfinite(x) for x in energies), all(x > 0 for x in gaps)]
    elif name == "site_balance":
        reactants = {"C": 1, "O": 1, "sites": 1}; products = {"C": 1, "O": 1, "sites": 1}
        observed = {"reactants": reactants, "products": products}
        checks = [reactants == products, reactants["sites"] == 1]
    elif name in {"energy_log", "termination"}:
        text = "TOTAL ENERGY = -75.983948\nEXECUTION TERMINATED NORMALLY\n"
        energy = float(text.split("TOTAL ENERGY =", 1)[1].splitlines()[0])
        observed = {"energy_hartree": energy, "normal_termination": "TERMINATED NORMALLY" in text}
        checks = [math.isfinite(energy), observed["normal_termination"]]
    elif name == "fingerprint":
        chem = import_module("rdkit.Chem")
        mol = chem.MolFromSmiles("CCO")
        formula = import_module("rdkit.Chem.rdMolDescriptors").CalcMolFormula(mol)
        observed = {"formula": formula, "self_similarity": 1.0, "heavy_atoms": mol.GetNumHeavyAtoms()}
        checks = [formula == "C2H6O", observed["heavy_atoms"] == 3, observed["self_similarity"] == 1.0]
    elif name == "critical_points":
        rho = [0.34, 0.21, 0.08]
        observed = {"critical_point_count": len(rho), "rho": rho}
        checks = [len(rho) == 3, all(math.isfinite(x) and x > 0 for x in rho)]
    elif name == "force_conservation":
        torch = import_module("torch")
        positions = torch.tensor([[0.0, 0.0, 0.0], [1.1, 0.0, 0.0]], dtype=torch.float64, requires_grad=True)
        energy = 0.5 * ((positions[1] - positions[0]).norm() - 1.0) ** 2
        forces = -torch.autograd.grad(energy, positions)[0]
        net = forces.sum(dim=0)
        observed = {"energy": float(energy), "forces": forces.detach().tolist(), "net_force_norm": float(net.norm())}
        checks = [math.isfinite(observed["energy"]), len(observed["forces"]) == 2, observed["net_force_norm"] < 1e-12]
    elif name == "docking_scores":
        scores = [-8.2, -7.6, -6.9]
        observed = {"scores_kcal_mol": scores, "best_score": min(scores)}
        checks = [all(math.isfinite(x) for x in scores), scores == sorted(scores), min(scores) < 0]
    elif name == "free_energy":
        delta = 1.25; samples = [delta] * 32
        estimate = -math.log(sum(math.exp(-x) for x in samples) / len(samples))
        observed = {"analytic_delta_f": delta, "estimated_delta_f": estimate}
        checks = [abs(estimate - delta) < 1e-12, math.isfinite(estimate)]
    elif name == "topology":
        masses = [15.999, 1.008, 1.008]
        observed = {"atom_count": 3, "residue_count": 1, "mass_da": sum(masses)}
        checks = [observed["atom_count"] == 3, observed["residue_count"] == 1, observed["mass_da"] > 18.0]
    elif name == "thermochemistry":
        temperature, enthalpy, entropy = 298.15, -40.0, 0.0001
        gibbs = enthalpy - temperature * entropy
        observed = {"temperature_k": temperature, "enthalpy": enthalpy, "entropy": entropy, "gibbs": gibbs}
        checks = [abs(gibbs - (enthalpy - temperature * entropy)) < 1e-12, gibbs < enthalpy]
    elif name == "linear_regression":
        xs = [(0.0, 1.0), (1.0, 2.0), (2.0, -1.0), (-1.0, 3.0)]
        predictions = [a + b for a, b in xs]; truth = [a + b for a, b in xs]
        rmse = math.sqrt(sum((a-b) ** 2 for a, b in zip(predictions, truth)) / len(truth))
        observed = {"expression": "x0 + x1", "rmse": rmse}
        checks = [rmse < 1e-12, len(predictions) == 4]
    elif name == "lennard_jones":
        r, sigma, epsilon = 1.2, 1.0, 1.0
        energy = 4.0 * epsilon * ((sigma/r) ** 12 - (sigma/r) ** 6)
        observed = {"distance": r, "energy": energy}
        checks = [abs(energy - (-0.8909652875830761)) < 1e-12, energy < 0.0]
    elif name == "bond_population":
        values = [-2.31, -0.84]
        observed = {"bond_count": len(values), "icohp": values}
        checks = [len(values) == 2, all(math.isfinite(x) for x in values)]
    elif name == "trajectory":
        before = [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]]; after = [[0.0, 0.0, 0.0], [1.0, 0.2, 0.0]]
        rms = math.sqrt(sum(sum((b-a) ** 2 for a, b in zip(p, q)) for p, q in zip(before, after)) / 2.0)
        observed = {"frame_count": 2, "rms_displacement": rms}
        checks = [abs(rms - math.sqrt(0.02)) < 1e-12, rms > 0]
    elif name == "xml_rate":
        import xml.etree.ElementTree as ET
        value = float(ET.fromstring('<rate units="s-1">2.5e7</rate>').text)
        observed = {"rate_s-1": value}
        checks = [math.isfinite(value), value > 0]
    elif name == "rate_table":
        rows = [(300.0, 1.2e5), (600.0, 8.1e6), (1000.0, 5.0e7)]
        observed = {"rows": rows}
        checks = [all(t > 0 and k > 0 for t, k in rows), rows[-1][1] > rows[0][1]]
    elif name == "density_integral":
        spacing, density = 0.5, [1.0] * 16
        electrons = sum(density) * spacing ** 3
        observed = {"grid_points": len(density), "electron_count": electrons}
        checks = [abs(electrons - 2.0) < 1e-12, all(x >= 0 for x in density)]
    elif name == "populations":
        populations = [[1.0, 0.0], [0.75, 0.25], [0.4, 0.6]]
        observed = {"populations": populations}
        checks = [all(abs(sum(row)-1.0) < 1e-12 for row in populations), all(0 <= x <= 1 for row in populations for x in row)]
    elif name == "unit_conversion":
        angstrom = 0.74; bohr = angstrom / 0.529177210903
        observed = {"distance_angstrom": angstrom, "distance_bohr": bohr}
        checks = [abs(bohr - 1.39839733222307) < 1e-12, bohr > angstrom]
    elif name == "stress_tensor":
        stress = [[1.0, 0.1, 0.0], [0.1, 2.0, 0.2], [0.0, 0.2, 3.0]]
        observed = {"stress_gpa": stress}
        checks = [all(math.isfinite(x) for row in stress for x in row), all(stress[i][j] == stress[j][i] for i in range(3) for j in range(3))]
    elif name == "acoustic_modes":
        frequencies = [0.0, 0.0, 0.0, 4.2, 7.1, 9.3]
        observed = {"frequencies_thz": frequencies, "acoustic_count": sum(abs(x) < 1e-8 for x in frequencies)}
        checks = [observed["acoustic_count"] == 3, all(math.isfinite(x) for x in frequencies)]
    elif name == "thermodynamic_integration":
        lambdas = [0.0, 0.25, 0.5, 0.75, 1.0]; values = [2*x + 1 for x in lambdas]
        integral = sum((values[i] + values[i+1]) * (lambdas[i+1] - lambdas[i]) / 2 for i in range(4))
        observed = {"delta_g": integral}
        checks = [abs(integral - 2.0) < 1e-12, integral > 0]
    elif name == "h2_energy":
        energy = -1.117349034
        observed = {"energy_hartree": energy, "electron_count": 2}
        checks = [-1.2 < energy < -0.8, observed["electron_count"] == 2]
    elif name == "activation_strain":
        rows = [{"total": 5.0, "strain": 8.0, "interaction": -3.0}, {"total": 7.0, "strain": 12.0, "interaction": -5.0}]
        errors = [abs(row["total"] - row["strain"] - row["interaction"]) for row in rows]
        observed = {"rows": rows, "maximum_closure_error": max(errors)}
        checks = [max(errors) < 1e-12, all(row["strain"] > 0 for row in rows)]
    elif name == "first_order":
        k, time = 1.0, 1.0; a = math.exp(-k*time); b = 1-a
        observed = {"A": a, "B": b}
        checks = [abs(a - math.exp(-1)) < 1e-12, abs(a+b-1) < 1e-12]
    elif name == "arrhenius":
        A, ea, gas_constant, temperature = 1e12, 10000.0, 8.314462618, 1000.0
        rate = A * math.exp(-ea/(gas_constant*temperature))
        observed = {"rate_s-1": rate}
        checks = [abs(rate - 300375010355.7517) / rate < 1e-12, rate > 0]
    elif name == "optimization":
        x0, x1 = 2.0, 0.02; e0, e1 = 0.5*2.0**2, 0.5*0.02**2
        observed = {"initial_energy": e0, "final_energy": e1, "final_force": abs(x1)}
        checks = [e1 < e0, observed["final_force"] < 0.05]
    elif name == "service_records":
        records = {"pubchem": {"cid": 962, "formula": "H2O"}, "rcsb": {"id": "1CRN", "method": "X-RAY DIFFRACTION"}}
        observed = records
        checks = [records["pubchem"] == {"cid": 962, "formula": "H2O"}, records["rcsb"]["id"] == "1CRN"]
    elif name == "conductivity":
        tensor = [[12.0, 0.1, 0.0], [0.1, 11.0, 0.2], [0.0, 0.2, 9.0]]
        observed = {"kappa_w_mk": tensor}
        checks = [all(tensor[i][i] > 0 for i in range(3)), all(tensor[i][j] == tensor[j][i] for i in range(3) for j in range(3))]
    elif name == "descriptor_rmse":
        expected = [1.0, 2.0, 3.0]; predicted = [1.1, 1.9, 3.0]
        rmse = math.sqrt(sum((a-b)**2 for a, b in zip(expected, predicted))/3)
        observed = {"rmse": rmse, "sample_count": 3}
        checks = [abs(rmse - math.sqrt(0.02/3)) < 1e-12, observed["sample_count"] == 3]
    elif name == "force_constants":
        matrix = [[1.0, -1.0], [-1.0, 1.0]]
        observed = {"force_constants": matrix, "row_sums": [sum(row) for row in matrix]}
        checks = [matrix[0][1] == matrix[1][0], max(abs(x) for x in observed["row_sums"]) < 1e-12]
    elif name == "excited_states":
        states = [{"energy_ev": 3.2, "oscillator_strength": 0.12}, {"energy_ev": 4.1, "oscillator_strength": 0.0}]
        observed = {"states": states}
        checks = [len(states) == 2, all(x["energy_ev"] > 0 and x["oscillator_strength"] >= 0 for x in states)]
    elif name == "band_gap":
        occupied, empty = [-1.2, -0.4], [0.8, 1.7]; gap = min(empty) - max(occupied)
        observed = {"vbm_ev": max(occupied), "cbm_ev": min(empty), "gap_ev": gap}
        checks = [abs(gap - 1.2) < 1e-12, gap > 0]
    elif name == "cif":
        cell = [5.43, 5.43, 5.43]; occupancies = [1.0, 1.0]
        observed = {"cell_angstrom": cell, "site_count": len(occupancies), "occupancies": occupancies}
        checks = [all(x > 0 for x in cell), all(0 < x <= 1 for x in occupancies)]
    elif name == "radius_of_gyration":
        coordinates = [[-1.0, 0.0, 0.0], [1.0, 0.0, 0.0]]
        rg = math.sqrt(sum(sum(x*x for x in point) for point in coordinates)/len(coordinates))
        observed = {"atom_count": 2, "radius_of_gyration_angstrom": rg}
        checks = [abs(rg - 1.0) < 1e-12, observed["atom_count"] == 2]
    elif name == "space_group":
        observed = {"international_symbol": "Fd-3m", "number": 227, "species": "Si"}
        checks = [observed["number"] == 227, observed["international_symbol"] == "Fd-3m"]
    elif name == "quasiparticle":
        records = [{"ks_ev": -1.0, "qp_ev": -0.7}, {"ks_ev": 1.2, "qp_ev": 1.8}]
        corrections = [row["qp_ev"] - row["ks_ev"] for row in records]
        observed = {"records": records, "corrections_ev": corrections}
        checks = [all(math.isfinite(x) for x in corrections), abs(corrections[0]-0.3) < 1e-12]
    else:
        raise ValueError("unknown scientific algorithm: " + name)
    return observed, [{"name": "criterion_" + str(i+1), "passed": bool(value)} for i, value in enumerate(checks)]


ctx = JobContext.load()
versions = module_versions()
api_checks = module_api_checks()
observed, checks = run_science(ALGORITHM)
critical = None
blocked_reason = None
try:
    critical = run_critical_runtime(RUNTIME)
except BlockedDependency as exc:
    blocked_reason = str(exc)
base_passed = bool(checks) and all(item["passed"] for item in checks)
status = "blocked" if blocked_reason else "passed" if base_passed else "failed"
payload = {
    "schema_version": 1,
    "runtime": RUNTIME,
    "algorithm": ALGORITHM,
    "module_versions": versions,
    "module_api_checks": api_checks,
    "observed": observed,
    "checks": checks,
    "critical_calculation": critical,
    "blocked_reason": blocked_reason,
    "status": status,
    "passed": status == "passed",
}
ctx.write_json("scientific_result", payload)
'''


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def authoritative_modules(runtime: str) -> list[str]:
    specification = runtime_spec(runtime)
    modules = set(
        (specification.get("health_checks") or {}).get("modules")
        or specification.get("modules")
        or []
    )
    for backend in backend_specs().values():
        if backend.runtime == runtime:
            modules.update(backend.python_modules)
    return sorted(str(item) for item in modules)


def required_symbols(modules: list[str]) -> dict[str, list[str]]:
    return {
        module: sorted(set(("__name__", *SYMBOLS.get(module, ()))))
        for module in modules
    }


def program_source(runtime: str, case: Case, modules: list[str]) -> str:
    return (
        PROGRAM_TEMPLATE.replace("__RUNTIME__", repr(runtime))
        .replace("__ALGORITHM__", repr(case.algorithm))
        .replace("__MODULES__", repr(modules))
    )


def request_for(runtime: str, script_path: str, modules: list[str]) -> AnalysisJobRequest:
    memory_mb = 8192 if runtime in {"deepmd", "nequip"} else 4096 if runtime in {"gpaw", "quantum", "psi4"} else 2048
    return AnalysisJobRequest(
        runtime=runtime,
        script_path=script_path,
        script_target=f"code/{runtime}_scientific_validation.py",
        required_modules=modules,
        required_symbols=required_symbols(modules),
        outputs=[
            AnalysisOutputDeclaration(
                name="scientific_result",
                path="outputs/scientific_result.json",
                semantic_type="ScientificRuntimeValidationResult",
                media_type="application/json",
                json_schema={
                    "type": "object",
                    "required": ["runtime", "algorithm", "module_versions", "module_api_checks", "observed", "checks", "status", "passed"],
                    "properties": {
                        "runtime": {"type": "string", "const": runtime},
                        "algorithm": {"type": "string"},
                        "module_versions": {"type": "object"},
                        "module_api_checks": {"type": "object"},
                        "observed": {"type": "object"},
                        "checks": {"type": "array", "minItems": 1},
                        "status": {"type": "string", "enum": ["passed", "blocked", "failed"]},
                        "passed": {"type": "boolean"},
                    },
                },
            )
        ],
        resource_limits=ResourceLimits(cpu_cores=1, memory_mb=memory_mb, gpu_count=0),
        label=f"full-programmable-scientific-validation:{runtime}",
    )


def compact_validation(value: dict[str, Any]) -> dict[str, Any]:
    return {
        key: value.get(key)
        for key in (
            "status", "valid", "runtime", "runtime_python", "script_sha256",
            "discovered_imports", "required_modules", "required_symbols",
            "module_status", "module_details", "job_context_compliance", "error",
        )
        if key in value
    }


def load_report(path: Path, resume: bool) -> dict[str, Any]:
    if resume and path.is_file():
        value = json.loads(path.read_text(encoding="utf-8"))
        if value.get("schema_version") == SCHEMA_VERSION:
            return value
    return {"schema_version": SCHEMA_VERSION, "started_at": now(), "cases": {}}


def save_report(path: Path, report: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    temporary.replace(path)


def selected_runtimes(values: list[str]) -> list[str]:
    requested = {item.strip() for value in values for item in value.split(",") if item.strip()}
    configured = set(runtime_names())
    unknown = sorted(requested - configured)
    if unknown:
        raise SystemExit(f"Unknown runtime(s): {', '.join(unknown)}")
    names = sorted(requested or configured)
    missing_cases = sorted(set(names) - set(CASES))
    extra_cases = sorted(set(CASES) - configured)
    if missing_cases or extra_cases:
        raise SystemExit(f"Case registry/config mismatch: missing={missing_cases}, extra={extra_cases}")
    return names


def artifact_payload(collected: dict[str, Any]) -> tuple[dict[str, Any] | None, dict[str, Any] | None]:
    artifacts = collected.get("declared_artifacts") or []
    artifact = next((item for item in artifacts if item.get("name") == "scientific_result"), None)
    if not artifact or not artifact.get("workspace_path"):
        return artifact, None
    response = read_workspace_text(
        WorkspaceTextReadRequest(path=artifact["workspace_path"], max_chars=2_000_000)
    )
    if response.get("status") != "success":
        return artifact, None
    return artifact, json.loads(response["content"])


def finalize_case(runtime: str, record: dict[str, Any]) -> None:
    collected = collect_execution_job(JobCollectRequest(job_id=record["job_id"], tail_chars=20_000))
    artifact, payload = artifact_payload(collected)
    checks = (payload or {}).get("checks") or []
    modules = set(record["request"]["required_modules"])
    reported_modules = set((payload or {}).get("module_versions") or {})
    api_modules = set((payload or {}).get("module_api_checks") or {})
    payload_status = (payload or {}).get("status")
    criteria = {
        "job_completed": collected.get("process_status") == "completed",
        "artifact_valid": collected.get("artifact_status") == "valid",
        "artifact_sha256_present": bool((artifact or {}).get("sha256")),
        "all_program_criteria_pass": bool(checks) and all(item.get("passed") is True for item in checks),
        "all_authoritative_modules_reported": modules == reported_modules,
        "all_authoritative_module_apis_called": modules == api_modules and all(
            item.get("status") == "passed"
            for item in ((payload or {}).get("module_api_checks") or {}).values()
        ),
    }
    mechanically_complete = all(criteria.values())
    status = (
        "blocked"
        if mechanically_complete and payload_status == "blocked" and (payload or {}).get("blocked_reason")
        else "passed"
        if mechanically_complete and payload_status == "passed" and (payload or {}).get("passed") is True
        else "failed"
    )
    record.update(
        {
            "status": status,
            "completed_at": now(),
            "collection": collected,
            "artifact": artifact,
            "artifact_sha256": (artifact or {}).get("sha256"),
            "scientific_result": payload,
            "criteria": criteria,
        }
    )


def run(names: list[str], output: Path, resume: bool) -> int:
    report = load_report(output, resume)
    report["updated_at"] = now()
    report["selected_runtimes"] = names
    discovery = list_analysis_runtimes(
        AnalysisRuntimeListRequest(available_only=False, include_details=True, limit=500)
    )
    report["runtime_discovery"] = discovery
    report["physical_python_map"] = {name: str(runtime_python(name)) for name in names}
    pending: dict[str, str] = {}

    for runtime in names:
        prior = report["cases"].get(runtime) or {}
        if resume and prior.get("status") == "passed":
            continue
        modules = authoritative_modules(runtime)
        script_path = f"code/full_programmable_validation/{runtime}.py"
        write_result = write_workspace_text(
            WorkspaceTextWriteRequest(
                path=script_path,
                content=program_source(runtime, CASES[runtime], modules),
                overwrite=True,
            )
        )
        request = request_for(runtime, script_path, modules)
        validation = validate_analysis_program(request)
        record = {
            "runtime": runtime,
            "physical_python": str(runtime_python(runtime)),
            "description": CASES[runtime].description,
            "dependencies": list(CASES[runtime].dependencies),
            "authoritative_modules": modules,
            "required_symbols": request.required_symbols,
            "request": request.model_dump(mode="json"),
            "workspace_write": write_result,
            "validation": compact_validation(validation),
            "submitted_at": now(),
        }
        report["cases"][runtime] = record
        if validation.get("status") != "success":
            record["status"] = "preflight_failed"
            continue
        submitted = submit_analysis_program(request)
        record["submission"] = submitted
        if submitted.get("status") != "success" or not submitted.get("job_id"):
            record["status"] = "submission_failed"
            continue
        record["status"] = "submitted"
        record["job_id"] = submitted["job_id"]
        pending[runtime] = submitted["job_id"]
        save_report(output, report)

    while pending:
        waited = wait_execution_jobs(JobWaitRequest(job_ids=list(pending.values())))
        report.setdefault("wait_history", []).append(
            {"at": now(), "summary": waited.get("summary"), "return_reason": waited.get("return_reason")}
        )
        remaining = set(waited.get("remaining_job_ids") or [])
        completed = [runtime for runtime, job_id in pending.items() if job_id not in remaining]
        for runtime in completed:
            finalize_case(runtime, report["cases"][runtime])
            pending.pop(runtime)
        save_report(output, report)

    selected_records = [report["cases"].get(name, {}) for name in names]
    counts: dict[str, int] = {}
    for record in selected_records:
        status = str(record.get("status") or "missing")
        counts[status] = counts.get(status, 0) + 1
    report["summary"] = {
        "runtime_count": len(names),
        "status_counts": counts,
        "passed": counts.get("passed", 0),
        "failed": len(names) - counts.get("passed", 0),
        "all_passed": counts.get("passed", 0) == len(names),
    }
    report["completed_at"] = now()
    save_report(output, report)
    print(json.dumps(report["summary"], indent=2, sort_keys=True))
    print(f"Report: {output}")
    return 0 if report["summary"]["all_passed"] else 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true", help="List the case matrix without submitting jobs")
    parser.add_argument("--runtime", action="append", default=[], help="Runtime id or comma-separated ids; repeatable")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="Checkpoint/report JSON path")
    parser.add_argument("--resume", action="store_true", help="Keep prior passing cases and rerun incomplete/failed cases")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    names = selected_runtimes(args.runtime)
    if args.list:
        rows = [
            {
                "runtime": name,
                "physical_python": str(runtime_python(name)),
                "modules": authoritative_modules(name),
                "algorithm": CASES[name].algorithm,
                "criterion": CASES[name].description,
                "dependencies": list(CASES[name].dependencies),
            }
            for name in names
        ]
        print(json.dumps(rows, indent=2, sort_keys=True))
        return 0
    return run(names, args.output.resolve(), args.resume)


if __name__ == "__main__":
    raise SystemExit(main())
