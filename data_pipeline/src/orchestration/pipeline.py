from __future__ import annotations

import contextlib
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

from src.core.config import normalize_config
from src.core.io import read_json, read_jsonl, write_json, write_jsonl
from src.core.logging import configure_pipeline_logging, pipeline_logger
from src.integrations.softcite import SoftciteClientPool, softcite_service
from src.integrations.stage03_llm_runtime import stage03_llm_runtime
from src.orchestration.screening_microbatch import run_screening_microbatches
from src.stages.stage00_remote_corpus import prepare_remote_corpus
from src.stages.stage01_inventory import group_inventory_by_paper, inventory_corpus
from src.stages.stage02_parsing import (
    build_paper_text_bundles,
    extract_documents_with_grobid,
    grobid_service,
)
from src.stages.stage03_computation_relevance import (
    assess_computation_relevance,
    computation_relevance_summary,
)
from src.stages.stage03_software_coverage.toolbox import load_toolbox_profile
from src.stages.stage04_supplementary_acquisition import (
    acquire_supplementary_materials,
    supplementary_acquisition_summary,
)
from src.stages.stage05_asset_collection import run_asset_collection
from src.stages.stage05_preliminary_coverage import (
    assess_preliminary_coverage,
    preliminary_coverage_summary,
)
from src.stages.stage06_builder import run_builder_stage
from src.stages.stage06_supplementary_extraction import (
    extract_supplementary_materials,
    supplementary_asset_result,
    supplementary_extraction_summary,
)
from src.stages.stage07_builder import run_builder_stage as run_stage07_builder
from src.stages.stage07_judge import run_judge_stage
from src.stages.stage08_judge import run_judge_stage as run_stage08_judge


def run_pipeline(
    config_path: str | Path,
    *,
    execution_backend: str = "local",
    sandbox_options=None,
    microbatch_overrides: dict[str, Any] | None = None,
) -> dict[str, Any]:
    path = Path(config_path).expanduser().resolve()
    raw = read_json(path)
    config = normalize_config(raw, path.parent)
    config.setdefault("microbatch", {}).update(microbatch_overrides or {})
    configure_pipeline_logging(config.get("log_file", Path(config["workspace"]) / "pipeline.log"))
    if (config.get("source") or {}).get("mode") != "corpus":
        raise ValueError("the redesigned pipeline supports corpus mode only")
    with stage03_llm_runtime(config) as runtime_config:
        if execution_backend == "sandbox":
            from src.sandbox.manager import SandboxRunOptions
            from src.sandbox.runtime import SandboxPipelineRuntime

            options = sandbox_options or SandboxRunOptions()
            with SandboxPipelineRuntime(options) as runtime:
                return run_corpus_pipeline(path, runtime.apply(runtime_config), path.parent)
        if execution_backend != "local":
            raise ValueError("execution_backend must be local or sandbox")
        return run_corpus_pipeline(path, runtime_config, path.parent)


def run_corpus_pipeline(config_path: Path, config: dict[str, Any], base: Path) -> dict[str, Any]:
    workspace = _resolve(base, config.get("workspace", "work"))
    workspace.mkdir(parents=True, exist_ok=True)
    source = config["source"]
    _write_stage_index(workspace)

    stage00_config = config.get("stage00_remote_corpus") or {}
    if stage00_config.get("enabled"):
        stage00_root = _resolve(
            base,
            stage00_config.get("output_directory") or workspace / "stage_00_remote_corpus",
        )
        stage00_result = prepare_remote_corpus(
            stage00_root,
            dataset=str(stage00_config["dataset"]),
            count=int(stage00_config["count"]),
            credentials=_resolve(base, stage00_config["credentials"]),
            outside=bool(stage00_config.get("outside", False)),
            resume=bool(stage00_config.get("resume", True)),
            copy_supplementary=bool(
                stage00_config.get("copy_existing_supplementary", True)
            ),
            selection=str(stage00_config.get("selection", "remote_order")),
            seed=int(stage00_config.get("seed", 0)),
        )
        corpus_root = Path(stage00_result["corpus_root"])
        _write_stage_summary(stage00_root, stage00_result["summary"])
        if _stop_after(config, 0):
            return _new_summary(config_path, corpus_root, workspace, 0, stage00=stage00_result["summary"])
    else:
        corpus_root = _resolve(base, source["root"])
        stage00_result = None

    stage = _stage_dir(workspace, "stage_01_inventory")
    inventory = inventory_corpus(
        corpus_root, workers=int((config.get("stage01") or {}).get("workers", 1))
    )
    supplementary_inventory = [
        item for item in inventory if item.get("document_role") == "supplementary"
    ]
    canonical_inventory = [item for item in inventory if not item.get("duplicate_of")]
    duplicate_inventory = [item for item in inventory if item.get("duplicate_of")]
    paper_inventory = group_inventory_by_paper(canonical_inventory)
    write_jsonl(stage / "corpus_inventory.jsonl", inventory)
    write_jsonl(stage / "papers.jsonl", paper_inventory)
    write_jsonl(stage / "pdf_paths.jsonl", _pdf_path_rows(inventory, "inventory_status"))
    write_jsonl(
        stage / "canonical_pdf_paths.jsonl", _pdf_path_rows(canonical_inventory, "inventory_status")
    )
    write_jsonl(
        stage / "duplicate_pdf_paths.jsonl", _pdf_path_rows(duplicate_inventory, "inventory_status")
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
            "duplicate_pdfs": len(duplicate_inventory),
            "supplementary_pdfs": len(supplementary_inventory),
            "supplementary_excluded": 0,
            "papers": len(paper_inventory),
            "downstream_documents": len(canonical_inventory),
        },
    )
    if _stop_after(config, 1):
        return _new_summary(config_path, corpus_root, workspace, 1, stage01={"papers": len(paper_inventory)})

    if (config.get("microbatch") or {}).get("enabled"):
        return _run_redesigned_microbatch(
            config_path=config_path,
            config=config,
            base=base,
            workspace=workspace,
            corpus_root=corpus_root,
            canonical_inventory=canonical_inventory,
            paper_inventory=paper_inventory,
            stage00_summary=stage00_result["summary"] if stage00_result else None,
        )

    grobid_config = config.get("grobid_extract", {})
    stage = _stage_dir(workspace, "stage_02_grobid_extract")
    extraction_kwargs = {
        "tei_dir": _resolve(base, grobid_config.get("tei_dir", str(stage / "tei"))),
        "text_dir": _resolve(base, grobid_config.get("text_dir", str(stage / "text"))),
        "max_chars": grobid_config.get("max_chars", 2_000_000),
        "reuse_existing": grobid_config.get("reuse_existing", True),
        "exclude_supplementary": False,
        "fallback_config": grobid_config.get("fallback", {}),
        "workers": int(grobid_config.get("workers", 1)),
    }
    # The service remains alive through Stage 06. In sandbox mode this avoids per-stage churn.
    with contextlib.ExitStack() as services:
        client = services.enter_context(grobid_service(grobid_config))
        extracted_records = extract_documents_with_grobid(
            canonical_inventory, client, **extraction_kwargs
        )
        request_attempts = sum(bool(item.get("grobid_request_attempted")) for item in extracted_records)
        request_failures = sum(bool(item.get("grobid_request_failed")) for item in extracted_records)
        paper_bundles = build_paper_text_bundles(extracted_records)
        write_jsonl(stage / "documents.jsonl", extracted_records)
        write_jsonl(stage / "paper_text_bundles.jsonl", paper_bundles)
        stage02_summary = {
            **_field_summary(extracted_records, "grobid_extract_status", "documents"),
            "papers": len(paper_bundles),
            "main_documents": sum(len(item.get("main_documents") or []) for item in paper_bundles),
            "supplementary_documents": sum(len(item.get("supplementary_documents") or []) for item in paper_bundles),
            "duplicates_excluded": len(duplicate_inventory),
            "supplementary_excluded": 0,
            "grobid_request_attempts": request_attempts,
            "grobid_request_failures": request_failures,
            "grobid_request_failure_ratio": (
                round(request_failures / request_attempts, 6) if request_attempts else 0.0
            ),
        }
        _write_stage_summary(stage, stage02_summary)
        if _stop_after(config, 2):
            return _new_summary(config_path, corpus_root, workspace, 2, stage02=stage02_summary)

        stage03_config = config.get("stage03_computation_relevance") or {}
        stage = _stage_dir(workspace, "stage_03_computation_relevance")
        reused = _completed_stage_records(
            config, stage, "decisions.jsonl", len(paper_bundles)
        )
        if reused is not None:
            relevance_records, stage03_summary = reused
        else:
            relevance_records = assess_computation_relevance(
                paper_bundles,
                method_ontology=_resolve(base, stage03_config["method_ontology"]),
                evidence_rules=_resolve(base, stage03_config["evidence_rules"]),
                negative_contexts=_resolve(base, stage03_config["negative_contexts"]),
                workers=int(stage03_config.get("workers", 1)),
                llm_config={
                    **(stage03_config.get("llm") or {}),
                    "enabled": bool(stage03_config.get("use_llm"))
                    and bool((stage03_config.get("llm") or {}).get("enabled")),
                },
                llm_cache_dir=(stage03_config.get("llm") or {}).get(
                    "cache_directory", stage / "llm_cache"
                ),
            )
            stage03_summary = computation_relevance_summary(relevance_records)
            write_jsonl(stage / "decisions.jsonl", relevance_records)
            write_jsonl(stage / "evidence_spans.jsonl", [evidence for item in relevance_records for evidence in (item.get("computation_relevance") or {}).get("evidence", [])])
            write_jsonl(stage / "strong_candidates.jsonl", [item for item in relevance_records if (item.get("computation_relevance") or {}).get("decision") == "strong_candidate"])
            write_jsonl(stage / "weak_candidates.jsonl", [item for item in relevance_records if (item.get("computation_relevance") or {}).get("decision") == "weak_candidate"])
            write_jsonl(stage / "rejected.jsonl", [item for item in relevance_records if (item.get("computation_relevance") or {}).get("decision") == "not_computational"])
            _write_stage_summary(stage, stage03_summary)
        if _stop_after(config, 3):
            return _new_summary(config_path, corpus_root, workspace, 3, stage03=stage03_summary)

        candidates = [
            item for item in relevance_records if (item.get("pipeline_routing") or {}).get("continue")
        ]
        stage04_config = config.get("stage04_supplementary_acquisition") or {}
        stage = _stage_dir(workspace, "stage_04_supplementary_acquisition")
        reused = _completed_stage_records(
            config, stage, "supplementary_manifest.jsonl", len(candidates)
        )
        if reused is not None:
            acquisition_records, stage04_summary = reused
        else:
            store = _stage04_store(config, base, candidates)
            acquisition_records = acquire_supplementary_materials(
                candidates, stage, stage04_config, store=store
            )
            stage04_summary = supplementary_acquisition_summary(acquisition_records)
            write_jsonl(stage / "supplementary_manifest.jsonl", acquisition_records)
            write_jsonl(stage / "discovery_attempts.jsonl", _stage04_attempts(acquisition_records))
            _write_stage_summary(stage, stage04_summary)
        if _stop_after(config, 4):
            return _new_summary(config_path, corpus_root, workspace, 4, stage03=stage03_summary, stage04=stage04_summary)

        toolbox_profile = _load_toolbox(config, base)
        software_config = config.get("software_coverage", {})
        stage05_config = config.get("stage05_preliminary_coverage") or {}
        stage = _stage_dir(workspace, "stage_05_preliminary_coverage")
        softcite_configs = _softcite_service_configs(
            software_config, int(stage05_config.get("softcite_instances", 1))
        )
        softcite_clients = [
            services.enter_context(softcite_service(item)) for item in softcite_configs
        ]
        softcite_client = (
            softcite_clients[0]
            if len(softcite_clients) == 1
            else SoftciteClientPool(softcite_clients)
        )
        coverage_records = assess_preliminary_coverage(
            acquisition_records,
            extracted_records,
            softcite_client,
            toolbox_profile,
            capability_catalog=_resolve(base, stage05_config["capability_catalog"]),
            aliases_file=_resolve(base, software_config["aliases_file"]),
            role_rules_file=_resolve(base, software_config["role_rules_file"]),
            capability_map_file=_resolve(base, software_config["capability_map_file"]),
            raw_output_dir=stage / "softcite_raw",
            workers=int(software_config.get("workers", 1)),
        )
        stage05_summary = preliminary_coverage_summary(coverage_records)
        write_jsonl(stage / "decisions.jsonl", coverage_records)
        _write_stage_summary(stage, stage05_summary)
        if _stop_after(config, 5):
            return _new_summary(config_path, corpus_root, workspace, 5, stage03=stage03_summary, stage04=stage04_summary, stage05=stage05_summary)

        stage06_config = config.get("stage06_supplementary_extraction") or {}
        stage = _stage_dir(workspace, "stage_06_supplementary_extraction")
        stage06_records = extract_supplementary_materials(
            [item for item in coverage_records if (item.get("pipeline_routing") or {}).get("continue")],
            stage,
            {**stage06_config, "mineru": config.get("mineru", {})},
            grobid_client=client,
        )
        stage06_summary = supplementary_extraction_summary(stage06_records)
        write_jsonl(stage / "documents.jsonl", [document for item in stage06_records for document in (item.get("supplementary_extraction") or {}).get("documents", [])])
        write_jsonl(stage / "supplementary_evidence_bundles.jsonl", stage06_records)
        write_jsonl(stage / "extraction_errors.jsonl", [error for item in stage06_records for error in (item.get("supplementary_extraction") or {}).get("errors", [])])
        _write_stage_summary(stage, stage06_summary)
        if _stop_after(config, 6):
            summary = _new_summary(config_path, corpus_root, workspace, 6, stage03=stage03_summary, stage04=stage04_summary, stage05=stage05_summary, stage06=stage06_summary)
            write_json(workspace / "run_summary.json", summary)
            return summary

        asset_result = supplementary_asset_result(stage06_records)
        stage = _stage_dir(workspace, "stage_07_builder")
        builder_result = run_stage07_builder(
            stage06_records,
            asset_result,
            stage,
            config.get("stage07_builder", {}),
            toolbox_profile,
        )
        _write_stage_summary(stage, builder_result["summary"])
        if _stop_after(config, 7):
            return _new_summary(config_path, corpus_root, workspace, 7, stage06=stage06_summary, stage07=builder_result["summary"])

        stage = _stage_dir(workspace, "stage_08_judge")
        judge_result = run_stage08_judge(
            stage06_records,
            asset_result,
            builder_result,
            stage,
            config.get("stage08_judge", {}),
            toolbox_profile,
        )
        _write_stage_summary(stage, judge_result["summary"])
        summary = _new_summary(config_path, corpus_root, workspace, 8, stage06=stage06_summary, stage07=builder_result["summary"], stage08=judge_result["summary"])
        write_json(workspace / "run_summary.json", summary)
        return summary


def run_late_stages(
    input_path: str | Path,
    config_path: str | Path,
    workspace_override: str | Path | None = None,
) -> dict[str, Any]:
    config_file = Path(config_path).expanduser().resolve()
    config = normalize_config(read_json(config_file), config_file.parent)
    workspace = (
        Path(workspace_override).expanduser().resolve()
        if workspace_override
        else _resolve(config_file.parent, config["workspace"])
    )
    workspace.mkdir(parents=True, exist_ok=True)
    configure_pipeline_logging(workspace / "pipeline.log")
    _write_stage_index(workspace)
    records = [
        item for item in read_jsonl(input_path) if (item.get("resource_limits") or {}).get("passed")
    ]
    return run_late_stages_records(
        records,
        config=config,
        base=config_file.parent,
        workspace=workspace,
        run_metadata={
            "source_mode": "stage04_reuse",
            "config": str(config_file),
            "input": str(Path(input_path).resolve()),
        },
    )


def run_late_stages_records(
    records: list[dict[str, Any]],
    *,
    config: dict[str, Any],
    base: Path,
    workspace: Path,
    run_metadata: dict[str, Any],
) -> dict[str, Any]:
    toolbox = _load_toolbox(config, base)
    stage05 = _stage_dir(workspace, "stage_05_asset_collection")
    stage05_config = config.get("stage05", {})
    if stage05_config.get("enabled", True):
        asset_result = run_asset_collection(
            records, stage05, stage05_config, config.get("mineru", {})
        )
    else:
        asset_result = run_asset_collection(
            records,
            stage05,
            {
                **stage05_config,
                "enable_network": False,
                "max_rounds": 0,
                "max_clues_per_paper": 0,
                "include_local_siblings": False,
                "query_metadata": False,
            },
            {**config.get("mineru", {}), "execute": False},
        )
        asset_result["summary"].update(
            {"skipped": True, "skip_adapter": "primary_pdf_with_stage02_text"}
        )
    _write_stage_summary(stage05, asset_result["summary"])
    if config.get("stop_after") == "asset_collection":
        return {
            **run_metadata,
            "workspace": str(workspace),
            "stopped_after": "asset_collection",
            "stage_05": asset_result["summary"],
        }

    stage06 = _stage_dir(workspace, "stage_06_builder")
    builder_result = run_builder_stage(
        records, asset_result, stage06, config.get("stage06", {}), toolbox
    )
    _write_stage_summary(stage06, builder_result["summary"])
    if any(item.get("status") == "error" for item in builder_result["records"]):
        raise RuntimeError("Stage 06 agent execution failed; inspect stage_06_builder agent logs")
    if config.get("stop_after") == "builder":
        return {
            **run_metadata,
            "workspace": str(workspace),
            "stopped_after": "builder",
            "stage_05": asset_result["summary"],
            "stage_06": builder_result["summary"],
        }

    stage07 = _stage_dir(workspace, "stage_07_judge")
    judge_result = run_judge_stage(
        records, asset_result, builder_result, stage07, config.get("stage07", {}), toolbox
    )
    _write_stage_summary(stage07, judge_result["summary"])
    if any(item.get("status") == "error" for item in judge_result["records"]):
        raise RuntimeError("Stage 07 agent execution failed; inspect stage_07_judge agent logs")
    summary = {
        **run_metadata,
        "workspace": str(workspace),
        "stopped_after": "judge",
        "stage_05": asset_result["summary"],
        "stage_06": builder_result["summary"],
        "stage_07": judge_result["summary"],
    }
    write_json(workspace / "run_summary.json", summary)
    return summary


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


def _completed_stage_records(
    config: dict[str, Any], stage: Path, records_name: str, expected: int
) -> tuple[list[dict[str, Any]], dict[str, Any]] | None:
    if not config.get("resume_completed_stages", False):
        return None
    records_path = stage / records_name
    summary_path = stage / "summary.json"
    if not records_path.is_file() or not summary_path.is_file():
        return None
    records = read_jsonl(records_path)
    if len(records) != expected:
        return None
    summary = read_json(summary_path)
    pipeline_logger().info(
        "STAGE REUSED | %s | records=%d", stage.name, len(records)
    )
    return records, summary


def _softcite_service_configs(
    config: dict[str, Any], requested_instances: int
) -> list[dict[str, Any]]:
    runtime = config.get("_sandbox_runtime")
    instances = max(1, int(requested_instances)) if runtime is not None else 1
    configs = [
        runtime.service_config("softcite", config, instance=index)
        for index in range(instances)
    ] if runtime is not None else [config]
    if runtime is not None and len(configs) > 1:
        with ThreadPoolExecutor(
            max_workers=len(configs), thread_name_prefix="softcite-service-start"
        ) as executor:
            futures = [
                executor.submit(runtime.start_service, "softcite", item, instance=index)
                for index, item in enumerate(configs)
            ]
            for future in futures:
                future.result()
    return configs


def _write_stage_index(workspace: Path) -> None:
    stages = [
        ("stage_00_remote_corpus", "remote selection and grouped main-paper/SI corpus"),
        ("stage_01_inventory", "paper grouping, PDF roles, hashes, and duplicate detection"),
        ("stage_02_grobid_extract", "main-paper and existing-SI text extraction"),
        (
            "stage_03_computation_relevance",
            "deterministic computation relevance evidence without LLM calls",
        ),
        (
            "stage_04_supplementary_acquisition",
            "missing official supplementary-information acquisition only",
        ),
        (
            "stage_05_preliminary_coverage",
            "software extraction and preliminary frozen-toolbox coverage",
        ),
        (
            "stage_06_supplementary_extraction",
            "newly acquired SI extraction and computational evidence bundle",
        ),
        ("stage_07_builder", "isolated Builder Agent availability decision and construction"),
        ("stage_08_judge", "isolated Judge Agent audit and final pipeline decision"),
    ]
    write_json(
        workspace / "stage_index.json",
        {
            "output_root": str(workspace),
            "stages": [
                {"order": index, "directory": directory, "description": description}
                for index, (directory, description) in enumerate(stages)
            ],
        },
    )


STOP_AFTER_STAGE = {
    "stage00": 0,
    "remote_corpus": 0,
    "stage01": 1,
    "inventory": 1,
    "stage02": 2,
    "grobid_extract": 2,
    "parsing": 2,
    "stage03": 3,
    "computation_relevance": 3,
    "stage04": 4,
    "supplementary_acquisition": 4,
    "stage05": 5,
    "preliminary_coverage": 5,
    "stage06": 6,
    "supplementary_extraction": 6,
    "stage07": 7,
    "builder": 7,
    "stage08": 8,
    "judge": 8,
}


def _stop_after(config: dict[str, Any], stage: int) -> bool:
    value = str(config.get("stop_after", "stage08")).casefold()
    if value not in STOP_AFTER_STAGE:
        raise ValueError(f"unsupported stop_after value: {value}")
    return STOP_AFTER_STAGE[value] == stage


def _new_summary(
    config_path: Path,
    corpus_root: Path,
    workspace: Path,
    stopped_after_stage: int,
    **stage_summaries: Any,
) -> dict[str, Any]:
    return {
        "pipeline_schema_version": 2,
        "source_mode": "corpus",
        "config": str(config_path),
        "corpus_root": str(corpus_root),
        "workspace": str(workspace),
        "stopped_after": f"stage{stopped_after_stage:02d}",
        **{key: value for key, value in stage_summaries.items() if value is not None},
    }


def _run_redesigned_microbatch(
    *,
    config_path: Path,
    config: dict[str, Any],
    base: Path,
    workspace: Path,
    corpus_root: Path,
    canonical_inventory: list[dict[str, Any]],
    paper_inventory: list[dict[str, Any]],
    stage00_summary: dict[str, Any] | None,
) -> dict[str, Any]:
    stop_value = str(config.get("stop_after", "stage06")).casefold()
    if stop_value not in STOP_AFTER_STAGE:
        raise ValueError(f"unsupported stop_after value: {stop_value}")
    end_stage = STOP_AFTER_STAGE[stop_value]
    if end_stage > 6:
        raise ValueError(
            "redesigned microbatch mode currently supports stop_after through stage06"
        )
    grobid_config = config.get("grobid_extract") or {}
    with contextlib.ExitStack() as services:
        grobid_client = services.enter_context(grobid_service(grobid_config))
        softcite_client = None
        toolbox_profile = None
        if end_stage >= 5:
            toolbox_profile = _load_toolbox(config, base)
            software_config = config.get("software_coverage") or {}
            requested_instances = int(
                (config.get("stage05_preliminary_coverage") or {}).get(
                    "softcite_instances", 1
                )
            )
            softcite_configs = _softcite_service_configs(
                software_config, requested_instances
            )
            softcite_clients = [
                services.enter_context(softcite_service(item)) for item in softcite_configs
            ]
            softcite_client = (
                softcite_clients[0]
                if len(softcite_clients) == 1
                else SoftciteClientPool(softcite_clients)
            )
        result = run_screening_microbatches(
            config=config,
            base=base,
            workspace=workspace,
            canonical_inventory=canonical_inventory,
            end_stage=end_stage,
            grobid_client=grobid_client,
            softcite_client=softcite_client,
            toolbox_profile=toolbox_profile,
            store_factory=lambda candidates: _stage04_store(config, base, candidates),
        )
    summary = _new_summary(
        config_path,
        corpus_root,
        workspace,
        end_stage,
        stage00=stage00_summary,
        stage01={"papers": len(paper_inventory)},
        stage02=result.get("stage02"),
        stage03=result.get("stage03"),
        stage04=result.get("stage04"),
        stage05=result.get("stage05"),
        stage06=result.get("stage06"),
    )
    summary["execution_mode"] = "microbatch"
    summary["microbatch"] = result["microbatch"]
    write_json(workspace / "run_summary.json", summary)
    return summary


def _stage04_store(
    config: dict[str, Any], base: Path, candidates: list[dict[str, Any]]
):
    needs_store = any(
        not item.get("has_local_supplementary")
        and (item.get("source_record") or {}).get("support_path")
        for item in candidates
    )
    credentials = (config.get("stage00_remote_corpus") or {}).get("credentials")
    if not needs_store or not credentials:
        return None
    from src.integrations.xinghe import XingheObjectStore

    return XingheObjectStore(
        _resolve(base, credentials),
        outside=bool((config.get("stage00_remote_corpus") or {}).get("outside", False)),
    )


def _stage04_attempts(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for record in records:
        for attempt in (record.get("supplementary_acquisition") or {}).get("attempts", []):
            output.append({"paper_id": record.get("paper_id"), **attempt})
    return output


def _load_toolbox(config: dict[str, Any], base: Path) -> dict[str, Any]:
    toolbox = dict(config.get("toolbox", {}))
    return load_toolbox_profile(_resolve(base, toolbox["profile"]), toolbox)


def _resolve(base: Path, value: str | Path) -> Path:
    path = Path(value).expanduser()
    return path.resolve() if path.is_absolute() else (base / path).resolve()


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
        source_path = item.get("source_path")
        if not source_path:
            continue
        row = {
            "document_id": item.get("document_id"),
            "paper_id": item.get("paper_id"),
            "title": item.get("title"),
            "pdf_path": str(Path(source_path).expanduser().resolve()),
            "relative_path": item.get("relative_path"),
        }
        if status_field:
            row["status"] = item.get(status_field)
        output.append(row)
    return output


def _summary(
    config_path: Path,
    corpus_root: Path,
    workspace: Path,
    inventory: list[dict[str, Any]],
    *,
    stopped_after: str,
    stage03: dict[str, Any] | None = None,
    stage04: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "source_mode": "corpus",
        "stopped_after": stopped_after,
        "config": str(config_path),
        "corpus_root": str(corpus_root),
        "workspace": str(workspace),
        "pdf_files": len(inventory),
        "stage_03_software_coverage": stage03,
        "stage_04_resource_limits": stage04,
    }
