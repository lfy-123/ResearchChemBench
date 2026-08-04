from __future__ import annotations

import contextlib
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from src.integrations.grobid import GrobidError, extract_documents_with_grobid, parse_grobid_tei
from src.integrations.pdf_fallback import text_to_minimal_tei
from src.orchestration.pipeline import run_corpus_pipeline


class BrokenGrobidClient:
    def process_fulltext_document(self, _path: str | Path) -> str:
        raise RuntimeError("fixture GROBID failure")


class Stage02FallbackTests(unittest.TestCase):
    def test_minimal_tei_is_consumable_by_stage02_and_stage03(self) -> None:
        tei = text_to_minimal_tei(
            "# Methods\n\nAll calculations were performed with Gaussian 16.\n\n# Results\n\nDone.",
            title="Fallback paper",
            abstract="Fallback abstract",
        )
        parsed = parse_grobid_tei(tei)
        self.assertEqual(parsed["title"], "Fallback paper")
        self.assertIn("Methods", parsed["section_headings"])
        self.assertIn("Gaussian 16", parsed["text"])

    def test_failed_grobid_request_uses_fallback_tei(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            pdf = root / "paper.pdf"
            pdf.write_bytes(b"fixture")
            fallback = {
                "parser": "pdftotext",
                "text": "# Methods\n\nCalculations used ORCA.",
                "tei_xml": text_to_minimal_tei(
                    "# Methods\n\nCalculations used ORCA.", title="Fallback title"
                ),
                "title": "Fallback title",
                "abstract": "",
                "details": {"return_code": 0},
            }
            with patch("src.integrations.grobid.fallback_pdf_to_tei", return_value=fallback):
                records = extract_documents_with_grobid(
                    [
                        {
                            "document_id": "doc_test",
                            "paper_id": "doc_test",
                            "source_path": str(pdf),
                            "file_name": pdf.name,
                            "duplicate_of": None,
                            "document_role": "main_paper",
                            "page_count": 1,
                        }
                    ],
                    BrokenGrobidClient(),
                    root / "tei",
                    root / "text",
                    fallback_config={"enabled": True, "output_dir": str(root / "fallback")},
                )
            record = records[0]
            self.assertEqual(record["grobid_extract_status"], "fallback_pdftotext")
            self.assertEqual(record["metadata_source"], "pdftotext_fallback_tei")
            self.assertTrue(record["grobid_request_attempted"])
            self.assertTrue(record["grobid_request_failed"])
            self.assertIn("fixture GROBID failure", record["grobid_request_error"])
            self.assertTrue(Path(record["grobid_tei_path"]).is_file())
            self.assertNotIn("tei_xml", record["grobid_fallback"])

    def test_service_startup_failure_stops_pipeline(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = self._pipeline_config(root)
            with (
                patch("src.orchestration.pipeline.inventory_corpus", return_value=[]),
                patch(
                    "src.orchestration.pipeline.grobid_service",
                    side_effect=GrobidError("service startup failed"),
                ),
                self.assertRaisesRegex(GrobidError, "service startup failed"),
            ):
                run_corpus_pipeline(root / "config.json", config, root)

    def test_stage_summary_records_request_failure_ratio(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            pdf = root / "paper.pdf"
            pdf.write_bytes(b"fixture")
            inventory = [
                {
                    "document_id": "doc_test",
                    "paper_id": "doc_test",
                    "source_path": str(pdf),
                    "file_name": pdf.name,
                    "relative_path": pdf.name,
                    "duplicate_of": None,
                    "document_role": "main_paper",
                    "page_count": 1,
                    "inventory_status": "canonical",
                }
            ]
            fallback = {
                "parser": "pdftotext",
                "text": "Calculations used ORCA.",
                "tei_xml": text_to_minimal_tei("Calculations used ORCA.", title="Fallback"),
                "title": "Fallback",
                "abstract": "",
                "details": {"return_code": 0},
            }
            config = self._pipeline_config(root)
            with (
                patch("src.orchestration.pipeline.inventory_corpus", return_value=inventory),
                patch(
                    "src.orchestration.pipeline.grobid_service",
                    return_value=contextlib.nullcontext(BrokenGrobidClient()),
                ),
                patch("src.integrations.grobid.fallback_pdf_to_tei", return_value=fallback),
            ):
                run_corpus_pipeline(root / "config.json", config, root)
            summary = json.loads(
                (root / "outputs/stage_02_grobid_extract/summary.json").read_text()
            )
            self.assertEqual(summary["grobid_request_attempts"], 1)
            self.assertEqual(summary["grobid_request_failures"], 1)
            self.assertEqual(summary["grobid_request_failure_ratio"], 1.0)

    @staticmethod
    def _pipeline_config(root: Path) -> dict[str, object]:
        return {
            "source": {"mode": "corpus", "root": str(root), "exclude_supplementary": True},
            "workspace": str(root / "outputs"),
            "stop_after": "grobid_extract",
            "grobid_extract": {
                "tei_dir": str(root / "outputs/stage_02_grobid_extract/tei"),
                "text_dir": str(root / "outputs/stage_02_grobid_extract/text"),
                "fallback": {
                    "enabled": True,
                    "output_dir": str(root / "outputs/stage_02_grobid_extract/fallback"),
                },
            },
        }


if __name__ == "__main__":
    unittest.main()
