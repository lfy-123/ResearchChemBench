"""Compatibility exports for the split ActionSpec and BackendSpec catalog."""

from __future__ import annotations

from .actions import ACTION_SPECS
from .backend_specs import BACKEND_SPECS

__all__ = ["ACTION_SPECS", "BACKEND_SPECS"]
