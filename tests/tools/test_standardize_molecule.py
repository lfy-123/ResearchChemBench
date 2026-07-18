from ._helpers import assert_tool_smoke
def test_standardize_molecule(tmp_path, monkeypatch): assert_tool_smoke("standardize_molecule", tmp_path, monkeypatch)
