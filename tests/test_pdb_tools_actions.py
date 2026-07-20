from __future__ import annotations

from researchchem_toolbox.service import execute_action


PDB_TEXT = """MODEL        1
ATOM     10  N   ALA A  10       0.000   0.000   0.000  1.00 20.00           N
ATOM     11  CA  ALA A  10       1.450   0.000   0.000  1.00 20.00           C
HETATM   12  O   HOH A 201       2.000   2.000   2.000  1.00 20.00           O
ATOM     20  N   GLY B  20       3.000   0.000   0.000  1.00 20.00           N
ENDMDL
MODEL        2
ATOM     30  N   ALA A  10       0.100   0.000   0.000  1.00 20.00           N
ATOM     31  CA  ALA A  10       1.550   0.000   0.000  1.00 20.00           C
ENDMDL
END
"""


def test_pdb_tools_actions_compose_through_artifacts(tmp_path, monkeypatch):
    (tmp_path / "input.pdb").write_text(PDB_TEXT, encoding="utf-8")
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))

    selected = execute_action(
        "select_structure_subset",
        {
            "inputs": {"structure": "input.pdb"},
            "method_spec": {},
            "action_settings": {
                "chains": ["A"],
                "models": [1],
                "keep_heteroatoms": False,
            },
        },
    )
    assert selected["status"] == "success"
    assert selected["selection_source"] == "internal_deterministic"
    assert selected["result"]["atom_record_count"] == 2
    assert selected["result"]["chains"] == ["A"]

    renumbered = execute_action(
        "renumber_biomolecular_structure",
        {
            "inputs": {"structure": selected["output_artifacts"][0]},
            "method_spec": {},
            "action_settings": {
                "starting_atom_serial": 1,
                "starting_residue_number": 5,
                "hybrid36": False,
            },
        },
    )
    assert renumbered["status"] == "success"

    normalized = execute_action(
        "normalize_pdb_records",
        {
            "inputs": {"structure": renumbered["output_artifacts"][0]},
            "method_spec": {},
            "action_settings": {
                "sort_by": "chain_and_residue",
                "strict_chain_breaks": False,
                "hybrid36": False,
            },
        },
    )
    assert normalized["status"] == "success"
    output = (tmp_path / normalized["result"]["structure_path"]).read_text(encoding="utf-8")
    atom_lines = [line for line in output.splitlines() if line.startswith("ATOM")]
    assert atom_lines[0][6:11].strip() == "1"
    assert atom_lines[0][22:26].strip() == "5"
    assert output.rstrip().endswith("END")
