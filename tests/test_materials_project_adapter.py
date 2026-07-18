from __future__ import annotations

import sys
from types import ModuleType, SimpleNamespace

from researchchem_toolbox.backends import data as module


class FakeMaterialId:
    def __str__(self) -> str:
        return "mp-149"


class FakeDocument:
    material_id = FakeMaterialId()

    def model_dump(self, *, mode: str):
        assert mode == "json"
        return {"material_id": "mp-ft", "formula_pretty": "Si"}


class FakeMPRester:
    def __init__(self, api_key: str):
        assert api_key == "test-key"
        self.materials = SimpleNamespace(
            summary=SimpleNamespace(search=lambda **_kwargs: [FakeDocument()])
        )

    def __enter__(self):
        return self

    def __exit__(self, *_args):
        return False


def test_material_id_is_normalized_from_public_attribute(monkeypatch):
    monkeypatch.setenv("MP_API_KEY", "test-key")
    package = ModuleType("mp_api")
    client = ModuleType("mp_api.client")
    client.MPRester = FakeMPRester
    package.client = client
    monkeypatch.setitem(sys.modules, "mp_api", package)
    monkeypatch.setitem(sys.modules, "mp_api.client", client)
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
    assert result["result"]["records"][0]["material_id"] == "mp-149"
