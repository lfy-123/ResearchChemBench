from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from src.agents import AgentRunRequest, create_agent_harness
from src.agents.schemas import STAGE06_AUTONOMOUS_CONVERTER_SCHEMA
from src.stages.stage06_task_builder.prompts import (
    autonomous_converter_instructions,
    task_pair_builder_instructions,
)
from src.stages.stage06_task_builder.stage import _run_phase
from src.stages.phase_gate import run


def test_phase_gate_tool_reports_all_findings_in_one_result(tmp_path: Path) -> None:
    outputs = tmp_path / "outputs"
    outputs.mkdir()
    report = run("stage06b", outputs)
    assert report["status"] == "failed"
    assert "autonomous_directory_missing" in report["findings"]
    assert len(report["findings"]) == len(set(report["findings"]))


def test_phase_gate_tool_detects_autonomous_protocol_and_route_leaks(tmp_path: Path) -> None:
    root = tmp_path / "outputs" / "autonomous_research"
    (root / "data" / "inputs").mkdir(parents=True)
    (root / "data" / "inputs" / "input.xyz").write_text("1\ninput\nH 0 0 0\n", encoding="utf-8")
    (root / "task.md").write_text(
        "Use the supplied input and report the result. Read conversion_packet first.\n",
        encoding="utf-8",
    )
    files = {
        "task_info.json": {
            "mode": "autonomous_research",
            "scientific_mode": "autonomous_research",
            "task_mode": "open_discovery",
            "task_id": "pair_autonomous",
            "required_deliverables": [{"path": "report/results.json"}],
        },
        "task_spec.json": {
            "mode": "autonomous_research",
            "scientific_mode": "autonomous_research",
            "input_assets": [{"path": "data/inputs/input.xyz"}],
        },
        "submission_contract.json": {"required_files": ["report/results.json"]},
        "process_rubric.json": [{"id": "kp1"}],
    }
    for name, value in files.items():
        (root / name).write_text(json.dumps(value), encoding="utf-8")
    (root / "paper_route.md").write_text("route", encoding="utf-8")
    report = run("stage06b", tmp_path / "outputs")
    assert any(item.startswith("autonomous_protocol_marker:") for item in report["findings"])
    assert "autonomous_forbidden_route_file:paper_route.md" in report["findings"]


def test_external_gate_is_one_read_only_check_without_model_recovery(tmp_path: Path) -> None:
    calls = 0

    def responder(request: AgentRunRequest) -> dict:
        nonlocal calls
        calls += 1
        output = request.workspace / "outputs" / "autonomous_research"
        output.mkdir(parents=True, exist_ok=True)
        return {
            "status": "converted",
            "artifact_path": "outputs/autonomous_research",
            "summary": "done",
            "invalid_reasons": [],
        }

    harness = create_agent_harness(
        "mock", config={"mock_responder": responder}, model_config={"model": "mock"}
    )
    response, _, workspace = _run_phase(
        harness=harness,
        stage_root=tmp_path / "stage",
        paper_id="paper-self-check",
        phase="autonomous_converter",
        prompt_version="v9-test",
        instructions="convert",
        output_schema=STAGE06_AUTONOMOUS_CONVERTER_SCHEMA,
        fingerprint_value={"paper": "paper-self-check"},
        config={"max_attempts": 1, "resume": False, "max_tool_calls": 4},
        setup=lambda root: (root / "inputs" / "task_pair" / "paper_reproduction").mkdir(parents=True),
        phase_gate_validator=lambda _response, _workspace: ["synthetic_external_finding"],
        phase_gate_agent_self_check=True,
    )
    assert calls == 1
    assert response["phase_gate_status"] == "failed"
    assert response["phase_gate_authority"] == "orchestrator_external_read_only"
    assert response["phase_gate_findings"] == ["synthetic_external_finding"]
    assert workspace is not None
    report = json.loads((workspace / "phase_gate_report.json").read_text(encoding="utf-8"))
    assert report["authority"] == "orchestrator_external_read_only"
    assert report["status"] == "failed"


def test_stage06b_external_only_does_not_inject_self_check_or_retry(tmp_path: Path) -> None:
    calls = 0
    instructions_seen: list[str] = []

    def responder(request: AgentRunRequest) -> dict:
        nonlocal calls
        calls += 1
        instructions_seen.append(request.instructions)
        output = request.workspace / "outputs" / "autonomous_research"
        output.mkdir(parents=True, exist_ok=True)
        return {
            "status": "converted",
            "artifact_path": "outputs/autonomous_research",
            "summary": "done",
            "invalid_reasons": [],
        }

    harness = create_agent_harness(
        "mock", config={"mock_responder": responder}, model_config={"model": "mock"}
    )
    response, _, workspace = _run_phase(
        harness=harness,
        stage_root=tmp_path / "stage",
        paper_id="paper-external-only",
        phase="autonomous_converter",
        prompt_version="v10-test",
        instructions=autonomous_converter_instructions(
            paper_id="paper-external-only", task_pair_id="paper-external-only_task_pair"
        ),
        output_schema=STAGE06_AUTONOMOUS_CONVERTER_SCHEMA,
        fingerprint_value={"paper": "paper-external-only"},
        config={"max_attempts": 1, "resume": False, "max_tool_calls": 4},
        setup=lambda root: (root / "inputs" / "task_pair" / "paper_reproduction").mkdir(
            parents=True
        ),
        phase_gate_validator=lambda _response, _workspace: ["synthetic_external_finding"],
        phase_gate_mode="external_only",
        phase_gate_max_checks=1,
    )
    assert calls == 1
    assert len(instructions_seen) == 1
    assert "MANDATORY AGENT SELF-CHECK" not in instructions_seen[0]
    assert "phase_gate.py --phase stage06b" not in instructions_seen[0]
    assert response["phase_gate_status"] == "failed"
    assert workspace is not None
    report = json.loads((workspace / "phase_gate_report.json").read_text(encoding="utf-8"))
    assert report["agent_self_check_required"] is False
    assert report["authority"] == "orchestrator_external_read_only"


def test_stage06a_agent_and_external_mode_injects_self_check() -> None:
    prompt = task_pair_builder_instructions(paper_id="paper-a", snapshot_hash="snapshot")
    assert "phase_gate.py --phase stage06a" in prompt
    assert "STAGE06A PREFLIGHT GATE" in prompt


def test_stage06b_prompt_defers_gate_to_orchestrator() -> None:
    prompt = autonomous_converter_instructions(
        paper_id="paper-b", task_pair_id="paper-b_task_pair"
    )
    assert "orchestrator will run one independent" in prompt
    assert "phase_gate.py --phase stage06b" not in prompt


def test_phase_gate_cli_exit_codes(tmp_path: Path) -> None:
    command = [
        sys.executable,
        str(Path(__file__).resolve().parents[1] / "src" / "stages" / "phase_gate.py"),
        "--phase",
        "stage06a",
        "--root",
        str(tmp_path / "missing"),
    ]
    result = subprocess.run(command, capture_output=True, text=True, check=False)
    assert result.returncode == 1
    assert json.loads(result.stdout)["status"] == "failed"
