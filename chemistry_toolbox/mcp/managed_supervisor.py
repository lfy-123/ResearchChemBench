"""One-shot launch claim. It survives manager and MCP disconnection."""
import json
import os
import sys
from pathlib import Path

from chemistry_toolbox.src.recovery_io import atomic_json, file_lock, process_identity
from .execution_store import ExecutionStore
from .job_supervisor import supervise


def main(spec_path):
    spec = json.loads(spec_path.read_text())
    store = ExecutionStore(Path(spec["workspace"]), run_id=spec["run_id"])
    job_id = spec["job_id"]
    with file_lock(store.directory / "claims" / (job_id + ".lock"), blocking=False):
        if store.get_record("launch_claim", job_id):
            return 75
        identity = process_identity(os.getpid())
        for _ in range(3):
            row = store.get_job(job_id)
            facts = json.loads(row["state_json"])
            if facts.get("launch_token") != spec["launch_token"]:
                return 75
            if row["state"] == "cancel_requested":
                state = "timeout" if facts.get("cancel_reason") == "deadline" else "cancelled"
                terminal = {"status": state, "job_id": job_id, "launch_token": spec["launch_token"], "reason": "cancelled_before_child_launch"}
                atomic_json(store.directory / "terminal" / (job_id + ".json"), terminal)
                atomic_json(Path(spec["status_path"]), terminal)
                store.record_job_state(job_id, state, expected_snapshot=row, state_payload={"status": terminal})
                return 0
            if row["state"] == "running" and facts.get("supervisor_identity") == identity:
                return supervise(spec_path)
            recoverable = row["state"] == "needs_reconciliation" and facts.get("reason") == "owner_unverified" and not facts.get("cancel_reason") and not (facts.get("status") or {}).get("error")
            if row["state"] != "launching" and not recoverable:
                return 75
            store.put_record("launch_claim", job_id, {"launch_token": spec["launch_token"], "identity": identity}, immutable=True)
            registered = store.record_job_state(job_id, "running", expected_snapshot=row,
                state_payload={"supervisor_identity": identity, "reason": None, "survivors": []})
            if registered.get("supervisor_identity") == identity and registered["state"] == "running":
                return supervise(spec_path)
        return 75


if __name__ == "__main__":
    raise SystemExit(main(Path(sys.argv[1])))
