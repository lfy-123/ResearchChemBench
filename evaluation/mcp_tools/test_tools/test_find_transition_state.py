from ._helpers import assert_tool_runtime


def test_find_transition_state(tmp_path, monkeypatch):
    assert_tool_runtime("find_transition_state", tmp_path, monkeypatch)

