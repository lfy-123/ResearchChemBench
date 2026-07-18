from ._helpers import assert_tool_smoke
def test_find_transition_state(tmp_path, monkeypatch): assert_tool_smoke("find_transition_state", tmp_path, monkeypatch)
