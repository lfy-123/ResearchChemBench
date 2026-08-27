from __future__ import annotations

import json
from pathlib import Path

from src.stages.phase_gate import run as run_gate
from src.stages.stage06_task_builder.prompts import (
    STAGE06_SYNTHESIS_PROMPT_VERSION,
    final_task_synthesis_instructions,
)
from src.stages.stage07_task_judge.package import assemble_release_pair
from src.stages.stage07_task_judge.prompts import STAGE07_AUDIT_PROMPT_VERSION


PAPER_ID = "paper_v24fixture"


def _write(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        value if isinstance(value, str) else json.dumps(value, ensure_ascii=False),
        encoding="utf-8",
    )


def _mode(root: Path, mode: str) -> None:
    base = root / mode
    _write(base / "task.md", "# Task\n\n## Scientific objective\n\nDetermine the barrier.\n")
    _write(base / "data/inputs/reactant.xyz", "1\nreactant\nH 0.0 0.0 0.0\n")
    _write(
        base / "task_info.json",
        {
            "paper_id": PAPER_ID,
            "task_type": mode,
            "title": "Barrier task",
            "category": "reaction",
            "paper": {"title": "", "doi": "", "journal": "", "publication_date": ""},
            "data": [{"path": "data/inputs", "description": "Reactant input"}],
            "required_deliverables": [
                {"path": "report/results.json", "description": "Results"}
            ],
        },
    )
    _write(
        base / "submission_schema.json",
        {
            "required_files": ["report/results.json"],
            "primary_result_file": "report/results.json",
            "result_schema": {
                "type": "object",
                "properties": {
                    "barrier": {"type": "number"},
                    "conclusion": {"type": "string"},
                },
                "required": ["barrier", "conclusion"],
            },
        },
    )
    ev = root / "evaluator_reference" / mode
    common = {"paper_id": PAPER_ID}
    _write(
        ev / "reference_key_points.json",
        {**common, "items": [{"key_point_id": "kp1", "statement": "Barrier", "expected": 12.3, "evidence_ids": ["ev1"]}]},
    )
    _write(
        ev / "reference_conclusions.json",
        {**common, "items": [{"conclusion_id": "c1", "statement": "Path", "expected": "path A", "supporting_key_point_ids": ["kp1"], "evidence_ids": ["ev1"], "claim_role": "final"}]},
    )
    _write(
        ev / "scoring_rules.json",
        {**common, "rules": [
            {"rule_id": "r1", "reference_id": "kp1", "type": "numeric", "target": 12.3, "unit": "kcal/mol", "tolerance": 1.0, "binding": {"artifact_paths": ["report/results.json"], "fields": ["$.barrier"], "comparison": "absolute difference"}},
            {"rule_id": "r2", "reference_id": "c1", "type": "semantic", "expected": "path A", "binding": {"artifact_paths": ["report/results.json"], "fields": ["$.conclusion"], "comparison": "semantic comparison"}},
        ]},
    )
    _write(ev / "evidence_map.json", {**common, "evidence": [{"evidence_id": "ev1", "source": "article result"}]})
    _write(ev / "critical_failures.json", {**common, "items": [{"failure_id": "f1", "condition": "No result", "severity": "critical"}]})


def _candidate(root: Path, modes: list[str]) -> Path:
    _write(
        root / "workflow_review.json",
        {
            "decision": "candidate_ready",
            "paper_id": PAPER_ID,
            "scientific_core": {"objective": "barrier"},
            "paper_route": {"scientific_route": "author hypothesis"},
            "reference_results": {"source": "article"},
            "feasibility": {
                "objective": {"status": "passed"},
                "public_inputs": {"status": "passed", "agent_input_assets": [], "database_inputs": [], "unresolved_essential_inputs": []},
                "evaluation": {"status": "passed"},
                "reproducible_investigation": {"status": "passed"},
                "modes": {
                    mode: {"status": "feasible" if mode in modes else "infeasible"}
                    for mode in ("autonomous_research", "paper_reproduction")
                },
                "release_modes": modes,
            },
        },
    )
    for mode in modes:
        _mode(root, mode)
    return root


def test_v24_prompt_and_versions_express_per_mode_database_boundary() -> None:
    prompt = final_task_synthesis_instructions(paper_id=PAPER_ID, snapshot_hash="hash")
    assert STAGE06_SYNTHESIS_PROMPT_VERSION.startswith("v24-")
    assert "separately" in prompt and "One feasible" in prompt
    assert "Do not require PubChem/CCDC calls" in prompt
    assert "stable record ID" in prompt
    assert STAGE07_AUDIT_PROMPT_VERSION.startswith("v24-")


def test_single_mode_gate_and_release_are_supported(tmp_path: Path) -> None:
    pair = _candidate(tmp_path / "pair", ["paper_reproduction"])
    report = run_gate("synthesis", pair)
    assert report["status"] == "passed", report
    source_pdf = tmp_path / "source.pdf"
    source_pdf.write_bytes(b"%PDF fixture")
    _write(pair / "paper_info.json", {"paper_id": PAPER_ID, "title": "Fixture", "doi": "", "journal": "", "publication_date": "", "documents": [{"document_type": "main_paper", "source_path": str(source_pdf)}]})
    release = assemble_release_pair(pair_root=pair, release_root=tmp_path / "release", paper_id=PAPER_ID, release_modes=["paper_reproduction"])
    assert release["status"] == "passed", release
    assert (tmp_path / "release/tasks/paper_reproduction/paper_v24fixture").is_dir()
    assert not (tmp_path / "release/tasks/autonomous_research").exists()


def test_scientific_rejection_cannot_contain_mode_tree(tmp_path: Path) -> None:
    root = tmp_path / "outputs"
    _write(root / "workflow_review.json", {"decision": "scientific_not_constructible", "paper_id": PAPER_ID})
    _mode(root, "paper_reproduction")
    report = run_gate("synthesis", root)
    assert report["status"] == "failed"
    assert "scientific_rejection_contains_mode:paper_reproduction" in report["findings"]


def test_numeric_target_and_required_chain_are_mechanical_contracts(tmp_path: Path) -> None:
    root = _candidate(tmp_path / "outputs", ["paper_reproduction"])
    rules = json.loads((root / "evaluator_reference/paper_reproduction/scoring_rules.json").read_text())
    rules["rules"][0]["target"] = "12.3"
    _write(root / "evaluator_reference/paper_reproduction/scoring_rules.json", rules)
    report = run_gate("synthesis", root)
    assert "paper_reproduction:numeric_rule_target_not_number:r1" in report["findings"]
