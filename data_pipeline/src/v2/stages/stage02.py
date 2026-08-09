"""Stage 02: screen for substantive computational-chemistry content.

The legacy exports remain temporarily available for callers that used Stage 02
as the document-normalization stage before the v2.1 layout migration.
"""

from src.v2.stages import _document_normalization as _normalization_impl
from src.v2.stages._computational_content import run_computational_content_screening
from src.v2.stages._document_normalization import (
    _normalize_non_pdf,
    _paper_quality,
    _pdftotext_fallback,
    assess_text_quality,
    extract_documents_with_grobid,
    materialize_document,
    run_document_normalization,
)

__all__ = [
    "_normalize_non_pdf",
    "_paper_quality",
    "_pdftotext_fallback",
    "assess_text_quality",
    "extract_documents_with_grobid",
    "materialize_document",
    "run_stage02",
]


def run_stage02(**kwargs):
    # Keep the pre-split API readable for old cached-workspace tests and callers.
    if "model" not in kwargs:
        _normalization_impl.extract_documents_with_grobid = globals()[
            "extract_documents_with_grobid"
        ]
        _normalization_impl._pdftotext_fallback = globals()["_pdftotext_fallback"]
        return run_document_normalization(**kwargs)
    return run_computational_content_screening(**kwargs)
