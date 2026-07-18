from ._helpers import assert_tool_smoke
def test_check_backend_availability(tmp_path, monkeypatch): assert_tool_smoke("check_backend_availability", tmp_path, monkeypatch)
