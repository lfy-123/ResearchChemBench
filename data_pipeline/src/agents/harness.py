from __future__ import annotations

import json
import os
import shutil
import signal
import subprocess
import tempfile
import time
import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

import jsonschema
from json_repair import repair_json

from src.agents.responses_bridge import ResponsesBridge
from src.contracts import now_utc, write_json
from src.model_client import DEFAULT_REMOTE_API_PROXY


@dataclass(frozen=True)
class AgentRunRequest:
    phase: str
    record_id: str
    workspace: Path
    instructions: str
    output_schema: dict[str, Any]
    prompt_version: str
    timeout_seconds: int = 3600
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentRunResult:
    status: str
    response: dict[str, Any] | None
    harness: str
    model: str
    phase: str
    attempt_id: str
    started_at: str
    duration_seconds: float
    command: list[str]
    exit_code: int | None
    workspace: str
    stdout_path: str | None = None
    stderr_path: str | None = None
    final_message_path: str | None = None
    failure_class: str | None = None
    retryable: bool = False
    tool_calls: int = 0
    error: dict[str, Any] | None = None
    receipt_recovered_from_artifact: bool = False
    usage: dict[str, Any] = field(default_factory=dict)
    session_id: str | None = None
    resume_mode: str = "fresh"

    def audit_record(self) -> dict[str, Any]:
        return {key: value for key, value in self.__dict__.items() if key != "response"}


class AgentExecutionError(RuntimeError):
    def __init__(
        self,
        message: str,
        *,
        failure_class: str,
        retryable: bool,
        result: AgentRunResult | None = None,
    ) -> None:
        super().__init__(message)
        self.failure_class = failure_class
        self.retryable = retryable
        self.result = result


def _apply_schema_defaults(value: dict[str, Any], schema: dict[str, Any]) -> dict[str, Any]:
    """Apply only defaults declared explicitly by the response contract."""

    output = json.loads(json.dumps(value, ensure_ascii=False))

    def apply(node: Any, node_schema: Any) -> None:
        if not isinstance(node_schema, dict):
            return
        if isinstance(node, dict):
            for key, child_schema in (node_schema.get("properties") or {}).items():
                if key not in node and isinstance(child_schema, dict) and "default" in child_schema:
                    node[key] = json.loads(json.dumps(child_schema["default"], ensure_ascii=False))
                if key in node:
                    apply(node[key], child_schema)
        elif isinstance(node, list):
            child_schema = node_schema.get("items")
            for child in node:
                apply(child, child_schema)

    apply(output, schema)
    return output


def _validated_structured_response(
    response: dict[str, Any],
    *,
    request: AgentRunRequest,
    workspace: Path,
) -> dict[str, Any]:
    """Validate the final response, falling back to an explicitly contracted JSON artifact.

    File-first Agent phases may correctly finish by writing a full artifact and returning a
    small receipt. The artifact path is supplied by trusted orchestration metadata; arbitrary
    paths from model output are never used for this fallback.
    """

    candidates = [response]
    if len(response) == 1:
        wrapped = next(iter(response.values()))
        if isinstance(wrapped, dict):
            candidates.insert(0, wrapped)
    response_error: jsonschema.ValidationError | None = None
    for candidate in candidates:
        normalized = _apply_schema_defaults(candidate, request.output_schema)
        try:
            jsonschema.validate(normalized, request.output_schema)
            return normalized
        except jsonschema.ValidationError as exc:
            response_error = exc
    assert response_error is not None
    try:
        artifact_value = request.metadata.get("structured_artifact_path")
        if not artifact_value:
            raise response_error
        relative = Path(str(artifact_value))
        if relative.is_absolute() or ".." in relative.parts:
            raise response_error
        artifact = (workspace / relative).resolve()
        try:
            artifact.relative_to(workspace.resolve())
        except ValueError as path_error:
            raise response_error from path_error
        if not artifact.is_file():
            raise response_error
        artifact_response = _apply_schema_defaults(
            _parse_json_object(artifact.read_text(encoding="utf-8", errors="replace")),
            request.output_schema,
        )
        jsonschema.validate(artifact_response, request.output_schema)
        return artifact_response
    except jsonschema.ValidationError as artifact_error:
        raise response_error from artifact_error


def _trusted_artifact_receipt(
    *,
    request: AgentRunRequest,
    workspace: Path,
) -> dict[str, Any] | None:
    """Recover a small receipt only from an orchestration-declared complete artifact.

    Some CLI harnesses can finish all file writes but lose or truncate the final message.
    Recovery is intentionally unavailable unless trusted request metadata fixes the artifact
    directory, required-file allowlist, and receipt body before the Agent starts.
    """

    artifact_value = request.metadata.get("artifact_receipt_path")
    required_values = request.metadata.get("artifact_required_files")
    receipt_value = request.metadata.get("artifact_receipt")
    if (
        not artifact_value
        or not isinstance(required_values, list)
        or not required_values
        or not isinstance(receipt_value, dict)
    ):
        return None

    relative = Path(str(artifact_value))
    if relative.is_absolute() or not relative.parts or ".." in relative.parts:
        return None
    workspace_root = workspace.resolve()
    artifact_root = (workspace_root / relative).resolve()
    try:
        artifact_root.relative_to(workspace_root)
    except ValueError:
        return None
    if not artifact_root.is_dir() or artifact_root.is_symlink():
        return None

    for required_value in required_values:
        required = Path(str(required_value))
        if required.is_absolute() or not required.parts or ".." in required.parts:
            return None
        path = (artifact_root / required).resolve()
        try:
            path.relative_to(artifact_root)
        except ValueError:
            return None
        if not path.is_file() or path.is_symlink() or path.stat().st_size <= 0:
            return None
        if path.suffix.casefold() == ".json":
            try:
                json.loads(path.read_text(encoding="utf-8", errors="strict"))
            except (UnicodeError, ValueError, json.JSONDecodeError):
                return None

    receipt = json.loads(json.dumps(receipt_value, ensure_ascii=False))
    receipt["artifact_path"] = relative.as_posix()
    receipt["receipt_recovered_from_artifact"] = True
    conversion_report = artifact_root.parent / "conversion_report.json"
    if "conversion_report" in receipt and conversion_report.is_file():
        try:
            parsed_report = json.loads(
                conversion_report.read_text(encoding="utf-8", errors="strict")
            )
        except (OSError, UnicodeError, ValueError, json.JSONDecodeError):
            parsed_report = None
        if isinstance(parsed_report, dict):
            receipt["conversion_report"] = parsed_report
    receipt = _apply_schema_defaults(receipt, request.output_schema)
    try:
        jsonschema.validate(receipt, request.output_schema)
    except jsonschema.ValidationError:
        return None
    return receipt


def _recover_trusted_workspace_response(
    *, request: AgentRunRequest, workspace: Path
) -> dict[str, Any] | None:
    """Recover a valid result when the CLI final message is absent or malformed."""

    try:
        return _validated_structured_response({}, request=request, workspace=workspace)
    except (jsonschema.ValidationError, ValueError, json.JSONDecodeError):
        return _trusted_artifact_receipt(request=request, workspace=workspace)


def _codex_stdout_usage(path: Path) -> dict[str, Any]:
    """Read cumulative token usage from Codex's terminal JSONL event stream."""

    if not path.is_file():
        return {}
    try:
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError:
        return {}
    completed: list[dict[str, Any]] = []
    for line in lines:
        try:
            event = json.loads(line)
        except (TypeError, ValueError, json.JSONDecodeError):
            continue
        if event.get("type") == "turn.completed" and isinstance(event.get("usage"), dict):
            completed.append(event["usage"])
    if not completed:
        return {}
    usage = completed[-1]
    prompt = int(usage.get("input_tokens") or 0)
    cache_hit = int(usage.get("cached_input_tokens") or 0)
    output = int(usage.get("output_tokens") or 0)
    reasoning = int(usage.get("reasoning_output_tokens") or 0)
    return {
        "source": "codex_turn_completed",
        "request_count": len(completed),
        "prompt_tokens": prompt,
        "prompt_cache_hit_tokens": cache_hit,
        "prompt_cache_miss_tokens": max(0, prompt - cache_hit),
        "cache_write_input_tokens": int(usage.get("cache_write_input_tokens") or 0),
        "completion_tokens": output,
        "reasoning_output_tokens": reasoning,
        "total_tokens": prompt + output,
    }


def _agent_usage_summary(
    bridge: ResponsesBridge | None, stdout_path: Path
) -> dict[str, Any]:
    bridge_usage = bridge.usage_summary() if bridge is not None else {}
    if int(bridge_usage.get("total_tokens") or 0) > 0:
        return {"source": "responses_bridge", **bridge_usage}
    return _codex_stdout_usage(stdout_path) or bridge_usage


class AgentHarness(ABC):
    def __init__(
        self,
        *,
        name: str,
        config: dict[str, Any],
        model_config: dict[str, Any],
        model_client: Any = None,
    ) -> None:
        self.name = name
        self.config = dict(config)
        self.model_config = dict(model_config)
        self.model_client = model_client

    @property
    def model(self) -> str:
        return str(self.model_config.get("model") or "")

    @abstractmethod
    def run(self, request: AgentRunRequest) -> AgentRunResult:
        raise NotImplementedError

    def command_preview(self, request: AgentRunRequest) -> list[str]:
        raise NotImplementedError


class CliAgentHarness(AgentHarness):
    executable = ""

    def run(self, request: AgentRunRequest) -> AgentRunResult:
        workspace = request.workspace.expanduser().resolve()
        workspace.mkdir(parents=True, exist_ok=True)
        instruction_path = workspace / "INSTRUCTIONS.md"
        schema_path = workspace / "output.schema.json"
        stdout_path = workspace / "_agent_stdout.jsonl"
        stderr_path = workspace / "_agent_stderr.log"
        final_path = workspace / "_final_message.txt"
        instruction_path.write_text(request.instructions, encoding="utf-8")
        write_json(schema_path, request.output_schema)
        attempt_id = f"attempt_{uuid.uuid4().hex[:12]}"
        started_at = now_utc()
        started = time.monotonic()
        bridge: ResponsesBridge | None = None
        process: subprocess.Popen[str] | None = None
        isolation_root: Path | None = None
        command: list[str] = []
        exit_code: int | None = None
        receipt_recovered_from_artifact = False
        try:
            if shutil.which(self.executable) is None:
                raise AgentExecutionError(
                    f"Agent executable is not installed: {self.executable}",
                    failure_class="harness_unavailable",
                    retryable=True,
                )
            bridge = self._bridge(request)
            if bridge is not None:
                bridge.__enter__()
            command = self._build_command(
                request=request,
                instruction_path=instruction_path,
                schema_path=schema_path,
                final_path=final_path,
                bridge=bridge,
            )
            if bool(self.config.get("filesystem_isolation", True)) and os.name == "posix":
                command, isolation_root = self._isolate_command(
                    command, workspace, request=request
                )
            environment = self._environment(bridge, request=request)
            response: dict[str, Any] | None = None
            with (
                stdout_path.open("w", encoding="utf-8") as stdout,
                stderr_path.open("w", encoding="utf-8") as stderr,
            ):
                process = subprocess.Popen(
                    command,
                    cwd=workspace,
                    env=environment,
                    stdout=stdout,
                    stderr=stderr,
                    text=True,
                    start_new_session=os.name == "posix",
                )
                try:
                    exit_code = process.wait(timeout=request.timeout_seconds)
                except subprocess.TimeoutExpired as exc:
                    self._terminate(process)
                    response = _trusted_artifact_receipt(
                        request=request,
                        workspace=workspace,
                    )
                    if response is None:
                        raise AgentExecutionError(
                            f"{self.name} timed out after {request.timeout_seconds} seconds",
                            failure_class="agent_timeout",
                            retryable=True,
                        ) from exc
                    receipt_recovered_from_artifact = True
            if exit_code != 0 and response is None:
                stderr_tail = _tail(stderr_path, 5000)
                failure_class, retryable = classify_cli_failure(stderr_tail)
                raise AgentExecutionError(
                    f"{self.name} exited with code {exit_code}: {stderr_tail[-1000:]}",
                    failure_class=failure_class,
                    retryable=retryable,
                )
            session_metadata = self._extract_session_metadata(stdout_path)
            requested_session_id = str(
                request.metadata.get("codex_resume_session_id") or ""
            ).strip()
            if session_metadata is None and requested_session_id:
                session_metadata = {
                    "session_id": requested_session_id,
                    "source": "explicit_codex_resume_request",
                }
            if session_metadata:
                write_json(workspace / "codex_session.json", session_metadata)
            if response is None:
                try:
                    response = self._parse_response(stdout_path, final_path)
                    response = _validated_structured_response(
                        response,
                        request=request,
                        workspace=workspace,
                    )
                except (jsonschema.ValidationError, ValueError, json.JSONDecodeError):
                    recovered = _recover_trusted_workspace_response(
                        request=request,
                        workspace=workspace,
                    )
                    if recovered is None:
                        raise
                    response = recovered
                    receipt_recovered_from_artifact = True
            result = AgentRunResult(
                status="succeeded",
                response=response,
                harness=self.name,
                model=self.model,
                phase=request.phase,
                attempt_id=attempt_id,
                started_at=started_at,
                duration_seconds=round(time.monotonic() - started, 3),
                command=_redact_command(command),
                exit_code=exit_code,
                workspace=str(workspace),
                stdout_path=str(stdout_path),
                stderr_path=str(stderr_path),
                final_message_path=str(final_path) if final_path.exists() else None,
                tool_calls=bridge.tool_call_count if bridge is not None else 0,
                usage=_agent_usage_summary(bridge, stdout_path),
                receipt_recovered_from_artifact=receipt_recovered_from_artifact,
                session_id=(session_metadata or {}).get("session_id"),
                resume_mode=(
                    "native_session" if requested_session_id else "fresh"
                ),
            )
            write_json(workspace / "agent_run.json", result.audit_record())
            return result
        except AgentExecutionError as exc:
            result = AgentRunResult(
                status="failed",
                response=None,
                harness=self.name,
                model=self.model,
                phase=request.phase,
                attempt_id=attempt_id,
                started_at=started_at,
                duration_seconds=round(time.monotonic() - started, 3),
                command=_redact_command(command),
                exit_code=exit_code,
                workspace=str(workspace),
                stdout_path=str(stdout_path) if stdout_path.exists() else None,
                stderr_path=str(stderr_path) if stderr_path.exists() else None,
                final_message_path=str(final_path) if final_path.exists() else None,
                failure_class=exc.failure_class,
                retryable=exc.retryable,
                tool_calls=bridge.tool_call_count if bridge is not None else 0,
                usage=_agent_usage_summary(bridge, stdout_path),
                error={"error_type": type(exc).__name__, "message": str(exc)},
                session_id=(self._extract_session_metadata(stdout_path) or {}).get(
                    "session_id"
                )
                or str(request.metadata.get("codex_resume_session_id") or "").strip()
                or None,
                resume_mode=(
                    "native_session"
                    if request.metadata.get("codex_resume_session_id")
                    else "fresh"
                ),
            )
            write_json(workspace / "agent_run.json", result.audit_record())
            exc.result = result
            raise
        except (jsonschema.ValidationError, ValueError, json.JSONDecodeError) as exc:
            result = AgentRunResult(
                status="failed",
                response=None,
                harness=self.name,
                model=self.model,
                phase=request.phase,
                attempt_id=attempt_id,
                started_at=started_at,
                duration_seconds=round(time.monotonic() - started, 3),
                command=_redact_command(command),
                exit_code=exit_code,
                workspace=str(workspace),
                stdout_path=str(stdout_path) if stdout_path.exists() else None,
                stderr_path=str(stderr_path) if stderr_path.exists() else None,
                final_message_path=str(final_path) if final_path.exists() else None,
                failure_class="invalid_agent_output",
                retryable=True,
                tool_calls=bridge.tool_call_count if bridge is not None else 0,
                usage=_agent_usage_summary(bridge, stdout_path),
                error={"error_type": type(exc).__name__, "message": str(exc)[:3000]},
                session_id=(self._extract_session_metadata(stdout_path) or {}).get(
                    "session_id"
                )
                or str(request.metadata.get("codex_resume_session_id") or "").strip()
                or None,
                resume_mode=(
                    "native_session"
                    if request.metadata.get("codex_resume_session_id")
                    else "fresh"
                ),
            )
            write_json(workspace / "agent_run.json", result.audit_record())
            raise AgentExecutionError(
                f"{self.name} returned invalid structured output: {exc}",
                failure_class="invalid_agent_output",
                retryable=True,
                result=result,
            ) from exc
        finally:
            if bridge is not None:
                bridge.__exit__(None, None, None)
            if isolation_root is not None:
                shutil.rmtree(isolation_root, ignore_errors=True)

    def command_preview(self, request: AgentRunRequest) -> list[str]:
        workspace = request.workspace.resolve()
        return self._build_command(
            request=request,
            instruction_path=workspace / "INSTRUCTIONS.md",
            schema_path=workspace / "output.schema.json",
            final_path=workspace / "_final_message.txt",
            bridge=None,
        )

    def _bridge(self, request: AgentRunRequest) -> ResponsesBridge | None:
        return None

    def _environment(
        self,
        bridge: ResponsesBridge | None,
        *,
        request: AgentRunRequest | None = None,
    ) -> dict[str, str]:
        environment = os.environ.copy()
        environment["PYTHONUNBUFFERED"] = "1"
        return environment

    def _extract_session_metadata(self, stdout_path: Path) -> dict[str, Any] | None:
        """Optional persisted-session hook for CLI harnesses."""

        return None

    def _isolate_command(
        self,
        command: list[str],
        workspace: Path,
        *,
        request: AgentRunRequest | None = None,
    ) -> tuple[list[str], Path]:
        unshare = shutil.which("unshare")
        executable = shutil.which(str(self.config.get("executable") or self.executable))
        if not unshare or not executable:
            raise AgentExecutionError(
                "mount-namespace filesystem isolation is unavailable",
                failure_class="harness_isolation_unavailable",
                retryable=False,
            )
        root = Path(tempfile.mkdtemp(prefix="rcb-agent-rootfs-"))
        helper = Path(__file__).with_name("namespace_exec.py").resolve()
        isolated = [
                unshare,
                "--user",
                "--map-root-user",
                "--mount",
                "--pid",
                "--fork",
                str(Path(os.sys.executable).resolve()),
                str(helper),
                "--workspace",
                str(workspace),
                "--rootfs",
                str(root),
                "--executable",
                executable,
            ]
        metadata = request.metadata if request is not None else {}
        if bool(metadata.get("codex_native_resume")):
            raw_session_home = str(metadata.get("codex_session_home") or "").strip()
            if raw_session_home:
                session_home = Path(raw_session_home).expanduser().resolve()
                session_home.mkdir(parents=True, exist_ok=True)
                isolated.extend(["--codex-home", str(session_home)])
        isolated.extend(["--", *command])
        return isolated, root

    @abstractmethod
    def _build_command(
        self,
        *,
        request: AgentRunRequest,
        instruction_path: Path,
        schema_path: Path,
        final_path: Path,
        bridge: ResponsesBridge | None,
    ) -> list[str]:
        raise NotImplementedError

    @abstractmethod
    def _parse_response(self, stdout_path: Path, final_path: Path) -> dict[str, Any]:
        raise NotImplementedError

    @staticmethod
    def _terminate(process: subprocess.Popen[str]) -> None:
        if process.poll() is not None:
            return
        if os.name == "posix":
            try:
                os.killpg(process.pid, signal.SIGTERM)
                process.wait(timeout=10)
                return
            except (ProcessLookupError, subprocess.TimeoutExpired):
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                return
        process.kill()


class CodexHarness(CliAgentHarness):
    executable = "codex"

    def _bridge(self, request: AgentRunRequest) -> ResponsesBridge | None:
        wire_api = str(
            request.metadata.get("codex_wire_api")
            or self.model_config.get("codex_wire_api")
            or self.config.get("codex_wire_api")
            or "chat_completions"
        ).casefold()
        if wire_api == "responses":
            return None
        key_name = str(self.model_config.get("api_key_env") or "")
        api_key = os.environ.get(key_name, "")
        if not api_key:
            raise AgentExecutionError(
                f"missing API key environment variable: {key_name}",
                failure_class="missing_credentials",
                retryable=True,
            )
        artifact_value = request.metadata.get("structured_artifact_path")
        artifact_path: Path | None = None
        if artifact_value:
            artifact_relative = Path(str(artifact_value))
            if artifact_relative.is_absolute() or ".." in artifact_relative.parts:
                raise AgentExecutionError(
                    "structured artifact path must be workspace-relative",
                    failure_class="invalid_agent_configuration",
                    retryable=False,
                )
            artifact_path = (request.workspace / artifact_relative).resolve()
            try:
                artifact_path.relative_to(request.workspace.resolve())
            except ValueError as exc:
                raise AgentExecutionError(
                    "structured artifact path escapes the Agent workspace",
                    failure_class="invalid_agent_configuration",
                    retryable=False,
                ) from exc
        file_first_value = request.metadata.get("artifact_receipt_path")
        file_first_path: Path | None = None
        file_first_required_files: list[str] = []
        file_first_required_modified_files: list[str] = []
        if file_first_value:
            file_first_relative = Path(str(file_first_value))
            if file_first_relative.is_absolute() or ".." in file_first_relative.parts:
                raise AgentExecutionError(
                    "file-first artifact path must be workspace-relative",
                    failure_class="invalid_agent_configuration",
                    retryable=False,
                )
            file_first_path = (request.workspace / file_first_relative).resolve()
            try:
                file_first_path.relative_to(request.workspace.resolve())
            except ValueError as exc:
                raise AgentExecutionError(
                    "file-first artifact path escapes the Agent workspace",
                    failure_class="invalid_agent_configuration",
                    retryable=False,
                ) from exc
            for value in request.metadata.get("artifact_required_files") or []:
                relative = Path(str(value))
                if relative.is_absolute() or ".." in relative.parts:
                    raise AgentExecutionError(
                        "file-first required file must be artifact-relative",
                        failure_class="invalid_agent_configuration",
                        retryable=False,
                    )
                file_first_required_files.append(relative.as_posix())
            for value in request.metadata.get("artifact_required_modified_files") or []:
                relative = Path(str(value))
                if relative.is_absolute() or ".." in relative.parts:
                    raise AgentExecutionError(
                        "file-first modified file must be artifact-relative",
                        failure_class="invalid_agent_configuration",
                        retryable=False,
                    )
                file_first_required_modified_files.append(relative.as_posix())
        return ResponsesBridge(
            upstream_base_url=str(self.model_config["base_url"]),
            api_key=api_key,
            model=self.model,
            timeout_seconds=float(self.model_config.get("timeout_seconds", 900)),
            proxy_url=_model_proxy_url(self.model_config),
            chat_template_kwargs=self.model_config.get("chat_template_kwargs"),
            thinking=self.model_config.get("thinking"),
            reasoning_mode=self.model_config.get("reasoning_mode"),
            max_tokens=int(self.model_config.get("max_tokens", 16384)),
            structured_finalization_max_tokens=int(
                self.config.get("structured_finalization_max_tokens", 32768)
            ),
            prefer_json_schema=bool(
                request.metadata.get(
                    "codex_chat_json_schema",
                    self.config.get("codex_chat_json_schema", False),
                )
            ),
            tool_choice_policy=str(
                request.metadata.get("tool_choice_policy")
                or self.model_config.get(
                    "tool_choice_policy", self.config.get("tool_choice_policy", "auto")
                )
            ),
            response_format_policy=str(
                request.metadata.get("response_format_policy")
                or self.model_config.get(
                    "response_format_policy",
                    self.config.get("response_format_policy", "auto"),
                )
            ),
            structured_finalization_via_submit_tool=bool(
                self.config.get("codex_structured_final_tool", False)
            ),
            max_tool_calls=int(
                request.metadata["max_tool_calls"]
                if request.metadata.get("max_tool_calls") is not None
                else self.config.get("max_tool_calls", 24)
            ),
            finalization_reserve=int(
                request.metadata["finalization_reserve"]
                if request.metadata.get("finalization_reserve") is not None
                else self.config.get("finalization_reserve", 4)
            ),
            artifact_finalization_required=not bool(
                request.metadata.get("inline_contract", False)
            ),
            structured_artifact_path=artifact_path,
            file_first_artifact_path=file_first_path,
            file_first_required_files=file_first_required_files,
            file_first_required_modified_files=file_first_required_modified_files,
            retries=int(self.model_config.get("retries", 2)),
        )

    def _environment(
        self,
        bridge: ResponsesBridge | None,
        *,
        request: AgentRunRequest | None = None,
    ) -> dict[str, str]:
        environment = super()._environment(bridge, request=request)
        for key in list(environment):
            if key.endswith("_API_KEY") or key in {
                "OPENAI_API_KEY",
                "CODEX_API_KEY",
                "ANTHROPIC_API_KEY",
            }:
                environment.pop(key, None)
        for key in {
            "HTTP_PROXY",
            "HTTPS_PROXY",
            "ALL_PROXY",
            "http_proxy",
            "https_proxy",
            "all_proxy",
        }:
            environment.pop(key, None)
        # Direct Responses mode sends the request from Codex to the configured
        # upstream. Keep the role credential inside the child only for that
        # mode; bridge mode intentionally never exports it.
        if bridge is None:
            key_name = str(self.model_config.get("api_key_env") or "")
            api_key = os.environ.get(key_name, "")
            if api_key:
                environment["OPENAI_API_KEY"] = api_key
        request_metadata = request.metadata if request is not None else {}
        native_resume = bool(
            request_metadata.get(
                "codex_native_resume",
                self.config.get("codex_native_resume", False),
            )
        )
        if native_resume:
            # Sessions share one run-local store, but every resume uses an
            # explicit UUID.  Never use `--last`: concurrent papers must not
            # be able to select one another's conversation.
            raw_session_home = str(
                request_metadata.get("codex_session_home")
                or self.config.get("codex_session_home")
                or ""
            ).strip()
            session_home = (
                Path(raw_session_home).expanduser().resolve()
                if raw_session_home
                else Path(os.environ.get("TMPDIR", "/tmp"))
                / f"rcb-codex-sessions-{os.getuid()}"
            )
            session_home.mkdir(parents=True, exist_ok=True)
            environment["CODEX_HOME"] = str(session_home)
        return environment

    def _extract_session_metadata(self, stdout_path: Path) -> dict[str, Any] | None:
        if not stdout_path.is_file():
            return None
        session_id = ""
        try:
            lines = stdout_path.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            return None
        for line in lines:
            try:
                event = json.loads(line)
            except (TypeError, ValueError, json.JSONDecodeError):
                continue
            if event.get("type") == "thread.started":
                session_id = str(
                    event.get("thread_id") or event.get("threadId") or event.get("id") or ""
                ).strip()
                if session_id:
                    break
        return {"session_id": session_id, "source": "codex_thread_started"} if session_id else None

    def _build_command(
        self,
        *,
        request: AgentRunRequest,
        instruction_path: Path,
        schema_path: Path,
        final_path: Path,
        bridge: ResponsesBridge | None,
    ) -> list[str]:
        base_url = (
            bridge.base_url
            if bridge is not None
            else str(self.model_config.get("base_url") or "").rstrip("/")
        )
        provider = "rcb_pipeline"
        native_resume_value = request.metadata.get("codex_native_resume")
        native_resume = bool(
            self.config.get("codex_native_resume", False)
            if native_resume_value is None
            else native_resume_value
        )
        resume_session_id = str(request.metadata.get("codex_resume_session_id") or "").strip()
        command = [
            str(self.config.get("executable") or self.executable),
            "exec",
        ]
        if resume_session_id:
            # `-C` and the sandbox are parent `exec` options.  Supplying them
            # before the resume subcommand makes the recovered conversation
            # operate on the newly staged recovery workspace.
            command.extend(
                [
                    "-C",
                    str(request.workspace.resolve()),
                    "--sandbox",
                    "danger-full-access",
                    "resume",
                    resume_session_id,
                ]
            )
        command.extend([
            "--ignore-user-config",
            "--ignore-rules",
            "--skip-git-repo-check",
            "--json",
            "--output-schema",
            str(schema_path.resolve()),
            "--output-last-message",
            str(final_path.resolve()),
            "-m",
            self.model,
            "-c",
            f'model_provider="{provider}"',
            "-c",
            f'model_providers.{provider}.name="ResearchChemBench"',
            "-c",
            f"model_providers.{provider}.base_url={json.dumps(base_url)}",
            "-c",
            # Codex CLI speaks its Responses protocol to the local bridge.  The
            # model-level codex_wire_api controls the bridge's upstream wire;
            # it must not be passed through as a Codex CLI enum (which currently
            # accepts only `responses`).
            f'model_providers.{provider}.wire_api="responses"',
            "-c",
            f"model_providers.{provider}.requires_openai_auth={'true' if bridge is None else 'false'}",
            "-c",
            'approval_policy="never"',
            "-c",
            f"model_context_window={int(self.config.get('model_context_window', 1_000_000))}",
            "-c",
            f"model_auto_compact_token_limit={int(self.config.get('model_auto_compact_token_limit', 750_000))}",
            "-c",
            f"model_auto_compact_token_limit_scope={json.dumps(str(self.config.get('model_auto_compact_token_limit_scope', 'total')))}",
            "-c",
            "sandbox_workspace_write.network_access=false",
        ])
        if not resume_session_id:
            if not native_resume:
                command.insert(5, "--ephemeral")
            command.extend(["-C", str(request.workspace.resolve()), "--sandbox", "danger-full-access"])
        if bool(self.config.get("codex_disable_code_mode", False)):
            command.extend(
                [
                    "--disable",
                    "code_mode",
                    "--disable",
                    "code_mode_host",
                ]
            )
        reasoning_effort = (
            request.metadata.get("reasoning_effort")
            or self.model_config.get("reasoning_effort")
            or self.config.get("reasoning_effort")
        )
        if reasoning_effort:
            command.extend(
                [
                    "-c",
                    f"model_reasoning_effort={json.dumps(str(reasoning_effort).casefold())}",
                ]
            )
        command.append(request.instructions)
        return command

    def _parse_response(self, stdout_path: Path, final_path: Path) -> dict[str, Any]:
        if not final_path.is_file():
            raise ValueError("Codex did not create --output-last-message")
        return _parse_json_object(final_path.read_text(encoding="utf-8", errors="replace"))


class ClaudeHarness(CliAgentHarness):
    executable = "claude"

    def _build_command(
        self,
        *,
        request: AgentRunRequest,
        instruction_path: Path,
        schema_path: Path,
        final_path: Path,
        bridge: ResponsesBridge | None,
    ) -> list[str]:
        return [
            str(self.config.get("executable") or self.executable),
            "-p",
            "--output-format",
            "json",
            "--max-turns",
            str(int(self.config.get("max_turns", 24))),
            "--tools",
            "Read,Glob,Grep",
            "--allowedTools",
            "Read,Glob,Grep",
            "--permission-mode",
            "dontAsk",
            "--disable-slash-commands",
            "--no-session-persistence",
            "--model",
            self.model,
            request.instructions,
        ]

    def _parse_response(self, stdout_path: Path, final_path: Path) -> dict[str, Any]:
        wrapper = json.loads(stdout_path.read_text(encoding="utf-8"))
        content = wrapper.get("result") if isinstance(wrapper, dict) else None
        if not isinstance(content, str):
            raise ValueError("Claude JSON output does not contain a result string")
        return _parse_json_object(content)


class OpenCodeHarness(CliAgentHarness):
    executable = "opencode"

    def _environment(
        self,
        bridge: ResponsesBridge | None,
        *,
        request: AgentRunRequest | None = None,
    ) -> dict[str, str]:
        environment = super()._environment(bridge, request=request)
        key_name = str(self.model_config.get("api_key_env") or "")
        api_key = os.environ.get(key_name, "")
        if not api_key:
            raise AgentExecutionError(
                f"missing API key environment variable: {key_name}",
                failure_class="missing_credentials",
                retryable=True,
            )
        environment["OPENAI_API_KEY"] = api_key
        runtime_root = Path(tempfile.gettempdir()) / "researchchembench-pipeline-opencode"
        runtime_root.mkdir(parents=True, exist_ok=True)
        environment["OPENCODE_DB"] = str(runtime_root / f"{uuid.uuid4().hex}.db")
        environment.pop("OPENCODE_WORKSPACE_ID", None)
        return environment

    def _write_config(self, workspace: Path) -> tuple[str, str]:
        provider = str(self.config.get("provider") or "rcb")
        model_id = self.model.split("/", 1)[-1]
        qualified = f"{provider}/{model_id}"
        config = {
            "$schema": "https://opencode.ai/config.json",
            "model": qualified,
            "small_model": qualified,
            "provider": {
                provider: {
                    "npm": "@ai-sdk/openai-compatible",
                    "name": "ResearchChemBench",
                    "options": {
                        "baseURL": str(self.model_config.get("base_url") or ""),
                        "apiKey": "{env:OPENAI_API_KEY}",
                    },
                    "models": {model_id: {"name": model_id}},
                }
            },
            "agent": {
                "build": {"steps": int(self.config.get("max_turns", 24))},
                "general": {"steps": int(self.config.get("max_turns", 24))},
            },
        }
        write_json(workspace / "opencode.json", config)
        return provider, qualified

    def _build_command(
        self,
        *,
        request: AgentRunRequest,
        instruction_path: Path,
        schema_path: Path,
        final_path: Path,
        bridge: ResponsesBridge | None,
    ) -> list[str]:
        _provider, model = self._write_config(request.workspace.resolve())
        return [
            str(self.config.get("executable") or self.executable),
            "run",
            "--pure",
            "--dir",
            str(request.workspace.resolve()),
            "--model",
            model,
            "--format",
            "json",
            "--auto",
            request.instructions,
        ]

    def _parse_response(self, stdout_path: Path, final_path: Path) -> dict[str, Any]:
        candidates: list[str] = []
        for line in stdout_path.read_text(encoding="utf-8", errors="replace").splitlines():
            try:
                value = json.loads(line)
            except json.JSONDecodeError:
                continue
            candidates.extend(_recursive_text_values(value))
        for candidate in reversed(candidates):
            try:
                return _parse_json_object(candidate)
            except (ValueError, json.JSONDecodeError):
                continue
        raise ValueError("OpenCode output did not contain a JSON object response")


class DirectApiHarness(AgentHarness):
    """Deprecated compatibility adapter for pre-Agent configurations."""

    def run(self, request: AgentRunRequest) -> AgentRunResult:
        if self.model_client is None:
            raise AgentExecutionError(
                "direct_api compatibility requires a RoleModelClient",
                failure_class="harness_configuration",
                retryable=False,
            )
        request.workspace.mkdir(parents=True, exist_ok=True)
        (request.workspace / "INSTRUCTIONS.md").write_text(request.instructions, encoding="utf-8")
        started_at = now_utc()
        started = time.monotonic()
        response, audit = self.model_client.call_json(
            namespace=request.phase,
            record_id=request.record_id,
            prompt_version=request.prompt_version,
            system_prompt=(
                "Follow the supplied role and return exactly one JSON object matching the "
                "requested contract. You cannot browse files, so use the inline packet."
            ),
            user_content=request.instructions,
            max_tokens=int(self.config.get("max_tokens", 8192)),
        )
        response = _apply_schema_defaults(response, request.output_schema)
        jsonschema.validate(response, request.output_schema)
        write_json(request.workspace / "direct_api_audit.json", audit)
        return AgentRunResult(
            status="succeeded",
            response=response,
            harness=self.name,
            model=self.model,
            phase=request.phase,
            attempt_id=f"attempt_{uuid.uuid4().hex[:12]}",
            started_at=started_at,
            duration_seconds=round(time.monotonic() - started, 3),
            command=["direct_api"],
            exit_code=0,
            workspace=str(request.workspace),
        )


class MockHarness(AgentHarness):
    def run(self, request: AgentRunRequest) -> AgentRunResult:
        responder: Callable[[AgentRunRequest], dict[str, Any]] | None = self.config.get(
            "mock_responder"
        )
        responses = self.config.get("mock_responses") or {}
        response = responder(request) if responder else responses.get(request.phase)
        if response is None:
            raise AgentExecutionError(
                f"no mock response configured for {request.phase}",
                failure_class="mock_response_missing",
                retryable=False,
            )
        response = _apply_schema_defaults(response, request.output_schema)
        jsonschema.validate(response, request.output_schema)
        request.workspace.mkdir(parents=True, exist_ok=True)
        write_json(request.workspace / "mock_response.json", response)
        return AgentRunResult(
            status="succeeded",
            response=response,
            harness=self.name,
            model=self.model or "mock",
            phase=request.phase,
            attempt_id=f"attempt_{uuid.uuid4().hex[:12]}",
            started_at=now_utc(),
            duration_seconds=0.0,
            command=["mock"],
            exit_code=0,
            workspace=str(request.workspace),
        )


def create_agent_harness(
    name: str,
    *,
    config: dict[str, Any],
    model_config: dict[str, Any],
    model_client: Any = None,
) -> AgentHarness:
    normalized = str(name or "").strip().casefold()
    classes: dict[str, type[AgentHarness]] = {
        "codex": CodexHarness,
        "claude": ClaudeHarness,
        "opencode": OpenCodeHarness,
        "direct_api": DirectApiHarness,
        "mock": MockHarness,
    }
    if normalized not in classes:
        raise ValueError(
            f"unsupported Agent harness {name!r}; expected codex, claude, opencode, or mock"
        )
    return classes[normalized](
        name=normalized,
        config=config,
        model_config=model_config,
        model_client=model_client,
    )


def classify_cli_failure(text: str) -> tuple[str, bool]:
    normalized = text.casefold()
    if any(value in normalized for value in ("timed out", "timeout", "deadline exceeded")):
        return "agent_timeout", True
    if any(
        value in normalized
        for value in (
            "connection reset",
            "connection refused",
            "connection failed",
            "502 bad gateway",
            "503 service unavailable",
            "504 gateway timeout",
            "rate limit",
            "capacity",
        )
    ):
        return "model_endpoint_unavailable", True
    if "not found" in normalized and any(
        name in normalized for name in ("codex", "claude", "opencode")
    ):
        return "harness_unavailable", True
    if any(value in normalized for value in ("unauthorized", "forbidden", "invalid api key")):
        return "authentication_failed", True
    return "agent_process_failed", True


def _parse_json_object(content: str) -> dict[str, Any]:
    cleaned = content.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    try:
        value = json.loads(cleaned)
    except json.JSONDecodeError:
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start < 0 or end <= start:
            raise
        value = repair_json(cleaned[start : end + 1], return_objects=True)
    if not isinstance(value, dict):
        raise ValueError("Agent final response must be one JSON object")
    return value


def _recursive_text_values(value: Any) -> list[str]:
    output: list[str] = []
    if isinstance(value, str):
        output.append(value)
    elif isinstance(value, list):
        for item in value:
            output.extend(_recursive_text_values(item))
    elif isinstance(value, dict):
        for key, item in value.items():
            if key in {"text", "content", "result", "message"}:
                output.extend(_recursive_text_values(item))
    return output


def _model_proxy_url(config: dict[str, Any]) -> str | None:
    if not bool(config.get("use_proxy", True)):
        return None
    env_name = str(config.get("proxy_url_env") or "HTTPS_PROXY")
    return str(
        os.environ.get(env_name)
        or os.environ.get(env_name.lower())
        or config.get("proxy_url")
        or DEFAULT_REMOTE_API_PROXY
    )


def _tail(path: Path, characters: int) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")[-characters:]


def _redact_command(command: list[str]) -> list[str]:
    # Commands contain paths, model names, and prompts but never credentials.
    # Replace the full prompt to keep run records compact and prevent evidence
    # or hidden-reference text from leaking into public audit summaries.
    if not command:
        return []
    output = list(command)
    if output:
        output[-1] = "<PROMPT>"
    return output
