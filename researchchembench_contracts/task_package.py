"""Task Package v1 models and transport-only validation.

The models in this module deliberately avoid scientific judgement and scoring
policy.  Producers decide the scientific content of a reference; benchmark
adapters decide how that reference is scored.  This shared layer only protects
identity, path safety, public/private visibility, hashes, and reference links.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path, PurePosixPath
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


TASK_PACKAGE_SCHEMA_V1 = "researchchembench.task-package.v1"
TASK_INFO_SCHEMA_V1 = "researchchembench.task-info.v1"
SUBMISSION_SCHEMA_V1 = "researchchembench.submission-schema.v1"
PACKAGE_MANIFEST_SCHEMA_V1 = "researchchembench.package-manifest.v1"
COMPUTATIONAL_REFERENCE_SCHEMA_V1 = "computational-science-reference.v1"

TaskType = Literal[
    "paper_reproduction",
    "autonomous_research",
    "experiment_validation",
]
RuntimeReadiness = Literal["ready", "needs_software"]
Visibility = Literal[
    "public_instruction",
    "public_metadata",
    "public_contract",
    "public_data",
    "private_reference",
    "private_asset",
]

_REQUIRED_TOP_LEVEL = {
    "task.md",
    "task_info.json",
    "submission_schema.json",
    "data",
    "evaluation",
    "package_manifest.json",
}
_PUBLIC_VISIBILITIES = {
    "public_instruction",
    "public_metadata",
    "public_contract",
    "public_data",
}


def _safe_relative_posix(value: str, *, allow_glob: bool = False) -> str:
    if not value or "\\" in value or "\x00" in value:
        raise ValueError("path must be a non-empty relative POSIX path")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or "." in path.parts:
        raise ValueError("path must be a safe relative POSIX path")
    if not allow_glob and any(character in value for character in "*?[]"):
        raise ValueError("path must not contain glob syntax")
    return path.as_posix()


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class DataFileV1(StrictModel):
    name: str
    path: str
    type: str = ""
    description: str = ""

    @field_validator("path")
    @classmethod
    def safe_path(cls, value: str) -> str:
        value = _safe_relative_posix(value)
        if value != "data" and not value.startswith("data/"):
            raise ValueError("task data paths must be rooted below data/")
        return value


class RequiredDeliverableV1(StrictModel):
    path: str
    description: str = ""
    allow_empty: bool = False

    @field_validator("path")
    @classmethod
    def safe_path(cls, value: str) -> str:
        return _safe_relative_posix(value)


class RequiredCapabilityV1(StrictModel):
    capability: str
    preferred_software: list[str] = Field(default_factory=list)
    required: bool = True
    purpose: str = ""


class TaskInfoV1(StrictModel):
    schema_version: Literal["researchchembench.task-info.v1"] = TASK_INFO_SCHEMA_V1
    task_id: str
    task_family_id: str
    task_type: TaskType
    source_id: str
    title: str
    category: str
    tags: list[str] = Field(default_factory=list)
    runtime_readiness: RuntimeReadiness = "ready"
    required_capabilities: list[RequiredCapabilityV1] = Field(default_factory=list)
    data: list[DataFileV1] = Field(default_factory=list)
    required_deliverables: list[RequiredDeliverableV1] = Field(default_factory=list)
    related_task_ids: list[str] = Field(default_factory=list)
    reference_schema: str

    @field_validator("task_id", "task_family_id", "source_id", "title", "category", "reference_schema")
    @classmethod
    def non_empty_text(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("value must be non-empty")
        return value

    @model_validator(mode="after")
    def unique_lists(self) -> "TaskInfoV1":
        if len(self.related_task_ids) != len(set(self.related_task_ids)):
            raise ValueError("related_task_ids must be unique")
        paths = [item.path for item in self.required_deliverables]
        if len(paths) != len(set(paths)):
            raise ValueError("required_deliverable paths must be unique")
        return self


class SubmissionSchemaV1(StrictModel):
    schema_version: Literal[
        "researchchembench.submission-schema.v1"
    ] = SUBMISSION_SCHEMA_V1
    task_id: str
    required_files: list[str]
    primary_result_file: str | None = None
    result_schema: dict[str, Any] = Field(default_factory=dict)
    allowed_extra_fields: bool = True

    @field_validator("required_files")
    @classmethod
    def safe_required_files(cls, values: list[str]) -> list[str]:
        normalized = [_safe_relative_posix(value) for value in values]
        if not normalized:
            raise ValueError("required_files must not be empty")
        if len(normalized) != len(set(normalized)):
            raise ValueError("required_files must be unique")
        return normalized

    @field_validator("primary_result_file")
    @classmethod
    def safe_primary_result_file(cls, value: str | None) -> str | None:
        return _safe_relative_posix(value) if value else None

    @model_validator(mode="after")
    def primary_is_required(self) -> "SubmissionSchemaV1":
        if self.primary_result_file and self.primary_result_file not in self.required_files:
            raise ValueError("primary_result_file must be included in required_files")
        return self


class AnswerItemV1(StrictModel):
    answer_id: str
    kind: str
    canonical_answer: Any
    claim_role: Literal["intermediate", "final"]
    evidence_grade: str = ""
    evidence_ids: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class AcceptanceProfileV1(StrictModel):
    acceptance_profile_id: str
    answer_id: str
    acceptance_type: str
    parameters: dict[str, Any] = Field(default_factory=dict)
    required_propositions: list[str] = Field(default_factory=list)
    forbidden_contradictions: list[str] = Field(default_factory=list)
    description: str = ""


class SubmissionBindingV1(StrictModel):
    binding_id: str
    acceptance_profile_id: str
    artifact_paths: list[str]
    observed_fields: list[str]
    comparison: str
    document_binding: bool = False

    @field_validator("artifact_paths")
    @classmethod
    def safe_artifact_paths(cls, values: list[str]) -> list[str]:
        normalized = [_safe_relative_posix(value) for value in values]
        if not normalized:
            raise ValueError("artifact_paths must not be empty")
        return normalized

    @model_validator(mode="after")
    def observed_selector_present(self) -> "SubmissionBindingV1":
        if not self.observed_fields:
            raise ValueError("observed_fields must not be empty")
        if not self.comparison.strip():
            raise ValueError("comparison must be non-empty")
        return self


class ProcessKeyPointV1(StrictModel):
    key_point_id: str
    title: str
    description: str
    evidence_requirements: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class FinalConclusionV1(StrictModel):
    conclusion_id: str
    statement: Any
    answer_ids: list[str]
    acceptance_profile_ids: list[str]
    required_evidence: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def references_present(self) -> "FinalConclusionV1":
        if not self.answer_ids:
            raise ValueError("final conclusions must reference at least one answer")
        if not self.acceptance_profile_ids:
            raise ValueError(
                "final conclusions must reference at least one acceptance profile"
            )
        return self


class ComputationalScienceReferenceV1(StrictModel):
    schema_version: Literal[
        "computational-science-reference.v1"
    ] = COMPUTATIONAL_REFERENCE_SCHEMA_V1
    task_id: str
    task_type: Literal["paper_reproduction", "autonomous_research"]
    answer_items: list[AnswerItemV1]
    acceptance_profiles: list[AcceptanceProfileV1]
    submission_bindings: list[SubmissionBindingV1]
    process_key_points: list[ProcessKeyPointV1]
    final_conclusions: list[FinalConclusionV1]
    critical_failures: list[str] = Field(default_factory=list)
    private_evidence: dict[str, Any] = Field(default_factory=dict)
    evaluation_constraints: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def linked_contract(self) -> "ComputationalScienceReferenceV1":
        answer_ids = [item.answer_id for item in self.answer_items]
        profile_ids = [item.acceptance_profile_id for item in self.acceptance_profiles]
        binding_ids = [item.binding_id for item in self.submission_bindings]
        key_point_ids = [item.key_point_id for item in self.process_key_points]
        conclusion_ids = [item.conclusion_id for item in self.final_conclusions]
        for label, values in (
            ("answer", answer_ids),
            ("acceptance profile", profile_ids),
            ("submission binding", binding_ids),
            ("process key point", key_point_ids),
            ("final conclusion", conclusion_ids),
        ):
            if len(values) != len(set(values)):
                raise ValueError(f"{label} IDs must be unique")
        if not answer_ids:
            raise ValueError("answer_items must not be empty")
        if not self.process_key_points:
            raise ValueError("process_key_points must not be empty")
        if not self.final_conclusions:
            raise ValueError("final_conclusions must not be empty")
        answer_set = set(answer_ids)
        profile_set = set(profile_ids)
        profile_by_id = {
            item.acceptance_profile_id: item for item in self.acceptance_profiles
        }
        for profile in self.acceptance_profiles:
            if profile.answer_id not in answer_set:
                raise ValueError(
                    f"acceptance profile references unknown answer: {profile.answer_id}"
                )
        bindings_by_profile: dict[str, int] = {}
        for binding in self.submission_bindings:
            if binding.acceptance_profile_id not in profile_set:
                raise ValueError(
                    "submission binding references unknown acceptance profile: "
                    f"{binding.acceptance_profile_id}"
                )
            bindings_by_profile[binding.acceptance_profile_id] = (
                bindings_by_profile.get(binding.acceptance_profile_id, 0) + 1
            )
        for profile_id in profile_by_id:
            if bindings_by_profile.get(profile_id) != 1:
                raise ValueError(
                    "each acceptance profile requires exactly one submission binding: "
                    f"{profile_id}"
                )
        for conclusion in self.final_conclusions:
            unknown_answers = set(conclusion.answer_ids) - answer_set
            unknown_profiles = set(conclusion.acceptance_profile_ids) - profile_set
            if unknown_answers:
                raise ValueError(
                    f"final conclusion references unknown answers: {sorted(unknown_answers)}"
                )
            if unknown_profiles:
                raise ValueError(
                    "final conclusion references unknown acceptance profiles: "
                    f"{sorted(unknown_profiles)}"
                )
            for profile_id in conclusion.acceptance_profile_ids:
                if profile_by_id[profile_id].answer_id not in conclusion.answer_ids:
                    raise ValueError(
                        "final conclusion profile owner is not included in answer_ids: "
                        f"{profile_id}"
                    )
        return self


class ManifestEntryV1(StrictModel):
    path: str
    sha256: str
    size_bytes: int
    visibility: Visibility

    @field_validator("path")
    @classmethod
    def safe_path(cls, value: str) -> str:
        return _safe_relative_posix(value)

    @field_validator("sha256")
    @classmethod
    def valid_sha256(cls, value: str) -> str:
        value = value.strip().casefold()
        if len(value) != 64 or any(character not in "0123456789abcdef" for character in value):
            raise ValueError("sha256 must contain 64 hexadecimal characters")
        return value

    @field_validator("size_bytes")
    @classmethod
    def valid_size(cls, value: int) -> int:
        if value < 0:
            raise ValueError("size_bytes must be non-negative")
        return value


class PackageManifestV1(StrictModel):
    schema_version: Literal[
        "researchchembench.package-manifest.v1"
    ] = PACKAGE_MANIFEST_SCHEMA_V1
    package_schema: Literal[
        "researchchembench.task-package.v1"
    ] = TASK_PACKAGE_SCHEMA_V1
    task_id: str
    task_family_id: str
    task_type: TaskType
    reference_schema: str
    assembler_version: str
    package_content_sha256: str
    entries: list[ManifestEntryV1]
    public_to_agent: list[str]
    manifest_self_excluded: Literal[True] = True

    @field_validator("package_content_sha256")
    @classmethod
    def valid_content_sha256(cls, value: str) -> str:
        return ManifestEntryV1.valid_sha256(value)

    @field_validator("public_to_agent")
    @classmethod
    def safe_public_paths(cls, values: list[str]) -> list[str]:
        normalized = [_safe_relative_posix(value, allow_glob=True) for value in values]
        if len(normalized) != len(set(normalized)):
            raise ValueError("public_to_agent entries must be unique")
        return normalized

    @model_validator(mode="after")
    def unique_entries(self) -> "PackageManifestV1":
        paths = [entry.path for entry in self.entries]
        if len(paths) != len(set(paths)):
            raise ValueError("manifest entry paths must be unique")
        if "package_manifest.json" in paths:
            raise ValueError("package_manifest.json must be self-excluded")
        return self


class TaskPackageValidation(StrictModel):
    status: Literal["passed", "failed"]
    task_id: str = ""
    task_type: str = ""
    reference_schema: str = ""
    findings: list[str] = Field(default_factory=list)
    diagnostics: list[str] = Field(default_factory=list)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _visibility(path: str) -> Visibility:
    if path == "task.md":
        return "public_instruction"
    if path == "task_info.json":
        return "public_metadata"
    if path == "submission_schema.json":
        return "public_contract"
    if path.startswith("data/"):
        return "public_data"
    if path == "evaluation/reference.json":
        return "private_reference"
    if path.startswith("evaluation/hidden_assets/"):
        return "private_asset"
    raise ValueError(f"file is outside the Task Package v1 allowlist: {path}")


def package_payload_entries(root: Path) -> list[ManifestEntryV1]:
    """Return deterministic payload entries, excluding the self-referential manifest."""

    values: list[ManifestEntryV1] = []
    for path in sorted(root.rglob("*")):
        if path.is_symlink():
            raise ValueError(f"symbolic links are not allowed in task packages: {path}")
        if not path.is_file() or path.name == "package_manifest.json":
            continue
        relative = path.relative_to(root).as_posix()
        values.append(
            ManifestEntryV1(
                path=relative,
                sha256=_sha256(path),
                size_bytes=path.stat().st_size,
                visibility=_visibility(relative),
            )
        )
    return values


def _content_hash(entries: list[ManifestEntryV1]) -> str:
    payload = [entry.model_dump(mode="json") for entry in entries]
    encoded = json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _jsonpath_tokens(value: str) -> list[str | int] | None:
    path = str(value or "").strip()
    if path and not path.startswith("$") and re.fullmatch(
        r"[A-Za-z_][A-Za-z0-9_-]*(?:\.[A-Za-z_][A-Za-z0-9_-]*)*", path
    ):
        return path.split(".")
    if path == "$":
        return []
    if not path.startswith("$"):
        return None
    tail = path[1:]
    tokens: list[str | int] = []
    position = 0
    token_pattern = re.compile(
        r"(?:\.([A-Za-z_][A-Za-z0-9_-]*)|\[(\*|\d+|['\"][^'\"]+['\"])\])"
    )
    while position < len(tail):
        match = token_pattern.match(tail, position)
        if match is None:
            return None
        dotted, bracket = match.groups()
        if dotted is not None:
            tokens.append(dotted)
        elif bracket == "*":
            tokens.append("*")
        elif bracket.isdigit():
            tokens.append(int(bracket))
        else:
            tokens.append(bracket[1:-1])
        position = match.end()
    return tokens


def _schema_path_status(schema: Any, tokens: list[str | int]) -> str:
    """Return present, open, or missing for a structured submission field."""

    current = schema
    for token in tokens:
        if not isinstance(current, dict):
            return "missing"
        if token == "*":
            if isinstance(current.get("items"), dict):
                current = current["items"]
                continue
            if isinstance(current.get("additionalProperties"), dict):
                current = current["additionalProperties"]
                continue
            if current.get("additionalProperties") is True:
                return "open"
            return "missing"
        if isinstance(token, int):
            if not isinstance(current.get("items"), dict):
                return "missing"
            current = current["items"]
            continue
        properties = current.get("properties")
        if isinstance(properties, dict) and token in properties:
            current = properties[token]
            continue
        if isinstance(current.get("additionalProperties"), dict):
            current = current["additionalProperties"]
            continue
        if current.get("additionalProperties") is True or (
            "additionalProperties" not in current and not isinstance(properties, dict)
        ):
            return "open"
        return "missing"
    return "present"


def _binding_schema_findings(
    *,
    submission: SubmissionSchemaV1,
    reference: ComputationalScienceReferenceV1,
) -> list[str]:
    findings: list[str] = []
    required_files = set(submission.required_files)
    for binding in reference.submission_bindings:
        for artifact in binding.artifact_paths:
            if artifact not in required_files:
                findings.append(
                    f"binding_artifact_not_required:{binding.binding_id}:{artifact}"
                )
        if binding.document_binding or binding.observed_fields == ["document"]:
            continue
        if not submission.primary_result_file:
            findings.append(
                f"structured_binding_without_primary_result:{binding.binding_id}"
            )
            continue
        if submission.primary_result_file not in binding.artifact_paths:
            findings.append(
                f"structured_binding_wrong_artifact:{binding.binding_id}"
            )
        for observed in binding.observed_fields:
            tokens = _jsonpath_tokens(observed)
            if tokens is None:
                findings.append(
                    f"binding_jsonpath_invalid:{binding.binding_id}:{observed}"
                )
                continue
            status = _schema_path_status(submission.result_schema, tokens)
            if status != "present":
                findings.append(
                    f"binding_schema_path_{status}:{binding.binding_id}:{observed}"
                )
    return findings


def validate_task_package(root: str | Path) -> TaskPackageValidation:
    """Validate one complete Task Package v1 without making scientific decisions."""

    root = Path(root).expanduser().resolve()
    findings: list[str] = []
    diagnostics: list[str] = []
    task_info: TaskInfoV1 | None = None
    manifest: PackageManifestV1 | None = None
    submission: SubmissionSchemaV1 | None = None
    if not root.is_dir():
        return TaskPackageValidation(
            status="failed", findings=["task_package_missing"]
        )
    actual_top = {path.name for path in root.iterdir()}
    for name in sorted(_REQUIRED_TOP_LEVEL - actual_top):
        findings.append(f"required_top_level_missing:{name}")
    for name in sorted(actual_top - _REQUIRED_TOP_LEVEL):
        findings.append(f"unexpected_top_level_entry:{name}")
    task_text_path = root / "task.md"
    if task_text_path.is_file() and not task_text_path.read_text(
        encoding="utf-8", errors="replace"
    ).strip():
        findings.append("task_instruction_empty")

    try:
        task_info = TaskInfoV1.model_validate(_read_json(root / "task_info.json"))
    except Exception as exc:  # pydantic/json errors are reported as contract findings
        findings.append(f"task_info_invalid:{type(exc).__name__}:{exc}")
    try:
        submission = SubmissionSchemaV1.model_validate(
            _read_json(root / "submission_schema.json")
        )
    except Exception as exc:
        findings.append(f"submission_schema_invalid:{type(exc).__name__}:{exc}")
    try:
        manifest = PackageManifestV1.model_validate(
            _read_json(root / "package_manifest.json")
        )
    except Exception as exc:
        findings.append(f"package_manifest_invalid:{type(exc).__name__}:{exc}")

    if task_info:
        if root.name != task_info.task_id:
            findings.append("task_directory_id_mismatch")
        if submission and submission.task_id != task_info.task_id:
            findings.append("submission_task_id_mismatch")
        for item in task_info.data:
            if not (root / item.path).exists():
                findings.append(f"declared_data_missing:{item.path}")
        deliverables = {item.path for item in task_info.required_deliverables}
        if submission and deliverables != set(submission.required_files):
            findings.append("deliverable_submission_required_files_mismatch")
        reference_path = root / "evaluation" / "reference.json"
        if reference_path.is_file():
            try:
                reference_value = _read_json(reference_path)
            except Exception as exc:
                findings.append(f"reference_invalid_json:{type(exc).__name__}:{exc}")
            else:
                schema = str(
                    reference_value.get("schema_version")
                    if isinstance(reference_value, dict)
                    else ""
                )
                if schema != task_info.reference_schema:
                    findings.append("reference_schema_mismatch")
                elif schema == COMPUTATIONAL_REFERENCE_SCHEMA_V1:
                    try:
                        reference = ComputationalScienceReferenceV1.model_validate(
                            reference_value
                        )
                    except Exception as exc:
                        findings.append(
                            f"computational_reference_invalid:{type(exc).__name__}:{exc}"
                        )
                    else:
                        if reference.task_id != task_info.task_id:
                            findings.append("reference_task_id_mismatch")
                        if reference.task_type != task_info.task_type:
                            findings.append("reference_task_type_mismatch")
                        if submission:
                            findings.extend(
                                _binding_schema_findings(
                                    submission=submission, reference=reference
                                )
                            )
                else:
                    diagnostics.append(f"reference_schema_unregistered:{schema}")

    if manifest:
        if task_info:
            for field_name in (
                "task_id",
                "task_family_id",
                "task_type",
                "reference_schema",
            ):
                if getattr(manifest, field_name) != getattr(task_info, field_name):
                    findings.append(f"manifest_{field_name}_mismatch")
        try:
            actual_entries = package_payload_entries(root)
        except (OSError, ValueError) as exc:
            findings.append(f"package_payload_invalid:{type(exc).__name__}:{exc}")
            actual_entries = []
        expected_by_path = {entry.path: entry for entry in manifest.entries}
        actual_by_path = {entry.path: entry for entry in actual_entries}
        for path in sorted(set(expected_by_path) - set(actual_by_path)):
            findings.append(f"manifest_entry_missing:{path}")
        for path in sorted(set(actual_by_path) - set(expected_by_path)):
            findings.append(f"manifest_entry_unlisted:{path}")
        for path in sorted(set(expected_by_path) & set(actual_by_path)):
            if expected_by_path[path] != actual_by_path[path]:
                findings.append(f"manifest_entry_mismatch:{path}")
        if manifest.package_content_sha256 != _content_hash(actual_entries):
            findings.append("package_content_hash_mismatch")
        entry_by_path = {entry.path: entry for entry in manifest.entries}
        for path in manifest.public_to_agent:
            if path.endswith("/**"):
                prefix = path[:-2]
                matches = [
                    entry
                    for entry in manifest.entries
                    if entry.path.startswith(prefix)
                ]
            else:
                matches = [entry_by_path[path]] if path in entry_by_path else []
            if not matches:
                findings.append(f"public_allowlist_unmatched:{path}")
            for entry in matches:
                if entry.visibility not in _PUBLIC_VISIBILITIES:
                    findings.append(f"private_entry_publicly_allowlisted:{entry.path}")

    return TaskPackageValidation(
        status="failed" if findings else "passed",
        task_id=task_info.task_id if task_info else "",
        task_type=task_info.task_type if task_info else "",
        reference_schema=task_info.reference_schema if task_info else "",
        findings=sorted(set(findings)),
        diagnostics=sorted(set(diagnostics)),
    )


def package_content_hash(entries: list[ManifestEntryV1]) -> str:
    """Public helper used by deterministic assemblers."""

    return _content_hash(entries)
