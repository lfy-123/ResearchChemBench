from __future__ import annotations

import importlib
import json
import os
import subprocess
import sys
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


def test_pilot_and_resume_launch_with_identical_runtime_paths(tmp_path, monkeypatch):
    framework = tmp_path / "framework environment"
    python = framework / "bin" / "python"
    python.parent.mkdir(parents=True)
    python.write_text(
        f"#!{sys.executable}\n"
        "import json, os, sys\n"
        "print(json.dumps({'path': os.environ['PATH'], "
        "'libraries': os.environ.get('LD_LIBRARY_PATH'), 'argv': sys.argv[1:], "
        "'cwd': os.getcwd()}))\n"
    )
    python.chmod(0o755)
    monkeypatch.setenv("RESEARCHCHEMBENCH_LOCAL_CONFIG", str(tmp_path / "absent.env"))
    monkeypatch.setenv("RESEARCHCHEMBENCH_FRAMEWORK_ENV", str(framework))
    monkeypatch.setenv("PATH", "/usr/bin:/bin")
    monkeypatch.setenv("LD_LIBRARY_PATH", "/existing/library/path")
    records = []
    for script, arguments in [
        ("test_codex_gpt56.sh", ["paper_fixture", "--dry-run"]),
        ("submit_evaluation.sh", ["resume", "--run-root", str(tmp_path), "--run-id", "fixture"]),
        ("codex/test_codex_gpt56.sh", ["--mode", "paper_reproduction", "paper_one", "paper_two", "--dry-run"]),
    ]:
        result = subprocess.run(
            ["bash", str(ROOT / "scripts" / script), *arguments],
            capture_output=True, text=True, check=True, env=os.environ.copy(), cwd=tmp_path,
        )
        records.append(json.loads(result.stdout))
    assert records[0]["argv"][:2] == ["-m", "evaluation.pilot"]
    assert records[1]["argv"][1] == "resume"
    assert records[2]["argv"] == ["-m", "evaluation.pilot", "--mode", "paper_reproduction", "paper_one", "paper_two", "--dry-run"]
    assert records[0]["path"] == records[1]["path"] == records[2]["path"]
    assert records[0]["libraries"] == records[1]["libraries"] == records[2]["libraries"]
    assert all(record["cwd"] == str(ROOT) for record in records)
    assert records[0]["path"].split(":")[0] == str(framework / "bin")
    assert records[0]["libraries"].split(":")[0] == str(framework / "lib")
