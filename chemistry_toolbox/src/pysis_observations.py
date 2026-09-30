"""Small, bounded readers for pysisyphus' native result files.

The readers expose recorded facts only.  They deliberately do not decide whether
an image is a transition state or whether a scan deviation is acceptable.
"""
from __future__ import annotations

import math
import re
from pathlib import Path
from typing import Any

BOHR_TO_ANGSTROM = 0.529177210903
ANGSTROM_TO_BOHR = 1.8897261254578281
_STEP_RE = re.compile(r"\bRUNNING\s+STEP\s+(\d+)\s*,\s*COORD\s*=\s*([-+]?\d*\.?\d+(?:[Ee][-+]?\d+)?)\s*([A-Za-z*^-]+)?", re.I)
_LIMITS = {"max_atoms": 10_000, "max_images": 4_096, "max_cycles": 100_000}


def _finite(values: Any) -> bool:
    try:
        return all(math.isfinite(float(value)) for value in values)
    except (TypeError, ValueError):
        return False


def _element(value: Any) -> str:
    if isinstance(value, bytes):
        value = value.decode("ascii", errors="replace")
    return str(value).strip()


def read_path_hdf5(path: str | Path, *, charge: int = 0, multiplicity: int = 1) -> dict[str, Any]:
    """Read one valid optimizer cycle from an HDF5 chain-of-states result."""
    source = Path(path)
    result: dict[str, Any] = {
        "source": {"path": source.name, "format": "pysisyphus_hdf5", "group": "opt"},
        "observation_gaps": [],
    }
    try:
        import h5py
        import numpy as np
    except ImportError:
        result["observation_gaps"].append("h5py is unavailable; native path history was not read")
        return result
    if not source.is_file():
        result["observation_gaps"].append("optimization.h5 is missing")
        return result
    try:
        with h5py.File(source, "r") as handle:
            group = handle.get("opt")
            if group is None:
                result["observation_gaps"].append("optimization.h5 has no opt group")
                return result
            attrs = group.attrs
            atoms = [_element(value) for value in attrs.get("atoms", [])]
            n_atoms = len(atoms)
            if not 1 <= n_atoms <= _LIMITS["max_atoms"]:
                result["observation_gaps"].append("invalid or unsafe atom count in HDF5 metadata")
                return result
            energies = group.get("energies")
            cart_coords = group.get("cart_coords")
            image_nums = group.get("image_nums")
            image_inds = group.get("image_inds")
            if any(item is None for item in (energies, cart_coords, image_nums, image_inds)):
                result["observation_gaps"].append("HDF5 opt group lacks synchronized energies/coordinates/index datasets")
                return result
            cycle_count = min(int(energies.shape[0]), int(cart_coords.shape[0]), int(image_nums.shape[0]), int(image_inds.shape[0]))
            if cycle_count <= 0 or cycle_count > _LIMITS["max_cycles"]:
                result["observation_gaps"].append("HDF5 cycle count is invalid or exceeds the reader bound")
                return result
            cur_cycle = int(attrs.get("cur_cycle", cycle_count - 1))
            requested_cycle = cur_cycle
            cur_cycle = min(max(cur_cycle, 0), cycle_count - 1)
            if cur_cycle != requested_cycle:
                result["observation_gaps"].append("cur_cycle was outside dataset bounds; selected the last stored cycle")
            selected = None
            for cycle in range(cur_cycle, -1, -1):
                count = int(image_nums[cycle])
                if not 1 <= count <= _LIMITS["max_images"]:
                    continue
                e = np.asarray(energies[cycle, :count], dtype=float)
                c = np.asarray(cart_coords[cycle, : count * n_atoms * 3], dtype=float)
                inds = np.asarray(image_inds[cycle, :count], dtype=int)
                if c.size != count * n_atoms * 3 or len(inds) != count or not _finite(e) or not _finite(c):
                    continue
                selected = (cycle, count, e, c.reshape(count, n_atoms, 3), inds)
                break
            if selected is None:
                result["observation_gaps"].append("no synchronized finite optimizer cycle was available")
                return result
            cycle, count, energies_row, coords_row, indices_row = selected
            if len(set(int(v) for v in indices_row)) != count:
                result["observation_gaps"].append("HDF5 image indices are not unique")
                return result
            frames = []
            for image_position in range(count):
                frame = {
                    "atoms": [
                        {"element": atoms[atom_index], "position_angstrom": [float(v) * BOHR_TO_ANGSTROM for v in coords_row[image_position, atom_index]]}
                        for atom_index in range(n_atoms)
                    ],
                    "charge": int(charge), "multiplicity": int(multiplicity),
                    "energy_hartree": float(energies_row[image_position]),
                    "image_index": int(indices_row[image_position]),
                    "image_position": image_position,
                    "source_cycle": cycle,
                }
                frames.append(frame)
            result.update({
                "status": "parsed", "cycle": cycle, "requested_cycle": requested_cycle,
                "image_count": count, "frames": frames,
                "converged": bool(attrs.get("is_converged", False)),
                "convergence_source": "opt.is_converged",
                "units": {"coordinates": "bohr in HDF5, returned as angstrom", "energy": "hartree"},
                "image_indices": [int(v) for v in indices_row],
            })
            return result
    except (OSError, ValueError, TypeError, KeyError, IndexError) as exc:
        result["observation_gaps"].append(f"HDF5 parse error: {exc}")
        return result


def read_scan_observations(
    stdout: str, *, targets: list[float], actuals: list[float], coordinate_unit: str,
    requested_steps: int, data_file: str | None = None, trajectory_file: str | None = None,
) -> dict[str, Any]:
    """Associate scan points with native log markers without inventing markers."""
    markers = []
    for line_number, line in enumerate(stdout.splitlines(), 1):
        match = _STEP_RE.search(line)
        if match:
            markers.append({"point": int(match.group(1)), "value": float(match.group(2)), "unit": (match.group(3) or "unknown").lower(), "line": line_number, "source": "stdout"})
    reconstructed = []
    for number, line in enumerate(stdout.splitlines(), 1):
        if "rebuilt internal coordinates" not in line.lower():
            continue
        prior = [item for item in markers if int(item["line"]) <= number]
        reconstructed.append({
            "point": prior[-1]["point"] if prior else None,
            "line": number, "message": line.strip(), "source": "stdout",
        })
    lines = stdout.splitlines()
    # Pysisyphus writes the scan point title in a few historical forms.  If a
    # point marker is absent, retain an explicit unknown instead of inferring
    # convergence from the number of rows in relaxed_scan.dat.
    convergence = []
    for point in range(len(actuals)):
        marker = next((item for item in markers if item["point"] == point), None)
        if marker is not None:
            start = int(marker["line"]) - 1
            next_lines = [int(item["line"]) - 1 for item in markers if int(item["line"]) > int(marker["line"])]
            end = min(next_lines) if next_lines else len(lines)
            segment = "\n".join(lines[start:end])
        else:
            segment = ""
        if re.search(r"Number of cycles exceeded|did not converge", segment, re.I):
            status = "failed"
        elif re.search(r"\bConverged!", segment, re.I):
            status = "converged"
        else:
            status = "unknown"
        convergence.append({
            "point": point,
            "status": status,
            "marker": marker,
            "rebuild_events": [item for item in reconstructed if item["point"] == point],
        })
    points = []
    for point, actual in enumerate(actuals):
        target = targets[point] if point < len(targets) else None
        points.append({"point": point, "target": target, "actual": actual, "delta": (actual - target) if target is not None else None, "unit": coordinate_unit, "native": convergence[point]})
    return {
        "points": points, "native_step_markers": markers, "reconstructed_internal_coordinates": reconstructed,
        "data_file": data_file, "trajectory_file": trajectory_file,
        "requested_points": int(requested_steps) + 1, "observed_points": len(actuals),
        "native_status": "converged" if len(actuals) == requested_steps + 1 and all(item["status"] == "converged" for item in convergence) else "partial" if actuals else "unknown",
    }
