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
    text = "/".join(parts)
    # The review may express an asset relative to the input root (``foo.xyz``)
    # or relative to the public task (``data/inputs/foo.xyz``).  This helper
    # writes below ``paper_reproduction/data/inputs`` and therefore must strip
    # transport prefixes before both materializing the file and projecting its
    # task_spec path.  Iterate so legacy nested aliases normalize once.
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


def evidence_ids(value) -> list[str]:
    if isinstance(value, dict):
        result: list[str] = []
        for key, row in value.items():
            if isinstance(row, dict):
                nested = row.get("evidence_ids") or row.get("evidence_id") or [key]
                result.extend(nested if isinstance(nested, list) else [nested])
        return [str(item) for item in result if str(item)]
    return [str(item) for item in (value or []) if str(item)]


def evaluator_evidence_map(value, *, paper_id: str) -> dict:
    """Project authored review evidence into the one v15 transport shape."""

    if isinstance(value, dict) and isinstance(value.get("evidence"), list):
        candidates = value["evidence"]
    elif isinstance(value, dict) and isinstance(value.get("items"), list):
        candidates = value["items"]
    elif isinstance(value, dict):
        candidates = []
        for identifier, raw in value.items():
            row = dict(raw) if isinstance(raw, dict) else {"description": str(raw)}
            row.setdefault("evidence_id", str(identifier))
            candidates.append(row)
    elif isinstance(value, list):
        candidates = value
    else:
        candidates = []
    rows = []
    seen = set()
    for raw in candidates:
        if isinstance(raw, str):
            row = {"evidence_id": raw}
        elif isinstance(raw, dict):
            row = dict(raw)
        else:
            continue
        identifier = str(row.get("evidence_id") or "").strip()
        if not identifier or identifier in seen:
            continue
        seen.add(identifier)
        row["evidence_id"] = identifier
        rows.append(row)
    return {
        "schema_version": "evidence-map/v1",
        "paper_id": paper_id,
        "evidence": rows,
    }


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
            "numeric": "numeric_final_result",
            "number": "numeric_final_result",
            "numerical_value": "numeric_final_result",
            "numeric_value": "numeric_final_result",
            "numeric_result": "numeric_final_result",
            "conclusion": "textual_final_conclusion",
            "semantic": "textual_final_conclusion",
            "text": "textual_final_conclusion",
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
                "description": raw.get("description") or raw.get("statement"),
                "required_propositions": propositions,
                "forbidden_contradictions": raw.get("forbidden_contradictions") or [],
                "acceptance_type": acceptance_type,
                "acceptance_parameters": raw.get("acceptance_parameters") or {},
                "unit": raw.get("unit") or (raw.get("acceptance_parameters") or {}).get("unit"),
                "rule_id": str(raw.get("rule_id") or raw.get("acceptance_profile_id") or f"rule-{index}"),
                "evidence_grade": raw.get("evidence_grade") or "B",
                "evidence_ids": raw.get("evidence_ids") or [],
                # Claim ownership is scientific authoring, not scaffold syntax.
                # Keep a missing role visible so the Stage06A Gate can ask the
                # Agent to repair it; never promote a claim from its kind/name.
                "claim_role": raw.get("claim_role"),
                "supporting_key_point_ids": raw.get("supporting_key_point_ids") or [],
                "applies_to_modes": raw.get(
                    "applies_to_modes", ["autonomous_research", "paper_reproduction"]
                ),
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


def _profiles(truths: list[dict]) -> list[dict]:
    profiles = []
    for truth in truths:
        profile_id = truth["rule_id"]
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
            "rule_id": profile_id,
            "type": profile_type,
            "submission_binding": binding,
            "applies_to_modes": truth.get(
                "applies_to_modes", ["autonomous_research", "paper_reproduction"]
            ),
        }
        if profile_type == "numeric_tolerance":
            # Preserve scientific incompleteness for the Agent/Gate to repair.
            # A fake unit or zero tolerance changes evaluator meaning and can
            # make an invalid task look complete.
            profile["target"] = answer
            if parameters.get("unit") not in (None, ""):
                profile["unit"] = parameters["unit"]
            for key in (
                "absolute_tolerance",
                "relative_tolerance",
                "tolerance",
                "numeric_tolerances",
            ):
                if parameters.get(key) is not None:
                    # ``tolerance`` is the legacy absolute-tolerance spelling;
                    # expose the canonical evaluator field while retaining the
                    # original parameter object for provenance.
                    profile[
                        "absolute_tolerance" if key == "tolerance" else key
                    ] = parameters[key]
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
    truths = normalize_truths(review)
    profiles = _profiles(truths)
    rubric = []
    if truths:
        for truth in truths:
            rubric.append({"id": "claim_" + truth["ground_truth_id"], "statement": str(truth.get("canonical_answer") or truth["ground_truth_id"]), "acceptance_rule": "Evaluate against the linked typed scoring rule.", "required_evidence": ["report/results.json", "report/report.md"], "ground_truth_ids": [truth["ground_truth_id"]], "rule_ids": [truth["rule_id"]]})
    hidden_root = root / "hidden_reference"
    hidden = {"status": "ready", "paper_id": pair_id, "expected_result": {}, "ground_truth_items": truths, "scoring_rules": profiles, "scientific_conclusion_rubric": rubric, "critical_failures": ["No real chemistry calculation was executed."], "reference_evidence": {"evidence_ids": evidence_ids(review.get("evidence_map"))}, "evidence_gate_policy": {}, "managed_computation_policy": {"required": True}, "summary": "Replace this scaffold summary with an evidence-backed summary."}
    dump(hidden_root / "ground_truth_common.json", hidden)
    dump(hidden_root / "private_evidence_map.json", review.get("evidence_map") or {})
    # Split evaluator transport draft. Scientific authoring and final closure
    # remain the Agent's responsibility; this projection merely avoids
    # duplicating every Ground Truth item into both reference collections.
    evaluator_root = root / "evaluator_reference"
    intermediate_truths = [truth for truth in truths if truth.get("claim_role") != "final"]
    final_truths = [truth for truth in truths if truth.get("claim_role") == "final"]
    dump(
        evaluator_root / "reference_key_points.json",
        {
            "schema_version": "reference-key-points/v1",
            "paper_id": pair_id,
            "items": [
                {
                    "key_point_id": truth["ground_truth_id"],
                    "kind": truth.get("kind") or truth.get("type") or "scientific_result",
                    "statement": str(truth.get("description") or truth.get("canonical_answer") or truth["ground_truth_id"]),
                    "claim_role": truth.get("claim_role") or "intermediate",
                    "expected": truth.get("canonical_answer"),
                    "reference_value": truth.get("canonical_answer"),
                    "unit": truth.get("unit"),
                    "evidence_ids": truth.get("evidence_ids") or [],
                    "evidence_grade": truth.get("evidence_grade") or "",
                    "applies_to_modes": truth.get("applies_to_modes") or ["paper_reproduction", "autonomous_research"],
                }
                for truth in intermediate_truths
            ],
        },
    )
    dump(
        evaluator_root / "reference_conclusions.json",
        {
            "schema_version": "reference-conclusions/v1",
            "paper_id": pair_id,
            "items": [
                {
                    "conclusion_id": "claim_" + truth["ground_truth_id"],
                    "statement": str(truth.get("description") or truth.get("canonical_answer") or truth["ground_truth_id"]),
                    "expected": truth.get("canonical_answer"),
                    "claim_role": "final",
                    "supporting_key_point_ids": truth.get("supporting_key_point_ids") or [],
                    "evidence_ids": truth.get("evidence_ids") or [],
                    "applies_to_modes": truth.get("applies_to_modes") or ["paper_reproduction", "autonomous_research"],
                }
                for truth in final_truths
            ],
        },
    )
    profiles_by_id = {profile.get("rule_id"): profile for profile in profiles}
    split_rules = []
    for truth in truths:
        profile = profiles_by_id.get(truth.get("rule_id")) or {}
        legacy_type = str(profile.get("type") or truth.get("acceptance_type") or "semantic_propositions")
        rule_type = {
            "numeric_tolerance": "numeric",
            "ranking": "ordering",
            "trend": "semantic",
            "semantic_propositions": "semantic",
            "mechanism_claim": "semantic",
        }.get(legacy_type, legacy_type)
        reference_id = (
            "claim_" + truth["ground_truth_id"]
            if truth.get("claim_role") == "final"
            else truth["ground_truth_id"]
        )
        rule = {
            "rule_id": profile.get("rule_id"),
            "reference_id": reference_id,
            "type": rule_type,
            "binding": profile.get("submission_binding") or {},
        }
        if rule_type == "numeric":
            parameters = truth.get("acceptance_parameters") or {}
            rule.update(
                {
                    "target": truth.get("canonical_answer"),
                    "unit": truth.get("unit"),
                    "tolerance": parameters.get("tolerance")
                    if parameters.get("tolerance") is not None
                    else parameters.get("absolute_tolerance")
                    if parameters.get("absolute_tolerance") is not None
                    else parameters.get("numeric_tolerances"),
                }
            )
        else:
            rule["expected"] = truth.get("canonical_answer") or truth.get("required_propositions")
        split_rules.append(rule)
    dump(
        evaluator_root / "scoring_rules.json",
        {
            "schema_version": "scoring-rules/v1",
            "paper_id": pair_id,
            "rules": split_rules,
        },
    )
    dump(
        evaluator_root / "evidence_map.json",
        evaluator_evidence_map(review.get("evidence_map"), paper_id=pair_id),
    )
    dump(
        evaluator_root / "critical_failures.json",
        {
            "schema_version": "critical-failures/v1",
            "paper_id": pair_id,
            "items": hidden["critical_failures"],
        },
    )
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
    print("task-pair scaffold created; replace scaffold prose and validate before receipt")


if __name__ == "__main__":
    main()
