"""Task Package v1 models and transport-only validation.

The models in this module deliberately avoid scientific judgement and scoring
policy.  Producers decide the scientific content of a reference; benchmark
adapters decide how that reference is scored.  This shared layer only protects
identity, path safety, public/private visibility, hashes, and reference links.
"""

from __future__ import annotations

import hashlib
import json
import math
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
    # Evaluator-only transport metadata; never copied to the public submission
    # schema or Agent workspace.
    canonical_projection: Any | None = None

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
        answer_by_id = {item.answer_id: item for item in self.answer_items}
        profile_set = set(profile_ids)
        profile_by_id = {
            item.acceptance_profile_id: item for item in self.acceptance_profiles
        }
        for profile in self.acceptance_profiles:
            if profile.answer_id not in answer_set:
                raise ValueError(
                    f"acceptance profile references unknown answer: {profile.answer_id}"
                )
                continue
            acceptance_type = profile.acceptance_type.strip().casefold()
            answer = answer_by_id[profile.answer_id]
            if acceptance_type in {"semantic_propositions", "mechanism_claim"}:
                if not profile.required_propositions:
                    raise ValueError(
                        "semantic acceptance profile requires propositions: "
                        f"{profile.acceptance_profile_id}"
                    )
            elif acceptance_type == "numeric_tolerance":
                if answer.canonical_answer is None:
                    raise ValueError(
                        "numeric acceptance profile requires a canonical answer: "
                        f"{profile.acceptance_profile_id}"
                    )
                parameters = profile.parameters
                vector = parameters.get("numeric_tolerances")
                vector_valid = isinstance(vector, dict) and bool(vector) and all(
                    str(key).strip()
                    and isinstance(value, (int, float))
                    and not isinstance(value, bool)
                    and math.isfinite(float(value))
                    and float(value) >= 0
                    for key, value in vector.items()
                )
                scalar_tolerance = any(
                    isinstance(parameters.get(key), (int, float))
                    and not isinstance(parameters.get(key), bool)
                    and math.isfinite(float(parameters[key]))
                    and float(parameters[key]) >= 0
                    for key in ("absolute_tolerance", "relative_tolerance")
                )
                if not vector_valid and not str(parameters.get("unit") or "").strip():
                    raise ValueError(
                        "numeric acceptance profile requires an explicit unit: "
                        f"{profile.acceptance_profile_id}"
                    )
                if not vector_valid and not scalar_tolerance:
                    raise ValueError(
                        "numeric acceptance profile requires a tolerance: "
                        f"{profile.acceptance_profile_id}"
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
            owner = profile_by_id[binding.acceptance_profile_id]
            if (
                binding.document_binding
                and owner.acceptance_type.strip().casefold()
                not in {
                    "semantic_propositions",
                    "mechanism_claim",
                    "artifact_validation",
                }
                and binding.canonical_projection is None
            ):
                raise ValueError(
                    "non-semantic document binding requires canonical projection: "
                    f"{binding.binding_id}"
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
    if path in {
        "evaluation/reference_key_points.json",
        "evaluation/reference_conclusions.json",
        "evaluation/scoring_rules.json",
        "evaluation/evidence_map.json",
        "evaluation/critical_failures.json",
    }:
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


def normalize_process_rubric(value: Any) -> Any:
    """Unwrap the supported process-Key-Point container spellings losslessly.

    Stage06 agents have historically emitted either a top-level list or one of
    ``criteria``, ``items``, ``rubric`` and ``key_points``.  These names are
    serialization wrappers, not separate scientific schemas.  The helper keeps
    every row and authored field intact, adding only the transport alias fields
    needed by downstream readers.  An unknown non-empty object is returned
    unchanged so callers can report a contract finding instead of silently
    turning it into an empty rubric.
    """

    if isinstance(value, list):
        rows = list(value)
    elif isinstance(value, dict):
        rows = []
        recognized = False
        for key in ("criteria", "items", "rubric", "key_points"):
            candidate = value.get(key)
            if isinstance(candidate, list):
                recognized = True
                rows.extend(candidate)
        if not recognized:
            return value
    else:
        return value

    output: list[Any] = []
    seen: set[str] = set()
    for row in rows:
        if not isinstance(row, dict):
            # Preserve malformed rows for the validator; dropping them would
            # hide an Agent contract error and change the authored rubric.
            output.append(row)
            continue
        normalized = dict(row)
        evidence = (
            normalized.get("evidence_artifacts")
            or normalized.get("required_evidence")
            or normalized.get("required_artifact")
        )
        if evidence and "evidence_artifacts" not in normalized:
            normalized["evidence_artifacts"] = evidence
        if evidence and "required_evidence" not in normalized:
            normalized["required_evidence"] = evidence
        marker = json.dumps(normalized, ensure_ascii=False, sort_keys=True, default=str)
        if marker in seen:
            continue
        seen.add(marker)
        output.append(normalized)
    return output


def process_rubric_container_findings(value: Any) -> list[str]:
    """Report only container-shape problems for a process rubric."""

    if isinstance(value, list):
        return [] if value else ["process_rubric_empty"]
    if isinstance(value, dict):
        if any(isinstance(value.get(key), list) for key in ("criteria", "items", "rubric", "key_points")):
            return []
        return ["process_rubric_wrapper_unknown"] if value else ["process_rubric_empty"]
    return ["process_rubric_container_invalid"]


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


def _safe_document_artifact(value: Any) -> bool:
    """Return whether a relative path can safely denote a text/report artifact."""

    if not isinstance(value, str) or not value.strip():
        return False
    path = PurePosixPath(value.strip())
    return (
        not path.is_absolute()
        and ".." not in path.parts
        and "\\" not in value
        and path.suffix.casefold() in {".md", ".txt", ".json", ".jsonl"}
    )


def is_document_selector(
    field: Any,
    artifact_paths: list[str] | None = None,
    *,
    allow_json_artifact: bool = False,
) -> bool:
    """Identify transport-level document selectors without judging their prose.

    A bare ``report/results.json`` path is not treated as a document by default:
    it is normally a structured result artifact and must either be projected to a
    JSONPath or be explicitly marked as a document binding.  Markdown/text report
    paths remain compatible with older receipts.
    """

    token = str(field or "").strip().casefold()
    if token in {"document", "text", "report"}:
        return True
    if not artifact_paths or token not in {
        str(path).strip().casefold() for path in artifact_paths
    }:
        return False
    value = str(field).strip()
    if not _safe_document_artifact(value):
        return False
    suffix = PurePosixPath(value).suffix.casefold()
    return suffix in {".md", ".txt"} or (
        allow_json_artifact and suffix in {".json", ".jsonl"}
    )


def is_document_binding_selector(
    field: Any,
    artifact_paths: list[str] | None = None,
    *,
    document_binding: bool = False,
) -> bool:
    """Recognize a report selector, including legacy semantic labels.

    Older receipts used a JSONPath-shaped label for a report-only binding.  If
    the binding explicitly declares document mode and has no structured JSON
    result artifact, that label is transport metadata rather than a schema path.
    Mixed bindings still validate their structured selectors normally.
    """

    if is_document_selector(
        field,
        artifact_paths,
        allow_json_artifact=document_binding,
    ):
        return True
    if not document_binding:
        return False
    artifacts = artifact_paths or []
    has_structured_artifact = any(
        PurePosixPath(str(path)).suffix.casefold() in {".json", ".jsonl"}
        for path in artifacts
    )
    return not has_structured_artifact


def is_safe_jsonpath_filter(value: Any) -> bool:
    """Accept the small, answer-free filter form used by result-array bindings.

    The evaluator owns semantic interpretation.  The package contract only
    needs to ensure that a filter is bounded to one array member selected by a
    literal field equality and followed by ordinary child selectors.
    """

    path = str(value or "").strip()
    marker = "[?(@"
    if marker not in path:
        return False
    prefix, remainder = path.split(marker, 1)
    if _jsonpath_tokens(prefix) is None:
        return False
    match = re.match(
        r"\.([A-Za-z_][A-Za-z0-9_-]*)\s*==\s*(['\"])([^'\"]*)\2\)\](.*)$",
        remainder,
    )
    if match is None:
        return False
    suffix = match.group(4)
    if not suffix:
        return True
    return _jsonpath_tokens("$" + suffix) is not None


def normalize_binding_observed_fields(binding: dict[str, Any]) -> list[str]:
    """Project one unambiguous legacy artifact/target spelling to selectors.

    Some historical receipts used ``observed_fields`` for an artifact path and
    put the actual structured result keys in ``target_fields``.  When exactly
    one observed JSON result artifact is present, that mapping is transport-
    deterministic.  Report selectors are retained for mixed bindings; multiple
    structured artifacts remain untouched and are rejected by normal validation
    instead of being guessed.
    """

    def values(value: Any) -> list[str]:
        if isinstance(value, str) and value.strip():
            return [value.strip()]
        if isinstance(value, list):
            return [str(item).strip() for item in value if str(item).strip()]
        return []

    def selector(value: str) -> str:
        if value.startswith("$"):
            return value
        if re.fullmatch(
            r"[A-Za-z_][A-Za-z0-9_-]*(?:\.[A-Za-z_][A-Za-z0-9_-]*)*", value
        ):
            return f"$.{value}"
        return value

    raw_artifacts = (
        binding.get("artifact_paths")
        or binding.get("artifact_path")
        or binding.get("artifact")
        or binding.get("artifacts")
    )
    artifact_rows = raw_artifacts if isinstance(raw_artifacts, list) else [raw_artifacts]
    artifacts = []
    artifact_json_paths: list[str] = []
    artifact_document_paths: list[str] = []
    for item in artifact_rows:
        if isinstance(item, dict):
            path = str(item.get("path") or item.get("file") or "").strip()
            json_path = str(item.get("json_path") or item.get("selector") or "").strip()
            if json_path:
                artifact_json_paths.append(json_path)
            elif PurePosixPath(path).suffix.casefold() in {".md", ".txt"}:
                artifact_document_paths.append(path)
        else:
            path = str(item or "").strip()
            if PurePosixPath(path).suffix.casefold() in {".md", ".txt"}:
                artifact_document_paths.append(path)
        if path and path not in artifacts:
            artifacts.append(path)
    observed = values(
        binding.get("observed_fields")
        or binding.get("observed_field")
        or binding.get("field")
    )
    targets = values(binding.get("target_fields"))
    for field in artifact_json_paths:
        if field not in observed:
            observed.append(field)
    for field in artifact_document_paths:
        if field not in observed:
            observed.append(field)
    if not observed or not targets:
        return observed
    artifact_by_folded = {item.casefold(): item for item in artifacts}
    structured = [
        field
        for field in observed
        if field.casefold() in artifact_by_folded
        and PurePosixPath(field).suffix.casefold() in {".json", ".jsonl"}
    ]
    if len(structured) != 1:
        return observed
    return [
        *[selector(field) for field in targets],
        *[
            field
            for field in observed
            if field.casefold() not in {item.casefold() for item in structured}
        ],
    ]


def normalize_binding_artifact_paths(binding: dict[str, Any]) -> list[str]:
    """Extract safe transport paths from string or ``{path, json_path}`` rows."""

    raw = (
        binding.get("artifact_paths")
        or binding.get("artifact_path")
        or binding.get("artifact")
        or binding.get("artifacts")
    )
    rows = raw if isinstance(raw, list) else [raw]
    output: list[str] = []
    for item in rows:
        if isinstance(item, dict):
            value = item.get("path") or item.get("file")
        else:
            value = item
        text = str(value or "").strip()
        if text and text not in output:
            output.append(text)
    return output


def normalize_binding_contract(
    binding: dict[str, Any],
    *,
    profile: dict[str, Any] | None = None,
    answer: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Normalize legacy binding rows and copy authored acceptance semantics.

    This is a transport projection only.  When a binding already names at least
    one artifact and selector but omits comparison/projection fields, those
    fields are copied from the owning profile/answer; no value or proposition is
    invented.  An empty binding remains empty and therefore still blocks.
    """

    def as_string_list(value: Any) -> list[str]:
        if isinstance(value, str) and value.strip():
            return [value.strip()]
        if isinstance(value, list):
            return [str(item).strip() for item in value if str(item).strip()]
        return []

    normalized = json.loads(json.dumps(binding, ensure_ascii=False))
    if normalized.get("canonical_projection") is None and "projection" in normalized:
        normalized["canonical_projection"] = normalized.get("projection")
    if not str(normalized.get("comparison") or "").strip() and normalized.get(
        "comparison_type"
    ) is not None:
        normalized["comparison"] = normalized.get("comparison_type")
    # Extract selectors while the original artifact rows are still present;
    # converting ``{path, json_path}`` rows to bare paths first would silently
    # discard the structured selector and could turn a mixed binding into a
    # report-only binding.
    fields = normalize_binding_observed_fields(normalized)
    artifacts = normalize_binding_artifact_paths(normalized)
    if artifacts:
        normalized["artifact_paths"] = artifacts
    if fields:
        normalized["observed_fields"] = fields
    document_hint = bool(
        normalized.get("document_binding")
        or normalized.get("document_target") is not None
    )
    structured_fields = [
        field
        for field in fields
        if not is_document_binding_selector(
            field,
            artifacts,
            document_binding=document_hint,
        )
    ]
    # Comparison is a typed transport operator and is uniquely determined by
    # an already-authored profile type even for document bindings.  Projection
    # remains optional for document/identity bindings in SubmissionBindingV1;
    # only structured fields receive the bounded projection below.
    if artifacts and fields:
        profile = profile or {}
        answer = answer or {}
        if not str(normalized.get("comparison") or "").strip():
            normalized["comparison"] = str(
                profile.get("comparison")
                or profile.get("type")
                or profile.get("acceptance_type")
                or answer.get("acceptance_type")
                or ""
            ).strip()
    # Copying authored answer semantics is safe only when the binding already
    # identifies a structured result field.  A report-only/document binding
    # does not need a canonical projection under the formal package model.
    if artifacts and structured_fields:
        profile = profile or {}
        answer = answer or {}
        if normalized.get("canonical_projection") is None and normalized.get(
            "projection"
        ) is None:
            profile_type = str(
                profile.get("type")
                or profile.get("acceptance_type")
                or answer.get("acceptance_type")
                or ""
            ).strip()
            if profile_type in {"semantic_propositions", "mechanism_claim"}:
                normalized["canonical_projection"] = {
                    "required_propositions": as_string_list(
                        profile.get("required_propositions")
                        or answer.get("required_propositions")
                    ),
                    "forbidden_contradictions": as_string_list(
                        profile.get("forbidden_contradictions")
                        or answer.get("forbidden_contradictions")
                    ),
                }
            elif profile_type == "trend":
                normalized["canonical_projection"] = {
                    "required_trends": as_string_list(
                        profile.get("required_trends")
                        or profile.get("parameters", {}).get("required_trends")
                        if isinstance(profile.get("parameters"), dict)
                        else profile.get("required_trends")
                    )
                }
            elif profile_type == "artifact_validation":
                normalized["canonical_projection"] = {
                    "required_artifacts": as_string_list(profile.get("required_artifacts"))
                }
            elif "canonical_answer" in answer:
                normalized["canonical_projection"] = answer.get("canonical_answer")
    normalized["document_binding"] = bool(
        normalized.get("document_binding")
        or normalized.get("document_target") is not None
        or any(
            is_document_binding_selector(
                field,
                artifacts,
                document_binding=bool(normalized.get("document_binding")),
            )
            for field in fields
        )
    )
    return normalized


def _schema_status_rank(status: str) -> int:
    return {"missing": 0, "open": 1, "present": 2}.get(status, 0)


def _resolve_local_schema_ref(schema: Any, root: Any, seen: set[str] | None = None) -> Any:
    """Resolve a local JSON-Schema ``$ref`` without fetching external files.

    Submission schemas are embedded JSON objects, so local JSON-Pointer refs are
    deterministic and safe to resolve here.  External refs remain opaque/open and
    are deliberately not fetched by the transport validator.
    """

    if not isinstance(schema, dict) or not isinstance(schema.get("$ref"), str):
        return schema
    reference = schema["$ref"]
    if not reference.startswith("#/"):
        return schema
    seen = set() if seen is None else set(seen)
    if reference in seen:
        return schema
    target: Any = root
    try:
        for segment in reference[2:].split("/"):
            segment = segment.replace("~1", "/").replace("~0", "~")
            if isinstance(target, dict):
                target = target[segment]
            elif isinstance(target, list) and segment.isdigit():
                target = target[int(segment)]
            else:
                return schema
    except (KeyError, IndexError, TypeError, ValueError):
        return schema
    if not isinstance(target, dict):
        return schema
    resolved = _resolve_local_schema_ref(target, root, seen | {reference})
    if not isinstance(resolved, dict):
        return schema
    merged = dict(resolved)
    merged.update({key: value for key, value in schema.items() if key != "$ref"})
    return merged


def _schema_step_schemas(
    schema: Any,
    token: str | int,
    *,
    root: Any = None,
) -> tuple[list[Any], bool]:
    """Resolve one JSON-Schema path token without interpreting scientific fields.

    The resolver intentionally supports only the structural keywords used by the
    benchmark submission contract.  ``patternProperties`` is evaluated alongside
    ``properties`` (an exact property wins), and multiple matching patterns are
    retained as alternatives.  The boolean indicates that the token was accepted
    through an open ``additionalProperties`` branch.
    """

    if root is None:
        root = schema
    schema = _resolve_local_schema_ref(schema, root)
    if not isinstance(schema, dict):
        return [], False
    if isinstance(token, int):
        items = schema.get("items")
        if isinstance(items, dict):
            return [items], False
        if isinstance(items, list) and 0 <= token < len(items):
            candidate = items[token]
            return ([candidate] if isinstance(candidate, dict) else []), False
        additional = schema.get("additionalItems")
        if isinstance(additional, dict):
            return [additional], False
        return ([], additional is True)
    if token == "*":
        items = schema.get("items")
        if isinstance(items, dict):
            return [items], False
        additional = schema.get("additionalProperties")
        if isinstance(additional, dict):
            return [additional], False
        return ([], additional is True or additional is None)

    properties = schema.get("properties")
    if isinstance(properties, dict) and token in properties:
        child = properties[token]
        return ([child] if isinstance(child, dict) else []), False

    patterns = schema.get("patternProperties")
    matched: list[Any] = []
    if isinstance(patterns, dict):
        for pattern, child in patterns.items():
            try:
                matches = re.search(str(pattern), token) is not None
            except re.error:
                matches = False
            if matches and isinstance(child, dict):
                matched.append(child)
    if matched:
        return matched, False

    # The pipeline's historical transport contract treats an explicit
    # ``properties``/``patternProperties`` map as closed unless the author
    # explicitly opts into additional properties.  This is stricter than the
    # JSON-Schema default and is retained for backwards-compatible diagnostics.
    additional = schema.get(
        "additionalProperties",
        True if not isinstance(properties, dict) and not isinstance(patterns, dict) else False,
    )
    if isinstance(additional, dict):
        return [additional], False
    if additional is True:
        return [], True
    return [], False


def schema_path_status(schema: Any, tokens: list[str | int]) -> str:
    """Return ``present``, ``open`` or ``missing`` for a JSON-Schema path.

    This is a transport-level check.  It does not validate a submitted value and
    does not infer any scientific meaning.  A path resolved by a declared
    ``properties``/``patternProperties`` schema is ``present``; a path accepted
    only through an open object is ``open``.
    """

    states: list[tuple[Any, bool]] = [(schema, False)]
    for token in tokens:
        next_states: list[tuple[Any, bool]] = []
        for current, was_open in states:
            children, open_branch = _schema_step_schemas(current, token, root=schema)
            if children:
                next_states.extend((child, was_open or open_branch) for child in children)
            elif open_branch:
                # There is no child schema to continue through.  The remainder of
                # the selector is therefore still open, but not explicitly declared.
                # An empty schema is the JSON-Schema representation of an
                # unconstrained/open child; retain it so later dotted selectors
                # remain ``open`` instead of being falsely reported missing.
                next_states.append(({}, True))
        if not next_states:
            return "missing"
        states = next_states
    statuses = ["open" if was_open else "present" for _, was_open in states]
    return max(statuses, key=_schema_status_rank) if statuses else "missing"


def _schema_path_status(schema: Any, tokens: list[str | int]) -> str:
    """Backward-compatible private alias for the shared resolver."""

    return schema_path_status(schema, tokens)


def materialize_result_schema_path(
    schema: dict[str, Any], selector: str, projection: Any = None
) -> bool:
    """Declare an already-bound structured path without copying its answer.

    This is a transport projection used when an audited binding walks through
    an intentionally open object.  It adds only property containers and a
    coarse JSON type inferred from the binding's projection; it never writes a
    target, enum, tolerance, or proposition into the public schema.
    """

    tokens = _jsonpath_tokens(selector)
    if tokens is None or is_safe_jsonpath_filter(selector):
        return False
    if _schema_path_status(schema, tokens) != "open":
        # A closed schema with a missing path is a real contract defect; do
        # not make it disappear through transport normalization.
        return False
    current: dict[str, Any] = schema
    for token in tokens:
        if token == "*" or isinstance(token, int):
            items = current.get("items")
            if not isinstance(items, dict):
                items = {"type": "object"}
                current["items"] = items
            current = items
            continue
        properties = current.get("properties")
        if not isinstance(properties, dict):
            # Preserve the source schema's intentional openness while making
            # this one already-bound child explicit.  Without this marker a
            # second sibling under the same open object would look falsely
            # missing after the first child is materialized.
            if "additionalProperties" not in current:
                current["additionalProperties"] = True
            properties = {}
            current["properties"] = properties
        child = properties.get(token)
        if not isinstance(child, dict):
            child = {}
            properties[token] = child
        current = child
    if "type" not in current:
        if isinstance(projection, bool):
            current["type"] = "boolean"
        elif isinstance(projection, (int, float)) and not isinstance(projection, bool):
            current["type"] = "number"
        elif isinstance(projection, list):
            current["type"] = "array"
        elif isinstance(projection, str):
            current["type"] = "string"
        else:
            current["type"] = "object"
    return True


def _binding_schema_findings(
    *,
    submission: SubmissionSchemaV1,
    reference: ComputationalScienceReferenceV1,
    diagnostics: list[str] | None = None,
) -> list[str]:
    findings: list[str] = []
    diagnostics = diagnostics if diagnostics is not None else []
    required_files = set(submission.required_files)
    for binding in reference.submission_bindings:
        for artifact in binding.artifact_paths:
            if artifact not in required_files:
                findings.append(
                    f"binding_artifact_not_required:{binding.binding_id}:{artifact}"
                )
        document_fields = {
            field
            for field in binding.observed_fields
            if is_document_binding_selector(
                field,
                binding.artifact_paths,
                document_binding=binding.document_binding,
            )
        }
        # A mixed binding may contain both a report/document selector and
        # structured result selectors.  Skip only the document selectors; keep
        # validating the structured paths.
        if not submission.primary_result_file:
            if len(document_fields) != len(binding.observed_fields):
                findings.append(
                    f"structured_binding_without_primary_result:{binding.binding_id}"
                )
        elif submission.primary_result_file not in binding.artifact_paths and not document_fields:
            findings.append(
                f"structured_binding_wrong_artifact:{binding.binding_id}"
            )
        for observed in binding.observed_fields:
            if observed in document_fields:
                continue
            if is_safe_jsonpath_filter(observed):
                diagnostics.append(
                    f"binding_filter_selector_unchecked:{binding.binding_id}:{observed}"
                )
                continue
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
        split_root = root / "evaluation"
        if (split_root / "reference.json").exists():
            findings.append("legacy_reference_file_forbidden")

        split_files = {
            "reference_key_points.json": True,
            "reference_conclusions.json": True,
            "scoring_rules.json": True,
            "evidence_map.json": True,
            "critical_failures.json": True,
        }
        split_root = root / "evaluation"
        for name, required in split_files.items():
            path = split_root / name
            if not path.is_file():
                if required:
                    findings.append(f"split_reference_file_missing:{name}")
                continue
            try:
                value = _read_json(path)
            except Exception as exc:
                findings.append(f"split_reference_invalid_json:{name}:{type(exc).__name__}")
                continue
            if not isinstance(value, dict):
                findings.append(f"split_reference_not_object:{name}")
                continue
            if name == "reference_key_points.json":
                items = value.get("items")
                if not isinstance(items, list) or not items:
                    findings.append("split_reference_key_points_empty")
            elif name == "reference_conclusions.json":
                items = value.get("items")
                if not isinstance(items, list) or not any(
                    isinstance(item, dict)
                    and str(item.get("claim_role") or "").casefold() == "final"
                    for item in (items or [])
                ):
                    findings.append("split_reference_final_conclusion_missing")
            elif name == "scoring_rules.json":
                if not isinstance(value.get("rules"), list):
                    diagnostics.append("split_scoring_rules_not_array")

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
