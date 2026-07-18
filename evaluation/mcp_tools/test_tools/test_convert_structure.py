from ._helpers import assert_tool_runtime


def test_convert_structure(tmp_path, monkeypatch):
    assert_tool_runtime("convert_structure", tmp_path, monkeypatch)

