from __future__ import annotations

import json
from pathlib import Path

from src.stages.phase_gate import run as run_gate
from src.stages.stage07_task_judge.package import assemble_release_pair
from src.stages.stage07_task_judge.validation import validate_audit_receipt


PAPER_ID = "paper_v25fixture"
MODES = ("paper_reproduction", "autonomous_research")


def _write(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        value if isinstance(value, str) else json.dumps(value, indent=2),
        encoding="utf-8",
    )


def _mode(root: Path, mode: str, *, process: bool = True, stopping: bool = True) -> None:
    stop = (
        "The calculation is complete when both checks pass. Stop the search when the "
        "reported coverage is exhausted and no new candidate is found."
        if stopping
        else "Perform the calculation and report the result."
    )
    _write(
        root / mode / "task.md",
        "\n".join(
            [
                "# Task",
                "## Scientific objective",
                "Determine the reaction barrier and preferred pathway.",
                "## Public inputs and scientific boundaries",
                "Use data/inputs/reactant.xyz; charge and multiplicity are explicit.",
                "## Required scientific validation/investigation",
                "Validate the stationary point and compare both pathways.",
                stop,
                "## Deliverables",
                "Submit report/results.json with the barrier and conclusion.",
            ]
        ),
    )
    _write(root / mode / "data/inputs/reactant.xyz", "1\nreactant\nH 0 0 0\n")
    _write(
        root / mode / "task_info.json",
        {
            "paper_id": PAPER_ID,
            "task_type": mode,
            "title": "Barrier task",
            "category": "reaction",
            "paper": {"title": "Source", "doi": "", "journal": "", "publication_date": ""},
            "data": [{"path": "data/inputs", "description": "Reactant input"}],
            "required_deliverables": [{"path": "report/results.json", "description": "Results"}],
        },
    )
    _write(
        root / mode / "submission_schema.json",
        {
            "required_files": ["report/results.json"],
            "primary_result_file": "report/results.json",
            "result_schema": {
                "type": "object",
                "properties": {"barrier": {"type": "number"}, "conclusion": {"type": "string"}},
                "required": ["barrier", "conclusion"],
            },
        },
    )
    ev = root / "evaluator_reference" / mode
    common = {"paper_id": PAPER_ID}
    key_point = {
        "key_point_id": "kp_process",
        "key_point_type": "process" if process else "result",
        "statement": "Validate the stationary point",
        "expected": "validated",
        "evidence_ids": ["ev1"],
    }
    _write(ev / "reference_key_points.json", {**common, "items": [key_point]})
    _write(
        ev / "reference_conclusions.json",
        {**common, "items": [{"conclusion_id": "c1", "statement": "Preferred pathway", "expected": "path A", "supporting_key_point_ids": ["kp_process"], "evidence_ids": ["ev1"], "claim_role": "final"}]},
    )
    _write(
        ev / "scoring_rules.json",
        {**common, "rules": [{"rule_id": "r1", "reference_id": "kp_process", "type": "semantic", "expected": "validated", "binding": {"artifact_paths": ["report/results.json"], "fields": ["$.conclusion"], "comparison": "semantic"}}, {"rule_id": "r2", "reference_id": "c1", "type": "semantic", "expected": "path A", "binding": {"artifact_paths": ["report/results.json"], "fields": ["$.conclusion"], "comparison": "semantic"}}]},
    )
    _write(ev / "evidence_map.json", {**common, "evidence": [{"evidence_id": "ev1", "source": "article result"}]})
    _write(ev / "critical_failures.json", {**common, "items": [{"failure_id": "f1", "condition": "No result", "severity": "critical"}]})


def _review(root: Path, modes=MODES) -> None:
    _write(root / "paper_route.md", "## Private author route\nSource-supported protocol reference.\n")
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
                "public_inputs": {"status": "passed", "unresolved_essential_inputs": []},
                "evaluation": {"status": "passed"},
                "reproducible_investigation": {"status": "passed"},
                "modes": {m: {"status": "feasible" if m in modes else "infeasible"} for m in MODES},
                "release_modes": list(modes),
            },
            "task_quality": {
                name: {"status": "passed", "finding": "checked", "evidence": ["task.md"], "repairs": []}
                for name in ("instruction_completeness", "input_completeness", "process_keypoints", "final_conclusions", "mode_separation")
            },
        },
    )
    for mode in modes:
        _mode(root, mode)


def test_complete_task_contract_passes(tmp_path: Path) -> None:
    root = tmp_path / "outputs"
    _review(root, modes=("paper_reproduction",))
    report = run_gate("synthesis", root)
    assert report["status"] == "passed", report


def test_missing_process_key_point_is_blocking(tmp_path: Path) -> None:
    root = tmp_path / "outputs"
    _review(root, modes=("paper_reproduction",))
    _mode(root, "paper_reproduction", process=False)
    report = run_gate("synthesis", root)
    assert "paper_reproduction:process_key_point_missing" in report["findings"]


def test_missing_stopping_condition_is_blocking(tmp_path: Path) -> None:
    root = tmp_path / "outputs"
    _review(root, modes=("paper_reproduction",))
    _mode(root, "paper_reproduction", stopping=False)
    report = run_gate("synthesis", root)
    assert "paper_reproduction:task_stopping_condition_missing" in report["findings"]


def test_explicit_atom_count_description_matches_xyz(tmp_path: Path) -> None:
    root = tmp_path / "outputs"
    _review(root, modes=("paper_reproduction",))
    info_path = root / "paper_reproduction/task_info.json"
    info = json.loads(info_path.read_text())
    info["data"][0]["description"] = "A complete 2-atom XYZ input."
    _write(info_path, info)
    report = run_gate("synthesis", root)
    assert any("data_description_atom_count_mismatch" in item for item in report["findings"])


def test_public_json_reference_answer_field_is_blocking(tmp_path: Path) -> None:
    root = tmp_path / "outputs"
    _review(root, modes=("paper_reproduction",))
    _write(root / "paper_reproduction/data/inputs/system.json", {"experimental_constraints": {"reaction_energy_kJ_mol": -162.0}, "conditions": {"temperature_K": 298.15}})
    report = run_gate("synthesis", root)
    assert any("public_answer_field" in item for item in report["findings"])


def test_approved_audit_requires_all_scientific_dimensions(tmp_path: Path) -> None:
    artifact = tmp_path / "outputs" / "audited_task"
    _review(artifact, modes=("paper_reproduction",))
    audit = {
        name: {"status": "passed", "finding": "checked", "evidence": [name], "repairs": []}
        for name in ("objective", "inputs", "instruction_completeness", "process_keypoints", "final_conclusions", "mode_separation", "answer_inversion", "evaluator_quality")
    }
    receipt = {"audit_decision": "approved", "paper_id": PAPER_ID, "artifact_path": "outputs/audited_task", "release_modes": ["paper_reproduction"], "selected_workflow_preserved": True, "repairs": [], "remaining_issues": [], "scientific_audit": audit, "summary": "approved"}
    assert validate_audit_receipt(receipt, paper_id=PAPER_ID, workspace=tmp_path) == artifact


def test_paper_route_is_released_as_non_agent_metadata(tmp_path: Path) -> None:
    root = tmp_path / "pair"
    _review(root, modes=("paper_reproduction",))
    _write(root / "paper_info.json", {"paper_id": PAPER_ID, "title": "Source", "doi": "", "journal": "", "publication_date": "", "documents": [{"document_type": "main_paper", "source_path": str(tmp_path / "source.pdf")}]})
    (tmp_path / "source.pdf").write_bytes(b"%PDF fixture")
    release = assemble_release_pair(pair_root=root, release_root=tmp_path / "release", paper_id=PAPER_ID, release_modes=["paper_reproduction"])
    assert release["status"] == "passed", release
    task = tmp_path / "release/tasks/paper_reproduction" / PAPER_ID
    assert (task / "paper_route.md").is_file()
    assert not (task / "agent_input/paper_route.md").exists()
    manifest = json.loads((task / "package_manifest.json").read_text())
    route_entries = [entry for entry in manifest["entries"] if entry["path"] == "paper_route.md"]
    assert route_entries and route_entries[0]["visibility"] == "metadata"
