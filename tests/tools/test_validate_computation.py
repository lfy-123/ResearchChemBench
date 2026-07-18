from ._helpers import assert_tool_smoke
def test_validate_computation(tmp_path, monkeypatch): assert_tool_smoke("validate_computation", tmp_path, monkeypatch)
