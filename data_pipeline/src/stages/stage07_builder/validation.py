from __future__ import annotations

from typing import Any


def validate_builder_candidate(
    response: dict[str, Any],
    *,
    assets: list[dict[str, Any]],
    document: dict[str, Any],
    toolbox: dict[str, Any],
) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    if response.get("decision") != "candidate":
        return {"passed": False, "errors": ["builder did not produce a candidate"], "warnings": []}
    task = response.get("task") or {}
    asset_ids = {str(item.get("asset_id")) for item in assets}
    public_ids = [str(item) for item in task.get("public_asset_ids", [])]
    missing_assets = sorted(set(public_ids) - asset_ids)
    if missing_assets:
        errors.append(f"unknown public asset IDs: {', '.join(missing_assets)}")
    if len(public_ids) != len(set(public_ids)):
        errors.append("public_asset_ids contains duplicates")
    rubric = response.get("scoring_rubric") or []
    points = sum(float(item.get("points") or 0) for item in rubric)
    if abs(points - 100.0) > 1e-6:
        errors.append(f"scoring rubric totals {points}, expected 100")
    evidenced_software = {
        str(item.get("normalized_name"))
        for item in (document.get("preliminary_coverage") or {}).get("core_software", [])
        if item.get("normalized_name")
    }
    for item in (document.get("supplementary_extraction") or {}).get("software_evidence", []):
        if item.get("matched_text"):
            evidenced_software.add(str(item["matched_text"]).casefold().replace(" ", "_"))
    requested_software = {str(item) for item in task.get("allowed_software", [])}
    available_software = set(toolbox.get("available_identifiers", [])) | set(
        toolbox.get("backends", [])
    )
    unsupported_software = sorted(requested_software - available_software)
    if unsupported_software:
        errors.append(
            f"software not present in frozen toolbox catalog: {', '.join(unsupported_software)}"
        )
    if requested_software and evidenced_software and not requested_software & evidenced_software:
        warnings.append("selected toolbox backend is an equivalent rather than paper-named software")
    available_actions = set(toolbox.get("actions", []))
    unknown_actions = sorted(set(task.get("allowed_actions", [])) - available_actions)
    if unknown_actions:
        errors.append(f"unknown toolbox actions: {', '.join(unknown_actions)}")
    evidence = response.get("evidence_map") or []
    evidence_assets = {str(item.get("asset_id")) for item in evidence}
    unknown_evidence = sorted(evidence_assets - asset_ids)
    if unknown_evidence:
        errors.append(f"evidence references unknown assets: {', '.join(unknown_evidence)}")
    if not evidence:
        errors.append("evidence_map is empty")
    evidence_text = " ".join(
        f"{item.get('claim', '')} {item.get('evidence', '')} {item.get('location', '')}"
        for item in evidence
    ).casefold()
    if not any(marker in evidence_text for marker in ("figure", "table", "claim", "conclusion")):
        errors.append("evidence_map does not identify a paper claim, figure, or table")
    construction_text = " ".join(
        [
            *map(str, task.get("instructions", [])),
            *map(str, task.get("expected_deliverables", [])),
            *(f"{item.get('criterion', '')} {item.get('method', '')}" for item in rubric),
        ]
    ).casefold()
    if any(
        marker in construction_text
        for marker in ("not constructed", "placeholder", "no grading applies")
    ):
        errors.append("candidate contains abstention or placeholder task content")
    if any(
        marker in construction_text
        for marker in ("read the existing output", "extract the reported", "redraw", "replot")
    ):
        errors.append("candidate is a trivial read/extract/plot task without a computation")
    public_text = " ".join(
        [str(task.get("objective") or ""), *map(str, task.get("instructions", []))]
    ).casefold()
    for result in (response.get("hidden_reference") or {}).get("expected_results", []):
        normalized = " ".join(str(result).casefold().split())
        if len(normalized) >= 20 and normalized in public_text:
            errors.append("public task text contains a hidden expected result")
            break
    if not task.get("allowed_actions"):
        errors.append("no toolbox action selected for the computation")
    return {"passed": not errors, "errors": errors, "warnings": warnings}
