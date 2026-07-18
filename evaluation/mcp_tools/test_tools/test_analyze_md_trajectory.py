from ._helpers import assert_tool_runtime


def test_analyze_md_trajectory(tmp_path, monkeypatch):
    assert_tool_runtime("analyze_md_trajectory", tmp_path, monkeypatch)

