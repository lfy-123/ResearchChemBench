from __future__ import annotations

import os
import shutil
from pathlib import Path

from chemistry_toolbox.src.backends import structure
from chemistry_toolbox.src.service import execute_action


ROOT = Path(__file__).resolve().parents[2]
RUNTIME = ROOT / ".envs" / "molecular-simulation-openff"
PMX = RUNTIME / "bin" / "pmx"
GMXLIB = RUNTIME / "lib" / "python3.12" / "site-packages" / "pmx" / "data" / "mutff"
SOURCE = ROOT / ".software_cache" / "sources" / "pmx" / "develop-0dd5f0a"
ALCHEMY = SOURCE / "tests" / "data" / "alchemy"


def _execute(action_id: str, backend_id: str, request: dict) -> dict:
    payload = {"backend_id": backend_id, **request}
    payload["resource_limits"] = dict(request.get("resource_limits") or {})
    payload["resource_limits"].pop("walltime_seconds", None)
    return execute_action(action_id, payload)
LIGANDS = SOURCE / "protLig_benchmark" / "ptp1b" / "ligands_gaff2"


def _configure_runtime(monkeypatch) -> None:
    monkeypatch.setenv("CHEMGRAPH_PMX_COMMAND", str(PMX))
    monkeypatch.setenv("GMXLIB", str(GMXLIB))
    monkeypatch.setenv("PATH", f"{RUNTIME / 'bin'}:{os.environ.get('PATH', '')}")
    monkeypatch.setenv("LD_LIBRARY_PATH", f"{RUNTIME / 'lib'}:{os.environ.get('LD_LIBRARY_PATH', '')}")


def _mutation_request(path: Path) -> dict:
    return {
        "inputs": {
            "structure": str(path),
            "mutations": [{"residue_id": 6, "target_residue_name": "F"}],
        },
        "method_spec": {"force_field": "amber99sb-star-ildn-mut"},
        "action_settings": {"keep_residue_ids": False},
        "resource_limits": {"cpu_cores": 1, "walltime_seconds": 60},
    }


def test_pmx_mutates_real_upstream_protein_fixture(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    _configure_runtime(monkeypatch)
    protein = Path(shutil.copy2(ALCHEMY / "protein.pdb", tmp_path / "protein.pdb"))
    result = _execute(
        "mutate_biomolecular_residues_for_alchemy", "pmx", _mutation_request(protein)
    )
    assert result["status"] == "success"
    assert result["backend_version"] == "0+untagged.1.g0dd5f0a"
    hybrid = tmp_path / result["result"]["structure_file"]
    assert hybrid.is_file()
    assert "W2F" in hybrid.read_text(encoding="utf-8")
    assert result["result"]["parameterized"] is False


def test_pmx_generates_real_b_state_hybrid_topology(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    _configure_runtime(monkeypatch)
    topology = Path(shutil.copy2(ALCHEMY / "topol.top", tmp_path / "topol.top"))
    result = _execute(
        "generate_alchemical_hybrid_topology",
        "pmx",
        {
            "inputs": {"topology_file": str(topology)},
            "method_spec": {"force_field": "amber99sb-star-ildn-mut"},
            "action_settings": {
                "recursive": False,
                "split_transformations": False,
                "dummy_mass_scale": 0.33,
                "dummy_dihedral_scale": 1.0,
            },
            "resource_limits": {"cpu_cores": 1, "walltime_seconds": 60},
        },
    )
    assert result["status"] == "success"
    hybrid = tmp_path / result["result"]["hybrid_topology_path"]
    text = hybrid.read_text(encoding="utf-8")
    assert "typeB" in text
    assert "W2F" in text


def test_pmx_maps_real_ligand_pair(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    _configure_runtime(monkeypatch)
    ligand_a = Path(shutil.copy2(LIGANDS / "lig_23466" / "mol_gmx.pdb", tmp_path / "ligand_a.pdb"))
    ligand_b = Path(shutil.copy2(LIGANDS / "lig_23467" / "mol_gmx.pdb", tmp_path / "ligand_b.pdb"))
    result = _execute(
        "map_alchemical_ligand_atoms",
        "pmx",
        {
            "inputs": {"ligand_a": str(ligand_a), "ligand_b": str(ligand_b)},
            "method_spec": {},
            "action_settings": {
                "use_alignment": True,
                "use_mcs": True,
                "map_nonpolar_hydrogens": True,
                "map_polar_hydrogens": False,
                "allow_hydrogen_to_heavy": False,
                "rings_only": False,
                "apply_distance_to_mcs": False,
                "cross_check_swapped_order": False,
                "check_chirality": True,
                "distance_cutoff_nm": 0.05,
                "mcs_timeout_seconds": 10,
            },
            "resource_limits": {"cpu_cores": 1, "walltime_seconds": 60},
        },
    )
    assert result["status"] == "success"
    assert result["result"]["mapped_atom_count"] == 27
    assert result["result"]["dissimilarity_score"] == 0.1818


def test_pmx_dispatches_through_unified_service(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    protein = Path(shutil.copy2(ALCHEMY / "protein.pdb", tmp_path / "protein.pdb"))
    request = _mutation_request(protein)
    request["resource_limits"].pop("walltime_seconds")
    result = execute_action(
        "mutate_biomolecular_residues_for_alchemy",
        {"backend_id": "pmx", **request},
    )
    assert result["status"] == "success"
    assert result["backend_version"] == "0+untagged.1.g0dd5f0a"
