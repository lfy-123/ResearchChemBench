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
import random
import subprocess
import sys
import urllib.error
import urllib.request
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


def _preflight_models(
    endpoints: dict[str, tuple[str, str, str]],
) -> dict[str, str] | None:
    """Return unavailable requested models, or ``None`` when the endpoint cannot be probed.

    The preflight is deliberately fail-open for gateways without a `/models`
    route.  When the route is available it prevents a known account/model
    mismatch from launching ten identical Agent processes and their internal
    reconnect loops.
    """

    unavailable: dict[str, str] = {}
    for role, (base_url, api_key, model) in endpoints.items():
        url = base_url.rstrip("/") + "/models"
        request = urllib.request.Request(url, headers={"Authorization": f"Bearer {api_key}"})
        try:
            with urllib.request.urlopen(request, timeout=10) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except (OSError, urllib.error.URLError, TimeoutError, ValueError, TypeError, json.JSONDecodeError):
            # A gateway may intentionally omit /models. Let the real request
            # decide in that case; this preflight is only a deterministic guard
            # for known model/account mismatches.
            continue
        available = {
            str(row.get("id") or "").strip()
            for row in (payload.get("data") or [])
            if isinstance(row, dict) and str(row.get("id") or "").strip()
        }
        if model not in available:
            unavailable[role] = model
    return unavailable


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
        result = {
            "paper_id": paper,
            **_late_stage_outcome(paper_root / "late_stage_run_summary.json"),
            "skipped": True,
            "exit_code": 0,
        }
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
    try:
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
    except Exception as exc:
        # A worker must never leave its paper in RUNNING when process creation,
        # logging, or the child command fails before it returns a CompletedProcess.
        finished = _now()
        result = {
            "paper_id": paper,
            "state": "FAILED",
            "started_at": started,
            "finished_at": finished,
            "exit_code": None,
            "skipped": False,
            "error": {"type": type(exc).__name__, "message": str(exc)[:4000]},
        }
        _write_json(status_path, result)
        return result
    finished = _now()
    summary_path = paper_root / "late_stage_run_summary.json"
    if completed.returncode == 0:
        outcome = _late_stage_outcome(summary_path)
    else:
        outcome = {
            "state": "FAILED",
            "outcome": "technical_blocked",
            "failure_class": "child_process_failed",
        }
    result = {
        "paper_id": paper,
        **outcome,
        "started_at": started,
        "finished_at": finished,
        "exit_code": completed.returncode,
        "skipped": False,
    }
    if result["state"] == "FAILED":
        result["late_stage_summary"] = str(summary_path)
    _write_json(status_path, result)
    return result


def _late_stage_outcome(summary_path: Path) -> dict[str, str]:
    """Classify one paper into the canonical late-stage terminal outcome."""

    def blocked(failure_class: str) -> dict[str, str]:
        return {
            "state": "FAILED",
            "outcome": "technical_blocked",
            "failure_class": failure_class,
        }

    if not summary_path.is_file():
        return blocked("late_stage_summary_missing")
    try:
        summary = json.loads(summary_path.read_text(encoding="utf-8"))
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        return blocked("late_stage_summary_invalid")
    if not isinstance(summary, dict):
        return blocked("late_stage_summary_invalid")
    stage06 = summary.get("stage06") or {}
    if not isinstance(stage06, dict):
        return blocked("stage06_summary_invalid")
    decisions = stage06.get("decisions") or {}
    if not isinstance(decisions, dict):
        return blocked("stage06_summary_invalid")
    try:
        stage06_blocked = int(
            stage06.get("technical_blocked") or decisions.get("technical_blocked") or 0
        )
        scientific_rejections = int(
            stage06.get("provisional_not_constructible")
            or decisions.get("provisional_not_constructible")
            or 0
        )
    except (TypeError, ValueError):
        return blocked("stage06_summary_invalid")
    if stage06_blocked:
        return blocked("stage06_technical_blocked")
    stage07 = summary.get("stage07") or {}
    if not isinstance(stage07, dict):
        return blocked("stage07_summary_invalid")
    if str(stage07.get("status") or "").casefold() == "not_run":
        if scientific_rejections > 0:
            return {"state": "COMPLETED", "outcome": "scientific_rejection"}
        return blocked("stage07_not_run")
    try:
        stage07_blocked = int(stage07.get("technical_blocked") or 0)
        mechanical_blocked = int(stage07.get("mechanical_publish_blocked") or 0)
        scientific_rejected = int(stage07.get("rejected_scientific_unrepairable") or 0)
        publish_ready = int(stage07.get("publish_ready") or 0)
    except (TypeError, ValueError):
        return blocked("stage07_summary_invalid")
    if stage07_blocked or mechanical_blocked:
        return blocked("stage07_technical_blocked")
    if scientific_rejected:
        return {"state": "COMPLETED", "outcome": "scientific_rejection"}
    if publish_ready:
        return {"state": "COMPLETED", "outcome": "published"}
    return blocked("late_stage_outcome_unknown")


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
        "--random-seed",
        type=int,
        help="Sample --limit papers reproducibly from the discovered Stage05 set",
    )
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
    parser.add_argument(
        "--reasoning-mode",
        help="Optional upstream reasoning mode (for example, pro); recorded as a model configuration, not a model slug",
    )
    parser.add_argument("--api-key", help="API key (prefer --api-key-env to avoid shell history)")
    parser.add_argument("--api-key-env", default="RCB_GPT_API_KEY")
    parser.add_argument(
        "--stage06-model",
        help="Model used by Stage06A/06B; defaults to --model",
    )
    parser.add_argument(
        "--stage07-model",
        help="Model used by Stage07; defaults to --model",
    )
    parser.add_argument(
        "--stage06-base-url",
        help="Stage06 endpoint; defaults to --base-url",
    )
    parser.add_argument(
        "--stage07-base-url",
        help="Stage07 endpoint; defaults to --base-url",
    )
    parser.add_argument(
        "--stage06-api-key",
        help="Stage06 API key (prefer --stage06-api-key-env)",
    )
    parser.add_argument(
        "--stage07-api-key",
        help="Stage07 API key (prefer --stage07-api-key-env)",
    )
    parser.add_argument("--stage06-api-key-env")
    parser.add_argument("--stage07-api-key-env")
    parser.add_argument("--stage06-reasoning-effort")
    parser.add_argument("--stage07-reasoning-effort")
    parser.add_argument("--stage06-reasoning-mode")
    parser.add_argument("--stage07-reasoning-mode")
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
        if args.random_seed is None:
            selected = selected[: args.limit]
        else:
            if args.limit > len(selected):
                raise SystemExit("--limit cannot exceed the discovered paper count")
            selected = random.Random(args.random_seed).sample(selected, args.limit)
    if not selected:
        raise SystemExit("no papers selected")

    shared_api_key = args.api_key or os.environ.get(args.api_key_env)

    def _role_credential(explicit: str | None, env_name: str | None) -> str | None:
        return explicit or (os.environ.get(env_name) if env_name else None) or shared_api_key

    stage06_api_key = _role_credential(args.stage06_api_key, args.stage06_api_key_env)
    stage07_api_key = _role_credential(args.stage07_api_key, args.stage07_api_key_env)
    if not stage06_api_key or not stage07_api_key:
        raise SystemExit(
            f"missing Stage06/07 API key; set {args.api_key_env} or the role-specific key env "
            "or pass an explicit key (keys are not persisted)"
        )
    stage06_model = args.stage06_model or args.model
    stage07_model = args.stage07_model or args.model
    stage06_base_url = args.stage06_base_url or args.base_url
    stage07_base_url = args.stage07_base_url or args.base_url
    stage06_reasoning_effort = args.stage06_reasoning_effort or args.reasoning_effort
    stage07_reasoning_effort = args.stage07_reasoning_effort or args.reasoning_effort
    stage06_reasoning_mode = args.stage06_reasoning_mode or args.reasoning_mode
    stage07_reasoning_mode = args.stage07_reasoning_mode or args.reasoning_mode
    environment = os.environ.copy()
    environment.update(
        {
            "RCB_STAGE06_HARNESS": args.harness,
            "RCB_STAGE07_HARNESS": args.harness,
            "RCB_STAGE06_CONVERTER_HARNESS": args.harness,
            "RCB_BUILDER_BASE_URL": stage06_base_url,
            "RCB_JUDGE_BASE_URL": stage07_base_url,
            "RCB_BUILDER_MODEL": stage06_model,
            "RCB_JUDGE_MODEL": stage07_model,
            "RCB_BUILDER_REASONING_EFFORT": stage06_reasoning_effort,
            "RCB_JUDGE_REASONING_EFFORT": stage07_reasoning_effort,
            "RCB_BUILDER_API_KEY": stage06_api_key,
            "RCB_JUDGE_API_KEY": stage07_api_key,
            "PYTHONPATH": str(args.pipeline_root)
            + (os.pathsep + environment["PYTHONPATH"] if environment.get("PYTHONPATH") else ""),
        }
    )
    for key, value in (
        ("RCB_BUILDER_REASONING_MODE", stage06_reasoning_mode),
        ("RCB_JUDGE_REASONING_MODE", stage07_reasoning_mode),
    ):
        if value:
            environment[key] = value
        else:
            environment.pop(key, None)
    args.output_root.mkdir(parents=True, exist_ok=True)
    batch = {
        "state": "RUNNING",
        "started_at": _now(),
        "source_run": str(args.source_run),
        "config": str(args.config),
        "harness": args.harness,
        "model": stage06_model if stage06_model == stage07_model else "mixed",
        "stage06_model": stage06_model,
        "stage07_model": stage07_model,
        "stage06_base_url": stage06_base_url,
        "stage07_base_url": stage07_base_url,
        "stage06_reasoning_effort": stage06_reasoning_effort,
        "stage07_reasoning_effort": stage07_reasoning_effort,
        "stage06_reasoning_mode": stage06_reasoning_mode,
        "stage07_reasoning_mode": stage07_reasoning_mode,
        "papers": selected,
    }
    _write_json(args.output_root / "batch_status.json", batch)
    unavailable = _preflight_models(
        {
            "stage06": (stage06_base_url, stage06_api_key, stage06_model),
            "stage07": (stage07_base_url, stage07_api_key, stage07_model),
        }
    )
    if unavailable:
        results = [
            {
                "paper_id": paper,
                "state": "FAILED",
                "started_at": _now(),
                "finished_at": _now(),
                "exit_code": None,
                "skipped": False,
                "failure_class": "model_not_available",
                "unavailable_models": sorted(set(unavailable.values())),
            }
            for paper in selected
        ]
        batch.update(
            {
                "state": "COMPLETED",
                "completed_count": len(results),
                "failed_count": len(results),
                "results": results,
                "finished_at": _now(),
                "preflight": {
                    "status": "failed",
                    "failure_class": "model_not_available",
                    "unavailable_models": sorted(set(unavailable.values())),
                    "unavailable_by_role": unavailable,
                },
            }
        )
        for result in results:
            _write_json(
                args.output_root / "papers" / result["paper_id"] / "run_status.json",
                result,
            )
        _write_json(args.output_root / "batch_status.json", batch)
        return 0
    results: list[dict[str, Any]] = []
    with ThreadPoolExecutor(max_workers=args.max_parallel) as executor:
        futures = {
            executor.submit(
                _run_one,
                paper=paper,
                args=args,
                output_root=args.output_root,
                environment=environment,
            ): paper
            for paper in selected
        }
        for future in as_completed(futures):
            paper = futures[future]
            try:
                results.append(future.result())
            except Exception as exc:
                # Defensive parent-side convergence for an unexpected worker exception.
                # `_run_one` normally records this itself, but the batch must still reach a
                # visible terminal state if a future fails outside that handler.
                result = {
                    "paper_id": paper,
                    "state": "FAILED",
                    "finished_at": _now(),
                    "exit_code": None,
                    "skipped": False,
                    "error": {"type": type(exc).__name__, "message": str(exc)[:4000]},
                }
                _write_json(args.output_root / "papers" / paper / "run_status.json", result)
                results.append(result)
            batch["completed_count"] = len(results)
            batch["results"] = sorted(
                results, key=lambda row: selected.index(row["paper_id"])
            )
            _write_json(args.output_root / "batch_status.json", batch)
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
