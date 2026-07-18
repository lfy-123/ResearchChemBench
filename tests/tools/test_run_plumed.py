from ._helpers import assert_tool_smoke
def test_run_plumed(tmp_path, monkeypatch): assert_tool_smoke("run_plumed", tmp_path, monkeypatch)
