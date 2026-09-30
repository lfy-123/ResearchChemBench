#!/usr/bin/env python3
"""Apply the approved, non-numeric quality repairs to final task packages.

Scientific values and evaluator reference files are not regenerated here.  The
script only (1) adds fixed-structure boundary language, (2) replaces two
answer-bearing author geometries with deterministic displaced starters while
keeping the originals evaluator-private, and (3) removes the public TS
coordinate from the Ru-bda-Py barrier task.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import shutil
from pathlib import Path

FIXED_STRUCTURE_IDS = {
    "paper_2f2aa11ea61a32bb",
    "paper_4e9774f4128551d3",
    "paper_641a923cbe5bbc48",
    "paper_72f60526b64ce1b6",
    "paper_94b0a8ae694590ea",
    "paper_988bc12ae3768679",
    "paper_b276b18215cba283",
    "paper_9a58a1fa6ed7d780",
    "paper_9f4c259696ad2f87",
    "paper_db6c4e0558113873",
    "paper_86a0b654270a8ce7",
}

FIXED_NOTICE = (
    "This is a fixed-structure property track: the supplied coordinates are "
    "public inputs for the named property comparison, not a scored structure "
    "discovery answer. Do not claim that the input geometry itself was "
    "rediscovered; report any optimization or conformer search separately."
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace_public_section(text: str, notice: str) -> str:
    marker = "# Public inputs and scientific boundaries"
    start = text.index(marker)
    next_start = text.find("\n# ", start + len(marker))
    if next_start < 0:
        next_start = len(text)
    section = text[start:next_start]
    if notice not in section:
        section = section.rstrip() + "\n\n" + notice + "\n"
    return text[:start] + section.rstrip() + text[next_start:]


def perturb_xyz(path: Path, private_path: Path, amplitude: float) -> dict[str, object]:
    original = path.read_text(encoding="utf-8")
    lines = original.splitlines()
    count = int(lines[0].strip())
    if len(lines) < count + 2:
        raise ValueError(f"invalid XYZ: {path}")
    private_path.parent.mkdir(parents=True, exist_ok=True)
    if private_path.is_file() and len(lines) > 1 and "independently displaced starting geometry" in lines[1]:
        return {
            "path": str(path),
            "private_original": str(private_path),
            "amplitude_angstrom": amplitude,
            "original_sha256": sha256(private_path),
            "public_sha256": sha256(path),
            "atom_count": count,
            "idempotent_skip": True,
        }
    shutil.copy2(path, private_path)
    out = [str(count), "independently displaced starting geometry; source endpoint retained evaluator-private"]
    for index, line in enumerate(lines[2 : count + 2], start=1):
        fields = line.split()
        if len(fields) != 4:
            raise ValueError(f"invalid XYZ atom row: {path}:{index + 2}")
        element = fields[0]
        x, y, z = (float(value) for value in fields[1:])
        # Deterministic, zero-mean-ish displacement.  It changes the supplied
        # endpoint without changing atom order, element identity or formula.
        dx = amplitude * math.sin(index * 1.731)
        dy = amplitude * math.cos(index * 1.193)
        dz = amplitude * math.sin(index * 0.917 + 0.41)
        out.append(f"{element} {x + dx:.8f} {y + dy:.8f} {z + dz:.8f}")
    path.write_text("\n".join(out) + "\n", encoding="utf-8")
    return {
        "path": str(path),
        "private_original": str(private_path),
        "amplitude_angstrom": amplitude,
        "original_sha256": sha256(private_path),
        "public_sha256": sha256(path),
        "atom_count": count,
    }


def update_task_info(path: Path, description: str) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    for item in payload.get("data", []):
        if item.get("path") == "data/inputs":
            item["description"] = description
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_difficulty_reason(path: Path, reason: str) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["difficulty_reasons"] = [reason]
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def rewrite_xyz_comment(path: Path, comment: str) -> bool:
    lines = path.read_text(encoding="utf-8").splitlines()
    if len(lines) < 2 or lines[1] == comment:
        return False
    lines[1] = comment
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return True


def repair_package(root: Path, mode: str, paper_id: str) -> dict[str, object]:
    pkg = root / f"final_verified_{mode}" / paper_id
    task = pkg / "agent_input" / "task.md"
    if not task.is_file():
        raise FileNotFoundError(task)
    text = task.read_text(encoding="utf-8")
    changes: list[dict[str, object]] = []

    if paper_id in FIXED_STRUCTURE_IDS:
        updated = replace_public_section(text, FIXED_NOTICE)
        if updated != text:
            task.write_text(updated, encoding="utf-8")
            changes.append({"kind": "fixed_structure_boundary", "path": str(task)})

    if paper_id == "paper_0dc85595cab7bc0a":
        xyz = pkg / "agent_input/data/inputs/precursor_1_cis.xyz"
        private = pkg / "evaluation/private_inputs/precursor_1_cis_author_endpoint.xyz"
        changes.append({"kind": "displaced_start", **perturb_xyz(xyz, private, 0.18)})
        text = task.read_text(encoding="utf-8")
        text = text.replace(
            "SI Table S5 optimized Cartesian geometry of compound 1-cis",
            "independently displaced 52-atom Cartesian starter for compound 1-cis (the original SI endpoint is evaluator-private)",
        )
        task.write_text(text, encoding="utf-8")

    if paper_id == "paper_221aafe4bd916a11":
        xyz = pkg / "agent_input/data/inputs/2a_inout.xyz"
        private = pkg / "evaluation/private_inputs/2a_inout_author_endpoint.xyz"
        changes.append({"kind": "displaced_start", **perturb_xyz(xyz, private, 0.16)})
        text = task.read_text(encoding="utf-8")
        text = text.replace(
            "79-atom Cartesian geometry of protonated bisphosphine 2a in a defined in–out conformer",
            "independently displaced 79-atom Cartesian starter for protonated bisphosphine 2a in the defined in–out connectivity",
        )
        text = text.replace(
            "79-atom Cartesian geometry of protonated bisphosphine 2a in the in–out conformer",
            "independently displaced 79-atom Cartesian starter for protonated bisphosphine 2a in the in–out connectivity",
        )
        task.write_text(text, encoding="utf-8")

    if paper_id == "paper_e2d9397dff2a3f0f":
        target = pkg / "agent_input/data/inputs/target.xyz"
        private = pkg / "evaluation/private_inputs/target_author_ts.xyz"
        private.parent.mkdir(parents=True, exist_ok=True)
        if target.is_file():
            shutil.copy2(target, private)
            target.unlink()
            changes.append({
                "kind": "remove_public_answer_geometry",
                "public_path": "agent_input/data/inputs/target.xyz",
                "private_path": str(private),
                "sha256": sha256(private),
            })
        text = task.read_text(encoding="utf-8")
        text = text.replace(
            "using the two public stationary-point starting geometries",
            "using the public reference starter and an independently generated transition-state candidate",
        )
        text = text.replace(
            "using the two public stationary-point starting geometries.",
            "using the public reference starter and an independently generated transition-state candidate.",
        )
        text = text.replace(
            "The only molecular inputs are `data/inputs/reference.xyz` and `data/inputs/target.xyz`, explicit 48-atom XYZ files with element identities and Cartesian coordinates.",
            "The public molecular input is `data/inputs/reference.xyz`, an explicit 48-atom XYZ reference starter with element identities and Cartesian coordinates. Generate and validate the transition-state candidate independently; no TS coordinate is public.",
        )
        text = text.replace(
            "Inputs are `data/inputs/reference.xyz` and `data/inputs/target.xyz`, each an explicit 48-atom XYZ geometry with element identities and coordinates.",
            "The public input is `data/inputs/reference.xyz`, an explicit 48-atom XYZ reference geometry with element identities and coordinates. Generate the TS candidate independently; no TS coordinate is public.",
        )
        text = text.replace(
            "and the target transition-state starting structure is `target.xyz` (1(TS3bda)+).",
            "and the transition-state candidate must be generated and validated independently; no TS coordinate is public.",
        )
        text = text.replace(
            "`data/inputs/state_definition.json` is authoritative for charge +1 and singlet multiplicity for both structures.",
            "`data/inputs/state_definition.json` is authoritative for charge +1 and singlet multiplicity for the reference and the independently generated TS candidate.",
        )
        text = text.replace(
            "using the supplied reference geometry and the public target geometry",
            "using the public reference geometry and an independently generated TS candidate",
        )
        text = text.replace("`target.xyz`", "the independently generated TS candidate")
        text = text.replace(
            "Plan a reproducible calculation for the fixed pair, optimize and frequency-test both structures",
            "Plan a reproducible calculation for the public reference and an independently generated TS candidate; optimize and frequency-test both",
        )
        text = text.replace(
            "Stop after the fixed pair and these validation checks; no open candidate search is authorized.",
            "Stop after the reference plus the independently generated TS candidate and these validation checks; no open candidate search is authorized.",
        )
        text = text.replace(
            "Choose and document a defensible computational method, optimize both supplied geometries",
            "Choose and document a defensible computational method, optimize the supplied reference and the independently generated TS candidate",
        )
        text = text.replace(
            "Stop after these two fixed structures and the declared validation checks; do not search other pathways or conformers.",
            "Stop after the reference and independently generated TS candidate and the declared validation checks; do not search other pathways or conformers.",
        )
        text = text.replace("supplied singlet target saddle", "independently generated singlet candidate saddle")
        text = text.replace("with the fixed structures", "with the reference and generated candidate")
        task.write_text(text, encoding="utf-8")
        info = pkg / "task_info.json"
        description = (
            "Public 48-atom XYZ reference starter for charge +1 singlet Ru-bda-Py; "
            "the transition-state coordinate is not agent-visible and must be generated independently."
        )
        update_task_info(info, description)
        update_difficulty_reason(
            info,
            "The reference geometry is public, but the transition-state candidate must be generated and independently validated before the barrier can be reported.",
        )

    if paper_id == "paper_9a58a1fa6ed7d780":
        xyz = pkg / "agent_input/data/inputs/bn_akflu_s0.xyz"
        if xyz.is_file() and rewrite_xyz_comment(
            xyz, "BN-AkFlu 5a provided S0 Cartesian starting geometry; neutral singlet; Angstrom"
        ):
            changes.append({"kind": "fixed_input_provenance_label", "path": str(xyz)})
        task.write_text(
            task.read_text(encoding="utf-8").replace("optimized S0 Cartesian geometry", "provided S0 Cartesian starting geometry"),
            encoding="utf-8",
        )

    if paper_id == "paper_9f4c259696ad2f87":
        old = pkg / "agent_input/data/inputs/compound_1_optimized.xyz"
        new = pkg / "agent_input/data/inputs/compound_1_start.xyz"
        if old.is_file() and not new.exists():
            old.rename(new)
            changes.append({"kind": "fixed_input_provenance_label", "old_path": str(old), "new_path": str(new)})
        if new.is_file() and rewrite_xyz_comment(
            new, "Provided starting geometry of compound 1; neutral singlet; CH2Cl2 PCM"
        ):
            changes.append({"kind": "fixed_input_provenance_label", "path": str(new)})
        text = task.read_text(encoding="utf-8").replace("compound_1_optimized.xyz", "compound_1_start.xyz")
        text = text.replace("Optimized geometry of compound 1", "Provided starting geometry of compound 1")
        task.write_text(text, encoding="utf-8")

    if paper_id == "paper_db6c4e0558113873":
        for name, label in (
            ("syn_anti_Cu_Int_I_6b.xyz", "syn_anti_Cu_Int_I_6b; provided fixed-property input; neutral singlet"),
            ("syn_syn_Cu_Int_I_6b.xyz", "syn_syn_Cu_Int_I_6b; provided fixed-property input; neutral singlet"),
        ):
            xyz = pkg / "agent_input/data/inputs" / name
            if xyz.is_file() and rewrite_xyz_comment(xyz, label):
                changes.append({"kind": "fixed_input_provenance_label", "path": str(xyz)})

    if changes:
        prov = pkg / "evaluation/quality_repair_provenance.json"
        prov.parent.mkdir(parents=True, exist_ok=True)
        # Preserve the audit trail when a package receives a later, independent
        # repair (for example a fixed-structure boundary notice after an
        # input-provenance rename).  Overwriting the file would erase evidence
        # of the earlier change and make the manifest history misleading.
        previous: dict[str, object] = {}
        if prov.is_file():
            try:
                loaded = json.loads(prov.read_text(encoding="utf-8"))
                if isinstance(loaded, dict):
                    previous = loaded
            except (OSError, json.JSONDecodeError):
                previous = {}
        previous_changes = previous.get("changes", [])
        if not isinstance(previous_changes, list):
            previous_changes = []
        merged_changes: list[dict[str, object]] = []
        for item in [*previous_changes, *changes]:
            if not isinstance(item, dict):
                continue
            if item not in merged_changes:
                merged_changes.append(item)
        payload = {"paper_id": paper_id, "task_type": mode, "changes": merged_changes}
        prov.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {"paper_id": paper_id, "task_type": mode, "changes": changes}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path("tasks"))
    args = parser.parse_args()
    reports = []
    for mode in ("autonomous_research", "paper_reproduction"):
        final = args.root / f"final_verified_{mode}"
        for pkg in sorted(final.glob("paper_*")):
            reports.append(repair_package(args.root, mode, pkg.name))
    print(json.dumps(reports, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
