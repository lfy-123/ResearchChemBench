from __future__ import annotations

import hashlib
import json
import re
import shutil
import time
import uuid
from html.parser import HTMLParser
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Callable

import jsonschema
from pypdf import PdfReader
from pypdf import __version__ as pypdf_version

from src.agents import AgentExecutionError, AgentRunRequest, create_agent_harness
from src.agents.schemas import (
    STAGE06_AUTONOMOUS_SCHEMA,
    STAGE06_AUTONOMOUS_CONVERTER_SCHEMA,
    STAGE06_HIDDEN_SCHEMA,
    STAGE06_REPRODUCTION_SCHEMA,
    STAGE06_REVIEW_SCHEMA,
    STAGE06_TASK_PAIR_BUILDER_SCHEMA,
    STAGE06_WORKFLOW_REVIEW_SCHEMA,
)
from src.agents.workspace import (
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
    sha256_file,
    validate_relative_path,
    write_manifest,
    write_text_asset,
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
from src.core.toolbox_inventory import installed_software_inventory
from src.stages.stage06_task_builder.prompts import (
    STAGE06_AUTONOMOUS_VERSION,
    STAGE06_AUTONOMOUS_CONVERTER_VERSION,
    STAGE06_HIDDEN_VERSION,
    STAGE06_REPRODUCTION_VERSION,
    STAGE06_REVIEW_VERSION,
    STAGE06_TASK_PAIR_BUILDER_VERSION,
    autonomous_instructions,
    autonomous_converter_instructions,
    hidden_reference_instructions,
    reproduction_instructions,
    review_instructions,
    task_pair_builder_instructions,
)
from src.stages.stage06_task_builder.validation import (
    evaluation_critical_failures,
    evaluation_reference_evidence,
    validate_autonomous_route_isolation,
    validate_hidden_reference,
    validate_mode_task,
    validate_scientific_review,
    validate_task_boundary_conditions,
    validate_task_pair,
    validate_task_pair_draft,
    validate_workflow_review,
    canonicalize_complexity_profile,
    canonicalize_mode_task_contract,
    anonymous_source_id,
)

STAGE06_IMPLEMENTATION_VERSION = "v9-fifth-round-closure-and-contract-20260818"
STAGE06_DIRECTORY = "stage_06_task_construction"
STAGE06_INPUT_PACKAGE_VERSION = "v2-canonical-deduplicated-inputs"


def run_stage06(
    *,
    candidates,
    stage04_records,
    documents,
    stage02_records=None,
    stage03_records=None,
    config,
    model,
    review_model=None,
    workspace: Path,
    run_id: str,
):
    """Construct benchmark pairs with the configured Stage06 generation strategy."""

    strategy = str(
        config.get("mode_generation_strategy") or "two_agent_objective_centered"
    )
    if strategy in {"single_agent", "two_agent_objective_centered"}:
        return _run_stage06_single_agent(
            candidates=candidates,
            stage04_records=stage04_records,
            documents=documents,
            stage02_records=stage02_records,
            stage03_records=stage03_records,
            config=config,
            model=model,
            workspace=workspace,
            run_id=run_id,
        )
    raise ValueError(
        "stage06.mode_generation_strategy must be single_agent; the legacy multi-phase "
        "strategies are disabled because their deterministic semantic validators can "
        "override Agent scientific decisions"
    )


def _run_stage06_single_agent(
    *,
    candidates,
    stage04_records,
    documents,
    stage02_records=None,
    stage03_records=None,
    config,
    model,
    workspace: Path,
    run_id: str,
):
    generation_strategy = str(config.get("mode_generation_strategy") or "single_agent")
    stage_root = workspace / STAGE06_DIRECTORY
    stage_root.mkdir(parents=True, exist_ok=True)
    coverage = {str(row["paper_id"]): row for row in stage04_records}
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

    model_config = dict(getattr(model, "config", {}) or {})
    harness_name = str(config.get("harness") or "codex")
    harness = create_agent_harness(
        harness_name,
        config=config,
        model_config=model_config,
        model_client=model,
    )
    converter_harness_name = str(config.get("converter_harness") or harness_name)
    converter_harness = create_agent_harness(
        converter_harness_name,
        config=config,
        model_config=model_config,
        model_client=model,
    )

    def build(item: tuple[str, list[dict[str, Any]]]) -> dict[str, Any]:
        paper_id, paper_candidates = item
        candidate_id = str(paper_candidates[0].get("candidate_id") or paper_id)
        try:
            if paper_id not in coverage:
                return _objective_failure(
                    run_id,
                    paper_id,
                    candidate_id,
                    "stage04_record_missing",
                    "The Stage04 paper record is unavailable.",
                )
            paper_documents = documents_by_paper.get(paper_id, [])
            if not paper_documents:
                return _objective_failure(
                    run_id,
                    paper_id,
                    candidate_id,
                    "source_parse_failure",
                    "No successfully parsed main-paper or supplementary document is available.",
                )
            snapshot = _prepare_input_snapshot(
                stage_root=stage_root,
                paper_id=paper_id,
                candidates=paper_candidates,
                stage02=stage02_by_paper.get(paper_id),
                stage03=stage03_by_paper.get(paper_id),
                stage04=coverage[paper_id],
                documents=paper_documents,
                config=config,
                run_id=run_id,
            )
            receipt, agent_audit, agent_workspace = _run_phase(
                harness=harness,
                stage_root=stage_root,
                paper_id=paper_id,
                phase="task_pair_builder",
                prompt_version=STAGE06_TASK_PAIR_BUILDER_VERSION,
                instructions=task_pair_builder_instructions(
                    paper_id=paper_id,
                    snapshot_hash=snapshot["snapshot_hash"],
                    max_tool_calls=int(
                        config.get(
                            "task_pair_builder_max_tool_calls",
                            config.get("max_tool_calls", 120),
                        )
                    ),
                    finalization_reserve=int(
                        config.get(
                            "task_pair_builder_finalization_reserve",
                            config.get("finalization_reserve", 12),
                        )
                    ),
                    evidence_search_max_tool_calls=int(
                        config.get("task_pair_builder_search_max_tool_calls", 72)
                    ),
                ),
                output_schema=STAGE06_TASK_PAIR_BUILDER_SCHEMA,
                fingerprint_value={
                    "snapshot_hash": snapshot["snapshot_hash"],
                    "prompt_version": STAGE06_TASK_PAIR_BUILDER_VERSION,
                    "receipt_schema": canonical_hash(STAGE06_TASK_PAIR_BUILDER_SCHEMA),
                    "workflow_schema": canonical_hash(STAGE06_WORKFLOW_REVIEW_SCHEMA),
                    "harness": harness_name,
                    "model": harness.model,
                    "preferred_scope": config.get(
                        "preferred_scope", "objective_centered_core_workflow"
                    ),
                    "minimum_complexity": config.get("minimum_complexity", "medium"),
                    "reject_trivial_single_call": config.get(
                        "reject_trivial_single_call", True
                    ),
                },
                config=config,
                setup=lambda root: _copy_phase_inputs(
                    snapshot["root"],
                    root / "inputs",
                    include_visual_fallback=bool(config.get("stage06_include_visual_fallback", False)),
                ),
            )
            if agent_workspace is None:
                raise FileNotFoundError("Stage06 task-pair builder workspace is unavailable")
            outputs = agent_workspace / "outputs"
            if receipt.get("decision") == "scientific_not_constructible":
                # A scientific rejection is allowed to stop after the receipt; it is
                # not required to emit a workflow review or any task files.  Do not
                # turn that Agent decision into a filesystem failure by reading a
                # success-only artifact first.
                review_path = outputs / "workflow_review.json"
                review = read_json(review_path) if review_path.is_file() else {}
                return _publish_provisional_not_constructible(
                    stage_root=stage_root,
                    run_id=run_id,
                    paper_id=paper_id,
                    candidate_id=candidate_id,
                    receipt=receipt,
                    review=review,
                    agent_audit=agent_audit,
                    outputs=outputs,
                    snapshot=snapshot,
                    documents=paper_documents,
                )

            review = read_json(outputs / "workflow_review.json")

            task_pair_id = str(
                review.get("task_pair_id")
                or receipt.get("task_pair_id")
                or f"{paper_id}-provisional"
            )
            staging_root = prepare_clean_directory(
                stage_root
                / "staging"
                / safe_component(paper_id)
                / f"{safe_component(task_pair_id)}-{uuid.uuid4().hex[:8]}"
            )
            copytree_exact(outputs, staging_root)
            make_writable(staging_root)
            write_json(staging_root / "workflow_review.json", review)
            write_json(staging_root / "construction_receipt.json", receipt)
            _ensure_objective_handoff_artifacts(staging_root, review)
            use_converter = generation_strategy == "two_agent_objective_centered"
            if use_converter:
                converter_response, converter_audit, converter_workspace = _run_phase(
                    harness=converter_harness,
                    stage_root=stage_root,
                    paper_id=paper_id,
                    phase="autonomous_converter",
                    prompt_version=STAGE06_AUTONOMOUS_CONVERTER_VERSION,
                    instructions=autonomous_converter_instructions(
                        paper_id=paper_id,
                        task_pair_id=task_pair_id,
                        max_tool_calls=int(
                            config.get(
                                "autonomous_converter_max_tool_calls",
                                config.get("max_tool_calls", 60),
                            )
                        ),
                    ),
                    output_schema=STAGE06_AUTONOMOUS_CONVERTER_SCHEMA,
                    fingerprint_value={
                        "task_pair_id": task_pair_id,
                        "paper_reproduction_hash": directory_manifest(
                            staging_root / "paper_reproduction"
                        )["content_hash"],
                        "objective_card_hash": canonical_hash(
                            read_json(staging_root / "objective_card.json")
                            if (staging_root / "objective_card.json").is_file()
                            else review.get("objective_card") or {}
                        ),
                        "prompt_version": STAGE06_AUTONOMOUS_CONVERTER_VERSION,
                        "harness": converter_harness_name,
                        "model": converter_harness.model,
                    },
                    config=config,
                    setup=lambda root: _setup_converter_inputs(root, staging_root),
                    semantic_validator=_converter_phase_findings,
                )
            else:
                # Explicit legacy mode remains available for old fixtures and migration runs.
                converter_response = {"status": "converted", "artifact_path": "outputs/autonomous_research"}
                converter_audit = {"status": "skipped", "reason": "legacy_single_agent_mode"}
                converter_workspace = None
            if converter_response.get("status") not in {"converted", "conversion_uncertain"}:
                return _artifact_delivery_failure(
                    run_id,
                    paper_id,
                    candidate_id,
                    "autonomous_conversion_failed",
                    str(
                        converter_response.get("summary")
                        or converter_response.get("invalid_reasons")
                        or "Stage06B did not produce an autonomous task."
                    ),
                    agent_run=converter_audit,
                )
            if use_converter:
                converted_root = converter_workspace / "outputs" / "autonomous_research"
                if not converted_root.is_dir():
                    raise FileNotFoundError("Stage06B autonomous task artifact is unavailable")
                old_autonomous_root = staging_root / "autonomous_research"
                if old_autonomous_root.exists() and converted_root != old_autonomous_root:
                    shutil.rmtree(old_autonomous_root)
                if converted_root != old_autonomous_root:
                    copytree_exact(converted_root, old_autonomous_root)
                make_writable(old_autonomous_root)
                mode_findings = canonicalize_mode_task_contract(
                    old_autonomous_root,
                    expected_mode="autonomous_research",
                    task_pair_id=task_pair_id,
                )
                if mode_findings:
                    raise ValueError(
                        "Stage06B autonomous mode contract is incomplete: "
                        + "; ".join(mode_findings)
                    )
                report_path = converter_workspace / "outputs" / "conversion_report.json"
                if report_path.is_file():
                    shutil.copy2(report_path, staging_root / "conversion_report.json")
            # Freeze the shared mechanical public contracts before Stage07 sees the pair.  This
            # does not choose a scientific workflow or alter Ground Truth; it only canonicalizes
            # the route-fidelity criterion and the identical submission path contract.
            reproduction_root = staging_root / "paper_reproduction"
            autonomous_root = staging_root / "autonomous_research"
            if reproduction_root.is_dir() and autonomous_root.is_dir():
                submission_candidates = [
                    _json_object(reproduction_root / "submission_contract.json"),
                    _json_object(autonomous_root / "submission_contract.json"),
                ]
                shared_submission = next(
                    (value for value in submission_candidates if value.get("required_files")),
                    {},
                )
                if shared_submission:
                    # The submission contract is shared by both modes.  A mode-specific task_id
                    # would make the two otherwise identical contracts disagree and is redundant
                    # because task_info/task_spec carry the canonical mode-specific IDs.
                    shared_submission.pop("task_id", None)
                    shared_submission["task_pair_id"] = task_pair_id
                    write_json(reproduction_root / "submission_contract.json", shared_submission)
                    write_json(autonomous_root / "submission_contract.json", shared_submission)
                rubric_path = reproduction_root / "process_rubric.json"
                if rubric_path.is_file():
                    rubric = _ensure_reproduction_route_rubric(
                        read_json(rubric_path), submission=shared_submission
                    )
                    write_json(rubric_path, rubric)
            requirements_path = outputs / "toolbox_requirements.json"
            requirements = (
                read_json(requirements_path)
                if requirements_path.is_file()
                else review.get("toolbox_requirements") or []
            )
            review["toolbox_requirements"] = _normalize_toolbox_requirements(
                requirements if isinstance(requirements, list) else []
            )
            if isinstance(review.get("complexity_profile"), dict):
                review["complexity_profile"] = canonicalize_complexity_profile(
                    review["complexity_profile"]
                )
            autonomous_root = staging_root / "autonomous_research"
            reproduction_root = staging_root / "paper_reproduction"
            handoff_warnings: list[str] = []
            hidden_path = staging_root / "hidden_reference" / "ground_truth_common.json"
            if reproduction_root.is_dir() and autonomous_root.is_dir() and hidden_path.is_file():
                try:
                    for mode_root, expected_mode in (
                        (reproduction_root, "paper_reproduction"),
                        (autonomous_root, "autonomous_research"),
                    ):
                        mode_findings = canonicalize_mode_task_contract(
                            mode_root,
                            expected_mode=expected_mode,
                            task_pair_id=task_pair_id,
                        )
                        if mode_findings:
                            raise ValueError(
                                f"{expected_mode} mode contract is incomplete: "
                                + "; ".join(mode_findings)
                            )
                    _write_mode_public_manifest(reproduction_root)
                    _write_mode_public_manifest(autonomous_root)
                    _materialize_pair_metadata(
                        staging_root,
                        paper_id=paper_id,
                        task_pair_id=task_pair_id,
                        documents=paper_documents,
                        stage04=coverage[paper_id],
                        candidates=paper_candidates,
                        review=review,
                        hidden=read_json(hidden_path),
                        evidence_index=snapshot["evidence_index"],
                        snapshot=snapshot,
                        autonomous_root=autonomous_root,
                        reproduction_root=reproduction_root,
                        construction_harness=harness,
                        review_harness=harness,
                        phase_audits={
                            "task_pair_builder": agent_audit,
                            **(
                                {"autonomous_converter": converter_audit}
                                if use_converter
                                else {}
                            ),
                        },
                        mode_generation_order=["paper_reproduction", "autonomous_research"],
                        mode_generation_strategy=generation_strategy,
                    )
                except (
                    AttributeError,
                    KeyError,
                    TypeError,
                    ValueError,
                    json.JSONDecodeError,
                ) as exc:
                    # Content drift belongs to the Stage07 audit-repair Agent.  Preserve the
                    # candidate instead of turning a repairable task into a Stage06 rejection.
                    handoff_warnings.append(
                        f"metadata_materialization_deferred:{type(exc).__name__}:{exc}"
                    )
            else:
                handoff_warnings.append("candidate_task_tree_incomplete_stage07_review_required")
            _write_provisional_handoff_metadata(
                staging_root,
                paper_id=paper_id,
                task_pair_id=task_pair_id,
                decision="provisional_constructed",
                documents=paper_documents,
                candidates=paper_candidates,
                review=review,
                receipt=receipt,
                snapshot=snapshot,
                agent_audit=agent_audit,
                handoff_warnings=handoff_warnings,
            )
            write_manifest(staging_root, staging_root / "task_pair_manifest.json")
            target = stage_root / "provisional_tasks" / safe_component(paper_id)
            atomic_commit_tree(staging_root, target)
            scope = review.get("workflow_scope") or {}
            complexity = review.get("complexity_profile") or {}
            toolbox_gap = any(
                _toolbox_requirement_status(row) in {"missing", "unknown", "incompatible"}
                for row in review.get("toolbox_requirements") or []
            )
            return {
                **record_header(run_id=run_id, stage="stage06", paper_id=paper_id),
                "candidate_id": str(review.get("selected_candidate_id") or candidate_id),
                "input_candidate_ids": [
                    str(row.get("candidate_id") or "") for row in paper_candidates
                ],
                "task_pair_id": task_pair_id,
                "processing_status": "completed",
                "decision": "provisional_constructed",
                "handoff_ready": True,
                "passed": False,
                "provisional": True,
                "scientifically_ready": False,
                "task_pair_path": str(target),
                "handoff_path": str(target),
                "source_snapshot_path": str(snapshot["root"]),
                "workflow_scope_kind": scope.get("kind"),
                "complexity_level": complexity.get("level"),
                "toolbox_gap_present": toolbox_gap,
                "resource_risk_present": _resource_risk_present(
                    review.get("resource_assessment") or {}
                ),
                "stage05_candidate_disposition": review.get(
                    "stage05_candidate_disposition"
                ),
                "stage05_candidate_replaced": str(
                    review.get("stage05_candidate_disposition") or ""
                ).casefold()
                in {"replaced", "corrected", "ignored"},
                "handoff_warnings": handoff_warnings,
                "agent_harness": harness.name,
                "agent_model": harness.model,
                "mode_generation_strategy": generation_strategy,
                "converter_harness": converter_harness.name,
                "converter_model": converter_harness.model,
            }
        except AgentExecutionError as exc:
            if exc.failure_class in {"partial_agent_artifact", "missing_agent_artifact"}:
                return _artifact_delivery_failure(
                    run_id,
                    paper_id,
                    candidate_id,
                    exc.failure_class,
                    str(exc),
                    agent_run=exc.result.audit_record() if exc.result else None,
                )
            return _objective_failure(
                run_id,
                paper_id,
                candidate_id,
                exc.failure_class,
                str(exc),
                agent_run=exc.result.audit_record() if exc.result else None,
                retryable=exc.retryable,
            )
        except (FileNotFoundError, OSError) as exc:
            return _objective_failure(
                run_id,
                paper_id,
                candidate_id,
                "source_or_workspace_failure",
                f"{type(exc).__name__}: {exc}",
            )
        except Exception as exc:
            return _objective_failure(
                run_id,
                paper_id,
                candidate_id,
                "stage06_processing_error",
                f"{type(exc).__name__}: {exc}",
            )

    records = ordered_parallel_map(
        build,
        sorted(candidates_by_paper.items()),
        max_workers=int(config.get("workers", 1)),
    )
    write_jsonl(stage_root / "build_results.jsonl", records)
    summary = {
        **record_header(run_id=run_id, stage="stage06"),
        "implementation_version": STAGE06_IMPLEMENTATION_VERSION,
        "mode_generation_strategy": generation_strategy,
        "papers": len(records),
        "provisional_constructed": sum(
            row.get("decision") == "provisional_constructed" for row in records
        ),
        "provisional_not_constructible": sum(
            row.get("decision") == "provisional_not_constructible" for row in records
        ),
        "retryable_failures": sum(
            row.get("decision") == "objective_failure_retryable" for row in records
        ),
        "artifact_delivery_failures": sum(
            row.get("decision") == "artifact_delivery_failure_retryable"
            for row in records
        ),
        "toolbox_gaps": sum(bool(row.get("toolbox_gap_present")) for row in records),
        "paper_ids": sorted({str(row.get("paper_id")) for row in records if row.get("paper_id")}),
        "decisions": decision_counts(records),
        "agent_harness": harness.name,
        "agent_model": harness.model,
    }
    write_json(stage_root / "stage_summary.json", summary)
    return {"records": records, "summary": summary}


def _run_stage06_legacy(
    *,
    candidates,
    stage04_records,
    documents,
    stage02_records=None,
    stage03_records=None,
    config,
    model,
    review_model=None,
    workspace: Path,
    run_id: str,
):
    """Construct one isolated two-mode benchmark task per eligible paper."""

    stage_root = workspace / STAGE06_DIRECTORY
    stage_root.mkdir(parents=True, exist_ok=True)
    coverage = {str(row["paper_id"]): row for row in stage04_records}
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

    review_model = review_model or model
    model_config = dict(getattr(model, "config", {}) or {})
    review_model_config = dict(getattr(review_model, "config", {}) or {})
    harness_name = str(config.get("harness") or "codex")
    construction_harness = create_agent_harness(
        harness_name,
        config=config,
        model_config=model_config,
        model_client=model,
    )
    review_harness = create_agent_harness(
        harness_name,
        config=config,
        model_config=review_model_config,
        model_client=review_model,
    )

    def build(item: tuple[str, list[dict[str, Any]]]) -> dict[str, Any]:
        paper_id, paper_candidates = item
        candidate_id = str(paper_candidates[0].get("candidate_id") or paper_id)
        try:
            if paper_id not in coverage:
                return _objective_failure(
                    run_id,
                    paper_id,
                    candidate_id,
                    "stage04_record_missing",
                    "The Stage04 paper record is unavailable.",
                )
            paper_documents = documents_by_paper.get(paper_id, [])
            if not paper_documents:
                return _objective_failure(
                    run_id,
                    paper_id,
                    candidate_id,
                    "source_parse_failure",
                    "No successfully parsed main-paper or supplementary document is available.",
                )
            snapshot = _prepare_input_snapshot(
                stage_root=stage_root,
                paper_id=paper_id,
                candidates=paper_candidates,
                stage02=stage02_by_paper.get(paper_id),
                stage03=stage03_by_paper.get(paper_id),
                stage04=coverage[paper_id],
                documents=paper_documents,
                config=config,
                run_id=run_id,
            )
            evidence_ids = set(snapshot["evidence_by_id"])

            review_receipt, review_audit, review_workspace = _run_phase(
                harness=review_harness,
                stage_root=stage_root,
                paper_id=paper_id,
                phase="scientific_review",
                prompt_version=STAGE06_REVIEW_VERSION,
                instructions=review_instructions(
                    paper_id=paper_id,
                    snapshot_hash=snapshot["snapshot_hash"],
                    max_tool_calls=int(
                        config.get(
                            "scientific_review_max_tool_calls",
                            config.get("max_tool_calls", 32),
                        )
                    ),
                    finalization_reserve=int(
                        config.get(
                            "scientific_review_finalization_reserve",
                            config.get("finalization_reserve", 8),
                        )
                    ),
                ),
                output_schema=STAGE06_REVIEW_SCHEMA,
                fingerprint_value={
                    "snapshot_hash": snapshot["snapshot_hash"],
                    "prompt_version": STAGE06_REVIEW_VERSION,
                    "harness": harness_name,
                    "model": review_harness.model,
                },
                config=config,
                setup=lambda root: _copy_phase_inputs(
                    snapshot["root"],
                    root / "inputs",
                    include_visual_fallback=bool(config.get("stage06_include_visual_fallback", False)),
                ),
                semantic_validator=lambda response, root: _scientific_review_phase_findings(
                    response, root, evidence_ids
                ),
            )
            review_response = _load_phase_json_artifact(
                review_receipt,
                review_workspace,
                fallback=review_receipt,
            )
            _hydrate_public_input_assets(review_response, review_workspace)
            review_findings = validate_scientific_review(review_response, evidence_ids)
            if review_response.get("decision") == "scientific_reject":
                reasons = list(review_response.get("reject_reasons") or [])
                return _scientific_reject(
                    run_id=run_id,
                    paper_id=paper_id,
                    candidate_id=candidate_id,
                    task_pair_id=str(review_response.get("task_pair_id") or ""),
                    reasons=sorted(set(reasons or ["scientific_workflow_not_constructible"])),
                    review_audit=review_audit,
                    stage05_disposition=review_response.get("stage05_candidate_disposition"),
                )
            if review_findings:
                return _construction_invalid(
                    run_id,
                    paper_id,
                    candidate_id,
                    str(review_response.get("task_pair_id") or "") or None,
                    review_findings,
                    {"review": review_audit},
                )

            task_pair_id = str(review_response["task_pair_id"])
            staging_root = prepare_clean_directory(
                stage_root
                / "staging"
                / safe_component(paper_id)
                / f"{safe_component(task_pair_id)}-{uuid.uuid4().hex[:8]}"
            )
            public_basis = _public_basis(review_response, paper_id, task_pair_id, config)
            autonomous_response, autonomous_audit, autonomous_workspace = _run_phase(
                harness=construction_harness,
                stage_root=stage_root,
                paper_id=paper_id,
                phase="autonomous_task",
                prompt_version=STAGE06_AUTONOMOUS_VERSION,
                instructions=autonomous_instructions(task_pair_id=task_pair_id),
                output_schema=STAGE06_AUTONOMOUS_SCHEMA,
                fingerprint_value={
                    "public_basis": public_basis,
                    "prompt_version": STAGE06_AUTONOMOUS_VERSION,
                    "harness": harness_name,
                    "model": construction_harness.model,
                },
                config=config,
                setup=lambda root: _setup_autonomous_inputs(
                    root,
                    public_basis=public_basis,
                    toolbox_snapshot=snapshot["toolbox_snapshot"],
                    task_pair_id=task_pair_id,
                ),
                semantic_validator=lambda response, root: (
                    _autonomous_phase_findings(
                        root,
                        public_basis=public_basis,
                        review=review_response,
                    )
                    if response.get("artifact_path")
                    else []
                ),
            )
            if autonomous_response.get("status") != "ready":
                return _construction_invalid(
                    run_id,
                    paper_id,
                    candidate_id,
                    task_pair_id,
                    autonomous_response.get("invalid_reasons") or ["autonomous_builder_invalid"],
                    {"review": review_audit, "autonomous": autonomous_audit},
                )
            autonomous_root = staging_root / "autonomous_research"
            _materialize_autonomous(
                autonomous_root,
                autonomous_response,
                public_basis=public_basis,
                paper_id=paper_id,
                task_pair_id=task_pair_id,
                agent_workspace=autonomous_workspace,
            )
            autonomous_findings = validate_mode_task(
                autonomous_root, expected_mode="autonomous_research"
            )
            autonomous_findings.extend(
                validate_task_boundary_conditions(
                    autonomous_root,
                    expected_conditions=public_basis.get("boundary_conditions"),
                )
            )
            autonomous_findings.extend(
                validate_autonomous_route_isolation(
                    autonomous_root,
                    paper_route=review_response.get("paper_route") or {},
                    allowed_boundary_conditions=public_basis.get("boundary_conditions"),
                )
            )
            if autonomous_findings:
                return _construction_invalid(
                    run_id,
                    paper_id,
                    candidate_id,
                    task_pair_id,
                    autonomous_findings,
                    {"review": review_audit, "autonomous": autonomous_audit},
                )

            reproduction_root = staging_root / "paper_reproduction"
            copytree_exact(autonomous_root, reproduction_root)
            base_manifest = directory_manifest(reproduction_root)
            reproduction_response, reproduction_audit, reproduction_workspace = _run_phase(
                harness=construction_harness,
                stage_root=stage_root,
                paper_id=paper_id,
                phase="paper_reproduction",
                prompt_version=STAGE06_REPRODUCTION_VERSION,
                instructions=reproduction_instructions(
                    task_pair_id=task_pair_id,
                    base_manifest_hash=base_manifest["content_hash"],
                ),
                output_schema=STAGE06_REPRODUCTION_SCHEMA,
                fingerprint_value={
                    "base_manifest_hash": base_manifest["content_hash"],
                    "paper_route": review_response.get("paper_route"),
                    "prompt_version": STAGE06_REPRODUCTION_VERSION,
                    "harness": harness_name,
                    "model": construction_harness.model,
                },
                config=config,
                setup=lambda root: _setup_reproduction_inputs(
                    root,
                    autonomous_root=autonomous_root,
                    review=review_response,
                    base_manifest=base_manifest,
                ),
                semantic_validator=lambda response, root: (
                    _reproduction_phase_findings(
                        root,
                        autonomous_root=autonomous_root,
                        review=review_response,
                    )
                    if response.get("artifact_path")
                    else []
                ),
            )
            if reproduction_response.get("status") != "ready":
                return _construction_invalid(
                    run_id,
                    paper_id,
                    candidate_id,
                    task_pair_id,
                    reproduction_response.get("invalid_reasons")
                    or ["reproduction_builder_invalid"],
                    {
                        "review": review_audit,
                        "autonomous": autonomous_audit,
                        "reproduction": reproduction_audit,
                    },
                )
            _materialize_reproduction(
                reproduction_root,
                reproduction_response,
                autonomous_root=autonomous_root,
                paper_id=paper_id,
                task_pair_id=task_pair_id,
                base_manifest_hash=base_manifest["content_hash"],
                agent_workspace=reproduction_workspace,
            )
            reproduction_findings = validate_mode_task(
                reproduction_root, expected_mode="paper_reproduction"
            )
            reproduction_findings.extend(
                _reproduction_copy_findings(
                    autonomous_root,
                    reproduction_root,
                    reproduction_response.get("modified_files") or [],
                )
            )
            if reproduction_findings:
                return _construction_invalid(
                    run_id,
                    paper_id,
                    candidate_id,
                    task_pair_id,
                    sorted(set(reproduction_findings)),
                    {
                        "review": review_audit,
                        "autonomous": autonomous_audit,
                        "reproduction": reproduction_audit,
                    },
                )

            submission_contract = read_json(autonomous_root / "submission_contract.json")
            hidden_receipt, hidden_audit, hidden_workspace = _run_phase(
                harness=construction_harness,
                stage_root=stage_root,
                paper_id=paper_id,
                phase="hidden_reference",
                prompt_version=STAGE06_HIDDEN_VERSION,
                instructions=hidden_reference_instructions(task_pair_id=task_pair_id),
                output_schema=STAGE06_HIDDEN_SCHEMA,
                fingerprint_value={
                    "review_hash": canonical_hash(review_response),
                    "autonomous_hash": directory_manifest(autonomous_root)["content_hash"],
                    "reproduction_hash": directory_manifest(reproduction_root)["content_hash"],
                    "prompt_version": STAGE06_HIDDEN_VERSION,
                    "harness": harness_name,
                    "model": construction_harness.model,
                },
                config=config,
                setup=lambda root: _setup_hidden_inputs(
                    root,
                    review=review_response,
                    autonomous_root=autonomous_root,
                    reproduction_root=reproduction_root,
                    evidence_index=snapshot["evidence_index"],
                ),
                semantic_validator=lambda response, root: _hidden_reference_phase_findings(
                    response,
                    root,
                    review=review_response,
                    submission_contract=submission_contract,
                ),
            )
            hidden_response = _load_phase_json_artifact(
                hidden_receipt,
                hidden_workspace,
                fallback=hidden_receipt,
            )
            hidden_findings = validate_hidden_reference(
                hidden_response,
                expected_ground_truth_items=review_response.get("ground_truth_items") or [],
                submission_contract=submission_contract,
            )
            if hidden_response.get("status") != "ready" or hidden_findings:
                reasons = list(hidden_response.get("invalid_reasons") or [])
                reasons.extend(hidden_findings)
                return _construction_invalid(
                    run_id,
                    paper_id,
                    candidate_id,
                    task_pair_id,
                    sorted(set(reasons)),
                    {
                        "review": review_audit,
                        "autonomous": autonomous_audit,
                        "reproduction": reproduction_audit,
                        "hidden_reference": hidden_audit,
                    },
                )

            _materialize_pair_metadata(
                staging_root,
                paper_id=paper_id,
                task_pair_id=task_pair_id,
                documents=paper_documents,
                stage04=coverage[paper_id],
                candidates=paper_candidates,
                review=review_response,
                hidden=hidden_response,
                evidence_index=snapshot["evidence_index"],
                snapshot=snapshot,
                autonomous_root=autonomous_root,
                reproduction_root=reproduction_root,
                construction_harness=construction_harness,
                review_harness=review_harness,
                phase_audits={
                    "review": review_audit,
                    "autonomous": autonomous_audit,
                    "reproduction": reproduction_audit,
                    "hidden_reference": hidden_audit,
                },
            )
            pair_audit = validate_task_pair(staging_root)
            write_json(staging_root / "construction_validation.json", pair_audit)
            write_manifest(staging_root, staging_root / "task_pair_manifest.json")
            if not pair_audit["passed"]:
                return _construction_invalid(
                    run_id,
                    paper_id,
                    candidate_id,
                    task_pair_id,
                    pair_audit["findings"],
                    {
                        "review": review_audit,
                        "autonomous": autonomous_audit,
                        "reproduction": reproduction_audit,
                        "hidden_reference": hidden_audit,
                    },
                )

            target = stage_root / "tasks" / safe_component(paper_id)
            atomic_commit_tree(staging_root, target)
            toolbox_gap = any(
                _toolbox_requirement_status(row) in {"missing", "unknown", "incompatible"}
                for row in review_response.get("toolbox_requirements") or []
            )
            return {
                **record_header(run_id=run_id, stage="stage06", paper_id=paper_id),
                "candidate_id": str(review_response.get("selected_candidate_id") or candidate_id),
                "input_candidate_ids": [
                    str(row.get("candidate_id") or "") for row in paper_candidates
                ],
                "task_pair_id": task_pair_id,
                "processing_status": "completed",
                "decision": "constructed",
                "passed": True,
                "task_pair_path": str(target),
                "toolbox_gap_present": toolbox_gap,
                "stage05_candidate_disposition": review_response.get(
                    "stage05_candidate_disposition"
                ),
                "deterministic_audit": pair_audit,
                "agent_harness": construction_harness.name,
                "agent_model": construction_harness.model,
                "scientific_review_agent_model": review_harness.model,
            }
        except AgentExecutionError as exc:
            result = exc.result.audit_record() if exc.result else None
            return _objective_failure(
                run_id,
                paper_id,
                candidate_id,
                exc.failure_class,
                str(exc),
                task_pair_id=None,
                agent_run=result,
                retryable=exc.retryable,
            )
        except (FileNotFoundError, OSError) as exc:
            return _objective_failure(
                run_id,
                paper_id,
                candidate_id,
                "source_or_workspace_failure",
                f"{type(exc).__name__}: {exc}",
            )
        except Exception as exc:
            return _construction_invalid(
                run_id,
                paper_id,
                candidate_id,
                None,
                [f"{type(exc).__name__}: {exc}"],
                {},
            )

    records = ordered_parallel_map(
        build,
        sorted(candidates_by_paper.items()),
        max_workers=int(config.get("workers", 1)),
    )
    write_jsonl(stage_root / "build_results.jsonl", records)
    summary = {
        **record_header(run_id=run_id, stage="stage06"),
        "implementation_version": STAGE06_IMPLEMENTATION_VERSION,
        "papers": len(records),
        "constructed": sum(row.get("decision") == "constructed" for row in records),
        "scientific_rejects": sum(row.get("decision") == "scientific_reject" for row in records),
        "retryable_failures": sum(
            row.get("decision") == "objective_failure_retryable" for row in records
        ),
        "invalid_constructions": sum(
            row.get("decision") == "construction_invalid" for row in records
        ),
        "toolbox_gaps": sum(bool(row.get("toolbox_gap_present")) for row in records),
        "decisions": decision_counts(records),
        "agent_harness": construction_harness.name,
        "agent_model": construction_harness.model,
        "scientific_review_agent_model": review_harness.model,
    }
    write_json(stage_root / "stage_summary.json", summary)
    return {"records": records, "summary": summary}


def deterministic_builder_audit(*args):
    """Compatibility wrapper for callers that previously audited three API objects."""

    if len(args) == 1 and isinstance(args[0], (str, Path)):
        return validate_task_pair(Path(args[0]))
    if len(args) == 3:
        shared, autonomous, reproduction = args
        findings: list[str] = []
        if autonomous.get("mode") != "autonomous" or reproduction.get("mode") != "reproduction":
            findings.append("mode_mismatch")
        if not shared.get("hidden_reference"):
            findings.append("missing_private_reference")
        return {"passed": not findings, "findings": findings}
    raise TypeError("deterministic_builder_audit expects a task path or three legacy records")


def _source_coverage_manifest(
    *, root: Path, source_manifest: list[dict[str, Any]]
) -> dict[str, Any]:
    documents: list[dict[str, Any]] = []
    for document in source_manifest:
        document_id = str(document.get("document_id") or "")
        document_root = root / "documents" / safe_component(document_id)
        materials = document.get("materials") or []
        kinds = {str(row.get("kind") or "") for row in materials if isinstance(row, dict)}
        table_coverage_path = document_root / "derived_tables" / "coverage.json"
        table_coverage = (
            read_json(table_coverage_path) if table_coverage_path.is_file() else {}
        )
        row = {
            "document_id": document_id,
            "document_role": document.get("document_role"),
            "source_pdf_available": "source_pdf" in kinds,
            "normalized_markdown_available": "normalized_markdown_path" in kinds,
            "content_blocks_available": "content_blocks_path" in kinds,
            "layout_fallback_available": bool(
                {"layout_text_path", "pypdf_layout_path", "pypdf_layout_text"} & kinds
            ),
            "parser_structured_available": any(
                kind
                in {
                    "content_list_v2_path",
                    "content_list_path",
                    "middle_json_path",
                    "model_json_path",
                }
                for kind in kinds
            ),
            "table_coverage": table_coverage,
            "coordinate_index_available": (
                document_root / "derived_coordinates" / "index.json"
            ).is_file(),
        }
        row["coverage_status"] = (
            "complete"
            if row["normalized_markdown_available"]
            and row["content_blocks_available"]
            and (row["source_pdf_available"] or row["layout_fallback_available"])
            and table_coverage.get("coverage_status") != "failed"
            else "partial"
        )
        documents.append(row)
    main_documents = [
        row for row in documents if str(row.get("document_role") or "") == "main_paper"
    ]
    return {
        "coverage_status": (
            "complete"
            if documents
            and main_documents
            and all(row.get("coverage_status") == "complete" for row in documents)
            else "partial"
        ),
        "known_document_count": len(documents),
        "main_document_count": len(main_documents),
        "supplementary_document_count": sum(
            str(row.get("document_role") or "") != "main_paper" for row in documents
        ),
        "documents": documents,
    }


def _write_stage06_helper_scripts(root: Path) -> None:
    root.mkdir(parents=True, exist_ok=True)
    scripts = {
        "validate_workflow_review.py": _WORKFLOW_REVIEW_VALIDATOR_SCRIPT,
        "bootstrap_task_pair.py": _TASK_PAIR_BOOTSTRAP_SCRIPT,
        "validate_reproduction.py": _REPRODUCTION_VALIDATOR_SCRIPT,
        "copy_reproduction_to_autonomous.py": _REPRODUCTION_COPY_SCRIPT,
        "validate_task_pair_draft.py": _TASK_PAIR_DRAFT_VALIDATOR_SCRIPT,
    }
    for name, content in scripts.items():
        path = root / name
        path.write_text(content.strip() + "\n", encoding="utf-8")
        path.chmod(0o555)


_TASK_PAIR_BOOTSTRAP_SCRIPT = Path(__file__).with_name(
    "bootstrap_task_pair.py"
).read_text(encoding="utf-8")


_WORKFLOW_REVIEW_VALIDATOR_SCRIPT = r'''#!/usr/bin/env python3
import json
import sys
from pathlib import Path

path = Path(sys.argv[1] if len(sys.argv) > 1 else "outputs/workflow_review.json")
value = json.loads(path.read_text(encoding="utf-8"))
required = {
    "decision", "task_pair_id", "paper_workflow_inventory_complete",
    "full_paper_workflow_checked", "alternative_scope_search_complete",
    "workflow_inventory", "workflow_scope", "complexity_profile", "evidence_map",
    "toolbox_requirements", "resource_assessment", "failure_code", "failure_reasons",
}
missing = sorted(required - set(value))
if missing:
    raise SystemExit("missing workflow review fields: " + ", ".join(missing))
if value["decision"] not in {"candidate_ready", "scientific_not_constructible"}:
    raise SystemExit("invalid workflow review decision")
for field in (
    "paper_workflow_inventory_complete", "full_paper_workflow_checked",
    "alternative_scope_search_complete",
):
    if value[field] is not True:
        raise SystemExit(field + " must be true before finalization")
print("workflow review shape: OK")
'''


_REPRODUCTION_VALIDATOR_SCRIPT = r'''#!/usr/bin/env python3
import json
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else "outputs/paper_reproduction")
if root.name == "outputs" and (root / "paper_reproduction").is_dir():
    root = root / "paper_reproduction"
required = {
    "task.md", "task_info.json", "task_spec.json", "submission_contract.json",
    "process_rubric.json", "paper_route.md", "workflow_spec.json",
    "route_evidence_map.json",
}
missing = sorted(name for name in required if not (root / name).is_file())
if missing:
    raise SystemExit("missing reproduction files: " + ", ".join(missing))
if not (root / "data" / "inputs").is_dir():
    raise SystemExit("missing reproduction data/inputs directory")
info = json.loads((root / "task_info.json").read_text(encoding="utf-8"))
spec = json.loads((root / "task_spec.json").read_text(encoding="utf-8"))
for value, label in ((info, "task_info"), (spec, "task_spec")):
    if value.get("mode") != "paper_reproduction":
        raise SystemExit(label + " mode must be paper_reproduction")
    if not value.get("workflow_scope") or not value.get("complexity_profile"):
        raise SystemExit(label + " lacks workflow_scope or complexity_profile")
print("paper reproduction shape: OK")
'''


_REPRODUCTION_COPY_SCRIPT = r'''#!/usr/bin/env python3
import hashlib
import json
import shutil
import sys
from pathlib import Path

source = Path(sys.argv[1] if len(sys.argv) > 1 else "outputs/paper_reproduction").resolve()
target = Path(sys.argv[2] if len(sys.argv) > 2 else "outputs/autonomous_research").resolve()
if source.name == "outputs" and (source / "paper_reproduction").is_dir():
    # Accept the common Agent shorthand `copy_reproduction_to_autonomous.py outputs`.
    target = source / "autonomous_research"
    source = source / "paper_reproduction"
workspace = Path.cwd().resolve()
for path in (source, target):
    if workspace != path and workspace not in path.parents:
        raise SystemExit("task directory escapes the workspace")
required = {
    "task.md", "task_info.json", "task_spec.json", "submission_contract.json",
    "process_rubric.json", "paper_route.md", "workflow_spec.json",
    "route_evidence_map.json",
}
missing = sorted(name for name in required if not (source / name).is_file())
if missing or not (source / "data" / "inputs").is_dir():
    raise SystemExit("reproduction is incomplete: " + ", ".join(missing))

def manifest(root):
    rows = []
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        relative = path.relative_to(root).as_posix()
        if relative == "public_manifest.json":
            continue
        rows.append({"path": relative, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    payload = json.dumps(rows, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    return rows, hashlib.sha256(payload).hexdigest()

rows, base_hash = manifest(source)
(source / "public_manifest.json").write_text(
    json.dumps({"files": rows, "content_hash": base_hash}, ensure_ascii=False, indent=2) + "\n",
    encoding="utf-8",
)
if target.exists():
    shutil.rmtree(target)
shutil.copytree(source, target)
for name in ("paper_route.md", "workflow_spec.json", "route_evidence_map.json", "public_manifest.json"):
    (target / name).unlink(missing_ok=True)
for name in ("conversion_contract.json", "conversion_receipt.json", "derived_from.json", "conversion_manifest.json"):
    (target / name).unlink(missing_ok=True)
editable = {"process_rubric.json", "task.md", "task_info.json", "task_spec.json"}
for path in target.rglob("*"):
    if path.is_file() and path.relative_to(target).as_posix() not in editable:
        path.chmod(0o444)
print(base_hash)
'''


_TASK_PAIR_DRAFT_VALIDATOR_SCRIPT = r'''#!/usr/bin/env python3
import hashlib
import json
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else "outputs")
reproduction = root / "paper_reproduction"
autonomous = root / "autonomous_research"
hidden = root / "hidden_reference" / "ground_truth_common.json"
required_public = {
    "task.md", "task_info.json", "task_spec.json", "submission_contract.json",
    "process_rubric.json",
}
for mode_root in (reproduction, autonomous):
    missing = sorted(name for name in required_public if not (mode_root / name).is_file())
    if missing:
        raise SystemExit(mode_root.name + " missing: " + ", ".join(missing))
if not hidden.is_file():
    raise SystemExit("hidden_reference/ground_truth_common.json is missing")
for name in ("paper_route.md", "workflow_spec.json", "route_evidence_map.json"):
    if (autonomous / name).exists():
        raise SystemExit("autonomous route file remains: " + name)
if (reproduction / "submission_contract.json").read_bytes() != (
    autonomous / "submission_contract.json"
).read_bytes():
    raise SystemExit("submission contracts differ")

def tree_hash(path):
    rows = []
    for item in sorted(entry for entry in path.rglob("*") if entry.is_file()):
        rows.append((item.relative_to(path).as_posix(), hashlib.sha256(item.read_bytes()).hexdigest()))
    return hashlib.sha256(json.dumps(rows, separators=(",", ":")).encode()).hexdigest()

if tree_hash(reproduction / "data") != tree_hash(autonomous / "data"):
    raise SystemExit("public inputs differ")
print("task pair draft shape: OK")
'''


def _public_builder_packet(shared, mode):
    """Legacy helper retained as an explicit hidden-reference exclusion test."""

    return {
        "mode": mode,
        "task_pair_id": shared.get("task_pair_id"),
        "scientific_record": shared.get("scientific_record"),
        "required_assets": shared.get("required_assets"),
        "allowed_backends": shared.get("allowed_backends"),
        "allowed_actions": shared.get("allowed_actions"),
        "budget": shared.get("budget"),
    }


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
        "candidate_hash": canonical_hash(candidates),
        "stage02_hash": canonical_hash(stage02 or {}),
        "stage03_hash": canonical_hash(stage03 or {}),
        "stage04_hash": canonical_hash(stage04),
        "documents": [
            {
                "document_id": row.get("document_id"),
                "sha256": row.get("sha256"),
                "normalized_markdown_path": row.get("normalized_markdown_path"),
                "content_blocks_path": row.get("content_blocks_path"),
                "normalized_markdown_sha256": _optional_file_hash(
                    row.get("normalized_markdown_path")
                ),
                "content_blocks_sha256": _optional_file_hash(row.get("content_blocks_path")),
                "source_pdf_sha256": _optional_file_hash(row.get("source_path")),
            }
            for row in documents
        ],
        "toolbox_path": config.get("toolbox_capabilities"),
        "toolbox_sha256": _optional_file_hash(config.get("toolbox_capabilities")),
        "resource_policy": config.get("resource_policy") or stage04.get("resource_profile") or {},
        "implementation_version": STAGE06_IMPLEMENTATION_VERSION,
        "input_package_version": STAGE06_INPUT_PACKAGE_VERSION,
        "builder_prompt_version": STAGE06_TASK_PAIR_BUILDER_VERSION,
        "builder_schema_hash": canonical_hash(STAGE06_TASK_PAIR_BUILDER_SCHEMA),
        "workflow_review_schema_hash": canonical_hash(STAGE06_WORKFLOW_REVIEW_SCHEMA),
        "helper_scripts_hash": canonical_hash(
            {
                "workflow_review": _WORKFLOW_REVIEW_VALIDATOR_SCRIPT,
                "bootstrap": _TASK_PAIR_BOOTSTRAP_SCRIPT,
                "reproduction": _REPRODUCTION_VALIDATOR_SCRIPT,
                "copy": _REPRODUCTION_COPY_SCRIPT,
                "pair": _TASK_PAIR_DRAFT_VALIDATOR_SCRIPT,
            }
        ),
    }
    snapshot_hash = input_fingerprint(source_facts)
    root = stage_root / "input_snapshots" / safe_component(paper_id) / snapshot_hash[:16]
    complete = root / "snapshot_complete.json"
    if complete.is_file():
        metadata = read_json(complete)
        if (
            metadata.get("snapshot_hash") == snapshot_hash
            and (root / "upstream_hints.json").is_file()
            and (root / "dedup_report.json").is_file()
        ):
            evidence_index = read_json(root / "evidence_index.json")
            return {
                "root": root,
                "snapshot_hash": snapshot_hash,
                "evidence_index": evidence_index,
                "evidence_by_id": {
                    row["evidence_id"]: row for row in evidence_index if row.get("evidence_id")
                },
                "toolbox_snapshot": read_json(root / "toolbox_snapshot.json"),
                "source_manifest": read_json(root / "source_manifest.json"),
                "source_facts": read_json(root / "source_facts.json"),
            }
    prepare_clean_directory(root)
    write_json(root / "source_facts.json", source_facts)
    write_json(
        root / "upstream_hints.json",
        _upstream_hints(
            paper_id=paper_id,
            candidates=candidates,
            stage02=stage02,
            stage03=stage03,
            stage04=stage04,
        ),
    )
    write_json(root / "stage04_record.json", stage04)
    write_json(root / "resource_policy.json", source_facts["resource_policy"])
    write_json(
        root / "task_contract.json",
        {
            "schema_version": "stage06-objective-centered-two-agent/v1",
            "receipt_schema": STAGE06_TASK_PAIR_BUILDER_SCHEMA,
            "workflow_review_schema": STAGE06_WORKFLOW_REVIEW_SCHEMA,
            "workflow_review_normalization": {
                "accepted_aliases": {
                    "workflow_scope.scope_kind": "workflow_scope.kind",
                    "workflow_scope.included_workflows": "workflow_scope.included_workflow_ids",
                    "workflow_scope.included_claims": "workflow_scope.included_claim_ids",
                    "complexity_profile.core_computation_count": "complexity_profile.scientific_core_operation_count",
                    "complexity_profile.tool_call_count": "complexity_profile.estimated_typical_tool_calls",
                    "complexity_profile.dependency_count": "complexity_profile.dependency_edge_count",
                    "workflow_steps[].output_artifact": "workflow_steps[].output_artifacts",
                    "ground_truth_items[].item_id": "ground_truth_items[].ground_truth_id",
                    "ground_truth_items[].value": "ground_truth_items[].canonical_answer",
                },
                "scientific_fields_never_invented": [
                    "public_task_basis.input_assets",
                    "public_task_basis.boundary_conditions",
                    "paper_route.closed_fields",
                    "ground_truth_items",
                ],
            },
            "mode_generation_order": ["paper_reproduction", "autonomous_research"],
            "objective_contract": {
                "files": ["objective_card.json", "key_points.json", "conversion_manifest.json"],
                "selection": "objective_first",
                "scientific_decision_authority": "stage06_agent_and_stage07_agent",
            },
            "bootstrap_script": "inputs/scripts/bootstrap_task_pair.py",
            "bootstrap_usage": (
                "After candidate_ready workflow_review.json, run the bootstrap script once. "
                "It creates a syntax-complete draft from the review and copies only source-provided "
                "public input content; replace marked prose and validate before writing the receipt."
            ),
            "autonomous_editable_files": "recursive_autonomous_public_surface",
            "shared_across_modes": [
                "data/inputs",
                "submission_contract.json",
                "workflow_scope",
                "complexity_profile",
                "scientific_question",
                "target_definition",
                "input_assets",
                "boundary_conditions",
                "required_deliverables",
            ],
        },
    )
    toolbox_snapshot = installed_software_inventory(
        _load_toolbox_snapshot(config, stage04)
    )
    write_json(root / "toolbox_snapshot.json", toolbox_snapshot)
    evidence_index: list[dict[str, Any]] = []
    source_manifest: list[dict[str, Any]] = []
    for document in sorted(documents, key=lambda row: str(row.get("document_id") or "")):
        document_id = str(document["document_id"])
        document_root = root / "documents" / safe_component(document_id)
        document_root.mkdir(parents=True, exist_ok=True)
        parser_metadata = _parser_metadata(document)
        write_json(
            document_root / "source_metadata.json",
            _paper_document_metadata(document, parser_metadata=parser_metadata),
        )
        copied = []
        source_value = document.get("source_path")
        if source_value:
            source_pdf = Path(str(source_value)).expanduser().resolve()
            if source_pdf.is_file() and source_pdf.suffix.casefold() == ".pdf":
                role = str(document.get("document_role") or "").casefold()
                if role == "main_paper" and not (root / "main_paper.pdf").exists():
                    source_target = root / "main_paper.pdf"
                else:
                    source_target = root / "supplementary" / f"{safe_component(document_id)}.pdf"
                    source_target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(source_pdf, source_target)
                copied.append(
                    {
                        "kind": "source_pdf",
                        "path": str(source_target.relative_to(root)),
                        "sha256": sha256_file(source_target),
                    }
                )
        for key, target_name in (
            ("normalized_markdown_path", "normalized_document.md"),
            ("content_blocks_path", "content_blocks.jsonl"),
            ("layout_text_path", "layout_text.txt"),
            ("pypdf_layout_path", "pypdf_layout.txt"),
            ("tables_path", "tables.json"),
        ):
            source_value = document.get(key)
            if not source_value:
                continue
            source = Path(str(source_value)).expanduser().resolve()
            if not source.is_file():
                if key in {"normalized_markdown_path", "content_blocks_path"}:
                    raise FileNotFoundError(f"Stage04 document material is missing: {source}")
                continue
            target = document_root / target_name
            shutil.copy2(source, target)
            copied.append({"kind": key, "path": str(target.relative_to(root))})
        copied.extend(
            _copy_parser_materials(
                parser_metadata=parser_metadata,
                document_root=document_root,
                snapshot_root=root,
            )
        )
        layout_evidence, layout_materials = _extract_pdf_layout_materials(
            document=document,
            document_root=document_root,
            snapshot_root=root,
            document_id=document_id,
            document_role=document.get("document_role"),
        )
        evidence_index.extend(layout_evidence)
        copied.extend(layout_materials)
        blocks_path = document_root / "content_blocks.jsonl"
        if not blocks_path.is_file():
            raise FileNotFoundError(f"content blocks missing for document {document_id}")
        document_blocks = read_jsonl(blocks_path)
        for block in document_blocks:
            evidence_id = str(block.get("evidence_id") or block.get("block_id") or "")
            if not evidence_id:
                continue
            evidence_index.append(
                {
                    "evidence_id": evidence_id,
                    "document_id": document_id,
                    "document_role": document.get("document_role"),
                    "page": block.get("page"),
                    "section_path": block.get("section_path") or [],
                    "block_type": block.get("block_type"),
                    "text": block.get("text"),
                    "source_ref": block.get("source_ref"),
                }
            )
        derived_tables = _extract_markdown_tables(
            markdown_path=document_root / "normalized_document.md",
            document_root=document_root,
            snapshot_root=root,
            document_id=document_id,
            document_role=document.get("document_role"),
            canonical_blocks=document_blocks,
        )
        evidence_index.extend(derived_tables)
        table_coverage_path = document_root / "derived_tables" / "coverage.json"
        if table_coverage_path.is_file():
            copied.append(
                {
                    "kind": "derived_table_coverage",
                    "path": str((document_root / "derived_tables").relative_to(root)),
                    "count": len(derived_tables),
                    "coverage_status": read_json(table_coverage_path).get("coverage_status"),
                }
            )
        source_manifest.append(
            {
                "document_id": document_id,
                "document_role": document.get("document_role"),
                "file_name": document.get("file_name"),
                "sha256": document.get("sha256"),
                "source_remote_uri": document.get("source_remote_uri"),
                "materials": copied,
            }
        )
    if not evidence_index:
        raise FileNotFoundError(f"no evidence blocks resolved for {paper_id}")
    write_json(root / "evidence_index.json", evidence_index)
    write_json(
        root / "priority_review_packet.json",
        _priority_review_packet(
            candidates=candidates,
            stage02=stage02,
            stage03=stage03,
            evidence_index=evidence_index,
        ),
    )
    _write_dedup_report(root)
    write_json(root / "source_manifest.json", source_manifest)
    write_json(
        root / "coverage_manifest.json",
        _source_coverage_manifest(root=root, source_manifest=source_manifest),
    )
    _write_stage06_helper_scripts(root / "scripts")
    manifest = write_manifest(root)
    write_json(
        complete,
        {
            "snapshot_hash": snapshot_hash,
            "created_at": now_utc(),
            "run_id": run_id,
            "manifest_hash": manifest["content_hash"],
        },
    )
    make_read_only(root)
    return {
        "root": root,
        "snapshot_hash": snapshot_hash,
        "evidence_index": evidence_index,
        "evidence_by_id": {
            row["evidence_id"]: row for row in evidence_index if row.get("evidence_id")
        },
        "toolbox_snapshot": toolbox_snapshot,
        "source_manifest": source_manifest,
        "source_facts": source_facts,
    }


def _run_phase(
    *,
    harness,
    stage_root: Path,
    paper_id: str,
    phase: str,
    prompt_version: str,
    instructions: str,
    output_schema: dict[str, Any],
    fingerprint_value: Any,
    config: dict[str, Any],
    setup: Callable[[Path], None],
    semantic_validator: Callable[[dict[str, Any], Path], list[str]] | None = None,
) -> tuple[dict[str, Any], dict[str, Any], Path | None]:
    fingerprint = input_fingerprint(fingerprint_value)
    artifact_root = (
        stage_root
        / "phase_artifacts"
        / safe_component(paper_id)
        / safe_component(phase)
        / fingerprint[:16]
    )
    checkpoint = (
        stage_root / "checkpoints" / safe_component(paper_id) / f"{safe_component(phase)}.json"
    )
    failure_checkpoint = checkpoint.with_suffix(".failure.json")
    cached_recovery_context: str | None = None
    cached_recovery_workspace: Path | None = None
    if bool(config.get("resume", True)) and checkpoint.is_file():
        cached = read_json(checkpoint)
        if cached.get("input_fingerprint") == fingerprint:
            response = cached.get("response")
            jsonschema.validate(response, output_schema)
            cached_workspace = artifact_root if artifact_root.is_dir() else None
            semantic_findings = (
                semantic_validator(response, cached_workspace)
                if semantic_validator is not None and cached_workspace is not None
                else []
            )
            invalid_claimed_artifact = bool(
                response.get("status") == "invalid" and response.get("artifact_path")
            )
            if (
                not semantic_findings
                and not invalid_claimed_artifact
                and (
                    not response.get("artifact_path")
                    or artifact_root.is_dir()
                    or _receipt_is_terminal_negative(response)
                )
            ):
                return (
                    response,
                    {**(cached.get("agent_run") or {}), "cache_hit": True},
                    artifact_root if artifact_root.is_dir() else None,
                )
            if semantic_findings:
                cached_recovery_context = (
                    "# Previous Agent Attempt\n\n"
                    "The cached phase artifact has a valid JSON shape but fails the current "
                    "deterministic semantic contract. Treat it as a revision draft.\n\n"
                    "Failure class: invalid_phase_contract\n\n"
                    "## Validation failure to repair\n\n"
                    + "\n".join(f"- {finding}" for finding in semantic_findings[:80])
                    + "\n"
                )
                cached_recovery_workspace = (
                    artifact_root if artifact_root.is_dir() else None
                )

    attempts = max(1, int(config.get("max_attempts", 3)))
    last_error: AgentExecutionError | None = None
    recovery_context = cached_recovery_context
    recovery_workspace = cached_recovery_workspace
    if (
        bool(config.get("resume", True))
        and recovery_context is None
        and failure_checkpoint.is_file()
    ):
        failed = read_json(failure_checkpoint)
        if failed.get("input_fingerprint") == fingerprint:
            saved_context = str(failed.get("recovery_context") or "").strip() or None
            audit = failed.get("agent_run")
            regenerated_context = (
                agent_recovery_context(SimpleNamespace(**audit))
                if isinstance(audit, dict)
                else None
            )
            saved_has_validation = bool(
                saved_context and "## Validation failure to repair" in saved_context
            )
            regenerated_has_validation = bool(
                regenerated_context
                and "## Validation failure to repair" in regenerated_context
            )
            recovery_context = (
                saved_context
                if saved_has_validation and not regenerated_has_validation
                else regenerated_context or saved_context
            )
            recovery_workspace = artifact_root if artifact_root.is_dir() else None
    if (
        bool(config.get("resume", True))
        and recovery_context is None
        and phase == "scientific_review"
    ):
        interrupted = _interrupted_scientific_review_recovery(
            stage_root=stage_root,
            paper_id=paper_id,
            snapshot_hash=str((fingerprint_value or {}).get("snapshot_hash") or ""),
        )
        if interrupted is not None:
            recovery_context, recovery_workspace = interrupted
    if bool(config.get("resume", True)) and recovery_context is None:
        interrupted = _interrupted_phase_artifact_recovery(
            stage_root=stage_root,
            paper_id=paper_id,
            phase=phase,
            input_fingerprint_value=fingerprint,
        )
        if interrupted is not None:
            recovery_context, recovery_workspace = interrupted
    for attempt in range(1, attempts + 1):
        attempt_root = prepare_clean_directory(
            stage_root
            / "workspaces"
            / safe_component(paper_id)
            / safe_component(phase)
            / f"attempt-{attempt:02d}-{uuid.uuid4().hex[:8]}"
        )
        setup(attempt_root)
        # Every Stage06/07 Agent receives an explicit writable artifact root.  Some
        # harnesses expose only the isolated workspace and a model can otherwise
        # mask a failed shell redirection such as `cat > outputs/receipt.json` with
        # a trailing successful command.  Creating the directory in the orchestrator
        # makes file-first contracts deterministic across Codex, Claude, and
        # OpenCode adapters.
        (attempt_root / "outputs").mkdir(parents=True, exist_ok=True)
        write_json(
            attempt_root / "phase_state.json",
            {
                "phase": phase,
                "paper_id": paper_id,
                "input_fingerprint": fingerprint,
                "prompt_version": prompt_version,
            },
        )
        phase_instructions = instructions
        if recovery_context:
            (attempt_root / "RECOVERY_CONTEXT.md").write_text(
                recovery_context, encoding="utf-8"
            )
            copy_recovery_artifacts(
                recovery_workspace,
                attempt_root,
                include_evidence_trace=phase == "scientific_review",
            )
            if phase == "task_pair_builder":
                _prepare_task_pair_builder_recovery(attempt_root)
        prior_review_findings: list[str] | None = None
        if phase == "scientific_review" and recovery_context:
            prior_review_findings = _seed_prior_scientific_review_draft(
                stage_root=stage_root,
                paper_id=paper_id,
                checkpoint=checkpoint,
                attempt_root=attempt_root,
                output_schema=output_schema,
                semantic_validator=semantic_validator,
            )
        if prior_review_findings is not None:
            phase_instructions += (
                "\n\nA complete review contract from an earlier contract version has been "
                "staged at `outputs/scientific_review.json` together with its public input "
                "assets. Treat it only as a revision draft, never as source evidence. Inspect "
                "that file first, repair the current deterministic findings listed in "
                "`PRIOR_REVIEW_DRAFT_STATUS.json`, recheck the changed fields against canonical "
                "evidence, and atomically rewrite the same file so its fingerprint changes. "
                "Do not rebuild the contract from scratch or repeat broad document searches."
            )
        phase_tool_calls = int(
            config.get(
                f"{phase}_max_tool_calls",
                config.get("max_tool_calls", 24),
            )
        )
        if recovery_context:
            phase_tool_calls = int(
                config.get(
                    f"{phase}_recovery_max_tool_calls",
                    config.get("recovery_max_tool_calls", 160),
                )
            )
            phase_instructions += recovery_instructions(
                phase, max_tool_calls=phase_tool_calls
            )
            if phase == "task_pair_builder":
                phase_instructions += (
                    "\n\nTASK-PAIR RECOVERY RULE: read TASK_PAIR_RECOVERY_STATUS.json and the existing "
                    "workflow_review.json. If its decision is candidate_ready, keep that scientific "
                    "decision unless canonical evidence directly disproves it. Missing task files, "
                    "bad IDs, stale receipts, or schema/validation findings are construction-repair "
                    "work, not scientific rejection. Preserve any already refined reproduction files. "
                    "Run bootstrap_task_pair.py only when the reproduction scaffold is absent; otherwise "
                    "repair the listed fields in one grouped command. If reproduction is complete and "
                    "autonomous_research is missing, run copy_reproduction_to_autonomous.py and then "
                    "rewrite the recursive autonomous public surface through Stage06B. Only write scientific_not_constructible "
                    "when the source evidence itself proves a required input, route, or scoreable "
                    "claim cannot be recovered.\n"
                )
        artifact_receipt_metadata: dict[str, Any] = {}
        if phase == "autonomous_task":
            artifact_receipt_metadata = {
                "artifact_receipt_path": "task",
                "artifact_required_files": [
                    "task.md",
                    "task_info.json",
                    "task_spec.json",
                    "submission_contract.json",
                    "process_rubric.json",
                ],
                "artifact_receipt": {
                    "status": "ready",
                    "summary": (
                        "Recovered from a complete file-first task artifact after the "
                        "CLI final receipt could not be parsed."
                    ),
                    "invalid_reasons": [],
                },
            }
        elif phase == "paper_reproduction":
            artifact_receipt_metadata = {
                "artifact_receipt_path": "task",
                "artifact_required_files": [
                    "task.md",
                    "task_info.json",
                    "task_spec.json",
                    "submission_contract.json",
                    "process_rubric.json",
                    "paper_route.md",
                    "workflow_spec.json",
                    "route_evidence_map.json",
                ],
                "artifact_required_modified_files": [
                    "task.md",
                    "task_info.json",
                    "task_spec.json",
                    "process_rubric.json",
                ],
                "artifact_receipt": {
                    "status": "ready",
                    "modified_files": sorted(
                        _REPRODUCTION_ALLOWED_DIFFERENCES
                        - {"derived_from.json", "public_manifest.json"}
                    ),
                    "route_disclosure_summary": (
                        "Recovered from a complete file-first reproduction artifact after "
                        "the CLI final receipt could not be parsed."
                    ),
                    "invalid_reasons": [],
                },
            }
        finalization_reserve_key = (
            f"{phase}_recovery_finalization_reserve"
            if recovery_context
            else f"{phase}_finalization_reserve"
        )
        phase_finalization_reserve = int(
            config.get(
                finalization_reserve_key,
                config.get(
                    f"{phase}_finalization_reserve",
                    config.get("finalization_reserve", 4),
                ),
            )
        )
        phase_finalization_reserve = max(
            0, min(phase_finalization_reserve, max(0, phase_tool_calls - 1))
        )
        request = AgentRunRequest(
            phase=f"stage06_{phase}",
            record_id=paper_id,
            workspace=attempt_root,
            instructions=phase_instructions,
            output_schema=output_schema,
            prompt_version=prompt_version,
            timeout_seconds=int(
                config.get(
                    f"{phase}_timeout_seconds",
                    config.get("timeout_seconds", 3600),
                )
            ),
            metadata={
                "paper_id": paper_id,
                "input_fingerprint": fingerprint,
                "max_tool_calls": phase_tool_calls,
                "finalization_reserve": phase_finalization_reserve,
                # Protocol policies are optional phase overrides.  When absent,
                # the harness resolves them from models.builder (or its model
                # fallback), keeping gateway quirks out of business logic.
                "tool_choice_policy": config.get(f"{phase}_tool_choice_policy"),
                "response_format_policy": config.get(f"{phase}_response_format_policy"),
                "codex_wire_api": config.get(f"{phase}_codex_wire_api"),
                "inline_contract": False,
                "structured_artifact_path": {
                    "scientific_review": "outputs/scientific_review.json",
                    "hidden_reference": "outputs/ground_truth_common.json",
                    "task_pair_builder": "outputs/construction_receipt.json",
                }.get(phase),
                "recovery_attempt": bool(recovery_context),
                **artifact_receipt_metadata,
            },
        )
        try:
            result = harness.run(request)
            if phase == "scientific_review":
                result.response = _materialize_scientific_review_response(
                    result.response or {}, attempt_root
                )
            elif phase == "hidden_reference":
                result.response = _materialize_hidden_response(
                    result.response or {}, attempt_root
                )
            elif phase in {"autonomous_task", "paper_reproduction"}:
                result.response = _reconcile_task_phase_receipt(
                    result.response or {},
                    workspace=attempt_root,
                    phase=phase,
                    result=result,
                )
            if semantic_validator is not None:
                semantic_findings = semantic_validator(result.response or {}, attempt_root)
                if semantic_findings:
                    message = (
                        f"Agent {phase} contract failed semantic validation: "
                        + ", ".join(semantic_findings)
                    )
                    result.status = "failed"
                    result.failure_class = "invalid_phase_contract"
                    result.retryable = True
                    result.error = {
                        "error_type": "InvalidPhaseContract",
                        "message": message[:4000],
                    }
                    write_json(attempt_root / "agent_run.json", result.audit_record())
                    raise AgentExecutionError(
                        message,
                        failure_class="invalid_phase_contract",
                        retryable=True,
                        result=result,
                    )
            _require_claimed_phase_artifact(result.response or {}, attempt_root, result)
        except AgentExecutionError as exc:
            recovered_response = (
                _recover_builder_receipt_from_review(
                    workspace=attempt_root,
                    output_schema=output_schema,
                    semantic_validator=semantic_validator,
                )
                if phase == "task_pair_builder"
                and exc.failure_class == "invalid_agent_output"
                else None
            )
            if recovered_response is not None and exc.result is not None:
                result = exc.result
                result.status = "succeeded"
                result.response = recovered_response
                result.failure_class = None
                result.retryable = False
                result.error = None
                result.receipt_recovered_from_artifact = True
                write_json(attempt_root / "agent_run.json", result.audit_record())
                _persist_phase_artifacts(attempt_root, artifact_root)
                write_json(
                    checkpoint,
                    {
                        "phase": phase,
                        "paper_id": paper_id,
                        "input_fingerprint": fingerprint,
                        "prompt_version": prompt_version,
                        "response": recovered_response,
                        "agent_run": result.audit_record(),
                        "completed_at": now_utc(),
                    },
                )
                failure_checkpoint.unlink(missing_ok=True)
                return (
                    recovered_response,
                    {**result.audit_record(), "cache_hit": False},
                    artifact_root if artifact_root.is_dir() else attempt_root,
                )
            last_error = exc
            _persist_phase_artifacts(attempt_root, artifact_root)
            latest_context = agent_recovery_context(exc.result)
            if exc.failure_class == "invalid_phase_contract" or recovery_context is None:
                recovery_context = latest_context
            if not exc.retryable or attempt >= attempts:
                write_json(
                    failure_checkpoint,
                    {
                        "phase": phase,
                        "paper_id": paper_id,
                        "input_fingerprint": fingerprint,
                        "prompt_version": prompt_version,
                        "failure_class": exc.failure_class,
                        "retryable": exc.retryable,
                        "recovery_context": recovery_context,
                        "agent_run": exc.result.audit_record() if exc.result else None,
                        "failed_at": now_utc(),
                    },
                )
                raise
            failed_workspace = (
                Path(exc.result.workspace)
                if exc.result and exc.result.workspace
                else None
            )
            recovery_workspace = (
                failed_workspace
                if failed_workspace is not None and failed_workspace.is_dir()
                else artifact_root
                if artifact_root.is_dir()
                else None
            )
            delay = min(
                float(config.get("retry_max_seconds", 30)),
                float(config.get("retry_backoff_seconds", 2)) * (2 ** (attempt - 1)),
            )
            if delay > 0:
                time.sleep(delay)
            continue
        _persist_phase_artifacts(attempt_root, artifact_root)
        write_json(
            checkpoint,
            {
                "phase": phase,
                "paper_id": paper_id,
                "input_fingerprint": fingerprint,
                "prompt_version": prompt_version,
                "response": result.response,
                "agent_run": result.audit_record(),
                "completed_at": now_utc(),
            },
        )
        failure_checkpoint.unlink(missing_ok=True)
        return (
            result.response or {},
            {**result.audit_record(), "cache_hit": False},
            artifact_root if artifact_root.is_dir() else attempt_root,
        )
    if last_error is not None:
        raise last_error
    raise RuntimeError(f"Stage06 phase did not execute: {phase}")


def _recover_builder_receipt_from_review(
    *,
    workspace: Path,
    output_schema: dict[str, Any],
    semantic_validator: Callable[[dict[str, Any], Path], list[str]] | None,
) -> dict[str, Any] | None:
    """Recover a derivative receipt when the Agent's final message is malformed.

    The workflow review remains the authority for this small transport receipt.
    When a semantic validator is supplied (legacy phases), it must accept the
    artifact.  The provisional single-Agent path deliberately performs only the
    JSON/artifact recovery here and leaves scientific review to Stage07.
    """

    review_path = workspace / "outputs" / "workflow_review.json"
    if not review_path.is_file():
        return None
    try:
        review = read_json(review_path)
    except (OSError, ValueError, TypeError):
        return None
    decision = str(review.get("decision") or "")
    if decision not in {"candidate_ready", "scientific_not_constructible"}:
        return None
    receipt: dict[str, Any] = {
        "decision": (
            "constructed"
            if decision == "candidate_ready"
            else "scientific_not_constructible"
        ),
        "task_pair_id": str(review.get("task_pair_id") or ""),
        "artifact_path": (
            "outputs"
            if decision == "candidate_ready"
            else "outputs/construction_receipt.json"
        ),
        "milestones": {},
        "workflow_scope_kind": str(
            (review.get("workflow_scope") or {}).get("kind") or "none"
        ),
        "complexity_level": str(
            (review.get("complexity_profile") or {}).get("level") or "not_assessed"
        ),
        "failure_code": str(review.get("failure_code") or ""),
        "failure_reasons": review.get("failure_reasons") or [],
        "summary": str(
            review.get("workflow_summary")
            or review.get("scientific_question")
            or "Recovered the construction receipt from validated file artifacts."
        ),
    }
    write_json(workspace / "outputs" / "construction_receipt.json", receipt)
    if semantic_validator is not None:
        findings = semantic_validator(receipt, workspace)
        if findings:
            return None
    try:
        jsonschema.validate(receipt, output_schema)
    except jsonschema.ValidationError:
        return None
    return receipt


def _task_pair_builder_phase_findings(
    receipt: dict[str, Any],
    workspace: Path,
    *,
    evidence_ids: set[str],
    source_root: Path | None = None,
) -> list[str]:
    outputs = workspace / "outputs"
    make_writable(outputs)
    review_path = outputs / "workflow_review.json"
    if not review_path.is_file():
        return ["workflow_review_artifact_missing"]
    try:
        review = read_json(review_path)
    except (OSError, ValueError, TypeError) as exc:
        return [f"workflow_review_unreadable:{type(exc).__name__}:{exc}"]
    frozen_review_path = workspace / "inputs" / "frozen_workflow_review.json"
    if frozen_review_path.is_file():
        # Recovery attempts may repair construction files, but they may not
        # rewrite an already validated scientific selection or hidden targets.
        review = read_json(frozen_review_path)
    review = _normalize_workflow_review_aliases(review)
    review = _normalize_scientific_failure_contract(review)
    review = _canonicalize_review_evidence_ids(review, evidence_ids)
    canonical_source_root = (
        source_root
        if source_root is not None
        else workspace / "inputs"
    )
    evidence_index_path = canonical_source_root / "evidence_index.json"
    evidence_index = (
        read_json(evidence_index_path) if evidence_index_path.is_file() else []
    )
    review = _recover_workflow_review_from_pair_artifacts(
        review,
        outputs,
        source_root=canonical_source_root,
        evidence_index=evidence_index if isinstance(evidence_index, list) else [],
    )
    review = _normalize_workflow_review_aliases(review)
    review = _normalize_scientific_failure_contract(review)
    review = _canonicalize_review_evidence_ids(review, evidence_ids)
    review["toolbox_requirements"] = _normalize_toolbox_requirements(
        review.get("toolbox_requirements") or []
    )
    try:
        jsonschema.validate(review, STAGE06_WORKFLOW_REVIEW_SCHEMA)
    except jsonschema.ValidationError as exc:
        write_json(review_path, review)
        return [f"workflow_review_schema_invalid:{type(exc).__name__}:{exc}"]
    write_json(review_path, review)
    validation_review = json.loads(json.dumps(review, ensure_ascii=False))
    _hydrate_public_input_assets(validation_review, workspace)
    review_findings = validate_workflow_review(validation_review, evidence_ids)
    findings = list(review_findings)
    _synchronize_builder_receipt(receipt, review, outputs=outputs)
    write_json(outputs / "construction_receipt.json", receipt)
    if receipt.get("task_pair_id") != review.get("task_pair_id"):
        findings.append("receipt_task_pair_id_mismatch")
    expected_receipt_decision = (
        "constructed"
        if review.get("decision") == "candidate_ready"
        else "scientific_not_constructible"
    )
    if receipt.get("decision") != expected_receipt_decision:
        findings.append("receipt_workflow_decision_mismatch")
    if review.get("decision") == "scientific_not_constructible":
        if receipt.get("failure_code") != review.get("failure_code"):
            findings.append("receipt_failure_code_mismatch")
        if receipt.get("failure_reasons") != review.get("failure_reasons"):
            findings.append("receipt_failure_reasons_mismatch")
        if any((outputs / name).exists() for name in ("paper_reproduction", "autonomous_research")):
            findings.append("scientific_failure_created_task_directory")
        milestones = receipt.get("milestones") or {}
        if milestones.get("workflow_review_validated") is not True:
            findings.append("builder_milestone_incomplete:workflow_review_validated")
        for name in (
            "reproduction_validated",
            "autonomous_copy_created",
            "autonomous_validated",
            "hidden_reference_validated",
            "pair_draft_validated",
        ):
            if milestones.get(name) is True:
                findings.append(f"scientific_failure_milestone_unexpected:{name}")
        return sorted(set(findings))

    # Only freeze and repair the task pair after the source-backed scientific
    # review itself is valid.  This prevents a formatter from turning missing
    # structures, parameters, routes, or Ground Truth into a false success.
    if not review_findings:
        frozen_output_path = outputs / "frozen_workflow_review.json"
        if not frozen_output_path.is_file():
            write_json(frozen_output_path, review)
        findings.extend(_normalize_task_pair_artifact_contracts(outputs, review))

    if receipt.get("artifact_path") != "outputs":
        findings.append("constructed_receipt_artifact_path_invalid")
    milestones = receipt.get("milestones") or {}
    for name in (
        "workflow_review_validated",
        "reproduction_validated",
        "autonomous_copy_created",
        "autonomous_validated",
        "hidden_reference_validated",
        "pair_draft_validated",
    ):
        if milestones.get(name) is not True:
            findings.append(f"builder_milestone_incomplete:{name}")
    scope = review.get("workflow_scope") or {}
    complexity = review.get("complexity_profile") or {}
    if receipt.get("workflow_scope_kind") != scope.get("kind"):
        findings.append("receipt_workflow_scope_mismatch")
    if receipt.get("complexity_level") != complexity.get("level"):
        findings.append("receipt_complexity_level_mismatch")
    required_paths = (
        "paper_reproduction",
        "autonomous_research",
        "hidden_reference/ground_truth_common.json",
        "hidden_reference/acceptance_profiles.json",
        "hidden_reference/conclusion_rubric.json",
        "hidden_reference/private_evidence_map.json",
        "toolbox_requirements.json",
    )
    for relative in required_paths:
        if not (outputs / relative).exists():
            findings.append(f"builder_output_missing:{relative}")
    hidden_common_path = outputs / "hidden_reference" / "ground_truth_common.json"
    acceptance_path = outputs / "hidden_reference" / "acceptance_profiles.json"
    rubric_path = outputs / "hidden_reference" / "conclusion_rubric.json"
    if hidden_common_path.is_file():
        hidden = read_json(hidden_common_path)
        if acceptance_path.is_file() and read_json(acceptance_path) != hidden.get(
            "acceptance_profiles"
        ):
            findings.append("hidden_acceptance_profiles_file_mismatch")
        if rubric_path.is_file() and read_json(rubric_path) != hidden.get(
            "scientific_conclusion_rubric"
        ):
            findings.append("hidden_conclusion_rubric_file_mismatch")
    toolbox_path = outputs / "toolbox_requirements.json"
    if toolbox_path.is_file():
        toolbox_value = read_json(toolbox_path)
        if not isinstance(toolbox_value, list):
            findings.append("toolbox_requirements_artifact_invalid")
        elif _normalize_toolbox_requirements(toolbox_value) != _normalize_toolbox_requirements(
            review.get("toolbox_requirements") or []
        ):
            findings.append("toolbox_requirements_artifact_mismatch")
    if (outputs / "paper_reproduction").is_dir() and (
        outputs / "autonomous_research"
    ).is_dir():
        findings.extend(validate_task_pair_draft(outputs, review=review))
    return sorted(set(findings))


def _prepare_task_pair_builder_recovery(attempt_root: Path) -> None:
    """Make a partial builder artifact safe and unambiguous for the next attempt."""

    outputs = attempt_root / "outputs"
    outputs.mkdir(parents=True, exist_ok=True)
    make_writable(outputs)
    review_path = outputs / "workflow_review.json"
    if not review_path.is_file():
        return
    frozen_output = outputs / "frozen_workflow_review.json"
    try:
        review = _normalize_workflow_review_aliases(
            read_json(frozen_output if frozen_output.is_file() else review_path)
        )
    except (OSError, ValueError, TypeError):
        return
    write_json(review_path, review)
    if frozen_output.is_file():
        frozen_input = attempt_root / "inputs" / "frozen_workflow_review.json"
        make_writable(frozen_input.parent)
        write_json(frozen_input, review)
        make_read_only(frozen_input.parent)
    # A receipt from the previous attempt describes a tree that is about to be
    # repaired. Keeping it makes the semantic validator compare stale milestones
    # with the new tree and encourages the Agent to turn an execution failure into
    # a false scientific rejection.
    stale_receipt = outputs / "construction_receipt.json"
    if stale_receipt.is_file() and review.get("decision") == "candidate_ready":
        stale_receipt.unlink()
    write_json(
        attempt_root / "TASK_PAIR_RECOVERY_STATUS.json",
        {
            "review_decision": review.get("decision"),
            "task_pair_id": review.get("task_pair_id"),
            "frozen_review_hash": (
                canonical_hash(review) if frozen_output.is_file() else None
            ),
            "required_action": (
                "For candidate_ready, run inputs/scripts/bootstrap_task_pair.py, repair only "
                "the listed construction findings, run all validators, and write a fresh "
                "construction_receipt.json. Never change candidate_ready to scientific failure "
                "because a prior Agent stopped early."
            ),
        },
    )


_SCIENTIFIC_FAILURE_CODE_ALIASES = {
    "missing_input": "missing_core_input",
    "missing_inputs": "missing_core_input",
    "missing_input_asset": "missing_core_input",
    "missing_input_assets": "missing_core_input",
    "missing_essential_input_assets": "missing_core_input",
    "missing_required_input_assets": "missing_core_input",
    "incomplete_workflow": "incomplete_computational_process",
    "workflow_incomplete": "incomplete_computational_process",
    "missing_results": "missing_ground_truth",
    "missing_scoreable_result": "missing_ground_truth",
    "insufficient_source_evidence": "source_evidence_insufficient",
    "trivial_task": "benchmark_not_challenging",
}


def _normalize_scientific_failure_contract(review: dict[str, Any]) -> dict[str, Any]:
    """Normalize naming variants in a source-backed scientific rejection.

    Construction/runtime failures deliberately have no aliases here: they must
    remain retryable orchestration failures rather than being laundered into a
    paper-level scientific rejection.
    """

    value = json.loads(json.dumps(review, ensure_ascii=False))
    if value.get("decision") != "scientific_not_constructible":
        return value
    failure_code = str(value.get("failure_code") or "").strip()
    value["failure_code"] = _SCIENTIFIC_FAILURE_CODE_ALIASES.get(
        failure_code, failure_code
    )
    normalized_reasons: list[Any] = []
    for raw in value.get("failure_reasons") or []:
        if not isinstance(raw, dict):
            normalized_reasons.append(raw)
            continue
        reason = dict(raw)
        code = str(reason.get("code") or "").strip()
        reason["code"] = _SCIENTIFIC_FAILURE_CODE_ALIASES.get(code, code)
        if not reason.get("scope_attempted") and reason.get("scope"):
            reason["scope_attempted"] = reason["scope"]
        if not reason.get("evidence_ids") and reason.get("evidence_id"):
            reason["evidence_ids"] = [reason["evidence_id"]]
        checked = reason.get("checked_sources")
        if isinstance(checked, str) and checked.strip():
            reason["checked_sources"] = [checked]
        normalized_reasons.append(reason)
    value["failure_reasons"] = normalized_reasons
    return value


_BLOCK_EVIDENCE_RE = re.compile(
    r"^ev_(?P<document>doc_[A-Za-z0-9]+)_(?P<index>\d{6})_(?P<digest>[A-Fa-f0-9*]+)$"
)
_DERIVED_EVIDENCE_RE = re.compile(
    r"^ev_derived_(?P<document>doc_[A-Za-z0-9]+)_(?P<digest>[A-Fa-f0-9]+)$"
)
_LEGACY_DERIVED_EVIDENCE_RE = re.compile(
    r"^ev_(?P<document>doc_[A-Za-z0-9]+)_(?P<digest>[A-Fa-f0-9]{8,})$"
)


def _canonical_evidence_id(
    identifier: Any, canonical_ids: set[str]
) -> str:
    """Resolve a stale evidence hash only when its structural match is unique."""

    candidate = str(identifier or "")
    if not candidate or candidate in canonical_ids:
        return candidate
    by_document_index: dict[tuple[str, str], list[str]] = {}
    by_document_digest: dict[tuple[str, str], list[str]] = {}
    for canonical in canonical_ids:
        block = _BLOCK_EVIDENCE_RE.fullmatch(canonical)
        if block:
            by_document_index.setdefault(
                (block.group("document"), block.group("index")), []
            ).append(canonical)
            by_document_digest.setdefault(
                (block.group("document"), block.group("digest").casefold()), []
            ).append(canonical)
            continue
        derived = _DERIVED_EVIDENCE_RE.fullmatch(canonical)
        if derived:
            by_document_digest.setdefault(
                (derived.group("document"), derived.group("digest").casefold()), []
            ).append(canonical)

    block = _BLOCK_EVIDENCE_RE.fullmatch(candidate)
    if block:
        matches = by_document_index.get(
            (block.group("document"), block.group("index")), []
        )
        if len(matches) == 1:
            return matches[0]
        if block.group("digest") != "*":
            matches = by_document_digest.get(
                (block.group("document"), block.group("digest").casefold()), []
            )
            if len(matches) == 1:
                return matches[0]
        return candidate
    derived = _DERIVED_EVIDENCE_RE.fullmatch(candidate)
    if not derived:
        derived = _LEGACY_DERIVED_EVIDENCE_RE.fullmatch(candidate)
    if derived:
        matches = by_document_digest.get(
            (derived.group("document"), derived.group("digest").casefold()), []
        )
        if len(matches) == 1:
            return matches[0]
    return candidate


def _canonicalize_review_evidence_ids(
    review: dict[str, Any], canonical_ids: set[str]
) -> dict[str, Any]:
    """Canonicalize exact evidence references without guessing ambiguous IDs."""

    def visit(node: Any) -> Any:
        if isinstance(node, dict):
            output: dict[str, Any] = {}
            for key, nested in node.items():
                normalized_key = (
                    _canonical_evidence_id(key, canonical_ids)
                    if str(key).startswith("ev_")
                    else key
                )
                output[str(normalized_key)] = visit(nested)
            return output
        if isinstance(node, list):
            return [visit(item) for item in node]
        if isinstance(node, str) and node.startswith("ev_"):
            return _canonical_evidence_id(node, canonical_ids)
        return node

    value = visit(review)
    return value if isinstance(value, dict) else {}


def _synchronize_builder_receipt(
    receipt: dict[str, Any], review: dict[str, Any], *, outputs: Path
) -> None:
    """Make the small builder receipt a deterministic projection of artifacts."""

    negative = review.get("decision") == "scientific_not_constructible"
    receipt["decision"] = (
        "scientific_not_constructible" if negative else "constructed"
    )
    receipt["task_pair_id"] = str(review.get("task_pair_id") or "")
    receipt["artifact_path"] = (
        "outputs/construction_receipt.json" if negative else "outputs"
    )
    scope = review.get("workflow_scope") or {}
    complexity = review.get("complexity_profile") or {}
    receipt["workflow_scope_kind"] = str(scope.get("kind") or "none")
    receipt["complexity_level"] = str(
        complexity.get("level") or "not_assessed"
    )
    receipt["failure_code"] = str(review.get("failure_code") or "") if negative else ""
    receipt["failure_reasons"] = (
        json.loads(json.dumps(review.get("failure_reasons") or [], ensure_ascii=False))
        if negative
        else []
    )
    if not str(receipt.get("summary") or "").strip():
        receipt["summary"] = str(
            review.get("workflow_summary")
            or review.get("scientific_question")
            or (
                "Source evidence does not support a constructible benchmark task."
                if negative
                else "Constructed the paired benchmark task artifacts."
            )
        )
    if negative:
        receipt["milestones"] = {
            "workflow_review_validated": True,
            "reproduction_validated": False,
            "autonomous_copy_created": False,
            "autonomous_validated": False,
            "hidden_reference_validated": False,
            "pair_draft_validated": False,
        }
        return
    milestones = dict(receipt.get("milestones") or {})
    reproduction = outputs / "paper_reproduction"
    autonomous = outputs / "autonomous_research"
    hidden = outputs / "hidden_reference"
    milestones["workflow_review_validated"] = True
    milestones["reproduction_validated"] = reproduction.is_dir() and all(
        (reproduction / name).is_file()
        for name in (
            "task.md",
            "task_info.json",
            "task_spec.json",
            "submission_contract.json",
            "process_rubric.json",
            "paper_route.md",
            "workflow_spec.json",
            "route_evidence_map.json",
        )
    )
    milestones["autonomous_copy_created"] = autonomous.is_dir()
    milestones["autonomous_validated"] = autonomous.is_dir() and all(
        (autonomous / name).is_file()
        for name in (
            "task.md",
            "task_info.json",
            "task_spec.json",
            "submission_contract.json",
            "process_rubric.json",
        )
    )
    milestones["hidden_reference_validated"] = hidden.is_dir() and all(
        (hidden / name).is_file()
        for name in (
            "ground_truth_common.json",
            "acceptance_profiles.json",
            "conclusion_rubric.json",
            "private_evidence_map.json",
        )
    )
    milestones["pair_draft_validated"] = all(
        milestones.get(name) is True
        for name in (
            "reproduction_validated",
            "autonomous_copy_created",
            "autonomous_validated",
            "hidden_reference_validated",
        )
    )
    receipt["milestones"] = milestones


def _normalize_public_asset_declarations(raw: Any) -> list[dict[str, Any]]:
    """Normalize list/map asset syntax without creating scientific inputs."""

    if isinstance(raw, list):
        candidates = [(str(index), value) for index, value in enumerate(raw, start=1)]
    elif isinstance(raw, dict):
        candidates = [(str(key), value) for key, value in raw.items()]
    else:
        return []

    rows: list[dict[str, Any]] = []
    for label, value in candidates:
        if isinstance(value, dict):
            row = dict(value)
        elif isinstance(value, str) and value.strip():
            row = {"description": value.strip()}
        else:
            continue
        if isinstance(raw, dict):
            row.setdefault("asset_id", label)
            if not row.get("path") and ("/" in label or Path(label).suffix):
                row["path"] = label
        rows.append(row)
    return rows


def _normalize_workflow_review_aliases(review: dict[str, Any]) -> dict[str, Any]:
    """Normalize harmless Agent naming variants before scientific validation.

    This is deliberately syntax-only.  It may rename fields and derive counts
    from already supplied workflow steps, but it never creates missing inputs,
    route facts, evidence, or Ground Truth values.
    """

    value = json.loads(json.dumps(review, ensure_ascii=False))
    public_basis = value.get("public_task_basis")
    if isinstance(public_basis, dict) and isinstance(
        public_basis.get("input_assets"), (list, dict)
    ):
        public_basis["input_assets"] = _normalize_public_asset_declarations(
            public_basis.get("input_assets")
        )

    scope = value.get("workflow_scope")
    if isinstance(scope, dict):
        aliases = {
            "scope_kind": "kind",
            "rationale": "selection_rationale",
            "included_workflows": "included_workflow_ids",
            "excluded_workflows": "excluded_workflow_ids",
            "included_claims": "included_claim_ids",
            "excluded_claims": "excluded_claim_ids",
            "scope_evidence": "scope_evidence_ids",
        }
        for source, target in aliases.items():
            if target not in scope and source in scope:
                scope[target] = scope[source]
        if not scope.get("included_claim_ids"):
            claims: list[str] = []
            for row in value.get("workflow_inventory") or []:
                if not isinstance(row, dict):
                    continue
                for key in ("claim_ids", "supports_claim_ids"):
                    rows = row.get(key) or []
                    claims.extend(rows if isinstance(rows, list) else [rows])
                if (
                    str(row.get("workflow_id") or "")
                    in {str(item) for item in scope.get("included_workflow_ids") or []}
                    and str(row.get("claim_supported") or "").strip()
                ):
                    claims.append(f"claim:{row['workflow_id']}")
            scope["included_claim_ids"] = [str(item) for item in claims if str(item)]
        if (
            scope.get("kind") not in {
                "full_paper_core_workflow",
                "full_paper_computational_workflow",
            }
            and not scope.get("larger_scope_failure_reasons")
        ):
            excluded = {
                str(row.get("workflow_id") or ""): str(row.get("excluded_reason") or "").strip()
                for row in value.get("workflow_inventory") or []
                if isinstance(row, dict) and str(row.get("excluded_reason") or "").strip()
            }
            reasons = [
                f"{workflow_id}: {excluded[workflow_id]}"
                for workflow_id in scope.get("excluded_workflow_ids") or []
                if str(workflow_id) in excluded
            ]
            if reasons:
                scope["larger_scope_failure_reasons"] = reasons
        if not scope.get("scope_evidence_ids"):
            scope["scope_evidence_ids"] = _workflow_review_evidence_ids(value)
        # Some harness/model combinations place the paper-level summary fields in
        # workflow_scope.  Promote them before the public projection below strips
        # route-bearing convenience fields from the scope copied into both tasks.
        for field in (
            "scientific_question",
            "public_scientific_question",
            "task_direction",
            "category",
            "workflow_summary",
        ):
            if not value.get(field) and scope.get(field):
                value[field] = scope[field]
        if not scope.get("selection_rationale"):
            rationale = str(
                scope.get("workflow_summary")
                or value.get("workflow_summary")
                or ""
            ).strip()
            if rationale:
                scope["selection_rationale"] = rationale

    selected_workflow_ids = {
        str(item)
        for item in (scope or {}).get("included_workflow_ids") or []
        if str(item)
    }
    selected_inventory = [
        row
        for row in value.get("workflow_inventory") or []
        if isinstance(row, dict)
        and (
            not selected_workflow_ids
            or str(row.get("workflow_id") or "") in selected_workflow_ids
        )
    ]
    if not value.get("workflow_steps"):
        value["workflow_steps"] = [
            dict(step)
            for row in selected_inventory
            for step in row.get("steps") or []
            if isinstance(step, dict)
        ]
    if not value.get("ground_truth_items"):
        value["ground_truth_items"] = [
            dict(truth)
            for row in selected_inventory
            for truth in row.get("ground_truth_items") or []
            if isinstance(truth, dict)
        ]

    normalized_steps: list[dict[str, Any]] = []
    for index, raw_step in enumerate(value.get("workflow_steps") or [], start=1):
        if not isinstance(raw_step, dict):
            continue
        step = dict(raw_step)
        step.setdefault("step_id", f"step-{index}")
        if not step.get("action"):
            step["action"] = str(
                step.get("name") or step.get("description") or step["step_id"]
            )
        if not step.get("depends_on") and step.get("dependencies"):
            dependencies = step.get("dependencies")
            step["depends_on"] = (
                list(dependencies) if isinstance(dependencies, list) else [dependencies]
            )
        step.setdefault("depends_on", [])
        if not step.get("output_artifacts"):
            output = step.get(
                "output_artifact",
                step.get("output", step.get("outputs", step.get("generated_output"))),
            )
            if output not in (None, ""):
                step["output_artifacts"] = (
                    list(output) if isinstance(output, list) else [output]
                )
        if not step.get("input_artifacts"):
            input_value = step.get("input_artifact", step.get("input"))
            if input_value not in (None, ""):
                step["input_artifacts"] = (
                    list(input_value)
                    if isinstance(input_value, list)
                    else [input_value]
                )
        if not step.get("method_parameters"):
            if isinstance(step.get("parameters"), dict) and step.get("parameters"):
                step["method_parameters"] = dict(step["parameters"])
            elif step.get("method"):
                step["method_parameters"] = {"method": step["method"]}
        if not step.get("evidence_ids") and step.get("evidence_id"):
            step["evidence_ids"] = [step["evidence_id"]]
        if not step.get("step_type"):
            action = str(step.get("action") or "").casefold()
            if any(
                token in action
                for token in ("frequency", "verify", "validation", "irc", "convergence")
            ):
                step["step_type"] = "validation"
            elif any(
                token in action
                for token in ("analysis", "compare", "profile", "thermochemistry", "gibbs")
            ):
                step["step_type"] = "scientific_analysis"
            else:
                step["step_type"] = "core_computation"
        normalized_steps.append(step)
    if normalized_steps:
        value["workflow_steps"] = normalized_steps

    complexity = value.get("complexity_profile")
    if isinstance(complexity, dict):
        aliases = {
            "core_computation_count": "scientific_core_operation_count",
            "core_operations": "scientific_core_operation_count",
            "tool_call_count": "estimated_typical_tool_calls",
            "tool_calls": "estimated_typical_tool_calls",
            "dependency_count": "dependency_edge_count",
            "dependencies": "dependency_edge_count",
            "branch_count": "parallel_branch_count",
            "branches": "parallel_branch_count",
            "system_state_count": "system_or_state_count",
            "systems": "system_or_state_count",
            "states": "system_or_state_count",
        }
        for source, target in aliases.items():
            if target in complexity or source not in complexity:
                continue
            raw_alias = complexity[source]
            if isinstance(raw_alias, list):
                complexity[target] = len(raw_alias)
            elif isinstance(raw_alias, int) and not isinstance(raw_alias, bool):
                complexity[target] = raw_alias
        if "system_or_state_count" not in complexity:
            counts = [
                complexity.get(name)
                for name in ("system_count", "state_count")
                if isinstance(complexity.get(name), int)
                and not isinstance(complexity.get(name), bool)
            ]
            if counts:
                complexity["system_or_state_count"] = max(counts)
        if "software_capability_count" not in complexity:
            capabilities = complexity.get("software_capabilities")
            if isinstance(capabilities, list):
                complexity["software_capability_count"] = len(capabilities)
        steps = value.get("workflow_steps") or []
        if "estimated_min_tool_calls" not in complexity:
            complexity["estimated_min_tool_calls"] = max(
                1, int(complexity.get("estimated_typical_tool_calls") or len(steps) or 1)
            )
        if "estimated_typical_tool_calls" not in complexity:
            complexity["estimated_typical_tool_calls"] = max(
                1, int(complexity.get("estimated_min_tool_calls") or len(steps) or 1)
            )
        if "scientific_core_operation_count" not in complexity:
            complexity["scientific_core_operation_count"] = sum(
                row.get("step_type")
                in {"core_computation", "scientific_analysis", "validation"}
                for row in steps
                if isinstance(row, dict)
            )
        for field in (
            "parallel_branch_count",
            "system_or_state_count",
            "software_capability_count",
        ):
            if field not in complexity:
                complexity[field] = 0
        # Dependency count is a derived graph property, never a model estimate.
        complexity["dependency_edge_count"] = sum(
            len(row.get("depends_on") or [])
            for row in steps
            if isinstance(row, dict)
        )
        for singular, plural in (
            ("iterative_decision", "iterative_decisions"),
            ("validation_operation", "validation_operations"),
            ("reasoning_requirement", "reasoning_requirements"),
            ("excluded_work", "non_core_operations_excluded"),
        ):
            if not complexity.get(plural) and complexity.get(singular):
                raw = complexity[singular]
                if isinstance(raw, list):
                    complexity[plural] = list(raw)
                elif isinstance(raw, int) and not isinstance(raw, bool):
                    complexity[plural] = [f"declared_{singular}_{index + 1}" for index in range(raw)]
                else:
                    complexity[plural] = [raw]
            complexity.setdefault(plural, [])
        if not complexity.get("validation_operations"):
            complexity["validation_operations"] = [
                str(row.get("action") or row.get("step_id"))
                for row in steps
                if isinstance(row, dict) and row.get("step_type") == "validation"
            ]
    normalized_truths: list[dict[str, Any]] = []
    for index, raw in enumerate(value.get("ground_truth_items") or [], start=1):
        if not isinstance(raw, dict):
            continue
        truth = dict(raw)
        for source, target in (
            ("item_id", "ground_truth_id"),
            ("value", "canonical_answer"),
            ("type", "kind"),
        ):
            if target not in truth and source in truth:
                truth[target] = truth[source]
        truth.setdefault("ground_truth_id", f"gt-{index}")
        kind = str(truth.get("kind") or "textual_intermediate_conclusion")
        claim_role = str(truth.get("claim_role") or "").casefold()
        item_type = str(truth.get("item_type") or "").casefold()
        if "numeric" in item_type or "energy_difference" in item_type:
            kind = (
                "numeric_final_result"
                if claim_role == "final"
                else "numeric_intermediate_result"
            )
        elif "ranking" in item_type or "ordering" in item_type:
            kind = "ranking"
        elif "trend" in item_type:
            kind = "trend"
        truth["kind"] = {
            "numerical_value": "numeric_final_result",
            "numeric_value": "numeric_final_result",
            "numeric": (
                "numeric_final_result"
                if claim_role == "final"
                else "numeric_intermediate_result"
            ),
            "numerical": (
                "numeric_final_result"
                if claim_role == "final"
                else "numeric_intermediate_result"
            ),
            "conclusion": "textual_final_conclusion",
            "textual_conclusion": "textual_final_conclusion",
            "textual": (
                "textual_final_conclusion"
                if claim_role == "final"
                else "textual_intermediate_conclusion"
            ),
            "intermediate_conclusion": "textual_intermediate_conclusion",
        }.get(kind, kind)
        if not truth.get("evidence_ids") and truth.get("evidence_id"):
            truth["evidence_ids"] = [truth["evidence_id"]]
        canonical_answer = truth.get("canonical_answer")
        numeric_answer = (
            isinstance(canonical_answer, (int, float))
            and not isinstance(canonical_answer, bool)
        ) or (
            isinstance(canonical_answer, dict)
            and isinstance(canonical_answer.get("value"), (int, float))
            and not isinstance(canonical_answer.get("value"), bool)
        )
        if not truth.get("acceptance_type") or (
            numeric_answer
            and truth["kind"].startswith("numeric_")
            and truth.get("acceptance_type") == "semantic_propositions"
        ) or (
            truth["kind"] in {"ranking", "trend"}
            and truth.get("acceptance_type") == "semantic_propositions"
        ):
            truth["acceptance_type"] = {
                "numeric_final_result": "numeric_tolerance",
                "numeric_intermediate_result": "numeric_tolerance",
                "ranking": "ranking",
                "trend": "trend",
            }.get(truth["kind"], "semantic_propositions")
        if not truth.get("required_propositions") and isinstance(
            truth.get("canonical_answer"), str
        ) and truth["kind"].startswith("textual_"):
            truth["required_propositions"] = [truth["canonical_answer"]]
        parameters = dict(truth.get("acceptance_parameters") or {})
        if isinstance(canonical_answer, dict):
            if canonical_answer.get("unit") not in (None, ""):
                parameters.setdefault("unit", canonical_answer["unit"])
            declared_tolerance = canonical_answer.get("tolerance")
            if isinstance(declared_tolerance, dict):
                if declared_tolerance.get("absolute") is not None:
                    parameters.setdefault(
                        "absolute_tolerance", declared_tolerance["absolute"]
                    )
                if declared_tolerance.get("relative") is not None:
                    parameters.setdefault(
                        "relative_tolerance", declared_tolerance["relative"]
                    )
        if truth.get("unit") not in (None, ""):
            parameters.setdefault("unit", truth["unit"])
        tolerance = truth.get("tolerance")
        if tolerance is not None:
            tolerance_kind = str(truth.get("tolerance_type") or "absolute").casefold()
            parameters.setdefault(
                "relative_tolerance" if tolerance_kind == "relative" else "absolute_tolerance",
                tolerance,
            )
        truth["acceptance_parameters"] = parameters
        truth.setdefault("required_propositions", [])
        truth.setdefault("forbidden_contradictions", [])
        truth.setdefault("evidence_grade", "B")
        truth.setdefault("claim_role", "final" if "final" in truth["kind"] else "intermediate")
        normalized_truths.append(truth)
    if normalized_truths:
        value["ground_truth_items"] = normalized_truths
        if isinstance(scope, dict) and not scope.get("included_claim_ids"):
            scope["included_claim_ids"] = [
                str(row.get("ground_truth_id"))
                for row in normalized_truths
                if str(row.get("ground_truth_id") or "")
            ]
    for reason in value.get("failure_reasons") or []:
        if isinstance(reason, dict) and not reason.get("evidence_ids") and reason.get(
            "evidence_id"
        ):
            reason["evidence_ids"] = [reason["evidence_id"]]
    return value


def _workflow_review_evidence_ids(review: dict[str, Any]) -> list[str]:
    ids: list[str] = []
    for row in review.get("workflow_inventory") or []:
        if isinstance(row, dict):
            values = row.get("evidence_ids") or []
            ids.extend(values if isinstance(values, list) else [values])
    for row in review.get("workflow_steps") or []:
        if isinstance(row, dict):
            values = row.get("evidence_ids") or []
            ids.extend(values if isinstance(values, list) else [values])
    return sorted({str(item) for item in ids if str(item)})


def _json_object(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        value = read_json(path)
    except (OSError, ValueError, TypeError):
        return {}
    return value if isinstance(value, dict) else {}


def _canonical_workflow_scope(scope: Any) -> dict[str, Any]:
    if not isinstance(scope, dict):
        return {}
    allowed = (
        "kind",
        "included_workflow_ids",
        "excluded_workflow_ids",
        "included_claim_ids",
        "excluded_claim_ids",
        "selection_rationale",
        "larger_scope_failure_reasons",
        "scope_evidence_ids",
        "central_scientific_question",
        "supported_primary_claims",
        "parent_workflow_position",
        "why_not_full_workflow",
        "excluded_workflows_summary",
    )
    output = {key: json.loads(json.dumps(scope[key])) for key in allowed if key in scope}
    for key in (
        "included_workflow_ids",
        "excluded_workflow_ids",
        "included_claim_ids",
        "excluded_claim_ids",
        "larger_scope_failure_reasons",
        "scope_evidence_ids",
    ):
        output.setdefault(key, [])
    return output


def _normalize_boundary_contract(
    rows: Any, *, evidence_ids: list[str]
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    normalized_rows: list[Any]
    if isinstance(rows, dict):
        normalized_rows = [
            {"name": str(name), "value": value}
            for name, value in rows.items()
            if value not in (None, "", [], {})
        ]
    else:
        normalized_rows = rows if isinstance(rows, list) else []
    for index, raw in enumerate(normalized_rows, start=1):
        if isinstance(raw, dict):
            row = dict(raw)
            name = str(
                row.get("name")
                or row.get("condition")
                or row.get("type")
                or f"condition-{index}"
            ).strip()
            value = row.get("value", row.get("description"))
        else:
            text = str(raw or "").strip()
            if not text:
                continue
            left, separator, right = text.partition(":")
            name = left.strip() if separator and left.strip() else f"condition-{index}"
            value = right.strip() if separator and right.strip() else text
            row = {}
        row["name"] = name
        row["value"] = value
        if not row.get("evidence_ids") and evidence_ids:
            row["evidence_ids"] = list(evidence_ids)
        output.append(row)
    return output


def _public_boundary_projection(rows: Any) -> Any:
    """Remove paper-route method fields from a reproduction-spec fallback."""

    denied = (
        "method",
        "functional",
        "basis",
        "pseudopotential",
        "dispersion",
        "software",
        "program",
        "package",
        "solvation_model",
        "entropy",
        "grid",
        "kpoint",
        "k_point",
        "cutoff",
        "symmetry",
    )

    def is_public(name: Any) -> bool:
        normalized = str(name or "").casefold().replace("-", "_").replace(" ", "_")
        return not any(token in normalized for token in denied)

    if isinstance(rows, dict):
        return {key: value for key, value in rows.items() if is_public(key)}
    if isinstance(rows, list):
        return [
            row
            for row in rows
            if not isinstance(row, dict)
            or is_public(row.get("name") or row.get("condition") or row.get("type"))
        ]
    return rows


def _task_input_relative_path(value: Any) -> str:
    relative = validate_relative_path(str(value or ""))
    for prefix in ("task/data/inputs/", "data/inputs/", "task/inputs/"):
        if relative.startswith(prefix):
            relative = relative[len(prefix) :]
            break
    return _normalize_public_input_path(relative)


_UNCERTAIN_ASSET_RE = re.compile(
    r"\b(?:approximate(?:ly)?|best[- ]effort|estimated|guessed|inferred|placeholder|"
    r"reconstruct(?:ed|ion)?|verify|cross[- ]check|not text[- ]extractable)\b",
    flags=re.IGNORECASE,
)
_XYZ_ROUTE_COMMENT_RE = re.compile(
    r"(?:optimized geometry|level of theory|\b(?:pbe0|b3lyp|wb97|ωb97|m06|d3(?:bj)?|"
    r"def2|6-31g|cc-pv|basis|functional)\b)",
    flags=re.IGNORECASE,
)
_XYZ_COMMENT_REDACTION_ID = "xyz_route_comment_redaction_v1"


def _public_xyz_bytes(content: bytes, *, relative: str) -> tuple[bytes, bool]:
    """Redact route-bearing XYZ comments without changing coordinates."""

    if Path(relative).suffix.casefold() != ".xyz":
        return content, False
    try:
        text = content.decode("utf-8", errors="strict")
    except UnicodeDecodeError:
        return content, False
    lines = text.splitlines()
    if len(lines) < 2 or not _XYZ_ROUTE_COMMENT_RE.search(lines[1]):
        return content, False
    lines[1] = f"Source-provided geometry: {Path(relative).name}"
    suffix = "\n" if text.endswith(("\n", "\r")) else ""
    return ("\n".join(lines) + suffix).encode("utf-8"), True


def _snapshot_relative_file(source_root: Path, value: Any) -> Path | None:
    try:
        relative = validate_relative_path(str(value or ""))
        candidate = (source_root / relative).resolve()
        candidate.relative_to(source_root.resolve())
    except (ValueError, OSError):
        return None
    return candidate if candidate.is_file() and not candidate.is_symlink() else None


def _source_asset_catalog(
    *, source_root: Path, evidence_index: list[dict[str, Any]]
) -> dict[str, list[dict[str, Any]]]:
    """Index only canonical, evidence-linked source/derived files by byte hash."""

    evidence_by_id = {
        str(row.get("evidence_id")): row
        for row in evidence_index
        if isinstance(row, dict) and row.get("evidence_id")
    }
    records: list[dict[str, Any]] = []

    def add(
        path_value: Any,
        *,
        evidence_id: Any,
        description: Any = "",
        source_ref: Any = None,
    ) -> None:
        path = _snapshot_relative_file(source_root, path_value)
        identifier = str(evidence_id or "")
        if path is None or identifier not in evidence_by_id:
            return
        relative = path.relative_to(source_root.resolve()).as_posix()
        reference = source_ref if isinstance(source_ref, dict) else {}
        records.append(
            {
                "path": relative,
                "sha256": sha256_file(path),
                "evidence_id": identifier,
                "description": str(description or evidence_by_id[identifier].get("text") or ""),
                "source_ref": reference,
                "deterministic_transform": bool(
                    reference.get("derivation")
                    or "/derived_coordinates/" in f"/{relative}"
                    or "/derived_tables/" in f"/{relative}"
                ),
            }
        )

    path_pattern = re.compile(
        r"documents/[A-Za-z0-9_.\-/]+\.(?:xyz|mol2?|sdf|smi|csv|tsv|txt|json)",
        flags=re.IGNORECASE,
    )
    for row in evidence_index:
        if not isinstance(row, dict) or not row.get("evidence_id"):
            continue
        for relative in path_pattern.findall(str(row.get("text") or "")):
            add(
                relative.rstrip(".,;:)\"]}"),
                evidence_id=row["evidence_id"],
                description=row.get("text"),
                source_ref=row.get("source_ref"),
            )

    for index_path in sorted(
        [
            *source_root.glob("documents/*/derived_coordinates/index.json"),
            *source_root.glob("documents/*/derived_tables/index.json"),
        ]
    ):
        try:
            payload = read_json(index_path)
        except (OSError, ValueError, TypeError):
            continue
        if isinstance(payload, dict):
            rows = next(
                (
                    payload.get(key)
                    for key in ("items", "coordinates", "tables", "records")
                    if isinstance(payload.get(key), list)
                ),
                [],
            )
        else:
            rows = payload if isinstance(payload, list) else []
        for row in rows:
            if not isinstance(row, dict):
                continue
            add(
                row.get("path") or row.get("file") or row.get("source_file"),
                evidence_id=row.get("evidence_id"),
                description=row.get("label") or row.get("caption"),
                source_ref=row.get("source_ref"),
            )

    catalog: dict[str, list[dict[str, Any]]] = {}
    seen: set[tuple[str, str]] = set()
    for record in records:
        key = (record["path"], record["evidence_id"])
        if key in seen:
            continue
        seen.add(key)
        catalog.setdefault(record["sha256"], []).append(record)
    return catalog


def _asset_source_matches(
    *,
    digest: str,
    asset: dict[str, Any],
    catalog: dict[str, list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    matches = list(catalog.get(digest) or [])
    source_file = str(
        asset.get("source_file") or asset.get("source_path") or ""
    ).strip()
    if source_file:
        matches = [row for row in matches if row.get("path") == source_file]
    cited = {
        str(item)
        for item in (
            asset.get("source_evidence_ids")
            or ([asset["source_evidence_id"]] if asset.get("source_evidence_id") else [])
        )
        if str(item)
    }
    if cited:
        evidence_matches = [row for row in matches if row.get("evidence_id") in cited]
        if evidence_matches:
            matches = evidence_matches
    return matches


def _transformed_asset_source_matches(
    *,
    content: bytes,
    relative: str,
    asset: dict[str, Any],
    catalog: dict[str, list[dict[str, Any]]],
    source_root: Path,
) -> list[dict[str, Any]]:
    provenance = asset.get("provenance") or {}
    if provenance.get("transform_id") != _XYZ_COMMENT_REDACTION_ID:
        return []
    source_file = str(
        asset.get("source_file") or asset.get("source_path") or ""
    ).strip()
    candidates = [
        row
        for rows in catalog.values()
        for row in rows
        if not source_file or row.get("path") == source_file
    ]
    matches: list[dict[str, Any]] = []
    for row in candidates:
        source = _snapshot_relative_file(source_root, row.get("path"))
        if source is None:
            continue
        transformed, changed = _public_xyz_bytes(
            source.read_bytes(), relative=relative
        )
        if changed and transformed == content:
            matches.append(row)
    return matches


def _recover_public_assets(
    *,
    mode_roots: list[Path],
    rows: Any,
    source_root: Path,
    evidence_index: list[dict[str, Any]],
    discover_source_matched_files: bool = False,
) -> tuple[list[dict[str, Any]], list[str]]:
    """Recover public inputs only when bytes match canonical source evidence."""

    catalog = _source_asset_catalog(
        source_root=source_root, evidence_index=evidence_index
    )
    assets: list[dict[str, Any]] = []
    unresolved: list[str] = []
    raw_rows = rows if isinstance(rows, list) else []
    for index, raw in enumerate(raw_rows, start=1):
        if not isinstance(raw, dict):
            continue
        asset = dict(raw)
        target_value = (
            asset.get("path")
            or asset.get("file")
            or asset.get("target_path")
            or Path(str(asset.get("source_file") or "")).name
        )
        try:
            relative = _task_input_relative_path(target_value)
        except ValueError:
            unresolved.append(f"invalid_asset_path:{index}")
            continue
        staged = next(
            (
                root / "data" / "inputs" / relative
                for root in mode_roots
                if (root / "data" / "inputs" / relative).is_file()
                and (root / "data" / "inputs" / relative).stat().st_size > 0
            ),
            None,
        )
        content = asset.get("content")
        content_bytes: bytes | None = None
        if staged is not None:
            content_bytes = staged.read_bytes()
            try:
                content = content_bytes.decode("utf-8", errors="strict")
            except UnicodeDecodeError:
                content = None
                unresolved.append(f"non_text_public_asset:{relative}")
        elif content is not None:
            content = _asset_content(content)
            content_bytes = content.encode("utf-8")
        if content_bytes is None:
            unresolved.append(f"missing_public_asset:{relative}")

        uncertain_text = " ".join(
            str(asset.get(field) or "")
            for field in ("note", "notes", "warning", "provenance_note")
        )
        matches = (
            _asset_source_matches(
                digest=hashlib.sha256(content_bytes).hexdigest(),
                asset=asset,
                catalog=catalog,
            )
            if content_bytes is not None
            else []
        )
        if content_bytes is not None and not matches:
            matches = _transformed_asset_source_matches(
                content=content_bytes,
                relative=relative,
                asset=asset,
                catalog=catalog,
                source_root=source_root,
            )
        introduced = [
            value
            for match in matches
            for value in (match.get("source_ref") or {}).get("introduced_values") or []
        ]
        trusted = bool(matches) and not introduced and not _UNCERTAIN_ASSET_RE.search(
            uncertain_text
        )

        asset["path"] = relative
        asset["content"] = content
        asset.setdefault("description", str(asset.get("name") or f"Public input {index}"))
        asset.setdefault("role", "computational_input")
        provenance = dict(asset.get("provenance") or {})
        if trusted:
            transformed_content, route_comment_redacted = _public_xyz_bytes(
                content_bytes or b"", relative=relative
            )
            if route_comment_redacted:
                content_bytes = transformed_content
                content = transformed_content.decode("utf-8")
                for mode_root in mode_roots:
                    target = mode_root / "data" / "inputs" / relative
                    if target.is_file():
                        make_writable(target)
                        target.write_bytes(transformed_content)
            asset["content"] = content
            evidence = list(
                dict.fromkeys(str(match["evidence_id"]) for match in matches)
            )
            asset["source_evidence_ids"] = evidence
            asset["source_file"] = str(matches[0]["path"])
            provenance = {
                "kind": (
                    "deterministic_transform"
                    if any(match.get("deterministic_transform") for match in matches)
                    else "source_copy"
                ),
                "derivation": str(
                    (matches[0].get("source_ref") or {}).get("derivation")
                    or "Byte-for-byte copy of an evidence-linked source file."
                ),
                "introduced_values": [],
                "source_sha256": str(matches[0]["sha256"]),
            }
            if route_comment_redacted or (
                (asset.get("provenance") or {}).get("transform_id")
                == _XYZ_COMMENT_REDACTION_ID
            ):
                provenance.update(
                    {
                        "kind": "deterministic_transform",
                        "derivation": (
                            "Evidence-linked XYZ with route-bearing comment metadata "
                            "replaced by a neutral public label; coordinates are unchanged."
                        ),
                        "transform_id": _XYZ_COMMENT_REDACTION_ID,
                    }
                )
        else:
            unresolved.append(f"unverified_public_asset_provenance:{relative}")
            provenance.update(
                {
                    "kind": "unverified_agent_staging",
                    "derivation": str(
                        provenance.get("derivation")
                        or "The staged bytes could not be matched uniquely to canonical source evidence."
                    ),
                    "introduced_values": list(
                        provenance.get("introduced_values")
                        or ["source_alignment_unverified"]
                    ),
                }
            )
        asset["provenance"] = provenance
        assets.append(asset)

    if discover_source_matched_files and not raw_rows:
        seen_paths: set[str] = set()
        for mode_root in mode_roots:
            data_root = mode_root / "data" / "inputs"
            if not data_root.is_dir():
                continue
            for staged in sorted(path for path in data_root.rglob("*") if path.is_file()):
                relative = staged.relative_to(data_root).as_posix()
                if relative in seen_paths:
                    continue
                matches = catalog.get(sha256_file(staged)) or []
                if not matches:
                    continue
                try:
                    content_bytes = staged.read_bytes()
                    public_bytes, route_comment_redacted = _public_xyz_bytes(
                        content_bytes, relative=relative
                    )
                    if route_comment_redacted:
                        make_writable(staged)
                        staged.write_bytes(public_bytes)
                    content = public_bytes.decode("utf-8", errors="strict")
                except UnicodeDecodeError:
                    unresolved.append(f"non_text_public_asset:{relative}")
                    continue
                introduced = [
                    value
                    for match in matches
                    for value in (match.get("source_ref") or {}).get("introduced_values") or []
                ]
                if introduced:
                    unresolved.append(f"source_asset_introduces_values:{relative}")
                    continue
                seen_paths.add(relative)
                assets.append(
                    {
                        "path": relative,
                        "description": f"Source-provided computational input: {relative}.",
                        "role": "computational_input",
                        "content": content,
                        "source_evidence_ids": list(
                            dict.fromkeys(
                                str(match["evidence_id"]) for match in matches
                            )
                        ),
                        "source_file": str(matches[0]["path"]),
                        "provenance": {
                            "kind": (
                                "deterministic_transform"
                                if any(
                                    match.get("deterministic_transform")
                                    for match in matches
                                )
                                else "source_copy"
                            ),
                            "derivation": str(
                                (matches[0].get("source_ref") or {}).get("derivation")
                                or "Byte-for-byte copy of an evidence-linked source file."
                            ),
                            "introduced_values": [],
                            "source_sha256": str(matches[0]["sha256"]),
                            **(
                                {
                                    "kind": "deterministic_transform",
                                    "derivation": (
                                        "Evidence-linked XYZ with route-bearing comment metadata "
                                        "replaced by a neutral public label; coordinates are unchanged."
                                    ),
                                    "transform_id": _XYZ_COMMENT_REDACTION_ID,
                                }
                                if route_comment_redacted
                                else {}
                            ),
                        },
                    }
                )
    return assets, sorted(set(unresolved))


def _normalize_artifact_workflow_steps(
    rows: Any, *, evidence_ids: list[str]
) -> list[dict[str, Any]]:
    preliminary: list[dict[str, Any]] = []
    for index, raw in enumerate(rows if isinstance(rows, list) else [], start=1):
        if not isinstance(raw, dict):
            continue
        step = dict(raw)
        step["step_id"] = str(step.get("step_id") or f"step-{index}")
        if not step.get("action"):
            step["action"] = str(
                step.get("name") or step.get("description") or step["step_id"]
            )
        inputs = step.get("input_artifacts", step.get("input_artifact", step.get("input")))
        outputs = step.get(
            "output_artifacts",
            step.get(
                "output_artifact",
                step.get("output", step.get("outputs", step.get("generated_output"))),
            ),
        )
        step["input_artifacts"] = (
            list(inputs) if isinstance(inputs, list) else [inputs] if inputs not in (None, "") else []
        )
        step["output_artifacts"] = (
            list(outputs)
            if isinstance(outputs, list)
            else [outputs]
            if outputs not in (None, "")
            else []
        )
        dependencies = step.get("depends_on", step.get("dependencies")) or []
        step["depends_on"] = (
            list(dependencies) if isinstance(dependencies, list) else [dependencies]
        )
        if not step.get("method_parameters"):
            if isinstance(step.get("parameters"), dict) and step.get("parameters"):
                step["method_parameters"] = dict(step["parameters"])
            elif step.get("method"):
                step["method_parameters"] = {"method": step["method"]}
        action = str(step.get("action") or "").casefold()
        if not step.get("step_type"):
            if any(token in action for token in ("frequency", "verify", "irc", "validation")):
                step["step_type"] = "validation"
            elif any(token in action for token in ("analysis", "compare", "profile", "gibbs")):
                step["step_type"] = "scientific_analysis"
            else:
                step["step_type"] = "core_computation"
        if not step.get("evidence_ids") and step.get("evidence_id"):
            step["evidence_ids"] = [step["evidence_id"]]
        if not step.get("evidence_ids") and evidence_ids:
            step["evidence_ids"] = list(evidence_ids)
        preliminary.append(step)

    producer: dict[str, str] = {}
    for step in preliminary:
        for artifact in step.get("output_artifacts") or []:
            text = str(artifact)
            producer[text] = step["step_id"]
            producer[Path(text).name] = step["step_id"]
    for step in preliminary:
        dependencies = [str(item) for item in step.get("depends_on") or [] if str(item)]
        for artifact in step.get("input_artifacts") or []:
            text = str(artifact)
            dependency = producer.get(text) or producer.get(Path(text).name)
            if dependency and dependency != step["step_id"] and dependency not in dependencies:
                dependencies.append(dependency)
        step["depends_on"] = dependencies
    return preliminary


def _recover_workflow_review_from_pair_artifacts(
    review: dict[str, Any],
    outputs: Path,
    *,
    source_root: Path,
    evidence_index: list[dict[str, Any]],
) -> dict[str, Any]:
    """Recover fields already present in Agent artifacts into the review contract.

    No structure, parameter, method, route, or answer is synthesized here. Missing
    files remain missing and are rejected by the normal scientific validators.
    """

    value = json.loads(json.dumps(review, ensure_ascii=False))
    if value.get("decision") != "candidate_ready":
        return value
    autonomous_root = outputs / "autonomous_research"
    reproduction_root = outputs / "paper_reproduction"
    autonomous_info = _json_object(autonomous_root / "task_info.json")
    autonomous_spec = _json_object(autonomous_root / "task_spec.json")
    reproduction_info = _json_object(reproduction_root / "task_info.json")
    reproduction_spec = _json_object(reproduction_root / "task_spec.json")
    workflow_spec = _json_object(reproduction_root / "workflow_spec.json")

    scope = value.get("workflow_scope") or {}
    scope_evidence = [str(item) for item in scope.get("scope_evidence_ids") or []]
    for field, candidates in {
        "scientific_question": (
            scope.get("scientific_question"),
            reproduction_spec.get("scientific_question"),
            autonomous_spec.get("scientific_question"),
        ),
        "public_scientific_question": (
            scope.get("public_scientific_question"),
            autonomous_spec.get("scientific_question"),
        ),
        "task_direction": (
            scope.get("task_direction"),
            autonomous_info.get("benchmark_family"),
        ),
        "category": (
            scope.get("category"),
            autonomous_info.get("category"),
            reproduction_info.get("category"),
        ),
        "workflow_summary": (
            scope.get("workflow_summary"),
            reproduction_info.get("scientific_mode_description"),
        ),
    }.items():
        if not value.get(field):
            value[field] = next((item for item in candidates if str(item or "").strip()), "")

    route_rows = (
        workflow_spec.get("workflow_steps")
        or workflow_spec.get("steps")
        or workflow_spec.get("route_steps")
        or []
    )
    recovered_steps = _normalize_artifact_workflow_steps(
        route_rows, evidence_ids=scope_evidence
    )
    if len(recovered_steps) > len(value.get("workflow_steps") or []):
        value["workflow_steps"] = recovered_steps

    public_basis = dict(value.get("public_task_basis") or {})
    public_basis.setdefault(
        "scientific_question",
        value.get("public_scientific_question") or autonomous_spec.get("scientific_question"),
    )
    public_basis.setdefault(
        "target_definition",
        autonomous_spec.get("target_definition") or public_basis.get("scientific_question"),
    )
    boundaries = public_basis.get("boundary_conditions")
    if not boundaries:
        boundaries = _public_boundary_projection(
            reproduction_spec.get("boundary_conditions")
            or autonomous_spec.get("boundary_conditions")
            or []
        )
    boundaries = _normalize_boundary_contract(boundaries, evidence_ids=scope_evidence)
    public_basis["boundary_conditions"] = boundaries
    declared_assets = _normalize_public_asset_declarations(
        public_basis.get("input_assets")
    )
    raw_assets = declared_assets
    assets, unresolved = _recover_public_assets(
        mode_roots=[reproduction_root, autonomous_root],
        rows=raw_assets,
        source_root=source_root,
        evidence_index=evidence_index,
        discover_source_matched_files=not bool(declared_assets),
    )
    if not assets or unresolved:
        # A partially built reproduction may retain declarations only in its
        # task spec. They remain untrusted unless the staged bytes match a
        # canonical source/derived asset.
        fallback_assets = _normalize_public_asset_declarations(
            reproduction_spec.get("input_assets")
            or autonomous_spec.get("input_assets")
            or []
        )
        if fallback_assets:
            fallback_recovered, fallback_unresolved = _recover_public_assets(
                mode_roots=[reproduction_root, autonomous_root],
                rows=fallback_assets,
                source_root=source_root,
                evidence_index=evidence_index,
            )
            if len(fallback_recovered) > len(assets) or (
                len(fallback_recovered) == len(assets)
                and len(fallback_unresolved) < len(unresolved)
            ):
                assets, unresolved = fallback_recovered, fallback_unresolved
    public_basis["input_assets"] = assets
    completeness = dict(public_basis.get("input_completeness") or {})
    completeness["status"] = (
        "confirmed" if assets and boundaries and not unresolved else "incomplete"
    )
    completeness["unresolved_fields"] = unresolved
    completeness["closed_fields"] = [
        *[f"input_asset:{asset['path']}" for asset in assets if asset.get("content") is not None],
        *[f"boundary:{row.get('name')}" for row in boundaries if row.get("value") not in (None, "")],
    ]
    public_basis["input_completeness"] = completeness
    value["public_task_basis"] = public_basis

    paper_route = dict(value.get("paper_route") or {})
    route_steps = recovered_steps or value.get("workflow_steps") or []
    if not paper_route.get("route_steps") and route_steps:
        paper_route["route_steps"] = [
            {
                "step_id": step.get("step_id"),
                "mapped_author_step": step.get("action"),
                "method_parameters": step.get("method_parameters") or {},
                "evidence_ids": step.get("evidence_ids") or [],
            }
            for step in route_steps
            if isinstance(step, dict)
        ]
    software_names: list[str] = []
    methods: list[str] = []
    for step in route_steps:
        if not isinstance(step, dict):
            continue
        software = step.get("software")
        software_rows = software if isinstance(software, list) else [software]
        for row in software_rows:
            name = str(row.get("name") if isinstance(row, dict) else row or "").strip()
            if name and name not in software_names:
                software_names.append(name)
        method = (step.get("method_parameters") or {}).get("method") or step.get("method")
        if str(method or "").strip() and str(method) not in methods:
            methods.append(str(method))
    if not paper_route.get("software") and software_names:
        paper_route["software"] = [
            {"name": name, "role": "core_compute", "evidence_ids": scope_evidence}
            for name in software_names
        ]
    if not paper_route.get("method") and methods:
        paper_route["method"] = "; ".join(methods)
    paper_route.setdefault("method_parameters", {})
    paper_route.setdefault("sequence", [step.get("step_id") for step in route_steps])
    paper_route.setdefault(
        "validation_procedure",
        "; ".join(
            str(step.get("action") or step.get("step_id"))
            for step in route_steps
            if isinstance(step, dict) and step.get("step_type") == "validation"
        ),
    )
    if not paper_route.get("autonomous_forbidden_disclosures"):
        paper_route["autonomous_forbidden_disclosures"] = [
            *software_names,
            *methods,
        ]
    route_unresolved = []
    if not route_steps:
        route_unresolved.append("workflow_steps")
    if not paper_route.get("software"):
        route_unresolved.append("software")
    if not paper_route.get("method") and not any(
        (step.get("method_parameters") or {}) for step in route_steps if isinstance(step, dict)
    ):
        route_unresolved.append("method")
    route_completeness = dict(paper_route.get("route_completeness") or {})
    route_completeness["status"] = "confirmed" if not route_unresolved else "incomplete"
    route_completeness["unresolved_fields"] = route_unresolved
    route_completeness["closed_fields"] = [
        *[f"route_step:{step.get('step_id')}" for step in route_steps if step.get("step_id")],
        *[f"software:{name}" for name in software_names],
        *[f"method:{method}" for method in methods],
    ]
    paper_route["route_completeness"] = route_completeness
    value["paper_route"] = paper_route
    value["workflow_scope"] = _canonical_workflow_scope(scope)
    return value


def _mode_asset_projection(public_basis: dict[str, Any]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for asset in public_basis.get("input_assets") or []:
        if not isinstance(asset, dict):
            continue
        try:
            relative = _normalize_public_input_path(str(asset.get("path") or ""))
        except ValueError:
            continue
        output.append(
            {
                "path": f"data/inputs/{relative}",
                "description": asset.get("description") or asset.get("name") or "Public input",
                "role": asset.get("role") or "computational_input",
                "source_evidence_ids": asset.get("source_evidence_ids") or [],
            }
        )
    return output


def _normalize_required_deliverables(
    info: dict[str, Any], submission: dict[str, Any]
) -> list[dict[str, Any]]:
    descriptions: dict[str, str] = {}
    for row in info.get("required_deliverables") or []:
        if not isinstance(row, dict):
            continue
        try:
            path = _normalize_runtime_artifact_path(str(row.get("path") or ""))
        except ValueError:
            continue
        descriptions[path] = str(row.get("description") or "Required task artifact.")
    return [
        {
            "path": path,
            "description": descriptions.get(path, "Required task artifact."),
            "allow_empty": False,
        }
        for path in submission.get("required_files") or []
    ]


def _ensure_reproduction_route_rubric(
    rubric: list[dict[str, Any]], *, submission: dict[str, Any]
) -> list[dict[str, Any]]:
    if not rubric:
        return rubric
    output = json.loads(json.dumps(rubric, ensure_ascii=False))
    evidence_paths = [
        str(path)
        for path in submission.get("required_files") or []
        if any(
            token in str(path).casefold()
            for token in ("trace", "provenance", "plan", "report")
        )
    ]
    if not evidence_paths:
        # The evaluator/harness owns the canonical tool trace.  The task only
        # requires a scientific report as human-readable route evidence.
        evidence_paths = ["report/report.md"]
    target = next(
        (
            row
            for row in output
            if isinstance(row, dict)
            and (
                str(row.get("criterion_type") or "").casefold() == "route_fidelity"
                or str(row.get("id") or "").casefold()
                in {"paper_route_fidelity", "route_fidelity"}
            )
        ),
        None,
    )
    if target is None:
        # Do not repurpose an unrelated scientific criterion as route fidelity.
        # Add one small generic transport criterion instead and rebalance the
        # existing numeric rubric, preserving every original criterion's
        # meaning. This is contract closure, not a scientific pass/fail rule.
        numeric_scores: list[float] = []
        for row in output:
            try:
                score = float(row.get("max_score", 0))
            except (TypeError, ValueError):
                numeric_scores = []
                break
            numeric_scores.append(score)
        total = sum(numeric_scores)
        if numeric_scores and total > 0:
            route_score = min(20.0, max(5.0, round(total * 0.10, 2)))
            scale = max(0.0, (total - route_score) / total)
            for row, score in zip(output, numeric_scores):
                row["max_score"] = round(score * scale, 2)
            correction = round(
                (100.0 - route_score)
                - sum(float(row["max_score"]) for row in output),
                2,
            )
            output[-1]["max_score"] = round(float(output[-1]["max_score"]) + correction, 2)
            output.append(
                {
                    "id": "paper_route_fidelity",
                    "criterion_type": "route_fidelity",
                    "max_score": route_score,
                    "name": "Paper-route fidelity",
                    "description": "Follow the disclosed paper route, dependency order, method hierarchy, and validation sequence.",
                    "evidence_artifacts": evidence_paths,
                }
            )
            # Correct a final centering round-off without touching semantics.
            output[-1]["max_score"] = round(
                float(output[-1]["max_score"])
                + (100.0 - sum(float(row.get("max_score") or 0) for row in output)),
                2,
            )
        return output
    target["id"] = "paper_route_fidelity"
    target["criterion_type"] = "route_fidelity"
    target["description"] = (
        "Follow the disclosed paper route, dependency order, method hierarchy, and validation "
        "sequence while reporting any unavoidable deviation."
    )
    target["evidence_artifacts"] = evidence_paths
    return output


def _ensure_public_boundary_markdown(path: Path, boundaries: Any) -> None:
    if not path.is_file() or not isinstance(boundaries, list) or not boundaries:
        return
    text = path.read_text(encoding="utf-8", errors="replace").rstrip()
    marker = "## Shared Public Boundary Conditions"
    if marker in text:
        return
    lines = ["", marker, ""]
    for row in boundaries:
        if not isinstance(row, dict) or row.get("value") in (None, ""):
            continue
        lines.append(f"- {row.get('name') or 'condition'}: {row['value']}")
    if len(lines) > 3:
        path.write_text(text + "\n" + "\n".join(lines) + "\n", encoding="utf-8")


def _hidden_reference_from_review(
    *,
    current: dict[str, Any],
    review: dict[str, Any],
    submission: dict[str, Any],
) -> dict[str, Any]:
    expected_truths = json.loads(
        json.dumps(review.get("ground_truth_items") or [], ensure_ascii=False)
    )
    current_truths = {
        str(row.get("ground_truth_id") or row.get("item_id") or ""): row
        for row in current.get("ground_truth_items") or []
        if isinstance(row, dict)
    }
    for truth in expected_truths:
        identifier = str(truth.get("ground_truth_id") or "")
        prior = current_truths.get(identifier) or {}
        if prior.get("acceptance_profile_id"):
            truth["acceptance_profile_id"] = prior["acceptance_profile_id"]
        if not truth.get("description") and prior.get("description"):
            truth["description"] = prior["description"]

    payload = {
        **current,
        "status": "ready",
        "task_pair_id": review.get("task_pair_id"),
        "ground_truth_items": expected_truths,
    }
    hidden = _normalize_hidden_reference_contract(payload)
    profiles_by_id = {
        str(row.get("acceptance_profile_id")): row
        for row in hidden.get("acceptance_profiles") or []
        if isinstance(row, dict)
    }
    truths_by_profile = {
        str(row.get("acceptance_profile_id")): row
        for row in hidden.get("ground_truth_items") or []
        if isinstance(row, dict)
    }
    for profile_id, profile in profiles_by_id.items():
        truth = truths_by_profile.get(profile_id) or {}
        profile_type = str(profile.get("type") or "")
        canonical = truth.get("canonical_answer")
        if profile_type in {"semantic_propositions", "mechanism_claim"}:
            projection: Any = {
                "required_propositions": truth.get("required_propositions") or [],
                "forbidden_contradictions": truth.get("forbidden_contradictions") or [],
            }
        else:
            projection = canonical
        profile["submission_binding"] = {
            "artifact_paths": _hidden_binding_artifact_paths(
                ground_truth_id=str(truth.get("ground_truth_id") or profile_id),
                submission_contract=submission,
            ),
            "observed_fields": ["$.results", "$.conclusions"],
            "canonical_projection": projection,
            "comparison": profile_type,
        }

    truths = hidden.get("ground_truth_items") or []
    count = len(truths)
    rubric: list[dict[str, Any]] = []
    if count:
        base, remainder = divmod(100, count)
        for index, truth in enumerate(truths):
            ground_truth_id = str(truth.get("ground_truth_id") or f"gt-{index + 1}")
            profile_id = str(truth.get("acceptance_profile_id") or "")
            description = str(
                truth.get("description")
                or f"Recover the source-supported scientific target {ground_truth_id}."
            )
            profile_type = str((profiles_by_id.get(profile_id) or {}).get("type") or "")
            rubric.append(
                {
                    "id": f"conclusion-{safe_component(ground_truth_id)}",
                    "max_score": base + (1 if index < remainder else 0),
                    "statement": description,
                    "acceptance_rule": (
                        f"Apply the item-specific {profile_type} acceptance profile {profile_id} "
                        "to the bound submitted artifacts."
                    ),
                    "required_evidence": _hidden_binding_artifact_paths(
                        ground_truth_id=ground_truth_id,
                        submission_contract=submission,
                    ),
                    "ground_truth_ids": [ground_truth_id],
                    "acceptance_profile_ids": [profile_id],
                }
            )
    hidden["scientific_conclusion_rubric"] = rubric
    hidden["expected_result"] = {
        "ground_truth_by_id": {
            str(row.get("ground_truth_id")): row.get("canonical_answer") for row in truths
        },
        "required_propositions_by_id": {
            str(row.get("ground_truth_id")): row.get("required_propositions") or []
            for row in truths
        },
    }
    summary = str(hidden.get("summary") or "").strip()
    if not summary or any(token in summary.casefold() for token in ("agent_required", "replace")):
        hidden["summary"] = str(
            review.get("workflow_summary")
            or review.get("scientific_question")
            or "Shared evidence-backed scientific scoring contract."
        )
    hidden.setdefault(
        "critical_failures",
        [
            "Fabricated computation or provenance.",
            "No real scientific computation supports the scored conclusions.",
        ],
    )
    hidden.setdefault("invalid_reasons", [])
    return hidden


def _normalize_task_pair_artifact_contracts(
    outputs: Path, review: dict[str, Any]
) -> list[str]:
    """Mechanically freeze pair invariants before strict semantic validation."""

    reproduction = outputs / "paper_reproduction"
    autonomous = outputs / "autonomous_research"
    if not reproduction.is_dir() or not autonomous.is_dir():
        return []
    try:
        reproduction_info = read_json(reproduction / "task_info.json")
        autonomous_info = read_json(autonomous / "task_info.json")
        reproduction_spec = read_json(reproduction / "task_spec.json")
        autonomous_spec = read_json(autonomous / "task_spec.json")
    except (OSError, ValueError, TypeError) as exc:
        return [f"pair_contract_normalization_unreadable:{type(exc).__name__}"]
    if not all(
        isinstance(value, dict)
        for value in (reproduction_info, autonomous_info, reproduction_spec, autonomous_spec)
    ):
        return ["pair_contract_normalization_json_invalid"]

    pair_id = str(review.get("task_pair_id") or "")
    scope = _canonical_workflow_scope(review.get("workflow_scope") or {})
    complexity = json.loads(
        json.dumps(review.get("complexity_profile") or {}, ensure_ascii=False)
    )
    public_basis = review.get("public_task_basis") or {}
    # The public task_info/task_spec pair must carry the same answer-free
    # scientific question.  Prefer the explicit public contract, but recover
    # the question already emitted by the Agent's task_spec when an older or
    # partial response omitted public_task_basis.  Do not fall back to private
    # review metadata here: task_info is part of the evaluator-facing bundle.
    pair_scientific_question = next(
        (
            str(value).strip()
            for value in (
                public_basis.get("scientific_question"),
                review.get("public_scientific_question"),
                autonomous_spec.get("scientific_question"),
                reproduction_spec.get("scientific_question"),
            )
            if str(value or "").strip()
        ),
        "",
    )
    common_spec = {
        "task_pair_id": pair_id,
        "scientific_question": pair_scientific_question,
        "target_definition": public_basis.get("target_definition")
        or public_basis.get("scientific_question")
        or review.get("public_scientific_question"),
        "boundary_conditions": public_basis.get("boundary_conditions") or [],
        "input_assets": _mode_asset_projection(public_basis),
        "workflow_scope": scope,
        "complexity_profile": complexity,
    }

    reproduction_submission = _normalize_submission_contract(
        _json_object(reproduction / "submission_contract.json")
    )
    autonomous_submission = _normalize_submission_contract(
        _json_object(autonomous / "submission_contract.json")
    )
    submission = (
        reproduction_submission
        if reproduction_submission.get("required_files")
        else autonomous_submission
    )
    if submission.get("required_files"):
        submission["task_pair_id"] = pair_id
        write_json(reproduction / "submission_contract.json", submission)
        write_json(autonomous / "submission_contract.json", submission)

    # Public evaluator metadata uses an anonymous stable key. Full DOI/title
    # provenance remains in the pair-level paper_info/source_manifest files.
    source_id = anonymous_source_id(pair_id)
    common_info = {
        "task_pair_id": pair_id,
        "scientific_question": pair_scientific_question,
        "source_id": source_id,
        "category": str(
            review.get("category")
            or reproduction_info.get("category")
            or autonomous_info.get("category")
            or "computational_chemistry"
        ),
        "benchmark_family": str(
            reproduction_info.get("benchmark_family")
            or autonomous_info.get("benchmark_family")
            or review.get("task_direction")
            or "computational_chemistry"
        ),
        "data": reproduction_info.get("data")
        or autonomous_info.get("data")
        or [
            {
                "name": "ResearchChemBench public inputs",
                "path": "data/inputs",
                "type": "directory",
                "description": "Public scientific inputs shared by both task modes.",
            }
        ],
        "archive_extractions": reproduction_info.get("archive_extractions")
        or autonomous_info.get("archive_extractions")
        or [],
        "workflow_scope": scope,
        "complexity_profile": complexity,
    }
    common_deliverables = (
        _normalize_required_deliverables(reproduction_info, submission)
        if submission.get("required_files")
        else []
    )

    for mode, info, spec in (
        ("paper_reproduction", reproduction_info, reproduction_spec),
        ("autonomous_research", autonomous_info, autonomous_spec),
    ):
        is_reproduction = mode == "paper_reproduction"
        task_id = f"{safe_component(pair_id)}_{'reproduction' if is_reproduction else 'autonomous'}"
        task_mode = "guided_reproduction" if is_reproduction else "open_discovery"
        disclosure = "paper_route_disclosed" if is_reproduction else "none"
        info.update(common_info)
        info.update(
            {
                "task_id": task_id,
                "mode": mode,
                "task_mode": task_mode,
                "scientific_mode": mode,
                "method_disclosure": disclosure,
                "pathway_disclosure": disclosure,
            }
        )
        if submission.get("required_files"):
            info["required_deliverables"] = json.loads(
                json.dumps(common_deliverables, ensure_ascii=False)
            )
        spec.update(common_spec)
        spec.update(
            {
                "task_id": task_id,
                "mode": mode,
                "task_mode": task_mode,
                "scientific_mode": mode,
                "method_disclosure": disclosure,
                "pathway_disclosure": disclosure,
            }
        )
        write_json((reproduction if is_reproduction else autonomous) / "task_info.json", info)
        write_json((reproduction if is_reproduction else autonomous) / "task_spec.json", spec)
        _ensure_public_boundary_markdown(
            (reproduction if is_reproduction else autonomous) / "task.md",
            common_spec["boundary_conditions"],
        )

    reproduction_data = reproduction / "data"
    autonomous_data = autonomous / "data"
    if reproduction_data.is_dir():
        copytree_exact(reproduction_data, autonomous_data)
    elif autonomous_data.is_dir():
        copytree_exact(autonomous_data, reproduction_data)
    for name in ("paper_route.md", "workflow_spec.json", "route_evidence_map.json"):
        (autonomous / name).unlink(missing_ok=True)

    reproduction_rubric_path = reproduction / "process_rubric.json"
    if reproduction_rubric_path.is_file():
        reproduction_rubric = _normalize_process_rubric(read_json(reproduction_rubric_path))
        reproduction_rubric = _ensure_reproduction_route_rubric(
            reproduction_rubric, submission=submission
        )
        write_json(reproduction_rubric_path, reproduction_rubric)
    autonomous_rubric_path = autonomous / "process_rubric.json"
    if autonomous_rubric_path.is_file():
        write_json(
            autonomous_rubric_path,
            _normalize_process_rubric(read_json(autonomous_rubric_path)),
        )

    base_hash = canonical_hash(
        [
            {"path": row["path"], "sha256": row["sha256"]}
            for row in directory_manifest(reproduction).get("files") or []
            if row.get("path") != "public_manifest.json"
        ]
    )
    # Derivation/source contracts are internal handoff metadata. Never place them
    # in either public evaluation mode; retain only the pair-level conversion report.
    for internal_name in (
        "derived_from.json",
        "conversion_contract.json",
        "conversion_receipt.json",
        "conversion_manifest.json",
    ):
        (autonomous / internal_name).unlink(missing_ok=True)
        (reproduction / internal_name).unlink(missing_ok=True)

    hidden_root = outputs / "hidden_reference"
    hidden_path = hidden_root / "ground_truth_common.json"
    if hidden_path.is_file() and submission.get("required_files"):
        current_hidden = _json_object(hidden_path)
        hidden = _hidden_reference_from_review(
            current=current_hidden,
            review=review,
            submission=submission,
        )
        write_json(hidden_path, hidden)
        write_json(hidden_root / "acceptance_profiles.json", hidden.get("acceptance_profiles") or [])
        write_json(
            hidden_root / "conclusion_rubric.json",
            hidden.get("scientific_conclusion_rubric") or [],
        )
        if not (hidden_root / "private_evidence_map.json").is_file():
            write_json(hidden_root / "private_evidence_map.json", review.get("evidence_map") or {})

    requirements = _normalize_toolbox_requirements(
        review.get("toolbox_requirements") or []
    )
    review["toolbox_requirements"] = requirements
    write_json(outputs / "workflow_review.json", review)
    write_json(outputs / "toolbox_requirements.json", requirements)
    return []


def _seed_prior_scientific_review_draft(
    *,
    stage_root: Path,
    paper_id: str,
    checkpoint: Path,
    attempt_root: Path,
    output_schema: dict[str, Any],
    semantic_validator: Callable[[dict[str, Any], Path], list[str]] | None,
) -> list[str] | None:
    """Stage a prior validated-shape review as an explicitly non-authoritative draft."""

    destination_outputs = attempt_root / "outputs"
    destination_artifact = destination_outputs / "scientific_review.json"
    source_authority = "previous_recovery_artifact"
    prior_fingerprint = ""
    try:
        response = read_json(destination_artifact)
        jsonschema.validate(response, output_schema)
    except (OSError, ValueError, jsonschema.ValidationError):
        if not checkpoint.is_file():
            return None
        try:
            cached = read_json(checkpoint)
            response = cached.get("response")
            if not isinstance(response, dict):
                return None
            jsonschema.validate(response, output_schema)
        except (OSError, ValueError, jsonschema.ValidationError):
            return None
        source_authority = "prior_checkpoint_revision_draft"
        prior_fingerprint = str(cached.get("input_fingerprint") or "")

        prior_artifact_root = (
            stage_root
            / "phase_artifacts"
            / safe_component(paper_id)
            / "scientific_review"
            / prior_fingerprint[:16]
        )
        source_outputs = prior_artifact_root / "outputs"
        if source_outputs.is_dir():
            copytree_exact(source_outputs, destination_outputs)
        else:
            destination_outputs.mkdir(parents=True, exist_ok=True)
    else:
        prior_artifact_root = attempt_root
    make_writable(destination_outputs)
    write_json(destination_artifact, response)

    findings = (
        semantic_validator(response, attempt_root) if semantic_validator is not None else []
    )
    write_json(
        attempt_root / "PRIOR_REVIEW_DRAFT_STATUS.json",
        {
            "authority": source_authority,
            "source_input_fingerprint": prior_fingerprint,
            "current_deterministic_findings": findings,
            "required_action": (
                "Verify changed fields against canonical inputs and rewrite "
                "outputs/scientific_review.json."
            ),
        },
    )
    return findings


def _interrupted_scientific_review_recovery(
    *, stage_root: Path, paper_id: str, snapshot_hash: str
) -> tuple[str, Path] | None:
    """Resume a failed review workspace when its immutable paper snapshot matches."""

    if not snapshot_hash:
        return None
    phase_root = (
        stage_root
        / "workspaces"
        / safe_component(paper_id)
        / "scientific_review"
    )
    if not phase_root.is_dir():
        return None
    attempts = sorted(
        (path for path in phase_root.glob("attempt-*") if path.is_dir()),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    for attempt in attempts:
        audit_path = attempt / "agent_run.json"
        snapshot_path = attempt / "inputs" / "snapshot_complete.json"
        if not audit_path.is_file() or not snapshot_path.is_file():
            continue
        audit = read_json(audit_path)
        snapshot = read_json(snapshot_path)
        if (
            audit.get("status") != "failed"
            or not audit.get("retryable")
            or snapshot.get("snapshot_hash") != snapshot_hash
        ):
            continue
        context = agent_recovery_context(SimpleNamespace(**audit))
        if context:
            return context, attempt
    return None


def _interrupted_phase_artifact_recovery(
    *,
    stage_root: Path,
    paper_id: str,
    phase: str,
    input_fingerprint_value: str,
) -> tuple[str, Path] | None:
    """Recover exact-input partial artifacts left by an interrupted Agent process."""

    phase_root = (
        stage_root
        / "workspaces"
        / safe_component(paper_id)
        / safe_component(phase)
    )
    if not phase_root.is_dir():
        return None
    attempts = sorted(
        (path for path in phase_root.glob("attempt-*") if path.is_dir()),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )
    for attempt in attempts:
        state_path = attempt / "phase_state.json"
        if not state_path.is_file():
            continue
        try:
            state = read_json(state_path)
        except (OSError, ValueError):
            continue
        if state.get("input_fingerprint") != input_fingerprint_value:
            continue
        artifacts = [
            path.relative_to(attempt).as_posix()
            for directory_name in ("outputs", "task")
            for path in (attempt / directory_name).rglob("*")
            if path.is_file()
            and not path.relative_to(attempt).as_posix().startswith("task/data/inputs/")
        ]
        if not artifacts:
            continue
        context = (
            "# Interrupted Agent Attempt\n\n"
            "The previous isolated process ended before returning a receipt. Its exact-input "
            "partial artifacts have been copied into this new isolated workspace. Continue "
            "from them; do not restart evidence collection.\n\n"
            "Failure class: interrupted_agent_process\n\n"
            "## Preserved partial artifacts\n\n"
            + "\n".join(f"- {path}" for path in artifacts[:80])
            + "\n"
        )
        return context, attempt
    return None


def _materialize_scientific_review_response(
    response: dict[str, Any], workspace: Path
) -> dict[str, Any]:
    """Persist the model's review contract and stage its referenced public assets."""

    contract = json.loads(json.dumps(response, ensure_ascii=False))
    public_root = workspace / "outputs" / "public_inputs"
    for asset in (contract.get("public_task_basis") or {}).get("input_assets") or []:
        try:
            logical = _normalize_public_input_path(str(asset.get("path") or ""))
        except ValueError:
            continue
        destination = public_root / logical
        content = asset.get("content")
        source_value = asset.get("content_path")
        if content is not None:
            write_text_asset(public_root, logical, _asset_content(content))
        elif source_value:
            try:
                source_relative = validate_relative_path(str(source_value))
                source = (workspace / source_relative).resolve()
                source.relative_to(workspace.resolve())
            except (ValueError, OSError):
                continue
            if not source.is_file():
                continue
            destination.parent.mkdir(parents=True, exist_ok=True)
            if source != destination.resolve():
                shutil.copy2(source, destination)
        else:
            continue
        asset.pop("content", None)
        asset["path"] = logical
        asset["content_path"] = destination.relative_to(workspace).as_posix()
    contract["artifact_path"] = "outputs/scientific_review.json"
    write_json(workspace / contract["artifact_path"], contract)
    return contract


def _materialize_hidden_response(
    response: dict[str, Any], workspace: Path
) -> dict[str, Any]:
    contract = json.loads(json.dumps(response, ensure_ascii=False))
    contract["artifact_path"] = "outputs/ground_truth_common.json"
    write_json(workspace / contract["artifact_path"], contract)
    return contract


def _hidden_reference_phase_findings(
    response: dict[str, Any],
    workspace: Path,
    *,
    review: dict[str, Any],
    submission_contract: dict[str, Any],
) -> list[str]:
    """Canonicalize syntax while keeping the review's scientific targets frozen."""

    normalized = _normalize_hidden_reference_contract(response)
    response.clear()
    response.update(normalized)
    artifact_path = str(response.get("artifact_path") or "outputs/ground_truth_common.json")
    try:
        relative = validate_relative_path(artifact_path)
    except ValueError:
        relative = "outputs/ground_truth_common.json"
        response["artifact_path"] = relative
    write_json(workspace / relative, response)
    if response.get("status") != "ready":
        return []
    return validate_hidden_reference(
        response,
        expected_ground_truth_items=review.get("ground_truth_items") or [],
        submission_contract=submission_contract,
    )


def _normalize_hidden_reference_contract(response: dict[str, Any]) -> dict[str, Any]:
    """Normalize common model aliases into the strict evaluator contract.

    This function only changes contract syntax. Canonical answers, propositions,
    evidence and scientific target identities remain untouched and are checked
    against the frozen scientific review by ``validate_hidden_reference``.
    """

    contract = json.loads(json.dumps(response, ensure_ascii=False))
    truths = [row for row in contract.get("ground_truth_items") or [] if isinstance(row, dict)]
    raw_profiles = [
        row for row in contract.get("acceptance_profiles") or [] if isinstance(row, dict)
    ]
    profiles_by_id = {
        str(row.get("acceptance_profile_id") or row.get("profile_id")): row
        for row in raw_profiles
        if row.get("acceptance_profile_id") or row.get("profile_id")
    }
    raw_references = [
        str(row.get("acceptance_profile_id") or row.get("acceptance_profile") or "")
        for row in truths
    ]
    reference_counts = {value: raw_references.count(value) for value in set(raw_references)}
    used_profile_ids: set[str] = set()
    profile_aliases: dict[str, list[str]] = {}
    normalized_profiles: list[dict[str, Any]] = []

    for index, truth in enumerate(truths, start=1):
        ground_truth_id = str(truth.get("ground_truth_id") or f"gt-{index}")
        raw_reference = str(
            truth.get("acceptance_profile_id") or truth.get("acceptance_profile") or ""
        )
        if raw_reference and reference_counts.get(raw_reference) == 1:
            profile_id = raw_reference
        else:
            profile_id = f"ap-{safe_component(ground_truth_id)}"
        base_profile_id = profile_id
        suffix = 2
        while profile_id in used_profile_ids:
            profile_id = f"{base_profile_id}-{suffix}"
            suffix += 1
        used_profile_ids.add(profile_id)
        if raw_reference:
            profile_aliases.setdefault(raw_reference, []).append(profile_id)

        profile = json.loads(
            json.dumps(profiles_by_id.get(raw_reference) or {}, ensure_ascii=False)
        )
        profile.pop("profile_id", None)
        profile["acceptance_profile_id"] = profile_id
        profile_type = str(truth.get("acceptance_type") or profile.get("type") or "")
        profile["type"] = profile_type
        parameters: dict[str, Any] = {}
        for source in (
            profile.get("default_parameters") or {},
            profile.get("parameters") or {},
            truth.get("acceptance_parameters") or {},
        ):
            if isinstance(source, dict):
                parameters.update(source)
        profile["parameters"] = parameters
        canonical_answer = truth.get("canonical_answer")
        propositions = truth.get("required_propositions") or []
        if not propositions and isinstance(canonical_answer, str) and canonical_answer.strip():
            propositions = [canonical_answer]

        if profile_type == "numeric_tolerance":
            profile["target"] = canonical_answer
            if parameters.get("unit") is not None:
                profile["unit"] = parameters["unit"]
            for key in ("absolute_tolerance", "relative_tolerance"):
                if parameters.get(key) is not None:
                    profile[key] = parameters[key]
            if (
                profile.get("absolute_tolerance") is None
                and profile.get("relative_tolerance") is None
            ):
                tolerance = next(
                    (
                        value
                        for key, value in parameters.items()
                        if str(key).startswith("tolerance")
                        and isinstance(value, (int, float))
                    ),
                    None,
                )
                if tolerance is not None:
                    profile["absolute_tolerance"] = tolerance
        elif profile_type == "categorical":
            profile["target"] = canonical_answer
        elif profile_type == "ranking":
            profile["target_order"] = canonical_answer
        elif profile_type == "trend":
            profile["required_trends"] = propositions or canonical_answer
        elif profile_type in {"structure_identity", "geometry_metric"}:
            profile["target"] = canonical_answer
        elif profile_type in {"mechanism_claim", "semantic_propositions"}:
            profile["required_propositions"] = propositions
            profile["forbidden_contradictions"] = truth.get("forbidden_contradictions") or []
        elif profile_type == "artifact_validation":
            profile["required_artifacts"] = (
                parameters.get("required_artifacts") or canonical_answer
            )

        truth.pop("acceptance_profile", None)
        truth["acceptance_profile_id"] = profile_id
        truth["applies_to_modes"] = ["autonomous_research", "paper_reproduction"]
        normalized_profiles.append(profile)

    profile_to_truth = {
        str(row.get("acceptance_profile_id")): str(row.get("ground_truth_id"))
        for row in truths
    }
    normalized_rubric: list[dict[str, Any]] = []
    for row in contract.get("scientific_conclusion_rubric") or []:
        if not isinstance(row, dict):
            normalized_rubric.append(row)
            continue
        criterion = json.loads(json.dumps(row, ensure_ascii=False))
        criterion["id"] = criterion.get("id") or criterion.get("claim_id")
        criterion["max_score"] = criterion.get("max_score") or criterion.get("weight")
        raw_profile_ids = criterion.get("acceptance_profile_ids") or []
        if not raw_profile_ids:
            singular = criterion.get("acceptance_profile_id") or criterion.get(
                "acceptance_profile"
            )
            raw_profile_ids = [singular] if singular else []
        expanded_profile_ids: list[str] = []
        for raw_profile_id in raw_profile_ids:
            expanded_profile_ids.extend(
                profile_aliases.get(str(raw_profile_id), [str(raw_profile_id)])
            )
        criterion["acceptance_profile_ids"] = list(dict.fromkeys(expanded_profile_ids))
        ground_truth_ids = criterion.get("ground_truth_ids") or []
        if not ground_truth_ids:
            singular_truth = criterion.get("ground_truth_id")
            if singular_truth:
                ground_truth_ids = [singular_truth]
            else:
                ground_truth_ids = [
                    profile_to_truth[profile_id]
                    for profile_id in criterion["acceptance_profile_ids"]
                    if profile_id in profile_to_truth
                ]
        criterion["ground_truth_ids"] = list(
            dict.fromkeys(str(value) for value in ground_truth_ids if str(value))
        )
        for alias in ("claim_id", "weight", "acceptance_profile", "acceptance_profile_id"):
            criterion.pop(alias, None)
        normalized_rubric.append(criterion)

    contract["ground_truth_items"] = truths
    contract["acceptance_profiles"] = normalized_profiles
    contract["scientific_conclusion_rubric"] = normalized_rubric
    return contract


def _reconcile_task_phase_receipt(
    receipt: dict[str, Any],
    *,
    workspace: Path,
    phase: str,
    result: Any,
) -> dict[str, Any]:
    """Reconcile a file-first builder receipt with the files actually written.

    Agent model state can lag behind a successful shell call. Complete artifacts are
    accepted and later undergo deterministic semantic validation. Partial artifacts
    are retryable so the next isolated workspace can finish them.
    """

    if not receipt.get("artifact_path"):
        # Mock and legacy direct-API adapters may return the task members inline;
        # _materialize_autonomous/_materialize_reproduction normalize that form.
        return receipt

    required = {
        "task.md",
        "task_info.json",
        "task_spec.json",
        "submission_contract.json",
        "process_rubric.json",
    }
    if phase == "paper_reproduction":
        required.update({"paper_route.md", "workflow_spec.json", "route_evidence_map.json"})
    task_root = workspace / "task"
    present = {
        path.relative_to(task_root).as_posix()
        for path in task_root.rglob("*")
        if task_root.is_dir() and path.is_file()
    }
    missing = sorted(required - present)
    if not missing:
        output = dict(receipt)
        if output.get("status") != "ready":
            output["receipt_reconciled_from_artifact"] = True
            output["summary"] = (
                "The complete task artifact superseded a stale terminal receipt; "
                "deterministic package validation remains mandatory."
            )
        output.update({"status": "ready", "artifact_path": "task", "invalid_reasons": []})
        return output

    phase_specific_present = present
    if phase == "paper_reproduction":
        phase_specific_present &= {"paper_route.md", "workflow_spec.json", "route_evidence_map.json"}
    if receipt.get("artifact_path") or phase_specific_present:
        message = f"Agent task artifact is partial; missing files: {', '.join(missing)}"
        result.status = "failed"
        result.failure_class = "partial_agent_artifact"
        result.retryable = True
        result.error = {"error_type": "PartialAgentArtifact", "message": message}
        write_json(workspace / "agent_run.json", result.audit_record())
        raise AgentExecutionError(
            message,
            failure_class="partial_agent_artifact",
            retryable=True,
            result=result,
        )
    return receipt


def _require_claimed_phase_artifact(
    receipt: dict[str, Any], workspace: Path, result: Any
) -> None:
    """Turn a positive receipt with no referenced artifact into a retryable Agent failure."""

    artifact_value = receipt.get("artifact_path")
    if not artifact_value or _receipt_is_terminal_negative(receipt):
        return
    try:
        relative = validate_relative_path(str(artifact_value))
        artifact = (workspace.resolve() / relative).resolve()
        artifact.relative_to(workspace.resolve())
    except (ValueError, OSError) as exc:
        message = f"Agent returned an unsafe artifact_path: {artifact_value!r}: {exc}"
    else:
        if artifact.exists():
            return
        message = f"Agent claimed a phase artifact that was not written: {relative}"

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
    )


def _copy_phase_inputs(
    source: Path,
    destination: Path,
    *,
    include_visual_fallback: bool = False,
) -> None:
    copytree_exact(source, destination)
    make_writable(destination)
    removed: list[str] = []
    # Keep one canonical upstream summary in the Agent-visible tree.  The complete
    # source snapshot remains immutable and is still used for provenance/publication.
    for relative in (
        "stage02_record.json",
        "stage02_hint.json",
        "stage03_record.json",
        "stage03_hint.json",
        "stage05_candidates.json",
        "stage05_hint.json",
        "output_manifest.json",
    ):
        candidate = destination / relative
        if candidate.is_file() or candidate.is_symlink():
            candidate.unlink()
            removed.append(relative)

    if not include_visual_fallback:
        # Stage06 normally has complete normalized/layout text plus deterministic table and
        # coordinate derivatives.  Raster images, parser-internal JSON and duplicate PDF copies
        # are therefore excluded from the Agent-visible packet by default.  They remain in the
        # immutable source snapshot and can be enabled for a paper whose evidence genuinely needs
        # visual fallback.
        for relative in ("main_paper.pdf", "supplementary"):
            candidate = destination / relative
            if candidate.is_dir():
                shutil.rmtree(candidate)
                removed.append(f"{relative}/:visual_fallback_excluded")
            elif candidate.is_file():
                candidate.unlink()
                removed.append(f"{relative}:visual_fallback_excluded")
        for document_root in (destination / "documents").glob("*"):
            if not document_root.is_dir():
                continue
            for relative in ("images", "parser_structured"):
                candidate = document_root / relative
                if candidate.is_dir():
                    shutil.rmtree(candidate)
                    removed.append(f"{candidate.relative_to(destination).as_posix()}/:visual_fallback_excluded")
    evidence_path = destination / "evidence_index.json"
    if evidence_path.is_file():
        try:
            full_index = read_json(evidence_path)
            write_json(
                evidence_path,
                _compact_agent_evidence_index(full_index),
            )
            removed.append("evidence_index.json:full_text_stripped")
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            pass
    write_json(
        destination / "visible_input_manifest.json",
        {
            "schema_version": "stage06-visible-input-manifest-v1",
            "source_snapshot": str(source),
            "removed_duplicate_materials": removed,
            "canonical_upstream_file": "upstream_hints.json",
            "evidence_index_mode": "metadata_with_previews",
            "visual_fallback": "included" if include_visual_fallback else "excluded_by_default",
        },
    )
    make_read_only(destination)


def _setup_converter_inputs(root: Path, source_pair: Path) -> None:
    """Give Stage06B the reproduction task plus a minimal conversion packet.

    Stage06B must know what to redact and which physical/public boundaries to preserve, but it
    does not need canonical answers, private evidence, or the complete Stage06A review.  The
    packet is an internal handoff and is never copied into either published task directory.
    """

    destination = root / "inputs" / "task_pair"
    destination.mkdir(parents=True, exist_ok=True)
    reproduction = source_pair / "paper_reproduction"
    if not reproduction.is_dir():
        raise FileNotFoundError("Stage06B reproduction task is unavailable")
    copytree_exact(reproduction, destination / "paper_reproduction")
    review = {}
    review_path = source_pair / "workflow_review.json"
    if review_path.is_file():
        try:
            review = read_json(review_path)
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            review = {}
    packet = destination / "conversion_packet"
    packet.mkdir(parents=True, exist_ok=True)
    public_basis = review.get("public_task_basis") or {}
    scope = dict(review.get("workflow_scope") or {})
    # Public conversion needs the scope shape, not the answer-bearing claims.
    scope.pop("supported_primary_claims", None)
    scope["autonomy_scope"] = "fixed_input_workflow_comparison"
    write_json(
        packet / "public_objective.json",
        {
            "schema_version": "stage06-public-objective-v1",
            "objective_id": review.get("objective_id"),
            "public_scientific_question": review.get("public_scientific_question")
            or review.get("scientific_question"),
            "workflow_scope": scope,
            "autonomy_scope": "fixed_input_workflow_comparison",
        },
    )
    input_assets = public_basis.get("input_assets") or []
    write_json(
        packet / "public_input_assets.json",
        [
            {
                key: asset.get(key)
                for key in ("asset_id", "path", "description", "role")
                if asset.get(key) not in (None, "", [])
            }
            for asset in input_assets
            if isinstance(asset, dict)
        ],
    )
    truths = review.get("ground_truth_items") or []
    write_json(
        packet / "key_point_ids.json",
        [
            {
                "key_point_id": row.get("ground_truth_id") or row.get("item_id"),
                "claim_role": row.get("claim_role") or "intermediate",
                "acceptance_type": row.get("acceptance_type") or "semantic_propositions",
            }
            for row in truths
            if isinstance(row, dict)
            and (row.get("ground_truth_id") or row.get("item_id"))
        ],
    )
    boundary_conditions = public_basis.get("boundary_conditions") or []
    write_json(
        packet / "preserve_boundary_conditions.json",
        [
            {
                **row,
                "classification": row.get("classification") or "needs_stage07_review",
            }
            if isinstance(row, dict)
            else {"value": row, "classification": "needs_stage07_review"}
            for row in boundary_conditions
        ],
    )
    write_json(
        packet / "route_redaction_map.json",
        {
            "files_to_remove": ["paper_route.md", "workflow_spec.json", "route_evidence_map.json"],
            "fields_to_rewrite": [
                "scientific_mode_description",
                "scientific_requirements",
                "input_assets[].description",
                "data[].description",
            ],
            "source_route_fields": [
                "software",
                "method",
                "method_parameters",
                "sequence",
                "route_steps",
                "validation_procedure",
            ],
            "answer_fields_to_remove": [
                "canonical_answer",
                "required_propositions",
                "forbidden_contradictions",
                "target",
                "target_order",
                "required_trends",
            ],
        },
    )
    write_json(
        packet / "asset_neutralization_map.json",
        [
            {
                "source_path": asset.get("path"),
                "public_identifier": f"candidate_{index}",
                "remove_source_label": True,
                "preserve_coordinate_rows": True,
            }
            for index, asset in enumerate(input_assets, start=1)
            if isinstance(asset, dict) and asset.get("path")
        ],
    )
    write_json(
        packet / "deliverable_contract.json",
        {
            "task_pair_id": review.get("task_pair_id"),
            "required_files": ["task.md", "task_info.json", "task_spec.json", "submission_contract.json", "process_rubric.json"],
            "preserve_submission_contract": True,
            "preserve_key_point_ids": True,
        },
    )
    make_read_only(destination)


def _ensure_objective_handoff_artifacts(pair_root: Path, review: dict[str, Any]) -> None:
    """Materialize lightweight objective contracts from the Agent review when omitted.

    This is a lossless transport fallback: it only projects fields already supplied by Stage06A
    and never invents a structure, parameter, result, or conclusion.
    """

    objective_path = pair_root / "objective_card.json"
    if not objective_path.is_file():
        objective = review.get("objective_card")
        if not isinstance(objective, dict):
            objective = {
                "objective_id": str(review.get("objective_id") or "objective-1"),
                "task_family": str(
                    review.get("task_family") or review.get("category") or "computational_chemistry"
                ),
                "scientific_question": review.get("scientific_question") or "",
                "public_question": review.get("public_scientific_question") or "",
                "problem_inputs": (review.get("public_task_basis") or {}).get(
                    "input_assets"
                ) or [],
                "unknowns": [],
                "selected_scope": review.get("workflow_scope") or {},
                "workflow_steps": review.get("workflow_steps") or [],
                "key_points": review.get("key_points") or review.get("ground_truth_items") or [],
                "final_claim": review.get("final_claim") or {},
                "evidence_ids": [],
            }
        write_json(objective_path, objective)
    key_points_path = pair_root / "key_points.json"
    if not key_points_path.is_file():
        points = review.get("key_points") or review.get("ground_truth_items") or []
        write_json(key_points_path, points if isinstance(points, list) else [])
    manifest_path = pair_root / "conversion_manifest.json"
    if not manifest_path.is_file():
        write_json(
            manifest_path,
            {
                "schema_version": "stage06-conversion-manifest-v1",
                "common_problem_inputs": [
                    row.get("path")
                    for row in ((review.get("public_task_basis") or {}).get("input_assets") or [])
                    if isinstance(row, dict) and row.get("path")
                ],
                "reproduction_route_assets": [
                    "paper_route.md",
                    "workflow_spec.json",
                    "route_evidence_map.json",
                ],
                "hidden_reference_assets": ["hidden_reference/"],
                "notes": "Generated from Stage06A fields; Stage06B must inspect all nested public files.",
            },
        )
    else:
        # Older builder prompts advertised a four-file autonomous allowlist.  That is
        # incompatible with recursive filename/XYZ/JSON disclosure cleanup, so normalize
        # only this transport field while preserving the Agent's scientific manifest fields.
        try:
            manifest = read_json(manifest_path)
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            manifest = {}
        if isinstance(manifest, dict):
            manifest["autonomous_editable_files"] = "recursive_autonomous_public_surface"
            manifest["conversion_scope"] = [
                "task.md",
                "task_info.json",
                "task_spec.json",
                "process_rubric.json",
                "submission_contract.json",
                "data/",
                "all nested filenames and metadata",
            ]
            write_json(manifest_path, manifest)


def _converter_phase_findings(response: dict[str, Any], workspace: Path) -> list[str]:
    """Check only the converter's file contract; scientific decisions remain with the Agents."""

    if response.get("status") not in {"converted", "conversion_uncertain"}:
        return []
    outputs = workspace / "outputs"
    autonomous = outputs / "autonomous_research"
    required = {
        "task.md",
        "task_info.json",
        "task_spec.json",
        "submission_contract.json",
        "process_rubric.json",
    }
    if not autonomous.is_dir():
        return ["autonomous_converter_artifact_missing"]
    present = {
        path.relative_to(autonomous).as_posix()
        for path in autonomous.rglob("*")
        if path.is_file()
    }
    findings = [f"autonomous_converter_missing:{name}" for name in sorted(required - present)]
    # conversion_report.json is optional internal telemetry.  Its absence must not trigger a
    # retry when the autonomous task tree itself was delivered successfully.
    _normalize_converter_report(response, workspace)
    return findings


def _normalize_converter_report(
    response: dict[str, Any], workspace: Path
) -> dict[str, Any] | None:
    """Normalize the converter's optional report into one pair-level handoff file.

    Agents occasionally return the report in their structured response, or write it below the
    autonomous task directory.  Both are equivalent mechanical delivery forms.  Recovering the
    report here prevents a response/file-placement mismatch from causing a retry, while keeping
    the report out of the public task directory.  This helper deliberately does not inspect the
    scientific content of the report.
    """

    outputs = workspace / "outputs"
    root_report = outputs / "conversion_report.json"
    candidates: list[Path] = [root_report, outputs / "autonomous_research" / "conversion_report.json"]
    report: dict[str, Any] | None = None
    for path in candidates:
        if not path.is_file():
            continue
        try:
            value = read_json(path)
        except (OSError, TypeError, ValueError, json.JSONDecodeError):
            continue
        if isinstance(value, dict):
            report = value
            break
    if report is None:
        value = response.get("conversion_report")
        if isinstance(value, dict):
            report = value
    if report is None:
        return None
    existing_root: Any = None
    if root_report.is_file():
        try:
            existing_root = read_json(root_report)
        except (OSError, TypeError, ValueError, json.JSONDecodeError):
            existing_root = None
    if existing_root != report:
        write_json(root_report, report)
    nested = outputs / "autonomous_research" / "conversion_report.json"
    if nested.is_file() and nested != root_report:
        nested.unlink(missing_ok=True)
    return report


def _persist_phase_artifacts(workspace: Path, destination: Path) -> None:
    available = [name for name in ("outputs", "task") if (workspace / name).is_dir()]
    if not available:
        return
    staging = prepare_clean_directory(destination.parent / f".{destination.name}-{uuid.uuid4().hex[:8]}")
    for name in available:
        copytree_exact(workspace / name, staging / name)
    atomic_commit_tree(staging, destination)


def _load_phase_json_artifact(
    receipt: dict[str, Any],
    workspace: Path | None,
    *,
    fallback: dict[str, Any],
) -> dict[str, Any]:
    artifact_value = receipt.get("artifact_path")
    if not artifact_value:
        return fallback
    if workspace is None:
        raise FileNotFoundError(f"phase artifact workspace missing: {artifact_value}")
    relative = validate_relative_path(str(artifact_value))
    path = (workspace / relative).resolve()
    workspace_root = workspace.resolve()
    if workspace_root not in path.parents:
        raise ValueError(f"phase artifact escapes workspace: {relative}")
    if not path.is_file() and _receipt_is_terminal_negative(receipt):
        return fallback
    if not path.is_file():
        raise FileNotFoundError(f"phase JSON artifact missing: {relative}")
    return read_json(path)


def _receipt_is_terminal_negative(receipt: dict[str, Any]) -> bool:
    return receipt.get("decision") in {
        "scientific_reject",
        "scientific_not_constructible",
    } or receipt.get("status") == "invalid"


def _hydrate_public_input_assets(review: dict[str, Any], workspace: Path | None) -> None:
    assets = (review.get("public_task_basis") or {}).get("input_assets") or []
    for asset in assets:
        if not isinstance(asset, dict):
            continue
        if asset.get("content") is not None:
            continue
        content_path = asset.get("content_path")
        if not content_path or workspace is None:
            continue
        relative = validate_relative_path(str(content_path))
        path = (workspace / relative).resolve()
        workspace_root = workspace.resolve()
        if workspace_root not in path.parents or not path.is_file():
            continue
        asset["content"] = path.read_text(encoding="utf-8", errors="strict")


def _scientific_review_phase_findings(
    response: dict[str, Any], workspace: Path, evidence_ids: set[str]
) -> list[str]:
    review = json.loads(json.dumps(response, ensure_ascii=False))
    _hydrate_public_input_assets(review, workspace)
    return validate_scientific_review(review, evidence_ids)


def _autonomous_phase_findings(
    workspace: Path,
    *,
    public_basis: dict[str, Any],
    review: dict[str, Any],
) -> list[str]:
    task_root = workspace / "task"
    findings = validate_task_boundary_conditions(
        task_root,
        expected_conditions=public_basis.get("boundary_conditions"),
    )
    findings.extend(
        validate_autonomous_route_isolation(
            task_root,
            paper_route=review.get("paper_route") or {},
            allowed_boundary_conditions=public_basis.get("boundary_conditions"),
        )
    )
    return sorted(set(findings))


def _setup_autonomous_inputs(
    root: Path,
    *,
    public_basis: dict[str, Any],
    toolbox_snapshot: dict[str, Any],
    task_pair_id: str,
) -> None:
    inputs = root / "inputs"
    inputs.mkdir(parents=True, exist_ok=True)
    write_json(inputs / "public_task_basis.json", _agent_public_basis(public_basis))
    write_json(
        inputs / "toolbox_snapshot.json",
        _compact_toolbox_snapshot(toolbox_snapshot, public_basis=public_basis),
    )
    write_json(
        inputs / "construction_contract.json",
        {
            "task_pair_id": task_pair_id,
            "mode": "autonomous_research",
            "hidden_reference_access": False,
            "paper_route_access": False,
            "toolbox_access": "read_only_snapshot",
        },
    )
    make_read_only(inputs)
    task_inputs = root / "task" / "data" / "inputs"
    task_inputs.mkdir(parents=True, exist_ok=True)
    for asset in public_basis.get("input_assets") or []:
        relative = _normalize_public_input_path(str(asset.get("path") or ""))
        if asset.get("content") is None:
            raise ValueError(f"public input content is missing: {relative}")
        write_text_asset(task_inputs, relative, _asset_content(asset.get("content")))
    make_read_only(task_inputs)


def _agent_public_basis(public_basis: dict[str, Any]) -> dict[str, Any]:
    """Remove large payload bodies after deterministic task input materialization."""

    output = json.loads(json.dumps(public_basis, ensure_ascii=False))
    for asset in output.get("input_assets") or []:
        relative = _normalize_public_input_path(str(asset.get("path") or ""))
        content = asset.pop("content", None)
        asset.pop("content_path", None)
        asset["path"] = relative
        asset["materialized_path"] = f"task/data/inputs/{relative}"
        if content is not None:
            encoded = _asset_content(content).encode("utf-8")
            asset["size_bytes"] = len(encoded)
    return output


def _compact_toolbox_snapshot(
    snapshot: dict[str, Any], *, public_basis: dict[str, Any]
) -> dict[str, Any]:
    """Expose only the installed-software inventory to the Agent."""

    del public_basis  # Software inventory is task-independent and intentionally complete.
    return installed_software_inventory(snapshot)


def _setup_reproduction_inputs(
    root: Path,
    *,
    autonomous_root: Path,
    review: dict[str, Any],
    base_manifest: dict[str, Any],
) -> None:
    copytree_exact(autonomous_root, root / "task")
    _write_reproduction_route_scaffold(
        root / "task",
        review=review,
    )
    private = root / "private_input"
    private.mkdir(parents=True, exist_ok=True)
    write_json(private / "paper_route.json", review.get("paper_route") or {})
    write_json(
        private / "modification_contract.json",
        {
            "base_manifest_hash": base_manifest["content_hash"],
            "hidden_reference_access": False,
            "allowed_files": sorted(_REPRODUCTION_ALLOWED_DIFFERENCES),
            "inputs_must_remain_identical": True,
            "conclusion_contract_must_remain_identical": True,
        },
    )
    (private / "apply_reproduction_patch.py").write_text(
        _reproduction_patch_script(), encoding="utf-8"
    )
    make_read_only(private)


def _reproduction_patch_script() -> str:
    """Return a task-agnostic helper for the reproduction Agent's mechanical edits."""

    return r'''from __future__ import annotations

import json
import re
from pathlib import Path


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, value) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


root = Path("task")
route = load(Path("private_input/paper_route.json"))
info = load(root / "task_info.json")
spec = load(root / "task_spec.json")
submission = load(root / "submission_contract.json")
rubric = load(root / "process_rubric.json")
pair_id = str(info.get("task_pair_id") or spec.get("task_pair_id") or "task")
task_id = pair_id + "_reproduction"
software = ", ".join(
    str(row.get("name") or "").strip()
    for row in route.get("software") or []
    if isinstance(row, dict) and str(row.get("name") or "").strip()
)
route_label = software or "the author-reported route"

task_path = root / "task.md"
task_text = task_path.read_text(encoding="utf-8")
lines = task_text.splitlines()
if lines and lines[0].startswith("# "):
    lines[0] = re.sub(
        r"Autonomous Research Task",
        "Paper Reproduction Task",
        lines[0],
        flags=re.IGNORECASE,
    )
task_text = "\n".join(lines).strip()
task_text = re.sub(
    r"(?im)^.*(?:open-ended research task|no software route or step order is prescribed).*$",
    "This is a guided reproduction task. Follow the frozen author route and do not substitute "
    "another software or method hierarchy for the primary reproduction.",
    task_text,
)
guide = f"""## Mandatory Paper Route

Follow `paper_route.md` and the dependencies in `workflow_spec.json` using {route_label}. Generate every target
quantity anew; route disclosure is not permission to copy paper results. Cite `route_evidence_map.json` when
describing author-reported settings, preserve failed attempts, and distinguish reproduced values from validation
cross-checks.
"""
if "## Mandatory Paper Route" not in task_text:
    first_break = task_text.find("\n")
    if first_break >= 0:
        task_text = task_text[:first_break] + "\n\n" + guide + "\n" + task_text[first_break + 1 :]
    else:
        task_text = task_text + "\n\n" + guide
task_path.write_text(task_text.rstrip() + "\n", encoding="utf-8")

existing_task = str(info.get("task") or info.get("description") or "").strip()
task_prefix = (
    "Perform a guided paper-route reproduction using paper_route.md and workflow_spec.json."
)
if not existing_task.startswith(task_prefix):
    existing_task = task_prefix + (" " + existing_task if existing_task else "")
info.update(
    {
        "task_id": task_id,
        "task_pair_id": pair_id,
        "mode": "paper_reproduction",
        "task_mode": "guided_reproduction",
        "scientific_mode": "paper_reproduction",
        "scientific_mode_description": (
            "Follow the frozen author-reported route in paper_route.md and workflow_spec.json, "
            "execute it independently, validate its outputs, and report all failures."
        ),
        "method_disclosure": "paper_route_disclosed",
        "pathway_disclosure": "paper_route_disclosed",
        "task": existing_task.strip(),
    }
)
if info.get("title"):
    info["title"] = re.sub(
        r"^Autonomous\s+",
        "Paper Reproduction ",
        str(info["title"]),
        flags=re.IGNORECASE,
    )
dump(root / "task_info.json", info)

spec.update(
    {
        "task_id": task_id,
        "task_pair_id": pair_id,
        "task_mode": "guided_reproduction",
        "mode": "paper_reproduction",
        "scientific_mode": "paper_reproduction",
        "method_disclosure": "paper_route_disclosed",
        "pathway_disclosure": "paper_route_disclosed",
        "route_files": [
            "paper_route.md",
            "workflow_spec.json",
            "route_evidence_map.json",
        ],
    }
)
dump(root / "task_spec.json", spec)

if not isinstance(rubric, list) or not rubric:
    raise ValueError("process_rubric.json must contain a non-empty criterion list")
criterion = next(
    (
        row
        for row in rubric
        if isinstance(row, dict)
        and (
            str(row.get("criterion_type") or "").casefold() == "route_fidelity"
            or str(row.get("id") or "").casefold()
            in {"paper_route_fidelity", "route_fidelity"}
        )
    ),
    None,
)
if criterion is None:
    raise ValueError("process_rubric.json lacks an explicit route_fidelity criterion")
criterion["id"] = "paper_route_fidelity"
criterion["criterion_type"] = "route_fidelity"
criterion["name"] = "Paper-route fidelity"
criterion["description"] = (
    "Follow the disclosed paper route, software, method hierarchy, dependencies, and validation "
    "sequence; document any unavoidable deviation without using hidden result agreement to select it."
)
required_files = [
    str(path)
    for path in submission.get("required_files") or []
    if str(path).strip()
]
evidence_paths = [
    path
    for path in required_files
    if any(
        token in path.casefold()
        for token in ("research_plan", "provenance", "trace", "report")
    )
]
if not evidence_paths:
    raise ValueError("submission contract has no plan, provenance, trace, or report artifact")
criterion["evidence"] = "; ".join(evidence_paths)
criterion["evidence_artifacts"] = evidence_paths
dump(root / "process_rubric.json", rubric)

print(
    json.dumps(
        {
            "task_id": task_id,
            "task_mode": info["task_mode"],
            "spec_mode": spec["mode"],
            "route_label": route_label,
            "rubric_total": sum(float(row.get("max_score") or 0) for row in rubric),
            "changed_files": [
                "task/task.md",
                "task/task_info.json",
                "task/task_spec.json",
                "task/process_rubric.json",
            ],
        },
        ensure_ascii=False,
    )
)
'''


def _public_reproduction_workflow_steps(review: dict[str, Any]) -> list[dict[str, Any]]:
    """Project private review steps into an answer-free, runtime-visible route graph."""

    route = review.get("paper_route") or {}
    route_rows = route.get("route_steps") or route.get("steps") or route.get("sequence") or []
    normalized_route_rows: list[dict[str, Any]] = []
    for index, row in enumerate(route_rows):
        if isinstance(row, dict):
            normalized_route_rows.append(row)
        else:
            normalized_route_rows.append(
                {"step": f"step-{index + 1}", "mapped_author_step": str(row)}
            )
    route_by_id = {
        str(row.get("step") or row.get("step_id") or ""): row
        for row in normalized_route_rows
        if row.get("step") or row.get("step_id")
    }
    public_inputs = [
        f"data/inputs/{_normalize_public_input_path(str(asset.get('path') or ''))}"
        for asset in _normalize_public_asset_declarations(
            (review.get("public_task_basis") or {}).get("input_assets")
        )
        if isinstance(asset, dict) and asset.get("path")
    ]
    output: list[dict[str, Any]] = []
    for index, source in enumerate(review.get("workflow_steps") or []):
        if not isinstance(source, dict):
            continue
        step_id = str(source.get("step_id") or f"step-{index + 1}")
        mapped = route_by_id.get(step_id)
        if mapped is None and index < len(normalized_route_rows):
            mapped = normalized_route_rows[index]
        mapped = mapped or {}
        action = str(
            mapped.get("mapped_author_step")
            or mapped.get("action")
            or mapped.get("description")
            or source.get("action")
            or ""
        ).strip()
        input_artifacts: list[str] = []
        for raw_value in source.get("input_artifacts") or []:
            value = str(raw_value)
            if value.startswith("outputs/public_inputs/"):
                value = "data/inputs/" + value.removeprefix("outputs/public_inputs/")
            elif "inputs/documents/" in value or re.search(
                r"\bcoordinates?-\d", value, flags=re.IGNORECASE
            ):
                value = "public input assets listed in $.public_input_assets"
            if value not in input_artifacts:
                input_artifacts.append(value)
        method_parameters = {}
        for key, value in (source.get("method_parameters") or {}).items():
            normalized_key = str(key).casefold().replace("-", "_")
            if any(
                marker in normalized_key
                for marker in (
                    "expected_result",
                    "ground_truth",
                    "paper_value",
                    "reference_value",
                    "primary_target",
                )
            ):
                continue
            method_parameters[key] = value
        output.append(
            {
                "step_id": step_id,
                "action": action,
                "depends_on": source.get("depends_on") or [],
                "input_artifacts": input_artifacts,
                "output_artifacts": source.get("output_artifacts") or [],
                "software": source.get("software") or route.get("software") or [],
                "method_parameters": method_parameters,
                "evidence_ids": sorted(
                    set(source.get("evidence_ids") or [])
                    | set(mapped.get("evidence_ids") or [])
                ),
            }
        )
    if public_inputs and output and not any(
        "$.public_input_assets" in str(value)
        or str(value).startswith("data/inputs/")
        for row in output
        for value in row.get("input_artifacts") or []
    ):
        output[0]["input_artifacts"] = [
            *output[0]["input_artifacts"],
            "public input assets listed in $.public_input_assets",
        ]
    return output


def _write_reproduction_route_scaffold(
    task_root: Path,
    *,
    review: dict[str, Any],
) -> None:
    """Render validated route facts before the Agent performs mode-specific editing."""

    route = review.get("paper_route") or {}
    task_pair_id = str(review.get("task_pair_id") or "")
    workflow_steps = _public_reproduction_workflow_steps(review)
    public_input_assets = [
        f"data/inputs/{_normalize_public_input_path(str(asset.get('path') or ''))}"
        for asset in _normalize_public_asset_declarations(
            (review.get("public_task_basis") or {}).get("input_assets")
        )
        if isinstance(asset, dict) and asset.get("path")
    ]
    workflow_spec = {
        "schema_version": "1.0",
        "task_pair_id": task_pair_id,
        "mode": "paper_reproduction",
        "route_completeness": route.get("route_completeness") or {},
        "software": route.get("software") or [],
        "method": route.get("method") or "",
        "method_parameters": route.get("method_parameters") or {},
        "sequence": route.get("sequence") or [],
        "route_steps": route.get("route_steps") or route.get("steps") or [],
        "adaptive_execution_controls": route.get("adaptive_execution_controls") or [],
        "validation_procedure": route.get("validation_procedure")
        or route.get("validation_notes")
        or "",
        "public_input_assets": public_input_assets,
        "workflow_steps": workflow_steps,
    }
    route_evidence = {
        "schema_version": "1.0",
        "task_pair_id": task_pair_id,
        "route_evidence_ids": sorted(
            set(_route_evidence_ids(route)) | set(_route_evidence_ids(workflow_steps))
        ),
        "software": [
            {
                "name": row.get("name"),
                "role": row.get("role"),
                "evidence_ids": row.get("evidence_ids") or [],
            }
            for row in route.get("software") or []
            if isinstance(row, dict)
        ],
        "workflow_steps": [
            {
                "step_id": row.get("step_id"),
                "evidence_ids": row.get("evidence_ids") or [],
            }
            for row in workflow_steps
            if isinstance(row, dict)
        ],
    }
    write_json(task_root / "workflow_spec.json", workflow_spec)
    write_json(task_root / "route_evidence_map.json", route_evidence)
    (task_root / "paper_route.md").write_text(
        _paper_route_markdown(task_pair_id, route), encoding="utf-8"
    )


def _paper_route_markdown(task_pair_id: str, route: dict[str, Any]) -> str:
    lines = [
        "# Paper Reproduction Route",
        "",
        f"Task pair: `{task_pair_id}`",
        "",
        "Follow this author-reported computational route. Compute all target results anew; "
        "this route contains no expected result values or conclusions.",
        "",
        "## Software",
        "",
    ]
    software = route.get("software") or []
    if software:
        for row in software:
            if isinstance(row, dict):
                evidence = ", ".join(
                    f"`{item}`" for item in row.get("evidence_ids") or []
                )
                suffix = f" Evidence: {evidence}." if evidence else ""
                lines.append(
                    f"- {row.get('name') or 'Unspecified software'}"
                    f" ({row.get('role') or 'compute'}).{suffix}"
                )
            else:
                lines.append(f"- {row}")
    else:
        lines.append("- See `workflow_spec.json` for the validated software contract.")
    lines.extend(["", "## Method", ""])
    if route.get("method"):
        lines.append(str(route["method"]))
    method_parameters = route.get("method_parameters") or {}
    if method_parameters:
        for key, value in method_parameters.items():
            lines.append(f"- **{key}:** {value}")
    if not route.get("method") and not method_parameters:
        lines.append("See `workflow_spec.json` for the structured method contract.")
    lines.extend(["", "## Workflow", ""])
    route_steps = route.get("route_steps") or route.get("steps") or route.get("sequence") or []
    for index, step in enumerate(route_steps, start=1):
        if isinstance(step, dict):
            description = (
                step.get("mapped_author_step")
                or step.get("action")
                or step.get("description")
                or ""
            )
        else:
            description = step
        lines.append(f"{index}. {description}")
    controls = route.get("adaptive_execution_controls") or []
    if controls:
        lines.extend(["", "## Adaptive Execution Controls", ""])
        for row in controls:
            if not isinstance(row, dict):
                continue
            lines.append(f"- **{row.get('control') or 'Control'}:** {row.get('procedure') or ''}")
            if row.get("stopping_rule"):
                lines.append(f"  Stopping rule: {row['stopping_rule']}")
    validation = route.get("validation_procedure") or route.get("validation_notes")
    if validation:
        lines.extend(["", "## Validation", "", str(validation)])
    completeness = route.get("route_completeness") or {}
    if completeness.get("closed_fields"):
        lines.extend(["", "## Closed Route Facts", ""])
        lines.extend(f"- {item}" for item in completeness["closed_fields"])
    return "\n".join(lines).rstrip() + "\n"


def _route_evidence_ids(value: Any) -> list[str]:
    output: list[str] = []
    if isinstance(value, dict):
        for key, nested in value.items():
            if key == "evidence_ids" and isinstance(nested, list):
                output.extend(str(item) for item in nested if str(item).startswith("ev_"))
            else:
                output.extend(_route_evidence_ids(nested))
    elif isinstance(value, list):
        for nested in value:
            output.extend(_route_evidence_ids(nested))
    return output


def _reproduction_phase_findings(
    workspace: Path,
    *,
    autonomous_root: Path,
    review: dict[str, Any],
) -> list[str]:
    task_root = workspace / "task"
    findings: list[str] = []
    for name in ("paper_route.md", "workflow_spec.json", "route_evidence_map.json"):
        path = task_root / name
        if not path.is_file() or path.stat().st_size == 0:
            findings.append(f"reproduction_route_artifact_missing:{name}")
    try:
        info = read_json(task_root / "task_info.json")
        spec = read_json(task_root / "task_spec.json")
        rubric = read_json(task_root / "process_rubric.json")
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        return [*findings, f"reproduction_core_json_invalid:{type(exc).__name__}"]
    if info.get("task_mode") != "guided_reproduction":
        findings.append("reproduction_task_mode_not_guided")
    if info.get("mode") != "paper_reproduction":
        findings.append("reproduction_info_mode_not_guided")
    if str(info.get("scientific_mode") or "") not in {
        "paper_reproduction",
        "guided_reproduction",
    }:
        findings.append("reproduction_scientific_mode_not_guided")
    if spec.get("mode") != "paper_reproduction":
        findings.append("reproduction_spec_mode_not_guided")
    if spec.get("task_mode") != "guided_reproduction":
        findings.append("reproduction_spec_task_mode_not_guided")
    if spec.get("scientific_mode") != "paper_reproduction":
        findings.append("reproduction_spec_scientific_mode_not_guided")
    if spec.get("task_id") != info.get("task_id"):
        findings.append("reproduction_mode_task_ids_differ")
    if spec.get("task_pair_id") != info.get("task_pair_id"):
        findings.append("reproduction_mode_pair_ids_differ")
    disclosure_text = json.dumps(
        {"info": info, "spec": spec}, ensure_ascii=False, sort_keys=True
    ).casefold()
    if "paper_route" not in disclosure_text and "paper route" not in disclosure_text:
        findings.append("reproduction_route_reference_missing")
    task_text = (task_root / "task.md").read_text(encoding="utf-8", errors="replace")
    if task_text == (autonomous_root / "task.md").read_text(
        encoding="utf-8", errors="replace"
    ):
        findings.append("reproduction_task_instruction_unchanged")
    if rubric == read_json(autonomous_root / "process_rubric.json"):
        findings.append("reproduction_process_rubric_unchanged")
    if not any(
        isinstance(row, dict)
        and str(row.get("criterion_type") or "").casefold() == "route_fidelity"
        for row in rubric
    ):
        findings.append("reproduction_route_fidelity_rubric_missing")
    if (
        directory_manifest(task_root / "data")["content_hash"]
        != directory_manifest(autonomous_root / "data")["content_hash"]
    ):
        findings.append("reproduction_phase_data_changed")
    return sorted(set(findings))


def _setup_hidden_inputs(
    root: Path,
    *,
    review: dict[str, Any],
    autonomous_root: Path,
    reproduction_root: Path,
    evidence_index: list[dict[str, Any]],
) -> None:
    inputs = root / "inputs"
    inputs.mkdir(parents=True, exist_ok=True)
    submission_contract = read_json(autonomous_root / "submission_contract.json")
    scaffold = _hidden_reference_scaffold(
        review=review,
        submission_contract=submission_contract,
    )
    write_json(inputs / "hidden_reference_scaffold.json", scaffold)
    write_json(
        inputs / "hidden_reference_packet.json",
        {
            "task_pair_id": review.get("task_pair_id"),
            "scientific_question": review.get("scientific_question"),
            "frozen_ground_truth_items": review.get("ground_truth_items") or [],
            "submission_contract": submission_contract,
            "allowed_modes": ["autonomous_research", "paper_reproduction"],
            "known_evidence_ids": sorted(
                {
                    str(evidence_id)
                    for item in review.get("ground_truth_items") or []
                    for evidence_id in item.get("evidence_ids") or []
                }
            ),
            "instructions": (
                "Replace only AGENT_REQUIRED scoring fields in the scaffold. Keep frozen "
                "targets, ids, evidence, modes, and public artifact paths unchanged."
            ),
        },
    )
    (inputs / "initialize_hidden_reference.py").write_text(
        _hidden_reference_initializer_script(), encoding="utf-8"
    )
    make_read_only(inputs)


def _hidden_reference_scaffold(
    *, review: dict[str, Any], submission_contract: dict[str, Any]
) -> dict[str, Any]:
    truths = json.loads(
        json.dumps(review.get("ground_truth_items") or [], ensure_ascii=False)
    )
    truth_ids = [str(item.get("ground_truth_id") or "") for item in truths]
    count = max(1, len(truths))
    base_weight, remainder = divmod(100, count)
    rubric = []
    for index, truth in enumerate(truths):
        ground_truth_id = str(truth.get("ground_truth_id") or f"gt-{index + 1}")
        profile_id = f"ap-{safe_component(ground_truth_id)}"
        rubric.append(
            {
                "id": f"conclusion-{safe_component(ground_truth_id)}",
                "max_score": base_weight + (1 if index < remainder else 0),
                "statement": f"AGENT_REQUIRED: describe the scored claim {ground_truth_id}",
                "acceptance_rule": (
                    f"AGENT_REQUIRED: apply {profile_id} to the bound submitted fields"
                ),
                "required_evidence": [
                    "Artifact-linked output produced by a real scientific computation."
                ],
                "ground_truth_ids": [ground_truth_id],
                "acceptance_profile_ids": [profile_id],
            }
        )
    scaffold = _normalize_hidden_reference_contract(
        {
            "status": "ready",
            "task_pair_id": review.get("task_pair_id"),
            "expected_result": {
                "ground_truth_by_id": {
                    str(item.get("ground_truth_id")): item.get("canonical_answer")
                    for item in truths
                },
                "required_propositions_by_id": {
                    str(item.get("ground_truth_id")): item.get("required_propositions") or []
                    for item in truths
                },
            },
            "ground_truth_items": truths,
            "acceptance_profiles": [],
            "scientific_conclusion_rubric": rubric,
            "critical_failures": [
                "Fabricated results or provenance.",
                "Hidden-answer copying instead of independent computation.",
                "No real scientific computation supporting the scored conclusions.",
                "Invalid chemical identity, charge, multiplicity, or electronic state.",
                "Unsupported scientific claims presented as computed evidence.",
            ],
            "summary": "AGENT_REQUIRED: summarize the shared scientific scoring contract",
            "invalid_reasons": [],
        }
    )
    truths_by_id = {
        str(item.get("ground_truth_id")): item for item in scaffold["ground_truth_items"]
    }
    for profile in scaffold["acceptance_profiles"]:
        profile_id = str(profile.get("acceptance_profile_id") or "")
        ground_truth_id = profile_id.removeprefix("ap-")
        truth = truths_by_id.get(ground_truth_id) or {}
        if profile.get("type") == "numeric_tolerance" and not profile.get("unit"):
            canonical = truth.get("canonical_answer")
            if isinstance(canonical, dict) and canonical.get("unit"):
                profile["unit"] = canonical["unit"]
        profile["submission_binding"] = {
            "artifact_paths": _hidden_binding_artifact_paths(
                ground_truth_id=ground_truth_id,
                submission_contract=submission_contract,
            ),
            "observed_fields": ["AGENT_REQUIRED: exact submitted field selectors"],
            "canonical_projection": truth.get("canonical_answer"),
            "comparison": "AGENT_REQUIRED: deterministic typed comparison",
        }
    if not truth_ids:
        scaffold["status"] = "invalid"
        scaffold["invalid_reasons"] = ["No frozen Ground Truth items were supplied."]
    return scaffold


def _hidden_binding_artifact_paths(
    *, ground_truth_id: str, submission_contract: dict[str, Any]
) -> list[str]:
    required = [str(path) for path in submission_contract.get("required_files") or []]
    identifier_tokens = {
        token
        for token in re.split(r"[^a-z0-9]+", ground_truth_id.casefold())
        if len(token) >= 4
    }
    ranked: list[tuple[int, int, str]] = []
    for index, path in enumerate(required):
        normalized = path.casefold()
        token_match = any(token in normalized for token in identifier_tokens)
        if token_match:
            priority = 0
        elif normalized.endswith("results.json"):
            priority = 1
        elif normalized.endswith((".csv", ".tsv", ".json")):
            priority = 2
        elif normalized.endswith((".md", ".txt")):
            priority = 3
        else:
            priority = 4
        ranked.append((priority, index, path))
    selected = [path for _, _, path in sorted(ranked)[:3]]
    return selected or ["AGENT_REQUIRED: select a required public artifact"]


def _hidden_reference_initializer_script() -> str:
    return r'''from __future__ import annotations

import json
import os
from pathlib import Path

root = Path(__file__).resolve().parent.parent
source = root / "inputs" / "hidden_reference_scaffold.json"
destination = root / "outputs" / "ground_truth_common.json"
destination.parent.mkdir(parents=True, exist_ok=True)
value = json.loads(source.read_text(encoding="utf-8"))
temporary = destination.with_suffix(".json.tmp")
temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
json.loads(temporary.read_text(encoding="utf-8"))
os.replace(temporary, destination)
print(json.dumps({
    "artifact": "outputs/ground_truth_common.json",
    "ground_truth_ids": [row["ground_truth_id"] for row in value["ground_truth_items"]],
    "acceptance_profile_ids": [row["acceptance_profile_id"] for row in value["acceptance_profiles"]],
    "fields_to_replace": ["submission_binding.observed_fields", "submission_binding.comparison", "rubric statement", "rubric acceptance_rule", "summary"],
}, ensure_ascii=False))
'''


def _public_basis(
    review: dict[str, Any], paper_id: str, task_pair_id: str, config: dict[str, Any]
) -> dict[str, Any]:
    basis = json.loads(json.dumps(review.get("public_task_basis") or {}, ensure_ascii=False))
    for asset in basis.get("input_assets") or []:
        asset["path"] = _normalize_public_input_path(str(asset.get("path") or ""))
    basis.update(
        {
            "paper_id": paper_id,
            "task_pair_id": task_pair_id,
            "scientific_question": review.get("public_scientific_question"),
            "task_direction": review.get("task_direction"),
            "category": review.get("category") or review.get("task_direction"),
            "resource_policy": config.get("resource_policy")
            or review.get("resource_assessment")
            or {},
        }
    )
    basis.pop("ground_truth", None)
    basis.pop("paper_route", None)
    return basis


def _materialize_autonomous(
    root: Path,
    response: dict[str, Any],
    *,
    public_basis: dict[str, Any],
    paper_id: str,
    task_pair_id: str,
    agent_workspace: Path | None = None,
) -> None:
    response = _load_task_artifacts(response, agent_workspace, reproduction=False)
    prepare_clean_directory(root)
    task_markdown = str(
        _normalize_evaluation_references(str(response.get("task_markdown") or ""))
    )
    submission_contract = _normalize_submission_contract(
        response.get("submission_contract") or {}
    )
    task_info = _normalized_task_info(
        response.get("task_info") or {},
        public_basis=public_basis,
        paper_id=paper_id,
        task_pair_id=task_pair_id,
        mode="autonomous_research",
        task_markdown=task_markdown,
        submission_contract=submission_contract,
    )
    task_spec = _normalized_task_spec(
        response.get("task_spec") or {},
        public_basis=public_basis,
        task_pair_id=task_pair_id,
        mode="autonomous_research",
    )
    # Older Agent responses may put the answer-free scientific question only in
    # task_spec.  Keep task_info and task_spec as one public contract without
    # copying private review fields into the evaluator-facing bundle.
    if not str(task_info.get("scientific_question") or "").strip():
        task_info["scientific_question"] = task_spec.get("scientific_question") or ""
    if not str(task_info.get("target_definition") or "").strip():
        task_info["target_definition"] = task_spec.get("target_definition") or ""
    write_json(root / "task_info.json", task_info)
    write_json(root / "task_spec.json", task_spec)
    write_json(root / "submission_contract.json", submission_contract)
    write_json(
        root / "process_rubric.json",
        _normalize_process_rubric(
            _normalize_evaluation_references(response.get("process_rubric") or [])
        ),
    )
    (root / "task.md").write_text(task_markdown, encoding="utf-8")
    inputs = root / "data" / "inputs"
    inputs.mkdir(parents=True, exist_ok=True)
    for asset in public_basis.get("input_assets") or []:
        relative = _normalize_public_input_path(str(asset.get("path") or ""))
        write_text_asset(inputs, relative, _asset_content(asset.get("content")))
    manifest = directory_manifest(root)
    write_json(root / "public_manifest.json", manifest)


def _materialize_reproduction(
    root: Path,
    response: dict[str, Any],
    *,
    autonomous_root: Path,
    paper_id: str,
    task_pair_id: str,
    base_manifest_hash: str,
    agent_workspace: Path | None = None,
) -> None:
    response = _load_task_artifacts(response, agent_workspace, reproduction=True)
    autonomous_info = read_json(autonomous_root / "task_info.json")
    autonomous_spec = read_json(autonomous_root / "task_spec.json")
    proposed_info = _normalize_evaluation_references(
        dict(response.get("task_info") or {})
    )
    proposed_spec = _normalize_evaluation_references(
        dict(response.get("task_spec") or {})
    )
    info = dict(autonomous_info)
    for field in ("task", "scientific_mode_description", "scientific_requirements"):
        if field in proposed_info:
            info[field] = proposed_info[field]
    info.update(
        {
            "task_id": f"{safe_component(task_pair_id)}_reproduction",
            "task_pair_id": task_pair_id,
            "mode": "paper_reproduction",
            "task_mode": "guided_reproduction",
            "scientific_mode": "paper_reproduction",
            "method_disclosure": "paper_route_disclosed",
            "pathway_disclosure": "paper_route_disclosed",
        }
    )
    frozen_spec_fields = {
        "task_pair_id",
        "scientific_question",
        "target_definition",
        "input_assets",
        "boundary_conditions",
    }
    spec = dict(autonomous_spec)
    spec.update(
        {
            key: value
            for key, value in proposed_spec.items()
            if key not in frozen_spec_fields
        }
    )
    spec.update(
        {
            "task_id": f"{safe_component(task_pair_id)}_reproduction",
            "task_pair_id": task_pair_id,
            "mode": "paper_reproduction",
            "task_mode": "guided_reproduction",
            "scientific_mode": "paper_reproduction",
            "method_disclosure": "paper_route_disclosed",
            "pathway_disclosure": "paper_route_disclosed",
        }
    )
    write_json(root / "task_info.json", info)
    write_json(root / "task_spec.json", spec)
    shutil.copy2(autonomous_root / "submission_contract.json", root / "submission_contract.json")
    write_json(
        root / "process_rubric.json",
        _normalize_process_rubric(
            _normalize_evaluation_references(response.get("process_rubric") or [])
        ),
    )
    (root / "task.md").write_text(
        str(_normalize_evaluation_references(response.get("task_markdown") or "")),
        encoding="utf-8",
    )
    (root / "paper_route.md").write_text(
        str(_normalize_evaluation_references(response.get("paper_route_markdown") or "")),
        encoding="utf-8",
    )
    write_json(
        root / "workflow_spec.json",
        _normalize_evaluation_references(response.get("workflow_spec") or {}),
    )
    write_json(
        root / "route_evidence_map.json",
        _normalize_evaluation_references(response.get("route_evidence_map") or {}),
    )
    # The mode directory is a public evaluation surface. Source/derivation
    # provenance belongs to the pair-level audit record, never in the task.
    for internal_name in (
        "derived_from.json",
        "conversion_contract.json",
        "conversion_receipt.json",
        "conversion_manifest.json",
    ):
        (root / internal_name).unlink(missing_ok=True)
    manifest = directory_manifest(root)
    write_json(root / "public_manifest.json", manifest)


def _load_task_artifacts(
    receipt: dict[str, Any], workspace: Path | None, *, reproduction: bool
) -> dict[str, Any]:
    if not receipt.get("artifact_path"):
        return receipt
    if workspace is None:
        raise FileNotFoundError("task artifact workspace missing")
    relative = validate_relative_path(str(receipt["artifact_path"]))
    task_root = (workspace / relative).resolve()
    workspace_root = workspace.resolve()
    if workspace_root not in task_root.parents or not task_root.is_dir():
        raise FileNotFoundError(f"task artifact directory missing: {relative}")
    required = {
        "task_info": "task_info.json",
        "task_markdown": "task.md",
        "task_spec": "task_spec.json",
        "submission_contract": "submission_contract.json",
        "process_rubric": "process_rubric.json",
    }
    if reproduction:
        required.update(
            {
                "paper_route_markdown": "paper_route.md",
                "workflow_spec": "workflow_spec.json",
                "route_evidence_map": "route_evidence_map.json",
            }
        )
    output = dict(receipt)
    for key, name in required.items():
        path = task_root / name
        if not path.is_file():
            raise FileNotFoundError(f"task artifact file missing: {relative}/{name}")
        output[key] = (
            path.read_text(encoding="utf-8", errors="strict")
            if path.suffix == ".md"
            else read_json(path)
        )
    return output


def _normalized_task_info(
    value: dict[str, Any],
    *,
    public_basis: dict[str, Any],
    paper_id: str,
    task_pair_id: str,
    mode: str,
    task_markdown: str,
    submission_contract: dict[str, Any],
) -> dict[str, Any]:
    output = _normalize_evaluation_references(dict(value))
    deliverable_descriptions: dict[str, str] = {}
    raw_deliverables = output.get("required_deliverables") or output.get("deliverables") or []
    if isinstance(raw_deliverables, list):
        for row in raw_deliverables:
            if not isinstance(row, dict):
                continue
            try:
                path = _normalize_runtime_artifact_path(str(row.get("path") or ""))
            except ValueError:
                continue
            deliverable_descriptions[path] = str(
                row.get("description") or row.get("kind") or row.get("role") or ""
            )
    required_files = submission_contract.get("required_files") or []
    output.update(
        {
            "task_id": f"{safe_component(task_pair_id)}_autonomous",
            "task_pair_id": task_pair_id,
            "source_id": anonymous_source_id(task_pair_id),
            "category": str(public_basis.get("category") or "computational_chemistry"),
            "mode": mode,
            "task_mode": "open_discovery",
            "scientific_mode": "autonomous_research",
            "method_disclosure": "none",
            "pathway_disclosure": "none",
            "task": str(output.get("task") or task_markdown).strip(),
            "required_deliverables": [
                {
                    "path": path,
                    "description": deliverable_descriptions.get(path, "Required task artifact."),
                    "allow_empty": False,
                }
                for path in required_files
            ],
        }
    )
    output.setdefault("benchmark_family", str(public_basis.get("task_direction") or ""))
    output.setdefault("scientific_requirements", [])
    output.pop("deliverables", None)
    output["data"] = [
        {
            "name": "ResearchChemBench public inputs",
            "path": "data/inputs",
            "type": "directory",
            "description": "Public structures, raw data, observations, and boundary conditions.",
        }
    ]
    output.setdefault("archive_extractions", [])
    return output


def _normalize_submission_contract(value: Any) -> dict[str, Any]:
    output = _normalize_evaluation_references(
        dict(value) if isinstance(value, dict) else {}
    )
    raw_paths = output.get("required_files")
    if not isinstance(raw_paths, list) or not raw_paths:
        raw_paths = []
        for row in output.get("required_artifacts") or []:
            if isinstance(row, dict):
                raw_paths.append(row.get("path"))
            elif isinstance(row, str):
                raw_paths.append(row)
        artifact_paths = output.get("artifact_paths")
        if isinstance(artifact_paths, dict):
            for row in artifact_paths.values():
                if isinstance(row, dict):
                    raw_paths.append(row.get("path"))
                elif isinstance(row, str):
                    raw_paths.append(row)
    required_files: list[str] = []
    for raw_path in raw_paths:
        try:
            path = _normalize_runtime_artifact_path(str(raw_path or ""))
        except ValueError:
            continue
        if path.endswith("/") or path in required_files:
            continue
        required_files.append(path)
    output["required_files"] = required_files
    # Keep the submission contract evaluator-loadable when an Agent only
    # supplied paths. The permissive schema is transport metadata; semantic
    # fields remain defined by the hidden acceptance profiles.
    output.setdefault("schema_version", "researchchembench.submission.v1")
    output.setdefault(
        "results_schema",
        {
            "type": "object",
            "description": "Structured report/results.json submitted by the evaluated agent.",
            "additionalProperties": True,
        },
    )
    return output


def _normalize_process_rubric(value: Any) -> list[dict[str, Any]]:
    rows = value.get("criteria") if isinstance(value, dict) else value
    if not isinstance(rows, list):
        return []
    output: list[dict[str, Any]] = []
    for index, row in enumerate(rows, start=1):
        if not isinstance(row, dict):
            continue
        normalized = dict(row)
        normalized["id"] = str(
            row.get("id") or row.get("criterion_id") or f"criterion_{index}"
        )
        normalized["max_score"] = row.get(
            "max_score", row.get("max_points", row.get("points", 0))
        )
        normalized["description"] = str(
            row.get("description") or row.get("criterion") or row.get("statement") or ""
        )
        output.append(normalized)
    return output


def _normalized_task_spec(
    value: dict[str, Any],
    *,
    public_basis: dict[str, Any],
    task_pair_id: str,
    mode: str,
) -> dict[str, Any]:
    output = _normalize_evaluation_references(dict(value))
    output.update(
        {
            "task_id": f"{safe_component(task_pair_id)}_autonomous",
            "task_pair_id": task_pair_id,
            "mode": mode,
            "task_mode": "open_discovery",
            "scientific_mode": "autonomous_research",
            "method_disclosure": "none",
            "pathway_disclosure": "none",
            "scientific_question": public_basis.get("scientific_question"),
            "target_definition": public_basis.get("target_definition")
            or public_basis.get("scientific_question"),
            "boundary_conditions": public_basis.get("boundary_conditions") or [],
            "input_assets": [
                {
                    key: (
                        f"data/inputs/{_normalize_public_input_path(str(asset.get('path') or ''))}"
                        if key == "path"
                        else asset.get(key)
                    )
                    for key in ("path", "description", "role", "source_evidence_ids")
                }
                for asset in public_basis.get("input_assets") or []
            ],
        }
    )
    return output


def _normalize_runtime_artifact_path(value: str) -> str:
    """Normalize an evaluated-Agent deliverable path to the execution workspace."""

    normalized = str(_normalize_evaluation_references(str(value or "")))
    return validate_relative_path(normalized)


def _normalize_evaluation_references(value: Any) -> Any:
    """Translate construction-workspace paths into evaluation-workspace paths."""

    if isinstance(value, dict):
        return {
            key: _normalize_evaluation_references(nested)
            for key, nested in value.items()
        }
    if isinstance(value, list):
        return [_normalize_evaluation_references(nested) for nested in value]
    if not isinstance(value, str):
        return value
    output = value.replace("task/data/inputs/", "data/inputs/")
    output = output.replace("task/data/inputs", "data/inputs")
    output = output.replace("task/inputs/", "data/inputs/")
    output = output.replace("task/inputs", "data/inputs")
    for prefix in ("outputs", "report", "results", "trace", "code"):
        output = output.replace(f"task/{prefix}/", f"{prefix}/")
        if output == f"task/{prefix}":
            output = prefix
    return output


def _normalize_public_input_path(value: str) -> str:
    """Return an asset path relative to the public task's inputs/ directory."""

    relative = validate_relative_path(value)
    while True:
        for prefix in ("inputs/", "public_inputs/"):
            if relative.startswith(prefix):
                relative = relative[len(prefix) :]
                break
        else:
            break
    return validate_relative_path(relative)


_REPRODUCTION_ALLOWED_DIFFERENCES = {
    "task.md",
    "task_info.json",
    "task_spec.json",
    "process_rubric.json",
    "paper_route.md",
    "workflow_spec.json",
    "route_evidence_map.json",
    "derived_from.json",
    "public_manifest.json",
}


def _reproduction_copy_findings(
    autonomous_root: Path,
    reproduction_root: Path,
    declared_modified_files: list[str],
) -> list[str]:
    findings: list[str] = []
    autonomous = directory_manifest(autonomous_root)
    reproduction = directory_manifest(reproduction_root)
    before = {row["path"]: row["sha256"] for row in autonomous["files"]}
    after = {row["path"]: row["sha256"] for row in reproduction["files"]}
    differences = {path for path in set(before) | set(after) if before.get(path) != after.get(path)}
    unauthorized = differences - _REPRODUCTION_ALLOWED_DIFFERENCES
    if unauthorized:
        findings.extend(f"reproduction_unauthorized_change:{path}" for path in sorted(unauthorized))
    if (
        directory_manifest(autonomous_root / "data")["content_hash"]
        != directory_manifest(reproduction_root / "data")["content_hash"]
    ):
        findings.append("reproduction_inputs_changed")
    normalized_declared = {
        str(path).removeprefix("task/") for path in declared_modified_files if str(path).strip()
    }
    if normalized_declared - _REPRODUCTION_ALLOWED_DIFFERENCES:
        findings.append("reproduction_declared_unauthorized_files")
    orchestrator_generated = {
        "derived_from.json",
        "public_manifest.json",
        "paper_route.md",
        "workflow_spec.json",
        "route_evidence_map.json",
    }
    undeclared = differences - normalized_declared - orchestrator_generated
    if undeclared:
        findings.extend(f"reproduction_undeclared_change:{path}" for path in sorted(undeclared))
    if read_json(autonomous_root / "submission_contract.json") != read_json(
        reproduction_root / "submission_contract.json"
    ):
        findings.append("mode_submission_contract_differs")
    return findings


def _materialize_pair_metadata(
    root: Path,
    *,
    paper_id: str,
    task_pair_id: str,
    documents: list[dict[str, Any]],
    stage04: dict[str, Any],
    candidates: list[dict[str, Any]],
    review: dict[str, Any],
    hidden: dict[str, Any],
    evidence_index: list[dict[str, Any]],
    snapshot: dict[str, Any],
    autonomous_root: Path,
    reproduction_root: Path,
    construction_harness,
    review_harness,
    phase_audits: dict[str, Any],
    mode_generation_order: list[str] | None = None,
    mode_generation_strategy: str = "legacy_multi_phase",
) -> None:
    # Stage06B may return a task_spec with the public question while omitting
    # the duplicated field in task_info.  Normalize this at the pair boundary
    # for both the legacy single-agent and converter paths.  The value comes
    # only from evaluator-facing task specs; private review text is never
    # copied into a public task directory.
    for mode_root in (autonomous_root, reproduction_root):
        info_path = mode_root / "task_info.json"
        spec_path = mode_root / "task_spec.json"
        if not (info_path.is_file() and spec_path.is_file()):
            continue
        info = _json_object(info_path)
        spec = _json_object(spec_path)
        changed = False
        for field in ("scientific_question", "target_definition"):
            if not str(info.get(field) or "").strip() and str(spec.get(field) or "").strip():
                info[field] = spec[field]
                changed = True
        if changed:
            write_json(info_path, info)
    write_json(
        root / "paper_info.json",
        {
            "paper_id": paper_id,
            "task_pair_id": task_pair_id,
            "doi": next((row.get("doi") for row in documents if row.get("doi")), None),
            "title": _paper_title(documents),
            "journal": next(
                (row.get("journal_name") for row in documents if row.get("journal_name")), None
            ),
            "documents": [_paper_document_metadata(row) for row in documents],
            "stage05_candidates": [row.get("candidate_id") for row in candidates],
            "stage05_candidate_disposition": review.get("stage05_candidate_disposition"),
            "selected_candidate_id": review.get("selected_candidate_id"),
            "workflow_scope": review.get("workflow_scope") or {},
            "complexity_profile": review.get("complexity_profile") or {},
            "agent_harness": construction_harness.name,
            "agent_model": construction_harness.model,
            "scientific_review_agent_model": review_harness.model,
            "construction_version": STAGE06_IMPLEMENTATION_VERSION,
            "constructed_at": now_utc(),
            "publication_governance": {
                "license_status": "unknown_not_assessed",
                "release_rights_status": "requires_separate_review",
                "source_access": "private_corpus",
            },
        },
    )
    write_json(root / "evidence_index.json", evidence_index)
    write_json(
        root / "source_manifest.json",
        {
            "snapshot_hash": snapshot["snapshot_hash"],
            "documents": snapshot["source_manifest"],
            "source_facts": snapshot.get("source_facts") or {},
            "stage04_record_hash": canonical_hash(stage04),
            "stage05_candidates_hash": canonical_hash(candidates),
        },
    )
    toolbox_requirements_path = root / "toolbox_requirements.json"
    if not toolbox_requirements_path.is_file():
        write_json(
            toolbox_requirements_path,
            _normalize_toolbox_requirements(review.get("toolbox_requirements") or []),
        )
    hidden_root = root / "hidden_reference"
    hidden_root.mkdir(parents=True, exist_ok=True)
    write_json(hidden_root / "ground_truth_common.json", hidden)
    write_json(hidden_root / "ground_truth_items.json", hidden.get("ground_truth_items") or [])
    write_json(hidden_root / "acceptance_profiles.json", hidden.get("acceptance_profiles") or [])
    write_json(
        hidden_root / "conclusion_rubric.json",
        hidden.get("scientific_conclusion_rubric") or [],
    )
    write_json(
        hidden_root / "disclosure_contract.json",
        {
            "schema_version": "1.0",
            "authority": "validated_stage06_scientific_review",
            "autonomous_allowed": {
                "public_scientific_question": review.get("public_scientific_question"),
                "public_task_basis": review.get("public_task_basis") or {},
            },
            "reproduction_additional_allowed": {
                "paper_route": review.get("paper_route") or {},
                "workflow_steps": _public_reproduction_workflow_steps(review),
            },
        },
    )
    write_json(
        hidden_root / "process_rubric_autonomous.json",
        read_json(autonomous_root / "process_rubric.json"),
    )
    write_json(
        hidden_root / "process_rubric_reproduction.json",
        read_json(reproduction_root / "process_rubric.json"),
    )
    shared_managed_policy = dict(hidden.get("managed_computation_policy") or {})
    # Keep shared evidence requirements separate from mode-specific route
    # policy.  A common policy must not accidentally say that autonomous work
    # follows the disclosed paper route.
    shared_managed_policy["mode_scope"] = "shared_conclusion_evidence"
    shared_managed_policy["route_policy_scope"] = "mode_specific"
    common = {
        "expected_tool_calls": [],
        "expected_result": hidden.get("expected_result") or {},
        "evaluation_mode": "dual_axis_100",
        "score_max": 100,
        "scientific_conclusion_rubric": hidden.get("scientific_conclusion_rubric") or [],
        "dual_axis_scoring_policy": {
            "formula": "scientific_conclusion_score * research_process_score / 100",
            "scientific_conclusion_score_max": 100,
            "research_process_score_max": 100,
            "final_score_max": 100,
            "unsupported_claim_policy": (
                "A conclusion without newly generated valid evidence receives no conclusion credit."
            ),
            "invalid_submission_policy": (
                "Fabricated evidence or hidden-answer leakage makes the submission invalid."
            ),
        },
        "critical_failures": evaluation_critical_failures(hidden),
        "reference_evidence": evaluation_reference_evidence(hidden),
        "evidence_gate_policy": hidden.get("evidence_gate_policy") or {},
        "managed_computation_policy": shared_managed_policy,
    }
    write_json(
        hidden_root / "ground_truth_autonomous.json",
        {
            **common,
            "evaluation_profile": "autonomous_discovery",
            "scoring_rubric": read_json(autonomous_root / "process_rubric.json"),
            "managed_computation_policy": {
                **shared_managed_policy,
                "mode": "autonomous_research",
                "route_disclosure": "not_required",
                "route_choice": "agent_selected",
            },
            "judge_instructions": (
                "Score autonomous scientific process and the shared hidden conclusions independently."
            ),
        },
    )
    write_json(
        hidden_root / "ground_truth_reproduction.json",
        {
            **common,
            "evaluation_profile": "paper_reproduction",
            "scoring_rubric": read_json(reproduction_root / "process_rubric.json"),
            "managed_computation_policy": {
                **shared_managed_policy,
                "mode": "paper_reproduction",
                "route_disclosure": "paper_route_required",
                "route_choice": "follow_disclosed_route",
            },
            "judge_instructions": (
                "Score fidelity to the disclosed paper route and the same shared hidden conclusions."
            ),
        },
    )
    write_json(
        root / "construction_record.json",
        {
            "paper_id": paper_id,
            "task_pair_id": task_pair_id,
            "implementation_version": STAGE06_IMPLEMENTATION_VERSION,
            "phase_audits": phase_audits,
            "toolbox_access": "read_only_snapshot",
            "mode_generation_order": mode_generation_order
            or ["autonomous_research", "paper_reproduction"],
            "mode_generation_strategy": mode_generation_strategy,
        },
    )


def _load_toolbox_snapshot(config: dict[str, Any], stage04: dict[str, Any]) -> dict[str, Any]:
    path_value = config.get("toolbox_capabilities")
    if path_value:
        path = Path(str(path_value)).expanduser().resolve()
        if path.is_file():
            return read_json(path)
    return {
        "profile_id": stage04.get("toolbox_profile_id"),
        "catalog_hash": stage04.get("toolbox_catalog_hash"),
        "software_mappings": stage04.get("software_mappings") or [],
        "snapshot_status": "stage04_facts_only",
    }


def _toolbox_requirement_status(requirement: dict[str, Any]) -> str:
    # Models often emit mutually exclusive boolean flags instead of a status
    # string.  Resolve those flags deterministically before applying aliases.
    if requirement.get("incompatible") is True:
        return "incompatible"
    if requirement.get("missing") is True:
        return "missing"
    if requirement.get("available") is True or requirement.get("installed") is True:
        return "available"
    if requirement.get("unknown") is True:
        return "unknown"
    raw = str(
        requirement.get("status") or requirement.get("availability") or "unknown"
    ).casefold()
    aliases = {
        "available": "available",
        "installed": "available",
        "present": "available",
        "supported": "available",
        "declared_supported": "available",
        "missing": "missing",
        "absent": "missing",
        "not_installed": "missing",
        "incompatible": "incompatible",
        "unsupported": "incompatible",
        "unknown": "unknown",
        "unverified": "unknown",
        "not_evaluated": "unknown",
    }
    return aliases.get(raw, "unknown")


def _normalize_toolbox_requirements(rows: Any) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    for row in rows if isinstance(rows, list) else []:
        if not isinstance(row, dict):
            continue
        normalized = dict(row)
        normalized["status"] = _toolbox_requirement_status(row)
        if not normalized.get("software"):
            normalized["software"] = (
                row.get("software_id")
                or row.get("display_name")
                or row.get("tool")
                or row.get("normalized_backend")
                or "unknown"
            )
        normalized.setdefault("capability", row.get("requirement") or "unspecified")
        normalized.setdefault("missing_capabilities", [])
        normalized.setdefault("incompatible_capabilities", [])
        normalized.setdefault("evidence_ids", [])
        output.append(normalized)
    return output


def _paper_document_metadata(
    document: dict[str, Any], *, parser_metadata: dict[str, Any] | None = None
) -> dict[str, Any]:
    output = {
        key: document.get(key)
        for key in (
            "document_id",
            "document_role",
            "file_name",
            "sha256",
            "size_bytes",
            "doi",
            "journal_name",
            "source_remote_uri",
            "source_dataset",
            "selected_parser",
            "quality",
            "article_url",
            "issn",
        )
    }
    parser_output = (parser_metadata or {}).get("parser_output") or {}
    for key in ("title", "abstract", "authors", "publication_date", "year"):
        if parser_output.get(key) not in (None, "", []):
            output[key] = parser_output[key]
    return output


def _parser_metadata(document: dict[str, Any]) -> dict[str, Any]:
    normalized = document.get("normalized_markdown_path")
    if normalized:
        metadata = Path(str(normalized)).expanduser().resolve().parent / "metadata.json"
        if metadata.is_file():
            return read_json(metadata)
    return {}


def _copy_parser_materials(
    *,
    parser_metadata: dict[str, Any],
    document_root: Path,
    snapshot_root: Path,
) -> list[dict[str, str]]:
    parser_output = parser_metadata.get("parser_output") or {}
    copied: list[dict[str, str]] = []
    if parser_metadata:
        write_json(document_root / "parser_metadata.json", parser_metadata)
        copied.append(
            {
                "kind": "parser_metadata",
                "path": str((document_root / "parser_metadata.json").relative_to(snapshot_root)),
            }
        )
    structured_root = document_root / "parser_structured"
    for key in (
        "content_list_v2_path",
        "content_list_path",
        "middle_json_path",
        "model_json_path",
    ):
        value = parser_output.get(key)
        if not value:
            continue
        source = Path(str(value)).expanduser().resolve()
        if not source.is_file():
            continue
        structured_root.mkdir(parents=True, exist_ok=True)
        target = structured_root / source.name
        shutil.copy2(source, target)
        copied.append({"kind": key, "path": str(target.relative_to(snapshot_root))})
    markdown_value = parser_output.get("markdown_path")
    if markdown_value:
        image_root = Path(str(markdown_value)).expanduser().resolve().parent / "images"
        if image_root.is_dir():
            target = document_root / "images"
            shutil.copytree(image_root, target, symlinks=False)
            copied.append({"kind": "mineru_images", "path": str(target.relative_to(snapshot_root))})
    return copied


_LAYOUT_COORDINATE_RE = re.compile(
    r"^\s*([A-Z][a-z]?)\s+"
    r"([+\-\N{MINUS SIGN}]?\d+(?:\.\d+)?(?:[Ee][+\-]?\d+)?)\s+"
    r"([+\-\N{MINUS SIGN}]?\d+(?:\.\d+)?(?:[Ee][+\-]?\d+)?)\s+"
    r"([+\-\N{MINUS SIGN}]?\d+(?:\.\d+)?(?:[Ee][+\-]?\d+)?)\s*$"
)
_GAUSSIAN_ORIENTATION_RE = re.compile(
    r"^\s*(\d+)\s+(\d+)\s+(-?\d+)\s+"
    r"([+\-\N{MINUS SIGN}]?\d+(?:\.\d+)?(?:[Ee][+\-]?\d+)?)\s+"
    r"([+\-\N{MINUS SIGN}]?\d+(?:\.\d+)?(?:[Ee][+\-]?\d+)?)\s+"
    r"([+\-\N{MINUS SIGN}]?\d+(?:\.\d+)?(?:[Ee][+\-]?\d+)?)\s*$"
)
_ATOMIC_SYMBOLS = (
    "",
    "H", "He", "Li", "Be", "B", "C", "N", "O", "F", "Ne",
    "Na", "Mg", "Al", "Si", "P", "S", "Cl", "Ar", "K", "Ca",
    "Sc", "Ti", "V", "Cr", "Mn", "Fe", "Co", "Ni", "Cu", "Zn",
    "Ga", "Ge", "As", "Se", "Br", "Kr", "Rb", "Sr", "Y", "Zr",
    "Nb", "Mo", "Tc", "Ru", "Rh", "Pd", "Ag", "Cd", "In", "Sn",
    "Sb", "Te", "I", "Xe", "Cs", "Ba", "La", "Ce", "Pr", "Nd",
    "Pm", "Sm", "Eu", "Gd", "Tb", "Dy", "Ho", "Er", "Tm", "Yb",
    "Lu", "Hf", "Ta", "W", "Re", "Os", "Ir", "Pt", "Au", "Hg",
    "Tl", "Pb", "Bi", "Po", "At", "Rn", "Fr", "Ra", "Ac", "Th",
    "Pa", "U", "Np", "Pu", "Am", "Cm", "Bk", "Cf", "Es", "Fm",
    "Md", "No", "Lr", "Rf", "Db", "Sg", "Bh", "Hs", "Mt", "Ds",
    "Rg", "Cn", "Nh", "Fl", "Mc", "Lv", "Ts", "Og",
)


def _extract_pdf_layout_materials(
    *,
    document: dict[str, Any],
    document_root: Path,
    snapshot_root: Path,
    document_id: str,
    document_role: Any,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    source_value = document.get("source_path")
    if not source_value:
        return [], []
    source = Path(str(source_value)).expanduser().resolve()
    if not source.is_file() or source.suffix.casefold() != ".pdf":
        return [], []
    try:
        reader = PdfReader(source)
        pages = [page.extract_text(extraction_mode="layout") or "" for page in reader.pages]
    except Exception:
        return [], []
    if not any(page.strip() for page in pages):
        return [], []

    pdf_hash = sha256_file(source)
    layout_path = document_root / "pypdf_layout.txt"
    layout_path.write_text(
        "\n\n".join(
            f"===== PDF PAGE {page_number} =====\n{text}"
            for page_number, text in enumerate(pages, start=1)
        ),
        encoding="utf-8",
    )
    materials: list[dict[str, Any]] = [
        {
            "kind": "pypdf_layout_text",
            "path": str(layout_path.relative_to(snapshot_root)),
            "pdf_sha256": pdf_hash,
            "extractor": f"pypdf-{pypdf_version}",
        }
    ]
    evidence: list[dict[str, Any]] = []
    coordinate_root = document_root / "derived_coordinates"
    coordinate_index: list[dict[str, Any]] = []
    for ordinal, block in enumerate(_layout_coordinate_blocks(pages), start=1):
        rows = block["rows"]
        label = str(block["label"])
        page_numbers = sorted({int(row[0]) for row in rows})
        xyz_rows = [
            f"{row[1]} {row[2]:.10g} {row[3]:.10g} {row[4]:.10g}" for row in rows
        ]
        formula = _atom_formula([str(row[1]) for row in rows])
        xyz = f"{len(rows)}\n{label}; source PDF pages {page_numbers[0]}-{page_numbers[-1]}\n"
        xyz += "\n".join(xyz_rows) + "\n"
        block_hash = canonical_hash(
            {
                "document_id": document_id,
                "pdf_sha256": pdf_hash,
                "label": label,
                "pages": page_numbers,
                "xyz_rows": xyz_rows,
            }
        )
        coordinate_root.mkdir(parents=True, exist_ok=True)
        target = coordinate_root / f"coordinates-{ordinal:03d}-{block_hash[:10]}.xyz"
        target.write_text(xyz, encoding="utf-8")
        relative_path = target.relative_to(snapshot_root)
        evidence_id = f"ev_derived_{safe_component(document_id)}_{block_hash[:16]}"
        source_ref = {
            "derivation": "pypdf_layout_strict_cartesian_rows_to_xyz",
            "source_pdf_sha256": pdf_hash,
            "source_pages": page_numbers,
            "extractor": f"pypdf-{pypdf_version}",
            "label_confidence": block.get("label_confidence") or "low",
            "coordinate_line_patterns": block.get("row_formats") or [],
            "introduced_values": [],
            "xyz_sha256": sha256_file(target),
        }
        evidence.append(
            {
                "evidence_id": evidence_id,
                "document_id": document_id,
                "document_role": document_role,
                "page": page_numbers[0],
                "section_path": ["Derived machine-readable coordinates", label],
                "block_type": "derived_coordinates",
                "text": (
                    f"{label}: {len(rows)} Cartesian-coordinate rows, formula {formula}, "
                    f"PDF pages {page_numbers[0]}-{page_numbers[-1]}. "
                    f"Machine-readable XYZ: {relative_path.as_posix()}"
                ),
                "source_ref": source_ref,
            }
        )
        coordinate_index.append(
            {
                "label": label,
                "path": relative_path.as_posix(),
                "atom_count": len(rows),
                "formula": formula,
                "source_pages": page_numbers,
                "label_confidence": block.get("label_confidence") or "low",
                "evidence_id": evidence_id,
                "source_ref": source_ref,
            }
        )
    if coordinate_index:
        write_json(coordinate_root / "index.json", coordinate_index)
        materials.append(
            {
                "kind": "derived_machine_readable_coordinates",
                "path": str(coordinate_root.relative_to(snapshot_root)),
                "count": len(coordinate_index),
            }
        )
    return evidence, materials


def _layout_coordinate_blocks(pages: list[str]) -> list[dict[str, Any]]:
    blocks: list[dict[str, Any]] = []
    active = False
    label = "Unlabeled coordinate block"
    label_confidence = "low"
    rows: list[tuple[int, str, float, float, float]] = []
    row_formats: set[str] = set()

    def flush() -> None:
        nonlocal rows, row_formats
        if len(rows) >= 3:
            blocks.append(
                {
                    "label": label,
                    "label_confidence": label_confidence,
                    "rows": rows,
                    "row_formats": sorted(row_formats),
                }
            )
        rows = []
        row_formats = set()

    for page_number, page in enumerate(pages, start=1):
        page_coordinate_count = sum(
            _layout_coordinate_row(line) is not None for line in page.splitlines()
        )
        page_has_coordinates = page_coordinate_count >= 1
        for line in page.splitlines():
            cleaned = " ".join(line.split()).strip()
            if re.search(r"(?i)(?:cartesian|atomic) coordinates", cleaned):
                if page_has_coordinates:
                    flush()
                    active = True
                    label = cleaned[:200]
                    label_confidence = "medium"
                continue
            if not active:
                continue
            if page_has_coordinates and _layout_state_geometry_label(cleaned):
                flush()
                label = cleaned[:200]
                label_confidence = "high"
                continue
            coordinate = _layout_coordinate_row(line)
            if coordinate is not None:
                element, x, y, z, row_format = coordinate
                rows.append((page_number, element, x, y, z))
                row_formats.add(row_format)
                continue
            if _layout_ignored_line(cleaned):
                continue
            if re.match(r"(?i)^(?:zero.point correction|thermal correction|sum of electronic)", cleaned):
                flush()
                continue
            if re.match(r"(?i)^\d+\.\s+(?:references|author contributions)", cleaned):
                flush()
                active = False
                continue
            if not rows and _layout_coordinate_label(cleaned):
                label = cleaned[:200]
                label_confidence = "medium"
    flush()
    return blocks


def _layout_coordinate_row(
    line: str,
) -> tuple[str, float, float, float, str] | None:
    match = _LAYOUT_COORDINATE_RE.match(line)
    if match:
        values = [
            float(value.replace("\N{MINUS SIGN}", "-"))
            for value in match.groups()[1:]
        ]
        return match.group(1), *values, "element_symbol_and_three_floats"
    match = _GAUSSIAN_ORIENTATION_RE.match(line)
    if not match:
        return None
    atomic_number = int(match.group(2))
    if atomic_number < 1 or atomic_number >= len(_ATOMIC_SYMBOLS):
        return None
    values = [
        float(value.replace("\N{MINUS SIGN}", "-"))
        for value in match.groups()[3:]
    ]
    return (
        _ATOMIC_SYMBOLS[atomic_number],
        *values,
        "gaussian_center_atomic_number_type_and_three_floats",
    )


def _layout_state_geometry_label(value: str) -> bool:
    normalized = value.casefold()
    return (
        "optimized" in normalized
        and "geometry" in normalized
        and any(token in normalized for token in ("ground state", "excited state", "equilibrium"))
    )


def _layout_ignored_line(value: str) -> bool:
    return not value or value.casefold() == "supporting information" or bool(
        re.fullmatch(r"\d+", value)
    )


def _layout_coordinate_label(value: str) -> bool:
    if not value or len(value) > 120 or re.search(r"[=:]", value):
        return False
    normalized = " ".join(value.split()).strip()
    if re.fullmatch(r"(?i)(?:page\s*)?[sivxlcdm-]*\d+(?:\s*(?:of|/)\s*\d+)?", normalized):
        return False
    if re.fullmatch(r"(?i)(?:figure|fig\.?|table|scheme)\s*[sivxlcdm-]*\d+[a-z]?", normalized):
        return False
    if re.search(
        r"(?i)^(?:supporting information|supplementary information|confidential|doi\b|https?://)",
        normalized,
    ):
        return False
    return bool(re.search(r"[A-Za-z]", normalized))


def _atom_formula(elements: list[str]) -> str:
    counts: dict[str, int] = {}
    for element in elements:
        counts[element] = counts.get(element, 0) + 1
    order = []
    for element in ("C", "H"):
        if element in counts:
            order.append(element)
    order.extend(sorted(element for element in counts if element not in {"C", "H"}))
    return "".join(f"{element}{counts[element] if counts[element] != 1 else ''}" for element in order)


def _optional_file_hash(value: Any) -> str | None:
    if not value:
        return None
    path = Path(str(value)).expanduser().resolve()
    return sha256_file(path) if path.is_file() else None


def _paper_title(documents: list[dict[str, Any]]) -> str | None:
    for document in documents:
        path_value = document.get("normalized_markdown_path")
        if not path_value:
            continue
        path = Path(str(path_value))
        if not path.is_file():
            continue
        for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
            value = line.strip().lstrip("#").strip()
            if len(value) >= 8:
                return value[:500]
    return None


class _TableTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.rows: list[list[str]] = []
        self._row: list[str] | None = None
        self._cell: list[str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        del attrs
        if tag.casefold() == "tr":
            self._row = []
        elif tag.casefold() in {"td", "th"} and self._row is not None:
            self._cell = []

    def handle_data(self, data: str) -> None:
        if self._cell is not None:
            self._cell.append(data)

    def handle_endtag(self, tag: str) -> None:
        normalized = tag.casefold()
        if normalized in {"td", "th"} and self._cell is not None and self._row is not None:
            value = " ".join("".join(self._cell).split())
            self._row.append(value)
            self._cell = None
        elif normalized == "tr" and self._row is not None:
            if any(cell for cell in self._row):
                self.rows.append(self._row)
            self._row = None


def _extract_markdown_tables(
    *,
    markdown_path: Path,
    document_root: Path,
    snapshot_root: Path,
    document_id: str,
    document_role: Any,
    canonical_blocks: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    if not markdown_path.is_file():
        return []
    markdown = markdown_path.read_text(encoding="utf-8", errors="replace")
    table_root = document_root / "derived_tables"
    table_root.mkdir(parents=True, exist_ok=True)
    evidence: list[dict[str, Any]] = []
    index: list[dict[str, Any]] = []
    parsed_tables: list[dict[str, Any]] = []
    html_matches = list(re.finditer(r"(?is)<table\b.*?</table>", markdown))
    source_tables: list[dict[str, Any]] = []
    for match in html_matches:
        source_tables.append(
            {
                "start": match.start(),
                "format": "html",
                "content": match.group(0),
            }
        )
    source_tables.extend(_markdown_pipe_tables(markdown))
    source_tables.sort(key=lambda row: int(row["start"]))
    rejected_sources: list[dict[str, Any]] = []
    for ordinal, source_table in enumerate(source_tables, start=1):
        if source_table["format"] == "html":
            parser = _TableTextParser()
            parser.feed(str(source_table["content"]))
            rows = parser.rows
        else:
            rows = source_table["rows"]
        if len(rows) < 2 or max((len(row) for row in rows), default=0) < 2:
            rejected_sources.append(
                {"ordinal": ordinal, "format": source_table["format"], "reason": "too_small"}
            )
            continue
        parsed_tables.append(
            {
                "caption": _table_caption(markdown, int(source_table["start"]), ordinal),
                "rows": rows,
                "source_table_ordinals": [ordinal],
                "source_formats": [source_table["format"]],
            }
        )
    for table in _merge_continuation_tables(parsed_tables):
        caption = str(table["caption"])
        rows, normalizations = _normalize_coordinate_atom_labels(
            table["rows"], caption=caption
        )
        ordinals = table["source_table_ordinals"]
        source_formats = sorted(set(table.get("source_formats") or []))
        tsv = "\n".join(
            "\t".join(_tsv_cell(cell) for cell in row)
            for row in rows
        ) + "\n"
        table_hash = canonical_hash(
            {
                "document_id": document_id,
                "caption": caption,
                "rows": rows,
                "source_table_ordinals": ordinals,
                "source_formats": source_formats,
                "normalizations": normalizations,
            }
        )
        stem = f"table-{int(ordinals[0]):03d}-{table_hash[:10]}"
        relative_path = Path("documents") / safe_component(document_id) / "derived_tables" / f"{stem}.tsv"
        target = snapshot_root / relative_path
        target.write_text(tsv, encoding="utf-8")
        source_ids = _caption_evidence_ids(caption, canonical_blocks)
        evidence_id = f"ev_derived_{safe_component(document_id)}_{table_hash[:16]}"
        record = {
            "evidence_id": evidence_id,
            "document_id": document_id,
            "document_role": document_role,
            "page": None,
            "section_path": ["Derived machine-readable tables", caption],
            "block_type": "derived_table",
            "text": (
                f"{caption}\nMachine-readable TSV: {relative_path.as_posix()}\n{tsv}"
            ),
            "source_ref": {
                "derivation": "deterministic_normalized_markdown_table_to_tsv",
                "normalized_markdown_path": str(markdown_path.relative_to(snapshot_root)),
                "source_evidence_ids": source_ids,
                "source_table_ordinals": ordinals,
                "source_formats": source_formats,
                "normalizations": normalizations,
                "table_sha256": sha256_file(target),
            },
        }
        evidence.append(record)
        index.append(
            {
                "caption": caption,
                "path": relative_path.as_posix(),
                "rows": len(rows),
                "max_columns": max(len(row) for row in rows),
                "evidence_id": evidence_id,
                "source_evidence_ids": source_ids,
                "source_table_ordinals": ordinals,
                "source_formats": source_formats,
                "normalizations": normalizations,
                "sha256": record["source_ref"]["table_sha256"],
            }
        )
    if index:
        write_json(table_root / "index.json", index)
    table_caption_count = len(
        re.findall(r"(?im)^\s*(?:#+\s*)?(?:supporting\s+)?table\s+[A-Z]?\d+\b", markdown)
    )
    unresolved_caption_count = max(0, table_caption_count - len(source_tables))
    coverage_status = (
        "failed"
        if source_tables and not parsed_tables
        else "partial"
        if rejected_sources or unresolved_caption_count
        else "complete"
    )
    write_json(
        table_root / "coverage.json",
        {
            "coverage_status": coverage_status,
            "source_format_counts": {
                "html": len(html_matches),
                "markdown_pipe": sum(
                    row.get("format") == "markdown_pipe" for row in source_tables
                ),
            },
            "table_caption_count": table_caption_count,
            "source_table_count": len(source_tables),
            "parsed_source_table_count": len(parsed_tables),
            "derived_table_count": len(index),
            "rejected_sources": rejected_sources,
            "unresolved_caption_count": unresolved_caption_count,
            "fallbacks": {
                "parser_structured_available": (document_root / "parser_structured").is_dir(),
                "layout_text_available": any(
                    (document_root / name).is_file()
                    for name in ("layout_text.txt", "pypdf_layout.txt")
                ),
                "table_images_available": (document_root / "images").is_dir(),
            },
        },
    )
    return evidence


def _markdown_pipe_tables(markdown: str) -> list[dict[str, Any]]:
    lines = markdown.splitlines(keepends=True)
    offsets: list[int] = []
    offset = 0
    for line in lines:
        offsets.append(offset)
        offset += len(line)
    tables: list[dict[str, Any]] = []
    index = 0
    while index + 1 < len(lines):
        header = _split_markdown_table_row(lines[index])
        separator = _split_markdown_table_row(lines[index + 1])
        if (
            len(header) < 2
            or len(separator) != len(header)
            or not all(re.fullmatch(r":?-{3,}:?", cell.strip()) for cell in separator)
        ):
            index += 1
            continue
        rows = [header]
        cursor = index + 2
        while cursor < len(lines):
            row = _split_markdown_table_row(lines[cursor])
            if len(row) != len(header):
                break
            rows.append(row)
            cursor += 1
        tables.append(
            {
                "start": offsets[index],
                "format": "markdown_pipe",
                "rows": rows,
            }
        )
        index = cursor
    return tables


def _split_markdown_table_row(line: str) -> list[str]:
    value = line.strip()
    if "|" not in value:
        return []
    value = value.removeprefix("|").removesuffix("|")
    cells = re.split(r"(?<!\\)\|", value)
    return [" ".join(cell.replace(r"\|", "|").split()) for cell in cells]


def _merge_continuation_tables(
    tables: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    merged: list[dict[str, Any]] = []
    for table in tables:
        current = {
            "caption": table["caption"],
            "rows": [list(row) for row in table["rows"]],
            "source_table_ordinals": list(table["source_table_ordinals"]),
            "source_formats": list(table.get("source_formats") or []),
        }
        if merged and _is_coordinate_continuation(merged[-1], current):
            merged[-1]["rows"].extend(current["rows"])
            merged[-1]["source_table_ordinals"].extend(
                current["source_table_ordinals"]
            )
            merged[-1]["source_formats"].extend(current["source_formats"])
            continue
        merged.append(current)
    return merged


def _is_coordinate_continuation(
    previous: dict[str, Any], current: dict[str, Any]
) -> bool:
    previous_caption = str(previous.get("caption") or "")
    current_caption = str(current.get("caption") or "")
    if "coordinate" not in previous_caption.casefold():
        return False
    if re.match(r"(?i)^table\s+[A-Z]?\d+\b", current_caption):
        return False
    current_rows = current.get("rows") or []
    previous_rows = previous.get("rows") or []
    if not current_rows or not previous_rows:
        return False
    if max(map(len, current_rows)) != max(map(len, previous_rows)):
        return False
    sample = current_rows[: min(5, len(current_rows))]
    return all(_looks_like_coordinate_row(row) for row in sample)


def _looks_like_coordinate_row(row: list[str]) -> bool:
    if len(row) < 4 or not re.fullmatch(r"[A-Za-z0-9]+", row[0].strip()):
        return False
    try:
        [float(value.strip()) for value in row[1:4]]
    except ValueError:
        return False
    return True


def _normalize_coordinate_atom_labels(
    rows: list[list[str]], *, caption: str
) -> tuple[list[list[str]], list[dict[str, Any]]]:
    """Repair only high-confidence O/0 OCR errors in an atomic-coordinate label column."""

    normalized = [list(row) for row in rows]
    if "coordinate" not in caption.casefold():
        return normalized, []
    header_index = next(
        (
            index
            for index, row in enumerate(normalized)
            if row and row[0].strip().casefold() in {"atom", "element", "label"}
        ),
        None,
    )
    if header_index is None:
        return normalized, []
    corrections: list[dict[str, Any]] = []
    for index in range(header_index + 1, len(normalized)):
        row = normalized[index]
        if len(row) < 4:
            continue
        match = re.fullmatch(r"0(\d+)", row[0].strip())
        if not match:
            continue
        atom_number = int(match.group(1))
        previous_number = _atom_label_number(normalized[index - 1][0]) if index > 0 else None
        next_number = (
            _atom_label_number(normalized[index + 1][0])
            if index + 1 < len(normalized) and normalized[index + 1]
            else None
        )
        if previous_number != atom_number - 1 or next_number != atom_number + 1:
            continue
        original = row[0]
        corrected = f"O{match.group(1)}"
        row[0] = corrected
        corrections.append(
            {
                "row_number": index + 1,
                "column": "Atom",
                "original": original,
                "normalized": corrected,
                "rule": "leading_zero_to_oxygen_between_sequential_atom_labels",
            }
        )
    return normalized, corrections


def _atom_label_number(value: str) -> int | None:
    match = re.fullmatch(r"[A-Za-z]+(\d+)", str(value).strip())
    return int(match.group(1)) if match else None


def _table_caption(markdown: str, table_start: int, ordinal: int) -> str:
    prefix = markdown[max(0, table_start - 1500) : table_start]
    lines = [line.strip() for line in prefix.splitlines() if line.strip()]
    for line in reversed(lines):
        cleaned = re.sub(r"<[^>]+>", " ", line)
        cleaned = " ".join(cleaned.split())
        if re.match(r"(?i)^(?:table|supporting table)\b", cleaned):
            return cleaned[:500]
        if cleaned and not cleaned.startswith("!["):
            return cleaned[:500]
    return f"Uncaptioned table {ordinal}"


def _caption_evidence_ids(
    caption: str, canonical_blocks: list[dict[str, Any]]
) -> list[str]:
    label_match = re.search(r"(?i)\btable\s+[A-Z]?\d+\b", caption)
    needle = (label_match.group(0) if label_match else caption[:80]).casefold()
    output = []
    for block in canonical_blocks:
        text = str(block.get("text") or "").casefold()
        evidence_id = str(block.get("evidence_id") or block.get("block_id") or "")
        if evidence_id and needle and needle in text:
            output.append(evidence_id)
    return sorted(set(output))


def _tsv_cell(value: str) -> str:
    return " ".join(str(value).replace("\t", " ").replace("\r", " ").splitlines()).strip()


def _upstream_hints(
    *,
    paper_id: str,
    candidates: list[dict[str, Any]],
    stage02: dict[str, Any] | None,
    stage03: dict[str, Any] | None,
    stage04: dict[str, Any],
) -> dict[str, Any]:
    """Return one compact, explicitly non-binding upstream hint file.

    The previous snapshot wrote the same Stage02/03/05 data as both ``record`` and
    ``hint`` files.  Keeping one compact copy preserves provenance without encouraging
    the Agent to compare duplicate representations.
    """

    return {
        "schema_version": "stage06-upstream-hints-v1",
        "non_binding": True,
        "paper_id": paper_id,
        "stage02": _compact_upstream_record(stage02),
        "stage03": _compact_upstream_record(stage03),
        "stage04": {
            key: stage04.get(key)
            for key in (
                "paper_id",
                "processing_status",
                "coverage_status",
                "parser_status",
                "document_count",
                "evidence_count",
            )
            if key in stage04
        },
        "stage05_candidates": candidates,
        "source_hashes": {
            "stage02": canonical_hash(stage02 or {}),
            "stage03": canonical_hash(stage03 or {}),
            "stage05_candidates": canonical_hash(candidates),
            "stage04": canonical_hash(stage04),
        },
    }


def _compact_agent_evidence_index(value: Any, *, preview_chars: int = 720) -> list[dict[str, Any]]:
    """Strip repeated block bodies while retaining navigable evidence metadata."""

    rows = value if isinstance(value, list) else []
    compact: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        item = {
            key: row.get(key)
            for key in (
                "evidence_id",
                "document_id",
                "document_role",
                "page",
                "section_path",
                "block_type",
                "source_ref",
            )
            if key in row
        }
        text = str(row.get("text") or "")
        if text:
            item["text_preview"] = text[:preview_chars]
        compact.append(item)
    return compact


def _write_dedup_report(root: Path) -> dict[str, Any]:
    """Write a factual file-level duplicate report for the immutable snapshot."""

    groups: dict[str, list[dict[str, Any]]] = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.name in {"dedup_report.json", "snapshot_complete.json"}:
            continue
        try:
            digest = sha256_file(path)
            size = path.stat().st_size
        except OSError:
            continue
        groups.setdefault(digest, []).append(
            {"path": str(path.relative_to(root)), "size": size}
        )
    duplicate_groups = [rows for rows in groups.values() if len(rows) > 1]
    duplicate_bytes = sum(
        sum(int(row["size"]) for row in rows[1:]) for rows in duplicate_groups
    )
    report = {
        "schema_version": "stage06-dedup-report-v1",
        "duplicate_group_count": len(duplicate_groups),
        "duplicate_file_count": sum(len(rows) - 1 for rows in duplicate_groups),
        "duplicate_bytes_avoided": duplicate_bytes,
        "groups": duplicate_groups,
    }
    write_json(root / "dedup_report.json", report)
    return report


def _priority_review_packet(
    *,
    candidates: list[dict[str, Any]],
    stage02: dict[str, Any] | None,
    stage03: dict[str, Any] | None,
    evidence_index: list[dict[str, Any]],
) -> dict[str, Any]:
    requested = _collect_evidence_ids({"candidates": candidates, "stage02": stage02, "stage03": stage03})
    by_document: dict[str, list[dict[str, Any]]] = {}
    for block in evidence_index:
        by_document.setdefault(str(block.get("document_id") or ""), []).append(block)
    selected: dict[str, dict[str, Any]] = {}
    for blocks in by_document.values():
        positions = {
            str(block.get("evidence_id") or ""): index for index, block in enumerate(blocks)
        }
        for evidence_id in requested:
            if evidence_id not in positions:
                continue
            center = positions[evidence_id]
            for block in blocks[max(0, center - 2) : min(len(blocks), center + 3)]:
                selected[str(block["evidence_id"])] = block
    keyword_pattern = (
        "computational details",
        "cartesian coordinates",
        "fractional atomic coordinates",
        "atomic coordinates",
        "unit cell",
        "cell parameters",
        "space group",
        "geometry optimization",
        "vibration analysis",
        "frequency calculations",
        "table 3:",
        "table s1",
        "table s2",
        "table s3",
    )
    for block in evidence_index:
        text = str(block.get("text") or "").casefold()
        if any(keyword in text for keyword in keyword_pattern):
            selected[str(block["evidence_id"])] = block
    document_index = []
    for document_id, blocks in sorted(by_document.items()):
        roles = sorted({str(block.get("document_role") or "unknown") for block in blocks})
        document_index.append(
            {
                "document_id": document_id,
                "document_roles": roles,
                "block_count": len(blocks),
                "first_evidence_id": blocks[0].get("evidence_id") if blocks else None,
                "last_evidence_id": blocks[-1].get("evidence_id") if blocks else None,
                "priority_block_count": sum(
                    1 for block in blocks if str(block.get("evidence_id")) in selected
                ),
            }
        )
    ordered_selected = _compact_agent_evidence_index(
        [
            block
            for block in evidence_index
            if str(block.get("evidence_id") or "") in selected
        ],
        preview_chars=960,
    )
    return {
        "purpose": "Start here; use full documents only for explicitly unresolved fields.",
        "data_contract": {
            "canonical_evidence_source": "evidence_index.json and documents/*/content_blocks.jsonl",
            "normalized_document_role": "readable full-text fallback preserving nearby context",
            "parser_structured_role": "layout/table fallback; parser files may not carry canonical evidence IDs",
            "citation_rule": "Use only evidence IDs present in the canonical evidence source.",
            "priority_blocks_are_previews": True,
        },
        "document_index": document_index,
        "stage05_candidates": candidates,
        "stage02_summary": _compact_upstream_record(stage02),
        "stage03_summary": _compact_upstream_record(stage03),
        "requested_evidence_ids": sorted(requested),
        "evidence_blocks": ordered_selected,
    }


def _collect_evidence_ids(value: Any) -> set[str]:
    output: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            if key == "evidence_id" and isinstance(item, str):
                output.add(item)
            elif key == "evidence_ids" and isinstance(item, list):
                output.update(str(entry) for entry in item if entry)
            else:
                output.update(_collect_evidence_ids(item))
    elif isinstance(value, list):
        for item in value:
            output.update(_collect_evidence_ids(item))
    return output


def _compact_upstream_record(value: dict[str, Any] | None) -> dict[str, Any]:
    if not value:
        return {}
    keys = (
        "decision",
        "review",
        "pass_verification",
        "workflow_inventory",
        "software_mentions",
        "resource_profile",
        "toolbox_profile_id",
        "toolbox_catalog_hash",
    )
    return {key: value.get(key) for key in keys if key in value}


def _asset_content(value: Any) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def _write_mode_public_manifest(root: Path) -> None:
    (root / "public_manifest.json").unlink(missing_ok=True)
    write_json(root / "public_manifest.json", directory_manifest(root))


def _resource_risk_present(value: dict[str, Any]) -> bool:
    status = str(value.get("status") or value.get("cost_status") or "").casefold()
    return status in {
        "uncertain",
        "over_budget",
        "resource_risk",
        "model_estimated_high",
        "infeasible",
    } or bool(value.get("risk_present"))


def _write_provisional_handoff_metadata(
    root: Path,
    *,
    paper_id: str,
    task_pair_id: str,
    decision: str,
    documents: list[dict[str, Any]],
    candidates: list[dict[str, Any]],
    review: dict[str, Any],
    receipt: dict[str, Any],
    snapshot: dict[str, Any],
    agent_audit: dict[str, Any],
    handoff_warnings: list[str],
) -> None:
    """Write provenance for Stage07 without judging the candidate's science."""

    paper_info_path = root / "paper_info.json"
    if not paper_info_path.is_file():
        write_json(
            paper_info_path,
            {
                "paper_id": paper_id,
                "task_pair_id": task_pair_id,
                "doi": next((row.get("doi") for row in documents if row.get("doi")), None),
                "title": _paper_title(documents),
                "journal": next(
                    (
                        row.get("journal_name")
                        for row in documents
                        if row.get("journal_name")
                    ),
                    None,
                ),
                "documents": [_paper_document_metadata(row) for row in documents],
                "stage05_candidates": [row.get("candidate_id") for row in candidates],
                "workflow_scope": review.get("workflow_scope") or {},
                "complexity_profile": review.get("complexity_profile") or {},
                "construction_version": STAGE06_IMPLEMENTATION_VERSION,
                "constructed_at": now_utc(),
                "publication_governance": {
                    "license_status": "unknown_not_assessed",
                    "release_rights_status": "requires_separate_review",
                    "source_access": "private_corpus",
                },
            },
        )
    write_json(root / "evidence_index.json", snapshot.get("evidence_index") or [])
    write_json(
        root / "source_manifest.json",
        {
            "snapshot_hash": snapshot.get("snapshot_hash"),
            "documents": snapshot.get("source_manifest") or [],
            "source_facts": snapshot.get("source_facts") or {},
        },
    )
    toolbox_path = root / "toolbox_requirements.json"
    if not toolbox_path.is_file():
        write_json(
            toolbox_path,
            _normalize_toolbox_requirements(review.get("toolbox_requirements") or []),
        )
    write_json(
        root / "stage06_handoff.json",
        {
            "schema_version": "researchchembench.stage06-provisional-handoff.v1",
            "paper_id": paper_id,
            "task_pair_id": task_pair_id,
            "decision": decision,
            "handoff_ready": True,
            "source_snapshot_path": str(snapshot["root"]),
            "snapshot_hash": snapshot.get("snapshot_hash"),
            "construction_receipt": receipt,
            "handoff_warnings": handoff_warnings,
            "agent_run": agent_audit,
            "created_at": now_utc(),
        },
    )


def _publish_provisional_not_constructible(
    *,
    stage_root: Path,
    run_id: str,
    paper_id: str,
    candidate_id: str,
    receipt: dict[str, Any],
    review: dict[str, Any],
    agent_audit: dict[str, Any],
    outputs: Path,
    snapshot: dict[str, Any],
    documents: list[dict[str, Any]],
) -> dict[str, Any]:
    task_pair_id = str(
        review.get("task_pair_id")
        or receipt.get("task_pair_id")
        or f"{paper_id}-provisional"
    )
    staging = prepare_clean_directory(
        stage_root
        / "staging"
        / safe_component(paper_id)
        / f"not-constructible-{uuid.uuid4().hex[:8]}"
    )
    copytree_exact(outputs, staging)
    make_writable(staging)
    write_json(staging / "workflow_review.json", review)
    write_json(staging / "construction_receipt.json", receipt)
    _write_provisional_handoff_metadata(
        staging,
        paper_id=paper_id,
        task_pair_id=task_pair_id,
        decision="provisional_not_constructible",
        documents=documents,
        candidates=[{"candidate_id": candidate_id}],
        review=review,
        receipt=receipt,
        snapshot=snapshot,
        agent_audit=agent_audit,
        handoff_warnings=["stage06_agent_abstained_stage07_source_review_required"],
    )
    write_manifest(staging, staging / "task_pair_manifest.json")
    target = stage_root / "provisional_rejections" / safe_component(paper_id)
    atomic_commit_tree(staging, target)
    scope = review.get("workflow_scope") or {}
    complexity = review.get("complexity_profile") or {}
    return {
        **record_header(run_id=run_id, stage="stage06", paper_id=paper_id),
        "candidate_id": candidate_id,
        "task_pair_id": task_pair_id,
        "processing_status": "completed",
        "decision": "provisional_not_constructible",
        "handoff_ready": True,
        "passed": False,
        "retryable": False,
        "failure_code": review.get("failure_code"),
        "failure_reasons": review.get("failure_reasons") or [],
        "workflow_scope_kind": scope.get("kind") or "none",
        "complexity_level": complexity.get("level") or "not_assessed",
        "toolbox_gap_present": any(
            _toolbox_requirement_status(row) in {"missing", "unknown", "incompatible"}
            for row in review.get("toolbox_requirements") or []
        ),
        "task_pair_path": str(target),
        "handoff_path": str(target),
        "source_snapshot_path": str(snapshot["root"]),
        "agent_runs": {"task_pair_builder": agent_audit},
    }


def _scientific_not_constructible(
    *,
    run_id: str,
    paper_id: str,
    candidate_id: str,
    review: dict[str, Any],
    agent_audit: dict[str, Any],
) -> dict[str, Any]:
    scope = review.get("workflow_scope") or {}
    complexity = review.get("complexity_profile") or {}
    return {
        **record_header(run_id=run_id, stage="stage06", paper_id=paper_id),
        "candidate_id": candidate_id,
        "task_pair_id": review.get("task_pair_id") or None,
        "processing_status": "completed",
        "decision": "scientific_not_constructible",
        "passed": False,
        "retryable": False,
        "failure_code": review.get("failure_code"),
        "failure_reasons": review.get("failure_reasons") or [],
        "paper_workflow_inventory_complete": review.get(
            "paper_workflow_inventory_complete"
        ),
        "full_paper_workflow_checked": review.get("full_paper_workflow_checked"),
        "alternative_scope_search_complete": review.get(
            "alternative_scope_search_complete"
        ),
        "workflow_scope_kind": scope.get("kind") or "none",
        "complexity_level": complexity.get("level") or "not_assessed",
        "toolbox_gap_present": any(
            _toolbox_requirement_status(row) in {"missing", "unknown", "incompatible"}
            for row in review.get("toolbox_requirements") or []
        ),
        "stage05_candidate_disposition": review.get("stage05_candidate_disposition"),
        "agent_runs": {"task_pair_builder": agent_audit},
    }


def _scientific_reject(
    *,
    run_id: str,
    paper_id: str,
    candidate_id: str,
    task_pair_id: str,
    reasons: list[str],
    review_audit: dict[str, Any],
    stage05_disposition: Any,
) -> dict[str, Any]:
    return {
        **record_header(run_id=run_id, stage="stage06", paper_id=paper_id),
        "candidate_id": candidate_id,
        "task_pair_id": task_pair_id or None,
        "processing_status": "completed",
        "decision": "scientific_reject",
        "passed": False,
        "reject_reasons": reasons,
        "stage05_candidate_disposition": stage05_disposition,
        "agent_runs": {"scientific_review": review_audit},
    }


def _objective_failure(
    run_id: str,
    paper_id: str,
    candidate_id: str,
    failure_class: str,
    message: str,
    *,
    task_pair_id: str | None = None,
    agent_run: dict[str, Any] | None = None,
    retryable: bool = True,
) -> dict[str, Any]:
    return {
        **record_header(run_id=run_id, stage="stage06", paper_id=paper_id),
        "candidate_id": candidate_id,
        "task_pair_id": task_pair_id,
        "processing_status": "failed",
        "decision": "objective_failure_retryable" if retryable else "objective_failure",
        "passed": False,
        "retryable": retryable,
        "failure_class": failure_class,
        "error": {"error_type": failure_class, "message": message[:4000]},
        "agent_run": agent_run,
    }


def _artifact_delivery_failure(
    run_id: str,
    paper_id: str,
    candidate_id: str,
    failure_class: str,
    message: str,
    *,
    agent_run: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        **record_header(run_id=run_id, stage="stage06", paper_id=paper_id),
        "candidate_id": candidate_id,
        "task_pair_id": None,
        "processing_status": "failed",
        "decision": "artifact_delivery_failure_retryable",
        "handoff_ready": False,
        "passed": False,
        "retryable": True,
        "failure_class": failure_class,
        "error": {"error_type": failure_class, "message": message[:4000]},
        "agent_run": agent_run,
    }


def _construction_invalid(
    run_id: str,
    paper_id: str,
    candidate_id: str,
    task_pair_id: str | None,
    findings: list[str],
    agent_runs: dict[str, Any],
) -> dict[str, Any]:
    return {
        **record_header(run_id=run_id, stage="stage06", paper_id=paper_id),
        "candidate_id": candidate_id,
        "task_pair_id": task_pair_id,
        "processing_status": "completed",
        "decision": "construction_invalid",
        "passed": False,
        "retryable": True,
        "validation_findings": findings,
        "agent_runs": agent_runs,
    }
