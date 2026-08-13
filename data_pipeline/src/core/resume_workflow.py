from __future__ import annotations

import copy
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

from src.config import load_config
from src.contracts import canonical_hash
from src.core.io import merge_dict, write_json
from src.core.resume import ResumeStateStore
from src.core.resume import scientific_stage_fingerprints
from src.core.resume_importer import import_legacy_run, reconcile_dependencies
from src.core.run_lease import RunLease
from src.pipeline import run_pipeline


STAGES = tuple(f"stage{index:02d}" for index in range(6))
CHILD_STAGES = {
    "stage01": ("stage01_package", "stage01"),
    "stage05": ("stage05_router", "stage05_auditor", "stage05"),
}


@dataclass(frozen=True)
class BatchSpec:
    batch_id: str
    index: int
    target_slot_start: int
    count: int
    config_path: Path
    workspace: Path
    is_new: bool


def prepare_resume(
    *,
    run_root: str | Path,
    total: int,
    batch_size: int,
    template_path: str | Path | None = None,
    start_stage: str = "stage00",
    stop_stage: str = "stage05",
    batch_ids: Iterable[str] = (),
    pending_only: bool = False,
    retry_only: bool = False,
    materialize_expansion: bool = True,
) -> tuple[ResumeStateStore, list[BatchSpec], dict[str, Any]]:
    root = Path(run_root).expanduser().resolve()
    _validate_stage_range(start_stage, stop_stage)
    if total < 1 or batch_size < 1:
        raise ValueError("--total and --batch-size must be positive")
    root.mkdir(parents=True, exist_ok=True)
    store = ResumeStateStore.for_run_root(root)
    migration = import_legacy_run(root, store)
    reconcile_dependencies(root, store, stop_stage=stop_stage)
    old_target = _configured_target(root, store)
    if total < old_target:
        raise ValueError(
            f"--total {total} is smaller than the frozen cumulative target {old_target}"
        )
    new_specs: list[BatchSpec] = []
    if total > old_target and (pending_only or retry_only):
        mode = "--pending-only" if pending_only else "--retry-only"
        raise ValueError(f"{mode} cannot expand --total beyond {old_target}")
    if total > old_target:
        new_specs = append_batches(
            root,
            old_target=old_target,
            total=total,
            batch_size=batch_size,
            template_path=template_path,
            write_configs=materialize_expansion,
        )
        # Empty batches have no artifacts to import; Stage00 will create their
        # ledger entries transactionally during execution.
    specs = discover_batches(root, old_target=old_target, new_specs=new_specs)
    requested = {_normalize_batch_id(value) for value in batch_ids}
    if requested:
        missing = requested - {item.batch_id for item in specs}
        if missing:
            raise ValueError(f"unknown --batch values: {sorted(missing)}")
        specs = [item for item in specs if item.batch_id in requested]
    plan = {
        "run_root": str(root),
        "database": str(store.database),
        "previous_target": old_target,
        "requested_total": total,
        "new_target_slots": max(0, total - old_target),
        "new_batches": [item.batch_id for item in new_specs],
        "selected_batches": [item.batch_id for item in specs],
        "stage_range": [start_stage, stop_stage],
        "migration": migration,
        "work": store.work_counts(start_stage=start_stage, stop_stage=stop_stage),
    }
    write_json(store.root / "resume_plan.json", plan)
    return store, specs, plan


def execute_resume(
    *,
    store: ResumeStateStore,
    specs: list[BatchSpec],
    total: int,
    start_stage: str,
    stop_stage: str,
    retry_only: bool,
    invalidated_stages: Iterable[str],
    resume_config: str,
    runtime_overrides: dict[str, Any] | None,
    command_digest: str,
) -> dict[str, Any]:
    invalidated = expanded_invalidation(invalidated_stages)
    generation = store.create_generation(
        command_hash=command_digest,
        total_target=total,
        start_stage=start_stage,
        stop_stage=stop_stage,
        invalidated_stages=invalidated,
    )
    generation_status = "failed"
    results: list[dict[str, Any]] = []
    try:
        runtime_configs = [
            materialize_runtime_config(
                store=store,
                spec=spec,
                generation=generation,
                stop_stage=stop_stage,
                resume_config=resume_config,
                runtime_overrides=runtime_overrides or {},
            )
            for spec in specs
        ]
        for spec, config_path in zip(specs, runtime_configs, strict=True):
            fingerprints = scientific_stage_fingerprints(load_config(config_path))
            mismatches = store.configuration_mismatches(
                outer_batch_id=spec.batch_id,
                fingerprints=fingerprints,
                through_stage=stop_stage,
                invalidated_stages=invalidated,
            )
            if mismatches:
                stages = sorted({row["stage"] for row in mismatches})
                raise RuntimeError(
                    f"{spec.batch_id} scientific configuration changed for {stages}; "
                    "use --invalidate-stage for the earliest changed stage"
                )
        with RunLease(
            store,
            command_digest=command_digest,
            generation=generation,
        ):
            if invalidated:
                store.invalidate_stages(
                    invalidated,
                    outer_batch_ids=[spec.batch_id for spec in specs],
                )
            reconcile_dependencies(store.database.parents[1], store, stop_stage=stop_stage)
            shared_sandbox = _shared_sandbox(
                runtime_configs,
                start_stage=start_stage,
                stop_stage=stop_stage,
            )
            with shared_sandbox as sandbox_runtime:
                for spec, runtime_config in zip(specs, runtime_configs, strict=True):
                    result = run_pipeline(
                        runtime_config,
                        execution_backend=("sandbox" if sandbox_runtime is not None else "local"),
                        stop_after=stop_stage,
                        resume_options={
                            "store": store,
                            "generation": generation,
                            "outer_batch_id": spec.batch_id,
                            "target_slot_start": spec.target_slot_start,
                            "start_stage": start_stage,
                            "stop_stage": stop_stage,
                            "retry_only": retry_only,
                            "invalidated_stages": invalidated,
                        },
                        sandbox_runtime=sandbox_runtime,
                    )
                    results.append(
                        {
                            "batch": spec.batch_id,
                            "status": result.get("status"),
                            "workspace": result.get("workspace"),
                        }
                    )
            generation_status = "completed"
    finally:
        store.finish_generation(generation, status=generation_status)
        summary = store.export_audit_files()
    return {
        "generation": generation,
        "status": generation_status,
        "batches": results,
        "summary": summary,
    }


def append_batches(
    run_root: Path,
    *,
    old_target: int,
    total: int,
    batch_size: int,
    template_path: str | Path | None,
    write_configs: bool = True,
) -> list[BatchSpec]:
    existing_configs = sorted((run_root / "configs").glob("batch-[0-9][0-9][0-9][0-9].json"))
    if existing_configs:
        template = _plain_loaded_config(existing_configs[-1])
    elif template_path is not None:
        template = _plain_loaded_config(Path(template_path).expanduser().resolve())
    else:
        raise ValueError("a --template is required when creating the first batch")
    next_index = max((_batch_index(path.stem) for path in existing_configs), default=0) + 1
    cursor = old_target
    output: list[BatchSpec] = []
    while cursor < total:
        count = min(batch_size, total - cursor)
        batch_id = f"batch-{next_index:04d}"
        config_path = run_root / "configs" / f"{batch_id}.json"
        workspace = run_root / "batches" / batch_id
        config = copy.deepcopy(template)
        config.update(
            {
                "workspace": str(workspace),
                "run_id": f"resume-{batch_id}",
                "resume_completed_stages": True,
            }
        )
        config.setdefault("stage00", {}).update(
            {
                "enabled": True,
                "count": count,
                "resume": True,
                # The run-local selection ledger is authoritative. Keeping this
                # empty avoids an O(number-of-batches) manifest chain.
                "exclude_selected_manifests": [],
            }
        )
        registry = config.setdefault("registry", {})
        registry.update(
            {
                "database": str(run_root / "registry" / "paper_screening_registry.sqlite"),
                "export_jsonl": str(
                    run_root / "registry" / "paper_screening_registry.jsonl"
                ),
            }
        )
        sandbox = config.setdefault("execution", {}).setdefault("sandbox", {})
        sandbox.update(
            {
                "source": str(run_root / ".sandboxes.local.yaml"),
                "inventory": str(run_root / ".sandbox_inventory.local.json"),
            }
        )
        if write_configs:
            write_json(config_path, config)
        output.append(
            BatchSpec(
                batch_id=batch_id,
                index=next_index,
                target_slot_start=cursor + 1,
                count=count,
                config_path=config_path,
                workspace=workspace,
                is_new=True,
            )
        )
        cursor += count
        next_index += 1
    return output


def discover_batches(
    run_root: Path,
    *,
    old_target: int,
    new_specs: Iterable[BatchSpec] = (),
) -> list[BatchSpec]:
    new_by_id = {item.batch_id: item for item in new_specs}
    output: list[BatchSpec] = []
    slot = 1
    for config_path in sorted((run_root / "configs").glob("batch-[0-9][0-9][0-9][0-9].json")):
        batch_id = config_path.stem
        if batch_id in new_by_id:
            item = new_by_id[batch_id]
        else:
            raw = json.loads(config_path.read_text(encoding="utf-8"))
            count = int((raw.get("stage00") or {}).get("count", 0))
            item = BatchSpec(
                batch_id=batch_id,
                index=_batch_index(batch_id),
                target_slot_start=slot,
                count=count,
                config_path=config_path,
                workspace=(run_root / "batches" / batch_id),
                is_new=slot > old_target,
            )
        output.append(item)
        slot += item.count
    existing_ids = {item.batch_id for item in output}
    output.extend(item for item in new_by_id.values() if item.batch_id not in existing_ids)
    output.sort(key=lambda item: item.index)
    return output


def materialize_runtime_config(
    *,
    store: ResumeStateStore,
    spec: BatchSpec,
    generation: int,
    stop_stage: str,
    resume_config: str,
    runtime_overrides: dict[str, Any],
) -> Path:
    if resume_config not in {"original", "current"}:
        raise ValueError("resume_config must be original or current")
    current = _plain_loaded_config(spec.config_path)
    frozen_path = store.root / "config_snapshots" / f"{spec.batch_id}.json"
    if resume_config == "original" and frozen_path.is_file():
        frozen = json.loads(frozen_path.read_text(encoding="utf-8"))
        config = _original_science_current_runtime(frozen, current)
    else:
        config = current
    config = merge_dict(config, runtime_overrides)
    config.update(
        {
            "workspace": str(spec.workspace),
            "stop_after": stop_stage,
            "resume_completed_stages": True,
        }
    )
    config.setdefault("stage00", {}).update(
        {"enabled": True, "count": spec.count, "resume": True}
    )
    runtime_path = (
        store.root
        / "runtime_configs"
        / f"generation-{generation:04d}"
        / f"{spec.batch_id}.json"
    )
    write_json(runtime_path, config)
    return runtime_path


def expanded_invalidation(stages: Iterable[str]) -> tuple[str, ...]:
    requested = {_normalize_stage(value) for value in stages}
    expanded: list[str] = []
    for index in range(6):
        stage = f"stage{index:02d}"
        if any(index >= int(value.removeprefix("stage")) for value in requested):
            expanded.extend(CHILD_STAGES.get(stage, (stage,)))
    return tuple(dict.fromkeys(expanded))


def command_digest(values: dict[str, Any]) -> str:
    return canonical_hash(_json_command_value(values))


def _configured_target(run_root: Path, store: ResumeStateStore) -> int:
    configured = 0
    for path in sorted((run_root / "configs").glob("batch-[0-9][0-9][0-9][0-9].json")):
        value = json.loads(path.read_text(encoding="utf-8"))
        configured += int((value.get("stage00") or {}).get("count", 0))
    return max(configured, store.max_target_slot())


def _plain_loaded_config(path: str | Path) -> dict[str, Any]:
    config = load_config(path)
    config.pop("config_path", None)
    return _strip_runtime_sentinels(config)


def _original_science_current_runtime(
    frozen: dict[str, Any], current: dict[str, Any]
) -> dict[str, Any]:
    config = copy.deepcopy(frozen)
    for key in ("pipeline_contract", "workspace", "run_id", "source", "registry"):
        if key in current:
            config[key] = copy.deepcopy(current[key])
    config["execution"] = copy.deepcopy(current.get("execution") or {})
    current_stage00 = current.get("stage00") or {}
    for key in (
        "credentials",
        "outside",
        "resume",
        "exclude_selected_manifests",
    ):
        if key in current_stage00:
            config.setdefault("stage00", {})[key] = copy.deepcopy(current_stage00[key])
    for stage in ("stage00", "stage01", "stage02", "stage03", "stage04", "stage05"):
        config.setdefault(stage, {})
    # Runtime service endpoints in a snapshot are ephemeral sandbox proxies.
    config["stage01"].setdefault("normalization", {})["grobid"] = _overlay_runtime_keys(
        config["stage01"].setdefault("normalization", {}).get("grobid") or {},
        ((current.get("stage01") or {}).get("normalization") or {}).get("grobid") or {},
    )
    config["stage03"]["softcite"] = _overlay_runtime_keys(
        config["stage03"].get("softcite") or {},
        (current.get("stage03") or {}).get("softcite") or {},
    )
    current_mineru = copy.deepcopy((current.get("stage04") or {}).get("mineru") or {})
    frozen_mineru = copy.deepcopy((config.get("stage04") or {}).get("mineru") or {})
    for key in (
        "command",
        "environment",
        "working_directory",
        "api_url",
        "api_concurrency",
        "request_batch_size",
        "timeout_seconds",
        "reuse_existing",
        "managed_gpu",
    ):
        if key in current_mineru:
            frozen_mineru[key] = current_mineru[key]
    config["stage04"]["mineru"] = frozen_mineru
    current_models = current.get("models") or {}
    for role, model in (config.get("models") or {}).items():
        runtime_model = current_models.get(role) or {}
        for key in (
            "base_url",
            "base_url_env",
            "api_key_env",
            "timeout_seconds",
            "retries",
            "workers",
            "use_proxy",
            "proxy_url_env",
            "fallback_models",
            "enabled",
            "managed_rlaunch",
            "allow_worker_creation",
            "preserve_worker_on_exit",
            "existing_worker",
            "manager_script",
            "state_file",
        ):
            if key in runtime_model:
                model[key] = copy.deepcopy(runtime_model[key])
    for role, model in current_models.items():
        config.setdefault("models", {}).setdefault(role, copy.deepcopy(model))
    config["microbatch"] = copy.deepcopy(current.get("microbatch") or {})
    return _strip_runtime_sentinels(config)


def _shared_sandbox(
    runtime_configs: list[Path], *, start_stage: str, stop_stage: str
):
    import contextlib

    if not runtime_configs:
        return contextlib.nullcontext(None)
    config = load_config(runtime_configs[0])
    if (config.get("execution") or {}).get("backend", "local") != "sandbox":
        return contextlib.nullcontext(None)
    if not _stage_range_requires_sandbox(config, start_stage, stop_stage):
        return contextlib.nullcontext(None)
    from src.pipeline import _sandbox_options_from_config
    from src.sandbox.runtime import SandboxPipelineRuntime

    return SandboxPipelineRuntime(_sandbox_options_from_config(config))


def _stage_range_requires_sandbox(
    config: dict[str, Any], start_stage: str, stop_stage: str
) -> bool:
    start_index = int(start_stage.removeprefix("stage"))
    stop_index = int(stop_stage.removeprefix("stage"))
    if start_index <= 1 <= stop_index:
        return True
    softcite = (config.get("stage03") or {}).get("softcite") or {}
    if start_index <= 3 <= stop_index and softcite.get("enabled", False):
        return True
    mineru = (config.get("stage04") or {}).get("mineru") or {}
    return bool(
        start_index <= 4 <= stop_index
        and mineru.get("enabled", True)
        and not mineru.get("managed_gpu", False)
    )


def _json_command_value(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _json_command_value(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_json_command_value(item) for item in value]
    if isinstance(value, Path):
        return str(value.expanduser().resolve())
    return value


def _overlay_runtime_keys(original: dict[str, Any], current: dict[str, Any]) -> dict[str, Any]:
    runtime_keys = {
        "api_concurrency",
        "api_url",
        "base_url",
        "buffer_size",
        "cache",
        "cleanup",
        "connect_timeout_seconds",
        "credentials",
        "lifecycle_minutes",
        "manage_service",
        "network_workers",
        "outside",
        "proxy_url_env",
        "read_timeout_seconds",
        "retries",
        "service_log",
        "startup_timeout_seconds",
        "timeout_seconds",
        "use_proxy",
        "workers",
        "working_directory",
    }
    output = copy.deepcopy(original)
    for key, value in current.items():
        if key in runtime_keys:
            output[key] = copy.deepcopy(value)
    return output


def _strip_runtime_sentinels(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: _strip_runtime_sentinels(item)
            for key, item in value.items()
            if not key.startswith("_sandbox_") and key != "execution_backend"
        }
    if isinstance(value, list):
        return [_strip_runtime_sentinels(item) for item in value]
    return value


def _normalize_stage(value: str) -> str:
    text = str(value).strip().casefold().replace("_", "")
    if text.startswith("stage"):
        suffix = text[5:]
    else:
        suffix = text
    if not suffix.isdigit() or not 0 <= int(suffix) <= 5:
        raise ValueError(f"invalid Stage00-05 stage: {value}")
    return f"stage{int(suffix):02d}"


def _normalize_batch_id(value: str) -> str:
    text = str(value).strip().casefold()
    if text.startswith("batch-"):
        suffix = text[6:]
    else:
        suffix = text
    if not suffix.isdigit():
        raise ValueError(f"invalid batch ID: {value}")
    return f"batch-{int(suffix):04d}"


def _batch_index(value: str) -> int:
    return int(value.removeprefix("batch-"))


def _validate_stage_range(start_stage: str, stop_stage: str) -> None:
    start = _normalize_stage(start_stage)
    stop = _normalize_stage(stop_stage)
    if int(start[-2:]) > int(stop[-2:]):
        raise ValueError("--start-stage must not be after --stop-stage")
