from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from src.core.concurrency import ordered_parallel_map
from src.core.io import read_json, write_json
from src.core.logging import log_progress
from src.integrations.softcite import SoftciteClient
from src.integrations.tei import read_tei_paragraphs, sentence_windows


def assess_software_coverage(
    documents: list[dict[str, Any]],
    client: SoftciteClient,
    toolbox_profile: dict[str, Any],
    *,
    aliases_file: str | Path,
    role_rules_file: str | Path,
    capability_map_file: str | Path,
    raw_output_dir: str | Path,
    workers: int = 1,
    isolate_errors: bool = False,
) -> list[dict[str, Any]]:
    aliases = _alias_index(read_json(aliases_file))
    role_rules = read_json(role_rules_file)
    capability_rules = read_json(capability_map_file)
    known_core = {
        *aliases.values(),
        *capability_rules.keys(),
        *(_alias_key(item) for item in role_rules.get("core", [])),
    }
    raw_dir = Path(raw_output_dir).expanduser().resolve()
    raw_dir.mkdir(parents=True, exist_ok=True)
    service_version = client.version()

    def assess(document: dict[str, Any]) -> dict[str, Any]:
        tei_path = document.get("grobid_tei_path")
        if not tei_path:
            raise ValueError(f"Missing GROBID TEI for {document.get('paper_id')}")
        raw_path = raw_dir / f"{document['document_id']}.json"
        if raw_path.is_file():
            raw = read_json(raw_path)
        else:
            raw = client.annotate_tei(tei_path)
            write_json(raw_path, raw)
        direct_mentions = _softcite_mentions(
            raw.get("mentions") or [], aliases, role_rules, known_core
        )
        recovered_mentions = _recover_known_software(
            tei_path,
            direct_mentions,
            aliases,
            role_rules,
            client,
            known_core,
        )
        mentions = _merge_mentions([*direct_mentions, *recovered_mentions])
        for mention in mentions:
            mention["execution_context_confirmed"] = _execution_context_confirmed(
                mention
            )
        core = [item for item in mentions if item["role"] == "core" and item["used"]]
        auxiliary = [item for item in mentions if item["role"] == "auxiliary" and item["used"]]
        unclassified = [
            item for item in mentions if item["role"] == "unknown" and item["used"]
        ]
        ignored = [item for item in mentions if item["role"] == "ignore" or not item["used"]]

        for mention in core:
            mention["direct_support"] = _direct_support(mention["normalized_name"], toolbox_profile)
            mention["capability_equivalence"] = _capability_equivalence(
                mention, capability_rules, toolbox_profile
            )

        unsupported = [
            item
            for item in core
            if not item["direct_support"]["supported"] and not item["capability_equivalence"]
        ]
        equivalent = [
            item
            for item in core
            if not item["direct_support"]["supported"] and item["capability_equivalence"]
        ]
        if not core:
            decision = "software_not_identified"
            status = "reject"
            stop_reason = "no_core_software"
        elif unsupported:
            decision = "unsupported"
            status = "reject"
            stop_reason = "unsupported_core_software"
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
                "unclassified_software": unclassified,
                "ignored_mentions": ignored,
                "unsupported_core_software": [item["normalized_name"] for item in unsupported],
                "equivalent_core_software": [item["normalized_name"] for item in equivalent],
                "service_version": service_version,
                "softcite_raw_path": str(raw_path),
            },
            "pipeline_routing": {
                "stage_03": decision,
                "stage_04": "pending" if decision == "direct_covered" else "not_run",
                "continue": decision == "direct_covered",
                "stopped_at": None
                if decision == "direct_covered"
                else "stage_03_software_coverage",
                "stop_reason": stop_reason,
            },
        }
        return record

    def safe_assess(document: dict[str, Any]) -> dict[str, Any]:
        try:
            return assess(document)
        except Exception as exc:
            if not isolate_errors:
                raise
            return {
                **document,
                "software_coverage": {
                    "status": "error",
                    "decision": "stage_error",
                    "core_software": [],
                    "auxiliary_software": [],
                    "unclassified_software": [],
                    "ignored_mentions": [],
                    "service_version": service_version,
                    "error": f"{type(exc).__name__}: {exc}",
                },
                "pipeline_routing": {
                    "stage_03": "stage_error",
                    "continue": True,
                    "stopped_at": None,
                    "stop_reason": None,
                },
            }

    return ordered_parallel_map(
        safe_assess,
        documents,
        max_workers=workers,
        on_complete=lambda completed, total, _index, document, record: log_progress(
            "stage_03_software_coverage",
            completed,
            total,
            document.get("title") or document["paper_id"],
            status=(record.get("software_coverage") or {}).get("decision"),
        ),
    )


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
        "software_not_identified": decisions.get("software_not_identified", 0),
    }


def _softcite_mentions(
    raw_mentions: list[dict[str, Any]],
    aliases: dict[str, str],
    role_rules: dict[str, Any],
    known_core: set[str],
) -> list[dict[str, Any]]:
    output = []
    for raw in raw_mentions:
        name = raw.get("software-name") or {}
        raw_name = str(name.get("rawForm") or name.get("normalizedForm") or "").strip()
        if not raw_name:
            continue
        normalized = _normalize_software(raw_name, aliases)
        document_used = (raw.get("documentContextAttributes") or {}).get("used") or {}
        mention_used = (raw.get("mentionContextAttributes") or {}).get("used") or {}
        used_payload = document_used if "value" in document_used else mention_used
        used = bool(used_payload.get("value")) if "value" in used_payload else False
        evidence = str(raw.get("context") or "").strip()
        if _is_nonsoftware_alias_context(normalized, evidence):
            used = False
        output.append(
            {
                "raw_name": raw_name,
                "normalized_name": normalized,
                "version": ((raw.get("version") or {}).get("normalizedForm") or ""),
                "role": _software_role(
                    normalized, raw_name, role_rules, known_core
                ),
                "used": used,
                "used_score": used_payload.get("score"),
                "evidence": evidence,
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
    known_core: set[str],
) -> list[dict[str, Any]]:
    existing_names = {item["normalized_name"] for item in existing if item["used"]}
    candidates: dict[str, list[tuple[str, dict[str, Any]]]] = {}
    alias_patterns = sorted(aliases, key=len, reverse=True)
    for paragraph in read_tei_paragraphs(tei_path):
        for sentence in sentence_windows(paragraph):
            for alias_key in alias_patterns:
                normalized = aliases[alias_key]
                if normalized in existing_names:
                    continue
                if _contains_alias(sentence["text"], alias_key):
                    if _is_nonsoftware_alias_context(normalized, sentence["text"]):
                        continue
                    values = candidates.setdefault(normalized, [])
                    if not any(item[1]["text"] == sentence["text"] for item in values):
                        values.append((alias_key, sentence))
    output = []
    for normalized, contexts in candidates.items():
        classified = []
        for alias_key, sentence in contexts[:5]:
            result = client.characterize_context(
                _context_around_alias(sentence["text"], alias_key)
            )
            used_payload = (result.get("classification") or {}).get("used") or {}
            classified.append((alias_key, sentence, result, used_payload))
        alias_key, sentence, result, used_payload = max(
            classified,
            key=lambda item: (
                bool(item[3].get("value")) or _strong_software_use(item[1]["text"]),
                float(item[3].get("score") or 0),
            ),
        )
        used = bool(used_payload.get("value")) or _strong_software_use(sentence["text"])
        output.append(
            {
                "raw_name": alias_key,
                "normalized_name": normalized,
                "version": "",
                "role": _software_role(
                    normalized, alias_key, role_rules, known_core
                ),
                "used": used,
                "used_score": used_payload.get("score"),
                "evidence": sentence["text"],
                "section": sentence.get("section"),
                "paragraph_index": sentence.get("paragraph_index"),
                "source": "toolbox_lexicon_softcite_context",
                "softcite_context": result,
                "additional_evidence": [
                    item[1]["text"] for item in classified if item[1]["text"] != sentence["text"]
                ],
            }
        )
    return output


def _context_around_alias(text: str, alias: str, max_chars: int = 600) -> str:
    """Bound Softcite's GET query while retaining the software mention."""
    if len(text) <= max_chars:
        return text
    position = text.casefold().find(alias.casefold())
    if position < 0:
        return text[:max_chars]
    start = max(0, position - max_chars // 2)
    end = min(len(text), start + max_chars)
    start = max(0, end - max_chars)
    return text[start:end]


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
    key = _alias_key(value)
    if key in aliases:
        return aliases[key]
    key = _alias_key(re.sub(r"\b(?:version|ver\.?|v)\s*\d+(?:\.\d+)*\b", "", value, flags=re.I))
    if key in aliases:
        return aliases[key]
    versionless = re.sub(r"\s+\d+(?:\s+\d+)*$", "", key)
    if versionless in aliases:
        return aliases[versionless]
    return aliases.get(key, key.replace(" ", "_"))


def _software_role(
    normalized: str,
    raw_name: str,
    rules: dict[str, Any],
    known_core: set[str] | None = None,
) -> str:
    ignored = {_alias_key(item) for item in rules.get("ignore", [])}
    auxiliary = {_alias_key(item) for item in rules.get("auxiliary", [])}
    values = {_alias_key(normalized), _alias_key(raw_name)}
    if values & ignored:
        return "ignore"
    if values & auxiliary:
        return "auxiliary"
    explicit_core = {_alias_key(item) for item in rules.get("core", [])}
    normalized_core = {_alias_key(item) for item in (known_core or set())}
    if values & (explicit_core | normalized_core):
        return "core"
    return "unknown"


def _execution_context_confirmed(mention: dict[str, Any]) -> bool:
    normalized = str(mention.get("normalized_name") or "")
    contexts = [
        str(mention.get("evidence") or ""),
        *(str(item) for item in mention.get("additional_evidence") or []),
    ]
    for context in contexts:
        if _is_nonsoftware_alias_context(normalized, context):
            continue
        if re.search(
            r"\b(?:previous(?:ly)?|prior)\b.{0,100}"
            r"\b(?:calculation|simulation|software|program|package)\b",
            context,
            re.I,
        ):
            continue
        computational_action = re.search(
            r"\b(?:calculat(?:e|ed|es|ing|ion|ions)|comput(?:e|ed|es|ing|ation|ations)|"
            r"simulat(?:e|ed|es|ing|ion|ions)|optimi[sz](?:e|ed|es|ing|ation|ations)|"
            r"docking|dynamics|energy|energies|orbital|orbitals|force\s*field|"
            r"conformer|conformers|electronic\s+structure|density\s+functional|"
            r"molecular\s+mechanics|wavefunction|spectra|spectrum)\b",
            context,
            re.I,
        )
        execution = re.search(
            r"\b(?:perform(?:ed|ing)?|carried\s+out|conducted|used|using|employ(?:ed|ing)?|"
            r"utili[sz](?:ed|ing)?|implemented|run|ran|generated|produced|analysed|analyzed)\b",
            context,
            re.I,
        )
        if computational_action and execution:
            return True
    return False


def _direct_support(name: str, toolbox: dict[str, Any]) -> dict[str, Any]:
    unavailable = {str(item).casefold() for item in toolbox.get("unavailable", [])}
    backends = {str(item).casefold() for item in toolbox.get("backends", [])}
    identifiers = {str(item).casefold() for item in toolbox.get("available_identifiers", [])}
    normalized = name.casefold()
    supported = normalized in (identifiers | backends) and normalized not in unavailable
    if name in toolbox.get("scientific_smoke", []):
        level = "functional"
    elif name in toolbox.get("interface_smoke", []):
        level = "interface"
    elif name in toolbox.get("needs_complete_input", []):
        level = "needs_complete_input"
    else:
        level = "catalogued" if supported else "not_catalogued"
    if normalized in backends:
        support_kind = "backend"
    elif supported:
        support_kind = "runtime"
    else:
        support_kind = None
    return {
        "supported": supported,
        "identifier": name if supported else None,
        "support_kind": support_kind,
        "validation_level": level,
    }


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
    pattern = (
        r"(?<![A-Za-z0-9])" + re.escape(alias_key).replace(r"\ ", r"[\s_-]+") + r"(?![A-Za-z0-9])"
    )
    return re.search(pattern, _alias_key(text), re.I) is not None


def _strong_software_use(text: str) -> bool:
    return bool(
        re.search(
            r"\b(?:calculations?|simulations?|dynamics|workflows?|sampling|energies|structures?)\b"
            r".{0,100}\b(?:using|with|in|via|implemented|performed|carried out|run|used)\b"
            r"|\b(?:using|with|via|implemented in|performed with|carried out with|run with|used in)\b"
            r".{0,100}\b(?:calculations?|simulations?|dynamics|engine|package|program|software|plugin)\b",
            text,
            re.I,
        )
    )


def _is_nonsoftware_alias_context(normalized: str, text: str) -> bool:
    if normalized == "gaussian":
        software_context = re.search(
            r"\bGaussian\s*(?:0?9|16)\b|"
            r"\bGaussian\b.{0,30}\b(?:software|package|program|code|revision)\b|"
            r"\b(?:calculations?|optimizations?|frequenc(?:y|ies))\b.{0,100}"
            r"\b(?:using|with|in|via)\s+Gaussian\b",
            text,
            re.I,
        )
        return not bool(software_context)
    if normalized == "amber_pmemd":
        return bool(
            re.search(
                r"\b(?:AMBER|GAFF2?)\b.{0,40}\b(?:force\s*field|parameters?|charges?)\b",
                text,
                re.I,
            )
        )
    return False


def _alias_key(value: str) -> str:
    return re.sub(r"[^a-z0-9+]+", " ", str(value).casefold()).strip()
