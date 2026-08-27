from __future__ import annotations

from pathlib import Path
from typing import Any

from src.contracts import read_json
from src.stages.phase_gate import run as run_shared_phase_gate

MODES = {"autonomous_research", "paper_reproduction"}


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
    relative = str(receipt.get("artifact_path") or "")
    if relative != "outputs/audited_task":
        raise ValueError("approved artifact_path must be outputs/audited_task")
    root = workspace.resolve()
    artifact = (root / relative).resolve()
    artifact.relative_to(root)
    if not artifact.is_dir():
        raise FileNotFoundError(f"approved audit artifact is missing: {artifact}")
    review = read_json(artifact / "workflow_review.json")
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
