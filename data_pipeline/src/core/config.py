import os
from pathlib import Path
from typing import Any

DEFAULT_REVIEW_ROLES = (
    "scientific_grounding",
    "tool_data_feasibility",
    "evaluation_design",
    "leakage_difficulty",
)


def normalize_config(raw: dict[str, Any], base: Path) -> dict[str, Any]:
    """Expand the public compact config into the internal stage configuration."""

    if "pdf_directory" not in raw:
        return raw

    run_dir = _resolve(base, raw.get("run_directory", "runs/current"))
    pdf_directory = _resolve(base, raw["pdf_directory"])
    llm = raw.get("llm") or {}
    llm_enabled = bool(llm.get("enabled", True))
    workers = int(llm.get("max_workers", 3))
    extraction_llm = _llm_stage(llm, "extraction", "EXTRACTION_LLM", "deepseek-v4-flash")
    classification_llm = _llm_stage(
        llm, "classification", "TASK_CLASSIFICATION_LLM", "deepseek-v4-flash"
    )
    generation_llm = _llm_stage(llm, "generation", "TASK_GENERATION_LLM", "deepseek-v4-pro")
    review_llm = _llm_stage(llm, "review", "REVIEW_LLM", "deepseek-v4-flash")
    roles = (llm.get("review") or {}).get("roles") or list(DEFAULT_REVIEW_ROLES)

    mineru = raw.get("mineru") or {}
    toolbox = raw.get("toolbox") or {}
    mineru_environment = {"MINERU_MODEL_SOURCE": "local"}
    mineru_environment.update(
        {str(key): str(value) for key, value in (mineru.get("environment") or {}).items()}
    )
    verify_urls = bool(raw.get("verify_asset_urls", True))
    prompt_path = _resolve(base, raw.get("prompt_examples", "assets/prompt_examples.json"))

    reviewers = [
        {
            "name": f"{review_llm['model']}_{role}",
            "role": role,
            **review_llm,
            "max_tokens": 4000,
        }
        for role in roles
    ]

    return {
        "source": {"mode": "corpus", "root": str(pdf_directory)},
        "workspace": str(run_dir / "outputs"),
        "log_file": str(run_dir / "outputs" / "pipeline.log"),
        "output": str(run_dir / "outputs" / "stage_18_dataset_build" / "dataset"),
        "stop_after": raw.get("stop_after", "model_ensemble"),
        "cheap_extract": {
            "text_dir": str(run_dir / "outputs" / "stage_02_cheap_extract" / "text"),
            "reuse_existing": True,
        },
        "mineru": {
            "execute": bool(mineru.get("enabled", True)),
            "output_dir": str(run_dir / "outputs" / "stage_07_mineru_parse" / "mineru"),
            "command": mineru.get("command", ".venv/bin/mineru"),
            "method": "auto",
            "backend": mineru.get("backend", "pipeline"),
            "timeout_seconds": int(mineru.get("timeout_seconds", 3600)),
            "environment": mineru_environment,
            "extra_args": ["--formula", "true", "--table", "true"],
            "reuse_existing": True,
        },
        "extract": {"relevance_decisions": ["pass"]},
        "semantic_review": {
            "enabled": llm_enabled,
            **extraction_llm,
            "max_source_chars": 50_000,
            "max_tokens": 4000,
            "max_workers": workers,
            "cache_dir": str(
                run_dir / "outputs" / "stage_12_scientific_record_extraction" / "llm_cache"
            ),
        },
        "task_selection": {
            "enabled": llm_enabled,
            **classification_llm,
            "allow_deterministic_fallback": not llm_enabled,
            "max_tokens": 3000,
            "cache_dir": str(run_dir / "outputs" / "stage_13_task_selection" / "llm_cache"),
        },
        "package_generation": {
            "enabled": llm_enabled,
            **generation_llm,
            "prompt_examples": str(prompt_path),
            "max_source_chars": 80_000,
            "max_tokens": 8000,
            "max_workers": max(1, min(workers, 2)),
            "repair_attempts": 1,
            "cache_dir": str(run_dir / "outputs" / "stage_14_package_generation" / "llm_cache"),
        },
        "toolbox": {
            "profile": str(_resolve(base, toolbox.get("file", "assets/toolbox.json"))),
            "enabled_software": toolbox.get("enabled_software", ["*"]),
            "enabled_actions": toolbox.get("enabled_actions", ["*"]),
            "priority_software": toolbox.get("priority_software", []),
            "preserve_priority_matches": True,
        },
        "quality_funnel": {
            "verify_asset_urls": verify_urls,
            "url_timeout_seconds": 8,
            "max_asset_urls": 8,
        },
        "asset_discovery": {
            "verify_asset_urls": verify_urls,
            "url_timeout_seconds": 8,
            "max_asset_urls": 8,
        },
        "model_ensemble": {
            "enabled": llm_enabled,
            "reviewers": reviewers,
            "minimum_completed_reviewers": min(3, len(reviewers)),
            "pass_quorum": 0.67,
            "reject_quorum": 0.5,
            "minimum_median_score": 75,
            "max_score_range": 30,
            "max_workers": workers,
        },
        "validation": {"allow_empty": True},
        "build": {
            "allow_machine_drafts": False,
            "require_reference_run": True,
            "accepted_curation_statuses": ["expert_approved"],
            "split_salt": "researchchembench-v1",
        },
    }


def _resolve(base: Path, value: str | Path) -> Path:
    path = Path(value).expanduser()
    return path.resolve() if path.is_absolute() else (base / path).resolve()


def _llm_stage(
    llm: dict[str, Any],
    stage_name: str,
    environment_prefix: str,
    default_model: str,
) -> dict[str, Any]:
    stage = llm.get(stage_name) or {}
    return {
        "base_url": os.environ.get(f"{environment_prefix}_URL")
        or stage.get("url", "https://api.deepseek.com/v1"),
        "api_key_env": stage.get("api_key_env", f"{environment_prefix}_API_KEY"),
        "model": os.environ.get(f"{environment_prefix}_MODEL_NAME")
        or stage.get("model_name", default_model),
        "timeout_seconds": int(stage.get("timeout_seconds", 900)),
        "retries": int(stage.get("retries", 2)),
        "thinking": stage.get("thinking", "disabled"),
    }
