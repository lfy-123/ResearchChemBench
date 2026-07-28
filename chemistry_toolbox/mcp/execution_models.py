"""Typed MCP contracts for software-native and programmable execution layers."""

from __future__ import annotations

import re
from pathlib import PurePosixPath
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from researchchem_toolbox.models import ResourceLimits


_SOFTWARE_ID = re.compile(r"^[a-z][a-z0-9_]*$")
_JOB_ID = re.compile(r"^job_[0-9a-f]{32}$")
_RUNTIME_ID = re.compile(r"^[a-z][a-z0-9_]*$")
_JOB_CONTROL_FILES = {
    "analysis_contract.json",
    "artifact_manifest.json",
    "request.json",
    "status.json",
    "supervisor_spec.json",
    "collection.json",
    "stdout.log",
    "stderr.log",
    "researchchem_job.py",
}


def _validate_relative_target(value: str) -> str:
    normalized = value.strip().replace("\\", "/")
    path = PurePosixPath(normalized)
    if not normalized or path.is_absolute() or ".." in path.parts:
        raise ValueError("staged target must be a non-empty relative path without '..'")
    if any(part in {"", "."} for part in path.parts):
        raise ValueError("staged target contains an invalid path component")
    if path.parts[0] in {".tmp", ".home"} or str(path) in _JOB_CONTROL_FILES:
        raise ValueError("staged target conflicts with an execution job control path")
    return str(path)


class SoftwareListRequest(BaseModel):
    """Filter the installed/documented software inventory without selecting for the Agent."""

    model_config = ConfigDict(extra="forbid")

    query: str | None = Field(default=None, max_length=200)
    native_only: bool = False
    available_only: bool = False
    offset: int = Field(default=0, ge=0)
    limit: int = Field(default=50, ge=1, le=200)


class SoftwareInspectRequest(BaseModel):
    """Request the exact local capabilities and invocation guide for one software id."""

    model_config = ConfigDict(extra="forbid")

    software_id: str

    @field_validator("software_id")
    @classmethod
    def validate_software_id(cls, value: str) -> str:
        normalized = value.strip().lower().replace("-", "_")
        if not _SOFTWARE_ID.fullmatch(normalized):
            raise ValueError("software_id must use lower_snake_case")
        return normalized


class DocumentationSearchRequest(SoftwareInspectRequest):
    """Route to or search bounded sections of local software documentation."""

    query: str | None = Field(default=None, min_length=2, max_length=200)
    topic: str | None = Field(default=None, min_length=2, max_length=100)
    section: str | None = Field(default=None, min_length=1, max_length=200)
    retrieval_mode: Literal["lexical", "hybrid"] = "hybrid"
    max_results: int = Field(default=10, ge=1, le=50)
    context_chars: int = Field(default=500, ge=100, le=4000)

    @model_validator(mode="after")
    def require_route_or_query(self) -> "DocumentationSearchRequest":
        if not any((self.query, self.topic, self.section)):
            raise ValueError("provide query, topic, or section")
        return self


class DocumentationReadRequest(SoftwareInspectRequest):
    """Read exact first-party documentation selected by topic and optional section."""

    topic: str = Field(min_length=2, max_length=100)
    section: str | None = Field(default=None, min_length=1, max_length=200)
    max_chars: int = Field(default=12_000, ge=200, le=100_000)


class WorkspaceTextWriteRequest(BaseModel):
    """Write an auditable text input deck or program under code/ or outputs/."""

    model_config = ConfigDict(extra="forbid")

    path: str = Field(min_length=1, max_length=1000)
    content: str = Field(max_length=10_000_000)
    overwrite: bool = False


class WorkspaceTextReadRequest(BaseModel):
    """Read an existing UTF-8 workspace file with an explicit output limit."""

    model_config = ConfigDict(extra="forbid")

    path: str = Field(min_length=1, max_length=1000)
    max_chars: int = Field(default=100_000, ge=1, le=2_000_000)


class StagedInput(BaseModel):
    """Explicit mapping from an existing workspace file to a native job filename."""

    model_config = ConfigDict(extra="forbid")

    source_path: str = Field(min_length=1, max_length=1000)
    target_path: str = Field(min_length=1, max_length=1000)

    @field_validator("target_path")
    @classmethod
    def validate_target_path(cls, value: str) -> str:
        return _validate_relative_target(value)


class AnalysisInputDeclaration(BaseModel):
    """One named programmable-job input staged under inputs/."""

    model_config = ConfigDict(extra="forbid")

    name: str
    source_path: str = Field(min_length=1, max_length=1000)
    semantic_type: str = Field(default="InputFile", min_length=1, max_length=200)
    target_path: str | None = Field(default=None, max_length=1000)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        return _catalog_name(value, field_name="input name")

    @model_validator(mode="after")
    def set_target_path(self) -> "AnalysisInputDeclaration":
        suffix = PurePosixPath(self.source_path.replace("\\", "/")).suffix
        target = self.target_path or f"inputs/{self.name}{suffix}"
        normalized = _validate_relative_target(target)
        if PurePosixPath(normalized).parts[0] != "inputs":
            raise ValueError("analysis input target_path must be under inputs/")
        self.target_path = normalized
        return self


class AnalysisOutputDeclaration(BaseModel):
    """One named expected output and its mechanical validation contract."""

    model_config = ConfigDict(extra="forbid")

    name: str
    path: str = Field(min_length=1, max_length=1000)
    semantic_type: str = Field(min_length=1, max_length=200)
    media_type: str = Field(default="application/octet-stream", min_length=1, max_length=200)
    required: bool = True
    json_schema: dict | None = None
    parent_artifact_ids: list[str] = Field(default_factory=list, max_length=1000)

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        return _catalog_name(value, field_name="output name")

    @field_validator("path")
    @classmethod
    def validate_path(cls, value: str) -> str:
        normalized = _validate_relative_target(value)
        if PurePosixPath(normalized).parts[0] not in {"outputs", "report", "logs"}:
            raise ValueError("analysis output path must be under outputs/, report/, or logs/")
        return normalized


def _catalog_name(value: str, *, field_name: str) -> str:
    normalized = value.strip().lower().replace("-", "_")
    if not _SOFTWARE_ID.fullmatch(normalized):
        raise ValueError(f"{field_name} must use lower_snake_case")
    return normalized


class NativeJobRequest(BaseModel):
    """A complete, exact native program invocation authored by the Agent."""

    model_config = ConfigDict(extra="forbid")

    software_id: str
    executable: str = Field(min_length=1, max_length=200)
    arguments: list[str] = Field(default_factory=list, max_length=500)
    staged_inputs: list[StagedInput] = Field(default_factory=list, max_length=1000)
    stdin_target: str | None = Field(default=None, max_length=1000)
    resource_limits: ResourceLimits = Field(default_factory=ResourceLimits)
    label: str | None = Field(default=None, max_length=200)
    parent_job_id: str | None = None

    @field_validator("software_id")
    @classmethod
    def validate_software_id(cls, value: str) -> str:
        normalized = value.strip().lower().replace("-", "_")
        if not _SOFTWARE_ID.fullmatch(normalized):
            raise ValueError("software_id must use lower_snake_case")
        return normalized

    @field_validator("executable")
    @classmethod
    def validate_executable(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized or "/" in normalized or "\\" in normalized or "\x00" in normalized:
            raise ValueError("executable must be the configured command name, not a path")
        return normalized

    @field_validator("arguments")
    @classmethod
    def validate_arguments(cls, values: list[str]) -> list[str]:
        normalized: list[str] = []
        for value in values:
            if "\x00" in value or len(value) > 8192:
                raise ValueError("arguments cannot contain NUL bytes or exceed 8192 characters")
            normalized.append(value)
        return normalized

    @field_validator("stdin_target")
    @classmethod
    def validate_stdin_target(cls, value: str | None) -> str | None:
        return _validate_relative_target(value) if value is not None else None

    @field_validator("parent_job_id")
    @classmethod
    def validate_parent_job_id(cls, value: str | None) -> str | None:
        if value is not None and not _JOB_ID.fullmatch(value):
            raise ValueError("invalid parent_job_id")
        return value

    @model_validator(mode="after")
    def validate_staging(self) -> "NativeJobRequest":
        targets = [item.target_path for item in self.staged_inputs]
        if len(targets) != len(set(targets)):
            raise ValueError("staged_inputs contains duplicate target_path values")
        if self.stdin_target is not None and self.stdin_target not in set(targets):
            raise ValueError("stdin_target must name one of the explicitly staged target files")
        return self


class AnalysisJobRequest(BaseModel):
    """Run an Agent-authored Python file in one exact configured chemistry runtime."""

    model_config = ConfigDict(extra="forbid")

    runtime: str
    script_path: str = Field(min_length=1, max_length=1000)
    script_target: str = Field(default="code/agent_program.py", min_length=1, max_length=1000)
    arguments: list[str] = Field(default_factory=list, max_length=500)
    staged_inputs: list[StagedInput] = Field(default_factory=list, max_length=1000)
    required_modules: list[str] = Field(default_factory=list, max_length=500)
    inputs: list[AnalysisInputDeclaration] = Field(default_factory=list, max_length=1000)
    outputs: list[AnalysisOutputDeclaration] = Field(default_factory=list, max_length=1000)
    execution_policy: Literal["in_process_only"] = "in_process_only"
    external_execution: Literal["native_job_runner_only"] = "native_job_runner_only"
    resource_limits: ResourceLimits = Field(default_factory=ResourceLimits)
    label: str | None = Field(default=None, max_length=200)
    parent_job_id: str | None = None

    @field_validator("runtime")
    @classmethod
    def validate_runtime(cls, value: str) -> str:
        normalized = value.strip().lower()
        if not _RUNTIME_ID.fullmatch(normalized):
            raise ValueError("runtime must use lower_snake_case")
        return normalized

    @field_validator("script_target")
    @classmethod
    def validate_script_target(cls, value: str) -> str:
        normalized = _validate_relative_target(value)
        if not normalized.endswith(".py"):
            raise ValueError("script_target must end in .py")
        return normalized

    @field_validator("arguments")
    @classmethod
    def validate_arguments(cls, values: list[str]) -> list[str]:
        for value in values:
            if "\x00" in value or len(value) > 8192:
                raise ValueError("arguments cannot contain NUL bytes or exceed 8192 characters")
        return values

    @field_validator("required_modules")
    @classmethod
    def validate_required_modules(cls, values: list[str]) -> list[str]:
        normalized = []
        for value in values:
            name = value.strip()
            if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_.]*", name):
                raise ValueError(f"invalid Python module name: {value!r}")
            normalized.append(name)
        if len(normalized) != len(set(normalized)):
            raise ValueError("required_modules contains duplicates")
        return normalized

    @field_validator("parent_job_id")
    @classmethod
    def validate_parent_job_id(cls, value: str | None) -> str | None:
        if value is not None and not _JOB_ID.fullmatch(value):
            raise ValueError("invalid parent_job_id")
        return value

    @model_validator(mode="after")
    def validate_staging(self) -> "AnalysisJobRequest":
        targets = [item.target_path for item in self.staged_inputs] + [
            str(item.target_path) for item in self.inputs
        ]
        if self.script_target in targets or len(targets) != len(set(targets)):
            raise ValueError("script_target and all staged input targets must be unique")
        input_names = [item.name for item in self.inputs]
        output_names = [item.name for item in self.outputs]
        output_paths = [item.path for item in self.outputs]
        if len(input_names) != len(set(input_names)):
            raise ValueError("analysis inputs contain duplicate names")
        if len(output_names) != len(set(output_names)):
            raise ValueError("analysis outputs contain duplicate names")
        if len(output_paths) != len(set(output_paths)):
            raise ValueError("analysis outputs contain duplicate paths")
        return self


class AnalysisRuntimeListRequest(BaseModel):
    """List exact Python environments available to the programmable layer."""

    model_config = ConfigDict(extra="forbid")

    available_only: bool = True
    query: str | None = Field(default=None, max_length=200)
    runtime: str | None = None
    include_details: bool = False
    limit: int = Field(default=100, ge=1, le=500)

    @field_validator("runtime")
    @classmethod
    def validate_optional_runtime(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip().lower()
        if not _RUNTIME_ID.fullmatch(normalized):
            raise ValueError("runtime must use lower_snake_case")
        return normalized


class JobStatusRequest(BaseModel):
    """Read persistent state and bounded log tails for one submitted job."""

    model_config = ConfigDict(extra="forbid")

    job_id: str
    tail_chars: int = Field(default=8000, ge=0, le=100_000)

    @field_validator("job_id")
    @classmethod
    def validate_job_id(cls, value: str) -> str:
        if not _JOB_ID.fullmatch(value):
            raise ValueError("invalid job_id")
        return value


class JobCollectRequest(JobStatusRequest):
    """Collect a completed job manifest and output hashes without interpreting science."""

    include_inputs: bool = False
    max_files: int = Field(default=1000, ge=1, le=10_000)


class JobCancelRequest(BaseModel):
    """Request cancellation of one running native or programmable job."""

    model_config = ConfigDict(extra="forbid")

    job_id: str

    @field_validator("job_id")
    @classmethod
    def validate_job_id(cls, value: str) -> str:
        if not _JOB_ID.fullmatch(value):
            raise ValueError("invalid job_id")
        return value


class ArtifactDeclarationRequest(BaseModel):
    """Attach scientific semantics and lineage to an existing workspace file."""

    model_config = ConfigDict(extra="forbid")

    path: str = Field(min_length=1, max_length=1000)
    semantic_type: str = Field(min_length=1, max_length=200)
    media_type: str = Field(default="application/octet-stream", min_length=1, max_length=200)
    producer_layer: Literal["native_software", "programmable_analysis", "external_input"]
    producer_id: str = Field(min_length=1, max_length=200)
    parent_artifact_ids: list[str] = Field(default_factory=list, max_length=1000)


__all__ = [
    "AnalysisInputDeclaration",
    "AnalysisJobRequest",
    "AnalysisOutputDeclaration",
    "AnalysisRuntimeListRequest",
    "ArtifactDeclarationRequest",
    "DocumentationReadRequest",
    "DocumentationSearchRequest",
    "JobCancelRequest",
    "JobCollectRequest",
    "JobStatusRequest",
    "NativeJobRequest",
    "SoftwareInspectRequest",
    "SoftwareListRequest",
    "StagedInput",
    "WorkspaceTextReadRequest",
    "WorkspaceTextWriteRequest",
]
