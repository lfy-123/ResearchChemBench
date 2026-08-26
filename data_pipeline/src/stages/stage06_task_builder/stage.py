from __future__ import annotations

import json
import shutil
import uuid
from pathlib import Path
from typing import Any

import jsonschema

from src.agents import AgentExecutionError, AgentRunRequest, create_agent_harness
from src.agents.schemas import STAGE06_SYNTHESIS_SCHEMA
from src.agents.workspace import (
    atomic_commit_tree,
    copytree_exact,
    input_fingerprint,
    make_read_only,
    make_writable,
    prepare_clean_directory,
    sha256_file,
    write_manifest,
)
from src.contracts import (
    canonical_hash,
    decision_counts,
    now_utc,
    read_json,
    read_jsonl,
    record_header,
    safe_component,
    write_json,
    write_jsonl,
)
from src.core.concurrency import ordered_parallel_map
from src.stages.paper_metadata import canonical_paper_metadata
from src.stages.pdf_layout import (
    LAYOUT_EXTRACTOR_VERSION,
    install_document_query_tool,
    write_layout_blocks,
)
from src.stages.phase_gate import install_phase_gate_tool, run as run_shared_phase_gate
from src.stages.stage06_task_builder.prompts import (
    STAGE06_SYNTHESIS_PROMPT_VERSION,
    final_task_synthesis_instructions,
)


STAGE06_IMPLEMENTATION_VERSION = "v20-model-driven-input-closure"
STAGE06_DIRECTORY = "stage_06_task_construction"


def run_stage06(
    *,
    candidates,
    stage04_records,
    documents,
    stage02_records=None,
    stage03_records=None,
    paper_metadata_by_paper=None,
    config,
    model,
    workspace: Path,
    run_id: str,
):
    """Synthesize a complete reproduction-first task pair in one Agent call."""

    config = dict(config)
    paper_metadata_by_paper = dict(paper_metadata_by_paper or {})
    stage_root = workspace / STAGE06_DIRECTORY
    stage_root.mkdir(parents=True, exist_ok=True)
    stage04_by_paper = {
        str(row["paper_id"]): row for row in stage04_records if row.get("paper_id")
    }
    stage02_by_paper = {
        str(row["paper_id"]): row for row in (stage02_records or []) if row.get("paper_id")
    }
    stage03_by_paper = {
        str(row["paper_id"]): row for row in (stage03_records or []) if row.get("paper_id")
    }
    documents_by_paper: dict[str, list[dict[str, Any]]] = {}
    for document in documents:
        if document.get("decision") == "pass":
            documents_by_paper.setdefault(str(document["paper_id"]), []).append(document)
    candidates_by_paper: dict[str, list[dict[str, Any]]] = {}
    for candidate in candidates:
        candidates_by_paper.setdefault(str(candidate["paper_id"]), []).append(candidate)

    harness = create_agent_harness(
        str(config.get("harness") or "codex"),
        config=config,
        model_config=dict(getattr(model, "config", {}) or {}),
        model_client=model,
    )

    def synthesize(item: tuple[str, list[dict[str, Any]]]) -> dict[str, Any]:
        paper_id, paper_candidates = item
        candidate_id = str(paper_candidates[0].get("candidate_id") or paper_id)
        if paper_id not in stage04_by_paper:
            return _technical_block(
                run_id, paper_id, candidate_id, "stage04_record_missing",
                "The Stage04 paper record is unavailable."
            )
        paper_documents = documents_by_paper.get(paper_id, [])
        if not paper_documents:
            return _technical_block(
                run_id, paper_id, candidate_id, "source_parse_failure",
                "No parsed paper or supplementary document is available."
            )
        try:
            paper_info = _paper_info(
                paper_id,
                paper_documents,
                metadata=paper_metadata_by_paper.get(paper_id),
                paper_records=[stage02_by_paper.get(paper_id) or {}],
            )
            snapshot = _prepare_input_snapshot(
                stage_root=stage_root,
                paper_id=paper_id,
                candidates=paper_candidates,
                stage02=stage02_by_paper.get(paper_id),
                stage03=stage03_by_paper.get(paper_id),
                stage04=stage04_by_paper[paper_id],
                documents=paper_documents,
                config=config,
                run_id=run_id,
            )
            response, audit, agent_workspace = _run_synthesis_agent(
                harness=harness,
                stage_root=stage_root,
                paper_id=paper_id,
                snapshot=snapshot,
                config=config,
            )
            outputs = agent_workspace / "outputs"
            review = read_json(outputs / "workflow_review.json")
            receipt_path = outputs / "construction_receipt.json"
            receipt = read_json(receipt_path) if receipt_path.is_file() else response
            if review.get("decision") == "scientific_not_constructible" or response.get(
                "decision"
            ) == "scientific_not_constructible":
                return _publish_scientific_rejection(
                    stage_root=stage_root,
                    run_id=run_id,
                    paper_id=paper_id,
                    candidate_id=candidate_id,
                    outputs=outputs,
                    snapshot=snapshot,
                    audit=audit,
                    paper_info=paper_info,
                )

            gate_report = run_shared_phase_gate("synthesis", outputs)
            external_report = {
                **gate_report,
                "authority": "orchestrator_external_read_only",
                "created_at": now_utc(),
            }
            if gate_report.get("paper_id") != paper_id:
                external_report["status"] = "failed"
                external_report["findings"] = sorted(
                    set(external_report.get("findings") or []) | {"paper_id_mismatch"}
                )
            write_json(agent_workspace / "external_phase_gate_report.json", external_report)
            if external_report["status"] != "passed":
                _persist_agent_workspace(agent_workspace, stage_root, paper_id)
                return _technical_block(
                    run_id,
                    paper_id,
                    candidate_id,
                    "invalid_synthesis_contract",
                    "; ".join(external_report["findings"]),
                    agent_run=audit,
                    gate_report=external_report,
                )

            staging = prepare_clean_directory(
                stage_root / "staging" / safe_component(paper_id) / uuid.uuid4().hex[:10]
            )
            copytree_exact(outputs, staging)
            make_writable(staging)
            write_json(staging / "paper_info.json", paper_info)
            write_json(staging / "source_manifest.json", snapshot["source_manifest"])
            write_json(
                staging / "stage06_handoff.json",
                {
                    "paper_id": paper_id,
                    "decision": "provisional_constructed",
                    "handoff_ready": True,
                    "source_snapshot_path": str(snapshot["root"]),
                    "snapshot_hash": snapshot["snapshot_hash"],
                    "synthesis_prompt_version": STAGE06_SYNTHESIS_PROMPT_VERSION,
                    "agent_run": audit,
                    "created_at": now_utc(),
                },
            )
            write_manifest(staging, staging / "candidate_manifest.json")
            target = stage_root / "provisional_tasks" / safe_component(paper_id)
            atomic_commit_tree(staging, target)
            return {
                **record_header(run_id=run_id, stage="stage06", paper_id=paper_id),
                "candidate_id": candidate_id,
                "paper_id": paper_id,
                "processing_status": "completed",
                "decision": "provisional_constructed",
                "scientific_status": "constructed_candidate",
                "contract_status": "complete",
                "handoff_ready": True,
                "passed": False,
                "provisional": True,
                "task_pair_path": str(target),
                "handoff_path": str(target),
                "source_snapshot_path": str(snapshot["root"]),
                "gate_status": "passed",
                "gate_findings": [],
                "gate_diagnostics": gate_report["diagnostics"],
                "agent_harness": harness.name,
                "agent_model": harness.model,
                "mode_generation_strategy": "reproduction_first_same_agent",
            }
        except AgentExecutionError as exc:
            return _technical_block(
                run_id,
                paper_id,
                candidate_id,
                exc.failure_class,
                str(exc),
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
                run_id, paper_id, candidate_id, "synthesis_processing_error",
                f"{type(exc).__name__}: {exc}"
            )

    records = ordered_parallel_map(
        synthesize,
        sorted(candidates_by_paper.items()),
        max_workers=int(config.get("workers", 1)),
    )
    write_jsonl(stage_root / "build_results.jsonl", records)
    summary = {
        **record_header(run_id=run_id, stage="stage06"),
        "implementation_version": STAGE06_IMPLEMENTATION_VERSION,
        "mode_generation_strategy": "reproduction_first_same_agent",
        "papers": len(records),
        "provisional_constructed": sum(
            row.get("decision") == "provisional_constructed" for row in records
        ),
        "provisional_not_constructible": sum(
            row.get("decision") == "provisional_not_constructible" for row in records
        ),
        "technical_blocked": sum(
            row.get("decision") == "technical_blocked" for row in records
        ),
        "paper_ids": sorted(candidates_by_paper),
        "decisions": decision_counts(records),
        "agent_harness": harness.name,
        "agent_model": harness.model,
    }
    write_json(stage_root / "stage_summary.json", summary)
    return {"records": records, "summary": summary}


def _run_synthesis_agent(
    *, harness, stage_root: Path, paper_id: str, snapshot: dict[str, Any], config: dict[str, Any]
) -> tuple[dict[str, Any], dict[str, Any], Path]:
    fingerprint = input_fingerprint(
        {
            "snapshot_hash": snapshot["snapshot_hash"],
            "prompt_version": STAGE06_SYNTHESIS_PROMPT_VERSION,
            "schema": canonical_hash(STAGE06_SYNTHESIS_SCHEMA),
            "model": harness.model,
        }
    )
    workspace = prepare_clean_directory(
        stage_root
        / "workspaces"
        / safe_component(paper_id)
        / "final_task_synthesis"
        / f"attempt-01-{uuid.uuid4().hex[:8]}"
    )
    inputs = copytree_exact(snapshot["root"], workspace / "inputs")
    # Immutable snapshots retain their read-only mode through copytree. The
    # Gate is part of workspace setup, so add it to the copy before freezing
    # the complete Agent input tree again.
    make_writable(inputs)
    install_phase_gate_tool(inputs / "tools")
    install_document_query_tool(inputs / "tools")
    make_read_only(inputs)
    (workspace / "outputs").mkdir(parents=True)
    request = AgentRunRequest(
        phase="stage06_final_task_synthesis",
        record_id=paper_id,
        workspace=workspace,
        instructions=final_task_synthesis_instructions(
            paper_id=paper_id,
            snapshot_hash=snapshot["snapshot_hash"],
            max_tool_calls=int(config.get("synthesis_max_tool_calls", 180)),
        ),
        output_schema=STAGE06_SYNTHESIS_SCHEMA,
        prompt_version=STAGE06_SYNTHESIS_PROMPT_VERSION,
        timeout_seconds=int(config.get("synthesis_timeout_seconds", 5400)),
        metadata={
            "paper_id": paper_id,
            "input_fingerprint": fingerprint,
            "max_tool_calls": int(config.get("synthesis_max_tool_calls", 180)),
            "finalization_reserve": int(config.get("synthesis_finalization_reserve", 28)),
            "structured_artifact_path": "outputs/construction_receipt.json",
            "inline_contract": False,
        },
    )
    result = harness.run(request)
    response = result.response or {}
    jsonschema.validate(response, STAGE06_SYNTHESIS_SCHEMA)
    if not (workspace / "outputs" / "workflow_review.json").is_file():
        raise AgentExecutionError(
            "Synthesis Agent did not write workflow_review.json",
            failure_class="missing_agent_artifact",
            retryable=False,
            result=result,
        )
    return response, result.audit_record(), workspace


def _prepare_input_snapshot(
    *,
    stage_root: Path,
    paper_id: str,
    candidates: list[dict[str, Any]],
    stage02: dict[str, Any] | None,
    stage03: dict[str, Any] | None,
    stage04: dict[str, Any],
    documents: list[dict[str, Any]],
    config: dict[str, Any],
    run_id: str,
) -> dict[str, Any]:
    source_facts = {
        "paper_id": paper_id,
        "candidates": candidates,
        "stage02": stage02 or {},
        "stage03": stage03 or {},
        "stage04": stage04,
        "documents": [
            {
                key: row.get(key)
                for key in (
                    "document_id", "document_role", "file_name", "sha256", "source_path",
                    "normalized_markdown_path", "content_blocks_path", "title", "doi",
                    "journal_name", "publication_date",
                )
            }
            for row in documents
        ],
        "implementation_version": STAGE06_IMPLEMENTATION_VERSION,
        "prompt_version": STAGE06_SYNTHESIS_PROMPT_VERSION,
        "layout_extractor_version": LAYOUT_EXTRACTOR_VERSION,
    }
    snapshot_hash = input_fingerprint(source_facts)
    root = stage_root / "input_snapshots" / safe_component(paper_id) / snapshot_hash[:16]
    complete = root / "snapshot_complete.json"
    if complete.is_file():
        return {
            "root": root,
            "snapshot_hash": snapshot_hash,
            "source_manifest": read_json(root / "source_manifest.json"),
        }
    prepare_clean_directory(root)
    write_json(root / "upstream_hints.json", source_facts)
    evidence_index: list[dict[str, Any]] = []
    source_manifest: list[dict[str, Any]] = []
    for document in sorted(documents, key=lambda row: str(row.get("document_id") or "")):
        document_id = str(document.get("document_id") or uuid.uuid4().hex[:12])
        document_root = root / "documents" / safe_component(document_id)
        document_root.mkdir(parents=True)
        materials: list[dict[str, Any]] = []
        for key, name in (
            ("normalized_markdown_path", "document.md"),
            ("content_blocks_path", "content_blocks.jsonl"),
            ("layout_text_path", "layout_text.txt"),
            ("tables_path", "tables.json"),
        ):
            source_value = document.get(key)
            if not source_value:
                continue
            source = Path(str(source_value)).expanduser().resolve()
            if not source.is_file():
                continue
            target = document_root / name
            shutil.copy2(source, target)
            materials.append({"kind": key, "path": target.relative_to(root).as_posix()})
        source_value = document.get("source_path")
        layout_status = "unavailable"
        layout_error = ""
        if source_value:
            source = Path(str(source_value)).expanduser().resolve()
            if source.is_file() and source.suffix.casefold() == ".pdf":
                target = document_root / "source.pdf"
                shutil.copy2(source, target)
                materials.append(
                    {
                        "kind": "source_pdf",
                        "path": target.relative_to(root).as_posix(),
                        "sha256": sha256_file(target),
                    }
                )
                layout_path = document_root / "layout_blocks.jsonl"
                try:
                    block_count = write_layout_blocks(target, layout_path)
                except (OSError, RuntimeError, ValueError) as exc:
                    layout_error = f"{type(exc).__name__}: {exc}"
                else:
                    layout_status = "available" if block_count else "empty"
                    if block_count:
                        materials.append(
                            {
                                "kind": "pdf_layout_blocks",
                                "path": layout_path.relative_to(root).as_posix(),
                                "records": block_count,
                                "extractor_version": LAYOUT_EXTRACTOR_VERSION,
                            }
                        )
        blocks = document_root / "content_blocks.jsonl"
        if blocks.is_file():
            for row in read_jsonl(blocks):
                evidence_id = str(row.get("evidence_id") or row.get("block_id") or "")
                if evidence_id:
                    evidence_index.append(
                        {
                            "evidence_id": evidence_id,
                            "document_id": document_id,
                            "document_role": document.get("document_role"),
                            "page": row.get("page"),
                            "section_path": row.get("section_path") or [],
                            "text": row.get("text"),
                            "source_ref": row.get("source_ref"),
                        }
                    )
        source_manifest.append(
            {
                "document_id": document_id,
                "document_role": document.get("document_role"),
                "file_name": document.get("file_name"),
                "sha256": document.get("sha256"),
                "materials": materials,
                "layout_status": layout_status,
                "layout_error": layout_error,
            }
        )
    if not evidence_index:
        raise FileNotFoundError(f"no evidence blocks available for {paper_id}")
    write_json(root / "evidence_index.json", evidence_index)
    write_json(root / "source_manifest.json", source_manifest)
    toolbox = config.get("toolbox_capabilities")
    if toolbox and Path(str(toolbox)).expanduser().is_file():
        shutil.copy2(Path(str(toolbox)).expanduser(), root / "toolbox_capabilities.json")
    write_json(
        complete,
        {"paper_id": paper_id, "snapshot_hash": snapshot_hash, "run_id": run_id, "created_at": now_utc()},
    )
    make_read_only(root)
    return {"root": root, "snapshot_hash": snapshot_hash, "source_manifest": source_manifest}


def _paper_info(
    paper_id: str,
    documents: list[dict[str, Any]],
    *,
    metadata: dict[str, Any] | None = None,
    paper_records: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    canonical = metadata or canonical_paper_metadata(
        paper_id=paper_id,
        paper_records=paper_records or [],
        documents=documents,
    )
    return {
        **canonical,
        "documents": [
            {
                "document_id": row.get("document_id"),
                "document_type": row.get("document_role"),
                "original_filename": row.get("file_name"),
                "sha256": row.get("sha256"),
                "source_path": row.get("source_path"),
            }
            for row in documents
        ],
    }


def _publish_scientific_rejection(
    *, stage_root: Path, run_id: str, paper_id: str, candidate_id: str,
    outputs: Path, snapshot: dict[str, Any],
    audit: dict[str, Any], paper_info: dict[str, Any],
) -> dict[str, Any]:
    staging = prepare_clean_directory(
        stage_root / "staging" / safe_component(paper_id) / f"rejected-{uuid.uuid4().hex[:8]}"
    )
    copytree_exact(outputs, staging)
    make_writable(staging)
    write_json(staging / "paper_info.json", paper_info)
    target = stage_root / "provisional_rejections" / safe_component(paper_id)
    atomic_commit_tree(staging, target)
    review = read_json(target / "workflow_review.json")
    return {
        **record_header(run_id=run_id, stage="stage06", paper_id=paper_id),
        "candidate_id": candidate_id,
        "paper_id": paper_id,
        "processing_status": "completed",
        "decision": "provisional_not_constructible",
        "scientific_status": "scientific_not_constructible",
        "contract_status": "not_applicable",
        "handoff_ready": False,
        "passed": False,
        "retryable": False,
        "failure_code": review.get("failure_code"),
        "failure_reasons": review.get("failure_reasons") or [],
        "task_pair_path": str(target),
        "source_snapshot_path": str(snapshot["root"]),
        "agent_run": audit,
    }


def _persist_agent_workspace(workspace: Path, stage_root: Path, paper_id: str) -> None:
    target = stage_root / "phase_artifacts" / safe_component(paper_id) / "final_task_synthesis"
    if target.exists():
        shutil.rmtree(target)
    copytree_exact(workspace, target)


def _technical_block(
    run_id: str,
    paper_id: str,
    candidate_id: str,
    failure_class: str,
    message: str,
    *,
    agent_run: dict[str, Any] | None = None,
    gate_report: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        **record_header(run_id=run_id, stage="stage06", paper_id=paper_id),
        "candidate_id": candidate_id,
        "paper_id": paper_id,
        "processing_status": "failed",
        "decision": "technical_blocked",
        "handoff_ready": False,
        "passed": False,
        "retryable": False,
        "failure_class": failure_class,
        "error": {"error_type": failure_class, "message": message[:4000]},
        "agent_run": agent_run,
        "gate_report": gate_report or {},
    }
