from __future__ import annotations

import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from src.ingestion.grobid_quantities import GrobidQuantitiesClient
from src.ingestion.softcite import SoftciteClient, SoftciteError
from src.screening.computation_completeness import assess_computation_completeness
from src.screening.resource_limits import assess_resource_limits
from src.screening.software_coverage import assess_software_coverage


class FakeSoftciteClient:
    def __init__(self, mentions: list[dict]) -> None:
        self.mentions = mentions

    def version(self) -> dict:
        return {"version": "test", "revision": "fixture"}

    def annotate_tei(self, _path: str | Path) -> dict:
        return {"mentions": self.mentions}

    def characterize_context(self, _text: str) -> dict:
        return {"classification": {"used": {"value": True, "score": 0.99}}}


class FakeQuantitiesClient:
    def version(self) -> dict:
        return {"version": "test", "revision": "fixture"}

    def process_text(self, _text: str) -> dict:
        return {"measurements": []}


class StageGateTests(unittest.TestCase):
    def test_grobid_quantities_uses_multipart_text_field(self) -> None:
        response = io.BytesIO(b'{"measurements": []}')
        with mock.patch("urllib.request.urlopen", return_value=response) as urlopen:
            result = GrobidQuantitiesClient(retries=0).process_text("used 8 GPUs")

        request = urlopen.call_args.args[0]
        content_type = request.headers["Content-type"]
        self.assertTrue(content_type.startswith("multipart/form-data; boundary="))
        self.assertIn(b'name="text"', request.data)
        self.assertIn(b"used 8 GPUs", request.data)
        self.assertEqual(result, {"measurements": []})

    def test_softcite_fatal_model_log_stops_the_stage(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            log = Path(directory) / "softcite.log"
            log.write_text(
                "ERROR DeLFT classifier model initialization failed\n", encoding="utf-8"
            )
            client = SoftciteClient(service_log=str(log))
            with self.assertRaises(SoftciteError):
                client._raise_on_fatal_service_log()

    def test_stage03_routes_direct_equivalent_and_unsupported(self) -> None:
        gaussian = _mention("Gaussian 16")
        qchem = _mention("Q-Chem")
        cases = [
            ([gaussian], "direct_covered"),
            ([gaussian, qchem], "capability_equivalent"),
            ([gaussian, _mention("UnknownChem")], "unsupported"),
            ([], "unsupported"),
        ]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tei = root / "paper.tei.xml"
            aliases = root / "aliases.json"
            roles = root / "roles.json"
            capabilities = root / "capabilities.json"
            aliases.write_text(
                json.dumps(
                    {
                        "gaussian": ["Gaussian 16"],
                        "qchem": ["Q-Chem"],
                        "unknownchem": ["UnknownChem"],
                    }
                ),
                encoding="utf-8",
            )
            roles.write_text('{"ignore": [], "auxiliary": []}', encoding="utf-8")
            capabilities.write_text(
                json.dumps(
                    {
                        "qchem": {
                            "usage_patterns": ["calculations"],
                            "required_actions": ["calculate_energy"],
                            "equivalent_backends": ["gaussian"],
                        }
                    }
                ),
                encoding="utf-8",
            )
            toolbox = {
                "backends": ["gaussian"],
                "scientific_smoke": ["gaussian"],
                "actions": ["calculate_energy"],
                "unavailable": [],
            }
            document = {
                "document_id": "doc_test",
                "paper_id": "doc_test",
                "source_path": str(root / "paper.pdf"),
                "grobid_tei_path": str(tei),
                "title": "Test paper",
            }
            for mentions, expected in cases:
                with self.subTest(expected=expected):
                    names = " and ".join(
                        item["software-name"]["rawForm"] for item in mentions
                    ) or "an undocumented program"
                    tei.write_text(
                        _tei(f"All calculations were performed with {names}."),
                        encoding="utf-8",
                    )
                    records = assess_software_coverage(
                        [document],
                        FakeSoftciteClient(mentions),
                        toolbox,
                        aliases_file=aliases,
                        role_rules_file=roles,
                        capability_map_file=capabilities,
                        raw_output_dir=root / expected,
                    )
                    self.assertEqual(records[0]["software_coverage"]["decision"], expected)

    def test_stage03_ignores_background_or_auxiliary_mentions(self) -> None:
        background = _mention("Gaussian 16", used=False)
        python = _mention("Python")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tei = root / "paper.tei.xml"
            tei.write_text(
                """<TEI xmlns="http://www.tei-c.org/ns/1.0"><text><body><div><head>Methods</head><p>The analysis scripts were written in Python.</p></div></body></text></TEI>""",
                encoding="utf-8",
            )
            for name, value in {
                "aliases.json": {"gaussian": ["Gaussian 16"], "python": ["Python"]},
                "roles.json": {"ignore": [], "auxiliary": ["Python"]},
                "capabilities.json": {},
            }.items():
                (root / name).write_text(json.dumps(value), encoding="utf-8")
            records = assess_software_coverage(
                [
                    {
                        "document_id": "doc_test",
                        "paper_id": "doc_test",
                        "source_path": str(root / "paper.pdf"),
                        "grobid_tei_path": str(tei),
                    }
                ],
                FakeSoftciteClient([background, python]),
                {"backends": ["gaussian"], "actions": [], "unavailable": []},
                aliases_file=root / "aliases.json",
                role_rules_file=root / "roles.json",
                capability_map_file=root / "capabilities.json",
                raw_output_dir=root / "raw",
            )
            result = records[0]["software_coverage"]
            self.assertEqual(result["decision"], "unsupported")
            self.assertEqual(result["core_software"], [])
            self.assertEqual(result["auxiliary_software"][0]["normalized_name"], "python")

    def test_stage03_recovers_later_use_and_ignores_gaussian_basis(self) -> None:
        unused_lammps = _mention("LAMMPS", used=False)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tei = root / "paper.tei.xml"
            tei.write_text(
                _tei(
                    "A Gaussian basis set was selected. "
                    "The production simulations were run with LAMMPS and the PLUMED plugin."
                ),
                encoding="utf-8",
            )
            (root / "aliases.json").write_text(
                json.dumps(
                    {
                        "gaussian": ["Gaussian"],
                        "lammps": ["LAMMPS"],
                        "plumed": ["PLUMED"],
                    }
                ),
                encoding="utf-8",
            )
            (root / "roles.json").write_text(
                '{"ignore": [], "auxiliary": []}', encoding="utf-8"
            )
            (root / "capabilities.json").write_text("{}", encoding="utf-8")
            rows = assess_software_coverage(
                [
                    {
                        "document_id": "doc_test",
                        "paper_id": "doc_test",
                        "source_path": str(root / "paper.pdf"),
                        "grobid_tei_path": str(tei),
                    }
                ],
                FakeSoftciteClient([unused_lammps]),
                {"backends": ["lammps", "plumed"], "actions": [], "unavailable": []},
                aliases_file=root / "aliases.json",
                role_rules_file=root / "roles.json",
                capability_map_file=root / "capabilities.json",
                raw_output_dir=root / "raw",
            )
            result = rows[0]["software_coverage"]
            self.assertEqual(result["decision"], "direct_covered")
            self.assertEqual(
                {item["normalized_name"] for item in result["core_software"]},
                {"lammps", "plumed"},
            )

    def test_stage04_complete_reject_and_skip_semantics(self) -> None:
        complete = {
            "decision": "complete",
            "has_computational_object": True,
            "has_method_setup": True,
            "has_software_execution": True,
            "has_computational_results": True,
            "has_interpretation_or_conclusion": True,
            "evidence": ["The optimized structures were analyzed."],
            "reason": "A complete calculation and result chain is present.",
        }
        incomplete = {**complete, "decision": "incomplete", "has_computational_results": False}
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            document = _screened_document(root, "The calculations produced optimized structures.")

            def caller(**_kwargs):
                return complete, {"raw_content": json.dumps(complete), "model_returned": "test"}

            passed = assess_computation_completeness(
                [document],
                {"enabled": True, "base_url": "http://test", "model": "test", "api_key": "x"},
                output_dir=root / "complete",
                model_caller=caller,
            )
            self.assertTrue(passed[0]["computation_completeness"]["passed"])

            def reject_caller(**_kwargs):
                return incomplete, {"raw_content": json.dumps(incomplete)}

            rejected = assess_computation_completeness(
                [document],
                {"enabled": True, "base_url": "http://test", "model": "test", "api_key": "x"},
                output_dir=root / "incomplete",
                model_caller=reject_caller,
            )
            self.assertEqual(rejected[0]["pipeline_routing"]["stage_05"], "not_run")

            skipped = assess_computation_completeness(
                [document], {"enabled": False}, output_dir=root / "skipped"
            )
            self.assertEqual(skipped[0]["computation_completeness"]["status"], "skipped")
            self.assertTrue(skipped[0]["pipeline_routing"]["continue"])

    def test_stage04_contradictory_response_becomes_uncertain(self) -> None:
        contradictory = {
            "decision": "incomplete",
            "has_computational_object": True,
            "has_method_setup": True,
            "has_software_execution": True,
            "has_computational_results": True,
            "has_interpretation_or_conclusion": True,
            "evidence": ["All five required elements are present."],
            "reason": "The process is complete.",
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            document = _screened_document(root, "Calculations produced interpreted results.")

            def caller(**_kwargs):
                return contradictory, {"raw_content": json.dumps(contradictory)}

            rows = assess_computation_completeness(
                [document],
                {"enabled": True, "base_url": "http://test", "model": "test", "api_key": "x"},
                output_dir=root / "out",
                model_caller=caller,
            )
            result = rows[0]["computation_completeness"]
            self.assertEqual(result["decision"], "uncertain")
            self.assertFalse(result["passed"])
            self.assertEqual(
                result["model_result"]["consistency_warnings"],
                ["decision_incomplete_conflicts_with_all_requirement_flags_true"],
            )

    def test_stage04_api_failure_skips_without_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            document = _screened_document(root, "Calculations were performed with Gaussian.")

            def failing_caller(**_kwargs):
                raise TimeoutError("fixture timeout")

            rows = assess_computation_completeness(
                [document],
                {"enabled": True, "base_url": "http://test", "model": "test", "api_key": "x"},
                output_dir=root / "out",
                model_caller=failing_caller,
            )
            result = rows[0]["computation_completeness"]
            self.assertEqual(result["status"], "skipped_error")
            self.assertEqual(result["decision"], "skipped")
            self.assertTrue(result["passed"])

    def test_stage05_rejects_only_explicit_over_limit_resources(self) -> None:
        cases = [
            ("The calculations used 501 CPU cores.", "exceeds_limit"),
            ("The calculations used 8 GPUs and 900 GB memory.", "within_limit"),
            ("The cluster supports 2048 CPU cores.", "ambiguous"),
            ("A 100 ns trajectory was generated with a 2 fs timestep.", "no_explicit_resource"),
            ("The simulation ran for 13 hours.", "exceeds_limit"),
            ("The reaction was performed for 24 hours at room temperature.", "ambiguous"),
        ]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for index, (text, expected) in enumerate(cases):
                with self.subTest(text=text):
                    document = _screened_document(root / str(index), text)
                    rows = assess_resource_limits(
                        [document],
                        FakeQuantitiesClient(),
                        {"cpu_cores": 500, "gpus": 8, "memory_gb": 1000, "runtime_hours": 12},
                        output_dir=root / f"out_{index}",
                    )
                    self.assertEqual(rows[0]["resource_limits"]["decision"], expected)


def _mention(name: str, *, used: bool = True) -> dict:
    return {
        "software-name": {"rawForm": name, "normalizedForm": name},
        "context": f"All calculations were performed with {name}.",
        "mentionContextAttributes": {"used": {"value": used, "score": 0.99}},
        "documentContextAttributes": {"used": {"value": used, "score": 0.99}},
    }


def _tei(text: str) -> str:
    return (
        '<TEI xmlns="http://www.tei-c.org/ns/1.0"><text><body><div>'
        f"<head>Methods</head><p>{text}</p>"
        "</div></body></text></TEI>"
    )


def _screened_document(root: Path, text: str) -> dict:
    root.mkdir(parents=True, exist_ok=True)
    tei = root / "paper.tei.xml"
    tei.write_text(_tei(text), encoding="utf-8")
    return {
        "document_id": f"doc_{root.name}",
        "paper_id": f"doc_{root.name}",
        "source_path": str(root / "paper.pdf"),
        "grobid_tei_path": str(tei),
        "title": "Fixture paper",
        "abstract": "A computational chemistry study.",
        "software_coverage": {
            "decision": "direct_covered",
            "core_software": [{"normalized_name": "gaussian", "evidence": text}],
        },
        "computation_completeness": {"passed": True, "decision": "complete"},
        "pipeline_routing": {"stage_03": "direct_covered", "stage_04": "complete"},
    }


if __name__ == "__main__":
    unittest.main()
