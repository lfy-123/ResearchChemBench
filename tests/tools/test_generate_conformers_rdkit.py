from ._helpers import assert_tool_smoke
def test_generate_conformers_rdkit(tmp_path, monkeypatch): assert_tool_smoke("generate_conformers_rdkit", tmp_path, monkeypatch)
