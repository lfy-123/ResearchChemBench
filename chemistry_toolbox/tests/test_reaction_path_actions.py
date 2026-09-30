from __future__ import annotations

import math

import pytest

from chemistry_toolbox.src.backends import reaction, structure
from chemistry_toolbox.src.catalog import action_specs, validate_catalog


H2_REACTANT = {
    "atoms": [
        {"element": "H", "position_angstrom": [0.0, 0.0, 0.0]},
        {"element": "H", "position_angstrom": [0.8, 0.0, 0.0]},
    ],
    "charge": 0,
    "multiplicity": 1,
}
H2_PRODUCT = {
    "atoms": [
        {"element": "H", "position_angstrom": [0.0, 0.0, 0.0]},
        {"element": "H", "position_angstrom": [1.2, 0.0, 0.0]},
    ],
    "charge": 0,
    "multiplicity": 1,
}


def test_reaction_path_actions_are_reciprocal_and_ts_action_no_longer_claims_endpoints():
    validate_catalog()
    specs = action_specs()
    assert specs["locate_transition_state"].optional_inputs == ()
    assert specs["search_reaction_path"].required_inputs == ("reactant", "product")
    assert specs["scan_reaction_coordinates"].required_inputs == ("structure",)
    assert specs["validate_reaction_path"].selection_policy == "internal_deterministic"
    assert specs["analyze_reaction_coordinate"].selection_policy == "internal_deterministic"


def test_double_ended_pysis_action_consumes_both_endpoints_and_parses_energies(
    tmp_path, monkeypatch
):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))

    def fake_run_external(**kwargs):
        (kwargs["directory"] / "final_geometries.trj").write_text(
            "2\n-1.00 , \nH 0 0 0\nH 0.8 0 0\n"
            "2\n-0.95 , \nH 0 0 0\nH 1.0 0 0\n"
            "2\n-1.01 , \nH 0 0 0\nH 1.2 0 0\n",
            encoding="utf-8",
        )
        return {
            "available": True,
            "returncode": 0,
            "stdout": "Converged!\n",
            "stderr": "",
            "command": ["pysis", "pysis.yaml"],
        }

    monkeypatch.setattr(reaction, "run_external", fake_run_external)
    result = reaction._pysisyphus(
        "search_reaction_path",
        {
            "inputs": {"reactant": H2_REACTANT, "product": H2_PRODUCT},
            "method_spec": {
                "calculator_backend": "xtb",
                "method": "GFN2-xTB",
                "solvation_model": "alpb",
                "solvent": "methanol",
            },
            "action_settings": {
                "path_method": "neb",
                "interpolation": "linear",
                "images": 3,
                "optimizer": "qm",
                "convergence": "gau_loose",
                "max_cycles": 10,
                "climb": False,
            },
            "resource_limits": {"cpu_cores": 4,},
        },
    )

    assert result["status"] == "success"
    assert result["result"]["endpoints_consumed"] is True
    assert result["result"]["energies_hartree"] == [-1.0, -0.95, -1.01]
    assert result["result"]["highest_interior_energy_image_index"] == 1
    configuration = result["provenance"]["generated_config"]
    assert len(configuration["geom"]["fn"]) == 2
    assert configuration["calc"]["alpb"] == "methanol"
    assert configuration["calc"]["pal"] == 4


def test_growing_string_rejects_optimizer_that_cannot_resize_history(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    with pytest.raises(ValueError, match="requires optimizer=string"):
        reaction._pysisyphus(
            "search_reaction_path",
            {
                "inputs": {"reactant": H2_REACTANT, "product": H2_PRODUCT},
                "method_spec": {"calculator_backend": "xtb", "method": "gfn2"},
                "action_settings": {
                    "path_method": "growing_string",
                    "interpolation": "linear",
                    "images": 4,
                    "optimizer": "qm",
                    "convergence": "gau_loose",
                    "max_cycles": 10,
                    "climb": False,
                },
            },
        )


def test_pysisyphus_xtb_rejects_unparametrized_ethanol_before_execution():
    with pytest.raises(ValueError, match="ethanol.*not parametrized"):
        reaction._pysisyphus_calculator(
            {
                "calculator_backend": "xtb",
                "method": "GFN2-xTB",
                "solvation_model": "gbsa",
                "solvent": "ethanol",
            },
            H2_REACTANT,
            {"cpu_cores": 2},
        )


def test_pysisyphus_xtb_accepts_supported_model_specific_solvent():
    calculator, charge, multiplicity = reaction._pysisyphus_calculator(
        {
            "calculator_backend": "xtb",
            "method": "GFN2-xTB",
            "solvation_model": "gbsa",
            "solvent": "DMF",
        },
        H2_REACTANT,
        {"cpu_cores": 2},
    )
    assert calculator["gbsa"] == "dmf"
    assert charge == 0
    assert multiplicity == 1


def test_relaxed_scan_converts_angstrom_to_bohr_and_returns_aligned_points(
    tmp_path, monkeypatch
):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))

    def fake_run_external(**kwargs):
        (kwargs["directory"] / "relaxed_scan.dat").write_text(
            "1.7007535129 -1.0\n1.8897261255 -0.9\n", encoding="utf-8"
        )
        (kwargs["directory"] / "relaxed_scan.trj").write_text(
            "2\n\nH 0 0 0\nH 0.9 0 0\n"
            "2\n\nH 0 0 0\nH 1.0 0 0\n",
            encoding="utf-8",
        )
        return {
            "available": True,
            "returncode": 0,
            "stdout": "| RUNNING STEP 00, COORD=1.7008 AU |\nConverged!\n"
            "| RUNNING STEP 01, COORD=1.8897 AU |\nConverged!\n",
            "stderr": "",
            "command": ["pysis", "pysis.yaml"],
        }

    monkeypatch.setattr(reaction, "run_external", fake_run_external)
    result = reaction._pysisyphus(
        "scan_reaction_coordinates",
        {
            "inputs": {"structure": H2_REACTANT},
            "method_spec": {"calculator_backend": "xtb", "method": "gfn2"},
            "action_settings": {
                "coordinate_type": "bond",
                "atom_indices": [0, 1],
                "start_value": 0.9,
                "end_value": 1.0,
                "value_unit": "angstrom",
                "steps": 1,
                "optimizer": "rfo",
                "convergence": "gau_loose",
                "max_cycles": 10,
                "hessian_init": "fischer",
            },
        },
    )

    assert result["status"] == "success"
    assert result["result"]["coordinate_values"] == pytest.approx([0.9, 1.0])
    assert result["result"]["energies_hartree"] == [-1.0, -0.9]
    assert result["result"]["target_values"] == pytest.approx([0.9, 1.0])
    assert result["result"]["points"][1]["delta"] == pytest.approx(0.0, abs=1e-9)
    assert result["result"]["points"][0]["native"]["status"] == "converged"
    scan = result["provenance"]["generated_config"]["scan"]
    assert scan["start"] == pytest.approx(0.9 * 1.8897261254578281)
    assert scan["end"] == pytest.approx(1.0 * 1.8897261254578281)
    assert result["provenance"]["generated_config"]["geom"]["coord_kwargs"] == {
        "define_prims": [["BOND", 0, 1]]
    }


def test_internal_coordination_and_path_analysis_actions():
    enumeration = structure.execute(
        "enumerate_coordination_isomers",
        "internal_reaction_analysis",
        {
            "inputs": {
                "structure": {
                    "atoms": [
                        {"element": "P", "position_angstrom": [0, 0, 0]},
                        *[
                            {"element": "C", "position_angstrom": [index, 0, 0]}
                            for index in range(1, 6)
                        ],
                    ]
                },
                "coordination_center_index": 0,
                "ligand_anchor_indices": [1, 2, 3, 4, 5],
                "ligand_labels": ["A", "B", "B", "C", "C"],
            },
            "action_settings": {
                "coordination_geometry": "trigonal_bipyramidal",
                "max_isomers": 20,
            },
        },
    )
    assert enumeration["status"] == "success"
    assert enumeration["result"]["coordinates_generated"] is False
    assert enumeration["result"]["isomer_count"] == 5

    middle = {
        "atoms": [
            {"element": "H", "position_angstrom": [0.0, 0.0, 0.0]},
            {"element": "H", "position_angstrom": [1.0, 0.0, 0.0]},
        ],
        "charge": 0,
        "multiplicity": 1,
    }
    path = {"structures": [H2_REACTANT, middle, H2_PRODUCT]}
    validation = reaction.execute(
        "validate_reaction_path",
        "internal_reaction_analysis",
        {
            "inputs": {
                "path": path,
                "reactant": H2_REACTANT,
                "product": H2_PRODUCT,
                "bond_changes": [{"type": "break", "atom_indices": [0, 1]}],
            },
            "action_settings": {
                "endpoint_rmsd_tolerance_angstrom": 0.01,
                "maximum_image_step_rmsd_angstrom": 0.3,
                "bond_distance_tolerance_angstrom": 0.2,
            },
        },
    )
    assert validation["status"] == "success"
    assert validation["result"]["valid"] is True

    analysis = reaction.execute(
        "analyze_reaction_coordinate",
        "internal_reaction_analysis",
        {
            "inputs": {"path": path, "energies": [-1.0, -0.9, -1.1]},
            "action_settings": {"energy_unit": "hartree"},
        },
    )
    assert analysis["status"] == "success"
    assert analysis["result"]["highest_energy_image_index"] == 1
    assert math.isclose(
        analysis["result"]["highest_energy_relative_kcal_mol"],
        0.2 * 627.5094740631,
    )
    assert analysis["result"]["transition_state_validated"] is False
