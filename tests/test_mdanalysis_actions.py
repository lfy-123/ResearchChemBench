from __future__ import annotations

from researchchem_toolbox.service import execute_action


TRAJECTORY = """MODEL        1
ATOM      1  O1  HOH A   1       0.000   0.000   0.000  1.00  0.00           O
ATOM      2  H1  HOH A   1       0.960   0.000   0.000  1.00  0.00           H
ATOM      3  H2  HOH A   1      -0.240   0.930   0.000  1.00  0.00           H
ATOM      4  O2  HOH A   2       2.700   0.000   0.000  1.00  0.00           O
ATOM      5  H3  HOH A   2       3.660   0.000   0.000  1.00  0.00           H
ATOM      6  H4  HOH A   2       2.460   0.930   0.000  1.00  0.00           H
ENDMDL
MODEL        2
ATOM      1  O1  HOH A   1       0.000   0.000   0.000  1.00  0.00           O
ATOM      2  H1  HOH A   1       0.960   0.050   0.000  1.00  0.00           H
ATOM      3  H2  HOH A   1      -0.240   0.930   0.050  1.00  0.00           H
ATOM      4  O2  HOH A   2       2.750   0.050   0.000  1.00  0.00           O
ATOM      5  H3  HOH A   2       3.710   0.050   0.000  1.00  0.00           H
ATOM      6  H4  HOH A   2       2.510   0.980   0.000  1.00  0.00           H
ENDMDL
END
"""


def _request(path, settings, inputs=None):
    return {
        "backend_id": "mdanalysis",
        "inputs": {"trajectory": str(path), "topology": str(path), **(inputs or {})},
        "method_spec": {},
        "action_settings": settings,
    }


def test_mdanalysis_hydrogen_bonds_use_explicit_geometry_and_selections(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    path = tmp_path / "waters.pdb"
    path.write_text(TRAJECTORY, encoding="utf-8")
    result = execute_action(
        "calculate_hydrogen_bonds",
        _request(
            path,
            {
                "donor_selection": "name O1",
                "hydrogen_selection": "name H1",
                "acceptor_selection": "name O2",
                "donor_hydrogen_cutoff_angstrom": 1.2,
                "donor_acceptor_cutoff_angstrom": 3.0,
                "angle_cutoff_degrees": 150.0,
                "update_selections": False,
                "start_frame": 0,
                "stop_frame": -1,
                "frame_stride": 1,
                "max_events": 100,
            },
        ),
    )
    assert result["status"] == "success"
    assert result["result"]["event_count"] == 2
    assert result["result"]["counts_by_frame"] == [1, 1]


def test_mdanalysis_pca_and_dynamic_cross_correlation(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    path = tmp_path / "waters.pdb"
    path.write_text(TRAJECTORY, encoding="utf-8")
    pca = execute_action(
        "calculate_principal_components",
        _request(
            path,
            {
                "selection": "name O1 O2",
                "align": False,
                "n_components": 1,
                "start_frame": 0,
                "stop_frame": -1,
                "frame_stride": 1,
                "include_eigenvectors": True,
                "max_atoms": 10,
            },
        ),
    )
    assert pca["status"] == "success"
    assert pca["result"]["component_count"] == 1
    assert len(pca["result"]["frame_projections"]) == 2
    assert len(pca["result"]["eigenvectors"]) == 6

    correlation = execute_action(
        "calculate_dynamic_cross_correlation",
        _request(
            path,
            {
                "selection": "name O1 O2",
                "align": False,
                "alignment_selection": "name O1 O2",
                "reference_frame": 0,
                "start_frame": 0,
                "stop_frame": -1,
                "frame_stride": 1,
                "max_atoms": 10,
            },
        ),
    )
    assert correlation["status"] == "success"
    assert correlation["result"]["frame_count"] == 2
    assert len(correlation["result"]["matrix"]) == 2
    assert len(correlation["result"]["matrix"][0]) == 2
