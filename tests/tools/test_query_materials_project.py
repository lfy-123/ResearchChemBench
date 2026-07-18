from ._helpers import assert_tool_smoke
def test_query_materials_project(tmp_path, monkeypatch): assert_tool_smoke("query_materials_project", tmp_path, monkeypatch)
