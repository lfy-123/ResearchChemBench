from __future__ import annotations

import hashlib
import json
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from src.core.io import read_json, read_jsonl, write_json, write_jsonl
from src.core.logging import pipeline_logger
from src.stages.stage02_parsing import build_paper_text_bundles, extract_documents_with_grobid
from src.stages.stage03_computation_relevance import (
    assess_computation_relevance,
    computation_relevance_summary,
)
from src.stages.stage04_supplementary_acquisition import (
    acquire_supplementary_materials,
    supplementary_acquisition_summary,
)
from src.stages.stage05_preliminary_coverage import (
    assess_preliminary_coverage,
    preliminary_coverage_summary,
)
from src.stages.stage06_supplementary_extraction import (
    extract_supplementary_materials,
    supplementary_extraction_summary,
)

STAGE_NAMES = {
    2: "stage_02_grobid_extract",
    3: "stage_03_computation_relevance",
    4: "stage_04_supplementary_acquisition",
    5: "stage_05_preliminary_coverage",
    6: "stage_06_supplementary_extraction",
}


@dataclass(frozen=True)
class ScreeningMicrobatchOptions:
    size: int
    concurrency: int
    resume: bool
    stage_limits: dict[int, int]

    @classmethod
    def from_config(cls, config: dict[str, Any], end_stage: int) -> ScreeningMicrobatchOptions:
        raw = config.get("microbatch") or {}
        size = max(1, int(raw.get("size", 10)))
        concurrency = max(1, int(raw.get("concurrency", 5)))
        limits = {
            stage: min(
                concurrency,
                max(1, int((raw.get("stage_limits") or {}).get(str(stage), concurrency))),
            )
            for stage in range(2, end_stage + 1)
        }
        return cls(
            size=size,
            concurrency=concurrency,
            resume=bool(raw.get("resume", True)),
            stage_limits=limits,
        )


def run_screening_microbatches(
    *,
    config: dict[str, Any],
    base: Path,
    workspace: Path,
    canonical_inventory: list[dict[str, Any]],
    end_stage: int,
    grobid_client: Any,
    softcite_client: Any | None,
    toolbox_profile: dict[str, Any] | None,
    store_factory: Callable[[list[dict[str, Any]]], Any],
) -> dict[str, Any]:
    if end_stage < 2 or end_stage > 6:
        raise ValueError("redesigned microbatch execution currently supports Stage 02-06")
    options = ScreeningMicrobatchOptions.from_config(config, end_stage)
    batches = _paper_batches(canonical_inventory, options.size)
    root = workspace / "microbatches"
    root.mkdir(parents=True, exist_ok=True)
    write_json(
        root / "run_config.json",
        {
            "schema_version": 2,
            "pipeline": "redesigned_stage00_08",
            "size": options.size,
            "concurrency": options.concurrency,
            "stage_limits": {str(key): value for key, value in options.stage_limits.items()},
            "end_stage": end_stage,
            "batches": len(batches),
            "documents": len(canonical_inventory),
        },
    )
    semaphores = {
        stage: threading.BoundedSemaphore(limit) for stage, limit in options.stage_limits.items()
    }
    pipeline_logger().info(
        "REDESIGNED MICROBATCH START | papers=%d | batches=%d | size=%d | concurrency=%d",
        len({str(item["paper_id"]) for item in canonical_inventory}),
        len(batches),
        options.size,
        options.concurrency,
    )

    def run_batch(batch_number: int, documents: list[dict[str, Any]]) -> dict[str, Any]:
        batch_root = root / f"batch_{batch_number:06d}"
        batch_root.mkdir(parents=True, exist_ok=True)
        state_path = batch_root / "state.json"
        signature = _signature(documents)
        if state_path.is_file() and options.resume:
            state = read_json(state_path)
            if state.get("input_signature") != signature:
                raise RuntimeError(f"microbatch input changed: {batch_root.name}")
        else:
            state = {
                "schema_version": 2,
                "batch": batch_number,
                "input_signature": signature,
                "paper_ids": list(dict.fromkeys(str(item["paper_id"]) for item in documents)),
                "completed_stages": [],
            }
            write_json(state_path, state)
        completed = {int(item) for item in state.get("completed_stages") or []}
        result: dict[str, Any] = {"batch": batch_number, "root": str(batch_root)}
        current: dict[str, Any] = {"inventory": documents}
        for stage in range(2, end_stage + 1):
            stage_root = batch_root / STAGE_NAMES[stage]
            if stage in completed:
                current = _load_stage(stage, stage_root, current)
            else:
                try:
                    with semaphores[stage]:
                        pipeline_logger().info(
                            "MICROBATCH STAGE START | batch=%06d | stage=%02d | papers=%d",
                            batch_number,
                            stage,
                            len({str(item["paper_id"]) for item in documents}),
                        )
                        current = _execute_stage(
                            stage,
                            current,
                            root=stage_root,
                            config=config,
                            base=base,
                            grobid_client=grobid_client,
                            softcite_client=softcite_client,
                            toolbox_profile=toolbox_profile,
                            store_factory=store_factory,
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
            result[f"stage{stage:02d}"] = current
        return result

    ordered: list[dict[str, Any] | None] = [None] * len(batches)
    failures: list[tuple[int, BaseException]] = []
    with ThreadPoolExecutor(
        max_workers=min(options.concurrency, max(1, len(batches))),
        thread_name_prefix="redesigned-microbatch",
    ) as executor:
        futures = {
            executor.submit(run_batch, index, documents): index
            for index, documents in enumerate(batches, start=1)
        }
        for future in as_completed(futures):
            index = futures[future]
            try:
                ordered[index - 1] = future.result()
            except BaseException as exc:
                failures.append((index, exc))
                pipeline_logger().exception("MICROBATCH FAILED | batch=%06d", index)
    if failures:
        details = "; ".join(
            f"batch_{index:06d}: {type(exc).__name__}: {exc}" for index, exc in failures
        )
        raise RuntimeError(f"{len(failures)} redesigned microbatch(es) failed: {details}")
    results = [item for item in ordered if item is not None]
    aggregated = _aggregate(results, workspace, end_stage)
    aggregated["microbatch"] = {
        "size": options.size,
        "concurrency": options.concurrency,
        "stage_limits": {str(key): value for key, value in options.stage_limits.items()},
        "batches": len(batches),
    }
    return aggregated


def _execute_stage(
    stage: int,
    current: dict[str, Any],
    *,
    root: Path,
    config: dict[str, Any],
    base: Path,
    grobid_client: Any,
    softcite_client: Any | None,
    toolbox_profile: dict[str, Any] | None,
    store_factory: Callable[[list[dict[str, Any]]], Any],
) -> dict[str, Any]:
    root.mkdir(parents=True, exist_ok=True)
    if stage == 2:
        stage_config = config.get("grobid_extract") or {}
        documents = extract_documents_with_grobid(
            current["inventory"],
            grobid_client,
            tei_dir=root / "tei",
            text_dir=root / "text",
            max_chars=stage_config.get("max_chars", 2_000_000),
            reuse_existing=stage_config.get("reuse_existing", True),
            exclude_supplementary=False,
            fallback_config={
                **(stage_config.get("fallback") or {}),
                "output_dir": str(root / "fallback"),
            },
            workers=int(stage_config.get("workers", 1)),
        )
        bundles = build_paper_text_bundles(documents)
        write_jsonl(root / "documents.jsonl", documents)
        write_jsonl(root / "paper_text_bundles.jsonl", bundles)
        return {**current, "documents": documents, "bundles": bundles}
    if stage == 3:
        stage_config = config.get("stage03_computation_relevance") or {}
        records = assess_computation_relevance(
            current["bundles"],
            method_ontology=stage_config["method_ontology"],
            evidence_rules=stage_config["evidence_rules"],
            negative_contexts=stage_config["negative_contexts"],
            workers=int(stage_config.get("workers", 1)),
            llm_config={
                **(stage_config.get("llm") or {}),
                "enabled": bool(stage_config.get("use_llm"))
                and bool((stage_config.get("llm") or {}).get("enabled")),
            },
            llm_cache_dir=(stage_config.get("llm") or {}).get(
                "cache_directory", root / "llm_cache"
            ),
        )
        write_jsonl(root / "decisions.jsonl", records)
        return {**current, "relevance": records}
    if stage == 4:
        candidates = [
            item
            for item in current["relevance"]
            if (item.get("pipeline_routing") or {}).get("continue")
        ]
        records = acquire_supplementary_materials(
            candidates,
            root,
            config.get("stage04_supplementary_acquisition") or {},
            store=store_factory(candidates),
        )
        write_jsonl(root / "supplementary_manifest.jsonl", records)
        return {**current, "acquisition": records}
    if stage == 5:
        if softcite_client is None or toolbox_profile is None:
            raise RuntimeError("Stage 05 microbatch clients are not initialized")
        stage_config = config.get("stage05_preliminary_coverage") or {}
        software_config = config.get("software_coverage") or {}
        records = assess_preliminary_coverage(
            current["acquisition"],
            current["documents"],
            softcite_client,
            toolbox_profile,
            capability_catalog=stage_config["capability_catalog"],
            aliases_file=software_config["aliases_file"],
            role_rules_file=software_config["role_rules_file"],
            capability_map_file=software_config["capability_map_file"],
            raw_output_dir=root / "softcite_raw",
            workers=int(software_config.get("workers", 1)),
        )
        write_jsonl(root / "decisions.jsonl", records)
        return {**current, "coverage": records}
    if stage == 6:
        records = extract_supplementary_materials(
            [
                item
                for item in current["coverage"]
                if (item.get("pipeline_routing") or {}).get("continue")
            ],
            root,
            {
                **(config.get("stage06_supplementary_extraction") or {}),
                "mineru": config.get("mineru") or {},
            },
            grobid_client=grobid_client,
        )
        write_jsonl(root / "supplementary_evidence_bundles.jsonl", records)
        return {**current, "supplementary_extraction": records}
    raise AssertionError(stage)


def _load_stage(stage: int, root: Path, current: dict[str, Any]) -> dict[str, Any]:
    if stage == 2:
        return {
            **current,
            "documents": read_jsonl(root / "documents.jsonl"),
            "bundles": read_jsonl(root / "paper_text_bundles.jsonl"),
        }
    key, filename = {
        3: ("relevance", "decisions.jsonl"),
        4: ("acquisition", "supplementary_manifest.jsonl"),
        5: ("coverage", "decisions.jsonl"),
        6: ("supplementary_extraction", "supplementary_evidence_bundles.jsonl"),
    }[stage]
    return {**current, key: read_jsonl(root / filename)}


def _aggregate(
    results: list[dict[str, Any]], workspace: Path, end_stage: int
) -> dict[str, Any]:
    output: dict[str, Any] = {}
    stage02_states = [item["stage02"] for item in results]
    documents = [row for state in stage02_states for row in state["documents"]]
    bundles = [row for state in stage02_states for row in state["bundles"]]
    root = workspace / STAGE_NAMES[2]
    root.mkdir(parents=True, exist_ok=True)
    write_jsonl(root / "documents.jsonl", documents)
    write_jsonl(root / "paper_text_bundles.jsonl", bundles)
    attempts = sum(bool(item.get("grobid_request_attempted")) for item in documents)
    failures = sum(bool(item.get("grobid_request_failed")) for item in documents)
    summary02 = {
        "documents": len(documents),
        "papers": len(bundles),
        "grobid_extract_status": _counts(item.get("grobid_extract_status") for item in documents),
        "grobid_request_attempts": attempts,
        "grobid_request_failures": failures,
        "grobid_request_failure_ratio": round(failures / attempts, 6) if attempts else 0.0,
    }
    write_json(root / "summary.json", summary02)
    output["stage02"] = summary02
    if end_stage == 2:
        return output

    relevance = [row for item in results for row in item["stage03"]["relevance"]]
    root = workspace / STAGE_NAMES[3]
    root.mkdir(parents=True, exist_ok=True)
    write_jsonl(root / "decisions.jsonl", relevance)
    write_jsonl(
        root / "evidence_spans.jsonl",
        [
            evidence
            for item in relevance
            for evidence in (item.get("computation_relevance") or {}).get("evidence", [])
        ],
    )
    for decision, filename in (
        ("strong_candidate", "strong_candidates.jsonl"),
        ("weak_candidate", "weak_candidates.jsonl"),
        ("not_computational", "rejected.jsonl"),
    ):
        write_jsonl(
            root / filename,
            [
                item
                for item in relevance
                if (item.get("computation_relevance") or {}).get("decision") == decision
            ],
        )
    summary03 = computation_relevance_summary(relevance)
    write_json(root / "summary.json", summary03)
    output["stage03"] = summary03
    if end_stage == 3:
        return output

    acquisition = [row for item in results for row in item["stage04"]["acquisition"]]
    root = workspace / STAGE_NAMES[4]
    root.mkdir(parents=True, exist_ok=True)
    write_jsonl(root / "supplementary_manifest.jsonl", acquisition)
    write_jsonl(
        root / "discovery_attempts.jsonl",
        [
            {"paper_id": item.get("paper_id"), **attempt}
            for item in acquisition
            for attempt in (item.get("supplementary_acquisition") or {}).get("attempts", [])
        ],
    )
    summary04 = supplementary_acquisition_summary(acquisition)
    write_json(root / "summary.json", summary04)
    output["stage04"] = summary04
    if end_stage == 4:
        return output

    coverage = [row for item in results for row in item["stage05"]["coverage"]]
    root = workspace / STAGE_NAMES[5]
    root.mkdir(parents=True, exist_ok=True)
    write_jsonl(root / "decisions.jsonl", coverage)
    summary05 = preliminary_coverage_summary(coverage)
    write_json(root / "summary.json", summary05)
    output["stage05"] = summary05
    if end_stage == 5:
        return output

    extraction = [
        row for item in results for row in item["stage06"]["supplementary_extraction"]
    ]
    root = workspace / STAGE_NAMES[6]
    root.mkdir(parents=True, exist_ok=True)
    write_jsonl(root / "supplementary_evidence_bundles.jsonl", extraction)
    write_jsonl(
        root / "documents.jsonl",
        [
            document
            for item in extraction
            for document in (item.get("supplementary_extraction") or {}).get("documents", [])
        ],
    )
    write_jsonl(
        root / "extraction_errors.jsonl",
        [
            error
            for item in extraction
            for error in (item.get("supplementary_extraction") or {}).get("errors", [])
        ],
    )
    summary06 = supplementary_extraction_summary(extraction)
    write_json(root / "summary.json", summary06)
    output["stage06"] = summary06
    return output


def _paper_batches(
    documents: list[dict[str, Any]], size: int
) -> list[list[dict[str, Any]]]:
    order = list(dict.fromkeys(str(item["paper_id"]) for item in documents))
    grouped: dict[str, list[dict[str, Any]]] = {paper_id: [] for paper_id in order}
    for document in documents:
        grouped[str(document["paper_id"])].append(document)
    return [
        [document for paper_id in order[index : index + size] for document in grouped[paper_id]]
        for index in range(0, len(order), size)
    ]


def _signature(documents: list[dict[str, Any]]) -> str:
    payload = [
        {
            "document_id": item.get("document_id"),
            "sha256": item.get("sha256"),
            "source_path": item.get("source_path"),
        }
        for item in documents
    ]
    return hashlib.sha256(
        json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
    ).hexdigest()


def _counts(values: Any) -> dict[str, int]:
    output: dict[str, int] = {}
    for value in values:
        key = "unknown" if value is None else str(value)
        output[key] = output.get(key, 0) + 1
    return output


__all__ = ["ScreeningMicrobatchOptions", "run_screening_microbatches"]
