from ._helpers import assert_tool_smoke
def test_run_reaction_kinetics(tmp_path, monkeypatch): assert_tool_smoke("run_reaction_kinetics", tmp_path, monkeypatch)
