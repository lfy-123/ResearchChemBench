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
        return values

    def _mcp_server_specs(self) -> list[dict[str, Any]]:
        values = []
        for spec in chemistry_server_specs(self.tool_discovery_mode):
            item = dict(spec)
            item["environment"] = self._mcp_environment(
                dict(spec.get("environment") or {})
            )
            values.append(item)
        return values

    def _agent_environment(self) -> dict[str, str]:
        """Build child environment without exposing benchmark judge credentials."""

        env = os.environ.copy()
        env.pop("JUDGE_API_KEY", None)
        env.update(self._mcp_environment())
        env["PYTHONUNBUFFERED"] = "1"
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
                "--ignore-user-config",
                "--skip-git-repo-check",
                "-C",
                str(self.workspace.resolve()),
                "--sandbox",
                "workspace-write",
                "--json",
                "--output-last-message",
                str(self.final_message_path.resolve()),
            ]
            for spec in server_specs:
                name = spec["name"]
                command = spec["command"]
                argv.extend(
                    [
                        "-c",
                        f"mcp_servers.{name}.command={self._toml_string(command[0])}",
                        "-c",
                        f"mcp_servers.{name}.args={json.dumps(command[1:])}",
                        "-c",
                        f"mcp_servers.{name}.required=true",
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
            argv.append(prompt)
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
