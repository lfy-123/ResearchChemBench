from __future__ import annotations

import sys
import tempfile
import unittest
from copy import deepcopy
from pathlib import Path

from src.core.assets import prompt_example
from src.core.config import normalize_config
from src.core.io import read_json, stable_id, write_json
from src.core.models import TASK_TYPES
from src.core.runtime import runtime_tier
from src.curation.availability import assess_asset_availability
from src.curation.extract import collect_text
from src.curation.model_review import (
    _reconcile_candidate_verdict,
    _review_packet,
    review_with_ensemble,
)
from src.curation.package_generation import (
    generate_complete_packages,
    generation_prompt,
)
from src.curation.package_validation import package_readiness
from src.curation.quality_gates import (
    apply_ensemble_results,
    gate_scientific_records,
    pre_screen_documents,
)
from src.curation.quality_score import score_record
from src.curation.task_candidates import generate_task_candidates
from src.curation.task_selection import deterministic_selection, select_task_types
from src.curation.toolbox import assess_toolbox_coverage, load_toolbox_profile
from src.delivery.agent_pilot import run_agent_pilot
from src.delivery.build import build_dataset
from src.delivery.reference_run import attach_reference_runs, execute_reference_run
from src.delivery.smoke import run_mock_task
from src.delivery.validate import validate_dataset
from src.discovery.corpus_classify import classify_corpus_documents
from src.discovery.query import expand_seeds
from src.discovery.seed_audit import audit_seed_coverage
from src.ingestion.corpus import inventory_corpus
from src.ingestion.dedupe import deduplicate
from src.ingestion.deep_parse import build_mineru_queue
from src.ingestion.deep_quality import assess_deep_parse_quality
from src.ingestion.grobid import extract_documents_with_grobid, parse_grobid_tei
from src.ingestion.study_bundle import build_study_bundles
from src.orchestration.pipeline import _curation_queue_item, _seedless_coverage_summary

ROOT = Path(__file__).resolve().parents[1]


class PipelineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.seeds = read_json(ROOT / "tests/fixtures/seeds.json")
        self.record = read_json(ROOT / "tests/fixtures/curation.json")

    def test_query_expansion_has_three_tiers(self) -> None:
        queries = expand_seeds(self.seeds, max_per_tier=5)
        tiers = {query["tier"] for query in queries}
        self.assertEqual(tiers, {"broad", "medium", "narrow"})
        self.assertEqual(len({query["query_id"] for query in queries}), len(queries))

    def test_compact_config_expands_all_llm_roles(self) -> None:
        compact = read_json(ROOT / "config.json")
        compact["llm"]["extraction"]["url"] = "https://extract.example/v1"
        compact["llm"]["classification"]["url"] = "https://classify.example/v1"
        compact["llm"]["generation"]["url"] = "https://generate.example/v1"
        compact["llm"]["review"]["url"] = "https://review.example/v1"
        config = normalize_config(compact, ROOT)

        self.assertEqual(config["source"]["mode"], "corpus")
        self.assertEqual(len(config["model_ensemble"]["reviewers"]), 4)
        self.assertEqual(config["semantic_review"]["base_url"], "https://extract.example/v1")
        self.assertEqual(config["task_selection"]["base_url"], "https://classify.example/v1")
        self.assertEqual(config["package_generation"]["base_url"], "https://generate.example/v1")
        self.assertEqual(
            config["model_ensemble"]["reviewers"][0]["base_url"],
            "https://review.example/v1",
        )
        self.assertEqual(
            config["package_generation"]["prompt_examples"],
            str((ROOT / "assets/prompt_examples.json").resolve()),
        )
        self.assertEqual(
            config["toolbox"]["profile"],
            str((ROOT / "assets/toolbox.json").resolve()),
        )

    def test_curation_queue_contains_unresolved_selected_task_gates(self) -> None:
        record = deepcopy(self.record)
        task_type = record["selected_task_type"]
        record["quality_funnel"] = {
            "mode_reports": {
                task_type: {
                    "decision": "review",
                    "gates": [
                        {
                            "gate_id": "G2_data_availability",
                            "name": "data availability",
                            "decision": "review",
                            "reasons": ["asset discovery pending"],
                        }
                    ],
                }
            }
        }

        item = _curation_queue_item(record)

        self.assertEqual(item["selected_task_type"], task_type)
        self.assertEqual(item["priority_rank"], 1)
        self.assertEqual(
            item["unresolved_gates"][task_type][0]["gate_id"],
            "G2_data_availability",
        )

    def test_stable_id_accepts_missing_identifiers(self) -> None:
        self.assertTrue(stable_id("paper", None, "A title").startswith("paper_"))

    def test_dedupe_preserves_query_provenance(self) -> None:
        rows = [
            {
                "title": "A Mechanistic Study",
                "doi": "10.1/example",
                "query_id": "q1",
                "seed_id": "s1",
                "query_tier": "broad",
                "retrieval_source": "offline",
            },
            {
                "title": "A mechanistic study",
                "doi": "https://doi.org/10.1/example",
                "query_id": "q2",
                "seed_id": "s1",
                "query_tier": "narrow",
                "retrieval_source": "openalex",
            },
        ]
        papers = deduplicate(rows)
        self.assertEqual(len(papers), 1)
        self.assertEqual(set(papers[0]["query_ids"]), {"q1", "q2"})
        self.assertEqual(set(papers[0]["query_tiers"]), {"broad", "narrow"})

    def test_quality_gates_pass_curated_record(self) -> None:
        mode = self.record["selected_task_type"]
        report = score_record(self.record, mode)
        self.assertTrue(report["passed"], report)
        self.assertGreaterEqual(report["score"], report["threshold"])

    def test_toolbox_selection_is_configurable_and_preserves_priority_software(self) -> None:
        profile = load_toolbox_profile(
            ROOT / "assets/toolbox.json",
            {
                "enabled_software": ["gaussian"],
                "enabled_actions": ["calculate_excited_states"],
                "priority_software": ["gaussian"],
                "preserve_priority_matches": True,
            },
        )
        coverage = assess_toolbox_coverage(self.record, profile)
        self.assertIn("gaussian", coverage["directly_available"])
        self.assertIn("gaussian", coverage["priority_matches"])
        self.assertNotIn("rdkit", coverage["directly_available"])
        self.assertEqual(profile["selection"]["enabled_software"], ["gaussian"])

    def test_full_quality_funnel_reviews_missing_reference_run(self) -> None:
        profile = load_toolbox_profile(
            ROOT / "assets/toolbox.json",
            {"enabled_software": ["*"], "enabled_actions": ["*"], "priority_software": ["*"]},
        )
        record = {
            **self.record,
            "schema_validation": {"passed": True, "errors": []},
            "assets": {"visible_data": {}, "text": [], "supplementary": []},
        }
        gated = gate_scientific_records([record], profile)[0]
        self.assertEqual(gated["quality_funnel"]["review_task_types"], ["autonomous_research"])
        report = gated["quality_funnel"]["mode_reports"]["autonomous_research"]
        self.assertIn("G5_reference_run", report["review_gates"])
        self.assertEqual(gated["toolbox_coverage"]["direct_coverage"], 1.0)

    def test_described_inputs_are_not_treated_as_materialized(self) -> None:
        profile = load_toolbox_profile(
            ROOT / "assets/toolbox.json",
            {"enabled_software": ["*"], "enabled_actions": ["*"], "priority_software": ["*"]},
        )
        record = deepcopy(self.record)
        record["inputs"] = [
            {
                "name": "described structure",
                "description": "The paper mentions a starting structure.",
                "verification_status": "described",
            }
        ]
        record["assets"] = {"visible_data": {}, "text": [], "supplementary": []}
        record["benchmark_package"]["public_inputs"] = {"observations": []}
        gated = gate_scientific_records([record], profile)[0]
        report = gated["quality_funnel"]["mode_reports"][record["selected_task_type"]]
        data_gate = next(
            gate for gate in report["gates"] if gate["gate_id"] == "G2_data_availability"
        )
        self.assertEqual(data_gate["decision"], "review")
        self.assertEqual(data_gate["evidence"]["materialized_input_count"], 0)

    def test_primary_computational_paper_without_cheap_task_match_goes_to_review(self) -> None:
        document = {
            "paper_id": "doc_primary",
            "title": "Computational study",
            "text_quality": {"score": 90},
            "corpus_classification": {
                "relevance_decision": "pass",
                "relevance_score": 90,
                "computational_role": "primary",
                "eligible_task_types": [],
                "constructability_scores": {},
                "software": ["ORCA"],
                "methods": ["DFT"],
            },
        }
        profile = load_toolbox_profile(
            ROOT / "assets/toolbox.json",
            {"enabled_software": ["*"], "enabled_actions": ["*"], "priority_software": ["*"]},
        )
        screened = pre_screen_documents([document], profile)[0]
        gate = next(
            item
            for item in screened["pre_extraction_quality"]["gates"]
            if item["gate_id"] == "P2_task_extractability"
        )
        self.assertEqual(gate["decision"], "review")
        self.assertNotEqual(screened["pre_extraction_quality"]["decision"], "reject")

    def test_pdf_only_asset_signal_is_pending_acquisition_not_unavailable(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            text_path = Path(directory) / "paper.txt"
            text_path.write_text(
                "Data Availability Statement\nInput files are available on GitHub at "
                "https://github.com/example/research-data.",
                encoding="utf-8",
            )
            record = deepcopy(self.record)
            record["assets"] = {"text": [str(text_path)], "visible_data": {}}
            availability = assess_asset_availability(record)
            self.assertEqual(availability["availability_state"], "pending_acquisition")
            self.assertFalse(availability["release_blocking"])
            self.assertIn(
                "https://github.com/example/research-data", availability["repository_urls"]
            )

    def test_pdf_url_repair_does_not_append_sentence_words(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            text_path = Path(directory) / "paper.txt"
            text_path.write_text(
                "Data are available at https://github.com/example/repo. Results follow.\n"
                "Mirror: https://www.plumed-nest. org/eggs/24/017/.",
                encoding="utf-8",
            )
            record = deepcopy(self.record)
            record["assets"] = {"text": [str(text_path)], "visible_data": {}}
            urls = assess_asset_availability(record)["candidate_urls"]
            self.assertIn("https://github.com/example/repo", urls)
            self.assertIn("https://www.plumed-nest.org/eggs/24/017/", urls)
            self.assertFalse(any("Results" in url for url in urls))

    def test_bare_repository_doi_in_availability_context_becomes_candidate_url(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            text_path = Path(directory) / "paper.txt"
            text_path.write_text(
                "Input scripts are available through Zenodo: http://10.5281/zenodo.10127153.",
                encoding="utf-8",
            )
            record = deepcopy(self.record)
            record["assets"] = {"text": [str(text_path)], "visible_data": {}}
            availability = assess_asset_availability(record)
            self.assertIn(
                "https://doi.org/10.5281/zenodo.10127153",
                availability["candidate_urls"],
            )
            self.assertEqual(availability["availability_state"], "pending_acquisition")

    def test_confirmed_unavailable_requires_explicit_acquisition_status(self) -> None:
        record = deepcopy(self.record)
        record["assets"] = {
            "text": [],
            "visible_data": {},
            "acquisition": {"status": "confirmed_unavailable", "discovery_completed": True},
        }
        availability = assess_asset_availability(record)
        self.assertEqual(availability["availability_state"], "confirmed_unavailable")
        self.assertTrue(availability["release_blocking"])

    def test_pending_asset_veto_is_downgraded_for_tool_data_reviewer(self) -> None:
        record = deepcopy(self.record)
        record["asset_availability"] = {"availability_state": "pending_acquisition"}
        record["toolbox_coverage"] = {"coverage_state": "mapped_pending_functional_validation"}
        verdict = {
            "reviewer": "judge",
            "role": "tool_data_feasibility",
            "source": "offline_file",
            "decision": "reject",
            "score": 40,
            "confidence": 0.9,
            "dimensions": {},
            "issues": ["files have not been downloaded"],
            "vetoes": ["data_unavailable", "tool_unavailable"],
            "evidence_refs": ["asset_availability"],
        }
        reconciled = _reconcile_candidate_verdict(verdict, record)
        self.assertEqual(reconciled["decision"], "review")
        self.assertEqual(reconciled["vetoes"], [])

    def test_file_descriptions_are_not_valid_public_files(self) -> None:
        record = deepcopy(self.record)
        package = record["benchmark_package"]
        package["public_inputs"]["files"] = {
            "missing.csv": "CSV file with columns: molecule_id, energy."
        }
        report = package_readiness(record, record["selected_task_type"])
        self.assertFalse(report["passed"])
        self.assertTrue(
            any("description rather than file content" in error for error in report["errors"])
        )

    def test_structured_method_objects_are_supported_by_toolbox_mapping(self) -> None:
        profile = load_toolbox_profile(
            ROOT / "assets/toolbox.json",
            {"enabled_software": ["*"], "enabled_actions": ["*"], "priority_software": ["*"]},
        )
        record = deepcopy(self.record)
        record["methods"] = [
            {"method_name": "DFT", "parameters": {"functional": "PBE0"}},
            {"description": "molecular dynamics sampling"},
        ]
        coverage = assess_toolbox_coverage(record, profile)
        self.assertIn("calculate_energy", coverage["requested_actions"])
        self.assertIn("propagate_dynamics", coverage["requested_actions"])

    def test_method_program_names_are_included_in_toolbox_coverage(self) -> None:
        profile = load_toolbox_profile(
            ROOT / "assets/toolbox.json",
            {"enabled_software": ["*"], "enabled_actions": ["*"], "priority_software": ["*"]},
        )
        record = deepcopy(self.record)
        record["tools"] = []
        record["source_classification"] = {"software": [], "methods": []}
        record["methods"] = [
            {"name": "CREST", "description": "GFN2-xTB conformer sampling"},
            {"name": "CENSO"},
            {"description": "Enhanced sampling with PLUMED and GROMACS"},
        ]
        coverage = assess_toolbox_coverage(record, profile)
        self.assertTrue(
            {"crest", "xtb", "censo", "plumed", "gromacs"}.issubset(
                set(coverage["required_software"])
            )
        )

    def test_model_review_packet_separates_solver_visible_and_hidden_fields(self) -> None:
        packet = _review_packet(self.record, self.record["selected_task_type"])
        self.assertNotIn("ground_truth", packet["solver_visible_package"])
        self.assertIn("ground_truth", packet["reviewer_only_hidden_reference"])
        self.assertFalse(packet["visibility_policy"]["paper_pdf_visible_to_solver"])

    def test_multi_model_consensus_supports_offline_independent_verdicts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            record = {
                **self.record,
                "task_candidates": generate_task_candidates(self.record),
                "quality_funnel": {
                    "status": "deterministic_complete",
                    "mode_reports": {
                        "autonomous_research": {
                            "decision": "pass",
                            "gates": [],
                            "blocking_gates": [],
                            "review_gates": [],
                        }
                    },
                },
                "selected_task_type": "autonomous_research",
            }
            reviewers = []
            for index, score in enumerate((88, 91, 86), start=1):
                name = f"judge_{index}"
                reviewers.append(
                    {"name": name, "role": "independent", "offline_verdict_dir": str(root)}
                )
                write_json(
                    root / f"{record['paper_id']}__autonomous_research__{name}.json",
                    {
                        "decision": "pass",
                        "score": score,
                        "confidence": 0.9,
                        "dimensions": {
                            "scientific_grounding": score,
                            "tool_and_data_feasibility": score,
                            "question_clarity": score,
                            "difficulty_and_nontriviality": score,
                            "evaluation_verifiability": score,
                            "leakage_resistance": score,
                        },
                        "issues": [],
                        "vetoes": [],
                        "evidence_refs": ["question", "evidence"],
                    },
                )
            reviewed = review_with_ensemble(
                [record],
                {
                    "enabled": True,
                    "minimum_completed_reviewers": 3,
                    "reviewers": reviewers,
                },
            )
            reviewed = apply_ensemble_results(reviewed)[0]
            consensus = reviewed["model_ensemble"]["mode_reviews"]["autonomous_research"]
            self.assertEqual(consensus["decision"], "pass")
            self.assertEqual(
                reviewed["quality_funnel"]["mode_reports"]["autonomous_research"]["decision"],
                "pass",
            )

    def test_visibility_policy(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            manifest = build_dataset([self.record], directory)
            autonomous = Path(directory) / manifest["tasks"][0]["path"] / "data" / "benchmark_data"
            self.assertFalse((autonomous / "method_protocol.json").exists())
            public_text = "\n".join(
                path.read_text(encoding="utf-8") for path in autonomous.rglob("*") if path.is_file()
            )
            self.assertNotIn("102.8", public_text)
            self.assertNotIn("0.0567", public_text)

    def test_build_and_validate_exactly_one_task(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            manifest = build_dataset([self.record], directory)
            self.assertEqual(manifest["task_count"], 1)
            self.assertEqual(manifest["tasks"][0]["task_type"], "autonomous_research")
            self.assertTrue(
                all(Path(item["path"]).name == item["task_id"] for item in manifest["tasks"])
            )
            report = validate_dataset(directory)
            self.assertTrue(report["passed"], report)
            self.assertTrue(all(item["workspace_smoke"]["passed"] for item in report["tasks"]))
            self.assertTrue(all(item["chemistry_validation"]["passed"] for item in report["tasks"]))

    def test_empty_dataset_is_not_release_valid_by_default(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            build_dataset([], directory)
            report = validate_dataset(directory, run_workspace_smoke=False)
            self.assertFalse(report["passed"])
            self.assertIn("dataset contains no constructed tasks", report["errors"])
            self.assertTrue(
                validate_dataset(directory, run_workspace_smoke=False, require_tasks=False)[
                    "passed"
                ]
            )

    def test_complete_package_gate_rejects_question_only_record(self) -> None:
        incomplete = {
            key: value for key, value in self.record.items() if key != "benchmark_package"
        }
        report = package_readiness(incomplete, incomplete["selected_task_type"])
        self.assertFalse(report["passed"])
        self.assertIn("missing benchmark_package curation", report["errors"])

    def test_offline_package_generation_promotes_only_complete_candidate(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = {
                key: value for key, value in self.record.items() if key != "benchmark_package"
            }
            write_json(root / f"{source['paper_id']}.json", self.record["benchmark_package"])
            generated = generate_complete_packages(
                [source],
                {"enabled": True, "offline_package_dir": str(root)},
            )[0]
            self.assertEqual(generated["package_generation"]["status"], "complete")
            self.assertIn("benchmark_package", generated)
            self.assertTrue(generated["package_generation"]["validation"]["passed"])

    def test_manifest_tampering_is_detected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            manifest = build_dataset([self.record], directory)
            task = Path(directory) / manifest["tasks"][0]["path"]
            reaction = task / "data" / "benchmark_data" / "reaction.json"
            reaction.write_text("{}\n", encoding="utf-8")
            report = validate_dataset(directory, run_workspace_smoke=False)
            self.assertFalse(report["passed"])
            self.assertTrue(
                any("sha256 mismatch: reaction.json" in error for error in report["errors"])
            )

    def test_hidden_marker_in_public_package_blocks_build(self) -> None:
        leaked = read_json(ROOT / "tests/fixtures/curation.json")
        leaked["benchmark_package"]["public_inputs"]["files"]["leak.txt"] = "hidden target 102.8"
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaisesRegex(ValueError, "leaks hidden markers"):
                build_dataset([leaked], directory)

    def test_rebuilding_same_output_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            build_dataset([self.record], directory)
            build_dataset([self.record], directory)
            report = validate_dataset(directory)
            self.assertTrue(report["passed"], report)

    def test_real_benchmark_mock_agent_runs_staged_task(self) -> None:
        with (
            tempfile.TemporaryDirectory() as directory,
            tempfile.TemporaryDirectory() as workspaces,
        ):
            manifest = build_dataset([self.record], directory)
            task = manifest["tasks"][0]
            result = run_mock_task(Path(directory) / task["path"], workspaces)
            self.assertTrue(result["passed"], result)
            self.assertEqual(result["status"], "completed")
            self.assertFalse(result["hidden_ground_truth_exposed"])

    def test_agent_pilot_requires_real_scores_before_filtering(self) -> None:
        with (
            tempfile.TemporaryDirectory() as directory,
            tempfile.TemporaryDirectory() as workspaces,
        ):
            manifest = build_dataset([self.record], directory)
            task = manifest["tasks"][0]
            result = run_agent_pilot(
                Path(directory) / task["path"],
                workspaces,
                {"score": False, "agents": [{"agent_key": "mock", "repeats": 1}]},
            )
            self.assertEqual(result["summary"]["decision"], "incomplete_no_valid_scores")
            self.assertEqual(result["summary"]["completed_runs"], 1)

    def test_corpus_classifier_separates_primary_computation_from_negative(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            computational_text = root / "computational.txt"
            computational_text.write_text(
                """Reaction mechanism by density functional theory. Abstract We performed DFT calculations with Gaussian 16 to identify transition states and activation barriers. Introduction. Computational Methods. Geometry optimization and frequency calculations used the B3LYP functional and def2-SVP basis set with a solvation model. Intrinsic reaction coordinate calculations validated each transition state. Gaussian DFT Gaussian DFT. Free energy barriers distinguish two reaction pathways. Supporting Information and code availability are provided in a repository.""",
                encoding="utf-8",
            )
            experimental_text = root / "experimental.txt"
            experimental_text.write_text(
                """A practical copper-catalyzed synthesis. Abstract We report substrate scope, isolated yields, NMR characterization, and catalyst loading experiments. Materials and Methods. Reagents were combined under nitrogen, purified by chromatography, and characterized by NMR and mass spectrometry.""",
                encoding="utf-8",
            )
            rows = classify_corpus_documents(
                [
                    {
                        "document_id": "doc_comp",
                        "paper_id": "doc_comp",
                        "title": "Reaction mechanism by density functional theory",
                        "abstract": "We performed DFT calculations with Gaussian 16 to identify transition states and activation barriers.",
                        "section_headings": ["Computational Methods", "Results"],
                        "text_path": str(computational_text),
                        "text_quality": {"needs_ocr": False},
                    },
                    {
                        "document_id": "doc_exp",
                        "paper_id": "doc_exp",
                        "title": "A practical copper-catalyzed synthesis",
                        "abstract": "An experimental synthetic chemistry study.",
                        "section_headings": ["Materials and Methods", "Results"],
                        "text_path": str(experimental_text),
                        "text_quality": {"needs_ocr": False},
                    },
                ]
            )
            self.assertEqual(rows[0]["corpus_classification"]["relevance_decision"], "pass")
            self.assertIn(
                "paper_reproduction", rows[0]["corpus_classification"]["eligible_task_types"]
            )
            self.assertEqual(
                set(rows[0]["corpus_classification"]["task_suitability_scores"]),
                {
                    "paper_reproduction",
                    "conclusion_guided_reconstruction",
                    "autonomous_research",
                    "mechanistic_rule_discovery",
                },
            )
            self.assertEqual(rows[1]["corpus_classification"]["relevance_decision"], "reject")

    def test_mineru_queue_and_seed_audit_are_advisory(self) -> None:
        document = {
            "document_id": "doc_new",
            "paper_id": "doc_new",
            "source_path": "/tmp/new.pdf",
            "title": "Solid-state band structure dataset",
            "abstract": "A VASP dataset for materials property prediction.",
            "corpus_classification": {
                "relevance_decision": "pass",
                "deep_parse_decision": "required",
                "constructability_scores": {"paper_reproduction": 70},
                "eligible_modes": ["paper_reproduction"],
                "domains": ["materials_solid_state"],
                "methods": ["DFT"],
                "software": ["VASP"],
            },
        }
        audited, summary = audit_seed_coverage([document], self.seeds, match_threshold=0.5)
        self.assertEqual(audited[0]["seed_guidance"]["coverage_role"], "new_capability_candidate")
        self.assertEqual(summary["new_capability_documents"], 1)
        self.assertEqual(len(build_mineru_queue(audited)), 1)

    def test_study_bundle_groups_main_text_and_supplement_before_extraction(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "study"
            main = root / "paper" / "paper.pdf"
            si = root / "supplementary" / "Supplementary_Information.pdf"
            main.parent.mkdir(parents=True)
            si.parent.mkdir(parents=True)
            main.write_bytes(b"main")
            si.write_bytes(b"si")
            documents = [
                {
                    "paper_id": "main",
                    "source_path": str(main),
                    "title": "Computational reaction study",
                    "corpus_classification": {"relevance_score": 80},
                    "pre_extraction_quality": {"decision": "pass"},
                },
                {
                    "paper_id": "si",
                    "source_path": str(si),
                    "title": "Microsoft Word - SI.docx",
                    "corpus_classification": {"relevance_score": 90},
                    "pre_extraction_quality": {"decision": "pass"},
                },
            ]
            bundles = build_study_bundles(documents)
            self.assertEqual(len(bundles), 1)
            self.assertEqual(bundles[0]["primary_paper_id"], "main")
            self.assertEqual(set(bundles[0]["member_paper_ids"]), {"main", "si"})
            self.assertEqual(len(bundles[0]["supplementary_paths"]), 1)

    def test_mineru_queue_skips_low_cost_rejections(self) -> None:
        rejected = {
            "document_id": "doc",
            "paper_id": "doc",
            "source_path": "/tmp/doc.pdf",
            "pre_extraction_quality": {"decision": "reject"},
            "corpus_classification": {
                "deep_parse_decision": "required",
                "constructability_scores": {"paper_reproduction": 100},
            },
        }
        self.assertEqual(build_mineru_queue([rejected]), [])

    def test_seedless_summary_is_recomputed_after_ocr_reclassification(self) -> None:
        documents = [
            {"paper_id": "recovered", "corpus_classification": {"relevance_decision": "pass"}},
            {"paper_id": "negative", "corpus_classification": {"relevance_decision": "reject"}},
        ]
        summary = _seedless_coverage_summary(documents)
        self.assertEqual(summary["seed_count"], 0)
        self.assertEqual(summary["new_capability_documents"], 1)

    def test_grobid_tei_parser_extracts_structured_metadata(self) -> None:
        tei = """<?xml version="1.0" encoding="UTF-8"?>
<TEI xmlns="http://www.tei-c.org/ns/1.0" xml:lang="en">
  <teiHeader>
    <fileDesc>
      <titleStmt><title level="a" type="main">A Structured Chemistry Paper</title></titleStmt>
      <publicationStmt><publisher>Example Publisher</publisher></publicationStmt>
      <sourceDesc>
        <biblStruct>
          <analytic>
            <author role="corresp"><persName><forename>Jane</forename><surname>Doe ∇</surname></persName><idno type="ORCID">0000-0001</idno><affiliation><orgName>Example University</orgName></affiliation></author>
            <author><persName><surname>Wt</surname></persName></author>
            <idno type="DOI">10.1000/example</idno>
          </analytic>
          <monogr><title level="j">Journal of Structured Chemistry</title><imprint><date type="published" when="2024-05-02"/><biblScope unit="volume">12</biblScope><biblScope unit="issue">3</biblScope><biblScope unit="page" from="101" to="110"/></imprint></monogr>
        </biblStruct>
      </sourceDesc>
    </fileDesc>
    <profileDesc><abstract><p>This paper reports a structured computational chemistry result.</p></abstract><textClass><keywords><term>density functional theory</term></keywords></textClass></profileDesc>
  </teiHeader>
  <text><body><div><head>Introduction</head><p>Body text.</p><figure><head>Figure 1. Workflow</head></figure></div><div><head>Methods</head><p>Method text.</p></div><div><head>By studying these</head><p>systems we obtain a complete sentence.</p></div></body></text>
</TEI>"""
        parsed = parse_grobid_tei(tei)
        self.assertEqual(parsed["title"], "A Structured Chemistry Paper")
        self.assertEqual(
            parsed["abstract"], "This paper reports a structured computational chemistry result."
        )
        self.assertEqual(parsed["authors"], ["Jane Doe"])
        self.assertEqual(parsed["doi"], "10.1000/example")
        self.assertEqual(parsed["publication_date"], "2024-05-02")
        self.assertEqual(parsed["year"], 2024)
        self.assertEqual(parsed["venue"], "Journal of Structured Chemistry")
        self.assertEqual(parsed["volume"], "12")
        self.assertEqual(parsed["issue"], "3")
        self.assertEqual(parsed["article_pages"], "101-110")
        self.assertEqual(parsed["section_headings"], ["Introduction", "Methods"])

    def test_grobid_tei_parser_drops_citation_heavy_intro_from_abstract(self) -> None:
        first = "A" * 650
        tei = f"""<TEI xmlns="http://www.tei-c.org/ns/1.0"><teiHeader><fileDesc><titleStmt><title type="main">Paper</title></titleStmt><sourceDesc><biblStruct/></sourceDesc></fileDesc><profileDesc><abstract><p>{first}</p><p>Prior work established this result <ref type="bibr">1</ref>.</p></abstract></profileDesc></teiHeader><text><body/></text></TEI>"""
        parsed = parse_grobid_tei(tei)
        self.assertEqual(parsed["abstract"], first)

    def test_grobid_extraction_excludes_duplicate_inventory_rows(self) -> None:
        tei = """<TEI xmlns="http://www.tei-c.org/ns/1.0"><teiHeader><fileDesc><titleStmt><title type="main">Canonical Paper</title></titleStmt><sourceDesc><biblStruct/></sourceDesc></fileDesc><profileDesc><abstract><p>A sufficiently descriptive abstract for the canonical document.</p></abstract></profileDesc></teiHeader><text><body><div><head>Methods</head><p>Computational text.</p></div></body></text></TEI>"""

        class FakeClient:
            def __init__(self) -> None:
                self.calls = 0

            def process_fulltext_document(self, _path: str) -> str:
                self.calls += 1
                return tei

        inventory = [
            {
                "document_id": "doc_same",
                "paper_id": "doc_same",
                "source_path": "/tmp/canonical.pdf",
                "file_name": "canonical.pdf",
                "page_count": 1,
                "duplicate_of": None,
            },
            {
                "document_id": "doc_same",
                "paper_id": "doc_same",
                "source_path": "/tmp/duplicate.pdf",
                "file_name": "duplicate.pdf",
                "page_count": 1,
                "duplicate_of": "doc_same",
            },
            {
                "document_id": "doc_supplement",
                "paper_id": "doc_supplement",
                "source_path": "/tmp/supplementary/SI.pdf",
                "file_name": "SI.pdf",
                "page_count": 1,
                "duplicate_of": None,
                "document_role": "supplementary",
            },
        ]
        client = FakeClient()
        with tempfile.TemporaryDirectory() as directory:
            rows = extract_documents_with_grobid(
                inventory,
                client,
                Path(directory) / "tei",
                Path(directory) / "text",
            )
        self.assertEqual(len(rows), 1)
        self.assertEqual(client.calls, 1)
        self.assertEqual(rows[0]["title"], "Canonical Paper")
        self.assertIsNone(rows[0].get("duplicate_of"))

    def test_inventory_records_duplicate_owner_path_for_stage_one_audit(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "a.pdf").write_bytes(b"same-pdf-content")
            (root / "b.pdf").write_bytes(b"same-pdf-content")
            supplementary = root / "supplementary"
            supplementary.mkdir()
            (supplementary / "SI.pdf").write_bytes(b"supplementary-content")
            rows = inventory_corpus(root)
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0]["inventory_status"], "canonical")
        self.assertEqual(rows[1]["inventory_status"], "duplicate")
        self.assertEqual(rows[1]["duplicate_of"], rows[0]["document_id"])
        self.assertEqual(rows[1]["duplicate_of_source_path"], rows[0]["source_path"])
        self.assertEqual(rows[0]["document_role"], "main_paper")
        self.assertEqual(rows[2]["document_role"], "supplementary")

    def test_rejected_paper_is_out_of_scope_for_seed_coverage(self) -> None:
        document = {
            "document_id": "doc_exp",
            "paper_id": "doc_exp",
            "title": "Experimental reaction mechanism study",
            "abstract": "A synthesis paper with transition-state terminology.",
            "corpus_classification": {
                "relevance_decision": "reject",
                "domains": ["reaction_mechanism"],
                "methods": ["transition_state"],
                "software": [],
            },
        }
        audited, summary = audit_seed_coverage([document], self.seeds)
        self.assertEqual(audited[0]["seed_guidance"]["coverage_role"], "out_of_scope")
        self.assertEqual(summary["covered_documents"], 0)

    def test_cached_text_prevents_duplicate_pdf_parsing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fake_pdf = root / "paper.pdf"
            fake_pdf.write_text("not a real PDF", encoding="utf-8")
            cached = root / "paper.txt"
            cached.write_text("Cached computational methods text.", encoding="utf-8")
            text, provenance = collect_text(
                {"title": "Test", "abstract": "", "retrieval_sources": [], "paper_id": "p1"},
                {
                    "paper": str(fake_pdf),
                    "text": [str(cached)],
                    "prefer_text_assets": True,
                },
            )
            self.assertIn("Cached computational methods text.", text)
            self.assertEqual(provenance[1]["status"], "referenced")

    def test_deep_parse_quality_accepts_complete_output(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            cheap = root / "cheap.txt"
            deep = root / "deep.md"
            text = (
                "A VASP density functional theory dataset. "
                "Methods use VASP for DFT calculations and validation. "
            ) * 30
            cheap.write_text(text, encoding="utf-8")
            deep.write_text(
                "# A VASP density functional theory dataset\n\n" + text, encoding="utf-8"
            )
            rows = assess_deep_parse_quality(
                [
                    {
                        "paper_id": "p1",
                        "title": "A VASP density functional theory dataset",
                        "page_count": 2,
                        "text_path": str(cheap),
                        "corpus_classification": {
                            "software": ["VASP"],
                            "methods": ["DFT"],
                        },
                    }
                ],
                [
                    {
                        "paper_id": "p1",
                        "status": "success",
                        "valid": True,
                        "markdown_path": str(deep),
                        "structured_pages": 2,
                    }
                ],
            )
            self.assertTrue(rows[0]["deep_parse_quality"]["passed"])

    def test_each_task_type_has_a_dedicated_prompt_example(self) -> None:
        for task_type in TASK_TYPES:
            example = prompt_example(task_type)
            prompt = generation_prompt(task_type)
            self.assertIsInstance(example, str)
            self.assertGreater(len(example), 200)
            self.assertIn(f"type {task_type}", prompt)
            self.assertIn("Complete structural example", prompt)
            self.assertIn("3-10 ScoredFinding", prompt)

    def test_deterministic_selection_prefers_rich_cross_system_rule_data(self) -> None:
        record = {
            "paper_id": "rule-rich",
            "central_problem": "Infer a mechanistic descriptor across a catalyst series and predict held-out systems.",
            "inputs": [{"systems": 12}],
            "expected_outputs": ["rule", "held-out predictions"],
            "methods": ["DFT"],
            "workflow": [],
            "evidence": [{"statement": "trend"}] * 5,
            "reference_results": ["descriptor relationship"],
            "hypotheses": [],
            "information_richness": {"comparable_system_count": 12},
            "source_classification": {
                "task_suitability_scores": {
                    "paper_reproduction": 25,
                    "conclusion_guided_reconstruction": 35,
                    "autonomous_research": 30,
                    "mechanistic_rule_discovery": 80,
                }
            },
        }
        result = deterministic_selection(record)
        self.assertEqual(result["selected_task_type"], "mechanistic_rule_discovery")
        selected = select_task_types([record], {"enabled": False})[0]
        self.assertNotIn("task_modes", selected)
        self.assertEqual(len(selected["rejected_task_types"]), 3)

    def test_runtime_tiers_use_measured_walltime_boundaries(self) -> None:
        self.assertEqual(runtime_tier(0.5), "short")
        self.assertEqual(runtime_tier(1), "short")
        self.assertEqual(runtime_tier(2.5), "medium")
        self.assertEqual(runtime_tier(4), "medium")
        self.assertEqual(runtime_tier(4.01), "long_challenge")
        self.assertEqual(runtime_tier(None), "unknown")

    def test_reference_run_manifest_validates_artifacts_and_sets_runtime_tier(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            artifact = root / "result.json"
            artifact.write_text('{"energy": -1.0}\n', encoding="utf-8")
            record = {
                **self.record,
                "reference_run": {
                    "command": "rcb-tool run reference.inp",
                    "exit_code": 0,
                    "measured_walltime_hours": 2.5,
                    "cpu_cores": 8,
                    "artifacts": [{"path": str(artifact)}],
                },
            }
            updated = attach_reference_runs([record])[0]
            self.assertEqual(updated["reference_run"]["status"], "validated")
            self.assertEqual(updated["runtime"]["runtime_tier"], "medium")
            self.assertEqual(updated["runtime"]["cpu_core_hours"], 20.0)

    def test_reference_runner_executes_without_shell_and_hashes_outputs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result = execute_reference_run(
                {
                    "command": [
                        sys.executable,
                        "-c",
                        "from pathlib import Path; Path('energy.json').write_text('{\\\"energy\\\": -1.0}\\n')",
                    ],
                    "cwd": str(root),
                    "artifacts": ["energy.json"],
                    "cpu_cores": 1,
                    "timeout_seconds": 30,
                }
            )
            self.assertEqual(result["status"], "validated")
            self.assertEqual(result["exit_code"], 0)
            self.assertTrue(result["artifacts"][0]["sha256"])

    def test_four_internal_task_types_fit_parent_benchmark_contract(self) -> None:
        records = []
        source_package = self.record["benchmark_package"]
        for index, task_type in enumerate(TASK_TYPES):
            record = deepcopy(self.record)
            record["paper_id"] = f"compat-{index}"
            record["selected_task_type"] = task_type
            record["rejected_task_types"] = [value for value in TASK_TYPES if value != task_type]
            record["selection_reason"] = (
                f"Compatibility fixture selects {task_type} using rich source evidence."
            )
            record["information_richness"] = {"comparable_system_count": 8}
            record["benchmark_package"] = {
                "task_id": f"Compatibility_{index}_{task_type}",
                "task_instruction": source_package["task_instructions"]["autonomous_research"],
                "scientific_requirements": source_package["scientific_requirements"][
                    "autonomous_research"
                ],
                "public_inputs": deepcopy(source_package["public_inputs"]),
                "leakage_markers": source_package["leakage_markers"]["autonomous_research"],
                "ground_truth": deepcopy(source_package["ground_truth"]),
            }
            if task_type == "paper_reproduction":
                record["benchmark_package"]["method_protocol"] = deepcopy(
                    source_package["method_protocol"]
                )
            elif task_type == "conclusion_guided_reconstruction":
                record["benchmark_package"]["public_inputs"]["target_conclusion"] = (
                    "The disclosed pathway is favored."
                )
            elif task_type == "mechanistic_rule_discovery":
                record["benchmark_package"]["public_inputs"]["training_systems"] = [
                    {"system_id": "A"},
                    {"system_id": "B"},
                    {"system_id": "C"},
                ]
                record["benchmark_package"]["public_inputs"]["heldout_systems"] = [
                    {"system_id": "D"}
                ]
                record["benchmark_package"]["heldout_design"] = {"outcomes_hidden": True}
                record["benchmark_package"]["ground_truth"]["expected_result"][
                    "heldout_predictions"
                ] = [{"system_id": "D", "outcome": "reference"}]
            records.append(record)
        with tempfile.TemporaryDirectory() as directory:
            manifest = build_dataset(records, directory)
            self.assertEqual(manifest["task_count"], 4, manifest["skipped"])
            by_type = {item["task_type"]: item for item in manifest["tasks"]}
            self.assertEqual(
                by_type["paper_reproduction"]["benchmark_task_mode"], "guided_reproduction"
            )
            for task_type in set(TASK_TYPES) - {"paper_reproduction"}:
                self.assertEqual(by_type[task_type]["benchmark_task_mode"], "open_discovery")
            self.assertTrue(validate_dataset(directory)["passed"])


if __name__ == "__main__":
    unittest.main()
