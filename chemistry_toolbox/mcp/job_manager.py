"""Independent local queue dispatcher and conservative process reconciliation."""
from __future__ import annotations

from chemistry_toolbox.src.execution_states import TERMINAL_STATES, ACTIVE_STATES, aggregate_outcomes

import json
import hashlib
import os
import shutil
import signal
import socket
import subprocess
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

from chemistry_toolbox.src.paths import PROJECT_ROOT
from chemistry_toolbox.src.recovery_io import atomic_json, file_hash, file_lock, process_identity, signal_identity, token_processes
from chemistry_toolbox.src.resource_budget import ResourceBudgetExceeded, reserve_resources
from .execution_store import ExecutionStore, canonical_json



class JobManager:
    def __init__(self, workspace: Path, *, run_id: str):
        self.workspace = Path(workspace).resolve()
        self.run_id = run_id
        self.store = ExecutionStore(self.workspace, run_id=run_id)
        self.children = []

    def _directory(self, entity_id):
        return self.workspace / "outputs" / "execution_jobs" / entity_id

    def _configure(self):
        config = self.store.get_record("manager", "config", {})
        os.environ.update(config.get("environment", {}))
        os.environ["RESEARCHCHEMBENCH_WORKSPACE"] = str(self.workspace)
        os.environ["RESEARCHCHEM_MCP_WORKSPACE"] = str(self.workspace)
        os.environ["RESEARCHCHEMBENCH_RUN_ID"] = self.run_id

    def _prepare(self, job_id, spec, allocation, token):
        from .open_execution import _job_environment, JOB_CONTEXT_PATH
        directory = self._directory(job_id)
        directory.mkdir(parents=True, exist_ok=True)
        for name in ("code", "inputs", "outputs", "report", "logs"):
            (directory / name).mkdir(exist_ok=True)
        for item in spec.get("frozen_inputs", []):
            snapshot = Path(item["snapshot_path"])
            if file_hash(snapshot) != item["sha256"]:
                raise ValueError("input snapshot was modified")
            target = directory / item["target_path"]
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(snapshot, target)
            if file_hash(target) != item["sha256"]:
                raise ValueError("input snapshot copy mismatch")
        metadata = {**spec.get("metadata", {}), "recovery_managed": True}
        if spec["job_type"] == "programmable_analysis":
            shutil.copyfile(JOB_CONTEXT_PATH, directory / "researchchem_job.py")
            atomic_json(directory / "analysis_contract.json", metadata.get("analysis_contract", {}))
        command = spec["command"]
        if spec["job_type"] == "predefined_action":
            command = [sys.executable, "-m", "chemistry_toolbox.mcp.managed_action_worker", str(self.store.directory), job_id]
            catalog = self.workspace / "_toolbox_catalog.json"
            if catalog.is_file():
                shutil.copyfile(catalog, directory / catalog.name)
        relative = str(directory.relative_to(self.workspace))
        value = {**spec, "job_id": job_id, "command": command, "metadata": metadata,
                 "job_directory": str(directory), "relative_job_directory": relative,
                 "resource_allocation": allocation, "evaluation_resource_budget": spec["budget"],
                 "submitted_at": datetime.now(timezone.utc).isoformat(), "launch_token": token,
                 "recovery_managed": True, "run_id": self.run_id, "workspace": str(self.workspace),
                 "staged_inputs": spec.get("frozen_inputs", []),
                 "stdin_path": str(directory / spec["stdin_target"]) if spec.get("stdin_target") else None}
        for kind in ("status", "stdout", "stderr"):
            filename = "status.json" if kind == "status" else kind + ".log"
            value[kind + "_path"] = str(directory / filename)
            value["relative_" + kind + "_path"] = relative + "/" + filename
        atomic_json(directory / "request.json", value)
        spec_path = self.store.directory / "launches" / (job_id + ".json")
        atomic_json(spec_path, value)
        environment = _job_environment(spec["runtime"], job_id, directory, spec["resource_limits"], allocation,
                                       job_type=spec["job_type"], software_id=metadata.get("software_id"))
        environment.update(self.store.get_record("manager", "config", {}).get("environment", {}))
        environment.update({"PYTHONPATH": str(directory) + os.pathsep + str(PROJECT_ROOT), "RCB_JOB_LAUNCH_TOKEN": token,
                            "RESEARCHCHEMBENCH_WORKSPACE": str(self.workspace), "RESEARCHCHEMBENCH_RUN_ID": self.run_id})
        return spec_path, environment

    def _dispatch(self, job):
        job_id = job["entity_id"]
        spec = self.store.spec(job_id)
        if spec is None:
            self.store.record_job_state(job_id, "needs_reconciliation", state_payload={"reason": "legacy_submission_has_no_durable_spec"})
            return
        if spec["job_type"] == "batch":
            self._batch(job, spec)
            return
        parent = spec.get("parent_batch")
        if parent:
            parent_spec = self.store.spec(parent)
            running = sum(self.store.spec(j["entity_id"]).get("parent_batch") == parent and j["state"] in {"launching", "running", "needs_reconciliation"}
                          for j in self.store.list_jobs() if self.store.spec(j["entity_id"]))
            if running >= (parent_spec.get("max_concurrency") or 32):
                return
        try:
            reservation = reserve_resources(spec["resource_limits"], kind=spec["job_type"], label=job_id,
                                             owner_id=self.run_id + "/" + job_id)
        except ResourceBudgetExceeded:
            return  # Accepted work remains in the durable queue.
        token = uuid.uuid4().hex
        # Reservation precedes intent; a crash in between reuses this same
        # reservation. Any crash after intent requires reconciliation.
        intent = self.store.record_job_state(job_id, "launching", event_type="launch_intent", expected_state="queued", state_payload={
            "launch_token": token, "launch_time": time.time(), "reservation_path": str(reservation.path),
            "resource_allocation": reservation.resource_allocation})
        if intent.get("launch_token") != token:
            if intent["state"] in TERMINAL_STATES:
                reservation.release()
            return
        try:
            path, environment = self._prepare(job_id, spec, reservation.resource_allocation, token)
            log = self.store.directory / "supervisor.log"
            with log.open("ab") as handle:
                child = subprocess.Popen([sys.executable, "-m", "chemistry_toolbox.mcp.managed_supervisor", str(path)],
                                         cwd=PROJECT_ROOT, stdin=subprocess.DEVNULL, stdout=handle, stderr=handle,
                                         env=environment, start_new_session=True, close_fds=True)
            self.children.append(child)
        except Exception as exc:
            self.store.record_job_state(job_id, "needs_reconciliation", state_payload={"reason": "launch_exception", "error": str(exc)})

    def _batch(self, job, spec):
        with file_lock(self.store.directory / "batches" / (job["entity_id"] + ".lock")):
            return self._update_batch(job, spec)

    def _update_batch(self, job, spec):
        batch_id = job["entity_id"]
        job = self.store.get_job(batch_id)
        mapping = {}
        for index, child in enumerate(spec["children"]):
            child_spec = {**child["spec"], "parent_batch": batch_id, "budget": spec["budget"], "run_deadline": spec.get("run_deadline")}
            receipt = self.store.accept_submission(submission_key=batch_id + ":" + str(index), entity_type="job",
                request={"batch_id": batch_id, "item_id": child["item_id"]}, spec=child_spec)
            mapping[child["item_id"]] = receipt.entity_id
        self.store.put_record("batch_items", batch_id, mapping, immutable=True)
        if job["state"] == "queued":
            self.store.record_job_state(batch_id, "running")
        from .result_transport import compact_action_result
        rows, events = [], []
        history = self.store.get_record("batch_feedback_events", batch_id)
        if history is None:
            # Preserve existing event sequence numbers on upgrade.
            old_path = self.workspace / "outputs" / "action_batches" / batch_id / "status.json"
            try: history = json.loads(old_path.read_text()).get("events", [])
            except (OSError, ValueError): history = []
        for index, (item_id, job_id) in enumerate(mapping.items()):
            row = self.store.get_job(job_id)
            result = self.store.get_record("result", job_id)
            raw = (result or {}).get("action_result")
            public = compact_action_result(raw, full_result_ref=result.get("full_result_ref")) if raw else result
            feedback = (public or {}).get("execution_feedback")
            if feedback:
                from chemistry_toolbox.src.execution_feedback import execution_feedback
                facts = json.loads(row["state_json"])
                feedback = execution_feedback(status={**facts.get("status", {}), "job_id": job_id, "status": row["state"]}, action_result=raw, record=result)
                public = {**public, "execution_feedback": feedback}
            rows.append({"item_id": item_id, "job_id": job_id, "batch_index": index, "status": row["state"], "result": public, "execution_feedback": feedback, "resource_limits": self.store.spec(job_id).get("resource_limits", {})})
            if row["state"] in TERMINAL_STATES:
                prior = [e for e in history if e.get("item_id") == item_id]
                receipt = (result or {}).get("result_receipt_id")
                if not prior or prior[-1].get("result_receipt_id") != receipt:
                    history.append({"sequence": len(history) + 1, "type": "result_updated" if prior else "item_finished",
                                    "item_id": item_id, "job_id": job_id, "status": row["state"], "result": public,
                                    "execution_feedback": feedback, "result_receipt_id": receipt})
                event = self.store.put_record("batch_event", batch_id + ":" + item_id, {
                    "item_id": item_id, "job_id": job_id, "status": row["state"], "result": public}, immutable=True)
                events.append(event)
        state = "running"
        if all(r["status"] in TERMINAL_STATES for r in rows):
            state = job["state"] if job["state"] in TERMINAL_STATES else aggregate_outcomes(r["status"] for r in rows)
            if job["state"] == "cancel_requested":
                state = "timeout" if json.loads(job["state_json"]).get("cancel_reason") == "deadline" else "cancelled"
            self.store.record_job_state(batch_id, state)
        directory = self.workspace / "outputs" / "action_batches" / batch_id
        # Sequence is assigned once on completion; restarts never renumber events.
        sequence_map = self.store.get_record("batch_sequences", batch_id, [])
        for event in events:
            if event["job_id"] not in sequence_map: sequence_map.append(event["job_id"])
        self.store.put_record("batch_sequences", batch_id, sequence_map)
        self.store.put_record("batch_feedback_events", batch_id, history)
        numbered = history
        atomic_json(directory / "status.json", {"batch_id": batch_id, "status": state, "items": rows, "events": numbered, "last_sequence": len(numbered), "execution_mode": "local", "recovery_managed": True})
        temporary = directory / "events.jsonl.tmp"
        temporary.write_text("".join(json.dumps(event) + "\n" for event in numbered))
        os.replace(temporary, directory / "events.jsonl")

    def _index_result(self, job_id):
        from .action_result_io import read_action_result
        from chemistry_toolbox.src.execution_feedback import preserve_result
        with file_lock(self.store.directory / "result_locks" / (job_id + ".lock")):
            old = self.store.get_record("result", job_id) or {}
            spec = self.store.spec(job_id) or {}
            action_job = spec.get("job_type") == "predefined_action"
            if old.get("result_state") in {"indexed", "ready"} and (not action_job or old.get("action_result")):
                return old
            action, problem = read_action_result(self.store, job_id) if action_job else (None, None)
            signature = hashlib.sha256(canonical_json({"action": action, "problem": problem}).encode()).hexdigest()
            if old.get("source_signature") == signature and (old.get("result_diagnostic") or {}).get("code") != "result_index_error":
                return old
            files = old.get("artifact_manifest", [])
            reference = None
            try:
                if not old or (old.get("result_diagnostic") or {}).get("code") == "result_index_error":
                    directory = self._directory(job_id)
                    files = [{"path": str(p.relative_to(self.workspace)), "sha256": file_hash(p), "size_bytes": p.stat().st_size}
                             for p in sorted(directory.rglob("*")) if p.is_file() and not p.is_symlink() and not any(part.startswith(".") for part in p.relative_to(directory).parts)]
                if action: reference = preserve_result(action, self.workspace)
            except (OSError, ValueError) as exc:
                problem = {"code": "result_index_error", "category": "result_delivery", "message": str(exc)}
            revision = int(old.get("terminal_revision", 0)) + 1
            result = {"job_id": job_id, "terminal_revision": revision, "result_receipt_id": "result_" + uuid.uuid4().hex,
                      "artifact_manifest": files, "artifact_manifest_hash": hashlib.sha256(canonical_json(files).encode()).hexdigest(),
                      "result_state": "ready" if problem is None else "missing" if problem["code"] == "result_missing" else "corrupt",
                      "result_diagnostic": problem, "source_signature": signature, "full_result_ref": reference}
            if action: result["action_result"] = action
            self.store.put_record("result_revision", job_id + ":" + str(revision), result, immutable=True)
            self.store.put_record("result", job_id, result)
            return result

    def reconcile_job(self, job_id):
        # Inspect a fresh row, then compare the complete snapshot inside the
        # write transaction. A supervisor may register or finish during /proc IO.
        job = self.store.get_job(job_id)
        if job is None or job["state"] in TERMINAL_STATES:
            return job
        facts = json.loads(job["state_json"])
        state, payload = job["state"], None
        blocked_state = "cancel_requested" if state == "cancel_requested" else "needs_reconciliation"
        if self.store.spec(job_id) is None:
            payload = {"reason": "legacy_submission_has_no_durable_spec"}
            state = blocked_state
        elif job["entity_type"] != "batch" and state in {"launching", "running", "needs_reconciliation", "cancel_requested"}:
            token = facts.get("launch_token")
            terminal_path = self.store.directory / "terminal" / (job_id + ".json")
            if terminal_path.is_file():
                try:
                    terminal = json.loads(terminal_path.read_text())
                    if not isinstance(terminal, dict) or terminal.get("status") not in TERMINAL_STATES:
                        raise ValueError("Invalid terminal record")
                    if not token or terminal.get("launch_token") != token or terminal.get("job_id") != job_id:
                        raise ValueError("Terminal record does not match the original job and launch token")
                    state, payload = terminal["status"], {"status": terminal}
                except (OSError, ValueError) as exc:
                    state, payload = blocked_state, {"reason": "terminal_record_invalid", "error": str(exc)}
            else:
                claim = self.store.get_record("launch_claim", job_id, {})
                identity = claim.get("identity") or {}
                recorded = facts.get("supervisor_identity") or {}
                matching_claim = bool(token and claim.get("launch_token") == token)
                matching_identity = not recorded or all(recorded.get(key) == identity.get(key)
                    for key in ("host", "boot_id", "pid", "start_ticks"))
                owner = process_identity(identity.get("pid"), {**identity, "launch_token": token}) if matching_claim and matching_identity else {}
                if claim and (not matching_claim or not matching_identity):
                    state, payload = blocked_state, {"reason": "launch_identity_mismatch"}
                elif owner.get("verified"):
                    if state == "needs_reconciliation" and facts.get("reason") == "owner_unverified" and not facts.get("cancel_reason") and not (facts.get("status") or {}).get("error"):
                        state, payload = "running", {"reason": None, "survivors": [], "supervisor_identity": identity}
                elif time.time() - facts.get("launch_time", 0) > 5:
                    if state != "needs_reconciliation" or facts.get("reason") == "owner_unverified":
                        state, payload = blocked_state, {"reason": "owner_unverified", "owner_diagnostic": owner.get("reason"),
                            "survivors": token_processes(token) if token else []}
        if payload is not None:
            self.store.record_job_state(job_id, state, expected_snapshot=job,
                                        state_payload={**payload, "automatic_restart": False})
        return self.store.get_job(job_id)

    def reconcile(self):
        results = []
        for snapshot in self.store.list_jobs():
            job_id = snapshot["entity_id"]
            job = self.reconcile_job(job_id)
            state = job["state"]
            if state in TERMINAL_STATES:
                if job["entity_type"] != "batch":
                    self._index_result(job_id)
                reservation = json.loads(job["state_json"]).get("reservation_path")
                if reservation: Path(reservation).unlink(missing_ok=True)
            results.append({"entity_id": job_id, "state": state, "automatic_restart": False})
        for row in self.store.list_jobs():
            if row["entity_type"] == "batch" and self.store.spec(row["entity_id"]):
                self._batch(row, self.store.spec(row["entity_id"]))
        return {"status": "success", "run_id": self.run_id, "automatic_restarts": 0, "results": results, "summary": {
            "total": len(results), "active": sum(r["state"] in ACTIVE_STATES for r in results),
            "terminal": sum(r["state"] in TERMINAL_STATES for r in results),
            "needs_reconciliation": sum(r["state"] == "needs_reconciliation" for r in results)}}

    def cancel_entity(self, entity_id, entity_type="job", *, reason="cancel"):
        row = self.store.get_job(entity_id)
        if row is None: return {"status": "recovery_blocked", "reason": "unknown_job"}
        if row["state"] in TERMINAL_STATES: return {"status": "success", "already_terminal": True}
        spec = self.store.spec(entity_id)
        if entity_type == "batch":
            if spec: self._batch(row, spec)
            for child in self.store.get_record("batch_items", entity_id, {}).values():
                self.cancel_entity(child, reason=reason)
            self.store.record_job_state(entity_id, "cancel_requested", state_payload={"cancel_reason": reason})
            return {"status": "success", "entity_id": entity_id}
        if row["state"] in {"accepted", "queued"}:
            self.store.record_job_state(entity_id, "timeout" if reason == "deadline" else "cancelled")
            return {"status": "success", "entity_id": entity_id}
        facts = json.loads(row["state_json"])
        atomic_json(self._directory(entity_id) / "cancel_requested", {"reason": reason})
        identity = facts.get("supervisor_identity", {})
        signalled = False
        if process_identity(identity.get("pid"), identity).get("verified"):
            signalled = signal_identity(identity)
        elif facts.get("launch_token"):
            # Unknown owner: stop only independently identified surviving
            # descendants. Keep the reservation until their absence is proven.
            survivors = token_processes(facts["launch_token"])
            for child in survivors:
                if process_identity(child["pid"], child).get("verified"):
                    signal_identity(child, signal.SIGKILL)
            if survivors:
                self.store.put_record("orphan_cancel", entity_id, {"identities": survivors, "reason": reason})
        self.store.record_job_state(entity_id, "cancel_requested", state_payload={"cancel_reason": reason})
        return {"status": "success", "entity_id": entity_id, "signalled": signalled}

    def tick(self):
        self._configure()
        self.children = [p for p in self.children if p.poll() is None]
        self.reconcile()
        run = self.store.get_record("run", "manifest", {})
        control = self.store.get_record("control", "current", {})
        deadline = run.get("deadline_at") or os.environ.get("RESEARCHCHEMBENCH_RUN_DEADLINE")
        expired = bool(deadline and time.time() >= datetime.fromisoformat(deadline).timestamp())
        totals = self.store.usage()
        config = run.get("config", {})
        usage_exhausted = (config.get("max_tokens") and totals["input_tokens"] + totals["output_tokens"] >= config["max_tokens"]) or (config.get("max_turns") and totals["turns"] >= config["max_turns"])
        stopping = expired or usage_exhausted or control.get("command") in {"cancel", "finalize"}
        if expired:
            self.store.put_record("control", "current", {"command": "cancel", "reason": "deadline"})
        elif usage_exhausted:
            self.store.put_record("control", "current", {"command": "cancel", "reason": "usage_budget"})
        for job in self.store.list_jobs():
            if job["state"] in TERMINAL_STATES: continue
            if stopping:
                self.cancel_entity(job["entity_id"], job["entity_type"], reason="deadline" if expired else "cancel")
            elif job["entity_type"] == "batch":
                self._batch(job, self.store.spec(job["entity_id"]))
            elif job["state"] == "queued":
                self._dispatch(job)
            orphan = self.store.get_record("orphan_cancel", job["entity_id"])
            if orphan and all(not process_identity(i["pid"], i).get("verified") for i in orphan["identities"]):
                self.store.record_job_state(job["entity_id"], "timeout" if orphan["reason"] == "deadline" else "cancelled")
        if control.get("command") in {"pause", "cancel", "finalize"} or expired or usage_exhausted:
            agent = self.store.get_record("agent", "identity", {})
            stop_key = str(agent.get("pid")) + ":" + str(agent.get("start_ticks"))
            stop_started = self.store.put_record("agent_stop", stop_key, time.time(), immutable=True)
            sig = signal.SIGKILL if time.time() - stop_started > 5 else signal.SIGTERM
            signal_identity(agent, sig)
            if agent.get("agent_token"):
                for child in token_processes(agent["agent_token"], variable="RCB_AGENT_RUN_TOKEN"):
                    signal_identity(child, sig)
        result = self.reconcile()
        controller = self.store.get_record("controller", "identity", {})
        if run and not process_identity(controller.get("pid"), controller).get("verified"):
            state = run.get("run_state")
            if state not in {"completed", "failed", "cancelled", "budget_exhausted"}:
                new_state = "budget_exhausted" if expired or usage_exhausted else "cancelled" if control.get("command") == "cancel" else "suspended_infrastructure"
                if state != new_state:
                    updated = {**run, "run_state": new_state, "manager_observed_controller_exit": True}
                    if new_state in {"cancelled", "budget_exhausted"}:
                        updated["termination"] = new_state
                        updated["run_elapsed_seconds"] = max(0, time.time() - datetime.fromisoformat(run["first_started_at"]).timestamp()) if run.get("first_started_at") else None
                    self.store.put_record("run", "manifest", updated)
                    atomic_json(self.store.directory / "run.json", updated)
        return result

    def serve(self):
        try:
            with file_lock(self.store.directory / "manager.lock"):
                self.store.put_record("manager", "identity", process_identity(os.getpid()))
                idle_since = time.time()
                while True:
                    try:
                        result = self.tick()
                    except Exception as exc:
                        print(f"manager_tick_failed: {type(exc).__name__}: {exc}", file=sys.stderr, flush=True)
                        time.sleep(1)
                        continue
                    pending = result["summary"]["active"] + result["summary"]["needs_reconciliation"]
                    run = self.store.get_record("run", "manifest", {})
                    if pending: idle_since = time.time()
                    if not pending and (not run or run.get("run_state") in {"completed", "failed", "cancelled", "budget_exhausted"}) and time.time() - idle_since > 3:
                        # Share the startup lock with enqueue/ensure_manager:
                        # an accepted job must not race an idle daemon exit.
                        with file_lock(self.store.directory / "manager_start.lock"):
                            if all(row["state"] in TERMINAL_STATES for row in self.store.list_jobs()):
                                self.store.put_record("manager", "identity", {})
                                return
                    time.sleep(0.5)
        except BlockingIOError:
            return


def ensure_manager(store: ExecutionStore):
    with file_lock(store.directory / "manager_start.lock"):
        identity = store.get_record("manager", "identity", {})
        if process_identity(identity.get("pid"), identity).get("verified"): return
        environment = {key: value for key, value in os.environ.items() if key.startswith("RESEARCHCHEMBENCH_") and not any(word in key for word in ("KEY", "TOKEN", "SECRET"))}
        environment.setdefault("RESEARCHCHEMBENCH_GLOBAL_RESOURCE_ALLOCATION_ROOT", str(store.directory.parent / ("host_" + socket.gethostname())))
        store.put_record("manager", "config", {"environment": environment}, immutable=True)
        with (store.directory / "manager.log").open("ab") as log:
            child = subprocess.Popen([sys.executable, "-m", "chemistry_toolbox.mcp.job_manager", str(store.root), store.run_id],
                                     cwd=PROJECT_ROOT, env={**os.environ, "PYTHONPATH": str(PROJECT_ROOT)},
                                     stdin=subprocess.DEVNULL, stdout=log, stderr=log, start_new_session=True, close_fds=True)
        # Record the launch identity now, not after a later health probe.
        store.put_record("manager", "identity", process_identity(child.pid))


if __name__ == "__main__":
    JobManager(Path(sys.argv[1]), run_id=sys.argv[2]).serve()
