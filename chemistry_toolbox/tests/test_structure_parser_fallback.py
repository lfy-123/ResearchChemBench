from __future__ import annotations

import builtins
from pathlib import Path

import pytest

from researchchem_toolbox.artifacts import ArtifactStore
from researchchem_toolbox.backends.common import _parse_vasp_structure, structure_dict


def test_vasp_structure_parser_falls_back_to_ase_without_pymatgen(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setenv("RESEARCHCHEM_MCP_WORKSPACE", str(tmp_path))
    structure = tmp_path / "POSCAR"
    structure.write_text(
        "Si\n"
        "1.0\n"
        "5.43 0 0\n"
        "0 5.43 0\n"
        "0 0 5.43\n"
        "Si\n"
        "1\n"
        "Direct\n"
        "0 0 0\n",
        encoding="utf-8",
    )
    original_import = builtins.__import__

    def reject_pymatgen(name, *args, **kwargs):
        if name.startswith("pymatgen"):
            raise ModuleNotFoundError("simulated missing pymatgen")
        return original_import(name, *args, **kwargs)

    monkeypatch.setattr(builtins, "__import__", reject_pymatgen)
    parsed = _parse_vasp_structure(structure)
    assert parsed["atoms"][0]["element"] == "Si"
    assert parsed["pbc"] == [True, True, True]
    assert len(parsed["cell_angstrom"]) == 3


def test_structure_input_rejects_ensemble_artifact_with_actionable_message(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setenv("RESEARCHCHEM_MCP_WORKSPACE", str(tmp_path))
    reference = ArtifactStore().put_json(
        {"conformers": [{"atoms": []}]},
        semantic_type="ConformerEnsemble",
        producer_action="generate_conformer_ensemble",
        producer_backend="rdkit_etkdg",
    )
    with pytest.raises(ValueError, match="Select one conformer/frame"):
        structure_dict(reference.artifact_id)
