from pathlib import Path

from pymatgen.core import Lattice, Structure

from chemistry_toolbox.src import execute_action
from chemistry_toolbox.src.catalog import validate_catalog


def test_ccdc_cif_export_connector_returns_pinned_structure(tmp_path, monkeypatch):
    validate_catalog()
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    cif = workspace / "SYNTHETIC01.cif"
    Structure(
        Lattice.cubic(5.0),
        ["C", "O"],
        [[0, 0, 0], [0.5, 0.5, 0.5]],
    ).to(filename=str(cif), fmt="cif")
    monkeypatch.setenv("RESEARCHCHEM_MCP_WORKSPACE", str(workspace))
    result = execute_action(
        "retrieve_crystal_structure",
        {
            "backend_id": "ccdc",
            "inputs": {
                "query": {
                    "record_id": "SYNTHETIC01",
                    "cif_path": "SYNTHETIC01.cif",
                }
            },
            "action_settings": {
                "component_policy": "full_crystal",
                "hydrogen_policy": "as_deposited",
            },
        },
    )
    assert result["status"] == "success"
    payload = result["result"]
    assert payload["record_id"] == "SYNTHETIC01"
    assert payload["formula"] == "CO"
    assert len(payload["sites"]) == 2
    assert payload["source"] == "explicit_cif_export"


def test_ccdc_record_without_license_is_structured_unavailable(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEM_MCP_WORKSPACE", str(tmp_path))
    result = execute_action(
        "retrieve_crystal_structure",
        {
            "backend_id": "ccdc",
            "inputs": {"query": {"record_id": "does-not-exist"}},
            "action_settings": {
                "component_policy": "full_crystal",
                "hydrogen_policy": "as_deposited",
            },
        },
    )
    assert result["status"] == "unavailable"
    assert "licensed" in result["error"]["message"]


def test_ccdc_unimplemented_transform_is_not_silently_accepted(tmp_path, monkeypatch):
    workspace = tmp_path / "workspace"
    workspace.mkdir()
    cif = workspace / "GENERIC01.cif"
    Structure(Lattice.cubic(4.0), ["N", "H"], [[0, 0, 0], [0.2, 0, 0]]).to(
        filename=str(cif), fmt="cif"
    )
    monkeypatch.setenv("RESEARCHCHEM_MCP_WORKSPACE", str(workspace))
    result = execute_action(
        "retrieve_crystal_structure",
        {
            "backend_id": "ccdc",
            "inputs": {
                "query": {"record_id": "GENERIC01", "cif_path": "GENERIC01.cif"}
            },
            "action_settings": {
                "component_policy": "unique_molecule",
                "hydrogen_policy": "as_deposited",
            },
        },
    )
    assert result["status"] == "unsupported"
    assert "component-selection" in result["error"]["message"]
