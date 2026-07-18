from ._helpers import assert_tool_runtime


def test_molecule_name_to_smiles(tmp_path, monkeypatch):
    assert_tool_runtime("molecule_name_to_smiles", tmp_path, monkeypatch)

