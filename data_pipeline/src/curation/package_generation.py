from __future__ import annotations

import json
import os
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any

from src.core.assets import prompt_example
from src.core.logging import log_progress
from src.core.models import selected_task_type
from src.curation.llm_client import call_json_chat
from src.curation.package_validation import package_readiness
from src.curation.source_excerpt import evidence_excerpt


def generate_complete_packages(
    records: list[dict[str, Any]], config: dict[str, Any] | None
) -> list[dict[str, Any]]:
    """Create exactly one public task and one hidden reference package per study."""

    config = config or {}
    enabled = bool(config.get("enabled", False))
    workers = max(1, min(int(config.get("max_workers", 1)), len(records) or 1))
    if workers == 1:
        output = []
        for index, record in enumerate(records, start=1):
            generated = _generate_record(record, config, enabled)
            output.append(generated)
            log_progress(
                "stage_14_package_generation",
                index,
                len(records),
                record.get("paper_id", str(index)),
                status=(generated.get("package_generation") or {}).get("status"),
            )
        return output
    with ThreadPoolExecutor(max_workers=workers) as executor:
        output = []
        for index, generated in enumerate(
            executor.map(lambda record: _generate_record(record, config, enabled), records),
            start=1,
        ):
            output.append(generated)
            log_progress(
                "stage_14_package_generation",
                index,
                len(records),
                generated.get("paper_id", str(index)),
                status=(generated.get("package_generation") or {}).get("status"),
            )
        return output


def _generate_record(
    record: dict[str, Any], config: dict[str, Any], enabled: bool
) -> dict[str, Any]:
    updated = dict(record)
    task_type = selected_task_type(record)
    if not task_type:
        updated["package_generation"] = {
            "status": "failed",
            "error": "selected_task_type is required before package generation",
        }
        return updated
    if record.get("benchmark_package"):
        report = package_readiness(record, task_type)
        updated["package_generation"] = {
            "status": "curator_supplied" if report["passed"] else "invalid_candidate",
            "source": "curator_supplied",
            "task_type": task_type,
            "validation": report,
        }
        return updated
    if not enabled:
        updated["package_generation"] = {
            "status": "disabled",
            "task_type": task_type,
            "reason": "enable package_generation or provide a curator benchmark_package",
        }
        return updated
    try:
        package, source, calls = _generate_validated(record, task_type, config)
        candidate = {**record, "benchmark_package": package}
        report = package_readiness(candidate, task_type)
        updated["package_generation"] = {
            "status": "complete" if report["passed"] else "invalid_candidate",
            "source": source,
            "task_type": task_type,
            "validation": report,
            "candidate": package,
            "llm_calls": calls,
        }
        if report["passed"]:
            updated["benchmark_package"] = package
    except Exception as exc:
        updated["package_generation"] = {
            "status": "failed",
            "task_type": task_type,
            "error": f"{type(exc).__name__}: {exc}",
        }
    return updated


def package_generation_summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    statuses = Counter(
        (record.get("package_generation") or {}).get("status", "missing") for record in records
    )
    invalid = Counter()
    for record in records:
        report = (record.get("package_generation") or {}).get("validation") or {}
        if report and not report.get("passed"):
            invalid[record.get("selected_task_type", "unknown")] += 1
    return {
        "records": len(records),
        "statuses": dict(statuses),
        "invalid_task_types": dict(invalid),
    }


def generation_prompt(task_type: str, examples_path: str | Path | None = None) -> str:
    disclosure = {
        "paper_reproduction": (
            "Disclose the source-grounded method, parameters, and workflow. Hide author numerical outputs "
            "and conclusions. A method_protocol is mandatory."
        ),
        "conclusion_guided_reconstruction": (
            "Disclose the target high-level conclusion and starting evidence, but hide the paper route and "
            "paper numerical outputs. Accept scientifically valid alternative verification routes."
        ),
        "autonomous_research": (
            "Disclose the bounded scientific objective, materialized inputs, and starting observations. Hide "
            "the paper route, conclusion, hypothesis ranking, and computed outputs."
        ),
        "mechanistic_rule_discovery": (
            "Disclose comparable training systems and their permitted input observables. Hide the final rule, "
            "held-out outcomes, and applicability boundary. A held-out prediction contract is mandatory."
        ),
    }[task_type]
    example = (
        prompt_example(task_type, examples_path) if examples_path else prompt_example(task_type)
    )
    return f"""You construct one source-grounded computational-chemistry benchmark task of type {task_type}.
{disclosure}

Return JSON only with top-level key benchmark_package. Use this canonical single-task shape:
- task_id: stable solver-facing ID.
- task_instruction: source-anonymous instruction with no hidden answer values.
- scientific_requirements: non-empty executable requirements.
- required_deliverables: optional list of path/description objects.
- public_inputs: materializable reaction, molecular_systems, observations, files, and task-specific fields.
  files must be a mapping from relative file name to complete inline content or JSON data. Never place a file
  description, imaginary path, downloadable URL, or unavailable directory in files; put such gaps in
  unavailable_inputs and allow validation to reject the draft.
  conclusion_guided_reconstruction requires target_conclusion; mechanistic_rule_discovery requires at least
  three training_systems and heldout_systems whose outcomes remain hidden.
- method_protocol: required only for paper_reproduction.
- leakage_markers: hidden answer phrases/numbers as one list.
- ground_truth.expected_result: reference findings, quantitative ranges, uncertainty, and unresolved points.
- ground_truth.expected_structured_output: machine-readable answer contract.
- ground_truth.scientific_conclusion_rubric: 3-10 ScoredFinding criteria. Each has id, max_score,
  statement, acceptance_rule, required_evidence, and evidence_class (required/alternative/error). Total=100.
- ground_truth.evidence_gates, critical_failures, managed_computation_policy, and reference_evidence.
- mechanistic_rule_discovery additionally requires heldout_design and hidden heldout_predictions.

Rules:
1. Every scientific fact must be traceable to supplied text or a registered source artifact. Do not invent files,
   structures, parameters, calculations, or gold values. Explicitly mark unavailable material.
2. The public package must contain enough real input data for an agent to start without internet access.
3. Reference findings are evaluation anchors, not unique scientific truth. Artifact-supported extra findings are allowed.
4. Score scientific results and evidence, not similarity to the paper's software sequence, except protocol fidelity in
   paper_reproduction. Use a full evidence DAG only when the source genuinely contains a multi-stage mechanism or rule.
5. The package remains a draft until deterministic checks, reference execution, independent review, agent pilots,
   and human approval are complete.
6. Keep the package compact. Use 3-10 scored findings and include only evidence needed to solve or score the task;
   do not reproduce long paper passages or duplicate the same fact across fields.

Complete structural example for this task type (imitate disclosure and package structure, never copy its chemistry):
{example}
"""


def _generate_one(
    record: dict[str, Any],
    task_type: str,
    config: dict[str, Any],
    repair_errors: list[str] | None = None,
) -> tuple[dict[str, Any], str, dict[str, Any]]:
    cache_dir = config.get("cache_dir")
    if cache_dir and not repair_errors:
        path = Path(cache_dir).expanduser() / f"{record['paper_id']}.json"
        if path.is_file():
            value = json.loads(path.read_text(encoding="utf-8"))
            calls = value.get("llm_calls", [])
            return value.get("benchmark_package", value), "api_cache", calls[-1] if calls else {}
    offline_dir = config.get("offline_package_dir")
    if offline_dir:
        path = Path(offline_dir).expanduser() / f"{record['paper_id']}.json"
        if path.is_file():
            value = json.loads(path.read_text(encoding="utf-8"))
            return value.get("benchmark_package", value), "offline_file", {}

    api_key = config.get("api_key")
    if not api_key and config.get("api_key_env"):
        api_key = os.environ.get(config["api_key_env"])
    api_key = api_key or os.environ.get("RCB_LLM_API_KEY")
    if not api_key:
        raise ValueError("missing package-generation API key and no offline package file")

    model = str(config["model"])
    base_url = str(config.get("base_url", "https://api.openai.com/v1")).rstrip("/")
    packet = _source_packet(record, task_type, int(config.get("max_source_chars", 120_000)))
    if repair_errors:
        packet["repair_request"] = {
            "validation_errors": repair_errors,
            "instruction": "Return a corrected complete package. Preserve grounded content and fix every listed error.",
        }
    value, metadata = call_json_chat(
        model=model,
        base_url=base_url,
        api_key=api_key,
        system_prompt=generation_prompt(task_type, config.get("prompt_examples")),
        user_content=json.dumps(packet, ensure_ascii=False),
        timeout_seconds=float(config.get("timeout_seconds", 600)),
        max_tokens=config.get("max_tokens"),
        retries=int(config.get("retries", 2)),
        thinking=config.get("thinking"),
    )
    return value.get("benchmark_package", value), f"api:{model}", metadata


def _generate_validated(
    record: dict[str, Any], task_type: str, config: dict[str, Any]
) -> tuple[dict[str, Any], str, list[dict[str, Any]]]:
    calls: list[dict[str, Any]] = []
    package, source, metadata = _generate_one(record, task_type, config)
    if metadata:
        calls.append(metadata)
    report = package_readiness({**record, "benchmark_package": package}, task_type)
    for _ in range(int(config.get("repair_attempts", 1))):
        if report["passed"]:
            break
        package, source, metadata = _generate_one(record, task_type, config, report["errors"])
        if metadata:
            calls.append(metadata)
        report = package_readiness({**record, "benchmark_package": package}, task_type)
    cache_dir = config.get("cache_dir")
    if cache_dir and report["passed"]:
        path = Path(cache_dir).expanduser() / f"{record['paper_id']}.json"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(
                {"benchmark_package": package, "llm_calls": calls}, ensure_ascii=False, indent=2
            )
            + "\n",
            encoding="utf-8",
        )
    return package, source, calls


def _source_packet(record: dict[str, Any], task_type: str, max_source_chars: int) -> dict[str, Any]:
    assets = record.get("assets") or {}
    source_text = evidence_excerpt(assets.get("text", []), max_source_chars)
    public_record = {
        key: value
        for key, value in record.items()
        if key
        not in {"benchmark_package", "package_generation", "quality_funnel", "model_ensemble"}
    }
    visible = assets.get("visible_data") or {}
    return {
        "record": public_record,
        "selected_task_type": task_type,
        "selection_reason": record.get("selection_reason"),
        "source_text": source_text,
        "visible_asset_paths": visible.get(task_type, visible.get("all", [])),
        "hidden_reference_file_names": [
            Path(path).name for path in assets.get("hidden_reference_files", [])
        ],
    }
