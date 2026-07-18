from ._helpers import assert_tool_runtime


def test_query_rcsb_pdb(tmp_path, monkeypatch):
    assert_tool_runtime("query_rcsb_pdb", tmp_path, monkeypatch)

