"""Agent process supervision, cancellation, and run finalization."""

from __future__ import annotations

import json
import os
import queue
import signal
import subprocess
import threading
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ..provenance.model_io import export_model_io_trace
from ..provenance.results import write_workspace_results
from ..provenance.trace import load_tool_trace, process_metrics
from ..settings import JUDGE_MODEL_NAME, OPENCODE_MODEL
from .progress import LiveProgressReporter

TERMINAL_EXECUTION_JOB_STATES = {"success", "failed", "timeout", "cancelled"}


class RunLifecycleMixin:
    def _write_meta(self, status: str, extra: dict[str, Any] | None = None) -> None:
        previous: dict[str, Any] = {}
        if self.meta_path.exists():
            try:
                previous = json.loads(self.meta_path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                previous = {}
        meta = {
            **previous,
            "task_id": self.task_id,
            "run_id": self.run_id,
            "timestamp": self.timestamp,
            "status": status,
            "workspace": str(self.workspace),
            "agent_key": self.agent_key,
            "agent_name": self.agent_name,
            "configured_agent_model": (
                OPENCODE_MODEL
                if self.agent.get("kind") == "opencode"
                else str(self.agent.get("model", ""))
            ),
            "configured_judge_model": JUDGE_MODEL_NAME,
            "tool_discovery_mode": self.tool_discovery_mode,
            "query": self.task_info.get("task", ""),
            "category": self.task_info.get("category", ""),
            "scientific_mode": self.task_info.get("scientific_mode", ""),
            "scientific_mode_description": self.task_info.get(
                "scientific_mode_description", ""
            ),
            "scientific_requirements": self.task_info.get(
                "scientific_requirements", []
            ),
            "required_deliverables": self.task_info.get(
                "required_deliverables", []
            ),
            "live_progress": self.live_progress,
            "progress_console": self.progress_console,
            "progress_max_chars": self.progress_max_chars,
            "timeout_policy": {
                "agent_timeout_seconds": self.timeout_seconds,
                "mcp_tool_timeout_seconds": (
                    self.mcp_tool_timeout_ms + 999
                ) // 1000,
                "compute_action_timeout_seconds": self.compute_action_timeout_seconds,
                "fast_action_timeout_seconds": self.fast_action_timeout_seconds,
                "action_timeout_agent_controllable": False,
            },
            "resource_budget": self.resource_budget_record(),
            "job_supervision_policy": {
                "event_settle_seconds": self.job_event_settle_seconds,
                "event_max_batch_seconds": self.job_event_max_batch_seconds,
                "wait_heartbeat_seconds": self.job_wait_heartbeat_seconds,
                "internal_poll_interval_seconds": self.job_internal_poll_interval_seconds,
                "failure_tail_chars": self.job_failure_tail_chars,
                "agent_controllable": False,
            },
            "live_progress_path": "_live_progress.log",
        }
        if extra:
            meta.update(extra)
        self.meta_path.write_text(
            json.dumps(meta, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )

    def _detect_model(self) -> str:
        if not self.output_path.exists():
            return ""
        for line in self.output_path.read_text(encoding="utf-8", errors="replace").splitlines()[:100]:
            try:
                value = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(value, dict):
                model = value.get("model") or value.get("model_name")
                if model:
                    return str(model)
                result = value.get("result")
                if isinstance(result, dict) and result.get("model"):
                    return str(result["model"])
        if self.agent.get("kind") == "opencode":
            return OPENCODE_MODEL
        return str(self.agent.get("model", ""))

    def request_stop(self) -> None:
        self._stop_requested = True
        self._terminate_process_tree()

    def _terminate_process_tree(self, *, force: bool = False) -> None:
        if self.process is None:
            return
        if os.name == "posix" and self.process_group_id is not None:
            try:
                os.killpg(
                    self.process_group_id,
                    signal.SIGKILL if force else signal.SIGTERM,
                )
                return
            except ProcessLookupError:
                return
            except PermissionError:
                pass
        if self.process.poll() is None:
            self.process.kill() if force else self.process.terminate()

    @staticmethod
    def _write_execution_job_status(path: Path, value: dict[str, Any]) -> None:
        """Atomically replace one detached execution-job status record."""

        temporary = path.with_suffix(path.suffix + ".runner-cleanup.tmp")
        temporary.write_text(
            json.dumps(value, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        os.replace(temporary, path)

    def _cancel_workspace_execution_jobs(
        self,
        *,
        reason: str,
        grace_seconds: float = 7.0,
    ) -> dict[str, Any]:
        """Stop detached native/program jobs owned by this run workspace.

        Native execution supervisors intentionally start in independent sessions
        so a normal Agent/MCP restart does not destroy submitted scientific work.
        A benchmark-level timeout is different: the run is terminal and no
        detached work may continue consuming host resources.  Status files under
        the immutable execution-job directory are the ownership boundary.
        """

        root = self.workspace / "outputs" / "execution_jobs"
        summary: dict[str, Any] = {
            "reason": reason,
            "job_root": str(root),
            "discovered_jobs": 0,
            "active_jobs": 0,
            "already_terminal_jobs": 0,
            "termination_signals_sent": 0,
            "cancellation_markers_written": 0,
            "forced_jobs": 0,
            "cancelled_jobs": 0,
            "errors": [],
            "jobs": [],
        }
        if not root.is_dir():
            return summary

        pending: dict[Path, dict[str, Any]] = {}
        for status_path in sorted(root.glob("job_*/status.json")):
            summary["discovered_jobs"] += 1
            try:
                status = json.loads(status_path.read_text(encoding="utf-8"))
            except Exception as exc:
                summary["errors"].append(
                    {
                        "status_path": str(status_path),
                        "error": f"{type(exc).__name__}: {exc}",
                    }
                )
                continue
            job_id = str(status.get("job_id") or status_path.parent.name)
            state = str(status.get("status") or "unknown")
            if state in TERMINAL_EXECUTION_JOB_STATES:
                summary["already_terminal_jobs"] += 1
                continue
            summary["active_jobs"] += 1
            pending[status_path] = status
            supervisor_pid = status.get("supervisor_pid")
            sent = False
            distributed = status.get("execution_mode") == "distributed" or (
                status.get("metadata") or {}
            ).get("execution_mode") == "distributed"
            if distributed:
                try:
                    (status_path.parent / "cancel_requested").write_text(
                        json.dumps(
                            {
                                "job_id": job_id,
                                "requested_at": datetime.now(timezone.utc).isoformat(),
                                "reason": reason,
                            },
                            indent=2,
                            ensure_ascii=False,
                        )
                        + "\n",
                        encoding="utf-8",
                    )
                    sent = True
                    summary["cancellation_markers_written"] += 1
                except OSError as exc:
                    summary["errors"].append(
                        {
                            "job_id": job_id,
                            "stage": "distributed_cancel_marker",
                            "error": f"{type(exc).__name__}: {exc}",
                        }
                    )
            elif isinstance(supervisor_pid, int) and supervisor_pid > 0:
                try:
                    os.kill(supervisor_pid, signal.SIGTERM)
                    sent = True
                    summary["termination_signals_sent"] += 1
                except ProcessLookupError:
                    pass
                except (PermissionError, OSError) as exc:
                    summary["errors"].append(
                        {
                            "job_id": job_id,
                            "stage": "supervisor_sigterm",
                            "error": f"{type(exc).__name__}: {exc}",
                        }
                    )
            summary["jobs"].append(
                {
                    "job_id": job_id,
                    "initial_status": state,
                    "supervisor_pid": supervisor_pid,
                    "termination_signal_sent": sent,
                    "distributed_cancellation": distributed,
                }
            )

        deadline = time.monotonic() + max(0.0, float(grace_seconds))
        while pending and time.monotonic() < deadline:
            for status_path in list(pending):
                try:
                    status = json.loads(status_path.read_text(encoding="utf-8"))
                except (OSError, json.JSONDecodeError):
                    continue
                if status.get("status") in TERMINAL_EXECUTION_JOB_STATES:
                    pending.pop(status_path, None)
                    summary["cancelled_jobs"] += int(status.get("status") == "cancelled")
            if pending:
                time.sleep(0.1)

        # A supervisor normally terminates its child process group and records
        # cancellation.  Force the group only when that cooperative path did not
        # reach a terminal state within the bounded grace period.
        for status_path, original_status in list(pending.items()):
            try:
                status = json.loads(status_path.read_text(encoding="utf-8"))
            except Exception:
                status = dict(original_status)
            if status.get("status") in TERMINAL_EXECUTION_JOB_STATES:
                summary["cancelled_jobs"] += int(status.get("status") == "cancelled")
                continue
            job_id = str(status.get("job_id") or status_path.parent.name)
            distributed = status.get("execution_mode") == "distributed" or (
                status.get("metadata") or {}
            ).get("execution_mode") == "distributed"
            if distributed:
                summary["errors"].append(
                    {
                        "job_id": job_id,
                        "stage": "distributed_cancellation_grace_expired",
                        "error": (
                            "Remote job did not publish a terminal state within the cleanup "
                            "grace period; its persistent cancellation marker remains active."
                        ),
                    }
                )
                continue
            child_pid = status.get("child_pid")
            supervisor_pid = status.get("supervisor_pid")
            forced = False
            if isinstance(child_pid, int) and child_pid > 0:
                try:
                    if os.name == "posix":
                        os.killpg(child_pid, signal.SIGKILL)
                    else:
                        os.kill(child_pid, signal.SIGKILL)
                    forced = True
                except ProcessLookupError:
                    pass
                except (PermissionError, OSError) as exc:
                    summary["errors"].append(
                        {
                            "job_id": job_id,
                            "stage": "child_sigkill",
                            "error": f"{type(exc).__name__}: {exc}",
                        }
                    )
            if isinstance(supervisor_pid, int) and supervisor_pid > 0:
                try:
                    os.kill(supervisor_pid, signal.SIGKILL)
                    forced = True
                except ProcessLookupError:
                    pass
                except (PermissionError, OSError) as exc:
                    summary["errors"].append(
                        {
                            "job_id": job_id,
                            "stage": "supervisor_sigkill",
                            "error": f"{type(exc).__name__}: {exc}",
                        }
                    )
            if forced:
                summary["forced_jobs"] += 1
            status.update(
                {
                    "status": "cancelled",
                    "finished_at": datetime.now(timezone.utc).isoformat(),
                    "return_code": status.get("return_code"),
                    "error": {
                        "code": "benchmark_run_terminated",
                        "message": (
                            "Detached execution job was stopped because its owning "
                            f"benchmark run ended with {reason}."
                        ),
                    },
                    "benchmark_cleanup": {
                        "reason": reason,
                        "forced": forced,
                    },
                }
            )
            try:
                self._write_execution_job_status(status_path, status)
                summary["cancelled_jobs"] += 1
            except Exception as exc:
                summary["errors"].append(
                    {
                        "job_id": job_id,
                        "stage": "status_update",
                        "error": f"{type(exc).__name__}: {exc}",
                    }
                )
        return summary

    def _tail_tool_trace(
        self,
        reporter: LiveProgressReporter,
        stop_event: threading.Event,
    ) -> None:
        """Follow completed MCP events without delaying the Agent stdout reader."""

        path = self.workspace / "_tool_trace.jsonl"
        offset = 0
        while True:
            saw_new_line = False
            if path.is_file():
                try:
                    with path.open("r", encoding="utf-8", errors="replace") as handle:
                        handle.seek(offset)
                        while True:
                            line = handle.readline()
                            if not line:
                                break
                            offset = handle.tell()
                            if line.strip():
                                saw_new_line = True
                                reporter.handle_tool_trace_line(line)
                except OSError as exc:
                    reporter.emit("MCP_TRACE_READ_ERROR", error=str(exc))
            if stop_event.is_set() and not saw_new_line:
                break
            stop_event.wait(0.2)

    def run(self) -> dict[str, Any]:
        if not self.workspace.exists():
            self.setup_workspace()
        argv = self.build_agent_argv()
        self._write_meta("running", {"agent_command": self.command_preview()})
        env = self._agent_environment()
        started = time.monotonic()
        termination = "process_exit"
        exit_code = -1
        background_job_cleanup: dict[str, Any] | None = None
        opencode_database_sync: dict[str, Any] | None = None
        reporter = LiveProgressReporter(
            self.workspace,
            self.run_id,
            enabled=self.live_progress,
            console=self.progress_console,
            max_chars=self.progress_max_chars,
        )
        trace_stop = threading.Event()
        trace_thread = threading.Thread(
            target=self._tail_tool_trace,
            args=(reporter, trace_stop),
            daemon=True,
        )
        reporter.emit(
            "RUN_START",
            task=self.task_id,
            agent=self.agent_key,
            model=OPENCODE_MODEL if self.agent.get("kind") == "opencode" else self.agent_name,
            timeout_seconds=self.timeout_seconds,
            compute_action_timeout_seconds=self.compute_action_timeout_seconds,
            fast_action_timeout_seconds=self.fast_action_timeout_seconds,
            mcp_tool_timeout_seconds=(self.mcp_tool_timeout_ms + 999) // 1000,
            available_cpu_cores=self.available_cpu_cores,
            available_memory_mb=self.available_memory_mb,
            available_gpu_count=self.available_gpu_count,
            execution_mode=self.execution_mode,
            max_turns=self.max_turns,
        )
        reporter.emit(
            "MODEL_INPUT",
            source="initial_instructions",
            text=self.instructions_path.read_text(encoding="utf-8", errors="replace"),
        )
        trace_thread.start()

        try:
            self.process = subprocess.Popen(
                argv,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                cwd=str(self.workspace),
                text=True,
                encoding="utf-8",
                errors="replace",
                env=env,
                shell=False,
                bufsize=1,
                start_new_session=(os.name == "posix"),
            )
            self.process_group_id = self.process.pid if os.name == "posix" else None
            assert self.process.stdout is not None
            line_queue: queue.Queue[str | None] = queue.Queue()

            def read_stdout() -> None:
                assert self.process is not None and self.process.stdout is not None
                for line in self.process.stdout:
                    line_queue.put(line.rstrip("\n"))
                line_queue.put(None)

            reader = threading.Thread(target=read_stdout, daemon=True)
            reader.start()
            stream_done = False
            process_exit_cleanup_started = False
            with self.output_path.open("w", encoding="utf-8") as output:
                while not stream_done:
                    if time.monotonic() - started > self.timeout_seconds:
                        termination = "timeout"
                        self._terminate_process_tree()
                        break
                    try:
                        line = line_queue.get(timeout=0.2)
                    except queue.Empty:
                        if self.process.poll() is not None:
                            if not reader.is_alive():
                                break
                            if not process_exit_cleanup_started:
                                # Some Agent CLIs can exit before their MCP
                                # descendants. Those descendants inherit stdout
                                # and otherwise keep this reader open forever.
                                self._terminate_process_tree()
                                process_exit_cleanup_started = True
                        continue
                    if line is None:
                        stream_done = True
                    elif line:
                        output.write(line + "\n")
                        output.flush()
                        reporter.handle_agent_line(line)

            try:
                exit_code = self.process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self._terminate_process_tree(force=True)
                exit_code = self.process.wait()
            if self._stop_requested:
                termination = "stopped"
            if termination in {"timeout", "stopped"}:
                background_job_cleanup = self._cancel_workspace_execution_jobs(
                    reason=termination
                )
                reporter.emit(
                    "BACKGROUND_JOB_CLEANUP",
                    **background_job_cleanup,
                )
            opencode_database_sync = self._sync_opencode_database()
        except Exception as exc:
            termination = "runner_error"
            self._terminate_process_tree()
            background_job_cleanup = self._cancel_workspace_execution_jobs(
                reason=termination
            )
            trace_stop.set()
            trace_thread.join(timeout=2)
            opencode_database_sync = self._sync_opencode_database()
            try:
                model_io = export_model_io_trace(self.workspace)
            except Exception as trace_exc:
                model_io = {"error": f"{type(trace_exc).__name__}: {trace_exc}"}
            self._write_meta(
                "failed",
                {
                    "error": f"{type(exc).__name__}: {exc}",
                    "model_io_trace": model_io,
                    "background_job_cleanup": background_job_cleanup,
                    "opencode_database_sync": opencode_database_sync,
                },
            )
            write_workspace_results(self.workspace)
            reporter.emit("RUN_ERROR", error=f"{type(exc).__name__}: {exc}")
            reporter.close()
            raise
        finally:
            duration = round(time.monotonic() - started, 3)

        trace_stop.set()
        trace_thread.join(timeout=2)

        report_path = self.workspace / "report" / "report.md"
        report_exists = report_path.is_file() and bool(
            report_path.read_text(encoding="utf-8", errors="replace").strip()
        )
        completed = exit_code == 0 and report_exists and termination == "process_exit"
        status = "completed" if completed else "failed"
        events = load_tool_trace(self.workspace)
        try:
            model_io = export_model_io_trace(self.workspace)
        except Exception as exc:
            model_io = {"error": f"{type(exc).__name__}: {exc}"}
        metadata = {
            "exit_code": exit_code,
            "termination": termination,
            "duration_seconds": duration,
            "model": self._detect_model(),
            "report_exists": report_exists,
            "required_deliverable_status": self._required_deliverable_status(),
            "model_io_trace": model_io,
            **process_metrics(events, workspace=self.workspace),
        }
        if background_job_cleanup is not None:
            metadata["background_job_cleanup"] = background_job_cleanup
        if opencode_database_sync is not None:
            metadata["opencode_database_sync"] = opencode_database_sync
        self._write_meta(status, metadata)
        write_workspace_results(self.workspace)
        reporter.emit(
            "RUN_END",
            status=status,
            termination=termination,
            exit_code=exit_code,
            duration_seconds=duration,
            report_exists=report_exists,
            tool_calls=metadata.get("tool_call_count"),
            successful_tools=metadata.get("successful_tool_calls"),
            failed_tools=metadata.get("failed_tool_calls"),
            model_io_path=(model_io.get("path") if isinstance(model_io, dict) else None),
        )
        reporter.close()
        return json.loads(self.meta_path.read_text(encoding="utf-8"))

    def run_async(self) -> str:
        self.setup_workspace()
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()
        return self.run_id
