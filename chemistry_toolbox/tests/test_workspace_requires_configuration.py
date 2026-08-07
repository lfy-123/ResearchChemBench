from pathlib import Path

import pytest

from chemistry_toolbox.mcp.workspace import workspace_root as mcp_workspace_root
from chemistry_toolbox.src.artifacts import workspace_root as action_workspace_root


@pytest.mark.parametrize("resolver", [mcp_workspace_root, action_workspace_root])
def test_workspace_requires_explicit_configuration(monkeypatch, resolver) -> None:
    monkeypatch.delenv("RESEARCHCHEM_MCP_WORKSPACE", raising=False)
    monkeypatch.delenv("RESEARCHCHEMBENCH_WORKSPACE", raising=False)

    with pytest.raises(RuntimeError, match="must be set"):
        resolver()


@pytest.mark.parametrize("resolver", [mcp_workspace_root, action_workspace_root])
def test_workspace_uses_configured_directory(
    tmp_path: Path, monkeypatch, resolver
) -> None:
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))

    assert resolver() == tmp_path.resolve()
