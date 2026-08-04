from __future__ import annotations

from pathlib import Path
from typing import Any

SUPPLEMENTARY_HINTS = (
    "supplementary",
    "supporting_information",
    "supporting-information",
    "_si_",
    "-si-",
    "_si.",
    "s001",
    "moesm",
    "esm",
    "appendix",
)

GENERIC_SUPPLEMENTARY_TITLES = (
    "microsoft word",
    "supplementary information",
    "supporting information",
    "supporting data",
    "peer review file",
    "si.docx",
)


def classify_document_role(source_path: str | Path, title: Any = None) -> str:
    normalized_path = str(source_path).casefold().replace(" ", "_")
    normalized_title = str(title or "").casefold()
    if any(hint in normalized_path for hint in SUPPLEMENTARY_HINTS):
        return "supplementary"
    if any(value in normalized_title for value in GENERIC_SUPPLEMENTARY_TITLES):
        return "supplementary"
    return "main_paper"
