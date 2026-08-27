"""Transport contract for current ResearchChemBench task packages.

The contract checks identity, paths, visibility, evaluator completeness and
submission binding.  It deliberately does not judge whether an authored
tolerance or scientific conclusion is optimal.
"""

from __future__ import annotations

import hashlib
import json
import re
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


TASK_TYPES = (
    "autonomous_research",
    "paper_reproduction",
    "experiment_validation",
)
EVALUATION_FILES = (
    "reference_key_points.json",
    "reference_conclusions.json",
    "scoring_rules.json",
    "evidence_map.json",
    "critical_failures.json",
)
RULE_TYPES = {"numeric", "ordering", "condition", "semantic"}
_PAPER_ID = re.compile(r"paper_[A-Za-z0-9]+\Z")
_PLACEHOLDERS = {"todo", "tbd", "placeholder", "fill me", "fill_me", "fill-me"}


def _safe_path(value: str) -> str:
    if not isinstance(value, str) or not value or "\\" in value or "\x00" in value:
        raise ValueError("path must be a non-empty relative POSIX path")
    path = PurePosixPath(value)
    if path.is_absolute() or any(part in {"", ".", ".."} for part in path.parts):
        raise ValueError("path must be a safe relative POSIX path")
    return path.as_posix()


def _json_object(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"expected JSON object: {path}")
    return value


def _has_value(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, str):
        return bool(value.strip()) and value.strip().casefold() not in _PLACEHOLDERS
    if isinstance(value, (list, dict)):
        return bool(value)
    return True


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class DataDescription(StrictModel):
    path: str
    description: str

    @field_validator("path")
    @classmethod
    def data_path(cls, value: str) -> str:
        value = _safe_path(value)
        if value != "data" and not value.startswith("data/"):
            raise ValueError("data paths must be rooted below data/")
        return value


class RequiredDeliverable(StrictModel):
    path: str
    description: str

    @field_validator("path")
    @classmethod
    def deliverable_path(cls, value: str) -> str:
        return _safe_path(value)


class PaperSummary(StrictModel):
    title: str = ""
    doi: str = ""
    journal: str = ""
    publication_date: str = ""


class TaskInfo(StrictModel):
    paper_id: str
    task_type: Literal[
        "autonomous_research", "paper_reproduction", "experiment_validation"
    ]
    title: str
    category: str
    paper: PaperSummary = Field(default_factory=PaperSummary)
    data: list[DataDescription]
    required_deliverables: list[RequiredDeliverable]

    @field_validator("paper_id")
    @classmethod
    def valid_paper_id(cls, value: str) -> str:
        if not _PAPER_ID.fullmatch(value):
            raise ValueError("paper_id must use paper_<alphanumeric>")
        return value

    @field_validator("title", "category")
    @classmethod
    def nonempty(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("value must be non-empty")
        return value.strip()

    @model_validator(mode="after")
    def unique_paths(self) -> "TaskInfo":
        data_paths = [item.path for item in self.data]
        deliverables = [item.path for item in self.required_deliverables]
        if len(data_paths) != len(set(data_paths)):
            raise ValueError("data paths must be unique")
        if not deliverables or len(deliverables) != len(set(deliverables)):
            raise ValueError("required deliverables must be non-empty and unique")
        return self


class ManifestEntry(StrictModel):
    path: str
    size: int = Field(ge=0)
    sha256: str
    visibility: Literal["agent", "metadata", "evaluator"]

    @field_validator("path")
    @classmethod
    def valid_path(cls, value: str) -> str:
        return _safe_path(value)

    @field_validator("sha256")
    @classmethod
    def valid_hash(cls, value: str) -> str:
        if not re.fullmatch(r"[0-9a-f]{64}", value):
            raise ValueError("sha256 must contain 64 lowercase hexadecimal characters")
        return value


class PackageManifest(StrictModel):
    paper_id: str
    task_type: Literal[
        "autonomous_research", "paper_reproduction", "experiment_validation"
    ]
    package_format: Literal[1] = 1
    agent_input_root: Literal["agent_input"] = "agent_input"
    package_content_sha256: str
    entries: list[ManifestEntry]

    @field_validator("paper_id")
    @classmethod
    def valid_paper_id(cls, value: str) -> str:
        if not _PAPER_ID.fullmatch(value):
            raise ValueError("invalid paper_id")
        return value

    @field_validator("package_content_sha256")
    @classmethod
    def valid_hash(cls, value: str) -> str:
        if not re.fullmatch(r"[0-9a-f]{64}", value):
            raise ValueError("invalid package content hash")
        return value

    @model_validator(mode="after")
    def unique_entries(self) -> "PackageManifest":
        paths = [entry.path for entry in self.entries]
        if len(paths) != len(set(paths)):
            raise ValueError("manifest entry paths must be unique")
        return self


@dataclass(frozen=True)
class TaskPackageValidation:
    status: Literal["passed", "failed"]
    paper_id: str = ""
    task_type: str = ""
    findings: list[str] = field(default_factory=list)
    diagnostics: list[str] = field(default_factory=list)


def _visibility(relative: str) -> Literal["agent", "metadata", "evaluator"]:
    if relative.startswith("agent_input/"):
        return "agent"
    if relative.startswith("evaluation/"):
        return "evaluator"
    # The author route is a human/audit reference.  It is deliberately kept
    # at the task-package root, outside agent_input, while remaining part of
    # the immutable package manifest as metadata.
    if relative in {"task_info.json", "paper_route.md"}:
        return "metadata"
    raise ValueError(f"file is outside the task package payload: {relative}")


def package_payload_entries(root: str | Path) -> list[ManifestEntry]:
    root = Path(root).resolve()
    entries: list[ManifestEntry] = []
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"symlink is forbidden: {path.relative_to(root)}")
        if not path.is_file() or path.name == "package_manifest.json":
            continue
        relative = path.relative_to(root).as_posix()
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        entries.append(
            ManifestEntry(
                path=relative,
                size=path.stat().st_size,
                sha256=digest,
                visibility=_visibility(relative),
            )
        )
    return entries


def package_content_hash(entries: list[ManifestEntry]) -> str:
    payload = [entry.model_dump(mode="json") for entry in entries]
    encoded = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(encoded).hexdigest()


def read_evaluation(root: str | Path) -> dict[str, dict[str, Any]]:
    root = Path(root)
    return {name: _json_object(root / name) for name in EVALUATION_FILES}


def _binding_paths(rule: dict[str, Any]) -> tuple[list[str], list[str], str]:
    binding = rule.get("binding")
    if not isinstance(binding, dict):
        return [], [], ""
    paths = binding.get("artifact_paths")
    fields = binding.get("fields")
    return (
        [str(item) for item in paths] if isinstance(paths, list) else [],
        [str(item) for item in fields] if isinstance(fields, list) else [],
        str(binding.get("comparison") or "").strip(),
    )


def validate_evaluation(
    root: str | Path,
    *,
    paper_id: str,
    required_files: set[str],
) -> tuple[list[str], list[str]]:
    root = Path(root)
    findings: list[str] = []
    diagnostics: list[str] = []
    documents: dict[str, dict[str, Any]] = {}
    for name in EVALUATION_FILES:
        path = root / name
        if not path.is_file():
            findings.append(f"evaluation_file_missing:{name}")
            continue
        try:
            documents[name] = _json_object(path)
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            findings.append(f"evaluation_json_invalid:{name}:{type(exc).__name__}")
            continue
        if documents[name].get("paper_id") != paper_id:
            findings.append(f"evaluation_paper_id_mismatch:{name}")

    key_points = documents.get("reference_key_points.json", {}).get("items")
    conclusions = documents.get("reference_conclusions.json", {}).get("items")
    rules = documents.get("scoring_rules.json", {}).get("rules")
    evidence = documents.get("evidence_map.json", {}).get("evidence")
    failures = documents.get("critical_failures.json", {}).get("items")
    for label, value in (
        ("key_points", key_points),
        ("conclusions", conclusions),
        ("rules", rules),
        ("evidence", evidence),
        ("critical_failures", failures),
    ):
        if not isinstance(value, list) or not value:
            findings.append(f"evaluation_{label}_empty")
    key_points = key_points if isinstance(key_points, list) else []
    conclusions = conclusions if isinstance(conclusions, list) else []
    rules = rules if isinstance(rules, list) else []
    evidence = evidence if isinstance(evidence, list) else []

    key_ids: set[str] = set()
    conclusion_ids: set[str] = set()
    referenced_evidence: set[str] = set()
    for row in key_points:
        if not isinstance(row, dict):
            findings.append("key_point_not_object")
            continue
        identifier = str(row.get("key_point_id") or "").strip()
        if not identifier or identifier in key_ids:
            findings.append("key_point_id_invalid")
        key_ids.add(identifier)
        if not _has_value(row.get("statement")):
            findings.append(f"key_point_statement_invalid:{identifier or 'missing'}")
        if not _has_value(row.get("expected")):
            findings.append(f"key_point_expected_missing:{identifier or 'missing'}")
        ids = row.get("evidence_ids")
        if not isinstance(ids, list) or not ids:
            findings.append(f"key_point_evidence_missing:{identifier or 'missing'}")
        else:
            referenced_evidence.update(str(item) for item in ids)
    for row in conclusions:
        if not isinstance(row, dict):
            findings.append("conclusion_not_object")
            continue
        identifier = str(row.get("conclusion_id") or "").strip()
        if not identifier or identifier in conclusion_ids:
            findings.append("conclusion_id_invalid")
        conclusion_ids.add(identifier)
        if not _has_value(row.get("statement")):
            findings.append(f"conclusion_statement_invalid:{identifier or 'missing'}")
        if not _has_value(row.get("expected")):
            findings.append(f"conclusion_expected_missing:{identifier or 'missing'}")
        supports = row.get("supporting_key_point_ids")
        if not isinstance(supports, list) or not supports:
            findings.append(f"conclusion_support_missing:{identifier or 'missing'}")
        else:
            for key_id in supports:
                if key_id not in key_ids:
                    findings.append(f"conclusion_unknown_key_point:{identifier}:{key_id}")
        ids = row.get("evidence_ids")
        if not isinstance(ids, list) or not ids:
            findings.append(f"conclusion_evidence_missing:{identifier or 'missing'}")
        else:
            referenced_evidence.update(str(item) for item in ids)
    if conclusions and not any(
        isinstance(row, dict) and row.get("claim_role") == "final" for row in conclusions
    ):
        findings.append("final_conclusion_missing")

    evidence_ids = {
        str(row.get("evidence_id"))
        for row in evidence
        if isinstance(row, dict) and row.get("evidence_id") and _has_value(row.get("source"))
    }
    for evidence_id in sorted(referenced_evidence - evidence_ids):
        findings.append(f"evidence_reference_missing:{evidence_id}")

    covered: set[str] = set()
    rule_ids: set[str] = set()
    valid_references = key_ids | conclusion_ids
    for row in rules:
        if not isinstance(row, dict):
            findings.append("scoring_rule_not_object")
            continue
        rule_id = str(row.get("rule_id") or "").strip()
        reference_id = str(row.get("reference_id") or "").strip()
        rule_type = str(row.get("type") or "").strip()
        if not rule_id or rule_id in rule_ids:
            findings.append("scoring_rule_id_invalid")
        rule_ids.add(rule_id)
        if reference_id not in valid_references:
            findings.append(f"scoring_rule_reference_invalid:{rule_id or 'missing'}")
        else:
            covered.add(reference_id)
        if rule_type not in RULE_TYPES:
            findings.append(f"scoring_rule_type_invalid:{rule_id or 'missing'}")
        elif rule_type == "numeric":
            for field_name in ("target", "unit", "tolerance"):
                if not _has_value(row.get(field_name)):
                    findings.append(
                        f"numeric_rule_{field_name}_missing:{rule_id or 'missing'}"
                    )
            diagnostics.append(f"tolerance_requires_scientific_review:{rule_id or 'missing'}")
        elif not _has_value(row.get("expected")):
            findings.append(f"scoring_rule_expected_missing:{rule_id or 'missing'}")
        paths, fields, comparison = _binding_paths(row)
        if not paths or not fields or not comparison:
            findings.append(f"scoring_rule_binding_incomplete:{rule_id or 'missing'}")
        for path in paths:
            try:
                normalized = _safe_path(path)
            except ValueError:
                findings.append(f"scoring_rule_binding_path_invalid:{rule_id or 'missing'}")
                continue
            if normalized not in required_files:
                findings.append(
                    f"scoring_rule_binding_artifact_undeclared:{rule_id or 'missing'}:{normalized}"
                )
        if any(not field.startswith("$") for field in fields):
            findings.append(f"scoring_rule_binding_field_invalid:{rule_id or 'missing'}")
    for reference_id in sorted(valid_references - covered):
        findings.append(f"reference_without_scoring_rule:{reference_id}")
    return sorted(set(findings)), sorted(set(diagnostics))


def validate_task_package(root: str | Path) -> TaskPackageValidation:
    root = Path(root).resolve()
    findings: list[str] = []
    diagnostics: list[str] = []
    task_info: TaskInfo | None = None
    manifest: PackageManifest | None = None
    submission: dict[str, Any] = {}

    required = (
        root / "agent_input" / "task.md",
        root / "agent_input" / "submission_schema.json",
        root / "agent_input" / "data",
        root / "task_info.json",
        root / "evaluation",
        root / "package_manifest.json",
    )
    for path in required:
        if not path.exists():
            findings.append(f"required_path_missing:{path.relative_to(root).as_posix()}")
    task_path = root / "agent_input" / "task.md"
    if task_path.is_file() and not task_path.read_text(encoding="utf-8", errors="replace").strip():
        findings.append("task_instruction_empty")
    try:
        task_info = TaskInfo.model_validate(_json_object(root / "task_info.json"))
    except Exception as exc:
        findings.append(f"task_info_invalid:{type(exc).__name__}")
    try:
        submission = _json_object(root / "agent_input" / "submission_schema.json")
    except Exception as exc:
        findings.append(f"submission_schema_invalid:{type(exc).__name__}")
    required_files = submission.get("required_files")
    if not isinstance(required_files, list) or not required_files:
        findings.append("submission_required_files_empty")
        required_set: set[str] = set()
    else:
        try:
            required_set = {_safe_path(str(item)) for item in required_files}
        except ValueError:
            required_set = set()
            findings.append("submission_required_file_path_invalid")
    if task_info:
        if root.name != task_info.paper_id:
            findings.append("task_directory_paper_id_mismatch")
        if root.parent.name != task_info.task_type:
            findings.append("task_directory_type_mismatch")
        declared = {item.path for item in task_info.required_deliverables}
        if declared != required_set:
            findings.append("deliverable_submission_mismatch")
        for item in task_info.data:
            if not (root / "agent_input" / item.path).exists():
                findings.append(f"declared_data_missing:{item.path}")
        eval_findings, eval_diagnostics = validate_evaluation(
            root / "evaluation", paper_id=task_info.paper_id, required_files=required_set
        )
        findings.extend(eval_findings)
        diagnostics.extend(eval_diagnostics)
        if task_info.task_type in {"autonomous_research", "paper_reproduction"}:
            for path in (root / "agent_input").rglob("*"):
                if path.is_file() and path.suffix.casefold() == ".pdf":
                    findings.append(
                        f"paper_pdf_exposed_to_agent:{path.relative_to(root).as_posix()}"
                    )

    try:
        manifest = PackageManifest.model_validate(
            _json_object(root / "package_manifest.json")
        )
    except Exception as exc:
        findings.append(f"package_manifest_invalid:{type(exc).__name__}")
    if manifest:
        if task_info and (manifest.paper_id, manifest.task_type) != (
            task_info.paper_id,
            task_info.task_type,
        ):
            findings.append("manifest_identity_mismatch")
        try:
            actual = package_payload_entries(root)
        except ValueError as exc:
            findings.append(f"package_payload_invalid:{exc}")
            actual = []
        if manifest.entries != actual:
            findings.append("manifest_entries_mismatch")
        if manifest.package_content_sha256 != package_content_hash(actual):
            findings.append("package_content_hash_mismatch")

    return TaskPackageValidation(
        status="failed" if findings else "passed",
        paper_id=task_info.paper_id if task_info else "",
        task_type=task_info.task_type if task_info else "",
        findings=sorted(set(findings)),
        diagnostics=sorted(set(diagnostics)),
    )
