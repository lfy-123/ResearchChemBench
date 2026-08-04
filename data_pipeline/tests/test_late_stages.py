from __future__ import annotations

import json
import stat
import tempfile
import unittest
import zipfile
from pathlib import Path
from unittest.mock import patch

from src.agents.runner import run_agent
from src.agents.workspace import create_agent_run, isolated_environment
from src.core.config import normalize_config
from src.core.io import read_jsonl
from src.orchestration.pipeline import run_late_stages_records
from src.stages.stage04_resource_limits.resource_limits import bypass_resource_limits
from src.stages.stage05_asset_collection.archive import ArchiveError, safe_extract
from src.stages.stage05_asset_collection.clues import (
    extract_clues,
    normalize_url,
    seed_document_clues,
)
from src.stages.stage05_asset_collection.discovery import (
    _metadata_payload_clues,
    _publisher_attachment_clues,
    metadata_clues,
)
from src.stages.stage05_asset_collection.download import (
    DownloadError,
    _response_filename,
    register_local_file,
    validate_public_url,
)
from src.stages.stage05_asset_collection.parsers import _parse_pdf, parse_asset
from src.stages.stage05_asset_collection.stage import (
    _acquire_clue,
    _filter_discovered_clues,
    _is_supplementary_clue,
    _prioritize_archive_children,
    run_asset_collection,
)
from src.stages.stage06_builder.context import _asset_logical_path
from src.stages.stage06_builder.validation import validate_builder_candidate
from src.stages.stage07_judge.probe import public_input_probe


class LateStageTests(unittest.TestCase):
    def test_compact_config_builds_three_new_stages(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            compact = {
                "pdf_directory": "papers",
                "run_directory": "runs/test",
                "stage06": {"agent": {"cli": "claude", "model": "sonnet"}},
                "stage07": {"agent": {"cli": "codex", "model": "gpt-test"}},
            }
            config = normalize_config(compact, root)
        self.assertEqual(config["stage05"]["max_rounds"], 3)
        self.assertTrue(config["stage04"]["enabled"])
        self.assertTrue(config["stage05"]["enabled"])
        self.assertEqual(config["stage05"]["download_scope"], "all")
        self.assertEqual(config["stage06"]["agent"]["cli"], "claude")
        self.assertEqual(config["stage07"]["agent"]["cli"], "codex")
        self.assertTrue(config["stage06"]["agent"]["isolate_workspace"])
        model_cache = root / ".model_cache"
        self.assertEqual(config["mineru"]["working_directory"], str(model_cache.resolve()))
        self.assertEqual(
            config["mineru"]["environment"]["MINERU_TOOLS_CONFIG_JSON"],
            str((model_cache / "mineru" / "mineru.json").resolve()),
        )

    def test_agent_cli_environment_override_also_updates_default_command(self) -> None:
        with (
            tempfile.TemporaryDirectory() as directory,
            patch.dict("os.environ", {"BUILDER_AGENT_CLI": "codex"}),
        ):
            config = normalize_config(
                {
                    "pdf_directory": "papers",
                    "stage06": {"agent": {"cli": "opencode", "command": "opencode"}},
                },
                Path(directory),
            )

        self.assertEqual(config["stage06"]["agent"]["cli"], "codex")
        self.assertEqual(config["stage06"]["agent"]["command"], "codex")

    def test_invalid_stage05_download_scope_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "download_scope"):
                normalize_config(
                    {"pdf_directory": "papers", "stage05": {"download_scope": "unknown"}},
                    Path(directory),
                )

    def test_stage04_skip_preserves_downstream_contract(self) -> None:
        rows = bypass_resource_limits(
            [{"paper_id": "paper", "pipeline_routing": {"stage_03": "direct_covered"}}],
            {"cpu_cores": 500},
        )
        result = rows[0]["resource_limits"]
        self.assertTrue(result["passed"])
        self.assertTrue(result["skipped"])
        self.assertEqual(result["decision"], "skipped")
        self.assertEqual(result["resource_records"], [])
        self.assertTrue(rows[0]["pipeline_routing"]["continue"])

    def test_clues_keep_repository_and_availability_links(self) -> None:
        text = (
            "Code availability: scripts are available at https://github.com/example/project. "
            "Data are available at https://zenodo.org/records/12345. "
            "A background citation is https://example.org/article."
        )
        clues = extract_clues(
            text,
            paper_id="paper",
            discovery_round=1,
            source_asset_id=None,
        )
        values = {item["canonical_value"] for item in clues}
        self.assertIn("https://github.com/example/project", values)
        self.assertIn("https://zenodo.org/records/12345", values)
        self.assertNotIn("https://example.org/article", values)
        self.assertEqual(
            normalize_url("HTTPS://Example.org/a?utm_source=x&b=1#part"),
            "https://example.org/a?b=1",
        )

    def test_paper_doi_is_identity_not_download_frontier(self) -> None:
        clues = seed_document_clues({"paper_id": "paper", "doi": "10.1000/example"})
        paper_doi = next(item for item in clues if item["kind"] == "paper_doi")
        self.assertEqual(paper_doi["status"], "resolved")
        self.assertEqual(paper_doi["resolution"], "paper_identity")

    def test_archive_rejects_path_traversal(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            archive = root / "bad.zip"
            with zipfile.ZipFile(archive, "w") as handle:
                handle.writestr("../escape.txt", "bad")
            with self.assertRaises(ArchiveError):
                safe_extract(archive, root / "out")

    def test_local_asset_is_content_addressed(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "data.txt"
            source.write_text("content", encoding="utf-8")
            asset = register_local_file(
                source,
                paper_id="paper",
                object_root=root / "objects",
                role="source_data",
                relation_type="pipeline_input",
                discovered_by="test",
                discovery_round=0,
            )
            self.assertTrue(Path(asset["original_path"]).is_file())
            self.assertEqual(Path(asset["original_path"]).read_text(), "content")

    def test_stage05_parses_local_pdf_fallback_and_archive(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            study = root / "study"
            paper_dir = study / "paper"
            paper_dir.mkdir(parents=True)
            pdf = paper_dir / "paper.pdf"
            pdf.write_bytes(b"not a real pdf")
            text = root / "paper.txt"
            text.write_text("A calculation was performed with VASP.", encoding="utf-8")
            archive = study / "source-data.zip"
            with zipfile.ZipFile(archive, "w") as handle:
                handle.writestr("README.md", "Input structures and scripts")
                handle.writestr("data.csv", "x,y\n1,2\n")
            document = {
                "paper_id": "paper",
                "document_id": "paper",
                "source_path": str(pdf),
                "text_path": str(text),
                "title": "Test",
                "doi": None,
                "duplicate_of": None,
                "resource_limits": {"passed": True},
            }
            result = run_asset_collection(
                [document],
                root / "stage05",
                {
                    "max_rounds": 3,
                    "enable_network": False,
                    "include_local_siblings": True,
                    "query_metadata": False,
                    "network_workers": 1,
                },
                {"execute": False},
            )
            self.assertGreaterEqual(len(result["assets"]), 4)
            self.assertIn("grobid_fallback", {item.get("parser") for item in result["assets"]})
            self.assertIn("archive", {item.get("parser") for item in result["assets"]})

    def test_stage05_supplementary_scope_excludes_other_local_assets(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            paper_dir = root / "study" / "paper"
            paper_dir.mkdir(parents=True)
            pdf = paper_dir / "paper.pdf"
            pdf.write_bytes(b"not a real pdf")
            text = root / "paper.txt"
            text.write_text("Calculations used ORCA.", encoding="utf-8")
            with zipfile.ZipFile(root / "study" / "supporting_information.zip", "w") as handle:
                handle.writestr("SI_input.xyz", "1\nH\nH 0 0 0\n")
            with zipfile.ZipFile(root / "study" / "source_data.zip", "w") as handle:
                handle.writestr("results.csv", "x,y\n1,2\n")
            result = run_asset_collection(
                [
                    {
                        "paper_id": "paper",
                        "document_id": "paper",
                        "source_path": str(pdf),
                        "text_path": str(text),
                        "title": "Test",
                        "doi": None,
                        "duplicate_of": None,
                        "resource_limits": {"passed": True},
                    }
                ],
                root / "stage05",
                {
                    "download_scope": "supplementary_only",
                    "max_rounds": 0,
                    "enable_network": False,
                    "include_local_siblings": True,
                    "query_metadata": False,
                },
                {"execute": False},
            )
            names = {item.get("file_name") for item in result["assets"]}
            self.assertIn("paper.pdf", names)
            self.assertIn("supporting_information.zip", names)
            self.assertNotIn("source_data.zip", names)
            self.assertNotIn("results.csv", names)
            self.assertEqual(result["summary"]["download_scope"], "supplementary_only")

    def test_publisher_page_only_recalls_explicit_supplements(self) -> None:
        clues = _publisher_attachment_clues(
            """
            <a href="/article.pdf">Download article</a>
            <a href="https://cdn.example.org/si.pdf">Supplementary Information</a>
            <a href="https://github.com/example/code">Code repository</a>
            """,
            base_url="https://publisher.example.org/article",
            paper_id="paper",
        )
        self.assertEqual(
            [item["canonical_value"] for item in clues],
            ["https://cdn.example.org/si.pdf"],
        )
        self.assertEqual(clues[0]["relation_type"], "publisher_attachment")

    def test_supplementary_scope_rejects_article_url_near_si_text(self) -> None:
        self.assertFalse(
            _is_supplementary_clue(
                {
                    "kind": "url",
                    "canonical_value": "https://doi.org/10.1234/example",
                    "evidence": "Supplementary information is available with this article.",
                }
            )
        )

    def test_stage05_ignores_self_doi_recalled_from_parsed_text(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            pdf = root / "paper.pdf"
            pdf.write_bytes(b"not a real pdf")
            text = root / "paper.txt"
            text.write_text(
                "Supplementary information is available at https://doi.org/10.1234/example.",
                encoding="utf-8",
            )
            result = run_asset_collection(
                [
                    {
                        "paper_id": "paper",
                        "document_id": "paper",
                        "source_path": str(pdf),
                        "text_path": str(text),
                        "title": "Test",
                        "doi": "10.1234/example",
                        "duplicate_of": None,
                        "resource_limits": {"passed": True},
                    }
                ],
                root / "stage05",
                {
                    "download_scope": "supplementary_only",
                    "max_rounds": 0,
                    "enable_network": False,
                    "include_local_siblings": False,
                    "query_metadata": False,
                },
                {"execute": False},
            )

            self.assertEqual([item["kind"] for item in result["clues"]], ["paper_doi"])

    def test_supplementary_metadata_scope_skips_broad_discovery_apis(self) -> None:
        calls: list[str] = []

        class Response:
            def raise_for_status(self) -> None:
                return None

            def json(self) -> dict[str, object]:
                return {}

        def request(_client: object, _method: str, url: str, **_kwargs: object) -> Response:
            calls.append(url)
            return Response()

        with patch(
            "src.stages.stage05_asset_collection.discovery.request_with_retry",
            side_effect=request,
        ):
            metadata_clues(
                {"paper_id": "paper", "doi": "10.1234/example"},
                download_scope="supplementary_only",
            )

        self.assertEqual(len(calls), 3)
        self.assertTrue(any("crossref" in value for value in calls))
        self.assertTrue(any("datacite" in value for value in calls))
        self.assertTrue(any("europepmc" in value for value in calls))
        self.assertFalse(any("openalex" in value for value in calls))

    def test_stage05_skip_produces_builder_compatible_asset_result(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            pdf = root / "paper.pdf"
            pdf.write_bytes(b"not a real pdf")
            text = root / "paper.txt"
            text.write_text("Calculations used Gaussian.", encoding="utf-8")
            records = [
                {
                    "paper_id": "paper",
                    "document_id": "paper",
                    "source_path": str(pdf),
                    "text_path": str(text),
                    "title": "Test",
                    "duplicate_of": None,
                    "resource_limits": {"passed": True},
                }
            ]
            config = {
                "stop_after": "asset_collection",
                "stage05": {"enabled": False, "download_scope": "all"},
                "mineru": {"execute": True},
            }
            with patch("src.orchestration.pipeline._load_toolbox", return_value={}):
                summary = run_late_stages_records(
                    records,
                    config=config,
                    base=root,
                    workspace=root / "outputs",
                    run_metadata={"source_mode": "test"},
                )
            assets = read_jsonl(root / "outputs/stage_05_asset_collection/asset_manifest.jsonl")
            self.assertTrue(summary["stage_05"]["skipped"])
            self.assertEqual(summary["stage_05"]["skip_adapter"], "primary_pdf_with_stage02_text")
            self.assertEqual(summary["stage_05"]["clues"], 0)
            self.assertEqual(len(assets), 1)
            self.assertEqual(assets[0]["role"], "main_paper")
            self.assertEqual(assets[0]["parser"], "grobid_fallback")

    def test_html_parser_only_recalls_asset_links(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            html = root / "article"
            html.write_text(
                '<a href="/reference/1">Background paper</a>'
                '<a href="/files/supplement.zip">Supplementary information</a>',
                encoding="utf-8",
            )
            asset = register_local_file(
                html,
                paper_id="paper",
                object_root=root / "objects",
                role="other",
                relation_type="explicit_url",
                discovered_by="test",
                discovery_round=1,
            )
            asset["media_type"] = "text/html"
            asset["resolved_url"] = "https://example.org/article"
            _, _, clues = parse_asset(
                asset,
                parsed_root=root / "parsed",
                mineru_config={"execute": False},
                next_round=2,
            )
            self.assertEqual(
                [item["canonical_value"] for item in clues],
                ["https://example.org/files/supplement.zip"],
            )

    def test_europe_pmc_metadata_exposes_supplementary_archive(self) -> None:
        clues = _metadata_payload_clues(
            "europe_pmc",
            {
                "resultList": {
                    "result": [
                        {
                            "doi": "10.1021/example",
                            "pmcid": "PMC123456",
                            "hasSuppl": "Y",
                        }
                    ]
                }
            },
            "paper",
            "10.1021/example",
        )

        self.assertEqual(len(clues), 1)
        self.assertEqual(clues[0]["resource_type"], "supplement")
        self.assertEqual(clues[0]["relation_type"], "publisher_attachment")
        self.assertEqual(
            clues[0]["canonical_value"],
            "https://www.ebi.ac.uk/europepmc/webservices/rest/PMC123456/supplementaryFiles?includeInlineImage=false",
        )

    def test_download_filename_accepts_spaced_content_disposition(self) -> None:
        class Response:
            headers = {
                "content-disposition": ("attachment; filename = PMC123456_SupplementaryFiles.zip")
            }

        self.assertEqual(
            _response_filename(Response(), "https://example.org/supplementaryFiles"),
            "PMC123456_SupplementaryFiles.zip",
        )

    def test_long_pdf_uses_bounded_pdftotext_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            pdf = root / "large.pdf"
            pdf.write_bytes(b"placeholder")
            with (
                patch(
                    "src.stages.stage05_asset_collection.parsers._pdf_page_count",
                    return_value=654,
                ),
                patch(
                    "src.stages.stage05_asset_collection.parsers._pdftotext",
                    return_value="extracted text",
                ) as pdftotext,
                patch("src.stages.stage05_asset_collection.parsers.run_mineru_queue") as mineru,
            ):
                text, metadata = _parse_pdf(
                    {
                        "asset_id": "asset",
                        "paper_id": "paper",
                        "original_path": str(pdf),
                        "file_name": pdf.name,
                    },
                    root,
                    {"max_pages": 40},
                )

        self.assertEqual(text, "extracted text")
        self.assertEqual(metadata["parser"], "pdftotext_large_pdf")
        self.assertTrue(metadata["mineru_skipped"])
        pdftotext.assert_called_once()
        mineru.assert_not_called()

    def test_clue_acquisition_continues_after_one_target_fails(self) -> None:
        clue = {"paper_id": "paper", "kind": "related_doi", "canonical_value": "10.1/x"}
        targets = [
            {"url": "https://example.org/large.bin"},
            {"url": "https://example.org/readme.txt", "file_name": "README.txt"},
        ]
        asset = {"asset_id": "asset1", "paper_id": "paper"}
        with (
            tempfile.TemporaryDirectory() as directory,
            patch(
                "src.stages.stage05_asset_collection.stage.resolve_clue_targets",
                return_value=(targets, []),
            ),
            patch(
                "src.stages.stage05_asset_collection.stage.download_url",
                side_effect=[DownloadError("too large"), asset],
            ),
        ):
            acquired = _acquire_clue(clue, Path(directory), {}, 1)
        self.assertEqual(acquired, [asset])
        self.assertEqual(len(clue["target_errors"]), 1)

    def test_archive_priority_keeps_foundational_inputs_before_outputs(self) -> None:
        children = [
            Path("2D-hBN/400_8/aiida.in"),
            Path("2D-hBN/400_8/o-aiida.out.qp"),
            Path("2D-hBN/DFT/scf/aiida.in"),
            Path("README.txt"),
        ]

        ordered = _prioritize_archive_children(children, "source_data")

        self.assertLess(ordered.index(Path("2D-hBN/DFT/scf/aiida.in")), 3)
        self.assertEqual(ordered[-1], Path("2D-hBN/400_8/o-aiida.out.qp"))

    def test_code_assets_do_not_expand_into_github_dependencies(self) -> None:
        clues = [
            {"canonical_value": "https://github.com/example/dependency"},
            {"canonical_value": "https://zenodo.org/records/123"},
        ]

        filtered = _filter_discovered_clues({"role": "code"}, clues)

        self.assertEqual(filtered, [clues[1]])

    def test_agent_runner_saves_isolated_conversation(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            executable = root / "fake-opencode"
            response = {"ok": True}
            event = json.dumps(
                {
                    "type": "text",
                    "sessionID": "session-test",
                    "part": {"text": json.dumps(response)},
                }
            )
            executable.write_text(f"#!/bin/sh\nprintf '%s\\n' '{event}'\n", encoding="utf-8")
            executable.chmod(executable.stat().st_mode | stat.S_IXUSR)
            paths = create_agent_run(root / "stage", "test")
            result = run_agent(
                cli_config={
                    "cli": "opencode",
                    "command": str(executable),
                    "model": "fake/model",
                    "timeout_seconds": 30,
                },
                paths=paths,
                prompt="Return JSON",
                response_schema={
                    "type": "object",
                    "required": ["ok"],
                    "properties": {"ok": {"type": "boolean"}},
                },
                label="test-agent",
            )
            self.assertEqual(result["status"], "success")
            self.assertEqual(result["session_id"], "session-test")
            self.assertTrue(Path(result["conversation_path"]).is_file())
            self.assertTrue(str(paths["run_root"]) in result["conversation_path"])
            self.assertFalse(
                (paths["home"] / "opencode_root" / "data" / "opencode" / "auth.json").exists()
            )

    def test_agent_environment_uses_isolated_workspace_as_pwd(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            paths = create_agent_run(Path(directory), "builder")
            environment = isolated_environment(paths, "opencode")

        self.assertEqual(environment["PWD"], str(paths["workspace"]))
        self.assertEqual(environment["INIT_CWD"], str(paths["workspace"]))

    def test_agent_asset_logical_path_keeps_archive_context_only(self) -> None:
        logical = _asset_logical_path(
            {
                "file_name": "aiida.in",
                "source_local_path": "/private/run/parsed/asset/extracted/raw/2D-hBN/DFT/scf/aiida.in",
            }
        )

        self.assertEqual(logical, "raw/2D-hBN/DFT/scf/aiida.in")
        self.assertNotIn("/private/run", logical)

    def test_agent_runner_retries_transient_error_and_records_usage(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            executable = root / "fake-opencode"
            error = json.dumps(
                {
                    "type": "error",
                    "error": {"name": "UnknownError", "message": "Unexpected server error"},
                }
            )
            success = json.dumps(
                {
                    "type": "text",
                    "sessionID": "retry-session",
                    "part": {"text": '{"ok": true}'},
                }
            )
            usage = json.dumps(
                {
                    "type": "step_finish",
                    "part": {"tokens": {"input": 10, "output": 2, "total": 12}},
                }
            )
            executable.write_text(
                "#!/bin/sh\n"
                'marker="$TMPDIR/retried"\n'
                'if [ ! -f "$marker" ]; then\n'
                '  touch "$marker"\n'
                f"  printf '%s\\n' '{error}'\n"
                "  exit 1\n"
                "fi\n"
                f"printf '%s\\n' '{success}' '{usage}'\n",
                encoding="utf-8",
            )
            executable.chmod(executable.stat().st_mode | stat.S_IXUSR)
            paths = create_agent_run(root / "stage", "retry")
            result = run_agent(
                cli_config={
                    "cli": "opencode",
                    "command": str(executable),
                    "model": "fake/model",
                    "timeout_seconds": 30,
                    "retries": 1,
                },
                paths=paths,
                prompt="Return JSON",
                response_schema={
                    "type": "object",
                    "required": ["ok"],
                    "properties": {"ok": {"type": "boolean"}},
                },
                label="retry-agent",
            )
            self.assertEqual(result["status"], "success")
            self.assertEqual(len(result["attempts"]), 2)
            self.assertEqual(result["usage"]["total"], 12)
            self.assertTrue(
                (paths["run_root"] / "attempts" / "attempt_01" / "stdout.log").is_file()
            )

    def test_builder_validation_and_public_probe(self) -> None:
        assets = [{"asset_id": "asset1", "original_path": "/tmp/a", "sha256": "x"}]
        document = {"software_coverage": {"core_software": [{"normalized_name": "vasp"}]}}
        response = {
            "decision": "candidate",
            "task": {
                "objective": "Run a calculation",
                "instructions": ["Use the supplied input"],
                "expected_deliverables": ["Calculated energy"],
                "allowed_software": ["vasp"],
                "allowed_actions": ["calculate_energy"],
                "public_asset_ids": ["asset1"],
            },
            "hidden_reference": {"expected_results": ["a sufficiently long hidden result value"]},
            "scoring_rubric": [{"criterion": "result", "points": 100, "method": "compare"}],
            "evidence_map": [{"claim": "input", "asset_id": "asset1", "evidence": "source"}],
        }
        report = validate_builder_candidate(
            response,
            assets=assets,
            document=document,
            toolbox={"actions": ["calculate_energy"]},
        )
        self.assertTrue(report["passed"])
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "public_inputs").mkdir()
            (root / "candidate_task.json").write_text("{}")
            (root / "task.md").write_text("task")
            (root / "public_inputs" / "manifest.json").write_text("[]")
            self.assertTrue(public_input_probe(root)["passed"])

    def test_builder_validation_rejects_placeholder_candidate(self) -> None:
        response = {
            "decision": "candidate",
            "task": {
                "instructions": ["Not constructed: insufficient evidence"],
                "expected_deliverables": ["Not constructed"],
                "allowed_software": ["yambo"],
                "allowed_actions": [],
                "public_asset_ids": ["asset1"],
            },
            "hidden_reference": {"expected_results": ["hidden reference result"]},
            "scoring_rubric": [
                {"criterion": "placeholder", "points": 100, "method": "no grading applies"}
            ],
            "evidence_map": [{"claim": "input", "asset_id": "asset1", "evidence": "source"}],
        }

        report = validate_builder_candidate(
            response,
            assets=[{"asset_id": "asset1"}],
            document={"software_coverage": {"core_software": [{"normalized_name": "yambo"}]}},
            toolbox={"actions": []},
        )

        self.assertFalse(report["passed"])
        self.assertIn("candidate contains abstention or placeholder task content", report["errors"])

    def test_private_url_is_rejected(self) -> None:
        with self.assertRaises(DownloadError):
            validate_public_url("http://127.0.0.1/file")

    @patch("src.stages.stage05_asset_collection.download.socket.getaddrinfo")
    def test_https_github_hosts_work_with_proxy_dns(self, getaddrinfo) -> None:
        getaddrinfo.return_value = [(2, 1, 6, "", ("100.64.0.2", 443))]

        validate_public_url("https://api.github.com/repos/example/project/zipball/main")

        getaddrinfo.assert_not_called()


if __name__ == "__main__":
    unittest.main()
