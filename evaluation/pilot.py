"""Run selected final verified tasks through the persistent Codex adapter."""


def _new_output_directory(parent, paper_id):
    import uuid
    from datetime import datetime, timezone

    stamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    return parent / f"{paper_id}_{stamp}_{uuid.uuid4().hex[:6]}"


def _latest_run(root, paper_id, task_type):
    """Find the latest started run, without changing any saved run or using mtime."""
    import json
    from datetime import datetime, timezone

    candidates = []
    pattern = f"*/runs/cli_runs/batch_*/{task_type}-{paper_id}-codex-*"
    for workspace in (root / "workspaces/codex_gpt56").glob(pattern):
        if not workspace.is_dir():
            continue
        try:
            meta = json.loads((workspace / "_meta.json").read_text(encoding="utf-8"))
            if not isinstance(meta, dict) or any(meta.get(key) != value for key, value in {
                "run_id": workspace.name, "paper_id": paper_id,
                "task_type": task_type, "agent_key": "codex",
            }.items()):
                raise ValueError("saved run identity mismatch")
            if meta.get("first_started_at"):
                started = datetime.fromisoformat(meta["first_started_at"])
                if started.tzinfo is None:
                    raise ValueError("first_started_at has no timezone")
            else:
                # Older metadata stores this immutable UTC start stamp.
                started = datetime.strptime(meta["timestamp"], "%Y%m%d_%H%M%S").replace(tzinfo=timezone.utc)
        except (OSError, ValueError, KeyError, TypeError) as exc:
            raise ValueError(f"Cannot select latest run: {workspace}: {exc}; use explicit --run-root and --run-id") from exc
        candidates.append((started, workspace.resolve()))
    if not candidates:
        return None
    latest = max(started for started, _ in candidates)
    matches = {workspace for started, workspace in candidates if started == latest}
    if len(matches) != 1:
        raise ValueError(f"Ambiguous latest run for {paper_id}; use explicit --run-root and --run-id: {sorted(map(str, matches))}")
    return matches.pop()


def _automatic_resume_arguments(workspace, paper_id, args, explicit_options):
    """Prepare an existing-run request; None means previewed or already finished."""
    import json
    from .execution.recovery import load_run_manifest
    from .provenance.results import read_scoring_status

    manifest = load_run_manifest(workspace)
    if any(manifest.get(key) != value for key, value in {
        "run_id": workspace.name, "paper_id": paper_id, "task_type": args.mode,
    }.items()):
        raise ValueError(f"Saved manifest identity mismatch: {workspace}")
    state = manifest.get("run_state")
    scoring = read_scoring_status(workspace)["evaluation_status"]
    print(f"Auto-resume {paper_id}: {workspace} (Agent={state}, Judge={scoring})", flush=True)
    if explicit_options & {"--job-timeout-seconds", "--max-tokens", "--cpu-cores", "--memory-mb"}:
        raise ValueError("Resume uses saved resources; only --timeout-seconds can extend a saved budget")
    if args.dry_run:
        print(json.dumps({"status": "resume_preview", "run_id": workspace.name,
                          "run_root": str(workspace), "run_state": state, "evaluation_status": scoring,
                          "note": "Selection only; host, process, environment and session checks occur on actual resume."}))
        return None
    if state == "completed" and (scoring == "scored" or args.no_score):
        print(f"Skipping {paper_id}: {'evaluation already scored' if scoring == 'scored' else 'Agent already completed (--no-score)'}. Saved results retained.", flush=True)
        return None
    values = ["--resume", "--run-root", str(workspace), "--run-id", workspace.name]
    if "--timeout-seconds" in explicit_options:
        saved_budget = manifest.get("config", {}).get("timeout_seconds")
        # Reusing the original submission command is not a request to reset its clock.
        if args.timeout_seconds != saved_budget:
            values += ["--timeout-seconds", str(args.timeout_seconds)]
    if args.no_score:
        values.append("--no-score")
    if args.retry_in_doubt:
        values.append("--retry-in-doubt")
    return values


def _run_sequential(root, args, *, explicit_options=None):
    """Finish each paper's Agent and Judge in an isolated process and directory."""
    import signal
    import subprocess
    import sys

    from .execution.recovery import RunRecoveryError

    explicit_options = explicit_options or set()
    output_root = (args.output_dir or root / "workspaces/codex_gpt56").resolve()
    output_root.mkdir(parents=True, exist_ok=args.output_dir is None)
    options = []
    for name, value in vars(args).items():
        if name in {"paper_ids", "output_dir", "run_root", "run_id"} or value is None:
            continue
        if name == "resume_enabled":
            options.append("--resume" if value else "--no-resume")
        elif isinstance(value, bool):
            if value:
                options.append("--" + name.replace("_", "-"))
        else:
            options.extend(("--" + name.replace("_", "-"), str(value)))

    child = None
    interrupted = None

    def stop(signum, _frame):
        nonlocal interrupted
        interrupted = signum
        if child is not None and child.poll() is None:
            # Use the evaluation CLI's graceful SIGINT handler for both signals.
            child.send_signal(signal.SIGINT)

    previous = {sig: signal.signal(sig, stop) for sig in (signal.SIGINT, signal.SIGTERM)}
    exit_code = 0
    try:
        for index, paper_id in enumerate(args.paper_ids, 1):
            if interrupted is not None:
                break
            try:
                # Recheck at dispatch: a long queue must not select a stale run.
                workspace = _latest_run(root, paper_id, args.mode) if args.resume_enabled and not args.output_dir else None
                if workspace:
                    child_options = _automatic_resume_arguments(workspace, paper_id, args, explicit_options)
                    if child_options is None:
                        continue
                    print(f"[{index}/{len(args.paper_ids)}] Resuming {paper_id}; run: {workspace.name}", flush=True)
                else:
                    output = _new_output_directory(output_root, paper_id)
                    child_options = [*options, paper_id, "--output-dir", str(output)]
                    print(f"[{index}/{len(args.paper_ids)}] Starting new {paper_id}; output: {output}", flush=True)
            except (RunRecoveryError, ValueError, OSError) as exc:
                print(f"[{index}/{len(args.paper_ids)}] Resume blocked for {paper_id}: {exc}", file=sys.stderr, flush=True)
                exit_code = exit_code or 2
                continue
            with subprocess.Popen(
                [sys.executable, "-m", "evaluation.pilot", *child_options],
                cwd=root,
            ) as child:
                if interrupted is not None:
                    child.send_signal(signal.SIGINT)
                code = child.wait()
            child = None
            print(f"[{index}/{len(args.paper_ids)}] Finished {paper_id}; exit={code}", flush=True)
            if interrupted is not None:
                return 128 + interrupted
            if code < 0 or code >= 128:
                return 128 - code if code < 0 else code
            if code and not exit_code:
                exit_code = code
        return 128 + interrupted if interrupted is not None else exit_code
    finally:
        for sig, handler in previous.items():
            signal.signal(sig, handler)


def main():
    import argparse
    import json
    import os
    import re
    import shutil
    import sys
    from datetime import datetime, timezone
    from pathlib import Path
    from urllib.parse import urlsplit

    root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(
        description="Evaluate final verified tasks sequentially with Codex and a Responses API judge.",
        epilog="With --resume PAPER_ID, resume the latest matching run under workspaces/codex_gpt56, or start new if none exists. Agent and judge default to gpt-5.6-sol / high. No API key is logged.",
    )
    parser.add_argument("paper_ids", nargs="*", metavar="PAPER_ID", help="One or more paper IDs, executed in the given order.")
    parser.add_argument("--mode", choices=("autonomous_research", "paper_reproduction"), default="autonomous_research",
                        help="Select tasks/final_verified_<mode> (default: autonomous_research).")
    parser.add_argument("--dry-run", action="store_true", help="Prepare a new run or preview automatic resume selection; no Agent, MCP, or Judge is started.")
    parser.add_argument("--no-score", action="store_true", help="Run Codex without the LLM judge.")
    parser.add_argument("--output-dir", type=Path,
                        help="Force a new output directory (bypasses latest-run discovery); for multiple papers, a new parent containing per-paper directories. Must not already exist.")
    parser.add_argument("--timeout-seconds", type=int, default=345600, help="Per-task total Agent wall time (default: 345600 seconds / 96 hours).")
    parser.add_argument("--job-timeout-seconds", type=int, default=86400, help="Per-job walltime; the original run deadline is also enforced.")
    parser.add_argument("--max-tokens", type=int, default=None, help="Cumulative reported input/output token budget across attempts.")
    parser.add_argument("--cpu-cores", type=int, default=48)
    parser.add_argument("--memory-mb", type=int, default=204800)
    from .execution.resume_policy import add_resume_arguments
    add_resume_arguments(parser)
    parser.add_argument("--run-root", type=Path)
    parser.add_argument("--run-id")
    parser.add_argument("--retry-in-doubt", action="store_true", help="Permit bounded retry of uncertain Judge requests with --resume; billing may be duplicated.")
    args = parser.parse_args()
    explicit_options = {option.split("=", 1)[0] for option in sys.argv[1:]}
    if args.run_root is not None or args.run_id is not None:
        if not (args.run_root and args.run_id) or args.resume_enabled is not True:
            parser.error("Existing run requires --resume, --run-root and --run-id")
        if args.output_dir or args.dry_run:
            parser.error("Existing run cannot be combined with --output-dir or --dry-run; use status to inspect")
        if len(args.paper_ids) > 1:
            parser.error("--run-id identifies one existing run; specify at most one paper ID")
        # Scientific configuration belongs to the saved run, not new-run defaults.
        if explicit_options & {"--job-timeout-seconds", "--max-tokens", "--cpu-cores", "--memory-mb"}:
            parser.error("Resume can only explicitly extend --timeout-seconds; other saved budgets and resources are frozen")
        from .execution.recovery import load_run_manifest, locate_workspace
        if args.paper_ids or "--mode" in explicit_options:
            saved = load_run_manifest(locate_workspace(args.run_root.resolve(), args.run_id))
            if args.paper_ids and saved["paper_id"] != args.paper_ids[0]:
                parser.error("paper_id does not match the saved run")
            if "--mode" in explicit_options and saved["task_type"] != args.mode:
                parser.error("--mode does not match the saved run")
        from .execution.control import main as manage
        values = ["resume", "--resume", "--run-root", str(args.run_root), "--run-id", args.run_id]
        if "--timeout-seconds" in explicit_options:
            values += ["--timeout-seconds", str(args.timeout_seconds)]
        if args.no_score:
            values.append("--no-score")
        if args.retry_in_doubt:
            values.append("--retry-in-doubt")
        raise SystemExit(manage(values))
    if args.retry_in_doubt and args.resume_enabled is not True:
        parser.error("--retry-in-doubt requires --resume")
    if not args.paper_ids:
        parser.error("Provide at least one PAPER_ID")
    if any(not re.fullmatch(r"paper_[A-Za-z0-9]+", paper) for paper in args.paper_ids):
        parser.error("Each PAPER_ID must have the form paper_<identifier>")
    if len(set(args.paper_ids)) != len(args.paper_ids):
        parser.error("Duplicate paper IDs are not allowed in one submission")
    if args.timeout_seconds < 1 or args.job_timeout_seconds < 1 or args.cpu_cores < 1 or args.memory_mb < 128 or (args.max_tokens is not None and args.max_tokens < 1):
        parser.error("timeout/cpu must be positive and memory must be at least 128 MiB")

    task_type = args.mode
    existing = {}
    if args.resume_enabled and not args.output_dir:
        from .execution.recovery import RunRecoveryError
        try:
            existing = {paper: _latest_run(root, paper, task_type) for paper in args.paper_ids}
            if len(args.paper_ids) == 1 and existing[args.paper_ids[0]]:
                values = _automatic_resume_arguments(existing[args.paper_ids[0]], args.paper_ids[0], args, explicit_options)
                if values is None:
                    raise SystemExit(0)
                from .execution.control import main as manage
                raise SystemExit(manage(["resume", *values]))
        except (RunRecoveryError, ValueError, OSError) as exc:
            parser.error(str(exc))
    # Existing runs use their frozen task snapshot, even if today's release changed.
    sources = [root / "tasks" / f"final_verified_{task_type}" / paper for paper in args.paper_ids if not existing.get(paper)]
    for source in sources:
        if not (source / "task_info.json").is_file():
            parser.error(f"Final verified task not found: {source}; hold and other task directories are not selected")

    if len(args.paper_ids) > 1 and not sources:
        raise SystemExit(_run_sequential(root, args, explicit_options=explicit_options))

    api_key = os.environ.get("RCB_CODEX_API_KEY", "").strip()
    if not api_key and not args.dry_run:
        parser.error("Set RCB_CODEX_API_KEY in config.local.env or the environment")
    base_url = os.environ["RCB_CODEX_BASE_URL"].rstrip("/")
    parsed_url = urlsplit(base_url)
    if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
        parser.error("RCB_CODEX_BASE_URL must be an HTTP(S) API base URL")
    if parsed_url.username or parsed_url.password or parsed_url.query or parsed_url.fragment:
        parser.error("The API base URL must not contain credentials, query parameters, or fragments")
    # A bare gateway origin is assumed to expose the OpenAI-compatible /v1 API.
    # Set RCB_CODEX_BASE_URL to a complete base path if the gateway uses another one.
    if not parsed_url.path:
        base_url += "/v1"
    model = os.environ["RCB_CODEX_MODEL"]
    effort = os.environ["RCB_CODEX_REASONING_EFFORT"]
    if effort not in {"low", "medium", "high", "xhigh"}:
        parser.error("RCB_CODEX_REASONING_EFFORT must be low, medium, high, or xhigh")
    codex_executable = shutil.which(os.environ.get("RCB_CODEX_EXECUTABLE", "codex"))

    if len(args.paper_ids) > 1:
        from .contracts import validate_task_package
        for source in sources:
            validation = validate_task_package(source)
            if validation.status != "passed":
                parser.error(f"Invalid task package: {source}: {';'.join(validation.findings)}")
        raise SystemExit(_run_sequential(root, args, explicit_options=explicit_options))

    label = args.paper_ids[0]
    run_root = (args.output_dir or _new_output_directory(root / "workspaces/codex_gpt56", label)).resolve()
    run_root.mkdir(parents=True, exist_ok=False)
    from chemistry_toolbox.src.recovery_io import atomic_json
    from .execution.provider_errors import normalize_error
    submission = {"schema_version": 1, "submitted_at": datetime.now(timezone.utc).isoformat(),
                  "run_root": str(run_root), "tasks": [{"task_type": task_type, "paper_id": paper} for paper in args.paper_ids],
                  "agent": "codex", "repeats": 1, "phase": "preflight", "status": "preparing", "api_verified": False}
    atomic_json(run_root / "submission.json", submission)

    # TaskRepository requires <root>/<task_type>/<paper_id>, and rejects symlinked
    # task directories. Snapshot only the selected final packages, without
    # editing its manifest or scientific content. Private references stay in this
    # evaluator-side snapshot; TaskRunner materializes only the public Agent files.
    task_root = run_root / "task_snapshot"
    task_settings = []
    try:
        for source in sources:
            staged_task = task_root / task_type / source.name
            shutil.copytree(source, staged_task)
            manifest = json.loads((staged_task / "package_manifest.json").read_text(encoding="utf-8"))
            task_settings.append({"paper_id": source.name, "task_type": task_type,
                                  "source_task": str(source), "staged_task": str(staged_task),
                                  "package_content_sha256": manifest["package_content_sha256"]})
    except (OSError, ValueError, KeyError) as exc:
        error = normalize_error(exc, source="task_snapshot")
        atomic_json(run_root / "submission.json", {**submission, "status": "preflight_failed", "error": error})
        print(json.dumps(error, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(2)
    os.environ.update({
        "RESEARCHCHEMBENCH_TASKS_DIR": str(task_root),
        "RESEARCHCHEMBENCH_TASK_ROOTS": str(task_root),
        "RESEARCHCHEMBENCH_WORKSPACES_DIR": str(run_root / "runs"),
        "RESEARCHCHEMBENCH_EXECUTION_MODE": "local",
        "RESEARCHCHEM_TOOL_DISCOVERY_MODE": "progressive",
        "RCB_CODEX_API_KEY": api_key,
        "OPENAI_API_KEY": api_key,
        "JUDGE_API_KEY": api_key,
        "JUDGE_API_BASE": base_url,
        "JUDGE_MODEL_NAME": model,
    })
    for name in ("RESEARCHCHEM_MCP_ENABLED_TOOLS", "RESEARCHCHEM_MCP_DISABLED_TOOLS"):
        os.environ.pop(name, None)

    # Import only after setting task roots, credentials, and workspace defaults.
    from evaluation import cli

    # Agent and judge settings are formal evaluation configuration, shared by resume.
    os.environ["JUDGE_WIRE_API"] = "responses"
    os.environ["JUDGE_REASONING_EFFORT"] = effort
    codex_settings = {"model": model, "base_url": base_url, "reasoning_effort": effort}
    config = {
        "name": f"codex_gpt56_{label}",
        "agents": ["codex"],
        "recovery_enabled": True,
        "resume": bool(args.resume_enabled),
        "codex_model": model,
        "codex_base_url": base_url,
        "codex_reasoning_effort": effort,
        "tasks": submission["tasks"],
        "repeats": 1,
        "max_concurrent_runs": 1,
        "timeout_seconds": args.timeout_seconds,
        # Toolbox deadlines retain the standard submission-script defaults; the
        # Agent's wall-time limit still stops its outstanding jobs on termination.
        "compute_action_timeout_seconds": args.job_timeout_seconds,
        "fast_action_timeout_seconds": args.job_timeout_seconds,
        "mcp_tool_timeout_seconds": max(86700, args.timeout_seconds + 60),
        "model_wait_strategy": "host_event_wait",
        "available_cpu_cores": args.cpu_cores,
        "available_memory_mb": args.memory_mb,
        "available_gpu_count": 0,
        # Counts completed Codex turns across attempts, not MCP calls or HTTP requests.
        "max_turns": 600,
        "max_tokens": args.max_tokens,
        "job_event_settle_seconds": 60,
        "job_event_max_batch_seconds": 300,
        "job_wait_heartbeat_seconds": 3600,
        "job_internal_poll_interval_seconds": 2,
        "job_failure_tail_chars": 2000,
        "tool_discovery_mode": "progressive",
        "execution_mode": "local",
        "live_progress": True,
        "progress_console": True,
        "progress_max_chars": 600,
        "judge": {"enabled": not args.no_score, "model": model, "base_url": base_url,
                  "reasoning_effort": effort, "wire_api": "responses", "api_key_env": "RCB_CODEX_API_KEY",
                  "retry_in_doubt": args.retry_in_doubt, "max_in_doubt_retries": 1},
    }
    config_path = run_root / "evaluation_config.yaml"
    # JSON is valid YAML and avoids an additional configuration serializer.
    config_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
    (run_root / "test_settings.json").write_text(json.dumps({
        "tasks": task_settings,
        "codex_executable": codex_executable,
        "codex_cli_settings": codex_settings,
        "judge": {"enabled": not args.no_score, "model": model, "reasoning_effort": effort, "wire_api": "responses"},
        "dry_run": args.dry_run,
    }, indent=2) + "\n", encoding="utf-8")
    print(f"Tasks ({task_type}, sequential): " + ", ".join(args.paper_ids), flush=True)
    print(f"Per-task budget: {args.timeout_seconds} seconds", flush=True)
    print(f"Agent: Codex / {model} / reasoning={effort}", flush=True)
    print(f"API base: {base_url} (Responses API; key omitted)", flush=True)
    print(f"Judge: {'disabled' if args.no_score else model + ' / ' + effort}", flush=True)
    print(f"Output: {run_root}", flush=True)
    print("Artifacts: runs/cli_runs/batch_*/{eval_report.json,results.json}; per-run _live_progress.log, _score.json, report/results.json", flush=True)
    try:
        exit_code = cli.run_eval(config_path, dry_run=args.dry_run, no_score=args.no_score)
    except (ValueError, OSError, RuntimeError) as exc:
        error = normalize_error(exc, source="preflight")
        atomic_json(run_root / "submission.json", {**submission, "status": "preflight_failed", "error": error})
        print(json.dumps(error, ensure_ascii=False), file=sys.stderr)
        raise SystemExit(2)
    # The standard batch CLI reports scoring errors in eval_report.json but may
    # otherwise exit successfully. Make a missing/failed pilot score visible to sh.
    if not args.dry_run and not args.no_score and exit_code == 0:
        reports = list((run_root / "runs" / "cli_runs").glob("batch_*/eval_report.json"))
        if len(reports) != 1:
            raise SystemExit("Expected exactly one pilot evaluation report")
        report = json.loads(reports[0].read_text(encoding="utf-8"))
        if any(row.get("score_error") or row.get("score") is None for row in report["runs"]):
            print(f"Pilot scoring failed; inspect {reports[0]}", file=sys.stderr)
            exit_code = 1
    raise SystemExit(exit_code)


if __name__ == "__main__":
    main()
