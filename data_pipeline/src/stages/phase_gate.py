#!/usr/bin/env python3
"""Small, read-only Stage06/07 self-check tool.

The tool is intentionally self contained so an Agent can run it from an isolated
workspace without importing the pipeline.  It checks transport and public-surface
contracts only; scientific scope, answers, and paper importance remain Agent
responsibilities.  The orchestrator uses the same phase-specific validators for
the final check.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import stat
import sys
from pathlib import Path
from typing import Any


MODES = ("paper_reproduction", "autonomous_research")
REPRODUCTION_FILES = (
    "task.md",
    "task_info.json",
    "task_spec.json",
    "submission_contract.json",
    "process_rubric.json",
    "paper_route.md",
    "workflow_spec.json",
    "route_evidence_map.json",
)
CORE_FILES = (
    "task.md",
    "task_info.json",
    "task_spec.json",
    "submission_contract.json",
    "process_rubric.json",
)

# These are framework/protocol markers, rather than molecule, paper, or answer
# keywords.  They catch accidental disclosure of the construction protocol in
# autonomous instructions without attempting to infer a scientific answer.
_PROTOCOL_MARKERS = (
    re.compile(r"conversion[_ -]?packet", re.I),
    re.compile(r"(?:phase[_ -]?gate|recovery_context|construction_contract)", re.I),
    re.compile(r"(?:paper_route\.md|workflow_spec\.json|route_evidence_map\.json)", re.I),
    re.compile(r"(?:task_info\.json|task_spec\.json|submission_contract\.json|process_rubric\.json)", re.I),
    re.compile(r"inputs/tools", re.I),
)


def _json(path: Path, findings: list[str]) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        findings.append(f"json_unreadable:{path.name}:{type(exc).__name__}")
        return None


def _required_files(root: Path, names: tuple[str, ...], findings: list[str]) -> dict[str, Any]:
    parsed: dict[str, Any] = {}
    for name in names:
        path = root / name
        if not path.is_file():
            findings.append(f"required_file_missing:{path.relative_to(root.parent).as_posix()}")
            continue
        if path.suffix == ".json":
            value = _json(path, findings)
            if value is not None:
                parsed[name] = value
    task = root / "task.md"
    if task.is_file() and not task.read_text(encoding="utf-8", errors="replace").strip():
        findings.append(f"task_instruction_empty:{root.name}")
    return parsed


def _paths(value: Any) -> set[str]:
    if not isinstance(value, list):
        return set()
    result: set[str] = set()
    for item in value:
        if isinstance(item, str) and item.strip():
            result.add(item.strip().replace("\\", "/"))
        elif isinstance(item, dict):
            raw = item.get("path") or item.get("file")
            if isinstance(raw, str) and raw.strip():
                result.add(raw.strip().replace("\\", "/"))
    return result


def _deliverable_findings(root: Path, parsed: dict[str, Any], findings: list[str]) -> None:
    info = parsed.get("task_info.json")
    submission = parsed.get("submission_contract.json")
    if not isinstance(info, dict) or not isinstance(submission, dict):
        return
    declared = _paths(info.get("required_deliverables"))
    required = _paths(submission.get("required_files"))
    if not required:
        findings.append(f"submission_required_files_missing:{root.name}")
    if declared != required:
        missing = sorted(declared - required)
        extra = sorted(required - declared)
        findings.append(
            "deliverables_submission_mismatch:"
            f"{root.name}:declared_missing={','.join(missing) or '-'}:"
            f"required_missing={','.join(extra) or '-'}"
        )


def _input_findings(root: Path, parsed: dict[str, Any], findings: list[str]) -> None:
    spec = parsed.get("task_spec.json")
    input_root = root / "data" / "inputs"
    if not input_root.is_dir():
        findings.append(f"input_directory_missing:{root.name}")
        return
    if not isinstance(spec, dict):
        return
    assets = spec.get("input_assets") or []
    if not isinstance(assets, list):
        findings.append(f"input_assets_not_array:{root.name}")
        return
    for index, asset in enumerate(assets):
        if not isinstance(asset, dict):
            findings.append(f"input_asset_not_object:{root.name}:{index}")
            continue
        raw = str(asset.get("path") or "").replace("\\", "/")
        if not raw or raw.startswith("/") or ".." in Path(raw).parts:
            findings.append(f"input_asset_path_invalid:{root.name}:{index}")
            continue
        for prefix in ("data/inputs/", "inputs/"):
            if raw.startswith(prefix):
                raw = raw[len(prefix) :]
                break
        if not (input_root / raw).is_file():
            findings.append(f"input_asset_missing:{root.name}:{raw}")


def _mode_contract(root: Path, mode: str, findings: list[str]) -> dict[str, Any]:
    parsed = _required_files(root, REPRODUCTION_FILES if mode == "paper_reproduction" else CORE_FILES, findings)
    _deliverable_findings(root, parsed, findings)
    _input_findings(root, parsed, findings)
    info = parsed.get("task_info.json")
    spec = parsed.get("task_spec.json")
    expected_task_mode = "guided_reproduction" if mode == "paper_reproduction" else "open_discovery"
    mode_aliases = {
        "paper_reproduction": {"paper_reproduction", "reproduction", "guided_reproduction"},
        "autonomous_research": {"autonomous_research", "autonomous", "open_discovery"},
    }
    if isinstance(info, dict):
        if any(
            value not in (None, "") and str(value) not in mode_aliases[mode]
            for value in (info.get("mode"), info.get("scientific_mode"))
        ):
            findings.append(f"mode_contract_mismatch:{root.name}")
        if info.get("task_mode") not in (None, "", expected_task_mode, *mode_aliases[mode]):
            findings.append(f"task_mode_contract_mismatch:{root.name}")
        # Task IDs and enum aliases are canonicalized by the orchestrator before
        # the external Gate.  The self-check only catches a missing identity, not
        # an Agent's harmless legacy spelling.
        if not str(info.get("task_id") or "").strip():
            findings.append(f"task_id_missing:{root.name}")
    if isinstance(spec, dict):
        allowed = mode_aliases[mode]
        if any(
            value not in (None, "") and str(value) not in allowed
            for value in (spec.get("mode"), spec.get("scientific_mode"))
        ):
            findings.append(f"task_spec_mode_mismatch:{root.name}")
    return parsed


def _stage06a(root: Path, findings: list[str]) -> None:
    receipt_path = root / "construction_receipt.json"
    receipt = _json(receipt_path, findings) if receipt_path.is_file() else None
    if not receipt_path.is_file():
        findings.append("construction_receipt_missing")
    if isinstance(receipt, dict) and receipt.get("decision") == "scientific_not_constructible":
        return
    reproduction = root / "paper_reproduction"
    parsed = _mode_contract(reproduction, "paper_reproduction", findings) if reproduction.is_dir() else {}
    review_path = root / "workflow_review.json"
    review = _json(review_path, findings) if review_path.is_file() else None
    if not review_path.is_file():
        findings.append("workflow_review_missing")
    elif isinstance(review, dict) and review.get("decision") != "candidate_ready":
        findings.append("workflow_review_not_candidate_ready")
    for name in ("workflow_completeness_check.json", "public_to_private_asset_map.json", "toolbox_requirements.json"):
        path = root / name
        if not path.is_file():
            findings.append(f"handoff_file_missing:{name}")
        else:
            _json(path, findings)
    hidden = root / "hidden_reference" / "ground_truth_common.json"
    value = _json(hidden, findings) if hidden.is_file() else None
    if not hidden.is_file():
        findings.append("hidden_reference_missing")
    elif not isinstance(value, dict):
        findings.append("hidden_reference_not_object")
    elif value.get("status") != "ready":
        findings.append("hidden_reference_not_ready")
    elif not any(isinstance(item, dict) and item.get("claim_role") == "final" for item in value.get("ground_truth_items") or []):
        findings.append("final_claim_missing")
    if isinstance(value, dict) and not isinstance(value.get("acceptance_profiles"), list):
        findings.append("acceptance_profiles_missing")
    if isinstance(value, dict) and not isinstance(value.get("scientific_conclusion_rubric"), list):
        findings.append("conclusion_key_points_missing")
    del parsed


def _autonomous_leaks(root: Path, findings: list[str]) -> None:
    task = root / "task.md"
    if task.is_file():
        text = task.read_text(encoding="utf-8", errors="replace")
        for marker in _PROTOCOL_MARKERS:
            if marker.search(text):
                findings.append(f"autonomous_protocol_marker:{marker.pattern}")
    for path in root.rglob("*"):
        if path.is_dir() and path.name in {"paper_reproduction", "conversion_packet", "hidden_reference", "source_materials", "stage06_candidate"}:
            findings.append(f"autonomous_forbidden_directory:{path.relative_to(root).as_posix()}")
        if path.is_file() and path.name in {"paper_route.md", "workflow_spec.json", "route_evidence_map.json"}:
            findings.append(f"autonomous_forbidden_route_file:{path.relative_to(root).as_posix()}")
    for path in root.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in {".json", ".md", ".txt"}:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        # Internal IDs/protocol names in metadata are transport leakage; this
        # intentionally does not inspect numeric values or chemistry labels.
        if re.search(r"\bgt_[A-Za-z0-9_.-]+\b|canonical_answer|acceptance_profile_id", text):
            findings.append(f"autonomous_internal_scoring_marker:{path.relative_to(root).as_posix()}")


def _stage06b(root: Path, findings: list[str]) -> None:
    autonomous = root / "autonomous_research"
    if not autonomous.is_dir():
        findings.append("autonomous_directory_missing")
        return
    parsed = _mode_contract(autonomous, "autonomous_research", findings)
    _autonomous_leaks(autonomous, findings)
    del parsed


def _stage07a(root: Path, findings: list[str]) -> None:
    pair = root / "task_pair"
    if not pair.is_dir():
        findings.append("task_pair_missing")
        return
    for mode in MODES:
        mode_root = pair / mode
        if not mode_root.is_dir():
            findings.append(f"mode_directory_missing:{mode}")
            continue
        _mode_contract(mode_root, mode, findings)
    hidden = pair / "hidden_reference" / "ground_truth_common.json"
    value = _json(hidden, findings) if hidden.is_file() else None
    if not hidden.is_file():
        findings.append("hidden_reference_missing")
    elif not isinstance(value, dict):
        findings.append("hidden_reference_not_object")
    elif value.get("status") != "ready":
        findings.append("hidden_reference_not_ready")
    elif not isinstance(value.get("ground_truth_items"), list) or not value.get("ground_truth_items"):
        findings.append("ground_truth_items_missing")


def run(phase: str, root: Path) -> dict[str, Any]:
    findings: list[str] = []
    if not root.is_dir():
        findings.append("root_missing")
    elif phase == "stage06a":
        _stage06a(root, findings)
    elif phase == "stage06b":
        _stage06b(root, findings)
    elif phase == "stage07a":
        _stage07a(root, findings)
    else:
        findings.append(f"unsupported_phase:{phase}")
    findings = sorted(set(findings))
    return {"status": "passed" if not findings else "failed", "phase": phase, "findings": findings}


def install_phase_gate_tool(destination: Path) -> Path:
    """Copy this standalone tool into an Agent's read-only input tree."""

    destination.mkdir(parents=True, exist_ok=True)
    target = destination / "phase_gate.py"
    source = Path(__file__).resolve()
    if source != target:
        shutil.copyfile(source, target)
    target.chmod(stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR | stat.S_IRGRP | stat.S_IXGRP | stat.S_IROTH | stat.S_IXOTH)
    return target


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Read-only Stage06/07 phase self-check")
    parser.add_argument("--phase", required=True, choices=("stage06a", "stage06b", "stage07a"))
    parser.add_argument("--root", default="outputs", type=Path)
    args = parser.parse_args(argv)
    try:
        report = run(args.phase, args.root)
    except Exception as exc:  # tool errors are distinct from contract findings
        report = {"status": "tool_error", "phase": args.phase, "findings": [f"tool_error:{type(exc).__name__}:{exc}"]}
        print(json.dumps(report, ensure_ascii=False, separators=(",", ":")))
        return 2
    print(json.dumps(report, ensure_ascii=False, separators=(",", ":")))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
