from __future__ import annotations

import contextlib
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.contracts import (
    canonical_hash,
    decision_counts,
    read_json,
    read_jsonl,
    write_json,
    write_jsonl,
)
from src.core.concurrency import ordered_pipeline_map
from src.core.io import sha256_file
from src.core.resume import (
    document_input_fingerprint,
    ResumeStateStore,
    input_fingerprint,
    paper_input_fingerprint,
    result_artifacts,
    scientific_stage_fingerprints,
    stable_input_value,
)
from src.integrations.grobid import GrobidClient
from src.integrations.managed_service import managed_service
from src.integrations.softcite import SoftciteClient, SoftciteClientPool, softcite_service
from src.model_client import ModelCaller, RoleModelClient, is_transient_connection_error
from src.prompts import (
    STAGE02_CLASSIFY_VERSION,
    STAGE02_PASS_VERIFY_VERSION,
    STAGE03_VERSION,
    STAGE05_ROUTER_VERSION,
    STAGE05_VERSION,
)
from src.registry import ScreeningRegistry
from src.runtime import (
    ManagedScreeningServiceError,
    ensure_managed_screening_worker,
    screening_model_runtime,
    start_managed_mineru_service,
    stop_managed_screening_worker,
)
from src.stages.stage00_remote_corpus.stage import run_stage00
from src.stages.stage01_document_preparation.normalization import (
    DOCUMENT_NORMALIZATION_IMPLEMENTATION_VERSION,
    run_document_normalization,
)
from src.stages.stage01_document_preparation.stage import run_paper_package
from src.stages.stage02_computational_content.stage import (
    COMPUTATIONAL_CONTENT_IMPLEMENTATION_VERSION,
    run_stage02,
)
from src.stages.stage03_toolbox_resource_gate.stage import run_stage03
from src.stages.stage04_mineru_normalization.stage import run_stage04
from src.stages.stage05_benchmark_suitability.stage import run_stage05
from src.stages.stage06_task_builder.stage import run_stage06
from src.stages.stage07_task_judge.stage import run_stage07

STAGE_DIRS = {
    "stage01": "stage_01_document_preparation",
    "stage02": "stage_02_computational_content",
    "stage03": "stage_03_toolbox_resource_gate",
    "stage04": "stage_04_mineru_deep_normalization",
    "stage05": "stage_05_benchmark_suitability",
}


def run_pipeline(
    config_path: str | Path,
    *,
    model_callers: dict[str, ModelCaller] | None = None,
    execution_backend: str | None = None,
    stop_after: str | None = None,
    sandbox_options=None,
    microbatch_overrides: dict[str, Any] | None = None,
    resume_options: dict[str, Any] | None = None,
    sandbox_runtime=None,
) -> dict[str, Any]:
    config = load_config(config_path)
    if stop_after is not None:
        if stop_after not in {f"stage{index:02d}" for index in range(8)}:
            raise ValueError("stop_after must be stage00 through stage07")
        config["stop_after"] = stop_after
    config["microbatch"].update(microbatch_overrides or {})
    backend = execution_backend or (config.get("execution") or {}).get("backend", "local")
    if backend == "sandbox":
        if sandbox_runtime is not None:
            _apply_sandbox(config, sandbox_runtime)
            return _run_loaded_pipeline(
                config,
                model_callers=model_callers,
                resume_options=resume_options,
            )
        from src.sandbox.runtime import SandboxPipelineRuntime

        options = sandbox_options or _sandbox_options_from_config(config)
        screening = config["models"]["screening"]
        prewarm = _uses_managed_screening_model(config) and bool(
            screening.get("managed_rlaunch")
        )
        with ThreadPoolExecutor(max_workers=1) as executor:
            future = (
                executor.submit(ensure_managed_screening_worker, screening) if prewarm else None
            )
            try:
                with SandboxPipelineRuntime(options) as runtime:
                    if future is not None:
                        future.result()
                    _apply_sandbox(config, runtime)
                    return _run_loaded_pipeline(
                        config,
                        model_callers=model_callers,
                        resume_options=resume_options,
                    )
            finally:
                if future is not None:
                    try:
                        future.result()
                    finally:
                        if not _preserve_screening_worker(screening):
                            stop_managed_screening_worker(screening)
    if backend != "local":
        raise ValueError("execution backend must be local or sandbox")
    try:
        return _run_loaded_pipeline(
            config,
            model_callers=model_callers,
            resume_options=resume_options,
        )
    finally:
        if (
            _uses_managed_screening_model(config)
            and config["models"]["screening"].get("managed_rlaunch")
            and not _preserve_screening_worker(config["models"]["screening"])
        ):
            stop_managed_screening_worker(config["models"]["screening"])


def load_config(config_path: str | Path) -> dict[str, Any]:
    from src.config import load_config as load_pipeline_config

    return load_pipeline_config(config_path)


def _preserve_screening_worker(config: dict[str, Any]) -> bool:
    """Keep a managed worker only when an outer batch controller owns cleanup."""

    return bool(config.get("preserve_worker_on_exit", False))


def _uses_managed_screening_model(config: dict[str, Any]) -> bool:
    """Return whether a requested stage still uses the legacy shared model role."""

    stop_index = int(config["stop_after"].replace("stage", ""))
    return (stop_index >= 2 and config["stage02"].get("model_role", "screening") == "screening") or (
        stop_index >= 3
        and config["stage03"].get("model_role", "screening") == "screening"
    )


def _run_loaded_pipeline(
    config: dict[str, Any], *, model_callers=None, resume_options=None
) -> dict[str, Any]:
    workspace = Path(config["workspace"])
    workspace.mkdir(parents=True, exist_ok=True)
    run_id = str(config.get("run_id") or _run_id(config))
    stop_index = int(config["stop_after"].replace("stage", ""))
    resume = _resume_runtime(config, resume_options)
    snapshot = _config_snapshot(config, run_id)
    snapshot_path = workspace / "config.snapshot.json"
    if resume is None:
        write_json(snapshot_path, snapshot)
    else:
        if not snapshot_path.is_file():
            write_json(snapshot_path, snapshot)
        write_json(
            workspace
            / "resume_attempts"
            / f"generation-{resume['generation']:04d}"
            / "config.snapshot.json",
            snapshot,
        )
    registry = ScreeningRegistry.from_config(
        config.get("registry")
        or {
            "enabled": False,
            "prune_rejected_stage00_assets": False,
            "database": workspace / "registry.disabled.sqlite",
        }
    )
    registry.start_run(
        run_id=run_id,
        workspace=workspace,
        config_path=config.get("config_path", "<in-memory-config>"),
        config_hash=canonical_hash(snapshot),
    )

    stage00_config = {
        **config["stage00"],
        "source_root": (config.get("source") or {}).get("root"),
    }
    if resume is not None:
        stage00_config.update(
            {
                "_resume_store": resume["store"],
                "_resume_outer_batch_id": resume["outer_batch_id"],
                "_resume_target_slot_start": resume["target_slot_start"],
                "_resume_retry_only": resume["retry_only"],
            }
        )
    if resume is not None and not _resume_stage_active(resume, "stage00"):
        stage00_summary = workspace / "stage_00_remote_corpus" / "stage_summary.json"
        if not stage00_summary.is_file():
            raise RuntimeError(
                "Stage00 is outside the requested resume range, but its stage_summary.json "
                f"is missing from {workspace}"
            )
        stage00 = read_json(stage00_summary)
    else:
        stage00 = run_stage00(stage00_config, workspace, run_id)
    registry.register_stage00_manifest(
        run_id=run_id,
        manifest_path=workspace / "stage_00_remote_corpus" / "source_manifest.jsonl",
        corpus_root=stage00["corpus_root"],
    )
    result: dict[str, Any] = {"run_id": run_id, "workspace": str(workspace), "stage00": stage00}
    if (
        resume is not None
        and config["stage00"].get("enabled", False)
        and _resume_stage_active(resume, "stage00")
    ):
        _checkpoint_stage00(resume, config, workspace)
    if stop_index == 0:
        return _finish(result, config, workspace, registry)
    package = (
        _load_or_run_package(
            config,
            stage00["corpus_root"],
            workspace,
            run_id,
            resume=resume,
        )
        if resume is not None
        else _load_or_run_package(
            config,
            stage00["corpus_root"],
            workspace,
            run_id,
        )
    )
    registry.register_document_sources(run_id=run_id, documents=package["documents"])
    _record_registry_stage(
        registry,
        resume,
        run_id=run_id,
        stage="stage01",
        rows=package["papers"],
    )
    if stop_index == 1 and not package["papers"]:
        return _finish(result, config, workspace, registry)
    batches = _paper_batches(package["papers"], int(config["microbatch"].get("size", 10)))
    overall = (
        int(config["microbatch"].get("concurrency", 1))
        if config["microbatch"].get("enabled", True)
        else 1
    )
    configured = config["microbatch"].get("stage_concurrency") or {}
    # Legacy configs keep one deployed model resident. Dedicated API roles bypass
    # the worker lifecycle entirely.
    resume_start_index = resume["start_index"] if resume is not None else 0
    phase1_model_active = stop_index >= 2 and resume_start_index <= 3
    uses_managed_screening = _uses_managed_screening_model(config) and phase1_model_active
    phase1_context = (
        screening_model_runtime(
            config["models"]["screening"],
            preserve_worker=bool(
                config.get("stage04", {}).get("mineru", {}).get("managed_gpu", False)
            ),
        )
        if uses_managed_screening
        else contextlib.nullcontext(config["models"]["screening"])
    )
    with contextlib.ExitStack() as services:
        screening_config = services.enter_context(phase1_context)
        grobid_client = (
            _grobid_service(config["stage01"]["normalization"], services)
            if resume_start_index <= 1
            else None
        )
        softcite_client = (
            _softcite_service(config["stage03"], services)
            if stop_index >= 3 and resume_start_index <= 3
            else None
        )
        clients = _clients(
            config,
            workspace,
            model_callers or {},
            screening_config,
            stop_index,
            include_screening=phase1_model_active,
        )

        def process_stage01(item):
            index, paper_batch = item
            return _run_phase1_stage01(
                index=index,
                papers=paper_batch,
                all_documents=package["documents"],
                config=config,
                workspace=workspace,
                run_id=run_id,
                grobid_client=grobid_client,
                registry=registry,
                resume=resume,
            )

        def process_stage02(state):
            return _run_phase1_stage02(
                state=state,
                config=config,
                clients=clients,
                workspace=workspace,
                run_id=run_id,
                registry=registry,
                resume=resume,
            )

        def process_stage03(state):
            return _run_phase1_stage03(
                state=state,
                config=config,
                clients=clients,
                workspace=workspace,
                run_id=run_id,
                softcite_client=softcite_client,
                registry=registry,
                resume=resume,
            )

        stage_functions = [process_stage01]
        stage_names = ["stage01"]
        if stop_index >= 2:
            stage_functions.append(process_stage02)
            stage_names.append("stage02")
        if stop_index >= 3:
            stage_functions.append(process_stage03)
            stage_names.append("stage03")
        phase1 = ordered_pipeline_map(
            stage_functions,
            list(enumerate(batches)),
            max_workers=[int(configured.get(stage, overall)) for stage in stage_names],
            buffer_size=int(config["microbatch"].get("buffer_size", overall)),
        )
    aggregated = _aggregate_phase1(phase1, package, workspace, run_id, stop_index)
    result.update({key: value["summary"] for key, value in aggregated.items()})
    if stop_index <= 3:
        return _finish(result, config, workspace, registry)

    # Phase 2 is independent of Qwen. The same worker is switched to MinerU when configured.
    mineru_config = config["stage04"].get("mineru") or {}
    if mineru_config.get("managed_gpu") and resume_start_index <= 4:
        mineru_config = start_managed_mineru_service(config["models"]["screening"], mineru_config)
        config["stage04"]["mineru"] = mineru_config
    with contextlib.ExitStack() as services:
        softcite_client = None
        clients = _clients(
            config,
            workspace,
            model_callers or {},
            config["models"]["screening"],
            stop_index,
            include_screening=False,
        )

        def process_stage04(item):
            index, paper_batch, source = item
            return _run_phase2_stage04(
                index=index,
                papers=paper_batch,
                phase1=source,
                config=config,
                workspace=workspace,
                run_id=run_id,
                registry=registry,
                resume=resume,
            )

        def process_stage05(state):
            return _run_phase2_stage05(
                state=state,
                config=config,
                clients=clients,
                workspace=workspace,
                run_id=run_id,
                registry=registry,
                resume=resume,
            )

        phase2_functions = [process_stage04]
        phase2_names = ["stage04"]
        if stop_index >= 5:
            phase2_functions.append(process_stage05)
            phase2_names.append("stage05")
        phase2 = ordered_pipeline_map(
            phase2_functions,
            [(index, paper_batch, phase1[index]) for index, paper_batch in enumerate(batches)],
            max_workers=[int(configured.get(stage, overall)) for stage in phase2_names],
            buffer_size=int(config["microbatch"].get("buffer_size", overall)),
        )
    aggregated.update(_aggregate_phase2(phase2, workspace, run_id, stop_index))
    result.update({key: value["summary"] for key, value in aggregated.items() if key not in result})
    if stop_index <= 5:
        return _finish(result, config, workspace, registry)

    late_clients = _clients(
        config, workspace, model_callers or {}, config["models"]["screening"], stop_index
    )
    builder = run_stage06(
        candidates=aggregated["stage05"]["candidates"],
        stage02_records=aggregated["stage02"]["records"],
        stage03_records=aggregated["stage03"]["records"],
        stage04_records=aggregated["stage04"]["records"],
        documents=aggregated["stage04"]["documents"],
        config={
            **config["stage06"],
            "toolbox_capabilities": config["stage03"]["toolbox_capabilities"],
        },
        model=late_clients["builder"],
        workspace=workspace,
        run_id=run_id,
    )
    result["stage06"] = builder["summary"]
    registry.record_stage_results(
        run_id=run_id,
        stage="stage06",
        rows=builder["records"],
        prune=False,
    )
    if stop_index == 6:
        return _finish(result, config, workspace, registry)
    judge = run_stage07(
        build_records=builder["records"],
        documents=aggregated["stage04"]["documents"],
        config={
            **config["stage07"],
            "toolbox_capabilities": config["stage03"]["toolbox_capabilities"],
        },
        model=late_clients["judge"],
        workspace=workspace,
        run_id=run_id,
    )
    result["stage07"] = judge["summary"]
    registry.record_stage_results(
        run_id=run_id,
        stage="stage07",
        rows=judge["records"],
        prune=False,
    )
    return _finish(result, config, workspace, registry)


def _run_phase1_stage01(
    *,
    index,
    papers,
    all_documents,
    config,
    workspace,
    run_id,
    grobid_client,
    registry=None,
    resume=None,
):
    started_epoch = time.time()
    started = time.perf_counter()
    root = workspace / "microbatches" / f"batch-{index + 1:06d}"
    documents = [
        row for row in all_documents if row.get("paper_id") in {p["paper_id"] for p in papers}
    ]
    hashes = _microbatch_stage_hashes(papers, documents, config)
    output = {"batch_id": f"batch-{index + 1:06d}"}
    stage01 = (
        None
        if resume is not None
        else _load_cached_microbatch_stage(root, "stage01", hashes["stage01"])
    )
    cache_hit = stage01 is not None
    if stage01 is None and resume is not None:
        reused_documents = []
        pending_document_ids = set()
        reused_papers = []
        pending_paper_ids = set()
        unresolved_papers = []
        for paper in papers:
            paper_documents = [
                row for row in documents if row.get("paper_id") == paper["paper_id"]
            ]
            plan = _resume_plan(
                resume,
                "stage01",
                paper["paper_id"],
                None,
                _resume_paper_input(paper, paper_documents),
            )
            if plan.action == "reuse" and plan.result:
                reused_papers.append(plan.result)
            elif plan.action == "run":
                pending_paper_ids.add(str(paper["paper_id"]))
            elif plan.result:
                reused_papers.append(plan.result)
            else:
                unresolved_papers.append(
                    {
                        **paper,
                        "processing_status": "pending",
                        "decision": "processing_pending",
                        "passed": False,
                    }
                )
        for document in documents:
            plan = _resume_plan(
                resume,
                "stage01",
                document["paper_id"],
                document["document_id"],
                _resume_document_input(document),
            )
            if plan.action == "reuse" and plan.result:
                reused_documents.append(plan.result)
            elif plan.action == "run":
                pending_document_ids.add(str(document["document_id"]))
            elif plan.result:
                reused_documents.append(plan.result)
        fresh_paper_ids = pending_paper_ids | {
            str(document["paper_id"])
            for document in documents
            if str(document.get("document_id")) in pending_document_ids
        }
        fresh = {"papers": [], "documents": [], "attempts": []}
        if _resume_stage_active(resume, "stage01") and fresh_paper_ids:
            attempt_root = _resume_attempt_root(root, resume, "stage01")
            fresh = run_document_normalization(
                papers=[row for row in papers if str(row["paper_id"]) in fresh_paper_ids],
                documents=[
                    row for row in documents if str(row["paper_id"]) in fresh_paper_ids
                ],
                config=config["stage01"]["normalization"],
                workspace=attempt_root,
                run_id=run_id,
                grobid_client=grobid_client,
                document_ids=pending_document_ids,
                existing_documents=[
                    row
                    for row in reused_documents
                    if str(row["paper_id"]) in fresh_paper_ids
                ],
            )
            for row in fresh.get("documents") or []:
                if str(row.get("document_id")) in pending_document_ids:
                    _resume_record(resume, "stage01", row, _resume_document_input(row))
            for row in fresh.get("papers") or []:
                source_paper = next(
                    item for item in papers if item["paper_id"] == row["paper_id"]
                )
                _resume_record(
                    resume,
                    "stage01",
                    row,
                    _resume_paper_input(
                        source_paper,
                        [
                            document
                            for document in documents
                            if document.get("paper_id") == source_paper["paper_id"]
                        ],
                    ),
                )
        fresh_document_ids = {
            str(row["document_id"]) for row in fresh.get("documents") or []
        }
        final_documents = _deduplicate_document_rows(
            [
                *[
                    row
                    for row in reused_documents
                    if str(row["document_id"]) not in fresh_document_ids
                ],
                *(fresh.get("documents") or []),
            ]
        )
        final_papers = _ordered_records(
            {row["paper_id"]: row for row in papers},
            [
                *[
                    row
                    for row in reused_papers
                    if str(row["paper_id"]) not in fresh_paper_ids
                ],
                *unresolved_papers,
                *(fresh.get("papers") or []),
            ],
        )
        stage01 = _stage01_projection(
            final_papers,
            final_documents,
            fresh.get("attempts") or [],
            run_id,
        )
        _write_stage01_output(root, stage01, run_id)
        _write_microbatch_stage_cache(
            root,
            "stage01",
            hashes["stage01"],
            run_id,
            cacheable=not _has_stage01_processing_errors(stage01),
        )
        cache_hit = not fresh_paper_ids
    elif stage01 is None:
        stage01 = run_document_normalization(
            papers=papers,
            documents=documents,
            config=config["stage01"]["normalization"],
            workspace=root,
            run_id=run_id,
            grobid_client=grobid_client,
        )
        _write_microbatch_stage_cache(root, "stage01", hashes["stage01"], run_id, cacheable=True)
    output["stage01"] = stage01
    if registry is not None:
        _record_registry_stage(
            registry,
            resume,
            run_id=run_id,
            stage="stage01",
            rows=stage01.get("papers") or [],
        )
    output["_phase1_root"] = root
    output["_phase1_hashes"] = hashes
    _record_stage_timing(
        output, "stage01", started_epoch, started, cache_hit, len(stage01.get("papers") or [])
    )
    return output


def _run_phase1_stage02(
    *, state, config, clients, workspace, run_id, registry=None, resume=None
):
    started_epoch = time.time()
    started = time.perf_counter()
    root = state["_phase1_root"]
    hashes = state["_phase1_hashes"]
    stage02 = (
        None
        if resume is not None
        else _load_cached_microbatch_stage(root, "stage02", hashes["stage02"])
    )
    cache_hit = stage02 is not None
    if stage02 is None and resume is not None:
        by_paper = {row["paper_id"]: row for row in state["stage01"]["papers"]}
        documents = state["stage01"]["documents"]
        reused, pending = [], []
        for paper in by_paper.values():
            if paper.get("decision") != "pass":
                continue
            paper_documents = [
                row for row in documents if row.get("paper_id") == paper["paper_id"]
            ]
            fingerprint = _resume_paper_input(paper, paper_documents)
            plan = _resume_plan(resume, "stage02", paper["paper_id"], None, fingerprint)
            if plan.action == "reuse" and plan.result:
                reused.append(plan.result)
            elif plan.action == "run":
                pending.append(paper)
            elif plan.result:
                reused.append(plan.result)
        attempt_root = _resume_attempt_root(root, resume, "stage02")
        fresh = {"records": []}
        if _resume_stage_active(resume, "stage02") and pending:
            fresh = run_stage02(
                papers=pending,
                documents=documents,
                config=config["stage02"],
                model=clients[config["stage02"].get("model_role", "screening")],
                workspace=attempt_root,
                run_id=run_id,
                on_result=lambda paper, row: _resume_record(
                    resume,
                    "stage02",
                    row,
                    _resume_paper_input(
                        paper,
                        [item for item in documents if item.get("paper_id") == paper["paper_id"]],
                    ),
                ),
            )
        records = _ordered_records(by_paper, [*reused, *(fresh.get("records") or [])])
        stage02 = _stage_output("stage02", records, run_id)
        _write_stage_records(root, "stage02", stage02)
        _write_microbatch_stage_cache(
            root,
            "stage02",
            hashes["stage02"],
            run_id,
            cacheable=not _has_processing_errors(stage02),
        )
        cache_hit = not pending
    elif stage02 is None:
        stage02 = run_stage02(
            papers=state["stage01"]["papers"],
            documents=state["stage01"]["documents"],
            config=config["stage02"],
            model=clients[config["stage02"].get("model_role", "screening")],
            workspace=root,
            run_id=run_id,
        )
        _write_microbatch_stage_cache(
            root,
            "stage02",
            hashes["stage02"],
            run_id,
            cacheable=not _has_processing_errors(stage02),
        )
        _raise_on_screening_infrastructure_error(stage02, "stage02")
    state["stage02"] = stage02
    if registry is not None:
        _record_registry_stage(
            registry,
            resume,
            run_id=run_id,
            stage="stage02",
            rows=stage02.get("records") or [],
        )
    _record_stage_timing(
        state, "stage02", started_epoch, started, cache_hit, len(stage02.get("records") or [])
    )
    return state


def _run_phase1_stage03(
    *,
    state,
    config,
    clients,
    workspace,
    run_id,
    softcite_client,
    registry=None,
    resume=None,
):
    started_epoch = time.time()
    started = time.perf_counter()
    root = state["_phase1_root"]
    hashes = state["_phase1_hashes"]
    stage03 = (
        None
        if resume is not None
        else _load_cached_microbatch_stage(root, "stage03", hashes["stage03"])
    )
    cache_hit = stage03 is not None
    if stage03 is None and resume is not None:
        stage02_by_id = {row["paper_id"]: row for row in state["stage02"]["records"]}
        reused, pending = [], []
        for row in stage02_by_id.values():
            if not row.get("passed"):
                continue
            fingerprint = _resume_paper_input(row, [])
            plan = _resume_plan(resume, "stage03", row["paper_id"], None, fingerprint)
            if plan.action == "reuse" and plan.result:
                reused.append(plan.result)
            elif plan.action == "run":
                pending.append(row)
            elif plan.result:
                reused.append(plan.result)
        attempt_root = _resume_attempt_root(root, resume, "stage03")
        fresh = {"records": []}
        if _resume_stage_active(resume, "stage03") and pending:
            fresh = run_stage03(
                stage02_records=pending,
                documents=state["stage01"]["documents"],
                config=config["stage03"],
                model=clients[config["stage03"].get("model_role", "screening")],
                workspace=attempt_root,
                run_id=run_id,
                softcite=softcite_client,
                on_result=lambda source, row: _resume_record(
                    resume,
                    "stage03",
                    row,
                    _resume_paper_input(source, []),
                ),
            )
        records = _ordered_records(stage02_by_id, [*reused, *(fresh.get("records") or [])])
        stage03 = _stage_output("stage03", records, run_id)
        _write_stage_records(root, "stage03", stage03)
        _write_microbatch_stage_cache(
            root,
            "stage03",
            hashes["stage03"],
            run_id,
            cacheable=not _has_processing_errors(stage03),
        )
        cache_hit = not pending
    elif stage03 is None:
        stage03 = run_stage03(
            stage02_records=state["stage02"]["records"],
            documents=state["stage01"]["documents"],
            config=config["stage03"],
            model=clients[config["stage03"].get("model_role", "screening")],
            workspace=root,
            run_id=run_id,
            softcite=softcite_client,
        )
        _write_microbatch_stage_cache(
            root,
            "stage03",
            hashes["stage03"],
            run_id,
            cacheable=not _has_processing_errors(stage03),
        )
        _raise_on_screening_infrastructure_error(stage03, "stage03")
    state["stage03"] = stage03
    if registry is not None:
        _record_registry_stage(
            registry,
            resume,
            run_id=run_id,
            stage="stage03",
            rows=stage03.get("records") or [],
        )
    _record_stage_timing(
        state, "stage03", started_epoch, started, cache_hit, len(stage03.get("records") or [])
    )
    return state


def _run_phase2_stage04(
    *, index, papers, phase1, config, workspace, run_id, registry=None, resume=None
):
    started_epoch = time.time()
    started = time.perf_counter()
    root = workspace / "microbatches" / f"batch-{index + 1:06d}"
    hashes = _microbatch_stage_hashes(papers, phase1["stage01"]["documents"], config)
    output = dict(phase1)
    stage04 = (
        None
        if resume is not None
        else _load_cached_microbatch_stage(root, "stage04", hashes["stage04"])
    )
    cache_hit = stage04 is not None
    if stage04 is None and resume is not None:
        stage03_by_id = {row["paper_id"]: row for row in phase1["stage03"]["records"]}
        source_documents = phase1["stage01"]["documents"]
        eligible_ids = {
            paper_id for paper_id, row in stage03_by_id.items() if row.get("passed")
        }
        selected_documents = [
            row
            for row in source_documents
            if row.get("paper_id") in eligible_ids and row.get("decision") == "pass"
        ]
        reused_documents, pending_document_ids = [], set()
        reused_papers = []
        pending_paper_ids = set()
        for paper_id, row in stage03_by_id.items():
            if not row.get("passed"):
                continue
            paper_documents = [
                item for item in source_documents if item.get("paper_id") == paper_id
            ]
            plan = _resume_plan(
                resume,
                "stage04",
                paper_id,
                None,
                _resume_paper_input(row, paper_documents),
            )
            if plan.action == "reuse" and plan.result:
                reused_papers.append(plan.result)
            elif plan.action == "run":
                pending_paper_ids.add(str(paper_id))
            elif plan.result:
                reused_papers.append(plan.result)
        for document in selected_documents:
            plan = _resume_plan(
                resume,
                "stage04",
                document["paper_id"],
                document["document_id"],
                _resume_document_input(document),
            )
            if plan.action == "reuse" and plan.result:
                reused_documents.append(plan.result)
            elif plan.action == "run":
                pending_document_ids.add(str(document["document_id"]))
            elif plan.result:
                reused_documents.append(plan.result)
        fresh_paper_ids = pending_paper_ids | {
            str(document["paper_id"])
            for document in selected_documents
            if str(document.get("document_id")) in pending_document_ids
        }
        fresh = {"records": [], "documents": [], "deep_parse_attempts": []}
        if _resume_stage_active(resume, "stage04") and fresh_paper_ids:
            attempt_root = _resume_attempt_root(root, resume, "stage04")
            fresh = run_stage04(
                stage03_records=[
                    row
                    for row in stage03_by_id.values()
                    if str(row["paper_id"]) in fresh_paper_ids
                ],
                documents=[
                    row
                    for row in source_documents
                    if str(row["paper_id"]) in fresh_paper_ids
                ],
                config=config["stage04"],
                workspace=attempt_root,
                run_id=run_id,
                document_ids=pending_document_ids,
                existing_deep_documents=[
                    row
                    for row in reused_documents
                    if str(row["paper_id"]) in fresh_paper_ids
                ],
            )
            for row in fresh.get("documents") or []:
                if str(row.get("document_id")) in pending_document_ids:
                    _resume_record(resume, "stage04", row, _resume_document_input(row))
            for row in fresh.get("records") or []:
                if row.get("paper_id") in eligible_ids:
                    _resume_record(
                        resume,
                        "stage04",
                        row,
                        _resume_paper_input(
                            stage03_by_id[row["paper_id"]],
                            [
                                item
                                for item in source_documents
                                if item.get("paper_id") == row["paper_id"]
                            ],
                        ),
                    )
        fresh_document_ids = {
            str(row["document_id"]) for row in fresh.get("documents") or []
        }
        final_documents = _deduplicate_document_rows(
            [
                *[
                    row
                    for row in reused_documents
                    if str(row["document_id"]) not in fresh_document_ids
                ],
                *(fresh.get("documents") or []),
            ]
        )
        final_records = _ordered_records(
            stage03_by_id,
            [
                *[
                    row
                    for row in reused_papers
                    if str(row["paper_id"]) not in fresh_paper_ids
                ],
                *(fresh.get("records") or []),
            ],
        )
        stage04 = _stage_output("stage04", final_records, run_id)
        stage04.update(
            {
                "documents": final_documents,
                "deep_parse_attempts": fresh.get("deep_parse_attempts") or [],
            }
        )
        _write_stage04_output(root, stage04)
        _write_microbatch_stage_cache(
            root,
            "stage04",
            hashes["stage04"],
            run_id,
            cacheable=not _has_processing_errors(stage04),
        )
        cache_hit = not fresh_paper_ids
    elif stage04 is None:
        stage04 = run_stage04(
            stage03_records=phase1["stage03"]["records"],
            documents=phase1["stage01"]["documents"],
            config=config["stage04"],
            workspace=root,
            run_id=run_id,
        )
        _write_microbatch_stage_cache(
            root,
            "stage04",
            hashes["stage04"],
            run_id,
            cacheable=not _has_processing_errors(stage04),
        )
    output["stage04"] = stage04
    if registry is not None:
        registry.record_stage_results(
            run_id=run_id,
            stage="stage04",
            rows=stage04.get("records") or [],
            prune=False,
        )
    output["_phase2_root"] = root
    output["_phase2_hashes"] = hashes
    _record_stage_timing(
        output, "stage04", started_epoch, started, cache_hit, len(stage04.get("records") or [])
    )
    return output


def _run_phase2_stage05(
    *, state, config, clients, workspace, run_id, registry=None, resume=None
):
    started_epoch = time.time()
    started = time.perf_counter()
    root = state["_phase2_root"]
    hashes = state["_phase2_hashes"]
    stage05 = (
        None
        if resume is not None
        else _load_cached_microbatch_stage(root, "stage05", hashes["stage05"])
    )
    cache_hit = stage05 is not None
    if stage05 is None and resume is not None:
        stage04_by_id = {row["paper_id"]: row for row in state["stage04"]["records"]}
        deep_documents = state["stage04"]["documents"]
        reused, pending, router_checkpoints, auditor_checkpoints = [], [], {}, {}
        for row in stage04_by_id.values():
            if not row.get("passed"):
                continue
            paper_documents = [
                item for item in deep_documents if item.get("paper_id") == row["paper_id"]
            ]
            fingerprint = _resume_paper_input(row, paper_documents)
            plan = _resume_plan(resume, "stage05", row["paper_id"], None, fingerprint)
            if plan.action == "reuse" and plan.result:
                reused.append(plan.result)
                continue
            if plan.action != "run":
                if plan.result:
                    reused.append(plan.result)
                continue
            pending.append(row)
            router_plan = _resume_plan(
                resume, "stage05_router", row["paper_id"], None, fingerprint
            )
            if router_plan.action == "reuse" and router_plan.result:
                router_checkpoints[row["paper_id"]] = router_plan.result
            auditor_plan = _resume_plan(
                resume, "stage05_auditor", row["paper_id"], None, fingerprint
            )
            if auditor_plan.action == "reuse" and auditor_plan.result:
                auditor_checkpoints[row["paper_id"]] = auditor_plan.result
        attempt_root = _resume_attempt_root(root, resume, "stage05")
        fresh = {"records": []}
        if _resume_stage_active(resume, "stage05") and pending:
            fresh = run_stage05(
                stage04_records=pending,
                documents=deep_documents,
                config=config["stage05"],
                router_model=clients["stage05_router"],
                auditor_model=clients["suitability"],
                workspace=attempt_root,
                run_id=run_id,
                router_checkpoints=router_checkpoints,
                auditor_checkpoints=auditor_checkpoints,
                on_router_result=lambda source, row: _resume_record(
                    resume,
                    "stage05_router",
                    row,
                    _resume_paper_input(
                        source,
                        [
                            item
                            for item in deep_documents
                            if item.get("paper_id") == source["paper_id"]
                        ],
                    ),
                ),
                on_auditor_result=lambda source, row: _resume_record(
                    resume,
                    "stage05_auditor",
                    row,
                    _resume_paper_input(
                        source,
                        [
                            item
                            for item in deep_documents
                            if item.get("paper_id") == source["paper_id"]
                        ],
                    ),
                ),
                on_result=lambda source, row: _resume_record_stage05_result(
                    resume, source, row, deep_documents
                ),
            )
        records = _ordered_records(stage04_by_id, [*reused, *(fresh.get("records") or [])])
        candidates = [
            {"paper_id": row["paper_id"], **candidate}
            for row in records
            for candidate in row.get("candidates") or []
        ]
        stage05 = _stage_output("stage05", records, run_id, candidates=candidates)
        _write_stage_records(root, "stage05", stage05)
        _write_microbatch_stage_cache(
            root,
            "stage05",
            hashes["stage05"],
            run_id,
            cacheable=not _has_processing_errors(stage05),
        )
        cache_hit = not pending
    elif stage05 is None:
        stage05 = run_stage05(
            stage04_records=state["stage04"]["records"],
            documents=state["stage04"]["documents"],
            config=config["stage05"],
            router_model=clients["stage05_router"],
            auditor_model=clients["suitability"],
            workspace=root,
            run_id=run_id,
        )
        _write_microbatch_stage_cache(
            root,
            "stage05",
            hashes["stage05"],
            run_id,
            cacheable=not _has_processing_errors(stage05),
        )
        _raise_on_model_infrastructure_error(stage05, "stage05")
    state["stage05"] = stage05
    if registry is not None:
        registry.record_stage_results(
            run_id=run_id,
            stage="stage05",
            rows=stage05.get("records") or [],
            prune=False,
        )
    _record_stage_timing(
        state, "stage05", started_epoch, started, cache_hit, len(stage05.get("records") or [])
    )
    return state


def _aggregate_phase1(batch_results, package, workspace, run_id, stop_index):
    output = {}
    normalized_papers = [row for batch in batch_results for row in batch["stage01"]["papers"]]
    normalized_by_id = {row["paper_id"]: row for row in normalized_papers}
    papers = [normalized_by_id.get(row["paper_id"], row) for row in package["papers"]]
    normalized_documents = [row for batch in batch_results for row in batch["stage01"]["documents"]]
    normalized_document_ids = {row["document_id"] for row in normalized_documents}
    documents = [
        *normalized_documents,
        *[row for row in package["documents"] if row["document_id"] not in normalized_document_ids],
    ]
    attempts = [row for batch in batch_results for row in batch["stage01"]["attempts"]]
    root = workspace / STAGE_DIRS["stage01"]
    write_jsonl(root / "documents.jsonl", documents)
    write_jsonl(root / "paper_bundles.jsonl", papers)
    write_jsonl(root / "parser_attempts.jsonl", attempts)
    summary = {
        "run_id": run_id,
        "stage": "stage01",
        "papers": len(papers),
        "documents": len(documents),
        "package_passed_papers": sum(row.get("decision") == "pass" for row in package["papers"]),
        "package_held_papers": sum(row.get("decision") != "pass" for row in package["papers"]),
        "normalization_attempted_papers": len(normalized_papers),
        "passed_papers": sum(row.get("decision") == "pass" for row in papers),
        "failed_papers": sum(row.get("decision") != "pass" for row in papers),
        "selected_parsers": decision_counts(documents, "selected_parser"),
        "microbatches": len(batch_results),
        "performance": _aggregate_stage_timings(batch_results, "stage01"),
    }
    write_json(root / "stage_summary.json", summary)
    output["stage01"] = {
        "papers": papers,
        "documents": documents,
        "attempts": attempts,
        "summary": summary,
    }
    for key in ("stage02", "stage03"):
        if stop_index < int(key[-2:]):
            continue
        records = [row for batch in batch_results for row in batch[key]["records"]]
        stage_root = workspace / STAGE_DIRS[key]
        write_jsonl(stage_root / "decisions.jsonl", records)
        stage_summary = {
            "run_id": run_id,
            "stage": key,
            "papers": len(records),
            "decisions": decision_counts(records),
            "passed": sum(bool(row.get("passed")) for row in records),
            "processing_errors": sum(row.get("processing_status") == "failed" for row in records),
            "run_status": _stage_run_status(records),
            "microbatches": len(batch_results),
            "performance": _aggregate_stage_timings(batch_results, key),
        }
        write_json(stage_root / "stage_summary.json", stage_summary)
        output[key] = {"records": records, "summary": stage_summary}
    return output


def _aggregate_phase2(batch_results, workspace, run_id, stop_index):
    output = {}
    for key in ("stage04", "stage05"):
        if stop_index < int(key[-2:]):
            continue
        records = [row for batch in batch_results for row in batch[key]["records"]]
        root = workspace / STAGE_DIRS[key]
        write_jsonl(root / "decisions.jsonl", records)
        summary = {
            "run_id": run_id,
            "stage": key,
            "papers": len(records),
            "decisions": decision_counts(records),
            "passed": sum(bool(row.get("passed")) for row in records),
            "processing_errors": sum(row.get("processing_status") == "failed" for row in records),
            "run_status": _stage_run_status(records),
            "microbatches": len(batch_results),
            "performance": _aggregate_stage_timings(batch_results, key),
        }
        stage_output = {"records": records, "summary": summary}
        if key == "stage04":
            documents = [row for batch in batch_results for row in batch[key].get("documents", [])]
            attempts = [
                row for batch in batch_results for row in batch[key].get("deep_parse_attempts", [])
            ]
            stage_output.update({"documents": documents, "deep_parse_attempts": attempts})
            summary["deep_normalized_documents"] = sum(
                row.get("selected_parser") == "mineru" and row.get("decision") == "pass"
                for row in documents
            )
            summary["deep_parse_failed_papers"] = sum(
                row.get("decision") == "deep_parse_failed" for row in records
            )
            write_jsonl(root / "deep_normalization" / "documents.jsonl", documents)
            write_jsonl(root / "deep_normalization" / "parser_attempts.jsonl", attempts)
        if key == "stage05":
            candidates = [
                row for batch in batch_results for row in batch[key].get("candidates", [])
            ]
            stage_output["candidates"] = candidates
            summary["candidates"] = len(candidates)
            write_jsonl(root / "candidates.jsonl", candidates)
        write_json(root / "stage_summary.json", summary)
        output[key] = stage_output
    return output


def _record_stage_timing(state, stage, started_epoch, started, cache_hit, paper_count):
    finished_epoch = time.time()
    state.setdefault("_stage_timings", {})[stage] = {
        "started_epoch": started_epoch,
        "finished_epoch": finished_epoch,
        "duration_seconds": max(0.0, time.perf_counter() - started),
        "cache_hit": bool(cache_hit),
        "paper_count": int(paper_count),
    }


def _aggregate_stage_timings(batch_results, stage):
    rows = [
        batch.get("_stage_timings", {}).get(stage)
        for batch in batch_results
        if batch.get("_stage_timings", {}).get(stage)
    ]
    if not rows:
        return {}
    durations = sorted(float(row["duration_seconds"]) for row in rows)
    started = min(float(row["started_epoch"]) for row in rows)
    finished = max(float(row["finished_epoch"]) for row in rows)
    wall = max(0.0, finished - started)
    papers = sum(int(row.get("paper_count", 0)) for row in rows)

    def percentile(fraction):
        index = min(len(durations) - 1, max(0, int((len(durations) - 1) * fraction)))
        return durations[index]

    return {
        "microbatches_measured": len(rows),
        "cache_hits": sum(bool(row.get("cache_hit")) for row in rows),
        "batch_duration_seconds": {
            "p50": round(percentile(0.50), 3),
            "p90": round(percentile(0.90), 3),
            "max": round(durations[-1], 3),
        },
        "worker_seconds": round(sum(durations), 3),
        "wall_seconds": round(wall, 3),
        "papers_per_minute": round(papers * 60.0 / wall, 3) if wall else None,
    }


def _load_or_run_package(config, corpus_root, workspace, run_id, *, resume=None):
    root = workspace / "stage_01_document_preparation" / "package"
    if resume is not None:
        manifest_path = workspace / "stage_00_remote_corpus" / "source_manifest.jsonl"
        source_rows = read_jsonl(manifest_path)
        existing_papers = read_jsonl(root / "papers.jsonl") if (root / "papers.jsonl").is_file() else []
        existing_documents = (
            read_jsonl(root / "documents.jsonl") if (root / "documents.jsonl").is_file() else []
        )
        existing_by_paper: dict[str, list[dict[str, Any]]] = {}
        for document in existing_documents:
            existing_by_paper.setdefault(str(document.get("paper_id") or ""), []).append(document)
        reused_papers = []
        pending_ids = set()
        for source in source_rows:
            paper_id = str(source["paper_id"])
            fingerprint = input_fingerprint(_resume_input_value(source))
            plan = _resume_plan(
                resume,
                "stage01_package",
                paper_id,
                None,
                fingerprint,
            )
            if plan.action == "reuse" and plan.result:
                reused_papers.append(plan.result)
            elif plan.action == "run":
                pending_ids.add(paper_id)
            elif plan.result:
                reused_papers.append(plan.result)
        fresh = {"papers": [], "documents": [], "duplicate_groups": [], "summary": {}}
        if pending_ids and _resume_stage_active(resume, "stage01_package"):
            fresh = run_paper_package(
                corpus_root=corpus_root,
                config=config["stage01"].get("package") or config["stage01"],
                workspace=_resume_attempt_root(workspace, resume, "stage01_package"),
                run_id=run_id,
                paper_ids=pending_ids,
            )
        fresh_ids = {str(row["paper_id"]) for row in fresh.get("papers") or []}
        retained_reused = [
            row for row in reused_papers if str(row.get("paper_id") or "") not in fresh_ids
        ]
        papers = _deduplicate_rows([*retained_reused, *(fresh.get("papers") or [])])
        retained_ids = {str(row["paper_id"]) for row in retained_reused}
        documents = _deduplicate_document_rows(
            [
                *[
                    document
                    for paper_id in retained_ids
                    for document in existing_by_paper.get(paper_id, [])
                ],
                *(fresh.get("documents") or []),
            ]
        )
        for row in fresh.get("papers") or []:
            paper_documents = [
                item for item in documents if item.get("paper_id") == row.get("paper_id")
            ]
            source = next(
                (item for item in source_rows if item.get("paper_id") == row.get("paper_id")),
                row,
            )
            _resume_record(
                resume,
                "stage01_package",
                row,
                input_fingerprint(_resume_input_value(source)),
                artifacts=[
                    item["source_path"]
                    for item in paper_documents
                    if item.get("source_path") and Path(str(item["source_path"])).is_file()
                ],
            )
        summary = {
            "run_id": run_id,
            "stage": "stage01",
            "papers": len(papers),
            "documents": len(documents),
            "package_statuses": decision_counts(papers, "package_status"),
            "passed": sum(row.get("decision") == "pass" for row in papers),
            "held": sum(row.get("decision") != "pass" for row in papers),
            "config_hash": resume["fingerprints"]["stage01_package"],
        }
        write_jsonl(root / "papers.jsonl", papers)
        write_jsonl(root / "documents.jsonl", documents)
        write_jsonl(root / "duplicate_groups.jsonl", fresh.get("duplicate_groups") or [])
        write_json(root / "stage_summary.json", summary)
        return {"papers": papers, "documents": documents, "summary": summary}
    if config.get("resume_completed_stages") and (root / "stage_summary.json").is_file():
        return {
            "papers": read_jsonl(root / "papers.jsonl"),
            "documents": read_jsonl(root / "documents.jsonl"),
            "summary": read_json(root / "stage_summary.json"),
        }
    return run_paper_package(
        corpus_root=corpus_root,
        config=config["stage01"].get("package") or config["stage01"],
        workspace=workspace,
        run_id=run_id,
    )


def _resume_runtime(config, options):
    if not options:
        return None
    store = options.get("store")
    if store is None:
        run_root = options.get("run_root")
        if not run_root:
            raise ValueError("resume_options requires store or run_root")
        store = ResumeStateStore.for_run_root(run_root)
    return {
        "store": store,
        "generation": int(options.get("generation", 0)),
        "outer_batch_id": str(options.get("outer_batch_id") or Path(config["workspace"]).name),
        "target_slot_start": int(options.get("target_slot_start", 1)),
        "retry_only": bool(options.get("retry_only", False)),
        "pending_only": bool(options.get("pending_only", False)),
        "invalidated_stages": set(options.get("invalidated_stages") or []),
        "fingerprints": scientific_stage_fingerprints(config),
        "start_index": int(str(options.get("start_stage", "stage00")).removeprefix("stage")),
        "stop_index": int(str(options.get("stop_stage", config["stop_after"])).removeprefix("stage")),
    }


def _checkpoint_stage00(resume, config, workspace):
    manifest = workspace / "stage_00_remote_corpus" / "source_manifest.jsonl"
    for row in read_jsonl(manifest):
        fingerprint = input_fingerprint(
            {"remote_uri": (row.get("main_document") or {}).get("remote_uri")}
        )
        plan = _resume_plan(
            resume,
            "stage00",
            row["paper_id"],
            None,
            fingerprint,
        )
        if plan.action != "run":
            continue
        _resume_record(
            resume,
            "stage00",
            {
                **row,
                "processing_status": (
                    "completed" if row.get("copy_status") == "complete" else "failed"
                ),
                "decision": (
                    "copied" if row.get("copy_status") == "complete" else "copy_incomplete"
                ),
                "passed": row.get("copy_status") == "complete",
            },
            fingerprint,
        )


def _resume_plan(resume, stage, paper_id, document_id, fingerprint):
    active = _resume_stage_active(resume, stage)
    return resume["store"].plan_work(
        outer_batch_id=resume["outer_batch_id"],
        stage=stage,
        paper_id=str(paper_id),
        document_id=str(document_id) if document_id else None,
        config_fingerprint=resume["fingerprints"][stage],
        input_fingerprint=fingerprint,
        allow_pending=active,
        retry_only=resume["retry_only"],
        invalidated=stage in resume["invalidated_stages"],
        upstream_ready=stage != "stage00",
    )


def _resume_stage_active(resume, stage):
    parent = (
        "stage01"
        if stage == "stage01_package"
        else "stage05"
        if stage in {"stage05_router", "stage05_auditor"}
        else stage
    )
    index = int(parent.removeprefix("stage"))
    return resume["start_index"] <= index <= resume["stop_index"]


def _resume_record(resume, stage, row, fingerprint, *, artifacts=None):
    return resume["store"].record_result(
        generation=resume["generation"],
        outer_batch_id=resume["outer_batch_id"],
        stage=stage,
        paper_id=str(row["paper_id"]),
        document_id=(str(row["document_id"]) if row.get("document_id") else None),
        config_fingerprint=resume["fingerprints"][stage],
        input_fingerprint=fingerprint,
        row=row,
        artifacts=artifacts if artifacts is not None else result_artifacts(row),
    )


def _resume_record_stage05_result(resume, source, row, deep_documents):
    fingerprint = _resume_paper_input(
        source,
        [
            item
            for item in deep_documents
            if item.get("paper_id") == source["paper_id"]
        ],
    )
    _resume_record(resume, "stage05", row, fingerprint)
    if row.get("processing_status") != "failed":
        return
    if not row.get("router_response"):
        _resume_record(resume, "stage05_router", row, fingerprint)
    elif not row.get("model_response"):
        _resume_record(resume, "stage05_auditor", row, fingerprint)


def _resume_attempt_root(root: Path, resume, stage: str) -> Path:
    return (
        root
        / "resume_attempts"
        / f"generation-{resume['generation']:04d}"
        / stage
    )


def _resume_document_input(document):
    return document_input_fingerprint(document)


def _resume_paper_input(paper, documents):
    return paper_input_fingerprint(paper, documents)


def _resume_input_value(value):
    return stable_input_value(value)


def _ordered_records(upstream_by_id, rows):
    by_id = {str(row["paper_id"]): row for row in rows if row.get("paper_id")}
    return [by_id[paper_id] for paper_id in upstream_by_id if paper_id in by_id]


def _deduplicate_rows(rows):
    by_id = {str(row["paper_id"]): row for row in rows if row.get("paper_id")}
    return [by_id[key] for key in sorted(by_id)]


def _deduplicate_document_rows(rows):
    by_id = {
        str(row["document_id"]): row for row in rows if row.get("document_id")
    }
    return [by_id[key] for key in sorted(by_id)]


def _stage_output(stage, records, run_id, *, candidates=None):
    summary = {
        "run_id": run_id,
        "stage": stage,
        "papers": len(records),
        "decisions": decision_counts(records),
        "passed": sum(bool(row.get("passed")) for row in records),
        "processing_errors": sum(
            row.get("processing_status") == "failed" for row in records
        ),
        "run_status": _stage_run_status(records),
    }
    output = {"records": records, "summary": summary}
    if candidates is not None:
        output["candidates"] = candidates
        summary["candidates"] = len(candidates)
    return output


def _stage01_projection(papers, documents, attempts, run_id):
    summary = {
        "run_id": run_id,
        "stage": "stage01",
        "papers": len(papers),
        "documents": len(documents),
        "passed_papers": sum(row.get("decision") == "pass" for row in papers),
        "failed_papers": sum(row.get("decision") != "pass" for row in papers),
        "partial_si_parse_papers": sum(bool(row.get("partial_si_parse")) for row in papers),
        "failed_supplementary_documents": sum(
            len(row.get("failed_supplementary_document_ids") or []) for row in papers
        ),
        "selected_parsers": decision_counts(documents, "selected_parser"),
    }
    return {
        "papers": papers,
        "documents": documents,
        "attempts": attempts,
        "summary": summary,
    }


def _write_stage01_output(root, output, run_id):
    stage_root = root / STAGE_DIRS["stage01"]
    write_jsonl(stage_root / "documents.jsonl", output.get("documents") or [])
    write_jsonl(stage_root / "paper_bundles.jsonl", output.get("papers") or [])
    write_jsonl(stage_root / "parser_attempts.jsonl", output.get("attempts") or [])
    write_json(stage_root / "stage_summary.json", output["summary"])


def _write_stage_records(root, stage, output):
    stage_root = root / STAGE_DIRS[stage]
    write_jsonl(stage_root / "decisions.jsonl", output.get("records") or [])
    if stage == "stage05":
        write_jsonl(stage_root / "candidates.jsonl", output.get("candidates") or [])
    write_json(stage_root / "stage_summary.json", output["summary"])


def _write_stage04_output(root, output):
    _write_stage_records(root, "stage04", output)
    stage_root = root / STAGE_DIRS["stage04"] / "deep_normalization"
    write_jsonl(stage_root / "documents.jsonl", output.get("documents") or [])
    write_jsonl(stage_root / "parser_attempts.jsonl", output.get("deep_parse_attempts") or [])


def _has_stage01_processing_errors(output):
    return any(
        row.get("processing_status") == "failed"
        for row in [*(output.get("papers") or []), *(output.get("documents") or [])]
    )


def _record_registry_stage(registry, resume, *, run_id, stage, rows, prune=True):
    result = registry.record_stage_results(
        run_id=run_id,
        stage=stage,
        rows=rows,
        prune=prune,
    )
    if resume is not None:
        for paper_id in result.get("deleted_paper_ids") or []:
            resume["store"].set_local_assets_state(str(paper_id), "pruned_terminal")
    return result


def _paper_batches(papers, size):
    eligible = [row for row in papers if row.get("decision") == "pass"]
    size = max(1, int(size))
    return [eligible[index : index + size] for index in range(0, len(eligible), size)]


def _microbatch_stage_hashes(papers, documents, config):
    inputs = {
        "paper_ids": [row["paper_id"] for row in papers],
        "documents": sorted(
            (row["document_id"], row.get("sha256"), row.get("source_path")) for row in documents
        ),
    }
    stage01_config = config.get("stage01", {}).get("normalization") or {}
    stage02_config = config.get("stage02", {})
    stage03_config = config.get("stage03", {})
    stage04_config = config.get("stage04", {})
    stage01 = canonical_hash(
        {
            "inputs": inputs,
            "config": _stage_config_cache_value("stage01", stage01_config),
            "implementation": DOCUMENT_NORMALIZATION_IMPLEMENTATION_VERSION,
        }
    )
    stage02_model = _model_cache_signature(
        config["models"][config["stage02"].get("model_role", "screening")]
    )
    stage03_model = _model_cache_signature(
        config["models"][config["stage03"].get("model_role", "screening")]
    )
    stage02 = canonical_hash(
        {
            "upstream": stage01,
            "config": _stage_config_cache_value("stage02", stage02_config),
            "model": stage02_model,
            "prompts": [STAGE02_CLASSIFY_VERSION, STAGE02_PASS_VERIFY_VERSION],
            "implementation": COMPUTATIONAL_CONTENT_IMPLEMENTATION_VERSION,
        }
    )
    stage03 = canonical_hash(
        {
            "upstream": stage02,
            "config": _stage_config_cache_value("stage03", stage03_config),
            "model": stage03_model,
            "prompt": STAGE03_VERSION,
            "capability_files": _stage03_capability_fingerprints(stage03_config),
        }
    )
    stage04 = canonical_hash(
        {
            "upstream": stage03,
            "config": _stage_config_cache_value("stage04", stage04_config),
            "mineru_external_files": _mineru_external_file_fingerprints(stage04_config),
        }
    )
    stage05 = canonical_hash(
        {
            "upstream": stage04,
            "config": _json_safe(config.get("stage05", {})),
            "router_model": _model_cache_signature(
                config.get("models", {}).get("stage05_router") or {}
            ),
            "auditor_model": _model_cache_signature(
                config.get("models", {}).get("suitability") or {}
            ),
            "prompts": [STAGE05_ROUTER_VERSION, STAGE05_VERSION],
        }
    )
    return {
        "stage01": stage01,
        "stage02": stage02,
        "stage03": stage03,
        "stage04": stage04,
        "stage05": stage05,
    }


def _model_cache_signature(config):
    return {
        key: config.get(key)
        for key in (
            "model",
            "base_url",
            "thinking",
            "chat_template_kwargs",
            "max_tokens",
            "fallback_models",
        )
    }


def _stage_config_cache_value(stage, config):
    value = _json_safe(config)
    service_key = "grobid" if stage == "stage01" else "softcite" if stage == "stage03" else None
    if stage == "stage04" and isinstance(value, dict):
        # MinerU semantics exclude forwarding/runtime endpoints, but preserve parser settings.
        value.get("mineru", {}).pop("api_url", None)
        if "softcite" in value:
            value["softcite"].pop("base_url", None)
    if service_key and isinstance(value.get(service_key), dict):
        value[service_key].pop("base_url", None)
        value[service_key].pop("_sandbox_instance_configs", None)
    return value


def _stage03_capability_fingerprints(config):
    return [
        _file_fingerprint(config.get(key))
        for key in (
            "toolbox_capabilities",
            "software_aliases",
            "external_software_aliases",
        )
        if config.get(key)
    ]


def _file_fingerprint(value):
    path = Path(str(value)).expanduser().resolve()
    item = {"path": str(path), "exists": path.is_file()}
    if path.is_file():
        item.update({"size_bytes": path.stat().st_size, "sha256": sha256_file(path)})
    return item


def _mineru_external_file_fingerprints(stage_config):
    environment = (stage_config.get("mineru") or {}).get("environment") or {}
    output = []
    for value in sorted(
        str(item) for key, item in environment.items() if key.endswith("_CONFIG_JSON") and item
    ):
        path = Path(value).expanduser().resolve()
        item = {"path": str(path), "exists": path.is_file()}
        if path.is_file():
            item.update({"size_bytes": path.stat().st_size, "sha256": sha256_file(path)})
        output.append(item)
    return output


_stage02_external_file_fingerprints = _mineru_external_file_fingerprints


def _load_cached_microbatch_stage(root, stage, expected_hash):
    stage_root = root / STAGE_DIRS[stage]
    cache_path = stage_root / "stage_cache.json"
    if not cache_path.is_file():
        return None
    cache = read_json(cache_path)
    if cache.get("status") != "completed" or cache.get("stage_hash") != expected_hash:
        return None
    try:
        if stage == "stage01":
            return {
                "documents": read_jsonl(stage_root / "documents.jsonl"),
                "papers": read_jsonl(stage_root / "paper_bundles.jsonl"),
                "attempts": read_jsonl(stage_root / "parser_attempts.jsonl"),
                "summary": read_json(stage_root / "stage_summary.json"),
            }
        output = {
            "records": read_jsonl(stage_root / "decisions.jsonl"),
            "summary": read_json(stage_root / "stage_summary.json"),
        }
        if stage == "stage04":
            output["documents"] = read_jsonl(stage_root / "deep_normalization" / "documents.jsonl")
            output["deep_parse_attempts"] = read_jsonl(
                stage_root / "deep_normalization" / "parser_attempts.jsonl"
            )
        if stage == "stage05":
            output["candidates"] = read_jsonl(stage_root / "candidates.jsonl")
        return output
    except (FileNotFoundError, ValueError):
        return None


def _write_microbatch_stage_cache(root, stage, stage_hash, run_id, *, cacheable):
    stage_root = root / STAGE_DIRS[stage]
    write_json(
        stage_root / "stage_cache.json",
        {
            "stage": stage,
            "stage_hash": stage_hash,
            "status": "completed" if cacheable else "completed_with_errors",
            "produced_run_id": run_id,
        },
    )


def _has_processing_errors(output):
    rows = output.get("records", [])
    return any(row.get("processing_status") == "failed" for row in rows)


def _raise_on_screening_infrastructure_error(output, stage):
    _raise_on_model_infrastructure_error(output, stage)


def _raise_on_model_infrastructure_error(output, stage):
    errors = [
        row.get("error") or {}
        for row in (output.get("records") or [])
        if row.get("processing_status") == "failed"
    ]
    infrastructure = [
        error
        for error in errors
        if error.get("error_type") == "ManagedScreeningServiceError"
        or is_transient_connection_error(
            RuntimeError(f"{error.get('error_type', '')}: {error.get('message', '')}")
        )
    ]
    if infrastructure:
        first = infrastructure[0]
        raise ManagedScreeningServiceError(
            f"{stage} lost its model endpoint; aborting this batch "
            f"({len(infrastructure)} paper errors in this microbatch; "
            f"first={first.get('error_type')}: {first.get('message')})"
        )


def _stage_run_status(records):
    if not records:
        return "not_applicable"
    failures = sum(row.get("processing_status") == "failed" for row in records)
    if failures == len(records):
        return "infrastructure_failed"
    if failures:
        return "completed_with_errors"
    return "completed"


def _clients(config, workspace, callers, screening_config, stop_index, *, include_screening=True):
    values = {
        "screening": screening_config,
        **{key: value for key, value in config["models"].items() if key != "screening"},
    }
    required = set()
    if include_screening and stop_index >= 2:
        required.add(config["stage02"].get("model_role", "screening"))
    if include_screening and stop_index >= 3:
        required.add(config["stage03"].get("model_role", "screening"))
    if stop_index >= 5:
        required.add("stage05_router")
        required.add("suitability")
    if stop_index >= 6:
        required.add("builder")
    if stop_index >= 7:
        required.add("judge")
    return {
        role: RoleModelClient(
            role=role,
            config=values[role],
            cache_root=workspace / "llm_cache",
            **({"caller": callers[role]} if role in callers else {}),
        )
        for role in required
    }


def _grobid_service(config, stack):
    value = config.get("grobid") or {}
    if value.get("manage_service", False):
        stack.enter_context(
            managed_service(
                value, service_name="GROBID", health_path="/api/isalive", sandbox_service="grobid"
            )
        )
    return GrobidClient(
        base_url=str(value.get("base_url", "http://127.0.0.1:8070")),
        timeout_seconds=int(value.get("timeout_seconds", 900)),
        retries=int(value.get("retries", 2)),
    )


def _softcite_service(config, stack):
    value = config.get("softcite") or {}
    if not value.get("enabled", False):
        return None
    instance_configs = value.get("_sandbox_instance_configs") or []
    if instance_configs:
        runtime = instance_configs[0]["_sandbox_runtime"]
        with ThreadPoolExecutor(max_workers=len(instance_configs)) as executor:
            futures = [
                executor.submit(
                    runtime.start_service,
                    "softcite",
                    item,
                    instance=int(item.get("_sandbox_instance", 0)),
                )
                for item in instance_configs
            ]
            for future in futures:
                future.result()
        return SoftciteClientPool(
            [stack.enter_context(softcite_service(item)) for item in instance_configs]
        )
    if value.get("manage_service", False):
        return stack.enter_context(softcite_service(value))
    return SoftciteClient(
        base_url=str(value.get("base_url", "http://127.0.0.1:8060")),
        timeout_seconds=int(value.get("timeout_seconds", 600)),
        retries=int(value.get("retries", 2)),
        service_log=value.get("service_log"),
    )


def _sandbox_options_from_config(config):
    from src.sandbox.manager import (
        DEFAULT_BASE_URL,
        DEFAULT_IMAGE,
        DEFAULT_INVENTORY,
        DEFAULT_PROJECT,
        DEFAULT_SOURCE,
        SandboxRunOptions,
    )

    value = (config.get("execution") or {}).get("sandbox") or {}
    return SandboxRunOptions(
        cpu=int(value.get("cpu", 128)),
        memory=str(value.get("memory", "256Gi")),
        lifecycle_minutes=int(value.get("lifecycle_minutes", 1440)),
        startup_timeout_seconds=int(value.get("startup_timeout_seconds", 3600)),
        cleanup=str(value.get("cleanup", "stop")),
        source=Path(value.get("source") or DEFAULT_SOURCE),
        inventory=Path(value.get("inventory") or DEFAULT_INVENTORY),
        base_url=str(value.get("base_url", DEFAULT_BASE_URL)),
        project=str(value.get("project", DEFAULT_PROJECT)),
        image=str(value.get("image", DEFAULT_IMAGE)),
        api_key_env=str(value.get("api_key_env", "RCB_SANDBOX_API_KEY")),
    )


def _apply_sandbox(config, runtime):
    stage04 = config.setdefault("stage04", {})
    mineru = stage04.setdefault("mineru", {})
    if not mineru.get("managed_gpu"):
        mineru.setdefault("environment", {})["_sandbox_runtime"] = runtime
    stage01 = config.setdefault("stage01", {})
    normalization = stage01.setdefault("normalization", {})
    grobid = normalization.setdefault("grobid", {})
    grobid.update(runtime.service_config("grobid", grobid, instance=0))
    grobid["manage_service"] = True
    recovery_timeout = int(runtime.options.startup_timeout_seconds) + 300
    grobid["timeout_seconds"] = max(int(grobid.get("timeout_seconds", 900)), recovery_timeout)
    stage03 = config.setdefault("stage03", {})
    if "softcite" in config.get("stage04", {}) and "softcite" not in stage03:
        stage03["softcite"] = config["stage04"]["softcite"]
    softcite = stage03.setdefault("softcite", {})
    if softcite.get("enabled", False):
        instances = max(1, int(softcite.get("instances", 1)))
        configs = [
            runtime.service_config("softcite", softcite, instance=index)
            for index in range(instances)
        ]
        softcite.update(configs[0])
        softcite["manage_service"] = True
        softcite["timeout_seconds"] = max(
            int(softcite.get("timeout_seconds", 600)), recovery_timeout
        )
        for item in configs:
            item["manage_service"] = True
            item["timeout_seconds"] = softcite["timeout_seconds"]
        softcite["_sandbox_instance_configs"] = configs
    config["execution_backend"] = "sandbox"


def _run_id(config):
    return f"run-{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ')}-{canonical_hash(_json_safe(config))[:8]}"


def _config_snapshot(config, run_id):
    value = _json_safe(config)
    value["run_id"] = run_id
    return value


def _json_safe(value):
    if isinstance(value, dict):
        return {
            str(key): ("managed_sandbox_runtime" if key == "_sandbox_runtime" else _json_safe(item))
            for key, item in value.items()
        }
    if isinstance(value, (list, tuple)):
        return [_json_safe(item) for item in value]
    if isinstance(value, Path):
        return str(value)
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    return f"<{type(value).__name__}>"


def _finish(result, config, workspace, registry=None):
    stage_summaries = [
        value
        for key, value in result.items()
        if key.startswith("stage") and isinstance(value, dict)
    ]
    result["status"] = (
        "completed_with_infrastructure_errors"
        if any(item.get("run_status") == "infrastructure_failed" for item in stage_summaries)
        else "completed"
    )
    result["stop_after"] = config["stop_after"]
    if registry is not None:
        result["registry"] = registry.finish_run(run_id=result["run_id"], status=result["status"])
    write_json(workspace / "run_summary.json", result)
    return result
