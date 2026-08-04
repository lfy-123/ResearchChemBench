from __future__ import annotations

import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from src.integrations.grobid_quantities import GrobidQuantitiesClient
from src.integrations.softcite import SoftciteClient, SoftciteError
from src.stages.stage03_software_coverage.software_coverage import assess_software_coverage
from src.stages.stage04_resource_limits.resource_limits import (
    _recall_contexts,
    assess_resource_limits,
)


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
    def test_stage04_does_not_treat_ordinal_steps_as_runtime(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            tei = Path(directory) / "paper.tei.xml"
            tei.write_text(
                _tei(
                    "The second step forms a tetracyclic core intermediate. "
                    "The calculation then ran for 14 hours on 32 CPU cores."
                ),
                encoding="utf-8",
            )

            contexts = _recall_contexts(tei)

        self.assertEqual(len(contexts), 1)
        self.assertIn("14 hours", contexts[0]["text"])

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
            log.write_text("ERROR DeLFT classifier model initialization failed\n", encoding="utf-8")
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
            ([], "software_not_identified"),
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
                "available_identifiers": ["gaussian"],
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
                    names = (
                        " and ".join(item["software-name"]["rawForm"] for item in mentions)
                        or "an undocumented program"
                    )
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
            self.assertEqual(result["decision"], "software_not_identified")
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
                    "A Gaussian bias potential was deposited. "
                    "A new Gaussian was deposited every 25 fs. "
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
            (root / "roles.json").write_text('{"ignore": [], "auxiliary": []}', encoding="utf-8")
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

    def test_stage03_accepts_interface_runtime_and_ignores_force_field_names(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tei = root / "paper.tei.xml"
            tei.write_text(
                _tei(
                    "GW calculations were performed with Yambo. "
                    "The AMBER force field and GAFF2 parameters were used."
                ),
                encoding="utf-8",
            )
            (root / "aliases.json").write_text(
                json.dumps({"yambo": ["Yambo"], "amber_pmemd": ["AMBER", "GAFF2"]}),
                encoding="utf-8",
            )
            (root / "roles.json").write_text('{"ignore": [], "auxiliary": []}', encoding="utf-8")
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
                FakeSoftciteClient(
                    [
                        _mention(
                            "AMBER",
                            context="The AMBER force field and GAFF2 parameters were used.",
                        )
                    ]
                ),
                {
                    "available_identifiers": ["yambo"],
                    "interface_smoke": ["yambo"],
                    "backends": [],
                    "actions": [],
                    "unavailable": [],
                },
                aliases_file=root / "aliases.json",
                role_rules_file=root / "roles.json",
                capability_map_file=root / "capabilities.json",
                raw_output_dir=root / "raw",
            )
            result = rows[0]["software_coverage"]
            self.assertEqual(result["decision"], "direct_covered")
            self.assertEqual(
                [item["normalized_name"] for item in result["core_software"]], ["yambo"]
            )
            self.assertEqual(
                result["core_software"][0]["direct_support"]["validation_level"],
                "interface",
            )

    def test_stage03_recovers_compact_gaussian_and_ignores_auxiliary_tools(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            tei = root / "paper.tei.xml"
            tei.write_text(
                _tei(
                    "Computations were performed using the Gaussian09 suite. "
                    "Graphical representations were generated with CYLView. "
                    "The crystal structure was solved with ShelXT using Olex2."
                ),
                encoding="utf-8",
            )
            capabilities = root / "capabilities.json"
            capabilities.write_text("{}", encoding="utf-8")
            assets = Path(__file__).resolve().parents[1] / "assets"
            rows = assess_software_coverage(
                [
                    {
                        "document_id": "doc_test",
                        "paper_id": "doc_test",
                        "source_path": str(root / "paper.pdf"),
                        "grobid_tei_path": str(tei),
                    }
                ],
                FakeSoftciteClient(
                    [
                        _mention("CYLView"),
                        _mention("ShelXT"),
                        _mention("Olex2"),
                    ]
                ),
                {
                    "backends": ["gaussian"],
                    "available_identifiers": ["gaussian"],
                    "scientific_smoke": ["gaussian"],
                    "actions": [],
                    "unavailable": [],
                },
                aliases_file=assets / "software_aliases.json",
                role_rules_file=assets / "software_role_rules.json",
                capability_map_file=capabilities,
                raw_output_dir=root / "raw",
            )
            result = rows[0]["software_coverage"]
            self.assertEqual(result["decision"], "direct_covered")
            self.assertEqual(
                [item["normalized_name"] for item in result["core_software"]],
                ["gaussian"],
            )
            self.assertEqual(
                {item["normalized_name"] for item in result["auxiliary_software"]},
                {"cylview", "shelxt", "olex2"},
            )

    def test_stage04_normalizes_resources_before_comparing_limits(self) -> None:
        cases = [
            (
                "The average CENSO job took 1 day and 4 hours of wall time using 54 cores.",
                [
                    _resource(
                        "runtime_hours",
                        28,
                        "The average CENSO job took 1 day and 4 hours of wall time using 54 cores.",
                    ),
                    _resource(
                        "cpu_cores",
                        54,
                        "The average CENSO job took 1 day and 4 hours of wall time using 54 cores.",
                    ),
                ],
                "exceeds_limit",
            ),
            (
                "The run used a 40-core (230 GB RAM) Intel Xeon Gold 6230 CPU for 6 hours.",
                [
                    _resource(
                        "cpu_cores",
                        40,
                        "The run used a 40-core (230 GB RAM) Intel Xeon Gold 6230 CPU for 6 hours.",
                    ),
                    _resource(
                        "memory_gb",
                        230,
                        "The run used a 40-core (230 GB RAM) Intel Xeon Gold 6230 CPU for 6 hours.",
                    ),
                    _resource(
                        "runtime_hours",
                        6,
                        "The run used a 40-core (230 GB RAM) Intel Xeon Gold 6230 CPU for 6 hours.",
                    ),
                ],
                "within_limit",
            ),
        ]
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for index, (text, records, expected) in enumerate(cases):
                with self.subTest(text=text):
                    document = _screened_document(root / str(index), text)

                    def caller(*, result=records, **_kwargs):
                        return _model_result(result), {"usage": {"prompt_tokens": 10}}

                    rows = assess_resource_limits(
                        [document],
                        FakeQuantitiesClient(),
                        _limits(),
                        _model_config(),
                        output_dir=root / f"out_{index}",
                        model_caller=caller,
                    )
                    self.assertEqual(rows[0]["resource_limits"]["decision"], expected)

    def test_stage04_keeps_aggregate_compute_out_of_core_limit(self) -> None:
        text = "A total of 13 million core hours were used in this study."
        aggregate = {
            **_resource("core_hours", 13_000_000, text, scope="aggregate_study"),
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            def caller(**_kwargs):
                return _model_result([], aggregate=[aggregate]), {}

            rows = assess_resource_limits(
                [_screened_document(root, text)],
                FakeQuantitiesClient(),
                _limits(),
                _model_config(),
                output_dir=root / "out",
                model_caller=caller,
            )
            self.assertEqual(rows[0]["resource_limits"]["decision"], "ambiguous")
            self.assertEqual(
                rows[0]["resource_limits"]["aggregate_resources"][0]["value"],
                13_000_000,
            )

    def test_stage04_empty_model_result_is_no_explicit_resource(self) -> None:
        text = "The method has a much lower computational cost."
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            def caller(**_kwargs):
                return _model_result([]), {}

            rows = assess_resource_limits(
                [_screened_document(root, text)],
                FakeQuantitiesClient(),
                _limits(),
                _model_config(),
                output_dir=root / "out",
                model_caller=caller,
            )

            self.assertEqual(rows[0]["resource_limits"]["decision"], "no_explicit_resource")

    def test_stage04_retries_invalid_evidence_and_stops_on_api_failure(self) -> None:
        text = "The simulation ran for 13 hours."
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            calls = 0

            def retrying_caller(**_kwargs):
                nonlocal calls
                calls += 1
                evidence = "Invented evidence." if calls == 1 else text
                return _model_result([_resource("runtime_hours", 13, evidence)]), {}

            rows = assess_resource_limits(
                [_screened_document(root, text)],
                FakeQuantitiesClient(),
                _limits(),
                _model_config(),
                output_dir=root / "retry",
                model_caller=retrying_caller,
            )
            self.assertEqual(calls, 2)
            self.assertEqual(rows[0]["resource_limits"]["decision"], "exceeds_limit")

            def failing_caller(**_kwargs):
                raise TimeoutError("fixture timeout")

            with self.assertRaises(TimeoutError):
                assess_resource_limits(
                    [_screened_document(root / "failure", text)],
                    FakeQuantitiesClient(),
                    _limits(),
                    _model_config(),
                    output_dir=root / "failure_out",
                    model_caller=failing_caller,
                )

    def test_stage04_rejects_cpu_model_number_as_core_count(self) -> None:
        text = "The run used a 40-core Intel Xeon Gold 6230 CPU for 6 hours."
        calls = 0
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)

            def caller(**_kwargs):
                nonlocal calls
                calls += 1
                cores = 6230 if calls == 1 else 40
                return _model_result([_resource("cpu_cores", cores, text)]), {}

            rows = assess_resource_limits(
                [_screened_document(root, text)],
                FakeQuantitiesClient(),
                _limits(),
                _model_config(),
                output_dir=root / "out",
                model_caller=caller,
            )
            self.assertEqual(calls, 2)
            self.assertEqual(rows[0]["resource_limits"]["decision"], "within_limit")


def _mention(name: str, *, used: bool = True, context: str | None = None) -> dict:
    return {
        "software-name": {"rawForm": name, "normalizedForm": name},
        "context": context or f"All calculations were performed with {name}.",
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
        "pipeline_routing": {"stage_03": "direct_covered", "stage_04": "pending"},
    }


def _limits() -> dict:
    return {"cpu_cores": 500, "gpus": 8, "memory_gb": 1000, "runtime_hours": 12}


def _model_config() -> dict:
    return {
        "enabled": True,
        "base_url": "http://test",
        "model": "test",
        "api_key": "x",
        "validation_retries": 1,
    }


def _resource(
    resource_type: str, value: float, evidence: str, *, scope: str = "single_job"
) -> dict:
    return {
        "resource_type": resource_type,
        "value": value,
        "relation": "exact",
        "scope": scope,
        "actual_computation": True,
        "confidence": "high",
        "evidence": evidence,
    }


def _model_result(records: list[dict], *, aggregate: list[dict] | None = None) -> dict:
    return {
        "resource_records": records,
        "aggregate_resources": aggregate or [],
        "platform_mentions": [],
        "physical_simulation_durations": [],
        "unresolved_mentions": [],
    }


if __name__ == "__main__":
    unittest.main()
