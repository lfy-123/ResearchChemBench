from __future__ import annotations

from researchchem_toolbox.service import execute_action


WATER = {
    "atoms": [
        {"element": "O", "position_angstrom": [0.0, 0.0, 0.0]},
        {"element": "H", "position_angstrom": [0.96, 0.0, 0.0]},
        {"element": "H", "position_angstrom": [-0.24, 0.93, 0.0]},
    ],
    "charge": 0,
    "multiplicity": 1,
    "pbc": [False, False, False],
}


def test_geometric_uses_exact_agent_selected_calculator_component(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    result = execute_action(
        "optimize_geometry",
        {
            "backend_id": "geometric",
            "component_backends": {"calculator": "ase_emt"},
            "inputs": {"structure": WATER},
            "method_spec": {"calculator_method": {}},
            "action_settings": {
                "calculator_action_settings": {
                    "calculate_energy": {},
                    "calculate_forces": {},
                },
                "coordinate_system": "cart",
                "max_iterations": 30,
                "trust_radius_angstrom": 0.1,
                "minimum_trust_radius_angstrom": 1e-4,
                "maximum_trust_radius_angstrom": 0.3,
                "hessian_strategy": "never",
                "project_rigid_force_torque": "auto",
                "convergence_energy_hartree": 1e-4,
                "convergence_grms_hartree_per_bohr": 0.1,
                "convergence_gmax_hartree_per_bohr": 0.1,
                "convergence_drms_angstrom": 0.1,
                "convergence_dmax_angstrom": 0.1,
                "rigid_fragments": False,
                "constraint_algorithm": 0,
                "constraint_enforcement_tolerance": 0.0,
            },
            "resource_limits": {"cpu_cores": 1, "walltime_seconds": 300},
        },
    )
    assert result["status"] == "success"
    assert result["selection_source"] == "agent_components"
    assert result["result"]["calculator_backend"] == "ase_emt"
    assert result["result"]["evaluation_count"] >= 1
    assert result["provenance"]["agent_selected_component_backends"] == {
        "calculator": "ase_emt"
    }
    assert result["provenance"]["automatic_component_selection"] is False


def test_geometric_rejects_missing_calculator_component(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    result = execute_action(
        "optimize_geometry",
        {
            "backend_id": "geometric",
            "inputs": {"structure": WATER},
            "method_spec": {"calculator_method": {}},
            "action_settings": {},
        },
    )
    assert result["status"] == "invalid_request"
    assert "component_backends" in result["error"]["message"]


def test_sella_minimum_optimizer_uses_exact_agent_calculator(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    result = execute_action(
        "optimize_geometry",
        {
            "backend_id": "sella",
            "component_backends": {"calculator": "ase_emt"},
            "inputs": {"structure": WATER},
            "method_spec": {"calculator_method": {}},
            "action_settings": {
                "calculator_action_settings": {
                    "calculate_energy": {},
                    "calculate_forces": {},
                },
                "force_threshold_ev_per_angstrom": 5.0,
                "max_steps": 10,
                "internal_coordinates": False,
                "initial_trust_radius": 0.1,
                "minimum_model_quality": 1e-4,
                "finite_difference_step": 0.1,
                "three_point_differences": False,
                "steps_per_diagonalization": 3,
                "diagonalization_interval": 1,
                "allow_fragments": True,
                "refine_initial_hessian_iterations": 0,
            },
            "resource_limits": {"cpu_cores": 1, "walltime_seconds": 300},
        },
    )
    assert result["status"] == "success"
    assert result["selection_source"] == "agent_components"
    assert result["result"]["optimizer"] == "sella"
    assert result["result"]["stationary_point_order"] == 0
    assert result["result"]["calculator_backend"] == "ase_emt"


def test_sella_transition_state_search_is_agent_composed(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    initial_guess = {
        "atoms": [
            {"element": "H", "position_angstrom": [-0.93, 0.0, 0.0]},
            {"element": "H", "position_angstrom": [0.0, 0.0, 0.0]},
            {"element": "H", "position_angstrom": [0.93, 0.0, 0.0]},
        ],
        "charge": 0,
        "multiplicity": 2,
        "pbc": [False, False, False],
    }
    result = execute_action(
        "locate_transition_state",
        {
            "backend_id": "sella",
            "component_backends": {"calculator": "xtb"},
            "inputs": {"initial_guess": initial_guess},
            "method_spec": {"calculator_method": {"method": "gfn2"}},
            "action_settings": {
                "calculator_action_settings": {
                    "calculate_energy": {},
                    "calculate_forces": {},
                },
                "force_threshold_ev_per_angstrom": 5.0,
                "max_steps": 5,
                "internal_coordinates": False,
                "initial_trust_radius": 0.1,
                "minimum_model_quality": 1.0e-4,
                "finite_difference_step": 0.05,
                "three_point_differences": False,
                "steps_per_diagonalization": 3,
                "diagonalization_interval": 1,
                "allow_fragments": True,
                "refine_initial_hessian_iterations": 0,
            },
            "resource_limits": {"cpu_cores": 1, "walltime_seconds": 300},
        },
    )
    assert result["status"] == "success"
    assert result["selection_source"] == "agent_components"
    assert result["result"]["stationary_point_order"] == 1
    assert result["result"]["calculator_backend"] == "xtb"
    assert result["result"]["structure"]["multiplicity"] == 2
    assert "calculate_hessian" in result["result"]["validation_required"]
    assert result["provenance"]["automatic_component_selection"] is False
