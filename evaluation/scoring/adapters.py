"""Versioned adapters from task scientific references to runtime scoring policy.

The data producer owns scientific answers, acceptance contracts, process key
points, and conclusions.  This module owns benchmark-only policy: evaluator
selection, weights, the shared process rubric, and the dual-axis formula.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any, Protocol

from researchchembench_contracts import (
    COMPUTATIONAL_REFERENCE_SCHEMA_V1,
    ComputationalScienceReferenceV1,
)

from ..repository import (
    TaskPackage,
    load_private_reference,
    load_submission_schema,
    load_task_package,
)
from ..schemas.task import GroundTruth
from .dual_axis import DUAL_AXIS_POLICY_ID, dual_axis_policy, process_rubric


class EvaluatorAdapterError(RuntimeError):
    """Base class for explicit evaluator-adapter failures."""


class EvaluatorAdapterUnavailable(EvaluatorAdapterError):
    """Raised when no evaluator is registered for a task/reference pair."""


class EvaluatorReferenceInvalid(EvaluatorAdapterError):
    """Raised when a registered adapter cannot build a valid runtime contract."""


@dataclass(frozen=True)
class RuntimeEvaluation:
    ground_truth: dict[str, Any]
    adapter_id: str
    policy_id: str
    task_type: str
    reference_schema: str
    package_content_sha256: str
    package_format: str


class EvaluatorAdapter(Protocol):
    adapter_id: str
    policy_id: str

    def adapt(
        self,
        *,
        package: TaskPackage,
        reference: dict[str, Any],
        submission_schema: dict[str, Any],
    ) -> dict[str, Any]: ...


def _weights(count: int) -> list[int]:
    if count <= 0:
        raise EvaluatorReferenceInvalid("final_conclusions must not be empty")
    quotient, remainder = divmod(100, count)
    return [quotient + (1 if index < remainder else 0) for index in range(count)]


def _text(value: Any) -> str:
    if isinstance(value, str):
        return value.strip()
    return json.dumps(value, ensure_ascii=False, sort_keys=True)


class ComputationalScienceDualAxisAdapter:
    adapter_id = "computational-science-dual-axis.v1"
    policy_id = DUAL_AXIS_POLICY_ID

    def __init__(self, *, reproduction: bool):
        self.reproduction = reproduction

    def adapt(
        self,
        *,
        package: TaskPackage,
        reference: dict[str, Any],
        submission_schema: dict[str, Any],
    ) -> dict[str, Any]:
        try:
            value = ComputationalScienceReferenceV1.model_validate(reference)
        except Exception as exc:
            raise EvaluatorReferenceInvalid(
                f"computational reference is invalid: {type(exc).__name__}: {exc}"
            ) from exc
        expected_type = (
            "paper_reproduction" if self.reproduction else "autonomous_research"
        )
        if package.task_type != expected_type or value.task_type != expected_type:
            raise EvaluatorReferenceInvalid(
                f"adapter/task type mismatch: expected {expected_type}, received "
                f"{package.task_type}/{value.task_type}"
            )

        answers = {item.answer_id: item for item in value.answer_items}
        profiles = {
            item.acceptance_profile_id: item for item in value.acceptance_profiles
        }
        bindings = {
            item.acceptance_profile_id: item for item in value.submission_bindings
        }
        conclusion_weights = _weights(len(value.final_conclusions))
        conclusion_rubric: list[dict[str, Any]] = []
        for conclusion, maximum in zip(value.final_conclusions, conclusion_weights):
            typed_contract = {
                "answers": [
                    answers[answer_id].model_dump(mode="json")
                    for answer_id in conclusion.answer_ids
                ],
                "acceptance_profiles": [
                    profiles[profile_id].model_dump(mode="json")
                    for profile_id in conclusion.acceptance_profile_ids
                ],
                "submission_bindings": [
                    bindings[profile_id].model_dump(mode="json")
                    for profile_id in conclusion.acceptance_profile_ids
                ],
            }
            authored_rule = _text(conclusion.metadata.get("acceptance_rule", ""))
            rule = (
                (authored_rule + " ") if authored_rule else ""
            ) + "Apply the following typed answer/profile/binding contract: " + json.dumps(
                typed_contract, ensure_ascii=False, sort_keys=True
            )
            evidence = list(dict.fromkeys(conclusion.required_evidence))
            for profile_id in conclusion.acceptance_profile_ids:
                evidence.extend(
                    path
                    for path in bindings[profile_id].artifact_paths
                    if path not in evidence
                )
            if not evidence:
                evidence = ["Agent report and declared result artifacts"]
            conclusion_rubric.append(
                {
                    "id": conclusion.conclusion_id,
                    "max_score": maximum,
                    "statement": _text(conclusion.statement)
                    or f"Evaluate conclusion {conclusion.conclusion_id}.",
                    "acceptance_rule": rule,
                    "required_evidence": evidence,
                }
            )

        constraints = value.evaluation_constraints
        task_key_points = [
            item.model_dump(mode="json") for item in value.process_key_points
        ]
        expected_result = {
            "answer_items": [item.model_dump(mode="json") for item in value.answer_items],
            "acceptance_profiles": [
                item.model_dump(mode="json") for item in value.acceptance_profiles
            ],
            "submission_bindings": [
                item.model_dump(mode="json") for item in value.submission_bindings
            ],
            "final_conclusions": [
                item.model_dump(mode="json") for item in value.final_conclusions
            ],
        }
        runtime = {
            "expected_tool_calls": [],
            "expected_result": expected_result,
            "expected_structured_output": submission_schema.get("required_files", []),
            "evaluation_mode": "dual_axis_100",
            "evaluation_profile": (
                "paper_reproduction" if self.reproduction else "autonomous_discovery"
            ),
            "score_max": 100,
            "scoring_rubric": process_rubric(reproduction=self.reproduction),
            "scientific_conclusion_rubric": conclusion_rubric,
            "dual_axis_scoring_policy": dual_axis_policy(),
            "critical_failures": value.critical_failures,
            "judge_instructions": (
                "Score the task-authored conclusions from newly generated evidence and score "
                "research process independently. Treat task-specific process Key Points as an "
                "evidence checklist, not an additional weighted rubric."
            ),
            "reference_evidence": {
                "task_specific_process_key_points": task_key_points,
                "private_evidence": value.private_evidence,
                "submission_schema": submission_schema,
            },
            "managed_computation_policy": constraints.get(
                "managed_computation_policy", {"required": True}
            ),
            "evidence_gate_policy": constraints.get("evidence_gate_policy", {}),
            "reference_conclusion_gate_policy": constraints.get(
                "reference_conclusion_gate_policy", {}
            ),
            "current_toolbox_feasibility_baseline": {},
            "current_toolbox_reproduction_baseline": {},
        }
        try:
            validated = GroundTruth.model_validate(runtime).model_dump(mode="json")
        except Exception as exc:
            raise EvaluatorReferenceInvalid(
                f"runtime dual-axis contract is invalid: {type(exc).__name__}: {exc}"
            ) from exc
        return validated


_ADAPTERS: dict[tuple[str, str], EvaluatorAdapter] = {
    (
        "paper_reproduction",
        COMPUTATIONAL_REFERENCE_SCHEMA_V1,
    ): ComputationalScienceDualAxisAdapter(reproduction=True),
    (
        "autonomous_research",
        COMPUTATIONAL_REFERENCE_SCHEMA_V1,
    ): ComputationalScienceDualAxisAdapter(reproduction=False),
}


def evaluator_adapter_available(task_type: str, reference_schema: str) -> bool:
    return (task_type, reference_schema) in _ADAPTERS


def resolve_evaluator_adapter(
    task_type: str, reference_schema: str
) -> EvaluatorAdapter:
    try:
        return _ADAPTERS[(task_type, reference_schema)]
    except KeyError as exc:
        raise EvaluatorAdapterUnavailable(
            f"No evaluator adapter registered for {task_type} + {reference_schema}"
        ) from exc


def load_runtime_evaluation(task_id: str) -> RuntimeEvaluation:
    package = load_task_package(task_id)
    if not package.is_v1:
        reference = load_private_reference(task_id, evaluator_context=True)
        return RuntimeEvaluation(
            ground_truth=reference,
            adapter_id="legacy-ground-truth-adapter.v1",
            policy_id=str(
                reference.get("dual_axis_scoring_policy", {}).get("policy_id") or "legacy"
            ),
            task_type=package.task_type,
            reference_schema=package.reference_schema,
            package_content_sha256="",
            package_format=package.package_format,
        )
    adapter = resolve_evaluator_adapter(package.task_type, package.reference_schema)
    reference = load_private_reference(task_id, evaluator_context=True)
    submission = load_submission_schema(task_id)
    ground_truth = adapter.adapt(
        package=package,
        reference=reference,
        submission_schema=submission,
    )
    return RuntimeEvaluation(
        ground_truth=ground_truth,
        adapter_id=adapter.adapter_id,
        policy_id=adapter.policy_id,
        task_type=package.task_type,
        reference_schema=package.reference_schema,
        package_content_sha256=package.package_content_sha256,
        package_format=package.package_format,
    )


__all__ = [
    "ComputationalScienceDualAxisAdapter",
    "EvaluatorAdapterError",
    "EvaluatorAdapterUnavailable",
    "EvaluatorReferenceInvalid",
    "RuntimeEvaluation",
    "evaluator_adapter_available",
    "load_runtime_evaluation",
    "resolve_evaluator_adapter",
]
