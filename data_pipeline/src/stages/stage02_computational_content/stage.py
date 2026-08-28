from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from src.contracts import decision_counts, read_jsonl, record_header, write_json, write_jsonl
from src.core.concurrency import ordered_parallel_map
from src.model_client import RoleModelClient
from src.prompts import (
    STAGE02_CLASSIFY_SYSTEM,
    STAGE02_CLASSIFY_VERSION,
    STAGE02_PASS_VERIFY_SYSTEM,
    STAGE02_PASS_VERIFY_VERSION,
)
from src.stages.stage02_computational_content.adjudication import (
    NON_ORIGINAL_ARTICLE_ROLES,
    PASS_DECISIONS,
    apply_pass_verification,
    sanitize_classification,
)
from src.stages.stage02_computational_content.evidence import build_evidence_packet
from src.stages.stage02_computational_content.workflows import (
    WORKFLOW_CONTRACT_VERSION,
    compact_candidate_skeletons,
    sanitize_workflow_candidates,
    sanitize_workflow_verifications,
)

COMPUTATIONAL_CONTENT_IMPLEMENTATION_VERSION = (
    "v2-stage02-computational-content-20260814-r17-article-role-lock"
)

CONTENT_CONFIRMATION_DECISIONS = set(PASS_DECISIONS)

DECISIONS = {
    *CONTENT_CONFIRMATION_DECISIONS,
    "computational_workflow_not_benchmarkable",
    "computational_content_not_found",
    "non_original_article",
    "uncertain",
}


def run_stage02(
    *,
    papers: list[dict[str, Any]],
    documents: list[dict[str, Any]],
    config: dict[str, Any],
    model: RoleModelClient,
    workspace: Path,
    run_id: str,
    on_result=None,
) -> dict[str, Any]:
    stage_root = workspace / "stage_02_computational_content"
    document_by_id = {row["document_id"]: row for row in documents if row.get("decision") == "pass"}
    eligible = [row for row in papers if _is_stage02_eligible(row)]

    def review(
        paper: dict[str, Any],
    ) -> tuple[
        dict[str, Any],
        dict[str, Any] | None,
        list[dict[str, Any]],
        list[dict[str, Any]],
    ]:
        semantic_calls_started = 0
        completed_model_audits: list[dict[str, Any]] = []
        try:
            source_blocks = [
                {
                    **block,
                    "document_role": document_by_id[document_id].get("document_role"),
                }
                for document_id in paper.get("document_ids") or []
                if document_id in document_by_id
                for block in read_jsonl(document_by_id[document_id]["content_blocks_path"])
            ]
            article_guard = _non_original_article_guard(paper, source_blocks)
            if article_guard:
                record = {
                    **record_header(run_id=run_id, stage="stage02", paper_id=paper["paper_id"]),
                    "title": paper.get("title"),
                    "doi": paper.get("doi"),
                    "journal_name": paper.get("journal_name"),
                    "article_url": paper.get("article_url"),
                    "processing_status": "completed",
                    "decision": "non_original_article",
                    "passed": False,
                    "review": article_guard,
                    "validated_evidence": [],
                    "validated_author_experiment_evidence": [],
                    "skipped_nonsemantic_blocks": 0,
                    "reduce_validation_warnings": [],
                    "model_audit": {"model_called": False, "deterministic_guard": True},
                }
                return record, None, [], []
            blocks = [block for block in source_blocks if not _is_atomic_coordinate_dump(block)]
            skipped_nonsemantic_blocks = len(source_blocks) - len(blocks)
            metadata = _paper_metadata(paper)
            packet = build_evidence_packet(
                paper_metadata=metadata,
                blocks=blocks,
                config=config,
            )
            deterministic_experiments = _find_deterministic_author_experiments(blocks)
            visible_deterministic_experiments = _visible_deterministic_experiments(
                deterministic_experiments,
                limit=int(config.get("max_deterministic_experiment_evidence", 8)),
            )
            packet["deterministic_author_experiment_evidence"] = visible_deterministic_experiments
            visible_experiment_ids = [
                str(item.get("evidence_id") or "")
                for item in visible_deterministic_experiments
                if item.get("evidence_id")
            ]
            packet["valid_evidence_ids"] = list(
                dict.fromkeys([*packet["valid_evidence_ids"], *visible_experiment_ids])
            )
            packet["rule_screen"]["deterministic_author_experiment_hits"] = len(
                deterministic_experiments
            )
            valid_ids = set(packet["valid_evidence_ids"])
            computational_ids = {
                str(item.get("evidence_id") or "")
                for item in packet["computational_evidence"]
                if item.get("evidence_id")
            }
            experiment_ids = set(visible_experiment_ids)
            experimental_candidate_ids = {
                str(item.get("evidence_id") or "")
                for item in packet["experimental_evidence"]
                if item.get("evidence_id")
            } | experiment_ids
            if not packet["rule_screen"]["computation_candidate"]:
                response = {
                    "decision": "computational_content_not_found",
                    "article_role": "original_research",
                    "performed_computation": "no",
                    "complete_computational_workflow": "no",
                    "benchmarkable_computational_workflow": "no",
                    "author_performed_experiments": "yes" if experiment_ids else "uncertain",
                    "computation_role": "none",
                    "evidence_direction": "none",
                    "study_mode": "noncomputational",
                    "central_claims": [],
                    "computational_workflow_steps": [],
                    "experimental_contributions": [],
                    "counterfactual_without_computation": "main_claim_survives",
                    "counterfactual_without_experiments": "uncertain",
                    "evidence_ids": [],
                    "experimental_evidence_ids": [],
                    "conflicting_evidence_ids": [],
                    "method_families": [],
                    "computational_actions": [],
                    "software_clues": [],
                    "resource_clues": [],
                    "rationale": "No substantive computational-chemistry signal was found in parsed main/SI text.",
                    "confidence": 1.0,
                    "passed": False,
                    "verification": {
                        "computation_complete": False,
                        "workflow_benchmarkable": False,
                        "computation_central": False,
                        "verified_author_experiment_ids": sorted(experiment_ids),
                        "computation_required_claims": 0,
                        "minimum_confidence": float(config.get("minimum_confidence", 0.85)),
                    },
                }
                workflow_candidates: list[dict[str, Any]] = []
                workflow_verification: list[dict[str, Any]] = []
                confirmed_workflows: list[dict[str, Any]] = []
                audits = {"model_called": False, "zero_call_rule_rejection": True}
                validation_warnings: list[dict[str, Any]] = []
                attempts: list[dict[str, Any]] = []
            else:
                semantic_calls_started += 1
                raw_response, primary_audit = _call_complete_json(
                    model,
                    namespace="stage02_classify",
                    record_id=paper["paper_id"],
                    prompt_version=STAGE02_CLASSIFY_VERSION,
                    system_prompt=STAGE02_CLASSIFY_SYSTEM,
                    user_content=json.dumps(packet, ensure_ascii=False),
                    max_tokens=int(config.get("classification_max_tokens", 2048)),
                )
                completed_model_audits.append(primary_audit)
                response, validation_warnings, review_reasons = sanitize_classification(
                    raw_response,
                    valid_ids=valid_ids,
                    computational_ids=computational_ids,
                    deterministic_experiment_ids=experiment_ids,
                    minimum_confidence=float(config.get("minimum_confidence", 0.85)),
                )
                workflow_candidates, candidate_warnings = sanitize_workflow_candidates(
                    raw_response,
                    valid_ids=valid_ids,
                    computational_ids=computational_ids,
                    limit=int(config.get("workflow_candidate_limit", 3)),
                )
                validation_warnings.extend(candidate_warnings)
                workflow_verification = []
                confirmed_workflows = []
                attempts = [
                    {
                        "paper_id": paper["paper_id"],
                        "eval_id": paper.get("eval_id"),
                        "attempt": "primary",
                        "raw_response": raw_response,
                        "validated_response": response,
                        "validation_warnings": validation_warnings,
                        "review_reasons": review_reasons,
                        "model_audit": primary_audit,
                    }
                ]
                review_audit = None
                # Every paper with deterministic computation signals receives one independent
                # workflow verification. This also recovers first-pass false negatives.
                review_enabled = bool(config.get("review_pass_decisions", True))
                locked_article_role = str(response.get("article_role") or "unknown")
                pass_precision_review = (
                    review_enabled and locked_article_role == "original_research"
                )
                if pass_precision_review:
                    review_payload = {
                        "article_type_lock": {
                            "article_role": locked_article_role,
                            "mutable": False,
                        },
                        "evidence_packet": _compact_pass_verification_packet(packet),
                        "workflow_candidates": compact_candidate_skeletons(
                            workflow_candidates
                        ),
                    }
                    semantic_calls_started += 1
                    retry_raw, review_audit = _call_complete_json(
                        model,
                        namespace="stage02_pass_verify",
                        record_id=paper["paper_id"],
                        prompt_version=STAGE02_PASS_VERIFY_VERSION,
                        system_prompt=STAGE02_PASS_VERIFY_SYSTEM,
                        user_content=json.dumps(review_payload, ensure_ascii=False),
                        max_tokens=int(config.get("pass_verification_max_tokens", 768)),
                    )
                    completed_model_audits.append(review_audit)
                    retry_response, retry_warnings = apply_pass_verification(
                        response,
                        retry_raw,
                        valid_ids=valid_ids,
                        computational_ids=computational_ids,
                        experimental_candidate_ids=experimental_candidate_ids,
                        minimum_confidence=float(config.get("minimum_confidence", 0.85)),
                    )
                    attempts.append(
                        {
                            "paper_id": paper["paper_id"],
                            "eval_id": paper.get("eval_id"),
                            "attempt": "pass_precision_review",
                            "raw_response": retry_raw,
                            "validated_response": retry_response,
                            "validation_warnings": retry_warnings,
                            "review_reasons": [],
                            "model_audit": review_audit,
                        }
                    )
                    response = retry_response
                    workflow_verification, confirmed_workflows, workflow_warnings = (
                        sanitize_workflow_verifications(
                            retry_raw,
                            candidates=workflow_candidates,
                            valid_ids=valid_ids,
                            computational_ids=computational_ids,
                            minimum_confidence=float(
                                config.get("minimum_confidence", 0.85)
                            ),
                        )
                    )
                    validation_warnings = [*retry_warnings, *workflow_warnings]
                    if response.get("passed") and not confirmed_workflows:
                        response["decision"] = "uncertain"
                        response["passed"] = False
                        response.setdefault("verification", {})[
                            "confirmed_workflow_contract_ok"
                        ] = False
                        validation_warnings.append(
                            {
                                "field": "confirmed_workflows",
                                "reason": "pass_without_confirmed_workflow",
                            }
                        )
                    else:
                        response.setdefault("verification", {})[
                            "confirmed_workflow_contract_ok"
                        ] = bool(confirmed_workflows)
                elif not review_enabled:
                    # Explicit legacy/test mode. Production configs keep the verifier
                    # enabled; callers that disable it retain the pre-v1 behavior.
                    confirmed_workflows = (
                        list(workflow_candidates) if response.get("passed") else []
                    )
                    workflow_verification = [
                        {
                            "workflow_id": candidate["workflow_id"],
                            "confirmed": True,
                            "status": "verification_bypassed_by_config",
                            "evidence_ids": candidate.get("evidence_ids") or [],
                            "computational_evidence_ids": [
                                value
                                for value in candidate.get("evidence_ids") or []
                                if value in computational_ids
                            ],
                            "confidence": response.get("confidence", 0.0),
                        }
                        for candidate in confirmed_workflows
                    ]
                else:
                    # Non-original and unresolved article types cannot be promoted by
                    # workflow verification. Keep candidate evidence for audit, but do
                    # not spend a second model call or publish confirmed workflows.
                    confirmed_workflows = []
                    workflow_verification = [
                        {
                            "workflow_id": candidate["workflow_id"],
                            "confirmed": False,
                            "status": "blocked_by_article_role",
                            "article_role": locked_article_role,
                            "evidence_ids": candidate.get("evidence_ids") or [],
                            "computational_evidence_ids": [],
                            "confidence": 0.0,
                        }
                        for candidate in workflow_candidates
                    ]
                audits = {
                    "model_called": True,
                    "calls": len(attempts),
                    "successful_http_requests": sum(
                        _audit_http_requests(attempt.get("model_audit") or {})
                        for attempt in attempts
                    ),
                    "primary": primary_audit,
                    "review": review_audit,
                    "review_skip_reason": (
                        f"article_role:{locked_article_role}"
                        if review_enabled and not pass_precision_review
                        else None
                    ),
                }

            article_role = str(response.get("article_role") or "unknown")
            if article_role in NON_ORIGINAL_ARTICLE_ROLES:
                response["decision"] = "non_original_article"
                response["passed"] = False
                confirmed_workflows = []
            elif article_role != "original_research":
                response["decision"] = "uncertain"
                response["passed"] = False
                confirmed_workflows = []
            response["workflow_candidates"] = workflow_candidates
            response["workflow_verification"] = workflow_verification
            response["confirmed_workflows"] = confirmed_workflows
            response["workflow_contract_version"] = WORKFLOW_CONTRACT_VERSION

            decision = str(response.get("decision") or "uncertain")
            if decision not in DECISIONS:
                raise ValueError(f"invalid Stage02 decision: {decision}")
            record = {
                **record_header(run_id=run_id, stage="stage02", paper_id=paper["paper_id"]),
                "title": paper.get("title"),
                "doi": paper.get("doi"),
                "journal_name": paper.get("journal_name"),
                "article_url": paper.get("article_url"),
                "processing_status": "completed",
                "decision": decision,
                "passed": decision in PASS_DECISIONS,
                "workflow_contract_version": WORKFLOW_CONTRACT_VERSION,
                "workflow_candidates": workflow_candidates,
                "workflow_verification": workflow_verification,
                "confirmed_workflows": confirmed_workflows,
                "review": response,
                "validated_evidence": _selected_packet_evidence(packet),
                "validated_author_experiment_evidence": deterministic_experiments,
                "skipped_nonsemantic_blocks": skipped_nonsemantic_blocks,
                "reduce_validation_warnings": validation_warnings,
                "model_audit": audits,
            }
            packet_record = {
                "paper_id": paper["paper_id"],
                **packet,
                "deterministic_author_experiment_ids": sorted(experiment_ids),
            }
            return record, packet_record, attempts, []
        except Exception as exc:
            failure_audit = exc.audit if isinstance(exc, Stage02ModelCallError) else None
            if failure_audit:
                completed_model_audits.append(failure_audit)
            error = {
                "paper_id": paper["paper_id"],
                "error_type": type(exc).__name__,
                "message": str(exc),
            }
            record = {
                **record_header(run_id=run_id, stage="stage02", paper_id=paper["paper_id"]),
                "title": paper.get("title"),
                "doi": paper.get("doi"),
                "journal_name": paper.get("journal_name"),
                "article_url": paper.get("article_url"),
                "processing_status": "failed",
                "decision": "processing_failed",
                "passed": False,
                "error": error,
                "model_audit": {
                    "model_called": semantic_calls_started > 0,
                    "calls_started": semantic_calls_started,
                    "calls_completed": len(completed_model_audits),
                    "successful_http_requests": sum(
                        _audit_http_requests(audit) for audit in completed_model_audits
                    ),
                    "http_request_count_complete": not any(
                        audit.get("http_requests_unknown") for audit in completed_model_audits
                    ),
                    "failed_call": failure_audit,
                },
            }
            return record, None, [], [error]

    reviewed = ordered_parallel_map(
        review,
        eligible,
        max_workers=int(config.get("workers", model.config.get("workers", 1))),
        on_complete=(
            (lambda _completed, _total, _index, paper, result: on_result(paper, result[0]))
            if on_result is not None
            else None
        ),
    )
    records = [item[0] for item in reviewed]
    packet_rows = [item[1] for item in reviewed if item[1] is not None]
    review_rows = [row for item in reviewed for row in item[2]]
    errors = [row for item in reviewed for row in item[3]]
    write_jsonl(stage_root / "decisions.jsonl", records)
    write_jsonl(stage_root / "evidence_packets.jsonl", packet_rows)
    write_jsonl(stage_root / "review_attempts.jsonl", review_rows)
    write_jsonl(stage_root / "processing_errors.jsonl", errors)
    write_jsonl(
        stage_root / "rejected.jsonl",
        [
            row
            for row in records
            if row["decision"]
            in {
                "computational_workflow_not_benchmarkable",
                "computational_content_not_found",
                "non_original_article",
            }
        ],
    )
    write_jsonl(
        stage_root / "held.jsonl",
        [row for row in records if row["decision"] in {"uncertain", "processing_failed"}],
    )
    summary = {
        **record_header(run_id=run_id, stage="stage02"),
        "input_papers": len(papers),
        "eligible_papers": len(eligible),
        "ineligible_papers": len(papers) - len(eligible),
        "papers": len(records),
        "decisions": decision_counts(records),
        "passed": sum(row["passed"] for row in records),
        "processing_errors": len(errors),
        "model_calls": sum(
            int(
                (row.get("model_audit") or {}).get(
                    "calls_started", (row.get("model_audit") or {}).get("calls", 0)
                )
            )
            for row in records
        ),
        "completed_model_calls": sum(
            int(
                (row.get("model_audit") or {}).get(
                    "calls_completed", (row.get("model_audit") or {}).get("calls", 0)
                )
            )
            for row in records
        ),
        "successful_model_http_requests": sum(
            int((row.get("model_audit") or {}).get("successful_http_requests") or 0)
            for row in records
        ),
        "papers_with_incomplete_http_request_audit": sum(
            (row.get("model_audit") or {}).get("http_request_count_complete") is False
            for row in records
        ),
        "papers_with_model_calls": sum(
            bool((row.get("model_audit") or {}).get("model_called")) for row in records
        ),
        "zero_call_rejections": sum(
            bool((row.get("model_audit") or {}).get("zero_call_rule_rejection")) for row in records
        ),
        "conflict_reviews": sum(
            any(row.get("attempt") == "contract_conflict_review" for row in item[2])
            for item in reviewed
        ),
        "pass_precision_reviews": sum(
            any(row.get("attempt") == "pass_precision_review" for row in item[2])
            for item in reviewed
        ),
        "model_role": model.role,
        "model": model.model,
    }
    write_json(stage_root / "stage_summary.json", summary)
    return {"records": records, "summary": summary}


def _selected_packet_evidence(packet: dict[str, Any]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    seen: set[str] = set()
    for key in ("narrative_evidence", "computational_evidence", "experimental_evidence"):
        for block in packet.get(key) or []:
            evidence_id = str(block.get("evidence_id") or "")
            if not evidence_id or evidence_id in seen:
                continue
            seen.add(evidence_id)
            output.append(block)
    return output


def _compact_pass_verification_packet(packet: dict[str, Any]) -> dict[str, Any]:
    def compact(blocks: list[dict[str, Any]]) -> list[dict[str, Any]]:
        output = []
        for block in blocks:
            output.append(
                {
                    key: block.get(key)
                    for key in (
                        "evidence_id",
                        "document_id",
                        "document_role",
                        "page",
                        "section_path",
                    )
                }
                | {"text": str(block.get("text") or "")[:1400]}
            )
        return output

    return {
        "paper_metadata": packet.get("paper_metadata") or {},
        "narrative_evidence": compact(packet.get("narrative_evidence") or []),
        "computational_evidence": compact(packet.get("computational_evidence") or []),
        "experimental_evidence": compact(packet.get("experimental_evidence") or []),
        "deterministic_author_experiment_evidence": packet.get(
            "deterministic_author_experiment_evidence"
        )
        or [],
    }


def _is_stage02_eligible(paper: dict[str, Any]) -> bool:
    """Accept only Stage01 rows whose main paper and every known SI parsed successfully."""
    if paper.get("decision") != "pass" or paper.get("main_parse_ok") is not True:
        return False
    if paper.get("partial_si_parse", False):
        return False
    if paper.get("package_status") == "complete_with_si":
        return paper.get("supplementary_parse_ok") is True
    return paper.get("supplementary_parse_ok") is not False


_NON_ORIGINAL_TITLE_RE = re.compile(
    r"^\s*(?P<role>correction|corrigendum|erratum|retraction|editorial|commentary)\b",
    re.IGNORECASE,
)
_NON_ORIGINAL_TEXT_PATTERNS = (
    (
        "review",
        re.compile(
            r"\b(?:in|for)\s+this\s+(?:brief\s+|short\s+)?review\b|"
            r"\bthis\s+review\s+(?:summarizes|surveys|discusses|covers|highlights)\b|"
            r"\bwe\s+(?:herein\s+)?highlight\s+the\s+advances\s+that\s+have\s+been\s+made\b",
            re.IGNORECASE,
        ),
    ),
    (
        "perspective",
        re.compile(
            r"\bin\s+this\s+perspective\b|"
            r"\bthis\s+perspective\s+(?:explores|discusses|summarizes|highlights)\b",
            re.IGNORECASE,
        ),
    ),
    (
        "commentary",
        re.compile(
            r"\b(?:[A-Z][A-Za-z-]+(?:,\s*[A-Z][A-Za-z-]+)*,?\s+and\s+)?"
            r"colleagues\s+report\s+in\s+(?:Nature|Science|Cell|Chem)\b|"
            r"\brecently\s+in\s+(?:the\s+)?Journal\s+of\s+the\s+American\s+Chemical\s+Society,"
            r".{0,240}\b(?:co-?workers?|colleagues)\s+reported\b|"
            r"\bthis\s+commentary\b",
            re.IGNORECASE | re.DOTALL,
        ),
    ),
)


def _paper_metadata(paper: dict[str, Any]) -> dict[str, Any]:
    return {
        key: paper.get(key)
        for key in ("title", "doi", "journal_name", "article_url")
        if paper.get(key)
    }


def _non_original_article_guard(
    paper: dict[str, Any], blocks: list[dict[str, Any]]
) -> dict[str, Any] | None:
    title = str(paper.get("title") or "").strip()
    title_match = _NON_ORIGINAL_TITLE_RE.search(title)
    if title_match:
        role = title_match.group("role").casefold()
        return _non_original_review(role, title, "title")

    front_text = "\n".join(str(block.get("text") or "") for block in blocks[:8])[:12000]
    for role, pattern in _NON_ORIGINAL_TEXT_PATTERNS:
        match = pattern.search(front_text)
        if match:
            return _non_original_review(role, match.group(0), "front_matter")
    return None


def _non_original_review(role: str, quote: str, source: str) -> dict[str, Any]:
    normalized_role = (
        "editorial"
        if role in {"editorial", "commentary"}
        else "correction"
        if role in {"correction", "corrigendum", "erratum", "retraction"}
        else role
    )
    return {
        "decision": "non_original_article",
        "article_role": normalized_role,
        "performed_computation": "uncertain",
        "computation_role": "background_only",
        "evidence_direction": "none",
        "study_mode": "noncomputational",
        "author_performed_experiments": "uncertain",
        "workflow_complete": "no",
        "method_families": [],
        "computational_actions": [],
        "software_clues": [],
        "resource_clues": [],
        "evidence_ids": [],
        "experimental_evidence_ids": [],
        "conflicting_evidence_ids": [],
        "article_type_evidence": {"source": source, "exact_quote": quote[:500]},
        "rationale": f"Deterministic article-type guard identified a {role} article.",
        "confidence": "high",
    }


_DETERMINISTIC_LAB_ACTION_RE = re.compile(
    r"\b(?:experiments?|measurements?)\s+(?:were|was)\s+"
    r"(?:performed|conducted|carried\s+out)|"
    r"\b(?:spectra|images?|micrographs?)\s+(?:were|was)\s+"
    r"(?:recorded|measured|acquired|collected)|"
    r"\bwe\s+(?:synthesi[sz]ed|prepared|fabricated|purified|isolated|grew|measured|"
    r"recorded|acquired|collected|characteri[sz]ed|tested|assayed|irradiated)\b|"
    r"\bin\s+this\s+study,?\s+we\s+combine\b.{0,180}\bexperimental\s+methods?\b",
    re.IGNORECASE,
)
_SENTENCE_BOUNDARY_RE = re.compile(r"(?<=[.!?])\s+")


def _find_deterministic_author_experiments(
    blocks: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Recall explicit current-author laboratory work independently of the LLM."""

    output: list[dict[str, Any]] = []
    for block in blocks:
        text = str(block.get("text") or "")
        sentences = _SENTENCE_BOUNDARY_RE.split(" ".join(text.split()))
        for index, sentence in enumerate(sentences):
            quote = sentence.strip()
            if not quote or not _DETERMINISTIC_LAB_ACTION_RE.search(quote):
                continue
            attribution_context = " ".join(sentences[max(0, index - 2) : index + 1])
            if _EXTERNAL_EXPERIMENT_RE.search(attribution_context):
                continue
            if not _LABORATORY_TECHNIQUE_RE.search(quote):
                continue
            item = {
                "evidence_id": str(block.get("evidence_id") or ""),
                "exact_quote": quote[:500],
                "experiment_type": "physical laboratory measurement or preparation",
                "attribution": "this_paper",
                "confidence": "high",
                "source": "deterministic_full_text_scan",
            }
            if _is_explicit_author_laboratory_evidence(item):
                output.append(item)
    return _deduplicate_quoted_evidence(output)


def _deduplicate_quoted_evidence(
    values: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for item in values:
        key = (str(item.get("evidence_id") or ""), str(item.get("exact_quote") or ""))
        if not all(key) or key in seen:
            continue
        seen.add(key)
        output.append(item)
    return output


def _visible_deterministic_experiments(
    values: list[dict[str, Any]], *, limit: int
) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    seen_ids: set[str] = set()
    for item in values:
        evidence_id = str(item.get("evidence_id") or "")
        if not evidence_id or evidence_id in seen_ids:
            continue
        seen_ids.add(evidence_id)
        output.append(item)
        if len(output) >= max(1, limit):
            break
    return output


def _chunks(blocks: list[dict[str, Any]], limit: int) -> list[list[dict[str, Any]]]:
    chunks, _skipped = _chunks_with_stats(blocks, limit)
    return chunks


def _chunks_with_stats(
    blocks: list[dict[str, Any]], limit: int
) -> tuple[list[list[dict[str, Any]]], int]:
    if limit < 1:
        raise ValueError("Stage02 chunk character limit must be positive")
    chunks: list[list[dict[str, Any]]] = []
    current: list[dict[str, Any]] = []
    size = 0
    skipped_coordinate_segments = 0
    for block in blocks:
        compact = {
            key: block.get(key)
            for key in ("evidence_id", "document_id", "page", "section_path", "block_type", "text")
        }
        text = str(compact.get("text") or "")
        segments = _split_text_by_utf8_bytes(text, limit)
        for segment_index, segment in enumerate(segments):
            if _is_atomic_coordinate_dump({"text": segment}):
                segment = _strip_atomic_coordinate_sequences(segment)
                skipped_coordinate_segments += 1
                if len(segment.split()) < 4:
                    continue
            segmented = {
                **compact,
                "text": segment,
                "segment_index": segment_index,
                "segment_count": len(segments),
            }
            block_size = len(
                json.dumps(segmented, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
            )
            if current and size + block_size > limit:
                chunks.append(current)
                current, size = [], 0
            current.append(segmented)
            size += block_size
    if current:
        chunks.append(current)
    return chunks, skipped_coordinate_segments


def _call_complete_json(
    model: RoleModelClient,
    *,
    namespace: str,
    record_id: str,
    prompt_version: str,
    system_prompt: str,
    user_content: str,
    max_tokens: int,
) -> tuple[dict[str, Any], dict[str, Any]]:
    try:
        response, audit = model.call_json(
            namespace=namespace,
            record_id=record_id,
            prompt_version=prompt_version,
            system_prompt=system_prompt,
            user_content=user_content,
            max_tokens=max_tokens,
        )
    except Exception as exc:
        raise Stage02ModelCallError(
            f"{namespace} request failed: {exc}",
            audit={"http_requests_unknown": True, "failed": True},
        ) from exc
    if audit.get("finish_reason") != "length":
        return response, audit

    try:
        retry_response, retry_audit = model.call_json(
            namespace=f"{namespace}_complete_retry",
            record_id=f"{record_id}-complete-retry",
            prompt_version=f"{prompt_version}-complete-retry-v1",
            system_prompt=(
                f"{system_prompt}\nThe previous response was truncated. Return a complete, compact JSON "
                "object. Use at most two items in every evidence array and shorten non-quote strings."
            ),
            user_content=user_content,
            # The retry prompt is deliberately compact, but thinking models still
            # need enough output budget to finish reasoning before emitting JSON.
            max_tokens=max(2048, min(max_tokens, 8192)),
        )
    except Exception as exc:
        raise Stage02ModelCallError(
            f"{namespace} compact retry failed: {exc}",
            audit={
                "http_requests": _audit_http_requests(audit),
                "http_requests_unknown": True,
                "initial_audit": audit,
                "failed": True,
            },
        ) from exc
    http_requests = _audit_http_requests(audit) + _audit_http_requests(retry_audit)
    if retry_audit.get("finish_reason") == "length":
        raise Stage02ModelCallError(
            f"{namespace} response remained truncated after compact retry",
            audit={
                "http_requests": http_requests,
                "initial_audit": audit,
                "retry_audit": retry_audit,
                "failed": True,
            },
        )
    return retry_response, {
        **retry_audit,
        "truncation_retry": True,
        "truncation_retry_count": retry_audit.get("truncation_retry_count", 1),
        "initial_finish_reason": "length",
        "initial_request_hash": audit.get("request_hash"),
        "http_requests": http_requests,
    }


def _audit_http_requests(audit: dict[str, Any]) -> int:
    if audit.get("cache_hit"):
        return 0
    if isinstance(audit.get("http_requests"), int):
        return max(0, int(audit["http_requests"]))
    if audit.get("http_requests_unknown"):
        return 0
    return max(1, int(audit.get("attempts") or 1))


class Stage02ModelCallError(RuntimeError):
    def __init__(self, message: str, *, audit: dict[str, Any]) -> None:
        super().__init__(message)
        self.audit = audit


def _split_text_by_utf8_bytes(text: str, limit: int) -> list[str]:
    if not text:
        return [""]
    segments: list[str] = []
    current: list[str] = []
    size = 0
    for character in text:
        character_size = len(character.encode("utf-8"))
        if current and size + character_size > limit:
            segments.append("".join(current))
            current, size = [], 0
        current.append(character)
        size += character_size
    if current:
        segments.append("".join(current))
    return segments


_NUMBER_TOKEN_RE = re.compile(r"^[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[Ee][+-]?\d+)?$")
_ATOM_TOKEN_RE = re.compile(r"^(?:[A-Z][a-z]?|[A-Z][a-z]?\d+)$")
_COORDINATE_NUMBER = r"[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[Ee][+-]?\d+)?"
_ATOMIC_COORDINATE_RUN_RE = re.compile(
    rf"(?:\b[A-Z][a-z]?\s+{_COORDINATE_NUMBER}\s+{_COORDINATE_NUMBER}\s+"
    rf"{_COORDINATE_NUMBER}(?:\s+|$)){{12,}}"
)


def _is_atomic_coordinate_dump(block: dict[str, Any]) -> bool:
    text = str(block.get("text") or "")
    if len(text) < 500:
        return False
    tokens = text.split()
    if len(tokens) < 80:
        return False
    numeric = sum(bool(_NUMBER_TOKEN_RE.fullmatch(token.rstrip(",;"))) for token in tokens)
    if numeric / len(tokens) < 0.65:
        return False
    labels = [
        token.rstrip(",;:")
        for token in tokens
        if not _NUMBER_TOKEN_RE.fullmatch(token.rstrip(",;"))
    ]
    if not labels:
        return False
    atom_labels = sum(bool(_ATOM_TOKEN_RE.fullmatch(token)) for token in labels)
    return atom_labels / len(labels) >= 0.8


def _strip_atomic_coordinate_sequences(text: str) -> str:
    return " ".join(_ATOMIC_COORDINATE_RUN_RE.sub(" ", text).split())


def _reduce_evidence_packet(
    evidence: list[dict[str, Any]],
    *,
    max_items: int,
    max_quote_characters: int,
) -> list[dict[str, Any]]:
    confidence_order = {"high": 0, "medium": 1, "low": 2}
    ranked = sorted(
        enumerate(evidence),
        key=lambda pair: (
            confidence_order.get(str(pair[1].get("confidence") or "low"), 3),
            pair[0],
        ),
    )
    selected = [item for _index, item in ranked[: max(1, max_items)]]
    return [
        {
            "evidence_id": item.get("evidence_id"),
            "exact_quote": str(item.get("exact_quote") or "")[: max(1, max_quote_characters)],
            "method_family": str(item.get("method_family") or "")[:120],
            "action": str(item.get("action") or "")[:240],
            "software_clues": _compact_string_list(item.get("software_clues"), 8, 80),
            "result_clues": _compact_string_list(item.get("result_clues"), 4, 120),
            "confidence": item.get("confidence"),
        }
        for item in selected
    ]


def _compact_string_list(value: Any, max_items: int, max_characters: int) -> list[str]:
    if isinstance(value, list):
        values = value
    elif value is None or value == "":
        values = []
    else:
        values = [value]
    return [str(item)[:max_characters] for item in values[:max_items]]


def _compact_chunk_review(review: dict[str, Any]) -> dict[str, Any]:
    response = review.get("response") or {}
    return {
        "chunk_index": review.get("chunk_index"),
        "has_computational_evidence": bool(response.get("has_computational_evidence")),
        "validated_evidence_count": len(review.get("validated_evidence") or []),
        "validated_experiment_count": len(review.get("validated_experiments") or []),
        "background_only_count": len(response.get("background_only_evidence") or []),
        "conflict_count": len(response.get("conflicts") or []),
    }


def _sanitize_reduce_response(
    response: dict[str, Any],
    valid_ids: set[str],
    *,
    experiment_ids: set[str] | None = None,
    allow_primary_mixed: bool = True,
    minimum_confidence: float = 0.75,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    sanitized = dict(response)
    warnings: list[dict[str, Any]] = []
    experiment_ids = experiment_ids or set()
    id_fields = {
        "evidence_ids": valid_ids,
        "experimental_evidence_ids": experiment_ids,
        "conflicting_evidence_ids": valid_ids | experiment_ids,
    }
    for field, allowed_ids in id_fields.items():
        raw = response.get(field) or []
        values = raw if isinstance(raw, list) else []
        known = _deduplicate([str(item) for item in values if str(item) in allowed_ids], 24)
        unknown = [str(item) for item in values if str(item) not in allowed_ids]
        sanitized[field] = known
        if unknown:
            warnings.append({"field": field, "reason": "unknown_evidence_ids", "values": unknown})
    for field in (
        "method_families",
        "computational_actions",
        "software_clues",
        "resource_clues",
    ):
        sanitized[field] = _deduplicate_string_values(response.get(field), 24, 160)

    if (
        sanitized.get("decision") in CONTENT_CONFIRMATION_DECISIONS
        and not sanitized["evidence_ids"]
    ):
        sanitized["decision"] = "uncertain"
        sanitized["confidence"] = "low"
        warnings.append(
            {
                "field": "decision",
                "reason": "confirmed_without_validated_evidence_downgraded",
            }
        )
    actual_computation = sanitized.get("performed_computation") == "yes"
    if actual_computation and _lacks_target_chemistry_computation(sanitized):
        sanitized["performed_computation"] = "no"
        sanitized["computation_role"] = "none"
        sanitized["study_mode"] = "noncomputational"
        sanitized["workflow_complete"] = "no"
        actual_computation = False
        warnings.append(
            {
                "field": "performed_computation",
                "reason": "target_computational_chemistry_evidence_missing",
            }
        )
    verified_author_experiments = bool(experiment_ids)
    if not actual_computation:
        if sanitized.get("decision") in {
            *CONTENT_CONFIRMATION_DECISIONS,
            "not_pure_computational",
        }:
            sanitized["decision"] = "computational_content_not_found"
            sanitized["computation_role"] = "none"
            sanitized["study_mode"] = "noncomputational"
            sanitized["workflow_complete"] = "no"
            warnings.append(
                {
                    "field": "decision",
                    "reason": "noncomputational_record_normalized",
                }
            )
    elif verified_author_experiments:
        sanitized["author_performed_experiments"] = "yes"
        sanitized["study_mode"] = (
            "mixed_computational_experimental"
            if sanitized.get("computation_role") == "primary"
            else "experimental_with_computational_support"
        )
    elif sanitized.get("author_performed_experiments") == "yes" or (
        actual_computation
        and (
            sanitized.get("decision") == "not_pure_computational"
            or sanitized.get("study_mode")
            in {"mixed_computational_experimental", "experimental_with_computational_support"}
        )
    ):
        sanitized["author_performed_experiments"] = "uncertain"
        sanitized["study_mode"] = "uncertain"
        sanitized["decision"] = "uncertain"
        warnings.append(
            {
                "field": "author_performed_experiments",
                "reason": "author_experiment_claim_without_verified_laboratory_evidence",
            }
        )
    if actual_computation:
        confidence = _confidence_number(sanitized.get("confidence"))
        primary_requirements = {
            "article_role": sanitized.get("article_role") == "original_research",
            "performed_computation": sanitized.get("performed_computation") == "yes",
            "computation_role": sanitized.get("computation_role") == "primary",
            "workflow_complete": sanitized.get("workflow_complete") == "yes",
            "minimum_confidence": confidence >= minimum_confidence,
            "validated_computational_evidence": bool(sanitized.get("evidence_ids")),
        }
        failed = [name for name, passed in primary_requirements.items() if not passed]
        if failed:
            sanitized["decision"] = (
                "not_pure_computational"
                if sanitized.get("computation_role") in {"supporting", "background_only", "none"}
                else "uncertain"
            )
            warnings.append(
                {
                    "field": "decision",
                    "reason": "computation_primary_requirements_failed",
                    "requirements": failed,
                }
            )
        elif verified_author_experiments:
            if allow_primary_mixed:
                sanitized["decision"] = "computational_primary_mixed_confirmed"
            else:
                sanitized["decision"] = "not_pure_computational"
            warnings.append(
                {
                    "field": "decision",
                    "reason": (
                        "verified_computation_primary_mixed_study_accepted"
                        if allow_primary_mixed
                        else "verified_author_laboratory_evidence_rejects_pure_computation"
                    ),
                }
            )
        elif (
            sanitized.get("author_performed_experiments") == "no"
            and sanitized.get("study_mode") == "pure_computational"
        ):
            sanitized["decision"] = "computational_content_confirmed"
        else:
            sanitized["decision"] = "uncertain"
            warnings.append(
                {
                    "field": "decision",
                    "reason": "computation_primary_study_mode_unresolved",
                }
            )
    return sanitized, warnings


def _deduplicate(values: list[str], max_items: int) -> list[str]:
    output: list[str] = []
    seen: set[str] = set()
    for value in values:
        key = value.strip().casefold()
        if not key or key in seen:
            continue
        seen.add(key)
        output.append(value.strip())
        if len(output) >= max_items:
            break
    return output


def _deduplicate_string_values(value: Any, max_items: int, max_characters: int) -> list[str]:
    values = value if isinstance(value, list) else ([] if value in (None, "") else [value])
    return _deduplicate([str(item)[:max_characters] for item in values], max_items)


def _confidence_number(value: Any) -> float:
    if isinstance(value, (int, float)):
        return max(0.0, min(1.0, float(value)))
    mapping = {"high": 0.9, "medium": 0.6, "low": 0.3}
    return mapping.get(str(value or "").casefold(), 0.0)


_TARGET_CHEMISTRY_COMPUTATION_RE = re.compile(
    r"\b(?:dft|density functional|ab initio|quantum chem|electronic structure|"
    r"molecular dynamics|atomistic simulation|\bmd\b|qm/mm|monte carlo(?!\s+tree)|"
    r"force field|phonon|vibrational calculation|thermal transport|transition state|"
    r"reaction path|reaction dynamics|quantum dynamics|quasi[- ]classical traject|"
    r"potential energy surface|free[- ]energy|metadynamics|umbrella sampling|"
    r"microkinetic|kinetic model|master equation|rrkm|rate constant|molecular docking|"
    r"tight[- ]binding|wave function|coupled cluster|excited state|tddft|"
    r"thermochemistry|conformer|energy decomposition|electron density|qtaim|bader|"
    r"high[- ]pressure phase|phase stability)\b",
    re.IGNORECASE,
)


def _lacks_target_chemistry_computation(response: dict[str, Any]) -> bool:
    """Require a positive computational-chemistry workflow, independent of product names."""

    descriptors = [
        *(response.get("method_families") or []),
        *(response.get("computational_actions") or []),
        *(response.get("software_clues") or []),
    ]
    text = re.sub(r"[_-]+", " ", " ".join(str(item) for item in descriptors)).strip()
    if not text:
        return False
    return not bool(_TARGET_CHEMISTRY_COMPUTATION_RE.search(text))


def _validate_map(response: dict[str, Any], blocks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        item
        for item in _validate_quoted_items(response.get("evidence"), blocks)
        if str(item.get("attribution") or "").casefold() == "this_paper"
    ]


def _validate_experiment_map(value: Any, blocks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        item
        for item in _validate_quoted_items(value, blocks)
        if str(item.get("attribution") or "").casefold() == "this_paper"
        and _is_explicit_author_laboratory_evidence(item)
        and not _has_external_experiment_context(item, blocks)
    ]


def _has_external_experiment_context(item: dict[str, Any], blocks: list[dict[str, Any]]) -> bool:
    evidence_id = str(item.get("evidence_id") or "")
    quote = str(item.get("exact_quote") or "")
    for block in blocks:
        if str(block.get("evidence_id") or "") != evidence_id:
            continue
        text = " ".join(str(block.get("text") or "").split())
        index = text.find(quote)
        if index >= 0 and _EXTERNAL_EXPERIMENT_RE.search(text[max(0, index - 500) : index]):
            return True
    return False


_COMPUTATIONAL_OPERATION_RE = re.compile(
    r"\b(?:dft|density functional|ab initio|molecular dynamics|\bmd\b|qm/mm|monte carlo|"
    r"simulation|simulated|computational|calculated|computed|predicted|phonon|trajectory|"
    r"free[- ]energy|machine learning|screening|geometry optimization|transition state|"
    r"electronic structure|model(?:ing|ling)?)\b",
    re.IGNORECASE,
)
_EXTERNAL_EXPERIMENT_RE = re.compile(
    r"\b(?:published|previously reported|previous study|taken from|reported by|et al\.|"
    r"database|pdb(?: id)?|"
    r"coworkers?|colleagues|adapted with permission|existing experimental|reference data|"
    r"starts? from|originates? from|derived from)\b",
    re.IGNORECASE,
)
_LABORATORY_ACTION_RE = re.compile(
    r"\b(?:synthesi[sz](?:e|ed|ing|is)|prepared|fabricated|purified|isolated|grew|grown|"
    r"measur(?:e|ed|ing)|recorded|acquired|collected|characteri[sz](?:e|ed|ing)|tested|"
    r"assayed|incubated|cultured|irradiated|electrodeposited|added|stirred|heated|washed|"
    r"centrifuged|filtered|dried|conducted|carried\s+out|performed\s+(?:an?\s+)?"
    r"(?:experiment|measurement|spectroscop|microscop|diffraction|electrochem)|"
    r"(?:experiments?|measurements?)\s+(?:were|was)\s+"
    r"(?:performed|conducted|carried\s+out)|"
    r"combine(?:d|s|ing)?\b.{0,120}\bexperimental\s+methods?)\b",
    re.IGNORECASE,
)
_LABORATORY_TECHNIQUE_RE = re.compile(
    r"\b(?:synthesis|fabrication|purification|isolation|nmr|spectroscopy|spectrometer|"
    r"microscopy|microscope|diffraction|crystallography|xrd|pxrd|xps|xas|xanes|exafs|"
    r"rixs|raman|ftir|infrared|epr|esr|mass spectrometry|hrms|chromatography|hplc|gc-ms|"
    r"calorimetry|scattering|langmuir|voltammetry|electrochemistry|electrochemical|"
    r"battery|assay|cell culture|microscopy|"
    r"catalytic activity|reaction screening|substrate scope|physical testing)\b",
    re.IGNORECASE,
)
_STRONG_LABORATORY_TYPE_RE = re.compile(
    r"\b(?:synthesis|fabrication|purification|isolation|nmr|spectroscopy|microscopy|"
    r"xps|xas|xanes|exafs|rixs|raman|ftir|infrared|epr|esr|mass spectrometry|hrms|"
    r"chromatography|hplc|gc-ms|calorimetry|scattering|langmuir|voltammetry|"
    r"electrochemistry|electrochemical|battery|"
    r"assay|cell culture|magnetometry|magnetization measurement|catalytic activity|"
    r"reaction screening|substrate scope|physical testing)\b",
    re.IGNORECASE,
)


def _is_explicit_author_laboratory_evidence(item: dict[str, Any]) -> bool:
    experiment_type = str(item.get("experiment_type") or "")
    quote = str(item.get("exact_quote") or "")
    combined = f"{experiment_type} {quote}"
    if _EXTERNAL_EXPERIMENT_RE.search(quote):
        return False
    explicit_action = bool(_LABORATORY_ACTION_RE.search(quote))
    laboratory_context = bool(_LABORATORY_TECHNIQUE_RE.search(combined))
    if _COMPUTATIONAL_OPERATION_RE.search(combined) and not _LABORATORY_ACTION_RE.search(quote):
        return False
    return explicit_action and laboratory_context


def _validate_quoted_items(value: Any, blocks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    source = {str(block["evidence_id"]): str(block.get("text") or "") for block in blocks}
    output = []
    evidence = value or []
    if not isinstance(evidence, list):
        return output
    for item in evidence:
        if not isinstance(item, dict):
            continue
        evidence_id = str(item.get("evidence_id") or "")
        quote = str(item.get("exact_quote") or "").strip()
        if evidence_id in source and quote and quote in source[evidence_id]:
            output.append(item)
    return output
