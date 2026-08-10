from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from src.contracts import read_jsonl, record_header, safe_component, write_json, write_jsonl
from src.core.concurrency import ordered_parallel_map
from src.prompts import (
    STAGE06_AUTONOMOUS_SYSTEM,
    STAGE06_AUTONOMOUS_VERSION,
    STAGE06_REPRODUCTION_SYSTEM,
    STAGE06_REPRODUCTION_VERSION,
    STAGE06_SHARED_SYSTEM,
    STAGE06_SHARED_VERSION,
)


def run_stage06(
    *, candidates, stage04_records, documents, config, model, workspace: Path, run_id: str
):
    stage_root = workspace / "stage_06_task_builder"
    coverage = {row["paper_id"]: row for row in stage04_records}
    documents_by_paper: dict[str, list[dict[str, Any]]] = {}
    for document in documents:
        if document.get("decision") == "pass":
            documents_by_paper.setdefault(document["paper_id"], []).append(document)

    def build(candidate):
        paper_id = candidate["paper_id"]
        candidate_id = candidate["candidate_id"]
        try:
            evidence_ids = set(candidate.get("evidence_ids") or [])
            paper_documents = documents_by_paper.get(paper_id, [])
            evidence_blocks = [
                block
                for document in paper_documents
                for block in read_jsonl(document["content_blocks_path"])
                if block.get("evidence_id") in evidence_ids
            ]
            packet = {
                "candidate": candidate,
                "source_evidence_blocks": evidence_blocks,
                "source_documents": [
                    {
                        "document_id": document["document_id"],
                        "document_role": document.get("document_role"),
                        "file_name": document.get("file_name"),
                        "sha256": document.get("sha256"),
                    }
                    for document in paper_documents
                ],
                "frozen_toolbox": {
                    "profile_id": coverage[paper_id].get("toolbox_profile_id"),
                    "catalog_hash": coverage[paper_id].get("toolbox_catalog_hash"),
                    "software_mappings": coverage[paper_id].get("software_mappings"),
                },
                "resource_profile": coverage[paper_id].get("resource_profile"),
                "disclosure_policy": config.get("disclosure_policy") or {},
            }
            if not evidence_blocks:
                return _abstain(run_id, paper_id, candidate_id, ["candidate_evidence_not_resolved"])
            shared, shared_audit = model.call_json(
                namespace="stage06_shared",
                record_id=candidate_id,
                prompt_version=STAGE06_SHARED_VERSION,
                system_prompt=STAGE06_SHARED_SYSTEM,
                user_content=json.dumps(packet, ensure_ascii=False),
                max_tokens=int(config.get("shared_max_tokens", 6144)),
            )
            _validate_shared(shared, candidate)
            if shared.get("status") != "candidate_ready":
                return _abstain(
                    run_id,
                    paper_id,
                    candidate_id,
                    shared.get("abstention_reasons") or ["builder_abstained"],
                )
            autonomous, autonomous_audit = model.call_json(
                namespace="stage06_autonomous",
                record_id=candidate_id,
                prompt_version=STAGE06_AUTONOMOUS_VERSION,
                system_prompt=STAGE06_AUTONOMOUS_SYSTEM,
                user_content=json.dumps(
                    _public_builder_packet(shared, "autonomous"), ensure_ascii=False
                ),
                max_tokens=int(config.get("mode_max_tokens", 6144)),
            )
            reproduction, reproduction_audit = model.call_json(
                namespace="stage06_reproduction",
                record_id=candidate_id,
                prompt_version=STAGE06_REPRODUCTION_VERSION,
                system_prompt=STAGE06_REPRODUCTION_SYSTEM,
                user_content=json.dumps(
                    _public_builder_packet(shared, "reproduction"), ensure_ascii=False
                ),
                max_tokens=int(config.get("mode_max_tokens", 6144)),
            )
            audit = deterministic_builder_audit(shared, autonomous, reproduction)
            decision = "built" if audit["passed"] else "validation_failed"
            task_pair_id = str(shared.get("task_pair_id") or candidate_id)
            target = stage_root / safe_component(task_pair_id)
            _write_task_pair(
                target,
                shared,
                autonomous,
                reproduction,
                audit,
                {
                    "shared": shared_audit,
                    "autonomous": autonomous_audit,
                    "reproduction": reproduction_audit,
                },
            )
            return {
                **record_header(run_id=run_id, stage="stage06", paper_id=paper_id),
                "candidate_id": candidate_id,
                "task_pair_id": task_pair_id,
                "processing_status": "completed",
                "decision": decision,
                "passed": audit["passed"],
                "task_pair_path": str(target),
                "deterministic_audit": audit,
            }
        except Exception as exc:
            return {
                **record_header(run_id=run_id, stage="stage06", paper_id=paper_id),
                "candidate_id": candidate_id,
                "processing_status": "failed",
                "decision": "processing_failed",
                "passed": False,
                "error": {"error_type": type(exc).__name__, "message": str(exc)},
            }

    records = ordered_parallel_map(
        build, candidates, max_workers=int(config.get("workers", model.config.get("workers", 1)))
    )
    write_jsonl(stage_root / "build_results.jsonl", records)
    summary = {
        **record_header(run_id=run_id, stage="stage06"),
        "candidates": len(candidates),
        "built": sum(row.get("passed", False) for row in records),
        "abstained_or_failed": sum(not row.get("passed", False) for row in records),
        "model_role": model.role,
        "model": model.model,
    }
    write_json(stage_root / "stage_summary.json", summary)
    return {"records": records, "summary": summary}


def deterministic_builder_audit(shared, autonomous, reproduction):
    findings = []
    if autonomous.get("mode") != "autonomous" or reproduction.get("mode") != "reproduction":
        findings.append("mode_mismatch")
    task_pair_id = shared.get("task_pair_id")
    if (
        autonomous.get("task_pair_id") != task_pair_id
        or reproduction.get("task_pair_id") != task_pair_id
    ):
        findings.append("task_pair_id_mismatch")
    if not shared.get("evidence_map") or not shared.get("hidden_reference"):
        findings.append("missing_private_reference")
    for label, mode in (("autonomous", autonomous), ("reproduction", reproduction)):
        if mode.get("status") != "candidate_ready":
            findings.append(f"{label}_not_ready")
        if not mode.get("task_markdown") or not mode.get("task_info"):
            findings.append(f"{label}_missing_task_content")
    hidden_strings = _answer_strings(shared.get("hidden_reference"))
    public_text = json.dumps(
        {"autonomous": autonomous, "reproduction": reproduction}, ensure_ascii=False
    )
    leaked = [value for value in hidden_strings if len(value) >= 6 and value in public_text]
    if leaked:
        findings.append("hidden_answer_leakage")
    return {"passed": not findings, "findings": findings, "leaked_values": leaked[:20]}


def _validate_shared(shared, candidate):
    if shared.get("candidate_id") != candidate.get("candidate_id"):
        raise ValueError("Builder shared record candidate_id mismatch")
    if shared.get("status") not in {"candidate_ready", "abstain"}:
        raise ValueError("Builder shared status must be candidate_ready or abstain")
    if shared.get("status") == "candidate_ready" and not shared.get("task_pair_id"):
        raise ValueError("ready shared record requires task_pair_id")


def _public_builder_packet(shared, mode):
    # Public task writers never receive hidden_reference.  They only see the
    # scientific record and an explicit allowlist of public construction fields.
    return {
        "mode": mode,
        "task_pair_id": shared.get("task_pair_id"),
        "scientific_record": shared.get("scientific_record"),
        "required_assets": shared.get("required_assets"),
        "allowed_backends": shared.get("allowed_backends"),
        "allowed_actions": shared.get("allowed_actions"),
        "budget": shared.get("budget"),
    }


def _write_task_pair(root, shared, autonomous, reproduction, audit, model_audit):
    write_json(root / "shared" / "scientific_record.json", shared.get("scientific_record"))
    write_json(root / "shared" / "hidden_reference.json", shared.get("hidden_reference"))
    write_json(root / "evidence_map.json", shared.get("evidence_map"))
    hidden = shared.get("hidden_reference") or {}
    write_json(root / "target_study" / "ground_truth.json", hidden.get("ground_truth"))
    write_json(root / "scoring" / "rubric.json", hidden.get("scoring_rubric"))
    for name, value in (("autonomous", autonomous), ("reproduction", reproduction)):
        write_json(root / name / "task_info.json", value.get("task_info"))
        path = root / name / "task.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(str(value.get("task_markdown") or ""), encoding="utf-8")
    write_json(root / "builder_audit.json", {"deterministic": audit, "model_calls": model_audit})


def _answer_strings(value):
    output = []
    if isinstance(value, dict):
        for key, item in value.items():
            if any(word in str(key).casefold() for word in ("answer", "target", "value", "result")):
                output.extend(_answer_strings(item))
            elif isinstance(item, (dict, list)):
                output.extend(_answer_strings(item))
    elif isinstance(value, list):
        for item in value:
            output.extend(_answer_strings(item))
    elif value is not None:
        output.append(str(value))
    return output


def _abstain(run_id, paper_id, candidate_id, reasons):
    return {
        **record_header(run_id=run_id, stage="stage06", paper_id=paper_id),
        "candidate_id": candidate_id,
        "processing_status": "completed",
        "decision": "abstain",
        "passed": False,
        "abstention_reasons": reasons,
    }
