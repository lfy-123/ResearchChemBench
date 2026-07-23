#!/usr/bin/env python3
"""Materialize minimal, decontaminated input data for six P(V) tasks.

Coordinates are copied only from the independent RDKit ETKDG seed generation
performed by ``run_heterobiaryl_feasibility_audit.py``.  The legacy shared ZIP
is read solely for paper-reported experimental measurements; none of its
author-derived coordinates or computational results are used.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import tempfile
from pathlib import Path
from typing import Any
from zipfile import ZipFile


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TASKS_ROOT = PROJECT_ROOT / "tasks"
LEGACY_PUBLIC_ARCHIVE = TASKS_ROOT / "_heterobiaryl_pv_shared" / "public" / "autonomous_inputs.zip"

TASK_SPECS: dict[str, dict[str, Any]] = {
    "Heterobiaryl_PV_01_Protonation": {
        "states": ["P0", "P1", "P2"],
        "measurement_ids": [],
        "purpose": "Protonation-state comparison; three independent seeds per P0/P1/P2 state.",
    },
    "Heterobiaryl_PV_02_CC_Selectivity": {
        "states": ["P0", "P1", "P2"],
        "measurement_ids": [],
        "purpose": "Py-Py versus Ph-Py pathway comparison across P0/P1/P2.",
    },
    "Heterobiaryl_PV_03_CC_vs_CO": {
        "states": ["P2"],
        "measurement_ids": ["E02", "E10", "E11", "E12"],
        "purpose": "P2 Py-Py C-C versus C-O competition with only directly relevant product observations.",
    },
    "Heterobiaryl_PV_04_Coupling_Mechanism": {
        "states": ["P0", "P1", "P2"],
        "measurement_ids": [],
        "purpose": "Mechanism discrimination; all states retained because the task requires calculation-backed protonation-state selection.",
    },
    "Heterobiaryl_PV_05_Rate_Determining_Step": {
        "states": ["P2"],
        "measurement_ids": ["E01", "E02", "E04", "E05", "E06", "E07", "E08", "E09", "E10", "E11", "E12"],
        "purpose": "P2 downstream coupling plus the supplied selectivity, non-detection, rate-series, and alcohol/ethoxide observations.",
    },
    "Heterobiaryl_PV_06_End_to_End": {
        "states": ["P0", "P1", "P2"],
        "measurement_ids": ["E01", "E02", "E04", "E05", "E06", "E07", "E08", "E09", "E10", "E11", "E12"],
        "purpose": "Non-duplicated union of the available inputs needed by Q1-Q5.",
    },
}

SYSTEMS: dict[str, dict[str, Any]] = {
    "P0": {
        "ordered_generation_smiles": "CO[P](c1ccccc1)(c1ccccc1)(c1ccncc1)c1ccncc1",
        "formula": "C23H21N2OP",
        "atom_count": 48,
        "charge": 0,
        "multiplicity": 1,
        "protonated_pyridyl_nitrogen_indices_zero_based": [],
        "generation_random_seed": 20260724,
    },
    "P1": {
        "ordered_generation_smiles": "CO[P](c1ccccc1)(c1ccccc1)(c1cc[nH+]cc1)c1ccncc1",
        "formula": "C23H22N2OP",
        "atom_count": 49,
        "charge": 1,
        "multiplicity": 1,
        "protonated_pyridyl_nitrogen_indices_zero_based": [18],
        "generation_random_seed": 20260725,
    },
    "P2": {
        "ordered_generation_smiles": "CO[P](c1ccccc1)(c1ccccc1)(c1cc[nH+]cc1)c1cc[nH+]cc1",
        "formula": "C23H23N2OP",
        "atom_count": 50,
        "charge": 2,
        "multiplicity": 1,
        "protonated_pyridyl_nitrogen_indices_zero_based": [18, 24],
        "generation_random_seed": 20260726,
    },
}

ATOM_MAP = {
    "indexing": "zero_based",
    "methoxy_carbon": 0,
    "methoxy_oxygen": 1,
    "phosphorus": 2,
    "p_bound_phenyl_ipso_carbons": [3, 9],
    "p_bound_pyridyl_ipso_carbons": [15, 21],
    "pyridyl_nitrogens": [18, 24],
}


def json_bytes(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_xyz_header(path: Path) -> tuple[int, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    return int(lines[0]), lines[1]


def load_measurements() -> list[dict[str, Any]]:
    with ZipFile(LEGACY_PUBLIC_ARCHIVE) as archive:
        payload = json.loads(
            archive.read("experimental_measurements/measurements.json").decode("utf-8")
        )
    return payload["measurements"]


def write_measurements(root: Path, measurements: list[dict[str, Any]]) -> None:
    measurement_root = root / "experimental_measurements"
    measurement_root.mkdir(parents=True, exist_ok=True)
    (measurement_root / "measurements.json").write_bytes(
        json_bytes(
            {
                "data_type": "paper-reported experimental measurements and non-detections",
                "raw_instrument_files_available": False,
                "measurements": measurements,
            }
        )
    )


def task_readme(task_id: str, specification: dict[str, Any], seed_count: int) -> str:
    measurement_note = (
        f"Filtered experimental observations: {', '.join(specification['measurement_ids'])}."
        if specification["measurement_ids"]
        else "No experimental table is needed for this task and none is included."
    )
    q5_gap = ""
    q3_context = ""
    if task_id == "Heterobiaryl_PV_03_CC_vs_CO":
        q3_context = (
            "\nE12 is retained only as a competing protiodephosphination observation under "
            "EtONa conditions, so a C-O interpretation is not made from an incomplete product balance."
        )
    if task_id in {"Heterobiaryl_PV_05_Rate_Determining_Step", "Heterobiaryl_PV_06_End_to_End"}:
        q5_gap = (
            "\nA pre-addition phosphonium/ethanol model, the OMe/Me/H/Cl precursor series, "
            "counterions, and raw kinetic traces are not available and are not silently invented."
        )
    return f"""# Direct task inputs

Purpose: {specification['purpose']}

This directory contains {seed_count} normal XYZ files generated independently from
the ordered generation SMILES and explicit atom-index table in `molecular_systems.json` with the chemistry-toolbox
`generate_conformer_ensemble` Action and the `rdkit_etkdg` backend. The structures
are ETKDG embeddings and have not been geometry-optimized. No author coordinate,
energy, Hessian, transition state, IRC, barrier, product endpoint, or reference
answer is present.

{measurement_note}
{q3_context}

The explicit P(V) ligand is methoxy (P-O-Me). Ethanol is the bulk solvent/protocol;
the coordinates do not contain an ethoxy ligand, explicit solvent, acid, or
counterion. P1/P2 are therefore bare +1/+2 molecular ions in the supplied model.
{q5_gap}
"""


def materialize_task(
    task_id: str,
    specification: dict[str, Any],
    seed_root: Path,
    all_measurements: list[dict[str, Any]],
) -> tuple[int, str]:
    task_root = TASKS_ROOT / task_id
    data_root = task_root / "data"
    old_link = data_root / "autonomous_inputs.zip"
    if old_link.is_symlink() or old_link.is_file():
        old_link.unlink()
    benchmark_root = data_root / "benchmark_data"
    if benchmark_root.exists():
        shutil.rmtree(benchmark_root)
    benchmark_root.mkdir(parents=True)

    selected_systems = {state: SYSTEMS[state] for state in specification["states"]}
    molecular_systems = {
        "schema_version": 1,
        "coordinate_provenance": {
            "action": "generate_conformer_ensemble",
            "backend": "rdkit_etkdg",
            "status": "unoptimized_embedding",
            "author_coordinates_used": False,
            "author_computational_outputs_used": False,
        },
        "atom_map": ATOM_MAP,
        "systems": selected_systems,
    }
    (benchmark_root / "molecular_systems.json").write_bytes(json_bytes(molecular_systems))
    (benchmark_root / "conditions.json").write_bytes(
        json_bytes(
            {
                "temperature_kelvin": 353.15,
                "solution_standard_state_mol_l": 1.0,
                "bulk_solvent": "ethanol",
                "acidic_conditions": True,
                "experimental_acid_protocols": [
                    {
                        "scope": "standard reaction and product observations",
                        "acid": "HCl",
                        "reported_amount": "2 equivalents",
                    },
                    {
                        "scope": "substituent relative-rate series",
                        "acid": "TfOH",
                        "reported_amount": None,
                    },
                ],
                "continuum_model": None,
                "continuum_model_note": "The task fixes the physical solvent but does not prescribe a computational solvation model.",
                "explicit_solvent_molecules": 0,
                "explicit_counterions": 0,
                "explicit_acid_molecules": 0,
                "p_v_alkoxy_ligand_in_coordinates": "methoxy",
            }
        )
    )

    seed_records = []
    for state in specification["states"]:
        for offset in range(1, 4):
            seed_id = f"{state}_SEED_{offset:02d}"
            source = seed_root / state / f"{seed_id}.xyz"
            destination = benchmark_root / "initial_structures" / state / source.name
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)
            atom_count, comment = parse_xyz_header(destination)
            expected = SYSTEMS[state]
            if atom_count != expected["atom_count"]:
                raise ValueError(f"{destination}: expected {expected['atom_count']} atoms, got {atom_count}")
            required_tokens = [
                f"system={state}",
                f"charge={expected['charge']}",
                "multiplicity=1",
                "geometry_status=rdkit_etkdg_unoptimized",
            ]
            if any(token not in comment for token in required_tokens):
                raise ValueError(f"Unexpected XYZ metadata in {destination}: {comment}")
            seed_records.append(
                {
                    "seed_id": seed_id,
                    "state": state,
                    "path": str(destination.relative_to(benchmark_root)),
                    "sha256": sha256(destination),
                    "atom_count": atom_count,
                    "charge": expected["charge"],
                    "multiplicity": expected["multiplicity"],
                    "geometry_status": "rdkit_etkdg_unoptimized",
                    "generation_random_seed": expected["generation_random_seed"],
                }
            )

    selected_ids = set(specification["measurement_ids"])
    selected_measurements = [
        measurement
        for measurement in all_measurements
        if measurement["measurement_id"] in selected_ids
    ]
    if len(selected_measurements) != len(selected_ids):
        missing = sorted(selected_ids - {m["measurement_id"] for m in selected_measurements})
        raise ValueError(f"Missing requested measurements for {task_id}: {missing}")
    if selected_measurements:
        write_measurements(benchmark_root, selected_measurements)

    (benchmark_root / "README.md").write_text(
        task_readme(task_id, specification, len(seed_records)), encoding="utf-8"
    )
    files = []
    for path in sorted(benchmark_root.rglob("*")):
        if path.is_file() and path.name != "input_manifest.json":
            files.append(
                {
                    "path": str(path.relative_to(benchmark_root)),
                    "size_bytes": path.stat().st_size,
                    "sha256": sha256(path),
                }
            )
    manifest = {
        "schema_version": 1,
        "task_id": task_id,
        "purpose": specification["purpose"],
        "unoptimized_seed_count": len(seed_records),
        "states": specification["states"],
        "measurement_ids": specification["measurement_ids"],
        "completed_computational_outputs": 0,
        "optimized_stationary_points": 0,
        "transition_states": 0,
        "reaction_path_outputs": 0,
        "reference_answers": 0,
        "seed_records": seed_records,
        "files": files,
    }
    manifest_path = benchmark_root / "input_manifest.json"
    manifest_path.write_bytes(json_bytes(manifest))
    manifest_sha = sha256(manifest_path)

    task_info_path = task_root / "task_info.json"
    task_info = json.loads(task_info_path.read_text(encoding="utf-8"))
    task_info["archive_extractions"] = []
    task_info["data"] = [
        {
            "name": "Direct Heterobiaryl P(V) task inputs",
            "path": "data/benchmark_data",
            "type": "directory",
            "description": (
                f"{len(seed_records)} independent unoptimized ETKDG seed XYZ files; mapped molecular identity and conditions"
                + (f"; filtered experimental observations {specification['measurement_ids']}" if selected_measurements else "")
                + ". No archive, symlink, completed calculation, stationary point, pathway result, or reference answer is included."
            ),
        }
    ]
    task_info_path.write_bytes(json_bytes(task_info))

    truth_path = task_root / "target_study" / "ground_truth.json"
    truth = json.loads(truth_path.read_text(encoding="utf-8"))
    evidence = truth["reference_evidence"]
    evidence["public_input_contract"] = {
        "unoptimized_seed_count": len(seed_records),
        "states": specification["states"],
        "measurement_ids": specification["measurement_ids"],
        "completed_computational_outputs": 0,
        "optimized_stationary_points": 0,
        "raw_instrument_files": 0,
    }
    evidence.pop("public_archive_sha256", None)
    evidence["input_manifest_sha256"] = manifest_sha
    truth_path.write_bytes(json_bytes(truth))
    return len(seed_records), manifest_sha


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--seed-root",
        type=Path,
        default=None,
    )
    args = parser.parse_args()
    candidates = [
        args.seed_root,
        PROJECT_ROOT / "docs" / "check" / "heterobiaryl_task_feasibility_audit" / "generated_inputs",
        TASKS_ROOT / "Heterobiaryl_PV_06_End_to_End" / "data" / "benchmark_data" / "initial_structures",
    ]
    source_seed_root = next(
        (path.resolve() for path in candidates if path is not None and path.is_dir()),
        None,
    )
    if source_seed_root is None:
        raise FileNotFoundError(
            "No independent seed root found; run scripts/run_heterobiaryl_feasibility_audit.py first"
        )
    all_measurements = load_measurements()
    summary = {}
    with tempfile.TemporaryDirectory(prefix="heterobiaryl_clean_seeds_") as temporary:
        staged_seed_root = Path(temporary)
        for state in ("P0", "P1", "P2"):
            shutil.copytree(source_seed_root / state, staged_seed_root / state)
        for task_id, specification in TASK_SPECS.items():
            seed_count, manifest_sha = materialize_task(
                task_id, specification, staged_seed_root, all_measurements
            )
            summary[task_id] = {
                "unoptimized_seed_count": seed_count,
                "input_manifest_sha256": manifest_sha,
            }
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
