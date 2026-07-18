from ._helpers import assert_tool_smoke
def test_compute_thermochemistry(tmp_path, monkeypatch): assert_tool_smoke("compute_thermochemistry", tmp_path, monkeypatch)
