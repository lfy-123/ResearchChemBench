from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from src.agents import AgentExecutionError, AgentRunRequest, create_agent_harness
from src.agents.harness import CliAgentHarness, _trusted_artifact_receipt
from src.agents.schemas import STAGE06_AUTONOMOUS_CONVERTER_SCHEMA
from src.stages.stage06_task_builder.prompts import (
    autonomous_converter_instructions,
    task_pair_builder_instructions,
)
from src.stages.stage06_task_builder.stage import (
    _reconcile_complete_converter_artifact,
    _run_phase,
)
from src.stages.phase_gate import run


def test_phase_gate_tool_reports_all_findings_in_one_result(tmp_path: Path) -> None:
    outputs = tmp_path / "outputs"
    outputs.mkdir()
    report = run("stage06b", outputs)
    assert report["status"] == "failed"
    assert "autonomous_directory_missing" in report["findings"]
    assert len(report["findings"]) == len(set(report["findings"]))


def test_complete_converter_tree_overrides_negative_prose_without_retry(
    tmp_path: Path,
) -> None:
    root = tmp_path / "outputs" / "autonomous_research"
    (root / "data" / "inputs").mkdir(parents=True)
    for name, content in {
        "task.md": "task\n",
        "task_info.json": "{}\n",
        "task_spec.json": "{}\n",
        "submission_contract.json": "{}\n",
        "process_rubric.json": "[]\n",
    }.items():
        (root / name).write_text(content, encoding="utf-8")

    class Result:
        status = "succeeded"
        exit_code = 0

    receipt = _reconcile_complete_converter_artifact(
        {
            "status": "objective_consistency_error",
            "artifact_path": "outputs/autonomous_research",
            "summary": "tool calls were rejected",
            "invalid_reasons": ["model prose"],
        },
        workspace=tmp_path,
        result=Result(),
    )
    assert receipt["status"] == "conversion_uncertain"
    assert receipt["agent_reported_status"] == "objective_consistency_error"
    assert "agent_reported_status:objective_consistency_error" in receipt["invalid_reasons"]


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
    with pytest.raises(AgentExecutionError):
        _run_phase(
        harness=harness,
        stage_root=tmp_path / "stage",
        paper_id="paper-self-check",
        phase="autonomous_converter",
        prompt_version="v9-test",
        instructions="convert",
        output_schema=STAGE06_AUTONOMOUS_CONVERTER_SCHEMA,
        fingerprint_value={"paper": "paper-self-check"},
        config={"max_tool_calls": 4},
        setup=lambda root: (root / "inputs" / "task_pair" / "paper_reproduction").mkdir(parents=True),
        phase_gate_validator=lambda _response, _workspace: ["synthetic_external_finding"],
        phase_gate_mode="agent_and_external",
    )
    assert calls == 1


def test_stage06b_one_shot_injects_self_check_without_retry(tmp_path: Path) -> None:
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
    with pytest.raises(AgentExecutionError):
        _run_phase(
        harness=harness,
        stage_root=tmp_path / "stage",
        paper_id="paper-external-only",
        phase="autonomous_converter",
        prompt_version="v10-test",
        instructions=autonomous_converter_instructions(paper_id="paper-external-only"),
        output_schema=STAGE06_AUTONOMOUS_CONVERTER_SCHEMA,
        fingerprint_value={"paper": "paper-external-only"},
        config={"max_tool_calls": 4},
        setup=lambda root: (root / "inputs" / "task_pair" / "paper_reproduction").mkdir(
            parents=True
        ),
        phase_gate_validator=lambda _response, _workspace: ["synthetic_external_finding"],
        phase_gate_mode="agent_and_external",
        phase_gate_max_checks=1,
    )
    assert calls == 1
    assert len(instructions_seen) == 1
    assert "phase_gate.py --phase autonomous_conversion" in instructions_seen[0]
    assert calls == 1


def test_stage06a_agent_and_external_mode_injects_self_check() -> None:
    prompt = task_pair_builder_instructions(paper_id="paper-a", snapshot_hash="snapshot")
    assert "phase_gate.py --phase synthesis" in prompt
    assert "FINAL SYNTHESIS SELF-CHECK" in prompt


def test_stage06b_prompt_runs_self_check_and_defers_external_gate() -> None:
    prompt = autonomous_converter_instructions(paper_id="paper-b")
    assert "phase_gate.py --phase autonomous_conversion" in prompt
    assert "external check" in prompt


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


def test_timeout_artifact_recovery_requires_complete_declared_tree(tmp_path: Path) -> None:
    outputs = tmp_path / "outputs"
    autonomous = outputs / "autonomous_research"
    autonomous.mkdir(parents=True)
    for name, value in {
        "task.md": "task\n",
        "task_info.json": {},
        "task_spec.json": {},
        "submission_contract.json": {},
        "process_rubric.json": [],
    }.items():
        path = autonomous / name
        path.write_text(value if isinstance(value, str) else json.dumps(value), encoding="utf-8")
    (outputs / "conversion_report.json").write_text(
        json.dumps({"remaining_disclosures": ["audit this"]}), encoding="utf-8"
    )
    request = AgentRunRequest(
        phase="stage06_autonomous_converter",
        record_id="paper-timeout",
        workspace=tmp_path,
        instructions="",
        output_schema=STAGE06_AUTONOMOUS_CONVERTER_SCHEMA,
        prompt_version="test",
        metadata={
            "artifact_receipt_path": "outputs/autonomous_research",
            "artifact_receipt": {
                "status": "conversion_uncertain",
                "artifact_path": "outputs/autonomous_research",
                "summary": "recovered",
                "conversion_report": {},
                "invalid_reasons": ["agent_timeout_after_artifact_write"],
            },
            "artifact_required_files": [
                "task.md",
                "task_info.json",
                "task_spec.json",
                "submission_contract.json",
                "process_rubric.json",
            ],
        },
    )
    recovered = _trusted_artifact_receipt(request=request, workspace=tmp_path)
    assert recovered is not None
    assert recovered["status"] == "conversion_uncertain"
    assert recovered["receipt_recovered_from_artifact"] is True
    assert recovered["conversion_report"]["remaining_disclosures"] == ["audit this"]


def test_cli_timeout_returns_trusted_complete_artifact_without_retry(tmp_path: Path) -> None:
    class TimeoutHarness(CliAgentHarness):
        executable = sys.executable

        def _build_command(self, **_kwargs: object) -> list[str]:
            script = """
import json, pathlib, time
root = pathlib.Path('outputs/autonomous_research')
root.mkdir(parents=True)
for name, value in {
    'task.md': 'task\\n',
    'task_info.json': {},
    'task_spec.json': {},
    'submission_contract.json': {},
    'process_rubric.json': [],
}.items():
    path = root / name
    path.write_text(value if isinstance(value, str) else json.dumps(value))
time.sleep(5)
"""
            return [sys.executable, "-c", script]

        def _parse_response(self, _stdout_path: Path, _final_path: Path) -> dict:
            raise AssertionError("timeout recovery must not parse a missing final response")

    request = AgentRunRequest(
        phase="stage06_autonomous_converter",
        record_id="paper-timeout",
        workspace=tmp_path,
        instructions="",
        output_schema=STAGE06_AUTONOMOUS_CONVERTER_SCHEMA,
        prompt_version="test",
        timeout_seconds=1,
        metadata={
            "artifact_receipt_path": "outputs/autonomous_research",
            "artifact_receipt": {
                "status": "conversion_uncertain",
                "artifact_path": "outputs/autonomous_research",
                "summary": "recovered",
                "conversion_report": {},
                "invalid_reasons": ["agent_timeout_after_artifact_write"],
            },
            "artifact_required_files": [
                "task.md",
                "task_info.json",
                "task_spec.json",
                "submission_contract.json",
                "process_rubric.json",
            ],
        },
    )
    harness = TimeoutHarness(
        name="timeout-test",
        config={"filesystem_isolation": False},
        model_config={"model": "test"},
    )
    result = harness.run(request)
    assert result.status == "succeeded"
    assert result.receipt_recovered_from_artifact is True
    assert result.response is not None
    assert result.response["status"] == "conversion_uncertain"
