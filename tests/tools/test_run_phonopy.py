from ._helpers import assert_tool_smoke
def test_run_phonopy(tmp_path, monkeypatch): assert_tool_smoke("run_phonopy", tmp_path, monkeypatch)
