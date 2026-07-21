"""Workspace construction and external agent CLI execution."""

from __future__ import annotations

import json
import os
import queue
import shutil
import subprocess
import threading
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from .config import (
    AGENT_PRESETS,
    CHEMGRAPH_SRC,
    DEFAULT_AGENT_TIMEOUT_SECONDS,
    DEFAULT_MCP_TOOL_TIMEOUT_MS,
    DEFAULT_MAX_TURNS,
    OPENCODE_BASE_URL,
    OPENCODE_MODEL,
    PROJECT_ROOT,
    TASKS_DIR,
    WORKSPACES_DIR,
    chemistry_server_command,
    chemistry_server_specs,
)
from .instructions_tmpl import INSTRUCTIONS_TEMPLATE
from .trace import load_tool_trace, process_metrics
from .utils import load_task_info
from researchchem_toolbox.catalog import agent_toolbox_overview, catalog_snapshot


class TaskRunner:
    """Set up one benchmark workspace and run one configured agent."""

    def __init__(
        self,
        task_id: str,
        *,
        agent_key: str = "mock",
        workspace_root: Path | None = None,
        timeout_seconds: int = DEFAULT_AGENT_TIMEOUT_SECONDS,
        max_turns: int = DEFAULT_MAX_TURNS,
    ):
        if agent_key not in AGENT_PRESETS:
            raise ValueError(f"Unknown agent preset: {agent_key}")
        self.task_id = task_id
        self.task_dir = TASKS_DIR / task_id
        self.task_info = load_task_info(task_id)
        self.agent_key = agent_key
        self.agent = AGENT_PRESETS[agent_key]
        self.agent_name = self.agent["label"]
        self.timeout_seconds = timeout_seconds
        self.max_turns = max_turns
        self.timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        self.run_id = f"{task_id}_{agent_key}_{self.timestamp}_{uuid.uuid4().hex[:6]}"
        root = Path(workspace_root) if workspace_root else WORKSPACES_DIR
        self.workspace = root / self.run_id
        self.meta_path = self.workspace / "_meta.json"
        self.output_path = self.workspace / "_agent_output.jsonl"
        self.instructions_path = self.workspace / "INSTRUCTIONS.md"
        self.final_message_path = self.workspace / "_final_message.txt"
        self.process: subprocess.Popen[str] | None = None
        self.thread: threading.Thread | None = None
        self._stop_requested = False

    def _build_instructions(self) -> str:
        data_parts = []
        for item in self.task_info.get("data", []):
            type_text = f" [{item.get('type')}]" if item.get("type") else ""
            data_parts.append(
                f"- **{item.get('name', '')}**{type_text} "
                f"(`{item.get('path', '')}`): {item.get('description', '')}"
            )
        data_text = "\n".join(data_parts) if data_parts else "No additional input files."
        return INSTRUCTIONS_TEMPLATE.format(
            workspace=str(self.workspace.resolve()),
            task_desc=self.task_info["task"],
            category=self.task_info.get("category", "uncategorized"),
            data_text=data_text,
            toolbox_overview=agent_toolbox_overview(
                include_health=True,
                snapshot=(
                    json.loads((self.workspace / "_toolbox_catalog.json").read_text(encoding="utf-8"))
                    if (self.workspace / "_toolbox_catalog.json").is_file()
                    else None
                ),
            ),
        )

    def _runtime_pythonpath(self) -> str:
        values = [str(PROJECT_ROOT), str(CHEMGRAPH_SRC)]
        existing = os.environ.get("PYTHONPATH", "")
        if existing:
            values.append(existing)
        return os.pathsep.join(values)

    def _mcp_environment(self, extra: dict[str, str] | None = None) -> dict[str, str]:
        values = {
            "RESEARCHCHEMBENCH_WORKSPACE": str(self.workspace.resolve()),
            "RESEARCHCHEMBENCH_RUN_ID": self.run_id,
            "PYTHONPATH": self._runtime_pythonpath(),
            "CHEMGRAPH_LOG_DIR": str((self.workspace / "tool_logs").resolve()),
        }
        if extra:
            values.update(extra)
        return values

    def _mcp_server_specs(self) -> list[dict[str, Any]]:
        values = []
        for spec in chemistry_server_specs():
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
            database_directory = self.workspace / "_opencode"
            database_directory.mkdir(parents=True, exist_ok=True)
            env["OPENCODE_DB"] = str((database_directory / "opencode.db").resolve())
            env["OPENCODE_WORKSPACE_ID"] = self.run_id
        return env

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
                    "options": {"baseURL": base_url},
                    "models": {model_id: {"name": model_id}},
                }
            },
            "mcp": {
                spec["name"]: {
                    "type": "local",
                    "command": spec["command"],
                    "environment": spec["environment"],
                    # OpenCode otherwise applies a 30 s timeout to both MCP
                    # discovery and tool execution. Scientific backends such
                    # as finite-difference Hessians routinely exceed that.
                    "timeout": DEFAULT_MCP_TOOL_TIMEOUT_MS,
                    "enabled": True,
                }
                for spec in server_specs
            },
        }
        path = self.workspace / "opencode.json"
        path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
        return path

    def setup_workspace(self) -> None:
        if not self.task_dir.is_dir():
            raise FileNotFoundError(f"Task not found: {self.task_id}")
        self.workspace.mkdir(parents=True, exist_ok=False)
        source_data = self.task_dir / "data"
        if source_data.exists():
            shutil.copytree(source_data, self.workspace / "data", dirs_exist_ok=True)
        else:
            (self.workspace / "data").mkdir()
        for directory in (
            "code",
            "outputs",
            "report",
            "report/images",
            "tool_logs",
            "_tool_results",
            "_tool_artifacts",
        ):
            (self.workspace / directory).mkdir(parents=True, exist_ok=True)

        # Input data is copied but made read-only for the normal benchmark path.
        for path in (self.workspace / "data").rglob("*"):
            if path.is_file():
                path.chmod(0o444)

        (self.workspace / "_toolbox_catalog.json").write_text(
            json.dumps(catalog_snapshot(include_health=True), indent=2, ensure_ascii=False)
            + "\n",
            encoding="utf-8",
        )
        self.instructions_path.write_text(self._build_instructions(), encoding="utf-8")
        self._write_claude_mcp_config()
        self._write_opencode_config()
        self._write_meta("ready")

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
                "evaluation.mock_agent",
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
                        f"mcp_servers.{name}.tool_timeout_sec=3600",
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
            return [
                executable,
                "run",
                "--pure",
                "--dir",
                str(self.workspace.resolve()),
                "--model",
                OPENCODE_MODEL,
                "--format",
                "json",
                "--dangerously-skip-permissions",
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
            "query": self.task_info.get("task", ""),
            "category": self.task_info.get("category", ""),
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
        if self.process and self.process.poll() is None:
            self.process.terminate()

    def run(self) -> dict[str, Any]:
        if not self.workspace.exists():
            self.setup_workspace()
        argv = self.build_agent_argv()
        self._write_meta("running", {"agent_command": self.command_preview()})
        env = self._agent_environment()
        started = time.monotonic()
        termination = "process_exit"
        exit_code = -1

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
            )
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
            with self.output_path.open("w", encoding="utf-8") as output:
                while not stream_done:
                    if time.monotonic() - started > self.timeout_seconds:
                        termination = "timeout"
                        self.process.terminate()
                        break
                    try:
                        line = line_queue.get(timeout=0.2)
                    except queue.Empty:
                        if self.process.poll() is not None and not reader.is_alive():
                            break
                        continue
                    if line is None:
                        stream_done = True
                    elif line:
                        output.write(line + "\n")
                        output.flush()

            try:
                exit_code = self.process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                self.process.kill()
                exit_code = self.process.wait()
            if self._stop_requested:
                termination = "stopped"
        except Exception as exc:
            termination = "runner_error"
            if self.process and self.process.poll() is None:
                self.process.terminate()
            self._write_meta("failed", {"error": f"{type(exc).__name__}: {exc}"})
            raise
        finally:
            duration = round(time.monotonic() - started, 3)

        report_path = self.workspace / "report" / "report.md"
        report_exists = report_path.is_file() and bool(
            report_path.read_text(encoding="utf-8", errors="replace").strip()
        )
        completed = exit_code == 0 and report_exists and termination == "process_exit"
        status = "completed" if completed else "failed"
        events = load_tool_trace(self.workspace)
        metadata = {
            "exit_code": exit_code,
            "termination": termination,
            "duration_seconds": duration,
            "model": self._detect_model(),
            "report_exists": report_exists,
            **process_metrics(events),
        }
        self._write_meta(status, metadata)
        return json.loads(self.meta_path.read_text(encoding="utf-8"))

    def run_async(self) -> str:
        self.setup_workspace()
        self.thread = threading.Thread(target=self.run, daemon=True)
        self.thread.start()
        return self.run_id
