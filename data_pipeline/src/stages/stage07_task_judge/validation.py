from __future__ import annotations

from pathlib import Path
from typing import Any

from src.contracts import read_json
from src.stages.phase_gate import run as run_shared_phase_gate

MODES = {"autonomous_research", "paper_reproduction"}
AUDIT_DIMENSIONS = (
    "objective",
    "inputs",
    "instruction_completeness",
    "process_keypoints",
    "final_conclusions",
    "mode_separation",
    "answer_inversion",
    "evaluator_quality",
)


APPROVED_AUDIT_DECISIONS = {"approved", "approved_with_repairs"}


def validate_audit_receipt(
    receipt: dict[str, Any], *, paper_id: str, workspace: Path
) -> Path | None:
    """Validate the Agent decision and resolve its approved snapshot without mutation."""

    decision = str(receipt.get("audit_decision") or "")
    if decision not in {
        "approved",
        "approved_with_repairs",
        "rejected_scientific_unrepairable",
        "technical_blocked",
    }:
        raise ValueError(f"unsupported audit_decision: {decision!r}")
    if receipt.get("paper_id") != paper_id:
        raise ValueError("audit receipt paper_id mismatch")
    modes = receipt.get("release_modes")
    if decision in APPROVED_AUDIT_DECISIONS and (
        not isinstance(modes, list) or not modes or any(
            not isinstance(mode, str) or mode not in MODES for mode in modes
        ) or len(modes) != len(set(modes))
    ):
        raise ValueError("approved audit must declare one or more valid release_modes")
    if decision not in APPROVED_AUDIT_DECISIONS:
        return None
    if receipt.get("selected_workflow_preserved") is not True:
        raise ValueError("approved audit did not preserve the selected workflow")
    if receipt.get("remaining_issues"):
        raise ValueError("approved audit contains remaining issues")
    scientific_audit = receipt.get("scientific_audit")
    if not isinstance(scientific_audit, dict):
        raise ValueError("audit receipt scientific_audit must be an object")
    missing = [name for name in AUDIT_DIMENSIONS if not isinstance(scientific_audit.get(name), dict)]
    if missing:
        raise ValueError(f"audit receipt missing scientific audit dimensions: {', '.join(missing)}")
    unresolved = [
        name for name in AUDIT_DIMENSIONS
        if scientific_audit[name].get("status") not in {"passed", "repaired"}
    ]
    if unresolved:
        raise ValueError(
            "approved audit has unresolved scientific findings: " + ", ".join(unresolved)
        )
    for name in AUDIT_DIMENSIONS:
        item = scientific_audit[name]
        if not isinstance(item.get("finding"), str) or not item["finding"].strip():
            raise ValueError(f"audit receipt finding missing: {name}")
        if not isinstance(item.get("evidence"), list) or not item["evidence"]:
            raise ValueError(f"audit receipt evidence missing: {name}")
    relative = str(receipt.get("artifact_path") or "")
    if relative != "outputs/audited_task":
        raise ValueError("approved artifact_path must be outputs/audited_task")
    root = workspace.resolve()
    artifact = (root / relative).resolve()
    artifact.relative_to(root)
    if not artifact.is_dir():
        raise FileNotFoundError(f"approved audit artifact is missing: {artifact}")
    review = read_json(artifact / "workflow_review.json")
    if review.get("decision") != "candidate_ready":
        raise ValueError(
            "approved audit must preserve workflow_review decision candidate_ready"
        )
    review_modes = list((review.get("feasibility") or {}).get("release_modes") or [])
    if modes != review_modes:
        raise ValueError("audit receipt release_modes do not match audited workflow review")
    return artifact


def external_audit_gate(pair_root: Path) -> dict[str, Any]:
    """Run the exact same contract implementation used by the Agent self-check."""

    return run_shared_phase_gate("audit", pair_root)


__all__ = [
    "APPROVED_AUDIT_DECISIONS",
    "external_audit_gate",
    "validate_audit_receipt",
]
