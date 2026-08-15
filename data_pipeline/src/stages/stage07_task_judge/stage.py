from __future__ import annotations

import json
import time
import uuid
from pathlib import Path
from typing import Any

import jsonschema

from src.agents import AgentExecutionError, AgentRunRequest, create_agent_harness
from src.agents.schemas import STAGE07_AUDIT_SCHEMA
from src.agents.workspace import (
    IGNORED_MANIFEST_NAMES,
    agent_recovery_context,
    copy_recovery_artifacts,
    copytree_exact,
    directory_manifest,
    input_fingerprint,
    make_read_only,
    prepare_clean_directory,
    recovery_instructions,
    write_manifest,
)
from src.contracts import (
    canonical_hash,
    decision_counts,
    now_utc,
    read_json,
    record_header,
    safe_component,
    write_json,
    write_jsonl,
)
from src.core.concurrency import ordered_parallel_map
from src.stages.stage07_task_judge.prompts import (
    STAGE07_AUDIT_VERSION,
    audit_instructions,
)
from src.stages.stage07_task_judge.validation import (
    deterministic_stage07_audit,
    merge_audit_outcomes,
    validate_agent_audit,
)

STAGE07_IMPLEMENTATION_VERSION = "v4-scope-complexity-objective-audit-20260815-r1"
STAGE07_DIRECTORY = "stage_07_task_audit"
STAGE07_IGNORED_PAIR_FILES = {*IGNORED_MANIFEST_NAMES, "construction_record.json"}


def run_stage07(*, build_records, documents, config, model, workspace: Path, run_id: str):
    stage_root = workspace / STAGE07_DIRECTORY
    stage_root.mkdir(parents=True, exist_ok=True)
    eligible = [
        row for row in build_records if row.get("decision") == "constructed" and row.get("passed")
    ]
    model_config = dict(getattr(model, "config", {}) or {})
    harness_name = str(config.get("harness") or "codex")
    harness = create_agent_harness(
        harness_name,
        config=config,
        model_config=model_config,
        model_client=model,
    )

    def audit(record: dict[str, Any]) -> dict[str, Any]:
        paper_id = str(record["paper_id"])
        task_pair_id = str(record["task_pair_id"])
        pair_root = Path(str(record["task_pair_path"])).expanduser().resolve()
        try:
            if not pair_root.is_dir():
                return _audit_failure(
                    run_id,
                    paper_id,
                    task_pair_id,
                    "task_pair_missing",
                    f"Stage06 task pair directory is missing: {pair_root}",
                )
            deterministic = deterministic_stage07_audit(pair_root)
            pair_manifest = _audit_pair_manifest(pair_root)
            response, agent_run = _run_audit_agent(
                harness=harness,
                stage_root=stage_root,
                paper_id=paper_id,
                task_pair_id=task_pair_id,
                pair_root=pair_root,
                pair_manifest=pair_manifest,
                deterministic=deterministic,
                config=config,
            )
            validation_findings = validate_agent_audit(response)
            model_outcomes = list(response.get("outcomes") or [])
            if validation_findings:
                model_outcomes.extend(
                    {
                        "type": "acceptance_rule_invalid",
                        "severity": "blocking",
                        "scope": "hidden_reference",
                        "details": finding,
                        "evidence_refs": [],
                        "source": "agent_contract_validation",
                    }
                    for finding in validation_findings
                )
            outcomes = merge_audit_outcomes(deterministic.get("outcomes") or [], model_outcomes)
            summary = "issues_found" if outcomes else "passed_audit"
            target = stage_root / "audits" / safe_component(paper_id)
            target.mkdir(parents=True, exist_ok=True)
            private_report = {
                "paper_id": paper_id,
                "task_pair_id": task_pair_id,
                "audit_summary": summary,
                "outcomes": outcomes,
                "checks": response.get("checks") or [],
                "toolbox_assessment": response.get("toolbox_assessment") or {},
                "cost_assessment": response.get("cost_assessment") or {},
                "rationale": response.get("rationale") or "",
                "deterministic_audit": deterministic,
                "agent_run": agent_run,
                "validation_findings": validation_findings,
            }
            write_json(target / "private_audit_details.json", private_report)
            write_json(
                target / "audit_summary.json",
                {
                    "paper_id": paper_id,
                    "task_pair_id": task_pair_id,
                    "audit_summary": summary,
                    "outcomes": [
                        {
                            key: outcome.get(key)
                            for key in ("type", "severity", "scope", "source")
                        }
                        for outcome in outcomes
                    ],
                },
            )
            (target / "public_audit_report.md").write_text(
                _public_audit_report(task_pair_id, summary, outcomes), encoding="utf-8"
            )
            write_json(
                target / "toolbox_gap_report.json",
                {
                    "outcomes": [
                        row
                        for row in outcomes
                        if row.get("type") in {"needs_software", "toolbox_capability_unknown"}
                    ],
                    "assessment": response.get("toolbox_assessment") or {},
                },
            )
            write_json(
                target / "cost_risk_report.json",
                {
                    "outcomes": [
                        row for row in outcomes if row.get("type") == "task_cost_too_high"
                    ],
                    "assessment": response.get("cost_assessment") or {},
                },
            )
            write_manifest(target, target / "audit_manifest.json")
            return {
                **record_header(run_id=run_id, stage="stage07", paper_id=paper_id),
                "task_pair_id": task_pair_id,
                "processing_status": "completed",
                "decision": summary,
                "audit_summary": summary,
                "passed": summary == "passed_audit",
                "outcomes": outcomes,
                "outcome_types": sorted({str(row.get("type")) for row in outcomes}),
                "audit_path": str(target),
                "agent_harness": harness.name,
                "agent_model": harness.model,
            }
        except AgentExecutionError as exc:
            return _audit_failure(
                run_id,
                paper_id,
                task_pair_id,
                exc.failure_class,
                str(exc),
                agent_run=exc.result.audit_record() if exc.result else None,
                retryable=exc.retryable,
            )
        except (FileNotFoundError, OSError) as exc:
            return _audit_failure(
                run_id,
                paper_id,
                task_pair_id,
                "audit_input_unavailable",
                f"{type(exc).__name__}: {exc}",
            )
        except Exception as exc:
            return _audit_failure(
                run_id,
                paper_id,
                task_pair_id,
                "audit_processing_error",
                f"{type(exc).__name__}: {exc}",
            )

    records = ordered_parallel_map(
        audit,
        eligible,
        max_workers=int(config.get("workers", 1)),
    )
    write_jsonl(stage_root / "audit_results.jsonl", records)
    summary = {
        **record_header(run_id=run_id, stage="stage07"),
        "implementation_version": STAGE07_IMPLEMENTATION_VERSION,
        "task_pairs": len(records),
        "passed_audit": sum(row.get("audit_summary") == "passed_audit" for row in records),
        "issues_found": sum(row.get("audit_summary") == "issues_found" for row in records),
        "audit_failed_retryable": sum(
            row.get("audit_summary") == "audit_failed_retryable" for row in records
        ),
        "decisions": decision_counts(records, "audit_summary"),
        "outcome_counts": _outcome_counts(records),
        "agent_harness": harness.name,
        "agent_model": harness.model,
    }
    write_json(stage_root / "stage_summary.json", summary)
    return {"records": records, "summary": summary}


def _run_audit_agent(
    *,
    harness,
    stage_root: Path,
    paper_id: str,
    task_pair_id: str,
    pair_root: Path,
    pair_manifest: dict[str, Any],
    deterministic: dict[str, Any],
    config: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    toolbox = _toolbox_snapshot_from_pair(pair_root, config)
    resource_policy = config.get("resource_policy") or {}
    fingerprint = input_fingerprint(
        {
            "pair_manifest_hash": pair_manifest["content_hash"],
            "deterministic": deterministic,
            "toolbox": toolbox,
            "resource_policy": resource_policy,
            "prompt_version": STAGE07_AUDIT_VERSION,
            "harness": harness.name,
            "model": harness.model,
        }
    )
    checkpoint = stage_root / "checkpoints" / safe_component(paper_id) / "objective_audit.json"
    if bool(config.get("resume", True)) and checkpoint.is_file():
        cached = read_json(checkpoint)
        cached_fingerprint = cached.get("input_fingerprint")
        legacy_fingerprint = input_fingerprint(
            {
                "pair_manifest_hash": directory_manifest(pair_root)["content_hash"],
                "deterministic": deterministic,
                "prompt_version": STAGE07_AUDIT_VERSION,
                "harness": harness.name,
                "model": harness.model,
            }
        )
        stable_input_match = _cached_audit_inputs_match(
            cached,
            stage_root=stage_root,
            pair_manifest_hash=str(pair_manifest["content_hash"]),
            toolbox=toolbox,
            resource_policy=resource_policy,
            harness_name=harness.name,
            model_name=harness.model,
        )
        if cached_fingerprint in {fingerprint, legacy_fingerprint} or stable_input_match:
            response = cached.get("response")
            jsonschema.validate(response, STAGE07_AUDIT_SCHEMA)
            if cached_fingerprint != fingerprint:
                cached["input_fingerprint"] = fingerprint
                write_json(checkpoint, cached)
            return response, {**(cached.get("agent_run") or {}), "cache_hit": True}

    attempts = max(1, int(config.get("max_attempts", 3)))
    last_error: AgentExecutionError | None = None
    recovery_context: str | None = None
    recovery_workspace: Path | None = None
    for attempt in range(1, attempts + 1):
        root = prepare_clean_directory(
            stage_root
            / "workspaces"
            / safe_component(paper_id)
            / "objective_audit"
            / f"attempt-{attempt:02d}-{uuid.uuid4().hex[:8]}"
        )
        inputs = root / "inputs"
        inputs.mkdir(parents=True, exist_ok=True)
        copytree_exact(pair_root, inputs / "task_pair")
        audit_packet = _stage07_audit_packet(
            pair_root=pair_root,
            pair_manifest=pair_manifest,
            deterministic=deterministic,
            toolbox=toolbox,
            resource_policy=resource_policy,
        )
        write_json(inputs / "toolbox_snapshot.json", toolbox)
        write_json(inputs / "resource_policy.json", resource_policy)
        write_json(inputs / "deterministic_audit.json", deterministic)
        write_json(inputs / "audit_packet.json", audit_packet)
        write_json(
            inputs / "objective_audit_scaffold.json",
            _stage07_audit_scaffold(deterministic, audit_packet),
        )
        (inputs / "initialize_objective_audit.py").write_text(
            _stage07_audit_initializer_script(), encoding="utf-8"
        )
        make_read_only(inputs)
        max_tool_calls = int(
            config.get("audit_max_tool_calls", config.get("max_tool_calls", 16))
        )
        if recovery_context:
            max_tool_calls = min(
                max_tool_calls,
                int(
                    config.get(
                        "audit_recovery_max_tool_calls",
                        config.get("recovery_max_tool_calls", 8),
                    )
                ),
            )
        max_tool_calls = max(2, max_tool_calls)
        finalization_reserve = min(
            max_tool_calls - 1,
            max(
                1,
                int(config.get("audit_finalization_reserve", max_tool_calls - 1)),
            ),
        )
        instructions = audit_instructions(
            paper_id=paper_id,
            task_pair_id=task_pair_id,
            manifest_hash=pair_manifest["content_hash"],
            max_tool_calls=max_tool_calls,
            finalization_reserve=finalization_reserve,
        )
        if recovery_context:
            (root / "RECOVERY_CONTEXT.md").write_text(recovery_context, encoding="utf-8")
            copy_recovery_artifacts(recovery_workspace, root)
            instructions += recovery_instructions(
                "stage07_objective_audit", max_tool_calls=max_tool_calls
            )
        request = AgentRunRequest(
            phase="stage07_objective_audit",
            record_id=task_pair_id,
            workspace=root,
            instructions=instructions,
            output_schema=STAGE07_AUDIT_SCHEMA,
            prompt_version=STAGE07_AUDIT_VERSION,
            timeout_seconds=int(config.get("timeout_seconds", 3600)),
            metadata={
                "paper_id": paper_id,
                "task_pair_id": task_pair_id,
                "max_tool_calls": max_tool_calls,
                "finalization_reserve": finalization_reserve,
                "inline_contract": False,
                "structured_artifact_path": "outputs/objective_audit.json",
                "recovery_attempt": bool(recovery_context),
            },
        )
        try:
            result = harness.run(request)
            semantic_findings = validate_agent_audit(result.response or {})
            if semantic_findings:
                message = (
                    "Stage07 Agent contract failed semantic validation: "
                    + ", ".join(semantic_findings)
                )
                result.status = "failed"
                result.failure_class = "invalid_phase_contract"
                result.retryable = True
                result.error = {
                    "error_type": "InvalidPhaseContract",
                    "message": message[:4000],
                }
                write_json(root / "agent_run.json", result.audit_record())
                raise AgentExecutionError(
                    message,
                    failure_class="invalid_phase_contract",
                    retryable=True,
                    result=result,
                )
        except AgentExecutionError as exc:
            last_error = exc
            if not exc.retryable or attempt >= attempts:
                raise
            recovery_context = agent_recovery_context(exc.result)
            recovery_workspace = (
                Path(exc.result.workspace) if exc.result and exc.result.workspace else None
            )
            delay = min(
                float(config.get("retry_max_seconds", 30)),
                float(config.get("retry_backoff_seconds", 2)) * (2 ** (attempt - 1)),
            )
            if delay > 0:
                time.sleep(delay)
            continue
        write_json(
            checkpoint,
            {
                "paper_id": paper_id,
                "task_pair_id": task_pair_id,
                "input_fingerprint": fingerprint,
                "prompt_version": STAGE07_AUDIT_VERSION,
                "response": result.response,
                "agent_run": result.audit_record(),
                "completed_at": now_utc(),
            },
        )
        return result.response or {}, {**result.audit_record(), "cache_hit": False}
    if last_error is not None:
        raise last_error
    raise RuntimeError("Stage07 Agent audit did not execute")


def _audit_pair_manifest(pair_root: Path) -> dict[str, Any]:
    """Hash task semantics without volatile Stage06 execution provenance."""

    manifest = directory_manifest(
        pair_root,
        ignored_names=STAGE07_IGNORED_PAIR_FILES,
    )
    semantic_files: list[dict[str, str]] = []
    for row in manifest["files"]:
        semantic_hash = str(row["sha256"])
        if row["path"] == "paper_info.json":
            paper_info = read_json(pair_root / "paper_info.json")
            paper_info.pop("constructed_at", None)
            semantic_hash = canonical_hash(paper_info)
        semantic_files.append({"path": str(row["path"]), "semantic_hash": semantic_hash})
    manifest["format"] = "researchchembench.audit-input-manifest.v1"
    manifest["content_hash"] = canonical_hash(semantic_files)
    manifest["normalizations"] = {
        "ignored_files": ["construction_record.json"],
        "ignored_fields": ["paper_info.json#/constructed_at"],
    }
    return manifest


def _cached_audit_inputs_match(
    cached: dict[str, Any],
    *,
    stage_root: Path,
    pair_manifest_hash: str,
    toolbox: dict[str, Any],
    resource_policy: dict[str, Any],
    harness_name: str,
    model_name: str,
) -> bool:
    """Safely migrate a pre-stable-fingerprint Stage07 checkpoint."""

    if cached.get("prompt_version") != STAGE07_AUDIT_VERSION:
        return False
    agent_run = cached.get("agent_run") or {}
    if agent_run.get("harness") != harness_name or agent_run.get("model") != model_name:
        return False
    try:
        previous_workspace = Path(str(agent_run["workspace"])).expanduser().resolve()
        previous_workspace.relative_to((stage_root / "workspaces").resolve())
        previous_pair = previous_workspace / "inputs" / "task_pair"
        if _audit_pair_manifest(previous_pair)["content_hash"] != pair_manifest_hash:
            return False
        if read_json(previous_workspace / "inputs" / "toolbox_snapshot.json") != toolbox:
            return False
        if read_json(previous_workspace / "inputs" / "resource_policy.json") != resource_policy:
            return False
    except (KeyError, FileNotFoundError, OSError, ValueError, json.JSONDecodeError):
        return False
    return True


def deterministic_judge_audit(pair: Any) -> dict[str, Any]:
    """Compatibility entry point with support for the new task-pair directory."""

    if isinstance(pair, (str, Path)):
        return deterministic_stage07_audit(Path(pair))
    findings = []
    for mode in ("autonomous", "reproduction"):
        if not pair.get(mode, {}).get("task_info") or not pair.get(mode, {}).get("task_markdown"):
            findings.append(f"{mode}_incomplete")
    if (
        not pair.get("scientific_record")
        or not pair.get("hidden_reference")
        or not pair.get("evidence_map")
    ):
        findings.append("shared_record_incomplete")
    return {"passed": not findings, "findings": findings}


def run_gold(record, config, stage_root):
    """Deprecated boundary marker: Stage07 no longer executes Gold Runs."""

    return {"status": "not_run", "reason": "gold_run_moved_outside_stage07"}


def _toolbox_snapshot_from_pair(pair_root: Path, config: dict[str, Any]) -> dict[str, Any]:
    path_value = config.get("toolbox_capabilities")
    if path_value:
        path = Path(str(path_value)).expanduser().resolve()
        if path.is_file():
            return read_json(path)
    requirements = pair_root / "toolbox_requirements.json"
    return {
        "snapshot_status": "requirements_only",
        "requirements": read_json(requirements) if requirements.is_file() else [],
    }


def _stage07_audit_packet(
    *,
    pair_root: Path,
    pair_manifest: dict[str, Any],
    deterministic: dict[str, Any],
    toolbox: dict[str, Any],
    resource_policy: dict[str, Any],
) -> dict[str, Any]:
    autonomous_info = read_json(pair_root / "autonomous_research" / "task_info.json")
    autonomous_spec = read_json(pair_root / "autonomous_research" / "task_spec.json")
    reproduction_info = read_json(pair_root / "paper_reproduction" / "task_info.json")
    reproduction_spec = read_json(pair_root / "paper_reproduction" / "task_spec.json")
    workflow = read_json(pair_root / "paper_reproduction" / "workflow_spec.json")
    submission = read_json(pair_root / "autonomous_research" / "submission_contract.json")
    hidden = read_json(pair_root / "hidden_reference" / "ground_truth_common.json")
    paper_info = read_json(pair_root / "paper_info.json")
    workflow_review_path = pair_root / "workflow_review.json"
    workflow_review = read_json(workflow_review_path) if workflow_review_path.is_file() else {}
    requirements_path = pair_root / "toolbox_requirements.json"
    requirements = read_json(requirements_path) if requirements_path.is_file() else []
    mode_fields = (
        "task_id",
        "task_pair_id",
        "task_mode",
        "scientific_mode",
        "method_disclosure",
        "pathway_disclosure",
        "category",
        "benchmark_family",
    )
    shared_spec_fields = (
        "scientific_question",
        "target_definition",
        "boundary_conditions",
        "input_assets",
        "workflow_scope",
        "complexity_profile",
        "resources",
        "resource_policy",
        "required_outputs",
    )
    profiles = hidden.get("acceptance_profiles") or []
    rubric = hidden.get("scientific_conclusion_rubric") or []
    workflow_steps = next(
        (
            workflow.get(key)
            for key in ("workflow_steps", "steps", "route_steps")
            if workflow.get(key)
        ),
        [],
    )
    workflow_summary = {
        key: workflow.get(key)
        for key in ("software", "method", "method_parameters", "validation_procedure")
        if workflow.get(key) not in (None, [], {}, "")
    }
    workflow_summary["steps"] = workflow_steps
    return {
        "pair_manifest_hash": pair_manifest["content_hash"],
        "deterministic_audit": deterministic,
        "mode_summaries": {
            "shared_task_spec": {
                key: autonomous_spec.get(key)
                for key in shared_spec_fields
                if key in autonomous_spec
            },
            "autonomous_research": {
                "task_info": {
                    key: autonomous_info.get(key) for key in mode_fields if key in autonomous_info
                },
                "task_spec": {"mode": autonomous_spec.get("mode")},
            },
            "paper_reproduction": {
                "task_info": {
                    key: reproduction_info.get(key)
                    for key in mode_fields
                    if key in reproduction_info
                },
                "task_spec": {"mode": reproduction_spec.get("mode")},
            },
        },
        "workflow_summary": workflow_summary,
        "workflow_selection": {
            "workflow_scope": workflow_review.get("workflow_scope")
            or paper_info.get("workflow_scope")
            or autonomous_spec.get("workflow_scope")
            or {},
            "complexity_profile": workflow_review.get("complexity_profile")
            or paper_info.get("complexity_profile")
            or autonomous_spec.get("complexity_profile")
            or {},
            "paper_workflow_inventory_complete": workflow_review.get(
                "paper_workflow_inventory_complete"
            ),
            "full_paper_workflow_checked": workflow_review.get(
                "full_paper_workflow_checked"
            ),
            "alternative_scope_search_complete": workflow_review.get(
                "alternative_scope_search_complete"
            ),
            "workflow_inventory": workflow_review.get("workflow_inventory") or [],
            "stage05_candidate_disposition": workflow_review.get(
                "stage05_candidate_disposition"
            ),
        },
        "submission_contract": {
            "required_files": submission.get("required_files") or [],
            "artifact_paths": submission.get("artifact_paths") or {},
            "result_schema_names": sorted(
                key for key in submission if "schema" in str(key).casefold()
            ),
        },
        "hidden_scoring_summary": {
            "ground_truth_items": [
                {
                    key: item.get(key)
                    for key in (
                        "ground_truth_id",
                        "kind",
                        "acceptance_type",
                        "acceptance_profile_id",
                        "evidence_grade",
                        "evidence_ids",
                        "claim_role",
                        "applies_to_modes",
                    )
                }
                for item in hidden.get("ground_truth_items") or []
            ],
            "acceptance_profiles": [
                {
                    "acceptance_profile_id": profile.get("acceptance_profile_id"),
                    "type": profile.get("type"),
                    "submission_binding": {
                        key: (profile.get("submission_binding") or {}).get(key)
                        for key in ("artifact_paths", "observed_fields")
                        if key in (profile.get("submission_binding") or {})
                    },
                    "comparison_rule_present": bool(
                        (profile.get("submission_binding") or {}).get("comparison")
                    ),
                }
                for profile in profiles
            ],
            "scientific_conclusion_rubric": [
                {
                    key: criterion.get(key)
                    for key in (
                        "id",
                        "max_score",
                        "ground_truth_ids",
                        "acceptance_profile_ids",
                        "required_evidence",
                    )
                }
                for criterion in rubric
            ],
        },
        "provenance_summary": {
            **{
                key: paper_info.get(key)
                for key in ("paper_id", "task_pair_id", "doi", "title", "journal")
                if key in paper_info
            },
            "documents": [
                {
                    key: document.get(key)
                    for key in (
                        "document_id",
                        "document_role",
                        "file_name",
                        "sha256",
                        "size_bytes",
                        "source_remote_uri",
                        "selected_parser",
                    )
                    if key in document
                }
                for document in paper_info.get("documents") or []
                if isinstance(document, dict)
            ],
        },
        "source_evidence_bundle": _stage07_source_evidence_bundle(
            pair_root, workflow_review=workflow_review, hidden=hidden
        ),
        "toolbox_requirements": requirements,
        "toolbox_focus": _focused_toolbox_view(toolbox, requirements),
        "resource_policy": resource_policy,
        "unresolved_questions": [
            "Was a larger complete computational scope available but not selected?",
            "Does the task provide genuine medium/high scientific complexity rather than split non-core steps?",
            "Are requirements marked unknown actually unsupported, or only unverified?",
            "Is the requested workflow obviously infeasible under the stated resource policy?",
        ],
        "targeted_fallback_paths": [
            "inputs/task_pair/paper_reproduction/workflow_spec.json",
            "inputs/task_pair/workflow_review.json",
            "inputs/task_pair/toolbox_requirements.json",
            "inputs/task_pair/hidden_reference/acceptance_profiles.json",
            "inputs/task_pair/paper_info.json",
        ],
    }


def _focused_toolbox_view(
    toolbox: dict[str, Any], requirements: list[dict[str, Any]]
) -> dict[str, Any]:
    names = {
        str(
            row.get("software")
            or row.get("tool")
            or row.get("normalized_backend")
            or ""
        ).casefold()
        for row in requirements
        if isinstance(row, dict)
    }
    names.discard("")
    focused: dict[str, Any] = {
        key: toolbox.get(key)
        for key in (
            "schema_version",
            "profile_id",
            "catalog_hash",
            "runtime_profile_hash",
            "snapshot_status",
            "unknown_field_policy",
            "execution_layers",
        )
        if key in toolbox
    }
    for section in ("backends", "native_software", "python_packages"):
        rows = toolbox.get(section)
        if not isinstance(rows, dict):
            continue
        selected = {
            name: value
            for name, value in rows.items()
            if str(name).casefold() in names
            or any(alias in str(name).casefold() for alias in names)
        }
        if selected:
            focused[section] = selected
    if toolbox.get("requirements") is not None:
        focused["requirements"] = toolbox.get("requirements")
    return focused


def _stage07_source_evidence_bundle(
    pair_root: Path,
    *,
    workflow_review: dict[str, Any],
    hidden: dict[str, Any],
    limit: int = 80,
) -> dict[str, Any]:
    evidence_path = pair_root / "evidence_index.json"
    if not evidence_path.is_file():
        return {"status": "missing", "records": []}
    records = read_json(evidence_path)
    by_id = {
        str(row.get("evidence_id")): row
        for row in records
        if isinstance(row, dict) and row.get("evidence_id")
    }
    requested: list[str] = []

    def collect(value: Any) -> None:
        if isinstance(value, dict):
            singular = value.get("evidence_id")
            if singular not in (None, ""):
                requested.append(str(singular))
            plural = value.get("evidence_ids")
            if isinstance(plural, list):
                requested.extend(str(item) for item in plural if item not in (None, ""))
            for key, nested in value.items():
                if key not in {"evidence_id", "evidence_ids"}:
                    collect(nested)
        elif isinstance(value, list):
            for nested in value:
                collect(nested)

    collect(
        {
            "workflow_scope": workflow_review.get("workflow_scope") or {},
            "workflow_inventory": workflow_review.get("workflow_inventory") or [],
            "workflow_steps": workflow_review.get("workflow_steps") or [],
            "paper_route": workflow_review.get("paper_route") or {},
            "ground_truth_items": hidden.get("ground_truth_items") or [],
        }
    )
    unique = list(dict.fromkeys(requested))
    selected = []
    for evidence_id in unique[:limit]:
        row = by_id.get(evidence_id)
        if row is None:
            selected.append({"evidence_id": evidence_id, "status": "unresolved"})
            continue
        selected.append(
            {
                "evidence_id": evidence_id,
                "document_id": row.get("document_id"),
                "document_role": row.get("document_role"),
                "page": row.get("page"),
                "section_path": row.get("section_path") or [],
                "block_type": row.get("block_type"),
                "text": str(row.get("text") or "")[:4000],
                "source_ref": row.get("source_ref"),
            }
        )
    return {
        "status": "complete" if len(unique) <= limit else "truncated",
        "requested_count": len(unique),
        "included_count": len(selected),
        "records": selected,
    }


def _stage07_audit_scaffold(
    deterministic: dict[str, Any], packet: dict[str, Any]
) -> dict[str, Any]:
    outcomes = json.loads(json.dumps(deterministic.get("outcomes") or []))
    pair_audit = deterministic.get("pair_audit") or {}
    return {
        "audit_summary": "issues_found" if outcomes else "passed_audit",
        "outcomes": outcomes,
        "checks": [
            {
                "check": "deterministic_task_pair_validation",
                "status": "passed" if pair_audit.get("passed") else "failed",
                "evidence_refs": ["inputs/audit_packet.json#/deterministic_audit"],
            },
            {
                "check": "mode_input_hash_equality",
                "status": (
                    "passed"
                    if pair_audit.get("autonomous_input_hash")
                    == pair_audit.get("reproduction_input_hash")
                    else "failed"
                ),
                "evidence_refs": ["inputs/audit_packet.json#/deterministic_audit/pair_audit"],
            },
        ],
        "toolbox_assessment": {
            "status": "AGENT_REQUIRED: assess required capabilities",
            "requirements": packet.get("toolbox_requirements") or [],
        },
        "cost_assessment": {
            "status": "AGENT_REQUIRED: assess obvious feasibility",
            "resource_policy": packet.get("resource_policy") or {},
        },
        "rationale": "AGENT_REQUIRED: concise objective audit rationale",
    }


def _stage07_audit_initializer_script() -> str:
    return r'''from __future__ import annotations

import json
import os
from pathlib import Path

root = Path(__file__).resolve().parent.parent
source = root / "inputs" / "objective_audit_scaffold.json"
destination = root / "outputs" / "objective_audit.json"
destination.parent.mkdir(parents=True, exist_ok=True)
value = json.loads(source.read_text(encoding="utf-8"))
temporary = destination.with_suffix(".json.tmp")
temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
json.loads(temporary.read_text(encoding="utf-8"))
os.replace(temporary, destination)
print(json.dumps({
    "artifact": "outputs/objective_audit.json",
    "deterministic_outcome_count": len(value["outcomes"]),
    "fields_to_replace": ["toolbox_assessment.status", "cost_assessment.status", "rationale"],
}))
'''


def _public_audit_report(task_pair_id: str, summary: str, outcomes: list[dict[str, Any]]) -> str:
    lines = [f"# Stage07 audit: {task_pair_id}", "", f"Result: `{summary}`", ""]
    if not outcomes:
        lines.append("No objective task-integrity, toolbox, or cost issue was identified.")
    else:
        lines.append("Observed outcomes:")
        lines.append("")
        for outcome in outcomes:
            lines.append(
                f"- `{outcome.get('type')}` ({outcome.get('severity')}, "
                f"{outcome.get('scope')})"
            )
    lines.append("")
    return "\n".join(lines)


def _outcome_counts(records: list[dict[str, Any]]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for record in records:
        for outcome in record.get("outcomes") or []:
            name = str(outcome.get("type") or "missing")
            counts[name] = counts.get(name, 0) + 1
    return dict(sorted(counts.items()))


def _audit_failure(
    run_id: str,
    paper_id: str,
    task_pair_id: str,
    failure_class: str,
    message: str,
    *,
    agent_run: dict[str, Any] | None = None,
    retryable: bool = True,
) -> dict[str, Any]:
    return {
        **record_header(run_id=run_id, stage="stage07", paper_id=paper_id),
        "task_pair_id": task_pair_id,
        "processing_status": "failed",
        "decision": "audit_failed_retryable",
        "audit_summary": "audit_failed_retryable",
        "passed": False,
        "retryable": retryable,
        "failure_class": failure_class,
        "outcomes": [],
        "error": {"error_type": failure_class, "message": message[:4000]},
        "agent_run": agent_run,
    }
