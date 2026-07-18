from ._helpers import assert_tool_smoke
def test_run_cp2k(tmp_path, monkeypatch): assert_tool_smoke("run_cp2k", tmp_path, monkeypatch)
