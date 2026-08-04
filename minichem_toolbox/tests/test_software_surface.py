from __future__ import annotations

import pytest

from minichem_mcp_tools.execution_models import SoftwareListRequest
from minichem_mcp_tools.software_catalog import (
    list_software,
    native_command_guide,
    resolve_software_id,
    validate_native_guides,
)
from minichem_toolbox.mini_profile import MINI_NATIVE_SOFTWARE_IDS


def test_native_guides_cover_focused_executables() -> None:
    validate_native_guides()
    result = list_software(SoftwareListRequest(native_only=True, limit=100))
    assert {item["software_id"] for item in result["software"]} == set(
        MINI_NATIVE_SOFTWARE_IDS
    )


def test_hidden_comprehensive_software_cannot_be_resolved() -> None:
    for software_id in ("orca", "vasp", "gromacs", "vina"):
        with pytest.raises(KeyError):
            resolve_software_id(software_id)


def test_gaussian_native_commands_remain_available() -> None:
    assert native_command_guide("gaussian", "g16")["runtime"] == "gaussian"
    assert native_command_guide("gaussian", "formchk")["runtime"] == "gaussian"
