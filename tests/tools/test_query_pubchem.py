from ._helpers import assert_tool_smoke
def test_query_pubchem(tmp_path, monkeypatch): assert_tool_smoke("query_pubchem", tmp_path, monkeypatch)
