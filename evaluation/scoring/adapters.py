"""Adapt the five authored evaluator files to the benchmark scoring runtime."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from ..repository import load_private_reference, load_submission_schema, load_task_package
from ..schemas.task import GroundTruth
from .dual_axis import (
    DUAL_AXIS_POLICY_ID, RESULTS_POLICY_ID, OPEN_RESEARCH_POLICY_ID,
    dual_axis_policy, process_rubric,
)
from .rules import associate_rules
from ..contracts.scientific_rubric import scientific_rubric


class EvaluatorAdapterError(RuntimeError):
    pass


class EvaluatorReferenceInvalid(EvaluatorAdapterError):
    pass


@dataclass(frozen=True)
class RuntimeEvaluation:
    ground_truth: dict[str, Any]
    adapter_id: str
    policy_id: str
    task_type: str
    package_content_sha256: str


def _weights(count: int) -> list[int]:
    if count < 1:
        raise EvaluatorReferenceInvalid("reference conclusions must not be empty")
    quotient, remainder = divmod(100, count)
    return [quotient + (index < remainder) for index in range(count)]


def _text(value: Any) -> str:
    return value.strip() if isinstance(value, str) else json.dumps(value, ensure_ascii=False)


def _runtime_contract(
    *, task_type: str, reference: dict[str, dict[str, Any]], submission: dict[str, Any]
) -> dict[str, Any]:
    conclusions = reference["reference_conclusions.json"]["items"]
    rules = reference["scoring_rules.json"]["rules"]
    authored_policy = reference["scoring_rules.json"].get("scoring_policy")
    if authored_policy not in (None, DUAL_AXIS_POLICY_ID, RESULTS_POLICY_ID, OPEN_RESEARCH_POLICY_ID):
        raise EvaluatorReferenceInvalid(f"unknown authored scoring_policy:{authored_policy}")
    scientific_results = authored_policy == RESULTS_POLICY_ID
    open_research = authored_policy == OPEN_RESEARCH_POLICY_ID
    rule_table = associate_rules(reference)
    conclusion_rubric: list[dict[str, Any]] = []
    for conclusion, maximum in zip(conclusions, _weights(len(conclusions))):
        conclusion_id = str(conclusion["conclusion_id"])
        authored_rules = [entry["rule"] for entry in rule_table if conclusion_id in entry["conclusion_ids"]]
        evidence = list(
            dict.fromkeys(
                path
                for rule in authored_rules
                for path in rule.get("binding", {}).get("artifact_paths", [])
            )
        )
        conclusion_rubric.append(
            {
                "id": conclusion_id,
                "max_score": maximum,
                "statement": _text(conclusion["statement"]),
                "acceptance_rule": json.dumps(authored_rules, ensure_ascii=False),
                "required_evidence": evidence or submission["required_files"],
            }
        )
    failures = [
        _text(item.get("description") or item.get("condition") or item)
        if isinstance(item, dict)
        else _text(item)
        for item in reference["critical_failures.json"]["items"]
    ]
    authored_rubric = scientific_rubric(reference["scoring_rules.json"])
    if authored_rubric is not None:
        conclusion_rubric = [{"id": item["id"], "max_score": item["max_score"], "statement": item["description"],
                             "acceptance_rule": json.dumps({"rule_ids": item["rule_ids"]}), "rule_ids": item["rule_ids"],
                             "required_evidence": submission["required_files"]} for item in authored_rubric]
    runtime = {
        "expected_tool_calls": [],
        "expected_result": {
            "key_points": reference["reference_key_points.json"]["items"],
            "conclusions": conclusions,
            "scoring_rules": rules,
        },
        "expected_structured_output": submission["required_files"],
        "evaluation_mode": "dual_axis_100",
        "evaluation_profile": (
            "paper_reproduction" if task_type == "paper_reproduction" else "autonomous_discovery"
        ),
        "score_max": 100,
        "scoring_rubric": process_rubric(
            reproduction=task_type == "paper_reproduction", scientific_results=scientific_results,
            open_research=open_research,
        ),
        "scientific_conclusion_rubric": conclusion_rubric,
        "dual_axis_scoring_policy": dual_axis_policy(
            scientific_results=scientific_results, open_research=open_research
        ),
        "critical_failures": failures,
        "judge_instructions": (
            "Apply the task-authored scoring rules to submitted artifacts, then score the "
            "research process independently."
        ),
        "reference_evidence": reference,
        "rule_table": rule_table,
    }
    return GroundTruth.model_validate(runtime).model_dump(mode="json")


def load_runtime_evaluation(*, paper_id: str, task_type: str, repository=None) -> RuntimeEvaluation:
    package = load_task_package(paper_id=paper_id, task_type=task_type, repository=repository)
    reference = load_private_reference(
        paper_id=paper_id, task_type=task_type, evaluator_context=True, repository=repository
    )
    submission = load_submission_schema(paper_id=paper_id, task_type=task_type, repository=repository)
    try:
        ground_truth = _runtime_contract(
            task_type=task_type, reference=reference, submission=submission
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise EvaluatorReferenceInvalid(
            f"evaluator files cannot be adapted: {type(exc).__name__}: {exc}"
        ) from exc
    return RuntimeEvaluation(
        ground_truth=ground_truth,
        adapter_id="split-computational-evaluator.v3-flat" if reference["scoring_rules.json"].get("scientific_rubric") else "split-computational-evaluator.v2",
        policy_id=ground_truth["dual_axis_scoring_policy"]["policy_id"],
        task_type=task_type,
        package_content_sha256=package.package_content_sha256,
    )


__all__ = [
    "EvaluatorAdapterError",
    "EvaluatorReferenceInvalid",
    "RuntimeEvaluation",
    "load_runtime_evaluation",
]
