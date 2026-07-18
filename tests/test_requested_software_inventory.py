from __future__ import annotations

import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]


def _yaml(path: str):
    return yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))


def test_requested_software_inventory_covers_all_59_unique_items():
    items = _yaml("config/requested_software.yaml")["requested_software"]
    names = [item["name"] for item in items]
    assert len(names) == len(set(names)) == 59
    assert {item["category"] for item in items} == {
        "数据与工作流基础",
        "构象与分子量子化学",
        "周期材料、声子与输运",
        "分子动力学与自由能",
        "反应网络与动力学",
        "激发态、光谱与可视化",
        "对接、结构处理与机器学习势",
        "数据接口",
    }


def test_probe_items_reference_declared_runtimes_and_models_use_model_cache():
    items = _yaml("config/requested_software.yaml")["requested_software"]
    mcp = _yaml("config/mcp_profiles.yaml")
    auxiliary = _yaml("config/auxiliary_environments.yaml")[
        "auxiliary_environments"
    ]
    runtime_names = {
        *mcp["profiles"],
        *mcp.get("support_environments", {}),
        *auxiliary,
    }
    for item in items:
        if item["status_policy"] == "probe":
            assert item["environment"] in runtime_names
        if item.get("model_cache"):
            assert item["model_cache"] == ".model_cache"


def test_auxiliary_environments_do_not_define_public_tools_or_backend_order():
    auxiliary = _yaml("config/auxiliary_environments.yaml")[
        "auxiliary_environments"
    ]
    for specification in auxiliary.values():
        assert "backends" not in specification
        assert "tools" not in specification
        assert "workflow" not in specification


def test_new_source_and_binary_extensions_are_audited_as_runtime_only():
    items = {
        item["name"]: item
        for item in _yaml("config/requested_software.yaml")["requested_software"]
    }
    for name in {"Multiwfn", "MESS", "MESMER", "AutoMeKin", "VESTA"}:
        item = items[name]
        assert item["status_policy"] == "probe"
        assert item["public_adapter"] == "runtime_only"
        assert item["commands"]
        assert all(path.startswith(".software_cache/") for path in item["cache_paths"])


def test_generated_requested_software_status_has_no_unaccounted_missing_item():
    payload = json.loads(
        (ROOT / "config/requested_software_status.json").read_text(encoding="utf-8")
    )
    assert payload["summary"]["total"] == 59
    assert payload["summary"]["counts"].get("not_found", 0) == 0
    assert {item["status"] for item in payload["software"]} <= {
        "configured",
        "partial",
        "specification",
        "manual_required",
        "manual_api_review",
    }


def test_nist_interfaces_require_api_review_instead_of_scraping():
    items = _yaml("config/requested_software.yaml")["requested_software"]
    nist = [item for item in items if item["name"].startswith("NIST ")]
    assert len(nist) == 2
    assert all(item["status_policy"] == "interface" for item in nist)
    assert all(item["public_adapter"] == "not_implemented" for item in nist)
    assert all("scrap" in item["notes"].lower() for item in nist)
