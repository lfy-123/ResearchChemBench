from __future__ import annotations

import ast
from pathlib import Path

import pytest

from chemistry_toolbox.scripts import run_data_source_smokes
from chemistry_toolbox.scripts.run_native_interface_smokes import classify_probe

TOOLBOX_ROOT = Path(__file__).resolve().parents[1]


def test_action_backend_matrix_does_not_set_evaluator_walltime() -> None:
    source = TOOLBOX_ROOT.joinpath(
        "scripts", "run_action_backend_matrix_smokes.py"
    ).read_text(encoding="utf-8")
    tree = ast.parse(source)
    keys = {
        key.value
        for node in ast.walk(tree)
        if isinstance(node, ast.Dict)
        for key in node.keys
        if isinstance(key, ast.Constant) and isinstance(key.value, str)
    }
    assert "walltime_seconds" not in keys


def test_native_probe_marks_runtime_linker_and_gamess_config_errors_failed() -> None:
    failed_process = {"process_status": "failed"}
    for output in (
        "libstdc++.so.6: version `GLIBCXX_3.4.32' not found",
        "libstdc++.so.6: version `CXXABI_1.3.15' not found",
        "Please run 'config' first, to set up GAMESS compiling information",
    ):
        status, _reason = classify_probe(failed_process, output, cancelled=False)
        assert status == "failed"


def test_native_probe_preserves_expected_missing_input_classification() -> None:
    status, _reason = classify_probe(
        {"process_status": "failed"},
        "ERROR: No input file 'dftb_in.hsd' found.",
        cancelled=False,
    )
    assert status == "started_input_required"


def test_data_source_smoke_help_does_not_execute_live_actions(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(
        run_data_source_smokes,
        "execute_action",
        lambda *_args, **_kwargs: pytest.fail("--help executed a live action"),
    )
    with pytest.raises(SystemExit) as exc_info:
        run_data_source_smokes.main(["--help"])
    assert exc_info.value.code == 0
    assert "--output" in capsys.readouterr().out
