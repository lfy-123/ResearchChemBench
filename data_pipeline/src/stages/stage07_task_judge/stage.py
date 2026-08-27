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
    atomic_commit_tree,
    copytree_exact,
    input_fingerprint,
    make_read_only,
    make_writable,
    prepare_clean_directory,
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
from src.stages.pdf_layout import install_document_query_tool
from src.stages.phase_gate import install_phase_gate_tool
from src.stages.stage07_task_judge.package import (
    assemble_release_pair,
    write_release_manifest,
)
from src.stages.stage07_task_judge.prompts import (
    STAGE07_AUDIT_PROMPT_VERSION,
    final_task_audit_instructions,
)
from src.stages.stage07_task_judge.validation import (
    APPROVED_AUDIT_DECISIONS,
    external_audit_gate,
    validate_audit_receipt,
)


STAGE07_IMPLEMENTATION_VERSION = "v24-per-mode-scientific-audit"
STAGE07_DIRECTORY = "stage_07_task_audit"
ELIGIBLE_STAGE06_DECISIONS = {"provisional_constructed", "constructed"}


def run_stage07(*, build_records, documents, config, model, workspace: Path, run_id: str):
    """Audit complete Stage06 pairs; never rebuild a missing or failed task."""

    del documents  # The immutable Stage06 source snapshot is the audit authority.
    stage_root = workspace / STAGE07_DIRECTORY
    stage_root.mkdir(parents=True, exist_ok=True)
    release_root = workspace / "release"
    eligible = [
        row
        for row in build_records
        if row.get("decision") in ELIGIBLE_STAGE06_DECISIONS
        and row.get("handoff_ready") is True
    ]
    harness = create_agent_harness(
        str(config.get("harness") or "codex"),
        config=config,
        model_config=dict(getattr(model, "config", {}) or {}),
        model_client=model,
    )

    def audit(record: dict[str, Any]) -> dict[str, Any]:
        paper_id = str(record.get("paper_id") or "")
        try:
            candidate = Path(str(record.get("handoff_path") or "")).expanduser().resolve()
            source = Path(str(record.get("source_snapshot_path") or "")).expanduser().resolve()
            if not candidate.is_dir() or not source.is_dir():
                return _technical_block(
                    run_id, paper_id, "stage06_handoff_missing",
                    "Stage07 requires the complete candidate and immutable source snapshot."
                )
            response, agent_audit, agent_workspace = _run_audit_agent(
                harness=harness,
                stage_root=stage_root,
                paper_id=paper_id,
                candidate=candidate,
                source=source,
                config=config,
            )
            artifact = validate_audit_receipt(
                response, paper_id=paper_id, workspace=agent_workspace
            )
            decision = str(response["audit_decision"])
            if decision == "technical_blocked":
                return _technical_block(
                    run_id, paper_id, "agent_audit_incomplete",
                    str(response.get("summary") or "The audit Agent could not complete its work."),
                    agent_run=agent_audit,
                )
            if decision not in APPROVED_AUDIT_DECISIONS:
                rejection = _publish_rejection(
                    stage_root=stage_root,
                    paper_id=paper_id,
                    receipt=response,
                    agent_workspace=agent_workspace,
                )
                return {
                    **record_header(run_id=run_id, stage="stage07", paper_id=paper_id),
                    "paper_id": paper_id,
                    "processing_status": "completed",
                    "decision": decision,
                    "passed": False,
                    "publish_ready": False,
                    "audit_path": str(rejection),
                    "repair_count": len(response.get("repairs") or []),
                    "agent_run": agent_audit,
                }

            assert artifact is not None
            gate = external_audit_gate(artifact)
            write_json(
                agent_workspace / "external_phase_gate_report.json",
                {**gate, "authority": "orchestrator_external_read_only", "created_at": now_utc()},
            )
            if gate["status"] != "passed":
                _persist_failed_audit(stage_root, paper_id, agent_workspace)
                return _technical_block(
                    run_id, paper_id, "audit_contract_mismatch",
                    "; ".join(gate["findings"]), agent_run=agent_audit, gate_report=gate
                )

            audited_staging = prepare_clean_directory(
                stage_root / "staging" / safe_component(paper_id) / uuid.uuid4().hex[:8]
            )
            copytree_exact(artifact, audited_staging)
            make_writable(audited_staging)
            write_json(audited_staging / "stage07_audit.json", response)
            write_json(audited_staging / "external_phase_gate_report.json", gate)
            write_manifest(audited_staging, audited_staging / "audit_manifest.json")
            audited = stage_root / "audited_tasks" / safe_component(paper_id)
            atomic_commit_tree(audited_staging, audited)
            release = assemble_release_pair(
                pair_root=audited,
                release_root=release_root,
                paper_id=paper_id,
                release_modes=list(response.get("release_modes") or []),
            )
            publish_ready = release["status"] == "passed"
            return {
                **record_header(run_id=run_id, stage="stage07", paper_id=paper_id),
                "paper_id": paper_id,
                "processing_status": "completed" if publish_ready else "failed",
                "decision": decision if publish_ready else "technical_blocked",
                "scientific_audit_decision": decision,
                "passed": publish_ready,
                "publish_ready": publish_ready,
                "publication_state": "approved_ready" if publish_ready else "technical_blocked",
                "failure_class": "" if publish_ready else "release_assembly_failed",
                "gate_status": gate["status"],
                "gate_findings": gate["findings"],
                "gate_diagnostics": gate["diagnostics"],
                "repair_count": len(response.get("repairs") or []),
                "audited_task_path": str(audited),
                "release_report": release,
                "final_task_paths": {
                    mode: report["path"]
                    for mode, report in release.get("tasks", {}).items()
                    if report.get("status") == "passed"
                },
                "agent_run": agent_audit,
                "agent_harness": harness.name,
                "agent_model": harness.model,
            }
        except AgentExecutionError as exc:
            return _technical_block(
                run_id, paper_id, exc.failure_class, str(exc),
                agent_run=exc.result.audit_record() if exc.result else None,
            )
        except (
            FileNotFoundError,
            OSError,
            ValueError,
            json.JSONDecodeError,
            jsonschema.ValidationError,
        ) as exc:
            return _technical_block(
                run_id, paper_id, "audit_processing_error", f"{type(exc).__name__}: {exc}"
            )

    records = ordered_parallel_map(
        audit, eligible, max_workers=int(config.get("workers", 1))
    )
    write_jsonl(stage_root / "audit_results.jsonl", records)
    write_release_manifest(release_root=release_root, run_id=run_id, records=records)
    summary = {
        **record_header(run_id=run_id, stage="stage07"),
        "implementation_version": STAGE07_IMPLEMENTATION_VERSION,
        "papers": len(records),
        "approved": sum(row.get("decision") == "approved" for row in records),
        "approved_with_repairs": sum(
            row.get("scientific_audit_decision") == "approved_with_repairs"
            for row in records
        ),
        "rejected_scientific_unrepairable": sum(
            row.get("decision") == "rejected_scientific_unrepairable" for row in records
        ),
        "technical_blocked": sum(row.get("decision") == "technical_blocked" for row in records),
        "mechanical_publish_blocked": sum(
            row.get("failure_class") in {"audit_contract_mismatch", "release_assembly_failed"}
            for row in records
        ),
        "publish_ready": sum(bool(row.get("publish_ready")) for row in records),
        "decisions": decision_counts(records),
        "release_path": str(release_root),
        "agent_harness": harness.name,
        "agent_model": harness.model,
    }
    write_json(stage_root / "stage_summary.json", summary)
    return {"records": records, "summary": summary}


def _run_audit_agent(
    *, harness, stage_root: Path, paper_id: str, candidate: Path, source: Path,
    config: dict[str, Any]
) -> tuple[dict[str, Any], dict[str, Any], Path]:
    fingerprint = input_fingerprint(
        {
            "candidate": str(candidate),
            "source": str(source),
            "prompt": STAGE07_AUDIT_PROMPT_VERSION,
            "schema": canonical_hash(STAGE07_AUDIT_SCHEMA),
            "model": harness.model,
        }
    )
    workspace = prepare_clean_directory(
        stage_root / "workspaces" / safe_component(paper_id) /
        f"attempt-01-{uuid.uuid4().hex[:8]}"
    )
    copytree_exact(candidate, workspace / "inputs" / "candidate")
    copytree_exact(source, workspace / "inputs" / "source")
    (workspace / "inputs" / "tools").mkdir(parents=True)
    install_phase_gate_tool(workspace / "inputs" / "tools")
    install_document_query_tool(workspace / "inputs" / "tools")
    (workspace / "outputs").mkdir()
    make_read_only(workspace / "inputs")
    request = AgentRunRequest(
        phase="final_task_scientific_audit",
        record_id=paper_id,
        workspace=workspace,
        instructions=final_task_audit_instructions(
            paper_id=paper_id,
            max_tool_calls=int(config.get("audit_repair_max_tool_calls", 120)),
        ),
        output_schema=STAGE07_AUDIT_SCHEMA,
        prompt_version=STAGE07_AUDIT_PROMPT_VERSION,
        timeout_seconds=int(config.get("timeout_seconds", 7200)),
        metadata={
            "paper_id": paper_id,
            "input_fingerprint": fingerprint,
            "max_tool_calls": int(config.get("audit_repair_max_tool_calls", 120)),
            "finalization_reserve": int(config.get("audit_repair_finalization_reserve", 16)),
            "structured_artifact_path": "outputs/audit_receipt.json",
            "inline_contract": False,
        },
    )
    result = harness.run(request)
    response = result.response or {}
    jsonschema.validate(response, STAGE07_AUDIT_SCHEMA)
    receipt_path = workspace / "outputs" / "audit_receipt.json"
    if not receipt_path.is_file():
        raise AgentExecutionError(
            "Audit Agent did not write outputs/audit_receipt.json",
            failure_class="missing_agent_artifact", retryable=False, result=result,
        )
    receipt = read_json(receipt_path)
    jsonschema.validate(receipt, STAGE07_AUDIT_SCHEMA)
    return receipt, result.audit_record(), workspace


def _publish_rejection(
    *, stage_root: Path, paper_id: str, receipt: dict[str, Any], agent_workspace: Path
) -> Path:
    staging = prepare_clean_directory(
        stage_root / "staging" / safe_component(paper_id) / f"rejected-{uuid.uuid4().hex[:8]}"
    )
    write_json(staging / "audit_receipt.json", receipt)
    source = agent_workspace / "outputs" / "audited_task"
    if source.is_dir():
        copytree_exact(source, staging / "audited_candidate")
    target = stage_root / "rejections" / safe_component(paper_id)
    atomic_commit_tree(staging, target)
    return target


def _persist_failed_audit(stage_root: Path, paper_id: str, workspace: Path) -> None:
    target = stage_root / "phase_artifacts" / safe_component(paper_id)
    if target.exists():
        make_writable(target)
        shutil.rmtree(target)
    copytree_exact(workspace, target)


def _technical_block(
    run_id: str, paper_id: str, failure_class: str, message: str, *,
    agent_run: dict[str, Any] | None = None, gate_report: dict[str, Any] | None = None
) -> dict[str, Any]:
    return {
        **record_header(run_id=run_id, stage="stage07", paper_id=paper_id),
        "paper_id": paper_id,
        "processing_status": "failed",
        "decision": "technical_blocked",
        "passed": False,
        "publish_ready": False,
        "publication_state": "technical_blocked",
        "failure_class": failure_class,
        "error": {"error_type": failure_class, "message": message[:4000]},
        "agent_run": agent_run,
        "gate_report": gate_report or {},
    }


__all__ = ["run_stage07"]
