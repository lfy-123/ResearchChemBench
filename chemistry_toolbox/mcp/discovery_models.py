"""Typed MCP requests for progressive catalog discovery and Action execution."""

from __future__ import annotations

import re
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from researchchem_toolbox.models import ActionRequest


_CATALOG_ID = re.compile(r"^[a-z][a-z0-9_]*$")


def _catalog_id(value: str, *, field_name: str) -> str:
    normalized = value.strip().lower().replace("-", "_")
    if not _CATALOG_ID.fullmatch(normalized):
        raise ValueError(f"{field_name} must use lower_snake_case")
    return normalized


class ActionDomainListRequest(BaseModel):
    """Return the complete compact Action-domain index."""

    model_config = ConfigDict(extra="forbid")

    include_action_ids: bool = Field(
        default=True,
        description=(
            "Include every exact action_id grouped by domain. Disable only when counts alone are needed."
        ),
    )


class ActionSearchRequest(BaseModel):
    """Search and relevance-rank the complete Action catalog."""

    model_config = ConfigDict(extra="forbid")

    query: str | None = Field(default=None, max_length=300)
    category: str | None = None
    backend_id: str | None = None
    action_kind: Literal["all", "scientific", "data"] = "all"
    retrieval_mode: Literal["lexical", "hybrid"] = "hybrid"
    available_only: bool = False
    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0, le=100_000)

    @field_validator("category", "backend_id")
    @classmethod
    def validate_optional_ids(cls, value: str | None, info) -> str | None:
        return _catalog_id(value, field_name=info.field_name) if value is not None else None


class ActionCategoryBrowseRequest(BaseModel):
    """Return every compact Action summary in one exact category."""

    model_config = ConfigDict(extra="forbid")

    category: str
    action_kind: Literal["all", "scientific", "data"] = "all"
    available_only: bool = False

    @field_validator("category")
    @classmethod
    def validate_category(cls, value: str) -> str:
        return _catalog_id(value, field_name="category")


class ActionInspectRequest(BaseModel):
    """Inspect one exact Action, optionally scoped to one exact provider."""

    model_config = ConfigDict(extra="forbid")

    action_id: str
    backend_id: str | None = None

    @field_validator("action_id", "backend_id")
    @classmethod
    def validate_ids(cls, value: str | None, info) -> str | None:
        return _catalog_id(value, field_name=info.field_name) if value is not None else None


class BackendInspectRequest(BaseModel):
    """Inspect one exact Backend and its complete Action capability list."""

    model_config = ConfigDict(extra="forbid")

    backend_id: str
    action_id: str | None = None

    @field_validator("backend_id", "action_id")
    @classmethod
    def validate_ids(cls, value: str | None, info) -> str | None:
        return _catalog_id(value, field_name=info.field_name) if value is not None else None


class ResourceSearchRequest(BaseModel):
    """Apply Agent-supplied filters to all registered scientific resources."""

    model_config = ConfigDict(extra="forbid")

    query: str | None = Field(default=None, max_length=300)
    backend_id: str | None = None
    available_only: bool = False
    limit: int = Field(default=20, ge=1, le=100)
    offset: int = Field(default=0, ge=0, le=100_000)

    @field_validator("backend_id")
    @classmethod
    def validate_backend_id(cls, value: str | None) -> str | None:
        return _catalog_id(value, field_name="backend_id") if value is not None else None


class ResourceInspectRequest(BaseModel):
    """Resolve one exact registered resource and its selection contract."""

    model_config = ConfigDict(extra="forbid")

    resource_id: str

    @field_validator("resource_id")
    @classmethod
    def validate_resource_id(cls, value: str) -> str:
        return _catalog_id(value, field_name="resource_id")


class ProgressiveActionRequest(ActionRequest):
    """Explicit Action id plus the unchanged validated ActionRequest fields."""

    action_id: str = Field(
        description="Exact action_id returned by search_actions or inspect_action."
    )

    @field_validator("action_id")
    @classmethod
    def validate_action_id(cls, value: str) -> str:
        return _catalog_id(value, field_name="action_id")


__all__ = [
    "ActionCategoryBrowseRequest",
    "ActionDomainListRequest",
    "ActionInspectRequest",
    "ActionSearchRequest",
    "BackendInspectRequest",
    "ProgressiveActionRequest",
    "ResourceInspectRequest",
    "ResourceSearchRequest",
]
