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
            # Stage04 evidence IDs refer to the coarse GROBID text. MinerU creates a
            # new block namespace, so Stage05 uses the deep document stream instead of
            # trying to reuse stale coarse-parser IDs.
            # MinerU's content-list output does not reliably attach section ancestry to
            # paragraph blocks.  Keyword-only selection can therefore retain a heading
            # while dropping the method/result paragraphs below it.  Keep the complete
            # document stream and apply the per-document character budget instead.
            evidence_blocks = _bounded_by_document(
                blocks, int(config.get("max_evidence_characters", 120000))
            )
            packet = {
                "paper_id": paper_id,
                "taxonomy": list(TASK_DIRECTIONS),
                "documents": [
                    {
                        "document_id": document.get("document_id"),
                        "document_role": document.get("document_role"),
                        "title": document.get("title"),
                        "selected_parser": document.get("selected_parser"),
                        "source_name": Path(str(document.get("source_path") or "")).name,
                    }
                    for document in by_paper.get(paper_id, [])
                ],
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
                "software_coverage_facts": _software_coverage_facts(record),
                "evidence_blocks": evidence_blocks,
                "requirements": {
                    "minimum_dependent_steps": 3,
                    "candidate_limit": int(config.get("candidate_limit", 1)),
                },
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
            candidate_limit = int(config.get("candidate_limit", 1))
            candidates, validation_rejections = _validate_candidates(
                response, evidence_ids, record, candidate_limit=candidate_limit
            )
            validation_rejections.extend(_response_contract_rejections(response, record))
            validation_rejections.extend(_software_fact_contradictions(response, record))
            response_attempts = [{"response": response, "audit": audit}]
            if (
                validation_rejections
                and (
                    str(response.get("decision") or "").casefold() == "pass"
                    or any(
                        row.get("candidate_id")
                        in {"response-software-facts", "response-contract"}
                        for row in validation_rejections
                    )
                )
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
                        "scoring_metrics, required_software, and evidence_ids; include estimated_cost "
                        "and all five buildability_checks; treat software_coverage_facts as immutable; "
                        "and cite only evidence "
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
                    response, evidence_ids, record, candidate_limit=candidate_limit
                )
                validation_rejections.extend(_response_contract_rejections(response, record))
                validation_rejections.extend(_software_fact_contradictions(response, record))
            has_response_contradiction = any(
                row.get("candidate_id") in {"response-software-facts", "response-contract"}
                for row in validation_rejections
            )
            if candidates and not has_response_contradiction:
                decision = "pass"
            elif (
                str(response.get("decision") or "").casefold() == "abstain"
                and not has_response_contradiction
            ):
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
                "passed": decision == "pass",
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


def _validate_candidates(response, evidence_ids, stage04, *, candidate_limit=3):
    output: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    software_lookup = _covered_software_lookup(stage04)
    for index, candidate in enumerate((response.get("candidates") or [])[:candidate_limit]):
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
        estimated_cost = candidate.get("estimated_cost")
        if not _valid_estimated_cost(estimated_cost, stage04):
            reasons.append("cost_estimate_missing_invalid_or_over_budget")
        buildability = candidate.get("buildability_checks")
        required_checks = ("input_assets", "parameters", "ground_truth", "software", "cost")
        if not isinstance(buildability, dict) or any(
            buildability.get(key) != "confirmed" for key in required_checks
        ):
            reasons.append("buildability_not_confirmed")
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


def _valid_estimated_cost(value, stage04):
    if not isinstance(value, dict) or not str(value.get("basis") or "").strip():
        return False
    if value.get("confidence") not in {"high", "medium"}:
        return False
    numeric = {}
    for key in ("runtime_hours", "cpu_cores", "gpus", "job_count"):
        raw = value.get(key)
        if isinstance(raw, bool) or not isinstance(raw, (int, float)) or raw < 0:
            return False
        numeric[key] = float(raw)
    if numeric["runtime_hours"] <= 0 or numeric["cpu_cores"] <= 0 or numeric["job_count"] <= 0:
        return False
    budget = (stage04.get("resource_profile") or {}).get("budget") or {}
    comparisons = {
        "runtime_hours": numeric["runtime_hours"],
        "cpu_cores": numeric["cpu_cores"],
        "gpus": numeric["gpus"],
        "job_count": numeric["job_count"],
        "core_hours": numeric["runtime_hours"] * numeric["cpu_cores"],
        "gpu_hours": numeric["runtime_hours"] * numeric["gpus"],
    }
    return not any(
        key in budget and float(budget[key]) < amount for key, amount in comparisons.items()
    )


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


def _software_coverage_facts(stage04):
    covered, uncovered = [], []
    for row in stage04.get("software_mappings") or []:
        fact = {
            "paper_name": row.get("raw_name"),
            "toolbox_identifier": row.get("normalized_identifier")
            or row.get("normalized_backend"),
        }
        (covered if row.get("catalog_present") else uncovered).append(fact)
    return {
        "covered_required_software": covered,
        "uncovered_required_software": uncovered,
        "inventory_status": stage04.get("coverage_decision"),
        "rule": (
            "Only uncovered_required_software may be reported as absent from the toolbox. "
            "A covered entry may still be unusable for a non-software reason, but must not be "
            "described as missing from the catalog."
        ),
    }


def _software_fact_contradictions(response, stage04):
    blocking = _software_list(response.get("blocking_software"))
    if not blocking:
        return []
    if str(response.get("decision") or "").casefold() == "pass":
        return [
            {
                "candidate_id": "response-software-facts",
                "reasons": ["pass_response_has_blocking_software"],
            }
        ]
    uncovered = {
        _software_key(value)
        for row in _software_coverage_facts(stage04)["uncovered_required_software"]
        for value in (row.get("paper_name"), row.get("toolbox_identifier"))
        if value
    }
    invalid = [name for name in blocking if _software_key(name) not in uncovered]
    if not invalid:
        return []
    return [
        {
            "candidate_id": "response-software-facts",
            "reasons": [f"blocking_software_not_in_uncovered_facts:{name}" for name in invalid],
        }
    ]


def _response_contract_rejections(response, stage04):
    decision = str(response.get("decision") or "").casefold()
    dimensions = _string_list(response.get("blocking_dimensions"))
    allowed = {
        "input_assets",
        "parameters",
        "ground_truth",
        "software",
        "cost",
        "scientific_significance",
    }
    blocking_software = _software_list(response.get("blocking_software"))
    inventory_unconfirmed = (
        _software_coverage_facts(stage04).get("inventory_status")
        == "software_inventory_unconfirmed"
    )
    reasons = []
    if decision == "pass" and (dimensions or blocking_software):
        reasons.append("pass_response_has_blockers")
    if decision == "abstain":
        if not dimensions:
            reasons.append("abstain_missing_blocking_dimensions")
        if set(dimensions) - allowed:
            reasons.append("invalid_blocking_dimensions")
        if blocking_software and "software" not in dimensions:
            reasons.append("software_dimension_and_blocking_software_disagree")
        if "software" in dimensions and not (blocking_software or inventory_unconfirmed):
            reasons.append("software_dimension_and_blocking_software_disagree")
    if not reasons:
        return []
    return [{"candidate_id": "response-contract", "reasons": reasons}]


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


def _bounded_by_document(blocks, limit):
    by_document: dict[str, list[dict]] = {}
    for block in blocks:
        document_id = str(block.get("document_id") or "unknown")
        by_document.setdefault(document_id, []).append(block)
    if not by_document:
        return []
    per_document = max(1, int(limit) // len(by_document))
    return [
        block
        for document_blocks in by_document.values()
        for block in _bounded(document_blocks, per_document)
    ]
