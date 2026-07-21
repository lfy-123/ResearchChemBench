from __future__ import annotations

from researchchem_toolbox.backends import data as module


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


def test_catalysis_hub_omits_absent_filter_instead_of_sending_null(monkeypatch):
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
