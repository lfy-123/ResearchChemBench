from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path
from typing import Any

from src.core.io import read_json
from src.core.logging import log_progress
from src.integrations.softcite import SoftciteClient
from src.stages.stage03_software_coverage import assess_software_coverage
from src.stages.supplementary_retention import supplementary_retention


def assess_preliminary_coverage(
    papers: list[dict[str, Any]],
    documents: list[dict[str, Any]],
    client: SoftciteClient,
    toolbox_profile: dict[str, Any],
    *,
    capability_catalog: str | Path,
    aliases_file: str | Path,
    role_rules_file: str | Path,
    capability_map_file: str | Path,
    raw_output_dir: str | Path,
    workers: int = 1,
    screening_config: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    by_paper: dict[str, list[dict[str, Any]]] = defaultdict(list)
    errors: dict[str, list[dict[str, Any]]] = defaultdict(list)
    eligible = {
        str(paper["paper_id"])
        for paper in papers
        if (paper.get("pipeline_routing") or {}).get("continue", True)
        and supplementary_retention(paper)["keep"]
    }
    inputs = [
        document
        for document in documents
        if str(document["paper_id"]) in eligible and document.get("grobid_tei_path")
    ]
    rows = assess_software_coverage(
        inputs,
        client,
        toolbox_profile,
        aliases_file=aliases_file,
        role_rules_file=role_rules_file,
        capability_map_file=capability_map_file,
        raw_output_dir=raw_output_dir,
        workers=max(1, int(workers)),
        isolate_errors=True,
    )
    for row in rows:
        paper_id = str(row["paper_id"])
        coverage = row.get("software_coverage") or {}
        if coverage.get("decision") == "stage_error":
            errors[paper_id].append(
                {
                    "document_id": row.get("document_id"),
                    "error": coverage.get("error"),
                }
            )
        else:
            by_paper[paper_id].append(row)
    return aggregate_preliminary_coverage(
        papers,
        by_paper,
        toolbox_profile,
        read_json(capability_catalog),
        errors=errors,
        screening_config=screening_config,
        software_aliases=read_json(aliases_file),
    )


def aggregate_preliminary_coverage(
    papers: list[dict[str, Any]],
    software_documents: dict[str, list[dict[str, Any]]],
    toolbox_profile: dict[str, Any],
    capability_catalog: dict[str, Any],
    *,
    errors: dict[str, list[dict[str, Any]]] | None = None,
    screening_config: dict[str, Any] | None = None,
    software_aliases: dict[str, list[str]] | None = None,
) -> list[dict[str, Any]]:
    errors = errors or {}
    screening_config = screening_config or {}
    records: list[dict[str, Any]] = []
    for index, paper in enumerate(papers, start=1):
        paper_id = str(paper["paper_id"])
        documents = software_documents.get(paper_id, [])
        record = _aggregate_paper(
            paper,
            documents,
            toolbox_profile,
            capability_catalog,
            errors.get(paper_id, []),
            screening_config,
            software_aliases or {},
        )
        records.append(record)
        log_progress(
            "stage_05_preliminary_coverage",
            index,
            len(papers),
            paper_id,
            status=record["preliminary_coverage"]["decision"],
        )
    return records


def preliminary_coverage_summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    decisions: dict[str, int] = {}
    for record in records:
        decision = (record.get("preliminary_coverage") or {}).get("decision", "unknown")
        decisions[decision] = decisions.get(decision, 0) + 1
    return {
        "papers": len(records),
        "decisions": decisions,
        "continued": sum(
            (record.get("pipeline_routing") or {}).get("continue", False)
            for record in records
        ),
    }


def _aggregate_paper(
    paper,
    documents,
    toolbox,
    catalog,
    errors,
    screening_config,
    software_aliases,
):
    retention = supplementary_retention(paper)
    if not retention["keep"]:
        return {
            **paper,
            "supplementary_retention": retention,
            "preliminary_coverage": {
                "decision": "supplementary_unavailable",
                "core_software": [],
                "auxiliary_software": [],
                "unclassified_software": [],
                "ignored_mentions": [],
                "unsupported_core_software": [],
                "covered_method_families": [],
                "uncovered_method_families": [],
                "required_workflow_software": [],
                "uncovered_workflow_software": [],
                "software_inventory_complete": False,
                "software_inventory_status": "not_evaluated",
                "software_inventory_corroborated": False,
                "all_core_software_covered": False,
                "pure_computational_review": False,
                "method_coverage_scope": "not_evaluated",
                "document_decisions": [],
                "errors": [],
                "toolbox_profile_id": toolbox.get("profile_id"),
                "toolbox_catalog_hash": toolbox.get("catalog_hash"),
                "capability_schema_version": catalog.get("schema_version"),
                "unknown_capability_policy": catalog.get(
                    "unknown_field_policy", "unknown"
                ),
            },
            "pipeline_routing": {
                **(paper.get("pipeline_routing") or {}),
                "stage_05": "supplementary_unavailable",
                "continue": False,
                "stop_reason": retention["reason"],
            },
        }
    core: dict[str, dict[str, Any]] = {}
    auxiliary: dict[str, dict[str, Any]] = {}
    unclassified: dict[str, dict[str, Any]] = {}
    ignored: list[dict[str, Any]] = []
    document_decisions: list[dict[str, Any]] = []
    for document in documents:
        coverage = document.get("software_coverage") or {}
        document_decisions.append(
            {
                "document_id": document.get("document_id"),
                "document_role": document.get("document_role"),
                "decision": coverage.get("decision"),
            }
        )
        for mention in coverage.get("core_software") or []:
            core.setdefault(str(mention["normalized_name"]), mention)
        for mention in coverage.get("auxiliary_software") or []:
            auxiliary.setdefault(str(mention["normalized_name"]), mention)
        for mention in coverage.get("unclassified_software") or []:
            unclassified.setdefault(str(mention["normalized_name"]), mention)
        ignored.extend(coverage.get("ignored_mentions") or [])
    direct = [item for item in core.values() if (item.get("direct_support") or {}).get("supported")]
    equivalent = [item for item in core.values() if item.get("capability_equivalence")]
    unsupported = [
        item
        for item in core.values()
        if not (item.get("direct_support") or {}).get("supported")
        and not item.get("capability_equivalence")
    ]
    relevance = paper.get("computation_relevance") or {}
    families = set(relevance.get("method_families") or [])
    family_matrix = catalog.get("method_families") or {}
    available_backends = set(toolbox.get("backends") or []) - set(toolbox.get("unavailable") or [])
    functionally_validated_backends = (
        set(toolbox.get("scientific_smoke") or []) & available_backends
    )
    toolbox_covered_families = {
        family
        for family in families
        if available_backends & set((family_matrix.get(family) or {}).get("backends") or [])
    }
    validated_toolbox_covered_families = _covered_method_families(
        functionally_validated_backends, families, family_matrix
    )
    strict = str(screening_config.get("screening_policy", "recall")) == "strict"
    accepted_levels = set(
        screening_config.get("accepted_validation_levels")
        or (["functional"] if strict else ["functional", "interface", "needs_complete_input", "catalogued"])
    )
    require_execution = bool(
        screening_config.get("require_execution_context", strict)
    )
    require_method_match = bool(screening_config.get("require_method_match", strict))
    allow_equivalent = bool(
        screening_config.get("allow_capability_equivalent", not strict)
    )
    continue_without_name = bool(
        screening_config.get("continue_without_software_name", not strict)
    )
    continue_on_error = bool(screening_config.get("continue_on_stage_error", not strict))
    require_all_core = bool(
        screening_config.get("require_all_core_software", strict)
    )
    require_all_families = bool(
        screening_config.get("require_all_method_families", strict)
    )
    reject_unclassified_execution = bool(
        screening_config.get("reject_unclassified_execution_software", strict)
    )
    require_pure_review = bool(
        screening_config.get("require_pure_computational_review", strict)
    )
    require_inventory_complete = bool(
        screening_config.get("require_complete_software_inventory", strict)
    )
    eligible_direct = [
        item
        for item in direct
        if (
            (item.get("direct_support") or {}).get("validation_level") in accepted_levels
            or (
                not strict
                and not (item.get("direct_support") or {}).get("validation_level")
            )
        )
        and (not require_execution or item.get("execution_context_confirmed"))
        and (
            not require_method_match
            or _backend_matches_method_families(
                str(item["normalized_name"]), families, family_matrix
            )
        )
    ]
    ineligible_direct = [
        item["normalized_name"] for item in direct if item not in eligible_direct
    ]
    review = paper.get("llm_computation_review") or {}
    pure_review = (
        review.get("study_mode") == "pure_computational"
        and review.get("author_performed_experiments") == "no"
        and review.get("computation_role") == "primary"
    )
    required_workflow = _assess_required_workflow_software(
        review.get("required_software") or [],
        toolbox=toolbox,
        aliases=software_aliases,
        accepted_levels=accepted_levels,
        families=families,
        family_matrix=family_matrix,
        require_method_match=require_method_match,
    )
    uncovered_required = [
        item for item in required_workflow if not item["covered"]
    ]
    covered_required = [item for item in required_workflow if item["covered"]]
    eligible_workflow_backends = {
        *(str(item["normalized_name"]) for item in eligible_direct),
        *(str(item["normalized_name"]) for item in covered_required),
    }
    covered_families = (
        validated_toolbox_covered_families if strict else toolbox_covered_families
    )
    uncovered_families = families - covered_families
    unclassified_execution = [
        item
        for item in unclassified.values()
        if item.get("execution_context_confirmed")
    ]
    uncovered_core = [
        item
        for item in core.values()
        if item not in eligible_direct
    ]
    uncovered_workflow_names = {
        *(str(item["normalized_name"]) for item in uncovered_core),
        *(str(item["normalized_name"]) for item in uncovered_required),
    }
    if reject_unclassified_execution:
        uncovered_workflow_names.update(
            str(item["normalized_name"]) for item in unclassified_execution
        )
    inventory_status = str(review.get("software_inventory_complete") or "uncertain")
    required_names = {
        str(item["normalized_name"]) for item in required_workflow
    }
    observed_names = {*core, *auxiliary}
    inventory_corroborated = (
        inventory_status == "uncertain"
        and bool(required_names)
        and required_names.issubset(observed_names)
        and not uncovered_core
        and not uncovered_required
        and not unclassified_execution
    )
    inventory_complete = inventory_status == "yes" or inventory_corroborated
    if require_pure_review and not pure_review:
        decision = "not_pure_computational"
        continue_pipeline = False
        reason = "pure_computational_llm_confirmation_required"
    elif errors:
        decision = "stage_error"
        continue_pipeline = continue_on_error
        reason = "software_extraction_failed"
    elif require_all_core and uncovered_workflow_names:
        decision = "workflow_software_uncovered"
        continue_pipeline = False
        reason = "all_workflow_software_must_be_functionally_covered"
    elif require_all_families and eligible_workflow_backends and uncovered_families:
        decision = "method_coverage_incomplete"
        continue_pipeline = False
        reason = "all_computational_method_families_must_be_covered"
    elif require_inventory_complete and not inventory_complete:
        decision = "workflow_inventory_unconfirmed"
        continue_pipeline = False
        reason = "complete_workflow_software_inventory_required"
    elif eligible_direct or covered_required:
        decision = "direct_candidate"
        continue_pipeline = True
        reason = None
    elif direct:
        decision = "direct_support_unverified"
        continue_pipeline = False
        reason = "direct_software_failed_strict_validation"
    elif equivalent and allow_equivalent:
        decision = "equivalent_candidate"
        continue_pipeline = True
        reason = None
    elif equivalent:
        decision = "equivalent_unverified"
        continue_pipeline = False
        reason = "capability_equivalence_not_allowed"
    elif core and len(unsupported) == len(core):
        decision = "explicitly_unsupported"
        continue_pipeline = False
        reason = "all_identified_core_software_explicitly_unsupported"
    elif toolbox_covered_families and continue_without_name:
        decision = "method_only_candidate"
        continue_pipeline = True
        reason = None
    elif toolbox_covered_families:
        decision = "method_only_rejected"
        continue_pipeline = False
        reason = "direct_functionally_validated_backend_required"
    elif relevance.get("decision") in {"strong_candidate", "weak_candidate", "rule_error"}:
        if strict:
            decision = "software_unknown_rejected"
            continue_pipeline = False
            reason = "direct_functionally_validated_backend_required"
        else:
            decision = "software_unknown_candidate"
            continue_pipeline = True
            reason = None
    else:
        decision = "not_significant"
        continue_pipeline = False
        reason = "no_core_computation_or_software_evidence"
    return {
        **paper,
        "supplementary_retention": retention,
        "preliminary_coverage": {
            "decision": decision,
            "core_software": list(core.values()),
            "auxiliary_software": list(auxiliary.values()),
            "unclassified_software": list(unclassified.values()),
            "ignored_mentions": ignored,
            "unsupported_core_software": [item["normalized_name"] for item in unsupported],
            "covered_method_families": sorted(covered_families),
            "uncovered_method_families": sorted(uncovered_families),
            "ineligible_direct_software": ineligible_direct,
            "required_workflow_software": required_workflow,
            "uncovered_workflow_software": sorted(uncovered_workflow_names),
            "software_inventory_complete": inventory_complete,
            "software_inventory_status": inventory_status,
            "software_inventory_corroborated": inventory_corroborated,
            "all_core_software_covered": (
                bool(core or required_workflow)
                and not uncovered_core
                and not uncovered_required
            ),
            "pure_computational_review": pure_review,
            "screening_policy": "strict" if strict else "recall",
            "method_coverage_scope": (
                "functionally_validated_toolbox_backends"
                if strict
                else "available_toolbox_backends"
            ),
            "document_decisions": document_decisions,
            "errors": errors,
            "toolbox_profile_id": toolbox.get("profile_id"),
            "toolbox_catalog_hash": toolbox.get("catalog_hash"),
            "capability_schema_version": catalog.get("schema_version"),
            "unknown_capability_policy": catalog.get("unknown_field_policy", "unknown"),
        },
        "pipeline_routing": {
            **(paper.get("pipeline_routing") or {}),
            "stage_05": decision,
            "continue": continue_pipeline,
            "stop_reason": reason,
        },
    }


def _backend_matches_method_families(
    backend: str,
    families: set[str],
    family_matrix: dict[str, Any],
) -> bool:
    normalized = backend.casefold()
    for family in families:
        backends = {
            str(item).casefold()
            for item in (family_matrix.get(family) or {}).get("backends") or []
        }
        if normalized in backends:
            return True
    return False


def _covered_method_families(
    backends: set[str],
    families: set[str],
    family_matrix: dict[str, Any],
) -> set[str]:
    normalized_backends = {item.casefold() for item in backends}
    return {
        family
        for family in families
        if normalized_backends
        & {
            str(item).casefold()
            for item in (family_matrix.get(family) or {}).get("backends") or []
        }
    }


def _assess_required_workflow_software(
    values: list[dict[str, Any]],
    *,
    toolbox: dict[str, Any],
    aliases: dict[str, list[str]],
    accepted_levels: set[str],
    families: set[str],
    family_matrix: dict[str, Any],
    require_method_match: bool,
) -> list[dict[str, Any]]:
    alias_index = _software_alias_index(aliases)
    output: dict[str, dict[str, Any]] = {}
    for value in values:
        raw_name = str(value.get("name") or "").strip()
        if not raw_name:
            continue
        normalized = _normalize_required_software(raw_name, alias_index)
        validation_level = _toolbox_validation_level(normalized, toolbox)
        supported = validation_level != "not_catalogued"
        method_match = (
            not require_method_match
            or _backend_matches_method_families(
                normalized, families, family_matrix
            )
        )
        output.setdefault(
            normalized,
            {
                **value,
                "normalized_name": normalized,
                "validation_level": validation_level,
                "covered": (
                    supported
                    and validation_level in accepted_levels
                    and method_match
                ),
                "method_match": method_match,
            },
        )
    return list(output.values())


def _software_alias_index(aliases: dict[str, list[str]]) -> dict[str, str]:
    output: dict[str, str] = {}
    for normalized, values in aliases.items():
        output[_software_key(normalized)] = normalized
        for value in values:
            output[_software_key(value)] = normalized
    return output


def _normalize_required_software(value: str, aliases: dict[str, str]) -> str:
    key = _software_key(value)
    if key in aliases:
        return aliases[key]
    for alias in sorted(aliases, key=len, reverse=True):
        if re.search(rf"(?:^|\s){re.escape(alias)}(?:$|\s)", key):
            return aliases[alias]
    return key.replace(" ", "_")


def _toolbox_validation_level(name: str, toolbox: dict[str, Any]) -> str:
    unavailable = {str(item).casefold() for item in toolbox.get("unavailable", [])}
    if name.casefold() in unavailable:
        return "not_catalogued"
    for field, level in (
        ("scientific_smoke", "functional"),
        ("interface_smoke", "interface"),
        ("needs_complete_input", "needs_complete_input"),
    ):
        if name.casefold() in {
            str(item).casefold() for item in toolbox.get(field, [])
        }:
            return level
    available = {
        *(str(item).casefold() for item in toolbox.get("backends", [])),
        *(str(item).casefold() for item in toolbox.get("available_identifiers", [])),
    }
    return "catalogued" if name.casefold() in available else "not_catalogued"


def _software_key(value: str) -> str:
    return re.sub(r"[^a-z0-9+]+", " ", str(value).casefold()).strip()
