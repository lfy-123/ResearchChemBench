"""Pydantic schemas for ResearchChemBench tasks and ground truth."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class DataFile(BaseModel):
    name: str
    path: str
    type: str = ""
    description: str = ""


class TaskInfo(BaseModel):
    task_id: str
    source_id: str
    category: str
    task: str
    data: list[DataFile] = Field(default_factory=list)


class GroundTruth(BaseModel):
    expected_tool_calls: list[dict[str, Any]] = Field(default_factory=list)
    expected_result: Any = ""
    expected_structured_output: dict[str, Any] | None = None

