from ._helpers import assert_tool_runtime


def test_calculator(tmp_path, monkeypatch):
    assert_tool_runtime("calculator", tmp_path, monkeypatch)

