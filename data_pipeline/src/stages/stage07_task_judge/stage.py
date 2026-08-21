from __future__ import annotations

import json
import shutil
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
    atomic_commit_tree,
    copy_recovery_artifacts,
    copytree_exact,
    directory_manifest,
    input_fingerprint,
    make_read_only,
    make_writable,
    prepare_clean_directory,
    recovery_instructions,
    validate_relative_path,
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
from src.core.toolbox_inventory import installed_software_inventory
from src.stages.stage07_task_judge.prompts import (
    STAGE07_AUDIT_VERSION,
    audit_instructions,
)
from src.stages.stage07_task_judge.validation import (
    _project_hidden_for_mode,
    published_bundle_mechanical_check,
    stage07_mechanical_pre_publish_check,
    validate_agent_audit,
)
from src.stages.stage06_task_builder.validation import canonical_task_pair_id

STAGE07_IMPLEMENTATION_VERSION = "v12-contract-observation-and-publication-state-20260821"
STAGE07_DIRECTORY = "stage_07_task_audit"
STAGE07_IGNORED_PAIR_FILES = {*IGNORED_MANIFEST_NAMES, "construction_record.json"}
STAGE07_APPROVED_DECISIONS = {
    "approved",
    "approved_with_repairs",
    "approved_after_workflow_redesign",
}
STAGE07_ELIGIBLE_STAGE06_DECISIONS = {
    "provisional_constructed",
    "provisional_not_constructible",
    "constructed",
}


def _write_stage07_audit_index(root: Path) -> None:
    """Write non-scientific navigation metadata for the audit Agent.

    The index deliberately contains paths, sizes, JSON top-level keys, and small counts only.
    It is a transport aid: it does not summarize chemistry, expose hidden values, or decide
    whether a workflow is scientifically complete.  The Agent still reads the source files when
    making the scientific audit decision.
    """

    inputs = root / "inputs"
    entries: list[dict[str, Any]] = []
    for path in sorted(inputs.rglob("*")):
        if not path.is_file() or path.name == "audit_index.json":
            continue
        rel = path.relative_to(inputs).as_posix()
        item: dict[str, Any] = {"path": rel, "size_bytes": path.stat().st_size}
        if path.suffix.lower() == ".json":
            try:
                value = read_json(path)
            except (OSError, TypeError, ValueError, json.JSONDecodeError):
                item["json_status"] = "unreadable"
            else:
                item["json_status"] = "object" if isinstance(value, dict) else type(value).__name__
                if isinstance(value, dict):
                    item["top_level_keys"] = sorted(str(key) for key in value.keys())
                    for key in ("input_assets", "workflow_steps", "ground_truth_items", "acceptance_profiles"):
                        if isinstance(value.get(key), list):
                            item[f"{key}_count"] = len(value[key])
        entries.append(item)
    write_json(
        inputs / "audit_index.json",
        {
            "schema_version": "stage07-audit-index/v1",
            "purpose": "transport_navigation_only",
            "scientific_decision": "agent_only",
            "files": entries,
        },
    )


def run_stage07(*, build_records, documents, config, model, workspace: Path, run_id: str):
    stage_root = workspace / STAGE07_DIRECTORY
    stage_root.mkdir(parents=True, exist_ok=True)
    eligible = [
        row
        for row in build_records
        if row.get("decision") in STAGE07_ELIGIBLE_STAGE06_DECISIONS
        and row.get("handoff_ready", True)
    ]
    documents_by_paper: dict[str, list[dict[str, Any]]] = {}
    for document in documents:
        if document.get("decision") == "pass" and document.get("paper_id"):
            documents_by_paper.setdefault(str(document["paper_id"]), []).append(document)
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
        task_pair_id = canonical_task_pair_id(paper_id)
        handoff_value = record.get("handoff_path") or record.get("task_pair_path")
        try:
            if not handoff_value:
                return _audit_failure(
                    run_id,
                    paper_id,
                    task_pair_id,
                    "stage06_handoff_missing",
                    "Stage06 did not provide a handoff path.",
                )
            handoff_root = Path(str(handoff_value)).expanduser().resolve()
            if not handoff_root.is_dir():
                return _audit_failure(
                    run_id,
                    paper_id,
                    task_pair_id,
                    "stage06_handoff_missing",
                    f"Stage06 handoff directory is missing: {handoff_root}",
                )
            source_root = _resolve_stage07_source_root(
                record=record,
                paper_id=paper_id,
                documents=documents_by_paper.get(paper_id, []),
                stage_root=stage_root,
                config=config,
            )
            source_stage06_decision = (
                "provisional_constructed"
                if record.get("decision") == "constructed"
                else str(record["decision"])
            )
            response, agent_run, artifact_root = _run_audit_repair_agent(
                harness=harness,
                stage_root=stage_root,
                paper_id=paper_id,
                task_pair_id=task_pair_id,
                source_stage06_decision=source_stage06_decision,
                handoff_root=handoff_root,
                source_root=source_root,
                stage06_record=record,
                config=config,
            )
            decision = str(response["audit_decision"])
            if decision == "objective_failure_retryable":
                return _audit_failure(
                    run_id,
                    paper_id,
                    task_pair_id,
                    "agent_reported_objective_failure",
                    str(response.get("summary") or "Stage07 could not complete the audit."),
                    agent_run=agent_run,
                )
            agent_proposed_task_pair_id = str(response.get("final_task_pair_id") or "")
            final_task_pair_id = canonical_task_pair_id(paper_id)
            response["agent_proposed_task_pair_id"] = agent_proposed_task_pair_id
            response["final_task_pair_id"] = final_task_pair_id
            final_path: str | None = None
            published_paths: dict[str, str] = {}
            evaluator_paths: dict[str, str] = {}
            published_bundle_statuses: dict[str, dict[str, Any]] = {}
            if decision in STAGE07_APPROVED_DECISIONS:
                task_root = _stage07_approved_artifact(response, artifact_root)
                target = stage_root / "audited_tasks" / safe_component(paper_id)
                atomic_commit_tree(task_root, target)
                _synchronize_hidden_pair_identity(
                    target, task_pair_id=canonical_task_pair_id(paper_id)
                )
                write_json(target / "stage07_audit.json", response)
                write_json(target / "stage06_handoff_record.json", record)
                mechanical_report = stage07_mechanical_pre_publish_check(
                    target, task_pair_id=canonical_task_pair_id(paper_id)
                )
                write_json(target / "mechanical_pre_publish_report.json", mechanical_report)
                write_manifest(target, target / "audit_manifest.json")
                response["orchestrator_mechanical_status"] = (
                    "passed"
                    if mechanical_report.get("mechanical_pre_publish_status") == "passed"
                    else "blocked"
                )
                response["orchestrator_mechanical_findings"] = mechanical_report.get(
                    "findings", []
                )
                response["orchestrator_schema_load_diagnostic"] = mechanical_report.get(
                    "schema_load_diagnostic", "not_run"
                )
                response["orchestrator_normalization_records"] = mechanical_report.get(
                    "normalization_records", []
                )
                write_json(target / "stage07_audit.json", response)
                if mechanical_report.get("mechanical_pre_publish_status") == "passed":
                    published_paths = _publish_mode_bundles(
                        target,
                        stage_root / "published_tasks",
                        task_pair_id=final_task_pair_id or task_pair_id,
                    )
                    evaluator_paths = _publish_private_evaluator_registry(
                        target,
                        stage_root / "evaluator_registry",
                        task_pair_id=final_task_pair_id or task_pair_id,
                    )
                    published_bundle_statuses = {
                        mode: published_bundle_mechanical_check(Path(path))
                        for mode, path in published_paths.items()
                    }
                    if published_paths and all(
                        status.get("status") == "passed"
                        for status in published_bundle_statuses.values()
                    ):
                        response["publication_state"] = "published"
                        response["blocking_phase"] = ""
                    else:
                        response["publication_state"] = "publish_ready"
                        response["blocking_phase"] = "published_bundle"
                else:
                    # A transport failure blocks publication, but does not
                    # reopen the scientific audit or silently turn it into a
                    # scientific rejection.  The finding is recorded for a
                    # bounded technical recovery path.
                    response["orchestrator_mechanical_status"] = "blocked"
                    response["orchestrator_mechanical_findings"] = mechanical_report.get(
                        "findings", []
                    )
                    response["publication_state"] = "mechanical_blocked"
                    response["blocking_phase"] = "prepublish_mechanical"
                write_json(target / "stage07_audit.json", response)
                final_path = str(target)
            else:
                target = _publish_stage07_rejection(
                    stage_root=stage_root,
                    paper_id=paper_id,
                    response=response,
                    stage06_record=record,
                    handoff_root=handoff_root,
                )
            return {
                **record_header(run_id=run_id, stage="stage07", paper_id=paper_id),
                "task_pair_id": final_task_pair_id or task_pair_id,
                "original_task_pair_id": task_pair_id,
                "processing_status": "completed",
                "decision": decision,
                "audit_decision": decision,
                "audit_summary": decision,
                "passed": decision in STAGE07_APPROVED_DECISIONS,
                "scientific_audit_passed": decision in STAGE07_APPROVED_DECISIONS,
                "mechanical_contract_passed": response.get(
                    "orchestrator_mechanical_status", "not_run"
                ) == "passed",
                "publication_state": response.get(
                    "publication_state",
                    "not_applicable"
                    if decision not in STAGE07_APPROVED_DECISIONS
                    else "mechanical_blocked",
                ),
                "blocking_phase": response.get("blocking_phase", ""),
                "publish_ready": bool(published_paths),
                "mechanical_approved_but_unpublished": bool(
                    decision in STAGE07_APPROVED_DECISIONS
                    and response.get("orchestrator_mechanical_status") == "blocked"
                ),
                "selected_workflow_preserved": response.get(
                    "selected_workflow_preserved"
                ),
                "repair_count": len(response.get("repairs") or []),
                "workflow_redesign": response.get("workflow_redesign") or {},
                "toolbox_status": response.get("toolbox_status"),
                "required_additions": response.get("required_additions") or [],
                "resource_status": response.get("resource_status"),
                "agent_observed_contract_status": response.get("contract_status"),
                "agent_observed_disclosure_status": response.get("disclosure_status"),
                "agent_observed_schema_load_diagnostic": response.get(
                    "schema_load_diagnostic", response.get("evaluator_dry_run_status")
                ),
                "orchestrator_mechanical_status": response.get(
                    "orchestrator_mechanical_status", "not_run"
                ),
                "orchestrator_mechanical_findings": response.get(
                    "orchestrator_mechanical_findings", []
                ),
                "orchestrator_schema_load_diagnostic": response.get(
                    "orchestrator_schema_load_diagnostic", "not_run"
                ),
                "orchestrator_normalization_records": response.get(
                    "orchestrator_normalization_records", []
                ),
                "published_bundle_statuses": published_bundle_statuses,
                "task_pair_path": final_path,
                "published_task_paths": published_paths,
                "evaluator_registry_paths": evaluator_paths,
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
        "approved": sum(row.get("audit_decision") == "approved" for row in records),
        "approved_with_repairs": sum(
            row.get("audit_decision") == "approved_with_repairs" for row in records
        ),
        "approved_after_workflow_redesign": sum(
            row.get("audit_decision") == "approved_after_workflow_redesign"
            for row in records
        ),
        "rejected_scientific_unrepairable": sum(
            row.get("audit_decision") == "rejected_scientific_unrepairable"
            for row in records
        ),
        "objective_failure_retryable": sum(
            row.get("audit_decision") == "objective_failure_retryable" for row in records
        ),
        "mechanical_publish_blocked": sum(
            row.get("orchestrator_mechanical_status") == "blocked" for row in records
        ),
        "mechanical_approved_but_unpublished": sum(
            bool(row.get("mechanical_approved_but_unpublished")) for row in records
        ),
        "blocking_reasons": sorted(
            {
                str(reason)
                for row in records
                if row.get("orchestrator_mechanical_status") == "blocked"
                for reason in row.get("orchestrator_mechanical_findings") or []
            }
        ),
        "schema_load_failed": sum(
            row.get("orchestrator_schema_load_diagnostic") == "failed" for row in records
        ),
        "scientific_audit_passed": sum(
            bool(row.get("scientific_audit_passed")) for row in records
        ),
        "mechanical_contract_passed": sum(
            bool(row.get("mechanical_contract_passed")) for row in records
        ),
        "publish_ready": sum(bool(row.get("publish_ready")) for row in records),
        "publication_states": {
            state: sum(row.get("publication_state") == state for row in records)
            for state in ("not_applicable", "publish_ready", "mechanical_blocked", "published")
        },
        "blocking_phases": {
            phase: sum(row.get("blocking_phase") == phase for row in records)
            for phase in ("prepublish_mechanical", "published_bundle")
        },
        "paper_ids": sorted({str(row.get("paper_id")) for row in records if row.get("paper_id")}),
        "needs_software": sum(row.get("toolbox_status") == "needs_software" for row in records),
        "decisions": decision_counts(records, "audit_decision"),
        "agent_harness": harness.name,
        "agent_model": harness.model,
    }
    write_json(stage_root / "stage_summary.json", summary)
    return {"records": records, "summary": summary}


def _run_audit_repair_agent(
    *,
    harness,
    stage_root: Path,
    paper_id: str,
    task_pair_id: str,
    source_stage06_decision: str,
    handoff_root: Path,
    source_root: Path,
    stage06_record: dict[str, Any],
    config: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], Path]:
    handoff_manifest = directory_manifest(handoff_root)
    source_manifest = directory_manifest(source_root)
    toolbox = _stage07_toolbox_snapshot(source_root, handoff_root, config)
    resource_policy = _stage07_resource_policy(source_root, config)
    fingerprint = input_fingerprint(
        {
            "handoff_manifest_hash": handoff_manifest["content_hash"],
            "source_manifest_hash": source_manifest["content_hash"],
            "source_stage06_decision": source_stage06_decision,
            "toolbox": toolbox,
            "resource_policy": resource_policy,
            "prompt_version": STAGE07_AUDIT_VERSION,
            "receipt_schema": canonical_hash(STAGE07_AUDIT_SCHEMA),
            "harness": harness.name,
            "model": harness.model,
        }
    )
    artifact_root = (
        stage_root
        / "phase_artifacts"
        / safe_component(paper_id)
        / "audit_repair"
        / fingerprint[:16]
    )
    checkpoint = (
        stage_root / "checkpoints" / safe_component(paper_id) / "audit_repair.json"
    )
    failure_checkpoint = checkpoint.with_suffix(".failure.json")
    if bool(config.get("resume", True)) and checkpoint.is_file() and artifact_root.is_dir():
        cached = read_json(checkpoint)
        if cached.get("input_fingerprint") == fingerprint:
            response = cached.get("response") or {}
            jsonschema.validate(response, STAGE07_AUDIT_SCHEMA)
            if response.get("audit_decision") in STAGE07_APPROVED_DECISIONS:
                _stage07_approved_artifact(response, artifact_root)
                return (
                    response,
                    {**(cached.get("agent_run") or {}), "cache_hit": True},
                    artifact_root,
                )
            else:
                return (
                    response,
                    {**(cached.get("agent_run") or {}), "cache_hit": True},
                    artifact_root,
                )

    attempts = max(1, int(config.get("max_attempts", 3)))
    last_error: AgentExecutionError | None = None
    recovery_context: str | None = None
    recovery_workspace: Path | None = None
    for attempt in range(1, attempts + 1):
        root = prepare_clean_directory(
            stage_root
            / "workspaces"
            / safe_component(paper_id)
            / "audit_repair"
            / f"attempt-{attempt:02d}-{uuid.uuid4().hex[:8]}"
        )
        inputs = root / "inputs"
        inputs.mkdir(parents=True, exist_ok=True)
        copytree_exact(handoff_root, inputs / "stage06_candidate")
        _copy_stage07_source_packet(source_root, inputs / "source_materials")
        write_json(inputs / "stage06_record.json", stage06_record)
        write_json(inputs / "toolbox_snapshot.json", toolbox)
        write_json(inputs / "resource_policy.json", resource_policy)
        write_json(
            inputs / "input_manifest.json",
            {
                "paper_id": paper_id,
                "task_pair_id": task_pair_id,
                "source_stage06_decision": source_stage06_decision,
                "handoff_manifest_hash": handoff_manifest["content_hash"],
                "source_manifest_hash": source_manifest["content_hash"],
                "input_fingerprint": fingerprint,
            },
        )
        _write_stage07_audit_index(root)
        make_read_only(inputs)
        outputs = root / "outputs"
        outputs.mkdir(parents=True, exist_ok=True)
        copytree_exact(handoff_root, outputs / "task_pair")
        make_writable(outputs)
        if recovery_context:
            (root / "RECOVERY_CONTEXT.md").write_text(
                recovery_context, encoding="utf-8"
            )
            copy_recovery_artifacts(
                recovery_workspace,
                root,
                directory_names=("outputs",),
                include_evidence_trace=True,
            )
            # A failed Agent may have redundantly copied the immutable handoff
            # inside the task tree. It is never a valid deliverable and would
            # otherwise be carried into every recovery attempt.
            redundant_candidate = outputs / "task_pair" / "stage06_candidate"
            if redundant_candidate.is_dir():
                shutil.rmtree(redundant_candidate)
            elif redundant_candidate.exists():
                redundant_candidate.unlink()
            make_writable(outputs)
        max_tool_calls = max(
            4,
            int(
                config.get(
                    "audit_repair_max_tool_calls",
                    config.get("audit_max_tool_calls", config.get("max_tool_calls", 120)),
                )
            ),
        )
        if recovery_context:
            max_tool_calls = max(
                4,
                int(
                    config.get(
                        "audit_repair_recovery_max_tool_calls",
                        config.get("recovery_max_tool_calls", 160),
                    )
                ),
            )
        finalization_reserve = min(
            max_tool_calls - 1,
            max(
                2,
                int(
                    config.get(
                        "audit_repair_finalization_reserve",
                        config.get("finalization_reserve", 12),
                    )
                ),
            ),
        )
        instructions = audit_instructions(
            paper_id=paper_id,
            task_pair_id=task_pair_id,
            manifest_hash=fingerprint,
            max_tool_calls=max_tool_calls,
            finalization_reserve=finalization_reserve,
            source_stage06_decision=source_stage06_decision,
        )
        if recovery_context:
            instructions += recovery_instructions(
                "stage07_audit_repair", max_tool_calls=max_tool_calls
            )
        request = AgentRunRequest(
            phase="stage07_audit_repair",
            record_id=task_pair_id,
            workspace=root,
            instructions=instructions,
            output_schema=STAGE07_AUDIT_SCHEMA,
            prompt_version=STAGE07_AUDIT_VERSION,
            timeout_seconds=int(config.get("timeout_seconds", 7200)),
            metadata={
                "paper_id": paper_id,
                "task_pair_id": task_pair_id,
                "source_stage06_decision": source_stage06_decision,
                "max_tool_calls": max_tool_calls,
                "finalization_reserve": finalization_reserve,
                "tool_choice_policy": config.get("audit_repair_tool_choice_policy", config.get("tool_choice_policy")),
                "response_format_policy": config.get("audit_repair_response_format_policy", config.get("response_format_policy")),
                "codex_wire_api": config.get("audit_repair_codex_wire_api"),
                # The Agent may finish by writing this small internal receipt.  The harness can
                # recover it if the CLI final message is truncated or non-JSON.
                "inline_contract": True,
                "structured_artifact_path": "outputs/stage07_audit.json",
                "recovery_attempt": bool(recovery_context),
            },
        )
        try:
            result = harness.run(request)
            response = result.response or {}
            contract_findings = _approved_receipt_contract_findings(response)
            if contract_findings:
                message = "Stage07 receipt is internally inconsistent: " + "; ".join(
                    contract_findings
                )
                result.status = "failed"
                result.failure_class = "invalid_phase_contract"
                result.retryable = True
                result.error = {
                    "error_type": "InvalidPhaseContract",
                    "message": message,
                }
                write_json(root / "agent_run.json", result.audit_record())
                raise AgentExecutionError(
                    message,
                    failure_class="invalid_phase_contract",
                    retryable=True,
                    result=result,
                )
            response = _finalize_stage07_response(
                response=response,
                task_root=outputs / "task_pair",
                toolbox=toolbox,
            )
            write_json(outputs / "stage07_audit.json", response)
            _require_stage07_artifact_delivery(response, root, result)
            if response.get("audit_decision") in STAGE07_APPROVED_DECISIONS:
                mechanical_report = stage07_mechanical_pre_publish_check(
                    outputs / "task_pair", task_pair_id=canonical_task_pair_id(paper_id)
                )
                write_json(root / "mechanical_pre_publish_report.json", mechanical_report)
                if mechanical_report.get("mechanical_pre_publish_status") != "passed":
                    # Mechanical findings are surfaced to the orchestrator and
                    # handled as a bounded publication block.  They must not
                    # trigger another full-paper Stage07 scientific review.
                    response["orchestrator_mechanical_status"] = "blocked"
                    response["orchestrator_mechanical_findings"] = mechanical_report.get(
                        "findings", []
                    )
                else:
                    response["orchestrator_mechanical_status"] = "passed"
                response["orchestrator_schema_load_diagnostic"] = mechanical_report.get(
                    "schema_load_diagnostic", "not_run"
                )
                write_json(outputs / "stage07_audit.json", response)
        except AgentExecutionError as exc:
            last_error = exc
            recovery_context = agent_recovery_context(exc.result)
            recovery_workspace = (
                Path(exc.result.workspace)
                if exc.result is not None and exc.result.workspace
                else None
            )
            if not exc.retryable or attempt >= attempts:
                write_json(
                    failure_checkpoint,
                    {
                        "paper_id": paper_id,
                        "task_pair_id": task_pair_id,
                        "input_fingerprint": fingerprint,
                        "failure_class": exc.failure_class,
                        "retryable": exc.retryable,
                        "agent_run": exc.result.audit_record() if exc.result else None,
                        "failed_at": now_utc(),
                    },
                )
                raise
            delay = min(
                float(config.get("retry_max_seconds", 30)),
                float(config.get("retry_backoff_seconds", 2)) * (2 ** (attempt - 1)),
            )
            if delay > 0:
                time.sleep(delay)
            continue
        staging = prepare_clean_directory(
            artifact_root.parent / f".{artifact_root.name}-{uuid.uuid4().hex[:8]}"
        )
        copytree_exact(outputs, staging / "outputs")
        atomic_commit_tree(staging, artifact_root)
        write_json(
            checkpoint,
            {
                "paper_id": paper_id,
                "task_pair_id": task_pair_id,
                "input_fingerprint": fingerprint,
                "prompt_version": STAGE07_AUDIT_VERSION,
                "response": response,
                "agent_run": result.audit_record(),
                "artifact_manifest_hash": directory_manifest(artifact_root)[
                    "content_hash"
                ],
                "completed_at": now_utc(),
            },
        )
        failure_checkpoint.unlink(missing_ok=True)
        return response, {**result.audit_record(), "cache_hit": False}, artifact_root
    if last_error is not None:
        raise last_error
    raise RuntimeError("Stage07 audit-repair Agent did not execute")


def _finalize_stage07_response(
    *, response: dict[str, Any], task_root: Path, toolbox: dict[str, Any]
) -> dict[str, Any]:
    """Refresh pair-level file-management metadata without inspecting task content."""

    decision = str(response.get("audit_decision") or "")
    if decision not in STAGE07_APPROVED_DECISIONS:
        return response

    write_manifest(task_root, task_root / "task_pair_manifest.json")
    return response


def _publish_private_evaluator_registry(
    pair_root: Path, registry_root: Path, *, task_pair_id: str
) -> dict[str, str]:
    """Install public metadata plus private truth for evaluator loading tests."""

    exported: dict[str, str] = {}
    hidden_root = pair_root / "hidden_reference"
    common_path = hidden_root / "ground_truth_common.json"
    if not common_path.is_file():
        return exported
    common = read_json(common_path)
    for mode in ("paper_reproduction", "autonomous_research"):
        source_mode = pair_root / mode
        if not source_mode.is_dir():
            continue
        destination = prepare_clean_directory(
            registry_root / f"{safe_component(task_pair_id)}_{mode}"
        )
        copy2_source = source_mode / "task_info.json"
        if not copy2_source.is_file():
            # The registry is a convenience export, not a publication verdict.  Stage07 Agent
            # remains authoritative and the audited pair is preserved even if this optional
            # evaluator projection cannot be built.
            shutil.rmtree(destination)
            continue
        shutil.copy2(copy2_source, destination / "task_info.json")
        target_study = destination / "target_study"
        target_study.mkdir(parents=True, exist_ok=True)
        projected = {
            **_project_hidden_for_mode(common, mode),
            "evaluation_profile": (
                "paper_reproduction"
                if mode == "paper_reproduction"
                else "autonomous_discovery"
            ),
            "scoring_rubric": read_json(source_mode / "process_rubric.json"),
        }
        write_json(target_study / "ground_truth.json", projected)
        write_manifest(destination, destination / "published_manifest.json")
        exported[mode] = str(destination)
    return exported


def _synchronize_hidden_pair_identity(pair_root: Path, *, task_pair_id: str) -> None:
    """Synchronize the transport identity of the single hidden Ground Truth source.

    The scientific contents are untouched.  Agent-proposed IDs are not authoritative;
    the canonical pair ID is assigned by the orchestrator and must also be reflected in
    the private evaluator projection.
    """

    path = pair_root / "hidden_reference" / "ground_truth_common.json"
    if not path.is_file():
        return
    value = read_json(path)
    if not isinstance(value, dict):
        return
    if value.get("task_pair_id") == task_pair_id:
        return
    value["task_pair_id"] = task_pair_id
    write_json(path, value)


def _approved_receipt_contract_findings(response: dict[str, Any]) -> list[str]:
    """Check only fields needed to locate an approved file artifact."""

    decision = str(response.get("audit_decision") or "")
    if decision not in STAGE07_APPROVED_DECISIONS:
        return []
    findings: list[str] = []
    if response.get("artifact_path") != "outputs/task_pair":
        findings.append("approved_artifact_path_invalid")
    return sorted(set(findings))


def _require_stage07_artifact_delivery(
    response: dict[str, Any], workspace: Path, result: Any
) -> None:
    """Check only that an approved Agent points to a safe, non-empty artifact tree.

    This is transport/file-safety validation.  It intentionally does not compare task contents,
    require a particular repair list, or judge whether the scientific task is valid.
    """
    decision = str(response.get("audit_decision") or "")
    if decision not in STAGE07_APPROVED_DECISIONS:
        return
    try:
        relative = validate_relative_path(str(response.get("artifact_path") or ""))
        artifact = (workspace.resolve() / relative).resolve()
        artifact.relative_to(workspace.resolve())
        if relative != "outputs/task_pair":
            raise ValueError("approved artifact_path must be outputs/task_pair")
        if not artifact.is_dir() or not any(path.is_file() for path in artifact.rglob("*")):
            raise FileNotFoundError("approved task-pair directory is empty or missing")
        # A nested immutable handoff copy is a transport mistake and would leak internal
        # provenance into the deliverable.  Removing/rejecting this file-layout error does not
        # make a scientific judgment.
        if (artifact / "stage06_candidate").exists():
            raise ValueError("approved task-pair contains a redundant stage06_candidate source copy")
        return
    except (FileNotFoundError, OSError, ValueError) as exc:
        message = f"Stage07 approved a task but did not deliver its task tree: {exc}"
        result.status = "failed"
        result.failure_class = "missing_agent_artifact"
        result.retryable = True
        result.error = {"error_type": "MissingAgentArtifact", "message": message}
        write_json(workspace / "agent_run.json", result.audit_record())
        raise AgentExecutionError(
            message,
            failure_class="missing_agent_artifact",
            retryable=True,
            result=result,
        ) from exc


def _copy_stage07_source_packet(source_root: Path, destination: Path) -> None:
    """Copy a compact, text-first source packet for Stage07.

    The full Stage04 snapshot remains available to the pipeline for provenance, but repeatedly
    handing PDFs, raster images and parser internals to an audit Agent wastes context and makes
    recovery attempts needlessly expensive.  Keep canonical text/layout/table/coordinate files
    and metadata; retain PDFs only when explicitly requested by configuration at the caller level
    in a future extension.
    """

    destination.mkdir(parents=True, exist_ok=True)
    allowed_top = {
        "source_manifest.json",
        "toolbox_snapshot.json",
        "resource_policy.json",
    }
    for name in allowed_top:
        source = source_root / name
        if source.is_file():
            shutil.copy2(source, destination / name)

    documents = source_root / "documents"
    if not documents.is_dir():
        return
    for document_root in sorted(path for path in documents.iterdir() if path.is_dir()):
        target = destination / "documents" / document_root.name
        target.mkdir(parents=True, exist_ok=True)
        for name in (
            "normalized_document.md",
            "content_blocks.jsonl",
            "layout_text.txt",
            "pypdf_layout.txt",
            "tables.json",
            "source_metadata.json",
        ):
            source = document_root / name
            if source.is_file():
                shutil.copy2(source, target / name)
        for subdir in ("derived_coordinates", "derived_tables"):
            source_dir = document_root / subdir
            if source_dir.is_dir():
                shutil.copytree(source_dir, target / subdir, dirs_exist_ok=True)

    write_json(
        destination / "source_packet_manifest.json",
        {
            "schema_version": "stage07-source-packet-v1",
            "source_root_manifest_hash": directory_manifest(source_root)["content_hash"],
            "included": [
                "canonical normalized/layout text",
                "derived tables and coordinates",
                "document metadata",
                "toolbox snapshot and resource policy",
            ],
            "excluded": ["pdf", "raster images", "parser internals", "duplicate evidence exports"],
        },
    )


def _stage07_approved_artifact(response: dict[str, Any], artifact_root: Path) -> Path:
    relative = validate_relative_path(str(response.get("artifact_path") or ""))
    if relative != "outputs/task_pair":
        raise ValueError("approved Stage07 artifact_path must be outputs/task_pair")
    path = (artifact_root.resolve() / relative).resolve()
    path.relative_to(artifact_root.resolve())
    if not path.is_dir() or not any(item.is_file() for item in path.rglob("*")):
        raise FileNotFoundError(f"Stage07 task artifact is missing or empty: {path}")
    return path


def _publish_stage07_rejection(
    *,
    stage_root: Path,
    paper_id: str,
    response: dict[str, Any],
    stage06_record: dict[str, Any],
    handoff_root: Path,
) -> Path:
    staging = prepare_clean_directory(
        stage_root / "staging" / safe_component(paper_id) / f"rejected-{uuid.uuid4().hex[:8]}"
    )
    for name in (
        "paper_info.json",
        "workflow_review.json",
        "construction_receipt.json",
        "stage06_handoff.json",
    ):
        source = handoff_root / name
        if source.is_file():
            shutil.copy2(source, staging / name)
    write_json(staging / "stage06_handoff_record.json", stage06_record)
    write_json(staging / "stage07_audit.json", response)
    write_manifest(staging, staging / "audit_manifest.json")
    target = stage_root / "rejected_tasks" / safe_component(paper_id)
    atomic_commit_tree(staging, target)
    return target


def _publish_mode_bundles(
    pair_root: Path,
    published_root: Path,
    *,
    task_pair_id: str,
) -> dict[str, str]:
    """Export each approved mode as an isolated benchmark task directory.

    The Agent owns the contents of each mode directory.  The orchestrator only isolates and copies
    that directory; it does not apply an allowlist or run a semantic validator.  Sibling mode,
    hidden reference and pair-level provenance are never copied into a public task.
    """

    published_root.mkdir(parents=True, exist_ok=True)
    exported: dict[str, str] = {}
    for mode in ("paper_reproduction", "autonomous_research"):
        source = pair_root / mode
        if not source.is_dir():
            continue
        destination = published_root / f"{safe_component(task_pair_id)}_{mode}"
        staging = prepare_clean_directory(
            published_root / f".{safe_component(task_pair_id)}_{mode}-{uuid.uuid4().hex[:8]}"
        )
        copytree_exact(source, staging)
        # This hash cache is useful only inside Stage06/07 and is not part of the benchmark task.
        (staging / "public_manifest.json").unlink(missing_ok=True)
        atomic_commit_tree(staging, destination)
        make_writable(staging)
        shutil.rmtree(staging, ignore_errors=True)
        exported[mode] = str(destination)
    return exported


def _resolve_stage07_source_root(
    *,
    record: dict[str, Any],
    paper_id: str,
    documents: list[dict[str, Any]],
    stage_root: Path,
    config: dict[str, Any],
) -> Path:
    source_value = record.get("source_snapshot_path")
    if source_value:
        source = Path(str(source_value)).expanduser().resolve()
        if source.is_dir():
            return source
    return _prepare_stage07_fallback_source(
        paper_id=paper_id,
        documents=documents,
        stage_root=stage_root,
        config=config,
    )


def _prepare_stage07_fallback_source(
    *,
    paper_id: str,
    documents: list[dict[str, Any]],
    stage_root: Path,
    config: dict[str, Any],
) -> Path:
    if not documents:
        raise FileNotFoundError(f"No Stage04 source documents are available for {paper_id}")
    identity = canonical_hash(
        [
            {
                "document_id": row.get("document_id"),
                "sha256": row.get("sha256"),
                "source_path": row.get("source_path"),
                "normalized_markdown_path": row.get("normalized_markdown_path"),
                "content_blocks_path": row.get("content_blocks_path"),
            }
            for row in documents
        ]
    )
    root = stage_root / "source_snapshots" / safe_component(paper_id) / identity[:16]
    complete = root / "snapshot_complete.json"
    if complete.is_file():
        return root
    prepare_clean_directory(root)
    source_manifest: list[dict[str, Any]] = []
    for document in sorted(documents, key=lambda row: str(row.get("document_id") or "")):
        document_id = safe_component(str(document.get("document_id") or "document"))
        document_root = root / "documents" / document_id
        document_root.mkdir(parents=True, exist_ok=True)
        copied: list[str] = []
        for key, name in (
            ("normalized_markdown_path", "normalized_document.md"),
            ("content_blocks_path", "content_blocks.jsonl"),
            ("layout_text_path", "layout_text.txt"),
            ("pypdf_layout_path", "pypdf_layout.txt"),
            ("tables_path", "tables.json"),
        ):
            value = document.get(key)
            if not value:
                continue
            source = Path(str(value)).expanduser().resolve()
            if source.is_file():
                shutil.copy2(source, document_root / name)
                copied.append(f"documents/{document_id}/{name}")
        source_value = document.get("source_path")
        if source_value:
            source_pdf = Path(str(source_value)).expanduser().resolve()
            if source_pdf.is_file() and source_pdf.suffix.casefold() == ".pdf":
                if str(document.get("document_role") or "") == "main_paper":
                    target = root / "main_paper.pdf"
                else:
                    target = root / "supplementary" / f"{document_id}.pdf"
                    target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source_pdf, target)
                copied.append(target.relative_to(root).as_posix())
        write_json(document_root / "source_metadata.json", document)
        source_manifest.append(
            {
                "document_id": document.get("document_id"),
                "document_role": document.get("document_role"),
                "materials": copied,
            }
        )
    write_json(root / "source_manifest.json", source_manifest)
    toolbox_path = config.get("toolbox_capabilities")
    if toolbox_path and Path(str(toolbox_path)).expanduser().is_file():
        write_json(
            root / "toolbox_snapshot.json",
            installed_software_inventory(
                read_json(Path(str(toolbox_path)).expanduser())
            ),
        )
    else:
        write_json(
            root / "toolbox_snapshot.json",
            installed_software_inventory({"snapshot_status": "unavailable"}),
        )
    write_json(root / "resource_policy.json", config.get("resource_policy") or {})
    write_json(
        complete,
        {"paper_id": paper_id, "identity": identity, "created_at": now_utc()},
    )
    make_read_only(root)
    return root


def _stage07_toolbox_snapshot(
    source_root: Path, handoff_root: Path, config: dict[str, Any]
) -> dict[str, Any]:
    for path in (
        source_root / "toolbox_snapshot.json",
        Path(str(config.get("toolbox_capabilities") or "" )).expanduser(),
    ):
        if str(path) and path.is_file():
            return installed_software_inventory(read_json(path))
    requirements = handoff_root / "toolbox_requirements.json"
    return installed_software_inventory(
        {
            "snapshot_status": "unavailable",
            "requirements": read_json(requirements) if requirements.is_file() else [],
        }
    )


def _stage07_resource_policy(source_root: Path, config: dict[str, Any]) -> dict[str, Any]:
    path = source_root / "resource_policy.json"
    if path.is_file():
        value = read_json(path)
        if isinstance(value, dict):
            return value
    return dict(config.get("resource_policy") or {})


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
    raise RuntimeError(
        "The legacy objective-audit path is disabled: only the Stage07 audit-repair "
        "Agent may make scientific decisions"
    )

    # Retained temporarily for checkpoint migration reference. This code is
    # unreachable and must not be reconnected to the publication path.
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
            config.get("audit_max_tool_calls", config.get("max_tool_calls", 120))
        )
        if recovery_context:
            max_tool_calls = int(
                config.get(
                    "audit_recovery_max_tool_calls",
                    config.get("recovery_max_tool_calls", 160),
                )
            )
        max_tool_calls = max(2, max_tool_calls)
        finalization_reserve = min(
            max_tool_calls - 1,
            max(
                1,
                int(config.get("audit_finalization_reserve", 12)),
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
                "tool_choice_policy": config.get("objective_audit_tool_choice_policy", config.get("tool_choice_policy")),
                "response_format_policy": config.get("objective_audit_response_format_policy", config.get("response_format_policy")),
                "codex_wire_api": config.get("objective_audit_codex_wire_api"),
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
    """Reject use of the former code-side scientific judge."""

    raise RuntimeError(
        "deterministic_judge_audit is disabled; Stage07 Agent decisions are authoritative"
    )


def run_gold(record, config, stage_root):
    """Deprecated boundary marker: Stage07 no longer executes Gold Runs."""

    return {"status": "not_run", "reason": "gold_run_moved_outside_stage07"}


def _toolbox_snapshot_from_pair(pair_root: Path, config: dict[str, Any]) -> dict[str, Any]:
    path_value = config.get("toolbox_capabilities")
    if path_value:
        path = Path(str(path_value)).expanduser().resolve()
        if path.is_file():
            return installed_software_inventory(read_json(path))
    requirements = pair_root / "toolbox_requirements.json"
    return installed_software_inventory(
        {
            "snapshot_status": "unavailable",
            "requirements": read_json(requirements) if requirements.is_file() else [],
        }
    )


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
            "inputs/task_pair/hidden_reference/ground_truth_common.json",
            "inputs/task_pair/paper_info.json",
        ],
    }


def _focused_toolbox_view(
    toolbox: dict[str, Any], requirements: list[dict[str, Any]]
) -> dict[str, Any]:
    del requirements
    return installed_software_inventory(toolbox)


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
        "decision": "objective_failure_retryable",
        "audit_decision": "objective_failure_retryable",
        "audit_summary": "objective_failure_retryable",
        "passed": False,
        "publication_state": "not_applicable",
        "blocking_phase": "",
        "retryable": retryable,
        "failure_class": failure_class,
        "outcomes": [],
        "error": {"error_type": failure_class, "message": message[:4000]},
        "agent_run": agent_run,
    }
