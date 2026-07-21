#!/usr/bin/env python3
"""Build six leak-resistant P(V) heterobiaryl benchmark tasks from the user archive."""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import os
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
PUBLIC_ARCHIVE = SHARED_ROOT / "public" / "computational_records.zip"
REFERENCE_ROOT = SHARED_ROOT / "reference"

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
        r"TS_Int\d",
        r"postTS",
        r"preTS",
        r"Pyrax",
        r"Phrax",
    )
)


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


def _repair_zip_name(name: str) -> str:
    try:
        return name.encode("cp437").decode("utf-8")
    except (UnicodeEncodeError, UnicodeDecodeError):
        return name


def _nested_members(data: bytes) -> tuple[ZipFile, dict[str, str]]:
    archive = ZipFile(io.BytesIO(data))
    fixed_to_raw: dict[str, str] = {}
    for raw in archive.namelist():
        fixed_to_raw[_repair_zip_name(raw)] = raw
    return archive, fixed_to_raw


def _sanitize_output(text: str, candidate_id: str) -> str:
    job_names = re.findall(r"(?m)^SLURM Job Name:\s*(.+?)\s*$", text)
    for job_name in job_names:
        text = text.replace(job_name, f"anonymous_{candidate_id}")
    replacements = {
        "jvalegre@colostate.edu": "anonymous_user",
        "jvalegre": "anonymous_user",
        "colostate.edu": "example.invalid",
        "colostate": "anonymous_org",
    }
    for original, replacement in replacements.items():
        text = re.sub(re.escape(original), replacement, text, flags=re.IGNORECASE)
    text = re.sub(
        r"(?i)(?:pre|post)?TS_Int\d[A-Za-z0-9_.+-]*",
        f"anonymous_{candidate_id}",
        text,
    )
    text = re.sub(
        r"(?i)Int[123](?:_[A-Za-z0-9.+-]+)+",
        f"anonymous_{candidate_id}",
        text,
    )
    text = re.sub(
        r"(?i)[A-Za-z0-9_.+-]*(?:Pyrax|Phrax)[A-Za-z0-9_.+-]*",
        f"anonymous_{candidate_id}",
        text,
    )
    text = re.sub(
        r"(?m)^(Job Start Time|SLURM Job ID|SLURM Job Nodes):.*$",
        lambda match: f"{match.group(1)}: redacted",
        text,
    )
    for pattern in PUBLIC_LEAK_PATTERNS:
        if pattern.search(text):
            raise ValueError(
                f"Sanitized record {candidate_id} still contains leak pattern {pattern.pattern!r}"
            )
    return text


def _write_deterministic_zip(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(".tmp.zip")
    with ZipFile(temporary, "w", compression=ZIP_DEFLATED, compresslevel=6) as archive:
        for path in sorted(item for item in source.rglob("*") if item.is_file()):
            relative = path.relative_to(source).as_posix()
            info = ZipInfo(relative, date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes(), compress_type=ZIP_DEFLATED, compresslevel=6)
    temporary.replace(destination)


def _verify_public_archive(path: Path) -> dict[str, object]:
    """Verify public-record integrity, anonymity, and manifest completeness."""

    with ZipFile(path) as archive:
        infos = archive.infolist()
        names = [info.filename for info in infos]
        if len(names) != len(set(names)):
            raise ValueError("Public archive contains duplicate member names")
        for info in infos:
            member = PurePosixPath(info.filename)
            mode = (info.external_attr >> 16) & 0o170000
            if (
                not info.filename
                or member.is_absolute()
                or ".." in member.parts
                or "\\" in info.filename
                or "\x00" in info.filename
                or (mode and mode not in {stat.S_IFREG, stat.S_IFDIR})
            ):
                raise ValueError(f"Unsafe public archive member: {info.filename!r}")

        candidate_manifest = json.loads(archive.read("candidate_manifest.json"))
        starting_manifest = json.loads(
            archive.read("starting_structure_manifest.json")
        )
        record_manifest = json.loads(archive.read("record_manifest.json"))
        experimental = json.loads(
            archive.read("experimental_evidence/experimental_observations.json")
        )
        candidates = candidate_manifest["candidates"]
        starting_structures = starting_manifest["structures"]
        records = record_manifest["records"]
        if candidate_manifest["candidate_count"] != len(candidates) or len(candidates) != 66:
            raise ValueError("Public candidate manifest is incomplete")
        if (
            starting_manifest["starting_structure_count"] != len(starting_structures)
            or len(starting_structures) != 27
        ):
            raise ValueError("Public starting-structure manifest is incomplete")
        if record_manifest["record_count"] != len(records) or len(records) != 66:
            raise ValueError("Public computational-record manifest is incomplete")

        for item in candidates:
            data = archive.read(item["xyz_file"])
            if _sha256_bytes(data) != item["xyz_sha256"]:
                raise ValueError(f"Structure hash mismatch for {item['candidate_id']}")
            if int(data.splitlines()[0]) != int(item["atom_count"]):
                raise ValueError(f"Structure atom-count mismatch for {item['candidate_id']}")
        for item in starting_structures:
            data = archive.read(item["xyz_file"])
            if _sha256_bytes(data) != item["xyz_sha256"]:
                raise ValueError(f"Starting-structure hash mismatch for {item['starting_id']}")
            if int(data.splitlines()[0]) != int(item["atom_count"]):
                raise ValueError(
                    f"Starting-structure atom-count mismatch for {item['starting_id']}"
                )
        record_fields = {
            "frequency": "frequency_record",
            "large_basis_single_point": "large_basis_single_point_record",
            "correlated_single_point": "correlated_single_point_record",
        }
        for item in records:
            for hash_key, path_key in record_fields.items():
                data = archive.read(item[path_key])
                if _sha256_bytes(data) != item["sha256"][hash_key]:
                    raise ValueError(
                        f"Computational-record hash mismatch for {item['candidate_id']} "
                        f"({hash_key})"
                    )

        for info in infos:
            if PurePosixPath(info.filename).suffix.casefold() not in {
                ".csv", ".json", ".log", ".md", ".out", ".xyz",
            }:
                continue
            text = archive.read(info).decode("utf-8", errors="replace")
            for pattern in PUBLIC_LEAK_PATTERNS:
                if pattern.search(text):
                    raise ValueError(
                        f"Public archive member {info.filename!r} contains leak pattern "
                        f"{pattern.pattern!r}"
                    )
        e03 = next(
            item for item in experimental["observations"] if item["id"] == "E03"
        )
        if e03.get("source_location") != "main text citing Fig. S12":
            raise ValueError("Corrected E03 source location was not preserved")
        expected_entries = 3 * len(records) + len(candidates) + len(starting_structures) + 7
        if len(infos) != expected_entries:
            raise ValueError(
                f"Public archive entry count mismatch: {len(infos)} != {expected_entries}"
            )
        return {
            "archive_entry_count": len(infos),
            "archive_uncompressed_bytes": sum(info.file_size for info in infos),
            "record_file_count": len(records) * 3,
            "starting_structure_count": len(starting_structures),
            "anonymity_scan_passed": True,
            "integrity_scan_passed": True,
        }


def _record_pair_names(frequency_entry: str) -> tuple[str, str]:
    directory, filename = frequency_entry.rsplit("/", 1)
    stem = Path(filename).stem
    qz = f"{directory.replace(' freq', ' Def2QZVPP')}/{stem}_QZ.log"
    dlpno = f"{directory.replace(' freq', ' DLPNO')}/{stem}_DLPNO.out"
    return qz, dlpno


def _build_public_archive(outer: ZipFile, destination: Path) -> dict[str, object]:
    agent_prefix = f"{SOURCE_ROOT}/01_agent_tasks_and_data"
    hidden_prefix = f"{SOURCE_ROOT}/02_hidden_reference_answers"
    structure_manifest = json.loads(
        outer.read(f"{agent_prefix}/task_inputs/structure_manifest.json")
    )
    starting_manifest = json.loads(
        outer.read(f"{agent_prefix}/task_inputs/starting_structure_manifest.json")
    )
    private_mapping = json.loads(
        outer.read(f"{hidden_prefix}/gold_answers/structure_private_mapping.json")
    )["mapping"]
    experimental_json = json.loads(
        outer.read(f"{agent_prefix}/experimental_evidence/experimental_observations.json")
    )
    for observation in experimental_json["observations"]:
        if observation["id"] == "E03":
            observation["source_location"] = "main text citing Fig. S12"
    experimental_csv = outer.read(
        f"{agent_prefix}/experimental_evidence/experimental_observations.csv"
    ).decode("utf-8")
    rows = list(csv.DictReader(io.StringIO(experimental_csv)))
    for row in rows:
        if row["evidence_id"] == "E03":
            row["source_location"] = "main text citing Fig. S12"
    csv_buffer = io.StringIO()
    writer = csv.DictWriter(csv_buffer, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)

    archives = {
        "P0": "Int-I_unprotonated.zip",
        "P1": "Int-I_H_plus.zip",
        "P2": "Int-I_2H_2plus.zip",
    }
    nested: dict[str, tuple[ZipFile, dict[str, str]]] = {}
    for system, filename in archives.items():
        nested[system] = _nested_members(
            outer.read(f"{hidden_prefix}/zenodo_outputs/{filename}")
        )

    record_manifest: list[dict[str, object]] = []
    mapping_by_id = {item["candidate_id"]: item for item in private_mapping}
    with tempfile.TemporaryDirectory(prefix="heterobiaryl_public_") as temporary:
        root = Path(temporary)
        (root / "records").mkdir()
        (root / "structures").mkdir()
        (root / "starting_structures").mkdir()
        (root / "experimental_evidence").mkdir()

        for record in structure_manifest["candidates"]:
            source = f"{agent_prefix}/task_inputs/{record['xyz_file']}"
            target = root / "structures" / record["system"] / f"{record['candidate_id']}.xyz"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(outer.read(source))
        for record in starting_manifest["structures"]:
            source = f"{agent_prefix}/task_inputs/{record['xyz_file']}"
            target = root / "starting_structures" / record["system"] / f"{record['starting_id']}.xyz"
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(outer.read(source))

        for public_record in structure_manifest["candidates"]:
            candidate_id = public_record["candidate_id"]
            private = mapping_by_id[candidate_id]
            frequency_name = private["original_entry"]
            qz_name, dlpno_name = _record_pair_names(frequency_name)
            archive, fixed_to_raw = nested[public_record["system"]]
            missing = [
                name
                for name in (frequency_name, qz_name, dlpno_name)
                if name not in fixed_to_raw
            ]
            if missing:
                raise FileNotFoundError(f"Missing records for {candidate_id}: {missing}")
            record_dir = root / "records" / public_record["system"]
            record_dir.mkdir(parents=True, exist_ok=True)
            output_paths = {
                "frequency": record_dir / f"{candidate_id}.log",
                "large_basis_single_point": record_dir / f"{candidate_id}_QZ.log",
                "correlated_single_point": record_dir / f"{candidate_id}_DLPNO.out",
            }
            source_names = {
                "frequency": frequency_name,
                "large_basis_single_point": qz_name,
                "correlated_single_point": dlpno_name,
            }
            hashes: dict[str, str] = {}
            for kind, output_path in output_paths.items():
                raw = archive.read(fixed_to_raw[source_names[kind]])
                sanitized = _sanitize_output(
                    raw.decode("utf-8", errors="replace"), candidate_id
                ).encode("utf-8")
                output_path.write_bytes(sanitized)
                hashes[kind] = _sha256_bytes(sanitized)
            record_manifest.append(
                {
                    "candidate_id": candidate_id,
                    "system": public_record["system"],
                    "charge": public_record["charge"],
                    "multiplicity": public_record["multiplicity"],
                    "atom_count": public_record["atom_count"],
                    "structure_file": f"structures/{public_record['system']}/{candidate_id}.xyz",
                    "frequency_record": f"records/{public_record['system']}/{candidate_id}.log",
                    "large_basis_single_point_record": f"records/{public_record['system']}/{candidate_id}_QZ.log",
                    "correlated_single_point_record": f"records/{public_record['system']}/{candidate_id}_DLPNO.out",
                    "sha256": hashes,
                }
            )

        public_structure_manifest = {
            **structure_manifest,
            "description": (
                "Anonymous candidate geometries grouped only by protonation state. "
                "Mechanistic roles, pathway labels, energies, and frequencies are withheld "
                "from this manifest and must be inferred from the supplied evidence."
            ),
            "candidates": [
                {
                    **record,
                    "xyz_file": f"structures/{record['system']}/{record['candidate_id']}.xyz",
                }
                for record in structure_manifest["candidates"]
            ],
        }
        public_starting_manifest = {
            **starting_manifest,
            "structures": [
                {
                    **record,
                    "xyz_file": f"starting_structures/{record['system']}/{record['starting_id']}.xyz",
                }
                for record in starting_manifest["structures"]
            ],
        }
        (root / "candidate_manifest.json").write_bytes(
            _json_bytes(public_structure_manifest)
        )
        (root / "starting_structure_manifest.json").write_bytes(
            _json_bytes(public_starting_manifest)
        )
        (root / "record_manifest.json").write_bytes(
            _json_bytes(
                {
                    "record_count": len(record_manifest),
                    "record_types_per_candidate": 3,
                    "records": record_manifest,
                }
            )
        )
        (root / "experimental_evidence" / "experimental_observations.json").write_bytes(
            _json_bytes(experimental_json)
        )
        (root / "experimental_evidence" / "experimental_observations.csv").write_text(
            csv_buffer.getvalue(), encoding="utf-8"
        )
        limitations = {
            "experimental_data_scope": (
                "The experimental table contains paper-level observations, not raw NMR FID, "
                "chromatograms, or time-resolved kinetic measurements."
            ),
            "computational_data_scope": (
                "The archive contains optimized geometry/frequency records and two single-point "
                "energy layers for 66 anonymous candidates."
            ),
            "not_archived": [
                "intrinsic reaction-coordinate trajectories",
                "bond-order or lone-pair trajectories",
                "an explicit competitive C-O transition-state record",
            ],
            "interpretation_rule": (
                "Absence of a record is not evidence that a pathway or intermediate does not exist."
            ),
        }
        (root / "data_limitations.json").write_bytes(_json_bytes(limitations))
        (root / "README.md").write_text(
            "# Anonymous P(V) coupling evidence package\n\n"
            "This directory contains 66 candidate structures, paired computational records, "
            "27 reactant-side starting conformers, and paper-level experimental observations. "
            "Candidate roles and pathway identities are intentionally withheld. The records are "
            "evidence to be audited rather than labels to be trusted. See `data_limitations.json` "
            "before drawing conclusions from missing files.\n",
            encoding="utf-8",
        )
        _write_deterministic_zip(root, destination)

    for archive, _mapping in nested.values():
        archive.close()
    systems = Counter(item["system"] for item in record_manifest)
    verification = _verify_public_archive(destination)
    return {
        "archive_sha256": hashlib.sha256(destination.read_bytes()).hexdigest(),
        "archive_size_bytes": destination.stat().st_size,
        "uncompressed_candidate_count": len(record_manifest),
        "systems": dict(systems),
        **verification,
    }


def _extract_references(outer: ZipFile, source_sha256: str, public_meta: dict[str, object]) -> None:
    REFERENCE_ROOT.mkdir(parents=True, exist_ok=True)
    selected_prefixes = (
        f"{SOURCE_ROOT}/02_hidden_reference_answers/gold_answers/",
    )
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
        relative = Path(name).relative_to(
            f"{SOURCE_ROOT}/02_hidden_reference_answers"
        )
        target = REFERENCE_ROOT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(_normalized_reference_bytes(name, outer.read(name)))

    recomputed = {
        "conditions": {
            "temperature_K": 353.15,
            "standard_state_M": 1.0,
            "solvent": "ethanol",
        },
        "thermochemistry_protocol": {
            "entropy_model": "Grimme mRRHO",
            "entropy_frequency_cutoff_cm-1": 100.0,
            "free_rotor_inertia_model": "global",
            "enthalpy_model": "RRHO",
            "frequency_scale_factor": 1.0,
            "zpe_scale_factor": 1.0,
            "imaginary_frequency_policy": "invert modes between -5 and 0 cm-1 only",
            "symmetry_correction": False,
            "single_point_correction": "author archived correlated single-point energies",
            "software_version": "GoodVibes 4.3.0",
        },
        "common_reactant_ensemble_reference": True,
        "profiles_kcal_mol": {
            "P0": {
                "BiPy_dG_dagger": 30.91,
                "PhPy_dG_dagger": 37.32,
                "delta_delta_G_dagger": 6.41,
                "BiPy_dG_reaction": -32.38,
                "PhPy_dG_reaction": -32.54,
            },
            "P1": {
                "BiPy_dG_dagger": 19.81,
                "PhPy_dG_dagger": 26.86,
                "delta_delta_G_dagger": 7.05,
                "BiPy_dG_reaction": -30.53,
                "PhPy_dG_reaction": -28.51,
            },
            "P2": {
                "BiPy_dG_dagger": 14.30,
                "PhPy_dG_dagger": 25.57,
                "delta_delta_G_dagger": 11.27,
                "BiPy_dG_reaction": -31.35,
                "PhPy_dG_reaction": -31.85,
            },
        },
        "interpretation": (
            "Barrier trends reproduce the published ordering and rounded barriers. Reaction "
            "free energies differ materially from the published integers and must be scored as "
            "a separate, provenance-bearing recomputation rather than an exact replacement."
        ),
    }
    (REFERENCE_ROOT / "recomputed_reference_353K_1M.json").write_bytes(
        _json_bytes(recomputed)
    )
    audit = f"""# Heterobiaryl P(V) benchmark curation audit

- Source archive SHA-256: `{source_sha256}`
- Public anonymous archive SHA-256: `{public_meta['archive_sha256']}`
- Public archive size: {public_meta['archive_size_bytes']} bytes
- Public archive entries: {public_meta['archive_entry_count']} ({public_meta['archive_uncompressed_bytes']} uncompressed bytes)
- Computational record files: {public_meta['record_file_count']}
- Starting structures: {public_meta['starting_structure_count']}
- Candidate systems: {public_meta['systems']}
- Integrity and anonymity scans: passed

## Corrections and fairness decisions

1. The protonation NMR observation points to Fig. S12 in the paper text; the supplied task package incorrectly cited Figs. S17-S18. The public evidence table is corrected.
2. All explicit Action/backend/software recommendations were removed from tested task prompts.
3. The author archive contains 66 frequency records, 66 large-basis single-point records, and 66 correlated single-point records, but no archived IRC trajectory, population trajectory, or explicit C-O transition-state record.
4. The correlated single-point records took roughly 5-8 wall-clock hours each in the author archive. Requiring all 66 to be recomputed inside a normal Agent evaluation would test budget rather than scientific orchestration. The anonymous records are therefore supplied as auditable input, while independent recalculation remains available to the Agent.
5. Published rounded free energies and the 353.15 K, 1 M GoodVibes 4.3 recomputation are stored separately.
6. The five subtasks and end-to-end task use rubric scoring. No exact tool name or unique invocation order is part of the public question or hidden scoring requirement.
"""
    (REFERENCE_ROOT / "CURATION_AUDIT.md").write_text(audit, encoding="utf-8")


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
            "source": "computational_records.zip",
            "destination": "benchmark_data",
            "format": "zip",
            "sha256": archive_sha256,
        }
    ]
    common_data = [
        {
            "name": "Anonymous P(V) evidence package",
            "path": "data/benchmark_data",
            "type": "directory",
            "description": (
                "Anonymous candidate structures, paired computational records, starting "
                "conformers, experimental observations, manifests, and explicit data limitations."
            ),
        }
    ]
    published = {
        "P0": {"BiPy": 30, "PhPy": 37, "BiPy_reaction": -39, "PhPy_reaction": -38},
        "P1": {"BiPy": 20, "PhPy": 27, "BiPy_reaction": -37, "PhPy_reaction": -37},
        "P2": {"BiPy": 14, "PhPy": 25, "BiPy_reaction": -38, "PhPy_reaction": -41},
    }
    recomputed = {
        "P0": {"BiPy": 30.91, "PhPy": 37.32, "delta_delta": 6.41, "BiPy_reaction": -32.38, "PhPy_reaction": -32.54},
        "P1": {"BiPy": 19.81, "PhPy": 26.86, "delta_delta": 7.05, "BiPy_reaction": -30.53, "PhPy_reaction": -28.51},
        "P2": {"BiPy": 14.30, "PhPy": 25.57, "delta_delta": 11.27, "BiPy_reaction": -31.35, "PhPy_reaction": -31.85},
    }

    prompts = {
        TASK_IDS[0]: """Using only the supplied anonymous evidence, determine how successive N-protonation changes the activation free energy of pyridyl-pyridyl ligand coupling in neutral, singly protonated, and doubly protonated P(V) systems. Establish which records support the reactant and transition-state ensembles, keep all three states on a common thermochemical convention at 353.15 K and 1 M, quantify the barrier trend, and explain the structural or electronic origin. Distinguish values taken from supplied records from any independent recalculation, and state uncertainties or missing connectivity evidence. Do not identify or search for the source publication.""",
        TASK_IDS[1]: """Using only the supplied anonymous evidence, determine whether pyridyl-pyridyl coupling is preferred over phenyl-pyridyl coupling for kinetic or thermodynamic reasons in each protonation state. Assign defensible reactant, transition-state, and product ensembles; compare activation and reaction free energies under a common 353.15 K, 1 M convention; report path rankings and confidence; and explain any difference between published-style rounded values and your own reprocessing. Do not identify or search for the source publication.""",
        TASK_IDS[2]: """For the doubly protonated P(V) system, assess whether pyridyl-pyridyl C-C coupling or competitive C-O coupling should dominate under the reported acidic ethanol conditions. Use the supplied evidence without treating an absent archived record as proof that a pathway is absent. Quantify every barrier that is actually supported, investigate the missing competitor as far as the available data and resources permit, predict the dominant and minor products, and clearly separate calculated evidence, experimental constraints, and unresolved uncertainty. Do not identify or search for the source publication.""",
        TASK_IDS[3]: """Determine whether the key P(V) ligand-coupling event is concerted, stepwise, synchronous, or asynchronous. Reconstruct the most defensible stationary-point sequence from the anonymous records, analyze the forming C-C bond and relevant P-C bonds along the reaction coordinate, determine whether a dearomatized intermediate is required, and assess whether oxygen lone-pair participation is supported. Every mechanistic claim must be tied to direct structural, vibrational, connectivity, or electronic evidence, with missing trajectory evidence stated explicitly. Do not identify or search for the source publication.""",
        TASK_IDS[4]: """Integrate the supplied experimental observations with the anonymous computational evidence to determine the rate-determining step under the reported acidic ethanol conditions. Quantify the substituent-rate trend, reconcile it with the accessible ligand-coupling barriers and the ethoxide experiment, and distinguish the rate-determining, selectivity-determining, and strongly irreversible stages. Explain the non-observation of a P(V) intermediate without treating non-detection as proof of absence, and retain plausible alternatives. Do not identify or search for the source publication.""",
        TASK_IDS[5]: """Develop a reproducible mechanistic and energetic account of the P(V)-mediated heterobiaryl-forming reaction represented by the anonymous structures, computational records, and experimental observations. Starting from the evidence rather than a predetermined workflow, formulate and test competing explanations for protonation effects, product selectivity, elementary bond reorganization, and observed kinetics. Produce a coherent final mechanism that distinguishes established facts, computed results, inference, failed or inconclusive analyses, and remaining uncertainty. Do not identify or search for the source publication.""",
    }

    definitions: dict[str, tuple[dict, dict]] = {}
    source_id = "hidden_pv_heterobiaryl_mechanism_2018"
    categories = (
        "mechanistic_quantum_chemistry",
        "mechanistic_quantum_chemistry",
        "competing_reaction_pathways",
        "reaction_coordinate_analysis",
        "experimental_computational_integration",
        "end_to_end_scientific_investigation",
    )
    rubrics = {
        TASK_IDS[0]: _rubric(
            ("input_and_ensemble_assignment", 20, "Correctly separates P0/P1/P2 and identifies defensible common reactant and pyridyl-pyridyl transition-state ensembles without relying on hidden labels."),
            ("stationary_point_evidence", 15, "Uses vibrational and, where available, connectivity evidence; unsupported transition-state claims are qualified."),
            ("thermochemical_consistency", 20, "Uses a common energy layer, 353.15 K, 1 M convention, units, conformer treatment, and complete provenance."),
            ("quantitative_barrier_trend", 25, "Recovers the approximately 31/20/14 kcal mol-1 recomputed trend or the published 30/20/14 trend with a justified distinction between them."),
            ("mechanistic_explanation", 15, "Explains protonation through acceptor electrophilicity and weakening/polarization of the migrating apical P-C bond."),
            ("uncertainty", 5, "States numerical, conformational, version, solvation, and missing-connectivity limitations."),
        ),
        TASK_IDS[1]: _rubric(
            ("path_and_ensemble_assignment", 20, "Distinguishes pyridyl-pyridyl and phenyl-pyridyl reactant, transition-state, and product evidence across P0/P1/P2."),
            ("stationary_point_and_provenance", 15, "Uses defensible stationary-point evidence and records methods, units, standard state, and conformer treatment."),
            ("activation_selectivity", 25, "Finds positive PhPy-BiPy barrier gaps near 6.4, 7.1, and 11.3 kcal mol-1, consistent with published 7/7/11 ordering."),
            ("reaction_thermodynamics", 15, "Recognizes both products are strongly exergonic and that recomputed reaction free energies need not equal published rounded values."),
            ("kinetic_vs_thermodynamic_conclusion", 20, "Correctly attributes selectivity primarily to transition-state kinetics rather than product thermodynamics."),
            ("uncertainty", 5, "Explains method/version and pathway-assignment uncertainty."),
        ),
        TASK_IDS[2]: _rubric(
            ("problem_definition", 15, "Defines comparable doubly protonated C-C and C-O pathways, charges, states, and reference convention."),
            ("supported_cc_barrier", 20, "Validates the supplied C-C evidence and obtains a barrier near 14-14.3 kcal mol-1."),
            ("co_path_investigation", 25, "Recognizes the archive lacks an explicit C-O transition-state record and either performs a defensible independent investigation or gives a rigorous bounded conclusion without fabrication."),
            ("barrier_comparison", 20, "If independently supported, recovers the paper checkpoint near 18 kcal mol-1 and a roughly 4 kcal mol-1 C-O penalty; otherwise reports why an exact number is not established."),
            ("product_prediction_and_uncertainty", 20, "Predicts dominant C-C coupling with at most minor C-O product, integrates the trace experimental product, and states uncertainty."),
        ),
        TASK_IDS[3]: _rubric(
            ("stationary_point_sequence", 20, "Reconstructs reactant-side P(V), bond-forming transition state, dearomatized intermediate, subsequent transition region, and product-side state."),
            ("connectivity_validation", 20, "Uses or attempts direct reaction-path connectivity evidence and does not present an unverified guess as proof."),
            ("bond_reorganization", 25, "Shows one apical P-C bond weakens/breaks as the new C-C bond forms while other equatorial P-C bonds change much less."),
            ("intermediate_and_classification", 20, "Identifies a dearomatized intermediate and classifies the event as stepwise, asynchronous, apical-to-equatorial ligand coupling."),
            ("oxygen_lone_pairs", 10, "Supports little direct oxygen lone-pair involvement with electronic evidence or explicitly limits the claim when that trajectory is unavailable."),
            ("uncertainty", 5, "Separates direct evidence from inference and records failed analyses."),
        ),
        TASK_IDS[4]: _rubric(
            ("experimental_rate_trend", 20, "Correctly extracts OMe 0.16 < Me 0.37 < H 1.00 < Cl 1.89 and relates it to increasing phosphorus electrophilicity."),
            ("computed_barrier_integration", 20, "Uses the low doubly protonated ligand-coupling barrier without confusing a computed elementary barrier with the observed overall rate."),
            ("ethoxide_and_nmr_evidence", 20, "Uses rapid room-temperature ethoxide coupling and cautious P(V) NMR non-detection reasoning."),
            ("rate_determining_step", 20, "Assigns alcohol attack/addition at phosphonium phosphorus before ligand coupling as the most likely rate-determining step."),
            ("step_role_separation", 15, "Separates rate determination, ligand-coupling selectivity determination, and strongly exergonic/near-irreversible collapse."),
            ("alternatives", 5, "Retains detection-limit, steady-state, and other falsifiable alternatives."),
        ),
        TASK_IDS[5]: _rubric(
            ("autonomous_problem_formulation", 14, "Builds competing hypotheses from the evidence without merely restating the five subtasks or a canned workflow."),
            ("input_audit_and_stationary_points", 14, "Audits structures/records and establishes defensible stationary-point classifications with failures retained."),
            ("energetics_and_thermochemistry", 16, "Constructs common-condition profiles with separate published and recomputed values and full provenance."),
            ("protonation_and_selectivity", 16, "Explains the 31/20/14 barrier trend and kinetic preference over PhPy and C-O alternatives."),
            ("reaction_coordinate_mechanism", 14, "Supports stepwise asynchronous apical-to-equatorial coupling and a dearomatized intermediate."),
            ("experimental_computational_integration", 14, "Explains substituent rates, ethoxide behavior, and NMR non-detection while separating rate and selectivity control."),
            ("tool_orchestration_and_failure_handling", 8, "Uses a coherent, traceable sequence of scientific operations, diagnoses failures, and avoids fabricated substitutions."),
            ("reporting_and_uncertainty", 4, "Produces a reproducible report separating facts, calculations, inference, and limitations."),
        ),
    }

    expected_results = {
        TASK_IDS[0]: {
            "published_barriers_kcal_mol": {"P0": 30, "P1": 20, "P2": 14},
            "recomputed_353K_1M_barriers_kcal_mol": {"P0": 30.91, "P1": 19.81, "P2": 14.30},
            "conclusion": "Successive N-protonation lowers the pyridyl-pyridyl ligand-coupling barrier by about 11 and then 5.5-6 kcal mol-1.",
        },
        TASK_IDS[1]: {
            "published_profiles_kcal_mol": published,
            "recomputed_353K_1M_profiles_kcal_mol": recomputed,
            "conclusion": "Pyridyl-pyridyl selectivity is kinetic; product thermodynamics do not explain the observed selectivity.",
        },
        TASK_IDS[2]: {
            "published_P2_barriers_kcal_mol": {"C-C": 14, "C-O": 18, "C-O_minus_C-C": 4},
            "recomputed_supported_C-C_barrier_kcal_mol": 14.30,
            "archive_limitation": "No explicit C-O transition-state record is present in the supplied author archive.",
            "conclusion": "C-C coupling is favored, while a minor C-O pathway remains chemically plausible and is experimentally observed only at trace level under ethoxide conditions.",
        },
        TASK_IDS[3]: {
            "classification": ["stepwise", "asynchronous", "apical-to-equatorial ligand coupling"],
            "key_event": "One apical P-C(pyridyl) bond breaks while a new C-C bond forms; other equatorial P-C bonds change much less.",
            "intermediate": "dearomatized post-coupling intermediate",
            "published_P_C_distances_angstrom": {"P1_apical": 1.95, "P1_equatorial": 1.87, "P2_apical": 1.99, "P2_equatorial": 1.86},
            "oxygen_lone_pair_conclusion": "Little change along the published key reaction coordinate, but the raw population trajectory is not included in the task data.",
        },
        TASK_IDS[4]: {
            "relative_rates": {"OMe": 0.16, "Me": 0.37, "H": 1.0, "Cl": 1.89},
            "rate_determining_step": "Alcohol attack/addition at phosphonium phosphorus to form the P(V) species.",
            "selectivity_determining_step": "Intramolecular ligand coupling from the P(V) intermediate.",
            "strongly_irreversible_stage": "Collapse of the dearomatized intermediate toward products.",
        },
        TASK_IDS[5]: {
            "active_protonation_state": "doubly protonated P2",
            "preferred_path": "pyridyl-pyridyl C-C coupling",
            "mechanism": "stepwise asynchronous apical-to-equatorial ligand coupling through a dearomatized intermediate",
            "rate_determining_step": "alcohol addition before ligand coupling",
            "selectivity_determining_step": "P(V) ligand-coupling transition state",
            "published_barriers_kcal_mol": {"BiPy": {"P0": 30, "P1": 20, "P2": 14}, "PhPy": {"P0": 37, "P1": 27, "P2": 25}, "P2_C-O": 18},
            "recomputed_profiles_kcal_mol": recomputed,
        },
    }

    critical = [
        "The report presents a precise literature target as an independently computed value without supporting provenance.",
        "Charges, multiplicities, units, temperature, standard state, or energy layers are mixed in a way that invalidates the claimed comparison.",
        "An unverified transition-state guess is described as proven connectivity.",
        "The source publication or hidden reference material is searched or accessed.",
    ]
    for index, task_id in enumerate(TASK_IDS):
        task_info = {
            "task_id": task_id,
            "source_id": source_id,
            "category": categories[index],
            "task": prompts[task_id],
            "data": common_data,
            "archive_extractions": common_archive,
        }
        lowered = task_info["task"].casefold()
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
            "expected_structured_output": None,
            "scoring_rubric": rubrics[task_id],
            "critical_failures": critical,
            "judge_instructions": (
                "Judge scientific dependencies and evidence, not exact tool names or a unique call order. "
                "Treat the declared archive limitations as part of the benchmark boundary. "
                "Flag objective framework/backend failures separately from model scientific errors."
            ),
            "reference_evidence": {
                "conditions": {"temperature_K": 353.15, "standard_state_M": 1.0, "solvent": "ethanol"},
                "thermochemistry_protocol": {
                    "entropy_model": "Grimme mRRHO",
                    "entropy_frequency_cutoff_cm-1": 100.0,
                    "free_rotor_inertia_model": "global",
                    "enthalpy_model": "RRHO",
                    "frequency_scale_factor": 1.0,
                    "zpe_scale_factor": 1.0,
                    "imaginary_frequency_policy": "invert modes between -5 and 0 cm-1 only",
                    "symmetry_correction": False,
                },
                "published_rounding_is_not_exact_recompute": True,
                "experimental_observation_ids": [f"E{number:02d}" for number in range(1, 13)],
                "public_archive_sha256": archive_sha256,
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
        link = data_root / "computational_records.zip"
        if link.is_symlink() or link.exists():
            link.unlink()
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
        + "repeats: 1\nmax_concurrent_runs: 2\ntimeout_seconds: 7200\nmax_turns: 220\njudge:\n  enabled: true\n",
        encoding="utf-8",
    )
    (PROJECT_ROOT / "eval_configs/heterobiaryl_pv_e2e_deepseek_v4_flash.yaml").write_text(
        "name: heterobiaryl_pv_e2e_deepseek_v4_flash\n"
        "agents:\n  - opencode\n"
        f"tasks:\n  - {TASK_IDS[5]}\n"
        "repeats: 1\nmax_concurrent_runs: 1\ntimeout_seconds: 14400\nmax_turns: 260\njudge:\n  enabled: true\n",
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
        _extract_references(outer, source_sha256, public_meta)
    definitions = _task_definitions(str(public_meta["archive_sha256"]))
    _write_tasks(definitions)
    _write_eval_configs()
    build_meta = {
        "source_archive": os.path.relpath(source, start=PROJECT_ROOT),
        "source_sha256": source_sha256,
        "public_archive": os.path.relpath(PUBLIC_ARCHIVE, start=PROJECT_ROOT),
        **public_meta,
        "task_ids": list(TASK_IDS),
    }
    (SHARED_ROOT / "BUILD_METADATA.json").write_bytes(_json_bytes(build_meta))
    print(json.dumps(build_meta, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
