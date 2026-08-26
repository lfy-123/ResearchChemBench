"""Adapt the five authored evaluator files to the benchmark scoring runtime."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from ..repository import load_private_reference, load_submission_schema, load_task_package
from ..schemas.task import GroundTruth
from .dual_axis import DUAL_AXIS_POLICY_ID, dual_axis_policy, process_rubric


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
    rules_by_reference: dict[str, list[dict[str, Any]]] = {}
    for rule in rules:
        rules_by_reference.setdefault(str(rule["reference_id"]), []).append(rule)
    conclusion_rubric: list[dict[str, Any]] = []
    for conclusion, maximum in zip(conclusions, _weights(len(conclusions))):
        conclusion_id = str(conclusion["conclusion_id"])
        authored_rules = rules_by_reference.get(conclusion_id, [])
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
        "scoring_rubric": process_rubric(reproduction=task_type == "paper_reproduction"),
        "scientific_conclusion_rubric": conclusion_rubric,
        "dual_axis_scoring_policy": dual_axis_policy(),
        "critical_failures": failures,
        "judge_instructions": (
            "Apply the task-authored scoring rules to submitted artifacts, then score the "
            "research process independently."
        ),
        "reference_evidence": reference,
    }
    return GroundTruth.model_validate(runtime).model_dump(mode="json")


def load_runtime_evaluation(*, paper_id: str, task_type: str) -> RuntimeEvaluation:
    package = load_task_package(paper_id=paper_id, task_type=task_type)
    reference = load_private_reference(
        paper_id=paper_id, task_type=task_type, evaluator_context=True
    )
    submission = load_submission_schema(paper_id=paper_id, task_type=task_type)
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
        adapter_id="split-computational-evaluator.v1",
        policy_id=DUAL_AXIS_POLICY_ID,
        task_type=task_type,
        package_content_sha256=package.package_content_sha256,
    )


__all__ = [
    "EvaluatorAdapterError",
    "EvaluatorReferenceInvalid",
    "RuntimeEvaluation",
    "load_runtime_evaluation",
]
