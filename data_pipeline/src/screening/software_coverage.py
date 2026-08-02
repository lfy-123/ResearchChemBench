from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from src.core.io import read_json, write_json
from src.core.logging import log_progress
from src.ingestion.softcite import SoftciteClient
from src.ingestion.tei import read_tei_paragraphs, sentence_windows


def assess_software_coverage(
    documents: list[dict[str, Any]],
    client: SoftciteClient,
    toolbox_profile: dict[str, Any],
    *,
    aliases_file: str | Path,
    role_rules_file: str | Path,
    capability_map_file: str | Path,
    raw_output_dir: str | Path,
) -> list[dict[str, Any]]:
    aliases = _alias_index(read_json(aliases_file))
    role_rules = read_json(role_rules_file)
    capability_rules = read_json(capability_map_file)
    raw_dir = Path(raw_output_dir).expanduser().resolve()
    raw_dir.mkdir(parents=True, exist_ok=True)
    service_version = client.version()
    output: list[dict[str, Any]] = []

    for index, document in enumerate(documents, start=1):
        tei_path = document.get("grobid_tei_path")
        if not tei_path:
            raise ValueError(f"Missing GROBID TEI for {document.get('paper_id')}")
        raw = client.annotate_tei(tei_path)
        write_json(raw_dir / f"{document['document_id']}.json", raw)
        direct_mentions = _softcite_mentions(raw.get("mentions") or [], aliases, role_rules)
        recovered_mentions = _recover_known_software(
            tei_path,
            direct_mentions,
            aliases,
            role_rules,
            client,
        )
        mentions = _merge_mentions([*direct_mentions, *recovered_mentions])
        core = [item for item in mentions if item["role"] == "core" and item["used"]]
        auxiliary = [item for item in mentions if item["role"] == "auxiliary" and item["used"]]
        ignored = [item for item in mentions if item["role"] == "ignore" or not item["used"]]

        for mention in core:
            mention["direct_support"] = _direct_support(
                mention["normalized_name"], toolbox_profile
            )
            mention["capability_equivalence"] = _capability_equivalence(
                mention, capability_rules, toolbox_profile
            )

        unsupported = [
            item
            for item in core
            if not item["direct_support"]["supported"]
            and not item["capability_equivalence"]
        ]
        equivalent = [
            item
            for item in core
            if not item["direct_support"]["supported"]
            and item["capability_equivalence"]
        ]
        if not core or unsupported:
            decision = "unsupported"
            status = "reject"
            stop_reason = "no_core_software" if not core else "unsupported_core_software"
        elif equivalent:
            decision = "capability_equivalent"
            status = "candidate"
            stop_reason = "capability_equivalent_backup"
        else:
            decision = "direct_covered"
            status = "pass"
            stop_reason = None

        record = {
            **document,
            "software_coverage": {
                "status": status,
                "decision": decision,
                "core_software": core,
                "auxiliary_software": auxiliary,
                "ignored_mentions": ignored,
                "unsupported_core_software": [
                    item["normalized_name"] for item in unsupported
                ],
                "equivalent_core_software": [item["normalized_name"] for item in equivalent],
                "service_version": service_version,
                "softcite_raw_path": str(raw_dir / f"{document['document_id']}.json"),
            },
            "pipeline_routing": {
                "stage_03": decision,
                "stage_04": "pending" if decision == "direct_covered" else "not_run",
                "stage_05": "pending" if decision == "direct_covered" else "not_run",
                "continue": decision == "direct_covered",
                "stopped_at": None if decision == "direct_covered" else "stage_03_software_coverage",
                "stop_reason": stop_reason,
            },
        }
        output.append(record)
        log_progress(
            "stage_03_software_coverage",
            index,
            len(documents),
            document.get("title") or document["paper_id"],
            status=decision,
        )
    return output


def software_coverage_summary(records: list[dict[str, Any]]) -> dict[str, Any]:
    decisions: dict[str, int] = {}
    for record in records:
        decision = (record.get("software_coverage") or {}).get("decision", "unknown")
        decisions[decision] = decisions.get(decision, 0) + 1
    return {
        "documents": len(records),
        "decisions": decisions,
        "direct_covered": decisions.get("direct_covered", 0),
        "capability_equivalent_candidates": decisions.get("capability_equivalent", 0),
        "unsupported": decisions.get("unsupported", 0),
    }


def _softcite_mentions(
    raw_mentions: list[dict[str, Any]],
    aliases: dict[str, str],
    role_rules: dict[str, Any],
) -> list[dict[str, Any]]:
    output = []
    for raw in raw_mentions:
        name = raw.get("software-name") or {}
        raw_name = str(name.get("rawForm") or name.get("normalizedForm") or "").strip()
        if not raw_name:
            continue
        normalized = _normalize_software(raw_name, aliases)
        document_used = ((raw.get("documentContextAttributes") or {}).get("used") or {})
        mention_used = ((raw.get("mentionContextAttributes") or {}).get("used") or {})
        used_payload = document_used if "value" in document_used else mention_used
        used = bool(used_payload.get("value")) if "value" in used_payload else False
        output.append(
            {
                "raw_name": raw_name,
                "normalized_name": normalized,
                "version": ((raw.get("version") or {}).get("normalizedForm") or ""),
                "role": _software_role(normalized, raw_name, role_rules),
                "used": used,
                "used_score": used_payload.get("score"),
                "evidence": str(raw.get("context") or "").strip(),
                "source": "softcite_ner",
                "softcite_mention": raw,
            }
        )
    return output


def _recover_known_software(
    tei_path: str | Path,
    existing: list[dict[str, Any]],
    aliases: dict[str, str],
    role_rules: dict[str, Any],
    client: SoftciteClient,
) -> list[dict[str, Any]]:
    existing_names = {item["normalized_name"] for item in existing}
    candidates: dict[str, tuple[str, dict[str, Any]]] = {}
    alias_patterns = sorted(aliases, key=len, reverse=True)
    for paragraph in read_tei_paragraphs(tei_path):
        for sentence in sentence_windows(paragraph):
            for alias_key in alias_patterns:
                normalized = aliases[alias_key]
                if normalized in existing_names or normalized in candidates:
                    continue
                if _contains_alias(sentence["text"], alias_key):
                    candidates[normalized] = (alias_key, sentence)
    output = []
    for normalized, (alias_key, sentence) in candidates.items():
        result = client.characterize_context(sentence["text"])
        used_payload = ((result.get("classification") or {}).get("used") or {})
        output.append(
            {
                "raw_name": alias_key,
                "normalized_name": normalized,
                "version": "",
                "role": _software_role(normalized, alias_key, role_rules),
                "used": bool(used_payload.get("value")),
                "used_score": used_payload.get("score"),
                "evidence": sentence["text"],
                "section": sentence.get("section"),
                "paragraph_index": sentence.get("paragraph_index"),
                "source": "toolbox_lexicon_softcite_context",
                "softcite_context": result,
            }
        )
    return output


def _merge_mentions(mentions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: dict[str, dict[str, Any]] = {}
    for mention in mentions:
        key = mention["normalized_name"]
        current = output.get(key)
        if current is None or (not current["used"] and mention["used"]):
            output[key] = mention
        elif current and mention.get("evidence") and mention["evidence"] != current.get("evidence"):
            current.setdefault("additional_evidence", []).append(mention["evidence"])
    return list(output.values())


def _alias_index(value: dict[str, Any]) -> dict[str, str]:
    output: dict[str, str] = {}
    for normalized, aliases in value.items():
        output[_alias_key(normalized)] = normalized
        for alias in aliases:
            output[_alias_key(str(alias))] = normalized
    return output


def _normalize_software(value: str, aliases: dict[str, str]) -> str:
    key = _alias_key(re.sub(r"\b(?:version|ver\.?|v)\s*\d+(?:\.\d+)*\b", "", value, flags=re.I))
    return aliases.get(key, key.replace(" ", "_"))


def _software_role(normalized: str, raw_name: str, rules: dict[str, Any]) -> str:
    ignored = {_alias_key(item) for item in rules.get("ignore", [])}
    auxiliary = {_alias_key(item) for item in rules.get("auxiliary", [])}
    values = {_alias_key(normalized), _alias_key(raw_name)}
    if values & ignored:
        return "ignore"
    if values & auxiliary:
        return "auxiliary"
    return "core"


def _direct_support(name: str, toolbox: dict[str, Any]) -> dict[str, Any]:
    unavailable = {str(item).casefold() for item in toolbox.get("unavailable", [])}
    backends = {str(item).casefold() for item in toolbox.get("backends", [])}
    supported = name.casefold() in backends and name.casefold() not in unavailable
    if name in toolbox.get("scientific_smoke", []):
        level = "functional"
    elif name in toolbox.get("interface_smoke", []):
        level = "interface"
    elif name in toolbox.get("needs_complete_input", []):
        level = "needs_complete_input"
    else:
        level = "catalogued" if supported else "unavailable"
    return {"supported": supported, "backend": name if supported else None, "validation_level": level}


def _capability_equivalence(
    mention: dict[str, Any], rules: dict[str, Any], toolbox: dict[str, Any]
) -> dict[str, Any] | None:
    rule = rules.get(mention["normalized_name"])
    if not rule:
        return None
    evidence = mention.get("evidence", "").casefold()
    usage_patterns = rule.get("usage_patterns") or []
    if usage_patterns and not any(pattern.casefold() in evidence for pattern in usage_patterns):
        return None
    actions = set(toolbox.get("actions", []))
    required = set(rule.get("required_actions", []))
    available_backends = set(toolbox.get("backends", []))
    equivalent_backends = [
        item for item in rule.get("equivalent_backends", []) if item in available_backends
    ]
    if not required.issubset(actions) or not equivalent_backends:
        return None
    return {
        "required_actions": sorted(required),
        "equivalent_backends": equivalent_backends,
        "limitations": rule.get("limitations", []),
    }


def _contains_alias(text: str, alias_key: str) -> bool:
    pattern = r"(?<![A-Za-z0-9])" + re.escape(alias_key).replace(r"\ ", r"[\s_-]+") + r"(?![A-Za-z0-9])"
    return re.search(pattern, _alias_key(text), re.I) is not None


def _alias_key(value: str) -> str:
    return re.sub(r"[^a-z0-9+]+", " ", str(value).casefold()).strip()
