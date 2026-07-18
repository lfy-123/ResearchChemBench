from ._helpers import assert_tool_runtime


def test_query_pubchem(tmp_path, monkeypatch):
    assert_tool_runtime("query_pubchem", tmp_path, monkeypatch)

