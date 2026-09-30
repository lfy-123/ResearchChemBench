"""Cross-process input handoffs without invoking a scientific executable."""
import json
import os
import shutil
import subprocess
import sys
import threading
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest

from chemistry_toolbox.mcp.execution_store import ExecutionStore
from chemistry_toolbox.mcp.managed_execution import freeze_action_inputs
from chemistry_toolbox.mcp.managed_action_worker import restore_input_artifacts
from chemistry_toolbox.src.artifacts import ArtifactStore
from chemistry_toolbox.src.backends.common import structure_dict


STRUCTURE = {"atoms": [{"element": "H", "position_angstrom": [0, 0, 0]}]}


def process(root, code):
    env = {**os.environ, "RESEARCHCHEM_MCP_WORKSPACE": str(root),
           "RESEARCHCHEMBENCH_WORKSPACE": str(root),
           "PYTHONPATH": str(Path(__file__).resolve().parents[2])}
    result = subprocess.run([sys.executable, "-c", code], cwd=root, env=env,
                            text=True, capture_output=True, timeout=15)
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


@pytest.mark.parametrize("compact", [False, True])
def test_three_process_chain_preserves_ids_hashes_and_lineage(tmp_path, monkeypatch, compact):
    monkeypatch.setenv("RESEARCHCHEM_MCP_WORKSPACE", str(tmp_path))
    ref = process(tmp_path, '''
import json
from chemistry_toolbox.src.artifacts import ArtifactStore
s = ArtifactStore()
s.put_json({}, semantic_type="Unrelated", producer_action="fixture", producer_backend=None)
ref = s.put_json({"atoms":[{"element":"H","position_angstrom":[0,0,0]}]},
    semantic_type="AtomicStructure", producer_action="fixture_a", producer_backend=None)
print(ref.model_dump_json())
''')
    run_store = ExecutionStore(tmp_path, run_id="chain")
    for label in ("b", "c"):
        supplied = {"artifact_id": ref["artifact_id"]} if compact else ref
        inputs, frozen, _ = freeze_action_inputs(run_store, {"structure": supplied})
        workspace = tmp_path / "outputs" / label
        workspace.mkdir(parents=True)
        for item in frozen:
            target = workspace / item["target_path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(item["snapshot_path"], target)
        spec = {"frozen_inputs": frozen, "action_request": {"inputs": inputs},
                "input_artifacts": [inputs["structure"]]}
        (workspace / "spec.json").write_text(json.dumps(spec))
        new_ref = process(workspace, '''
import json
from pathlib import Path
from chemistry_toolbox.mcp.managed_action_worker import restore_input_artifacts
from chemistry_toolbox.src.artifacts import ArtifactStore
from chemistry_toolbox.src.backends.common import structure_dict
spec = json.loads(Path("spec.json").read_text())
restore_input_artifacts(spec, Path.cwd())
restore_input_artifacts(spec, Path.cwd()) # resume must be idempotent
ref = spec["input_artifacts"][0]
assert len(Path("_tool_artifacts/index.jsonl").read_text().splitlines()) == 1
assert ArtifactStore().find(ref["artifact_id"]).model_dump(mode="json") == ref
assert structure_dict(ref) == structure_dict({"artifact_id":ref["artifact_id"]}) == structure_dict(ref["artifact_id"])
out = ArtifactStore().put_json(structure_dict(ref), semantic_type="AtomicStructure",
    producer_action="fixture_transform", producer_backend=None, parent_artifact_ids=[ref["artifact_id"]])
print(out.model_dump_json())
''')
        assert new_ref["parent_artifact_ids"] == [ref["artifact_id"]]
        assert new_ref["sha256"] == ref["sha256"]
        new_ref["path"] = str(workspace.relative_to(tmp_path)) + "/" + new_ref["path"]
        ArtifactStore(tmp_path).import_reference(new_ref)
        ref = new_ref
    assert ArtifactStore().load(ref) == STRUCTURE


def test_full_reference_works_without_local_index_and_rejects_conflicts(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEM_MCP_WORKSPACE", str(tmp_path))
    store = ArtifactStore()
    ref = store.put_json(STRUCTURE, semantic_type="AtomicStructure", producer_action="fixture", producer_backend=None)
    store.index_path.unlink()
    assert structure_dict(ref.model_dump()) == STRUCTURE
    store.import_reference(ref)
    store.import_reference(ref)
    assert len(store.index_path.read_text().splitlines()) == 1
    conflicting = ref.model_copy(update={"producer_action": "other"})
    with pytest.raises(ValueError, match="reference conflict"):
        store.import_reference(conflicting)
    with pytest.raises(ValueError, match="reference conflict"):
        store.load(conflicting)
    (tmp_path / ref.path).write_text('{}')
    with pytest.raises(ValueError, match="hash mismatch"):
        store.load(ref)
    with pytest.raises(ValueError, match="hash mismatch"):
        freeze_action_inputs(ExecutionStore(tmp_path, run_id="tamper"), {"structure": ref})


def test_worker_verifies_copy_and_can_restore_historical_spec(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEM_MCP_WORKSPACE", str(tmp_path))
    store = ArtifactStore()
    ref = store.put_json(STRUCTURE, semantic_type="AtomicStructure", producer_action="fixture", producer_backend=None)
    spec = {"action_request": {"inputs": {"structure": ref.model_dump()}},
            "frozen_inputs": [{"target_path": ref.path, "sha256": ref.sha256}]}
    store.index_path.unlink()
    restore_input_artifacts(spec, tmp_path)
    assert store.find(ref.artifact_id) == ref
    (tmp_path / ref.path).write_text('{}')
    with pytest.raises(ValueError, match="snapshot mismatch"):
        restore_input_artifacts(spec, tmp_path)


def test_import_rejects_workspace_escape(tmp_path):
    root = tmp_path / "job"
    root.mkdir()
    external = tmp_path / "external.json"
    external.write_text('{}')
    from chemistry_toolbox.src.recovery_io import file_hash
    ref = {"artifact_id":"art_" + "a"*32, "semantic_type":"AtomicStructure",
           "media_type":"application/json", "sha256":file_hash(external),
           "path":"../external.json", "producer_action":"fixture"}
    with pytest.raises(ValueError, match="escapes workspace"):
        ArtifactStore(root).import_reference(ref)


def test_real_managed_worker_exports_new_outputs_without_rebasing_inputs(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEM_MCP_WORKSPACE", str(tmp_path))
    from chemistry_toolbox.src.recovery_io import atomic_json
    artifacts = ArtifactStore(tmp_path)
    original = artifacts.put_json(STRUCTURE, semantic_type="AtomicStructure", producer_action="fixture", producer_backend=None)
    store = ExecutionStore(tmp_path, run_id="worker")
    inputs, frozen, manifest = freeze_action_inputs(store, {"structure": original.artifact_id})
    spec = {"action_id":"fixture", "action_request":{"inputs":inputs},
            "input_artifacts":[original.model_dump()], "frozen_inputs":frozen}
    receipt = store.accept_submission(submission_key="child", entity_type="job", request={}, spec=spec, input_manifest=manifest)
    workspace = tmp_path/"outputs/execution_jobs"/receipt.entity_id
    for item in frozen:
        target = workspace/item["target_path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(item["snapshot_path"], target)
    atomic_json(store.directory/"launches"/(receipt.entity_id+'.json'), {
        "workspace":str(tmp_path),"run_id":"worker","job_directory":str(workspace),"resource_allocation":{},
    })
    result = process(tmp_path, f'''
import json
from pathlib import Path
from chemistry_toolbox.src import service
from chemistry_toolbox.src.artifacts import ArtifactStore
from chemistry_toolbox.src.backends.common import structure_dict
from chemistry_toolbox.mcp.managed_action_worker import main
def fixture(action, request, **kwargs):
    ref = request["inputs"]["structure"]
    out = ArtifactStore().put_json(structure_dict(ref), semantic_type="AtomicStructure",
        producer_action="fixture_output", producer_backend=None, parent_artifact_ids=[ref["artifact_id"]])
    return {{"status":"success","input_artifacts":[ref],"output_artifacts":[out.model_dump(mode="json")]}}
service.execute_action = fixture
control = Path({str(store.directory)!r})
assert main(control, {receipt.entity_id!r}) == 0
print((control/"action_results"/{(receipt.entity_id+'.json')!r}).read_text())
''')
    assert result["input_artifacts"] == [original.model_dump(mode="json")]
    output = result["output_artifacts"][0]
    assert output["path"].startswith(f"outputs/execution_jobs/{receipt.entity_id}/")
    assert artifacts.load(output) == STRUCTURE
    assert artifacts.find(original.artifact_id) == original


def test_reader_waits_for_complete_index_append_and_duplicate_import_is_atomic(tmp_path):
    from chemistry_toolbox.src.recovery_io import file_lock
    store = ArtifactStore(tmp_path)
    ref = store.put_json(STRUCTURE, semantic_type="AtomicStructure", producer_action="fixture", producer_backend=None)
    with ThreadPoolExecutor(4) as pool:
        assert all(value == ref for value in pool.map(store.import_reference, [ref] * 8))
        assert len(store.index_path.read_text().splitlines()) == 1
        started = threading.Event()
        def read():
            started.set()
            return store.find(ref.artifact_id)
        with file_lock(store.index_path.with_suffix('.lock')):
            store.index_path.write_text('{"artifact_id":')
            reading = pool.submit(read)
            assert started.wait(2)
            assert not reading.done()
            store.index_path.write_text(ref.model_dump_json()+'\n')
        assert reading.result(timeout=3) == ref
