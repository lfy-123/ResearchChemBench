from __future__ import annotations

import shutil
from zipfile import ZipFile

from researchchem_toolbox.paths import PROJECT_ROOT as ROOT
from researchchem_toolbox.service import execute_action
WATER = {
    "atoms": [
        {"element": "O", "position_angstrom": [0.0, 0.0, 0.0]},
        {"element": "H", "position_angstrom": [0.0, 0.7578, 0.5859]},
        {"element": "H", "position_angstrom": [0.0, -0.7578, 0.5859]},
    ],
    "charge": 0,
    "multiplicity": 1,
}


def test_qcelemental_normalize_and_validate_are_deterministic_actions(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    normalized = execute_action(
        "normalize_qcschema_molecule",
        {
            "inputs": {"structure": WATER},
            "method_spec": {},
            "action_settings": {
                "fix_center_of_mass": True,
                "fix_orientation": True,
            },
        },
    )
    assert normalized["status"] == "success"
    assert normalized["backend"] == "qcelemental"
    assert normalized["selection_source"] == "internal_deterministic"
    assert normalized["result"]["atom_count"] == 3
    molecule = normalized["result"]["molecule"]
    assert molecule["schema_name"] == "qcschema_molecule"

    valid = execute_action(
        "validate_qcschema_record",
        {
            "inputs": {"record": molecule},
            "method_spec": {},
            "action_settings": {"record_type": "molecule"},
        },
    )
    assert valid["status"] == "success"
    assert valid["result"]["valid"] is True

    invalid = execute_action(
        "validate_qcschema_record",
        {
            "inputs": {"record": {"symbols": ["H"]}},
            "method_spec": {},
            "action_settings": {"record_type": "molecule"},
        },
    )
    assert invalid["status"] == "success"
    assert invalid["result"]["valid"] is False
    assert invalid["result"]["errors"]


def test_cclib_parses_selected_existing_output_properties(tmp_path, monkeypatch):
    source = ROOT / ".software_cache" / "gaussian" / "g16" / "smoke" / "water.log"
    shutil.copy2(source, tmp_path / "water.log")
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    result = execute_action(
        "parse_quantum_chemistry_output",
        {
            "inputs": {"output_file": "water.log"},
            "method_spec": {},
            "action_settings": {
                "properties": ["metadata", "atom_coordinates", "energies"],
                "coordinate_frames": "last",
                "include_orbital_coefficients": False,
                "include_excited_state_configurations": False,
                "max_array_elements": 100000,
            },
        },
    )
    assert result["status"] == "success"
    assert result["backend"] == "cclib"
    assert result["backend_version"] == "1.8.1"
    assert result["result"]["properties"]["scfenergies"]
    assert len(result["result"]["properties"]["atomcoords"]) == 3
    assert result["output_artifacts"]


def test_cclib_parses_orca_output_with_missing_first_rms_target(tmp_path, monkeypatch):
    archive_path = (
        ROOT
        / "tasks"
        / "_heterobiaryl_pv_shared"
        / "public"
        / "computational_records.zip"
    )
    member = "records/P0/P0_C001_DLPNO.out"
    with ZipFile(archive_path) as archive:
        (tmp_path / "orca.out").write_bytes(archive.read(member))
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))

    result = execute_action(
        "parse_quantum_chemistry_output",
        {
            "inputs": {"output_file": "orca.out"},
            "method_spec": {},
            "action_settings": {
                "properties": ["metadata", "energies"],
                "coordinate_frames": "last",
                "include_orbital_coefficients": False,
                "include_excited_state_configurations": False,
                "max_array_elements": 10000,
            },
        },
    )

    assert result["status"] == "success"
    assert result["result"]["properties"]["scfenergies"]
    assert any("compatibility fix" in warning for warning in result["warnings"])
