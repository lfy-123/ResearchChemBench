#!/usr/bin/env python3
"""Reclassify historical Stage03 records with the current deterministic gate."""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
from typing import Any

from src.contracts import read_json, read_jsonl, write_json, write_jsonl
from src.stages.stage03_toolbox_resource_gate.stage import (
    _combine_decision,
    _freeze_workflow_bindings,
    _stage02_confirmed_workflows,
    coverage_gate,
    resolve_software,
    workflow_coverage_results,
)


def main() -> int:
    args = _parse_args()
    stage02 = {row["paper_id"]: row for row in read_jsonl(args.stage02)}
    stage03 = read_jsonl(args.stage03)
    aliases = read_json(args.software_aliases)
    external_aliases = read_json(args.external_software_aliases)
    profile = read_json(args.toolbox_capabilities)
    rows = []
    for old in stage03:
        paper_id = str(old.get("paper_id") or "")
        upstream = stage02.get(paper_id)
        if upstream is None or not old.get("model_review"):
            continue
        evidence_ids = _collect_evidence_ids(
            {"stage02": upstream, "stage03": old.get("model_review")}
        )
        frozen, contract_status, contract_warnings = _stage02_confirmed_workflows(
            upstream, evidence_ids
        )
        locked, freeze_warnings = _freeze_workflow_bindings(
            frozen,
            (old.get("model_review") or {}).get("workflows") or [],
            {value: "" for value in evidence_ids},
        )
        review = dict(old.get("model_review") or {})
        review["workflows"] = locked
        mappings = resolve_software(
            review.get("software_mentions") or [],
            aliases,
            profile,
            external_aliases=external_aliases,
        )
        workflow_results = workflow_coverage_results(review, mappings)
        coverage = coverage_gate(
            review,
            mappings,
            profile,
            {},
            workflow_results=workflow_results,
        )
        new_decision = _combine_decision(coverage)
        rows.append(
            {
                "paper_id": paper_id,
                "doi": old.get("doi"),
                "title": old.get("title"),
                "old_decision": old.get("decision"),
                "new_decision": new_decision,
                "changed": old.get("decision") != new_decision,
                "upstream_contract_status": contract_status,
                "confirmed_workflows": frozen,
                "workflow_coverage_results": workflow_results,
                "software_mappings": mappings,
                "warnings": [*contract_warnings, *freeze_warnings],
            }
        )
    transitions = Counter(
        (str(row["old_decision"]), str(row["new_decision"])) for row in rows
    )
    summary = {
        "source_stage02": str(args.stage02.resolve()),
        "source_stage03": str(args.stage03.resolve()),
        "papers": len(rows),
        "changed": sum(bool(row["changed"]) for row in rows),
        "old_decisions": dict(Counter(str(row["old_decision"]) for row in rows)),
        "new_decisions": dict(Counter(str(row["new_decision"]) for row in rows)),
        "transitions": {
            f"{old} -> {new}": count
            for (old, new), count in sorted(transitions.items())
        },
    }
    write_jsonl(args.output / "decisions.jsonl", rows)
    write_json(args.output / "summary.json", summary)
    print(summary)
    return 0


def _collect_evidence_ids(value: Any) -> set[str]:
    output: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            if key == "evidence_ids" and isinstance(item, list):
                output.update(str(entry) for entry in item if str(entry))
            else:
                output.update(_collect_evidence_ids(item))
    elif isinstance(value, list):
        for item in value:
            output.update(_collect_evidence_ids(item))
    return output


def _parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage02", type=Path, required=True)
    parser.add_argument("--stage03", type=Path, required=True)
    parser.add_argument("--toolbox-capabilities", type=Path, required=True)
    parser.add_argument("--software-aliases", type=Path, required=True)
    parser.add_argument("--external-software-aliases", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    return parser.parse_args()


if __name__ == "__main__":
    raise SystemExit(main())
