from __future__ import annotations

import hashlib
import re
from pathlib import Path
from typing import Any

import yaml

from src.core.concurrency import ordered_parallel_map
from src.core.logging import log_progress


def assess_computation_relevance(
    paper_bundles: list[dict[str, Any]],
    *,
    method_ontology: str | Path,
    evidence_rules: str | Path,
    negative_contexts: str | Path,
    workers: int = 1,
) -> list[dict[str, Any]]:
    ontology_path = Path(method_ontology)
    rules_path = Path(evidence_rules)
    negative_path = Path(negative_contexts)
    ontology = _read_yaml(ontology_path)
    rules = _read_yaml(rules_path)
    negative = _read_yaml(negative_path)
    rule_hash = _rules_hash((ontology_path, rules_path, negative_path))
    def assess(bundle: dict[str, Any]) -> dict[str, Any]:
        try:
            return _assess_paper(bundle, ontology, rules, negative, rule_hash)
        except Exception as exc:
            return {
                **bundle,
                "computation_relevance": {
                    "decision": "rule_error",
                    "score": 0.0,
                    "evidence": [],
                    "excluded_evidence": [],
                    "rule_hash": rule_hash,
                    "error": f"{type(exc).__name__}: {exc}",
                },
                "pipeline_routing": {
                    "stage_03": "rule_error",
                    "continue": True,
                    "stop_reason": None,
                },
            }

    return ordered_parallel_map(
        assess,
        paper_bundles,
        max_workers=workers,
        on_complete=lambda completed, total, _index, bundle, record: log_progress(
            "stage_03_computation_relevance",
            completed,
            total,
            str(bundle["paper_id"]),
            status=record["computation_relevance"]["decision"],
        ),
    )


def computation_relevance_summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    decisions: dict[str, int] = {}
    for record in records:
        decision = (record.get("computation_relevance") or {}).get("decision", "unknown")
        decisions[decision] = decisions.get(decision, 0) + 1
    return {
        "papers": len(records),
        "decisions": decisions,
        "candidates": decisions.get("strong_candidate", 0)
        + decisions.get("weak_candidate", 0),
        "errors_retained_for_review": decisions.get("rule_error", 0),
    }


def _assess_paper(
    bundle: dict[str, Any],
    ontology: dict[str, Any],
    rules: dict[str, Any],
    negative: dict[str, Any],
    rule_hash: str,
) -> dict[str, Any]:
    evidence: list[dict[str, Any]] = []
    excluded: list[dict[str, Any]] = []
    documents = [
        *(bundle.get("main_documents") or []),
        *(bundle.get("supplementary_documents") or []),
    ]
    for document in documents:
        text_path = document.get("text_path")
        if not text_path or not Path(text_path).is_file():
            continue
        text = Path(text_path).read_text(encoding="utf-8", errors="replace")
        for section, section_text, section_start in _sections(text):
            target = excluded if _excluded_section(section, negative) else evidence
            target.extend(
                _section_evidence(
                    section_text,
                    section=section,
                    offset=section_start,
                    document=document,
                    ontology=ontology,
                    rules=rules,
                    negative=negative,
                    excluded_by_section=target is excluded,
                )
            )
    valid = [item for item in evidence if not item.get("excluded")]
    excluded.extend(item for item in evidence if item.get("excluded"))
    valid = [item for item in valid if not item.get("excluded")]
    raw_score = round(sum(float(item["weighted_score"]) for item in valid), 3)
    scored_evidence = _score_contributions(valid, rules)
    score = round(sum(float(item["weighted_score"]) for item in scored_evidence), 3)
    types = {item["evidence_type"] for item in valid}
    method_or_action = bool(types & {"method_evidence", "action_evidence"})
    execution = "performed_here_evidence" in types
    result_or_pointer = bool(types & {"result_evidence", "si_computation_pointer"})
    method_mentions = sum(
        item["evidence_type"] == "method_evidence" for item in valid
    )
    thresholds = rules.get("thresholds") or {}
    if score >= float(thresholds.get("strong", 7)) and method_or_action and execution and result_or_pointer:
        decision = "strong_candidate"
    elif (
        score >= float(thresholds.get("weak", 3))
        and method_or_action
        and (len(types) >= 2 or method_mentions >= 2)
    ):
        decision = "weak_candidate"
    else:
        decision = "not_computational"
    return {
        **bundle,
        "computation_relevance": {
            "decision": decision,
            "score": score,
            "raw_score": raw_score,
            "score_contribution_count": len(scored_evidence),
            "evidence_types": sorted(types),
            "method_families": sorted(
                {item["family"] for item in valid if item.get("family")}
            ),
            "evidence": valid,
            "excluded_evidence": excluded,
            "rule_hash": rule_hash,
            "used_llm": False,
        },
        "pipeline_routing": {
            "stage_03": decision,
            "continue": decision in {"strong_candidate", "weak_candidate", "rule_error"},
            "stop_reason": None if decision != "not_computational" else "no_computation_evidence",
        },
    }


def _section_evidence(
    text: str,
    *,
    section: str,
    offset: int,
    document: dict[str, Any],
    ontology: dict[str, Any],
    rules: dict[str, Any],
    negative: dict[str, Any],
    excluded_by_section: bool,
) -> list[dict[str, Any]]:
    patterns: list[tuple[str, str, str | None, str]] = []
    for family, values in (ontology.get("families") or {}).items():
        patterns.extend(("method_evidence", term, family, f"method:{family}:{term}") for term in values.get("terms", []))
        patterns.extend(("result_evidence", term, family, f"result:{family}:{term}") for term in values.get("results", []))
    patterns.extend(("action_evidence", term, None, f"action:{term}") for term in rules.get("actions", []))
    patterns.extend(("performed_here_evidence", pattern, None, f"performed:{index}") for index, pattern in enumerate(rules.get("performed_here_patterns", []), start=1))
    patterns.extend(("si_computation_pointer", pattern, None, f"si_pointer:{index}") for index, pattern in enumerate(rules.get("si_pointer_patterns", []), start=1))
    output: list[dict[str, Any]] = []
    negative_patterns = [re.compile(item, re.I) for item in negative.get("patterns", [])]
    for evidence_type, raw_pattern, family, rule_id in patterns:
        pattern = re.compile(raw_pattern, re.I) if evidence_type in {"performed_here_evidence", "si_computation_pointer"} else re.compile(rf"(?<![A-Za-z0-9]){re.escape(raw_pattern)}(?![A-Za-z0-9])", re.I)
        for match in pattern.finditer(text):
            start = max(0, match.start() - 140)
            end = min(len(text), match.end() + 140)
            snippet = " ".join(text[start:end].split())
            negative_match = next((item.pattern for item in negative_patterns if item.search(snippet)), None)
            excluded = excluded_by_section or negative_match is not None
            base_weight = float((rules.get("weights") or {}).get(evidence_type, 1))
            section_weight = float((rules.get("section_weights") or {}).get(_section_kind(section), 1))
            output.append(
                {
                    "paper_id": document.get("paper_id"),
                    "document_id": document.get("document_id"),
                    "document_role": document.get("document_role"),
                    "evidence_type": evidence_type,
                    "family": family,
                    "rule_id": rule_id,
                    "matched_text": match.group(0),
                    "section": section,
                    "character_start": offset + match.start(),
                    "character_end": offset + match.end(),
                    "snippet": snippet,
                    "weighted_score": round(base_weight * section_weight, 3),
                    "excluded": excluded,
                    "exclusion_reason": "excluded_section" if excluded_by_section else negative_match,
                }
            )
    return _deduplicate_evidence(output)


def _sections(text: str) -> list[tuple[str, str, int]]:
    lines = text.splitlines(keepends=True)
    output: list[tuple[str, str, int]] = []
    current_name = "unknown"
    current: list[str] = []
    start = 0
    cursor = 0
    heading = re.compile(r"^\s*(?:\d+(?:\.\d+)*\s+)?([A-Z][A-Za-z /&-]{2,60})\s*$")
    for line in lines:
        match = heading.match(line.rstrip())
        if match and len(line.split()) <= 8:
            if current:
                output.append((current_name, "".join(current), start))
            current_name = match.group(1).strip()
            current = [line]
            start = cursor
        else:
            current.append(line)
        cursor += len(line)
    if current:
        output.append((current_name, "".join(current), start))
    return output or [("unknown", text, 0)]


def _section_kind(section: str) -> str:
    value = section.casefold()
    for kind, terms in {
        "abstract": ("abstract",),
        "method": ("method", "computational", "theoretical", "experimental"),
        "result": ("result", "discussion"),
        "conclusion": ("conclusion",),
        "introduction": ("introduction", "background"),
        "title": ("title",),
    }.items():
        if any(term in value for term in terms):
            return kind
    return "unknown"


def _excluded_section(section: str, negative: dict[str, Any]) -> bool:
    value = section.casefold()
    return any(term.casefold() in value for term in negative.get("excluded_sections", []))


def _deduplicate_evidence(items: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: dict[tuple[Any, ...], dict[str, Any]] = {}
    for item in items:
        key = (item["document_id"], item["evidence_type"], item["character_start"], item["character_end"])
        output.setdefault(key, item)
    return list(output.values())


def _score_contributions(
    evidence: list[dict[str, Any]], rules: dict[str, Any]
) -> list[dict[str, Any]]:
    limit = int(rules.get("max_contributions_per_rule_section", 2))
    if limit < 1:
        raise ValueError("max_contributions_per_rule_section must be positive")
    counts: dict[tuple[Any, ...], int] = {}
    output: list[dict[str, Any]] = []
    for item in evidence:
        key = (
            item.get("document_id"),
            item.get("evidence_type"),
            item.get("rule_id"),
            _section_kind(str(item.get("section") or "")),
        )
        count = counts.get(key, 0)
        if count >= limit:
            continue
        counts[key] = count + 1
        output.append(item)
    return output


def _read_yaml(path: Path) -> dict[str, Any]:
    value = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"rule asset must contain a mapping: {path}")
    return value


def _rules_hash(paths: tuple[Path, ...]) -> str:
    digest = hashlib.sha256()
    for path in paths:
        digest.update(path.read_bytes())
    return digest.hexdigest()
