#!/usr/bin/env python3
"""Build a deterministic Stage06 task-pair scaffold from workflow_review.json.

The scaffold supplies syntax, IDs, mode invariants, public-input copies, and
typed Ground Truth bindings. It never invents scientific inputs or answers.
The builder Agent must replace the marked prose and run the validators before
writing construction_receipt.json.
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
    return "/".join(parts) or "input.dat"


def evidence_ids(value) -> list[str]:
    if isinstance(value, dict):
        result: list[str] = []
        for key, row in value.items():
            if isinstance(row, dict):
                nested = row.get("evidence_ids") or row.get("evidence_id") or [key]
                result.extend(nested if isinstance(nested, list) else [nested])
        return [str(item) for item in result if str(item)]
    return [str(item) for item in (value or []) if str(item)]


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


def normalize_truths(review: dict) -> list[dict]:
    result: list[dict] = []
    for index, raw in enumerate(review.get("ground_truth_items") or [], start=1):
        if not isinstance(raw, dict):
            continue
        identifier = str(raw.get("ground_truth_id") or raw.get("item_id") or f"gt-{index}")
        kind = str(raw.get("kind") or raw.get("type") or "textual_intermediate_conclusion")
        kind = {
            "numerical_value": "numeric_final_result",
            "numeric_value": "numeric_final_result",
            "conclusion": "textual_final_conclusion",
            "intermediate_conclusion": "textual_intermediate_conclusion",
        }.get(kind, kind)
        answer = raw.get("canonical_answer", raw.get("value"))
        propositions = raw.get("required_propositions") or []
        if not propositions and isinstance(answer, str) and kind.startswith("textual_"):
            propositions = [answer]
        acceptance_type = raw.get("acceptance_type") or {
            "numeric_final_result": "numeric_tolerance",
            "numeric_intermediate_result": "numeric_tolerance",
            "trend": "trend",
            "ranking": "ranking",
            "textual_final_conclusion": "semantic_propositions",
            "textual_intermediate_conclusion": "semantic_propositions",
        }.get(kind, "semantic_propositions")
        result.append(
            {
                "ground_truth_id": identifier,
                "kind": kind,
                "canonical_answer": answer,
                "required_propositions": propositions,
                "forbidden_contradictions": raw.get("forbidden_contradictions") or [],
                "acceptance_type": acceptance_type,
                "acceptance_parameters": raw.get("acceptance_parameters") or {},
                "acceptance_profile_id": str(raw.get("acceptance_profile_id") or f"ap-{index}"),
                "evidence_grade": raw.get("evidence_grade") or "B",
                "evidence_ids": raw.get("evidence_ids") or [],
                "claim_role": raw.get("claim_role")
                or ("final" if "final" in kind else "intermediate"),
                "applies_to_modes": ["autonomous_research", "paper_reproduction"],
            }
        )
    return result


def _mode_info(
    review: dict,
    scope: dict,
    complexity: dict,
    pair_id: str,
    *,
    mode: str,
    task_mode: str,
    disclosure: str,
    task_text: str,
) -> dict:
    suffix = "autonomous" if mode == "autonomous_research" else "reproduction"
    public = review.get("public_task_basis") or {}
    return {
        "task_id": f"{pair_id}_{suffix}",
        "task_pair_id": pair_id,
        "source_id": str(review.get("source_id") or "paper_source"),
        "category": str(review.get("category") or "computational_chemistry"),
        "benchmark_family": str(review.get("task_direction") or ""),
        "mode": mode,
        "task_mode": task_mode,
        "scientific_mode": mode,
        "method_disclosure": disclosure,
        "pathway_disclosure": disclosure,
        "task": task_text,
        "scientific_mode_description": "Replace this scaffold with an evidence-backed task description.",
        "scientific_requirements": [],
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
        "workflow_scope": scope,
        "complexity_profile": complexity,
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
    suffix = "autonomous" if mode == "autonomous_research" else "reproduction"
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
        "task_id": f"{pair_id}_{suffix}",
        "task_pair_id": pair_id,
        "mode": mode,
        "task_mode": task_mode,
        "scientific_mode": mode,
        "method_disclosure": disclosure,
        "pathway_disclosure": disclosure,
        "scientific_question": question,
        "target_definition": question,
        "boundary_conditions": public.get("boundary_conditions") or [],
        "input_assets": assets,
        "workflow_scope": scope,
        "complexity_profile": complexity,
    }


def _profiles(truths: list[dict]) -> list[dict]:
    profiles = []
    for truth in truths:
        profile_id = truth["acceptance_profile_id"]
        profile_type = truth["acceptance_type"]
        parameters = truth.get("acceptance_parameters") or {}
        answer = truth.get("canonical_answer")
        binding = {
            "artifact_paths": ["report/results.json", "report/report.md"],
            "observed_fields": ["document"],
            "canonical_projection": answer,
            "comparison": profile_type,
        }
        profile = {
            "acceptance_profile_id": profile_id,
            "type": profile_type,
            "submission_binding": binding,
        }
        if profile_type == "numeric_tolerance":
            profile.update(
                {
                    "target": answer,
                    "unit": parameters.get("unit") or "source_unit",
                    "absolute_tolerance": parameters.get("absolute_tolerance", 0.0),
                }
            )
            binding["observed_fields"] = ["$.value"]
        elif profile_type == "ranking":
            profile["target_order"] = parameters.get("target_order") or answer
        elif profile_type == "trend":
            profile["required_trends"] = parameters.get("required_trends") or [answer]
        else:
            required = truth.get("required_propositions") or (
                [answer] if isinstance(answer, str) else []
            )
            profile["required_propositions"] = required
            profile["forbidden_contradictions"] = truth.get("forbidden_contradictions") or []
            binding["canonical_projection"] = {"required_propositions": required}
        profiles.append(profile)
    return profiles


def main() -> None:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "outputs").resolve()
    review_path = Path(sys.argv[2] if len(sys.argv) > 2 else root / "workflow_review.json").resolve()
    review = json.loads(review_path.read_text(encoding="utf-8"))
    if review.get("decision") != "candidate_ready":
        raise SystemExit("bootstrap requires workflow_review decision=candidate_ready")
    scope = review.get("workflow_scope") or {}
    complexity = review.get("complexity_profile") or {}
    pair_id = str(review.get("task_pair_id") or "task_pair")
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
    task_text = "Follow the author-disclosed route to determine the stated computational quantities. Replace this scaffold with the complete evidence-backed reproduction instruction."
    dump(reproduction / "task_info.json", _mode_info(review, scope, complexity, pair_id, mode="paper_reproduction", task_mode="guided_reproduction", disclosure="paper_route_disclosed", task_text=task_text))
    dump(reproduction / "task_spec.json", _mode_spec(review, scope, complexity, pair_id, mode="paper_reproduction", task_mode="guided_reproduction", disclosure="paper_route_disclosed"))
    dump(reproduction / "submission_contract.json", {"schema_version": "1.0", "task_pair_id": pair_id, "required_files": ["report/results.json", "report/report.md"], "submission_path": "report/results.json", "allowed_extra_fields": True})
    dump(reproduction / "process_rubric.json", [{"id": "workflow_execution", "max_score": 60, "description": "Execute the complete scientific workflow and preserve intermediate evidence."}, {"id": "validation_and_analysis", "max_score": 40, "description": "Validate outputs and connect them to the scientific question."}])
    (reproduction / "task.md").write_text(task_text + "\n", encoding="utf-8")
    (reproduction / "paper_route.md").write_text(json.dumps(review.get("paper_route") or {}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    dump(reproduction / "workflow_spec.json", {"steps": review.get("workflow_steps") or []})
    dump(reproduction / "route_evidence_map.json", review.get("evidence_map") or {})
    truths = normalize_truths(review)
    profiles = _profiles(truths)
    rubric = []
    if truths:
        base = 100 // len(truths)
        remainder = 100 - base * len(truths)
        for index, truth in enumerate(truths):
            rubric.append({"id": "claim_" + truth["ground_truth_id"], "max_score": base + (remainder if index == len(truths) - 1 else 0), "statement": str(truth.get("canonical_answer") or truth["ground_truth_id"]), "acceptance_rule": "Evaluate against the linked typed acceptance profile.", "required_evidence": ["report/results.json", "report/report.md"], "ground_truth_ids": [truth["ground_truth_id"]], "acceptance_profile_ids": [truth["acceptance_profile_id"]]})
    hidden_root = root / "hidden_reference"
    hidden = {"status": "ready", "task_pair_id": pair_id, "expected_result": {}, "ground_truth_items": truths, "acceptance_profiles": profiles, "scientific_conclusion_rubric": rubric, "critical_failures": ["No real chemistry calculation was executed."], "reference_evidence": {"evidence_ids": evidence_ids(review.get("evidence_map"))}, "evidence_gate_policy": {}, "managed_computation_policy": {"required": True}, "summary": "Replace this scaffold summary with an evidence-backed summary."}
    dump(hidden_root / "ground_truth_common.json", hidden)
    dump(hidden_root / "acceptance_profiles.json", profiles)
    dump(hidden_root / "conclusion_rubric.json", rubric)
    dump(hidden_root / "private_evidence_map.json", review.get("evidence_map") or {})
    dump(root / "toolbox_requirements.json", review.get("toolbox_requirements") or [])
    print("task-pair scaffold created; replace scaffold prose and validate before receipt")


if __name__ == "__main__":
    main()
