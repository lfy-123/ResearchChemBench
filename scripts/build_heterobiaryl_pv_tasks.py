#!/usr/bin/env python3
"""Build six P(V) benchmark tasks that require new, observable computation.

The public package intentionally contains no completed quantum-chemistry output,
optimized stationary point, energy, frequency, pathway label, or literature target.
Author calculations remain under the hidden reference tree for scoring and audit.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import os
import random
import re
import stat
import tempfile
from collections import Counter
from pathlib import Path, PurePosixPath
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo


PROJECT_ROOT = Path(__file__).resolve().parents[1]
TASKS_ROOT = PROJECT_ROOT / "tasks"
SOURCE_ARCHIVE = TASKS_ROOT / "Heterobiaryl_PV_Benchmark.zip"
SOURCE_ROOT = "Heterobiaryl_PV_Benchmark"
SHARED_ROOT = TASKS_ROOT / "_heterobiaryl_pv_shared"
PUBLIC_ARCHIVE = SHARED_ROOT / "public" / "autonomous_inputs.zip"
LEGACY_PUBLIC_ARCHIVE = SHARED_ROOT / "public" / "computational_records.zip"
REFERENCE_ROOT = SHARED_ROOT / "reference"
REFERENCE_OUTPUT_ROOT = REFERENCE_ROOT / "author_computational_outputs"

TASK_IDS = (
    "Heterobiaryl_PV_01_Protonation",
    "Heterobiaryl_PV_02_CC_Selectivity",
    "Heterobiaryl_PV_03_CC_vs_CO",
    "Heterobiaryl_PV_04_Coupling_Mechanism",
    "Heterobiaryl_PV_05_Rate_Determining_Step",
    "Heterobiaryl_PV_06_End_to_End",
)

FORBIDDEN_PROMPT_TERMS = (
    "gaussian",
    "orca",
    "goodvibes",
    "xtb",
    "backend",
    "action",
    "mcp",
    "calculate_energy",
    "calculate_hessian",
    "derive_thermochemistry",
)

PUBLIC_LEAK_PATTERNS = tuple(
    re.compile(pattern, re.IGNORECASE)
    for pattern in (
        r"jvalegre",
        r"colostate",
        r"mcnally",
        r"paton",
        r"alegre-requena",
        r"hilton",
        r"aas8961",
        r"1439888",
        r"TS[-_ ]?I",
        r"Int[-_ ]?(?:II|III|IV)",
        r"SCF Done",
        r"FINAL SINGLE POINT ENERGY",
        r"Frequencies\s*--",
        r"thermal free energy",
        r"Sum of electronic and thermal",
        r"DLPNO-CCSD",
        r"omegaB97",
        r"def2-QZVPP",
        r"imaginary frequenc",
    )
)

PUBLIC_ALLOWED_SUFFIXES = {".csv", ".json", ".md", ".xyz"}
PUBLIC_SEED_IDS = {
    "P0": ("P0_S001", "P0_S002", "P0_S003"),
    "P1": ("P1_S001", "P1_S002", "P1_S003"),
    "P2": ("P2_S001", "P2_S002", "P2_S003"),
}


def _json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def _sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def _normalized_reference_bytes(name: str, data: bytes) -> bytes:
    if PurePosixPath(name).suffix.casefold() not in {".csv", ".json", ".md"}:
        return data
    text = data.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
    return (text.rstrip() + "\n").encode("utf-8")


def _safe_outer_archive(path: Path) -> None:
    with ZipFile(path) as archive:
        for info in archive.infolist():
            member = PurePosixPath(info.filename)
            if member.is_absolute() or ".." in member.parts or "\\" in info.filename:
                raise ValueError(f"Unsafe source archive member: {info.filename!r}")


def _write_deterministic_zip(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(".tmp.zip")
    with ZipFile(temporary, "w", compression=ZIP_DEFLATED, compresslevel=6) as archive:
        for path in sorted(item for item in source.rglob("*") if item.is_file()):
            relative = path.relative_to(source).as_posix()
            info = ZipInfo(relative, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(
                info,
                path.read_bytes(),
                compress_type=ZIP_DEFLATED,
                compresslevel=6,
            )
    temporary.replace(destination)


def _parse_xyz(data: bytes) -> tuple[list[str], list[list[float]]]:
    lines = data.decode("utf-8").splitlines()
    atom_count = int(lines[0].strip())
    symbols: list[str] = []
    coordinates: list[list[float]] = []
    for line in lines[2 : 2 + atom_count]:
        fields = line.split()
        symbols.append(fields[0])
        coordinates.append([float(value) for value in fields[1:4]])
    if len(symbols) != atom_count:
        raise ValueError("Incomplete XYZ structure")
    return symbols, coordinates


def _perturbed_seed_xyz(
    source: bytes,
    *,
    public_id: str,
    system: str,
    charge: int,
    multiplicity: int,
) -> bytes:
    """Create a deterministic non-stationary input geometry from a connectivity seed."""

    symbols, coordinates = _parse_xyz(source)
    rng = random.Random(int(hashlib.sha256(public_id.encode()).hexdigest()[:16], 16))
    displacements = [
        [rng.uniform(-0.14, 0.14) for _axis in range(3)] for _atom in symbols
    ]
    means = [sum(row[axis] for row in displacements) / len(displacements) for axis in range(3)]
    perturbed = [
        [
            coordinate[axis] + displacement[axis] - means[axis]
            for axis in range(3)
        ]
        for coordinate, displacement in zip(coordinates, displacements)
    ]
    lines = [
        str(len(symbols)),
        (
            f"seed_id={public_id} system={system} charge={charge} "
            f"multiplicity={multiplicity} geometry_status=generated_unoptimized_seed"
        ),
    ]
    lines.extend(
        f"{symbol:<2s} {row[0]: .10f} {row[1]: .10f} {row[2]: .10f}"
        for symbol, row in zip(symbols, perturbed)
    )
    return ("\n".join(lines) + "\n").encode("utf-8")


def _structure_index_metadata(data: bytes) -> dict[str, object]:
    symbols, coordinates = _parse_xyz(data)
    phosphorus = [index for index, symbol in enumerate(symbols) if symbol == "P"]
    oxygen = [index for index, symbol in enumerate(symbols) if symbol == "O"]
    nitrogen = [index for index, symbol in enumerate(symbols) if symbol == "N"]
    if len(phosphorus) != 1:
        raise ValueError("Expected exactly one phosphorus atom")
    p_index = phosphorus[0]
    p_coordinate = coordinates[p_index]
    neighbours = []
    for index, (symbol, coordinate) in enumerate(zip(symbols, coordinates)):
        if index == p_index or symbol not in {"C", "N", "O"}:
            continue
        distance = math.dist(p_coordinate, coordinate)
        cutoff = 2.25 if symbol in {"C", "N"} else 2.10
        if distance <= cutoff:
            neighbours.append(
                {"atom_index": index, "element": symbol, "distance_angstrom": round(distance, 4)}
            )
    return {
        "indexing": "zero_based",
        "phosphorus_atom_index": p_index,
        "oxygen_atom_indices": oxygen,
        "nitrogen_atom_indices": nitrogen,
        "initial_phosphorus_neighbours": neighbours,
        "note": (
            "Indices and initial distances describe only the supplied seed geometry. They are not "
            "optimized values, stationary-point labels, bond orders, or pathway assignments."
        ),
    }


def _clean_experimental_rows(outer: ZipFile) -> list[dict[str, str]]:
    prefix = f"{SOURCE_ROOT}/01_agent_tasks_and_data/experimental_evidence"
    text = outer.read(f"{prefix}/experimental_observations.csv").decode("utf-8")
    rows = list(csv.DictReader(io.StringIO(text)))
    cleaned = []
    for row in rows:
        # E03 is an author interpretation without an archived spectrum or numeric shift table.
        # It remains in the hidden reference, not in the public measurement table.
        if row.get("evidence_id") == "E03":
            continue
        cleaned.append(
            {
                "measurement_id": row.get("evidence_id", ""),
                "category": row.get("category", ""),
                "condition": row.get("system_or_condition", ""),
                "reported_observation": row.get("observation", ""),
                "reported_value": row.get("value", ""),
                "unit": row.get("unit", ""),
                "measurement_scope": "paper_reported_measurement_or_non_detection",
            }
        )
    return cleaned


def _build_public_archive(outer: ZipFile, destination: Path) -> dict[str, object]:
    prefix = f"{SOURCE_ROOT}/01_agent_tasks_and_data/task_inputs"
    starting_manifest = json.loads(
        outer.read(f"{prefix}/starting_structure_manifest.json")
    )
    by_id = {item["starting_id"]: item for item in starting_manifest["structures"]}
    missing = sorted(
        seed_id
        for values in PUBLIC_SEED_IDS.values()
        for seed_id in values
        if seed_id not in by_id
    )
    if missing:
        raise FileNotFoundError(f"Missing selected seed structures: {missing}")
    experimental_rows = _clean_experimental_rows(outer)

    with tempfile.TemporaryDirectory(prefix="heterobiaryl_autonomous_inputs_") as temporary:
        root = Path(temporary)
        (root / "initial_structures").mkdir(parents=True)
        (root / "experimental_measurements").mkdir(parents=True)
        public_structures: list[dict[str, object]] = []

        for system, source_ids in PUBLIC_SEED_IDS.items():
            for offset, source_id in enumerate(source_ids, start=1):
                source_record = by_id[source_id]
                public_id = f"{system}_SEED_{offset:02d}"
                source_path = f"{prefix}/{source_record['xyz_file']}"
                seed_data = _perturbed_seed_xyz(
                    outer.read(source_path),
                    public_id=public_id,
                    system=system,
                    charge=int(source_record["charge"]),
                    multiplicity=int(source_record["multiplicity"]),
                )
                target_relative = f"initial_structures/{system}/{public_id}.xyz"
                target = root / target_relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(seed_data)
                public_structures.append(
                    {
                        "seed_id": public_id,
                        "system": system,
                        "charge": int(source_record["charge"]),
                        "multiplicity": int(source_record["multiplicity"]),
                        "atom_count": int(source_record["atom_count"]),
                        "xyz_file": target_relative,
                        "xyz_sha256": _sha256_bytes(seed_data),
                        "geometry_status": "generated_unoptimized_seed",
                        "atom_index_metadata": _structure_index_metadata(seed_data),
                    }
                )

        manifest = {
            "schema_version": 2,
            "description": (
                "Nine deliberately perturbed, unoptimized molecular seeds: three for each "
                "protonation state. They provide composition and starting coordinates only."
            ),
            "selection_rule": (
                "The first three lexicographic source conformers in each protonation state were "
                "selected before consulting energies or pathway labels, anonymized, and perturbed."
            ),
            "seed_count": len(public_structures),
            "structures": public_structures,
        }
        (root / "initial_structure_manifest.json").write_bytes(_json_bytes(manifest))

        system_definition = {
            "system_family": "anonymous_pentacoordinate_PV_ligand_coupling_model",
            "molecular_composition": (
                "Each seed contains one pentacoordinate phosphorus center, two pyridyl-derived "
                "ligands, two phenyl ligands, and one methoxy ligand."
            ),
            "protonation_states": {
                "P0": {"charge": 0, "multiplicity": 1, "protonated_pyridyl_nitrogens": 0},
                "P1": {"charge": 1, "multiplicity": 1, "protonated_pyridyl_nitrogens": 1},
                "P2": {"charge": 2, "multiplicity": 1, "protonated_pyridyl_nitrogens": 2},
            },
            "scientific_hypotheses_to_test": [
                "pyridyl-pyridyl carbon-carbon ligand coupling",
                "phenyl-pyridyl carbon-carbon ligand coupling",
                "competitive carbon-oxygen coupling",
                "concerted versus stepwise and synchronous versus asynchronous bond reorganization",
            ],
            "experimental_conditions": {
                "solvent": "ethanol",
                "temperature_kelvin": 353.15,
                "solution_standard_state_mol_l": 1.0,
                "acidic_conditions": True,
            },
            "important_boundary": (
                "The hypotheses are alternatives, not labels or conclusions. No preferred pathway, "
                "stationary point, reaction coordinate, or numerical target is supplied."
            ),
        }
        (root / "chemical_system.json").write_bytes(_json_bytes(system_definition))

        fieldnames = list(experimental_rows[0])
        buffer = io.StringIO()
        writer = csv.DictWriter(buffer, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(experimental_rows)
        (root / "experimental_measurements" / "measurements.csv").write_text(
            buffer.getvalue(), encoding="utf-8"
        )
        (root / "experimental_measurements" / "measurements.json").write_bytes(
            _json_bytes(
                {
                    "data_type": "paper-reported measurements and non-detections",
                    "raw_instrument_files_available": False,
                    "measurements": experimental_rows,
                }
            )
        )

        data_scope = {
            "agent_visible": [
                "nine generated unoptimized molecular seed geometries",
                "charges, multiplicities, atom indices, and experimental conditions",
                "paper-reported yields, relative rates, and qualitative non-detections",
            ],
            "intentionally_absent": [
                "optimized geometries",
                "transition-state guesses or stationary-point labels",
                "electronic energies or free energies",
                "frequency or Hessian results",
                "reaction-coordinate trajectories",
                "bond-order or population-analysis results",
                "author input or output files",
                "published barrier values, pathway rankings, and mechanism conclusions",
            ],
            "experimental_limitation": (
                "The source package does not contain raw NMR FID, chromatograms, or time-resolved "
                "kinetic traces. Public measurements are neutral paper-level reports, not raw files."
            ),
            "evaluation_intent": (
                "Scientific conclusions must be supported by new computations and artifacts created "
                "during the Agent run; reading the input package alone cannot establish them."
            ),
        }
        (root / "data_scope.json").write_bytes(_json_bytes(data_scope))
        (root / "README.md").write_text(
            "# Autonomous P(V) computation input package\n\n"
            "This package contains only experimental measurements, chemical-system metadata, and "
            "deliberately unoptimized starting geometries. It contains no completed quantum-chemistry "
            "calculation or reference answer. Inspect `data_scope.json` before planning calculations.\n",
            encoding="utf-8",
        )
        _write_deterministic_zip(root, destination)

    return _verify_public_archive(destination)


def _verify_public_archive(path: Path) -> dict[str, object]:
    with ZipFile(path) as archive:
        infos = archive.infolist()
        names = [info.filename for info in infos]
        if len(names) != len(set(names)):
            raise ValueError("Public archive contains duplicate member names")
        for info in infos:
            member = PurePosixPath(info.filename)
            mode = (info.external_attr >> 16) & 0o170000
            suffix = member.suffix.casefold()
            if (
                not info.filename
                or member.is_absolute()
                or ".." in member.parts
                or "\\" in info.filename
                or "\x00" in info.filename
                or (mode and mode not in {stat.S_IFREG, stat.S_IFDIR})
                or (not info.is_dir() and suffix not in PUBLIC_ALLOWED_SUFFIXES)
            ):
                raise ValueError(f"Unsafe or forbidden public archive member: {info.filename!r}")
            if any(part in {"records", "structures", "candidate_structures"} for part in member.parts):
                raise ValueError(f"Completed-result directory leaked publicly: {info.filename!r}")
            if info.is_dir():
                continue
            text = archive.read(info).decode("utf-8", errors="replace")
            for pattern in PUBLIC_LEAK_PATTERNS:
                if pattern.search(text):
                    raise ValueError(
                        f"Public archive member {info.filename!r} contains result leak "
                        f"pattern {pattern.pattern!r}"
                    )

        manifest = json.loads(archive.read("initial_structure_manifest.json"))
        structures = manifest["structures"]
        if manifest["seed_count"] != 9 or len(structures) != 9:
            raise ValueError("Public seed manifest must contain exactly nine structures")
        for item in structures:
            data = archive.read(item["xyz_file"])
            if _sha256_bytes(data) != item["xyz_sha256"]:
                raise ValueError(f"Structure hash mismatch for {item['seed_id']}")
            if b"generated_unoptimized_seed" not in data.splitlines()[1]:
                raise ValueError(f"Seed status missing for {item['seed_id']}")
        counts = Counter(item["system"] for item in structures)
        if counts != Counter({"P0": 3, "P1": 3, "P2": 3}):
            raise ValueError(f"Unexpected public seed balance: {counts}")

        metadata = {
            "archive_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "archive_size_bytes": path.stat().st_size,
            "archive_entry_count": len(infos),
            "archive_uncompressed_bytes": sum(info.file_size for info in infos),
            "public_seed_count": len(structures),
            "systems": dict(counts),
            "completed_computational_output_count": 0,
            "optimized_structure_count": 0,
            "result_leak_scan_passed": True,
            "integrity_scan_passed": True,
        }
        return metadata


def _extract_references(
    outer: ZipFile,
    source_sha256: str,
    public_meta: dict[str, object],
) -> dict[str, object]:
    REFERENCE_ROOT.mkdir(parents=True, exist_ok=True)
    selected_prefixes = (f"{SOURCE_ROOT}/02_hidden_reference_answers/gold_answers/",)
    selected_files = {
        f"{SOURCE_ROOT}/02_hidden_reference_answers/paper/Heterobiaryl_synthesis_by_contractive_CC_coupling_via_PV_intermediates.pdf": "paper.pdf",
        f"{SOURCE_ROOT}/02_hidden_reference_answers/sources/Figure_2.jpg": "Figure_2.jpg",
        f"{SOURCE_ROOT}/02_hidden_reference_answers/sources/zenodo_1439888_metadata.json": "zenodo_1439888_metadata.json",
        f"{SOURCE_ROOT}/02_hidden_reference_answers/sources/zenodo_3674160_metadata.json": "zenodo_3674160_metadata.json",
        f"{SOURCE_ROOT}/02_hidden_reference_answers/sources/SOURCE_MANIFEST.md": "SOURCE_MANIFEST_ORIGINAL.md",
    }
    for source, relative in selected_files.items():
        (REFERENCE_ROOT / relative).write_bytes(
            _normalized_reference_bytes(relative, outer.read(source))
        )
    for name in outer.namelist():
        if not any(name.startswith(prefix) for prefix in selected_prefixes):
            continue
        if name.endswith("/") or name.startswith("__MACOSX"):
            continue
        relative = Path(name).relative_to(f"{SOURCE_ROOT}/02_hidden_reference_answers")
        target = REFERENCE_ROOT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(_normalized_reference_bytes(name, outer.read(name)))

    REFERENCE_OUTPUT_ROOT.mkdir(parents=True, exist_ok=True)
    output_manifest = []
    for filename in (
        "Int-I_unprotonated.zip",
        "Int-I_H_plus.zip",
        "Int-I_2H_2plus.zip",
    ):
        source = f"{SOURCE_ROOT}/02_hidden_reference_answers/zenodo_outputs/{filename}"
        data = outer.read(source)
        target = REFERENCE_OUTPUT_ROOT / filename
        target.write_bytes(data)
        output_manifest.append(
            {
                "file": target.relative_to(REFERENCE_ROOT).as_posix(),
                "sha256": _sha256_bytes(data),
                "size_bytes": len(data),
                "agent_visible": False,
            }
        )
    (REFERENCE_OUTPUT_ROOT / "manifest.json").write_bytes(
        _json_bytes(
            {
                "description": (
                    "Hidden author computational archives used only for scoring, reference "
                    "comparison, and post-run audit. They are never copied to an Agent workspace."
                ),
                "archives": output_manifest,
            }
        )
    )

    recomputed = {
        "conditions": {"temperature_K": 353.15, "standard_state_M": 1.0, "solvent": "ethanol"},
        "profiles_kcal_mol": {
            "P0": {"BiPy_dG_dagger": 30.91, "PhPy_dG_dagger": 37.32, "delta_delta_G_dagger": 6.41, "BiPy_dG_reaction": -32.38, "PhPy_dG_reaction": -32.54},
            "P1": {"BiPy_dG_dagger": 19.81, "PhPy_dG_dagger": 26.86, "delta_delta_G_dagger": 7.05, "BiPy_dG_reaction": -30.53, "PhPy_dG_reaction": -28.51},
            "P2": {"BiPy_dG_dagger": 14.30, "PhPy_dG_dagger": 25.57, "delta_delta_G_dagger": 11.27, "BiPy_dG_reaction": -31.35, "PhPy_dG_reaction": -31.85},
        },
        "interpretation": (
            "These are hidden high-level comparison values, not mandatory outputs for a lower-cost "
            "independent run. Method-dependent deviations are acceptable when provenance is complete."
        ),
    }
    (REFERENCE_ROOT / "recomputed_reference_353K_1M.json").write_bytes(
        _json_bytes(recomputed)
    )
    audit = f"""# Heterobiaryl P(V) autonomous-computation curation audit

- Source archive SHA-256: `{source_sha256}`
- Agent-visible archive SHA-256: `{public_meta['archive_sha256']}`
- Agent-visible archive size: {public_meta['archive_size_bytes']} bytes
- Public unoptimized seeds: {public_meta['public_seed_count']}
- Public completed computational outputs: **0**
- Public optimized stationary-point structures: **0**
- Hidden author output archives: {len(output_manifest)}
- Integrity and result-leak scans: passed

## Fairness decisions

1. All completed Gaussian/ORCA-style outputs, optimized candidate structures, frequencies, energies, labels, and pathway rankings are hidden reference assets.
2. The public geometry seeds are deterministic perturbations, not author stationary points. Their IDs contain no pathway role.
3. The source package has no raw NMR FID, chromatograms, or time-resolved kinetic traces. Only neutral paper-reported measurements are public; the interpretive dual-protonation statement without raw numeric shifts is hidden.
4. Tasks require newly generated calculation artifacts. Reading inputs or writing a plausible narrative cannot earn the computation/orchestration score.
5. Exact software, predefined Actions, method, and invocation order are never named in a tested task prompt. All three managed toolbox layers remain valid.
6. Hidden high-level literature values are comparison targets, not mandatory equality constraints for resource-aware independent calculations.
"""
    (REFERENCE_ROOT / "CURATION_AUDIT.md").write_text(audit, encoding="utf-8")
    return {"hidden_output_archives": output_manifest}


def _rubric(*rows: tuple[str, int, str]) -> list[dict[str, object]]:
    if sum(row[1] for row in rows) != 100:
        raise ValueError("Rubric weights must sum to 100")
    return [
        {"id": identifier, "max_score": maximum, "criterion": criterion}
        for identifier, maximum, criterion in rows
    ]


def _task_definitions(archive_sha256: str) -> dict[str, tuple[dict, dict]]:
    common_archive = [
        {
            "source": "autonomous_inputs.zip",
            "destination": "benchmark_data",
            "format": "zip",
            "sha256": archive_sha256,
        }
    ]
    common_data = [
        {
            "name": "P(V) autonomous-computation inputs",
            "path": "data/benchmark_data",
            "type": "directory",
            "description": (
                "Nine unoptimized molecular seeds, chemical-system metadata, experimental "
                "conditions, and paper-reported measurements. No completed calculation is included."
            ),
        }
    ]
    prompts = {
        TASK_IDS[0]: (
            "Starting only from the supplied unoptimized neutral, singly protonated, and doubly "
            "protonated P(V) seeds, independently test how successive N-protonation changes the "
            "activation free energy of pyridyl-pyridyl ligand coupling. The three seeds in each "
            "protonation class are alternative starting guesses, not completed results; use your "
            "own staged screening to choose which representatives merit refinement rather than "
            "exhaustively calculating every seed without evidence. Formulate a resource-aware "
            "calculation plan, generate and validate the necessary reactant and transition-region "
            "evidence, and compare all states at 353.15 K and a 1 M solution standard state. Explain "
            "the structural or electronic origin of the trend. This is a calculation-and-tool-"
            "orchestration task: reading or tabulating the supplied metadata is only preparation "
            "and cannot establish the answer. Every numerical claim must point to "
            "an artifact generated in this run; if a full pathway cannot be established, report the "
            "strongest computed bound and the missing validation instead of using a literature value."
        ),
        TASK_IDS[1]: (
            "Starting from the supplied unoptimized P(V) seeds, independently determine whether "
            "pyridyl-pyridyl coupling is preferred over phenyl-pyridyl coupling for kinetic or "
            "thermodynamic reasons in each protonation state. The three seeds in each protonation "
            "class are alternative starting guesses, not completed results; screen them and refine "
            "only representatives justified by your own intermediate calculations. Construct and "
            "test competing pathways, "
            "validate any claimed stationary points, and compare activation and reaction free energies "
            "under one 353.15 K, 1 M convention. Use a staged calculation strategy appropriate to the "
            "available resources. The central evidence must come from new managed chemical calculations "
            "and their artifacts, not from descriptive analysis of the input files. Do not substitute "
            "remembered or published values for calculations "
            "performed during this run."
        ),
        TASK_IDS[2]: (
            "For the doubly protonated P(V) system, independently compare pyridyl-pyridyl carbon-carbon "
            "coupling with competitive carbon-oxygen coupling under the supplied acidic ethanol "
            "conditions. The supplied P2 structures are alternative unoptimized starting guesses; "
            "use a staged screen to select representatives and then generate and test the pathway "
            "candidates needed for a comparable energetic prediction of dominant and minor products. "
            "Separate newly "
            "calculated results, experimental constraints, failed searches, and unresolved uncertainty. "
            "This is not a measurement-table interpretation task: both competing-path claims require "
            "new managed chemical computation or an explicitly documented failed computation that "
            "establishes a defensible bound. "
            "No precise barrier may be reported unless it is supported by an artifact created in this run."
        ),
        TASK_IDS[3]: (
            "Use new calculations beginning from the supplied alternative unoptimized P(V) seeds to determine "
            "whether the key pyridyl-pyridyl ligand-coupling event is concerted or stepwise and "
            "synchronous or asynchronous. Use a resource-aware screen to choose starting representatives, "
            "then establish the most defensible stationary-point sequence, "
            "test transition-state connectivity, follow the forming carbon-carbon bond and relevant "
            "phosphorus-carbon bonds, and assess whether a dearomatized intermediate and oxygen "
            "participation are supported. Input-file inspection alone cannot answer the task. Tie every "
            "mechanistic claim to a newly generated managed structural, vibrational, reaction-path, "
            "or electronic artifact, and label any branch that could not be validated."
        ),
        TASK_IDS[4]: (
            "Use the supplied experimental measurements as constraints on a new calculation-backed "
            "test of the most likely rate-determining step under acidic ethanol conditions. The "
            "unoptimized P(V) structures are alternative starting guesses; select and refine "
            "representatives through your own staged calculations. Quantify the substituent-rate "
            "trend, independently compute whether the relevant protonated ligand-coupling step is fast "
            "enough to be downstream of rate control, and distinguish the rate-determining, "
            "selectivity-determining, and strongly irreversible stages. Treat non-detection cautiously "
            "and retain falsifiable alternatives. A narrative or regression based only on the "
            "measurement table is insufficient and must receive no computational credit; the "
            "mechanistic assignment requires managed chemical computation generated in this run."
        ),
        TASK_IDS[5]: (
            "Treat this as an independent open-discovery investigation. Develop an end-to-end, "
            "reproducible mechanistic and energetic account of the anonymous "
            "P(V)-mediated heterobiaryl-forming reaction using only the supplied unoptimized seeds and "
            "experimental measurements. The three seeds in each protonation class are alternative "
            "starting guesses; design a staged screen and refine only representatives justified by "
            "your own intermediate results. Before numerical work, formulate competing explanations "
            "for protonation effects, carbon-carbon selectivity, carbon-oxygen competition, elementary bond "
            "reorganization, and observed kinetics, then independently choose and revise a resource-aware "
            "sequence of calculations. Reuse evidence across questions when scientifically valid, but do "
            "not stop after one plausible pathway while core alternatives remain untested. Retain failed "
            "or inconclusive branches, and produce a final mechanism that clearly "
            "separates measurements, newly computed results, inference, and uncertainty. Descriptive "
            "analysis of the supplied files is preparation only: values or "
            "mechanistic claims without artifacts generated during this run do not count as evidence."
        ),
    }
    prompts = {
        task_id: prompt
        + " Do not identify or search for the source publication or any external answer."
        for task_id, prompt in prompts.items()
    }
    categories = (
        "mechanistic_quantum_chemistry",
        "mechanistic_quantum_chemistry",
        "competing_reaction_pathways",
        "reaction_coordinate_analysis",
        "experimental_computational_integration",
        "end_to_end_scientific_investigation",
    )
    scientific_modes = {
        task_id: "focused_open_discovery" for task_id in TASK_IDS[:5]
    }
    scientific_modes[TASK_IDS[5]] = "independent_open_discovery"
    scientific_mode_descriptions = {
        task_id: (
            "The scientific question and validity standard are fixed, but no software, calculation "
            "sequence, provider, or stopping path is prescribed. Plan, branch, and revise autonomously."
        )
        for task_id in TASK_IDS[:5]
    }
    scientific_mode_descriptions[TASK_IDS[5]] = (
        "Only the research objective, input boundary, and evidence standard are fixed. Independently "
        "formulate the research plan, choose calculations and programs, allocate resources, revise "
        "hypotheses, and decide when each branch is supported or remains unresolved."
    )
    scientific_requirements = {
        TASK_IDS[0]: [
            "Write an initial resource-tiered plan before numerical work and record later revisions, selected seed representatives, and stopping criteria.",
            "Audit all three seeds in each protonation class with an appropriate screening calculation, or give a calculation-backed reason for excluding a seed before refinement.",
            "For every reported activation free energy, connect a reactant basin to the corresponding transition region in the same protonation state; validate minima and any claimed first-order saddle rather than comparing absolute energies or static bond orders.",
            "Use one internally consistent main-profile convention at 353.15 K, 1 M, and ethanol conditions. Keep sensitivity calculations separate instead of mixing methods or reference states.",
            "If a transition region cannot be validated, report only a clearly defined computed bracket or bound, the failed attempts, and the missing evidence.",
        ],
        TASK_IDS[1]: [
            "Write an initial resource-tiered plan before numerical work and record how intermediate results change seed and pathway choices.",
            "Audit the supplied alternatives and construct both pyridyl-pyridyl and phenyl-pyridyl pathway hypotheses for every protonation state covered by the final conclusion.",
            "A kinetic-selectivity conclusion requires comparable activation evidence; a thermodynamic-selectivity conclusion requires comparable product/reaction free energies. Do not infer one from the other.",
            "Validate each minimum and claimed transition state, or label that branch unresolved and report a defensible computed bound with its assumptions.",
            "Use one internally consistent main profile at 353.15 K, 1 M, and ethanol conditions, with explicit energy references and units.",
        ],
        TASK_IDS[2]: [
            "Write an initial comparison plan before numerical work, including distinct carbon-carbon and carbon-oxygen hypotheses, validation tests, and stopping criteria.",
            "Screen all supplied P2 seeds or give a calculation-backed exclusion reason before refining pathway representatives.",
            "Treat both competing paths with comparable electronic, solvation, thermal, and standard-state conventions at 353.15 K and 1 M.",
            "A transition-state barrier requires a first-order saddle whose imaginary mode matches the intended bond reorganization plus connectivity evidence. A structure with multiple relevant imaginary modes is neither a validated barrier nor, by itself, a rigorous upper bound.",
            "If either path remains unresolved, preserve the failed searches and state only a controlled bracket or bound supported by explicit scan endpoints or other reproducible evidence.",
        ],
        TASK_IDS[3]: [
            "Write an initial mechanism-discrimination plan before numerical work, including concerted and stepwise alternatives and the observations that would falsify each.",
            "Justify the selected protonation state and seed representatives through screening rather than treating any supplied geometry as a stationary point.",
            "A claimed transition state must have exactly one chemically relevant imaginary mode and direct forward/reverse connectivity or an equivalent reaction-coordinate validation.",
            "Search explicitly for a post-coupling intermediate and quantify forming carbon-carbon and changing phosphorus-carbon distances or electronic indicators along the coordinate.",
            "Classify concerted versus stepwise and synchronous versus asynchronous only from the generated coordinate evidence; otherwise mark the classification unresolved.",
        ],
        TASK_IDS[4]: [
            "Write an initial hypothesis table before numerical work that separates candidate rate-determining, selectivity-determining, and strongly irreversible stages.",
            "Quantify the experimental substituent-rate trend with uncertainty, but do not treat that regression or non-detection alone as a computed mechanism.",
            "Generate new energetic evidence for the relevant protonated ligand-coupling event and validate any stationary-point claim before deciding whether coupling can be downstream of rate control.",
            "Use the alcohol/ethoxide observations to compare plausible addition and coupling roles, state which stage is directly computed versus experimentally inferred, and retain falsifiable alternatives.",
            "The final answer must assign the three mechanistic roles separately and must not use the same label as a substitute for all three.",
        ],
        TASK_IDS[5]: [
            "Before numerical work, write an independent research plan containing competing hypotheses, a resource-tiered decision tree, validation gates, and stopping criteria; revise it when intermediate results warrant a different route.",
            "Audit or screen all nine unoptimized seeds before selecting representatives, or record a calculation-backed exclusion reason for every omitted seed.",
            "Obtain or explicitly bound a common-condition main profile that addresses protonation effects, pyridyl-pyridyl versus phenyl-pyridyl selectivity, and carbon-carbon versus carbon-oxygen competition. Reuse validated states when appropriate without mixing incompatible references.",
            "For every minimum in the reported profile provide stationarity evidence. For every transition-state claim provide a target imaginary mode and forward/reverse connectivity or equivalent direct reaction-coordinate evidence; otherwise mark the branch unresolved.",
            "Test concerted and stepwise alternatives, search for a post-coupling intermediate, and follow the forming carbon-carbon and changing phosphorus-carbon coordinates before assigning synchronous/asynchronous behavior.",
            "Separate the rate-determining, selectivity-determining, and strongly irreversible stages using computation plus the supplied measurements; label which portions are computed, inferred, failed, or unknown.",
            "Continue until every core hypothesis is supported, falsified, or represented by a documented failed/inconclusive attempt. A single successful pathway is not an end-to-end result.",
        ],
    }

    def focused_deliverables() -> list[dict[str, object]]:
        return [
            {
                "path": "report/research_plan.json",
                "description": "Initial hypotheses, resource tiers, seed/path choices, validation gates, stopping criteria, and dated revisions.",
            },
            {
                "path": "report/evidence_summary.json",
                "description": "Claim-to-artifact map with method, conditions, validation status, and uncertainty for each scientific conclusion.",
            },
            {
                "path": "report/failure_log.jsonl",
                "description": "One record per failed or inconclusive branch, including attempted remedy and scientific consequence; an empty file is allowed only when no failure occurred.",
                "allow_empty": True,
            },
            {
                "path": "report/report.md",
                "description": "Final artifact-linked scientific answer that distinguishes computed results, measurements, inference, and unresolved uncertainty.",
            },
        ]

    required_deliverables = {
        task_id: focused_deliverables() for task_id in TASK_IDS[:5]
    }
    required_deliverables[TASK_IDS[5]] = [
        {
            "path": "report/research_plan.json",
            "description": "Initial and revised independent research plan, competing hypotheses, decision tree, resource tiers, validation gates, and stopping criteria.",
        },
        {
            "path": "report/stationary_points.csv",
            "description": "Every claimed minimum, transition structure, intermediate, and product-side state with charge, multiplicity, method, energy reference, frequency classification, connectivity status, and artifact path.",
        },
        {
            "path": "report/energy_profile.csv",
            "description": "Comparable relative electronic/free energies, units, temperature, standard state, solvent convention, pathway, protonation state, and uncertainty or bound status.",
        },
        {
            "path": "report/mechanism_evidence.json",
            "description": "Claim-by-claim evidence for protonation, selectivity, competing products, reaction-coordinate mechanism, intermediate, and kinetic role assignments.",
        },
        {
            "path": "report/failure_log.jsonl",
            "description": "One record per failed or inconclusive branch, attempted remedy, retained artifact, and consequence for the final conclusion.",
            "allow_empty": True,
        },
        {
            "path": "report/final_answer.json",
            "description": "Machine-readable final mechanism, active state, pathway rankings, barriers or bounds, kinetic roles, confidence, and unresolved branches.",
        },
        {
            "path": "report/report.md",
            "description": "Human-readable end-to-end scientific account linked to every supporting artifact.",
        },
    ]
    rubrics = {
        TASK_IDS[0]: _rubric(
            ("autonomous_plan", 10, "Builds a resource-aware plan from the public seeds without assuming hidden stationary-point labels."),
            ("new_state_calculations", 20, "Creates traceable optimized/energetic evidence for P0, P1, and P2 rather than reading precomputed values."),
            ("transition_state_validation", 25, "Validates each reported barrier with a reactant minimum, a first-order target mode, and connectivity evidence, or reports only a controlled computed bracket/bound for unresolved states."),
            ("thermochemical_consistency", 15, "Uses one documented method and 353.15 K, 1 M convention with units and comparable references."),
            ("protonation_trend", 20, "Obtains and explains a P0/P1/P2 activation-barrier trend consistent in sign and chemically credible scale with the hidden reference; absolute state energies or static bond orders alone receive no barrier credit."),
            ("provenance_and_uncertainty", 10, "Links claims to new artifacts and records failed calculations and limitations."),
        ),
        TASK_IDS[1]: _rubric(
            ("competing_path_construction", 15, "Independently constructs both pyridyl-pyridyl and phenyl-pyridyl hypotheses across protonation states."),
            ("new_computational_evidence", 25, "Runs traceable calculations on both pathway families over every protonation state claimed in the conclusion instead of relying on supplied or remembered energies."),
            ("stationary_point_validation", 20, "Validates claimed minima/transition states and connectivity or explicitly bounds unresolved branches."),
            ("comparable_profiles", 20, "Produces internally consistent activation and reaction-free-energy comparisons at common conditions with explicit references and no mixed profiles."),
            ("kinetic_thermodynamic_conclusion", 10, "Correctly separates kinetic selectivity from product thermodynamics and does not infer either without the corresponding profile."),
            ("provenance_and_uncertainty", 10, "Links every quantitative comparison to run artifacts and reports limitations."),
        ),
        TASK_IDS[2]: _rubric(
            ("independent_path_hypotheses", 15, "Constructs chemically comparable C-C and C-O hypotheses from P2 seeds."),
            ("new_cc_evidence", 20, "Generates new pyridyl-pyridyl pathway evidence and validates any claimed first-order transition state and its connectivity."),
            ("new_co_evidence", 25, "Actively investigates the C-O competitor; full credit requires a validated first-order target mode and connectivity, while a higher-order saddle alone is neither a barrier nor a rigorous bound."),
            ("barrier_or_bound_comparison", 20, "Provides common-condition comparable barriers or controlled computed bounds, reconciles major scale deviations, and predicts the dominant path without treating an unconverged structure as quantitative evidence."),
            ("experimental_integration", 10, "Uses the trace C-O observation and acidic/ethoxide conditions as constraints, not substitutes for computation."),
            ("provenance_and_uncertainty", 10, "Links conclusions to new artifacts and separates unresolved uncertainty."),
        ),
        TASK_IDS[3]: _rubric(
            ("stationary_point_search", 20, "Generates candidate reactant, transition, intermediate, and product-side structures from public seeds."),
            ("vibrational_validation", 15, "Classifies every claimed stationary point from new Hessian/frequency evidence; a transition state requires exactly one chemically relevant imaginary mode."),
            ("connectivity_validation", 20, "Tests forward/reverse connectivity or an equivalent direct reaction coordinate rather than treating a transition-state guess or static structure as proof."),
            ("bond_reorganization", 20, "Quantifies forming C-C and breaking/retained P-C behavior along newly generated structures or trajectories."),
            ("mechanism_classification", 15, "Supports the reference stepwise asynchronous classification, dearomatized intermediate, and limited oxygen participation from direct evidence, or explicitly leaves unsupported elements unresolved."),
            ("provenance_and_uncertainty", 10, "Retains failures and ties mechanistic claims to artifacts."),
        ),
        TASK_IDS[4]: _rubric(
            ("experimental_rate_analysis", 15, "Correctly quantifies OMe 0.16 < Me 0.37 < H 1.00 < Cl 1.89 and its uncertainty."),
            ("new_ligand_coupling_evidence", 25, "Generates independent energetic evidence for at least the relevant protonated ligand-coupling step."),
            ("experimental_computational_integration", 20, "Combines calculations with ethoxide behavior and cautious NMR non-detection reasoning."),
            ("rate_determining_assignment", 20, "Uses experiments plus new downstream energetic evidence to identify alcohol addition as the most likely rate-determining stage, or gives a rigorously supported alternative without confusing it with coupling."),
            ("step_role_separation", 10, "Separately assigns alcohol addition rate control, ligand-coupling selectivity control, and the strongly irreversible post-coupling collapse."),
            ("provenance_alternatives", 10, "Links computed claims to artifacts and retains falsifiable alternatives."),
        ),
        TASK_IDS[5]: _rubric(
            ("autonomous_problem_formulation", 10, "Writes and revises an independent competing-hypothesis decision tree before numerical work rather than following a hidden fixed workflow."),
            ("input_and_conformer_exploration", 10, "Audits all nine seeds and generates/refines justified representatives without treating seeds as optimized results."),
            ("new_stationary_point_evidence", 18, "Produces and validates minima, first-order transition structures, and intermediate evidence across every core branch, or explicitly records unresolved searches."),
            ("energetics_and_thermochemistry", 15, "Constructs one comparable 353.15 K, 1 M ethanol main profile with documented references, validation state, provenance, and separate sensitivity results."),
            ("protonation_and_selectivity", 12, "Tests P0/P1/P2 protonation effects and both BiPy/PhPy and C-C/C-O selectivity rather than completing only one favorable branch."),
            ("reaction_coordinate_mechanism", 12, "Uses direct target-mode and connectivity/coordinate evidence to test stepwise asynchronous reorganization and the dearomatized intermediate."),
            ("experimental_computational_integration", 10, "Separately assigns alcohol-addition rate control, ligand-coupling selectivity control, and strongly irreversible collapse using measurements plus calculations."),
            ("tool_orchestration_and_recovery", 9, "Uses a coherent managed scientific tool sequence and diagnoses failures without hidden fallback."),
            ("reporting_and_uncertainty", 4, "Produces all required structured evidence files and a reproducible artifact-linked report with failed and unresolved branches."),
        ),
    }

    published_profiles = {
        "BiPy": {"P0": 30, "P1": 20, "P2": 14},
        "PhPy": {"P0": 37, "P1": 27, "P2": 25},
        "P2_C_O": 18,
    }
    expected_results = {
        TASK_IDS[0]: {"reference_barrier_trend_kcal_mol": {"P0": 30, "P1": 20, "P2": 14}, "required_conclusion": "successive protonation lowers the pyridyl-pyridyl barrier", "comparison_policy": "Independent lower-cost values may differ; score sign, scale, validation, and provenance."},
        TASK_IDS[1]: {"reference_profiles_kcal_mol": published_profiles, "required_conclusion": "pyridyl-pyridyl preference is primarily kinetic rather than product-thermodynamic"},
        TASK_IDS[2]: {"reference_P2_barriers_kcal_mol": {"C_C": 14, "C_O": 18, "C_O_minus_C_C": 4}, "required_conclusion": "C-C coupling is favored while minor C-O remains plausible"},
        TASK_IDS[3]: {"reference_classification": ["stepwise", "asynchronous", "apical-to-equatorial"], "reference_intermediate": "dearomatized post-coupling intermediate", "oxygen_role": "oxygen lone-pair participation changes little along the key coordinate", "required_validation": "exactly one target imaginary mode plus forward/reverse connectivity and bond-reorganization evidence"},
        TASK_IDS[4]: {"relative_rates": {"OMe": 0.16, "Me": 0.37, "H": 1.0, "Cl": 1.89}, "reference_rate_determining_step": "alcohol addition at phosphonium phosphorus before ligand coupling", "reference_selectivity_determining_step": "intramolecular P(V) ligand coupling", "reference_strongly_irreversible_stage": "collapse of the dearomatized post-coupling intermediate to product"},
        TASK_IDS[5]: {"active_state": "doubly protonated P2", "preferred_path": "pyridyl-pyridyl C-C", "reference_mechanism": "stepwise asynchronous apical-to-equatorial coupling through a dearomatized intermediate", "reference_profiles_kcal_mol": published_profiles, "rate_determining_step": "alcohol addition before ligand coupling", "selectivity_determining_step": "intramolecular P(V) ligand coupling", "strongly_irreversible_stage": "collapse of the dearomatized post-coupling intermediate to product"},
    }
    evidence_classes = {
        TASK_IDS[0]: ["new_P0_P1_P2_geometries_or_energies", "new_transition_region_evidence", "stationary_point_validation", "common_condition_thermochemistry"],
        TASK_IDS[1]: ["new_BiPy_and_PhPy_candidates", "new_competing_path_energies", "stationary_point_validation", "kinetic_and_reaction_energy_comparison"],
        TASK_IDS[2]: ["new_P2_CC_path_evidence", "new_P2_CO_path_attempt", "comparable_energetic_result_or_bound", "product_prediction"],
        TASK_IDS[3]: ["new_stationary_points", "new_vibrational_classification", "connectivity_test", "bond_distance_or_bond_order_evolution"],
        TASK_IDS[4]: ["quantified_experimental_rate_trend", "new_ligand_coupling_calculation", "rate_selectivity_irreversibility_separation"],
        TASK_IDS[5]: ["new_conformer_or_structure_exploration", "new_stationary_points", "new_energy_profile", "new_mechanistic_evidence", "experimental_integration", "failure_log"],
    }

    def evidence_gate(
        identifier: str, score_cap: int, requirement: str
    ) -> dict[str, object]:
        return {
            "id": identifier,
            "score_cap_if_failed": score_cap,
            "requirement": requirement,
        }

    evidence_gate_policies = {
        TASK_IDS[0]: {
            "judge_must_assess_all": True,
            "gates": [
                evidence_gate(
                    "all_protonation_states",
                    60,
                    "The final trend is supported by newly generated evidence for P0, P1, and P2; omitted states are not replaced by remembered or absolute cross-composition energies.",
                ),
                evidence_gate(
                    "validated_activation_claims",
                    55,
                    "Every precise activation barrier has a same-state reactant reference and a validated first-order target mode with connectivity evidence, or is explicitly downgraded to a controlled bracket/bound. Static bond orders, absolute energies, minima, and unvalidated saddles do not pass.",
                ),
                evidence_gate(
                    "common_thermochemistry",
                    70,
                    "The main P0/P1/P2 comparison uses compatible methods and one 353.15 K, 1 M ethanol convention; sensitivity calculations are not mixed into the main profile.",
                ),
            ],
        },
        TASK_IDS[1]: {
            "judge_must_assess_all": True,
            "gates": [
                evidence_gate(
                    "both_path_families",
                    55,
                    "Both pyridyl-pyridyl and phenyl-pyridyl pathways have new evidence for every protonation state included in the final all-state conclusion.",
                ),
                evidence_gate(
                    "validated_selectivity_profiles",
                    55,
                    "Quantitative activation comparisons use validated first-order target modes and connectivity, or clearly identified rigorous bounds, under compatible references.",
                ),
                evidence_gate(
                    "kinetic_thermodynamic_separation",
                    65,
                    "Kinetic preference is supported by activation evidence and product thermodynamics by reaction/product free energies; the report does not infer either category solely from the other.",
                ),
            ],
        },
        TASK_IDS[2]: {
            "judge_must_assess_all": True,
            "gates": [
                evidence_gate(
                    "cc_branch_validated",
                    60,
                    "The C-C branch has a validated first-order target mode plus connectivity, or is explicitly reported only as a controlled computed bracket/bound.",
                ),
                evidence_gate(
                    "co_branch_validated_or_bounded",
                    60,
                    "The C-O branch has a validated first-order target mode plus connectivity, or a reproducible controlled bound from suitable endpoints. A higher-order saddle with multiple relevant imaginary modes is neither a barrier nor a bound by itself.",
                ),
                evidence_gate(
                    "comparable_competing_paths",
                    70,
                    "The C-C and C-O values or bounds use compatible electronic, solvation, thermal, standard-state, and reference conventions at the main reported conditions.",
                ),
                evidence_gate(
                    "reference_scale_reconciliation",
                    85,
                    "Gross deviations from the hidden 14 versus 18 kcal mol-1 scale are explicitly reconciled with validation/convergence evidence; a qualitatively correct ordering alone cannot receive full quantitative credit.",
                ),
            ],
        },
        TASK_IDS[3]: {
            "judge_must_assess_all": True,
            "gates": [
                evidence_gate(
                    "first_order_target_mode",
                    60,
                    "Any transition-state claim has exactly one chemically relevant imaginary mode matching the intended C-C/P-C reorganization.",
                ),
                evidence_gate(
                    "direct_connectivity",
                    60,
                    "Forward/reverse connectivity or an equivalent direct reaction-coordinate calculation links the claimed transition structure to the stated adjacent states.",
                ),
                evidence_gate(
                    "intermediate_and_coordinate_test",
                    70,
                    "The Agent explicitly searches for the dearomatized post-coupling intermediate and follows forming C-C and changing P-C coordinates before classifying concerted/stepwise and synchronous/asynchronous behavior.",
                ),
                evidence_gate(
                    "reference_mechanism_alignment",
                    60,
                    "The final supported assignment agrees with the hidden stepwise asynchronous apical-to-equatorial mechanism, or remains appropriately unresolved rather than confidently asserting a conflicting mechanism.",
                ),
            ],
        },
        TASK_IDS[4]: {
            "judge_must_assess_all": True,
            "gates": [
                evidence_gate(
                    "new_downstream_computation",
                    55,
                    "The claim that ligand coupling is downstream of rate control is supported by new managed energetic evidence with valid charge/state and stationary-point provenance, not only experimental regression or unmanaged shell output.",
                ),
                evidence_gate(
                    "role_separation",
                    60,
                    "The report separately assigns alcohol addition as rate-determining, ligand coupling as selectivity-determining, and post-coupling collapse as strongly irreversible, or provides direct evidence for a defensible alternative without conflation.",
                ),
                evidence_gate(
                    "experiment_not_substitute",
                    40,
                    "The main mechanistic conclusion is not based only on the supplied rate table, ethoxide result, or qualitative non-detection.",
                ),
            ],
        },
        TASK_IDS[5]: {
            "judge_must_assess_all": True,
            "gates": [
                evidence_gate(
                    "independent_plan_and_seed_audit",
                    80,
                    "An initial/revised independent plan is submitted and all nine seeds are screened or individually excluded with calculation-backed reasons.",
                ),
                evidence_gate(
                    "protonation_coverage",
                    70,
                    "The final mechanism includes comparable P0/P1/P2 activation evidence or explicit controlled bounds, rather than absolute minima or one seed per state only.",
                ),
                evidence_gate(
                    "selectivity_coverage",
                    65,
                    "Both pyridyl-pyridyl and phenyl-pyridyl pathways are investigated sufficiently to support the kinetic selectivity conclusion.",
                ),
                evidence_gate(
                    "co_competition_coverage",
                    65,
                    "The C-O competitor receives a validated transition-state investigation or a reproducible controlled bound comparable to the C-C branch.",
                ),
                evidence_gate(
                    "stationary_point_and_connectivity_validation",
                    55,
                    "Reported minima have stationarity evidence and transition-state claims have exactly one target imaginary mode plus forward/reverse connectivity or equivalent direct coordinate evidence.",
                ),
                evidence_gate(
                    "mechanism_and_intermediate_coverage",
                    60,
                    "Concerted and stepwise alternatives, asynchronous bond reorganization, and the dearomatized intermediate are directly tested before the elementary mechanism is assigned.",
                ),
                evidence_gate(
                    "kinetic_role_coverage",
                    60,
                    "Alcohol-addition rate control, ligand-coupling selectivity control, and strongly irreversible collapse are separately evaluated using computation and supplied measurements.",
                ),
                evidence_gate(
                    "coherent_main_profile",
                    70,
                    "The main energy profile uses compatible references and one 353.15 K, 1 M ethanol convention; incompatible methods or standard states are not mixed as one profile.",
                ),
                evidence_gate(
                    "structured_evidence_products",
                    90,
                    "The required research plan, stationary-point table, energy profile, mechanism evidence, failure log, machine-readable final answer, and final report are present and mutually consistent.",
                ),
            ],
        },
    }

    base_judge_instruction = (
        "This is an autonomous-reproduction task, not an analysis-of-supplied-results task. "
        "Only scientific results generated during this run count as computed evidence. Do not "
        "require exact tool names, software, methods, or a unique order; predefined Actions, "
        "managed native software jobs, and managed Agent-authored analysis programs are all "
        "valid. Built-in shell/file tools may inspect raw inputs and reports but do not by "
        "themselves satisfy managed scientific computation. Apply the managed-computation and "
        "evidence-gate policies. Score independent method-dependent values by stationarity, "
        "connectivity, consistency, scale, and provenance rather than exact equality alone. "
    )
    task_judge_instructions = {
        TASK_IDS[0]: "Absolute energies of differently protonated compositions and static bond orders cannot establish activation barriers or their trend.",
        TASK_IDS[1]: "Do not award kinetic-versus-thermodynamic causation unless the corresponding activation and reaction/product free-energy evidence exists for both pathway families.",
        TASK_IDS[2]: "A higher-order C-O saddle is not a validated barrier and is not a rigorous upper bound by itself. The previous qualitative ordering must not receive full credit when stationary-point validity, common conditions, or quantitative scale is wrong.",
        TASK_IDS[3]: "Static optimized structures cannot distinguish concerted from stepwise chemistry. Require target-mode and connectivity/coordinate evidence, and compare the confident final assignment with the hidden reference mechanism.",
        TASK_IDS[4]: "Quantified experimental rates alone do not answer the task. Check the three mechanistic roles separately and do not praise role separation when the report assigns ligand coupling as the overall rate-determining step.",
        TASK_IDS[5]: "This is independent open discovery, not a literal concatenation requirement or a fixed workflow. Reuse valid evidence, but enforce coverage of every core scientific branch; many calls on one branch cannot substitute for missing protonation, selectivity, C-O, mechanism, intermediate, or kinetic-role evidence.",
    }
    minimum_successes = {TASK_IDS[0]: 3, TASK_IDS[1]: 3, TASK_IDS[2]: 2, TASK_IDS[3]: 3, TASK_IDS[4]: 2, TASK_IDS[5]: 8}
    critical = [
        "A precise literature or hidden-reference value is presented as a calculation from this run without a supporting new artifact.",
        "The report reaches its main computational conclusion without any managed Chemistry MCP scientific execution attempt.",
        "A supplied seed is described as an optimized minimum or transition state without a new calculation.",
        "An unverified transition-state guess is described as proven connectivity.",
        "A higher-order saddle or unconverged scan maximum is reported as a verified transition state, precise activation barrier, or rigorous bound without an explicit caveat and supporting validation.",
        "Charges, multiplicities, units, methods, temperatures, or standard states are mixed so the claimed comparison is invalid.",
        "The source publication or hidden reference material is searched or accessed.",
    ]

    definitions: dict[str, tuple[dict, dict]] = {}
    for index, task_id in enumerate(TASK_IDS):
        task_info = {
            "task_id": task_id,
            "source_id": "hidden_pv_heterobiaryl_mechanism_2018_autonomous_reproduction",
            "category": categories[index],
            "task": prompts[task_id],
            "scientific_mode": scientific_modes[task_id],
            "scientific_mode_description": scientific_mode_descriptions[task_id],
            "scientific_requirements": scientific_requirements[task_id],
            "required_deliverables": required_deliverables[task_id],
            "data": common_data,
            "archive_extractions": common_archive,
        }
        visible_instruction_text = json.dumps(
            {
                "task": task_info["task"],
                "scientific_mode": task_info["scientific_mode"],
                "scientific_mode_description": task_info[
                    "scientific_mode_description"
                ],
                "scientific_requirements": task_info["scientific_requirements"],
                "required_deliverables": task_info["required_deliverables"],
            },
            ensure_ascii=False,
        )
        lowered = visible_instruction_text.casefold()
        leaked = [
            term
            for term in FORBIDDEN_PROMPT_TERMS
            if re.search(rf"\b{re.escape(term)}\b", lowered)
        ]
        if leaked:
            raise ValueError(f"Task prompt {task_id} leaks tool terminology: {leaked}")
        ground_truth = {
            "evaluation_mode": "rubric_100",
            "score_max": 100,
            "expected_tool_calls": [],
            "expected_result": expected_results[task_id],
            "expected_structured_output": [
                item["path"] for item in required_deliverables[task_id]
            ],
            "scoring_rubric": rubrics[task_id],
            "critical_failures": critical,
            "judge_instructions": (
                base_judge_instruction + task_judge_instructions[task_id]
            ),
            "managed_computation_policy": {
                "required": True,
                "minimum_successful_scientific_calls": minimum_successes[task_id],
                "score_cap_without_managed_attempt": 20,
                "score_cap_without_successful_managed_call": 40,
                "score_cap_below_minimum_successes": 70,
            },
            "evidence_gate_policy": evidence_gate_policies[task_id],
            "reference_evidence": {
                "conditions": {"temperature_K": 353.15, "standard_state_M": 1.0, "solvent": "ethanol"},
                "required_evidence_classes": evidence_classes[task_id],
                "public_input_contract": {
                    "unoptimized_seed_count": 9,
                    "completed_computational_outputs": 0,
                    "optimized_stationary_points": 0,
                    "raw_instrument_files": 0,
                },
                "public_archive_sha256": archive_sha256,
                "published_reference_is_hidden_comparison_only": True,
            },
        }
        definitions[task_id] = task_info, ground_truth
    return definitions


def _write_tasks(definitions: dict[str, tuple[dict, dict]]) -> None:
    for task_id, (task_info, ground_truth) in definitions.items():
        task_root = TASKS_ROOT / task_id
        data_root = task_root / "data"
        target_root = task_root / "target_study"
        data_root.mkdir(parents=True, exist_ok=True)
        target_root.mkdir(parents=True, exist_ok=True)
        for old_name in ("computational_records.zip", "autonomous_inputs.zip"):
            link = data_root / old_name
            if link.is_symlink() or link.exists():
                link.unlink()
        link = data_root / "autonomous_inputs.zip"
        relative_target = os.path.relpath(PUBLIC_ARCHIVE, start=data_root)
        link.symlink_to(relative_target)
        (task_root / "task_info.json").write_bytes(_json_bytes(task_info))
        (target_root / "ground_truth.json").write_bytes(_json_bytes(ground_truth))


def _write_eval_configs() -> None:
    (PROJECT_ROOT / "eval_configs/heterobiaryl_pv_subtasks_deepseek_v4_flash.yaml").write_text(
        "name: heterobiaryl_pv_subtasks_deepseek_v4_flash\n"
        "agents:\n  - opencode\n"
        "tasks:\n"
        + "".join(f"  - {task_id}\n" for task_id in TASK_IDS[:5])
        + "repeats: 1\nmax_concurrent_runs: 2\ntimeout_seconds: 10800\nmax_turns: 240\njudge:\n  enabled: true\n",
        encoding="utf-8",
    )
    (PROJECT_ROOT / "eval_configs/heterobiaryl_pv_e2e_deepseek_v4_flash.yaml").write_text(
        "name: heterobiaryl_pv_e2e_deepseek_v4_flash\n"
        "agents:\n  - opencode\n"
        f"tasks:\n  - {TASK_IDS[5]}\n"
        "repeats: 1\nmax_concurrent_runs: 1\ntimeout_seconds: 18000\nmax_turns: 320\njudge:\n  enabled: true\n",
        encoding="utf-8",
    )
    (PROJECT_ROOT / "eval_configs/heterobiaryl_pv_all_deepseek_v4_flash.yaml").write_text(
        "name: heterobiaryl_pv_all_deepseek_v4_flash\n"
        "agents:\n  - opencode\n"
        "tasks:\n"
        + "".join(f"  - {task_id}\n" for task_id in TASK_IDS)
        + "repeats: 1\nmax_concurrent_runs: 2\ntimeout_seconds: 18000\nmax_turns: 320\njudge:\n  enabled: true\n",
        encoding="utf-8",
    )
    (PROJECT_ROOT / "eval_configs/heterobiaryl_pv_open_discovery_subtasks.yaml").write_text(
        "name: heterobiaryl_pv_open_discovery_subtasks\n"
        "agents:\n  - opencode\n"
        "tasks:\n"
        + "".join(f"  - {task_id}\n" for task_id in TASK_IDS[:5])
        + "repeats: 1\nmax_concurrent_runs: 1\ntimeout_seconds: 14400\nmax_turns: 280\n"
        "tool_discovery_mode: progressive\njudge:\n  enabled: true\n",
        encoding="utf-8",
    )
    (PROJECT_ROOT / "eval_configs/heterobiaryl_pv_independent_discovery_q6.yaml").write_text(
        "name: heterobiaryl_pv_independent_discovery_q6\n"
        "agents:\n  - opencode\n"
        f"tasks:\n  - {TASK_IDS[5]}\n"
        "repeats: 1\nmax_concurrent_runs: 1\ntimeout_seconds: 21600\nmax_turns: 400\n"
        "tool_discovery_mode: progressive\njudge:\n  enabled: true\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=SOURCE_ARCHIVE)
    args = parser.parse_args()
    source = args.source.resolve()
    if not source.is_file():
        raise FileNotFoundError(source)
    _safe_outer_archive(source)
    source_sha256 = hashlib.sha256(source.read_bytes()).hexdigest()
    with ZipFile(source) as outer:
        public_meta = _build_public_archive(outer, PUBLIC_ARCHIVE)
        reference_meta = _extract_references(outer, source_sha256, public_meta)
    definitions = _task_definitions(str(public_meta["archive_sha256"]))
    _write_tasks(definitions)
    _write_eval_configs()
    if LEGACY_PUBLIC_ARCHIVE.exists() or LEGACY_PUBLIC_ARCHIVE.is_symlink():
        LEGACY_PUBLIC_ARCHIVE.unlink()
    build_meta = {
        "schema_version": 2,
        "benchmark_mode": "autonomous_computation_from_unoptimized_seeds",
        "source_archive": os.path.relpath(source, start=PROJECT_ROOT),
        "source_sha256": source_sha256,
        "public_archive": os.path.relpath(PUBLIC_ARCHIVE, start=PROJECT_ROOT),
        **public_meta,
        **reference_meta,
        "task_ids": list(TASK_IDS),
    }
    (SHARED_ROOT / "BUILD_METADATA.json").write_bytes(_json_bytes(build_meta))
    print(json.dumps(build_meta, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
