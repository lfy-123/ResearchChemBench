from __future__ import annotations

from pathlib import Path

from researchchem_toolbox.backends import structure
from researchchem_toolbox.service import execute_action


def test_rdkit_descriptor_fingerprint_similarity_and_substructure_actions(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    (tmp_path / "outputs").mkdir()

    descriptors = execute_action(
        "calculate_molecular_descriptors",
        {
            "backend_id": "rdkit",
            "inputs": {"molecule": "CCO"},
            "method_spec": {},
            "action_settings": {"descriptor_names": ["MolWt", "TPSA", "MolLogP"]},
        },
    )
    assert descriptors["status"] == "success"
    assert set(descriptors["result"]["descriptors"]) == {"MolWt", "TPSA", "MolLogP"}

    fingerprint = execute_action(
        "calculate_molecular_fingerprint",
        {
            "backend_id": "rdkit",
            "inputs": {"molecule": "CCO"},
            "method_spec": {"fingerprint_type": "morgan"},
            "action_settings": {"radius": 2, "n_bits": 256, "use_chirality": True},
        },
    )
    assert fingerprint["status"] == "success"
    assert fingerprint["result"]["n_bits"] == 256
    assert fingerprint["result"]["bit_count"] > 0

    identical = execute_action(
        "calculate_molecular_similarity",
        {
            "backend_id": "rdkit",
            "inputs": {"molecule_a": "CCO", "molecule_b": "CCO"},
            "method_spec": {"fingerprint_type": "morgan", "similarity_metric": "tanimoto"},
            "action_settings": {"radius": 2, "n_bits": 256},
        },
    )
    assert identical["status"] == "success"
    assert identical["result"]["similarity"] == 1.0

    matches = execute_action(
        "search_local_substructures",
        {
            "backend_id": "rdkit",
            "inputs": {"molecule": "CCO", "query": "CO"},
            "method_spec": {"query_format": "smarts"},
            "action_settings": {"max_matches": 10, "unique": True, "use_chirality": True},
        },
    )
    assert matches["status"] == "success"
    assert matches["result"]["match_count"] == 1


def test_rdkit_tautomer_and_stereoisomer_enumeration_are_bounded(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    (tmp_path / "outputs").mkdir()

    tautomers = execute_action(
        "enumerate_tautomers",
        {
            "backend_id": "rdkit",
            "inputs": {"molecule": "O=C1NC=CC1"},
            "method_spec": {},
            "action_settings": {"max_tautomers": 32},
        },
    )
    assert tautomers["status"] == "success"
    assert 1 <= tautomers["result"]["count"] <= 32

    stereoisomers = execute_action(
        "enumerate_stereoisomers",
        {
            "backend_id": "rdkit",
            "inputs": {"molecule": "CC(F)Cl"},
            "method_spec": {},
            "action_settings": {
                "max_isomers": 8,
                "only_unassigned": True,
                "unique": True,
                "try_embedding": False,
            },
        },
    )
    assert stereoisomers["status"] == "success"
    assert stereoisomers["result"]["count"] == 2


def test_rdkit_conformer_clustering_and_explicit_alignment(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    generated = execute_action(
        "generate_conformer_ensemble",
        {
            "backend_id": "rdkit_etkdg",
            "inputs": {"molecule": "CCCO"},
            "method_spec": {},
            "action_settings": {
                "num_conformers": 8,
                "random_seed": 17,
                "prune_rms_threshold_angstrom": -1.0,
            },
        },
    )
    assert generated["status"] == "success"
    clustered = execute_action(
        "cluster_conformers",
        {
            "backend_id": "rdkit",
            "inputs": {"ensemble": generated["output_artifacts"][0]},
            "method_spec": {},
            "action_settings": {
                "rmsd_cutoff_angstrom": 0.5,
                "atom_selection": "heavy",
                "prealign_conformers": False,
                "reorder_cluster_centers": True,
            },
        },
    )
    assert clustered["status"] == "success"
    assert clustered["result"]["conformer_count"] == generated["result"]["count"]
    assert 1 <= clustered["result"]["cluster_count"] <= generated["result"]["count"]

    reference = generated["result"]["ensemble"][0]["structure"]
    probe = generated["result"]["ensemble"][1]["structure"]
    atom_map = [[index, index] for index in range(len(reference["atoms"]))]
    aligned = execute_action(
        "align_molecular_structures",
        {
            "backend_id": "rdkit",
            "inputs": {"reference": reference, "probe": probe, "atom_map": atom_map},
            "method_spec": {},
            "action_settings": {"reflect": False, "max_iterations": 100},
        },
    )
    assert aligned["status"] == "success"
    assert aligned["result"]["rmsd_angstrom"] >= 0.0
    assert len(aligned["result"]["aligned_probe"]["atoms"]) == len(probe["atoms"])


def test_rdkit_conformer_clustering_accepts_file_artifacts(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    (tmp_path / "outputs").mkdir()
    generated = execute_action(
        "generate_conformer_ensemble",
        {
            "backend_id": "rdkit_etkdg",
            "inputs": {"molecule": "CCCO"},
            "method_spec": {},
            "action_settings": {
                "num_conformers": 6,
                "random_seed": 17,
                "prune_rms_threshold_angstrom": -1.0,
            },
        },
    )
    sdf_artifact = next(
        artifact
        for artifact in generated["output_artifacts"]
        if artifact["media_type"] == "chemical/x-mdl-sdfile"
    )
    clustered = execute_action(
        "cluster_conformers",
        {
            "backend_id": "rdkit",
            "inputs": {"ensemble": sdf_artifact},
            "method_spec": {},
            "action_settings": {
                "rmsd_cutoff_angstrom": 0.5,
                "atom_selection": "heavy",
                "prealign_conformers": False,
                "reorder_cluster_centers": True,
            },
        },
    )
    assert clustered["status"] == "success"
    assert clustered["result"]["conformer_count"] == 6


def test_rdkit_conformer_clustering_accepts_multi_xyz(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    (tmp_path / "outputs").mkdir()
    xyz = tmp_path / "outputs" / "ensemble.xyz"
    xyz.write_text(
        "3\nconf-0\nO 0.0 0.0 0.0\nH 0.0 0.8 0.6\nH 0.0 -0.8 0.6\n"
        "3\nconf-1\nO 0.0 0.0 0.0\nH 0.0 0.9 0.5\nH 0.0 -0.9 0.5\n",
        encoding="utf-8",
    )
    clustered = execute_action(
        "cluster_conformers",
        {
            "backend_id": "rdkit",
            "inputs": {"ensemble": "outputs/ensemble.xyz"},
            "method_spec": {},
            "action_settings": {
                "rmsd_cutoff_angstrom": 0.5,
                "atom_selection": "all",
                "prealign_conformers": False,
                "reorder_cluster_centers": True,
            },
        },
    )
    assert clustered["status"] == "success"
    assert clustered["result"]["conformer_count"] == 2


def test_crest_accepts_common_method_alias_solvent_and_cpu_limit(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    (tmp_path / "outputs").mkdir()
    captured = {}

    def fake_run_external(**kwargs):
        captured.update(kwargs)
        source = Path(kwargs["directory"]) / "input.xyz"
        (Path(kwargs["directory"]) / "crest_conformers.xyz").write_text(
            source.read_text(encoding="utf-8"), encoding="utf-8"
        )
        return {
            "available": True,
            "returncode": 0,
            "stdout": "CREST terminated normally",
            "stderr": "",
            "command": ["crest", *kwargs["arguments"]],
        }

    monkeypatch.setattr(structure, "run_external", fake_run_external)
    result = execute_action(
        "generate_conformer_ensemble",
        {
            "backend_id": "crest",
            "inputs": {
                "molecule": "O",
                "initial_structure": {
                    "atoms": [
                        {"element": "O", "position_angstrom": [0.0, 0.0, 0.0]},
                        {"element": "H", "position_angstrom": [0.0, 0.8, 0.6]},
                        {"element": "H", "position_angstrom": [0.0, -0.8, 0.6]},
                    ],
                    "charge": 0,
                    "multiplicity": 1,
                }
            },
            "method_spec": {
                "method": "GFN2-xTB",
                "solvation_model": "ALPB",
                "solvent": "water",
            },
            "action_settings": {"energy_window_kcal_mol": 6.0},
            "resource_limits": {"cpu_cores": 8, "walltime_seconds": 300},
        },
    )
    assert result["status"] == "success"
    assert "--gfn2" in captured["arguments"]
    assert captured["arguments"][-4:] == ["--ewin", "6.0", "--T", "8"]
    alpb_index = captured["arguments"].index("--alpb")
    assert captured["arguments"][alpb_index : alpb_index + 2] == ["--alpb", "water"]
    assert captured["environment_overrides"]["OMP_NUM_THREADS"] == "8"
