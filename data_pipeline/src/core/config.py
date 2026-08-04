from __future__ import annotations

import os
import sysconfig
from pathlib import Path
from typing import Any


def normalize_config(raw: dict[str, Any], base: Path) -> dict[str, Any]:
    """Expand the compact corpus configuration into the internal stage configuration."""

    if "pdf_directory" not in raw:
        return raw
    run_dir = _resolve(base, raw.get("run_directory", "runs/current"))
    pdf_directory = _resolve(base, raw["pdf_directory"])
    grobid = raw.get("grobid") or {}
    softcite = raw.get("softcite") or {}
    quantities = raw.get("grobid_quantities") or {}
    resource_interpretation = raw.get("resource_interpretation") or {}
    resource_limits = raw.get("resource_limits") or {}
    mineru = raw.get("mineru") or {}
    toolbox = raw.get("toolbox") or {}
    stage04 = raw.get("stage04") or {}
    stage05 = raw.get("stage05") or {}
    model_cache = _resolve(
        base, raw.get("model_cache_directory", "../.model_cache/data_pipeline")
    )
    model_cache_config = model_cache / "config"
    runtime_grobid_config = model_cache / "grobid-home" / "config" / "grobid.yaml"
    java_home = softcite.get("java_home") or grobid.get("java_home")
    mineru_environment = {
        "MINERU_MODEL_SOURCE": "local",
        "MINERU_TOOLS_CONFIG_JSON": str(model_cache / "mineru" / "mineru.json"),
    }
    mineru_environment.update(
        {str(key): str(value) for key, value in (mineru.get("environment") or {}).items()}
    )
    normalized_mineru = {
        "execute": bool(mineru.get("enabled", True)),
        "command": mineru.get("command", "mineru"),
        "method": "auto",
        "backend": mineru.get("backend", "pipeline"),
        "timeout_seconds": int(mineru.get("timeout_seconds", 3600)),
        "working_directory": str(
            _resolve(base, mineru["working_directory"])
            if mineru.get("working_directory")
            else model_cache
        ),
        "environment": mineru_environment,
        "extra_args": ["--formula", "true", "--table", "true"],
        "reuse_existing": bool(mineru.get("reuse_existing", True)),
        "min_markdown_chars": int(mineru.get("min_markdown_chars", 100)),
    }
    return {
        "source": {
            "mode": "corpus",
            "root": str(pdf_directory),
            "exclude_supplementary": bool(raw.get("exclude_supplementary", True)),
        },
        "workspace": str(run_dir / "outputs"),
        "log_file": str(run_dir / "outputs" / "pipeline.log"),
        "stop_after": raw.get("stop_after", "judge"),
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
            "start_command": grobid.get(
                "start_command",
                [
                    "./gradlew",
                    "--no-daemon",
                    "run",
                    f"--args=server {runtime_grobid_config}",
                ],
            ),
            "java_home": grobid.get("java_home"),
            "auto_start": bool(grobid.get("auto_start", True)),
            "startup_timeout_seconds": int(grobid.get("startup_timeout_seconds", 300)),
            "timeout_seconds": int(grobid.get("timeout_seconds", 900)),
            "retries": int(grobid.get("retries", 2)),
            "consolidate_header": int(grobid.get("consolidate_header", 0)),
            "consolidate_citations": int(grobid.get("consolidate_citations", 0)),
            "max_chars": int(grobid.get("max_chars", 2_000_000)),
            "reuse_existing": bool(grobid.get("reuse_existing", True)),
            "fallback": {
                "enabled": bool((grobid.get("fallback") or {}).get("enabled", True)),
                "output_dir": str(
                    run_dir / "outputs" / "stage_02_grobid_extract" / "fallback"
                ),
                "pdftotext_enabled": bool(
                    (grobid.get("fallback") or {}).get("pdftotext_enabled", True)
                ),
                "pdftotext_timeout_seconds": int(
                    (grobid.get("fallback") or {}).get("pdftotext_timeout_seconds", 300)
                ),
            },
        },
        "software_coverage": {
            "base_url": softcite.get("base_url", "http://127.0.0.1:8060"),
            "working_directory": str(
                _resolve(base, softcite.get("working_directory", "third_party/software-mentions"))
            ),
            "start_command": softcite.get(
                "start_command",
                [
                    "./gradlew",
                    "--no-daemon",
                    "run",
                    f"--args=server {model_cache_config / 'software-mentions.yml'}",
                ],
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
                        str(
                            _resolve(
                                base, softcite.get("delft_directory", "third_party/delft")
                            )
                        ),
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
            "aliases_file": str(
                _resolve(base, softcite.get("aliases_file", "assets/software_aliases.json"))
            ),
            "role_rules_file": str(
                _resolve(
                    base, softcite.get("role_rules_file", "assets/software_role_rules.json")
                )
            ),
            "capability_map_file": str(
                _resolve(
                    base,
                    softcite.get(
                        "capability_map_file", "assets/software_capability_map.json"
                    ),
                )
            ),
        },
        "resource_interpretation": {
            "enabled": bool(resource_interpretation.get("enabled", True)),
            "base_url": os.environ.get("RESOURCE_LLM_URL")
            or resource_interpretation.get("url", "https://api.deepseek.com/v1"),
            "api_key_env": resource_interpretation.get("api_key_env", "RESOURCE_LLM_API_KEY"),
            "model": os.environ.get("RESOURCE_LLM_MODEL_NAME")
            or resource_interpretation.get("model_name", "deepseek-v4-flash"),
            "timeout_seconds": int(resource_interpretation.get("timeout_seconds", 900)),
            "retries": int(resource_interpretation.get("retries", 2)),
            "thinking": resource_interpretation.get("thinking", "disabled"),
            "max_tokens": int(resource_interpretation.get("max_tokens", 3000)),
            "validation_retries": int(resource_interpretation.get("validation_retries", 1)),
        },
        "resource_limits": {
            "cpu_cores": float(resource_limits.get("cpu_cores", 500)),
            "gpus": float(resource_limits.get("gpus", 8)),
            "memory_gb": float(resource_limits.get("memory_gb", 1000)),
            "runtime_hours": float(resource_limits.get("runtime_hours", 12)),
        },
        "stage04": {"enabled": bool(stage04.get("enabled", True))},
        "grobid_quantities": {
            "base_url": quantities.get("base_url", "http://127.0.0.1:8062"),
            "working_directory": str(
                _resolve(base, quantities.get("working_directory", "third_party/grobid-quantities"))
            ),
            "start_command": quantities.get(
                "start_command",
                [
                    "./gradlew",
                    "--no-daemon",
                    "run",
                    f"--args=server {model_cache_config / 'grobid-quantities.yml'}",
                ],
            ),
            "java_home": quantities.get("java_home") or grobid.get("java_home"),
            "auto_start": bool(quantities.get("auto_start", True)),
            "startup_timeout_seconds": int(quantities.get("startup_timeout_seconds", 600)),
            "timeout_seconds": int(quantities.get("timeout_seconds", 120)),
            "retries": int(quantities.get("retries", 2)),
            "service_log": str(
                run_dir / "outputs" / "stage_04_resource_limits" / "grobid_quantities.log"
            ),
            "environment": {
                str(key): str(value) for key, value in (quantities.get("environment") or {}).items()
            },
        },
        "mineru": normalized_mineru,
        "toolbox": {
            "profile": str(_resolve(base, toolbox.get("file", "assets/toolbox.json"))),
            "enabled_software": toolbox.get("enabled_software", ["*"]),
            "enabled_actions": toolbox.get("enabled_actions", ["*"]),
            "priority_software": toolbox.get("priority_software", []),
            "preserve_priority_matches": True,
        },
        "stage05": {
            "enabled": bool(stage05.get("enabled", True)),
            "download_scope": _download_scope(stage05.get("download_scope", "all")),
            "enable_network": bool(stage05.get("enable_network", True)),
            "max_rounds": int(stage05.get("max_rounds", 3)),
            "max_archive_depth": int(stage05.get("max_archive_depth", 3)),
            "max_archive_children_per_archive": int(
                stage05.get("max_archive_children_per_archive", 300)
            ),
            "max_assets_per_paper": int(stage05.get("max_assets_per_paper", 500)),
            "max_clues_per_paper": int(stage05.get("max_clues_per_paper", 500)),
            "max_single_file_bytes": int(stage05.get("max_single_file_bytes", 10 * 1024**3)),
            "max_archive_expanded_bytes": int(
                stage05.get("max_archive_expanded_bytes", 50 * 1024**3)
            ),
            "max_archive_files": int(stage05.get("max_archive_files", 5000)),
            "max_text_chars": int(stage05.get("max_text_chars", 2_000_000)),
            "max_targets_per_clue": int(stage05.get("max_targets_per_clue", 200)),
            "network_workers": int(stage05.get("network_workers", 4)),
            "default_per_host_workers": int(stage05.get("default_per_host_workers", 2)),
            "per_host_workers": {
                str(host).casefold(): int(limit)
                for host, limit in (
                    stage05.get("per_host_workers")
                    or {
                        "api.crossref.org": 1,
                        "api.datacite.org": 2,
                        "api.openalex.org": 2,
                        "api.github.com": 2,
                        "api.osf.io": 1,
                        "zenodo.org": 2,
                    }
                ).items()
            },
            "request_retries": int(stage05.get("request_retries", 3)),
            "retry_backoff_seconds": float(stage05.get("retry_backoff_seconds", 1.0)),
            "retry_max_seconds": float(stage05.get("retry_max_seconds", 60.0)),
            "metadata_timeout_seconds": int(stage05.get("metadata_timeout_seconds", 30)),
            "download_timeout_seconds": int(stage05.get("download_timeout_seconds", 120)),
            "include_local_siblings": bool(stage05.get("include_local_siblings", True)),
            "query_metadata": bool(stage05.get("query_metadata", True)),
            "discover_publisher_supplements": bool(
                stage05.get("discover_publisher_supplements", True)
            ),
            "paper_limit": stage05.get("paper_limit"),
        },
        "stage06": _agent_stage(raw.get("stage06") or {}, "BUILDER_AGENT"),
        "stage07": _agent_stage(raw.get("stage07") or {}, "JUDGE_AGENT"),
    }


def _agent_stage(stage: dict[str, Any], prefix: str) -> dict[str, Any]:
    agent = stage.get("agent") or {}
    cli_override = os.environ.get(f"{prefix}_CLI")
    cli = cli_override or agent.get("cli", "opencode")
    command = os.environ.get(f"{prefix}_COMMAND")
    if not command:
        command = cli if cli_override else agent.get("command") or cli
    return {
        "enabled": bool(stage.get("enabled", True)),
        "max_agent_readable_bytes": int(stage.get("max_agent_readable_bytes", 50 * 1024**2)),
        "agent": {
            "cli": cli,
            "command": command,
            "model": os.environ.get(f"{prefix}_MODEL")
            or agent.get("model", "deepseek/deepseek-v4-flash"),
            "base_url": os.environ.get(f"{prefix}_BASE_URL")
            or agent.get("base_url")
            or os.environ.get("OPENCODE_BASE_URL_VALUE")
            or os.environ.get("JUDGE_API_BASE"),
            "api_key_env": agent.get("api_key_env", "JUDGE_API_KEY"),
            "timeout_seconds": int(agent.get("timeout_seconds", 1800)),
            "retries": int(agent.get("retries", 2)),
            "max_output_chars": int(agent.get("max_output_chars", 200_000)),
            "preserve_conversation": True,
            "isolate_workspace": True,
            "environment": {
                str(key): str(value) for key, value in (agent.get("environment") or {}).items()
            },
        },
    }


def _download_scope(value: Any) -> str:
    scope = str(value).casefold()
    if scope not in {"all", "supplementary_only"}:
        raise ValueError("stage05.download_scope must be 'all' or 'supplementary_only'")
    return scope


def _resolve(base: Path, value: str | Path) -> Path:
    path = Path(value).expanduser()
    return path.resolve() if path.is_absolute() else (base / path).resolve()
