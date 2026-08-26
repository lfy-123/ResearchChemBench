from __future__ import annotations

import json
from pathlib import Path

import jsonschema

from evaluation.contracts import validate_task_package
from src.agents.schemas import STAGE06_SYNTHESIS_SCHEMA
from src.stages.phase_gate import run as run_gate
from src.stages.stage06_task_builder.prompts import final_task_synthesis_instructions
from src.stages.stage07_task_judge.package import TASK_TYPES, assemble_release_pair
from src.stages.stage07_task_judge.validation import (
    external_audit_gate,
    validate_audit_receipt,
)
from src.agents.workspace import copytree_exact, make_read_only, make_writable
from src.stages.phase_gate import install_phase_gate_tool


PAPER_ID = "paper_fixture19"


def _write(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(value, str):
        path.write_text(value, encoding="utf-8")
    else:
        path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def _mode(root: Path, task_type: str) -> None:
    mode = root / task_type
    _write(mode / "task.md", f"# {task_type}\n\n## Scientific objective\n\nFind the barrier.\n")
    _write(mode / "data/inputs/reactant.xyz", "1\nreactant\nH 0 0 0\n")
    _write(
        mode / "task_info.json",
        {
            "paper_id": PAPER_ID,
            "task_type": task_type,
            "title": "Barrier study",
            "category": "reaction_mechanism",
            "paper": {"title": "", "doi": "", "journal": "", "publication_date": ""},
            "data": [{"path": "data/inputs", "description": "Reactant"}],
            "required_deliverables": [
                {"path": "report/results.json", "description": "Results"}
            ],
        },
    )
    _write(
        mode / "submission_schema.json",
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
                "additionalProperties": False,
            },
        },
    )
    evaluator = root / "evaluator_reference" / task_type
    common = {"paper_id": PAPER_ID}
    _write(
        evaluator / "reference_key_points.json",
        {**common, "items": [{"key_point_id": "kp1", "statement": "Barrier", "expected": 12.3, "evidence_ids": ["ev1"]}]},
    )
    _write(
        evaluator / "reference_conclusions.json",
        {**common, "items": [{"conclusion_id": "c1", "statement": "Path", "expected": "path A", "supporting_key_point_ids": ["kp1"], "evidence_ids": ["ev1"], "claim_role": "final"}]},
    )
    _write(
        evaluator / "scoring_rules.json",
        {**common, "rules": [
            {"rule_id": "r1", "reference_id": "kp1", "type": "numeric", "target": 12.3, "unit": "kcal/mol", "tolerance": 1.0, "binding": {"artifact_paths": ["report/results.json"], "fields": ["$.barrier"], "comparison": "absolute_difference"}},
            {"rule_id": "r2", "reference_id": "c1", "type": "semantic", "expected": "path A", "binding": {"artifact_paths": ["report/results.json"], "fields": ["$.conclusion"], "comparison": "semantic_entailment"}},
        ]},
    )
    _write(evaluator / "evidence_map.json", {**common, "evidence": [{"evidence_id": "ev1", "source": "main article, result section"}]})
    _write(evaluator / "critical_failures.json", {**common, "items": [{"id": "cf1", "description": "No computed result"}]})


def candidate(root: Path, *, both_modes: bool = True) -> Path:
    _write(
        root / "workflow_review.json",
        {
            "decision": "candidate_ready",
            "paper_id": PAPER_ID,
            "scientific_core": {"objective": "barrier"},
            "paper_route": {"method": "source supported"},
            "input_closure": {"status": "closed", "assets": ["reactant.xyz"]},
        },
    )
    _mode(root, "paper_reproduction")
    if both_modes:
        _mode(root, "autonomous_research")
    return root


def test_prompt_is_reproduction_first_then_same_agent_derivation() -> None:
    prompt = final_task_synthesis_instructions(paper_id=PAPER_ID, snapshot_hash="abc")
    reproduction = prompt.index("complete paper-reproduction task first")
    intermediate_gate = prompt.index("paper-reproduction-only mode")
    autonomous = prompt.index("copy the stable reproduction task")
    final_gate = prompt.index("full-pair Gate")
    assert reproduction < intermediate_gate < autonomous < final_gate
    assert "converter" not in prompt.casefold()
    assert prompt.index("construction_receipt.json` last") > final_gate


def test_prompt_terminal_receipt_examples_match_stage06_schema() -> None:
    prompt = final_task_synthesis_instructions(paper_id=PAPER_ID, snapshot_hash="abc")
    decoder = json.JSONDecoder()
    for decision in ("scientific_not_constructible", "constructed"):
        marker = f'"decision": "{decision}"'
        start = prompt.rfind("{", 0, prompt.index(marker))
        receipt, _ = decoder.raw_decode(prompt[start:])
        jsonschema.validate(receipt, STAGE06_SYNTHESIS_SCHEMA)
        assert receipt["paper_id"] == PAPER_ID
        assert receipt["summary"]


def test_gate_can_be_installed_into_a_copied_immutable_snapshot(tmp_path: Path) -> None:
    snapshot = tmp_path / "snapshot"
    _write(snapshot / "source.json", {})
    make_read_only(snapshot)
    inputs = copytree_exact(snapshot, tmp_path / "workspace/inputs")
    make_writable(inputs)
    tool = install_phase_gate_tool(inputs / "tools")
    make_read_only(inputs)
    assert tool.is_file()


def test_reproduction_gate_can_pass_before_autonomous_exists(tmp_path: Path) -> None:
    root = candidate(tmp_path, both_modes=False)
    report = run_gate("synthesis", root, mode="paper_reproduction")
    assert report["status"] == "passed"


def test_self_and_external_gate_are_the_same_contract(tmp_path: Path) -> None:
    root = candidate(tmp_path)
    self_report = run_gate("synthesis", root)
    external_report = external_audit_gate(root)
    assert self_report["status"] == external_report["status"] == "passed"
    assert self_report["findings"] == external_report["findings"] == []
    assert self_report["diagnostics"] == external_report["diagnostics"]


def test_gate_rejects_obsolete_paper_scoped_id(tmp_path: Path) -> None:
    root = candidate(tmp_path)
    info_path = root / "autonomous_research/task_info.json"
    info = json.loads(info_path.read_text())
    info["task_id"] = "obsolete"
    _write(info_path, info)
    report = run_gate("synthesis", root)
    assert "autonomous_research:obsolete_identity_field:task_id" in report["findings"]


def test_gate_rejects_source_paper_material_in_public_inputs(tmp_path: Path) -> None:
    root = candidate(tmp_path / "workspace/outputs")
    source = tmp_path / "workspace/inputs/documents/doc_main/document.md"
    _write(source, "article text")
    _write(root / "paper_reproduction/data/inputs/notes.md", source.read_text())
    report = run_gate("synthesis", root, mode="paper_reproduction")
    assert "paper_reproduction:paper_source_material_exposed:data/inputs/notes.md" in report["findings"]


def test_gate_allows_legitimate_input_filename_with_source_word(tmp_path: Path) -> None:
    root = candidate(tmp_path / "workspace/outputs")
    _write(tmp_path / "workspace/inputs/documents/doc_main/document.md", "article text")
    _write(root / "paper_reproduction/data/inputs/source_data.json", {"temperature": 298.15})
    report = run_gate("synthesis", root, mode="paper_reproduction")
    assert report["status"] == "passed"


def test_audit_receipt_allows_only_the_fixed_approved_snapshot(tmp_path: Path) -> None:
    artifact = candidate(tmp_path / "outputs/audited_task")
    receipt = {
        "audit_decision": "approved",
        "paper_id": PAPER_ID,
        "artifact_path": "outputs/audited_task",
        "selected_workflow_preserved": True,
        "repairs": [],
        "remaining_issues": [],
        "scientific_audit": {},
        "summary": "approved",
    }
    assert validate_audit_receipt(receipt, paper_id=PAPER_ID, workspace=tmp_path) == artifact


def test_release_pair_is_complete_and_agent_input_is_isolated(tmp_path: Path) -> None:
    pair = candidate(tmp_path / "pair")
    source_pdf = tmp_path / "source.pdf"
    source_pdf.write_bytes(b"%PDF fixture")
    _write(
        pair / "paper_info.json",
        {
            "paper_id": PAPER_ID,
            "title": "Fixture paper",
            "doi": "10.test/v19",
            "journal": "Journal",
            "publication_date": "2026-01-01",
            "documents": [{"document_type": "main_paper", "source_path": str(source_pdf)}],
        },
    )
    release = assemble_release_pair(
        pair_root=pair, release_root=tmp_path / "release", paper_id=PAPER_ID
    )
    assert release["status"] == "passed"
    assert (tmp_path / f"release/papers/{PAPER_ID}/documents/main.pdf").is_file()
    for task_type in TASK_TYPES:
        task = tmp_path / "release/tasks" / task_type / PAPER_ID
        assert validate_task_package(task).status == "passed"
        assert not list((task / "agent_input").rglob("*.pdf"))
        assert (task / "evaluation/scoring_rules.json").is_file()
