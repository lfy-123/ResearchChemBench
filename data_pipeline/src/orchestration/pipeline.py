from __future__ import annotations

from pathlib import Path
from typing import Any

from src.core.config import normalize_config
from src.core.io import read_json, write_json, write_jsonl
from src.core.logging import configure_pipeline_logging, pipeline_logger
from src.curation.availability import assess_asset_availability
from src.curation.extract import extract_records
from src.curation.llm_extract import review_records
from src.curation.model_review import ensemble_summary, review_with_ensemble
from src.curation.package_generation import (
    generate_complete_packages,
    package_generation_summary,
)
from src.curation.quality_gates import (
    apply_ensemble_results,
    gate_scientific_records,
    quality_funnel_summary,
)
from src.curation.task_selection import select_task_types, selection_summary
from src.curation.toolbox import load_toolbox_profile
from src.delivery.build import build_dataset
from src.delivery.reference_run import attach_reference_runs, reference_run_summary
from src.delivery.validate import validate_dataset
from src.discovery.query import expand_seeds
from src.discovery.screen import screen_papers
from src.discovery.search import retrieval_summary, search_offline, search_openalex
from src.ingestion.corpus import inventory_corpus, markdown_metadata
from src.ingestion.dedupe import deduplicate
from src.ingestion.deep_parse import build_mineru_queue, deep_text_map, run_mineru_queue
from src.ingestion.deep_quality import assess_deep_parse_quality, deep_quality_summary
from src.ingestion.grobid import extract_documents_with_grobid, grobid_service
from src.ingestion.grobid_quantities import grobid_quantities_service
from src.ingestion.softcite import softcite_service
from src.ingestion.study_bundle import build_study_bundles, member_bundle_map
from src.screening.computation_completeness import (
    assess_computation_completeness,
    computation_completeness_summary,
)
from src.screening.resource_limits import assess_resource_limits, resource_limits_summary
from src.screening.software_coverage import assess_software_coverage, software_coverage_summary


def run_pipeline(config_path: str | Path) -> dict[str, Any]:
    config_path = Path(config_path).resolve()
    base = config_path.parent
    config = normalize_config(read_json(config_path), base)
    workspace = _resolve(base, config.get("workspace", "work"))
    log_path = _resolve(base, config.get("log_file", workspace / "pipeline.log"))
    logger = configure_pipeline_logging(log_path)
    source_mode = (config.get("source") or {}).get("mode", "search")
    logger.info(
        "PIPELINE START | mode=%s | config=%s | workspace=%s",
        source_mode,
        config_path,
        workspace,
    )
    try:
        if source_mode == "corpus":
            result = run_corpus_pipeline(config_path, config, base)
        elif source_mode in {"search", "seed_search"}:
            result = run_search_pipeline(config_path, config, base)
        else:
            raise ValueError(f"Unsupported source mode: {source_mode}")
    except Exception:
        logger.exception("PIPELINE FAILED")
        raise
    logger.info("PIPELINE COMPLETE | summary=%s", result)
    return result


def run_search_pipeline(
    config_path: Path,
    config: dict[str, Any],
    base: Path,
) -> dict[str, Any]:
    workspace = _resolve(base, config.get("workspace", "work"))
    workspace.mkdir(parents=True, exist_ok=True)

    seeds = read_json(_resolve(base, config["seeds"]))
    queries = expand_seeds(seeds, config.get("query", {}).get("max_per_tier", 12))
    write_jsonl(workspace / "01_queries.jsonl", queries)

    search_config = config.get("search", {})
    provider = search_config.get("provider", "offline")
    if provider == "openalex":
        retrieved = search_openalex(
            queries,
            per_query=search_config.get("per_query", 20),
            mailto=search_config.get("mailto"),
            delay_seconds=search_config.get("delay_seconds", 0.1),
        )
    elif provider == "offline":
        candidates = read_json(_resolve(base, search_config["candidates"]))
        retrieved = search_offline(
            queries,
            candidates,
            min_overlap=search_config.get("min_overlap", 0.08),
            per_query=search_config.get("per_query", 50),
        )
    else:
        raise ValueError(f"Unsupported search provider: {provider}")
    write_jsonl(workspace / "02_retrieved.jsonl", retrieved)
    write_json(workspace / "02_retrieval_summary.json", retrieval_summary(retrieved))

    papers = deduplicate(retrieved, config.get("dedupe", {}).get("fuzzy_threshold", 0.97))
    write_jsonl(workspace / "03_deduplicated.jsonl", papers)

    screened = screen_papers(
        papers,
        seeds,
        threshold=config.get("screen", {}).get("threshold", 35.0),
    )
    write_jsonl(workspace / "04_screened.jsonl", screened)

    asset_path = config.get("assets")
    assets = _load_assets(base, asset_path) if asset_path else []
    study_bundles = build_study_bundles(screened, assets)
    bundle_map = member_bundle_map(study_bundles)
    screened = [
        {**paper, "study_bundle": bundle_map.get(paper["paper_id"], {})}
        for paper in screened
        if not bundle_map.get(paper["paper_id"])
        or bundle_map[paper["paper_id"]]["primary_paper_id"] == paper["paper_id"]
    ]
    write_json(workspace / "04_study_bundles.json", study_bundles)
    records = extract_records(
        screened,
        assets,
        include_review=config.get("extract", {}).get("include_review", False),
    )
    semantic_config = config.get("semantic_review", {})
    if semantic_config.get("enabled"):
        records = review_records(records, semantic_config)
    records = select_task_types(records, config.get("task_selection"))
    write_json(workspace / "05_task_selection_summary.json", selection_summary(records))
    write_jsonl(workspace / "05_selected_records.jsonl", records)
    records = generate_complete_packages(records, config.get("package_generation"))
    write_json(
        workspace / "06_package_generation_summary.json", package_generation_summary(records)
    )
    write_jsonl(workspace / "06_scientific_records_raw.jsonl", records)
    _write_candidate_exports(records, workspace / "06_candidate_packages")
    records = attach_reference_runs(records, _resolve_reference_config(config, base))
    write_json(workspace / "06_reference_run_summary.json", reference_run_summary(records))

    records, toolbox_profile = _run_quality_funnel(records, config, base, workspace)

    output_dir = _resolve(base, config.get("output", "dataset"))
    build_records = _records_for_build(records, config.get("build", {}), corpus_mode=False)
    manifest = build_dataset(
        build_records,
        output_dir,
        allow_failed_quality=config.get("build", {}).get("allow_failed_quality", False),
        split_salt=config.get("build", {}).get("split_salt", "researchchembench-v1"),
        require_reference_run=config.get("build", {}).get("require_reference_run", True),
    )
    validation = validate_dataset(
        output_dir,
        require_tasks=not config.get("validation", {}).get("allow_empty", False),
    )
    write_json(workspace / "10_validation_report.json", validation)
    return {
        "source_mode": "search",
        "config": str(config_path),
        "workspace": str(workspace),
        "output": str(output_dir),
        "queries": len(queries),
        "retrieved_rows": len(retrieved),
        "unique_papers": len(papers),
        "scientific_records": len(records),
        "toolbox_catalog_hash": (toolbox_profile or {}).get("catalog_hash"),
        "tasks_built": manifest["task_count"],
        "tasks_skipped": len(manifest["skipped"]),
        "validation": _validation_summary(validation),
    }


def run_corpus_pipeline(
    config_path: Path,
    config: dict[str, Any],
    base: Path,
) -> dict[str, Any]:
    workspace = _resolve(base, config.get("workspace", "work"))
    workspace.mkdir(parents=True, exist_ok=True)
    source = config["source"]
    corpus_root = _resolve(base, source["root"])
    _write_corpus_stage_index(workspace)

    stage = _stage_dir(workspace, "stage_01_inventory")
    inventory = inventory_corpus(corpus_root)
    exclude_supplementary = bool(source.get("exclude_supplementary", True))
    supplementary_inventory = [
        item for item in inventory if item.get("document_role") == "supplementary"
    ]
    eligible_inventory = [
        item
        for item in inventory
        if not exclude_supplementary or item.get("document_role") != "supplementary"
    ]
    canonical_inventory = [item for item in eligible_inventory if not item.get("duplicate_of")]
    duplicate_inventory = [item for item in inventory if item.get("duplicate_of")]
    write_jsonl(stage / "corpus_inventory.jsonl", inventory)
    write_jsonl(stage / "pdf_paths.jsonl", _pdf_path_rows(inventory, "inventory_status"))
    write_jsonl(
        stage / "canonical_pdf_paths.jsonl",
        _pdf_path_rows(canonical_inventory, "inventory_status"),
    )
    write_jsonl(
        stage / "duplicate_pdf_paths.jsonl",
        _pdf_path_rows(duplicate_inventory, "inventory_status"),
    )
    write_jsonl(
        stage / "supplementary_pdf_paths.jsonl",
        _pdf_path_rows(supplementary_inventory, "document_role"),
    )
    write_jsonl(
        stage / "main_paper_pdf_paths.jsonl",
        _pdf_path_rows(
            [item for item in inventory if item.get("document_role") == "main_paper"],
            "document_role",
        ),
    )
    _write_stage_summary(
        stage,
        {
            "pdf_files": len(inventory),
            "canonical_pdfs": sum(1 for item in inventory if not item.get("duplicate_of")),
            "duplicate_pdfs": sum(1 for item in inventory if item.get("duplicate_of")),
            "supplementary_pdfs": len(supplementary_inventory),
            "supplementary_excluded": (
                len(supplementary_inventory) if exclude_supplementary else 0
            ),
            "downstream_main_papers": len(canonical_inventory),
        },
    )

    grobid_config = config.get("grobid_extract", {})
    stage = _stage_dir(workspace, "stage_02_grobid_extract")
    with grobid_service(grobid_config) as client:
        extracted_records = extract_documents_with_grobid(
            canonical_inventory,
            client,
            _resolve(base, grobid_config.get("tei_dir", str(stage / "tei"))),
            _resolve(base, grobid_config.get("text_dir", str(stage / "text"))),
            max_chars=grobid_config.get("max_chars", 2_000_000),
            reuse_existing=grobid_config.get("reuse_existing", True),
            exclude_supplementary=exclude_supplementary,
        )
    write_jsonl(stage / "documents.jsonl", extracted_records)
    _write_stage_summary(
        stage,
        {
            **_field_summary(extracted_records, "grobid_extract_status", "documents"),
            "input_pdf_files": len(inventory),
            "duplicates_excluded": len(duplicate_inventory),
            "supplementary_excluded": (
                len(supplementary_inventory) if exclude_supplementary else 0
            ),
        },
    )

    if config.get("stop_after") == "grobid_extract":
        return {
            "source_mode": "corpus",
            "stopped_after": "grobid_extract",
            "config": str(config_path),
            "corpus_root": str(corpus_root),
            "workspace": str(workspace),
            "pdf_files": len(inventory),
            "supplementary_excluded": (
                len(supplementary_inventory) if exclude_supplementary else 0
            ),
            "canonical_main_papers": len(canonical_inventory),
            "grobid_documents": len(extracted_records),
            "grobid_success": sum(
                1
                for item in extracted_records
                if item.get("grobid_extract_status") in {"success", "reused"}
            ),
        }

    toolbox_profile = _load_toolbox_profile(config, base)
    software_config = config.get("software_coverage", {})
    stage = _stage_dir(workspace, "stage_03_software_coverage")
    with softcite_service(software_config) as client:
        software_records = assess_software_coverage(
            extracted_records,
            client,
            toolbox_profile or {},
            aliases_file=_resolve(base, software_config["aliases_file"]),
            role_rules_file=_resolve(base, software_config["role_rules_file"]),
            capability_map_file=_resolve(base, software_config["capability_map_file"]),
            raw_output_dir=stage / "softcite_raw",
        )
    write_jsonl(stage / "software_coverage_documents.jsonl", software_records)
    write_jsonl(
        stage / "direct_covered_pdf_paths.jsonl",
        _pdf_path_rows(
            [
                item
                for item in software_records
                if (item.get("software_coverage") or {}).get("decision") == "direct_covered"
            ]
        ),
    )
    write_jsonl(
        stage / "capability_equivalent_pdf_paths.jsonl",
        _pdf_path_rows(
            [
                item
                for item in software_records
                if (item.get("software_coverage") or {}).get("decision")
                == "capability_equivalent"
            ]
        ),
    )
    software_summary = software_coverage_summary(software_records)
    _write_stage_summary(stage, software_summary)
    if config.get("stop_after") == "software_coverage":
        return _screening_stop_summary(
            config_path,
            corpus_root,
            workspace,
            inventory,
            software_summary=software_summary,
        )

    stage = _stage_dir(workspace, "stage_04_computation_completeness")
    completeness_inputs = [
        item
        for item in software_records
        if (item.get("software_coverage") or {}).get("decision") == "direct_covered"
    ]
    completeness_records = assess_computation_completeness(
        completeness_inputs,
        config.get("computation_completeness", {}),
        output_dir=stage,
    )
    write_jsonl(stage / "computation_completeness_documents.jsonl", completeness_records)
    write_jsonl(
        stage / "selected_pdf_paths.jsonl",
        _pdf_path_rows(
            [
                item
                for item in completeness_records
                if (item.get("computation_completeness") or {}).get("passed")
            ]
        )
    )
    completeness_summary = computation_completeness_summary(completeness_records)
    _write_stage_summary(stage, completeness_summary)
    if config.get("stop_after") == "computation_completeness":
        return _screening_stop_summary(
            config_path,
            corpus_root,
            workspace,
            inventory,
            software_summary=software_summary,
            completeness_summary=completeness_summary,
        )

    stage = _stage_dir(workspace, "stage_05_resource_limits")
    resource_inputs = [
        item
        for item in completeness_records
        if (item.get("computation_completeness") or {}).get("passed")
    ]
    quantities_config = config.get("grobid_quantities", {})
    with grobid_quantities_service(quantities_config) as client:
        classified = assess_resource_limits(
            resource_inputs,
            client,
            config.get("resource_limits", {}),
            output_dir=stage,
        )
    write_jsonl(stage / "resource_screened_documents.jsonl", classified)
    write_jsonl(
        stage / "selected_pdf_paths.jsonl",
        _pdf_path_rows(
            [item for item in classified if (item.get("resource_limits") or {}).get("passed")]
        ),
    )
    resource_summary = resource_limits_summary(classified)
    _write_stage_summary(stage, resource_summary)
    if config.get("stop_after") == "resource_limits":
        return _screening_stop_summary(
            config_path,
            corpus_root,
            workspace,
            inventory,
            software_summary=software_summary,
            completeness_summary=completeness_summary,
            resource_summary=resource_summary,
        )
    classified = [
        item for item in classified if (item.get("resource_limits") or {}).get("passed")
    ]

    mineru_config = config.get("mineru", {})
    stage = _stage_dir(workspace, "stage_06_mineru_queue")
    queue = build_mineru_queue(
        classified,
        include_optional=mineru_config.get("include_optional", False),
        limit=mineru_config.get("limit"),
    )
    write_jsonl(stage / "mineru_queue.jsonl", queue)
    write_jsonl(stage / "selected_pdf_paths.jsonl", _pdf_path_rows(queue, "deep_parse_decision"))
    _write_stage_summary(
        stage,
        _field_summary(queue, "deep_parse_decision", "queued_documents"),
    )
    mineru_results = run_mineru_queue(
        queue,
        _resolve(
            base,
            mineru_config.get(
                "output_dir", str(_stage_dir(workspace, "stage_07_mineru_parse") / "mineru")
            ),
        ),
        execute=mineru_config.get("execute", False),
        command=_resolve_command(base, mineru_config.get("command", "mineru")),
        method=mineru_config.get("method", "auto"),
        backend=mineru_config.get("backend"),
        timeout_seconds=mineru_config.get("timeout_seconds", 3600),
        environment=mineru_config.get("environment"),
        extra_args=mineru_config.get("extra_args"),
        reuse_existing=mineru_config.get("reuse_existing", True),
        min_markdown_chars=mineru_config.get("min_markdown_chars", 1000),
    )
    stage = _stage_dir(workspace, "stage_07_mineru_parse")
    write_jsonl(stage / "mineru_results_raw.jsonl", mineru_results)
    _write_stage_summary(stage, _field_summary(mineru_results, "status", "documents"))
    stage = _stage_dir(workspace, "stage_08_deep_parse_quality")
    deep_quality_config = config.get("deep_parse_quality", {})
    mineru_results = assess_deep_parse_quality(
        classified,
        mineru_results,
        min_title_recall=deep_quality_config.get("min_title_recall", 0.7),
        min_grobid_vocab_recall=deep_quality_config.get("min_grobid_vocab_recall", 0.65),
        min_key_term_coverage=deep_quality_config.get("min_key_term_coverage", 0.5),
        min_length_ratio=deep_quality_config.get("min_length_ratio", 0.25),
        max_length_ratio=deep_quality_config.get("max_length_ratio", 2.5),
    )
    write_jsonl(stage / "mineru_results_with_quality.jsonl", mineru_results)
    _write_stage_summary(stage, deep_quality_summary(mineru_results))

    deep_paths = deep_text_map(mineru_results)
    deep_result_map = {item["paper_id"]: item for item in mineru_results}
    stage = _stage_dir(workspace, "stage_09_post_mineru_merge")
    refined_inputs = []
    for document in classified:
        refined = dict(document)
        if document["paper_id"] in deep_paths:
            refined["deep_text_path"] = deep_paths[document["paper_id"]]
            deep_metadata = markdown_metadata(
                Path(deep_paths[document["paper_id"]]).read_text(encoding="utf-8", errors="replace")
            )
            if deep_metadata.get("title"):
                refined["title"] = deep_metadata["title"]
            if deep_metadata.get("abstract"):
                refined["abstract"] = deep_metadata["abstract"]
            if deep_metadata.get("section_headings"):
                refined["section_headings"] = deep_metadata["section_headings"]
        refined_inputs.append(refined)
    classified = refined_inputs
    write_jsonl(stage / "merged_documents.jsonl", classified)
    write_jsonl(stage / "selected_pdf_paths.jsonl", _pdf_path_rows(classified))
    _write_stage_summary(
        stage,
        {
            "documents": len(classified),
            "mineru_text_attached": sum(1 for item in classified if item.get("deep_text_path")),
            "grobid_text_fallback": sum(1 for item in classified if not item.get("deep_text_path")),
        },
    )

    stage = _stage_dir(workspace, "stage_10_extraction_ready")
    write_jsonl(stage / "extraction_ready_documents.jsonl", classified)
    write_jsonl(stage / "selected_pdf_paths.jsonl", _pdf_path_rows(classified))
    _write_stage_summary(stage, {"documents": len(classified), "status": "ready"})

    stage = _stage_dir(workspace, "stage_11_study_bundles")
    explicit_assets = _load_assets(base, config["assets"]) if config.get("assets") else []
    explicit_map = {item["paper_id"]: item for item in explicit_assets}
    study_bundles = build_study_bundles(classified, explicit_assets)
    bundle_map = member_bundle_map(study_bundles)
    write_json(stage / "study_bundles.json", study_bundles)
    assets = []
    extractable = []
    for document in classified:
        bundle = bundle_map.get(document["paper_id"], {})
        if bundle and bundle.get("primary_paper_id") != document["paper_id"]:
            continue
        if document.get("duplicate_of") or not (document.get("resource_limits") or {}).get(
            "passed", False
        ):
            continue
        document = {**document, "study_bundle": bundle}
        extractable.append(document)
        asset = {
            "paper_id": document["paper_id"],
            "paper": bundle.get("main_paper_path") or document["source_path"],
            "prefer_text_assets": True,
            "supplementary": bundle.get("supplementary_paths", []),
            "text": [
                deep_paths.get(member_id)
                or next(
                    (item.get("text_path") for item in classified if item["paper_id"] == member_id),
                    None,
                )
                for member_id in bundle.get("member_paper_ids", [document["paper_id"]])
                if deep_paths.get(member_id)
                or next(
                    (item.get("text_path") for item in classified if item["paper_id"] == member_id),
                    None,
                )
            ],
            "parser": "mineru" if document["paper_id"] in deep_paths else "grobid",
            "deep_parse": {
                key: value
                for key, value in deep_result_map.get(document["paper_id"], {}).items()
                if key
                in {
                    "status",
                    "duration_seconds",
                    "markdown_path",
                    "content_list_v2_path",
                    "structured_pages",
                    "image_count",
                    "deep_parse_quality",
                }
            },
            "visible_data": {},
        }
        asset.update(explicit_map.get(document["paper_id"], {}))
        assets.append(asset)
    write_json(stage / "generated_assets.json", assets)
    write_jsonl(stage / "selected_pdf_paths.jsonl", _pdf_path_rows(extractable))
    _write_stage_summary(
        stage,
        {
            "study_bundles": len(study_bundles),
            "extractable_documents": len(extractable),
            "generated_assets": len(assets),
        },
    )

    stage = _stage_dir(workspace, "stage_12_scientific_record_extraction")
    records = extract_records(extractable, assets, include_review=True)
    write_jsonl(stage / "deterministic_records.jsonl", records)
    semantic_config = config.get("semantic_review", {})
    if semantic_config.get("enabled"):
        records = review_records(records, semantic_config)
    write_jsonl(stage / "semantic_review_records.jsonl", records)
    quality_config = config.get("quality_funnel", {})
    asset_config = {**quality_config, **config.get("asset_discovery", {})}
    records = _attach_asset_availability(records, asset_config)
    write_jsonl(stage / "asset_discovery_records.jsonl", records)
    write_jsonl(
        stage / "asset_acquisition_queue.jsonl",
        [_asset_acquisition_queue_item(record) for record in records],
    )
    _write_stage_summary(
        stage,
        {
            "extractable_documents": len(extractable),
            "scientific_records": len(records),
            "semantic_review_enabled": bool(semantic_config.get("enabled")),
        },
    )
    stage = _stage_dir(workspace, "stage_13_task_selection")
    records = select_task_types(records, config.get("task_selection"))
    write_jsonl(stage / "selected_records.jsonl", records)
    write_jsonl(stage / "selected_pdf_paths.jsonl", _record_pdf_path_rows(records))
    _write_stage_summary(stage, selection_summary(records))
    stage = _stage_dir(workspace, "stage_14_package_generation")
    records = generate_complete_packages(records, config.get("package_generation"))
    package_summary = package_generation_summary(records)
    write_json(stage / "package_generation_summary.json", package_summary)
    write_jsonl(stage / "scientific_records_raw.jsonl", records)
    _write_candidate_exports(records, stage / "candidate_packages")
    records = attach_reference_runs(records, _resolve_reference_config(config, base))
    write_jsonl(stage / "records_with_reference_runs.jsonl", records)
    reference_summary = reference_run_summary(records)
    write_json(stage / "reference_run_summary.json", reference_summary)
    _write_stage_summary(
        stage,
        {"package_generation": package_summary, "reference_runs": reference_summary},
    )
    stage = _stage_dir(workspace, "stage_15_quality_gates")
    records = gate_scientific_records(records, toolbox_profile, quality_config)
    write_jsonl(stage / "quality_gated_records.jsonl", records)
    _write_stage_summary(stage, quality_funnel_summary(records))

    stage = _stage_dir(workspace, "stage_16_model_ensemble")
    records = review_with_ensemble(records, _load_model_ensemble_config(config, base))
    records = apply_ensemble_results(records)
    write_jsonl(stage / "model_reviewed_records.jsonl", records)
    _write_stage_summary(stage, ensemble_summary(records))
    _write_candidate_exports(
        records,
        _stage_dir(workspace, "stage_14_package_generation") / "candidate_packages",
    )
    stage = _stage_dir(workspace, "stage_17_curation_queue")
    curation_queue = [_curation_queue_item(record) for record in records]
    curation_queue = [item for item in curation_queue if item["selected_task_type"]]
    curation_queue.sort(key=lambda item: (item["priority_rank"], item["paper_id"]))
    write_jsonl(stage / "curation_queue.jsonl", curation_queue)
    write_jsonl(stage / "selected_pdf_paths.jsonl", _pdf_path_rows(curation_queue))
    _write_stage_summary(
        stage,
        {
            "candidates": len(curation_queue),
            "selected_task_types": _value_counts(
                item.get("selected_task_type") for item in curation_queue
            ),
            "task_decisions": _value_counts(item.get("task_decision") for item in curation_queue),
        },
    )

    if config.get("stop_after") == "model_ensemble":
        return {
            "source_mode": "corpus",
            "stopped_after": "model_ensemble",
            "config": str(config_path),
            "corpus_root": str(corpus_root),
            "workspace": str(workspace),
            "pdf_files": len(inventory),
            "canonical_pdfs": sum(1 for item in inventory if not item.get("duplicate_of")),
            "software_direct_covered": software_summary["direct_covered"],
            "computation_stage_passed": sum(
                1
                for item in completeness_records
                if (item.get("computation_completeness") or {}).get("passed")
            ),
            "resource_stage_passed": len(classified),
            "mineru_queue": len(queue),
            "mineru_success": sum(
                1 for item in mineru_results if item.get("status") in {"success", "reused"}
            ),
            "scientific_records": len(records),
            "complete_packages": sum(
                1
                for item in records
                if (item.get("package_generation") or {}).get("status") == "complete"
            ),
            "model_review": ensemble_summary(records),
            "curation_queue_size": len(curation_queue),
        }

    build_config = config.get("build", {})
    stage = _stage_dir(workspace, "stage_18_dataset_build")
    build_records = _records_for_build(records, build_config, corpus_mode=True)
    output_dir = _resolve(base, config.get("output", "dataset"))
    write_jsonl(stage / "build_input_records.jsonl", build_records)
    manifest = build_dataset(
        build_records,
        output_dir,
        allow_failed_quality=build_config.get("allow_failed_quality", False),
        split_salt=build_config.get("split_salt", "researchchembench-v1"),
        require_reference_run=build_config.get("require_reference_run", True),
    )
    validation = validate_dataset(
        output_dir,
        require_tasks=not config.get("validation", {}).get("allow_empty", False),
    )
    write_json(stage / "build_manifest.json", manifest)
    write_json(stage / "validation_report.json", validation)
    _write_stage_summary(
        stage,
        {
            "build_input_records": len(build_records),
            "tasks_built": manifest["task_count"],
            "tasks_skipped": len(manifest["skipped"]),
            "validation": _validation_summary(validation),
        },
    )
    return {
        "source_mode": "corpus",
        "config": str(config_path),
        "corpus_root": str(corpus_root),
        "workspace": str(workspace),
        "output": str(output_dir),
        "pdf_files": len(inventory),
        "canonical_pdfs": sum(1 for item in inventory if not item.get("duplicate_of")),
        "software_direct_covered": software_summary["direct_covered"],
        "computation_stage_passed": sum(
            1
            for item in completeness_records
            if (item.get("computation_completeness") or {}).get("passed")
        ),
        "resource_stage_passed": len(classified),
        "mineru_queue": len(queue),
        "mineru_success": sum(
            1 for item in mineru_results if item.get("status") in {"success", "reused"}
        ),
        "mineru_failed": sum(
            1
            for item in mineru_results
            if item.get("status") in {"failed", "timeout", "unavailable"}
        ),
        "mineru_quality_pass": sum(
            1 for item in mineru_results if (item.get("deep_parse_quality") or {}).get("passed")
        ),
        "scientific_records": len(records),
        "curation_queue": len(curation_queue),
        "quality_pass_tasks": sum(
            len((record.get("quality_funnel") or {}).get("accepted_task_types", []))
            for record in records
        ),
        "quality_review_tasks": sum(
            len((record.get("quality_funnel") or {}).get("review_task_types", []))
            for record in records
        ),
        "quality_rejected_tasks": sum(
            len((record.get("quality_funnel") or {}).get("rejected_task_types", []))
            for record in records
        ),
        "toolbox_catalog_hash": (toolbox_profile or {}).get("catalog_hash"),
        "tasks_built": manifest["task_count"],
        "tasks_skipped": len(manifest["skipped"]),
        "stage_03_software_coverage": software_summary,
        "stage_04_computation_completeness": completeness_summary,
        "stage_05_resource_limits": resource_summary,
        "validation": _validation_summary(validation),
    }


def _curation_queue_item(record: dict[str, Any]) -> dict[str, Any]:
    funnel = record.get("quality_funnel") or {}
    reports = funnel.get("mode_reports") or {}
    selected = record.get("selected_task_type")
    candidate_modes = (
        [selected] if selected in reports and reports[selected].get("decision") != "reject" else []
    )
    unresolved = {
        mode: [
            {
                "gate_id": gate.get("gate_id"),
                "name": gate.get("name"),
                "decision": gate.get("decision"),
                "reasons": gate.get("reasons", []),
            }
            for gate in report.get("gates", [])
            if gate.get("decision") != "pass"
        ]
        for mode, report in reports.items()
        if mode in candidate_modes
    }
    decisions = [reports[mode].get("decision") for mode in candidate_modes]
    priority_rank = 0 if "pass" in decisions else 1
    return {
        "paper_id": record["paper_id"],
        "title": (record.get("paper") or {}).get("title"),
        "source_path": ((record.get("assets") or {}).get("paper")),
        "selected_task_type": selected if candidate_modes else None,
        "task_decision": reports.get(selected, {}).get("decision") if selected else None,
        "mode_decisions": {mode: reports[mode].get("decision") for mode in candidate_modes},
        "priority_rank": priority_rank,
        "unresolved_gates": unresolved,
        "toolbox_coverage": record.get("toolbox_coverage"),
        "asset_availability": record.get("asset_availability"),
        "model_ensemble": record.get("model_ensemble"),
        "schema_validation": record.get("schema_validation"),
        "curation_status": (record.get("curation") or {}).get("status"),
        "required_review": [
            "resolve only the non-passing gates listed in unresolved_gates",
            "confirm source evidence for every corrected field",
            "confirm that the selected task type is the single best-supported task for this study",
        ],
    }


def _attach_asset_availability(
    records: list[dict[str, Any]], config: dict[str, Any]
) -> list[dict[str, Any]]:
    output = []
    for record in records:
        updated = dict(record)
        updated["asset_availability"] = assess_asset_availability(
            updated,
            verify_urls=bool(config.get("verify_asset_urls", False)),
            url_timeout_seconds=float(config.get("url_timeout_seconds", 6.0)),
            max_urls=int(config.get("max_asset_urls", 8)),
        )
        output.append(updated)
    return output


def _asset_acquisition_queue_item(record: dict[str, Any]) -> dict[str, Any]:
    availability = record.get("asset_availability") or {}
    return {
        "paper_id": record.get("paper_id"),
        "title": (record.get("paper") or {}).get("title"),
        "availability_state": availability.get("availability_state"),
        "status_note": availability.get("status_note"),
        "availability_statements": availability.get("availability_statements", []),
        "candidate_urls": availability.get("candidate_urls", []),
        "repository_urls": availability.get("repository_urls", []),
        "reachable_urls": availability.get("reachable_urls", []),
        "external_identifiers": availability.get("external_identifiers", {}),
        "next_action": (
            "validate registered local task inputs"
            if availability.get("availability_state") in {"materialized", "acquired_unvalidated"}
            else "resolve, acquire, hash, license-check, and validate external task assets"
        ),
    }


def _load_toolbox_profile(config: dict[str, Any], base: Path) -> dict[str, Any] | None:
    toolbox = dict(config.get("toolbox", {}))
    raw = toolbox.get("profile")
    if not raw:
        return None
    if toolbox.get("selection"):
        selection = read_json(_resolve(base, toolbox["selection"]))
        selection.update(
            {key: value for key, value in toolbox.items() if key not in {"profile", "selection"}}
        )
    else:
        selection = toolbox
    return load_toolbox_profile(_resolve(base, raw), selection)


def _load_model_ensemble_config(config: dict[str, Any], base: Path) -> dict[str, Any]:
    ensemble = dict(config.get("model_ensemble", {}))
    if not ensemble.get("config"):
        return ensemble
    loaded = read_json(_resolve(base, ensemble["config"]))
    loaded.update({key: value for key, value in ensemble.items() if key != "config"})
    return loaded


def _resolve_reference_config(config: dict[str, Any], base: Path) -> dict[str, Any]:
    reference = dict(config.get("reference_runs", {}))
    if reference.get("manifest_dir"):
        reference["manifest_dir"] = str(_resolve(base, reference["manifest_dir"]))
    return reference


def _run_quality_funnel(
    records: list[dict[str, Any]],
    config: dict[str, Any],
    base: Path,
    workspace: Path,
) -> tuple[list[dict[str, Any]], dict[str, Any] | None]:
    toolbox_profile = _load_toolbox_profile(config, base)
    records = gate_scientific_records(records, toolbox_profile, config.get("quality_funnel", {}))
    write_jsonl(workspace / "07_quality_gated_records.jsonl", records)
    write_json(workspace / "07_quality_funnel_summary.json", quality_funnel_summary(records))
    records = review_with_ensemble(records, _load_model_ensemble_config(config, base))
    records = apply_ensemble_results(records)
    write_jsonl(workspace / "08_model_reviewed_records.jsonl", records)
    write_json(workspace / "08_model_ensemble_summary.json", ensemble_summary(records))
    _write_candidate_exports(records, workspace / "06_candidate_packages")
    queue = [_curation_queue_item(record) for record in records]
    queue = [item for item in queue if item["selected_task_type"]]
    queue.sort(key=lambda item: (item["priority_rank"], item["paper_id"]))
    write_jsonl(workspace / "09_curation_queue.jsonl", queue)
    return records, toolbox_profile


def _records_for_build(
    records: list[dict[str, Any]],
    build_config: dict[str, Any],
    corpus_mode: bool,
) -> list[dict[str, Any]]:
    accepted_statuses = set(build_config.get("accepted_curation_statuses", ["expert_approved"]))
    allow_machine = build_config.get("allow_machine_drafts", False)
    output = []
    for record in records:
        if (
            corpus_mode
            and not allow_machine
            and (record.get("curation") or {}).get("status") not in accepted_statuses
        ):
            continue
        accepted_types = set((record.get("quality_funnel") or {}).get("accepted_task_types", []))
        if not accepted_types and build_config.get("allow_review_quality", False):
            accepted_types.update((record.get("quality_funnel") or {}).get("review_task_types", []))
        selected = record.get("selected_task_type")
        if selected not in accepted_types:
            continue
        prepared = dict(record)
        output.append(prepared)
    return output


def _resolve(base: Path, value: str | Path) -> Path:
    path = Path(value).expanduser()
    return path.resolve() if path.is_absolute() else (base / path).resolve()


def _write_candidate_exports(records: list[dict[str, Any]], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for stale in output_dir.glob("*.json"):
        stale.unlink()
    for record in records:
        generation = record.get("package_generation") or {}
        package = record.get("benchmark_package") or generation.get("candidate")
        if not package:
            continue
        public_task = {
            key: value
            for key, value in package.items()
            if key not in {"ground_truth", "leakage_markers"}
        }
        write_json(
            output_dir / f"{record['paper_id']}.json",
            {
                "paper_id": record["paper_id"],
                "source_title": (record.get("paper") or {}).get("title"),
                "selected_task_type": record.get("selected_task_type"),
                "selection_reason": record.get("selection_reason"),
                "public_task": public_task,
                "hidden_reference": {
                    "ground_truth": package.get("ground_truth", {}),
                    "leakage_markers": package.get("leakage_markers", []),
                },
                "generation_status": generation.get("status"),
                "generation_validation": generation.get("validation"),
                "quality_funnel": record.get("quality_funnel"),
                "model_ensemble": record.get("model_ensemble"),
                "release_status": "candidate_only",
            },
        )


def _validation_summary(validation: dict[str, Any]) -> dict[str, Any]:
    """Keep CLI/run manifests compact while detailed validation stays on disk."""

    return {
        "passed": validation.get("passed", False),
        "format": validation.get("format"),
        "task_count": validation.get("task_count", 0),
        "error_count": len(validation.get("errors", [])),
        "warning_count": len(validation.get("warnings", [])),
    }


_STARTED_STAGES: set[str] = set()


def _stage_dir(workspace: Path, name: str) -> Path:
    stage = workspace / name
    stage.mkdir(parents=True, exist_ok=True)
    key = str(stage.resolve())
    if key not in _STARTED_STAGES:
        _STARTED_STAGES.add(key)
        pipeline_logger().info("STAGE START | %s | output=%s", name, stage)
    return stage


def _write_stage_summary(stage: Path, summary: dict[str, Any]) -> None:
    write_json(stage / "summary.json", summary)
    pipeline_logger().info("STAGE COMPLETE | %s | summary=%s", stage.name, summary)


def _write_corpus_stage_index(workspace: Path) -> None:
    stages = [
        (
            "stage_01_inventory",
            "PDF inventory, main/supplementary roles, hashes, and duplicate detection",
        ),
        (
            "stage_02_grobid_extract",
            "GROBID TEI extraction for metadata, structure, and full text",
        ),
        (
            "stage_03_software_coverage",
            "Softcite evidence and complete core-software toolbox coverage gate",
        ),
        (
            "stage_04_computation_completeness",
            "single-model gate for a complete independently constructable computation",
        ),
        (
            "stage_05_resource_limits",
            "explicit CPU, GPU, memory, and runtime hard-limit gate",
        ),
        ("stage_06_mineru_queue", "PDFs selected for deep parsing"),
        ("stage_07_mineru_parse", "raw MinerU execution outputs"),
        ("stage_08_deep_parse_quality", "MinerU output quality assessment"),
        ("stage_09_post_mineru_merge", "merge validated MinerU text without re-screening"),
        ("stage_10_extraction_ready", "non-filtering extraction-ready document snapshot"),
        ("stage_11_study_bundles", "paper/SI grouping and generated asset manifests"),
        ("stage_12_scientific_record_extraction", "record extraction and asset discovery"),
        ("stage_13_task_selection", "single benchmark task-type selection"),
        ("stage_14_package_generation", "candidate packages and reference-run attachment"),
        ("stage_15_quality_gates", "deterministic quality-gate decisions"),
        ("stage_16_model_ensemble", "role-separated model review"),
        ("stage_17_curation_queue", "human-curation queue"),
        ("stage_18_dataset_build", "formal dataset build and validation"),
    ]
    write_json(
        workspace / "stage_index.json",
        {
            "output_root": str(workspace),
            "pdf_handling": "PDF files are never copied into stage folders; manifests store paths.",
            "stages": [
                {"order": index, "directory": directory, "description": description}
                for index, (directory, description) in enumerate(stages, start=1)
            ],
        },
    )


def _field_summary(records: list[dict[str, Any]], field: str, count_label: str) -> dict[str, Any]:
    return {count_label: len(records), field: _value_counts(item.get(field) for item in records)}


def _value_counts(values: Any) -> dict[str, int]:
    counts: dict[str, int] = {}
    for value in values:
        key = "unknown" if value is None else str(value)
        counts[key] = counts.get(key, 0) + 1
    return counts


def _pdf_path_rows(
    records: list[dict[str, Any]], status_field: str | None = None
) -> list[dict[str, Any]]:
    output = []
    for item in records:
        source_path = item.get("source_path") or (item.get("assets") or {}).get("paper")
        if not source_path:
            continue
        row = {
            "document_id": item.get("document_id"),
            "paper_id": item.get("paper_id"),
            "title": item.get("title") or (item.get("paper") or {}).get("title"),
            "pdf_path": str(Path(source_path).expanduser().resolve()),
            "relative_path": item.get("relative_path"),
        }
        if status_field:
            row["status"] = item.get(status_field)
        output.append(row)
    return output


def _record_pdf_path_rows(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    selected = [record for record in records if record.get("selected_task_type")]
    rows = _pdf_path_rows(selected)
    selected_by_paper = {record.get("paper_id"): record for record in selected}
    for row in rows:
        record = selected_by_paper.get(row.get("paper_id"), {})
        row["selected_task_type"] = record.get("selected_task_type")
        row["selection_source"] = (record.get("task_selection") or {}).get("source")
    return rows


def _screening_stop_summary(
    config_path: Path,
    corpus_root: Path,
    workspace: Path,
    inventory: list[dict[str, Any]],
    *,
    software_summary: dict[str, Any],
    completeness_summary: dict[str, Any] | None = None,
    resource_summary: dict[str, Any] | None = None,
) -> dict[str, Any]:
    if resource_summary is not None:
        stopped_after = "resource_limits"
    elif completeness_summary is not None:
        stopped_after = "computation_completeness"
    else:
        stopped_after = "software_coverage"
    return {
        "source_mode": "corpus",
        "stopped_after": stopped_after,
        "config": str(config_path),
        "corpus_root": str(corpus_root),
        "workspace": str(workspace),
        "pdf_files": len(inventory),
        "stage_03_software_coverage": software_summary,
        "stage_04_computation_completeness": completeness_summary,
        "stage_05_resource_limits": resource_summary,
    }


def _resolve_command(base: Path, value: str) -> str:
    path = Path(value).expanduser()
    if path.is_absolute():
        return str(path)
    if path.parent != Path("."):
        return str((base / path).resolve())
    return value


def _load_assets(base: Path, value: str | Path) -> list[dict[str, Any]]:
    manifest_path = _resolve(base, value)
    asset_base = manifest_path.parent
    output: list[dict[str, Any]] = []
    path_keys = ("paper", "curation")
    path_list_keys = ("supplementary", "text", "hidden_reference_files")
    for raw in read_json(manifest_path):
        item = dict(raw)
        for key in path_keys:
            if item.get(key):
                item[key] = str(_resolve(asset_base, item[key]))
        for key in path_list_keys:
            item[key] = [str(_resolve(asset_base, path)) for path in item.get(key, [])]
        visible_data = {}
        for mode, paths in (item.get("visible_data") or {}).items():
            visible_data[mode] = [str(_resolve(asset_base, path)) for path in paths]
        item["visible_data"] = visible_data
        output.append(item)
    return output
