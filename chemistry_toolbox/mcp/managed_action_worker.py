"""Run an Action under the same supervisor/reservation as native jobs."""
import json
import os
import sys
from pathlib import Path

from chemistry_toolbox.src.recovery_io import atomic_json, file_hash
from chemistry_toolbox.src.artifacts import ArtifactStore, collect_artifact_refs
from .execution_store import ExecutionStore


def restore_input_artifacts(spec: dict, workspace: Path) -> None:
    """Verify frozen files and register only the declared input references."""
    for item in spec.get("frozen_inputs", []):
        if file_hash(workspace / item["target_path"]) != item["sha256"]:
            raise ValueError("Action input snapshot mismatch")
    # Historical specs have full refs in the request but no explicit manifest.
    references = spec.get("input_artifacts")
    if references is None:
        references = collect_artifact_refs(spec.get("action_request", {}).get("inputs", {}))
    artifacts = ArtifactStore(workspace)
    for reference in references:
        artifacts.import_reference(reference)


def _execute(store, launch, spec, workspace):
    os.environ["RESEARCHCHEMBENCH_ELECTRONIC_STATE_POLICY"] = spec.get("electronic_state_policy", "legacy")
    os.environ["RESEARCHCHEMBENCH_WORKSPACE"] = str(workspace)
    os.environ["RESEARCHCHEM_MCP_WORKSPACE"] = str(workspace)
    restore_input_artifacts(spec, workspace)
    from chemistry_toolbox.src.service import execute_action
    result = execute_action(spec["action_id"], spec["action_request"], _managed_allocation=launch["resource_allocation"])
    input_references = {ref.artifact_id: ref.model_dump(mode="json")
                        for ref in collect_artifact_refs(spec["action_request"]["inputs"])}
    prefix = str(workspace.relative_to(store.root))
    def relocate(value):
        if isinstance(value, dict):
            # Input refs are already relative to the run workspace. Only new
            # outputs are exported from the job workspace; re-prefixing an
            # input ref would change the identity's canonical path on return.
            if value.get("artifact_id") in input_references and "path" in value:
                original = input_references[value["artifact_id"]]
                if value != original:
                    raise ValueError(f"Artifact reference conflict: {value['artifact_id']}")
                return original
            return {k: relocate(v) for k, v in value.items()}
        if isinstance(value, list): return [relocate(v) for v in value]
        if isinstance(value, str) and len(value) < 4096:
            try:
                candidate = (workspace / value).resolve()
                if candidate.is_relative_to(workspace) and candidate.is_file():
                    return prefix + "/" + str(candidate.relative_to(workspace))
            except (OSError, ValueError): pass
        return value
    result = relocate(result)
    artifacts = ArtifactStore(store.root)
    for reference in result.get("output_artifacts", []):
        artifacts.import_reference(reference)
    return result


def main(control: Path, job_id: str):
    launch = json.loads((control / "launches" / (job_id + ".json")).read_text())
    store = ExecutionStore(Path(launch["workspace"]), run_id=launch["run_id"])
    spec = store.spec(job_id)
    try:
        result = _execute(store, launch, spec, Path(launch["job_directory"]))
    except Exception as exc:
        import traceback
        result = {"status": "failed", "action": spec["action_id"], "action_version": "unknown",
                  "requested_backend": spec["action_request"].get("backend_id"),
                  "backend": spec["action_request"].get("backend_id"), "selection_source": "agent",
                  "error": {"code": "managed_action_worker_error", "failure_stage": "action_worker",
                            "message": f"{type(exc).__name__}: {exc}", "traceback": traceback.format_exc()},
                  "warnings": [], "provenance": {}, "input_artifacts": [], "output_artifacts": [], "retryable": False}
    from .action_result_io import save_action_result
    save_action_result(store, job_id, launch.get("launch_token"), result)
    return 0 if result.get("status") in {"success", "partial_success"} else 1


if __name__ == "__main__":
    raise SystemExit(main(Path(sys.argv[1]), sys.argv[2]))
