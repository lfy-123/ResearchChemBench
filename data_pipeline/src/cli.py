from __future__ import annotations

import argparse
import json

from src.core.io import read_jsonl, write_json, write_jsonl
from src.ingestion.corpus import inventory_corpus
from src.ingestion.deep_parse import build_mineru_queue, run_mineru_queue
from src.ingestion.grobid import GrobidClient, extract_documents_with_grobid
from src.orchestration.pipeline import run_late_stages, run_pipeline


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="chem-pipeline")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run the configured seven-stage pipeline")
    run_parser.add_argument("--config", default="config.json")
    run_parser.add_argument("--output")

    late_parser = subparsers.add_parser(
        "run-late-stages", help="Run Stage 05-07 from an existing Stage 04 JSONL"
    )
    late_parser.add_argument("--input", required=True)
    late_parser.add_argument("--config", default="config.json")
    late_parser.add_argument("--workspace", required=True)
    late_parser.add_argument("--output")

    inventory_parser = subparsers.add_parser(
        "corpus-inventory", help="Inventory and hash a PDF corpus"
    )
    inventory_parser.add_argument("--root", required=True)
    inventory_parser.add_argument("--output", required=True)

    extract_parser = subparsers.add_parser(
        "corpus-extract", help="Extract structured PDF metadata and text with GROBID"
    )
    extract_parser.add_argument("--inventory", required=True)
    extract_parser.add_argument("--tei-dir", required=True)
    extract_parser.add_argument("--text-dir", required=True)
    extract_parser.add_argument("--output", required=True)
    extract_parser.add_argument("--grobid-url", default="http://127.0.0.1:8070")
    extract_parser.add_argument("--timeout-seconds", type=int, default=900)
    extract_parser.add_argument("--max-chars", type=int, default=2_000_000)
    extract_parser.add_argument("--include-supplementary", action="store_true")

    mineru_parser = subparsers.add_parser(
        "mineru-queue", help="Build or execute a standalone MinerU queue"
    )
    mineru_parser.add_argument("--input", required=True)
    mineru_parser.add_argument("--queue-output", required=True)
    mineru_parser.add_argument("--result-output", required=True)
    mineru_parser.add_argument("--mineru-output", required=True)
    mineru_parser.add_argument("--limit", type=int)
    mineru_parser.add_argument("--execute", action="store_true")
    mineru_parser.add_argument("--command", default="mineru")
    mineru_parser.add_argument("--method", default="auto")
    mineru_parser.add_argument("--backend")
    mineru_parser.add_argument("--force", action="store_true")
    args = parser.parse_args(argv)

    if args.command == "run":
        result = run_pipeline(args.config)
        if args.output:
            write_json(args.output, result)
    elif args.command == "run-late-stages":
        result = run_late_stages(args.input, args.config, args.workspace)
        if args.output:
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
        result = {"documents": len(rows), "output": args.output}
    elif args.command == "mineru-queue":
        queue = build_mineru_queue(read_jsonl(args.input), limit=args.limit)
        write_jsonl(args.queue_output, queue)
        rows = run_mineru_queue(
            queue,
            args.mineru_output,
            execute=args.execute,
            command=args.command,
            method=args.method,
            backend=args.backend,
            reuse_existing=not args.force,
        )
        write_jsonl(args.result_output, rows)
        result = {"queued": len(queue), "results": len(rows)}
    else:
        raise AssertionError(args.command)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
