"""Stage 02: GROBID parsing with the configured per-document fallback."""

from src.integrations.grobid import extract_documents_with_grobid, grobid_service

__all__ = ["extract_documents_with_grobid", "grobid_service"]
