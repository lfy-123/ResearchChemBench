from __future__ import annotations

import json
import shutil
import uuid
from pathlib import Path
from typing import Any

import jsonschema

from src.agents import AgentExecutionError, AgentRunRequest, create_agent_harness
from src.agents.schemas import STAGE07_AUDIT_SCHEMA
from src.agents.workspace import (
    IGNORED_MANIFEST_NAMES,
    atomic_commit_tree,
    copytree_exact,
    directory_manifest,
    input_fingerprint,
    make_read_only,
    make_writable,
    prepare_clean_directory,
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
    validate_stage07_transport_contract,
    stage07_mechanical_pre_publish_check,
    validate_agent_audit,
)
from src.stages.stage07_task_judge.package import assemble_task_packages
from src.stages.stage06_task_builder.validation import (
    canonical_paper_id,
)
from src.stages.phase_gate import (
    install_phase_gate_tool,
    run as run_shared_phase_gate,
    snapshot_sha256 as phase_gate_snapshot_sha256,
    write_final_self_check_report,
)
from src.stages.evaluator_reference import read_split_reference

STAGE07_IMPLEMENTATION_VERSION = "v20-bounded-audit-repair-20260826"
STAGE07_DIRECTORY = "stage_07_task_audit"
STAGE07_IGNORED_PAIR_FILES = {*IGNORED_MANIFEST_NAMES, "construction_record.json"}
STAGE07_APPROVED_DECISIONS = {
    "approved",
    "approved_with_repairs",
}
STAGE07_ELIGIBLE_STAGE06_DECISIONS = {
    "provisional_constructed",
    "constructed",
}


def _task_package_findings(
    reports: dict[str, dict[str, Any]] | None,
) -> list[str]:
    """Flatten package-validator findings without interpreting their meaning."""

    return sorted(
        {
            str(finding)
            for report in (reports or {}).values()
            if report.get("status") != "passed"
            for finding in report.get("findings") or []
            if str(finding).strip()
        }
    )


def _task_packages_passed(reports: dict[str, dict[str, Any]] | None) -> bool:
    return bool(reports) and set(reports) == {
        "paper_reproduction",
        "autonomous_research",
    } and all(report.get("status") == "passed" for report in reports.values())


def _assemble_task_packages_atomically(
    *,
    pair_root: Path,
    stage_root: Path,
    task_family_id: str,
    runtime_readiness: str,
    paper_id: str,
) -> dict[str, dict[str, Any]]:
    """Validate both mode packages in a private staging tree before publishing.

    The package assembler validates each mode independently.  Stage07 must
    expose neither a half pair nor a stale destination while a companion mode
    is invalid, so this wrapper gives each attempt a private root and commits
    both validated trees only after the complete pair passes.
    """

    attempt = stage_root / "package_staging" / safe_component(paper_id) / (
        f"attempt-{uuid.uuid4().hex[:8]}"
    )
    attempt.mkdir(parents=True, exist_ok=False)
    try:
        reports = assemble_task_packages(
            pair_root=pair_root,
            final_tasks_root=attempt,
            task_family_id=task_family_id,
            runtime_readiness=runtime_readiness,
        )
        if not _task_packages_passed(reports):
            # The attempt tree is about to be removed.  Never expose a path
            # to a successfully validated companion mode when the pair as a
            # whole was not publishable.
            return {
                mode: {
                    **report,
                    "path": "",
                }
                for mode, report in reports.items()
            }
        published: dict[str, dict[str, Any]] = {}
        for mode, report in reports.items():
            source = Path(str(report["path"])).resolve()
            destination = (
                stage_root / "final_tasks" / mode / safe_component(str(report["task_id"]))
            )
            atomic_commit_tree(source, destination)
            published[mode] = {
                **report,
                "path": str(destination),
            }
        return published
    finally:
        # The staging tree is private and contains no user data outside the
        # audited pair.  Remove it after either a failed validation or a
        # successful atomic commit.
        if attempt.exists():
            make_writable(attempt)
            shutil.rmtree(attempt, ignore_errors=True)
        for parent in (attempt.parent, attempt.parent.parent):
            try:
                parent.rmdir()
            except OSError:
                # Another paper/attempt may still use the shared staging
                # parent; leaving a harmless empty directory is preferable to
                # touching anything outside this scoped tree.
                pass


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
                    for key in ("input_assets", "workflow_steps", "items", "rules", "evidence"):
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
        paper_id = canonical_paper_id(paper_id)
        handoff_value = record.get("handoff_path") or record.get("task_pair_path")
        try:
            if not handoff_value:
                return _audit_technical_block(
                    run_id,
                    paper_id,
                    "stage06_handoff_missing",
                    "Stage06 did not provide a handoff path.",
                )
            handoff_root = Path(str(handoff_value)).expanduser().resolve()
            if not handoff_root.is_dir():
                return _audit_technical_block(
                    run_id,
                    paper_id,
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
                source_stage06_decision=source_stage06_decision,
                handoff_root=handoff_root,
                source_root=source_root,
                stage06_record=record,
                config=config,
            )
            decision = str(response["audit_decision"])
            if decision == "technical_blocked":
                return _audit_technical_block(
                    run_id,
                    paper_id,
                    "agent_reported_objective_failure",
                    str(response.get("summary") or "Stage07 could not complete the audit."),
                    agent_run=agent_run,
                )
            response["paper_id"] = paper_id
            final_path: str | None = None
            final_task_paths: dict[str, str] = {}
            task_package_reports: dict[str, dict[str, Any]] = {}
            if decision in STAGE07_APPROVED_DECISIONS:
                task_root = _stage07_approved_artifact(response, artifact_root)
                target = stage_root / "audited_tasks" / safe_component(paper_id)
                atomic_commit_tree(task_root, target)
                # A cached artifact may predate the current transport contract.
                # Normalize it through the same provenance-recorded boundary as
                # a fresh Stage07A result; never perform a hidden identity write
                # outside that record.
                final_normalization = validate_stage07_transport_contract(target, paper_id=paper_id)
                if final_normalization.get("records"):
                    response["orchestrator_normalization_records"] = (
                        final_normalization["records"]
                    )
                if final_normalization.get("new_records") and final_normalization.get(
                    "findings"
                ):
                    response["orchestrator_normalization_findings"] = (
                        final_normalization["findings"]
                    )
                write_manifest(target, target / "task_pair_manifest.json")
                write_json(target / "stage07_audit.json", response)
                write_json(target / "stage06_handoff_record.json", record)
                mechanical_report = stage07_mechanical_pre_publish_check(target, paper_id=paper_id)
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
                    runtime_readiness = (
                        "needs_software"
                        if response.get("toolbox_status") == "needs_software"
                        else "ready"
                    )
                    task_package_reports = _assemble_task_packages_atomically(
                        pair_root=target,
                        stage_root=stage_root,
                        task_family_id=paper_id,
                        runtime_readiness=runtime_readiness,
                        paper_id=paper_id,
                    )
                    final_task_paths = {
                        mode: str(report["path"])
                        for mode, report in task_package_reports.items()
                        if report.get("status") == "passed" and report.get("path")
                    }
                    package_findings = _task_package_findings(task_package_reports)

                    if len(final_task_paths) == len(task_package_reports) == 2:
                        response["publication_state"] = (
                            "approved_needs_software"
                            if runtime_readiness == "needs_software"
                            else "approved_ready"
                        )
                        response["blocking_phase"] = ""
                    else:
                        response["orchestrator_mechanical_status"] = "blocked"
                        response["orchestrator_mechanical_findings"] = package_findings
                        response["publication_state"] = "technical_blocked"
                        response["blocking_phase"] = "task_package"
                else:
                    # A transport failure blocks publication, but does not
                    # reopen the scientific audit or silently turn it into a
                    # scientific rejection.
                    response["orchestrator_mechanical_status"] = "blocked"
                    response["orchestrator_mechanical_findings"] = mechanical_report.get(
                        "findings", []
                    )
                    response["publication_state"] = "technical_blocked"
                    response["blocking_phase"] = "prepublish_mechanical"
                write_json(target / "stage07_audit.json", response)
                write_manifest(target, target / "audit_manifest.json")
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
                "paper_id": paper_id,
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
                "publish_ready": len(final_task_paths) == 2,
                "mechanical_approved_but_unpublished": bool(
                    decision in STAGE07_APPROVED_DECISIONS
                    and response.get("orchestrator_mechanical_status") == "blocked"
                ),
                "selected_workflow_preserved": response.get(
                    "selected_workflow_preserved"
                ),
                "repair_count": len(response.get("repairs") or []),
                "toolbox_status": response.get("toolbox_status"),
                "execution_readiness": response.get("execution_readiness", "unknown"),
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
                "stage07a_gate_status": response.get("stage07a_gate_status", "not_run"),
                "stage07a_gate_attempts": response.get("stage07a_gate_attempts", 0),
                "stage07a_gate_findings": response.get("stage07a_gate_findings", []),
                "task_package_reports": task_package_reports,
                "task_pair_path": final_path,
                "final_task_paths": final_task_paths,
                "audit_path": str(target),
                "agent_harness": harness.name,
                "agent_model": harness.model,
            }
        except AgentExecutionError as exc:
            return _audit_technical_block(
                run_id,
                paper_id,
                exc.failure_class,
                str(exc),
                agent_run=exc.result.audit_record() if exc.result else None,
            )
        except (FileNotFoundError, OSError) as exc:
            return _audit_technical_block(
                run_id,
                paper_id,
                "audit_input_unavailable",
                f"{type(exc).__name__}: {exc}",
            )
        except Exception as exc:
            return _audit_technical_block(
                run_id,
                paper_id,
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
        "rejected_scientific_unrepairable": sum(
            row.get("audit_decision") == "rejected_scientific_unrepairable"
            for row in records
        ),
        "technical_blocked": sum(
            row.get("audit_decision") == "technical_blocked" for row in records
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
        "stage07a_gate_bypassed": sum(
            row.get("stage07a_gate_status") == "bypassed_with_warnings"
            for row in records
        ),
        "stage07a_gate_attempts": sum(
            int(row.get("stage07a_gate_attempts") or 0) for row in records
        ),
        "stage07a_gate_findings": sorted(
            {
                str(finding)
                for row in records
                for finding in row.get("stage07a_gate_findings") or []
            }
        ),
        "publish_ready": sum(bool(row.get("publish_ready")) for row in records),
        "publication_states": {
            state: sum(row.get("publication_state") == state for row in records)
            for state in (
                "not_applicable",
                "approved_ready",
                "approved_needs_software",
                "mechanical_blocked",
                "technical_blocked",
            )
        },
        "blocking_phases": {
            phase: sum(row.get("blocking_phase") == phase for row in records)
            for phase in ("prepublish_mechanical", "task_package")
        },
        "final_tasks": sum(len(row.get("final_task_paths") or {}) for row in records),
        "paper_ids": sorted({str(row.get("paper_id")) for row in records if row.get("paper_id")}),
        "needs_software": sum(row.get("toolbox_status") == "needs_software" for row in records),
        "execution_readiness": {
            state: sum(row.get("execution_readiness") == state for row in records)
            for state in ("ready", "conditional", "unknown")
        },
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
    if bool(config.get("checkpoint_cache_enabled", True)) and checkpoint.is_file() and artifact_root.is_dir():
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

    agent_self_check_mode = bool(config.get("stage07_agent_self_check", True))
    root = prepare_clean_directory(
        stage_root
        / "workspaces"
        / safe_component(paper_id)
        / "audit_repair"
        / f"attempt-01-{uuid.uuid4().hex[:8]}"
    )
    inputs = root / "inputs"
    inputs.mkdir(parents=True, exist_ok=True)
    install_phase_gate_tool(inputs / "tools")
    copytree_exact(handoff_root, inputs / "stage06_candidate")
    _copy_stage07_source_packet(source_root, inputs / "source_materials")
    write_json(inputs / "stage06_record.json", stage06_record)
    write_json(inputs / "toolbox_snapshot.json", toolbox)
    write_json(inputs / "resource_policy.json", resource_policy)
    write_json(
        inputs / "input_manifest.json",
        {
            "paper_id": paper_id,
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
    max_tool_calls = max(
        4,
        int(
            config.get(
                "audit_repair_max_tool_calls",
                config.get("audit_max_tool_calls", config.get("max_tool_calls", 120)),
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
    request = AgentRunRequest(
            phase="stage07_audit_repair",
            record_id=paper_id,
            workspace=root,
            instructions=audit_instructions(
                paper_id=paper_id,
                manifest_hash=fingerprint,
                max_tool_calls=max_tool_calls,
                finalization_reserve=finalization_reserve,
                source_stage06_decision=source_stage06_decision,
            ),
            output_schema=STAGE07_AUDIT_SCHEMA,
            prompt_version=STAGE07_AUDIT_VERSION,
            timeout_seconds=int(config.get("timeout_seconds", 7200)),
            metadata={
                "paper_id": paper_id,
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
            result.retryable = False
            result.error = {
                "error_type": "InvalidPhaseContract",
                "message": message,
            }
            write_json(root / "agent_run.json", result.audit_record())
            raise AgentExecutionError(
                message,
                failure_class="invalid_phase_contract",
                retryable=False,
                result=result,
            )
        response = _finalize_stage07_response(
            response=response,
            task_root=outputs / "task_pair",
            toolbox=toolbox,
            paper_id=paper_id,
        )
        write_json(outputs / "stage07_audit.json", response)
        _require_stage07_artifact_delivery(response, root, result)
        pre_self_report = (
            read_json(root / "agent_self_check_report.json")
            if (root / "agent_self_check_report.json").is_file()
            else None
        )
        gate_applicable = response.get("audit_decision") in STAGE07_APPROVED_DECISIONS
        gate_findings = (
            _stage07a_phase_gate_findings(response, root, paper_id=paper_id)
            if gate_applicable
            else []
        )
        blocking_gate_findings = [
            finding for finding in gate_findings if is_blocking_finding(finding)
        ]
        gate_status = (
            "failed" if blocking_gate_findings else "passed"
        ) if gate_applicable else "not_applicable"
        final_self_report = write_final_self_check_report(
            phase="stage07a",
            outputs=outputs,
            report_root=root,
            pre_normalization=pre_self_report,
            findings=gate_findings,
        )
        if gate_applicable:
            gate_report = {
                "schema_version": "stage06-07-phase-gate/v3",
                "phase": "stage07a",
                "implementation_phase": "stage07a_audit",
                "paper_id": paper_id,
                "authority": "orchestrator_external_read_only",
                "status": gate_status,
                "attempt": 1,
                "max_checks": 1,
                "findings": sorted(set(gate_findings)),
                "blocking_findings": sorted(set(blocking_gate_findings)),
                "warnings": sorted(set(gate_findings) - set(blocking_gate_findings)),
                "agent_self_check_required": agent_self_check_mode,
                "snapshot_sha256": phase_gate_snapshot_sha256(outputs),
                "snapshot_stage": "post_normalization",
                "self_check_snapshot_sha256": final_self_report["snapshot_sha256"],
                "self_check_snapshot_parity": final_self_report.get("snapshot_parity"),
                "created_at": now_utc(),
            }
            write_json(root / "external_phase_gate_report.json", gate_report)
        response = dict(response)
        response.update(
            {
                "stage07a_gate_status": gate_status,
                "stage07a_gate_attempts": 1 if gate_applicable else 0,
                "stage07a_gate_findings": sorted(set(gate_findings)),
            }
        )
        write_json(outputs / "stage07_audit.json", response)
    except AgentExecutionError:
        raise
    staging = prepare_clean_directory(
        artifact_root.parent / f".{artifact_root.name}-{uuid.uuid4().hex[:8]}"
    )
    copytree_exact(outputs, staging / "outputs")
    for name in ("agent_self_check_report.json", "external_phase_gate_report.json"):
        report = root / name
        if report.is_file():
            shutil.copy2(report, staging / name)
    atomic_commit_tree(staging, artifact_root)
    write_json(
        checkpoint,
        {
            "paper_id": paper_id,
            "input_fingerprint": fingerprint,
            "prompt_version": STAGE07_AUDIT_VERSION,
            "response": response,
            "agent_run": result.audit_record(),
            "artifact_manifest_hash": directory_manifest(artifact_root)["content_hash"],
            "phase_gate": (
                read_json(root / "external_phase_gate_report.json")
                if (root / "external_phase_gate_report.json").is_file()
                else {
                    "status": response.get("stage07a_gate_status", "not_applicable"),
                    "attempt": response.get("stage07a_gate_attempts", 0),
                    "findings": response.get("stage07a_gate_findings", []),
                }
            ),
            "completed_at": now_utc(),
        },
    )
    return response, {**result.audit_record(), "cache_hit": False}, artifact_root


def _finalize_stage07_response(
    *,
    response: dict[str, Any],
    task_root: Path,
    toolbox: dict[str, Any],
    paper_id: str | None = None,
) -> dict[str, Any]:
    """Normalize transport contracts before the read-only publication Gate."""

    decision = str(response.get("audit_decision") or "")
    if decision not in STAGE07_APPROVED_DECISIONS:
        return response

    validation = validate_stage07_transport_contract(task_root, paper_id=paper_id)
    if validation.get("findings"):
        response["orchestrator_transport_findings"] = validation["findings"]
    write_manifest(task_root, task_root / "task_pair_manifest.json")
    return response


def _approved_receipt_contract_findings(response: dict[str, Any]) -> list[str]:
    """Require the Agent evidence that makes an approval auditable.

    This is a phase-output contract, not a second scientific judge: values remain
    Agent-authored and the checks below only establish that Stage07 actually left
    the scope, closure, repair, and resource evidence required by its role.
    """

    decision = str(response.get("audit_decision") or "")
    if decision not in STAGE07_APPROVED_DECISIONS:
        return []
    findings: list[str] = []
    if response.get("artifact_path") != "outputs/task_pair":
        findings.append("approved_artifact_path_invalid")
    if not str(response.get("paper_id") or "").strip():
        findings.append("approved_paper_id_missing")
    if not isinstance(response.get("selected_workflow_preserved"), bool):
        findings.append("approved_selected_workflow_preserved_missing")
    for key in ("repairs", "remaining_issues", "required_additions"):
        if not isinstance(response.get(key), list):
            findings.append(f"approved_{key}_invalid")
    expected_values = {
        "toolbox_status": {"available", "needs_software", "unknown"},
        "execution_readiness": {"ready", "conditional", "unknown"},
        "resource_status": {"feasible", "high_cost", "infeasible", "uncertain"},
        "contract_status": {"passed", "findings", "not_applicable"},
        "disclosure_status": {"passed", "needs_review", "not_applicable"},
        "schema_load_diagnostic": {"passed", "failed", "not_run"},
    }
    for key, allowed in expected_values.items():
        if response.get(key) not in allowed:
            findings.append(f"approved_{key}_missing_or_invalid")
    if response.get("scientific_decision") != decision:
        findings.append("approved_scientific_decision_mismatch")

    audit_table = response.get("scientific_audit_table")
    if not isinstance(audit_table, list) or len(audit_table) < 6:
        findings.append("approved_scientific_audit_table_incomplete")
    else:
        for index, row in enumerate(audit_table):
            if not isinstance(row, dict):
                findings.append(f"approved_scientific_audit_row_invalid:{index}")
                continue
            if not str(row.get("check") or "").strip():
                findings.append(f"approved_scientific_audit_check_missing:{index}")
            if row.get("status") not in {"closed", "repairable", "unrepairable"}:
                findings.append(f"approved_scientific_audit_status_invalid:{index}")

    audit = response.get("representativeness_audit")
    if not isinstance(audit, dict):
        findings.append("approved_representativeness_audit_missing")
    else:
        for key in (
            "paper_claims_checked",
            "coverage_summary",
        ):
            if not isinstance(audit.get(key), list):
                findings.append(f"approved_representativeness_{key}_invalid")
        if not str(audit.get("selected_scope_kind") or "").strip():
            findings.append("approved_representativeness_scope_missing")
        if not str(audit.get("rationale") or "").strip():
            findings.append("approved_representativeness_rationale_missing")
        dependency = audit.get("ultimate_claim_dependency")
        if not isinstance(dependency, dict):
            findings.append("approved_ultimate_claim_dependency_missing")
        else:
            if not str(dependency.get("advertised_conclusion") or "").strip():
                findings.append("approved_advertised_conclusion_missing")
            for key in (
                "direct_computational_evidence",
                "supporting_only_evidence",
            ):
                if not isinstance(dependency.get(key), list):
                    findings.append(f"approved_ultimate_claim_{key}_invalid")
            if not str(dependency.get("selected_workflow_position") or "").strip():
                findings.append("approved_selected_workflow_dependency_position_missing")
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
        result.retryable = False
        result.error = {"error_type": "MissingAgentArtifact", "message": message}
        write_json(workspace / "agent_run.json", result.audit_record())
        raise AgentExecutionError(
            message,
            failure_class="missing_agent_artifact",
            retryable=False,
            result=result,
        ) from exc


def _stage07a_phase_gate_findings(
    response: dict[str, Any],
    workspace: Path,
    *,
    paper_id: str | None = None,
) -> list[str]:
    """Run exactly the shared Gate exposed to the Agent self-check."""

    if str(response.get("audit_decision") or "") not in STAGE07_APPROVED_DECISIONS:
        return []
    return sorted(set(run_shared_phase_gate("stage07a", workspace / "outputs")["findings"]))


def _copy_stage07_source_packet(source_root: Path, destination: Path) -> None:
    """Copy a compact, text-first source packet for Stage07.

    The full Stage04 snapshot remains available to the pipeline for provenance, but repeatedly
    handing PDFs, raster images and parser internals to an audit Agent wastes context. Keep canonical
    text/layout/table/coordinate files
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






















def _audit_technical_block(
    run_id: str,
    paper_id: str,
    failure_class: str,
    message: str,
    *,
    agent_run: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        **record_header(run_id=run_id, stage="stage07", paper_id=paper_id),
        "paper_id": paper_id,
        "processing_status": "failed",
        "decision": "technical_blocked",
        "audit_decision": "technical_blocked",
        "audit_summary": "technical_blocked",
        "passed": False,
        "publication_state": "not_applicable",
        "blocking_phase": "",
        "failure_class": failure_class,
        "outcomes": [],
        "error": {"error_type": failure_class, "message": message[:4000]},
        "agent_run": agent_run,
    }
