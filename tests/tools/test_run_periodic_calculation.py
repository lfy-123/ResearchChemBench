from ._helpers import assert_tool_smoke
def test_run_periodic_calculation(tmp_path, monkeypatch): assert_tool_smoke("run_periodic_calculation", tmp_path, monkeypatch)
