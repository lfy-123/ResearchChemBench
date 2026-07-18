"""Typed contracts shared by actions, backends, transports, and traces."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field
from typing import Any, Literal, Mapping

from pydantic import BaseModel, ConfigDict, Field, field_validator


_ID_PATTERN = re.compile(r"^[a-z][a-z0-9_]*$")
ActionStatus = Literal[
    "success",
    "partial_success",
    "invalid_request",
    "unsupported",
    "unavailable",
    "failed",
    "timeout",
    "cancelled",
]


class ResourceLimits(BaseModel):
    """Mechanical execution limits; these do not choose scientific settings."""

    model_config = ConfigDict(extra="forbid")

    walltime_seconds: int = Field(default=1800, ge=1, le=172800)
    memory_mb: int | None = Field(default=None, ge=128)
    cpu_cores: int | None = Field(default=None, ge=1)
    gpu_count: int | None = Field(default=None, ge=0)


class ActionRequest(BaseModel):
    """Uniform request supplied to every public Scientific/Data Action."""

    model_config = ConfigDict(extra="forbid")

    backend_id: str | None = Field(
        default=None,
        description=(
            "Exact backend selected by the agent. Required for every Scientific "
            "Action; data actions use their fixed named data source."
        ),
    )
    inputs: dict[str, Any] = Field(
        default_factory=dict,
        description="Structured chemistry objects, values, or ArtifactRef objects.",
    )
    method_spec: dict[str, Any] = Field(
        default_factory=dict,
        description=(
            "Agent-selected theory, functional, basis, model, force field, charge "
            "model, or equivalent scientific method settings."
        ),
    )
    action_settings: dict[str, Any] = Field(
        default_factory=dict,
        description=(
            "Parameters belonging only to this atomic action, such as constraints, "
            "convergence thresholds, thermodynamic state, or search space."
        ),
    )
    resource_limits: ResourceLimits = Field(default_factory=ResourceLimits)

    @field_validator("backend_id")
    @classmethod
    def validate_backend_id(cls, value: str | None) -> str | None:
        if value is None:
            return None
        normalized = value.strip()
        if not normalized:
            raise ValueError("backend_id cannot be empty")
        if normalized == "auto":
            raise ValueError("backend_id='auto' is forbidden in the benchmark")
        if not _ID_PATTERN.fullmatch(normalized):
            raise ValueError("backend_id must use lower_snake_case")
        return normalized


class ArtifactRef(BaseModel):
    """Stable semantic reference passed between atomic actions."""

    model_config = ConfigDict(extra="forbid")

    artifact_id: str
    semantic_type: str
    media_type: str
    sha256: str
    path: str
    producer_action: str
    producer_backend: str | None = None
    parent_artifact_ids: list[str] = Field(default_factory=list)


class ActionResult(BaseModel):
    """Canonical result envelope returned by every public action."""

    model_config = ConfigDict(extra="forbid")

    status: ActionStatus
    action: str
    action_version: str
    requested_backend: str | None
    backend: str | None
    backend_version: str | None = None
    selection_source: Literal["agent", "task_constraint", "fixed_data_source"]
    result: Any = None
    input_artifacts: list[ArtifactRef] = Field(default_factory=list)
    output_artifacts: list[ArtifactRef] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)
    provenance: dict[str, Any] = Field(default_factory=dict)
    error: dict[str, Any] | None = None
    retryable: bool = False


@dataclass(frozen=True)
class ActionSpec:
    """One public action with one primary scientific result."""

    id: str
    category: str
    description: str
    primary_output: str
    backend_ids: tuple[str, ...]
    required_inputs: tuple[str, ...] = ()
    optional_inputs: tuple[str, ...] = ()
    input_description: str = ""
    version: str = "1.0.0"
    data_action: bool = False
    requires_network: bool = False

    def validate(self) -> None:
        if not _ID_PATTERN.fullmatch(self.id):
            raise ValueError(f"Invalid action id: {self.id!r}")
        if self.id.startswith("run_"):
            raise ValueError(f"Software runner cannot be a public action: {self.id}")
        if not self.category.strip() or not self.description.strip():
            raise ValueError(f"Action {self.id} requires category and description")
        if not self.primary_output.strip():
            raise ValueError(f"Action {self.id} requires one primary output")
        if not self.data_action and not self.backend_ids:
            raise ValueError(f"Scientific Action {self.id} requires backend choices")
        if "auto" in self.backend_ids:
            raise ValueError(f"Action {self.id} cannot advertise auto backend")
        if len(self.backend_ids) != len(set(self.backend_ids)):
            raise ValueError(f"Action {self.id} contains duplicate backend ids")
        for name in (*self.required_inputs, *self.optional_inputs):
            if not _ID_PATTERN.fullmatch(name):
                raise ValueError(f"Action {self.id} has invalid input key {name!r}")
        if set(self.required_inputs) & set(self.optional_inputs):
            raise ValueError(f"Action {self.id} repeats required/optional inputs")

    def as_dict(self) -> dict[str, Any]:
        value = asdict(self)
        for key in ("backend_ids", "required_inputs", "optional_inputs"):
            value[key] = list(value[key])
        return value


@dataclass(frozen=True)
class BackendSpec:
    """Objective capability/install metadata for one agent-selectable backend."""

    id: str
    display_name: str
    runtime: str
    capabilities: tuple[str, ...]
    description: str
    python_modules: tuple[str, ...] = ()
    executables: tuple[str, ...] = ()
    environment_variables: tuple[str, ...] = ()
    conda_packages: tuple[str, ...] = ()
    pip_packages: tuple[str, ...] = ()
    required_data_resources: tuple[str, ...] = ()
    license_class: str = "open_source"
    install_notes: str = ""
    method_schema: Mapping[str, str] = field(default_factory=dict)
    required_method_fields: Mapping[str, tuple[str, ...]] = field(default_factory=dict)
    required_setting_fields: Mapping[str, tuple[str, ...]] = field(default_factory=dict)

    def validate(self) -> None:
        if not _ID_PATTERN.fullmatch(self.id) or self.id == "auto":
            raise ValueError(f"Invalid backend id: {self.id!r}")
        if not self.display_name.strip() or not self.runtime.strip():
            raise ValueError(f"Backend {self.id} requires display_name and runtime")
        if not self.capabilities:
            raise ValueError(f"Backend {self.id} must declare capabilities")
        if len(self.capabilities) != len(set(self.capabilities)):
            raise ValueError(f"Backend {self.id} repeats capabilities")
        for mapping in (self.required_method_fields, self.required_setting_fields):
            for action_id, fields in mapping.items():
                if action_id not in self.capabilities:
                    raise ValueError(
                        f"Backend {self.id} declares fields for unsupported {action_id}"
                    )
                if len(fields) != len(set(fields)):
                    raise ValueError(
                        f"Backend {self.id}/{action_id} repeats required fields"
                    )

    def as_dict(self) -> dict[str, Any]:
        value = asdict(self)
        for key in (
            "capabilities",
            "python_modules",
            "executables",
            "environment_variables",
            "conda_packages",
            "pip_packages",
            "required_data_resources",
        ):
            value[key] = list(value[key])
        value["method_schema"] = dict(self.method_schema)
        value["required_method_fields"] = {
            key: list(fields) for key, fields in self.required_method_fields.items()
        }
        value["required_setting_fields"] = {
            key: list(fields) for key, fields in self.required_setting_fields.items()
        }
        return value
