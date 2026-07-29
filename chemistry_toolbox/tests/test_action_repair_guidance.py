from __future__ import annotations

from researchchem_toolbox.service import execute_action


H2 = {
    "atoms": [
        {"element": "H", "position_angstrom": [0.0, 0.0, 0.0]},
        {"element": "H", "position_angstrom": [0.0, 0.0, 0.74]},
    ],
    "charge": 0,
    "multiplicity": 1,
}


def _xtb_request(optimization_level: str | None = None) -> dict:
    settings = {}
    if optimization_level is not None:
        settings["optimization_level"] = optimization_level
    return {
        "backend_id": "xtb",
        "inputs": {"structure": H2},
        "method_spec": {"method": "gfn2"},
        "action_settings": settings,
    }


def test_missing_required_setting_returns_one_step_repair_template() -> None:
    result = execute_action("optimize_geometry", _xtb_request())
    assert result["status"] == "invalid_request"
    assert result["retryable"] is True
    assert result["error"]["missing_fields"] == [
        "action_settings.optimization_level"
    ]
    repaired = result["error"]["corrected_request_template"]
    assert repaired["action_id"] == "optimize_geometry"
    assert repaired["backend_id"] == "xtb"
    assert "inspect_action contract" in repaired["action_settings"][
        "optimization_level"
    ]
    assert "same Action/Backend" in result["error"]["repair_guidance"]


def test_invalid_enum_returns_allowed_values_without_changing_backend() -> None:
    result = execute_action("optimize_geometry", _xtb_request("fast"))
    assert result["status"] == "invalid_request"
    assert result["error"]["code"] == "invalid_explicit_choice"
    assert result["error"]["invalid_field"] == (
        "action_settings.optimization_level"
    )
    assert "normal" in result["error"]["allowed_values"]
    repaired = result["error"]["corrected_request_template"]
    assert repaired["backend_id"] == "xtb"
    assert "choose exactly one" in repaired["action_settings"][
        "optimization_level"
    ]


def test_repair_template_preserves_fixed_provider_selection_policy() -> None:
    result = execute_action(
        "search_compounds",
        {"inputs": {}, "method_spec": {}, "action_settings": {}},
    )
    assert result["status"] == "invalid_request"
    repaired = result["error"]["corrected_request_template"]
    assert repaired["backend_id"] is None
    assert repaired["source_id"] is None
    assert "inspect_action contract" in repaired["inputs"]["query"]
