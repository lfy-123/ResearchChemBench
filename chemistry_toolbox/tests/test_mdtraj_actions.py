from __future__ import annotations

import pytest

from researchchem_toolbox.service import execute_action


MULTIMODEL_PDB = """MODEL        1
ATOM      1  N   ALA A   1       0.000   0.000   0.000  1.00  0.00           N
ATOM      2  CA  ALA A   1       1.450   0.000   0.000  1.00  0.00           C
ATOM      3  C   ALA A   1       2.200   1.200   0.000  1.00  0.00           C
ATOM      4  O   ALA A   1       2.000   2.300   0.000  1.00  0.00           O
ATOM      5  N   GLY A   2       3.500   1.100   0.700  1.00  0.00           N
ATOM      6  CA  GLY A   2       4.200   2.300   1.000  1.00  0.00           C
ATOM      7  C   GLY A   2       5.500   2.100   1.400  1.00  0.00           C
ATOM      8  O   GLY A   2       6.000   1.000   1.400  1.00  0.00           O
ENDMDL
MODEL        2
ATOM      1  N   ALA A   1       0.000   0.000   0.000  1.00  0.00           N
ATOM      2  CA  ALA A   1       1.450   0.100   0.000  1.00  0.00           C
ATOM      3  C   ALA A   1       2.200   1.300   0.100  1.00  0.00           C
ATOM      4  O   ALA A   1       2.000   2.400   0.100  1.00  0.00           O
ATOM      5  N   GLY A   2       3.500   1.000   0.900  1.00  0.00           N
ATOM      6  CA  GLY A   2       4.200   2.400   1.100  1.00  0.00           C
ATOM      7  C   GLY A   2       5.500   2.200   1.500  1.00  0.00           C
ATOM      8  O   GLY A   2       6.000   1.100   1.500  1.00  0.00           O
ENDMDL
END
"""


def _request(path, *, inputs=None, settings=None):
    return {
        "backend_id": "mdtraj",
        "inputs": {"trajectory": str(path), "topology": str(path), **(inputs or {})},
        "method_spec": {},
        "action_settings": settings or {},
    }


@pytest.mark.parametrize(
    ("action_id", "inputs", "settings", "result_key"),
    [
        (
            "calculate_trajectory_rmsd", {},
            {"atom_indices": [0, 1, 2, 3, 4], "reference_frame": 0}, "rmsd_angstrom",
        ),
        (
            "calculate_radius_of_gyration", {},
            {"atom_indices": [0, 1, 2, 3, 4]}, "radius_of_gyration_angstrom",
        ),
        (
            "calculate_contacts", {"residue_pairs": [[0, 1]]},
            {"scheme": "closest-heavy", "periodic": False, "soft_min": False}, "distance_angstrom",
        ),
        (
            "calculate_solvent_accessible_surface", {},
            {"mode": "residue", "probe_radius_nm": 0.14, "sphere_points": 120}, "surface_area_nm2",
        ),
        (
            "calculate_dihedral_distribution", {"atom_quartets": [[0, 1, 2, 3]]},
            {"periodic": False}, "angles_radian",
        ),
        (
            "assign_secondary_structure", {},
            {"simplified": True}, "assignments",
        ),
        (
            "cluster_trajectory", {},
            {
                "atom_indices": list(range(8)), "frame_stride": 1,
                "rmsd_cutoff_angstrom": 0.01, "max_clusters": 2,
            },
            "cluster_assignments",
        ),
    ],
)
def test_mdtraj_atomic_trajectory_analyses(
    tmp_path, monkeypatch, action_id, inputs, settings, result_key
):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    path = tmp_path / "trajectory.pdb"
    path.write_text(MULTIMODEL_PDB, encoding="utf-8")
    result = execute_action(action_id, _request(path, inputs=inputs, settings=settings))
    assert result["status"] == "success"
    assert len(result["result"][result_key]) == 2
