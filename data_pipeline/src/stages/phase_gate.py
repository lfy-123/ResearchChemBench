#!/usr/bin/env python3
"""Single v19 task-tree Gate used by Agents and the orchestrator."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path, PurePosixPath
from typing import Any


MODES = ("autonomous_research", "paper_reproduction")
EVALUATION_FILES = (
    "reference_key_points.json",
    "reference_conclusions.json",
    "scoring_rules.json",
    "evidence_map.json",
    "critical_failures.json",
)
RULE_TYPES = {"numeric", "ordering", "condition", "semantic"}
_PLACEHOLDERS = {"todo", "tbd", "placeholder", "fill me", "fill_me", "fill-me"}


def _read_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError("expected JSON object")
    return value


def _has_value(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip()) and value.strip().casefold() not in _PLACEHOLDERS
    if isinstance(value, (list, dict)):
        return bool(value)
    return True


def _safe_path(value: Any) -> str | None:
    if not isinstance(value, str) or not value or "\\" in value or "\x00" in value:
        return None
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        return None
    return path.as_posix()


def _source_document_hashes(root: Path) -> set[str]:
    """Return hashes of source-paper assets visible from this Agent workspace."""

    for ancestor in (root, *root.parents):
        candidates = (
            ancestor / "inputs" / "documents",
            ancestor / "inputs" / "source" / "documents",
        )
        existing = [path for path in candidates if path.is_dir()]
        if existing:
            return {
                hashlib.sha256(path.read_bytes()).hexdigest()
                for directory in existing
                for path in directory.rglob("*")
                if path.is_file()
            }
    return set()


def _public_input_findings(root: Path, directory: Path, mode: str) -> list[str]:
    """Reject exact copies of source-paper assets in the Agent-visible input tree."""

    source_hashes = _source_document_hashes(root)
    data_directory = directory / "data"
    if not source_hashes or not data_directory.is_dir():
        return []
    return [
        f"{mode}:paper_source_material_exposed:{path.relative_to(directory)}"
        for path in data_directory.rglob("*")
        if path.is_file() and hashlib.sha256(path.read_bytes()).hexdigest() in source_hashes
    ]


def _schema_selector_status(schema: Any, selector: str) -> bool:
    """Return whether a simple JSONPath selector is represented by a schema.

    Dynamic object or array portions are accepted when the schema deliberately
    leaves them open.  This checks declared bindings without prescribing one
    paper-specific result shape.
    """

    if selector == "$":
        return True
    if not selector.startswith("$."):
        return False
    current = schema
    for token in selector[2:].split("."):
        token = token.split("[")[0]
        if not token:
            return False
        if not isinstance(current, dict):
            return True
        properties = current.get("properties")
        if isinstance(properties, dict) and token in properties:
            current = properties[token]
            continue
        additional = current.get("additionalProperties", True)
        return additional is not False
    return True


def _evaluation_findings(
    directory: Path,
    *,
    paper_id: str,
    submission: dict[str, Any],
    mode: str,
) -> tuple[list[str], list[str]]:
    findings: list[str] = []
    diagnostics: list[str] = []
    documents: dict[str, dict[str, Any]] = {}
    for name in EVALUATION_FILES:
        path = directory / name
        if not path.is_file():
            findings.append(f"{mode}:evaluation_file_missing:{name}")
            continue
        try:
            documents[name] = _read_object(path)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            findings.append(f"{mode}:evaluation_json_invalid:{name}:{type(exc).__name__}")
            continue
        if documents[name].get("paper_id") != paper_id:
            findings.append(f"{mode}:evaluation_paper_id_mismatch:{name}")

    key_points = documents.get("reference_key_points.json", {}).get("items")
    conclusions = documents.get("reference_conclusions.json", {}).get("items")
    rules = documents.get("scoring_rules.json", {}).get("rules")
    evidence = documents.get("evidence_map.json", {}).get("evidence")
    failures = documents.get("critical_failures.json", {}).get("items")
    for label, rows in (
        ("key_points", key_points),
        ("conclusions", conclusions),
        ("rules", rules),
        ("evidence", evidence),
        ("critical_failures", failures),
    ):
        if not isinstance(rows, list) or not rows:
            findings.append(f"{mode}:evaluation_{label}_empty")
    key_points = key_points if isinstance(key_points, list) else []
    conclusions = conclusions if isinstance(conclusions, list) else []
    rules = rules if isinstance(rules, list) else []
    evidence = evidence if isinstance(evidence, list) else []

    key_ids: set[str] = set()
    conclusion_ids: set[str] = set()
    used_evidence: set[str] = set()
    for label, id_field, rows in (
        ("key_point", "key_point_id", key_points),
        ("conclusion", "conclusion_id", conclusions),
    ):
        known = key_ids if label == "key_point" else conclusion_ids
        for row in rows:
            if not isinstance(row, dict):
                findings.append(f"{mode}:{label}_not_object")
                continue
            identifier = str(row.get(id_field) or "").strip()
            if not identifier or identifier in known:
                findings.append(f"{mode}:{label}_id_invalid")
            known.add(identifier)
            if not _has_value(row.get("statement")):
                findings.append(f"{mode}:{label}_statement_invalid:{identifier or 'missing'}")
            if not _has_value(row.get("expected")):
                findings.append(f"{mode}:{label}_expected_missing:{identifier or 'missing'}")
            evidence_ids = row.get("evidence_ids")
            if not isinstance(evidence_ids, list) or not evidence_ids:
                findings.append(f"{mode}:{label}_evidence_missing:{identifier or 'missing'}")
            else:
                used_evidence.update(str(item) for item in evidence_ids)
            if label == "conclusion":
                supports = row.get("supporting_key_point_ids")
                if not isinstance(supports, list) or not supports:
                    findings.append(f"{mode}:conclusion_support_missing:{identifier or 'missing'}")
                else:
                    for key_id in supports:
                        if key_id not in key_ids:
                            findings.append(f"{mode}:conclusion_unknown_key_point:{identifier}:{key_id}")
    if conclusions and not any(
        isinstance(row, dict) and row.get("claim_role") == "final" for row in conclusions
    ):
        findings.append(f"{mode}:final_conclusion_missing")

    evidence_ids = {
        str(row.get("evidence_id"))
        for row in evidence
        if isinstance(row, dict) and row.get("evidence_id") and _has_value(row.get("source"))
    }
    for evidence_id in sorted(used_evidence - evidence_ids):
        findings.append(f"{mode}:evidence_reference_missing:{evidence_id}")

    required_files = submission.get("required_files")
    required = {
        path
        for value in (required_files if isinstance(required_files, list) else [])
        if (path := _safe_path(value))
    }
    result_schema = submission.get("result_schema")
    result_schema = result_schema if isinstance(result_schema, dict) else {}
    covered: set[str] = set()
    rule_ids: set[str] = set()
    valid_references = key_ids | conclusion_ids
    for row in rules:
        if not isinstance(row, dict):
            findings.append(f"{mode}:scoring_rule_not_object")
            continue
        rule_id = str(row.get("rule_id") or "").strip()
        reference_id = str(row.get("reference_id") or "").strip()
        rule_type = str(row.get("type") or "").strip()
        if not rule_id or rule_id in rule_ids:
            findings.append(f"{mode}:scoring_rule_id_invalid")
        rule_ids.add(rule_id)
        if reference_id not in valid_references:
            findings.append(f"{mode}:scoring_rule_reference_invalid:{rule_id or 'missing'}")
        else:
            covered.add(reference_id)
        if rule_type not in RULE_TYPES:
            findings.append(f"{mode}:scoring_rule_type_invalid:{rule_id or 'missing'}")
        elif rule_type == "numeric":
            for field_name in ("target", "unit", "tolerance"):
                if not _has_value(row.get(field_name)):
                    findings.append(f"{mode}:numeric_rule_{field_name}_missing:{rule_id or 'missing'}")
            diagnostics.append(f"{mode}:tolerance_requires_scientific_review:{rule_id or 'missing'}")
        elif not _has_value(row.get("expected")):
            findings.append(f"{mode}:scoring_rule_expected_missing:{rule_id or 'missing'}")
        binding = row.get("binding")
        if not isinstance(binding, dict):
            findings.append(f"{mode}:scoring_rule_binding_missing:{rule_id or 'missing'}")
            continue
        paths = binding.get("artifact_paths")
        fields = binding.get("fields")
        comparison = str(binding.get("comparison") or "").strip()
        if not isinstance(paths, list) or not paths or not isinstance(fields, list) or not fields or not comparison:
            findings.append(f"{mode}:scoring_rule_binding_incomplete:{rule_id or 'missing'}")
            continue
        for value in paths:
            path = _safe_path(value)
            if path is None or path not in required:
                findings.append(f"{mode}:binding_artifact_undeclared:{rule_id or 'missing'}:{value}")
        primary = str(submission.get("primary_result_file") or "")
        if primary in paths:
            for selector in fields:
                if not isinstance(selector, str) or not _schema_selector_status(result_schema, selector):
                    findings.append(f"{mode}:binding_field_not_in_schema:{rule_id or 'missing'}:{selector}")
    for reference_id in sorted(valid_references - covered):
        findings.append(f"{mode}:reference_without_scoring_rule:{reference_id}")
    return findings, diagnostics


def _mode_findings(root: Path, mode: str, paper_id: str) -> tuple[list[str], list[str]]:
    directory = root / mode
    findings: list[str] = []
    diagnostics: list[str] = []
    required = ("task.md", "task_info.json", "submission_schema.json", "data")
    for name in required:
        if not (directory / name).exists():
            findings.append(f"{mode}:required_path_missing:{name}")
    task_path = directory / "task.md"
    if task_path.is_file() and not task_path.read_text(encoding="utf-8", errors="replace").strip():
        findings.append(f"{mode}:task_instruction_empty")
    try:
        info = _read_object(directory / "task_info.json")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        findings.append(f"{mode}:task_info_invalid:{type(exc).__name__}")
        info = {}
    if info.get("paper_id") != paper_id:
        findings.append(f"{mode}:task_info_paper_id_mismatch")
    if info.get("task_type") != mode:
        findings.append(f"{mode}:task_info_type_mismatch")
    allowed_info = {
        "paper_id", "task_type", "title", "category", "paper", "data",
        "required_deliverables",
    }
    for field in sorted(set(info) - allowed_info):
        findings.append(f"{mode}:task_info_field_unknown:{field}")
    forbidden_ids = {"task_id", "task_family_id", "source_id", "related_task_ids"}
    for field in sorted(forbidden_ids & set(info)):
        findings.append(f"{mode}:obsolete_identity_field:{field}")
    for field in ("title", "category"):
        if not _has_value(info.get(field)):
            findings.append(f"{mode}:task_info_{field}_missing")
    paper = info.get("paper")
    if paper is not None and (
        not isinstance(paper, dict)
        or set(paper) - {"title", "doi", "journal", "publication_date"}
        or any(not isinstance(value, str) for value in paper.values())
    ):
        findings.append(f"{mode}:task_info_paper_invalid")
    data_rows = info.get("data")
    if not isinstance(data_rows, list):
        findings.append(f"{mode}:task_info_data_invalid")
    else:
        for index, row in enumerate(data_rows):
            if not isinstance(row, dict) or set(row) != {"path", "description"}:
                findings.append(f"{mode}:task_info_data_invalid:{index}")
                continue
            path = _safe_path(row.get("path"))
            if (
                path is None
                or (path != "data" and not path.startswith("data/"))
                or not _has_value(row.get("description"))
                or not (directory / path).exists()
            ):
                findings.append(f"{mode}:task_info_data_invalid:{index}")
    try:
        submission = _read_object(directory / "submission_schema.json")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        findings.append(f"{mode}:submission_schema_invalid:{type(exc).__name__}")
        submission = {}
    required_files = submission.get("required_files")
    if not isinstance(required_files, list) or not required_files:
        findings.append(f"{mode}:submission_required_files_empty")
        submission_required: set[str] = set()
    else:
        submission_required = {path for value in required_files if (path := _safe_path(value))}
        if len(submission_required) != len(required_files):
            findings.append(f"{mode}:submission_required_file_path_invalid")
    deliverables = info.get("required_deliverables")
    declared = {
        path
        for row in (deliverables if isinstance(deliverables, list) else [])
        if isinstance(row, dict) and (path := _safe_path(row.get("path")))
    }
    if not isinstance(deliverables, list) or not deliverables:
        findings.append(f"{mode}:task_info_deliverables_empty")
    else:
        for index, row in enumerate(deliverables):
            if (
                not isinstance(row, dict)
                or set(row) != {"path", "description"}
                or _safe_path(row.get("path")) is None
                or not _has_value(row.get("description"))
            ):
                findings.append(f"{mode}:task_info_deliverable_invalid:{index}")
    if declared != submission_required:
        findings.append(f"{mode}:deliverable_submission_mismatch")
    for path in directory.rglob("*") if directory.is_dir() else []:
        if path.is_symlink():
            findings.append(f"{mode}:symlink_forbidden:{path.relative_to(directory)}")
        if path.is_file() and path.suffix.casefold() == ".pdf":
            findings.append(f"{mode}:paper_pdf_exposed_to_agent:{path.relative_to(directory)}")
    findings.extend(_public_input_findings(root, directory, mode))
    evaluation = root / "evaluator_reference" / mode
    eval_findings, eval_diagnostics = _evaluation_findings(
        evaluation, paper_id=paper_id, submission=submission, mode=mode
    )
    findings.extend(eval_findings)
    diagnostics.extend(eval_diagnostics)
    return findings, diagnostics


def validate(root: str | Path, *, mode: str | None = None) -> dict[str, Any]:
    root = Path(root).resolve()
    findings: list[str] = []
    diagnostics: list[str] = []
    review_path = root / "workflow_review.json"
    try:
        review = _read_object(review_path)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        review = {}
        findings.append(f"workflow_review_invalid:{type(exc).__name__}")
    paper_id = str(review.get("paper_id") or "")
    decision = review.get("decision")
    if decision == "scientific_not_constructible":
        return {
            "status": "passed" if paper_id else "failed",
            "paper_id": paper_id,
            "findings": [] if paper_id else ["paper_id_missing"],
            "diagnostics": [],
            "snapshot_sha256": snapshot_sha256(root),
        }
    if decision != "candidate_ready":
        findings.append("workflow_review_decision_invalid")
    for field in ("scientific_core", "paper_route", "input_closure"):
        if not isinstance(review.get(field), dict) or not review[field]:
            findings.append(f"workflow_review_{field}_missing")
    if isinstance(review.get("input_closure"), dict) and review["input_closure"].get("status") != "closed":
        findings.append("input_closure_not_closed")
    modes = (mode,) if mode else MODES
    if mode and mode not in MODES:
        findings.append(f"unsupported_mode:{mode}")
        modes = ()
    for selected_mode in modes:
        mode_findings, mode_diagnostics = _mode_findings(
            root, selected_mode, paper_id
        )
        findings.extend(mode_findings)
        diagnostics.extend(mode_diagnostics)
    return {
        "status": "failed" if findings else "passed",
        "paper_id": paper_id,
        "findings": sorted(set(findings)),
        "diagnostics": sorted(set(diagnostics)),
        "snapshot_sha256": snapshot_sha256(root),
    }


def run(phase: str, root: str | Path, *, mode: str | None = None) -> dict[str, Any]:
    report = validate(root, mode=mode)
    return {"phase": phase, "mode": mode or "task_pair", **report}


def snapshot_sha256(root: str | Path) -> str:
    root = Path(root)
    rows = []
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.name not in {
            "agent_self_check_report.json", "reproduction_self_check_report.json",
            "external_phase_gate_report.json"
        }:
            rows.append(
                (path.relative_to(root).as_posix(), hashlib.sha256(path.read_bytes()).hexdigest())
            )
    return hashlib.sha256(json.dumps(rows, separators=(",", ":")).encode()).hexdigest()


def is_blocking_finding(value: str) -> bool:
    return not value.startswith("diagnostic:")


def install_phase_gate_tool(destination: str | Path) -> Path:
    destination = Path(destination)
    destination.mkdir(parents=True, exist_ok=True)
    target = destination / "phase_gate.py"
    shutil.copy2(Path(__file__), target)
    target.chmod(0o555)
    return target


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", default="synthesis")
    parser.add_argument("--root", type=Path, default=Path("outputs"))
    parser.add_argument("--mode", choices=MODES)
    args = parser.parse_args(argv)
    report = run(args.phase, args.root, mode=args.mode)
    path = args.root / (
        "reproduction_self_check_report.json"
        if args.mode == "paper_reproduction"
        else "agent_self_check_report.json"
    )
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    return 0 if report["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
