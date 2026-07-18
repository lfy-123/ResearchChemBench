from ._helpers import assert_tool_runtime


def test_run_catmap(tmp_path, monkeypatch):
    assert_tool_runtime("run_catmap", tmp_path, monkeypatch)

