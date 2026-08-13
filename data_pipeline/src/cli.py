from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from src.core.io import read_jsonl, write_json, write_jsonl
from src.integrations.mineru import build_mineru_queue, run_mineru_queue
from src.pipeline import run_pipeline
from src.core.resume_workflow import STAGES, command_digest, execute_resume, prepare_resume
from src.stages.stage00_remote_corpus import prepare_remote_corpus

DATA_PIPELINE_ROOT = Path(__file__).resolve().parents[1]


def _load_local_environment() -> None:
    for path in (
        DATA_PIPELINE_ROOT / "config.local.env",
        DATA_PIPELINE_ROOT.parent / "config.local.env",
    ):
        if path.is_file():
            load_dotenv(path, override=False)
    if not os.environ.get("RESOURCE_LLM_URL") and os.environ.get("JUDGE_API_BASE"):
        os.environ["RESOURCE_LLM_URL"] = os.environ["JUDGE_API_BASE"]
    if not os.environ.get("RESOURCE_LLM_API_KEY") and os.environ.get("JUDGE_API_KEY"):
        os.environ["RESOURCE_LLM_API_KEY"] = os.environ["JUDGE_API_KEY"]
    if not os.environ.get("RESOURCE_LLM_MODEL_NAME") and os.environ.get("JUDGE_MODEL_NAME"):
        os.environ["RESOURCE_LLM_MODEL_NAME"] = os.environ["JUDGE_MODEL_NAME"]
    environment_bin = str(Path(sys.prefix) / "bin")
    path_entries = os.environ.get("PATH", "").split(os.pathsep)
    if environment_bin not in path_entries:
        os.environ["PATH"] = os.pathsep.join([environment_bin, *path_entries])


def _add_sandbox_options(parser: argparse.ArgumentParser, *, include_cleanup: bool = True) -> None:
    parser.add_argument("--sandbox-cpu", type=int, default=32)
    parser.add_argument("--sandbox-memory", default="96Gi")
    parser.add_argument("--sandbox-lifecycle-minutes", type=int, default=1440)
    parser.add_argument("--sandbox-startup-timeout-seconds", type=int, default=3600)
    parser.add_argument("--sandbox-source", type=Path)
    parser.add_argument("--sandbox-inventory", type=Path)
    parser.add_argument("--sandbox-base-url", default="https://h.pjlab.org.cn/brainbox")
    parser.add_argument("--sandbox-project", default="ailab-ai4chem")
    parser.add_argument(
        "--sandbox-image",
        default=("registry.h.pjlab.org.cn/ailab-ai4chem-ai4chem_cpu/base:python312-20260627215752"),
    )
    parser.add_argument("--sandbox-api-key-env", default="RCB_SANDBOX_API_KEY")
    if include_cleanup:
        parser.add_argument(
            "--sandbox-cleanup",
            choices=("keep", "stop", "delete"),
            default="stop",
            help="What to do with the sandbox instance after the pipeline exits",
        )


def _sandbox_options(args):
    from src.sandbox.manager import DEFAULT_INVENTORY, DEFAULT_SOURCE, SandboxRunOptions

    return SandboxRunOptions(
        cpu=args.sandbox_cpu,
        memory=args.sandbox_memory,
        lifecycle_minutes=args.sandbox_lifecycle_minutes,
        startup_timeout_seconds=args.sandbox_startup_timeout_seconds,
        cleanup=getattr(args, "sandbox_cleanup", "keep"),
        source=args.sandbox_source or DEFAULT_SOURCE,
        inventory=args.sandbox_inventory or DEFAULT_INVENTORY,
        base_url=args.sandbox_base_url,
        project=args.sandbox_project,
        image=args.sandbox_image,
        api_key_env=args.sandbox_api_key_env,
    )


def main(argv: list[str] | None = None) -> int:
    _load_local_environment()
    parser = argparse.ArgumentParser(prog="chem-pipeline")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run", help="Run the configured data pipeline")
    run_parser.add_argument("--config", default="config.example.json")
    run_parser.add_argument("--output")
    run_parser.add_argument(
        "--stop-after",
        choices=tuple(f"stage{index:02d}" for index in range(8)),
        help="Override the configured final stage for this invocation",
    )
    run_parser.add_argument("--execution-backend", choices=("local", "sandbox"), default=None)
    run_parser.add_argument(
        "--sandbox",
        action="store_const",
        const="sandbox",
        dest="execution_backend",
        help="Shortcut for --execution-backend sandbox",
    )
    run_parser.add_argument(
        "--microbatch",
        action=argparse.BooleanOptionalAction,
        default=None,
        help="Enable or disable the Stage 02 through stop_after microbatch scheduler",
    )
    run_parser.add_argument("--microbatch-size", type=int)
    run_parser.add_argument("--microbatch-concurrency", type=int)
    _add_sandbox_options(run_parser)

    prepare_parser = subparsers.add_parser(
        "prepare-remote-corpus",
        help="Run Stage 00 and group each remote main paper with its supplementary files",
    )
    prepare_parser.add_argument("--dataset", default="en-paper-hzzj")
    prepare_parser.add_argument("--count", type=int, required=True)
    prepare_parser.add_argument("--output", required=True)
    prepare_parser.add_argument(
        "--credentials",
        default="/mnt/shared-storage-user/liyuqiang/benchmark/pipline_demo/pdfs/xinghe.txt",
    )
    prepare_parser.add_argument("--outside", action="store_true")
    prepare_parser.add_argument(
        "--selection", choices=("remote_order", "seeded_sample"), default="remote_order"
    )
    prepare_parser.add_argument("--seed", type=int, default=0)
    prepare_parser.add_argument(
        "--exclude-selection-manifest", type=Path, action="append", default=[]
    )
    prepare_parser.add_argument("--no-resume", action="store_true")
    prepare_parser.add_argument("--without-supplementary", action="store_true")

    sandbox_parser = subparsers.add_parser(
        "sandbox", help="Create, inspect, stop, or delete the managed pipeline sandbox"
    )
    sandbox_parser.add_argument("action", choices=("create", "status", "stop", "delete"))
    sandbox_parser.add_argument(
        "--delete-environment",
        action="store_true",
        help="Also delete the managed Environment when action=delete",
    )
    _add_sandbox_options(sandbox_parser, include_cleanup=False)

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
    mineru_parser.add_argument("--workers", type=int, default=1)
    mineru_parser.add_argument("--request-batch-size", type=int, default=1)
    mineru_parser.add_argument("--force", action="store_true")

    resume_parser = subparsers.add_parser(
        "resume", help="Plan or resume Stage00-05 at paper/document granularity"
    )
    resume_parser.add_argument("--run-root", type=Path, required=True)
    resume_parser.add_argument("--total", type=int, required=True)
    resume_parser.add_argument("--batch-size", type=int, default=1000)
    resume_parser.add_argument("--template", type=Path, default=DATA_PIPELINE_ROOT / "config.example.json")
    resume_parser.add_argument("--batch", action="append", default=[])
    resume_parser.add_argument("--start-stage", choices=STAGES, default="stage00")
    resume_parser.add_argument("--stop-stage", choices=STAGES, default="stage05")
    resume_modes = resume_parser.add_mutually_exclusive_group()
    resume_modes.add_argument("--retry-only", action="store_true")
    resume_modes.add_argument("--pending-only", action="store_true")
    resume_parser.add_argument("--invalidate-stage", action="append", choices=STAGES, default=[])
    resume_parser.add_argument("--resume-config", choices=("original", "current"), default="original")
    resume_parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    if args.command == "run":
        result = run_pipeline(
            args.config,
            execution_backend=args.execution_backend,
            stop_after=args.stop_after,
            sandbox_options=(
                _sandbox_options(args) if args.execution_backend == "sandbox" else None
            ),
            microbatch_overrides={
                key: value
                for key, value in {
                    "enabled": args.microbatch,
                    "size": args.microbatch_size,
                    "concurrency": args.microbatch_concurrency,
                }.items()
                if value is not None
            },
        )
        if args.output:
            write_json(args.output, result)
    elif args.command == "prepare-remote-corpus":
        result = prepare_remote_corpus(
            args.output,
            dataset=args.dataset,
            count=args.count,
            credentials=args.credentials,
            outside=args.outside,
            resume=not args.no_resume,
            copy_supplementary=not args.without_supplementary,
            selection=args.selection,
            seed=args.seed,
            exclude_selected_manifests=args.exclude_selection_manifest,
        )
        result = {"summary": result["summary"], "corpus_root": result["corpus_root"]}
    elif args.command == "sandbox":
        from dataclasses import asdict

        from src.sandbox.manager import SandboxManager

        manager = SandboxManager(_sandbox_options(args))
        if args.action == "create":
            result = {"status": "running", "worker": asdict(manager.ensure())}
        elif args.action == "status":
            result = manager.status()
        elif args.action == "stop":
            result = manager.stop()
        elif args.action == "delete":
            result = manager.delete(delete_environment=args.delete_environment)
        else:
            raise AssertionError(args.action)
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
            max_workers=args.workers,
            request_batch_size=args.request_batch_size,
        )
        write_jsonl(args.result_output, rows)
        result = {"queued": len(queue), "results": len(rows)}
    elif args.command == "resume":
        values = {
            key: value
            for key, value in vars(args).items()
            if key not in {"command", "template"}
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
        result = plan if args.dry_run else execute_resume(
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
    else:
        raise AssertionError(args.command)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
