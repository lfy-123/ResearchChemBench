from ._helpers import assert_tool_runtime


def test_query_materials_project(tmp_path, monkeypatch):
    assert_tool_runtime("query_materials_project", tmp_path, monkeypatch)

