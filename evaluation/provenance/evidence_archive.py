"""Read-only evidence indexing and portable scientific-review exports.

Raw files are kept once. The audit directory lives outside the agent workspace.
An export is a review/scoring package, not an authenticated provider resume pack.
"""
from __future__ import annotations

import argparse
import gzip
import json
import os
from pathlib import Path
import shutil
import sqlite3
import tempfile
import time
from contextlib import closing

from chemistry_toolbox.src.recovery_io import atomic_json, control_directory

INDEX_VERSION = "run-evidence-3"
SKIP_DIRS = {".tmp", "tmp", "scratch", ".cache", ".home", "__pycache__", ".git", "node_modules", ".venv"}
SECRET_NAMES = {"auth.json", "config.local.env", ".env", "credentials.json"}


def read_json(path, default=None):
    try:
        return json.loads(Path(path).read_text())
    except (OSError, ValueError):
        return {} if default is None else default


def audit_directory(workspace):
    workspace = Path(workspace).resolve()
    return workspace.parent / "audit" / workspace.name


def _files(root):
    if not root.is_dir():
        return
    for directory, names, files in os.walk(root):
        names[:] = sorted(n for n in names if n not in SKIP_DIRS and not (Path(directory) / n).is_symlink())
        # ARCHE keeps its native session manifests and traces beside private
        # provider homes and unpacked executables. Only the former are review
        # evidence; authentication/runtime directories are not portable outputs.
        relative = Path(directory).relative_to(root)
        if root.name == "outputs" and relative.parts[:1] == ("arche",):
            names[:] = [n for n in names if n not in {"codex_home", "codex_runtime"}]
        for name in sorted(files):
            path = Path(directory) / name
            if not path.is_symlink() and name not in SECRET_NAMES and not name.endswith((".tmp", ".pyc")):
                yield path


def _without_credentials(value):
    if isinstance(value, dict):
        return {k: _without_credentials(v) for k, v in value.items()
                if not any(s in k.lower() for s in ("api_key", "authorization", "access_token", "secret", "password"))}
    if isinstance(value, list):
        return [_without_credentials(v) for v in value]
    if isinstance(value, str):
        from .model_io import redact_trace_value
        return redact_trace_value(value)
    return value


def build_run_index(workspace, *, output_dir=None):
    workspace = Path(workspace).resolve()
    meta = read_json(workspace / "_meta.json")
    run_id = meta.get("run_id", workspace.name)
    control = control_directory(workspace, run_id)
    roots = {"workspace": str(workspace), "control": str(control), "task_snapshot": str(control / "task_snapshot")}
    entries, jobs, problems = {}, [], []

    def add(path, scope="workspace", role="scientific_artifact", required=True, **facts):
        path = Path(path)
        root = Path(roots[scope])
        if not path.resolve().is_relative_to(root.resolve()) or path.is_symlink():
            problems.append({"path": str(path), "reason": "external_or_symlink"})
            return None
        ref = scope + "/" + path.relative_to(root).as_posix()
        exists = path.is_file()
        item = entries.setdefault(ref, {"ref": ref, "scope": scope, "path": path.relative_to(root).as_posix(),
            "role": role, "required": required, "exists": exists, "size_bytes": path.stat().st_size if exists else None,
            "producer": None, "consumers": [], "provenance": "unverified"})
        item.update(facts)
        if role != "scientific_artifact":
            item["role"] = role
        return item

    for name in ("report", "outputs", "code", "data", "_tool_results", "_tool_artifacts"):
        for path in _files(workspace / name):
            add(path, role="agent_report" if name == "report" else "tool_record" if name.startswith("_tool_") else "scientific_artifact")
    for name in ("_meta.json", "_tool_trace.jsonl", "_tool_call_events.jsonl", "task.md", "submission_schema.json", "_score.json", "_score_history.jsonl", "_scoring_attempt.json"):
        if (workspace / name).is_file():
            add(workspace / name, role="run_record")
    for name in ("INSTRUCTIONS.md", "_toolbox_catalog.json", "_agent_output.jsonl", "_model_io.jsonl", "_agent_events.jsonl"):
        if (workspace / name).is_file():
            add(workspace / name, role="process_record")
    if meta.get("agent_kind") == "external":
        for name in ("request.json", "tools.json"):
            add(workspace / "_agent_protocol" / name, role="process_record")
    contract = read_json(workspace / "submission_schema.json")
    from chemistry_toolbox.src.output_contract import public_path
    for specification in contract.get("required_files", []):
        name = specification if isinstance(specification, str) else specification.get("path")
        try:
            target = public_path(workspace, name)
            if target.is_dir():
                for path in _files(target):
                    add(path, role="agent_report")
            elif target.is_file():
                add(target, role="agent_report")
        except (ValueError, TypeError):
            problems.append({"reason": "invalid_public_deliverable", "required": False})
    for path in _files(control / "task_snapshot"):
        add(path, "task_snapshot", "frozen_rule_or_task")
    if not (control / "task_snapshot").is_dir():
        problems.append({"scope": "task_snapshot", "reason": "frozen_rules_unavailable", "required": bool(meta.get("recovery_enabled"))})
    for directory in sorted((workspace / "outputs" / "execution_jobs").glob("*")):
        if not directory.is_dir() or directory.is_symlink():
            continue
        request = read_json(directory / "request.json")
        status = read_json(directory / "status.json")
        collection = read_json(directory / "collection.json")
        job_id = status.get("job_id", directory.name)
        job = {"job_id": job_id, "state": status.get("status", "unknown"), "job_type": request.get("job_type"),
               "metadata": _without_credentials(request.get("metadata", {})), "command": request.get("command"),
               "inputs": [], "outputs": [], "request_ref": "workspace/" + (directory / "request.json").relative_to(workspace).as_posix()}
        inputs = request.get("frozen_inputs") or request.get("staged_inputs") or []
        targets = {i.get("target_path") for i in inputs}
        digests = {x.get("path"): x.get("sha256") for x in collection.get("outputs", [])}
        for path in _files(directory):
            relative = path.relative_to(directory).as_posix()
            role = "staged_input" if relative in targets else "execution_record" if relative in {"request.json", "status.json", "collection.json"} else "job_output"
            item = add(path, role=role, producer=None if role == "staged_input" else job_id,
                       provenance="staging_record" if role == "staged_input" else "job_directory",
                       sha256=digests.get(path.relative_to(workspace).as_posix()))
            if item and role == "job_output": job["outputs"].append(item["ref"])
        for frozen in inputs:
            source = str(frozen.get("source_path", ""))
            snapshot = Path(frozen.get("snapshot_path") or control / "inputs" / str(frozen.get("sha256", "missing")))
            if not snapshot.is_file() and frozen.get("sha256"):
                snapshot = control / "inputs" / frozen["sha256"]
            item = add(snapshot, "control", "frozen_input", sha256=frozen.get("sha256"), provenance="frozen_submission")
            if Path(source).is_absolute() and Path(source).is_relative_to(workspace):
                source = Path(source).relative_to(workspace).as_posix()
            link = {"source": "workspace/" + source if not Path(source).is_absolute() else source,
                    "target": frozen.get("target_path"), "snapshot": item["ref"] if item else None, "sha256": frozen.get("sha256")}
            job["inputs"].append(link)
            upstream = entries.get(link["source"])
            if upstream and job_id not in upstream["consumers"]:
                upstream["consumers"].append(job_id)
        for recorded in collection.get("outputs", []):
            relative = recorded.get("path")
            if not relative or any(part in SKIP_DIRS for part in Path(relative).parts):
                continue
            path = workspace / relative
            if not path.is_file():
                add(path, role="recorded_missing_output", producer=job_id,
                    sha256=recorded.get("sha256"), provenance="terminal_manifest")
        jobs.append(job)
    # Include accepted/queued attempts even if no process directory exists yet.
    db = control / "execution.sqlite3"
    if db.is_file():
        with closing(sqlite3.connect(db.as_uri() + "?mode=ro", uri=True)) as connection:
            connection.row_factory = sqlite3.Row
            tables = {r[0] for r in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            if "submissions" in tables:
                receipts = {r["entity_id"]: {k: r[k] for k in ("submission_key", "receipt_id", "request_fingerprint", "accepted_at")}
                            for r in connection.execute("SELECT * FROM submissions WHERE run_id=?", (run_id,))}
                for job in jobs: job["receipt"] = receipts.get(job["job_id"])
            if "jobs" in tables:
                known = {j["job_id"] for j in jobs}
                for row in connection.execute("SELECT * FROM jobs WHERE run_id=? AND entity_type='job'", (run_id,)):
                    if row["entity_id"] not in known:
                        jobs.append({"job_id": row["entity_id"], "state": row["state"], "inputs": [], "outputs": [],
                                     "receipt": receipts.get(row["entity_id"]) if "submissions" in tables else None})
            if "records" in tables:
                results = {row[0]: json.loads(row[1]) for row in connection.execute("SELECT key,payload FROM records WHERE namespace='result'")}
                for job in jobs:
                    result = results.get(job["job_id"], {})
                    reference = result.get("full_result_ref") or {}
                    if reference.get("path"):
                        item = add(workspace / reference["path"], role="action_result", producer=job["job_id"],
                                   sha256=reference.get("sha256"), provenance="durable_result")
                        job["result_ref"] = item["ref"] if item else None
                    else:
                        candidates = [control / "action_results" / (job["job_id"] + suffix)
                                      for suffix in (".envelope.json", ".json")]
                        original = next((path for path in candidates if path.is_file()), None)
                        if original:
                            item = add(original, "control", "action_result", producer=job["job_id"], provenance="durable_action_result")
                            job["result_ref"] = item["ref"] if item else None
                        elif result.get("action_result"):
                            job["action_result"] = result["action_result"]
                            job["result_provenance"] = "durable_result_record"
                    job["result_receipt_id"] = result.get("result_receipt_id")
            if "job_specs" in tables:
                specs = {r[0]: json.loads(r[1]) for r in connection.execute("SELECT entity_id,spec_json FROM job_specs")}
                for job in jobs:
                    spec = specs.get(job["job_id"], {})
                    job.setdefault("job_type", spec.get("job_type"))
                    job.setdefault("metadata", _without_credentials(spec.get("metadata", {})))
                    job.setdefault("command", spec.get("command"))
                    if job["inputs"]:
                        continue
                    for frozen in spec.get("frozen_inputs", []):
                        snapshot = control / "inputs" / str(frozen.get("sha256", "missing"))
                        item = add(snapshot, "control", "frozen_input", sha256=frozen.get("sha256"), provenance="frozen_submission")
                        source = Path(frozen.get("source_path", ""))
                        if source.is_absolute() and source.is_relative_to(workspace):
                            source = source.relative_to(workspace)
                        job["inputs"].append({"source": str(source) if source.is_absolute() else "workspace/" + source.as_posix(),
                            "target": frozen.get("target_path"), "snapshot": item["ref"] if item else None, "sha256": frozen.get("sha256")})
    # A consumer can sort before its producer; resolve links after all entries
    # exist rather than depending on arbitrary job IDs or directory ordering.
    for job in jobs:
        for link in job["inputs"]:
            upstream = entries.get(link["source"])
            if upstream and job["job_id"] not in upstream["consumers"]:
                upstream["consumers"].append(job["job_id"])
    artifacts = {}
    artifact_index = workspace / "_tool_artifacts/index.jsonl"
    if artifact_index.is_file():
        with artifact_index.open() as stream:
            for number, line in enumerate(stream, 1):
                try:
                    value = json.loads(line)
                    path = public_path(workspace, value["path"])
                    ref = "workspace/" + path.relative_to(workspace).as_posix()
                    if ref not in entries:
                        add(path, provenance="artifact_registry")
                    artifacts[value["artifact_id"]] = {"ref": ref, **{k: value.get(k) for k in
                        ("semantic_type", "media_type", "producer_action", "producer_backend", "parent_artifact_ids")}}
                    entries[ref].setdefault("artifact_ids", []).append(value["artifact_id"])
                except (ValueError, KeyError, TypeError):
                    problems.append({"reason": "invalid_artifact_record", "line": number, "required": False})
    process_sources = [f["ref"] for f in entries.values() if f["role"] == "process_record"]
    index = {"schema_version": INDEX_VERSION, "run_id": run_id, "source_roots": roots, "artifacts": artifacts,
             "process_evidence": {"sources": process_sources, "status": "available" if any(r.endswith(("_agent_output.jsonl", "_agent_events.jsonl")) for r in process_sources) else "incomplete"},
             "files": list(entries.values()), "jobs": jobs, "problems": problems,
             "retention": {"excluded_cache_directories": sorted(SKIP_DIRS), "sessions_included": False,
                           "purpose": "scientific_review_and_rescoring", "new_hash_scan": False}}
    index["verification"] = verify_required_evidence(index)
    if output_dir:
        write_index(index, output_dir)
    return index


def resolve_reference(index, ref, *, item=None):
    if ref in index.get("artifacts", {}):
        ref = index["artifacts"][ref]["ref"]
    item = item or next((f for f in index["files"] if f["ref"] == ref), None)
    if item is None:
        raise ValueError("unregistered evidence reference")
    if index.get("archive_root"):
        root = Path(index["archive_root"]).resolve()
        path = root / item.get("archive_path", item["ref"])
    else:
        root = Path(index["source_roots"][item["scope"]]).resolve()
        path = root / item["path"]
    if path.is_symlink() or not path.resolve().is_relative_to(root):
        raise ValueError("evidence reference escapes its registered root")
    return path


def verify_required_evidence(index):
    missing = [p for p in index.get("problems", []) if p.get("required", True)]
    for item in index["files"]:
        try:
            path = resolve_reference(index, item["ref"], item=item)
            if item.get("required") and not path.is_file():
                missing.append({"ref": item["ref"], "reason": "missing"})
            elif path.is_file() and item.get("role") != "run_record" and item.get("stored_size_bytes", item.get("size_bytes")) is not None and path.stat().st_size != item.get("stored_size_bytes", item["size_bytes"]):
                missing.append({"ref": item["ref"], "reason": "size_changed"})
        except (ValueError, OSError) as exc:
            missing.append({"ref": item["ref"], "reason": str(exc)})
    return {"state": "archive_incomplete" if missing else "complete", "missing": missing,
            "file_count": len(index["files"]), "total_bytes": sum(f.get("size_bytes") or 0 for f in index["files"])}


def write_index(index, output_dir):
    output = Path(output_dir)
    atomic_json(output / "index.json", index)
    lines = ["# Run evidence", "", f"Run: {index['run_id']}", f"State: {index['verification']['state']}",
             "", "| Job | State | Inputs | Outputs |", "| --- | --- | --- | --- |"]
    lines += [f"| {j['job_id']} | {j['state']} | {len(j['inputs'])} | {len(j['outputs'])} |" for j in index["jobs"]]
    lines += ["", "Full file locations, dependencies and missing evidence: index.json.",
              "Provider sessions and authentication are excluded; this package is for review and rescoring."]
    (output / "INDEX.md").write_text("\n".join(lines) + "\n")


def export_run_archive(workspace, destination, *, compress_logs=False):
    destination = Path(destination).resolve()
    if destination.exists() or destination.is_relative_to(Path(workspace).resolve()):
        raise ValueError("archive destination must be new and outside the source workspace")
    destination.parent.mkdir(parents=True, exist_ok=True)
    # The persistent manager drains for up to three seconds after a terminal
    # run, then clears its identity in SQLite. Wait before taking the snapshot;
    # do not waive change detection for a live ledger.
    from chemistry_toolbox.mcp.execution_store import ExecutionStore
    from chemistry_toolbox.src.recovery_io import process_identity
    store = ExecutionStore.open_existing(workspace)
    manager_active = False
    if store and read_json(Path(workspace) / "_meta.json").get("status") in {
        "completed", "failed", "cancelled", "budget_exhausted", "timeout",
    }:
        deadline = time.monotonic() + 5
        while True:
            identity = store.get_record("manager", "identity", {})
            manager_active = bool(identity and process_identity(identity.get("pid"), identity).get("verified"))
            if not manager_active or time.monotonic() >= deadline:
                break
            time.sleep(0.05)
    index = build_run_index(workspace)
    if manager_active:
        index["problems"].append({"reason": "active_manager_during_export", "required": True})
    if any(job.get("state") in {"accepted", "queued", "running", "starting", "collecting"} for job in index["jobs"]):
        index["problems"].append({"reason": "active_jobs_during_export", "required": True})
    if read_json(Path(workspace) / "_meta.json").get("status") in {"running", "ready", "recovering"}:
        index["problems"].append({"reason": "active_agent_during_export", "required": True})
    def signature(path):
        try:
            stat = path.stat()
            return stat.st_size, stat.st_mtime_ns
        except FileNotFoundError:
            return None
    sources = [resolve_reference(index, item["ref"], item=item) for item in index["files"]]
    database = Path(index["source_roots"]["control"]) / "execution.sqlite3"
    watched = {path for source in sources for path in (source, source.parent)} | {database, Path(str(database) + "-wal")}
    snapshot = {path: signature(path) for path in watched}
    staging = Path(tempfile.mkdtemp(prefix=".archive-", dir=destination.parent))
    try:
        for item in index["files"]:
            source = resolve_reference(index, item["ref"], item=item)
            if not source.is_file(): continue
            target = staging / item["ref"]
            target.parent.mkdir(parents=True, exist_ok=True)
            before = source.stat()
            textual = source.suffix in {".json", ".jsonl", ".log", ".out", ".md", ".txt", ".py", ".sh", ".yaml", ".yml"}
            redacted = False
            if textual:
                from .model_io import redact_trace_value
                if compress_logs and source.suffix in {".log", ".out"} and before.st_size > 65536:
                    target = Path(str(target) + ".gz")
                    item.update(encoding="gzip", archive_path=target.relative_to(staging).as_posix())
                opener = gzip.open if target.suffix == ".gz" else open
                with source.open(encoding="utf-8", errors="replace") as src, opener(target, "wt", encoding="utf-8") as dst:
                    for line in src:
                        sanitized = redact_trace_value(line)
                        redacted = redacted or sanitized != line
                        dst.write(sanitized)
                item["stored_size_bytes"] = target.stat().st_size
            else:
                shutil.copy2(source, target)
            after = source.stat()
            if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
                index["problems"].append({"ref": item["ref"], "reason": "source_changed_during_export"})
            if source.name in {"_meta.json", "request.json", "status.json"}:
                original = read_json(source)
                sanitized = _without_credentials(original)
                if sanitized != original:
                    atomic_json(target, sanitized)
                    item.update(stored_size_bytes=target.stat().st_size, credentials_redacted=True, sha256=None)
            if redacted:
                item.update(credentials_redacted=True, sha256=None)
        # Normalized events are a small portable derivative, never written back.
        from .agent_events import event_capture_summary, load_agent_events
        from .model_io import redact_trace_value
        events = load_agent_events(Path(workspace))
        normalized = staging / "workspace/_agent_events.jsonl"
        normalized.parent.mkdir(exist_ok=True)
        with normalized.open("w") as stream:
            for event in events:
                value = {k: v for k, v in event.items() if k != "raw" or event.get("kind") == "unparsed"}
                stream.write(json.dumps(redact_trace_value(value), ensure_ascii=False) + "\n")
        index["files"] = [f for f in index["files"] if f["ref"] != "workspace/_agent_events.jsonl"]
        index["files"].append({"ref": "workspace/_agent_events.jsonl", "scope": "workspace", "path": "_agent_events.jsonl",
            "role": "process_record", "required": True, "exists": True, "size_bytes": normalized.stat().st_size,
            "credentials_redacted": True, "derived": True})
        index["process_evidence"]["capture"] = event_capture_summary(events)
        # Consistent backup is optional supporting provenance, not needed to read
        # the index. No copying of a live SQLite main file without its journal.
        source_db = Path(index["source_roots"]["control"]) / "execution.sqlite3"
        if source_db.is_file():
            (staging / "control").mkdir(exist_ok=True)
            with closing(sqlite3.connect(source_db.as_uri() + "?mode=ro", uri=True)) as src, \
                    closing(sqlite3.connect(staging / "control" / "execution.sqlite3")) as dst, dst:
                src.backup(dst)
                # Controller records can contain operator configuration. The
                # portable index already carries scientific receipts/inputs;
                # exclude authentication/session/control records from review.
                tables = {row[0] for row in dst.execute("SELECT name FROM sqlite_master WHERE type='table'")}
                if "records" in tables:
                    dst.execute("DELETE FROM records WHERE namespace NOT IN ('result', 'collection', 'collection_revision', 'usage', 'usage_stream')")
                for table, keys, fields in (("records", "namespace, key", ("payload",)),
                        ("submissions", "run_id, submission_key", ("request_json", "input_manifest_json")),
                        ("job_specs", "entity_id", ("spec_json",)),
                        ("jobs", "entity_id", ("state_json",)),
                        ("execution_events", "sequence", ("payload_json",))):
                    # Fixed schema identifiers only; query parameters carry data.
                    if table not in tables:
                        continue
                    key_names = keys.split(", ")
                    columns = {row[1] for row in dst.execute(f"PRAGMA table_info({table})")}
                    for field in fields:
                        if field not in columns or not set(key_names) <= columns:
                            continue
                        for row in dst.execute(f"SELECT {keys}, {field} FROM {table}").fetchall():
                            original = json.loads(row[-1])
                            sanitized = _without_credentials(original)
                            if sanitized != original:
                                where = " AND ".join(name + "=?" for name in key_names)
                                dst.execute(f"UPDATE {table} SET {field}=? WHERE {where}", (json.dumps(sanitized), *row[:-1]))
            index["files"].append({"ref": "control/execution.sqlite3", "scope": "control", "path": "execution.sqlite3",
                "role": "review_ledger", "required": False, "exists": True,
                "size_bytes": (staging / "control/execution.sqlite3").stat().st_size,
                "credentials_redacted": True, "purpose": "provenance_only_not_resume"})
        changed_paths = [str(path) for path, before in snapshot.items() if signature(path) != before]
        if changed_paths:
            index["problems"].append({"reason": "source_changed_during_export", "required": True,
                                      "changed_paths": sorted(changed_paths)})
        index.pop("source_roots", None)
        index["archive_root"] = str(staging)
        index["verification"] = verify_required_evidence(index)
        index.pop("archive_root")
        write_index(index, staging / "audit")
        os.replace(staging, destination)
    except BaseException:
        shutil.rmtree(staging, ignore_errors=True)
        raise
    return open_archive(destination)


def open_archive(directory):
    root = Path(directory).resolve()
    index = read_json(root / "audit" / "index.json")
    if index.get("schema_version") != INDEX_VERSION:
        raise ValueError("unsupported or missing archive index")
    index["archive_root"] = str(root)
    index["verification"] = verify_required_evidence(index)
    return index


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=["index", "export", "verify"])
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--compress-logs", action="store_true")
    args = parser.parse_args(argv)
    if args.operation == "export":
        if not args.output: parser.error("export requires --output")
        result = export_run_archive(args.source, args.output, compress_logs=args.compress_logs)
    elif args.operation == "index":
        result = build_run_index(args.source, output_dir=args.output or audit_directory(args.source))
    else:
        result = open_archive(args.source)
    print(json.dumps(result["verification"], indent=2))
    return 0 if result["verification"]["state"] == "complete" else 2


if __name__ == "__main__":
    raise SystemExit(main())
