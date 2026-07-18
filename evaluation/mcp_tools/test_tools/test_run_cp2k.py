from ._helpers import assert_tool_runtime


def test_run_cp2k(tmp_path, monkeypatch):
    assert_tool_runtime("run_cp2k", tmp_path, monkeypatch)

