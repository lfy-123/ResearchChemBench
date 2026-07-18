from ._helpers import assert_tool_smoke
def test_refine_ensemble_censo(tmp_path, monkeypatch): assert_tool_smoke("refine_ensemble_censo", tmp_path, monkeypatch)
