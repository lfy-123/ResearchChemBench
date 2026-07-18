"""Pytest wiring for tools whose executables live in isolated profiles.

The MCP toolbox intentionally keeps conflicting native dependencies in separate
environments.  These tests still run under the lightweight ``.toolbox_env``
Python interpreter, so expose only the executable paths required by tests that
expect a working backend.  Production MCP servers obtain the same paths from
``config/mcp_profiles.yaml`` via ``evaluation.mcp_tools.profiles``.
"""

from __future__ import annotations

from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[3]

PROFILE_COMMANDS = {
    "CHEMGRAPH_XTB_COMMAND": PROJECT_ROOT / ".tool_envs" / "quantum" / "bin" / "xtb",
    "CHEMGRAPH_CREST_COMMAND": PROJECT_ROOT / ".tool_envs" / "reaction" / "bin" / "crest",
    "CHEMGRAPH_PHONOPY_COMMAND": PROJECT_ROOT
    / ".tool_envs"
    / "phonons"
    / "bin"
    / "phonopy-init",
}


@pytest.fixture(autouse=True)
def isolated_profile_commands(monkeypatch: pytest.MonkeyPatch) -> None:
    """Make installed profile executables available without changing PATH."""

    for variable, executable in PROFILE_COMMANDS.items():
        if executable.is_file():
            monkeypatch.setenv(variable, str(executable))
