#!/usr/bin/env python3
"""Plan or resume Stage00-05 work in an existing batch run root."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from src.core.resume_workflow import (
    STAGES,
    command_digest,
    execute_resume,
    prepare_resume,
)


PIPELINE_ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    args = _parse_args()
    values = {
        "run_root": str(args.run_root.expanduser().resolve()),
        "total": args.total,
        "batch_size": args.batch_size,
        "batches": args.batch,
        "start_stage": args.start_stage,
        "stop_stage": args.stop_stage,
        "retry_only": args.retry_only,
        "pending_only": args.pending_only,
        "invalidate_stage": args.invalidate_stage,
        "resume_config": args.resume_config,
    }
    store, specs, plan = prepare_resume(
        run_root=args.run_root,
        total=args.total,
        batch_size=args.batch_size,
        template_path=args.template,
        start_stage=args.start_stage,
        stop_stage=args.stop_stage,
        batch_ids=args.batch,
        pending_only=args.pending_only,
        retry_only=args.retry_only,
        materialize_expansion=not args.dry_run,
    )
    if args.dry_run:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
        return 0
    result = execute_resume(
        store=store,
        specs=specs,
        total=args.total,
        start_stage=args.start_stage,
        stop_stage=args.stop_stage,
        retry_only=args.retry_only,
        invalidated_stages=args.invalidate_stage,
        resume_config=args.resume_config,
        runtime_overrides={},
        command_digest=command_digest(values),
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "completed" else 1


def _parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--total", type=int, required=True)
    parser.add_argument("--batch-size", type=int, default=1000)
    parser.add_argument("--template", type=Path, default=PIPELINE_ROOT / "config.example.json")
    parser.add_argument("--batch", action="append", default=[])
    parser.add_argument("--start-stage", choices=STAGES, default="stage00")
    parser.add_argument("--stop-stage", choices=STAGES, default="stage05")
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--retry-only", action="store_true")
    modes.add_argument("--pending-only", action="store_true")
    parser.add_argument("--invalidate-stage", action="append", default=[], choices=STAGES)
    parser.add_argument("--resume-config", choices=("original", "current"), default="original")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


if __name__ == "__main__":
    raise SystemExit(main())
