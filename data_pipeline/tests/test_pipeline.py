from __future__ import annotations

import contextlib
import json
from pathlib import Path

import pytest

import src.pipeline as pipeline_module
import src.stages.stage01_document_preparation.normalization as normalization_module
import src.stages.stage04_mineru_normalization.stage as stage04_module
from src.config import load_config
from src.contracts import write_jsonl
from src.integrations.llm_client import _parse_json_object
from src.model_client import DEFAULT_REMOTE_API_PROXY, RoleModelClient
from src.pipeline import (
    _apply_sandbox,
    _microbatch_stage_hashes,
    _preserve_screening_worker,
    _softcite_service,
    run_pipeline,
)
from src.stages.stage01_document_preparation.normalization import _normalize_non_pdf, _paper_quality
from src.stages.stage01_document_preparation.stage import run_stage01
from src.stages.stage02_computational_content.stage import (
    _call_complete_json,
    _chunks,
    _compact_chunk_review,
    _find_deterministic_author_experiments,
    _is_atomic_coordinate_dump,
    _is_explicit_author_laboratory_evidence,
    _is_stage02_eligible,
    _non_original_article_guard,
    _reduce_evidence_packet,
    _sanitize_reduce_response,
    _validate_experiment_map,
    _validate_map,
    run_stage02,
)
from src.stages.stage03_toolbox_resource_gate.stage import (
    _bind_workflow_steps_to_mentions,
    _bound_prompt_packet,
    _call_complete_inventory,
    _combine_decision,
    _compact_softcite_mentions,
    _inventory_contract_errors,
    _looks_like_nonsoftware_name,
    _merge_catalog_actual_use_mentions,
    _merge_detection_aliases,
    _merge_explicit_executable_cues,
    _merge_workflow_software_mentions,
    _normalize_inventory_contract,
    _repair_inventory_contract,
    _safe_output_tokens,
    _sanitize_review,
    _softcite_mentions,
    _target_blocks,
    coverage_gate,
    find_explicit_executable_cues,
    find_software_mentions,
    resolve_software,
    resource_gate,
    run_stage03,
)
from src.stages.stage05_benchmark_suitability.stage import (
    _response_contract_rejections,
    _software_coverage_facts,
    _software_fact_contradictions,
    _validate_candidates,
    _without_evidence_ids,
)
from src.stages.stage06_task_builder.stage import _public_builder_packet


def test_config_enforces_shared_screening_role(tmp_path: Path) -> None:
    config = _base_config(tmp_path)
    config["stage03"]["model_role"] = "suitability"
    path = tmp_path / "config.json"
    path.write_text(json.dumps(config), encoding="utf-8")

    with pytest.raises(ValueError, match="stage03.model_role must be screening"):
        load_config(path)


def test_managed_worker_preservation_requires_explicit_boolean(tmp_path: Path) -> None:
    assert not _preserve_screening_worker({})
    assert _preserve_screening_worker({"preserve_worker_on_exit": True})

    config = _base_config(tmp_path)
    config["models"]["screening"]["preserve_worker_on_exit"] = "yes"
    path = tmp_path / "config.json"
    path.write_text(json.dumps(config), encoding="utf-8")

    with pytest.raises(ValueError, match="preserve_worker_on_exit must be true or false"):
        load_config(path)


def test_managed_worker_creation_policy_requires_explicit_boolean(tmp_path: Path) -> None:
    config = _base_config(tmp_path)
    config["models"]["screening"]["allow_worker_creation"] = "no"
    path = tmp_path / "config.json"
    path.write_text(json.dumps(config), encoding="utf-8")

    with pytest.raises(ValueError, match="allow_worker_creation must be true or false"):
        load_config(path)


def test_v2_config_preserves_logical_shared_storage_path(tmp_path: Path, monkeypatch) -> None:
    logical_root = tmp_path / "logical-workspace"
    logical_root.mkdir()
    config = _base_config(logical_root)
    path = logical_root / "config.json"
    path.write_text(json.dumps(config), encoding="utf-8")
    monkeypatch.setenv("PWD", str(logical_root))

    loaded = load_config("config.json")

    assert loaded["config_path"] == str(path)
    assert loaded["workspace"] == str(logical_root / "run")


def test_v2_config_rejects_invalid_per_stage_concurrency(tmp_path: Path) -> None:
    config = _base_config(tmp_path)
    config["microbatch"] = {"stage_concurrency": {"stage02": 0}}
    path = tmp_path / "config.json"
    path.write_text(json.dumps(config), encoding="utf-8")

    with pytest.raises(ValueError, match="stage02 must be at least 1"):
        load_config(path)


def test_stage03_reduce_packet_is_bounded_and_prefers_high_confidence() -> None:
    evidence = [
        {"evidence_id": "low", "confidence": "low", "exact_quote": "low quote"},
        {
            "evidence_id": "high",
            "confidence": "high",
            "exact_quote": "0123456789",
        },
        {
            "evidence_id": "medium",
            "confidence": "medium",
            "exact_quote": "medium quote",
        },
    ]

    packet = _reduce_evidence_packet(
        evidence,
        max_items=2,
        max_quote_characters=5,
    )

    assert [item["evidence_id"] for item in packet] == ["high", "medium"]
    assert packet[0]["exact_quote"] == "01234"


def test_stage03_compact_chunk_review_omits_full_model_response() -> None:
    compact = _compact_chunk_review(
        {
            "chunk_index": 3,
            "response": {
                "has_computational_evidence": True,
                "background_only_evidence": [{"explanation": "large response"}],
                "conflicts": [],
                "unneeded_free_text": "x" * 10000,
            },
            "validated_evidence": [{"evidence_id": "ev-1"}],
        }
    )

    assert compact == {
        "chunk_index": 3,
        "has_computational_evidence": True,
        "validated_evidence_count": 1,
        "validated_experiment_count": 0,
        "background_only_count": 1,
        "conflict_count": 0,
    }


def test_stage03_chunks_split_one_oversized_evidence_block() -> None:
    chunks = _chunks(
        [
            {
                "evidence_id": "ev-long",
                "document_id": "doc",
                "text": "0123456789ABCDEFGHIJabc",
            }
        ],
        10,
    )

    assert [chunk[0]["text"] for chunk in chunks] == ["0123456789", "ABCDEFGHIJ", "abc"]
    assert all(chunk[0]["evidence_id"] == "ev-long" for chunk in chunks)
    assert [chunk[0]["segment_index"] for chunk in chunks] == [0, 1, 2]


def test_stage03_chunks_apply_limit_to_utf8_bytes() -> None:
    chunks = _chunks([{"evidence_id": "ev-unicode", "text": "中文测试"}], 6)

    assert [chunk[0]["text"] for chunk in chunks] == ["中文", "测试"]
    assert all(len(chunk[0]["text"].encode("utf-8")) <= 6 for chunk in chunks)


def test_stage03_chunks_drop_coordinate_segments_inside_mixed_long_block() -> None:
    coordinates = " ".join(f"C {index}.0 {index + 1}.0 {index + 2}.0" for index in range(180))
    chunks = _chunks(
        [
            {
                "evidence_id": "ev-mixed",
                "document_id": "doc",
                "text": f"Computational details use DFT. {coordinates}",
            }
        ],
        900,
    )

    combined = " ".join(block["text"] for chunk in chunks for block in chunk)
    assert "Computational details use DFT" in combined
    assert len(combined) < len(coordinates) / 2


def test_stage03_chunks_budget_serialized_block_metadata() -> None:
    blocks = [
        {
            "evidence_id": f"ev-{index}",
            "document_id": "document-with-metadata",
            "section_path": ["Methods", "Computational details"],
            "text": "x",
        }
        for index in range(20)
    ]

    chunks = _chunks(blocks, 500)

    assert len(chunks) > 1
    assert all(len(chunk) < len(blocks) for chunk in chunks)


def test_stage03_skips_large_atomic_coordinate_dump_but_keeps_result_table() -> None:
    coordinates = " ".join(f"C {index}.1000 {index}.2000 {index}.3000" for index in range(100))
    result_table = "Reaction barrier kcal mol " + " ".join(
        f"R{index} {index}.5" for index in range(100)
    )

    assert _is_atomic_coordinate_dump({"text": coordinates}) is True
    assert _is_atomic_coordinate_dump({"text": result_table}) is False


def test_llm_json_parser_repairs_truncated_object() -> None:
    assert _parse_json_object('{"decision":"pass","items":[1,2') == {
        "decision": "pass",
        "items": [1, 2],
    }


def test_stage03_map_validation_ignores_repaired_scalar_items() -> None:
    blocks = [{"evidence_id": "ev-1", "text": "Gaussian was used for optimization."}]
    response = {
        "evidence": [
            {
                "evidence_id": "ev-1",
                "exact_quote": "Gaussian was used",
                "attribution": "this_paper",
                "confidence": "high",
            },
            "stray repaired fragment",
        ]
    }

    assert _validate_map(response, blocks) == [response["evidence"][0]]


@pytest.mark.parametrize(
    ("experiment_type", "quote"),
    [
        (
            "Phonon spectrum calculation",
            "Figure S20. Calculated phonon spectra of the six material candidates.",
        ),
        (
            "Molecular dynamics simulation",
            "All MD simulations were performed in an NPT ensemble at 310 K.",
        ),
        (
            "Density Functional Theory calculation",
            "DFT calculations were performed with a plane-wave cutoff of 600 eV.",
        ),
    ],
)
def test_stage03_does_not_treat_computation_as_author_laboratory_evidence(
    experiment_type: str, quote: str
) -> None:
    item = {
        "evidence_id": "ev-1",
        "exact_quote": quote,
        "experiment_type": experiment_type,
        "attribution": "this_paper",
    }

    assert _is_explicit_author_laboratory_evidence(item) is False
    assert _validate_experiment_map([item], [{"evidence_id": "ev-1", "text": quote}]) == []


def test_stage03_accepts_explicit_author_nmr_measurement_as_laboratory_evidence() -> None:
    quote = "1H NMR spectra were recorded on a 400 MHz spectrometer."
    item = {
        "evidence_id": "ev-1",
        "exact_quote": quote,
        "experiment_type": "NMR spectroscopy",
        "attribution": "this_paper",
    }

    assert _validate_experiment_map([item], [{"evidence_id": "ev-1", "text": quote}]) == [item]


def test_stage03_resolves_configured_native_software_without_predefined_action() -> None:
    mappings = resolve_software(
        [
            {
                "raw_name": "VMD",
                "role": "required_analysis",
                "actual_use": True,
                "evidence_ids": ["ev-vmd"],
            }
        ],
        {"vmd": ["VMD", "vmd"]},
        {
            "backends": {},
            "native_software": {
                "vmd": {
                    "availability": "configured_in_toolbox_runtime",
                    "validation_level": "functional",
                    "actions": [],
                    "method_families": [],
                }
            },
            "python_packages": {},
        },
    )

    assert mappings[0]["catalog_kind"] == "native_software"
    assert mappings[0]["catalog_present"] is True
    assert mappings[0]["normalized_identifier"] == "vmd"


def test_stage03_accepts_passive_author_rixs_experiment_and_full_text_scan() -> None:
    quote = (
        "The VtC-RIXS experiments were performed using the Alvra instrument of the "
        "Swiss Free Electron Laser (SwissFEL)."
    )
    block = {"evidence_id": "ev-rixs", "text": quote}
    item = {
        "evidence_id": "ev-rixs",
        "exact_quote": quote,
        "experiment_type": "VtC-RIXS measurement",
        "attribution": "this_paper",
    }

    assert _validate_experiment_map([item], [block]) == [item]
    assert _find_deterministic_author_experiments([block]) == [
        {
            "evidence_id": "ev-rixs",
            "exact_quote": quote,
            "experiment_type": "physical laboratory measurement or preparation",
            "attribution": "this_paper",
            "confidence": "high",
            "source": "deterministic_full_text_scan",
        }
    ]


def test_stage03_full_text_scan_ignores_computational_experiments() -> None:
    quote = "Control experiments were performed using DFT calculations with three functionals."
    assert (
        _find_deterministic_author_experiments([{"evidence_id": "ev-compute", "text": quote}]) == []
    )


def test_stage03_rejects_instrument_details_for_previous_study_spectra() -> None:
    quote = "CPL spectra were recorded on a JASCO CPL-200 spectrofluoropolarimeter."
    text = (
        "The experimental spectra were taken from the previous study, and recorded under "
        f"the following conditions. {quote}"
    )
    item = {
        "evidence_id": "ev-prior",
        "exact_quote": quote,
        "experiment_type": "CPL spectroscopy",
        "attribution": "this_paper",
    }
    blocks = [{"evidence_id": "ev-prior", "text": text}]

    assert _validate_experiment_map([item], blocks) == []
    assert _find_deterministic_author_experiments(blocks) == []


def test_stage03_rejects_external_xfel_structure_as_author_experiment() -> None:
    quote = "Our initial model originates from the published XFEL structure 8F4H."
    item = {
        "evidence_id": "ev-1",
        "exact_quote": quote,
        "experiment_type": "XFEL crystallography",
        "attribution": "this_paper",
    }

    assert _is_explicit_author_laboratory_evidence(item) is False


@pytest.mark.parametrize(
    ("experiment_type", "quote"),
    [
        (
            "catalyst synthesis",
            "In 2021, Mecking and coworkers introduced a neutral nickel catalyst.",
        ),
        (
            "electrochemical performance testing",
            "The optimized system exhibited an energy efficiency of 30%.",
        ),
    ],
)
def test_stage03_requires_quote_level_current_author_laboratory_action(
    experiment_type: str, quote: str
) -> None:
    assert (
        _is_explicit_author_laboratory_evidence(
            {
                "experiment_type": experiment_type,
                "exact_quote": quote,
                "attribution": "this_paper",
            }
        )
        is False
    )


@pytest.mark.parametrize(
    ("title", "front_text", "expected_role"),
    [
        (
            "Correction to an original article",
            "Corrected calculations are supplied.",
            "correction",
        ),
        (
            "Nanocellulose: New horizons in organic chemistry and beyond",
            "In this perspective, we explore the use of nanocellulose.",
            "perspective",
        ),
        (
            "Strained diradicaloids for bond insertion",
            "Houk, Garg, and colleagues report in Nature a new synthetic method.",
            "editorial",
        ),
        (
            "Acylsilanes as directing groups",
            "We herein highlight the advances that have been made in acylsilane chemistry.",
            "review",
        ),
        (
            "Controlled carbon nanotube growth",
            "Recently in the Journal of the American Chemical Society, Huang and co-workers "
            "reported the synthesis of collarene macrocycles.",
            "editorial",
        ),
    ],
)
def test_stage03_deterministically_rejects_non_original_articles(
    title: str, front_text: str, expected_role: str
) -> None:
    result = _non_original_article_guard(
        {"title": title}, [{"evidence_id": "ev-1", "text": front_text}]
    )

    assert result is not None
    assert result["decision"] == "non_original_article"
    assert result["article_role"] == expected_role


def test_stage03_retries_truncated_json_instead_of_accepting_repair() -> None:
    class Model:
        calls = []

        def call_json(self, **kwargs):
            self.calls.append(kwargs)
            if len(self.calls) == 1:
                return {"partial": True}, {"finish_reason": "length", "request_hash": "first"}
            return {"complete": True}, {"finish_reason": "stop", "request_hash": "second"}

    model = Model()
    response, audit = _call_complete_json(
        model,
        namespace="stage02_map",
        record_id="paper-1-0000",
        prompt_version="test-v1",
        system_prompt="Return JSON.",
        user_content="{}",
        max_tokens=2048,
    )

    assert response == {"complete": True}
    assert audit["truncation_retry"] is True
    assert len(model.calls) == 2
    assert model.calls[1]["namespace"] == "stage02_map_complete_retry"


def test_stage03_reduce_filters_unknown_ids_and_downgrades_unsupported_confirmation() -> None:
    response, warnings = _sanitize_reduce_response(
        {
            "decision": "computational_content_confirmed",
            "evidence_ids": ["invented"],
            "conflicting_evidence_ids": ["ev-1", "other"],
            "confidence": "high",
        },
        {"ev-1"},
    )

    assert response["decision"] == "uncertain"
    assert response["evidence_ids"] == []
    assert response["conflicting_evidence_ids"] == ["ev-1"]
    assert response["confidence"] == "low"
    assert {warning["reason"] for warning in warnings} == {
        "unknown_evidence_ids",
        "confirmed_without_validated_evidence_downgraded",
    }


def test_stage02_primary_gate_rejects_experimental_supporting_computation() -> None:
    response, warnings = _sanitize_reduce_response(
        {
            "decision": "computational_content_confirmed",
            "article_role": "original_research",
            "performed_computation": "yes",
            "computation_role": "supporting",
            "study_mode": "experimental_with_computational_support",
            "author_performed_experiments": "yes",
            "workflow_complete": "yes",
            "evidence_ids": ["calc"],
            "experimental_evidence_ids": ["experiment"],
            "confidence": 0.98,
        },
        {"calc"},
        experiment_ids={"experiment"},
        allow_primary_mixed=True,
    )

    assert response["decision"] == "not_pure_computational"
    assert any(
        warning["reason"] == "computation_primary_requirements_failed"
        for warning in warnings
    )


def test_stage02_primary_gate_accepts_complete_pure_computation() -> None:
    response, warnings = _sanitize_reduce_response(
        {
            "decision": "computational_content_confirmed",
            "article_role": "original_research",
            "performed_computation": "yes",
            "computation_role": "primary",
            "study_mode": "pure_computational",
            "author_performed_experiments": "no",
            "workflow_complete": "yes",
            "evidence_ids": ["calc"],
            "experimental_evidence_ids": [],
            "confidence": 0.9,
        },
        {"calc"},
        allow_primary_mixed=True,
    )

    assert response["decision"] == "computational_content_confirmed"
    assert warnings == []


def test_stage02_primary_gate_accepts_computation_primary_mixed_study() -> None:
    response, warnings = _sanitize_reduce_response(
        {
            "decision": "computational_content_confirmed",
            "article_role": "original_research",
            "performed_computation": "yes",
            "computation_role": "primary",
            "study_mode": "pure_computational",
            "author_performed_experiments": "no",
            "workflow_complete": "yes",
            "evidence_ids": ["calc"],
            "experimental_evidence_ids": [],
            "confidence": 0.9,
        },
        {"calc"},
        experiment_ids={"experiment"},
        allow_primary_mixed=True,
    )

    assert response["decision"] == "computational_primary_mixed_confirmed"
    assert response["author_performed_experiments"] == "yes"
    assert response["study_mode"] == "mixed_computational_experimental"
    assert any(
        warning["reason"] == "verified_computation_primary_mixed_study_accepted"
        for warning in warnings
    )


def test_stage02_primary_gate_can_retain_pure_only_policy() -> None:
    response, warnings = _sanitize_reduce_response(
        {
            "decision": "computational_primary_mixed_confirmed",
            "article_role": "original_research",
            "performed_computation": "yes",
            "computation_role": "primary",
            "study_mode": "mixed_computational_experimental",
            "author_performed_experiments": "yes",
            "workflow_complete": "yes",
            "evidence_ids": ["calc"],
            "experimental_evidence_ids": ["experiment"],
            "confidence": 0.9,
        },
        {"calc"},
        experiment_ids={"experiment"},
        allow_primary_mixed=False,
    )

    assert response["decision"] == "not_pure_computational"
    assert any(
        warning["reason"] == "verified_author_laboratory_evidence_rejects_pure_computation"
        for warning in warnings
    )


def test_stage03_normalizes_experimental_only_record_to_not_found() -> None:
    response, warnings = _sanitize_reduce_response(
        {
            "decision": "not_pure_computational",
            "article_role": "original_research",
            "performed_computation": "no",
            "computation_role": "none",
            "study_mode": "mixed_computational_experimental",
            "author_performed_experiments": "yes",
            "workflow_complete": "no",
            "evidence_ids": [],
            "experimental_evidence_ids": ["lab"],
            "confidence": "high",
        },
        set(),
        experiment_ids={"lab"},
        allow_primary_mixed=True,
    )

    assert response["decision"] == "computational_content_not_found"
    assert response["study_mode"] == "noncomputational"
    assert any(warning["reason"] == "noncomputational_record_normalized" for warning in warnings)


def test_stage03_holds_unverified_author_experiment_claim() -> None:
    response, warnings = _sanitize_reduce_response(
        {
            "decision": "not_pure_computational",
            "article_role": "original_research",
            "performed_computation": "yes",
            "computation_role": "primary",
            "study_mode": "mixed_computational_experimental",
            "author_performed_experiments": "yes",
            "workflow_complete": "yes",
            "evidence_ids": ["calc"],
            "experimental_evidence_ids": [],
            "confidence": "high",
        },
        {"calc"},
        allow_primary_mixed=True,
    )

    assert response["decision"] == "uncertain"
    assert response["author_performed_experiments"] == "uncertain"
    assert any(
        warning["reason"] == "author_experiment_claim_without_verified_laboratory_evidence"
        for warning in warnings
    )


def test_stage03_holds_mixed_decision_without_verified_author_experiment() -> None:
    response, warnings = _sanitize_reduce_response(
        {
            "decision": "not_pure_computational",
            "article_role": "original_research",
            "performed_computation": "yes",
            "computation_role": "primary",
            "study_mode": "mixed_computational_experimental",
            "author_performed_experiments": "no",
            "workflow_complete": "yes",
            "evidence_ids": ["calc"],
            "confidence": "high",
        },
        {"calc"},
        allow_primary_mixed=True,
    )

    assert response["decision"] == "uncertain"
    assert any(
        warning["reason"] == "author_experiment_claim_without_verified_laboratory_evidence"
        for warning in warnings
    )


@pytest.mark.parametrize(
    ("method_families", "software_clues"),
    [
        (["life-cycle assessment", "process simulation"], ["OpenLCA", "Aspen HYSYS"]),
        (["sequence alignment", "differential expression"], ["Clustal Omega", "UMAP"]),
        (["data digitization", "causal inference"], ["Random Forest", "particle swarm"]),
        (["AlphaFold 3 structure prediction"], ["AlphaFold"]),
        (["Bayesian biological target prediction", "target voting"], ["FMBS"]),
        (["reaction condition recommendation", "label ranking"], ["scikit-learn"]),
        (["retrosynthesis", "synthesis planning"], ["AiZynthFinder"]),
        (
            ["multi-objective Monte Carlo tree search", "template-based retrosynthesis"],
            ["AiZynthFinder"],
        ),
        (["similarity-based enumeration"], ["enumerate chemical libraries"]),
        (
            ["clustering"],
            ["predict carbohydrate-binding residues", "cluster residues into pockets"],
        ),
        (["variational quantum eigensolver", "quantum circuit simulation"], ["qiskit"]),
    ],
)
def test_stage03_normalizes_excluded_non_molecular_computation(
    method_families: list[str], software_clues: list[str]
) -> None:
    response, warnings = _sanitize_reduce_response(
        {
            "decision": "not_pure_computational",
            "article_role": "original_research",
            "performed_computation": "yes",
            "computation_role": "primary",
            "study_mode": "mixed_computational_experimental",
            "author_performed_experiments": "no",
            "workflow_complete": "yes",
            "method_families": method_families,
            "software_clues": software_clues,
            "evidence_ids": ["calc"],
            "confidence": "high",
        },
        {"calc"},
        allow_primary_mixed=True,
    )

    assert response["decision"] == "computational_content_not_found"
    assert response["performed_computation"] == "no"
    assert response["study_mode"] == "noncomputational"
    assert any(
        warning["reason"] == "target_computational_chemistry_evidence_missing"
        for warning in warnings
    )


def test_stage03_keeps_target_chemistry_when_process_terms_are_also_present() -> None:
    response, warnings = _sanitize_reduce_response(
        {
            "decision": "computational_content_confirmed",
            "article_role": "original_research",
            "performed_computation": "yes",
            "computation_role": "primary",
            "study_mode": "pure_computational",
            "author_performed_experiments": "no",
            "workflow_complete": "yes",
            "method_families": ["DFT", "process modeling"],
            "evidence_ids": ["calc"],
            "confidence": "high",
        },
        {"calc"},
        allow_primary_mixed=True,
    )

    assert response["decision"] == "computational_content_confirmed"
    assert not any(
        warning["reason"] == "target_computational_chemistry_evidence_missing"
        for warning in warnings
    )


def test_pipeline_module_explicit_contract_runs_stage00_without_model_calls(tmp_path: Path) -> None:
    config = _base_config(tmp_path)
    config["stop_after"] = "stage00"
    config["stage00"] = {"enabled": False}
    path = tmp_path / "config.json"
    path.write_text(json.dumps(config), encoding="utf-8")

    result = run_pipeline(path)

    assert result["status"] == "completed"
    assert result["stage00"]["status"] == "external_corpus"
    assert (tmp_path / "run" / "run_summary.json").is_file()


def test_stage02_external_config_is_part_of_cache_contract(tmp_path: Path) -> None:
    mineru_config = tmp_path / "mineru.json"
    mineru_config.write_text('{"models-dir": "/first"}', encoding="utf-8")
    stage_config = {"mineru": {"environment": {"MINERU_TOOLS_CONFIG_JSON": str(mineru_config)}}}

    first = pipeline_module._stage02_external_file_fingerprints(stage_config)
    mineru_config.write_text('{"models-dir": "/second"}', encoding="utf-8")
    second = pipeline_module._stage02_external_file_fingerprints(stage_config)

    assert first[0]["path"] == str(mineru_config)
    assert first[0]["sha256"] != second[0]["sha256"]


def test_stage02_requires_every_known_supplementary_document_to_parse() -> None:
    papers = [{"paper_id": "paper-1", "package_status": "complete_with_si"}]
    documents = [
        {
            "paper_id": "paper-1",
            "document_id": "main",
            "document_role": "main",
            "decision": "pass",
        },
        {
            "paper_id": "paper-1",
            "document_id": "si-ok",
            "document_role": "supplementary",
            "decision": "pass",
        },
        {
            "paper_id": "paper-1",
            "document_id": "si-failed",
            "document_role": "supplementary",
            "decision": "parse_failed",
        },
    ]

    record = _paper_quality(papers, documents, "test-run")[0]

    assert record["decision"] == "parse_failed"
    assert record["supplementary_parse_ok"] is False
    assert record["partial_si_parse"] is True
    assert record["known_supplementary_documents"] == 2
    assert record["parsed_supplementary_documents"] == 1
    assert record["failed_supplementary_document_ids"] == ["si-failed"]
    assert _is_stage02_eligible(record) is False


def test_stage02_accepts_complete_package_only_when_all_known_si_parse() -> None:
    papers = [{"paper_id": "paper-1", "package_status": "complete_with_si"}]
    documents = [
        {
            "paper_id": "paper-1",
            "document_id": "main",
            "document_role": "main",
            "decision": "pass",
        },
        {
            "paper_id": "paper-1",
            "document_id": "si-1",
            "document_role": "supplementary",
            "decision": "pass",
        },
        {
            "paper_id": "paper-1",
            "document_id": "si-2",
            "document_role": "supplementary",
            "decision": "pass",
        },
    ]

    record = _paper_quality(papers, documents, "test-run")[0]

    assert record["decision"] == "pass"
    assert record["supplementary_parse_ok"] is True
    assert record["partial_si_parse"] is False
    assert record["failed_supplementary_document_ids"] == []
    assert _is_stage02_eligible(record) is True


def test_stage02_paper_quality_preserves_article_metadata() -> None:
    paper = {
        "paper_id": "paper-1",
        "doi": "10.1000/example",
        "title": "Correction: example",
        "journal_name": "Example Journal",
        "article_url": "https://example.test/article",
        "package_status": "complete_confirmed_no_si",
    }
    document = {
        "paper_id": "paper-1",
        "document_id": "doc-1",
        "document_role": "main",
        "decision": "pass",
        "source_record": {},
    }

    record = _paper_quality([paper], [document], "test-run")[0]

    assert record["doi"] == paper["doi"]
    assert record["title"] == paper["title"]
    assert record["journal_name"] == paper["journal_name"]
    assert record["article_url"] == paper["article_url"]


def test_stage03_rejects_legacy_partial_si_stage02_record() -> None:
    assert not _is_stage02_eligible(
        {
            "decision": "pass",
            "main_parse_ok": True,
            "supplementary_parse_ok": True,
            "partial_si_parse": True,
        }
    )
    assert not _is_stage02_eligible({"decision": "pass"})


def test_microbatch_cache_invalidates_only_changed_stage_and_downstream(
    tmp_path: Path,
) -> None:
    config = _base_config(tmp_path)
    config["stage01"] = {
        "normalization": {"grobid": {"base_url": "http://127.0.0.1:10001"}}
    }
    config["stage03"]["softcite"] = {"base_url": "http://127.0.0.1:10002"}
    (tmp_path / "profile.json").write_text('{"backends": {}}', encoding="utf-8")
    (tmp_path / "aliases.json").write_text("{}", encoding="utf-8")
    papers = [{"paper_id": "paper-1"}]
    documents = [
        {
            "paper_id": "paper-1",
            "document_id": "doc-1",
            "sha256": "abc",
            "source_path": "/fixture/paper.pdf",
        }
    ]

    first = _microbatch_stage_hashes(papers, documents, config)
    changed = json.loads(json.dumps(config))
    changed["stage04"]["max_tokens"] = 5120
    second = _microbatch_stage_hashes(papers, documents, changed)

    assert first["stage02"] == second["stage02"]
    assert first["stage03"] == second["stage03"]
    assert first["stage04"] != second["stage04"]
    assert first["stage05"] != second["stage05"]

    changed["stage01"]["normalization"]["grobid"]["base_url"] = "http://127.0.0.1:20001"
    changed["stage03"]["softcite"]["base_url"] = "http://127.0.0.1:20002"
    third = _microbatch_stage_hashes(papers, documents, changed)
    assert second == third


def test_stage02_implementation_version_invalidates_all_downstream_cache(
    tmp_path: Path, monkeypatch
) -> None:
    config = _base_config(tmp_path)
    config["stage01"] = {
        "normalization": {"grobid": {"base_url": "http://127.0.0.1:10001"}}
    }
    (tmp_path / "profile.json").write_text('{"backends": {}}', encoding="utf-8")
    (tmp_path / "aliases.json").write_text("{}", encoding="utf-8")
    papers = [{"paper_id": "paper-1"}]
    documents = [
        {
            "paper_id": "paper-1",
            "document_id": "doc-1",
            "sha256": "abc",
            "source_path": "/fixture/paper.pdf",
        }
    ]
    first = _microbatch_stage_hashes(papers, documents, config)

    monkeypatch.setattr(
        pipeline_module,
        "COMPUTATIONAL_CONTENT_IMPLEMENTATION_VERSION",
        "v2-stage02-test-new-implementation",
    )
    second = _microbatch_stage_hashes(papers, documents, config)

    assert first["stage01"] == second["stage01"]
    assert all(first[stage] != second[stage] for stage in ("stage02", "stage03", "stage04", "stage05"))


def test_v2_sandbox_prewarms_and_pools_configured_softcite_instances(
    monkeypatch,
) -> None:
    class Runtime:
        class Options:
            startup_timeout_seconds = 3600

        options = Options()

        def __init__(self):
            self.started = []

        def service_config(self, name, config, *, instance=0):
            return {
                **config,
                "base_url": f"http://127.0.0.1:{10000 + instance}",
                "_sandbox_runtime": self,
                "_sandbox_instance": instance,
            }

        def start_service(self, name, config, *, instance=0):
            del config
            self.started.append((name, instance))
            return {"healthy": True}

    class Client:
        def __init__(self, instance):
            self.instance = instance

        def version(self):
            return {"instance": self.instance}

    @contextlib.contextmanager
    def fake_softcite_service(config):
        yield Client(config["_sandbox_instance"])

    monkeypatch.setattr(pipeline_module, "softcite_service", fake_softcite_service)
    runtime = Runtime()
    config = {
        "stage02": {"grobid": {}},
        "stage04": {"mineru": {}, "softcite": {"enabled": True, "instances": 3}},
    }
    _apply_sandbox(config, runtime)

    assert config["stage04"]["mineru"]["environment"]["_sandbox_runtime"] is runtime
    assert "mineru" not in config["stage02"]

    with contextlib.ExitStack() as stack:
        pool = _softcite_service(config["stage04"], stack)
        assert [pool.version()["instance"] for _ in range(3)] == [0, 1, 2]

    assert sorted(runtime.started) == [
        ("softcite", 0),
        ("softcite", 1),
        ("softcite", 2),
    ]


def test_stage01_groups_same_doi_and_inventories_manifest_non_pdf_si(tmp_path: Path) -> None:
    corpus = tmp_path / "corpus"
    for index in (1, 2):
        bundle = corpus / f"paper-{index}"
        bundle.mkdir(parents=True)
        (bundle / "main.pdf").write_bytes(b"%PDF-1.4\nfixture\n")
        supplementary = []
        if index == 1:
            (bundle / "supporting.txt").write_text("computational parameters", encoding="utf-8")
            supplementary = [
                {
                    "relative_path": "supporting.txt",
                    "remote_uri": "s3://fixture/supporting.txt",
                    "document_role": "supplementary",
                }
            ]
        (bundle / "paper.json").write_text(
            json.dumps(
                {
                    "paper_id": f"paper-{index}",
                    "doi": "10.1000/fixture",
                    "main_document": {
                        "relative_path": "main.pdf",
                        "document_role": "main",
                    },
                    "supplementary_documents": supplementary,
                }
            ),
            encoding="utf-8",
        )

    result = run_stage01(
        corpus_root=corpus,
        config={"workers": 1, "enable_network": False},
        workspace=tmp_path / "run",
        run_id="test-run",
    )

    assert len(result["papers"]) == 1
    assert result["papers"][0]["package_status"] == "complete_with_si"
    assert result["summary"]["duplicate_groups"] == 1
    assert any(row["file_name"] == "supporting.txt" for row in result["documents"])


def test_stage02_normalizes_text_supplementary_asset(tmp_path: Path) -> None:
    source = tmp_path / "supporting.txt"
    source.write_text(
        "Gaussian calculations used the B3LYP functional and def2-SVP basis set. " * 4,
        encoding="utf-8",
    )
    document = {
        "paper_id": "paper",
        "document_id": "si",
        "file_name": source.name,
        "source_path": str(source),
        "size_bytes": source.stat().st_size,
        "sha256": "fixture",
        "document_role": "supplementary",
    }

    record, attempt = _normalize_non_pdf(
        document,
        {"min_supplementary_characters": 20, "mineru": {"enabled": False}},
        tmp_path / "stage02",
        tmp_path / "stage02" / "raw",
        "test-run",
    )

    assert record["decision"] == "pass"
    assert record["selected_parser"] == "asset_text"
    assert attempt["status"] == "success"


def test_stage02_routes_all_pdfs_to_grobid(tmp_path: Path, monkeypatch) -> None:
    grobid_ids = []

    def fake_grobid(inventory, client, tei_dir, text_dir, **kwargs):
        results = []
        for item in inventory:
            grobid_ids.append(item["document_id"])
            text = tmp_path / f"{item['document_id']}.txt"
            text.write_text("supplementary computational parameters", encoding="utf-8")
            results.append({"grobid_extract_status": "success", "text_path": str(text)})
        return results

    monkeypatch.setattr(normalization_module, "extract_documents_with_grobid", fake_grobid)
    documents = []
    for document_id, role in (("main", "main_paper"), ("si", "supplementary")):
        source = tmp_path / f"{document_id}.pdf"
        source.write_bytes(b"%PDF fixture")
        documents.append(
            {
                "paper_id": "paper",
                "document_id": document_id,
                "document_role": role,
                "source_path": str(source),
                "page_count": 1,
                "canonical_in_paper": True,
            }
        )

    result = normalization_module.run_document_normalization(
        papers=[{"paper_id": "paper", "decision": "pass"}],
        documents=documents,
        config={
            "min_main_characters": 1,
            "min_supplementary_characters": 1,
            "grobid": {"workers": 1},
        },
        workspace=tmp_path / "run",
        run_id="test-run",
        grobid_client=object(),
    )

    assert grobid_ids == ["main", "si"]
    assert {row["document_id"]: row["selected_parser"] for row in result["documents"]} == {
        "main": "grobid",
        "si": "grobid",
    }


def test_stage02_low_quality_grobid_falls_back_to_pdftotext(tmp_path: Path, monkeypatch) -> None:
    source = tmp_path / "paper.pdf"
    source.write_bytes(b"%PDF fixture")
    grobid_text = tmp_path / "grobid.txt"
    grobid_text.write_text("short", encoding="utf-8")

    monkeypatch.setattr(
        normalization_module,
        "extract_documents_with_grobid",
        lambda *args, **kwargs: [
            {"grobid_extract_status": "success", "text_path": str(grobid_text)}
        ],
    )
    monkeypatch.setattr(
        normalization_module,
        "_pdftotext_fallback",
        lambda *args, **kwargs: {
            "status": "success",
            "text": "complete computational methods " * 20,
            "text_path": str(tmp_path / "pdftotext.txt"),
        },
    )
    result = normalization_module.run_document_normalization(
        papers=[{"paper_id": "paper", "decision": "pass"}],
        documents=[
            {
                "paper_id": "paper",
                "document_id": "main",
                "document_role": "main_paper",
                "source_path": str(source),
                "page_count": 1,
                "canonical_in_paper": True,
            }
        ],
        config={"min_main_characters": 100, "grobid": {"workers": 1}},
        workspace=tmp_path / "run",
        run_id="test-run",
        grobid_client=object(),
    )

    assert result["documents"][0]["selected_parser"] == "pdftotext"
    assert [row["parser"] for row in result["attempts"]] == ["grobid", "pdftotext"]


def test_stage04_deep_normalizes_only_gate_passed_papers(tmp_path: Path, monkeypatch) -> None:
    queued = []

    def fake_mineru(queue, output_dir, **kwargs):
        queued.extend(item["document_id"] for item in queue)
        output = []
        for item in queue:
            markdown = tmp_path / f"{item['document_id']}.md"
            markdown.write_text(
                "# Methods\n\n" + "Density functional theory results. " * 20,
                encoding="utf-8",
            )
            content = tmp_path / f"{item['document_id']}_content_list_v2.json"
            content.write_text(
                json.dumps([{"type": "text", "text": "Density functional theory results."}]),
                encoding="utf-8",
            )
            output.append(
                {
                    **item,
                    "status": "success",
                    "markdown_path": str(markdown),
                    "content_list_v2_path": str(content),
                    "structured_pages": 1,
                    "duration_seconds": 1.0,
                }
            )
        return output

    monkeypatch.setattr(stage04_module, "run_mineru_queue", fake_mineru)
    documents = []
    for paper_id in ("passed", "rejected"):
        source = tmp_path / f"{paper_id}.pdf"
        source.write_bytes(b"%PDF fixture")
        documents.append(
            {
                "paper_id": paper_id,
                "document_id": f"doc-{paper_id}",
                "document_role": "main_paper",
                "source_path": str(source),
                "page_count": 1,
                "decision": "pass",
                "selected_parser": "grobid",
            }
        )
    records = [
        {"paper_id": "passed", "decision": "software_covered", "passed": True},
        {"paper_id": "rejected", "decision": "core_software_uncovered", "passed": False},
    ]

    updated, deep_documents, attempts = stage04_module._deep_normalize_passed_papers(
        records=records,
        documents=documents,
        config={"mineru": {"enabled": True, "min_main_characters": 10}},
        stage_root=tmp_path / "stage04",
        run_id="test-run",
    )

    assert queued == ["doc-passed"]
    assert updated[0]["passed"] is True
    assert deep_documents[0]["selected_parser"] == "mineru"
    assert deep_documents[0]["stage01_selected_parser"] == "grobid"
    assert attempts[0]["status"] == "success"
    assert Path(deep_documents[0]["content_blocks_path"]).is_file()


def test_stage04_mineru_failure_holds_paper(tmp_path: Path, monkeypatch) -> None:
    source = tmp_path / "paper.pdf"
    source.write_bytes(b"%PDF fixture")
    monkeypatch.setattr(
        stage04_module,
        "run_mineru_queue",
        lambda queue, output_dir, **kwargs: [
            {**queue[0], "status": "failed", "error": "fixture failure"}
        ],
    )
    records, documents, _attempts = stage04_module._deep_normalize_passed_papers(
        records=[{"paper_id": "paper", "decision": "software_covered", "passed": True}],
        documents=[
            {
                "paper_id": "paper",
                "document_id": "main",
                "document_role": "main_paper",
                "source_path": str(source),
                "page_count": 1,
                "decision": "pass",
                "selected_parser": "grobid",
            }
        ],
        config={"mineru": {"enabled": True}},
        stage_root=tmp_path / "stage04",
        run_id="test-run",
    )

    assert records[0]["gate_decision"] == "software_covered"
    assert records[0]["decision"] == "deep_parse_failed"
    assert records[0]["passed"] is False
    assert documents[0]["decision"] == "deep_parse_failed"


def test_role_model_cache_replays_without_second_call(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("TEST_MODEL_KEY", "secret")
    calls = []

    def caller(**kwargs):
        calls.append(kwargs)
        return {"ok": True}, {"model_returned": kwargs["model"]}

    client = RoleModelClient(
        role="screening",
        config={
            "model": "fixture",
            "base_url": "http://fixture/v1",
            "api_key_env": "TEST_MODEL_KEY",
            "workers": 2,
            "cache": True,
        },
        cache_root=tmp_path,
        caller=caller,
    )
    first, first_audit = client.call_json(
        namespace="test",
        record_id="paper",
        prompt_version="v1",
        system_prompt="system",
        user_content="input",
    )
    second, second_audit = client.call_json(
        namespace="test",
        record_id="paper",
        prompt_version="v1",
        system_prompt="system",
        user_content="input",
    )

    assert first == second == {"ok": True}
    assert first_audit["cache_hit"] is False
    assert second_audit["cache_hit"] is True
    assert len(calls) == 1


def test_late_stage_model_uses_default_proxy_without_global_environment(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setenv("TEST_MODEL_KEY", "secret")
    for name in ("HTTP_PROXY", "HTTPS_PROXY", "http_proxy", "https_proxy"):
        monkeypatch.delenv(name, raising=False)
    calls = []

    def caller(**kwargs):
        calls.append(kwargs)
        return {"ok": True}, {"model_returned": kwargs["model"]}

    client = RoleModelClient(
        role="suitability",
        config={
            "model": "fixture",
            "base_url": "https://fixture/v1",
            "api_key_env": "TEST_MODEL_KEY",
            "cache": False,
        },
        cache_root=tmp_path,
        caller=caller,
    )
    client.call_json(
        namespace="test",
        record_id="paper",
        prompt_version="v1",
        system_prompt="system",
        user_content="input",
    )

    assert calls[0]["proxy_url"] == DEFAULT_REMOTE_API_PROXY


def test_screening_model_disables_proxy_even_when_environment_has_one(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setenv("TEST_MODEL_KEY", "secret")
    monkeypatch.setenv("HTTPS_PROXY", "http://proxy.invalid:3128")
    calls = []

    def caller(**kwargs):
        calls.append(kwargs)
        return {"ok": True}, {"model_returned": kwargs["model"]}

    client = RoleModelClient(
        role="screening",
        config={
            "model": "fixture",
            "base_url": "http://127.0.0.1:18083/v1",
            "api_key_env": "TEST_MODEL_KEY",
            "cache": False,
        },
        cache_root=tmp_path,
        caller=caller,
    )
    client.call_json(
        namespace="test",
        record_id="paper",
        prompt_version="v1",
        system_prompt="system",
        user_content="input",
    )

    assert calls[0]["proxy_url"] == ""


def test_stage03_and_stage04_share_client_but_keep_prompt_namespaces(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.setenv("TEST_MODEL_KEY", "secret")
    evidence_id = "ev_doc_1_000001_fixture"
    quote = (
        "Density functional theory calculations were performed with Gaussian 16 using 8 CPU cores."
    )
    blocks_path = tmp_path / "blocks.jsonl"
    write_jsonl(
        blocks_path,
        [
            {
                "evidence_id": evidence_id,
                "document_id": "doc_1",
                "page": 2,
                "section_path": ["Computational methods"],
                "block_type": "paragraph",
                "text": quote,
            }
        ],
    )

    def caller(**kwargs):
        system = kwargs["system_prompt"]
        if "pure-computational-chemistry screening" in system:
            response = {
                "has_computational_evidence": True,
                "evidence": [
                    {
                        "evidence_id": evidence_id,
                        "exact_quote": quote,
                        "method_family": "electronic_structure",
                        "attribution": "this_paper",
                        "action": "energy calculation",
                        "software_clues": ["Gaussian 16"],
                        "result_clues": [],
                        "confidence": "high",
                    }
                ],
                "background_only_evidence": [],
                "conflicts": [],
            }
        elif "strict high-precision gate" in system:
            response = {
                "decision": "computational_content_confirmed",
                "article_role": "original_research",
                "performed_computation": "yes",
                "computation_role": "primary",
                "study_mode": "pure_computational",
                "author_performed_experiments": "no",
                "workflow_complete": "yes",
                "method_families": ["electronic_structure"],
                "computational_actions": ["energy calculation"],
                "software_clues": ["Gaussian 16"],
                "resource_clues": ["8 CPU cores"],
                "evidence_ids": [evidence_id],
                "experimental_evidence_ids": [],
                "conflicting_evidence_ids": [],
                "rationale": "Performed DFT is explicit.",
                "confidence": "high",
            }
        else:
            response = {
                "inventory_complete": True,
                "workflows": [
                    {
                        "workflow_id": "wf1",
                        "description": "DFT energy workflow",
                        "method_family": "electronic_structure",
                        "steps": [
                            {
                                "step_id": "step1",
                                "action": "prepare input",
                                "essential": False,
                                "software": "Gaussian 16",
                                "normalized_backend": "gaussian",
                                "required_action": None,
                                "reported_settings": [],
                                "evidence_ids": [evidence_id],
                            },
                            {
                                "step_id": "step2",
                                "action": "calculate energy",
                                "essential": True,
                                "software": "Gaussian 16",
                                "normalized_backend": "gaussian",
                                "required_action": "calculate_energy",
                                "reported_settings": [],
                                "evidence_ids": [evidence_id],
                            },
                            {
                                "step_id": "step3",
                                "action": "analyze result",
                                "essential": False,
                                "software": "Gaussian 16",
                                "normalized_backend": "gaussian",
                                "required_action": None,
                                "reported_settings": [],
                                "evidence_ids": [evidence_id],
                            },
                        ],
                        "evidence_ids": [evidence_id],
                    }
                ],
                "software_mentions": [
                    {
                        "raw_name": "Gaussian 16",
                        "normalized_hint": "gaussian",
                        "entity_type": "program",
                        "role": "core_compute",
                        "actual_use": True,
                        "workflow_ids": ["wf1"],
                        "evidence_ids": [evidence_id],
                        "exact_quote": quote,
                    }
                ],
                "resource_facts": [
                    {
                        "resource_type": "cpu_cores",
                        "relation": "exact",
                        "value_min": 8,
                        "value_max": 8,
                        "unit": "cores",
                        "scope": "single_job",
                        "actual_computation": True,
                        "evidence_ids": [evidence_id],
                        "exact_quote": quote,
                    }
                ],
                "complexity_facts": [],
                "unresolved": [],
                "evidence_ids": [evidence_id],
                "confidence": "high",
                "rationale": "Complete workflow and software evidence.",
            }
        return response, {"model_returned": "fixture"}

    client = RoleModelClient(
        role="screening",
        config={
            "model": "fixture",
            "base_url": "http://fixture/v1",
            "api_key_env": "TEST_MODEL_KEY",
            "workers": 4,
            "cache": False,
        },
        cache_root=tmp_path / "cache",
        caller=caller,
    )
    documents = [
        {
            "paper_id": "paper_1",
            "document_id": "doc_1",
            "decision": "pass",
            "content_blocks_path": str(blocks_path),
        }
    ]
    stage02 = run_stage02(
        papers=[
            {
                "paper_id": "paper_1",
                "document_ids": ["doc_1"],
                "decision": "pass",
                "package_status": "complete_confirmed_no_si",
                "main_parse_ok": True,
                "supplementary_parse_ok": None,
                "partial_si_parse": False,
            }
        ],
        documents=documents,
        config={"workers": 1},
        model=client,
        workspace=tmp_path / "run",
        run_id="test-run",
    )
    profile = {
        "profile_id": "fixture",
        "catalog_hash": "hash",
        "backends": {
            "gaussian": {
                "availability": "declared_supported",
                "validation_level": "functional",
                "local_installation_status": "not_evaluated",
                "actions": ["calculate_energy"],
            }
        },
    }
    aliases = {"gaussian": ["Gaussian", "Gaussian 16"]}
    profile_path, aliases_path = tmp_path / "profile.json", tmp_path / "aliases.json"
    profile_path.write_text(json.dumps(profile), encoding="utf-8")
    aliases_path.write_text(json.dumps(aliases), encoding="utf-8")

    class FakeSoftcite:
        calls = 0

        def annotate_tei(self, tei_path):
            self.calls += 1
            assert Path(tei_path).read_text(encoding="utf-8").startswith("<TEI")
            return {"mentions": [{"software-name": {"rawForm": "Gaussian 16"}}]}

    softcite = FakeSoftcite()
    stage03 = run_stage03(
        stage02_records=stage02["records"],
        documents=documents,
        config={
            "workers": 1,
            "toolbox_capabilities": str(profile_path),
            "software_aliases": str(aliases_path),
            "software_coverage_basis": "native_software_catalog_presence",
            "resource_budget": {"cpu_cores": 128},
        },
        model=client,
        workspace=tmp_path / "run",
        run_id="test-run",
        softcite=softcite,
    )

    assert stage02["records"][0]["decision"] == "computational_content_confirmed"
    assert stage03["records"][0]["decision"] == "software_covered"
    assert stage03["records"][0]["softcite_mentions"]
    assert softcite.calls == 1
    cache_namespaces = {
        path.parent.name for path in (tmp_path / "cache" / "screening").glob("*/*.json")
    }
    assert {"stage02_map", "stage02_reduce", "stage03_inventory"}.issubset(cache_namespaces)


def test_stage04_softcite_input_removes_xml10_forbidden_characters(tmp_path: Path) -> None:
    import xml.etree.ElementTree as ET

    class ParsingSoftcite:
        def annotate_tei(self, tei_path):
            ET.parse(tei_path)
            return {"mentions": []}

    mentions, error = _softcite_mentions(
        ParsingSoftcite(),
        [{"evidence_id": "ev-1", "text": "Gaussian\x00 calculation\x0b completed."}],
        tmp_path / "softcite.xml",
    )

    assert mentions == []
    assert error is None
    assert "\x00" not in (tmp_path / "softcite.xml").read_text(encoding="utf-8")


def test_stage04_softcite_prompt_mentions_exclude_full_paragraphs() -> None:
    compact = _compact_softcite_mentions(
        [
            {
                "software-name": {"rawForm": "Gaussian 16", "normalizedForm": "Gaussian"},
                "context": "Gaussian 16 was used for optimization.",
                "paragraph": "x" * 100000,
                "mentionContextAttributes": {
                    "used": {"value": True, "score": 0.99},
                    "created": {"value": False, "score": 0.01},
                },
            }
        ]
    )

    assert compact == [
        {
            "raw_name": "Gaussian 16",
            "normalized_name": "Gaussian",
            "context": "Gaussian 16 was used for optimization.",
            "used": True,
            "created": False,
            "shared": False,
        }
    ]
    assert len(json.dumps(compact)) < 300


def test_stage04_prompt_packet_has_hard_serialized_budget() -> None:
    packet = {
        "paper_id": "paper",
        "softcite_mentions": [{"context": "s" * 1000} for _ in range(12)],
        "rule_software_mentions": [{"context": "r" * 1000} for _ in range(12)],
        "evidence_blocks": [{"text": "e" * 1000} for _ in range(12)],
    }

    bounded = _bound_prompt_packet(packet, 6000)

    assert len(json.dumps(bounded, separators=(",", ":")).encode()) <= 6000
    assert len(bounded["evidence_blocks"]) >= 1


def test_stage04_sanitizer_drops_unsupported_fact_without_failing_paper() -> None:
    evidence = {"ev-1": "Gaussian 16 was used for all DFT calculations."}
    response = {
        "inventory_complete": True,
        "workflows": [
            {
                "workflow_id": "wf-1",
                "steps": [
                    {
                        "step_id": "step-1",
                        "essential": True,
                        "software": "Gaussian 16",
                        "reported_settings": ["8 CPU cores"],
                        "evidence_ids": ["ev-1"],
                    }
                ],
                "evidence_ids": ["ev-1"],
            }
        ],
        "software_mentions": [
            {
                "raw_name": "Gaussian 16",
                "role": "core_compute",
                "actual_use": True,
                "evidence_ids": ["ev-1"],
                "exact_quote": "Gaussian 16 was used",
            },
            {
                "raw_name": "InventedSoft",
                "role": "core_compute",
                "actual_use": True,
                "evidence_ids": ["ev-1"],
                "exact_quote": "InventedSoft was used",
            },
        ],
        "resource_facts": [
            {
                "resource_type": "cpu_cores",
                "value_min": 128,
                "value_max": 128,
                "actual_computation": True,
                "evidence_ids": ["ev-1"],
                "exact_quote": "Gaussian 16 was used",
            }
        ],
        "complexity_facts": [],
        "evidence_ids": ["ev-1", "unknown"],
    }

    sanitized, warnings = _sanitize_review(response, evidence)

    assert [item["raw_name"] for item in sanitized["software_mentions"]] == ["Gaussian 16"]
    assert sanitized["workflows"][0]["steps"][0]["reported_settings"] == ["8 CPU cores"]
    assert sanitized["evidence_ids"] == ["ev-1"]
    assert warnings == [
        {
            "field": "software_mentions",
            "index": 1,
            "reason": "unsupported_quote_or_evidence",
        },
        {
            "field": "resource_facts",
            "index": 0,
            "reason": "resource_value_not_supported_by_quote",
        },
    ]
    assert sanitized["resource_facts"] == []


def test_stage04_target_blocks_budget_serialized_metadata() -> None:
    blocks = [
        {
            "evidence_id": f"ev-{index}",
            "document_id": "document-with-metadata",
            "page": index,
            "section_path": ["Computational methods"],
            "text": "x" * 80,
        }
        for index in range(20)
    ]
    selected = _target_blocks(
        blocks,
        {"review": {"evidence_ids": ["ev-0"]}},
        [],
        700,
    )

    assert selected[0]["evidence_id"] == "ev-0"
    assert len(selected) < len(blocks)


def test_stage04_software_rules_do_not_match_internal_backend_id_as_common_word() -> None:
    aliases = {"geometric": ["geomeTRIC"]}
    blocks = [
        {
            "evidence_id": "ev-common",
            "section_path": ["Results"],
            "text": "Particle size is a geometric parameter.",
        },
        {
            "evidence_id": "ev-software",
            "section_path": ["Methods"],
            "text": "Structures were optimized with geomeTRIC.",
        },
    ]

    mentions = find_software_mentions(blocks, aliases)

    assert [(item["backend_hint"], item["evidence_id"]) for item in mentions] == [
        ("geometric", "ev-software")
    ]


def test_stage04_software_rules_disambiguate_gaussian_math_from_program() -> None:
    aliases = {"gaussian": ["Gaussian", "Gaussian 16"]}
    blocks = [
        {
            "evidence_id": "ev-math",
            "section_path": ["Methods"],
            "text": "Finite-temperature effects were represented by Gaussian smearing.",
        },
        {
            "evidence_id": "ev-program",
            "section_path": ["Methods"],
            "text": "DFT calculations were performed using Gaussian 16.",
        },
    ]

    mentions = find_software_mentions(blocks, aliases)

    assert [(item["backend_hint"], item["evidence_id"]) for item in mentions] == [
        ("gaussian", "ev-program")
    ]


def test_stage04_sanitizer_drops_gaussian_filter_as_software() -> None:
    quote = "The Marcus term forms a Gaussian filter that is convolved with the density of states."
    response = {
        "inventory_complete": True,
        "workflows": [
            {
                "workflow_id": "wf-1",
                "steps": [
                    {
                        "step_id": "step-1",
                        "software": "gaussian",
                        "required_action": "calculate_dos",
                        "constraints": {},
                        "evidence_ids": ["ev-1"],
                    }
                ],
                "evidence_ids": ["ev-1"],
            }
        ],
        "software_mentions": [
            {
                "raw_name": "Gaussian",
                "normalized_hint": "gaussian",
                "role": "core_compute",
                "actual_use": True,
                "evidence_ids": ["ev-1"],
                "exact_quote": quote,
            }
        ],
        "resource_facts": [],
        "complexity_facts": [],
        "evidence_ids": ["ev-1"],
    }

    sanitized, warnings = _sanitize_review(response, {"ev-1": quote})

    assert sanitized["software_mentions"] == []
    assert sanitized["workflows"][0]["steps"][0]["software"] is None
    assert {warning["reason"] for warning in warnings} == {
        "ambiguous_generic_software_term",
        "nonsoftware_or_unsupported_executable_name",
    }


def test_stage04_sanitizer_requires_software_name_in_exact_quote() -> None:
    quote = "The density of states was integrated over the selected energy window."
    response = {
        "inventory_complete": True,
        "workflows": [],
        "software_mentions": [
            {
                "raw_name": "Gaussian",
                "role": "core_compute",
                "actual_use": True,
                "evidence_ids": ["ev-1"],
                "exact_quote": quote,
            }
        ],
        "resource_facts": [],
        "complexity_facts": [],
        "evidence_ids": ["ev-1"],
    }

    sanitized, warnings = _sanitize_review(response, {"ev-1": quote})

    assert sanitized["software_mentions"] == []
    assert [warning["reason"] for warning in warnings] == ["software_name_not_in_exact_quote"]


def test_stage04_sanitizer_recovers_exact_software_context_from_cited_evidence() -> None:
    evidence = (
        "All calculations were performed using periodic DFT 6 with the Vienna Ab initio "
        "Simulation Package (VASP) 3 code."
    )
    response = {
        "inventory_complete": True,
        "workflows": [],
        "software_mentions": [
            {
                "raw_name": "VASP",
                "entity_type": "program",
                "role": "core_compute",
                "actual_use": True,
                "evidence_ids": ["ev-1"],
                "exact_quote": (
                    "All calculations were performed using periodic DFT with the Vienna Ab initio "
                    "Simulation Package (VASP) code."
                ),
            }
        ],
        "resource_facts": [],
        "complexity_facts": [],
    }

    sanitized, warnings = _sanitize_review(response, {"ev-1": evidence})

    assert sanitized["software_mentions"][0]["raw_name"] == "VASP"
    assert sanitized["software_mentions"][0]["exact_quote"] == evidence
    assert [warning["reason"] for warning in warnings] == ["software_quote_recovered_from_evidence"]


def test_stage04_sanitizer_recovers_missing_quote_from_bound_evidence() -> None:
    evidence = "All calculations were performed with ExampleCode software."
    response = {
        "inventory_complete": True,
        "workflows": [],
        "software_mentions": [
            {
                "raw_name": "ExampleCode",
                "entity_type": "program",
                "role": "core_compute",
                "actual_use": True,
                "workflow_ids": [],
                "evidence_ids": ["ev-1"],
                "exact_quote": "",
            }
        ],
        "resource_facts": [],
        "complexity_facts": [],
    }

    assert not _inventory_contract_errors(response)
    sanitized, warnings = _sanitize_review(response, {"ev-1": evidence})

    assert sanitized["software_mentions"][0]["exact_quote"] == evidence
    assert any(row["reason"] == "software_quote_recovered_from_evidence" for row in warnings)


@pytest.mark.parametrize(
    "name",
    [
        "HSE",
        "PAW",
        "AutoNEB",
        "Fourier transform",
        "Gaussian potentials",
        "AmberFF19SB",
        "CHARMM36",
        "SOAP descriptor",
        "GPU",
        "Wannier interpolation",
        "PBE",
        "Monkhorst-Pack",
        "ReLU",
        "Adamax",
        "Huber loss",
        "24 cores",
        "HPE Cray EX",
        "sine functions",
        "custom mean-squared error loss",
        "RASSCF",
        "QSAR model",
        "DBSCAN",
        "Adam optimizer",
        "logistic regressors",
        "random forests",
        "PIP-NN",
        "DeepPot-SE",
        "RPMD",
        "CP-HS-DM",
    ],
)
def test_stage04_nonsoftware_names_are_not_executable_entities(name: str) -> None:
    assert _looks_like_nonsoftware_name(name)


def test_stage04_sanitizer_drops_method_reported_as_software() -> None:
    quote = "The HSE functional was used for the VASP band structure calculations."
    response = {
        "inventory_complete": True,
        "workflows": [],
        "software_mentions": [
            {
                "raw_name": "HSE",
                "entity_type": "method",
                "role": "core_compute",
                "actual_use": True,
                "evidence_ids": ["ev-1"],
                "exact_quote": quote,
            }
        ],
        "resource_facts": [],
        "complexity_facts": [],
        "evidence_ids": ["ev-1"],
    }

    sanitized, warnings = _sanitize_review(response, {"ev-1": quote})

    assert sanitized["software_mentions"] == []
    assert [warning["reason"] for warning in warnings] == [
        "method_or_process_not_software"
    ]


def test_stage04_sanitizer_expands_parenthesized_software_name() -> None:
    quote = "The method was implemented in the Atomic Simulation Environment (ASE) library."
    response = {
        "inventory_complete": True,
        "workflows": [],
        "software_mentions": [
            {
                "raw_name": "Atomic",
                "entity_type": "library",
                "role": "required_preprocessing",
                "actual_use": True,
                "evidence_ids": ["ev-1"],
                "exact_quote": quote,
            }
        ],
        "resource_facts": [],
        "complexity_facts": [],
    }

    sanitized, warnings = _sanitize_review(response, {"ev-1": quote})

    assert warnings == []
    assert sanitized["software_mentions"][0]["raw_name"] == "Atomic Simulation Environment"
    assert sanitized["software_mentions"][0]["normalized_hint"] == "ase"


def test_stage04_explicit_cue_merge_expands_parenthesized_software_name() -> None:
    quote = "The calculation was implemented in the Atomic Simulation Environment (ASE) library."

    mentions = _merge_explicit_executable_cues(
        [],
        [
            {
                "raw_name": "Atomic",
                "entity_type": "program",
                "evidence_id": "ev-1",
                "context": quote,
            }
        ],
    )

    assert mentions[0]["raw_name"] == "Atomic Simulation Environment"
    assert mentions[0]["normalized_hint"] == "ase"


def test_stage04_sanitizer_normalizes_explicit_parenthesized_abbreviation() -> None:
    quote = "Vibrations were evaluated with the Atomic Simulation Environment (ASE) library."
    response = {
        "inventory_complete": True,
        "workflows": [],
        "software_mentions": [
            {
                "raw_name": "Atomic Simulation Environment (ASE)",
                "entity_type": "library",
                "role": "required_analysis",
                "actual_use": True,
                "evidence_ids": ["ev-1"],
                "exact_quote": quote,
            }
        ],
        "resource_facts": [],
        "complexity_facts": [],
    }

    sanitized, warnings = _sanitize_review(response, {"ev-1": quote})

    assert warnings == []
    assert sanitized["software_mentions"][0]["raw_name"] == "Atomic Simulation Environment"
    assert sanitized["software_mentions"][0]["normalized_hint"] == "ase"


def test_stage04_sanitizer_drops_pseudopotential_library() -> None:
    quote = "Calculations used pseudopotentials from the SSSP library."
    response = {
        "inventory_complete": True,
        "workflows": [],
        "software_mentions": [
            {
                "raw_name": "SSSP",
                "entity_type": "library",
                "role": "required_preprocessing",
                "actual_use": True,
                "evidence_ids": ["ev-1"],
                "exact_quote": quote,
            }
        ],
        "resource_facts": [],
        "complexity_facts": [],
    }

    sanitized, warnings = _sanitize_review(response, {"ev-1": quote})

    assert sanitized["software_mentions"] == []
    assert [warning["reason"] for warning in warnings] == [
        "nonexecutable_data_or_parameter_library"
    ]


def test_stage04_retries_truncated_inventory_response() -> None:
    class Model:
        calls = []

        def call_json(self, **kwargs):
            self.calls.append(kwargs)
            if len(self.calls) == 1:
                return {"partial": True}, {"finish_reason": "length", "request_hash": "first"}
            return {"inventory_complete": True}, {"finish_reason": "stop"}

    response, audit = _call_complete_inventory(
        Model(), paper_id="paper-1", packet={"paper_id": "paper-1"}, max_tokens=4096
    )

    assert response == {"inventory_complete": True}
    assert audit["truncation_retry"] is True
    assert len(Model.calls) == 2


def test_stage04_uses_minimal_third_attempt_after_two_truncations() -> None:
    class Model:
        calls = []

        def call_json(self, **kwargs):
            self.calls.append(kwargs)
            if len(self.calls) < 3:
                return {"partial": True}, {
                    "finish_reason": "length",
                    "request_hash": f"try-{len(self.calls)}",
                }
            return {"inventory_complete": True}, {
                "finish_reason": "stop",
                "request_hash": "try-3",
            }

    response, audit = _call_complete_inventory(
        Model(), paper_id="paper-1", packet={"paper_id": "paper-1"}, max_tokens=4096
    )

    assert response == {"inventory_complete": True}
    assert audit["minimal_retry"] is True
    assert len(Model.calls) == 3


def test_stage04_essential_step_without_named_software_is_unconfirmed() -> None:
    review = {
        "workflows": [
            {
                "workflow_id": "wf",
                "steps": [
                    {
                        "action": "run custom continuum model",
                        "essential": True,
                        "software": None,
                        "required_action": None,
                    }
                ],
            }
        ]
    }
    mappings = [
        {
            "raw_name": "VASP",
            "normalized_backend": "vasp",
            "actual_use": True,
            "role": "core_compute",
            "catalog_present": True,
            "availability": "declared_supported",
            "local_installation_status": "not_evaluated",
            "actions": ["calculate_periodic_energy"],
        }
    ]

    assert coverage_gate(review, mappings, {}, {}) == "software_inventory_unconfirmed"


def test_stage04_complete_inventory_allows_generic_python_postprocessing() -> None:
    review = {
        "inventory_complete": True,
        "workflows": [
            {
                "workflow_id": "wf",
                "steps": [
                    {"action": "run DFT", "essential": True, "software": "VASP"},
                    {
                        "action": "compare relative energies",
                        "essential": True,
                        "execution_layer": "task_specific_python",
                        "software": None,
                    },
                ],
            }
        ],
    }
    mappings = [
        {
            "raw_name": "VASP",
            "normalized_backend": "vasp",
            "actual_use": True,
            "role": "core_compute",
            "catalog_present": True,
        }
    ]

    assert coverage_gate(review, mappings, {}, {}) == "covered"


def test_stage04_complete_inventory_cannot_hide_unnamed_core_engine() -> None:
    review = {
        "inventory_complete": True,
        "workflows": [
            {
                "workflow_id": "wf",
                "steps": [
                    {
                        "action": "run electronic-structure calculation",
                        "essential": True,
                        "execution_layer": "unknown",
                        "software": None,
                    }
                ],
            }
        ],
    }
    mappings = [
        {
            "raw_name": "VASP",
            "actual_use": True,
            "role": "core_compute",
            "catalog_present": True,
        }
    ]

    assert coverage_gate(review, mappings, {}, {}) == "software_inventory_unconfirmed"


@pytest.mark.parametrize(
    ("raw_name", "expected"),
    [
        ("NumPy", "numpy"),
        ("Atomic Simulation Environment", "ase"),
        ("PyTorch", "torch"),
    ],
)
def test_stage04_resolves_configured_python_packages(raw_name: str, expected: str) -> None:
    profile = {
        "backends": {},
        "python_packages": {
            "numpy": {"aliases": ["NumPy"]},
            "ase": {"aliases": ["ASE", "Atomic Simulation Environment"]},
            "torch": {"aliases": ["torch", "PyTorch"]},
        },
    }
    aliases = {
        "numpy": ["NumPy"],
        "ase": ["ASE", "Atomic Simulation Environment"],
        "torch": ["torch", "PyTorch"],
    }

    mapping = resolve_software(
        [{"raw_name": raw_name, "actual_use": True, "role": "required_analysis"}],
        aliases,
        profile,
    )[0]

    assert mapping["catalog_present"] is True
    assert mapping["catalog_kind"] == "python_package"
    assert mapping["normalized_identifier"] == expected


def test_stage04_does_not_trust_model_normalized_hint_for_toolbox_presence() -> None:
    profile = {
        "backends": {"vina": {"availability": "declared_supported"}},
        "python_packages": {},
    }
    aliases = {"vina": ["AutoDock Vina", "Vina"]}

    mapping = resolve_software(
        [
            {
                "raw_name": "QVina2",
                "normalized_hint": "vina",
                "actual_use": True,
                "role": "core_compute",
            }
        ],
        aliases,
        profile,
    )[0]

    assert mapping["catalog_present"] is False
    assert mapping["normalized_identifier"] is None


def test_stage04_resolves_catalogued_software_with_version_suffix() -> None:
    profile = {
        "backends": {"orca": {"availability": "declared_supported"}},
        "python_packages": {},
    }
    aliases = {"orca": ["ORCA"]}

    mapping = resolve_software(
        [{"raw_name": "ORCA 4.2.1", "actual_use": True, "role": "core_compute"}],
        aliases,
        profile,
    )[0]

    assert mapping["catalog_present"] is True
    assert mapping["normalized_identifier"] == "orca"


def test_stage04_named_open_source_code_is_an_executable_cue() -> None:
    blocks = [
        {
            "evidence_id": "ev-1",
            "section_path": ["Availability"],
            "text": "We present the open source TcESTIME code for computing the networking value.",
        }
    ]

    cues = find_explicit_executable_cues(blocks)

    assert any(
        cue["raw_name"] == "TcESTIME" and cue["entity_type"] == "custom_code" for cue in cues
    )


def test_stage04_explicit_cue_preserves_custom_code_entity_type() -> None:
    cues = [
        {
            "raw_name": "TcESTIME",
            "entity_type": "custom_code",
            "evidence_id": "ev-1",
            "context": "We present the open source TcESTIME code.",
        }
    ]

    mentions = _merge_explicit_executable_cues([], cues)

    assert mentions[0]["entity_type"] == "custom_code"
    assert mentions[0]["role"] == "unknown"


def test_stage04_workflow_software_is_promoted_to_coverage_inventory() -> None:
    quote = "Descriptors were computed with MissingChem and analyzed thereafter."
    mentions, warnings = _merge_workflow_software_mentions(
        [],
        [
            {
                "workflow_id": "wf-1",
                "steps": [
                    {
                        "software": "MissingChem",
                        "essential": True,
                        "evidence_ids": ["ev-1"],
                    }
                ],
            }
        ],
        {"ev-1": quote},
        {},
    )
    mappings = resolve_software(mentions, {}, {"backends": {}, "python_packages": {}})

    assert mentions[0]["role"] == "core_compute"
    assert mentions[0]["source"] == "workflow_step_contract"
    assert warnings[0]["reason"] == "workflow_software_promoted_to_inventory"
    assert (
        coverage_gate(
            {"inventory_complete": True, "workflows": [{"steps": []}]},
            mappings,
            {},
            {},
        )
        == "core_software_uncovered"
    )


def test_stage04_workflow_software_uses_alias_identity_without_duplicate() -> None:
    mentions, warnings = _merge_workflow_software_mentions(
        [
            {
                "raw_name": "Vienna Ab initio Simulation Package",
                "role": "core_compute",
                "actual_use": True,
            }
        ],
        [{"workflow_id": "wf-1", "steps": [{"software": "VASP", "essential": True}]}],
        {},
        {"vasp": ["VASP", "Vienna Ab initio Simulation Package"]},
    )

    assert len(mentions) == 1
    assert warnings == []


def test_stage04_catalog_actual_use_recovers_and_binds_model_omission() -> None:
    evidence = {
        "ev-1": (
            "Electronic energies were computed using the Example Quantum Suite "
            "with the settings listed below."
        )
    }
    workflows = [
        {
            "workflow_id": "wf-1",
            "evidence_ids": ["ev-1"],
            "steps": [
                {
                    "step_id": "step-1",
                    "action": "compute electronic energies",
                    "essential": True,
                    "execution_layer": "unknown",
                    "software": None,
                    "evidence_ids": ["ev-1"],
                },
                {
                    "step_id": "step-2",
                    "action": "perform Bader charge analysis",
                    "essential": True,
                    "execution_layer": "unknown",
                    "software": None,
                    "evidence_ids": ["ev-1"],
                },
            ],
        }
    ]
    aliases = {"example_quantum": ["Example Quantum Suite", "EQS"]}
    mentions, warnings = _merge_catalog_actual_use_mentions(
        [],
        [
            {
                "backend_hint": "example_quantum",
                "raw_name": "Example Quantum Suite",
                "evidence_id": "ev-1",
            }
        ],
        workflows,
        evidence,
        aliases,
    )
    assert mentions[0]["source"] == "catalog_alias_actual_use"
    assert mentions[0]["role"] == "unknown"
    assert mentions[0]["workflow_ids"] == ["wf-1"]
    assert warnings[0]["reason"] == "catalog_actual_use_mention_recovered"
    assert workflows[0]["steps"][0]["software"] is None
    assert workflows[0]["steps"][1]["software"] is None
    assert _bind_workflow_steps_to_mentions(workflows, mentions, aliases) == []


def test_stage04_catalog_alias_without_local_actual_use_is_not_promoted() -> None:
    evidence = {"ev-1": "Earlier studies reported results from Example Quantum Suite."}

    mentions, warnings = _merge_catalog_actual_use_mentions(
        [],
        [
            {
                "backend_hint": "example_quantum",
                "raw_name": "Example Quantum Suite",
                "evidence_id": "ev-1",
            }
        ],
        [],
        evidence,
        {"example_quantum": ["Example Quantum Suite"]},
    )

    assert mentions == []
    assert warnings == []


def test_stage04_multiword_catalog_alias_is_case_insensitive() -> None:
    mentions = find_software_mentions(
        [
            {
                "evidence_id": "ev-1",
                "section_path": ["Methods"],
                "text": (
                    "We employed the Vienna ab initio simulation package to perform "
                    "the electronic-structure calculations."
                ),
            }
        ],
        {"vasp": ["VASP", "Vienna Ab initio Simulation Package"]},
    )

    assert len(mentions) == 1
    assert mentions[0]["backend_hint"] == "vasp"
    assert mentions[0]["raw_name"] == "Vienna ab initio simulation package"


def test_stage04_external_detection_alias_does_not_imply_toolbox_presence() -> None:
    detection_aliases = _merge_detection_aliases(
        {"orca": ["ORCA"]}, {"molpro": ["Molpro", "MOLPRO"]}
    )
    mentions = find_software_mentions(
        [
            {
                "evidence_id": "ev-1",
                "section_path": [],
                "text": "All electronic energies were calculated using Molpro.",
            }
        ],
        detection_aliases,
    )

    assert mentions[0]["backend_hint"] == "molpro"
    mapping = resolve_software(
        [
            {
                "raw_name": "Molpro",
                "actual_use": True,
                "role": "core_compute",
                "evidence_ids": ["ev-1"],
            }
        ],
        {"orca": ["ORCA"]},
        {"backends": {"orca": {}}},
    )[0]
    assert mapping["catalog_present"] is False


def test_stage04_target_blocks_recovers_plain_paragraph_method_heading() -> None:
    blocks = [
        {
            "evidence_id": "ev-main",
            "document_id": "main",
            "document_role": "main_paper",
            "section_path": [],
            "text": "The computational result is summarized here.",
        },
        {
            "evidence_id": "ev-si-heading",
            "document_id": "si",
            "document_role": "supplementary",
            "section_path": [],
            "text": "Computational Details",
        },
        {
            "evidence_id": "ev-si-method",
            "document_id": "si",
            "document_role": "supplementary",
            "section_path": [],
            "text": "Geometry optimizations used ExternalEngine with the stated settings.",
        },
    ]

    selected = _target_blocks(
        blocks,
        {"review": {"evidence_ids": ["ev-main"]}},
        [],
        8000,
    )

    assert {row["evidence_id"] for row in selected} == {
        "ev-main",
        "ev-si-heading",
        "ev-si-method",
    }
    assert any(row.get("document_role") == "supplementary" for row in selected)


def test_stage04_explicit_cue_recovers_materials_studio_product_name() -> None:
    blocks = [
        {
            "evidence_id": "ev-1",
            "section_path": ["Methods"],
            "text": "The accessible volume was calculated using the Materials Studio package.",
        }
    ]

    cues = find_explicit_executable_cues(blocks)

    assert [cue["raw_name"] for cue in cues] == ["Materials Studio"]


def test_stage04_explicit_extension_cue_is_retained_as_uncovered_software() -> None:
    blocks = [
        {
            "evidence_id": "ev-1",
            "section_path": ["Methods"],
            "text": "Implicit solvation was implemented via the VASPsol extension.",
        }
    ]

    cues = find_explicit_executable_cues(blocks)
    mentions = _merge_explicit_executable_cues([], cues)

    assert [(row["raw_name"], row["entity_type"]) for row in mentions] == [("VASPsol", "extension")]
    assert mentions[0]["actual_use"] is True


def test_stage04_vasp_sol_module_is_retained_separately_from_vasp() -> None:
    blocks = [
        {
            "evidence_id": "ev-1",
            "section_path": ["Computational Methods"],
            "text": (
                "AIMD was performed with VASP and implicit solvent was implemented via the "
                "VASP sol module."
            ),
        }
    ]

    cues = find_explicit_executable_cues(blocks)
    mentions = _merge_explicit_executable_cues([], cues)

    assert any(
        row["raw_name"] == "VASPsol" and row["entity_type"] == "extension" for row in mentions
    )


@pytest.mark.parametrize(
    ("text", "expected_name"),
    [
        (
            "All energies were computed using a development version of ORCA based on ORCA 5.",
            "a development version of ORCA",
        ),
        (
            "The barriers were obtained using a locally revised version of Gaussian 16.",
            "a locally revised version of Gaussian 16",
        ),
        (
            "Rates were calculated using a new implementation of RPMD for surfaces.",
            "a new implementation of RPMD for surfaces",
        ),
    ],
)
def test_stage04_custom_runtime_is_separate_uncovered_entity(text, expected_name) -> None:
    block = {"evidence_id": "ev-custom", "section_path": ["Methods"], "text": text}
    known = find_software_mentions([block], {"orca": ["ORCA"], "gaussian": ["Gaussian 16"]})
    cues = find_explicit_executable_cues([block], known)
    mentions = _merge_explicit_executable_cues([], cues)

    assert any(
        row["raw_name"].casefold() == expected_name.casefold()
        and row["entity_type"] == "custom_code"
        for row in mentions
    )
    mappings = resolve_software(
        mentions,
        {"orca": ["ORCA"], "gaussian": ["Gaussian 16"]},
        {"backends": {"orca": {}, "gaussian": {}}, "native_software": {}, "python_packages": {}},
    )
    assert any(row["catalog_present"] is False for row in mappings)


def test_stage04_revised_density_functional_is_not_custom_software() -> None:
    text = "Calculations used the revised Perdew-Burke-Ernzerhof functional in GPAW."
    cues = find_explicit_executable_cues(
        [{"evidence_id": "ev-rpbe", "section_path": ["Methods"], "text": text}]
    )

    assert all("Perdew" not in row["raw_name"] for row in cues)


def test_stage04_explicit_lowercase_software_entity_is_preserved() -> None:
    cues = find_explicit_executable_cues(
        [
            {
                "evidence_id": "ev-lowercase",
                "section_path": ["Methods"],
                "text": "The cavity volume was analyzed using exampletool software.",
            }
        ]
    )

    assert [row["raw_name"] for row in cues] == ["exampletool"]
    assert cues[0]["deterministic_merge"] is False


def test_stage04_lowercase_entity_requires_model_confirmation_before_merge() -> None:
    cue = {
        "raw_name": "exampletool",
        "entity_type": "program",
        "evidence_id": "ev-lowercase",
        "context": "The analysis used exampletool software.",
        "deterministic_merge": False,
    }

    assert _merge_explicit_executable_cues([], [cue]) == []
    confirmed = {
        "raw_name": "exampletool",
        "entity_type": "program",
        "role": "core_compute",
        "actual_use": True,
        "workflow_ids": ["wf-1"],
        "evidence_ids": ["ev-lowercase"],
        "exact_quote": "The analysis used exampletool software.",
    }
    assert _merge_explicit_executable_cues([confirmed], [cue]) == [confirmed]


def test_stage04_lowercase_scientific_module_is_not_assumed_to_be_software() -> None:
    cues = find_explicit_executable_cues(
        [
            {
                "evidence_id": "ev-module",
                "section_path": ["Results"],
                "text": "A polyhedral module connection algorithm was developed for structure analysis.",
            }
        ]
    )

    assert cues == []


def test_stage04_canonical_software_identifier_wins_alias_collision() -> None:
    mentions = [
        {
            "raw_name": "ORCA 4.2",
            "role": "core_compute",
            "actual_use": True,
            "evidence_ids": ["ev-orca"],
        }
    ]
    aliases = {"orca": ["ORCA"], "pyfrag": ["orca", "PyFrag"]}
    profile = {
        "backends": {
            "orca": {"availability": "declared_supported"},
            "pyfrag": {"availability": "declared_supported"},
        }
    }

    mappings = resolve_software(mentions, aliases, profile)

    assert mappings[0]["normalized_identifier"] == "orca"


def test_stage04_compound_plugin_resolves_rightmost_known_software() -> None:
    mentions = [
        {
            "raw_name": "HostEngine BiasEngine plugin",
            "role": "core_compute",
            "actual_use": True,
            "evidence_ids": ["ev-plugin"],
        }
    ]
    aliases = {"host": ["HostEngine"], "bias": ["BiasEngine"]}
    profile = {
        "backends": {
            "host": {"availability": "declared_supported"},
            "bias": {"availability": "declared_supported"},
        }
    }

    mappings = resolve_software(mentions, aliases, profile)

    assert mappings[0]["normalized_identifier"] == "bias"


@pytest.mark.parametrize(
    ("raw_name", "expected"),
    [("EngineX/Quickstep", "enginex")],
)
def test_stage04_decorated_method_name_resolves_single_known_engine(
    raw_name: str, expected: str
) -> None:
    aliases = {"enginex": ["EngineX"], "xtb": ["xTB"]}
    profile = {
        "backends": {
            "enginex": {"availability": "declared_supported"},
            "xtb": {"availability": "declared_supported"},
        }
    }
    mappings = resolve_software(
        [
            {
                "raw_name": raw_name,
                "role": "core_compute",
                "actual_use": True,
                "evidence_ids": ["ev-decorated"],
            }
        ],
        aliases,
        profile,
    )

    assert mappings[0]["normalized_identifier"] == expected


def test_stage04_hyphenated_distinct_program_is_not_split_into_command_alias() -> None:
    aliases = {"engine": ["ep"]}
    profile = {"backends": {"engine": {"availability": "declared_supported"}}}
    mappings = resolve_software(
        [
            {
                "raw_name": "EP-GEN",
                "role": "core_compute",
                "actual_use": True,
                "evidence_ids": ["ev-distinct"],
            }
        ],
        aliases,
        profile,
    )

    assert mappings[0]["catalog_present"] is False


def test_stage04_named_package_is_not_collapsed_to_parent_engine() -> None:
    aliases = {"host": ["HostEngine"]}
    profile = {"backends": {"host": {"availability": "declared_supported"}}}
    mappings = resolve_software(
        [
            {
                "raw_name": "HostEngine ELECTRODE package",
                "role": "core_compute",
                "actual_use": True,
                "evidence_ids": ["ev-package"],
            }
        ],
        aliases,
        profile,
    )

    assert mappings[0]["catalog_present"] is False


def test_stage03_incomplete_inventory_with_covered_engine_is_forwarded_as_probable() -> None:
    review = {
        "inventory_complete": False,
        "workflows": [
            {
                "steps": [
                    {"essential": True, "software": "ORCA"},
                ]
            }
        ],
    }
    mappings = [
        {
            "raw_name": "ORCA",
            "role": "core_compute",
            "actual_use": True,
            "catalog_present": True,
        }
    ]

    coverage = coverage_gate(review, mappings, {}, {})

    assert coverage == "covered"
    assert (
        _combine_decision(coverage, {"decision": "cost_unconfirmed"}, False)
        == "software_coverage_probable"
    )


def test_stage04_database_cue_is_not_merged_as_required_software() -> None:
    mentions = _merge_explicit_executable_cues(
        [],
        [
            {
                "raw_name": "ChEMBL",
                "entity_type": "library",
                "evidence_id": "ev-1",
                "context": "Training structures were taken from the ChEMBL database.",
            }
        ],
    )

    assert mentions == []


def test_stage04_sanitizer_drops_database_reported_as_program() -> None:
    quote = "Reference values were obtained from the CCCDB database."
    response = {
        "inventory_complete": True,
        "workflows": [],
        "software_mentions": [
            {
                "raw_name": "CCCDB",
                "entity_type": "program",
                "role": "required_preprocessing",
                "actual_use": True,
                "workflow_ids": [],
                "evidence_ids": ["ev-1"],
                "exact_quote": quote,
            }
        ],
        "resource_facts": [],
        "complexity_facts": [],
    }

    sanitized, warnings = _sanitize_review(response, {"ev-1": quote})

    assert sanitized["software_mentions"] == []
    assert [warning["reason"] for warning in warnings] == ["nonsoftware_data_resource"]


def test_stage04_sanitizer_drops_uniprot_data_resource() -> None:
    quote = "Protein sequences were obtained from the UniProt database."
    response = {
        "inventory_complete": True,
        "workflows": [],
        "software_mentions": [
            {
                "raw_name": "UniProt",
                "entity_type": "program",
                "role": "required_preprocessing",
                "actual_use": True,
                "workflow_ids": [],
                "evidence_ids": ["ev-1"],
                "exact_quote": quote,
            }
        ],
        "resource_facts": [],
        "complexity_facts": [],
    }

    sanitized, warnings = _sanitize_review(response, {"ev-1": quote})

    assert sanitized["software_mentions"] == []
    assert [warning["reason"] for warning in warnings] == ["nonsoftware_data_resource"]


def test_stage04_sanitizer_requires_step_local_software_attribution() -> None:
    method_quote = "Electronic-structure calculations were performed using VASP."
    response = {
        "inventory_complete": True,
        "workflows": [
            {
                "workflow_id": "wf-1",
                "evidence_ids": ["ev-method", "ev-analysis"],
                "steps": [
                    {
                        "step_id": "s-1",
                        "action": "perform charge partitioning analysis",
                        "essential": True,
                        "execution_layer": "named_software",
                        "software": "VASP",
                        "reported_settings": [],
                        "evidence_ids": ["ev-analysis"],
                    }
                ],
            }
        ],
        "software_mentions": [
            {
                "raw_name": "VASP",
                "entity_type": "program",
                "role": "core_compute",
                "actual_use": True,
                "workflow_ids": ["wf-1"],
                "evidence_ids": ["ev-method"],
                "exact_quote": method_quote,
            }
        ],
        "resource_facts": [],
        "complexity_facts": [],
    }

    sanitized, warnings = _sanitize_review(
        response,
        {
            "ev-method": method_quote,
            "ev-analysis": "Charge partitioning analysis was subsequently performed.",
        },
    )

    assert sanitized["workflows"][0]["steps"][0]["software"] is None
    assert sanitized["inventory_complete"] is False
    assert any(
        warning["reason"] == "nonsoftware_or_unsupported_executable_name" for warning in warnings
    )


def test_stage04_sanitizer_rejects_unnamed_python_core_runtime() -> None:
    response = {
        "inventory_complete": True,
        "workflows": [
            {
                "workflow_id": "wf-1",
                "evidence_ids": ["ev-1"],
                "steps": [
                    {
                        "step_id": "s-1",
                        "action": "train a machine-learning force field",
                        "essential": True,
                        "execution_layer": "task_specific_python",
                        "software": None,
                        "reported_settings": [],
                        "evidence_ids": ["ev-1"],
                    }
                ],
            }
        ],
        "software_mentions": [],
        "resource_facts": [],
        "complexity_facts": [],
    }

    sanitized, warnings = _sanitize_review(
        response, {"ev-1": "A machine-learning force field was trained."}
    )

    assert sanitized["workflows"][0]["steps"][0]["execution_layer"] == "unknown"
    assert sanitized["inventory_complete"] is False
    assert any(
        warning["reason"] == "core_runtime_cannot_use_unnamed_task_specific_python"
        for warning in warnings
    )


def test_stage03_contract_normalizer_separates_entity_type_from_role() -> None:
    response, warnings = _normalize_inventory_contract(
        {
            "workflows": [],
            "software_mentions": [
                {
                    "raw_name": "VESTA",
                    "entity_type": "visualization",
                    "role": "visualization",
                }
            ],
        }
    )

    assert response["software_mentions"][0]["entity_type"] == "program"
    assert response["software_mentions"][0]["role"] == "visualization"
    assert warnings[0]["reason"] == "role_value_moved_out_of_entity_type"


def test_stage03_sanitizer_resolves_host_module_and_drops_method_entity() -> None:
    module_quote = "The calculation was implemented in the SINGLE module of HostProgram."
    method_quote = "The density was expanded using the GPW approach."
    response = {
        "inventory_complete": True,
        "workflows": [
            {
                "workflow_id": "wf-1",
                "steps": [
                    {
                        "step_id": "s-1",
                        "action": "analyze states",
                        "essential": True,
                        "execution_layer": "named_software",
                        "software": "SINGLE",
                        "evidence_ids": ["module"],
                    },
                    {
                        "step_id": "s-2",
                        "action": "expand density",
                        "essential": True,
                        "execution_layer": "named_software",
                        "software": "GPW",
                        "evidence_ids": ["method"],
                    },
                ],
            }
        ],
        "software_mentions": [
            {
                "raw_name": "HostProgram",
                "entity_type": "program",
                "role": "core_compute",
                "actual_use": True,
                "workflow_ids": ["wf-1"],
                "evidence_ids": ["module"],
                "exact_quote": module_quote,
            },
            {
                "raw_name": "SINGLE",
                "entity_type": "extension",
                "role": "required_analysis",
                "actual_use": True,
                "workflow_ids": ["wf-1"],
                "evidence_ids": ["module"],
                "exact_quote": module_quote,
            },
            {
                "raw_name": "GPW",
                "entity_type": "extension",
                "role": "core_compute",
                "actual_use": True,
                "workflow_ids": ["wf-1"],
                "evidence_ids": ["method"],
                "exact_quote": method_quote,
            },
        ],
        "resource_facts": [],
        "complexity_facts": [],
        "evidence_ids": ["module", "method"],
    }

    sanitized, warnings = _sanitize_review(
        response, {"module": module_quote, "method": method_quote}
    )

    assert [row["raw_name"] for row in sanitized["software_mentions"]] == ["HostProgram"]
    assert sanitized["workflows"][0]["steps"][0]["software"] == "HostProgram"
    assert sanitized["workflows"][0]["steps"][1]["software"] is None
    assert sanitized["inventory_complete"] is False
    assert {warning["reason"] for warning in warnings} >= {
        "bundled_module_resolved_to_named_host",
        "bundled_module_not_separate_software",
        "method_or_process_removed_from_software_step",
        "method_or_process_not_software",
    }


def test_stage03_sanitizer_drops_generic_computation_label_as_software() -> None:
    quote = "To examine the active site, we employed MD simulations."
    response = {
        "inventory_complete": False,
        "workflows": [
            {
                "workflow_id": "wf-1",
                "steps": [
                    {
                        "step_id": "s-1",
                        "action": "simulate the active site",
                        "essential": True,
                        "execution_layer": "named_software",
                        "software": "MD simulations",
                        "evidence_ids": ["ev-1"],
                    }
                ],
            }
        ],
        "software_mentions": [
            {
                "raw_name": "MD simulations",
                "entity_type": "program",
                "role": "core_compute",
                "actual_use": True,
                "workflow_ids": ["wf-1"],
                "evidence_ids": ["ev-1"],
                "exact_quote": quote,
            }
        ],
        "resource_facts": [],
        "complexity_facts": [],
        "evidence_ids": ["ev-1"],
    }

    sanitized, warnings = _sanitize_review(response, {"ev-1": quote})

    assert sanitized["software_mentions"] == []
    assert sanitized["workflows"][0]["steps"][0]["software"] is None
    assert sanitized["workflows"][0]["steps"][0]["execution_layer"] == "unknown"
    assert {warning["reason"] for warning in warnings} >= {
        "method_or_process_removed_from_software_step",
        "method_or_process_not_software",
    }


def test_stage04_string_software_array_violates_contract() -> None:
    errors = _inventory_contract_errors(
        {
            "inventory_complete": True,
            "workflows": [],
            "software_mentions": ["VASP", "LAMMPS"],
            "excluded_entities": [],
        }
    )

    assert errors == [
        "software_mentions[0]_not_object",
        "software_mentions[1]_not_object",
    ]


def test_stage04_contract_repair_replaces_invalid_string_array() -> None:
    valid = {
        "inventory_complete": True,
        "workflows": [],
        "software_mentions": [],
        "excluded_entities": [],
        "resource_facts": [],
        "complexity_facts": [],
        "unresolved": [],
        "evidence_ids": [],
        "confidence": "high",
        "rationale": "No software was named.",
    }

    class Model:
        config = {"context_window_tokens": 32768}

        def __init__(self):
            self.calls = []

        def call_json(self, **kwargs):
            self.calls.append(kwargs)
            return valid, {"finish_reason": "stop", "request_hash": "repair"}

    model = Model()
    response, audit = _repair_inventory_contract(
        model,
        paper_id="paper-1",
        previous_response={"software_mentions": ["VASP"], "workflows": []},
        errors=["software_mentions[0]_not_object"],
        max_tokens=4096,
    )

    assert response == valid
    assert audit["contract_retry_count"] == 1
    assert len(model.calls) == 1


@pytest.mark.parametrize(
    "text",
    [
        "The backbone constraints simulating the experimental protein framework were applied.",
        "The HSAPO-34 framework was used for adsorption simulations.",
        "The calculation waited for emails from scheduling software.",
        "The SSSP pseudopotential library was used for the plane-wave calculation.",
        "The color code was used to distinguish atoms in the figure.",
        "Supporting Information is available using the Online program link.",
        "The collective variable was implemented using COORDINATIONNUMBER in PLUMED.",
        "Predictions were performed using the GNN model.",
    ],
)
def test_stage04_explicit_executable_cues_reject_nonsoftware_phrases(text: str) -> None:
    assert (
        find_explicit_executable_cues(
            [{"evidence_id": "ev-1", "section_path": ["Methods"], "text": text}]
        )
        == []
    )


def test_stage04_explicit_cue_deduplicates_partial_known_software_name() -> None:
    blocks = [
        {
            "evidence_id": "ev-1",
            "section_path": ["Methods"],
            "text": "Calculations were performed using the Quantum Espresso software package.",
        }
    ]
    known = [
        {
            "raw_name": "Quantum Espresso",
            "backend_hint": "quantum_espresso",
            "evidence_id": "ev-1",
        }
    ]

    assert find_explicit_executable_cues(blocks, known) == []


def test_stage04_explicit_cue_does_not_extract_possessive_author_as_program() -> None:
    text = "Trajectories were propagated as implemented in Singleton's Progdyn program."

    cues = find_explicit_executable_cues(
        [{"evidence_id": "ev-1", "section_path": ["Methods"], "text": text}]
    )

    assert all(item["raw_name"] != "Singleton" for item in cues)


def test_stage04_sanitizer_drops_possessive_author_fragment() -> None:
    quote = "Trajectories were propagated as implemented in Singleton's Progdyn program."
    response = {
        "workflows": [
            {
                "workflow_id": "wf-1",
                "steps": [
                    {
                        "step_id": "step-1",
                        "description": "propagate trajectories",
                        "essential": True,
                        "software": "Singleton",
                        "required_action": None,
                        "reported_settings": [],
                        "evidence_ids": ["ev-1"],
                    }
                ],
                "evidence_ids": ["ev-1"],
            }
        ],
        "software_mentions": [
            {
                "raw_name": "Singleton",
                "normalized_hint": None,
                "entity_type": "program",
                "role": "core_compute",
                "actual_use": True,
                "evidence_ids": ["ev-1"],
                "exact_quote": quote,
            }
        ],
        "resource_facts": [],
        "inventory_complete": True,
        "missing_information": [],
        "reason": "",
    }

    sanitized, warnings = _sanitize_review(response, {"ev-1": quote})

    assert sanitized["software_mentions"] == []
    assert any(
        warning["reason"] == "possessive_author_fragment_not_software" for warning in warnings
    )


def test_stage04_definitive_uncovered_software_precedes_unknown_step() -> None:
    review = {
        "workflows": [
            {
                "workflow_id": "wf",
                "steps": [
                    {
                        "software": None,
                        "essential": True,
                        "required_action": None,
                    },
                    {
                        "software": "Molpro",
                        "essential": True,
                        "required_action": None,
                    },
                ],
            }
        ]
    }
    mappings = [
        {
            "raw_name": "Molpro",
            "normalized_backend": None,
            "actual_use": True,
            "role": "core_compute",
            "catalog_present": False,
            "availability": "unknown",
            "actions": [],
        }
    ]

    assert coverage_gate(review, mappings, {}, {}) == "core_software_uncovered"


def test_stage04_definitive_uncovered_software_precedes_missing_workflow() -> None:
    mappings = [
        {
            "raw_name": "Tinker-HP",
            "normalized_backend": None,
            "actual_use": True,
            "role": "core_compute",
            "catalog_present": False,
            "availability": "unknown",
            "actions": [],
        }
    ]

    assert coverage_gate({"workflows": []}, mappings, {}, {}) == "core_software_uncovered"


def test_resource_range_crossing_limit_is_unconfirmed() -> None:
    result = resource_gate(
        [
            {
                "resource_type": "runtime_hours",
                "relation": "range",
                "value_min": 4,
                "value_max": 48,
                "scope": "single_job",
                "actual_computation": True,
            }
        ],
        {"runtime_hours": 24},
    )
    assert result["decision"] == "cost_unconfirmed"
    assert len(result["ambiguous_facts"]) == 1


def test_stage04_accepts_native_software_when_predefined_action_is_missing() -> None:
    review = {
        "workflows": [
            {
                "workflow_id": "wf",
                "steps": [
                    {
                        "software": "Gaussian 16",
                        "required_action": "propagate_dynamics",
                        "constraints": {},
                    }
                ],
            }
        ]
    }
    mappings = [
        {
            "raw_name": "Gaussian 16",
            "normalized_backend": "gaussian",
            "actual_use": True,
            "role": "core_compute",
            "catalog_present": True,
            "availability": "declared_supported",
            "local_installation_status": "not_evaluated",
            "actions": ["calculate_energy"],
            "constraint_snapshot": {},
        }
    ]

    assert coverage_gate(review, mappings, {}, {}) == "covered"


@pytest.mark.parametrize(
    ("backend", "settings", "constraints", "limitations"),
    [
        (
            "vasp",
            ["HSE hybrid functional", "600 eV encut"],
            {"xc_family": "lda, pbe, pbesol, scan, or r2scan"},
            [],
        ),
        (
            "gaussian",
            ["B3LYP*", "15% exact exchange"],
            {"method": "Gaussian SCF or DFT method keyword"},
            ["the adapter accepts no arbitrary route deck"],
        ),
    ],
)
def test_stage04_accepts_native_software_when_action_parameter_schema_is_narrower(
    backend, settings, constraints, limitations
) -> None:
    action = "calculate_periodic_energy" if backend == "vasp" else "calculate_energy"
    review = {
        "workflows": [
            {
                "workflow_id": "wf",
                "steps": [
                    {
                        "software": backend,
                        "normalized_backend": backend,
                        "required_action": action,
                        "essential": True,
                        "reported_settings": settings,
                    }
                ],
            }
        ]
    }
    mappings = [
        {
            "raw_name": backend,
            "normalized_backend": backend,
            "actual_use": True,
            "role": "core_compute",
            "catalog_present": True,
            "availability": "declared_supported",
            "local_installation_status": "not_evaluated",
            "actions": [action],
            "constraint_snapshot": {
                "method_constraints": constraints,
                "limitations": limitations,
            },
        }
    ]

    assert coverage_gate(review, mappings, {}, {}) == "covered"


def test_stage04_catalog_presence_does_not_require_runtime_verification() -> None:
    review = {
        "workflows": [
            {
                "workflow_id": "wf",
                "steps": [
                    {
                        "software": "CP2K",
                        "essential": True,
                        "required_action": None,
                        "reported_settings": ["AIMD with metadynamics"],
                    }
                ],
            }
        ]
    }
    mappings = [
        {
            "raw_name": "CP2K",
            "normalized_backend": "cp2k",
            "actual_use": True,
            "role": "core_compute",
            "catalog_present": True,
            "availability": "declared_supported",
            "local_installation_status": "not_evaluated",
            "actions": ["calculate_periodic_energy"],
        }
    ]

    assert (
        coverage_gate(
            review,
            mappings,
            {},
            {"required_coverage_level": "runtime_verified"},
        )
        == "covered"
    )


def test_stage04_explicit_resource_overrun_rejects_covered_software() -> None:
    assert (
        _combine_decision(
            "covered",
            {"decision": "cost_exceeds_budget", "exceeded_facts": [{"resource_type": "gpus"}]},
            True,
        )
        == "cost_exceeds_budget"
    )


def test_stage04_unknown_resource_cost_does_not_reject_by_itself() -> None:
    assert (
        _combine_decision("covered", {"decision": "cost_unconfirmed", "facts": []}, True)
        == "software_covered"
    )


def test_stage04_context_budget_reduces_output_before_model_limit() -> None:
    class Model:
        config = {"context_window_tokens": 16384, "context_safety_margin_tokens": 768}

    effective = _safe_output_tokens(Model(), "s" * 6000, "u" * 24000, 6144)

    assert 512 <= effective < 6144


def _stage05_fixture_candidate() -> dict:
    return {
        "candidate_id": "candidate-1",
        "task_direction": "molecular_dynamics_free_energy",
        "scientific_question": "Can the reported free-energy trend be reproduced?",
        "claim_reference": "Figure 3",
        "workflow_steps": ["prepare", "simulate", "analyze"],
        "validation_gates": ["convergence"],
        "public_input_requirements": "structures and parameters",
        "hidden_targets": "free energies",
        "scoring_metrics": ["MAE"],
        "ground_truth_level": "B",
        "required_software": "OpenMM, MDTraj, Packmol",
        "estimated_cost": {
            "runtime_hours": 4,
            "cpu_cores": 8,
            "gpus": 0,
            "job_count": 1,
            "basis": "one reported simulation",
            "confidence": "medium",
        },
        "buildability_checks": {
            "input_assets": "confirmed",
            "parameters": "confirmed",
            "ground_truth": "confirmed",
            "software": "confirmed",
            "cost": "confirmed",
        },
        "evidence_ids": ["mineru-1"],
        "significance_rationale": "Tests the central quantitative claim.",
    }


def _stage05_fixture_coverage() -> dict:
    return {
        "paper_id": "paper-1",
        "software_mappings": [
            {
                "raw_name": raw,
                "normalized_identifier": normalized,
                "normalized_backend": normalized,
                "catalog_present": True,
            }
            for raw, normalized in (
                ("OpenMM", "openmm"),
                ("MDTraj", "mdtraj"),
                ("Packmol", "packmol"),
            )
        ],
    }


def test_stage05_normalizes_software_string_without_character_set_bug() -> None:
    candidates, rejected = _validate_candidates(
        {"decision": "pass", "candidates": [_stage05_fixture_candidate()]},
        {"mineru-1"},
        _stage05_fixture_coverage(),
    )

    assert rejected == []
    assert candidates[0]["required_software"] == ["openmm", "mdtraj", "packmol"]
    assert candidates[0]["task_direction"] == "molecular_dynamics_free_energy"


def test_stage05_rejects_forward_as_invalid_taxonomy_direction_with_reason() -> None:
    candidate = _stage05_fixture_candidate()
    candidate["task_direction"] = "forward"

    candidates, rejected = _validate_candidates(
        {"decision": "pass", "candidates": [candidate]},
        {"mineru-1"},
        _stage05_fixture_coverage(),
    )

    assert candidates == []
    assert rejected[0]["reasons"] == ["invalid_task_direction"]


def test_stage05_rejects_stale_stage04_evidence_namespace_with_reason() -> None:
    candidate = _stage05_fixture_candidate()
    candidate["evidence_ids"] = ["grobid-old-id"]

    candidates, rejected = _validate_candidates(
        {"decision": "pass", "candidates": [candidate]},
        {"mineru-1"},
        _stage05_fixture_coverage(),
    )

    assert candidates == []
    assert "unknown_or_missing_mineru_evidence_ids" in rejected[0]["reasons"]
    assert rejected[0]["unknown_evidence_ids"] == ["grobid-old-id"]


def test_stage05_rejects_unconfirmed_buildability_and_unsupported_cost() -> None:
    candidate = _stage05_fixture_candidate()
    candidate["buildability_checks"]["input_assets"] = "uncertain"
    candidate["estimated_cost"]["runtime_hours"] = 48
    coverage = _stage05_fixture_coverage()
    coverage["resource_profile"] = {
        "budget": {
            "runtime_hours": 24,
            "cpu_cores": 128,
            "gpus": 1,
            "job_count": 1000,
            "core_hours": 3072,
            "gpu_hours": 24,
        }
    }

    candidates, rejected = _validate_candidates(
        {"decision": "pass", "candidates": [candidate]},
        {"mineru-1"},
        coverage,
    )

    assert candidates == []
    assert "buildability_not_confirmed" in rejected[0]["reasons"]
    assert "cost_estimate_missing_invalid_or_over_budget" in rejected[0]["reasons"]


def test_stage05_evidence_budget_preserves_main_and_supplementary_documents() -> None:
    from src.stages.stage05_benchmark_suitability.stage import _bounded_by_document

    blocks = [
        {"document_id": "main", "evidence_id": f"main-{index}", "text": "m" * 80}
        for index in range(4)
    ] + [
        {"document_id": "si", "evidence_id": f"si-{index}", "text": "s" * 80}
        for index in range(4)
    ]

    bounded = _bounded_by_document(blocks, 320)

    assert {row["document_id"] for row in bounded} == {"main", "si"}


def test_stage05_software_facts_prevent_covered_engine_from_becoming_a_blocker() -> None:
    coverage = _stage05_fixture_coverage()
    coverage["software_mappings"].append(
        {
            "raw_name": "UnknownEngine",
            "normalized_identifier": None,
            "normalized_backend": None,
            "catalog_present": False,
        }
    )

    facts = _software_coverage_facts(coverage)
    contradictions = _software_fact_contradictions(
        {"decision": "abstain", "blocking_software": ["OpenMM"]}, coverage
    )

    assert facts["uncovered_required_software"] == [
        {"paper_name": "UnknownEngine", "toolbox_identifier": None}
    ]
    assert contradictions[0]["candidate_id"] == "response-software-facts"


def test_stage05_allows_only_declared_uncovered_software_as_a_blocker() -> None:
    coverage = _stage05_fixture_coverage()
    coverage["software_mappings"].append(
        {"raw_name": "UnknownEngine", "catalog_present": False}
    )
    assert (
        _software_fact_contradictions(
            {"decision": "abstain", "blocking_software": ["UnknownEngine"]}, coverage
        )
        == []
    )


def test_stage05_abstention_contract_couples_software_dimension_and_blockers() -> None:
    assert _response_contract_rejections(
        {
            "decision": "abstain",
            "blocking_dimensions": ["software"],
            "blocking_software": [],
        },
        _stage05_fixture_coverage(),
    ) == [
        {
            "candidate_id": "response-contract",
            "reasons": ["software_dimension_and_blocking_software_disagree"],
        }
    ]
    assert (
        _response_contract_rejections(
            {
                "decision": "abstain",
                "blocking_dimensions": ["cost"],
                "blocking_software": [],
            },
            _stage05_fixture_coverage(),
        )
        == []
    )

    unresolved = _stage05_fixture_coverage()
    unresolved["coverage_decision"] = "software_inventory_unconfirmed"
    assert (
        _response_contract_rejections(
            {
                "decision": "abstain",
                "blocking_dimensions": ["software"],
                "blocking_software": [],
            },
            unresolved,
        )
        == []
    )

def test_stage05_packet_removes_nested_stage04_evidence_ids() -> None:
    value = {
        "workflow_inventory": [
            {
                "evidence_ids": ["old-workflow"],
                "steps": [{"action": "DFT", "evidence_ids": ["old-step"]}],
            }
        ],
        "software_mappings": [{"raw_name": "VASP", "evidence_ids": ["old-software"]}],
    }

    assert "evidence_ids" not in json.dumps(_without_evidence_ids(value))


def test_public_builder_packet_never_contains_hidden_reference() -> None:
    packet = _public_builder_packet(
        {
            "task_pair_id": "pair",
            "scientific_record": {"question": "q"},
            "hidden_reference": {"answer": "secret"},
            "required_assets": [],
            "allowed_backends": ["gaussian"],
            "allowed_actions": ["calculate_energy"],
            "budget": {},
        },
        "autonomous",
    )
    assert "hidden_reference" not in packet
    assert "secret" not in json.dumps(packet)


def _base_config(tmp_path: Path) -> dict:
    models = {
        role: {
            "base_url": "http://fixture/v1",
            "model": role,
            "api_key_env": f"{role.upper()}_KEY",
            "enabled": True,
        }
        for role in ("screening", "suitability", "builder", "judge")
    }
    return {
        "pipeline_contract": "researchchembench-data-pipeline/v2",
        "workspace": str(tmp_path / "run"),
        "source": {"root": str(tmp_path)},
        "stop_after": "stage07",
        "models": models,
        "stage01": {"normalization": {}},
        "stage02": {"model_role": "screening"},
        "stage03": {
            "model_role": "screening",
            "toolbox_capabilities": str(tmp_path / "profile.json"),
            "software_aliases": str(tmp_path / "aliases.json"),
        },
        "stage04": {"mineru": {"enabled": False}},
        "stage05": {"model_role": "suitability"},
        "stage06": {"model_role": "builder"},
        "stage07": {"model_role": "judge"},
    }
