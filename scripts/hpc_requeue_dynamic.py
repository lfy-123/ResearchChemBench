#!/usr/bin/env python3
"""Safely stop queued HPC jobs and re-submit them with live placement policy.

The script is deliberately account/workspace scoped.  It never sends StopJob
for RUNNING jobs.  Every re-submission performs a fresh HPC-capacity query and
chooses the 20 CPU/100 GiB group with the larger available-node estimate.
Priority 6 is used while the high-priority running budget has room; priority 3
is the explicit fallback after that budget is exhausted.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
QZTOOL = "/inspire/hdd/global_user/lifangyuan-253108110077/lfy_cc/qzcli_tool"
QZCLI = "/inspire/hdd/global_user/lifangyuan-253108110077/Anaconda3/bin/qzcli"
QZHOME = "/inspire/hdd/global_user/lifangyuan-253108110077/lfy_cc/.qzcli"
WS = "ws-6e6ba362-e98e-45b2-9c5a-311998e93d65"
WORKSPACE = "CPU资源空间"
PROJECT_HIGH = "project-35bc3935-0272-4ee5-aae3-8a7d0e2852ac"
PROJECT_LOW = "project-4493c9f7-2fbf-459a-ad90-749a5a420b91"
CG_CPU = "lcg-d4b51af1-2168-4ee2-920f-4fc50e2aeb69"
CG_HPC = "lcg-cb2de75c-40ac-4de1-bbb3-11e62b32f424"
QUOTA_20_100 = "a3502086-54ca-4275-b2f3-f42eff554fa2"
IMAGE = "docker.sii.shaipower.online/inspire-studio/hfss-slurm:v1.0"
CPU = 20
MEM_GIB = 100
HIGH_CAP = 2000
LOW_CAP = 3000
WAITING = {"QUEUEING", "CREATING", "PENDING", "STARTING", "SUBMITTING"}
TERMINAL = {"STOPPED", "SUCCEEDED", "FAILED", "CANCELLED", "DELETED", "RELEASED"}


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def env() -> dict[str, str]:
    e = os.environ.copy()
    e["QZCLI_HOME"] = QZHOME
    e["PYTHONPATH"] = QZTOOL + os.pathsep + e.get("PYTHONPATH", "")
    return e


def api():
    if QZTOOL not in sys.path:
        sys.path.insert(0, QZTOOL)
    from qzcli.api import QzAPI
    return QzAPI()


def listing(client) -> list[dict[str, Any]]:
    result = client.list_hpc_jobs(WS, page_size=5000)
    rows = result.get("jobs", []) or []
    if not rows:
        raise RuntimeError("empty HPC listing; refusing mutation")
    return rows


def capacity(group_id: str) -> dict[str, Any]:
    from qzcli.config import get_cookie
    cookie = (get_cookie() or {}).get("cookie")
    if not cookie:
        return {"group_id": group_id, "status": "UNAVAILABLE", "available_nodes": 0,
                "reason": "missing qzcli cookie"}
    rows = api().list_node_dimension(WS, cookie, page_size=500,
                                     logic_compute_group_id=group_id).get("node_dimensions", [])
    ready = [n for n in rows if n.get("status") == "Ready"]
    fit = [n for n in ready
           if float((n.get("cpu") or {}).get("available") or 0) >= CPU
           and float((n.get("memory") or {}).get("available") or 0) >= MEM_GIB]
    slots = sum(min(int(float((n.get("cpu") or {}).get("available") or 0)) // CPU,
                    int(float((n.get("memory") or {}).get("available") or 0)) // MEM_GIB)
                for n in ready)
    return {"group_id": group_id, "status": "OK", "total_nodes": len(rows),
            "ready_nodes": len(ready), "available_nodes": len(fit),
            "available_slots": slots,
            "node_types": sorted({str(n.get("node_type") or "") for n in rows}),
            "rule": "Ready nodes fitting >=20 CPU and >=100 GiB"}


def choose_group() -> tuple[str, dict[str, Any]]:
    options = [capacity(CG_CPU), capacity(CG_HPC)]
    usable = [x for x in options if x.get("status") == "OK"]
    if not usable:
        raise RuntimeError(json.dumps({"capacity": options}, ensure_ascii=False))
    chosen = max(usable, key=lambda x: (int(x.get("available_slots", 0)),
                                        int(x.get("available_nodes", 0)),
                                        x["group_id"] == CG_CPU))
    return chosen["group_id"], {"options": options, "selected": chosen,
                                "policy": "max available 20CPU/100GiB nodes"}


def account_high_running(rows: list[dict[str, Any]]) -> int:
    total = 0
    for row in rows:
        if str(row.get("status", "")).upper() != "RUNNING":
            continue
        # The platform exposes priority 31/name 6 for logical high priority.
        if str(row.get("priority_name", "")) != "6":
            continue
        spec = row.get("resource_spec_price") or {}
        total += int(spec.get("cpu_count") or 0) * int((row.get("slurm_cluster_spec") or {}).get("instance_count") or 1)
    return total


def stop_waiting(client, rows: list[dict[str, Any]], out: Path) -> list[dict[str, Any]]:
    targets = [r for r in rows if str(r.get("status", "")).upper() in WAITING]
    # Resolve one complete snapshot immediately before this loop.  Re-listing
    # before every item triggers Qizhi API rate limits for a large queue and
    # can leave the batch half-processed.  We still never include RUNNING in
    # the target set; a final listing below is used for reconciliation.
    events: list[dict[str, Any]] = []
    for row in targets:
        jid = str(row.get("job_id"))
        observed = str(row.get("status", "MISSING")).upper()
        event: dict[str, Any] = {"event": "stop_waiting", "at": now(), "job_id": jid,
                                 "observed_status": observed}
        if observed not in WAITING:
            event.update(ok=False, skipped=True, reason="state changed; never stop non-waiting job")
            events.append(event)
            continue
        try:
            # The v2 StopJob endpoint returns a successful response even when
            # the convenience stop_job() wrapper reports False after a legacy
            # fallback.  Use it directly and record exceptions.
            client._request_v2("hpc", "StopJob", {"job_id": jid})
            event["ok"] = True
        except Exception as exc:
            event["ok"] = False
            event["error"] = repr(exc)
        event["terminal_status"] = "REQUESTED"
        events.append(event)
        print(json.dumps(event, ensure_ascii=False), flush=True)
        time.sleep(0.35)
    # Reconcile once, rather than making a read request per target.
    try:
        final = {str(x.get("job_id")): x for x in listing(client)}
        for event in events:
            event["terminal_status"] = str((final.get(event["job_id"]) or {}).get("status", "MISSING")).upper()
            if event.get("terminal_status") == "STOPPED":
                event["ok"] = True
    except Exception as exc:
        for event in events:
            event.setdefault("reconcile_error", repr(exc))
    out.write_text(json.dumps({"created_at": now(), "events": events,
                               "counts": dict(Counter(str(e.get("terminal_status")) for e in events))},
                              ensure_ascii=False, indent=2) + "\n")
    return events


def submit_one(client, row: dict[str, Any], dry_run: bool) -> dict[str, Any]:
    spec = row.get("resource_spec_price") or {}
    cpu = int(spec.get("cpu_count") or 0)
    mem = int(spec.get("memory_size_gib") or 0)
    if cpu != CPU or mem != MEM_GIB:
        return {"job_id": row.get("job_id"), "status": "skipped_unsupported_spec",
                "cpu": cpu, "memory_gib": mem}
    # The approved limits are RUNNING limits, not queued/admission limits.
    # Use the shared account-wide inventory (HPC + interactive, all workspaces)
    # and select P6 until its running cap is reached; only then use P3.
    policy_dir = str(ROOT / "docs" / "verification" / "group_5")
    if policy_dir not in sys.path:
        sys.path.insert(0, policy_dir)
    from hpc_priority_policy import choose_priority
    decision = choose_priority(cpu=cpu, safety=0)
    if decision.get("status") != "selected":
        return {"job_id": row.get("job_id"), "status": "blocked_priority_capacity",
                "priority_decision": decision}
    priority = int(decision["priority"])
    project = str(decision["project"])
    group_id, cap = choose_group()
    # Repeat capacity immediately before the mutating create call.
    group_id, cap2 = choose_group()
    selected = cap2.get("selected", {})
    if int(selected.get("available_nodes", 0)) <= 0:
        return {"job_id": row.get("job_id"), "status": "blocked_no_capacity",
                "capacity": cap2, "priority": priority}
    sb = row.get("sbatch_script") or {}
    cluster = row.get("slurm_cluster_spec") or {}
    entrypoint = str(sb.get("entrypoint") or "")
    if not entrypoint:
        return {"job_id": row.get("job_id"), "status": "skipped_missing_entrypoint"}
    name = f"{row.get('job_name') or row.get('job_id')}-requeue-{int(time.time())}"
    args = {"job_name": name, "workspace_id": WS, "project_id": project,
            "logic_compute_group_id": group_id, "entrypoint": entrypoint,
            "image": str(cluster.get("image") or IMAGE),
            "predef_quota_id": QUOTA_20_100, "cpu": CPU, "mem_gi": MEM_GIB,
            "instances": 1, "cpus_per_task": int(sb.get("cpus_per_task") or CPU),
            "memory_per_cpu": str(sb.get("memory_per_cpu") or "5G"),
            "image_type": str(cluster.get("image_type") or "SOURCE_PUBLIC"),
            "priority": priority}
    result: Any = {"old_job_id": row.get("job_id"), "status": "dry_run" if dry_run else "submitted",
                   "priority": priority, "compute_group_id": group_id,
                   "capacity": cap2, "priority_decision": decision,
                   "create_args": {k: v for k, v in args.items() if k != "entrypoint"}}
    if not dry_run:
        try:
            cmd = [QZCLI, "hpc", "--json", "--name", args["job_name"],
                   "--workspace", WORKSPACE, "--project", project,
                   "--compute-group", group_id, "--predef-quota-id", QUOTA_20_100,
                   "--cpu", str(CPU), "--mem-gi", str(MEM_GIB), "--instances", "1",
                   "--cpus-per-task", str(args["cpus_per_task"]),
                   "--memory-per-cpu", args["memory_per_cpu"], "--priority", str(priority),
                   "--image", args["image"], "--image-type", args["image_type"],
                   "--entrypoint", entrypoint]
            p = subprocess.run(cmd, cwd=ROOT, env=env(), text=True, capture_output=True)
            result["return_code"] = p.returncode
            result["stdout_tail"] = p.stdout[-3000:]
            result["stderr_tail"] = p.stderr[-3000:]
            import re
            match = re.search(r"hpc-job-[0-9a-f-]+", p.stdout + p.stderr)
            result["new_job_id"] = match.group(0) if match else None
            if p.returncode or not match:
                result["status"] = "submit_failed"
        except Exception as exc:
            result["status"] = "submit_failed"
            result["error"] = repr(exc)
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["stop", "resubmit", "stop-and-resubmit"])
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--since", default="", help="API stopped_at lower bound (YYYY-MM-DD HH:MM:SS) for resubmit-only")
    ap.add_argument("--ledger", type=Path, default=ROOT / "docs/verification/qzcli_hpc_dynamic_requeue.json")
    args = ap.parse_args()
    client = api()
    rows = listing(client)
    summary: dict[str, Any] = {"started_at": now(), "mode": args.mode,
                               "initial_status_counts": dict(Counter(str(r.get("status")) for r in rows)),
                               "running_ids": [r.get("job_id") for r in rows if str(r.get("status")).upper() == "RUNNING"]}
    stop_path = args.ledger.with_name("dynamic_requeue_stop.json")
    if args.mode in {"stop", "stop-and-resubmit"}:
        summary["stop"] = stop_waiting(client, rows, stop_path)
        rows = listing(client)
    if args.mode in {"resubmit", "stop-and-resubmit"}:
        # Only terminal STOPPED records from this workspace are eligible.  A
        # RUNNING row is rejected again at this point as a second guard.
        # Never use the workspace's historical STOPPED set as the input: that
        # would duplicate old work.  In combined mode, only jobs stopped by
        # this invocation are eligible.  In resubmit-only mode, require an
        # explicit stop ledger produced by a prior invocation.
        stop_events = summary.get("stop")
        if stop_events is None:
            try:
                stop_events = json.loads(stop_path.read_text()).get("events", [])
            except Exception:
                stop_events = []
        stopped_ids = {str(e.get("job_id")) for e in (stop_events or [])
                       if e.get("ok") and str(e.get("terminal_status", "")).upper() == "STOPPED"}
        if args.since:
            # The platform keeps stopped_at on the immutable source record;
            # this recovers stop requests from an earlier interrupted batch
            # without ever touching historical STOPPED work.
            eligible = [r for r in rows if str(r.get("status", "")).upper() == "STOPPED"
                        and str(r.get("stopped_at", "")) >= args.since
                        and str(r.get("job_name", "")).startswith("rcb-")]
        else:
            eligible = [r for r in rows if str(r.get("status", "")).upper() == "STOPPED"
                        and str(r.get("job_id")) in stopped_ids]
        # A separate group supervisor may already have recovered some of the
        # same source decks while this cancellation batch was running.  Do not
        # create duplicate science calculations: compare immutable entrypoints
        # against all active jobs before submitting.
        active_entries = {str((r.get("sbatch_script") or {}).get("entrypoint") or "")
                          for r in rows if str(r.get("status", "")).upper() not in TERMINAL}
        eligible = [r for r in eligible
                    if str((r.get("sbatch_script") or {}).get("entrypoint") or "") not in active_entries]
        if args.limit:
            eligible = eligible[: args.limit]
        results = []
        for row in eligible:
            result = submit_one(client, row, args.dry_run)
            results.append(result)
            print(json.dumps(result, ensure_ascii=False), flush=True)
            if not args.dry_run:
                time.sleep(1)
        summary["resubmit"] = results
    summary["finished_at"] = now()
    args.ledger.parent.mkdir(parents=True, exist_ok=True)
    args.ledger.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"ledger": str(args.ledger), "finished_at": summary["finished_at"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
