from ._helpers import assert_tool_runtime


def test_refine_ensemble_censo(tmp_path, monkeypatch):
    assert_tool_runtime("refine_ensemble_censo", tmp_path, monkeypatch)

