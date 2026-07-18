from ._helpers import assert_tool_runtime


def test_run_psi4(tmp_path, monkeypatch):
    assert_tool_runtime("run_psi4", tmp_path, monkeypatch)

