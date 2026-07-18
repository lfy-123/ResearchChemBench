from ._helpers import assert_tool_smoke
def test_run_quantum_espresso(tmp_path, monkeypatch): assert_tool_smoke("run_quantum_espresso", tmp_path, monkeypatch)
