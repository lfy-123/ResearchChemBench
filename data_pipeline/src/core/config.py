from __future__ import annotations

import os
import sys
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
    stage01 = raw.get("stage01") or {}
    stage05 = raw.get("stage05") or {}
    stage00_remote = raw.get("stage00_remote_corpus") or {}
    stage03_relevance = raw.get("stage03_computation_relevance") or {}
    stage03_llm = stage03_relevance.get("llm") or {}
    stage04_supplementary = raw.get("stage04_supplementary_acquisition") or {}
    stage05_preliminary = raw.get("stage05_preliminary_coverage") or {}
    stage06_supplementary = raw.get("stage06_supplementary_extraction") or {}
    microbatch = raw.get("microbatch") or {}
    model_cache = _resolve(base, raw.get("model_cache_directory", ".model_cache"))
    model_cache_config = model_cache / "config"
    runtime_grobid_config = model_cache / "grobid-home" / "config" / "grobid.yaml"
    java_home = softcite.get("java_home") or grobid.get("java_home")
    mineru_environment = {
        "MINERU_MODEL_SOURCE": "local",
        "MINERU_TOOLS_CONFIG_JSON": str(model_cache / "mineru" / "mineru.json"),
        "LD_LIBRARY_PATH": os.pathsep.join(
            [str(Path(sys.prefix) / "lib"), os.environ.get("LD_LIBRARY_PATH", "")]
        ).strip(os.pathsep),
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
        "max_pages": int(mineru.get("max_pages", 100)),
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
            "exclude_supplementary": False,
        },
        "workspace": str(run_dir / "outputs"),
        "log_file": str(run_dir / "outputs" / "pipeline.log"),
        "stop_after": raw.get("stop_after", "stage08"),
        "resume_completed_stages": bool(raw.get("resume_completed_stages", False)),
        "stage00_remote_corpus": {
            "enabled": bool(stage00_remote.get("enabled", False)),
            "dataset": stage00_remote.get("dataset", "en-paper-hzzj"),
            "count": max(1, int(stage00_remote.get("count", 1000))),
            "output_directory": str(
                _resolve(
                    base,
                    stage00_remote.get(
                        "output_directory", run_dir / "stage_00_remote_corpus"
                    ),
                )
            ),
            "credentials": str(
                _resolve(
                    base,
                    stage00_remote.get(
                        "credentials",
                        "/mnt/shared-storage-user/liyuqiang/benchmark/pipline_demo/pdfs/xinghe.txt",
                    ),
                )
            ),
            "outside": bool(stage00_remote.get("outside", False)),
            "resume": bool(stage00_remote.get("resume", True)),
            "selection": stage00_remote.get("selection", "remote_order"),
            "seed": int(stage00_remote.get("seed", 0)),
            "copy_existing_supplementary": bool(
                stage00_remote.get("copy_existing_supplementary", True)
            ),
        },
        "microbatch": {
            "enabled": bool(microbatch.get("enabled", False)),
            "size": max(1, int(microbatch.get("size", 10))),
            "concurrency": max(1, int(microbatch.get("concurrency", 5))),
            "resume": bool(microbatch.get("resume", True)),
            "stage_limits": {
                str(stage): max(1, int(limit))
                for stage, limit in (microbatch.get("stage_limits") or {}).items()
            },
            "softcite_instances": microbatch.get("softcite_instances", "auto"),
        },
        "stage01": {"workers": max(1, int(stage01.get("workers", 1)))},
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
            "workers": max(1, int(grobid.get("workers", 1))),
            "fallback": {
                "enabled": bool((grobid.get("fallback") or {}).get("enabled", True)),
                "output_dir": str(run_dir / "outputs" / "stage_02_grobid_extract" / "fallback"),
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
            "workers": max(1, int(softcite.get("workers", 1))),
            "service_log": str(
                run_dir / "outputs" / "stage_05_preliminary_coverage" / "softcite_service.log"
            ),
            "environment": {
                "CONDA_PREFIX": str(
                    softcite.get("conda_prefix") or os.environ.get("CONDA_PREFIX") or sys.prefix
                ),
                "PYTHONPATH": os.pathsep.join(
                    [
                        str(_resolve(base, softcite.get("delft_directory", "third_party/delft"))),
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
                _resolve(base, softcite.get("role_rules_file", "assets/software_role_rules.json"))
            ),
            "capability_map_file": str(
                _resolve(
                    base,
                    softcite.get("capability_map_file", "assets/software_capability_map.json"),
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
        "stage04": {
            "enabled": bool(stage04.get("enabled", True)),
            "workers": max(1, int(stage04.get("workers", 1))),
        },
        "stage03_computation_relevance": {
            "method_ontology": str(
                _resolve(
                    base,
                    stage03_relevance.get(
                        "method_ontology", "assets/computational_method_ontology.yaml"
                    ),
                )
            ),
            "evidence_rules": str(
                _resolve(
                    base,
                    stage03_relevance.get(
                        "evidence_rules", "assets/computation_evidence_rules.yaml"
                    ),
                )
            ),
            "negative_contexts": str(
                _resolve(
                    base,
                    stage03_relevance.get(
                        "negative_contexts", "assets/computation_negative_contexts.yaml"
                    ),
                )
            ),
            "continue_decisions": stage03_relevance.get(
                "continue_decisions", ["strong_candidate", "weak_candidate", "rule_error"]
            ),
            "use_llm": bool(stage03_relevance.get("use_llm", False)),
            "workers": max(1, int(stage03_relevance.get("workers", 1))),
            "llm": {
                "enabled": bool(stage03_relevance.get("use_llm", False)),
                "managed_rlaunch": bool(stage03_llm.get("managed_rlaunch", False)),
                "required": bool(stage03_llm.get("required", False)),
                "base_url": os.environ.get("STAGE03_LLM_BASE_URL")
                or stage03_llm.get("base_url", "http://127.0.0.1:18083/v1"),
                "api_key_env": stage03_llm.get("api_key_env", "STAGE03_LLM_API_KEY"),
                "model": os.environ.get("STAGE03_LLM_MODEL")
                or stage03_llm.get("model", "qwen3-30b-a3b-instruct-2507"),
                "concurrency": max(1, int(stage03_llm.get("concurrency", 16))),
                "timeout_seconds": int(stage03_llm.get("timeout_seconds", 300)),
                "health_timeout_seconds": int(stage03_llm.get("health_timeout_seconds", 15)),
                "retries": max(0, int(stage03_llm.get("retries", 2))),
                "max_tokens": max(64, int(stage03_llm.get("max_tokens", 1024))),
                "thinking": str(stage03_llm.get("thinking") or "") or None,
                "max_prompt_chars": max(
                    4_000, int(stage03_llm.get("max_prompt_chars", 24_000))
                ),
                "cache_directory": str(
                    _resolve(
                        base,
                        stage03_llm.get(
                            "cache_directory",
                            run_dir / "outputs" / "stage_03_computation_relevance" / "llm_cache",
                        ),
                    )
                ),
                "manager_script": str(
                    _resolve(
                        base,
                        stage03_llm.get(
                            "manager_script", "scripts/stage03_llm/manage_rlaunch_worker.sh"
                        ),
                    )
                ),
                "state_file": str(
                    _resolve(
                        base,
                        stage03_llm.get(
                            "state_file", ".stage03_llm_worker.local.json"
                        ),
                    )
                ),
                "cpu": max(1, int(stage03_llm.get("cpu", 16))),
                "memory_mib": max(1, int(stage03_llm.get("memory_mib", 196000))),
                "charged_group": stage03_llm.get("charged_group", "ai4chem_gpu"),
                "positive_tag": stage03_llm.get("positive_tag", "h200"),
                "image": stage03_llm.get(
                    "image",
                    "registry.h.pjlab.org.cn/ailab-ai4chem-ai4chem_gpu/"
                    "chemllm-workspace:test1-20260425150803",
                ),
                "skip_bootstrap": bool(stage03_llm.get("skip_bootstrap", True)),
                "skip_download": bool(stage03_llm.get("skip_download", True)),
            },
        },
        "stage04_supplementary_acquisition": {
            "enabled": bool(stage04_supplementary.get("enabled", True)),
            "enable_network": bool(stage04_supplementary.get("enable_network", True)),
            "publisher_adapters": stage04_supplementary.get(
                "publisher_adapters", ["acs", "rsc", "elsevier", "wiley", "nature", "mdpi"]
            ),
            "allowed_extensions": stage04_supplementary.get(
                "allowed_extensions", ["pdf", "docx", "zip", "xlsx", "csv", "txt", "cif"]
            ),
            "max_attachments_per_paper": int(
                stage04_supplementary.get("max_attachments_per_paper", 20)
            ),
            "max_file_bytes": int(
                stage04_supplementary.get("max_file_bytes", 100 * 1024**2)
            ),
            "max_total_bytes_per_paper": int(
                stage04_supplementary.get("max_total_bytes_per_paper", 250 * 1024**2)
            ),
            "download_timeout_seconds": int(
                stage04_supplementary.get("download_timeout_seconds", 120)
            ),
            "read_timeout_seconds": int(
                stage04_supplementary.get("read_timeout_seconds", 20)
            ),
            "connect_timeout_seconds": int(
                stage04_supplementary.get("connect_timeout_seconds", 15)
            ),
            "paper_timeout_seconds": int(
                stage04_supplementary.get("paper_timeout_seconds", 180)
            ),
            "workers": max(1, int(stage04_supplementary.get("workers", 4))),
        },
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
        "stage05_preliminary_coverage": {
            "capability_catalog": str(
                _resolve(
                    base,
                    stage05_preliminary.get(
                        "capability_catalog", "assets/toolbox_capabilities.json"
                    ),
                )
            ),
            "continue_without_software_name": True,
            "unknown_capability_policy": "continue_low_priority",
            "softcite_instances": max(
                1, int(stage05_preliminary.get("softcite_instances", 1))
            ),
        },
        "stage06_supplementary_extraction": {
            "pdftotext_command": stage06_supplementary.get(
                "pdftotext_command", "pdftotext"
            ),
            "pdftotext_timeout_seconds": int(
                stage06_supplementary.get("pdftotext_timeout_seconds", 300)
            ),
            "minimum_text_quality": float(
                stage06_supplementary.get("minimum_text_quality", 60)
            ),
            "workers": max(1, int(stage06_supplementary.get("workers", 1))),
        },
        "stage06": _agent_stage(raw.get("stage06") or {}, "BUILDER_AGENT"),
        "stage07": _agent_stage(raw.get("stage07") or {}, "JUDGE_AGENT"),
        "stage07_builder": _agent_stage(
            raw.get("stage07_builder") or {}, "BUILDER_AGENT"
        ),
        "stage08_judge": _agent_stage(raw.get("stage08_judge") or {}, "JUDGE_AGENT"),
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
