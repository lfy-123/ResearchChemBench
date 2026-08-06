from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any

from src.core.io import read_json
from src.core.logging import log_progress
from src.integrations.softcite import SoftciteClient
from src.stages.stage03_software_coverage import assess_software_coverage


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
) -> list[dict[str, Any]]:
    by_paper: dict[str, list[dict[str, Any]]] = defaultdict(list)
    errors: dict[str, list[dict[str, Any]]] = defaultdict(list)
    eligible = {
        str(paper["paper_id"])
        for paper in papers
        if (paper.get("pipeline_routing") or {}).get("continue", True)
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
    )


def aggregate_preliminary_coverage(
    papers: list[dict[str, Any]],
    software_documents: dict[str, list[dict[str, Any]]],
    toolbox_profile: dict[str, Any],
    capability_catalog: dict[str, Any],
    *,
    errors: dict[str, list[dict[str, Any]]] | None = None,
) -> list[dict[str, Any]]:
    errors = errors or {}
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


def _aggregate_paper(paper, documents, toolbox, catalog, errors):
    core: dict[str, dict[str, Any]] = {}
    auxiliary: dict[str, dict[str, Any]] = {}
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
    covered_families = {
        family
        for family in families
        if available_backends & set((family_matrix.get(family) or {}).get("backends") or [])
    }
    if errors and not documents:
        decision = "stage_error"
        continue_pipeline = True
        reason = "software_extraction_failed"
    elif direct:
        decision = "direct_candidate"
        continue_pipeline = True
        reason = None
    elif equivalent:
        decision = "equivalent_candidate"
        continue_pipeline = True
        reason = None
    elif core and len(unsupported) == len(core):
        decision = "explicitly_unsupported"
        continue_pipeline = False
        reason = "all_identified_core_software_explicitly_unsupported"
    elif covered_families:
        decision = "method_only_candidate"
        continue_pipeline = True
        reason = None
    elif relevance.get("decision") in {"strong_candidate", "weak_candidate", "rule_error"}:
        decision = "software_unknown_candidate"
        continue_pipeline = True
        reason = None
    else:
        decision = "not_significant"
        continue_pipeline = False
        reason = "no_core_computation_or_software_evidence"
    return {
        **paper,
        "preliminary_coverage": {
            "decision": decision,
            "core_software": list(core.values()),
            "auxiliary_software": list(auxiliary.values()),
            "ignored_mentions": ignored,
            "unsupported_core_software": [item["normalized_name"] for item in unsupported],
            "covered_method_families": sorted(covered_families),
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
