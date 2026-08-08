from __future__ import annotations

from chemistry_toolbox.src import service
from chemistry_toolbox.src.models import ActionSpec, BackendSpec


def _available(backend):
    return {
        backend.id: {
            "available": True,
            "status": "available",
            "runtime": backend.runtime,
        }
    }


def test_dispatch_executes_only_agent_selected_backend(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    calls = []
    monkeypatch.setattr(service, "probe_all_backends", lambda values: _available(tuple(values)[0]))

    def invoke_worker(**kwargs):
        calls.append(kwargs)
        return {"status": "success", "result": {"energy": -1.0, "unit": "hartree"}}

    monkeypatch.setattr(service, "invoke_worker", invoke_worker)
    result = service.execute_action(
        "calculate_energy",
        {
            "backend_id": "xtb",
            "inputs": {"structure": {"atoms": [{"element": "H", "position_angstrom": [0, 0, 0]}]}},
            "method_spec": {"method": "gfn2"},
            "action_settings": {},
        },
    )
    assert result["status"] == "success"
    assert len(calls) == 1
    assert calls[0]["runtime"] == "reaction"
    assert calls[0]["payload"]["backend_id"] == "xtb"
    assert result["provenance"]["automatic_fallback_count"] == 0


def test_failure_is_returned_without_fallback(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    calls = []
    monkeypatch.setattr(service, "probe_all_backends", lambda values: _available(tuple(values)[0]))

    def invoke_worker(**kwargs):
        calls.append(kwargs)
        return {"status": "failed", "error": {"code": "test", "message": "failed"}}

    monkeypatch.setattr(service, "invoke_worker", invoke_worker)
    result = service.execute_action(
        "calculate_energy",
        {
            "backend_id": "pyscf",
            "inputs": {"structure": {}},
            "method_spec": {"method": "rhf", "basis": "sto-3g"},
            "action_settings": {},
        },
    )
    assert result["status"] == "failed"
    assert len(calls) == 1
    assert calls[0]["payload"]["backend_id"] == "pyscf"
    assert result["provenance"]["automatic_fallback_count"] == 0


def test_missing_auto_or_unsupported_backend_never_dispatches(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    monkeypatch.setattr(service, "invoke_worker", lambda **_kwargs: (_ for _ in ()).throw(AssertionError("must not dispatch")))
    missing = service.execute_action("calculate_energy", {"inputs": {"structure": {}}, "method_spec": {}, "action_settings": {}})
    automatic = service.execute_action("calculate_energy", {"backend_id": "auto", "inputs": {"structure": {}}, "method_spec": {}, "action_settings": {}})
    unsupported = service.execute_action("calculate_energy", {"backend_id": "vina", "inputs": {"structure": {}}, "method_spec": {}, "action_settings": {}})
    assert missing["status"] == automatic["status"] == unsupported["status"] == "invalid_request"


def test_data_action_uses_only_its_named_source(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    calls = []
    monkeypatch.setattr(service, "probe_all_backends", lambda values: _available(tuple(values)[0]))
    monkeypatch.setattr(
        service,
        "invoke_worker",
        lambda **kwargs: calls.append(kwargs) or {"status": "success", "result": {"records": []}},
    )
    result = service.execute_action(
        "search_compounds",
        {"inputs": {"query": "water"}, "method_spec": {}, "action_settings": {}},
    )
    assert result["selection_source"] == "fixed_data_source"
    assert calls[0]["payload"]["backend_id"] == "pubchem"


def test_internal_deterministic_action_does_not_require_fake_backend(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    calls = []
    monkeypatch.setattr(service, "probe_all_backends", lambda values: _available(tuple(values)[0]))
    monkeypatch.setattr(
        service,
        "invoke_worker",
        lambda **kwargs: calls.append(kwargs)
        or {"status": "success", "result": {"ensemble": [], "weights": []}},
    )
    result = service.execute_action(
        "rank_conformers_from_results",
        {
            "inputs": {"ensemble": [], "scores": []},
            "method_spec": {},
            "action_settings": {"temperature_kelvin": 298.15, "score_unit": "hartree"},
        },
    )
    assert result["status"] == "success"
    assert result["selection_source"] == "internal_deterministic"
    assert calls[0]["payload"]["backend_id"] == "internal_statistics"


def test_internal_deterministic_action_rejects_unrelated_backend(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    monkeypatch.setattr(
        service,
        "invoke_worker",
        lambda **_kwargs: (_ for _ in ()).throw(AssertionError("must not dispatch")),
    )
    result = service.execute_action(
        "derive_vibrational_modes",
        {
            "backend_id": "orca",
            "inputs": {"hessian": {}, "structure": {}},
            "method_spec": {},
            "action_settings": {},
        },
    )
    assert result["status"] == "invalid_request"


def test_composite_action_requires_and_traces_every_agent_component(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    action = ActionSpec(
        id="test_composite_action",
        category="reaction_and_kinetics",
        description="Test-only composite action.",
        primary_output="AtomicStructure",
        backend_ids=("test_driver",),
        required_inputs=("structure",),
        selection_policy="agent_components_required",
    )
    driver = BackendSpec(
        id="test_driver",
        display_name="Test driver",
        runtime="core",
        capabilities=("test_composite_action",),
        description="Test driver",
        required_component_roles={"test_composite_action": ("calculator",)},
        component_backend_options={
            "test_composite_action": {"calculator": ("test_calculator",)}
        },
    )
    calculator = BackendSpec(
        id="test_calculator",
        display_name="Test calculator",
        runtime="quantum",
        capabilities=("calculate_energy",),
        description="Test calculator",
    )
    monkeypatch.setattr(service, "action_specs", lambda: {action.id: action})
    monkeypatch.setattr(
        service,
        "backend_specs",
        lambda: {driver.id: driver, calculator.id: calculator},
    )
    monkeypatch.setattr(
        service,
        "probe_all_backends",
        lambda values: {item.id: {"available": True, "status": "available", "runtime": item.runtime} for item in values},
    )
    calls = []
    monkeypatch.setattr(
        service,
        "invoke_worker",
        lambda **kwargs: calls.append(kwargs) or {"status": "success", "result": {"ok": True}},
    )

    missing = service.execute_action(
        action.id,
        {
            "backend_id": driver.id,
            "inputs": {"structure": {}},
            "method_spec": {},
            "action_settings": {},
        },
    )
    assert missing["status"] == "invalid_request"

    result = service.execute_action(
        action.id,
        {
            "backend_id": driver.id,
            "component_backends": {"calculator": calculator.id},
            "inputs": {"structure": {}},
            "method_spec": {},
            "action_settings": {},
        },
    )
    assert result["status"] == "success"
    assert result["selection_source"] == "agent_components"
    assert result["provenance"]["agent_selected_component_backends"] == {
        "calculator": calculator.id
    }
    assert calls[0]["payload"]["request"]["component_backends"] == {
        "calculator": calculator.id
    }
