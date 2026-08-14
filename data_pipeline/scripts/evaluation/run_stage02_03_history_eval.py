#!/usr/bin/env python3
"""Run the current Stage02/03 contracts against a stratified historical sample."""

from __future__ import annotations

import argparse
import hashlib
import json
import time
from collections import defaultdict
from pathlib import Path
from typing import Any

from src.config import load_config
from src.contracts import read_jsonl, write_json, write_jsonl
from src.model_client import RoleModelClient
from src.stages.stage02_computational_content.stage import run_stage02
from src.stages.stage03_toolbox_resource_gate.stage import run_stage03


def main() -> int:
    args = _parse_args()
    source = args.source_batch.expanduser().resolve()
    output = args.output.expanduser().resolve()
    output.mkdir(parents=True, exist_ok=True)
    config = load_config(args.config)

    old_stage02 = _by_paper(
        read_jsonl(source / "stage_02_computational_content/decisions.jsonl")
    )
    old_stage03 = _by_paper(
        read_jsonl(source / "stage_03_toolbox_resource_gate/decisions.jsonl")
    )
    eligible_ids = {
        paper_id
        for paper_id, row in old_stage02.items()
        if row.get("processing_status") == "completed" and row.get("passed")
    }
    selected_ids = _select_sample(
        old_stage03,
        eligible_ids=eligible_ids,
        sample_size=args.sample_size,
        required=args.include_paper_id,
        seed=args.seed,
    )

    paper_rows = read_jsonl(source / "stage_01_document_preparation/paper_bundles.jsonl")
    selected_id_set = set(selected_ids)
    papers = [
        row
        for row in paper_rows
        if str(row.get("paper_id") or "") in selected_id_set
    ]
    if len(papers) != len(selected_ids):
        resolved = {str(row.get("paper_id") or "") for row in papers}
        raise RuntimeError(
            f"missing Stage01 paper bundles: {sorted(selected_id_set - resolved)}"
        )
    documents = [
        row
        for row in read_jsonl(source / "stage_01_document_preparation/documents.jsonl")
        if str(row.get("paper_id") or "") in selected_id_set
        and row.get("decision") == "pass"
    ]
    _validate_documents(documents, selected_id_set)

    manifest = [
        {
            "paper_id": paper_id,
            "doi": old_stage03[paper_id].get("doi"),
            "old_stage02_decision": old_stage02[paper_id].get("decision"),
            "old_stage03_decision": old_stage03[paper_id].get("decision"),
        }
        for paper_id in selected_ids
    ]
    write_jsonl(output / "selection.jsonl", manifest)

    stage02_config = dict(config["stage02"])
    stage03_config = dict(config["stage03"])
    stage02_config["workers"] = args.workers
    stage03_config["workers"] = args.workers
    stage02_model = _model_client(config, stage02_config["model_role"], output)
    stage03_model = _model_client(config, stage03_config["model_role"], output)

    if args.reuse_stage02_output:
        reused_root = args.reuse_stage02_output.expanduser().resolve()
        stage02_records = read_jsonl(reused_root / "decisions.jsonl")
        resolved_ids = {str(row.get("paper_id") or "") for row in stage02_records}
        if resolved_ids != selected_id_set:
            raise RuntimeError(
                "reused Stage02 paper IDs do not match the selected historical sample"
            )
        stage02_result = {
            "records": stage02_records,
            "summary": json.loads(
                (reused_root / "stage_summary.json").read_text(encoding="utf-8")
            ),
        }
        stage02_elapsed = 0.0
    else:
        started = time.monotonic()
        stage02_result = run_stage02(
            papers=papers,
            documents=documents,
            config=stage02_config,
            model=stage02_model,
            workspace=output / "model_run",
            run_id=args.run_id,
        )
        stage02_elapsed = time.monotonic() - started

    started = time.monotonic()
    stage03_result = run_stage03(
        stage02_records=stage02_result["records"],
        documents=documents,
        config=stage03_config,
        model=stage03_model,
        workspace=output / "model_run",
        run_id=args.run_id,
    )
    stage03_elapsed = time.monotonic() - started

    new_stage02 = _by_paper(stage02_result["records"])
    new_stage03 = _by_paper(stage03_result["records"])
    comparisons = []
    for paper_id in selected_ids:
        stage02_row = new_stage02.get(paper_id) or {}
        stage03_row = new_stage03.get(paper_id) or {}
        comparisons.append(
            {
                "paper_id": paper_id,
                "doi": old_stage03[paper_id].get("doi"),
                "old_stage02_decision": old_stage02[paper_id].get("decision"),
                "new_stage02_decision": stage02_row.get("decision"),
                "confirmed_workflow_count": len(
                    stage02_row.get("confirmed_workflows") or []
                ),
                "old_stage03_decision": old_stage03[paper_id].get("decision"),
                "new_stage03_decision": stage03_row.get("decision"),
                "new_stage03_passed": stage03_row.get("passed"),
                "workflow_coverage_results": stage03_row.get(
                    "workflow_coverage_results"
                )
                or [],
                "software_mappings": stage03_row.get("software_mappings") or [],
                "stage02_processing_status": stage02_row.get("processing_status"),
                "stage03_processing_status": stage03_row.get("processing_status"),
            }
        )
    write_jsonl(output / "comparison.jsonl", comparisons)
    summary = {
        "run_id": args.run_id,
        "source_batch": str(source),
        "sample_size": len(selected_ids),
        "stage02_elapsed_seconds": round(stage02_elapsed, 3),
        "stage03_elapsed_seconds": round(stage03_elapsed, 3),
        "stage02": stage02_result["summary"],
        "stage03": stage03_result["summary"],
    }
    write_json(output / "summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


def _model_client(config: dict[str, Any], role: str, output: Path) -> RoleModelClient:
    return RoleModelClient(
        role=role,
        config=config["models"][role],
        cache_root=output / "llm_cache",
    )


def _select_sample(
    old_stage03: dict[str, dict[str, Any]],
    *,
    eligible_ids: set[str],
    sample_size: int,
    required: list[str],
    seed: str,
) -> list[str]:
    missing = set(required) - eligible_ids
    if missing:
        raise ValueError(f"required paper IDs are not eligible: {sorted(missing)}")
    selected = list(dict.fromkeys(required))
    selected_set = set(selected)
    buckets: dict[str, list[str]] = defaultdict(list)
    for paper_id, row in old_stage03.items():
        if paper_id in eligible_ids and paper_id not in selected_set:
            buckets[str(row.get("decision") or "unknown")].append(paper_id)
    for values in buckets.values():
        values.sort(key=lambda value: _stable_key(seed, value))
    labels = sorted(buckets)
    while len(selected) < sample_size and any(buckets.values()):
        for label in labels:
            if buckets[label] and len(selected) < sample_size:
                paper_id = buckets[label].pop(0)
                selected.append(paper_id)
                selected_set.add(paper_id)
    if len(selected) != sample_size:
        raise ValueError(f"could only select {len(selected)} of {sample_size} papers")
    return selected


def _stable_key(seed: str, value: str) -> str:
    return hashlib.sha256(f"{seed}:{value}".encode()).hexdigest()


def _validate_documents(documents: list[dict[str, Any]], paper_ids: set[str]) -> None:
    by_paper: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in documents:
        by_paper[str(row["paper_id"])].append(row)
        path = Path(str(row["content_blocks_path"])).expanduser()
        if not path.is_file():
            raise RuntimeError(f"missing frozen content blocks: {path}")
    missing = paper_ids - set(by_paper)
    if missing:
        raise RuntimeError(f"selected papers have no parsed documents: {sorted(missing)}")


def _by_paper(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {str(row["paper_id"]): row for row in rows}


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path("config.example.json"))
    parser.add_argument("--source-batch", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--run-id", default="stage02-03-redesign-history-eval")
    parser.add_argument("--sample-size", type=int, default=16)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--seed", default="20260814")
    parser.add_argument("--include-paper-id", action="append", default=[])
    parser.add_argument(
        "--reuse-stage02-output",
        type=Path,
        help="Existing stage_02_computational_content directory for the same sample.",
    )
    return parser.parse_args()


if __name__ == "__main__":
    raise SystemExit(main())
