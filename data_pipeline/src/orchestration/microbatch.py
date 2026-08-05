from __future__ import annotations

import contextlib
import hashlib
import json
import queue
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator

from src.core.io import read_json, read_jsonl, write_json, write_jsonl
from src.core.logging import pipeline_logger, value_counts
from src.integrations.grobid_quantities import grobid_quantities_service
from src.integrations.softcite import softcite_service
from src.stages.stage02_parsing import extract_documents_with_grobid, grobid_service
from src.stages.stage03_software_coverage import (
    assess_software_coverage,
    software_coverage_summary,
)
from src.stages.stage03_software_coverage.toolbox import load_toolbox_profile
from src.stages.stage04_resource_limits import (
    assess_resource_limits,
    bypass_resource_limits,
    resource_limits_summary,
)
from src.stages.stage05_asset_collection import run_asset_collection
from src.stages.stage06_builder import run_builder_stage
from src.stages.stage07_judge import run_judge_stage

STOP_AFTER_STAGE = {
    "grobid_extract": 2,
    "software_coverage": 3,
    "resource_limits": 4,
    "asset_collection": 5,
    "builder": 6,
    "judge": 7,
}
STAGE_NAMES = {
    2: "stage_02_grobid_extract",
    3: "stage_03_software_coverage",
    4: "stage_04_resource_limits",
    5: "stage_05_asset_collection",
    6: "stage_06_builder",
    7: "stage_07_judge",
}


@dataclass(frozen=True)
class MicrobatchOptions:
    size: int
    concurrency: int
    resume: bool
    stage_limits: dict[int, int]
    softcite_instances: int

    @classmethod
    def from_config(cls, config: dict[str, Any], end_stage: int) -> MicrobatchOptions:
        raw = dict(config.get("microbatch") or {})
        size = int(raw.get("size", 10))
        concurrency = int(raw.get("concurrency", 5))
        if size < 1 or concurrency < 1:
            raise ValueError("microbatch.size and microbatch.concurrency must be positive")
        stage_limits: dict[int, int] = {}
        for raw_stage, raw_limit in (raw.get("stage_limits") or {}).items():
            stage = _parse_stage_number(raw_stage)
            limit = int(raw_limit)
            if stage < 2 or stage > 7 or limit < 1:
                raise ValueError("microbatch.stage_limits must map Stage 02-07 to positive values")
            stage_limits[stage] = min(concurrency, limit)
        for stage in range(2, end_stage + 1):
            stage_limits.setdefault(stage, concurrency)
        raw_instances = raw.get("softcite_instances", "auto")
        softcite_instances = (
            stage_limits.get(3, concurrency)
            if str(raw_instances).casefold() == "auto"
            else int(raw_instances)
        )
        if softcite_instances < 1:
            raise ValueError("microbatch.softcite_instances must be positive or 'auto'")
        return cls(
            size=size,
            concurrency=concurrency,
            resume=bool(raw.get("resume", True)),
            stage_limits=stage_limits,
            softcite_instances=min(softcite_instances, stage_limits.get(3, concurrency)),
        )


class ClientPool:
    def __init__(self, clients: list[Any]) -> None:
        if not clients:
            raise ValueError("client pool cannot be empty")
        self._clients: queue.Queue[Any] = queue.Queue()
        for client in clients:
            self._clients.put(client)

    @contextlib.contextmanager
    def acquire(self) -> Iterator[Any]:
        client = self._clients.get()
        try:
            yield client
        finally:
            self._clients.put(client)


def run_microbatch_stages(
    *,
    config_path: Path,
    config: dict[str, Any],
    base: Path,
    workspace: Path,
    corpus_root: Path,
    inventory: list[dict[str, Any]],
    canonical_inventory: list[dict[str, Any]],
    duplicate_inventory: list[dict[str, Any]],
    supplementary_inventory: list[dict[str, Any]],
    exclude_supplementary: bool,
) -> dict[str, Any]:
    stop_after = str(config.get("stop_after", "judge"))
    if stop_after not in STOP_AFTER_STAGE:
        raise ValueError(f"unsupported stop_after value: {stop_after}")
    end_stage = STOP_AFTER_STAGE[stop_after]
    options = MicrobatchOptions.from_config(config, end_stage)
    if end_stage >= 5 and (config.get("stage05") or {}).get("paper_limit") is not None:
        raise ValueError("microbatch mode does not support stage05.paper_limit")

    batches = [
        canonical_inventory[index : index + options.size]
        for index in range(0, len(canonical_inventory), options.size)
    ]
    microbatch_root = workspace / "microbatches"
    microbatch_root.mkdir(parents=True, exist_ok=True)
    write_json(
        microbatch_root / "run_config.json",
        {
            "schema_version": 1,
            "size": options.size,
            "concurrency": options.concurrency,
            "stage_limits": {str(key): value for key, value in options.stage_limits.items()},
            "softcite_instances": options.softcite_instances,
            "stop_after": stop_after,
            "batches": len(batches),
            "documents": len(canonical_inventory),
        },
    )
    pipeline_logger().info(
        "MICROBATCH START | documents=%d | batches=%d | size=%d | concurrency=%d | "
        "stage_limits=%s | softcite_instances=%d | stop_after=%s",
        len(canonical_inventory),
        len(batches),
        options.size,
        options.concurrency,
        options.stage_limits,
        options.softcite_instances,
        stop_after,
    )

    toolbox = _load_toolbox(config, base) if end_stage >= 3 else {}
    semaphores = {
        stage: threading.BoundedSemaphore(limit)
        for stage, limit in options.stage_limits.items()
        if stage <= end_stage
    }
    if options.resume and _all_batches_complete(batches, microbatch_root, end_stage):
        results = _run_batches(
            batches=batches,
            root=microbatch_root,
            config=config,
            base=base,
            toolbox=toolbox,
            options=options,
            end_stage=end_stage,
            semaphores=semaphores,
            clients={},
        )
    else:
        with _pipeline_clients(config, options, end_stage) as clients:
            results = _run_batches(
                batches=batches,
                root=microbatch_root,
                config=config,
                base=base,
                toolbox=toolbox,
                options=options,
                end_stage=end_stage,
                semaphores=semaphores,
                clients=clients,
            )

    summaries = _aggregate_outputs(
        results=results,
        workspace=workspace,
        config=config,
        inventory=inventory,
        duplicate_inventory=duplicate_inventory,
        supplementary_inventory=supplementary_inventory,
        exclude_supplementary=exclude_supplementary,
        end_stage=end_stage,
    )
    summary = {
        "source_mode": "corpus",
        "execution_mode": "microbatch",
        "stopped_after": stop_after,
        "config": str(config_path),
        "corpus_root": str(corpus_root),
        "workspace": str(workspace),
        "pdf_files": len(inventory),
        "microbatch": {
            "size": options.size,
            "concurrency": options.concurrency,
            "stage_limits": {str(key): value for key, value in options.stage_limits.items()},
            "softcite_instances": options.softcite_instances,
            "batches": len(batches),
        },
        **summaries,
    }
    write_json(workspace / "run_summary.json", summary)
    pipeline_logger().info("MICROBATCH COMPLETE | summary=%s", summary["microbatch"])
    return summary


@contextlib.contextmanager
def _pipeline_clients(
    config: dict[str, Any], options: MicrobatchOptions, end_stage: int
) -> Iterator[dict[str, Any]]:
    clients: dict[str, Any] = {}
    with contextlib.ExitStack() as stack:
        grobid_config = config.get("grobid_extract", {})
        runtime = grobid_config.get("_sandbox_runtime")
        softcite_configs: list[dict[str, Any]] = []
        if end_stage >= 3:
            softcite_config = config.get("software_coverage", {})
            if runtime is not None:
                softcite_configs = [
                    runtime.service_config("softcite", softcite_config, instance=index)
                    for index in range(options.softcite_instances)
                ]
            else:
                softcite_configs = [softcite_config]
        quantities_config = config.get("grobid_quantities", {})
        use_quantities = end_stage >= 4 and (config.get("stage04") or {}).get("enabled", True)
        if runtime is not None:
            services = [("grobid", grobid_config, 0)]
            services.extend(
                ("softcite", item, int(item.get("_sandbox_instance", 0)))
                for item in softcite_configs
            )
            if use_quantities:
                services.append(("quantities", quantities_config, 0))
            with ThreadPoolExecutor(
                max_workers=len(services), thread_name_prefix="sandbox-service-start"
            ) as executor:
                futures = [
                    executor.submit(runtime.start_service, name, item, instance=instance)
                    for name, item, instance in services
                ]
                for future in futures:
                    future.result()

        clients["grobid"] = stack.enter_context(grobid_service(grobid_config))
        if end_stage >= 3:
            softcite_clients = [
                stack.enter_context(softcite_service(item)) for item in softcite_configs
            ]
            if runtime is None and options.softcite_instances > 1:
                softcite_clients *= options.softcite_instances
            clients["softcite"] = ClientPool(softcite_clients)
        if use_quantities:
            clients["quantities"] = stack.enter_context(
                grobid_quantities_service(quantities_config)
            )
        yield clients


def _run_batches(
    *,
    batches: list[list[dict[str, Any]]],
    root: Path,
    config: dict[str, Any],
    base: Path,
    toolbox: dict[str, Any],
    options: MicrobatchOptions,
    end_stage: int,
    semaphores: dict[int, threading.BoundedSemaphore],
    clients: dict[str, Any],
) -> list[dict[str, Any]]:
    if not batches:
        return []
    ordered: list[dict[str, Any] | None] = [None] * len(batches)
    errors: list[tuple[int, BaseException]] = []
    with ThreadPoolExecutor(
        max_workers=min(options.concurrency, len(batches)),
        thread_name_prefix="pipeline-microbatch",
    ) as executor:
        futures = {
            executor.submit(
                _run_one_batch,
                batch_number=index,
                documents=documents,
                root=root / f"batch_{index:06d}",
                config=config,
                base=base,
                toolbox=toolbox,
                options=options,
                end_stage=end_stage,
                semaphores=semaphores,
                clients=clients,
            ): index
            for index, documents in enumerate(batches, start=1)
        }
        for future in as_completed(futures):
            index = futures[future]
            try:
                ordered[index - 1] = future.result()
                pipeline_logger().info(
                    "MICROBATCH COMPLETE | batch=%06d | completed=%d/%d",
                    index,
                    sum(item is not None for item in ordered),
                    len(batches),
                )
            except BaseException as exc:
                errors.append((index, exc))
                pipeline_logger().exception("MICROBATCH FAILED | batch=%06d", index)
    if errors:
        details = "; ".join(
            f"batch_{index:06d}: {type(exc).__name__}: {exc}" for index, exc in errors
        )
        raise RuntimeError(f"{len(errors)} microbatch(es) failed: {details}") from errors[0][1]
    return [item for item in ordered if item is not None]


def _run_one_batch(
    *,
    batch_number: int,
    documents: list[dict[str, Any]],
    root: Path,
    config: dict[str, Any],
    base: Path,
    toolbox: dict[str, Any],
    options: MicrobatchOptions,
    end_stage: int,
    semaphores: dict[int, threading.BoundedSemaphore],
    clients: dict[str, Any],
) -> dict[str, Any]:
    root.mkdir(parents=True, exist_ok=True)
    state_path = root / "state.json"
    signature = _batch_signature(documents, end_stage)
    if state_path.is_file() and options.resume:
        state = read_json(state_path)
        if state.get("input_signature") != signature:
            raise RuntimeError(
                f"microbatch input changed: {root.name}; set resume=false to replace it"
            )
    else:
        state = {
            "schema_version": 1,
            "batch": batch_number,
            "input_signature": signature,
            "document_ids": [str(item.get("document_id") or "") for item in documents],
            "completed_stages": [],
        }
        write_json(state_path, state)
    completed = {int(item) for item in state.get("completed_stages") or []}
    result: dict[str, Any] = {"batch": batch_number, "root": root}
    current: Any = documents
    try:
        for stage in range(2, end_stage + 1):
            stage_root = root / STAGE_NAMES[stage]
            if stage in completed:
                stage_result = _load_stage_result(stage, stage_root)
            else:
                with semaphores[stage]:
                    pipeline_logger().info(
                        "MICROBATCH STAGE START | batch=%06d | stage=%02d | inputs=%d",
                        batch_number,
                        stage,
                        _input_count(current),
                    )
                    stage_result = _execute_stage(
                        stage,
                        current,
                        stage_root=stage_root,
                        config=config,
                        base=base,
                        toolbox=toolbox,
                        clients=clients,
                    )
                completed.add(stage)
                state.update(
                    {
                        "completed_stages": sorted(completed),
                        "last_completed_stage": stage,
                        "failed_stage": None,
                        "error": None,
                    }
                )
                write_json(state_path, state)
            result[f"stage{stage:02d}"] = stage_result
            current = stage_result
        return result
    except BaseException as exc:
        state.update(
            {
                "completed_stages": sorted(completed),
                "failed_stage": stage,
                "error": f"{type(exc).__name__}: {exc}",
            }
        )
        write_json(state_path, state)
        raise


def _execute_stage(
    stage: int,
    previous: Any,
    *,
    stage_root: Path,
    config: dict[str, Any],
    base: Path,
    toolbox: dict[str, Any],
    clients: dict[str, Any],
) -> Any:
    stage_root.mkdir(parents=True, exist_ok=True)
    if stage == 2:
        grobid_config = config.get("grobid_extract", {})
        records = extract_documents_with_grobid(
            previous,
            clients["grobid"],
            tei_dir=_resolve(base, grobid_config.get("tei_dir", stage_root / "tei")),
            text_dir=_resolve(base, grobid_config.get("text_dir", stage_root / "text")),
            max_chars=grobid_config.get("max_chars", 2_000_000),
            reuse_existing=grobid_config.get("reuse_existing", True),
            exclude_supplementary=bool(
                (config.get("source") or {}).get("exclude_supplementary", True)
            ),
            fallback_config=grobid_config.get("fallback", {}),
            workers=1,
        )
        write_jsonl(stage_root / "documents.jsonl", records)
        return records
    if stage == 3:
        software_config = config.get("software_coverage", {})
        if previous:
            with clients["softcite"].acquire() as client:
                records = assess_software_coverage(
                    previous,
                    client,
                    toolbox,
                    aliases_file=_resolve(base, software_config["aliases_file"]),
                    role_rules_file=_resolve(base, software_config["role_rules_file"]),
                    capability_map_file=_resolve(base, software_config["capability_map_file"]),
                    raw_output_dir=stage_root / "softcite_raw",
                    workers=1,
                )
        else:
            records = []
        write_jsonl(stage_root / "software_coverage_documents.jsonl", records)
        return records
    if stage == 4:
        inputs = [
            item
            for item in previous
            if (item.get("software_coverage") or {}).get("decision") == "direct_covered"
        ]
        if (config.get("stage04") or {}).get("enabled", True) and inputs:
            records = assess_resource_limits(
                inputs,
                clients["quantities"],
                config.get("resource_limits", {}),
                config.get("resource_interpretation", {}),
                output_dir=stage_root,
                workers=1,
            )
        else:
            records = bypass_resource_limits(inputs, config.get("resource_limits", {}))
        write_jsonl(stage_root / "resource_screened_documents.jsonl", records)
        return records
    if stage == 5:
        records = [item for item in previous if (item.get("resource_limits") or {}).get("passed")]
        stage_config = config.get("stage05", {})
        if stage_config.get("enabled", True):
            result = run_asset_collection(
                records, stage_root, stage_config, config.get("mineru", {})
            )
        else:
            result = run_asset_collection(
                records,
                stage_root,
                {
                    **stage_config,
                    "enable_network": False,
                    "max_rounds": 0,
                    "max_clues_per_paper": 0,
                    "include_local_siblings": False,
                    "query_metadata": False,
                },
                {**config.get("mineru", {}), "execute": False},
            )
            result["summary"].update(
                {"skipped": True, "skip_adapter": "primary_pdf_with_stage02_text"}
            )
            write_json(stage_root / "stage_summary.json", result["summary"])
        result["events"] = _read_jsonl_if_exists(stage_root / "asset_events.jsonl")
        return result
    if stage == 6:
        records = _stage04_records(previous, stage_root.parent)
        result = run_builder_stage(
            records, previous, stage_root, config.get("stage06", {}), toolbox
        )
        if any(item.get("status") == "error" for item in result["records"]):
            raise RuntimeError("Stage 06 agent execution failed; inspect the microbatch agent logs")
        return result
    if stage == 7:
        asset_result = _load_stage_result(5, stage_root.parent / STAGE_NAMES[5])
        records = _stage04_records(asset_result, stage_root.parent)
        result = run_judge_stage(
            records,
            asset_result,
            previous,
            stage_root,
            config.get("stage07", {}),
            toolbox,
        )
        if any(item.get("status") == "error" for item in result["records"]):
            raise RuntimeError("Stage 07 agent execution failed; inspect the microbatch agent logs")
        return result
    raise AssertionError(stage)


def _stage04_records(_asset_result: dict[str, Any], batch_root: Path) -> list[dict[str, Any]]:
    return [
        item
        for item in read_jsonl(batch_root / STAGE_NAMES[4] / "resource_screened_documents.jsonl")
        if (item.get("resource_limits") or {}).get("passed")
    ]


def _load_stage_result(stage: int, root: Path) -> Any:
    if stage == 2:
        return read_jsonl(root / "documents.jsonl")
    if stage == 3:
        return read_jsonl(root / "software_coverage_documents.jsonl")
    if stage == 4:
        return read_jsonl(root / "resource_screened_documents.jsonl")
    if stage == 5:
        return {
            "assets": _read_jsonl_if_exists(root / "asset_manifest.jsonl"),
            "clues": _read_jsonl_if_exists(root / "clue_manifest.jsonl"),
            "events": _read_jsonl_if_exists(root / "asset_events.jsonl"),
            "papers": _read_jsonl_if_exists(root / "paper_asset_index.jsonl"),
            "summary": read_json(root / "stage_summary.json"),
        }
    if stage == 6:
        records = read_jsonl(root / "builder_records.jsonl")
        return {"records": records, "summary": read_json(root / "stage_summary.json")}
    if stage == 7:
        records = read_jsonl(root / "judge_records.jsonl")
        return {"records": records, "summary": read_json(root / "stage_summary.json")}
    raise AssertionError(stage)


def _aggregate_outputs(
    *,
    results: list[dict[str, Any]],
    workspace: Path,
    config: dict[str, Any],
    inventory: list[dict[str, Any]],
    duplicate_inventory: list[dict[str, Any]],
    supplementary_inventory: list[dict[str, Any]],
    exclude_supplementary: bool,
    end_stage: int,
) -> dict[str, Any]:
    summaries: dict[str, Any] = {}
    stage02 = _flatten(results, "stage02")
    root = _stage_root(workspace, 2)
    write_jsonl(root / "documents.jsonl", stage02)
    summary02 = {
        **_field_summary(stage02, "grobid_extract_status", "documents"),
        "input_pdf_files": len(inventory),
        "duplicates_excluded": len(duplicate_inventory),
        "supplementary_excluded": len(supplementary_inventory) if exclude_supplementary else 0,
        "grobid_request_attempts": sum(
            bool(item.get("grobid_request_attempted")) for item in stage02
        ),
        "grobid_request_failures": sum(bool(item.get("grobid_request_failed")) for item in stage02),
    }
    attempts = summary02["grobid_request_attempts"]
    summary02["grobid_request_failure_ratio"] = (
        round(summary02["grobid_request_failures"] / attempts, 6) if attempts else 0.0
    )
    _write_summary(root, summary02)
    summaries["stage_02_grobid_extract"] = summary02
    if end_stage == 2:
        return summaries

    stage03 = _flatten(results, "stage03")
    root = _stage_root(workspace, 3)
    write_jsonl(root / "software_coverage_documents.jsonl", stage03)
    write_jsonl(
        root / "direct_covered_pdf_paths.jsonl",
        _pdf_path_rows(
            [
                item
                for item in stage03
                if (item.get("software_coverage") or {}).get("decision") == "direct_covered"
            ]
        ),
    )
    write_jsonl(
        root / "capability_equivalent_pdf_paths.jsonl",
        _pdf_path_rows(
            [
                item
                for item in stage03
                if (item.get("software_coverage") or {}).get("decision") == "capability_equivalent"
            ]
        ),
    )
    summary03 = software_coverage_summary(stage03)
    _write_summary(root, summary03)
    summaries["stage_03_software_coverage"] = summary03
    if end_stage == 3:
        return summaries

    stage04 = _flatten(results, "stage04")
    root = _stage_root(workspace, 4)
    write_jsonl(root / "resource_screened_documents.jsonl", stage04)
    write_jsonl(
        root / "selected_pdf_paths.jsonl",
        _pdf_path_rows(
            [item for item in stage04 if (item.get("resource_limits") or {}).get("passed")]
        ),
    )
    write_jsonl(
        root / "recalled_contexts.jsonl",
        _merge_batch_jsonl(results, 4, "recalled_contexts.jsonl"),
    )
    write_jsonl(
        root / "structured_resource_documents.jsonl",
        _merge_batch_jsonl(results, 4, "structured_resource_documents.jsonl"),
    )
    summary04 = resource_limits_summary(stage04)
    summary04["skipped"] = not (config.get("stage04") or {}).get("enabled", True)
    _write_summary(root, summary04)
    summaries["stage_04_resource_limits"] = summary04
    if end_stage == 4:
        return summaries

    asset_results = [item["stage05"] for item in results]
    assets = _flatten_dict_records(asset_results, "assets")
    clues = _flatten_dict_records(asset_results, "clues")
    events = _flatten_dict_records(asset_results, "events")
    papers = _flatten_dict_records(asset_results, "papers")
    root = _stage_root(workspace, 5)
    write_jsonl(root / "asset_manifest.jsonl", assets)
    write_jsonl(root / "asset_events.jsonl", events)
    write_jsonl(root / "clue_manifest.jsonl", clues)
    write_jsonl(
        root / "unresolved_clues.jsonl",
        [item for item in clues if item.get("status") not in {"resolved", "duplicate"}],
    )
    write_jsonl(root / "paper_asset_index.jsonl", papers)
    _link_batch_directories(results, 5, root / "papers", nested="papers")
    summary05 = {
        "download_scope": (config.get("stage05") or {}).get("download_scope", "all"),
        "papers": len(papers),
        "paper_statuses": value_counts(item.get("status") for item in papers),
        "assets": len(assets),
        "asset_roles": value_counts(item.get("role") for item in assets),
        "access_statuses": value_counts(item.get("access_status") for item in assets),
        "parse_statuses": value_counts(item.get("parse_status") for item in assets),
        "clues": len(clues),
        "clue_statuses": value_counts(item.get("status") for item in clues),
    }
    if not (config.get("stage05") or {}).get("enabled", True):
        summary05.update({"skipped": True, "skip_adapter": "primary_pdf_with_stage02_text"})
    _write_summary(root, summary05)
    summaries["stage_05"] = summary05
    if end_stage == 5:
        return summaries

    builder_records = _flatten_dict_records([item["stage06"] for item in results], "records")
    root = _stage_root(workspace, 6)
    write_jsonl(root / "builder_records.jsonl", builder_records)
    _link_batch_directories(results, 6, root)
    summary06 = {
        "papers": len(builder_records),
        "statuses": value_counts(item.get("status") for item in builder_records),
    }
    _write_summary(root, summary06)
    summaries["stage_06"] = summary06
    if end_stage == 6:
        return summaries

    judge_records = _flatten_dict_records([item["stage07"] for item in results], "records")
    root = _stage_root(workspace, 7)
    write_jsonl(root / "judge_records.jsonl", judge_records)
    _link_batch_directories(results, 7, root)
    summary07 = {
        "tasks": len(judge_records),
        "statuses": value_counts(item.get("status") for item in judge_records),
    }
    _write_summary(root, summary07)
    summaries["stage_07"] = summary07
    return summaries


def _batch_signature(documents: list[dict[str, Any]], _end_stage: int) -> str:
    payload = [
        {
            "document_id": item.get("document_id"),
            "sha256": item.get("sha256"),
            "source_path": item.get("source_path"),
        }
        for item in documents
    ]
    encoded = json.dumps(
        {"schema_version": 1, "documents": payload},
        ensure_ascii=False,
        sort_keys=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _all_batches_complete(batches: list[list[dict[str, Any]]], root: Path, end_stage: int) -> bool:
    required = set(range(2, end_stage + 1))
    for index, documents in enumerate(batches, start=1):
        state_path = root / f"batch_{index:06d}" / "state.json"
        if not state_path.is_file():
            return False
        state = read_json(state_path)
        if state.get("input_signature") != _batch_signature(documents, end_stage):
            return False
        if not required.issubset({int(item) for item in state.get("completed_stages") or []}):
            return False
    return True


def _parse_stage_number(value: Any) -> int:
    text = str(value).casefold().replace("stage", "").replace("_", "").lstrip("0")
    return int(text or "0")


def _input_count(value: Any) -> int:
    if isinstance(value, list):
        return len(value)
    if isinstance(value, dict):
        return len(value.get("records") or value.get("papers") or [])
    return 0


def _resolve(base: Path, value: str | Path) -> Path:
    path = Path(value).expanduser()
    return path.resolve() if path.is_absolute() else (base / path).resolve()


def _load_toolbox(config: dict[str, Any], base: Path) -> dict[str, Any]:
    toolbox = dict(config.get("toolbox", {}))
    return load_toolbox_profile(_resolve(base, toolbox["profile"]), toolbox)


def _read_jsonl_if_exists(path: Path) -> list[dict[str, Any]]:
    return read_jsonl(path) if path.is_file() else []


def _flatten(results: list[dict[str, Any]], key: str) -> list[dict[str, Any]]:
    return [record for result in results for record in result.get(key, [])]


def _flatten_dict_records(results: list[dict[str, Any]], key: str) -> list[dict[str, Any]]:
    return [record for result in results for record in result.get(key, [])]


def _merge_batch_jsonl(
    results: list[dict[str, Any]], stage: int, file_name: str
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for result in results:
        path = Path(result["root"]) / STAGE_NAMES[stage] / file_name
        rows.extend(_read_jsonl_if_exists(path))
    return rows


def _link_batch_directories(
    results: list[dict[str, Any]], stage: int, destination: Path, *, nested: str | None = None
) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    for result in results:
        source = Path(result["root"]) / STAGE_NAMES[stage]
        if nested:
            source /= nested
        if not source.is_dir():
            continue
        for child in source.iterdir():
            if not child.is_dir():
                continue
            target = destination / child.name
            if target.is_symlink():
                if target.resolve() == child.resolve():
                    continue
                target.unlink()
            if not target.exists():
                target.symlink_to(child.resolve(), target_is_directory=True)


def _stage_root(workspace: Path, stage: int) -> Path:
    root = workspace / STAGE_NAMES[stage]
    root.mkdir(parents=True, exist_ok=True)
    return root


def _write_summary(root: Path, summary: dict[str, Any]) -> None:
    write_json(root / "summary.json", summary)
    if root.name in {STAGE_NAMES[5], STAGE_NAMES[6], STAGE_NAMES[7]}:
        write_json(root / "stage_summary.json", summary)
    pipeline_logger().info("STAGE COMPLETE | %s | summary=%s", root.name, summary)


def _field_summary(records: list[dict[str, Any]], field: str, count_label: str) -> dict[str, Any]:
    return {count_label: len(records), field: value_counts(item.get(field) for item in records)}


def _pdf_path_rows(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows = []
    for item in records:
        source_path = item.get("source_path")
        if not source_path:
            continue
        rows.append(
            {
                "document_id": item.get("document_id"),
                "paper_id": item.get("paper_id"),
                "title": item.get("title"),
                "pdf_path": str(Path(source_path).expanduser().resolve()),
                "relative_path": item.get("relative_path"),
            }
        )
    return rows


__all__ = ["MicrobatchOptions", "run_microbatch_stages"]
