import os
import sysconfig
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

    grobid = raw.get("grobid") or {}
    softcite = raw.get("softcite") or {}
    quantities = raw.get("grobid_quantities") or {}
    completeness = raw.get("computation_completeness") or {}
    resource_limits = raw.get("resource_limits") or {}
    java_home = softcite.get("java_home") or grobid.get("java_home")
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
        "source": {
            "mode": "corpus",
            "root": str(pdf_directory),
            "exclude_supplementary": bool(raw.get("exclude_supplementary", True)),
        },
        "workspace": str(run_dir / "outputs"),
        "log_file": str(run_dir / "outputs" / "pipeline.log"),
        "output": str(run_dir / "outputs" / "stage_18_dataset_build" / "dataset"),
        "stop_after": raw.get("stop_after", "model_ensemble"),
        "grobid_extract": {
            "base_url": grobid.get("base_url", "http://127.0.0.1:8070"),
            "tei_dir": str(run_dir / "outputs" / "stage_02_grobid_extract" / "tei"),
            "text_dir": str(run_dir / "outputs" / "stage_02_grobid_extract" / "text"),
            "service_log": str(
                run_dir / "outputs" / "stage_02_grobid_extract" / "grobid_service.log"
            ),
            "working_directory": str(
                _resolve(base, grobid.get("working_directory", "third_party/grobid"))
            ),
            "start_command": grobid.get("start_command", ["./gradlew", "--no-daemon", "run"]),
            "java_home": grobid.get("java_home"),
            "auto_start": bool(grobid.get("auto_start", True)),
            "startup_timeout_seconds": int(grobid.get("startup_timeout_seconds", 300)),
            "timeout_seconds": int(grobid.get("timeout_seconds", 900)),
            "retries": int(grobid.get("retries", 2)),
            "consolidate_header": int(grobid.get("consolidate_header", 0)),
            "consolidate_citations": int(grobid.get("consolidate_citations", 0)),
            "max_chars": int(grobid.get("max_chars", 2_000_000)),
            "reuse_existing": bool(grobid.get("reuse_existing", True)),
        },
        "software_coverage": {
            "base_url": softcite.get("base_url", "http://127.0.0.1:8060"),
            "working_directory": str(
                _resolve(base, softcite.get("working_directory", "third_party/software-mentions"))
            ),
            "start_command": softcite.get(
                "start_command", ["./gradlew", "--no-daemon", "run"]
            ),
            "java_home": java_home,
            "auto_start": bool(softcite.get("auto_start", True)),
            "startup_timeout_seconds": int(softcite.get("startup_timeout_seconds", 900)),
            "timeout_seconds": int(softcite.get("timeout_seconds", 600)),
            "retries": int(softcite.get("retries", 2)),
            "service_log": str(
                run_dir / "outputs" / "stage_03_software_coverage" / "softcite_service.log"
            ),
            "environment": {
                "CONDA_PREFIX": softcite.get("conda_prefix", "/usr/local"),
                "PYTHONPATH": os.pathsep.join(
                    [
                        str(_resolve(base, "third_party/delft")),
                        str(sysconfig.get_paths()["purelib"]),
                    ]
                ),
                "LD_LIBRARY_PATH": os.pathsep.join(
                    [
                        str(Path(java_home) / "lib" / "server") if java_home else "",
                        os.environ.get("LD_LIBRARY_PATH", ""),
                    ]
                ).strip(os.pathsep),
                **{
                    str(key): str(value)
                    for key, value in (softcite.get("environment") or {}).items()
                },
            },
            "aliases_file": str(_resolve(base, "assets/software_aliases.json")),
            "role_rules_file": str(_resolve(base, "assets/software_role_rules.json")),
            "capability_map_file": str(
                _resolve(base, "assets/software_capability_map.json")
            ),
        },
        "computation_completeness": {
            "enabled": bool(completeness.get("enabled", llm_enabled)),
            **classification_llm,
            **{
                key: value
                for key, value in completeness.items()
                if key not in {"enabled", "url", "model_name"}
            },
            "base_url": completeness.get("url", classification_llm["base_url"]),
            "model": completeness.get("model_name", classification_llm["model"]),
            "max_source_chars": int(completeness.get("max_source_chars", 30_000)),
            "max_paragraphs": int(completeness.get("max_paragraphs", 24)),
            "max_tokens": int(completeness.get("max_tokens", 1800)),
        },
        "resource_limits": {
            "cpu_cores": float(resource_limits.get("cpu_cores", 500)),
            "gpus": float(resource_limits.get("gpus", 8)),
            "memory_gb": float(resource_limits.get("memory_gb", 1000)),
            "runtime_hours": float(resource_limits.get("runtime_hours", 12)),
        },
        "grobid_quantities": {
            "base_url": quantities.get("base_url", "http://127.0.0.1:8062"),
            "working_directory": str(
                _resolve(base, quantities.get("working_directory", "third_party/grobid-quantities"))
            ),
            "start_command": quantities.get(
                "start_command", ["./gradlew", "--no-daemon", "run"]
            ),
            "java_home": quantities.get("java_home") or grobid.get("java_home"),
            "auto_start": bool(quantities.get("auto_start", True)),
            "startup_timeout_seconds": int(quantities.get("startup_timeout_seconds", 600)),
            "timeout_seconds": int(quantities.get("timeout_seconds", 120)),
            "retries": int(quantities.get("retries", 2)),
            "service_log": str(
                run_dir / "outputs" / "stage_05_resource_limits" / "grobid_quantities.log"
            ),
            "environment": {
                str(key): str(value)
                for key, value in (quantities.get("environment") or {}).items()
            },
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
