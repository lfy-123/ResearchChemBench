from ._helpers import assert_tool_runtime


def test_check_backend_availability(tmp_path, monkeypatch):
    assert_tool_runtime("check_backend_availability", tmp_path, monkeypatch)

