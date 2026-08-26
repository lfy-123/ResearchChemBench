#!/usr/bin/env python3
"""Build the public reproduction-file scaffold from workflow_review.json.

This helper supplies file syntax, the canonical paper ID, public-input copies,
and submission paths.  It deliberately does not create evaluator files: the
builder Agent must author those files from the paper and validate them with the
shared Gate.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


def dump(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def safe_path(value: object) -> str:
    text = str(value or "").replace("\\", "/").lstrip("/")
    parts = [part for part in text.split("/") if part not in {"", "."}]
    if any(part == ".." for part in parts):
        raise SystemExit("unsafe public input path")
    text = "/".join(parts)
    # The review may express an asset relative to the input root (``foo.xyz``)
    # or relative to the public task (``data/inputs/foo.xyz``).  This helper
    # writes below ``paper_reproduction/data/inputs`` and therefore must strip
    # transport prefixes before both materializing the file and projecting its
    # task_spec path. Iterate until the path is relative to the input root.
    prefixes = (
        "task/data/inputs/",
        "data/inputs/",
        "task/inputs/",
        "inputs/",
        "public_inputs/",
    )
    while True:
        stripped = next((text[len(prefix) :] for prefix in prefixes if text.startswith(prefix)), None)
        if stripped is None:
            break
        text = stripped
    return text or "input.dat"


def normalize_assets(value) -> list[dict]:
    """Accept list or keyed-map syntax without inventing missing asset data."""

    if isinstance(value, list):
        candidates = [(str(index), row) for index, row in enumerate(value, start=1)]
    elif isinstance(value, dict):
        if any(
            key in value
            for key in ("path", "content", "description", "role", "source_evidence_ids")
        ):
            candidates = [("asset-1", value)]
        else:
            candidates = [(str(key), row) for key, row in value.items()]
    else:
        return []

    assets: list[dict] = []
    for label, raw in candidates:
        if isinstance(raw, dict):
            asset = dict(raw)
        elif isinstance(raw, str) and raw.strip():
            asset = {"description": raw.strip()}
        else:
            continue
        asset.setdefault("asset_id", label)
        if not asset.get("path") and ("/" in label or Path(label).suffix):
            asset["path"] = label
        if asset.get("path"):
            assets.append(asset)
    return assets


def _mode_info(
    review: dict,
    scope: dict,
    complexity: dict,
    pair_id: str,
    *,
    mode: str,
    task_mode: str,
    disclosure: str,
) -> dict:
    public = review.get("public_task_basis") or {}
    question = str(
        review.get("public_scientific_question")
        or public.get("scientific_question")
        or review.get("scientific_question")
        or "Determine the paper-defined computational quantities."
    )
    return {
        "paper_id": pair_id,
        "task_id": pair_id,
        "source_id": str(review.get("source_id") or "paper_source"),
        "category": str(review.get("category") or "computational_chemistry"),
        "benchmark_family": str(review.get("task_direction") or ""),
        "mode": mode,
        "task_mode": task_mode,
        "scientific_mode": mode,
        "method_disclosure": disclosure,
        "pathway_disclosure": disclosure,
        "scientific_mode_description": question,
        "scientific_question": question,
        "scientific_requirements": [
            str(row.get("name") or row.get("description") or "")
            for row in public.get("boundary_conditions") or []
            if isinstance(row, dict) and str(row.get("name") or row.get("description") or "").strip()
        ],
        "required_deliverables": [
            {"path": "report/results.json", "description": "Structured scientific results.", "allow_empty": False},
            {"path": "report/report.md", "description": "Evidence-backed scientific report.", "allow_empty": False},
        ],
        "data": [
            {
                "name": "Public computational inputs",
                "path": "data/inputs",
                "type": "directory",
                "description": "Inputs disclosed by the source.",
            }
        ],
        "archive_extractions": [],
        "method_constraints": public.get("method_constraints")
        or public.get("public_method_constraints")
        or [],
    }


def _mode_spec(
    review: dict,
    scope: dict,
    complexity: dict,
    pair_id: str,
    *,
    mode: str,
    task_mode: str,
    disclosure: str,
) -> dict:
    public = review.get("public_task_basis") or {}
    assets = []
    for asset in normalize_assets(public.get("input_assets")):
        assets.append(
            {
                "path": "data/inputs/" + safe_path(asset.get("path")),
                "description": asset.get("description", "Public input"),
                "role": asset.get("role", "computational_input"),
                "source_evidence_ids": asset.get("source_evidence_ids") or [],
            }
        )
    question = str(
        review.get("public_scientific_question")
        or review.get("scientific_question")
        or "Determine the paper-defined computational quantities."
    )
    return {
        "paper_id": pair_id,
        "task_id": pair_id,
        "mode": mode,
        "task_mode": task_mode,
        "scientific_mode": mode,
        "method_disclosure": disclosure,
        "pathway_disclosure": disclosure,
        "scientific_question": question,
        "target_definition": question,
        "boundary_conditions": public.get("boundary_conditions") or [],
        "input_assets": assets,
        "method_constraints": public.get("method_constraints")
        or public.get("public_method_constraints")
        or [],
    }


def main() -> None:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "outputs").resolve()
    review_path = Path(sys.argv[2] if len(sys.argv) > 2 else root / "workflow_review.json").resolve()
    review = json.loads(review_path.read_text(encoding="utf-8"))
    if review.get("decision") != "candidate_ready":
        raise SystemExit("bootstrap requires workflow_review decision=candidate_ready")
    scope = review.get("workflow_scope") or {}
    complexity = review.get("complexity_profile") or {}
    pair_id = str(review.get("paper_id") or "paper")
    public = review.get("public_task_basis") or {}
    question = str(review.get("public_scientific_question") or review.get("scientific_question") or "Determine the paper-defined computational quantities.")
    reproduction = root / "paper_reproduction"
    (reproduction / "data" / "inputs").mkdir(parents=True, exist_ok=True)
    for asset in normalize_assets(public.get("input_assets")):
        if asset.get("content") is None:
            continue
        target = reproduction / "data" / "inputs" / safe_path(asset.get("path"))
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(str(asset["content"]), encoding="utf-8")
    task_text = str(
        public.get("task_instruction")
        or public.get("task_description")
        or review.get("public_task_instruction")
        or review.get("public_scientific_question")
        or review.get("scientific_question")
        or ""
    ).strip()
    dump(reproduction / "task_info.json", _mode_info(review, scope, complexity, pair_id, mode="paper_reproduction", task_mode="guided_reproduction", disclosure="paper_route_disclosed"))
    dump(reproduction / "task_spec.json", _mode_spec(review, scope, complexity, pair_id, mode="paper_reproduction", task_mode="guided_reproduction", disclosure="paper_route_disclosed"))
    dump(
        reproduction / "submission_contract.json",
        {
            "schema_version": "researchchembench.submission.v1",
            "paper_id": pair_id,
            "required_files": ["report/results.json", "report/report.md"],
            "submission_path": "report/results.json",
            "results_schema": {
                "type": "object",
                "description": "Structured report/results.json submitted by the evaluated agent.",
                "additionalProperties": True,
            },
            "allowed_extra_fields": True,
        },
    )
    dump(reproduction / "process_rubric.json", review.get("process_rubric") or [])
    (reproduction / "task.md").write_text(task_text + "\n", encoding="utf-8")
    (reproduction / "paper_route.md").write_text(json.dumps(review.get("paper_route") or {}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    dump(reproduction / "workflow_spec.json", {"steps": review.get("workflow_steps") or []})
    dump(reproduction / "route_evidence_map.json", review.get("evidence_map") or {})
    # These are deterministic handoff projections from the authored review.
    # Creating their files is transport scaffolding; the Agent remains
    # responsible for the scientific contents and may refine either object.
    dump(
        root / "workflow_completeness_check.json",
        review.get("workflow_completeness_check") or {},
    )
    dump(
        root / "public_to_private_asset_map.json",
        review.get("public_to_private_asset_map") or {},
    )
    dump(root / "toolbox_requirements.json", review.get("toolbox_requirements") or [])
    print("public reproduction scaffold created; author evaluator files and validate before receipt")


if __name__ == "__main__":
    main()
