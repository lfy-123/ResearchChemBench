from ._helpers import assert_tool_runtime


def test_extract_output_json(tmp_path, monkeypatch):
    assert_tool_runtime("extract_output_json", tmp_path, monkeypatch)

