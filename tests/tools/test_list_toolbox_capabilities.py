from ._helpers import assert_tool_smoke
def test_list_toolbox_capabilities(tmp_path, monkeypatch): assert_tool_smoke("list_toolbox_capabilities", tmp_path, monkeypatch)
