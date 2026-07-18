from ._helpers import assert_tool_runtime


def test_compute_thermochemistry(tmp_path, monkeypatch):
    assert_tool_runtime("compute_thermochemistry", tmp_path, monkeypatch)

