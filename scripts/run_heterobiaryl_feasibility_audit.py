#!/usr/bin/env python3
"""Generate independent P(V) seeds and record real toolbox screening calls.

This audit helper deliberately does not read the paper, hidden ground truth, or
author quantum-chemistry outputs.  Its molecular inputs are explicit SMILES for
the neutral, singly protonated, and doubly protonated pentacoordinate P(V)
system.  Every toolbox request and response is written to the selected audit
directory so the feasibility audit can be replayed and inspected.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
from pathlib import Path
from typing import Any

from researchchem_toolbox.service import execute_action


SYSTEMS: dict[str, dict[str, Any]] = {
    "P0": {
        "smiles": "CO[P](c1ccccc1)(c1ccccc1)(c1ccncc1)c1ccncc1",
        "charge": 0,
        "multiplicity": 1,
        "random_seed": 20260724,
    },
    "P1": {
        "smiles": "CO[P](c1ccccc1)(c1ccccc1)(c1cc[nH+]cc1)c1ccncc1",
        "charge": 1,
        "multiplicity": 1,
        "random_seed": 20260725,
    },
    "P2": {
        "smiles": "CO[P](c1ccccc1)(c1ccccc1)(c1cc[nH+]cc1)c1cc[nH+]cc1",
        "charge": 2,
        "multiplicity": 1,
        "random_seed": 20260726,
    },
}

EXPECTED_ATOM_COUNTS = {"P0": 48, "P1": 49, "P2": 50}
P_ATOM_INDEX = 2
P_LIGAND_ATOM_INDICES = (1, 3, 9, 15, 21)


def dump_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def write_xyz(path: Path, structure: dict[str, Any], comment: str) -> None:
    atoms = structure["atoms"]
    lines = [str(len(atoms)), comment]
    for atom in atoms:
        x, y, z = atom["position_angstrom"]
        lines.append(f"{atom['element']:<2s} {x: .10f} {y: .10f} {z: .10f}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def invoke(
    audit_root: Path,
    call_id: str,
    action_id: str,
    request: dict[str, Any],
) -> dict[str, Any]:
    call_dir = audit_root / "calls" / call_id
    cached_result = call_dir / "result.json"
    if cached_result.is_file():
        return json.loads(cached_result.read_text(encoding="utf-8"))
    dump_json(call_dir / "request.json", {"action_id": action_id, **request})
    result = execute_action(action_id, request)
    dump_json(call_dir / "result.json", result)
    dump_json(
        call_dir / "summary.json",
        {
            "call_id": call_id,
            "action_id": action_id,
            "status": result.get("status"),
            "backend": result.get("backend"),
            "error": result.get("error"),
            "warnings": result.get("warnings", []),
            "output_artifacts": result.get("output_artifacts", []),
            "provenance": result.get("provenance", {}),
        },
    )
    return result


def distance(structure: dict[str, Any], first: int, second: int) -> float:
    atoms = structure["atoms"]
    a = atoms[first]["position_angstrom"]
    b = atoms[second]["position_angstrom"]
    return math.dist(a, b)


def structure_audit(state: str, structure: dict[str, Any]) -> dict[str, Any]:
    atoms = structure["atoms"]
    elements: dict[str, int] = {}
    for atom in atoms:
        element = str(atom["element"])
        elements[element] = elements.get(element, 0) + 1
    p_distances = {
        str(index): distance(structure, P_ATOM_INDEX, index)
        for index in P_LIGAND_ATOM_INDICES
    }
    closest_heavy = sorted(
        (
            distance(structure, P_ATOM_INDEX, index),
            index,
            atom["element"],
        )
        for index, atom in enumerate(atoms)
        if index != P_ATOM_INDEX and atom["element"] != "H"
    )[:8]
    return {
        "state": state,
        "atom_count": len(atoms),
        "expected_atom_count": EXPECTED_ATOM_COUNTS[state],
        "atom_count_matches": len(atoms) == EXPECTED_ATOM_COUNTS[state],
        "element_counts": elements,
        "charge": structure.get("charge"),
        "expected_charge": SYSTEMS[state]["charge"],
        "charge_matches": structure.get("charge") == SYSTEMS[state]["charge"],
        "multiplicity": structure.get("multiplicity"),
        "expected_multiplicity": SYSTEMS[state]["multiplicity"],
        "multiplicity_matches": (
            structure.get("multiplicity") == SYSTEMS[state]["multiplicity"]
        ),
        "phosphorus_atom_index_zero_based": P_ATOM_INDEX,
        "expected_p_ligand_atom_indices_zero_based": list(P_LIGAND_ATOM_INDICES),
        "p_ligand_distances_angstrom": p_distances,
        "closest_heavy_atoms_to_p": [
            {"distance_angstrom": value, "atom_index": index, "element": element}
            for value, index, element in closest_heavy
        ],
    }


def generate_and_screen(audit_root: Path) -> None:
    audit_root.mkdir(parents=True, exist_ok=True)
    os.environ["RESEARCHCHEMBENCH_WORKSPACE"] = str(audit_root.resolve())

    all_screen_rows: list[dict[str, Any]] = []
    selected: dict[str, dict[str, Any]] = {}

    for state, specification in SYSTEMS.items():
        conformer_request = {
            "backend_id": "rdkit_etkdg",
            "inputs": {"molecule": specification["smiles"]},
            "method_spec": {},
            "action_settings": {
                "num_conformers": 3,
                "random_seed": specification["random_seed"],
            },
            "resource_limits": {
                "walltime_seconds": 300,
                "memory_mb": 4096,
                "cpu_cores": 1,
                "gpu_count": 0,
            },
        }
        conformer_result = invoke(
            audit_root,
            f"seed_generation_{state}",
            "generate_conformer_ensemble",
            conformer_request,
        )
        if conformer_result.get("status") != "success":
            continue

        ensemble = conformer_result["result"]["ensemble"]
        for offset, record in enumerate(ensemble, start=1):
            seed_id = f"{state}_SEED_{offset:02d}"
            structure = record["structure"]
            seed_path = audit_root / "generated_inputs" / state / f"{seed_id}.xyz"
            comment = (
                f"seed_id={seed_id} system={state} charge={specification['charge']} "
                f"multiplicity={specification['multiplicity']} "
                "geometry_status=rdkit_etkdg_unoptimized "
                f"random_seed={specification['random_seed']} conformer_id={record['conformer_id']}"
            )
            write_xyz(seed_path, structure, comment)
            seed_audit = structure_audit(state, structure)
            seed_audit.update(
                {
                    "seed_id": seed_id,
                    "xyz_file": str(seed_path.relative_to(audit_root)),
                    "xyz_sha256": file_sha256(seed_path),
                    "canonical_smiles": structure.get("smiles"),
                    "generation_action": "generate_conformer_ensemble",
                    "generation_backend": "rdkit_etkdg",
                    "generation_random_seed": specification["random_seed"],
                }
            )
            dump_json(
                audit_root / "generated_inputs" / state / f"{seed_id}.audit.json",
                seed_audit,
            )

            optimization_request = {
                "backend_id": "xtb",
                "inputs": {"structure": structure},
                "method_spec": {
                    "method": "gfn2",
                    "charge": specification["charge"],
                    "unpaired_electrons": 0,
                },
                "action_settings": {"optimization_level": "loose"},
                "resource_limits": {
                    "walltime_seconds": 900,
                    "memory_mb": 4096,
                    "cpu_cores": 4,
                    "gpu_count": 0,
                },
            }
            optimization_result = invoke(
                audit_root,
                f"seed_screen_{seed_id}",
                "optimize_geometry",
                optimization_request,
            )
            row: dict[str, Any] = {
                "state": state,
                "seed_id": seed_id,
                "seed_xyz": str(seed_path.relative_to(audit_root)),
                "status": optimization_result.get("status"),
                "backend": optimization_result.get("backend"),
                "method": "GFN2-xTB",
                "solvent_model": None,
                "optimization_level": "loose",
            }
            if optimization_result.get("status") == "success":
                optimized = optimization_result["result"]["structure"]
                optimized_path = (
                    audit_root
                    / "calculations"
                    / "seed_screen"
                    / state
                    / seed_id
                    / "optimized.xyz"
                )
                write_xyz(
                    optimized_path,
                    optimized,
                    (
                        f"seed_id={seed_id} system={state} charge={specification['charge']} "
                        "multiplicity=1 optimized_by=xtb method=GFN2-xTB "
                        "optimization_level=loose solvent=none"
                    ),
                )
                row.update(
                    {
                        "converged": optimization_result["result"].get("converged"),
                        "energy_hartree": optimization_result["result"].get("energy"),
                        "optimized_xyz": str(optimized_path.relative_to(audit_root)),
                        "optimized_xyz_sha256": file_sha256(optimized_path),
                        "structure_audit": structure_audit(state, optimized),
                    }
                )
            else:
                row["error"] = optimization_result.get("error")
            all_screen_rows.append(row)

        state_rows = [
            row
            for row in all_screen_rows
            if row["state"] == state and row.get("energy_hartree") is not None
        ]
        if state_rows:
            best = min(state_rows, key=lambda item: item["energy_hartree"])
            selected[state] = best

    for state, best in selected.items():
        specification = SYSTEMS[state]
        optimized_path = audit_root / best["optimized_xyz"]
        hessian_request = {
            "backend_id": "xtb",
            "inputs": {"structure": str(optimized_path.relative_to(audit_root))},
            "method_spec": {
                "method": "gfn2",
                "charge": specification["charge"],
                "unpaired_electrons": 0,
            },
            "action_settings": {},
            "resource_limits": {
                "walltime_seconds": 1800,
                "memory_mb": 8192,
                "cpu_cores": 4,
                "gpu_count": 0,
            },
        }
        hessian_result = invoke(
            audit_root,
            f"minimum_hessian_{state}_{best['seed_id']}",
            "calculate_hessian",
            hessian_request,
        )
        if hessian_result.get("status") != "success":
            continue
        hessian_artifact = next(
            (
                item["artifact_id"]
                for item in hessian_result.get("output_artifacts", [])
                if item.get("semantic_type") == "Hessian"
            ),
            None,
        )
        if not hessian_artifact:
            continue
        vibration_request = {
            "inputs": {
                "hessian": hessian_artifact,
                "structure": str(optimized_path.relative_to(audit_root)),
            },
            "method_spec": {},
            "action_settings": {"linearity": "nonlinear"},
            "resource_limits": {
                "walltime_seconds": 300,
                "memory_mb": 4096,
                "cpu_cores": 1,
                "gpu_count": 0,
            },
        }
        vibration_result = invoke(
            audit_root,
            f"minimum_vibrations_{state}_{best['seed_id']}",
            "derive_vibrational_modes",
            vibration_request,
        )
        if vibration_result.get("status") == "success":
            frequency_records = vibration_result["result"].get("frequencies_cm1", [])
            frequencies = [
                (
                    -float(record.get("imaginary", 0.0))
                    if float(record.get("imaginary", 0.0)) > 0.0
                    else float(record.get("real", 0.0))
                )
                if isinstance(record, dict)
                else float(record)
                for record in frequency_records
            ]
            best["frequency_validation"] = {
                "status": "success",
                "frequency_count": len(frequencies),
                "imaginary_frequency_count": sum(value < 0 for value in frequencies),
                "significant_imaginary_frequency_threshold_cm1": 20.0,
                "significant_imaginary_frequency_count": sum(
                    value < -20.0 for value in frequencies
                ),
                "lowest_frequencies_cm1": sorted(frequencies)[:10],
                "hessian_artifact_id": hessian_artifact,
            }
        else:
            best["frequency_validation"] = {
                "status": vibration_result.get("status"),
                "error": vibration_result.get("error"),
            }

    for state in SYSTEMS:
        rows = [row for row in all_screen_rows if row["state"] == state]
        energies = [row["energy_hartree"] for row in rows if "energy_hartree" in row]
        if not energies:
            continue
        minimum = min(energies)
        for row in rows:
            if "energy_hartree" in row:
                row["relative_energy_kcal_mol"] = (
                    row["energy_hartree"] - minimum
                ) * 627.509474

    dump_json(
        audit_root / "generated_inputs" / "molecular_identity.json",
        {
            "description": (
                "Independent molecular graphs used to generate audit inputs; no author "
                "coordinates, energies, stationary points, or pathway labels were used."
            ),
            "systems": SYSTEMS,
            "atom_indexing_note": (
                "RDKit output ordering is zero-based in JSON. P=2; O=1; P-bound ring "
                "carbons=3,9,15,21; pyridyl nitrogens=18,24."
            ),
        },
    )
    dump_json(audit_root / "calculations" / "seed_screen_summary.json", all_screen_rows)
    dump_json(audit_root / "calculations" / "selected_representatives.json", selected)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--audit-root",
        type=Path,
        default=Path("docs/check/heterobiaryl_task_feasibility_audit"),
    )
    args = parser.parse_args()
    generate_and_screen(args.audit_root.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
