from ._helpers import assert_tool_runtime


def test_query_catalysis_hub(tmp_path, monkeypatch):
    assert_tool_runtime("query_catalysis_hub", tmp_path, monkeypatch)

