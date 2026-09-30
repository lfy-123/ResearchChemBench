from __future__ import annotations

from chemistry_toolbox.src import service
from chemistry_toolbox.src.models import ActionRequest, ResourceLimits
from chemistry_toolbox.src.timeout_policy import (
    DEFAULT_COMPUTE_ACTION_TIMEOUT_SECONDS,
    DEFAULT_FAST_ACTION_TIMEOUT_SECONDS,
    compute_action_timeout_seconds,
    fast_action_timeout_seconds,
    native_software_timeout_seconds,
    native_timeout_policy_record,
    unbounded_native_software_ids,
)


def test_all_action_walltime_defaults_are_24_hours(monkeypatch):
    monkeypatch.delenv("RESEARCHCHEMBENCH_COMPUTE_ACTION_TIMEOUT_SECONDS", raising=False)
    monkeypatch.delenv("RESEARCHCHEMBENCH_FAST_ACTION_TIMEOUT_SECONDS", raising=False)
    assert DEFAULT_COMPUTE_ACTION_TIMEOUT_SECONDS == 86400
    assert DEFAULT_FAST_ACTION_TIMEOUT_SECONDS == 86400
    assert compute_action_timeout_seconds() == 86400
    assert fast_action_timeout_seconds() == 86400
    assert native_software_timeout_seconds("orca") == 86400


def test_implicit_fast_default_respects_explicit_compute_override(monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_COMPUTE_ACTION_TIMEOUT_SECONDS", "7200")
    monkeypatch.delenv("RESEARCHCHEMBENCH_FAST_ACTION_TIMEOUT_SECONDS", raising=False)
    assert fast_action_timeout_seconds() == 7200


def test_native_unbounded_policy_is_evaluator_selected(monkeypatch):
    monkeypatch.setenv(
        "RESEARCHCHEMBENCH_UNBOUNDED_NATIVE_SOFTWARE_IDS", "gaussian,open-babel"
    )
    assert unbounded_native_software_ids() == frozenset({"gaussian", "open_babel"})
    assert native_software_timeout_seconds("gaussian") is None
    assert native_timeout_policy_record("gaussian") == {
        "execution_class": "compute",
        "software_id": "gaussian",
        "timeout_seconds": None,
        "walltime_unbounded": True,
        "source": "evaluation_policy_unbounded_native_software",
        "agent_controllable": False,
    }


def test_native_jobs_keep_compute_timeout_when_not_selected(monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_COMPUTE_ACTION_TIMEOUT_SECONDS", "17")
    monkeypatch.delenv("RESEARCHCHEMBENCH_UNBOUNDED_NATIVE_SOFTWARE_IDS", raising=False)
    assert native_software_timeout_seconds("orca") == 17


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
