import json
import shutil

from evaluation.provenance.agent_events import load_agent_events
from evaluation.provenance.evidence_archive import build_run_index, export_run_archive, open_archive, resolve_reference
from evaluation.scoring.evidence_reading import read_registered_evidence
from test_evidence_archive import saved_run


def test_portable_events_instructions_and_artifact_aliases(tmp_path):
    root = saved_run(tmp_path)
    (root / "INSTRUCTIONS.md").write_text("Public instructions")
    (root / "_toolbox_catalog.json").write_text('{"version":1}')
    event = {"type": "item.completed", "item": {"type": "command_execution", "id": "i", "status": "completed",
        "command": "inspect --header 'Bearer example-secret'", "aggregated_output": "result", "exit_code": 0}}
    (root / "_agent_output.jsonl").write_text(json.dumps(event) + "\n")
    (root / "_tool_artifacts").mkdir()
    (root / "_tool_artifacts/index.jsonl").write_text(json.dumps({"artifact_id": "art_test", "path": "outputs/execution_jobs/job_example/input.xyz", "semantic_type": "AtomicStructure"}) + "\n")
    index = build_run_index(root)
    assert resolve_reference(index, "art_test").name == "input.xyz"
    before = (root / "_agent_output.jsonl").read_bytes()
    exported = export_run_archive(root, tmp_path / "portable")
    assert (root / "_agent_output.jsonl").read_bytes() == before
    shutil.rmtree(root)
    portable = open_archive(tmp_path / "portable")
    assert portable["verification"]["state"] == "complete"
    events = load_agent_events(tmp_path / "portable/workspace")
    assert len(events) == 1 and events[0]["tool"] == "shell"
    assert "example-secret" not in json.dumps(events)
    assert "Public instructions" in resolve_reference(portable, "workspace/INSTRUCTIONS.md").read_text()
    assert "He 0 0 0" in read_registered_evidence(portable, {"ref": "art_test"})["content"]
    assert exported["process_evidence"]["capture"]["completed_native_call_count"] == 1


def test_valid_directory_output_uses_same_public_validator(tmp_path):
    from chemistry_toolbox.src.output_contract import validate_output_contract
    (tmp_path / "report/structures").mkdir(parents=True)
    (tmp_path / "report/structures/a.xyz").write_text("1\n\nHe 0 0 0\n")
    contract = json.dumps({"required_files": ["report", "report/structures"]}).encode()
    assert validate_output_contract(tmp_path, contract)["valid"]
