from __future__ import annotations

import copy
import json
import re
from html import escape
from pathlib import Path
from typing import Any, Protocol

from src.contracts import (
    decision_counts,
    read_json,
    read_jsonl,
    record_header,
    write_json,
    write_jsonl,
)
from src.core.concurrency import ordered_parallel_map
from src.model_client import RoleModelClient
from src.prompts import STAGE03_SYSTEM, STAGE03_VERSION

REQUIRED_ROLES = {"core_compute", "required_preprocessing", "required_analysis"}
VALID_ROLES = REQUIRED_ROLES | {
    "optional_auxiliary",
    "visualization",
    "instrumentation",
    "background",
    "unknown",
}
SOFTWARE_ENTITY_TYPES = {"program", "library", "service", "extension", "custom_code"}
EXCLUDED_ENTITY_TYPES = {
    "method",
    "algorithm",
    "model",
    "database",
    "dataset",
    "file_format",
    "hardware",
    "parameter",
    "unknown",
}
EXECUTION_LAYERS = {"named_software", "task_specific_python"}
STAGE03_FORWARD_DECISIONS = {
    "software_covered",
    "software_coverage_probable",
    "mixed_workflow_candidate",
    "software_inventory_unconfirmed",
}
_CORE_RUNTIME_ACTION_RE = re.compile(
    r"\b(?:train(?:ing)?|fit(?:ting)?|simulate|simulation|molecular\s+dynamics|"
    r"microkinetic|kinetic\s+model|electronic[ -]structure|quantum\s+chemistry|"
    r"density\s+functional|geometry\s+optimi[sz]ation|docking)\b",
    re.I,
)


class SoftciteLike(Protocol):
    def annotate_tei(self, tei_path: str | Path) -> dict[str, Any]: ...


def run_stage03(
    *,
    stage02_records: list[dict[str, Any]],
    documents: list[dict[str, Any]],
    config: dict[str, Any],
    model: RoleModelClient,
    workspace: Path,
    run_id: str,
    softcite: SoftciteLike | None = None,
) -> dict[str, Any]:
    stage_root = workspace / "stage_03_toolbox_resource_gate"
    profile = read_json(config["toolbox_capabilities"])
    aliases = read_json(config["software_aliases"])
    detection_aliases = _merge_detection_aliases(
        aliases,
        read_json(config["external_software_aliases"])
        if config.get("external_software_aliases")
        else {},
    )
    documents_by_paper: dict[str, list[dict[str, Any]]] = {}
    for document in documents:
        if document.get("decision") == "pass":
            documents_by_paper.setdefault(document["paper_id"], []).append(document)
    eligible = [row for row in stage02_records if row.get("passed")]

    def review(
        record: dict[str, Any],
    ) -> tuple[dict[str, Any], dict[str, Any], list[dict[str, Any]]]:
        paper_id = record["paper_id"]
        try:
            blocks = [
                {**block, "document_role": document.get("document_role")}
                for document in documents_by_paper.get(paper_id, [])
                for block in read_jsonl(document["content_blocks_path"])
            ]
            rule_mentions = find_software_mentions(blocks, detection_aliases)
            executable_cues = find_explicit_executable_cues(blocks, rule_mentions)
            softcite_mentions, softcite_error = _softcite_mentions(
                softcite,
                blocks,
                stage_root / "softcite_input" / f"{paper_id}.tei.xml",
            )
            packet = _bound_prompt_packet(
                {
                    "paper_id": paper_id,
                    "stage02": _compact_stage02_review(record.get("review") or {}),
                    "rule_software_mentions": _compact_rule_mentions(rule_mentions),
                    "explicit_executable_cues": executable_cues,
                    "softcite_mentions": _compact_softcite_mentions(softcite_mentions),
                    "evidence_blocks": _target_blocks(
                        blocks,
                        record,
                        rule_mentions,
                        int(
                            config.get(
                                "max_evidence_payload_bytes",
                                config.get("max_evidence_characters", 9000),
                            )
                        ),
                    ),
                },
                int(config.get("max_prompt_payload_bytes", 18000)),
            )
            raw_response, audit = _call_complete_inventory(
                model,
                paper_id=paper_id,
                packet=packet,
                max_tokens=int(config.get("max_tokens", 4096)),
            )
            raw_response, contract_normalization_warnings = _normalize_inventory_contract(
                raw_response
            )
            contract_errors = _inventory_contract_errors(raw_response)
            if contract_errors:
                raw_response, contract_audit = _repair_inventory_contract(
                    model,
                    paper_id=paper_id,
                    previous_response=raw_response,
                    errors=contract_errors,
                    max_tokens=int(config.get("max_tokens", 4096)),
                )
                audit = {
                    **contract_audit,
                    "contract_retry": True,
                    "initial_request_hash": audit.get("request_hash"),
                    "initial_contract_errors": contract_errors,
                }
            response, validation_warnings = _sanitize_review(
                raw_response,
                {block["evidence_id"]: block["text"] for block in blocks},
            )
            validation_warnings = [*contract_normalization_warnings, *validation_warnings]
            response["software_mentions"] = _merge_explicit_executable_cues(
                response.get("software_mentions") or [], executable_cues
            )
            response["software_mentions"], catalog_warnings = _merge_catalog_actual_use_mentions(
                response.get("software_mentions") or [],
                rule_mentions,
                response.get("workflows") or [],
                {block["evidence_id"]: block["text"] for block in blocks},
                detection_aliases,
            )
            validation_warnings.extend(catalog_warnings)
            binding_warnings = _bind_workflow_steps_to_mentions(
                response.get("workflows") or [],
                response.get("software_mentions") or [],
                detection_aliases,
            )
            validation_warnings.extend(binding_warnings)
            response["software_mentions"], workflow_warnings = _merge_workflow_software_mentions(
                response.get("software_mentions") or [],
                response.get("workflows") or [],
                {block["evidence_id"]: block["text"] for block in blocks},
                detection_aliases,
            )
            validation_warnings.extend(workflow_warnings)
            mappings = resolve_software(response.get("software_mentions") or [], aliases, profile)
            coverage_decision = coverage_gate(response, mappings, profile, config)
            resource = resource_gate(
                response.get("resource_facts") or [], config.get("resource_budget") or {}
            )
            decision = _combine_decision(
                coverage_decision, resource, bool(response.get("inventory_complete"))
            )
            passed = decision in STAGE03_FORWARD_DECISIONS
            output = {
                **record_header(run_id=run_id, stage="stage03", paper_id=paper_id),
                "title": record.get("title"),
                "doi": record.get("doi"),
                "journal_name": record.get("journal_name"),
                "article_url": record.get("article_url"),
                "processing_status": "completed",
                "decision": decision,
                "passed": passed,
                "coverage_decision": coverage_decision,
                "forwarded_for_later_review": passed and decision != "software_covered",
                "workflow_inventory": response.get("workflows") or [],
                "software_mentions": response.get("software_mentions") or [],
                "softcite_mentions": softcite_mentions,
                "softcite_error": softcite_error,
                "software_mappings": mappings,
                "coverage_basis": "native_software_catalog_presence",
                "toolbox_execution_layers": [
                    "predefined_action",
                    "native_software_documentation",
                    "task_specific_python",
                ],
                "resource_profile": resource,
                "inventory_complete": bool(response.get("inventory_complete")),
                "toolbox_profile_id": profile.get("profile_id"),
                "toolbox_catalog_hash": profile.get("screening_snapshot_hash")
                or profile.get("catalog_hash"),
                "model_review": response,
                "model_validation_warnings": validation_warnings,
                "model_audit": audit,
            }
            return output, {"paper_id": paper_id, "mentions": rule_mentions}, []
        except Exception as exc:
            error = {"paper_id": paper_id, "error_type": type(exc).__name__, "message": str(exc)}
            return (
                {
                    **record_header(run_id=run_id, stage="stage03", paper_id=paper_id),
                    "title": record.get("title"),
                    "doi": record.get("doi"),
                    "journal_name": record.get("journal_name"),
                    "article_url": record.get("article_url"),
                    "processing_status": "failed",
                    "decision": "processing_failed",
                    "passed": False,
                    "error": error,
                },
                {"paper_id": paper_id, "mentions": []},
                [error],
            )

    reviewed = ordered_parallel_map(
        review, eligible, max_workers=int(config.get("workers", model.config.get("workers", 1)))
    )
    records = [item[0] for item in reviewed]
    rule_rows = [item[1] for item in reviewed]
    errors = [error for item in reviewed for error in item[2]]
    write_jsonl(stage_root / "decisions.jsonl", records)
    write_jsonl(stage_root / "rule_mentions.jsonl", rule_rows)
    write_jsonl(stage_root / "processing_errors.jsonl", errors)
    write_jsonl(
        stage_root / "rejected.jsonl",
        [
            row
            for row in records
            if row["decision"]
            in {
                "core_software_uncovered",
                "cost_exceeds_budget",
            }
        ],
    )
    write_jsonl(
        stage_root / "held.jsonl",
        [
            row
            for row in records
            if not row["passed"]
            and row not in []
            and row["decision"]
            not in {
                "core_software_uncovered",
                "cost_exceeds_budget",
            }
        ],
    )
    summary = {
        **record_header(run_id=run_id, stage="stage03"),
        "papers": len(records),
        "decisions": decision_counts(records),
        "passed": sum(row["passed"] for row in records),
        "processing_errors": len(errors),
        "model_role": model.role,
        "model": model.model,
        "toolbox_profile_id": profile.get("profile_id"),
        "toolbox_catalog_hash": profile.get("screening_snapshot_hash")
        or profile.get("catalog_hash"),
    }
    write_json(stage_root / "stage_summary.json", summary)
    return {
        "records": records,
        "summary": summary,
    }


def _call_complete_inventory(model, *, paper_id, packet, max_tokens):
    user_content = json.dumps(packet, ensure_ascii=False)
    response, audit = _inventory_model_call(
        model,
        namespace="stage03_inventory",
        record_id=paper_id,
        prompt_version=STAGE03_VERSION,
        system_prompt=STAGE03_SYSTEM,
        user_content=user_content,
        max_tokens=max_tokens,
    )
    if audit.get("finish_reason") != "length":
        return response, audit
    response, retry_audit = _inventory_model_call(
        model,
        namespace="stage03_inventory_complete_retry",
        record_id=f"{paper_id}-complete-retry",
        prompt_version=f"{STAGE03_VERSION}-complete-retry-v1",
        system_prompt=(
            f"{STAGE03_SYSTEM}\nThe previous response was truncated. Return a complete JSON object. "
            "Use at most 2 workflows, 6 total steps, 10 software mentions, 4 resource facts, "
            "4 complexity facts, and 4 unresolved items. Do not repeat evidence prose."
        ),
        user_content=user_content,
        max_tokens=max(max_tokens, 6144),
    )
    if retry_audit.get("finish_reason") == "length":
        response, minimal_audit = _inventory_model_call(
            model,
            namespace="stage03_inventory_minimal_retry",
            record_id=f"{paper_id}-minimal-retry",
            prompt_version=f"{STAGE03_VERSION}-minimal-retry-v1",
            system_prompt=_minimal_inventory_system_prompt(),
            user_content=json.dumps(_minimal_inventory_packet(packet), ensure_ascii=False),
            max_tokens=max(max_tokens, 6144),
        )
        if minimal_audit.get("finish_reason") == "length":
            raise ValueError("Stage03 inventory response remained truncated after minimal retry")
        return response, {
            **minimal_audit,
            "truncation_retry": True,
            "minimal_retry": True,
            "initial_finish_reason": "length",
            "initial_request_hash": audit.get("request_hash"),
            "compact_retry_request_hash": retry_audit.get("request_hash"),
        }
    return response, {
        **retry_audit,
        "truncation_retry": True,
        "initial_finish_reason": "length",
        "initial_request_hash": audit.get("request_hash"),
    }


def _repair_inventory_contract(model, *, paper_id, previous_response, errors, max_tokens):
    user_content = json.dumps(
        {
            "previous_contract_errors": errors,
            "previous_response": _compact_contract_source(previous_response),
        },
        ensure_ascii=False,
    )
    response, audit = _inventory_model_call(
        model,
        namespace="stage03_inventory_contract_retry",
        record_id=f"{paper_id}-contract-retry",
        prompt_version=f"{STAGE03_VERSION}-contract-retry-v1",
        system_prompt=_contract_repair_system_prompt(),
        user_content=user_content,
        max_tokens=max(max_tokens, 6144),
    )
    response, _ = _normalize_inventory_contract(response)
    retry_errors = _inventory_contract_errors(response)
    if not retry_errors and audit.get("finish_reason") != "length":
        return response, {**audit, "contract_retry_count": 1}

    response, final_audit = _inventory_model_call(
        model,
        namespace="stage03_inventory_contract_minimal_retry",
        record_id=f"{paper_id}-contract-minimal-retry",
        prompt_version=f"{STAGE03_VERSION}-contract-minimal-retry-v1",
        system_prompt=_contract_repair_system_prompt(minimal=True),
        user_content=user_content,
        max_tokens=max(max_tokens, 6144),
    )
    response, _ = _normalize_inventory_contract(response)
    final_errors = _inventory_contract_errors(response)
    if final_audit.get("finish_reason") == "length" or final_errors:
        raise ValueError(
            "Stage03 inventory response violated its contract after retries: "
            + "; ".join(final_errors[:8])
        )
    return response, {
        **final_audit,
        "contract_retry_count": 2,
        "compact_contract_retry": True,
        "contract_retry_request_hash": audit.get("request_hash"),
    }


def _normalize_inventory_contract(response):
    """Normalize common JSON enum/primitive mistakes without changing scientific claims."""

    if not isinstance(response, dict):
        return response, []
    normalized = copy.deepcopy(response)
    warnings = []
    for index, mention in enumerate(normalized.get("software_mentions") or []):
        if not isinstance(mention, dict):
            continue
        entity_type = str(mention.get("entity_type") or "").casefold()
        role = str(mention.get("role") or "").casefold()
        if entity_type in VALID_ROLES:
            mention["entity_type"] = "program"
            if role not in VALID_ROLES:
                mention["role"] = entity_type
            warnings.append(
                {
                    "field": "software_mentions.entity_type",
                    "index": index,
                    "reason": "role_value_moved_out_of_entity_type",
                    "original_value": entity_type,
                }
            )
    for workflow in normalized.get("workflows") or []:
        if not isinstance(workflow, dict):
            continue
        for step in workflow.get("steps") or []:
            if not isinstance(step, dict):
                continue
            if isinstance(step.get("essential"), str):
                step["essential"] = step["essential"].strip().casefold() not in {
                    "false",
                    "no",
                    "0",
                    "",
                }
            if str(step.get("software") or "").strip().casefold() in {"none", "null"}:
                step["software"] = None
    return normalized, warnings


def _minimal_inventory_system_prompt():
    return """Extract a compact evidence-grounded software inventory. Return exactly one JSON object with keys
inventory_complete, workflows, software_mentions, excluded_entities, resource_facts, complexity_facts,
unresolved, evidence_ids, confidence, rationale. Use at most 1 workflow with 4 step objects and 10 software
mention objects. Every step object has step_id, action, essential, execution_layer, software, normalized_backend=null,
reported_settings, evidence_ids. Every software object has raw_name, normalized_hint, entity_type, role,
actual_use, workflow_ids, evidence_ids, exact_quote. entity_type is exactly program, library, service,
extension, or custom_code. role is exactly core_compute, required_preprocessing, required_analysis,
optional_auxiliary, visualization, instrumentation, background, or unknown. Put methods, algorithms, models,
databases and datasets in excluded_entities as objects. Keep VASPsol separate from VASP. Set resource_facts=[]
and complexity_facts=[]. Arrays never contain bare strings except reported_settings, unresolved, and evidence_ids.
execution_layer is named_software or task_specific_python. Core scientific engines always use named_software;
task_specific_python is only for short transparent analysis of outputs from named engines.
Example step: {"step_id":"s1","action":"run DFT","essential":true,"execution_layer":"named_software","software":"VASP",
"normalized_backend":null,"reported_settings":["PBE"],"evidence_ids":["ev1"]}.
Example mention: {"raw_name":"VASP","normalized_hint":"vasp","entity_type":"program",
"role":"core_compute","actual_use":true,"workflow_ids":["wf1"],"evidence_ids":["ev1"],
"exact_quote":"calculations used VASP"}. Return compact JSON only."""


def _contract_repair_system_prompt(*, minimal=False):
    limit = "Use at most 1 workflow, 4 steps and 10 software mentions. " if minimal else ""
    return f"""Reformat the supplied previous_response; do not re-review the paper and do not invent evidence.
Return exactly one JSON object with keys inventory_complete, workflows, software_mentions, excluded_entities,
resource_facts, complexity_facts, unresolved, evidence_ids, confidence, rationale. {limit}Every workflow and step
is an object. A step has step_id, action, essential, execution_layer, software, normalized_backend=null, reported_settings and
evidence_ids. Every software mention is an object with raw_name, normalized_hint, entity_type, role, actual_use,
workflow_ids, evidence_ids and exact_quote. entity_type is one of program, library, service, extension,
custom_code. execution_layer is named_software or task_specific_python; only short transparent analysis may use
task_specific_python, never a core scientific engine. role is one of core_compute, required_preprocessing, required_analysis, optional_auxiliary,
visualization, instrumentation, background, unknown. Move methods, algorithms, models, databases and datasets
to excluded_entities objects. Preserve exact quotes and evidence IDs. Arrays never contain bare strings except
reported_settings, unresolved and evidence_ids. Return compact JSON only."""


def _minimal_inventory_packet(packet):
    evidence_blocks = []
    for block in (packet.get("evidence_blocks") or [])[:10]:
        evidence_blocks.append(
            {
                "evidence_id": block.get("evidence_id"),
                "document_role": block.get("document_role"),
                "section_path": block.get("section_path"),
                "text": _truncate_utf8(str(block.get("text") or ""), 700),
            }
        )
    return {
        "paper_id": packet.get("paper_id"),
        "rule_software_mentions": (packet.get("rule_software_mentions") or [])[:16],
        "explicit_executable_cues": (packet.get("explicit_executable_cues") or [])[:16],
        "softcite_mentions": (packet.get("softcite_mentions") or [])[:8],
        "evidence_blocks": evidence_blocks,
    }


def _compact_contract_source(response):
    if not isinstance(response, dict):
        return response
    return {
        "inventory_complete": response.get("inventory_complete"),
        "workflows": _compact_json_value(
            response.get("workflows") or [], max_items=8, max_string=180
        ),
        "software_mentions": _compact_json_value(
            response.get("software_mentions") or [], max_items=20, max_string=220
        ),
        "excluded_entities": _compact_json_value(
            response.get("excluded_entities") or [], max_items=16, max_string=180
        ),
        "unresolved": _compact_json_value(
            response.get("unresolved") or [], max_items=8, max_string=180
        ),
        "evidence_ids": (response.get("evidence_ids") or [])[:24],
        "confidence": response.get("confidence"),
        "rationale": str(response.get("rationale") or "")[:240],
    }


def _inventory_contract_errors(response):
    if not isinstance(response, dict):
        return ["response_not_object"]
    errors = []
    for field in ("workflows", "software_mentions"):
        if not isinstance(response.get(field), list):
            errors.append(f"{field}_not_array")
    if errors:
        return errors
    for index, workflow in enumerate(response["workflows"]):
        if not isinstance(workflow, dict):
            errors.append(f"workflows[{index}]_not_object")
            continue
        if not workflow.get("workflow_id"):
            errors.append(f"workflows[{index}]_missing_id")
        if not isinstance(workflow.get("steps"), list):
            errors.append(f"workflows[{index}].steps_not_array")
            continue
        for step_index, step in enumerate(workflow["steps"]):
            if not isinstance(step, dict):
                errors.append(f"workflows[{index}].steps[{step_index}]_not_object")
                continue
            layer = step.get("execution_layer")
            if layer is not None and layer not in EXECUTION_LAYERS:
                errors.append(f"workflows[{index}].steps[{step_index}]_invalid_execution_layer")
    for index, mention in enumerate(response["software_mentions"]):
        if not isinstance(mention, dict):
            errors.append(f"software_mentions[{index}]_not_object")
            continue
        entity_type = mention.get("entity_type")
        if entity_type not in SOFTWARE_ENTITY_TYPES and entity_type not in EXCLUDED_ENTITY_TYPES:
            errors.append(f"software_mentions[{index}]_invalid_entity_type")
        if mention.get("role") not in VALID_ROLES:
            errors.append(f"software_mentions[{index}]_invalid_role")
        if not isinstance(mention.get("raw_name"), str) or not mention.get("raw_name"):
            errors.append(f"software_mentions[{index}]_missing_raw_name")
        for field in ("workflow_ids", "evidence_ids"):
            if not isinstance(mention.get(field), list):
                errors.append(f"software_mentions[{index}].{field}_not_array")
    excluded = response.get("excluded_entities", [])
    if not isinstance(excluded, list):
        errors.append("excluded_entities_not_array")
    else:
        for index, entity in enumerate(excluded):
            if not isinstance(entity, dict):
                errors.append(f"excluded_entities[{index}]_not_object")
    return errors


def _inventory_model_call(
    model,
    *,
    namespace,
    record_id,
    prompt_version,
    system_prompt,
    user_content,
    max_tokens,
):
    effective = _safe_output_tokens(model, system_prompt, user_content, max_tokens)
    response, audit = model.call_json(
        namespace=namespace,
        record_id=record_id,
        prompt_version=prompt_version,
        system_prompt=system_prompt,
        user_content=user_content,
        max_tokens=effective,
    )
    return response, {
        **audit,
        "requested_max_tokens": int(max_tokens),
        "effective_max_tokens": effective,
    }


def _safe_output_tokens(model, system_prompt, user_content, requested):
    model_config = getattr(model, "config", {}) or {}
    context_window = int(model_config.get("context_window_tokens", 16384))
    safety_margin = int(model_config.get("context_safety_margin_tokens", 768))
    payload_bytes = len(f"{system_prompt}\n{user_content}".encode("utf-8", errors="replace"))
    bytes_per_token = float(model_config.get("context_estimated_bytes_per_token", 2.5))
    if bytes_per_token <= 0:
        raise ValueError("context_estimated_bytes_per_token must be positive")
    estimated_input = int(payload_bytes / bytes_per_token) + 256
    available = context_window - estimated_input - safety_margin
    if available < 512:
        raise ValueError(
            "Stage03 prompt leaves fewer than 512 output tokens after context budgeting"
        )
    return min(int(requested), available)


def find_software_mentions(
    blocks: list[dict[str, Any]], aliases: dict[str, list[str]]
) -> list[dict[str, Any]]:
    patterns = []
    for backend, values in aliases.items():
        configured = values or [backend]
        for alias in configured:
            if len(alias.strip()) >= 2:
                # Acronyms remain case-sensitive to avoid matching ordinary words
                # (for example ORCA/orca), while multiword product names are safe
                # and commonly vary capitalization across publisher text exports.
                flags = (
                    re.I
                    if any(character.isspace() for character in alias)
                    or not any(character.isupper() for character in alias)
                    else 0
                )
                patterns.append(
                    (
                        backend,
                        alias,
                        re.compile(
                            rf"(?<![A-Za-z0-9]){re.escape(alias)}(?![A-Za-z0-9])",
                            flags,
                        ),
                    )
                )
    output = []
    for block in blocks:
        text = str(block.get("text") or "")
        if _reference_section(block):
            continue
        for backend, alias, pattern in patterns:
            match = pattern.search(text)
            if match and not _ambiguous_software_term(backend, match.group(0), text):
                output.append(
                    {
                        "backend_hint": backend,
                        "raw_name": match.group(0),
                        "alias": alias,
                        "evidence_id": block["evidence_id"],
                        "context": _context_window(text, match.start(), match.end(), 1200),
                    }
                )
    unique = {(row["backend_hint"], row["evidence_id"]): row for row in output}
    return list(unique.values())


def _merge_detection_aliases(*sources: dict[str, list[str]]) -> dict[str, list[str]]:
    """Build a recognition vocabulary without changing toolbox availability."""

    merged: dict[str, set[str]] = {}
    for source in sources:
        for identifier, values in source.items():
            bucket = merged.setdefault(str(identifier), set())
            configured = [str(value) for value in values if str(value).strip()]
            bucket.update(configured or [str(identifier)])
    return {
        identifier: sorted(values, key=lambda value: (value.casefold(), value))
        for identifier, values in sorted(merged.items())
    }


_EXECUTABLE_ENTITY_RE = re.compile(
    r"\b(?P<name>[A-Za-z][A-Za-z0-9_.+/-]{1,48})"
    r"(?:\s+(?:version\s*)?v?\d+(?:\.\d+){0,3})?\s+"
    r"(?P<kind>extension|plugin|module|package|software|program|code|library|suite|server)\b",
    re.I,
)
_IMPLEMENTED_EXECUTABLE_RE = re.compile(
    r"\b(?:implemented|integrated|executed)\s+(?:in|with|using|via)\s+(?:the\s+)?"
    r"(?P<name>[A-Za-z][A-Za-z0-9_.+/-]{2,48})\b",
    re.I,
)
_FRAMEWORK_EXECUTABLE_RE = re.compile(
    r"\b(?:applied|implemented|trained|executed|run)\s+(?:within|using|with)\s+(?:the\s+)?"
    r"(?P<name>[A-Za-z][A-Za-z0-9_.+/-]{2,48})\s+framework\b",
    re.I,
)
_KNOWN_EXTENSION_RE = re.compile(
    r"\b(?P<name>VASP\s*sol|VASPsol)\s+(?:solvation\s+)?(?:module|extension|plugin)\b",
    re.I,
)
_CUSTOM_VARIANT_RE = re.compile(
    r"\b(?P<name>(?:a\s+)?(?:development|developer|locally\s+(?:modified|revised)|"
    r"modified|revised|in[- ]house)\s+(?:version|build|fork|copy)\s+of\s+"
    r"(?:the\s+)?[A-Z][A-Za-z0-9_.+/-]{1,32}(?:\s+\d+(?:\.\d+){0,3})?)\b",
    re.I,
)
_CUSTOM_IMPLEMENTATION_RE = re.compile(
    r"\b(?P<name>(?:our|a\s+new|an\s+in[- ]house|a\s+custom)\s+implementation\s+of\s+"
    r"[A-Za-z][A-Za-z0-9_.+/-]{1,32}(?:\s+[A-Za-z0-9_.+/-]{2,24}){0,3})\b",
    re.I,
)
_ACTUAL_SOFTWARE_USE_RE = re.compile(
    r"\b(?:use[ds]?|using|utilized|employed|executed|implemented|applied|performed|"
    r"carried\s+out|integrated|run|done|developed|present(?:ed)?|introduc(?:e|ed))\b",
    re.I,
)
_GENERIC_EXECUTABLE_NAMES = {
    "ab initio",
    "computer",
    "color",
    "colour",
    "dft",
    "open source",
    "online",
    "our",
    "same",
    "simulation",
    "software",
    "program",
    "the",
    "this",
}
_NONEXECUTABLE_LIBRARY_CONTEXT_RE = re.compile(
    r"\b(?:basis(?:\s+set)?|pseudopotentials?|force[ -]field|parameters?|dataset|database)\b",
    re.I,
)


def find_explicit_executable_cues(
    blocks: list[dict[str, Any]], known_mentions: list[dict[str, Any]] | None = None
) -> list[dict[str, Any]]:
    """Extract high-precision actual-use cues without treating them as toolbox support."""

    output = []
    for block in blocks:
        if _reference_section(block):
            continue
        text = str(block.get("text") or "")
        matches = [
            *list(_CUSTOM_VARIANT_RE.finditer(text)),
            *list(_CUSTOM_IMPLEMENTATION_RE.finditer(text)),
            *list(_KNOWN_EXTENSION_RE.finditer(text)),
            *list(_IMPLEMENTED_EXECUTABLE_RE.finditer(text)),
            *list(_FRAMEWORK_EXECUTABLE_RE.finditer(text)),
            *list(_EXECUTABLE_ENTITY_RE.finditer(text)),
        ]
        for match in matches:
            custom_match = match.re in {_CUSTOM_VARIANT_RE, _CUSTOM_IMPLEMENTATION_RE}
            explicit_entity_match = match.re is _EXECUTABLE_ENTITY_RE
            raw_name = match.group("name").strip(".,;:()[]")
            raw_name = _expand_contextual_executable_name(raw_name, text, match.start("name"))
            if re.fullmatch(r"VASP\s*sol", raw_name, re.I):
                raw_name = "VASPsol"
            trailing = text[match.end("name") : match.end("name") + 3]
            explicit_kind = (match.groupdict().get("kind") or "").casefold()
            ambiguous_lowercase_component = (
                explicit_entity_match
                and explicit_kind in {"extension", "plugin", "module"}
                and not any(character.isupper() or character.isdigit() for character in raw_name)
            )
            if (
                len(raw_name) < 3
                or raw_name.casefold() in _GENERIC_EXECUTABLE_NAMES
                or raw_name.endswith(("-", "/"))
                or (
                    not custom_match
                    and not explicit_entity_match
                    and not any(
                        character.isupper() or character.isdigit() for character in raw_name
                    )
                )
                or ambiguous_lowercase_component
                or (not custom_match and _looks_like_nonsoftware_name(raw_name))
                or re.match(r"[’']s\b", trailing, re.I)
            ):
                continue
            local_start = max(0, match.start() - 180)
            local_end = min(len(text), match.end() + 180)
            local_context = text[local_start:local_end]
            if not _ACTUAL_SOFTWARE_USE_RE.search(local_context):
                continue
            kind = (match.groupdict().get("kind") or "program").casefold()
            if custom_match:
                kind = "custom_code"
            elif match.re is _KNOWN_EXTENSION_RE:
                kind = "extension"
            if kind == "library" and _NONEXECUTABLE_LIBRARY_CONTEXT_RE.search(local_context):
                continue
            if _nonsoftware_data_resource(raw_name, kind, local_context):
                continue
            evidence_id = str(block["evidence_id"])
            if kind != "custom_code" and any(
                str(row.get("evidence_id")) == evidence_id
                and (
                    _normalize(raw_name) in _normalize(row.get("raw_name"))
                    or re.search(
                        rf"(?<![A-Za-z0-9]){re.escape(raw_name)}.{{0,80}}"
                        rf"\(\s*{re.escape(str(row.get('raw_name') or ''))}\s*\)",
                        str(row.get("context") or ""),
                        re.I,
                    )
                )
                for row in known_mentions or []
            ):
                continue
            context = _context_window(text, match.start(), match.end(), 600)
            entity_type = {
                "extension": "extension",
                "plugin": "extension",
                "module": "extension",
                "library": "library",
                "server": "service",
                "code": "custom_code",
                "custom_code": "custom_code",
            }.get(kind, "program")
            output.append(
                {
                    "raw_name": raw_name,
                    "entity_type": entity_type,
                    "evidence_id": evidence_id,
                    "context": context,
                    "deterministic_merge": bool(
                        custom_match
                        or match.re is _KNOWN_EXTENSION_RE
                        or any(character.isupper() or character.isdigit() for character in raw_name)
                    ),
                }
            )
    unique = {(_normalize(row["raw_name"]), row["evidence_id"]): row for row in output}
    return list(unique.values())[:24]


def _merge_explicit_executable_cues(mentions, cues):
    """Keep strong rule evidence even when an LLM omits an executable entity."""

    output = list(mentions)
    existing_names = {_normalize(row.get("raw_name")) for row in output}
    known = {
        (_normalize(row.get("raw_name")), evidence_id)
        for row in output
        for evidence_id in row.get("evidence_ids") or []
    }
    for cue in cues:
        entity_type = {
            "extension": "extension",
            "library": "library",
            "service": "service",
            "custom_code": "custom_code",
        }.get(str(cue.get("entity_type") or "program"), "program")
        if _nonsoftware_data_resource(
            str(cue.get("raw_name") or ""),
            entity_type,
            str(cue.get("context") or ""),
        ):
            continue
        raw_name, abbreviation = _expand_abbreviated_software_name(
            str(cue.get("raw_name") or ""), str(cue.get("context") or "")
        )
        normalized_name = _normalize(raw_name)
        if not cue.get("deterministic_merge", True) and normalized_name not in existing_names:
            continue
        key = (_normalize(cue.get("raw_name")), str(cue.get("evidence_id")))
        if (
            normalized_name in existing_names
            or key in known
            or (
                entity_type != "custom_code"
                and any(
                    str(cue.get("evidence_id")) in (row.get("evidence_ids") or [])
                    and _normalize(cue.get("raw_name")) in _normalize(row.get("raw_name"))
                    for row in output
                )
            )
        ):
            continue
        output.append(
            {
                "raw_name": raw_name,
                "normalized_hint": abbreviation,
                "entity_type": entity_type,
                "role": "unknown",
                "actual_use": True,
                "workflow_ids": [],
                "evidence_ids": [cue["evidence_id"]],
                "exact_quote": _truncate_utf8(str(cue.get("context") or ""), 600),
                "source": "deterministic_explicit_executable_cue",
            }
        )
        existing_names.add(normalized_name)
    return output


def _merge_catalog_actual_use_mentions(mentions, rule_mentions, workflows, evidence, aliases):
    """Recover catalog aliases that the model omitted when local use is explicit.

    The aliases come entirely from the frozen toolbox snapshot.  A match is promoted
    only when the same local context contains an actual-use verb; bibliography and
    background name matches therefore remain model-audit hints rather than required
    software.
    """

    output = list(mentions)
    warnings = []
    alias_keys = _software_alias_keys(aliases)
    known = {
        _software_identity(row.get("raw_name"), alias_keys) for row in output if row.get("raw_name")
    }
    for candidate in rule_mentions:
        raw_name = str(candidate.get("raw_name") or "").strip()
        evidence_id = str(candidate.get("evidence_id") or "")
        backend = str(candidate.get("backend_hint") or "")
        if not raw_name or evidence_id not in evidence:
            continue
        identity = _software_identity(raw_name, alias_keys)
        if identity in known:
            continue
        context = _catalog_actual_use_context(raw_name, str(evidence[evidence_id]))
        if not context or _ambiguous_software_term(backend, raw_name, context):
            continue
        workflow_ids = []
        for workflow in workflows:
            if not isinstance(workflow, dict):
                continue
            cited = set(str(item) for item in workflow.get("evidence_ids") or [])
            for step in workflow.get("steps") or []:
                if isinstance(step, dict):
                    cited.update(str(item) for item in step.get("evidence_ids") or [])
            workflow_id = str(workflow.get("workflow_id") or "")
            if workflow_id and evidence_id in cited:
                workflow_ids.append(workflow_id)
        output.append(
            {
                "raw_name": raw_name,
                "normalized_hint": backend or None,
                "entity_type": "program",
                "role": "unknown",
                "actual_use": True,
                "workflow_ids": workflow_ids,
                "evidence_ids": [evidence_id],
                "exact_quote": context,
                "source": "catalog_alias_actual_use",
            }
        )
        warnings.append(
            {
                "field": "software_mentions",
                "raw_name": raw_name,
                "reason": "catalog_actual_use_mention_recovered",
            }
        )
        known.add(identity)
    return output, warnings


def _catalog_actual_use_context(raw_name, text):
    pattern = re.compile(rf"(?<![A-Za-z0-9]){re.escape(str(raw_name))}(?![A-Za-z0-9])", re.I)
    for match in pattern.finditer(text):
        start = max(0, match.start() - 220)
        end = min(len(text), match.end() + 220)
        context = text[start:end]
        if _ACTUAL_SOFTWARE_USE_RE.search(context):
            return _truncate_utf8(context, 480)
    return ""


def _bind_workflow_steps_to_mentions(workflows, mentions, aliases):
    """Bind one unambiguous evidence-local software mention to an unnamed step."""

    warnings = []
    alias_keys = _software_alias_keys(aliases)
    required_mentions = [
        row for row in mentions if row.get("actual_use") and row.get("role") in REQUIRED_ROLES
    ]
    for workflow in workflows:
        if not isinstance(workflow, dict):
            continue
        workflow_id = str(workflow.get("workflow_id") or "")
        workflow_evidence = set(str(item) for item in workflow.get("evidence_ids") or [])
        for step in workflow.get("steps") or []:
            if (
                not isinstance(step, dict)
                or not bool(step.get("essential", True))
                or step.get("software")
                or step.get("execution_layer") == "task_specific_python"
            ):
                continue
            step_evidence = set(str(item) for item in step.get("evidence_ids") or [])
            cited = step_evidence or workflow_evidence
            candidates = []
            for mention in required_mentions:
                mention_evidence = set(str(item) for item in mention.get("evidence_ids") or [])
                mention_workflows = set(str(item) for item in mention.get("workflow_ids") or [])
                if (
                    cited.intersection(mention_evidence)
                    and (
                        not mention_workflows or not workflow_id or workflow_id in mention_workflows
                    )
                    and _step_action_matches_context(
                        str(step.get("action") or ""), str(mention.get("exact_quote") or "")
                    )
                ):
                    candidates.append(mention)
            identities = {_software_identity(row.get("raw_name"), alias_keys) for row in candidates}
            if len(identities) != 1:
                continue
            selected = candidates[0]
            step["software"] = selected.get("raw_name")
            step["normalized_backend"] = None
            step["execution_layer"] = "named_software"
            warnings.append(
                {
                    "field": "workflows.steps.software",
                    "step_id": step.get("step_id"),
                    "reason": "evidence_local_software_bound_to_step",
                    "raw_name": selected.get("raw_name"),
                }
            )
    return warnings


_GENERIC_STEP_ACTION_WORDS = {
    "analyze",
    "analysis",
    "calculate",
    "calculation",
    "compute",
    "computation",
    "conduct",
    "method",
    "model",
    "perform",
    "result",
    "run",
    "simulate",
    "simulation",
    "study",
    "using",
    "workflow",
}


def _step_action_matches_context(action, context, *, allow_unspecified=False):
    action_terms = {
        term
        for term in re.findall(r"[a-z0-9]+", action.casefold())
        if len(term) >= 4 and term not in _GENERIC_STEP_ACTION_WORDS
    }
    if not action_terms:
        return bool(allow_unspecified)
    context_terms = set(re.findall(r"[a-z0-9]+", context.casefold()))
    if action_terms.issubset({"energy", "energies"}) and re.search(
        r"\b(?:dft|density functional|electronic[ -]structure|ab initio)\b", context, re.I
    ):
        return True
    required_matches = min(2, len(action_terms))
    return len(action_terms.intersection(context_terms)) >= required_matches


def _merge_workflow_software_mentions(mentions, workflows, evidence, aliases):
    """Promote software named by workflow steps into the coverage inventory."""

    output = list(mentions)
    warnings = []
    alias_keys = _software_alias_keys(aliases)
    known = {
        _software_identity(row.get("raw_name"), alias_keys) for row in output if row.get("raw_name")
    }
    for workflow in workflows:
        if not isinstance(workflow, dict):
            continue
        workflow_id = str(workflow.get("workflow_id") or "")
        for step in workflow.get("steps") or []:
            if not isinstance(step, dict) or not isinstance(step.get("software"), str):
                continue
            raw_name = " ".join(step["software"].split()).strip(".,;:()[]")
            if not raw_name or _looks_like_nonsoftware_name(raw_name):
                continue
            identity = _software_identity(raw_name, alias_keys)
            if identity in known:
                continue
            evidence_ids = [
                str(item) for item in step.get("evidence_ids") or [] if str(item) in evidence
            ]
            exact_quote = _recover_software_quote(raw_name, evidence_ids, evidence, actual_use=True)
            if not exact_quote and evidence_ids:
                exact_quote = _truncate_utf8(str(evidence[evidence_ids[0]]), 480)
            output.append(
                {
                    "raw_name": raw_name,
                    "normalized_hint": None,
                    "entity_type": "program",
                    "role": "core_compute"
                    if bool(step.get("essential", True))
                    else "optional_auxiliary",
                    "actual_use": True,
                    "workflow_ids": [workflow_id] if workflow_id else [],
                    "evidence_ids": evidence_ids,
                    "exact_quote": exact_quote,
                    "source": "workflow_step_contract",
                }
            )
            warnings.append(
                {
                    "field": "software_mentions",
                    "raw_name": raw_name,
                    "reason": "workflow_software_promoted_to_inventory",
                }
            )
            known.add(identity)
    return output, warnings


def _software_alias_keys(aliases):
    # Canonical catalog identifiers always win over aliases contributed by a
    # different backend.  This prevents an executable name such as ``orca``
    # from being reassigned to the PyFrag wrapper that invokes it.
    lookup = {_normalize(backend): backend for backend in aliases}
    for backend, values in aliases.items():
        for value in values:
            lookup.setdefault(_normalize(value), backend)
    return lookup


def _software_identity(raw_name, alias_keys):
    normalized = _normalize(raw_name)
    return (
        alias_keys.get(normalized)
        or alias_keys.get(_normalize(_without_version_suffix(str(raw_name))))
        or normalized
    )


def _expand_contextual_executable_name(raw_name: str, text: str, start: int) -> str:
    """Recover a small set of multiword product names truncated by the cue regex."""

    if raw_name.casefold() == "studio":
        prefix = text[max(0, start - 24) : start]
        if re.search(r"\bMaterials\s+$", prefix, re.I):
            return "Materials Studio"
    return raw_name


def _context_window(text: str, start: int, end: int, limit: int) -> str:
    if len(text.encode("utf-8")) <= limit:
        return text
    margin = max(64, limit // 2)
    left = max(0, start - margin)
    right = min(len(text), end + margin)
    return _truncate_utf8(text[left:right], limit)


def resolve_software(mentions, aliases, profile):
    lookup = _software_alias_keys(aliases)
    backends = profile.get("backends") or {}
    native_software = profile.get("native_software") or {}
    python_packages = profile.get("python_packages") or {}
    output = []
    for mention in mentions:
        raw = str(mention.get("raw_name") or mention.get("normalized_hint") or "")
        # Model-proposed hints are audit data; only the frozen aliases establish presence.
        backend = lookup.get(_normalize(raw))
        if backend is None:
            backend = lookup.get(_normalize(_without_version_suffix(raw)))
        if backend is None:
            backend = _compound_extension_backend(raw, lookup)
        if backend is None:
            backend = _decorated_software_backend(raw, lookup)
        backend_entry = backends.get(backend) if backend else None
        native_entry = native_software.get(backend) if backend else None
        package_entry = python_packages.get(backend) if backend else None
        entry = backend_entry or native_entry or package_entry
        catalog_kind = (
            "native_backend"
            if backend_entry
            else (
                "native_software"
                if native_entry
                else ("python_package" if package_entry else "unknown")
            )
        )
        output.append(
            {
                "raw_name": raw,
                "role": mention.get("role"),
                "actual_use": bool(mention.get("actual_use")),
                "normalized_backend": backend if backend_entry else None,
                "normalized_identifier": backend if entry else None,
                "catalog_kind": catalog_kind,
                "catalog_present": entry is not None,
                "native_software_available": entry is not None,
                "coverage_basis": "native_software_catalog_presence",
                "availability": entry.get("availability") if entry else "unknown",
                "validation_level": entry.get("validation_level") if entry else "unknown",
                "local_installation_status": entry.get("local_installation_status")
                if entry
                else "unknown",
                "actions": entry.get("actions", []) if entry else [],
                "method_families": entry.get("method_families", []) if entry else [],
                "constraint_snapshot": _capability_excerpt(entry or {}),
                "evidence_ids": mention.get("evidence_ids") or [],
                "workflow_ids": mention.get("workflow_ids") or [],
            }
        )
    return output


def _compound_extension_backend(raw_name: str, lookup: dict[str, str]) -> str | None:
    """Resolve the rightmost known component of a compound plugin/module name."""

    if not re.search(r"\b(?:plugin|module|extension|interface)\b", raw_name, re.I):
        return None
    normalized = _normalize(raw_name)
    candidates: list[tuple[int, int, str]] = []
    for alias, backend in lookup.items():
        if len(alias) < 3:
            continue
        start = normalized.rfind(alias)
        if start >= 0:
            candidates.append((start, len(alias), backend))
    return max(candidates, default=(-1, -1, None), key=lambda item: (item[0], item[1]))[2]


def _decorated_software_backend(raw_name: str, lookup: dict[str, str]) -> str | None:
    """Resolve a catalogued engine inside a slash/hyphen decorated method name."""

    if re.search(r"\b(?:plugin|module|extension|package|interface)\b", raw_name, re.I):
        return None
    candidates: list[str] = []
    for part in re.split(r"\s*/\s*", raw_name):
        part = _without_version_suffix(part.strip())
        backend = lookup.get(_normalize(part))
        if backend and backend not in candidates:
            candidates.append(backend)
    return candidates[0] if len(candidates) == 1 else None


def _without_version_suffix(raw_name: str) -> str:
    return re.sub(
        r"(?:[\s_-]+(?:version\s*)?v?\d+(?:\.\d+){0,3})$",
        "",
        str(raw_name).strip(),
        flags=re.I,
    ).strip()


def coverage_gate(review, mappings, profile, config):
    """Check required software presence, not predefined Action coverage.

    A catalogued backend is usable through the toolbox's native-software layer even
    when the predefined Action layer does not expose a paper's exact operation or
    parameter. Action and method constraints therefore cannot reject Stage03.
    """
    del profile, config
    required = [row for row in mappings if row["actual_use"] and row.get("role") in REQUIRED_ROLES]
    workflows = review.get("workflows") or []
    covered_workflows: list[str] = []
    for workflow in workflows:
        if not isinstance(workflow, dict):
            continue
        workflow_id = str(workflow.get("workflow_id") or "")
        essential_steps = [
            step
            for step in workflow.get("steps") or []
            if isinstance(step, dict) and bool(step.get("essential", True))
        ]
        if not essential_steps:
            continue
        workflow_mappings = [
            row
            for row in required
            if workflow_id and workflow_id in {str(item) for item in row.get("workflow_ids") or []}
        ]
        for step in essential_steps:
            raw_name = str(step.get("software") or "")
            if not raw_name:
                continue
            normalized = _normalize(_without_version_suffix(raw_name))
            workflow_mappings.extend(
                row
                for row in required
                if _normalize(_without_version_suffix(str(row.get("raw_name") or ""))) == normalized
            )
        workflow_mappings = list({id(row): row for row in workflow_mappings}.values())
        unnamed_required = any(
            not step.get("software") and step.get("execution_layer") != "task_specific_python"
            for step in essential_steps
        )
        if (
            workflow_mappings
            and not unnamed_required
            and all(row.get("catalog_present") for row in workflow_mappings)
        ):
            covered_workflows.append(workflow_id or f"workflow-{len(covered_workflows) + 1}")

    uncovered_required = [row for row in required if not row.get("catalog_present")]
    if covered_workflows:
        return "mixed_workflow_candidate" if uncovered_required else "covered"
    if uncovered_required:
        return "core_software_uncovered"
    return "software_inventory_unconfirmed"


def resource_gate(facts: list[dict[str, Any]], budget: dict[str, Any]) -> dict[str, Any]:
    comparable = [
        row
        for row in facts
        if row.get("actual_computation") and row.get("scope") in {"single_job", "aggregate_study"}
    ]
    exceeded = []
    ambiguous = []
    for fact in comparable:
        key = str(fact.get("resource_type") or "")
        if key not in budget:
            ambiguous.append(fact)
            continue
        state = _fact_budget_state(fact, float(budget[key]))
        if fact.get("scope") == "aggregate_study" and state == "exceeded":
            state = "ambiguous"
        if state == "exceeded":
            exceeded.append(fact)
        elif state == "ambiguous":
            ambiguous.append(fact)
    if exceeded:
        decision = "cost_exceeds_budget"
    elif not comparable or ambiguous:
        decision = "cost_unconfirmed"
    else:
        decision = "within_preliminary_budget"
    return {
        "decision": decision,
        "facts": facts,
        "comparable_facts": comparable,
        "exceeded_facts": exceeded,
        "ambiguous_facts": ambiguous,
        "budget": budget,
    }


def _fact_budget_state(fact: dict[str, Any], threshold: float) -> str:
    relation = str(fact.get("relation") or "")
    lower = _float_or_none(fact.get("value_min"))
    upper = _float_or_none(fact.get("value_max"))
    if relation in {"exact", "approximately"}:
        value = lower if lower is not None else upper
        return "ambiguous" if value is None else ("exceeded" if value > threshold else "within")
    if relation == "range":
        if lower is None or upper is None:
            return "ambiguous"
        if lower > threshold:
            return "exceeded"
        return "within" if upper <= threshold else "ambiguous"
    if relation == "less_than":
        return "within" if upper is not None and upper <= threshold else "ambiguous"
    if relation == "greater_than":
        if lower is None:
            return "ambiguous"
        return "exceeded" if lower >= threshold else "ambiguous"
    return "ambiguous"


def _float_or_none(value):
    try:
        return float(value) if value is not None else None
    except (TypeError, ValueError):
        return None


def _combine_decision(coverage, resource, complete):
    if coverage == "core_software_uncovered":
        return coverage
    if resource.get("decision") == "cost_exceeds_budget":
        return "cost_exceeds_budget"
    if coverage == "covered":
        return "software_covered" if complete else "software_coverage_probable"
    if coverage == "mixed_workflow_candidate":
        return "mixed_workflow_candidate"
    return "software_inventory_unconfirmed"


def _sanitize_review(response, evidence):
    if not isinstance(response.get("workflows"), list) or not isinstance(
        response.get("software_mentions"), list
    ):
        raise ValueError("Stage03 response is missing workflows/software_mentions arrays")
    warnings: list[dict[str, Any]] = []
    sanitized = dict(response)
    reported_software_names = [
        str(mention.get("raw_name") or "")
        for mention in response.get("software_mentions") or []
        if isinstance(mention, dict) and mention.get("raw_name")
    ]

    workflows = []
    for index, workflow in enumerate(response.get("workflows") or []):
        if (
            not isinstance(workflow, dict)
            or not workflow.get("workflow_id")
            or not isinstance(workflow.get("steps"), list)
        ):
            warnings.append({"field": "workflows", "index": index, "reason": "invalid_shape"})
            continue
        steps = []
        for step_index, step in enumerate(workflow.get("steps") or []):
            if not isinstance(step, dict):
                warnings.append(
                    {
                        "field": "workflows.steps",
                        "index": f"{index}.{step_index}",
                        "reason": "invalid_shape",
                    }
                )
                continue
            evidence_ids = _known_evidence_ids(step.get("evidence_ids"), evidence)
            if not evidence_ids:
                warnings.append(
                    {
                        "field": "workflows.steps",
                        "index": f"{index}.{step_index}",
                        "reason": "missing_valid_evidence",
                    }
                )
                continue
            reported_settings = step.get("reported_settings")
            if not isinstance(reported_settings, list):
                legacy_constraints = step.get("constraints")
                reported_settings = (
                    []
                    if legacy_constraints in (None, "", [], {})
                    else [str(legacy_constraints)[:240]]
                )
            reported_settings = [str(item)[:240] for item in reported_settings[:12]]
            required_action = step.get("required_action")
            if required_action not in (None, "") and not isinstance(required_action, str):
                required_action = None
            software = step.get("software")
            evidence_text = " ".join(str(evidence[item]) for item in evidence_ids)
            bundled_host = _bundled_host_module(
                str(software or ""), evidence_text, reported_software_names
            )
            if bundled_host:
                warnings.append(
                    {
                        "field": "workflows.steps.software",
                        "index": f"{index}.{step_index}",
                        "reason": "bundled_module_resolved_to_named_host",
                        "raw_name": software,
                        "host_software": bundled_host,
                    }
                )
                software = bundled_host
            elif software and (
                _scientific_method_usage(str(software), evidence_text)
                or _generic_computation_label(str(software), evidence_text)
            ):
                warnings.append(
                    {
                        "field": "workflows.steps.software",
                        "index": f"{index}.{step_index}",
                        "reason": "method_or_process_removed_from_software_step",
                        "raw_name": software,
                    }
                )
                software = None
                sanitized["inventory_complete"] = False
            execution_layer = step.get("execution_layer")
            if isinstance(software, str) and software.strip():
                execution_layer = "named_software"
            elif execution_layer != "task_specific_python":
                execution_layer = "unknown"
            elif _CORE_RUNTIME_ACTION_RE.search(str(step.get("action") or "")):
                execution_layer = "unknown"
                sanitized["inventory_complete"] = False
                warnings.append(
                    {
                        "field": "workflows.steps.execution_layer",
                        "index": f"{index}.{step_index}",
                        "reason": "core_runtime_cannot_use_unnamed_task_specific_python",
                    }
                )
            steps.append(
                {
                    **step,
                    "essential": bool(step.get("essential", True)),
                    "software": software,
                    "execution_layer": execution_layer,
                    "required_action": required_action or None,
                    "reported_settings": reported_settings,
                    "evidence_ids": evidence_ids,
                }
            )
        if not steps:
            warnings.append({"field": "workflows", "index": index, "reason": "no_valid_steps"})
            continue
        workflows.append(
            {
                **workflow,
                "steps": steps,
                "evidence_ids": _known_evidence_ids(workflow.get("evidence_ids"), evidence),
            }
        )
    sanitized["workflows"] = workflows

    mentions = []
    for index, mention in enumerate(response.get("software_mentions") or []):
        if not isinstance(mention, dict) or mention.get("role") not in VALID_ROLES:
            warnings.append(
                {"field": "software_mentions", "index": index, "reason": "invalid_shape_or_role"}
            )
            continue
        raw_name = str(mention.get("raw_name") or mention.get("normalized_hint") or "")
        evidence_ids = _known_evidence_ids(mention.get("evidence_ids"), evidence)
        quote = str(mention.get("exact_quote") or "")
        if not evidence_ids:
            warnings.append(
                {
                    "field": "software_mentions",
                    "index": index,
                    "reason": "unsupported_quote_or_evidence",
                }
            )
            continue
        if not quote or not _quote_matches(quote, evidence_ids, evidence):
            recovered_quote = _recover_software_quote(
                raw_name,
                evidence_ids,
                evidence,
                actual_use=bool(mention.get("actual_use")),
            )
            if not recovered_quote:
                warnings.append(
                    {
                        "field": "software_mentions",
                        "index": index,
                        "reason": "unsupported_quote_or_evidence",
                    }
                )
                continue
            quote = recovered_quote
            warnings.append(
                {
                    "field": "software_mentions",
                    "index": index,
                    "reason": "software_quote_recovered_from_evidence",
                }
            )
        if not _software_name_in_quote(raw_name, quote):
            warnings.append(
                {
                    "field": "software_mentions",
                    "index": index,
                    "reason": "software_name_not_in_exact_quote",
                }
            )
            continue
        if _possessive_author_fragment(raw_name, quote):
            warnings.append(
                {
                    "field": "software_mentions",
                    "index": index,
                    "reason": "possessive_author_fragment_not_software",
                }
            )
            continue
        entity_type = str(mention.get("entity_type") or "program").casefold()
        bundled_host = _bundled_host_module(raw_name, quote, reported_software_names)
        if entity_type == "extension" and bundled_host:
            warnings.append(
                {
                    "field": "software_mentions",
                    "index": index,
                    "reason": "bundled_module_not_separate_software",
                    "host_software": bundled_host,
                }
            )
            continue
        if _scientific_method_usage(raw_name, quote) or _generic_computation_label(
            raw_name, quote
        ):
            warnings.append(
                {
                    "field": "software_mentions",
                    "index": index,
                    "reason": "method_or_process_not_software",
                }
            )
            continue
        if entity_type not in SOFTWARE_ENTITY_TYPES:
            warnings.append(
                {
                    "field": "software_mentions",
                    "index": index,
                    "reason": "nonsoftware_entity_type",
                }
            )
            continue
        raw_name, abbreviation = _expand_abbreviated_software_name(raw_name, quote)
        if _nonsoftware_data_resource(raw_name, entity_type, quote):
            warnings.append(
                {
                    "field": "software_mentions",
                    "index": index,
                    "reason": "nonsoftware_data_resource",
                }
            )
            continue
        if entity_type == "library" and _NONEXECUTABLE_LIBRARY_CONTEXT_RE.search(quote):
            warnings.append(
                {
                    "field": "software_mentions",
                    "index": index,
                    "reason": "nonexecutable_data_or_parameter_library",
                }
            )
            continue
        if _looks_like_nonsoftware_name(raw_name):
            warnings.append(
                {
                    "field": "software_mentions",
                    "index": index,
                    "reason": "nonsoftware_entity_name",
                }
            )
            continue
        if _ambiguous_software_term("", raw_name, quote):
            warnings.append(
                {
                    "field": "software_mentions",
                    "index": index,
                    "reason": "ambiguous_generic_software_term",
                }
            )
            continue
        mentions.append(
            {
                **mention,
                "raw_name": raw_name,
                "normalized_hint": abbreviation or mention.get("normalized_hint"),
                "entity_type": entity_type,
                "evidence_ids": evidence_ids,
                "exact_quote": quote,
            }
        )
    sanitized["software_mentions"] = mentions

    actual_mentions = [row for row in mentions if row.get("actual_use")]
    for workflow_index, workflow in enumerate(sanitized["workflows"]):
        for step_index, step in enumerate(workflow.get("steps") or []):
            software = str(step.get("software") or "")
            if not software:
                continue
            normalized = _normalize(software)
            backend = _normalize(step.get("normalized_backend") or "")
            evidence_text = " ".join(
                str(evidence[evidence_id]) for evidence_id in step.get("evidence_ids") or []
            )
            step_evidence_ids = set(str(item) for item in step.get("evidence_ids") or [])
            mention_supported = any(
                (
                    normalized
                    in {
                        _normalize(mention.get("raw_name")),
                        _normalize(mention.get("normalized_hint")),
                    }
                    or (backend and backend == _normalize(mention.get("normalized_hint")))
                )
                and bool(
                    step_evidence_ids.intersection(
                        str(item) for item in mention.get("evidence_ids") or []
                    )
                )
                for mention in actual_mentions
            )
            evidence_supported = bool(
                normalized
                and re.search(
                    rf"(?<![A-Za-z0-9]){re.escape(software)}(?![A-Za-z0-9])",
                    evidence_text,
                    re.I,
                )
            )
            ambiguous_name = _ambiguous_software_term(backend, software, evidence_text)
            if (
                _looks_like_nonsoftware_name(software)
                or (ambiguous_name and not mention_supported)
                or not (mention_supported or evidence_supported)
            ):
                step["software"] = None
                step["execution_layer"] = "unknown"
                step.pop("normalized_backend", None)
                if bool(step.get("essential", True)):
                    sanitized["inventory_complete"] = False
                warnings.append(
                    {
                        "field": "workflows.steps.software",
                        "index": f"{workflow_index}.{step_index}",
                        "reason": "nonsoftware_or_unsupported_executable_name",
                    }
                )

    for field in ("resource_facts", "complexity_facts"):
        facts = []
        for index, fact in enumerate(response.get(field) or []):
            if not isinstance(fact, dict):
                warnings.append({"field": field, "index": index, "reason": "invalid_shape"})
                continue
            evidence_ids = _known_evidence_ids(fact.get("evidence_ids"), evidence)
            quote = str(fact.get("exact_quote") or "")
            if not evidence_ids or (quote and not _quote_matches(quote, evidence_ids, evidence)):
                warnings.append(
                    {"field": field, "index": index, "reason": "unsupported_quote_or_evidence"}
                )
                continue
            if field == "resource_facts" and not _resource_fact_supported(fact, quote):
                warnings.append(
                    {
                        "field": field,
                        "index": index,
                        "reason": "resource_value_not_supported_by_quote",
                    }
                )
                continue
            facts.append({**fact, "evidence_ids": evidence_ids})
        sanitized[field] = facts
    sanitized["evidence_ids"] = _known_evidence_ids(response.get("evidence_ids"), evidence)
    return sanitized, warnings


_METHOD_USAGE_SUFFIX_RE = re.compile(
    r"(?:method|algorithm|approach|scheme|functional|basis(?:\s+set)?|"
    r"pseudopotential|force[ -]field|integrator)\b",
    re.I,
)

_GENERIC_COMPUTATION_LABEL_RE = re.compile(
    r"^(?:[a-z0-9+./()_-]+\s+){0,5}"
    r"(?:simulations?|calculations?|computations?|analyses|analysis|"
    r"model(?:ing|ling)?|optimizations?|sampling)$",
    re.I,
)
_EXECUTABLE_TYPE_CUE_RE = re.compile(
    r"\b(?:software|program|package|code|library|plugin|extension|module|suite)\b",
    re.I,
)


def _scientific_method_usage(raw_name: str, quote: str) -> bool:
    """Identify a candidate explicitly described as a method rather than executable."""

    name = str(raw_name).strip()
    if len(name) < 2:
        return False
    match = re.search(
        rf"(?<![A-Za-z0-9]){re.escape(name)}(?![A-Za-z0-9]).{{0,18}}",
        quote,
        re.I,
    )
    if not match:
        return False
    suffix = quote[match.start() : min(len(quote), match.end() + 24)]
    if not _METHOD_USAGE_SUFFIX_RE.search(suffix):
        return False
    return not _EXECUTABLE_TYPE_CUE_RE.search(suffix)


def _generic_computation_label(raw_name: str, quote: str) -> bool:
    """Reject a computation description presented as though it were a product name."""

    name = " ".join(str(raw_name).split())
    if not _GENERIC_COMPUTATION_LABEL_RE.fullmatch(name):
        return False
    match = re.search(
        rf"(?<![A-Za-z0-9]){re.escape(name)}(?![A-Za-z0-9])",
        str(quote),
        re.I,
    )
    if not match:
        return False
    context = _context_window(str(quote), match.start(), match.end(), 120)
    return not _EXECUTABLE_TYPE_CUE_RE.search(context)


def _bundled_host_module(raw_name: str, quote: str, software_names: list[str]) -> str | None:
    """Resolve an internal `module of Host` label to its separately named host program."""

    name = str(raw_name).strip()
    if not name or not re.search(
        rf"(?<![A-Za-z0-9]){re.escape(name)}(?![A-Za-z0-9])\s+module\s+of\s+",
        quote,
        re.I,
    ):
        return None
    for candidate in software_names:
        host = str(candidate).strip()
        if not host or _normalize(host) == _normalize(name):
            continue
        if re.search(
            rf"\bmodule\s+of\s+(?:the\s+)?{re.escape(host)}(?![A-Za-z0-9])",
            quote,
            re.I,
        ):
            return host
    return None


def _known_evidence_ids(value, evidence):
    if not isinstance(value, list):
        return []
    return [str(item) for item in value if str(item) in evidence]


def _quote_matches(quote, evidence_ids, evidence):
    return any(quote in str(evidence[evidence_id]) for evidence_id in evidence_ids)


def _recover_software_quote(raw_name, evidence_ids, evidence, *, actual_use):
    name = str(raw_name).strip()
    if len(name) < 2:
        return ""
    pattern = re.compile(rf"(?<![A-Za-z0-9]){re.escape(name)}(?![A-Za-z0-9])", re.I)
    for evidence_id in evidence_ids:
        text = str(evidence[evidence_id])
        match = pattern.search(text)
        if not match:
            continue
        context = _context_window(text, match.start(), match.end(), 480)
        if actual_use and not _ACTUAL_SOFTWARE_USE_RE.search(context):
            continue
        return context
    return ""


def _ambiguous_software_term(backend, raw_name, context):
    if _normalize(backend or raw_name) not in {"gaussian", "gaussian09", "gaussian16"}:
        return False
    return not _explicit_gaussian_software_use(context)


_NONSOFTWARE_NAME_RE = re.compile(
    r"^(?:figure\s*\d+|gpu|cpu|applied voltage|redox couple potential|fermi function|"
    r"fourier transform|fourier interpolation|gaussian potentials?|hse\d*|paw|revpbe|"
    r"b3lyp\*?|pbe|pbeh-?3c|pbe0|b2plyp|dsd(?:-pbep86)?|dlpno-ccsd\(t\)|"
    r"def2[-a-z0-9()]+|daug[-a-z0-9()]+\s+basis|pb\d[-a-z0-9()]+|"
    r"sg-?\d+|tip3p|amoeba|amberff\w+|charmm\d+[a-z]*|soap descriptor|autoneb|"
    r"nudged elastic band|"
    r"wannier interpolation|monkhorst-pack|car-parrinello|climbing image scheme|spring constant|"
    r"chebyshev polynomials|sine functions?|gaussian kernel|polynomial kernel|relu|adamax|"
    r"huber loss|custom mean-squared error loss|broken bonds score|state score|"
    r"\d+\s+(?:cpu\s+)?cores?|hpe cray(?:\s+ex)?|c\+\+|this|ad-compatible|modeling|vienna|"
    r"mfep\d*|1d-mtd|"
    r"mmpbsa/mmgbsa|ai-?gcmc|quicksteps?|fist|graph clustering|"
    r"rasscf|cas(?:scf)?|qsar(?:\s+model)?|gnn|pip-?nn|deep ?pot-?se|rpmd|cp-?hs-?dm|"
    r"coordinationnumber|color|colour|online|"
    r"dbscan|mcts|adam(?:\s+optimizer)?|"
    r"logistic\s+regress(?:ion|ors?)|random\s+forests?|borda(?:'s)?\s+method|"
    r"stratifiedkfold(?:\(\))?|rfr|lrrf|rpc|ibm|ibpl|python|script)$",
    re.I,
)


def _looks_like_nonsoftware_name(raw_name: str) -> bool:
    name = " ".join(str(raw_name).split())
    if _NONSOFTWARE_NAME_RE.fullmatch(name):
        return True
    return bool(
        re.search(
            r"\b(?:functional|basis set|pseudopotential|force field|thermostat|integrator|"
            r"descriptor|smearing|physical parameter|loss function|neural network architecture|"
            r"hardware|cpu cores?|(?:statistical|regression|classification|qsar) model|"
            r"(?:database|dataset|repository|data archive))\b",
            name,
            re.I,
        )
    )


_KNOWN_DATA_RESOURCE_RE = re.compile(
    r"^(?:chembl|zinc(?:20)?|cccdb(?:\s+database)?|protein\s+data\s+bank|pdb|"
    r"mavedb|uniprot|skempi(?:\s+v?\d+(?:\.\d+)*)?)$",
    re.I,
)
_ACTIVE_SERVICE_RE = re.compile(
    r"\b(?:api|web\s*service|endpoint|server|quer(?:y|ied)|programmatic(?:ally)?\s+access)\b",
    re.I,
)


def _nonsoftware_data_resource(raw_name: str, entity_type: str, context: str) -> bool:
    name = " ".join(str(raw_name).split())
    text = str(context)
    data_context = bool(
        _KNOWN_DATA_RESOURCE_RE.fullmatch(name)
        or re.search(r"\b(?:database|dataset|repository|data archive)\b", text, re.I)
    )
    if not data_context:
        return False
    return not (entity_type == "service" and _ACTIVE_SERVICE_RE.search(text))


def _expand_abbreviated_software_name(raw_name: str, quote: str) -> tuple[str, str | None]:
    explicit = re.fullmatch(r"(.+?)\s*\(([A-Z][A-Z0-9+.-]{1,12})\)", str(raw_name).strip())
    if explicit:
        return explicit.group(1).strip(), explicit.group(2).casefold()
    match = re.search(
        rf"\b({re.escape(raw_name)}(?:\s+[A-Z][A-Za-z0-9_.+-]+){{1,5}})\s+"
        r"\(([A-Z][A-Z0-9+.-]{1,12})\)\s+"
        r"(?:library|package|software|framework|environment)\b",
        quote,
    )
    if not match:
        return raw_name, None
    return match.group(1), match.group(2).casefold()


def _software_name_in_quote(raw_name, quote):
    name = str(raw_name).strip()
    if len(name) < 2:
        return False
    return bool(
        re.search(
            rf"(?<![A-Za-z0-9]){re.escape(name)}(?![A-Za-z0-9])",
            str(quote),
            re.I,
        )
    )


def _possessive_author_fragment(raw_name, quote):
    name = str(raw_name).strip()
    if not name:
        return False
    return bool(
        re.search(
            rf"(?<![A-Za-z0-9]){re.escape(name)}(?:'|\u2019)s\s+"
            r"[A-Za-z][A-Za-z0-9_.+/-]{1,48}\s+"
            r"(?:program|package|software|code|suite)\b",
            str(quote),
            re.I,
        )
    )


def _explicit_gaussian_software_use(context):
    text = str(context)
    return bool(
        re.search(r"\bGaussian\s*(?:0[39]|1[69])\b", text)
        or re.search(r"\bGaussian\s+(?:program|software|package|suite)\b", text, re.I)
        or re.search(r"\b(?:using|with|via|in)\s+Gaussian\b", text, re.I)
        or re.search(r"\bGaussian\s+(?:was|is)\s+used\b", text, re.I)
        or re.search(r"\bGaussian\s+calculations?\b", text, re.I)
    )


def _resource_fact_supported(fact, quote):
    if not quote:
        return False
    resource_type = str(fact.get("resource_type") or "")
    keywords = {
        "cpu_cores": ("cpu", "core", "processor"),
        "gpus": ("gpu", "graphics processing"),
        "memory_gb": ("memory", "ram", " gb", "gib"),
        "runtime_hours": ("runtime", "wall time", "hour", " hr", "minute", "day"),
        "core_hours": ("core-hour", "core hour", "cpu-hour", "cpu hour"),
        "gpu_hours": ("gpu-hour", "gpu hour"),
        "job_count": ("job", "runs", "calculations", "simulations"),
    }
    lowered = quote.casefold()
    if resource_type not in keywords or not any(
        word in lowered for word in keywords[resource_type]
    ):
        return False
    values = [fact.get("value_min"), fact.get("value_max")]
    numeric = [value for value in values if isinstance(value, (int, float))]
    if not numeric:
        return False
    return any(_numeric_value_in_quote(value, quote) for value in numeric)


def _numeric_value_in_quote(value, quote):
    number = float(value)
    forms = {str(value), f"{number:g}"}
    return any(re.search(rf"(?<![0-9.]){re.escape(form)}(?![0-9.])", quote) for form in forms)


_SOFTWARE_CUE_RE = re.compile(
    r"\b(?:software|program|package|suite|code|codebase|library|framework|module|script|"
    r"plugin|extension|implemented|in[- ]house|custom|calculations?\s+(?:were|was)\s+"
    r"(?:performed|carried out)\s+(?:using|with)|simulations?\s+(?:were|was)\s+"
    r"(?:performed|carried out)\s+(?:using|with))\b",
    re.I,
)


def _target_blocks(blocks, record, mentions, limit):
    by_id = {str(block["evidence_id"]): block for block in blocks}
    mention_contexts: dict[str, list[str]] = {}
    for mention in mentions:
        mention_contexts.setdefault(str(mention["evidence_id"]), []).append(
            str(mention.get("context") or "")
        )
    rule_ids = list(mention_contexts)
    stage02_ids = [str(value) for value in ((record.get("review") or {}).get("evidence_ids") or [])]
    cue_ids = [
        str(block["evidence_id"])
        for block in blocks
        if _SOFTWARE_CUE_RE.search(str(block.get("text") or ""))
    ]
    method_ids = [str(block["evidence_id"]) for block in blocks if _method_section(block)]
    method_ids.extend(_method_neighborhood_ids(blocks))
    ordered_ids = list(dict.fromkeys([*rule_ids, *cue_ids, *stage02_ids, *method_ids]))
    if not ordered_ids:
        ordered_ids = list(by_id)

    # GROBID does not always retain section paths. Keep the first relevant block
    # from every available document before filling the remaining evidence budget.
    first_by_document, remaining, seen_documents = [], [], set()
    for evidence_id in ordered_ids:
        block = by_id.get(evidence_id)
        document_id = str((block or {}).get("document_id") or "")
        if document_id and document_id not in seen_documents:
            first_by_document.append(evidence_id)
            seen_documents.add(document_id)
        else:
            remaining.append(evidence_id)
    ordered_ids = [*first_by_document, *remaining]

    output, size = [], 0
    per_block_limit = min(1600, max(600, limit // 6))
    for evidence_id in ordered_ids:
        block = by_id.get(evidence_id)
        if block is None:
            continue
        text = str(block.get("text") or "")
        contexts = [value for value in mention_contexts.get(evidence_id, []) if value]
        if contexts:
            text = " ... ".join(dict.fromkeys(contexts))
        else:
            match = _SOFTWARE_CUE_RE.search(text)
            if match:
                text = _context_window(text, match.start(), match.end(), per_block_limit)
        compact = {
            key: block.get(key)
            for key in (
                "evidence_id",
                "document_id",
                "document_role",
                "page",
                "section_path",
            )
        }
        compact["text"] = _truncate_utf8(text, per_block_limit)
        block_size = len(
            json.dumps(compact, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        )
        if size + block_size > limit:
            continue
        output.append(compact)
        size += block_size
    return output


def _method_section(block):
    section = " ".join(block.get("section_path") or []).casefold()
    return any(
        word in section for word in ("method", "comput", "simulation", "theory", "calculation")
    )


_METHOD_HEADING_RE = re.compile(
    r"\b(?:methods?|methodology|comput(?:ation|ational|ing)|calculations?|"
    r"simulations?|theor(?:y|etical)|molecular\s+dynamics)\b",
    re.I,
)


def _method_neighborhood_ids(blocks, *, following_blocks=8):
    """Recover method evidence when a parser emits headings as plain paragraphs."""

    output: list[str] = []
    by_document: dict[str, list[dict[str, Any]]] = {}
    for block in blocks:
        by_document.setdefault(str(block.get("document_id") or ""), []).append(block)
    for document_blocks in by_document.values():
        for index, block in enumerate(document_blocks):
            text = " ".join(str(block.get("text") or "").split())
            if (
                not text
                or len(text) > 120
                or len(text.split()) > 14
                or not _METHOD_HEADING_RE.search(text)
            ):
                continue
            for candidate in document_blocks[index : index + following_blocks + 1]:
                output.append(str(candidate["evidence_id"]))
    return list(dict.fromkeys(output))


def _reference_section(block):
    section = " ".join(block.get("section_path") or []).casefold()
    return "reference" in section or "bibliograph" in section


def _normalize(value):
    return re.sub(r"[^a-z0-9+]", "", str(value).casefold())


def _softcite_mentions(softcite, blocks, path):
    if softcite is None:
        return [], None
    body = "".join(
        f"<p xml:id='{escape(str(block['evidence_id']))}'>"
        f"{escape(_xml10_text(str(block.get('text') or '')))}</p>"
        for block in blocks
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        f"<TEI xmlns='http://www.tei-c.org/ns/1.0'><text><body>{body}</body></text></TEI>",
        encoding="utf-8",
    )
    try:
        response = softcite.annotate_tei(path)
        return response.get("mentions") or [], None
    except Exception as exc:
        return [], {"error_type": type(exc).__name__, "message": str(exc)}


def _xml10_text(value):
    return "".join(
        character
        if ord(character) in {0x09, 0x0A, 0x0D}
        or 0x20 <= ord(character) <= 0xD7FF
        or 0xE000 <= ord(character) <= 0xFFFD
        or 0x10000 <= ord(character) <= 0x10FFFF
        else " "
        for character in value
    )


def _compact_stage02_review(review):
    return _compact_json_value(
        {
            key: review.get(key)
            for key in (
                "centrality",
                "method_families",
                "computational_actions",
                "software_clues",
                "resource_clues",
                "evidence_ids",
                "confidence",
            )
        },
        max_items=24,
    )


def _compact_rule_mentions(mentions):
    return [
        {
            "backend_hint": row.get("backend_hint"),
            "raw_name": row.get("raw_name"),
            "evidence_id": row.get("evidence_id"),
            "context": str(row.get("context") or "")[:300],
        }
        for row in mentions[:24]
    ]


def _compact_softcite_mentions(mentions):
    output = []
    for mention in mentions[:12]:
        if not isinstance(mention, dict):
            continue
        software_name = mention.get("software-name") or {}
        attributes = mention.get("mentionContextAttributes") or {}
        output.append(
            {
                "raw_name": str(software_name.get("rawForm") or "")[:120],
                "normalized_name": str(software_name.get("normalizedForm") or "")[:120],
                "context": str(mention.get("context") or "")[:240],
                "used": bool((attributes.get("used") or {}).get("value")),
                "created": bool((attributes.get("created") or {}).get("value")),
                "shared": bool((attributes.get("shared") or {}).get("value")),
            }
        )
    return output


def _bound_prompt_packet(packet, limit):
    if limit < 4000:
        raise ValueError("Stage03 max_prompt_payload_bytes must be at least 4000")
    value = copy.deepcopy(packet)

    def size():
        return len(json.dumps(value, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))

    # Candidate names are more valuable than generic trailing evidence. Retain
    # rule and Softcite candidates until the bounded evidence packet is minimal.
    trim_order = (
        ("evidence_blocks", 1),
        ("softcite_mentions", 0),
        ("rule_software_mentions", 0),
    )
    while size() > limit:
        changed = False
        for key, minimum in trim_order:
            collection = value.get(key)
            if isinstance(collection, list) and len(collection) > minimum:
                collection.pop()
                changed = True
                break
            if isinstance(collection, dict) and len(collection) > minimum:
                collection.pop(next(reversed(collection)))
                changed = True
                break
        if not changed:
            break
    if size() > limit:
        raise ValueError(f"Stage03 prompt packet cannot fit within {limit} bytes")
    return value


def _compact_json_value(value, *, max_items, max_string=240, depth=0):
    if depth >= 4:
        return str(value)[:max_string]
    if isinstance(value, dict):
        return {
            str(key): _compact_json_value(
                item,
                max_items=max_items,
                max_string=max_string,
                depth=depth + 1,
            )
            for key, item in list(value.items())[:max_items]
        }
    if isinstance(value, list):
        return [
            _compact_json_value(
                item,
                max_items=max_items,
                max_string=max_string,
                depth=depth + 1,
            )
            for item in value[:max_items]
        ]
    return str(value)[:max_string] if isinstance(value, str) else value


def _truncate_utf8(value, limit):
    output = []
    size = 0
    for character in value:
        character_size = len(character.encode("utf-8"))
        if output and size + character_size > limit:
            break
        output.append(character)
        size += character_size
    return "".join(output)


def _capability_excerpt(entry):
    keys = (
        "actions",
        "method_families",
        "system_types",
        "elements",
        "basis_or_pseudopotential_constraints",
        "periodic_support",
        "excited_state_support",
        "solvent_support",
        "force_field_support",
        "input_formats",
        "method_constraints",
        "allowed_method_values",
        "limitations",
    )
    return {key: entry.get(key, "unknown") for key in keys}


def _constraints_unknown(required, snapshot):
    for key, value in required.items():
        if value in (None, "", [], {}):
            continue
        supported = snapshot.get(key, "unknown")
        if supported in (None, "unknown"):
            return True
        if isinstance(supported, list) and isinstance(value, str) and value not in supported:
            return True
    return False
