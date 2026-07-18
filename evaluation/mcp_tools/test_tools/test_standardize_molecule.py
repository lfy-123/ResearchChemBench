from ._helpers import assert_tool_runtime


def test_standardize_molecule(tmp_path, monkeypatch):
    assert_tool_runtime("standardize_molecule", tmp_path, monkeypatch)

