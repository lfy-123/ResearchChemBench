"""Shared process rubrics and policy for multiplicative dual-axis evaluation."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

DUAL_AXIS_POLICY: dict[str, Any] = {
    "formula": "scientific_conclusion_score * research_process_score / 100",
    "scientific_conclusion_score_max": 100,
    "research_process_score_max": 100,
    "final_score_max": 100,
    "unsupported_claim_policy": (
        "A conclusion copied, guessed, or asserted without newly generated valid evidence "
        "receives no scientific-conclusion credit."
    ),
    "objective_failure_policy": (
        "A demonstrated benchmark input, framework, backend, or infrastructure failure may "
        "make the run not_scorable_objective; agent-selected invalid inputs or resource limits do not."
    ),
    "invalid_submission_policy": (
        "Fabricated evidence, hidden-answer leakage, or paper values presented as new calculations "
        "make the final score zero."
    ),
}


_AUTONOMOUS_PROCESS_RUBRIC: list[dict[str, Any]] = [
    {
        "id": "problem_framing_and_route_design",
        "max_score": 20,
        "description": "Independently defines hypotheses, alternatives, decision criteria, a staged route, budgets, and stopping rules without a disclosed paper method.",
    },
    {
        "id": "method_and_tool_selection",
        "max_score": 15,
        "description": "Selects chemically appropriate structures, software, methods, parameters, numerical controls, and fallback routes.",
    },
    {
        "id": "managed_execution_and_artifact_flow",
        "max_score": 15,
        "description": "Executes real managed scientific calculations and passes identities, structures, parameters, and artifacts correctly between stages.",
    },
    {
        "id": "validation_falsification_and_uncertainty",
        "max_score": 20,
        "description": "Tests convergence, numerical sensitivity, chemical validity, alternative explanations, evidence sufficiency, and uncertainty.",
    },
    {
        "id": "failure_diagnosis_and_adaptation",
        "max_score": 10,
        "description": "Diagnoses failed or inconclusive calls, avoids repeating preventable errors, and adapts without fabricating or laundering results.",
    },
    {
        "id": "resource_and_search_efficiency",
        "max_score": 10,
        "description": "Uses CPU, memory, parallelism, numerical resolution, search breadth, and stopping decisions efficiently without avoidable under-allocation or waste.",
    },
    {
        "id": "provenance_reporting_and_reproducibility",
        "max_score": 10,
        "description": "Links claims to managed artifacts and clearly reports assumptions, failed branches, deviations, units, uncertainty, and reproducible parameters.",
    },
]


_REPRODUCTION_PROCESS_RUBRIC: list[dict[str, Any]] = [
    {
        "id": "protocol_interpretation_and_execution_plan",
        "max_score": 20,
        "description": "Correctly interprets the supplied paper method and route, maps dependencies, budgets stages, and defines validation and stopping rules.",
    },
    {
        "id": "method_parameter_and_structure_fidelity",
        "max_score": 15,
        "description": "Uses the supplied identities, structures, methods, parameters, reference states, and controlled version-compatible substitutions faithfully.",
    },
    {
        "id": "managed_recomputation_and_artifact_flow",
        "max_score": 15,
        "description": "Recomputes the required evidence through managed scientific execution and passes artifacts correctly across the disclosed workflow.",
    },
    {
        "id": "validation_numerical_quality_and_uncertainty",
        "max_score": 20,
        "description": "Validates convergence, identities, stationary points or surfaces, numerical resolution, statistics, uncertainty, and paper-comparison tolerances.",
    },
    {
        "id": "failure_diagnosis_and_protocol_recovery",
        "max_score": 10,
        "description": "Diagnoses failures, makes scientifically controlled recovery choices, and records any unavoidable protocol deviation.",
    },
    {
        "id": "resource_and_execution_efficiency",
        "max_score": 10,
        "description": "Uses available resources, parallelism, retries, numerical settings, and stopping decisions efficiently while preserving protocol validity.",
    },
    {
        "id": "provenance_reporting_and_reproducibility",
        "max_score": 10,
        "description": "Separates paper targets from recomputation and links conclusions, parameters, deviations, failures, and uncertainty to artifacts.",
    },
]


def process_rubric(*, reproduction: bool) -> list[dict[str, Any]]:
    """Return an independent copy of the shared 100-point process rubric."""

    return deepcopy(
        _REPRODUCTION_PROCESS_RUBRIC if reproduction else _AUTONOMOUS_PROCESS_RUBRIC
    )


def dual_axis_policy() -> dict[str, Any]:
    """Return an independent copy of the standard multiplicative policy."""

    return deepcopy(DUAL_AXIS_POLICY)
