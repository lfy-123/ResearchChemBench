"""Workspace construction and external agent CLI execution."""

from __future__ import annotations

import hashlib
import json
import os
import queue
import shutil
import signal
import stat
import subprocess
import threading
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from pathlib import PurePosixPath
from typing import Any
from zipfile import ZipFile

from .config import (
    AGENT_PRESETS,
    CHEMGRAPH_SRC,
    DEFAULT_AVAILABLE_CPU_CORES,
    DEFAULT_AVAILABLE_GPU_COUNT,
    DEFAULT_AVAILABLE_MEMORY_MB,
    DEFAULT_AGENT_TIMEOUT_SECONDS,
    DEFAULT_COMPUTE_ACTION_TIMEOUT_SECONDS,
    DEFAULT_FAST_ACTION_TIMEOUT_SECONDS,
    DEFAULT_LIVE_PROGRESS,
    DEFAULT_MCP_TOOL_TIMEOUT_MS,
    DEFAULT_MAX_TURNS,
    DEFAULT_PROGRESS_CONSOLE,
    DEFAULT_PROGRESS_MAX_CHARS,
    JUDGE_MODEL_NAME,
    OPENCODE_BASE_URL,
    OPENCODE_MODEL,
    PROJECT_ROOT,
    TASKS_DIR,
    WORKSPACES_DIR,
    chemistry_server_command,
    chemistry_server_specs,
)
from .instructions_tmpl import INSTRUCTIONS_TEMPLATE
from .live_progress import LiveProgressReporter
from .model_io import export_model_io_trace
from .results import write_workspace_results
from .trace import load_tool_trace, process_metrics
from .utils import load_task_info
from researchchem_toolbox.catalog import (
    TOOL_DISCOVERY_MODE_ENV,
    catalog_snapshot,
    resolve_tool_discovery_mode,
    toolbox_overview,
)


TERMINAL_EXECUTION_JOB_STATES = {"success", "failed", "timeout", "cancelled"}


class TaskRunner:
    """Set up one benchmark workspace and run one configured agent."""

    def __init__(
        self,
        task_id: str,
        *,
        agent_key: str = "mock",
        workspace_root: Path | None = None,
        timeout_seconds: int = DEFAULT_AGENT_TIMEOUT_SECONDS,
        compute_action_timeout_seconds: int = DEFAULT_COMPUTE_ACTION_TIMEOUT_SECONDS,
        fast_action_timeout_seconds: int = DEFAULT_FAST_ACTION_TIMEOUT_SECONDS,
        mcp_tool_timeout_ms: int = DEFAULT_MCP_TOOL_TIMEOUT_MS,
        available_cpu_cores: int = DEFAULT_AVAILABLE_CPU_CORES,
        available_memory_mb: int = DEFAULT_AVAILABLE_MEMORY_MB,
        available_gpu_count: int = DEFAULT_AVAILABLE_GPU_COUNT,
        max_turns: int = DEFAULT_MAX_TURNS,
        tool_discovery_mode: str | None = None,
        live_progress: bool = DEFAULT_LIVE_PROGRESS,
        progress_console: bool = DEFAULT_PROGRESS_CONSOLE,
        progress_max_chars: int = DEFAULT_PROGRESS_MAX_CHARS,
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
        self.compute_action_timeout_seconds = int(compute_action_timeout_seconds)
        self.fast_action_timeout_seconds = int(fast_action_timeout_seconds)
        self.mcp_tool_timeout_ms = int(mcp_tool_timeout_ms)
        self.available_cpu_cores = int(available_cpu_cores)
        self.available_memory_mb = int(available_memory_mb)
        self.available_gpu_count = int(available_gpu_count)
        if self.available_cpu_cores < 1:
            raise ValueError("available_cpu_cores must be positive")
        if self.available_memory_mb < 128:
            raise ValueError("available_memory_mb must be >= 128")
        if self.available_gpu_count < 0:
            raise ValueError("available_gpu_count must be non-negative")
        self.max_turns = max_turns
        self.tool_discovery_mode = resolve_tool_discovery_mode(tool_discovery_mode)
        self.live_progress = bool(live_progress)
        self.progress_console = bool(progress_console)
        self.progress_max_chars = max(80, int(progress_max_chars))
        self.timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        self.run_id = f"{task_id}_{agent_key}_{self.timestamp}_{uuid.uuid4().hex[:6]}"
        root = Path(workspace_root) if workspace_root else WORKSPACES_DIR
        self.workspace = root / self.run_id
        self.meta_path = self.workspace / "_meta.json"
        self.output_path = self.workspace / "_agent_output.jsonl"
        self.instructions_path = self.workspace / "INSTRUCTIONS.md"
        self.final_message_path = self.workspace / "_final_message.txt"
        self.process: subprocess.Popen[str] | None = None
        self.process_group_id: int | None = None
        self.thread: threading.Thread | None = None
        self._stop_requested = False

    def resource_budget_record(self) -> dict[str, Any]:
        return {
            "cpu_cores": self.available_cpu_cores,
            "memory_mb": self.available_memory_mb,
            "gpu_count": self.available_gpu_count,
            "source": "evaluation_policy",
            "agent_controllable": False,
            "scope": "per_task",
        }

    def _build_instructions(self) -> str:
        data_parts = []
        for item in self.task_info.get("data", []):
            type_text = f" [{item.get('type')}]" if item.get("type") else ""
            data_parts.append(
                f"- **{item.get('name', '')}**{type_text} "
                f"(`{item.get('path', '')}`): {item.get('description', '')}"
            )
        data_text = "\n".join(data_parts) if data_parts else "No additional input files."
        scientific_requirements = self.task_info.get("scientific_requirements") or []
        requirements_text = (
            "\n".join(
                f"{index}. {requirement}"
                for index, requirement in enumerate(scientific_requirements, start=1)
            )
            if scientific_requirements
            else "Follow the scientific validity requirements stated in the task."
        )
        deliverables = self.task_info.get("required_deliverables") or []
        deliverable_lines = []
        for item in deliverables:
            if isinstance(item, str):
                deliverable_lines.append(f"- `{item}`")
                continue
            path = str(item.get("path") or "").strip()
            description = str(item.get("description") or "").strip()
            if path:
                deliverable_lines.append(
                    f"- `{path}`" + (f": {description}" if description else "")
                )
        required_deliverables = (
            "\n".join(deliverable_lines)
            if deliverable_lines
            else "- `report/report.md`: final answer and artifact-linked scientific account."
        )
        return INSTRUCTIONS_TEMPLATE.format(
            workspace=str(self.workspace.resolve()),
            task_desc=self.task_info["task"],
            category=self.task_info.get("category", "uncategorized"),
            data_text=data_text,
            scientific_mode=self.task_info.get(
                "scientific_mode", "standard_autonomous_investigation"
            ),
            scientific_mode_description=self.task_info.get(
                "scientific_mode_description",
                "The objective is fixed, while scientific planning and execution remain autonomous.",
            ),
            scientific_requirements=requirements_text,
            available_cpu_cores=self.available_cpu_cores,
            available_memory_mb=self.available_memory_mb,
            available_gpu_count=self.available_gpu_count,
            required_deliverables=required_deliverables,
            toolbox_overview=toolbox_overview(
                discovery_mode=self.tool_discovery_mode,
                include_health=True,
                snapshot=(
                    json.loads((self.workspace / "_toolbox_catalog.json").read_text(encoding="utf-8"))
                    if (self.workspace / "_toolbox_catalog.json").is_file()
                    else None
                ),
            ),
        )

    def _required_deliverable_status(self) -> list[dict[str, Any]]:
        """Record task-specific evidence-product presence without making it a run gate."""

        values: list[dict[str, Any]] = []
        root = self.workspace.resolve()
        for item in self.task_info.get("required_deliverables") or []:
            specification = {"path": item} if isinstance(item, str) else dict(item)
            relative = str(specification.get("path") or "").strip()
            if not relative or Path(relative).is_absolute():
                continue
            path = (root / relative).resolve()
            try:
                path.relative_to(root)
            except ValueError:
                continue
            exists = path.is_file()
            size = path.stat().st_size if exists else 0
            allow_empty = bool(specification.get("allow_empty", False))
            values.append(
                {
                    "path": relative,
                    "exists": exists,
                    "size_bytes": size,
                    "satisfied": exists and (allow_empty or size > 0),
                    "allow_empty": allow_empty,
                }
            )
        return values

    @staticmethod
    def _resolve_under(base: Path, relative_path: str, *, field: str) -> Path:
        if not relative_path or Path(relative_path).is_absolute():
            raise ValueError(f"{field} must be a non-empty relative path")
        base = base.resolve()
        resolved = (base / relative_path).resolve()
        try:
            resolved.relative_to(base)
        except ValueError as exc:
            raise ValueError(f"{field} escapes the task data directory") from exc
        return resolved

    def _extract_task_archives(self) -> None:
        data_root = (self.workspace / "data").resolve()
        for specification in self.task_info.get("archive_extractions", []):
            source = self._resolve_under(
                data_root,
                str(specification["source"]),
                field="archive_extractions.source",
            )
            destination = self._resolve_under(
                data_root,
                str(specification["destination"]),
                field="archive_extractions.destination",
            )
            if not source.is_file():
                raise FileNotFoundError(f"Task data archive not found: {source}")
            expected_sha256 = str(specification.get("sha256") or "").strip().lower()
            if expected_sha256:
                actual_sha256 = hashlib.sha256(source.read_bytes()).hexdigest()
                if actual_sha256 != expected_sha256:
                    raise ValueError(
                        f"Task data archive SHA-256 mismatch for {source.name}: "
                        f"expected {expected_sha256}, received {actual_sha256}"
                    )
            with ZipFile(source) as archive:
                infos = archive.infolist()
                if len(infos) > 100_000:
                    raise ValueError("Task data archive contains too many entries")
                total_size = sum(info.file_size for info in infos)
                if total_size > 5_000_000_000:
                    raise ValueError("Task data archive expands beyond the 5 GB safety limit")
                targets: set[Path] = set()
                for info in infos:
                    name = info.filename
                    member = PurePosixPath(name)
                    mode = (info.external_attr >> 16) & 0o170000
                    if (
                        not name
                        or member.is_absolute()
                        or ".." in member.parts
                        or "\\" in name
                        or "\x00" in name
                        or info.flag_bits & 0x1
                        or (
                            mode
                            and mode not in {stat.S_IFREG, stat.S_IFDIR}
                        )
                    ):
                        raise ValueError(f"Unsafe task archive member: {name!r}")
                    target = destination.joinpath(*member.parts)
                    try:
                        resolved_target = target.resolve()
                        resolved_target.relative_to(destination.resolve())
                    except ValueError as exc:
                        raise ValueError(f"Task archive member escapes destination: {name!r}") from exc
                    if resolved_target in targets:
                        raise ValueError(f"Duplicate task archive target: {name!r}")
                    targets.add(resolved_target)
                destination.mkdir(parents=True, exist_ok=False)
                for info in infos:
                    member = PurePosixPath(info.filename)
                    target = destination.joinpath(*member.parts)
                    if info.is_dir():
                        target.mkdir(parents=True, exist_ok=True)
                        continue
                    target.parent.mkdir(parents=True, exist_ok=True)
                    with archive.open(info) as source_handle, target.open("wb") as target_handle:
                        shutil.copyfileobj(source_handle, target_handle)

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
            TOOL_DISCOVERY_MODE_ENV: self.tool_discovery_mode,
            "PYTHONPATH": self._runtime_pythonpath(),
            "CHEMGRAPH_LOG_DIR": str((self.workspace / "tool_logs").resolve()),
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
        }
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
            database_directory = self.workspace / "_opencode"
            database_directory.mkdir(parents=True, exist_ok=True)
            env["OPENCODE_DB"] = str((database_directory / "opencode.db").resolve())
            # OpenCode 1.18 interprets OPENCODE_WORKSPACE_ID as the identifier of
            # an already-created OpenCode workspace/session. A benchmark run ID
            # is not such an identifier and makes `opencode run` fail before the
            # first model call with "Session not found". The per-run database is
            # sufficient to isolate concurrent benchmark executions.
            env.pop("OPENCODE_WORKSPACE_ID", None)
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

    def setup_workspace(self) -> None:
        if not self.task_dir.is_dir():
            raise FileNotFoundError(f"Task not found: {self.task_id}")
        self.workspace.mkdir(parents=True, exist_ok=False)
        source_data = self.task_dir / "data"
        if source_data.exists():
            shutil.copytree(source_data, self.workspace / "data", dirs_exist_ok=True)
        else:
            (self.workspace / "data").mkdir()
        self._extract_task_archives()
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

        catalog = catalog_snapshot(
            include_health=True,
            discovery_mode=self.tool_discovery_mode,
            resource_budget=self.resource_budget_record(),
        )
        (self.workspace / "_toolbox_catalog.json").write_text(
            json.dumps(
                catalog,
                indent=2,
                ensure_ascii=False,
            )
            + "\n",
            encoding="utf-8",
        )
        self.instructions_path.write_text(self._build_instructions(), encoding="utf-8")
        self._write_claude_mcp_config()
        self._write_opencode_config()
        catalog_path = self.workspace / "_toolbox_catalog.json"
        self._write_meta(
            "ready",
            {
                "instruction_bytes": self.instructions_path.stat().st_size,
                "catalog_snapshot_bytes": catalog_path.stat().st_size,
                "mcp_public_tool_count": len(self._mcp_server_specs()[0].get("tools", [])),
            },
        )

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
            if isinstance(supervisor_pid, int) and supervisor_pid > 0:
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
        except Exception as exc:
            termination = "runner_error"
            self._terminate_process_tree()
            background_job_cleanup = self._cancel_workspace_execution_jobs(
                reason=termination
            )
            trace_stop.set()
            trace_thread.join(timeout=2)
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
