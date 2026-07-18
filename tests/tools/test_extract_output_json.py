from ._helpers import assert_tool_smoke
def test_extract_output_json(tmp_path, monkeypatch): assert_tool_smoke("extract_output_json", tmp_path, monkeypatch)
