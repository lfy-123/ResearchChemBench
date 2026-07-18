from ._helpers import assert_tool_runtime


def test_prepare_md_system(tmp_path, monkeypatch):
    assert_tool_runtime("prepare_md_system", tmp_path, monkeypatch)

