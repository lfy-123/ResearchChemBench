from __future__ import annotations

import json
import os
from copy import deepcopy
from pathlib import Path
from typing import Any

from src.contracts import PIPELINE_CONTRACT

MODEL_ROLES = (
    "screening",
    "stage02_screening",
    "stage03_screening",
    "stage05_router",
    "suitability",
    "builder",
    "judge",
)


def load_config(path: str | Path) -> dict[str, Any]:
    source = _logical_path(path)
    raw = json.loads(source.read_text(encoding="utf-8"))
    if raw.get("pipeline_contract") != PIPELINE_CONTRACT:
        raise ValueError(
            f"pipeline requires pipeline_contract={PIPELINE_CONTRACT!r}; "
            f"received {raw.get('pipeline_contract')!r}"
        )
    config = deepcopy(raw)
    config["config_path"] = str(source)
    config["workspace"] = str(_resolve(source.parent, config.get("workspace", "runs/current")))
    registry = config.setdefault("registry", {})
    registry.setdefault("enabled", True)
    registry.setdefault("prune_rejected_stage00_assets", True)
    registry["database"] = str(
        _resolve(
            source.parent,
            registry.get("database", "registry/paper_screening_registry.sqlite"),
        )
    )
    registry["export_jsonl"] = str(
        _resolve(
            source.parent,
            registry.get("export_jsonl", "registry/exports/paper_screening_registry.jsonl"),
        )
    )
    source_config = config.setdefault("source", {})
    if source_config.get("root"):
        source_config["root"] = str(_resolve(source.parent, source_config["root"]))
    stage00 = config.setdefault("stage00", {})
    if stage00.get("credentials"):
        stage00["credentials"] = str(_resolve(source.parent, stage00["credentials"]))
    stage03 = config.setdefault("stage03", {})
    stage03["toolbox_capabilities"] = str(
        _resolve(
            source.parent,
            stage03.get("toolbox_capabilities", "assets/toolbox_capabilities.json"),
        )
    )
    stage03["software_aliases"] = str(
        _resolve(source.parent, stage03.get("software_aliases", "assets/software_aliases.json"))
    )
    stage03["external_software_aliases"] = str(
        _resolve(
            source.parent,
            stage03.get("external_software_aliases", "assets/external_software_aliases.json"),
        )
    )
    stage01 = config.setdefault("stage01", {})
    normalization = stage01.setdefault("normalization", {})
    config.setdefault("stage02", {})
    stage04 = config.setdefault("stage04", {})
    mineru = stage04.setdefault("mineru", {})
    mineru.setdefault("managed_gpu", False)
    mineru.setdefault("api_concurrency", 3)
    mineru.setdefault("request_batch_size", 1)
    if mineru.get("managed_gpu"):
        mineru["gpu_env_dir"] = str(
            _resolve(
                source.parent,
                mineru.get("gpu_env_dir", ".envs/researchchem-data-pipeline"),
            )
        )
        mineru["command"] = str(
            _resolve(
                source.parent,
                mineru.get("command", ".envs/researchchem-data-pipeline/bin/mineru"),
            )
        )
        environment = mineru.setdefault("environment", {})
        environment["MINERU_TOOLS_CONFIG_JSON"] = str(
            _resolve(
                source.parent,
                environment.get("MINERU_TOOLS_CONFIG_JSON", ".model_cache/mineru/mineru.json"),
            )
        )
    config.setdefault("stage05", {})
    config.setdefault("stage06", {})
    config.setdefault("stage07", {})
    config.setdefault("microbatch", {})
    execution = config.setdefault("execution", {})
    sandbox = execution.setdefault("sandbox", {})
    for key in ("source", "inventory"):
        if sandbox.get(key):
            sandbox[key] = str(_resolve(source.parent, sandbox[key]))
    for service in (normalization.get("grobid") or {}, stage03.get("softcite") or {}):
        for key in ("working_directory", "service_log"):
            if service.get(key):
                service[key] = str(_resolve(source.parent, service[key]))
    _normalize_model_roles(config)
    screening = config["models"]["screening"]
    screening.setdefault("preserve_worker_on_exit", False)
    screening.setdefault("allow_worker_creation", True)
    for key in ("manager_script", "state_file"):
        if screening.get(key):
            screening[key] = str(_resolve(source.parent, screening[key]))
    _validate(config)
    return config


def _normalize_model_roles(config: dict[str, Any]) -> None:
    models = config.setdefault("models", {})
    screening = dict(models.get("screening") or {})
    for role in ("stage02_screening", "stage03_screening"):
        if role not in models:
            # Legacy v2 configs used one deployed screening model for both
            # stages. Preserve that behavior unless a stage-specific API role
            # is configured explicitly.
            inherited = dict(screening)
            inherited["api_key_env"] = f"RCB_{role.upper()}_API_KEY"
            models[role] = inherited
    if "stage05_router" not in models:
        # Existing v2 configs had one suitability role. Preserve their endpoint
        # and credentials while allowing router-specific environment overrides.
        inherited = dict(models.get("suitability") or {})
        inherited["api_key_env"] = "RCB_STAGE05_ROUTER_API_KEY"
        inherited["model"] = os.environ.get("RCB_STAGE05_ROUTER_MODEL") or inherited.get("model")
        inherited["base_url"] = (
            os.environ.get("RCB_STAGE05_ROUTER_BASE_URL") or inherited.get("base_url")
        )
        models["stage05_router"] = inherited
    for role in MODEL_ROLES:
        value = models.setdefault(role, {})
        value.setdefault("enabled", True)
        value.setdefault("timeout_seconds", 900)
        value.setdefault("retries", 2)
        value.setdefault("max_tokens", 2048)
        value.setdefault("thinking", "disabled")
        value.setdefault("workers", 1)
        value.setdefault("cache", True)
        value.setdefault("api_key_env", f"RCB_{role.upper()}_API_KEY")
        fallbacks = value.setdefault("fallback_models", [])
        if not isinstance(fallbacks, list) or any(not isinstance(item, dict) for item in fallbacks):
            raise ValueError(f"models.{role}.fallback_models must be a list of objects")
        value.setdefault(
            "use_proxy", role in {"stage05_router", "suitability", "builder", "judge"}
        )
        value.setdefault("proxy_url_env", "HTTPS_PROXY")
        env_prefix = f"RCB_{role.upper()}"
        base_url_env = str(value.get("base_url_env") or f"{env_prefix}_BASE_URL")
        model_env = str(value.get("model_env") or f"{env_prefix}_MODEL")
        value["base_url"] = os.environ.get(base_url_env) or value.get("base_url")
        value["model"] = os.environ.get(model_env) or value.get("model")
        for fallback in fallbacks:
            fallback.setdefault("base_url", value.get("base_url"))
            fallback.setdefault("api_key_env", value.get("api_key_env"))
            fallback.setdefault("timeout_seconds", value.get("timeout_seconds"))
            fallback.setdefault("retries", value.get("retries"))
            fallback.setdefault("max_tokens", value.get("max_tokens"))
            fallback.setdefault("use_proxy", value.get("use_proxy"))


def _validate(config: dict[str, Any]) -> None:
    models = config["models"]
    for role in MODEL_ROLES:
        model = models[role]
        if model.get("enabled", True) and (not model.get("base_url") or not model.get("model")):
            raise ValueError(f"models.{role} requires base_url and model")
        if int(model.get("workers", 1)) < 1:
            raise ValueError(f"models.{role}.workers must be at least 1")
        if not isinstance(model.get("use_proxy"), bool):
            raise ValueError(f"models.{role}.use_proxy must be true or false")
    if not isinstance(models["screening"].get("preserve_worker_on_exit"), bool):
        raise ValueError("models.screening.preserve_worker_on_exit must be true or false")
    if not isinstance(models["screening"].get("allow_worker_creation"), bool):
        raise ValueError("models.screening.allow_worker_creation must be true or false")
    for stage, dedicated_role in (
        ("stage02", "stage02_screening"),
        ("stage03", "stage03_screening"),
    ):
        configured_role = config[stage].get("model_role", "screening")
        if configured_role not in {"screening", dedicated_role}:
            raise ValueError(f"{stage}.model_role must be screening or {dedicated_role}")
        config[stage]["model_role"] = configured_role
    for stage, expected in (
        ("stage05", "suitability"),
        ("stage06", "builder"),
        ("stage07", "judge"),
    ):
        role = config[stage].get("model_role", expected)
        if role != expected:
            raise ValueError(f"{stage}.model_role must be {expected}")
        config[stage]["model_role"] = expected
    router_role = config["stage05"].get("router_model_role", "stage05_router")
    if router_role != "stage05_router":
        raise ValueError("stage05.router_model_role must be stage05_router")
    config["stage05"]["router_model_role"] = router_role
    stop_after = str(config.get("stop_after", "stage07"))
    if stop_after not in {f"stage{index:02d}" for index in range(8)}:
        raise ValueError("stop_after must be stage00 through stage07")
    config["stop_after"] = stop_after
    mode = str(config.get("policy", "strict"))
    if mode not in {"strict", "shadow"}:
        raise ValueError("policy must be strict or shadow")
    config["policy"] = mode
    registry = config["registry"]
    for key in ("enabled", "prune_rejected_stage00_assets"):
        if not isinstance(registry.get(key), bool):
            raise ValueError(f"registry.{key} must be true or false")
    microbatch = config["microbatch"]
    for key in ("size", "concurrency", "buffer_size"):
        if int(microbatch.get(key, 1)) < 1:
            raise ValueError(f"microbatch.{key} must be at least 1")
    stage_concurrency = microbatch.setdefault("stage_concurrency", {})
    for stage, value in stage_concurrency.items():
        if stage not in {"stage01", "stage02", "stage03", "stage04", "stage05"}:
            raise ValueError(f"microbatch.stage_concurrency has unknown stage: {stage}")
        if int(value) < 1:
            raise ValueError(f"microbatch.stage_concurrency.{stage} must be at least 1")
    mineru = config["stage04"].get("mineru") or {}
    if mineru.get("managed_gpu"):
        if not config["models"]["screening"].get("managed_rlaunch"):
            raise ValueError("stage04.mineru.managed_gpu requires models.screening.managed_rlaunch")
        if int(mineru.get("api_concurrency", 1)) < 1:
            raise ValueError("stage04.mineru.api_concurrency must be at least 1")
        if int(mineru.get("request_batch_size", 1)) < 1:
            raise ValueError("stage04.mineru.request_batch_size must be at least 1")


def _resolve(base: Path, value: str | Path) -> Path:
    return _logical_path(value, base=base)


def _logical_path(value: str | Path, *, base: Path | None = None) -> Path:
    path = Path(value).expanduser()
    if not path.is_absolute():
        logical_base = base or Path(os.environ.get("PWD") or os.getcwd())
        path = logical_base / path
    return Path(os.path.normpath(str(path)))
