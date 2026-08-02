from __future__ import annotations

import argparse
import json

from src.core.io import read_json, read_jsonl, write_json, write_jsonl
from src.curation.extract import extract_records
from src.curation.task_selection import select_task_types, selection_summary
from src.delivery.agent_pilot import run_agent_pilot
from src.delivery.build import build_dataset
from src.delivery.reference_run import execute_reference_run
from src.delivery.smoke import run_mock_task
from src.delivery.validate import validate_dataset
from src.discovery.corpus_classify import (
    classification_summary,
    classify_corpus_documents,
)
from src.discovery.query import expand_seeds
from src.discovery.screen import screen_papers
from src.discovery.search import search_offline, search_openalex
from src.discovery.seed_audit import audit_seed_coverage
from src.ingestion.corpus import inventory_corpus
from src.ingestion.dedupe import deduplicate
from src.ingestion.deep_parse import build_mineru_queue, run_mineru_queue
from src.ingestion.grobid import GrobidClient, extract_documents_with_grobid
from src.orchestration.pipeline import run_pipeline


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="chem-pipeline")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run the configured end-to-end pipeline")
    run_parser.add_argument("--config", default="config.json")
    run_parser.add_argument("--output", help="Optional path for the compact run summary")

    expand_parser = subparsers.add_parser(
        "expand", help="Expand seed tasks into three-tier queries"
    )
    expand_parser.add_argument("--seeds", required=True)
    expand_parser.add_argument("--output", required=True)
    expand_parser.add_argument("--max-per-tier", type=int, default=12)

    search_parser = subparsers.add_parser("search", help="Retrieve candidate papers")
    search_parser.add_argument("--queries", required=True)
    search_parser.add_argument("--output", required=True)
    search_parser.add_argument("--provider", choices=("offline", "openalex"), default="offline")
    search_parser.add_argument("--candidates")
    search_parser.add_argument("--per-query", type=int, default=20)
    search_parser.add_argument("--mailto")

    dedupe_parser = subparsers.add_parser("dedupe", help="Merge duplicate retrieval records")
    dedupe_parser.add_argument("--input", required=True)
    dedupe_parser.add_argument("--output", required=True)

    screen_parser = subparsers.add_parser("screen", help="Run metadata-level paper screening")
    screen_parser.add_argument("--input", required=True)
    screen_parser.add_argument("--seeds", required=True)
    screen_parser.add_argument("--output", required=True)
    screen_parser.add_argument("--threshold", type=float, default=35.0)

    extract_parser = subparsers.add_parser("extract", help="Build ScientificRecords")
    extract_parser.add_argument("--input", required=True)
    extract_parser.add_argument("--assets")
    extract_parser.add_argument("--output", required=True)
    extract_parser.add_argument("--include-review", action="store_true")

    select_parser = subparsers.add_parser(
        "task-select", help="Select exactly one task type for each ScientificRecord"
    )
    select_parser.add_argument("--input", required=True)
    select_parser.add_argument("--output", required=True)
    select_parser.add_argument("--config")
    select_parser.add_argument("--summary")

    build_parser = subparsers.add_parser(
        "build", help="Build complete ResearchChemBench-native staged task packages"
    )
    build_parser.add_argument("--records", required=True)
    build_parser.add_argument("--output", required=True)
    build_parser.add_argument("--allow-failed-quality", action="store_true")

    validate_parser = subparsers.add_parser("validate", help="Validate a generated dataset")
    validate_parser.add_argument("--dataset", required=True)
    validate_parser.add_argument("--output")

    smoke_parser = subparsers.add_parser(
        "smoke-run", help="Run ResearchChemBench's real mock agent on one staged task"
    )
    smoke_parser.add_argument("--task-dir", required=True)
    smoke_parser.add_argument("--workspace-root", required=True)
    smoke_parser.add_argument("--benchmark-root")
    smoke_parser.add_argument("--output")

    pilot_parser = subparsers.add_parser(
        "agent-pilot", help="Run configured solver agents on one staged task before human review"
    )
    pilot_parser.add_argument("--task-dir", required=True)
    pilot_parser.add_argument("--workspace-root", required=True)
    pilot_parser.add_argument("--config", required=True)
    pilot_parser.add_argument("--benchmark-root")
    pilot_parser.add_argument("--output", required=True)

    reference_parser = subparsers.add_parser(
        "reference-run", help="Execute and verify one explicit reference-run specification"
    )
    reference_parser.add_argument("--spec", required=True)
    reference_parser.add_argument("--output", required=True)

    inventory_parser = subparsers.add_parser(
        "corpus-inventory", help="Inventory and hash a PDF corpus"
    )
    inventory_parser.add_argument("--root", required=True)
    inventory_parser.add_argument("--output", required=True)

    extract_corpus_parser = subparsers.add_parser(
        "corpus-extract", help="Extract structured PDF metadata and text with GROBID"
    )
    extract_corpus_parser.add_argument("--inventory", required=True)
    extract_corpus_parser.add_argument("--tei-dir", required=True)
    extract_corpus_parser.add_argument("--text-dir", required=True)
    extract_corpus_parser.add_argument("--output", required=True)
    extract_corpus_parser.add_argument("--grobid-url", default="http://127.0.0.1:8070")
    extract_corpus_parser.add_argument("--timeout-seconds", type=int, default=900)
    extract_corpus_parser.add_argument("--max-chars", type=int, default=2_000_000)
    extract_corpus_parser.add_argument("--include-supplementary", action="store_true")

    classify_parser = subparsers.add_parser(
        "corpus-classify", help="Classify computational chemistry relevance and task potential"
    )
    classify_parser.add_argument("--input", required=True)
    classify_parser.add_argument("--output", required=True)
    classify_parser.add_argument("--summary")
    classify_parser.add_argument("--relevance-pass", type=float, default=45.0)
    classify_parser.add_argument("--relevance-review", type=float, default=22.0)
    classify_parser.add_argument("--constructability-threshold", type=float, default=55.0)

    seed_parser = subparsers.add_parser(
        "seed-audit", help="Map corpus papers to seed capability anchors"
    )
    seed_parser.add_argument("--input", required=True)
    seed_parser.add_argument("--seeds", required=True)
    seed_parser.add_argument("--output", required=True)
    seed_parser.add_argument("--summary", required=True)
    seed_parser.add_argument("--match-threshold", type=float, default=0.12)

    mineru_parser = subparsers.add_parser(
        "mineru-queue", help="Build or execute the shortlisted MinerU queue"
    )
    mineru_parser.add_argument("--input", required=True)
    mineru_parser.add_argument("--queue-output", required=True)
    mineru_parser.add_argument("--result-output", required=True)
    mineru_parser.add_argument("--mineru-output", required=True)
    mineru_parser.add_argument("--include-optional", action="store_true")
    mineru_parser.add_argument("--limit", type=int)
    mineru_parser.add_argument("--execute", action="store_true")
    mineru_parser.add_argument("--command", default="mineru")
    mineru_parser.add_argument("--method", default="auto")
    mineru_parser.add_argument("--backend")
    mineru_parser.add_argument("--force", action="store_true")
    mineru_parser.add_argument("--min-markdown-chars", type=int, default=1000)

    args = parser.parse_args(argv)
    if args.command == "run":
        result = run_pipeline(args.config)
        if args.output:
            write_json(args.output, result)
    elif args.command == "expand":
        result = expand_seeds(read_json(args.seeds), args.max_per_tier)
        write_jsonl(args.output, result)
        result = {"queries": len(result), "output": args.output}
    elif args.command == "search":
        queries = read_jsonl(args.queries)
        if args.provider == "offline":
            if not args.candidates:
                parser.error("--candidates is required for offline search")
            result_rows = search_offline(
                queries, read_json(args.candidates), per_query=args.per_query
            )
        else:
            result_rows = search_openalex(queries, per_query=args.per_query, mailto=args.mailto)
        write_jsonl(args.output, result_rows)
        result = {"retrieved_rows": len(result_rows), "output": args.output}
    elif args.command == "dedupe":
        rows = deduplicate(read_jsonl(args.input))
        write_jsonl(args.output, rows)
        result = {"unique_papers": len(rows), "output": args.output}
    elif args.command == "screen":
        rows = screen_papers(read_jsonl(args.input), read_json(args.seeds), args.threshold)
        write_jsonl(args.output, rows)
        result = {"screened_papers": len(rows), "output": args.output}
    elif args.command == "extract":
        assets = read_json(args.assets) if args.assets else []
        rows = extract_records(read_jsonl(args.input), assets, args.include_review)
        write_jsonl(args.output, rows)
        result = {"scientific_records": len(rows), "output": args.output}
    elif args.command == "task-select":
        selection_config = read_json(args.config) if args.config else {}
        rows = select_task_types(read_jsonl(args.input), selection_config)
        write_jsonl(args.output, rows)
        result = selection_summary(rows)
        if args.summary:
            write_json(args.summary, result)
    elif args.command == "build":
        result = build_dataset(read_jsonl(args.records), args.output, args.allow_failed_quality)
    elif args.command == "validate":
        result = validate_dataset(args.dataset)
        if args.output:
            write_json(args.output, result)
    elif args.command == "smoke-run":
        result = run_mock_task(
            args.task_dir,
            args.workspace_root,
            benchmark_root=args.benchmark_root,
        )
        if args.output:
            write_json(args.output, result)
    elif args.command == "agent-pilot":
        result = run_agent_pilot(
            args.task_dir,
            args.workspace_root,
            read_json(args.config),
            benchmark_root=args.benchmark_root,
        )
        write_json(args.output, result)
    elif args.command == "reference-run":
        result = execute_reference_run(read_json(args.spec))
        write_json(args.output, result)
    elif args.command == "corpus-inventory":
        rows = inventory_corpus(args.root)
        write_jsonl(args.output, rows)
        result = {
            "pdf_files": len(rows),
            "canonical_pdfs": sum(1 for row in rows if not row.get("duplicate_of")),
            "output": args.output,
        }
    elif args.command == "corpus-extract":
        rows = extract_documents_with_grobid(
            read_jsonl(args.inventory),
            GrobidClient(base_url=args.grobid_url, timeout_seconds=args.timeout_seconds),
            args.tei_dir,
            args.text_dir,
            max_chars=args.max_chars,
            exclude_supplementary=not args.include_supplementary,
        )
        write_jsonl(args.output, rows)
        result = {
            "documents": len(rows),
            "successful": sum(
                1 for row in rows if row.get("grobid_extract_status") in {"success", "reused"}
            ),
            "needs_ocr": sum(1 for row in rows if (row.get("text_quality") or {}).get("needs_ocr")),
            "output": args.output,
        }
    elif args.command == "corpus-classify":
        rows = classify_corpus_documents(
            read_jsonl(args.input),
            relevance_pass=args.relevance_pass,
            relevance_review=args.relevance_review,
            constructability_threshold=args.constructability_threshold,
        )
        write_jsonl(args.output, rows)
        summary = classification_summary(rows)
        if args.summary:
            write_json(args.summary, summary)
        result = {**summary, "output": args.output}
    elif args.command == "seed-audit":
        rows, summary = audit_seed_coverage(
            read_jsonl(args.input), read_json(args.seeds), args.match_threshold
        )
        write_jsonl(args.output, rows)
        write_json(args.summary, summary)
        result = summary
    elif args.command == "mineru-queue":
        queue = build_mineru_queue(read_jsonl(args.input), args.include_optional, args.limit)
        write_jsonl(args.queue_output, queue)
        rows = run_mineru_queue(
            queue,
            args.mineru_output,
            execute=args.execute,
            command=args.command,
            method=args.method,
            backend=args.backend,
            reuse_existing=not args.force,
            min_markdown_chars=args.min_markdown_chars,
        )
        write_jsonl(args.result_output, rows)
        result = {
            "queued": len(queue),
            "executed": sum(1 for row in rows if row.get("status") == "success"),
            "reused": sum(1 for row in rows if row.get("status") == "reused"),
            "unavailable": sum(1 for row in rows if row.get("status") == "unavailable"),
            "queue_output": args.queue_output,
            "result_output": args.result_output,
        }
    else:
        raise AssertionError(args.command)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not isinstance(result, dict) or result.get("passed", True) else 1


if __name__ == "__main__":
    raise SystemExit(main())
