from ._helpers import assert_tool_runtime


def test_list_toolbox_capabilities(tmp_path, monkeypatch):
    assert_tool_runtime("list_toolbox_capabilities", tmp_path, monkeypatch)

