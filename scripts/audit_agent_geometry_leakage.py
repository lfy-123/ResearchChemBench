#!/usr/bin/env python3
"""Audit agent-visible structure files for likely answer leakage.

Reports review candidates, not scientifically confirmed violations. Does not
rewrite packages. Equal coordinates across modes do not alone imply leakage.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path

MODES = ("autonomous_research", "paper_reproduction")
MARKERS = {
    "source_si": re.compile(r"\bSI\b|supplementary|supporting information"),
    "optimized": re.compile(r"\boptimi[sz]ed\b|\brelaxed\b", re.I),
    "transition_state": re.compile(r"\bts\d*\b|\btransition\s+state\b|\bsaddle\b", re.I),
    "product": re.compile(r"\bproduct\b", re.I),
    "final": re.compile(r"\bfinal\b", re.I),
}
STRUCTURE_SUFFIXES = {".xyz", ".mol", ".mol2", ".sdf", ".pdb", ".cif", ".gjf", ".com", ".poscar", ".vasp"}


def xyz_signature(text: str) -> str:
    """Single-frame ordered coordinates; ignores comments and numeric formatting.

    Does not align rotations, permute atoms, round, or compare perturbed geometry.
    Rejects extra frames so a first-frame match cannot mask different payloads.
    """
    lines = text.splitlines()
    try:
        count = int(lines[0])
        if count <= 0 or len(lines) < count + 2 or any(s.strip() for s in lines[count + 2:]):
            raise ValueError("invalid XYZ atom count or multiple frames")
        rows = []
        for line in lines[2:count + 2]:
            fields = line.split()
            if len(fields) != 4 or not re.fullmatch(r"[A-Z][a-z]?", fields[0]):
                raise ValueError("unsupported XYZ atom row")
            values = [Decimal(v) for v in fields[1:]]
            if any(not v.is_finite() for v in values):
                raise ValueError("non-finite XYZ coordinate")
            coordinates = []
            for value in values:
                number = format(value, "f")
                if "." in number:
                    number = number.rstrip("0").rstrip(".")
                coordinates.append("0" if value == 0 else number)
            rows.append([fields[0], *coordinates])
    except (IndexError, InvalidOperation) as exc:
        raise ValueError("invalid XYZ") from exc
    return hashlib.sha256(json.dumps(rows, separators=(",", ":")).encode()).hexdigest()


def structure_markers(name: str, header: str) -> list[str]:
    # Only inspect the XYZ comment, not atom rows: Si is an element, not SI provenance.
    text = name.replace("_", " ") + "\n" + header.replace("_", " ")
    return sorted(key for key, pattern in MARKERS.items() if pattern.search(text)
                  or (key == "source_si" and re.search(r"\bsi\b", name.replace("_", " "), re.I)))


def audit(root: Path, *, validate_packages: bool = False) -> dict:
    if not root.is_dir() or not any((root / mode).is_dir() for mode in MODES):
        raise ValueError(f"task roots not found: {root}")
    if validate_packages:
        sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
        from evaluation.contracts import validate_task_package
    inventory, errors, validations = [], [], []
    packages = {mode: [] for mode in MODES}
    groups = defaultdict(list)
    for mode in MODES:
        mode_root = root / mode
        if not mode_root.is_dir():
            continue
        for package in sorted(p for p in mode_root.iterdir() if p.is_dir()):
            if not (package / "task_info.json").is_file():
                errors.append({"path": str(package), "error": "task_info_missing"})
                continue
            packages[mode].append(package.name)
            if validate_packages:
                result = validate_task_package(package)
                validations.append({"task_type": mode, "paper_id": package.name,
                                    "status": result.status, "findings": result.findings})
            for path in sorted((package / "agent_input").rglob("*")):
                if not path.is_file() or (path.suffix.lower() not in STRUCTURE_SUFFIXES
                                          and path.name.upper() not in {"POSCAR", "CONTCAR"}):
                    continue
                row = {"task_type": mode, "paper_id": package.name,
                       "path": path.relative_to(package).as_posix()}
                try:
                    content = path.read_bytes()
                    text = content.decode("utf-8", errors="replace")
                    lines = text.splitlines()
                    header = lines[1] if path.suffix.lower() == ".xyz" and len(lines) > 1 else "\n".join(lines[:4])
                    row.update(header=header, sha256=hashlib.sha256(content).hexdigest(),
                               markers=structure_markers(path.name, header))
                    if path.suffix.lower() == ".xyz":
                        row["coordinate_sha256"] = xyz_signature(text)
                        groups[(package.name, row["coordinate_sha256"])].append(row)
                except (OSError, ValueError) as exc:
                    errors.append({**row, "error": str(exc)})
                inventory.append(row)
    rows = [row for row in inventory if row.get("markers")]
    paired = [{"paper_id": paper, "coordinate_sha256": sig,
               "files": [{key: row[key] for key in ("task_type", "path", "sha256")} for row in group]}
              for (paper, sig), group in sorted(groups.items())
              if len({row["task_type"] for row in group}) == 2]
    auto, repro = (set(packages[mode]) for mode in MODES)
    return {
        "policy": "Heuristic review candidates only. Unflagged files are NOT certified answer-neutral.",
        "limitations": ["No full SI comparison; no embedded JSON/archive or prose answer audit.",
                        "Equal-coordinate matches preserve atom order and orientation; no RMSD alignment.",
                        "Source markers can describe experimental inputs; require scientific review."],
        "counts": {"papers": len(auto | repro), "paired_papers": len(auto & repro),
                   "equal_coordinate_papers": len({row["paper_id"] for row in paired}),
                   "by_mode": {mode: {
                       "packages": len(packages[mode]),
                       "structure_packages": len({r["paper_id"] for r in inventory if r["task_type"] == mode}),
                       "structure_files": sum(r["task_type"] == mode for r in inventory),
                       "flagged_packages": len({r["paper_id"] for r in rows if r["task_type"] == mode}),
                       "flagged_files": sum(r["task_type"] == mode for r in rows),
                       "marker_packages": {key: len({r["paper_id"] for r in rows
                           if r["task_type"] == mode and key in r["markers"]}) for key in MARKERS},
                   } for mode in MODES}},
        "unpaired": {MODES[0]: sorted(auto - repro), MODES[1]: sorted(repro - auto)},
        "findings": rows,
        "structure_inventory": inventory,
        "equal_coordinates_across_modes": paired,
        "errors": errors,
        "package_validation": validations,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tasks", type=Path, default=Path("tasks"))
    parser.add_argument("--output", type=Path)
    parser.add_argument("--validate-packages", action="store_true")
    args = parser.parse_args()
    result = audit(args.tasks, validate_packages=args.validate_packages)
    payload = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")


if __name__ == "__main__":
    main()
