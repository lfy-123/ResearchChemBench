from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path

import yaml

from chemistry_toolbox.src.catalog import backend_specs
from chemistry_toolbox.src.runtime import runtime_environment


ROOT = Path(__file__).resolve().parents[1]


def _yaml(path: str):
    return yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))


def test_requested_software_inventory_covers_all_59_unique_items():
    items = _yaml("config/requested_software.yaml")["requested_software"]
    names = [item["name"] for item in items]
    assert len(names) == len(set(names)) == 59
    assert {item["category"] for item in items} == {
        "Data and Workflow Infrastructure",
        "Conformers and Molecular Quantum Chemistry",
        "Periodic Materials, Phonons, and Transport",
        "Molecular Dynamics and Free Energy",
        "Reaction Networks and Kinetics",
        "Excited States, Spectroscopy, and Visualization",
            "Docking, Structure Processing, and Machine-Learned Potentials",
            "Data Interfaces",
            "Molecular Simulation, Free Energy, and Biomolecular Modeling",
            "Data-Driven Chemistry and Materials Discovery",
        }


def test_probe_items_reference_declared_runtimes_and_models_use_model_cache():
    items = _yaml("config/requested_software.yaml")["requested_software"]
    mcp = _yaml("config/mcp_profiles.yaml")
    auxiliary = _yaml("config/auxiliary_environments.yaml")[
        "auxiliary_environments"
    ]
    runtime_names = {
        *mcp["profiles"],
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


def test_requested_software_audit_reuses_profile_runtime_environment(monkeypatch):
    monkeypatch.delenv("LD_PRELOAD", raising=False)
    script = ROOT / "scripts/audit_requested_software.py"
    spec = importlib.util.spec_from_file_location("audit_requested_software", script)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    amber = module.runtime_catalog()["amber"]
    audited = module.runtime_environment(amber)
    configured = runtime_environment("amber")
    assert audited["LD_PRELOAD"].split(os.pathsep) == configured[
        "LD_PRELOAD"
    ].split(os.pathsep)
    assert audited["LD_LIBRARY_PATH"] == configured["LD_LIBRARY_PATH"]


def test_new_source_and_binary_extensions_have_explicit_exposure_status():
    items = {
        item["name"]: item
        for item in _yaml("config/requested_software.yaml")["requested_software"]
    }
    for name in {"Multiwfn", "MESS", "MESMER", "LOBSTER"}:
        item = items[name]
        assert item["status_policy"] == "probe"
        assert item["public_adapter"] == "existing"
    for name in {"AutoMeKin", "VESTA", "Newton-X"}:
        item = items[name]
        assert item["status_policy"] == "probe"
        assert item["public_adapter"] == "runtime_only"
        assert item["commands"]
        assert all(path.startswith(".software_cache/") for path in item["cache_paths"])


def test_generated_requested_software_status_has_no_unaccounted_missing_item():
    payload = json.loads(
        (ROOT / "evidence/status/requested_software_status.json").read_text(encoding="utf-8")
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


def test_nist_interface_is_bound_to_official_webbook_cgi():
    items = _yaml("config/requested_software.yaml")["requested_software"]
    nist = {item["name"]: item for item in items if item["name"].startswith("NIST ")}
    assert set(nist) == {"NIST Chemistry WebBook Interface"}
    webbook = nist["NIST Chemistry WebBook Interface"]
    assert webbook["status_policy"] == "probe"
    assert webbook["environment"] == "services"
    assert webbook["public_adapter"] == "existing"
    assert "parameterized cgi" in webbook["notes"].lower()
    assert "bulk" in webbook["notes"].lower()


def test_removed_unlicensed_suites_are_absent_from_inventory_and_backends():
    names = {
        item["name"]
        for item in _yaml("config/requested_software.yaml")["requested_software"]
    }
    removed = {
        "Q-Chem", "Molpro", "TURBOMOLE", "CASTEP", "CRYSTAL", "WIEN2k",
        "EasySpin", "MATLAB", "OpenEye", "Schrödinger",
    }
    assert removed.isdisjoint(names)
    assert {
        "qchem", "molpro", "turbomole", "castep", "crystal", "wien2k",
        "easyspin", "matlab", "openeye", "schrodinger",
    }.isdisjoint(backend_specs())
