#!/usr/bin/env python3
"""Single v19 task-tree Gate used by Agents and the orchestrator."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import re
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


_TASK_SECTION_PATTERNS = {
    "objective": re.compile(
        r"^\s{0,3}#{1,6}\s*(?:scientific\s+objective|research\s+objective|scientific\s+question)\b",
        re.I | re.M,
    ),
    "inputs": re.compile(
        r"^\s{0,3}#{1,6}\s*(?:public\s+inputs?(?:\s+and\s+scientific\s+boundaries)?|inputs?(?:\s+and\s+boundaries)?)\b",
        re.I | re.M,
    ),
    "validation": re.compile(
        r"^\s{0,3}#{1,6}\s*(?:required\s+scientific\s+)?(?:validation|investigation)(?:\s*/\s*investigation)?\b",
        re.I | re.M,
    ),
    "deliverables": re.compile(
        r"^\s{0,3}#{1,6}\s*(?:deliverables?|submission|results?|report)\b",
        re.I | re.M,
    ),
}
_COMPLETION_TERMS = re.compile(
    r"\b(?:complete|completion|finished?|done|success(?:ful)?|acceptance|pass(?:ed)?|criterion|criteria)\b",
    re.I,
)
_STOPPING_TERMS = re.compile(
    r"\b(?:stop|stopping|terminate|termination|bounded|finite|until|no\s+further|exhaust(?:ed|ion)?|coverage\s+limit)\b",
    re.I,
)
_EXPLICIT_ATOM_COUNT = re.compile(r"\b(\d+)\s*[- ]\s*atom(?:s)?\b", re.I)
_PUBLIC_ANSWER_FIELD = re.compile(
    r"(?:^|_)(?:reference(?:_value|_interval)?|expected|target(?:_value)?|tolerance|"
    r"winning(?:_candidate)?|ordering)(?:$|_)|(?:^|_)reaction_energy(?:_|$)",
    re.I,
)


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


def _schema_selector_target(
    schema: Any, selector: str
) -> tuple[bool, dict[str, Any] | None, bool]:
    """Resolve a simple JSONPath selector and its required-property chain."""

    if selector == "$":
        return True, schema if isinstance(schema, dict) else None, True
    if not selector.startswith("$."):
        return False, None, False
    current = schema
    required_chain = True
    for raw_token in selector[2:].split("."):
        token = raw_token.split("[", 1)[0]
        if not token:
            return False, None, False
        if not isinstance(current, dict):
            return False, None, False
        if current.get("type") == "array":
            items = current.get("items")
            if not isinstance(items, dict):
                return False, None, False
            current = items
        properties = current.get("properties") if isinstance(current, dict) else None
        if not isinstance(properties, dict) or token not in properties:
            return False, None, False
        required = current.get("required")
        required_chain = required_chain and isinstance(required, list) and token in required
        current = properties[token]
        if "[" in raw_token:
            if not isinstance(current, dict):
                return False, None, False
            if current.get("type") != "array":
                return False, None, False
            items = current.get("items")
            if not isinstance(items, dict):
                return False, None, False
            current = items
    return True, current if isinstance(current, dict) else None, required_chain


def _xyz_findings(path: Path, *, mode: str, relative: str) -> list[str]:
    """Validate the minimal syntax needed to use an XYZ public input."""

    label = f"{mode}:xyz_invalid:{relative}"
    try:
        lines = path.read_text(encoding="utf-8", errors="strict").splitlines()
    except (OSError, UnicodeError):
        return [f"{label}:unreadable"]
    if len(lines) < 2:
        return [f"{label}:header"]
    try:
        atom_count = int(lines[0].strip())
    except ValueError:
        return [f"{label}:atom_count"]
    if atom_count <= 0 or len(lines) != atom_count + 2:
        return [f"{label}:coordinate_line_count"]
    findings: list[str] = []
    for index, line in enumerate(lines[2:], start=1):
        columns = line.split()
        if len(columns) < 4 or not columns[0]:
            findings.append(f"{label}:coordinate:{index}")
            continue
        try:
            tuple(float(value) for value in columns[1:4])
        except ValueError:
            findings.append(f"{label}:coordinate:{index}")
    return findings


def _task_instruction_findings(path: Path, *, mode: str) -> list[str]:
    """Check the small, mode-agnostic instruction contract without judging science."""

    try:
        text = path.read_text(encoding="utf-8", errors="strict")
    except (OSError, UnicodeError):
        return [f"{mode}:task_instruction_unreadable"]
    findings = [
        f"{mode}:task_section_missing:{name}"
        for name, pattern in _TASK_SECTION_PATTERNS.items()
        if not pattern.search(text)
    ]
    if not _COMPLETION_TERMS.search(text):
        findings.append(f"{mode}:task_completion_criterion_missing")
    if not _STOPPING_TERMS.search(text):
        findings.append(f"{mode}:task_stopping_condition_missing")
    return findings


def _declared_data_findings(
    directory: Path, data_rows: list[Any], *, mode: str
) -> list[str]:
    """Cross-check explicit ``N-atom`` descriptions against XYZ headers.

    This is intentionally limited to an explicit count in the task metadata;
    it does not infer molecular identity or impose a chemistry-specific format.
    """

    findings: list[str] = []
    for row in data_rows:
        if not isinstance(row, dict):
            continue
        match = _EXPLICIT_ATOM_COUNT.search(str(row.get("description") or ""))
        if not match:
            continue
        expected = int(match.group(1))
        path = _safe_path(row.get("path"))
        if path is None:
            continue
        for xyz in (directory / path).rglob("*.xyz") if (directory / path).is_dir() else []:
            try:
                first_line = xyz.read_text(encoding="utf-8", errors="strict").splitlines()[0]
                actual = int(first_line.strip())
            except (OSError, UnicodeError, IndexError, ValueError):
                continue
            if actual != expected:
                findings.append(
                    f"{mode}:data_description_atom_count_mismatch:{xyz.relative_to(directory)}:{expected}!={actual}"
                )
    return findings


def _public_json_answer_findings(directory: Path, *, mode: str) -> list[str]:
    """Reject explicit answer-like scalar fields in Agent-visible JSON inputs.

    This is a narrow anti-leak guard, not a scientific validator: ordinary
    physical conditions (temperature, collision energy, observed channel) are
    allowed, while fields named as references, targets, tolerances, rankings,
    winners, or reaction-energy results are not public inputs.
    """

    data_directory = directory / "data"
    if not data_directory.is_dir():
        return []
    findings: list[str] = []

    def visit(value: Any, path: str) -> None:
        if isinstance(value, dict):
            for key, child in value.items():
                child_path = f"{path}.{key}" if path else str(key)
                if _PUBLIC_ANSWER_FIELD.search(str(key)) and not isinstance(child, (dict, list)):
                    findings.append(f"{mode}:public_answer_field:{child_path}")
                visit(child, child_path)
        elif isinstance(value, list):
            for index, child in enumerate(value):
                visit(child, f"{path}[{index}]")

    for path in data_directory.rglob("*.json"):
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, ValueError, json.JSONDecodeError):
            continue
        visit(value, path.relative_to(directory).as_posix())
    return findings


def _task_quality_findings(review: dict[str, Any]) -> list[str]:
    """Validate the constructor's compact quality receipt for selected modes."""

    quality = review.get("task_quality")
    if not isinstance(quality, dict):
        return ["workflow_review_task_quality_missing"]
    required = (
        "instruction_completeness",
        "input_completeness",
        "process_keypoints",
        "final_conclusions",
        "mode_separation",
    )
    findings: list[str] = []
    for name in required:
        item = quality.get(name)
        if not isinstance(item, dict):
            findings.append(f"workflow_review_task_quality_missing:{name}")
            continue
        if item.get("status") != "passed":
            findings.append(f"workflow_review_task_quality_not_passed:{name}")
        if not _has_value(item.get("finding")):
            findings.append(f"workflow_review_task_quality_finding_missing:{name}")
        evidence = item.get("evidence")
        if not isinstance(evidence, list) or not evidence:
            findings.append(f"workflow_review_task_quality_evidence_missing:{name}")
    return findings


def _numeric_target_usable(target: dict[str, Any] | None) -> bool | None:
    """Classify an explicitly resolved target for a numeric scoring binding."""

    if target is None:
        return None
    declared = target.get("type")
    types = set(declared) if isinstance(declared, list) else {declared}
    types.discard(None)
    if types & {"number", "integer"}:
        return True
    if types:
        return False
    alternatives = target.get("anyOf") or target.get("oneOf")
    if isinstance(alternatives, list):
        classified = [
            _numeric_target_usable(row if isinstance(row, dict) else None)
            for row in alternatives
        ]
        if True in classified:
            return True
        if classified and all(value is False for value in classified):
            return False
    return None


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
    if key_points and not any(
        isinstance(row, dict) and row.get("key_point_type") == "process" for row in key_points
    ):
        findings.append(f"{mode}:process_key_point_missing")

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
            target = row.get("target")
            if isinstance(target, bool) or not isinstance(target, (int, float)):
                findings.append(f"{mode}:numeric_rule_target_not_number:{rule_id or 'missing'}")
            for field_name in ("unit", "tolerance"):
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
            numeric_targets: list[bool | None] = []
            for selector in fields:
                if not isinstance(selector, str):
                    findings.append(f"{mode}:binding_field_not_in_schema:{rule_id or 'missing'}:{selector}")
                    continue
                represented, target, required_chain = _schema_selector_target(
                    result_schema, selector
                )
                if not represented:
                    findings.append(f"{mode}:binding_field_not_in_schema:{rule_id or 'missing'}:{selector}")
                    continue
                if not required_chain:
                    findings.append(
                        f"{mode}:binding_field_not_required:{rule_id or 'missing'}:{selector}"
                    )
                if rule_type == "numeric":
                    numeric_targets.append(_numeric_target_usable(target))
            if (
                rule_type == "numeric"
                and numeric_targets
                and True not in numeric_targets
                and None not in numeric_targets
            ):
                findings.append(
                    f"{mode}:numeric_rule_binding_not_numeric_leaf:{rule_id or 'missing'}"
                )
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
    elif task_path.is_file():
        findings.extend(_task_instruction_findings(task_path, mode=mode))
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
        "required_deliverables", "difficulty", "difficulty_reasons",
    }
    for field in sorted(set(info) - allowed_info):
        findings.append(f"{mode}:task_info_field_unknown:{field}")
    forbidden_ids = {"task_id", "task_family_id", "source_id", "related_task_ids"}
    for field in sorted(forbidden_ids & set(info)):
        findings.append(f"{mode}:obsolete_identity_field:{field}")
    for field in ("title", "category"):
        if not _has_value(info.get(field)):
            findings.append(f"{mode}:task_info_{field}_missing")
    if info.get("difficulty") not in {"easy", "medium", "hard"}:
        findings.append(f"{mode}:task_info_difficulty_invalid")
    difficulty_reasons = info.get("difficulty_reasons")
    if (
        not isinstance(difficulty_reasons, list)
        or not difficulty_reasons
        or any(not isinstance(reason, str) or not reason.strip() for reason in difficulty_reasons)
    ):
        findings.append(f"{mode}:task_info_difficulty_reasons_invalid")
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
        findings.extend(_declared_data_findings(directory, data_rows, mode=mode))
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
        if path.is_file() and path.suffix.casefold() == ".xyz":
            findings.extend(
                _xyz_findings(
                    path,
                    mode=mode,
                    relative=path.relative_to(directory).as_posix(),
                )
            )
    findings.extend(_public_input_findings(root, directory, mode))
    findings.extend(_public_json_answer_findings(directory, mode=mode))
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
        residual_modes = [
            selected_mode
            for selected_mode in MODES
            if (root / selected_mode).exists()
            or (root / "evaluator_reference" / selected_mode).exists()
        ]
        rejection_findings = [] if paper_id else ["paper_id_missing"]
        rejection_findings.extend(
            f"scientific_rejection_contains_mode:{selected_mode}"
            for selected_mode in residual_modes
        )
        return {
            "status": "failed" if rejection_findings else "passed",
            "paper_id": paper_id,
            "findings": rejection_findings,
            "diagnostics": [],
            "snapshot_sha256": snapshot_sha256(root),
        }
    if decision != "candidate_ready":
        findings.append("workflow_review_decision_invalid")
    route_path = root / "paper_route.md"
    if not route_path.is_file():
        findings.append("paper_route_missing")
    elif not route_path.read_text(encoding="utf-8", errors="replace").strip():
        findings.append("paper_route_empty")
    for field in ("scientific_core", "paper_route", "reference_results", "feasibility"):
        if not isinstance(review.get(field), dict) or not review[field]:
            findings.append(f"workflow_review_{field}_missing")

    feasibility = review.get("feasibility")
    feasibility = feasibility if isinstance(feasibility, dict) else {}
    for closure in (
        "objective",
        "public_inputs",
        "evaluation",
        "reproducible_investigation",
    ):
        value = feasibility.get(closure)
        if not isinstance(value, dict) or value.get("status") != "passed":
            findings.append(f"feasibility_{closure}_not_passed")
    public_inputs = feasibility.get("public_inputs")
    if isinstance(public_inputs, dict):
        unresolved = public_inputs.get("unresolved_essential_inputs")
        if not isinstance(unresolved, list):
            findings.append("feasibility_public_inputs_unresolved_invalid")
        elif unresolved:
            findings.append("feasibility_public_inputs_unresolved")

    declared = feasibility.get("release_modes")
    release_modes = (
        [str(value) for value in declared]
        if isinstance(declared, list)
        else []
    )
    if (
        not release_modes
        or len(release_modes) != len(set(release_modes))
        or any(value not in MODES for value in release_modes)
    ):
        findings.append("feasibility_release_modes_invalid")
        release_modes = [value for value in release_modes if value in MODES]
    mode_reviews = feasibility.get("modes")
    mode_reviews = mode_reviews if isinstance(mode_reviews, dict) else {}
    for selected_mode in MODES:
        value = mode_reviews.get(selected_mode)
        if not isinstance(value, dict) or value.get("status") not in {
            "feasible", "infeasible"
        }:
            findings.append(f"feasibility_mode_invalid:{selected_mode}")
        elif (selected_mode in release_modes) != (value.get("status") == "feasible"):
            findings.append(f"feasibility_mode_release_mismatch:{selected_mode}")

    # The constructor's quality receipt is deliberately small and generic. It
    # records that the Agent checked the semantic properties which a mechanical
    # Gate cannot infer from JSON alone; the actual task files are still checked
    # below. Scientific method quality and tolerance choice remain non-blocking.
    findings.extend(_task_quality_findings(review))

    modes = (mode,) if mode else tuple(release_modes)
    if mode and mode not in MODES:
        findings.append(f"unsupported_mode:{mode}")
        modes = ()
    elif mode and mode not in release_modes:
        findings.append(f"mode_not_declared_for_release:{mode}")
        modes = ()
    if mode is None:
        for selected_mode in MODES:
            present = (root / selected_mode).exists() or (
                root / "evaluator_reference" / selected_mode
            ).exists()
            if present and selected_mode not in release_modes:
                findings.append(f"undeclared_mode_present:{selected_mode}")
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
    return {"phase": phase, "mode": mode or "declared_modes", **report}


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
