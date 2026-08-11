#!/usr/bin/env python3
"""Run Stage00-04 in sequential remote-copy batches with shared compute resources."""

from __future__ import annotations

import argparse
import copy
import json
import signal
import subprocess
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from src.config import load_config
from src.core.io import read_json, write_json
from src.pipeline import run_pipeline
from src.runtime import ensure_managed_screening_worker
from src.sandbox.manager import SandboxManager, SandboxRunOptions

PIPELINE_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_TEMPLATE = PIPELINE_ROOT / "config.example.json"


def main() -> int:
    args = _parse_args()
    _validate_args(args)
    run_root = Path(args.run_root).expanduser().resolve()
    run_root.mkdir(parents=True, exist_ok=True)
    template_path = Path(args.template).expanduser().resolve()
    template = json.loads(template_path.read_text(encoding="utf-8"))
    batches = (args.total + args.batch_size - 1) // args.batch_size
    status_path = run_root / "batch_status.json"
    status = _initial_status(args, run_root, batches)
    if status_path.is_file():
        previous = read_json(status_path)
        status["first_started_at"] = (
            previous.get("first_started_at") or previous.get("started_at")
        )
        status["completed_batches"] = list(previous.get("completed_batches") or [])
        status["batch_results"] = list(previous.get("batch_results") or [])
    write_json(status_path, status)

    configs: list[Path] = []
    manifests: list[Path] = []
    for index in range(batches):
        count = min(args.batch_size, args.total - index * args.batch_size)
        workspace = run_root / "batches" / f"batch-{index + 1:04d}"
        config_path = run_root / "configs" / f"batch-{index + 1:04d}.json"
        config = _batch_config(
            template,
            args=args,
            run_root=run_root,
            workspace=workspace,
            batch_index=index,
            count=count,
            exclusions=manifests,
        )
        write_json(config_path, config)
        configs.append(config_path)
        manifests.append(workspace / "stage_00_remote_corpus" / "selected_papers.jsonl")

    if args.prepare_only:
        status.update({"state": "prepared", "finished_at": _now()})
        write_json(status_path, status)
        print(f"prepared {len(configs)} batch configs under {run_root}", flush=True)
        return 0

    interrupted = False

    def interrupt(_signum, _frame):
        nonlocal interrupted
        interrupted = True
        raise KeyboardInterrupt

    signal.signal(signal.SIGTERM, interrupt)
    signal.signal(signal.SIGINT, interrupt)
    try:
        _wait_before_resource_start(args.initial_delay_hours, status_path, status)
        _start_single_sandbox(run_root, template, args, status_path, status)
        _start_single_worker(configs[0], status_path, status)
        for index, config_path in enumerate(configs, start=1):
            workspace = run_root / "batches" / f"batch-{index:04d}"
            summary_path = workspace / "run_summary.json"
            if _completed_summary(summary_path):
                _record_completed(status, index, read_json(summary_path), resumed=True)
                write_json(status_path, status)
                print(f"batch {index}/{batches} already completed; reusing", flush=True)
                continue
            status.update(
                {
                    "state": "running",
                    "current_batch": index,
                    "current_config": str(config_path),
                    "updated_at": _now(),
                }
            )
            write_json(status_path, status)
            print(
                f"starting batch {index}/{batches}: copy and process "
                f"{json.loads(config_path.read_text(encoding='utf-8'))['stage00']['count']} papers",
                flush=True,
            )
            result = run_pipeline(config_path)
            if result.get("status") != "completed":
                raise RuntimeError(
                    f"batch {index} did not complete cleanly: {result.get('status')}"
                )
            _record_completed(status, index, result, resumed=False)
            write_json(status_path, status)
            print(f"batch {index}/{batches} completed", flush=True)
        status.update(
            {
                "state": "completed",
                "current_batch": None,
                "current_config": None,
                "finished_at": _now(),
                "updated_at": _now(),
            }
        )
        write_json(status_path, status)
        return 0
    except KeyboardInterrupt:
        status.update(
            {
                "state": "interrupted",
                "interrupted": interrupted,
                "finished_at": _now(),
                "updated_at": _now(),
            }
        )
        write_json(status_path, status)
        return 130
    except Exception as exc:
        status.update(
            {
                "state": "failed",
                "error": f"{type(exc).__name__}: {exc}",
                "finished_at": _now(),
                "updated_at": _now(),
            }
        )
        write_json(status_path, status)
        raise
    finally:
        _cleanup_shared_resources(run_root, template, args, status)
        write_json(status_path, status)


def _batch_config(
    template: dict[str, Any],
    *,
    args,
    run_root: Path,
    workspace: Path,
    batch_index: int,
    count: int,
    exclusions: list[Path],
) -> dict[str, Any]:
    config = copy.deepcopy(template)
    config.update(
        {
            "workspace": str(workspace),
            "run_id": f"stage00-04-batch-{batch_index + 1:04d}",
            "stop_after": "stage04",
            "policy": "strict",
            "resume_completed_stages": True,
        }
    )
    config["registry"] = {
        "enabled": True,
        "database": str(run_root / "registry" / "paper_screening_registry.sqlite"),
        "export_jsonl": str(run_root / "registry" / "paper_screening_registry.jsonl"),
        "prune_rejected_stage00_assets": True,
    }
    sandbox = config.setdefault("execution", {}).setdefault("sandbox", {})
    config["execution"]["backend"] = "sandbox"
    sandbox.update(
        {
            "cpu": args.sandbox_cpu,
            "memory": args.sandbox_memory,
            "lifecycle_minutes": 1440,
            "startup_timeout_seconds": args.sandbox_startup_timeout_seconds,
            "cleanup": "keep",
            "source": str(run_root / ".sandboxes.local.yaml"),
            "inventory": str(run_root / ".sandbox_inventory.local.json"),
            "api_key_env": "RCB_SANDBOX_API_KEY",
        }
    )
    config["source"] = {"root": str(PIPELINE_ROOT / "datasets" / "en-paper-hzzj")}
    config["stage00"] = {
        "enabled": True,
        "dataset": args.dataset,
        "count": count,
        "credentials": str(Path(args.credentials).expanduser().resolve()),
        "outside": False,
        "resume": True,
        "selection": "remote_order",
        "seed": args.seed + batch_index,
        "exclude_selected_manifests": [str(path) for path in exclusions],
    }
    package = config["stage01"]["package"]
    package.update({"workers": 32, "network_workers": 32})
    normalization = config["stage01"]["normalization"]
    normalization["workers"] = 32
    normalization["grobid"].update({"workers": 32, "reuse_existing": True})
    config["stage02"].update({"workers": 16})
    config["stage03"].update(
        {
            "workers": 16,
            "toolbox_capabilities": str(PIPELINE_ROOT / "assets" / "toolbox_capabilities.json"),
            "software_aliases": str(PIPELINE_ROOT / "assets" / "software_aliases.json"),
            "external_software_aliases": str(
                PIPELINE_ROOT / "assets" / "external_software_aliases.json"
            ),
        }
    )
    mineru = config["stage04"]["mineru"]
    mineru.update(
        {
            "enabled": True,
            "managed_gpu": True,
            "gpu_env_dir": str(PIPELINE_ROOT / ".envs" / "researchchem-data-pipeline"),
            "command": str(
                PIPELINE_ROOT / ".envs" / "researchchem-data-pipeline" / "bin" / "mineru"
            ),
            "api_concurrency": args.stage04_concurrency,
            "request_batch_size": 1,
            "reuse_existing": True,
            "extra_args": ["--formula", "true", "--table", "true"],
            "environment": {
                "MINERU_TOOLS_CONFIG_JSON": str(
                    PIPELINE_ROOT / ".model_cache" / "mineru" / "mineru.json"
                )
            },
        }
    )
    for role in ("suitability", "builder", "judge"):
        config["models"][role] = {"enabled": False}
    screening = config["models"]["screening"]
    screening.update(
        {
            "enabled": True,
            "managed_rlaunch": True,
            "preserve_worker_on_exit": True,
            "allow_worker_creation": False,
            "existing_worker": args.existing_worker,
            "manager_script": str(
                PIPELINE_ROOT / "scripts" / "stage03_llm" / "manage_rlaunch_worker.sh"
            ),
            "state_file": str(run_root / ".screening_llm_worker.local.json"),
            "base_url": "http://127.0.0.1:18083/v1",
            "api_key_env": "RCB_SCREENING_API_KEY",
            "model": "qwen3-30b-a3b-instruct-2507",
            "workers": 32,
            "max_tokens": 6144,
            "context_window_tokens": 16384,
            "context_safety_margin_tokens": 768,
            "timeout_seconds": 900,
            "retries": 2,
            "thinking": "disabled",
            "cpu": 16,
            "memory_mib": args.worker_memory_mib,
            "charged_group": "ai4chem_gpu",
            "positive_tag": args.worker_positive_tag,
            "image": "",
            "skip_bootstrap": True,
            "skip_download": True,
        }
    )
    config["microbatch"] = {
        "enabled": True,
        "size": args.microbatch_size,
        "concurrency": 16,
        "buffer_size": 16,
        "stage_concurrency": {
            "stage01": 8,
            "stage02": 16,
            "stage03": 16,
            "stage04": args.stage04_concurrency,
            "stage05": 1,
        },
        "resume": True,
    }
    return config


def _sandbox_manager(run_root, template, args, *, cleanup: str) -> SandboxManager:
    sandbox_template = template.get("execution", {}).get("sandbox", {})
    return SandboxManager(
        SandboxRunOptions(
            cpu=args.sandbox_cpu,
            memory=args.sandbox_memory,
            lifecycle_minutes=1440,
            startup_timeout_seconds=args.sandbox_startup_timeout_seconds,
            cleanup=cleanup,
            source=run_root / ".sandboxes.local.yaml",
            inventory=run_root / ".sandbox_inventory.local.json",
            base_url=str(sandbox_template.get("base_url") or "https://h.pjlab.org.cn/brainbox"),
            project=str(sandbox_template.get("project") or "ailab-ai4chem"),
            image=str(sandbox_template.get("image") or ""),
            api_key_env="RCB_SANDBOX_API_KEY",
        )
    )


def _start_single_sandbox(run_root, template, args, status_path, status) -> None:
    status.update({"state": "starting_single_sandbox", "updated_at": _now()})
    write_json(status_path, status)
    worker = _sandbox_manager(run_root, template, args, cleanup="keep").ensure()
    status.update(
        {
            "sandbox_started_at": _now(),
            "sandbox_id": worker.sandbox_id,
            "sandbox_state": worker.state,
            "updated_at": _now(),
        }
    )
    write_json(status_path, status)


def _cleanup_shared_resources(run_root, template, args, status) -> None:
    cleanup_errors = []
    manager = PIPELINE_ROOT / "scripts" / "stage03_llm" / "manage_rlaunch_worker.sh"
    worker_state = run_root / ".screening_llm_worker.local.json"
    result = subprocess.run(
        ["bash", str(manager), "stop", "--state", str(worker_state)],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode:
        cleanup_errors.append((result.stderr or result.stdout or "worker cleanup failed").strip())
    try:
        _sandbox_manager(run_root, template, args, cleanup="stop").stop()
    except Exception as exc:
        cleanup_errors.append(f"sandbox cleanup: {type(exc).__name__}: {exc}")
    status["cleanup_errors"] = cleanup_errors
    status["resources_released_at"] = _now()


def _record_completed(status, index: int, result: dict[str, Any], *, resumed: bool) -> None:
    completed = set(int(value) for value in status.get("completed_batches") or [])
    completed.add(index)
    status["completed_batches"] = sorted(completed)
    rows = [
        row for row in status.get("batch_results") or [] if int(row.get("batch") or 0) != index
    ]
    rows.append(
        {
            "batch": index,
            "status": result.get("status"),
            "workspace": result.get("workspace"),
            "run_id": result.get("run_id"),
            "resumed": resumed,
            "stage00": result.get("stage00"),
            "stage01": result.get("stage01"),
            "stage02": result.get("stage02"),
            "stage03": result.get("stage03"),
            "stage04": result.get("stage04"),
            "completed_at": _now(),
        }
    )
    status["batch_results"] = sorted(rows, key=lambda row: int(row["batch"]))
    status["updated_at"] = _now()


def _completed_summary(path: Path) -> bool:
    if not path.is_file():
        return False
    summary = read_json(path)
    return summary.get("status") == "completed" and summary.get("stop_after") == "stage04"


def _initial_status(args, run_root: Path, batches: int) -> dict[str, Any]:
    return {
        "state": "initializing",
        "run_root": str(run_root),
        "total_papers": args.total,
        "batch_size": args.batch_size,
        "batches": batches,
        "stage04_api_concurrency": args.stage04_concurrency,
        "worker_memory_mib": args.worker_memory_mib,
        "worker_positive_tag": args.worker_positive_tag,
        "existing_worker": args.existing_worker,
        "initial_delay_hours": args.initial_delay_hours,
        "sandbox_startup_timeout_seconds": args.sandbox_startup_timeout_seconds,
        "resource_start_order": ["sandbox", "screening_worker"],
        "worker_start_policy": "single_attempt_fail_fast",
        "completed_batches": [],
        "batch_results": [],
        "current_batch": None,
        "started_at": _now(),
        "updated_at": _now(),
    }


def _parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--template", default=str(DEFAULT_TEMPLATE))
    parser.add_argument("--run-root", required=True)
    parser.add_argument("--total", type=int, default=10000)
    parser.add_argument("--batch-size", type=int, default=1000)
    parser.add_argument("--dataset", default="en-paper-hzzj")
    parser.add_argument(
        "--credentials",
        default="/mnt/shared-storage-user/liyuqiang/benchmark/pipline_demo/pdfs/xinghe.txt",
    )
    parser.add_argument("--seed", type=int, default=20260811)
    parser.add_argument("--microbatch-size", type=int, default=10)
    parser.add_argument("--stage04-concurrency", type=int, default=8)
    parser.add_argument("--worker-memory-mib", type=int, default=16000)
    parser.add_argument("--worker-positive-tag", default="")
    parser.add_argument(
        "--existing-worker",
        default="",
        help="Reuse this full worker SSH target instead of calling rlaunch",
    )
    parser.add_argument("--sandbox-cpu", type=int, default=64)
    parser.add_argument("--sandbox-memory", default="128Gi")
    parser.add_argument("--sandbox-startup-timeout-seconds", type=int, default=14400)
    parser.add_argument("--initial-delay-hours", type=float, default=5.0)
    parser.add_argument("--prepare-only", action="store_true")
    return parser.parse_args()


def _validate_args(args) -> None:
    for name in (
        "total",
        "batch_size",
        "microbatch_size",
        "stage04_concurrency",
        "worker_memory_mib",
        "sandbox_cpu",
    ):
        if int(getattr(args, name)) < 1:
            raise ValueError(f"--{name.replace('_', '-')} must be positive")
    if not Path(args.credentials).expanduser().is_file():
        raise FileNotFoundError(f"remote credentials not found: {args.credentials}")
    if args.initial_delay_hours < 0:
        raise ValueError("--initial-delay-hours must be zero or greater")
    if args.sandbox_startup_timeout_seconds < 60:
        raise ValueError("--sandbox-startup-timeout-seconds must be at least 60")


def _wait_before_resource_start(hours: float, status_path: Path, status: dict[str, Any]) -> None:
    seconds = hours * 3600
    if seconds <= 0:
        return
    resource_start_after = datetime.now(timezone.utc) + timedelta(seconds=seconds)
    status.update(
        {
            "state": "waiting_for_resource_start",
            "resource_start_after": resource_start_after.isoformat(),
            "updated_at": _now(),
        }
    )
    write_json(status_path, status)
    print(
        f"waiting {hours:g} hours before starting the sandbox and single GPU worker; "
        f"resource start after {resource_start_after.isoformat()}",
        flush=True,
    )
    time.sleep(seconds)


def _start_single_worker(
    config_path: Path, status_path: Path, status: dict[str, Any]
) -> None:
    screening = dict(load_config(config_path)["models"]["screening"])
    state_file = Path(str(screening["state_file"]))
    if state_file.exists():
        raise RuntimeError(
            f"refusing to create a worker while stale worker state exists: {state_file}"
        )
    status.update({"state": "starting_single_worker", "updated_at": _now()})
    write_json(status_path, status)
    screening["allow_worker_creation"] = True
    ensure_managed_screening_worker(screening)
    status.update({"worker_started_at": _now(), "updated_at": _now()})
    write_json(status_path, status)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


if __name__ == "__main__":
    raise SystemExit(main())
