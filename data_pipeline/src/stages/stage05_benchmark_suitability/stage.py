from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from src.contracts import decision_counts, read_jsonl, record_header, write_json, write_jsonl
from src.core.concurrency import ordered_parallel_map
from src.prompts import STAGE05_SYSTEM, STAGE05_VERSION, TASK_DIRECTIONS


def run_stage05(*, stage04_records, documents, config, model, workspace: Path, run_id: str):
    stage_root = workspace / "stage_05_benchmark_suitability"
    by_paper: dict[str, list[dict[str, Any]]] = {}
    for document in documents:
        if document.get("decision") == "pass":
            by_paper.setdefault(document["paper_id"], []).append(document)
    eligible = [row for row in stage04_records if row.get("passed")]

    def assess(record):
        paper_id = record["paper_id"]
        try:
            blocks = [
                block
                for document in by_paper.get(paper_id, [])
                for block in read_jsonl(document["content_blocks_path"])
            ]
            # Stage04 evidence IDs refer to the coarse GROBID text.  MinerU creates a
            # new block namespace, so Stage05 selects relevant sections from the deep
            # document instead of trying to reuse stale coarse-parser IDs.
            evidence = [
                block for block in blocks if _result_section(block) or _computational_block(block)
            ]
            evidence_blocks = _bounded(
                evidence or blocks, int(config.get("max_evidence_characters", 120000))
            )
            packet = {
                "paper_id": paper_id,
                "taxonomy": list(TASK_DIRECTIONS),
                "stage04": _without_evidence_ids(
                    {
                        key: record.get(key)
                        for key in (
                            "workflow_inventory",
                            "software_mappings",
                            "resource_profile",
                            "toolbox_profile_id",
                            "toolbox_catalog_hash",
                        )
                    }
                ),
                "evidence_blocks": evidence_blocks,
                "requirements": {"minimum_dependent_steps": 3, "candidate_limit": 3},
                "evidence_contract": {
                    "source": "stage04_mineru_deep_normalization",
                    "cite_only_evidence_block_ids_from_this_packet": True,
                },
            }
            response, audit = model.call_json(
                namespace="stage05_suitability",
                record_id=paper_id,
                prompt_version=STAGE05_VERSION,
                system_prompt=STAGE05_SYSTEM,
                user_content=json.dumps(packet, ensure_ascii=False),
                max_tokens=int(config.get("max_tokens", 4096)),
            )
            evidence_ids = {str(block["evidence_id"]) for block in evidence_blocks}
            candidates, validation_rejections = _validate_candidates(response, evidence_ids, record)
            response_attempts = [{"response": response, "audit": audit}]
            if (
                str(response.get("decision") or "").casefold() == "pass"
                and not candidates
                and validation_rejections
                and bool(config.get("contract_retry", True))
            ):
                retry_response, retry_audit = model.call_json(
                    namespace="stage05_suitability_contract_retry",
                    record_id=f"{paper_id}-contract-retry",
                    prompt_version=f"{STAGE05_VERSION}-contract-retry-v1",
                    system_prompt=(
                        f"{STAGE05_SYSTEM}\nYour previous response failed deterministic schema "
                        "validation. Return a corrected complete JSON object. Use one exact taxonomy "
                        "identifier for task_direction, arrays for workflow_steps, validation_gates, "
                        "scoring_metrics, required_software, and evidence_ids, and cite only evidence "
                        "IDs present in evidence_blocks. Do not change the scientific conclusion merely "
                        "to avoid a validation error."
                    ),
                    user_content=json.dumps(
                        {
                            **packet,
                            "previous_response": response,
                            "validation_rejections": validation_rejections,
                        },
                        ensure_ascii=False,
                    ),
                    max_tokens=int(config.get("max_tokens", 4096)),
                )
                response_attempts.append({"response": retry_response, "audit": retry_audit})
                response, audit = retry_response, retry_audit
                candidates, validation_rejections = _validate_candidates(
                    response, evidence_ids, record
                )
            if candidates:
                decision = "pass"
            elif str(response.get("decision") or "").casefold() == "abstain":
                decision = "abstain"
            else:
                decision = "contract_invalid"
            abstention_reasons = response.get("abstention_reasons") or []
            if decision == "contract_invalid" and not abstention_reasons:
                abstention_reasons = [
                    f"{item['candidate_id']}: {', '.join(item['reasons'])}"
                    for item in validation_rejections
                ] or ["model_pass_without_valid_candidate"]
            return {
                **record_header(run_id=run_id, stage="stage05", paper_id=paper_id),
                "processing_status": "completed",
                "decision": decision,
                "passed": bool(candidates),
                "candidates": candidates,
                "abstention_reasons": abstention_reasons,
                "validation_rejections": validation_rejections,
                "model_response": response,
                "model_response_attempts": response_attempts,
                "model_audit": audit,
            }
        except Exception as exc:
            return {
                **record_header(run_id=run_id, stage="stage05", paper_id=paper_id),
                "processing_status": "failed",
                "decision": "processing_failed",
                "passed": False,
                "candidates": [],
                "error": {"error_type": type(exc).__name__, "message": str(exc)},
            }

    records = ordered_parallel_map(
        assess, eligible, max_workers=int(config.get("workers", model.config.get("workers", 1)))
    )
    candidates = [
        {"paper_id": row["paper_id"], **candidate}
        for row in records
        for candidate in row.get("candidates") or []
    ]
    write_jsonl(stage_root / "decisions.jsonl", records)
    write_jsonl(stage_root / "candidates.jsonl", candidates)
    write_jsonl(
        stage_root / "abstentions.jsonl", [row for row in records if row["decision"] != "pass"]
    )
    summary = {
        **record_header(run_id=run_id, stage="stage05"),
        "papers": len(records),
        "decisions": decision_counts(records),
        "passed": sum(row["passed"] for row in records),
        "processing_errors": sum(row["processing_status"] == "failed" for row in records),
        "run_status": (
            "infrastructure_failed"
            if records and all(row["processing_status"] == "failed" for row in records)
            else "completed_with_errors"
            if any(row["processing_status"] == "failed" for row in records)
            else "completed"
        ),
        "candidates": len(candidates),
        "model_role": model.role,
        "model": model.model,
    }
    write_json(stage_root / "stage_summary.json", summary)
    return {"records": records, "candidates": candidates, "summary": summary}


def _validate_candidates(response, evidence_ids, stage04):
    output: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    software_lookup = _covered_software_lookup(stage04)
    for index, candidate in enumerate((response.get("candidates") or [])[:3]):
        if not isinstance(candidate, dict):
            rejected.append(
                {
                    "candidate_id": f"candidate-{index + 1}",
                    "reasons": ["candidate_not_an_object"],
                }
            )
            continue
        normalized = dict(candidate)
        candidate_id = str(
            candidate.get("candidate_id") or f"{stage04['paper_id']}-candidate-{index + 1}"
        )
        reasons: list[str] = []
        direction = candidate.get("task_direction") or candidate.get("direction")
        if direction not in TASK_DIRECTIONS:
            reasons.append("invalid_task_direction")
        normalized["task_direction"] = direction
        normalized.pop("direction", None)
        for field in (
            "workflow_steps",
            "validation_gates",
            "scoring_metrics",
            "evidence_ids",
        ):
            normalized[field] = _string_list(candidate.get(field))
        if (
            len(normalized["workflow_steps"]) < 3
            or not normalized["validation_gates"]
            or not normalized["scoring_metrics"]
        ):
            reasons.append("incomplete_workflow_validation_or_scoring")
        if candidate.get("ground_truth_level") not in {"A", "B", "C", "D"}:
            reasons.append("invalid_ground_truth_level")
        if not all(
            candidate.get(key)
            for key in (
                "scientific_question",
                "claim_reference",
                "public_input_requirements",
                "hidden_targets",
                "significance_rationale",
            )
        ):
            reasons.append("missing_required_scientific_fields")
        cited = set(normalized["evidence_ids"])
        if not cited or not cited.issubset(evidence_ids):
            reasons.append("unknown_or_missing_mineru_evidence_ids")
        required = _software_list(candidate.get("required_software"))
        normalized_required = []
        unknown_software = []
        for name in required:
            identifier = software_lookup.get(_software_key(name))
            if identifier:
                normalized_required.append(identifier)
            else:
                unknown_software.append(name)
        if not required:
            reasons.append("required_software_missing")
        if unknown_software:
            reasons.append("required_software_not_stage04_covered")
        normalized["required_software"] = list(dict.fromkeys(normalized_required))
        normalized["candidate_id"] = candidate_id
        if reasons:
            rejected.append(
                {
                    "candidate_id": candidate_id,
                    "reasons": list(dict.fromkeys(reasons)),
                    "unknown_software": unknown_software,
                    "unknown_evidence_ids": sorted(cited - evidence_ids),
                }
            )
            continue
        output.append(normalized)
    return output, rejected


def _covered_software_lookup(stage04):
    lookup: dict[str, str] = {}
    for row in stage04.get("software_mappings") or []:
        if not row.get("catalog_present"):
            continue
        identifier = str(
            row.get("normalized_identifier")
            or row.get("normalized_backend")
            or row.get("raw_name")
            or ""
        )
        if not identifier:
            continue
        for value in (
            identifier,
            row.get("normalized_backend"),
            row.get("raw_name"),
        ):
            if value:
                lookup[_software_key(value)] = identifier
    return lookup


def _software_list(value):
    values = _string_list(value)
    output = []
    for item in values:
        output.extend(part.strip() for part in re.split(r"[,;]", item) if part.strip())
    return list(dict.fromkeys(output))


def _string_list(value):
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if value in (None, ""):
        return []
    return [str(value).strip()]


def _software_key(value):
    return re.sub(r"[^a-z0-9+]", "", str(value).casefold())


def _without_evidence_ids(value):
    if isinstance(value, dict):
        return {
            key: _without_evidence_ids(item) for key, item in value.items() if key != "evidence_ids"
        }
    if isinstance(value, list):
        return [_without_evidence_ids(item) for item in value]
    return value


def _result_section(block):
    section = " ".join(block.get("section_path") or []).casefold()
    return any(
        word in section for word in ("result", "discussion", "conclusion", "method", "comput")
    )


def _computational_block(block):
    text = str(block.get("text") or "").casefold()
    return any(
        term in text
        for term in (
            "density functional",
            "molecular dynamics",
            "quantum chem",
            "computational method",
            "calculation was performed",
            "calculations were performed",
            "basis set",
            "force field",
        )
    )


def _bounded(blocks, limit):
    output, size = [], 0
    for block in blocks:
        compact = {
            key: block.get(key)
            for key in ("evidence_id", "document_id", "page", "section_path", "text")
        }
        if output and size + len(str(compact["text"])) > limit:
            break
        output.append(compact)
        size += len(str(compact["text"]))
    return output
