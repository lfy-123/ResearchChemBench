#!/usr/bin/env python3
"""Run Stage00-03 or Stage00-05 in sequential batches using API-hosted LLMs."""

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
    "suitability": "<selected-at-preflight>",
}
DEFAULT_STAGE02_FALLBACKS = (
    "DeepSeek-V4-Flash",
    "Kimi-K2.6",
)
DEFAULT_STAGE03_FALLBACKS = (
    "GLM-5.2",
    "Qwen3.6-27B",
)
DEFAULT_STAGE05_ROUTER_FALLBACKS = (
    "DeepSeek-V4-Flash",
    "Qwen3.6-27B",
)
DEFAULT_STAGE05_AUDITOR_CANDIDATES = (
    "DeepSeek-V4-Pro",
    "GLM-5.2",
    "Nex-N2-Pro",
    "Nex-N2-Pro-w8a8",
    "MiniMax-M2.7",
)
STAGE02_CLASSIFICATION_MAX_TOKENS = 12288
STAGE02_VERIFICATION_MAX_TOKENS = 6144
STAGE03_MAX_TOKENS = 12288
SCREENING_CONTEXT_WINDOW_TOKENS = 32768
SCREENING_CONTEXT_SAFETY_MARGIN_TOKENS = 2048


def main() -> int:
    args = _parse_args()
    _validate_args(args)
    api_key = os.environ.get(args.api_key_env, "") or os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise RuntimeError(
            f"missing API key environment variable: {args.api_key_env} or OPENAI_API_KEY"
        )
    os.environ[args.api_key_env] = api_key
    stop_index = int(args.stop_after.replace("stage", ""))
    fixed_models = {
        key: value
        for key, value in DEFAULT_MODELS.items()
        if key in {"stage02_screening", "stage03_screening"}
        or (stop_index >= 5 and key == "stage05_router")
    }
    fallback_names = {
        *DEFAULT_STAGE02_FALLBACKS,
        *DEFAULT_STAGE03_FALLBACKS,
        *(DEFAULT_STAGE05_ROUTER_FALLBACKS if stop_index >= 5 else ()),
    }
    _preflight_api(args.api_base_url, api_key, fixed_models, fallback_names=fallback_names)
    auditor_preflight: list[dict[str, Any]] = []
    models = dict(fixed_models)
    if stop_index >= 5:
        candidates = tuple(
            item.strip()
            for item in args.stage05_auditor_candidates.split(",")
            if item.strip()
        )
        auditor_preflight = _probe_model_candidates(
            args.api_base_url,
            api_key,
            candidates,
            attempts=args.stage05_auditor_probe_attempts,
        )
        usable = [row["model"] for row in auditor_preflight if row["usable"]]
        if not usable:
            raise RuntimeError("no Stage05B auditor candidate passed API preflight")
        args.stage05_auditor_candidates_resolved = tuple(usable)
        args.stage05_auditor_model = usable[0]
        args.stage05_auditor_chat_template_kwargs = _model_chat_template_kwargs(
            usable[0], thinking=True
        )
        models["suitability"] = usable[0]
        print(
            "Stage05B runtime model chain: " + " -> ".join(usable),
            flush=True,
        )

    run_root = Path(args.run_root).expanduser().resolve()
    run_root.mkdir(parents=True, exist_ok=True)
    template = json.loads(Path(args.template).expanduser().resolve().read_text(encoding="utf-8"))
    batches = (args.total + args.batch_size - 1) // args.batch_size
    status_path = run_root / "batch_status.json"
    status = _initial_status(args, run_root, batches, models, auditor_preflight)
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
            completed_result = _completed_result(workspace, summary_path, args.stop_after)
            if completed_result is not None:
                _record_completed(status, index, completed_result, resumed=True)
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
                f"starting API-only {args.stop_after} batch {index}/{batches}: "
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
    stop_after = getattr(args, "stop_after", "stage05")
    config.update(
        {
            "workspace": str(workspace),
            "run_id": f"stage00-{stop_after[-2:]}-api-batch-{batch_index + 1:04d}",
            "stop_after": stop_after,
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
    config["stage02"].update(
        {
            "model_role": "stage02_screening",
            "workers": args.stage02_workers,
            "classification_max_tokens": STAGE02_CLASSIFICATION_MAX_TOKENS,
            "pass_verification_max_tokens": STAGE02_VERIFICATION_MAX_TOKENS,
        }
    )
    config["stage03"].update(
        {
            "model_role": "stage03_screening",
            "workers": args.stage03_workers,
            "max_tokens": STAGE03_MAX_TOKENS,
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
            "auditor_max_tokens": args.stage05_auditor_max_tokens,
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
        max_tokens=STAGE02_CLASSIFICATION_MAX_TOKENS,
        context_window_tokens=SCREENING_CONTEXT_WINDOW_TOKENS,
        context_safety_margin_tokens=SCREENING_CONTEXT_SAFETY_MARGIN_TOKENS,
        chat_template_kwargs=_model_chat_template_kwargs(
            DEFAULT_MODELS["stage02_screening"], thinking=True
        ),
        fallback_models=_fallback_model_configs(
            DEFAULT_STAGE02_FALLBACKS,
            max_tokens=STAGE02_CLASSIFICATION_MAX_TOKENS,
            thinking=True,
        ),
    )
    config["models"]["stage03_screening"] = _api_model_config(
        args,
        role="stage03_screening",
        model=DEFAULT_MODELS["stage03_screening"],
        workers=args.stage03_workers,
        max_tokens=STAGE03_MAX_TOKENS,
        context_window_tokens=SCREENING_CONTEXT_WINDOW_TOKENS,
        context_safety_margin_tokens=SCREENING_CONTEXT_SAFETY_MARGIN_TOKENS,
        chat_template_kwargs=_model_chat_template_kwargs(
            DEFAULT_MODELS["stage03_screening"], thinking=True
        ),
        fallback_models=_fallback_model_configs(
            DEFAULT_STAGE03_FALLBACKS,
            max_tokens=STAGE03_MAX_TOKENS,
            thinking=True,
        ),
    )
    if int(stop_after.replace("stage", "")) >= 5:
        config["models"]["stage05_router"] = _api_model_config(
            args,
            role="stage05_router",
            model=DEFAULT_MODELS["stage05_router"],
            workers=args.stage05_workers,
            max_tokens=3072,
            chat_template_kwargs={"thinking": False},
            fallback_models=_fallback_model_configs(
                DEFAULT_STAGE05_ROUTER_FALLBACKS,
                max_tokens=4096,
                thinking=False,
            ),
        )
        config["models"]["suitability"] = _api_model_config(
            args,
            role="stage05_auditor",
            model=args.stage05_auditor_model,
            workers=args.stage05_workers,
            max_tokens=args.stage05_auditor_max_tokens,
            chat_template_kwargs=_model_chat_template_kwargs(
                getattr(
                    args,
                    "stage05_auditor_candidates_resolved",
                    (args.stage05_auditor_model,),
                )[0],
                thinking=True,
            ),
            fallback_models=[
                _model_candidate_config(model, max_tokens=args.stage05_auditor_max_tokens, thinking=True)
                for model in getattr(args, "stage05_auditor_candidates_resolved", ())[1:]
            ],
        )
    else:
        config["models"]["stage05_router"] = {"enabled": False}
        config["models"]["suitability"] = {"enabled": False}
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


def _api_model_config(
    args,
    *,
    role,
    model,
    workers,
    max_tokens,
    chat_template_kwargs,
    fallback_models=None,
    context_window_tokens=None,
    context_safety_margin_tokens=None,
):
    config = {
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
        "fallback_models": list(fallback_models or []),
    }
    if context_window_tokens is not None:
        config["context_window_tokens"] = int(context_window_tokens)
    if context_safety_margin_tokens is not None:
        config["context_safety_margin_tokens"] = int(context_safety_margin_tokens)
    return config


def _fallback_model_configs(models, *, max_tokens: int, thinking: bool):
    return [
        _model_candidate_config(model, max_tokens=max_tokens, thinking=thinking)
        for model in models
    ]


def _model_candidate_config(model: str, *, max_tokens: int, thinking: bool):
    return {
        "model": model,
        "max_tokens": max_tokens,
        "chat_template_kwargs": _model_chat_template_kwargs(model, thinking=thinking),
    }


def _preflight_api(
    base_url: str,
    api_key: str,
    models: dict[str, str],
    *,
    fallback_names: set[str] | None = None,
) -> None:
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
    missing = sorted((set(models.values()) | set(fallback_names or ())) - available)
    if missing:
        raise RuntimeError(f"New API does not expose configured models: {missing}")
    probes = [
        (models["stage02_screening"], {"enable_thinking": False}),
        (models["stage03_screening"], {"thinking": False}),
    ]
    if "stage05_router" in models:
        probes.append((models["stage05_router"], {"thinking": False}))
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


def _select_stage05_auditor(
    base_url: str,
    api_key: str,
    candidates: tuple[str, ...],
    *,
    attempts: int,
    caller=call_json_chat,
) -> tuple[str, list[dict[str, Any]]]:
    if not candidates:
        raise ValueError("at least one Stage05B auditor candidate is required")
    audit: list[dict[str, Any]] = []
    for model in candidates:
        outcomes = []
        for attempt in range(1, attempts + 1):
            try:
                response, _metadata = caller(
                    model=model,
                    base_url=base_url,
                    api_key=api_key,
                    system_prompt="Return one valid JSON object only.",
                    user_content=(
                        'Return {"decision":"pass","reason":"preflight",'
                        '"checks":["workflow","software","cost"]}.'
                    ),
                    timeout_seconds=120,
                    max_tokens=256,
                    retries=0,
                    chat_template_kwargs=_model_chat_template_kwargs(model),
                    proxy_url="",
                )
                valid = response.get("decision") == "pass" and isinstance(
                    response.get("checks"), list
                )
                outcomes.append({"attempt": attempt, "ok": valid})
                if not valid:
                    break
            except Exception as exc:
                outcomes.append(
                    {
                        "attempt": attempt,
                        "ok": False,
                        "error": f"{type(exc).__name__}: {exc}"[:500],
                    }
                )
                break
        selected = len(outcomes) == attempts and all(row["ok"] for row in outcomes)
        audit.append({"model": model, "selected": selected, "outcomes": outcomes})
        if selected:
            return model, audit
    raise RuntimeError(
        "no strong Stage05B auditor passed consecutive API probes: "
        + ", ".join(candidates)
    )


def _probe_model_candidates(
    base_url: str,
    api_key: str,
    candidates: tuple[str, ...],
    *,
    attempts: int,
    caller=call_json_chat,
) -> list[dict[str, Any]]:
    """Probe every candidate so runtime can preserve an ordered fallback chain."""

    audit: list[dict[str, Any]] = []
    for model in candidates:
        outcomes: list[dict[str, Any]] = []
        for attempt in range(1, attempts + 1):
            try:
                response, _metadata = caller(
                    model=model,
                    base_url=base_url,
                    api_key=api_key,
                    system_prompt="Return one valid JSON object only.",
                    user_content=(
                        'Return {"decision":"pass","reason":"preflight",'
                        '"checks":["workflow","software","cost"]}.'
                    ),
                    timeout_seconds=120,
                    max_tokens=512,
                    retries=0,
                    chat_template_kwargs=_model_chat_template_kwargs(model, thinking=False),
                    proxy_url="",
                )
                valid = response.get("decision") == "pass" and isinstance(
                    response.get("checks"), list
                )
                outcomes.append({"attempt": attempt, "ok": valid})
                if not valid:
                    break
            except Exception as exc:
                outcomes.append(
                    {
                        "attempt": attempt,
                        "ok": False,
                        "error": f"{type(exc).__name__}: {exc}"[:500],
                    }
                )
                break
        audit.append(
            {
                "model": model,
                "usable": len(outcomes) == attempts and all(row["ok"] for row in outcomes),
                "outcomes": outcomes,
            }
        )
    return audit


def _model_chat_template_kwargs(
    model: str, *, thinking: bool = False
) -> dict[str, bool] | None:
    normalized = model.casefold()
    if normalized.startswith("deepseek"):
        # This gateway returns reasoning-only messages with empty content when
        # DeepSeek thinking is enabled, which cannot satisfy the JSON contract.
        return {"thinking": False}
    if normalized in {"glm-5.2", "nex-n2-pro", "qwen3.6-27b"}:
        return {"enable_thinking": thinking}
    if normalized == "kimi-k2.6":
        return {"thinking": thinking}
    return None


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
            **{
                f"stage{stage:02d}": result.get(f"stage{stage:02d}")
                for stage in range(int(str(result.get("stop_after", "stage05"))[-2:]) + 1)
            },
            "completed_at": _now(),
        }
    )
    status["batch_results"] = sorted(rows, key=lambda row: int(row["batch"]))
    status["updated_at"] = _now()


def _completed_summary(path: Path, stop_after: str) -> bool:
    if not path.is_file():
        return False
    summary = read_json(path)
    return summary.get("status") == "completed" and summary.get("stop_after") == stop_after


def _completed_result(
    workspace: Path, summary_path: Path, stop_after: str
) -> dict[str, Any] | None:
    if _completed_summary(summary_path, stop_after):
        return read_json(summary_path)
    if stop_after != "stage03":
        return None
    stage_paths = {
        "stage00": workspace / "stage_00_remote_corpus" / "stage_summary.json",
        "stage01": workspace / "stage_01_document_preparation" / "stage_summary.json",
        "stage02": workspace / "stage_02_computational_content" / "stage_summary.json",
        "stage03": workspace / "stage_03_toolbox_resource_gate" / "stage_summary.json",
    }
    if any(not path.is_file() for path in stage_paths.values()):
        return None
    summaries = {stage: read_json(path) for stage, path in stage_paths.items()}
    if any(int(summary.get("processing_errors") or 0) for summary in summaries.values()):
        return None
    result = {
        "run_id": summaries["stage03"].get("run_id"),
        "workspace": str(workspace),
        "status": "completed",
        "stop_after": "stage03",
        **summaries,
        "resumed_from_existing_stage_outputs": True,
    }
    write_json(summary_path, result)
    return result


def _initial_status(
    args,
    run_root: Path,
    batches: int,
    models: dict[str, str],
    auditor_preflight: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "state": "initializing",
        "execution_mode": "api_only_no_worker",
        "stop_after": args.stop_after,
        "run_root": str(run_root),
        "total_papers": args.total,
        "batch_size": args.batch_size,
        "batches": batches,
        "api_base_url": args.api_base_url,
        "models": models,
        "stage05_auditor_preflight": auditor_preflight,
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
    parser.add_argument("--stop-after", choices=("stage03", "stage05"), default="stage05")
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
    parser.add_argument("--stage05-auditor-max-tokens", type=int, default=8192)
    parser.add_argument(
        "--stage05-auditor-candidates",
        default=",".join(DEFAULT_STAGE05_AUDITOR_CANDIDATES),
    )
    parser.add_argument("--stage05-auditor-probe-attempts", type=int, default=3)
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
        "stage05_auditor_max_tokens",
        "stage05_auditor_probe_attempts",
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
