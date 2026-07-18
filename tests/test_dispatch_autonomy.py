from __future__ import annotations

from researchchem_toolbox import service


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
    assert calls[0]["runtime"] == "quantum"
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
