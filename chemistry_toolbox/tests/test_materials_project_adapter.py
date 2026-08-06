from __future__ import annotations

import httpx

from chemistry_toolbox.src.backends import data as module


class FakeResponse:
    def __init__(self, payload):
        self.payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self.payload


def test_materials_project_uses_bounded_summary_rest_query(monkeypatch):
    monkeypatch.setenv("MP_API_KEY", "test-key")
    captured = {}

    def fake_get(url, **kwargs):
        captured["url"] = url
        captured.update(kwargs)
        return FakeResponse(
            {
                "data": [{"material_id": "mp-149", "formula_pretty": "Si"}],
                "meta": {"api_version": "test"},
            }
        )

    monkeypatch.setattr(module.httpx, "get", fake_get)
    result = module.execute(
        "search_materials",
        "materials_project",
        {
            "inputs": {"query": "mp-149"},
            "method_spec": {},
            "action_settings": {
                "max_records": 1,
                "fields": ["material_id", "formula_pretty"],
                "timeout_seconds": 12,
            },
        },
    )
    assert result["status"] == "success"
    assert result["result"]["records"][0]["material_id"] == "mp-149"
    assert captured["url"].endswith("/materials/summary/")
    assert captured["params"]["material_ids"] == "mp-149"
    assert captured["params"]["_limit"] == 1
    assert captured["timeout"] == 12.0
    assert captured["headers"] == {"X-API-KEY": "test-key"}
    assert result["provenance"]["remote_attempts"] == 1


def test_materials_project_retries_transient_failure_after_default_delay(monkeypatch):
    monkeypatch.setenv("MP_API_KEY", "test-key")
    calls = 0
    delays = []
    timeouts = []

    def fake_get(_url, **_kwargs):
        nonlocal calls
        calls += 1
        timeouts.append(_kwargs["timeout"])
        if calls == 1:
            raise httpx.ReadTimeout("temporary timeout")
        return FakeResponse(
            {
                "data": [{"material_id": "mp-149", "formula_pretty": "Si"}],
                "meta": {"api_version": "test"},
            }
        )

    monkeypatch.setattr(module.httpx, "get", fake_get)
    monkeypatch.setattr(module.time, "sleep", delays.append)
    result = module.execute(
        "search_materials",
        "materials_project",
        {
            "inputs": {"query": "mp-149"},
            "method_spec": {},
            "action_settings": {"max_records": 1},
        },
    )

    assert result["status"] == "success"
    assert result["provenance"]["remote_attempts"] == 2
    assert calls == 2
    assert delays == [3.0]
    assert timeouts == [25.0, 25.0]


def test_catalysis_hub_omits_absent_filter_instead_of_sending_null(monkeypatch):
    monkeypatch.setenv("CATALYSIS_HUB_API_KEY", "test-key")
    captured = {}

    def fake_post(url, **kwargs):
        captured["url"] = url
        captured.update(kwargs)
        return FakeResponse(
            {
                "data": {
                    "reactions": {
                        "totalCount": 1,
                        "edges": [{"node": {"id": "reaction-1"}}],
                    }
                }
            }
        )

    monkeypatch.setattr(module.httpx, "post", fake_post)
    result = module.execute(
        "search_catalysis_records",
        "catalysis_hub",
        {
            "inputs": {"query": {"reactants": "CO"}},
            "method_spec": {},
            "action_settings": {"max_records": 1, "timeout_seconds": 10},
        },
    )
    assert result["status"] == "success"
    assert "$reactants: String!" in captured["json"]["query"]
    assert "$products" not in captured["json"]["query"]
    assert captured["json"]["variables"] == {"first": 1, "reactants": "CO"}
    assert captured["headers"]["X-API-Key"] == "test-key"


def test_catalysis_hub_requires_api_key(monkeypatch):
    monkeypatch.delenv("CATALYSIS_HUB_API_KEY", raising=False)
    result = module.execute(
        "search_catalysis_records",
        "catalysis_hub",
        {
            "inputs": {"query": {"reactants": "CO"}},
            "method_spec": {},
            "action_settings": {"max_records": 1},
        },
    )

    assert result["status"] == "unavailable"
    assert "CATALYSIS_HUB_API_KEY" in result["error"]["message"]


def test_catalysis_hub_default_retry_budget_handles_two_transient_failures(monkeypatch):
    monkeypatch.setenv("CATALYSIS_HUB_API_KEY", "test-key")
    calls = 0
    delays = []
    timeouts = []

    def fake_post(_url, **kwargs):
        nonlocal calls
        calls += 1
        timeouts.append(kwargs["timeout"])
        if calls < 3:
            raise httpx.ConnectError("temporary connection failure")
        return FakeResponse(
            {
                "data": {
                    "reactions": {
                        "totalCount": 1,
                        "edges": [{"node": {"id": "reaction-1"}}],
                    }
                }
            }
        )

    monkeypatch.setattr(module.httpx, "post", fake_post)
    monkeypatch.setattr(module.time, "sleep", delays.append)
    result = module.execute(
        "search_catalysis_records",
        "catalysis_hub",
        {
            "inputs": {"query": {"reactants": "CO"}},
            "method_spec": {},
            "action_settings": {"max_records": 1},
        },
    )

    assert result["status"] == "success"
    assert result["provenance"]["remote_attempts"] == 3
    assert delays == [2.0, 4.0]
    assert timeouts == [15.0, 15.0, 15.0]
