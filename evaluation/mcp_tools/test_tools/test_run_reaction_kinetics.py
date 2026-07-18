from ._helpers import assert_tool_runtime


def test_run_reaction_kinetics(tmp_path, monkeypatch):
    assert_tool_runtime("run_reaction_kinetics", tmp_path, monkeypatch)

