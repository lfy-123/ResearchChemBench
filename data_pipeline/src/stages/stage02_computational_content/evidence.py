from __future__ import annotations

import json
import re
from collections import defaultdict
from typing import Any

_COMPUTATIONAL_METHOD_RE = re.compile(
    r"\b(?:density\s+functional\s+theor(?:y|etical)|DFT|TD[- ]?DFT|ab\s+initio|"
    r"quantum\s+chem(?:istry|ical)|electronic[- ]structure|Hartree[- ]Fock|"
    r"M[oø]ller[- ]Plesset|MP2|coupled[- ]cluster|CCSD(?:\(T\))?|CASSCF|CASPT2|"
    r"molecular\s+dynamics|MD\s+simulations?|Monte\s+Carlo|QM\s*/\s*MM|"
    r"first[- ]principles|atomistic\s+simulations?|force[- ]field|"
    r"free[- ]energy\s+(?:perturbation|calculation|profile)|umbrella\s+sampling|"
    r"metadynamics|nudged\s+elastic\s+band|\bNEB\b|transition[- ]state\s+search|"
    r"potential[- ]energy\s+surface|phonon\s+calculations?|molecular\s+docking|"
    r"kinetic\s+Monte\s+Carlo|master[- ]equation|microkinetic|"
    r"reaction\s+(?:path|dynamics)|geometry\s+optimi[sz]ation)\b",
    re.IGNORECASE,
)
_COMPUTATIONAL_ACTION_RE = re.compile(
    r"\b(?:we\s+)?(?:calculated|computed|simulated|optimi[sz]ed|modelled|modeled|"
    r"sampled|predicted|evaluated|performed|carried\s+out|investigated|obtained|"
    r"searched|propagated|minimi[sz]ed)\b|"
    r"\b(?:calculations?|simulations?)\s+(?:were|was|have\s+been)\s+"
    r"(?:performed|carried\s+out|conducted|run|executed)",
    re.IGNORECASE,
)
_COMPUTATIONAL_RESULT_RE = re.compile(
    r"\b(?:activation|reaction|binding|adsorption|free|Gibbs|relative|electronic)\s+"
    r"(?:energies?|barriers?|enthalp(?:y|ies))\b|"
    r"\b(?:transition\s+states?|optimi[sz]ed\s+(?:geometr(?:y|ies)|structures?)|"
    r"trajector(?:y|ies)|orbitals?|electron\s+density|charge\s+distribution|"
    r"rate\s+constants?|phonon\s+(?:modes?|spectra)|simulated\s+spectra|"
    r"potential[- ]energy\s+(?:surface|profile)|free[- ]energy\s+(?:surface|profile)|"
    r"computed\s+(?:values?|properties|results?)|calculated\s+(?:values?|properties|results?))\b",
    re.IGNORECASE,
)
_AUTHOR_COMPUTATION_RE = re.compile(
    r"\b(?:we|our|in\s+this\s+(?:work|study))\b.{0,160}\b"
    r"(?:calculat|simulat|comput|model|optimi[sz]|predict)|"
    r"\b(?:calculations?|simulations?)\s+(?:were|was)\s+(?:performed|carried\s+out)",
    re.IGNORECASE | re.DOTALL,
)
_LAB_RE = re.compile(
    r"\b(?:synthesi[sz](?:ed|ation)|fabricat(?:ed|ion)|prepared|purified|isolated|"
    r"measured|recorded|characteri[sz](?:ed|ation)|microscopy|spectroscopy|"
    r"diffraction|electrochem(?:istry|ical)|assay(?:ed|s)?|tested|irradiated|"
    r"crystallograph(?:y|ic)|NMR|XPS|XRD|SEM|TEM|cyclic\s+voltammetry)\b",
    re.IGNORECASE,
)
_AUTHOR_LAB_RE = re.compile(
    r"\bwe\s+(?:synthesi[sz]ed|prepared|fabricated|purified|isolated|grew|measured|"
    r"recorded|acquired|collected|characteri[sz]ed|tested|assayed|irradiated)\b|"
    r"\b(?:samples?|compounds?|materials?|spectra|images?|micrographs?|measurements?|"
    r"experiments?)\s+(?:were|was)\s+(?:prepared|synthesi[sz]ed|fabricated|purified|"
    r"isolated|measured|recorded|acquired|collected|characteri[sz]ed|tested|performed)",
    re.IGNORECASE,
)
_CONCLUSION_HEADING_RE = re.compile(
    r"^(?:conclusions?|summary(?:\s+and\s+outlook)?|discussion\s+and\s+conclusions?|"
    r"concluding\s+remarks?|outlook)$",
    re.IGNORECASE,
)
_REFERENCE_HEADING_RE = re.compile(
    r"^(?:references?|bibliography|literature\s+cited)$", re.IGNORECASE
)


def build_evidence_packet(
    *,
    paper_metadata: dict[str, Any],
    blocks: list[dict[str, Any]],
    config: dict[str, Any],
) -> dict[str, Any]:
    """Select a balanced paper-level packet without making a semantic decision."""

    usable = _mark_reference_blocks(blocks)
    scored = [
        {
            "block": block,
            "computation_score": _computation_score(block),
            "experiment_score": _experiment_score(block),
        }
        for block in usable
        if str(block.get("text") or "").strip() and not block.get("is_reference")
    ]
    computation_hits = [item for item in scored if item["computation_score"] > 0]
    experiment_hits = [item for item in scored if item["experiment_score"] > 0]
    substantive_hits = [item for item in computation_hits if item["computation_score"] >= 4]
    explicit_method_hits = [
        item
        for item in computation_hits
        if _COMPUTATIONAL_METHOD_RE.search(str(item["block"].get("text") or ""))
    ]
    computation_candidate = (
        bool(explicit_method_hits) or bool(substantive_hits) or len(computation_hits) >= 2
    )

    narrative = _narrative_blocks(usable)
    computational = _ranked_blocks(
        computation_hits,
        score_key="computation_score",
        limit=int(config.get("max_computational_excerpts", 8)),
    )
    experimental = _ranked_blocks(
        experiment_hits,
        score_key="experiment_score",
        limit=int(config.get("max_experimental_excerpts", 8)),
    )
    selected = _fit_budget(
        narrative=narrative,
        computational=computational,
        experimental=experimental,
        max_characters=int(config.get("max_prompt_characters", 28000)),
        excerpt_characters=int(config.get("excerpt_characters", 1400)),
    )
    valid_ids = list(
        dict.fromkeys(
            str(block.get("evidence_id") or "")
            for group in selected.values()
            for block in group
            if block.get("evidence_id")
        )
    )
    return {
        "paper_metadata": paper_metadata,
        "rule_screen": {
            "computation_candidate": computation_candidate,
            "explicit_method_blocks": len(explicit_method_hits),
            "substantive_computation_blocks": len(substantive_hits),
            "computation_signal_blocks": len(computation_hits),
            "experiment_signal_blocks": len(experiment_hits),
            "documents_seen": len(
                {
                    str(item["block"].get("document_id") or "")
                    for item in scored
                    if item["block"].get("document_id")
                }
            ),
        },
        "narrative_evidence": [
            _compact_block(block, config, mode="narrative") for block in selected["narrative"]
        ],
        "computational_evidence": [
            _compact_block(block, config, mode="computational")
            for block in selected["computational"]
        ],
        "experimental_evidence": [
            _compact_block(block, config, mode="experimental") for block in selected["experimental"]
        ],
        "valid_evidence_ids": valid_ids,
    }


def _computation_score(block: dict[str, Any]) -> int:
    text = str(block.get("text") or "")
    score = 0
    if _COMPUTATIONAL_METHOD_RE.search(text):
        score += 3
    if _COMPUTATIONAL_ACTION_RE.search(text):
        score += 2
    if _COMPUTATIONAL_RESULT_RE.search(text):
        score += 2
    if _AUTHOR_COMPUTATION_RE.search(text):
        score += 2
    return score


def _experiment_score(block: dict[str, Any]) -> int:
    text = str(block.get("text") or "")
    score = 2 if _LAB_RE.search(text) else 0
    if _AUTHOR_LAB_RE.search(text):
        score += 3
    return score


def _mark_reference_blocks(blocks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    order: list[str] = []
    for block in blocks:
        document_id = str(block.get("document_id") or "")
        if document_id not in grouped:
            order.append(document_id)
        grouped[document_id].append(dict(block))

    output: list[dict[str, Any]] = []
    for document_id in order:
        in_references = False
        for block in grouped[document_id]:
            text = " ".join(str(block.get("text") or "").split())
            section = " ".join(block.get("section_path") or []).casefold()
            if "reference" in section or "bibliograph" in section:
                in_references = True
            if len(text) <= 80 and _REFERENCE_HEADING_RE.fullmatch(text.rstrip(":")):
                in_references = True
            block["is_reference"] = in_references
            output.append(block)
    return output


def _narrative_blocks(blocks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    main = [
        block
        for block in blocks
        if block.get("document_role") == "main_paper" and not block.get("is_reference")
    ]
    if not main:
        main = [block for block in blocks if not block.get("is_reference")]
    selected: list[dict[str, Any]] = main[:3]
    for index, block in enumerate(main):
        text = " ".join(str(block.get("text") or "").split()).rstrip(":")
        if len(text) <= 100 and _CONCLUSION_HEADING_RE.fullmatch(text):
            selected.extend(main[index : index + 4])
    long_main = [block for block in main if len(str(block.get("text") or "").split()) >= 20]
    selected.extend(long_main[-2:])
    return _deduplicate_blocks(selected)[:10]


def _ranked_blocks(
    items: list[dict[str, Any]], *, score_key: str, limit: int
) -> list[dict[str, Any]]:
    ranked = sorted(
        enumerate(items),
        key=lambda pair: (-int(pair[1][score_key]), pair[0]),
    )
    selected: list[dict[str, Any]] = []
    seen_documents: set[str] = set()
    deferred: list[dict[str, Any]] = []
    for _index, item in ranked:
        block = item["block"]
        document_id = str(block.get("document_id") or "")
        if document_id and document_id not in seen_documents:
            selected.append(block)
            seen_documents.add(document_id)
        else:
            deferred.append(block)
    selected.extend(deferred)
    return _deduplicate_blocks(selected)[: max(1, limit)]


def _fit_budget(
    *,
    narrative: list[dict[str, Any]],
    computational: list[dict[str, Any]],
    experimental: list[dict[str, Any]],
    max_characters: int,
    excerpt_characters: int,
) -> dict[str, list[dict[str, Any]]]:
    groups = {
        "narrative": narrative,
        "computational": computational,
        "experimental": experimental,
    }
    output: dict[str, list[dict[str, Any]]] = {key: [] for key in groups}
    used = 0
    selected_ids: set[str] = set()
    # Interleave the three evidence types so a small budget cannot become one-sided.
    # Dedicated signal excerpts claim a duplicated block before generic narrative.
    for index in range(max((len(values) for values in groups.values()), default=0)):
        for key in ("computational", "experimental", "narrative"):
            values = groups[key]
            if index >= len(values):
                continue
            block = values[index]
            evidence_id = str(block.get("evidence_id") or "")
            if not evidence_id or evidence_id in selected_ids:
                continue
            compact = _compact_block(
                block,
                {"excerpt_characters": excerpt_characters},
                mode=key,
            )
            size = len(json.dumps(compact, ensure_ascii=False))
            if used + size > max(1000, max_characters):
                continue
            output[key].append(block)
            selected_ids.add(evidence_id)
            used += size
    return output


def _compact_block(block: dict[str, Any], config: dict[str, Any], *, mode: str) -> dict[str, Any]:
    limit = int(config.get("excerpt_characters", 1400))
    text = str(block.get("text") or "")
    return {
        "evidence_id": block.get("evidence_id"),
        "document_id": block.get("document_id"),
        "document_role": block.get("document_role"),
        "page": block.get("page"),
        "section_path": block.get("section_path") or [],
        "text": _focused_excerpt(text, max(200, limit), mode=mode),
    }


def _focused_excerpt(text: str, limit: int, *, mode: str) -> str:
    if len(text) <= limit or mode == "narrative":
        return text[:limit]
    patterns = {
        "computational": (
            _COMPUTATIONAL_METHOD_RE,
            _AUTHOR_COMPUTATION_RE,
            _COMPUTATIONAL_RESULT_RE,
            _COMPUTATIONAL_ACTION_RE,
        ),
        "experimental": (_AUTHOR_LAB_RE, _LAB_RE),
    }.get(mode, ())
    starts = [match.start() for pattern in patterns if (match := pattern.search(text))]
    if not starts:
        return text[:limit]
    center = min(starts)
    start = max(0, center - limit // 3)
    end = min(len(text), start + limit)
    start = max(0, end - limit)
    prefix = "..." if start else ""
    suffix = "..." if end < len(text) else ""
    return f"{prefix}{text[start:end]}{suffix}"


def _deduplicate_blocks(blocks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    output: list[dict[str, Any]] = []
    seen: set[str] = set()
    for block in blocks:
        evidence_id = str(block.get("evidence_id") or "")
        if not evidence_id or evidence_id in seen:
            continue
        seen.add(evidence_id)
        output.append(block)
    return output


__all__ = ["build_evidence_packet"]
