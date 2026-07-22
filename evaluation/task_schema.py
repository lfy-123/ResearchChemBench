"""Pydantic schemas for ResearchChemBench tasks and ground truth."""

from __future__ import annotations

from pathlib import PurePosixPath
from typing import Any, Literal

from pydantic import BaseModel, Field, field_validator, model_validator


class DataFile(BaseModel):
    name: str
    path: str
    type: str = ""
    description: str = ""


class ArchiveExtraction(BaseModel):
    """One trusted task-data archive expanded inside the run workspace."""

    source: str
    destination: str
    format: Literal["zip"] = "zip"
    sha256: str = ""

    @field_validator("source", "destination")
    @classmethod
    def relative_archive_path(cls, value: str) -> str:
        path = PurePosixPath(value)
        if (
            not value
            or path.is_absolute()
            or ".." in path.parts
            or "\\" in value
            or "\x00" in value
        ):
            raise ValueError("archive paths must be safe non-empty relative POSIX paths")
        return value

    @field_validator("sha256")
    @classmethod
    def valid_sha256(cls, value: str) -> str:
        normalized = value.strip().casefold()
        if normalized and (
            len(normalized) != 64
            or any(character not in "0123456789abcdef" for character in normalized)
        ):
            raise ValueError("sha256 must be an empty string or 64 hexadecimal characters")
        return normalized


class TaskInfo(BaseModel):
    task_id: str
    source_id: str
    category: str
    task: str
    data: list[DataFile] = Field(default_factory=list)
    archive_extractions: list[ArchiveExtraction] = Field(default_factory=list)


class GroundTruth(BaseModel):
    expected_tool_calls: list[dict[str, Any]] = Field(default_factory=list)
    expected_result: Any = ""
    expected_structured_output: dict[str, Any] | None = None
    evaluation_mode: Literal["binary", "rubric_100"] = "binary"
    score_max: int = 1
    scoring_rubric: list[dict[str, Any]] = Field(default_factory=list)
    critical_failures: list[str] = Field(default_factory=list)
    judge_instructions: str = ""
    reference_evidence: Any = None
    managed_computation_policy: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_scoring_definition(self) -> "GroundTruth":
        if self.evaluation_mode == "binary":
            if self.score_max != 1:
                raise ValueError("binary evaluation requires score_max=1")
            return self
        if self.score_max != 100:
            raise ValueError("rubric_100 evaluation requires score_max=100")
        if not self.scoring_rubric:
            raise ValueError("rubric_100 evaluation requires a non-empty scoring_rubric")
        criterion_ids: list[str] = []
        maximum_total = 0.0
        for criterion in self.scoring_rubric:
            criterion_id = str(criterion.get("id") or "").strip()
            maximum = float(criterion.get("max_score") or 0)
            if not criterion_id or maximum <= 0:
                raise ValueError("each rubric criterion requires an id and positive max_score")
            criterion_ids.append(criterion_id)
            maximum_total += maximum
        if len(criterion_ids) != len(set(criterion_ids)):
            raise ValueError("rubric criterion ids must be unique")
        if abs(maximum_total - self.score_max) > 1e-9:
            raise ValueError("rubric max_score values must sum to score_max")
        return self
