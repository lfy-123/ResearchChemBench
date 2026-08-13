#!/usr/bin/env python3
"""Resume Stage04/05 in an existing Stage00-03 run.

Only microbatches whose Stage03 cache is complete are consumed. Stage04 and
Stage05 caches are checked before every call, so the command can be interrupted
and restarted without re-parsing or re-auditing completed microbatches.
"""

from __future__ import annotations

import argparse
import copy
import fcntl
import json
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from src.config import load_config
from src.contracts import read_json, read_jsonl, write_json
from src.pipeline import (
    STAGE_DIRS,
    _aggregate_phase2,
    _clients,
    _load_cached_microbatch_stage,
    _microbatch_stage_hashes,
    _write_microbatch_stage_cache,
)
from src.registry import ScreeningRegistry
from src.sandbox.manager import SandboxRunOptions
from src.sandbox.mineru_pool import MineruSandboxPool
from src.stages.stage04_mineru_normalization.stage import run_stage04
from src.stages.stage05_benchmark_suitability.stage import run_stage05

PIPELINE_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_TEMPLATE = PIPELINE_ROOT / "config.example.json"


def main() -> int:
    args = _parse_args()
    if args.start_stage > args.stop_stage:
        raise ValueError("--start-stage must be less than or equal to --stop-stage")
    if args.mineru_sandbox_count < 1:
        raise ValueError("--mineru-sandbox-count must be at least 1")
    if args.stage04_microbatch_concurrency < 1:
        raise ValueError("--stage04-microbatch-concurrency must be at least 1")
    if args.mineru_max_attempts < 1:
        raise ValueError("--mineru-max-attempts must be at least 1")
    run_root = args.run_root.expanduser().resolve()
    lock_path = run_root / ".stage04-05-resume.lock"
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+", encoding="utf-8") as lock:
        try:
            fcntl.flock(lock.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as exc:
            raise RuntimeError(f"another Stage04/05 resume process owns {lock_path}") from exc
        return _run(args, run_root)


def _run(args, run_root: Path) -> int:
    template = load_config(args.template)
    batch_dirs = sorted((run_root / "batches").glob("batch-[0-9][0-9][0-9][0-9]"))
    if not batch_dirs:
        raise RuntimeError(f"no batch workspaces found under {run_root / 'batches'}")
    ready = [batch for batch in batch_dirs if _batch_ready(batch)]
    if args.dry_run:
        print(json.dumps({"run_root": str(run_root), "batches": len(batch_dirs), "stage03_ready": len(ready),
                          "sandbox_count": args.mineru_sandbox_count}, ensure_ascii=False))
        return 0
    pool_options = SandboxRunOptions(
        cpu=args.mineru_sandbox_cpu,
        memory=args.mineru_sandbox_memory,
        lifecycle_minutes=args.mineru_sandbox_lifecycle_minutes,
        startup_timeout_seconds=args.mineru_sandbox_startup_timeout_seconds,
        cleanup=args.mineru_sandbox_cleanup,
        source=run_root / ".mineru_pool" / "unused.yaml",
        inventory=run_root / ".mineru_pool" / "unused.json",
        api_key_env=args.sandbox_api_key_env,
    )
    pool_root = run_root / ".mineru_pool"
    processed = 0
    waiting = 0
    with MineruSandboxPool(
        options=pool_options,
        count=args.mineru_sandbox_count,
        state_root=pool_root,
        startup_concurrency=args.mineru_sandbox_startup_concurrency,
        supervisor_interval_seconds=args.mineru_sandbox_supervisor_interval_seconds,
        max_attempts=args.mineru_max_attempts,
        retry_delay_seconds=args.mineru_retry_delay_seconds,
    ) as pool:
        for batch_dir in batch_dirs:
            config_path = run_root / "configs" / f"{batch_dir.name}.json"
            if not config_path.is_file():
                continue
            batch = load_config(config_path)
            if not _batch_ready(batch_dir):
                waiting += 1
                continue
            if _process_batch(
                batch=batch,
                template=template,
                batch_dir=batch_dir,
                pool=pool,
                args=args,
            ):
                processed += 1
        if args.watch:
            while True:
                status = read_json(run_root / "batch_status.json") if (run_root / "batch_status.json").is_file() else {}
                state = str(status.get("state") or "")
                changed = False
                for batch_dir in batch_dirs:
                    config_path = run_root / "configs" / f"{batch_dir.name}.json"
                    if not config_path.is_file() or not _batch_ready(batch_dir):
                        continue
                    batch = load_config(config_path)
                    batch_changed = _process_batch(
                        batch=batch,
                        template=template,
                        batch_dir=batch_dir,
                        pool=pool,
                        args=args,
                    )
                    changed = batch_changed or changed
                    processed += int(batch_changed)
                if state in {"completed", "failed", "interrupted"}:
                    break
                if not changed:
                    time.sleep(args.poll_seconds)
    print(
        json.dumps(
            {
                "run_root": str(run_root),
                "processed_batches": processed,
                "waiting_batches": waiting,
                "sandbox_count": args.mineru_sandbox_count,
                "start_stage": args.start_stage,
                "stop_stage": args.stop_stage,
            },
            ensure_ascii=False,
        )
    )
    return 0


def _process_batch(*, batch, template, batch_dir: Path, pool, args) -> bool:
    stage03_root = batch_dir / STAGE_DIRS["stage03"]
    if not (stage03_root / "stage_summary.json").is_file():
        return False
    stage01_root = batch_dir / STAGE_DIRS["stage01"]
    papers = read_jsonl(stage01_root / "paper_bundles.jsonl")
    papers = [row for row in papers if row.get("decision") == "pass"]
    all_micro = sorted((batch_dir / "microbatches").glob("batch-[0-9][0-9][0-9][0-9][0-9][0-9]"))
    if not all_micro:
        return False
    # Stage05 config/model roles are absent when the upstream run stopped at
    # Stage03. Fill only those roles from the current template configuration.
    effective = copy.deepcopy(batch)
    effective["stop_after"] = "stage05"
    effective["stage05"] = copy.deepcopy(template["stage05"])
    effective["models"]["stage05_router"] = copy.deepcopy(template["models"]["stage05_router"])
    effective["models"]["suitability"] = copy.deepcopy(template["models"]["suitability"])
    effective["stage04"]["mineru"] = copy.deepcopy(batch["stage04"].get("mineru") or {})
    effective["stage04"]["mineru"]["api_concurrency"] = 1
    effective["stage04"]["mineru"]["request_batch_size"] = 1
    effective["stage04"]["mineru"]["environment"] = dict(
        effective["stage04"]["mineru"].get("environment") or {}
    )
    effective["stage04"]["mineru"]["environment"]["_sandbox_runtime"] = pool
    effective["microbatch"] = copy.deepcopy(batch.get("microbatch") or {})
    effective["microbatch"]["size"] = len(papers) or int(effective["microbatch"].get("size", 10))
    registry = ScreeningRegistry.from_config(effective.get("registry") or {})
    clients = _clients(
        effective,
        batch_dir,
        {},
        effective["models"].get("screening") or {},
        args.stop_stage,
        include_screening=False,
    )

    def process(root: Path):
        stage01 = read_jsonl(root / STAGE_DIRS["stage01"] / "paper_bundles.jsonl")
        docs = read_jsonl(root / STAGE_DIRS["stage01"] / "documents.jsonl")
        stage03 = read_jsonl(root / STAGE_DIRS["stage03"] / "decisions.jsonl")
        if not stage03:
            return None
        mb_papers = [row for row in stage01 if row.get("decision") == "pass"]
        hashes = _microbatch_stage_hashes(mb_papers, docs, effective)
        stage04 = _load_cached_microbatch_stage(root, "stage04", hashes["stage04"])
        changed = False
        if stage04 is None and args.start_stage <= 4 <= args.stop_stage:
            stage04 = run_stage04(
                stage03_records=stage03,
                documents=docs,
                config=effective["stage04"],
                workspace=root,
                run_id=batch["run_id"],
            )
            _write_microbatch_stage_cache(
                root, "stage04", hashes["stage04"], batch["run_id"],
                cacheable=not any(r.get("processing_status") == "failed" for r in stage04["records"]),
            )
            changed = True
        if stage04 is None:
            return None
        stage05 = _load_cached_microbatch_stage(root, "stage05", hashes["stage05"])
        if stage05 is None and args.start_stage <= 5 <= args.stop_stage:
            stage05 = run_stage05(
                stage04_records=stage04["records"],
                documents=stage04["documents"],
                config=effective["stage05"],
                router_model=clients["stage05_router"],
                auditor_model=clients["suitability"],
                workspace=root,
                run_id=batch["run_id"],
            )
            _write_microbatch_stage_cache(
                root, "stage05", hashes["stage05"], batch["run_id"],
                cacheable=not any(r.get("processing_status") == "failed" for r in stage05["records"]),
            )
            changed = True
        if stage04 is not None:
            registry.record_stage_results(
                run_id=batch["run_id"], stage="stage04", rows=stage04.get("records") or [], prune=False
            )
        if stage05 is not None:
            registry.record_stage_results(
                run_id=batch["run_id"], stage="stage05", rows=stage05.get("records") or [], prune=False
            )
        state = {
            "stage04": stage04 or {"records": [], "documents": [], "deep_parse_attempts": []},
            "stage05": stage05 or {"records": [], "candidates": []},
            "_resume_changed": changed,
        }
        return state

    ready_roots = []
    for root in all_micro:
        stage03_cache = root / STAGE_DIRS["stage03"] / "stage_cache.json"
        if stage03_cache.is_file() and read_json(stage03_cache).get("status") == "completed":
            ready_roots.append(root)
    if not ready_roots:
        return False
    max_workers = max(1, min(args.stage04_microbatch_concurrency, len(ready_roots)))
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Include cached microbatches in the aggregate, otherwise a later
        # resume would overwrite the batch-level summary with only new work.
        states = [state for state in executor.map(process, ready_roots) if state is not None]
    if not states:
        return False
    _aggregate_phase2(states, batch_dir, batch["run_id"], args.stop_stage)
    write_json(
        batch_dir / "stage04_05_resume_summary.json",
        {
            "run_id": batch["run_id"],
            "stages": [f"stage{index:02d}" for index in range(args.start_stage, args.stop_stage + 1)],
            "microbatches": len(states),
            "source": "resume_stage04_05",
        },
    )
    return any(bool(state.get("_resume_changed")) for state in states)


def _batch_ready(batch_dir: Path) -> bool:
    summary = batch_dir / STAGE_DIRS["stage03"] / "stage_summary.json"
    return summary.is_file()


def _parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE)
    parser.add_argument("--start-stage", type=int, choices=(4, 5), default=4)
    parser.add_argument("--stop-stage", type=int, choices=(4, 5), default=5)
    parser.add_argument("--mineru-sandbox-count", type=int, default=32)
    parser.add_argument("--mineru-sandbox-cpu", type=int, default=16)
    parser.add_argument("--mineru-sandbox-memory", default="32Gi")
    parser.add_argument("--mineru-sandbox-lifecycle-minutes", type=int, default=1440)
    parser.add_argument("--mineru-sandbox-startup-timeout-seconds", type=int, default=3600)
    parser.add_argument("--mineru-sandbox-cleanup", choices=("keep", "stop", "delete"), default="stop")
    parser.add_argument("--mineru-sandbox-startup-concurrency", type=int, default=32)
    parser.add_argument("--mineru-sandbox-supervisor-interval-seconds", type=float, default=15)
    parser.add_argument("--mineru-max-attempts", type=int, default=2)
    parser.add_argument("--mineru-retry-delay-seconds", type=float, default=5)
    parser.add_argument("--sandbox-api-key-env", default="RCB_SANDBOX_API_KEY")
    parser.add_argument("--stage04-microbatch-concurrency", type=int, default=32)
    parser.add_argument("--poll-seconds", type=int, default=60)
    parser.add_argument("--watch", action="store_true", help="wait for future Stage03-complete batches")
    parser.add_argument("--dry-run", action="store_true", help="inspect readiness without creating sandboxes")
    return parser.parse_args()


if __name__ == "__main__":
    raise SystemExit(main())
