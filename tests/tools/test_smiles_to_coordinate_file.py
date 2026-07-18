from ._helpers import assert_tool_smoke
def test_smiles_to_coordinate_file(tmp_path, monkeypatch): assert_tool_smoke("smiles_to_coordinate_file", tmp_path, monkeypatch)
