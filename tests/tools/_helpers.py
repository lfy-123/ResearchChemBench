from __future__ import annotations

import importlib
import json
from pathlib import Path


STRUCTURAL_ONLY = {
    "calculator",
    "extract_output_json",
    "molecule_name_to_smiles",
    "run_ase",
    "smiles_to_coordinate_file",
}

EXTERNAL_COMMAND_TOOLS = {
    "compute_thermochemistry",
    "find_transition_state",
    "generate_conformers_crest",
    "refine_ensemble_censo",
    "run_catmap",
    "run_cp2k",
    "run_docking",
    "run_gromacs",
    "run_irc",
    "run_lammps",
    "run_orca",
    "run_periodic_calculation",
    "run_phonopy",
    "run_plumed",
    "run_quantum_espresso",
    "run_xtb",
}


def _write_xyz(root: Path) -> Path:
    path = root / "data" / "water.xyz"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "3\nwater\nO 0.000000 0.000000 0.000000\nH 0.758602 0.000000 0.504284\nH -0.758602 0.000000 0.504284\n",
        encoding="utf-8",
    )
    return path


def _write_pdb(root: Path) -> Path:
    path = root / "data" / "water.pdb"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "HETATM    1  O   HOH A   1       0.000   0.000   0.000  1.00  0.00           O  \n"
        "HETATM    2  H1  HOH A   1       0.758   0.000   0.504  1.00  0.00           H  \n"
        "HETATM    3  H2  HOH A   1      -0.758   0.000   0.504  1.00  0.00           H  \n"
        "TER\nEND\n",
        encoding="utf-8",
    )
    return path


def assert_tool_smoke(name: str, tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    (tmp_path / "outputs").mkdir(exist_ok=True)
    module = importlib.import_module(f"evaluation.mcp_tools.tools.{name}")
    assert module.TOOL_SPEC.name == name
    module.TOOL_SPEC.validate()
    assert callable(module.register)
    if name in STRUCTURAL_ONLY:
        return

    core = getattr(module, f"{name}_core")
    if name in EXTERNAL_COMMAND_TOOLS:
        monkeypatch.setattr(
            module,
            "run_external",
            lambda **kwargs: {"status": "success", "backend": kwargs["backend"], "simulated": True},
        )

    xyz = _write_xyz(tmp_path)
    pdb = _write_pdb(tmp_path)
    dummy = tmp_path / "data" / "input.inp"
    dummy.write_text("test input\n", encoding="utf-8")

    if name == "list_toolbox_capabilities":
        result = core()
    elif name == "check_backend_availability":
        result = core("RDKit")
    elif name == "standardize_molecule":
        result = core("CCO")
    elif name == "convert_structure":
        result = core("data/water.xyz", "outputs/water_copy.xyz")
    elif name == "generate_3d_structure":
        result = core("O", "outputs/generated.sdf", 2025)
    elif name == "generate_conformers_rdkit":
        result = core("CCO", "outputs/conformers.sdf", 3, 2025)
    elif name == "query_rcsb_pdb":
        monkeypatch.setattr(module, "get_json", lambda _url: {"struct": {"title": "test"}, "rcsb_entry_info": {}})
        result = core("1CRN")
    elif name == "query_catalysis_hub":
        monkeypatch.setattr(module, "post_json", lambda *_args, **_kwargs: {"data": {"reactions": {"totalCount": 0, "edges": []}}})
        result = core("CO", "CO2", 2)
    elif name == "query_materials_project":
        monkeypatch.delenv("MP_API_KEY", raising=False)
        result = core(material_id="mp-149")
    elif name == "query_pubchem":
        monkeypatch.setattr(module, "module_available", lambda _name: False)
        result = core("water")
    elif name == "run_reaction_kinetics":
        result = core(["A", "B"], [1.0, 0.0], [[1, 0]], [[0, 1]], [1.0], 1.0, 5)
    elif name == "validate_computation":
        result_path = tmp_path / "outputs" / "result.json"
        result_path.write_text(json.dumps({"status": "success", "energy": -1.0}), encoding="utf-8")
        result = core("outputs/result.json", ["energy"], [])
    elif name == "run_pyscf":
        result = core("H 0 0 0; H 0 0 0.74", output_file="outputs/pyscf.json")
    elif name == "run_psi4":
        result = core("0 1\nH 0 0 0\nH 0 0 0.74\nunits angstrom", output_file="outputs/psi4.json")
    elif name == "analyze_wavefunction":
        monkeypatch.setattr(module, "module_available", lambda _name: False)
        result = core("data/input.inp")
    elif name in {"find_transition_state", "run_irc", "run_orca", "run_cp2k", "run_quantum_espresso", "run_lammps", "run_catmap"}:
        result = core("data/input.inp")
    elif name == "generate_conformers_crest":
        result = core("data/water.xyz")
    elif name == "refine_ensemble_censo":
        result = core("data/water.xyz")
    elif name == "run_xtb":
        result = core("data/water.xyz")
    elif name == "compute_thermochemistry":
        result = core("data/input.inp")
    elif name == "run_periodic_calculation":
        result = core("cp2k", "data/input.inp")
    elif name == "run_gromacs":
        result = core("data/input.inp")
    elif name == "run_plumed":
        result = core("data/input.inp")
    elif name == "run_phonopy":
        result = core("data/water.xyz")
    elif name == "run_docking":
        result = core("data/input.inp", "data/input.inp", [0, 0, 0], [10, 10, 10])
    elif name == "prepare_md_system":
        result = core("data/water.pdb", "outputs/prepared.pdb")
    elif name == "run_openmm":
        result = core("data/water.pdb", force_fields=["tip3p.xml"], steps=0)
    elif name == "analyze_md_trajectory":
        result = core("data/water.pdb", max_frames=1)
    elif name == "run_cantera":
        result = core("H2:2,O2:1,N2:3.76", temperature_kelvin=1000.0)
    elif name == "run_mlip":
        result = core("data/water.xyz", "nequip")
    else:
        raise AssertionError(f"No smoke case configured for {name}")

    assert isinstance(result, dict)
    assert result.get("status") in {"success", "available", "unavailable", "error", "unknown"}

