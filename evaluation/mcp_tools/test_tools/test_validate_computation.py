from ._helpers import assert_tool_runtime


def test_validate_computation(tmp_path, monkeypatch):
    assert_tool_runtime("validate_computation", tmp_path, monkeypatch)

