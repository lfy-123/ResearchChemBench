"""Agent-specific environments, configuration files, and CLI arguments."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import sqlite3
import tempfile
from pathlib import Path
from typing import Any

from chemistry_toolbox.src.catalog import TOOL_DISCOVERY_MODE_ENV

from ..settings import (
    OPENCODE_BASE_URL,
    OPENCODE_MODEL,
    PROJECT_ROOT,
    chemistry_server_specs,
)


class AgentAdapterMixin:
    def capture_provider_event(self, line: str) -> dict:
        try:
            event = json.loads(line)
        except (ValueError, TypeError):
            return {}
        if not isinstance(event, dict): return {}
        if self.agent.get("kind") == "external":
            from ..agent_plugins.protocol import normalize_external_event
            return normalize_external_event(event, run_id=self.run_id) or {}
        if event.get("type") == "thread.started":
            value = event.get("thread_id")
            if isinstance(value, str) and value:
                if self._resume_session_id and value != self._resume_session_id:
                    from .recovery import RunRecoveryError
                    raise RunRecoveryError("provider_resumed_a_different_session")
                self._resume_session_id = value
                if self.recovery_enabled:
                    self._persist_run_manifest(run_state="running", provider_session_id=value)
        return event

    def capture_provider_session_id(self) -> str | None:
        if self.output_path.is_file():
            for line in self.output_path.read_text(encoding="utf-8", errors="replace").splitlines():
                self.capture_provider_event(line)
        return self._resume_session_id

    def _runtime_pythonpath(self) -> str:
        values = [str(PROJECT_ROOT)]
        existing = os.environ.get("PYTHONPATH", "")
        if existing:
            values.append(existing)
        return os.pathsep.join(values)

    def _mcp_environment(self, extra: dict[str, str] | None = None) -> dict[str, str]:
        values = {
            "RESEARCHCHEMBENCH_WORKSPACE": str(self.workspace.resolve()),
            "RESEARCHCHEMBENCH_RUN_ID": self.run_id,
            TOOL_DISCOVERY_MODE_ENV: self.tool_discovery_mode,
            "PYTHONPATH": self._runtime_pythonpath(),
            "RESEARCHCHEM_TOOL_LOG_DIR": str(
                (self.workspace / "tool_logs").resolve()
            ),
            "RESEARCHCHEMBENCH_COMPUTE_ACTION_TIMEOUT_SECONDS": str(
                self.compute_action_timeout_seconds
            ),
            "RESEARCHCHEMBENCH_FAST_ACTION_TIMEOUT_SECONDS": str(
                self.fast_action_timeout_seconds
            ),
            "RESEARCHCHEMBENCH_AVAILABLE_CPU_CORES": str(
                self.available_cpu_cores
            ),
            "RESEARCHCHEMBENCH_AVAILABLE_MEMORY_MB": str(
                self.available_memory_mb
            ),
            "RESEARCHCHEMBENCH_AVAILABLE_GPU_COUNT": str(
                self.available_gpu_count
            ),
            "RESEARCHCHEMBENCH_EXECUTION_MODE": self.execution_mode,
            "RESEARCHCHEMBENCH_JOB_EVENT_SETTLE_SECONDS": str(
                self.job_event_settle_seconds
            ),
            "RESEARCHCHEMBENCH_JOB_EVENT_MAX_BATCH_SECONDS": str(
                self.job_event_max_batch_seconds
            ),
            "RESEARCHCHEMBENCH_JOB_WAIT_HEARTBEAT_SECONDS": str(
                self.job_wait_heartbeat_seconds
            ),
            "RESEARCHCHEMBENCH_JOB_INTERNAL_POLL_INTERVAL_SECONDS": str(
                self.job_internal_poll_interval_seconds
            ),
            "RESEARCHCHEMBENCH_JOB_FAILURE_TAIL_CHARS": str(
                self.job_failure_tail_chars
            ),
        }
        if self.recovery_enabled or self.agent.get("kind") == "external":
            values["RESEARCHCHEMBENCH_RECOVERY_ENABLED"] = "1"
        # Omit the new variable for restored legacy manifests to preserve their
        # frozen MCP configuration hash; legacy is the toolbox's default.
        if self.electronic_state_policy != "legacy":
            values["RESEARCHCHEMBENCH_ELECTRONIC_STATE_POLICY"] = self.electronic_state_policy
        if self.recovery_enabled or self.agent.get("kind") == "external":
            values["RCB_AGENT_RUN_TOKEN"] = hashlib.sha256((str(self.workspace.resolve()) + self.run_id).encode()).hexdigest()
            values["RESEARCHCHEMBENCH_RUN_DEADLINE"] = str(self.deadline_at or "")
            from chemistry_toolbox.src.recovery_io import control_directory
            import socket
            values["RESEARCHCHEMBENCH_GLOBAL_RESOURCE_ALLOCATION_ROOT"] = os.environ.get(
                "RESEARCHCHEMBENCH_GLOBAL_RESOURCE_ALLOCATION_ROOT",
                str(control_directory(self.workspace, self.run_id).parent / ("host_" + socket.gethostname())))
        if self.execution_mode == "distributed":
            for name in (
                "RCB_DISTRIBUTED_TRANSPORT",
                "RCB_DISTRIBUTED_INVENTORY",
                "RCB_DISTRIBUTED_WORKER_INVENTORY",
                "RCB_DISTRIBUTED_SANDBOX_INVENTORY",
                "RCB_DISTRIBUTED_STATE_ROOT",
                "RCB_DISTRIBUTED_DIRECT_SSH_OPTIONS",
                "RCB_DISTRIBUTED_KNOWN_HOSTS_FILE",
                "RCB_DISTRIBUTED_LEASE_TIMEOUT_SECONDS",
                "RCB_SANDBOX_API_KEY",
            ):
                if os.environ.get(name):
                    values[name] = os.environ[name]
        if extra:
            values.update(extra)
        if self.feedback_schema_version != 1:
            values["RESEARCHCHEMBENCH_FEEDBACK_SCHEMA_VERSION"] = str(self.feedback_schema_version)
        if self.native_input_validation_policy != "legacy":
            values["RESEARCHCHEMBENCH_NATIVE_INPUT_VALIDATION_POLICY"] = self.native_input_validation_policy
        if self.model_wait_strategy == "host_event_wait":
            values["RESEARCHCHEMBENCH_JOB_WAIT_MODE"] = "event"
        return values

    def _mcp_server_specs(self) -> list[dict[str, Any]]:
        values = []
        for spec in chemistry_server_specs(self.tool_discovery_mode):
            item = dict(spec)
            item["environment"] = self._mcp_environment(
                dict(spec.get("environment") or {})
            )
            if self.agent.get("kind") == "codex":
                # The evaluator authorizes its own scoped toolbox for unattended
                # runs. Codex's global `never` policy otherwise rejects MCP
                # calls that would ask for approval. Include this server policy
                # in the frozen MCP hash so restore cannot silently change it.
                item["default_tools_approval_mode"] = "approve"
            values.append(item)
        if self.model_wait_strategy == "host_event_wait":
            original = values[0]
            original["disabled_tools"] = ["wait_execution_jobs", "wait_execution_events"]
            wait_spec = {**original, "name": "chemistry_wait", "command": [*original["command"], "--wait-only"]}
            wait_spec.pop("disabled_tools", None)
            values.append(wait_spec)
        return values

    def _agent_environment(self) -> dict[str, str]:
        """Build child environment without exposing benchmark judge credentials."""

        if self.agent.get("kind") == "external":
            from ..agent_plugins.external import build_external_environment
            return build_external_environment(self, self.agent)
        env = os.environ.copy()
        env.pop("JUDGE_API_KEY", None)
        env.update(self._mcp_environment())
        env["PYTHONUNBUFFERED"] = "1"
        # Git discovery must stop at the run workspace, also on session resume.
        # This is a discovery boundary, not a filesystem access sandbox.
        ceilings = [value for value in env.get("GIT_CEILING_DIRECTORIES", "").split(os.pathsep) if value]
        env["GIT_CEILING_DIRECTORIES"] = os.pathsep.join(dict.fromkeys(
            [*ceilings, str(self.workspace.resolve()), str(self.workspace.resolve().parent)]))
        for key in ("GIT_DIR", "GIT_WORK_TREE", "GIT_COMMON_DIR", "GIT_INDEX_FILE", "GIT_OBJECT_DIRECTORY", "GIT_ALTERNATE_OBJECT_DIRECTORIES"):
            env.pop(key, None)
        if self.agent.get("kind") == "codex":
            # Keep provider session records inside the run so an exact resume
            # cannot accidentally select an operator's unrelated ~/.codex
            # conversation. Authentication/model overrides are still supplied
            # by the configured adapter and are never written to the manifest.
            from .codex_history import session_home
            from .recovery import runner_store
            codex_home = session_home(runner_store(self))
            codex_home.mkdir(parents=True, exist_ok=True)
            env["CODEX_HOME"] = str(codex_home.resolve())
            if os.environ.get("RCB_CODEX_API_KEY"):
                env["RCB_CODEX_API_KEY"] = os.environ["RCB_CODEX_API_KEY"]
        if self.agent.get("kind") == "opencode":
            runtime_root = Path(
                os.environ.get(
                    "RESEARCHCHEMBENCH_OPENCODE_RUNTIME_ROOT",
                    str(Path(tempfile.gettempdir()) / "researchchembench-opencode"),
                )
            )
            database_directory = runtime_root / self.run_id
            database_directory.mkdir(parents=True, exist_ok=True)
            self._opencode_runtime_database = database_directory / "opencode.db"
            env["OPENCODE_DB"] = str(self._opencode_runtime_database.resolve())
            # OpenCode 1.18 interprets OPENCODE_WORKSPACE_ID as the identifier of
            # an already-created OpenCode workspace/session. A benchmark run ID
            # is not such an identifier and makes `opencode run` fail before the
            # first model call with "Session not found". Keep the live SQLite WAL
            # on node-local storage to avoid mmap/SIGBUS failures on network file
            # systems; the closed database is archived into the run workspace.
            env.pop("OPENCODE_WORKSPACE_ID", None)
        return env

    def _sync_opencode_database(self) -> dict[str, Any]:
        """Archive the closed node-local OpenCode database into the workspace."""

        source = self._opencode_runtime_database
        if self.agent.get("kind") != "opencode" or source is None:
            return {"status": "not_applicable"}
        destination_dir = self.workspace / "_opencode"
        destination = destination_dir / "opencode.db"
        record: dict[str, Any] = {
            "status": "missing",
            "runtime_database": str(source),
            "archive_database": str(destination),
        }
        if not source.is_file():
            return record

        destination_dir.mkdir(parents=True, exist_ok=True)
        temporary = destination.with_suffix(".db.sync.tmp")
        temporary.unlink(missing_ok=True)
        try:
            with sqlite3.connect(f"file:{source}?mode=ro", uri=True) as source_db:
                with sqlite3.connect(temporary) as archive_db:
                    source_db.backup(archive_db)
            os.replace(temporary, destination)
            for suffix in ("-wal", "-shm"):
                (destination_dir / f"opencode.db{suffix}").unlink(missing_ok=True)
            record.update(
                {
                    "status": "archived",
                    "size_bytes": destination.stat().st_size,
                    "sha256": hashlib.sha256(destination.read_bytes()).hexdigest(),
                }
            )
        except Exception as exc:
            temporary.unlink(missing_ok=True)
            record.update(
                {
                    "status": "failed",
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )
        finally:
            if record["status"] == "archived":
                shutil.rmtree(source.parent, ignore_errors=True)
        return record

    def _write_claude_mcp_config(self) -> Path:
        servers = {}
        for spec in self._mcp_server_specs():
            command = spec["command"]
            servers[spec["name"]] = {
                    "type": "stdio",
                    "command": command[0],
                    "args": command[1:],
                    "env": spec["environment"],
            }
        config = {"mcpServers": servers}
        path = self.workspace / ".mcp.json"
        path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
        return path

    def _write_opencode_config(self) -> Path:
        """Write a run-local OpenCode provider and Chemistry MCP configuration."""

        server_specs = self._mcp_server_specs()
        model = OPENCODE_MODEL
        if "/" in model:
            provider, model_id = model.split("/", 1)
        else:
            provider, model_id = "deepseek", model
            model = f"{provider}/{model_id}"
        base_url = OPENCODE_BASE_URL
        config = {
            "$schema": "https://opencode.ai/config.json",
            "model": model,
            "small_model": model,
            "provider": {
                provider: {
                    "npm": "@ai-sdk/openai-compatible",
                    "name": provider,
                    # Resolve the credential only inside the Agent process.
                    # Custom provider IDs otherwise prefer OpenCode's saved
                    # provider credential, which can silently ignore the
                    # benchmark's OPENAI_API_KEY. The placeholder keeps the
                    # actual secret out of the run-local config artifact.
                    "options": {
                        "baseURL": base_url,
                        "apiKey": "{env:OPENAI_API_KEY}",
                    },
                    "models": {model_id: {"name": model_id}},
                }
            },
            "agent": {
                # OpenCode does not expose a run-level --max-turns flag. Apply
                # the benchmark budget to both the primary build Agent and the
                # general child Agent used by the task tool.
                "build": {"steps": self.max_turns},
                "general": {"steps": self.max_turns},
            },
            "mcp": {
                spec["name"]: {
                    "type": "local",
                    "command": spec["command"],
                    "environment": spec["environment"],
                    # OpenCode otherwise applies a 30 s timeout to both MCP
                    # discovery and tool execution. Scientific backends such
                    # as finite-difference Hessians routinely exceed that.
                    "timeout": self.mcp_tool_timeout_ms,
                    "enabled": True,
                }
                for spec in server_specs
            },
        }
        path = self.workspace / "opencode.json"
        path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
        return path

    @staticmethod
    def _toml_string(value: str) -> str:
        return json.dumps(value)

    def build_agent_argv(self) -> list[str]:
        kind = self.agent.get("kind")
        if kind == "external":
            from ..agent_plugins.external import build_external_argv
            return build_external_argv(self.agent, self.workspace / "_agent_protocol/request.json")
        executable = self.agent.get("executable", "")
        prompt = self.instructions_path.read_text(encoding="utf-8")
        server_specs = self._mcp_server_specs()

        if kind == "mock":
            return [
                os.environ.get("RESEARCHCHEMBENCH_PYTHON", os.sys.executable),
                "-m",
                "evaluation.testing.mock_agent",
                "--workspace",
                str(self.workspace.resolve()),
                "--prompt-file",
                str(self.instructions_path.resolve()),
            ]

        if kind == "codex":
            argv = [
                executable,
                "exec",
            ]
            if self._resume_session_id:
                # Codex's resume command accepts an explicit session ID.  Do
                # not use --last: the benchmark must never resume an operator's
                # unrelated conversation.
                argv.append("resume")
                argv.append(str(self._resume_session_id))
            argv.extend(["--ignore-user-config", "--skip-git-repo-check", "--json"])
            settings = {
                "model": self.codex_model, "model_reasoning_effort": self.codex_reasoning_effort,
                "model_provider": "rcb", "model_providers.rcb.name": "ResearchChemBench",
                "model_providers.rcb.base_url": self.codex_base_url,
                "model_providers.rcb.env_key": "RCB_CODEX_API_KEY",
                "model_providers.rcb.wire_api": "responses",
                "sandbox_mode": "workspace-write", "approval_policy": "never",
                "sandbox_workspace_write.network_access": True,
            }
            if self.model_wait_strategy == "host_event_wait":
                settings["features.code_mode.direct_only_tool_namespaces"] = ["mcp__chemistry_wait"]
            for name, value in settings.items():
                argv.extend(["-c", name + "=" + json.dumps(value)])
            if not self._resume_session_id:
                argv.extend(
                    [
                        "-C",
                        str(self.workspace.resolve()),
                        "--sandbox",
                        "workspace-write",
                    ]
                )
            argv.extend(
                [
                    "--output-last-message",
                    str(self.final_message_path.resolve()),
                ]
            )
            for spec in server_specs:
                name = spec["name"]
                command = spec["command"]
                if spec.get("disabled_tools"):
                    argv.extend(["-c", f"mcp_servers.{name}.disabled_tools=" + json.dumps(spec["disabled_tools"])])
                argv.extend(
                    [
                        "-c",
                        f"mcp_servers.{name}.command={self._toml_string(command[0])}",
                        "-c",
                        f"mcp_servers.{name}.args={json.dumps(command[1:])}",
                        "-c",
                        f"mcp_servers.{name}.required=true",
                        "-c",
                        f"mcp_servers.{name}.default_tools_approval_mode="
                        + self._toml_string(spec["default_tools_approval_mode"]),
                        "-c",
                        f"mcp_servers.{name}.startup_timeout_sec=60",
                        "-c",
                        (
                            f"mcp_servers.{name}.tool_timeout_sec="
                            f"{max(1, (self.mcp_tool_timeout_ms + 999) // 1000)}"
                        ),
                    ]
                )
                for key, value in spec["environment"].items():
                    argv.extend(
                        [
                            "-c",
                            f"mcp_servers.{name}.env.{key}={self._toml_string(value)}",
                        ]
                    )
            argv.append((self._recovery_notice or "Continue the original run.") if self._resume_session_id else prompt)
            return argv

        if kind == "claude":
            allowed_mcp = [f"mcp__{spec['name']}__*" for spec in server_specs]
            return [
                executable,
                "-p",
                "--strict-mcp-config",
                "--mcp-config",
                str((self.workspace / ".mcp.json").resolve()),
                "--output-format",
                "stream-json",
                "--verbose",
                "--max-turns",
                str(self.max_turns),
                "--tools",
                "Read,Write,Edit",
                "--allowedTools",
                ",".join(["Read", "Write", "Edit", *allowed_mcp]),
                "--permission-mode",
                "dontAsk",
                "--disable-slash-commands",
                "--no-session-persistence",
                prompt,
            ]

        if kind == "opencode":
            model = OPENCODE_MODEL
            if "/" not in model:
                model = f"deepseek/{model}"
            return [
                executable,
                "run",
                "--pure",
                "--dir",
                str(self.workspace.resolve()),
                "--model",
                model,
                "--format",
                "json",
                "--auto",
                prompt,
            ]

        command_template = self.agent.get("cmd")
        if command_template:
            raise ValueError(
                "String shell commands are not enabled for built-in runs; add a structured adapter"
            )
        raise ValueError(f"Unsupported agent kind: {kind}")

    def command_preview(self) -> list[str]:
        argv = self.build_agent_argv()
        prompt = self.instructions_path.read_text(encoding="utf-8")
        return ["<PROMPT>" if item == prompt else item for item in argv]
