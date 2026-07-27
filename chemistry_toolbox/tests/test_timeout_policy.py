from __future__ import annotations

from researchchem_toolbox import service
from researchchem_toolbox.models import ActionRequest, ResourceLimits


H2 = {
    "atoms": [
        {"element": "H", "position_angstrom": [0.0, 0.0, 0.0]},
        {"element": "H", "position_angstrom": [0.0, 0.0, 0.74]},
    ],
    "charge": 0,
    "multiplicity": 1,
    "pbc": [False, False, False],
}


def _available(specifications):
    return {
        item.id: {"available": True, "status": "available", "runtime": item.runtime}
        for item in specifications
    }


def test_compute_and_fast_actions_receive_evaluator_timeouts(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    monkeypatch.setenv("RESEARCHCHEMBENCH_COMPUTE_ACTION_TIMEOUT_SECONDS", "9000")
    monkeypatch.setenv("RESEARCHCHEMBENCH_FAST_ACTION_TIMEOUT_SECONDS", "45")
    monkeypatch.setattr(service, "probe_all_backends", _available)
    calls = []

    def fake_worker(**kwargs):
        calls.append(kwargs)
        return {"status": "success", "result": {"ok": True}}

    monkeypatch.setattr(service, "invoke_worker", fake_worker)

    compute = service.execute_action(
        "calculate_energy",
        {
            "backend_id": "xtb",
            "inputs": {"structure": H2},
            "method_spec": {"method": "gfn2"},
            "action_settings": {},
            "resource_limits": {"cpu_cores": 2, "memory_mb": 1024},
        },
    )
    fast = service.execute_action(
        "search_compounds",
        {
            "inputs": {"query": "water"},
            "method_spec": {},
            "action_settings": {},
            "resource_limits": {},
        },
    )

    assert compute["status"] == "success"
    assert fast["status"] == "success"
    assert [item["timeout_seconds"] for item in calls] == [9000, 45]
    assert calls[0]["payload"]["request"]["resource_limits"]["walltime_seconds"] == 9000
    assert calls[0]["payload"]["request"]["action_settings"]["timeout_seconds"] == 9000
    assert calls[1]["payload"]["request"]["resource_limits"]["walltime_seconds"] == 45
    assert calls[1]["payload"]["request"]["action_settings"]["timeout_seconds"] == 45
    assert compute["provenance"]["execution_timeout_policy"]["agent_controllable"] is False
    assert fast["provenance"]["execution_timeout_policy"]["execution_class"] == "fast"


def test_agent_request_schema_has_no_walltime_control():
    resource_schema = ResourceLimits.model_json_schema()["properties"]
    assert "walltime_seconds" not in resource_schema
    request_schema = ActionRequest.model_json_schema()
    assert "walltime_seconds" not in str(request_schema)


def test_action_settings_timeout_override_is_rejected(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    result = service.execute_action(
        "calculate_energy",
        {
            "backend_id": "xtb",
            "inputs": {"structure": H2},
            "method_spec": {"method": "gfn2"},
            "action_settings": {"timeout_seconds": 1},
        },
    )
    assert result["status"] == "invalid_request"
    assert result["error"]["code"] == "evaluator_controlled_timeout"
