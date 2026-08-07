from __future__ import annotations

import pytest

from chemistry_toolbox.src import service
from chemistry_toolbox.src.discovery import inspect_action


H2 = {
    "atoms": [
        {"element": "H", "position_angstrom": [0.0, 0.0, 0.0]},
        {"element": "H", "position_angstrom": [0.0, 0.0, 0.74]},
    ],
    "charge": 0,
    "multiplicity": 1,
}


def _request(method: str, basis: str | None) -> dict:
    method_spec = {"method": method}
    if basis is not None:
        method_spec["basis"] = basis
    return {
        "backend_id": "orca",
        "inputs": {"structure": H2},
        "method_spec": method_spec,
        "action_settings": {},
    }


@pytest.mark.parametrize("basis", [None, "auto", "method_default", "builtin"])
def test_orca_composite_basis_sentinels_pass_preflight(
    tmp_path, monkeypatch, basis
) -> None:
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    monkeypatch.setattr(
        service,
        "probe_all_backends",
        lambda specifications: {
            item.id: {
                "available": False,
                "status": "unavailable",
                "runtime": item.runtime,
            }
            for item in specifications
        },
    )
    result = service.execute_action(
        "calculate_energy", _request("r2SCAN-3c", basis)
    )
    assert result["status"] == "unavailable"
    assert result["error"]["code"] == "backend_unavailable"


@pytest.mark.parametrize(
    ("method", "basis", "expected"),
    [
        ("HF", None, "requires a concrete"),
        ("HF", "auto", "requires a concrete"),
        ("r2SCAN-3c", "def2-SVP", "includes its own orbital basis"),
    ],
)
def test_orca_invalid_method_basis_fails_before_health_probe(
    tmp_path, monkeypatch, method, basis, expected
) -> None:
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    monkeypatch.setattr(
        service,
        "probe_all_backends",
        lambda _values: (_ for _ in ()).throw(
            AssertionError("invalid ORCA method/basis must not reach health probing")
        ),
    )
    result = service.execute_action(
        "calculate_energy", _request(method, basis)
    )
    assert result["status"] == "invalid_request"
    assert result["error"]["code"] == "invalid_orca_method_basis"
    assert expected in result["error"]["message"]
    assert result["retryable"] is True
    assert result["error"]["inspect_action_request"] == {
        "action_id": "calculate_energy",
        "backend_id": "orca",
        "detail_level": "contract",
    }


def test_orca_discovery_exposes_conditional_basis_contract() -> None:
    contract = inspect_action(
        "optimize_geometry", backend_id="orca", detail_level="contract"
    )["selected_request_contract"]
    assert "basis" in contract["optional_field_names"]["method_spec"]
    assert any(
        item["name"] == "basis_conditional"
        and "r2SCAN-3c" in item["rule"]
        and "never emitted" in item["rule"]
        for item in contract["conditional_requirements"]
    )
