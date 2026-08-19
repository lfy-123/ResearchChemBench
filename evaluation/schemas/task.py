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


class RequiredDeliverable(BaseModel):
    """One task-specific evidence product written inside the run workspace."""

    path: str
    description: str = ""
    allow_empty: bool = False

    @field_validator("path")
    @classmethod
    def relative_deliverable_path(cls, value: str) -> str:
        path = PurePosixPath(value)
        if (
            not value
            or path.is_absolute()
            or ".." in path.parts
            or "\\" in value
            or "\x00" in value
        ):
            raise ValueError("deliverable paths must be safe non-empty relative POSIX paths")
        return value


class TaskInfo(BaseModel):
    task_id: str
    source_id: str
    category: str
    scientific_mode: str = "standard_autonomous_investigation"
    scientific_mode_description: str = ""
    scientific_requirements: list[str] = Field(default_factory=list)
    required_deliverables: list[RequiredDeliverable] = Field(default_factory=list)
    data: list[DataFile] = Field(default_factory=list)
    archive_extractions: list[ArchiveExtraction] = Field(default_factory=list)
    benchmark_family: str = ""
    task_mode: Literal["", "open_discovery", "guided_reproduction"] = ""
    method_disclosure: str = ""
    pathway_disclosure: str = ""


class GroundTruth(BaseModel):
    expected_tool_calls: list[dict[str, Any]] = Field(default_factory=list)
    expected_result: Any = ""
    expected_structured_output: Any = None
    evaluation_mode: Literal["binary", "rubric_100", "dual_axis_100"] = "binary"
    evaluation_profile: Literal[
        "", "autonomous_discovery", "paper_reproduction"
    ] = ""
    score_max: int = 1
    scoring_rubric: list[dict[str, Any]] = Field(default_factory=list)
    scientific_conclusion_rubric: list[dict[str, Any]] = Field(default_factory=list)
    dual_axis_scoring_policy: dict[str, Any] = Field(default_factory=dict)
    critical_failures: list[str] = Field(default_factory=list)
    judge_instructions: str = ""
    reference_evidence: Any = None
    managed_computation_policy: dict[str, Any] = Field(default_factory=dict)
    evidence_gate_policy: dict[str, Any] = Field(default_factory=dict)
    reference_conclusion_gate_policy: dict[str, Any] = Field(default_factory=dict)
    current_toolbox_feasibility_baseline: dict[str, Any] = Field(default_factory=dict)
    current_toolbox_reproduction_baseline: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def validate_scoring_definition(self) -> "GroundTruth":
        if self.evaluation_mode == "binary":
            if self.score_max != 1:
                raise ValueError("binary evaluation requires score_max=1")
            return self
        if self.score_max != 100:
            raise ValueError("100-point evaluation modes require score_max=100")
        if not self.scoring_rubric:
            raise ValueError("100-point evaluation modes require a non-empty scoring_rubric")
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
        if self.evaluation_mode == "dual_axis_100":
            if not self.scientific_conclusion_rubric:
                raise ValueError(
                    "dual_axis_100 requires a non-empty scientific_conclusion_rubric"
                )
            claim_ids: list[str] = []
            claim_total = 0.0
            for claim in self.scientific_conclusion_rubric:
                claim_id = str(claim.get("id") or "").strip()
                maximum = float(claim.get("max_score") or 0)
                statement = str(claim.get("statement") or "").strip()
                acceptance_rule = str(claim.get("acceptance_rule") or "").strip()
                required_evidence = claim.get("required_evidence")
                if (
                    not claim_id
                    or not statement
                    or not acceptance_rule
                    or maximum <= 0
                    or not isinstance(required_evidence, list)
                    or not required_evidence
                ):
                    raise ValueError(
                        "each scientific conclusion requires id, statement, acceptance_rule, "
                        "non-empty required_evidence, and positive max_score"
                    )
                claim_ids.append(claim_id)
                claim_total += maximum
            if len(claim_ids) != len(set(claim_ids)):
                raise ValueError("scientific conclusion ids must be unique")
            if abs(claim_total - 100.0) > 1e-9:
                raise ValueError(
                    "scientific conclusion max_score values must sum to 100"
                )
            formula = str(
                self.dual_axis_scoring_policy.get("formula") or ""
            ).strip()
            if formula != "scientific_conclusion_score * research_process_score / 100":
                raise ValueError(
                    "dual_axis_100 requires the standard multiplicative formula"
                )
        gates = self.evidence_gate_policy.get("gates", [])
        if gates:
            gate_ids: list[str] = []
            for gate in gates:
                gate_id = str(gate.get("id") or "").strip()
                cap = float(gate.get("score_cap_if_failed", -1))
                if not gate_id or cap < 0 or cap > self.score_max:
                    raise ValueError(
                        "each evidence gate requires an id and a score cap within score_max"
                    )
                gate_ids.append(gate_id)
            if len(gate_ids) != len(set(gate_ids)):
                raise ValueError("evidence gate ids must be unique")
        conclusion_policy = self.reference_conclusion_gate_policy
        if conclusion_policy:
            criterion_id = str(
                conclusion_policy.get("criterion_id") or ""
            ).strip()
            if conclusion_policy.get("required") is True and not criterion_id:
                raise ValueError(
                    "a required reference-conclusion gate needs criterion_id"
                )
            if criterion_id and criterion_id not in criterion_ids:
                raise ValueError(
                    "reference-conclusion criterion_id must exist in scoring_rubric"
                )
            for field_name in (
                "score_cap_if_not_matched",
                "score_cap_if_uncertain",
                "score_cap_if_omitted",
                "max_criterion_score_if_not_matched",
                "max_criterion_score_if_uncertain",
                "max_criterion_score_if_omitted",
            ):
                if field_name not in conclusion_policy:
                    continue
                value = float(conclusion_policy[field_name])
                if value < 0 or value > self.score_max:
                    raise ValueError(
                        f"{field_name} must be between zero and score_max"
                    )
        return self
