from __future__ import annotations

import json
from pathlib import Path

import yaml

from researchchem_toolbox.catalog import backend_specs


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
    for name in {"Multiwfn", "MESS", "MESMER", "AutoMeKin", "VESTA", "LOBSTER", "Newton-X"}:
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


def test_nist_interfaces_keep_cccbdb_disabled_and_bound_webbook_to_official_cgi():
    items = _yaml("config/requested_software.yaml")["requested_software"]
    nist = {item["name"]: item for item in items if item["name"].startswith("NIST ")}
    assert set(nist) == {"NIST CCCBDB 接口", "NIST Chemistry WebBook 接口"}
    cccbdb = nist["NIST CCCBDB 接口"]
    assert cccbdb["status_policy"] == "interface"
    assert cccbdb["public_adapter"] == "not_implemented"
    assert cccbdb["mcp_exposure"] == "disabled_no_documented_api"
    assert "scrap" in cccbdb["notes"].lower()
    webbook = nist["NIST Chemistry WebBook 接口"]
    assert webbook["status_policy"] == "probe"
    assert webbook["environment"] == "services"
    assert webbook["public_adapter"] == "existing"
    assert "parameterized cgi" in webbook["notes"].lower()
    assert "bulk" in webbook["notes"].lower()


def test_operator_disabled_unlicensed_suites_are_absent_from_mcp_backends():
    items = {
        item["name"]: item
        for item in _yaml("config/requested_software.yaml")["requested_software"]
    }
    disabled = {"Q-Chem", "Molpro", "TURBOMOLE", "CRYSTAL", "WIEN2k", "OpenEye"}
    for name in disabled:
        assert items[name]["mcp_exposure"] == "disabled_by_operator_no_license"
        assert items[name]["public_adapter"] == "not_implemented"
    assert {
        "qchem", "molpro", "turbomole", "crystal", "wien2k", "openeye"
    }.isdisjoint(backend_specs())
