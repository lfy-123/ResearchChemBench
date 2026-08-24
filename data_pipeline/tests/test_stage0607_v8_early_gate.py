from __future__ import annotations

import json
from pathlib import Path

from src.agents import (
    AgentExecutionError,
    AgentRunRequest,
    AgentRunResult,
    create_agent_harness,
)
from src.agents.schemas import STAGE06_AUTONOMOUS_CONVERTER_SCHEMA
from src.stages.stage06_task_builder.stage import (
    _run_phase,
    _stage06a_phase_gate_findings,
)
from src.stages.stage07_task_judge.stage import (
    _run_audit_repair_agent,
    _stage07a_phase_gate_findings,
)
from src.stages.stage07_task_judge.validation import (
    normalize_stage07_transport_contract,
    stage07_mechanical_pre_publish_check,
)


def test_phase_gate_recovers_once_then_fails_open_with_a_visible_warning(tmp_path: Path):
    calls = 0

    def responder(request: AgentRunRequest) -> dict:
        nonlocal calls
        calls += 1
        if calls == 2:
            assert (request.workspace / "RECOVERY_CONTEXT.md").is_file()
            assert "synthetic_gate_finding" in (
                request.workspace / "RECOVERY_CONTEXT.md"
            ).read_text(encoding="utf-8")
        output = request.workspace / "outputs" / "autonomous_research"
        output.mkdir(parents=True, exist_ok=True)
        return {
            "status": "converted",
            "artifact_path": "outputs/autonomous_research",
            "summary": "conversion receipt",
            "invalid_reasons": [],
        }

    harness = create_agent_harness(
        "mock",
        config={"mock_responder": responder},
        model_config={"model": "mock"},
    )
    response, _, workspace = _run_phase(
        harness=harness,
        stage_root=tmp_path / "stage",
        paper_id="paper-gate",
        phase="autonomous_converter",
        prompt_version="test-gate",
        instructions="convert",
        output_schema=STAGE06_AUTONOMOUS_CONVERTER_SCHEMA,
        fingerprint_value={"paper": "paper-gate"},
        config={
            "max_attempts": 1,
            "resume": False,
            "retry_backoff_seconds": 0,
            "max_tool_calls": 4,
        },
        setup=lambda root: (root / "inputs" / "task_pair" / "paper_reproduction").mkdir(
            parents=True
        ),
        phase_gate_validator=lambda _response, _workspace: ["synthetic_gate_finding"],
        phase_gate_max_checks=2,
        phase_gate_fail_open=True,
    )

    assert calls == 2
    assert response["phase_gate_status"] == "bypassed_with_warnings"
    assert response["phase_gate_attempts"] == 2
    assert response["phase_gate_findings"] == ["synthetic_gate_finding"]
    assert workspace is not None
    report = json.loads(
        (workspace / "phase_gate_report.json").read_text(encoding="utf-8")
    )
    assert report["status"] == "bypassed_with_warnings"
    assert report["attempt"] == 2


def test_phase_gate_falls_back_to_file_recovery_when_native_resume_fails(
    tmp_path: Path,
):
    session_id = "12345678-1234-4234-9234-123456789abc"
    resume_ids: list[str | None] = []
    recovery_context_seen: list[bool] = []
    session_homes: list[str] = []

    class FakeCodexHarness:
        name = "codex"
        model = "mock"

        def run(self, request: AgentRunRequest) -> AgentRunResult:
            requested = str(
                request.metadata.get("codex_resume_session_id") or ""
            ).strip() or None
            resume_ids.append(requested)
            session_homes.append(str(request.metadata["codex_session_home"]))
            recovery_context_seen.append(
                (request.workspace / "RECOVERY_CONTEXT.md").is_file()
            )
            if len(resume_ids) == 2:
                failed = AgentRunResult(
                    status="failed",
                    response=None,
                    harness="codex",
                    model="mock",
                    phase=request.phase,
                    attempt_id="resume-failed",
                    started_at="2026-08-24T00:00:00Z",
                    duration_seconds=0.0,
                    command=["codex", "exec", "resume", session_id],
                    exit_code=1,
                    workspace=str(request.workspace),
                    failure_class="agent_process_failed",
                    retryable=True,
                    session_id=session_id,
                    resume_mode="native_session",
                )
                raise AgentExecutionError(
                    "synthetic native resume failure",
                    failure_class="agent_process_failed",
                    retryable=True,
                    result=failed,
                )
            output = request.workspace / "outputs" / "autonomous_research"
            output.mkdir(parents=True, exist_ok=True)
            response = {
                "status": "converted",
                "artifact_path": "outputs/autonomous_research",
                "summary": "conversion receipt",
                "invalid_reasons": [],
            }
            return AgentRunResult(
                status="succeeded",
                response=response,
                harness="codex",
                model="mock",
                phase=request.phase,
                attempt_id=f"attempt-{len(resume_ids)}",
                started_at="2026-08-24T00:00:00Z",
                duration_seconds=0.0,
                command=["codex", "exec"],
                exit_code=0,
                workspace=str(request.workspace),
                session_id=session_id if len(resume_ids) == 1 else None,
            )

    response, _, workspace = _run_phase(
        harness=FakeCodexHarness(),
        stage_root=tmp_path / "stage",
        paper_id="paper-native-fallback",
        phase="autonomous_converter",
        prompt_version="test-gate",
        instructions="convert",
        output_schema=STAGE06_AUTONOMOUS_CONVERTER_SCHEMA,
        fingerprint_value={"paper": "paper-native-fallback"},
        config={
            "max_attempts": 1,
            "resume": False,
            "retry_backoff_seconds": 0,
            "max_tool_calls": 4,
            "codex_native_resume": True,
        },
        setup=lambda root: (
            root / "inputs" / "task_pair" / "paper_reproduction"
        ).mkdir(parents=True),
        phase_gate_validator=lambda _response, _workspace: [
            "synthetic_gate_finding"
        ],
        phase_gate_max_checks=2,
        phase_gate_fail_open=True,
    )

    assert resume_ids == [None, session_id, None]
    assert len(set(session_homes)) == 1
    assert session_homes[0].endswith(
        "/codex_sessions/paper-native-fallback/autonomous_converter"
    )
    assert response["phase_gate_status"] == "bypassed_with_warnings"
    assert response["phase_gate_attempts"] == 2
    assert workspace is not None
    assert recovery_context_seen == [False, True, True]


def test_stage07a_gate_is_structural_and_does_not_make_a_scientific_decision(
    tmp_path: Path,
):
    task_pair = tmp_path / "outputs" / "task_pair"
    (task_pair / "paper_reproduction").mkdir(parents=True)
    response = {"audit_decision": "approved"}
    findings = _stage07a_phase_gate_findings(response, tmp_path)
    assert "stage07a_mode_missing:autonomous_research" in findings
    assert "stage07a_hidden_reference_missing" in findings
    assert all("scientific" not in finding for finding in findings)


def test_stage07a_gate_prefers_orchestrator_pair_id(
    tmp_path: Path, monkeypatch
):
    task_pair = tmp_path / "outputs" / "task_pair"
    for mode in ("paper_reproduction", "autonomous_research"):
        mode_root = task_pair / mode
        mode_root.mkdir(parents=True)
        for name in (
            "task.md",
            "task_info.json",
            "task_spec.json",
            "submission_contract.json",
            "process_rubric.json",
        ):
            (mode_root / name).write_text("{}", encoding="utf-8")
    reproduction = task_pair / "paper_reproduction"
    for name in ("paper_route.md", "workflow_spec.json", "route_evidence_map.json"):
        (reproduction / name).write_text("{}", encoding="utf-8")
    hidden = task_pair / "hidden_reference"
    hidden.mkdir()
    (hidden / "ground_truth_common.json").write_text("{}", encoding="utf-8")
    observed: list[str | None] = []

    def fake_gate(_root: Path, *, task_pair_id: str | None = None):
        observed.append(task_pair_id)
        return {"findings": []}

    monkeypatch.setattr(
        "src.stages.stage07_task_judge.stage.stage07_mechanical_pre_publish_check",
        fake_gate,
    )

    findings = _stage07a_phase_gate_findings(
        {
            "audit_decision": "approved",
            "final_task_pair_id": "agent-invented-id",
        },
        tmp_path,
        task_pair_id="paper-canonical-task-pair",
    )

    assert findings == []
    assert observed == ["paper-canonical-task-pair"]


def test_stage07a_second_gate_failure_is_warning_only(
    tmp_path: Path, monkeypatch
):
    handoff = tmp_path / "handoff"
    source = tmp_path / "source"
    handoff.mkdir()
    source.mkdir()
    (handoff / "paper_info.json").write_text("{}\n", encoding="utf-8")
    calls: list[AgentRunRequest] = []

    def responder(request: AgentRunRequest) -> dict:
        calls.append(request)
        if len(calls) == 2:
            recovery = request.workspace / "RECOVERY_CONTEXT.md"
            assert recovery.is_file()
            assert "synthetic_stage07a_gate_finding" in recovery.read_text(
                encoding="utf-8"
            )
        return {
            "audit_decision": "approved",
            "artifact_path": "outputs/task_pair",
            "summary": "synthetic approved audit",
        }

    harness = create_agent_harness(
        "mock",
        config={"mock_responder": responder},
        model_config={"model": "mock"},
    )
    monkeypatch.setattr(
        "src.stages.stage07_task_judge.stage._approved_receipt_contract_findings",
        lambda _response: [],
    )
    monkeypatch.setattr(
        "src.stages.stage07_task_judge.stage._finalize_stage07_response",
        lambda **kwargs: kwargs["response"],
    )
    monkeypatch.setattr(
        "src.stages.stage07_task_judge.stage._require_stage07_artifact_delivery",
        lambda *_args, **_kwargs: None,
    )
    monkeypatch.setattr(
        "src.stages.stage07_task_judge.stage._stage07a_phase_gate_findings",
        lambda *_args, **_kwargs: ["synthetic_stage07a_gate_finding"],
    )

    response, _, artifact_root = _run_audit_repair_agent(
        harness=harness,
        stage_root=tmp_path / "stage07",
        paper_id="paper-stage07a-gate",
        task_pair_id="paper-stage07a-gate_task_pair",
        source_stage06_decision="provisional_constructed",
        handoff_root=handoff,
        source_root=source,
        stage06_record={"paper_id": "paper-stage07a-gate"},
        config={
            "resume": False,
            "max_attempts": 1,
            "retry_backoff_seconds": 0,
            "stage07a_gate_max_checks": 2,
            "stage07_agent_self_check": False,
        },
    )

    assert len(calls) == 2
    assert response["stage07a_gate_status"] == "bypassed_with_warnings"
    assert response["stage07a_gate_attempts"] == 2
    assert response["stage07a_gate_findings"] == [
        "synthetic_stage07a_gate_finding"
    ]
    assert artifact_root.is_dir()
    assert json.loads(
        (artifact_root / "phase_gate_report.json").read_text(encoding="utf-8")
    )["status"] == "bypassed_with_warnings"


def test_stage06a_gate_does_not_require_stage06b_autonomous_surface(
    tmp_path: Path,
):
    outputs = tmp_path / "outputs"
    reproduction = outputs / "paper_reproduction"
    (reproduction / "data" / "inputs").mkdir(parents=True)
    (reproduction / "data" / "inputs" / "input.xyz").write_text(
        "1\ninput\nH 0 0 0\n", encoding="utf-8"
    )
    (reproduction / "task.md").write_text("Run the task.\n", encoding="utf-8")
    for name, value in {
        "task_info.json": {},
        "task_spec.json": {
            "input_assets": [{"path": "data/inputs/input.xyz"}],
        },
        "submission_contract.json": {
            "required_files": ["report/results.json"],
            "results_schema": {"type": "object", "additionalProperties": True},
        },
        "process_rubric.json": [{"id": "kp-1"}],
        "workflow_spec.json": {},
        "route_evidence_map.json": {},
    }.items():
        (reproduction / name).write_text(json.dumps(value), encoding="utf-8")
    (reproduction / "paper_route.md").write_text("route\n", encoding="utf-8")
    hidden = outputs / "hidden_reference"
    hidden.mkdir()
    (hidden / "ground_truth_common.json").write_text(
        json.dumps(
            {
                "status": "ready",
                "ground_truth_items": [
                    {
                        "ground_truth_id": "gt-final",
                        "acceptance_profile_id": "ap-final",
                        "claim_role": "final",
                    }
                ],
                "acceptance_profiles": [
                    {
                        "acceptance_profile_id": "ap-final",
                        "type": "semantic_propositions",
                        "required_propositions": ["A"],
                        "submission_binding": {
                            "artifact_paths": ["report/results.json"],
                            "observed_fields": ["document"],
                            "document_binding": True,
                            "canonical_projection": {"required_propositions": ["A"]},
                            "comparison": "semantic_propositions",
                        },
                    }
                ],
                "scientific_conclusion_rubric": [{"id": "final"}],
            }
        ),
        encoding="utf-8",
    )
    (hidden / "private_evidence_map.json").write_text("{}", encoding="utf-8")
    for name, value in {
        "construction_receipt.json": {"decision": "constructed"},
        "workflow_completeness_check.json": {},
        "public_to_private_asset_map.json": {},
        "toolbox_requirements.json": [],
    }.items():
        (outputs / name).write_text(json.dumps(value), encoding="utf-8")

    findings = _stage06a_phase_gate_findings(
        {"decision": "constructed"}, tmp_path
    )

    assert not any("autonomous" in finding for finding in findings)


def test_stage06a_negative_receipt_ignores_empty_orchestrator_scaffold(
    tmp_path: Path,
):
    outputs = tmp_path / "outputs"
    (outputs / "paper_reproduction" / "data" / "inputs").mkdir(parents=True)
    (outputs / "construction_receipt.json").write_text(
        json.dumps({"decision": "scientific_not_constructible"}),
        encoding="utf-8",
    )

    findings = _stage06a_phase_gate_findings(
        {"decision": "scientific_not_constructible"}, tmp_path
    )

    assert findings == []


def test_stage06a_gate_reports_missing_final_without_modifying_claim_role(
    tmp_path: Path,
):
    hidden = tmp_path / "outputs" / "hidden_reference"
    hidden.mkdir(parents=True)
    original = {
        "status": "ready",
        "ground_truth_items": [
            {
                "ground_truth_id": "gt-1",
                "acceptance_profile_id": "ap-1",
                "claim_role": "intermediate",
            }
        ],
        "acceptance_profiles": [
            {
                "acceptance_profile_id": "ap-1",
                "type": "semantic_propositions",
                "required_propositions": ["A"],
            }
        ],
        "scientific_conclusion_rubric": [{"id": "kp"}],
    }
    (hidden / "ground_truth_common.json").write_text(
        json.dumps(original), encoding="utf-8"
    )

    findings = _stage06a_phase_gate_findings(
        {"decision": "constructed"}, tmp_path
    )

    assert "stage06a_final_claim_missing" in findings
    assert json.loads(
        (hidden / "ground_truth_common.json").read_text(encoding="utf-8")
    ) == original


def test_final_mechanical_gate_is_read_only_after_explicit_normalization(
    tmp_path: Path,
):
    pair = tmp_path / "pair"
    hidden = pair / "hidden_reference"
    hidden.mkdir(parents=True)
    for mode, task_mode, suffix in (
        ("paper_reproduction", "guided_reproduction", "_reproduction"),
        ("autonomous_research", "open_discovery", "_autonomous"),
    ):
        root = pair / mode
        (root / "data" / "inputs").mkdir(parents=True)
        (root / "data" / "inputs" / "input.xyz").write_text(
            "1\ninput\nH 0 0 0\n", encoding="utf-8"
        )
        (root / "task.md").write_text("task\n", encoding="utf-8")
        (root / "task_info.json").write_text(
            json.dumps(
                {
                    "task_id": "pair" + suffix,
                    "task_pair_id": "pair",
                    "source_id": "source",
                    "category": "chemistry",
                    "mode": mode,
                    "scientific_mode": mode,
                    "task_mode": task_mode,
                }
            ),
            encoding="utf-8",
        )
        (root / "task_spec.json").write_text(
            json.dumps(
                {
                    "task_id": "pair" + suffix,
                    "task_pair_id": "pair",
                    "mode": mode,
                    "scientific_mode": mode,
                }
            ),
            encoding="utf-8",
        )
        (root / "submission_contract.json").write_text(
            json.dumps(
                {
                    "required_files": ["report/results.json"],
                    "results_schema": {"type": "object", "additionalProperties": True},
                }
            ),
            encoding="utf-8",
        )
        (root / "process_rubric.json").write_text(
            json.dumps(
                [
                    {
                        "id": "route",
                        "criterion_type": "route_fidelity",
                        "evidence_artifacts": ["report/process_trace.jsonl"],
                    }
                ]
            ),
            encoding="utf-8",
        )
    (hidden / "ground_truth_common.json").write_text(
        json.dumps({"task_pair_id": "pair", "acceptance_profiles": []}),
        encoding="utf-8",
    )
    normalize_stage07_transport_contract(pair, task_pair_id="pair")
    before = {
        path.relative_to(pair).as_posix(): path.read_bytes()
        for path in pair.rglob("*")
        if path.is_file()
    }

    stage07_mechanical_pre_publish_check(pair, task_pair_id="pair")

    after = {
        path.relative_to(pair).as_posix(): path.read_bytes()
        for path in pair.rglob("*")
        if path.is_file()
    }
    assert after == before
