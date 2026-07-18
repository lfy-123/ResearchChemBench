from ._helpers import assert_tool_smoke
def test_calculator(tmp_path, monkeypatch): assert_tool_smoke("calculator", tmp_path, monkeypatch)
