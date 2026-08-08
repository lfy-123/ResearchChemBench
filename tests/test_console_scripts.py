from __future__ import annotations

import importlib
from pathlib import Path

import pytest

from evaluation.web import server

ROOT = Path(__file__).resolve().parents[1]
ENTRY_POINTS = {
    "researchchembench": "evaluation.web.server:main",
    "researchchembench-eval": "evaluation.cli:main",
    "researchchem-mcp-server": "chemistry_toolbox.mcp.server:main",
    "researchchem-mcp-install": "chemistry_toolbox.mcp.installer:main",
    "researchchem-tool": "chemistry_toolbox.mcp.tool_manager:main",
    "researchchem-software": "chemistry_toolbox.software_management.cli:main",
}


def test_console_entry_points_reference_importable_callables() -> None:
    project = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    setup = (ROOT / "chemistry_toolbox/scripts/setup_toolbox_env.sh").read_text(
        encoding="utf-8"
    )
    for command, target in ENTRY_POINTS.items():
        assert f'{command} = "{target}"' in project
        assert command in setup
        module_name, attribute = target.split(":", 1)
        assert callable(getattr(importlib.import_module(module_name), attribute))


def test_web_console_help_exits_without_starting_server(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(
        server.app,
        "run",
        lambda **_kwargs: pytest.fail("--help started the web server"),
    )
    with pytest.raises(SystemExit) as exc_info:
        server.main(["--help"])
    assert exc_info.value.code == 0
    assert "--host" in capsys.readouterr().out
