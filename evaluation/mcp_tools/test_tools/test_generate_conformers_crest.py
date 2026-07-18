from ._helpers import assert_tool_runtime


def test_generate_conformers_crest(tmp_path, monkeypatch):
    assert_tool_runtime("generate_conformers_crest", tmp_path, monkeypatch)

