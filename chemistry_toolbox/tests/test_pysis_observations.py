from __future__ import annotations

import h5py
import numpy as np
import pytest

from chemistry_toolbox.src.pysis_observations import read_path_hdf5, read_scan_observations


def test_hdf5_path_observation_keeps_synchronized_cycle_and_indices(tmp_path):
    path = tmp_path / "optimization.h5"
    with h5py.File(path, "w") as handle:
        group = handle.create_group("opt")
        group.attrs.update({
            "atoms": np.asarray([b"H", b"H"]),
            "cur_cycle": 1,
            "is_converged": False,
        })
        group.create_dataset("energies", data=np.asarray([[0.0, 0.0], [-1.2, -1.0]]))
        group.create_dataset("image_nums", data=np.asarray([2, 2]))
        group.create_dataset("image_inds", data=np.asarray([[0, 1], [0, 2]]))
        group.create_dataset(
            "cart_coords",
            data=np.asarray([
                [0.0] * 12,
                [0.0, 0.0, 0.0, 1.0, 0.0, 0.0,
                 0.0, 0.0, 0.0, 2.0, 0.0, 0.0],
            ]),
        )
    result = read_path_hdf5(path)
    assert result["status"] == "parsed"
    assert result["cycle"] == 1
    assert result["image_indices"] == [0, 2]
    assert result["frames"][1]["energy_hartree"] == -1.0
    assert result["frames"][1]["source_cycle"] == 1
    assert result["converged"] is False


def test_scan_observation_reports_native_gap_and_rebuild_source():
    result = read_scan_observations(
        "| RUNNING STEP 00, COORD=3.0 AU |\nConverged!\n"
        "Rebuilt internal coordinates!\n"
        "| RUNNING STEP 01, COORD=2.8 AU |\nStep 1 did not converge. Breaking!\n",
        targets=[3.0, 2.8], actuals=[3.016, 2.81], coordinate_unit="angstrom",
        requested_steps=1,
    )
    assert result["points"][0]["delta"] == pytest.approx(0.016)
    assert result["points"][0]["native"]["status"] == "converged"
    assert result["points"][1]["native"]["status"] == "failed"
    assert result["reconstructed_internal_coordinates"][0]["line"] == 3
    assert result["native_status"] == "partial"
