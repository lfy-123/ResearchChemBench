from __future__ import annotations

import importlib
import json
import os
from pathlib import Path
from types import SimpleNamespace


ORIGINAL_TOOLS = {
    "calculator",
    "extract_output_json",
    "molecule_name_to_smiles",
    "run_ase",
    "smiles_to_coordinate_file",
}

EXPECTED_WORKING = {
    "analyze_md_trajectory",
    "analyze_wavefunction",
    "calculator",
    "check_backend_availability",
    "convert_structure",
    "extract_output_json",
    "generate_3d_structure",
    "generate_conformers_crest",
    "generate_conformers_rdkit",
    "list_toolbox_capabilities",
    "molecule_name_to_smiles",
    "prepare_md_system",
    "query_catalysis_hub",
    "query_pubchem",
    "query_rcsb_pdb",
    "run_ase",
    "run_cantera",
    "run_mlip",
    "run_openmm",
    "run_phonopy",
    "run_psi4",
    "run_pyscf",
    "run_reaction_kinetics",
    "run_xtb",
    "smiles_to_coordinate_file",
    "standardize_molecule",
    "validate_computation",
}

LIVE_NETWORK = os.environ.get("RESEARCHCHEM_LIVE_NETWORK_TESTS", "").lower() in {
    "1",
    "true",
    "yes",
}


class CaptureMCP:
    def __init__(self) -> None:
        self.function = None
        self.name = None

    def tool(self, *args, **kwargs):
        def decorator(function):
            assert self.function is None, "one tool file must register exactly one public MCP function"
            self.function = function
            self.name = kwargs.get("name") or function.__name__
            return function

        if args and callable(args[0]):
            return decorator(args[0])
        return decorator


def _write_xyz(root: Path) -> str:
    path = root / "data" / "water.xyz"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "3\nwater\n"
        "O 0.000000 0.000000 0.000000\n"
        "H 0.758602 0.000000 0.504284\n"
        "H -0.758602 0.000000 0.504284\n",
        encoding="utf-8",
    )
    return "data/water.xyz"


def _write_pdb(root: Path) -> str:
    path = root / "data" / "water.pdb"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "HETATM    1  O   HOH A   1       0.000   0.000   0.000  1.00  0.00           O  \n"
        "HETATM    2  H1  HOH A   1       0.758   0.000   0.504  1.00  0.00           H  \n"
        "HETATM    3  H2  HOH A   1      -0.758   0.000   0.504  1.00  0.00           H  \n"
        "TER\nEND\n",
        encoding="utf-8",
    )
    return "data/water.pdb"


def _write_periodic(root: Path) -> str:
    path = root / "data" / "silicon.vasp"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "Si\n1.0\n"
        "5.43 0 0\n0 5.43 0\n0 0 5.43\n"
        "Si\n1\nDirect\n0 0 0\n",
        encoding="utf-8",
    )
    return "data/silicon.vasp"


def _write_dummy(root: Path) -> str:
    path = root / "data" / "input.inp"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("test input\n", encoding="utf-8")
    return "data/input.inp"


def _call_original(name: str, module, root: Path, monkeypatch):
    if name == "molecule_name_to_smiles" and not LIVE_NETWORK:
        module.ensure_chemgraph_on_path()
        chemistry = importlib.import_module("chemgraph.tools.cheminformatics_core")
        monkeypatch.setattr(
            chemistry,
            "molecule_name_to_smiles_core",
            lambda molecule_name: "O=S=O" if molecule_name == "sulfur dioxide" else "O",
        )

    capture = CaptureMCP()
    module.register(capture)
    assert capture.name == name
    assert callable(capture.function)
    function = capture.function

    if name == "calculator":
        value = function("(2 + 3) * 4")
        assert value == "20"
        return {"status": "success", "value": value}

    if name == "extract_output_json":
        result_path = root / "outputs" / "original_result.json"
        result_path.write_text(json.dumps({"energy": -1.0}), encoding="utf-8")
        value = function("outputs/original_result.json")
        assert value["energy"] == -1.0
        return {"status": "success", "value": value}

    if name == "molecule_name_to_smiles":
        value = function("sulfur dioxide")
        assert value == "O=S=O"
        return {"status": "success", "value": value}

    if name == "smiles_to_coordinate_file":
        result = function("O", "outputs/original_water.xyz", 2025, "xyz")
        assert (root / "outputs" / "original_water.xyz").is_file()
        return result

    if name == "run_ase":
        _write_xyz(root)
        params = module.ASEInputSchema.model_validate(
            {
                "input_structure_file": "data/water.xyz",
                "output_results_file": "outputs/ase_energy.json",
                "driver": "energy",
                "calculator": {"calculator_type": "emt"},
            }
        )
        result = function(params)
        assert (root / "outputs" / "ase_energy.json").is_file()
        return result

    raise AssertionError(f"No original-tool case for {name}")


def _configure_network_mock(name: str, module, monkeypatch) -> None:
    if LIVE_NETWORK:
        return
    if name == "query_pubchem":
        import pubchempy

        compound = SimpleNamespace(
            cid=962,
            canonical_smiles="O",
            isomeric_smiles="O",
            inchi="InChI=1S/H2O/h1H2",
            inchikey="XLYOFNOQVPJJNP-UHFFFAOYSA-N",
            molecular_formula="H2O",
            molecular_weight=18.015,
            iupac_name="oxidane",
        )
        monkeypatch.setattr(pubchempy, "get_compounds", lambda *_args, **_kwargs: [compound])
    elif name == "query_rcsb_pdb":
        monkeypatch.setattr(
            module,
            "get_json",
            lambda _url: {
                "struct": {"title": "Crambin"},
                "rcsb_entry_info": {"resolution_combined": [1.5]},
                "rcsb_accession_info": {},
                "exptl": [{"method": "X-RAY DIFFRACTION"}],
            },
        )
    elif name == "query_catalysis_hub":
        monkeypatch.setattr(
            module,
            "post_json",
            lambda *_args, **_kwargs: {
                "data": {"reactions": {"totalCount": 0, "edges": []}}
            },
        )


def _call_core(name: str, module, root: Path, monkeypatch):
    core = getattr(module, f"{name}_core")
    xyz = _write_xyz(root)
    pdb = _write_pdb(root)
    periodic = _write_periodic(root)
    dummy = _write_dummy(root)
    _configure_network_mock(name, module, monkeypatch)

    if name == "list_toolbox_capabilities":
        return core()
    if name == "check_backend_availability":
        result = core("RDKit")
        assert result["available"] is True
        assert core("Newton-X")["available"] is False
        return result
    if name == "standardize_molecule":
        return core("CCO")
    if name == "convert_structure":
        return core(xyz, "outputs/water_copy.xyz")
    if name == "generate_3d_structure":
        return core("O", "outputs/generated.sdf", 2025)
    if name == "generate_conformers_rdkit":
        return core("CCO", "outputs/conformers.sdf", 3, 2025)
    if name == "query_pubchem":
        return core("water", "name", 1)
    if name == "query_rcsb_pdb":
        return core("1CRN")
    if name == "query_catalysis_hub":
        return core("CO", "CO2", 1)
    if name == "query_materials_project":
        monkeypatch.delenv("MP_API_KEY", raising=False)
        return core(material_id="mp-149", max_records=1)
    if name == "run_reaction_kinetics":
        return core(["A", "B"], [1.0, 0.0], [[1, 0]], [[0, 1]], [1.0], 1.0, 5)
    if name == "validate_computation":
        result_path = root / "outputs" / "validation_input.json"
        result_path.write_text(json.dumps({"status": "success", "energy": -1.0}), encoding="utf-8")
        return core("outputs/validation_input.json", ["energy"], [])
    if name == "run_pyscf":
        return core("H 0 0 0; H 0 0 0.74", output_file="outputs/pyscf.json")
    if name == "run_psi4":
        return core(
            "0 1\nH 0 0 0\nH 0 0 0.74\nunits angstrom",
            output_file="outputs/psi4.json",
        )
    if name == "analyze_wavefunction":
        from evaluation.mcp_tools.tools.run_xtb import run_xtb_core

        xtb = run_xtb_core(xyz, output_directory="outputs/analyze_xtb", timeout_seconds=180)
        assert xtb["status"] == "success"
        return core("outputs/analyze_xtb/stdout.log")
    if name in {
        "find_transition_state",
        "run_irc",
        "run_orca",
        "run_cp2k",
        "run_quantum_espresso",
        "run_lammps",
        "run_catmap",
    }:
        return core(dummy)
    if name == "generate_conformers_crest":
        return core(xyz, output_directory="outputs/crest", timeout_seconds=180)
    if name == "refine_ensemble_censo":
        return core(xyz)
    if name == "run_xtb":
        return core(xyz, output_directory="outputs/xtb", timeout_seconds=180)
    if name == "compute_thermochemistry":
        return core(dummy)
    if name == "run_periodic_calculation":
        return core("cp2k", dummy)
    if name == "run_gromacs":
        return core(dummy)
    if name == "run_plumed":
        return core(dummy)
    if name == "run_phonopy":
        return core(periodic, output_directory="outputs/phonopy", timeout_seconds=120)
    if name == "run_docking":
        return core(dummy, dummy, [0, 0, 0], [10, 10, 10])
    if name == "prepare_md_system":
        return core(pdb, "outputs/prepared.pdb")
    if name == "run_openmm":
        return core(pdb, force_fields=["tip3p.xml"], steps=0)
    if name == "analyze_md_trajectory":
        return core(pdb, max_frames=1)
    if name == "run_cantera":
        return core("H2:2,O2:1,N2:3.76", temperature_kelvin=1000.0)
    if name == "run_mlip":
        return core(periodic, "chgnet", device="cpu", allow_model_download=True)
    raise AssertionError(f"No runtime test case configured for {name}")


def assert_tool_runtime(name: str, tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    monkeypatch.setenv("RESEARCHCHEMBENCH_RUN_ID", f"pytest-{name}")
    (tmp_path / "outputs").mkdir(parents=True, exist_ok=True)

    module = importlib.import_module(f"evaluation.mcp_tools.tools.{name}")
    assert module.TOOL_SPEC.name == name
    module.TOOL_SPEC.validate()
    assert callable(module.register)

    capture = CaptureMCP()
    module.register(capture)
    assert capture.name == name
    assert callable(capture.function)

    if name in ORIGINAL_TOOLS:
        result = _call_original(name, module, tmp_path, monkeypatch)
    else:
        result = _call_core(name, module, tmp_path, monkeypatch)

    if isinstance(result, dict):
        status = str(result.get("status", "success"))
    else:
        status = "success"

    if name in EXPECTED_WORKING:
        assert status in {"success", "available"}, (
            f"{name} was expected to work in its MCP profile but returned {status}: {result}"
        )
    else:
        assert status in {"unavailable", "error"}, (
            f"{name} should return a structured unavailable/error state until its backend is configured: {result}"
        )
