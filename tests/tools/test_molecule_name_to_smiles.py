from ._helpers import assert_tool_smoke
def test_molecule_name_to_smiles(tmp_path, monkeypatch): assert_tool_smoke("molecule_name_to_smiles", tmp_path, monkeypatch)
