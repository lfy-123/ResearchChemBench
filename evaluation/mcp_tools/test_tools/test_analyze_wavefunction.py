from ._helpers import assert_tool_runtime


def test_analyze_wavefunction(tmp_path, monkeypatch):
    assert_tool_runtime("analyze_wavefunction", tmp_path, monkeypatch)

