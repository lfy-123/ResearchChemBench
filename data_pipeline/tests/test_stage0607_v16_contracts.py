from __future__ import annotations

import json
from pathlib import Path

from src.stages.phase_gate import _input_findings, run
from src.stages.stage06_task_builder.bootstrap_task_pair import _mode_info, _mode_spec
from src.stages.stage06_task_builder.prompts import (
    autonomous_converter_instructions,
    task_pair_builder_instructions,
)
from src.stages.stage06_task_builder.validation import _input_closure_findings


def _write(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value if isinstance(value, str) else json.dumps(value), encoding="utf-8")


def _pair(tmp_path: Path) -> Path:
    pair = tmp_path / "pair"
    for mode in ("paper_reproduction", "autonomous_research"):
        root = pair / mode
        _write(root / "task.md", "# Task\nCompute the requested result.\n")
        _write(
            root / "task_info.json",
            {
                "paper_id": "paper-v16",
                "task_id": "paper-v16",
                "mode": mode,
                "scientific_mode": mode,
                "task_mode": "guided_reproduction" if mode == "paper_reproduction" else "open_discovery",
                "scientific_question": "Determine the requested quantity.",
                "required_deliverables": [{"path": "report/results.json"}],
            },
        )
        _write(
            root / "task_spec.json",
            {
                "paper_id": "paper-v16",
                "task_id": "paper-v16",
                "mode": mode,
                "scientific_mode": mode,
                "scientific_question": "Determine the requested quantity.",
                "input_assets": [{"path": "data/inputs/structure.xyz"}],
            },
        )
        _write(root / "submission_contract.json", {"required_files": ["report/results.json"], "results_schema": {"type": "object"}})
        _write(root / "process_rubric.json", [{"id": "science", "description": "Compute and validate the result."}])
        if mode == "paper_reproduction":
            _write(root / "paper_route.md", "# Route\n")
            _write(root / "workflow_spec.json", {"steps": []})
            _write(root / "route_evidence_map.json", {})
        _write(root / "data/inputs/structure.xyz", "2\nwater\nH 0 0 0\nH 0 0 1\n")
    return pair


def test_model_prompts_hide_internal_stage_roles_and_order_input_closure() -> None:
    synthesis = task_pair_builder_instructions(paper_id="paper-v16", snapshot_hash="hash")
    converter = autonomous_converter_instructions(
        paper_id="paper-v16", task_pair_id="paper-v16"
    )
    for prompt in (synthesis, converter):
        assert "Stage06A" not in prompt
        assert "Stage06B" not in prompt
        assert "Stage07" not in prompt
        assert "stage06a" not in prompt.casefold()
        assert "stage06b" not in prompt.casefold()
        assert "stage07" not in prompt.casefold()
    assert synthesis.index("minimum inputs") < synthesis.index("Generate the complete public task pair")
    assert "workflow_completeness_check.input_closure" in synthesis


def test_agent_facing_phase_alias_uses_same_gate_contract(tmp_path: Path) -> None:
    pair = _pair(tmp_path)
    assert run("synthesis", pair)["findings"] == run("stage06a", pair)["findings"]


def test_public_bootstrap_projection_drops_private_scope() -> None:
    review = {
        "paper_id": "paper-v16",
        "public_scientific_question": "Determine the requested quantity.",
        "category": "computational_chemistry",
        "task_direction": "energy",
        "workflow_scope": {"supported_primary_claims": ["hidden answer"]},
        "complexity_profile": {"level": "high"},
        "public_task_basis": {"boundary_conditions": [], "input_assets": []},
    }
    info = _mode_info(review, review["workflow_scope"], review["complexity_profile"], "paper-v16", mode="autonomous_research", task_mode="open_discovery", disclosure="public_problem_only")
    spec = _mode_spec(review, review["workflow_scope"], review["complexity_profile"], "paper-v16", mode="autonomous_research", task_mode="open_discovery", disclosure="public_problem_only")
    assert "workflow_scope" not in info and "complexity_profile" not in info
    assert "workflow_scope" not in spec and "complexity_profile" not in spec
    assert "Replace this scaffold" not in json.dumps(info)


def test_input_closure_requires_selected_assets_and_no_unresolved_fields() -> None:
    assert _input_closure_findings({"workflow_completeness_check": {"input_closure": {"status": "closed", "assets": [{"path": "a.xyz"}], "unresolved_fields": []}}}) == []
    assert "input_closure_fields_unresolved" in _input_closure_findings({"input_closure": {"status": "closed", "assets": [{"path": "a.xyz"}], "unresolved_fields": ["charge"]}})


def test_gate_blocks_malformed_xyz_and_private_public_fields(tmp_path: Path) -> None:
    pair = _pair(tmp_path)
    _write(pair / "paper_reproduction/data/inputs/structure.xyz", "not xyz\n")
    _write(pair / "paper_reproduction/task_spec.json", {"workflow_scope": {"answer": "hidden"}, "input_assets": [{"path": "data/inputs/structure.xyz"}]})
    report = run("stage06a", pair)
    assert any("input_asset_xyz_header_invalid" in value for value in report["blocking_findings"])
    assert any("public_private_field_present" in value for value in report["blocking_findings"])


def test_gate_blocks_public_placeholder(tmp_path: Path) -> None:
    pair = _pair(tmp_path)
    (pair / "paper_reproduction/task.md").write_text(
        "Replace this scaffold with the final task.", encoding="utf-8"
    )
    report = run("stage06a", pair)
    assert any("public_placeholder" in value for value in report["blocking_findings"])
