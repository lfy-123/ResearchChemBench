from __future__ import annotations

import pytest

from chemistry_toolbox.src.service import execute_action


def _arrhenius_model(**overrides):
    model = {
        "type": "arrhenius",
        "reaction_order": 1,
        "pre_exponential_factor": 1.0e12,
        "pre_exponential_unit": "s^-1",
        "temperature_exponent": 0.5,
        "activation_energy_kj_mol": 50.0,
        "reference_temperature_kelvin": 1.0,
        "minimum_temperature_kelvin": 300.0,
        "maximum_temperature_kelvin": 2000.0,
    }
    model.update(overrides)
    return model


def test_rmg_evaluates_explicit_arrhenius_model(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    result = execute_action(
        "calculate_rate_constants",
        {
            "backend_id": "rmg",
            "inputs": {
                "kinetics_model": _arrhenius_model(),
                "temperatures_kelvin": [500.0, 1000.0],
            },
            "method_spec": {},
            "action_settings": {"allow_extrapolation": False},
        },
    )
    assert result["status"] == "success"
    assert result["result"]["model_type"] == "arrhenius"
    assert result["result"]["rate_coefficient_unit"] == "s^-1"
    assert len(result["result"]["rate_coefficients"]) == 2
    assert result["result"]["rate_coefficients"][1] > result["result"]["rate_coefficients"][0]


def test_rmg_evaluates_pressure_dependent_arrhenius_model(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    first = _arrhenius_model(pre_exponential_factor=1.0e10)
    second = _arrhenius_model(pre_exponential_factor=2.0e10)
    model = {
        "type": "pressure_dependent_arrhenius",
        "reaction_order": 1,
        "pressures_bar": [1.0, 10.0],
        "terms": [first, second],
        "minimum_temperature_kelvin": 300.0,
        "maximum_temperature_kelvin": 2000.0,
    }
    result = execute_action(
        "calculate_rate_constants",
        {
            "backend_id": "rmg",
            "inputs": {
                "kinetics_model": model,
                "temperatures_kelvin": [600.0, 1000.0],
                "pressures_pa": [1.0e5, 1.0e6],
            },
            "method_spec": {},
            "action_settings": {"allow_extrapolation": False},
        },
    )
    assert result["status"] == "success"
    assert result["result"]["pressures_pa"] == [1.0e5, 1.0e6]
    assert len(result["result"]["rate_coefficients"]) == 2
    assert all(len(row) == 2 for row in result["result"]["rate_coefficients"])


@pytest.mark.parametrize("model_name", ["wigner", "eckart"])
def test_rmg_tunneling_models(tmp_path, monkeypatch, model_name: str):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    inputs = {
        "temperatures_kelvin": [300.0, 500.0],
        "imaginary_frequency_cm1": -1000.0,
    }
    if model_name == "eckart":
        inputs.update(
            {
                "reactant_energy_kj_mol": 0.0,
                "transition_state_energy_kj_mol": 50.0,
                "product_energy_kj_mol": -10.0,
            }
        )
    result = execute_action(
        "calculate_tunneling_correction",
        {
            "backend_id": "rmg",
            "inputs": inputs,
            "method_spec": {"tunneling_model": model_name},
            "action_settings": {},
        },
    )
    assert result["status"] == "success"
    assert result["result"]["tunneling_model"] == model_name
    assert len(result["result"]["tunneling_factors"]) == 2
    assert all(value >= 1.0 for value in result["result"]["tunneling_factors"])
