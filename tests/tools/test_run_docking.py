from ._helpers import assert_tool_smoke
def test_run_docking(tmp_path, monkeypatch): assert_tool_smoke("run_docking", tmp_path, monkeypatch)
