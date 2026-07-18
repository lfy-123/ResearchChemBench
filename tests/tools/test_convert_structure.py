from ._helpers import assert_tool_smoke
def test_convert_structure(tmp_path, monkeypatch): assert_tool_smoke("convert_structure", tmp_path, monkeypatch)
