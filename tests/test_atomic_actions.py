from __future__ import annotations

from researchchem_toolbox.backends import data, docking, dynamics, electronic, periodic, reaction, structure
from researchchem_toolbox.catalog import action_specs
from researchchem_toolbox.service import execute_action


def test_every_public_action_has_a_handler_module():
    handled = set().union(
        structure.ACTIONS,
        electronic.ACTIONS,
        reaction.ACTIONS,
        dynamics.ACTIONS,
        periodic.ACTIONS,
        docking.ACTIONS,
        data.ACTIONS,
    )
    assert handled == set(action_specs())


def test_real_rdkit_artifact_chain_and_emt_energy(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    (tmp_path / "outputs").mkdir()
    standard = execute_action(
        "standardize_structure",
        {
            "backend_id": "rdkit",
            "inputs": {"structure": "CC(=O)[O-].[Na+]"},
            "method_spec": {},
            "action_settings": {
                "largest_fragment": True,
                "neutralize": False,
                "canonical_tautomer": False,
            },
        },
    )
    assert standard["status"] == "success"
    generated = execute_action(
        "generate_3d_structure",
        {
            "backend_id": "rdkit",
            "inputs": {"molecule": "O"},
            "method_spec": {},
            "action_settings": {"random_seed": 20260718},
        },
    )
    assert generated["status"] == "success"
    energy = execute_action(
        "calculate_energy",
        {
            "backend_id": "ase_emt",
            "inputs": {"structure": generated["result"]["structure"]},
            "method_spec": {},
            "action_settings": {},
        },
    )
    assert energy["status"] == "success"
    assert energy["result"]["unit"] == "eV"
    assert standard["output_artifacts"] and generated["output_artifacts"] and energy["output_artifacts"]


def test_deterministic_conformer_ranking(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    result = execute_action(
        "rank_conformers_from_results",
        {
            "backend_id": "internal_statistics",
            "inputs": {
                "ensemble": [
                    {"conformer_id": "a", "structure": {}},
                    {"conformer_id": "b", "structure": {}},
                ],
                "scores": [{"value": 0.0}, {"value": 1.0}],
            },
            "method_spec": {},
            "action_settings": {"temperature_kelvin": 298.15, "score_unit": "kcal_mol"},
        },
    )
    assert result["status"] == "success"
    assert result["result"]["ensemble"][0]["conformer_id"] == "a"
    assert abs(sum(item["weight"] for item in result["result"]["ensemble"]) - 1.0) < 1e-12


def test_unavailable_manual_backend_does_not_switch(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    result = execute_action(
        "calculate_energy",
        {
            "backend_id": "orca",
            "inputs": {"structure": {"atoms": [{"element": "H", "position_angstrom": [0, 0, 0]}]}},
            "method_spec": {"method": "HF", "basis": "STO-3G"},
            "action_settings": {},
        },
    )
    assert result["status"] == "unavailable"
    assert result["backend"] == result["requested_backend"] == "orca"
    assert result["provenance"]["automatic_fallback_count"] == 0
