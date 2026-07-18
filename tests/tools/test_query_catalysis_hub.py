from ._helpers import assert_tool_smoke
def test_query_catalysis_hub(tmp_path, monkeypatch): assert_tool_smoke("query_catalysis_hub", tmp_path, monkeypatch)
