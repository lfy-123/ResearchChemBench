from ._helpers import assert_tool_smoke
def test_analyze_md_trajectory(tmp_path, monkeypatch): assert_tool_smoke("analyze_md_trajectory", tmp_path, monkeypatch)
