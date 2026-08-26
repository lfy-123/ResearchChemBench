from __future__ import annotations

import hashlib
import json
import re
import shutil
import uuid
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Callable

import jsonschema
from pypdf import PdfReader
from pypdf import __version__ as pypdf_version

from src.agents import AgentExecutionError, AgentRunRequest, create_agent_harness
from src.agents.schemas import (
    STAGE06_AUTONOMOUS_CONVERTER_SCHEMA,
    STAGE06_TASK_PAIR_BUILDER_SCHEMA,
    STAGE06_WORKFLOW_REVIEW_SCHEMA,
)
from src.agents.workspace import (
    atomic_commit_tree,
    copytree_exact,
    directory_manifest,
    input_fingerprint,
    make_read_only,
    make_writable,
    prepare_clean_directory,
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
    STAGE06_AUTONOMOUS_CONVERTER_VERSION,
    STAGE06_TASK_PAIR_BUILDER_VERSION,
    autonomous_converter_instructions,
    task_pair_builder_instructions,
)
from src.stages.stage06_task_builder.validation import (
    canonicalize_complexity_profile,
    canonicalize_mode_task_contract,
    canonical_paper_id,
)
from src.stages.phase_gate import (
    _conversion_renamed_paths,
    install_phase_gate_tool,
    run as run_shared_phase_gate,
    snapshot_sha256 as phase_gate_snapshot_sha256,
    write_final_self_check_report,
)
from src.stages.evaluator_reference import is_blocking_finding, read_split_reference

STAGE06_IMPLEMENTATION_VERSION = "v22-stage06b-oneshot-20260825"
STAGE06_DIRECTORY = "stage_06_task_construction"
STAGE06_INPUT_PACKAGE_VERSION = "v2-canonical-deduplicated-inputs"


def _normalize_unicode_scalar_text(value: str) -> str:
    """Combine UTF-16 surrogate pairs and replace isolated surrogates.

    Some PDF text extractors return mathematical supplementary-plane characters as literal
    surrogate code units.  Python strings can hold those units, but UTF-8 files and Agent requests
    require Unicode scalar values.
    """

    if not any(0xD800 <= ord(character) <= 0xDFFF for character in value):
        return value
    return value.encode("utf-16", errors="surrogatepass").decode(
        "utf-16", errors="replace"
    )


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

    config = dict(config)
    strategy = str(config.get("mode_generation_strategy") or "two_agent_objective_centered")
    if strategy == "two_agent_objective_centered":
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
        "stage06.mode_generation_strategy must be two_agent_objective_centered"
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
    generation_strategy = "two_agent_objective_centered"
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
                            "stage06a_max_tool_calls",
                            config.get(
                                "task_pair_builder_max_tool_calls",
                                config.get("max_tool_calls", 120),
                            ),
                        )
                    ),
                    finalization_reserve=int(
                        config.get(
                            "stage06a_finalization_reserve",
                            config.get(
                                "task_pair_builder_finalization_reserve",
                                config.get("finalization_reserve", 16),
                            ),
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
                    "phase_gate_mode": "agent_and_external",
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
                phase_gate_validator=_stage06a_phase_gate_findings,
                phase_gate_max_checks=1,
                phase_gate_fail_open=True,
                phase_gate_mode="agent_and_external",
                phase_gate_prepare=lambda root: _stage06a_phase_gate_prepare(
                    root,
                    paper_id=canonical_paper_id(paper_id),
                ),
            )
            if agent_workspace is None:
                raise FileNotFoundError("Stage06 task-pair builder workspace is unavailable")
            outputs = agent_workspace / "outputs"
            external_gate_path = agent_workspace / "external_phase_gate_report.json"
            stage06a_gate_report = read_json(external_gate_path) if external_gate_path.is_file() else {}
            if receipt.get("decision") == "scientific_not_constructible":
                # A scientific rejection is allowed to stop after the receipt; it is
                # not required to emit a workflow review or any task files.  Do not
                # turn that Agent decision into a filesystem failure by reading a
                # success-only artifact first.
                review_path = outputs / "workflow_review.json"
                # A model may have started a draft review before deciding that
                # the source is not constructible.  That draft is not part of
                # the negative contract and may be truncated or malformed;
                # never convert it into a processing/retry failure.
                try:
                    candidate_review = read_json(review_path) if review_path.is_file() else {}
                except (OSError, ValueError, TypeError, json.JSONDecodeError):
                    candidate_review = {}
                review = candidate_review if isinstance(candidate_review, dict) else {}
                failure_code = str(
                    receipt.get("failure_code") or review.get("failure_code") or ""
                ).strip()
                if failure_code == "execution_artifact_incomplete":
                    return _artifact_delivery_failure(
                        run_id,
                        paper_id,
                        candidate_id,
                        failure_code,
                        str(
                            receipt.get("summary")
                            or next(
                                (
                                    row.get("details")
                                    for row in receipt.get("failure_reasons") or []
                                    if isinstance(row, dict) and row.get("details")
                                ),
                                "Stage06 did not complete the candidate task artifacts.",
                            )
                        ),
                        agent_run=agent_audit,
                    )
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

            # Transport identity is deterministic and owned by the orchestrator;
            # preserve any Agent proposal only as non-authoritative review metadata.
            task_pair_id = canonical_paper_id(paper_id)
            review["paper_id"] = task_pair_id
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
            handoff_warnings: list[str] = []
            if receipt.get("phase_gate_status") == "bypassed_with_warnings":
                handoff_warnings.append("stage06a_gate_bypassed_with_warnings")
            if receipt.get("phase_gate_status") == "failed":
                handoff_warnings.append("stage06a_external_gate_findings")
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
                        "paper_id": task_pair_id,
                        "paper_reproduction_hash": directory_manifest(
                            staging_root / "paper_reproduction"
                        )["content_hash"],
                        "objective_card_hash": canonical_hash(
                            read_json(staging_root / "objective_card.json")
                            if (staging_root / "objective_card.json").is_file()
                            else review.get("objective_card") or {}
                        ),
                        "prompt_version": STAGE06_AUTONOMOUS_CONVERTER_VERSION,
                        "phase_gate_mode": "agent_and_external",
                        "harness": converter_harness_name,
                        "model": converter_harness.model,
                    },
                    config=config,
                    setup=lambda root: _setup_converter_inputs(
                        root,
                        staging_root,
                        stage06a_gate_report=stage06a_gate_report,
                    ),
                    # Stage06B is a single file-conversion Agent.  Its receipt is
                    # diagnostic input; it must never be promoted into a hidden
                    # semantic retry.  Execution/contract status is decided from
                    # process and artifact facts below.
                    semantic_validator=None,
                    phase_gate_validator=_converter_contract_gate_findings,
                    phase_gate_max_checks=1,
                    phase_gate_fail_open=True,
                    phase_gate_mode="agent_and_external",
                    phase_gate_prepare=lambda root: _converter_phase_gate_prepare(
                        root, paper_id=task_pair_id
                    ),
            )
            # conversion_report.json is optional handoff metadata.  It is read
            # from the one-shot workspace later, but never used to decide whether
            # Stage06B should execute again.
            if converter_response.get("phase_gate_status") == "bypassed_with_warnings":
                handoff_warnings.append("stage06b_gate_bypassed_with_warnings")
            if converter_response.get("phase_gate_status") == "failed":
                handoff_warnings.append("stage06b_external_gate_findings")
            converter_status = str(converter_response.get("status") or "").strip()
            if converter_status == "conversion_uncertain":
                # This is a semantic handoff state, not an execution failure.
                # Preserve the complete file pair and make the uncertainty
                # explicit to Stage07 instead of collapsing it into the generic
                # constructed-candidate status.
                handoff_warnings.append("stage06b_conversion_uncertain")
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
            converted_root = converter_workspace / "outputs" / "autonomous_research"
            if not converted_root.is_dir():
                raise FileNotFoundError("Stage06B autonomous task artifact is unavailable")
            old_autonomous_root = staging_root / "autonomous_research"
            if old_autonomous_root.exists() and converted_root != old_autonomous_root:
                shutil.rmtree(old_autonomous_root)
            if converted_root != old_autonomous_root:
                copytree_exact(converted_root, old_autonomous_root)
            make_writable(old_autonomous_root)
            report_path = converter_workspace / "outputs" / "conversion_report.json"
            if report_path.is_file():
                shutil.copy2(report_path, staging_root / "conversion_report.json")
            # Canonicalize each public mode's transport contract before Stage07 sees
            # the pair.  The modes may intentionally use neutral filenames, field
            # names, or result representations; do not overwrite one with the
            # other or turn a representation difference into a science decision.
            reproduction_root = staging_root / "paper_reproduction"
            autonomous_root = staging_root / "autonomous_research"
            if reproduction_root.is_dir() and autonomous_root.is_dir():
                for mode_root in (reproduction_root, autonomous_root):
                    submission_path = mode_root / "submission_contract.json"
                    if not submission_path.is_file():
                        continue
                    mode_submission = _normalize_submission_contract(
                        _json_object(submission_path)
                    )
                    mode_submission.pop("task_id", None)
                    mode_submission["paper_id"] = task_pair_id
                    write_json(submission_path, mode_submission)
                rubric_path = reproduction_root / "process_rubric.json"
                if rubric_path.is_file():
                    reproduction_submission = _normalize_submission_contract(
                        _json_object(reproduction_root / "submission_contract.json")
                    )
                    rubric = _ensure_reproduction_route_rubric(
                        read_json(rubric_path), submission=reproduction_submission
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
            split_reference = read_split_reference(staging_root)
            if reproduction_root.is_dir() and autonomous_root.is_dir() and split_reference is not None:
                try:
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
                        evidence_index=snapshot["evidence_index"],
                        snapshot=snapshot,
                        autonomous_root=autonomous_root,
                        reproduction_root=reproduction_root,
                        construction_harness=harness,
                        review_harness=harness,
                        phase_audits={
                            "task_pair_builder": agent_audit,
                            "autonomous_converter": converter_audit,
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
            _write_conversion_audit(
                staging_root,
                stage06a_gate_report=stage06a_gate_report,
                stage06b_response=converter_response,
                stage06b_agent_audit=converter_audit,
                stage06b_self_check=(
                    read_json(converter_workspace / "agent_self_check_report.json")
                    if converter_workspace is not None
                    and (converter_workspace / "agent_self_check_report.json").is_file()
                    else None
                ),
                stage06b_external_gate=(
                    read_json(converter_workspace / "external_phase_gate_report.json")
                    if converter_workspace is not None
                    and (converter_workspace / "external_phase_gate_report.json").is_file()
                    else None
                ),
            )
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
                "paper_id": task_pair_id,
                "processing_status": "completed",
                "decision": "provisional_constructed",
                "scientific_status": (
                    "conversion_uncertain"
                    if converter_status == "conversion_uncertain"
                    else "constructed_candidate"
                ),
                "contract_status": (
                    "complete"
                    if receipt.get("phase_gate_status") == "passed"
                    and converter_response.get("phase_gate_status") == "passed"
                    else "contract_incomplete"
                ),
                "handoff_ready": True,
                "passed": False,
                "provisional": True,
                "scientifically_ready": False,
                "task_pair_path": str(target),
                "handoff_path": str(target),
                "source_snapshot_path": str(snapshot["root"]),
                "workflow_scope_kind": _workflow_scope_kind(scope),
                "complexity_profile": complexity,
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
                "stage06a_gate_status": receipt.get("phase_gate_status", "not_run"),
                "stage06a_gate_attempts": receipt.get("phase_gate_attempts", 0),
                "stage06a_gate_findings": receipt.get("phase_gate_findings", []),
                "stage06a_gate_report": stage06a_gate_report,
                "stage06b_gate_status": converter_response.get(
                    "phase_gate_status", "not_run"
                ),
                "stage06b_gate_attempts": converter_response.get(
                    "phase_gate_attempts", 0
                ),
                "stage06b_gate_findings": converter_response.get(
                    "phase_gate_findings", []
                ),
                "stage06b_conversion_status": converter_status or "not_run",
                "stage06b_conversion_report": (
                    converter_response.get("conversion_report")
                    if isinstance(converter_response.get("conversion_report"), dict)
                    else {}
                ),
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
        "contract_incomplete": sum(
            row.get("contract_status") == "contract_incomplete" for row in records
        ),
        "retryable_failures": sum(
            row.get("decision") == "objective_failure_retryable" for row in records
        ),
        "artifact_delivery_failures": sum(
            row.get("decision") == "artifact_delivery_failure_retryable"
            for row in records
        ),
        "stage06a_gate_bypassed": sum(
            row.get("stage06a_gate_status") == "bypassed_with_warnings"
            for row in records
        ),
        "stage06a_gate_attempts": sum(
            int(row.get("stage06a_gate_attempts") or 0) for row in records
        ),
        "stage06a_gate_findings": sorted(
            {
                str(finding)
                for row in records
                for finding in row.get("stage06a_gate_findings") or []
            }
        ),
        "stage06b_gate_bypassed": sum(
            row.get("stage06b_gate_status") == "bypassed_with_warnings"
            for row in records
        ),
        "stage06b_gate_attempts": sum(
            int(row.get("stage06b_gate_attempts") or 0) for row in records
        ),
        "stage06b_gate_findings": sorted(
            {
                str(finding)
                for row in records
                for finding in row.get("stage06b_gate_findings") or []
            }
        ),
        "toolbox_gaps": sum(bool(row.get("toolbox_gap_present")) for row in records),
        "paper_ids": sorted({str(row.get("paper_id")) for row in records if row.get("paper_id")}),
        "decisions": decision_counts(records),
        "agent_harness": harness.name,
        "agent_model": harness.model,
    }
    write_json(stage_root / "stage_summary.json", summary)
    return {"records": records, "summary": summary}


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
    # The phase self-check is copied as a standalone script so Agent workspaces
    # never need to import the repository or its scientific validators.
    install_phase_gate_tool(root)


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
    "decision", "paper_id", "paper_workflow_inventory_complete",
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
    for private_key in ("workflow_scope", "complexity_profile", "ground_truth_items"):
        if private_key in value:
            raise SystemExit(
                "public_private_field_present:paper_reproduction:"
                + label + ".json:" + private_key
            )
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
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else "outputs")
reproduction = root / "paper_reproduction"
required_public = {
    "task.md", "task_info.json", "task_spec.json", "submission_contract.json",
    "process_rubric.json", "paper_route.md", "workflow_spec.json",
    "route_evidence_map.json",
}
missing = sorted(name for name in required_public if not (reproduction / name).is_file())
if missing:
    raise SystemExit("paper_reproduction missing: " + ", ".join(missing))
if not (reproduction / "data" / "inputs").is_dir():
    raise SystemExit("paper_reproduction data/inputs is missing")
evaluator = root / "evaluator_reference"
required_evaluator = {
    "reference_key_points.json", "reference_conclusions.json", "scoring_rules.json",
    "evidence_map.json", "critical_failures.json",
}
missing = sorted(name for name in required_evaluator if not (evaluator / name).is_file())
if missing:
    raise SystemExit("evaluator_reference missing: " + ", ".join(missing))
if (root / "hidden_reference").exists():
    raise SystemExit("legacy hidden_reference is forbidden")
print("Stage06 synthesis draft shape: OK")
'''




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
                "phase_gate": Path(__file__).resolve().parents[1].joinpath("phase_gate.py").read_text(encoding="utf-8"),
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
                "It creates the public reproduction file scaffold and copies only source-provided "
                "input content. Author all five evaluator_reference files from the paper, then "
                "run the shared Gate before writing the receipt."
            ),
            "autonomous_editable_files": "recursive_autonomous_public_surface",
            "shared_across_modes": [
                "data/inputs",
                "submission_contract.json",
                "workflow_scope",
                "complexity_profile",
                "autonomy_scope",
                "method_constraints",
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
    phase_gate_validator: Callable[[dict[str, Any], Path], list[str]] | None = None,
    phase_gate_max_checks: int | None = None,
    phase_gate_fail_open: bool | None = None,
    phase_gate_mode: str | None = None,
    phase_gate_agent_self_check: bool | None = None,
    phase_gate_prepare: Callable[[Path], list[str]] | None = None,
) -> tuple[dict[str, Any], dict[str, Any], Path | None]:
    """Run one late-stage Agent invocation and one shared post-write Gate."""

    gate_phase_name = {
        "task_pair_builder": "stage06a",
        "autonomous_converter": "stage06b",
        "stage06a": "stage06a",
        "stage06b": "stage06b",
    }.get(phase, phase)
    fingerprint = input_fingerprint(fingerprint_value)
    artifact_root = (
        stage_root / "phase_artifacts" / safe_component(paper_id)
        / safe_component(phase) / fingerprint[:16]
    )
    checkpoint = (
        stage_root / "checkpoints" / safe_component(paper_id)
        / f"{safe_component(phase)}.json"
    )
    gate_mode = phase_gate_mode or "none"
    if gate_mode not in {"none", "agent_and_external", "external_only"}:
        raise ValueError(f"unsupported phase_gate_mode={gate_mode!r}")
    gate_enabled = phase_gate_validator is not None and gate_mode != "none"
    agent_self_check = gate_mode == "agent_and_external"
    external_gate = gate_mode in {"agent_and_external", "external_only"}
    if phase_gate_max_checks not in (None, 1):
        raise ValueError("late-stage phases allow exactly one Gate check")

    # A completed artifact may be reused as a process checkpoint. Failed runs and
    # failed conversations are never resumed or copied into a new prompt.
    if bool(config.get("checkpoint_cache_enabled", True)) and checkpoint.is_file() and artifact_root.is_dir():
        cached = read_json(checkpoint)
        if cached.get("input_fingerprint") == fingerprint:
            response = cached.get("response") or {}
            jsonschema.validate(response, output_schema)
            findings: list[str] = []
            if semantic_validator is not None:
                findings.extend(semantic_validator(response, artifact_root))
            if gate_enabled and phase_gate_prepare is not None:
                findings.extend(phase_gate_prepare(artifact_root))
            if gate_enabled:
                findings.extend(phase_gate_validator(response, artifact_root))
            if not findings:
                return response, {**(cached.get("agent_run") or {}), "cache_hit": True}, artifact_root

    attempt_root = prepare_clean_directory(
        stage_root / "workspaces" / safe_component(paper_id)
        / safe_component(phase) / f"attempt-01-{uuid.uuid4().hex[:8]}"
    )
    setup(attempt_root)
    (attempt_root / "outputs").mkdir(parents=True, exist_ok=True)
    write_json(
        attempt_root / "phase_state.json",
        {"phase": phase, "paper_id": paper_id, "input_fingerprint": fingerprint,
         "prompt_version": prompt_version},
    )
    phase_instructions = instructions
    if agent_self_check and phase in {"task_pair_builder", "autonomous_converter"}:
        phase_instructions += f"""

MANDATORY AGENT SELF-CHECK (FINALIZATION STEP)
After writing the complete {gate_phase_name} artifact, run:
python inputs/tools/phase_gate.py --phase {gate_phase_name} --root outputs
Read the complete report, repair every blocking finding in this same workspace, and run the
check again after the final write. Do not return a constructed/converted result while the
self-check has blocking findings. The final receipt must describe the files after that check.
"""
    phase_tool_calls = max(
        4,
        int(config.get(f"{phase}_max_tool_calls", config.get("max_tool_calls", 24))),
    )
    phase_finalization_reserve = max(
        1,
        min(
            phase_tool_calls - 1,
            int(config.get(f"{phase}_finalization_reserve", config.get("finalization_reserve", 4))),
        ),
    )
    artifact_receipt_metadata: dict[str, Any] = {}
    if phase == "autonomous_task":
        artifact_receipt_metadata = {
            "artifact_receipt_path": "task",
            "artifact_required_files": [
                "task.md", "task_info.json", "task_spec.json",
                "submission_contract.json", "process_rubric.json",
            ],
        }
    elif phase == "paper_reproduction":
        artifact_receipt_metadata = {
            "artifact_receipt_path": "task",
            "artifact_required_files": [
                "task.md", "task_info.json", "task_spec.json",
                "submission_contract.json", "process_rubric.json",
                "paper_route.md", "workflow_spec.json", "route_evidence_map.json",
            ],
        }
    request = AgentRunRequest(
        phase=f"stage06_{phase}",
        record_id=paper_id,
        workspace=attempt_root,
        instructions=phase_instructions,
        output_schema=output_schema,
        prompt_version=prompt_version,
        timeout_seconds=int(config.get(f"{phase}_timeout_seconds", config.get("timeout_seconds", 3600))),
        metadata={
            "paper_id": paper_id,
            "input_fingerprint": fingerprint,
            "max_tool_calls": phase_tool_calls,
            "finalization_reserve": phase_finalization_reserve,
            "tool_choice_policy": config.get(f"{phase}_tool_choice_policy"),
            "response_format_policy": config.get(f"{phase}_response_format_policy"),
            "codex_wire_api": config.get(f"{phase}_codex_wire_api"),
            "inline_contract": False,
            "structured_artifact_path": {
                "task_pair_builder": "outputs/construction_receipt.json",
                "autonomous_converter": "outputs/conversion_report.json",
            }.get(phase),
            **artifact_receipt_metadata,
        },
    )
    try:
        result = harness.run(request)
        response = result.response or {}
        if phase == "scientific_review":
            response = _materialize_scientific_review_response(response, attempt_root)
        elif phase in {"autonomous_task", "paper_reproduction"}:
            response = _reconcile_task_phase_receipt(response, workspace=attempt_root, phase=phase, result=result)
        elif phase == "autonomous_converter":
            response = _reconcile_converter_phase_receipt(response, workspace=attempt_root)
            response = _reconcile_complete_converter_artifact(response, workspace=attempt_root, result=result)
        result.response = response
        if semantic_validator is not None:
            findings = semantic_validator(response, attempt_root)
            if findings:
                raise AgentExecutionError(
                    f"Agent {phase} contract failed: {'; '.join(findings)}",
                    failure_class="invalid_phase_contract",
                    retryable=False,
                    result=result,
                )
        _require_claimed_phase_artifact(response, attempt_root, result)
        if gate_enabled:
            pre_self_report = read_json(attempt_root / "agent_self_check_report.json") if (attempt_root / "agent_self_check_report.json").is_file() else None
            preparation_findings = phase_gate_prepare(attempt_root) if phase_gate_prepare is not None else []
            gate_findings = sorted(set(preparation_findings) | set(phase_gate_validator(response, attempt_root)))
            final_self_report = write_final_self_check_report(
                phase=gate_phase_name, outputs=attempt_root / "outputs", report_root=attempt_root,
                pre_normalization=pre_self_report, findings=gate_findings,
                normalization_findings=preparation_findings,
            )
            gate_report = {
                "schema_version": "stage06-07-phase-gate/v3",
                "phase": gate_phase_name,
                "implementation_phase": phase,
                "paper_id": paper_id,
                "authority": "orchestrator_external_read_only",
                "status": "passed" if not any(is_blocking_finding(item) for item in gate_findings) else "failed",
                "attempt": 1,
                "max_checks": 1,
                "findings": gate_findings,
                "blocking_findings": [item for item in gate_findings if is_blocking_finding(item)],
                "warnings": [item for item in gate_findings if not is_blocking_finding(item)],
                "agent_self_check_required": agent_self_check,
                "snapshot_sha256": phase_gate_snapshot_sha256(attempt_root / "outputs"),
                "snapshot_stage": "post_normalization",
                "self_check_snapshot_sha256": final_self_report["snapshot_sha256"],
                "self_check_snapshot_parity": final_self_report.get("snapshot_parity"),
                "created_at": now_utc(),
            }
            if external_gate:
                write_json(attempt_root / "external_phase_gate_report.json", gate_report)
            result.response = dict(response)
            result.response.update({
                "phase_gate_status": gate_report["status"],
                "phase_gate_attempts": 1,
                "phase_gate_findings": gate_findings,
                "phase_gate_authority": gate_report["authority"],
            })
            if gate_report["status"] == "failed":
                # Preserve the exact failed artifact and Gate diagnostics for Stage07/operators;
                # a terminal Gate finding must not erase the evidence needed to repair or reject
                # the candidate.  No retry or conversation recovery is started.
                write_json(attempt_root / "agent_run.json", result.audit_record())
                _persist_phase_artifacts(attempt_root, artifact_root)
                raise AgentExecutionError(
                    f"{gate_phase_name} external Gate failed: {'; '.join(gate_report['blocking_findings'])}",
                    failure_class="invalid_phase_contract",
                    retryable=False,
                    result=result,
                )
        _persist_phase_artifacts(attempt_root, artifact_root)
        write_json(attempt_root / "agent_run.json", result.audit_record())
        write_json(
            checkpoint,
            {"phase": phase, "paper_id": paper_id, "input_fingerprint": fingerprint,
             "prompt_version": prompt_version, "response": result.response,
             "agent_run": result.audit_record(), "completed_at": now_utc()},
        )
        return result.response or {}, {**result.audit_record(), "cache_hit": False}, artifact_root
    except AgentExecutionError as exc:
        if exc.result is not None:
            write_json(attempt_root / "agent_run.json", exc.result.audit_record())
        raise



def _stage06a_phase_gate_findings(
    response: dict[str, Any],
    workspace: Path,
) -> list[str]:
    """Run exactly the shared file contract exposed to the Agent self-check."""

    outputs = workspace / "outputs"
    return sorted(set(run_shared_phase_gate("stage06a", outputs)["findings"]))


def _stage06a_phase_gate_prepare(
    workspace: Path,
    *,
    paper_id: str | None = None,
) -> list[str]:
    """Canonicalize only a positive Stage06A task tree.

    A ``scientific_not_constructible`` receipt uses a failure-only Gate scope.
    The bootstrap may still leave an empty mode directory, but sending that
    directory through the positive canonicalizer would create spurious
    ``missing_public_file`` findings that are absent from the Agent self-check.
    """

    outputs = workspace / "outputs"
    receipt_path = outputs / "construction_receipt.json"
    if receipt_path.is_file():
        try:
            receipt = read_json(receipt_path)
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            receipt = None
        if isinstance(receipt, dict) and receipt.get("decision") == "scientific_not_constructible":
            return []
    reproduction = outputs / "paper_reproduction"
    if not reproduction.is_dir():
        return []
    return canonicalize_mode_task_contract(
        reproduction,
        expected_mode="paper_reproduction",
        task_pair_id=paper_id,
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




_BLOCK_EVIDENCE_RE = re.compile(
    r"^ev_(?P<document>doc_[A-Za-z0-9]+)_(?P<index>\d{6})_(?P<digest>[A-Fa-f0-9*]+)$"
)
_DERIVED_EVIDENCE_RE = re.compile(
    r"^ev_derived_(?P<document>doc_[A-Za-z0-9]+)_(?P<digest>[A-Fa-f0-9]+)$"
)
_LEGACY_DERIVED_EVIDENCE_RE = re.compile(
    r"^ev_(?P<document>doc_[A-Za-z0-9]+)_(?P<digest>[A-Fa-f0-9]{8,})$"
)








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






def _json_object(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    try:
        value = read_json(path)
    except (OSError, ValueError, TypeError):
        return {}
    return value if isinstance(value, dict) else {}




_AUTONOMY_SCOPES = {
    "fixed_input_method_constrained_workflow",
    "fixed_input_method_discovery",
}


def _autonomy_scope(scope: Any) -> str:
    """Read the Agent's autonomy contract, with a safe legacy default.

    Older task reviews did not carry this field and their autonomous prompt asked the
    evaluated Agent to choose a method.  Preserve that behavior instead of silently
    relabeling those tasks as method-constrained.
    """

    value = str((scope or {}).get("autonomy_scope") or "").strip()
    return value if value in _AUTONOMY_SCOPES else "fixed_input_method_discovery"










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






















def _ensure_reproduction_route_rubric(
    rubric: Any, *, submission: dict[str, Any]
) -> list[dict[str, Any]]:
    # Agents may serialize the same rubric as a bare list or as an object with an
    # ``items``/``criteria`` wrapper.  This is a transport normalization only;
    # the scientific meaning and scores are preserved.
    if isinstance(rubric, dict):
        rubric = rubric.get("items") or rubric.get("criteria") or []
    if not isinstance(rubric, list):
        return []
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
            and str(row.get("criterion_type") or "").casefold() == "route_fidelity"
        ),
        None,
    )
    if target is None:
        # Do not repurpose an unrelated scientific criterion as route fidelity.
        # Add a transport Key Point and preserve any score fields the Agent
        # supplied.  The data pipeline does not choose a scale, total, or
        # weighting policy.
        route_id = "paper_route_fidelity"
        used_ids = {
            str(row.get("id") or "") for row in output if isinstance(row, dict)
        }
        if route_id in used_ids:
            route_id = "paper_route_fidelity_transport"
        output.append(
            {
                "id": route_id,
                "criterion_type": "route_fidelity",
                "name": "Paper-route fidelity",
                "description": "Follow the disclosed paper route, dependency order, method hierarchy, and validation sequence.",
                "evidence_artifacts": evidence_paths,
            }
        )
        return output
    route_id = "paper_route_fidelity"
    if any(
        row is not target
        and isinstance(row, dict)
        and str(row.get("id") or "") == route_id
        for row in output
    ):
        route_id = "paper_route_fidelity_transport"
    target["id"] = route_id
    target["criterion_type"] = "route_fidelity"
    target["description"] = (
        "Follow the disclosed paper route, dependency order, method hierarchy, and validation "
        "sequence while reporting any unavoidable deviation."
    )
    target["evidence_artifacts"] = evidence_paths
    return output






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


def _reconcile_converter_phase_receipt(
    receipt: dict[str, Any], *, workspace: Path
) -> dict[str, Any]:
    """Prefer a complete canonical Stage06B tree over a stale receipt path.

    The converter writes a file-first artifact below ``outputs/autonomous_research``.
    A model may correctly finish that tree while returning the shortened path
    ``autonomous_research``.  The later semantic validator already audits the tree;
    normalizing this transport-only path prevents a complete conversion from being
    retried as a missing artifact without accepting a partial tree.
    """

    if receipt.get("status") not in {"converted", "conversion_uncertain"}:
        return receipt
    autonomous = workspace / "outputs" / "autonomous_research"
    required = {
        "task.md",
        "task_info.json",
        "task_spec.json",
        "submission_contract.json",
        "process_rubric.json",
    }
    present = {
        path.relative_to(autonomous).as_posix()
        for path in autonomous.rglob("*")
        if autonomous.is_dir() and path.is_file()
    }
    if not required.issubset(present):
        return receipt
    output = dict(receipt)
    if output.get("artifact_path") != "outputs/autonomous_research":
        output["artifact_path"] = "outputs/autonomous_research"
        output["receipt_reconciled_from_artifact"] = True
    return output


def _reconcile_complete_converter_artifact(
    receipt: dict[str, Any], *, workspace: Path, result: Any
) -> dict[str, Any]:
    """Make a complete file-first tree authoritative over contradictory prose.

    A successful one-shot CLI process can return ``objective_consistency_error``
    after writing the complete tree when the model misinterprets successful shell
    results as rejected tool calls.  Preserve that status as diagnostics, but do
    not discard a checkable artifact or turn model prose into a hidden retry.
    """

    autonomous = workspace / "outputs" / "autonomous_research"
    required = {
        "task.md",
        "task_info.json",
        "task_spec.json",
        "submission_contract.json",
        "process_rubric.json",
    }
    present = {
        path.relative_to(autonomous).as_posix()
        for path in autonomous.rglob("*")
        if autonomous.is_dir() and path.is_file()
    }
    if not required.issubset(present):
        return receipt
    if getattr(result, "status", None) != "succeeded" or getattr(result, "exit_code", 0) not in (0, None):
        return receipt
    status = str(receipt.get("status") or "").strip()
    if status not in {"objective_consistency_error", "invalid"}:
        return receipt
    output = dict(receipt)
    output["agent_reported_status"] = status
    output["status"] = "conversion_uncertain"
    output["summary"] = (
        "A complete autonomous task tree was delivered by a successful process, "
        "but the Agent returned a negative prose status; Stage07 must audit the "
        "final public surface."
    )
    reasons = output.get("invalid_reasons")
    if not isinstance(reasons, list):
        reasons = []
    output["invalid_reasons"] = [*reasons, f"agent_reported_status:{status}"]
    output["artifact_path"] = "outputs/autonomous_research"
    output["receipt_reconciled_from_artifact"] = True
    return output


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
    install_phase_gate_tool(destination / "tools")
    make_read_only(destination)


def _setup_converter_inputs(
    root: Path,
    source_pair: Path,
    *,
    stage06a_gate_report: dict[str, Any] | None = None,
) -> None:
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
    gate_report = stage06a_gate_report if isinstance(stage06a_gate_report, dict) else {}
    public_basis = review.get("public_task_basis") or {}
    scope = dict(review.get("workflow_scope") or {})
    # Public conversion needs the scope shape, not the answer-bearing claims.
    scope.pop("supported_primary_claims", None)
    selected_autonomy_scope = _autonomy_scope(scope)
    scope["autonomy_scope"] = selected_autonomy_scope
    method_policy = public_basis.get("method_constraints") or public_basis.get(
        "public_method_constraints"
    ) or []
    input_assets = public_basis.get("input_assets") or []
    truths = review.get("ground_truth_items") or []
    public_aliases = _public_key_point_aliases(truths)
    boundary_conditions = public_basis.get("boundary_conditions") or []
    reproduction_submission_path = reproduction / "submission_contract.json"
    reproduction_submission = (
        read_json(reproduction_submission_path)
        if reproduction_submission_path.is_file()
        else {}
    )
    submission_required_files = [
        str(path)
        for path in (
            reproduction_submission.get("required_files")
            if isinstance(reproduction_submission, dict)
            else []
        ) or []
        if isinstance(path, str) and path.strip()
    ]
    conversion_contract = {
        "schema_version": "stage06-conversion-contract/v1",
        "paper_id": review.get("paper_id"),
        "public_objective": {
            "public_scientific_question": review.get("public_scientific_question")
            or review.get("scientific_question"),
            "workflow_scope": scope,
            "autonomy_scope": selected_autonomy_scope,
            "method_constraints": method_policy,
        },
        "public_input_assets": [
            {
                key: asset.get(key)
                for key in ("asset_id", "path", "description", "role")
                if asset.get(key) not in (None, "", [])
            }
            for asset in input_assets
            if isinstance(asset, dict)
        ],
        "key_point_ids": [
            {
                "key_point_id": public_aliases.get(
                    str(row.get("ground_truth_id") or row.get("item_id") or ""),
                    f"kp_{index:03d}",
                ),
                "claim_role": row.get("claim_role") or "intermediate",
                "acceptance_type": row.get("acceptance_type") or "semantic_propositions",
            }
            for index, row in enumerate(truths, start=1)
            if isinstance(row, dict)
            and (row.get("ground_truth_id") or row.get("item_id"))
        ],
        "preserve_boundary_conditions": [
            {
                **row,
                "classification": row.get("classification") or "needs_stage07_review",
            }
            if isinstance(row, dict)
            else {"value": row, "classification": "needs_stage07_review"}
            for row in boundary_conditions
        ],
        "preserve_method_constraints": method_policy,
        "route_redaction_map": {
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
            "method_constraint_fields_to_preserve": [
                "public_task_basis.method_constraints",
                "task_spec.method_constraints",
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
        "asset_neutralization_map": [
            {
                "source_path": asset.get("path"),
                "public_identifier": f"candidate_{index}",
                "remove_source_label": True,
                "preserve_coordinate_rows": True,
            }
            for index, asset in enumerate(input_assets, start=1)
            if isinstance(asset, dict) and asset.get("path")
        ],
        "deliverable_contract": {
            "required_package_files": [
                "task.md",
                "task_info.json",
                "task_spec.json",
                "submission_contract.json",
                "process_rubric.json",
            ],
            "submission_required_files": submission_required_files,
            "package_files_are_not_submission_deliverables": True,
            "preserve_submission_contract": True,
            "preserve_key_point_ids": True,
        },
    }
    if gate_report.get("status") == "bypassed_with_warnings":
        conversion_contract["stage06a_gate_warning"] = {
            "status": gate_report.get("status"),
            "attempt": gate_report.get("attempt"),
            "findings": gate_report.get("findings") or [],
        }
    write_json(destination / "conversion_contract.json", conversion_contract)
    install_phase_gate_tool(root / "inputs" / "tools")
    make_read_only(destination)
    # Directory transport is deterministic.  Stage06B receives a correctly rooted,
    # writable copy and spends its budget only on semantic redaction/neutralization.
    autonomous = root / "outputs" / "autonomous_research"
    copytree_exact(reproduction, autonomous)
    make_writable(autonomous)
    # Seed the converter with the canonical autonomous transport surface.  This
    # removes deterministic reproduction-only route files and fixes enum/ID
    # aliases before the one-shot Agent spends its budget on semantic redaction.
    # It does not rewrite scientific fields, inputs, or evaluator targets.
    for name in ("paper_route.md", "workflow_spec.json", "route_evidence_map.json"):
        (autonomous / name).unlink(missing_ok=True)
    canonicalize_mode_task_contract(
        autonomous,
        expected_mode="autonomous_research",
        task_pair_id=str(review.get("paper_id") or "").strip() or None,
    )


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
                "paper_id": review.get("paper_id"),
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
        else:
            objective = dict(objective)
            objective.pop("objective_id", None)
            objective.setdefault("paper_id", review.get("paper_id"))
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


def _converter_contract_gate_findings(
    response: dict[str, Any], workspace: Path
) -> list[str]:
    """Check the final Stage06B artifact through the shared file contract.

    The Agent receipt is not the authority for whether a file tree is checkable.
    A malformed/uncertain receipt must not bypass the external Gate when the
    autonomous tree exists; conversely, a missing tree is reported as a concrete
    Gate finding instead of being converted into an Agent retry.
    """

    del response
    return list(run_shared_phase_gate("stage06b", workspace / "outputs")["findings"])


def _converter_phase_gate_prepare(root: Path, *, paper_id: str) -> list[str]:
    """Apply only deterministic converter path/ID normalization before Gate."""

    autonomous = root / "outputs" / "autonomous_research"
    if not autonomous.is_dir():
        return []
    findings = canonicalize_mode_task_contract(
        autonomous,
        expected_mode="autonomous_research",
        task_pair_id=paper_id,
    )
    report_path = root / "outputs" / "conversion_report.json"
    if not report_path.is_file():
        return findings
    try:
        report = read_json(report_path)
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        return findings
    # Use the same tolerant rename projection as the shared Gate.  The
    # converter may report a pair as [old, new] or as {from, to}; both forms
    # describe the same lossless transport edit.
    renamed = _conversion_renamed_paths(root / "outputs")
    if not renamed:
        return findings
    spec_path = autonomous / "task_spec.json"
    try:
        spec = read_json(spec_path)
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        return findings
    changed = False
    if isinstance(spec, dict):
        for asset in spec.get("input_assets") or []:
            if not isinstance(asset, dict):
                continue
            path = str(asset.get("path") or "").replace("\\", "/")
            replacement = renamed.get(path)
            if replacement:
                asset["path"] = replacement
                changed = True
    if changed:
        write_json(spec_path, spec)
    return findings


def _persist_phase_artifacts(workspace: Path, destination: Path) -> None:
    available = [name for name in ("outputs", "task") if (workspace / name).is_dir()]
    if not available:
        return
    staging = prepare_clean_directory(destination.parent / f".{destination.name}-{uuid.uuid4().hex[:8]}")
    for name in available:
        copytree_exact(workspace / name, staging / name)
    for name in (
        "agent_self_check_report.json",
        "external_phase_gate_report.json",
    ):
        gate_report = workspace / name
        if gate_report.is_file():
            shutil.copy2(gate_report, staging / name)
    atomic_commit_tree(staging, destination)




def _receipt_is_terminal_negative(receipt: dict[str, Any]) -> bool:
    return receipt.get("decision") in {
        "scientific_reject",
        "scientific_not_constructible",
    } or receipt.get("status") == "invalid"


















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














def _public_key_point_aliases(truths: Any) -> dict[str, str]:
    """Assign stable neutral aliases without exposing private Ground Truth IDs."""

    aliases: dict[str, str] = {}
    for index, item in enumerate(truths if isinstance(truths, list) else [], start=1):
        if not isinstance(item, dict):
            continue
        identifier = str(item.get("ground_truth_id") or item.get("item_id") or "").strip()
        if identifier:
            aliases[identifier] = f"kp_{index:03d}"
    return aliases














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
    "submission_contract.json",
    "process_rubric.json",
    "paper_route.md",
    "workflow_spec.json",
    "route_evidence_map.json",
    "derived_from.json",
    "public_manifest.json",
}




def _materialize_pair_metadata(
    root: Path,
    *,
    paper_id: str,
    task_pair_id: str,
    documents: list[dict[str, Any]],
    stage04: dict[str, Any],
    candidates: list[dict[str, Any]],
    review: dict[str, Any],
    evidence_index: list[dict[str, Any]],
    snapshot: dict[str, Any],
    autonomous_root: Path,
    reproduction_root: Path,
    construction_harness,
    review_harness,
    phase_audits: dict[str, Any],
    mode_generation_order: list[str] | None = None,
    mode_generation_strategy: str = "two_agent_objective_centered",
) -> None:
    write_json(
        root / "paper_info.json",
        {
            "paper_id": paper_id,
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
    split_reference = read_split_reference(root)
    if split_reference is None:
        raise ValueError(
            "evaluator_reference_missing: Stage06A must author all split evaluator files"
        )
    write_json(
        root / "construction_record.json",
        {
            "paper_id": paper_id,
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
        pages = [
            _normalize_unicode_scalar_text(
                page.extract_text(extraction_mode="layout") or ""
            )
            for page in reader.pages
        ]
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


def _write_conversion_audit(
    pair_root: Path,
    *,
    stage06a_gate_report: dict[str, Any] | None,
    stage06b_response: dict[str, Any],
    stage06b_agent_audit: dict[str, Any] | None,
    stage06b_self_check: dict[str, Any] | None,
    stage06b_external_gate: dict[str, Any] | None = None,
) -> None:
    """Persist a mechanical reproduction→autonomous audit beside the pair.

    This report is diagnostic metadata for Stage07/operators.  It never enters either
    public mode directory and it never changes a scientific decision.  The external
    Gate remains the contract authority; this audit records the exact file/input
    comparison that made the result reproducible.
    """

    required = {
        "task.md",
        "task_info.json",
        "task_spec.json",
        "submission_contract.json",
        "process_rubric.json",
    }
    reproduction = pair_root / "paper_reproduction"
    autonomous = pair_root / "autonomous_research"
    findings: list[str] = []
    disclosure_findings: list[str] = []

    def parse(name: str, root: Path) -> dict[str, Any]:
        path = root / name
        if not path.is_file():
            return {}
        try:
            value = read_json(path)
        except (OSError, TypeError, ValueError, json.JSONDecodeError):
            findings.append(f"json_unreadable:{root.name}/{name}")
            return {}
        return value if isinstance(value, dict) else {}

    def file_set(root: Path) -> set[str]:
        return {
            path.relative_to(root).as_posix()
            for path in root.rglob("*")
            if path.is_file()
        } if root.is_dir() else set()

    def input_fingerprints(root: Path, spec: dict[str, Any]) -> dict[str, str]:
        result: dict[str, str] = {}
        input_root = root / "data" / "inputs"
        for asset in spec.get("input_assets") or []:
            if not isinstance(asset, dict):
                continue
            raw = str(asset.get("path") or "").replace("\\", "/")
            for prefix in ("data/inputs/", "inputs/"):
                if raw.startswith(prefix):
                    raw = raw[len(prefix) :]
                    break
            if not raw:
                continue
            path = input_root / raw
            if path.is_file():
                if path.suffix.casefold() == ".xyz":
                    # Comments/neutral filenames are allowed to change during
                    # conversion.  Fingerprint atom count, element order and
                    # coordinate rows—the scientific geometry payload—only.
                    lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
                    try:
                        count = int(lines[0].strip())
                        rows = [line.strip() for line in lines[2 : 2 + count]]
                    except (IndexError, ValueError):
                        rows = []
                    result[raw] = canonical_hash(rows)
                else:
                    result[raw] = sha256_file(path)
            else:
                findings.append(f"input_missing:{root.name}:{raw}")
        return result

    reproduction_info = parse("task_info.json", reproduction)
    autonomous_info = parse("task_info.json", autonomous)
    reproduction_spec = parse("task_spec.json", reproduction)
    autonomous_spec = parse("task_spec.json", autonomous)
    reproduction_submission = parse("submission_contract.json", reproduction)
    autonomous_submission = parse("submission_contract.json", autonomous)
    reproduction_files = file_set(reproduction)
    autonomous_files = file_set(autonomous)
    for name in sorted(required - reproduction_files):
        findings.append(f"reproduction_required_missing:{name}")
    for name in sorted(required - autonomous_files):
        findings.append(f"autonomous_required_missing:{name}")

    mode_values = {
        "reproduction_mode": reproduction_info.get("mode"),
        "autonomous_mode": autonomous_info.get("mode"),
        "reproduction_task_mode": reproduction_info.get("task_mode"),
        "autonomous_task_mode": autonomous_info.get("task_mode"),
    }
    if autonomous_info.get("mode") not in {"autonomous_research", "autonomous"}:
        findings.append("autonomous_mode_invalid")
    if autonomous_info.get("task_mode") not in {"open_discovery", "autonomous_research", "autonomous"}:
        findings.append("autonomous_task_mode_invalid")

    def declared_deliverables(info: dict[str, Any]) -> set[str]:
        return {
            str(row.get("path"))
            for row in info.get("required_deliverables") or []
            if isinstance(row, dict) and row.get("path")
        }

    def required_deliverables(contract: dict[str, Any]) -> set[str]:
        return {str(row) for row in contract.get("required_files") or [] if isinstance(row, str)}

    deliverable_closure = {
        "reproduction": declared_deliverables(reproduction_info)
        == required_deliverables(reproduction_submission),
        "autonomous": declared_deliverables(autonomous_info)
        == required_deliverables(autonomous_submission),
    }
    for mode, closed in deliverable_closure.items():
        if not closed:
            findings.append(f"{mode}_deliverable_contract_not_closed")

    reproduction_inputs = input_fingerprints(reproduction, reproduction_spec)
    autonomous_inputs = input_fingerprints(autonomous, autonomous_spec)
    if Counter(reproduction_inputs.values()) != Counter(autonomous_inputs.values()):
        findings.append("public_input_fingerprint_mismatch")

    forbidden_names = {
        "paper_route.md",
        "workflow_spec.json",
        "route_evidence_map.json",
        "conversion_contract.json",
    }
    forbidden_dirs = {"paper_reproduction", "conversion_packet", "hidden_reference", "source_materials"}
    marker_re = re.compile(
        r"\b(?:gt_[A-Za-z0-9_.-]+|canonical_answer|acceptance_profile_id|source_evidence|evidence_id)\b",
        re.IGNORECASE,
    )
    if autonomous.is_dir():
        for path in autonomous.rglob("*"):
            relative = path.relative_to(autonomous).as_posix()
            if path.is_dir() and path.name in forbidden_dirs:
                disclosure_findings.append(f"forbidden_directory:{relative}")
            elif path.is_file():
                if path.name in forbidden_names:
                    disclosure_findings.append(f"forbidden_file:{relative}")
                if path.suffix.lower() in {".md", ".json", ".txt", ".xyz"}:
                    try:
                        text = path.read_text(encoding="utf-8", errors="replace")
                    except OSError:
                        continue
                    if marker_re.search(text):
                        disclosure_findings.append(f"internal_marker:{relative}")

    self_findings = sorted(set((stage06b_self_check or {}).get("findings") or []))
    external_findings = sorted(set(stage06b_response.get("phase_gate_findings") or []))
    conversion_report = stage06b_response.get("conversion_report")
    if not isinstance(conversion_report, dict):
        conversion_report = {}
    remaining_disclosures = [
        str(item).strip()
        for item in conversion_report.get("remaining_disclosures") or []
        if str(item).strip()
    ]
    agent_status = str(stage06b_response.get("status") or "not_run").strip()
    # ``conversion_uncertain`` is meaningful only when the Agent left a concrete
    # unresolved disclosure.  A conservative prose label on an otherwise closed
    # artifact must not downgrade a complete conversion.
    semantic_uncertain = bool(remaining_disclosures)
    contract_complete = not findings and not external_findings
    audit = {
        "schema_version": "researchchembench.stage06b-conversion-audit.v1",
        # ``complete`` means that the conversion is both mechanically closed
        # and semantically settled.  A passed Gate cannot erase an Agent's
        # explicit conversion_uncertain/remaining_disclosures state.
        "status": (
            "uncertain"
            if semantic_uncertain and contract_complete
            else "complete"
            if contract_complete
            else "incomplete"
        ),
        "execution_status": (
            "completed"
            if str((stage06b_agent_audit or {}).get("status") or "")
            in {"succeeded", "completed"}
            else "unknown"
        ),
        "process_exit_code": (stage06b_agent_audit or {}).get("exit_code"),
        "agent_reported_status": agent_status,
        "contract_status": "complete" if contract_complete else "incomplete",
        "scientific_status": (
            "conversion_uncertain" if semantic_uncertain else "converted"
        ),
        "remaining_disclosures": remaining_disclosures,
        "mode_values": mode_values,
        "required_files": {
            "reproduction": sorted(required & reproduction_files),
            "autonomous": sorted(required & autonomous_files),
            "autonomous_extra_files": sorted(autonomous_files - required),
        },
        "deliverable_closure": deliverable_closure,
        "public_input_fingerprints": {
            "reproduction": reproduction_inputs,
            "autonomous": autonomous_inputs,
            "equal": Counter(reproduction_inputs.values()) == Counter(autonomous_inputs.values()),
        },
        "tree_manifests": {
            "reproduction": directory_manifest(reproduction) if reproduction.is_dir() else None,
            "autonomous": directory_manifest(autonomous) if autonomous.is_dir() else None,
        },
        "self_external_gate": {
            "self_check": stage06b_self_check,
            "external_gate": {
                **(stage06b_external_gate or {}),
                "status": (stage06b_external_gate or {}).get(
                    "status", stage06b_response.get("phase_gate_status", "not_run")
                ),
                "findings": (stage06b_external_gate or {}).get(
                    "findings", external_findings
                ),
            },
            "findings_equal": self_findings == external_findings,
            "snapshot_sha256_equal": bool(
                isinstance(stage06b_self_check, dict)
                and isinstance(stage06b_external_gate, dict)
                and stage06b_self_check.get("snapshot_sha256")
                == stage06b_external_gate.get("snapshot_sha256")
            ),
        },
        "stage06a_gate": stage06a_gate_report or {},
        "disclosure_findings": sorted(set(disclosure_findings)),
        "findings": sorted(set(findings)),
        "created_at": now_utc(),
    }
    write_json(pair_root / "conversion_audit.json", audit)


def _resource_risk_present(value: dict[str, Any]) -> bool:
    status = str(value.get("status") or value.get("cost_status") or "").casefold()
    return status in {
        "uncertain",
        "over_budget",
        "resource_risk",
        "model_estimated_high",
        "infeasible",
    } or bool(value.get("risk_present"))


def _workflow_scope_kind(scope: Any) -> str | None:
    """Project the canonical scope kind for handoff metadata.

    The scientific review contract historically accepted both ``kind`` and
    ``scope_kind``.  This is a transport projection only: it does not infer or
    rank scientific scope, and it keeps the handoff record observable when an
    Agent emits the canonical contract spelling.
    """

    if not isinstance(scope, dict):
        return None
    value = scope.get("kind") or scope.get("scope_kind")
    if value is None:
        return None
    text = str(value).strip()
    return text or None


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
    handoff_ready: bool = True,
) -> None:
    """Write provenance for Stage07 without judging the candidate's science."""

    paper_info_path = root / "paper_info.json"
    if not paper_info_path.is_file():
        write_json(
            paper_info_path,
            {
                "paper_id": paper_id,
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
            "decision": decision,
            "handoff_ready": handoff_ready,
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
    task_pair_id = canonical_paper_id(paper_id)
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
        handoff_warnings=[],
        handoff_ready=False,
    )
    write_manifest(staging, staging / "task_pair_manifest.json")
    target = stage_root / "provisional_rejections" / safe_component(paper_id)
    atomic_commit_tree(staging, target)
    scope = review.get("workflow_scope") or {}
    complexity = review.get("complexity_profile") or {}
    return {
        **record_header(run_id=run_id, stage="stage06", paper_id=paper_id),
        "candidate_id": candidate_id,
        "paper_id": task_pair_id,
        "processing_status": "completed",
        "decision": "provisional_not_constructible",
        "scientific_status": "scientific_not_constructible",
        "contract_status": "not_applicable",
        "handoff_ready": False,
        "passed": False,
        "retryable": False,
        "failure_code": review.get("failure_code"),
        "failure_reasons": review.get("failure_reasons") or [],
        "workflow_scope_kind": _workflow_scope_kind(scope) or "none",
        "complexity_profile": json.loads(
            json.dumps(complexity, ensure_ascii=False)
        ),
        "toolbox_gap_present": any(
            _toolbox_requirement_status(row) in {"missing", "unknown", "incompatible"}
            for row in review.get("toolbox_requirements") or []
        ),
        "task_pair_path": str(target),
        "handoff_path": str(target),
        "source_snapshot_path": str(snapshot["root"]),
        "agent_runs": {"task_pair_builder": agent_audit},
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
        "paper_id": task_pair_id,
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
        "paper_id": None,
        "processing_status": "failed",
        "decision": "artifact_delivery_failure_retryable",
        "handoff_ready": False,
        "passed": False,
        "retryable": True,
        "failure_class": failure_class,
        "error": {"error_type": failure_class, "message": message[:4000]},
        "agent_run": agent_run,
    }
