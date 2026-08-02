from __future__ import annotations

import re
from typing import Any

from src.core.models import task_types_for_record

MODE_PREFIX = {
    "autonomous_research": (
        "Using the provided starting information and the ResearchChemBench chemistry toolbox, "
        "design and execute a computational investigation that addresses: "
    ),
    "paper_reproduction": (
        "Follow the supplied methodological route, reconstruct the required inputs, and reproduce "
        "the computational evidence needed to address: "
    ),
    "conclusion_guided_reconstruction": (
        "Using the disclosed target conclusion and starting evidence, independently design and execute "
        "a computational verification that addresses: "
    ),
    "mechanistic_rule_discovery": (
        "Construct competing mechanistic hypotheses, choose calculations that discriminate among "
        "them, infer a cross-system rule, and test it on held-out systems for: "
    ),
}


def generate_task_candidates(record: dict[str, Any]) -> dict[str, dict[str, Any]]:
    overrides = record.get("mode_overrides") or {}
    base_problem = _concise_problem(record.get("central_problem", ""))
    output = {}
    for mode in task_types_for_record(record):
        override = overrides.get(mode) or {}
        question = override.get("central_problem")
        source = "curator_override" if question else "deterministic_template"
        if not question:
            question = MODE_PREFIX[mode] + base_problem
        output[mode] = {
            "question": question.strip(),
            "generation_source": source,
            "quality": assess_question_quality(question, mode, record),
        }
    return output


def assess_question_quality(
    question: str,
    mode: str,
    record: dict[str, Any],
) -> dict[str, Any]:
    lower = question.casefold()
    words = re.findall(r"[a-zA-Z0-9][a-zA-Z0-9+_.-]*", question)
    checks = {
        "bounded_length": 18 <= len(words) <= 180,
        "task_action": any(
            term in lower
            for term in (
                "determine",
                "investigate",
                "reproduce",
                "construct",
                "compare",
                "identify",
                "evaluate",
                "explain",
                "discover",
                "test",
            )
        ),
        "scientific_anchor": any(
            term in lower
            for term in (
                "reaction",
                "mechan",
                "energy",
                "structure",
                "molecular",
                "material",
                "property",
                "spectrum",
                "catal",
                "simulation",
                "computational",
                "chemical",
                "excited",
            )
        ),
        "not_abstract_dump": len(question) < 1400 and question.count(". ") <= 5,
        "no_source_identity": not _contains_source_identity(question, record),
        "no_exact_gold_number": not _contains_private_number(question, record),
    }
    if mode == "autonomous_research":
        checks["mode_alignment"] = "design" in lower or "investigat" in lower
    elif mode == "paper_reproduction":
        checks["mode_alignment"] = "reproduc" in lower or "reconstruct" in lower
    elif mode == "conclusion_guided_reconstruction":
        checks["mode_alignment"] = "verif" in lower or "evidence" in lower
    else:
        checks["mode_alignment"] = (
            "rule" in lower or "predict" in lower or "held-out" in lower
        ) and ("mechan" in lower or "evidence" in lower)
    score = round(100 * sum(checks.values()) / len(checks), 1)
    failed = [name for name, passed in checks.items() if not passed]
    decision = "pass" if score >= 85 else "review" if score >= 60 else "reject"
    return {"decision": decision, "score": score, "checks": checks, "failed_checks": failed}


def _concise_problem(value: str) -> str:
    normalized = re.sub(r"\s+", " ", value).strip()
    if not normalized:
        return "the scientific question represented by the supplied inputs"
    sentence = re.split(r"(?<=[.!?])\s+", normalized, maxsplit=1)[0]
    if len(sentence) > 600:
        sentence = sentence[:600].rsplit(" ", 1)[0]
    return sentence.rstrip(".") + "."


def _contains_source_identity(question: str, record: dict[str, Any]) -> bool:
    paper = record.get("paper") or {}
    title = paper.get("title") or ""
    normalized_title = re.sub(r"[^a-z0-9]+", " ", title.casefold()).strip()
    normalized_question = re.sub(r"[^a-z0-9]+", " ", question.casefold()).strip()
    return bool(
        normalized_title
        and len(normalized_title.split()) >= 5
        and normalized_title in normalized_question
    )


def _contains_private_number(question: str, record: dict[str, Any]) -> bool:
    question_numbers = set(re.findall(r"\b\d+(?:\.\d+)?\b", question))
    if not question_numbers:
        return False
    private_text = " ".join(
        item.get("statement", "")
        for item in record.get("evidence", [])
        if item.get("visibility") == "private"
    )
    private_text += " " + " ".join(map(str, record.get("reference_results", [])))
    private_numbers = set(re.findall(r"\b\d+(?:\.\d+)?\b", private_text))
    return bool(question_numbers & private_numbers)
