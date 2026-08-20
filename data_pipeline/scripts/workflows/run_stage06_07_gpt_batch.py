#!/usr/bin/env python3
"""Run Stage06/07 for Stage05 candidate papers with one model profile.

The script discovers papers from Stage05 ``candidates.jsonl`` files and delegates
each paper to the existing ``src.cli run-stage06-07`` entry point.  Model
credentials are kept in the child process environment and are never written to
the batch manifest or status files.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_SOURCE_RUN = (
    Path(__file__).resolve().parents[2]
    / "runs/stage00-05-qualityfix-published-since-20260101-20260814T201641"
)
DEFAULT_BASE_URL = "http://127.0.0.1:50917/v1"
DEFAULT_MODEL = "gpt-5.6-sol"


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def _stage05_paths(source_root: Path, filename: str) -> list[Path]:
    paths = set(source_root.glob(f"batches/*/stage_05_benchmark_suitability/{filename}"))
    paths.update(
        source_root.glob(
            f"batches/*/microbatches/*/stage_05_benchmark_suitability/{filename}"
        )
    )
    paths.update(source_root.glob(f"stage_05_benchmark_suitability/{filename}"))
    paths.update(source_root.glob(f"microbatches/*/stage_05_benchmark_suitability/{filename}"))
    return sorted(path for path in paths if path.is_file())


def discover_papers(source_root: Path) -> list[str]:
    """Return unique candidate papers whose latest Stage05 decision passed."""

    papers: set[str] = set()
    paths = _stage05_paths(source_root, "candidates.jsonl")
    if not paths:
        raise FileNotFoundError(
            f"no Stage05 candidates.jsonl found below {source_root}"
        )
    for path in paths:
        with path.open(encoding="utf-8") as handle:
            for line in handle:
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                paper_id = str(row.get("paper_id") or "").strip()
                if paper_id:
                    papers.add(paper_id)
    decision_paths = _stage05_paths(source_root, "decisions.jsonl")
    if not decision_paths:
        raise FileNotFoundError(
            f"no Stage05 decisions.jsonl found below {source_root}"
        )
    latest_decisions: dict[str, dict[str, Any]] = {}
    for path in decision_paths:
        with path.open(encoding="utf-8") as handle:
            for line in handle:
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                paper_id = str(row.get("paper_id") or "").strip()
                if paper_id not in papers:
                    continue
                previous = latest_decisions.get(paper_id)
                if previous is None or str(row.get("created_at") or "") >= str(
                    previous.get("created_at") or ""
                ):
                    latest_decisions[paper_id] = row
    return sorted(
        paper_id
        for paper_id, decision in latest_decisions.items()
        if decision.get("passed") is True
        or str(decision.get("decision") or "").casefold() in {"pass", "needs_builder_review"}
    )


def _run_one(
    *,
    paper: str,
    args: argparse.Namespace,
    output_root: Path,
    environment: dict[str, str],
) -> dict[str, Any]:
    paper_root = output_root / "papers" / paper
    status_path = paper_root / "run_status.json"
    log_path = paper_root / "runner.log"
    paper_root.mkdir(parents=True, exist_ok=True)
    if (paper_root / "late_stage_run_summary.json").is_file() and not args.force:
        result = {"paper_id": paper, "state": "COMPLETED", "skipped": True, "exit_code": 0}
        _write_json(status_path, {**result, "updated_at": _now()})
        return result

    started = _now()
    _write_json(status_path, {"paper_id": paper, "state": "RUNNING", "started_at": started})
    command = [
        sys.executable,
        "-m",
        "src.cli",
        "run-stage06-07",
        "--source-run",
        str(args.source_run),
        "--paper",
        paper,
        "--output",
        str(paper_root),
        "--config",
        str(args.config),
        "--harness",
        args.harness,
    ]
    with log_path.open("a", encoding="utf-8") as log:
        log.write(f"[{started}] command started for {paper}\n")
        completed = subprocess.run(
            command,
            cwd=str(args.pipeline_root),
            env=environment,
            stdout=log,
            stderr=subprocess.STDOUT,
            check=False,
        )
    finished = _now()
    state = "COMPLETED" if completed.returncode == 0 else "FAILED"
    result = {
        "paper_id": paper,
        "state": state,
        "started_at": started,
        "finished_at": finished,
        "exit_code": completed.returncode,
        "skipped": False,
    }
    _write_json(status_path, result)
    return result


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Batch Stage06/07 synthesis for papers with Stage05 candidates."
    )
    parser.add_argument("--source-run", type=Path, default=DEFAULT_SOURCE_RUN)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--config", type=Path, default=Path("config.example.json"))
    parser.add_argument("--paper", action="append", help="Paper ID; repeat to select specific papers")
    parser.add_argument("--limit", type=int, help="Maximum discovered papers to run")
    parser.add_argument(
        "--max-parallel",
        type=int,
        default=8,
        help="Concurrent papers (default: 8; lower this if the endpoint rate-limits)",
    )
    parser.add_argument("--harness", choices=("codex", "opencode", "claude"), default="codex")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--reasoning-effort", default="high")
    parser.add_argument("--api-key", help="API key (prefer --api-key-env to avoid shell history)")
    parser.add_argument("--api-key-env", default="RCB_GPT_API_KEY")
    parser.add_argument("--force", action="store_true", help="Rerun papers with an existing summary")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    args.pipeline_root = Path(__file__).resolve().parents[2]
    args.source_run = args.source_run.expanduser().resolve()
    args.output_root = args.output_root.expanduser().resolve()
    args.config = args.config.expanduser().resolve()
    if not args.source_run.is_dir():
        raise SystemExit(f"source run does not exist: {args.source_run}")
    if not args.config.is_file():
        raise SystemExit(f"config does not exist: {args.config}")
    if args.max_parallel < 1:
        raise SystemExit("--max-parallel must be at least 1")

    discovered = discover_papers(args.source_run)
    selected = list(dict.fromkeys(args.paper or discovered))
    unknown = sorted(set(selected) - set(discovered))
    if unknown:
        raise SystemExit(f"selected papers have no Stage05 candidate: {unknown}")
    if args.limit is not None:
        if args.limit < 1:
            raise SystemExit("--limit must be at least 1")
        selected = selected[: args.limit]
    if not selected:
        raise SystemExit("no papers selected")

    api_key = args.api_key or os.environ.get(args.api_key_env)
    if not api_key:
        raise SystemExit(
            f"missing API key; set {args.api_key_env} or pass --api-key (it is not persisted)"
        )
    environment = os.environ.copy()
    environment.update(
        {
            "RCB_STAGE06_HARNESS": args.harness,
            "RCB_STAGE07_HARNESS": args.harness,
            "RCB_STAGE06_CONVERTER_HARNESS": args.harness,
            "RCB_BUILDER_BASE_URL": args.base_url,
            "RCB_JUDGE_BASE_URL": args.base_url,
            "RCB_BUILDER_MODEL": args.model,
            "RCB_JUDGE_MODEL": args.model,
            "RCB_BUILDER_REASONING_EFFORT": args.reasoning_effort,
            "RCB_JUDGE_REASONING_EFFORT": args.reasoning_effort,
            "RCB_BUILDER_API_KEY": api_key,
            "RCB_JUDGE_API_KEY": api_key,
            "PYTHONPATH": str(args.pipeline_root)
            + (os.pathsep + environment["PYTHONPATH"] if environment.get("PYTHONPATH") else ""),
        }
    )
    args.output_root.mkdir(parents=True, exist_ok=True)
    batch = {
        "state": "RUNNING",
        "started_at": _now(),
        "source_run": str(args.source_run),
        "config": str(args.config),
        "harness": args.harness,
        "model": args.model,
        "base_url": args.base_url,
        "reasoning_effort": args.reasoning_effort,
        "papers": selected,
    }
    _write_json(args.output_root / "batch_status.json", batch)
    results: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=args.max_parallel) as executor:
        futures = [
            executor.submit(
                _run_one,
                paper=paper,
                args=args,
                output_root=args.output_root,
                environment=environment,
            )
            for paper in selected
        ]
        for future in as_completed(futures):
            results.append(future.result())
    results.sort(key=lambda row: selected.index(row["paper_id"]))
    failed = [row for row in results if row["state"] != "COMPLETED"]
    batch.update(
        {
            "state": "COMPLETED" if not failed else "COMPLETED_WITH_FAILURES",
            "finished_at": _now(),
            "results": results,
            "failed_count": len(failed),
        }
    )
    _write_json(args.output_root / "batch_status.json", batch)
    print(json.dumps(batch, ensure_ascii=False, indent=2))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
