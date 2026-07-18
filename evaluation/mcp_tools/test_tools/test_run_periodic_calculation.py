from ._helpers import assert_tool_runtime


def test_run_periodic_calculation(tmp_path, monkeypatch):
    assert_tool_runtime("run_periodic_calculation", tmp_path, monkeypatch)

