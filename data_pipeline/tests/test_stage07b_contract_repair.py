from __future__ import annotations

import json
import sys
from pathlib import Path
from types import SimpleNamespace

DATA_PIPELINE_ROOT = Path(__file__).resolve().parents[1]
if str(DATA_PIPELINE_ROOT) not in sys.path:
    sys.path.insert(0, str(DATA_PIPELINE_ROOT))

from src.stages.stage07_contract_repair import (  # noqa: E402
    classify_technical_findings,
    run_stage07b_repair,
    science_fingerprint,
)


class _FakeHarness:
    name = "fake-stage07b"
    model = "fixture"

    def __init__(self, callback):
        self.callback = callback
        self.calls = 0

    def run(self, request):
        self.calls += 1
        response = self.callback(request)
        return SimpleNamespace(
            response=response,
            audit_record=lambda: {"status": "completed", "phase": request.phase},
        )


def _pair(tmp_path: Path) -> Path:
    root = tmp_path / "audited"
    for mode in ("paper_reproduction", "autonomous_research"):
        (root / mode / "data" / "inputs").mkdir(parents=True)
        (root / mode / "task.md").write_text(
            f"# {mode}\nscientific objective\n", encoding="utf-8"
        )
        (root / mode / "data" / "inputs" / "structure.xyz").write_text(
            "1\ninput\nH 0 0 0\n", encoding="utf-8"
        )
        (root / mode / "task_info.json").write_text(
            json.dumps({"task_id": mode, "category": "fixture"}) + "\n",
            encoding="utf-8",
        )
    (root / "hidden_reference").mkdir()
    (root / "hidden_reference" / "ground_truth_common.json").write_text(
        json.dumps({"answer": 1}) + "\n", encoding="utf-8"
    )
    (root / "stage07_audit.json").write_text(
        json.dumps({"audit_decision": "approved"}) + "\n", encoding="utf-8"
    )
    return root


def test_stage07b_only_accepts_transport_findings():
    eligible = classify_technical_findings(
        ["evaluator_binding_field_missing:paper_reproduction:ap_x"]
    )
    assert eligible["eligible"] is True
    assert eligible["unsupported"] == []
    blocked = classify_technical_findings(["reference_states_invalid"])
    assert blocked["eligible"] is False
    assert blocked["unsupported"] == ["reference_states_invalid"]
    open_schema = classify_technical_findings(
        ["binding_schema_path_open:binding_ap_x:$.energies.value"]
    )
    assert open_schema["eligible"] is True
    assert open_schema["unsupported"] == []
    malformed_selector = classify_technical_findings(
        ["evaluator_binding_path_invalid:paper_reproduction:ap_x:$.values[?(@.id=~1)]"]
    )
    assert malformed_selector["eligible"] is False
    assert malformed_selector["unsupported"]


def test_stage07b_does_not_run_for_scientific_or_empty_findings(tmp_path: Path):
    pair = _pair(tmp_path)
    harness = _FakeHarness(lambda _request: {"status": "repaired"})
    report = run_stage07b_repair(
        harness=harness,
        stage_root=tmp_path / "stage",
        paper_id="paper_fixture",
        task_pair_id="paper_fixture_task_pair",
        audited_root=pair,
        findings=["reference_states_invalid"],
        config={"stage07b_enabled": True},
    )
    assert report["status"] == "not_eligible"
    assert harness.calls == 0


def test_stage07b_rejects_science_mutation_and_preserves_audited_tree(tmp_path: Path):
    pair = _pair(tmp_path)
    before = science_fingerprint(pair)

    def mutate_science(request):
        task = request.workspace / "outputs" / "task_pair" / "paper_reproduction" / "task.md"
        task.write_text("# changed scientific objective\n", encoding="utf-8")
        return {
            "status": "repaired",
            "changed_files": ["paper_reproduction/task.md"],
            "findings_before": ["evaluator_binding_field_missing:ap_x"],
            "findings_after": [],
            "science_hash_before": before,
            "science_hash_after": "",
            "summary": "fixture mutation",
        }

    report = run_stage07b_repair(
        harness=_FakeHarness(mutate_science),
        stage_root=tmp_path / "stage",
        paper_id="paper_fixture",
        task_pair_id="paper_fixture_task_pair",
        audited_root=pair,
        findings=["evaluator_binding_field_missing:ap_x"],
        config={"stage07b_enabled": True},
    )
    assert report["status"] == "technical_blocked"
    assert report["reason"] == "science_fingerprint_changed"
    assert science_fingerprint(pair) == before
    assert (pair / "paper_reproduction" / "task.md").read_text(encoding="utf-8").startswith(
        "# paper_reproduction"
    )


def test_stage07b_freezes_task_type_and_process_key_point_content(tmp_path: Path):
    pair = _pair(tmp_path)
    info = pair / "paper_reproduction" / "task_info.json"
    info.write_text(
        json.dumps({"task_id": "paper_reproduction", "task_type": "paper_reproduction"})
        + "\n",
        encoding="utf-8",
    )
    before = science_fingerprint(pair)

    def mutate_semantics(request):
        changed = request.workspace / "outputs" / "task_pair" / "paper_reproduction" / "task_info.json"
        changed.write_text(
            json.dumps({"task_id": "paper_reproduction", "task_type": "autonomous_research"})
            + "\n",
            encoding="utf-8",
        )
        return {
            "status": "repaired",
            "changed_files": ["paper_reproduction/task_info.json"],
            "findings_before": ["evaluator_binding_field_missing:ap_x"],
            "findings_after": [],
            "science_hash_before": before,
            "summary": "fixture semantic mutation",
        }

    report = run_stage07b_repair(
        harness=_FakeHarness(mutate_semantics),
        stage_root=tmp_path / "stage",
        paper_id="paper_fixture",
        task_pair_id="paper_fixture_task_pair",
        audited_root=pair,
        findings=["evaluator_binding_field_missing:ap_x"],
        config={"stage07b_enabled": True},
    )
    assert report["status"] == "technical_blocked"
    assert report["reason"] == "science_fingerprint_changed"
    assert science_fingerprint(pair) == before


def test_stage07b_freezes_answers_but_allows_binding_transport_projection(tmp_path: Path):
    pair = _pair(tmp_path)
    hidden_path = pair / "hidden_reference" / "ground_truth_common.json"
    hidden_path.write_text(
        json.dumps(
            {
                "task_pair_id": "old",
                "ground_truth_items": [{"ground_truth_id": "answer", "canonical_answer": 4}],
                "acceptance_profiles": [
                    {
                        "acceptance_profile_id": "profile",
                        "ground_truth_id": "answer",
                        "canonical_value": 4,
                        "submission_binding": {
                            "observed_fields": ["$.old"],
                            "canonical_projection": 4,
                        },
                    }
                ],
            }
        )
        + "\n",
        encoding="utf-8",
    )
    before = science_fingerprint(pair)
    hidden = json.loads(hidden_path.read_text(encoding="utf-8"))
    hidden["task_pair_id"] = "new"
    hidden["acceptance_profiles"][0]["submission_binding"]["observed_fields"] = ["$.new"]
    hidden["acceptance_profiles"][0]["submission_binding"]["canonical_projection"] = 99
    hidden_path.write_text(json.dumps(hidden) + "\n", encoding="utf-8")
    assert science_fingerprint(pair) == before
    hidden["ground_truth_items"][0]["canonical_answer"] = 5
    hidden_path.write_text(json.dumps(hidden) + "\n", encoding="utf-8")
    assert science_fingerprint(pair) != before


def test_stage07b_disabled_is_explicit(tmp_path: Path):
    pair = _pair(tmp_path)
    harness = _FakeHarness(lambda _request: {"status": "repaired"})
    report = run_stage07b_repair(
        harness=harness,
        stage_root=tmp_path / "stage",
        paper_id="paper_fixture",
        task_pair_id="paper_fixture_task_pair",
        audited_root=pair,
        findings=["evaluator_binding_field_missing:ap_x"],
        config={"stage07b_enabled": False},
    )
    assert report["status"] == "disabled"
    assert harness.calls == 0
