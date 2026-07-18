from ._helpers import assert_tool_runtime


def test_smiles_to_coordinate_file(tmp_path, monkeypatch):
    assert_tool_runtime("smiles_to_coordinate_file", tmp_path, monkeypatch)

