from ._helpers import assert_tool_smoke
def test_prepare_md_system(tmp_path, monkeypatch): assert_tool_smoke("prepare_md_system", tmp_path, monkeypatch)
