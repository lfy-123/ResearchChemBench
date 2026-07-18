from ._helpers import assert_tool_runtime


def test_generate_3d_structure(tmp_path, monkeypatch):
    assert_tool_runtime("generate_3d_structure", tmp_path, monkeypatch)

