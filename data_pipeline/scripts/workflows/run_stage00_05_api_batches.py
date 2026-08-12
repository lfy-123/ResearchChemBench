#!/usr/bin/env python3
"""Run Stage00-05 in sequential batches using API-hosted LLMs only."""

from __future__ import annotations

import argparse
import copy
import json
import os
import signal
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.contracts import read_json, write_json
from src.integrations.llm_client import call_json_chat
from src.pipeline import run_pipeline
from src.sandbox.manager import DEFAULT_IMAGE, SandboxManager, SandboxRunOptions

PIPELINE_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_TEMPLATE = PIPELINE_ROOT / "config.example.json"
DEFAULT_API_BASE_URL = "http://127.0.0.1:13000/v1"
DEFAULT_MODELS = {
    "stage02_screening": "Qwen3.6-27B",
    "stage03_screening": "DeepSeek-V4-Flash",
    "stage05_router": "DeepSeek-V4-Flash-DSpark",
    "suitability": "DeepSeek-V4-Flash",
}


def main() -> int:
    args = _parse_args()
    _validate_args(args)
    api_key = os.environ.get(args.api_key_env, "") or os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise RuntimeError(
            f"missing API key environment variable: {args.api_key_env} or OPENAI_API_KEY"
        )
    os.environ[args.api_key_env] = api_key
    _preflight_api(args.api_base_url, api_key, DEFAULT_MODELS)

    run_root = Path(args.run_root).expanduser().resolve()
    run_root.mkdir(parents=True, exist_ok=True)
    template = json.loads(Path(args.template).expanduser().resolve().read_text(encoding="utf-8"))
    batches = (args.total + args.batch_size - 1) // args.batch_size
    status_path = run_root / "batch_status.json"
    status = _initial_status(args, run_root, batches)
    if status_path.is_file():
        previous = read_json(status_path)
        status["first_started_at"] = previous.get("first_started_at") or previous.get(
            "started_at"
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
        status.update({"state": "prepared", "finished_at": _now(), "updated_at": _now()})
        write_json(status_path, status)
        print(f"prepared {len(configs)} API-only batch configs under {run_root}", flush=True)
        return 0

    interrupted = False

    def interrupt(_signum, _frame):
        nonlocal interrupted
        interrupted = True
        raise KeyboardInterrupt

    signal.signal(signal.SIGTERM, interrupt)
    signal.signal(signal.SIGINT, interrupt)
    try:
        _start_single_sandbox(run_root, template, args, status_path, status)
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
                f"starting API-only batch {index}/{batches}: "
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
        _stop_sandbox(run_root, template, args, status)
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
            "run_id": f"stage00-05-api-batch-{batch_index + 1:04d}",
            "stop_after": "stage05",
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
    config["execution"]["backend"] = "sandbox"
    config["execution"]["sandbox"].update(
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
    config["stage01"]["package"].update({"workers": 32, "network_workers": 32})
    config["stage01"]["normalization"]["grobid"].update(
        {"workers": 32, "reuse_existing": True}
    )
    config["stage02"].update({"model_role": "stage02_screening", "workers": 8})
    config["stage03"].update(
        {
            "model_role": "stage03_screening",
            "workers": 8,
            "toolbox_capabilities": str(PIPELINE_ROOT / "assets/toolbox_capabilities.json"),
            "software_aliases": str(PIPELINE_ROOT / "assets/software_aliases.json"),
            "external_software_aliases": str(
                PIPELINE_ROOT / "assets" / "external_software_aliases.json"
            ),
        }
    )
    config["stage04"]["mineru"].update(
        {
            "enabled": True,
            "managed_gpu": False,
            "command": str(
                PIPELINE_ROOT / ".envs" / "researchchem-data-pipeline" / "bin" / "mineru"
            ),
            "api_concurrency": max(
                1,
                int(args.stage04_api_concurrency)
                // max(1, int(args.stage04_microbatch_concurrency)),
            ),
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
    config["stage05"].update(
        {
            "model_role": "suitability",
            "router_model_role": "stage05_router",
            "workers": args.stage05_workers,
        }
    )
    config["models"]["screening"].update(
        {
            "enabled": False,
            "managed_rlaunch": False,
            "preserve_worker_on_exit": False,
            "allow_worker_creation": False,
        }
    )
    config["models"]["stage02_screening"] = _api_model_config(
        args,
        role="stage02_screening",
        model=DEFAULT_MODELS["stage02_screening"],
        workers=args.stage02_workers,
        max_tokens=2048,
        chat_template_kwargs={"enable_thinking": False},
    )
    config["models"]["stage03_screening"] = _api_model_config(
        args,
        role="stage03_screening",
        model=DEFAULT_MODELS["stage03_screening"],
        workers=args.stage03_workers,
        max_tokens=6144,
        chat_template_kwargs={"thinking": False},
    )
    config["models"]["stage05_router"] = _api_model_config(
        args,
        role="stage05_router",
        model=DEFAULT_MODELS["stage05_router"],
        workers=args.stage05_workers,
        max_tokens=3072,
        chat_template_kwargs={"thinking": False},
    )
    config["models"]["suitability"] = _api_model_config(
        args,
        role="stage05_auditor",
        model=DEFAULT_MODELS["suitability"],
        workers=args.stage05_workers,
        max_tokens=16000,
        chat_template_kwargs={"thinking": False},
    )
    config["models"]["builder"] = {"enabled": False}
    config["models"]["judge"] = {"enabled": False}
    config["microbatch"] = {
        "enabled": True,
        "size": args.microbatch_size,
        "concurrency": args.microbatch_concurrency,
        "buffer_size": args.microbatch_concurrency,
        "stage_concurrency": {
            "stage01": 8,
            "stage02": args.stage02_workers,
            "stage03": args.stage03_workers,
            "stage04": args.stage04_microbatch_concurrency,
            "stage05": args.stage05_workers,
        },
        "resume": True,
    }
    return config


def _api_model_config(args, *, role, model, workers, max_tokens, chat_template_kwargs):
    return {
        "enabled": True,
        "use_proxy": False,
        "base_url": args.api_base_url,
        "base_url_env": "RCB_NEW_API_BASE_URL",
        "api_key_env": args.api_key_env,
        "model": model,
        "model_env": f"RCB_NEW_{role.upper()}_MODEL",
        "workers": workers,
        "max_tokens": max_tokens,
        "timeout_seconds": 1200,
        "retries": 3,
        "thinking": None,
        "chat_template_kwargs": chat_template_kwargs,
    }


def _preflight_api(base_url: str, api_key: str, models: dict[str, str]) -> None:
    request = urllib.request.Request(
        f"{base_url.rstrip('/')}/models",
        headers={"Authorization": f"Bearer {api_key}"},
    )
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    try:
        with opener.open(request, timeout=15) as response:
            payload = json.load(response)
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")[:500]
        raise RuntimeError(f"New API preflight HTTP {exc.code}: {body}") from exc
    available = {str(row.get("id")) for row in payload.get("data") or []}
    missing = sorted(set(models.values()) - available)
    if missing:
        raise RuntimeError(f"New API does not expose configured models: {missing}")
    probes = (
        (models["stage02_screening"], {"enable_thinking": False}),
        (models["stage03_screening"], {"thinking": False}),
        (models["stage05_router"], {"thinking": False}),
    )
    for model, template_kwargs in probes:
        response, _audit = call_json_chat(
            model=model,
            base_url=base_url,
            api_key=api_key,
            system_prompt="Return one JSON object only.",
            user_content='Return {"status":"ok"}.',
            timeout_seconds=120,
            max_tokens=128,
            retries=2,
            chat_template_kwargs=template_kwargs,
            proxy_url="",
        )
        if response.get("status") != "ok":
            raise RuntimeError(f"New API probe returned an invalid response for {model}")
    print(
        "New API preflight passed: " + ", ".join(dict.fromkeys(models.values())),
        flush=True,
    )


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
            image=str(sandbox_template.get("image") or DEFAULT_IMAGE),
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


def _stop_sandbox(run_root, template, args, status) -> None:
    try:
        _sandbox_manager(run_root, template, args, cleanup="stop").stop()
        status["sandbox_released_at"] = _now()
    except Exception as exc:
        status["cleanup_errors"] = [f"sandbox cleanup: {type(exc).__name__}: {exc}"]


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
            **{f"stage{stage:02d}": result.get(f"stage{stage:02d}") for stage in range(6)},
            "completed_at": _now(),
        }
    )
    status["batch_results"] = sorted(rows, key=lambda row: int(row["batch"]))
    status["updated_at"] = _now()


def _completed_summary(path: Path) -> bool:
    if not path.is_file():
        return False
    summary = read_json(path)
    return summary.get("status") == "completed" and summary.get("stop_after") == "stage05"


def _initial_status(args, run_root: Path, batches: int) -> dict[str, Any]:
    return {
        "state": "initializing",
        "execution_mode": "api_only_no_worker",
        "run_root": str(run_root),
        "total_papers": args.total,
        "batch_size": args.batch_size,
        "batches": batches,
        "api_base_url": args.api_base_url,
        "models": DEFAULT_MODELS,
        "sandbox_cpu": args.sandbox_cpu,
        "sandbox_memory": args.sandbox_memory,
        "stage04_microbatch_concurrency": args.stage04_microbatch_concurrency,
        "stage04_api_concurrency": args.stage04_api_concurrency,
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
    parser.add_argument("--seed", type=int, default=20260813)
    parser.add_argument(
        "--api-base-url",
        default=os.environ.get("RCB_NEW_API_BASE_URL")
        or os.environ.get("OPENAI_BASE_URL")
        or DEFAULT_API_BASE_URL,
    )
    parser.add_argument("--api-key-env", default="RCB_NEW_API_KEY")
    parser.add_argument("--microbatch-size", type=int, default=10)
    parser.add_argument("--microbatch-concurrency", type=int, default=8)
    parser.add_argument("--stage02-workers", type=int, default=8)
    parser.add_argument("--stage03-workers", type=int, default=8)
    parser.add_argument("--stage04-microbatch-concurrency", type=int, default=1)
    parser.add_argument("--stage04-api-concurrency", type=int, default=8)
    parser.add_argument("--stage05-workers", type=int, default=8)
    parser.add_argument("--sandbox-cpu", type=int, default=64)
    parser.add_argument("--sandbox-memory", default="128Gi")
    parser.add_argument("--sandbox-startup-timeout-seconds", type=int, default=14400)
    parser.add_argument("--prepare-only", action="store_true")
    return parser.parse_args()


def _validate_args(args) -> None:
    for name in (
        "total",
        "batch_size",
        "microbatch_size",
        "microbatch_concurrency",
        "stage02_workers",
        "stage03_workers",
        "stage04_microbatch_concurrency",
        "stage04_api_concurrency",
        "stage05_workers",
        "sandbox_cpu",
    ):
        if int(getattr(args, name)) < 1:
            raise ValueError(f"--{name.replace('_', '-')} must be positive")
    if not Path(args.credentials).expanduser().is_file():
        raise FileNotFoundError(f"remote credentials not found: {args.credentials}")
    if args.sandbox_startup_timeout_seconds < 60:
        raise ValueError("--sandbox-startup-timeout-seconds must be at least 60")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


if __name__ == "__main__":
    raise SystemExit(main())
