from __future__ import annotations

import json
import os
from copy import deepcopy
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

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

CODEX_WIRE_APIS = frozenset({"chat_completions", "responses"})
TOOL_CHOICE_POLICIES = frozenset({"auto", "required_until_artifact", "required", "none"})
RESPONSE_FORMAT_POLICIES = frozenset({"auto", "json_schema", "json_object", "none"})
MODEL_PROTOCOL_KEYS = (
    "codex_wire_api",
    "tool_choice_policy",
    "response_format_policy",
)
DEFAULT_MODEL_PROTOCOL = {
    "codex_wire_api": "chat_completions",
    "tool_choice_policy": "auto",
    "response_format_policy": "auto",
}


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
    protocol_profiles = _load_model_protocol_profiles(config, source=source)
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
    if stage00.get("publication_index_path"):
        stage00["publication_index_path"] = str(
            _resolve(source.parent, stage00["publication_index_path"])
        )
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
    # The managed GROBID runtime always materializes this mapping. Normalize it
    # before resume fingerprints are computed so service startup cannot look
    # like a scientific configuration change.
    grobid = normalization.setdefault("grobid", {})
    grobid.setdefault("environment", {})
    config.setdefault("stage02", {})
    stage04 = config.setdefault("stage04", {})
    mineru = stage04.setdefault("mineru", {})
    mineru.setdefault("managed_gpu", False)
    mineru.setdefault("api_concurrency", 3)
    mineru.setdefault("request_batch_size", 1)
    mineru.setdefault("cleanup_successful_intermediates", True)
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
    stage05 = config.setdefault("stage05", {})
    for key in (
        "toolbox_capabilities",
        "software_aliases",
        "external_software_aliases",
    ):
        stage05.setdefault(key, stage03[key])
        stage05[key] = str(_resolve(source.parent, stage05[key]))
    stage06 = config.setdefault("stage06", {})
    stage07 = config.setdefault("stage07", {})
    stage06["harness"] = os.environ.get("RCB_STAGE06_HARNESS") or stage06.get(
        "harness", "codex"
    )
    stage06.setdefault("synthesis_max_tool_calls", 180)
    stage06.setdefault("synthesis_finalization_reserve", 6)
    stage06.setdefault("synthesis_timeout_seconds", 5400)
    stage06.setdefault("model_context_window", 1_000_000)
    stage06.setdefault("model_auto_compact_token_limit", 750_000)
    stage06.setdefault("model_auto_compact_token_limit_scope", "total")
    # Late-stage Agents only need the ordinary shell in their isolated workspace.
    # Keep the unavailable optional code-mode host out of the model tool surface;
    # otherwise some Codex models mistake its startup diagnostic for a shell failure.
    stage06.setdefault("codex_disable_code_mode", True)
    stage07["harness"] = os.environ.get("RCB_STAGE07_HARNESS") or stage07.get(
        "harness", "codex"
    )
    stage07.setdefault("audit_repair_max_tool_calls", 120)
    stage07.setdefault("audit_repair_finalization_reserve", 16)
    stage07.setdefault("model_context_window", 1_000_000)
    stage07.setdefault("model_auto_compact_token_limit", 750_000)
    stage07.setdefault("model_auto_compact_token_limit_scope", "total")
    stage07.setdefault("codex_disable_code_mode", True)
    for stage in (stage06, stage07):
        stage.setdefault("toolbox_capabilities", stage03["toolbox_capabilities"])
        if stage.get("toolbox_capabilities"):
            stage["toolbox_capabilities"] = str(
                _resolve(source.parent, stage["toolbox_capabilities"])
            )
        stage.setdefault("workers", 1)
        stage.setdefault("timeout_seconds", 3600)
        stage.setdefault("checkpoint_cache_enabled", True)
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
    _normalize_model_roles(config, protocol_profiles=protocol_profiles)
    screening = config["models"]["screening"]
    screening.setdefault("preserve_worker_on_exit", False)
    screening.setdefault("allow_worker_creation", True)
    for key in ("manager_script", "state_file"):
        if screening.get(key):
            screening[key] = str(_resolve(source.parent, screening[key]))
    _validate(config)
    return config


def _load_model_protocol_profiles(
    config: dict[str, Any], *, source: Path
) -> dict[str, Any]:
    configured_path = config.get("model_protocol_profiles_path")
    if not configured_path:
        return {"defaults": {}, "models": {}}
    profile_path = _resolve(source.parent, str(configured_path))
    if not profile_path.is_file():
        raise FileNotFoundError(f"model protocol profiles file does not exist: {profile_path}")
    payload = json.loads(profile_path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError("model protocol profiles must be a JSON object")
    defaults = payload.get("defaults") or {}
    models = payload.get("models") or {}
    if not isinstance(defaults, dict) or not isinstance(models, dict):
        raise ValueError("model protocol profiles defaults and models must be JSON objects")
    for profile_name, profile in [("defaults", defaults), *models.items()]:
        if not isinstance(profile, dict):
            raise ValueError(f"model protocol profile {profile_name!r} must be a JSON object")
        unknown = set(profile) - set(MODEL_PROTOCOL_KEYS)
        if unknown:
            raise ValueError(
                f"model protocol profile {profile_name!r} has unsupported fields: "
                f"{sorted(unknown)}"
            )
        _validate_protocol_values(profile, label=f"model protocol profile {profile_name!r}")
    config["model_protocol_profiles_path"] = str(profile_path)
    return {"defaults": defaults, "models": models}


def _validate_protocol_values(values: dict[str, Any], *, label: str) -> None:
    allowed_by_key = {
        "codex_wire_api": CODEX_WIRE_APIS,
        "tool_choice_policy": TOOL_CHOICE_POLICIES,
        "response_format_policy": RESPONSE_FORMAT_POLICIES,
    }
    for key, value in values.items():
        normalized = str(value or "").casefold()
        if normalized not in allowed_by_key[key]:
            raise ValueError(f"{label}.{key} must be one of {sorted(allowed_by_key[key])}")
        values[key] = normalized


def _model_protocol_profile(
    protocol_profiles: dict[str, Any], model: str
) -> tuple[str | None, dict[str, Any]]:
    normalized_model = str(model or "").casefold()
    for profile_name, profile in (protocol_profiles.get("models") or {}).items():
        if str(profile_name).casefold() == normalized_model:
            return str(profile_name), dict(profile)
    return None, {}


def _apply_model_protocol_profile(
    value: dict[str, Any],
    *,
    protocol_profiles: dict[str, Any],
    inherited: dict[str, Any] | None = None,
) -> None:
    profile_name, profile = _model_protocol_profile(
        protocol_profiles, str(value.get("model") or "")
    )
    defaults = protocol_profiles.get("defaults") or {}
    for key in MODEL_PROTOCOL_KEYS:
        if key in value:
            continue
        if key in profile:
            value[key] = profile[key]
        elif inherited and key in inherited:
            value[key] = inherited[key]
        elif key in defaults:
            value[key] = defaults[key]
        else:
            value[key] = DEFAULT_MODEL_PROTOCOL[key]
    if profile_name:
        value["model_protocol_profile"] = profile_name


def _normalize_model_roles(
    config: dict[str, Any], *, protocol_profiles: dict[str, Any] | None = None
) -> None:
    protocol_profiles = protocol_profiles or {"defaults": {}, "models": {}}
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
        use_proxy_env = str(value.get("use_proxy_env") or f"{env_prefix}_USE_PROXY")
        raw_use_proxy = os.environ.get(use_proxy_env)
        if raw_use_proxy is not None:
            normalized_use_proxy = raw_use_proxy.strip().casefold()
            if normalized_use_proxy in {"1", "true", "yes", "on"}:
                value["use_proxy"] = True
            elif normalized_use_proxy in {"0", "false", "no", "off"}:
                value["use_proxy"] = False
            else:
                raise ValueError(
                    f"{use_proxy_env} must be a boolean (true/false), got {raw_use_proxy!r}"
                )
        # Explicit loopback endpoints are local services.  Do not route them through
        # the cluster's outbound proxy even when the shared remote-model defaults
        # enable proxying for this role.
        try:
            hostname = urlparse(str(value.get("base_url") or "")).hostname
        except ValueError:
            hostname = None
        if hostname in {"127.0.0.1", "localhost", "::1"} and raw_use_proxy is None:
            value["use_proxy"] = False
        model_override = os.environ.get(model_env)
        if model_override:
            if str(value.get("model") or "").casefold() != model_override.casefold():
                inferred = _model_thinking_kwargs(model_override)
                value["chat_template_kwargs"] = inferred or {}
                value["thinking"] = None
            value["model"] = model_override
        reasoning_effort = os.environ.get(f"{env_prefix}_REASONING_EFFORT")
        if reasoning_effort:
            value["reasoning_effort"] = reasoning_effort.strip().casefold()
        reasoning_mode = os.environ.get(f"{env_prefix}_REASONING_MODE")
        if reasoning_mode:
            value["reasoning_mode"] = reasoning_mode.strip().casefold()
        _apply_model_protocol_profile(value, protocol_profiles=protocol_profiles)
        for key in MODEL_PROTOCOL_KEYS:
            environment_value = os.environ.get(f"{env_prefix}_{key.upper()}")
            if environment_value:
                value[key] = environment_value.strip().casefold()
        if value.get("chat_template_kwargs") is None:
            inferred_kwargs = _model_thinking_kwargs(str(value.get("model") or ""))
            if inferred_kwargs:
                value["chat_template_kwargs"] = inferred_kwargs
                value["thinking"] = None
        fallback_env = os.environ.get(f"{env_prefix}_FALLBACK_MODELS", "").strip()
        if fallback_env:
            fallbacks[:] = [
                {"model": name.strip(), "chat_template_kwargs": _model_thinking_kwargs(name)}
                for name in fallback_env.split(",")
                if name.strip()
            ]
        fallback_strategy_env = os.environ.get(f"{env_prefix}_FALLBACK_STRATEGY", "").strip()
        if fallback_strategy_env:
            value["fallback_strategy"] = fallback_strategy_env.casefold()
        strategy = str(value.get("fallback_strategy", "sequential")).strip().casefold()
        if strategy not in {"sequential", "random_one", "random_single"}:
            raise ValueError(
                f"models.{role}.fallback_strategy must be sequential or random_one"
            )
        value["fallback_strategy"] = "random_one" if strategy == "random_single" else strategy
        for fallback in fallbacks:
            fallback.setdefault("base_url", value.get("base_url"))
            fallback.setdefault("api_key_env", value.get("api_key_env"))
            fallback.setdefault("timeout_seconds", value.get("timeout_seconds"))
            fallback.setdefault("retries", value.get("retries"))
            fallback.setdefault("max_tokens", value.get("max_tokens"))
            fallback.setdefault("use_proxy", value.get("use_proxy"))
            _apply_model_protocol_profile(
                fallback,
                protocol_profiles=protocol_profiles,
                inherited=value,
            )


def _model_thinking_kwargs(model: str) -> dict[str, bool]:
    name = model.casefold()
    if name.startswith("deepseek") or name.startswith("kimi"):
        return {"thinking": False}
    if name.startswith("glm") or name.startswith("qwen") or name == "nex-n2-pro":
        return {"enable_thinking": False}
    return {}


def _validate(config: dict[str, Any]) -> None:
    models = config["models"]
    for stage in ("stage06", "stage07"):
        harness = str(config[stage].get("harness") or "").casefold()
        if harness not in {"codex", "claude", "opencode", "mock", "direct_api"}:
            raise ValueError(
                f"{stage}.harness must be codex, claude, opencode, mock, or direct_api"
            )
        config[stage]["harness"] = harness
        if int(config[stage].get("workers", 1)) < 1:
            raise ValueError(f"{stage}.workers must be at least 1")
        if int(config[stage].get("timeout_seconds", 1)) < 1:
            raise ValueError(f"{stage}.timeout_seconds must be positive")
    for role in MODEL_ROLES:
        model = models[role]
        if model.get("enabled", True) and (not model.get("base_url") or not model.get("model")):
            raise ValueError(f"models.{role} requires base_url and model")
        if int(model.get("workers", 1)) < 1:
            raise ValueError(f"models.{role}.workers must be at least 1")
        if not isinstance(model.get("use_proxy"), bool):
            raise ValueError(f"models.{role}.use_proxy must be true or false")
        if str(model.get("codex_wire_api") or "") not in CODEX_WIRE_APIS:
            raise ValueError(
                f"models.{role}.codex_wire_api must be one of {sorted(CODEX_WIRE_APIS)}"
            )
        if str(model.get("tool_choice_policy") or "") not in TOOL_CHOICE_POLICIES:
            raise ValueError(
                f"models.{role}.tool_choice_policy must be one of "
                f"{sorted(TOOL_CHOICE_POLICIES)}"
            )
        if str(model.get("response_format_policy") or "") not in RESPONSE_FORMAT_POLICIES:
            raise ValueError(
                f"models.{role}.response_format_policy must be one of "
                f"{sorted(RESPONSE_FORMAT_POLICIES)}"
            )
    for stage_name in ("stage06", "stage07"):
        stage = config[stage_name]
        for key, allowed in (
            ("tool_choice_policy", TOOL_CHOICE_POLICIES),
            ("response_format_policy", RESPONSE_FORMAT_POLICIES),
        ):
            if stage.get(key) is not None and str(stage[key]) not in allowed:
                raise ValueError(f"{stage_name}.{key} must be one of {sorted(allowed)}")
        suffixes = ("synthesis",) if stage_name == "stage06" else ("audit_repair",)
        for suffix in suffixes:
            for key, allowed in (
                ("tool_choice_policy", TOOL_CHOICE_POLICIES),
                ("response_format_policy", RESPONSE_FORMAT_POLICIES),
            ):
                field = f"{suffix}_{key}"
                if stage.get(field) is not None and str(stage[field]) not in allowed:
                    raise ValueError(f"{stage_name}.{field} must be one of {sorted(allowed)}")
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
    if not isinstance(mineru.get("cleanup_successful_intermediates"), bool):
        raise ValueError("stage04.mineru.cleanup_successful_intermediates must be true or false")
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
