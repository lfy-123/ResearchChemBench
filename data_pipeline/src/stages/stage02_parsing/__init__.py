"""Stage 02: GROBID parsing with the configured per-document fallback."""

from src.integrations.grobid import extract_documents_with_grobid, grobid_service
from src.stages.stage02_parsing.bundles import build_paper_text_bundles

__all__ = ["build_paper_text_bundles", "extract_documents_with_grobid", "grobid_service"]
