"""Shared process rubrics and policy for multiplicative dual-axis evaluation."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

DUAL_AXIS_POLICY_ID = "dual_axis_100.v1"
RESULTS_POLICY_ID = "dual_axis_100.scientific_results.v1"
OPEN_RESEARCH_POLICY_ID = "dual_axis_100.open_research.v1"

DUAL_AXIS_POLICY: dict[str, Any] = {
    "policy_id": DUAL_AXIS_POLICY_ID,
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


def process_rubric(
    *, reproduction: bool, scientific_results: bool = False, open_research: bool = False
) -> list[dict[str, Any]]:
    """Return an independent copy of the shared 100-point process rubric."""

    if scientific_results and open_research:
        raise ValueError("Select only one versioned scoring policy")
    rubric = deepcopy(
        _REPRODUCTION_PROCESS_RUBRIC if reproduction else _AUTONOMOUS_PROCESS_RUBRIC
    )
    if scientific_results:
        # Preserve IDs and weights; opt in only through the authored package.
        rubric[0]["description"] = (
            "Interprets the supplied route, required observables and scientific dependencies, and plans their computation."
            if reproduction else
            "Independently designs a chemically appropriate route and candidate comparisons to obtain the requested observables."
        )
        rubric[3]["description"] = (
            "Checks the required convergence, identities, state or stationary-point validity, numerical controls and comparisons using actual evidence."
        )
        rubric[-1]["description"] = (
            "Links computed claims to managed artifacts and reports reproducible identities, parameters, units and observed failures."
        )
    if open_research:
        descriptions = (
            [
                "Interprets the disclosed source protocol and its ambiguities within the scientific question; plans reproducible execution and appropriate validation.",
                "Preserves disclosed chemical identities, conditions and protocol definitions; justifies controlled substitutions and distinguishes them from faithful reproduction.",
                "Generates relevant evidence through managed execution, preserving identities, parameters and artifacts across stages; unrelated successful calls earn no endpoint credit.",
                "Checks scientific validity and uncertainty appropriate to the claims, diagnoses discrepancies with the paper, and distinguishes recomputation from author assertions.",
                "Responds appropriately to observed failures or inconclusive results and records controlled recovery; a successful run need not manufacture failures.",
                "Allocates resources and validation effort according to the reproduction objective and evidence; neither a larger job count nor gratuitous reruns earn credit.",
                "Provides an auditable protocol and artifact trail, separates source results from recomputation, and reports material deviations with reproducible evidence.",
            ] if reproduction else [
                "Independently frames a tractable investigation and develops testable hypotheses or models within the given question and source bounds; no prescribed hypothesis list or count is required.",
                "Selects scientifically appropriate representations, methods and tools, connecting their assumptions and information value to the question; valid alternative routes are accepted.",
                "Generates relevant evidence through managed execution and preserves identities, parameters and artifacts across stages; unrelated successful calls earn no endpoint credit.",
                "Designs and interprets evidence capable of distinguishing or falsifying the agent's claims, with proportionate validity checks and uncertainty; no reference experiment matrix is mandatory merely because the author used it.",
                "Uses observed results, failures and uncertainty to revise or retain the investigation rationally; actual traces support claimed adaptation, and a successful run need not manufacture failure or revision.",
                "Chooses useful investigations under the budget and stops or redirects when justified by evidence; do not reward hypothesis count, calculation count, verbosity or apparent novelty.",
                "Links claims and meaningful research decisions to actual artifacts and execution records; distinguish prior plans from retrospective interpretation without requesting private internal reasoning.",
            ]
        )
        for criterion, description in zip(rubric, descriptions):
            criterion["description"] = description
    return rubric


def dual_axis_policy(
    *, scientific_results: bool = False, open_research: bool = False
) -> dict[str, Any]:
    """Return an independent copy of the standard multiplicative policy."""

    if scientific_results and open_research:
        raise ValueError("Select only one versioned scoring policy")
    policy = deepcopy(DUAL_AXIS_POLICY)
    if scientific_results:
        policy.update(
            policy_id=RESULTS_POLICY_ID,
            enforce_evidence_score_consistency=True,
            generic_commentary_scored=False,
        )
    if open_research:
        policy.update(
            policy_id=OPEN_RESEARCH_POLICY_ID,
            enforce_evidence_score_consistency=True,
            generic_commentary_scored=False,
            author_agreement_required=False,
            reference_route_required_for_autonomous_research=False,
        )
    return policy
